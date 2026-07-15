@echo off
setlocal enabledelayedexpansion
title VPS 1-CLICK SETUP - UPI WEB

:: 1. Xin quyen Administrator
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo [INFO] Xin quyen Administrator de mo Firewall...
    powershell -Command "Start-Process '%~0' -Verb RunAs"
    exit /b
)

cd /d "%~dp0"
echo ===================================================
echo    1-CLICK SETUP CHO VPS WINDOWS (UPI WEB API)
echo ===================================================
echo.

:: 2. Thiet lap Database (.env)
echo [1/3] Dang thiet lap thong tin Turso Database...
echo TURSO_DATABASE_URL=libsql://upi-lehongvan123.aws-ap-northeast-1.turso.io> .env
echo TURSO_AUTH_TOKEN=eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3ODQwOTc5OTUsImlkIjoiMDE5ZjY0ODYtNmYwMS03MjYxLTlkNTgtZmM2OWQyNDBkN2ViIiwia2lkIjoianpXdXZWNHBIVU1EaEZHb3FDN29fcExMcUtFeURRYUlmZHAybGlNZ3RfRSIsInJpZCI6ImM1MTUyZTRiLTJhNDQtNDFiNy04ODY5LTRiZDY1OGRlZTg2OSJ9.1k3Jp60t38ZK7ZEzGzXJ1LM8N0ib1WnywXmF5tznsKJ4H98aLm9AF2-gPye0Xwyb_4iDbhB4oplJtXTERHVHBw>> .env

:: 3. Mo cong Firewall 8000
echo [2/3] Dang mo cong Firewall 8000...
netsh advfirewall firewall show rule name="UPI Web API" >nul 2>&1
if %errorLevel% NEQ 0 (
    netsh advfirewall firewall add rule name="UPI Web API" dir=in action=allow protocol=TCP localport=8000 >nul 2>&1
)

:: 4. Cai thu vien va chay
echo [3/3] Dang cai thu vien va chay Server (Goi setup.bat)...
call setup.bat
if errorlevel 1 (
    echo [ERROR] Cai dat that bai.
    pause
    exit /b
)

echo Dang khoi dong Server...
timeout /t 3
python -m uvicorn web.server:app --host 0.0.0.0 --port 8000
pause
