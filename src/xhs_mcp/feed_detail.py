"""笔记详情模块"""

import asyncio
import json
from typing import Optional
from playwright.async_api import Page
import logging

logger = logging.getLogger(__name__)

from xhs_mcp.browser import BrowserManager
from xhs_mcp.interact import make_feed_detail_url


class FeedDetailAction:
    """获取笔记详情"""
    
    def __init__(self, browser: BrowserManager):
        self.browser = browser
    
    async def get_feed_detail(self, feed_id: str, xsec_token: str, load_comments: bool = False) -> dict:
        """获取笔记详情
        
        Args:
            feed_id: 笔记 ID
            xsec_token: 访问令牌
            load_comments: 是否加载评论
        """
        page = await self.browser.new_page()
        url = make_feed_detail_url(feed_id, xsec_token)
        
        try:
            logger.debug(f"打开笔记详情页: {url}")
            await page.goto(url)
            await page.wait_for_load_state("load")
            await asyncio.sleep(2)
            
            # 等待数据加载
            await page.wait_for_function("() => window.__INITIAL_STATE__ !== undefined", timeout=30000)
            
            # 提取笔记详情
            detail = await self._extract_detail(page, feed_id)
            
            # 加载评论
            if load_comments:
                comments = await self._extract_comments(page)
                detail["comments"] = comments
            
            return detail
        finally:
            await page.close()
    
    async def _extract_detail(self, page: Page, feed_id: str) -> dict:
        """提取笔记详情"""
        result = await page.evaluate("""() => {
            if (window.__INITIAL_STATE__ &&
                window.__INITIAL_STATE__.note &&
                window.__INITIAL_STATE__.note.noteDetailMap) {
                return JSON.stringify(window.__INITIAL_STATE__.note.noteDetailMap);
            }
            return "";
        }""")
        
        if not result:
            return {"feed_id": feed_id, "error": "未找到笔记详情"}
        
        try:
            note_detail_map = json.loads(result)
            detail = note_detail_map.get(feed_id, {})
            note = detail.get("note", {})
            
            # 提取关键信息
            return {
                "feed_id": feed_id,
                "title": note.get("title", ""),
                "desc": note.get("desc", ""),
                "type": note.get("type", ""),
                "time": note.get("time", ""),
                "user": {
                    "user_id": note.get("user", {}).get("userId", ""),
                    "nickname": note.get("user", {}).get("nickname", ""),
                    "avatar": note.get("user", {}).get("avatar", ""),
                },
                "interact_info": {
                    "liked": note.get("interactInfo", {}).get("liked", False),
                    "liked_count": note.get("interactInfo", {}).get("likedCount", "0"),
                    "collected": note.get("interactInfo", {}).get("collected", False),
                    "collected_count": note.get("interactInfo", {}).get("collectedCount", "0"),
                    "comment_count": note.get("interactInfo", {}).get("commentCount", "0"),
                    "share_count": note.get("interactInfo", {}).get("shareCount", "0"),
                },
                "images": [img.get("urlDefault", "") for img in note.get("imageList", [])],
                "tags": [tag.get("name", "") for tag in note.get("tagList", [])],
            }
        except Exception as e:
            logger.error(f"解析笔记详情失败: {e}")
            return {"feed_id": feed_id, "error": str(e)}
    
    async def _extract_comments(self, page: Page) -> list:
        """提取评论列表"""
        result = await page.evaluate("""() => {
            if (window.__INITIAL_STATE__ &&
                window.__INITIAL_STATE__.note &&
                window.__INITIAL_STATE__.note.noteDetailMap) {
                const map = window.__INITIAL_STATE__.note.noteDetailMap;
                const keys = Object.keys(map);
                if (keys.length > 0) {
                    const detail = map[keys[0]];
                    if (detail && detail.comments) {
                        return JSON.stringify(detail.comments);
                    }
                }
            }
            return "[]";
        }""")
        
        try:
            comments_data = json.loads(result)
            comments = []
            for c in comments_data:
                comments.append({
                    "id": c.get("id", ""),
                    "content": c.get("content", ""),
                    "user_id": c.get("userInfo", {}).get("userId", ""),
                    "nickname": c.get("userInfo", {}).get("nickname", ""),
                    "like_count": c.get("likeCount", "0"),
                    "create_time": c.get("createTime", ""),
                })
            return comments
        except Exception as e:
            logger.debug(f"解析评论失败: {e}")
            return []
