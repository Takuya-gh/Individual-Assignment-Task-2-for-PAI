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


def get_top_n_bundles(graph, n):
    """
    Return the top N most frequently co-purchased item pairs (bundles).
    Each pair appears only once (undirected).

    Args:
        graph (CoPurchaseGraph): The graph.
        n (int): Number of top bundles to return.

    Returns:
        list: List of tuples (item_a, item_b, count), sorted by count descending.
    """
    bundles = []
    seen = set()

    # Iterate through all edges
    for item_a in graph.adj:
        for item_b, count in graph.adj[item_a].items():
            # Create a canonical representation of the pair
            pair = tuple(sorted([item_a, item_b]))

            # Only add each pair once
            if pair not in seen:
                bundles.append((item_a, item_b, count))
                seen.add(pair)

    # Sort by count descending
    bundles.sort(key=lambda x: x[2], reverse=True)

    # Return top n
    return bundles[:n]


def are_often_copurchased(graph, item_a, item_b, threshold):
    """
    Check if two items are often co-purchased (count >= threshold).

    Args:
        graph (CoPurchaseGraph): The graph.
        item_a (str): First item name.
        item_b (str): Second item name.
        threshold (int): Minimum co-purchase count to be considered "often".

    Returns:
        bool: True if co-purchase count >= threshold, False otherwise.
    """
    count = graph.get_edge_weight(item_a, item_b)
    return count >= threshold


def bfs_related_items(graph, start_item, max_depth=None):
    """
    Use BFS to find all items related to start_item within max_depth.
    Returns items reachable from start_item (excluding start_item itself).

    Args:
        graph (CoPurchaseGraph): The graph.
        start_item (str): The starting item name.
        max_depth (int, optional): Maximum depth to search. None means unlimited.

    Returns:
        list: List of related item names (excluding start_item).
    """
    from collections import deque

    # Check if start_item exists
    if start_item not in graph.adj:
        return []

    visited = set()
    visited.add(start_item)
    queue = deque([(start_item, 0)])  # (item, depth)
    related = []

    while queue:
        current_item, depth = queue.popleft()

        # Check if we've reached max_depth
        if max_depth is not None and depth >= max_depth:
            continue

        # Explore neighbors
        neighbors = graph.get_neighbors(current_item)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                related.append(neighbor)
                queue.append((neighbor, depth + 1))

    return related