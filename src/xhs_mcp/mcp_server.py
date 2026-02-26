"""MCP 服务端"""

from typing import Optional
from mcp.server.fastmcp import FastMCP
import logging

logger = logging.getLogger(__name__)

from xhs_mcp.client import XhsClient


# 创建 MCP Server
mcp = FastMCP(name="xiaohongshu-mcp")

# 全局客户端实例
_client: Optional[XhsClient] = None
_headless: bool = True


def get_client() -> XhsClient:
    """获取客户端实例"""
    global _client
    if _client is None:
        _client = XhsClient(headless=_headless)
    return _client


@mcp.tool()
async def check_login_status() -> dict:
    """检查小红书登录状态"""
    client = get_client()
    status = await client.check_login_status()
    return {
        "is_logged_in": status.is_logged_in,
        "username": status.username
    }


@mcp.tool()
async def get_login_qrcode() -> dict:
    """获取登录二维码（返回 Base64 图片和超时时间）"""
    client = get_client()
    result = await client.get_login_qrcode()
    return {
        "timeout": result.timeout,
        "is_logged_in": result.is_logged_in,
        "img": result.img
    }


@mcp.tool()
async def delete_cookies() -> dict:
    """删除 cookies 文件，重置登录状态。删除后需要重新登录。"""
    client = get_client()
    client.delete_cookies()
    return {"success": True, "message": "Cookies 已删除"}


@mcp.tool()
async def publish_content(
    title: str,
    content: str,
    images: list[str],
    tags: Optional[list[str]] = None,
    schedule_at: Optional[str] = None
) -> dict:
    """发布小红书图文内容
    
    Args:
        title: 内容标题（小红书限制：最多20个中文字或英文单词）
        content: 正文内容，不包含以#开头的标签内容
        images: 图片路径列表（至少需要1张图片），支持本地绝对路径
        tags: 话题标签列表（可选），如 ["美食", "旅行", "生活"]
        schedule_at: 定时发布时间（可选），ISO8601格式如 2024-01-20T10:30:00+08:00
    """
    from datetime import datetime
    
    client = get_client()
    
    schedule_time = None
    if schedule_at:
        schedule_time = datetime.fromisoformat(schedule_at)
    
    result = await client.publish(
        title=title,
        content=content,
        images=images,
        tags=tags,
        schedule_at=schedule_time
    )
    
    return {
        "title": result.title,
        "content": result.content,
        "images": result.images,
        "status": result.status
    }


@mcp.tool()
async def publish_with_video(
    title: str,
    content: str,
    video: str,
    tags: Optional[list[str]] = None,
    schedule_at: Optional[str] = None
) -> dict:
    """发布小红书视频内容（仅支持本地单个视频文件）
    
    Args:
        title: 内容标题（小红书限制：最多20个中文字或英文单词）
        content: 正文内容，不包含以#开头的标签内容
        video: 本地视频绝对路径（仅支持单个视频文件）
        tags: 话题标签列表（可选），如 ["美食", "旅行", "生活"]
        schedule_at: 定时发布时间（可选），ISO8601格式如 2024-01-20T10:30:00+08:00
    """
    from datetime import datetime
    
    client = get_client()
    
    schedule_time = None
    if schedule_at:
        schedule_time = datetime.fromisoformat(schedule_at)
    
    result = await client.publish_video(
        title=title,
        content=content,
        video=video,
        tags=tags,
        schedule_at=schedule_time
    )
    
    return {
        "title": result.title,
        "content": result.content,
        "video": result.video,
        "status": result.status
    }


@mcp.tool()
async def search_feeds(keyword: str, sort_by: Optional[str] = None, note_type: Optional[str] = None) -> dict:
    """搜索小红书内容
    
    Args:
        keyword: 搜索关键词
        sort_by: 排序方式（可选）: 综合|最新|最多点赞|最多评论|最多收藏
        note_type: 笔记类型（可选）: 不限|视频|图文
    """
    from xhs_mcp.models import FilterOption
    
    client = get_client()
    filters = None
    if sort_by or note_type:
        filters = FilterOption(sort_by=sort_by, note_type=note_type)
    
    result = await client.search(keyword, filters)
    return {
        "count": result.count,
        "feeds": [f.model_dump() for f in result.feeds]
    }


@mcp.tool()
async def list_feeds() -> dict:
    """获取首页推荐列表"""
    client = get_client()
    result = await client.get_feeds()
    return {
        "count": result.count,
        "feeds": [f.model_dump() for f in result.feeds]
    }


@mcp.tool()
async def get_feed_detail(feed_id: str, xsec_token: str, load_comments: bool = False) -> dict:
    """获取笔记详情
    
    Args:
        feed_id: 笔记 ID，从搜索或推荐列表获取
        xsec_token: 访问令牌，从搜索或推荐列表获取
        load_comments: 是否加载评论列表
    """
    client = get_client()
    return await client.get_feed_detail(feed_id, xsec_token, load_comments)


@mcp.tool()
async def get_user_profile(user_id: str, xsec_token: str) -> dict:
    """获取用户主页信息
    
    Args:
        user_id: 用户 ID
        xsec_token: 访问令牌
    """
    client = get_client()
    return await client.get_user_profile(user_id, xsec_token)


@mcp.tool()
async def like_feed(feed_id: str, xsec_token: str, unlike: bool = False) -> dict:
    """点赞或取消点赞笔记
    
    Args:
        feed_id: 笔记 ID
        xsec_token: 访问令牌
        unlike: 是否取消点赞，默认 False 为点赞
    """
    client = get_client()
    if unlike:
        return await client.unlike(feed_id, xsec_token)
    return await client.like(feed_id, xsec_token)


@mcp.tool()
async def favorite_feed(feed_id: str, xsec_token: str, unfavorite: bool = False) -> dict:
    """收藏或取消收藏笔记
    
    Args:
        feed_id: 笔记 ID
        xsec_token: 访问令牌
        unfavorite: 是否取消收藏，默认 False 为收藏
    """
    client = get_client()
    if unfavorite:
        return await client.unfavorite(feed_id, xsec_token)
    return await client.favorite(feed_id, xsec_token)


@mcp.tool()
async def post_comment(feed_id: str, xsec_token: str, content: str) -> dict:
    """发表评论到笔记
    
    Args:
        feed_id: 笔记 ID
        xsec_token: 访问令牌
        content: 评论内容
    """
    client = get_client()
    return await client.comment(feed_id, xsec_token, content)


@mcp.tool()
async def publish_text_card(
    cover_text: str,
    pages: Optional[list[str]] = None,
    style: str = "基础",
    title: str = "",
    content: str = "",
    tags: Optional[list[str]] = None
) -> dict:
    """发布文字配图笔记（将文字生成为卡片图片）
    
    Args:
        cover_text: 封面文字内容
        pages: 正文页列表（最多17页），每页一段文字
        style: 卡片样式，可选：基础|边框|备忘|手写|便签|涂写|简约|光影|几何
        title: 笔记标题
        content: 笔记正文描述
        tags: 话题标签列表
    """
    client = get_client()
    result = await client.publish_text_card(
        cover_text=cover_text,
        pages=pages,
        style=style,
        title=title,
        content=content,
        tags=tags
    )
    return {
        "status": result.status,
        "message": result.message
    }


def init_server(headless: bool = True):
    """初始化服务器"""
    global _headless
    _headless = headless
    logger.info("MCP Server 已初始化")


def run_server(headless: bool = True):
    """运行 MCP 服务器（stdio 模式）"""
    init_server(headless=headless)
    mcp.run(transport="stdio")
