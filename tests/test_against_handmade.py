import pytest
from pathlib import Path
from src.graph_io import load_graph
from src.exhaustive import exhaustive_search
from src.greedy import greedy_basic_search, greedy_ratio_search

# Dynamically locate the handmade graphs folder
BASE_DIR = Path(__file__).parent.parent
HANDMADE_DIR = BASE_DIR / "data" / "graphs" / "handmade"

@pytest.mark.parametrize("filename, expected_cost, expected_set", [
    ("graph_4_4.graphml", 3, {2, 4}),
    ("graph_7_12.graphml", 5, {3, 6}),
    ("graph_12_15.graphml", 16, {4, 5, 7, 9, 10})
])

def test_exhaustive_handmade(filename, expected_cost, expected_set):

    # Load graph from GraphML
    filepath = HANDMADE_DIR / filename
    G = load_graph(str(filepath))

    # Run exhaustive search
    result = exhaustive_search(G)

    # Check expected results
    assert result["solution_quality"] == expected_cost
    assert set(result["dominating_set"]) == expected_set


@pytest.mark.parametrize("filename, expected_cost, expected_set", [
    ("graph_4_4.graphml", 5, {1, 2}),
    ("graph_7_12.graphml", 8, {1}),
    ("graph_12_15.graphml", 21, {1, 3, 7, 9})
])
def test_greedy_handmade(filename, expected_cost, expected_set):

    # Load graph from GraphML
    filepath = HANDMADE_DIR / filename
    G = load_graph(str(filepath))

    # Run greedy search
    result = greedy_basic_search(G)

    # Check expected results
    assert result["solution_quality"] == expected_cost
    assert set(result["dominating_set"]) == expected_set