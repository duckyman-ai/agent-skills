---
name: capcut-editor
description: >
  Read, analyze, and create CapCut desktop (macOS) video editing projects programmatically.
  Use this skill whenever the user mentions CapCut, video editing with CapCut, reading
  CapCut projects, creating CapCut-compatible drafts, adding video/audio/text tracks to
  CapCut, or wants to automate any CapCut desktop workflow. Also use when the user wants
  to batch-create video projects, insert media into CapCut, or manage CapCut project files.
---

# CapCut Desktop Project Skill

Programmatically read, create, and modify CapCut desktop (macOS) project files.

## Important Limitation

**Only locally-created projects can be read/written.** Projects downloaded from CapCut's
template library have encrypted `draft_info.json` files (base64-encoded with proprietary
ByteDance encryption) and cannot be modified. Always check by attempting `json.loads()` —
if it fails, the project is encrypted.

## Project Location

```
BASE = ~/Movies/CapCut/User Data/Projects/com.lveditor.draft/
```

## Quick Reference

Read `references/draft-schema.md` for the complete JSON schema with field descriptions
and time conversion rules.

## Commands

### List all projects

```bash
python3 -c "
import json, os
base = os.path.expanduser('~/Movies/CapCut/User Data/Projects/com.lveditor.draft')
with open(os.path.join(base, 'root_meta_info.json')) as f:
    data = json.load(f)
for d in data['all_draft_store']:
    name = d.get('draft_name', d['draft_fold_path'].split('/')[-1])
    dur = d.get('tm_duration', 0)
    secs = dur / 1000000 if dur else 0
    print(f'{name:30s}  {secs:>6.1f}s  {d[\"draft_fold_path\"]}')
"
```

### Check if a project is readable (not encrypted)

```bash
python3 -c "
import json, os
base = os.path.expanduser('~/Movies/CapCut/User Data/Projects/com.lveditor.draft')
path = os.path.join(base, 'PROJECT_NAME', 'draft_info.json')
try:
    with open(path) as f: json.load(f)
    print('READABLE (plain JSON)')
except:
    print('ENCRYPTED (template project — cannot modify)')
"
```

### Read project summary

```bash
python3 -c "
import json, os
base = os.path.expanduser('~/Movies/CapCut/User Data/Projects/com.lveditor.draft')
with open(os.path.join(base, 'PROJECT_NAME', 'draft_info.json')) as f:
    d = json.load(f)
print(f'ID: {d[\"id\"]}')
print(f'Duration: {d[\"duration\"]/1000000:.1f}s')
print(f'FPS: {d[\"fps\"]}')
print(f'Canvas: {d[\"canvas_config\"][\"width\"]}x{d[\"canvas_config\"][\"height\"]}')
tracks = d.get('tracks', [])
print(f'Tracks: {len(tracks)}')
for i, t in enumerate(tracks):
    segs = t.get('segments', [])
    print(f'  Track {i}: {t[\"type\"]} ({len(segs)} segments)')
mats = d.get('materials', {})
for k, v in mats.items():
    if isinstance(v, list) and len(v) > 0:
        print(f'  materials.{k}: {len(v)}')
"
```

### Create a new project from scratch

```bash
python3 scripts/create-project.py <name> [--width 1920] [--height 1080] [--fps 30]
```

### View and edit clips

```bash
# Show full timeline overview (tracks, segments, timing, transforms)
python3 scripts/edit-clips.py <project> --info

# Scale clips (1.0 = 100%, 1.5 = 150%)
python3 scripts/edit-clips.py <project> --scale 1.2 --clips 0 5 10
python3 scripts/edit-clips.py <project> --scale 1.1 --range 3-19

# Speed (0.5 = half speed, 2.0 = double)
python3 scripts/edit-clips.py <project> --speed 2.0 --clips 5
python3 scripts/edit-clips.py <project> --speed 0.5 --all

# Volume (0.0 = mute, 1.0 = normal, 2.0 = double)
python3 scripts/edit-clips.py <project> --volume 0 --range 0-2
python3 scripts/edit-clips.py <project> --mute --all

# Rotate/flip/opacity
python3 scripts/edit-clips.py <project> --rotate 90 --clips 2
python3 scripts/edit-clips.py <project> --flip-h --clips 3
python3 scripts/edit-clips.py <project> --opacity 0.8 --clips 0

# Trim clip to first N seconds
python3 scripts/edit-clips.py <project> --trim 3.5 --clips 0

# Split clip at position (seconds from clip start)
python3 scripts/edit-clips.py <project> --split 2.5 --clips 0

# Remove clips
python3 scripts/edit-clips.py <project> --remove --clips 10 11 12

# Move clip from index to index
python3 scripts/edit-clips.py <project> --move 5 --to 10

# Reset transforms
python3 scripts/edit-clips.py <project> --reset --clips 0 1 2
```

### Edit audio tracks

```bash
# Audio tracks shown in --info output
python3 scripts/edit-clips.py <project> --info

# Volume (0.0=mute, 1.0=normal)
python3 scripts/edit-clips.py <project> --audio-track --volume 0.5 --all
python3 scripts/edit-clips.py <project> --audio-track --mute --clips 0

# Move audio segment to align with video (seconds from timeline start)
python3 scripts/edit-clips.py <project> --audio-track --position 10.5 --clips 0

# Select which audio track (0=first, 1=second, etc.)
python3 scripts/edit-clips.py <project> --audio-track --track-index 2 --volume 0.8 --all

# Speed up/slow down audio
python3 scripts/edit-clips.py <project> --audio-track --speed 1.5 --clips 0

# Trim audio to first N seconds
python3 scripts/edit-clips.py <project> --audio-track --trim 5.0 --clips 0

# Remove audio segment
python3 scripts/edit-clips.py <project> --audio-track --remove --clips 2

# Fade in/out (seconds)
python3 scripts/edit-clips.py <project> --audio-track --fade-in 0.5 --clips 0
python3 scripts/edit-clips.py <project> --audio-track --fade-out 1.0 --clips 0
```

### Add video effects (zoom, blur, sparkle, etc.)

```bash
# List built-in effect shortcuts (20 effects)
python3 scripts/add-effect.py --list-effects

# Scan ALL cached effects (404+ downloaded effects)
python3 scripts/add-effect.py --scan-cache

# Add Zoom Lens to all clips
python3 scripts/add-effect.py <project> --effect zoom-lens --all

# Add Sparkle to specific clips
python3 scripts/add-effect.py <project> --effect sparkle --clips 0 5 10

# Add any cached effect by ID (from --scan-cache)
python3 scripts/add-effect.py <project> --effect-id 7399469087174233349 --all

# Add Blur to a range with custom parameters
python3 scripts/add-effect.py <project> --effect blur --range 3-19 --speed 0.02 --param-range 0.06

# Remove all effects
python3 scripts/add-effect.py <project> --clear
```

### Add transitions between clips

```bash
# List available transitions
python3 scripts/add-transition.py --list

# Add transition between two adjacent clips
python3 scripts/add-transition.py <project> --between 19 20

# Add transitions between all consecutive clips
python3 scripts/add-transition.py <project> --all-gaps

# Add at specific gaps with custom duration
python3 scripts/add-transition.py <project> --gaps 2 5 10 --duration 0.5

# Remove all transitions
python3 scripts/add-transition.py <project> --clear
```

### Add color grading (HSL)

```bash
# Show current color settings per clip
python3 scripts/add-color.py <project> --info

# Custom HSL values (hue: -180~180, sat: -100~100, light: -100~100)
python3 scripts/add-color.py <project> --hsl --hue 10 --saturation 20 --lightness -5 --clips 0 1 2
python3 scripts/add-color.py <project> --hsl --saturation 30 --all

# Presets
python3 scripts/add-color.py <project> --preset warm --all
python3 scripts/add-color.py <project> --preset vivid --range 0-10
python3 scripts/add-color.py <project> --preset moody --all

# Available presets: warm, cool, vivid, moody, vintage, fade
# Remove all color grading
python3 scripts/add-color.py <project> --clear
```

### Add text overlays

```bash
# Single text
python3 scripts/add-text.py <project> --text "Hello" --start 0 --duration 5 --y -0.65 --size 14

# With a specific font
python3 scripts/add-text.py <project> --text "สวัสดี" --font sarabun-bold --size 14
python3 scripts/add-text.py <project> --text "Hello" --font /full/path/to/font.ttf

# List available font aliases
python3 scripts/add-text.py --list-fonts

# From a JSON file
python3 scripts/add-text.py <project> --from-file texts.json

# Remove all text
python3 scripts/add-text.py <project> --clear
```

JSON file format (supports `font` field):
```json
[
  {"text": "Opening title", "start": 0, "duration": 4.5, "y": -0.65, "size": 14, "font": "thai"},
  {"text": "Subtitle", "start": 5.4, "duration": 2, "y": 0.7, "size": 10, "font": "sarabun-bold"}
]
```

Built-in font aliases: `default`, `en`, `th`/`thai`, `noto`, `noto-thai`, `capcut`/`capcut-bold`/`capcut-medium`,
`sarabun`/`sarabun-bold`/`sarabun-light`/`sarabun-med`/`sarabun-thin`, `thsarabun`/`thsarabun-new`,
`db-helv-med`/`db-helv-bold`. Or pass any full path to a `.ttf`/`.otf` file.

### Create project manually

The `create-project.py` script handles everything. Alternatively, create manually:

1. Generate **3 separate UUIDs**: `project_json_id`, `timeline_id`, `draft_id`
2. Create the folder structure (22 files total — see below)
3. **CapCut MUST be closed** — it overwrites `root_meta_info.json` on launch

### Required file structure (22 files)

```
PROJECT_NAME/
├── draft_info.json                          # Main project data
├── draft_info.json.bak                      # Backup (identical to draft_info.json)
├── draft_meta_info.json                     # Project metadata (plain JSON)
├── draft_settings                           # INI format settings
├── draft_agency_config.json                 # Resolution/agency config
├── draft_biz_config.json                    # Empty file (0 bytes)
├── performance_opt_info.json                # Performance optimization
├── timeline_layout.json                     # UI layout with timeline UUID
├── attachment_pc_common.json                # PC-specific attachments
├── template-2.tmp                           # Full draft_info copy
├── common_attachment/
│   └── attachment_pc_timeline.json          # Timeline reference lines config
└── Timelines/
    ├── project.json                         # Timeline registry (separate id!)
    ├── project.json.bak                     # Backup
    └── {timeline_id}/                       # Named with timeline_id UUID
        ├── draft_info.json                  # Same content as root draft_info.json
        ├── draft_info.json.bak
        ├── attachment_editing.json          # Edit state
        ├── attachment_pc_common.json        # Same as root level
        ├── template.tmp                     # Draft info with canvas w/h = 0
        ├── template-2.tmp                   # Full draft_info copy
        └── common_attachment/
            ├── attachment_action_scene.json
            ├── attachment_gen_ai_info.json
            ├── attachment_pc_timeline.json
            └── attachment_script_video.json
```

### UUID scheme

CapCut uses **3 separate UUIDs** for each project:

| UUID | Used in | Notes |
|------|---------|-------|
| `project_json_id` | `Timelines/project.json` → `id` | Separate from timeline |
| `timeline_id` | `Timelines/project.json` → `main_timeline_id`, `draft_info.json` → `id`, timeline folder name | The primary project UUID |
| `draft_id` | `root_meta_info.json` → `draft_id`, `draft_meta_info.json` → `draft_id` | Registry identifier |

### Key parameters

- `canvas_config.width/height` — 1080×1920 for 9:16 portrait, 1920×1080 for 16:9 landscape
- `fps` — 30.0 (standard)
- `create_time` / `update_time` — microseconds (0 for blank project)
- `tm_draft_create` / `tm_draft_modified` — microseconds (Unix timestamp × 1,000,000)

### Register in root_meta_info.json

When creating a project, add an entry to `all_draft_store` in `root_meta_info.json`:

```python
import json, os, uuid, time

BASE = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
dst = os.path.join(BASE, "PROJECT_NAME")
meta_path = os.path.join(BASE, "root_meta_info.json")

with open(meta_path) as f:
    meta = json.load(f)

meta["all_draft_store"].insert(0, {
    "cloud_draft_cover": False,
    "cloud_draft_sync": False,
    "draft_cloud_last_action_download": False,
    "draft_cloud_purchase_info": "",
    "draft_cloud_template_id": "",
    "draft_cloud_tutorial_info": "",
    "draft_cloud_videocut_purchase_info": "",
    "draft_cover": os.path.join(dst, "draft_cover.jpg"),
    "draft_fold_path": dst,
    "draft_id": str(uuid.uuid4()).upper(),
    "draft_is_ai_shorts": False,
    "draft_is_cloud_temp_draft": False,
    "draft_is_invisible": False,
    "draft_is_web_article_video": False,
    "draft_json_file": os.path.join(dst, "draft_info.json"),
    "draft_name": "PROJECT_NAME",
    "draft_new_version": "",
    "draft_root_path": BASE,
    "draft_timeline_materials_size": 4106,
    "draft_type": "",
    "draft_web_article_video_enter_from": "",
    "streaming_edit_draft_ready": True,
    "tm_draft_cloud_completed": "",
    "tm_draft_cloud_entry_id": -1,
    "tm_draft_cloud_modified": 0,
    "tm_draft_cloud_parent_entry_id": -1,
    "tm_draft_cloud_space_id": -1,
    "tm_draft_cloud_user_id": -1,
    "tm_draft_create": int(time.time() * 1_000_000),
    "tm_draft_modified": int(time.time() * 1_000_000),
    "tm_draft_removed": 0,
    "tm_duration": 0,
})

if isinstance(meta.get("draft_ids"), int):
    meta["draft_ids"] += 1

with open(meta_path, "w") as f:
    json.dump(meta, f, separators=(",", ":"))
```

### Add a video clip to a project

1. Generate UUIDs for: segment, video material, canvas material, speed material,
   placeholder_info, sound_channel_mapping, vocal_separation, material_color
2. Add a `video` material to `materials.videos` with the video file path and metadata
3. Add a `canvas_color` material to `materials.canvases`
4. Add entries to `materials.speeds`, `materials.placeholder_infos`,
   `materials.sound_channel_mappings`, `materials.vocal_separations`, `materials.material_colors`
5. Add a segment to the target video track with:
   - `material_id` → video material UUID
   - `extra_material_refs` → [speed_uuid, canvas_uuid, placeholder_uuid, sound_ch_uuid,
     vocal_sep_uuid, material_color_uuid]
   - `target_timerange` → { start: cumulative position, duration: clip length in μs }
   - `source_timerange` → { start: 0, duration: clip length in μs }
6. Update `duration` at the project root level

### Add an audio track

1. Generate UUIDs for: segment, audio material, audio_fade, beats, speed,
   placeholder_info, sound_channel_mapping, vocal_separation
2. Add `audio` material to `materials.audios`
3. Add entries to `materials.audio_fades`, `materials.beats`, `materials.speeds`,
   `materials.placeholder_infos`, `materials.sound_channel_mappings`, `materials.vocal_separations`
4. Either add a new track of `type: "audio"` or add segment to existing audio track
5. Segment `clip` should be `null` for audio

### Add a text overlay

1. Generate UUID for: segment and text material
2. Add text material to `materials.texts` with:
   - `content` — JSON-encoded string with `text` and `styles` array
   - `font_size`, `text_color`, `alignment`, `line_max_width`
3. Add segment to a `type: "text"` track (create one if needed)
   - `source_timerange` should be `null` for text
   - `clip.transform.y` controls vertical position (e.g., 0.7 = lower third)

### Text content field format

```python
import json
content = json.dumps({
    "text": "Your text here",
    "styles": [{
        "fill": {
            "content": {
                "solid": {"color": [1.0, 1.0, 1.0]},
                "render_type": "solid"
            }
        },
        "range": [0, len("Your text here")],
        "strokes": [{
            "width": 0.06,
            "content": {
                "solid": {"color": [0, 0, 0]},
                "render_type": "solid"
            }
        }],
        "size": 15,
        "font": {
            "path": "/Applications/CapCut.app/Contents/Resources/Font/SystemFont/en.ttf",
            "id": ""
        }
    }]
})
```

Colors in `styles` are `[R, G, B]` normalized 0.0-1.0 (not hex).

### Add video effects (zoom, blur, sparkle, etc.)

Video effects are placed on `type: "effect"` tracks and reference entries in
`materials.video_effects`. Each segment on an effect track matches the timing of
a video clip it applies to. Multiple effects can share one track via separate segments.

**Structure:**

1. Create a video_effect material in `materials.video_effects`
2. Create a segment on an `effect` track with `target_timerange` matching the video clip
3. The segment's `material_id` points to the video_effect entry

```python
import uuid, os

CACHE_BASE = "/Users/admin/Library/Containers/com.lemon.lvoverseas/Data/Movies/CapCut/User Data/Cache/effect"

def gen_uuid():
    return str(uuid.uuid4()).upper()

# Create a video effect material
effect_id = "7399465441057328389"  # Zoom Lens
effect_hash = "60a68556b7df52cc36d20d1f565b4569"
effect_path = os.path.join(CACHE_BASE, effect_id, effect_hash)

mat_id = gen_uuid()
video_effect = {
    "id": mat_id,
    "effect_id": effect_id,
    "resource_id": effect_id,
    "name": "Zoom Lens",
    "type": "video_effect",
    "path": effect_path,
    "adjust_params": [
        {"name": "effects_adjust_speed", "value": 0.01, "default_value": 0.33},
        {"name": "effects_adjust_range", "value": 0.07, "default_value": 0.3}
    ],
    "category_id": "27296",
    "category_name": "Trending",
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

# Add to materials
draft["materials"]["video_effects"].append(video_effect)

# Create effect segment (timing matches video clip)
effect_segment = {
    "id": gen_uuid(),
    "material_id": mat_id,
    "target_timerange": {"start": clip_start_us, "duration": clip_duration_us},
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

# Add to an existing effect track, or create one
effect_track = {
    "id": gen_uuid(),
    "type": "effect",
    "flag": 0,
    "attribute": 0,
    "name": "",
    "is_default_name": True,
    "segments": [effect_segment],
}
draft["tracks"].append(effect_track)
```

**Key notes:**
- Effect segments have `clip: null`, `source_timerange: null`, `extra_material_refs: []`
- Multiple effect segments for the same effect can go on a single effect track
- `render_index: 11001` and `track_render_index: 2` are typical values (from observed projects)
- Each effect needs its own video_effect material (separate UUID) even if using the same effect_id
- Effect files must exist in the CapCut cache (user must have used the effect at least once)

### Discover available effects from cache

```bash
# Scan all 404+ cached video effects
python3 scripts/add-effect.py --scan-cache
```

Or manually scan the cache:

```bash
python3 -c "
import os, json
CACHE = '/Users/admin/Library/Containers/com.lemon.lvoverseas/Data/Movies/CapCut/User Data/Cache/effect'
for eid in sorted(os.listdir(CACHE)):
    epath = os.path.join(CACHE, eid)
    if not os.path.isdir(epath): continue
    for h in os.listdir(epath):
        hpath = os.path.join(epath, h)
        config = os.path.join(hpath, 'config.json')
        if os.path.exists(config):
            try:
                with open(config) as f: data = json.load(f)
                name = data.get('name', '')
                if name: print(f'{eid:>20s}  {h}  {name}')
            except: pass
"
```

### Get effect info from an existing project

If a user has applied an effect in CapCut, extract the full structure:

```bash
python3 -c "
import json, os
base = os.path.expanduser('~/Movies/CapCut/User Data/Projects/com.lveditor.draft')
with open(os.path.join(base, 'PROJECT_NAME', 'draft_info.json')) as f:
    d = json.load(f)
for ve in d['materials'].get('video_effects', []):
    print(f'  {ve[\"name\"]:30s}  effect_id={ve[\"effect_id\"]}')
    print(f'    adjust_params={ve.get(\"adjust_params\", [])}')
    print(f'    path={ve.get(\"path\", \"\")}')
"
```

### Built-in effect reference

These effects are commonly cached after using CapCut. The `effect_id` is the identifier
used in `video_effect.effect_id` and the cache directory name. The `hash` is the
subdirectory inside the effect's cache folder.

| Effect | effect_id | hash | adjust_params |
|--------|-----------|------|---------------|
| Zoom Lens | `7399465441057328389` | `60a68556b7df52cc36d20d1f565b4569` | speed, range |
| Slow Zoom | `7399468961949125894` | `56b46f1ebc45c47730d3f7c2569200fc` | — |
| Slight Zoom | `7399463624906984709` | `c09004507723569a3e762494d4ffda7d` | — |
| Full Zoom | `7399470808759815429` | `24749b428adbacfa9712b8a249912905` | — |
| Zoom Far | `6724226338418332167` | `8d97f1c1a60d9393c97ff4e9da0669ae` | — |
| Blur | `7399464929830423813` | `2db7bf49d9349e308ef0f46c39b14abf` | — |
| Blur Opening | `7399468886309162246` | `5dd4bf7e879fe7356e3e27e5105f5af1` | — |
| Soft Light | `7399467970071743749` | `258b5bd7ba1fb94dce800bc496a30ed9` | — |
| Bokeh | `7399470883863088389` | `1c8442102d00628a4958e488251a75e7` | — |
| Dark Corner | `7399463239379209477` | `ef7abad9671e2f3da7993b7673ece5fc` | — |
| Sparkle | `7399469087174233349` | `816803366dd866837e21380513b81e33` | — |
| Flashing Light | `7399472112223669510` | `d7c42c303074967c0cad7c7a6adfe896` | — |
| Color Shift | `7399470160203107589` | `53c8584c8174f887b2802540dd28955b` | — |
| Fog | `7399471802361105669` | `bdda3043cfa04aa56d2806ada93367ae` | — |
| Oil Paint | `11353735` | `118b5e6a07a603581825a0fa8bb08e35` | — |
| Rainbow Bubble | `7399470727121947910` | `ae2e32daa7af0fa8f4b61a0c5aacd196` | — |
| Petals Falling | `7399464130664500486` | `a772c059e7fb8304292e7ebb870e8eb3` | — |
| Curtain Close | `7399468499044683013` | `05c17ac3298c0521cd91a720850a27de` | — |
| Star Shift | `7399470054053547270` | `f1c6583c2a7227b6ccf002863fdfdf65` | — |

**Note:** Effect availability depends on what the user has downloaded/used in CapCut.
Always verify the cache path exists before using an effect. If an effect isn't cached,
ask the user to apply it once in CapCut, then close CapCut and re-read the project.

## Time System

All time values in CapCut are **microseconds** (μs).

```
1 second = 1,000,000 μs
30fps frame ≈ 33,333 μs
```

## UUID Generation

```python
import uuid
str(uuid.uuid4()).upper()
# Example: "595F710B-F0C1-44C6-AA60-525CF85705D5"
```

## Safety

- **CapCut MUST be closed** when creating/modifying projects — it overwrites files on launch
- Always back up `draft_info.json` before modifying
- Always back up `root_meta_info.json` before adding/removing projects
- To check if CapCut is running: `pgrep -fl "CapCut|lvoverseas|lemon"`
