# script_analysis/report/report.py

import logging
import os
from datetime import datetime
from urllib.parse import urlparse, unquote

def report_issues(issues):
    for issue in issues:
        print(issue)
        logging.info(issue)

def generate_report(url, all_duplicates, issues, inline_scripts, css_files, deprecated_html, performance_metrics, seo_issues, accessibility_issues, broken_links, security_issues, reports_dir):
    # Ensure the reports directory exists
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    # Create a unique filename for the report based on the current timestamp
    now = datetime.now()
    report_filename = os.path.join(reports_dir, now.strftime("report_%Y%m%d_%H%M%S.txt"))

    # Generate the report content
    report_content = []
    report_content.append(f"URL: {url}")
    report_content.append("\n=== Duplicate Trackers ===")
    for tracker, duplicates in all_duplicates.items():
        report_content.append(f"{tracker}:")
        for script, count in duplicates.items():
            report_content.append(f"  {script} - {count} times")
    
    report_content.append("\n=== Script Issues ===")
    for issue in issues:
        report_content.append(issue)
    
    report_content.append("\n=== Inline Scripts ===")
    for script in inline_scripts:
        report_content.append(script)
    
    report_content.append("\n=== CSS Files ===")
    for css in css_files:
        report_content.append(css)
    
    report_content.append("\n=== Deprecated HTML ===")
    for deprecated in deprecated_html:
        report_content.append(deprecated)
    
    report_content.append("\n=== Performance Metrics ===")
    for metric, value in performance_metrics.items():
        report_content.append(f"{metric}: {value}")
    
    report_content.append("\n=== SEO Issues ===")
    for seo_issue in seo_issues:
        report_content.append(seo_issue)
    
    report_content.append("\n=== Accessibility Issues ===")
    for accessibility_issue in accessibility_issues:
        report_content.append(accessibility_issue)
    
    report_content.append("\n=== Broken Links ===")
    for broken_link in broken_links:
        report_content.append(broken_link)
    
    report_content.append("\n=== Security Issues ===")
    for security_issue in security_issues:
        report_content.append(security_issue)
    
    # Print and log the report
    print("\nReport:")
    for line in report_content:
        print(line)
        logging.info(line)

    # Write the report to a file
    with open(report_filename, 'w') as report_file:
        for line in report_content:
            report_file.write(line + '\n')

    logging.info(f"Report generated and saved to {report_filename}.")

def generate_seo_report(url, meta_tags, header_tags, config):
    # Ensure the reports directory exists
    reports_dir = create_report_directory("./reports", url)
    
    # Create a unique filename for the report based on the current timestamp
    now = datetime.now()
    report_filename = os.path.join(reports_dir, now.strftime("seo_audit_%Y%m%d_%H%M%S.txt"))

    # Generate the SEO report content
    report_content = []
    report_content.append(f"URL: {url}")
    report_content.append(f"\n=== Meta Tags ===")
    for meta in meta_tags:
        report_content.append(meta)
    
    report_content.append("\n=== Header Tags ===")
    for header in header_tags:
        report_content.append(header)
    
    # Print and log the SEO report
    print("\nSEO Report:")
    for line in report_content:
        print(line)
        logging.info(line)

    # Write the SEO report to a file
    with open(report_filename, 'w') as report_file:
        for line in report_content:
            report_file.write(line + '\n')

    logging.info(f"SEO Report generated and saved to {report_filename}.")

def generate_schema_report(url, schema_data, config):
    # Ensure the reports directory exists
    reports_dir = create_report_directory("./reports", url)
    
    # Create a unique filename for the report based on the current timestamp
    now = datetime.now()
    report_filename = os.path.join(reports_dir, now.strftime("schema_audit_%Y%m%d_%H%M%S.txt"))

    # Generate the schema report content
    report_content = []
    report_content.append(f"URL: {url}")
    report_content.append("\n=== Schema Data ===")
    for schema in schema_data:
        report_content.append(schema)
    
    # Print and log the schema report
    print("\nSchema Report:")
    for line in report_content:
        print(line)
        logging.info(line)

    # Write the schema report to a file
    with open(report_filename, 'w') as report_file:
        for line in report_content:
            report_file.write(line + '\n')

    logging.info(f"Schema Report generated and saved to {report_filename}.")

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
    return path.replace("-", "_").replace(" ", "_").replace(":", "_")
