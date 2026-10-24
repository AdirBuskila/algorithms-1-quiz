import random, itertools, heapq
from collections import Counter
M=[[0,1,1,0,1,1],[0,0,1,0,0,0],[1,0,0,0,0,0],[1,1,0,0,0,1],[1,1,0,0,0,0]]
n,m=5,6
def Tbf(i,j):
    best=0
    for s in range(1,min(i,j)+2):
        if all(M[a][b]==0 for a in range(i-s+1,i+1) for b in range(j-s+1,j+1)): best=s
    return best
T=[[Tbf(i,j) for j in range(m)] for i in range(n)]
for r in T:print(r)
print("max",max(map(max,T)))
# recurrence check
def Tr(i,j):
    if M[i][j]==1:return 0
    if i==0 or j==0:return 1
    return 1+min(Tr(i-1,j),Tr(i,j-1),Tr(i-1,j-1))
assert all(Tr(i,j)==T[i][j] for i in range(n) for j in range(m))
for _ in range(500):
    n2,m2=random.randint(1,6),random.randint(1,6)
    M=[[random.randint(0,1) for _ in range(m2)] for _ in range(n2)];n,m=n2,m2
    assert all(Tr(i,j)==Tbf(i,j) for i in range(n) for j in range(m))
# Q2 greedy: decrement max count k times  vs brute force on small strings
def val(c):return sum(v*v for v in c.values())
def greedy(S,k):
    c=Counter(S);h=[-v for v in c.values()];heapq.heapify(h)
    for _ in range(k):
        x=heapq.heappop(h);heapq.heappush(h,x+1)
    return sum(x*x for x in h)
def brute(S,k):
    best=10**9
    for rem in itertools.combinations(range(len(S)),k):
        r=''.join(ch for i,ch in enumerate(S) if i not in rem);best=min(best,val(Counter(r)))
    return best
for _ in range(2000):
    L=random.randint(2,9);S=''.join(random.choice('abc') for _ in range(L));k=random.randint(1,L-1)
    assert greedy(S,k)==brute(S,k),(S,k)
print("greedy ok", greedy("character",2), brute("character",2))
# Q3 inversions
def inv(A):
    if len(A)<=1:return A,0
    h=len(A)//2;l,a=inv(A[:h]);r,b=inv(A[h:]);i=j=c=0;o=[]
    while i<len(l) and j<len(r):
        if l[i]<=r[j]:o.append(l[i]);i+=1
        else:o.append(r[j]);j+=1;c+=len(l)-i
    return o+l[i:]+r[j:],a+b+c
for _ in range(2000):
    A=[random.randint(-5,5) for _ in range(random.randint(0,10))]
    assert inv(A)[1]==sum(A[i]>A[j] for i in range(len(A)) for j in range(i+1,len(A)))
print("inv ok",inv([30,10,40,20])[1])
# Q4 almost-match via Z
def zf(s):
    n=len(s);z=[0]*n;l=r=0
    for i in range(1,n):
        if i<r:z[i]=min(r-i,z[i-l])
        while i+z[i]<n and s[z[i]]==s[i+z[i]]:z[i]+=1
        if i+z[i]>r:l,r=i,i+z[i]
    return z
def almost(T,P):
    n,m=len(T),len(P)
    z=zf(P+'\x00'+T)
    pre=[z[m+1+i] for i in range(n)]            # lcp(P,T[i:])
    zr=zf(P[::-1]+'\x00'+T[::-1])
    # suf[e]=longest common suffix of P and T[:e+1]
    suf=[zr[m+1+(n-1-e)] for e in range(n)]
    out=[]
    for i in range(n-m+1):
        l=min(pre[i],m)
        if l>=m or l+1+suf[i+m-1]>=m: out.append(i)
    return out
def abf(T,P):
    m=len(P);return [i for i in range(len(T)-m+1) if sum(T[i+t]!=P[t] for t in range(m))<=1]
for _ in range(20000):
    n=random.randint(2,12);m=random.randint(1,n-1)
    T=''.join(random.choice('ab') for _ in range(n));P=''.join(random.choice('ab') for _ in range(m))
    assert almost(T,P)==abf(T,P),(T,P)
print("almost ok")
# bonus: bipartite poly; connectivity via BFS
