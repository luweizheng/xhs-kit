# xhs-mcp-py

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

小红书 MCP 工具的 Python 实现，基于 Playwright 浏览器自动化，支持登录、发布、搜索、点赞、收藏、评论等功能。

## 特性

- 🔐 **扫码登录** - 支持二维码扫码登录，自动保存 cookies
- 📝 **发布内容** - 支持发布图文、视频、文字配图，支持定时发布
- 🔍 **搜索内容** - 支持关键词搜索，支持多维度筛选（排序、类型、时间、范围、位置）
- ❤️ **互动功能** - 支持点赞、收藏、评论、回复评论
- 📊 **数据获取** - 获取首页推荐、笔记详情、用户主页，支持高级评论加载配置
- 🤖 **MCP 协议** - 支持 MCP 协议，可与 AI 助手集成

## 安装

```bash
pip install xhs-mcp-py

# 首次运行需安装浏览器
playwright install chromium
```

## 快速开始

### 命令行使用

```bash
# 扫码登录（会打开浏览器窗口）
xhs-mcp login --no-headless

# 检查登录状态
xhs-mcp status

# 发布图文
xhs-mcp publish -t "标题" -c "正文内容" -i image1.jpg -i image2.jpg --tag 旅行 --tag 美食

# 发布视频
xhs-mcp publish-video -t "标题" -c "正文内容" -v video.mp4

# 发布文字配图（将文字生成为卡片图片）
xhs-mcp publish-text-card -c "封面文字" -p "第一页内容" -p "第二页内容" -s "基础" -t "笔记标题"

# 搜索内容
xhs-mcp search -k "关键词"

# 退出登录
xhs-mcp logout

# 启动 MCP 服务
xhs-mcp serve
```

## MCP 工具列表

| 工具名 | 说明 |
|--------|------|
| `check_login_status` | 检查登录状态 |
| `get_login_qrcode` | 获取登录二维码 |
| `delete_cookies` | 删除 cookies，重置登录 |
| `publish_content` | 发布图文内容 |
| `publish_with_video` | 发布视频内容 |
| `list_feeds` | 获取首页推荐列表 |
| `search_feeds` | 搜索内容 |
| `get_feed_detail` | 获取笔记详情 |
| `get_user_profile` | 获取用户主页 |
| `like_feed` | 点赞/取消点赞 |
| `favorite_feed` | 收藏/取消收藏 |
| `post_comment` | 发表评论 |
| `reply_comment` | 回复评论 |
| `publish_text_card` | 发布文字配图笔记 |

## MCP 客户端配置

### Claude Desktop

编辑配置文件 `~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）或 `%APPDATA%\Claude\claude_desktop_config.json`（Windows）：

```json
{
  "mcpServers": {
    "xiaohongshu": {
      "command": "xhs-mcp",
      "args": ["serve"]
    }
  }
}
```

如果 `xhs-mcp` 不在系统 PATH 中，使用完整路径：

```json
{
  "mcpServers": {
    "xiaohongshu": {
      "command": "/path/to/your/python/bin/xhs-mcp",
      "args": ["serve"]
    }
  }
}
```

可通过 `which xhs-mcp`（macOS/Linux）或 `where xhs-mcp`（Windows）查看完整路径。

配置完成后重启 Claude Desktop。

### Claude Code

```bash
# 添加 MCP 服务


# 查看已添加的 MCP
claude mcp list

# 移除 MCP 服务
claude mcp remove xiaohongshu
```

### Cursor

在 Cursor 设置中添加 MCP 配置：

1. 打开 Cursor Settings → Features → MCP Servers
2. 点击 "Add Server"
3. 填写：
   - Name: `xiaohongshu`
   - Command: `xhs-mcp serve`

### 其他 MCP 客户端

任何支持 MCP 协议的客户端都可以使用，启动命令为：

```bash
xhs-mcp serve
```

## API 参考

### XhsClient

| 方法 | 说明 |
|------|------|
| `login()` | 交互式扫码登录 |
| `is_logged_in()` | 检查是否已登录 |
| `delete_cookies()` | 删除 cookies |
| `publish(title, content, images, tags)` | 发布图文 |
| `publish_video(title, content, video, tags)` | 发布视频 |
| `search(keyword, filters)` | 搜索内容 |
| `get_feeds()` | 获取首页推荐 |
| `get_feed_detail(feed_id, xsec_token)` | 获取笔记详情 |
| `get_user_profile(user_id, xsec_token)` | 获取用户主页 |
| `like(feed_id, xsec_token)` | 点赞 |
| `unlike(feed_id, xsec_token)` | 取消点赞 |
| `favorite(feed_id, xsec_token)` | 收藏 |
| `unfavorite(feed_id, xsec_token)` | 取消收藏 |
| `comment(feed_id, xsec_token, content)` | 发表评论 |
| `reply_comment(feed_id, xsec_token, content, comment_id, user_id)` | 回复评论 |

## 开发

```bash
# 克隆项目
git clone https://github.com/luweizheng/xhs-mcp-py.git
cd xhs-mcp-py

# 安装开发依赖
pip install -e ".[dev]"

# 安装浏览器
playwright install chromium

# 运行测试
pytest
```

## 注意事项

- 首次使用需要扫码登录，登录后 cookies 会保存到本地
- 建议使用 `--no-headless` 模式进行登录，以便扫码
- cookies 默认保存在当前目录的 `cookies.json` 文件
- 可通过环境变量 `COOKIES_PATH` 指定 cookies 文件路径

## License

MIT
