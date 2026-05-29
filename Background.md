# GridFrameBench Project Background Skill

## 1. Project Origin

The project originally started from a simple but unusual idea:

> Can an image generation model generate a short video-like sequence by generating a single frame grid image?

The intuition was:

* Instead of generating a video tensor,
* represent multiple temporal frames as cells inside one image canvas,
* and let an image model generate the entire sequence at once.

Initially, the idea was framed as:

> "Using image models to generate videos through frame-grid images."

However, after extensive analysis and multiple rounds of simulated NeurIPS / ICLR / ICML reviewer critiques, it became clear that this framing was scientifically weak.

Several existing works already explored similar ideas:

* Grid Diffusion Models for Text-to-Video Generation
* GRID / GridShow
* GriDiT
* StoryDiffusion
* keyframe interpolation / storyboard generation works

These works already established that:

* temporal sequences can be spatialized into grid layouts,
* image diffusion models can generate image sequences through grid representations,
* grid-as-video is not a new representation.

Therefore, the project underwent a major reframing.

---

# 2. Final Correct Framing

The final project is NOT:

* a new video generation architecture,
* a replacement for video diffusion,
* or a claim that image models can outperform video models.

Instead, the final framing is:

> GridFrameBench studies whether image generators can produce reference-conditioned, stage-controllable, editable motion sheets.

A motion sheet is:

* a grid image,
* where each cell is an explicit temporal anchor,
* corresponding to one stage or sub-stage of an action sequence.

The key insight is:

> The output is not the final video.
> It is a controllable and editable sparse temporal anchor representation before video synthesis.

This project studies:

* stage-to-cell grounding,
* logical continuity,
* reference fidelity,
* temporal ordering,
* local editability,
* and whether spatialized frame sheets help expose and control intermediate action states.

---

# 3. Why This Task Matters

The motivation is NOT:

> "image models should replace video models."

The actual motivation is:

## 3.1 Video models are difficult to control locally

Video diffusion models often produce temporally smooth outputs, but:

* intermediate states are hidden,
* local stage editing is difficult,
* users cannot easily modify one action stage,
* errors are difficult to diagnose.

For example:

* when exactly did the character start drinking?
* did the cup actually reach the mouth?
* which frames are incorrect?
* can Stage 2 be modified without affecting Stage 1/3/4?

GridFrame exposes intermediate stages explicitly.

---

## 3.2 Existing benchmarks do not evaluate editable motion sheets

Benchmarks such as:

* VBench,
* TC-Bench,
* VideoScore,
* T2V-CompBench,

focus on:

* video quality,
* temporal consistency,
* compositionality,
* human preference,
* motion smoothness.

However, they do NOT evaluate:

* grid validity,
* stage-to-cell localization,
* local stage editability,
* non-target cell preservation,
* reference fidelity decay,
* static collapse under reference conditioning,
* motion sheets as sparse temporal anchors.

GridFrameBench fills this gap.

---

## 3.3 Motion sheets are useful for real workflows

GridFrame is positioned as:

* action sheets,
* animation thumbnails,
* storyboard-like motion planning,
* sparse temporal anchors,
* pre-video planning representations.

The intended pipeline is:

Reference image + Stage prompt
→ GridFrame motion sheet
→ keyframe selection
→ interpolation / video refinement
→ final video

Thus:

> GridFrame is not the final video.
> It is a controllable temporal planning representation before video synthesis.

---

# 4. Final Scientific Question

The final scientific question is:

> Can image generators produce reference-conditioned, stage-controllable motion sheets where each cell is an editable temporal unit aligned with explicit action stages?

More specifically:

* Can stage prompts be localized to specific cell ranges?
* Can logical action progression be preserved?
* Can identity remain stable across cells?
* Can users locally edit one stage without breaking unrelated stages?
* Does spatializing time into a grid help action layout and editability?

---

# 5. Important Negative Lessons / Rejected Directions

The project originally explored several directions that were eventually rejected.

## 5.1 "Grid video generation is novel"

Rejected because:

* Grid Diffusion Models,
* GRID,
* GriDiT,
* storyboard generation,
* and keyframe interpolation

already explored grid-based sequence representations.

Therefore:

> Grid representation itself cannot be claimed as novelty.

---

## 5.2 "Image models as world models"

Rejected because:

* reviewers found the claim too weak,
* video models themselves do not strongly justify "world model" narratives,
* open image models are not strong enough,
* and the story became too abstract.

---

## 5.3 "Delta-grid dynamics / temporal residual theory"

Rejected because reviewers argued:

* the math was tautological,
* diffusion predicts noise rather than deterministic motion residuals,
* and the proposed delta accumulation lacked a rigorous theoretical foundation.

The final direction avoids overclaiming dynamics theory.

---

## 5.4 Overly broad scope

The project originally tried to do:

* new representation,
* new architecture,
* new benchmark,
* new temporal theory,
* new world model story,
* video replacement,
* physics consistency.

This was too broad.

The final scope is intentionally narrower:

> benchmark + diagnostic study + controlled baseline.

---

# 6. Final Project Structure

The project now has three core components:

## 6.1 GridFrameBench

A benchmark for:

* reference-conditioned,
* stage-controllable,
* editable motion sheet generation.

The benchmark evaluates:

* stage-to-cell alignment,
* logical continuity,
* reference fidelity,
* editability,
* static collapse,
* and temporal layout quality.

---

## 6.2 GridFrame-STA

A controlled baseline model.

GridFrame-STA is NOT a new foundation architecture.
It is a strong baseline used to test:

* cell-time encoding,
* stage-to-cell routing,
* order-aware training,
* and editability-aware generation.

The key novelty is not IP-Adapter / LoRA / ControlNet themselves,
but explicit stage-token routing into temporal cell regions.

---

## 6.3 Evaluation Protocol

The benchmark introduces metrics for:

* Grid validity,
* Stage localization,
* Logical continuity,
* Action entropy,
* Reference fidelity tracking,
* Static collapse,
* Editability,
* Human calibration.

This evaluation layer is one of the main contributions.

---

# 7. Final Benchmark Protocol

## Standard Protocol

Main benchmark protocol:

* Grid: 4×4
* Total frames: 16
* Stages: 4
* Frames per stage: 4
* Reading order: row-major
* Reference image always enabled

This protocol is chosen because:

* it is realistic for SDXL / FLUX-level models,
* cell resolution remains high enough,
* evaluators remain stable,
* stage boundaries remain interpretable.

---

## Additional Tiers

### Lite Protocol

* 2×4
* 8 frames
* for weaker models.

### Dense Protocol

* 4×6
* 24 frames
* stress test.

### Frontier Protocol

* 5×8
* 40 frames
* future scaling experiments.

This creates a "Temporal Density Scaling" benchmark.

---

# 8. Prompt Philosophy

Prompts should NOT correspond to individual metrics.

Prompts should represent:

* diverse real-world scenarios,
* multi-stage actions,
* interactions,
* trajectories,
* compositions,
* camera patterns,
* physical dynamics.

Metrics evaluate the outputs afterward.

---

# 9. Final Data Philosophy

Benchmark data should be:

* small but high-quality,
* strongly annotated,
* protocol-consistent,
* human-calibrated.

Recommended v1 scale:

* 8–12 scenario categories,
* 50–100 clips per category,
* 500–1000 total samples.

Main experiments should focus on:

* human-object interaction,
* multi-stage tasks,
* fine-grained manipulation.

---

# 10. Final Engineering Philosophy

Do NOT start from huge-scale training.

Instead:

1. build benchmark v0,
2. build evaluators,
3. run zero-shot diagnostics,
4. train simple SDXL LoRA baselines,
5. validate metrics with humans,
6. only then scale models or datasets.

The benchmark and evaluation protocol are more important than training a giant model.
