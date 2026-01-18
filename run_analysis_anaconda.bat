@echo off
echo.
echo ================================================
echo   MARKET ANALYSIS - ANACONDA ONE-CLICK
echo ================================================
echo.
echo Starting market analysis with Anaconda...
echo This will take about 2 minutes.
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Try to activate conda base environment
echo Activating Anaconda environment...
call conda activate base 2>nul

REM If conda activation fails, try to find conda
if errorlevel 1 (
    echo Searching for Anaconda installation...
    
    REM Try common Anaconda paths
    if exist "%USERPROFILE%\Anaconda3\Scripts\activate.bat" (
        call "%USERPROFILE%\Anaconda3\Scripts\activate.bat" base
    ) else if exist "%USERPROFILE%\Miniconda3\Scripts\activate.bat" (
        call "%USERPROFILE%\Miniconda3\Scripts\activate.bat" base
    ) else if exist "C:\Anaconda3\Scripts\activate.bat" (
        call "C:\Anaconda3\Scripts\activate.bat" base
    ) else if exist "C:\ProgramData\Anaconda3\Scripts\activate.bat" (
        call "C:\ProgramData\Anaconda3\Scripts\activate.bat" base
    ) else (
        echo.
        echo Warning: Could not find Anaconda installation.
        echo Trying with system Python...
        echo.
    )
)

REM Run the Python script
echo.
echo Starting market analysis pipeline...
echo.
python run_analysis.py

REM Check if successful
if errorlevel 1 (
    echo.
    echo ============================================
    echo   ERROR: Analysis failed to complete
    echo ============================================
    echo.
    echo Possible solutions:
    echo 1. Open Anaconda Prompt manually
    echo 2. Navigate to project folder: cd c:\project
    echo 3. Run: python run_analysis.py
    echo.
    echo Or install missing packages:
    echo conda install pandas numpy scikit-learn selenium beautifulsoup4 plotly
    echo pip install undetected-chromedriver selenium-stealth
    echo.
) else (
    echo.
    echo ============================================
    echo   SUCCESS: Analysis completed!
    echo ============================================
    echo.
    echo Your interactive dashboard is now running at:
    echo http://localhost:8080/interactive_dashboard.html
    echo.
    echo Press Ctrl+C in the Python window to stop the server.
    echo.
)

echo.
echo Press any key to exit...
pause >nul