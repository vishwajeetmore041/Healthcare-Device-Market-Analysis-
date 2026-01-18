@echo off
setlocal

echo ================================================================
echo   QODER AI - RUN ANALYSIS
echo ================================================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo ❌ Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo 🚀 Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Environment activated
echo.
echo 📊 Starting market analysis...

REM Run the analysis
python run_analysis.py

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Analysis completed successfully!
    echo.
    echo 🌐 Access your results at:
    echo    http://localhost:8080/interactive_dashboard.html
    echo    http://localhost:8080/phase4_results_interactive.html
    echo.
    echo Press any key to exit...
    pause >nul
) else (
    echo.
    echo ❌ Analysis failed. Check the error messages above.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)