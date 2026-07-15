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
TABS = ("reg", "session", "upi", "getacc", "settings")
VIEWPORTS = ((1600, 900), (1920, 900))


def _server_ready() -> bool:
    try:
        with urlopen(URL, timeout=3) as response:
            return response.status < 500
    except URLError:
        return False


def _launch_browser(p):
    for launch in (
        lambda: p.chromium.launch(headless=True),
        lambda: p.firefox.launch(headless=True),
        lambda: p.chromium.launch(channel="chrome", headless=True),
        lambda: p.chromium.launch(channel="msedge", headless=True),
    ):
        try:
            return launch()
        except PlaywrightError:
            continue
    return None


def main() -> int:
    if not _server_ready():
        print("all tab layout check: SKIP, local web server is not reachable")
        return 0

    failures: list[str] = []
    with sync_playwright() as p:
        browser = _launch_browser(p)
        if browser is None:
            print("all tab layout check: SKIP, no browser executable is available")
            return 0

        page = browser.new_page()
        for width, height in VIEWPORTS:
            page.set_viewport_size({"width": width, "height": height})
            page.goto(URL, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_selector(".topbar", timeout=10000)

            for tab in TABS:
                page.click(f'.tab-btn[data-tab="{tab}"]')
                metrics = page.evaluate(
                    """(tabName) => {
                      const active = document.querySelector('.tab-content.active');
                      const rectOf = (node) => {
                        const rect = node.getBoundingClientRect();
                        return {
                          name: node.id || node.className || node.tagName,
                          top: Math.round(rect.top),
                          right: Math.round(rect.right),
                          bottom: Math.round(rect.bottom),
                          left: Math.round(rect.left),
                          width: Math.round(rect.width),
                          height: Math.round(rect.height),
                        };
                      };
                      const selectors = [
                        '.workspace-mast',
                        '.metric-strip',
                        '.workspace-grid',
                        '.settings-workspace',
                        '.control-surface',
                        '.jobs-surface',
                        '.diagnostics-dock',
                        '.insights-rail',
                        '.settings-sidebar',
                        '.settings-section.active',
                      ];
                      const surfaces = selectors
                        .flatMap((selector) => [...active.querySelectorAll(selector)])
                        .filter((node) => {
                          const style = getComputedStyle(node);
                          const rect = node.getBoundingClientRect();
                          return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
                        })
                        .map(rectOf);
                      const hidden = surfaces.filter((rect) => (
                        rect.top < -2 ||
                        rect.left < -2 ||
                        rect.right > window.innerWidth + 2 ||
                        rect.bottom > window.innerHeight + 2
                      ));
                      const overlaps = (a, b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
                      const actionOverlaps = [...active.querySelectorAll('.card-actions')].map((bar) => {
                        const count = bar.querySelector('.muted');
                        if (!count) return null;
                        const countRect = count.getBoundingClientRect();
                        const offender = [...bar.querySelectorAll('button')].find((button) => overlaps(button.getBoundingClientRect(), countRect));
                        return offender ? { count: rectOf(count), button: rectOf(offender) } : null;
                      }).filter(Boolean);
                      const clippedButtons = [...active.querySelectorAll('.card-actions')].flatMap((bar) => {
                        const barRect = bar.getBoundingClientRect();
                        return [...bar.querySelectorAll('button')].map((button) => {
                          const rect = button.getBoundingClientRect();
                          const clipped = (
                            rect.top < barRect.top - 2 ||
                            rect.left < barRect.left - 2 ||
                            rect.right > barRect.right + 2 ||
                            rect.bottom > barRect.bottom + 2 ||
                            rect.bottom > window.innerHeight + 2
                          );
                          return clipped ? { bar: rectOf(bar), button: rectOf(button) } : null;
                        }).filter(Boolean);
                      });
                      const isVisible = (node) => {
                        const style = getComputedStyle(node);
                        const rect = node.getBoundingClientRect();
                        return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
                      };
                      const railOverflow = [...active.querySelectorAll('.insights-rail, .tab-chart-rail, .settings-chart-rail')]
                        .filter(isVisible)
                        .map((rail) => ({
                          rail: rectOf(rail),
                          scrollHeight: rail.scrollHeight,
                          clientHeight: rail.clientHeight,
                          overflowY: getComputedStyle(rail).overflowY,
                        }))
                        .filter((rail) => rail.scrollHeight > rail.clientHeight + 2);
                      const insightClips = [...active.querySelectorAll('.insight-card')]
                        .filter(isVisible)
                        .flatMap((card) => {
                          const cardRect = card.getBoundingClientRect();
                          return [...card.children].map((child) => {
                            const rect = child.getBoundingClientRect();
                            const clipped = (
                              rect.top < cardRect.top - 2 ||
                              rect.left < cardRect.left - 2 ||
                              rect.right > cardRect.right + 2 ||
                              rect.bottom > cardRect.bottom + 2
                            );
                            return clipped ? { card: rectOf(card), child: rectOf(child) } : null;
                          }).filter(Boolean);
                        });
                      const queueLayerIssues = [...active.querySelectorAll('.jobs-surface')]
                        .filter(isVisible)
                        .map((surface) => {
                          const list = surface.querySelector('.job-list');
                          const head = list?.querySelector('.job-table-head');
                          const firstJob = list?.querySelector('.job');
                          if (!list || !head || !firstJob || !isVisible(firstJob)) return null;
                          const listRect = list.getBoundingClientRect();
                          const headRect = head.getBoundingClientRect();
                          const firstRect = firstJob.getBoundingClientRect();
                          const badHead = headRect.top < listRect.top - 2 || headRect.bottom > firstRect.top + 2;
                          const badFirst = firstRect.top < headRect.bottom - 2;
                          return (badHead || badFirst)
                            ? { list: rectOf(list), head: rectOf(head), firstJob: rectOf(firstJob) }
                            : null;
                        })
                        .filter(Boolean);
                      return {
                        tabName,
                        viewport: { width: window.innerWidth, height: window.innerHeight },
                        active: rectOf(active),
                        hidden,
                        actionOverlaps,
                        clippedButtons,
                        railOverflow,
                        insightClips,
                        queueLayerIssues,
                        horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth + 2 || document.body.scrollWidth > window.innerWidth + 2,
                      };
                    }""",
                    tab,
                )

                if metrics["horizontalOverflow"]:
                    failures.append(f"{width}x{height} {tab}: horizontal overflow")
                if metrics["active"]["bottom"] > height + 2 or metrics["active"]["right"] > width + 2:
                    failures.append(f"{width}x{height} {tab}: active tab clipped {metrics['active']}")
                if metrics["hidden"]:
                    failures.append(f"{width}x{height} {tab}: hidden surfaces {metrics['hidden']}")
                if metrics["actionOverlaps"]:
                    failures.append(f"{width}x{height} {tab}: action overlap {metrics['actionOverlaps']}")
                if metrics["clippedButtons"]:
                    failures.append(f"{width}x{height} {tab}: clipped action buttons {metrics['clippedButtons']}")
                if metrics["railOverflow"]:
                    failures.append(f"{width}x{height} {tab}: right rail needs internal scroll {metrics['railOverflow']}")
                if metrics["insightClips"]:
                    failures.append(f"{width}x{height} {tab}: insight card content clipped {metrics['insightClips']}")
                if metrics["queueLayerIssues"]:
                    failures.append(f"{width}x{height} {tab}: queue header/row overlap {metrics['queueLayerIssues']}")

                dock_count = page.locator(".tab-content.active .diagnostics-dock").count()
                if dock_count:
                    before = page.evaluate(
                        """() => ({
                          windowY: window.scrollY,
                          activeY: document.querySelector('.tab-content.active')?.scrollTop || 0
                        })"""
                    )
                    for index in range(page.locator(".tab-content.active .dock-tab").count()):
                        page.locator(".tab-content.active .dock-tab").nth(index).click()
                        after = page.evaluate(
                            """() => {
                              const dock = document.querySelector('.tab-content.active .diagnostics-dock');
                              const rect = dock.getBoundingClientRect();
                              return {
                                windowY: window.scrollY,
                                activeY: document.querySelector('.tab-content.active')?.scrollTop || 0,
                                dockBottom: Math.round(rect.bottom),
                                height: window.innerHeight,
                              };
                            }"""
                        )
                        if after["windowY"] > before["windowY"] + 2 or after["activeY"] > before["activeY"] + 2:
                            failures.append(f"{width}x{height} {tab}: dock tab click scrolls downward")
                        if after["dockBottom"] > after["height"] + 2:
                            failures.append(f"{width}x{height} {tab}: dock clipped after tab click {after}")

        browser.close()

    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}")
        return 1

    print("all tab layout checks OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
