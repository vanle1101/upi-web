"""Static check for Get Session headed auto-fill fallback wiring."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

ROOT = Path(__file__).resolve().parents[1]
MANAGER = ROOT / "web" / "manager.py"


def main() -> int:
    src = MANAGER.read_text(encoding="utf-8")
    checks = [
        ("def _should_browser_session_fallback" in src, "SessionJobManager has fallback detector"),
        ("invalid_state" in src and "authorize/continue" in src, "fallback detects invalid_state"),
        ("if self._debug:" in src, "Debug path exists"),
        ("Debug ON -> thử pure request ngầm trước" in src, "Debug path keeps pure request first"),
        ("headless=False" in src, "browser fallback is headed"),
        ("auto-fill mail/pass/2FA" in src, "invalid_state fallback logs auto-fill"),
        ("keep_browser_open_on_error=True" in src, "headed browser stays open only on error"),
        ("manual_login=True" not in src, "Get Session fallback does not require manual login"),
        ("timeout=None" in src, "headed debug/fallback is not cut by job timeout"),
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
