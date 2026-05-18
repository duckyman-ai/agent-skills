#!/usr/bin/env python3
"""Create a new CapCut desktop project from scratch.

Based on the exact file structure of a blank CapCut 8.6.0 project (0517).

Usage:
    python3 create-project.py <project-name> [--width 1920] [--height 1080] [--fps 30]

Requires CapCut to be CLOSED — it overwrites root_meta_info.json on launch.
"""

import json, os, sys, time, shutil, argparse

sys.path.insert(0, os.path.dirname(__file__))
from _common import BASE, check_capcut_closed, gen_uuid


def now_us():
    return int(time.time() * 1_000_000)


def now_sec():
    return int(time.time())


def get_machine_ids():
    """Read device_id, hard_disk_id, mac_address from an existing project."""
    for name in sorted(os.listdir(BASE)):
        path = os.path.join(BASE, name, "draft_info.json")
        if not os.path.exists(path):
            continue
        try:
            with open(path) as f:
                d = json.load(f)
            plat = d.get("platform", {})
            if "device_id" in plat:
                return {
                    "device_id": plat["device_id"],
                    "hard_disk_id": plat.get("hard_disk_id", ""),
                    "mac_address": plat.get("mac_address", ""),
                    "os_version": plat.get("os_version", ""),
                }
        except Exception:
            continue
    return {"device_id": "", "hard_disk_id": "", "mac_address": "", "os_version": ""}


def make_draft_info(timeline_id, width, height, fps, machine):
    return {
        "id": timeline_id,
        "version": 360000,
        "new_version": "169.0.0",
        "name": "",
        "duration": 0,
        "create_time": 0,
        "update_time": 0,
        "fps": fps,
        "is_drop_frame_timecode": False,
        "color_space": -1,
        "config": {
            "video_mute": False,
            "record_audio_last_index": 1,
            "extract_audio_last_index": 1,
            "original_sound_last_index": 1,
            "subtitle_recognition_id": "",
            "subtitle_taskinfo": [],
            "lyrics_recognition_id": "",
            "lyrics_taskinfo": [],
            "subtitle_sync": True,
            "lyrics_sync": True,
            "voice_change_sync": False,
            "sticker_max_index": 1,
            "adjust_max_index": 1,
            "material_save_mode": 0,
            "export_range": None,
            "maintrack_adsorb": True,
            "combination_max_index": 1,
            "attachment_info": [],
            "zoom_info_params": None,
            "system_font_list": [],
            "multi_language_mode": "none",
            "multi_language_main": "none",
            "multi_language_current": "none",
            "multi_language_list": [],
            "subtitle_keywords_config": None,
            "use_float_render": False,
        },
        "canvas_config": {
            "ratio": "original",
            "width": width,
            "height": height,
            "background": None,
        },
        "tracks": [],
        "group_container": None,
        "materials": {
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
            "video_shadows": [], "video_strokes": [], "video_radius": [],
        },
        "keyframes": {
            "videos": [], "audios": [], "texts": [], "stickers": [],
            "filters": [], "adjusts": [], "handwrites": [], "effects": [],
        },
        "keyframe_graph_list": [],
        "platform": {
            "os": "mac",
            "os_version": machine["os_version"],
            "app_id": 359289,
            "app_version": "8.6.0",
            "app_source": "cc",
            "device_id": machine["device_id"],
            "hard_disk_id": machine["hard_disk_id"],
            "mac_address": machine["mac_address"],
        },
        "last_modified_platform": {
            "os": "mac",
            "os_version": machine["os_version"],
            "app_id": 359289,
            "app_version": "8.6.0",
            "app_source": "cc",
            "device_id": machine["device_id"],
            "hard_disk_id": "",
            "mac_address": machine["mac_address"],
        },
        "mutable_config": None,
        "cover": None,
        "retouch_cover": None,
        "extra_info": None,
        "relationships": [],
        "render_index_track_mode_on": True,
        "free_render_index_mode_on": False,
        "static_cover_image_path": "",
        "source": "default",
        "time_marks": None,
        "path": "",
        "lyrics_effects": [],
        "uneven_animation_template_info": {
            "composition": "", "content": "", "order": "",
            "sub_template_info_list": [],
        },
        "draft_type": "video",
        "smart_ads_info": {"page_from": "", "routine": "", "draft_url": ""},
        "function_assistant_info": {
            "smart_rec_applied": False, "fixed_rec_applied": False,
            "auto_adjust": False, "auto_adjust_segid_list": [],
            "color_correction": False, "color_correction_segid_list": [],
            "enhance_quality": False, "smooth_slow_motion": False,
            "deflicker_segid_list": [], "video_noise_segid_list": [],
            "enhance_quality_segid_list": [], "smart_segid_list": [],
            "retouch": False, "retouch_segid_list": [],
            "enhande_voice": False, "enhance_voice_segid_list": [],
            "audio_noise_segid_list": [],
            "auto_caption": False, "auto_caption_segid_list": [],
            "auto_caption_template_id": "",
            "caption_opt": False, "caption_opt_segid_list": [],
            "eye_correction": False, "eye_correction_segid_list": [],
            "normalize_loudness": False, "normalize_loudness_segid_list": [],
            "normalize_loudness_audio_denoise_segid_list": [],
            "auto_adjust_fixed": False, "auto_adjust_fixed_value": 50.0,
            "color_correction_fixed": False, "color_correction_fixed_value": 50.0,
            "normalize_loudness_fixed": False, "enhande_voice_fixed": False,
            "retouch_fixed": False, "enhance_quality_fixed": False,
            "smooth_slow_motion_fixed": False,
            "fps": {"num": 0, "den": 1},
        },
    }


def make_template_tmp(draft_info):
    """template.tmp = draft_info with canvas width/height set to 0."""
    tmp = json.loads(json.dumps(draft_info))
    tmp["canvas_config"]["width"] = 0
    tmp["canvas_config"]["height"] = 0
    return tmp


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, separators=(",", ":"))


def create_project(name, width=1920, height=1080, fps=30.0):
    check_capcut_closed()

    dst = os.path.join(BASE, name)
    if os.path.exists(dst):
        print(f"ERROR: {dst} already exists", file=sys.stderr)
        sys.exit(1)

    # 3 separate UUIDs matching CapCut's own structure
    project_json_id = gen_uuid()  # Timelines/project.json id
    timeline_id = gen_uuid()      # main_timeline_id = draft_info id = folder name
    draft_id = gen_uuid()         # root_meta_info draft_id = draft_meta_info draft_id

    t_us = now_us()
    t_sec = now_sec()

    machine = get_machine_ids()

    # Directory structure
    tl_dir = os.path.join(dst, "Timelines", timeline_id)
    tl_common = os.path.join(tl_dir, "common_attachment")
    root_common = os.path.join(dst, "common_attachment")
    os.makedirs(tl_common)
    os.makedirs(root_common)

    draft = make_draft_info(timeline_id, width, height, fps, machine)
    draft_json = json.dumps(draft, separators=(",", ":"))
    template_tmp = make_template_tmp(draft)

    # ── Root-level files ──────────────────────────────────────────

    # draft_info.json + .bak
    for fn in ["draft_info.json", "draft_info.json.bak"]:
        with open(os.path.join(dst, fn), "w") as f:
            f.write(draft_json)

    # draft_meta_info.json
    write_json(os.path.join(dst, "draft_meta_info.json"), {
        "cloud_draft_cover": False, "cloud_draft_sync": False,
        "cloud_package_completed_time": "",
        "draft_cloud_capcut_purchase_info": "",
        "draft_cloud_last_action_download": False,
        "draft_cloud_package_type": "",
        "draft_cloud_purchase_info": "",
        "draft_cloud_template_id": "",
        "draft_cloud_tutorial_info": "",
        "draft_cloud_videocut_purchase_info": "",
        "draft_cover": "draft_cover.jpg",
        "draft_deeplink_url": "",
        "draft_enterprise_info": {
            "draft_enterprise_extra": "", "draft_enterprise_id": "",
            "draft_enterprise_name": "", "enterprise_material": [],
        },
        "draft_fold_path": dst,
        "draft_id": draft_id,
        "draft_is_ae_produce": False,
        "draft_is_ai_packaging_used": False,
        "draft_is_ai_shorts": False,
        "draft_is_ai_translate": False,
        "draft_is_article_video_draft": False,
        "draft_is_cloud_temp_draft": False,
        "draft_is_from_deeplink": "false",
        "draft_is_invisible": False,
        "draft_is_pippit_draft": False,
        "draft_is_web_article_video": False,
        "draft_materials": [
            {"type": 0, "value": []}, {"type": 1, "value": []},
            {"type": 2, "value": []}, {"type": 3, "value": []},
            {"type": 6, "value": []}, {"type": 7, "value": []},
            {"type": 8, "value": []},
        ],
        "draft_materials_copied_info": [],
        "draft_name": name,
        "draft_need_rename_folder": False,
        "draft_new_version": "",
        "draft_removable_storage_device": "",
        "draft_root_path": BASE,
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
        "tm_draft_create": t_us,
        "tm_draft_modified": t_us,
        "tm_draft_removed": 0,
        "tm_duration": 0,
    })

    # draft_settings (INI format)
    with open(os.path.join(dst, "draft_settings"), "w") as f:
        f.write(f"[General]\ncloud_last_modify_platform=mac\n"
                f"draft_create_time={t_sec}\n"
                f"draft_last_edit_time={t_sec}\n"
                f"real_edit_keys=1\nreal_edit_seconds=0\n")

    # draft_agency_config.json
    write_json(os.path.join(dst, "draft_agency_config.json"), {
        "is_auto_agency_enabled": False, "is_auto_agency_popup": False,
        "is_single_agency_mode": False, "marterials": None,
        "use_converter": False, "video_resolution": 720,
    })

    # draft_biz_config.json (empty file — 0 bytes)
    open(os.path.join(dst, "draft_biz_config.json"), "w").close()

    # performance_opt_info.json
    write_json(os.path.join(dst, "performance_opt_info.json"), {
        "manual_cancle_precombine_segs": None,
        "need_auto_precombine_segs": None,
    })

    # timeline_layout.json
    write_json(os.path.join(dst, "timeline_layout.json"), {
        "dockItems": [{"dockIndex": 0, "ratio": 1,
                       "timelineIds": [timeline_id],
                       "timelineNames": ["Timeline 01"]}],
        "layoutOrientation": 1,
    })

    # attachment_pc_common.json
    pc_common = {
        "ai_packaging_infos": [],
        "ai_packaging_report_info": {
            "caption_id_list": [], "commercial_material": "",
            "material_source": "", "method": "", "page_from": "",
            "style": "", "task_id": "", "text_style": "",
            "tos_id": "", "video_category": "",
        },
        "broll": {
            "ai_packaging_infos": [],
            "ai_packaging_report_info": {
                "caption_id_list": [], "commercial_material": "",
                "material_source": "", "method": "", "page_from": "",
                "style": "", "task_id": "", "text_style": "",
                "tos_id": "", "video_category": "",
            },
        },
        "commercial_music_category_ids": [], "pc_feature_flag": 0,
        "recognize_tasks": [],
        "reference_lines_config": {
            "horizontal_lines": [], "is_lock": False,
            "is_visible": False, "vertical_lines": [],
        },
        "safe_area_type": 0, "template_item_infos": [],
        "unlock_template_ids": [],
    }
    write_json(os.path.join(dst, "attachment_pc_common.json"), pc_common)

    # common_attachment/attachment_pc_timeline.json
    pc_timeline = {
        "reference_lines_config": {
            "horizontal_lines": [], "is_lock": False,
            "is_visible": False, "vertical_lines": [],
        },
        "safe_area_type": 0,
    }
    write_json(os.path.join(root_common, "attachment_pc_timeline.json"), pc_timeline)

    # template-2.tmp (full draft_info) — 0517 only has this at root, not template.tmp
    with open(os.path.join(dst, "template-2.tmp"), "w") as f:
        f.write(draft_json)

    # ── Timelines/ files ──────────────────────────────────────────

    # Timelines/project.json + .bak
    tl_project = {
        "config": {"color_space": -1, "render_index_track_mode_on": False,
                   "use_float_render": False},
        "create_time": t_us,
        "id": project_json_id,
        "main_timeline_id": timeline_id,
        "timelines": [{"create_time": t_us, "id": timeline_id,
                       "is_marked_delete": False, "name": "Timeline 01",
                       "update_time": t_us}],
        "update_time": t_us,
        "version": 0,
    }
    tl_proj_json = json.dumps(tl_project, separators=(",", ":"))
    for fn in ["project.json", "project.json.bak"]:
        with open(os.path.join(dst, "Timelines", fn), "w") as f:
            f.write(tl_proj_json)

    # Timelines/{UUID}/draft_info.json + .bak
    for fn in ["draft_info.json", "draft_info.json.bak"]:
        with open(os.path.join(tl_dir, fn), "w") as f:
            f.write(draft_json)

    # Timelines/{UUID}/attachment_editing.json
    write_json(os.path.join(tl_dir, "attachment_editing.json"), {
        "editing_draft": {
            "ai_remove_filter_words": {"enter_source": "", "right_id": ""},
            "ai_shorts_info": {"report_params": "", "type": 0},
            "cover_extra_info": {
                "draft_id": "", "position": 0,
                "select_segment_id": "",
                "select_segment_source_start": 0,
                "select_segment_target_start": 0, "type": 1,
            },
            "crop_info_extra": {
                "crop_mirror_type": 0, "crop_rotate": 0.0,
                "crop_rotate_total": 0.0,
            },
            "digital_human_template_to_video_info": {
                "has_upload_material": False, "template_type": 0,
            },
            "draft_used_recommend_function": "",
            "edit_type": 0,
            "eye_correct_enabled_multi_face_time": 0,
            "has_adjusted_render_layer": False,
            "image_ai_chat_info": {
                "before_chat_edit": False, "draft_modify_time": 0,
                "generate_type": "", "keyword_content": "",
                "keyword_type": "", "message_id": "",
                "model_name": "", "need_restore": False,
                "picture_id": "", "prompt_content": "",
                "prompt_from": "", "sugs_info": [],
            },
            "is_open_expand_player": False,
            "is_template_text_ai_generate": False,
            "is_use_adjust": False,
            "is_use_ai_expand": False,
            "is_use_ai_remove": False,
            "is_use_ai_video": False,
            "is_use_audio_separation": False,
            "is_use_chroma_key": False,
            "is_use_curve_speed": False,
            "is_use_digital_human": False,
            "is_use_edit_multi_camera": False,
            "is_use_lip_sync": False,
            "is_use_lock_object": False,
            "is_use_loudness_unify": False,
            "is_use_noise_reduction": False,
            "is_use_one_click_beauty": False,
            "is_use_one_click_ultra_hd": False,
            "is_use_retouch_face": False,
            "is_use_smart_adjust_color": False,
            "is_use_smart_body_beautify": False,
            "is_use_smart_motion": False,
            "is_use_subtitle_recognition": False,
            "is_use_text_to_audio": False,
            "material_edit_session": {
                "material_edit_info": [], "session_id": "", "session_time": 0,
            },
            "paste_segment_list": [],
            "profile_entrance_type": "",
            "publish_enter_from": "",
            "publish_type": "",
            "single_function_type": 0,
            "text_convert_case_types": [],
            "version": "1.0.0",
            "video_recording_create_draft": "",
        },
    })

    # Timelines/{UUID}/attachment_pc_common.json (same as root level)
    write_json(os.path.join(tl_dir, "attachment_pc_common.json"), pc_common)

    # Timelines/{UUID}/common_attachment/ files
    write_json(os.path.join(tl_common, "attachment_action_scene.json"), {
        "action_scene": {"removed_segments": [], "segment_infos": []},
    })

    write_json(os.path.join(tl_common, "attachment_gen_ai_info.json"), {
        "gen_ai": {
            "ai_func_config": {
                "ai_common_configs": [], "ai_effect_configs": [],
                "ai_func_list": [], "aigc_generation_configs": [],
            },
            "cc_agent_info": {
                "agent_stringent_section_id_list": [],
                "agent_stringent_used_tool_list": [],
                "click_cnt": 0, "conversation_ids": [],
                "generate_success_cnt": 0,
                "is_agent_stringent_used": False,
                "is_agent_used": False,
                "request_cnt": 0, "request_from": [],
                "tool_list": [],
            },
            "id": "", "scene": "", "version": "1.0.0",
        },
    })

    write_json(os.path.join(tl_common, "attachment_pc_timeline.json"), pc_timeline)

    write_json(os.path.join(tl_common, "attachment_script_video.json"), {
        "script_video": {
            "attachment_valid": False, "language": "",
            "overdub_recover": [], "overdub_sentence_ids": [],
            "parts": [], "sync_subtitle": False,
            "translate_segments": [], "translate_type": "",
            "version": "1.0.0",
        },
    })

    # Timelines/{UUID}/template.tmp + template-2.tmp
    write_json(os.path.join(tl_dir, "template.tmp"), template_tmp)
    with open(os.path.join(tl_dir, "template-2.tmp"), "w") as f:
        f.write(draft_json)

    # ── Register in root_meta_info.json ───────────────────────────

    meta_path = os.path.join(BASE, "root_meta_info.json")
    shutil.copy2(meta_path, meta_path + ".bak")

    with open(meta_path) as f:
        root_meta = json.load(f)

    root_meta["all_draft_store"].insert(0, {
        "cloud_draft_cover": False,
        "cloud_draft_sync": False,
        "draft_cloud_last_action_download": False,
        "draft_cloud_purchase_info": "",
        "draft_cloud_template_id": "",
        "draft_cloud_tutorial_info": "",
        "draft_cloud_videocut_purchase_info": "",
        "draft_cover": os.path.join(dst, "draft_cover.jpg"),
        "draft_fold_path": dst,
        "draft_id": draft_id,
        "draft_is_ai_shorts": False,
        "draft_is_cloud_temp_draft": False,
        "draft_is_invisible": False,
        "draft_is_web_article_video": False,
        "draft_json_file": os.path.join(dst, "draft_info.json"),
        "draft_name": name,
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
        "tm_draft_create": t_us,
        "tm_draft_modified": t_us,
        "tm_draft_removed": 0,
        "tm_duration": 0,
    })

    if isinstance(root_meta.get("draft_ids"), int):
        root_meta["draft_ids"] += 1

    with open(meta_path, "w") as f:
        json.dump(root_meta, f, separators=(",", ":"))

    print(f"Created: {name}")
    print(f"  Path: {dst}")
    print(f"  Project JSON ID: {project_json_id}")
    print(f"  Timeline ID: {timeline_id}")
    print(f"  Draft ID: {draft_id}")
    print(f"  Canvas: {width}x{height} @ {fps}fps")
    print(f"  Files: {sum(1 for _, _, fs in os.walk(dst) for _ in fs)}")
    print(f"\nCapCut must be CLOSED. Open CapCut to see the project.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a new CapCut project from scratch (no template)")
    parser.add_argument("name", help="Project name")
    parser.add_argument("--width", type=int, default=1920,
                        help="Canvas width (default: 1920)")
    parser.add_argument("--height", type=int, default=1080,
                        help="Canvas height (default: 1080)")
    parser.add_argument("--fps", type=float, default=30.0,
                        help="Frame rate (default: 30)")
    args = parser.parse_args()
    create_project(args.name, args.width, args.height, args.fps)
