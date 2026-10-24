# tie-aware Huffman: set of code-length vectors, and set of code assignments under 'lighter child on the left' convention
def lens(freqs):
    res=set()
    def rec(nodes):
        if len(nodes)==1:
            d={}
            def w(n,dep):
                if n[0]=='L': d[n[1]]=dep
                else: w(n[1],dep+1); w(n[2],dep+1)
            w(nodes[0][1],0); res.add(tuple(d[i] for i in range(len(freqs)))); return
        ws=sorted(n[0] for n in nodes)
        for i in range(len(nodes)):
            for j in range(i+1,len(nodes)):
                a,b=nodes[i],nodes[j]
                if sorted([a[0],b[0]])!=ws[:2]: continue
                rest=[n for t,n in enumerate(nodes) if t not in(i,j)]
                rec(rest+[(a[0]+b[0],('N',a[1],b[1]))])
    rec([(f,('L',i)) for i,f in enumerate(freqs)])
    return res
# labelled by letter: letters a,b,c,d with freqs
for f in ([1,1,1,3],[2,2,2,4],[1,1,2,3],[3,3,4,5],[1,1,4],[2,2,5],[4,4,7]):
    print(f,sorted(lens(f)))
# official example: bbabbc -> a1 c1 b4; k=1 (2,2,5); k=3 (4,4,7)
