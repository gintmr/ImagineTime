# Benchmark Data

This directory is for benchmark assets and generated data. It should contain data, manifests, QC records, and evaluation outputs rather than reusable prompt templates.

## Target Layout

```text
benchmark_data/
  cases/
    <case_id>/
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

  references/
    images/
    qc_reports/

  scaffold_templates/
    2x2/

  generations/
    prompt_only/
    scaffold_standard/
    scaffold_enhanced/

  evaluations/
    vlm_judge/
    human_calibration/

  manifests/
  pilot/
  optional_extensions/
  legacy_generated_images/
```

## Case Data Contract

Each final case should be traceable from structured specification to prompt versions, reference image, scaffold template, model outputs, and scores.

Minimum required files for a completed case:

- `process_spec.json`
- `prompts/standard_process_prompt.md`
- `prompts/consistency_enhanced_prompt.md`
- `prompts/reference_prompt.md`
- `references/reference.png`
- `references/reference_qc.json`
- `scaffold_templates/scaffold_2x2.png`
- `metadata.json`

## Legacy Data

`legacy_generated_images/grid_4x4_legacy_outputs_20260530/` contains old generated images from the earlier 4x4 prompt workflow. Keep these for inspection, failure-mode mining, and coverage checks, but do not treat them as final benchmark cases.
