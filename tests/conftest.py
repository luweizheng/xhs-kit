"""pytest 配置和共享 fixtures"""

import pytest
import os
from pathlib import Path


def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--with-browser",
        action="store_true",
        default=False,
        help="运行需要浏览器的测试"
    )
    parser.addoption(
        "--cookies-file",
        action="store",
        default=None,
        help="指定 cookies 文件路径，用于跳过登录"
    )


def pytest_configure(config):
    """配置自定义标记"""
    config.addinivalue_line(
        "markers", "browser: 需要浏览器环境的测试"
    )
    config.addinivalue_line(
        "markers", "logged_in: 需要已登录状态的测试"
    )


def pytest_collection_modifyitems(config, items):
    """根据命令行选项跳过测试"""
    if not config.getoption("--with-browser"):
        skip_browser = pytest.mark.skip(reason="需要 --with-browser 选项")
        for item in items:
            if "browser" in item.keywords:
                item.add_marker(skip_browser)


@pytest.fixture
def cookies_file(request):
    """获取 cookies 文件路径
    
    优先级：
    1. 命令行 --cookies-file 选项
    2. 环境变量 COOKIES_PATH
    3. 项目根目录的 cookies.json
    """
    # 命令行选项
    cli_path = request.config.getoption("--cookies-file")
    if cli_path and Path(cli_path).exists():
        return cli_path
    
    # 环境变量
    env_path = os.environ.get("COOKIES_PATH")
    if env_path and Path(env_path).exists():
        return env_path
    
    # 项目根目录
    project_root = Path(__file__).parent.parent
    default_path = project_root / "cookies.json"
    if default_path.exists():
        return str(default_path)
    
    # 上级目录（post2xhs）
    parent_path = project_root.parent / "cookies.json"
    if parent_path.exists():
        return str(parent_path)
    
    return None


@pytest.fixture
def has_cookies(cookies_file):
    """检查是否有可用的 cookies"""
    return cookies_file is not None


@pytest.fixture
def skip_if_no_cookies(cookies_file):
    """如果没有 cookies 则跳过测试"""
    if cookies_file is None:
        pytest.skip("没有可用的 cookies 文件，请先登录或指定 --cookies-file")
