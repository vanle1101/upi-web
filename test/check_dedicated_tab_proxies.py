from __future__ import annotations

import ast
import asyncio
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def check_python_syntax() -> None:
    for relative in ("db/repositories.py", "web/manager.py", "web/server.py"):
        path = ROOT / relative
        ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))


def check_settings_validation() -> None:
    from db.repositories import RepositoryError, _validate_type_constraint

    for key in ("reg.proxy", "upi.proxy"):
        _validate_type_constraint(key, None)
        _validate_type_constraint(key, "127.0.0.1:8080:user:pass")
        _validate_type_constraint(
            key,
            "127.0.0.1:8080:user:pass\n127.0.0.1:8081:user:pass",
        )
        try:
            _validate_type_constraint(key, ["not-a-string"])
        except RepositoryError:
            pass
        else:
            raise AssertionError(f"{key} accepted a non-string value")

    for key in ("reg.use_proxy", "upi.use_proxy"):
        _validate_type_constraint(key, True)
        _validate_type_constraint(key, False)
        try:
            _validate_type_constraint(key, 1)
        except RepositoryError:
            pass
        else:
            raise AssertionError(f"{key} accepted a non-boolean value")


def check_managers_are_independent() -> None:
    from web.manager import Job, JobManager, UpiJobManager

    reg = JobManager()
    upi = UpiJobManager()
    reg_proxy_pool = (
        "127.0.0.1:8101:reg_user:reg_pass\n"
        "127.0.0.1:8105:reg_user2:reg_pass2"
    )
    upi_proxy_pool = (
        "127.0.0.1:8102:upi_user:upi_pass\n"
        "127.0.0.1:8106:upi_user2:upi_pass2"
    )
    reg.apply_settings({
        "reg.proxy": reg_proxy_pool,
        "reg.use_proxy": False,
    })
    upi.apply_settings({
        "upi.proxy": upi_proxy_pool,
        "upi.use_proxy": False,
    })

    assert reg.proxy == reg_proxy_pool
    assert upi.proxy == upi_proxy_pool
    assert reg.proxy != upi.proxy
    assert reg.use_proxy is False
    assert upi.use_proxy is False

    job = Job(
        id="proxy-check",
        combo="check@example.com|password",
        email="check@example.com",
        password="password",
    )
    url, raw = asyncio.run(reg._resolve_proxy_for_job(job, None))
    assert url is None and raw is None

    reg.set_use_proxy(True)
    upi.set_use_proxy(True)
    url, raw = asyncio.run(reg._resolve_proxy_for_job(job, None))
    assert raw == "127.0.0.1:8101:reg_user:reg_pass"
    assert url == "http://reg_user:reg_pass@127.0.0.1:8101"
    url, raw = asyncio.run(reg._resolve_proxy_for_job(job, None))
    assert raw == "127.0.0.1:8105:reg_user2:reg_pass2"
    assert url == "http://reg_user2:reg_pass2@127.0.0.1:8105"

    reg.set_proxy(None)
    assert reg.proxy is None
    assert reg.use_proxy is True
    assert upi.proxy == upi_proxy_pool
    try:
        asyncio.run(reg._resolve_proxy_for_job(job, None))
    except ValueError as exc:
        assert "enabled but empty" in str(exc)
    else:
        raise AssertionError("Reg accepted an enabled proxy with no value")

    legacy_reg = JobManager()
    legacy_upi = UpiJobManager()
    legacy_reg.apply_settings({"reg.proxy": "127.0.0.1:8103"})
    legacy_upi.apply_settings({"upi.proxy": "127.0.0.1:8104"})
    assert legacy_reg.use_proxy is True
    assert legacy_upi.use_proxy is True


def check_no_shared_pool_calls() -> None:
    source = (ROOT / "web/manager.py").read_text(encoding="utf-8-sig")
    reg_block = source[source.index("class JobManager:"):source.index("class SessionJobManager:")]
    upi_block = source[source.index("class UpiJobManager:"):]
    assert "url, line = await _resolve_job_proxy" not in reg_block
    assert "raw_pool = list(get_proxy_pool().live_entries())" not in upi_block
    assert "raw_pool = _split_proxy_lines(self._proxy) if self._use_proxy else []" in upi_block


if __name__ == "__main__":
    check_python_syntax()
    check_settings_validation()
    check_managers_are_independent()
    check_no_shared_pool_calls()
    print("dedicated tab proxies: OK")
