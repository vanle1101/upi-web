"""Static check for UPI log auto-select and low retry warning."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

ROOT = Path(__file__).resolve().parents[1]
UPI_JS = ROOT / "web" / "static" / "upi.js"


def main() -> int:
    src = UPI_JS.read_text(encoding="utf-8")
    checks = [
        ("state.activeJobId = state.order[0] || null" in src, "snapshot auto-selects first job"),
        ("state.activeJobId = j.id" in src, "job update auto-selects new job"),
        ("if (!state.activeJobId) {" in src and "renderJobs();" in src, "log event auto-selects job"),
        ("approveRetries < 50" in src, "low approve retries warning"),
        ("Giá trị này rất thấp" in src, "warning message explains low retries"),
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
