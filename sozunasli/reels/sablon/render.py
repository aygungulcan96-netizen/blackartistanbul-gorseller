import sys, asyncio
from playwright.async_api import async_playwright
FPS=30; DUR=float(__import__("os").environ.get("DUR","22.5"))
async def main(html, outdir, only=None):
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto("file://"+html); await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(500)
        await pg.evaluate("document.getAnimations().forEach(a=>a.pause())")
        frames = [int(x*FPS) for x in only] if only else range(int(DUR*FPS))
        for i in frames:
            await pg.evaluate(f"document.getAnimations().forEach(a=>a.currentTime={i*1000/FPS})")
            await pg.screenshot(path=f"{outdir}/f{i:04d}.png")
        await b.close()
only = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv)>3 else None
asyncio.run(main(sys.argv[1], sys.argv[2], only))
