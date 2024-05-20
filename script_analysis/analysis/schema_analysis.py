import logging
from aiohttp import ClientSession
from extraction.schema_extract import extract_schema_data, refine_schema_data
from utils.common import create_report_directory, save_json_report, load_config, setup_logging

async def fetch_page(session, url):
    """Asynchronously fetch a page and return its content."""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                logging.error(f"Failed to fetch {url}: HTTP status {response.status}")
                return None
    except Exception as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None

async def process_url(url, config):
    """Process a URL to extract and report its schema data."""
    logging.info(f"Checking {url} for schema analysis...")
    try:
        async with ClientSession() as session:
            page_content = await fetch_page(session, url)
            if page_content:
                schema_data = extract_schema_data(page_content)
                refined_schema_data = refine_schema_data(schema_data)
                generate_schema_report(url, refined_schema_data, config)
            else:
                logging.error(f"No content retrieved from {url}")
    except Exception as e:
        logging.error(f"Error processing {url}: {e}")
