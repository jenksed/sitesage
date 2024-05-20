import logging
import os
import json
from datetime import datetime
from utils.common import create_report_directory, save_json_report

def report_issues(issues):
    for issue in issues:
        print(issue)
        logging.info(issue)

def generate_report(url, all_duplicates, issues, inline_scripts, css_files, deprecated_html, performance_metrics, seo_issues, accessibility_issues, broken_links, security_issues):
    # Ensure the reports directory exists
    reports_dir = create_report_directory("./reports", url)
    
    # Create a unique filename for the report based on the current timestamp
    now = datetime.now()
    report_filename = os.path.join(reports_dir, now.strftime("page_analysis_%Y%m%d_%H%M%S.txt"))
    inline_script_filename = os.path.join(reports_dir, now.strftime("page_analysis_%Y%m%d_%H%M%S_inline_scripts.txt"))
    json_report_filename = os.path.join(reports_dir, now.strftime("page_analysis_%Y%m%d_%H%M%S.json"))

    # Generate the report content
    report_content = {
        "url": url,
        "duplicate_trackers": all_duplicates,
        "script_issues": issues,
        "css_files": css_files,
        "deprecated_html": deprecated_html,
        "performance_metrics": performance_metrics,
        "seo_issues": seo_issues,
        "accessibility_issues": accessibility_issues,
        "broken_links": broken_links,
        "security_issues": security_issues
    }
    
    # Print and log the report
    print("\nPage Analysis Report:")
    for section, content in report_content.items():
        print(f"\n=== {section.replace('_', ' ').title()} ===")
        logging.info(f"\n=== {section.replace('_', ' ').title()} ===")
        if isinstance(content, dict):
            for key, value in content.items():
                print(f"{key}: {value}")
                logging.info(f"{key}: {value}")
        else:
            for item in content:
                print(item)
                logging.info(item)

    # Write the report to a file
    with open(report_filename, 'w') as report_file:
        for section, content in report_content.items():
            report_file.write(f"\n=== {section.replace('_', ' ').title()} ===\n")
            if isinstance(content, dict):
                for key, value in content.items():
                    report_file.write(f"{key}: {value}\n")
            else:
                for item in content:
                    report_file.write(f"{item}\n")
    
    logging.info(f"Page Analysis Report generated and saved to {report_filename}.")

    # Write the inline scripts to a separate file
    with open(inline_script_filename, 'w') as script_file:
        for script in inline_scripts:
            script_file.write(script + '\n')
    
    logging.info(f"Inline Scripts saved to {inline_script_filename}.")

    # Save JSON report
    save_json_report(report_content, json_report_filename)

def generate_seo_report(url, meta_tags, header_tags, config):
    # Ensure the reports directory exists
    reports_dir = create_report_directory("./reports", url)
    
    # Create a unique filename for the report based on the current timestamp
    now = datetime.now()
    report_filename = os.path.join(reports_dir, now.strftime("seo_audit_%Y%m%d_%H%M%S.txt"))
    json_report_filename = os.path.join(reports_dir, now.strftime("seo_audit_%Y%m%d_%H%M%S.json"))

    # Generate the report content
    report_content = {
        "url": url,
        "meta_tags": meta_tags,
        "header_tags": header_tags
    }
    
    # Print and log the report
    print("\nSEO Report:")
    for section, content in report_content.items():
        print(f"\n=== {section.replace('_', ' ').title()} ===")
        logging.info(f"\n=== {section.replace('_', ' ').title()} ===")
        for item in content:
            print(item)
            logging.info(item)

    # Write the report to a file
    with open(report_filename, 'w') as report_file:
        for section, content in report_content.items():
            report_file.write(f"\n=== {section.replace('_', ' ').title()} ===\n")
            for item in content:
                report_file.write(f"{item}\n")

    logging.info(f"SEO Report generated and saved to {report_filename}.")

    # Save JSON report
    save_json_report(report_content, json_report_filename)

def generate_schema_report(url, schema_data, config):
    # Ensure the reports directory exists
    reports_dir = create_report_directory("./reports", url)
    
    # Create a unique filename for the report based on the current timestamp
    now = datetime.now()
    report_filename = os.path.join(reports_dir, now.strftime("schema_audit_%Y%m%d_%H%M%S.txt"))
    json_report_filename = os.path.join(reports_dir, now.strftime("schema_audit_%Y%m%d_%H%M%S.json"))

    # Generate the report content
    report_content = {
        "url": url,
        "schema_data": schema_data
    }
    
    # Print and log the report
    print("\nSchema Report:")
    for section, content in report_content.items():
        print(f"\n=== {section.replace('_', ' ').title()} ===")
        logging.info(f"\n=== {section.replace('_', ' ').title()} ===")
        for item in content:
            print(item)
            logging.info(item)

    # Write the report to a file
    with open(report_filename, 'w') as report_file:
        for section, content in report_content.items():
            report_file.write(f"\n=== {section.replace('_', ' ').title()} ===\n")
            for item in content:
                report_file.write(f"{item}\n")

    logging.info(f"Schema Report generated and saved to {report_filename}.")

    # Save JSON report
    save_json_report(report_content, json_report_filename)
