# Weather Scraper

This project is a web scraper built with Python and Selenium that extracts temperature data from a weather website. It navigates to the site, scrapes the data, and saves it into CSV files.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.x
*   pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Portfolio-UpSkill.git
    cd Portfolio-UpSkill/Selenium-webscraper
    ```

2.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **WebDriver:**
    This project requires `chromedriver` to be available in your system's PATH. A `chromedriver` for macOS has been included in the `chromedriver_mac64` directory. You may need to move this to a directory in your PATH, like `/usr/local/bin`, or you can update the scraper logic to point to its location directly.

## Running the Scraper

To run the web scraper, execute the main script:

```bash
python -m webscraper.main
```

The scraper will run and generate CSV files with the temperature data in the `test_results` directory.

## Running Tests

To run the automated tests, use the provided script:

```bash
python run_pytest.py
```

This will execute the test suite using `pytest` and generate an HTML report in the `test_results` directory.
