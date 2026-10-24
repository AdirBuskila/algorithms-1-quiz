import random, itertools
random.seed(3)
# Q1
def sq_bf(N):
    # BFS shortest number of squares
    from collections import deque
    d={0:0};q=deque([0])
    while q:
        x=q.popleft()
        k=1
        while x+k*k<=N:
            y=x+k*k
            if y not in d:d[y]=d[x]+1;q.append(y)
            k+=1
    return d[N]
def sq_dp(N):
    f=[0]+[0]*N
    for i in range(1,N+1): f[i]=1+min(f[i-k*k] for k in range(1,int(i**.5)+1))
    return f[N]
assert all(sq_bf(N)==sq_dp(N) for N in range(1,200)); print("Q1 ok", sq_dp(12))
# Q2
def pi(s):
    p=[0]*len(s)
    for i in range(1,len(s)):
        k=p[i-1]
        while k and s[i]!=s[k]: k=p[k-1]
        if s[i]==s[k]:k+=1
        p[i]=k
    return p
def pp_bf(S): return max(l for l in range(1,len(S)+1) if S[:l]==S[:l][::-1])
def pp_kmp(S): return pi(S+'#'+S[::-1])[-1]
for n in range(1,12):
    for t in itertools.product('abc',repeat=n) if n<8 else [tuple(random.choice('ab') for _ in range(n)) for _ in range(300)]:
        S=''.join(t); assert pp_bf(S)==pp_kmp(S),S
print("Q2 ok",pp_bf('aabaac'))
# Q3 pairing: min paid = sum of larger of each pair
def best_pairing(p):
    best=10**9
    def rec(rem,cost):
        nonlocal best
        if not rem: best=min(best,cost);return
        a=rem[0]
        for j in range(1,len(rem)):
            rec(rem[1:j]+rem[j+1:],cost+max(a,rem[j]))
    rec(list(p),0);return best
def greedy(p):
    s=sorted(p,reverse=True);return sum(s[0::2])
for _ in range(500):
    p=[random.randint(1,9) for _ in range(2*random.randint(1,4))]
    assert best_pairing(p)==greedy(p)
print("Q3 ok")
# Q4: find k<m, k>=n/2 occurrences, m>=n/3 occurrences; existence can fail? test candidate method: Misra-Gries 3 counters + verify
def bf4(A):
    n=len(A);from collections import Counter
    c=Counter(A)
    return sorted((k,m) for k in c for m in c if k<m and 2*c[k]>=n and 3*c[m]>=n)
def mg(A,counters):
    C={}
    for x in A:
        if x in C:C[x]+=1
        elif len(C)<counters:C[x]=1
        else:
            for c in list(C):
                C[c]-=1
                if C[c]==0:del C[c]
    return list(C)
miss=0;tot=0
for _ in range(20000):
    n=random.randint(1,12);A=[random.randint(1,4) for _ in range(n)]
    sols=bf4(A)
    if not sols: continue
    tot+=1
    from collections import Counter
    c=Counter(A)
    for cnt in (2,):
        cand=mg(A,cnt)
        ok=any(k in cand and m in cand for k,m in sols)
        if not ok: miss+=1
print("Q4: MG with 2 counters misses (>=n/2,>=n/3 exact thresholds):",miss,"of",tot)
miss=0
for _ in range(20000):
    n=random.randint(1,12);A=[random.randint(1,4) for _ in range(n)]
    sols=bf4(A)
    if not sols: continue
    cand=mg(A,3)
    if not any(k in cand and m in cand for k,m in sols): miss+=1
print("Q4: MG with 3 counters misses:",miss)
