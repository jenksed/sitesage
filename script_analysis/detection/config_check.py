import logging
from selenium.webdriver.common.by import By

def check_config_issues(driver):
    config_issues = []

    # Check for synchronous XMLHttpRequests
    sync_xhr_used = driver.execute_script("""
        return window.XMLHttpRequest ? XMLHttpRequest.prototype.open.toString().includes('false') : 'No XHR';
    """)
    if sync_xhr_used:
        config_issues.append("Synchronous XMLHttpRequests found.")
    logging.info(f"Checked config issues: {config_issues}.")

    # Enhanced GA and GA4 detection
    ga_config = driver.execute_script("""
        if (window.ga) {
            return ga.getAll().length === 0 ? 'Analytics misconfigured' : 'Analytics configured';
        } else if (window.gtag) {
            return 'GA4 found';
        } else {
            return 'Analytics not found';
        }
    """)
    if ga_config in ['Analytics misconfigured', 'Analytics not found']:
        config_issues.append(ga_config)
    logging.info(f"Checked analytics config issues: {ga_config}.")

    return config_issues

def check_script_tags(driver):
    script_issues = []

    # Check for Google Tag Manager
    gtm = driver.execute_script("""
        return Array.from(document.scripts).some(script => script.src.includes('googletagmanager.com/gtm.js'));
    """)
    if gtm:
        script_issues.append("Google Tag Manager detected.")
    
    # Check for Facebook Pixel
    fb_pixel = driver.execute_script("""
        return Array.from(document.scripts).some(script => script.src.includes('connect.facebook.net/en_US/fbevents.js'));
    """)
    if fb_pixel:
        script_issues.append("Facebook Pixel detected.")
    
    # Check for Google Analytics
    ga = driver.execute_script("""
        return Array.from(document.scripts).some(script => script.src.includes('google-analytics.com/analytics.js'));
    """)
    if ga:
        script_issues.append("Google Analytics detected.")
    
    logging.info(f"Checked script tags: {script_issues}.")
    return script_issues

def check_deprecated_html(driver, deprecated_tags):
    deprecated_issues = []
    for tag in deprecated_tags:
        elements = driver.find_elements(By.XPATH, f"//{tag}")
        if elements:
            deprecated_issues.append(f"Deprecated HTML tag found: <{tag}>")
    logging.info(f"Checked deprecated HTML issues: {deprecated_issues}.")
    return deprecated_issues
