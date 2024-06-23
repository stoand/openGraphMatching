import networkx as nx
import openGraphMatching.matcher as matcher
from openGraphMatching.utils import convert_graph, check_match_correctness

# CommentForm(session, post_id, id, body) :-
#     CommentId(@session: Session, @post_id: Id, @id: Id),
#     CommentBody(@session: Session, @post_id: Id, body: String), 

# User(session, first_name, last_name) :-
# 	UserFirstName(@session, first_name),
# 	UserLastName(@session, last_name).

# The classic example
# Construct the query graph
q = nx.Graph()
q.add_nodes_from([
    (10, {'feat': 'primary_key'}),
    
    # (11, {'feat': 'comment_id'}),
    # (12, {'feat': 'comment_body'}),

    (13, {'feat': 'first_name'}),
    (14, {'feat': 'last_name'}),
])

q.add_edges_from([
    # (10, 11),
    # (10, 12),
    
    (10, 13),
    (10, 14),
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
    # (h('primary0'), {'feat': 'primary_key'}),
    # # (h('post0'), {'feat': 'post_id'}),
    # (h('comment_id0'), {'feat': 'comment_id'}),
    # (h('comment_body0'), {'feat': 'comment_body'}),
    
    (h('primary1'), {'feat': 'primary_key'}),
    # (h('post1'), {'feat': 'post_id'}),
    (h('comment_id1'), {'feat': 'comment_id'}),
    (h('comment_body1'), {'feat': 'comment_body'}),

    (h('Andy'), {'feat': 'first_name'}),
    (h('Bob'), {'feat': 'first_name'}),
    (h('Zero'), {'feat': 'last_name'}),
]

graph_nodes.sort()

# Construct the target graph
G = nx.Graph()
G.add_nodes_from(graph_nodes)
G.add_edges_from([
    # (h('primary0'), h("comment_id0")),
    # (h('primary0'), h("comment_body0")),

    # (h('primary1'), h("comment_id1")),
    # (h('primary1'), h("comment_body1")),
    
    (h('primary1'), h("Andy")),
    (h('primary1'), h("Bob")),
    (h('primary1'), h("Zero")),
    
    # (h('comment_id0'), {'feat': 'comment_id'}),
    # (h('comment_body0'), {'feat': 'comment_body'}),
    
    # (h('session1'), {'feat': 'session'}),
    # (h('post1'), {'feat': 'post_id'}),
    # (h('comment_id1'), {'feat': 'comment_id'}),
    # (h('comment_body1'), {'feat': 'comment_body'}),
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
