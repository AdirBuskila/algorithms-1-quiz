# -*- coding: utf-8 -*-
"""Generator for tools/raw/26A-B.json -- algorithms-1 (70162), semester A 2026, moed B (05/03/2026).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_26A-B.py

Source: exam booklet, 18 pages (cover with formulas p.1, bonus p.2, Q1 pp.3-6, Q2 pp.7-10, Q3 pp.11-14, Q4 pp.15-16,
answer lines only; pp.8, 10, 12, 15, 17, 18 are continuation pages with no text). Cap printed on the cover: 115.
There is NO answer source for this sitting (GATE1: no-key), so every item is held with reason "no-key" and goes to
the solver. The question text is transcribed character-exact from the rendered pages.

Items: Q1 a,b,c (5/15/5), Q2 a,b (12.5/12.5), Q3 a,b,c (5/10/10), Q4 (25), bonus a,b,c (5 each, num 5).
Notes
- The bonus block is printed on p.2, before Q1 (it is the second page of the booklet). Transcribed as num 5 like 26A-A.
- Q2 sub-points are 12.5 each, transcribed as printed.
- Q3's algorithm is the reverse-delete algorithm (remove an edge when the graph stays connected).
Figures: images/exams/26A-B-Q1-route.png (the route diagram, a context figure). No data graph is needed (Q2/Q3 are
abstract claims with no printed graph).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "26A-B.json"
HOLD = "no-key"


def Q(num, part, kind, topic, question, points, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "points": points, "hold": HOLD}
    if part:
        q["part"] = part
    q.update(kw)
    return q


C1 = (r"ברצוננו לערוך מסע לאורך מסלול ישר מנקודת-התחלה $s=0$ לנקודת-סיום $f>0$." "\n"
      r"נתון מערך $p$ של מיקומי-מלונות $0<p_1<\cdots<p_n=f$ קילומטרים, כך שמלון $i$ ממוקם בדיוק $p_i$ קילומטרים "
      r"מנקודת תחילת המסלול." "\n"
      r"להלן סרטוט המסלול עבור $n=6$:" "\n"
      r"![סרטוט המסלול עבור n=6: נקודת ההתחלה s, ששה מלונות ונקודת הסיום f, עם המרחקים p1 עד p6 מהתחלת המסלול]"
      r"(images/exams/26A-B-Q1-route.png)" "\n"
      r"במהלך המסע לנים בכל לילה במלון אחד." "\n"
      r"החופשה מוגבלת בזמן, ולכן חייבים לסיים את המסע תוך לכל היותר $t$ ימים (נתון $t<n$)." "\n"
      r"המאמץ שנדרש ביום-הליכה הינה $d^2$, כאשר $d$ הוא המרחק שהולכים באותו יום." "\n"
      r"עלינו לבחור את נקודות-הלינה, כך שנמזער את סכום המאמצים בכל המסע." "\n"
      r"הערה: הבעיה ניתנת לפתרון בעזרת תכנון דינמי.")

C2 = (r"נתון גרף $G=(V,E)$ עם קודקוד מוצא $s\in V$. נתון כי כל יתר הקודקודים בגרף נגישים מהמוצא, כלומר ניתן להגיע "
      r"מקודקוד המוצא $s$ לכל קודקוד $v\in V$." "\n"
      r"נסמן ב: $T_{BFS},T'_{BFS}$ שני עצי BFS שונים של $G$ המושרשים ב-$s$. בדומה נסמן ב-$T_{DFS},T'_{DFS}$ שני עצי DFS "
      r"שונים של $G$ המושרשים ב-$s$." "\n"
      r"בשני הסעיפים הבאים מובאת טענה שיש להוכיח או להפריך. אם הטענה נכונה אז נדרשת הוכחה מדויקת וקצרה. "
      r"אם הטענה אינה נכונה אז נדרשת דוגמה נגדית.")

C3 = (r"יהי $G=(V,E)$ גרף קשיר עם $|V|=n$." "\n"
      r"לכל צלע משקל חיובי, וכל המשקלים שונים זה מזה." "\n"
      r"נבחן את האלגוריתם הבא:" "\n"
      r"1. מיין את הצלעות לפי סדר משקל יורד." "\n"
      r"2. עבור על הצלעות לפי הסדר הזה. לכל צלע $e$:" "\n"
      r"- הסר את $e$ מן הגרף אם לאחר הסרתה הגרף נשאר קשיר." "\n"
      r"- אחרת, נשאיר אותה." "\n"
      r"3. בסיום נסמן ב-$T$ את קבוצת הצלעות שנותרה.")

BONUS = (r"**שאלת בונוס - (15 נקודות)** יש להקיף את התשובה הנכונה ולציין נימוק קצר. "
         r"אין קשר בין הסעיפים השונים, כל סעיף 5 נקודות." "\n")

questions = [
    Q(1, "א", "computation", "dp_optimization",
      r"(5 נקודות) בהמשך לסרטוט בשאלה, הנח שהמרחק בין כל מלון הוא בדיוק 5 קילומטר, ואנו רוצים לסיים את המסע ב-3 ימים. "
      r"מהו סכום המאמץ אם נבחר כנקודות לינה את $p_2$ ואת $p_4$. נמקו תשובתכם.",
      5, contextId="c1"),
    Q(1, "ב", "algorithm", "dp_optimization",
      r"(15 נקודות) בהינתן נקודת-התחלה $s=0$ ונקודת-סיום $f>0$ ומערך $p$ של מיקומי-מלונות וכן $t$, כמות הימים שניתן "
      r"לכל היותר לטייל:" "\n"
      r"כתבו נוסחה רקורסיבית לחישוב העלות המזערית לסכום המאמצים בכל המסע." "\n"
      r"יש לפרט גם את מקרי הבסיס. יש לפרט את משמעות הנוסחה.",
      15, contextId="c1"),
    Q(1, "ג", "computation", "dp_optimization",
      r"(5 נקודות) מהי סיבוכיות זמן הריצה של אלגוריתם תכנון דינמי המבוסס על הנוסחה שכתבתם בסעיף ב', "
      r"ומהי סיבוכיות המקום שלו?",
      5, contextId="c1"),

    Q(2, "א", "truefalse", "graph_proofs",
      r"(12.5 נקודות) אם $G$ גרף לא מכוון, אז בהכרח לשני עצי ה-BFS יש אותו עומק "
      r"$\operatorname{depth}(T_{BFS})=\operatorname{depth}(T'_{BFS})$." "\n"
      r"(בחרתי ב: הוכחה/הפרכה - יש להקיף את בחירתך.)",
      12.5, contextId="c2"),
    Q(2, "ב", "truefalse", "graph_proofs",
      r"(12.5 נקודות) אם $G$ גרף מכוון, אז בהכרח לשני עצי ה-DFS יש אותו עומק "
      r"$\operatorname{depth}(T_{DFS})=\operatorname{depth}(T'_{DFS})$." "\n"
      r"(בחרתי ב: הוכחה/הפרכה - יש להקיף את בחירתך.)",
      12.5, contextId="c2"),

    Q(3, "א", "proof", "mst",
      r"(5 נקודות) הוכח כי כאשר האלגוריתם נעצר, ב-$T$ יש בדיוק $n-1$ צלעות.",
      5, contextId="c3"),
    Q(3, "ב", "proof", "mst",
      r"(10 נקודות) הוכח כי הגרף המתקבל הוא עץ פורש של $G$.",
      10, contextId="c3"),
    Q(3, "ג", "proof", "mst",
      r"(10 נקודות) הוכח כי $T$ הוא עץ פורש מינימלי (MST).",
      10, contextId="c3"),

    Q(4, None, "algorithm", "divide_conquer",
      r"נתון מערך בגודל $n$." "\n"
      r"רוצים למצוא את האיבר שהוא ה-$k$-י הקטן ביותר כאשר $k<\frac{n}{2}$." "\n"
      r"מותר להשתמש ב-SELECT רק על תתי מערכים בגודל לכל היותר $\frac{n}{2}$:" "\n"
      r"הראו אלגוריתם הרץ בזמן $O(n)$ לפתרון הבעיה המוצגת. נמקו תשובתכם.",
      25),

    Q(5, "א", "truefalse", "kmp_strings",
      BONUS + r"נסתכל על הטבלה של $\pi$ המתקבלת בהרצת אלגוריתם KMP עבור תבנית באורך $m>1$ אזי לא יתכן כי בטבלה יש את "
      r"הערך $m-1$." "\n"
      r"נכון / לא נכון. נימוק:",
      5),
    Q(5, "ב", "truefalse", "kmp_strings",
      r"**שאלת בונוס** (סעיף בלתי תלוי, 5 נקודות)." "\n"
      r"יתכן שבאלגוריתם KMP עם טקסט $T$ באורך $n$ ותבנית $P$ באורך $m$, הלולאה הפנימית תתבצע $O(1)$." "\n"
      r"נכון / לא נכון. נימוק:",
      5),
    Q(5, "ג", "truefalse", "kmp_strings",
      r"**שאלת בונוס** (סעיף בלתי תלוי, 5 נקודות)." "\n"
      r"יתכן שהאלגוריתם הנאיבי לפתרון בעיית חיפוש מחרוזת $P$ באורך $m$ בטקסט $T$ באורך $n$ רץ בזמן לינארי." "\n"
      r"נכון / לא נכון. נימוק:",
      5),
]

exam = {
    "examCode": "26A-B",
    "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד ב (05/03/2026)",
    "year": 2026,
    "examDate": "05/03/2026",
    "sourceFile": "26A-B exam pp.1-18",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1: מסע עם לינה במלונות", "text": C1},
        "c2": {"kind": "text", "title": "שאלה 2: עצי BFS ו-DFS", "text": C2},
        "c3": {"kind": "text", "title": "שאלה 3: אלגוריתם הסרת צלעות", "text": C3},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
