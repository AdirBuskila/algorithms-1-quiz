import itertools, random
S1,S2="BADAEAT","CAEADAS"
subs=lambda s:{s[i:j] for i in range(len(s)) for j in range(i+1,len(s)+1)}
com=subs(S1)&subs(S2);L=max(map(len,com));print(L,sorted(x for x in com if len(x)==L))
# Q1 path
def best_path(A):
    n=len(A)
    best=-10**9;
    for choice in itertools.product([0,1],repeat=n-1):
        j=0;s=A[0][0]
        for i,c in enumerate(choice,1): j+=c; s+=A[i][j]
        best=max(best,s)
    return best
def dpv(A):
    n=len(A);f=[[None]*n for _ in range(n)];f[0][0]=A[0][0]
    for i in range(1,n):
        for j in range(i+1):
            c=[f[i-1][jj] for jj in (j,j-1) if 0<=jj<=i-1]
            f[i][j]=A[i][j]+max(c)
    return max(f[n-1])
print(best_path([[1,0,0],[3,2,0],[4,10,12]]),dpv([[1,0,0],[3,2,0],[4,10,12]]))
random.seed(2)
for _ in range(300):
    n=random.randint(1,8);A=[[random.randint(-9,9) if j<=i else 0 for j in range(n)] for i in range(n)]
    assert best_path(A)==dpv(A)
# Q3 table + LV
p=0.3
import fractions
print("probabilities", (1-p)*p, p*(1-p), p*p,(1-p)**2)
random.seed(3);cnt=[0,0];rounds=0
for _ in range(200000):
    while True:
        a=random.random()<p;b=random.random()<p;rounds+=1
        if a!=b: cnt[a]+=1;break
print(cnt, rounds/200000, 1/(2*p*(1-p)))
# Q4 greedy vs DP, powers of 5
def mincoins(W,den):
    INF=10**9;f=[0]+[INF]*W
    for w in range(1,W+1):
        for d in den:
            if d<=w: f[w]=min(f[w],f[w-d]+1)
    return f[W]
def gr(W,den):
    c=0
    for d in sorted(den,reverse=True): c+=W//d;W%=d
    return c
for K in range(1,6):
    den=[5**i for i in range(K)]
    for W in range(0,400): assert mincoins(W,den)==gr(W,den)
print("greedy ok", gr(35,[1,5,25]))
# Q5 greedy set cover ratio not exceeding H(n)
import math
random.seed(5);worst=0
for _ in range(300):
    U=list(range(random.randint(3,10)));m=random.randint(3,8)
    sets=[frozenset(random.sample(U,random.randint(1,len(U)))) for _ in range(m)];Uu=frozenset().union(*sets)
    opt=min(r for r in range(1,m+1) if any(frozenset().union(*c)==Uu for c in itertools.combinations(sets,r)))
    cov=set();g=0
    while cov!=Uu:
        s=max(sets,key=lambda s:len(s-cov));cov|=s;g+=1
    worst=max(worst,g/opt); assert g/opt<=sum(1/i for i in range(1,len(Uu)+1))+1e-9
print("worst ratio",worst)
