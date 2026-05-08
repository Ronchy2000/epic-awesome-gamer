<div align="center">
  <h1>Epic 周免游戏领取助手</h1>
  <p>一个基于 GitHub Actions 的 Epic 周免自动领取工具。</p>

  <p>
    <a href="https://github.com/Ronchy2000/epic-freebies-helper/actions/workflows/epic-gamer.yml"><img src="https://img.shields.io/github/actions/workflow/status/Ronchy2000/epic-freebies-helper/epic-gamer.yml?branch=master&style=flat-square" alt="Workflow Status" /></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.12-blue?style=flat-square" alt="Python" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/github/license/Ronchy2000/epic-freebies-helper?style=flat-square" alt="License" /></a>
    <a href="https://github.com/Ronchy2000/epic-freebies-helper/stargazers"><img src="https://img.shields.io/github/stars/Ronchy2000/epic-freebies-helper?style=flat-square" alt="Stars" /></a>
    <a href="https://visitor-badge.laobi.icu/badge?page_id=Ronchy2000.epic-freebies-helper"><img src="https://visitor-badge.laobi.icu/badge?page_id=Ronchy2000.epic-freebies-helper&left_text=views" alt="Views" /></a>
  </p>
</div>

[🇨🇳 中文文档](README.md) | [🇺🇸 English](README.en.md)

`Epic 周免游戏领取助手` 面向普通用户，默认运行在 GitHub Actions 上。你不需要自建服务器，也不需要本地常驻环境；只要有 GitHub 账号，就可以按文档完成自动领取配置。

这个仓库现在采用 **protocol-first** 的 provider 设计。你不需要按模型名理解所有接入方式，只要先知道自己手上的服务属于哪类 API 协议，再选择对应 preset 即可。

## 这个项目能做什么

| 功能 | 说明 |
| --- | --- |
| 自动登录 | 自动完成 Epic 账号登录 |
| 自动发现周免 | 拉取并识别当周可领取游戏 |
| 自动领取 | 自动进入商品页并完成结账流程 |
| 验证码处理 | 支持登录验证码和 checkout 二次安全校验 |
| 定时执行 | 默认通过 GitHub Actions 定时运行 |
| 多协议 LLM 接入 | 支持 `google_genai` 与 `openai_compatible` 两大协议家族 |

## 先理解两个概念

### 1. 协议家族

协议家族决定“程序怎么调用模型服务”。

本仓库当前主要有两类：

| 协议家族 | 典型对象 |
| --- | --- |
| `google_genai` | Gemini 官方接口、AiHubMix 这类 Gemini 中转 |
| `openai_compatible` | OpenAI、DeepSeek、GLM、Ollama、很多本地网关、部分第三方平台 |

### 2. preset

preset 是具体目标服务的默认配置包，例如：

- `gemini`
- `aihubmix`
- `openai`
- `deepseek`
- `glm`
- `ollama`
- `minimax`
- `xiaomi_mimo`
- `custom_openai_compatible`

也就是说，`DeepSeek`、`GLM`、`Ollama` 并不是新的协议家族，而是 `openai_compatible` 家族下的不同 preset。

更详细的解释、官方文档入口和配置示例，请看：

- [Provider 配置说明](docs/providers.md)
- [Protocol 架构说明](docs/provider-protocol-architecture.md)
- [Protocol 迁移计划](docs/provider-protocol-migration-plan.md)

## 你可以怎么选

| 你的情况 | 推荐 preset | 备注 |
| --- | --- | --- |
| 我用 Gemini 官方接口 | `gemini` | `LLM_BASE_URL` 留空 |
| 我用 AiHubMix 这类 Gemini 中转 | `aihubmix` | 仍属于 `google_genai` |
| 我用 OpenAI / GPT | `openai` | 模型必须支持图片输入 |
| 我用 DeepSeek | `deepseek` | 支持 thinking / reasoning 参数 |
| 我用智谱 GLM | `glm` | 推荐 `glm-4.6v` |
| 我用本地 Ollama | `ollama` | 走官方 OpenAI-compatible `/v1` |
| 我用 MiniMax | `minimax` | 你需要改成支持图片输入的模型 |
| 我用 Xiaomi MiMo | `xiaomi_mimo` | 从你自己的控制台填写官方 endpoint / model |
| 我用别的兼容网关 | `custom_openai_compatible` | 自填 base URL 与 model |

## 🚀 快速开始

### 1. Fork 并启用 Actions

> [!TIP]
> 如果你已经 Fork 过这个仓库，建议先在 GitHub 网页里进入自己的仓库，点击 `Sync fork` -> `Update branch`，先同步到最新版本再继续配置。

Fork 后先打开你自己仓库的 `Actions` 页面，进入 `Epic Awesome Gamer (Scheduled)`，点击一次 `Enable workflow`。否则 GitHub 不会为这个 Fork 启用定时 `schedule`。

### 2. 配置 Epic 账号

必须配置：

| Secret | 示例值 |
| --- | --- |
| `EPIC_EMAIL` | your_epic_email@example.com |
| `EPIC_PASSWORD` | your_epic_password |

前提要求：

- Epic 账号必须关闭 2FA
- 能正常在浏览器里登录 Epic

### 3. 配置 LLM

新版本推荐优先使用 canonical 配置：

| Secret | 作用 |
| --- | --- |
| `LLM_PRESET` | 选择服务 |
| `LLM_API_KEY` | API key |
| `LLM_BASE_URL` | base URL，可留空走默认值 |
| `LLM_MODEL` | 模型名 |
| `LLM_THINKING_ENABLED` | 可选 |
| `LLM_REASONING_EFFORT` | 可选 |

最常见的几种最小配置示例：

**Gemini 官方接口**

| Secret | 值 |
| --- | --- |
| `LLM_PRESET` | `gemini` |
| `LLM_API_KEY` | 你的 Gemini API key |
| `LLM_BASE_URL` | 留空 |
| `LLM_MODEL` | `gemini-2.5-pro` |

**OpenAI / GPT**

| Secret | 值 |
| --- | --- |
| `LLM_PRESET` | `openai` |
| `LLM_API_KEY` | 你的 OpenAI API key |
| `LLM_BASE_URL` | `https://api.openai.com/v1` |
| `LLM_MODEL` | `gpt-4.1-mini` |

**DeepSeek**

| Secret | 值 |
| --- | --- |
| `LLM_PRESET` | `deepseek` |
| `LLM_API_KEY` | 你的 DeepSeek API key |
| `LLM_BASE_URL` | `https://api.deepseek.com` |
| `LLM_MODEL` | `deepseek-v4-pro` |

**GLM**

| Secret | 值 |
| --- | --- |
| `LLM_PRESET` | `glm` |
| `LLM_API_KEY` | 你的智谱 API key |
| `LLM_BASE_URL` | `https://open.bigmodel.cn/api/paas/v4` |
| `LLM_MODEL` | `glm-4.6v` |

**Ollama**

| Secret | 值 |
| --- | --- |
| `LLM_PRESET` | `ollama` |
| `LLM_API_KEY` | 留空 |
| `LLM_BASE_URL` | `http://127.0.0.1:11434/v1` |
| `LLM_MODEL` | 例如 `qwen3-vl:8b` |

如果你要配：

- `aihubmix`
- `minimax`
- `xiaomi_mimo`
- `custom_openai_compatible`

请直接看 [docs/providers.md](docs/providers.md) 里的完整示例。

### 4. 手动运行一次

1. 打开 `Actions`
2. 选择 `Epic Awesome Gamer (Scheduled)`
3. 点击 `Run workflow`

> [!IMPORTANT]
> 不要因为它运行了几分钟还在重试就提前取消。验证码与 checkout 二次校验可能会反复失败又重试，有些最终成功的运行会持续 15 到 20 分钟。

## GitHub Actions 日志现在会显示什么

启动时会输出一段 runtime summary，包含：

- 当前 `protocol`
- 当前 `preset`
- 当前 `model`
- 当前 `base_url`
- 脱敏后的 Epic 邮箱，例如 `du***@example.com`

这样你明天测试不同平台时，可以直接从日志里确认：

- 到底走的是哪条协议路径
- 模型名是不是你配置的那个
- 是不是把 Secrets 配错了

## 高级覆盖项

如果你不需要把不同验证码步骤拆给不同模型，下面四个字段通常都可以留空：

- `CHALLENGE_CLASSIFIER_MODEL`
- `IMAGE_CLASSIFIER_MODEL`
- `SPATIAL_POINT_REASONER_MODEL`
- `SPATIAL_PATH_REASONER_MODEL`

留空时，它们会自动跟随当前解析出的默认模型，也就是 `LLM_MODEL` 或 preset 对应的默认模型。

## 本地单次调试

如果你想在本地复现同一个入口流程：

1. 复制 [`.env.example`](.env.example) 为 `.env`
2. 填入自己的账号和模型配置
3. 执行 `uv sync --group dev`
4. 执行 `ENABLE_APSCHEDULER=false uv run app/deploy.py`

`.env`、`.venv`、`app/volumes/` 都已经在 `.gitignore` 里，不会被误提交。

## 问题排查与 Artifact

如果运行失败，不要只看一小段日志。

优先下载 Actions 页面底部的 artifact：

| Artifact | 内容 |
| --- | --- |
| `epic-logs-<run_id>` | 运行日志 |
| `epic-runtime-<run_id>` | `promotions.json`、`purchase_debug`、运行时截图 |
| `epic-screenshots-<run_id>` | 登录、风控、授权等额外截图 |

如果要提 issue，最好同时上传这些 zip，而不是只粘贴控制台片段。

## 如果你把这个项目当作 LLM 入门样例

建议按这个顺序理解：

1. 先看 [docs/providers.md](docs/providers.md)，理解 `protocol family` 和 `preset`
2. 再看 [docs/provider-protocol-architecture.md](docs/provider-protocol-architecture.md)，理解为什么不再按模型名逐个写 provider
3. 再看 `app/settings.py`，理解配置是怎么被解析成统一 runtime config 的
4. 再看 `app/extensions/llm_protocols/`，理解不同协议家族的适配方式

如果你只是想最快跑起来，优先尝试：

1. `glm`
2. `openai`
3. `deepseek`
4. `gemini`

## 常见提醒

- `OpenAI-compatible` 不等于“一定能稳定跑验证码”
- 本项目是多模态验证码链路，不是普通文本问答
- 模型必须尽量支持图片输入和稳定结构化输出
- 本地模型如果只会聊天、不擅长坐标/框选/拖拽推理，实际效果通常不会好

## 社区致谢

本项目的持续完善，离不开每一位在遇到报错时没有选择放弃，而是耐心回传完整错误现场的使用者。

许多边界情况的修复，并非源自开发者的独自排查，而是建立在大家主动提供的详实日志、截图与复现步骤之上。正是这些真实的报错数据，让各种隐蔽的问题得以被精准定位并解决。

在此，向所有提供过反馈的用户致以由衷的感谢。是你们投入的时间与提供的测试数据，逐步扫除了开发过程中的盲区，让这个项目日益稳定，切实帮助到了更多人。

<div align="center">
  <sub>感谢每一位提过 issue、上传过 artifact、留下过真实失败案例的朋友。</sub>
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
