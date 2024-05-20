# audits/seo_audit/seo_audit.py

import sys
import os
import logging
import yaml  # type: ignore
from datetime import datetime
from tqdm.asyncio import tqdm
from urllib.parse import urlparse, unquote
from core.driver_setup import get_driver
from script_analysis.report.report import generate_seo_report
from utils.common import load_config, setup_logging, create_report_directory, save_json_report
import asyncio

async def process_url(driver, url, config):
    """Process a single URL for SEO analysis."""
    try:
        logging.info(f"Checking {url} for SEO analysis...")
        print(f"\nChecking {url} for SEO analysis...")
        driver.get(url)

        # Perform SEO checks
        meta_tags = check_meta_tags(driver)
        header_tags = check_header_tags(driver)

        # Generate the SEO report
        generate_seo_report(url, meta_tags, header_tags, config)
    except Exception as e:
        logging.error(f"An error occurred while processing {url}: {e}")
        print(f"An error occurred while processing {url}: {e}")

async def main(urls):
    """Main function to process multiple URLs."""
    print("Loading configuration...")
    config = load_config()
    setup_logging(config, "seo")
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python seo_audit.py <url1> <url2> ...")
        sys.exit(1)
    
    urls = sys.argv[1:]
    asyncio.run(main(urls))
