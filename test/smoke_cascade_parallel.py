"""Smoke test cho OutlookCascadeProvider.poll_otp poll song song.

Khong goi network that — chi inject fake _dongvanfb / _microsoft provider de
verify hanh vi: ai ve truoc thang, ca hai fail thi raise dung loai loi,
provider thua bi cancel.
"""
import asyncio
import io
import sys
from datetime import datetime, timezone

import mail_providers as mp


class FakeProvider:
    def __init__(self, *, delay, result=None, exc=None):
        self.delay = delay
        self.result = result
        self.exc = exc
        self.cancelled = False

    async def poll_otp(self, *, recipient, started_at, timeout_seconds,
                       poll_interval_seconds, log):
        try:
            await asyncio.sleep(self.delay)
        except asyncio.CancelledError:
            self.cancelled = True
            raise
        if self.exc is not None:
            raise self.exc
        return self.result


def _make_cascade(dv, ms):
    c = mp.OutlookCascadeProvider.__new__(mp.OutlookCascadeProvider)
    class _Combo:
        email = "x@outlook.com"
    c.combo = _Combo()
    c._dongvanfb = dv
    c._microsoft = ms
    return c


def _logs():
    out = []
    return out, (lambda m: out.append(m))


async def _poll(c):
    return await c.poll_otp(
        recipient="x@outlook.com",
        started_at=datetime.now(timezone.utc),
        timeout_seconds=10.0,
        poll_interval_seconds=1.0,
        log=_logs()[1],
    )


async def main():
    failures = []

    # 1) Microsoft ve truoc khi DongVanFB cham -> Microsoft thang, DongVanFB cancel.
    dv = FakeProvider(delay=5.0, result="111111")
    ms = FakeProvider(delay=0.1, result="999999")
    c = _make_cascade(dv, ms)
    code = await _poll(c)
    if code != "999999":
        failures.append(f"case1: expected 999999 got {code}")
    await asyncio.sleep(0.05)
    if not dv.cancelled:
        failures.append("case1: DongVanFB phai bi cancel")

    # 2) DongVanFB timeout, Microsoft ve sau -> Microsoft thang.
    dv = FakeProvider(delay=0.1, exc=TimeoutError("dv timeout"))
    ms = FakeProvider(delay=0.3, result="555555")
    c = _make_cascade(dv, ms)
    code = await _poll(c)
    if code != "555555":
        failures.append(f"case2: expected 555555 got {code}")

    # 3) Ca hai fail thuong -> raise loi cuoi (khong phai combo error).
    dv = FakeProvider(delay=0.1, exc=TimeoutError("dv timeout"))
    ms = FakeProvider(delay=0.2, exc=RuntimeError("ms down"))
    c = _make_cascade(dv, ms)
    try:
        await _poll(c)
        failures.append("case3: phai raise")
    except mp.OutlookComboError:
        failures.append("case3: khong duoc raise OutlookComboError")
    except Exception:
        pass

    # 4) Combo error duoc uu tien khi ca hai fail.
    dv = FakeProvider(delay=0.1, exc=RuntimeError("dv net"))
    ms = FakeProvider(delay=0.2, exc=mp.OutlookComboError("token revoked"))
    c = _make_cascade(dv, ms)
    try:
        await _poll(c)
        failures.append("case4: phai raise")
    except mp.OutlookComboError:
        pass
    except Exception as e:
        failures.append(f"case4: expected OutlookComboError got {type(e).__name__}")

    if failures:
        print("FAIL:")
        for f in failures:
            print(" -", f)
        sys.exit(1)
    print("ALL CASES PASS")


asyncio.run(main())
