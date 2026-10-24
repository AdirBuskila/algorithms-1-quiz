import itertools
def canon(t):
    return t if isinstance(t,str) else tuple(sorted((canon(t[0]),canon(t[1])),key=repr))
def huff_trees(items):
    # items: list of (weight, tree); return set of canon trees over all tie-breaks
    if len(items)==1: return {canon(items[0][1])}
    items=sorted(items,key=lambda x:x[0]); res=set()
    n=len(items)
    # candidates for pair: any (i,j) such that the pair is a valid "two smallest" multiset
    w=[x[0] for x in items]
    for i in range(n):
        for j in range(i+1,n):
            if sorted([w[i],w[j]])==w[:2]:
                rest=[items[k] for k in range(n) if k not in(i,j)]
                new=(w[i]+w[j],(items[i][1],items[j][1]))
                res|=huff_trees(rest+[new])
    return res
target=canon((('b',('c','d')),('a','e')))
def weight(t,f):
    return f[t] if isinstance(t,str) else weight(t[0],f)+weight(t[1],f)
sol=[]
for c in range(1,40):
  for d in range(1,40):
    f=dict(a=7,b=4,e=7,c=c,d=d)
    # left<=right on given tree
    ok = c<=d and 4<=c+d and weight((('b',('c','d'))),f)<=weight(('a','e'),f)
    if not ok: continue
    items=[(f[x],x) for x in f]
    if target in huff_trees(items): sol.append((c,d))
print(len(sol),sol)
# without tie ambiguity: strict deterministic? just info
