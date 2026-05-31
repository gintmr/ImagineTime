#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s PROMPT_FILE [OUTPUT_DIR]\n' "$0" >&2
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 2
fi

PROMPT_FILE="$1"
OUTPUT_DIR="${2:-codex_cli_workflows/outputs/generations/$(date +%Y%m%d-%H%M%S)}"

if ! command -v codex >/dev/null 2>&1; then
  printf 'Error: codex CLI was not found on PATH.\n' >&2
  exit 127
fi

if [[ ! -f "$PROMPT_FILE" ]]; then
  printf 'Error: prompt file not found: %s\n' "$PROMPT_FILE" >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

RUN_NOTE="$OUTPUT_DIR/run_note.md"

TASK=$(cat <<EOF
You are running inside the ImagineTime project.

Use Codex CLI image generation only. Do not call OpenAI APIs, SDKs, Python image API scripts, curl, or any non-Codex image generation tool.

Read this prompt file:
$PROMPT_FILE

Generate the requested image using the image generation capability available through Codex CLI. If the prompt is not already explicit, preserve its intent and make only the minimal clarifications needed for a high-quality result.

Save the final generated image under:
$OUTPUT_DIR

Also write a short Markdown run note under:
$RUN_NOTE

The run note must include:
- source prompt file
- final generation prompt used
- generated image file path
- any assumptions or deviations
EOF
)

codex --ask-for-approval never exec \
  --cd . \
  --sandbox workspace-write \
  --output-last-message "$RUN_NOTE" \
  "$TASK"

printf 'Codex image-generation run complete. See: %s\n' "$OUTPUT_DIR"
