# -*- coding: utf-8 -*-
"""Generator for tools/raw/22B-B.json -- algorithms-1 (60172), semester B 2022, moed B (14.07.2022).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_22B-B.py

Source: 18-page file "exam + solutions" (cover, 4 questions with the solution typed in each answer box, a page of
black-box algorithms and the Master theorem, 4 scratch pages). Cap 110, 3 hours. Items: Q1 a,b,c,d (30 in total),
Q2 a,b (25), Q3 a,b (25), Q4 a,b,c (30); no per-part points are printed.
The suffix tree of Q1c is hand-drawn on lined paper in the file: it is NOT cropped (no handwriting ships); it is
transcribed as text and recorded in tools/verify/22B-B/graphs.json.

Held items (official key problems found by checks.py, see docs/ASK_ADIR.md):
- Q2a/Q2b: the official code is wrong whenever k > n-k (it always splits into the k smallest vs the n-k largest, and in the
  else branch the sizes of B and C are swapped). Q2b explains/analyses that code, so it is held with it.
- Q4c: two cells of the printed 5x5 table are wrong ((2,4) and (4,5)); the final answer 3 is right.
Shipped with a visible transcription note: Q1a (the official counterexample has identical tree shape, differing only by
left/right orientation), Q1c (the official tree lacks the leaf of the suffix '$'), Q1d (the official text never states
the answer ABABA).
Other notes: Q1a "k times more" means k added to every count (bbabbc has a=1,b=4,c=1 -> 2,5,2 for k=1).
The cover's "unanswered = 20%" rule is not part of any question.

Checks (tools/verify/22B-B/checks.py): Huffman counts/trees; Q1b brute force (6,2),(5,3); suffix tree rebuilt and
compared; Q1d longest repeated substring; Q2 brute force over all splits; Q3 Prim order and unique MST (all 8-edge
subsets); Q4 recurrence vs brute force + the printed table cell by cell.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "22B-B.json"


def Q(num, part, kind, topic, question, solution, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


# ---------------------------------------------------------------- contexts
C2 = (r"נתון מערך $A$ של $n$ מספרים טבעיים שונים ומספר טבעי $k$ קטן מ-$n$. נסמן $Sum(A)$ - סכום איברים במערך $A$.")

C3 = r"נתון הגרף הבא."

C4 = (r"נתון מערך **ממוין** $A$ של $n$ מספרים שלמים ומספר שלם לא שלילי $k$." "\n"
      r"עליכם למצוא מספר מינימלי של אברים שיש להסיר מן מערך $A$ כך שהפרש בין ערך המקסימאלי שנשאר במערך לבין ערך "
      r"המינימלי שנשאר יהיה לא גדול מ-$k$." "\n"
      r"לדוגמא:" "\n"
      r"Input: $A=\{1,3,4,9,10,12,17,20\}$, $k=4$" "\n"
      r"Output: 5 (remove 1,3,4,17,20)" "\n"
      r"Input: $A=\{1,2,5,6,8\}$, $k=2$" "\n"
      r"Output: 3 (remove 1,2,8 or 5,6,8)" "\n"
      r"הבעיה ניתנת לפתרון בעזרת תכנון דינמי.")

# ---------------------------------------------------------------- solutions
SOL_1A = r"""**פתרון רשמי** (22B-B פתרון עמ' 2):
תשובה לא נכונה. דוגמא: ניקח את אותה מחרוזת עם $k=1$ ונקבל עץ: השורש $9$ עם הבן השמאלי $4$ (שני עלים $2$ ו-$2$) והבן הימני $5$ (עלה).
ועם $k=3$ נקבל עץ אחר: השורש $15$ עם הבן השמאלי $7$ (עלה) והבן הימני $8$ (שני עלים $4$ ו-$4$).
מכיוון שהמסלולים שונים (העץ שלהלן נוטה ימינה בעוד שהקודם נוטה שמאלה), הקידודים שונים.

**הערת תמלול:** בבדיקה במחשב נמצא ששני העצים הרשמיים הם אותו עץ במבנה (אותם אורכי קוד) והם נבדלים רק בכיוון שמאל/ימין. התשובה "לא" נכונה, ודוגמה שבה המבנה עצמו משתנה היא למשל שכיחויות $1,1,1,3$ עם $k=1$ (מתקבלות $2,2,2,4$)."""

SOL_1B = r"""**פתרון רשמי** (22B-B פתרון עמ' 3):
נבנה את העץ: השורש ($x+y+2=10$) עם הבן השמאלי $y+2$ (העלים $b,00$ ו-$c,01$) והבן הימני $a,1$.
מכיוון ש-$c$ נמצא ימינה ל-$b$ אז נובע כי $y\ge2$ ומכיוון ש-$a$ נמצא ימינה לצומת ששכיחותו $y+2$ נובע כי $x\ge y+2$.
אבל מהנתון נובע כי $x+y=8$. לכן $8=x+y\ge2y+2$. אם פותרים את האי שיוויון האחרון מקבלים כי $y\le3$.
לכן אם $y=2$ אז $x=6$ ואילו אם $y=3$ אז $x=5$."""

SOL_1C = r"""**פתרון רשמי** (22B-B פתרון עמ' 4; העץ שרטוט ביד בקובץ ומתומלל כאן כטקסט):
עץ הסיפות של $T=ABABABA$. מהשורש יוצאות שתי צלעות:
- הצלע $BA$ לקודקוד פנימי שיש לו שני בנים: הצלע $\text{\textdollar}$ לעלה $5$, והצלע $BA$ לקודקוד פנימי נוסף שיש לו שני בנים: הצלע $\text{\textdollar}$ לעלה $3$ והצלע $BA\text{\textdollar}$ לעלה $1$.
- הצלע $A$ לקודקוד פנימי שיש לו שני בנים: הצלע $\text{\textdollar}$ לעלה $6$, והצלע $BA$ לקודקוד פנימי שיש לו שני בנים: הצלע $\text{\textdollar}$ לעלה $4$ והצלע $BA$ לקודקוד פנימי שיש לו שני בנים: הצלע $\text{\textdollar}$ לעלה $2$ והצלע $BA\text{\textdollar}$ לעלה $0$.

**הערת תמלול:** בעץ הרשמי חסר העלה של הסיפא הריקה (צלע $\text{\textdollar}$ ישירות מהשורש, עלה $7$); שאר העץ זהה לעץ הסיפות האמיתי (נבדק בחישוב)."""

SOL_1D = r"""**פתרון רשמי** (22B-B פתרון עמ' 5):
דרך אחת לפתרון היא לחפש מסלול החל מצומת פנימי (לא שורש ולא עלה) שהחל ממנה ניתן למצוא סייפא: אם הרישא של אותה סייפא תואמת לתחילת הסייפא, ממשיכים את החיפוש ומתמרנים את החיפוש בעץ בהתאם.
דרך שניה - להלן אלגוריתם:
1. נבנה רשימה מקושרת של כל הרישות של המחרוזת $T$.
2. נבצע חיפוש בעץ הסיפות את הסיפא הארוכה ביותר האפשרית אשר מתאימה לרישא המבוקשת באופן הבא:
2.1. נסרוק את הסיפות מהרישא הארוכה ביותר לפי סדר יורד של אורכים ואז יתכנו שני מקרים:
2.1.1. הרישא מתאימה לסיפא המבוקשת. ולכן עוצרים את החיפוש.
2.1.2. אין התאמה בין הרישא לסיפא המבוקשת ואז מבצעים חיפוש של הרישא הבאה אשר נלקחת מתוך הרשימה המקושרת.

סיבוכיות: בניית רשימה מקושרת - $O(n)$ כאשר $n$ שווה למספר הרישות. חיפוש בעץ - האורך המחרוזת.

**הערת תמלול:** הפתרון הרשמי אינו מציין את התשובה לדוגמה. בבדיקה במחשב: תת-המחרוזת החוזרת הארוכה ביותר ב-$ABABABA$ היא $ABABA$ (מופיעה במקומות $0$ ו-$2$), והיא הקודקוד הפנימי העמוק ביותר בעץ הסיפות."""

CODE_2 = r"""Alg (A, n ,k)
{
  r = 1, t=1;          //indexes
  S = select (A, n, k)
  if (k<n-k) do
    for i=1 to n do
      if (A[i] > S) do
        C[r++] = A[i]
      else B[t++] = A[i]
      end if
    end for
  else for i=1 to n do
      if (A[i]>S) do
        B[t++]=A[i]
      else C[r++] = A[i]
      end if
    end for
  end else
}"""

NOTE_2 = (r"**הערת תמלול:** בבדיקה במחשב נמצא שהאלגוריתם הרשמי מחלק תמיד ל-$k$ הקטנים מול $n-k$ הגדולים, וזה אופטימלי רק כאשר "
          r"$k\le n-k$. כאשר $k>n-k$ התוצאה אינה מקסימלית (למשל $A=[13,5,7]$, $k=2$: ההפרש המקסימלי הוא $15$, האלגוריתם נותן $1$), "
          r"ובענף ה-else גודלי $B$ ו-$C$ מוחלפים. הרעיון (Select) והסיבוכיות הרשמיים נכונים.")

SOL_2A = (r"**פתרון רשמי** (22B-B פתרון עמ' 6):" "\n```\n" + CODE_2 + "\n```\n" + NOTE_2)

SOL_2B = (r"""**פתרון רשמי** (22B-B פתרון עמ' 8):
שורת ה-select מתבצעת ב-$O(n)$ לאחר מכן מתבצעת לולאה שרצה $n$ פעמים אשר מבצעת הכנסה לשני מערכים: אחד בגודל $k$ והשני בגודל $n-k$ כך שבלולאה מתבצעות $k$ הכנסות למערך אחד ועוד $n-k$ הכנסות למערך שני.
לכן סה"כ מקבלים:
$$O(n)+O(k)+O(n-k)=O(n)$$

""" + NOTE_2)

SOL_3A = r"""**פתרון רשמי** (22B-B פתרון עמ' 9):
סדר הצלעות ש-Prim מכניס לעפ"מ החל מקודקוד $A$: $(A,J),(J,G),(G,E),(E,C),(C,D),(E,F),(G,H),(J,B)$
המשקלים: $13+8+5+2+1+4+7+10=50$"""

SOL_3B = r"""**פתרון רשמי** (22B-B פתרון עמ' 10):
היות וכל הצלעות בגרף בעלות משקל שונה, אזי קיים עץ פורש מינימלי יחיד:
הסבר: כדי שהעץ הפורש יישאר עץ פורש, די להוריד את אחת הקשתות מתוך העץ פורש ולהוסיף במקומה קשת אחרת אשר לא סוגרת לולאה בגרף מחד ומאידך הוספה זו תוודא כי קיים כיסוי מלא לכל הקודקודים בגרף, אלא שהצלע $e=(u,v)$ אשר הורדנו מהעץ הינה בעלת משקל מינימלי, ועל מנת שהמשקל הכולל ישאר מינימלי גם לאחר הוספת קשת אחרת $(x,y)$ משקלה צריך להיות זהה כלומר $w(x,y)=w(u,v)$, אלא שלפי נתוני התרגיל ידוע כי $w(x,y)$ בהכרח שונה מזה של $w(u,v)$ סתירה."""

SOL_4A = r"""**פתרון רשמי** (22B-B פתרון עמ' 11):
נגדיר נוסחה רקורסיבית:
$$C(i,j)=\begin{cases}0 & |A[i]-A[j]|\le k\\ \min\bigl(C(i+1,j),\,C(i,j-1)\bigr)+1 & |A[i]-A[j]|>k\end{cases}\qquad 0\le i+j\le n$$
הערך של $C(i,j)$ מחזיר את מספר האיברים המינימלי שיש להסיר מהמערך החל מאינדקס $i$ ועד לאינדקס $j$."""

SOL_4B = r"""**פתרון רשמי** (22B-B פתרון עמ' 12):
הסיבוכיות תהיה $O(n^2)$ משום שקיימת לולאה שרצה $n$ פעמים ובתוכה היא בודקת את מספר האיברים שיש להחסיר על מנת שההפרש בין האיברים שנותרו יהיה מקסימלי."""

SOL_4C = r"""**פתרון רשמי** (22B-B פתרון עמ' 13):
הטבלה ($A=\{1,2,5,6,8\}$, $k=2$; שורות $i$, עמודות $j$; $X$ - לא מוגדר):
$$\begin{array}{c|ccccc} & 1 & 2 & 5 & 6 & 8\\\hline 1 & 0 & 0 & 1 & 2 & 3\\ 2 & X & 0 & 1 & 2 & 2\\ 5 & X & X & 0 & 0 & 1\\ 6 & X & X & X & 0 & 1\\ 8 & X & X & X & X & 0\end{array}$$
התשובה: $3$ (הפינה העליונה).

**הערת תמלול:** שני תאים בטבלה הרשמית אינם מתאימים לנוסחה: התא $(2,6)$ מודפס $2$ ובנוסחה $1$, והתא $(6,8)$ מודפס $1$ ובנוסחה $0$ (כי $|6-8|=2\le k$). התשובה הסופית $3$ נכונה."""

questions = [
    Q(1, "א", "truefalse", "huffman",
      r"אלגוריתם הופמן מקבל מחרוזת ובונה עץ הופמן. האם **לכל** מחרוזת ולכל $k>0$, עץ הופמן יישאר ללא שינוי אם כל אות "
      r"תופיע **ב-$k$ פעמים** יותר?" "\n"
      r"לדוגמא: עבור מחרוזת $bbabbc$ ו-$k=1$, נקבל שכיחויות הבאות: $a-2$, $c-2$, $b-5$. במקרה זה העץ יישאר ללא שינוי." "\n"
      r"אם התשובה היא כן - נמקו מדוע. אם לא - תנו דוגמא נגדית (הראו מחרוזת, $k$ מתאים, ושני עצים שונים).",
      SOL_1A, verdict=False),
    Q(1, "ב", "computation", "huffman",
      r"במחרוזת $S$ מעל א\"ב $\Sigma=\{a,b,c\}$ האות $b$ מופיעה $2$ פעמים, האות $a$ מופיעה $x$ פעמים, האות $c$ מופיעה $y$ פעמים." "\n"
      r"קוד הופמן של האותיות במחרוזת $S$ הינו: $a-1$, $b-00$, $c-01$." "\n"
      r"ידוע ש-$2+x+y=10$." "\n"
      r"חשבו מהו הערך האפשרי של $x$ ו-$y$? ציינו את כל הערכים האפשריים כאשר ידוע שמספר הופעות של \"אח\" השמאלי הוא לא "
      r"יותר גדול ממספר הופעות של \"אח\" הימני. (להזכירכם - $0$ מסמן כיוון ל\"אח\" השמאלי, ו-$1$ - כיוון ל\"אח\" הימני.)",
      SOL_1B),
    Q(1, "ג", "computation", "suffix_structures",
      r"נתונה מחרוזת הבאה: $T=ABABABA$. תבנו Suffix tree עבור המחרוזת.",
      SOL_1C),
    Q(1, "ד", "algorithm", "suffix_structures",
      r"הסבירו איך אפשר בעזרת Suffix tree למצוא במחרוזת $T$ את **תת-המחרוזת** (רצף אותיות) **החוזרת** (שמופיעה לפחות "
      r"פעמיים ב-$T$) **הארוכה ביותר**. כדוגמא לרעיון שלכם תמצאו את תת-המחרוזת החוזרת הארוכה ביותר במחרוזת $T$ מסעיף הקודם.",
      SOL_1D),

    Q(2, "א", "algorithm", "divide_conquer",
      r"יש לתאר אלגוריתם בסיבוכיות $O(n)$ שמחלק את המערך $A$ לשני מערכים $B$ ו-$C$ בגודל $k$ ו-$n-k$ בהתאם כך שההפרש בין "
      r"שני סכומים של האברים במערכים $B$ ו-$C$ יהיה מקסימאלי:" "\n"
      r"$$|Sum(B)-Sum(C)|\to\max$$" "\n"
      r"לדוגמא: עבור המערך $8,4,5,2,10$ ו-$k=2$ החלוקה האופטימלית היא $\{4,2\}$ ו-$\{8,5,10\}$ עם הפרש $17$." "\n"
      r"רמז: אפשר להיעזר באלגוריתם Select.",
      SOL_2A, contextId="c2",
      hold="official code is wrong for k > n-k (not optimal, sizes of B and C swapped); see ASK_ADIR"),
    Q(2, "ב", "computation", "divide_conquer",
      r"הסבירו את **נכונות** האלגוריתם שכתבתם בסעיף הקודם ונתחו את **סיבוכיותו**.",
      SOL_2B, contextId="c2",
      hold="depends on Q2a, whose official code is wrong for k > n-k; see ASK_ADIR"),

    Q(3, "א", "computation", "mst",
      r"כתבו את **המשקלים** של צלעות העץ לפי הסדר ש-**PRIM** הכניס אותם לעפ\"מ החל מקודקוד $A$.",
      SOL_3A, contextId="c3", image="images/exams/22B-B-Q3-graph.png"),
    Q(3, "ב", "proof", "mst",
      r"כמה עפ\"מים (עצים פורשים מינימליים) קיימים בגרף זה? **נמקו** את תשובתכם.",
      SOL_3B, contextId="c3", image="images/exams/22B-B-Q3-graph.png"),

    Q(4, "א", "algorithm", "dp_optimization",
      r"הציגו נוסחה רקורסיבית המחשבת את מספר מינימלי של אברים שיש להסיר. יש **להגדיר** את הפונקציה הרקורסיבית ו**לנמק** "
      r"הנכונות של הנוסחה.",
      SOL_4A, contextId="c4"),
    Q(4, "ב", "computation", "dp_optimization",
      r"מה סיבוכיות האלגוריתם שפותר את הבעיה בשיטה תכנון דינמי על בסיס נוסחה רקורסיבית מסעיף הקודם? נמקו בקצרה.",
      SOL_4B, contextId="c4"),
    Q(4, "ג", "computation", "dp_optimization",
      r"תנו דוגמא לעבודת האלגוריתם שפותר את הבעיה בשיטה תכנון דינמי על בסיס נוסחה רקורסיבית מסעיף א עבור "
      r"$A=\{1,2,5,6,8\}$, $k=2$.",
      SOL_4C, contextId="c4",
      hold="two cells of the official table disagree with the official recurrence ((2,4) and (4,5)); see ASK_ADIR"),
]

exam = {
    "examCode": "22B-B",
    "examLabel": "אלגוריתמים 1 (60172), סמסטר ב' תשפ\"ב, מועד ב (14.07.2022)",
    "year": 2022,
    "examDate": "14.07.2022",
    "sourceFile": "22B-B exam with solutions pp.1-18",
    "solutionFile": "22B-B exam with solutions pp.1-18",
    "contexts": {
        "c2": {"kind": "text", "title": "שאלה 2: חלוקת מערך", "text": C2},
        "c3": {"kind": "text", "title": "שאלה 3: גרף משוקלל", "text": C3},
        "c4": {"kind": "text", "title": "שאלה 4: הסרת מינימום איברים", "text": C4},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
