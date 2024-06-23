import networkx as nx
import openGraphMatching.matcher as matcher
from openGraphMatching.utils import convert_graph, check_match_correctness

# User(session, first_name, last_name) :- UserFirstName(@session, first_name), UserLastName(@session, last_name).



# The classic example
# Construct the query graph
q = nx.Graph()
q.add_nodes_from([
    (10, {'feat': 'User:session'}),
    
    (13, {'feat': 'UserFirstName:session'}),
    (14, {'feat': 'UserFirstName:first_name'}),
    
    (15, {'feat': 'UserLastName:session'}),
    (16, {'feat': 'UserLastName:last_name'}),
])

q.add_edges_from([
    (13, 14),

    (15, 16),

    (10, 13),
    (10, 15),
])

hashes = []

def h(val):
   hashed_val = abs(hash(val))
   hashes.append({"h": hashed_val, "v": val})
   return hashed_val

def rev_h(h):
    for i in hashes:
        if i["h"] == h:
            return i["v"]
    return "<missing_hash>"

graph_nodes = [
    (0, {'feat': 'User:session', 'value': 'none'}),
    
    (h("session1"), {'feat': 'UserFirstName:session', 'value': 'session1'}),
    (h("Andy"), {'feat': 'UserFirstName:first_name', 'value': 'Andy'}),
    
    (5, {'feat': 'UserLastName:session', 'value': 'session0'}),
    (6, {'feat': 'UserLastName:last_name', 'value': 'Zero'}),

    (7, {'feat': 'UserFirstName:session', 'value': 'session0'}),
    (8, {'feat': 'UserFirstName:first_name', 'value': 'Bob'}),
]

graph_nodes.sort()

# Construct the target graph
G = nx.Graph()
G.add_nodes_from(graph_nodes)
G.add_edges_from([
    (h("session1"), h("Andy")),

    (5, 6),

    (7, 8),

    (0, h("session1")),
    (0, 5),
    (0, 7),
])

print(q.nodes)
print(q.edges)

m = matcher.CECIMatcher(G)
l = m.is_subgraph_match(q)

print(l[1])

print ("\n")
for found in l[1]:
    for key, value in found.items():
        v = 0
        for node in graph_nodes:
            if node[0] == value:
                v = node[1]['value']
        print(str(key) + '(' + rev_h(value) + ')' + ' = ' + str(v))
    print ("\n")
