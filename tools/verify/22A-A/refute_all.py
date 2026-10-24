import random, itertools
random.seed(1)
# Q1 LCS3
def lcs3_bf(a,b,c):
    best=0
    n=len(a)
    for mask in range(1<<n):
        s=''.join(a[i] for i in range(n) if mask>>i&1)
        def sub(s,t):
            it=iter(t); return all(ch in it for ch in s)
        if len(s)>best and sub(s,b) and sub(s,c): best=len(s)
    return best
def lcs3(a,b,c):
    f={}
    def F(i,j,k):
        if i==0 or j==0 or k==0: return 0
        if (i,j,k) in f: return f[i,j,k]
        if a[i-1]==b[j-1]==c[k-1]: r=1+F(i-1,j-1,k-1)
        else: r=max(F(i-1,j,k),F(i,j-1,k),F(i,j,k-1))
        f[i,j,k]=r;return r
    return F(len(a),len(b),len(c))
for _ in range(300):
    n=random.randint(1,8)
    a,b,c=[''.join(random.choice('abc') for _ in range(n)) for _ in range(3)]
    assert lcs3(a,b,c)==lcs3_bf(a,b,c)
print("Q1 ok")
# Q2 periodic
def per_bf(A):
    n=len(A)
    return any(n%d==0 and A==A[:d]*(n//d) for d in range(1,n//2+1))
def pi(s):
    p=[0]*len(s)
    for i in range(1,len(s)):
        k=p[i-1]
        while k and s[i]!=s[k]: k=p[k-1]
        if s[i]==s[k]:k+=1
        p[i]=k
    return p
def per_pi(A):
    n=len(A);p=pi(A)[-1]
    return p>0 and n%(n-p)==0
def per_kmp(A):
    return (A in (A+A)[1:-1])
for n in range(1,13):
    for t in itertools.product('ab',repeat=n):
        A=''.join(t)
        assert per_bf(A)==per_pi(A)==per_kmp(A),A
print("Q2 ok")
# Q4 greedy
def bf4(A):
    best=None
    for idx in itertools.product(range(len(A[0])),repeat=len(A)):
        v=[A[i][j] for i,j in enumerate(idx)]
        if all(v[i]<v[i+1] for i in range(len(v)-1)):
            s=sum(v); best=s if best is None or s>best else best
    return 0 if best is None else best
def gr4(A):
    cur=max(A[-1]);tot=cur
    for arr in reversed(A[:-1]):
        c=[x for x in arr if x<cur]
        if not c: return 0
        cur=max(c);tot+=cur
    return tot
print(bf4([[-3,-4,-8,-1],[20,17,-8,9],[-7,4,3,19]]),gr4([[-3,-4,-8,-1],[20,17,-8,9],[-7,4,3,19]]))
for _ in range(2000):
    m=random.randint(1,4);n=random.randint(1,4)
    A=[[random.randint(-5,8) for _ in range(n)] for _ in range(m)]
    assert bf4(A)==gr4(A),A
print("Q4 ok")
# Q3 polynomial identity: Schwartz-Zippel bound n-1/|S|
# Q5 done separately
