import itertools, random
# Q1a counterexample: triangle a,b,c ab=1 bc=3 ac=2, DFS from a taking lightest white edge
def lightest_dfs(adj,start):
    seen={start};T=[]
    def go(u):
        while True:
            cand=[(w,v) for v,w in adj[u] if v not in seen]
            if not cand:return
            w,v=min(cand);seen.add(v);T.append((u,v,w));go(v)
    go(start);return T
adj={'a':[('b',1),('c',2)],'b':[('a',1),('c',3)],'c':[('a',2),('b',3)]}
T=lightest_dfs(adj,'a');print('DFS tree',T,'weight',sum(w for *_,w in T),'MST weight 3')
# random: how often is lightest-DFS tree an MST (w/ distinct weights) -> False exists
def mst_w(n,E):
    par=list(range(n))
    def f(x):
        while par[x]!=x:x=par[x]
        return x
    t=0
    for w,u,v in sorted(E):
        a,b=f(u),f(v)
        if a!=b:par[a]=b;t+=w
    return t
bad=0
for _ in range(2000):
    n=random.randint(3,6);E=[(w,u,v) for w,(u,v) in zip(random.sample(range(1,100),n*(n-1)//2),itertools.combinations(range(n),2)) if random.random()<.8 or True]
    adj={i:[] for i in range(n)}
    for w,u,v in E:adj[u].append((v,w));adj[v].append((u,w))
    T=lightest_dfs(adj,0)
    if sum(w for *_,w in T)!=mst_w(n,E):bad+=1
print('Q1a: random complete graphs where lightest-DFS tree not MST:',bad,'/2000')
# Q1b: component property, brute force
def compcheck():
    for _ in range(500):
        n=random.randint(2,8);E=[e for e in itertools.combinations(range(n),2) if random.random()<.3]
        adj={i:set() for i in range(n)}
        for u,v in E:adj[u].add(v);adj[v].add(u)
        comp={}
        for s in range(n):
            if s in comp:continue
            st=[s];comp[s]=s
            while st:
                x=st.pop()
                for y in adj[x]:
                    if y not in comp:comp[y]=s;st.append(y)
        # any path from x to y: all path vertices connected to x => same comp
        for x in range(n):
            for y in range(n):
                if comp[x]==comp[y]:
                    # enumerate simple paths
                    def paths(u,seen):
                        if u==y:yield seen;return
                        for v in adj[u]:
                            if v not in seen:yield from paths(v,seen|{v})
                    for p in paths(x,{x}):
                        if any(comp[v]!=comp[x] for v in p):return False
    return True
print('Q1b true on random graphs:',compcheck())
# Q2
D=[1,9,4,2,4];K=10
def best(D,K):
    m=0;sols=[]
    for r in range(len(D)+1):
        for S in itertools.combinations(range(len(D)),r):
            if sum(D[i] for i in S)<=K:
                if r>m:m=r;sols=[]
                if r==m:sols.append(S)
    return m,sols
m,s=best(D,K);print('Q2 max children',m,'optimal sets (indices)',s)
def greedy(D,K):
    c=0;t=0
    for d in sorted(D):
        if t+d<=K:t+=d;c+=1
        else:break
    return c
for _ in range(3000):
    D=[random.randint(1,9) for _ in range(random.randint(0,7))];K=random.randint(0,25)
    assert greedy(D,K)==best(D,K)[0]
print('Q2 greedy verified')
# Q3a(i) tree & Q3a(ii)
def alltrees(items):
    res=set()
    def rec(items):
        if len(items)==1:res.add(items[0][1]);return
        items=sorted(items,key=lambda x:x[0]);w=[x[0] for x in items]
        for i in range(len(items)):
            for j in range(len(items)):
                if i!=j and sorted([w[i],w[j]])==w[:2] and True:
                    rest=[items[k] for k in range(len(items)) if k not in(i,j)]
                    # (left,right) = (i,j): record ordered pair
                    rec(rest+[(w[i]+w[j],(items[i][1],items[j][1]))])
    rec(items);return res
def cdict(t,p=''):
    if isinstance(t,str):return {t:p}
    d={};d.update(cdict(t[0],p+'0'));d.update(cdict(t[1],p+'1'));return d
target={'a':'011','b':'010','c':'00','d':'10','e':'11'}
# unordered target shape check: allow any ordering? first: strict left<=right convention:
def wt(t,f):
    return f[t] if isinstance(t,str) else wt(t[0],f)+wt(t[1],f)
def ordered_ok(t,f):
    if isinstance(t,str):return True
    return wt(t[0],f)<=wt(t[1],f) and ordered_ok(t[0],f) and ordered_ok(t[1],f)
print('Q3a(ii): values of d for which SOME Huffman tie-break gives the exact code (left<=right):')
res={}
for d in range(1,15):
    f={'a':5,'b':2,'c':5,'e':7,'d':d}
    ok=[t for t in alltrees([(w,s) for s,w in f.items()]) if cdict(t)==target]
    # also unordered (shape) match
    def shp(t):return 'L' if isinstance(t,str) else '('+''.join(sorted([shp(t[0]),shp(t[1])]))+')'
    tshape=None
    res[d]=bool(ok)
    # optimal cost check
    lens={k:len(v) for k,v in target.items()}
    cost=sum(f[k]*lens[k] for k in f)
    hcost=sum(wt(t,f) for t in [None]) if False else None
    # huffman cost
    import heapq
    h=list(f.values());heapq.heapify(h);hc=0
    while len(h)>1:
        x=heapq.heappop(h);y=heapq.heappop(h);hc+=x+y;heapq.heappush(h,x+y)
    print(' d=%2d exact-code obtainable(any tiebreak, any left/right order)=%s ; code cost %d, Huffman cost %d%s'%(d,bool(ok),cost,hc,' (optimal)' if cost==hc else ''))
# with convention left<=right and ties
print('with left<=right convention (d<=7 forced by sibling e=7):',{d for d in range(1,15) if res[d] and d<=7})
