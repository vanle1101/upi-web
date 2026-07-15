from __future__ import annotations

import sys
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


def _server_ready() -> bool:
    try:
        with urlopen(URL, timeout=3) as response:
            return response.status < 500
    except URLError:
        return False


def main() -> int:
    if not _server_ready():
        print("ui interaction smoke: SKIP, local web server is not reachable")
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
            print("ui interaction smoke: SKIP, no browser executable is available")
            return 0

        page = browser.new_page(viewport={"width": 1600, "height": 900})
        page.goto(URL, wait_until="domcontentloaded", timeout=15000)
        page.click('.tab-btn[data-tab="reg"]')
        page.wait_for_selector("#mail-mode-select", state="attached", timeout=10000)
        page.wait_for_selector("#mail-mode-select + .mac-select-trigger", timeout=10000)

        metrics = page.evaluate(
            """() => {
              const select = document.querySelector('#mail-mode-select');
              const trigger = select && select.parentElement
                ? select.parentElement.querySelector('.mac-select-trigger')
                : null;
              if (!select || !trigger) return { ok: false, reason: 'missing trigger' };
              trigger.click();
              const dropdown = document.querySelector('.mac-select-dropdown.is-open');
              if (!dropdown) return { ok: false, reason: 'dropdown not open' };
              const triggerRect = trigger.getBoundingClientRect();
              const dropdownRect = dropdown.getBoundingClientRect();
              const option = [...dropdown.querySelectorAll('.mac-select-option')]
                .find((item) => /icloud/i.test(item.textContent))
                || dropdown.querySelector('.mac-select-option:nth-child(2)')
                || dropdown.querySelector('.mac-select-option');
              const before = select.value;
              const beforeText = trigger.textContent.trim();
              const optionText = option ? option.textContent.trim() : '';
              if (option) option.click();
              const afterText = trigger.textContent.trim();
              const initialScrollY = window.scrollY;
              const initialWorkspaceScroll = document.querySelector('.tab-content.active')?.scrollTop || 0;
              const detailButton = document.querySelector('.tab-content.active [data-dock-collapse]');
              if (detailButton) detailButton.click();
              const dock = document.querySelector('.tab-content.active .diagnostics-dock');
              const dockRect = dock ? dock.getBoundingClientRect() : null;
              const afterScrollY = window.scrollY;
              const afterWorkspaceScroll = document.querySelector('.tab-content.active')?.scrollTop || 0;
              const tabResults = [];
              const overlaps = (a, b) => {
                if (!a || !b) return false;
                return a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
              };
              for (const tabName of ['reg', 'session', 'upi', 'getacc', 'settings']) {
                const tabButton = document.querySelector(`.tab-btn[data-tab="${tabName}"]`);
                if (tabButton) tabButton.click();
                const active = document.querySelector('.tab-content.active');
                const activeRect = active.getBoundingClientRect();
                const actionBars = [...active.querySelectorAll('.card-actions')];
                const worstActionBottom = actionBars.reduce((max, bar) => {
                  const rect = bar.getBoundingClientRect();
                  return Math.max(max, Math.round(rect.bottom));
                }, 0);
                const surfaceSelectors = [
                  '.workspace-mast',
                  '.metric-strip',
                  '.workspace-grid',
                  '.settings-workspace',
                  '.control-surface',
                  '.jobs-surface',
                  '.diagnostics-dock',
                  '.insights-rail',
                  '.settings-section.active',
                  '.settings-sidebar',
                ];
                const surfaces = surfaceSelectors
                  .flatMap((selector) => [...active.querySelectorAll(selector)])
                  .filter((node) => {
                    const style = getComputedStyle(node);
                    const rect = node.getBoundingClientRect();
                    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
                  })
                  .map((node) => {
                    const rect = node.getBoundingClientRect();
                    return {
                      selector: node.className || node.id || node.tagName,
                      top: Math.round(rect.top),
                      right: Math.round(rect.right),
                      bottom: Math.round(rect.bottom),
                      left: Math.round(rect.left),
                    };
                  });
                const hiddenSurfaces = surfaces.filter((rect) => (
                  rect.left < -2 ||
                  rect.top < -2 ||
                  rect.right > window.innerWidth + 2 ||
                  rect.bottom > window.innerHeight + 2
                ));
                const actionOverlaps = actionBars.some((bar) => {
                  const count = bar.querySelector('.muted');
                  if (!count) return false;
                  const countRect = count.getBoundingClientRect();
                  return [...bar.querySelectorAll('button')].some((button) => overlaps(button.getBoundingClientRect(), countRect));
                });
                tabResults.push({
                  tabName,
                  activeRight: Math.round(activeRect.right),
                  activeBottom: Math.round(activeRect.bottom),
                  hasHorizontalOverflow: document.documentElement.scrollWidth > window.innerWidth + 2 || document.body.scrollWidth > window.innerWidth + 2,
                  worstActionBottom,
                  hiddenSurfaces,
                  actionOverlaps,
                  viewportHeight: window.innerHeight,
                  viewportWidth: window.innerWidth,
                });
              }
              return {
                ok: true,
                before,
                after: select.value,
                beforeText,
                afterText,
                optionText,
                dockExpanded: dock ? !dock.classList.contains('is-collapsed') : false,
                dockBottom: dockRect ? Math.round(dockRect.bottom) : 0,
                viewportHeight: window.innerHeight,
                initialScrollY,
                afterScrollY,
                initialWorkspaceScroll,
                afterWorkspaceScroll,
                tabResults,
                dropdownLeft: Math.round(dropdownRect.left),
                dropdownTop: Math.round(dropdownRect.top),
                triggerLeft: Math.round(triggerRect.left),
                triggerBottom: Math.round(triggerRect.bottom),
                dropdownVisible: dropdown.classList.contains('is-open'),
              };
            }"""
        )
        browser.close()

    checks = [
        (metrics.get("ok"), f"custom select opens ({metrics.get('reason', 'ok')})"),
        (abs(metrics.get("dropdownLeft", -999) - metrics.get("triggerLeft", 999)) <= 6, "dropdown aligns with trigger"),
        (metrics.get("dropdownTop", 0) >= metrics.get("triggerBottom", 0) - 8, "dropdown opens near the clicked control"),
        (not metrics.get("dropdownVisible"), "dropdown closes after option click"),
        (metrics.get("afterText") == metrics.get("optionText") or metrics.get("after") != metrics.get("before"), "selected label updates after option click"),
        (metrics.get("dockExpanded"), "show details expands diagnostics dock"),
        (metrics.get("dockBottom", 0) <= metrics.get("viewportHeight", 0) + 2, "expanded diagnostics dock stays inside viewport"),
        (metrics.get("afterScrollY", 0) <= metrics.get("initialScrollY", 0) + 2, "expanding diagnostics does not push window downward"),
        (metrics.get("afterWorkspaceScroll", 0) <= metrics.get("initialWorkspaceScroll", 0) + 2, "expanding diagnostics does not push workspace downward"),
        (all(not item["hasHorizontalOverflow"] for item in metrics.get("tabResults", [])), "main tabs avoid horizontal clipping"),
        (all(item["worstActionBottom"] <= item["viewportHeight"] + 2 for item in metrics.get("tabResults", [])), "main tab action bars stay inside viewport"),
        (all(item["activeRight"] <= item["viewportWidth"] + 2 and item["activeBottom"] <= item["viewportHeight"] + 2 for item in metrics.get("tabResults", [])), "all active tabs fit inside viewport"),
        (all(not item["hiddenSurfaces"] for item in metrics.get("tabResults", [])), "all tab panels stay visible"),
        (all(not item["actionOverlaps"] for item in metrics.get("tabResults", [])), "action counters do not overlap buttons"),
    ]

    failed = 0
    for ok, label in checks:
        if ok:
            print(f"[PASS] {label}")
        else:
            print(f"[FAIL] {label}: {metrics}")
            failed += 1

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
