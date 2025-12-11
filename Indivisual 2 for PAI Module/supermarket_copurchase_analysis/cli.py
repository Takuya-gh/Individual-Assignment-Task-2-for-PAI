# CLI for supermarket co-purchase analysis
import argparse


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Supermarket Co-Purchase Analysis Tool',
        prog='cli.py'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no subcommands are added yet, just show help
    parser.print_help()


if __name__ == '__main__':
    main()