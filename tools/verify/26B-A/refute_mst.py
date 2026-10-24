import itertools
E0=[('A','D',7),('A','C',2),('A','B',6),('A','F',8),('C','D',1),('C','B',3),('C','F',9),('D','E',4),('E','G',2),('E','F',5),('G','F',7),('G','H',3),('F','H',4)]
V='ABCDEFGH'
def edges(X): return E0+[('D','F',X)]
def isTree(es):
    p={v:v for v in V}
    def f(x):
        while p[x]!=x:x=p[x]
        return x
    for a,b,_ in es:
        ra,rb=f(a),f(b)
        if ra==rb:return False
        p[ra]=rb
    return True
def msts(X):
    E=edges(X);best=None;res=[]
    for c in itertools.combinations(E,7):
        if isTree(c):
            w=sum(e[2] for e in c)
            if best is None or w<best: best=w;res=[c]
            elif w==best:res.append(c)
    return best,res
for X in range(0,12):
    b,r=msts(X)
    inall=all(('D','F',X) in m for m in r)
    print(X,b,len(r),inall)
# Prim from C, X=3
def prim_runs(X,s='C'):
    E=edges(X);out=set()
    def rec(T,order):
        if len(T)==8: out.add(tuple(order));return
        cand=[e for e in E if (e[0] in T)!=(e[1] in T)]
        m=min(e[2] for e in cand)
        for e in cand:
            if e[2]==m:
                nv=e[1] if e[0] in T else e[0]
                rec(T|{nv},order+[(e[0],e[1],e[2]) if e[0] in T else (e[1],e[0],e[2])])
    rec({s},[]);return out
for X in (3,):
    o=prim_runs(X)
    print(X,len(o))
    for r in sorted(o):print([a+b for a,b,_ in r],sum(w for *_,w in r))
    print(len({frozenset(frozenset(e[:2]) for e in r) for r in o}),"distinct MSTs")
