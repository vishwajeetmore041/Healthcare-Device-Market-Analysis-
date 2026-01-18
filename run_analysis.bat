@echo off
echo.
echo ================================
echo   MARKET ANALYSIS - ONE CLICK
echo ================================
echo.
echo Starting market analysis...
echo This will take a few minutes.
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Run the Python script
python run_analysis.py

echo.
echo Press any key to exit...
pause >nul