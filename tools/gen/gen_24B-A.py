# -*- coding: utf-8 -*-
"""Generator for tools/raw/24B-A.json -- algorithms-1 (60172), semester B 2024, moed A (24.7.2024).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24B-A.py

Source: one 13-page file = exam booklet with the official typed solution written in the answer boxes
(no blank exam exists). Cover: 4 questions x 25 + a 5-point bonus, cap 105.
Items: Q1 a,b,c (10/7/8), Q2 a,b,c (5/10/10), Q3 a,b (15/10), Q4 a,b,c (15/5/5), bonus (5).
Q4c prints no points; 25 - 15 - 5 = 5.

Transcription notes
- The official solution figures (Q1a, Q1b, Q3a tree, Q3b graph) are cropped from the solution file (pure drawings).
  The Q1b crop carries a white smudge that is in the source file.
- Q2b: official pseudocode transcribed as is (it only returns the list C of station positions).
- Q4a has two official solutions (a forward 1 -> i recurrence and a backward K -> i recurrence); both are kept.
- Q4b/Q4c: the official text is short ("time K, space K, pseudo-polynomial; K=7 table").

Checks (tools/verify/24B-A/checks.py, networkx + brute force):
- Q1: both counterexamples have |E|=|V|, are disconnected, and (Q1b) BFS from 0 and the DFS forest both have 3
  edges; claim (c) holds over every graph with |E|=|V| and up to 7 vertices (95 graphs).
- Q2: the official algorithm is valid and optimal against brute force (300 random); [3,9,16] and [4,9,16] both cover.
- Q3a: the code is prefix-free, Kraft sum 1, cost 18 = optimal Huffman cost for 1,1,2,2,2.
  Q3b: the weight-10 edge is a bridge and in all 3 MSTs.
- Q4: both recurrences equal BFS shortest distance for K=1..399; the K=7 table is 0 1 1 2 3 2 3.
- Bonus: the true suffix array of BANANABAN is 6 8 4 2 7 1 9 5 3 (positions 3 and 4 of the given array swapped).
Graph data for the visualizer: tools/verify/24B-A/graphs.json (Q1a, Q1b, Q3a tree, Q3b).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24B-A.json"


def Q(num, part, kind, topic, question, solution, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


C1 = (r"יהיו $G=(V,E)$ גרף לא מכוון כך ש-$|E|=|V|\neq\emptyset$. שלוש הטענות הבאות מתייחסות לגרף זה." "\n"
      r"כתבו נכון או לא נכון על כל הטענה, נמקו תשובתכם (אם הטענה לא נכונה, הביאו דוגמה נגדית, ואם הינה נכונה, הסבירו מדוע).")

C2 = (r"במדינת אלגו-לנד סללו פסי רכבת בקו ישר לרוחבה של המדינה ממערב למזרח (מקצה שמאל לקצה ימין). לאורך המסלול, "
      r"פסי הרכבת חוצים $K$ ערים שונות, כאשר עבור כל עיר נתון המיקום שלה (נקודה בודדת $x_i$ על ציר פסי הרכבת)." "\n"
      r"המטרה שלנו היא לבחור מספר מיקומים ספציפיים על פסי הרכבת לבניית תחנות לרווחת התושבים, כאשר התחנות לא חייבות "
      r"להיות במיקומים המדויקים של הערים. הדרישה היחידה היא שכל עיר חייבת להיות במרחק של $D$ ק\"מ לכל היותר מאיזושהי תחנת רכבת." "\n"
      r"על מנת לחסוך בעלויות נרצה לתכנן אלגוריתם המחזיר מספר מינימלי של תחנות ומיקומיהם (קואורדינטות $x$ על ציר פסי הרכבת) שיש להקים." "\n"
      r"**לדוגמה:** עבור $K=4$ ערים הממוקמות בקואורדינטות $[1,5,9,16]$ ומרחק $D=3$, קיים פתרון אופטימלי עם 3 תחנות רכבת "
      r"בקואורדינטות $[3,9,16]$ (התחנה הראשונה משותפת לשתי הערים הראשונות)." "\n"
      r"הבעיה ניתנת לפתרון באמצעות **אלגוריתם חמדן**.")

C4 = (r"בהינתן מספר טבעי $K$, המשימה היא למצוא את המספר המינימלי של פעולות משלושת הסוגים הבאים:" "\n"
      r"(i) להגדיל מספר ב-1" "\n"
      r"(ii) להכפיל מספר ב-2" "\n"
      r"(iii) להכפיל מספר ב-3" "\n"
      r"ההופכות 1 ל-$K$." "\n"
      r"**לדוגמה:** כדי לקבל 10 חייבים לעשות 3 פעולות (מימין לשמאל): $1\cdot 3=3$, $3\cdot 3=9$, $9+1=10$." "\n"
      r"הבעיה ניתנת לפתרון בתכנון דינמי.")

SOL_1A = r"""**פתרון רשמי** (24B-A עמ' 2): הטענה לא נכונה.
**דוגמה נגדית:** גרף עם 6 קודקודים ו-6 צלעות. הגרף אינו קשיר.
![דוגמה נגדית: שני משולשים זרים על שישה קודקודים ושש צלעות](images/exams/24B-A-Q1a-graph.png)"""

SOL_1B = r"""**פתרון רשמי** (24B-A עמ' 3): הטענה לא נכונה.
**דוגמה נגדית:** גרף עם 5 קודקודים ו-5 צלעות. הגרף אינו קשיר.
אם מריצים אלגוריתם BFS מקודקוד $0$, מקבלים עץ פורש בעל 3 צלעות. האלגוריתם לא יגיע לקודקוד $4$.
DFS מבצע מעברים בין רכיבי קשירות שונים, כלומר מחזיר יער. מכיוון שאין קשתות ברכיב הקשירות שמכיל את הקודקוד $4$, נקבל שכמות הצלעות המוחזרות היא 3.
![דוגמה נגדית: ארבעה קודקודים קשורים בחמש צלעות וקודקוד 4 מבודד](images/exams/24B-A-Q1b-graph.png)"""

SOL_1C = r"""**פתרון רשמי** (24B-A עמ' 4): הטענה נכונה.
**הוכחה.** נניח בשלילה שהגרף לא קשיר, לכן יש לו $k>0$ ר"ק (רכיבי קשירות). נסמן ב-$n_i$ את מספר הקודקודים ברכיב $i$.
בכל הרצת DFS אנו תמיד נקבל אותה כמות צלעות:
$$|E_{DFS(G)}|=(n_1-1)+(n_2-1)+\cdots+(n_k-1)$$
וזה לא משנה באיזה קודקוד נתחיל, מכיוון ש-DFS מבצע מעברים בין כל רכיבי הקשירות בגרף.
אלגוריתם BFS אינו מבצע מעברים בין רכיבי קשירות.
נקח ר"ק עם מספר קודקודים מינימלי, ללא הגבלת הכלליות זה הר"ק הראשון, עם $n_1$ קודקודים. יהיה $v$ קודקוד של אותו ר"ק. לכן $BFS(G,v)$ יחזיר $n_1-1$ צלעות.
בגלל שלפחות באחד מהר"ק יש יותר מקודקוד אחד (כי נתון שמספר הצלעות בגרף שונה מ-0), אז $(n_2-1)+\cdots+(n_k-1)>0$, ולכן $n_1-1$ קטן מ-$|E_{DFS(G)}|$.
סתירה ל-$|E_{BFS(G,v)}|=|E_{DFS(G)}|$. לכן הגרף חייב להיות קשיר."""

SOL_2A = r"""**פתרון רשמי** (24B-A עמ' 5): יש מספר רב של פתרונות אופטימליים, למשל: $[4,9,16]$."""

CODE_2B = r"""Algorithm (X)
Assume: K>0
1.   J=1, C[1]=x1+D //the first station
2.   For i=2 to K
        If xi-D > C[J]
            J++
            C[J]=xi+D
3.   Return C"""

SOL_2B = (r"""**פתרון רשמי** (24B-A עמ' 6):
**רעיון:** כל פעם למקם תחנה הכי רחוק שאפשר כך שהעיר עדיין תהיה "מכוסה" (במרחק עד $D$ ק"מ ממנה), ומשם ממשיכים לעיר הבאה שאינה "מכוסה" על ידי אותה תחנה.
**קלט:** מערך ממוין $X=[x_1,\ldots,x_K]$ של מיקומי ערים.
""" + "```\n" + CODE_2B + "\n```")

SOL_2C = r"""**פתרון רשמי** (24B-A עמ' 7):
1. האלגוריתם מחזיר פתרון: לפי האלגוריתם עבור כל עיר יש תחנה שהיא לא יותר ממרחק $D$ מהעיר.
2. נניח $D=[d_1,d_2,\ldots,d_p]$ קבוצת המקומות של התחנות שהחזיר אלגוריתם חמדן. נוכיח ש-$D$ פתרון אופטימלי (מינימלי).

נניח בשלילה ש-$D$ אינו פתרון אופטימלי. מכל הפתרונות המינימליים, ניקח פתרון $OPT=\{b_1,b_2,\ldots,b_l\}$ הכי "קרוב" ל-$D$, כך שיש prefix משותף הכי ארוך:
$$d_1=b_1,\ d_2=b_2,\ \ldots,\ d_i=b_i;\quad d_{i+1}\neq b_{i+1}$$
ואין פתרון אופטימלי שבו מתקיים גם $d_{i+1}=b_{i+1}$.
יהיה $x_m$ העיר האחרונה שמכוסה על ידי $i$ התחנות ה"משותפות" הראשונות. תחנות מ-$b_{i+1}$ והלאה מכסות ערים מ-$m+1$ עד $K$.
$d_{i+1}=x_{m+1}+D$. לפי הבחירה החמדנית $d_{i+1}>b_{i+1}$ (כי האלגוריתם עבור כל עיר שלא "מכוסה" על ידי תחנות קודמות בוחר מיקום לתחנה הכי ימני שאפשר).
לכן תחנה $d_{i+1}$ מכסה כל הערים שמכסה תחנה $b_{i+1}$ ואולי יותר. לכן $OPT-\{b_{i+1}\}\cup\{d_{i+1}\}$ הוא גם פתרון (מכסה כל הערים) וגם אופטימלי (כי נשארו אותו מספר תחנות).
כלומר, קיים פתרון אופטימלי "יותר קרוב" ל-$D$ ($d_{i+1}=b_{i+1}$). סתירה. לכן $D$ פתרון אופטימלי."""

SOL_3A = r"""**פתרון רשמי** (24B-A עמ' 8): כן, למשל עבור השכיחויות $a=1,\ b=1,\ c=2,\ d=2,\ e=2$ (סך הכול 8):
![עץ הופמן: השורש 8, ענף 0 לצומת 4 עם העלים c ו-d, ענף 1 לצומת 4 עם העלה e והצומת 2 שבניו a ו-b](images/exams/24B-A-Q3a-tree.png)
הקידוד המתקבל: `c`=00, `d`=01, `e`=10, `a`=110, `b`=111."""

SOL_3B = r"""**פתרון רשמי** (24B-A עמ' 9): הטענה לא נכונה (קיים עץ פורש מינימלי המכיל את $e_1$).
אם הצלע מהווה גשר, היא חייבת להיות בכל עץ פורש מינימלי.
**דוגמה:** הצלע שמשקלה 10 חייבת להיות בכל עץ פורש מינימלי.
![דוגמה: משולש עם שלוש צלעות במשקל 2 וצלע גשר במשקל 10 לקודקוד 3](images/exams/24B-A-Q3b-graph.png)"""

SOL_4A = r"""**פתרון רשמי** (24B-A עמ' 10-11):
**פתרון ראשון:** $C(i)$ - המספר המינימלי של פעולות הנדרשות כדי להפוך $1$ ל-$i$.
$$C(i)=\begin{cases}0 & ;\ i=1\\ \infty & ;\ i\notin\mathbb{N}\ (i\text{ is not an integer})\\ \min\bigl(C(i-1),\,C(i/2),\,C(i/3)\bigr)+1 & ;\ \text{else}\end{cases}$$
יש עד 3 אפשרויות בכל שלב להגיע ל-$i$. בוחרים ביניהן את האופציה הטובה ביותר.
הערך $\infty$ עבור $i\notin\mathbb{N}$ הוא טריק כדי לא להתייחס לכל האופציות בנפרד (האם מספר זוגי, האם מתחלק ב-3).
**פתרון שני:** $C(i)$ - המספר המינימלי של פעולות הנדרשות כדי להפוך $K$ ל-$i$, כאשר הפעולות הן:
(i) להקטין מספר ב-1, (ii) לחלק מספר זוגי ב-2, (iii) לחלק מספר (שמתחלק ב-3) ב-3.
$$C(i)=\begin{cases}0 & ;\ i=K\\ \infty & ;\ i>K\\ \min\bigl(C(i+1),\,C(2i),\,C(3i)\bigr)+1 & ;\ \text{else}\end{cases}$$"""

SOL_4B = r"""**פתרון רשמי** (24B-A עמ' 12):
זמן הריצה הוא $K$ ומקום - $K$.
אך בגלל שגודל הקלט הוא $n=\log K$, סיבוכיות הזמן והמקום היא $2^n$. האלגוריתם הוא פסאודו-פולינומיאלי."""

SOL_4C = r"""**פתרון רשמי** (24B-A עמ' 12): עבור $K=7$ הטבלה $C(1),\ldots,C(7)$:

$C(1)=0,\ C(2)=1,\ C(3)=1,\ C(4)=2,\ C(5)=3,\ C(6)=2,\ C(7)=3$"""

SOL_5 = r"""**פתרון רשמי** (24B-A עמ' 13): לא נכון, הערכים 2 ו-4 התחלפו."""

questions = [
    Q(1, "א", "truefalse", "graph_proofs", r"הגרף $G$ בהכרח גרף קשיר.", SOL_1A, points=10, contextId="c1", verdict=False),
    Q(1, "ב", "truefalse", "graph_proofs",
      r"אם קיים $v\in V$ כך ש-$|E_{BFS(G,v)}|=|E_{DFS(G)}|$ אז $G$ בהכרח גרף קשיר.",
      SOL_1B, points=7, contextId="c1", verdict=False),
    Q(1, "ג", "truefalse", "graph_proofs",
      r"אם לכל $v\in V$ מתקיים $|E_{BFS(G,v)}|=|E_{DFS(G)}|$ אז $G$ בהכרח גרף קשיר.",
      SOL_1C, points=8, contextId="c1", verdict=True),

    Q(2, "א", "computation", "greedy",
      r"האם קיים פתרון אופטימלי יחיד לבעיה? אם כן, נמקו תשובתכם. אם לא, הציגו פתרון נוסף (לא בהכרח חמדן) עבור הדוגמה.",
      SOL_2A, points=5, contextId="c2"),
    Q(2, "ב", "algorithm", "greedy", r"כתבו אלגוריתם (או פסאודו-קוד) לפתרון הבעיה.", SOL_2B, points=10, contextId="c2"),
    Q(2, "ג", "proof", "greedy", r"הוכיחו שהאלגוריתם שפיתחתם מחזיר פתרון אופטימלי.", SOL_2C, points=10, contextId="c2"),

    Q(3, "א", "computation", "huffman",
      r"האם הקוד הבא יכול להיות קוד הופמן עבור שכיחויות כלשהן של האותיות:" "\n"
      r"`00, 01, 10, 110, 111`" "\n"
      r"אם לא - נמקו מדוע. אם כן - תנו דוגמה לשכיחויות מתאימות.",
      SOL_3A, points=15),
    Q(3, "ב", "truefalse", "mst",
      r"נתון גרף לא מכוון, קשיר ומשוקלל $G=(V,E,w)$. תהי $e_1\in E$ הצלע עם משקל מקסימלי מבין משקליהן של כל הצלעות, כלומר:" "\n"
      r"$$\forall e\in(E-\{e_1\}),\ w(e_1)>w(e)$$" "\n"
      r"הוכיחו או הפריכו: לא קיים עץ פורש **מינימלי** של $G$ המכיל את $e_1$.",
      SOL_3B, points=10, verdict=False),

    Q(4, "א", "algorithm", "dp_optimization",
      r"הציגו נוסחה רקורסיבית המחשבת את המספר המינימלי של פעולות הנדרשות כדי להפוך 1 למספר הנתון." "\n"
      r"יש להגדיר (במילים) את הפונקציה הרקורסיבית ולנמק בקצרה את הנכונות של הנוסחה.",
      SOL_4A, points=15, contextId="c4"),
    Q(4, "ב", "computation", "complexity_recurrence",
      r"מה סיבוכיות הזמן וסיבוכיות המקום לאלגוריתם תכנון דינמי למציאת המספר המינימלי של פעולות הנדרשות כדי להפוך 1 למספר הנתון?" "\n"
      r"האם האלגוריתם הוא פולינומיאלי? נמקו תשובתכם (אין צורך לפרט את האלגוריתם עצמו).",
      SOL_4B, points=5, contextId="c4"),
    Q(4, "ג", "computation", "dp_optimization",
      r"תנו דוגמה לריצת האלגוריתם תכנון דינמי עבור $K=7$ (בנו ומלאו טבלה).",
      SOL_4C, points=5, contextId="c4"),

    Q(5, None, "truefalse", "suffix_structures",
      r"**שאלת בונוס (5 נקודות)** - ענו נכון או לא נכון, אין צורך לנמק." "\n"
      r"האם המערך הבא הוא Suffix array עבור המילה `BANANABAN` (האינדקס הראשון הוא 1)?" "\n"
      r"`6 8 2 4 7 1 9 5 3`",
      SOL_5, points=5, verdict=False),
]

exam = {
    "examCode": "24B-A",
    "examLabel": "אלגוריתמים 1 (60172), סמסטר ב' תשפ\"ד, מועד א (24.7.2024)",
    "year": 2024,
    "examDate": "24.7.2024",
    "sourceFile": "24B-A exam with solution pp.1-13",
    "solutionFile": "24B-A official solution (typed in the answer boxes)",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1: BFS ו-DFS בגרף עם |E|=|V|", "text": C1},
        "c2": {"kind": "text", "title": "שאלה 2: תחנות רכבת באלגו-לנד", "text": C2},
        "c4": {"kind": "text", "title": "שאלה 4: מ-1 ל-K בפעולות", "text": C4},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
