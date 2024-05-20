import logging
from collections import Counter

def find_duplicates(scripts):
    count = Counter(scripts)
    duplicates = {item: quantity for item, quantity in count.items() if quantity > 1}
    logging.info(f"Found {len(duplicates)} duplicate scripts.")
    return duplicates
