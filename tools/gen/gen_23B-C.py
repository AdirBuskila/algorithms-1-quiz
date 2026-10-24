# -*- coding: utf-8 -*-
"""Generator for tools/raw/23B-C.json -- algorithms-1 (60172), semester B 2023, special sitting (24.08.23).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_23B-C.py

Source: the blank exam booklet (scan, 30 pages: cover, answer boxes, a page of allowed black-box algorithms, 4 draft pages).
There is NO answer source for this sitting (no solution file, no student paper). The solver wrote all 8 solutions
(solutionSource "solved", official false, 2026-10-24), pending the refuter. Q1 and Q3 print one 30-point total, so their
parts carry no points.
Cover: 2.5 h, closed material except the last-page list of black-box algorithms, 4 questions (all compulsory),
cap 110, "unanswered = 20% of the points".
Items: Q1 a,b (30 points together, the split is not printed), Q2 a,b (25/15), Q3 a,b,c (30 together, split not printed), Q4 (10).

Transcription notes
- Q1a: the printed sequence is "0, 1, 2, 3, 1" (as rendered on the page, left to right).
- Q2b: positions are 1-based in the printed example (K=5 keeps the 15).
- Q3 cost matrix: rows are houses 1-3, columns R, B, G: (14,2,11), (11,14,5), (14,3,19).

Solver notes
- Q1a: the answer (no such string) holds for both bidi readings of the printed sequence: 0,1,2,3,1 is impossible
  (P[1..4]=aaaa forces pi(5) in {0,4}) and 1,3,2,1,0 is impossible (pi(1)=0 always). The solution says so.
- Q1b: suffix array 1-based without $ (the course's convention in 24B-A); the tree uses the terminator $.
- Q3: the text says cost is 3 x n with rows = houses; the example table is n x 3 (rows = houses). The solution
  uses cost[i][colour], rows = houses, as the example.
- Q4: answer assumes c and d occur in S (frequency >= 1); with 0 allowed, (0,7) is the one extra pair (noted).
Checks: tools/verify/23B-C/solve_23BC.py: all 5^5 strings for Q1a; suffix tree / array rebuilt naively; Q2a formula vs
every circular segment (3000 random); Q2b vs brute force over permutations; Q3 DP vs all colourings (500 random)
and the example table; Q4 by enumerating every Huffman run (all tie breaks, both sibling orders on ties) for
c,d in 0..24.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "23B-C.json"


def H(num, part, kind, topic, question, sol, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question,
         "solution": sol, "solutionSource": "solved", "official": False, "confidence": "high"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


SOL = "**פתרון** (אין פתרון רשמי לבחינה זו; הפתרון נכתב ונבדק במחשב):\n"

SOL_1A = SOL + r"""**לא קיימת** מחרוזת כזו.
נניח ש-$\pi=0,1,2,3,1$ עבור $P=P[1..5]$.
- $\pi(2)=1$: הרישא $P[1]$ שווה לסיפא $P[2]$, כלומר $P[2]=P[1]$. נסמן את התו הזה $a$.
- $\pi(3)=2$: $P[1..2]=P[2..3]$, ולכן $P[3]=P[2]=a$.
- $\pi(4)=3$: $P[1..3]=P[2..4]$, ולכן $P[4]=a$. כלומר $P[1..4]=aaaa$.
- $\pi(5)$: אם $P[5]=a$ אז $P=aaaaa$ ו-$\pi(5)=4$. אם $P[5]\ne a$, כל גבול (רישא שהיא גם סיפא) של $P$ צריך להתחיל ב-$a$ ולהסתיים ב-$P[5]\ne a$. אבל כל רישא של $P$ באורך $1$ עד $4$ מסתיימת ב-$a$, ולכן אין גבול כזה ו-$\pi(5)=0$.

בכל מקרה $\pi(5)\in\{0,4\}$, ולעולם לא $1$. (באותו אופן לפי חישוב KMP: $\pi(5)$ הוא $k+1$ עבור $k$ בשרשרת $3,2,1,0$ שבה $P[k+1]=P[5]$, או $0$. כל ה-$P[k+1]$ הם $a$, ולכן או שהערך הגדול $4$ מתקבל או $0$.)
**הערת קריאה:** בעמוד המודפס הסדרה מופיעה בתוך שורה עברית. גם אם קוראים אותה בסדר ההפוך, $1,3,2,1,0$, אין מחרוזת כזו, כי תמיד $\pi(1)=0$."""

SOL_1B = SOL + r"""**Suffix array** (אינדקסים מ-$1$): ממיינים את הסיפות של `algogoal` לפי סדר מילוני:
`al` ($7$) < `algogoal` ($1$) < `goal` ($5$) < `gogoal` ($3$) < `l` ($8$) < `lgogoal` ($2$) < `oal` ($6$) < `ogoal` ($4$).
$$SA=[7,1,5,3,8,2,6,4]$$
(אם מוסיפים את התו $\text{\textdollar}$ כסיפא הקטנה ביותר, הוא נכנס ראשון: $[9,7,1,5,3,8,2,6,4]$.)

**Suffix tree** של $\mathtt{algogoal}\text{\textdollar}$ (העלה $i$ מייצג את הסיפא שמתחילה במקום $i$). מהשורש יוצאות חמש צלעות:
- הצלע `al` לקודקוד פנימי עם שני בנים: הצלע $\mathtt{gogoal}\text{\textdollar}$ לעלה $1$ והצלע $\text{\textdollar}$ לעלה $7$.
- הצלע `go` לקודקוד פנימי עם שני בנים: הצלע $\mathtt{goal}\text{\textdollar}$ לעלה $3$ והצלע $\mathtt{al}\text{\textdollar}$ לעלה $5$.
- הצלע `l` לקודקוד פנימי עם שני בנים: הצלע $\mathtt{gogoal}\text{\textdollar}$ לעלה $2$ והצלע $\text{\textdollar}$ לעלה $8$.
- הצלע `o` לקודקוד פנימי עם שני בנים: הצלע $\mathtt{goal}\text{\textdollar}$ לעלה $4$ והצלע $\mathtt{al}\text{\textdollar}$ לעלה $6$.
- הצלע $\text{\textdollar}$ לעלה $9$.

בדיקה: יש $9$ עלים ($9$ סיפות של $\mathtt{algogoal}\text{\textdollar}$), וכל קודקוד פנימי מתפצל לפחות לשניים. הקודקודים הפנימיים הם בדיוק המחרוזות שמופיעות פעמיים עם המשך שונה: `al`, `go`, `l`, `o` (למשל `go` מופיעה במקומות $3$ ו-$5$ וממשיכה ב-`g` וב-`a`)."""

SOL_2A = SOL + r"""**רעיון:** הרצף המקסימלי במערך המעגלי הוא מאחד משני סוגים:
1. רצף **שאינו עובר** מהסוף להתחלה: זה רצף רגיל, והסכום המקסימלי שלו הוא $\mathrm{Kadane}(A,n)$.
2. רצף **שעובר** מהסוף להתחלה: המשלים שלו (מה שנשאר במעגל) הוא רצף רגיל ולא ריק באמצע המערך. סכום הרצף הוא $\text{sum}(A)$ פחות סכום המשלים, ולכן כדי למקסם אותו צריך למצוא את הרצף הרגיל עם הסכום **המינימלי**. רצף מינימלי ב-$A$ הוא רצף מקסימלי ב-$-A$, ולכן הסכום המינימלי הוא $-\mathrm{Kadane}(-A,n)$.
```
CircularMax(A, n):
  m1 <- Kadane(A, n)                 // best segment that does not wrap
  if m1 < 0:  return m1              // all numbers are negative
  total <- A[1] + ... + A[n]
  for i <- 1 to n:  B[i] <- -A[i]
  minSeg <- -Kadane(B, n)            // smallest sum of a (non-wrapping) segment
  return max(m1, total - minSeg)     // best wrapping segment = total - minSeg
```
**נכונות:** כל רצף מעגלי שייך לאחד משני הסוגים, ובכל סוג המקסימום מחושב נכון. מקרה קצה: אם כל המספרים שליליים, הרצף המינימלי הוא כל המערך ו-$\text{total}-\text{minSeg}=0$ מתאים לרצף **ריק**, שאינו מותר; לכן מחזירים $m1$ (האיבר הגדול ביותר). אם $m1\ge 0$, גם כשהמשלים הוא כל המערך מתקבל $0\le m1$, כך שהמקרה הזה אינו משנה את המקסימום.
**דוגמה:** $4,-6,5,-6,10,-5,3$: $m1=10$, $\text{total}=5$, הרצף המינימלי הוא $-6,5,-6$ עם סכום $-7$, ולכן $5-(-7)=12=10-5+3+4$.
**סיבוכיות:** שתי קריאות ל-$\mathrm{Kadane}$ ($O(n)$ כל אחת), סכום ושלילה ב-$O(n)$. סה"כ $O(n)$ זמן, ו-$O(n)$ מקום למערך $B$ (אפשר גם $O(1)$ אם הופכים סימן במקום ומחזירים בסוף)."""

SOL_2B = SOL + r"""**אלגוריתם:**
```
SortExceptK(A, n, K):
  x <- A[K]
  B <- A[1..K-1] followed by A[K+1..n]      // n-1 numbers, O(n)
  MergeSort(B)                              // O(n log n)
  return B[1..K-1], x, B[K..n-1]           // x goes back to place K
```
**נכונות:** האיבר במקום $K$ נשאר במקומו, וכל שאר האיברים יוצאים בסדר עולה סביבו, וזה בדיוק הנדרש.
**דוגמה:** $A=4,10,-6,3,15,-8,7$, $K=5$: $x=15$, $B=4,10,-6,3,-8,7$, אחרי מיון $-8,-6,3,4,7,10$. מחזירים $-8,-6,3,4,\mathbf{15},7,10$.
**סיבוכיות:** $O(n\log n)$ זמן (המיון שולט), $O(n)$ מקום. אי אפשר לעשות טוב יותר במודל ההשוואות: הפלט כולל מיון של $n-1$ מספרים כלליים, ומיון מבוסס השוואות דורש $\Omega(n\log n)$."""

SOL_3A = SOL + r"""נגדיר לכל $1\le i\le n$ שלוש פונקציות:
- $R(i)$ = העלות המינימלית לצביעת הבתים $1..i$ (חוקית) כשהבית $i$ **אדום**.
- $B(i)$ = כנ"ל כשהבית $i$ **כחול**.
- $G(i)$ = כנ"ל כשהבית $i$ **ירוק**.

**בסיס:** $R(1)=\mathrm{cost}[1][1]$, $B(1)=\mathrm{cost}[1][2]$, $G(1)=\mathrm{cost}[1][3]$.
**נוסחה** לכל $i\ge 2$:
$$R(i)=\mathrm{cost}[i][1]+\min\bigl(B(i-1),G(i-1)\bigr)$$
$$B(i)=\mathrm{cost}[i][2]+\min\bigl(R(i-1),G(i-1)\bigr)$$
$$G(i)=\mathrm{cost}[i][3]+\min\bigl(R(i-1),B(i-1)\bigr)$$
**התשובה:** $\min\bigl(R(n),B(n),G(n)\bigr)$.
**נכונות** (למשל עבור $R(i)$): בצביעה חוקית שבה הבית $i$ אדום, הבית $i-1$ כחול או ירוק, והבתים $1..i-1$ צבועים בעצמם חוקית. העלות היא $\mathrm{cost}[i][1]$ ועוד עלות הצביעה של $1..i-1$, שהיא לפחות $B(i-1)$ או לפחות $G(i-1)$ לפי צבע הבית $i-1$; לכן $R(i)\ge \mathrm{cost}[i][1]+\min(B(i-1),G(i-1))$. בכיוון השני, לוקחים צביעה אופטימלית של $1..i-1$ שמסתיימת בצבע שממנו בא המינימום (כחול או ירוק) ומוסיפים בית $i$ אדום: הצביעה חוקית כי $i-1$ אינו אדום, ומשיגה את הערך. אותו טיעון עבור $B$ ו-$G$. הבית האחרון צבוע באחד משלושת הצבעים, ולכן התשובה היא המינימום של שלושתם."""

SOL_3B = SOL + r"""ממלאים את הטבלה עמודה אחר עמודה (בית אחר בית):
- בית $1$: $R=14$, $B=2$, $G=11$.
- בית $2$: $R=11+\min(2,11)=13$, $B=14+\min(14,11)=25$, $G=5+\min(14,2)=7$.
- בית $3$: $R=14+\min(25,7)=21$, $B=3+\min(13,7)=10$, $G=19+\min(13,25)=32$.

$$\begin{array}{c|ccc} & 1 & 2 & 3\\ \hline R & 14 & 13 & 21\\ B & 2 & 25 & 10\\ G & 11 & 7 & 32 \end{array}$$
העלות המינימלית: $\min(21,10,32)=10$. שחזור: בית $3$ כחול ($10=3+7$), ולכן בית $2$ ירוק ($7=5+2$), ולכן בית $1$ כחול ($2$). הצביעה $B,G,B$ עולה $2+5+3=10$."""

SOL_3C = SOL + r"""**זמן:** $O(n)$. בטבלה $3n$ תאים, וכל תא מחושב ב-$O(1)$ (מינימום של שני ערכים ועוד חיבור). המינימום הסופי $O(1)$.
**מקום:** $O(n)$ לטבלה (נחוצה אם רוצים לשחזר את הצביעה עצמה). אם צריך רק את העלות, מספיק לשמור את העמודה הקודמת: $O(1)$."""

SOL_4 = SOL + r"""**מבנה העץ** לפי הקודים ($0$ שמאלה, $1$ ימינה):
- השורש: בשמאל צומת $X$ (קודים שמתחילים ב-$0$), בימין צומת $Z$ (קודים שמתחילים ב-$1$).
- $Z$: בשמאל $a$ ($10$), בימין $e$ ($11$). משקלו $10+10=20$.
- $X$: בשמאל $b$ ($00$), בימין צומת $Y$ (קודים $01x$). משקלו $7+c+d$.
- $Y$: בשמאל $c$ ($010$), בימין $d$ ($011$). משקלו $c+d$.

**תנאי "השמאלי לא גדול מהימני":**
- ב-$Z$: $10\le 10$, מתקיים.
- ב-$Y$: $c\le d$.
- ב-$X$: $7\le c+d$.
- בשורש: $7+c+d\le 20$.

**תנאי ריצת הופמן** (בכל שלב מאחדים שני משקלים מינימליים; בשוויון מותר לבחור כל אחד):
- האיחוד הראשון: $X$ אינו יכול להיות ראשון (הוא צריך את $Y$), וגם $Z$ לא: איחוד $a,e$ ראשון דורש ש-$10,10$ יהיו שני הקטנים, אבל $b=7<10$. לכן האיחוד הראשון הוא $c,d$, ושניהם צריכים להיות שני הקטנים מבין $10,7,c,d,10$: $d\le 7$.
- האיחוד השני, מתוך $10,7,c+d,10$: שוב $Z$ אינו אפשרי ($7<10$), ולכן מאחדים את $b$ עם $Y$, ושניהם צריכים להיות שני הקטנים: $c+d\le 10$.
- אחר כך מאחדים $a,e$ ל-$20$, ולבסוף את השורש. (התנאי בשורש, $7+c+d\le 20$, נובע מ-$c+d\le 10$.)

**סיכום:** $1\le c\le d\le 7$ וגם $7\le c+d\le 10$ ($c,d$ מופיעות ב-$S$, ולכן השכיחויות לפחות $1$). כל האפשרויות $(c,d)$:
$$(1,6),(1,7),(2,5),(2,6),(2,7),(3,4),(3,5),(3,6),(3,7),(4,4),(4,5),(4,6),(5,5)$$
כלומר $13$ אפשרויות. (אם מתירים שכיחות $0$ לאות שלא מופיעה, נוספת רק האפשרות $(0,7)$.)"""


CBB = (r"אלגוריתמים (ביחד עם סיבוכיותם) שניתן להיעזר בהן כקופסא שחורה:" "\n"
       r"- $\mathrm{Select}(S,n,k)$ - $O(n)$" "\n"
       r"- $\mathrm{Majority}(S,n)$ - $O(n)$" "\n"
       r"- $\mathrm{Kadane}(S,n)$ - $O(n)$" "\n"
       r"- $\mathrm{KMP}(T,n,P,m)$ - $O(n+m)$" "\n"
       r"- $\mathrm{Kruskal}(G,w)$ - $O(|E|\cdot\log|V|)$" "\n"
       r"- $\mathrm{Prim}(G,w)$ - $O(|V|^2)$ (או $O(|E|\cdot\log|V|)$)" "\n"
       r"- $\mathrm{Huffman}(C,f,n)$ - $O(n\log n)$" "\n"
       r"- $\mathrm{Greedy\text{-}Coloring}(G)$ - $O(|V|+|E|)$")

C3 = (r"אנו מעוניינים לחשב **עלות מינימלית** לצביעה של $n$ בתים הנצבים בשורה. כל בית יכול להיות צבוע באחד משלושת הצבעים: אדום $R$, כחול $B$ או ירוק $G$, "
      r"אך, **בשונה** מצבע הבית הסמוך לו. עלות הצביעה תלויה בבית ובצבע." "\n"
      r"העלות של צביעה כל בית עם צבע מסוים מיוצגת על ידי מטריצת עלויות $\mathrm{cost}$ בגודל $3\times n$. שורות המטריצה מייצגות את הבתים, ועמודות המטריצה מייצגות את הצבעים: "
      r"עמודה $1$ עבור צבע האדום, עמודה $2$ עבור צבע הכחול, ועמודה $3$ עבור הירוק. לדוגמא, $\mathrm{cost}[1][1]$ היא העלות של צביעת בית $1$ בצבע אדום; "
      r"$\mathrm{cost}[2][3]$ היא עלות הצביעה של בית $2$ בצבע ירוק." "\n"
      r"מצא את הצביעה האופטימלית (עלות מינימלית) של כל הבתים.")

questions = [
    H(1, "א", "computation", "kmp_strings",
      r"האם קיימת מחרוזת $P$ באורך $5$ כך שפונקציה $\pi$ עבורה היא $0,1,2,3,1$ ?" "\n"
      r"אם לא - נמקו מדוע, אם כן - תנו דוגמא למחרוזת $P$.", SOL_1A),
    H(1, "ב", "computation", "suffix_structures",
      r"בנו Suffix tree ו-Suffix array עבור המחרוזת `algogoal`", SOL_1B),

    H(2, "א", "algorithm", "dp_optimization",
      r"(25 נקודות) נתון מערך עם מספרים שלמים. נתייחס למערך כאילו הוא מעגלי, ז\"א אחרי איבר האחרון בא איבר הראשון." "\n"
      r"מצאו רצף מספרים במערך מעגלי, אשר נותן סכום מקסימלי." "\n"
      r"לדוגמה: עבור מערך: $4,-6,5,-6,10,-5,3$ עליכם להחזיר: $12=10-5+3+4$" "\n"
      r"רמז: אפשר להיעזר באלגוריתם Kadane שמחזיר רצף עם סכום מקסימלי במערך (לא מעגלי)." "\n"
      r"נמקו נכונות האלגוריתם שכתבתם. מהי הסיבוכיות של האלגוריתם? נמקו את תשובתכם.",
      SOL_2A, points=25, contextId="cbb"),
    H(2, "ב", "algorithm", "divide_conquer",
      r"(15 נקודות) נתון מערך $A$ עם מספרים שלמים ואנדקס $K$." "\n"
      r"יש למיין את המערך המקורי $A$, מלבד האיבר במקום ה-$K$ שאינו משנה את מיקומו." "\n"
      r"לדוגמה: עבור מערך $A$: $4,10,-6,3,15,-8,7$ ו-$K=5$ האלגוריתם מחזיר $-8,-6,3,4,15,7,10$" "\n"
      r"בנו אלגוריתם יעיל ונתחו את הסיבוכיות שלו.",
      SOL_2B, points=15, contextId="cbb"),

    H(3, "א", "algorithm", "dp_optimization",
      r"בעיית תכנון הצביעה ניתנת לפתרון בעזרת **תכנון דינמי**." "\n"
      r"הציגו נוסחה רקורסיבית המחשבת את **העלות** המינימלית." "\n"
      r"יש **להגדיר** את הפונקציה הרקורסיבית **ולנמק** נכונות של הנוסחה." "\n"
      r"רמז: תגדירו $3$ פונקציות רקורסיביות בהתאם לשלוש אופציות לצביעה של הבית האחרון.",
      SOL_3A, contextId="c3"),
    H(3, "ב", "computation", "dp_optimization",
      r"תנו דוגמא לעבודת האלגוריתם שפותר את הבעיה בשיטה תכנון דינאמי על בסיס נוסחה רקורסיבית מסעיף הקודם עבור מטריצה $\mathrm{cost}$ הבאה ($n=3$):" "\n"
      r"בית $1$: אדום $14$, כחול $2$, ירוק $11$" "\n"
      r"בית $2$: אדום $11$, כחול $14$, ירוק $5$" "\n"
      r"בית $3$: אדום $14$, כחול $3$, ירוק $19$" "\n"
      r"(בתשובה יש למלא טבלה עם עמודות הבתים $1,2,3$ ושורות הצבעים $R,B,G$.)",
      SOL_3B, contextId="c3"),
    H(3, "ג", "computation", "complexity_recurrence",
      r"מה סיבוכיות האלגוריתם שפותר את הבעיה בשיטה תכנון דינמי על בסיס נוסחה רקורסיבית מסעיף א? נמקו בקצרה.",
      SOL_3C, contextId="c3"),

    H(4, "", "computation", "huffman",
      r"עבור מחרוזת $S$ מעל א\"ב $\Sigma=\{a,b,c,d,e\}$ נתון כי:" "\n"
      r"- האות $a$ מופיעה $10$ פעמים, האות $b$ מופיעה $7$ פעמים והאות $e$ מופיעה $10$ פעמים." "\n"
      r"- קוד הופמן של האותיות הוא: $a-10,\ b-00,\ c-010,\ d-011,\ e-11$" "\n"
      r"- מספר ההופעות של \"אח\" השמאלי הוא **לא** יותר גדול ממספר הופעות של \"אח\" הימני." "\n"
      r"הניחו שסיבית הקוד לצומת הימני היא $1$ ולשמאלי $0$." "\n"
      r"רשמו את **כל** האופציות האפשריות לשכיחויות של אותיות $c$ ו-$d$ במחרוזת $S$. נמקו את תשובתכם.",
      SOL_4, points=10),
]

exam = {
    "examCode": "23B-C",
    "examLabel": "אלגוריתמים 1 (60172), סמסטר ב' תשפ\"ג, מועד מיוחד (24.08.2023)",
    "year": 2023,
    "examDate": "24.08.2023",
    "sourceFile": "23B-C exam booklet pp.1-31",
    "solutionFile": "none",
    "contexts": {
        "cbb": {"kind": "text", "title": "אלגוריתמים שמותר להשתמש בהם כקופסה שחורה", "text": CBB},
        "c3": {"kind": "text", "title": "שאלה 3: צביעת בתים", "text": C3},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
