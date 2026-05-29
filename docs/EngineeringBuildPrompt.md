# GridFrameBench Engineering Build Prompt

You are helping build a research benchmark project called:

GridFrameBench

The project studies:

reference-conditioned,
stage-controllable,
editable motion sheet generation.

The benchmark evaluates whether image generators can produce temporally ordered frame-grid motion sheets where:

* each cell is a temporal unit,
* each stage is localized to specific cell ranges,
* identity remains stable,
* logical continuity is preserved,
* local stage editing is possible.

The project is NOT:

* a new video generation architecture,
* a replacement for video diffusion,
* or a claim that grid-as-video is novel.

Instead, it is:

* a benchmark,
* a diagnostic evaluation suite,
* and a controlled baseline study.

---

# Main Benchmark Protocol

Standard protocol:

* Grid: 4×4
* Total frames: 16
* Stages: 4
* Frames per stage: 4
* Reading order: row-major

Additional protocols:

* Lite: 2×4
* Dense: 4×6
* Frontier: 5×8

---

# Required Project Structure

Please design the full project structure.

The repository should contain:

GridFrameBench/
data/
prompts/
metrics/
evaluators/
baselines/
training/
visualization/
scripts/
docs/

---

# Prompt System Design

Implement a structured motion-sheet prompt protocol.

The prompt system should contain:

1. scenarios/
   Defines action stages and logical constraints.

2. layouts/
   Defines grid structures.

3. constraints/
   Defines consistency/editability constraints.

4. prompt_builder/
   Automatically builds prompts from structured configs.

Example scenario:

drink_water.yaml

with:

* 4 stages,
* stage descriptions,
* logical constraints,
* object list,
* evaluator tags.

---

# Prompt Corpus Structure

Organize prompts as a corpus of small text files under `prompts/`.

* `prompts/system/`
  * Size-specific system prompts.
  * Each file only changes the grid geometry and cell count, not the prompt logic.
  * Example sizes now include `4x2`, `4x4`, and `4x6`.

* `prompts/actions/`
  * Action seed prompts and candidate action pools.
  * The flat action pool lives in `prompts/action_candidates_500.txt`.
  * This file is a 500-line list of base scenarios centered on temporal-space consistency, scene/action diversity, and count-sensitive cases.
  * Each line should carry at most one sparse camera or visual cue; such cues must never dominate the pool.

* `prompts/edits/`
  * Local edit instructions.
  * Edit prompts stay separate from action prompts so target edits can be evaluated independently.

The `4x6` system prompt is a separate size variant only; it does not change the action prompt format.

---

# Data Pipeline

Implement:

video clip
→ sample frames
→ build grid image
→ generate metadata.json
→ generate prompt

Support:

* Something-Something-V2
* EPIC-KITCHENS
* future datasets.

---

# Metrics

Implement benchmark metrics:

## Grid Validity

* Grid Count Accuracy
* Boundary Alignment Error
* Cell Occupancy
* Leakage Rate

## Stage-to-Cell

* CSA
* Stage Coverage
* Order Consistency
* Boundary Localization Error

## Logical Continuity

* Transition Validity
* Causal Violation Rate

## Motion

* Action Entropy
* Static Collapse Rate
* Object-centric trajectory metrics

## Reference Fidelity

* similarity decay curve
* identity preservation

## Editability

* target edit success
* non-target preservation
* stage insertion/deletion/timing shift

---

# Evaluator Integration

Reuse existing tools whenever possible.

Please integrate wrappers for:

* VBench
* VideoScore
* Video-Bench
* ViStoryBench metrics
* TC-Bench ideas
* T2V-CompBench evaluators
* Grounding DINO
* SAM2
* CLIP
* Qwen2.5-VL

---

# Baselines

Implement baselines:

## Image baselines

* zero-shot SDXL
* zero-shot FLUX
* LoRA SDXL
* LoRA + reference conditioning
* independent cell generation
* sequential generation

## Grid baselines

* 4×4 grid
* 1×16 strip
* snake order
* shuffled order

## Video baselines

* Stable Video Diffusion
* CogVideoX
* Wan2.1
* segmented video generation
* keyframe interpolation baseline

---

# GridFrame-STA Baseline

Implement:

1. Cell-Time Encoding
2. Soft Stage-to-Cell Routing
3. Order-aware Contrastive Loss
4. Motion Entropy Regularization
5. Reference Fidelity Loss

This is a controlled baseline, NOT a new foundation model.

---

# Core Experiments

Please organize experiment code for:

E1 Benchmark Necessity
E2 Zero-shot Diagnostics
E3 GridFrame-STA Main Results
E4 Grid vs Sequential / Strip / Shuffled / Blocked
E5 Early Denoising Analysis
E6 Logical Continuity vs Visual Smoothness
E7 Editability Study
E8 GridFrame as Sparse Temporal Anchor
E9 Temporal Density Scaling

---

# Important Philosophy

The benchmark is benchmark-first, not model-first.

The main contribution is:

* benchmark,
* evaluation protocol,
* diagnostic analysis.

The model is secondary.

Avoid overclaiming novelty.

Do not claim:

* "new video generation paradigm"
* "replacement for video diffusion"
* "grid-as-video novelty"

The correct framing is:

GridFrameBench studies whether image generators can produce editable, stage-controllable motion sheets where time is spatialized into explicit temporal cells before video synthesis.
