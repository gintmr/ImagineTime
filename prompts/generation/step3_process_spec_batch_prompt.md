# Step 3 批量生成 Structured Process Specification 的 Codex Prompt

用途：把动作 taxonomy 中的动作批量转成最终 benchmark 的 `process_spec.json`。这个 prompt 只用于 Step 3，不生成自然语言 generation prompt，不生成 reference image，不生成 scaffold template。

## 角色

你是 ImageTime / GridFrameBench 的 benchmark 数据构造助手。你的任务是把动作列表中的每个 action 转换成结构化过程规格。每个 action 必须生成两组不同配置，也就是两个不同 case。两个 case 的核心动作相同，但主体、场景、物体、数量、背景、相机视角、非目标物和细节配置应不同，以增加 benchmark 多样性。

## 输入

你会收到：

1. 一个或多个动作条目，每个条目可能包含：
   - domain
   - subcategory
   - action phrase
   - high-risk failure points
   - expected capability tags
2. C0-C9 能力体系摘要。
3. 本 prompt。

## 输出

为每个 action 输出两个 `process_spec.json`，命名规则：

```text
<domain_slug>_<action_slug>_v01/process_spec.json
<domain_slug>_<action_slug>_v02/process_spec.json
```

两个版本必须动作相同，但配置不同。

例如动作是 “open a door”：

- v01 可以是成人在公寓走廊打开白色木门，正面视角。
- v02 可以是孩子在教室里打开蓝色半玻璃门，三分之二侧面视角。

## 主评测 setting

每个 case 的 `applicable_settings` 固定为：

```json
[
  "prompt_only",
  "scaffold_standard",
  "scaffold_enhanced"
]
```

含义：

- `prompt_only`: 只用 standard process prompt 让模型生成完整 2x2 图片。
- `scaffold_standard`: 用同一个 standard process prompt + 左上角固定 reference image 的 2x2 scaffold template，让模型补全/生成 t2-t4。
- `scaffold_enhanced`: 用 consistency-enhanced prompt + 左上角固定 reference image 的 2x2 scaffold template，让模型补全/生成 t2-t4。

## 每个 JSON 必须包含的字段

```json
{
  "case_id": "",
  "version": "0.1",
  "source_action": "",
  "variant_id": "v01",
  "domain": "",
  "subcategory": "",
  "action": "",
  "difficulty": "easy|medium|hard",
  "applicable_settings": [
    "prompt_only",
    "scaffold_standard",
    "scaffold_enhanced"
  ],
  "capability_tags": [],
  "special_flags": {
    "uses_reference": true,
    "constraint_sensitive": false,
    "multi_agent": false,
    "quantity": false,
    "occlusion": false,
    "tool_use": false,
    "state_change": true,
    "gaze_tracking": false
  },
  "diversity_config": {
    "subject_variant": "",
    "scene_variant": "",
    "object_variant": "",
    "camera_view": "",
    "background_distractors": [],
    "non_target_objects": [],
    "quantity_configuration": {},
    "visual_style": "realistic photo"
  },
  "entities": {},
  "initial_state": "",
  "stages": [],
  "temporal_constraints": [],
  "causal_constraints": [],
  "attention_or_gaze_constraints": [],
  "quantity_constraints": [],
  "forbidden_violations": [],
  "reference_image_requirements": {},
  "notes": ""
}
```

## 两组配置的多样性要求

对同一个 action 的 v01 和 v02，至少改变下列 4 类内容：

- 主体：年龄、职业、服装、姿态、手部使用方式。
- 场景：房间类型、户外/室内、工作台、厨房、教室、车库等。
- 关键物体：颜色、材质、大小、形状、容器类型。
- 相机视角：正面、轻微俯视、三分之二侧面、桌面高度、肩后视角等。
- 背景/非主体物体：增加少量不干扰任务的非目标物。
- 数量配置：目标物、非目标物或类别数量不同。
- 空间布局：目标位于左/右/前/后、容器内/外、近/远。

不要让两组配置只是换一个颜色。它们必须在视觉上和评测属性上都有实际差异。

## 数量相关任务要求

如果 action 主要评测数量一致性、分类、排序、集合变化或多物体操作，必须明确写出数量。

示例：

```json
"quantity_configuration": {
  "red_paperclips": 5,
  "blue_paperclips": 3,
  "yellow_paperclips": 4,
  "target_action": "sort by color into three groups"
}
```

必须写清：

- 每类物体是什么。
- 每类有几个。
- 哪些被操作，哪些不应被操作。
- 数量在 t1-t4 中如何变化或保持。
- 禁止复制、消失、颜色互换、类别混淆。

## 视线 / 注意方向追踪要求

如果 action 涉及一个主体观察、追踪、等待、接球、看宠物移动、看车辆移动、看玩具移动、看他人递物等情况，应启用：

```json
"gaze_tracking": true
```

并填写：

```json
"attention_or_gaze_constraints": [
  "The child's gaze follows the toy car from the lower-left area in t1 toward the lower-right area in t4.",
  "The head orientation and eye direction should change gradually with the moving target.",
  "The subject should not keep looking at the old location after the target has moved."
]
```

在每个 stage 里也要写清楚主体大致看向哪里。例如：

- t1: child looks toward the toy car near the lower-left area.
- t2: child turns gaze slightly right as the toy car moves.
- t3: child continues tracking the car near the center-right area.
- t4: child looks toward the toy car near the lower-right area.

这类能力主要标记为 C7，也可同时标记 C3 和 C4。

## Stage 写法要求

每个 case 必须有四个 stage：

- `t1`: 初始状态。必须能作为 reference image 的内容。
- `t2`: 动作前提或早期变化。
- `t3`: 中间状态或关键因果状态。
- `t4`: 结果状态。

每个 stage 必须包含：

```json
{
  "stage_id": "t1",
  "description": "",
  "required_visible_state": [],
  "forbidden_visible_state": []
}
```

Stage 描述必须是视觉可检查的。不要写抽象心理状态，除非它能通过视线、姿态、方向、接触关系等被观察。

## Reference image 要求

`reference_image_requirements` 只描述 t1 初始状态。

必须包含：

```json
{
  "must_show": [],
  "must_not_show": [],
  "preferred_view": "",
  "style": "realistic photo, no text, no labels"
}
```

reference image 不允许提前暴露 t2-t4 的结果。

## 生成质量要求

- 不要复用旧数据中的粗糙 prompt。
- 不要直接输出自然语言 generation prompt。
- 不要生成图片。
- 不要把 VLM judge 的逐项评分问题泄露到 generation-facing 字段。
- JSON 必须合法，可被 `python3 -m json.tool` 解析。
- 每个 case 都要有足够具体的物体、数量、空间位置和禁止违例。

## 最终输出格式

如果在对话中输出，按 case 分块给出 JSON。

如果在文件系统中生成，创建：

```text
benchmark_data/cases/<case_id>/process_spec.json
```

每个 action 必须生成两个 case：`v01` 和 `v02`。

