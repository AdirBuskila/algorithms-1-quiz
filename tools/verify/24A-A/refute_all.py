import random, itertools, math
from collections import deque
# Q1a/b on random graphs: brute force walks / shortest paths
def bfs(adj,s):
    d={s:0};q=deque([s])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in d:d[v]=d[u]+1;q.append(v)
    return d
def walk_through(adj,x,y,z):
    d=bfs(adj,z);return x in d and y in d
def walk_brute(adj,x,y,z):
    # state (vertex,seenz): reachability in product graph
    start=(x,x==z);seen={start};q=deque([start])
    while q:
        u,f=q.popleft()
        if u==y and f:return True
        for v in adj[u]:
            s=(v,f or v==z)
            if s not in seen:seen.add(s);q.append(s)
    return False
def short_through(adj,x,y,z):
    dx=bfs(adj,x);dy=bfs(adj,y)
    if y not in dx:return False
    return z in dx and z in dy and dx[z]+dy[z]==dx[y]
def short_brute(adj,x,y,z):
    dx=bfs(adj,x)
    if y not in dx:return False
    L=dx[y];found=False
    def dfs(u,path):
        nonlocal found
        if found or len(path)-1>L:return
        if u==y:
            if len(path)-1==L and z in path:found=True
            return
        for v in adj[u]:
            if v not in path:dfs(v,path+[u] if False else path+[v])
    dfs(x,[x]);return found
ba=bb=0
for _ in range(3000):
    n=random.randint(1,7);adj={i:set() for i in range(n)}
    for i in range(n):
        for j in range(i+1,n):
            if random.random()<0.3:adj[i].add(j);adj[j].add(i)
    x,y,z=[random.randrange(n) for _ in range(3)]
    if walk_through(adj,x,y,z)!=walk_brute(adj,x,y,z):ba+=1
    if short_through(adj,x,y,z)!=short_brute(adj,x,y,z):bb+=1
print('Q1a wrong',ba,'Q1b wrong',bb)
# steps graphs
g={'x':{'u','v'},'u':{'x','y'},'v':{'x','z'},'z':{'v','y'},'y':{'u','z'}}
dx=bfs(g,'x');dy=bfs(g,'y');print('step Q1b',dx['z'],dx['y'],dx['z']+dy['z'])
g2={'x':{'u'},'u':{'x','z'},'z':{'u','v'},'v':{'z','y'},'y':{'v'},'w':set()}
print('step Q1a d[y]',bfs(g2,'z')['y'])
# Q2
def greedy(pts):
    pts=sorted(pts);end=-math.inf;segs=[]
    for p in pts:
        if p>end:segs.append((p,p+1));end=p+1
    return segs
def brute_cover(pts):
    pts=sorted(set(pts))
    # candidate left endpoints: each point (WLOG) ; min k
    for k in range(1,len(pts)+1):
        for comb in itertools.combinations(pts,k):
            if all(any(a<=p<=a+1 for a in comb) for p in pts):return k
ok=True
for _ in range(2000):
    pts=[random.randint(0,12)/2 for _ in range(random.randint(1,7))]
    if len(greedy(pts))!=brute_cover(pts):ok=False
print('Q2 greedy ok',ok,len(greedy([0.2,0.9,1.3,2.5,2.7,5.0])),len(greedy([0,1])),len(greedy([0,.5,3,3.2])))
def greedy_ge(pts):
    pts=sorted(pts);end=-math.inf;n=0
    for p in pts:
        if p>=end:n+=1;end=p+1
    return n
print('>= bug on [0,1]',greedy_ge([0,1]))
# alternatives
def centered(pts):
    pts=sorted(pts);end=-math.inf;n=0
    for p in pts:
        if p>end:n+=1;end=p+.5
    return n
def endsat(pts):
    pts=sorted(pts);end=-math.inf;n=0
    for p in pts:
        if p>end:n+=1;end=p
    return n
print('alt on 0,1,1.9',centered([0,1,1.9]),endsat([0,1,1.9]),'on 0,1',centered([0,1]),endsat([0,1]),'opt',len(greedy([0,1,1.9])),len(greedy([0,1])))
# Q3 exact probabilities
n=10
print('P(correct "different")=',1/n,'P(err equal)=',(n-1)/n)
from math import comb
print('half bits',comb(9,4)/comb(10,5))
print('bits',math.ceil(math.log2(1000))+1,math.ceil(math.log2(1025))+1)
# Q4
def tower_best(L,W,H,desc=True):
    n=len(L);best=0
    for r in range(1,n+1):
        for perm in itertools.permutations(range(n),r):
            if all(L[perm[t]]<L[perm[t+1]] and W[perm[t]]<W[perm[t+1]] for t in range(r-1)):
                best=max(best,sum(H[i] for i in perm))
    return best
def T_dp(L,H):
    n=len(L);T=[0]*(n+1);P=[0]*(n+1);Lx=[math.inf]+list(L);Hx=[0]+list(H)
    for i in range(1,n+1):
        bj=0;bv=-1
        for j in range(0,i):
            if Lx[j]>Lx[i] and T[j]+Hx[i]>bv:bv=T[j]+Hx[i];bj=j
        T[i]=bv;P[i]=bj
    return T,P
L=[8,5,6,3];H=[3,4,2,5];W=[10,8,6,4]  # width descending
T,P=T_dp(L,H);print('T',T,'P',P,'brute',tower_best(L,W,H))
ok=True
for _ in range(500):
    n=random.randint(1,6);Ls=random.sample(range(1,30),n);Ws=sorted(random.sample(range(1,30),n),reverse=True);Hs=random.sample(range(1,30),n)
    T,P=T_dp(Ls,Hs)
    if max(T[1:])!=tower_best(Ls,Ws,Hs):ok=False
    # reconstruct
    i=max(range(1,n+1),key=lambda t:T[t]);tot=0;boxes=[]
    while i:boxes.append(i);tot+=Hs[i-1];i=P[i]
    if tot!=max(T[1:]):ok=False
    for a,b in zip(boxes,boxes[1:]):
        if not(Ls[a-1]<Ls[b-1] and Ws[a-1]<Ws[b-1]):ok=False
print('Q4 dp+reconstruction ok',ok)
# T min-bug
print('min variant max',max(H))
# bonus counterexample
iv=[(0,10),(9,12),(11,20)]
def shortest_first(iv):
    iv=sorted(iv,key=lambda t:t[1]-t[0]);chosen=[]
    for a,b in iv:
        if all(b<c or d<a for c,d in chosen):chosen.append((a,b))
    return len(chosen)
def opt(iv):
    best=0
    for r in range(len(iv)+1):
        for comb_ in itertools.combinations(iv,r):
            if all(a[1]<b[0] or b[1]<a[0] for a,b in itertools.combinations(comb_,2)):best=max(best,r)
    return best
print('bonus',shortest_first(iv),opt(iv))
