"""Static checks for the premium operational UI theme."""
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
    html = (ROOT / "web" / "static" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "web" / "static" / "style.css").read_text(encoding="utf-8")
    checks = [
        ('class="brand-mark"' in html, "header has production brand mark"),
        ("Operations Console" in html, "header has operational product name"),
        ("Precision Console 2026" in css, "premium theme layer exists"),
        ('--font-sans: "Geist"' in css, "Geist typography stack is configured"),
        ("grid-template-columns: minmax(420px, 0.86fr) minmax(520px, 1.14fr)" in css,
         "desktop workspace prioritizes jobs"),
        (".card-jobs::before" in css and ".card-log::before" in css,
         "functional panels have distinct hierarchy"),
        ("@media (max-width: 700px)" in css, "mobile command bar layout exists"),
        ('id="combo-input"' in html and 'id="job-list"' in html and 'id="log-pane"' in html,
         "core Reg bindings remain intact"),
        ('id="ses-combo-input"' in html and 'id="ses-job-list"' in html,
         "Get Session bindings remain intact"),
        ('id="upi-combo-input"' in html and 'id="upi-job-list"' in html,
         "UPI bindings remain intact"),
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
