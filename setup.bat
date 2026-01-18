@echo off
setlocal enabledelayedexpansion

echo ================================================================
echo   QODER AI - CLEAN SETUP SCRIPT
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYTHON_VERSION=%%v
echo ✅ Python !PYTHON_VERSION! found

REM Check if virtual environment already exists
if exist ".venv" (
    echo ✅ Virtual environment already exists. Skipping creation.
    echo To recreate it, delete the .venv folder and run this script again.
) else (
    echo 🚀 Creating virtual environment...
    python -m venv .venv
    if !errorlevel! neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created successfully
)

echo.
echo 📦 Installing/updating dependencies...

REM Activate virtual environment and install requirements
call .venv\Scripts\activate.bat
if !errorlevel! neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip to latest version
python -m pip install --upgrade pip >nul 2>&1

REM Install requirements
if exist "requirements.txt" (
    pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo ❌ Failed to install requirements
        pause
        exit /b 1
    )
    echo ✅ All dependencies installed successfully
) else (
    echo ⚠️  requirements.txt not found
    echo Installing core packages...
    pip install pandas numpy scikit-learn selenium beautifulsoup4 plotly matplotlib seaborn
    pip install undetected-chromedriver selenium-stealth webdriver-manager fake-useragent loguru tqdm python-dotenv aiohttp aiofiles openpyxl joblib
    echo ✅ Core packages installed
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo To run the project:
echo   1. Run: run_project.bat
echo   2. Or manually:
echo      a. Activate environment: call .venv\Scripts\activate.bat
echo      b. Run analysis: python run_analysis.py
echo.
pause