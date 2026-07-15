from __future__ import annotations

import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass


URL = "http://127.0.0.1:8083/"
SCREENSHOT = Path(__file__).with_name("operations_dashboard_smoke.png")


def _server_ready() -> bool:
    try:
        with urlopen(URL, timeout=3) as response:
            return response.status < 500
    except URLError:
        return False


def main() -> int:
    if not _server_ready():
        print("operations visual smoke: SKIP, local web server is not reachable")
        return 0

    with sync_playwright() as p:
        launch_attempts = (
            lambda: p.chromium.launch(headless=True),
            lambda: p.firefox.launch(headless=True),
            lambda: p.chromium.launch(channel="chrome", headless=True),
            lambda: p.chromium.launch(channel="msedge", headless=True),
        )
        browser = None
        for launch in launch_attempts:
            try:
                browser = launch()
                break
            except PlaywrightError:
                continue
        if browser is None:
            print("operations visual smoke: SKIP, no Playwright or system browser executable is available")
            return 0
        page = browser.new_page(viewport={"width": 1600, "height": 900})
        page.goto(URL, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_selector(".topbar", timeout=10000)
        page.click('.tab-btn[data-tab="reg"]')
        page.screenshot(path=str(SCREENSHOT), full_page=False)

        metrics = page.evaluate(
            """() => {
              const body = document.body;
              const sideRail = document.querySelector('.tab-nav');
              const workspace = document.querySelector('.ops-workspace.active');
              const tabButtons = [...document.querySelectorAll('.tab-btn')];
              const dock = document.querySelector('.tab-content.active .diagnostics-dock');
              const styles = getComputedStyle(body);
              return {
                background: styles.backgroundColor,
                columns: getComputedStyle(body).gridTemplateColumns,
                sideRailWidth: sideRail ? Math.round(sideRail.getBoundingClientRect().width) : 0,
                workspaceLeft: workspace ? Math.round(workspace.getBoundingClientRect().left) : 0,
                tabs: tabButtons.length,
                activeTabs: tabButtons.filter(btn => btn.classList.contains('active')).length,
                hasHorizontalOverflow: body.scrollWidth > window.innerWidth + 2,
                dockHeight: dock ? Math.round(dock.getBoundingClientRect().height) : 0,
              };
            }"""
        )
        browser.close()

    checks = [
        (metrics["tabs"] == 5, f"keeps 5 tabs ({metrics['tabs']})"),
        (metrics["activeTabs"] == 1, f"has one active tab ({metrics['activeTabs']})"),
        (metrics["sideRailWidth"] >= 130, f"side rail width is visible ({metrics['sideRailWidth']}px)"),
        (metrics["workspaceLeft"] >= 220, "workspace starts after side rail"),
        (not metrics["hasHorizontalOverflow"], "no horizontal overflow at desktop viewport"),
        (54 <= metrics["dockHeight"] <= 62, f"diagnostics dock starts collapsed ({metrics['dockHeight']}px)"),
        ("220px" in metrics["columns"], f"body grid columns: {metrics['columns']}"),
    ]

    failed = 0
    for ok, label in checks:
        if ok:
            print(f"[PASS] {label}")
        else:
            print(f"[FAIL] {label}")
            failed += 1

    print(f"operations visual smoke screenshot: {SCREENSHOT}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
