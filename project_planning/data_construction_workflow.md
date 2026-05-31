# Data Construction Workflow

This is the planned benchmark construction pipeline.

## 1. Capability Taxonomy Definition

Define C0-C9 diagnostic dimensions for layout validity, reference grounding, entity consistency, spatial-view consistency, motion continuity, temporal ordering, causal process consistency, interaction consistency, constraint sensitivity, and overall visual quality.

## 2. Scenario Taxonomy Construction

Define process-oriented domains and action categories. Each action should eventually include category, subcategory, action phrase, expected capability tags, difficulty level, and flags for special conditions such as constraint sensitivity, multi-agent interaction, quantity, or occlusion.

## 3. Structured Process Specification

Convert each selected action into a structured process specification before writing natural-language prompts.

For each taxonomy action, create two variants (`v01` and `v02`). The variants share the same core action but differ in subject, scene, camera view, object appearance, non-target objects, background distractors, and quantity configuration where appropriate. This increases visual diversity and supports stronger tests of entity consistency, quantity consistency, spatial relations, and attention/gaze tracking.

Recommended fields:

```json
{
  "case_id": "open_drawer_take_red_box_0001",
  "action": "open a drawer and take out a red box",
  "subject": "a person",
  "main_object": "a red box",
  "container": "a wooden drawer",
  "initial_state": "drawer closed; red box inside and not visible",
  "t1": "drawer closed; hand outside",
  "t2": "hand touches drawer handle",
  "t3": "drawer open; red box visible inside",
  "t4": "red box in hand outside drawer",
  "temporal_constraints": [
    "hand touches handle before drawer opens",
    "drawer opens before red box appears in hand"
  ],
  "forbidden_violations": [
    "red box in hand before drawer opens",
    "drawer opens without contact",
    "red box duplicated"
  ],
  "capability_tags": ["C1", "C2", "C3", "C5", "C6", "C7"]
}
```

## 4. Prompt Verbalization

Generate two prompt versions from the same process specification:

- Standard Process Prompt: describes the action process and ordered stages.
- Consistency-enhanced Process Prompt: adds general consistency constraints without leaking VLM judge questions or scoring rules.

## 5. Reference Prompt Generation

Generate an initial-state reference prompt for each case. The reference prompt should show only the initial state, keep the scene simple, avoid text labels, and avoid revealing future action outcomes.

## 6. Reference Image Generation And QC

Generate reference images from initial-state prompts. Then run:

- automatic VLM QC for initial-state correctness, object presence, absence of final state leakage, clutter, and style consistency;
- manual inspection for ambiguous or failed cases.

## 7. Evaluation Setting Construction

Build the main evaluation settings:

- Prompt-only Setting;
- Scaffold-standard Setting;
- Scaffold-enhanced Setting.

The second and third settings use a 2x2 scaffold template whose top-left cell is fixed to the reference image. The difference is that Scaffold-standard uses the standard process prompt, while Scaffold-enhanced uses the consistency-enhanced prompt.

## 8. Model Generation

Query each image generation model under standardized settings. Keep outputs separated by setting and model.

Each case should produce one image per supported setting. Multi-seed sampling is not part of the current main benchmark protocol.

## 9. Structured VLM Evaluation

Run VLM-as-judge in two stages:

- panel/layout parsing;
- C0-C9 capability scoring with evidence and failure modes.

## 10. Human Calibration

Validate the VLM judge on a manually annotated subset and report agreement at dimension and sample levels.
