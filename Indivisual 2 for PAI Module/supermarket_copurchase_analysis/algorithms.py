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
