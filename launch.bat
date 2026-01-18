@echo off
echo.
echo ================================================================
echo   MARKET ANALYSIS - ONE-CLICK LAUNCHER
echo ================================================================
echo.
echo Choose your setup method:
echo.
echo   [1] Quick Setup (Batch) - Uses existing Python/Anaconda
echo   [2] Advanced Setup (PowerShell) - Full environment management
echo   [3] Manual Commands - Show manual installation steps
echo   [4] Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto quick_setup
if "%choice%"=="2" goto advanced_setup  
if "%choice%"=="3" goto manual_commands
if "%choice%"=="4" goto exit
goto invalid_choice

:quick_setup
echo.
echo Starting Quick Setup (using existing Python/Anaconda)...
echo.
call setup_and_run.bat
goto end

:advanced_setup
echo.
echo Starting Advanced Setup (full environment management)...
echo.
powershell -ExecutionPolicy Bypass -File setup_and_run.ps1
goto end

:manual_commands
echo.
echo ================================================================
echo   MANUAL INSTALLATION COMMANDS
echo ================================================================
echo.
echo If you prefer to install manually, run these commands:
echo.
echo 1. In Anaconda Prompt:
echo    conda install -y pandas numpy scikit-learn selenium beautifulsoup4 plotly
echo    pip install undetected-chromedriver selenium-stealth
echo.
echo 2. Or with regular Python:
echo    pip install -r requirements.txt
echo.
echo 3. Then run the analysis:
echo    python run_analysis.py
echo.
echo ================================================================
pause
goto end

:invalid_choice
echo.
echo Invalid choice. Please enter 1, 2, 3, or 4.
pause
goto start

:exit
echo.
echo Goodbye!
goto end

:end