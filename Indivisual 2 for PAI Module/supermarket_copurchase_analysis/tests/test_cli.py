# Tests for CLI
import unittest
from io import StringIO
import sys
import os
from supermarket_copurchase_analysis.cli import main


class TestCLIBasicExecution(unittest.TestCase):
    """Test suite for basic CLI execution."""

    def test_main_function_exists(self):
        """Test that main function exists and is callable."""
        self.assertTrue(callable(main))

    def test_main_with_no_args_shows_help(self):
        """Test that running main with no arguments shows help message."""
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        # Run main with empty args (simulating no command)
        sys.argv = ['cli.py']
        try:
            main()
            output = sys.stdout.getvalue()
            # Should contain some help text or usage information
            self.assertIn('usage', output.lower())
        finally:
            sys.stdout = old_stdout


class TestCLILoadCommand(unittest.TestCase):
    """Test suite for load command."""

    def setUp(self):
        """Set up test fixtures."""
        # Get the path to the sample CSV file
        test_dir = os.path.dirname(os.path.abspath(__file__))
        self.sample_csv_path = os.path.join(test_dir, "sample_data.csv")

    def test_load_command_with_csv_file(self):
        """Test that load command can process a CSV file."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        sys.argv = ['cli.py', 'load', self.sample_csv_path]
        try:
            main()
            output = sys.stdout.getvalue()
            # Should indicate success
            self.assertIn('loaded', output.lower())
        finally:
            sys.stdout = old_stdout

    def test_load_command_shows_graph_statistics(self):
        """Test that load command shows basic graph statistics."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        sys.argv = ['cli.py', 'load', self.sample_csv_path]
        try:
            main()
            output = sys.stdout.getvalue()
            # Should show some statistics about the loaded graph
            self.assertIn('items', output.lower())
        finally:
            sys.stdout = old_stdout


class TestCLIQueryCommand(unittest.TestCase):
    """Test suite for query command."""

    def setUp(self):
        """Set up test fixtures."""
        # Get the path to the sample CSV file
        test_dir = os.path.dirname(os.path.abspath(__file__))
        self.sample_csv_path = os.path.join(test_dir, "sample_data.csv")

    def test_query_command_with_item_name(self):
        """Test that query command can find co-purchases for an item."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        sys.argv = ['cli.py', 'query', self.sample_csv_path, 'bread']
        try:
            main()
            output = sys.stdout.getvalue()
            # Should show co-purchases for bread
            self.assertIn('bread', output.lower())
        finally:
            sys.stdout = old_stdout

    def test_query_command_shows_copurchased_items(self):
        """Test that query command shows items co-purchased with target item."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        sys.argv = ['cli.py', 'query', self.sample_csv_path, 'bread']
        try:
            main()
            output = sys.stdout.getvalue()
            # bread is co-purchased with milk, butter, jam in sample data
            self.assertTrue('milk' in output.lower() or 'butter' in output.lower() or 'jam' in output.lower())
        finally:
            sys.stdout = old_stdout

    def test_query_command_with_min_count_filter(self):
        """Test that query command respects min_count filter."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        sys.argv = ['cli.py', 'query', self.sample_csv_path, 'bread', '--min-count', '1']
        try:
            main()
            output = sys.stdout.getvalue()
            # Should show results with at least 1 co-purchase
            self.assertIn('bread', output.lower())
        finally:
            sys.stdout = old_stdout

if __name__ == '__main__':
    unittest.main()