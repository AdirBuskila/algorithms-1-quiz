import json,re,sys
pat=re.compile(r"(אפשרות|תשובה\s*[א-ד]\b|תשובה\s*\(|סעיף|מסעיף|בסעיף|הראשון|הראשונה|השני|השנייה|שניה|\boption\b|\bchoice\b|לעיל|שלמעלה|שלמטה|הקודם|הבא)")
for code in sys.argv[1:]:
    d=json.load(open('raw/%s.json'%code,encoding='utf8'))
    for qi,q in enumerate(d['questions']):
        def scan(label,s):
            if isinstance(s,str):
                for m in pat.finditer(s):
                    a=max(0,m.start()-25);print(code,'Q%s%s'%(q.get('num'),q.get('part')),label,'|',s[a:m.end()+25].replace('\n',' '))
        for k in ('rubric','pitfalls'):
            for x in q.get(k,[]):
                scan(k,x if isinstance(x,str) else x.get('text'))
        for si,st in enumerate(q.get('steps',[])):
            scan('step%d.prompt'%si,st.get('prompt'));scan('step%d.explain'%si,st.get('explain'))
            for o in st.get('options',[]):scan('step%d.option'%si,o.get('value'))
            for l in st.get('lines',[]):scan('step%d.line'%si,l)
