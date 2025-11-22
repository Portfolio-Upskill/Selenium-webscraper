import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# Selenium will automatically manage the driver executable
driver = webdriver.Chrome()

driver.get('http://www.google.com/');

time.sleep(5) # Let the user actually see something!

search_box = driver.find_element(By.NAME, 'q')

search_box.send_keys('ChromeDriver')

search_box.submit()

time.sleep(5) # Let the user actually see something!

driver.quit()