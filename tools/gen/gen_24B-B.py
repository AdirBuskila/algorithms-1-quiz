# -*- coding: utf-8 -*-
"""Generator for tools/raw/24B-B.json -- algorithms-1 (60172), semester B 2024, second sitting (14.8.2024).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24B-B.py

Source: exam booklet pp.1-17 (cover says "מועד א" with the date 14.8.24; GATE1 treats it as 24B-B).
4 questions x 25 + a 5-point bonus, cap 105.
No answer source exists, so EVERY item is held as no-key (the orchestrator routes them to the solver).
Items: Q1 a,b,c (8/9/8), Q2 a,b (15/10), Q3 a,b,c (15/5/5), Q4 a,b,c (5/10/10), bonus (5).
- Q2b: the question text is missing from the booklet (p.6 shows only a stray "A. ..." line and the empty answer
  box "פתרון סעיף ב'"); held with that reason, points 10 inferred from 25 - 15.
- Bonus: the figure (suffix tree, cropped from p.14) belongs to a text T that is not printed; the garbled root-to-leaf-0
  label reads RATATAT. Graph data: tools/verify/24B-B/graphs.json.
Reference values (not answers): tools/verify/24B-B/checks.py (Q2a candidate frequencies, Q4 example, bonus).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24B-B.json"
NOKEY = "no-key: no answer source for this sitting"


def Q(num, part, kind, topic, question, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "hold": NOKEY}
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

questions = [
    Q(1, "א", "truefalse", "graph_proofs",
      r"אם $E_{DFS}=E_{BFS}$, אזי $s$ הוא שורש (צומת שממנו יש מסלול לכל צומת בגרף).", points=8, contextId="c1"),
    Q(1, "ב", "truefalse", "graph_proofs",
      r"אם $E_{DFS}=E_{BFS}$ וגם דרגת כניסה $deg^-(x)\neq 0$ וגם דרגת יציאה $deg^+(x)\neq 0$ שונות מ-0 לכל צומת $x\in V$, אזי $s$ הוא שורש.",
      points=9, contextId="c1"),
    Q(1, "ג", "truefalse", "graph_proofs",
      r"אם $E_{DFS}=E_{BFS}$ וגם סכום דרגות כניסה וגם יציאה $deg^+(x)+deg^-(x)\neq 0$ שונות מ-0 לכל צומת $x\in V$, אזי $s$ הוא שורש.",
      points=8, contextId="c1"),

    Q(2, "א", "computation", "huffman",
      r"עבור מחרוזת $S$ מעל א\"ב $\Sigma=\{a,b,c,d,e\}$ נתון כי:" "\n"
      r"- האות $a$ מופיעה 7 פעמים, האות $b$ מופיעה 4 פעמים והאות $e$ מופיעה 7 פעמים." "\n"
      r"- קוד הופמן של האותיות הוא: $a$ - `10`, $b$ - `00`, $c$ - `010`, $d$ - `011`, $e$ - `11`." "\n"
      r"- מספר ההופעות של \"אח\" השמאלי הוא לא יותר גדול ממספר ההופעות של \"אח\" הימני." "\n"
      r"הניחו שסיבית הקוד לצומת הימני היא 1 ולשמאלי 0." "\n"
      r"רשמו את כל האופציות האפשריות לשכיחויות של אותיות $c$ ו-$d$ במחרוזת $S$. נמקו את תשובתכם.",
      points=15),
    {"num": 2, "part": "ב", "kind": "algorithm", "points": 10,
     "hold": "no-key: the question text of Q2b is missing from the booklet (p.6 shows only a stray 'A. ...' line and the empty answer box); no answer source either"},

    Q(3, "א", "algorithm", "dp_optimization",
      r"הציגו נוסחה רקורסיבית לחישוב הרווח הכולל המקסימלי. יש להגדיר (במילים) את הפונקציה הרקורסיבית ולנמק בקצרה את הנכונות של הנוסחה.",
      points=15, contextId="c3"),
    Q(3, "ב", "computation", "complexity_recurrence",
      r"מה סיבוכיות הזמן וסיבוכיות המקום לאלגוריתם תכנון דינמי למציאת הרווח הכולל המקסימלי? נמקו תשובתכם (אין צורך לפרט את האלגוריתם עצמו).",
      points=5, contextId="c3"),
    Q(3, "ג", "computation", "complexity_recurrence",
      r"מה סיבוכיות הזמן וסיבוכיות המקום של אלגוריתם תכנון דינמי המחזיר את הפתרון עצמו - המקומות למסעדות? נמקו את תשובתכם (אין צורך לפרט את האלגוריתם עצמו).",
      points=5, contextId="c3"),

    Q(4, "א", "computation", "greedy",
      r"האם קיים פתרון אופטימלי יחיד לבעיה? אם כן, נמקו תשובתכם. אם לא, הציגו פתרון נוסף (לא בהכרח חמדן) עבור הדוגמה.",
      points=5, contextId="c4"),
    Q(4, "ב", "algorithm", "greedy", r"כתבו אלגוריתם (או פסודו-קוד) לפתרון הבעיה.", points=10, contextId="c4"),
    Q(4, "ג", "proof", "greedy", r"הוכיחו שהאלגוריתם שפיתחתם מחזיר פתרון אופטימלי.", points=10, contextId="c4"),

    Q(5, None, "truefalse", "suffix_structures",
      r"**שאלת בונוס (5 נקודות)** - ענו, אין צורך לנמק." "\n"
      r"נתון suffix tree עבור מחרוזת $T$." "\n"
      r"מהי תת-המחרוזת (רצף אותיות) החוזרת (שמופיעה לפחות פעמיים ב-$T$) הארוכה ביותר? (אין צורך לנמק)",
      points=5, image="images/exams/24B-B-Q5-suffix-tree.png"),
]

exam = {
    "examCode": "24B-B",
    "examLabel": "אלגוריתמים 1 (60172), סמסטר ב' תשפ\"ד, מועד ב (14.8.2024)",
    "year": 2024,
    "examDate": "14.8.2024",
    "sourceFile": "24B-B exam pp.1-17 (cover says moed A, dated 14.8.24)",
    "solutionFile": "none (no answer source)",
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
