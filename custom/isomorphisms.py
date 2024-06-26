import networkx as nx
from itertools import permutations

def is_isomorphic(graph, subgraph, mapping):
    for u in subgraph.nodes():
        for v in subgraph.neighbors(u):
            if not graph.has_edge(mapping[u], mapping[v]):
                return False
    return True

def find_subgraph_isomorphisms(graph, subgraph):
    subgraph_nodes = list(subgraph.nodes())
    graph_nodes = list(graph.nodes())
    
    if len(subgraph_nodes) > len(graph_nodes):
        return []

    matches = []
    
    for perm in permutations(graph_nodes, len(subgraph_nodes)):
        mapping = {subgraph_nodes[i]: perm[i] for i in range(len(subgraph_nodes))}
        if is_isomorphic(graph, subgraph, mapping):
            matches.append(mapping)
    
    return matches

def main():
    # Define the main graph Q
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (1, 3), (1, 4)])
    
    # Define the subgraph Q
    subgraph = nx.Graph()
    subgraph.add_edges_from([(0, 1), (1, 2), (2, 0)])
    
    matches = find_subgraph_isomorphisms(graph, graph)
    
    if matches:
        print("Subgraph isomorphisms found:")
        for match in matches:
            print(match)
    else:
        print("No subgraph isomorphisms found")

if __name__ == "__main__":
    main()
