import networkx as nx
import openGraphMatching.matcher as matcher
from openGraphMatching.utils import convert_graph, check_match_correctness

# User(session, first_name, last_name) :- UserFirstName(@session, first_name), UserLastName(@session, last_name).



# The classic example
# Construct the query graph
q = nx.Graph()
q.add_nodes_from([
    (0, {'feat': 'A'}),
    (1, {'feat': 'B'}),
    (2, {'feat': 'C'}),
    (3, {'feat': 'D'}),
    (4, {'feat': 'E'}),
    # (4, {'feat': 'User:session'}),
    
    # (1, {'feat': 'User:first_name'}),
    # (2, {'feat': 'User:last_name'}),
    
    # (3, {'feat': 'UserFirstName:session'}),
    # (4, {'feat': 'UserFirstName:first_name'}),
    
    # (5, {'feat': 'UserLastName:session'}),
    # (6, {'feat': 'UserLastName:last_name'}),
])
q.add_edges_from([
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 3),
    (3, 4),
])

# Construct the target graph
G = nx.Graph()
G.add_nodes_from([
    (0, {'feat': 'A'}),
    (1, {'feat': 'C'}),
    (2, {'feat': 'B'}),
    (3, {'feat': 'C'}),
    (4, {'feat': 'B'}),
    (5, {'feat': 'C'}),
    (6, {'feat': 'B'}),
    (7, {'feat': 'C'}),
    (8, {'feat': 'D'}),
    (9, {'feat': 'D'}),
    (10, {'feat': 'D'}),
    (11, {'feat': 'D'}),
    (12, {'feat': 'D'}),
    (13, {'feat': 'C'}),
    (14, {'feat': 'D'}),
    (15, {'feat': 'E'}),
])
G.add_edges_from([
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (0, 5),
    (0, 6),
    (0, 7),
    (1, 2),
    (1, 8),
    (2, 9),
    (2, 10),
    (3, 4),
    (3, 10),
    (4, 5),
    (4, 10),
    (4, 11),
    (4, 12),
    (5, 12),
    (6, 12),
    (6, 13),
    (7, 14),
    (9, 10),
    (14, 15),
])

print(q.nodes)
print(q.edges)
m = matcher.CECIMatcher(G)
l = m.is_subgraph_match(q)
for i in l:
    print(i)

