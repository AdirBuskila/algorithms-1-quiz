import itertools, random
P='ABABBAAABABA'
def pi(P):
    p=[0]*len(P);k=0
    for i in range(1,len(P)):
        while k>0 and P[i]!=P[k]:k=p[k-1]
        if P[i]==P[k]:k+=1
        p[i]=k
    return p
def pi_brute(P):
    return [max([k for k in range(0,i+1) if P[:k]==P[i+1-k:i+1] and k<i+1],default=0) for i in range(len(P))]
print('pi',pi(P),pi(P)==pi_brute(P))
# KMP matcher counting comparisons of the text letter 'C' (T[11]) with pattern letters
T='ABABBAAABABC'+'XXXX'
p=pi(P);k=0;m=len(P)
cmps=[]  # (i, j)
i=0
log=[]
while i<len(T):
    # standard CLRS: while k>0 and P[k]!=T[i]: k=pi[k-1]; then if P[k]==T[i] k++
    while True:
        if k==m: k=p[k-1]
        log.append((i,T[i],k,P[k]))
        if T[i]==P[k]:k+=1;break
        if k==0:break
        k=p[k-1]
    i+=1
    if i>11:break
c=[(i,t,k,pk) for (i,t,k,pk) in log if t=='C']
print('comparisons of C:',len(c),c)
# variant: counting only comparisons (loop-form: while k>0 and P[k]!=T[i]) - second common implementation
k=0;cnt=0
for i,t in enumerate(T[:12]):
    while k>0 and P[k]!=t:
        if t=='C':cnt+=1
        k=p[k-1]
    if t=='C':cnt+=1  # comparison for k==0 ... actually the `if P[k]==t` comparison
    if P[k]==t:k+=1
print('variant count (while-test comparisons + final if)',cnt)
# Q4
def L(A):
    n=len(A);d=[1]*n;par=[-1]*n
    for i in range(n):
        for j in range(i):
            if A[i]%A[j]==0 and d[j]+1>d[i]:d[i]=d[j]+1;par[i]=j
    return d,par
A=[1,2,3,4,5,6,8,10,11]
d,par=L(A);print('Q4 table',list(zip(A,d)),'max',max(d))
def brute(A):
    best=0
    for r in range(len(A)+1):
        for S in itertools.combinations(A,r):
            if all(x%y==0 or y%x==0 for x,y in itertools.combinations(S,2)):best=max(best,r)
    return best
print('brute',brute(A),'example 8-set brute',brute([1,2,3,4,5,6,8,10]),[S for S in itertools.combinations([1,2,3,4,5,6,8,10],4) if all(x%y==0 or y%x==0 for x,y in itertools.combinations(S,2))])
for _ in range(300):
    B=sorted(random.sample(range(1,40),random.randint(0,9)))
    if B: assert max(L(B)[0])==brute(B),B
print('Q4 DP verified (distinct sorted)')
print('all optimal sets for A:',[S for S in itertools.combinations(A,4) if all(x%y==0 or y%x==0 for x,y in itertools.combinations(S,2))])
