# -*- coding: utf-8 -*-
"""Generator for tools/raw/22B-A.json -- algorithms-1 (60172), semester B 2022, moed A (16.06.2022).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_22B-A.py

Source: the typed 8-page file "exam + solutions" (text layer + rendered pages; the separate scanned blank exam of the
same sitting was not needed). Each page repeats the question and shows the typed solution in an answer box.
Items: Q1 a,b,c,d (30 in total, no per-part points printed), Q2 (25), Q3 a,b (25 in total), Q4 a,b,c (30 in total).
Cap 110 (cover of the sister sitting 22B-B; this file's cover page has no cap line).

Transcription notes
- Q1c: the official tree is drawn with leaf a on the left; transcribed as a text description + graph data.
- Q2 (solver pass 2026-10-24, typo ruling, solutionSource "solved", pending refuter): besides '>' n/2, testing only
  the median Select(A,(n+1)/2) misses pairs that sit on the upper half for even n (A=[1,2,3,4,5,5]: pair 4,5 has 3
  occurrences, the median 3 is in no such pair). The fix tests both medians (positions ceil(n/2) and floor(n/2)+1) with
  >= ceil(n/2); brute force over all 17.6M arrays n<=8 with values 1..n (tools/verify/22B-A/solve_22B-A.py).
  Original hold reason: the official pseudo-code uses CountL+CountM > n/2 while the question needs >= ceil(n/2);
  for every even n this misses pairs whose total is exactly n/2 (A=[1,2,3,4]: the true answer is True, the code returns
  False). The loops of the official code also have no increments. Idea and explanation of the official solution are right.
- Q4a: the official solution text writes P[1..i-1] and T[1..j-1] (indices swapped); the recurrence itself is right.

Checks (tools/verify/22B-A/checks.py, networkx + brute force):
- Q1: pi tables recomputed (abbbba -> 0,0,0,0,0,1; no string over {a,b} gives 0,0,1,1,2,1). Q1c: brute-force set of (x,y)
  equals the official answer (11 pairs) and every pair gives the printed code lengths for some Huffman tie-breaking.
  Q1d: Print_lines(2^k) prints 2^k-1 lines. Q2: finding above (9804 arrays, all with even n).
- Q3a: triangle 1,2,2 has an MBST that is not an MST (weights 4 vs 3). Q3b: every MST is an MBST on 300 random graphs.
- Q4: recurrence = brute force on 1500 random pairs, example 6, and the printed 6x3 table matches cell by cell.
Graph data for the visualizer: tools/verify/22B-A/graphs.json (Q3a triangle and MBST, Q1c Huffman tree).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "22B-A.json"


def Q(num, part, kind, topic, question, solution, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


# ---------------------------------------------------------------- solutions
SOL_1A = r"""**פתרון רשמי** (22B-A פתרון עמ' 1):
המחרוזת קיימת: $P=abbbba$"""

SOL_1B = r"""**פתרון רשמי** (22B-A פתרון עמ' 1):
המחרוזת לא קיימת: נניח קיימת מחרוזת $P$ עם פונקציית $\pi$: $001121$. אז
$\pi[1]=\pi[2]=0\Longrightarrow P[1]\neq P[2]$
ללא הגבלת כלליות נניח $P[1]=a,\ P[2]=b\Longrightarrow P[3]=a\ (\pi[3]=1)\Longrightarrow P[4]=a\ (\pi[4]=1)$
$\pi[5]=2\Longrightarrow P[5]=P[2]=b$
$\pi[6]=1\Longrightarrow P[6]=P[1]=a$
אך אז יש רישא וסיפא $aba$, לכן $\pi[6]=3$ - סתירה."""

SOL_1C = r"""**פתרון רשמי** (22B-A פתרון עמ' 2):
אם בונים את העץ מקבלים כי $C$ אח ימני של $B$ ולכן $x\ge2$: לכן ניתן להסיק כי השכיחות המצטברת של $bc$ היא $x+2$, לכן $x+2\le5$, ואז יש שתי אופציות ל-$x$: $x=2$ או $x=3$.
$A$ - אח שמאלי ל-$(x+7)$: $y\le x+7$, מצד שני האלגוריתם קודם בחר $d$, לכן $y\ge5$.
העץ: השורש (כל האותיות, שכיחות מצטברת $x+y+7$) - הבן השמאלי $A,y$ והבן הימני $x+7$; מתחת ל-$x+7$ הבן השמאלי $x+2$ (עם העלים $B,2$ ו-$C,x$) והבן הימני $D,5$.
**תשובה:**
$x=2,\ 5\le y\le9$ או $x=3,\ 5\le y\le10$"""

SOL_1D = r"""**פתרון רשמי** (22B-A פתרון עמ' 3):
$$T(n)=2T\left(\frac{n}{2}\right)+O(1)$$
פתרון לפי משפט אב: $T(n)=O(n)$
הסיבוכיות היא פסאודו פולינומית וזאת משום שגודל הקלט הוא $\log n$ ואז $n=2^{\log n}$, ז"א שזמן ריצה הוא פונקציה לא פולינומית ביחס לגודל הקלט."""

CODE_2 = r"""M= Select (A, (n+1)/2)
Count_M=0;
for i=1to n
  if (A[i]==M)
    Count_M++;
If (⌈n/2⌉ ≤ Count_M < n)
  Return True
i=1; flag=0;
while (A[i]>=M) i++;
if(i<=n)
  { L=A[i]; flag=1}
if (flag)
{
 while (i<=n)
   if(A[i]>L and A[i]<M)  L=A[i];
CountL=0;
for (int i =0; i<n; i++)
  if (A[i]==L) CountL++
 if (CountL+CountM>n/2)
   Return True
}
i=1; flag=0;
while (A[i]<=M) i++;
if(i<=n)
  { R=A[i]; flag=1}
if (flag)
{
 while (i<=n)
   if(A[i]<R and A[i]>M)  R=A[i];
CountR=0;
for (int i =0; i<n; i++)
  if (A[i]==R) CountR++
 if (CountR+CountM>n/2)
   Return True
}
Return False"""

SOL_2 = (r"""**פתרון רשמי** (22B-A פתרון עמ' 4):
אם קיים זוג ערכים עוקבים שסכום ה**מופעים** של שניהם ביחד במערך הוא לפחות $\lceil n/2\rceil$ אז איבר אחד מהזוג חייב להיות חציון. האיבר השני - הוא או איבר הכי גדול שקטן מהחציון, או איבר הכי קטן שגדול מחציון. מוצאים איברים האלה כמועמדים ובודקים כמות המופעים האם מקיימים את התנאי הדרוש:
""" + "```\n" + CODE_2 + "\n```\n" + r"""אם חציון $M$ מופיע לפחות $\lceil n/2\rceil$ פעמים, אך יש עוד איברים במערך ($Count\_M<n$), אז יש זוג ערכים עוקבים שתופסים יותר מחצי מקומות במערך.
נחפש איבר מקסימלי שקטן מ-$M$ (הזוג "השמאלי"): $flag=1$ - מצאנו איבר שהוא קטן מ-$M$.
נחפש איבר מינימלי שגדול מ-$M$ (הזוג "הימני"): $flag=1$ - מצאנו איבר שהוא גדול מ-$M$.

**הערת תמלול:** בבדיקה במחשב נמצא שהקוד הרשמי מחזיר תשובה שגויה לכל מערך שבו $n$ זוגי והסכום הוא בדיוק $n/2$ (למשל $A=[1,2,3,4]$: התשובה הנכונה היא True והקוד מחזיר False), כי התנאי בקוד הוא $>n/2$ ולא $\ge\lceil n/2\rceil$. הרעיון וההסבר הרשמיים נכונים."""
         )

CODE_2_FIX = r"""Pair(A, n)
   M1 = Select(A, ceil(n/2))
   M2 = Select(A, floor(n/2)+1)       // = M1 when n is odd
   return Check(A, n, M1) or Check(A, n, M2)

Check(A, n, M)
   Count_M = 0
   for i = 1 to n
      if (A[i] == M) Count_M++
   if (ceil(n/2) <= Count_M < n) return True
   // L = the largest value smaller than M (the "left" neighbour)
   flag = 0
   for i = 1 to n
      if (A[i] < M and (flag == 0 or A[i] > L))  { L = A[i]; flag = 1 }
   if (flag)
      Count_L = 0
      for i = 1 to n
         if (A[i] == L) Count_L++
      if (Count_L + Count_M >= ceil(n/2)) return True
   // R = the smallest value larger than M (the "right" neighbour)
   flag = 0
   for i = 1 to n
      if (A[i] > M and (flag == 0 or A[i] < R))  { R = A[i]; flag = 1 }
   if (flag)
      Count_R = 0
      for i = 1 to n
         if (A[i] == R) Count_R++
      if (Count_R + Count_M >= ceil(n/2)) return True
   return False"""

SOL_2_FIX = (r"""הפתרון הרשמי עם תיקון: הודפס התנאי $CountL+CountM>n/2$ ונבדק רק החציון $Select(A,(n+1)/2)$; הנכון הוא התנאי $\ge\lceil n/2\rceil$, ועבור $n$ זוגי לבדוק גם את האיבר במקום $n/2+1$ (עבור $A=[1,2,3,4]$ הקוד המודפס מחזיר False, ועבור $A=[1,2,3,4,5,5]$ הזוג $4,5$ מופיע $3$ פעמים אבל החציון $3$ אינו חלק ממנו).
**רעיון (כמו בפתרון הרשמי).** אם זוג ערכים עוקבים $x<y$ מופיע יחד לפחות $\lceil n/2\rceil$ פעמים, אז במערך הממוין המופעים שלהם תופסים רצף של לפחות $\lceil n/2\rceil$ מקומות. רצף כזה מכיל את המקום $\lceil n/2\rceil$ או את המקום $\lfloor n/2\rfloor+1$ (אם הוא מתחיל אחרי המקום $\lceil n/2\rceil$, הוא מתחיל בדיוק במקום $n/2+1$ עבור $n$ זוגי). לכן אחד מערכי הזוג הוא $M_1$ או $M_2$, והערך השני הוא השכן שלו: הערך הגדול ביותר שקטן ממנו או הערך הקטן ביותר שגדול ממנו. בודקים את כל המועמדים:
""" + "```\n" + CODE_2_FIX + "\n```\n" + r"""אם $M$ מופיע לפחות $\lceil n/2\rceil$ פעמים, אך יש עוד איברים במערך ($Count\_M<n$), אז $M$ ואחד משכניו הם זוג ערכים עוקבים שמופיע לפחות $\lceil n/2\rceil$ פעמים.
**סיבוכיות.** שתי קריאות ל-Select ב-$O(n)$, ובכל קריאה ל-Check מספר קבוע של מעברים על המערך, $O(n)$. סה"כ $O(n)$.""")

SOL_3A = r"""**פתרון רשמי** (22B-A פתרון עמ' 5):
הגרף: משולש על 3 קודקודים עם המשקלים $1,2,2$ (הצלע בעלת המשקל 1 מחברת את הקודקוד העליון לימני; שתי הצלעות האחרות במשקל 2).
**MST:** הצלע בעלת המשקל 1 והצלע התחתונה בעלת המשקל 2. משקל של צלע צוואר בקבוק הוא $2$.
**MBST:** שתי הצלעות בעלות המשקל 2 (השמאלית והתחתונה). משקל של צלע צוואר בקבוק הוא $2$.
העץ השני הוא MBST (צוואר הבקבוק שלו הוא 2, הקטן ביותר האפשרי) אך אינו עפ"מ (משקלו 4 לעומת 3)."""

SOL_3B = r"""**פתרון רשמי** (22B-A פתרון עמ' 6):
נוכיח שכל עפ"מ ($MST$) הוא גם עץ צוואר בקבוק מינימאלי ($MBST$). נניח בשלילה שקיים עפ"מ $T_{min}$ שהוא לא עץ צוואר בקבוק מינימאלי, ז"א שיש ב-$T_{min}$ צלע (צוואר בקבוק) שמשקלה גדול ממשקל של כל צלע בגרף $T$ שהוא עץ צוואר בקבוק מינימאלי ($MBST$), ז"א קיימת צלע $e_0=(u,v)\in E_{min}$ עם משקל מקסימאלי בעפ"מ $T_{min}$ שלכל צלע מ-$T$ המשקל יותר נמוך.
$T_{min}-e_0=A\cup B$ (כי $e_0$ - גשר בעץ), ב-$T$ יש מסלול יחיד $P_{uv}$ שמחבר בין $u$ ל-$v$. המסלול מתחיל ב-$A$ ומסתיים ב-$B$, לכן יש לפחות צלע אחת $e_1\in E$ שמחברת $A$ ל-$B$ ושייכת למסלול זה. $e_1\in T$, לכן $w(e_1)<w(e_0)$.
צלע $e_1$ מחברת בין $A$ ל-$B$, לכן $e_1\notin T_{min}-e_0$, וגם $T'=T_{min}-e_0\cup e_1$ ע"פ, אך $w(T')<w(T_{min})$.
סתירה, כי $T_{min}$ עפ"מ."""

SOL_4A = r"""**פתרון רשמי** (22B-A פתרון עמ' 7):
נגדיר $C(i,j)$ - מספר הפעמים ש-$P[1..j]$ מופיעה ב-$T[1..i]$ כתת-סדרה.
$$C(i,j)=\begin{cases}0 & j>i\\ 1 & j=0\\ C(i-1,j) & T[i]\ne P[j]\\ C(i-1,j-1)+C(i-1,j) & T[i]=P[j]\end{cases}$$
אם $T[i]\ne P[j]$, אז אפשר לזרוק אות אחרונה ב-$T$ כי היא לא יכולה להשתתף בהתאמה עם $P$.
אם $T[i]=P[j]$, אז כל הפתרונות אפשר לחלק לשתי קבוצות: קבוצת הפתרונות עם התאמה $T[i]=P[j]$, ואז נשאר להתאים $P[1..i-1]$ ל-$T[1..j-1]$ וקבוצת הפתרונות ללא התאמה זו $C(i-1,j)$."""

SOL_4B = r"""**פתרון רשמי** (22B-A פתרון עמ' 8):
מילוי טבלה בגודל $|T|\times|P|$, לכן הסיבוכיות $O(|T|\cdot|P|)$"""

SOL_4C = r"""**פתרון רשמי** (22B-A פתרון עמ' 8):
טבלה ($T=abcbac$ בשורות, $P=abc$ בעמודות):
$$\begin{array}{c|ccc} & a & b & c\\\hline a & 1 & 0 & 0\\ b & 1 & 1 & 0\\ c & 1 & 1 & 1\\ b & 1 & 2 & 1\\ a & 2 & 2 & 1\\ c & 2 & 2 & 3\end{array}$$
התשובה: $3$ (התא האחרון)."""

INTRO_1 = (r"האם קיימת מחרוזת $P$ מעל א\"ב $\{a,b\}$ כך שפונקציה $\pi$ (prefix function) עבורה היא:" "\n")
TAIL_1 = "\n" r"אם לא - נמקו מדוע לא קיימת. אם כן - תנו דוגמא למחרוזת $P$ מתאימה."

questions = [
    Q(1, "א", "computation", "kmp_strings", INTRO_1 + r"$0,0,0,0,0,1$" + TAIL_1, SOL_1A),
    Q(1, "ב", "proof", "kmp_strings", INTRO_1 + r"$0,0,1,1,2,1$" + TAIL_1, SOL_1B),
    Q(1, "ג", "computation", "huffman",
      r"במחרוזת $S$ מעל א\"ב $\Sigma=\{a,b,c,d\}$ האות $b$ מופיעה $2$ פעמים, האות $d$ מופיעה $5$ פעמים, האות $c$ מופיעה "
      r"$x$ פעמים, האות $a$ מופיעה $y$ פעמים." "\n"
      r"קוד הופמן של האותיות במחרוזת $S$ הינו: $a-0$, $b-100$, $c-101$, $d-11$." "\n"
      r"חשבו מהו הערך האפשרי של $x$ ו-$y$? ציינו את כל הערכים האפשריים כאשר ידוע שמספר הופעות של \"אח\" השמאלי הוא לא "
      r"יותר גדול ממספר הופעות של \"אח\" הימני. (להזכירכם - $0$ מסמן כיוון ל\"אח\" השמאלי, ו-$1$ - כיוון ל\"אח\" הימני.)",
      SOL_1C),
    Q(1, "ד", "computation", "complexity_recurrence",
      r"נתונה פונקציה רקורסיבית המקבלת מספר טבעי $n$ ומדפיסה שורות:" "\n"
      "```\nPrint_lines(n)\nif (n>1)\n{\n  print_line(\"still running \\n\");\n  Print_lines(n/2);\n  Print_lines(n/2);\n}\n```\n"
      r"בהנחה שפעולה `print_line(\"still running \n\")` לוקחת זמן $O(1)$ מה תהיה סיבוכיות של פונקציית זמן הריצה כפונקציה של $n$?" "\n"
      r"האם פונקצית זמן הריצה כפונקציה של **גודל הקלט** היא פונקציה פולינומית? **נמקו** את תשובתכם.",
      SOL_1D),

    Q(2, "", "algorithm", "divide_conquer",
      r"זוג ערכים במערך נקרא זוג **ערכים עוקבים** אם הם ערכים שונים זה מזה, אבל לאחר מיון הם יהיו סמוכים זה לזה במערך." "\n"
      r"נתון מערך בגודל $n$. יש **לתאר אלגוריתם** בסיבוכיות $O(n)$ הבודק האם במערך קיים זוג ערכים עוקבים שסכום ה**מופעים** "
      r"של שניהם ביחד במערך הוא לפחות $\lceil n/2\rceil$. תנו הסבר קצר ל**נכונות** האלגוריתם." "\n"
      r"לדוגמא: במערך $5,2,8,3,2,5,8$ הערכים $3$ ו-$5$ הם עוקבים, וגם $5,8$ - הם ערכים עוקבים, אך רק זוג $5$ ו-$8$ מקיים את "
      r"התנאי שסכום המופעים ($5,8$ מופיעים $4$ פעמים) של הזוג הוא לפחות $\lceil n/2\rceil=4$." "\n"
      r"רמז: אפשר להיעזר באלגוריתם Select.",
      SOL_2_FIX, points=25, solutionSource="solved", official=False, confidence="high"),

    Q(3, "א", "computation", "mst",
      r"יהי $G=(V,E,w)$ גרף לא מכוון, קשיר ומשוקלל ויהי $T=(V,E_T)$ - עץ פורש." "\n"
      r"צלע בעלת משקל מקסימאלי ב-$E_T$ נקראת **צלע צוואר בקבוק**." "\n"
      r"עבור גרף $G$ **עץ צוואר בקבוק מינימאלי** ($MBST$ - a minimum bottleneck spanning tree) הינו עץ פורש של $G$ שבו משקלה "
      r"של צלע צוואר בקבוק הוא מינימאלי (מבין כל העצים הפורשים של $G$)." "\n"
      r"תנו דוגמא לגרף $G=(V,E,w)$ על $3$ קדקודים שבו יש עץ צוואר בקבוק מינימאלי ($MBST$) שהוא **לא עפ\"מ** ($MST$). "
      r"ציירו את הגרף עם פונקציית משקל על צלעות, $MBST$ ו-$MST$.",
      SOL_3A),
    Q(3, "ב", "proof", "mst",
      r"הוכיחו שכל עפ\"מ ($MST$) הוא גם עץ צוואר בקבוק מינימאלי ($MBST$).",
      SOL_3B),

    Q(4, "א", "algorithm", "dp_sequences",
      r"בהינתן טקסט $T$ ומחרוזת $P$, עליכם למצוא את **מספר פעמים** שמחרוזת $P$ מופיעה בטקסט $T$ **כתת-סדרה**." "\n"
      r"לדוגמא:" "\n"
      r"Input: $T=$\"subsequence\", $P=$\"see\"" "\n"
      r"Output: 6" "\n"
      r"(שש התאמות: האות s הראשונה או הרביעית, ושתיים משלוש האותיות e)." "\n"
      r"הבעיה ניתנת לפתרון בעזרת תכנון דינמי." "\n"
      r"הציגו נוסחה רקורסיבית המחשבת את מספר הפעמים ש-$P$ מופיעה ב-$T$ כתת-סדרה. יש **להגדיר** את הפונקציה הרקורסיבית "
      r"ו**לנמק** הנכונות של הנוסחה.",
      SOL_4A),
    Q(4, "ב", "computation", "dp_sequences",
      r"מה סיבוכיות האלגוריתם שפותר את הבעיה בשיטה תכנון דינמי על בסיס נוסחה רקורסיבית מסעיף הקודם? נמקו בקצרה.",
      SOL_4B),
    Q(4, "ג", "computation", "dp_sequences",
      r"תנו דוגמא לעבודת האלגוריתם שפותר את הבעיה בשיטה תכנון דינמי על בסיס נוסחה רקורסיבית מסעיף א עבור "
      r"$T=abcbac$, $P=abc$.",
      SOL_4C),
]

# ---------------------------------------------------------------- rubric / pitfalls / steps (ai-draft)
# Every expected value is recomputed by tools/verify/22B-A/steps_22B-A.py (prefix function, Huffman tie-break brute force,
# spanning-tree enumeration, subsequence DP). Per-part points are not printed in the exam: the split below
# (Q1 6/8/8/6, Q3 10/15, Q4 12/6/12) is a draft that sums to the printed question totals (30/25/30).
def rub(*items):
    return [{"text": t, "points": p} for t, p in items]


def ch(prompt, correct, wrong, pos, explain, **kw):
    vals = list(wrong)
    vals.insert(pos, correct)
    s = {"type": "choice", "prompt": prompt,
         "options": [{"id": "abcdefgh"[i], "value": v} for i, v in enumerate(vals)],
         "correctId": "abcdefgh"[pos], "explain": explain}
    s.update(kw)
    return s


def num(prompt, answer, explain, **kw):
    s = {"type": "numeric", "prompt": prompt, "answer": answer, "tol": 0, "explain": explain}
    s.update(kw)
    return s


def txt(prompt, accept, explain, normalize="complexity", **kw):
    s = {"type": "text", "prompt": prompt, "accept": accept, "normalize": normalize, "explain": explain}
    s.update(kw)
    return s


def add(num_, part, **kw):
    for q in questions:
        if q["num"] == num_ and q.get("part") == part:
            if "hold" in q:
                raise ValueError("held item %s%s" % (num_, part))
            q.update(kw)
            return
    raise KeyError((num_, part))


def clean(src):
    out = []
    for ln in src.strip("\n").split("\n"):
        ln = ln.split("//")[0].rstrip()
        if ln.strip():
            out.append(ln)
    return out


def swap1(lines, old, new):
    idx = [i for i, ln in enumerate(lines) if ln.strip() == old.strip()]
    assert len(idx) == 1, old
    out = list(lines)
    out[idx[0]] = out[idx[0]].replace(old.strip(), new.strip())
    return out, idx[0]


# ---- Q1a
add(1, "א",
    rubric=rub(("קביעה שהמחרוזת קיימת", 1),
               ("מתן דוגמה: $P=abbbba$ (או $baaaab$)", 2),
               ("בדיקת $\\pi$ ערך אחר ערך: רק האות האחרונה שווה לראשונה, ולכן $\\pi[6]=1$ והשאר $0$", 3)),
    rubricSource="ai-draft",
    pitfalls=["לתת מחרוזת שבה אות באמצע שווה לאות הראשונה (למשל `aabbba`): אז $\\pi$ באמצע כבר אינו $0$.",
              "לחשב את $\\pi$ כמספר ההופעות של האות הראשונה ולא כאורך הרישא-סיפא הארוכה ביותר."],
    steps=[
        ch("מה נובע מ-$\\pi[6]=1$ על המחרוזת $P$ באורך 6?",
           "$P[6]=P[1]$", ["$P[6]=P[2]$", "$P[5]=P[1]$", "$P[6]\\ne P[1]$"], 0,
           "$\\pi[6]=1$ אומר שרישא באורך 1 היא גם סיפא של $P$, כלומר האות האחרונה שווה לאות הראשונה. שאר השוויונות אינם נובעים מכך."),
        ch("איזו מהמחרוזות הבאות מקיימת $\\pi=0,0,0,0,0,1$?",
           "`abbbba`", ["`abbbbb`", "`aabbba`", "`abbbab`"], 1,
           "ב-`abbbbb` הערך האחרון $0$, ב-`aabbba` כבר $\\pi[2]=1$, וב-`abbbab` הערך החמישי הוא $1$ והאחרון $0$ (חישוב $\\pi$ לכל אחת)."),
        num("כמה מחרוזות באורך 6 מעל $\\{a,b\\}$ מקיימות $\\pi=0,0,0,0,0,1$?", 2,
            "`abbbba` והמחרוזת שמתקבלת ממנה בהחלפת האותיות, `baaaab` (בדיקת כל 64 המחרוזות: 2)."),
    ],
    stepsSource="ai-draft")

# ---- Q1b
PROOF1B = [r"נניח שקיימת מחרוזת $P$ כזו. מ-$\pi[1]=\pi[2]=0$ נובע $P[1]\ne P[2]$, ובלי הגבלת כלליות $P[1]=a,\ P[2]=b$.",
           r"מ-$\pi[3]=\pi[4]=1$ נובע $P[3]=P[4]=a$, מ-$\pi[5]=2$ נובע $P[5]=P[2]=b$, ומ-$\pi[6]=1$ נובע $P[6]=P[1]=a$. כלומר $P=abaaba$.",
           r"אבל אז $aba$ היא גם רישא וגם סיפא של $P$, ולכן $\pi[6]=3$, בסתירה ל-$\pi[6]=1$."]
PROOF1B_BUG = list(PROOF1B)
PROOF1B_BUG[1] = r"מ-$\pi[3]=\pi[4]=1$ נובע $P[3]=P[4]=a$, מ-$\pi[5]=2$ נובע $P[5]=P[2]=b$, ומ-$\pi[6]=1$ נובע $P[6]=P[1]=b$. כלומר $P=abaabb$."
add(1, "ב",
    rubric=rub(("קביעה שהמחרוזת לא קיימת", 1),
               ("הנחה שקיימת וגזירת $P[1]\\ne P[2]$ ובלי הגבלת כלליות $P[1]=a,\\ P[2]=b$", 2),
               ("גזירת שאר האותיות מערכי $\\pi$: $P=abaaba$", 3),
               ("סתירה: $\\pi[6]=3$ ולא $1$", 2)),
    rubricSource="ai-draft",
    pitfalls=["לבדוק כמה מחרוזות ולהסיק שאין: צריך הוכחה לכל המחרוזות.",
              "לשכוח את \"בלי הגבלת כלליות\" ולטפל בשני המקרים $P[1]=a$ ו-$P[1]=b$ בנפרד.",
              "לגזור את האות השישית מ-$\\pi[6]=1$ ולהתעלם מכך שהרישא $aba$ גם היא סיפא."],
    steps=[
        ch("איזו שיטת הוכחה משמשת בפתרון הרשמי?",
           "הנחה שהמחרוזת קיימת, גזירת אותיותיה מערכי $\\pi$ עד לסתירה",
           ["בניית מחרוזת מפורשת שמקיימת את הדרישה", "אינדוקציה על אורך המחרוזת", "הוכחה שהסכום של $\\pi$ גדול מדי"], 0,
           "הפתרון הרשמי מניח קיום, מסיק את כל אותיות $P$ ומראה ש-$\\pi[6]$ חייב להיות $3$."),
        {"type": "order", "prompt": "סדרו את שלבי ההוכחה.", "lines": PROOF1B,
         "explain": "קודם ההנחה והאותיות הראשונות, אחר כך שאר האותיות, ובסוף הסתירה."},
        {"type": "findbug", "prompt": "בגרסה הבאה של ההוכחה שורה אחת שונתה. מצאו אותה.", "lines": PROOF1B_BUG, "bugIndex": 1,
         "explain": "$\\pi[6]=1$ אומר $P[6]=P[1]=a$ ולא $b$. עם $P[6]=b$ ההוכחה כבר אינה מתקיימת."},
        num("מהו $\\pi[6]$ של המחרוזת $abaaba$ שנגזרה בהוכחה?", 3,
            "הרישא `aba` היא גם הסיפא, ולכן $\\pi[6]=3$ (חישוב $\\pi$: 3)."),
    ],
    stepsSource="ai-draft")

# ---- Q1c
add(1, "ג",
    rubric=rub(("בניית העץ מהקוד ומיקום האחים: $c$ ימני ל-$b$, ו-$a$ שמאלי לצומת $x+7$", 2),
               ("מ-$c$ ימני ל-$b$: $x\\ge2$, ומהצומת $x+2\\le5$: $x\\in\\{2,3\\}$", 2),
               ("$y\\le x+7$ (אח שמאלי) ו-$y\\ge5$ (האלגוריתם בחר קודם את $d$)", 2),
               ("התשובה: $x=2$, $5\\le y\\le9$ או $x=3$, $5\\le y\\le10$", 2)),
    rubricSource="ai-draft",
    pitfalls=["לשכוח את אחד האי-שוויונות (למשל $y\\ge5$) ולהרחיב את טווח $y$.",
              "לפרש \"אח שמאלי לא כבד מהימני\" בכיוון ההפוך.",
              "לשכוח שהסדר שבו Huffman ממזג קובע גם $x+2\\le5$."],
    steps=[
        num("מהו הערך המינימלי של $x$?", 2,
            "$c$ הוא האח הימני של $b$ (שכיחות 2), ולכן $x\\ge2$ (בדיקה בכוח גס על כל טיבי הופמן: 2)."),
        num("מהו הערך המקסימלי של $x$?", 3,
            "השכיחות המצטברת של $b,c$ היא $x+2$ והיא אח שמאלי של $d$ (שכיחות 5): $x+2\\le5$ (בכוח גס: 3)."),
        num("עבור $x=3$: מהו הערך המקסימלי של $y$?", 10,
            "$y\\le x+7=10$ (בכוח גס: 10)."),
        num("כמה זוגות $(x,y)$ אפשריים בסך הכול?", 11,
            "עבור $x=2$: $5\\le y\\le9$ (5 ערכים), ועבור $x=3$: $5\\le y\\le10$ (6 ערכים). סך הכול 11 (בכוח גס: 11)."),
    ],
    stepsSource="ai-draft")

# ---- Q1d
add(1, "ד",
    rubric=rub(("נוסחת הנסיגה $T(n)=2T(n/2)+O(1)$", 2),
               ("משפט האב: $n^{\\log_2 2}=n$ גדול פולינומית מ-$f(n)=O(1)$ ולכן $T(n)=O(n)$", 2),
               ("גודל הקלט הוא $\\log n$ ולכן $n=2^{\\log n}$ אינו פולינומי בגודל הקלט", 2)),
    rubricSource="ai-draft",
    pitfalls=["להסיק שהזמן פולינומי כי $O(n)$ הוא פולינום ב-$n$: הקלט הוא המספר $n$ בייצוג בינארי.",
              "לכתוב $T(n)=T(n/2)+O(1)$ כי יש קריאה אחת: יש שתי קריאות."],
    steps=[
        ch("איזו נוסחת נסיגה מתארת את זמן הריצה של `Print_lines`?",
           "$T(n)=2T(n/2)+O(1)$", ["$T(n)=T(n/2)+O(1)$", "$T(n)=2T(n/2)+O(n)$", "$T(n)=T(n-1)+O(1)$"], 0,
           "יש שתי קריאות על $n/2$ והדפסה אחת (קבוע)."),
        num("כמה שורות מודפסות עבור $n=16$?", 15,
            "מספר השורות הוא $2^k-1$ עבור $n=2^k$ (הרצה של הפונקציה: 15)."),
        txt("מהי הסיבוכיות כפונקציה של $n$? (למשל `O(n)`)", ["O(n)", "Θ(n)"],
            "לפי משפט האב $T(n)=\\Theta(n)$."),
        ch("האם זמן הריצה פולינומי בגודל הקלט?",
           "לא: גודל הקלט הוא $\\log n$ ו-$n=2^{\\log n}$ אקספוננציאלי בו",
           ["כן, כי $O(n)$ הוא פולינום", "כן, כי הקלט הוא $n$", "לא, כי יש רקורסיה"], 1,
           "גודל הקלט הוא מספר הסיביות של $n$. זמן $n=2^{\\text{bits}}$ אינו פולינומי."),
    ],
    stepsSource="ai-draft")

# ---- Q2 (solved)
C2_LINES = clean(CODE_2_FIX)
C2_BUG, C2_BI = swap1(C2_LINES, "if (Count_L + Count_M >= ceil(n/2)) return True", "if (Count_L + Count_M > n/2) return True")
add(2, None,
    rubric=rub(("מועמדים: שני החציונים בעזרת Select (המקומות $\\lceil n/2\\rceil$ ו-$\\lfloor n/2\\rfloor+1$)", 6),
               ("ספירת המופעים של המועמד ובדיקה שמופיע לפחות $\\lceil n/2\\rceil$ פעמים", 4),
               ("מציאת השכן השמאלי (הגדול ביותר שקטן ממנו) והימני (הקטן ביותר שגדול ממנו)", 6),
               ("בדיקת סכום המופעים של המועמד והשכן מול $\\lceil n/2\\rceil$", 5),
               ("הסבר נכונות: זוג כזה תופס רצף של לפחות $\\lceil n/2\\rceil$ מקומות במערך הממוין, ולכן מכיל אחד החציונים", 2),
               ("זמן $O(n)$", 2)),
    rubricSource="ai-draft",
    pitfalls=["לבדוק רק את החציון התחתון: במערך זוגי כמו $[1,2,3,4,5,5]$ הזוג $4,5$ מופיע 3 פעמים אך החציון $3$ אינו בו.",
              "להשתמש בתנאי $>n/2$ במקום $\\ge\\lceil n/2\\rceil$: עבור $[1,2,3,4]$ מוחזר False בטעות.",
              "למיין את המערך ($O(n\\log n)$) במקום להשתמש ב-Select."],
    steps=[
        num("בדוגמה $5,2,8,3,2,5,8$: כמה פעמים מופיעים יחד הערכים העוקבים $5$ ו-$8$?", 4,
            "$5$ מופיע פעמיים ו-$8$ פעמיים: סך הכול 4, וזה $\\lceil 7/2\\rceil=4$ (ספירה: 4)."),
        ch("איזה ערכים נבדקים כמועמדים לזוג?",
           "שני החציונים (המקום $\\lceil n/2\\rceil$ והמקום $\\lfloor n/2\\rfloor+1$ במערך הממוין) ושכניהם",
           ["רק החציון התחתון ושכניו", "המינימום והמקסימום ושכניהם", "החציון בלבד, בלי שכנים"], 0,
           "רצף של לפחות $\\lceil n/2\\rceil$ מקומות מכיל אחד משני המקומות האמצעיים. כל אחת מהחלופות נכשלת על קלט כלשהו (בדיקה מול כוח גס)."),
        {"type": "findbug", "prompt": "בגרסה הבאה של הקוד שורה אחת שונתה והאלגוריתם נכשל על קלטים מסוימים. מצאו אותה.", "code": True,
         "lines": C2_BUG, "bugIndex": C2_BI,
         "explain": "התנאי הנכון הוא סכום מופעים לפחות $\\lceil n/2\\rceil$. עם `> n/2` מתקבל False עבור $[1,1,3,4,5,6]$ למרות שהזוג $1,3$ מופיע 3 פעמים."},
        txt("מהי הסיבוכיות? (למשל `O(n)`)", ["O(n)", "Θ(n)"],
            "מספר קבוע של קריאות ל-Select ושל מעברים על המערך."),
    ],
    stepsSource="ai-draft")

# ---- Q3a
G3A = {"nodes": ["T", "L", "R"], "directed": False, "algo": "kruskal",
       "edges": [{"u": "T", "v": "L", "w": 2}, {"u": "T", "v": "R", "w": 1}, {"u": "L", "v": "R", "w": 2}]}
add(3, "א",
    rubric=rub(("גרף על 3 קודקודים עם משקלים $1,2,2$", 2),
               ("העפ\"מ: הצלע במשקל 1 וצלע אחת במשקל 2 (משקל 3)", 2),
               ("עץ צוואר בקבוק מינימלי: שתי הצלעות במשקל 2 (צוואר בקבוק 2, משקל 4)", 3),
               ("הסבר שהעץ הזה MBST כי אין עץ עם צוואר בקבוק קטן מ-2, אך אינו עפ\"מ כי משקלו 4 לעומת 3", 3)),
    rubricSource="ai-draft",
    pitfalls=["לתת גרף שבו כל המשקלים שונים: אז כל עפ\"מ הוא היחיד ושווה ל-MBST.",
              "לבלבל בין משקל צוואר הבקבוק (הצלע המקסימלית) לבין המשקל הכולל של העץ."],
    steps=[
        num("מהו המשקל של העפ\"מ בגרף?", 3,
            "הצלע במשקל 1 ועוד צלע במשקל 2.", graph=G3A, key="weight"),
        num("מהו משקל צוואר הבקבוק (הצלע המקסימלית) של העפ\"מ?", 2,
            "העפ\"מ מכיל צלע במשקל 2, וכל עץ פורש בגרף מכיל לפחות צלע אחת במשקל 2."),
        num("מהו המשקל הכולל של העץ שמורכב משתי הצלעות במשקל 2?", 4,
            "$2+2=4$, גדול מ-3, ולכן אינו עפ\"מ."),
        ch("איזה עץ פורש הוא MBST שאינו עפ\"מ?",
           "העץ שמורכב משתי הצלעות במשקל 2",
           ["העץ שמורכב מהצלע במשקל 1 ומהצלע $T$-$L$", "העץ שמורכב מהצלע במשקל 1 ומהצלע $L$-$R$", "כל שלושת העצים הפורשים"], 0,
           "שני העצים האחרים הם עפ\"מים (משקל 3). לכל שלושת העצים צוואר בקבוק 2, אבל רק אחד מהם אינו מינימלי במשקל."),
    ],
    stepsSource="ai-draft")

# ---- Q3b
PROOF3B = [r'נניח בשלילה שקיים עפ"מ $T_{min}$ שאינו MBST: הצלע $e_0=(u,v)$ המקסימלית בו כבדה מכל צלע בעץ צוואר בקבוק $T$.',
           r"הסרת $e_0$ מפצלת את $T_{min}$ לשני רכיבים $A$ ו-$B$.",
           r"במסלול היחיד ב-$T$ בין $u$ ל-$v$ יש צלע $e_1$ שמחברת בין $A$ ל-$B$, ולכן $w(e_1)<w(e_0)$.",
           r"העץ $T'=T_{min}-e_0+e_1$ הוא עץ פורש ו-$w(T')<w(T_{min})$.",
           r'זו סתירה לכך ש-$T_{min}$ הוא עפ"מ.']
PROOF3B_BUG = list(PROOF3B)
PROOF3B_BUG[3] = r"העץ $T'=T_{min}-e_0+e_1$ הוא עץ פורש ו-$w(T')>w(T_{min})$."
G3B = {"nodes": ["1", "2", "3", "4"], "directed": False, "algo": "kruskal",
       "edges": [{"u": "1", "v": "2", "w": 1}, {"u": "2", "v": "3", "w": 2}, {"u": "3", "v": "4", "w": 3},
                 {"u": "4", "v": "1", "w": 4}]}
add(3, "ב",
    rubric=rub(("הנחת השלילה: עפ\"מ שאינו MBST, והצלע $e_0$ שלו כבדה מכל צלעות $T$", 3),
               ("פיצול $T_{min}-e_0$ לשני רכיבים", 3),
               ("מציאת הצלע $e_1$ במסלול ב-$T$ החוצה בין הרכיבים וקלה מ-$e_0$", 3),
               ("בניית $T'$ שהוא עץ פורש קל יותר", 4),
               ("סתירה", 2)),
    rubricSource="ai-draft",
    pitfalls=["להחליף את $e_0$ בצלע שאינה חוצה בין שני הרכיבים: התוצאה אינה עץ פורש.",
              "לשכוח שהצלע $e_1$ קלה מ-$e_0$ כי $e_0$ כבדה מכל צלעות $T$.",
              "להוכיח את הכיוון ההפוך (MBST הוא עפ\"מ), שאינו נכון."],
    steps=[
        ch("איזו שיטת הוכחה משמשת?",
           "הוכחה בשלילה בעזרת החלפת צלע: מחליפים את הצלע הכבדה של העפ\"מ בצלע קלה יותר",
           ["אינדוקציה על מספר הקודקודים", "דוגמה נגדית", "השוואה לאלגוריתם Prim"], 0,
           "מניחים עפ\"מ שאינו MBST ומראים שאפשר להפחית את משקלו."),
        num("במעגל על 4 קודקודים עם משקלים $1,2,3,4$: מהו משקל צוואר הבקבוק של העפ\"מ?", 3,
            "העפ\"מ מסיר את הצלע 4 ונשארות $1,2,3$, ולכן צוואר הבקבוק 3, וזה גם המינימום מבין כל העצים הפורשים (בדיקה מלאה: 3).",
            graph=G3B),
        {"type": "order", "prompt": "סדרו את שלבי ההוכחה.", "lines": PROOF3B,
         "explain": "הנחה, פיצול, מציאת צלע חוצה, בניית עץ קל יותר, סתירה."},
        {"type": "findbug", "prompt": "בגרסה הבאה שורה אחת שונתה. מצאו אותה.", "lines": PROOF3B_BUG, "bugIndex": 3,
         "explain": "$e_1$ קלה מ-$e_0$, ולכן $T'$ קל יותר מ-$T_{min}$ ולא כבד ממנו. רק כך מתקבלת סתירה."},
    ],
    stepsSource="ai-draft")

# ---- Q4a
REC4A = [r"$C(i,0)=1$ (המחרוזת הריקה מופיעה פעם אחת), ו-$C(i,j)=0$ כאשר $j>i$",
         r"אם $T[i]\ne P[j]$: $C(i,j)=C(i-1,j)$ (התו $T[i]$ אינו משתתף בהתאמה)",
         r"אם $T[i]=P[j]$: $C(i,j)=C(i-1,j-1)+C(i-1,j)$ (התאמות שמשתמשות ב-$T[i]$ והתאמות שלא)",
         r"התשובה היא $C(|T|,|P|)$"]
REC4A_BUG = list(REC4A)
REC4A_BUG[1] = r"אם $T[i]\ne P[j]$: $C(i,j)=C(i-1,j-1)$ (התו $T[i]$ אינו משתתף בהתאמה)"
add(4, "א",
    rubric=rub(("הגדרת $C(i,j)$: מספר ההופעות של $P[1..j]$ כתת-סדרה ב-$T[1..i]$", 3),
               ("מקרי בסיס: $C(i,0)=1$ ו-$C(i,j)=0$ עבור $j>i$", 3),
               ("מקרה $T[i]\\ne P[j]$: $C(i-1,j)$", 2),
               ("מקרה $T[i]=P[j]$: סכום ההתאמות עם התו ובלעדיו", 4)),
    rubricSource="ai-draft",
    pitfalls=["במקרה השוויון לכתוב רק $C(i-1,j-1)$ ולאבד את ההתאמות שאינן משתמשות ב-$T[i]$.",
              "לשכוח את בסיס $C(i,0)=1$, ולכן כל הטבלה מתאפסת.",
              "לבלבל בין תת-סדרה לבין תת-מחרוזת רציפה."],
    steps=[
        num("מה מספר ההופעות של `see` כתת-סדרה ב-`subsequence`?", 6,
            "שש התאמות: ה-s הראשון או הרביעי, ושתיים משלוש האותיות e (ספירה בכוח גס: 6)."),
        ch("מה הנוסחה כאשר $T[i]=P[j]$?",
           "$C(i,j)=C(i-1,j-1)+C(i-1,j)$",
           ["$C(i,j)=C(i-1,j-1)$", "$C(i,j)=C(i-1,j-1)\\cdot C(i-1,j)$", "$C(i,j)=C(i-1,j-1)+C(i,j-1)$"], 2,
           "התאמות שמשתמשות ב-$T[i]$ הן $C(i-1,j-1)$, ושאינן משתמשות בו $C(i-1,j)$. החלופות נכשלות, למשל על $T=aa$, $P=a$ (התשובה 2)."),
        {"type": "findbug", "prompt": "בגרסה הבאה שורה אחת שונתה. מצאו אותה.", "lines": REC4A_BUG, "bugIndex": 1,
         "explain": "כשהתו אינו תואם פשוט מוותרים עליו: $C(i-1,j)$. עם $C(i-1,j-1)$ מתקבלות ספירות שגויות (למשל $T=ba$, $P=a$)."},
    ],
    stepsSource="ai-draft")

# ---- Q4b
add(4, "ב",
    rubric=rub(("טבלה בגודל $|T|\\times|P|$", 3),
               ("עבודה קבועה לכל תא", 1),
               ("סך הכול $O(|T|\\cdot|P|)$", 2)),
    rubricSource="ai-draft",
    pitfalls=["לכתוב $O(n)$ או $O(|T|)$ ולשכוח את הממד השני של הטבלה.",
              "לחשב בכוח גס כל התאמה אפשרית: זמן אקספוננציאלי."],
    steps=[
        num("בטבלה של הפתרון הרשמי עבור $T=abcbac$ ו-$P=abc$ (שורה לכל תו של $T$ ועמודה לכל תו של $P$): כמה תאים?", 18,
            "$6\\cdot3=18$."),
        txt("מהי סיבוכיות הזמן? (בסימונים `T` ו-`P` לאורכי המחרוזות, למשל `O(|T||P|)`)",
            ["O(|T||P|)", "O(|T|·|P|)", "O(|T|*|P|)", "O(nm)", "O(mn)"],
            "$O(|T|\\cdot|P|)$ תאים בעבודה קבועה כל אחד."),
    ],
    stepsSource="ai-draft")

# ---- Q4c
add(4, "ג",
    rubric=rub(("מילוי הטבלה שורה אחר שורה לפי הנוסחה", 4),
               ("ערכי תאים נכונים בעמודה האמצעית", 3),
               ("ערכים נכונים בעמודה האחרונה", 3),
               ("התשובה $3$ (התא האחרון)", 2)),
    rubricSource="ai-draft",
    pitfalls=["להתחיל את הטבלה בלי שורה/עמודה של בסיסים ולטעות בתאים הראשונים.",
              "לחבר בתא את הערך מהשורה הנוכחית במקום מהשורה הקודמת."],
    steps=[
        num("מהו $C(4,2)$: כמה פעמים `ab` מופיעה כתת-סדרה ב-`abcb` (ארבעת התווים הראשונים של $T$)?", 2,
            "ה-`a` מתאים ל-`b` בשני המקומות: 2 (ספירה בכוח גס: 2)."),
        num("מהו $C(5,3)$: כמה פעמים `abc` מופיעה כתת-סדרה ב-`abcba`?", 1,
            "רק `a`,`b`,`c` בשלושת התווים הראשונים (ספירה בכוח גס: 1)."),
        num("מהו $C(6,3)$, התשובה לבעיה: כמה פעמים `abc` מופיעה כתת-סדרה ב-`abcbac`?", 3,
            "ההתאמות במקומות $(1,2,3)$, $(1,2,6)$ ו-$(1,4,6)$ (ספירה בכוח גס: 3)."),
    ],
    stepsSource="ai-draft")

exam = {
    "examCode": "22B-A",
    "examLabel": "אלגוריתמים 1 (60172), סמסטר ב' תשפ\"ב, מועד א (16.06.2022)",
    "year": 2022,
    "examDate": "16.06.2022",
    "sourceFile": "22B-A exam with solutions pp.1-8",
    "solutionFile": "22B-A exam with solutions pp.1-8",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
