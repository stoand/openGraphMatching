import networkx as nx
import openGraphMatching.matcher as matcher
from openGraphMatching.utils import convert_graph, check_match_correctness

# PostForm(session, id, body) :-
#     PostId(session: Session, @id: Id),
#     PostBody(session: Session, id: Id, @body: String).

# CommentForm(session, post_id, id, title, body) :-
#     CommentId(session: Session, post_id: Id, @id: Id),
#     CommentPostId(session: Session, @post_id: Id, id: Id),
#     CommentTitle(session: Session, post_id: Id, id: Id, @title: String),
#     CommentBody(session: Session, post_id: Id, id: Id, @body: String).

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
    (1, {'feat': 'CommentPostId'}),
    (2, {'feat': 'CommentTitle'}),
    (3, {'feat': 'CommentBody'}),
    
    (4, {'feat': 'PostId'}),
    (5, {'feat': 'PostBody'}),
    
    (6, {'feat': 'HyperLinkId'}),
    (7, {'feat': 'HyperLinkPostId'}),
    (8, {'feat': 'HyperLinkValue'}),
])

q.add_edges_from([
    (0, 1),
    (0, 2),
    (0, 3),

    (4, 5),

    (4, 1),
    
    (6, 7),
    (6, 8),
    
    (4, 6),
])

graph_nodes = [
    (h('CommentId:session0:post0:id0'), {'feat': 'CommentId'}),
    (h('CommentPostId:session0:post0:id0'), {'feat': 'CommentPostId'}),
    (h('CommentTitle:session0:post0:id0:titleval0'), {'feat': 'CommentTitle'}),
    (h('CommentBody:session0:post0:id0:bodyval0'), {'feat': 'CommentBody'}),
    
    (h('CommentId:session0:post0:id1'), {'feat': 'CommentId'}),
    (h('CommentPostId:session0:post0:id1'), {'feat': 'CommentPostId'}),
    (h('CommentTitle:session0:post0:id1:titleval1'), {'feat': 'CommentTitle'}),
    (h('CommentBody:session0:post0:id1:bodyval1'), {'feat': 'CommentBody'}),
    
    (h('PostId:session0:post0'), {'feat': 'PostId'}),
    (h('PostBody:session0:post0:bodyval33'), {'feat': 'PostBody'}),
    
    (h('HyperLinkId:session0:post0:id0'), {'feat': 'HyperLinkId'}),
    (h('HyperLinkPostId:session0:post0:id0'), {'feat': 'HyperLinkPostId'}),
    (h('HyperLinkValue:session0:post0:id0:hlvalue'), {'feat': 'HyperLinkValue'}),
    
    (h('HyperLinkId:session0:post0:id1'), {'feat': 'HyperLinkId'}),
    (h('HyperLinkPostId:session0:post0:id1'), {'feat': 'HyperLinkPostId'}),
    (h('HyperLinkValue:session0:post0:id1:hlvalue2'), {'feat': 'HyperLinkValue'}),
]

graph_nodes.sort()

# Construct the target graph
G = nx.Graph()
G.add_nodes_from(graph_nodes)
G.add_edges_from([
    (h('CommentId:session0:post0:id0'), h('CommentPostId:session0:post0:id0')),
    (h('CommentId:session0:post0:id0'), h('CommentTitle:session0:post0:id0:titleval0')),
    (h('CommentId:session0:post0:id0'), h('CommentBody:session0:post0:id0:bodyval0')),
    
    (h('CommentId:session0:post0:id1'), h('CommentPostId:session0:post0:id1')),
    (h('CommentId:session0:post0:id1'), h('CommentTitle:session0:post0:id1:titleval1')),
    (h('CommentId:session0:post0:id1'), h('CommentBody:session0:post0:id1:bodyval1')),
    
    (h('PostId:session0:post0'), h('PostBody:session0:post0:bodyval33')),
    
    (h('PostId:session0:post0'), h('CommentPostId:session0:post0:id1')),
    (h('PostId:session0:post0'), h('CommentPostId:session0:post0:id0')),
    
    (h('HyperLinkId:session0:post0:id0'), h('HyperLinkPostId:session0:post0:id0')),
    (h('HyperLinkId:session0:post0:id0'), h('HyperLinkValue:session0:post0:id0:hlvalue')),
    
    (h('PostId:session0:post0'), h('HyperLinkId:session0:post0:id0')),
    
    (h('HyperLinkId:session0:post0:id1'), h('HyperLinkPostId:session0:post0:id1')),
    (h('HyperLinkId:session0:post0:id1'), h('HyperLinkValue:session0:post0:id1:hlvalue2')),
    
    (h('PostId:session0:post0'), h('HyperLinkId:session0:post0:id1')),
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
