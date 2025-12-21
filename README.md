<div align="center">

# 🎮 Epic Awesome Gamer
### (AiHubMix Enhanced Edition)

<img src="https://img.shields.io/static/v1?message=Python 3.12&color=3776AB&style=for-the-badge&logo=python&label=Build">
<img src="https://img.shields.io/static/v1?message=Gemini Pro&color=4285F4&style=for-the-badge&logo=google&label=AI Model">
<img src="https://img.shields.io/github/license/QIN2DIM/epic-awesome-gamer?style=for-the-badge&color=orange">
<img src="https://img.shields.io/github/actions/workflow/status/QIN2DIM/epic-awesome-gamer/ci.yaml?label=Auto Claim&style=for-the-badge&color=2ea44f">

<p class="description">
  🍷 <b>优雅、智能、全自动</b>。<br>
  专为 GitHub Actions 打造的 Epic Games Store 免费游戏领取机器人。
</p>

[特性一览](#-核心特性) • [快速部署](#-部署指南-github-actions) • [配置说明](#-配置详解-secrets) • [常见问题](#-常见问题-faq)

</div>

---

## 📖 项目简介

**Epic Awesome Gamer (AiHubMix 版)** 是一款基于 Python 的全自动 Epic 游戏领取工具。

本项目在原版基础上进行了**深度重构**，集成了 **AiHubMix (Gemini)** 多模态大模型来通过复杂的 hCaptcha 人机验证，并专门针对 GitHub Actions 环境进行了优化，确保“零成本”守护你的游戏库。

## ✨ 核心特性

| 模块 | 功能描述 |
| :--- | :--- |
| **🤖 AI 强力驱动** | 内置针对 `google-genai` SDK 的底层补丁，完美适配 **AiHubMix** 等中转站，支持 Base64 图片直传，**0 报错**通过 hCaptcha 验证。 |
| **⚡️ 即时结账支持** | 独家支持 **Instant Checkout** 流程。自动识别点击 "Get" 后弹出的支付窗口（如 *Blood West*），不再因为找不到购物车而漏领。 |
| **🛡️ 智能弹窗处理** | 自动识别并处理 **"内容警告 (Content Warning)"** 和年龄限制弹窗，确保脚本不会卡在确认页面。 |
| **📦 全内容收集** | 移除了原版的捆绑包过滤逻辑，无论是普通游戏还是 **Bundles**，所有免费内容一网打尽。 |
| **☁️ 云端自动运行** | 深度适配 GitHub Actions，利用 `uv` 极速管理依赖，每周定时自动执行，无需本地挂机。 |

---

## 🚀 部署指南 (GitHub Actions)

这是最推荐的部署方式，完全免费，配置一次即可永久自动运行。

### 1. Fork 仓库
点击页面右上角的 **Fork** 按钮，将本项目克隆到你自己的 GitHub 账号下。

### 2. 配置 Secrets
进入你 Fork 后的仓库，依次点击：
`Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`

添加以下必要变量：

| 变量名 | 必填 | 说明 | 示例 |
| :--- | :---: | :--- | :--- |
| `EPIC_EMAIL` | ✅ | Epic 账号邮箱 (**必须关闭 2FA**) | `myname@email.com` |
| `EPIC_PASSWORD` | ✅ | Epic 账号密码 | `password123` |
| `GEMINI_API_KEY` | ✅ | AiHubMix 或 Google 的 API Key | `sk-xxxxxxxx` |

### 3. 可选配置 (Advanced)

| 变量名 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `GEMINI_BASE_URL` | `https://aihubmix.com/v1` | 如果使用官方接口，请填 `https://generativelanguage.googleapis.com` |
| `GEMINI_MODEL` | `gemini-2.5-pro` | 推荐使用 2.5 Pro 或 1.5 Pro，视觉识别能力更强 |

### 4. 启动工作流
1. 点击仓库上方的 **Actions** 标签页。
2. 如果看到绿色按钮 **I understand my workflows...**，请点击启用。
3. 选择左侧的 `Epic Free Games` 工作流。
4. 点击右侧的 **Run workflow** 手动触发第一次运行测试。

> ✅ **成功提示**：之后的每周，脚本都会根据 `.github/workflows` 中的定时配置自动运行。

---

## 🐳 本地/Docker 部署

如果您拥有自己的服务器（VPS/NAS），也可以使用 Docker Compose 一键部署。

```bash
# 1. 克隆代码
git clone [https://github.com/your-username/epic-awesome-gamer.git](https://github.com/your-username/epic-awesome-gamer.git)
cd epic-awesome-gamer/docker

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入上述 Secrets 中的账号信息

# 3. 启动容器
docker compose up -d
