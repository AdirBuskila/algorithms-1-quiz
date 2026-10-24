import itertools
def trees(n,adj,s):
    B=set();D=set()
    perms=[list(itertools.permutations(adj[v])) for v in range(n)]
    for ch in itertools.product(*perms):
        order=ch
        # BFS
        seen={s};q=[s];t=set()
        while q:
            u=q.pop(0)
            for w in order[u]:
                if w not in seen: seen.add(w);q.append(w);t.add(frozenset((u,w)))
        B.add(frozenset(t))
        seen={s};t=set()
        def dfs(u):
            for w in order[u]:
                if w not in seen: seen.add(w);t.add(frozenset((u,w)));dfs(w)
        dfs(s);D.add(frozenset(t))
    return B,D
bad=0;cnt=0
for n in range(3,5):
    allE=list(itertools.combinations(range(n),2))
    for mask in range(1<<len(allE)):
        E=[allE[i] for i in range(len(allE)) if mask>>i&1]
        if len(E)<n: continue
        adj=[[] for _ in range(n)]
        for a,b in E: adj[a].append(b);adj[b].append(a)
        # connected
        seen={0};st=[0]
        while st:
            u=st.pop()
            for w in adj[u]:
                if w not in seen: seen.add(w);st.append(w)
        if len(seen)<n: continue
        for s in range(n):
            # s on a cycle: some edge at s non-bridge; just test all s
            B,D=trees(n,adj,s);cnt+=1
            if B&D: bad+=1;print("overlap",E,s)
print(cnt,"cases, overlaps:",bad)

# n=5,6 random orders sample
import random
random.seed(1)
bad2=0;cnt2=0
for n in (5,6,7):
  for _ in range(300):
    E=set()
    while True:
        E={tuple(sorted(random.sample(range(n),2))) for _ in range(random.randint(n,2*n))}
        adj=[[] for _ in range(n)]
        for a,b in E: adj[a].append(b);adj[b].append(a)
        seen={0};st=[0]
        while st:
            u=st.pop()
            for w in adj[u]:
                if w not in seen: seen.add(w);st.append(w)
        if len(seen)==n and len(E)>=n: break
    s0=random.randrange(n)
    B=set();D=set()
    for _ in range(300):
        order=[random.sample(a,len(a)) for a in adj]
        seen={s0};q=[s0];t=set()
        while q:
            u=q.pop(0)
            for w in order[u]:
                if w not in seen: seen.add(w);q.append(w);t.add(frozenset((u,w)))
        B.add(frozenset(t))
        seen={s0};t=set()
        def dfs(u):
            for w in order[u]:
                if w not in seen: seen.add(w);t.add(frozenset((u,w)));dfs(w)
        dfs(s0);D.add(frozenset(t))
    cnt2+=1
    if B&D: bad2+=1
print("random",cnt2,"overlaps",bad2)
# explicit: s leaf attached to triangle
