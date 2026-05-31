# Codex CLI Workflow Rules

This directory is intentionally CLI-only.

- Use `codex` / `codex exec` for all agent work.
- Do not call OpenAI API clients, SDKs, image API scripts, or custom HTTP clients from this directory.
- Keep reusable workflows as shell scripts that orchestrate Codex CLI.
- Store image-generation prompts as Markdown files.
- Store image-scoring rubrics as Markdown files.
- Store generated reports and image artifacts under `outputs/` unless a caller passes another destination.

