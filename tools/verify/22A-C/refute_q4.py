import random, itertools, math
from collections import Counter
def alg(A):
    n=len(A);S=sorted(A);h=math.ceil(n/2);t=math.ceil(n/3)
    Kc={S[q-1] for q in range(h,n+1,h)};Mc={S[q-1] for q in range(t,n+1,t)}
    c=Counter(A)
    for k in sorted(Kc):
        for m in sorted(Mc):
            if k<m and 2*c[k]>=n and 3*c[m]>=n: return (k,m)
    return None
def bf(A):
    n=len(A);c=Counter(A)
    return [(k,m) for k in c for m in c if k<m and 2*c[k]>=n and 3*c[m]>=n]
random.seed(5)
for _ in range(40000):
    n=random.randint(1,15);A=[random.randint(1,4) for _ in range(n)]
    s=bf(A);r=alg(A)
    assert (r is None)==(not s) and (r is None or r in s),(A,r,s)
print("Q4 alg ok; example",alg([2,1,1,3,1,2,1,2,1]))
