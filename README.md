# ImagineTime / GridFrameBench Workspace

This repository is organized around one goal: build a benchmark dataset for evaluating whether image generation models can create reference-conditioned, stage-controllable, editable motion sheets.

## Main Modules

```text
codex_cli_workflows/
  Codex CLI-only automation for generating assets and scoring images.

project_planning/
  Human-authored benchmark design, capability taxonomy, scenario taxonomy, and workflow plans.

prompts/
  Prompt assets that are fed to generation models, VLM judges, or Codex CLI workflows.

benchmark_data/
  Generated benchmark data, references, model generations, evaluations, and manifests.

docs/
  Higher-level notes, engineering prompts, methodology drafts, and project status reports.
```

## Current Benchmark Direction

The intended dataset is case-based. Each final case should contain:

- a structured process specification;
- a standard process prompt;
- a consistency-enhanced process prompt;
- an initial-state reference image;
- a 2x2 scaffold template with the reference image fixed in the top-left cell;
- QC records;
- model outputs under each evaluation setting;
- VLM-as-judge scores and optional human calibration scores.

The project intentionally separates data construction from model evaluation. Data assets live in `benchmark_data/`; Codex CLI automation lives in `codex_cli_workflows/`; reusable prompts live in `prompts/`.
