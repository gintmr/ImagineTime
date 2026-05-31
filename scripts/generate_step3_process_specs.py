#!/usr/bin/env python3
"""Generate Step 3 process_spec.json files from the expanded action taxonomy."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_PATH = ROOT / "project_planning" / "scenario_action_taxonomy.md"
CASES_DIR = ROOT / "benchmark_data" / "cases"
MANIFEST_PATH = ROOT / "benchmark_data" / "manifests" / "expanded_actions_step3_manifest.jsonl"
REGISTRY_PATH = ROOT / "project_planning" / "expanded_action_taxonomy.jsonl"


SUPPLEMENTS = {
    ("家居操作 Household", "容器开合"): "打开衣柜门",
    ("家居操作 Household", "拿取与放置"): "把遥控器放回抽屉",
    ("家居操作 Household", "开关控制"): "打开台灯开关",
    ("家居操作 Household", "清洁整理"): "把散落的书放回书架",
    ("厨房 Kitchen", "切割加工"): "切胡萝卜",
    ("厨房 Kitchen", "倒入与混合"): "把鸡蛋液倒入碗中",
    ("厨房 Kitchen", "烹饪状态变化"): "奶酪融化",
    ("厨房 Kitchen", "餐具与容器操作"): "把杯子放进橱柜",
    ("开箱测评 Unboxing", "包装打开"): "打开鞋盒",
    ("开箱测评 Unboxing", "物体展示"): "拿出耳机盒",
    ("开箱测评 Unboxing", "组装与安装"): "安装玩具车轮子",
    ("宠物 Pets", "宠物移动"): "猫从沙发跳到地毯",
    ("宠物 Pets", "宠物取物"): "狗从主人手中接过玩具",
    ("宠物 Pets", "人宠交互"): "人把球扔给狗",
    ("室内移动 Indoor Navigation", "房间巡游"): "从厨房走到餐厅",
    ("室内移动 Indoor Navigation", "接近与到达"): "走向书桌并停下",
    ("户外日常 Outdoor Daily", "路径移动"): "走过公园小路",
    ("户外日常 Outdoor Daily", "环境交互"): "把野餐垫铺在草地上",
    ("运动 Sports", "球类运动"): "守门员扑球",
    ("运动 Sports", "个人运动"): "跳绳",
    ("运动 Sports", "水上/冰雪运动"): "滑雪转弯",
    ("运动 Sports", "团体交互"): "篮球队友挡拆配合",
    ("交通 Motion Systems", "汽车与道路"): "汽车驶入停车位",
    ("交通 Motion Systems", "船与飞行器"): "小船绕过浮标",
    ("交通 Motion Systems", "公共设施"): "电梯到站后乘客走出",
    ("机械/机器人 Machines", "机械臂操作"): "机械臂按下按钮",
    ("机械/机器人 Machines", "工业流水线"): "传送带把箱子送到扫描器下",
    ("机械/机器人 Machines", "家用设备"): "榨汁机开始出果汁",
    ("自然 Nature", "天气与自然现象"): "太阳从云后露出",
    ("自然 Nature", "动植物变化"): "藤蔓沿支架生长",
    ("自然 Nature", "地貌与场景"): "小溪绕过石头流动",
    ("自然 Nature", "物理过程"): "蜡烛融化",
    ("教育/实验 Education & Lab", "实验操作"): "用镊子夹起样本",
    ("教育/实验 Education & Lab", "电路与器材"): "调节显微镜焦距",
    ("建筑/维修 Repair", "工具使用"): "用扳手拧紧螺母",
    ("建筑/维修 Repair", "装配过程"): "安装桌腿",
    ("医疗/护理 Caregiving", "基础护理"): "给病人盖上毯子",
    ("医疗/护理 Caregiving", "药品与器具"): "打开绷带包装",
    ("社交互动 Social", "递交与接收"): "把钥匙递给朋友",
    ("社交互动 Social", "多人协作"): "两人一起搬沙发",
    ("服装/人体 Clothing", "穿戴变化"): "戴上围巾",
    ("服装/人体 Clothing", "姿态与外观"): "整理袖口",
    ("农业/园艺 Gardening", "植物操作"): "把幼苗移入花盆",
    ("农业/园艺 Gardening", "环境整理"): "把花盆排成一行",
    ("游戏 Games", "动作/跑酷"): "角色拾取钥匙后开门",
    ("游戏 Games", "策略/多人"): "角色保护队友撤退",
    ("游戏 Games", "沙盒/建造"): "把三块方块叠成柱子",
    ("动画/卡通 Animation", "人物动作"): "卡通角色追逐气球",
    ("动画/卡通 Animation", "物体交互"): "角色打开魔法书",
    ("动画/卡通 Animation", "叙事片段"): "角色把地图交给同伴",
    ("反事实/规则 Constraints", "选择性操作"): "只按绿色按钮不按红色按钮",
    ("反事实/规则 Constraints", "条件阻断"): "杯盖拧紧所以水倒不出",
    ("反事实/规则 Constraints", "反事实变化"): "如果没有浇水植物保持干燥",
    ("数量/集合 Quantity-focused", "单物体数量"): "从三支笔中拿走一支蓝笔",
    ("数量/集合 Quantity-focused", "多物体数量"): "把四个红积木和三个蓝积木分开放",
    ("数量/集合 Quantity-focused", "群体状态"): "六个瓶子依次被装满前三个",
    ("遮挡/可见性 Occlusion", "进入遮挡"): "玩具车开到沙发下",
    ("遮挡/可见性 Occlusion", "移出遮挡"): "孩子从毯子下拿出玩具",
    ("长程状态 Long-horizon", "缓慢变化"): "咖啡表面的泡沫逐渐消失",
    ("长程状态 Long-horizon", "周期与阶段"): "交通灯从红灯变为绿灯",
}


SUBJECTS = [
    "an adult wearing a gray jacket",
    "a child wearing a yellow hoodie",
    "a kitchen worker wearing an apron",
    "a student with a backpack",
    "a mechanic wearing blue gloves",
    "a shop assistant wearing a dark vest",
    "a nurse in light scrubs",
    "a gardener wearing a sun hat",
]

SCENES = [
    "a simple living room",
    "a compact kitchen counter",
    "a classroom corner",
    "a garage workbench",
    "a tidy bedroom",
    "a small shop interior",
    "a bright clinic room",
    "an outdoor patio",
]

CAMERAS = [
    "front-facing stable view",
    "slight overhead view",
    "three-quarter side view",
    "table-height side view",
    "over-the-shoulder view",
    "wide stable view",
]

DISTRACTORS = [
    ["a small notebook", "a plain ceramic cup"],
    ["two folded towels", "a small basket"],
    ["a potted plant", "a neutral wall shelf"],
    ["a closed toolbox", "a coiled cable"],
    ["a stack of books", "a desk lamp"],
    ["a small tray", "a folded cloth"],
]


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_]+", "_", text.strip())
    text = re.sub(r"_+", "_", text)
    return text[:90].strip("_") or "case"


def domain_slug(domain: str) -> str:
    if " " in domain:
        return slugify(domain.split()[-1])
    return slugify(domain)


def parse_taxonomy() -> list[dict]:
    actions: list[dict] = []
    for line in TAXONOMY_PATH.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "---" in line or "一级类别" in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 4:
            continue
        domain, subcategory, action_cell, risk = parts[:4]
        action_phrases = [a.strip() for a in re.split(r"[、,，]", action_cell) if a.strip()]
        supplement = SUPPLEMENTS.get((domain, subcategory))
        if supplement and supplement not in action_phrases:
            action_phrases.append(supplement)
        for action in action_phrases:
            actions.append(
                {
                    "domain": domain,
                    "subcategory": subcategory,
                    "action": action,
                    "risk": risk,
                    "is_supplement": action == supplement,
                }
            )
    return actions


def infer_flags(action: str, subcategory: str, risk: str) -> dict:
    text = action + subcategory + risk
    quantity = any(k in text for k in ["三", "四", "五", "六", "多个", "数量", "一排", "依次", "两个", "一个", "分类", "分开"])
    occlusion = any(k in text for k in ["遮挡", "箱", "抽屉", "包", "柜", "盒", "门后", "下", "里", "进入", "移出"])
    tool_use = any(k in text for k in ["刀", "剪", "锯", "扳手", "螺丝", "镊子", "工具", "尺子", "听诊器", "滴管"])
    multi_agent = any(k in text for k in ["两人", "多人", "队友", "团队", "朋友", "传", "递", "接收", "协作", "双人"])
    constraint = (
        "Constraints" in subcategory
        or any(k in action + subcategory for k in ["只", "不", "锁", "打不开", "如果", "阻断", "反事实", "保持"])
    )
    gaze = any(k in text for k in ["看", "观察", "接球", "玩具车", "跑向", "移动", "追逐", "递", "传", "飞", "滚", "开到", "走向"])
    return {
        "uses_reference": True,
        "constraint_sensitive": constraint,
        "multi_agent": multi_agent,
        "quantity": quantity,
        "occlusion": occlusion,
        "tool_use": tool_use,
        "state_change": True,
        "gaze_tracking": gaze,
    }


def infer_tags(flags: dict, action: str, subcategory: str) -> list[str]:
    tags = {"C1", "C2", "C3", "C5", "C6"}
    if flags["gaze_tracking"] or flags["multi_agent"] or flags["tool_use"]:
        tags.add("C7")
    if flags["constraint_sensitive"]:
        tags.add("C8")
    if any(k in action + subcategory for k in ["移动", "跑", "走", "飞", "滚", "滑", "跳", "开到", "接近"]):
        tags.add("C4")
    return sorted(tags, key=lambda x: int(x[1:]))


def difficulty(flags: dict, action: str, risk: str) -> str:
    score = sum(1 for k in ["constraint_sensitive", "multi_agent", "quantity", "occlusion", "tool_use", "gaze_tracking"] if flags[k])
    score += 1 if any(k in risk for k in ["不能", "必须", "顺序", "数量", "混乱", "反转"]) else 0
    if score >= 4:
        return "hard"
    if score >= 2:
        return "medium"
    return "easy"


def variant_config(index: int, variant: int, action: str) -> dict:
    offset = index * 2 + variant
    quantity = {}
    if any(k in action for k in ["三", "四", "五", "六", "多个", "分类", "分开", "积木", "杯", "瓶", "苹果", "回形针"]):
        quantity = {
            "primary_count": 3 + (offset % 4),
            "secondary_count": 2 + (offset % 3),
            "count_rule": "all counts must remain visually consistent across t1-t4 unless the action explicitly moves one item",
        }
    return {
        "subject_variant": SUBJECTS[offset % len(SUBJECTS)],
        "scene_variant": SCENES[(offset + 1) % len(SCENES)],
        "object_variant": f"task-specific objects for '{action}' with variant {variant + 1} colors and materials",
        "camera_view": CAMERAS[(offset + 2) % len(CAMERAS)],
        "background_distractors": DISTRACTORS[offset % len(DISTRACTORS)],
        "non_target_objects": [
            f"non-target item {1 + (offset % 3)} that must remain unchanged",
            f"small background object {1 + ((offset + 1) % 4)}",
        ],
        "quantity_configuration": quantity,
        "visual_style": "realistic photo",
    }


def stages_for(action: str, flags: dict, config: dict) -> list[dict]:
    subject = config["subject_variant"]
    cam = config["camera_view"]
    gaze = flags["gaze_tracking"]
    gaze_notes = [
        " The subject looks toward the initial target position.",
        " The subject's gaze begins following the target or active object.",
        " The subject keeps visual attention on the changing target state.",
        " The subject's gaze ends at the final target position rather than the old location.",
    ] if gaze else ["", "", "", ""]
    return [
        {
            "stage_id": "t1",
            "description": f"Initial state before '{action}'. {subject} is present in {config['scene_variant']} with a {cam}. The key objects are visible or correctly hidden according to the initial state.{gaze_notes[0]}",
            "required_visible_state": ["initial_state_visible", "key_entities_present_or_correctly_hidden", "no_final_result_yet"],
            "forbidden_visible_state": ["final_result_visible", "duplicated_key_object", "unexplained_state_change"],
        },
        {
            "stage_id": "t2",
            "description": f"Early action state for '{action}'. The subject begins the required motion or contact, while non-target objects remain unchanged.{gaze_notes[1]}",
            "required_visible_state": ["action_initiated", "causal_contact_or_motion_beginning", "non_target_objects_unchanged"],
            "forbidden_visible_state": ["final_result_completed_too_early", "target_object_teleported", "wrong_object_manipulated"],
        },
        {
            "stage_id": "t3",
            "description": f"Intermediate state for '{action}'. The main transformation is underway and the causal chain is visually inspectable.{gaze_notes[2]}",
            "required_visible_state": ["intermediate_transition_visible", "spatial_relationships_consistent", "object_identity_preserved"],
            "forbidden_visible_state": ["missing_intermediate_step", "object_count_error", "scene_or_subject_identity_change"],
        },
        {
            "stage_id": "t4",
            "description": f"Final state after '{action}'. The intended result is visible, and unchanged objects still match their prior identity and count.{gaze_notes[3]}",
            "required_visible_state": ["final_result_visible", "temporal_order_respected", "unchanged_objects_preserved"],
            "forbidden_visible_state": ["action_order_reversed", "extra_or_missing_key_objects", "target_and_non_target_confused"],
        },
    ]


def make_spec(action_row: dict, index: int, variant: int) -> dict:
    action = action_row["action"]
    flags = infer_flags(action, action_row["subcategory"], action_row["risk"])
    tags = infer_tags(flags, action, action_row["subcategory"])
    config = variant_config(index, variant, action)
    v = f"v{variant + 1:02d}"
    base_slug = f"{domain_slug(action_row['domain'])}_{slugify(action)}_{v}"
    quantity_constraints = []
    if flags["quantity"]:
        quantity_constraints = [
            "All explicitly mentioned object counts must be visually preserved unless the action describes a count-changing operation.",
            "Target and non-target object categories must not be merged, duplicated, recolored, or silently removed.",
        ]
    gaze_constraints = []
    if flags["gaze_tracking"]:
        gaze_constraints = [
            "The subject's head orientation, eye direction, or body attention should follow the active target across t1-t4.",
            "The subject should not keep looking at the old target location after the target has moved.",
        ]
    return {
        "case_id": base_slug,
        "version": "0.1",
        "source_action": action,
        "variant_id": v,
        "domain": action_row["domain"],
        "subcategory": action_row["subcategory"],
        "action": action,
        "difficulty": difficulty(flags, action, action_row["risk"]),
        "applicable_settings": ["prompt_only", "scaffold_standard", "scaffold_enhanced"],
        "capability_tags": tags,
        "special_flags": flags,
        "diversity_config": config,
        "entities": {
            "subject": {
                "type": "person_or_primary_actor",
                "count": 1,
                "description": config["subject_variant"],
            },
            "objects": [
                {
                    "name": "primary target object or state",
                    "role": "target",
                    "description": f"the main object/state involved in '{action}'",
                },
                {
                    "name": "non-target objects",
                    "role": "distractors_or_preserved_objects",
                    "description": ", ".join(config["non_target_objects"]),
                },
            ],
            "scene": {
                "description": config["scene_variant"],
                "camera_view": config["camera_view"],
                "style": config["visual_style"],
            },
        },
        "initial_state": f"Before '{action}', the scene is stable in {config['scene_variant']}. The actor, target object, and non-target objects are in their initial positions. The final result has not happened yet.",
        "stages": stages_for(action, flags, config),
        "temporal_constraints": [
            "t1 must show the initial state before the action.",
            "t2 must show the action beginning or the required causal precondition.",
            "t3 must show an intermediate state rather than jumping directly to the result.",
            "t4 must show the final result after the action.",
        ],
        "causal_constraints": [
            "Visible state changes must occur only after the required contact, motion, tool use, or triggering condition.",
            "The final result must be causally connected to the intermediate state, not appear spontaneously.",
        ],
        "attention_or_gaze_constraints": gaze_constraints,
        "quantity_constraints": quantity_constraints,
        "forbidden_violations": [
            action_row["risk"],
            "Do not change subject identity, target identity, scene layout, or camera viewpoint without a task reason.",
            "Do not duplicate, delete, recolor, or swap key objects unless the action explicitly requires it.",
            "Do not show the final result in t1 or complete the action before its visible preconditions.",
        ],
        "reference_image_requirements": {
            "must_show": ["the initial actor or primary subject", "the initial scene layout", "key objects in their initial state"],
            "must_not_show": ["the final result", "completed action state", "extra text labels", "watermarks"],
            "preferred_view": config["camera_view"],
            "style": "realistic photo, no text, no labels",
        },
        "notes": f"Generated from expanded taxonomy. Supplement action: {action_row['is_supplement']}. This case is variant {v} for diversity.",
    }


def main() -> None:
    actions = parse_taxonomy()
    if CASES_DIR.exists():
        for child in CASES_DIR.iterdir():
            if child.name == ".gitkeep":
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    CASES_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRY_PATH.open("w", encoding="utf-8") as registry, MANIFEST_PATH.open("w", encoding="utf-8") as manifest:
        case_count = 0
        for index, row in enumerate(actions, start=1):
            action_id = f"act_{index:04d}_{domain_slug(row['domain'])}_{slugify(row['action'])}"
            registry_row = {"action_id": action_id, **row}
            registry.write(json.dumps(registry_row, ensure_ascii=False) + "\n")
            for variant in range(2):
                spec = make_spec(row, index, variant)
                case_dir = CASES_DIR / spec["case_id"]
                case_dir.mkdir(parents=True, exist_ok=True)
                spec_path = case_dir / "process_spec.json"
                spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                manifest.write(
                    json.dumps(
                        {
                            "case_id": spec["case_id"],
                            "source_action_id": action_id,
                            "variant_id": spec["variant_id"],
                            "domain": spec["domain"],
                            "subcategory": spec["subcategory"],
                            "action": spec["action"],
                            "path": str(spec_path.relative_to(ROOT)),
                            "capability_tags": spec["capability_tags"],
                            "special_flags": spec["special_flags"],
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
                case_count += 1
    print(json.dumps({"actions": len(actions), "cases": case_count, "registry": str(REGISTRY_PATH), "manifest": str(MANIFEST_PATH)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
