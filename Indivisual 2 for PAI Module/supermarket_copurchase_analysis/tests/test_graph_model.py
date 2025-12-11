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


if __name__ == '__main__':
    unittest.main()