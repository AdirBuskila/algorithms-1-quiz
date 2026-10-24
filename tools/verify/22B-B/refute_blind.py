import itertools, heapq, networkx as nx
# Q1a: huffman shapes under any tie break
def shapes(freqs):
    res=set()
    def rec(nodes):
        if len(nodes)==1:
            res.add(canon(nodes[0])); return
        nodes=sorted(nodes,key=lambda n:n[0])
        # all pairs among minimal choices
        for i in range(len(nodes)):
            for j in range(i+1,len(nodes)):
                rest=[n for t,n in enumerate(nodes) if t not in(i,j)]
                a,b=nodes[i],nodes[j]
                # valid if a,b are two smallest (weights)
                ws=sorted(n[0] for n in nodes)
                if sorted([a[0],b[0]])!=ws[:2]: continue
                rec(rest+[(a[0]+b[0],('N',a,b))])
    def canon(n):
        t=n[1]
        if t[0]=='L': return ('L',)
        l,r=canon(t[1]),canon(t[2])
        return ('N',)+tuple(sorted([l,r]))
    rec([(f,('L',i)) for i,f in enumerate(freqs)])
    return res
# shape up to unlabeled? need labels: use depth multiset per letter
def depthsets(freqs):
    res=set()
    def rec(nodes):
        if len(nodes)==1:
            d={}
            def w(n,dep):
                if n[0]=='L': d[n[1]]=dep
                else: w(n[1],dep+1); w(n[2],dep+1)
            w(nodes[0][1],0); res.add(tuple(d[i] for i in range(len(freqs)))); return
        ws=sorted(n[0] for n in nodes)
        for i in range(len(nodes)):
            for j in range(i+1,len(nodes)):
                a,b=nodes[i],nodes[j]
                if sorted([a[0],b[0]])!=ws[:2]: continue
                rest=[n for t,n in enumerate(nodes) if t not in(i,j)]
                rec(rest+[(a[0]+b[0],('N',a[1],b[1]))])
    rec([(f,('L',i)) for i,f in enumerate(freqs)])
    return res
print('1,1,2,3',depthsets([1,1,2,3]),'3,3,4,5',depthsets([3,3,4,5]))
# does +k ever hold? search random counterexamples
cnt=0
for f in itertools.product(range(1,6),repeat=4):
    for k in range(1,4):
        if depthsets(list(f))!=depthsets([x+k for x in f]): cnt+=1
print('cases where tree sets differ',cnt)
# Q1b brute force: code a-1 b-00 c-01 ; leaves left<=right freq
def codes_ok(freqs_map, target, orient_rule=True):
    pass
def huff_codes(f, leftle=True):
    # all huffman trees with any tie-break, children ordered so left freq <= right freq (both orders if equal)
    out=set()
    def rec(nodes):
        if len(nodes)==1:
            c={}
            def w(n,p):
                if n[0]=='L': c[n[1]]=p
                else: w(n[1],p+'0'); w(n[2],p+'1')
            w(nodes[0][1],''); out.add(tuple(sorted(c.items()))); return
        ws=sorted(n[0] for n in nodes)
        for i in range(len(nodes)):
            for j in range(i+1,len(nodes)):
                a,b=nodes[i],nodes[j]
                if sorted([a[0],b[0]])!=ws[:2]: continue
                rest=[n for t,n in enumerate(nodes) if t not in(i,j)]
                for l,r in((a,b),(b,a)):
                    if l[0]<=r[0]:
                        rec(rest+[(a[0]+b[0],('N',l[1],r[1]))])
    rec([(v,('L',k)) for k,v in f.items()])
    return out
sol=[]
for x in range(1,11):
    y=8-x
    if y<1: continue
    if (('a','1'),('b','00'),('c','01')) in huff_codes({'a':x,'b':2,'c':y}): sol.append((x,y))
print('Q1b (x,y)',sol)
sol=[]
tgt=(('a','0'),('b','100'),('c','101'),('d','11'))
for x in range(1,40):
    for y in range(1,40):
        if tgt in huff_codes({'a':y,'b':2,'c':x,'d':5}): sol.append((x,y))
print('22B-A Q1c (x,y)',sol)
# Q1c suffix: longest repeated substring of ABABABA
T='ABABABA'
best=''
for i in range(len(T)):
    for j in range(i+1,len(T)+1):
        s=T[i:j]
        if sum(T.startswith(s,p) for p in range(len(T)))>=2 and len(s)>len(best): best=s
print('LRS',best)
# Q2: brute force
A=[8,4,5,2,10];k=2
bestd=max(abs(sum(c)-(sum(A)-sum(c))) for c in itertools.combinations(A,k));print('Q2 best',bestd)
def alg_orig(A,k):  # k smallest or k largest
    s=sorted(A);n=len(A);S=sum(A)
    d1=S-2*sum(s[:k]); d2=2*sum(s[n-k:])-S
    return max(d1,d2)
def alg_only_small(A,k):
    s=sorted(A); return sum(s[k:])-sum(s[:k])
import random
bad_small=0;bad_both=0
for _ in range(3000):
    n=random.randint(2,7);A=random.sample(range(1,30),n);k=random.randint(1,n-1)
    b=max(abs(sum(c)-(sum(A)-sum(c))) for c in itertools.combinations(A,k))
    if alg_orig(A,k)!=b: bad_both+=1
    if alg_only_small(A,k)!=b: bad_small+=1
print('both-ends wrong',bad_both,'only-smallest wrong',bad_small)
# Q3
E=[('B','C',12),('C','D',1),('B','J',10),('C','J',11),('C','A',16),('C','E',2),('D','E',3),('J','A',13),('A','E',15),('E','F',4),('J','G',8),('J','H',9),('A','G',14),('E','G',5),('H','G',7),('G','F',6)]
G=nx.Graph();G.add_weighted_edges_from(E)
vis={'A'};order=[]
while len(vis)<len(G):
    w,u,v=min((d['weight'],u,v) for u in vis for v,d in G[u].items() if v not in vis)
    order.append(w);vis.add(v)
print('Prim',order)
mst=nx.minimum_spanning_tree(G);print('mst edges',sorted(d['weight'] for _,_,d in mst.edges(data=True)))
# count MSTs: brute force over spanning trees
cnt=0;best=None
ws=[w for *_,w in E];
mw=sum(d['weight'] for *_,d in mst.edges(data=True))
for comb in itertools.combinations(E,len(G)-1):
    if sum(c[2] for c in comb)!=mw: continue
    H=nx.Graph();H.add_nodes_from(G);H.add_edges_from((a,b) for a,b,_ in comb)
    if nx.is_connected(H): cnt+=1
print('#MST',cnt, 'weights distinct',len(set(ws))==len(ws))
# Q4
def minrem(A,k):
    A=sorted(A);best=0
    for i in range(len(A)):
        for j in range(i,len(A)):
            if A[j]-A[i]<=k: best=max(best,j-i+1)
    return len(A)-best
print(minrem([1,3,4,9,10,12,17,20],4),minrem([1,2,5,6,8],2))
# dp formula candidates: f(i)=max window ending at i
A=[1,2,5,6,8];k=2
L=[];
for i in range(len(A)):
    j=i
    while j>0 and A[i]-A[j-1]<=k:j-=1
    L.append(i-j+1)
print('window len ending at i',L,'remove',len(A)-max(L))
