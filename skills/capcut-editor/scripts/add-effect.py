#!/usr/bin/env python3
"""Add video effects to clips in a CapCut desktop project.

Effects are placed on a single `type: "effect"` track with one segment per clip.

Usage:
    # Add Zoom Lens to all clips
    python3 add-effect.py <project> --effect zoom-lens --all

    # Add Sparkle to clips 0, 5, 10
    python3 add-effect.py <project> --effect sparkle --clips 0 5 10

    # Add Blur to clips 3-19 with custom speed/range
    python3 add-effect.py <project> --effect blur --range 3-19 --speed 0.02 --param-range 0.06

    # Use any cached effect by ID
    python3 add-effect.py <project> --effect-id 7399469087174233349 --all

    # List built-in effect shortcuts
    python3 add-effect.py --list-effects

    # Scan all cached effects (404+)
    python3 add-effect.py --scan-cache

    # Remove all effect tracks
    python3 add-effect.py <project> --clear

Requires CapCut to be CLOSED.
"""

import argparse, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import (
    CACHE_BASE, check_capcut_closed, gen_uuid, get_video_track,
    load_project, resolve_indices, save_draft, scan_cached_effects,
)

EFFECTS = {
    "zoom-lens":     {"id": "7399465441057328389", "hash": "60a68556b7df52cc36d20d1f565b4569", "name": "Zoom Lens",     "cat": "Trending",      "cat_id": "27296"},
    "slow-zoom":     {"id": "7399468961949125894", "hash": "56b46f1ebc45c47730d3f7c2569200fc", "name": "Slow Zoom",     "cat": "Video effects",  "cat_id": ""},
    "slight-zoom":   {"id": "7399463624906984709", "hash": "c09004507723569a3e762494d4ffda7d", "name": "Slight Zoom",   "cat": "Video effects",  "cat_id": ""},
    "full-zoom":     {"id": "7399470808759815429", "hash": "24749b428adbacfa9712b8a249912905", "name": "Full Zoom",     "cat": "Video effects",  "cat_id": ""},
    "zoom-far":      {"id": "6724226338418332167", "hash": "8d97f1c1a60d9393c97ff4e9da0669ae", "name": "Zoom Far",      "cat": "Video effects",  "cat_id": ""},
    "blur":          {"id": "7399464929830423813", "hash": "2db7bf49d9349e308ef0f46c39b14abf", "name": "Blur",          "cat": "Video effects",  "cat_id": ""},
    "blur-opening":  {"id": "7399468886309162246", "hash": "5dd4bf7e879fe7356e3e27e5105f5af1", "name": "Blur Opening",  "cat": "Video effects",  "cat_id": ""},
    "soft-light":    {"id": "7399467970071743749", "hash": "258b5bd7ba1fb94dce800bc496a30ed9", "name": "Soft Light",    "cat": "Video effects",  "cat_id": ""},
    "bokeh":         {"id": "7399470883863088389", "hash": "1c8442102d00628a4958e488251a75e7", "name": "Bokeh",         "cat": "Video effects",  "cat_id": ""},
    "dark-corner":   {"id": "7399463239379209477", "hash": "ef7abad9671e2f3da7993b7673ece5fc", "name": "Dark Corner",   "cat": "Video effects",  "cat_id": ""},
    "sparkle":       {"id": "7399469087174233349", "hash": "816803366dd866837e21380513b81e33", "name": "Sparkle",       "cat": "Video effects",  "cat_id": ""},
    "sparkle-2":     {"id": "7399466130177330438", "hash": "715227fc796386820c16198a57fd5249", "name": "Sparkle 2",     "cat": "Video effects",  "cat_id": ""},
    "flash":         {"id": "7399472112223669510", "hash": "d7c42c303074967c0cad7c7a6adfe896", "name": "Flashing Light","cat": "Video effects",  "cat_id": ""},
    "color-shift":   {"id": "7399470160203107589", "hash": "53c8584c8174f887b2802540dd28955b", "name": "Color Shift",   "cat": "Video effects",  "cat_id": ""},
    "fog":           {"id": "7399471802361105669", "hash": "bdda3043cfa04aa56d2806ada93367ae", "name": "Fog",           "cat": "Video effects",  "cat_id": ""},
    "oil-paint":     {"id": "11353735",            "hash": "118b5e6a07a603581825a0fa8bb08e35", "name": "Oil Paint",     "cat": "Video effects",  "cat_id": ""},
    "rainbow":       {"id": "7399470727121947910", "hash": "ae2e32daa7af0fa8f4b61a0c5aacd196", "name": "Rainbow Bubble","cat": "Video effects",  "cat_id": ""},
    "petals":        {"id": "7399464130664500486", "hash": "a772c059e7fb8304292e7ebb870e8eb3", "name": "Petals Falling","cat": "Video effects",  "cat_id": ""},
    "curtain":       {"id": "7399468499044683013", "hash": "05c17ac3298c0521cd91a720850a27de", "name": "Curtain Close", "cat": "Video effects",  "cat_id": ""},
    "star-shift":    {"id": "7399470054053547270", "hash": "f1c6583c2a7227b6ccf002863fdfdf65", "name": "Star Shift",    "cat": "Video effects",  "cat_id": ""},
}


def make_video_effect(effect_id, effect_hash, name, cat="", cat_id="",
                      cache_path=None, adjust_params=None):
    mat_id = gen_uuid()
    path = cache_path or os.path.join(CACHE_BASE, effect_id, effect_hash)
    return {
        "id": mat_id,
        "effect_id": effect_id,
        "resource_id": effect_id,
        "name": name,
        "type": "video_effect",
        "path": path,
        "adjust_params": adjust_params or [],
        "category_id": cat_id,
        "category_name": cat,
        "apply_target_type": 2,
        "platform": "all",
        "source_platform": 1,
        "effect_type": 0,
        "is_ai_generate_effect": False,
        "is_third_party": False,
        "meta": "",
        "request_id": "",
        "resource_name": "",
        "sub_effects": [],
        "track_id": "",
    }


def make_effect_segment(mat_id, start, duration):
    return {
        "id": gen_uuid(),
        "material_id": mat_id,
        "target_timerange": {"start": start, "duration": duration},
        "source_timerange": None,
        "render_timerange": None,
        "clip": None,
        "speed": 1.0,
        "volume": 1.0,
        "visible": True,
        "extra_material_refs": [],
        "render_index": 11001,
        "keyframe_refs": {},
        "common_keyframes": {},
        "group_id": "",
        "track_render_index": 2,
        "is_placeholder": False,
    }


def list_effects():
    print(f"{'Name':20s}  {'Key':20s}  effect_id            cached")
    print("-" * 78)
    for key, info in sorted(EFFECTS.items()):
        cache_path = os.path.join(CACHE_BASE, info["id"], info["hash"])
        exists = "ok" if os.path.isdir(cache_path) else "--"
        print(f'{info["name"]:20s}  {key:20s}  {info["id"]:20s}  {exists}')


def list_cached():
    effects = scan_cached_effects()
    known_ids = {e["id"] for e in EFFECTS.values()}

    print(f"Cached video effects: {len(effects)}")
    print()
    print(f"{'effect_id':25s}  {'Adj':3s}  {'Known':5s}  Name")
    print("-" * 80)

    for eff in sorted(effects, key=lambda x: x["name"]):
        known = "yes" if eff["id"] in known_ids else ""
        adj = "+" if eff["has_params"] else " "
        name = eff["name"][:40]
        print(f'  {eff["id"]:25s}  {adj:3s}  {known:5s}  {name}')

    print(f"\nUse --effect-id <id> to apply any cached effect.")


def main():
    parser = argparse.ArgumentParser(
        description="Add video effects to a CapCut project")
    parser.add_argument("project", nargs="?", help="Project name")
    parser.add_argument("--effect", "-e", help="Effect key (use --list-effects)")
    parser.add_argument("--effect-id", help="Raw effect_id from cache (overrides --effect)")
    parser.add_argument("--all", "-a", action="store_true", help="Apply to all video clips")
    parser.add_argument("--clips", "-c", nargs="+", type=int, help="Clip indices (0-based)")
    parser.add_argument("--range", "-r", dest="clip_range", help="Clip range (e.g. 3-19)")
    parser.add_argument("--speed", type=float, help="Speed param (0.01-0.03)")
    parser.add_argument("--param-range", type=float, dest="param_range",
                        help="Range param (0.03-0.08)")
    parser.add_argument("--clear", action="store_true", help="Remove all effect tracks")
    parser.add_argument("--list-effects", action="store_true", help="List built-in effects")
    parser.add_argument("--scan-cache", action="store_true", help="Scan all cached effects")

    args = parser.parse_args()

    if args.list_effects:
        list_effects()
        return
    if args.scan_cache:
        list_cached()
        return

    if not args.project:
        parser.error("project name is required (unless using --list-effects or --scan-cache)")

    check_capcut_closed()

    draft, draft_path = load_project(args.project)

    if args.clear:
        before = len(draft["tracks"])
        draft["tracks"] = [t for t in draft["tracks"] if t.get("type") != "effect"]
        draft["materials"]["video_effects"] = []
        save_draft(draft, draft_path)
        print(f"Cleared {before - len(draft['tracks'])} effect tracks.")
        return

    if not args.effect and not args.effect_id:
        parser.error("Specify --effect or --effect-id")

    # Resolve effect info
    if args.effect_id:
        effect_id = args.effect_id
        cache_dir = os.path.join(CACHE_BASE, effect_id)
        if not os.path.isdir(cache_dir):
            print(f"ERROR: effect_id {effect_id} not cached.", file=sys.stderr)
            sys.exit(1)
        hashes = [h for h in os.listdir(cache_dir)
                  if os.path.isdir(os.path.join(cache_dir, h))]
        if not hashes:
            print(f"ERROR: No cache hash found for {effect_id}", file=sys.stderr)
            sys.exit(1)
        effect_hash = hashes[0]
        name = effect_id
        cat = ""
        cat_id = ""
        cache_path = os.path.join(cache_dir, effect_hash)
    else:
        if args.effect not in EFFECTS:
            print(f"Unknown effect: {args.effect}", file=sys.stderr)
            print("Use --list-effects to see options.", file=sys.stderr)
            sys.exit(1)
        info = EFFECTS[args.effect]
        effect_id = info["id"]
        effect_hash = info["hash"]
        name = info["name"]
        cat = info["cat"]
        cat_id = info["cat_id"]
        cache_path = os.path.join(CACHE_BASE, effect_id, effect_hash)

    if not os.path.isdir(cache_path):
        print(f"WARNING: Effect cache not found at {cache_path}", file=sys.stderr)
        print("Apply this effect once in CapCut to cache it.", file=sys.stderr)

    # Resolve clip indices
    track = get_video_track(draft)
    if not track:
        print("No video track found.", file=sys.stderr)
        sys.exit(1)

    segments = track["segments"]
    indices = resolve_indices(args, len(segments))
    if not indices:
        parser.error("Specify --all, --clips, or --range")

    # Build adjust_params
    adjust_params = None
    if args.speed or args.param_range:
        adjust_params = []
        if args.speed:
            adjust_params.append({"name": "effects_adjust_speed",
                                  "value": args.speed, "default_value": 0.33})
        if args.param_range:
            adjust_params.append({"name": "effects_adjust_range",
                                  "value": args.param_range, "default_value": 0.3})

    # Create effect materials and segments
    new_materials = []
    new_segments = []

    for i in indices:
        if i < 0 or i >= len(segments):
            print(f"WARNING: Clip index {i} out of range (0-{len(segments)-1}), skipping.")
            continue

        seg = segments[i]
        tr = seg.get("target_timerange", {})
        start = tr.get("start", 0)
        dur = tr.get("duration", 0)
        if dur <= 0:
            continue

        mat = make_video_effect(effect_id, effect_hash, name, cat, cat_id,
                                cache_path, adjust_params)
        new_materials.append(mat)
        new_segments.append(make_effect_segment(mat["id"], start, dur))

    if not new_segments:
        print("No clips matched.", file=sys.stderr)
        sys.exit(1)

    # Add to existing effect track or create one
    effect_tracks = [t for t in draft["tracks"] if t.get("type") == "effect"]
    if effect_tracks:
        effect_tracks[0]["segments"].extend(new_segments)
    else:
        draft["tracks"].append({
            "id": gen_uuid(),
            "type": "effect",
            "flag": 0,
            "attribute": 0,
            "name": "",
            "is_default_name": True,
            "segments": new_segments,
        })

    draft["materials"]["video_effects"].extend(new_materials)
    save_draft(draft, draft_path)
    print(f"Added {name} to {len(new_segments)} clips in '{args.project}'.")
    print(f"  Clips: {indices}")
    if adjust_params:
        print(f"  Params: {[(p['name'], p['value']) for p in adjust_params]}")


if __name__ == "__main__":
    main()
