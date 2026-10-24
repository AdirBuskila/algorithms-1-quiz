import itertools, random
# Q1a: any P of length 5 with pi=0,1,2,3,1 ? brute over alphabet size 5
def pi(P):
    r=[0]*len(P);k=0
    for i in range(1,len(P)):
        while k and P[i]!=P[k]:k=r[k-1]
        if P[i]==P[k]:k+=1
        r[i]=k
    return r
print("Q1a exists:",[p for p in itertools.product(range(5),repeat=5) if pi(p)==[0,1,2,3,1]])
# Q1b suffix array
s="algogoal"
sa=sorted(range(len(s)),key=lambda i:s[i:])
print("SA 1-based:",[i+1 for i in sa],[s[i:] for i in sa])
lcp=[0]+[next(k for k in range(100) if s[sa[j-1]:][k:k+1]!=s[sa[j]:][k:k+1]) for j in range(1,len(sa))]
print("LCP",lcp)
# Q2a circular max
def circ_brute(A):
    n=len(A);best=None
    for st in range(n):
        for L in range(1,n+1):
            v=sum(A[(st+t)%n] for t in range(L))
            best=v if best is None or v>best else best
    return best
def kad(A):
    b=cur=A[0]
    for x in A[1:]:
        cur=max(x,cur+x);b=max(b,cur)
    return b
def circ(A):
    mx=kad(A)
    if mx<0:return mx
    mn=-kad([-x for x in A])
    return max(mx,sum(A)-mn)
print("ex",circ_brute([4,-6,5,-6,10,-5,3]),circ([4,-6,5,-6,10,-5,3]))
random.seed(1)
for _ in range(20000):
    A=[random.randint(-6,6) for _ in range(random.randint(1,8))]
    assert circ(A)==circ_brute(A),A
# naive sum-total-minus-min without negative guard fails when all negative:
A=[-3,-1,-2];print("allneg",circ_brute(A),circ(A),max(kad(A),sum(A)+kad([-x for x in A])))
# the min-subarray = whole array case: total-min=0 (empty) -> only matters if all negative
# Q2b
A=[4,10,-6,3,15,-8,7];K=5
o=sorted(A[:K-1]+A[K:]);R=o[:K-1]+[A[K-1]]+o[K-1:];print("Q2b",R)
# Q3 DP
cost=[[14,2,11],[11,14,5],[14,3,19]]
T=[[0]*3 for _ in range(3)]
T[0]=cost[0][:]
for i in range(1,3):
    for c in range(3):
        T[i][c]=cost[i][c]+min(T[i-1][d] for d in range(3) if d!=c)
print("Q3 table (rows=house):",T,"min",min(T[2]))
bf=min(sum(cost[i][c[i]] for i in range(3)) for c in itertools.product(range(3),repeat=3) if all(c[i]!=c[i+1] for i in range(2)))
print("brute",bf)
# Q4 Huffman exhaustive tie-break
def huff_trees(freqs):
    # returns set of trees (frozenset-nested) obtainable
    res=set()
    def rec(nodes):
        if len(nodes)==1:
            res.add(nodes[0][1]);return
        ws=sorted(w for w,_ in nodes)
        m1,m2=ws[0],ws[1]
        for i in range(len(nodes)):
            for j in range(i+1,len(nodes)):
                wi,wj=nodes[i][0],nodes[j][0]
                if sorted([wi,wj])==[m1,m2]:
                    new=[nodes[k] for k in range(len(nodes)) if k not in(i,j)]
                    new.append((wi+wj,frozenset([nodes[i][1],nodes[j][1]])))
                    rec(new)
    rec([(w,l) for l,w in freqs.items()])
    return res
target=frozenset([frozenset(['b',frozenset(['c','d'])]),frozenset(['a','e'])])
def sol(lo):
    out=[]
    for c in range(lo,60):
        for d in range(lo,60):
            if not(c<=d and 7<=c+d and 10<=10): continue   # sibling order constraints (left<=right)
            # root children: left = b-subtree(7+c+d), right = a,e (20): left<=right
            if 7+c+d>20: continue
            f={'a':10,'b':7,'e':10,'c':c,'d':d}
            if target in huff_trees(f): out.append((c,d))
    return out
for lo in(1,0):
    s=sol(lo);print("lo",lo,len(s),s)
# without root-sibling ordering constraint, and without any ordering, for sensitivity
def sol2(lo,cons):
    out=[]
    for c in range(lo,60):
        for d in range(lo,60):
            if cons and not(c<=d and 7<=c+d and 7+c+d<=20):continue
            f={'a':10,'b':7,'e':10,'c':c,'d':d}
            if target in huff_trees(f): out.append((c,d))
    return out
print("unordered all obtainable (c,d>=1):",len(sol2(1,False)))
