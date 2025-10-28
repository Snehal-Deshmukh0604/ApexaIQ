"""
Java Version History Scraper - Wikipedia

This script extracts Java version information from Wikipedia using only:
- Selenium WebDriver
- HTML tags only (no classes, no IDs)
- String methods only (no regex)
- Exactly four columns: version_name, version, url, scraped_date
"""

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from datetime import datetime


class JavaVersionScraper:
    def __init__(self):
        """Initialize the Selenium WebDriver with tags only."""
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Firefox WebDriver with stable configuration."""
        firefox_options = Options()
        firefox_options.add_argument("--disable-blink-features=AutomationControlled")
        firefox_options.add_argument("--no-sandbox")
        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.implicitly_wait(10)

    def extract_java_versions(self, url):
        """
        Extract Java version information from Wikipedia using only tags and string methods.
        
        Args:
            url (str): The target URL to scrape
            
        Returns:
            list: List of dictionaries with version_name, version, url, scraped_date
        """
        try:
            print(f"Navigating to: {url}")
            self.driver.get(url)
            time.sleep(3)
            
            versions_data = []
            scraped_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Extract from all tables on the page
            print("Extracting from tables...")
            tables = self.driver.find_elements(By.TAG_NAME, "table")
            print(f"Found {len(tables)} tables")
            
            for i, table in enumerate(tables):
                print(f"Processing table {i+1}...")
                table_data = self.extract_from_table(table, url, scraped_date)
                versions_data.extend(table_data)
            
            # Remove duplicates based on version number
            unique_versions = []
            seen_versions = set()
            for item in versions_data:
                if item['version'] not in seen_versions:
                    seen_versions.add(item['version'])
                    unique_versions.append(item)
            
            return unique_versions
            
        except Exception as e:
            print(f"Error during extraction: {e}")
            return []

    def extract_from_table(self, table, url, scraped_date):
        """
        Extract version information from a table using only tags.
        
        Args:
            table: Selenium table element
            url (str): Source URL
            scraped_date (str): Timestamp of scraping
            
        Returns:
            list: List of version dictionaries from the table
        """
        table_data = []
        
        try:
            # Get all rows from the table
            rows = table.find_elements(By.TAG_NAME, "tr")
            
            for row_idx, row in enumerate(rows):
                # Skip header rows (usually first row)
                if row_idx == 0:
                    continue
                    
                # Get all cells in the row
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 3:  # Need at least version, name, and date columns
                    version_info = self.parse_table_row(cells, url, scraped_date)
                    if version_info:
                        table_data.append(version_info)
                        print(f"Found: {version_info['version_name']} | {version_info['version']}")
                        
        except Exception as e:
            print(f"Error extracting from table: {e}")
            
        return table_data

    def parse_table_row(self, cells, url, scraped_date):
        """
        Parse a table row to extract version information.
        
        Args:
            cells: List of table cell elements
            url (str): Source URL
            scraped_date (str): Timestamp of scraping
            
        Returns:
            dict: Dictionary with version_name, version, url, scraped_date or None
        """
        try:
            # In Wikipedia Java version tables, typical structure:
            # Cell 0: Version number (e.g., JDK 1.0, Java SE 8)
            # Cell 1: Release date
            # Cell 2: Additional info or version name
            
            version_text = cells[0].text.strip()
            date_text = cells[1].text.strip()
            
            # Extract version name and number
            version_name = self.extract_version_name(version_text)
            version_number = self.extract_version_number(version_text)
            
            if not version_number:
                return None
            
            # Format the date
            formatted_date = self.format_date(date_text)
            
            return {
                'version_name': version_name,
                'version': version_number,
                'url': url,
                'scraped_date': scraped_date
            }
            
        except Exception as e:
            print(f"Error parsing table row: {e}")
            return None

    def extract_version_name(self, text):
        """
        Extract version name from text.
        
        Args:
            text (str): Text containing version information
            
        Returns:
            str: Version name
        """
        # Clean the text and use as version name
        text = text.replace('\n', ' ').replace('  ', ' ').strip()
        return text

    def extract_version_number(self, text):
        """
        Extract version number from text using string methods.
        
        Args:
            text (str): Text containing version information
            
        Returns:
            str: Version number or None
        """
        text_lower = text.lower()
        
        # Look for common Java version patterns
        patterns = [
            'jdk', 'java se', 'java ', 'j2se', 'j2ee'
        ]
        
        for pattern in patterns:
            if pattern in text_lower:
                # Find the pattern position
                pattern_pos = text_lower.find(pattern)
                after_pattern = text[pattern_pos + len(pattern):].strip()
                
                # Extract version numbers and dots
                version_chars = []
                for char in after_pattern:
                    if char.isdigit() or char == '.':
                        version_chars.append(char)
                    elif version_chars:
                        break
                    elif char.isspace():
                        continue
                    else:
                        break
                
                version_str = ''.join(version_chars).strip('.')
                if version_str and any(c.isdigit() for c in version_str):
                    return version_str
        
        # If no specific pattern found, look for any numbers in the text
        version_chars = []
        for char in text:
            if char.isdigit() or char == '.':
                version_chars.append(char)
            elif version_chars:
                break
        
        version_str = ''.join(version_chars).strip('.')
        if version_str and any(c.isdigit() for c in version_str):
            return version_str
        
        return None

    def format_date(self, date_text):
        """
        Format date text to a standard format.
        
        Args:
            date_text (str): Raw date text from website
            
        Returns:
            str: Formatted date
        """
        # Clean the date text
        date_text = date_text.replace('\n', ' ').replace('  ', ' ').strip()
        
        # Remove any citations like [1], [2], etc.
        while '[' in date_text and ']' in date_text:
            start = date_text.find('[')
            end = date_text.find(']') + 1
            date_text = date_text[:start] + date_text[end:]
        
        return date_text.strip()

    def save_to_csv(self, data, filename='java_versions.csv'):
        """
        Save extracted data to CSV file with exactly four columns.
        
        Args:
            data (list): List of version dictionaries
            filename (str): Output filename
        """
        try:
            if data:
                # Create DataFrame with the four required columns
                df = pd.DataFrame(data)
                df = df[['version_name', 'version', 'url', 'scraped_date']]
                
                # Save to CSV
                df.to_csv(filename, index=False)
                
                print(f"SUCCESS: Saved {len(data)} Java versions to {filename}")
                print("\nEXTRACTED JAVA VERSION DATA:")
                print("=" * 80)
                print(df.to_string(index=False))
                print("=" * 80)
                
                return df
            else:
                print("No Java version data found to save")
                return None
                
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return None

    def close_driver(self):
        """Close the browser driver."""
        if hasattr(self, 'driver'):
            self.driver.quit()
            print("Browser closed")


def main():
    """Main function to execute the Java version scraping process."""
    print("Java Version History Scraper - Wikipedia")
    print("=" * 50)
    print("Extracting: version_name, version, url, scraped_date")
    print("=" * 50)
    
    scraper = None
    try:
        scraper = JavaVersionScraper()
        url = "https://en.wikipedia.org/wiki/Java_version_history"
        
        # Extract Java versions
        version_data = scraper.extract_java_versions(url)
        
        # Save to CSV
        scraper.save_to_csv(version_data)
        
        if version_data:
            print(f"\nEXTRACTION COMPLETE: Found {len(version_data)} Java versions")
            print(f"File saved: java_versions.csv")
        else:
            print("No Java versions found in the extraction")
        
    except Exception as e:
        print(f"Critical error: {e}")
        
    finally:
        if scraper:
            scraper.close_driver()


if __name__ == "__main__":
    main()