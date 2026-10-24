import random, itertools, heapq
from fractions import Fraction
random.seed(2)
# Q1 min cuts
def mincut_dp(n,T):
    INF=10**9;f=[0]+[INF]*n
    for j in range(1,n+1):
        for i in range(1,j+1):
            if T(i,j): f[j]=min(f[j],f[i-1]+1)
    return f[n]
def mincut_bf(n,T):
    best=INF=10**9
    for mask in range(1<<(n-1)):
        cuts=[0]+[i+1 for i in range(n-1) if mask>>i&1]+[n]
        if all(T(cuts[k]+1,cuts[k+1]) for k in range(len(cuts)-1)): best=min(best,len(cuts)-1)
    return best
for _ in range(300):
    n=random.randint(1,9)
    tab={(i,j):random.random()<0.4 for i in range(1,n+1) for j in range(i,n+1)}
    for i in range(1,n+1): tab[i,i]=True  # ensure legal
    T=lambda i,j:tab[i,j]
    assert mincut_dp(n,T)==mincut_bf(n,T)
print("Q1 ok")
# Q2 lines through origin
def best_line(pts):
    z=sum(1 for p in pts if p==(0,0)); cnt={}
    for x,y in pts:
        if (x,y)==(0,0): continue
        from math import gcd
        g=gcd(abs(x),abs(y)); x//=g;y//=g
        if x<0 or (x==0 and y<0): x,y=-x,-y
        cnt[(x,y)]=cnt.get((x,y),0)+1
    return z+max(cnt.values(),default=0)
def misra(pts,k):  # k-1 counters; candidates for >n/k
    C={}
    def same(p,q): return p[0]*q[1]==p[1]*q[0]
    for p in pts:
        if p==(0,0): continue
        for c in C:
            if same(c,p): C[c]+=1;break
        else:
            if len(C)<k-1: C[p]=1
            else:
                for c in list(C):
                    C[c]-=1
                    if C[c]==0: del C[c]
    return list(C)
def decide(pts,frac,k):
    n=len(pts); cands=misra(pts,k)
    z=sum(1 for p in pts if p==(0,0))
    def same(p,q): return p[0]*q[1]==p[1]*q[0]
    for c in cands:
        if (sum(1 for p in pts if p!=(0,0) and same(c,p))+z)*100>=frac*n: return True
    return (z*100>=frac*n)
bad=0;badnoorigin=0
for _ in range(3000):
    n=random.randint(1,12)
    pts=[(random.randint(-2,2),random.randint(-2,2)) for _ in range(n)]
    truth=best_line(pts)*100>=51*n
    truth34=best_line(pts)*100>=34*n
    if decide(pts,51,2)!=truth: bad+=1
    if decide(pts,34,3)!=truth34: bad+=1
print("Q2 plain-misra mismatches (with origin pts allowed):",bad)
bad=0
for _ in range(3000):
    n=random.randint(1,12)
    pts=[(random.randint(-2,2),random.randint(-2,2)) for _ in range(n)]
    pts=[p for p in pts if p!=(0,0)]
    n=len(pts)
    if not n: continue
    if decide(pts,51,2)!=(best_line(pts)*100>=51*n): bad+=1
    if decide(pts,34,3)!=(best_line(pts)*100>=34*n): bad+=1
print("Q2 no origin mismatches:",bad)
# Q3 mismatch problem via complement KMP
def mism_bf(T,P):
    n,m=len(T),len(P);return [i for i in range(n-m+1) if all(P[j]!=T[i+j] for j in range(m))]
def pi(s):
    p=[0]*len(s)
    for i in range(1,len(s)):
        k=p[i-1]
        while k and s[i]!=s[k]: k=p[k-1]
        if s[i]==s[k]:k+=1
        p[i]=k
    return p
def kmp_all(T,P):
    s=P+'#'+T;p=pi(s);m=len(P)
    return [i-2*m for i in range(len(s)) if p[i]==m]
for _ in range(2000):
    n=random.randint(1,14);m=random.randint(1,n)
    T=''.join(random.choice('ab') for _ in range(n));P=''.join(random.choice('ab') for _ in range(m))
    comp=P.translate(str.maketrans('ab','ba'))
    assert mism_bf(T,P)==kmp_all(T,comp)
print("Q3 ok")
# Q4 ropes
def huff(a):
    h=list(a);heapq.heapify(h);c=0
    while len(h)>1:
        x=heapq.heappop(h);y=heapq.heappop(h);c+=x+y;heapq.heappush(h,x+y)
    return c
def bf(a):
    from functools import lru_cache
    @lru_cache(None)
    def g(t):
        if len(t)==1:return 0
        b=10**9
        for i,j in itertools.combinations(range(len(t)),2):
            r=[t[k] for k in range(len(t)) if k not in (i,j)]+[t[i]+t[j]]
            b=min(b,t[i]+t[j]+g(tuple(sorted(r))))
        return b
    return g(tuple(sorted(a)))
print(huff([4,3,2,6]),bf([4,3,2,6]))
for _ in range(300):
    a=[random.randint(1,9) for _ in range(random.randint(1,6))]
    assert huff(a)==bf(a)
print("Q4 ok")
