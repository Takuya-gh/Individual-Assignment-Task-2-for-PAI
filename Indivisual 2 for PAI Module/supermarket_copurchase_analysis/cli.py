# CLI for supermarket co-purchase analysis
import argparse
from supermarket_copurchase_analysis.data_loader import load_transactions_from_csv
from supermarket_copurchase_analysis.algorithms import (
    build_graph_from_transactions,
    get_co_purchases_for_item,
    get_top_n_bundles,
    are_often_copurchased
)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Supermarket Co-Purchase Analysis Tool',
        prog='cli.py'
    )

    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Load command
    load_parser = subparsers.add_parser('load', help='Load transactions from CSV file')
    load_parser.add_argument('csv_file', help='Path to the CSV file')

    # Query command
    query_parser = subparsers.add_parser('query', help='Find co-purchases for an item')
    query_parser.add_argument('csv_file', help='Path to the CSV file')
    query_parser.add_argument('item', help='Item name to query')
    query_parser.add_argument('--min-count', type=int, default=1, 
                             help='Minimum co-purchase count (default: 1)')

    # Bundles command
    bundles_parser = subparsers.add_parser('bundles', help='Find top N co-purchased bundles')
    bundles_parser.add_argument('csv_file', help='Path to the CSV file')
    bundles_parser.add_argument('n', type=int, help='Number of top bundles to return')

    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'load':
        handle_load(args.csv_file)
    elif args.command == 'query':
        handle_query(args.csv_file, args.item, args.min_count)
    elif args.command == 'bundles':
        handle_bundles(args.csv_file, args.n)
    else:
        parser.print_help()


def handle_load(csv_file):
    """Handle the load command."""
    # Load transactions from CSV
    transactions = load_transactions_from_csv(csv_file)
    
    # Build graph
    graph = build_graph_from_transactions(transactions)
    
    # Print statistics
    print(f"Successfully loaded {len(transactions)} transactions")
    print(f"Graph contains {len(graph.adj)} unique items")
    
    # Count total edges
    total_edges = sum(len(neighbors) for neighbors in graph.adj.values()) // 2
    print(f"Graph contains {total_edges} co-purchase relationships")


def handle_query(csv_file, item, min_count):
    """Handle the query command."""
    # Load transactions and build graph
    transactions = load_transactions_from_csv(csv_file)
    graph = build_graph_from_transactions(transactions)
    
    # Get co-purchases for the item
    co_purchases = get_co_purchases_for_item(graph, item, min_count)
    
    # Print results
    print(f"Co-purchases for '{item}' (min_count={min_count}):")
    
    if not co_purchases:
        print("  No co-purchases found")
    else:
        for copurchased_item, count in co_purchases.items():
            print(f"  {copurchased_item}: {count}")


def handle_bundles(csv_file, n):
    """Handle the bundles command."""
    # Load transactions and build graph    
    transactions = load_transactions_from_csv(csv_file)
    graph = build_graph_from_transactions(transactions)
    
    # Get top N bundles
    bundles = get_top_n_bundles(graph, n)
    
    # Print results
    print(f"Top {n} bundles:")
    
    if not bundles:
        print("  No bundles found")
    else:
        for item_a, item_b, count in bundles:
            print(f"  {item_a} + {item_b}: {count}")


def handle_check(csv_file, item_a, item_b, threshold):
    """Handle the check command."""
    # Load transactions and build graph
    transactions = load_transactions_from_csv(csv_file)
    graph = build_graph_from_transactions(transactions)
    
    # Check if items are often co-purchased
    result = are_often_copurchased(graph, item_a, item_b, threshold)
    
    # Get the actual count for informative output
    count = graph.get_edge_weight(item_a, item_b)
    
    # Print results
    if result:
        print(f"Yes, '{item_a}' and '{item_b}' are often co-purchased (count: {count}, threshold: {threshold})")
    else:
        print(f"No, '{item_a}' and '{item_b}' are not often co-purchased (count: {count}, threshold: {threshold})")


if __name__ == '__main__':
    main()