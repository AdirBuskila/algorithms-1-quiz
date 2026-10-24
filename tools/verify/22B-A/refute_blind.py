import itertools, random
from collections import Counter
def pi(P):
    p=[0]*len(P)
    for i in range(1,len(P)):
        k=p[i-1]
        while k and P[i]!=P[k]:k=p[k-1]
        if P[i]==P[k]:k+=1
        p[i]=k
    return p
for tgt in([0,0,0,0,0,1],[0,0,1,1,2,1]):
    for al in('ab','abc','abcd'):
        s=[''.join(t) for t in itertools.product(al,repeat=6) if pi(t)==tgt]
        print(tgt,al,s[:5],len(s))
# Q2 brute
def truth(A):
    n=len(A);c=Counter(A);vals=sorted(c);need=-(-n//2)
    return any(c[vals[i]]+c[vals[i+1]]>=need for i in range(len(vals)-1))
def alg(A,positions):
    n=len(A);s=sorted(A);c=Counter(A);vals=sorted(c);need=-(-n//2)
    for p in positions(n):
        v=s[p-1];i=vals.index(v)
        for j in (i-1,i):
            if 0<=j<len(vals)-1 and c[vals[j]]+c[vals[j+1]]>=need: return True
    return False
pos_med=lambda n:[ (n+1)//2 ]
pos_two=lambda n:[n//2,n//2+1] if n%2==0 else [(n+1)//2]
pos_n2=lambda n:[n//2]  # position floor(n/2)
bad={'ceil-only':0,'two':0,'floor-only':0}
ex=[]
for _ in range(20000):
    n=random.randint(2,9);A=[random.randint(1,6) for _ in range(n)]
    t=truth(A)
    if alg(A,pos_med)!=t: bad['ceil-only']+=1; ex.append(A) if len(ex)<3 else 0
    if alg(A,pos_two)!=t: bad['two']+=1
    if alg(A,pos_n2)!=t: bad['floor-only']+=1
print(bad,ex)
print('counter [1,2,3,4,5,5] truth',truth([1,2,3,4,5,5]), 'floor-only',alg([1,2,3,4,5,5],pos_n2),'two',alg([1,2,3,4,5,5],pos_two))
print('example',truth([5,2,8,3,2,5,8]))
# Q3a
import networkx as nx
G=nx.Graph();G.add_weighted_edges_from([(1,2,1),(2,3,2),(1,3,2)])
def trees(G):
    for c in itertools.combinations(G.edges(data='weight'),2):
        H=nx.Graph(); H.add_nodes_from(G); H.add_edges_from((a,b) for a,b,_ in c)
        if nx.is_connected(H): yield c
for t in trees(G):print(t,sum(w for *_,w in t),max(w for *_,w in t))
# Q3b brute: every MST has min bottleneck on random graphs
ok=True
for _ in range(500):
    n=random.randint(3,6);G=nx.gnp_random_graph(n,0.7)
    if not nx.is_connected(G):continue
    for u,v in G.edges: G[u][v]['weight']=random.randint(1,4)
    ts=[]
    for c in itertools.combinations(G.edges(data='weight'),n-1):
        H=nx.Graph();H.add_nodes_from(G);H.add_edges_from((a,b) for a,b,_ in c)
        if nx.is_connected(H): ts.append(c)
    mb=min(max(w for *_,w in t) for t in ts);ms=min(sum(w for *_,w in t) for t in ts)
    for t in ts:
        if sum(w for *_,w in t)==ms and max(w for *_,w in t)!=mb: ok=False
print('MST=>MBST',ok)
# Q4
def cnt(T,P):
    c=0
    for idx in itertools.combinations(range(len(T)),len(P)):
        if all(T[i]==p for i,p in zip(idx,P)):c+=1
    return c
print(cnt('subsequence','see'),cnt('abcbac','abc'))
def dp(T,P):
    n,m=len(T),len(P);D=[[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1):D[i][0]=1
    for i in range(1,n+1):
        for j in range(1,m+1):
            D[i][j]=D[i-1][j]+(D[i-1][j-1] if T[i-1]==P[j-1] else 0)
    return D
for r in dp('abcbac','abc'):print(r)
ok=True
for _ in range(300):
    T=''.join(random.choice('abc') for _ in range(random.randint(0,8)));P=''.join(random.choice('abc') for _ in range(random.randint(1,3)))
    if dp(T,P)[-1][-1]!=cnt(T,P):ok=False
print('dp ok',ok)
# Q1d
def T(n): return 0 if n<=1 else 1+2*T(n//2)
print([T(2**k) for k in range(6)])
