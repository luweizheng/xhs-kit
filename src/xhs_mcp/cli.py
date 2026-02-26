"""命令行入口"""

import asyncio
import click
import logging

logger = logging.getLogger(__name__)


@click.group()
def main():
    """小红书 MCP 工具"""
    pass


@main.command()
@click.option("--headless/--no-headless", default=False, help="是否无头模式")
def login_browser(headless: bool):
    """通过浏览器扫码登录小红书（会打开浏览器窗口）"""
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
@click.option("--save", "-s", type=click.Path(), help="保存二维码图片到指定路径")
@click.option("--terminal/--no-terminal", default=True, help="是否在终端显示二维码")
def login_qrcode(save: str, terminal: bool):
    """通过二维码登录（无需打开浏览器窗口）
    
    获取登录二维码，可以保存为图片或在终端显示。
    扫码成功后 cookies 会自动保存。
    """
    import base64
    import io
    import sys
    from xhs_mcp.client import XhsClient
    
    async def _login_qrcode():
        from xhs_mcp.browser import BrowserManager
        from xhs_mcp.login import LoginAction
        
        browser = BrowserManager(headless=True)
        login_action = LoginAction(browser)
        
        try:
            # 检查是否已登录
            status = await login_action.check_login_status()
            if status.is_logged_in:
                click.echo("✅ 已经登录")
                return
            
            click.echo("正在获取二维码...")
            
            # 直接打开页面获取二维码，不使用后台任务
            from playwright.async_api import Page
            page = await browser.new_page()
            await page.goto("https://www.xiaohongshu.com/explore")
            await page.wait_for_load_state("load")
            await asyncio.sleep(2)
            
            # 检查是否已登录
            if await page.locator(".main-container .user .link-wrapper .channel").count() > 0:
                click.echo("✅ 已经登录")
                await page.close()
                return
            
            # 获取二维码
            qrcode_elem = page.locator(".login-container .qrcode-img")
            img_src = await qrcode_elem.get_attribute("src")
            
            if not img_src:
                click.echo("❌ 无法获取二维码")
                await page.close()
                return
            
            # 构造 result 对象
            class QRResult:
                def __init__(self, img, timeout):
                    self.img = img
                    self.timeout = timeout
                    self.is_logged_in = False
            
            result = QRResult(img_src, "240s")
            
            if result.is_logged_in:
                click.echo("✅ 已经登录")
                return
            
            if not result.img:
                click.echo("❌ 无法获取二维码")
                return
            
            # 保存二维码图片
            if save:
                try:
                    from PIL import Image
                    img_base64 = result.img
                    if img_base64.startswith('data:'):
                        img_base64 = img_base64.split(',', 1)[1]
                    img_data = base64.b64decode(img_base64)
                    img = Image.open(io.BytesIO(img_data))
                    img.save(save)
                    click.echo(f"✅ 二维码已保存到: {save}")
                except Exception as e:
                    click.echo(f"❌ 保存图片失败: {e}")
            
            # 在终端显示二维码
            if terminal:
                terminal_displayed = False
                
                # 方法1: 使用 pyzbar 解码（需要 zbar 系统库）
                try:
                    # macOS Homebrew 安装的 zbar 需要设置库路径
                    import os
                    import platform
                    if platform.system() == "Darwin":
                        homebrew_lib = "/opt/homebrew/lib"
                        if os.path.exists(homebrew_lib):
                            current_path = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
                            if homebrew_lib not in current_path:
                                os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = f"{homebrew_lib}:{current_path}"
                    
                    from PIL import Image
                    from pyzbar.pyzbar import decode
                    import qrcode
                    
                    img_base64 = result.img
                    if img_base64.startswith('data:'):
                        img_base64 = img_base64.split(',', 1)[1]
                    img_data = base64.b64decode(img_base64)
                    img = Image.open(io.BytesIO(img_data))
                    
                    # 解码二维码内容
                    decoded = decode(img)
                    if decoded:
                        qr_data = decoded[0].data.decode('utf-8')
                        
                        # 生成终端二维码
                        qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=1,
                            border=2,
                        )
                        qr.add_data(qr_data)
                        qr.make(fit=True)
                        
                        matrix = qr.get_matrix()
                        
                        click.echo("\n" + "="*60)
                        click.echo("请使用小红书 App 扫描以下二维码登录:")
                        click.echo("="*60)
                        
                        # 使用 Unicode 块字符打印
                        for row_idx in range(0, len(matrix), 2):
                            line = ""
                            for col_idx in range(len(matrix[0])):
                                top = matrix[row_idx][col_idx] if row_idx < len(matrix) else False
                                bottom = matrix[row_idx + 1][col_idx] if row_idx + 1 < len(matrix) else False
                                
                                if top and bottom:
                                    line += "█"
                                elif top and not bottom:
                                    line += "▀"
                                elif not top and bottom:
                                    line += "▄"
                                else:
                                    line += " "
                            click.echo(line)
                        
                        terminal_displayed = True
                except ImportError:
                    pass
                except Exception:
                    pass
                
                # 方法2: 如果 pyzbar 不可用，提示用户查看保存的图片
                if not terminal_displayed:
                    if not save:
                        # 自动保存到临时文件
                        import tempfile
                        import os
                        temp_path = os.path.join(tempfile.gettempdir(), "xhs_qrcode.png")
                        try:
                            from PIL import Image
                            img_base64 = result.img
                            if img_base64.startswith('data:'):
                                img_base64 = img_base64.split(',', 1)[1]
                            img_data = base64.b64decode(img_base64)
                            img = Image.open(io.BytesIO(img_data))
                            img.save(temp_path)
                            click.echo(f"⚠️  终端显示需要 zbar 库，二维码已保存到: {temp_path}")
                            click.echo("macOS 安装: brew install zbar")
                            click.echo("Ubuntu 安装: sudo apt-get install libzbar0")
                        except Exception as e:
                            click.echo(f"❌ 无法显示二维码: {e}")
                    else:
                        click.echo(f"⚠️  终端显示需要 zbar 库，请查看保存的图片: {save}")
            
            click.echo(f"⏳ 等待扫码登录（超时: {result.timeout}）...")
            click.echo("扫码成功后 cookies 会自动保存")
            
            # 等待登录完成 - 直接在当前页面检测
            timeout_seconds = 240
            login_success_selector = ".main-container .user .link-wrapper .channel"
            for i in range(timeout_seconds * 2):  # 每 0.5 秒检查一次
                await asyncio.sleep(0.5)
                if await page.locator(login_success_selector).count() > 0:
                    click.echo("✅ 登录成功！正在保存 cookies...")
                    await browser.save_cookies(page)
                    click.echo("✅ cookies 已保存")
                    await page.close()
                    return
                # 每 30 秒提示一次
                if i > 0 and i % 60 == 0:
                    remaining = timeout_seconds - i // 2
                    click.echo(f"⏳ 继续等待扫码... 剩余 {remaining} 秒")
            
            click.echo("❌ 登录超时，请重试")
            await page.close()
        finally:
            await browser.close()
    
    asyncio.run(_login_qrcode())


@main.command()
@click.option("--title", "-t", required=True, help="文字标题")
@click.option("--content", "-c", required=True, help="文字正文内容")
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
@click.option("--title", "-t", required=True, help="文字标题")
@click.option("--content", "-c", required=True, help="文字正文内容")
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
@click.option("--cover", "-c", required=True, help="封面文字")
@click.option("--page", "-p", multiple=True, help="正文页文字（可多次指定，最多17页）")
@click.option("--style", "-s", default="基础", help="卡片样式：基础|边框|备忘|手写|便签|涂写|简约|光影|几何")
@click.option("--title", "-t", default="", help="文字标题")
@click.option("--content", default="", help="文字正文内容")
@click.option("--tag", multiple=True, help="标签（可多次指定）")
@click.option("--headless/--no-headless", default=True, help="是否无头模式")
def publish_text_card(cover: str, page: tuple, style: str, title: str, content: str, tag: tuple, headless: bool):
    """发布文字配图笔记"""
    from xhs_mcp.client import XhsClient
    
    async def _publish():
        async with XhsClient(headless=headless) as client:
            if not await client.is_logged_in():
                click.echo("❌ 请先登录")
                return
            
            click.echo(f"正在发布文字配图: {cover[:20]}...")
            result = await client.publish_text_card(
                cover_text=cover,
                pages=list(page) if page else None,
                style=style,
                title=title,
                content=content,
                tags=list(tag) if tag else None
            )
            click.echo(f"✅ {result.status}: {result.message}")
    
    asyncio.run(_publish())


@main.command()
@click.option("--headless/--no-headless", default=True, help="是否无头模式")
def serve(headless: bool):
    """启动 MCP 服务（stdio 模式）"""
    from xhs_mcp.mcp_server import run_server
    run_server(headless=headless)


if __name__ == "__main__":
    main()
