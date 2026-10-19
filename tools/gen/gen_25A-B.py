# -*- coding: utf-8 -*-
"""Generator for tools/raw/25A-B.json -- algorithms-1 (70162), semester A 2025, moed B (9.03.2025).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25A-B.py

Source: exam booklet pp.1-14 (cover + bonus on p.1, four questions with answer lines). Cap 115.
No answer source exists, so EVERY item is held as no-key (the orchestrator routes them to the solver).
Items: Q1 a,b,c (5/15/5), Q2 a,b (15/10), Q3 a,b (15/10), Q4 a,b (15/10), bonus a,b,c (5 each; the cover
says 15 points for the three).
Q1: the matrix M is a figure (images/exams/25A-B-Q1-matrix.png, cropped from p.2).

Reference values (not answers, not shipped): tools/verify/25A-B/checks.py computes the T table of Q1a, the
greedy of Q2, inversions of Q3 and a linear almost-match of Q4 against brute force.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25A-B.json"
NOKEY = "no-key: no answer source for this sitting"


def Q(num, part, kind, topic, question, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "hold": NOKEY}
    if part:
        q["part"] = part
    q.update(kw)
    return q


C1 = (r"נתונה מטריצה $M$ מסדר $n\times m$, של אפסים ואחדים. נרצה למצוא את גודלו של ריבוע אפסים גדול ביותר בתוך $M$. "
      r"(ב\"גודל הריבוע\" הכוונה לאורך הצלע שלו.)" "\n"
      r"**דוגמה:** עבור המטריצה $M$ הבאה, מסדר $5\times 6$ (התשובה היא 3, ריבוע האפסים עם צלע באורך 3 מודגש במסגרת עבה בתוך המטריצה):" "\n"
      r"נרצה לכתוב נוסחה רקורסיבית $T(i,j)$ המייצגת את גודלו של ריבוע אפסים גדול ביותר ב-$M$ **אשר הפינה הימנית התחתונה שלו היא בשורה $i$ עמודה $j$**. "
      r"בהמשך לדוגמה האחרונה, $T(4,4)=3$." "\n"
      r"המטרה היא לבנות מטריצה $T$ על פי הנוסחה, בתהליך של תכנון דינמי, כך שלאחר שנחשב את $T(i,j)$ לכל $1\le i\le n$, $1\le j\le m$, "
      r"התשובה תתקבל על ידי $\max_{1\le i\le n,\,1\le j\le m}(T(i,j))$.")

C2 = (r"בהינתן מחרוזת $S$ של אותיות קטנות באנגלית, נגדיר את הערך של מחרוזת כסכום הריבועים של תדירות כל תו ייחודי במחרוזת." "\n"
      r"לדוגמה: נתונה המחרוזת $S=$`character`. התדירות של האותיות במחרוזת $S$ היא: `a`=2, `c`=2, `e`=1, `h`=1, `r`=2, `t`=1, "
      r"ולכן הערך של המחרוזת $S$ הוא: $2^2+2^2+1^2+1^2+2^2+1^2=15$." "\n"
      r"להלן בעיית צמצום ערך מחרוזת תלוי $k$:" "\n"
      r"**קלט:** מחרוזת $S$ של אותיות קטנות באנגלית באורך $n$ ומספר טבעי $k$ (הקטן מאורך המחרוזת $S$)." "\n"
      r"**פלט:** מחרוזת $S'$ עם ערך מחרוזת מינימלי, המתקבלת מהמחרוזת $S$ לאחר הורדה של $k$ אותיות." "\n"
      r"בהמשך לדוגמה האחרונה, עבור הקלט $S=$`character` והקבוע 2, פלט אפשרי: $S'=$`charter`.")

C3 = (r"**הגדרה:** בהינתן מערך $A$ של מספרים שלמים בגודל $n$, נאמר שבמערך $A$ קיים היפוך אם קיימים שני איברים במערך $A$, "
      r"באינדקסים $i,j$ כך ש-$i<j$ אך $A[i]>A[j]$. להלן בעיית ההיפוכים במערך." "\n"
      r"**קלט:** מערך $A$ של מספרים שלמים בגודל $n$." "\n"
      r"**פלט:** מספר ההיפוכים במערך $A$." "\n"
      r"**דוגמאות:**" "\n"
      r"- אם המערך כבר ממוין בסדר עולה, מספר ההיפוכים יהיה 0." "\n"
      r"- אם המערך ממוין בסדר יורד, מספר ההיפוכים יהיה מקסימלי." "\n"
      r"- עבור המערך $A=[30,10,40,20]$ מספר ההיפוכים הוא 3. ההיפוכים הם: $(30,10)$ (אינדקסים 1,2), $(30,20)$ (אינדקסים 1,4), $(40,20)$ (אינדקסים 3,4); "
      r"אין היפוך בזוגות $(10,40)$, $(10,20)$ ו-$(30,40)$.")

C4 = (r"**הגדרה:** נאמר ששתי מחרוזות באותו אורך $P_1,P_2$ תואמות \"כמעט בהתאמה\" אם הן זהות או יש לכל היותר תו אחד שבו הן אינן תואמות." "\n"
      r"לדוגמה, המחרוזות הבאות הן \"כמעט בהתאמה\": `aababa`, `aaaaba`" "\n"
      r"להלן בעיית \"כמעט התאמה\":" "\n"
      r"**קלט:** טקסט $T$ באורך $n$ ותבנית $P$ באורך $m$ כאשר $m<n$." "\n"
      r"**פלט:** כל המיקומים $1\le i\le n$ בטקסט $T$ כך שהמחרוזת $P$ והמחרוזת $T[i]T[i+1]\ldots T[i+m-1]$ הן תואמות \"כמעט בהתאמה\".")

C5 = (r"**שאלת בונוס - 15 נקודות** (יש להקיף את התשובה הנכונה): יהי $G$ גרף לא מכוון, קבע לכל אחת מהטענות אם היא נכונה או לא נכונה.")

questions = [
    Q(1, "א", "computation", "dp_optimization",
      r"מלאו את ערכי המטריצה $T$ כפי שיתקבלו עבור המטריצה $M$ הנתונה בדוגמה בראש השאלה (מטריצה ריקה בגודל $5\times 6$, שורות ועמודות 0-4 ו-0-5)." "\n"
      r"שימו לב! אין צורך לכתוב את הנוסחה עדיין, אלא רק להבין מה הנוסחה מבטאת (על פי הכתוב לעיל בפונט מודגש).",
      points=5, contextId="c1"),
    Q(1, "ב", "algorithm", "dp_optimization",
      r"כתבו נוסחה רקורסיבית עבור $T(i,j)$. שימו לב לציין גם את מקרי הבסיס של הנוסחה. "
      r"(כדאי לוודא שהנוסחה שכתבתם מתאימה לערכים שמילאתם בסעיף א'.)",
      points=15, contextId="c1"),
    Q(1, "ג", "computation", "dp_optimization",
      r"מהי סיבוכיות זמן הריצה של אלגוריתם תכנון דינמי המבוסס על הנוסחה שכתבתם בסעיף ב', ומהי סיבוכיות המקום שלו?" "\n"
      r"אין צורך לפרט את האלגוריתם עצמו.",
      points=5, contextId="c1"),

    Q(2, "א", "algorithm", "greedy",
      r"כתוב אלגוריתם חמדני לפתרון הבעיה בזמן $O(n+k\cdot\log k)$." "\n" r"**רמז:** העזר במבנה נתונים.",
      points=15, contextId="c2"),
    Q(2, "ב", "proof", "greedy", r"הוכח את נכונות הפתרון שהצגת בסעיף א'.", points=10, contextId="c2"),

    Q(3, "א", "algorithm", "divide_conquer", r"הציעו אלגוריתם הפרד ומשול יעיל ככל הניתן לפתרון הבעיה.", points=15, contextId="c3"),
    Q(3, "ב", "computation", "complexity_recurrence", r"מה סיבוכיות זמן הריצה של האלגוריתם שהצעתם? נמקו תשובתכם.", points=10, contextId="c3"),

    Q(4, "א", "algorithm", "kmp_strings",
      r"הציעו אלגוריתם לינארי לפתרון הבעיה ללא שימוש בעצי סיפות או מערכי סיפות.", points=15, contextId="c4"),
    Q(4, "ב", "computation", "kmp_strings",
      r"הסבירו מדוע זמן הריצה לינארי בגודל הקלט? מה סיבוכיות המקום של האלגוריתם שהצעתם?", points=10, contextId="c4"),

    Q(5, "א", "truefalse", "graphs_search",
      r"לא ניתן לקבוע בזמן פולינומי האם הגרף $G$ הוא דו צדדי או לא." "\n" r"נכון / לא נכון", points=5, contextId="c5"),
    Q(5, "ב", "truefalse", "graphs_search",
      r"נניח כי הגרף $G$ מיוצג על ידי רשימת סמיכויות, אזי בהינתן קודקוד מהגרף, ניתן בזמן קבוע למצוא את כמות שכניו." "\n" r"נכון / לא נכון",
      points=5, contextId="c5"),
    Q(5, "ג", "truefalse", "graphs_search",
      r"ניתן לאפיין האם הגרף $G$ קשיר על ידי אלג' BFS." "\n" r"נכון / לא נכון", points=5, contextId="c5"),
]

exam = {
    "examCode": "25A-B",
    "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ה, מועד ב (9.03.2025)",
    "year": 2025,
    "examDate": "9.03.2025",
    "sourceFile": "25A-B exam pp.1-14",
    "solutionFile": "none (no answer source)",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1: ריבוע אפסים גדול ביותר", "image": "images/exams/25A-B-Q1-matrix.png",
               "caption": C1},
        "c2": {"kind": "text", "title": "שאלה 2: צמצום ערך מחרוזת", "text": C2},
        "c3": {"kind": "text", "title": "שאלה 3: היפוכים במערך", "text": C3},
        "c4": {"kind": "text", "title": "שאלה 4: כמעט התאמה", "text": C4},
        "c5": {"kind": "text", "title": "שאלת בונוס: גרפים", "text": C5},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
