import os
import logging
import yaml
import json
from datetime import datetime
from urllib.parse import urlparse, unquote

def load_config(config_file='config/config.yaml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def setup_logging(config, audit_type):
    log_dir = config['logging']['directory']
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    now = datetime.now()
    log_filename = now.strftime(f"{log_dir}/{audit_type}_audit_%Y%m%d_%H%M%S.log")

    logging.basicConfig(filename=log_filename, level=getattr(logging, config['logging']['level'].upper()),
                        format=config['logging']['format'])

    console = logging.StreamHandler()
    console.setLevel(getattr(logging, config['logging']['level'].upper()))
    formatter = logging.Formatter(config['logging']['format'])
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.info("Logging setup complete.")

def create_report_directory(base_dir, url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('.', '_')
    path = unquote(parsed_url.path).strip("/")
    
    if not path:
        path = domain
    else:
        path = f"{domain}_{path.replace('/', '_')}"

    path = sanitize_path(path)
    report_dir = os.path.join(base_dir, path)
    
    if not os.path.exists(report_dir):
        os.makedirs(report_dir, exist_ok=True)
    
    return report_dir

def sanitize_path(path):
    # Additional replacements to handle other possible problematic characters
    return path.replace("-", "_").replace(" ", "_").replace(":", "_")

def save_json_report(report_data, filename):
    """Save the report data as a JSON file."""
    with open(filename, 'w') as json_file:
        json.dump(report_data, json_file, indent=4)
    logging.info(f"JSON report saved to {filename}")
