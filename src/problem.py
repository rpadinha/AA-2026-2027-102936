def validate_graph(graph, weights):
    """ Validate graph structure and weights"""

    if set(graph.keys()) != set(weights.keys()):
        return False

    for v in graph:

        if weights[v] <= 0:
            return False
        for u in graph[v]:

            if u not in graph:
                return False

            if u == v:
                return False

            if v not in graph[u]:
                return False
            
    return True

def is_dominating_set(graph, D):
    """ Check whether D is a dominating set. """

    D = set(D)

    if not D.issubset(set(graph.keys())):
        return False

    for v in graph:

        if v in D:
            continue

        if not graph[v].intersection(D):
            return False

    return True

def solution_weight(weights, D):
    """ Calculate total weight of a solution. """

    return sum(weights[v] for v in D)

def evaluate_solution(graph, weights, D):
    """ Evaluate a candidate solution. """

    if not is_dominating_set(graph, D):
        return None

    return solution_weight(weights, D)