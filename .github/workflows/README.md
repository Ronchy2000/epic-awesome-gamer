# GitHub Actions 使用说明

语言版本：

- 简体中文（当前页）
- [English](README.en.md)

当前仓库已经内置 [`.github/workflows/epic-gamer.yml`](epic-gamer.yml)。

如果你只是想把仓库跑起来，建议先看：

- [主 README](../../README.md)
- [Provider 配置说明](../../docs/providers.md)

这份文档只补充 workflow 层面的运行信息。

## 工作流做了什么

这个工作流会在 GitHub Hosted Runner 上完成以下步骤：

1. 检出仓库代码
2. 安装 `uv` 和 Python 3.12
3. 安装系统依赖
4. 执行 `uv sync`
5. 尝试下载 Camoufox
6. 安装 Playwright Firefox 作为回退方案
7. 在 `xvfb` 中运行 `uv run app/deploy.py`

仓库内的 APScheduler 在 GitHub Actions 模式下会关闭，避免重复调度。

## 默认运行时间

- 默认 schedule：每周四一次
- GitHub cron：`20 15 * * 4`
- 对应时间：`UTC 周四 15:20` / `北京时间周四 23:20`

如果你想改时间，直接修改 [`.github/workflows/epic-gamer.yml`](epic-gamer.yml) 里的 `schedule` 即可。

## 推荐配置方式

新版本优先使用 canonical Secrets：

| Secret | 说明 |
| --- | --- |
| `EPIC_EMAIL` | Epic 邮箱 |
| `EPIC_PASSWORD` | Epic 密码 |
| `LLM_PRESET` | 目标服务，例如 `gemini` / `openai` / `deepseek` / `glm` / `ollama` |
| `LLM_API_KEY` | API key |
| `LLM_BASE_URL` | base URL |
| `LLM_MODEL` | 模型名 |
| `LLM_THINKING_ENABLED` | 可选 |
| `LLM_REASONING_EFFORT` | 可选 |

旧字段仍然可用：

- `LLM_PROVIDER`
- `GEMINI_*`
- `GLM_*`
- `OPENAI_*`
- `DEEPSEEK_*`

但后续更推荐优先走 `LLM_PRESET + LLM_API_KEY + LLM_BASE_URL + LLM_MODEL`。

完整的 preset 示例，请看 [../../docs/providers.md](../../docs/providers.md)。

## 日志里会显示什么

运行开始时，日志会输出一段 runtime summary，包含：

- 当前 `protocol`
- 当前 `preset`
- 当前 `model`
- 当前 `base_url`
- 脱敏后的 Epic 邮箱

这样你可以直接从 Actions 日志判断本次到底用了哪条 provider 路线。

## 本地复现同一个入口

如果你想在本地复现 workflow 的启动路径：

1. 复制 [`.env.example`](../../.env.example) 为 `.env`
2. 填入自己的账号和模型配置
3. 执行 `uv sync --group dev`
4. 执行 `ENABLE_APSCHEDULER=false uv run app/deploy.py`

## 首次启动提醒

Fork 之后先打开你自己仓库的 `Actions` 页面，进入 `Epic Awesome Gamer (Scheduled)` 并点一次 `Enable workflow`，否则 GitHub 不会让这个 Fork 的定时 `schedule` 自动生效。

> [!IMPORTANT]
> 不要因为运行了几分钟还在重试就提前取消。验证码和 checkout 安全校验可能需要较长时间，有些最终成功的运行会持续 15 到 20 分钟。

## 提 issue 时建议附带什么

优先附带：

- 本次 Actions 运行链接
- `epic-logs-<run_id>.zip`
- `epic-runtime-<run_id>.zip`
- `epic-screenshots-<run_id>.zip`

不要只贴一小段控制台日志。
