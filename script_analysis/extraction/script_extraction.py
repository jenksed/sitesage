import logging
from selenium.webdriver.common.by import By
import re
import os

def extract_scripts(driver):
    scripts = [script.get_attribute('src') for script in driver.find_elements(By.TAG_NAME, 'script') if script.get_attribute('src')]
    logging.info(f"Extracted {len(scripts)} scripts.")
    return scripts

def extract_trackers(driver, pattern):
    driver.implicitly_wait(10)
    trackers = [script.get_attribute('src') for script in driver.find_elements(By.TAG_NAME, 'script') if script.get_attribute('src') and pattern in script.get_attribute('src')]
    logging.info(f"Extracted {len(trackers)} trackers for pattern '{pattern}'.")
    return trackers

def extract_inline_scripts(driver):
    inline_scripts = [script.get_attribute('innerHTML') for script in driver.find_elements(By.TAG_NAME, 'script') if not script.get_attribute('src')]
    logging.info(f"Extracted {len(inline_scripts)} inline scripts.")
    return inline_scripts

def extract_css(driver):
    css_files = [link.get_attribute('href') for link in driver.find_elements(By.TAG_NAME, 'link') if link.get_attribute('rel') == 'stylesheet']
    logging.info(f"Extracted {len(css_files)} CSS files.")
    return css_files

def extract_meta_tags(driver):
    meta_tags = {}
    meta_elements = driver.find_elements(By.TAG_NAME, 'meta')
    for element in meta_elements:
        name = element.get_attribute('name') or element.get_attribute('property')
        content = element.get_attribute('content')
        if name and content:
            meta_tags[name] = content
    return meta_tags

def extract_header_tags(driver):
    header_tags = {}
    for header in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        headers = driver.find_elements(By.TAG_NAME, header)
        header_tags[header] = [h.text for h in headers if h.text]
    return header_tags

def load_unwanted_patterns(patterns_dir='script_analysis/extraction/unwanted_patterns'):
    """Load unwanted text patterns from files in a directory."""
    patterns = []
    if os.path.exists(patterns_dir):
        for filename in os.listdir(patterns_dir):
            filepath = os.path.join(patterns_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                patterns.append(file.read().strip())
    return patterns

def remove_elements(driver, selectors):
    """Remove elements from the DOM by their selectors."""
    for selector in selectors:
        script = f"""
        var elements = document.querySelectorAll('{selector}');
        for (var i = 0; i < elements.length; i++) {{
            elements[i].parentNode.removeChild(elements[i]);
        }}
        """
        driver.execute_script(script)

def extract_page_text(driver):
    """Extract visible text content from a webpage and filter unwanted patterns."""
    # Remove specific elements
    selectors_to_remove = [
        '#cookie-banner',  # Example ID
        '.header',  # Example class name
        '.footer',  # Example class name
        'nav',  # Example tag name
        '#privacy-popup',  # Example ID
        '.cookie-popup',  # Example class name
        '#nav-bar'  # Example ID
    ]
    remove_elements(driver, selectors_to_remove)
    
    body_text = driver.find_element(By.TAG_NAME, 'body').text
    
    # Load unwanted text patterns from the directory
    unwanted_patterns = load_unwanted_patterns()

    # Remove common unwanted text patterns
    for pattern in unwanted_patterns:
        # Use re.escape to handle special characters in the patterns
        body_text = re.sub(re.escape(pattern), '', body_text, flags=re.IGNORECASE)

    # Optionally, remove repeated phrases (this is a basic example)
    lines = body_text.split('\n')
    seen_lines = set()
    filtered_lines = []
    for line in lines:
        if line.strip() and line not in seen_lines:
            seen_lines.add(line)
            filtered_lines.append(line)
    filtered_text = '\n'.join(filtered_lines)

    return filtered_text.strip()