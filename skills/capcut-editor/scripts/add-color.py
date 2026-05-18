#!/usr/bin/env python3
"""Add color grading (HSL) to clips in a CapCut desktop project.

Usage:
    # Show current color settings
    python3 add-color.py <project> --info

    # Add HSL adjustment to specific clips
    python3 add-color.py <project> --hsl --hue 10 --saturation 20 --lightness -5 --clips 0 1 2

    # Boost saturation on all clips
    python3 add-color.py <project> --hsl --saturation 30 --all

    # Preset: warm, cool, vivid, moody, vintage, fade
    python3 add-color.py <project> --preset vivid --all

    # Remove all HSL adjustments
    python3 add-color.py <project> --clear

Requires CapCut to be CLOSED.
"""

import argparse, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import (
    CACHE_BASE, US, check_capcut_closed, gen_uuid, get_video_track,
    load_project, resolve_indices, save_draft,
)

HSL_CACHE_ID = "7501974767453474064"
HSL_CACHE_HASH = "26e574bcfa176c3c1a1f7fd5df0a4996"
HSL_CACHE_PATH = os.path.join(CACHE_BASE, HSL_CACHE_ID, HSL_CACHE_HASH)

PRESETS = {
    "warm":    (5,   15,  5),
    "cool":    (-10, 0,   0),
    "vivid":   (0,   35,  5),
    "moody":   (-5,  -15, -20),
    "vintage": (15,  -10, -5),
    "fade":    (0,   -30, 15),
}


def make_hsl_material(hue=0, saturation=0, lightness=0):
    return {
        "id": gen_uuid(),
        "constant_material_id": gen_uuid(),
        "hsl_color_type": 1,
        "hue": hue,
        "saturation": saturation,
        "lightness": lightness,
        "interacting": True,
        "version": "1",
        "path": HSL_CACHE_PATH,
        "type": "hsl",
        "lumi_hub_path": os.path.join(HSL_CACHE_PATH, "lumi_hub_path"),
        "custom_color": "#FFE64444",
        "resource_id": "",
        "source_platform": 0,
    }


def show_color_info(draft):
    track = get_video_track(draft)
    if not track:
        print("No video track found.")
        return

    hsl_map = {h["id"]: h for h in draft["materials"].get("hsl", [])}
    print(f"{'Clip':>5s}  {'Hue':>6s}  {'Sat':>6s}  {'Light':>6s}  {'HSL':>4s}")
    print("-" * 40)

    for i, seg in enumerate(track["segments"]):
        hsl_entry = None
        for ref in seg.get("extra_material_refs", []):
            if ref in hsl_map:
                hsl_entry = hsl_map[ref]
                break

        enable = seg.get("enable_hsl", False)
        if hsl_entry:
            print(f"  {i:>3d}  {hsl_entry['hue']:>6d}  {hsl_entry['saturation']:>6d}  "
                  f"{hsl_entry['lightness']:>6d}  {'on' if enable else 'off':>4s}")
        else:
            print(f"  {i:>3d}  {'--':>6s}  {'--':>6s}  {'--':>6s}  {'on' if enable else 'off':>4s}")


def main():
    parser = argparse.ArgumentParser(description="Add HSL color grading to a CapCut project")
    parser.add_argument("project", help="Project name")
    parser.add_argument("--info", "-i", action="store_true", help="Show current HSL settings")
    parser.add_argument("--all", "-a", action="store_true", help="Apply to all clips")
    parser.add_argument("--clips", "-c", nargs="+", type=int, help="Clip indices")
    parser.add_argument("--range", "-r", dest="clip_range", help="Clip range (e.g. 3-19)")
    parser.add_argument("--hsl", action="store_true", help="Apply HSL adjustment")
    parser.add_argument("--hue", type=int, default=0, help="Hue shift (-180 to 180)")
    parser.add_argument("--saturation", "--sat", type=int, default=0, help="Saturation (-100 to 100)")
    parser.add_argument("--lightness", "--light", type=int, default=0, help="Lightness (-100 to 100)")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), help="Color preset")
    parser.add_argument("--clear", action="store_true", help="Remove all HSL adjustments")

    args = parser.parse_args()

    check_capcut_closed()

    draft, draft_path = load_project(args.project)

    if args.info:
        show_color_info(draft)
        return

    if args.clear:
        hsl_ids = {h["id"] for h in draft["materials"].get("hsl", [])}
        for track in draft.get("tracks", []):
            for seg in track.get("segments", []):
                seg["extra_material_refs"] = [
                    r for r in seg.get("extra_material_refs", [])
                    if r not in hsl_ids
                ]
                seg["enable_hsl"] = False
        draft["materials"]["hsl"] = []
        save_draft(draft, draft_path)
        print("Cleared all HSL adjustments.")
        return

    if not args.hsl and not args.preset:
        parser.error("Specify --hsl with values or --preset")

    track = get_video_track(draft)
    if not track:
        print("No video track found.", file=sys.stderr)
        sys.exit(1)

    segments = track["segments"]
    indices = resolve_indices(args, len(segments))
    if not indices:
        parser.error("Specify --all, --clips, or --range")
        return

    hue, sat, light = args.hue, args.saturation, args.lightness
    if args.preset:
        hue, sat, light = PRESETS[args.preset]

    if not os.path.isdir(HSL_CACHE_PATH):
        print(f"WARNING: HSL cache not found at {HSL_CACHE_PATH}", file=sys.stderr)
        print("Use color adjustment once in CapCut first.", file=sys.stderr)

    hsl_map = {h["id"]: h for h in draft["materials"]["hsl"]}
    count = 0
    for i in indices:
        if i < 0 or i >= len(segments):
            continue

        seg = segments[i]
        existing_hsl = None
        for ref in seg.get("extra_material_refs", []):
            if ref in hsl_map:
                existing_hsl = hsl_map[ref]
                break

        if existing_hsl:
            existing_hsl["hue"] = hue
            existing_hsl["saturation"] = sat
            existing_hsl["lightness"] = light
        else:
            hsl_mat = make_hsl_material(hue, sat, light)
            draft["materials"]["hsl"].append(hsl_mat)
            seg["extra_material_refs"].append(hsl_mat["id"])

        seg["enable_hsl"] = True
        count += 1

    save_draft(draft, draft_path)
    preset_str = f" (preset: {args.preset})" if args.preset else ""
    print(f"Applied HSL to {count} clips in '{args.project}'{preset_str}.")
    print(f"  Hue: {hue:+d}  Saturation: {sat:+d}  Lightness: {light:+d}")


if __name__ == "__main__":
    main()
