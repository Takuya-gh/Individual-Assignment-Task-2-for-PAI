# Tests for CLI
import unittest
from io import StringIO
import sys
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


if __name__ == '__main__':
    unittest.main()