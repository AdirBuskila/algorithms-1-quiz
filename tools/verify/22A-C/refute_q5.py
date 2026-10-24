import itertools
E=[('a','h'),('a','b'),('a','f'),('h','g'),('h','i'),('g','f'),('g','d'),('i','b'),('i','d'),('b','c'),('c','d'),('d','e'),('d','j'),('j','f'),('f','e')]
V=sorted({x for e in E for x in e})
for k in range(len(V)+1):
    s=[set(c) for c in itertools.combinations(V,k) if all(u in c or v in c for u,v in E)]
    if s: print("OPT",k,len(s),s[:3]);break
# trace
def trace(order):
    Ep=list(E);C=set();rows=[]
    for (u,v) in order:
        assert (u,v) in Ep or (v,u) in Ep
        C|={u,v};Ep=[e for e in Ep if u not in e and v not in e];rows.append((sorted(C),len(Ep)))
    return rows,Ep
print(trace([('a','b'),('h','g'),('i','d'),('f','e')]))
# all outputs sizes
outs={}
def rec(ed,C):
    if not ed: outs[frozenset(C)]=1;return
    for u,v in ed: rec([e for e in ed if u not in e and v not in e],C|{u,v})
rec(E,frozenset())
print(sorted({len(c) for c in outs}),len(outs))
