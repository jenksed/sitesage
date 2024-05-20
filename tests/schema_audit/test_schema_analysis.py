import os
import json
import logging
from datetime import datetime
from utils.common import create_report_directory


def test_create_report_directory():
    base_dir = "./reports"
    urls = [
        "https://www.crownbio.com",
        "https://www.crownbio.com/model-systems/in-vitro/organoids",
        "https://www.example.com/path/to/resource"
    ]

    for url in urls:
        report_dir = create_report_directory(base_dir, url)
        print(f"Report directory for {url}: {report_dir}")

def test_generate_schema_report():
    url = "https://www.crownbio.com/model-systems/in-vitro/organoids"
    schema_data = {"example": "data"}
    config = {
        "reporting": {
            "directory": "./reports"
        }
    }
    
    generate_schema_report(url, schema_data, config)

if __name__ == "__main__":
    test_create_report_directory()
    test_generate_schema_report()
