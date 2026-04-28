# 排障说明

本文说明 GitHub Actions 日志、Artifact、常见问题和提交 Issue 前需要准备的信息。

## 查看 GitHub Actions 日志

1. 打开 Fork 后仓库的 `Actions` 页面。
2. 选择失败或异常的运行记录。
3. 打开 `Run Epic Awesome Gamer` 步骤。
4. 查看登录、验证码、商品页、checkout 阶段的日志。

不要只根据最后一行判断失败原因。验证码和 checkout 阶段可能有多轮重试。

## 下载 Artifact

1. 打开本次 GitHub Actions 运行页面。
2. 拉到页面底部。
3. 找到 `Artifacts`。
4. 下载页面中实际出现的 zip 文件。

## Artifact 类型

| Artifact | 内容 | 出现条件 |
| --- | --- | --- |
| `epic-logs-<run_id>` | 运行日志 | 通常每次运行都会上传 |
| `epic-runtime-<run_id>` | `promotions.json`、`purchase_debug` 截图和文本 | 进入商品页或 checkout 阶段后常见 |
| `epic-screenshots-<run_id>` | 登录失败、风控页、授权页截图 | 登录或授权阶段保存过截图时出现 |

GitHub Actions 只显示实际上传成功且包含文件的 Artifact。不同运行记录中显示的
Artifact 可能不同。

## 常见问题索引

| 日志或现象 | 阶段 | 可能原因 | 处理方式 |
| --- | --- | --- | --- |
| `two_factor_authentication.required` | 登录 | Epic 账号仍启用 2FA | 关闭邮箱、短信、验证器二步验证后重新运行 |
| 页面跳转到 `/id/login/mfa` | 登录 | Epic 要求二步验证 | 关闭 Epic 2FA |
| `privacy-policy correction` | 登录后跳转 | 账号需要确认隐私政策 | 使用浏览器手动登录 Epic 并完成确认 |
| `One more step` | 结账 | Epic 结账阶段追加人机校验 | 等待脚本处理，不要立即取消 |
| `Device not supported` | 商品页或结账 | 商品仅支持 Windows | 等待脚本点击 `Continue` |
| Actions 运行 15 分钟以上 | 验证码或结账 | 多轮重试 | 等待运行结束后查看日志 |
| 工作流成功但游戏未入库 | 结账 | 状态识别或 checkout 未完成 | 下载 Artifact 并提交 Issue |

## 登录阶段问题

### Epic 2FA 未关闭

当前项目不处理 Epic 邮箱、短信、验证器二步验证。

如果日志中出现以下内容，通常表示 2FA 仍启用：

- `errors.com.epicgames.common.two_factor_authentication.required`
- `Two-Factor authentication required to process request`
- 页面跳转到 `/id/login/mfa`

处理方式：

1. 使用浏览器登录 Epic 账号。
2. 进入账号安全设置页面。
3. 移除所有启用的二步验证方式。
4. 重新运行 GitHub Actions。

参考界面：

![Epic 2FA remove methods](images/faq/epic-2fa-remove-methods.png)

### 隐私政策确认页

部分账号登录后会跳转到 `/id/login/correction/privacy-policy`。

处理方式：

1. 使用浏览器手动登录 Epic。
2. 完成隐私政策确认。
3. 重新运行 GitHub Actions。

## 验证码阶段问题

验证码阶段可能触发多轮模型请求和页面重试。运行时间较长不一定表示失败。

如果失败，请查看：

- `epic-logs-<run_id>` 中的 provider 错误。
- `epic-runtime-<run_id>` 中的 `purchase_debug` 文件。
- `epic-screenshots-<run_id>` 中的登录或风控截图。

## 结账阶段问题

### `One more step`

这是 Epic checkout 阶段的额外人机校验。项目会尝试处理该环节。

![Checkout Security Check](images/faq/checkout-security-check.png)

### `Device not supported`

该提示通常表示商品仅支持 Windows，而 GitHub Actions 使用 Linux 环境。

当前流程会尝试点击 `Continue` 后继续执行。最终结果以日志和 Artifact 为准。

## Provider 接口问题

| 日志或现象 | 可能原因 | 处理方式 |
| --- | --- | --- |
| 401 / 403 | API Key 无效、权限不足或账户不可用 | 检查 provider API Key 和账户状态 |
| 429 | provider 限流或额度不足 | 稍后重试或更换模型 |
| HTTP 400 | 模型或接口不支持当前图片输入 | 更换支持图片输入的模型 |
| `model not found` | 模型名写错或账户无权限 | 检查模型名和账户权限 |
| `GEMINI_BASE_MODEL` | 变量名写错 | 改为 `GEMINI_BASE_URL` |

## 提交 Issue 前需要准备的信息

提交 Issue 时请提供：

- 本次 GitHub Actions 运行链接。
- 使用的 provider：`glm` / `openai` / `gemini`。
- 失败阶段：登录 / 验证码 / 商品页 / checkout / 其他。
- 相关日志片段。
- 本次运行生成的 Artifact zip。

如果 fork 是私有仓库，需要上传实际 Artifact。维护者无法访问私有仓库的 Actions 页面。
