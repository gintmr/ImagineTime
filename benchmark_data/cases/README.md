# Step 3 Process Specifications

This directory contains the generated Step 3 `process_spec.json` files for the main benchmark construction path.

Generation source:

- Taxonomy: `project_planning/scenario_action_taxonomy.md`
- Expanded action registry: `project_planning/expanded_action_taxonomy.jsonl`
- Batch prompt/spec rules: `prompts/generation/step3_process_spec_batch_prompt.md`
- Generator script: `scripts/generate_step3_process_specs.py`
- Manifest: `benchmark_data/manifests/expanded_actions_step3_manifest.jsonl`

Current generated scale:

- 375 expanded source actions
- 2 variants per action
- 750 total case folders

Each case contains:

```text
benchmark_data/cases/<case_id>/process_spec.json
```

The old legacy prompt and image outputs are not used for this generation pass.

