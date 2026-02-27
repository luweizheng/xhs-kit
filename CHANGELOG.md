# Changelog

## [0.1.4] - 2025-02-26

### 新增功能

- **CLI 互动命令** - 新增命令行互动功能
  - `xhs-mcp like` - 点赞/取消点赞笔记
  - `xhs-mcp favorite` - 收藏/取消收藏笔记
  - `xhs-mcp comment` - 发表评论
  - `xhs-mcp reply-comment` - 回复评论

### 改进

- **互动功能稳定性** - 修复点赞、收藏、评论的选择器超时问题
  - 增加对互动容器的显式等待
  - 使用 locator 方式点击，确保元素可见
  - 评论功能使用 force 点击避免被遮挡问题
- **结果验证** - 点赞和收藏操作后验证状态变化，确保操作成功
- **错误处理** - CLI 命令正确处理操作结果，显示明确的成功/失败信息

### 修复

- **页面结构适配** - 修复小红书页面改版导致的选择器失效问题
  - 更新点赞按钮选择器: `.like-wrapper .like-lottie`
  - 更新收藏按钮选择器: `.collect-wrapper .collect-icon`
  - 更新页面加载等待选择器

## [0.1.0] - 2025-02-26

### 初始版本

#### 核心功能

- **扫码登录** (`login`) - 二维码扫码登录，自动保存 cookies 到本地
- **登录状态检查** (`check_login_status`) - 检查当前登录状态
- **删除 Cookies** (`delete_cookies`) - 清除登录信息

#### 发布功能

- **发布图文** (`publish_content`) - 支持多图、标签、定时发布
- **发布视频** (`publish_with_video`) - 支持视频文件上传

#### 搜索与浏览

- **搜索内容** (`search_feeds`) - 关键词搜索，支持排序和类型筛选
- **首页推荐** (`list_feeds`) - 获取首页推荐列表
- **笔记详情** (`get_feed_detail`) - 获取笔记详情和评论
- **用户主页** (`get_user_profile`) - 获取用户主页信息

#### 互动功能

- **点赞** (`like_feed`) - 点赞/取消点赞
- **收藏** (`favorite_feed`) - 收藏/取消收藏
- **评论** (`post_comment`) - 发表评论

#### 工具支持

- **MCP 协议** - 支持 stdio 模式，可与 Claude Desktop、Claude Code 等 AI 助手集成
- **CLI 命令行** - `xhs-mcp` 命令行工具，支持登录、发布、搜索等操作

## [0.1.1] - 2025-02-26

### 新增功能

- **文字配图发布** (`publish_text_card`) - 支持将文字生成为卡片图片发布
  - 封面文字 + 最多17页正文
  - 9种卡片样式：基础、边框、备忘、手写、便签、涂写、简约、光影、几何
  - 支持标题、正文描述

- **回复评论** (`reply_comment`) - 支持回复笔记下的指定评论
  - 通过 comment_id 或 user_id 定位目标评论

- **搜索筛选增强** - `search_feeds` 新增筛选参数
  - `publish_time`: 发布时间（不限|一天内|一周内|半年内）
  - `search_scope`: 搜索范围（不限|已看过|未看过|已关注）
  - `location`: 位置距离（不限|同城|附近）

- **评论加载配置** - `get_feed_detail` 新增高级评论加载参数
  - `load_all_comments`: 滚动加载全部评论
  - `limit`: 限制加载的一级评论数量
  - `click_more_replies`: 展开二级回复
  - `reply_limit`: 跳过回复数过多的评论
  - `scroll_speed`: 滚动速度（slow|normal|fast）

### 改进

- 优化浏览器视口尺寸 (1440x900)，提升页面元素可见性
- 改进错误处理和日志输出
