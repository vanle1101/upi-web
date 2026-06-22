"""Static check for the premium all-tab UI skin."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "web" / "static" / "style.css"


def _balanced_braces(src: str) -> bool:
    depth = 0
    in_comment = False
    i = 0
    while i < len(src):
        ch = src[i]
        nxt = src[i + 1] if i + 1 < len(src) else ""
        if not in_comment and ch == "/" and nxt == "*":
            in_comment = True
            i += 2
            continue
        if in_comment and ch == "*" and nxt == "/":
            in_comment = False
            i += 2
            continue
        if in_comment:
            i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return False
        i += 1
    return depth == 0 and not in_comment


def main() -> int:
    src = CSS.read_text(encoding="utf-8")
    checks = [
        ("Premium operations skin" in src, "premium skin layer exists"),
        (_balanced_braces(src), "CSS braces are balanced"),
        ('--font-sans: "Geist"' in src, "Geist typography stack selected"),
        (".topbar" in src and "backdrop-filter" in src, "premium command topbar styles exist"),
        (".tab-btn.active" in src and ".settings-nav-item.active" in src, "nav and settings active states styled"),
        (".card:hover" in src and ".job:hover" in src, "card and job hover physics exist"),
        (".modal" in src and ".upi-qr-modal-image-wrap" in src, "modal and UPI QR surfaces styled"),
        ("#tab-hme.hme-grid" in src and ".hme-table tbody tr:hover" in src, "HME grid and table styling covered"),
        ("grid-auto-flow: dense" in src, "dense grid behavior enabled"),
        ("SECTION 01" not in src and "QUESTION 05" not in src, "no cheap meta labels added"),
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
