"""Focused verification for click-free password entry fallback."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from _browser_form import fill_password_without_click


class FillTimeoutLocator:
    def __init__(self) -> None:
        self.value = ""
        self.evaluate_calls = 0

    async def fill(self, _value: str, *, timeout: int) -> None:
        assert timeout == 8000
        raise TimeoutError("simulated fill timeout")

    async def input_value(self, *, timeout: int) -> str:
        assert timeout == 3000
        return self.value

    async def evaluate(self, script: str, value: str) -> None:
        assert "HTMLInputElement" in script
        self.evaluate_calls += 1
        self.value = value


async def run_check() -> None:
    locator = FillTimeoutLocator()
    logs: list[str] = []
    await fill_password_without_click(
        locator,
        "example-password",
        log=logs.append,
        prefix="[test]",
    )
    assert locator.value == "example-password"
    assert locator.evaluate_calls == 1
    assert any("without click" in line for line in logs)
    assert any("entered and verified" in line for line in logs)


def main() -> int:
    asyncio.run(run_check())
    print("[PASS] fill timeout falls back to DOM and verifies without click", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
