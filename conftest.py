import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime
import pytest_html

@pytest.fixture(scope="function")
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    
    yield driver
    
    # Teardown: Take screenshot if test failed, then quit driver
    if request.node.rep_call.failed:
        today_str = datetime.now().strftime("%Y-%m-%d")
        # Ensure output_dir is within the temporary project directory
        # The project's temporary directory is: /Users/anupam/.gemini/tmp/882169829f907d18fa526fa851175a3e0e0a73474be48e0eb0eae7d14b6c9c6b
        output_dir = os.path.join('/Users/anupam/.gemini/tmp/882169829f907d18fa526fa851175a3e0e0a73474be48e0eb0eae7d14b6c9c6b', today_str)
        os.makedirs(output_dir, exist_ok=True)
        
        test_method_name = request.node.name
        screenshot_name = f"{test_method_name}.png"
        screenshot_path = os.path.join(output_dir, screenshot_name)
        
        try:
            driver.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")
            # Attach screenshot to report if available
            if 'pytest_html' in request.config.pluginmanager.get_plugins():
                 request.node.add_report_section("call", "image", pytest_html.extras.image(screenshot_path))
        except Exception as e:
            print(f"\nCould not take screenshot: {e}")
            
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # This hook is executed after the test has run, but before its teardown
    # We store the call result in the item for access in the fixture teardown
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)