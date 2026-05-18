#!/usr/bin/env python3
"""Add text overlays to a CapCut desktop project.

Usage:
    # Add a single text overlay at 0-5s
    python3 add-text.py <project> --text "Hello World" --start 0 --duration 5

    # Add text at lower third with custom font size
    python3 add-text.py <project> --text "Subtitle" --start 10 --duration 3 --y 0.7 --size 12

    # Use a specific font
    python3 add-text.py <project> --text "Sawasdee" --font sarabun-bold
    python3 add-text.py <project> --text "Hello" --font /full/path/to/font.ttf

    # List available fonts
    python3 add-text.py --list-fonts

    # Add from a JSON file with multiple entries
    python3 add-text.py <project> --from-file texts.json

    # Clear all text tracks
    python3 add-text.py <project> --clear

Requires CapCut to be CLOSED.
"""

import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import US, check_capcut_closed, gen_uuid, load_project, save_draft

FONT_ALIASES = {
    "default":       "/Applications/CapCut.app/Contents/Resources/Font/SystemFont/en.ttf",
    "en":            "/Applications/CapCut.app/Contents/Resources/Font/SystemFont/en.ttf",
    "th":            "/Applications/CapCut.app/Contents/Resources/Font/SystemFont/th.ttf",
    "thai":          "/Applications/CapCut.app/Contents/Resources/Font/SystemFont/th.ttf",
    "noto":          "/Applications/CapCut.app/Contents/Resources/Font/SystemFont/NotoSans-Regular.ttf",
    "noto-thai":     "/Applications/CapCut.app/Contents/Resources/Font/SystemFont/NotoSansThai-Regular.ttf",
    "capcut":        "/Applications/CapCut.app/Contents/Resources/Font/SystemFont/CapCutSansText-Regular.otf",
    "capcut-bold":   "/Applications/CapCut.app/Contents/Resources/Font/SystemFont/CapCutSansText-Bold.otf",
    "capcut-medium": "/Applications/CapCut.app/Contents/Resources/Font/SystemFont/CapCutSansText-Medium.otf",
    "sarabun":       os.path.expanduser("~/Library/Fonts/Sarabun-Regular.ttf"),
    "sarabun-bold":  os.path.expanduser("~/Library/Fonts/Sarabun-Bold.ttf"),
    "sarabun-light": os.path.expanduser("~/Library/Fonts/Sarabun-Light.ttf"),
    "sarabun-med":   os.path.expanduser("~/Library/Fonts/Sarabun-Medium.ttf"),
    "sarabun-thin":  os.path.expanduser("~/Library/Fonts/Sarabun-Thin.ttf"),
    "thsarabun":     os.path.expanduser("~/Library/Fonts/THSarabun.ttf"),
    "thsarabun-new": os.path.expanduser("~/Library/Fonts/THSarabunNew.ttf"),
    "db-helv-med":   os.path.expanduser("~/Library/Fonts/DB Helvethaica X Med v3.2.ttf"),
    "db-helv-bold":  os.path.expanduser("~/Library/Fonts/DB Helvethaica X Bd v3.2.ttf"),
}


def resolve_font(font_arg):
    if not font_arg:
        return FONT_ALIASES["default"]
    if font_arg in FONT_ALIASES:
        return FONT_ALIASES[font_arg]
    if os.path.isfile(font_arg):
        return font_arg
    raise ValueError(f"Font not found: {font_arg} (use --list-fonts to see options)")


def list_fonts():
    print(f"{'Alias':18s}  {'Exists':6s}  Path")
    print("-" * 90)
    for alias, path in sorted(FONT_ALIASES.items()):
        exists = "ok" if os.path.isfile(path) else "--"
        print(f"  {alias:16s}  {exists:6s}  {path}")


def make_text_content(text, font_size=15, font_path=None):
    return json.dumps({
        "text": text,
        "styles": [{
            "fill": {
                "content": {
                    "solid": {"color": [1.0, 1.0, 1.0]},
                    "render_type": "solid"
                }
            },
            "range": [0, len(text)],
            "strokes": [{
                "width": 0.06,
                "content": {
                    "solid": {"color": [0, 0, 0]},
                    "render_type": "solid"
                }
            }],
            "size": font_size,
            "font": {"path": font_path, "id": ""}
        }]
    })


def make_text_material(text, font_size=15.0, font_path=None):
    return {
        "id": gen_uuid(),
        "type": "text",
        "content": make_text_content(text, font_size, font_path),
        "text_color": "#FFFFFF",
        "font_size": font_size,
        "font_path": font_path,
        "alignment": 1,
        "global_alpha": 1.0,
        "line_spacing": 0.02,
        "border_width": 0.08,
        "border_color": "#000000",
        "text_size": int(font_size * 2),
        "fixed_width": 427.5,
        "line_max_width": 0.82,
    }


def make_text_segment(material_id, start_us, duration_us, y_pos=0.0, x_pos=0.0):
    return {
        "id": gen_uuid(),
        "material_id": material_id,
        "target_timerange": {"start": start_us, "duration": duration_us},
        "source_timerange": None,
        "render_timerange": None,
        "clip": {
            "scale": {"x": 1.0, "y": 1.0},
            "rotation": 0.0,
            "transform": {"x": x_pos, "y": y_pos},
            "flip": {"vertical": False, "horizontal": False},
            "alpha": 1.0,
        },
        "speed": 1.0,
        "volume": 1.0,
        "visible": True,
        "extra_material_refs": [],
        "render_index": 0,
        "keyframe_refs": {},
        "common_keyframes": {},
        "group_id": "",
        "track_render_index": 0,
        "is_placeholder": False,
    }


def main():
    parser = argparse.ArgumentParser(description="Add text overlays to a CapCut project")
    parser.add_argument("project", nargs="?", help="Project name")
    parser.add_argument("--text", "-t", help="Text content")
    parser.add_argument("--start", type=float, default=0, help="Start time in seconds")
    parser.add_argument("--duration", "-d", type=float, default=3, help="Duration in seconds")
    parser.add_argument("--y", type=float, default=0.0, help="Vertical position (-1 to 1)")
    parser.add_argument("--x", type=float, default=0.0, help="Horizontal position (-1 to 1)")
    parser.add_argument("--size", "-s", type=float, default=15.0, help="Font size")
    parser.add_argument("--font", help="Font alias or full path (use --list-fonts)")
    parser.add_argument("--list-fonts", action="store_true", help="List available fonts")
    parser.add_argument("--from-file", "-f", dest="from_file", help="JSON file with entries")
    parser.add_argument("--clear", action="store_true", help="Remove all text tracks")

    args = parser.parse_args()

    if args.list_fonts:
        list_fonts()
        return

    if not args.project:
        parser.error("project name is required (unless using --list-fonts)")

    check_capcut_closed()

    draft, draft_path = load_project(args.project)

    if args.clear:
        before = len(draft["tracks"])
        draft["tracks"] = [t for t in draft["tracks"] if t.get("type") != "text"]
        draft["materials"]["texts"] = []
        save_draft(draft, draft_path)
        print(f"Cleared {before - len(draft['tracks'])} text tracks.")
        return

    entries = []
    if args.from_file:
        with open(args.from_file) as f:
            entries = json.load(f)
    elif args.text:
        entries = [{"text": args.text, "start": args.start,
                    "duration": args.duration, "y": args.y,
                    "x": args.x, "size": args.size, "font": args.font}]
    else:
        parser.error("Specify --text or --from-file")
        return

    new_materials = []
    new_segments = []

    for entry in entries:
        font_arg = entry.get("font") or args.font
        try:
            font_path = resolve_font(font_arg) if font_arg else FONT_ALIASES["default"]
        except ValueError as e:
            print(f"WARNING: {e}", file=sys.stderr)
            font_path = FONT_ALIASES["default"]

        mat = make_text_material(entry["text"], entry.get("size", 15.0), font_path)
        new_materials.append(mat)
        new_segments.append(make_text_segment(
            mat["id"],
            int(entry.get("start", 0) * US),
            int(entry.get("duration", 3) * US),
            y_pos=entry.get("y", 0.0),
            x_pos=entry.get("x", 0.0),
        ))

    text_tracks = [t for t in draft["tracks"] if t.get("type") == "text"]
    if text_tracks:
        text_tracks[0]["segments"].extend(new_segments)
    else:
        draft["tracks"].append({
            "id": gen_uuid(),
            "type": "text",
            "flag": 0,
            "attribute": 0,
            "name": "",
            "is_default_name": True,
            "segments": new_segments,
        })

    draft["materials"]["texts"].extend(new_materials)
    save_draft(draft, draft_path)

    print(f"Added {len(new_materials)} text overlay(s) to '{args.project}'.")
    for entry in entries:
        print(f"  \"{entry['text']}\" at {entry.get('start', 0)}s for {entry.get('duration', 3)}s")


if __name__ == "__main__":
    main()
