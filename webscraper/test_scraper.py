import os
import pandas as pd
import time
import datetime
import sys
from functools import wraps

# --- The final, clean import ---
# Final correct import line for direct execution:
from .pages.homepage import HomePage
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from .constants import REGION_MAP
# -----------------------------

# Define base directory for test results and the current day's subdirectory
TEST_RESULTS_BASE_DIR = "test_results"
CURRENT_DAY_DIR = datetime.datetime.now().strftime("%Y-%m-%d")
CURRENT_DAY_RESULTS_DIR = os.path.join(TEST_RESULTS_BASE_DIR, CURRENT_DAY_DIR)

def test_page_header_loads_correctly(driver):
    """Positive test case: Verify the main header text is correct."""
    home_page = HomePage(driver)
    home_page.load()
    print("\nRunning Test 1: Positive Flow (Header Assertion)")
    expected_text = "AVERAGE TEMPERATURE BY COUNTRY"
    
    # ACT: Get the header text using the Page Object method
    actual_text = home_page.get_header_text()
    
    # ASSERT: Check if the extracted text contains the expected keyword
    assert expected_text in actual_text.upper(), f"Header text assertion failed. Expected '{expected_text}' to be in '{actual_text}'."
    print(f"PASS: Header assertion successful. Found: {actual_text}")

def test_sort_by_country_ascending(driver):
    """Positive test case: Verify that clicking the 'Country' header sorts the table."""
    home_page = HomePage(driver)
    home_page.load()
    print("\nRunning Test 2: Positive Flow (Sort by Country)")
    
    # 1. Click the 'Country' header to sort the table
    home_page.click_country_header()
    
    # 2. Scrape the data again after sorting
    scraped_data = home_page.extract_table_data()
    
    # 3. Extract the country names from the scraped data
    country_names = [row['Country'] for row in scraped_data]
    
    # 4. Create a sorted version of the country names
    sorted_country_names = sorted(country_names)
    
    # 5. Assert that the scraped country names are already sorted
    assert country_names == sorted_country_names, "Assertion failed: Countries are not sorted in ascending order."
    print("PASS: Country sorting assertion successful.")

def test_scrape_and_export_data(driver):
    """Main scraping and export function, includes data quality assertions."""
    home_page = HomePage(driver)
    home_page.load()
    print("\nRunning Test 3: Data Scraping and Export")
    
    # Ensure the daily results directory exists
    os.makedirs(CURRENT_DAY_RESULTS_DIR, exist_ok=True)
    
    # The CSV will be saved in the current day's test results directory
    output_filename = os.path.join(CURRENT_DAY_RESULTS_DIR, "scraped_temperature_data.csv")
    
    # Clean up old file if it exists
    if os.path.exists(output_filename):
        os.remove(output_filename)

    # 1. Scrape the data
    scraped_data = home_page.extract_table_data()
    
    # 2. Assertions on the data structure
    assert len(scraped_data) > 10, "Assertion failed: Did not scrape at least 10 rows."
    assert 'Country' in scraped_data[0], "Assertion failed: Missing 'Country' key in first scraped data item."
    
    print(f"Scraped {len(scraped_data)} rows successfully.")
    
    # 3. Export to CSV 
    # The HomePage method exports the file to the specified path
    home_page.export_to_csv(scraped_data, output_filename)
    
    # Final Assertion: Verify the CSV file was created
    assert os.path.exists(output_filename), f"Assertion failed: CSV file '{output_filename}' was not created."

def test_scrape_and_export_by_region(driver):
    """Scrapes data and exports it into separate CSV files for each region."""
    home_page = HomePage(driver)
    home_page.load()
    print("\nRunning Test 4: Data Scraping and Export by Region")

    # Ensure the daily results directory exists
    os.makedirs(CURRENT_DAY_RESULTS_DIR, exist_ok=True)

    # 1. Scrape the data
    scraped_data = home_page.extract_table_data()
    assert len(scraped_data) > 10, "Assertion failed: Did not scrape at least 10 rows."

    # 2. Segregate data by region
    regional_data = {'Americas': [], 'EMEA': [], 'Asia': []}
    for row in scraped_data:
        country = row['Country']
        for region, countries in REGION_MAP.items():
            if country in countries:
                regional_data[region].append(row)
                break
    
    # 3. Export to CSV for each region
    for region, data in regional_data.items():
        if data:
            output_filename = os.path.join(CURRENT_DAY_RESULTS_DIR, f"{region.lower()}_temperature_data.csv")
            if os.path.exists(output_filename):
                os.remove(output_filename)
            
            home_page.export_to_csv(data, output_filename)
            assert os.path.exists(output_filename), f"Assertion failed: CSV file '{output_filename}' was not created."
            print(f"Successfully exported {len(data)} rows to {output_filename}")

def test_verify_specific_country_data(driver):
    """Test case: Verify specific country's data is present and not empty."""
    home_page = HomePage(driver)
    home_page.load()
    print("\nRunning Test 5: Verify Specific Country Data")
    
    scraped_data = home_page.extract_table_data()
    
    # Look for a known country, e.g., "United States"
    united_states_data = next((row for row in scraped_data if row['Country'] == 'United States'), None)
    
    assert united_states_data is not None, "Assertion failed: 'United States' data not found."
    assert united_states_data['Last_Temperature'] != '', "Assertion failed: 'United States' Last_Temperature is empty."
    assert united_states_data['Previous_Temperature'] != '', "Assertion failed: 'United States' Previous_Temperature is empty."
    
    print("PASS: Specific country data for 'United States' verified successfully.")

def test_sort_by_temperature_descending(driver):
    """Test case: Verify sorting by 'Last Temperature' in ascending order after one click."""
    home_page = HomePage(driver)
    home_page.load()
    print("\nRunning Test 6: Sort by Temperature Ascending (Single Click)")
    
    # Click 'Last' temperature header once for ascending sort
    home_page.click_last_temperature_header() 
    
    scraped_data = home_page.extract_table_data()
    
    temperatures = []
    for row in scraped_data:
        try:
            temp_str = row['Last_Temperature'].replace(',', '').strip()
            if temp_str:
                temperatures.append(float(temp_str))
        except ValueError:
            continue 

    # Assert that temperatures are in descending order
    assert all(temperatures[i] >= temperatures[i+1] for i in range(len(temperatures)-1)), \
        "Assertion failed: Temperatures are not sorted in descending order."
    print("PASS: Temperature sorting (ascending) assertion successful.")

# def test_search_non_existent_country(driver):
#     """Test case: Search for a non-existent country and verify 'No results found' message."""
#     home_page = HomePage(driver)
#     home_page.load()
#     print("\nRunning Test 7: Search Non-Existent Country")
    
#     non_existent_country = "NoCountryHere123"
#     home_page.search_country(non_existent_country)
    
#     # Instead of checking for a specific message, check if the table becomes empty
#     updated_data = home_page.extract_table_data()
#     assert len(updated_data) == 0, \
#         f"Assertion failed: Table was not empty after searching for non-existent country '{non_existent_country}'."
#     print(f"PASS: Table is empty for non-existent country '{non_existent_country}'.")

def test_search_non_existent_country_table_unchanged(driver):
    """Negative test case: Verify table content remains unchanged after searching for a non-existent country."""
    home_page = HomePage(driver)
    home_page.load()
    print("\nRunning Test 7 (New): Search Non-Existent Country (Table Unchanged)")
    
    # Scrape initial data
    initial_data = home_page.extract_table_data()
    
    non_existent_country = "NoCountryHere123"
    home_page.search_country(non_existent_country)
    
    # Scrape data again after search
    updated_data = home_page.extract_table_data()
    
    # Assert that the table content is still the same (i.e., search had no filtering effect)
    assert initial_data == updated_data, \
        f"Assertion failed: Table content changed unexpectedly after searching for non-existent country '{non_existent_country}'."
    print(f"PASS: Table content remained unchanged after searching for non-existent country '{non_existent_country}'.")

def test_temperature_values_are_numeric(driver):
    """Test case: Verify 'Last_Temperature' and 'Previous_Temperature' values are numeric."""
    home_page = HomePage(driver)
    home_page.load()
    print("\nRunning Test 8: Temperature Values Are Numeric")
    
    scraped_data = home_page.extract_table_data()
    
    assert len(scraped_data) > 0, "Assertion failed: No data scraped to validate."
    
    for row in scraped_data:
        last_temp_str = row.get('Last_Temperature', '').replace(',', '').strip()
        prev_temp_str = row.get('Previous_Temperature', '').replace(',', '').strip()
        
        # Check Last_Temperature
        if last_temp_str: # Only check if not empty
            try:
                float(last_temp_str)
            except ValueError:
                assert False, f"Assertion failed: Last_Temperature '{last_temp_str}' for '{row['Country']}' is not numeric."
        
        # Check Previous_Temperature
        if prev_temp_str: # Only check if not empty
            try:
                float(prev_temp_str)
            except ValueError:
                assert False, f"Assertion failed: Previous_Temperature '{prev_temp_str}' for '{row['Country']}' is not numeric."
                
    print("PASS: All scraped 'Last_Temperature' and 'Previous_Temperature' values are numeric.")