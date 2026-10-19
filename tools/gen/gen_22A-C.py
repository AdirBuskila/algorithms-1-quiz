# -*- coding: utf-8 -*-
"""Generator for tools/raw/22A-C.json -- algorithms-1 (60072), semester A 5782 (2022), special moed (10.4.2022).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_22A-C.py

Source: a graded student answer booklet (33 pp scan, score 100). It is NOT an official source: answers are labelled
student-solution, official False. PRIVACY: text only, no crops of any page (the pages carry a student id and handwriting);
no id, name or grader mark is copied. The questions are printed text on the booklet pages; the answers are handwritten
and were read as far as they are legible.
Items: Q1; Q2; Q3 a (b held); Q4 held; Q5 (bonus) held.

Transcription notes
- Q2's header says "3 סעיפים" but one request is printed.
- Q3b: the student's proof was marked "not proven" by the grader (-10) -> no key, HELD.
- Q4: the student's pseudocode (select at n/2 and 2n/3 and count) tests the counts with equality (== n/3) where the
  statement says "at least"; see checks. HELD so the solver writes a sound solution.
- Q5 (bonus, 15 pts): a table of E' and C per iteration for a graph; the student's table is incomplete and was scored 3/15,
  and the graph figure would need a crop of the student's page (not allowed). HELD (no-key).
- Q1: the grader's marks show -3 on the base case of the student's formula; the recurrence below is the standard
  one (F(0)=0, F(i)=1+min over 1<=j<=sqrt(i) of F(i-j^2)), which the paper's second line matches.

Checks (tools/verify/22A-C/checks.py): Q1 recurrence vs BFS (N<=60); Q2 pi(S$S^R) last value vs brute force
(3000 random strings; aabaac -> 5); Q3a sort + pair neighbours vs all pairings (1500 random); Q4 shows the '==' flaw.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "22A-C.json"


def Q(num, part, kind, topic, question, solution, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution,
         "solutionSource": "student-solution", "official": False, "confidence": "med"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


Q1 = (r"כל מספר טבעי $N$ ניתן לייצוג כסכום של מספרים שהם ריבועים. למשל:" "\n"
      r"$1+\ldots+1+1=9+1+1+1=4+4+4=12$" "\n"
      r"הטענה נכונה לכל $N$ כי $1$ הוא ריבוע ותמיד ניתן לייצג את $N$ כסכום של $N$ אחדות." "\n"
      r"**בעיית הסכום הריבועי המינימלי:**" "\n"
      r"**קלט:** מספר $N$" "\n"
      r"**פלט:** ייצוג של $N$ כסכום של מספר מינימלי של ריבועים." "\n"
      r"הבעיה ניתנת לפתרון בעזרת תכנון דינמי." "\n"
      r"הציגו נוסחה רקורסיבית המחשבת את המספר המינימלי של ריבועים שסכומם הוא $N$. יש לפרט לכל פרמטר בנוסחה את תפקידו "
      r"וכן להסביר את הפלט ונכונות הנוסחה (אין צורך בהוכחה פורמלית).")

S1 = r"""$$F(i)=\begin{cases}0 & ;\ i=0\\ \displaystyle\min_{1\le j\le\sqrt{i}}\bigl(F(i-j^2)\bigr)+1 & ;\ \text{else}\end{cases}$$
$i$ הוא המספר שיש לייצג כסכום ריבועים, ו-$j$ הוא שורש הריבוע האחרון בסכום ($1\le j\le\sqrt{i}$); $F(i)$ הוא מספר הריבועים המינימלי שסכומם $i$. הפלט הוא $F(N)$."""

Q2 = (r"תהי $S=s_1s_2\ldots s_n$ מחרוזת. נסמן ב-$S^R$ את המחרוזת ההופכת של $S$, ז\"א $S^R=s_ns_{n-1}\ldots s_1$. לדוגמא, אם "
      r"$S=aabc$ אז $S^R=cbaa$. נאמר שמחרוזת $S$ היא פולינדרום אם $S^R=S$." "\n"
      r"להלן, בעיית הרישא הפולינדרומית:" "\n"
      r"**קלט:** מחרוזת $S$ באורך של $n$ תווים." "\n"
      r"**פלט:** אורך הרישא המקסימלית של $S$ שהינה פולינדרום." "\n"
      r"לדוגמא: עבור הקלט: $aabaac$, יוחזר הערך: $5$." "\n"
      r"הציעו האלגוריתם היעיל ביותר המקבל מחרוזת $S$ באורך $n$ ומחזיר את אורך הרישא הפולינדרומית. יש לציין את סיבוכיות זמן "
      r"הריצה של האלגוריתם שהצעתם (אין צורך בהוכחה).")

S2 = r"""- נגדיר את $S^R$ ונבנה את המחרוזת `S#SR` (מחרוזת $S$, אחריה תו מפריד `#` שאינו מופיע ב-$S$, ואחריו $S^R$).
- נריץ את פונקציית הרישא (prefix function) של KMP על המחרוזת `S#SR`.
- הערך האחרון בטבלה הוא אורך הרישא המקסימלית של $S$ שהיא פולינדרום.

סיבוכיות זמן הריצה: $O(n)$ (המחרוזת באורך $2n+1$, ולכן $\Theta(n)$)."""

Q3 = (r"לרגל חג הפסח המתקרב, רשת המרכולים \"רק אצלנו\" יצאה במבצע לחג. הרשת הכריזה שמי שקונה זוג מוצרים מקבל את הזול "
      r"מביניהם בחינם. לרותי רשימה של $2n$ מוצרים שברצונה לקנות, במחירים (רשימת המחירים לאו דווקא ממוינת): "
      r"$p_1,p_2,\ldots,p_{2n}$." "\n"
      r"רותי מתכננת לבצע $n$ רכישות, בכל רכישה תקנה $2$ מוצרים.")

S3A = r"""- נמיין את רשימת המחירים מהקטן לגדול.
- נחלק את המוצרים לזוגות לפי הסדר הממוין: המוצר הראשון עם השני, השלישי עם הרביעי וכן הלאה; בכל זוג המוצר הזול בחינם ומשלמים על היקר.
- נחזיר את הסכום."""

Q4 = (r"נתון מערך $A$ עם $n$ מספרים טבעיים." "\n"
      r"הציעו אלגוריתם לינארי המקבל כקלט את המערך $A$ ומחזיר שני ערכים מהמערך $k,m$ כך ששלושת התנאים הבאים מתקיימים:" "\n"
      r"I. $k<m$" "\n"
      r"II. $k$ מופיע במערך לפחות $n/2$ פעמים." "\n"
      r"III. $m$ מופיע במערך לפחות $n/3$ פעמים")

Q5 = (r"**שאלת בונוס (15 נקודות).**" "\n"
      r"נתון הגרף הבא, כתבו את ערכי קבוצת הכיסוי $C$ וערכי הקבוצה $E'$ בכל איטרציה בהרצת האלגוריתם למציאת קירוב לכיסוי "
      r"קודקודים שלמדנו במסגרת הקורס.")

questions = [
    Q(1, None, "algorithm", "dp_sequences", Q1, S1, points=25),
    Q(2, None, "algorithm", "kmp_strings", Q2, S2, points=25),
    Q(3, "א", "algorithm", "greedy",
      r"הציעו אלגוריתם חמדני המחלק את המוצרים ל-$n$ זוגות, כך שהסכום הכולל שנשלם עבורם יהיה מינימלי.", S3A, contextId="c3"),
    {"num": 3, "part": "ב", "kind": "proof", "topic": "greedy", "contextId": "c3",
     "question": r"הוכיחו שהאלגוריתם שהצעת מקיים את תכונת הבחירה החמדנית.",
     "hold": "no-key: the student's proof of the greedy-choice property was marked 'not proven' (-10)"},
    {"num": 4, "kind": "algorithm", "topic": "divide_conquer", "question": Q4, "points": 25,
     "hold": "no-key: the student's algorithm tests the counts with '==' instead of 'at least' (see tools/verify/22A-C/checks.py); a sound solution is needed"},
    {"num": 5, "kind": "computation", "topic": "approximation", "question": Q5, "points": 15,
     "hold": "no-key: the student's iteration table is incomplete (scored 3/15) and the figure cannot be cropped from the student's page"},
]

exam = {
    "examCode": "22A-C",
    "examLabel": "אלגוריתמים 1 (60072), סמסטר א' תשפ\"ב, מועד מיוחד (10.4.2022)",
    "year": 2022,
    "examDate": "10.4.2022",
    "sourceFile": "22A-C exam booklet (graded student scan)",
    "solutionFile": "student-solution-1",
    "contexts": {
        "c3": {"kind": "text", "title": "שאלה 3: חג הפסח והמבצע", "text": Q3},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
