#!/usr/bin/env python3
"""
Quick Dashboard Regeneration Script

This script regenerates the interactive dashboard using the enhanced dataset
with 575+ businesses instead of the smaller processed dataset.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analysis.market_analysis import FitnessMarketAnalyzer
from pathlib import Path

# Check and use enhanced data
enhanced_data_file = 'data/output/pune_enhanced_final.csv'

if Path(enhanced_data_file).exists():
    print(f"✅ Found enhanced dataset: {enhanced_data_file}")
    analyzer = FitnessMarketAnalyzer(enhanced_data_file)
    
    if analyzer.data is not None and not analyzer.data.empty:
        print(f"📊 Loaded {len(analyzer.data)} businesses successfully!")
        
        # Regenerate dashboard
        print("🎨 Generating interactive dashboard...")
        analyzer.create_interactive_dashboard()
        
        print("📈 Generating market overview chart...")
        analyzer.create_market_overview_chart()
        
        print("✅ Dashboard regenerated successfully!")
        print(f"🌐 Open: file:///c:/project/data/output/interactive_dashboard.html")
    else:
        print("❌ Failed to load data")
else:
    print(f"❌ Enhanced data file not found: {enhanced_data_file}")