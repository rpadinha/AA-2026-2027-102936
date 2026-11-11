# src/graph_io.py
import networkx as nx
import os

# AI-Assisted: Generated boilerplate for NetworkX I/O wrappers.
# Tool: Gemini | Verified by: Student #102936
def save_graph(G: nx.Graph, filepath: str) -> None:
    """Saves a NetworkX graph to the specified filepath based on extension."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == '.graphml':
        nx.write_graphml(G, filepath)
    elif ext == '.adj':
        nx.write_adjlist(G, filepath)
    else:
        raise ValueError(f"Unsupported file extension for saving: {ext}")

def load_graph(filepath: str) -> nx.Graph:
    """Loads a NetworkX graph from the specified filepath based on extension."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Graph file not found: {filepath}")
        
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == '.graphml':
        # GraphML nodes are sometimes read as strings, converting back to int if needed
        G = nx.read_graphml(filepath)
        # Convert node labels back to integers if they are digits
        return nx.relabel_nodes(G, lambda x: int(x) if str(x).isdigit() else x)
    elif ext == '.adj':
        return nx.read_adjlist(filepath)
    else:
        raise ValueError(f"Unsupported file extension for loading: {ext}")