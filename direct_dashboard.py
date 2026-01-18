#!/usr/bin/env python3
"""
Direct Dashboard Generator
Creates dashboard directly from comprehensive dataset without processing pipeline
"""

import pandas as pd
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from analysis.market_analysis import FitnessMarketAnalyzer

def main():
    print("🔧 Direct Dashboard Generator")
    print("=" * 50)
    
    # Use the comprehensive dataset directly
    data_file = 'data/output/pune_comprehensive_market_data.csv'
    
    try:
        # Check if file exists and has data
        if not Path(data_file).exists():
            print(f"❌ File not found: {data_file}")
            return False
            
        df = pd.read_csv(data_file)
        print(f"✅ Found dataset with {len(df)} businesses")
        
        if len(df) < 100:
            print(f"⚠️  Dataset seems small ({len(df)} records). Checking for larger dataset...")
            # Try to find a backup with more data
            alt_files = [
                'data/output/pune_comprehensive_market_data_backup.csv',
                'data/output/pune_enhanced_final.csv'
            ]
            
            for alt_file in alt_files:
                if Path(alt_file).exists():
                    alt_df = pd.read_csv(alt_file)
                    if len(alt_df) > len(df):
                        print(f"✅ Using larger dataset: {alt_file} ({len(alt_df)} records)")
                        data_file = alt_file
                        df = alt_df
                        break
        
        # Show data summary
        print(f"\n📊 Dataset Summary:")
        print(f"   • Total businesses: {len(df)}")
        
        if 'business_category' in df.columns:
            categories = df['business_category'].value_counts()
            print(f"   • Business categories: {len(categories)}")
            print(f"   • Top categories: {', '.join(categories.head(3).index.tolist())}")
            
        if 'rating' in df.columns:
            ratings = df['rating'].dropna()
            if len(ratings) > 0:
                print(f"   • Businesses with ratings: {len(ratings)}")
                print(f"   • Average rating: {ratings.mean():.2f}")
                print(f"   • Rating range: {ratings.min():.1f} - {ratings.max():.1f}")
        
        # Create analyzer and run analysis
        print(f"\n🔄 Generating dashboard...")
        analyzer = FitnessMarketAnalyzer(data_file)
        
        # Run complete analysis to generate all visualizations
        analyzer.run_complete_analysis()
        
        print(f"✅ Dashboard generated successfully!")
        print(f"   • File: data/output/interactive_dashboard.html")
        print(f"   • Market overview: data/output/market_overview.png")
        print(f"   • Analysis report: data/output/market_analysis_report.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print(f"\n🎉 SUCCESS!")
        print(f"📂 Dashboard is ready with comprehensive data!")
        print(f"🌐 Open: data/output/interactive_dashboard.html")
    else:
        print(f"\n❌ FAILED!")
    
    print("\nPress Enter to exit...")
    input()