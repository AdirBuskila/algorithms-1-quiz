import itertools, random, math
import networkx as nx
from functools import lru_cache
from collections import deque
# Q1: walk semantics: shortest walk x->A->y = min dx[v]+dy[v]; brute via product-state BFS
def bfs(G,s):
    return nx.single_source_shortest_path_length(G,s)
def prod(G,x,y,A):
    st=(x,x in A); dist={st:0}; q=deque([st])
    while q:
        v,f=q.popleft()
        if v==y and f: return dist[(v,f)]
        for w in G[v]:
            s2=(w,f or w in A)
            if s2 not in dist: dist[s2]=dist[(v,f)]+1; q.append(s2)
    return math.inf
for _ in range(3000):
    n=random.randint(3,8); G=nx.gnp_random_graph(n,random.random()*0.6)
    x,y=random.sample(range(n),2); rest=[v for v in range(n) if v not in(x,y)]
    A=set(random.sample(rest,random.randint(1,len(rest))))
    dx=bfs(G,x); dy=bfs(G,y)
    cl=math.inf if y not in dx else min([dx[v]+dy[v] for v in A if v in dx] or [math.inf])
    assert cl==prod(G,x,y,A)
    # Q1a
    a = y in dx and any(v in dx for v in A)
    assert a==(prod(G,x,y,A)<math.inf)
print("Q1 ok")
G=nx.Graph([(1,2),(2,3),(3,4),(4,5),(2,6),(6,7)])
for A in ({7},{3,7}):
    print(A,prod(G,1,5,A))
G2=nx.Graph([(1,2),(2,3),(3,4),(5,6)]);print(prod(G2,1,4,{3}),prod(G2,1,4,{5}))
# Q2 greedy vs DP
def greedy(L,m):
    c=0;rem=0
    for l in L:
        if l<=rem: rem-=l
        else: c+=1; rem=m-l
    return c
def opt(L,m):
    n=len(L)
    @lru_cache(None)
    def f(i):
        if i==n: return 0
        best=10**9;s=0
        for j in range(i,n):
            s+=L[j]
            if s>m: break
            best=min(best,1+f(j+1))
        return best
    return f(0)
for _ in range(5000):
    m=random.randint(1,9);L=tuple(random.randint(1,m) for _ in range(random.randint(1,8)))
    assert greedy(L,m)==opt(L,m)
print("greedy ok",greedy((2,1,4,2),5),greedy((3,3,2,4,1),6))
# Q3a brute 6 bits
ok=True
primes=lambda N:[p for p in range(2,N+1) if all(p%d for d in range(2,int(p**.5)+1))]
bad=0
for x in range(64):
    for b in range(6):
        y=x^(1<<b)
        for q in primes(36):
            if x%q==y%q: bad+=1
print("collisions exist (6 bits):",bad>0, "q=2 example", 10%2==8%2, bin(10),bin(8))
# p0 for one-bit difference
for n in (2,3,5,10,20):
    P=primes(n*n); worst=0
    for i in range(n):
        d=1<<i
        worst=max(worst,sum(1 for q in P if d%q==0)/len(P))
    print("n",n,"p0max",worst,"pi",len(P))
# Q3b bits
for n in (10,100):
    P=primes(n*n); print(n,P[-1],P[-1].bit_length(),math.ceil(math.log2(n*n)),2*math.ceil(math.log2(n*n)))
print("0.3^3",0.3**3, 3*.09*.7+.027, 1-.7**3)
# Q4 dice
def T(i,j):
    @lru_cache(None)
    def t(i,j):
        if i==0: return 1 if j==0 else 0
        if j==0: return 0
        return sum(t(i-1,j-k) for k in range(1,7) if j-k>=0)
    return t(i,j)
def brute(i,j): return sum(1 for r in itertools.product(range(1,7),repeat=i) if sum(r)==j)
for i in range(1,6):
    for j in range(1,31): assert T(i,j)==brute(i,j)
print("T(2,7)",T(2,7),"T(3,10)",T(3,10))
# count of outcomes vs table size (4c all-combinations exponential)
print("n=20,m=70 outcomes",T(20,70),"table",20*70)
# Q5 intervals
iv=[(0,10),(9,12),(11,20)]
def maxset(iv):
    b=0
    for r in range(len(iv)+1):
        for S in itertools.combinations(iv,r):
            if all(S[a][1]<S[b2][0] or S[b2][1]<S[a][0] for a in range(len(S)) for b2 in range(a+1,len(S))): b=max(b,r)
    return b
print("opt",maxset(iv),"shortest-first picks [9,12] ->1")
