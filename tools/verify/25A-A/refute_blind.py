import random, itertools
INF=float('inf')
# --- Q1a official Mid (typos repaired): A,B 1-indexed lists with sentinel
def mid(A,i,j,B,k,l):
    if i==j: return (A[i]+B[k])/2
    a1=A[(i+j-1)//2];a2=A[(i+j+1)//2];b1=B[(k+l-1)//2];b2=B[(k+l+1)//2]
    if a1<b1<b2<a2: return (b1+b2)/2
    if b1<a1<a2<b2: return (a1+a2)/2
    if a1<a2<b1<b2 or a1<b1<a2<b2: return mid(A,(i+j+1)//2,j,B,k,(k+l-1)//2)
    if b1<b2<a1<a2 or b1<a1<b2<a2: return mid(A,i,(i+j-1)//2,B,(k+l+1)//2,l)
    raise Exception('uncovered')
calls=[0]
bad=0
for _ in range(3000):
    k=random.randint(0,5);m=2**k  # per-array size n/2 = m ; n=2m ; n power of 2 -> m power of 2
    vals=random.sample(range(1,10000),2*m)
    A=sorted(vals[:m]);B=sorted(vals[m:])
    exp=sorted(vals);want=(exp[m-1]+exp[m])/2
    got=mid([None]+A,1,m,[None]+B,1,m)
    if got!=want: bad+=1
print('Q1a mismatches',bad)
# example steps
A=[1,2,3,10];B=[4,5,6,7];print(mid([None]+A,1,4,[None]+B,1,4))
# recursion depth for 8,8
depth=0;m=8
while m>1:m//=2;depth+=1
print('depth 8->1',depth)
# --- Q1c Find_r from claim
def find_r(A,B,r):
    Aa=lambda x: -INF if x==0 else (A[x-1] if x<=r else INF)
    Bb=lambda x: -INF if x==0 else (B[x-1] if x<=r else INF)
    lo,hi=0,r;it=0
    while lo<=hi:
        it+=1
        i=(lo+hi)//2;j=r-i
        if Aa(i+1)<Bb(j): lo=i+1
        elif Bb(j+1)<Aa(i): hi=i-1
        else: return max(Aa(i),Bb(j)),it
    raise Exception('no return')
bad=0;maxit=0
for _ in range(5000):
    h=random.choice([1,2,4,8,16]);vals=random.sample(range(1,500),2*h)
    A=sorted(vals[:h]);B=sorted(vals[h:]);r=random.randint(1,h)
    got,it=find_r(A,B,r)
    if got!=sorted(vals)[r-1]:bad+=1
    import math
    maxit=max(maxit,it-(math.floor(math.log2(r+1))+1))
print('Q1c bad',bad,'iters over bound',maxit)
print(find_r([2,5,8,11],[1,3,9,12],3), [x for x in sorted([2,5,8,11,1,3,9,12])][:3])
# printed official: mid of A[1..r],B[1..r] avg of two middles
print('printed official for A=[1,2],B=[3,4],r=2:', mid([None,1,2],1,2,[None,3,4],1,2),'true 2nd smallest',sorted([1,2,3,4])[1])
# buggy j<-r
def find_bug(A,B,r):
    Aa=lambda x: -INF if x==0 else (A[x-1] if x<=r else INF)
    Bb=lambda x: -INF if x==0 else (B[x-1] if x<=r else INF)
    lo,hi=0,r;it=0
    while lo<=hi and it<100:
        it+=1;i=(lo+hi)//2;j=r
        if Aa(i+1)<Bb(j): lo=i+1
        elif Bb(j+1)<Aa(i): hi=i-1
        else: return max(Aa(i),Bb(j))
    return None
print('bugged on example',find_bug([2,5,8,11],[1,3,9,12],3))
# --- Q2a recurrence
def T(S1,S2,S3,i,j,k):
    if i==0 and j==0 and k==0: return True
    if i>0 and j>0 and k>0:
        e1=S1[i-1]==S3[k-1];e2=S2[j-1]==S3[k-1]
        if e1 and e2: return T(S1,S2,S3,i-1,j,k-1) or T(S1,S2,S3,i,j-1,k-1)
        if e1: return T(S1,S2,S3,i-1,j,k-1)
        if e2: return T(S1,S2,S3,i,j-1,k-1)
        return False
    if i>0 and k>0 and j==0: return S1[i-1]==S3[k-1] and T(S1,S2,S3,i-1,j,k-1)
    if i==0 and j>0 and k>0: return S2[j-1]==S3[k-1] and T(S1,S2,S3,i,j-1,k-1)
    return False
def brute(S1,S2,S3):
    n=len(S1)+len(S2)
    if len(S3)!=n: return False
    for pos in itertools.combinations(range(n),len(S1)):
        a=iter(S1);b=iter(S2);s=''
        ps=set(pos);ok=True;x=y=0
        for t in range(n):
            if t in ps:
                if S1[x]!=S3[t]: ok=False;break
                x+=1
            else:
                if S2[y]!=S3[t]: ok=False;break
                y+=1
        if ok:return True
    return False
bad=0
for _ in range(4000):
    S1=''.join(random.choice('ab') for _ in range(random.randint(0,4)));S2=''.join(random.choice('ab') for _ in range(random.randint(0,4)))
    S3=''.join(random.choice('ab') for _ in range(random.choice([len(S1)+len(S2),len(S1)+len(S2),random.randint(0,8)])))
    if T(S1,S2,S3,len(S1),len(S2),len(S3))!=brute(S1,S2,S3): bad+=1
print('Q2a recurrence bad',bad)
print('step0',T('ab','b','bab',2,1,3),T('ab','b','bab',1,1,2),T('ab','b','bab',2,0,2))
print('step1',T('abc','dec','adbcec',3,3,6))
# official printed version (k not decremented in rows 4 and 8): count failures
def Tbad(S1,S2,S3,i,j,k):
    f=Tbad
    if i==0 and j==0 and k==0: return True
    if i>0 and j>0 and k>0:
        e1=S1[i-1]==S3[k-1];e2=S2[j-1]==S3[k-1]
        if e1 and e2: return f(S1,S2,S3,i-1,j,k-1) or f(S1,S2,S3,i,j-1,k-1)
        if e1: return f(S1,S2,S3,i-1,j,k-1)
        if e2: return f(S1,S2,S3,i,j-1,k)
        return False
    if i>0 and k>0 and j==0: return S1[i-1]==S3[k-1] and f(S1,S2,S3,i-1,j,k-1)
    if i==0 and j>0 and k>0: return S2[j-1]==S3[k-1] and f(S1,S2,S3,i,j-1,k)
    return False
print('printed official on ex1', Tbad('abc','def','adbcef',3,3,6),'ex2',Tbad('abc','dec','adbcec',3,3,6))
cnt=0
for _ in range(2000):
    S1=''.join(random.choice('ab') for _ in range(random.randint(0,4)));S2=''.join(random.choice('ab') for _ in range(random.randint(0,4)))
    S3=''.join(random.choice('ab') for _ in range(len(S1)+len(S2)))
    try:
        if Tbad(S1,S2,S3,len(S1),len(S2),len(S3))!=brute(S1,S2,S3):cnt+=1
    except RecursionError: cnt+=1
print('printed-official wrong on',cnt,'/2000')
# --- Q3
def greedy(L,n):
    s=0;c=0
    for x in sorted(L):
        if s+x<=n:s+=x;c+=1
        else:break
    return c
def bf(L,n):
    return max(r for r in range(len(L)+1) if any(sum(c)<=n for c in itertools.combinations(L,r)))
ok=all(greedy(L,n)==bf(L,n) for L,n in [([random.randint(1,9) for _ in range(random.randint(0,7))],random.randint(1,25)) for _ in range(3000)])
print('Q3 greedy',ok,greedy([7,1,4,2,9,3],10),greedy([2,5,3,8,10],6),greedy([1,2,3],6))
def greedy_lt(L,n):
    s=0;c=0
    for x in sorted(L):
        if s+x<n:s+=x;c+=1
        else:break
    return c
print('lt bug',greedy_lt([1,2,3],6))
# --- Q4a
def pi(S):
    p=[0]*len(S);k=0
    for q in range(1,len(S)):
        while k and S[k]!=S[q]:k=p[k-1]
        if S[k]==S[q]:k+=1
        p[q]=k
    return p
def longest_proper(S): return max([l for l in range(len(S)) if S[:l]==S[len(S)-l:]]+[0])
ok=all(pi(S)[-1]==longest_proper(S) for S in [''.join(random.choice('ab') for _ in range(random.randint(1,10))) for _ in range(3000)])
print('Q4a pi[n] ok',ok,pi('aabcdaabc'),pi('aaaa'),pi('abcabcd'),max(pi('abcabcd')))
# --- Q5 DFS
edges={'A':['B','D'],'B':['C'],'C':[],'D':['E'],'E':[],'F':[]}
t=[0];D={};F={};P={}
def dfs(u,p):
    t[0]+=1;D[u]=t[0];P[u]=p
    for v in edges[u]:
        if v not in D:dfs(v,u)
    t[0]+=1;F[u]=t[0]
for u in sorted(edges):
    if u not in D:dfs(u,None)
print(D,F,[u for u in P if P[u] is None],[u for u in D if F[u]==D[u]+1])
# suffix tree BA occurrences
T_='ABABABA';print([i+1 for i in range(len(T_)) if T_.startswith('BA',i)],'1-indexed')
