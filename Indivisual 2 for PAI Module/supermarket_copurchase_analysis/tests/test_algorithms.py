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


class TestGetTopNBundles(unittest.TestCase):
    """Test suite for get_top_n_bundles function."""

    def setUp(self):
        """Set up a sample graph for testing."""
        self.graph = CoPurchaseGraph()
        self.graph.add_co_purchase("bread", "milk")
        self.graph.add_co_purchase("bread", "milk")
        self.graph.add_co_purchase("bread", "milk")  # weight = 3
        self.graph.add_co_purchase("bread", "butter")
        self.graph.add_co_purchase("bread", "butter")  # weight = 2
        self.graph.add_co_purchase("milk", "butter")  # weight = 1
        self.graph.add_co_purchase("jam", "honey")
        self.graph.add_co_purchase("jam", "honey")
        self.graph.add_co_purchase("jam", "honey")
        self.graph.add_co_purchase("jam", "honey")  # weight = 4

    def test_get_top_n_bundles_returns_list(self):
        """Test that get_top_n_bundles returns a list."""
        from supermarket_copurchase_analysis.algorithms import get_top_n_bundles
        result = get_top_n_bundles(self.graph, n=2)
        self.assertIsInstance(result, list)

    def test_get_top_2_bundles(self):
        """Test getting top 2 bundles."""
        from supermarket_copurchase_analysis.algorithms import get_top_n_bundles
        result = get_top_n_bundles(self.graph, n=2)
        self.assertEqual(len(result), 2)
        # First should be (jam, honey) with count 4
        self.assertEqual(result[0][2], 4)
        # Second should be (bread, milk) with count 3
        self.assertEqual(result[1][2], 3)

    def test_bundles_sorted_descending_by_count(self):
        """Test that bundles are sorted by count descending."""
        from supermarket_copurchase_analysis.algorithms import get_top_n_bundles
        result = get_top_n_bundles(self.graph, n=10)
        counts = [bundle[2] for bundle in result]
        self.assertEqual(counts, sorted(counts, reverse=True))

    def test_each_pair_appears_once(self):
        """Test that each undirected pair appears only once."""
        from supermarket_copurchase_analysis.algorithms import get_top_n_bundles
        result = get_top_n_bundles(self.graph, n=10)
        pairs = [(bundle[0], bundle[1]) for bundle in result]
        # Check no duplicate pairs (considering undirected)
        seen = set()
        for item_a, item_b in pairs:
            pair = tuple(sorted([item_a, item_b]))
            self.assertNotIn(pair, seen)
            seen.add(pair)

    def test_empty_graph_returns_empty_list(self):
        """Test that empty graph returns empty list."""
        from supermarket_copurchase_analysis.algorithms import get_top_n_bundles
        empty_graph = CoPurchaseGraph()
        result = get_top_n_bundles(empty_graph, n=5)
        self.assertEqual(result, [])

    def test_n_larger_than_edges(self):
        """Test requesting more bundles than exist."""
        from supermarket_copurchase_analysis.algorithms import get_top_n_bundles
        result = get_top_n_bundles(self.graph, n=100)
        # Should return all 4 edges without error
        self.assertEqual(len(result), 4)


class TestAreOftenCopurchased(unittest.TestCase):
    """Test suite for are_often_copurchased function."""

    def setUp(self):
        """Set up a sample graph for testing."""
        self.graph = CoPurchaseGraph()
        self.graph.add_co_purchase("bread", "milk")
        self.graph.add_co_purchase("bread", "milk")
        self.graph.add_co_purchase("bread", "milk")
        self.graph.add_co_purchase("bread", "milk")
        self.graph.add_co_purchase("bread", "milk")  # weight = 5
        self.graph.add_co_purchase("bread", "butter")
        self.graph.add_co_purchase("bread", "butter")  # weight = 2
        self.graph.add_co_purchase("jam", "honey")  # weight = 1

    def test_returns_boolean(self):
        """Test that are_often_copurchased returns a boolean."""
        from supermarket_copurchase_analysis.algorithms import are_often_copurchased
        result = are_often_copurchased(self.graph, "bread", "milk", threshold=3)
        self.assertIsInstance(result, bool)

    def test_above_threshold_returns_true(self):
        """Test that items above threshold return True."""
        from supermarket_copurchase_analysis.algorithms import are_often_copurchased
        # bread-milk has weight 5, threshold 3
        result = are_often_copurchased(self.graph, "bread", "milk", threshold=3)
        self.assertTrue(result)

    def test_below_threshold_returns_false(self):
        """Test that items below threshold return False."""
        from supermarket_copurchase_analysis.algorithms import are_often_copurchased
        # bread-butter has weight 2, threshold 3
        result = are_often_copurchased(self.graph, "bread", "butter", threshold=3)
        self.assertFalse(result)

    def test_equal_to_threshold_returns_true(self):
        """Test that items equal to threshold return True."""
        from supermarket_copurchase_analysis.algorithms import are_often_copurchased
        # bread-milk has weight 5, threshold 5
        result = are_often_copurchased(self.graph, "bread", "milk", threshold=5)
        self.assertTrue(result)

    def test_non_existent_items_return_false(self):
        """Test that non-existent items return False."""
        from supermarket_copurchase_analysis.algorithms import are_often_copurchased
        result = are_often_copurchased(self.graph, "dragonfruit", "kiwi", threshold=1)
        self.assertFalse(result)

    def test_no_edge_between_items_returns_false(self):
        """Test that items with no edge return False."""
        from supermarket_copurchase_analysis.algorithms import are_often_copurchased
        # bread and jam have no edge
        result = are_often_copurchased(self.graph, "bread", "jam", threshold=1)
        self.assertFalse(result)

    def test_symmetric_check(self):
        """Test that order of items doesn't matter."""
        from supermarket_copurchase_analysis.algorithms import are_often_copurchased
        result1 = are_often_copurchased(self.graph, "bread", "milk", threshold=3)
        result2 = are_often_copurchased(self.graph, "milk", "bread", threshold=3)
        self.assertEqual(result1, result2)
        self.assertTrue(result1)


if __name__ == '__main__':
    unittest.main()
