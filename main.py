import sys
import asyncio
import logging
import os
from audits.page_audit.page_audit import main as page_audit_main
from audits.nlp_audit.nlp_audit import main as nlp_audit_main
from audits.schema_audit.schema_audit import main as schema_audit_main
from audits.seo_audit.seo_audit import main as seo_audit_main

def print_usage():
    print("Usage: python main.py [--page-analysis | --seo-audit | --nlp-audit | --schema-audit] <url1> <url2> ...")
    print("       python main.py --create-pattern <pattern_name>")

def create_pattern_file(pattern_name):
    patterns_dir = './script_analysis/extraction/unwanted_patterns'
    if not os.path.exists(patterns_dir):
        os.makedirs(patterns_dir)

    pattern_file_path = os.path.join(patterns_dir, f"{pattern_name}.txt")
    with open(pattern_file_path, 'w') as f:
        f.write("")
    
    print(f"Pattern file '{pattern_name}.txt' created successfully in {patterns_dir}.")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    flag = sys.argv[1]

    if flag == "--create-pattern":
        if len(sys.argv) != 3:
            print("Usage: python main.py --create-pattern <pattern_name>")
            sys.exit(1)
        pattern_name = sys.argv[2]
        create_pattern_file(pattern_name)
    else:
        urls = sys.argv[2:]

        actions = {
            '--page-analysis': page_audit_main,
            '--seo-audit': seo_audit_main,
            '--nlp-audit': nlp_audit_main,
            '--schema-audit': schema_audit_main
        }

        if flag in actions:
            asyncio.run(actions[flag](urls))
        else:
            print_usage()
            sys.exit(1)
