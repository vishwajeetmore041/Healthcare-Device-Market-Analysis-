# Market Analysis - Complete Setup and Execution
# PowerShell Script for Windows

param(
    [string]$PythonVersion = "3.11.9"
)

# Set execution policy for this session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "   AUTOMATED MARKET ANALYSIS SETUP & EXECUTION" -ForegroundColor Yellow
Write-Host "================================================================`n" -ForegroundColor Cyan

Write-Host "This will automatically:" -ForegroundColor White
Write-Host "  ✅ Check/Install Python $PythonVersion" -ForegroundColor Green
Write-Host "  ✅ Setup virtual environment" -ForegroundColor Green  
Write-Host "  ✅ Install all required dependencies" -ForegroundColor Green
Write-Host "  ✅ Run complete market analysis" -ForegroundColor Green
Write-Host "  ✅ Start web server and open results`n" -ForegroundColor Green

# Change to script directory
Set-Location $PSScriptRoot

# =================================================================
# STEP 1: PYTHON VERSION DETECTION AND INSTALLATION
# =================================================================
Write-Host "[STEP 1/6] Checking Python installation..." -ForegroundColor Yellow

$pythonCmd = $null
$anacondaDetected = $false

# Check for Anaconda Python first
$anacondaPaths = @(
    "$env:USERPROFILE\Anaconda3\python.exe",
    "$env:USERPROFILE\Miniconda3\python.exe", 
    "C:\ProgramData\Anaconda3\python.exe",
    "C:\Anaconda3\python.exe"
)

foreach ($path in $anacondaPaths) {
    if (Test-Path $path) {
        $pythonCmd = $path
        $anacondaDetected = $true
        Write-Host "✅ Found Anaconda Python: $path" -ForegroundColor Green
        break
    }
}

# Check system Python if no Anaconda
if (-not $pythonCmd) {
    try {
        $version = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = "python"
            Write-Host "✅ Found System Python: $version" -ForegroundColor Green
        }
    } catch {
        # Python not found
    }
}

# Install Python if not found
if (-not $pythonCmd) {
    Write-Host "❌ No suitable Python found. Installing Python $PythonVersion..." -ForegroundColor Red
    
    $installerUrl = "https://www.python.org/ftp/python/$PythonVersion/python-$PythonVersion-amd64.exe"
    $installerPath = "python-installer.exe"
    
    try {
        Write-Host "Downloading Python $PythonVersion..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing
        
        Write-Host "Installing Python $PythonVersion..." -ForegroundColor Yellow
        Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0" -Wait
        
        # Clean up
        Remove-Item $installerPath -Force
        
        # Refresh environment
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        # Test installation
        try {
            $version = python --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $pythonCmd = "python"
                Write-Host "✅ Python $PythonVersion installed successfully" -ForegroundColor Green
            }
        } catch {
            Write-Host "❌ Python installation verification failed" -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "❌ Failed to install Python. Please install manually from python.org" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Python Command: $pythonCmd`n" -ForegroundColor Cyan

# =================================================================
# STEP 2: VIRTUAL ENVIRONMENT SETUP
# =================================================================
Write-Host "[STEP 2/6] Setting up virtual environment..." -ForegroundColor Yellow

$venvPath = "venv_market_analysis"

if ($anacondaDetected) {
    # Use conda environment
    Write-Host "Setting up Conda environment..." -ForegroundColor Cyan
    try {
        & conda create -n market_analysis python=$($PythonVersion.Substring(0,4)) -y 2>$null
        & conda activate market_analysis 2>$null
        Write-Host "✅ Conda environment created and activated" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Conda environment setup failed, using base environment" -ForegroundColor Yellow
    }
} else {
    # Use Python venv
    if (Test-Path $venvPath) {
        Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
    } else {
        Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
        & $pythonCmd -m venv $venvPath
        Write-Host "✅ Virtual environment created" -ForegroundColor Green
    }
    
    # Activate virtual environment
    & "$venvPath\Scripts\Activate.ps1"
    $pythonCmd = "$venvPath\Scripts\python.exe"
}

Write-Host ""

# =================================================================
# STEP 3: DEPENDENCY INSTALLATION  
# =================================================================
Write-Host "[STEP 3/6] Installing dependencies..." -ForegroundColor Yellow

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Cyan
& $pythonCmd -m pip install --upgrade pip --quiet

if ($anacondaDetected) {
    Write-Host "Installing packages via Conda + Pip..." -ForegroundColor Cyan
    
    # Core packages via conda
    $condaPackages = @("pandas", "numpy", "scikit-learn", "selenium", "beautifulsoup4", "plotly", "matplotlib", "seaborn")
    foreach ($package in $condaPackages) {
        Write-Host "Installing $package via conda..." -ForegroundColor Gray
        & conda install $package -y --quiet 2>$null
    }
    
    # Specialized packages via pip
    $pipPackages = @("undetected-chromedriver", "selenium-stealth", "webdriver-manager", "fake-useragent", "loguru", "tqdm", "python-dotenv", "aiohttp", "aiofiles", "openpyxl", "joblib")
    foreach ($package in $pipPackages) {
        Write-Host "Installing $package via pip..." -ForegroundColor Gray
        & $pythonCmd -m pip install $package --quiet
    }
} else {
    Write-Host "Installing all packages via pip..." -ForegroundColor Cyan
    
    # Try requirements.txt first
    if (Test-Path "requirements.txt") {
        & $pythonCmd -m pip install -r requirements.txt --quiet
    } else {
        # Manual package list
        $allPackages = @(
            "pandas", "numpy", "scikit-learn", "selenium", "beautifulsoup4", "plotly", 
            "matplotlib", "seaborn", "undetected-chromedriver", "selenium-stealth", 
            "webdriver-manager", "fake-useragent", "loguru", "tqdm", "python-dotenv", 
            "aiohttp", "aiofiles", "openpyxl", "joblib", "requests"
        )
        
        foreach ($package in $allPackages) {
            Write-Host "Installing $package..." -ForegroundColor Gray
            & $pythonCmd -m pip install $package --quiet
        }
    }
}

# Verify installation
Write-Host "Verifying critical packages..." -ForegroundColor Cyan
try {
    & $pythonCmd -c "import pandas, selenium, undetected_chromedriver; print('✅ Critical packages verified')"
    Write-Host "✅ All critical dependencies verified" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Some packages may be missing, but continuing..." -ForegroundColor Yellow
}

Write-Host ""

# =================================================================
# STEP 4: CHROME BROWSER CHECK
# =================================================================
Write-Host "[STEP 4/6] Checking browser availability..." -ForegroundColor Yellow

$chromeRegPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
$edgeRegPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe"

if (Test-Path $chromeRegPath) {
    Write-Host "✅ Google Chrome detected" -ForegroundColor Green
} elseif (Test-Path $edgeRegPath) {
    Write-Host "✅ Microsoft Edge detected (can be used as fallback)" -ForegroundColor Green
} else {
    Write-Host "⚠️ No browser detected. Chrome will be downloaded automatically if needed." -ForegroundColor Yellow
}

Write-Host ""

# =================================================================
# STEP 5: ENVIRONMENT VALIDATION
# =================================================================
Write-Host "[STEP 5/6] Validating environment..." -ForegroundColor Yellow

# Test Python execution
try {
    $pythonVersion = & $pythonCmd --version
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python execution failed" -ForegroundColor Red
    exit 1
}

# Test package imports
$testScript = @"
try:
    import pandas
    import selenium  
    import undetected_chromedriver
    import plotly
    print('✅ All packages imported successfully')
except ImportError as e:
    print(f'❌ Package import failed: {e}')
    exit(1)
"@

$testResult = & $pythonCmd -c $testScript
Write-Host $testResult -ForegroundColor Green

Write-Host ""

# =================================================================
# STEP 6: RUN MARKET ANALYSIS
# =================================================================
Write-Host "[STEP 6/6] Starting Market Analysis System..." -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   LAUNCHING AUTOMATED MARKET ANALYSIS" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Run the analysis
try {
    & $pythonCmd run_analysis.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "================================================================" -ForegroundColor Green
        Write-Host "   ✅ SETUP AND ANALYSIS COMPLETED SUCCESSFULLY!" -ForegroundColor Yellow
        Write-Host "================================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your market analysis is now running at:" -ForegroundColor White
        Write-Host "  🌐 http://localhost:8080/interactive_dashboard.html" -ForegroundColor Cyan
        Write-Host "  🌐 http://localhost:8080/phase4_results_interactive.html" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "The web server is running. Press Ctrl+C in the Python window to stop." -ForegroundColor Yellow
    } else {
        throw "Analysis script failed"
    }
} catch {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host "   ❌ ANALYSIS FAILED" -ForegroundColor Yellow
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible solutions:" -ForegroundColor White
    Write-Host "  1. Run this script as Administrator" -ForegroundColor Yellow
    Write-Host "  2. Check your internet connection" -ForegroundColor Yellow
    Write-Host "  3. Ensure all firewalls allow Python/pip" -ForegroundColor Yellow
    Write-Host "  4. Try running: python run_analysis.py manually" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null