from __future__ import annotations

import sys
from urllib.error import URLError
from urllib.request import urlopen

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

URL = "http://127.0.0.1:8083/"


def server_ready() -> bool:
    try:
        with urlopen(URL, timeout=3) as response:
            return response.status < 500
    except URLError:
        return False


def main() -> int:
    if not server_ready():
        print("brand overlap check: SKIP, local web server is not reachable")
        return 0

    with sync_playwright() as p:
        browser = None
        for launch in (
            lambda: p.chromium.launch(headless=True),
            lambda: p.firefox.launch(headless=True),
            lambda: p.chromium.launch(channel="chrome", headless=True),
            lambda: p.chromium.launch(channel="msedge", headless=True),
        ):
            try:
                browser = launch()
                break
            except PlaywrightError:
                continue
        if browser is None:
            print("brand overlap check: SKIP, no browser executable is available")
            return 0

        page = browser.new_page(viewport={"width": 1600, "height": 900})
        page.goto(URL, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_selector(".brand-mark", timeout=10000)
        metrics = page.evaluate(
            """() => {
              const brand = document.querySelector('.brand-mark');
              const rect = brand.getBoundingClientRect();
              const cx = rect.left + rect.width / 2;
              const cy = rect.top + rect.height / 2;
              const stack = document.elementsFromPoint(cx, cy).slice(0, 8).map((el) => ({
                tag: el.tagName,
                id: el.id || '',
                cls: el.className || '',
                text: (el.textContent || '').trim().slice(0, 40),
              }));
              const theme = document.querySelector('#theme-toggle-btn');
              const controls = document.querySelector('.sidebar-footer-controls');
              const themeRect = theme ? theme.getBoundingClientRect() : null;
              const controlsRect = controls ? controls.getBoundingClientRect() : null;
              const controlsStyle = controls ? getComputedStyle(controls) : null;
              return {
                brand: {
                  left: Math.round(rect.left),
                  top: Math.round(rect.top),
                  width: Math.round(rect.width),
                  height: Math.round(rect.height),
                },
                theme: themeRect ? {
                  left: Math.round(themeRect.left),
                  top: Math.round(themeRect.top),
                  width: Math.round(themeRect.width),
                  height: Math.round(themeRect.height),
                } : null,
                controls: controlsRect ? {
                  left: Math.round(controlsRect.left),
                  top: Math.round(controlsRect.top),
                  width: Math.round(controlsRect.width),
                  height: Math.round(controlsRect.height),
                  position: controlsStyle.position,
                  bottom: controlsStyle.bottom,
                  topStyle: controlsStyle.top,
                } : null,
                stack,
              };
            }"""
        )
        browser.close()

    print(metrics)
    theme = metrics.get("theme")
    brand = metrics.get("brand")
    overlap = False
    if theme and brand:
        overlap = not (
            theme["left"] >= brand["left"] + brand["width"]
            or theme["left"] + theme["width"] <= brand["left"]
            or theme["top"] >= brand["top"] + brand["height"]
            or theme["top"] + theme["height"] <= brand["top"]
        )
    if overlap:
        print("[FAIL] theme toggle overlaps brand mark")
        return 1
    print("[PASS] theme toggle does not overlap brand mark")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
