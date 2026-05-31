# Current Project Status

Date: 2026-06-01

## What Exists Now

- C0-C9 capability rubric exists at `prompts/judging/c0_c9_ability_rubric.md`.
- Scenario/action taxonomy exists at `project_planning/scenario_action_taxonomy.md`.
- Codex CLI-only workflow scaffolding exists at `codex_cli_workflows/`.
- Legacy action assets exist at `prompts/legacy/`.
- Legacy generated images exist at `benchmark_data/legacy_generated_images/grid_4x4_legacy_outputs_20260530/`.
- Detailed Chinese data construction protocol exists at `docs/methodology/data_construction_protocol_zh.md`.
- Three Step 3 pilot process specifications exist at `benchmark_data/pilot/step3_process_spec_examples/`.

## Where The Project Is In The 10-Step Workflow

The project has substantially completed early conceptual design, but has not yet produced final benchmark cases.

| Step | Status | Evidence |
|---|---|---|
| 1. Capability Taxonomy Definition | Mostly done | `prompts/judging/c0_c9_ability_rubric.md` defines C0-C9. |
| 2. Scenario Taxonomy Construction | Draft done | `project_planning/scenario_action_taxonomy.md` lists domains, subcategories, actions, and failure points. |
| 3. Structured Process Specification | Pilot examples created, final data not started | Three examples exist under `benchmark_data/pilot/step3_process_spec_examples/`; no final `benchmark_data/cases/<case_id>/process_spec.json` files exist yet. |
| 4. Prompt Verbalization | Prototype only | Legacy action prompts exist, but they are not derived from structured specs. |
| 5. Reference Prompt Generation | Not started as final data | No per-case reference prompts exist under `benchmark_data/cases/`. |
| 6. Reference Image Generation And QC | Not started as final data | No reference images or QC reports exist in `benchmark_data/references/`. |
| 7. Scaffold Template Construction | Designed, not materialized | Each case will need a 2x2 scaffold template with the reference image fixed in the top-left cell. |
| 8. Evaluation Setting Construction | Designed, not materialized | Three main settings are planned: Prompt-only, Scaffold-standard, and Scaffold-enhanced. No manifests yet. |
| 9. Model Generation | Legacy prototype only | 60 legacy generated images exist, but they are not final benchmark outputs. |
| 10. Structured VLM Evaluation | Rubric exists, pipeline not run | Judge rubric exists, but no VLM score outputs exist. |
| 11. Human Calibration | Not started | No human annotation subset or agreement analysis exists. |

## Practical Next Step

The next concrete step is to review the three Step 3 pilot process specifications. If the schema and content style are approved, generate the full set of final `process_spec.json` files under `benchmark_data/cases/`.
