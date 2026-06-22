"""Static check: DongVanFB should try latest visible OTP before resend."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "mail_providers.py"


def main() -> int:
    src = TARGET.read_text(encoding="utf-8")
    checks = [
        ("fallback: thử code mới nhất đang có" in src,
         "DongVanFB logs fallback to latest visible code"),
        ("return code" in src and "openai_codes[0]" in src,
         "DongVanFB returns latest visible code from baseline"),
        ("OTP rejected" in (ROOT / "browser_phase.py").read_text(encoding="utf-8"),
         "browser_phase handles rejected OTP before resend"),
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
