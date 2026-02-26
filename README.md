# xhs-mcp-py

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

小红书 MCP 工具的 Python 实现，基于 Playwright 浏览器自动化，支持登录、发布、搜索、点赞、收藏、评论等功能。

## 特性

- 🔐 **扫码登录** - 支持二维码扫码登录，自动保存 cookies
- 📝 **发布内容** - 支持发布图文、视频，支持定时发布
- 🔍 **搜索内容** - 支持关键词搜索，支持筛选条件
- ❤️ **互动功能** - 支持点赞、收藏、评论
- 📊 **数据获取** - 获取首页推荐、笔记详情、用户主页
- 🤖 **MCP 协议** - 支持 MCP 协议，可与 AI 助手集成

## 安装

```bash
pip install xhs-mcp

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

# 搜索内容
xhs-mcp search -k "关键词"

# 退出登录
xhs-mcp logout

# 启动 MCP 服务
xhs-mcp serve
```

### Python API

```python
import asyncio
from xhs_mcp import XhsClient

async def main():
    # 创建客户端（headless=False 可看到浏览器窗口）
    async with XhsClient(headless=False) as client:
        # 扫码登录
        await client.login()
        
        # 检查登录状态
        if await client.is_logged_in():
            # 发布图文
            result = await client.publish(
                title="我的标题",
                content="正文内容",
                images=["./img1.jpg", "./img2.jpg"],
                tags=["旅行", "美食"]
            )
            print(f"发布结果: {result.status}")
            
            # 搜索内容
            feeds = await client.search("Python")
            for feed in feeds.feeds[:5]:
                print(f"- {feed.display_title}")
            
            # 点赞
            await client.like(feed_id="xxx", xsec_token="xxx")
            
            # 收藏
            await client.favorite(feed_id="xxx", xsec_token="xxx")
            
            # 评论
            await client.comment(feed_id="xxx", xsec_token="xxx", content="好文章！")

asyncio.run(main())
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

### MCP 配置示例

在 Claude Desktop 或其他 MCP 客户端中配置：

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

## 开发

```bash
# 克隆项目
git clone https://github.com/yourname/xhs-mcp-py.git
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
