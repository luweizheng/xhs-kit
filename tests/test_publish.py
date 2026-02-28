"""发布功能测试"""

import pytest
from xhs_kit.po.client import XhsClient
from xhs_kit.po.models import PublishImageContent


@pytest.mark.skip(reason="需要登录后手动测试")
@pytest.mark.asyncio
async def test_publish_image():
    """测试发布图文"""
    async with XhsClient(headless=False) as client:
        result = await client.publish(
            title="Hello World",
            content="这是测试内容",
            images=["/tmp/1.jpg"],
            tags=["测试"]
        )
        assert result.status == "发布完成"


@pytest.mark.skip(reason="需要登录后手动测试")
@pytest.mark.asyncio
async def test_publish_video():
    """测试发布视频"""
    async with XhsClient(headless=False) as client:
        result = await client.publish_video(
            title="视频测试",
            content="这是视频测试内容",
            video="/tmp/test.mp4",
            tags=["测试"]
        )
        assert result.status == "发布完成"
