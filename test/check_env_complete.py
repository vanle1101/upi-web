from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"

REQUIRED_KEYS = {
    "BROWSER_ENGINE",
    "RUNTIME_DIR",
    "BROWSER_VIEWPORT_WIDTH",
    "BROWSER_VIEWPORT_HEIGHT",
    "BROWSER_USE_PROFILE_TEMPLATE",
    "BROWSER_PROFILE_TEMPLATE_DIR",
    "BROWSER_CAMOUFOX_PROFILE_DIR",
    "BROWSER_RANDOM_SCREEN",
    "HYBRID_MAX_CONCURRENT",
    "HYBRID_OUTLOOK_PROXY",
    "HYBRID_JOB_TIMEOUT",
}

REQUIRED_DIRS = [
    "runtime/profiles/template",
    "runtime/profiles/camoufox_template",
    "runtime/sessions",
    "runtime/outlook_state",
    "runtime/outlook_pool",
    "runtime/har_hybrid",
]


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def main() -> int:
    errors: list[str] = []

    if not ENV_PATH.exists():
        errors.append(".env missing")
    else:
        values = parse_env(ENV_PATH)
        missing = sorted(REQUIRED_KEYS - set(values))
        if missing:
            errors.append("missing env keys: " + ", ".join(missing))

    for rel in REQUIRED_DIRS:
        if not (ROOT / rel).is_dir():
            errors.append(f"missing runtime dir: {rel}")

    if errors:
        print("[FAIL] .env/runtime check failed")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("[PASS] .env and runtime dirs are complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
