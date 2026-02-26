"""Cookie 管理测试"""

import pytest
import json
from pathlib import Path
from xhs_mcp.cookies import CookieManager


def test_save_and_load_cookies(tmp_path):
    """测试保存和加载 cookies"""
    cookie_file = tmp_path / "test_cookies.json"
    manager = CookieManager(path=cookie_file)
    
    # 测试保存
    test_cookies = [
        {"name": "test", "value": "123", "domain": ".xiaohongshu.com"}
    ]
    manager.save_cookies(test_cookies)
    
    assert cookie_file.exists()
    
    # 测试加载
    loaded = manager.load_cookies()
    assert loaded == test_cookies


def test_load_nonexistent_cookies(tmp_path):
    """测试加载不存在的 cookies"""
    cookie_file = tmp_path / "nonexistent.json"
    manager = CookieManager(path=cookie_file)
    
    result = manager.load_cookies()
    assert result is None


def test_delete_cookies(tmp_path):
    """测试删除 cookies"""
    cookie_file = tmp_path / "test_cookies.json"
    manager = CookieManager(path=cookie_file)
    
    # 先创建文件
    manager.save_cookies([{"name": "test", "value": "123"}])
    assert cookie_file.exists()
    
    # 删除
    manager.delete_cookies()
    assert not cookie_file.exists()


def test_delete_nonexistent_cookies(tmp_path):
    """测试删除不存在的 cookies（不应报错）"""
    cookie_file = tmp_path / "nonexistent.json"
    manager = CookieManager(path=cookie_file)
    
    # 不应抛出异常
    manager.delete_cookies()
