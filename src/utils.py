# src/utils.py
import os
import random
import argparse
import networkx as nx
from pathlib import Path
from src.graph_io import save_graph # save_graph from src/graph_io.py

# Dynamically point to the project root
BASE_DIR = Path(__file__).parent.parent
SAVE_DIR_HANDMADE = BASE_DIR / "data" / "graphs" / "handmade"
SAVE_DIR_SYNTHETIC = BASE_DIR / "data" / "graphs" / "synthetic"

N_VALUES = range(17, 41)
M_VALUES = [0.125, 0.250, 0.500, 0.750]

### --------- handmade graphs goes here? ---------- 
HANDMADE_1 = nx.Graph() # 4 verticies, 4 edges graph
HANDMADE_7 = nx.Graph() # 7 verticies, 12 edges graph

HANDMADE_1.add_nodes_from([
    (1, {"weight": 3}),
    (2, {"weight": 2}),
    (3, {"weight": 6}),
    (4, {"weight": 1})
])
HANDMADE_1.add_edges_from([
    (1, 2),
    (2, 3),
    (3, 4),
    (1, 4)
])

HANDMADE_7.add_nodes_from([
    (1, {"weight": 8}),
    (2, {"weight": 3}),
    (3, {"weight": 4}),
    (4, {"weight": 2}),
    (5, {"weight": 5}),
    (6, {"weight": 1}),
    (7, {"weight": 6})

])
HANDMADE_7.add_edges_from([
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 6),
    (1, 7),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 2)
])

HANDMADE_GRAPHS = {
    "graph_4_4" : HANDMADE_1,
    "graph_7_12" : HANDMADE_7
}

def generate_handmade_graphs(handmadeGraphs) -> list[str]:
    """ Save handmade graphs in Graphml format. """
    os.makedirs(SAVE_DIR_HANDMADE, exist_ok=True)
    paths = []

    for name, G in handmadeGraphs.items():
        filename = f"{name}.graphml"
        path = SAVE_DIR_HANDMADE / filename

        save_graph(G, str(path))
        paths.append(str(path))

    return paths

def generate_random_graph(n, m, seed) -> str:
    """Generate a random weighted graph and save it in GraphML format."""
    os.makedirs(SAVE_DIR_SYNTHETIC, exist_ok=True)
    random.seed(seed)

    G = nx.Graph()
    pos = {}

    while G.number_of_nodes() < n:
        x, y = random.randint(1, 500), random.randint(1, 500)
        if (x, y) not in pos.values():
            new_node = G.number_of_nodes()
            weight = random.randint(1, 100)
            G.add_node(new_node, weight=weight)
            pos[new_node] = (x, y)

    max_edges = (n * (n - 1)) // 2
    num_edges = int(max_edges * m)

    while G.number_of_edges() < num_edges:
        u, v = random.sample(list(G.nodes()), 2)
        if not G.has_edge(u, v):
            G.add_edge(u, v)

    filename = f"graph_{n}_{int(m*100)}.graphml"
    path = os.path.join(SAVE_DIR_SYNTHETIC, filename)
    save_graph(G, path)
    return path

# AI-Assisted: Generated boilerplate CLI parser using argparse.
# Tool: Gemini | Verified by: Student #102936
if __name__ == "__main__":
    # This fulfills the requirement to pass the seed via CLI
    parser = argparse.ArgumentParser(description="Generate spatial graphs for P1/P2.")
    parser.add_argument("--seed", 
                        type=int, 
                        required=True, 
                        help="Student ID for random seed") # seed arg
    parser.add_argument("--handmade",
                        action="store_true", # help from gemini again because argparse treats type=bool simply as a check of whether the passed string is empty
                        help="Flag to generate handmade graphs") # generate handmade graphs?
    
    args = parser.parse_args()
    student_seed = args.seed
    gen_handmade = args.handmade
    
    print(f" {'~' * 40} Generating graphs for Seed: {student_seed} {'~' * 40} ")
    total_graphs = len(N_VALUES) * len(M_VALUES)
    count = 0
    
    for n in N_VALUES:
        for m in M_VALUES:
            count += 1
            # Creating a unique, reproducible seed per graph based on your student ID
            unique_seed = int(f"{student_seed}{n}{int(m*100)}")
            path = generate_random_graph(n, m, unique_seed)
            print(f"({count}/{total_graphs}) Saved: {path}")

    if gen_handmade:
        print(f" {'~' * 40} Generating handmade graphs {'~' * 40} ")
        handmade_paths = generate_handmade_graphs(HANDMADE_GRAPHS)
        for path in handmade_paths:
            print(f"Handmade graph saved: {path}")

    print(f" {'~' * 40} Graphs generated {'~' * 40} ")