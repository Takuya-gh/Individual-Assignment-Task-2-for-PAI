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


class TestGetCoPurchasesForItem(unittest.TestCase):
    """Test suite for get_co_purchases_for_item function."""

    def setUp(self):
        """Set up a sample graph for testing."""
        self.graph = CoPurchaseGraph()
        self.graph.add_co_purchase("bread", "milk")
        self.graph.add_co_purchase("bread", "milk")  # weight = 2
        self.graph.add_co_purchase("bread", "butter")  # weight = 1
        self.graph.add_co_purchase("bread", "jam")
        self.graph.add_co_purchase("bread", "jam")
        self.graph.add_co_purchase("bread", "jam")  # weight = 3

    def test_get_co_purchases_for_item_with_neighbors(self):
        """Test getting co-purchases for item with neighbors."""
        from supermarket_copurchase_analysis.algorithms import get_co_purchases_for_item
        result = get_co_purchases_for_item(self.graph, "bread")
        self.assertIsInstance(result, dict)
        self.assertIn("milk", result)
        self.assertIn("butter", result)
        self.assertIn("jam", result)

    def test_filtering_by_min_count(self):
        """Test filtering by min_count."""
        from supermarket_copurchase_analysis.algorithms import get_co_purchases_for_item
        result = get_co_purchases_for_item(self.graph, "bread", min_count=2)
        # Should only include milk (2) and jam (3), not butter (1)
        self.assertIn("milk", result)
        self.assertIn("jam", result)
        self.assertNotIn("butter", result)

    def test_sorting_by_count_descending(self):
        """Test that results are sorted by count descending."""
        from supermarket_copurchase_analysis.algorithms import get_co_purchases_for_item
        result = get_co_purchases_for_item(self.graph, "bread")
        items = list(result.keys())
        counts = list(result.values())
        # Check counts are in descending order
        self.assertEqual(counts, sorted(counts, reverse=True))
        # jam (3) should be first
        self.assertEqual(items[0], "jam")

    def test_non_existent_item(self):
        """Test getting co-purchases for non-existent item."""
        from supermarket_copurchase_analysis.algorithms import get_co_purchases_for_item
        result = get_co_purchases_for_item(self.graph, "dragonfruit")
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()
