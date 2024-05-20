import logging
from selenium.webdriver.common.by import By

def extract_css(driver):
    css_files = [link.get_attribute('href') for link in driver.find_elements(By.TAG_NAME, 'link') if link.get_attribute('rel') == 'stylesheet']
    logging.info(f"Extracted {len(css_files)} CSS files.")
    return css_files
