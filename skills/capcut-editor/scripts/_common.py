"""Shared utilities for CapCut desktop project scripts."""

import json, os, subprocess, sys, uuid

BASE = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
CACHE_BASE = "/Users/admin/Library/Containers/com.lemon.lvoverseas/Data/Movies/CapCut/User Data/Cache/effect"
US = 1_000_000


def gen_uuid():
    return str(uuid.uuid4()).upper()


def load_project(name):
    path = os.path.join(BASE, name, "draft_info.json")
    with open(path) as f:
        return json.load(f), path


def save_draft(draft, draft_path):
    project_dir = os.path.dirname(draft_path)
    compact = json.dumps(draft, separators=(",", ":"))

    for p in [draft_path, draft_path + ".bak"]:
        with open(p, "w") as f:
            f.write(compact)

    tl_proj_path = os.path.join(project_dir, "Timelines", "project.json")
    with open(tl_proj_path) as f:
        tl_proj = json.load(f)
    tl_id = tl_proj["main_timeline_id"]
    tl_draft = os.path.join(project_dir, "Timelines", tl_id, "draft_info.json")
    for p in [tl_draft, tl_draft + ".bak"]:
        with open(p, "w") as f:
            f.write(compact)

    for tmpl in [
        os.path.join(project_dir, "template-2.tmp"),
        os.path.join(project_dir, "Timelines", tl_id, "template-2.tmp"),
    ]:
        if os.path.exists(tmpl):
            with open(tmpl, "w") as f:
                f.write(compact)


def check_capcut_closed():
    r = subprocess.run(["pgrep", "-fl", "CapCut|lvoverseas|lemon"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        print("ERROR: CapCut is running. Close it first.", file=sys.stderr)
        sys.exit(1)


def get_video_track(draft):
    for track in draft.get("tracks", []):
        if track.get("type") == "video":
            return track
    return None


def parse_range(range_str):
    parts = range_str.split("-")
    if len(parts) == 2:
        return list(range(int(parts[0]), int(parts[1]) + 1))
    return [int(parts[0])]


def resolve_indices(args, total):
    if args.all:
        return list(range(total))
    elif getattr(args, "clip_range", None):
        return parse_range(args.clip_range)
    elif args.clips:
        return args.clips
    return []


def scan_cached_effects():
    """Scan CapCut effect cache for video effects (AmazingFeature type).

    Returns list of dicts: {id, hash, name, has_params, cache_path}.
    """
    results = []

    # Collect known names from existing projects
    known_names = {}
    for proj in os.listdir(BASE):
        path = os.path.join(BASE, proj, "draft_info.json")
        try:
            with open(path) as f:
                d = json.load(f)
            for ve in d["materials"].get("video_effects", []):
                eid = ve["effect_id"]
                if eid not in known_names:
                    known_names[eid] = ve.get("name", "")
        except Exception:
            pass

    if not os.path.isdir(CACHE_BASE):
        return results

    for eid in os.listdir(CACHE_BASE):
        epath = os.path.join(CACHE_BASE, eid)
        if not os.path.isdir(epath):
            continue
        for h in os.listdir(epath):
            hpath = os.path.join(epath, h)
            config_path = os.path.join(hpath, "config.json")
            if not os.path.exists(config_path):
                continue
            try:
                with open(config_path) as f:
                    cfg = json.load(f)
                links = cfg.get("effect", {}).get("Link", [])
                if not any(l.get("type") == "AmazingFeature" for l in links):
                    continue
                name = known_names.get(eid, cfg.get("name", ""))
                has_params = os.path.exists(os.path.join(hpath, "extra.json"))
                results.append({
                    "id": eid,
                    "hash": h,
                    "name": name,
                    "has_params": has_params,
                    "cache_path": hpath,
                })
            except Exception:
                pass

    return results
