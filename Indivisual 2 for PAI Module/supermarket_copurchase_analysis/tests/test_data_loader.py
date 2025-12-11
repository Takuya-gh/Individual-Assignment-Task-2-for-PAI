# Tests for data loader
import unittest
import os
from supermarket_copurchase_analysis.data_loader import load_transactions_from_csv


class TestLoadTransactionsFromCSV(unittest.TestCase):
    """Test suite for load_transactions_from_csv function."""

    def setUp(self):
        """Set up the path to the sample CSV file."""
        # Get the directory where this test file is located
        test_dir = os.path.dirname(os.path.abspath(__file__))
        self.sample_csv_path = os.path.join(test_dir, "sample_data.csv")

    def test_load_sample_csv(self):
        """Test loading the sample CSV file."""
        transactions = load_transactions_from_csv(self.sample_csv_path)
        self.assertIsNotNone(transactions)
        self.assertIsInstance(transactions, list)

    def test_correct_number_of_transactions(self):
        """Test that the correct number of transactions are returned."""
        transactions = load_transactions_from_csv(self.sample_csv_path)
        # Sample data has 3 transactions:
        # (1001, 2024-01-01), (1002, 2024-01-01), (1003, 2024-01-02)
        self.assertEqual(len(transactions), 3)

    def test_transaction_grouping_by_member_and_date(self):
        """Test that transactions are grouped by (Member_number, Date)."""
        transactions = load_transactions_from_csv(self.sample_csv_path)
        # Find the transaction for member 1002 on 2024-01-01
        # It should contain: bread, butter, jam
        transaction_1002 = None
        for t in transactions:
            if set(t) == {"bread", "butter", "jam"}:
                transaction_1002 = t
                break
        self.assertIsNotNone(transaction_1002)
        self.assertEqual(len(transaction_1002), 3)

    def test_items_in_each_transaction(self):
        """Test that items in each transaction are correct."""
        transactions = load_transactions_from_csv(self.sample_csv_path)
        # Transaction for member 1001 should have bread and milk
        transaction_1001 = None
        for t in transactions:
            if set(t) == {"bread", "milk"}:
                transaction_1001 = t
                break
        self.assertIsNotNone(transaction_1001)
        self.assertEqual(len(transaction_1001), 2)


if __name__ == '__main__':
    unittest.main()
