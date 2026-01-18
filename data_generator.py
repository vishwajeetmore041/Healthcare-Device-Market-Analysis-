"""
Enhanced Data Generator for Market Opportunity Analysis

This module generates large-scale, realistic data for gyms and clinics in Pune
to demonstrate the full capabilities of the market analysis system.
Includes geographic distribution, realistic business profiles, and market dynamics.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedDataGenerator:
    def __init__(self):
        """Initialize the enhanced data generator with realistic parameters"""
        self.pune_areas = [
            "Baner", "Koregaon Park", "Aundh", "Viman Nagar", "Hadapsar", "Wakad", "Hinjewadi",
            "Pune Station", "Camp", "Deccan", "Shivaji Nagar", "Karve Nagar", "Kothrud",
            "Warje", "Bavdhan", "Sus", "Pashan", "Magarpatta", "Kalyani Nagar", "Yerawada",
            "Kharadi", "Wagholi", "Undri", "Kondhwa", "Wanowrie", "Salisbury Park",
            "Vishrantwadi", "Dhanori", "Lohegaon", "Mundhwa", "Tingre Nagar", "Pimpri",
            "Chinchwad", "Nigdi", "Akurdi", "Bhosari", "Chakan", "Talegaon", "Dehu Road",
            "Alandi Road", "Sangvi", "Ravet", "Pimple Saudagar", "Pimple Nilakh"
        ]
        
        self.gym_name_components = {
            'prefixes': ['Gold\'s', 'Anytime', 'Planet', 'Fitness First', 'Talwalkars', 'Snap',
                        'LA Fitness', 'Body Fuel', 'Iron Paradise', 'Muscle Factory', 'Power Zone',
                        'Flex', 'Elite', 'Prime', 'Apex', 'Titan', 'Warrior', 'Champion',
                        'Victory', 'Supreme', 'Ultimate', 'Royal', 'Diamond', 'Platinum'],
            'middle': ['Fitness', 'Gym', 'Health', 'Wellness', 'Body', 'Muscle', 'Power',
                      'Strength', 'Training', 'Sports', 'Performance', 'Athletic'],
            'suffixes': ['Club', 'Center', 'Studio', 'Academy', 'Institute', 'Zone',
                        'Arena', 'Complex', 'Hub', 'Point', 'Palace', 'Empire']
        }
        
        self.clinic_name_components = {
            'prefixes': ['Apollo', 'Fortis', 'Max', 'Narayana', 'Manipal', 'Care', 'KIMS',
                        'Cloudnine', 'Rainbow', 'Motherhood', 'Nova', 'Medanta', 'Asian',
                        'Global', 'City', 'Metro', 'Prime', 'Elite', 'Advanced', 'Modern'],
            'specialties': ['Multi-Specialty', 'Cardiology', 'Orthopedic', 'Neurology',
                           'Gastroenterology', 'Dermatology', 'Pediatric', 'Gynecology',
                           'ENT', 'Ophthalmology', 'Dental', 'Physiotherapy', 'Diagnostic'],
            'suffixes': ['Hospital', 'Clinic', 'Medical Center', 'Healthcare', 'Diagnostics',
                        'Medical Institute', 'Health Center', 'Care Center', 'Medical Hub']
        }
        
        self.business_categories = {
            'gyms': {
                'Traditional Gym': 0.40,
                'Health Club/Wellness': 0.25,
                'Functional Fitness': 0.15,
                'Women-Only Gym': 0.10,
                'Yoga/Pilates Studio': 0.07,
                'Martial Arts/Boxing': 0.03
            },
            'clinics': {
                'Multi-Specialty Hospital': 0.20,
                'Specialty Clinic': 0.35,
                'Diagnostic Center': 0.25,
                'Physiotherapy Clinic': 0.15,
                'Wellness Center': 0.05
            }
        }

    def generate_business_name(self, business_type: str, area: str) -> str:
        """Generate realistic business names"""
        if business_type in ['Traditional Gym', 'Health Club/Wellness', 'Functional Fitness', 
                           'Women-Only Gym', 'Yoga/Pilates Studio', 'Martial Arts/Boxing']:
            components = self.gym_name_components
            
            # Different naming patterns
            patterns = [
                lambda: f"{random.choice(components['prefixes'])} {random.choice(components['middle'])}",
                lambda: f"{random.choice(components['prefixes'])} {random.choice(components['suffixes'])}",
                lambda: f"{random.choice(components['middle'])} {random.choice(components['suffixes'])}",
                lambda: f"{area} {random.choice(components['middle'])} {random.choice(components['suffixes'])}",
                lambda: f"{random.choice(components['prefixes'])} {random.choice(components['middle'])} {random.choice(components['suffixes'])}"
            ]
            
            base_name = random.choice(patterns)()
            
            # Add specialty suffixes
            if business_type == 'Women-Only Gym':
                if random.random() < 0.7:
                    base_name += " - Ladies Only"
            elif business_type == 'Yoga/Pilates Studio':
                if random.random() < 0.6:
                    base_name = base_name.replace('Gym', 'Yoga Studio').replace('Fitness', 'Yoga')
            elif business_type == 'Martial Arts/Boxing':
                if random.random() < 0.8:
                    base_name += " & Martial Arts"
                    
        else:  # Clinics
            components = self.clinic_name_components
            
            patterns = [
                lambda: f"{random.choice(components['prefixes'])} {random.choice(components['suffixes'])}",
                lambda: f"{area} {random.choice(components['suffixes'])}",
                lambda: f"Dr. {random.choice(['Sharma', 'Patel', 'Kumar', 'Singh', 'Agarwal'])} {random.choice(components['suffixes'])}",
                lambda: f"{random.choice(components['prefixes'])} {random.choice(components['specialties'])} {random.choice(components['suffixes'])}"
            ]
            
            base_name = random.choice(patterns)()
        
        return base_name

    def generate_realistic_address(self, area: str) -> str:
        """Generate realistic addresses for Pune"""
        street_types = ['Road', 'Lane', 'Street', 'Marg', 'Path', 'Galli']
        building_types = ['Plaza', 'Complex', 'Tower', 'Apartment', 'Building', 'Center', 'Mall']
        
        street_number = random.randint(1, 999)
        street_name = random.choice(['MG', 'FC', 'JM', 'Survey No.', 'Plot No.', 'Shop No.'])
        street_type = random.choice(street_types)
        
        if random.random() < 0.6:  # 60% chance of building name
            building_name = f"{random.choice(['Sunrise', 'Sunset', 'Royal', 'Imperial', 'Grand', 'Star', 'Diamond', 'Golden'])} {random.choice(building_types)}"
            address = f"{building_name}, {street_name} {street_number}, {area}, Pune"
        else:
            address = f"{street_name} {street_number}, {street_type}, {area}, Pune"
        
        # Add PIN code
        pin_code = random.randint(411001, 411061)
        address += f" - {pin_code}"
        
        return address

    def generate_phone_number(self) -> str:
        """Generate realistic Indian phone numbers"""
        prefixes = ['98', '99', '97', '96', '95', '94', '93', '92', '91', '90', '89', '88', '87', '86', '85', '84', '83', '82', '81', '80']
        prefix = random.choice(prefixes)
        number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return f"{prefix}{number}"

    def generate_rating(self, business_type: str, area_tier: int) -> float:
        """Generate realistic ratings based on business type and area"""
        # Base rating influenced by business type
        base_ratings = {
            'Traditional Gym': 3.8,
            'Health Club/Wellness': 4.1,
            'Functional Fitness': 4.0,
            'Women-Only Gym': 3.9,
            'Yoga/Pilates Studio': 4.2,
            'Martial Arts/Boxing': 3.7,
            'Multi-Specialty Hospital': 4.0,
            'Specialty Clinic': 4.1,
            'Diagnostic Center': 3.9,
            'Physiotherapy Clinic': 4.0,
            'Wellness Center': 4.2
        }
        
        base_rating = base_ratings.get(business_type, 3.8)
        
        # Adjust for area tier (1=premium, 2=mid, 3=budget)
        area_adjustment = {1: 0.3, 2: 0.0, 3: -0.2}
        adjusted_rating = base_rating + area_adjustment.get(area_tier, 0)
        
        # Add random variation
        rating = adjusted_rating + random.uniform(-0.5, 0.5)
        
        # Ensure rating is within valid range
        rating = max(1.0, min(5.0, rating))
        
        return round(rating, 1)

    def categorize_area_tier(self, area: str) -> int:
        """Categorize areas into tiers for realistic distribution"""
        premium_areas = ['Koregaon Park', 'Baner', 'Aundh', 'Kalyani Nagar', 'Viman Nagar', 'Magarpatta']
        mid_tier_areas = ['Kothrud', 'Shivaji Nagar', 'Camp', 'Deccan', 'Wakad', 'Hinjewadi']
        
        if area in premium_areas:
            return 1  # Premium
        elif area in mid_tier_areas:
            return 2  # Mid-tier
        else:
            return 3  # Budget

    def generate_website(self, business_name: str) -> str:
        """Generate realistic website URLs"""
        if random.random() < 0.4:  # 40% of businesses have websites
            clean_name = business_name.lower().replace(' ', '').replace('&', 'and').replace('-', '')
            clean_name = ''.join(c for c in clean_name if c.isalnum())[:15]
            
            domains = ['.com', '.in', '.co.in', '.org']
            return f"www.{clean_name}{random.choice(domains)}"
        return None

    def generate_establishment_year(self) -> int:
        """Generate realistic establishment years"""
        current_year = datetime.now().year
        # Most businesses established in last 20 years, with some older ones
        
        # Create decade ranges from 1970 to current year
        decades = list(range(1970, current_year, 10))
        
        # Ensure weights match the number of decades
        num_decades = len(decades)
        if num_decades == 6:  # 1970s, 1980s, 1990s, 2000s, 2010s, 2020s
            weights = [0.05, 0.10, 0.15, 0.20, 0.35, 0.15]
        elif num_decades == 5:  # Fewer decades
            weights = [0.10, 0.15, 0.20, 0.30, 0.25]
        else:  # Fallback for any number of decades
            # Create weights that favor recent years
            weights = []
            for i in range(num_decades):
                if i < num_decades - 3:  # Older decades
                    weights.append(0.05)
                elif i < num_decades - 1:  # Recent decades
                    weights.append(0.25)
                else:  # Current decade
                    weights.append(0.40)
            # Normalize weights to sum to 1.0
            total_weight = sum(weights)
            weights = [w / total_weight for w in weights]
        
        chosen_decade = random.choices(decades, weights=weights)[0]
        return random.randint(chosen_decade, min(chosen_decade + 9, current_year - 1))

    def generate_employee_count(self, business_type: str) -> int:
        """Generate realistic employee counts"""
        employee_ranges = {
            'Traditional Gym': (5, 25),
            'Health Club/Wellness': (10, 50),
            'Functional Fitness': (3, 15),
            'Women-Only Gym': (4, 20),
            'Yoga/Pilates Studio': (2, 10),
            'Martial Arts/Boxing': (3, 12),
            'Multi-Specialty Hospital': (50, 500),
            'Specialty Clinic': (5, 30),
            'Diagnostic Center': (8, 40),
            'Physiotherapy Clinic': (3, 15),
            'Wellness Center': (5, 25)
        }
        
        min_emp, max_emp = employee_ranges.get(business_type, (5, 25))
        return random.randint(min_emp, max_emp)

    def generate_comprehensive_dataset(self, total_gyms: int = 300, total_clinics: int = 250) -> pd.DataFrame:
        """Generate comprehensive dataset with both gyms and clinics"""
        logger.info(f"Generating comprehensive dataset: {total_gyms} gyms + {total_clinics} clinics")
        
        all_businesses = []
        
        # Generate gyms
        logger.info("Generating gym data...")
        gym_categories = list(self.business_categories['gyms'].keys())
        gym_weights = list(self.business_categories['gyms'].values())
        
        for i in range(total_gyms):
            area = random.choice(self.pune_areas)
            area_tier = self.categorize_area_tier(area)
            business_type = random.choices(gym_categories, weights=gym_weights)[0]
            
            business = {
                'business_id': f"GYM_{i+1:04d}",
                'business_name': self.generate_business_name(business_type, area),
                'business_type': 'Gym/Fitness',
                'business_category': business_type,
                'rating': self.generate_rating(business_type, area_tier),
                'address': self.generate_realistic_address(area),
                'area': area,
                'area_tier': area_tier,
                'phone': self.generate_phone_number(),
                'website': self.generate_website(f"gym_{i}"),
                'established_year': self.generate_establishment_year(),
                'employee_count': self.generate_employee_count(business_type),
                'extraction_method': 'enhanced_generator',
                'data_source': 'synthetic_realistic'
            }
            all_businesses.append(business)
        
        # Generate clinics
        logger.info("Generating clinic data...")
        clinic_categories = list(self.business_categories['clinics'].keys())
        clinic_weights = list(self.business_categories['clinics'].values())
        
        for i in range(total_clinics):
            area = random.choice(self.pune_areas)
            area_tier = self.categorize_area_tier(area)
            business_type = random.choices(clinic_categories, weights=clinic_weights)[0]
            
            business = {
                'business_id': f"CLI_{i+1:04d}",
                'business_name': self.generate_business_name(business_type, area),
                'business_type': 'Healthcare/Clinic',
                'business_category': business_type,
                'rating': self.generate_rating(business_type, area_tier),
                'address': self.generate_realistic_address(area),
                'area': area,
                'area_tier': area_tier,
                'phone': self.generate_phone_number(),
                'website': self.generate_website(f"clinic_{i}"),
                'established_year': self.generate_establishment_year(),
                'employee_count': self.generate_employee_count(business_type),
                'extraction_method': 'enhanced_generator',
                'data_source': 'synthetic_realistic'
            }
            all_businesses.append(business)
        
        # Create DataFrame
        df = pd.DataFrame(all_businesses)
        
        # Add some realistic data quality issues (missing values)
        self._add_realistic_missing_data(df)
        
        # Add market dynamics
        self._add_market_dynamics(df)
        
        logger.info(f"Generated comprehensive dataset: {len(df)} total businesses")
        return df

    def _add_realistic_missing_data(self, df: pd.DataFrame):
        """Add realistic missing data patterns"""
        # Some businesses don't have websites (already handled in generation)
        
        # Some phone numbers might be missing (5% chance)
        missing_phone_mask = np.random.random(len(df)) < 0.05
        df.loc[missing_phone_mask, 'phone'] = None
        
        # Some addresses might be incomplete (2% chance)
        missing_address_mask = np.random.random(len(df)) < 0.02
        df.loc[missing_address_mask, 'address'] = None
        
        # Some ratings might be missing (8% chance for new businesses)
        missing_rating_mask = np.random.random(len(df)) < 0.08
        df.loc[missing_rating_mask, 'rating'] = None

    def _add_market_dynamics(self, df: pd.DataFrame):
        """Add market dynamics and competitive intelligence"""
        # Add competitor clusters (businesses in same area)
        area_counts = df['area'].value_counts()
        df['area_competition_level'] = df['area'].map(area_counts)
        
        # Add market penetration score
        df['market_penetration'] = df.apply(lambda row: self._calculate_market_penetration(row), axis=1)
        
        # Add growth potential score
        df['growth_potential'] = df.apply(lambda row: self._calculate_growth_potential(row), axis=1)

    def _calculate_market_penetration(self, row) -> float:
        """Calculate market penetration score"""
        base_score = 5.0
        
        # Adjust based on area tier
        tier_adjustment = {1: -1.0, 2: 0.0, 3: 1.0}  # Premium areas are more saturated
        score = base_score + tier_adjustment.get(row['area_tier'], 0)
        
        # Adjust based on competition level
        if row['area_competition_level'] > 15:
            score -= 2.0
        elif row['area_competition_level'] > 10:
            score -= 1.0
        elif row['area_competition_level'] < 5:
            score += 1.0
        
        return max(1.0, min(10.0, score))

    def _calculate_growth_potential(self, row) -> float:
        """Calculate growth potential score"""
        base_score = 6.0
        
        # Newer businesses have higher growth potential
        years_in_operation = datetime.now().year - row['established_year']
        if years_in_operation < 5:
            base_score += 2.0
        elif years_in_operation < 10:
            base_score += 1.0
        elif years_in_operation > 25:
            base_score -= 1.0
        
        # Adjust based on rating
        if pd.notna(row['rating']):
            if row['rating'] >= 4.5:
                base_score += 1.0
            elif row['rating'] < 3.0:
                base_score -= 2.0
        
        return max(1.0, min(10.0, base_score))

    def save_enhanced_dataset(self, df: pd.DataFrame, filename: str = 'data/output/pune_comprehensive_market_data.csv'):
        """Save the enhanced dataset with metadata and proper error handling"""
        import os
        import time
        from pathlib import Path
        
        # Ensure output directory exists
        output_dir = Path(filename).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Handle file locking issues
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # Try to save with a unique filename if the original is locked
                if attempt > 0:
                    base_name = Path(filename).stem
                    extension = Path(filename).suffix
                    filename = f"{output_dir}/{base_name}_{int(time.time())}{extension}"
                
                # Save main dataset with explicit error handling
                df.to_csv(filename, index=False, encoding='utf-8')
                logger.info(f"Enhanced dataset saved to: {filename}")
                break
                
            except PermissionError as e:
                logger.warning(f"Permission denied for {filename}, attempt {attempt + 1}/{max_attempts}")
                if attempt == max_attempts - 1:
                    # Try alternative filename
                    timestamp = int(time.time())
                    alt_filename = f"data/output/pune_market_data_{timestamp}.csv"
                    try:
                        df.to_csv(alt_filename, index=False, encoding='utf-8')
                        logger.info(f"Enhanced dataset saved to alternative file: {alt_filename}")
                        filename = alt_filename
                        break
                    except Exception as e2:
                        logger.error(f"Failed to save dataset: {e2}")
                        raise
                time.sleep(1)  # Wait before retry
            except Exception as e:
                logger.error(f"Unexpected error saving dataset: {e}")
                if attempt == max_attempts - 1:
                    raise
                time.sleep(1)
        
        # Save metadata with same error handling
        try:
            metadata = {
                'generation_date': datetime.now().isoformat(),
                'total_businesses': len(df),
                'business_types': df['business_type'].value_counts().to_dict(),
                'business_categories': df['business_category'].value_counts().to_dict(),
                'areas_covered': df['area'].nunique(),
                'data_completeness': {
                    'business_name': f"{df['business_name'].notna().sum()}/{len(df)}",
                    'rating': f"{df['rating'].notna().sum()}/{len(df)}",
                    'address': f"{df['address'].notna().sum()}/{len(df)}",
                    'phone': f"{df['phone'].notna().sum()}/{len(df)}",
                    'website': f"{df['website'].notna().sum()}/{len(df)}"
                },
                'market_insights': {
                    'avg_rating': df['rating'].mean(),
                    'rating_std': df['rating'].std(),
                    'most_common_area': df['area'].value_counts().index[0],
                    'newest_business_year': df['established_year'].max(),
                    'oldest_business_year': df['established_year'].min()
                },
                'saved_filename': filename
            }
            
            metadata_file = filename.replace('.csv', '_metadata.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            logger.info(f"Metadata saved to: {metadata_file}")
            
        except Exception as e:
            logger.warning(f"Could not save metadata: {e}")
            metadata = {'error': str(e), 'saved_filename': filename}
        
        return metadata

def main():
    """Generate comprehensive dataset for market analysis"""
    logger.info("Starting enhanced data generation...")
    
    generator = EnhancedDataGenerator()
    
    # Generate large-scale dataset
    df = generator.generate_comprehensive_dataset(
        total_gyms=400,    # Increased from 300
        total_clinics=350  # Increased from 250
    )
    
    # Save the dataset
    metadata = generator.save_enhanced_dataset(df)
    
    # Print summary
    print("\n" + "="*70)
    print("ENHANCED DATASET GENERATION COMPLETE")
    print("="*70)
    
    print(f"\n📊 DATASET SUMMARY:")
    print(f"   • Total businesses generated: {len(df)}")
    print(f"   • Gyms/Fitness centers: {len(df[df['business_type'] == 'Gym/Fitness'])}")
    print(f"   • Healthcare/Clinics: {len(df[df['business_type'] == 'Healthcare/Clinic'])}")
    print(f"   • Areas covered: {df['area'].nunique()}")
    print(f"   • Average rating: {df['rating'].mean():.2f}")
    
    print(f"\n🏋️ GYM CATEGORIES:")
    gym_categories = df[df['business_type'] == 'Gym/Fitness']['business_category'].value_counts()
    for category, count in gym_categories.items():
        print(f"   • {category}: {count}")
    
    print(f"\n🏥 CLINIC CATEGORIES:")
    clinic_categories = df[df['business_type'] == 'Healthcare/Clinic']['business_category'].value_counts()
    for category, count in clinic_categories.items():
        print(f"   • {category}: {count}")
    
    print(f"\n📍 TOP AREAS BY BUSINESS DENSITY:")
    top_areas = df['area'].value_counts().head(5)
    for area, count in top_areas.items():
        print(f"   • {area}: {count} businesses")
    
    print(f"\n📁 FILES GENERATED:")
    print(f"   • Main dataset: data/output/pune_comprehensive_market_data.csv")
    print(f"   • Metadata: data/output/pune_comprehensive_market_data_metadata.json")
    
    print(f"\n🚀 READY FOR ANALYSIS:")
    print(f"   • Run: python main.py --mode all")
    print(f"   • Or process this enhanced dataset directly")
    
    print("="*70)

if __name__ == "__main__":
    main()