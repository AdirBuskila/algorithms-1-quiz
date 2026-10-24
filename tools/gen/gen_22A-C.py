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

# ---------------------------------------------------------------- rubric / pitfalls / guided steps (ai-draft)
# Printed points: Q1 25, Q2 25, Q4 25, Q5 15; Q3 (a+b) has none printed, so the split 10 + 15 below is an AI draft.
# Rechecked while authoring (Q1 and Q3a are the med-confidence items): Q1's recurrence equals a BFS over all N <= 60, and
# Q3a's sorted-adjacent pairing equals the optimum over all pairings -- the stored (student-written) answers are right,
# so steps are authored for both. Every numeric / trace / complexity value is recomputed by
# tools/verify/22A-C/steps_22A-C.py (py -X utf8 -I), which also binds the results to tools/raw/22A-C.json.
IDS = "abcdef"


def opts(*vals):
    return [{"id": IDS[i], "type": "text", "value": v} for i, v in enumerate(vals)]


def rub(*items):
    return [{"text": t, "points": p} for t, p in items]


def add(num, part, **kw):
    for q in questions:
        if q["num"] == num and q.get("part", "") == part:
            q.update(kw)
            return
    raise KeyError((num, part))


add(1, "",
    rubric=rub(("הגדרת $F(i)$ כמספר הריבועים המינימלי שסכומם $i$", 5),
               ("תנאי התחלה $F(0)=0$", 4),
               ("הנוסחה $F(i)=1+\\min_{1\\le j\\le\\sqrt{i}}F(i-j^2)$: ניחוש הריבוע האחרון בסכום", 10),
               ("הסבר תפקיד $j$: שורש הריבוע האחרון, עם התנאי $j^2\\le i$", 3),
               ("הפלט הוא $F(N)$", 3)),
    rubricSource="ai-verified",
    pitfalls=["לשכוח את תנאי ההתחלה $F(0)=0$ ולהישאר בלי ערך לריבוע שמשלים בדיוק את $i$.",
              "לקחת תמיד את הריבוע הגדול ביותר: עבור $12$ זה נותן $9+1+1+1$ (ארבעה ריבועים) במקום $4+4+4$.",
              "לתת ל-$j$ לרוץ עד $i$ במקום עד $\\sqrt{i}$, כך שנוצרים אינדקסים שליליים $i-j^2$."],
    steps=[
        {"type": "numeric", "prompt": "מהו $F(12)$, מספר הריבועים המינימלי שסכומם $12$?",
         "answer": 3, "tol": 0,
         "explain": "$12=4+4+4$, ואין ייצוג בשני ריבועים (נבדק בנוסחה ובחיפוש BFS)."},
        {"type": "numeric", "prompt": "מהו $F(13)$?",
         "answer": 2, "tol": 0,
         "explain": "$13=9+4$, ואין ריבוע יחיד ששווה ל-$13$ (נבדק בנוסחה ובחיפוש BFS)."},
        {"type": "numeric",
         "prompt": "אלגוריתם חמדן לוקח בכל שלב את הריבוע הגדול ביותר שאינו עולה על המספר שנשאר. כמה ריבועים הוא משתמש עבור $N=12$?",
         "answer": 4, "tol": 0,
         "explain": "החמדן לוקח $9$ ואז שלוש פעמים $1$: ארבעה ריבועים, ואילו $F(12)=3$. לכן הנוסחה צריכה לבדוק את כל הריבועים האפשריים (נבדק)."},
        {"type": "choice", "prompt": "באיזה טווח רץ $j$ בנוסחה?",
         "options": opts("$1\\le j\\le\\sqrt{i}$", "$1\\le j\\le i$", "$0\\le j\\le\\sqrt{i}$", "$1\\le j<\\sqrt{i}$"),
         "correctId": "a",
         "explain": "דורשים $j^2\\le i$ ו-$j\\ge1$. עד $i$ מגיעים לאינדקס שלילי, עם $j=0$ הנוסחה קוראת לעצמה בלי להתקדם, ועם $j<\\sqrt{i}$ מפספסים את הריבועים המושלמים (למשל $F(4)=1$ יוצא $4$) (נבדק)."},
    ],
    stepsSource="ai-verified")

add(2, "",
    rubric=rub(("בניית $S^R$ ושרשור $S\\#S^R$ עם תו מפריד שאינו מופיע ב-$S$", 7),
               ("הרצת פונקציית הרישא (prefix function) של KMP על המחרוזת", 6),
               ("הערך האחרון בטבלה הוא אורך הרישא הפולינדרומית המקסימלית", 7),
               ("תפקיד המפריד, וסיבוכיות הזמן $O(n)$", 5)),
    rubricSource="ai-verified",
    pitfalls=["לשכוח את המפריד: אז הרישא של המחרוזת המשורשרת יכולה להתפרש על שני החלקים ולחרוג מ-$|S|$.",
              "לקחת את הערך המקסימלי בטבלה במקום את הערך האחרון.",
              "לשרשר את $S$ ל-$S$ עצמה בלי להפוך: זה מוצא רישא שחוזרת, לא רישא פולינדרומית."],
    steps=[
        {"type": "choice", "prompt": "איזו מחרוזת מריצים עליה את פונקציית הרישא עבור $S=aabaac$?",
         "options": opts("`aabaac#caabaa`", "`aabaac#aabaac`", "`caabaa#caabaa`", "`caabaa#aabaac`"), "correctId": "a",
         "explain": "מחברים את $S$, מפריד ו-$S^R$. בלי ההיפוך, כשמהפכים את שני החלקים, או כשהחלקים בסדר הפוך, הערך האחרון בטבלה אינו אורך הרישא הפולינדרומית $5$ (נבדק)."},
        {"type": "numeric", "prompt": "מהו הערך האחרון בטבלת הרישא של המחרוזת `aabaac#caabaa` (עבור $S=aabaac$)?",
         "answer": 5, "tol": 0,
         "explain": "הרישא הפולינדרומית הארוכה ביותר של $aabaac$ היא $aabaa$ באורך $5$, וגם הטבלה נותנת $5$ (נבדק מול בדיקה ישירה)."},
        {"type": "numeric", "prompt": "מהו אורך הרישא הפולינדרומית המקסימלית של $S=abacdc$, לפי הערך האחרון בטבלת הרישא של `abacdc#cdcaba`?",
         "answer": 3, "tol": 0,
         "explain": "הרישאות הפולינדרומיות הן $a$ ו-$aba$, ולכן $3$. הערך האחרון בטבלה הוא $3$ (נבדק)."},
        {"type": "numeric", "prompt": "מה יהיה הערך האחרון בטבלת הרישא עבור $S=aaa$ אם שוכחים את המפריד ומריצים על `aaaaaa`?",
         "answer": 5, "tol": 0,
         "explain": "הרישא הארוכה ביותר ששווה לסיפא היא באורך $5$, גדולה מאורך $S$. לכן המפריד חיוני: איתו הערך הוא $3$ (נבדק)."},
        {"type": "text", "prompt": "מהי סיבוכיות הזמן כפונקציה של $n=|S|$? (למשל `O(n^2)`)",
         "accept": ["O(n)", "Θ(n)"], "normalize": "complexity",
         "explain": "המחרוזת באורך $2n+1$ ופונקציית הרישא לינארית באורך הקלט (נמדד: מספר הצעדים גדל לינארית)."},
    ],
    stepsSource="ai-verified")

OL3A = [r"נמיין את המחירים מהקטן לגדול.",
        r"נחלק לזוגות לפי הסדר הממוין: הראשון עם השני, השלישי עם הרביעי, וכן הלאה, ובכל זוג הזול בחינם.",
        r"נחזיר את סכום המחירים שמשלמים (המחיר היקר בכל זוג)."]

add(3, "א",
    rubric=rub(("מיון המחירים בסדר עולה", 3),
               ("חלוקה לזוגות של איברים סמוכים בסדר הממוין", 3),
               ("בכל זוג משלמים על המוצר היקר ומקבלים את הזול בחינם", 2),
               ("החזרת סכום התשלומים", 2)),
    rubricSource="ai-verified",
    pitfalls=["לזווג את הזול ביותר עם היקר ביותר: כל המוצרים היקרים נהפכים לתשלום והחיסכון קטן.",
              "לזווג זוגות סמוכים לפי סדר הקלט בלי למיין.",
              "לסכום את כל המחירים במקום רק את המחיר היקר בכל זוג."],
    steps=[
        {"type": "numeric", "prompt": "המחירים הם $5,1,4,2,8,3$. מהו הסכום המינימלי שרותי משלמת לפי האלגוריתם?",
         "answer": 14, "tol": 0,
         "explain": "אחרי המיון $1,2,3,4,5,8$ הזוגות הם $(1,2),(3,4),(5,8)$ ומשלמים $2+4+8=14$. זהו גם המינימום מבין כל החלוקות לזוגות (נבדק בכוח גס)."},
        {"type": "choice", "prompt": "כיצד האלגוריתם מחלק לזוגות?",
         "options": opts("זוגות סמוכים בסדר הממוין", "הזול ביותר עם היקר ביותר, אחר כך השני בזולותו עם השני ביוקרו וכן הלאה",
                         "זוגות סמוכים לפי סדר הקלט המקורי"), "correctId": "a",
         "explain": "עבור $5,1,4,2,8,3$ האלגוריתם משלם $14$, ואילו זיווג הזול עם היקר וזיווג לפי סדר הקלט משלמים $17$ כל אחד (נבדק בכוח גס)."},
        {"type": "order", "prompt": "סדרו את שלבי האלגוריתם.", "lines": OL3A,
         "explain": "קודם ממיינים, אחר כך מזווגים לפי הסדר הממוין, ובסוף סוכמים."},
    ],
    stepsSource="ai-verified")

OL3B = [r"נמיין את המחירים ונבחר חמדנית את הזוג $(p_1,p_2)$ של שני המוצרים הזולים ביותר.",
        r"יהי $OPT$ אופטימלי שבו $p_1$ מזווג עם $x$ ו-$p_2$ מזווג עם $y$; אז $x,y\ge p_2$ ומשלמים $x+y$.",
        r"נחליף לזוגות $(p_1,p_2)$ ו-$(x,y)$, ואז משלמים $p_2+\max(x,y)$.",
        r"מתקיים $x+y=\max(x,y)+\min(x,y)\ge\max(x,y)+p_2$, כי $\min(x,y)\ge p_2$.",
        r"לכן החלוקה החדשה אינה יקרה יותר, ולכן היא אופטימלית ומכילה את הזוג $(p_1,p_2)$."]
OL3B_BUG = list(OL3B)
OL3B_BUG[3] = r"מתקיים $x+y=\max(x,y)+\min(x,y)\le\max(x,y)+p_2$, כי $\min(x,y)\ge p_2$."

add(3, "ב",
    rubric=rub(("ניסוח הבחירה החמדנית: הזוג $(p_1,p_2)$ של שני המוצרים הזולים ביותר", 3),
               ("פתרון אופטימלי $OPT$ שבו $p_1$ ו-$p_2$ מזווגים עם $x$ ו-$y$, ומחירם $x+y$", 3),
               ("החלפה לזוגות $(p_1,p_2)$ ו-$(x,y)$ ומחיר $p_2+\\max(x,y)$", 3),
               ("אי-השוויון $x+y\\ge\\max(x,y)+p_2$ מכך ש-$\\min(x,y)\\ge p_2$", 3),
               ("מסקנה: החלוקה החדשה אופטימלית ומכילה את הבחירה החמדנית", 3)),
    rubricSource="ai-verified",
    pitfalls=["להניח ש-$p_1$ ו-$p_2$ מזווגים כבר ב-$OPT$ ולדלג על מקרה הפרדתם.",
              "לשכוח שמשלמים על המוצר היקר, כך שבזוג $(x,y)$ המחיר הוא $\\max(x,y)$ ולא $x+y$.",
              "להחליף בלי להשוות את מחיר החלוקה החדשה למחיר $OPT$."],
    steps=[
        {"type": "choice", "prompt": "איזו שיטה משמש הפתרון להוכחת תכונת הבחירה החמדנית?",
         "options": opts("טיעון החלפה: מחליפים בחלוקה אופטימלית זוגות כך שהזוג החמדני יופיע בה, בלי להעלות את המחיר",
                         "אינדוקציה על $n$ בלבד, בלי לדבר על חלוקה אופטימלית",
                         "בדיקת כל החלוקות האפשריות לזוגות"), "correctId": "a",
         "explain": "ההוכחה מתחילה בחלוקה אופטימלית כלשהי $OPT$ ומשנה אותה, כלומר טיעון החלפה."},
        {"type": "numeric",
         "prompt": "נניח $p_1=1$, $p_2=3$ ו-$OPT$ מזווג $(1,5)$ ו-$(3,9)$. בכמה יורד המחיר לאחר ההחלפה ל-$(1,3)$ ו-$(5,9)$?",
         "answer": 2, "tol": 0,
         "explain": "לפני ההחלפה משלמים $5+9=14$, אחריה $3+9=12$, כלומר חיסכון של $2=\\min(x,y)-p_2$ (נבדק, וגם שהחלפה כזו אינה מייקרת באף מקרה אקראי)."},
        {"type": "order", "prompt": "סדרו את שלבי ההוכחה.", "lines": OL3B,
         "explain": "כל שלב נשען על הקודם: בוחרים את הזוג החמדני, מניחים אופטימלי, מחליפים, משווים את המחירים, ומסיקים."},
        {"type": "findbug", "prompt": "בגרסה הבאה שורה אחת שונתה. מצאו אותה.", "lines": OL3B_BUG, "bugIndex": 3,
         "explain": "כיוון אי-השוויון חייב להיות $\\ge$: רק כך המחיר $x+y$ של החלוקה הישנה אינו קטן מהמחיר החדש. עם $\\le$ ההחלפה לא הייתה מוכיחה כלום."},
    ],
    stepsSource="ai-verified")

add(4, "",
    rubric=rub(("רעיון המועמדים: ערך שמופיע לפחות $n/2$ פעמים תופס בממוין $\\lceil n/2\\rceil$ מקומות סמוכים, ולכן נמצא במיקום שהוא כפולה של $\\lceil n/2\\rceil$; כך גם עבור $n/3$", 7),
               ("מציאת המועמדים בעזרת Select (לכל היותר שניים עבור $k$ ושלושה עבור $m$)", 6),
               ("ספירת מספר המופעים של כל מועמד בעזרת מעבר אחד על המערך", 4),
               ("בדיקה מפורשת של $k<m$ ושל 'לפחות' ($\\ge$) ולא שוויון", 4),
               ("סיבוכיות $O(n)$: מספר קבוע של קריאות Select ושל מעברים", 4)),
    rubricSource="ai-verified",
    pitfalls=["לבדוק שוויון ($cnt=n/3$) במקום 'לפחות': ערך שמופיע יותר מ-$n/3$ פעמים ייפסל.",
              "למיין את המערך ($O(n\\log n)$) במקום להשתמש ב-Select הלינארי.",
              "לשכוח את התנאי $k<m$ ולהחזיר זוג שבו הערכים שווים או בסדר הפוך."],
    steps=[
        {"type": "choice", "prompt": "מדוע מספיק לבדוק רק ערכים שנמצאים במיקומים שהם כפולות של $h=\\lceil n/2\\rceil$ בסדר הממוין, כמועמדים עבור $k$?",
         "options": opts("ערך שמופיע לפחות $n/2$ פעמים תופס בממוין לפחות $h$ מקומות סמוכים, וכל $h$ מקומות סמוכים מכילים כפולה של $h$",
                         "ערך כזה חייב להיות הערך הקטן ביותר במערך",
                         "ערך כזה חייב להיות הערך הגדול ביותר במערך"), "correctId": "a",
         "explain": "זו בדיוק הטענה של הפתרון. שתי החלופות האחרות שגויות: במערך $1,2,2,2$ הערך $2$ מופיע לפחות $n/2$ פעמים ואינו המינימום, ובמערך $1,1,1,2$ הערך $1$ מופיע כך ואינו המקסימום (נבדק)."},
        {"type": "numeric", "prompt": "עבור $n=12$ כמה קריאות Select מבצע האלגוריתם בסך הכול (מועמדים עבור $k$ ועבור $m$)?",
         "answer": 5, "tol": 0,
         "explain": "כפולות של $h=6$: המיקומים $6,12$; כפולות של $t=4$: המיקומים $4,8,12$. סך הכול $2+3=5$. לאורך כל $n$ הסכום לא עולה על $5$ (נבדק)."},
        {"type": "numeric",
         "prompt": "המערך הוא $2,1,1,3,1,2,1,2,1$ ($n=9$). האלגוריתם מחזיר זוג $(k,m)$. מהו $k+m$?",
         "answer": 3, "tol": 0,
         "explain": "הערך $1$ מופיע $5$ פעמים ($\\ge4.5$), והערך $2$ מופיע $3$ פעמים ($\\ge3$), ולכן $(k,m)=(1,2)$ והוא הזוג היחיד שמקיים את כל התנאים (נבדק בכוח גס)."},
        {"type": "text", "prompt": "מהי סיבוכיות הזמן של האלגוריתם? (למשל `O(n^2)`)",
         "accept": ["O(n)", "Θ(n)"], "normalize": "complexity",
         "explain": "לכל היותר חמש קריאות Select ולכל היותר חמישה מעברי ספירה, כל אחד לינארי, ועוד לכל היותר $6$ בדיקות זוגות: $O(n)$ (נספר)."},
    ],
    stepsSource="ai-verified")

add(5, "",
    rubric=rub(("תיאור האלגוריתם: בוחרים צלע, מוסיפים את שני קצותיה ל-$C$ ומוחקים מ-$E'$ את כל הצלעות הנוגעות בהם", 3),
               ("טבלה לכל אחת מארבע האיטרציות: הצלע שנבחרה, הקבוצה $C$ והקבוצה $E'$", 8),
               ("הפלט $C=\\{a,b,d,e,f,g,h,i\\}$ ו-$|C|=8$", 2),
               ("הסבר שהצלעות שנבחרו זיווג, ולכן $|C|\\le2\\cdot OPT$", 2)),
    rubricSource="ai-verified",
    pitfalls=["להוסיף ל-$C$ רק קצה אחד של הצלע שנבחרה, או למחוק מ-$E'$ רק את הצלע עצמה ולא את כל הצלעות הנוגעות בקצותיה.",
              "לחשוב שיש הרצה יחידה נכונה: בחירת הצלעות שרירותית, ולכן $C$ ו-$E'$ בכל איטרציה תלויים בבחירה.",
              "להכריז שהפלט הוא כיסוי אופטימלי: האלגוריתם נותן רק קירוב עד פי $2$."],
    steps=[
        {"type": "numeric",
         "prompt": "באיטרציה הראשונה נבחרת הצלע $(a,b)$. כמה צלעות נשארות ב-$E'$ (מתוך $15$ צלעות הגרף)?",
         "answer": 10, "tol": 0,
         "explain": "נמחקות חמש צלעות: $ab,ah,af,bi,bc$. נשארות $10$ (חושב ישירות מרשימת הצלעות)."},
        {"type": "numeric",
         "prompt": "באיטרציה השנייה נבחרת הצלע $(h,g)$. כמה צלעות נשארות ב-$E'$?",
         "answer": 6, "tol": 0,
         "explain": "נמחקות ארבע הצלעות $hg,gf,ih,gd$, ונשארות $6$ (חושב ישירות)."},
        {"type": "choice", "prompt": "מה מאפיין את הצלעות שהאלגוריתם בוחר לאורך ההרצה?",
         "options": opts("אין להן קודקוד משותף, ואי אפשר להוסיף להן צלע בלי קודקוד משותף (זיווג מקסימלי)",
                         "כולן נוגעות באותו קודקוד",
                         "הן יוצרות מסלול אחד",
                         "הן יוצרות עץ פורש של הגרף"), "correctId": "a",
         "explain": "אחרי בחירת צלע נמחקות כל הצלעות הנוגעות בקצותיה, ולכן הצלעות הבאות זרות לה. שלוש האפשרויות האחרות לא מתקיימות בהרצה (נבדק גם על הרצות אקראיות)."},
        {"type": "numeric",
         "prompt": "ההרצה בוחרת בסדר הצלעות $(a,b)$, $(h,g)$, $(i,d)$, $(f,e)$. מהו הגודל $|C|$ של הפלט?",
         "answer": 8, "tol": 0,
         "explain": "כל איטרציה מוסיפה שני קודקודים חדשים: ארבע איטרציות, $|C|=8$ (נבדק בהרצה)."},
        {"type": "numeric", "prompt": "מהו הגודל של כיסוי קודקודים מינימום בגרף זה ($OPT$)?",
         "answer": 4, "tol": 0,
         "explain": "בדיקה בכוח גס על כל הקבוצות מראה ש-$OPT=4$, ולכן $|C|=8=2\\cdot OPT$ ועומד בחסם של הקירוב."},
    ],
    stepsSource="ai-verified")

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
