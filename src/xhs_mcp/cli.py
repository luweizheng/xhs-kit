"""命令行入口"""

import asyncio
import click
from loguru import logger


@click.group()
def main():
    """小红书 MCP 工具"""
    pass


@main.command()
@click.option("--headless/--no-headless", default=False, help="是否无头模式")
def login(headless: bool):
    """扫码登录小红书"""
    from xhs_mcp.client import XhsClient
    
    async def _login():
        async with XhsClient(headless=headless) as client:
            if await client.is_logged_in():
                click.echo("✅ 已经登录")
                return
            
            click.echo("请扫描二维码登录...")
            success = await client.login()
            if success:
                click.echo("✅ 登录成功")
            else:
                click.echo("❌ 登录失败或超时")
    
    asyncio.run(_login())


@main.command()
@click.option("--headless/--no-headless", default=True, help="是否无头模式")
def status(headless: bool):
    """检查登录状态"""
    from xhs_mcp.client import XhsClient
    
    async def _status():
        async with XhsClient(headless=headless) as client:
            status = await client.check_login_status()
            if status.is_logged_in:
                click.echo(f"✅ 已登录")
            else:
                click.echo("❌ 未登录")
    
    asyncio.run(_status())


@main.command()
def logout():
    """退出登录（删除 cookies）"""
    from xhs_mcp.client import XhsClient
    
    client = XhsClient()
    client.delete_cookies()
    click.echo("✅ 已退出登录")


@main.command()
@click.option("--title", "-t", required=True, help="标题")
@click.option("--content", "-c", required=True, help="正文内容")
@click.option("--image", "-i", multiple=True, required=True, help="图片路径（可多次指定）")
@click.option("--tag", multiple=True, help="标签（可多次指定）")
@click.option("--headless/--no-headless", default=True, help="是否无头模式")
def publish(title: str, content: str, image: tuple, tag: tuple, headless: bool):
    """发布图文内容"""
    from xhs_mcp.client import XhsClient
    
    async def _publish():
        async with XhsClient(headless=headless) as client:
            if not await client.is_logged_in():
                click.echo("❌ 请先登录")
                return
            
            click.echo(f"正在发布: {title}")
            result = await client.publish(
                title=title,
                content=content,
                images=list(image),
                tags=list(tag) if tag else None
            )
            click.echo(f"✅ {result.status}")
    
    asyncio.run(_publish())


@main.command()
@click.option("--title", "-t", required=True, help="标题")
@click.option("--content", "-c", required=True, help="正文内容")
@click.option("--video", "-v", required=True, help="视频路径")
@click.option("--tag", multiple=True, help="标签（可多次指定）")
@click.option("--headless/--no-headless", default=True, help="是否无头模式")
def publish_video(title: str, content: str, video: str, tag: tuple, headless: bool):
    """发布视频内容"""
    from xhs_mcp.client import XhsClient
    
    async def _publish():
        async with XhsClient(headless=headless) as client:
            if not await client.is_logged_in():
                click.echo("❌ 请先登录")
                return
            
            click.echo(f"正在发布视频: {title}")
            result = await client.publish_video(
                title=title,
                content=content,
                video=video,
                tags=list(tag) if tag else None
            )
            click.echo(f"✅ {result.status}")
    
    asyncio.run(_publish())


@main.command()
@click.option("--keyword", "-k", required=True, help="搜索关键词")
@click.option("--headless/--no-headless", default=True, help="是否无头模式")
def search(keyword: str, headless: bool):
    """搜索小红书内容"""
    from xhs_mcp.client import XhsClient
    
    async def _search():
        async with XhsClient(headless=headless) as client:
            click.echo(f"正在搜索: {keyword}")
            result = await client.search(keyword)
            click.echo(f"找到 {result.count} 条结果:\n")
            for i, feed in enumerate(result.feeds[:10], 1):
                click.echo(f"{i}. {feed.display_title}")
                click.echo(f"   作者: {feed.nickname} | 点赞: {feed.liked_count}")
                click.echo(f"   ID: {feed.id}")
                click.echo()
    
    asyncio.run(_search())


@main.command()
@click.option("--headless/--no-headless", default=True, help="是否无头模式")
def serve(headless: bool):
    """启动 MCP 服务（stdio 模式）"""
    from xhs_mcp.mcp_server import run_server
    
    click.echo("启动 MCP 服务...")
    asyncio.run(run_server(headless=headless))


if __name__ == "__main__":
    main()
