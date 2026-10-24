import itertools
E=[(1,4),(1,9),(4,9),(1,6),(6,2),(6,7),(6,5),(5,3),(5,8),(3,8),(9,0)]
outs=set()
def rec(edges,C):
    if not edges: outs.add(frozenset(C));return
    for (u,v) in edges:
        rec([e for e in edges if u not in e and v not in e],C|{u,v})
rec(E,frozenset())
opts={'a':{5,3,2,7,1,9},'b':{3,4,1,9,0,6},'c':{1,8,3,4,9,6},'e':{1,9,6,3,5,8},'f':{6,3,1,8,0,4}}
print(len(outs))
for k,v in opts.items(): print(k,frozenset(v) in outs, all(u in v or w in v for u,w in E))
# maximal matchings variant: output is vertex cover; also check whether cover is valid
