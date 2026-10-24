import itertools, heapq, bisect, random
# Q1: tasks, no two consecutive skipped
def brute(A):
    n=len(A);best=None
    for m in range(1<<n):
        ok=True
        for i in range(n-1):
            if not (m>>i&1) and not (m>>(i+1)&1): ok=False;break
        if ok:
            s=sum(A[i] for i in range(n) if m>>i&1)
            best=s if best is None or s<best else best
    return best
print('Q1a [10]->',brute([10]),' ex1',brute([10,5,7,10]),' ex2',brute([10,5,2,4,8,6,7,10]))
def dp(A):
    n=len(A)
    T=[0]*(n+2)
    for i in range(n-1,-1,-1): T[i]=A[i]+min(T[i+1],T[i+2])
    return min(T[0],T[1]) if n>=2 else 0
def dp2(A):  # F(i)=min cost of A[i..], i-1 chosen? alt formulation
    from functools import lru_cache
    n=len(A)
    @lru_cache(None)
    def F(i): # prev task i-1 skipped? no: prev was chosen => free to skip i
        if i>=n: return 0
        return min(F(i+1), A[i]+F(i+1) if False else A[i]+F(i+1))
    return None
for _ in range(2000):
    A=[random.randint(1,9) for _ in range(random.randint(1,10))]
    assert brute(A)==dp(A),(A,brute(A),dp(A))
print('Q1b dp T(i)=A[i]+min(T(i+1),T(i+2)), ans min(T0,T1) ok')
# Q3a Huffman all tie-breaks
f={'a':22,'b':15,'c':3,'d':24,'e':4,'f':10,'g':8}
def allhuff(items):
    # items: list of (w, tree); explore all choices of the two smallest (with ties)
    res=set()
    def rec(items):
        if len(items)==1: res.add(items[0][1]);return
        items=sorted(items,key=lambda x:x[0])
        ws=[x[0] for x in items]
        # candidate pairs: any pair (i,j) whose weights are the two smallest values multiset
        for i in range(len(items)):
            for j in range(i+1,len(items)):
                if sorted([ws[i],ws[j]])==ws[:2]:
                    rest=[items[k] for k in range(len(items)) if k not in(i,j)]
                    rec(rest+[(ws[i]+ws[j],(items[i][1],items[j][1]))])
    rec(items); return res
trees=allhuff([(w,s) for s,w in f.items()])
def codes(t,p=''):
    if isinstance(t,str): return {t:p}
    d={};d.update(codes(t[0],p+'0'));d.update(codes(t[1],p+'1'));return d
def lens(t):
    return {k:len(v) for k,v in codes(t).items()}
costs=set(); shapes=set()
for t in trees:
    L=lens(t); costs.add(sum(f[k]*L[k] for k in f)); shapes.add(tuple(sorted(L.items())))
print('Q3a costs',costs,'distinct length-vectors',len(shapes))
for s in shapes: print(s)
# optimum check by exhaustive: min cost over all full trees = Huffman cost
# Q3b: freq 2^-depth gives T as a Huffman tree under some tie-break
def fulltrees(n):
    if n==1: return ['L']
    out=[]
    for k in range(1,n):
        for l in fulltrees(k):
            for r in fulltrees(n-k): out.append((l,r))
    return out
def leafdepths(t,d=0):
    if t=='L': return [d]
    return leafdepths(t[0],d+1)+leafdepths(t[1],d+1)
def shape(t):
    return 'L' if t=='L' else (shape(t[0]),shape(t[1]))
def huff_shapes(ws):
    res=set()
    def rec(items):
        if len(items)==1: res.add(items[0][1]);return
        items=sorted(items,key=lambda x:x[0]); w=[x[0] for x in items]
        for i in range(len(items)):
            for j in range(len(items)):
                if i!=j and sorted([w[i],w[j]])==w[:2]:
                    rest=[items[k] for k in range(len(items)) if k not in(i,j)]
                    rec(rest+[(w[i]+w[j],(items[i][1],items[j][1]))])
    rec([(w,'L') for w in ws]); return res
def canon(t):
    if t=='L':return 'L'
    a,b=sorted([canon(t[0]),canon(t[1])]); return '('+a+b+')'
from fractions import Fraction
cnt=0
for n in range(2,8):
    for T in fulltrees(n):
        ws=[Fraction(1,2**d) for d in leafdepths(T)]
        hs={canon(h) for h in huff_shapes(ws)}
        assert canon(T) in hs,(n,T)
        cnt+=1
print('Q3b: freq 2^-depth realizes every full tree up to n=7:',cnt,'trees')
# Q4
def missing(A,k):
    x=0;c=0
    S=set(A)
    while True:
        x+=1
        if x not in S:
            c+=1
            if c==k:return x
print('Q4a',missing([3,5,9,10,11,12],2),missing([2,3,4,7,11],5))
def fast(A,k):
    lo,hi=0,len(A)
    while lo<hi:
        m=(lo+hi)//2
        if A[m]-(m+1)>=k: hi=m
        else: lo=m+1
    return lo+k
for _ in range(3000):
    A=sorted(random.sample(range(1,40),random.randint(0,12)));k=random.randint(1,15)
    assert fast(A,k)==missing(A,k)
print('Q4b binary search A[m]-(m+1)>=k ok')
# Q2 brute (manual Kruskal)
def kruskal(n,W):
    par=list(range(n))
    def find(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    T=set()
    for w,(u,v) in sorted((w,e) for e,w in W.items()):
        a,b=find(u),find(v)
        if a!=b: par[a]=b;T.add(frozenset((u,v)))
    return T
fa=False;tb=True
for _ in range(5000):
    n=random.randint(3,7);E=list(itertools.combinations(range(n),2))
    W=dict(zip(E,random.sample(range(1,200),len(E))))
    T=kruskal(n,W)
    special=set()
    for u in range(n):
        e=min((e for e in E if u in e),key=lambda e:W[e]);special.add(frozenset(e))
    if T-special: fa=True
    if special-T: tb=False
print('Q2a counterexample (MST edge not special) found:',fa,'| Q2b special always in MST:',tb)
# explicit 4-vertex counterexample uw=1 vx=2 uv=3 others bigger
W={(0,1):1,(2,3):2,(0,2):3,(0,3):4,(1,2):5,(1,3):6} # u=0? edges: 0-1 (u-w),2-3(v-x),0-2(u-v)
T=kruskal(4,W);print('explicit K4 MST',sorted(map(sorted,T)),'edge {0,2} in T and not special:',frozenset((0,2)) in T)
