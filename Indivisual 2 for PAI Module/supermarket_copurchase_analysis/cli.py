# CLI for supermarket co-purchase analysis
import argparse
from supermarket_copurchase_analysis.data_loader import load_transactions_from_csv
from supermarket_copurchase_analysis.algorithms import build_graph_from_transactions


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
        
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'load':
        handle_load(args.csv_file)
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


if __name__ == '__main__':
    main()