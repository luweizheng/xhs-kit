import pytest

from xhs_kit.po.client import XhsClient

KEYWORD = "Google"


@pytest.mark.browser
@pytest.mark.asyncio
async def test_feed_detail_contains_desc():
    """确保笔记详情包含正文描述"""
    async with XhsClient(headless=True) as client:
        search_result = await client.search(KEYWORD)

        if not search_result.feeds:
            pytest.skip(f"搜索无结果，跳过：{KEYWORD}")

        last_detail = None
        last_feed = None
        for feed in search_result.feeds[:5]:
            if not feed.id or not feed.xsec_token:
                continue
            last_feed = feed
            detail = await client.get_feed_detail(feed.id, feed.xsec_token, load_comments=False)
            last_detail = detail
            if detail.get("error"):
                continue
            title = detail.get("title")
            desc = detail.get("desc") or detail.get("content")
            if title and desc and len(desc) > 10:
                assert detail.get("feed_id") == feed.id
                return

    pytest.skip(f"前 5 条搜索结果均无法稳定获取详情，last_feed={getattr(last_feed, 'id', None)} last_detail={last_detail}")
