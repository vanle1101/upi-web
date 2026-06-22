from __future__ import annotations

import importlib


MODULES = [
    "typer",
    "fastapi",
    "uvicorn",
    "pydantic",
    "curl_cffi",
    "filelock",
    "camoufox",
    "playwright",
    "gpt_signup_hybrid",
    "cli",
    "web.server",
]


def main() -> int:
    errors: list[str] = []

    for module_name in MODULES:
        try:
            importlib.import_module(module_name)
        except Exception as exc:
            errors.append(f"{module_name}: {type(exc).__name__}: {exc}")

    if errors:
        print("[FAIL] Runtime import check failed")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"[PASS] Imported {len(MODULES)} runtime modules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
