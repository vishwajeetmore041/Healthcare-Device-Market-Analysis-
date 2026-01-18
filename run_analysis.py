#!/usr/bin/env python3
"""
🚀 One-Command Market Analysis Runner

This script runs the complete market analysis pipeline and automatically 
serves the interactive results on a local web server.

Usage:
    python run_analysis.py

That's it! Everything is automated:
✅ Generates comprehensive market data (750+ businesses)
✅ Processes and analyzes the data
✅ Creates interactive visualizations
✅ Serves results on local web server
✅ Opens browser automatically

No manual steps required!
"""

import os
import sys
import time
import subprocess
import webbrowser
import threading
import signal
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class SimpleMarketAnalysisRunner:
    def __init__(self):
        self.server_process = None
        self.project_dir = Path(__file__).parent
        
    def print_banner(self):
        """Print a nice banner"""
        conda_env = os.environ.get('CONDA_DEFAULT_ENV')
        python_info = f"Python {sys.version.split()[0]}"
        if conda_env:
            python_info += f" (Anaconda: {conda_env})"
            
        print("\n" + "="*70)
        print("🚀 ONE-COMMAND MARKET ANALYSIS SYSTEM")
        print("="*70)
        print("🎯 Target: Pune Gym & Healthcare Market Analysis")
        print("📊 Data: 750+ businesses across multiple categories")
        print("🤖 AI: Machine learning lead scoring")
        print("🌐 Output: Interactive web dashboard")
        print(f"🐍 Environment: {python_info}")
        print("="*70 + "\n")
        
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        logger.info("🔍 Checking dependencies...")
        
        # Check if running in Anaconda
        conda_env = os.environ.get('CONDA_DEFAULT_ENV')
        if conda_env:
            logger.info(f"✅ Detected Anaconda environment: {conda_env}")
        
        # Required packages to check
        required_packages = {
            'pandas': 'pandas',
            'plotly': 'plotly', 
            'sklearn': 'scikit-learn',
            'selenium': 'selenium',
            'undetected_chromedriver': 'undetected-chromedriver',
            'selenium_stealth': 'selenium-stealth',
            'bs4': 'beautifulsoup4'
        }
        
        missing_packages = []
        
        for module_name, package_name in required_packages.items():
            try:
                __import__(module_name)
                logger.info(f"✅ {module_name} found")
            except ImportError:
                missing_packages.append((module_name, package_name))
                logger.warning(f"❌ Missing: {module_name}")
        
        if not missing_packages:
            logger.info("✅ All dependencies found")
            return True
            
        logger.info(f"📦 Installing {len(missing_packages)} missing packages...")
        
        try:
            # Install missing packages
            conda_packages = ['pandas', 'numpy', 'scikit-learn', 'selenium', 'beautifulsoup4', 'plotly']
            pip_packages = ['undetected-chromedriver', 'selenium-stealth']
            
            if conda_env:
                logger.info("🐍 Installing conda packages...")
                conda_to_install = [pkg for _, pkg in missing_packages if pkg in conda_packages]
                if conda_to_install:
                    subprocess.run(["conda", "install", "-y"] + conda_to_install, 
                                 check=True, capture_output=True, text=True)
                    logger.info(f"✅ Conda packages installed: {', '.join(conda_to_install)}")
                
                logger.info("📦 Installing pip packages...")
                pip_to_install = [pkg for _, pkg in missing_packages if pkg in pip_packages or pkg not in conda_packages]
                if pip_to_install:
                    subprocess.run([sys.executable, "-m", "pip", "install"] + pip_to_install, 
                                 check=True, capture_output=True, text=True)
                    logger.info(f"✅ Pip packages installed: {', '.join(pip_to_install)}")
            else:
                # Fallback to pip for all packages
                all_packages = [pkg for _, pkg in missing_packages]
                subprocess.run([sys.executable, "-m", "pip", "install"] + all_packages, 
                             check=True, capture_output=True, text=True)
                logger.info(f"✅ All packages installed via pip: {', '.join(all_packages)}")
            
            # Verify installation
            logger.info("🔄 Verifying installation...")
            for module_name, _ in missing_packages:
                try:
                    __import__(module_name)
                    logger.info(f"✅ {module_name} now available")
                except ImportError:
                    logger.error(f"❌ {module_name} still not available after installation")
                    return False
            
            logger.info("✅ All dependencies installed and verified")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install packages: {e}")
            logger.info("\n🔧 Manual Installation Required:")
            if conda_env:
                logger.info("   Run these commands in Anaconda Prompt:")
                logger.info("   conda install -y pandas numpy scikit-learn selenium beautifulsoup4 plotly")
                logger.info("   pip install undetected-chromedriver selenium-stealth")
            else:
                logger.info("   pip install pandas numpy scikit-learn selenium beautifulsoup4 plotly")
                logger.info("   pip install undetected-chromedriver selenium-stealth")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error during installation: {e}")
            return False
                
    def run_analysis_pipeline(self):
        """Run the complete analysis pipeline"""
        logger.info("🚀 Starting market analysis pipeline...")
        
        # Step 1: Generate enhanced dataset (fastest option)
        logger.info("📊 Step 1/3: Generating comprehensive market data...")
        try:
            subprocess.run([sys.executable, "main.py", "--mode", "generate"], 
                         check=True, cwd=self.project_dir)
            logger.info("✅ Market data generated successfully")
        except subprocess.CalledProcessError:
            logger.error("❌ Failed to generate market data")
            return False
            
        # Step 2: Skip data processing to preserve comprehensive dataset
        logger.info("🧠 Step 2/3: Using generated comprehensive dataset (skipping processing to preserve data)...")
        logger.info("✅ Using comprehensive dataset with 750+ businesses")
            
        # Step 3: Generate analysis and lead scoring using comprehensive data
        logger.info("🎯 Step 3/3: Creating analysis and lead scores...")
        try:
            subprocess.run([sys.executable, "main.py", "--mode", "analyze"], 
                         check=True, cwd=self.project_dir)
            subprocess.run([sys.executable, "main.py", "--mode", "score"], 
                         check=True, cwd=self.project_dir)
            logger.info("✅ Analysis and scoring completed")
        except subprocess.CalledProcessError:
            logger.error("❌ Failed to complete analysis")
            return False
            
        return True
        
    def start_web_server(self):
        """Start local web server for interactive results"""
        logger.info("🌐 Starting local web server...")
        
        try:
            # Start server in data/output directory where HTML files are located
            output_dir = self.project_dir / "data" / "output"
            
            if not output_dir.exists():
                logger.error("❌ Output directory not found")
                return False
                
            # Start HTTP server
            self.server_process = subprocess.Popen(
                [sys.executable, "-m", "http.server", "8080"],
                cwd=output_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a moment for server to start
            time.sleep(2)
            
            if self.server_process.poll() is None:
                logger.info("✅ Web server started on http://localhost:8080")
                return True
            else:
                logger.error("❌ Failed to start web server")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error starting web server: {e}")
            return False
            
    def open_results_in_browser(self):
        """Open the interactive dashboard in the default browser"""
        logger.info("🌐 Opening interactive dashboard...")
        
        # List of possible dashboard files to open
        dashboard_urls = [
            "http://localhost:8080/interactive_dashboard.html",
            "http://localhost:8080/phase4_results_interactive.html"
        ]
        
        # Try to open the main dashboard
        try:
            webbrowser.open(dashboard_urls[0])
            logger.info("✅ Dashboard opened in browser")
            
            # Also show available results
            self.show_available_results()
            
        except Exception as e:
            logger.warning(f"⚠️  Could not auto-open browser: {e}")
            logger.info(f"🌐 Manually open: {dashboard_urls[0]}")
            
    def show_available_results(self):
        """Show available result files"""
        logger.info("\n📊 AVAILABLE RESULTS:")
        
        results = [
            ("Interactive Dashboard", "http://localhost:8080/interactive_dashboard.html"),
            ("Enhanced Gym Results", "http://localhost:8080/phase4_results_interactive.html"),
            ("Market Analysis Report", "http://localhost:8080/market_analysis_report.json"),
            ("Lead Scores CSV", "http://localhost:8080/scored_leads.csv"),
            ("Sales Recommendations", "http://localhost:8080/sales_recommendations.json")
        ]
        
        for name, url in results:
            print(f"   🔗 {name}: {url}")
            
    def show_success_summary(self):
        """Show final success summary"""
        print("\n" + "="*70)
        print("🎉 MARKET ANALYSIS COMPLETE!")
        print("="*70)
        print("📊 Generated comprehensive market data (750+ businesses)")
        print("🧠 Processed with AI-powered lead scoring")
        print("📈 Created interactive visualizations")
        print("🌐 Serving on local web server")
        print("="*70)
        print("\n🎯 KEY INSIGHTS AVAILABLE:")
        print("   • Market size & opportunity areas")
        print("   • Competition density mapping")
        print("   • Top 20% priority prospects")
        print("   • Sales strategy recommendations")
        print("\n🌐 ACCESS YOUR RESULTS:")
        print("   • Main Dashboard: http://localhost:8080/interactive_dashboard.html")
        print("   • Interactive Results: http://localhost:8080/phase4_results_interactive.html")
        print("\n⚡ Quick Actions:")
        print("   • Press Ctrl+C to stop server")
        print("   • Server runs at http://localhost:8080")
        print("   • All files saved in data/output/ directory")
        print("="*70 + "\n")
        
    def handle_shutdown(self, signum, frame):
        """Handle graceful shutdown"""
        logger.info("\n🛑 Shutting down server...")
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
        logger.info("✅ Server stopped. Goodbye!")
        sys.exit(0)
        
    def wait_for_shutdown(self):
        """Wait for user to stop the server"""
        try:
            logger.info("🔄 Server is running. Press Ctrl+C to stop...")
            while True:
                if self.server_process and self.server_process.poll() is not None:
                    logger.error("❌ Server stopped unexpectedly")
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            self.handle_shutdown(None, None)
            
    def run(self):
        """Run the complete one-command analysis"""
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.handle_shutdown)
        
        # Start the process
        self.print_banner()
        
        # Check dependencies
        if not self.check_dependencies():
            logger.error("❌ Dependency check failed")
            return False
            
        # Run analysis pipeline
        if not self.run_analysis_pipeline():
            logger.error("❌ Analysis pipeline failed")
            return False
            
        # Start web server
        if not self.start_web_server():
            logger.error("❌ Web server failed to start")
            return False
            
        # Open browser
        time.sleep(1)  # Give server a moment
        self.open_results_in_browser()
        
        # Show success summary
        self.show_success_summary()
        
        # Wait for shutdown
        self.wait_for_shutdown()
        
        return True

def main():
    """Main entry point"""
    runner = SimpleMarketAnalysisRunner()
    
    try:
        success = runner.run()
        if not success:
            logger.error("❌ Analysis failed!")
            sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()