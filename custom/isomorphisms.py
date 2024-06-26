class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adj_list = [[] for _ in range(num_vertices)]

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

def is_valid_mapping(graph, subgraph, mapping):
    for i in range(len(subgraph.adj_list)):
        for j in subgraph.adj_list[i]:
            if mapping[j] not in graph.adj_list[mapping[i]]:
                return False
    return True

def find_subgraph_isomorphisms(graph, subgraph, mapping, used, depth, results):
    if depth == len(subgraph.adj_list):
        if is_valid_mapping(graph, subgraph, mapping):
            results.append(mapping[:])
        return

    for v in range(graph.num_vertices):
        if not used[v]:
            used[v] = True
            mapping[depth] = v
            find_subgraph_isomorphisms(graph, subgraph, mapping, used, depth + 1, results)
            used[v] = False

def convert_to_edges_and_vertices(mapping, subgraph):
    vertices = mapping
    edges = []
    for u in range(len(subgraph.adj_list)):
        for v in subgraph.adj_list[u]:
            if u < v:  # Avoid duplicate edges
                edges.append((mapping[u], mapping[v]))
    return vertices, edges

def main():
    # Define the main graph Q
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 0)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    
    print(graph.adj_list)

    # Define the subgraph Q
    subgraph = Graph(3)
    subgraph.add_edge(0, 1)
    subgraph.add_edge(1, 2)
    subgraph.add_edge(2, 0)

    mapping = [-1] * graph.num_vertices
    used = [False] * graph.num_vertices
    results = []

    find_subgraph_isomorphisms(graph, graph, mapping, used, 0, results)

    for result in results:
        vertices, edges = convert_to_edges_and_vertices(result, graph)
        print(f"Match found: vertices = {vertices}, edges = {edges}")

if __name__ == "__main__":
    main()
