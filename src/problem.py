import networkx as nx

def validate_graph(G : nx.Graph) -> bool:
    """ Validate graph structure and weights"""

    if not isinstance(G, nx.Graph):
        return False

    # check all nodes have positive weight
    for v in G.nodes():

        if "weight" not in G.nodes()[v]:
            return False
        
        if G.nodes[v]["weight"] <= 0:
            return False

        # check for self-loops
        if G.has_edge(v, v):
            return False
        
    return True

def is_dominating_set(G : nx.Graph, D : set) -> tuple[bool, int]:
    """ Check whether D is a dominating set. Returns (is_valid, basic_ops)"""
    ops = 0

    # check that all vertices in D belong to G
    if not D.issubset(set(G.nodes())):
        return False, ops

    for v in G.nodes():
        ops += 1
        if v in D:
            continue

        ops += 1 # counting the neighborhood intersection check
        if not set(G.neighbors(v)).intersection(D):
            return False, ops

    return True, ops

def solution_weight(G : nx.Graph, D : set) -> tuple[int, int]:
    """ Calculate total weight of a solution. Returns (cost, basic_ops)"""
    ops = 0
    cost = 0
    for v in D:
        ops += 1
        cost += G.nodes[v]["weight"]

    return cost, ops 