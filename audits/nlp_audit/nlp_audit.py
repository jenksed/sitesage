import sys
import os
import logging
import yaml
from datetime import datetime
from tqdm.asyncio import tqdm
from core.driver_setup import get_driver
from audits.nlp_audit.nlp_analysis import analyze_text, extract_text_from_url, generate_nlp_report
from utils.common import load_config, setup_logging, create_report_directory, save_json_report
import asyncio

# Rest of the code remains the same


def create_unwanted_pattern_file(pattern_name):
    """Create a new unwanted pattern file in the specified directory."""
    patterns_dir = os.path.join(os.path.dirname(__file__), '../script_analysis/extraction/unwanted_patterns')
    if not os.path.exists(patterns_dir):
        os.makedirs(patterns_dir)
    
    pattern_file_path = os.path.join(patterns_dir, f"{pattern_name}.txt")
    if not os.path.exists(pattern_file_path):
        with open(pattern_file_path, 'w') as file:
            file.write("Replace this text with the unwanted pattern.")
        print(f"Pattern file created: {pattern_file_path}")
    else:
        print(f"Pattern file already exists: {pattern_file_path}")

async def process_url(driver, url, config):
    """Process a single URL for NLP analysis."""
    try:
        logging.info(f"Checking {url} for NLP analysis...")
        print(f"\nChecking {url} for NLP analysis...")
        driver.get(url)

        # Extract text content from the webpage
        text = extract_text_from_url(driver)

        # Perform NLP analysis
        results = analyze_text(text)

        # Generate the NLP report
        generate_nlp_report(url, text, results, config)
    except Exception as e:
        logging.error(f"An error occurred while processing {url}: {e}")
        print(f"An error occurred while processing {url}: {e}")

async def main(urls):
    """Main function to process multiple URLs."""
    print("Loading configuration...")
    config = load_config()
    setup_logging(config, "nlp")
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
        print("Usage: python nlp_audit.py [--create-pattern pattern_name] <url1> <url2> ...")
        sys.exit(1)

    if sys.argv[1] == '--create-pattern':
        if len(sys.argv) != 3:
            print("Usage: python nlp_audit.py --create-pattern pattern_name")
            sys.exit(1)
        pattern_name = sys.argv[2]
        create_unwanted_pattern_file(pattern_name)
        sys.exit(0)
    else:
        urls = sys.argv[1:]
        asyncio.run(main(urls))
