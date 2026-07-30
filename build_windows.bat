@echo off
echo ========================================================
echo Building Battery Alert (.exe) for Windows
echo ========================================================
echo.

pip install -r requirements.txt

pyinstaller --noconfirm --onedir --windowed --name "BatteryAlert" ^
    --icon "icon/app.ico" ^
    --add-data "assets;assets" ^
    --add-data "config;config" ^
    --add-data "icon;icon" ^
    app.py

echo.
echo ========================================================
echo SUCCESS! BatteryAlert.exe built at:
echo dist\BatteryAlert\BatteryAlert.exe
echo ========================================================
pause
