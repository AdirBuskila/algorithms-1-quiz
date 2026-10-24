# -*- coding: utf-8 -*-
"""Generator for tools/raw/24A-A.json -- algorithms-1 (60072), semester A 2024, moed A (18.3.24).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24A-A.py

Source: exam booklet pp.1-17 (cover, 4 questions + bonus in answer boxes, draft pages) and a 4-page partial solution file.
Cover: 2 h, 4 questions x 25 + a 5-point bonus, cap 105.
Items: Q1 a,b (10/15), Q2 a,b,c (10/10/5), Q3 a,b,c (12/8/5), Q4 a,b,c (15/5/5), bonus (num 5, 5 points).

Question-to-solution mapping (checked page by page): the solution file repeats the printed text of Q2 and Q3 verbatim, so
Q2 and Q3 map directly. Q1 is "see the Moodle model solution" (a homework-style question) -> no key. Q4 is a variant:
the solution file's Q4 adds an example table, says the array is sorted by width in DESCENDING order and asks, as its part b, to
demonstrate the recurrence on that example and, as part c, for the time and space of the algorithm that returns the boxes;
the printed exam has no table, does not state the direction, and asks (b) time/space of the height-only DP, (c) time/space
of the algorithm that returns the boxes. The bonus says "see the homework solutions" -> no key.

Former holds (no-key, now solved below): Q1a, Q1b (Moodle), Q4c (the file gives only the time, O(n^2) overall; space is
not stated), bonus.
Q4b: the file says finding the tallest height needs O(n^2) (a one-dimensional array, each cell compares with up to n values);
the O(n) space follows from "one-dimensional array", so it is kept with confidence med.
Solver pass (2026-10-24, solutionSource "solved", official false, pending refuter): Q1a (BFS from z reaches x and y),
Q1b (BFS from x and from y, d(x,z)+d(z,y)=d(x,y)), Q4c (time O(n^2), space O(n) with a predecessor array) and the bonus
(false) are solved; checks in tools/verify/24A-A/solve_24A-A.py (product-graph BFS, networkx all_shortest_paths, brute
force over towers).
Q2a: the printed text reads "תבו" (missing letter); the solution file repeats it as "כתבו", which is used.
Q2b: the official proof is transcribed as printed (it writes p2>q2 where the lengths of both segments are 1).
Q4a: the official recurrence assumes the boxes are sorted by width in descending order (stated only in the solution file).
Note (not part of the exam): the worked example in the solution file's variant of Q4b computes T(3)=15 although its table
has H(3)=1; by the table the tallest tower is 10 (checked in checks.py). Not used here.

Checks (tools/verify/24A-A/checks.py, brute force; Python only):
- Q2a: the official greedy covers every point and uses the minimum number of unit segments on 3000 random inputs.
- Q3a: if the strings differ in one bit the answer "equal" has probability (n-1)/n; Q3b: ceil(log2 n) == bit_length(n-1),
  plus 1 bit for the value; Q3c: n/2 distinct random positions contain the one differing bit with probability exactly 1/2.
- Q4a: the official recurrence equals a brute force over all stable towers on 3000 random box sets (widths descending).
- Bonus (info for the solver, no key in the file): shortest-interval-first is not optimal, e.g. [0,10],[9,12],[11,20].
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24A-A.json"


def Q(num, part, kind, topic, question, solution, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


def H(num, part, kind, topic, question, reason, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "hold": reason}
    if part:
        q["part"] = part
    q.update(kw)
    return q


# ---------------------------------------------------------------- contexts
C1 = r"יהי $G=(V,E)$ גרף לא מכוון."

C2 = (r"הגדרה: נאמר כי מקטע $[a,b]$ על ציר המספרים הממשיים מכסה נקודה $x$ על הציר אם $x\in[a,b]$." "\n"
      r"נתונה הבעיה הבאה:" "\n"
      r"**קלט:** מערך עם $n$ מספרים ממשיים המבטאים נקודות על ציר המספרים." "\n"
      r"**פלט:** סדרת מקטעים באורך $1$ המכסים את כל נקודות הקלט המינימלית (ז\"א, בסדרה יש מינימום כמות המקטעים באורך $1$ המכסים את כל נקודות הקלט)." "\n"
      r"הבעיה ניתנת לפתרון בעזרת אלגוריתם חמדני.")

C3 = (r"לאליס מחרוזת $x$ של $n$ ביטים. לבוב מחרוזת $y$ של $n$ ביטים. אליס ובוב יודעים ששני המחרוזות $x,y$ לכל היותר שונות בביט אחד." "\n"
      r"אליס ובוב רוצים להבין אם לשניהם אותה מחרוזת." "\n"
      r"אליס מציעה לבוב את האלגוריתם הבא:" "\n"
      r"- אליס תגריל בהתפלגות אחידה אינדקס בטווח $1\le i\le n$, ותשלח לבוב את המיקום $i$ והסיבית $x_i$ במיקום זה." "\n"
      r"- אם $x_i=y_i$ בוב יחזיר \"שווים\"" "\n"
      r"- אם $x_i\ne y_i$ בוב יחזיר \"שונים\"")

C4 = (r"להלן הגדרת בעיית המגדל היציב." "\n"
      r"**קלט:** מערך $A$ בגודל $n$ המייצגים מדיים של תיבות מלבניות. כל תא $1\le i\le n$ במערך מכיל $3$ שדות: אורך $l(i)$, רוחב $w(i)$ וגובה $h(i)$ של התיבה. כל ערכי האורך שונים, כל ערכי הרוחב שונים וכל ערכי הגובה שונים." "\n"
      r"**פלט:** הקובייה שבעזרתן לבנות מגדל יציב הגבוה ביותר מקוביות הקלט." "\n"
      r"הערה: נאמר כי מגדל יציב כאשר מתקיים שאם תיבה $x$ מונחת על תיבה $y$ אז מימדי הבסיס של תיבה $x$ קטנים מימדי הבסיס של תיבה $y$." "\n"
      r"הנח כי המערך $A$ ממוין לפי שדה הרוחב." "\n"
      r"בעיית המגדל היציב ניתנת לפתרון בתכנות דינמי.")

# ---------------------------------------------------------------- solutions
SOL_2A = ("**פתרון רשמי** (24A-A פתרון עמ' 1):\n"
          "```\n"
          "Algorithm CoverPointsWithSegments(points):\n"
          "    Sort(points)\n"
          "    segments = []\n"
          "    end = -inf   # משתנה לציון קצה הימני האחרון של המקטע\n"
          "    for point in points:\n"
          "        if point > end:\n"
          "            # צור מקטע חדש החל מהנקודה הנוכחית\n"
          "            newSegment = [point, point + 1]\n"
          "            segments.append(newSegment)\n"
          "            end = point + 1   # עדכן את קצה המקטע החדש\n"
          "    return segments\n"
          "```\n"
          "**הסבר:**\n"
          "1. **מיון הנקודות:** מתחילים במיון הנקודות הנתונות לפי סדר עולה. שלב זה מבטיח שניגש לנקודות ברצף המאפשר מיקום אופטימלי של המקטעים.\n"
          "2. **אתחול רשימת המקטעים:** יוצרים רשימה ריקה לאחסון המקטעים שיכסו את הנקודות.\n"
          "3. **כיסוי הנקודות:** תרים על רשימת הנקודות הממוינת. עבור כל נקודה, אם היא אינה מכוסה כבר על ידי המקטע האחרון שנוסף לרשימה, יוצרים מקטע חדש באורך 1 שמתחיל בנקודה זו. מקטע זה יכסה את הנקודה עצמה וימתח כדי לכסות כל נקודה בתוך יחידה אחת לימין.\n"
          "4. **עדכון וחזרה:** לאחר הוספת מקטע חדש לכיסוי הנקודה הנוכחית, ממשיכים לנקודה הבאה ובודקים אם יש צורך במקטע חדש או אם היא כבר מכוסה על ידי המקטע האחרון שנוסף. חוזרים על התהליך עד שכל הנקודות מכוסות.\n"
          "5. **החזרת רשימת המקטעים:** ברגע שלא נותרו עוד נקודות שאינן מכוסות, מחזירים את רשימת המקטעים.")

SOL_2B = r"""**פתרון רשמי** (24A-A פתרון עמ' 1-2):
**הבחירה הראשונה:**
יהי $A^*$ פתרון אופטימלי. יהי $[p_1,p_2]$ המקטע הראשון שנבחר בבחירה החמדנית ויהי $[q_1,q_2]$ המקטע הראשון בפתרון $A^*$.
אם המקטעים זהים סימנו.
אחרת, $q_1<p_1$ (לא יתכן כי $p_1<q_1$ כי לפי האלג' $p_1$ היא אחת מנקודות הקלט ואם $p_1<q_1$ אזי ל-$p_1$ אין כיסוי בסתירה ש-$A^*$ מהווה פתרון לבעיה.
נחליף את המקטע $[q_1,q_2]$ בפתרון האופטימלי $A^*$ במקטע $[p_1,p_2]$ ונקבל פתרון אופטימלי חדש.
מדוע? כי הנקודה הראשונה (כפי שהסברנו ששני המקטעי מכסים הינו $p_1$) וכיוון שאורך שני המקטעים הינו $1$ בדיוק אזי $p_2>q_2$ ולכן לפי חוקי תורת הקבוצות הטענה נכונה.
**תת מבנה אופטימלי:**
נוצרה תת בעיה בה יש לכל היותר $n-1$ נקודות (כי הנקודה הראשונה בוודאי מכוסה על ידי המטע הראשון) שיש לכסות עם מינימום מקטעים, ז"א גודל הקלט קטן יותר עם אותה הבעיה."""

SOL_2C = r"""**פתרון רשמי** (24A-A פתרון עמ' 2):
"צוואר הבקבוק" הוא המיון שלוקח $O(n\log n)$
המעבר על כל הנקודות מתבצע פעם אחת בלבד ולכן לוקח $O(n)$
סה"כ $O(n\log n)$"""

SOL_3A = r"""**פתרון רשמי** (24A-A פתרון עמ' 2):
אם האלג' מחזיר "שונים" אזי התשובה $100\%$ נכונה.
אם האלג' מחזיר "שווים" אזי התשובה לאו דווקא נכונה. אם המחרוזות שונות אזי ההסתברות שיבחר ביט השווה לביט שאליס מחזיקה הינו: $\frac{n-1}{n}$ כי יש $n-1$ ביטים שווים מתוך $n$ אפשרויות."""

SOL_3B = r"""**פתרון רשמי** (24A-A פתרון עמ' 3):
$\lceil\log n\rceil+1$
כי יש הביט (ה-$1$ בביטוי) והאינדקס שערכו נע בין $0$ ל-$(n-1)$ ולכן ידרשו לכל היותר $\lceil\log n\rceil$ ביטים לייצוג המספר (כמו בכל תקשורת תקינה, הקביעה היא מראש על כמות הביטים שישלחו או אמורים להיקלט)."""

SOL_3C = r"""**פתרון רשמי** (24A-A פתרון עמ' 3):
בהנחה שהמחרוזות אינם שוות אזי בהסתכלות על חצי מכמות הביטים או שבחצי שבוב בחר נמצא הביט השונה או שהוא נמצא בחצי כמות הביטים שלא נבחרה ולכן הסיכוי הוא $\frac12:\frac12$ (כלומר $\frac12$)."""

SOL_4A = r"""**פתרון רשמי** (24A-A פתרון עמ' 3):
$$T(i)=\begin{cases}0 & ;\ i=0\\ \max\limits_{0\le j\le i-1\ \text{and}\ L(j)>L(i)}\bigl(T(j)+H(i)\bigr) & ;\ \text{else}\end{cases}$$
הנח כי $L(0)$ מוגדר להיות $\infty$. החזר $\max\limits_{1\le i\le n}T(i)$.
הקלט מייצג את סדרת התיבות ממנה מנסים לבנות את המגדל הכי גבוה. מהקוביה הראשונה עד הקוביה ה-$i$.
(הפתרון הרשמי מניח שהמערך ממוין לפי הרוחב בסדר יורד.)"""

SOL_4B = r"""**פתרון רשמי** (24A-A פתרון עמ' 4):
מציאת הגובה הגבוה ביותר דורשת $O(n^2)$ (כיוון שלכל מיקום במערך החד ממדי נצטרך לבצע השוואה עם מקסימום $n$ ערכים). מערך חד ממדי - לכן סיבוכיות המקום $O(n)$."""

SOLVED = {"solutionSource": "solved", "official": False, "confidence": "high"}

CODE_1A = r"""Walk_Through(G, x, y, z)
   for each v in V:  color[v] <- WHITE
   color[z] <- GRAY ; Q <- {z}
   while Q is not empty
      u <- Dequeue(Q)
      for each v in Adj[u]
         if color[v] = WHITE
            color[v] <- GRAY ; Enqueue(Q, v)
   return (color[x] != WHITE and color[y] != WHITE)"""

SOL_1A = (r"""**רעיון.** בטיול מותר לחזור על קודקודים ועל צלעות. לכן קיים טיול מ-$x$ ל-$y$ שעובר דרך $z$ אם ורק אם קיים טיול מ-$x$ ל-$z$ וקיים טיול מ-$z$ ל-$y$ (משרשרים את שניהם). הגרף לא מכוון, ולכן זה שקול לכך ש-$x$ ו-$y$ נמצאים באותו רכיב קשירות כמו $z$, כלומר סריקת BFS (או DFS) מ-$z$ מגיעה גם ל-$x$ וגם ל-$y$.
""" + "```\n" + CODE_1A + "\n```\n" + r"""**נכונות.** אם הסריקה מ-$z$ מגיעה ל-$x$ ול-$y$, יש מסלול $z\leadsto x$ ומסלול $z\leadsto y$; הפיכת הראשון (הגרף לא מכוון) ושרשור השני נותנים טיול $x\leadsto z\leadsto y$. להפך, אם יש טיול כזה, החלק $z\leadsto y$ שלו והחלק $x\leadsto z$ (הפוך) מראים ש-$x$ ו-$y$ ישיגים מ-$z$, ולכן הסריקה מגיעה אליהם.
**סיבוכיות.** סריקת BFS אחת על רשימות סמיכויות: $O(|V|+|E|)$.""")

CODE_1B = r"""Shortest_Through(G, x, y, z)
   dx <- BFS(G, x)        // dx[v] = distance from x (infinity if unreachable)
   dy <- BFS(G, y)        // dy[v] = distance from y
   if dx[y] = infinity  return false
   return (dx[z] + dy[z] = dx[y])"""

SOL_1B = (r"""**רעיון.** הגרף לא ממושקל, ולכן BFS מחשב מרחקים (מספר צלעות במסלול קצר ביותר). קיים מסלול קצר ביותר מ-$x$ ל-$y$ שעובר דרך $z$ אם ורק אם $d(x,z)+d(z,y)=d(x,y)$ (והמרחק סופי). מריצים BFS מ-$x$ ומ-$y$; בגרף לא מכוון $d(z,y)=d(y,z)$.
""" + "```\n" + CODE_1B + "\n```\n" + r"""**נכונות.** אם $d(x,z)+d(z,y)=d(x,y)$, שרשור מסלול קצר ביותר $x\leadsto z$ עם מסלול קצר ביותר $z\leadsto y$ נותן הילוך באורך $d(x,y)$ מ-$x$ ל-$y$. הילוך באורך המרחק אינו חוזר על קודקוד (אחרת היה אפשר לקצר אותו), ולכן זהו מסלול קצר ביותר שעובר דרך $z$. להפך, אם מסלול קצר ביותר $P$ עובר דרך $z$, אז החלקים שלו $x\leadsto z$ ו-$z\leadsto y$ באורכים לפחות $d(x,z)$ ו-$d(z,y)$, כך ש-$d(x,y)=|P|\ge d(x,z)+d(z,y)$; מאי-שוויון המשולש $d(x,y)\le d(x,z)+d(z,y)$, ולכן יש שוויון.
**סיבוכיות.** שתי סריקות BFS: $O(|V|+|E|)$.""")

SOL_4C = r"""**זמן $O(n^2)$, מקום $O(n)$.**
את גובה המגדל מחשבים כמו בסעיף הקודם: לכל $i$ עוברים על כל $j<i$, כלומר $O(n^2)$ זמן, ושומרים את המערך החד ממדי $T$. כדי להחזיר את התיבות שומרים מערך חד ממדי נוסף $P$: $P(i)$ הוא האינדקס $j$ שבו התקבל המקסימום עבור $T(i)$ (התיבה שמתחת לתיבה $i$ במגדל הטוב ביותר שבראשו $i$), או $0$ אם התיבה $i$ היא התחתונה. בסוף מוצאים את $i$ שעבורו $T(i)$ מקסימלי ($O(n)$) והולכים אחורה לפי $P$ עד $0$, ומדפיסים את התיבות. המגדל מכיל לכל היותר $n$ תיבות, ולכן השחזור לוקח $O(n)$.
סה"כ זמן $O(n^2)+O(n)=O(n^2)$, ומקום: שני מערכים בגודל $n$, $O(n)$."""

SOL_5 = r"""**לא נכון.** הבחירה החמדנית לפי המקטע הקצר ביותר אינה מבטיחה פתרון אופטימלי. דוגמה נגדית: המקטעים $[0,10]$, $[9,12]$, $[11,20]$. הקצר ביותר הוא $[9,12]$; הוא נחתך עם שני האחרים, ולכן מתקבל מקטע אחד בלבד, בעוד שהפתרון האופטימלי בוחר שניים: $[0,10]$ ו-$[11,20]$. (הבחירה החמדנית הנכונה היא לפי זמן הסיום המוקדם ביותר.)"""

questions = [
    Q(1, "א", "algorithm", "graphs_search",
      r"כתבו אלגוריתם (או פסודוקוד) המקבל כקלט את הגרף $G$ (המיוצג על ידי רשימת סמיכויות) ושלושה קודקודים $x,y,z\in V$ בגרף $G$ ומחזיר אמת אם קיים **טיול** מ-$x$ ל-$y$ שעובר דרך $z$.",
      SOL_1A, points=10, contextId="c1", **SOLVED),
    Q(1, "ב", "algorithm", "graphs_search",
      r"כתבו אלגוריתם (או פסודוקוד) המקבל כקלט את הגרף $G$ (המיוצג על ידי רשימת סמיכויות) ושלושה קודקודים $x,y,z\in V$ בגרף $G$ ומחזיר אמת אם קיים מסלול קצר ביותר מ-$x$ ל-$y$ שעובר דרך $z$.",
      SOL_1B, points=15, contextId="c1", **SOLVED),

    Q(2, "א", "algorithm", "greedy", "כתבו אלגוריתם (או פסודו-קוד) לפתרון הבעיה.", SOL_2A, points=10, contextId="c2"),
    Q(2, "ב", "proof", "greedy", "הוכיחו את נכונות האלגוריתם שהצגתם.", SOL_2B, points=10, contextId="c2"),
    Q(2, "ג", "computation", "complexity_recurrence", "מה סיבוכיות זמן הריצה של האלגוריתם שהצגתם? נמקו תשובתכם", SOL_2C, points=5, contextId="c2"),

    Q(3, "א", "computation", "randomized",
      "מה ההסתברות שהאלגוריתם יחזיר תשובה נכונה? אבחנו בין המקרה שהאלגוריתם יחזיר שווים לבין המקרה שיחזיר לא שווים? נמקו תשובתכם",
      SOL_3A, points=12, contextId="c3"),
    Q(3, "ב", "computation", "randomized",
      "כמה ביטים נדרשת אליס להעביר לבוב באלגוריתם שהצענו? נמקו תשובתכם", SOL_3B, points=8, contextId="c3"),
    Q(3, "ג", "computation", "randomized",
      r"מה ההסתברות שהאלגוריתם יחזיר תשובה נכונה אם אליס תשלח לבוב באופן אקראי $\frac n2$ ביטים שונים מתוך המחרוזת $x$? נמקו תשובתכם",
      SOL_3C, points=5, contextId="c3", confidence="med"),

    Q(4, "א", "algorithm", "dp_optimization",
      r"כתבו נוסחה רקורסיבית $T(i)$ המקבלת אינדקס $1\le i\le n$ ומחזירה את גובה המגדל היציב הגבוה ביותר. פרטו מה מייצג אינדקס $i$ בקלט הנוסחה $T$.",
      SOL_4A, points=15, contextId="c4", confidence="med"),
    Q(4, "ב", "computation", "complexity_recurrence",
      "מה סיבוכיות הזמן והמקום לאלגוריתם תכנות דינמי למציאת גובה המגדל היציב הגבוה ביותר. נמקו תשובתכם (אין צורך לפרט את האלגוריתם עצמו).",
      SOL_4B, points=5, contextId="c4", confidence="med"),
    Q(4, "ג", "computation", "complexity_recurrence",
      "מה סיבוכיות הזמן והמקום לאלגוריתם תכנות דינמי המחזיר את הקוביות מהם ניתן לבנות את המגדל היציב הגבוה ביותר. נמקו תשובתכם (אין צורך לפרט את האלגוריתם עצמו).",
      SOL_4C, points=5, contextId="c4", **SOLVED),

    Q(5, "", "truefalse", "greedy",
      "**שאלת בונוס (5 נקודות)** - ענה נכון או לא נכון, אין צורך לנמק." "\n"
      "בבעיית תזמון מקטעים, הגישה החמדנית הבוחרת במקטע שמשך הזמן שלו קצר ביותר תניב בהכרח פתרון אופטימלי.",
      SOL_5, points=5, verdict=False, **SOLVED),
]

exam = {
    "examCode": "24A-A",
    "examLabel": "אלגוריתמים 1 (60072), סמסטר א' תשפ\"ד, מועד א (18.3.24)",
    "year": 2024,
    "examDate": "18.3.2024",
    "sourceFile": "24A-A exam pp.1-17",
    "solutionFile": "24A-A partial solution pp.1-4",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1: טיול בגרף", "text": C1},
        "c2": {"kind": "text", "title": "שאלה 2: כיסוי נקודות במקטעים", "text": C2},
        "c3": {"kind": "text", "title": "שאלה 3: אליס ובוב", "text": C3},
        "c4": {"kind": "text", "title": "שאלה 4: המגדל היציב", "text": C4},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
