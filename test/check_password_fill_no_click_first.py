"""Static check: password fill should not depend on click-first."""
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
    session_src = (ROOT / "session_phase.py").read_text(encoding="utf-8")
    browser_src = (ROOT / "browser_phase.py").read_text(encoding="utf-8")
    helper_src = (ROOT / "_browser_form.py").read_text(encoding="utf-8")
    checks = [
        ("fill_password_without_click" in session_src,
         "session_phase uses shared click-free password helper"),
        (browser_src.count("fill_password_without_click(") == 2,
         "browser_phase uses click-free helper in both login paths"),
        ("await locator.fill(password" in helper_src,
         "helper attempts native fill first"),
        ("await locator.evaluate(_SET_INPUT_VALUE_JS, password)" in helper_src,
         "helper falls back to DOM input events"),
        ("await locator.input_value" in helper_src,
         "helper verifies the entered password"),
        ("locator.click" not in helper_src and "pwd_input.click" not in session_src,
         "password entry never relies on locator click"),
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
