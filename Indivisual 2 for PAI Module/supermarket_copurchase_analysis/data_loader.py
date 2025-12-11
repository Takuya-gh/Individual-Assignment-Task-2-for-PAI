# Data loader for CSV transactions
import csv
from collections import defaultdict


def load_transactions_from_csv(filepath):
    """
    Load the supermarket dataset and return a list of transactions.
    
    One transaction = all rows with same (Member_number, Date).
    
    Args:
        filepath (str): Path to the CSV file.
    
    Returns:
        list: List of transactions, where each transaction is a list of items.
    """
    # Use defaultdict to group items by (member_number, date)
    baskets = defaultdict(list)
    
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            member_number = row['Member_number'].strip()
            date = row['Date'].strip()
            item = row['itemDescription'].strip()
            
            # Group by (member_number, date)
            key = (member_number, date)
            baskets[key].append(item)
    
    # Convert to list of transactions
    return list(baskets.values())