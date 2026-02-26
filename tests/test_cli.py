"""CLI 命令测试"""

import pytest
from click.testing import CliRunner
from xhs_mcp.cli import main


@pytest.fixture
def runner():
    return CliRunner()


class TestHelp:
    """测试帮助信息"""
    
    def test_main_help(self, runner):
        """测试主命令帮助"""
        result = runner.invoke(main, ['--help'])
        assert '小红书 MCP 工具' in result.output
        assert result.exit_code == 0
    
    def test_login_browser_help(self, runner):
        """测试 login-browser 帮助"""
        result = runner.invoke(main, ['login-browser', '--help'])
        assert '浏览器' in result.output
        assert result.exit_code == 0
    
    def test_login_qrcode_help(self, runner):
        """测试 login-qrcode 帮助"""
        result = runner.invoke(main, ['login-qrcode', '--help'])
        assert '二维码' in result.output
        assert result.exit_code == 0
    
    def test_status_help(self, runner):
        """测试 status 帮助"""
        result = runner.invoke(main, ['status', '--help'])
        assert '登录状态' in result.output
        assert result.exit_code == 0
    
    def test_logout_help(self, runner):
        """测试 logout 帮助"""
        result = runner.invoke(main, ['logout', '--help'])
        assert '退出登录' in result.output
        assert result.exit_code == 0
    
    def test_publish_help(self, runner):
        """测试 publish 帮助"""
        result = runner.invoke(main, ['publish', '--help'])
        assert '发布' in result.output
        assert result.exit_code == 0
    
    def test_serve_help(self, runner):
        """测试 serve 帮助"""
        result = runner.invoke(main, ['serve', '--help'])
        assert 'MCP' in result.output
        assert result.exit_code == 0


class TestCommands:
    """测试命令是否存在"""
    
    def test_all_commands_exist(self, runner):
        """测试所有命令都存在"""
        result = runner.invoke(main, ['--help'])
        # 检查所有命令都在帮助输出中
        commands = [
            'login-browser',
            'login-qrcode', 
            'status',
            'logout',
            'publish',
            'serve'
        ]
        for cmd in commands:
            assert cmd in result.output, f"命令 {cmd} 不存在"
