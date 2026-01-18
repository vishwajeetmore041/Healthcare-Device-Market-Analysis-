@echo off
setlocal enabledelayedexpansion

echo.
echo ================================================================
echo   AUTOMATED MARKET ANALYSIS SETUP ^& EXECUTION
echo ================================================================
echo.
echo This will automatically:
echo   ✅ Check/Install Python 3.9-3.12
echo   ✅ Setup Anaconda environment (if available)
echo   ✅ Install all required dependencies
echo   ✅ Run complete market analysis
echo   ✅ Start web server and open results
echo.
echo Starting automated setup...
echo.

REM Change to script directory
cd /d "%~dp0"

REM =================================================================
REM STEP 1: PYTHON VERSION DETECTION AND MANAGEMENT
REM =================================================================
echo [STEP 1/5] Checking Python installation...

set PYTHON_CMD=
set PYTHON_VERSION=
set ANACONDA_DETECTED=0

REM Check for Anaconda Python first
if exist "%USERPROFILE%\Anaconda3\python.exe" (
    set PYTHON_CMD="%USERPROFILE%\Anaconda3\python.exe"
    set ANACONDA_DETECTED=1
    echo ✅ Found Anaconda Python
) else if exist "%USERPROFILE%\Miniconda3\python.exe" (
    set PYTHON_CMD="%USERPROFILE%\Miniconda3\python.exe"
    set ANACONDA_DETECTED=1
    echo ✅ Found Miniconda Python
) else if exist "C:\ProgramData\Anaconda3\python.exe" (
    set PYTHON_CMD="C:\ProgramData\Anaconda3\python.exe"
    set ANACONDA_DETECTED=1
    echo ✅ Found System Anaconda Python
)

REM Check system Python if no Anaconda
if not defined PYTHON_CMD (
    python --version >nul 2>&1
    if !errorlevel! == 0 (
        for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYTHON_VERSION=%%v
        set PYTHON_CMD=python
        echo ✅ Found System Python !PYTHON_VERSION!
    )
)

REM If no Python found, install it
if not defined PYTHON_CMD (
    echo ❌ No suitable Python found. Installing Python 3.11...
    
    REM Download and install Python 3.11
    echo Downloading Python 3.11.9...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python-installer.exe'}"
    
    if exist python-installer.exe (
        echo Installing Python 3.11.9...
        python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        
        REM Wait for installation
        timeout /t 30 /nobreak >nul
        
        REM Clean up
        del python-installer.exe
        
        REM Refresh PATH
        call refreshenv >nul 2>&1
        
        REM Try to find Python again
        python --version >nul 2>&1
        if !errorlevel! == 0 (
            set PYTHON_CMD=python
            echo ✅ Python 3.11.9 installed successfully
        ) else (
            echo ❌ Python installation failed. Please install Python manually.
            pause
            exit /b 1
        )
    ) else (
        echo ❌ Failed to download Python installer
        echo Please install Python 3.9+ manually from https://python.org
        pause
        exit /b 1
    )
)

echo Python Command: !PYTHON_CMD!
echo.

REM =================================================================
REM STEP 2: CONDA ENVIRONMENT SETUP (if Anaconda detected)
REM =================================================================
if !ANACONDA_DETECTED! == 1 (
    echo [STEP 2/5] Setting up Anaconda environment...
    
    REM Try to activate conda
    call conda activate base >nul 2>&1
    if !errorlevel! == 0 (
        echo ✅ Activated Anaconda base environment
    ) else (
        REM Try alternative conda paths
        if exist "%USERPROFILE%\Anaconda3\Scripts\activate.bat" (
            call "%USERPROFILE%\Anaconda3\Scripts\activate.bat" base
        ) else if exist "%USERPROFILE%\Miniconda3\Scripts\activate.bat" (
            call "%USERPROFILE%\Miniconda3\Scripts\activate.bat" base
        ) else if exist "C:\ProgramData\Anaconda3\Scripts\activate.bat" (
            call "C:\ProgramData\Anaconda3\Scripts\activate.bat" base
        )
        echo ✅ Conda environment setup complete
    )
) else (
    echo [STEP 2/5] Using system Python (no Anaconda detected)
)
echo.

REM =================================================================
REM STEP 3: DEPENDENCY INSTALLATION
REM =================================================================
echo [STEP 3/5] Installing dependencies...

if !ANACONDA_DETECTED! == 1 (
    echo Installing via Conda + Pip...
    
    REM Install conda packages
    echo Installing core packages via conda...
    conda install -y pandas numpy scikit-learn selenium beautifulsoup4 plotly matplotlib seaborn >nul 2>&1
    if !errorlevel! == 0 (
        echo ✅ Conda packages installed
    ) else (
        echo ⚠️ Some conda packages failed, continuing with pip...
    )
    
    REM Install pip-only packages
    echo Installing specialized packages via pip...
    !PYTHON_CMD! -m pip install --upgrade pip >nul 2>&1
    !PYTHON_CMD! -m pip install undetected-chromedriver selenium-stealth webdriver-manager fake-useragent loguru tqdm python-dotenv aiohttp aiofiles openpyxl joblib >nul 2>&1
    if !errorlevel! == 0 (
        echo ✅ Pip packages installed
    ) else (
        echo ❌ Some pip packages failed
    )
) else (
    echo Installing all packages via pip...
    !PYTHON_CMD! -m pip install --upgrade pip >nul 2>&1
    !PYTHON_CMD! -m pip install -r requirements.txt >nul 2>&1
    if !errorlevel! == 0 (
        echo ✅ All packages installed via pip
    ) else (
        echo ❌ Package installation failed
        echo Trying individual package installation...
        
        !PYTHON_CMD! -m pip install pandas numpy scikit-learn selenium beautifulsoup4 plotly matplotlib seaborn >nul 2>&1
        !PYTHON_CMD! -m pip install undetected-chromedriver selenium-stealth webdriver-manager fake-useragent >nul 2>&1
        !PYTHON_CMD! -m pip install loguru tqdm python-dotenv aiohttp aiofiles openpyxl joblib >nul 2>&1
        echo ✅ Individual package installation completed
    )
)

REM Verify critical packages
echo Verifying critical packages...
!PYTHON_CMD! -c "import pandas, selenium, undetected_chromedriver; print('✅ Critical packages verified')" 2>nul
if !errorlevel! == 0 (
    echo ✅ All critical dependencies verified
) else (
    echo ❌ Some critical packages missing, but continuing...
)
echo.

REM =================================================================
REM STEP 4: CHROME/CHROMIUM SETUP FOR SELENIUM
REM =================================================================
echo [STEP 4/5] Setting up browser driver...

REM Check if Chrome is installed
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" >nul 2>&1
if !errorlevel! == 0 (
    echo ✅ Google Chrome detected
) else (
    echo ⚠️ Chrome not found, checking for Edge...
    reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe" >nul 2>&1
    if !errorlevel! == 0 (
        echo ✅ Microsoft Edge detected (can be used as fallback)
    ) else (
        echo ⚠️ No suitable browser found. Chrome will be downloaded automatically if needed.
    )
)
echo.

REM =================================================================
REM STEP 5: RUN MARKET ANALYSIS
REM =================================================================
echo [STEP 5/5] Starting Market Analysis System...
echo.
echo ================================================================
echo   LAUNCHING AUTOMATED MARKET ANALYSIS
echo ================================================================
echo.

REM Run the analysis
!PYTHON_CMD! run_analysis.py

REM Check if successful
if !errorlevel! == 0 (
    echo.
    echo ================================================================
    echo   ✅ SETUP AND ANALYSIS COMPLETED SUCCESSFULLY!
    echo ================================================================
    echo.
    echo Your market analysis is now running at:
    echo   🌐 http://localhost:8080/interactive_dashboard.html
    echo   🌐 http://localhost:8080/phase4_results_interactive.html
    echo.
    echo The web server is running. Press Ctrl+C in the Python window to stop.
    echo.
) else (
    echo.
    echo ================================================================
    echo   ❌ ANALYSIS FAILED
    echo ================================================================
    echo.
    echo Possible solutions:
    echo   1. Run this script as Administrator
    echo   2. Check your internet connection
    echo   3. Manually install Python 3.9+ from python.org
    echo   4. Contact support with error details
    echo.
)

echo.
echo Press any key to exit setup...
pause >nul

endlocal