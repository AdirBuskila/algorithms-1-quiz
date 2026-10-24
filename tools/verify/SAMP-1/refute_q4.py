import itertools
def run(c5r):
    C={1:(-4.5,2),2:(0,2),3:(0,3),4:(5,4),5:(6,c5r),6:(7,5),7:(8,3)}
    def disj(a,b):
        (c,r),(d,s)=C[a],C[b]; return abs(c-d)>r+s
    best=0;sets=[]
    for k in range(1,8):
        for S in itertools.combinations(C,k):
            if all(disj(a,b) for a,b in itertools.combinations(S,2)):
                if k>best: best=k;sets=[]
                if k==best: sets.append(S)
    print("c5 r=",c5r,best,sets)
run(2);run(4)
