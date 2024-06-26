import networkx as nx

class ContinuousSubgraphMatcher:
    def __init__(self, graph, subgraph):
        self.graph = graph
        self.subgraph = subgraph
        self.results = []

    def update_graph(self, operation, u=None, v=None):
        if operation == "add_vertex":
            self.graph.add_node(u)
        elif operation == "add_edge":
            self.graph.add_edge(u, v)
        
        self.results = self.find_matches()

    def find_matches(self):
        matcher = nx.algorithms.isomorphism.GraphMatcher(self.graph, self.subgraph)
        matches = []
        for subgraph_mapping in matcher.subgraph_isomorphisms_iter():
            matches.append(subgraph_mapping)
        return matches

    def convert_to_edges_and_vertices(self, match):
        vertices = list(match.values())
        edges = [(match[u], match[v]) for u, v in self.subgraph.edges()]
        return vertices, edges

    def print_matches(self):
        for match in self.results:
            vertices, edges = self.convert_to_edges_and_vertices(match)
            print(f"Match found: vertices = {vertices}, edges = {edges}")

def main():
    # Define the main graph Q
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (1, 3), (1, 4)])
    nx.set_node_attributes(graph, {i: f"v{i}" for i in graph.nodes()}, "label")

    # Define the subgraph Q
    subgraph = nx.Graph()
    subgraph.add_edges_from([(0, 1), (1, 2), (2, 0)])
    nx.set_node_attributes(subgraph, {i: f"u{i}" for i in subgraph.nodes()}, "label")

    matcher = ContinuousSubgraphMatcher(graph, subgraph)
    matcher.print_matches()

    print("Adding a new edge (4, 0)...")
    matcher.update_graph("add_edge", 4, 0)
    matcher.print_matches()

    print("Adding a new vertex and edge (5, 0)...")
    matcher.update_graph("add_vertex", 5)
    matcher.update_graph("add_edge", 5, 0)
    matcher.print_matches()

if __name__ == "__main__":
    main()
