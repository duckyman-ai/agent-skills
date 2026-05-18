#!/usr/bin/env python3
"""Edit video clips in a CapCut desktop project.

Supports: scale, rotate, flip, opacity, speed, volume, trim, split, remove, reorder.
Audio track operations: volume, mute, speed, trim, remove, position, fade in/out.

Usage:
    # Show project timeline
    python3 edit-clips.py <project> --info

    # Video: scale, speed, volume, trim, split, remove, move, reset
    python3 edit-clips.py <project> --scale 1.2 --clips 0 5 10
    python3 edit-clips.py <project> --speed 2.0 --all
    python3 edit-clips.py <project> --trim 3.5 --clips 0
    python3 edit-clips.py <project> --split 2.5 --clips 0
    python3 edit-clips.py <project> --remove --clips 10 11 12
    python3 edit-clips.py <project> --move 5 --to 10

    # Audio: volume, mute, speed, trim, remove, position, fade
    python3 edit-clips.py <project> --audio-track --volume 0.5 --all
    python3 edit-clips.py <project> --audio-track --position 10.5 --clips 0
    python3 edit-clips.py <project> --audio-track --fade-in 0.5 --clips 0

Requires CapCut to be CLOSED.
"""

import argparse, copy, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import (
    BASE, US, check_capcut_closed, gen_uuid, get_video_track,
    load_project, resolve_indices, save_draft,
)


def find_speed_material(draft, seg):
    speed_ids = {s["id"] for s in draft["materials"]["speeds"]}
    for ref in seg.get("extra_material_refs", []):
        if ref in speed_ids:
            for s in draft["materials"]["speeds"]:
                if s["id"] == ref:
                    return s
    return None


def find_audio_fade(draft, seg):
    fade_ids = {f["id"] for f in draft["materials"]["audio_fades"]}
    for ref in seg.get("extra_material_refs", []):
        if ref in fade_ids:
            for f in draft["materials"]["audio_fades"]:
                if f["id"] == ref:
                    return f
    return None


def make_audio_fade():
    return {
        "id": gen_uuid(),
        "type": "audio_fade",
        "fade_type": 0,
        "fade_in_duration": 0,
        "fade_out_duration": 0,
    }


def show_info(draft):
    print(f"Duration: {draft.get('duration', 0) / US:.1f}s")
    print(f"FPS: {draft.get('fps')}")
    cc = draft.get("canvas_config", {})
    print(f"Canvas: {cc.get('width')}x{cc.get('height')}")
    print()

    videos = {v["id"]: v for v in draft["materials"].get("videos", [])}

    for i, track in enumerate(draft.get("tracks", [])):
        segs = track.get("segments", [])
        print(f"Track {i}: {track['type']} ({len(segs)} segments)")
        if track["type"] == "video":
            for j, seg in enumerate(segs):
                tr = seg["target_timerange"]
                sr = seg["source_timerange"]
                vid = videos.get(seg["material_id"])
                name = vid["path"].split("/")[-1][:30] if vid else "?"
                clip = seg.get("clip", {})
                flags = []
                if seg.get("speed", 1.0) != 1.0:
                    flags.append(f"spd={seg['speed']}")
                if seg.get("volume", 1.0) != 1.0:
                    flags.append(f"vol={seg['volume']:.2f}")
                if clip.get("scale", {}).get("x", 1.0) != 1.0:
                    flags.append(f"scale={clip['scale']['x']}")
                if clip.get("rotation", 0):
                    flags.append(f"rot={clip['rotation']}")
                flag_str = f"  [{', '.join(flags)}]" if flags else ""
                print(f"  [{j:>3d}] {tr['start']/US:>8.2f}s  +{tr['duration']/US:>6.2f}s  "
                      f"src={sr['start']/US:.1f}s  {name}{flag_str}")
        elif track["type"] == "audio":
            for j, seg in enumerate(segs):
                tr = seg["target_timerange"]
                vol = seg.get("volume", 1.0)
                print(f"  [{j:>3d}] {tr['start']/US:>8.2f}s  +{tr['duration']/US:>6.2f}s  vol={vol:.2f}")
        elif track["type"] == "text":
            texts = {t["id"]: t for t in draft["materials"].get("texts", [])}
            for j, seg in enumerate(segs):
                tr = seg["target_timerange"]
                txt = texts.get(seg["material_id"])
                text_str = ""
                if txt:
                    try:
                        content = json.loads(txt.get("content", "{}"))
                        text_str = content.get("text", "")[:30]
                    except Exception:
                        pass
                print(f"  [{j:>3d}] {tr['start']/US:>8.2f}s  +{tr['duration']/US:>6.2f}s  \"{text_str}\"")
        elif track["type"] == "effect":
            ves = {ve["id"]: ve for ve in draft["materials"].get("video_effects", [])}
            for j, seg in enumerate(segs):
                tr = seg["target_timerange"]
                ve = ves.get(seg["material_id"])
                name = ve.get("name", "?") if ve else "?"
                print(f"  [{j:>3d}] {tr['start']/US:>8.2f}s  +{tr['duration']/US:>6.2f}s  {name}")
        print()


def retarget_timeline(draft):
    track = get_video_track(draft)
    if not track:
        return
    pos = 0
    for seg in track["segments"]:
        dur = seg["source_timerange"]["duration"]
        speed = seg.get("speed", 1.0)
        actual_dur = int(dur / speed)
        seg["target_timerange"] = {"start": pos, "duration": actual_dur}
        pos += actual_dur
    draft["duration"] = pos


def main():
    parser = argparse.ArgumentParser(description="Edit video clips in a CapCut project")
    parser.add_argument("project", help="Project name")
    parser.add_argument("--info", "-i", action="store_true", help="Show project timeline")
    parser.add_argument("--all", "-a", action="store_true", help="Apply to all clips")
    parser.add_argument("--clips", "-c", nargs="+", type=int, help="Clip indices")
    parser.add_argument("--range", "-r", dest="clip_range", help="Clip range (e.g. 3-19)")
    parser.add_argument("--audio-track", "-A", action="store_true",
                        help="Operate on audio tracks instead of video")
    parser.add_argument("--track-index", "-T", type=int, default=0,
                        help="Which audio track (0-based, default: 0)")
    parser.add_argument("--position", type=float, metavar="SECONDS",
                        help="Move audio segment to this time position")
    parser.add_argument("--fade-in", type=float, help="Fade in duration (seconds)")
    parser.add_argument("--fade-out", type=float, help="Fade out duration (seconds)")
    parser.add_argument("--scale", type=float, help="Scale (1.0=100%%)")
    parser.add_argument("--rotate", type=float, help="Rotation in degrees")
    parser.add_argument("--flip-h", action="store_true", help="Flip horizontal")
    parser.add_argument("--flip-v", action="store_true", help="Flip vertical")
    parser.add_argument("--opacity", type=float, help="Opacity (0.0-1.0)")
    parser.add_argument("--reset", action="store_true", help="Reset clip transforms")
    parser.add_argument("--speed", type=float, help="Playback speed (0.5=half, 2.0=double)")
    parser.add_argument("--volume", type=float, help="Volume (0.0=mute, 1.0=normal)")
    parser.add_argument("--mute", action="store_true", help="Set volume to 0")
    parser.add_argument("--trim", type=float, help="Trim clip to N seconds")
    parser.add_argument("--split", type=float, help="Split clip at N seconds from clip start")
    parser.add_argument("--remove", action="store_true", help="Remove clips")
    parser.add_argument("--move", type=int, help="Move clip FROM this index")
    parser.add_argument("--to", type=int, dest="move_to", help="Move clip TO this index")

    args = parser.parse_args()

    check_capcut_closed()

    draft, draft_path = load_project(args.project)

    if args.info:
        show_info(draft)
        return

    # ── Audio track mode ─────────────────────────────────────────────

    if args.audio_track:
        audio_tracks = [t for t in draft.get("tracks", []) if t.get("type") == "audio"]
        if not audio_tracks:
            print("No audio tracks found.", file=sys.stderr)
            sys.exit(1)
        if args.track_index >= len(audio_tracks):
            print(f"Only {len(audio_tracks)} audio tracks (index 0-{len(audio_tracks)-1}).",
                  file=sys.stderr)
            sys.exit(1)

        track = audio_tracks[args.track_index]
        segments = track["segments"]

        if args.remove:
            if not args.clips:
                parser.error("--remove requires --clips")
            remove_set = set(args.clips)
            track["segments"] = [s for i, s in enumerate(segments) if i not in remove_set]
            save_draft(draft, draft_path)
            print(f"Removed {len(remove_set)} audio segments from track {args.track_index}.")
            return

        if args.position is not None:
            if not args.clips or len(args.clips) != 1:
                parser.error("--position requires exactly one --clips index")
            seg = segments[args.clips[0]]
            seg["target_timerange"]["start"] = int(args.position * US)
            save_draft(draft, draft_path)
            print(f"Moved audio segment {args.clips[0]} to {args.position}s.")
            return

        if args.fade_in is not None or args.fade_out is not None:
            indices = resolve_indices(args, len(segments))
            for i in indices:
                seg = segments[i]
                fade_mat = find_audio_fade(draft, seg)
                if not fade_mat:
                    fade_mat = make_audio_fade()
                    draft["materials"]["audio_fades"].append(fade_mat)
                    seg["extra_material_refs"].append(fade_mat["id"])
                if args.fade_in is not None:
                    fade_mat["fade_in_duration"] = int(args.fade_in * US)
                if args.fade_out is not None:
                    fade_mat["fade_out_duration"] = int(args.fade_out * US)
            save_draft(draft, draft_path)
            print(f"Set fade on {len(indices)} audio segments.")
            return

        indices = resolve_indices(args, len(segments))
        if not indices:
            parser.error("Specify --all, --clips, or --range")

        count = 0
        for i in indices:
            if i < 0 or i >= len(segments):
                continue
            seg = segments[i]

            if args.volume is not None:
                seg["volume"] = args.volume
                seg["last_nonzero_volume"] = args.volume if args.volume > 0 else seg.get("last_nonzero_volume", 1.0)
                count += 1
            if args.mute:
                seg["volume"] = 0.0
                count += 1
            if args.speed is not None:
                seg["speed"] = args.speed
                speed_mat = find_speed_material(draft, seg)
                if speed_mat:
                    speed_mat["speed"] = args.speed
                src_dur = seg["source_timerange"]["duration"]
                seg["target_timerange"]["duration"] = int(src_dur / args.speed)
                count += 1
            if args.trim is not None:
                trim_us = int(args.trim * US)
                if trim_us < seg["source_timerange"]["duration"]:
                    seg["source_timerange"]["duration"] = trim_us
                    seg["target_timerange"]["duration"] = trim_us
                count += 1

        save_draft(draft, draft_path)
        print(f"Modified {count} properties on {len(indices)} audio segments (track {args.track_index}).")
        return

    # ── Video track mode ─────────────────────────────────────────────

    track = get_video_track(draft)
    if not track:
        print("No video track found.", file=sys.stderr)
        sys.exit(1)

    segments = track["segments"]
    needs_retarget = False

    if args.remove:
        if not args.clips:
            parser.error("--remove requires --clips")
        remove_set = set(args.clips)
        track["segments"] = [s for i, s in enumerate(segments) if i not in remove_set]
        needs_retarget = True
        print(f"Removed {len(remove_set)} clips.")

    elif args.split is not None:
        if not args.clips or len(args.clips) != 1:
            parser.error("--split requires exactly one --clips index")
        idx = args.clips[0]
        seg = segments[idx]
        split_us = int(args.split * US)
        src_dur = seg["source_timerange"]["duration"]
        if split_us <= 0 or split_us >= src_dur:
            parser.error(f"Split point must be between 0 and {src_dur/US:.2f}s")
        seg2 = copy.deepcopy(seg)
        seg2["id"] = gen_uuid()
        seg2["source_timerange"] = {
            "start": seg["source_timerange"]["start"] + split_us,
            "duration": src_dur - split_us,
        }
        seg["source_timerange"]["duration"] = split_us
        segments.insert(idx + 1, seg2)
        needs_retarget = True
        print(f"Split clip {idx} at {args.split}s -> now clips {idx} and {idx+1}.")

    elif args.move is not None:
        if args.move_to is None:
            parser.error("--move requires --to")
        frm, to = args.move, args.move_to
        if frm < 0 or frm >= len(segments) or to < 0 or to >= len(segments):
            parser.error(f"Indices out of range (0-{len(segments)-1})")
        seg = segments.pop(frm)
        segments.insert(to, seg)
        needs_retarget = True
        print(f"Moved clip {frm} -> {to}.")

    elif args.trim is not None:
        indices = resolve_indices(args, len(segments))
        for i in indices:
            trim_us = int(args.trim * US)
            seg = segments[i]
            if trim_us < seg["source_timerange"]["duration"]:
                seg["source_timerange"]["duration"] = trim_us
        needs_retarget = True
        print(f"Trimmed {len(indices)} clips to {args.trim}s.")

    else:
        indices = resolve_indices(args, len(segments))
        if not indices:
            parser.error("Specify --all, --clips, or --range")

        count = 0
        for i in indices:
            if i < 0 or i >= len(segments):
                continue
            seg = segments[i]
            clip = seg.get("clip", {})

            if args.scale is not None:
                clip["scale"] = {"x": args.scale, "y": args.scale}
                seg["uniform_scale"] = {"on": True, "value": args.scale}
                count += 1
            if args.rotate is not None:
                clip["rotation"] = args.rotate
                count += 1
            if args.flip_h:
                clip["flip"]["horizontal"] = not clip.get("flip", {}).get("horizontal", False)
                count += 1
            if args.flip_v:
                clip["flip"]["vertical"] = not clip.get("flip", {}).get("vertical", False)
                count += 1
            if args.opacity is not None:
                clip["alpha"] = max(0.0, min(1.0, args.opacity))
                count += 1
            if args.reset:
                clip["scale"] = {"x": 1.0, "y": 1.0}
                clip["rotation"] = 0.0
                clip["transform"] = {"x": 0.0, "y": 0.0}
                clip["flip"] = {"vertical": False, "horizontal": False}
                clip["alpha"] = 1.0
                seg["uniform_scale"] = {"on": True, "value": 1.0}
                count += 1
            if args.speed is not None:
                seg["speed"] = args.speed
                speed_mat = find_speed_material(draft, seg)
                if speed_mat:
                    speed_mat["speed"] = args.speed
                needs_retarget = True
                count += 1
            if args.volume is not None:
                seg["volume"] = args.volume
                seg["last_nonzero_volume"] = args.volume if args.volume > 0 else seg.get("last_nonzero_volume", 1.0)
                count += 1
            if args.mute:
                seg["volume"] = 0.0
                count += 1

        print(f"Modified {count} properties across {len(indices)} clips.")

    if needs_retarget:
        retarget_timeline(draft)

    save_draft(draft, draft_path)
    print(f"Saved '{args.project}'.")


if __name__ == "__main__":
    main()
