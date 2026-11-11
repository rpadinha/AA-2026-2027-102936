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

def is_dominating_set(G : nx.Graph, D) -> bool:
    """ Check whether D is a dominating set. """

    D = set(D)

    # check that all vertices in D belong to G
    if not D.issubset(set(G.nodes())):
        return False

    for v in G.nodes():

        if v in D:
            continue

        if not set(G.neighbors(v)).intersection(D):
            return False

    return True

def solution_weight(G : nx.Graph, D) -> int:
    """ Calculate total weight of a solution. """

    return sum(G.nodes[v]["weight"] for v in D)

def evaluate_solution(G : nx.Graph, D) -> int:
    """ Evaluate a candidate solution. """

    if not is_dominating_set(G, D):
        return None

    return solution_weight(G, D)