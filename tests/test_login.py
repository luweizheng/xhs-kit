"""登录功能测试

测试分为两类：
1. 不需要登录的测试：可以直接运行
2. 需要已登录状态的测试：需要先有 cookies 文件

运行方式：
- 运行所有测试：pytest tests/test_login.py
- 运行需要浏览器的测试：pytest tests/test_login.py --with-browser
- 指定 cookies 文件：pytest tests/test_login.py --cookies-file=/path/to/cookies.json
"""

import pytest
import os
from xhs_mcp.client import XhsClient


class TestLoginStatus:
    """登录状态测试（使用已有 cookies）"""
    
    @pytest.mark.asyncio
    async def test_check_login_status_with_cookies(self, cookies_file, skip_if_no_cookies):
        """测试检查登录状态（使用已有 cookies）"""
        # 设置 cookies 路径
        os.environ["COOKIES_PATH"] = cookies_file
        
        async with XhsClient(headless=True) as client:
            status = await client.check_login_status()
            assert hasattr(status, "is_logged_in")
            # 如果有 cookies，应该是已登录状态
            assert status.is_logged_in is True
    
    @pytest.mark.asyncio
    async def test_check_login_status_structure(self, cookies_file):
        """测试登录状态返回结构"""
        if cookies_file:
            os.environ["COOKIES_PATH"] = cookies_file
        
        async with XhsClient(headless=True) as client:
            status = await client.check_login_status()
            # 验证返回结构
            assert hasattr(status, "is_logged_in")
            assert isinstance(status.is_logged_in, bool)


class TestLoginInteractive:
    """交互式登录测试（需要浏览器）"""
    
    @pytest.mark.browser
    @pytest.mark.asyncio
    async def test_login_interactive(self):
        """测试交互式登录（需要 --with-browser）"""
        async with XhsClient(headless=False) as client:
            success = await client.login()
            assert success is True


class TestQrcode:
    """二维码相关测试"""
    
    @pytest.mark.browser
    @pytest.mark.asyncio
    async def test_get_login_qrcode(self):
        """测试获取登录二维码（需要 --with-browser）"""
        async with XhsClient(headless=True) as client:
            result = await client.get_login_qrcode()
            assert hasattr(result, "timeout")
            assert hasattr(result, "is_logged_in")
            if not result.is_logged_in:
                assert result.img is not None
