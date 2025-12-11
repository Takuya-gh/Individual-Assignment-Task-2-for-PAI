# Tests for graph model
import unittest
from supermarket_copurchase_analysis.graph_model import CoPurchaseGraph


class TestCoPurchaseGraphInitialization(unittest.TestCase):
    """Test suite for CoPurchaseGraph initialization."""

    def test_graph_initialization_creates_empty_graph(self):
        """Test that CoPurchaseGraph() creates an empty graph."""
        graph = CoPurchaseGraph()
        self.assertIsNotNone(graph)

    def test_graph_has_empty_adj_dict(self):
        """Test that graph.adj is an empty dict after initialization."""
        graph = CoPurchaseGraph()
        self.assertEqual(graph.adj, {})
        self.assertIsInstance(graph.adj, dict)


class TestAddItem(unittest.TestCase):
    """Test suite for add_item method."""

    def test_add_single_item_creates_node(self):
        """Test adding a single item creates a node in the graph."""
        graph = CoPurchaseGraph()
        graph.add_item("bread")
        self.assertIn("bread", graph.adj)

    def test_add_item_twice_does_not_break(self):
        """Test adding the same item twice doesn't cause errors."""
        graph = CoPurchaseGraph()
        graph.add_item("milk")
        graph.add_item("milk")
        self.assertIn("milk", graph.adj)

    def test_item_node_has_empty_neighbor_dict_initially(self):
        """Test that a newly added item has an empty neighbor dict."""
        graph = CoPurchaseGraph()
        graph.add_item("butter")
        self.assertEqual(graph.adj["butter"], {})
        self.assertIsInstance(graph.adj["butter"], dict)


class TestAddCoPurchase(unittest.TestCase):
    """Test suite for add_co_purchase method."""

    def test_add_edge_between_two_items_increments_count(self):
        """Test adding an edge between two items creates bidirectional edge."""
        graph = CoPurchaseGraph()
        graph.add_co_purchase("bread", "milk")
        self.assertIn("milk", graph.adj["bread"])
        self.assertIn("bread", graph.adj["milk"])
        self.assertEqual(graph.adj["bread"]["milk"], 1)
        self.assertEqual(graph.adj["milk"]["bread"], 1)

    def test_add_same_edge_multiple_times_increases_weight(self):
        """Test adding the same edge multiple times increases the weight."""
        graph = CoPurchaseGraph()
        graph.add_co_purchase("bread", "butter")
        graph.add_co_purchase("bread", "butter")
        graph.add_co_purchase("bread", "butter")
        self.assertEqual(graph.adj["bread"]["butter"], 3)
        self.assertEqual(graph.adj["butter"]["bread"], 3)

    def test_bidirectional_edge_undirected_graph(self):
        """Test that edges are bidirectional (undirected graph)."""
        graph = CoPurchaseGraph()
        graph.add_co_purchase("eggs", "bacon")
        self.assertEqual(graph.adj["eggs"]["bacon"], graph.adj["bacon"]["eggs"])

    def test_self_loop_ignored(self):
        """Test that self-loops (item with itself) are ignored."""
        graph = CoPurchaseGraph()
        graph.add_co_purchase("milk", "milk")
        # Self-loops should not be added
        self.assertNotIn("milk", graph.adj.get("milk", {}))


class TestAddTransaction(unittest.TestCase):
    """Test suite for add_transaction method."""

    def test_empty_transaction(self):
        """Test that empty transaction doesn't break."""
        graph = CoPurchaseGraph()
        graph.add_transaction([])
        self.assertEqual(graph.adj, {})

    def test_single_item_transaction(self):
        """Test single-item transaction creates no edges."""
        graph = CoPurchaseGraph()
        graph.add_transaction(["bread"])
        self.assertIn("bread", graph.adj)
        self.assertEqual(graph.adj["bread"], {})

    def test_two_item_transaction(self):
        """Test two-item transaction creates one edge."""
        graph = CoPurchaseGraph()
        graph.add_transaction(["bread", "milk"])
        self.assertEqual(graph.adj["bread"]["milk"], 1)
        self.assertEqual(graph.adj["milk"]["bread"], 1)

    def test_three_item_transaction(self):
        """Test three-item transaction creates three edges (AB, AC, BC)."""
        graph = CoPurchaseGraph()
        graph.add_transaction(["bread", "milk", "butter"])
        # Check all three pairs exist
        self.assertEqual(graph.adj["bread"]["milk"], 1)
        self.assertEqual(graph.adj["bread"]["butter"], 1)
        self.assertEqual(graph.adj["milk"]["butter"], 1)

    def test_duplicate_items_in_transaction(self):
        """Test duplicate items in transaction are handled correctly."""
        graph = CoPurchaseGraph()
        graph.add_transaction(["milk", "bread", "milk"])
        # Should only count unique pairs once per transaction
        # Implementation will handle this
        self.assertIn("bread", graph.adj["milk"])


class TestGetNeighbors(unittest.TestCase):
    """Test suite for get_neighbors method."""

    def test_get_neighbors_of_item_with_no_edges(self):
        """Test getting neighbors of item with no edges returns empty dict."""
        graph = CoPurchaseGraph()
        graph.add_item("bread")
        neighbors = graph.get_neighbors("bread")
        self.assertEqual(neighbors, {})

    def test_get_neighbors_of_item_with_edges(self):
        """Test getting neighbors of item with edges."""
        graph = CoPurchaseGraph()
        graph.add_co_purchase("bread", "milk")
        graph.add_co_purchase("bread", "butter")
        neighbors = graph.get_neighbors("bread")
        self.assertEqual(neighbors, {"milk": 1, "butter": 1})

    def test_get_neighbors_of_non_existent_item(self):
        """Test getting neighbors of non-existent item returns empty dict."""
        graph = CoPurchaseGraph()
        neighbors = graph.get_neighbors("dragonfruit")
        self.assertEqual(neighbors, {})


class TestGetEdgeWeight(unittest.TestCase):
    """Test suite for get_edge_weight method."""

    def test_get_weight_of_existing_edge(self):
        """Test getting weight of existing edge."""
        graph = CoPurchaseGraph()
        graph.add_co_purchase("bread", "milk")
        graph.add_co_purchase("bread", "milk")
        weight = graph.get_edge_weight("bread", "milk")
        self.assertEqual(weight, 2)

    def test_get_weight_of_non_existent_edge(self):
        """Test getting weight of non-existent edge returns 0."""
        graph = CoPurchaseGraph()
        graph.add_item("bread")
        graph.add_item("milk")
        weight = graph.get_edge_weight("bread", "milk")
        self.assertEqual(weight, 0)

    def test_symmetric_weight(self):
        """Test that weight(A,B) == weight(B,A)."""
        graph = CoPurchaseGraph()
        graph.add_co_purchase("eggs", "bacon")
        graph.add_co_purchase("eggs", "bacon")
        graph.add_co_purchase("eggs", "bacon")
        weight_ab = graph.get_edge_weight("eggs", "bacon")
        weight_ba = graph.get_edge_weight("bacon", "eggs")
        self.assertEqual(weight_ab, weight_ba)
        self.assertEqual(weight_ab, 3)

if __name__ == '__main__':
    unittest.main()