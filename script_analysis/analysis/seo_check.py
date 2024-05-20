from selenium.webdriver.common.by import By

def check_meta_tags(driver):
    meta_tags = {}
    elements = driver.find_elements(By.TAG_NAME, 'meta')
    for element in elements:
        name = element.get_attribute('name')
        content = element.get_attribute('content')
        if name and content:
            meta_tags[name] = content
    return meta_tags

def check_header_tags(driver):
    header_tags = {}
    for i in range(1, 7):
        tag = f'h{i}'
        elements = driver.find_elements(By.TAG_NAME, tag)
        header_tags[tag] = [element.text for element in elements if element.text]
    return header_tags

def check_seo_issues(driver):
    issues = []

    # Example checks for SEO issues
    # Check for missing title tag
    title = driver.find_element(By.TAG_NAME, 'title')
    if not title:
        issues.append("Missing title tag")
    
    # Check for missing meta description
    meta_description = driver.find_element(By.NAME, 'description')
    if not meta_description:
        issues.append("Missing meta description")
    
    return issues
