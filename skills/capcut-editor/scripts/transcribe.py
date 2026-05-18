#!/usr/bin/env python3
"""Transcribe audio from a CapCut desktop project using Whisper.

Resolves audio file paths from the project (including placeholder paths),
then transcribes each audio segment with word-level timestamps.

Usage:
    # Show audio info
    python3 transcribe.py <project> --info

    # Transcribe all audio (Thai language)
    python3 transcribe.py <project> --language th

    # Plain text output
    python3 transcribe.py <project> --language th --text

    # Export as SRT
    python3 transcribe.py <project> --language th --srt output.srt

    # Only track 2
    python3 transcribe.py <project> --language th --track-index 2

Requires: faster-whisper (pip install faster-whisper)
"""

import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import BASE, US, load_project

AUDIO_RECORD_SUBDIR = "audio_record"


def resolve_audio_path(audio_mat, project_name):
    raw_path = audio_mat.get("path", "")
    if os.path.isfile(raw_path):
        return raw_path
    if "draftpath_placeholder" in raw_path:
        filename = raw_path.split("/")[-1]
        actual = os.path.join(BASE, project_name, AUDIO_RECORD_SUBDIR, filename)
        if os.path.isfile(actual):
            return actual
    if raw_path:
        filename = os.path.basename(raw_path)
        for subdir in [AUDIO_RECORD_SUBDIR, ""]:
            actual = os.path.join(BASE, project_name, subdir, filename)
            if os.path.isfile(actual):
                return actual
    return None


def get_audio_segments(draft, project_name):
    audios = {a["id"]: a for a in draft["materials"].get("audios", [])}
    audio_tracks = [t for t in draft.get("tracks", []) if t.get("type") == "audio"]

    segments = []
    for track_idx, track in enumerate(audio_tracks):
        for seg_idx, seg in enumerate(track.get("segments", [])):
            mat_id = seg.get("material_id", "")
            mat = audios.get(mat_id)
            if not mat:
                continue
            resolved = resolve_audio_path(mat, project_name)
            if not resolved:
                continue
            tr = seg.get("target_timerange", {})
            segments.append({
                "track": track_idx,
                "seg_index": seg_idx,
                "file": resolved,
                "filename": os.path.basename(resolved),
                "start_s": tr.get("start", 0) / US,
                "duration_s": tr.get("duration", 0) / US,
                "volume": seg.get("volume", 1.0),
                "audio_type": mat.get("type", ""),
            })
    return segments


def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def to_srt(words):
    lines = []
    for i, w in enumerate(words, 1):
        lines.append(str(i))
        lines.append(f"{format_timestamp(w['start'])} --> {format_timestamp(w['end'])}")
        lines.append(w["text"].strip())
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio from a CapCut project")
    parser.add_argument("project", help="Project name")
    parser.add_argument("--model", "-m", default="small",
                        help="Whisper model size (tiny, base, small, medium, large)")
    parser.add_argument("--language", "-l", default=None,
                        help="Language code (e.g. th, en)")
    parser.add_argument("--device", default="cpu",
                        help="Device (cpu or auto)")
    parser.add_argument("--track-index", "-t", type=int, default=None,
                        help="Only transcribe this audio track (0-based)")
    parser.add_argument("--srt", metavar="FILE", help="Export as SRT file")
    parser.add_argument("--text", action="store_true", help="Plain text output")
    parser.add_argument("--info", "-i", action="store_true",
                        help="Show audio info without transcribing")

    args = parser.parse_args()

    draft, _ = load_project(args.project)
    segments = get_audio_segments(draft, args.project)

    if not segments:
        print("No audio files found.")
        return

    if args.track_index is not None:
        segments = [s for s in segments if s["track"] == args.track_index]
        if not segments:
            print(f"No audio on track {args.track_index}.", file=sys.stderr)
            sys.exit(1)

    if args.info:
        print(f"Audio segments: {len(segments)}")
        for s in segments:
            print(f"  Track {s['track']} [{s['seg_index']}] "
                  f"{s['start_s']:.1f}s +{s['duration_s']:.1f}s  "
                  f"vol={s['volume']:.2f}  {s['filename']}")
        return

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("ERROR: faster-whisper not installed.", file=sys.stderr)
        print("  Run: pip install faster-whisper", file=sys.stderr)
        sys.exit(1)

    model = WhisperModel(args.model, device=args.device, compute_type="int8")
    all_words = []

    for s in segments:
        print(f"Transcribing: {s['filename']} ({s['duration_s']:.1f}s)...",
              file=sys.stderr)

        segs, info = model.transcribe(s["file"], language=args.language,
                                      word_timestamps=True)
        lang = info.language
        prob = info.language_probability
        print(f"  Detected: {lang} ({prob:.0%})", file=sys.stderr)

        full_text = []
        for seg in segs:
            full_text.append(seg.text)
            for word in seg.words:
                all_words.append({
                    "start": round(word.start + s["start_s"], 3),
                    "end": round(word.end + s["start_s"], 3),
                    "text": word.word.strip(),
                    "track": s["track"],
                    "source": s["filename"],
                })

        if args.text:
            print("".join(full_text).strip())

    if args.text:
        return

    if args.srt:
        with open(args.srt, "w") as f:
            f.write(to_srt(all_words))
        print(f"SRT saved to {args.srt} ({len(all_words)} words)", file=sys.stderr)
        return

    output = {
        "project": args.project,
        "model": args.model,
        "language": info.language if segments else None,
        "segments": all_words,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
