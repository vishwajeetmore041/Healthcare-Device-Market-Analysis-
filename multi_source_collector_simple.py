"""
Simplified Multi-Source Data Collector (No Async Dependencies)

This simplified version removes async dependencies and implements fallback mechanisms
for Chrome driver connectivity issues as mentioned in project memories.
"""

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import random
import logging
from pathlib import Path
import json
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimplifiedMultiSourceCollector:
    def __init__(self):
        """Initialize simplified multi-source data collector"""
        self.driver = None
        self.results = []
        self.fallback_data_generator = None
        self._cleanup_attempted = False  # Track cleanup attempts
        
        # Import data generator as fallback
        try:
            from data_generator import EnhancedDataGenerator
            self.fallback_data_generator = EnhancedDataGenerator()
            logger.info("Fallback data generator loaded successfully")
        except ImportError:
            logger.warning("Data generator not available for fallback")
        
        self.search_terms = {
            'fitness': [
                'Gyms', 'Fitness Centers', 'Health Clubs', 'Yoga Centers',
                'Personal Training', 'Ladies Gym', 'CrossFit'
            ],
            'healthcare': [
                'Hospitals', 'Clinics', 'Medical Centers', 'Diagnostic Centers',
                'Physiotherapy', 'Cardiology Clinics', 'Dental Clinics'
            ]
        }

    def setup_driver_with_fallback(self) -> bool:
        """Setup driver with fallback mechanisms and improved cleanup handling"""
        logger.info("Setting up Chrome driver with fallback mechanisms...")
        
        # Strategy 1: Try undetected-chromedriver with additional safety measures
        try:
            logger.info("Attempting undetected-chromedriver setup...")
            options = uc.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")
            options.add_argument("--disable-javascript")
            options.add_argument("--no-first-run")
            options.add_argument("--no-default-browser-check")
            
            # Create driver with version_main to avoid some compatibility issues
            self.driver = uc.Chrome(options=options, version_main=None)
            
            # Test if driver is working
            self.driver.get("about:blank")
            
            logger.info("Undetected-chromedriver setup successful")
            return True
            
        except Exception as e:
            logger.warning(f"Undetected-chromedriver failed: {e}")
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
            
        # Strategy 2: Try regular Selenium with stealth and enhanced safety
        try:
            logger.info("Attempting regular Selenium with stealth...")
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")
            options.add_argument("--headless=new")  # Use new headless mode
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Hide automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Test if driver is working
            self.driver.get("about:blank")
            
            logger.info("Regular Selenium setup successful")
            return True
            
        except Exception as e:
            logger.warning(f"Regular Selenium failed: {e}")
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
            
        # Strategy 3: Use requests-only approach
        logger.warning("All Chrome driver strategies failed, using requests-only approach")
        return False

    def collect_multi_source_data(self, target_businesses: int = 500) -> pd.DataFrame:
        """Collect data from multiple sources with fallback mechanisms"""
        logger.info("Starting simplified multi-source data collection...")
        
        all_results = []
        driver_available = self.setup_driver_with_fallback()
        
        if driver_available:
            # Try to collect real data from web sources
            logger.info("Chrome driver available - attempting web scraping...")
            
            try:
                # Collect from Justdial
                justdial_results = self._collect_justdial_simplified()
                all_results.extend(justdial_results)
                logger.info(f"Collected {len(justdial_results)} businesses from Justdial")
                
                # Add small delay between sources
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                logger.error(f"Web scraping failed: {e}")
        
        # Always supplement with generated data to meet target
        current_count = len(all_results)
        needed_count = max(0, target_businesses - current_count)
        
        if needed_count > 0 and self.fallback_data_generator:
            logger.info(f"Generating {needed_count} additional businesses using fallback data generator...")
            
            # Calculate gym/clinic split
            gyms_needed = int(needed_count * 0.7)  # 70% gyms
            clinics_needed = needed_count - gyms_needed
            
            generated_df = self.fallback_data_generator.generate_comprehensive_dataset(
                total_gyms=gyms_needed, 
                total_clinics=clinics_needed
            )
            
            # Convert to list format
            for _, row in generated_df.iterrows():
                all_results.append({
                    'business_name': row['business_name'],
                    'business_category': row['business_category'],
                    'rating': row['rating'],
                    'address': row['address'],
                    'area': row['area'],
                    'phone': row['phone'],
                    'website': row.get('website', ''),
                    'source': 'generated_fallback',
                    'business_type': row['business_type']
                })
        
        # Cleanup driver if used with improved error handling
        self.cleanup()
        
        # Convert to DataFrame and process
        df = pd.DataFrame(all_results)
        df = self._process_multi_source_data(df)
        
        logger.info(f"Multi-source collection complete: {len(df)} businesses total")
        return df

    def _collect_justdial_simplified(self) -> List[Dict]:
        """Simplified Justdial collection"""
        results = []
        
        if not self.driver:
            return results
        
        try:
            # Navigate to Justdial
            self.driver.get("https://www.justdial.com")
            time.sleep(3)
            
            # Try to search for gyms
            search_terms = ['Gyms', 'Fitness Centers']
            
            for term in search_terms:
                try:
                    logger.info(f"Searching for: {term}")
                    
                    # Find search input
                    search_selectors = [
                        "input[placeholder*='Search']",
                        "input[name='what']",
                        "#srchbx"
                    ]
                    
                    search_input = None
                    for selector in search_selectors:
                        try:
                            search_input = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                            )
                            break
                        except:
                            continue
                    
                    if search_input:
                        search_input.clear()
                        search_input.send_keys(term)
                        search_input.send_keys("\n")
                        
                        time.sleep(5)  # Wait for results
                        
                        # Extract results
                        businesses = self._extract_justdial_businesses()
                        results.extend(businesses)
                        
                        time.sleep(3)  # Rate limiting
                    
                except Exception as e:
                    logger.warning(f"Error searching for {term}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in Justdial collection: {e}")
        
        return results

    def _extract_justdial_businesses(self) -> List[Dict]:
        """Extract business data from current Justdial page"""
        businesses = []
        
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Look for business listings
            listing_selectors = [
                '.result-box',
                '.srp-tuple', 
                '.listing-card',
                '.business-item'
            ]
            
            for selector in listing_selectors:
                elements = soup.select(selector)
                if elements:
                    logger.info(f"Found {len(elements)} listings with selector: {selector}")
                    
                    for element in elements[:10]:  # Limit to 10 per selector
                        business = self._parse_business_element(element)
                        if business:
                            businesses.append(business)
                    break
                    
        except Exception as e:
            logger.error(f"Error extracting businesses: {e}")
        
        return businesses

    def _parse_business_element(self, element) -> Optional[Dict]:
        """Parse individual business element"""
        try:
            # Extract business name
            name_elem = element.select_one('h3, h4, .business-name, .store-name')
            if not name_elem:
                return None
            
            business_name = name_elem.get_text(strip=True)
            if not business_name or len(business_name) < 3:
                return None
            
            # Extract rating
            rating = None
            rating_elem = element.select_one('.rating, .star-rating')
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                import re
                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                if rating_match:
                    try:
                        rating = float(rating_match.group(1))
                    except ValueError:
                        pass
            
            # Extract address
            address = None
            addr_elem = element.select_one('.address, .location, .addr')
            if addr_elem:
                address = addr_elem.get_text(strip=True)
            
            return {
                'business_name': business_name,
                'rating': rating,
                'address': address,
                'source': 'justdial_scraped',
                'business_category': 'Traditional Gym',  # Default category
                'business_type': 'fitness'
            }
            
        except Exception as e:
            logger.debug(f"Error parsing business element: {e}")
            return None

    def _process_multi_source_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process and clean multi-source data"""
        if df.empty:
            return df
        
        logger.info("Processing multi-source data...")
        
        # Remove duplicates based on business name
        df = df.drop_duplicates(subset=['business_name'], keep='first')
        
        # Fill missing values with pandas-compatible approach
        missing_ratings = df['rating'].isna().sum()
        if missing_ratings > 0:
            # Generate random ratings for missing values
            random_ratings = pd.Series(np.random.uniform(3.0, 4.5, missing_ratings), 
                                     index=df[df['rating'].isna()].index)
            df.loc[df['rating'].isna(), 'rating'] = random_ratings
        
        df['business_category'] = df['business_category'].fillna('General Fitness')
        df['business_type'] = df['business_type'].fillna('fitness')
        
        # Add source summary
        source_counts = df['source'].value_counts()
        logger.info(f"Data sources: {source_counts.to_dict()}")
        
        return df
    
    def cleanup(self):
        """Safe cleanup method for driver resources with enhanced error handling"""
        if self.driver and not self._cleanup_attempted:
            self._cleanup_attempted = True
            try:
                logger.info("Starting Chrome driver cleanup...")
                
                # Step 1: Close all tabs/windows except the main one
                try:
                    handles = self.driver.window_handles
                    if len(handles) > 1:
                        main_handle = handles[0]
                        for handle in handles[1:]:
                            try:
                                self.driver.switch_to.window(handle)
                                self.driver.close()
                            except Exception as e:
                                logger.debug(f"Error closing window handle {handle}: {e}")
                        
                        # Switch back to main window
                        try:
                            self.driver.switch_to.window(main_handle)
                        except:
                            pass
                            
                except Exception as e:
                    logger.debug(f"Error managing window handles: {e}")
                
                # Step 2: Navigate to about:blank to clear any ongoing requests
                try:
                    self.driver.get("about:blank")
                    time.sleep(0.5)  # Give it time to load
                except:
                    pass
                
                # Step 3: Stop any ongoing operations
                try:
                    self.driver.execute_script("window.stop();")
                except:
                    pass
                
                # Step 4: Quit the driver
                try:
                    self.driver.quit()
                    logger.info("Chrome driver quit successfully")
                except Exception as e:
                    logger.warning(f"Error during driver.quit(): {e}")
                    
                    # Force process termination if needed
                    try:
                        if hasattr(self.driver, 'service') and hasattr(self.driver.service, 'process'):
                            if self.driver.service.process:
                                self.driver.service.process.terminate()
                                logger.info("Chrome driver process terminated")
                    except Exception as e2:
                        logger.debug(f"Error terminating process: {e2}")
                
            except Exception as e:
                logger.warning(f"Error during cleanup: {e}")
            
            finally:
                self.driver = None
                logger.info("Chrome driver cleanup completed")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup"""
        self.cleanup()
        return False  # Don't suppress exceptions
    
    def __del__(self):
        """Silent destructor to prevent handle errors"""
        # Completely silent cleanup to avoid any destructor errors
        try:
            if hasattr(self, 'driver') and self.driver and not getattr(self, '_cleanup_attempted', False):
                # Set flag to prevent multiple cleanup attempts
                self._cleanup_attempted = True
                
                # Try minimal cleanup without logging
                try:
                    self.driver.quit()
                except:
                    try:
                        if hasattr(self.driver, 'service') and hasattr(self.driver.service, 'process'):
                            if self.driver.service.process:
                                self.driver.service.process.terminate()
                    except:
                        pass
                finally:
                    self.driver = None
        except:
            pass  # Completely silent

def main():
    """Main function to test simplified multi-source collection"""
    logger.info("Testing Simplified Multi-Source Data Collection")
    logger.info("=" * 60)
    
    collector = SimplifiedMultiSourceCollector()
    
    # Collect data
    df = collector.collect_multi_source_data(target_businesses=100)
    
    if not df.empty:
        # Save results
        output_file = 'data/output/multi_source_simplified.csv'
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        logger.info(f"Results saved to: {output_file}")
        logger.info(f"Total businesses: {len(df)}")
        
        # Show sample
        print("\nSample Results:")
        print(df[['business_name', 'business_category', 'rating', 'source']].head())
        
        # Show source distribution
        print(f"\nSource Distribution:")
        print(df['source'].value_counts())
        
    else:
        logger.error("No data collected")

if __name__ == "__main__":
    main()