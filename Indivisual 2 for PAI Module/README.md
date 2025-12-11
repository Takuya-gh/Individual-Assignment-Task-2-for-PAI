# Supermarket Co-Purchase Analysis System

A Python-based system for analyzing co-purchase patterns in supermarket transaction data using graph data structures and algorithms. This project implements a command-line interface (CLI) tool that helps identify which products are frequently bought together, enabling better product placement and marketing strategies.

## Project Overview

This system analyzes supermarket transaction data to discover co-purchase relationships between products. It uses a graph-based approach where:
- **Nodes** represent individual products
- **Edges** represent co-purchase relationships
- **Edge weights** represent the frequency of co-purchases

The project was developed using **Test-Driven Development (TDD)** methodology, ensuring robust and well-tested code.

## Features

The system provides three main analytical capabilities:

1. **Co-purchase Query**: Find which items are most frequently bought together with a specific product
2. **Top Bundles Discovery**: Identify the most common product bundles (pairs of items)
3. **Co-purchase Verification**: Check if two specific items are frequently co-purchased above a threshold

## Data Structure

### Graph Model

The core data structure is the `CoPurchaseGraph` class, which implements an undirected weighted graph using an adjacency list representation:

```python
{
    "item_a": {
        "item_b": weight,
        "item_c": weight
    },
    "item_b": {
        "item_a": weight
    }
}
```

**Key Methods:**
- `add_vertex(item)`: Add a product to the graph
- `add_edge(item_a, item_b, weight)`: Add/update a co-purchase relationship
- `get_edge_weight(item_a, item_b)`: Get co-purchase frequency between two items
- `get_neighbors(item)`: Get all items co-purchased with a given item
- `get_all_edges()`: Retrieve all co-purchase relationships
- `has_vertex(item)`: Check if an item exists in the graph

## Algorithms Implemented

### 1. Graph Construction
**Function**: `build_graph_from_transactions(transactions)`
- Builds the co-purchase graph from transaction data
- Groups items by transaction ID
- Creates edges between all items in the same transaction
- Time Complexity: O(n × m²) where n is number of transactions and m is average items per transaction

### 2. Co-purchase Query
**Function**: `get_co_purchases_for_item(graph, item, min_count)`
- Finds all items co-purchased with a specific item
- Filters by minimum co-purchase frequency
- Returns sorted list of (item, count) tuples
- Time Complexity: O(k log k) where k is the number of neighbors

### 3. Top Bundles Discovery
**Function**: `get_top_n_bundles(graph, n)`
- Identifies the N most common product pairs
- Returns sorted list of (item_a, item_b, count) tuples
- Time Complexity: O(e log e) where e is the number of edges

### 4. Co-purchase Verification
**Function**: `are_often_copurchased(graph, item_a, item_b, threshold)`
- Checks if two items are frequently co-purchased
- Compares co-purchase count against a threshold
- Returns boolean result
- Time Complexity: O(1)

### 5. BFS Related Items
**Function**: `bfs_related_items(graph, start_item, max_depth)`
- Performs Breadth-First Search to find related items
- Explores co-purchase relationships up to a specified depth
- Returns items reachable within max_depth steps
- Time Complexity: O(V + E) where V is vertices and E is edges

## Project Structure

```
supermarket_copurchase_analysis/
├── __init__.py
├── graph_model.py          # CoPurchaseGraph class
├── data_loader.py          # CSV transaction loader
├── algorithms.py           # Analysis algorithms
├── cli.py                  # Command-line interface
└── tests/
    ├── __init__.py
    ├── test_graph_model.py
    ├── test_data_loader.py
    ├── test_algorithms.py
    ├── test_cli.py
    └── sample_data.csv     # Test dataset

data/
└── Supermarket_dataset_PAI.csv  # Real supermarket dataset
```

## Installation

This project requires Python 3.6 or higher. No external dependencies are required - it uses only Python standard library modules.

Clone the repository and navigate to the project directory:

```bash
cd "Indivisual 2 for PAI Module"
```

## Usage

### Command-Line Interface

The system provides a CLI with four commands: `load`, `query`, `bundles`, and `check`.

#### 1. Load Transactions (Validation)

Validate that a CSV file can be loaded successfully:

```bash
python -m supermarket_copurchase_analysis.cli load data/Supermarket_dataset_PAI.csv
```

**Output:**
```
Successfully loaded 14963 transactions
Graph contains 167 unique items
Graph contains 6260 co-purchase relationships
```

#### 2. Query Co-purchases for an Item

Find which items are most frequently bought together with a specific product:

```bash
python -m supermarket_copurchase_analysis.cli query data/Supermarket_dataset_PAI.csv "whole milk"
```

**Options:**
- `--min-count N`: Only show items co-purchased at least N times (default: 1)

**Example with minimum count:**
```bash
python -m supermarket_copurchase_analysis.cli query data/Supermarket_dataset_PAI.csv "whole milk" --min-count 50
```

**Sample Output:**
```
Co-purchases for 'whole milk' (min_count=50):
  other vegetables: 222
  rolls/buns: 209
  soda: 174
  yogurt: 167
  sausage: 134
  tropical fruit: 123
  root vegetables: 113
  ...
```

#### 3. Find Top Product Bundles

Identify the most common product bundles (pairs):

```bash
python -m supermarket_copurchase_analysis.cli bundles data/Supermarket_dataset_PAI.csv 5
```

**Sample Output:**
```
Top 5 bundles:
  whole milk + other vegetables: 222
  rolls/buns + whole milk: 209
  whole milk + soda: 174
  whole milk + yogurt: 167
  rolls/buns + other vegetables: 158
```

#### 4. Check if Two Items Are Often Co-purchased

Verify whether two specific items are frequently bought together:

```bash
python -m supermarket_copurchase_analysis.cli check data/Supermarket_dataset_PAI.csv "whole milk" "other vegetables" --threshold 100
```

**Options:**
- `--threshold N`: Minimum co-purchase count to be considered "often" (default: 1)

**Sample Output:**
```
Yes, 'whole milk' and 'other vegetables' are often co-purchased (count: 222, threshold: 100)
```

**Example with high threshold (negative result):**
```bash
python -m supermarket_copurchase_analysis.cli check data/Supermarket_dataset_PAI.csv "whole milk" "other vegetables" --threshold 300
```

**Output:**
```
No, 'whole milk' and 'other vegetables' are not often co-purchased (count: 222, threshold: 300)
```

## Running Tests

The project includes comprehensive unit tests for all components.

### Run All Tests

```bash
python -m unittest discover -s supermarket_copurchase_analysis/tests -p "test_*.py" -v
```

### Run Specific Test Modules

**Graph Model Tests:**
```bash
python -m unittest supermarket_copurchase_analysis.tests.test_graph_model -v
```

**Data Loader Tests:**
```bash
python -m unittest supermarket_copurchase_analysis.tests.test_data_loader -v
```

**Algorithms Tests:**
```bash
python -m unittest supermarket_copurchase_analysis.tests.test_algorithms -v
```

**CLI Tests:**
```bash
python -m unittest supermarket_copurchase_analysis.tests.test_cli -v
```

### Expected Test Output

All tests should pass with output similar to:

```
test_add_edge (supermarket_copurchase_analysis.tests.test_graph_model.TestCoPurchaseGraph) ... ok
test_add_vertex (supermarket_copurchase_analysis.tests.test_graph_model.TestCoPurchaseGraph) ... ok
...
----------------------------------------------------------------------
Ran 30 tests in 0.156s

OK
```

## Dataset Format

The CSV file should have the following format:

```csv
Member_number,Date,itemDescription
1000,2015-01-01,whole milk
1000,2015-01-01,other vegetables
1001,2015-01-01,rolls/buns
1001,2015-01-01,whole milk
```

**Required columns:**
- `Member_number`: Transaction identifier
- `Date`: Transaction date
- `itemDescription`: Product name

Transactions are grouped by `Member_number` - all items with the same member number are considered to be purchased together.

## Development Methodology

This project was developed using **Test-Driven Development (TDD)**:

1. **Write tests first** - Define expected behavior through unit tests
2. **Run tests and see them fail** - Verify tests are properly detecting missing functionality
3. **Implement minimum code** - Write just enough code to make tests pass
4. **Refactor** - Improve code while keeping tests green
5. **Repeat** - Continue cycle for each new feature

All commits follow the TDD cycle, ensuring high code quality and test coverage.

## Example Use Cases

### 1. Product Placement Strategy

Find what customers buy with bread to optimize shelf placement:

```bash
python -m supermarket_copurchase_analysis.cli query data/Supermarket_dataset_PAI.csv "brown bread" --min-count 10
```

### 2. Bundle Promotion Ideas

Discover the most popular product combinations for promotional bundles:

```bash
python -m supermarket_copurchase_analysis.cli bundles data/Supermarket_dataset_PAI.csv 10
```

### 3. Cross-Selling Validation

Verify if a proposed product pairing makes sense based on historical data:

```bash
python -m supermarket_copurchase_analysis.cli check data/Supermarket_dataset_PAI.csv "yogurt" "fruit" --threshold 20
```

## Key Insights from Real Dataset

Based on analysis of the provided supermarket dataset:

**Top 3 Most Common Product Bundles:**
1. Whole milk + Other vegetables: 222 co-purchases
2. Rolls/buns + Whole milk: 209 co-purchases
3. Whole milk + Soda: 174 co-purchases

This indicates that **whole milk** is a central product in the store, frequently purchased alongside many other items. Strategic placement of whole milk can drive sales of complementary products.

## Author

Developed as part of Individual Assignment Task 2 for the Programming for Artificial Intelligence module.

## License

This project is submitted as academic coursework.
