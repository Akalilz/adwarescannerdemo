@echo off
cls
echo ========================================
echo   Android Adware Scanner - Web App
echo ========================================
echo.
echo Starting local web server...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 to 3.10 from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Python found! Checking dependencies...
echo.

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    echo This may take a few minutes...
    echo.
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies!
        echo Please run manually: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
    echo.
    echo Dependencies installed successfully!
    echo.
)

echo ========================================
echo   Starting Flask Server
echo ========================================
echo.
echo The app will open in your browser at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start Flask app
python app.py

REM If app exits
echo.
echo Server stopped.
pause
