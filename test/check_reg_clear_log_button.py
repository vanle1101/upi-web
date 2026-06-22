"""Static check for Reg tab Clear Log button."""
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
    app = (ROOT / "web" / "static" / "app.js").read_text(encoding="utf-8")
    checks = [
        ('id="btn-clear-log"' in index, "Reg HTML has Clear Log button"),
        ("btnClearLog: $('btn-clear-log')" in app, "app.js has Clear Log DOM ref"),
        ("dom.btnClearLog.addEventListener" in app, "app.js wires Clear Log click"),
        ("dom.logPane.textContent = ''" in app, "Clear Log clears visible log pane"),
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
