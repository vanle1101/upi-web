"""Static check for clear UPI approve failure wording."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "web" / "upi_runner.py"


def main() -> int:
    src = TARGET.read_text(encoding="utf-8")
    checks = [
        ("approve/thanh toán không thành công" in src, "approve error names payment phase"),
        ("không phải login attempts" in src, "approve error says not login attempts"),
        ("Approve retries=" in src, "approve error names UI field"),
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
