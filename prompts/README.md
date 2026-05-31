# Prompt Assets

This directory stores reusable prompt assets.

## Layout

```text
prompts/
  judging/
    VLM-as-judge rubrics and scoring prompts.

  generation/
    Generation-facing system prompts, templates, and prompt scaffolds.

  legacy/
    Old action prompts and coarse candidate lists kept for coverage analysis and backfilling.
```

## Current Files

- `judging/c0_c9_ability_rubric.md`: current C0-C9 ability taxonomy and judge-oriented rubric.
- `generation/legacy_grid_system/`: old 4x2, 4x4, and 4x6 grid system prompts.
- `legacy/action_candidates_500.txt`: old coarse 500-action list.
- `legacy/actions_500_prompt_files/`: old 502 prompt files generated from the earlier action list.

