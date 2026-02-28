import os

import pytest

from xhs_kit.po.browser import BrowserManager


def test_non_headless_disallowed_by_default(monkeypatch):
    monkeypatch.delenv("XHS_ALLOW_NON_HEADLESS", raising=False)
    with pytest.raises(RuntimeError):
        BrowserManager(headless=False)


def test_non_headless_allowed_when_env_set(monkeypatch):
    monkeypatch.setenv("XHS_ALLOW_NON_HEADLESS", "1")
    BrowserManager(headless=False)
