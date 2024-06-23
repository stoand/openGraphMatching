import networkx as nx
import openGraphMatching.matcher as matcher
from openGraphMatching.utils import convert_graph, check_match_correctness

# User(session, first_name, last_name) :- UserFirstName(@session, first_name), UserLastName(@session, last_name).



# The classic example
# Construct the query graph
q = nx.Graph()
q.add_nodes_from([
    # User:session
    (10, {'feat': 'session'}),
    # UserFirstName:session
    (13, {'feat': 'first_name'}),
    # UsersLastName:session
    (15, {'feat': 'last_name'}),
    # # User:session
    # (10, {'feat': 'value'}),
    # # User:first_name
    # (11, {'feat': 'value'}),
    # # User:last_name
    # (12, {'feat': 'value'}),
    # # UserFirstName:session
    # (13, {'feat': 'value'}),
    # # UserFirstName:first_name
    # (14, {'feat': 'value'}),
    # # UsersLastName:session
    # (15, {'feat': 'value'}),
    # # UsersLastName:last_name
    # (16, {'feat': 'value'}),
])

q.add_edges_from([
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
    # (0, {'feat': 'User:session', 'value': 'none'}),
    
    # (h("session1"), {'feat': 'UserFirstName:session', 'value': 'session1'}),
    # (h("Andy"), {'feat': 'UserFirstName:first_name', 'value': 'Andy'}),
    
    # (5, {'feat': 'UserLastName:session', 'value': 'session0'}),
    # (6, {'feat': 'UserLastName:last_name', 'value': 'Zero'}),

    # (7, {'feat': 'UserFirstName:session', 'value': 'session0'}),
    # (8, {'feat': 'UserFirstName:first_name', 'value': 'Bob'}),
    # 
    (h('session3'), {'feat': 'session'}),
    (h('session4'), {'feat': 'session'}),
    (h('Andy'), {'feat': 'first_name'}),
    (h('Bob'), {'feat': 'first_name'}),
    (h('Zero'), {'feat': 'last_name'}),
]

graph_nodes.sort()

# Construct the target graph
G = nx.Graph()
G.add_nodes_from(graph_nodes)
G.add_edges_from([
    (h("session3"), h("Andy")),
    (h("session3"), h("Zero")),
    
    (h("session4"), h("Bob")),
    (h("session4"), h("Zero")),
])

print(q.nodes)
print(q.edges)

m = matcher.CECIMatcher(G)
l = m.is_subgraph_match(q)

print(l[1])

print ("\n")
for found in l[1]:
    for key, value in found.items():
        v = ''
        for node in graph_nodes:
            if node[0] == value:
                v = node[1]['feat']
        print(str(key) + ' - (' + v + ') = ' + rev_h(value))
    print ("\n")
