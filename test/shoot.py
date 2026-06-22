import asyncio
from playwright.async_api import async_playwright

TABS = ["reg", "session", "upi", "settings"]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        await pg.goto("http://127.0.0.1:8099/", wait_until="domcontentloaded")
        await pg.wait_for_timeout(1500)
        for t in TABS:
            try:
                await pg.click(f'.tab-btn[data-tab="{t}"]', timeout=3000)
                await pg.wait_for_timeout(700)
            except Exception as e:
                print("tab", t, "click fail:", repr(e)[:80])
            await pg.screenshot(path=f"test/_shot_{t}.png")
            print("shot:", t)
        await b.close()

asyncio.run(main())
