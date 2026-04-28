# Provider 配置说明

本文说明模型 provider 的配置方式、模型要求和常见接口错误。

## 支持的 Provider

| Provider | 用途 | 推荐模型 |
| --- | --- | --- |
| `glm` | 调用智谱 GLM 视觉模型处理验证码 | `glm-4.6v` |
| `openai` | 调用 OpenAI / GPT 视觉模型处理验证码 | `gpt-4.1-mini` |
| `gemini` | 调用 Gemini 或 AiHubMix 兼容接口处理验证码 | `gemini-2.5-pro` |

`LLM_PROVIDER` 必须填写为上表中的一个值。

## GLM

### Secrets

| Secret | 说明 | 示例 |
| --- | --- | --- |
| `LLM_PROVIDER` | 固定为 `glm` | `glm` |
| `GLM_API_KEY` | 智谱 API Key | - |
| `GLM_BASE_URL` | 智谱 OpenAI 兼容接口地址 | `https://open.bigmodel.cn/api/paas/v4` |
| `GLM_MODEL` | 支持图片输入的 GLM 模型 | `glm-4.6v` |

### 推荐配置

| Secret | 推荐值 |
| --- | --- |
| `LLM_PROVIDER` | `glm` |
| `GLM_BASE_URL` | `https://open.bigmodel.cn/api/paas/v4` |
| `GLM_MODEL` | `glm-4.6v` |

### 注意事项

- `glm-4.6v` 作为默认推荐模型。
- `glm-4.6v-flash` 在高峰期可能出现模型繁忙错误。
- 如果 API 无法调用，先检查 API Key、账户状态和接口权限。
- GLM provider 不需要额外配置 `GEMINI_API_KEY`。

## OpenAI / GPT

### Secrets

| Secret | 说明 | 示例 |
| --- | --- | --- |
| `LLM_PROVIDER` | 固定为 `openai` | `openai` |
| `OPENAI_API_KEY` | OpenAI API Key | - |
| `OPENAI_BASE_URL` | OpenAI API 地址 | `https://api.openai.com/v1` |
| `OPENAI_MODEL` | 支持图片输入的模型 | `gpt-4.1-mini` |

### 推荐配置

| Secret | 推荐值 |
| --- | --- |
| `LLM_PROVIDER` | `openai` |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` |
| `OPENAI_MODEL` | `gpt-4.1-mini` |

### 模型要求

OpenAI provider 要求模型支持图片输入。

如果使用第三方 OpenAI 兼容网关，需要确认该网关支持 Chat Completions 的
`image_url` 输入格式。

### 常见错误

| 现象 | 可能原因 | 处理方式 |
| --- | --- | --- |
| HTTP 400 | 模型不支持图片输入 | 更换支持图片输入的模型 |
| `unsupported image` | 网关不支持图片参数 | 更换网关或使用官方接口 |
| `invalid content type` | 请求格式不被兼容接口支持 | 检查 `OPENAI_BASE_URL` 和模型能力 |
| `authentication failed` | API Key 无效或未配置 | 检查 `OPENAI_API_KEY` |

## Gemini / AiHubMix

### Secrets

| Secret | 说明 | 示例 |
| --- | --- | --- |
| `LLM_PROVIDER` | 固定为 `gemini` | `gemini` |
| `GEMINI_API_KEY` | Gemini 或 AiHubMix Key | - |
| `GEMINI_BASE_URL` | Gemini 兼容接口地址 | `https://aihubmix.com` |
| `GEMINI_MODEL` | Gemini 模型 | `gemini-2.5-pro` |

### 推荐配置

| Secret | 推荐值 |
| --- | --- |
| `LLM_PROVIDER` | `gemini` |
| `GEMINI_BASE_URL` | `https://aihubmix.com` |
| `GEMINI_MODEL` | `gemini-2.5-pro` |

### 注意事项

- 变量名是 `GEMINI_BASE_URL`，不是 `GEMINI_BASE_MODEL`。
- 使用官方 Gemini 接口时，`GEMINI_BASE_URL` 需要按实际接口地址配置。
- 使用 AiHubMix 时，确认账户余额、模型权限和接口地址。

## 高级模型覆盖项

以下配置通常不需要填写。留空时会自动使用当前 provider 的默认模型。

| Secret | 说明 |
| --- | --- |
| `CHALLENGE_CLASSIFIER_MODEL` | 验证码类型识别模型 |
| `IMAGE_CLASSIFIER_MODEL` | 图片分类模型 |
| `SPATIAL_POINT_REASONER_MODEL` | 点选类验证码推理模型 |
| `SPATIAL_PATH_REASONER_MODEL` | 拖拽路径类验证码推理模型 |

只有在需要为不同验证码步骤指定不同模型时再填写。

## 配置检查清单

- `LLM_PROVIDER` 与所选 provider 的 Key、Base URL、Model 变量一致。
- 模型支持图片输入。
- Base URL 没有多余路径或拼写错误。
- API Key 没有复制到末尾换行或空格。
- GitHub Secrets 中没有把 `GEMINI_BASE_URL` 写成 `GEMINI_BASE_MODEL`。
