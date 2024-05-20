import spacy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import os
import logging
from selenium.webdriver.common.by import By
from utils.common import create_report_directory
from script_analysis.extraction.script_extraction import extract_page_text

# Ensure the VADER lexicon is downloaded
nltk.download('vader_lexicon')

# Load spaCy's small English language model
nlp = spacy.load('en_core_web_sm')

# Initialize the VADER sentiment intensity analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_text(text):
    """Analyze the text and return results for various NLP tasks."""
    doc = nlp(text)
    results = {
        'sentences': [],
        'named_entities': [],
        'keywords': [],
        'sentiment': sentiment_analysis(text)
    }
    
    # Extract sentences
    for sent in doc.sents:
        results['sentences'].append(sent.text)
    
    # Extract named entities
    for ent in doc.ents:
        results['named_entities'].append((ent.text, ent.label_))
    
    # Extract keywords
    for chunk in doc.noun_chunks:
        results['keywords'].append(chunk.text)
    
    return results

def sentiment_analysis(text):
    """Perform sentiment analysis using VADER."""
    return analyzer.polarity_scores(text)

def extract_text_from_url(driver):
    """Extract and filter visible text content from a webpage."""
    return extract_page_text(driver)

def generate_nlp_report(url, text, results, config):
    """Generate a report for NLP analysis."""
    # Ensure the reports directory exists
    reports_dir = create_report_directory("./reports", url)
    
    # Create a unique filename for the report based on the current timestamp
    now = datetime.now()
    report_filename = os.path.join(reports_dir, now.strftime("nlp_analysis_%Y%m%d_%H%M%S.txt"))

    # Generate the NLP report content
    report_content = []
    report_content.append(f"URL: {url}")
    report_content.append(f"\n=== Text Sentences ===")
    for sentence in results['sentences']:
        report_content.append(sentence)
    
    report_content.append("\n=== Named Entities ===")
    for entity, label in results['named_entities']:
        report_content.append(f"{entity} ({label})")
    
    report_content.append("\n=== Keywords ===")
    for keyword in results['keywords']:
        report_content.append(keyword)
    
    report_content.append("\n=== Sentiment Analysis ===")
    report_content.append(str(results['sentiment']))

    # Print and log the NLP report
    print("\nNLP Report:")
    for line in report_content:
        print(line)
        logging.info(line)
    
    # Write the NLP report to a file
    with open(report_filename, 'w') as report_file:
        for line in report_content:
            report_file.write(line + '\n')

    logging.info(f"NLP Report generated and saved to {report_filename}.")
