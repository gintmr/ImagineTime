# Codex CLI Workflows

This folder contains project-local workflows that use Codex CLI only. It is meant for:

1. Generating images from user-selected prompt files.
2. Scoring input images with project-specific evaluation standards.

No workflow in this folder should call the OpenAI API, OpenAI SDK, image API scripts, or any other non-Codex agent tool directly. The only agent entrypoint is `codex exec`.

## Layout

```text
codex_cli_workflows/
  AGENTS.md
  README.md
  scripts/
    generate_image_from_prompt.sh
    score_image_with_rubric.sh
  outputs/
```

## Prerequisites

Install and authenticate Codex CLI first:

```bash
codex
```

The first run should prompt you to sign in. These scripts assume `codex` is available on `PATH`.

## Generate An Image From A Prompt File

```bash
./codex_cli_workflows/scripts/generate_image_from_prompt.sh \
  benchmark_data/cases/<case_id>/prompts/standard_process_prompt.md
```

Optional output directory:

```bash
./codex_cli_workflows/scripts/generate_image_from_prompt.sh \
  benchmark_data/cases/<case_id>/prompts/standard_process_prompt.md \
  codex_cli_workflows/outputs/my_generation_run
```

The script asks Codex CLI to read the prompt file, invoke image generation through Codex CLI, and save the final image plus a short run note in the output directory.

During execution, Codex CLI may print a live transcript such as `exec ... succeeded` and short `codex` status messages. That is normal. The script is finished only when it prints the final `Codex image-generation run complete...` line.

## Score An Image With A Rubric

```bash
./codex_cli_workflows/scripts/score_image_with_rubric.sh \
  path/to/image.png \
  prompts/judging/c0_c9_ability_rubric.md
```

Optional report path:

```bash
./codex_cli_workflows/scripts/score_image_with_rubric.sh \
  path/to/image.png \
  prompts/judging/c0_c9_ability_rubric.md \
  codex_cli_workflows/outputs/scores/example_score.md
```

The script attaches the image with `--image`, gives Codex the rubric, and writes the final scoring report with `--output-last-message`.

During execution, Codex CLI may print a live transcript. The script is finished only when it prints the final `Codex image-scoring report written to...` line.

## Notes

- Keep prompt files explicit about desired grid size, action stages, reference constraints, and forbidden violations.
- Keep scoring rubrics stable so scores can be compared across images.
- For batch work, call these scripts repeatedly from your own shell loop; the underlying evaluation still goes through Codex CLI.
