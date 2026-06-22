@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "ROOT_DIR=%CD%"
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"

echo ============================================================
echo   gpt_signup_hybrid - setup + start web UI
echo   root: %ROOT_DIR%
echo ============================================================
echo.

REM 1. Create Python venv.
if not exist ".venv\Scripts\python.exe" (
    echo [1/6] Creating .venv...
    python -m venv .venv
    if errorlevel 1 goto :fail
) else (
    echo [1/6] .venv exists
)

REM 2. Install dependencies. Do not hide errors; missing deps cause startup crash.
echo [2/6] Installing dependencies...
".venv\Scripts\python.exe" -m pip --version
if errorlevel 1 (
    echo [WARN] pip is broken or missing. Trying ensurepip repair...
    ".venv\Scripts\python.exe" -m ensurepip --upgrade
    if errorlevel 1 goto :fail
)

call :pip_install "pydantic" "typer" "fastapi" "uvicorn" "pyotp" "filelock"
if errorlevel 1 goto :fail
call :pip_install "httpx[socks]" "curl_cffi>=0.7" "requests" "PyYAML"
if errorlevel 1 goto :fail
call :pip_install "camoufox[geoip]" "playwright==1.49.1" "playwright-stealth>=2.0.0" "ruyiPage"
if errorlevel 1 goto :fail
call :pip_install "faker>=20.0" "qrcode[pil]" "lxml" "screeninfo" "language-tags" "browserforge" "apify_fingerprint_datapoints"
if errorlevel 1 goto :fail

REM 3. Quick import check for the most common missing dependency.
echo [3/6] Checking Python imports...
".venv\Scripts\python.exe" -m pip show typer >nul
if errorlevel 1 (
    echo [ERROR] Missing package: typer
    goto :fail
)

REM 4. Playwright Firefox.
echo [4/6] Installing Playwright Firefox...
".venv\Scripts\python.exe" -m playwright install firefox
if errorlevel 1 goto :fail

REM 5. Camoufox binary.
echo [5/6] Fetching Camoufox binary...
".venv\Scripts\python.exe" -m camoufox fetch
if errorlevel 1 goto :fail

REM 6. .env
if not exist ".env" (
    echo [6/6] Creating .env...
    (
        echo BROWSER_ENGINE=camoufox
        echo RUNTIME_DIR=runtime
        echo BROWSER_VIEWPORT_WIDTH=1440
        echo BROWSER_VIEWPORT_HEIGHT=800
        echo BROWSER_USE_PROFILE_TEMPLATE=true
        echo BROWSER_PROFILE_TEMPLATE_DIR=runtime/profiles/template
        echo BROWSER_CAMOUFOX_PROFILE_DIR=runtime/profiles/camoufox_template
        echo BROWSER_RANDOM_SCREEN=true
        echo HYBRID_MAX_CONCURRENT=2
        echo HYBRID_OUTLOOK_PROXY=
        echo HYBRID_JOB_TIMEOUT=240
    ) > .env
) else (
    echo [6/6] .env exists
)

call :mkdir_if_missing "runtime\profiles\template"
call :mkdir_if_missing "runtime\profiles\camoufox_template"
call :mkdir_if_missing "runtime\sessions"
call :mkdir_if_missing "runtime\outlook_state"
call :mkdir_if_missing "runtime\outlook_pool"
call :mkdir_if_missing "runtime\har_hybrid"

echo.
echo ============================================================
echo   Setup done. Starting web UI...
echo   URL: http://127.0.0.1:8083/
echo.
echo   Combo format: email^|password^|refresh_token^|client_id
echo ============================================================
echo.

start "" "http://127.0.0.1:8083/"
".venv\Scripts\python.exe" -m gpt_signup_hybrid web --host 127.0.0.1 --port 8083
echo.
pause
exit /b 0

:pip_install
echo   pip install %*
".venv\Scripts\python.exe" -m pip install %*
exit /b %ERRORLEVEL%

:mkdir_if_missing
if not exist "%~1" mkdir "%~1"
exit /b 0

:fail
echo.
echo [ERROR] Setup failed. Read the error above, then run setup.bat again.
echo.
pause
exit /b 1
