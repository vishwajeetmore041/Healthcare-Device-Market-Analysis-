"""
Quick test to verify the data generator fix
"""
import sys
import traceback

try:
    from data_generator import EnhancedDataGenerator
    
    print("Testing data generator fix...")
    generator = EnhancedDataGenerator()
    
    # Test the problematic method
    print("Testing establishment year generation...")
    for i in range(5):
        year = generator.generate_establishment_year()
        print(f"  Generated year: {year}")
    
    print("✅ Establishment year generation works!")
    
    # Test small dataset generation
    print("Testing small dataset generation...")
    df = generator.generate_comprehensive_dataset(total_gyms=5, total_clinics=3)
    print(f"✅ Successfully generated {len(df)} businesses!")
    
    print("\nDataset sample:")
    print(df[['business_name', 'business_type', 'business_category', 'area']].head())
    
    print("\n🎉 Data generator fix verified!")
    print("The enhanced demo should now work correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nFull traceback:")
    traceback.print_exc()