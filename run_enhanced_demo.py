"""
Quick Demo Script for Enhanced Market Analysis

This script demonstrates the enhanced capabilities with large-scale data generation
for both gyms and clinics, showcasing the full potential of the market analysis system.
"""

import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_enhanced_demo():
    """Run enhanced demo with large-scale data"""
    
    print("\n" + "="*80)
    print("🚀 ENHANCED MARKET OPPORTUNITY ANALYSIS DEMO")
    print("="*80)
    
    print("\n📊 This demo will:")
    print("   • Generate 750+ realistic businesses (400 gyms + 350 clinics)")
    print("   • Include comprehensive business profiles with ratings, addresses, phones")
    print("   • Cover 40+ areas across Pune")
    print("   • Demonstrate advanced lead scoring on large dataset")
    print("   • Show market segmentation for both fitness and healthcare sectors")
    
    print("\n⏱️  Estimated time: 3-5 minutes")
    print("💾 Data size: ~2MB comprehensive dataset")
    
    # Ask for confirmation
    response = input("\n🤔 Run enhanced demo? (y/n): ").strip().lower()
    
    if response != 'y':
        print("Demo cancelled.")
        return
    
    print("\n🔄 Starting enhanced data generation...")
    
    try:
        # Generate enhanced data
        from data_generator import EnhancedDataGenerator
        
        generator = EnhancedDataGenerator()
        
        print("   📋 Generating comprehensive business dataset...")
        df = generator.generate_comprehensive_dataset(
            total_gyms=400,
            total_clinics=350
        )
        
        print("   💾 Saving enhanced dataset...")
        metadata = generator.save_enhanced_dataset(df)
        
        print(f"   ✅ Generated {len(df)} businesses successfully!")
        
        # Process the enhanced data
        print("\n🔄 Processing enhanced data...")
        
        from analysis.data_processor import FitnessDataProcessor
        
        processor = FitnessDataProcessor()
        clean_data = processor.process_all_data(
            input_file='data/output/pune_comprehensive_market_data.csv',
            output_file='data/output/pune_enhanced_final.csv'
        )
        
        print(f"   ✅ Processed {len(clean_data)} clean records!")
        
        # Run market analysis
        print("\n🔄 Running enhanced market analysis...")
        
        from analysis.market_analysis import FitnessMarketAnalyzer
        
        analyzer = FitnessMarketAnalyzer('data/output/pune_enhanced_final.csv')
        analyzer.run_complete_analysis()
        
        print("   ✅ Market analysis completed!")
        
        # Run lead scoring
        print("\n🔄 Running enhanced lead scoring...")
        
        from analysis.lead_scorer import FitnessLeadScorer
        
        scorer = FitnessLeadScorer()
        data = scorer.load_data('data/output/pune_enhanced_final.csv')
        
        # Feature engineering and model training
        featured_data = scorer.engineer_features(data)
        X, y = scorer.prepare_training_data(featured_data)
        training_results = scorer.train_model(X, y)
        
        # Score all leads
        scored_data = scorer.score_leads(data)
        recommendations = scorer.generate_sales_recommendations(scored_data)
        
        # Save results
        scored_data.to_csv('data/output/enhanced_scored_leads.csv', index=False)
        
        import json
        with open('data/output/enhanced_sales_recommendations.json', 'w') as f:
            json.dump(recommendations, f, indent=2, default=str)
        
        print(f"   ✅ Lead scoring completed! Model R²: {training_results['test_r2']:.3f}")
        
        # Display results
        print("\n" + "="*80)
        print("🎉 ENHANCED DEMO COMPLETED SUCCESSFULLY!")
        print("="*80)
        
        print(f"\n📊 ENHANCED RESULTS SUMMARY:")
        print(f"   • Total businesses analyzed: {len(scored_data)}")
        print(f"   • Gym/Fitness businesses: {len(scored_data[scored_data['business_type'] == 'Gym/Fitness'])}")
        print(f"   • Healthcare/Clinic businesses: {len(scored_data[scored_data['business_type'] == 'Healthcare/Clinic'])}")
        print(f"   • Areas covered: {scored_data['area'].nunique()}")
        print(f"   • Average lead score: {scored_data['ml_lead_score'].mean():.2f}/10")
        print(f"   • High-priority targets: {len(scored_data[scored_data['priority_tier'] == 'Very High'])}")
        
        print(f"\n🏋️ TOP GYM CATEGORIES:")
        gym_categories = scored_data[scored_data['business_type'] == 'Gym/Fitness']['business_category'].value_counts()
        for category, count in gym_categories.head(5).items():
            print(f"   • {category}: {count} businesses")
        
        print(f"\n🏥 TOP CLINIC CATEGORIES:")
        clinic_categories = scored_data[scored_data['business_type'] == 'Healthcare/Clinic']['business_category'].value_counts()
        for category, count in clinic_categories.head(5).items():
            print(f"   • {category}: {count} businesses")
        
        print(f"\n🎯 TOP 5 PRIORITY TARGETS:")
        top_targets = scored_data.nlargest(5, 'ml_lead_score')
        for i, (_, target) in enumerate(top_targets.iterrows()):
            print(f"   {i+1}. {target['business_name']} (Score: {target['ml_lead_score']:.2f}, {target['business_type']})")
        
        print(f"\n📍 TOP BUSINESS AREAS:")
        top_areas = scored_data['area'].value_counts().head(5)
        for area, count in top_areas.items():
            print(f"   • {area}: {count} businesses")
        
        print(f"\n📁 ENHANCED FILES GENERATED:")
        print(f"   • Raw dataset: data/output/pune_comprehensive_market_data.csv")
        print(f"   • Clean dataset: data/output/pune_enhanced_final.csv")
        print(f"   • Scored leads: data/output/enhanced_scored_leads.csv")
        print(f"   • Sales recommendations: data/output/enhanced_sales_recommendations.json")
        print(f"   • Interactive dashboard: data/output/interactive_dashboard.html")
        print(f"   • Market overview: data/output/market_overview.png")
        
        print(f"\n💡 BUSINESS INSIGHTS:")
        print(f"   • Market size: {len(scored_data)} potential customers")
        print(f"   • Immediate targets: {len(scored_data[scored_data['ml_lead_score'] >= 7])} high-value prospects")
        print(f"   • Market coverage: Comprehensive across {scored_data['area'].nunique()} Pune areas")
        print(f"   • Data completeness: {(scored_data[['business_name', 'address', 'phone']].notna().sum().sum() / (len(scored_data) * 3) * 100):.1f}%")
        
        print(f"\n🚀 NEXT STEPS:")
        print(f"   1. Review interactive dashboard for visual insights")
        print(f"   2. Contact top-priority targets from scored leads")
        print(f"   3. Develop area-specific sales strategies")
        print(f"   4. Monitor market changes with regular data updates")
        
        print("\n" + "="*80)
        print("✨ Enhanced demo showcases 10x larger dataset with comprehensive insights!")
        print("="*80)
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"\n❌ Demo failed: {e}")
        print("Please check the logs and try again.")

if __name__ == "__main__":
    run_enhanced_demo()