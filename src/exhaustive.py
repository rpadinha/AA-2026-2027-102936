import networkx as nx
from src.problem import validate_graph, is_dominating_set, solution_weight

def exhaustive_search(G : nx.Graph) -> dict:
    """ 
        Exhaustive search for a dominating set
        Returns a dictionary with 4 values: 
        dominating_set      -> Optimal set found
        solution_quality    -> The total cost of the optimal set found
        tested_configs      -> Number of states evaluated
        basic_ops           -> Counter for number of operations executed
    """

    best_set = None
    min_cost = float('inf')
    tested_configs = 0
    basic_ops = 0

    # uses the src/problem.py helper functions
    if not validate_graph(G): # this doesnt account into basic_ops i believe
        raise ValueError("Invalid graph")
    
    # number of nodes of graph
    nodes = list(G.nodes())
    n = len(nodes)

    # Generate all possible subsets using binary representation (2^n)
    max_sets = 2 ** n

    for mask in range(1 , max_sets):
        tested_configs += 1

        D = set()

        # binary representation into a subset
        for i in range(n):
            basic_ops += 1

            if mask & (1 << i): # left shift operator so (example for mask = (5) binary mask = 101: i = 0 ; 1 << 0 ; 001 << 000 ; 001 ; 101 & 001 ; 001)
                D.add(nodes[i])

        # check if D is a dominating set, capturing both the boolean and the number of operations to check if it is a dominating set
        is_dominating, dominating_ops = is_dominating_set(G, D)
        basic_ops += dominating_ops

        if is_dominating:

            # captures the cost of the solution and the operations it took to calculate the solution
            cost, weight_ops = solution_weight(G, D)
            basic_ops += weight_ops

            if cost < min_cost: # if the cost is better we store the cost and the set
                min_cost = cost
                best_set = D

    return {
        "dominating_set" : best_set,
        "solution_quality" : min_cost,
        "tested_configs" : tested_configs,
        "basic_ops" : basic_ops
    }