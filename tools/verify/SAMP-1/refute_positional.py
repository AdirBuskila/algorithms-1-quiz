import json,re,sys
pat=re.compile(r'(סעיף|סעיפים|אפשרות|החלופה|החלופות|הראשונה|השנייה|option|\([a-d]\)|הקודם|הבא)')
out=open(sys.argv[1],'w',encoding='utf-8')
for c in ['22A-A','22A-B','22A-C','SAMP-1']:
    d=json.load(open('../raw/%s.json'%c,encoding='utf-8'))
    def walk(o,path):
        if isinstance(o,dict):
            for k,v in o.items(): walk(v,path+'.'+k)
        elif isinstance(o,list):
            for i,v in enumerate(o): walk(v,path+'[%d]'%i)
        elif isinstance(o,str):
            for m in pat.finditer(o):
                s=max(0,m.start()-30);out.write('%s %s | %s\n'%(c,path,o[s:m.end()+30].replace('\n',' ')))
    for q in d['questions']: walk(q,'Q%s%s'%(q['num'],q.get('part','')))
    for k,v in d.get('contexts',{}).items(): walk(v,'ctx'+k)
