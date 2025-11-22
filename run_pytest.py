import pytest
import os
from datetime import datetime
import sys

if __name__ == '__main__':
    today = datetime.now().strftime("%Y-%m-%d")
    test_results_dir = os.path.join('test_results', today)
    os.makedirs(test_results_dir, exist_ok=True)

    report_path = os.path.join(test_results_dir, 'test_report.html')

    # We need to add the webscraper directory to the python path
    # so that pytest can find the tests.
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Selenium-webscraper', 'webscraper')))

    pytest_args = [
        'Selenium-webscraper/webscraper/test_scraper.py',
        f'--html={report_path}',
        '--self-contained-html',
    ]

    pytest.main(pytest_args)