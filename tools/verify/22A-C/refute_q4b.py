import itertools
from collections import Counter
def mg(A,c):
    C={}
    for x in A:
        if x in C:C[x]+=1
        elif len(C)<c:C[x]=1
        else:
            for y in list(C):
                C[y]-=1
                if C[y]==0:del C[y]
    return list(C)
for cnt in (2,3):
  miss=0;ex=None
  for n in (6,9,12):
    for A in itertools.product(range(4),repeat=n if n<=9 else 0):
        c=Counter(A)
        sols=[(k,m) for k in c for m in c if k<m and 2*c[k]>=n and 3*c[m]>=n]
        if not sols: continue
        cand=mg(A,cnt)
        if not any(k in cand and m in cand for k,m in sols): miss+=1; ex=ex or A
  print(cnt,"counters: misses",miss,ex)
