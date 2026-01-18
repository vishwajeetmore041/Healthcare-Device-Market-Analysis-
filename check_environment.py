#!/usr/bin/env python3
"""
Environment Validation Script
Checks if all dependencies are properly installed and compatible
"""

import sys
import importlib
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.9+")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed and can be imported"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name}")
        return True
    except ImportError:
        print(f"❌ {package_name} - Not installed")
        return False

def install_missing_packages(missing_packages):
    """Install missing packages"""
    if not missing_packages:
        return True
    
    print(f"\n📦 Installing {len(missing_packages)} missing packages...")
    
    try:
        # Try conda first if available
        conda_env = os.environ.get('CONDA_DEFAULT_ENV')
        if conda_env:
            print("🐍 Using conda for compatible packages...")
            conda_packages = ['pandas', 'numpy', 'scikit-learn', 'selenium', 'beautifulsoup4', 'plotly']
            pip_packages = ['undetected-chromedriver', 'selenium-stealth', 'webdriver-manager', 'fake-useragent']
            
            conda_to_install = [pkg for pkg in missing_packages if pkg in conda_packages]
            pip_to_install = [pkg for pkg in missing_packages if pkg in pip_packages or pkg not in conda_packages]
            
            if conda_to_install:
                subprocess.run(['conda', 'install', '-y'] + conda_to_install, check=True)
            
            if pip_to_install:
                subprocess.run([sys.executable, '-m', 'pip', 'install'] + pip_to_install, check=True)
        else:
            # Use pip for all packages
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages, check=True)
        
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def main():
    """Main validation function"""
    print("🔍 ENVIRONMENT VALIDATION")
    print("=" * 50)
    
    # Check Python version
    python_ok = check_python_version()
    
    # Define required packages
    required_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy', 
        'scikit-learn': 'sklearn',
        'selenium': 'selenium',
        'beautifulsoup4': 'bs4',
        'plotly': 'plotly',
        'undetected-chromedriver': 'undetected_chromedriver',
        'selenium-stealth': 'selenium_stealth',
        'requests': 'requests',
        'matplotlib': 'matplotlib',
        'loguru': 'loguru'
    }
    
    print(f"\n📦 CHECKING {len(required_packages)} REQUIRED PACKAGES:")
    print("-" * 50)
    
    missing = []
    for package_name, import_name in required_packages.items():
        if not check_package(package_name, import_name):
            missing.append(package_name)
    
    # Summary
    print("\n" + "=" * 50)
    if python_ok and not missing:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Environment is ready for market analysis")
        return True
    else:
        print("❌ ENVIRONMENT ISSUES DETECTED")
        if not python_ok:
            print("   • Python version incompatible (need 3.9+)")
        if missing:
            print(f"   • {len(missing)} packages missing: {', '.join(missing)}")
        
        # Offer to install missing packages
        if missing:
            print(f"\n🔧 AUTOMATIC FIX AVAILABLE")
            response = input("Install missing packages automatically? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                return install_missing_packages(missing)
        
        return False

if __name__ == "__main__":
    import os
    success = main()
    
    if success:
        print("\n🚀 READY TO RUN ANALYSIS!")
        print("Execute: python run_analysis.py")
    else:
        print("\n🔧 MANUAL INSTALLATION REQUIRED:")
        print("   conda install -y pandas numpy scikit-learn selenium beautifulsoup4 plotly")
        print("   pip install undetected-chromedriver selenium-stealth")
    
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)