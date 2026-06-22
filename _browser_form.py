"""Robust browser form helpers shared by login flows."""
from __future__ import annotations

import asyncio
from typing import Any, Callable


LogFn = Callable[[str], None]


_SET_INPUT_VALUE_JS = r"""
(el, value) => {
    const descriptor = Object.getOwnPropertyDescriptor(
        window.HTMLInputElement.prototype,
        'value'
    );
    if (!descriptor || typeof descriptor.set !== 'function') {
        throw new Error('HTMLInputElement value setter unavailable');
    }
    descriptor.set.call(el, value);
    const inputEvent = typeof window.InputEvent === 'function'
        ? new window.InputEvent('input', {
            bubbles: true,
            inputType: 'insertText',
            data: value,
        })
        : new window.Event('input', {bubbles: true});
    el.dispatchEvent(inputEvent);
    el.dispatchEvent(new window.Event('change', {bubbles: true}));
}
"""


async def fill_password_without_click(
    locator: Any,
    password: str,
    *,
    log: LogFn,
    prefix: str,
    timeout_ms: int = 8000,
) -> None:
    """Fill and verify a password field without relying on pointer actions."""
    fill_error: BaseException | None = None
    try:
        await locator.fill(password, timeout=timeout_ms)
    except Exception as exc:
        fill_error = exc
        log(
            f"{prefix} native fill failed ({type(exc).__name__}); "
            "using DOM input fallback without click"
        )

    try:
        current = await locator.input_value(timeout=3000)
    except Exception:
        current = ""

    if current != password:
        try:
            await locator.evaluate(_SET_INPUT_VALUE_JS, password)
            await asyncio.sleep(0.15)
            current = await locator.input_value(timeout=3000)
        except Exception as exc:
            detail = f"{type(exc).__name__}: {exc}"
            if fill_error is not None:
                detail = (
                    f"fill={type(fill_error).__name__}: {fill_error}; "
                    f"dom={detail}"
                )
            raise RuntimeError(
                f"password input failed without click fallback: {detail}"
            ) from exc

    if current != password:
        raise RuntimeError(
            "password input value verification failed after native fill and DOM fallback"
        )

    log(f"{prefix} password entered and verified")
