# ImageTime / GridFrameBench 数据构建流程

本文档用于规范整个 benchmark 数据构建流程。目标是把项目从“生成一批 prompt 和图片”升级为一套可追踪、可复现、可审计的数据构造与评测协议。

核心原则：

- 数据构造流程和模型评测流程严格分开。
- Prompt 增强不直接泄露 VLM judge 的具体评分问题或打分规则。
- 每个最终样本都先有结构化过程规格，再生成自然语言 prompt、reference image、2x2 scaffold template 和评测输入。
- 当前主评测只包含三个 setting：Prompt-only、Scaffold-standard、Scaffold-enhanced。
- 第二、第三个 setting 都使用左上角已经固定 reference image 的 2x2 模板；区别只在于使用 standard prompt 还是 enhanced prompt。
- 旧数据只作为历史参考和覆盖查漏来源，不进入新的主数据构建流程。

## 目标数据形态

最终 benchmark 以 case 为单位组织。每个 case 对应一个明确的动作过程，例如“打开抽屉并取出红盒子”。

每个最终 case 应包含：

```text
benchmark_data/cases/<case_id>/
  process_spec.json
  prompts/
    standard_process_prompt.md
    consistency_enhanced_prompt.md
    reference_prompt.md
  references/
    reference.png
    reference_qc.json
  scaffold_templates/
    scaffold_2x2.png
  metadata.json
```

后续模型输出和评测结果不直接混入 case 文件夹，而是按照 setting / model / run 单独存放在：

```text
benchmark_data/generations/
benchmark_data/evaluations/
benchmark_data/manifests/
```

这样可以避免原始 benchmark 数据、模型生成结果和评测结果互相污染。

## Step 1. 定义能力评价体系

目标：定义 benchmark 要诊断的能力维度。

当前能力体系为 C0-C9：

- C0 Layout：布局有效性。
- C1 Reference Grounding：参考状态扎根。
- C2 Entity Consistency：实体一致性。
- C3 Spatial-View Consistency：空间与视角一致性。
- C4 Motion Continuity：运动连续性。
- C5 Temporal Ordering：时序顺序感知。
- C6 Causal Process Consistency：因果过程一致性。
- C7 Interaction Consistency：交互关系一致性。
- C8 Constraint and Counterfactual Sensitivity：约束与反事实敏感性。
- C9 Overall Quality：总体视觉质量。

文件位置：

```text
prompts/judging/c0_c9_ability_rubric.md
```

注意事项：

- C0 是 layout gate。如果图像不是清晰的四帧或不能按顺序阅读，后续时空能力分数应谨慎解释。
- C9 是辅助视觉质量指标，不应混入核心时空一致性主分。
- C8 不一定适用于所有 case，只有包含否定、选择性操作、阻断条件或反事实条件时才启用。

产物：

- 一份稳定的 judge rubric。
- 每个能力维度的定义、核心问题、失败模式。

## Step 2. 构建场景与动作 taxonomy

目标：定义数据覆盖空间，避免动作集合只覆盖少量常见场景。

当前 taxonomy 文件：

```text
project_planning/scenario_action_taxonomy.md
```

每个动作候选应最终标注：

- 一级类别，例如 Household、Kitchen、Sports、Repair。
- 二级类别，例如 container opening、pouring、tool use。
- action phrase。
- expected capability tags，例如 C2、C3、C5、C6。
- difficulty level。
- 是否启用 C8。
- 是否涉及 multi-agent。
- 是否涉及 quantity。
- 是否涉及 occlusion。
- 是否涉及 long-horizon state change。

旧数据位置：

```text
prompts/legacy/
```

旧数据用途：

- 只用于覆盖查漏。
- 不直接进入新的主数据构建流程。
- 不作为最终 benchmark case。

产物：

- 一份动作空间清单。
- 每个动作类别的高难点和禁止性违例。

## Step 3. 构建 Structured Process Specification

目标：把每个动作转成结构化世界状态，而不是直接写 prompt。

这是整个 benchmark 最关键的数据构造步骤。每个 case 都必须先写成 `process_spec.json`，再进入 prompt verbalization。

每个 taxonomy action 应生成两组不同配置：

- `v01`
- `v02`

两组配置的核心动作相同，但主体、场景、物体、颜色、大小、数量、背景物、非目标物、空间布局和相机视角应尽量不同。这样可以避免 benchmark 只测试单一视觉实例，也能增加数量一致性、背景干扰、实体保持和空间关系的诊断力度。

Step 3 批量生成时使用的标准 prompt：

```text
prompts/generation/step3_process_spec_batch_prompt.md
```

推荐 schema：

```json
{
  "case_id": "household_open_drawer_take_red_box_0001",
  "version": "0.1",
  "source_action": "open a drawer and take out a red box",
  "variant_id": "v01",
  "domain": "Household",
  "subcategory": "Object retrieval from container",
  "action": "open a drawer and take out a red box",
  "difficulty": "medium",
  "applicable_settings": [
    "prompt_only",
    "scaffold_standard",
    "scaffold_enhanced"
  ],
  "capability_tags": ["C1", "C2", "C3", "C5", "C6", "C7"],
  "special_flags": {
    "uses_reference": true,
    "constraint_sensitive": false,
    "multi_agent": false,
    "quantity": false,
    "occlusion": true,
    "tool_use": false,
    "state_change": true,
    "gaze_tracking": false
  },
  "diversity_config": {
    "subject_variant": "one adult person wearing a light sweater",
    "scene_variant": "simple bedroom or study room",
    "object_variant": "one small red cardboard box",
    "camera_view": "front-facing stable view",
    "background_distractors": ["one small lamp on top of the drawer"],
    "non_target_objects": [],
    "quantity_configuration": {
      "red_box": 1
    },
    "visual_style": "realistic photo"
  },
  "entities": {
    "subject": {
      "type": "person",
      "description": "one adult person"
    },
    "objects": [
      {
        "name": "red box",
        "role": "target_object",
        "initial_visibility": "hidden_inside_container"
      }
    ],
    "container": {
      "name": "wooden drawer",
      "initial_state": "closed"
    },
    "scene": {
      "description": "simple bedroom or study room",
      "camera_view": "front-facing stable view"
    }
  },
  "initial_state": "The drawer is closed. The red box is inside the drawer and not visible. The person is near the drawer but not yet touching it.",
  "stages": [
    {
      "stage_id": "t1",
      "description": "The person is near the closed drawer. The drawer remains closed and the red box is not visible.",
      "required_visible_state": ["drawer_closed", "person_not_touching_handle"],
      "forbidden_visible_state": ["red_box_visible", "red_box_in_hand", "drawer_open"]
    }
  ],
  "temporal_constraints": [],
  "causal_constraints": [],
  "attention_or_gaze_constraints": [],
  "quantity_constraints": [],
  "forbidden_violations": [],
  "reference_image_requirements": {},
  "notes": ""
}
```

Stage 3 的质量要求：

- 每个 case 必须有明确的 t1-t4。
- 每个 stage 必须写清楚 required visible state 和 forbidden visible state。
- initial state 只能包含动作前状态，不能暴露最终结果。
- 同一个 action 必须有两个视觉和语义配置不同的 variant。
- 如果任务涉及数量、分类、排序、集合变化或多物体操作，必须明确各类物体数量。
- 如果任务涉及主体观察移动目标、追踪目标、接球、看玩具/宠物/车辆移动，应启用 `gaze_tracking` 并写清视线或头部朝向如何从 t1 到 t4 变化。
- temporal constraints 描述顺序。
- causal constraints 描述前提和结果。
- attention_or_gaze_constraints 描述视线、头部朝向、注意目标是否随被观察对象合理移动。
- quantity_constraints 描述各类物体数量如何保持或变化。
- forbidden violations 写给数据构造和后续 judge 用，但不要原样泄露到 generation prompt 中。

产物：

```text
benchmark_data/cases/<case_id>/process_spec.json
```

## Step 4. Prompt Verbalization

目标：从同一个 process specification 生成两种任务 prompt。

### 4.1 Standard Process Prompt

只描述动作过程和四阶段，不额外加入过多一致性提醒。

它测试模型在普通任务描述下能否构思四阶段过程。

### 4.2 Consistency-enhanced Process Prompt

加入通用一致性约束，例如：

- 保持同一人物。
- 保持同一物体。
- 保持同一场景。
- 保持相机视角稳定。
- 按 t1 到 t4 顺序。
- 不要提前出现最终状态。
- 不要复制关键物体。

禁止做法：

- 不要写 “C6 得分规则”。
- 不要写 “judge 会检查 drawer_open before object_in_hand”。
- 不要泄露 VLM judge 的逐项问题。

产物：

```text
benchmark_data/cases/<case_id>/prompts/standard_process_prompt.md
benchmark_data/cases/<case_id>/prompts/consistency_enhanced_prompt.md
```

## Step 5. Reference Prompt Generation

目标：为每个 case 生成 reference image prompt。

Reference prompt 只描述初始状态，不描述后续动作结果。

要求：

- 只展示初始状态。
- 包含关键对象或合理隐藏状态。
- 场景简洁。
- 风格稳定，例如 realistic photo。
- 避免文字、箭头、标签、水印。
- 避免多余人物。
- 指定相机视角。

产物：

```text
benchmark_data/cases/<case_id>/prompts/reference_prompt.md
```

## Step 6. Reference Image Generation And QC

目标：生成 reference image，并过滤不合格 reference。

Reference image 质量会影响后续所有 setting，因此必须 QC。

自动 QC 检查：

- 是否符合 initial state。
- 是否包含必要主体和容器。
- 是否没有提前出现最终状态。
- 是否没有多余干扰物。
- 是否没有文字标签或水印。
- 是否安全、无隐私风险。
- 是否风格稳定。

人工检查策略：

- 全量自动 QC。
- 20% 人工抽检。
- 对失败率高的类别全量人工检查。

产物：

```text
benchmark_data/cases/<case_id>/references/reference.png
benchmark_data/cases/<case_id>/references/reference_qc.json
```

## Step 7. Scaffold Template Construction

目标：构建 2x2 scaffold template，作为第二、第三个主评测 setting 的图像输入。

模板构造流程：

- 先根据 reference prompt 生成每个 case 的 reference image。
- 将所有 reference image 统一缩放到相同分辨率。
- 自动生成 2x2 空白模板。
- 将 reference image 固定放入左上角，也就是 t1 位置。
- 其余三个格子为空白区域，供模型生成 t2、t3、t4。

为什么需要这个模板：

- 它保证所有模型在第二、第三个 setting 中拥有完全一致的 t1 初始状态。
- 它降低模型重新绘制第一帧和保持 reference fidelity 的负担。
- 它让评测更集中于“从固定初始状态展开后续动作阶段”的能力。
- 它与你的任务目标一致：最终输出仍然是单张 2x2 motion sheet，但左上角已经给定。

产物：

```text
benchmark_data/cases/<case_id>/scaffold_templates/scaffold_2x2.png
```

## Step 8. Evaluation Setting Construction

目标：定义模型生成输入。

主要 setting：

| Setting | 输入 | 测试目的 |
|---|---|---|
| Prompt-only | standard process prompt | 测模型仅根据文字 prompt 生成完整 2x2 过程图像的能力 |
| Scaffold-standard | 2x2 scaffold template + same standard process prompt | 测模型在左上角 reference 已固定时，能否根据同样 prompt 生成后续 t2-t4 |
| Scaffold-enhanced | 2x2 scaffold template + consistency-enhanced process prompt | 测增强 prompt 是否能在固定 reference 模板条件下进一步减少时空一致性错误 |

三组 setting 的比较逻辑：

- Scaffold-standard vs Prompt-only：固定 t1 reference 模板是否帮助模型展开后续过程。
- Scaffold-enhanced vs Scaffold-standard：增强一致性约束是否进一步减少失败。

不要把不同 setting 混成一个主分数。应分别报告，并做上述差异分析。

产物：

```text
benchmark_data/manifests/
```

## Step 9. Model Generation

目标：对每个模型、每个 case、每个 setting 生成输出。

建议规范：

- 每个 case 每个 setting 生成 1 张图片。
- 输出格式统一为单张 2x2 image。
- 第二、第三个 setting 的输入必须包含该 case 的 `scaffold_2x2.png`。
- 如果某个模型完全不支持图像输入或模板续写，则只评 Prompt-only，并在 manifest 中记录不支持的 setting。
- 当前主 benchmark 不要求多 seed 或多次采样；每个 case 每个 setting 一张图即可。

输出位置：

```text
benchmark_data/generations/prompt_only/
benchmark_data/generations/scaffold_standard/
benchmark_data/generations/scaffold_enhanced/
```

## Step 10. Structured VLM Evaluation

目标：用 VLM-as-judge 按 C0-C9 评分。

建议两阶段：

### 10.1 Panel / Layout Parsing

先判断：

- 是否四帧。
- 是否能按顺序读。
- 是否每格内容可见。
- scaffold setting 中左上角 t1 是否保留或对应给定 reference。

如果 C0 失败，后续评分应标记为低置信或不可评。

### 10.2 Capability Scoring

根据 C1-C9 输出分数、证据和失败模式。

输出格式建议 JSON + Markdown 双份：

```text
benchmark_data/evaluations/vlm_judge/<model>/<setting>/<case_id>.json
benchmark_data/evaluations/vlm_judge/<model>/<setting>/<case_id>.md
```

## Step 11. Human Calibration

目标：验证 VLM judge 的可靠性。

建议：

- 抽样 100-200 个生成结果。
- 2-3 名人工标注者。
- 按 C0-C8 打分。
- 计算 VLM-human agreement。
- 计算 inter-annotator agreement。

产物：

```text
benchmark_data/evaluations/human_calibration/
```

## Step 12. Dataset Release Manifest

目标：让最终 benchmark 可复现、可审计。

Manifest 至少记录：

- case_id。
- domain / subcategory。
- action。
- capability tags。
- difficulty。
- reference image path。
- scaffold template path。
- prompt paths。
- QC status。
- included settings。
- version。

产物：

```text
benchmark_data/manifests/cases_manifest.jsonl
benchmark_data/manifests/dataset_card.md
```

## 当前下一步

当前项目下一步是 Step 3：批量构建所有 final case 的 `process_spec.json`。

在正式全量生成前，应先审查 2-3 个样例，确认：

- schema 是否足够表达任务。
- stage 描述是否清楚。
- forbidden violations 是否足够具体。
- C8、quantity、occlusion 等 flags 是否设计合理。
- 后续是否容易自动转成 standard / enhanced / reference prompts。
