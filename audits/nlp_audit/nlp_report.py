import os
import logging
from datetime import datetime
from urllib.parse import urlparse, unquote

def create_report_directory(base_dir, url):
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path).strip("/").replace("/", "_")
    path = sanitize_path(path)
    report_dir = os.path.join(base_dir, path)
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def sanitize_path(path):
    return path.replace("-", "_")

def generate_nlp_report(url, text, results, config):
    reports_dir = "./reports"
    report_dir = create_report_directory(reports_dir, url)

    now = datetime.now()
    report_filename = os.path.join(report_dir, now.strftime("nlp_analysis_%Y%m%d_%H%M%S.txt"))

    report_content = [
        f"URL: {url}",
        "\n=== Text Sentences ==="
    ] + results['sentences'][:10] + [
        "\n=== Named Entities ==="
    ] + [f"{entity} ({label})" for entity, label in results['named_entities']] + [
        "\n=== Keywords ==="
    ] + results['keywords'] + [
        "\n=== Sentiment Analysis ===",
        str(results['sentiment']),
        "\n=== Readability Scores ===",
        str(results['readability']),
        "\n=== Engagement Metrics ===",
        str(results['engagement']),
        "\n=== Part-of-Speech Tags ===",
        str(results['pos_tags'])
    ]

    print("\nNLP Report:")
    for line in report_content:
        print(line)
        logging.info(line)

    with open(report_filename, 'w') as report_file:
        for line in report_content:
            report_file.write(line + '\n')

    logging.info(f"NLP Report generated and saved to {report_filename}.")
