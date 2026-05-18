#!/usr/bin/env python3
"""Add transitions between clips in a CapCut desktop project.

Transitions are stored in materials.transitions and referenced in the outgoing
segment's extra_material_refs. The transition overlaps the boundary between clips.

Usage:
    python3 add-transition.py --list
    python3 add-transition.py <project> --between 19 20
    python3 add-transition.py <project> --all-gaps
    python3 add-transition.py <project> --gaps 2 5 10
    python3 add-transition.py <project> --between 19 20 --duration 0.5
    python3 add-transition.py <project> --between 19 20 --effect-id 7486288371376049413
    python3 add-transition.py <project> --clear

Requires CapCut to be CLOSED.
"""

import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import (
    BASE, CACHE_BASE, US, check_capcut_closed, gen_uuid, get_video_track,
    load_project, save_draft,
)

TRANSITIONS = {
    "suction": {
        "effect_id": "7486288371376049413",
        "hash": "141b391d38432d6c741b485f22804e95",
        "name": "Suction",
        "category_id": "32431",
        "category_name": "Pro",
    },
}


def make_transition_material(effect_id, name, path, category_id, category_name, duration_us):
    return {
        "id": gen_uuid(),
        "type": "transition",
        "name": name,
        "effect_id": effect_id,
        "resource_id": effect_id,
        "third_resource_id": "0",
        "source_platform": 1,
        "path": path,
        "duration": duration_us,
        "is_overlap": True,
        "platform": "all",
        "category_id": category_id,
        "category_name": category_name,
        "request_id": "",
        "is_ai_transition": False,
        "video_path": "",
        "task_id": "",
    }


def list_transitions():
    print(f"{'Name':20s}  {'Key':15s}  effect_id             cached")
    print("-" * 70)
    for key, info in sorted(TRANSITIONS.items()):
        cache = os.path.join(CACHE_BASE, info["effect_id"], info["hash"])
        exists = "ok" if os.path.isdir(cache) else "--"
        print(f'{info["name"]:20s}  {key:15s}  {info["effect_id"]}  {exists}')


def scan_cached_transitions():
    known_names = {}
    for proj in os.listdir(BASE):
        path = os.path.join(BASE, proj, "draft_info.json")
        try:
            with open(path) as f:
                d = json.load(f)
            for t in d["materials"].get("transitions", []):
                eid = t["effect_id"]
                if eid not in known_names:
                    known_names[eid] = {
                        "name": t.get("name", ""),
                        "cat": t.get("category_name", ""),
                    }
        except Exception:
            pass

    seen = set()
    results = []
    for eid in os.listdir(CACHE_BASE):
        epath = os.path.join(CACHE_BASE, eid)
        if not os.path.isdir(epath):
            continue
        for h in os.listdir(epath):
            hpath = os.path.join(epath, h)
            extra_path = os.path.join(hpath, "extra.json")
            config_path = os.path.join(hpath, "config.json")
            if not os.path.exists(extra_path):
                continue
            try:
                with open(extra_path) as f:
                    extra = json.load(f)
                if "transition" not in extra:
                    continue
                key = (eid, h)
                if key in seen:
                    continue
                seen.add(key)
                name = known_names.get(eid, {}).get("name", "")
                if not name:
                    try:
                        with open(config_path) as f:
                            cfg = json.load(f)
                        name = cfg.get("name", eid)
                    except Exception:
                        name = eid
                overlap = extra["transition"].get("isOverlap", False)
                def_dur = extra["transition"].get("defaultDura", 1)
                results.append({
                    "id": eid, "hash": h, "name": name,
                    "overlap": overlap, "default_duration": def_dur,
                    "known": eid in {i["effect_id"] for i in TRANSITIONS.values()},
                })
            except Exception:
                pass

    overlap_only = [r for r in results if r["overlap"]]
    print(f"Cached transitions: {len(results)} total, {len(overlap_only)} with overlap")
    print()
    print(f"{'effect_id':25s}  {'Overlap':7s}  {'DefDur':6s}  {'Known':5s}  Name")
    print("-" * 80)
    for t in sorted(results, key=lambda x: x["name"]):
        known = "yes" if t["known"] else ""
        overlap = "yes" if t["overlap"] else "no"
        print(f'  {t["id"]:25s}  {overlap:7s}  {t["default_duration"]:>5.1f}s  {known:5s}  {t["name"][:40]}')
    print(f"\nUse --effect-id <id> to apply any cached transition.")


def main():
    parser = argparse.ArgumentParser(description="Add transitions between clips in a CapCut project")
    parser.add_argument("project", nargs="?", help="Project name")
    parser.add_argument("--list", action="store_true", help="List built-in transitions")
    parser.add_argument("--scan-cache", action="store_true", help="Scan all cached transitions")
    parser.add_argument("--between", nargs=2, type=int, metavar=("A", "B"),
                        help="Add transition between clip A and clip B")
    parser.add_argument("--all-gaps", action="store_true",
                        help="Add transition between all consecutive clips")
    parser.add_argument("--gaps", nargs="+", type=int,
                        help="Add transitions at gaps after clip N")
    parser.add_argument("--duration", type=float, default=1.0,
                        help="Transition duration in seconds (default: 1.0)")
    parser.add_argument("--effect", "-e", default="suction",
                        help="Transition key (default: suction)")
    parser.add_argument("--effect-id", help="Raw effect_id (overrides --effect)")
    parser.add_argument("--clear", action="store_true", help="Remove all transitions")

    args = parser.parse_args()

    if args.list:
        list_transitions()
        return
    if args.scan_cache:
        scan_cached_transitions()
        return

    if not args.project:
        parser.error("project name is required (unless using --list or --scan-cache)")

    check_capcut_closed()

    draft, draft_path = load_project(args.project)

    if args.clear:
        trans_ids = {t["id"] for t in draft["materials"].get("transitions", [])}
        for track in draft.get("tracks", []):
            for seg in track.get("segments", []):
                seg["extra_material_refs"] = [
                    r for r in seg.get("extra_material_refs", [])
                    if r not in trans_ids
                ]
        draft["materials"]["transitions"] = []
        save_draft(draft, draft_path)
        print("Cleared all transitions.")
        return

    track = get_video_track(draft)
    if not track:
        print("No video track found.", file=sys.stderr)
        sys.exit(1)

    segments = track["segments"]
    if len(segments) < 2:
        print("Need at least 2 clips for transitions.", file=sys.stderr)
        sys.exit(1)

    if args.between:
        a, b = args.between
        if b != a + 1:
            print("WARNING: clips should be adjacent (B = A + 1).", file=sys.stderr)
        gap_indices = [a]
    elif args.all_gaps:
        gap_indices = list(range(len(segments) - 1))
    elif args.gaps:
        gap_indices = args.gaps
    else:
        parser.error("Specify --between, --all-gaps, or --gaps")
        return

    # Resolve effect info
    if args.effect_id:
        effect_id = args.effect_id
        name = effect_id
        category_id = ""
        category_name = ""
        hash_val = None
        for proj in os.listdir(BASE):
            try:
                with open(os.path.join(BASE, proj, "draft_info.json")) as f:
                    d = json.load(f)
                for t in d["materials"].get("transitions", []):
                    if t["effect_id"] == effect_id:
                        name = t["name"]
                        category_id = t.get("category_id", "")
                        category_name = t.get("category_name", "")
                        hash_val = t["path"].split("/")[-1]
                        break
            except Exception:
                pass
        if not hash_val:
            cache_dir = os.path.join(CACHE_BASE, effect_id)
            if os.path.isdir(cache_dir):
                hashes = [h for h in os.listdir(cache_dir)
                          if os.path.isdir(os.path.join(cache_dir, h))]
                if hashes:
                    hash_val = hashes[0]
        if not hash_val:
            print(f"ERROR: effect_id {effect_id} not found.", file=sys.stderr)
            sys.exit(1)
        path = os.path.join(CACHE_BASE, effect_id, hash_val)
    else:
        if args.effect not in TRANSITIONS:
            print(f"Unknown transition: {args.effect}. Use --list.", file=sys.stderr)
            sys.exit(1)
        info = TRANSITIONS[args.effect]
        effect_id = info["effect_id"]
        name = info["name"]
        category_id = info["category_id"]
        category_name = info["category_name"]
        path = os.path.join(CACHE_BASE, effect_id, info["hash"])

    if not os.path.isdir(path):
        print(f"ERROR: Transition cache not found at {path}", file=sys.stderr)
        print("Apply this transition once in CapCut to cache it.", file=sys.stderr)
        sys.exit(1)

    duration_us = int(args.duration * US)
    count = 0

    for gap_idx in gap_indices:
        if gap_idx < 0 or gap_idx >= len(segments) - 1:
            print(f"WARNING: Gap index {gap_idx} out of range, skipping.")
            continue

        trans_mat = make_transition_material(
            effect_id, name, path, category_id, category_name, duration_us)
        draft["materials"]["transitions"].append(trans_mat)

        seg = segments[gap_idx]
        if trans_mat["id"] not in seg.get("extra_material_refs", []):
            seg["extra_material_refs"].append(trans_mat["id"])

        count += 1

    save_draft(draft, draft_path)
    print(f"Added {name} transition to {count} gap(s) in '{args.project}'.")
    print(f"  Duration: {args.duration}s per transition")


if __name__ == "__main__":
    main()
