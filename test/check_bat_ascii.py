from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = ["setup.bat", "start_web.bat"]
FORBIDDEN = [
    "2>nul",
    "python -c",
    "â",
    "Ã",
    "áº",
    "á»",
    "Æ",
    "═",
    "√",
    "→",
]


def main() -> int:
    errors: list[str] = []

    for name in TARGETS:
        path = ROOT / name
        data = path.read_bytes()
        non_ascii = sorted({byte for byte in data if byte > 0x7F})
        if non_ascii:
            errors.append(f"{name}: non-ASCII bytes: {non_ascii}")

        text = data.decode("ascii", errors="replace")
        for pattern in FORBIDDEN:
            if pattern in text:
                errors.append(f"{name}: forbidden pattern {pattern!r}")

    if errors:
        print("[FAIL] Batch file checks failed")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("[PASS] setup.bat and start_web.bat are ASCII-safe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
