C={1:(-4.5,2),2:(0,2),3:(0,3),4:(5,4),5:(6,2),6:(7,5),7:(8,3)}
def run(strict):
    L=sorted(C,key=lambda i:C[i][0]+C[i][1]);out=[]
    while L:
        g=L.pop(0);out.append(g);R=C[g][0]+C[g][1]
        L=[i for i in L if not ((C[i][0]-C[i][1])<R if strict else (C[i][0]-C[i][1])<=R)]
    return out
print("<=",run(False),"<",run(True))
