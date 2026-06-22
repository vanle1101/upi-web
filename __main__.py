"""python -m gpt_signup_hybrid -> CLI."""
from __future__ import annotations

import sys


for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from _expire_check import enforce_expiry

enforce_expiry()

from cli import app  # noqa: E402


if __name__ == "__main__":
    app()
