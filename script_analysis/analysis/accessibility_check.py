import logging
from selenium.webdriver.common.by import By

def check_accessibility_issues(driver):
    accessibility_issues = []
    images_without_alt = driver.execute_script("return document.querySelectorAll('img:not([alt])').length")
    if images_without_alt:
        accessibility_issues.append(f"Found {images_without_alt} images without alt attributes")
    logging.info(f"Accessibility issues: {accessibility_issues}.")
    return accessibility_issues
