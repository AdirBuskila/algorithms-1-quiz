import random, itertools
random.seed(4)
# Q1 LPS
def lps_bf(S):
    n=len(S);best=0
    for mask in range(1<<n):
        s=''.join(S[i] for i in range(n) if mask>>i&1)
        if s==s[::-1] and len(s)>best:best=len(s)
    return best
def lps_dp(S):
    n=len(S);f=[[0]*n for _ in range(n)]
    for i in range(n-1,-1,-1):
        f[i][i]=1
        for j in range(i+1,n):
            f[i][j]=2+(f[i+1][j-1] if i+1<=j-1 else 0) if S[i]==S[j] else max(f[i+1][j],f[i][j-1])
    return f[0][n-1]
for _ in range(500):
    S=''.join(random.choice('abc') for _ in range(random.randint(1,11)))
    assert lps_bf(S)==lps_dp(S)
print("Q1 ok",lps_dp("BARCAR"))
# palindromic subseq enumerate for BARCAR
S="BARCAR";n=len(S);res=set()
for mask in range(1<<n):
    s=''.join(S[i] for i in range(n) if mask>>i&1)
    if len(s)==3 and s==s[::-1]:res.add(s)
print(res)
# Q2 rotation
def rot_bf(a,b): return len(a)==len(b) and any(a[k:]+a[:k]==b for k in range(1,len(a)+1))
for n in range(1,9):
    for t in itertools.product('ab',repeat=n):
        a=''.join(t)
        for u in itertools.product('ab',repeat=n):
            b=''.join(u)
            assert rot_bf(a,b)==(b in a+a)
print("Q2 ok (T2 in T1*T1)")
# Q3 Freivalds error prob: worst-case over C != AB with r in {0,1}^n and range
import numpy as np
worst=0
for _ in range(2000):
    n=random.randint(2,4)
    A=np.random.randint(0,4,(n,n));B=np.random.randint(0,4,(n,n))
    C=A@B
    i,j=random.randrange(n),random.randrange(n);C[i,j]+=random.randint(1,3)
    cnt=0;tot=0
    for r in itertools.product((0,1),repeat=n):
        r=np.array(r);tot+=1
        if (A@(B@r)==C@r).all():cnt+=1
    worst=max(worst,cnt/tot)
print("Freivalds worst err",worst)
# Q5 suffix trie banana
s="banana$";nodes=0
trie={}
cnt=1
for i in range(len(s)):
    t=trie
    for ch in s[i:]:
        if ch not in t:t[ch]={};cnt+=1
        t=t[ch]
print("trie nodes with $",cnt,"without $", end=' ')
s2="banana";trie={};c2=1
for i in range(len(s2)):
    t=trie
    for ch in s2[i:]:
        if ch not in t:t[ch]={};c2+=1
        t=t[ch]
print(c2)
