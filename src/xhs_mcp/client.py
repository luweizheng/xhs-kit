"""小红书客户端"""

from typing import Optional
from datetime import datetime

from xhs_mcp.browser import BrowserManager
from xhs_mcp.login import LoginAction
from xhs_mcp.publish import PublishAction
from xhs_mcp.search import SearchAction
from xhs_mcp.feeds import FeedsListAction
from xhs_mcp.feed_detail import FeedDetailAction
from xhs_mcp.user_profile import UserProfileAction
from xhs_mcp.interact import LikeAction, FavoriteAction, CommentAction
from xhs_mcp.text_card import TextCardAction
from xhs_mcp.models import (
    LoginStatus, 
    LoginQrcodeResponse,
    PublishImageContent, 
    PublishVideoContent, 
    PublishResponse,
    FeedsListResponse,
    FilterOption,
)


class XhsClient:
    """小红书客户端
    
    提供登录、发布等功能的统一接口
    """
    
    def __init__(self, headless: bool = True, bin_path: Optional[str] = None):
        """初始化客户端
        
        Args:
            headless: 是否无头模式运行浏览器
            bin_path: 浏览器可执行文件路径（可选）
        """
        self.browser = BrowserManager(headless=headless, bin_path=bin_path)
        self._login_action = LoginAction(self.browser)
        self._publish_action = PublishAction(self.browser)
        self._search_action = SearchAction(self.browser)
        self._feeds_action = FeedsListAction(self.browser)
        self._feed_detail_action = FeedDetailAction(self.browser)
        self._user_profile_action = UserProfileAction(self.browser)
        self._like_action = LikeAction(self.browser)
        self._favorite_action = FavoriteAction(self.browser)
        self._comment_action = CommentAction(self.browser)
        self._text_card_action = TextCardAction(self.browser)
    
    async def check_login_status(self) -> LoginStatus:
        """检查登录状态"""
        return await self._login_action.check_login_status()
    
    async def is_logged_in(self) -> bool:
        """是否已登录"""
        status = await self.check_login_status()
        return status.is_logged_in
    
    async def get_login_qrcode(self) -> LoginQrcodeResponse:
        """获取登录二维码
        
        返回二维码图片数据，扫码后自动保存 cookies
        """
        return await self._login_action.get_login_qrcode()
    
    async def login(self) -> bool:
        """交互式登录
        
        打开浏览器窗口，等待用户扫码登录
        注意：需要 headless=False 才能看到浏览器窗口
        """
        return await self._login_action.login_interactive()
    
    def delete_cookies(self) -> None:
        """删除 cookies，重置登录状态"""
        self.browser.delete_cookies()
    
    async def publish(
        self,
        title: str,
        content: str,
        images: list[str],
        tags: Optional[list[str]] = None,
        schedule_at: Optional[datetime] = None
    ) -> PublishResponse:
        """发布图文内容
        
        Args:
            title: 文字标题（最多20个字）
            content: 文字正文内容
            images: 图片路径列表（至少1张）
            tags: 标签列表（可选，最多10个）
            schedule_at: 定时发布时间（可选，1小时至14天内）
        """
        publish_content = PublishImageContent(
            title=title,
            content=content,
            images=images,
            tags=tags or [],
            schedule_at=schedule_at
        )
        return await self._publish_action.publish_image(publish_content)
    
    async def publish_video(
        self,
        title: str,
        content: str,
        video: str,
        tags: Optional[list[str]] = None,
        schedule_at: Optional[datetime] = None
    ) -> PublishResponse:
        """发布视频内容
        
        Args:
            title: 文字标题（最多20个字）
            content: 文字正文内容
            video: 视频文件路径
            tags: 标签列表（可选，最多10个）
            schedule_at: 定时发布时间（可选，1小时至14天内）
        """
        publish_content = PublishVideoContent(
            title=title,
            content=content,
            video=video,
            tags=tags or [],
            schedule_at=schedule_at
        )
        return await self._publish_action.publish_video(publish_content)
    
    async def search(
        self,
        keyword: str,
        filters: Optional[FilterOption] = None
    ) -> FeedsListResponse:
        """搜索小红书内容
        
        Args:
            keyword: 搜索关键词
            filters: 筛选选项（可选）
        """
        return await self._search_action.search(keyword, filters)
    
    async def get_feeds(self) -> FeedsListResponse:
        """获取首页推荐列表"""
        return await self._feeds_action.get_feeds_list()
    
    async def get_feed_detail(self, feed_id: str, xsec_token: str, load_comments: bool = False) -> dict:
        """获取笔记详情
        
        Args:
            feed_id: 笔记 ID
            xsec_token: 访问令牌
            load_comments: 是否加载评论
        """
        return await self._feed_detail_action.get_feed_detail(feed_id, xsec_token, load_comments)
    
    async def get_feed_detail_with_config(self, feed_id: str, xsec_token: str, config) -> dict:
        """获取笔记详情（带评论加载配置）
        
        Args:
            feed_id: 笔记 ID
            xsec_token: 访问令牌
            config: CommentLoadConfig 评论加载配置
        """
        return await self._feed_detail_action.get_feed_detail_with_config(feed_id, xsec_token, config)
    
    async def get_user_profile(self, user_id: str, xsec_token: str) -> dict:
        """获取用户主页
        
        Args:
            user_id: 用户 ID
            xsec_token: 访问令牌
        """
        return await self._user_profile_action.get_user_profile(user_id, xsec_token)
    
    async def like(self, feed_id: str, xsec_token: str) -> dict:
        """点赞笔记"""
        return await self._like_action.like(feed_id, xsec_token)
    
    async def unlike(self, feed_id: str, xsec_token: str) -> dict:
        """取消点赞"""
        return await self._like_action.unlike(feed_id, xsec_token)
    
    async def favorite(self, feed_id: str, xsec_token: str) -> dict:
        """收藏笔记"""
        return await self._favorite_action.favorite(feed_id, xsec_token)
    
    async def unfavorite(self, feed_id: str, xsec_token: str) -> dict:
        """取消收藏"""
        return await self._favorite_action.unfavorite(feed_id, xsec_token)
    
    async def comment(self, feed_id: str, xsec_token: str, content: str) -> dict:
        """发表评论
        
        Args:
            feed_id: 笔记 ID
            xsec_token: 访问令牌
            content: 评论内容
        """
        return await self._comment_action.post_comment(feed_id, xsec_token, content)
    
    async def reply_comment(
        self, 
        feed_id: str, 
        xsec_token: str, 
        content: str,
        comment_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> dict:
        """回复评论
        
        Args:
            feed_id: 笔记 ID
            xsec_token: 访问令牌
            content: 回复内容
            comment_id: 目标评论 ID（可选）
            user_id: 目标用户 ID（可选）
        """
        return await self._comment_action.reply_comment(
            feed_id, xsec_token, content, comment_id, user_id
        )
    
    async def publish_text_card(
        self,
        cover_text: str,
        pages: Optional[list[str]] = None,
        style: str = "基础",
        title: str = "",
        content: str = "",
        tags: Optional[list[str]] = None
    ) -> PublishResponse:
        """发布文字配图笔记
        
        Args:
            cover_text: 封面文字
            pages: 正文页列表（最多17页）
            style: 卡片样式（基础、边框、备忘、手写、便签、涂写、简约、光影、几何）
            title: 笔记标题
            content: 笔记正文描述
            tags: 话题标签列表
        """
        return await self._text_card_action.publish_text_card(
            cover_text=cover_text,
            pages=pages,
            style=style,
            title=title,
            content=content,
            tags=tags
        )
    
    async def close(self) -> None:
        """关闭客户端，释放资源"""
        await self.browser.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
