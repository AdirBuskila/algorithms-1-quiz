import itertools, heapq, random, json, math
import networkx as nx
from math import comb
# Q1: snake
def longest(A):
    n=len(A); m=len(A[0]); T=[[1]*m for _ in range(n)]
    best=0
    for i in range(n):
        for j in range(m):
            for (a,b) in ((i-1,j),(i,j-1)):
                if a>=0 and b>=0 and abs(A[i][j]-A[a][b])<=1: T[i][j]=max(T[i][j],1+T[a][b])
    return T
def brute(A):
    n=len(A); m=len(A[0]); best=0
    def go(i,j,l):
        nonlocal best
        best=max(best,l)
        for a,b in ((i+1,j),(i,j+1)):
            if a<n and b<m and abs(A[a][b]-A[i][j])<=1: go(a,b,l+1)
    for i in range(n):
        for j in range(m): go(i,j,1)
    return best
A=[[10,20,30,40,50],[20,10,7,20,40],[30,20,8,8,30],[40,30,20,9,20],[50,40,30,20,30]]
print("official A brute",brute(A))
def paths_len_from_to(A,s,t):
    res=[]
    def go(i,j,p):
        if (i,j)==t: res.append(p); return
        for a,b in ((i+1,j),(i,j+1)):
            if a<=t[0] and b<=t[1] and abs(A[a][b]-A[i][j])<=1: go(a,b,p+[A[a][b]])
    go(s[0],s[1],[A[s[0]][s[1]]]); return res
print("paths (2,3)->(4,4) 0-idx (1,2)->(3,3):",paths_len_from_to(A,(1,2),(3,3)))
B=[[10,1,3],[12,2,2],[1,2,1]]
T=longest(B); print("T",T,brute(B))
# random check of recurrence vs brute
for _ in range(2000):
    n=random.randint(1,5);C=[[random.randint(0,4) for _ in range(n)] for _ in range(n)]
    assert max(map(max,longest(C)))==brute(C)
# Q2
print("k=7:",[ (k,0.5**k) for k in (3,6,7)])
for n in (10,):
    # any n/2+1 questions catch a half-wrong model
    for S in itertools.combinations(range(n),n//2+1):
        for good in itertools.combinations(range(n),n//2):
            assert not set(S)<=set(good)
    print("n/2+1 suffices, n/2 not:", any(set(S)<=set(good) for S in itertools.combinations(range(n),n//2) for good in [S]))
print("no-replacement pass prob n=10,k=3:",comb(5,3)/comb(10,3))
# geometric
print("E geometric",sum(k*0.5**k for k in range(1,200)))
# Q3b
def match(T,P):
    out=set()
    for perm in itertools.permutations('abc'):
        f=dict(zip('abc',perm)); Q=''.join(f[c] for c in P)
        for i in range(len(T)-len(Q)+1):
            if T[i:i+len(Q)]==Q: out.add(i)
    return sorted(out)
print("abccbaabb/abb",match("abccbaabb","abb"))
print("aaa patterns",{''.join(dict(zip('abc',p))[c] for c in 'aaa') for p in itertools.permutations('abc')})
# double count
print("dup positions possible (P=aaa, T=aaaa):",[ (p,) for p in itertools.permutations('abc')][:0], match("aaaa","aaa"))
# Q4a huffman
def hcost(f):
    h=list(f);heapq.heapify(h);c=0
    while len(h)>1:
        a=heapq.heappop(h);b=heapq.heappop(h);c+=a+b;heapq.heappush(h,a+b)
    return c
print("huffman 3,2,1,1:",hcost([3,2,1,1]),"13,0,0,0:",hcost([13,0,0,0]),"merge seq 1,1->2;2,2->4;3+4->7")
# Q4b spanning trees
def nst(edges,nodes):
    G=nx.Graph(); G.add_nodes_from(nodes); G.add_edges_from(edges)
    L=nx.laplacian_matrix(G).toarray()[1:,1:]
    import numpy as np
    return round(np.linalg.det(L))
E1=[("TL","TR"),("TL","BL"),("TL","BR"),("TR","BR"),("BL","BR")]
N=["TL","TR","BL","BR"]
print("drawing trees",nst(E1,N))
# brute
cnt=0
for S in itertools.combinations(E1,3):
    G=nx.Graph();G.add_nodes_from(N);G.add_edges_from(S)
    if nx.is_connected(G): cnt+=1
print("brute",cnt)
print("C4",nst([("a","b"),("b","c"),("c","d"),("d","a")],"abcd"),"triangle",nst([(1,2),(2,3),(1,3)],[1,2,3]))
# max spanning trees 3 vertices simple
print("3 vertices simple max: triangle 3")
# Q5 K33 maximal matching and min VC
G=nx.complete_bipartite_graph(3,3)
import random
sizes=set()
for _ in range(200):
    E=list(G.edges());random.shuffle(E);used=set();C=set()
    for u,v in E:
        if u not in used and v not in used: used|={u,v};C|={u,v}
    sizes.add(len(C))
print("K33 alg sizes",sizes)
best=min(k for k in range(7) for S in itertools.combinations(G.nodes(),k) if all(u in S or v in S for u,v in G.edges()))
print("K33 min VC",best)
print("47000",1000*(50-4+1))
