import random, itertools
from collections import Counter
from math import ceil
def pi(P):
    p=[0]*len(P)
    for i in range(1,len(P)):
        k=p[i-1]
        while k and P[i]!=P[k]:k=p[k-1]
        if P[i]==P[k]:k+=1
        p[i]=k
    return p
for s in ['abbbbb','abbbba','aabbba','abbbab','abaaba','abaabb']: print(s,pi(s))
def truth(A):
    n=len(A);c=Counter(A);v=sorted(c);need=ceil(n/2)
    return any(c[v[i]]+c[v[i+1]]>=need for i in range(len(v)-1))
def make(thr_ge=True,two=True,bug=False):
    def Check(A,M):
        n=len(A);need=ceil(n/2);cm=A.count(M)
        if need<=cm<n: return True
        sm=[a for a in A if a<M]
        if sm:
            L=max(sm);cl=A.count(L)
            if (cl+cm>n/2) if bug else (cl+cm>=need): return True
        lg=[a for a in A if a>M]
        if lg:
            R=min(lg);cr=A.count(R)
            if cr+cm>=need: return True
        return False
    def Pair(A):
        n=len(A);s=sorted(A)
        M1=s[ceil(n/2)-1];M2=s[n//2]
        return Check(A,M1) or Check(A,M2)
    return Pair
good=make();bugged=make(bug=True)
bad=0;badb=0
for _ in range(30000):
    n=random.randint(2,10);A=[random.randint(1,7) for _ in range(n)]
    t=truth(A)
    if good(A)!=t:bad+=1
    if bugged(A)!=t:badb+=1
print('claimed algorithm wrong on',bad,'| bug variant wrong on',badb)
print('bug on [1,1,3,4,5,6]',bugged([1,1,3,4,5,6]),truth([1,1,3,4,5,6]))
# printed original: M=Select((n+1)/2) (use floor and ceil readings), cond > n/2
def orig(A,rd):
    n=len(A);s=sorted(A);M=s[rd(n)-1]
    cm=A.count(M)
    if ceil(n/2)<=cm<n:return True
    sm=[a for a in A if a<M]
    if sm and A.count(max(sm))+cm>n/2:return True
    lg=[a for a in A if a>M]
    if lg and A.count(min(lg))+cm>n/2:return True
    return False
for name,rd in (('floor',lambda n:(n+1)//2),('ceil',lambda n:-(-(n+1)//2))):
    print('printed original',name,'[1,2,3,4]',orig([1,2,3,4],rd),'truth',truth([1,2,3,4]),'[1,2,3,4,5,5]',orig([1,2,3,4,5,5],rd),truth([1,2,3,4,5,5]))
# Q3 / Q4 verified in refute_blind
print('abbbab',pi('abbbab')[-1])
