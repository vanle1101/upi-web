"""Repo-root module shim so `python -m gpt_signup_hybrid` works here."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path


__path__ = [str(Path(__file__).resolve().parent)]
__package__ = __name__


def _configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main() -> None:
    _configure_utf8_stdio()
    from _expire_check import enforce_expiry

    enforce_expiry()
    cli_mod = importlib.import_module(".cli", __name__)
    cli_mod.app()


if __name__ == "__main__":
    main()
