@echo off
REM Jhopan VPN Bot - Installation Script
REM For Windows

echo ====================================
echo Jhopan VPN Bot - Installation
echo ====================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Upgrading pip...
python -m pip install --upgrade pip

echo [4/4] Installing dependencies...
pip install -r requirements.txt

echo.
echo ====================================
echo Installation Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env
echo    copy .env.example .env
echo.
echo 2. Edit .env and add your bot token
echo    notepad .env
echo.
echo 3. Run the bot:
echo    venv\Scripts\activate
echo    python bot.py
echo.
pause
