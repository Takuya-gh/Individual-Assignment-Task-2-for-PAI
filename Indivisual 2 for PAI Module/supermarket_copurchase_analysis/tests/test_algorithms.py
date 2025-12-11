# Tests for algorithms
import unittest
from supermarket_copurchase_analysis.graph_model import CoPurchaseGraph
from supermarket_copurchase_analysis.algorithms import build_graph_from_transactions


class TestBuildGraphFromTransactions(unittest.TestCase):
    """Test suite for build_graph_from_transactions function."""

    def test_build_graph_from_empty_list(self):
        """Test building graph from empty transaction list."""
        transactions = []
        graph = build_graph_from_transactions(transactions)
        self.assertIsInstance(graph, CoPurchaseGraph)
        self.assertEqual(graph.adj, {})

    def test_build_graph_from_sample_transactions(self):
        """Test building graph from sample transactions."""
        transactions = [
            ["bread", "milk"],
            ["bread", "butter", "jam"],
            ["milk"]
        ]
        graph = build_graph_from_transactions(transactions)
        self.assertIsInstance(graph, CoPurchaseGraph)

    def test_correct_node_count(self):
        """Test that all unique items become nodes."""
        transactions = [
            ["bread", "milk"],
            ["bread", "butter"],
        ]
        graph = build_graph_from_transactions(transactions)
        # Should have 3 nodes: bread, milk, butter
        self.assertEqual(len(graph.adj), 3)
        self.assertIn("bread", graph.adj)
        self.assertIn("milk", graph.adj)
        self.assertIn("butter", graph.adj)

    def test_correct_edge_weights(self):
        """Test that edge weights are correct."""
        transactions = [
            ["bread", "milk"],
            ["bread", "milk"],  # Same pair again
            ["bread", "butter"],
        ]
        graph = build_graph_from_transactions(transactions)
        # bread-milk should have weight 2
        self.assertEqual(graph.get_edge_weight("bread", "milk"), 2)
        # bread-butter should have weight 1
        self.assertEqual(graph.get_edge_weight("bread", "butter"), 1)


if __name__ == '__main__':
    unittest.main()
