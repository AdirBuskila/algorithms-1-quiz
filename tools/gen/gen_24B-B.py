# -*- coding: utf-8 -*-
"""Generator for tools/raw/24B-B.json -- algorithms-1 (60172), semester B 2024, second sitting (14.8.2024).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24B-B.py

Source: exam booklet pp.1-17 (cover says "מועד א" with the date 14.8.24; GATE1 treats it as 24B-B).
4 questions x 25 + a 5-point bonus, cap 105.
No answer source exists. The solver wrote solutions (solutionSource "solved", official false) for 11 of 12 items,
pending the refuter. Items: Q1 a,b,c (8/9/8), Q2 a,b (15/10), Q3 a,b,c (15/5/5), Q4 a,b,c (5/10/10), bonus (5).
- Q2b: the question text is missing from the booklet (p.6 shows only a stray "A. ..." line and the empty answer
  box "פתרון סעיף ב'"); still held, points 10 inferred from 25 - 15.
- Bonus: the figure (suffix tree, cropped from p.14) belongs to a text T that is not printed; the garbled root-to-leaf-0
  label reads RATATAT. The tree itself forces T[1..6] = ATATAT (leaves 1..7 spell ATATAT$, TATAT$, ..., $) and a
  first letter outside {A,T}; the answer ATAT does not depend on that letter. Kind changed truefalse -> computation
  (it asks for a string, not a verdict). Graph data: tools/verify/24B-B/graphs.json.

Solver notes
- Q1b assumes no self-loops (a vertex x with only the loop (x,x) would satisfy the degree condition and break the
  claim). The a/b/c gradation (no condition / in- and out-degree / degree sum) fits the simple-graph reading.
- Q2a assumes every letter with a code occurs at least once in S (c=0 would add the pair (0,4)).
- Q3b/c: the answer is for the recurrence given in Q3a (two-pointer prev): O(n) time, O(n) space for both.

Checks: tools/verify/24B-B/checks.py (reference facts), solve_q1_q2.py (Q1 exhaustive over all directed graphs on
<=4 vertices with every DFS root order and two adjacency orders + a random lemma check; Q2a hand conditions against
an exhaustive tie-aware Huffman search), solve_q3_q4_q5.py (Q3 DP + reconstruction vs brute force on 3000 random
inputs with negative profits; Q4 greedy vs brute force; bonus: suffixes read off the tree, longest repeat ATAT).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24B-B.json"


def Q(num, part, kind, topic, question, solution, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution,
         "solutionSource": "solved", "official": False, "confidence": "high"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


C1 = (r"יהיו $G=(V,E)$ גרף מכוון, $s\in V$ וגם $|E|\neq\emptyset$. נסמן $E_{BFS}$ - קבוצת קשתות של עץ BFS לאחר הרצה $BFS(G,s)$, "
      r"$E_{DFS}$ - קבוצת קשתות של יער DFS לאחר הרצה $DFS(G)$ **שמתחילה מצומת $s$** וממשיכה את הסריקה של כל הגרף." "\n"
      r"שלוש הטענות הבאות מתייחסות לגרף זה." "\n"
      r"כתבו נכון או לא נכון על כל הטענה, נמקו תשובתכם (אם הטענה לא נכונה, הביאו דוגמה נגדית, ואם הינה נכונה, הסבירו מדוע):")

C3 = (r"IGreg שוקלת לפתוח שורה של מסעדות לאורך הכביש 40 מפתח-תקווה עד מצפה רמון. המיקומים הזמינים הם לאורך הכביש; "
      r"המרחקים (בקילומטרים) של מיקומים אלה מתחילת הכביש בפתח-תקווה הם: $d_1<d_2<\cdots<d_n$." "\n"
      r"ההגבלות הן כדלקמן:" "\n"
      r"1. בכל מקום, IGreg רשאית לפתוח מסעדה אחת לכל היותר. הרווח הצפוי מפתיחת מסעדה במקום $d_i$ הוא $p_i$." "\n"
      r"2. כל שתי מסעדות צריכות להיות במרחק של $k$ קילומטרים לפחות זה מזה." "\n"
      r"הציעו אלגוריתם יעיל לחישוב הרווח הכולל המקסימלי הצפוי בכפוף לאילוצים הנתונים." "\n"
      r"הבעיה ניתנת לפתרון בתכנון דינמי.")

C4 = (r"נשנה קצת את הבעיה משאלה 3. IGreg שוקלת לפתוח שורה של מסעדות לאורך הכביש 40 מפתח-תקווה עד מצפה רמון. המיקומים הזמינים הם לאורך הכביש; "
      r"המרחקים (בקילומטרים) של מיקומים אלה מתחילת הכביש בפתח-תקווה הם: $d_1<d_2<\cdots<d_n$." "\n"
      r"ההגבלות הן כדלקמן:" "\n"
      r"1. בכל מקום, IGreg רשאית לפתוח מסעדה אחת לכל היותר. הרווח הצפוי מפתיחת מסעדה הוא $p$, ולא תלוי במיקום." "\n"
      r"2. כל שתי מסעדות צריכות להיות במרחק של $k$ קילומטרים לפחות זה מזה." "\n"
      r"הציעו אלגוריתם יעיל לחישוב הרווח הכולל המקסימלי הצפוי בכפוף לאילוצים הנתונים." "\n"
      r"**לדוגמה:** עבור $n=8$ המיקומים: $[1,2,15,20,26,27,30,35]$ ומרחק $k=10$, קיים פתרון אופטימלי עם 3 מסעדות: $[2,20,30]$." "\n"
      r"הבעיה ניתנת לפתרון באמצעות **אלגוריתם חמדן**.")

# ---------------------------------------------------------------- solutions (solver)
SOL_1A = r"""**לא נכון.**
דוגמה נגדית: $V=\{s,a,b\}$ ו-$E=\{(s,a),(b,s)\}$.
- $BFS(G,s)$ מגלה רק את $a$, ולכן $E_{BFS}=\{(s,a)\}$.
- ה-DFS מתחיל ב-$s$ ומגלה את $a$ בקשת העץ $(s,a)$. אחר כך הסריקה ממשיכה מ-$b$: השכן היחיד של $b$ הוא $s$, שכבר התגלה, ולכן $b$ הוא עץ בודד בלי קשתות. מכאן $E_{DFS}=\{(s,a)\}$.

כלומר $E_{DFS}=E_{BFS}$, אבל אין מסלול מ-$s$ ל-$b$, ולכן $s$ אינו שורש."""

SOL_1B = r"""**נכון** (בגרף מכוון בלי לולאות עצמיות, כמקובל).
נסמן ב-$R$ את קבוצת הצמתים הישיגים מ-$s$, וב-$U=V\setminus R$ את השאר. נניח בשלילה ש-$U\neq\emptyset$.
1. אין קשת מצומת ב-$R$ לצומת ב-$U$, אחרת הקצה שלה היה ישיג מ-$s$. לכן כל קשת שנכנסת לצומת ב-$U$ יוצאת מצומת ב-$U$.
2. BFS מגלה רק צמתים ישיגים מ-$s$, ולכן כל הקשתות של $E_{BFS}$ הן בין צמתים של $R$.
3. לכל $x\in U$ מתקיים $deg^-(x)\neq0$, ולפי 1 יש לו שכן נכנס ב-$U$. נצא מצומת כלשהו ב-$U$ ונלך אחורה לאורך קשתות נכנסות. הגרף סופי, ולכן נחזור על צומת: יש ב-$U$ מעגל מכוון $C$, באורך 2 לפחות כי אין לולאות.
4. ה-DFS מתחיל ב-$s$, ועץ ה-DFS של $s$ מכיל בדיוק את $R$ (משפט המסלול הלבן). לכן כל צמתי $R$ מתגלים לפני כל צומת של $U$.
5. יהי $v$ הצומת הראשון של $C$ שמתגלה, ו-$w$ הצומת שאחריו במעגל. כשמגלים את $v$, הצומת $w$ עדיין לבן והקשת $(v,w)$ היא מסלול לבן, ולכן $w$ יהיה צאצא של $v$. קשת העץ שנכנסת ל-$w$ יוצאת מצאצא של $v$. צאצאי $v$ מתגלים אחרי $v$, ואילו כל צמתי $R$ התגלו לפניו, ולכן גם הזנב של קשת זו נמצא ב-$U$.

קיבלנו ב-$E_{DFS}$ קשת ששני קצותיה ב-$U$. לפי 2 היא אינה ב-$E_{BFS}$, בסתירה ל-$E_{DFS}=E_{BFS}$. לכן $U=\emptyset$ ו-$s$ שורש.
הערה: ההוכחה משתמשת רק בתנאי $deg^-(x)\neq0$. אם מתירים לולאות עצמיות, הטענה נכשלת: $V=\{s,x\}$, $E=\{(s,s),(x,x)\}$."""

SOL_1C = r"""**לא נכון.**
אותה דוגמה נגדית כמו בסעיף א: $V=\{s,a,b\}$, $E=\{(s,a),(b,s)\}$.
סכומי הדרגות: $s$ - 2, $a$ - 1, $b$ - 1, כולם שונים מ-0. כמו בסעיף א, $E_{BFS}=E_{DFS}=\{(s,a)\}$, אבל $b$ אינו ישיג מ-$s$, ולכן $s$ אינו שורש.
ההבדל מסעיף ב: כאן מותר לצומת שאינו ישיג להיות בעל דרגת כניסה 0 (כמו $b$). צומת כזה מתגלה ב-DFS כעץ בודד בלי קשתות, ולכן אינו פוגע בשוויון."""

SOL_2A = r"""**התשובה:** $(c,d)\in\{(1,3),(1,4),(2,2),(2,3),(2,4),(3,3),(3,4)\}$.
**מבנה העץ לפי הקוד:** מתחת לשורש, בצד 0 נמצאים $b$ (`00`) וצומת פנימי $X$ (`01`) שילדיו $c$ (`010`) ו-$d$ (`011`). בצד 1 נמצאים $a$ (`10`) ו-$e$ (`11`). נסמן $x=c+d$, שכיחות הצומת $X$.
נניח שכל אות שיש לה קוד מופיעה ב-$S$, כלומר $c,d\ge1$.
**תנאי הופמן** (בכל שלב מאחדים שני מינימליים, ושוויונות נשברים לטובת העץ הנתון):
1. האיחוד הראשון יוצר צומת ששני ילדיו עלים: $\{c,d\}$ או $\{a,e\}$. האיחוד $\{a,e\}$ דורש ש-7 ו-7 יהיו שני הקטנים, וזה בלתי אפשרי כי $b=4$. לכן $c,d$ הם שני הקטנים מבין $7,4,7,c,d$, כלומר $c,d\le4$.
2. נשארו $a=7,\ b=4,\ e=7,\ X=x$. האיחוד הבא חייב להיות $\{b,X\}$ (איחוד $a,e$ שוב דורש $b\ge7$), ולכן $x\le7$.
3. נשארו $a=7,\ e=7,\ \{b,X\}=4+x$. כדי לאחד את $a$ עם $e$ צריך $4+x\ge7$, כלומר $x\ge3$.

**תנאי האחים** (האח השמאלי לא גדול מהימני):
- $c\le d$.
- $b\le X$, כלומר $x\ge4$.
- $a\le e$: $7\le7$, מתקיים.
- $4+x\le14$, כלומר $x\le10$.

**סיכום:** $1\le c\le d\le4$ וגם $4\le c+d\le7$. שבעת הזוגות שעומדים בתנאים הם אלה שבתשובה. לדוגמה, עבור $(3,4)$: $x=7$, ובאיחוד השני יש שוויון בין $X=7$ לבין $a,e$, והוא נשבר לטובת $X$."""

SOL_3A = r"""נסמן ב-$prev(i)$ את האינדקס הגדול ביותר $j<i$ המקיים $d_i-d_j\ge k$, ו-$prev(i)=0$ אם אין כזה.
נגדיר $OPT(i)$ - הרווח הכולל המקסימלי כשמותר לפתוח מסעדות רק במקומות $d_1,\ldots,d_i$.
$$OPT(i)=\begin{cases}0 & ;\ i=0\\ \max\bigl(OPT(i-1),\ p_i+OPT(prev(i))\bigr) & ;\ i\ge1\end{cases}$$
התשובה היא $OPT(n)$.
**נכונות:** נתבונן בפתרון אופטימלי למקומות $1..i$.
- אם לא פותחים מסעדה ב-$d_i$, הפתרון הוא פתרון חוקי למקומות $1..i-1$, ולכן ערכו $OPT(i-1)$.
- אם פותחים ב-$d_i$, כל שאר המסעדות במרחק $k$ לפחות ממנה. המקומות ממוינים, ולכן אלה בדיוק המקומות $1..prev(i)$: כל $j\le prev(i)$ מקיים $d_i-d_j\ge k$, וכל $prev(i)<j<i$ קרוב מדי. בין המסעדות האלה האילוץ הוא אותו אילוץ, ולכן החלק הזה הוא פתרון אופטימלי למקומות $1..prev(i)$ (אחרת מחליפים אותו בטוב יותר). ערכו $p_i+OPT(prev(i))$.

המקסימום בין שתי האפשרויות הוא $OPT(i)$."""

SOL_3B = r"""**זמן $O(n)$, מקום $O(n)$.**
- **חישוב $prev$:** המקומות ממוינים, ולכן $prev(i)$ לא יורד כש-$i$ עולה. מחשבים את כל הערכים בשני מצביעים, שכל אחד מהם רק מתקדם, בזמן $O(n)$ בסך הכול. חיפוש בינארי לכל $i$ נותן $O(n\log n)$.
- **מילוי הטבלה:** יש $n+1$ תאים $OPT(0..n)$, וכל תא מחושב ב-$O(1)$ ממקסימום של שני ערכים שכבר חושבו. לכן הזמן הכולל הוא $O(n)$.
- **מקום:** מערך $OPT$ ומערך $prev$, $O(n)$. אי אפשר להסתפק בשני ערכים אחרונים, כי $OPT(prev(i))$ יכול להיות רחוק מ-$i$."""

SOL_3C = r"""**זמן $O(n)$, מקום $O(n)$.**
ממלאים את אותה טבלה $OPT$ ($O(n)$ זמן ומקום, כמו בסעיף ב), ואז משחזרים אחורה:
- מתחילים ב-$i=n$.
- אם $OPT(i)=OPT(i-1)$, עוברים ל-$i-1$.
- אחרת, פותחים מסעדה ב-$d_i$ ועוברים ל-$prev(i)$.
- עוצרים כש-$i=0$.

כל צעד מקטין את $i$, ולכן השחזור לוקח $O(n)$. צריך לשמור את כל הטבלה ואת $prev$ כדי לשחזר, וגם הפלט עצמו יכול להכיל עד $n$ מקומות. לכן המקום הוא $O(n)$."""

SOL_4A = r"""**לא, הפתרון האופטימלי אינו יחיד.**
3 היא הכמות המקסימלית: לפי סעיף ג האלגוריתם החמדן אופטימלי, והוא מחזיר כאן 3 מסעדות.
פתרונות אופטימליים נוספים על $[2,20,30]$:
- הפתרון החמדן $[1,15,26]$: המרחקים 14 ו-11, שניהם לפחות 10.
- הפתרונות $[1,15,27]$ ו-$[2,15,26]$ (ויש עוד)."""

SOL_4B = r"""אסטרטגיה חמדנית: פותחים מסעדה במקום הראשון, ובכל פעם בוחרים את המקום הבא הראשון שמרחקו לפחות $k$ מהמסעדה האחרונה שנפתחה.
```
Restaurants(d[1..n], k, p):
    if n == 0: return 0, []
    S = [d[1]]                 // the first location is always opened
    last = d[1]
    for i = 2 to n:
        if d[i] - last >= k:   // far enough from the last opened restaurant
            S.append(d[i])
            last = d[i]
    return p * |S|, S
```
זמן הריצה $O(n)$, כי המקומות כבר ממוינים. נניח $p>0$: הרווח הוא $p$ כפול מספר המסעדות, ולכן ממקסמים את מספר המסעדות."""

SOL_4C = r"""נסמן את הפתרון החמדן $g_1<g_2<\cdots<g_m$ ופתרון אופטימלי כלשהו $o_1<o_2<\cdots<o_t$ (מיקומים).
**טענה ("החמדן מקדים"):** לכל $r\le\min(m,t)$ מתקיים $g_r\le o_r$.
**הוכחה באינדוקציה:**
- **בסיס:** $g_1=d_1$ הוא המקום הקטן ביותר, ולכן $g_1\le o_1$.
- **צעד:** נניח $g_r\le o_r$. אז $o_{r+1}\ge o_r+k\ge g_r+k$, כלומר $o_{r+1}$ הוא מקום שמרחקו לפחות $k$ מ-$g_r$. החמדן בוחר את המקום הראשון כזה, ולכן $g_{r+1}\le o_{r+1}$.

**אופטימליות:** נניח בשלילה ש-$t>m$. לפי הטענה $g_m\le o_m$, ולכן $o_{m+1}\ge o_m+k\ge g_m+k$. אז אחרי $g_m$ קיים מקום במרחק $k$ לפחות, והחמדן היה פותח מסעדה נוספת. זו סתירה לכך שהוא עצר אחרי $m$ מסעדות.
לכן $m\ge t$. הפתרון החמדן חוקי (כל מסעדה נבחרת במרחק $k$ לפחות מהקודמת), ולכן $m=t$ והרווח $p\cdot m$ מקסימלי."""

SOL_5 = r"""**ATAT**
**קריאת $T$ מהעץ:** בעץ 8 עלים, ולכן $|T|=7$ (עם $\text{\textdollar}$). המסלולים מהשורש לעלים 1 עד 7 נותנים את הסיפות $\mathrm{ATATAT}\text{\textdollar},\ \mathrm{TATAT}\text{\textdollar},\ \ldots,\ \text{\textdollar}$. מכאן $T[1..6]=\mathrm{ATATAT}$.
לשורש יש ילדים $\text{\textdollar}$, $\mathrm{A}$, $\mathrm{T}$ ועלה 0. לכן האות הראשונה של $T$ אינה $\mathrm{A}$ או $\mathrm{T}$, ובאיור היא $\mathrm{R}$: $T=\mathrm{RATATAT}$.
**התשובה:** תת-מחרוזת חוזרת היא מסלול מהשורש לצומת פנימי (לצומת יש לפחות שני עלים, כלומר שתי הופעות). הצומת הפנימי העמוק ביותר הוא שורש $\to\mathrm{AT}\to\mathrm{AT}$, בעומק 4. לכן התשובה היא $\mathrm{ATAT}$, שמופיעה בתחילת הסיפות 1 ו-3.
התשובה אינה תלויה באות הראשונה, כל עוד היא שונה מ-$\mathrm{A}$ ומ-$\mathrm{T}$."""

questions = [
    Q(1, "א", "truefalse", "graph_proofs",
      r"אם $E_{DFS}=E_{BFS}$, אזי $s$ הוא שורש (צומת שממנו יש מסלול לכל צומת בגרף).", SOL_1A,
      points=8, contextId="c1", verdict=False),
    Q(1, "ב", "truefalse", "graph_proofs",
      r"אם $E_{DFS}=E_{BFS}$ וגם דרגת כניסה $deg^-(x)\neq 0$ וגם דרגת יציאה $deg^+(x)\neq 0$ שונות מ-0 לכל צומת $x\in V$, אזי $s$ הוא שורש.",
      SOL_1B, points=9, contextId="c1", verdict=True),
    Q(1, "ג", "truefalse", "graph_proofs",
      r"אם $E_{DFS}=E_{BFS}$ וגם סכום דרגות כניסה וגם יציאה $deg^+(x)+deg^-(x)\neq 0$ שונות מ-0 לכל צומת $x\in V$, אזי $s$ הוא שורש.",
      SOL_1C, points=8, contextId="c1", verdict=False),

    Q(2, "א", "computation", "huffman",
      r"עבור מחרוזת $S$ מעל א\"ב $\Sigma=\{a,b,c,d,e\}$ נתון כי:" "\n"
      r"- האות $a$ מופיעה 7 פעמים, האות $b$ מופיעה 4 פעמים והאות $e$ מופיעה 7 פעמים." "\n"
      r"- קוד הופמן של האותיות הוא: $a$ - `10`, $b$ - `00`, $c$ - `010`, $d$ - `011`, $e$ - `11`." "\n"
      r"- מספר ההופעות של \"אח\" השמאלי הוא לא יותר גדול ממספר ההופעות של \"אח\" הימני." "\n"
      r"הניחו שסיבית הקוד לצומת הימני היא 1 ולשמאלי 0." "\n"
      r"רשמו את כל האופציות האפשריות לשכיחויות של אותיות $c$ ו-$d$ במחרוזת $S$. נמקו את תשובתכם.",
      SOL_2A, points=15),
    {"num": 2, "part": "ב", "kind": "algorithm", "points": 10,
     "hold": "no-key: the question text of Q2b is missing from the booklet (p.6 shows only a stray 'A. ...' line and the empty answer box); no answer source either"},

    Q(3, "א", "algorithm", "dp_optimization",
      r"הציגו נוסחה רקורסיבית לחישוב הרווח הכולל המקסימלי. יש להגדיר (במילים) את הפונקציה הרקורסיבית ולנמק בקצרה את הנכונות של הנוסחה.",
      SOL_3A, points=15, contextId="c3"),
    Q(3, "ב", "computation", "complexity_recurrence",
      r"מה סיבוכיות הזמן וסיבוכיות המקום לאלגוריתם תכנון דינמי למציאת הרווח הכולל המקסימלי? נמקו תשובתכם (אין צורך לפרט את האלגוריתם עצמו).",
      SOL_3B, points=5, contextId="c3"),
    Q(3, "ג", "computation", "complexity_recurrence",
      r"מה סיבוכיות הזמן וסיבוכיות המקום של אלגוריתם תכנון דינמי המחזיר את הפתרון עצמו - המקומות למסעדות? נמקו את תשובתכם (אין צורך לפרט את האלגוריתם עצמו).",
      SOL_3C, points=5, contextId="c3"),

    Q(4, "א", "computation", "greedy",
      r"האם קיים פתרון אופטימלי יחיד לבעיה? אם כן, נמקו תשובתכם. אם לא, הציגו פתרון נוסף (לא בהכרח חמדן) עבור הדוגמה.",
      SOL_4A, points=5, contextId="c4"),
    Q(4, "ב", "algorithm", "greedy", r"כתבו אלגוריתם (או פסודו-קוד) לפתרון הבעיה.", SOL_4B, points=10, contextId="c4"),
    Q(4, "ג", "proof", "greedy", r"הוכיחו שהאלגוריתם שפיתחתם מחזיר פתרון אופטימלי.", SOL_4C, points=10, contextId="c4"),

    Q(5, None, "computation", "suffix_structures",
      r"**שאלת בונוס (5 נקודות)** - ענו, אין צורך לנמק." "\n"
      r"נתון suffix tree עבור מחרוזת $T$." "\n"
      r"מהי תת-המחרוזת (רצף אותיות) החוזרת (שמופיעה לפחות פעמיים ב-$T$) הארוכה ביותר? (אין צורך לנמק)",
      SOL_5, points=5, image="images/exams/24B-B-Q5-suffix-tree.png"),
]

exam = {
    "examCode": "24B-B",
    "examLabel": "אלגוריתמים 1 (60172), סמסטר ב' תשפ\"ד, מועד ב (14.8.2024)",
    "year": 2024,
    "examDate": "14.8.2024",
    "sourceFile": "24B-B exam pp.1-17 (cover says moed A, dated 14.8.24)",
    "solutionFile": "none (no answer source; solutions written by the solver)",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1: BFS ו-DFS בגרף מכוון", "text": C1},
        "c3": {"kind": "text", "title": "שאלה 3: מסעדות לאורך כביש 40", "text": C3},
        "c4": {"kind": "text", "title": "שאלה 4: מסעדות עם רווח קבוע", "text": C4},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
