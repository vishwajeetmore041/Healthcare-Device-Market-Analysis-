"""
Main Execution Script for Market Opportunity Analysis

This script provides a unified interface to run the complete market analysis pipeline
for identifying potential customers for fitness device sales in Pune.

Usage:
    python main.py --mode all                    # Run complete pipeline
    python main.py --mode scrape --phase 4       # Run specific scraping phase
    python main.py --mode analyze                 # Run analysis only
    python main.py --mode score                   # Run lead scoring only
"""

import argparse
import logging
import sys
from pathlib import Path
import time

# --- START: AUTO-FIX FUNCTION ---
def patch_data_processor_file():
    """
    This function automatically finds and fixes the known bug in data_processor.py
    to prevent the 'float' object has no attribute 'round' error.
    """
    try:
        file_path = Path(__file__).parent / 'data_processor.py'
        if not file_path.exists():
            return # File not found, do nothing

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        incorrect_line = "'avg_rating': df['rating'].mean().round(2) if df['rating'].notna().any() else None,\n"
        correct_line = "                'avg_rating': round(df['rating'].mean(), 2) if df['rating'].notna().any() else None,\n"
        
        # Check if the file needs patching
        needs_patching = False
        for i, line in enumerate(lines):
            if incorrect_line.strip() in line.strip():
                lines[i] = correct_line
                needs_patching = True
                break
        
        # If a change was made, write the file back
        if needs_patching:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            logging.info(f"Automatically patched bug in {file_path.name}")
            
    except Exception as e:
        logging.warning(f"Could not auto-patch data_processor.py: {e}")
# --- END: AUTO-FIX FUNCTION ---


# Add project root to path
sys.path.append(str(Path(__file__).parent))

from scrapers.phase4_stealth_scraper import StealthJustdialScraper
from analysis.data_processor import FitnessDataProcessor
from analysis.market_analysis import FitnessMarketAnalyzer
from analysis.lead_scorer import FitnessLeadScorer

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/output/pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class MarketAnalysisPipeline:
    def __init__(self):
        self.raw_data_file = 'data/processed/phase4_ultimate_results.csv'
        
        # Prioritize comprehensive datasets - check which exists and use the best one
        data_file_priorities = [
            'data/output/pune_comprehensive_market_data.csv',  # 752 businesses
            'data/output/pune_enhanced_final.csv',            # 575+ businesses
            'data/output/multi_source_comprehensive_data.csv', # Multi-source data
            'data/output/pune_gyms_final.csv'                # Fallback (14 businesses)
        ]
        
        # Find the best available dataset
        self.clean_data_file = 'data/output/pune_gyms_final.csv'  # Default fallback
        for data_file in data_file_priorities:
            if Path(data_file).exists():
                self.clean_data_file = data_file
                logger.info(f"Using dataset: {data_file}")
                break
        
        self.scored_data_file = 'data/output/scored_leads.csv'
        self.enhanced_data_file = 'data/output/pune_comprehensive_market_data.csv'
        self.multi_source_data_file = 'data/output/multi_source_comprehensive_data.csv'
        
    def generate_enhanced_data(self, total_gyms: int = 400, total_clinics: int = 350):
        """Generate large-scale enhanced dataset with improved error handling"""
        logger.info("Starting enhanced data generation...")
        
        try:
            from data_generator import EnhancedDataGenerator
            
            generator = EnhancedDataGenerator()
            df = generator.generate_comprehensive_dataset(
                total_gyms=total_gyms,
                total_clinics=total_clinics
            )
            
            # Enhanced save with better error handling
            import time
            base_filename = self.enhanced_data_file
            
            # Try to use existing file if permission issues
            try:
                metadata = generator.save_enhanced_dataset(df, base_filename)
                actual_filename = metadata.get('saved_filename', base_filename)
                
                # Update the file path for subsequent processing
                if actual_filename != base_filename:
                    self.enhanced_data_file = actual_filename
                    logger.info(f"Updated enhanced data file path to: {actual_filename}")
                    
            except Exception as save_error:
                logger.warning(f"Save error: {save_error}")
                
                # Fallback: try to use existing file if it exists
                from pathlib import Path
                if Path(base_filename).exists():
                    logger.info(f"Using existing dataset: {base_filename}")
                    return True
                else:
                    raise save_error
            
            logger.info(f"Enhanced data generation completed: {len(df)} businesses")
            return True
            
        except Exception as e:
            logger.error(f"Error during enhanced data generation: {e}")
            # Check if we can use existing data
            from pathlib import Path
            if Path(self.enhanced_data_file).exists():
                logger.info(f"Using existing enhanced dataset: {self.enhanced_data_file}")
                return True
            return False
    
    def collect_multi_source_data(self):
        """Collect data from multiple sources using simplified collector with context manager"""
        logger.info("Starting multi-source data collection...")
        
        try:
            from multi_source_collector_simple import SimplifiedMultiSourceCollector
            
            # Use context manager for automatic cleanup
            with SimplifiedMultiSourceCollector() as collector:
                df = collector.collect_multi_source_data(target_businesses=500)
                
                if not df.empty:
                    df.to_csv(self.multi_source_data_file, index=False, encoding='utf-8')
                    logger.info(f"Multi-source collection completed: {len(df)} businesses")
                    return True
                else:
                    logger.warning("Multi-source collection returned no data")
                    return False
                    
        except Exception as e:
            logger.error(f"Error during multi-source collection: {e}")
            return False
    
    def run_scraping(self, phase: int = 4, city: str = "Pune", search_term: str = "Gyms"):
        logger.info(f"Starting Phase {phase} scraping for {search_term} in {city}")
        
        scraper = None
        try:
            if phase == 4:
                scraper = StealthJustdialScraper()
                
                if not scraper.setup_stealth_driver():
                    logger.error("Failed to setup stealth driver")
                    return False
                
                success = scraper.search_gyms_ultimate(city=city, search_term=search_term)
                
                if success:
                    df = scraper.save_results(self.raw_data_file)
                    logger.info(f"Scraping completed successfully: {len(df)} businesses found")
                    return True
                else:
                    logger.error("Scraping failed")
                    return False
                    
            else:
                logger.error(f"Phase {phase} not implemented in main pipeline")
                return False
                
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            return False
        finally:
            if scraper:
                scraper.cleanup()
    
    def run_enhanced_data_processing(self, data_source: str = "enhanced"):
        """Run data processing on enhanced datasets"""
        logger.info(f"Starting enhanced data processing for {data_source} data")
        
        try:
            # Determine input file based on data source
            if data_source == "enhanced":
                input_file = self.enhanced_data_file
                # Use a different output file to preserve the comprehensive dataset
                output_file = 'data/output/pune_enhanced_final.csv'
            elif data_source == "multi_source":
                input_file = self.multi_source_data_file
                output_file = self.clean_data_file
            else:
                input_file = self.raw_data_file
                output_file = self.clean_data_file
            
            if not Path(input_file).exists():
                logger.error(f"Data file not found: {input_file}")
                return False
            
            # Skip processing if we already have comprehensive data
            if data_source == "enhanced" and Path(input_file).exists():
                # Check if the input file is already comprehensive
                import pandas as pd
                df = pd.read_csv(input_file)
                if len(df) > 500:  # If we have a large dataset, skip processing
                    logger.info(f"Using existing comprehensive dataset: {len(df)} businesses")
                    # Update clean_data_file to point to the comprehensive dataset
                    self.clean_data_file = input_file
                    return True
            
            processor = FitnessDataProcessor()
            clean_data = processor.process_all_data(
                input_file=input_file,
                output_file=output_file
            )
            
            if not clean_data.empty:
                logger.info(f"Enhanced data processing completed: {len(clean_data)} clean records")
                # Update clean_data_file to point to the processed output
                if data_source == "enhanced":
                    self.clean_data_file = output_file
                return True
            else:
                logger.error("Enhanced data processing failed - no clean data produced")
                return False
                
        except Exception as e:
            logger.error(f"Error during enhanced data processing: {e}")
            return False
    
    def run_data_processing(self):
        """Run data cleaning and processing"""
        logger.info("Starting data processing pipeline")
        
        try:
            if not Path(self.raw_data_file).exists():
                logger.error(f"Raw data file not found: {self.raw_data_file}")
                return False
            
            processor = FitnessDataProcessor()
            clean_data = processor.process_all_data(
                input_file=self.raw_data_file,
                output_file=self.clean_data_file
            )
            
            if not clean_data.empty:
                logger.info(f"Data processing completed: {len(clean_data)} clean records")
                return True
            else:
                logger.error("Data processing failed - no clean data produced")
                return False
                
        except Exception as e:
            logger.error(f"Error during data processing: {e}")
            return False
        """Run data cleaning and processing"""
        logger.info("Starting data processing pipeline")
        
        try:
            if not Path(self.raw_data_file).exists():
                logger.error(f"Raw data file not found: {self.raw_data_file}")
                return False
            
            processor = FitnessDataProcessor()
            clean_data = processor.process_all_data(
                input_file=self.raw_data_file,
                output_file=self.clean_data_file
            )
            
            if not clean_data.empty:
                logger.info(f"Data processing completed: {len(clean_data)} clean records")
                return True
            else:
                logger.error("Data processing failed - no clean data produced")
                return False
                
        except Exception as e:
            logger.error(f"Error during data processing: {e}")
            return False
    
    def run_market_analysis(self):
        """Run market analysis and visualization"""
        logger.info("Starting market analysis")
        
        try:
            if not Path(self.clean_data_file).exists():
                logger.error(f"Clean data file not found: {self.clean_data_file}")
                return False
            
            analyzer = FitnessMarketAnalyzer(self.clean_data_file)
            analyzer.run_complete_analysis()
            
            logger.info("Market analysis completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error during market analysis: {e}")
            return False
    
    def run_lead_scoring(self):
        """Run lead scoring and recommendation generation"""
        logger.info("Starting lead scoring")
        
        try:
            if not Path(self.clean_data_file).exists():
                logger.error(f"Clean data file not found: {self.clean_data_file}")
                return False
            
            scorer = FitnessLeadScorer()
            
            # Load and prepare data
            data = scorer.load_data(self.clean_data_file)
            if data.empty:
                return False
            
            # Engineer features and train model
            featured_data = scorer.engineer_features(data)
            X, y = scorer.prepare_training_data(featured_data)
            training_results = scorer.train_model(X, y)
            
            # Score leads and generate recommendations
            scored_data = scorer.score_leads(data)
            recommendations = scorer.generate_sales_recommendations(scored_data)
            
            # Save results
            scored_data.to_csv(self.scored_data_file, index=False, encoding='utf-8')
            
            import json
            with open('data/output/sales_recommendations.json', 'w', encoding='utf-8') as f:
                json.dump(recommendations, f, indent=2, ensure_ascii=False, default=str)
            
            scorer.save_model('analysis/lead_scoring_model.joblib')
            
            logger.info(f"Lead scoring completed: {len(scored_data)} businesses scored")
            logger.info(f"Model R² score: {training_results['test_r2']:.3f}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error during lead scoring: {e}")
            return False
    
    def run_complete_pipeline(self, city: str = "Pune", search_term: str = "Gyms"):
        """Run the complete market analysis pipeline"""
        logger.info("Starting complete market analysis pipeline")
        
        start_time = time.time()
        
        # Step 1: Web Scraping
        logger.info("Step 1/4: Web Scraping")
        if not self.run_scraping(phase=4, city=city, search_term=search_term):
            logger.error("Pipeline failed at scraping stage")
            return False
        
        # Step 2: Data Processing
        logger.info("Step 2/4: Data Processing")
        if not self.run_data_processing():
            logger.error("Pipeline failed at data processing stage")
            return False
        
        # Step 3: Market Analysis
        logger.info("Step 3/4: Market Analysis")
        if not self.run_market_analysis():
            logger.error("Pipeline failed at market analysis stage")
            return False
        
        # Step 4: Lead Scoring
        logger.info("Step 4/4: Lead Scoring")
        if not self.run_lead_scoring():
            logger.error("Pipeline failed at lead scoring stage")
            return False
        
        # Pipeline completed successfully
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"Complete pipeline finished successfully in {duration/60:.1f} minutes")
        self._print_pipeline_summary()
        
        return True
    
    def _print_pipeline_summary(self):
        """Print a summary of pipeline results"""
        print("\n" + "="*70)
        print("MARKET OPPORTUNITY ANALYSIS - PIPELINE COMPLETE")
        print("="*70)
        
        # Check output files and provide summary
        outputs = {
            'Raw Data': self.raw_data_file,
            'Clean Data': self.clean_data_file,
            'Scored Leads': self.scored_data_file,
            'Market Overview': 'data/output/market_overview.png',
            'Interactive Dashboard': 'data/output/interactive_dashboard.html',
            'Analysis Report': 'data/output/market_analysis_report.json',
            'Sales Recommendations': 'data/output/sales_recommendations.json',
            'Trained Model': 'analysis/lead_scoring_model.joblib'
        }
        
        print("\n📁 Generated Outputs:")
        for name, path in outputs.items():
            if Path(path).exists():
                size = Path(path).stat().st_size / 1024  # KB
                print(f"   ✓ {name}: {path} ({size:.1f} KB)")
            else:
                print(f"   ✗ {name}: {path} (missing)")
        
        # Load and display key metrics if available
        try:
            import pandas as pd
            import json
            
            if Path(self.scored_data_file).exists():
                scored_data = pd.read_csv(self.scored_data_file)
                print(f"\n📊 Key Metrics:")
                print(f"   • Total businesses analyzed: {len(scored_data)}")
                print(f"   • Average lead score: {scored_data['ml_lead_score'].mean():.2f}/10")
                print(f"   • High-priority targets: {len(scored_data[scored_data['priority_tier'] == 'Very High'])}")
            
            if Path('data/output/sales_recommendations.json').exists():
                with open('data/output/sales_recommendations.json', 'r') as f:
                    recommendations = json.load(f)
                print(f"   • Priority targets identified: {len(recommendations.get('priority_targets', []))}")
                print(f"   • Quick wins identified: {len(recommendations.get('quick_wins', []))}")
        
        except Exception as e:
            logger.debug(f"Error loading metrics: {e}")
        
        print(f"\n🎯 Next Steps:")
        print(f"   1. Review interactive dashboard: data/output/interactive_dashboard.html")
        print(f"   2. Examine sales recommendations: data/output/sales_recommendations.json")
        print(f"   3. Contact priority targets from scored leads")
        print(f"   4. Monitor and update lead scores regularly")
        
        print("="*70)

def main():
    """Main function with command line interface"""
    
    # CALL THE AUTO-FIX FUNCTION AT THE START
    patch_data_processor_file()
    
    parser = argparse.ArgumentParser(description='Market Opportunity Analysis Pipeline')
    parser.add_argument('--mode', choices=['all', 'scrape', 'process', 'analyze', 'score', 'generate', 'multi-source'], 
                       default='all', help='Pipeline mode to run')
    parser.add_argument('--phase', type=int, choices=[1, 2, 3, 4], default=4, 
                       help='Scraping phase to run (only for scrape mode)')
    parser.add_argument('--city', default='Pune', help='City to analyze')
    parser.add_argument('--search-term', default='Gyms', help='Business type to search')
    
    args = parser.parse_args()
    
    pipeline = MarketAnalysisPipeline()
    
    logger.info(f"Starting pipeline in {args.mode} mode")
    
    try:
        if args.mode == 'all':
            success = pipeline.run_complete_pipeline(city=args.city, search_term=args.search_term)
        elif args.mode == 'scrape':
            success = pipeline.run_scraping(phase=args.phase, city=args.city, search_term=args.search_term)
        elif args.mode == 'process':
            success = pipeline.run_data_processing()
        elif args.mode == 'analyze':
            success = pipeline.run_market_analysis()
        elif args.mode == 'score':
            success = pipeline.run_lead_scoring()
        elif args.mode == 'generate':
            success = pipeline.generate_enhanced_data()
            if success:
                success = pipeline.run_enhanced_data_processing("enhanced")
                if success:
                    success = pipeline.run_market_analysis() and pipeline.run_lead_scoring()
        elif args.mode == 'multi-source':
            success = pipeline.collect_multi_source_data()
            if success:
                success = pipeline.run_enhanced_data_processing("multi_source")
                if success:
                    success = pipeline.run_market_analysis() and pipeline.run_lead_scoring()
        else:
            logger.error(f"Unknown mode: {args.mode}")
            success = False
        
        if success:
            logger.info("Pipeline completed successfully!")
            sys.exit(0)
        else:
            logger.error("Pipeline failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()