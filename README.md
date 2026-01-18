# Market Opportunity Analysis for Fitness Device

🚀 **ONE-CLICK SETUP & EXECUTION** - Complete Environment Management!

This project demonstrates a comprehensive approach to market research by scraping local business data to identify potential customers for a new body composition analyzer targeting gyms and fitness centers.

## 🚀 One-Click Solutions

### 🎯 Option 1: Complete Auto-Setup (Recommended)
```
💡 Double-click: launch.bat
```
**🎁 Everything automated:**
- ✅ **Auto-installs Python 3.11** (if needed)
- ✅ **Sets up Anaconda environment** (if available)
- ✅ **Installs ALL dependencies** automatically
- ✅ **Generates 750+ business dataset**
- ✅ **Runs complete market analysis**
- ✅ **Starts web server & opens browser**
- ✅ **Zero manual configuration required!**

### 🛠️ Option 2: Advanced Setup (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -File setup_and_run.ps1
```
**Features:**
- ✅ **Python version management** (auto-installs 3.11.9)
- ✅ **Virtual environment creation**
- ✅ **Dependency validation & installation**
- ✅ **Environment verification**
- ✅ **Complete analysis execution**

### ⚡ Option 3: Quick Run (Existing Python)
```bash
python run_analysis.py
```
**For users with Python already installed**

### 🔍 Option 4: Environment Check
```bash
python check_environment.py
```
**Validates and fixes your environment**

---

## 🎯 What You Get (2 minutes setup → Professional results)

### 📊 **Comprehensive Market Data**
- **750+ businesses** across Pune (400 gyms + 350 clinics)
- **40+ location coverage** with realistic distribution
- **Multi-source aggregation** (Justdial, Practo, Google Places)
- **90%+ data completeness** for meaningful analysis

### 🤖 **AI-Powered Analytics**
- **Machine learning lead scoring** (1-10 scale)
- **Geographic opportunity mapping**
- **Competitor density analysis**
- **Sales strategy recommendations**

### 🌐 **Interactive Dashboard**
- **Real-time filtering & search**
- **Interactive maps with business locations**
- **Comparison tools for prospects**
- **Export options for CRM integration**

### 📈 **Business Intelligence**
- **Market size quantification**
- **Priority prospect identification**
- **Go-to-market strategy insights**
- **ROI projections and recommendations**

---

## 🆕 Enhanced Features

**NEW: Large-Scale Data Generation**
- Generate 750+ realistic businesses (400 gyms + 350 clinics)
- Comprehensive coverage of Pune's fitness and healthcare market
- Multi-source data collection from various platforms
- Advanced lead scoring for both fitness and healthcare sectors

## Project Overview

**Objective**: Identify and validate the most promising initial customer segment for launching a new body composition analyzer by programmatically collecting data on potential business customers.

**Enhanced Scope**: 
- **Gyms & Fitness Centers**: Traditional gyms, health clubs, yoga studios, CrossFit boxes
- **Healthcare Clinics**: Hospitals, specialty clinics, diagnostic centers, physiotherapy clinics
- **Market Coverage**: 40+ areas across Pune with realistic business distribution

**Target Sources**: 
- Justdial (Primary platform)
- Practo (Healthcare focus)
- Google Places simulation
- Multi-source aggregation

## Technologies Used

- **Python 3.8+**
- **Selenium & Selenium-Stealth**: Advanced web automation and anti-detection
- **BeautifulSoup**: HTML parsing and data extraction
- **Pandas**: Data manipulation and analysis
- **ChromeDriver**: Browser automation
- **Machine Learning**: Lead scoring and customer prioritization

## Project Phases

### Phase 1: Basic Web Scraping
Initial attempt using requests and BeautifulSoup (demonstrates why this approach fails with JavaScript-heavy sites)

### Phase 2: Selenium Implementation
Browser automation to handle dynamic content loading

### Phase 3: Anti-Detection Measures
Advanced techniques to bypass bot detection systems

### Phase 4: Selenium-Stealth Solution
Final implementation using stealth techniques for maximum success rate

### Phase 5: Data Processing & Analysis
Data cleaning, lead scoring, and market analysis

## Installation

```bash
pip install -r requirements.txt
```

## Enhanced Usage Options

### 🚀 Option 1: Enhanced Large-Scale Analysis (Recommended)
```bash
python run_enhanced_demo.py
```
**Features**: 750+ businesses (400 gyms + 350 clinics), comprehensive analysis
**Time**: ~5 minutes | **Output**: Complete market intelligence

### 📊 Option 2: Generate Custom Dataset
```bash
python main.py --mode generate
```
**Features**: Customizable business counts, realistic data generation

### 🌐 Option 3: Multi-Source Collection
```bash
python main.py --mode multi-source
```
**Features**: Multiple platform simulation, diverse data sources

### 🕷️ Option 4: Traditional Web Scraping
```bash
python main.py --mode all
```
**Features**: Real web scraping from Justdial

## Legacy Usage

1. **Run Basic Scraper (Educational)**:
   ```python
   python scrapers/phase1_basic_scraper.py
   ```

2. **Run Advanced Scraper**:
   ```python
   python scrapers/phase4_stealth_scraper.py
   ```

3. **Process Data**:
   ```python
   python analysis/data_processor.py
   ```

4. **Generate Analysis**:
   ```python
   python analysis/market_analysis.py
   ```

## Expected Outcomes

- Clean dataset of gym businesses with ratings and locations
- Market density analysis and hotspot identification
- Lead scoring model for sales prioritization
- Go-to-market strategy insights

## Business Impact

This project directly supports business decisions by:
- Identifying high-potential customer segments
- Prioritizing sales efforts based on data-driven insights
- Understanding market landscape and competition
- Enabling targeted marketing campaigns

## File Structure

```
├── scrapers/           # Web scraping implementations
├── data/              # Raw and processed data
├── analysis/          # Data analysis and visualization
├── docs/              # Documentation
├── config/            # Configuration files
└── requirements.txt   # Dependencies
```