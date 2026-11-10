import os
import random
import networkx as nx

STUDENT_NUMBER = 102936                                             # Student Number
N = range(17, 41)                                                   # Number of verticies (goes from 17 to 41)
M = [0.125, 0.250, 0.500, 0.750]                                    # Density of edges (12.5%, 25%, 50%, 75%)
# BASE_DIR = os.path. idk how to do this correctly
SAVE_DIR = "data/graphs/synthetic"

def generate_random_graph(n , m, seed):
    """ Generates a random graph and saves it in a .gml file"""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    random.seed(seed)

    G = nx.Graph()
    pos = {}

    # node generation
    while G.number_of_nodes() < n:
        x, y = random.randint(1, 500), random.randint(1, 500)   # generates a random pos in the (0, 0) to (500, 500) space
        if (x, y) not in pos.values():
            new_node = G.number_of_nodes()
            G.add_node(new_node)
            pos[new_node] = (x, y)

    max_edges = (n * (n - 1)) // 2
    num_edges = int(max_edges * m)

    # edge generation
    while G.number_of_edges() < num_edges:
        u, v = random.sample(list(G.nodes()), 2) # random sample why? saw this in a post stack overflow
        if not G.has_edge(u, v):
            G.add_edge(u, v)

    filename = f"graph_{n}_{int(m*100)}.gml"
    path = os.path.join(SAVE_DIR, filename)
    nx.write_gml(G, path)
    return path

if __name__ == "__main__":
    print(" ~~~~~~~~~~~~ Generating graphs ~~~~~~~~~~~~ ")
    total_graphs = len(N) * len(M)
    count = 0
    for n in N:
        for m in M:
            count += 1
            unique_seed = f"{STUDENT_NUMBER}"
            path = generate_random_graph(n, m, unique_seed)
            print(f"({count}/{total_graphs}) Generated graph and saved in: {path}")

    print(" ~~~~~~~~~~~~ Graphs generated ~~~~~~~~~~~~ ")