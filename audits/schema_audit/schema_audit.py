# audits/schema_audit/schema_audit.py

import sys
import os
import logging
import yaml  # type: ignore
from datetime import datetime
from tqdm.asyncio import tqdm
from urllib.parse import urlparse, unquote
from core.driver_setup import get_driver
from script_analysis.report.report import generate_schema_report
from utils.common import load_config, setup_logging, create_report_directory, save_json_report
import asyncio

async def process_url(driver, url, config):
    """Process a single URL for schema analysis."""
    try:
        logging.info(f"Checking {url} for schema analysis...")
        print(f"\nChecking {url} for schema analysis...")
        driver.get(url)

        # Perform schema checks
        schema_data = {}  # Placeholder for actual schema extraction logic

        # Generate the schema report
        generate_schema_report(url, schema_data, config)
    except Exception as e:
        logging.error(f"An error occurred while processing {url}: {e}")
        print(f"An error occurred while processing {url}: {e}")

async def main(urls):
    """Main function to process multiple URLs."""
    print("Loading configuration...")
    config = load_config()
    setup_logging(config, "schema")
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
        print("Usage: python schema_audit.py <url1> <url2> ...")
        sys.exit(1)
    
    urls = sys.argv[1:]
    asyncio.run(main(urls))
