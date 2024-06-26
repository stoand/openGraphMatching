from itertools import permutations

def edges_to_adj_list(edges, num_nodes):
    adj_list = [[] for _ in range(num_nodes)]
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    return adj_list

def is_automorphism(edges, adj_list, perm):
    for u, v in edges:
        if perm[v] not in adj_list[perm[u]] or perm[u] not in adj_list[perm[v]]:
            return False
    return True

def find_automorphisms(edges, num_nodes):
    nodes = list(range(num_nodes))
    adj_list = edges_to_adj_list(edges, num_nodes)
    automorphisms = []

    
    for perm in permutations(nodes):
        if is_automorphism(edges, adj_list, perm):
            automorphisms.append(perm)
    
    return automorphisms

def main():
    # Define the graph as a list of edges
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (1, 3), (1, 4)]
    num_nodes = 5

    automorphisms = find_automorphisms(edges, num_nodes)
    
    if automorphisms:
        print("Automorphisms found:")
        for auto in automorphisms:
            print(auto)
    else:
        print("No automorphisms found")

if __name__ == "__main__":
    main()
