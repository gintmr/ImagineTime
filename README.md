<div align="center">

# Can Image Models Imagine Time?

### ImageTime — A Benchmark for Probing Visual World Modeling Through Spatiotemporal Consistency

[Xinrui Wu](https://github.com/gintmr)<sup>1*</sup> &nbsp;·&nbsp; [Lichen Huang](https://github.com/xhghhh)<sup>1*</sup>
<br>
<sup>1</sup>University of Electronic Science and Technology of China &nbsp;·&nbsp; <sup>*</sup>Equal contribution

[![arXiv](https://img.shields.io/badge/arXiv-2606.10620-b31b1b.svg)](https://arxiv.org/abs/2606.10620)
[![Project Page](https://img.shields.io/badge/Project-Page-8257e6.svg)](https://gintmr.github.io/ImagineTime/)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Dataset-ImageTime-yellow.svg)](https://huggingface.co/datasets/Xin-Rui/ImageTime_Benchmark)
[![alphaXiv](https://img.shields.io/badge/alphaXiv-discuss-1f6feb.svg)](https://www.alphaxiv.org/abs/2606.10620)
[![License](https://img.shields.io/badge/Data-CC%20BY--NC%204.0-green.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

<p align="center">
  <img src="assets/Intro.png" alt="ImageTime benchmark overview" width="92%">
</p>

</div>

---

## TL;DR

Image generators now paint stunning single frames — but can they hold a **coherent visual world across multiple states in one picture**? **ImageTime** asks a model to generate a *single image* containing **four ordered key states** of an action, and uses spatiotemporal consistency as a behavioral probe of visual world modeling: does it preserve identities, objects, spatial relations, and **causal order** over time?

> 🔗 **Explore the interactive results at the [project page →](https://gintmr.github.io/ImagineTime/)**

## Highlights

| | |
|---|---|
| 🧩 **750** benchmark cases across **22** domains (**375** action concepts × 2 variants) | 🎬 **4** ordered key states per image: `t₁ initial → t₂ onset → t₃ transition → t₄ final` |
| 🌳 **L0–L6** progressive capability tree (Static → Constraint) | 📊 **C0–C9** capability scores + **D0–D14** diagnostic subscores |
| ⚖️ **GPT-5.5** structured VLM-as-judge with traceable failure labels | 🤖 **8** image models benchmarked under a strict prompt-only protocol |

## The task

Given an action instruction — and optionally a reference image fixing the initial state — a model must produce **one image** laid out as a 2×2 **motion sheet**:

```
┌──────────────┬──────────────┐
│ t₁  initial  │ t₂  onset    │
├──────────────┼──────────────┤
│ t₃ transition│ t₄  final    │
└──────────────┴──────────────┘
```

This four-keyframe protocol is more temporally demanding than single-image generation, while avoiding the confounds of dense video dynamics. It targets five recurring failure modes that single-frame benchmarks cannot catch: **premature final state**, **missing key interaction**, **identity / scene drift**, **object duplication**, and **causal-order violation**.

## Leaderboard (prompt-only)

No reference image, single generation, no retries or human cherry-picking.

| Rank | Model | C mean | D mean | Overall |
|:---:|:---|:---:|:---:|:---:|
| 🏆 1 | GPT Image 2 | 7.86 | 7.87 | **7.86** |
| 2 | Nano Banana 2 | 7.43 | 7.47 | **7.45** |
| 3 | Seedream 5.0 Lite | 7.13 | 7.20 | **7.16** |
| 4 | FLUX.2 Pro | 5.92 | 6.28 | **6.10** |
| 5 | Z-Image-Turbo | 5.14 | 5.69 | **5.41** |
| 6 | Qwen-Image-2512 | 5.09 | 5.55 | **5.32** |
| 7 | HunyuanImage-2.1 | 4.91 | 5.04 | **4.98** |
| 8 | SDXL | 1.49 | 1.64 | **1.57** |

Static scenes are easy; maintaining a **constrained, evolving causal world** is hard — weaker models show clear **upper-tree collapse** at the causal (L5) and constraint (L6) levels. See the [project page](https://gintmr.github.io/ImagineTime/) for radar profiles, per-diagnostic heatmaps, cost trade-offs, and the full qualitative gallery.

## What's in this repository

This repo hosts the lightweight public materials and the source of the project website.

```text
assets/                Intro / overview figure
docs/                  Source for the project website (GitHub Pages)
evaluation_prompt/     VLM-as-judge scoring prompt + C0–C9 ability rubric
  ├── vlm_as_judge_scoring_prompt.md
  └── c0_c9_ability_rubric.md
examples_by_domain/    One representative prompt spec per domain (22 domains)
  └── <domain>/
        ├── standard_process_prompt.md   # the action / process specification
        └── case_id.txt                  # the corresponding benchmark case id
```

The **full benchmark package** lives on Hugging Face Datasets and includes the **750 cases** (process specs, prompts, reference images, 2×2 scaffold templates), **prompt-only generations from all eight models**, the **VLM-as-judge score files**, aggregate leaderboards, and metadata indices.

## Quickstart — get the full dataset

```python
from huggingface_hub import snapshot_download

path = snapshot_download(
    repo_id="Xin-Rui/ImageTime_Benchmark",
    repo_type="dataset",
)
print("Downloaded ImageTime to:", path)
```

Or browse it directly on the [Hugging Face dataset page](https://huggingface.co/datasets/Xin-Rui/ImageTime_Benchmark).

Key metadata files in the release:

| File | Description |
|---|---|
| `metadata/cases.jsonl` | One row per benchmark case |
| `metadata/prompt_only_generations.jsonl` | One row per released generated image |
| `metadata/prompt_only_scores.jsonl` | One flattened score row per generated image |
| `metadata/leaderboard_by_dimension.csv` | Model-level statistics by C/D dimension |
| `metadata/all_scores_long.csv` / `all_scores_wide.csv` | Long- and wide-form score tables |

## How scoring works

Each generated image is scored by a **structured VLM-as-judge (GPT-5.5)** that first validates the 2×2 layout, then parses each cell, then emits scores along two complementary axes plus confidence and failure labels:

- **C0–C9 — capability:** *did the model do it?* Layout, entity consistency, spatial coherence, motion continuity, temporal order, causality, interaction, constraint sensitivity, and overall quality.
- **D0–D14 — diagnostic:** *why did it succeed or fail?* Concrete visual evidence (transition visibility, count conservation, occlusion consistency, …) behind each judgement.

These are mapped onto a seven-level **L0–L6 capability tree** (Static → Identity → Spatial → Object → Interaction → Causal → Constraint), where higher levels depend on the visual promises of lower ones — so you can see *which level a model starts to fail*. The full rubric is in [`evaluation_prompt/c0_c9_ability_rubric.md`](evaluation_prompt/c0_c9_ability_rubric.md) and the judge prompt in [`evaluation_prompt/vlm_as_judge_scoring_prompt.md`](evaluation_prompt/vlm_as_judge_scoring_prompt.md).

## Citation

If you find ImageTime useful, please cite:

```bibtex
@misc{wu2026imagemodelsimaginetime,
      title={Can Image Models Imagine Time? ImageTime: A Novel Benchmark for Probing Visual World Modeling Through Spatiotemporal Consistency},
      author={Xinrui Wu and Lichen Huang},
      year={2026},
      eprint={2606.10620},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2606.10620},
}
```

## License & contact

The benchmark data is released under **[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)** (non-commercial).

Questions and discussion are welcome — open an issue, or reach the authors at
[xinruiwu.wxr@gmail.com](mailto:xinruiwu.wxr@gmail.com) · [xhghlc@gmail.com](mailto:xhghlc@gmail.com).
