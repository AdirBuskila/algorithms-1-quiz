# -*- coding: utf-8 -*-
"""Generator for tools/raw/23A-A.json -- algorithms-1 (60072), semester A 2023, moed A (25.1.2023).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_23A-A.py

Source: exam booklet pp.1-15 (cover, 4 questions + bonus, answer boxes, scratch pages). NO answer source exists
for this sitting (no solution file in either tree), so every item is held with reason "no-key"; the question
text is transcribed in full so the solver can work from the bank.
Items: Q1 a,b,c (15/5/5), Q2 a,b (10/15), Q3 a,b,c (4/8/13), Q4 a,b (15/10), bonus Q5 (15, num 5). Cap 115.

Transcription notes
- The printed headers say "Q2: 3 parts", "Q3: 4 parts", "Q4: 4 parts", but the booklet contains 2, 3 and 2 parts
  (sub-points 10+15, 4+8+13, 15+10 = 25 each). Transcribed as printed; nothing is missing from the page images.
- Q3b is a table whose probability column is left blank for the student; transcribed as four labelled rows.
- Q5 prints the approximation ratio as theta(log n); kept as printed.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "23A-A.json"


def H(num, part, kind, topic, question, points, **kw):
    """Held item: question text only, no answer source."""
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "points": points, "hold": "no-key"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


# ---------------------------------------------------------------- contexts
C1 = (r"נתון מערך $A$ דו ממדי של מספרים שלמים כך שהמשולש העליון (מימין לאלכסון הראשי) מכיל אפסים בלבד." "\n"
      r"לדוגמא:" "\n"
      r"$$A:\quad\begin{array}{|c|c|c|}\hline 1 & 0 & 0\\\hline 3 & 2 & 0\\\hline 4 & 10 & 12\\\hline\end{array}$$" "\n"
      r"מסלול על המערך $A$ מתחיל במיקום $[1,1]$ ומסתיים באחד המיקומים בשורה התחתונה. צעד במסלול ממשבצת $[i,j]$ יכולה "
      r"להיות ל-$[i+1,j]$ או $[i+1,j+1]$. **ערך מסלול**, הוא סכום הערכים הנמצאים על המסלול." "\n"
      r"המטרה, מציאת המסלול שערכו גדול ביותר." "\n"
      r"לדוגמא, בהמשך לדוגמת המערך $A$, הפתרון הוא המסלול: $1\to2\to12$." "\n"
      r"הבעיה ניתנת לפתרון בעזרת תכנון דינמי.")

C2 = (r"להלן תיאור בעיית תת המחרוזת הארוכה ביותר של שתי מחרוזות נתונות." "\n"
      r"קלט: שני מחרוזות $S_1,S_2$ כל אחת מהן באורך $n$" "\n"
      r"פלט: תת המחרוזת הארוכה ביותר המשותפת למחרוזות $S_1,S_2$." "\n"
      r"לדוגמא: בהינתן המחרוזות: $S_1=\mathrm{BADAEAT}$, $S_2=\mathrm{CAEADAS}$ אזי $\mathrm{ADA}$ היא תת מחרוזת משותפת ארוכה "
      r"ביותר של המחרוזות $S_1,S_2$.")

C3 = r"לרשותך מטבע אשר נופל על \"עץ\" בהסתברות $0<p<1$ (לא ידועה)."

C4 = (r"נתון שק שיכול לשאת משקל $W$ שלם של ק\"ג (למשל $W=35$ ק\"ג)." "\n"
      r"כמו כן נתונים פריטים מ-$K$ סוגים שונים כך שכל פריט משקלו $P_i$ $(1\le i\le K)$. כמות הפריטים מכל סוג לא מוגבלת." "\n"
      r"נתון שאוסף המשקלים מקיים:" "\n"
      r"(1) $P_i=5P_{i+1}$ $(1\le i\le K-1)$" "\n"
      r"(2) $P_K=1$")

C5 = (r"להלן תיאור בעיית כיסוי קבוצות:" "\n"
      r"קלט: אוסף של $m$ קבוצות $\mathcal{S}=\{A_1,A_2,\cdots,A_m\}$ והקבוצה האוניברסלית: "
      r"$\mathbb{U}=\bigcup_{A\in\mathcal{S}}A$" "\n"
      r"פלט: תת קבוצה $\mathcal{T}\subseteq\mathcal{S}$ בגודל מינימלי המקיימת $\bigcup_{A\in\mathcal{T}}A=\mathbb{U}$")

questions = [
    H(1, "א", "algorithm", "dp_optimization",
      r"**(15 נקודות) הציגו** נוסחה רקורסיבית המוצאת את ערכו של המסלול היקר ביותר (ז\"א שסכומו מקסימלי). יש לפרט לכל "
      r"פרמטר בנוסחה את תפקידו וכן להסביר את הפלט ונכונות הנוסחה (אין צורך בהוכחה פורמלית).",
      15, contextId="c1"),
    H(1, "ב", "computation", "dp_optimization",
      r"(5 נקודות) קבעו את סיבוכיות הזמן והמקום של אלגוריתם תכנון דינמי הפותר את הבעיה, ז\"א **מוצא את המסלול שערכו "
      r"מקסימלי**. נמקו תשובתכם. אין צורך לפרט את האלגוריתם עצמו.",
      5, contextId="c1"),
    H(1, "ג", "computation", "dp_optimization",
      r"(5 נקודות) קבעו את סיבוכיות הזמן והמקום של אלגוריתם תכנון דינמי המוצא את **ערך המסלול הגדול ביותר**. נמקו "
      r"תשובתך. אין צורך לפרט את האלגוריתם עצמו.",
      5, contextId="c1"),

    H(2, "א", "proof", "suffix_structures",
      r"(10 נקודות) בהינתן שהמחרוזות $S_1,S_2$ מעל א\"ב $\Sigma=\{A,B,C,D,E\}$, הסבירו מדוע ניתן לבנות עץ סיפות לאוסף "
      r"הסיפות של המחרוזות $S_1\text{\textdollar},S_2{*}$ (שימו לב, כי למחרוזת $S_1$ שורשר בסופה התו $\text{\textdollar}$, ולמחרוזת $S_2$ שורשר התו "
      r"${*}$, כאשר שני התווים $\text{\textdollar},{*}$ אינם תווים בא\"ב $\Sigma$) בזמן $O(n)$ שתומך גם בתכונות הבאות:" "\n"
      r"- אורך תת המחרוזת המתאימה למסלול משורש העץ ועד קדקוד זה." "\n"
      r"- בכל קדקוד בעץ מצוין אם עלי תתי העץ המושרש בקדקוד זה יש סיפות השייכות רק למחרוזת $S_1\text{\textdollar}$ או רק למחרוזת "
      r"$S_2{*}$ או לשתי המחרוזות $S_1\text{\textdollar},S_2{*}$.",
      10, contextId="c2"),
    H(2, "ב", "algorithm", "suffix_structures",
      r"(15 נקודות) תארו אלגוריתם לינארי לפתרון בעיית תת המחרוזת הארוכה ביותר עם מחרוזות מעל א\"ב בגודל $5$.",
      15, contextId="c2"),

    H(3, "א", "computation", "randomized",
      r"(4 נקודות) הגדירו מהו אלגוריתם הסתברותי מסוג מונטה קרלו ומהו אלגוריתם הסתברותי מסוג לאס וגאס.",
      4, contextId="c3"),
    H(3, "ב", "computation", "randomized",
      r"(8 נקודות) השלימו את הטבלה הבאה (עמודות: ההטלה, ההסתברות להטלה):" "\n"
      r"- הטלה הראשונה פלי ובשנייה עץ" "\n"
      r"- ההטלה הראשונה עץ ובשנייה פלי" "\n"
      r"- בשני ההטלות יצא עץ" "\n"
      r"- בשני ההטלות יצא פלי",
      8, contextId="c3"),
    H(3, "ג", "algorithm", "randomized",
      r"(13 נקודות) הציעו אלגוריתם מסוג לאס וגאס אשר עושה שימוש במטבע ליצירת הגרלה בהסתברות $\frac{1}{2}:\frac{1}{2}$ "
      r"(רמז: התבוננו בזוג הטלות).",
      13, contextId="c3"),

    H(4, "א", "algorithm", "greedy",
      r"(15 נקודות) מצאו אלגוריתם חמדני שממלא את כל השק עם מספר מינימלי של פריטים.",
      15, contextId="c4"),
    H(4, "ב", "proof", "greedy",
      r"(10 נקודות) הסבירו את נכונות האלגוריתם שפיתחתם (ז\"א, הראו שמתקיימת תכונת הבחירה החמדנית וכן מתקיימת תכונת "
      r"תת מבנה אופטימלי).",
      10, contextId="c4"),

    H(5, "", "algorithm", "approximation",
      r"**שאלה 5 (15 נקודות) - שאלת בונוס**" "\n"
      r"הציגו אלגוריתם קירוב לבעיית כיסויי הקבוצות בקירוב של $\theta(\log n)$ (כתיבת האלגוריתם בפסודו קוד מחייבת "
      r"כתיבת הערות לקוד).",
      15, contextId="c5"),
]

exam = {
    "examCode": "23A-A",
    "examLabel": "אלגוריתמים 1 (60072), סמסטר א' תשפ\"ג, מועד א (25.1.2023)",
    "year": 2023,
    "examDate": "25.1.2023",
    "sourceFile": "23A-A exam pp.1-15",
    "solutionFile": "none (no answer source)",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1: מסלול יקר במערך משולש", "text": C1},
        "c2": {"kind": "text", "title": "שאלה 2: תת המחרוזת המשותפת הארוכה ביותר", "text": C2},
        "c3": {"kind": "text", "title": "שאלה 3: מטבע עם הסתברות לא ידועה", "text": C3},
        "c4": {"kind": "text", "title": "שאלה 4: מילוי שק", "text": C4},
        "c5": {"kind": "text", "title": "שאלה 5: כיסוי קבוצות", "text": C5},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions (all held: no-key)")
