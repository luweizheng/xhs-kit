"""MCP Server 工具测试"""

import pytest
import os
from unittest.mock import patch, AsyncMock, MagicMock


class TestCheckLoginStatus:
    """测试 check_login_status MCP 工具"""
    
    @pytest.mark.asyncio
    async def test_check_login_status_logged_in(self, tmp_path, monkeypatch):
        """测试已登录状态"""
        from xhs_kit.po.mcp_server import check_login_status

        cookies_file = tmp_path / "cookies.json"
        cookies_file.write_text("[]")
        monkeypatch.setenv("COOKIES_PATH", str(cookies_file))

        result = await check_login_status()

        assert result["is_logged_in"] is True
        assert result["username"] is None
    
    @pytest.mark.asyncio
    async def test_check_login_status_not_logged_in(self, tmp_path, monkeypatch):
        """测试未登录状态"""
        from xhs_kit.po.mcp_server import check_login_status

        cookies_file = tmp_path / "cookies.json"
        monkeypatch.setenv("COOKIES_PATH", str(cookies_file))

        result = await check_login_status()

        assert result["is_logged_in"] is False


class TestLoginWithBrowser:
    """测试 login_with_browser MCP 工具"""
    
    @pytest.mark.skip(reason="需要浏览器环境，难以 mock")
    @pytest.mark.asyncio
    async def test_login_with_browser(self):
        """测试浏览器登录（需要手动测试）"""
        from xhs_kit.po.mcp_server import login_with_browser
        result = await login_with_browser()
        assert "is_logged_in" in result
        assert "message" in result


class TestGetLoginQrcode:
    """测试 get_login_qrcode MCP 工具"""
    
    @pytest.mark.asyncio
    async def test_get_login_qrcode(self):
        """测试获取二维码"""
        from xhs_kit.po.mcp_server import get_login_qrcode
        
        with patch('xhs_mcp.mcp_server.get_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_result = MagicMock()
            mock_result.timeout = "240s"
            mock_result.is_logged_in = False
            mock_result.img = "data:image/png;base64,test"
            mock_client.get_login_qrcode.return_value = mock_result
            mock_get_client.return_value = mock_client
            
            result = await get_login_qrcode()
            
            assert result["timeout"] == "240s"
            assert result["is_logged_in"] is False
            assert result["img"] == "data:image/png;base64,test"


class TestDeleteCookies:
    """测试 delete_cookies MCP 工具"""
    
    @pytest.mark.asyncio
    async def test_delete_cookies(self):
        """测试删除 cookies"""
        from xhs_kit.po.mcp_server import delete_cookies
        
        with patch('xhs_mcp.mcp_server.get_client') as mock_get_client:
            mock_client = MagicMock()
            mock_get_client.return_value = mock_client
            
            result = await delete_cookies()
            
            assert result["success"] is True
            mock_client.delete_cookies.assert_called_once()
