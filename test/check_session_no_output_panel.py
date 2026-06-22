"""Static check that Get Session does not expose session JSON in a page panel."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    index = (ROOT / "web" / "static" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "web" / "static" / "session.js").read_text(encoding="utf-8")
    css = (ROOT / "web" / "static" / "style.css").read_text(encoding="utf-8")
    checks = [
        ("ses-success-pane" not in index, "Get Session HTML has no visible session output pane"),
        ("ses-btn-copy-success" not in index, "Get Session HTML has no output Copy All"),
        ("Format: email|session_json" not in js, "session.js does not render session JSON panel"),
        ("copy-json" in js and "download" in js and "copy-token" in js,
         "session actions still provide copy/download icons"),
        ('"error error"' in css, "Get Session grid uses full-width error row"),
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
