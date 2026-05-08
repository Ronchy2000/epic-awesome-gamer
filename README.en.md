<div align="center">
  <h1>Epic Weekly Free Games Helper</h1>
  <p>An Epic weekly free-game claimer built around GitHub Actions.</p>

  <p>
    <a href="https://github.com/Ronchy2000/epic-freebies-helper/actions/workflows/epic-gamer.yml"><img src="https://img.shields.io/github/actions/workflow/status/Ronchy2000/epic-freebies-helper/epic-gamer.yml?branch=master&style=flat-square" alt="Workflow Status" /></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.12-blue?style=flat-square" alt="Python" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/github/license/Ronchy2000/epic-freebies-helper?style=flat-square" alt="License" /></a>
    <a href="https://github.com/Ronchy2000/epic-freebies-helper/stargazers"><img src="https://img.shields.io/github/stars/Ronchy2000/epic-freebies-helper?style=flat-square" alt="Stars" /></a>
    <a href="https://visitor-badge.laobi.icu/badge?page_id=Ronchy2000.epic-freebies-helper"><img src="https://visitor-badge.laobi.icu/badge?page_id=Ronchy2000.epic-freebies-helper&left_text=views" alt="Views" /></a>
  </p>
</div>

[🇺🇸 English](README.en.md) | [🇨🇳 中文文档](README.md)

`Epic Weekly Free Games Helper` is built for regular users and runs on GitHub Actions by default. You do not need a private server or a permanently running local machine. If you have a GitHub account, you can configure the workflow and use it directly.

The repository now uses a **protocol-first** provider design. You do not need to reason about every service by model name first. Instead, identify the API protocol family your service belongs to, then pick the matching preset.

## What This Project Does

| Feature | Description |
| --- | --- |
| Auto login | Signs in to Epic automatically |
| Weekly freebie discovery | Finds currently claimable free games |
| Auto claim | Opens product pages and completes checkout |
| Captcha handling | Supports login captcha and checkout security checks |
| Scheduled execution | Runs by GitHub Actions on a schedule |
| Multi-protocol LLM support | Supports both `google_genai` and `openai_compatible` families |

## Two Concepts First

### 1. Protocol family

A protocol family defines the API shape the application talks to.

This repository currently focuses on two families:

| Protocol family | Typical targets |
| --- | --- |
| `google_genai` | Official Gemini API, Gemini relays such as AiHubMix |
| `openai_compatible` | OpenAI, DeepSeek, GLM, Ollama, many local gateways, some third-party platforms |

### 2. preset

A preset is a concrete target configuration under one protocol family, for example:

- `gemini`
- `aihubmix`
- `openai`
- `deepseek`
- `glm`
- `ollama`
- `minimax`
- `xiaomi_mimo`
- `custom_openai_compatible`

So `DeepSeek`, `GLM`, and `Ollama` are not separate protocol families. They are presets inside the `openai_compatible` family.

More detail is available here:

- [Provider configuration guide](docs/providers.en.md)
- [Protocol architecture note](docs/provider-protocol-architecture.md)
- [Protocol migration plan](docs/provider-protocol-migration-plan.md)

## What You Can Choose

| Your situation | Recommended preset | Notes |
| --- | --- | --- |
| I use the official Gemini API | `gemini` | Leave `LLM_BASE_URL` empty |
| I use a Gemini relay such as AiHubMix | `aihubmix` | Still part of `google_genai` |
| I use OpenAI / GPT | `openai` | The model must support image input |
| I use DeepSeek | `deepseek` | Supports thinking and reasoning flags |
| I use Zhipu GLM | `glm` | `glm-4.6v` is recommended |
| I use local Ollama | `ollama` | Uses the official OpenAI-compatible `/v1` surface |
| I use MiniMax | `minimax` | Replace the default with a vision-capable model |
| I use Xiaomi MiMo | `xiaomi_mimo` | Fill the official endpoint and model from your console |
| I use another compatible gateway | `custom_openai_compatible` | Fill your own base URL and model |

## 🚀 Quick Start

### 1. Fork the repository and enable Actions

> [!TIP]
> If you have already forked this repository before, go to your fork on GitHub first and click `Sync fork` -> `Update branch` so your copy matches the latest upstream state before you continue.

After forking, open the `Actions` page in your fork, enter `Epic Awesome Gamer (Scheduled)`, and click `Enable workflow` once. Otherwise GitHub will not activate the scheduled run for that fork.

### 2. Configure the Epic account

Required:

| Secret | Example value |
| --- | --- |
| `EPIC_EMAIL` | your_epic_email@example.com |
| `EPIC_PASSWORD` | your_epic_password |

Prerequisites:

- Epic 2FA must be disabled
- The account must be able to log in in a normal browser

### 3. Configure the LLM route

The new preferred configuration is:

| Secret | Purpose |
| --- | --- |
| `LLM_PRESET` | Select the target service |
| `LLM_API_KEY` | API key |
| `LLM_BASE_URL` | Base URL, or leave empty to use the preset default |
| `LLM_MODEL` | Model name |
| `LLM_THINKING_ENABLED` | Optional |
| `LLM_REASONING_EFFORT` | Optional |

Minimal examples for the most common routes:

**Official Gemini API**

| Secret | Value |
| --- | --- |
| `LLM_PRESET` | `gemini` |
| `LLM_API_KEY` | your Gemini API key |
| `LLM_BASE_URL` | leave empty |
| `LLM_MODEL` | `gemini-2.5-pro` |

**OpenAI / GPT**

| Secret | Value |
| --- | --- |
| `LLM_PRESET` | `openai` |
| `LLM_API_KEY` | your OpenAI API key |
| `LLM_BASE_URL` | `https://api.openai.com/v1` |
| `LLM_MODEL` | `gpt-4.1-mini` |

**DeepSeek**

| Secret | Value |
| --- | --- |
| `LLM_PRESET` | `deepseek` |
| `LLM_API_KEY` | your DeepSeek API key |
| `LLM_BASE_URL` | `https://api.deepseek.com` |
| `LLM_MODEL` | `deepseek-v4-pro` |

**GLM**

| Secret | Value |
| --- | --- |
| `LLM_PRESET` | `glm` |
| `LLM_API_KEY` | your GLM API key |
| `LLM_BASE_URL` | `https://open.bigmodel.cn/api/paas/v4` |
| `LLM_MODEL` | `glm-4.6v` |

**Ollama**

| Secret | Value |
| --- | --- |
| `LLM_PRESET` | `ollama` |
| `LLM_API_KEY` | leave empty |
| `LLM_BASE_URL` | `http://127.0.0.1:11434/v1` |
| `LLM_MODEL` | for example `qwen3-vl:8b` |

For:

- `aihubmix`
- `minimax`
- `xiaomi_mimo`
- `custom_openai_compatible`

see the full examples in [docs/providers.en.md](docs/providers.en.md).

### 4. Trigger one manual run

1. Open `Actions`
2. Select `Epic Awesome Gamer (Scheduled)`
3. Click `Run workflow`

> [!IMPORTANT]
> Do not cancel the run too early just because it is still retrying after a few minutes. Captcha and checkout security checks may fail repeatedly before eventually passing. Some successful runs still take 15 to 20 minutes.

## What The GitHub Actions Logs Show Now

At startup, the workflow logs a runtime summary that includes:

- the active `protocol`
- the active `preset`
- the active `model`
- the active `base_url`
- a masked Epic email such as `du***@example.com`

That makes it much easier to confirm tomorrow's cross-provider tests from the logs alone:

- which protocol route was selected
- whether the model name is the one you intended
- whether your Secrets were mismatched

## Advanced Override Fields

If you do not need separate models for different captcha subtasks, these four fields can usually stay empty:

- `CHALLENGE_CLASSIFIER_MODEL`
- `IMAGE_CLASSIFIER_MODEL`
- `SPATIAL_POINT_REASONER_MODEL`
- `SPATIAL_PATH_REASONER_MODEL`

When left empty, they follow the resolved default model automatically.

## Local One-Shot Debugging

If you want to reproduce the same entrypoint locally:

1. Copy [`.env.example`](.env.example) to `.env`
2. Fill in your own account and model configuration
3. Run `uv sync --group dev`
4. Run `ENABLE_APSCHEDULER=false uv run app/deploy.py`

`.env`, `.venv`, and `app/volumes/` are already ignored by `.gitignore`.

## Troubleshooting And Artifacts

If a run fails, do not rely on a short log excerpt.

Download the artifacts from the bottom of the Actions run page:

| Artifact | Content |
| --- | --- |
| `epic-logs-<run_id>` | runtime logs |
| `epic-runtime-<run_id>` | `promotions.json`, `purchase_debug`, runtime screenshots |
| `epic-screenshots-<run_id>` | extra screenshots for login, auth, and risk-control states |

If you open an issue, upload those zip files whenever possible instead of only pasting a partial console snippet.

## If You Use This Repository As An LLM Learning Project

A good reading order is:

1. start with [docs/providers.en.md](docs/providers.en.md) to understand protocol families and presets
2. then read [docs/provider-protocol-architecture.md](docs/provider-protocol-architecture.md) to understand why the repository no longer adds one provider per model name
3. then inspect `app/settings.py` to see how configuration is normalized into one runtime config
4. then inspect `app/extensions/llm_protocols/` to see how different protocol families are adapted

If you only want the fastest working route, try these first:

1. `glm`
2. `openai`
3. `deepseek`
4. `gemini`

## Important Reminders

- `OpenAI-compatible` does not automatically mean “good enough for captcha solving”
- this is a multimodal captcha workflow, not a plain text-chat application
- the model should support image input and stable structured output
- a local model that is only decent at chat is usually not enough for coordinates, area boxes, and drag reasoning

## Community Thanks

The continuous improvement of this project relies not only on code iterations, but heavily on every user who, upon encountering an error, chose not to give up, but patiently submitted a complete error report.

The resolution of many edge cases did not stem from unilateral developer testing, but was built upon the detailed logs, screenshots, and reproduction steps actively provided by the community. It is this authentic diagnostic data that enabled obscure and hidden issues to be accurately isolated and resolved.

We extend our most genuine gratitude to everyone who has submitted feedback. The time you invested and the real-world data you shared have steadily illuminated the blind spots in development, allowing this project to mature and genuinely benefit a wider audience.

<div align="center">
  <sub>Thank you to everyone who opened issues, uploaded artifacts, and shared real failure cases.</sub>
</div>

<p align="center">
  <a href="https://github.com/AaronL725"><img src="https://github.com/AaronL725.png?size=96" width="64" height="64" alt="@AaronL725" /></a>
  <a href="https://github.com/cita-777"><img src="https://github.com/cita-777.png?size=96" width="64" height="64" alt="@cita-777" /></a>
  <a href="https://github.com/1208nn"><img src="https://github.com/1208nn.png?size=96" width="64" height="64" alt="@1208nn" /></a>
  <a href="https://github.com/LGDhuanghe"><img src="https://github.com/LGDhuanghe.png?size=96" width="64" height="64" alt="@LGDhuanghe" /></a>
  <a href="https://github.com/AdjieC"><img src="https://github.com/AdjieC.png?size=96" width="64" height="64" alt="@AdjieC" /></a>
</p>

<!-- <p align="center">
  <sub>
    <a href="https://github.com/AaronL725"><b>AaronL725</b></a> ·
    <a href="https://github.com/cita-777"><b>cita-777</b></a> ·
    <a href="https://github.com/1208nn"><b>1208nn</b></a> ·
    <a href="https://github.com/LGDhuanghe"><b>LGDhuanghe</b></a> ·
    <a href="https://github.com/AdjieC"><b>AdjieC</b></a>
  </sub>
</p> -->

<!--
Avatar wall template:

<p align="center">
  <a href="https://github.com/<username-1>"><img src="https://github.com/<username-1>.png?size=96" width="64" height="64" alt="@<username-1>" /></a>
  <a href="https://github.com/<username-2>"><img src="https://github.com/<username-2>.png?size=96" width="64" height="64" alt="@<username-2>" /></a>
  <a href="https://github.com/<username-3>"><img src="https://github.com/<username-3>.png?size=96" width="64" height="64" alt="@<username-3>" /></a>
</p>

<p align="center">
  <sub>
    <a href="https://github.com/<username-1>"><b><username-1></b></a> ·
    <a href="https://github.com/<username-2>"><b><username-2></b></a> ·
    <a href="https://github.com/<username-3>"><b><username-3></b></a>
  </sub>
</p>
-->
