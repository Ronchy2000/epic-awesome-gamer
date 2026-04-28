# 本地调试与 Docker

本文说明本地单次运行和 Docker 运行方式。

默认建议先使用 GitHub Actions。只有在需要复现问题或长期运行时，再使用本文方式。

## 本地单次调试

### 1. 安装依赖

```bash
uv sync --group dev
```

### 2. 创建 `.env`

复制 `.env.example`：

```bash
cp .env.example .env
```

填写 Epic 账号和 provider 配置。

`.env`、`.venv`、`app/volumes/` 已被 `.gitignore` 忽略，不会提交到 GitHub。

### 3. 单次运行

```bash
ENABLE_APSCHEDULER=false uv run app/deploy.py
```

### 4. 查看本地产物

| 路径 | 内容 |
| --- | --- |
| `app/volumes/logs/` | 本地运行日志 |
| `app/volumes/runtime/` | 运行期调试文件 |
| `app/volumes/screenshots/` | 截图 |
| `app/volumes/user_data/` | 浏览器用户数据 |

## Docker 运行

### 1. 克隆仓库

```bash
git clone https://github.com/Ronchy2000/epic-freebies-helper.git
cd epic-freebies-helper
```

### 2. 修改配置

主要入口是 [`../docker/docker-compose.yaml`](../docker/docker-compose.yaml)。

GLM 示例：

```yaml
environment:
  - LLM_PROVIDER=glm
  - GLM_API_KEY=your_glm_key
  - GLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
  - GLM_MODEL=glm-4.6v
```

OpenAI / GPT 示例：

```yaml
environment:
  - LLM_PROVIDER=openai
  - OPENAI_API_KEY=your_openai_key
  - OPENAI_BASE_URL=https://api.openai.com/v1
  - OPENAI_MODEL=gpt-4.1-mini
```

Gemini / AiHubMix 示例：

```yaml
environment:
  - LLM_PROVIDER=gemini
  - GEMINI_API_KEY=your_key
  - GEMINI_BASE_URL=https://aihubmix.com
  - GEMINI_MODEL=gemini-2.5-pro
```

### 3. 启动

```bash
docker compose up -d --build
```

### 4. 查看日志

```bash
docker compose logs -f epic-freebies-helper
```

## 注意事项

- 本地和 Docker 运行会在 `app/volumes/` 下生成运行数据。
- 不要提交 `.env` 或运行期产物。
- 如果本地运行和 GitHub Actions 行为不同，优先对比日志和截图。
