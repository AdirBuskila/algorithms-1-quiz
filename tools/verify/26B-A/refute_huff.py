import itertools
def outcomes(freq):
    res=set()
    def rec(nodes):
        if len(nodes)==1:
            codes={}
            def walk(n,p):
                if isinstance(n[1],str): codes[n[1]]=p
                else: walk(n[1][0],p+'0');walk(n[1][1],p+'1')
            walk(nodes[0],'')
            res.add(tuple(sorted(codes.items())));return
        s=sorted(nodes,key=lambda n:n[0]);m1=s[0][0]
        # choose two smallest with ties arbitrary
        ws=sorted(n[0] for n in nodes);a,b=ws[0],ws[1]
        pool=[i for i,n in enumerate(nodes) if n[0]==a]
        for i,j in itertools.permutations(range(len(nodes)),2):
            if nodes[i][0]==a and nodes[j][0]==b and (i!=j):
                if a==b and i>j: continue
                rest=[n for k,n in enumerate(nodes) if k not in(i,j)]
                x,y=nodes[i],nodes[j]
                for l,r in ((x,y),(y,x)):   # child order: left weight <= right weight
                    if l[0]<=r[0]: rec(rest+[(a+b,(l,r))])
    rec([(f,ch) for ch,f in freq.items()])
    return res
target=(('a','0'),('b','1100'),('c','1101'),('d','111'),('e','10'))
ok=[]
for e in range(1,40):
    o=outcomes(dict(a=13,b=1,c=2,d=4,e=e))
    if target in o: ok.append(e)
print(ok)
