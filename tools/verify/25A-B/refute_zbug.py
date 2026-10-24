import random
def z(s,bug):
    L=len(s);Z=[0]*L;Z[0]=L;l=r=0
    for k in range(1,L):
        if k<r: Z[k]=Z[k-l] if bug else min(r-k,Z[k-l])
        else: Z[k]=0
        while k+Z[k]<L and s[Z[k]]==s[k+Z[k]]:Z[k]+=1
        if k+Z[k]>r:l,r=k,k+Z[k]
    return Z
def zb(s):return [next(j for j in range(len(s)-k+1) if j==len(s)-k or s[j]!=s[k+j]) for k in range(len(s))]
random.seed(2);bad=0
for _ in range(3000):
    s=''.join(random.choice('ab') for _ in range(random.randint(2,10)))
    assert z(s,False)==zb(s)
    bad+= z(s,True)!=zb(s)
print("buggy differs on",bad,"of 3000"); print(z("aabxaab",False))
# successful comparisons count
def succ(s):
    L=len(s);Z=[0]*L;l=r=0;c=0
    for k in range(1,L):
        Z[k]=min(r-k,Z[k-l]) if k<r else 0
        while k+Z[k]<L and s[Z[k]]==s[k+Z[k]]:Z[k]+=1;c+=1
        if k+Z[k]>r:l,r=k,k+Z[k]
    return c
print(succ("a"*8))
for _ in range(3000):
    s=''.join(random.choice('ab') for _ in range(random.randint(2,14)));assert succ(s)<=len(s)
