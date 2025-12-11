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


    def add_co_purchase(self, item_a, item_b):
        """
        Add or update an undirected edge between item_a and item_b.
        Increases their co-purchase count by 1.

        Args:
            item_a (str): First item name.
            item_b (str): Second item name.
        """
        # Ignore self-loops
        if item_a == item_b:
            return

        # Ensure both items exist as nodes
        self.add_item(item_a)
        self.add_item(item_b)

        # Increment edge weight in both directions (undirected graph)
        if item_b not in self.adj[item_a]:
            self.adj[item_a][item_b] = 0
        self.adj[item_a][item_b] += 1

        if item_a not in self.adj[item_b]:
            self.adj[item_b][item_a] = 0
        self.adj[item_b][item_a] += 1