import networkx as nx
import openGraphMatching.matcher as matcher
from openGraphMatching.utils import convert_graph, check_match_correctness

# CommentForm(session, post_id, id, body) :-
#     CommentId(@session: Session, @post_id: Id, @id: Id),
#     CommentBody(@session: Session, @post_id: Id, body: String).

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

# The classic example
# Construct the query graph
q = nx.Graph()
q.add_nodes_from([
    (0, {'feat': 'CommentId'}),
    (1, {'feat': 'CommentBody'}),
    (2, {'feat': 'CommentBody:Body'}),
])

q.add_edges_from([
    (0, 1),
    (1, 2),
])

graph_nodes = [
    (h('CommentId:session0:post0:id0'), {'feat': 'CommentId'}),
    (h('CommentBody:session0:post0'), {'feat': 'CommentBody'}),
    (h('CommentBody:session0:post0:bodyval0'), {'feat': 'CommentBody:Body'}),
]

graph_nodes.sort()

# Construct the target graph
G = nx.Graph()
G.add_nodes_from(graph_nodes)
G.add_edges_from([
    (h('CommentId:session0:post0:id0'), h('CommentBody:session0:post0')),
    (h('CommentBody:session0:post0'), h('CommentBody:session0:post0:bodyval0')),
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
