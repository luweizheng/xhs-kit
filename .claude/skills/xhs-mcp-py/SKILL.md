---
name: xhs-auto-ops
description: 小红书内容发布与管理助手。当用户要求登录、发小红书、搜索小红书、评论点赞收藏等任何小红书相关操作时使用。
metadata: {"openclaw": {"emoji": "📕", "requires": {"bins": ["convert"]}}}
---

# xhs-mcp-py 使用方式

## 安装

首次使用需要确认环境中有 Python 解释器。

```bash
# 使用 pip 安装
pip install xhs-mcp

# 安装 Playwright 浏览器
playwright install chromium
```

## 发布或评论前必须先登录

**重要：** 所有操作都需要先登录小红书账号。

### 检查登录状态

```bash
xhs-mcp status
```

如果返回 `is_logged_in: false`，需要先登录。

### 登录方式

```bash
# 方式一：启动浏览器扫码登录（推荐）
xhs-mcp login-browser

# 方式二：在终端显示二维码，在 Claude Code、Open Code 中推荐使用这种
xhs-mcp login-qrcode --terminal

# 方式三：保存二维码图片，在 OpenClaw 中将 qrcode.png 发送给 Channel 中的用户
xhs-mcp login-qrcode --save /tmp/qrcode.png
```

登录成功后，cookies 会保存到本地文件，后续操作会自动复用。

### MCP 工具登录

如果通过 MCP 客户端使用：

**方式一：浏览器登录（推荐桌面环境）**
调用 `login_with_browser` 工具：
- 会弹出浏览器窗口显示二维码
- 用小红书 App 扫码登录
- 登录成功后 cookies 自动保存

**方式二：命令行登录（推荐 Claude Code / Open Code）**
在终端执行：
```bash
xhs-mcp login-qrcode --terminal
```
- 二维码直接显示在终端
- 扫码成功后 cookies 自动保存

### 登录状态检查流程

1. 先调用 `check_login_status` 检查是否已登录
2. 如果 `is_logged_in: false`，提醒用户需要登录
3. 根据环境选择登录方式：
   - 桌面环境：调用 `login_with_browser` 工具（会弹出浏览器窗口）
   - Claude Code / Open Code：执行命令 `xhs-mcp login-qrcode --terminal`
4. 登录成功后再执行其他操作
