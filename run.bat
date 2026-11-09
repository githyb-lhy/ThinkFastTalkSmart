@echo off
chcp 65001 >nul
title Think Fast, Talk Smart
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not installed. Install it from https://www.python.org/downloads/
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo [1/2] Creating virtual environment...
    python -m venv .venv || goto :fail
)

echo [2/2] Checking dependencies...
".venv\Scripts\python.exe" -m pip install -q --disable-pip-version-check -r requirements.txt || goto :fail

rem Skip Streamlit's first-run email prompt
if not exist "%USERPROFILE%\.streamlit\credentials.toml" (
    if not exist "%USERPROFILE%\.streamlit" mkdir "%USERPROFILE%\.streamlit"
    > "%USERPROFILE%\.streamlit\credentials.toml" (
        echo [general]
        echo email = ""
    )
)

echo.
echo Starting Think Fast, Talk Smart... (close this window to stop the app)
".venv\Scripts\python.exe" -m streamlit run app.py --browser.gatherUsageStats false
exit /b 0

:fail
echo [ERROR] Setup failed. See the messages above.
pause
exit /b 1
