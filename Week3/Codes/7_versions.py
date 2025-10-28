from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import time

def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    # Remove headless temporarily for debugging
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Use Selenium 4's built-in driver management
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_windows11_release_info():
    """Scrape Windows 11 release information"""
    driver = setup_driver()
    
    try:
        # Navigate to the URL
        url = "https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information"
        print("Navigating to URL...")
        driver.get(url)
        
        # Wait for the page to load
        print("Waiting for page to load...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        print("Page loaded successfully!")
        
        # Find all tables on the page
        tables = driver.find_elements(By.TAG_NAME, "table")
        print(f"Found {len(tables)} tables")
        
        release_data = []
        
        for table_index, table in enumerate(tables):
            # Find all rows in the table
            rows = table.find_elements(By.TAG_NAME, "tr")
            print(f"Table {table_index + 1}: Found {len(rows)} rows")
            
            for row_index, row in enumerate(rows):
                # Find all cells in the row
                cells = row.find_elements(By.TAG_NAME, "td")
                
                if len(cells) >= 3:  # Ensure we have enough cells
                    try:
                        # Extract version name (usually in the first cell)
                        version_name = cells[0].text.strip()
                        
                        # Extract version number (usually in the second cell)
                        version = cells[1].text.strip()
                        
                        # Extract URL from links in the third cell
                        url_cell = cells[2]
                        links = url_cell.find_elements(By.TAG_NAME, "a")
                        url = ""
                        if links:
                            url = links[0].get_attribute("href")
                        
                        # Only add if we have meaningful data
                        if version_name and version:
                            release_data.append({
                                'version_name': version_name,
                                'version': version,
                                'url': url,
                                'scraped_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            print(f"Added: {version_name} - {version}")
                            
                    except Exception as e:
                        print(f"Error processing row {row_index}: {e}")
                        continue
        
        return release_data
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []
    
    finally:
        driver.quit()

def save_to_csv(data, filename="windows11_releases.csv"):
    """Save scraped data to CSV"""
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
        print(f"Total records: {len(data)}")
    else:
        print("No data to save")

def save_to_excel(data, filename="windows11_releases.xlsx"):
    """Save scraped data to Excel"""
    if data:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")
        print(f"Total records: {len(data)}")
    else:
        print("No data to save")

if __name__ == "__main__":
    print("Scraping Windows 11 release information...")
    
    # Try the main scraping method
    data = scrape_windows11_release_info()
    
    # Display results
    if data:
        print(f"\nSuccessfully scraped {len(data)} records:")
        for i, item in enumerate(data[:5], 1):  # Show first 5 records
            print(f"{i}. {item['version_name']} - {item['version']}")
        
        if len(data) > 5:
            print(f"... and {len(data) - 5} more records")
        
        # Save to files
        save_to_csv(data)
        save_to_excel(data)
        
    else:
        print("No data was scraped.")