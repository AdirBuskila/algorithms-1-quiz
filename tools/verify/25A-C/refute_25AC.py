import random, itertools, math
from fractions import Fraction
# Q1: brute-force alignment distance vs DP
def d(a,b): return sum(x!=y for x,y in zip(a,b))
def brute(S1,S2):
    # try all alignments with gap placements up to total length n1+n2 (both gaps columns never help but allowed)
    n1,n2=len(S1),len(S2);best=99
    for m in range(max(n1,n2),n1+n2+1):
        for g1 in itertools.combinations(range(m),m-n1):
            T1=[];it=iter(S1)
            for i in range(m):T1.append('-' if i in g1 else next(it))
            for g2 in itertools.combinations(range(m),m-n2):
                T2=[];it=iter(S2)
                for i in range(m):T2.append('-' if i in g2 else next(it))
                best=min(best,sum(0 if x==y else 1 for x,y in zip(T1,T2)))
    return best
def opt(S1,S2):
    n1,n2=len(S1),len(S2);O=[[0]*(n2+1) for _ in range(n1+1)]
    for i in range(n1+1):O[i][0]=i
    for j in range(n2+1):O[0][j]=j
    for i in range(1,n1+1):
        for j in range(1,n2+1):
            if S1[i-1]==S2[j-1]:O[i][j]=O[i-1][j-1]
            else:O[i][j]=1+min(O[i-1][j-1],O[i-1][j],O[i][j-1])
    return O
for _ in range(300):
    a=''.join(random.choice('ACG') for _ in range(random.randint(0,5)));b=''.join(random.choice('ACG') for _ in range(random.randint(0,5)))
    assert brute(a,b)==opt(a,b)[len(a)][len(b)],(a,b)
print('Q1 ok; example',opt('AGCTTACG','ACTTAACG')[8][8],'AGC/ACT',opt('AGC','ACT')[3][3],'brute ex',brute('AGCT','ACTT'))
# Q2 fractional knapsack greedy vs LP brute (compare to alt orders)
def greedy(V,W,C,key):
    idx=sorted(range(len(V)),key=key);room=Fraction(C);tot=Fraction(0)
    for i in idx:
        t=min(Fraction(W[i]),room);tot+=Fraction(V[i])*t/W[i];room-=t
    return tot
from scipy.optimize import linprog
bad={'val':0,'wtasc':0,'wtdesc':0}
for _ in range(500):
    n=random.randint(1,6);V=[random.randint(1,20) for _ in range(n)];W=[random.randint(1,10) for _ in range(n)];C=random.randint(1,40)
    r=linprog([-v for v in V],A_ub=[W],b_ub=[C],bounds=[(0,1)]*n)
    g=greedy(V,W,C,lambda i:-Fraction(V[i],W[i]));assert abs(float(g)+r.fun)<1e-6
    if greedy(V,W,C,lambda i:-V[i])<g:bad['val']+=1
    if greedy(V,W,C,lambda i:W[i])<g:bad['wtasc']+=1
    if greedy(V,W,C,lambda i:-W[i])<g:bad['wtdesc']+=1
print('Q2 ok; wrong criteria fail counts',bad,'example',greedy([60,100,120],[10,20,30],50,lambda i:-Fraction([60,100,120][i],[10,20,30][i])))
# Q3
calls=[0]
def search(nums,t,lo,hi,var='ok'):
    calls[0]+=1
    if calls[0]>200:raise RecursionError
    if lo>hi:return -1
    mid=(lo+hi)//2
    if nums[mid]==t:return mid
    if nums[lo]<=nums[mid]:
        c=(nums[lo]<=t<nums[mid]) if var!='bug' else (nums[lo]<=t<=nums[hi])
        return search(nums,t,lo,mid-1,var) if c else search(nums,t,mid+1,hi,var)
    else:
        if nums[mid]<t<=nums[hi]:return search(nums,t,mid+1,hi,var)
        return search(nums,t,lo,mid-1,var)
for _ in range(2000):
    n=random.randint(1,30);base=sorted(random.sample(range(-20,60),n));r=random.randrange(n);nums=base[r:]+base[:r]
    for t in range(-22,62):
        calls[0]=0;assert search(nums,t,0,n-1)==(nums.index(t) if t in nums else -1)
print('Q3 ok')
calls[0]=0;print('example',search([4,5,6,7,0,1,2],0,0,6),calls[0])
mx=0;n=1000;base=list(range(n))
for r in range(n):
    nums=base[r:]+base[:r]
    for t in list(range(-1,n+1)):
        calls[0]=0;search(nums,t,0,n-1);mx=max(mx,calls[0])
print('max calls n=1000',mx)
# bugged version fails?
fails=0
for _ in range(300):
    n=random.randint(2,12);base=sorted(random.sample(range(0,40),n));r=random.randrange(n);nums=base[r:]+base[:r]
    for t in nums:
        try:
            calls[0]=0;fails+= search(nums,t,0,n-1,'bug')!=nums.index(t)
        except RecursionError:fails+=1
print('bug variant fails',fails)
# fillblank options
def mk(opt):
    def s(nums,t,lo,hi):
        calls[0]+=1
        if calls[0]>200:raise RecursionError
        if lo>hi:return -1
        mid=(lo+hi)//2
        if nums[mid]==t:return mid
        if nums[lo]<=nums[mid]:
            if nums[lo]<=t<nums[mid]:return s(nums,t,lo,mid-1)
            return {'a':lambda:s(nums,t,mid,hi),'b':lambda:s(nums,t,mid+1,hi-1),'c':lambda:s(nums,t,mid+1,hi),'d':lambda:s(nums,t,lo,mid)}[opt]()
        if nums[mid]<t<=nums[hi]:return s(nums,t,mid+1,hi)
        return s(nums,t,lo,mid-1)
    return s
for o in 'abcd':
    f=0;s=mk(o)
    for _ in range(300):
        n=random.randint(1,12);base=sorted(random.sample(range(0,40),n));r=random.randrange(n);nums=base[r:]+base[:r]
        for t in range(-1,41):
            try:
                calls[0]=0;f+=s(nums,t,0,n-1)!=(nums.index(t) if t in nums else -1)
            except RecursionError:f+=1
    print('fillblank option',o,'failures',f)
# Q4 KMP and reversed
def pi(P):
    f=[0]*len(P);k=0
    for q in range(1,len(P)):
        while k and P[k]!=P[q]:k=f[k-1]
        if P[k]==P[q]:k+=1
        f[q]=k
    return f
print('pi baaba',pi('baaba'),'idx',('dfzcbau'.find('cba')+1))
def kmp_has(T,P):
    f=pi(P);q=0;back=0
    for ch in T:
        while q and (q==len(P) or P[q]!=ch):q=f[q-1];back+=1
        if P[q]==ch:q+=1
        if q==len(P):return True,back
    return False,back
for _ in range(20000):
    T=''.join(random.choice('ab') for _ in range(random.randint(2,20)));P=''.join(random.choice('ab') for _ in range(random.randint(1,len(T)-1)))
    assert kmp_has(T,P[::-1])[0]==(P[::-1] in T)
    assert kmp_has(T,P[::-1])[1]<=len(T)
print('Q4 ok')
