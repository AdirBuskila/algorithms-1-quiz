import itertools, random
from fractions import Fraction
# Suffix array
s='BANANABAN'
sa=sorted(range(1,len(s)+1),key=lambda i:s[i-1:])
print('true SA',sa,'exam array [6,8,2,4,7,1,9,5,3] equal?',sa==[6,8,2,4,7,1,9,5,3])
# Q1: all simple graphs n<=6 with |E|=|V|
def comps(n,E):
    par=list(range(n))
    def f(x):
        while par[x]!=x:x=par[x]
        return x
    for u,v in E:par[f(u)]=f(v)
    return par,f
def bfs_edges(n,E,v):
    adj={i:[] for i in range(n)};
    for a,b in E:adj[a].append(b);adj[b].append(a)
    seen={v};q=[v];c=0
    while q:
        x=q.pop(0)
        for y in adj[x]:
            if y not in seen:seen.add(y);q.append(y);c+=1
    return c
def dfs_edges(n,E):
    par,f=comps(n,E);return n-len({f(i) for i in range(n)})
res={'a':None,'b':None,'c':True}
for n in range(1,8):
    allE=list(itertools.combinations(range(n),2))
    if len(allE)<n:continue
    for E in itertools.combinations(allE,n):
        par,f=comps(n,E);conn=len({f(i) for i in range(n)})==1
        d=dfs_edges(n,E)
        bs=[bfs_edges(n,E,v) for v in range(n)]
        if not conn and res['a'] is None:res['a']=(n,E)
        if any(b==d for b in bs) and not conn and res['b'] is None:res['b']=(n,E)
        if all(b==d for b in bs) and not conn:res['c']=False;print('c counterexample',n,E)
print('Q1a counterex',res['a']);print('Q1b counterex',res['b']);print('Q1c holds (no counterex, simple graphs n<=7):',res['c'])
# multigraph/loops allowed? note
# Q2 greedy
def greedy(xs,D):
    xs=sorted(xs);st=[];i=0
    while i<len(xs):
        p=xs[i]+D;st.append(p)
        while i<len(xs) and xs[i]<=p+D:i+=1
    return st
print('greedy [1,5,9,16] D=3 ->',greedy([1,5,9,16],3))
def opt_count(xs,D):
    # brute: stations at candidate points x_i +/- D (and between): min k such that cover
    xs=sorted(xs);cands=sorted({x+d for x in xs for d in (-D,D)}|set(xs))
    for k in range(1,len(xs)+1):
        for S in itertools.combinations(cands,k):
            if all(any(abs(x-s)<=D for s in S) for x in xs):return k
for _ in range(500):
    xs=random.sample(range(0,40),random.randint(1,7));D=random.randint(1,6)
    assert len(greedy(xs,D))==opt_count(xs,D),(xs,D)
print('Q2 greedy optimal count verified')
# multiple optima for example
ex=[1,5,9,16];sols=[S for S in itertools.combinations(range(0,20),3) if all(any(abs(x-s)<=3 for s in S) for x in ex)]
print('example 3-station integer solutions',len(sols),'e.g.',sols[:5])
print('2 stations possible?',any(all(any(abs(x-s)<=3 for s in S) for x in ex) for S in itertools.combinations(range(-5,25),2)))
# Q3a: code 00,01,10,110,111
def allhuff_trees(ws):
    res=set()
    def rec(items):
        if len(items)==1:res.add(items[0][1]);return
        items=sorted(items,key=lambda x:x[0]);w=[x[0] for x in items]
        for i in range(len(items)):
            for j in range(i+1,len(items)):
                if sorted([w[i],w[j]])==w[:2]:
                    rest=[items[k] for k in range(len(items)) if k not in(i,j)]
                    rec(rest+[(w[i]+w[j],(items[i][1],items[j][1]))])
    rec([(w,str(k)) for k,w in enumerate(ws)]);return res
def codes(t,p=''):
    if len(t)==1:return {t:p}
    d={};d.update(codes(t[0],p+'0'));d.update(codes(t[1],p+'1'));return d
target={'00','01','10','110','111'}
def codeset(t):
    # tree up to left/right swap: compare multiset of lengths and structure -> use sorted code lengths and shape
    return t
def shape(t): return 'L' if isinstance(t,str) else '('+''.join(sorted([shape(t[0]),shape(t[1])]))+')'
tgt_shape='((LL)(L(LL)))'
tgt_shape=shape((('a','b'),('c',('d','e'))))
found=[]
for ws in itertools.product(range(1,8),repeat=5):
    for t in allhuff_trees(ws):
        if shape(t)==tgt_shape: found.append(ws);break
print('Q3a freq vectors (1..7) giving that tree shape under some tiebreak:',len(found),'e.g.',found[:3])
# claimed example freq?  also: forced lengths for distinct freqs? 
print('(3,3,2,1,1) assignment 00=3,01=3,10=2,110=1,111=1:',any(shape(t)==tgt_shape for t in allhuff_trees((3,3,2,1,1))))
# Q3b
print('Q3b: single-edge graph, MST contains the unique max edge -> claim false')
# Q4
def f(K):
    d=[0]*(K+1)
    for i in range(2,K+1):
        d[i]=d[i-1]+1
        if i%2==0:d[i]=min(d[i],d[i//2]+1)
        if i%3==0:d[i]=min(d[i],d[i//3]+1)
    return d
print('Q4 table K=7',f(7),' f(10)=',f(10)[10])
# brute BFS check
from collections import deque
def bfsf(K):
    dist={1:0};q=deque([1])
    while q:
        x=q.popleft()
        for y in (x+1,2*x,3*x):
            if y<=K and y not in dist:dist[y]=dist[x]+1;q.append(y)
    return dist
b=bfsf(200);d=f(200)
print('Q4 recurrence matches BFS up to 200:',all(b[i]==d[i] for i in range(1,201)))
