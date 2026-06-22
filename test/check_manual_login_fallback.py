"""Static check for headed browser fallback support."""
from __future__ import annotations

import ast
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

ROOT = Path(__file__).resolve().parents[1]


def _load_tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _function_signature_has(tree: ast.Module, name: str, param: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return any(arg.arg == param for arg in node.args.kwonlyargs)
    return False


def main() -> int:
    session_src = (ROOT / "session_phase.py").read_text(encoding="utf-8")
    upi_src = (ROOT / "web" / "upi_runner.py").read_text(encoding="utf-8")
    session_tree = _load_tree(ROOT / "session_phase.py")

    checks = [
        (_function_signature_has(session_tree, "_get_session_browser", "manual_login"),
         "_get_session_browser accepts manual_login"),
        (_function_signature_has(session_tree, "get_session", "manual_login"),
         "get_session accepts manual_login"),
        (_function_signature_has(session_tree, "get_session_sync", "manual_login"),
         "get_session_sync accepts manual_login"),
        ("manual login popup opened" in session_src,
         "manual login log exists"),
        ("deadline_seconds=300.0" in session_src,
         "manual login waits 300s"),
        ("auto-fill mail/pass/2FA" in upi_src,
         "UPI invalid_state fallback logs auto-fill"),
        ("manual_login=True" not in upi_src,
         "UPI invalid_state fallback does not require manual login"),
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
