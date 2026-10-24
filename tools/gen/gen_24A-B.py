# -*- coding: utf-8 -*-
"""Generator for tools/raw/24A-B.json -- algorithms-1 (60172), semester A 2024, moed B (11.4.24).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24A-B.py

Source: a graded STUDENT scan (35 pages; handwritten answers inside the exam booklet, grader marks, score table on p.1).
Only TEXT is transcribed. No crop of any page is taken (the scan shows a student id and handwriting): there are no
figures in this sitting, no image files, and the solutions below are retyped, tidied transcriptions of the handwriting.
The solution source is the anonymized student paper (solutionSource "student-solution", official false).
Cover: 2 h, 4 questions x 25 + a 5-point bonus, cap 105. Items: Q1 a,b (10/15), Q2 a,b,c (10/10/5), Q3 a,b,c (5/10/10),
Q4 a,b,c (15/5/5), bonus (num 5, 5 points). The per-part points are the printed score-table maxima.

Transcription notes
- Handwriting is partly illegible (crossed-out first attempts in Q2 and Q4 are ignored). Where a line could not be read
  with certainty the answer is rebuilt from the legible parts and the graded result; confidence is "med" or "low" there.
- Q1: the exam refers to "טיול" "as defined in the assignment" (not printed); the graded solution treats it as a walk
  (vertices and edges may repeat) that passes through at least one vertex of A. Graded full marks.
- Q2a: the student's first tape needs count++ too (there is no current tape at the start); one clarifying sentence says so.
- Q2b: the student's inequality signs between g1 and A1 are ambiguous in the scan, so the two cases are written in words.
- Q3c: the printed hypothesis reads "ההסתברות להחזרת שווים היא לפחות 1/4" as printed. The student's handwriting is partly
  unreadable: the idea (several independent random primes q, answer "different" if any run says so) is kept.
- Q4a: the student's recurrence lost 3 of 15 points for missing edge cases (the grader's note); the model solution gives
  the recurrence with the full base cases T(0,0)=1, T(0,j>0)=0, T(i,0)=0 (checked by brute force).
- Q4b: the student's O(m*n) time was accepted, the O(m*n) space got half credit; the retyped solution gives O(n*m) time
  and O(m) space (two rows), with O(n*m) when the whole table is kept (solutionSource "solved").
- Q4c: the student's answer (time O(m*n), space O(m*n)) was graded full; kept as transcribed.
- Q5 (bonus): the printed statement says the shortest-first greedy does NOT necessarily give an optimal solution (the word
  "לא" is underlined); the student circled "נכון" with no justification. The example interval set is added for illustration.

Checks (tools/verify/24A-B/checks.py, networkx + brute force; Python only):
- Q1a/b: the student's BFS algorithms equal a product-graph BFS reference on 3000 random graphs (x,y not in A).
- Q2a: the student's greedy equals the DP optimum on 5000 random inputs; the example 2,1,4,2 with m=5 needs 3 tapes.
- Q3b: 2*ceil(log2 n^2) bits; Q3c: k independent runs multiply the error probability.
- Q4: the recurrence equals brute force for n<=6, m<=40; the two-row table equals the full table.
- Bonus: shortest-first is not optimal on [0,10],[9,12],[11,20].
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24A-B.json"


def Q(num, part, kind, topic, question, solution, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution,
         "solutionSource": "student-solution", "official": False, "confidence": "med"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


# ---------------------------------------------------------------- contexts
C1 = r"יהי $G=(V,E)$ גרף לא מכוון."

C2 = (r"נתונה הבעיה הבאה במפעל יצור \"מצליח\", להלן תיאור המצב על פס היצור:" "\n"
      r"**קלט:** $n$ ארגזים באורכים שונים: $l_1,l_2,\ldots,l_n$ היוצאים מפס היצור בסדר זה (ז\"א, יוצא הארגז באורך $l_1$ אחריו באורך $l_2$ וכך הלאה). "
      r"ומלאי לא מוגבל של סרטי הדבקה באורך $m$ שנועדו לסגירת הארגזים." "\n"
      r"**פלט:** מציאת **מספר מינימלי** של סרטי הדבקה לסגירת הארגזים כאשר יש לסגור את הארגזים בסדר היוצא מפס הייצור וניתן לגזור את סרט ההדבקה "
      r"אם יש צורך בכך (ואף להשתמש בחלק הנותר) אך ברגע שנבחר סרט הדבקה חדש, השאריות (אם נשארות) של סרט ההדבקה שכבר השתמשנו נזרקות לפח." "\n"
      r"**דוגמה:** בהינתן הארגזים באורכים הבאים: $2,1,4,2$ ואורך כל סרט הדבקה הינו $5$ ניתן להסתפק ב-$3$ סרטי הדבקה, למשל, אחד לסגירת הארגזים באורך $2,1$ "
      r"וזריקת שני מטרים הנותרים מסרט הדבקה זה (אין יכולת לנצל שארית זאת). נשתמש בסרט ההדבקה השני לסגירת הארגז באורך $4$ ובסרט השלישי לסגירת הארגז האחרון, "
      r"אבל בשני סרטי הדבקה בלבד לא נצליח לסגור את כל הארגזים." "\n"
      r"הבעיה ניתנת לפתרון בעזרת אלגוריתם חמדני.")

C3 = (r"לאליס מחרוזת $x$ של $n$ ביטים. לבוב מחרוזת $y$ של $n$ ביטים. אליס ובוב יודעים ששתי המחרוזות $x,y$ שונות לכל היותר בביט אחד." "\n"
      r"אליס ובוב רוצים להבין אם לשניהם אותה מחרוזת." "\n"
      r"אליס מציעה לבוב את האלגוריתם הבא (Karp & Rabin 87):" "\n"
      r"- אליס: מגרילה מספר ראשוני $2\le q\le n^2$, מחשבת $z=x \bmod q$ ושולחת לבוב את $z,q$" "\n"
      r"- אם $z\ne y \bmod q$ בוב מחזיר \"שונים\" אחרת מחזיר \"שווים\".")

C4 = (r"קוביית משחק היא אביזר בצורת קובייה המשמש לצורכי משחק. בקוביית המשחק הטיפוסית, מסומנת כל אחת מ-$6$ הפאות שלה במספר מ-$1$ עד $6$, "
      r"המיוצג על ידי ספרה או על ידי נקודות בכמות המתאימה." "\n"
      r"להלן הגדרת בעיית הקוביות בצבעים שונים:" "\n"
      r"**קלט:** $n$ קוביות משחק בצבעים שונים ומספר $m$" "\n"
      r"**פלט:** כמות האפשרויות השונות לתוצאות בהן בהטלת $n$ הקוביות סכום המספרים על הפאה העליונה בכל הקוביות הינו $m$" "\n"
      r"**דוגמא:** $n=2,\ m=3$ יש $2$ אפשרויות: $(1,2)$ או $(2,1)$, שימו לב שאלו שתי תוצאות שונות כי הקוביות בצבעים שונים" "\n"
      r"בעיית הקוביות בצבעים שונים ניתנת לפתרון בתכנון דינמי.")

# ---------------------------------------------------------------- solutions
SOL_1A = ("**פתרון סטודנט** (תמלול מכתב יד):\n"
          "```\n"
          "bool isTiyul(G, A, x, y)\n"
          "{\n"
          "    dx[] = BFS(G, x)\n"
          "    if dx[y] == INF\n"
          "        return false\n"
          "    foreach v in A:\n"
          "        if dx[v] != INF\n"
          "            return true\n"
          "    return false\n"
          "}\n"
          "```\n"
          "מספיק לבדוק האם קיים קודקוד אחד מהקבוצה $A$ שנמצא באותו רכיב קשירות עם $x,y$. תחילה נבדוק האם קיים מסלול $x\\to y$, אם כן נבדוק האם קיים קודקוד מהקבוצה $A$ שנגיש מ-$x$, ואם קיים - נחזיר אמת. אחרת נחזיר שקר.")

SOL_1B = ("**פתרון סטודנט** (תמלול מכתב יד):\n"
          "```\n"
          "int minTravel(G, x, y, A)\n"
          "{\n"
          "    dx[] = BFS(G, x)\n"
          "    if dx[y] == INF\n"
          "        return INF\n"
          "    dy[] = BFS(G, y)\n"
          "    int min = INF\n"
          "    foreach v in A:\n"
          "        if dx[v] + dy[v] < min\n"
          "            min = dx[v] + dy[v]\n"
          "    return min\n"
          "}\n"
          "```\n"
          "נתחיל בבדיקה האם ניתן להגיע מ-$x$ ל-$y$; במידה וכן, נבדוק עבור כל קודקוד $v$ בקבוצה $A$: אורך הטיול הקצר ביותר דרך $v$ הוא $d_x[v]+d_y[v]$ (מ-$x$ אל $v$ ומ-$v$ אל $y$). נעדכן את $min$ במידה ונמצא ערך קטן יותר, ובסוף נחזיר אותו.")

SOL_2A = (r"**פתרון סטודנט** (תמלול מכתב יד):" "\n"
          r"נגדיר משתנה $count=0$ שיסמן את מספר סרטי ההדבקה בהם השתמשנו." "\n"
          r"עבור כל ארגז שיוצא ממפס הייצור, לפי הסדר: במידה והסרט הנוכחי מספיק כדי לסגור את הארגז, נשתמש בו; אחרת (אם השארית שלו אינה מספיקה, למשל) נשתמש בסרט חדש (באורך $m$), נבצע $count{+}{+}$ ונסגור בו את הארגז." "\n"
          r"(בתחילה אין סרט נוכחי, ולכן הארגז הראשון מתחיל סרט חדש.)" "\n"
          r"נחזור על הפעולות עד שנסגור את כל הארגזים." "\n"
          r"בסוף נחזיר את $count$.")

SOL_2B = r"""**פתרון סטודנט** (תמלול מכתב יד):
**הוכחת הבחירה החמדנית:**
יהי $A$ פתרון אופטימלי ויהי $G$ פתרון חמדני. נסמן ב-$g_1$ את קבוצת הארגזים שסגרנו בעזרת הסרט הראשון ב-$G$, ו-$A_1$ כנ"ל ב-$A$.
אם $g_1=A_1$ - הפתרון זהה בבחירה הראשונה והפתרון צודק.
אם $g_1$ קטנה מ-$A_1$: לא ייתכן, שכן סגרנו בעזרת הסרט הראשון את המספר המקסימלי של ארגזים.
אם $A_1$ קטנה מ-$g_1$: אז שהבחירה החמדנית קיימת, ואת אותה קבוצת ארגזים יכולנו לסגור בעזרת הסרט הראשון גם ב-$A$, ולכן נחליף את $A_1$ ב-$g_1$ והפתרון נשאר אופטימלי.
לכן תכונת הבחירה החמדנית מתקיימת.
**הוכחת תת מבנה:**
לאחר שסימנו לסגור את מספר הארגזים המקסימלי שיכולנו בעזרת הסרט הראשון, אנחנו פותרים בדיוק את אותה תת בעיה, שכן שוב נתחיל עם סרט חדש, ולכן נשתמש שוב בבחירה החמדנית באותו אופן. לכן תת מבנה אופטימלי מתקיים.
סה"כ: תכונת הבחירה החמדנית מתקיימת וגם תת מבנה אופטימלי מתקיים, ולכן הפתרון החמדני שהצגנו אכן פותר את הבעיה."""

SOL_2C = (r"**פתרון סטודנט** (תמלול מכתב יד):" "\n"
          r"יש לנו $n$ ארגזים, עבור כל ארגז אנחנו מבצעים מספר קבוע של פעולות, לכן סה\"כ סיבוכיות זמן ריצה $O(n)$.")

SOL_3A = (r"**פתרון סטודנט** (תמלול מכתב יד):" "\n"
          r"אכן קיים הבדל, שכן כשבוב מחזיר \"שונים\" התשובה נכונה בוודאות, וכשבוב מחזיר \"שווים\" התשובה לא בהכרח נכונה.")

SOL_3B = (r"**פתרון סטודנט** (תמלול מכתב יד):" "\n"
          r"עבור $q$ - $\lceil\log(n^2)\rceil$ - מקסימלי." "\n"
          r"עבור $z$ - גם $\lceil\log(n^2)\rceil$ - כי הוא מודולו של $q$." "\n"
          r"סה\"כ: $2\cdot\lceil\log(n^2)\rceil$")

SOL_3C = (r"**פתרון סטודנט** (תמלול מכתב יד, חלקו קשה לקריאה):" "\n"
          r"נשתמש באותו אלגוריתם, רק שבמקום להעביר פעם אחת את $q$ נגריל כמה כאלה (בלתי תלויים, כמות שנקבעה מראש) ונעביר אותם לבוב, יחד עם הערכים $z$ המתאימים. "
          r"אם באחת הפעמים בוב החזיר \"שונים\" - נחזיר \"שונים\", ואחרת \"שווים\"." "\n"
          r"אם ההסתברות לטעות באלגוריתם יחיד היא $p_0$, אחרי $k$ הרצות בלתי תלויות היא $p_0^{\,k}$." "\n"
          r"* אפשר להגריל פעמיים.")

SOL_4A = r"""**פתרון סטודנט** (תמלול מכתב יד, עם השלמת מקרי הקצה):
$T(i,j)$ - מספר התוצאות השונות של הטלת $i$ קוביות (בצבעים שונים) שסכום הפאות העליונות הוא $j$.
$$T(i,j)=\begin{cases}1 & ;\ i=0\ \wedge\ j=0\\ 0 & ;\ j=0\ \wedge\ i\ge 1\\ 0 & ;\ i=0\ \wedge\ j>0\\ \displaystyle\sum_{\substack{1\le k\le 6\\ j-k\ge 0}} T(i-1,\,j-k) & ;\ \text{else}\end{cases}$$
נסכם את כל האפשרויות לצאת עם סכום $j$ באמצעות $i$ קוביות, כך שבכל פעם נוציא תוצאה אחרת $k\in\{1,\ldots,6\}$ בקובייה האחרונה: במידה והתוצאה בקובייה האחרונה היא $k$, נשארו $i-1$ קוביות שצריכות להשיג סכום $j-k$. במידה ו-$j-k<0$ אין אפשרות כזו ולכן היא אינה נספרת.
(הבודק הוריד 3 נקודות על חוסר התייחסות לחלק ממקרי הקצה; כאן הם הושלמו.)"""

SOL_4B = (r"**פתרון** (הפתרון הסטודנטי קיבל חצי נקודות; כאן מתוקן):" "\n"
          r"**סיבוכיות זמן:** $O(n\cdot m)$ - בטבלה $n\times m$ תאים, ולכל תא ממלאים סכום של לכל היותר $6$ ערכים." "\n"
          r"**סיבוכיות מקום:** $O(m)$ - כל שורה $i$ תלויה רק בשורה $i-1$, ולכן מספיקות שתי שורות (אם שומרים את כל הטבלה: $O(n\cdot m)$).")

SOL_4C = (r"**פתרון סטודנט** (תמלול מכתב יד):" "\n"
          r"**סיבוכיות זמן:** $O(m\cdot n)$, עוברים על כל הטבלה." "\n"
          r"**סיבוכיות מקום:** $O(m\cdot n)$ - נדרש מערך דו-ממדי לאחסון הפתרונות החלקיים.")

SOL_5 = (r"**פתרון סטודנט:** נכון (הסימון בלבד, ללא נימוק)." "\n"
         r"דוגמה להמחשה (לא נדרשה): המקטעים $[0,10],[9,12],[11,20]$ - הבחירה בקצר ביותר, $[9,12]$, חוסמת את שני האחרים ומניבה מקטע אחד, "
         r"בעוד שהפתרון האופטימלי בוחר שניים: $[0,10]$ ו-$[11,20]$.")

questions = [
    Q(1, "א", "algorithm", "graphs_search",
      r"כתבו אלגוריתם (או פסודוקוד) המקבל כקלט את הגרף $G$ (המיוצג על ידי רשימת סמיכויות) ושני קודקודים $x,y\in V$ בגרף $G$ וקבוצה $A$ כך ש: $x,y\notin A,\ \emptyset\ne A\subseteq V$ "
      r"ומחזיר אמת אם קיים **טיול** מ-$x$ ל-$y$ שעובר דרך הקבוצה $A$. (הגדרה של טיול כפי שהוגדרה במטלה)",
      SOL_1A, points=10, contextId="c1"),
    Q(1, "ב", "algorithm", "graphs_search",
      r"כתבו אלגוריתם (או פסודוקוד) המקבל כקלט את הגרף $G$ (המיוצג על ידי רשימת סמיכויות) ושני קודקודים $x,y\in V$ בגרף $G$ וקבוצה $A$ כך ש: $x,y\notin A,\ \emptyset\ne A\subseteq V$ "
      r"ומחזיר את אורך הטיול הקצר ביותר מ-$x$ ל-$y$ שעובר דרך הקבוצה $A$, אם לא קיים טיול יחזיר אינסוף.",
      SOL_1B, points=15, contextId="c1"),

    Q(2, "א", "algorithm", "greedy", "כתבו אלגוריתם (או פסודו-קוד) לפתרון הבעיה.", SOL_2A, points=10, contextId="c2"),
    Q(2, "ב", "proof", "greedy", "הוכיחו את נכונות האלגוריתם שהצגתם.", SOL_2B, points=10, contextId="c2"),
    Q(2, "ג", "computation", "complexity_recurrence", "מה סיבוכיות זמן הריצה של האלגוריתם שהצגתם? נמקו תשובתכם.", SOL_2C, points=5, contextId="c2"),

    Q(3, "א", "truefalse", "randomized",
      "האם קיים הבדל מבחינת נכונות התשובה בין המצב שבוב מחזיר \"שונים\" לבין המצב שבוב מחזיר \"שווים\"? נמקו תשובתכם.",
      SOL_3A, points=5, contextId="c3", verdict=True),
    Q(3, "ב", "computation", "randomized",
      "כמה ביטים נדרשת אליס להעביר לבוב באלגוריתם שהצענו? נמקו תשובתכם.", SOL_3B, points=10, contextId="c3"),
    Q(3, "ג", "algorithm", "randomized",
      r"אם ידוע שההסתברות להחזרת \"שווים\" היא לפחות $\frac14$, הציעו אלגוריתם המתבסס על האלגוריתם הנתון המקטין את ההסתברות ל-$0<p\le\frac14$.",
      SOL_3C, points=10, contextId="c3", confidence="low"),

    Q(4, "א", "algorithm", "dp_optimization",
      r"כתבו נוסחה רקורסיבית $T(i,j)$ המקבלת שני פרמטרים $1\le i\le n$ ו-$1\le j\le m$ ומחזירה את כמות האפשרויות השונות לתוצאות בהן בהטלת $i$ קוביות סכום המספרים על הפאה העליונה בקוביות הינו $j$.",
      SOL_4A, points=15, contextId="c4"),
    Q(4, "ב", "computation", "complexity_recurrence",
      r"מה סיבוכיות הזמן וסיבוכיות המקום לאלגוריתם תכנות דינמי למציאת כמות האפשרויות השונות לתוצאות בהן בהטלת $n$ הקוביות סכום המספרים על הפאות העליונות בקוביות הינו $m$. נמקו תשובתכם (אין צורך לפרט את האלגוריתם עצמו).",
      SOL_4B, points=5, contextId="c4", solutionSource="solved"),
    Q(4, "ג", "computation", "complexity_recurrence",
      r"מה סיבוכיות הזמן וסיבוכיות המקום לאלגוריתם תכנות דינמי המחזיר את הצירופים השונים של $n$ הקוביות שסכום הפאות שלהן הוא $m$. נמקו תשובתכם (אין צורך לפרט את האלגוריתם עצמו).",
      SOL_4C, points=5, contextId="c4", confidence="low"),

    Q(5, "", "truefalse", "greedy",
      "**שאלת בונוס (5 נקודות)** - ענה נכון או לא נכון, אין צורך לנמק." "\n"
      "בבעיית תזמון מקטעים, הגישה החמדנית הבוחרת במקטע שמשך הזמן שלו קצר ביותר **לא** תניב בהכרח פתרון אופטימלי.",
      SOL_5, points=5, verdict=True),
]

exam = {
    "examCode": "24A-B",
    "examLabel": "אלגוריתמים 1 (60172), סמסטר א' תשפ\"ד, מועד ב (11.4.24)",
    "year": 2024,
    "examDate": "11.4.2024",
    "sourceFile": "student-solution-1 (scan, text only)",
    "solutionFile": "student-solution-1",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1: טיול בגרף", "text": C1},
        "c2": {"kind": "text", "title": "שאלה 2: סרטי הדבקה במפעל", "text": C2},
        "c3": {"kind": "text", "title": "שאלה 3: אליס ובוב (Karp-Rabin)", "text": C3},
        "c4": {"kind": "text", "title": "שאלה 4: קוביות בצבעים שונים", "text": C4},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
