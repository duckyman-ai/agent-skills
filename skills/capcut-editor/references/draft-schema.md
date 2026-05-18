# CapCut Draft JSON Schema Reference

Based on reverse-engineering CapCut desktop (macOS) 8.6.0 blank project files.
Time values are in **microseconds** (1 second = 1,000,000).

## Project Location

```
~/Movies/CapCut/User Data/Projects/com.lveditor.draft/
├── root_meta_info.json              # Project registry (plain JSON)
├── {project-name}/
│   ├── draft_info.json              # Main project data (plain JSON if local, encrypted if template)
│   ├── draft_info.json.bak          # Backup (identical to draft_info.json)
│   ├── draft_meta_info.json         # Metadata (plain JSON)
│   ├── draft_settings               # INI format settings
│   ├── draft_agency_config.json     # Resolution/agency config (plain JSON)
│   ├── draft_biz_config.json        # Empty file (0 bytes)
│   ├── performance_opt_info.json    # Performance optimization (plain JSON)
│   ├── timeline_layout.json         # UI layout state (plain JSON)
│   ├── attachment_pc_common.json    # PC-specific attachments (plain JSON)
│   ├── template-2.tmp               # Full draft_info copy (compact JSON)
│   ├── common_attachment/
│   │   └── attachment_pc_timeline.json
│   └── Timelines/
│       ├── project.json             # Timeline registry (plain JSON)
│       ├── project.json.bak         # Backup
│       └── {timeline_id}/           # Named with the timeline_id UUID
│           ├── draft_info.json      # Same content as root draft_info.json
│           ├── draft_info.json.bak
│           ├── attachment_editing.json
│           ├── attachment_pc_common.json
│           ├── template.tmp         # Draft info with canvas width/height = 0
│           ├── template-2.tmp       # Full draft_info copy
│           └── common_attachment/
│               ├── attachment_action_scene.json
│               ├── attachment_gen_ai_info.json
│               ├── attachment_pc_timeline.json
│               └── attachment_script_video.json
```

## Encryption Note

Projects downloaded from CapCut's template library have encrypted `draft_info.json`
(base64-encoded with proprietary ByteDance encryption). Projects created locally
are **plain JSON** and can be freely read and modified.

To check: try `json.loads(content)`. If it fails, the project is encrypted.

## UUID Scheme

Each project uses **3 separate UUIDs**:

| UUID | Field | Used in |
|------|-------|---------|
| `project_json_id` | `Timelines/project.json` → `id` | Separate registry identifier |
| `timeline_id` | `main_timeline_id`, `draft_info.json` → `id`, timeline folder name | The primary project UUID |
| `draft_id` | `root_meta_info.json` → `draft_id`, `draft_meta_info.json` → `draft_id` | Project registry identifier |

## root_meta_info.json

```json
{
  "root_path": "/Users/.../com.lveditor.draft",
  "draft_ids": 28,
  "all_draft_store": [
    {
      "cloud_draft_cover": false,
      "cloud_draft_sync": false,
      "draft_cloud_last_action_download": false,
      "draft_cloud_purchase_info": "",
      "draft_cloud_template_id": "",
      "draft_cloud_tutorial_info": "",
      "draft_cloud_videocut_purchase_info": "",
      "draft_cover": "/full/path/to/draft_cover.jpg",
      "draft_fold_path": "/full/path/to/project/folder",
      "draft_id": "UUID",
      "draft_is_ai_shorts": false,
      "draft_is_cloud_temp_draft": false,
      "draft_is_invisible": false,
      "draft_is_web_article_video": false,
      "draft_json_file": "/full/path/to/draft_info.json",
      "draft_name": "Project Name",
      "draft_new_version": "",
      "draft_root_path": "/Users/.../com.lveditor.draft",
      "draft_timeline_materials_size": 4106,
      "draft_type": "",
      "draft_web_article_video_enter_from": "",
      "streaming_edit_draft_ready": true,
      "tm_draft_cloud_completed": "",
      "tm_draft_cloud_entry_id": -1,
      "tm_draft_cloud_modified": 0,
      "tm_draft_cloud_parent_entry_id": -1,
      "tm_draft_cloud_space_id": -1,
      "tm_draft_cloud_user_id": -1,
      "tm_draft_create": 1779025749059780,
      "tm_draft_modified": 1779027372997862,
      "tm_draft_removed": 0,
      "tm_duration": 0
    }
  ]
}
```

**Note:** `draft_ids` is an **integer counter**, not an array. CapCut overwrites this
file on every launch — only modify while CapCut is closed.

## draft_meta_info.json

Located inside the project folder. Plain JSON (not encrypted).

```json
{
  "cloud_draft_cover": false,
  "cloud_draft_sync": false,
  "cloud_package_completed_time": "",
  "draft_cloud_capcut_purchase_info": "",
  "draft_cloud_last_action_download": false,
  "draft_cloud_package_type": "",
  "draft_cloud_purchase_info": "",
  "draft_cloud_template_id": "",
  "draft_cloud_tutorial_info": "",
  "draft_cloud_videocut_purchase_info": "",
  "draft_cover": "draft_cover.jpg",
  "draft_deeplink_url": "",
  "draft_enterprise_info": {
    "draft_enterprise_extra": "",
    "draft_enterprise_id": "",
    "draft_enterprise_name": "",
    "enterprise_material": []
  },
  "draft_fold_path": "/full/path/to/project",
  "draft_id": "UUID",
  "draft_is_ae_produce": false,
  "draft_is_ai_packaging_used": false,
  "draft_is_ai_shorts": false,
  "draft_is_ai_translate": false,
  "draft_is_article_video_draft": false,
  "draft_is_cloud_temp_draft": false,
  "draft_is_from_deeplink": "false",
  "draft_is_invisible": false,
  "draft_is_pippit_draft": false,
  "draft_is_web_article_video": false,
  "draft_materials": [
    {"type": 0, "value": []}, {"type": 1, "value": []},
    {"type": 2, "value": []}, {"type": 3, "value": []},
    {"type": 6, "value": []}, {"type": 7, "value": []},
    {"type": 8, "value": []}
  ],
  "draft_materials_copied_info": [],
  "draft_name": "Project Name",
  "draft_need_rename_folder": false,
  "draft_new_version": "",
  "draft_removable_storage_device": "",
  "draft_root_path": "/path/to/com.lveditor.draft",
  "draft_segment_extra_info": [],
  "draft_timeline_materials_size_": 4106,
  "draft_type": "",
  "draft_web_article_video_enter_from": "",
  "tm_draft_cloud_completed": "",
  "tm_draft_cloud_entry_id": -1,
  "tm_draft_cloud_modified": 0,
  "tm_draft_cloud_parent_entry_id": -1,
  "tm_draft_cloud_space_id": -1,
  "tm_draft_cloud_user_id": -1,
  "tm_draft_create": 1779025749059780,
  "tm_draft_modified": 1779027372997862,
  "tm_draft_removed": 0,
  "tm_duration": 0
}
```

## draft_settings (INI format)

```ini
[General]
cloud_last_modify_platform=mac
draft_create_time=1779025749
draft_last_edit_time=1779027372
real_edit_keys=1
real_edit_seconds=14
```

Note: timestamps are in **seconds** (not microseconds or milliseconds).

## Timelines/project.json

```json
{
  "config": {
    "color_space": -1,
    "render_index_track_mode_on": false,
    "use_float_render": false
  },
  "create_time": 1779025749593381,
  "id": "FD00DE93-DC92-4E11-AEDA-2C6E0CCEDC22",
  "main_timeline_id": "2B0D4B14-D3C6-4C63-BCD9-D72D811A5028",
  "timelines": [
    {
      "create_time": 1779025749593381,
      "id": "2B0D4B14-D3C6-4C63-BCD9-D72D811A5028",
      "is_marked_delete": false,
      "name": "Timeline 01",
      "update_time": 1779025749593381
    }
  ],
  "update_time": 1779025749593381,
  "version": 0
}
```

**Important:** `id` is a **separate UUID** from `main_timeline_id`. Only
`main_timeline_id` matches the timeline folder name and `draft_info.json id`.

## draft_info.json (Main Project)

```json
{
  "id": "UUID (timeline_id)",
  "version": 360000,
  "new_version": "169.0.0",
  "name": "",
  "duration": 0,
  "create_time": 0,
  "update_time": 0,
  "fps": 30.0,
  "is_drop_frame_timecode": false,
  "color_space": -1,
  "config": {
    "video_mute": false,
    "record_audio_last_index": 1,
    "extract_audio_last_index": 1,
    "original_sound_last_index": 1,
    "subtitle_recognition_id": "",
    "subtitle_taskinfo": [],
    "lyrics_recognition_id": "",
    "lyrics_taskinfo": [],
    "subtitle_sync": true,
    "lyrics_sync": true,
    "voice_change_sync": false,
    "sticker_max_index": 1,
    "adjust_max_index": 1,
    "material_save_mode": 0,
    "export_range": null,
    "maintrack_adsorb": true,
    "combination_max_index": 1,
    "attachment_info": [],
    "zoom_info_params": null,
    "system_font_list": [],
    "multi_language_mode": "none",
    "multi_language_main": "none",
    "multi_language_current": "none",
    "multi_language_list": [],
    "subtitle_keywords_config": null,
    "use_float_render": false
  },
  "canvas_config": {
    "ratio": "original",
    "width": 1920,
    "height": 1080,
    "background": null
  },
  "tracks": [],
  "group_container": null,
  "materials": { "...": "see Materials section" },
  "keyframes": { "...": "see Keyframes section" },
  "keyframe_graph_list": [],
  "platform": {
    "os": "mac",
    "os_version": "26.3.1",
    "app_id": 359289,
    "app_version": "8.6.0",
    "app_source": "cc",
    "device_id": "hex string",
    "hard_disk_id": "hex string",
    "mac_address": "hex string"
  },
  "last_modified_platform": {
    "os": "mac",
    "os_version": "26.3.1",
    "app_id": 359289,
    "app_version": "8.6.0",
    "app_source": "cc",
    "device_id": "hex string",
    "hard_disk_id": "",
    "mac_address": "hex string"
  },
  "mutable_config": null,
  "cover": null,
  "retouch_cover": null,
  "extra_info": null,
  "relationships": [],
  "render_index_track_mode_on": true,
  "free_render_index_mode_on": false,
  "static_cover_image_path": "",
  "source": "default",
  "time_marks": null,
  "path": "",
  "lyrics_effects": [],
  "uneven_animation_template_info": {
    "composition": "",
    "content": "",
    "order": "",
    "sub_template_info_list": []
  },
  "draft_type": "video",
  "smart_ads_info": {
    "page_from": "",
    "routine": "",
    "draft_url": ""
  },
  "function_assistant_info": { "...": "see Function Assistant section" }
}
```

### Common Canvas Presets

| Name | Width | Height | Ratio |
|------|-------|--------|-------|
| Portrait HD | 1080 | 1920 | 9:16 |
| Landscape HD | 1920 | 1080 | 16:9 |
| Portrait (phone) | 720 | 1280 | 9:16 |
| Landscape | 1280 | 720 | 16:9 |
| Square | 1080 | 1080 | 1:1 |

### Time values for blank projects

Blank projects created by CapCut use `0` for both `create_time` and `update_time`.
When a project has content, these use Unix timestamp in microseconds.

## Tracks

Tracks are the top-level timeline containers. Each track holds segments.

```json
{
  "id": "UUID",
  "type": "video|audio|text|effect|sticker",
  "flag": 0,
  "attribute": 0,
  "name": "",
  "is_default_name": true,
  "segments": []
}
```

### Track Types

- `video` — Video clips, images, GIFs
- `audio` — Music, sound effects, voiceover
- `text` — Text overlays, captions, titles
- `effect` — Video effects (zoom, blur, sparkle, etc.). Segments have `clip: null` and
  `material_id` referencing a `materials.video_effects` entry. Multiple effect segments
  for the same effect type can share one track.
- `sticker` — Animated stickers

## Segments

Each segment references a material via `material_id` and defines timing and transform.

```json
{
  "id": "UUID",
  "material_id": "UUID-matching-materials-entry",
  "target_timerange": {
    "start": 0,
    "duration": 2333333
  },
  "source_timerange": {
    "start": 1200000,
    "duration": 2333333
  },
  "render_timerange": null,
  "clip": {
    "scale": { "x": 1.0, "y": 1.0 },
    "rotation": 0.0,
    "transform": { "x": 0.0, "y": 0.0 },
    "flip": { "vertical": false, "horizontal": false },
    "alpha": 1.0
  },
  "speed": 1.0,
  "volume": 1.0,
  "visible": true,
  "extra_material_refs": [],
  "render_index": 0,
  "keyframe_refs": {},
  "common_keyframes": {},
  "group_id": "",
  "track_render_index": 0,
  "is_placeholder": false
}
```

### Timerange

- `target_timerange` — Position on the timeline (in microseconds)
- `source_timerange` — Which part of the source media to use (null for text/generated content)
- Segments in a track are typically sequential: next `start` = previous `start` + previous `duration`

### Clip Transform

- `scale.x/y` — 1.0 = 100% (normalized to canvas)
- `transform.x/y` — Position offset (-1.0 to 1.0 from center)
- `rotation` — Degrees
- `alpha` — 0.0 (transparent) to 1.0 (opaque)

## Materials

Materials define the actual media/content. Keyed by type, each entry has a UUID `id`
that segments reference via `material_id`.

### Material types (all empty arrays in blank project)

```json
{
  "flowers": [], "videos": [], "tail_leaders": [], "audios": [],
  "images": [], "texts": [], "effects": [], "stickers": [],
  "canvases": [], "transitions": [], "audio_effects": [],
  "audio_fades": [], "beats": [], "material_animations": [],
  "placeholders": [], "placeholder_infos": [], "speeds": [],
  "common_mask": [], "chromas": [], "text_templates": [],
  "realtime_denoises": [], "audio_pannings": [],
  "audio_pitch_shifts": [], "video_trackings": [], "hsl": [],
  "drafts": [], "color_curves": [], "hsl_curves": [],
  "primary_color_wheels": [], "log_color_wheels": [],
  "video_effects": [], "audio_balances": [],
  "handwrites": [], "manual_deformations": [],
  "manual_beautys": [], "plugin_effects": [],
  "sound_channel_mappings": [], "green_screens": [],
  "shapes": [], "material_colors": [], "digital_humans": [],
  "digital_human_model_dressing": [], "smart_crops": [],
  "ai_translates": [], "audio_track_indexes": [],
  "loudnesses": [], "vocal_beautifys": [],
  "vocal_separations": [], "smart_relights": [],
  "time_marks": [], "multi_language_refs": [],
  "video_shadows": [], "video_strokes": [], "video_radius": []
}
```

### materials.videos

```json
{
  "id": "UUID",
  "type": "video",
  "duration": 35800000,
  "path": "/path/to/video.mp4",
  "media_path": "/original/media/path.mp4",
  "width": 2160,
  "height": 3840,
  "has_audio": true,
  "crop": {
    "upper_left_x": 0.0, "upper_left_y": 0.0,
    "upper_right_x": 1.0, "upper_right_y": 0.0,
    "lower_left_x": 0.0, "lower_left_y": 1.0,
    "lower_right_x": 1.0, "lower_right_y": 1.0
  },
  "crop_ratio": "free",
  "source": 0,
  "source_platform": 0
}
```

### materials.audios

```json
{
  "id": "UUID",
  "type": "music",
  "name": "Track Name",
  "duration": 150566666,
  "path": "/path/to/audio.mp3",
  "category_name": "",
  "music_id": "7378240542423533631",
  "source_platform": 0
}
```

### materials.texts

Text content is stored in the `content` field as a JSON-encoded string.

```json
{
  "id": "UUID",
  "type": "text",
  "content": "{\"styles\":[...],\"text\":\"Hello World\"}",
  "text_color": "#008eff",
  "font_size": 15.0,
  "font_path": "/Applications/CapCut.app/Contents/Resources/Font/SystemFont/en.ttf",
  "alignment": 1,
  "global_alpha": 1.0,
  "line_spacing": 0.02,
  "border_width": 0.08,
  "border_color": "#ffffff",
  "text_size": 30,
  "fixed_width": 427.5,
  "line_max_width": 0.82
}
```

**content field** (JSON string):
```json
{
  "text": "Display text here",
  "styles": [{
    "fill": {
      "content": {
        "solid": { "color": [0, 0.557, 1] },
        "render_type": "solid"
      }
    },
    "range": [0, 21],
    "strokes": [{
      "width": 0.06,
      "content": {
        "solid": { "color": [1, 1, 1] },
        "render_type": "solid"
      }
    }],
    "size": 15,
    "font": {
      "path": "/Applications/CapCut.app/Contents/Resources/Font/SystemFont/en.ttf",
      "id": ""
    }
  }]
}
```

Color arrays are `[R, G, B]` normalized 0.0-1.0.
`range` defines character range the style applies to.

### materials.canvases

```json
{
  "id": "UUID",
  "type": "canvas_color",
  "color": "",
  "blur": 0,
  "image": null
}
```

### materials.transitions

```json
{
  "id": "UUID",
  "type": "transition",
  "name": "Suction",
  "effect_id": "7486288371376049413",
  "resource_id": "7486288371376049413",
  "path": "/path/to/effect",
  "duration": 1000000,
  "is_overlap": true
}
```

### materials.speeds

```json
{
  "id": "UUID",
  "type": "speed",
  "mode": 0,
  "speed": 1.0,
  "curve_speed": null
}
```

### materials.material_animations

```json
{
  "id": "UUID",
  "type": "sticker_animation",
  "animations": [],
  "multi_language_current": "none"
}
```

### materials.video_effects

Video effects (zoom, blur, sparkle, etc.) applied to clips via `effect` tracks.

```json
{
  "id": "UUID",
  "effect_id": "7399465441057328389",
  "resource_id": "7399465441057328389",
  "name": "Zoom Lens",
  "type": "video_effect",
  "sub_type": 0,
  "bind_segment_id": "",
  "transparent_params": [],
  "path": "/Users/admin/Library/Containers/com.lemon.lvoverseas/Data/Movies/CapCut/User Data/Cache/effect/7399465441057328389/60a68556b7df52cc36d20d1f565b4569",
  "value": "",
  "category_id": "27296",
  "category_name": "Trending",
  "platform": "all",
  "apply_target_type": 2,
  "source_platform": 1,
  "version": "",
  "item_effect_type": 0,
  "adjust_params": [
    {"name": "effects_adjust_speed", "value": 0.01, "default_value": 0.33},
    {"name": "effects_adjust_range", "value": 0.07, "default_value": 0.3}
  ],
  "time_range": {},
  "formula_id": "",
  "apply_time_range": {},
  "render_index": 11001,
  "track_render_index": 2,
  "common_keyframes": {},
  "request_id": "",
  "algorithm_artifact_path": "",
  "disable_effect_faces": False,
  "covering_relation_change": {},
  "enable_mask": False,
  "effect_mask": {},
  "enable_video_mask_stroke": False,
  "enable_video_mask_shadow": False,
  "is_ai_generate_effect": False,
  "is_third_party": False,
  "meta": "",
  "resource_name": "",
  "sub_effects": [],
  "track_id": ""
}
```

**Key fields:**
- `effect_id` — The CapCut effect identifier (also the cache directory name)
- `path` — Must point to the cached effect files on disk
- `adjust_params` — Effect-specific parameters; each has `name`, `value`, `default_value`
- `apply_target_type: 2` — Standard for clip-level effects

**Effect track segment** (on a `type: "effect"` track):

```json
{
  "id": "UUID",
  "material_id": "UUID-of-video_effect-entry",
  "target_timerange": {"start": 46200000, "duration": 4900000},
  "source_timerange": null,
  "render_timerange": null,
  "clip": null,
  "speed": 1.0,
  "volume": 1.0,
  "visible": true,
  "extra_material_refs": [],
  "render_index": 11001,
  "keyframe_refs": {},
  "common_keyframes": {},
  "group_id": "",
  "track_render_index": 2,
  "is_placeholder": false
}
```

Effect segments always have `clip: null`, `source_timerange: null`, `extra_material_refs: []`.
The `target_timerange` must match the video clip the effect applies to.

### materials.transitions

Transitions between consecutive clips. Referenced in the **outgoing segment's**
`extra_material_refs`. The transition overlaps the boundary between two clips.

```json
{
  "id": "UUID",
  "type": "transition",
  "name": "Suction",
  "effect_id": "7486288371376049413",
  "resource_id": "7486288371376049413",
  "third_resource_id": "0",
  "source_platform": 1,
  "path": "/path/to/cache/effect/...",
  "duration": 1000000,
  "is_overlap": true,
  "platform": "all",
  "category_id": "32431",
  "category_name": "Pro",
  "request_id": "",
  "is_ai_transition": false,
  "video_path": "",
  "task_id": ""
}
```

**Key fields:**
- `duration` — Transition duration in microseconds (typically 500000-1000000 = 0.5-1.0s)
- `is_overlap` — Always `true` for standard transitions
- Referenced by adding the transition's `id` to the outgoing segment's `extra_material_refs`
- The outgoing segment is the clip that *ends* at the gap (not the incoming clip)

### materials.hsl

HSL (Hue, Saturation, Lightness) color grading per clip. Referenced in a segment's
`extra_material_refs` with `enable_hsl: true` on the segment.

```json
{
  "id": "UUID",
  "constant_material_id": "UUID",
  "hsl_color_type": 1,
  "hue": 0,
  "saturation": 0,
  "lightness": 0,
  "interacting": true,
  "version": "1",
  "path": "/path/to/hsl/cache",
  "type": "hsl",
  "lumi_hub_path": "/path/to/hsl/cache/lumi_hub_path",
  "custom_color": "#FFE64444",
  "resource_id": "",
  "source_platform": 0
}
```

**Key fields:**
- `hue` — -180 to 180
- `saturation` — -100 to 100
- `lightness` — -100 to 100
- `hsl_color_type` — 1 = standard
- `constant_material_id` — Separate UUID for internal tracking
- Segment must have `enable_hsl: true` for the adjustment to render
- Each clip needs its own HSL material entry

### materials.audio_fades

```json
{
  "id": "UUID",
  "type": "audio_fade",
  "fade_type": "audio_fade",
  "fade_in_duration": 500000,
  "fade_out_duration": 500000
}
```

## Keyframes

```json
{
  "videos": [],
  "audios": [],
  "texts": [],
  "stickers": [],
  "filters": [],
  "adjusts": [],
  "handwrites": [],
  "effects": []
}
```

## Function Assistant Info

CapCut 8.6.0 stores AI feature state in `function_assistant_info`:

```json
{
  "smart_rec_applied": false,
  "fixed_rec_applied": false,
  "auto_adjust": false,
  "auto_adjust_segid_list": [],
  "color_correction": false,
  "color_correction_segid_list": [],
  "enhance_quality": false,
  "smooth_slow_motion": false,
  "deflicker_segid_list": [],
  "video_noise_segid_list": [],
  "enhance_quality_segid_list": [],
  "smart_segid_list": [],
  "retouch": false,
  "retouch_segid_list": [],
  "enhande_voice": false,
  "enhance_voice_segid_list": [],
  "audio_noise_segid_list": [],
  "auto_caption": false,
  "auto_caption_segid_list": [],
  "auto_caption_template_id": "",
  "caption_opt": false,
  "caption_opt_segid_list": [],
  "eye_correction": false,
  "eye_correction_segid_list": [],
  "normalize_loudness": false,
  "normalize_loudness_segid_list": [],
  "normalize_loudness_audio_denoise_segid_list": [],
  "auto_adjust_fixed": false,
  "auto_adjust_fixed_value": 50.0,
  "color_correction_fixed": false,
  "color_correction_fixed_value": 50.0,
  "normalize_loudness_fixed": false,
  "enhande_voice_fixed": false,
  "retouch_fixed": false,
  "enhance_quality_fixed": false,
  "smooth_slow_motion_fixed": false,
  "fps": { "num": 0, "den": 1 }
}
```

## Support Files

### draft_agency_config.json

```json
{
  "is_auto_agency_enabled": false,
  "is_auto_agency_popup": false,
  "is_single_agency_mode": false,
  "marterials": null,
  "use_converter": false,
  "video_resolution": 720
}
```

### performance_opt_info.json

```json
{
  "manual_cancle_precombine_segs": null,
  "need_auto_precombine_segs": null
}
```

### timeline_layout.json

```json
{
  "dockItems": [{
    "dockIndex": 0,
    "ratio": 1,
    "timelineIds": ["TIMELINE_UUID"],
    "timelineNames": ["Timeline 01"]
  }],
  "layoutOrientation": 1
}
```

### attachment_pc_common.json

```json
{
  "ai_packaging_infos": [],
  "ai_packaging_report_info": {
    "caption_id_list": [],
    "commercial_material": "",
    "material_source": "",
    "method": "",
    "page_from": "",
    "style": "",
    "task_id": "",
    "text_style": "",
    "tos_id": "",
    "video_category": ""
  },
  "broll": {
    "ai_packaging_infos": [],
    "ai_packaging_report_info": { "..." : "same structure" }
  },
  "commercial_music_category_ids": [],
  "pc_feature_flag": 0,
  "recognize_tasks": [],
  "reference_lines_config": {
    "horizontal_lines": [],
    "is_lock": false,
    "is_visible": false,
    "vertical_lines": []
  },
  "safe_area_type": 0,
  "template_item_infos": [],
  "unlock_template_ids": []
}
```

## Time Conversion

```
seconds → microseconds: multiply by 1,000,000
microseconds → seconds: divide by 1,000,000

1 second    = 1,000,000 μs
3.5 seconds = 3,500,000 μs

For 30fps frame-aligned durations:
  1 frame ≈ 33,333 μs (technically 1,000,000/30 = 33,333.33...)
```
