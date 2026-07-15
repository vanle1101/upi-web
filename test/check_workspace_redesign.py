"""Structural checks for the redesigned operations workspace."""
from __future__ import annotations

import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

ROOT = Path(__file__).resolve().parents[1]


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.dock_targets: list[str] = []
        self.dock_panels: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if values.get("data-dock-target"):
            self.dock_targets.append(values["data-dock-target"] or "")
        if values.get("data-dock-panel"):
            self.dock_panels.append(values["data-dock-panel"] or "")


def main() -> int:
    html = (ROOT / "web" / "static" / "index.html").read_text(encoding="utf-8")
    workspace_css = (ROOT / "web" / "static" / "workspace.css").read_text(encoding="utf-8")
    operations_css = (ROOT / "web" / "static" / "operations.css").read_text(encoding="utf-8")
    css = f"{workspace_css}\n{operations_css}"
    js = (ROOT / "web" / "static" / "workspace.js").read_text(encoding="utf-8")
    parser = StructureParser()
    parser.feed(html)
    duplicates = sorted(key for key, count in Counter(parser.ids).items() if count > 1)
    required_ids = {
        "combo-input", "job-list", "log-pane", "success-pane", "error-pane",
        "ses-combo-input", "ses-job-list", "ses-log-pane", "ses-error-pane",
        "upi-combo-input", "upi-session-input", "upi-job-list", "upi-log-pane",
        "upi-success-pane", "upi-error-pane", "settings-section-proxies",
        "settings-section-telegram",
    }
    checks = [
        (not duplicates, f"all HTML ids are unique: {duplicates}"),
        (required_ids.issubset(set(parser.ids)), "all existing workflow bindings remain present"),
        (set(parser.dock_targets) == set(parser.dock_panels), "every diagnostics tab maps to a panel"),
        (len(parser.dock_targets) == 8, "Reg, Session and UPI diagnostics docks are complete"),
        ('class="tab-content ops-workspace ops-reg active"' in html, "Reg uses the new workspace"),
        ('class="tab-content ops-workspace ops-session"' in html, "Get Session uses the new workspace"),
        ('class="tab-content ops-workspace ops-upi"' in html, "UPI uses the new workspace"),
        ('class="tab-content settings-page"' in html, "Settings uses the dedicated page layout"),
        ("grid-template-columns: var(--ops-rail-width) minmax(0, 1fr)" in operations_css,
         "desktop side-rail shell is configured"),
        ("--ops-bg: #071017" in operations_css and "color-scheme: dark" in operations_css,
         "workspace uses the dark operations-console palette"),
        ("width: var(--ops-rail-width)" in operations_css and ".tab-btn.active" in operations_css,
         "navigation is isolated in the dark command rail"),
        (".toggle-wrap input:checked ~ .toggle-label" in css,
         "checked runtime toggle labels remain readable on the command rail"),
        ("font-size: 14px" in css and "font-size: 12.5px" in css,
         "interface typography uses the larger readable scale"),
        (".proxy-textarea" in css and "background: var(--ops-input)" in operations_css,
         "specialized proxy and modal inputs use visible dark surfaces"),
        (".tab-content input:disabled" in css and ".tab-content button:disabled" in css,
         "disabled form and action states remain readable"),
        (".diagnostics-dock" in css and ".dock-panel[hidden]" in css,
         "diagnostics dock states are styled"),
        (html.count("diagnostics-dock is-collapsed") == 3,
         "technical diagnostics are collapsed by default"),
        (css.count("{") == css.count("}"), "workspace CSS braces are balanced"),
        ("activateDockPanel" in js and "setDockCollapsed" in js and "MutationObserver" in js,
         "diagnostics interaction and output indicators are wired"),
        ('panel.querySelector(".output-pane")' in js,
         "diagnostics content markers ignore panel header text"),
        ('workspace.js?v=__ASSET_VERSION__' in html, "workspace interaction script is loaded"),
    ]
    failed = 0
    for ok, label in checks:
        if ok:
            print(f"[PASS] {label}", flush=True)
        else:
            print(f"[FAIL] {label}", flush=True)
            failed += 1
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
