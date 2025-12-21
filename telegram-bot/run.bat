@echo off
REM Jhopan VPN Bot - Run Script
REM Automatically activate venv and run bot

REM Check if venv exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Activate venv
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo .env created! Please edit it and add your bot token:
    echo    notepad .env
    echo.
    echo Then run run.bat again
    pause
    exit /b 1
)

REM Run bot
echo Starting Jhopan VPN Bot...
python main.py
pause
