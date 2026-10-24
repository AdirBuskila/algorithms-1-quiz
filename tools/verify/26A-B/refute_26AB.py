import random, itertools, networkx as nx
from functools import lru_cache
# Q1: brute force all choices of overnight stops
def brute(p,t):
    n=len(p); best=10**18; pts=[0]+list(p)
    for days in range(1,t+1):
        for ch in itertools.combinations(range(1,n),days-1):
            idx=[0]+list(ch)+[n]
            best=min(best,sum((pts[b]-pts[a])**2 for a,b in zip(idx,idx[1:])))
    return best
def dp(p,t):
    pts=[0]+list(p);n=len(p);INF=10**18
    O=[[INF]*(t+1) for _ in range(n+1)]
    for j in range(t+1):O[0][j]=0
    for j in range(1,t+1):
        for i in range(1,n+1):
            O[i][j]=min(O[l][j-1]+(pts[i]-pts[l])**2 for l in range(i))
    return O
p=[5*i for i in range(1,7)]
print('Q1a',brute(p,3), (10-0)**2*3)
O=dp(p,3);print('OPT(4,2)',O[4][2],'OPT(6,3)',O[6][3],'OPT(3,6)?',dp(p,6)[3][6],'OPT(6,2)',O[6][2],'OPT(5,3)',O[5][3])
for _ in range(300):
    n=random.randint(2,7);t=random.randint(1,n-1)
    p=sorted(random.sample(range(1,40),n))
    assert brute(p,t)==dp(p,t)[n][t]
print('Q1 dp ok')
# Q2a: BFS depth over all neighbor orders on random undirected graphs
def bfs_depths(G,s,order_seed):
    r=random.Random(order_seed);seen={s:0};q=[s]
    while q:
        u=q.pop(0);nb=list(G[u]);r.shuffle(nb)
        for v in nb:
            if v not in seen:seen[v]=seen[u]+1;q.append(v)
    return max(seen.values())
for _ in range(200):
    G=nx.gnp_random_graph(8,0.3)
    if not nx.is_connected(G):continue
    assert len({bfs_depths(G,0,k) for k in range(30)})==1
print('Q2a true ok')
# Q2b DFS depth on directed s->a,s->b,a->b all orders
def dfs_depth(G,s,order):
    seen=set();best=0
    def go(u,d):
        nonlocal best;seen.add(u);best=max(best,d)
        for v in order(u):
            if v not in seen:go(v,d+1)
    go(s,0);return best
G={'s':['a','b'],'a':['b'],'b':[]}
res={dfs_depth(G,'s',lambda u,o=o:(o if u=='s' else G[u])) for o in (['a','b'],['b','a'])}
print('Q2b depths',res)
# Q3: reverse delete on random graphs with distinct weights
for _ in range(300):
    n=random.randint(3,8);G=nx.gnp_random_graph(n,0.6)
    if not nx.is_connected(G):continue
    ws=random.sample(range(1,1000),G.number_of_edges())
    for (u,v),w in zip(G.edges,ws):G[u][v]['weight']=w
    H=G.copy()
    for u,v,d in sorted(G.edges(data=True),key=lambda e:-e[2]['weight']):
        H.remove_edge(u,v)
        if not nx.is_connected(H):H.add_edge(u,v,weight=d['weight'])
    M=nx.minimum_spanning_tree(G)
    assert H.number_of_edges()==n-1 and set(map(frozenset,H.edges))==set(map(frozenset,M.edges))
print('Q3 ok')
# K4
K=[('A','B',1),('C','D',2),('B','C',3),('A','C',4),('B','D',5),('A','D',6)]
H=nx.Graph();H.add_weighted_edges_from(K)
for u,v,w in sorted(K,key=lambda e:-e[2]):
    H.remove_edge(u,v)
    if not nx.is_connected(H):H.add_edge(u,v,weight=w)
print('K4',H.number_of_edges(),sum(d['weight'] for *_,d in H.edges(data=True)))
# Q4 algorithm
cnt=[0]
def sel(C,k,limit):
    assert len(C)<=limit; return sorted(C)[k-1]
def kth(A,k):
    n=len(A);C=list(A);iters=0;work=0
    while len(C)>n/2:
        iters+=1;N=len(C);work+=N
        C1=C[:N//2];assert C1
        import math
        p=sel(C1,math.ceil(len(C1)/2),n/2)
        L=[x for x in C if x<p];E=[x for x in C if x==p];R=[x for x in C if x>p]
        assert len(L)<=0.75*N+1 and len(R)<=0.75*N+1 and len(L)<N and len(R)<N
        if k<=len(L):C=L
        elif k<=len(L)+len(E):return p,iters,work
        else:k-=len(L)+len(E);C=R
    return sel(C,k,n/2),iters,work
mx=0
for _ in range(20000):
    n=random.randint(3,60);A=[random.randint(1,random.choice([5,100])) for _ in range(n)]
    if random.random()<.5:random.shuffle(A);A=sorted(A) if random.random()<.3 else A
    ks=[k for k in range(1,n+1) if k<n/2]
    for k in ks:
        v,it,w=kth(A,k);assert v==sorted(A)[k-1]
        mx=max(mx,w/n)
for k in range(1,n+1):
    v,_,_=kth(A,k);assert v==sorted(A)[k-1]  # also works for all k
print('Q4 ok, max work/n',mx)
A=[9,3,14,1,12,7,16,5,11,2,15,8,4,13,10,6];print('Q4 step |L|',len([x for x in A if x<7]),kth(A,3))
# Q5 KMP
def pi(P):
    m=len(P);f=[0]*(m+1);k=0
    for q in range(1,m):
        while k>0 and P[k]!=P[q]:k=f[k]
        if P[k]==P[q]:k+=1
        f[q+1]=k
    return f[1:]
print('pi aa',pi('aa'),'ab',pi('ab'),'aba',pi('aba'),'abab',pi('abab'),'aaaa',pi('aaaa'),'aaaaa',pi('aaaaa'))
def fallbacks(P,T):
    f=[0]+pi(P);q=0;c=0;m=len(P)
    for ch in T:
        while q>0 and (q==m or P[q]!=ch):q=f[q];c+=1
        if P[q]==ch:q+=1
    return c
def fallbacks2(P,T):  # CLRS: reset q=pi[m] right after full match
    f=[0]+pi(P);q=0;c=0;m=len(P)
    for ch in T:
        while q>0 and P[q]!=ch:q=f[q];c+=1
        if P[q]==ch:q+=1
        if q==m:q=f[q]
    return c
for nm,T in [('b^n','b'*30),('a^n','a'*30),('(aab)^n/3','aab'*10),('a^{n-1}b','a'*29+'b')]:
    print(nm,'CLRS-reset fallbacks',fallbacks2('aab',T),'lazy-reset',fallbacks('aab',T))
print('b^10 aab',fallbacks2('aab','b'*10))
def naive(P,T):
    c=0
    for s in range(len(T)-len(P)+1):
        for j in range(len(P)):
            c+=1
            if P[j]!=T[s+j]:break
    return c
print('naive 10,5:',naive('aaaab','a'*10),'10,10:',naive('a'*9+'b','a'*9+'b'),naive('a'*9+'b','a'*10 if False else 'a'*10))
