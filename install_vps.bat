@echo off
setlocal enabledelayedexpansion
title Setup VPS - UPI Web API

:: 1. Check for Administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Administrator privileges confirmed.
) else (
    echo [INFO] Requesting Administrator privileges to open Firewall ports...
    powershell -Command "Start-Process '%~0' -Verb RunAs"
    exit /b
)

cd /d "%~dp0"

echo ============================================================
echo   CAI DAT HE THONG AUTO TREN VPS WINDOWS RDP
echo ============================================================
echo.

:: 2. Setup .env file
if not exist ".env" (
    echo [SETUP] Phat hien chua co file .env
    echo Vui long nhap thong tin Turso Database de he thong ket noi.
    echo (Neu chua co, hay bam Enter de bo qua, he thong se dung SQLite local)
    
    set /p TURSO_URL="Nhap TURSO_DATABASE_URL (vd: libsql://...): "
    set /p TURSO_TOKEN="Nhap TURSO_AUTH_TOKEN: "
    
    echo TURSO_DATABASE_URL=!TURSO_URL!> .env
    echo TURSO_AUTH_TOKEN=!TURSO_TOKEN!>> .env
    echo [OK] Da tao file .env!
) else (
    echo [OK] File .env da ton tai.
)

:: 3. Open Firewall Port 8000
echo.
echo [SETUP] Dang mo port 8000 tren Windows Firewall...
netsh advfirewall firewall show rule name="UPI Web API Port 8000" >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Rule Firewall da ton tai.
) else (
    netsh advfirewall firewall add rule name="UPI Web API Port 8000" dir=in action=allow protocol=TCP localport=8000
    echo [OK] Mo port 8000 thanh cong!
)

:: 4. Run main setup.bat to install Python dependencies
echo.
echo [SETUP] Dang tien hanh cai dat thu vien Python (Goi setup.bat)...
call setup.bat
if errorlevel 1 (
    echo [ERROR] Qua trinh cai dat thu vien bi loi. Vui long kiem tra lai.
    pause
    exit /b
)

:: 5. Start the server
echo.
echo [OK] HOAN TAT CAI DAT! Dang khoi dong Server...
timeout /t 3
call start_web.bat
