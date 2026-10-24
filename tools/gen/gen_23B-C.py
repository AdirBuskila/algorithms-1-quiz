# -*- coding: utf-8 -*-
"""Generator for tools/raw/23B-C.json -- algorithms-1 (60172), semester B 2023, special sitting (24.08.23).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_23B-C.py

Source: the blank exam booklet (scan, 30 pages: cover, answer boxes, a page of allowed black-box algorithms, 4 draft pages).
There is NO answer source for this sitting (no solution file, no student paper): every question is held with reason no-key
and routed to the solver by the orchestrator. The question texts are transcribed so the solver can start.
Cover: 2.5 h, closed material except the last-page list of black-box algorithms, 4 questions (all compulsory),
cap 110, "unanswered = 20% of the points".
Items: Q1 a,b (30 points together, the split is not printed), Q2 a,b (25/15), Q3 a,b,c (30 together, split not printed), Q4 (10).

Transcription notes
- Q1a: the printed sequence is "0, 1, 2, 3, 1" (as rendered on the page, left to right).
- Q2b: positions are 1-based in the printed example (K=5 keeps the 15).
- Q3 cost matrix: rows are houses 1-3, columns R, B, G: (14,2,11), (11,14,5), (14,3,19).

Info for the solver (not shipped, no key given): see tools/verify/23B-C/ is intentionally absent; nothing was checked here.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "23B-C.json"
R = "no-key: blank booklet, no solution source for this sitting"


def H(num, part, kind, topic, question, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "hold": R}
    if part:
        q["part"] = part
    q.update(kw)
    return q


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
      r"אם לא - נמקו מדוע, אם כן - תנו דוגמא למחרוזת $P$."),
    H(1, "ב", "computation", "suffix_structures",
      r"בנו Suffix tree ו-Suffix array עבור המחרוזת `algogoal`"),

    H(2, "א", "algorithm", "dp_optimization",
      r"(25 נקודות) נתון מערך עם מספרים שלמים. נתייחס למערך כאילו הוא מעגלי, ז\"א אחרי איבר האחרון בא איבר הראשון." "\n"
      r"מצאו רצף מספרים במערך מעגלי, אשר נותן סכום מקסימלי." "\n"
      r"לדוגמה: עבור מערך: $4,-6,5,-6,10,-5,3$ עליכם להחזיר: $12=10-5+3+4$" "\n"
      r"רמז: אפשר להיעזר באלגוריתם Kadane שמחזיר רצף עם סכום מקסימלי במערך (לא מעגלי)." "\n"
      r"נמקו נכונות האלגוריתם שכתבתם. מהי הסיבוכיות של האלגוריתם? נמקו את תשובתכם.",
      points=25, contextId="cbb"),
    H(2, "ב", "algorithm", "divide_conquer",
      r"(15 נקודות) נתון מערך $A$ עם מספרים שלמים ואנדקס $K$." "\n"
      r"יש למיין את המערך המקורי $A$, מלבד האיבר במקום ה-$K$ שאינו משנה את מיקומו." "\n"
      r"לדוגמה: עבור מערך $A$: $4,10,-6,3,15,-8,7$ ו-$K=5$ האלגוריתם מחזיר $-8,-6,3,4,15,7,10$" "\n"
      r"בנו אלגוריתם יעיל ונתחו את הסיבוכיות שלו.",
      points=15, contextId="cbb"),

    H(3, "א", "algorithm", "dp_optimization",
      r"בעיית תכנון הצביעה ניתנת לפתרון בעזרת **תכנון דינמי**." "\n"
      r"הציגו נוסחה רקורסיבית המחשבת את **העלות** המינימלית." "\n"
      r"יש **להגדיר** את הפונקציה הרקורסיבית **ולנמק** נכונות של הנוסחה." "\n"
      r"רמז: תגדירו $3$ פונקציות רקורסיביות בהתאם לשלוש אופציות לצביעה של הבית האחרון.",
      contextId="c3"),
    H(3, "ב", "computation", "dp_optimization",
      r"תנו דוגמא לעבודת האלגוריתם שפותר את הבעיה בשיטה תכנון דינאמי על בסיס נוסחה רקורסיבית מסעיף הקודם עבור מטריצה $\mathrm{cost}$ הבאה ($n=3$):" "\n"
      r"בית $1$: אדום $14$, כחול $2$, ירוק $11$" "\n"
      r"בית $2$: אדום $11$, כחול $14$, ירוק $5$" "\n"
      r"בית $3$: אדום $14$, כחול $3$, ירוק $19$" "\n"
      r"(בתשובה יש למלא טבלה עם עמודות הבתים $1,2,3$ ושורות הצבעים $R,B,G$.)",
      contextId="c3"),
    H(3, "ג", "computation", "complexity_recurrence",
      r"מה סיבוכיות האלגוריתם שפותר את הבעיה בשיטה תכנון דינמי על בסיס נוסחה רקורסיבית מסעיף א? נמקו בקצרה.",
      contextId="c3"),

    H(4, "", "computation", "huffman",
      r"עבור מחרוזת $S$ מעל א\"ב $\Sigma=\{a,b,c,d,e\}$ נתון כי:" "\n"
      r"- האות $a$ מופיעה $10$ פעמים, האות $b$ מופיעה $7$ פעמים והאות $e$ מופיעה $10$ פעמים." "\n"
      r"- קוד הופמן של האותיות הוא: $a-10,\ b-00,\ c-010,\ d-011,\ e-11$" "\n"
      r"- מספר ההופעות של \"אח\" השמאלי הוא **לא** יותר גדול ממספר הופעות של \"אח\" הימני." "\n"
      r"הניחו שסיבית הקוד לצומת הימני היא $1$ ולשמאלי $0$." "\n"
      r"רשמו את **כל** האופציות האפשריות לשכיחויות של אותיות $c$ ו-$d$ במחרוזת $S$. נמקו את תשובתכם.",
      points=10),
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
