#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s IMAGE_FILE RUBRIC_FILE [REPORT_FILE]\n' "$0" >&2
}

if [[ $# -lt 2 || $# -gt 3 ]]; then
  usage
  exit 2
fi

IMAGE_FILE="$1"
RUBRIC_FILE="$2"
REPORT_FILE="${3:-codex_cli_workflows/outputs/scores/$(basename "${IMAGE_FILE%.*}")_score_$(date +%Y%m%d-%H%M%S).md}"

if ! command -v codex >/dev/null 2>&1; then
  printf 'Error: codex CLI was not found on PATH.\n' >&2
  exit 127
fi

if [[ ! -f "$IMAGE_FILE" ]]; then
  printf 'Error: image file not found: %s\n' "$IMAGE_FILE" >&2
  exit 1
fi

if [[ ! -f "$RUBRIC_FILE" ]]; then
  printf 'Error: rubric file not found: %s\n' "$RUBRIC_FILE" >&2
  exit 1
fi

mkdir -p "$(dirname "$REPORT_FILE")"

TASK=$(cat <<EOF
You are evaluating an image for the ImagineTime / GridFrameBench project.

Use Codex CLI multimodal image understanding only. Do not call OpenAI APIs, SDKs, Python image API scripts, curl, or any non-Codex evaluation tool.

The attached image is the evaluation target:
$IMAGE_FILE

Read the scoring rubric from:
$RUBRIC_FILE

Score the image strictly according to the rubric. Return a Markdown report with:
- image path
- rubric path
- overall score
- per-dimension scores
- evidence grounded in visible image details
- severe violations, if any
- short recommendation for improvement

If the image is a grid or motion sheet, inspect each cell or stage separately before giving the final score.
EOF
)

codex --ask-for-approval never exec \
  --cd . \
  --sandbox workspace-write \
  --image "$IMAGE_FILE" \
  --output-last-message "$REPORT_FILE" \
  "$TASK"

printf 'Codex image-scoring report written to: %s\n' "$REPORT_FILE"
