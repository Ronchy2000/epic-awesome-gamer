# GitHub Actions Guide

Language versions:

- [简体中文](README.md)
- English (this page)

The repository already includes [`.github/workflows/epic-gamer.yml`](epic-gamer.yml).

If you only want to get the project running, start with:

- [Main README](../../README.en.md)
- [Provider configuration guide](../../docs/providers.en.md)

This page only adds workflow-specific notes.

## What the Workflow Does

The workflow runs these steps on a GitHub-hosted runner:

1. check out the repository
2. install `uv` and Python 3.12
3. install system dependencies
4. run `uv sync`
5. try to download Camoufox
6. install Playwright Firefox as a fallback
7. run `uv run app/deploy.py` inside `xvfb`

APScheduler inside the repository is disabled in GitHub Actions mode to avoid duplicate scheduling.

## Default Schedule

- default schedule: once every Thursday
- GitHub cron: `20 15 * * 4`
- time: `Thursday 15:20 UTC` / `Thursday 23:20 China Standard Time`

If you want a different time, edit the `schedule` section inside [`.github/workflows/epic-gamer.yml`](epic-gamer.yml).

## Preferred Configuration Style

The new preferred Secrets are:

| Secret | Meaning |
| --- | --- |
| `EPIC_EMAIL` | Epic email |
| `EPIC_PASSWORD` | Epic password |
| `LLM_PRESET` | target service such as `gemini`, `openai`, `deepseek`, `glm`, or `ollama` |
| `LLM_API_KEY` | API key |
| `LLM_BASE_URL` | base URL |
| `LLM_MODEL` | model name |
| `LLM_THINKING_ENABLED` | optional |
| `LLM_REASONING_EFFORT` | optional |

Legacy fields still work:

- `LLM_PROVIDER`
- `GEMINI_*`
- `GLM_*`
- `OPENAI_*`
- `DEEPSEEK_*`

But new setups should prefer `LLM_PRESET + LLM_API_KEY + LLM_BASE_URL + LLM_MODEL`.

For complete preset examples, see [../../docs/providers.en.md](../../docs/providers.en.md).

## What the Logs Show

At startup, the workflow logs a runtime summary that includes:

- the active `protocol`
- the active `preset`
- the active `model`
- the active `base_url`
- the masked Epic email

That lets you confirm from the Actions logs which provider route was actually used.

## Reproducing the Same Entrypoint Locally

To reproduce the same startup path locally:

1. copy [`.env.example`](../../.env.example) to `.env`
2. fill in your own account and model configuration
3. run `uv sync --group dev`
4. run `ENABLE_APSCHEDULER=false uv run app/deploy.py`

## First-Run Reminder

After forking, open the `Actions` page in your fork, enter `Epic Awesome Gamer (Scheduled)`, and click `Enable workflow` once. Otherwise GitHub will not activate the scheduled run for that fork.

> [!IMPORTANT]
> Do not cancel the workflow too early just because it is still retrying after a few minutes. Captcha and checkout security checks may take significantly longer than a normal command-line task. Some successful runs still take 15 to 20 minutes.

## What To Attach When Opening An Issue

Prefer to include:

- the Actions run URL
- `epic-logs-<run_id>.zip`
- `epic-runtime-<run_id>.zip`
- `epic-screenshots-<run_id>.zip`

Do not rely on a tiny pasted console excerpt alone.
