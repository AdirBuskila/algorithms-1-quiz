import random, itertools
def select(A,k): return sorted(A)[k-1]
def alg(A,k,fixed=True):
    n=len(A)
    B=[];C=[]
    if k<n-k:
        S=select(A,k)
        for a in A:
            (C if a>S else B).append(a)
    else:
        S=select(A,n-k) if fixed else select(A,k)
        for a in A:
            (B if a>S else C).append(a)
    return B,C
def best(A,k):
    return max(abs(sum(c)-(sum(A)-sum(c))) for c in itertools.combinations(A,k))
bad=badorig=sizebad=0
for _ in range(4000):
    n=random.randint(2,8);A=random.sample(range(1,40),n);k=random.randint(1,n-1)
    B,C=alg(A,k)
    if len(B)!=k or abs(sum(B)-sum(C))!=best(A,k): bad+=1
    B,C=alg(A,k,False)
    if len(B)!=k: sizebad+=1
    if len(B)!=k or abs(sum(B)-sum(C))!=best(A,k): badorig+=1
print('corrected code wrong:',bad,'| printed original wrong size:',sizebad,'wrong diff/size:',badorig)
B,C=alg([13,5,7],2,False);print('orig on [13,5,7],2',B,C,abs(sum(B)-sum(C)))
B,C=alg([13,5,7],2);print('fixed',B,C,abs(sum(B)-sum(C)))
# findbug variant: condition flipped
def alg_flip(A,k):
    n=len(A)
    if k>n-k:
        S=select(A,k);B=[];C=[]
        for a in A:(C if a>S else B).append(a)
    else:
        S=select(A,n-k);B=[];C=[]
        for a in A:(B if a>S else C).append(a)
    return B,C
B,C=alg_flip([8,4,5,2,10],2);print('flipped on example',abs(sum(B)-sum(C)))
print('steps',best([13,5,7],2),best([1,2,3,4,5,10],2),best([1,2,3,4,10],3),best([8,4,5,2,10],2))
# Q4 recursion vs brute
def C4(A,k):
    A=sorted(A);n=len(A)
    from functools import lru_cache
    @lru_cache(None)
    def c(i,j):
        if A[j]-A[i]<=k: return 0
        return 1+min(c(i+1,j),c(i,j-1))
    return c(0,n-1)
def minrem(A,k):
    A=sorted(A);bestw=0
    for i in range(len(A)):
        for j in range(i,len(A)):
            if A[j]-A[i]<=k:bestw=max(bestw,j-i+1)
    return len(A)-bestw
print('Q4 formula ok',all(C4(A,k)==minrem(A,k) for A,k in [(random.sample(range(0,30),random.randint(1,8)),random.randint(0,8)) for _ in range(3000)]))
A=[1,2,5,6,8];k=2
from functools import lru_cache
@lru_cache(None)
def c(i,j):
    if A[j]-A[i]<=k:return 0
    return 1+min(c(i+1,j),c(i,j-1))
for i in range(5): print([c(i,j) if j>=i else 'X' for j in range(5)])
print('official printed C(2,6)=2? true',c(1,3),'C(6,8) true',c(3,4))
# bug variant with <
@lru_cache(None)
def cb(i,j):
    if A[j]-A[i]<k:return 0
    return 1+min(cb(i+1,j),cb(i,j-1))
A2=[1,5]
print('count check',len([1 for i in range(5) for j in range(i,5)]))
