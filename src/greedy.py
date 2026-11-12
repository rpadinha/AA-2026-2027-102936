import networkx as nx
from src.problem import validate_graph, is_dominating_set, solution_weight

def greedy_basic_search(G: nx.Graph) -> dict:
    """ 
    Basic greedy search for a dominating set:
    This greedy algorithm picks the most dominating vertex meaning the one with the most neighbors
    Returns a dictionary with 4 values: 
    dominating_set      -> Optimal set found
    solution_quality    -> The total cost of the optimal set found
    tested_configs      -> Number of states evaluated
    basic_ops           -> Counter for number of operations executed
    """
    
    D = set()
    dominated = set()
    tested_configs = 0
    basic_ops = 0

    if not validate_graph(G):
        raise ValueError("Invalid Graph")

    # cast to list to avoid iteration bugs
    nodes = list(G.nodes())

    # continue until every vertex is dominated
    while len(dominated) < len(nodes):
        best_vertex = None
        best_dominated = set()

        for v in nodes:
            tested_configs += 1
            basic_ops += 1

            if v in D:
                continue

            # unpack the iterator to a list once
            neighbors = list(G.neighbors(v))
            newly_dominated = {v} | set(neighbors)
            basic_ops += len(neighbors)

            # only count vertices that aren't already dominated
            newly_dominated = newly_dominated - dominated
            basic_ops += 1

            # skip vertices that don't dominate anything new
            if not newly_dominated:
                continue

            basic_ops += 1

            # store the vertex  like algorithm 33 compares the span w(v) = |W(v)| . chapter 7 algorithm 33
            if len(newly_dominated) > len(best_dominated):
                best_vertex = v
                best_dominated = newly_dominated

        if best_vertex is None:
            break

        D.add(best_vertex)
        dominated.update(best_dominated)

    is_dominating, dominating_ops = is_dominating_set(G, D)
    basic_ops += dominating_ops
    
    cost, weight_ops = solution_weight(G, D)
    basic_ops += weight_ops
    
    if not is_dominating:
        raise ValueError("Greedy algorithm failed to find a valid dominating set!")
    
    return {
        "dominating_set": D,
        "solution_quality": cost,
        "tested_configs": tested_configs,
        "basic_ops": basic_ops
    }

def greedy_ratio_search(G: nx.Graph) -> dict:
    """ 
    Ratio greedy search for a dominating set:
    This greedy algorithm picks the most dominating vertex based on the cost and the number of new neighbors by cost/neighbors = ratio 
    Returns a dictionary with 4 values: 
    dominating_set      -> Optimal set found
    solution_quality    -> The total cost of the optimal set found
    tested_configs      -> Number of states evaluated
    basic_ops           -> Counter for number of operations executed
    """
    
    D = set()
    dominated = set()
    tested_configs = 0
    basic_ops = 0

    if not validate_graph(G):
        raise ValueError("Invalid Graph")

    # cast to list to avoid iteration bugs
    nodes = list(G.nodes())

    # continue until every vertex is dominated
    while len(dominated) < len(nodes):
        best_vertex = None
        best_ratio = float('inf')
        best_dominated = set()

        for v in nodes:
            tested_configs += 1
            basic_ops += 1

            if v in D:
                continue

            # unpack the iterator to a list once
            neighbors = list(G.neighbors(v))
            newly_dominated = {v} | set(neighbors)
            basic_ops += len(neighbors)

            # only count vertices that aren't already dominated
            newly_dominated = newly_dominated - dominated
            basic_ops += 1

            # skip vertices that don't dominate anything new
            if not newly_dominated:
                continue

            # ratio calculation mentioned in line 133, 134
            weight = G.nodes[v]["weight"]
            ratio = weight / len(newly_dominated)
            basic_ops += 1

            # store the vertex  kinda like algorithm 33 compares the ratio of cost / number of nodes discovered
            #  w(v) = weight(v) / |W(v)| . chapter 7 algorithm 33 with a twist
            if ratio < best_ratio:
                best_ratio = ratio
                best_vertex = v
                best_dominated = newly_dominated

        if best_vertex is None:
            break

        D.add(best_vertex)
        dominated.update(best_dominated)

    is_dominating, dominating_ops = is_dominating_set(G, D)
    basic_ops += dominating_ops

    cost, weight_ops = solution_weight(G, D)
    basic_ops += weight_ops

    if not is_dominating:
        raise ValueError("Greedy algorithm failed to find a valid dominating set!")
    
    return {
        "dominating_set": D,
        "solution_quality": cost,
        "tested_configs": tested_configs,
        "basic_ops": basic_ops
    }