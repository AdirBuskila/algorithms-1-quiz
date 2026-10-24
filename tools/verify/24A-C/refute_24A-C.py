import itertools, random, heapq
import networkx as nx
from collections import deque
# Q1 cut vertex: official algorithm vs definition (more components)
def official(G,x):
    nb=list(G[x])
    if len(nb)<=1: return False
    H=G.copy();H.remove_node(x)
    d=nx.single_source_shortest_path_length(H,nb[0])
    return any(u not in d for u in nb)
for _ in range(4000):
    n=random.randint(1,9);G=nx.gnp_random_graph(n,random.random()*0.6)
    for x in G:
        H=G.copy();H.remove_node(x)
        assert official(G,x)==(nx.number_connected_components(H)>nx.number_connected_components(G))
print("Q1 official alg == definition")
G=nx.Graph([(1,2),(2,3),(3,4),(4,2),(4,5),(5,6)])
print("cut count",sum(official(G,x) for x in G),[x for x in G if official(G,x)])
# Q2 knapsack
def greedy(w,v,S):
    t=0;val=0
    for wi,vi in sorted(zip(w,v),key=lambda p:(p[0],-p[1])):
        if wi<=S: S-=wi;val+=vi
        else: break
    return val
def opt(w,v,S):
    b=0
    for r in range(len(w)+1):
        for c in itertools.combinations(range(len(w)),r):
            if sum(w[i] for i in c)<=S: b=max(b,sum(v[i] for i in c))
    return b
for _ in range(3000):
    n=random.randint(1,8)
    w=sorted(random.randint(1,10) for _ in range(n)); v=sorted((random.randint(1,10) for _ in range(n)),reverse=True)
    S=random.randint(0,40)
    assert greedy(w,v,S)==opt(w,v,S),(w,v,S)
print("knapsack ok",greedy([1,4,5,7,10],[8,6,5,4,2],10),greedy([1,4,5,7,10],[8,6,5,4,2],9),opt([1,4,5,7,10],[8,6,5,4,2],9))
w=[10,1,4];v=[2,8,6]
t=0;S=10;val=0
for wi,vi in zip(w,v):
    if wi<=S:S-=wi;val+=vi
print("raw order greedy",val,"opt",opt(w,v,10))
# Q3 Huffman: enumerate all tie-breaks -> set of depth multiset / code trees
def huff_trees(freqs):
    res=set()
    def rec(nodes):
        if len(nodes)==1: res.add(nodes[0][1]);return
        nodes=sorted(nodes,key=lambda x:x[0])
        a=nodes[0][0];b=nodes[1][0]
        # candidates: pairs of the two smallest values allowing ties
        idx=range(len(nodes))
        m=[i for i in idx if nodes[i][0]==a or nodes[i][0]==b] 
        for i,j in itertools.combinations(idx,2):
            if sorted([nodes[i][0],nodes[j][0]])==[nodes[0][0],nodes[1][0]]:
                rest=[nodes[k] for k in idx if k not in(i,j)]
                rec(rest+[(nodes[i][0]+nodes[j][0],(nodes[i][1],nodes[j][1]))])
    rec([(f,i) for i,f in enumerate(freqs)])
    def canon(t):
        if isinstance(t,int): return str(t)
        return '('+','.join(sorted([canon(t[0]),canon(t[1])]))+')'
    return {canon(t) for t in res}
print("3,4,3,1,2 trees:",huff_trees([3,4,3,1,2]))
def cost(f):
    h=list(f);heapq.heapify(h);c=0
    while len(h)>1:
        a=heapq.heappop(h);b=heapq.heappop(h);c+=a+b;heapq.heappush(h,a+b)
    return c
print("cost 3,4,3,1,2",cost([3,4,3,1,2]),"code cost",3*2+4*2+3*2+1*3+2*3)
print("1,3,9,27,81",cost([1,3,9,27,81]),1*4+3*4+9*3+27*2+81)
print("trees 1..81",huff_trees([1,3,9,27,81]),"equal5",huff_trees([1,1,1,1,1]))
# kraft code check: tie-free freq for code 00,11,01,100,101
f=[7,9,8,4,6] # a1=00,a2=11,a3=01,a4=100,a5=101  -> a1:7? set explicit
f1,f2,f3,f4,f5=7,9,8,4,6
print("tie-free huffman trees",huff_trees([f1,f2,f3,f4,f5]))
for q in (1,2,3,4,5,10,1.5,1.2):
    fr=[q**i for i in range(5)]
    print("q",q,huff_trees([round(x*1000) for x in fr]))
# Q4 jump
A=[1,4,6,4,5,3,3,2,1,3];n=len(A)
C=[None]*(n+1);C[n]=0
for i in range(n-1,0,-1):
    C[i]=1+min(C[i+j] for j in range(1,min(A[i-1],n-i)+1))
print("C",C[1:])
# BFS check
def bfs(A):
    n=len(A);d={1:0};q=deque([1])
    while q:
        i=q.popleft()
        for j in range(i+1,min(n,i+A[i-1])+1):
            if j not in d:d[j]=d[i]+1;q.append(j)
    return d[n]
print("bfs",bfs(A))
for _ in range(2000):
    n=random.randint(1,9);A=[random.randint(1,4) for _ in range(n)]
    C=[None]*(n+1);C[n]=0
    for i in range(n-1,0,-1): C[i]=1+min(C[i+j] for j in range(1,min(A[i-1],n-i)+1))
    assert C[1]==bfs(A)
    # alt formula
    D=[None]*(n+1);D[1]=0
    for i in range(2,n+1): D[i]=1+min(D[j] for j in range(1,i) if j+A[j-1]>=i)
    assert D[n]==C[1]
A=[1,4,6,4,5,3,3,2,1,3];n=10
# count paths of 3 jumps
paths=[]
def go(i,p):
    if i==n: paths.append(p);return
    for j in range(i+1,min(n,i+A[i-1])+1): go(j,p+[j])
go(1,[1]);print("min paths",[p for p in paths if len(p)==4])
print("greedy farthest:",)
i=1;c=0
while i<n: i=min(i+A[i-1],n);c+=1
print(c)
print("sum n-i",sum(10-i for i in range(1,10)))
# Q5 prim
E=[("L","TL",12),("TL","TM",9),("TM","TR",11),("TM","C",8),("TR","BR",13),("C","BL",10),("C","BM",9),("BL","BM",8),("BM","BR",13),("L","BL",15)]
for trbr in (13,14):
    E2=[(u,v,(trbr if (u,v)==("TR","BR") else w)) for u,v,w in E]
    G=nx.Graph();G.add_weighted_edges_from(E2)
    seqs=set()
    def rec(T,seq):
        if len(T)==len(G): seqs.add(tuple(seq));return
        cand=[(G[u][v]['weight'],u,v) for u in T for v in G[u] if v not in T]
        m=min(c[0] for c in cand)
        for c in {(w,v) for w,u,v in cand if w==m}:
            rec(T|{c[1]},seq+[m])
    rec({"C"},[])
    print("TR-BR",trbr,"claimed possible",(8,9,9,8,11,12,13) in seqs,"all seqs",sorted(seqs),"MST",nx.minimum_spanning_tree(G).size(weight='weight'))
