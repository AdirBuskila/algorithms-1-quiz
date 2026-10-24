# -*- coding: utf-8 -*-
"""Generator for tools/raw/22A-C.json -- algorithms-1 (60072), semester A 5782 (2022), special moed (10.4.2022).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_22A-C.py

Source: a graded student answer booklet (33 pp scan, score 100). It is NOT an official source: answers are labelled
student-solution, official False. PRIVACY: text only, no crops of any page (the pages carry a student id and handwriting);
no id, name or grader mark is copied. The questions are printed text on the booklet pages; the answers are handwritten
and were read as far as they are legible.
Items: Q1; Q2; Q3 a, b; Q4; Q5 (bonus). Q3b, Q4, Q5 were held (no key) and are solver-written.

Transcription notes
- Q2's header says "3 סעיפים" but one request is printed.
- Q3b: the student's proof was marked "not proven" by the grader (-10) -> no key, HELD.
- Q4: the student's pseudocode (select at n/2 and 2n/3 and count) tests the counts with equality (== n/3) where the
  statement says "at least"; see checks. HELD so the solver writes a sound solution.
- Q5 (bonus, 15 pts): a table of E' and C per iteration for a graph; the student's table is incomplete and was scored 3/15,
  and the graph figure would need a crop of the student's page (not allowed). HELD (no-key).
- Q1: the grader's marks show -3 on the base case of the student's formula; the recurrence below is the standard
  one (F(0)=0, F(i)=1+min over 1<=j<=sqrt(i) of F(i-j^2)), which the paper's second line matches.

Checks (tools/verify/22A-C/checks.py): Q1 recurrence vs BFS (N<=60); Q2 pi(S$S^R) last value vs brute force
(3000 random strings; aabaac -> 5); Q3a sort + pair neighbours vs all pairings (1500 random); Q4 shows the '==' flaw.

Solver pass (2026-10-24, solutionSource "solved", official false, pending refuter): Q3b (exchange argument: some optimal
pairing pairs the two cheapest items), Q4 (Select at the multiples of ceil(n/2) and ceil(n/3) gives at most 5 candidates,
count each, O(n)) and Q5 (one run of the approximation, 4 iterations, C={a,b,d,e,f,g,h,i}). The Q5 figure is a clean
redraw from data (tools/verify/22A-C/draw_graph.py -> images/exams/22A-C-Q5-graph.png), never a crop of the student page;
the edge set is read off the printed figure and agrees with the student's E' list. Checks: tools/verify/22A-C/solve_22A-C.py
(Q4 vs brute force on all 87380 arrays n<=8 over 1..4; graph data in tools/verify/22A-C/graphs.json).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "22A-C.json"


def Q(num, part, kind, topic, question, solution, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution,
         "solutionSource": "student-solution", "official": False, "confidence": "med"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


Q1 = (r"כל מספר טבעי $N$ ניתן לייצוג כסכום של מספרים שהם ריבועים. למשל:" "\n"
      r"$1+\ldots+1+1=9+1+1+1=4+4+4=12$" "\n"
      r"הטענה נכונה לכל $N$ כי $1$ הוא ריבוע ותמיד ניתן לייצג את $N$ כסכום של $N$ אחדות." "\n"
      r"**בעיית הסכום הריבועי המינימלי:**" "\n"
      r"**קלט:** מספר $N$" "\n"
      r"**פלט:** ייצוג של $N$ כסכום של מספר מינימלי של ריבועים." "\n"
      r"הבעיה ניתנת לפתרון בעזרת תכנון דינמי." "\n"
      r"הציגו נוסחה רקורסיבית המחשבת את המספר המינימלי של ריבועים שסכומם הוא $N$. יש לפרט לכל פרמטר בנוסחה את תפקידו "
      r"וכן להסביר את הפלט ונכונות הנוסחה (אין צורך בהוכחה פורמלית).")

S1 = r"""$$F(i)=\begin{cases}0 & ;\ i=0\\ \displaystyle\min_{1\le j\le\sqrt{i}}\bigl(F(i-j^2)\bigr)+1 & ;\ \text{else}\end{cases}$$
$i$ הוא המספר שיש לייצג כסכום ריבועים, ו-$j$ הוא שורש הריבוע האחרון בסכום ($1\le j\le\sqrt{i}$); $F(i)$ הוא מספר הריבועים המינימלי שסכומם $i$. הפלט הוא $F(N)$."""

Q2 = (r"תהי $S=s_1s_2\ldots s_n$ מחרוזת. נסמן ב-$S^R$ את המחרוזת ההופכת של $S$, ז\"א $S^R=s_ns_{n-1}\ldots s_1$. לדוגמא, אם "
      r"$S=aabc$ אז $S^R=cbaa$. נאמר שמחרוזת $S$ היא פולינדרום אם $S^R=S$." "\n"
      r"להלן, בעיית הרישא הפולינדרומית:" "\n"
      r"**קלט:** מחרוזת $S$ באורך של $n$ תווים." "\n"
      r"**פלט:** אורך הרישא המקסימלית של $S$ שהינה פולינדרום." "\n"
      r"לדוגמא: עבור הקלט: $aabaac$, יוחזר הערך: $5$." "\n"
      r"הציעו האלגוריתם היעיל ביותר המקבל מחרוזת $S$ באורך $n$ ומחזיר את אורך הרישא הפולינדרומית. יש לציין את סיבוכיות זמן "
      r"הריצה של האלגוריתם שהצעתם (אין צורך בהוכחה).")

S2 = r"""- נגדיר את $S^R$ ונבנה את המחרוזת `S#SR` (מחרוזת $S$, אחריה תו מפריד `#` שאינו מופיע ב-$S$, ואחריו $S^R$).
- נריץ את פונקציית הרישא (prefix function) של KMP על המחרוזת `S#SR`.
- הערך האחרון בטבלה הוא אורך הרישא המקסימלית של $S$ שהיא פולינדרום.

סיבוכיות זמן הריצה: $O(n)$ (המחרוזת באורך $2n+1$, ולכן $\Theta(n)$)."""

Q3 = (r"לרגל חג הפסח המתקרב, רשת המרכולים \"רק אצלנו\" יצאה במבצע לחג. הרשת הכריזה שמי שקונה זוג מוצרים מקבל את הזול "
      r"מביניהם בחינם. לרותי רשימה של $2n$ מוצרים שברצונה לקנות, במחירים (רשימת המחירים לאו דווקא ממוינת): "
      r"$p_1,p_2,\ldots,p_{2n}$." "\n"
      r"רותי מתכננת לבצע $n$ רכישות, בכל רכישה תקנה $2$ מוצרים.")

S3A = r"""- נמיין את רשימת המחירים מהקטן לגדול.
- נחלק את המוצרים לזוגות לפי הסדר הממוין: המוצר הראשון עם השני, השלישי עם הרביעי וכן הלאה; בכל זוג המוצר הזול בחינם ומשלמים על היקר.
- נחזיר את הסכום."""

Q4 = (r"נתון מערך $A$ עם $n$ מספרים טבעיים." "\n"
      r"הציעו אלגוריתם לינארי המקבל כקלט את המערך $A$ ומחזיר שני ערכים מהמערך $k,m$ כך ששלושת התנאים הבאים מתקיימים:" "\n"
      r"I. $k<m$" "\n"
      r"II. $k$ מופיע במערך לפחות $n/2$ פעמים." "\n"
      r"III. $m$ מופיע במערך לפחות $n/3$ פעמים")

Q5 = (r"**שאלת בונוס (15 נקודות).**" "\n"
      r"נתון הגרף הבא, כתבו את ערכי קבוצת הכיסוי $C$ וערכי הקבוצה $E'$ בכל איטרציה בהרצת האלגוריתם למציאת קירוב לכיסוי "
      r"קודקודים שלמדנו במסגרת הקורס.")

SOLVED = {"solutionSource": "solved", "official": False, "confidence": "high"}

S3B = r"""נמיין את המחירים: $p_1\le p_2\le\ldots\le p_{2n}$. **הבחירה החמדנית** של האלגוריתם היא לשים בזוג אחד את שני המוצרים הזולים ביותר, $p_1$ ו-$p_2$ (ומשלמים $p_2$). נוכיח שקיים פתרון אופטימלי שמכיל את הזוג הזה.
יהי $OPT$ חלוקה אופטימלית לזוגות. אם $p_1$ ו-$p_2$ באותו זוג ב-$OPT$, סיימנו. אחרת, ב-$OPT$ יש זוג $(p_1,x)$ וזוג $(p_2,y)$, כאשר $x,y$ הם מוצרים אחרים, ולכן $x\ge p_2$ ו-$y\ge p_2\ge p_1$. בשני הזוגות משלמים על היקר, כלומר על $x$ ועל $y$, ובסך הכול $x+y$.
נחליף את שני הזוגות בזוגות $(p_1,p_2)$ ו-$(x,y)$. עכשיו משלמים $p_2+\max(x,y)$. מתקיים
$$x+y=\max(x,y)+\min(x,y)\ge\max(x,y)+p_2$$
כי $\min(x,y)\ge p_2$. לכן החלוקה החדשה אינה יקרה יותר מ-$OPT$, ומכיוון ש-$OPT$ אופטימלית גם היא אופטימלית, והיא מכילה את הזוג $(p_1,p_2)$. לכן הבחירה החמדנית נמצאת בפתרון אופטימלי כלשהו."""

CODE_4 = r"""Find_k_m(A, n)
   h = ceil(n/2) ; t = ceil(n/3)
   Kc = { Select(A, q) : q = h, 2h, ... , q <= n }        // at most 2 candidates for k
   Mc = { Select(A, q) : q = t, 2t, 3t, ... , q <= n }    // at most 3 candidates for m
   for each value v in Kc u Mc
      cnt[v] = number of i with A[i] = v                  // one pass over A
   for each k in Kc
      for each m in Mc
         if k < m and cnt[k] >= n/2 and cnt[m] >= n/3
            return (k, m)
   return NIL                                           // no such pair"""

S4 = (r"""**רעיון.** נסתכל על המערך הממוין. אם ערך $v$ מופיע לפחות $n/2$ פעמים, המופעים שלו תופסים רצף של לפחות $h=\lceil n/2\rceil$ מקומות סמוכים, וכל רצף של $h$ מקומות סמוכים מכיל מקום שהוא כפולה של $h$. לכן $v$ הוא האיבר ה-$q$ בגודלו עבור כפולה כלשהי $q$ של $h$ (יש לכל היותר $2$ כפולות כאלה עד $n$). באותו אופן, ערך שמופיע לפחות $n/3$ פעמים הוא האיבר ה-$q$ בגודלו עבור כפולה $q$ של $t=\lceil n/3\rceil$ (לכל היותר $3$ כפולות). מוצאים את המועמדים בעזרת Select, סופרים את המופעים של כל מועמד, ובודקים את התנאים (כולל $k<m$) במפורש:
""" + "```\n" + CODE_4 + "\n```\n" + r"""**נכונות.** כל זוג שהאלגוריתם מחזיר מקיים את שלושת התנאים, כי הם נבדקים במפורש עם "לפחות" (ולא שוויון). להפך, אם קיים זוג $k<m$ מתאים, אז לפי הרעיון $k$ נמצא ב-$Kc$ ו-$m$ נמצא ב-$Mc$, ולכן האלגוריתם ימצא זוג מתאים.
**סיבוכיות.** לכל היותר $5$ קריאות ל-Select, כל אחת $O(n)$; לכל היותר $5$ מעברי ספירה על המערך, כל אחד $O(n)$; ולכל היותר $2\cdot3$ בדיקות של זוגות. סה"כ $O(n)$.
דוגמה: $A$ עם שש פעמים $1$ ושש פעמים $2$ ($n=12$): $h=6$, המועמדים ל-$k$ הם האיברים במקומות $6,12$, כלומר $1,2$; $t=4$, המועמדים ל-$m$ הם האיברים במקומות $4,8,12$, כלומר $1,2,2$. הזוג $(1,2)$ מקיים $6\ge6$ ו-$6\ge4$ ומוחזר.""")

S5 = r"""**האלגוריתם (קירוב 2 לכיסוי קודקודים):** $C\leftarrow\emptyset$, $E'\leftarrow E$. כל עוד $E'\ne\emptyset$: בוחרים צלע כלשהי $(u,v)\in E'$, מוסיפים את $u$ ואת $v$ ל-$C$, ומוחקים מ-$E'$ את כל הצלעות שנוגעות ב-$u$ או ב-$v$.
בגרף $15$ צלעות: $ab$, $ah$, $af$, $hg$, $gf$, $bi$, $ih$, $id$, $bc$, $cd$, $de$, $gd$, $dj$, $jf$, $fe$. בחירת הצלעות שרירותית, ולכן יש כמה הרצות נכונות; להלן הרצה אחת:
$$\begin{array}{c|c|l|l} \text{iteration} & \text{edge} & C & E'\\\hline 1 & (a,b) & \{a,b\} & \{hg,gf,ih,id,cd,de,gd,dj,jf,fe\}\\ 2 & (h,g) & \{a,b,g,h\} & \{id,cd,de,dj,jf,fe\}\\ 3 & (i,d) & \{a,b,d,g,h,i\} & \{jf,fe\}\\ 4 & (f,e) & \{a,b,d,e,f,g,h,i\} & \emptyset\end{array}$$
בכל איטרציה נמחקות הצלעות שנוגעות בשני הקודקודים שנבחרו: באיטרציה 1 נמחקות $ab,ah,af,bi,bc$; באיטרציה 2 $hg,gf,ih,gd$; באיטרציה 3 $id,cd,de,dj$; באיטרציה 4 $fe,jf$.
הפלט: $C=\{a,b,d,e,f,g,h,i\}$, $|C|=8$. הצלעות שנבחרו, $(a,b),(h,g),(i,d),(f,e)$, הן זיווג מקסימלי, וכל כיסוי חייב להכיל קודקוד אחד לפחות מכל אחת מהן, ולכן $|C|=2\cdot4\le2\cdot OPT$ (בגרף זה $OPT=4$)."""

questions = [
    Q(1, None, "algorithm", "dp_sequences", Q1, S1, points=25),
    Q(2, None, "algorithm", "kmp_strings", Q2, S2, points=25),
    Q(3, "א", "algorithm", "greedy",
      r"הציעו אלגוריתם חמדני המחלק את המוצרים ל-$n$ זוגות, כך שהסכום הכולל שנשלם עבורם יהיה מינימלי.", S3A, contextId="c3"),
    Q(3, "ב", "proof", "greedy", r"הוכיחו שהאלגוריתם שהצעת מקיים את תכונת הבחירה החמדנית.", S3B,
      contextId="c3", **SOLVED),
    Q(4, None, "algorithm", "divide_conquer", Q4, S4, points=25, **SOLVED),
    Q(5, None, "computation", "approximation", Q5, S5, points=15, image="images/exams/22A-C-Q5-graph.png", **SOLVED),
]

exam = {
    "examCode": "22A-C",
    "examLabel": "אלגוריתמים 1 (60072), סמסטר א' תשפ\"ב, מועד מיוחד (10.4.2022)",
    "year": 2022,
    "examDate": "10.4.2022",
    "sourceFile": "22A-C exam booklet (graded student scan)",
    "solutionFile": "student-solution-1",
    "contexts": {
        "c3": {"kind": "text", "title": "שאלה 3: חג הפסח והמבצע", "text": Q3},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
