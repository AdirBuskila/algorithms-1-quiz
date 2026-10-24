import math
bad={}
for n in range(1,400):
    L=math.ceil(0.34*n-1e-12)
    for name,posf in (("ceil",lambda n,f:math.ceil(n*f)),("floor",lambda n,f:max(1,math.floor(n*f)))):
        for s in range(1,n-L+2):
            blk=range(s,s+L)
            if not any(posf(n,f) in blk for f in (1/3,2/3)): bad.setdefault(name,[]).append((n,s,L))
        # 51% with n/2
    L=math.ceil(0.51*n-1e-12)
    for name,posf in (("ceil",lambda n:math.ceil(n/2)),("floor",lambda n:max(1,n//2))):
        for s in range(1,n-L+2):
            if posf(n) not in range(s,s+L): bad.setdefault("51"+name,[]).append((n,s,L))
print({k:(len(v),v[:3]) for k,v in bad.items()})
