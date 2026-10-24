import itertools, random
# Q3 DP vs brute
def brute(d,p,k):
    n=len(d);best=0
    for m in range(1<<n):
        ch=[i for i in range(n) if m>>i&1]
        if all(d[b]-d[a]>=k for a,b in zip(ch,ch[1:])):
            best=max(best,sum(p[i] for i in ch))
    return best
def dp(d,p,k):
    n=len(d);f=[0]*(n+1)
    for i in range(1,n+1):
        j=0
        while j<i-1 and d[j]<=d[i-1]-k: j+=1   # j = count of positions with d<=d_i-k
        pr=sum(1 for x in d[:i-1] if x<=d[i-1]-k)
        f[i]=max(f[i-1],p[i-1]+f[pr])
    return f[n]
def greedy(d,k):
    last=None;c=0
    for x in d:
        if last is None or x-last>=k: c+=1;last=x
    return c
random.seed(1)
for _ in range(2000):
    n=random.randint(1,10);d=sorted(random.sample(range(1,40),n));k=random.randint(1,15)
    p=[random.randint(1,9) for _ in range(n)]
    assert brute(d,p,k)==dp(d,p,k)
    assert brute(d,[1]*n,k)==greedy(d,k)
print("dp/greedy ok")
d=[1,2,15,20,26,27,30,35];k=10
sols=[c for r in range(5) for c in itertools.combinations(d,r) if all(b-a>=k for a,b in zip(c,c[1:]))and r==3]
print(len(sols),sols[:20], (2,20,30) in sols, greedy(d,k), max(len(c) for r in range(9) for c in itertools.combinations(d,r) if all(b-a>=k for a,b in zip(c,c[1:]))))
# Q1 brute: graphs with E_DFS==E_BFS, s not root, indeg,outdeg>0, no loops
def reach(n,adj,s):
    seen={s};st=[s]
    while st:
        u=st.pop()
        for v in adj[u]:
            if v not in seen: seen.add(v);st.append(v)
    return seen
def bfs_edges(n,adj,s):
    seen={s};q=[s];E=set()
    for u in q:
        for v in adj[u]:
            if v not in seen: seen.add(v);q.append(v);E.add((u,v))
    return E
def dfs_edges(n,adj,s):
    seen=set();E=set()
    def go(u):
        seen.add(u)
        for v in adj[u]:
            if v not in seen: E.add((u,v));go(v)
    go(s)
    for u in range(n):
        if u not in seen: go(u)
    return E
res={'a':0,'b':0,'c':0,'bloops':0}
for n in range(1,5):
    pairs=[(i,j) for i in range(n) for j in range(n)]
    for m in range(1<<len(pairs)):
        Es=[pairs[i] for i in range(len(pairs)) if m>>i&1]
        if not Es: continue
        # adjacency order: exhaust orders? use sorted order, plus reversed to vary
        for rev in (False,True):
            adj=[sorted([v for (u,v) in Es if u==x],reverse=rev) for x in range(n)]
            for s in range(n):
                if bfs_edges(n,adj,s)!=dfs_edges(n,adj,s): continue
                notroot=len(reach(n,adj,s))<n
                if not notroot: continue
                res['a']+=1
                indeg=[sum(1 for e in Es if e[1]==x) for x in range(n)];outdeg=[sum(1 for e in Es if e[0]==x) for x in range(n)]
                if all(indeg) and all(outdeg):
                    if any(u==v for u,v in Es): res['bloops']+=1
                    else: res['b']+=1
                if all(indeg[x]+outdeg[x] for x in range(n)): res['c']+=1
print(res)  # a,c counterexamples exist; b without loops must be 0
# Q5
T="XATATAT"
best=max((T[i:j] for i in range(7) for j in range(i+1,8) if T.count(T[i:j])>=1 and sum(T.startswith(T[i:j],t) for t in range(len(T)))>=2),key=len)
print(best)
