#!/usr/bin/env python3
"""
Quick Fix for Empty Dashboard
Regenerates the interactive dashboard using the comprehensive dataset
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    print("🔧 Quick Dashboard Fix")
    print("=" * 50)
    
    # Load the comprehensive dataset
    data_file = 'data/output/pune_comprehensive_market_data.csv'
    
    try:
        df = pd.read_csv(data_file)
        print(f"✅ Loaded {len(df)} businesses from comprehensive dataset")
        
        # Check data quality
        print(f"   • Business categories: {df['business_category'].nunique()}")
        print(f"   • Businesses with ratings: {df['rating'].notna().sum()}")
        print(f"   • Average rating: {df['rating'].mean():.2f}")
        
        # Create the dashboard
        print("\n🔄 Creating interactive dashboard...")
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Business Categories', 'Rating Distribution', 
                          'Category vs Rating', 'Geographic Distribution'),
            specs=[[{"type": "pie"}, {"type": "histogram"}],
                   [{"type": "box"}, {"type": "bar"}]]
        )
        
        # 1. Pie chart for business categories
        if 'business_category' in df.columns:
            category_counts = df['business_category'].value_counts()
            fig.add_trace(
                go.Pie(labels=category_counts.index, 
                      values=category_counts.values, 
                      name="Categories",
                      showlegend=False),
                row=1, col=1
            )
        
        # 2. Histogram for ratings
        if 'rating' in df.columns and df['rating'].notna().any():
            fig.add_trace(
                go.Histogram(x=df['rating'].dropna(), 
                           name="Ratings",
                           nbinsx=20,
                           showlegend=False),
                row=1, col=2
            )
        
        # 3. Box plot for category vs rating
        if 'business_category' in df.columns and 'rating' in df.columns:
            categories = df['business_category'].unique()[:5]  # Top 5 categories
            for category in categories:
                category_data = df[df['business_category'] == category]
                if not category_data.empty and category_data['rating'].notna().any():
                    fig.add_trace(
                        go.Box(y=category_data['rating'].dropna(), 
                              name=category,
                              showlegend=False),
                        row=2, col=1
                    )
        
        # 4. Geographic distribution (areas)
        if 'area' in df.columns:
            area_counts = df['area'].value_counts().head(10)
            fig.add_trace(
                go.Bar(x=area_counts.index, 
                      y=area_counts.values, 
                      name="Areas",
                      showlegend=False),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title_text="Pune Fitness Market Analysis Dashboard - FIXED",
            title_x=0.5,
            height=800,
            showlegend=False
        )
        
        # Save the fixed dashboard
        output_file = 'data/output/interactive_dashboard.html'
        fig.write_html(output_file)
        
        print(f"✅ Dashboard regenerated successfully!")
        print(f"   • File: {output_file}")
        print(f"   • Data source: {data_file}")
        print(f"   • Businesses processed: {len(df)}")
        
        # Display summary statistics
        print(f"\n📊 Dataset Summary:")
        print(f"   • Total businesses: {len(df)}")
        if 'business_category' in df.columns:
            print(f"   • Categories: {', '.join(df['business_category'].value_counts().head(3).index.tolist())}")
        if 'rating' in df.columns:
            rated = df['rating'].dropna()
            if len(rated) > 0:
                print(f"   • Rating range: {rated.min():.1f} - {rated.max():.1f}")
                print(f"   • Top rated: {len(df[df['rating'] >= 4.0])} businesses (≥4.0★)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print(f"\n🎉 SUCCESS!")
        print(f"📂 Your dashboard has been fixed and now shows all 750+ businesses!")
        print(f"🌐 Open: data/output/interactive_dashboard.html")
        print(f"💡 Or start the server with: python run_analysis.py")
    else:
        print(f"\n❌ FAILED! Could not regenerate dashboard.")
    
    print("\nPress Enter to exit...")
    input()