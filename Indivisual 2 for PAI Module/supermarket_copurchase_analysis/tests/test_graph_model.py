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


if __name__ == '__main__':
    unittest.main()