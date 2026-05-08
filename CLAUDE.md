# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

`AGENTS.md` is the canonical repo guide. Claude-oriented tools should follow it as well.

## Read These First For Provider Work

- `AGENTS.md`
- `docs/provider-protocol-architecture.md`
- `docs/provider-protocol-migration-plan.md`

## Project Overview

Epic 免费人 (Epic Awesome Gamer) automates Epic weekly free-game claims with Playwright and `hcaptcha-challenger`.

Core files:

- `app/settings.py`
- `app/extensions/llm_adapter.py`
- `app/services/epic_games_service.py`
- `app/services/epic_authorization_service.py`
- `app/jobs.py`
- `app/deploy.py`

## Commands

```bash
uv sync
uv sync --group dev
uv run black . -C -l 100
uv run ruff check --fix
```

## Testing

Test execution is not allowed.

Use linting, static inspection, and targeted non-test verification instead.

## Protocol-First Rules

- Add support by **protocol family**, not by vendor/model name.
- Phase-1 protocol families are `google_genai` and `openai_compatible`.
- Treat `openai`, `deepseek`, `glm`, `minimax`, `ollama`, and similar targets as presets unless official docs require a new protocol.
- Support Ollama through its OpenAI-compatible `/v1` path first.
- Keep provider logic in config/adapter modules, not in business flow.
- Reuse validated work from `add-openai-provider` and `add-deepseekv4-provider`.
- Do not delete or overwrite existing branch work while preparing the unified architecture.

## Maintenance Log

Any change that affects runtime behavior, bug handling, troubleshooting flow, user-facing guidance, or expected outcomes must append a new entry to `docs/maintenance-log.md`.
