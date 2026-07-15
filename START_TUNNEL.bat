@echo off
echo Dang tai xuong cong cu xuyen tuong lua (Cloudflare Tunnel)...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile 'cloudflared.exe'"
echo.
echo ========================================================
echo KHOI DONG THANH CONG! HAY COPY DUONG LINK HTTPS BEN DUOI:
echo ========================================================
echo.
cloudflared.exe tunnel --url http://127.0.0.1:80
pause
