# Algorithms for graph building and queries
from supermarket_copurchase_analysis.graph_model import CoPurchaseGraph


def build_graph_from_transactions(transactions):
    """
    Create a CoPurchaseGraph and populate it from the list of transactions.

    Args:
        transactions (list): List of transactions, where each transaction
                           is a list of item names.

    Returns:
        CoPurchaseGraph: The populated graph.
    """
    graph = CoPurchaseGraph()
    
    for transaction in transactions:
        graph.add_transaction(transaction)
    
    return graph


def get_co_purchases_for_item(graph, item, min_count=1):
    """
    Return neighbors of item whose co-purchase count >= min_count.
    Sorted by count descending.

    Args:
        graph (CoPurchaseGraph): The graph.
        item (str): The item name.
        min_count (int): Minimum co-purchase count.

    Returns:
        dict: Dictionary of neighbors with counts >= min_count,
              sorted by count descending.
    """
    neighbors = graph.get_neighbors(item)
    
    # Filter by min_count
    filtered = {k: v for k, v in neighbors.items() if v >= min_count}
    
    # Sort by count descending
    sorted_items = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    
    return dict(sorted_items)