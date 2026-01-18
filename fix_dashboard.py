#!/usr/bin/env python3
"""
Fix Dashboard Script - Regenerate dashboard with comprehensive dataset
"""

import pandas as pd
import logging
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from analysis.market_analysis import FitnessMarketAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Fix the dashboard by using the comprehensive dataset"""
    
    print("="*60)
    print("FIXING DASHBOARD WITH COMPREHENSIVE DATASET")
    print("="*60)
    
    # Check data files
    data_files = [
        'data/output/pune_comprehensive_market_data.csv',  # 752 businesses
        'data/output/pune_enhanced_final.csv',            # 575+ businesses  
        'data/output/multi_source_comprehensive_data.csv', # Multi-source data
        'data/output/pune_gyms_final.csv'                # 14 businesses (fallback)
    ]
    
    selected_file = None
    for data_file in data_files:
        if Path(data_file).exists():
            df = pd.read_csv(data_file)
            print(f"✓ Found: {data_file} ({len(df)} records)")
            
            if selected_file is None:
                selected_file = data_file
                print(f"  → Selected as primary dataset")
            else:
                print(f"  → Available as backup")
        else:
            print(f"✗ Missing: {data_file}")
    
    if not selected_file:
        print("❌ No data files found!")
        return False
    
    print(f"\n📊 Using dataset: {selected_file}")
    
    # Load and analyze data
    try:
        df = pd.read_csv(selected_file)
        print(f"   • Total businesses: {len(df)}")
        
        # Check data quality
        if 'business_category' in df.columns:
            categories = df['business_category'].value_counts()
            print(f"   • Business categories: {len(categories)}")
            print(f"   • Top category: {categories.index[0]} ({categories.iloc[0]} businesses)")
        
        if 'rating' in df.columns:
            ratings = df['rating'].dropna()
            if len(ratings) > 0:
                print(f"   • Businesses with ratings: {len(ratings)}")
                print(f"   • Average rating: {ratings.mean():.2f}")
        
        # Create analyzer and regenerate dashboard
        print(f"\n🔄 Regenerating dashboard...")
        analyzer = FitnessMarketAnalyzer(selected_file)
        
        # Run analysis
        analyzer.generate_market_overview()
        analyzer.analyze_competition_landscape()
        analyzer.identify_market_opportunities()
        analyzer.generate_business_insights()
        
        # Create new dashboard
        analyzer.create_interactive_dashboard('data/output/interactive_dashboard.html')
        
        print(f"✅ Dashboard regenerated successfully!")
        print(f"   • File: data/output/interactive_dashboard.html")
        print(f"   • Data source: {selected_file}")
        print(f"   • Records processed: {len(df)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error regenerating dashboard: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print(f"\n🎉 SUCCESS! Dashboard has been fixed.")
        print(f"📂 Open: data/output/interactive_dashboard.html")
        print(f"🌐 Or start server: python run_analysis.py")
    else:
        print(f"\n❌ FAILED! Could not fix dashboard.")
    
    print("\nPress Enter to exit...")
    input()