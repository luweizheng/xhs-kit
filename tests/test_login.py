"""登录功能测试"""

import pytest
from xhs_mcp.client import XhsClient


@pytest.mark.skip(reason="需要手动扫码测试")
@pytest.mark.asyncio
async def test_check_login_status():
    """测试检查登录状态"""
    async with XhsClient(headless=True) as client:
        status = await client.check_login_status()
        # 只验证返回结构正确
        assert hasattr(status, "is_logged_in")


@pytest.mark.skip(reason="需要手动扫码测试")
@pytest.mark.asyncio
async def test_login_interactive():
    """测试交互式登录"""
    async with XhsClient(headless=False) as client:
        success = await client.login()
        assert success is True


@pytest.mark.skip(reason="需要手动扫码测试")
@pytest.mark.asyncio
async def test_get_login_qrcode():
    """测试获取登录二维码"""
    async with XhsClient(headless=True) as client:
        result = await client.get_login_qrcode()
        assert hasattr(result, "timeout")
        assert hasattr(result, "is_logged_in")
        if not result.is_logged_in:
            assert result.img is not None
