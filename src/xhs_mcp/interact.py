"""互动模块：点赞、收藏、评论"""

import asyncio
import json
from typing import Optional
from playwright.async_api import Page
import logging

logger = logging.getLogger(__name__)

from xhs_mcp.browser import BrowserManager


# 选择器常量
SELECTOR_LIKE_BUTTON = ".interact-container .left .like-lottie"
SELECTOR_COLLECT_BUTTON = ".interact-container .left .reds-icon.collect-icon"


def make_feed_detail_url(feed_id: str, xsec_token: str) -> str:
    """构建笔记详情页 URL"""
    return f"https://www.xiaohongshu.com/explore/{feed_id}?xsec_token={xsec_token}&xsec_source=pc_feed"


class InteractAction:
    """互动操作基类"""
    
    def __init__(self, browser: BrowserManager):
        self.browser = browser
    
    async def _prepare_page(self, feed_id: str, xsec_token: str) -> Page:
        """准备页面，导航到笔记详情"""
        page = await self.browser.new_page()
        url = make_feed_detail_url(feed_id, xsec_token)
        logger.debug(f"打开笔记详情页: {url}")
        
        await page.goto(url)
        await page.wait_for_load_state("load")
        await asyncio.sleep(2)
        
        return page
    
    async def _get_interact_state(self, page: Page, feed_id: str) -> tuple[bool, bool]:
        """获取点赞/收藏状态
        
        Returns:
            (liked, collected) 元组
        """
        result = await page.evaluate("""() => {
            if (window.__INITIAL_STATE__ &&
                window.__INITIAL_STATE__.note &&
                window.__INITIAL_STATE__.note.noteDetailMap) {
                return JSON.stringify(window.__INITIAL_STATE__.note.noteDetailMap);
            }
            return "";
        }""")
        
        if not result:
            return False, False
        
        try:
            note_detail_map = json.loads(result)
            detail = note_detail_map.get(feed_id, {})
            note = detail.get("note", {})
            interact_info = note.get("interactInfo", {})
            return interact_info.get("liked", False), interact_info.get("collected", False)
        except Exception as e:
            logger.debug(f"解析互动状态失败: {e}")
            return False, False


class LikeAction(InteractAction):
    """点赞操作"""
    
    async def like(self, feed_id: str, xsec_token: str) -> dict:
        """点赞笔记"""
        return await self._perform(feed_id, xsec_token, target_liked=True)
    
    async def unlike(self, feed_id: str, xsec_token: str) -> dict:
        """取消点赞"""
        return await self._perform(feed_id, xsec_token, target_liked=False)
    
    async def _perform(self, feed_id: str, xsec_token: str, target_liked: bool) -> dict:
        action_name = "点赞" if target_liked else "取消点赞"
        page = await self._prepare_page(feed_id, xsec_token)
        
        try:
            # 获取当前状态
            liked, _ = await self._get_interact_state(page, feed_id)
            
            # 检查是否需要操作
            if target_liked and liked:
                logger.info(f"笔记 {feed_id} 已点赞，跳过")
                return {"feed_id": feed_id, "success": True, "message": "已点赞"}
            if not target_liked and not liked:
                logger.info(f"笔记 {feed_id} 未点赞，跳过")
                return {"feed_id": feed_id, "success": True, "message": "未点赞"}
            
            # 点击点赞按钮
            await page.click(SELECTOR_LIKE_BUTTON)
            await asyncio.sleep(2)
            
            logger.info(f"笔记 {feed_id} {action_name}成功")
            return {"feed_id": feed_id, "success": True, "message": f"{action_name}成功"}
        finally:
            await page.close()


class FavoriteAction(InteractAction):
    """收藏操作"""
    
    async def favorite(self, feed_id: str, xsec_token: str) -> dict:
        """收藏笔记"""
        return await self._perform(feed_id, xsec_token, target_collected=True)
    
    async def unfavorite(self, feed_id: str, xsec_token: str) -> dict:
        """取消收藏"""
        return await self._perform(feed_id, xsec_token, target_collected=False)
    
    async def _perform(self, feed_id: str, xsec_token: str, target_collected: bool) -> dict:
        action_name = "收藏" if target_collected else "取消收藏"
        page = await self._prepare_page(feed_id, xsec_token)
        
        try:
            # 获取当前状态
            _, collected = await self._get_interact_state(page, feed_id)
            
            # 检查是否需要操作
            if target_collected and collected:
                logger.info(f"笔记 {feed_id} 已收藏，跳过")
                return {"feed_id": feed_id, "success": True, "message": "已收藏"}
            if not target_collected and not collected:
                logger.info(f"笔记 {feed_id} 未收藏，跳过")
                return {"feed_id": feed_id, "success": True, "message": "未收藏"}
            
            # 点击收藏按钮
            await page.click(SELECTOR_COLLECT_BUTTON)
            await asyncio.sleep(2)
            
            logger.info(f"笔记 {feed_id} {action_name}成功")
            return {"feed_id": feed_id, "success": True, "message": f"{action_name}成功"}
        finally:
            await page.close()


class CommentAction(InteractAction):
    """评论操作"""
    
    async def post_comment(self, feed_id: str, xsec_token: str, content: str) -> dict:
        """发表评论"""
        page = await self._prepare_page(feed_id, xsec_token)
        
        try:
            # 点击评论输入框
            input_box = page.locator("div.input-box div.content-edit span")
            await input_box.click()
            await asyncio.sleep(0.5)
            
            # 输入评论内容
            content_input = page.locator("div.input-box div.content-edit p.content-input")
            await content_input.fill(content)
            await asyncio.sleep(1)
            
            # 点击提交按钮
            submit_btn = page.locator("div.bottom button.submit")
            await submit_btn.click()
            await asyncio.sleep(2)
            
            logger.info(f"评论发表成功: {feed_id}")
            return {"feed_id": feed_id, "success": True, "message": "评论发表成功"}
        except Exception as e:
            logger.error(f"评论发表失败: {e}")
            return {"feed_id": feed_id, "success": False, "message": str(e)}
        finally:
            await page.close()
