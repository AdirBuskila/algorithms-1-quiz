P="AABAABAABAAA"
pi=[0]*len(P)
for i in range(1,len(P)):
    # brute force
    pi[i]=max(k for k in range(i+1) if k<i+1 and P[:k]==P[i+1-k:i+1] and k<i+1)
print("pi",pi)
# knapsack
items=[(1,1),(2,3),(4,7),(5,10)];T=6
dp=[[0]*(T+1) for _ in range(5)]
for i,(t,v) in enumerate(items,1):
    for w in range(T+1):
        dp[i][w]=dp[i-1][w]
        if w>=t: dp[i][w]=max(dp[i][w],dp[i-1][w-t]+v)
for r in dp:print(r)
# brute
import itertools
best=max((sum(items[i][1] for i in c),c) for k in range(5) for c in itertools.combinations(range(4),k) if sum(items[i][0] for i in c)<=T)
print(best)
print([c for k in range(5) for c in itertools.combinations(range(4),k) if sum(items[i][0] for i in c)<=T and sum(items[i][1] for i in c)==best[0]])
# example from c1
ex=[(2,4),(3,5),(4,10)]
for T in(5,6):
    print(T,max((sum(ex[i][1] for i in c),c) for k in range(4) for c in itertools.combinations(range(3),k) if sum(ex[i][0] for i in c)<=T))
# greedy ratio counterexample sanity: items (1,2) ratio2,(3,5)? T=3: greedy picks ratio 2 then...
