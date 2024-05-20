import sys
import os
import logging
import yaml  # type: ignore
import asyncio
from datetime import datetime
from tqdm.asyncio import tqdm
from script_analysis.driver_setup import get_driver
from script_analysis.extraction.script_extraction import extract_scripts, extract_trackers, extract_inline_scripts, extract_css
from script_analysis.detection.duplication_detection import find_duplicates
from script_analysis.detection.js_version_check import check_js_versions
from script_analysis.detection.config_check import check_config_issues, check_deprecated_html, check_script_tags
from script_analysis.report.report import report_issues, generate_report
from script_analysis.analysis.performance_check import get_performance_metrics
from script_analysis.analysis.seo_check import check_seo_issues
from script_analysis.analysis.accessibility_check import check_accessibility_issues
from script_analysis.analysis.broken_link_check import find_broken_links
from script_analysis.detection.security_check import check_security_issues

def load_config(config_file='config/config.yaml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def setup_logging(config):
    log_dir = config['logging']['directory']
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    now = datetime.now()
    log_filename = now.strftime(f"{log_dir}/page_analysis_%Y%m%d_%H%M%S.log")
    
    logging.basicConfig(filename=log_filename, level=getattr(logging, config['logging']['level'].upper()),
                        format=config['logging']['format'])
    
    console = logging.StreamHandler()
    console.setLevel(getattr(logging, config['logging']['level'].upper()))
    formatter = logging.Formatter(config['logging']['format'])
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.info("Logging setup complete.")

def analyze_scripts(driver, scripts):
    issues = []
    js_versions = check_js_versions(driver)
    if js_versions:
        issues.append(f"Multiple jQuery versions found: {', '.join(js_versions)}")

    config_issues = check_config_issues(driver)
    if config_issues:
        issues.extend(config_issues)
    
    script_issues = check_script_tags(driver)
    if script_issues:
        issues.extend(script_issues)

    return issues

async def process_url(driver, url, config):
    try:
        logging.info(f"Checking {url} for issues...")
        print(f"\nChecking {url} for issues...")
        driver.get(url)

        trackers = config['trackers']
        all_duplicates = {}
        for description, pattern in trackers.items():
            scripts = extract_trackers(driver, pattern)
            duplicates = find_duplicates(scripts)
            if duplicates:
                all_duplicates[description] = duplicates

        if all_duplicates:
            logging.info("Duplicate tracking codes found:")
            print("Duplicate tracking codes found:")
            for tracker, duplicates in all_duplicates.items():
                for script, count in duplicates.items():
                    logging.info(f"{tracker}: {script} - {count} times")
                    print(f"{tracker}: {script} - {count} times")
        else:
            logging.info("No duplicate tracking codes detected.")
            print("No duplicate tracking codes detected.")

        scripts = extract_scripts(driver)
        issues = analyze_scripts(driver, scripts)
        report_issues(issues)

        # Additional Checks
        print("Extracting inline scripts...")
        inline_scripts = extract_inline_scripts(driver)
        print("Extracting CSS files...")
        css_files = extract_css(driver)
        print("Checking for deprecated HTML tags...")
        deprecated_html = check_deprecated_html(driver, config['deprecated_tags'])
        print("Gathering performance metrics...")
        performance_metrics = get_performance_metrics(driver, url)
        print("Checking SEO issues...")
        seo_issues = check_seo_issues(driver)
        print("Checking accessibility issues...")
        accessibility_issues = check_accessibility_issues(driver)
        print("Finding broken links...")
        broken_links = await find_broken_links(driver)  # Await the asynchronous function
        print("Checking security issues...")
        security_issues = check_security_issues(driver)
        
        print("Generating report...")
        generate_report(url, all_duplicates, issues, inline_scripts, css_files, deprecated_html, performance_metrics, seo_issues, accessibility_issues, broken_links, security_issues)
        print("Report generated.")
    except Exception as e:
        logging.error(f"An error occurred while processing {url}: {e}")
        print(f"An error occurred while processing {url}: {e}")

async def main(urls):
    print("Loading configuration...")
    config = load_config()
    setup_logging(config)
    print("Configuration loaded.")
    logging.info("Configuration loaded.")

    try:
        driver = get_driver(config)

        # Create tasks for each URL
        tasks = [process_url(driver, url, config) for url in urls]

        # Run tasks with tqdm progress bar
        for f in tqdm.as_completed(tasks, total=len(tasks), desc="Processing URLs", unit="url"):
            await f

        driver.quit()
        print("Processing complete.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        sys.exit(1)
