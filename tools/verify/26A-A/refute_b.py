import itertools
from fractions import Fraction
f={'a':22,'b':15,'c':3,'d':24,'e':4,'f':10,'g':8}
names=list(f)
best=None;opt=[]
for L in itertools.product(range(1,7),repeat=7):
    if sum(Fraction(1,2**l) for l in L)!=1: continue
    c=sum(f[n]*l for n,l in zip(names,L))
    if best is None or c<best: best=c;opt=[L]
    elif c==best: opt.append(L)
print('optimal cost',best,'#optimal length vectors',len(opt))
for L in opt: print(dict(zip(names,L)))
print('f lengths',{L[names.index('f')] for L in opt},'a',{L[0] for L in opt},'d',{L[3] for L in opt})
# official code
code={'a':'01','b':'111','c':'0000','d':'10','e':'0001','f':'110','g':'001'}
print('official cost',sum(f[k]*len(v) for k,v in code.items()),'prefix-free',not any(x!=y and y.startswith(x) for x in code.values() for y in code.values()))
# Q5c
T='aaaaaaaaaaaaaaaaaaaaaaaaab';P='aaaaaab'
cmp=0
for s in range(len(T)-len(P)+1):
    for j in range(len(P)):
        cmp+=1
        if T[s+j]!=P[j]:break
print('naive comparisons',cmp,len(T),len(P))
# Q5b inner loop iterations
def pi(P):
    p=[0]*len(P);k=0
    for i in range(1,len(P)):
        while k>0 and P[i]!=P[k]:k=p[k-1]
        if P[i]==P[k]:k+=1
        p[i]=k
    return p
print('pi ABB',pi('ABB'),'AAB',pi('AAB'),'ABA',pi('ABA'),'ABC',pi('ABC'))
def inner(P,T):
    p=pi(P);k=0;mx=0
    for c in T:
        it=0
        while k>0 and (k==len(P) or c!=P[k]):k=p[k-1];it+=1
        if c==P[k]:k+=1
        mx=max(mx,it)
    return mx
print('inner iterations P=a^6,T=aaaaab',inner('aaaaaa','aaaaab'))
# Q4c max iterations n=1024
def iters(n,k,A):
    low,high=0,n-1;c=0
    while low<=high:
        c+=1;mid=(low+high)//2
        if A[mid]-(mid+1)<k:low=mid+1
        else:high=mid-1
    return c
mx=0
for n in (1024,):
    for A in ([i+1 for i in range(n)],[2*i+5 for i in range(n)]):
        for k in range(1,3000):mx=max(mx,iters(n,k,A))
print('max loop iterations n=1024',mx)
# findbug check
def bug(A,k):
    low,high=0,len(A)-1
    while low<=high:
        mid=(low+high)//2
        if A[mid]-(mid+1)<=k:low=mid+1
        else:high=mid-1
    return low+k
print('bug version [2,3,4,7,11],3 ->',bug([2,3,4,7,11],3))
# Q2 family for even n
import itertools,random
def check(n):
    E=list(itertools.combinations(range(n),2))
    W={};c=0
    for e in E:
        if e[0]%2==0 and e[1]==e[0]+1: W[e]=e[0]//2+1
    c=n
    for e in E:
        if e not in W:c+=1;W[e]=c
    par=list(range(n))
    def find(x):
        while par[x]!=x:x=par[x]
        return x
    T=set()
    for w,e in sorted((w,e) for e,w in W.items()):
        a,b=find(e[0]),find(e[1])
        if a!=b:par[a]=b;T.add(e)
    mins={u:min((e for e in E if u in e),key=lambda e:W[e]) for u in range(n)}
    spec=set(mins.values())
    return len(T-spec)
print('non-special MST edges in matching family:',{n:check(n) for n in range(4,21,2)})
