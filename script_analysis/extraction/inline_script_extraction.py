import logging
from selenium.webdriver.common.by import By

def extract_inline_scripts(driver):
    inline_scripts = [script.get_attribute('innerHTML') for script in driver.find_elements(By.TAG_NAME, 'script') if not script.get_attribute('src')]
    logging.info(f"Extracted {len(inline_scripts)} inline scripts.")
    return inline_scripts
