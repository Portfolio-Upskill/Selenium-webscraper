# webscraper/testhomepage/HomePage.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time # Used sparingly, only to demonstrate a pause after search

class HomePage:
    
    # --- LOCATORS (Centralized & Using XPath where specified) ---
    
    # Positive Flow: Table Header for Assertion (Checking if the page loaded correctly)
    HEADER_TEXT = (By.XPATH, "//h1")
    
    # Search Input Field for Negative Flow (Searching for a country)
    SEARCH_INPUT = (By.XPATH, "//input[@id='thisIstheSearchBoxIdTag']")

    # Core Table Locator (Targets all <tr> elements in the main table body)
    TABLE_BODY_ROWS = (By.XPATH, "//table[@class=\"table table-hover table-striped table-heatmap\"]")
    
    # Locator to check for 'No results found' message (for Negative Flow assertion)
    NO_RESULTS_MESSAGE = (By.XPATH, "//h3[text()='No result found']")
    
    # Link for 'Country' in the first row (used to verify data structure/loading)
    FIRST_ROW_COUNTRY_LINK = (By.XPATH, "(//table[@class='table table-hover']/tbody/tr[1]/td[1]/a)[1]")
    
    # Locator for the 'Country' table header
    COUNTRY_HEADER = (By.XPATH, "//th[text()='Country']")
    
    # Locator for the 'Last' temperature table header
    LAST_TEMPERATURE_HEADER = (By.XPATH, "//th[contains(text(),'Last')]")
    
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://tradingeconomics.com/country-list/temperature"

    def load(self):
        """Navigates to the home page URL."""
        self.driver.get(self.url)
        
        try:
            accept_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'ACCEPT') or contains(text(), 'AGREE')]"))
            )
            accept_button.click()
            print("Cookie banner accepted.")
        except:
            print("No cookie banner found or could not be clicked.")
        
        # Wait until the main header is present to confirm the page has started loading
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.HEADER_TEXT)
        )

    def click_country_header(self):
        """Clicks the 'Country' table header to sort the table."""
        header = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.COUNTRY_HEADER)
        )
        self.driver.execute_script("arguments[0].click();", header)
        # Add a small delay to allow the table to re-render
        time.sleep(3)
        
    def click_last_temperature_header(self):
        """Clicks the 'Last' temperature table header to sort the table."""
        header = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.LAST_TEMPERATURE_HEADER)
        )
        self.driver.execute_script("arguments[0].click();", header)
        # Add a small delay to allow the table to re-render
        time.sleep(3)

    def is_no_results_message_displayed(self):
        """Checks if the 'No results found' message is displayed."""
        try:
            message_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.NO_RESULTS_MESSAGE)
            )
            # Add debug print to show the actual text found
            print(f"DEBUG: Text found in 'no results' element: '{message_element.text.strip()}'")
            return True
        except:
            return False

    def get_header_text(self):
        """Gets the main header text for positive assertion."""
        # Note: We rely on the wait in the load method, but we wait again to ensure visibility
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.HEADER_TEXT)
        )
        return self.driver.find_element(*self.HEADER_TEXT).text

    def search_country(self, country_name):
        """Simulates a user searching for a country and waits for results."""
        # First, click on the search input to activate it
        search_box = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        search_box.click()
        search_box.clear()
        search_box.send_keys(country_name)
        
        # Use a brief pause to allow the JavaScript filtering to complete
        # Wait for either the table rows to update or the no results message to appear
        WebDriverWait(self.driver, 10).until(
            EC.any_of(
                EC.presence_of_element_located(self.TABLE_BODY_ROWS),
                EC.presence_of_element_located(self.NO_RESULTS_MESSAGE)
            )
        )

    def extract_table_data(self):
        """Scrapes all visible data rows from the table."""
        data = []
        
        # Wait for the table to ensure data has loaded 
        table = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.TABLE_BODY_ROWS)
        )
        
        rows = table.find_elements(By.XPATH, "./tbody/tr")
        
        for row in rows:
            # Locate all <td> elements within the current row
            # We use XPath here to get the list of columns within the current row element
            cols = row.find_elements(By.XPATH, "./td")
            
            # Extract data from the columns: Country, Last, Previous, Unit, etc.
            if len(cols) >= 5: 
                try:
                    # Column 1: Country name is inside an <a> tag
                    country = cols[0].find_element(By.TAG_NAME, "a").text
                    last = cols[1].text
                    previous = cols[2].text
                    # Column 5: Unit (e.g., 'Celsius')
                    unit = cols[4].text 
                    
                    data.append({
                        'Country': country,
                        'Last_Temperature': last,
                        'Previous_Temperature': previous,
                        'Unit': unit
                    })
                except Exception as e:
                    # Skip row if any expected element is missing (e.g., if a row is empty)
                    # print(f"Skipping row due to missing element: {e}")
                    continue
                    
        return data
        
    def export_to_csv(self, data, filename):
        """Exports the list of dictionaries to a CSV file."""
        if not data:
            print("No data to export.")
            return

        df = pd.DataFrame(data)
        # Export to the root directory for easy access
        df.to_csv(filename, index=False)
        print(f"Successfully exported {len(data)} rows to the file named: {filename}")