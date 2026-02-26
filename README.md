# xhs-mcp-py

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

小红书 MCP 工具的 Python 实现，基于 Playwright 浏览器自动化，支持登录、发布、搜索、点赞、收藏、评论等功能。

## 特性

- 🔐 **扫码登录** - 支持二维码扫码登录，自动保存 cookies
- 📝 **发布内容** - 支持发布图文、视频、文字配图，支持定时发布
- 🔍 **搜索内容** - 支持关键词搜索（高级筛选能力在 MCP API 中提供）
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

### 使用流程

1. **首次使用必须先登录**：运行 `xhs-mcp login-browser` 弹出浏览器登录 或 `xhs-mcp login-qrcode --terminal` 在终端中显示二维码登录
2. **检查登录状态**：运行 `xhs-mcp status`（输出 `✅ 已登录` 或 `❌ 未登录`）
3. **执行操作**：登录成功后即可使用各种功能
4. **Cookies 有效期**：约 7-30 天，过期后需重新登录

> 💡 **MCP 使用提示**：让 AI 助手先调用 `check_login_status` 检查登录状态，如果未登录：
> - 通过 MCP：调用 `login_with_browser`
> - 或直接在命令行执行：`xhs-mcp login-browser`

## MCP 客户端配置

### Claude Desktop

编辑配置文件 
* `~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）
* `%APPDATA%\Claude\claude_desktop_config.json`（Windows）：

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
claude mcp add xhs-mcp -- xhs-mcp serve

# 查看已添加的 MCP
claude mcp list

# 移除 MCP 服务
claude mcp remove xhs-mcp
```

### Cursor

在 Cursor 设置中添加 MCP 配置：

1. 打开 Cursor Settings → Features → MCP Servers
2. 点击 "Add Server"
3. 填写：
   - Name: `xhs-mcp`
   - Command: `xhs-mcp serve`

### 其他 MCP 客户端

任何支持 MCP 协议的客户端都可以使用，启动命令为：

```bash
xhs-mcp serve
```

## 发布

### 图文

```
图：~/Downloads/vc.png

文字标题：Vibe Coding 真的心累💔

文字正文内容：强如 Opus，也只是傻乎乎地解决当下的指令...

就拿我的项目来说👇
App有两个登录渠道：
✅ 浏览器登录 ← 先调试好了
✅ 二维码登录 ← 后调试的

结果你猜怎么着？
浏览器登录的逻辑直接被二维码登录给复用覆盖了！😅

AI不会帮你考虑整体架构
它只看「现在」要解决的问题
就像装修师傅：你让他修灯，他可能把你刚装好的开关拆了😂

标签：#VibeCoding #AI #Claude #Agent #Opus
```

### 文字配图

```
封面文字：我开源了个小红书自动发布工具：xhs-mcp-py

文字标题：我开源了个小红书自动发布工具：xhs-mcp-py

文字正文内容：
我开源了个小红书自动发布工具：xhs-mcp-py。

基于 Python，轻松兼容 Windows、Mac、Linux。
支持 Claude Code 和 OpenClaw，还能发布文字配图笔记。
核心原理：模拟浏览器登录。

项目地址：https://github.com/luweizheng/xhs-mcp-py

欢迎来玩！
```

## 命令行使用

```bash
# 1. 扫码登录（首次使用必须执行）
# 方式一：打开浏览器窗口扫码
xhs-mcp login-browser

# 方式二：在终端显示二维码，在 Claude Code、Open Code 中推荐使用这种
# 注意：需要安装 zbar 库（macOS: brew install zbar，Ubuntu: apt install libzbar0）
# 如果未安装 zbar，会自动保存二维码图片并提示路径
xhs-mcp login-qrcode --terminal

# 方式三：保存二维码图片，在 OpenClaw 中将 qrcode.png 发送给 Channel 中的用户
xhs-mcp login-qrcode --save qrcode.png

# 2. 检查登录状态（确认已登录后再执行其他操作）
xhs-mcp status

# 发布图文
xhs-mcp publish -t "标题" -c "文字正文内容" -i image1.jpg -i image2.jpg --tag 旅行 --tag 美食

# 发布视频
xhs-mcp publish-video -t "标题" -c "文字正文内容" -v video.mp4

# 发布文字配图（将文字生成为卡片图片）
xhs-mcp publish-text-card -c "封面文字" -p "第一页内容" -p "第二页内容" -s "基础" -t "笔记标题"

# 搜索内容
xhs-mcp search -k "关键词"

# 点赞/取消点赞
xhs-mcp like --feed-id FEED_ID --xsec-token XSEC_TOKEN
xhs-mcp like --feed-id FEED_ID --xsec-token XSEC_TOKEN --unlike

# 收藏/取消收藏
xhs-mcp favorite --feed-id FEED_ID --xsec-token XSEC_TOKEN
xhs-mcp favorite --feed-id FEED_ID --xsec-token XSEC_TOKEN --unfavorite

# 发表评论
xhs-mcp comment --feed-id FEED_ID --xsec-token XSEC_TOKEN -c "评论内容"

# 回复评论
xhs-mcp reply-comment --feed-id FEED_ID --xsec-token XSEC_TOKEN -c "回复内容" --comment-id COMMENT_ID

# 退出登录
xhs-mcp logout

# 启动 MCP 服务
xhs-mcp serve
```

## MCP 工具列表

| 工具名 | 说明 |
|--------|------|
| `login_with_browser` | **浏览器登录** - 弹出浏览器窗口扫码登录，cookies 保存后可复用 |
| `check_login_status` | 检查登录状态 |
| `get_login_qrcode` | 获取登录二维码（返回 Base64 图片，需配合轮询使用）|
| `delete_cookies` | 删除 cookies，重置登录 |
| `publish_content` | 发布图文内容 |
| `publish_text_card` | 发布文字配图笔记 |
| `publish_with_video` | 发布视频内容 |
| `list_feeds` | 获取首页推荐列表 |
| `search_feeds` | 搜索内容 |
| `get_feed_detail` | 获取笔记详情 |
| `get_user_profile` | 获取用户主页 |
| `like_feed` | 点赞/取消点赞 |
| `favorite_feed` | 收藏/取消收藏 |
| `post_comment` | 发表评论 |
| `reply_comment` | 回复评论 |

## API 参考

> 💡 **提示：** 点击下方功能标题可展开查看详细说明

<details>
<summary><b>1. 登录和检查登录状态</b></summary>

第一步必须，小红书需要进行登录。可以检查当前登录状态。

**MCP 工具：**
- `login_with_browser` - 启动浏览器扫码登录，cookies 保存后可复用
- `check_login_status` - 检查当前登录状态
- `delete_cookies` - 删除 cookies，重置登录状态

**命令行：**
```bash
# 浏览器扫码登录
xhs-mcp login-browser

# 终端二维码登录，在 Claude Code、Open Code 中推荐使用这种
xhs-mcp login-qrcode --terminal

# 检查登录状态
xhs-mcp status

# 退出登录
xhs-mcp logout
```

</details>

<details>
<summary><b>2. 发布图文内容</b></summary>

支持发布图文内容到小红书，包括标题、内容描述和图片。

**MCP 工具：** `publish_content`

**参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 文章标题（最多20个字） |
| `content` | string | ✅ | 文字正文内容 |
| `images` | list[string] | ✅ | 图片路径列表（本地绝对路径） |
| `tags` | list[string] | ❌ | 话题标签列表 |
| `schedule_at` | string | ❌ | 定时发布时间（ISO8601格式） |

**命令行：**
```bash
xhs-mcp publish -t "标题" -c "文字正文内容" -i image1.jpg -i image2.jpg --tag 旅行 --tag 美食
```

</details>

<details>
<summary><b>3. 发布视频内容</b></summary>

支持发布视频内容到小红书，包括标题、内容描述和本地视频文件。

**MCP 工具：** `publish_with_video`

**参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 文章标题（最多20个字） |
| `content` | string | ✅ | 文字正文内容 |
| `video` | string | ✅ | 本地视频绝对路径 |
| `tags` | list[string] | ❌ | 话题标签列表 |
| `schedule_at` | string | ❌ | 定时发布时间（ISO8601格式） |

**命令行：**
```bash
xhs-mcp publish-video -t "标题" -c "文字正文内容" -v video.mp4
```

</details>

<details>
<summary><b>4. 发布文字配图</b></summary>

将文字生成为卡片图片并发布，支持多页和多种样式。

**MCP 工具：** `publish_text_card`

**参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `cover_text` | string | ✅ | 封面文字 |
| `pages` | list[string] | ❌ | 正文页列表（最多17页） |
| `style` | string | ❌ | 卡片样式：基础/边框/备忘/手写/便签/涂写/简约/光影/几何 |
| `title` | string | ❌ | 文章标题 |
| `content` | string | ❌ | 文字正文内容 |
| `tags` | list[string] | ❌ | 话题标签列表 |

**命令行：**
```bash
xhs-mcp publish-text-card -c "封面文字" -p "第一页" -p "第二页" -s "基础" -t "笔记标题"
```

</details>

<details>
<summary><b>5. 搜索内容</b></summary>

根据关键词搜索小红书内容，支持多维度筛选。

**MCP 工具：** `search_feeds`

**参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `keyword` | string | ✅ | 搜索关键词 |
| `sort_by` | string | ❌ | 排序：综合/最新/最多点赞/最多评论/最多收藏 |
| `note_type` | string | ❌ | 类型：不限/视频/图文 |
| `publish_time` | string | ❌ | 时间：不限/一天内/一周内/半年内 |
| `search_scope` | string | ❌ | 范围：不限/已看过/未看过/已关注 |
| `location` | string | ❌ | 位置：不限/同城/附近 |

**命令行：**
```bash
xhs-mcp search -k "关键词"
```

</details>

<details>
<summary><b>6. 获取推荐列表</b></summary>

获取小红书首页推荐内容列表。

**MCP 工具：** `list_feeds`

**参数：** 无

</details>

<details>
<summary><b>7. 获取笔记详情</b></summary>

获取小红书笔记的完整详情，包括内容、互动数据和评论。

**MCP 工具：** `get_feed_detail`

**参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `feed_id` | string | ✅ | 笔记 ID（从搜索或推荐列表获取） |
| `xsec_token` | string | ✅ | 访问令牌（从搜索或推荐列表获取） |
| `load_comments` | bool | ❌ | 是否加载评论（基础模式，前10条） |
| `load_all_comments` | bool | ❌ | 是否加载全部评论（滚动加载） |
| `limit` | int | ❌ | 限制一级评论数量（默认20） |
| `click_more_replies` | bool | ❌ | 是否展开二级回复 |
| `reply_limit` | int | ❌ | 跳过回复数过多的评论（默认10） |
| `scroll_speed` | string | ❌ | 滚动速度：slow/normal/fast |

</details>

<details>
<summary><b>8. 获取用户主页</b></summary>

获取小红书用户的个人主页信息。

**MCP 工具：** `get_user_profile`

**参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `user_id` | string | ✅ | 用户 ID |
| `xsec_token` | string | ✅ | 访问令牌 |

</details>

<details>
<summary><b>9. 点赞/收藏</b></summary>

对笔记进行点赞或收藏操作。

**MCP 工具：**
- `like_feed` - 点赞/取消点赞
- `favorite_feed` - 收藏/取消收藏

**参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `feed_id` | string | ✅ | 笔记 ID |
| `xsec_token` | string | ✅ | 访问令牌 |
| `unlike`/`unfavorite` | bool | ❌ | 是否取消操作（默认 false） |

</details>

<details>
<summary><b>10. 发表评论/回复</b></summary>

对笔记发表评论或回复已有评论。

**MCP 工具：**
- `post_comment` - 发表评论
- `reply_comment` - 回复评论

**post_comment 参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `feed_id` | string | ✅ | 笔记 ID |
| `xsec_token` | string | ✅ | 访问令牌 |
| `content` | string | ✅ | 评论内容 |

**reply_comment 参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `feed_id` | string | ✅ | 笔记 ID |
| `xsec_token` | string | ✅ | 访问令牌 |
| `content` | string | ✅ | 回复内容 |
| `comment_id` | string | ❌ | 目标评论 ID |
| `user_id` | string | ❌ | 目标用户 ID |

> **注意：** `comment_id` 和 `user_id` 至少需要提供一个

</details>

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
- 浏览器扫码登录需要弹出浏览器窗口，请使用 `xhs-mcp login-browser`
- cookies 默认保存在当前目录的 `cookies.json` 文件
- 可通过环境变量 `COOKIES_PATH` 指定 cookies 文件路径

## License

MIT
