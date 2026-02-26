# xhs-mcp-py 项目说明

## 项目概述

xhs-mcp-py 是一个小红书自动化工具，基于 Playwright 浏览器自动化框架实现，支持通过 MCP 协议与 AI 助手集成。

**核心功能：**
- 扫码登录（浏览器/二维码两种模式）
- 发布图文、视频、文字配卡笔记
- 搜索内容、获取推荐流
- 点赞、收藏、评论、回复
- 获取笔记详情、用户主页
---

## 实现思路

### 1. 浏览器自动化核心

基于 **Playwright** 模拟真实浏览器行为：

- 创建持久化浏览器上下文（Persistent Context）
- 复用用户数据目录和 cookies，避免重复登录
- 模拟真实用户操作（点击、输入、滚动等）
- 拦截和分析网络请求，获取 API 数据

核心文件：`src/xhs_mcp/browser.py`

### 2. 登录机制

小红书需要登录才能使用，实现了两种登录方式：

**浏览器扫码登录：**
- 弹出浏览器窗口访问小红书登录页
- 用户扫码后自动保存 cookies

**二维码登录（CLI 模式）：**
- 通过截取登录页的二维码获取登录二维码
- 支持终端显示二维码（需安装 zbar）
- 支持保存二维码图片
- 轮询检测登录状态

核心文件：`src/xhs_mcp/login.py`、`src/xhs_mcp/cookies.py`

### 3. 内容发布

**图文发布：**
- 访问创作者发布页面
- 上传图片、填写标题和正文
- 支持添加话题标签
- 支持定时发布

**文字配卡发布：**
- 使用小红书自带的文字生图将文字渲染为卡片
- 支持多页、多种样式（基础、边框、手写等）

核心文件：`src/xhs_mcp/publish.py`、`src/xhs_mcp/text_card.py`

### 4. 数据获取

**搜索与推荐：**
- 访问搜索页面，模拟用户输入关键词
- 监听网络请求拦截搜索结果 API 响应
- 解析返回的 JSON 数据

**笔记详情、用户主页：**
- 直接访问笔记/用户页面 URL
- 监听 API 响应获取结构化数据

核心文件：`src/xhs_mcp/search.py`、`src/xhs_mcp/feeds.py`、`src/xhs_mcp/feed_detail.py`

### 5. MCP 协议集成

将上述功能封装为 MCP 工具：

```
MCP Server (stdio 模式)
  ├── login_with_browser
  ├── check_login_status
  ├── get_login_qrcode
  ├── publish_content
  ├── publish_text_card
  ├── publish_with_video
  ├── search_feeds
  ├── list_feeds
  ├── get_feed_detail
  ├── get_user_profile
  ├── like_feed / favorite_feed
  └── post_comment / reply_comment
```

核心文件：`src/xhs_mcp/mcp_server.py`

### 6. CLI 封装

提供命令行接口 `xhs-mcp`，支持所有 MCP 工具的对应命令：

核心文件：`src/xhs_mcp/cli.py`

---

## 开发规范

### 不修改已有功能

**本项目遵循「只修 bug，不改功能」原则：**

- ✅ 可以修复现有 bug
- ✅ 可以优化错误提示和日志
- ✅ 可以改进代码结构和注释
- ❌ 不要修改现有功能的业务逻辑
- ❌ 不要添加未经讨论的新功能
- ❌ 不要删除或重命名现有接口

### 添加新功能的流程

如果需要添加新功能：

1. 先与项目维护者讨论需求和设计
2. 确认后再进行实现
3. 新功能应通过 MCP 工具和 CLI 双暴露

### 代码结构

```
src/xhs_mcp/
├── browser.py        # Playwright 浏览器封装
├── cookies.py        # Cookies 管理
├── login.py          # 登录逻辑（浏览器/二维码）
├── publish.py        # 发布图文/视频
├── text_card.py      # 文字生图生成
├── search.py         # 搜索功能
├── feeds.py          # 推荐流获取
├── feed_detail.py    # 笔记详情
├── user_profile.py   # 用户主页
├── interact.py       # 点赞/收藏/评论
├── models.py         # Pydantic 数据模型
├── mcp_server.py     # MCP 服务入口
└── cli.py            # 命令行入口
```
