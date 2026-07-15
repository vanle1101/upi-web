@echo off
setlocal
cd /d "%~dp0"
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"

echo ============================================
echo   gpt_signup_hybrid - start web UI
echo ============================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Chua co .venv.
    echo Hay chay setup.bat truoc de cai moi thu.
    echo.
    pause
    exit /b 1
)

if not exist ".env" (
    echo [WARN] Chua co .env.
    echo Neu app loi cau hinh, hay chay setup.bat truoc.
    echo.
)

if not exist "runtime" mkdir "runtime"

.venv\Scripts\python.exe -m pip show typer >nul
if errorlevel 1 (
    echo [ERROR] Missing Python package: typer.
    echo Run setup.bat first, then run start_web.bat again.
    echo.
    pause
    exit /b 1
)

echo Web UI: http://127.0.0.1:8080/
echo Nhan Ctrl+C de dung server.
echo.

start "" "http://127.0.0.1:8080/"
.venv\Scripts\python.exe -m gpt_signup_hybrid web --host 127.0.0.1 --port 8080

echo.
pause
