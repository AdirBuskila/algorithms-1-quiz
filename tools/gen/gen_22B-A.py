# -*- coding: utf-8 -*-
"""Generator for tools/raw/22B-A.json -- algorithms-1 (60172), semester B 2022, moed A (16.06.2022).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_22B-A.py

Source: the typed 8-page file "exam + solutions" (text layer + rendered pages; the separate scanned blank exam of the
same sitting was not needed). Each page repeats the question and shows the typed solution in an answer box.
Items: Q1 a,b,c,d (30 in total, no per-part points printed), Q2 (25), Q3 a,b (25 in total), Q4 a,b,c (30 in total).
Cap 110 (cover of the sister sitting 22B-B; this file's cover page has no cap line).

Transcription notes
- Q1c: the official tree is drawn with leaf a on the left; transcribed as a text description + graph data.
- Q2 is HELD (reason below): the official pseudo-code uses CountL+CountM > n/2 while the question needs >= ceil(n/2);
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
      SOL_2, points=25,
      hold="official pseudo-code disagrees with brute force for every even n (uses > n/2 instead of >= ceil(n/2)); see ASK_ADIR"),

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
