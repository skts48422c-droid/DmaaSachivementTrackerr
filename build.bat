@echo off
echo ============================================
echo  DmaaS Achievement Tracker - build script
echo ============================================
echo This installs the build tools and produces a single
echo DmaaS-Achievement-Tracker.exe file in the "dist" folder.
echo Only the person running THIS script needs Python installed.
echo Everyone else just receives the finished .exe.
echo.
pause

python --version >nul 2>&1
if errorlevel 1 (
    echo Python was not found on this machine.
    echo Install Python 3.9+ from https://www.python.org/downloads/
    echo   IMPORTANT: tick "Add python.exe to PATH" during install.
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

echo Building the .exe...
pyinstaller --onefile --windowed --add-data "ui.html;." --name "DmaaS-Achievement-Tracker" app.py

echo.
echo ============================================
echo  Done. Find DmaaS-Achievement-Tracker.exe
echo  inside the "dist" folder.
echo  That single file is all you need to share
echo  with the rest of the team - they don't need
echo  Python installed to run it.
echo ============================================
pause
