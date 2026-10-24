# -*- coding: utf-8 -*-
"""Generator for tools/raw/24A-C.json -- algorithms-1 (60172), semester A 2024, reserve sitting ("מועד מילואים", 31.3.24).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24A-C.py

Source: one 11-page file in which the exam questions sit in answer boxes together with the official typed solution
(the second file with the same text was ignored). Cover: 2 h, 4 questions x 25 + a 5-point bonus, cap 105.
Items: Q1 a,b,c (15/5/5), Q2 a,b,c (10/10/5), Q3 a,b,c (10/10/5), Q4 a,b,c (15/5/5), bonus (num 5, 5 points).

Transcription notes
- Q1a: the official pseudocode writes "BSF(G-x,v)"; transcribed as printed (it means BFS).
- Q3b: the printed tree has no bit labels and no root weight; the figure is the official handwritten tree.
- Q4: the example array is A={1,4,6,4,5,3,3,2,1,3}; the printed answer path is 1 -> 2 -> 5 -> last.
- Bonus: the graph figure in the exam shows the lecturer's handwritten Prim order; the question uses a clean redraw
  (tools/verify/24A-C/draw_graph.py) and the original crop only inside the solution.

Checks (tools/verify/24A-C/checks.py, networkx + brute force; Python only, no C in this sitting):
- Q1: the official BFS-from-one-neighbour algorithm equals networkx articulation_points on 3000 random graphs.
- Q2: greedy "lightest first" equals brute-force knapsack on 4000 random inputs with non-increasing values.
- Q3: the code is prefix-free (Kraft sum 1), costs the optimal Huffman cost for a1=3,a2=4,a3=3,a4=1,a5=2; the geometric
  sequence 1,3,9,27,81 gives code lengths 4,4,3,2,1; ratios q=2..11 give the same chain tree, q=1 does not.
- Q4: both official recurrences equal a BFS optimum on 5000 random arrays; the example gives 3.
- Bonus: Prim from C can output the weights 8,9,9,8,11,12,13 (2 tie-break orders exist).
Graph data: tools/verify/24A-C/graphs.json.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24A-C.json"


def Q(num, part, kind, topic, question, solution, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


# ---------------------------------------------------------------- contexts
C1 = r"יהי $G=(V,E)$ גרף לא מכוון."

C2 = (r"לפניכם גרסה בינארית (גרסת 0-1) של בעיית התרמיל." "\n"
      r"המטרה: למקסם את ערך הפריטים הנבחרים (כל פריט יכול להיבחר לכל היותר פעם אחת), כך שמשקלם יהיה קטן או שווה למיעד נתון $S$. "
      r"ידוע שאם נמיין את מערך המשקלים בסדר עולה לפי משקלים נקבל את מערך הערכים ממוין בסדר יורד לפי ערכם. "
      r"במילים אחרות - ככל שהפריט כבד יותר, כך הוא פחות יקר." "\n"
      r"לדוגמה:" "\n"
      r"משקלים: $1,4,5,7,10$" "\n"
      r"ערכים: $8,6,5,4,2$" "\n"
      r"**הבעיה ניתנת לפתרון בעזרת אלגוריתם חמדני.**")

C4 = (r"**משחק קפיצות חדש:** נתון מערך $A$ בגודל $n$ שבו כל איבר מייצג את המספר המרבי של הצעדים שניתן לבצע קדימה מאותו אינדקס. "
      r"המשימה היא למצוא את המספר המינימלי של הקפיצות כדי להגיע לסוף המערך (אינדקס $n$) החל מאינדקס $1$." "\n"
      r"**לדוגמה:** עבור המערך $A=\{1,4,6,4,5,3,3,2,1,3\}$ הפתרון האופטימאלי הוא $3$ צעדים: מאינדקס $1$ מגיעים לאינדקס $2$, "
      r"משם קופצים לאינדקס $5$, ומשם קופצים כבר למקום האחרון." "\n"
      r"הבעיה ניתנת לפתרון בתכנון דינמי.")

# ---------------------------------------------------------------- solutions
SOL_1A = ("**פתרון רשמי** (24A-C פתרון עמ' 2):\n"
          "```\n"
          "Is_cut_vertex(G,x)\n"
          "  If deg(x)<=1\n"
          "      return \"x is not cut\"\n"
          "  select v in N(x)\n"
          "  d[] = BSF(G-x,v)\n"
          "  for each u in N(x)\n"
          "      if d[u] = inf\n"
          "          return \"x is a cut\"\n"
          "  return \"x is not cut\"\n"
          "```")

SOL_1B = (r"**פתרון רשמי** (24A-C פתרון עמ' 3):" "\n"
          r"בהתאם להגדרה: $x$ - צומת הפרדה אמ\"מ **יש** זוג שכנים שלו שנמצאים בשני רכיבי קשירות שונים בגרף ללא $x$.")

SOL_1C = (r"**פתרון רשמי** (24A-C פתרון עמ' 3):" "\n"
          r"$O(V+E)+O(\deg(x))=O(V+E)$")

SOL_2A = ("**פתרון רשמי** (24A-C פתרון עמ' 4):\n"
          "1. $n=|w|$\n"
          "2. נמיין פריטים כך שהמערך $w$ ממוין בסדר עולה $w_1\\le\\cdots\\le w_n$ (ובהתאם מערך $v$ ממוין בסדר יורד)\n"
          "3. $G=\\{\\}$\n"
          "4. $i=1$\n"
          "5. כל עוד $i$ לא גדול מ-$n$ ו-$S\\ge w_i$:\n"
          "   $G=G\\cup\\{i\\}$, $S=S-w_i$, $i{+}{+}$\n"
          "6. החזר $G$")

SOL_2B = r"""**פתרון רשמי** (24A-C פתרון עמ' 5):
אם אין מקום בתרמיל ($w_1>S$) אז האלגוריתם יחזיר קבוצה ריקה, אחרת האלגוריתם מחזיר את הקבוצה של הפריטים שאפשר להכניס לתוך התרמיל (סכום משקליהם לא גדול מ-$S$).
נוכיח שערך הקבוצה הוא מקסימלי.
**א. נוכיח שהאלגוריתם מקיים את תכונת הבחירה החמדנית**, ז"א שיש פתרון אופטימלי שמכיל פריט 1 עם משקל $w_1$.
נניח $A=\{i_1\le i_2\le\ldots\le i_k\}$ פתרון אופטימאלי. אם $i_1=1$ - הוכחנו. אחרת **נחליף** את $i_1$ ב-$1$: $B=A-\{i_1\}\cup\{1\}$. מכיוון ש-$w_1\le w(i_1)$ $\Rightarrow$ משקל הפריטים ב-$B$ לא גדול מ-$S$, ולכן $B$ פתרון תקין. מצד שני $v_1\ge v(i_1)$, ולכן $B$ פתרון אופטימלי שמכיל את $1$.
**ב. נוכיח שהאלגוריתם מקיים את תת המבנה האופטימלי.**
נוכיח שאם $A=\{1\le i_2\le\ldots\le i_k\}$ הוא פתרון אופטימלי, אז $A_1=A-\{1\}=\{i_2\le\ldots\le i_k\}$ הוא פתרון אופטימלי עבור $(n-1)$ פריטים (ללא הפריט הראשון) ועבור $S_1=S-w_1$.
נניח קיים פתרון $B_1$ עבור הבעיה "הקטנה" ($S_1$ ו-$(n-1)$ פריטים) עם ערך יותר גדול מערך $A_1$. אזי $B_1\cup\{1\}$ הוא פתרון עבור $S$ וערך של הקבוצה $|A|<|B_1\cup\{1\}|$ - סתירה.
**אפשרות שניה להוכחה:**
נניח $G=\{1,2,\ldots,k\}$ הפלט של האלגוריתם החמדן. נוכיח ש-$G$ פתרון **אופטימלי** (מקסימלי).
נניח בשלילה ש-$G$ אינו פתרון אופטימלי. מכל הפתרונות האופטימליים, ניקח פתרון $OPT$ הכי "קרוב" ל-$G$: $OPT=\{i_1\le i_2\le\ldots\le i_l\}$, כך שיש prefix משותף **הכי ארוך**: $i_1=1,i_2=2,\ldots,i_j=j;\ i_{j+1}\ne j+1$ **ואין** פתרון אופטימלי שבו מתקיים גם $i_{j+1}=j+1$.
אם $i_{j+1}\ne j+1$, אז $i_{j+1}>j+1$, ולכן $w_{j+1}\le w_{i_{j+1}}$, לכן $OPT1=Opt-\{i_{j+1}\}\cup\{j+1\}$ הוא גם פתרון כי משקלו של $OPT1$ לא גדול ממשקלו של $Opt$ וגם אופטימלי - כי $v_{j+1}\ge v_{i_{j+1}}$, כלומר, קיים פתרון אופטימלי "יותר קרוב" ל-$G$ ($i_{j+1}=j+1$). סתירה.
לכן $G$ **פתרון אופטימלי**."""

SOL_2C = r"""**פתרון רשמי** (24A-C פתרון עמ' 6):
$O(n\log n)$"""

SOL_3A = r"""**פתרון רשמי** (24A-C פתרון עמ' 7):
$a_1=00,\ a_2=11,\ a_3=01,\ a_4=100,\ a_5=101$
כן, הקוד יכול להיות קוד הופמן. השכיחויות המתאימות: $a_1=3,\ a_2=4,\ a_3=3,\ a_4=1,\ a_5=2$ (סכום $13$), והעץ המתקבל:
![עץ הופמן לשכיחויות 3,4,3,1,2: השורש 13, הבנים 6 ו-7](images/exams/24A-C-Q3a-tree.png)"""

SOL_3B = r"""**פתרון רשמי** (24A-C פתרון עמ' 8):
העץ שנבנה בעזרת האלגוריתם של הופמן (הסדרה $1,3,9,27,81$, עץ "שרוך": כל איחוד מוסיף את העלה הבא):
![עץ הופמן לשכיחויות 1,3,9,27,81: מיזוג 1 ו-3 ל-4, אחר כך 13, 40 ולבסוף השורש](images/exams/24A-C-Q3b-tree.png)"""

SOL_3C = r"""**פתרון רשמי** (24A-C פתרון עמ' 8):
דוגמה נגדית עבור $q=1$."""

SOL_4A = r"""**פתרון רשמי** (24A-C פתרון עמ' 9):
$C(i)$ - מספר מינימלי של הקפיצות הנדרשות להגעת לסוף המערך $n$ ממקום $i$.
$$C(i)=\begin{cases}0 & ,\ i=n\\ 1+\min\limits_{1\le j\le\min\{A[i],\,n-i\}} C(i+j) & \end{cases}$$
או:
$C(i)$ - מספר מינימלי של הקפיצות הנדרשות להגעת למקום $i$ מתחילת המערך.
$$C(i)=\begin{cases}0 & ,\ i=1\\ 1+\min\limits_{(1\le j<i)\wedge(j+A[j]\ge i)} C(j) & \end{cases}$$"""

SOL_4B = r"""**פתרון רשמי** (24A-C פתרון עמ' 10):
סיבוכיות הזמן $O(n^2)$ וסיבוכיות המקום $O(n)$"""

SOL_4C = r"""**פתרון רשמי** (24A-C פתרון עמ' 10):
סיבוכיות הזמן $O(n^2)$ (או $O(n)$ אם כבר בנינו את הטבלה) וסיבוכיות המקום $O(n)$"""

SOL_5 = ("**פתרון רשמי** (24A-C פתרון עמ' 11): נכון.\n"
         "הפתרון הרשמי מציין על הגרף את סדר הוספת הצלעות על ידי PRIM מהצומת $C$: "
         "משקלים $8,9,9,8,11,12,13$ (התיקו בין שתי צלעות שמשקלן $9$ מאפשר סדר כזה).\n"
         "![הגרף עם מספרי הסדר שרשם המרצה (הסדר הוא סדר הוספת הצלעות על ידי PRIM)](images/exams/24A-C-Qb-graph-sol.png)")

questions = [
    Q(1, "א", "algorithm", "graphs_search",
      r"כתבו אלגוריתם יעיל המקבל כקלט את הגרף $G$ (המיוצג על ידי רשימת סמיכויות) וקודקוד $x\in V$ בגרף $G$ ומחזיר אמת אם הצומת $x$ הוא צומת הפרדה." "\n"
      r"תזכורת: $v$ הינה צומת הפרדה אמ\"מ בגרף $G-v$ ישנם יותר רכיבי קשירות ממה שהיה בגרף $G$.",
      SOL_1A, points=15, contextId="c1"),
    Q(1, "ב", "proof", "graph_proofs",
      "נמקו בקצרה את נכונות האלגוריתם.", SOL_1B, points=5, contextId="c1"),
    Q(1, "ג", "computation", "graphs_search",
      "מהי סיבוכיות הזמן של האלגוריתם שהצגתם בסעיף א. נמקו בקצרה את תשובתכם.", SOL_1C, points=5, contextId="c1"),

    Q(2, "א", "algorithm", "greedy",
      r"בנו אלגוריתם לפתרון בעיית התרמיל בגרסה זו. הקלט: שני מערכים $w[\,]$ (משקלים של הפריטים), $v[\,]$ (הערכים של הפריטים) ומשקל המקסימלי האפשרי $S$.",
      SOL_2A, points=10, contextId="c2"),
    Q(2, "ב", "proof", "greedy",
      "הוכיחו את נכונות האלגוריתם שהצגתם.", SOL_2B, points=10, contextId="c2"),
    Q(2, "ג", "computation", "complexity_recurrence",
      "מהי סיבוכיות זמן הריצה של האלגוריתם שהצגתם? נמקו בקצרה תשובתכם", SOL_2C, points=5, contextId="c2"),

    Q(3, "א", "computation", "huffman",
      "האם הקוד הבא יכול להיות קוד הופמן עבור שכיחויות כלשהן של האותיות:\n"
      "`00`, `11`, `01`, `100`, `101`\n"
      "אם לא - נמקו מדוע, אם כן - תנו דוגמא לשכיחויות מתאימות.",
      SOL_3A, points=10),
    Q(3, "ב", "computation", "huffman",
      r"מהו קוד הופמן אופטימלי עבור סדרת השכיחויות הבאה, המבוססת על 5 האברים הראשונים של הסדרה ההנדסית $a_1=1,\ a_2=3,\ a_3=9,\ a_4=27,\ a_5=81$ ?" "\n"
      "בנו עץ לפי האלגוריתם של הופמן.",
      SOL_3B, points=10),
    Q(3, "ג", "truefalse", "huffman",
      "האם עבור 5 האברים הראשונים של כל סדרה הנדסית נקבל עץ זהה לעץ מסעיף הקודם? אם כן - נמקו, אם לא - תנו דוגמא נגדית.",
      SOL_3C, points=5, verdict=False),

    Q(4, "א", "algorithm", "dp_optimization",
      r"הציגו נוסחה רקורסיבית המחשבת את המספר המינימלי של הקפיצות הנדרשות להגעת לסוף המערך." "\n"
      "יש להגדיר (במילים) את הפונקציה הרקורסיבית ולנמק בקצרה את הנכונות של הנוסחה.",
      SOL_4A, points=15, contextId="c4"),
    Q(4, "ב", "computation", "complexity_recurrence",
      "מהי סיבוכיות הזמן וסיבוכיות המקום לאלגוריתם תכנון דינמי למציאת המספר המינימלי של הקפיצות כדי להגיע לסוף המערך (אין צורך לפרט את האלגוריתם עצמו).",
      SOL_4B, points=5, contextId="c4"),
    Q(4, "ג", "computation", "complexity_recurrence",
      "מה סיבוכיות הזמן וסיבוכיות המקום לאלגוריתם תכנון דינמי המחזיר את הפתרון עצמו - האינדקסים שעוברים בדרך. נמקו את תשובתכם (אין צורך לפרט את האלגוריתם עצמו).",
      SOL_4C, points=5, contextId="c4"),

    Q(5, "", "truefalse", "mst",
      "**שאלה בונוס (5 נקודות)** - ענו נכון או לא נכון, אין צורך לנמק." "\n"
      "נתון הגרף הבא." "\n"
      "![הגרף הנתון: שמונה צמתים, הצומת C בפנים, והמשקלים 8 עד 15 על הצלעות](images/exams/24A-C-Qb-graph.png)" "\n"
      "מפעילים עליו את אלגוריתם PRIM (למציאת עץ פורש מינימלי) החל מקודקוד $C$. להלן הטענה הבאה:" "\n"
      "סדר המשקלים של צלעות העץ ש-PRIM יכניס לעפ\"מ (עץ פורש מינימלי) יכול להיות (משמאל לימין): $8,9,9,8,11,12,13$",
      SOL_5, points=5, verdict=True),
]

exam = {
    "examCode": "24A-C",
    "examLabel": "אלגוריתמים 1 (60172), סמסטר א' תשפ\"ד, מועד מילואים (31.3.24)",
    "year": 2024,
    "examDate": "31.3.2024",
    "sourceFile": "24A-C exam pp.1-11",
    "solutionFile": "24A-C official solution (typed in the answer boxes) pp.1-11",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1: צומת הפרדה", "text": C1},
        "c2": {"kind": "text", "title": "שאלה 2: בעיית התרמיל (0-1)", "text": C2},
        "c4": {"kind": "text", "title": "שאלה 4: משחק קפיצות", "text": C4},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
