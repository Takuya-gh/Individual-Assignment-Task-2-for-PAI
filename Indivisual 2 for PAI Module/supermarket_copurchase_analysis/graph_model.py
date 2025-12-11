# Graph model for co-purchase analysis
# Graph model for co-purchase analysis


class CoPurchaseGraph:
    """
    Undirected weighted graph of item co-purchases.

    Internal representation:
        self.adj: dict[str, dict[str, int]]
        Example:
        {
          "bread": {"milk": 10, "butter": 5},
          "milk": {"bread": 10, "cereal": 3},
        }
    """

    def __init__(self):
        """Initialize an empty co-purchase graph."""
        self.adj = {}


    def add_item(self, item):
        """
        Ensure the item exists as a node in the graph.

        Args:
            item (str): The item name to add as a node.
        """
        if item not in self.adj:
            self.adj[item] = {}