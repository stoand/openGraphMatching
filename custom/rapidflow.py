import networkx as nx
from collections import defaultdict

class RapidFlow:
    def __init__(self, graph):
        self.graph = graph
        self.node_label_index = self.build_node_label_index()
        self.edge_index = self.build_edge_index()

    def build_node_label_index(self):
        label_index = defaultdict(set)
        for node, data in self.graph.nodes(data=True):
            label = data.get('label', None)
            if label is not None:
                label_index[label].add(node)
        return label_index

    def build_edge_index(self):
        edge_index = defaultdict(list)
        for u, v, data in self.graph.edges(data=True):
            label = data.get('label', None)
            if label is not None:
                edge_index[label].append((u, v))
        return edge_index

    def match(self, subgraph):
        sub_node_label_index = self.build_node_label_index_subgraph(subgraph)
        sub_edge_index = self.build_edge_index_subgraph(subgraph)

        initial_candidates = self.find_initial_candidates(sub_node_label_index)
        if not initial_candidates:
            return []

        matches = self.search_subgraph_matches(initial_candidates, subgraph, sub_edge_index)
        return matches

    def build_node_label_index_subgraph(self, subgraph):
        label_index = defaultdict(set)
        for node, data in subgraph.nodes(data=True):
            label = data.get('label', None)
            if label is not None:
                label_index[label].add(node)
        return label_index

    def build_edge_index_subgraph(self, subgraph):
        edge_index = defaultdict(list)
        for u, v, data in subgraph.edges(data=True):
            label = data.get('label', None)
            if label is not None:
                edge_index[label].append((u, v))
        return edge_index

    def find_initial_candidates(self, sub_node_label_index):
        candidates = defaultdict(set)
        for label, sub_nodes in sub_node_label_index.items():
            if label in self.node_label_index:
                graph_nodes = self.node_label_index[label]
                for sub_node in sub_nodes:
                    candidates[sub_node] = graph_nodes.copy()
            else:
                return None
        return candidates

    def search_subgraph_matches(self, initial_candidates, subgraph, sub_edge_index):
        def is_feasible_mapping(mapping):
            for u, v in subgraph.edges():
                if mapping[u] not in self.graph or mapping[v] not in self.graph:
                    return False
                if not self.graph.has_edge(mapping[u], mapping[v]):
                    return False
            return True

        def backtrack(current_mapping, depth):
            if depth == len(subgraph.nodes):
                if is_feasible_mapping(current_mapping):
                    matches.append(current_mapping.copy())
                return

            sub_node = sub_nodes[depth]
            for graph_node in initial_candidates[sub_node]:
                if graph_node not in current_mapping.values():
                    current_mapping[sub_node] = graph_node
                    backtrack(current_mapping, depth + 1)
                    del current_mapping[sub_node]

        sub_nodes = list(subgraph.nodes)
        matches = []
        backtrack({}, 0)
        return matches

def main():
    # Define the main graph
    graph = nx.Graph()
    graph.add_edges_from([
        (0, 1, {'label': 'a'}), (1, 2, {'label': 'b'}),
        (2, 3, {'label': 'a'}), (3, 0, {'label': 'b'}),
        (1, 3, {'label': 'c'}), (1, 4, {'label': 'a'})
    ])
    nx.set_node_attributes(graph, {0: 'x', 1: 'y', 2: 'z', 3: 'x', 4: 'y'}, 'label')

    # Define the subgraph
    subgraph = nx.Graph()
    subgraph.add_edges_from([
        (0, 1, {'label': 'a'}), (1, 2, {'label': 'b'}),
        (2, 0, {'label': 'c'})
    ])
    nx.set_node_attributes(subgraph, {0: 'x', 1: 'y', 2: 'z'}, 'label')

    matcher = RapidFlow(graph)
    matches = matcher.match(subgraph)

    if matches:
        print("Subgraph isomorphisms found:")
        for match in matches:
            print(match)
    else:
        print("No subgraph isomorphisms found")

if __name__ == "__main__":
    main()
