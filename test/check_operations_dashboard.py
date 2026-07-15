from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "web" / "static" / "index.html"
OPERATIONS_CSS = ROOT / "web" / "static" / "operations.css"


def _without_comments_and_strings(source: str) -> str:
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    source = re.sub(r'"(?:\\.|[^"\\])*"', '""', source)
    source = re.sub(r"'(?:\\.|[^'\\])*'", "''", source)
    return source


def main() -> None:
    index = INDEX.read_text(encoding="utf-8")
    css = OPERATIONS_CSS.read_text(encoding="utf-8")
    compact_css = _without_comments_and_strings(css)

    links = re.findall(r'<link\s+rel="stylesheet"\s+href="([^"]+)"', index)
    assert links[-1].startswith("/static/operations.css"), links
    assert sum("operations.css" in link for link in links) == 1

    critical_ids = (
        "headless-toggle",
        "debug-toggle",
        "combo-input",
        "btn-run",
        "job-list",
        "log-pane",
        "proxy-toggle",
        "reg-proxy-input",
        "ses-combo-input",
        "ses-btn-run",
        "ses-job-list",
        "upi-combo-input",
        "upi-btn-run",
        "upi-job-list",
        "upi-proxy-toggle",
        "upi-proxy-input",
        "getacc-json-input",
        "getacc-extract-btn",
        "telegram-bot-token",
        "telegram-save",
    )
    for element_id in critical_ids:
        count = len(re.findall(rf'id="{re.escape(element_id)}"', index))
        assert count == 1, f"{element_id}: expected once, found {count}"

    assert compact_css.count("{") == compact_css.count("}"), "Unbalanced CSS braces"

    required_fragments = (
        "--ops-bg: #071017",
        "--ops-rail-width: 236px",
        "--ops-accent: #58a6ff",
        "GSH Control Room",
        "grid-template-columns: var(--ops-rail-width) minmax(0, 1fr)",
        ".topbar {",
        "width: var(--ops-rail-width)",
        "backdrop-filter: blur(18px)",
        ".tab-nav {",
        ".tab-btn.active",
        ".ops-workspace,",
        ".workspace-mast",
        ".workspace-grid",
        "grid-template-columns: minmax(315px, 360px) minmax(0, 1fr)",
        ".control-surface",
        ".execution-canvas",
        "grid-template-rows: minmax(0, 1fr) auto",
        ".workflow-proxy-toggle",
        ".diagnostics-dock {",
        ".diagnostics-dock:not(.is-collapsed)",
        ".job-list .empty,",
        ".settings-workspace",
        ".settings-sidebar",
        "@media (max-width: 1050px)",
        "@media (max-width: 900px)",
        "@media (prefers-reduced-motion: reduce)",
    )
    for fragment in required_fragments:
        assert fragment in css, f"Missing dashboard rule: {fragment}"

    lowered = css.lower()
    assert "#000" not in lowered
    assert "neon" not in lowered
    assert "glow" not in lowered

    print("operations dashboard check: OK")


if __name__ == "__main__":
    main()
