# -*- coding: utf-8 -*-
"""Generator for tools/raw/25A-C.json -- algorithms-1, semester A 2025, moed C (special sitting).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25A-C.py

Source: 4-page scan-like PDF (no text layer, one question per page, no cover page and no date), read from the rendered
pages. NO answer source (GATE1: no-key): every item is held with reason "no-key" for the solver.
This is a short sitting: pages 1-4 hold Q1..Q4 only. The printed points are: Q1 (25) = a 15 + b 10; Q2: a (no points
printed; 25 - 10 = 15 by subtraction, NOT printed, so omitted) and b 10; Q3: a 15, b 10; Q4: a 15, b 10.
Items: Q1 a,b; Q2 a,b; Q3 a,b; Q4 a,b (8 items).
Notes
- Q1: "S1 ו-S2 באורך i ו-j" in part a is as printed (the lengths of the prefixes in the recurrence OPT(i,j)).
  The printed answer skeleton is OPT(i,j) = { ... / ... / ... } (three empty cases).
- Q3: the example array shows a "0" printed with a slash in the scan ([4,5,6,7,0,1,2]); read as the digit zero.
- The scan is low resolution; every token was checked against the page image.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25A-C.json"
HOLD = "no-key"


def Q(num, part, kind, topic, question, points=None, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "hold": HOLD}
    if points is not None:
        q["points"] = points
    if part:
        q["part"] = part
    q.update(kw)
    return q


C1 = (r"**שאלה 1 (25 נקודות)**" "\n"
      r"מרחק בין סדרות. בהינתן שתי סדרות $S_1$ ו-$S_2$ באותו אורך $n$, המרחק $d(S_1,S_2)$ בין הסדרות הוא מספר "
      r"המקומות $i$ בהם התווים בשתי הסדרות שונים זה מזה:" "\n"
      r"$$d(S_1,S_2)=\sum_{i=1}^{n}\delta\bigl(S_1[i],S_2[i]\bigr)$$" "\n"
      r"כאשר" "\n"
      r"$$\delta(x,y)=\begin{cases}0 & x=y\\ 1 & x\neq y\end{cases}$$" "\n"
      r"למשל, עבור הסדרות" "\n"
      "```\n"
      "S1:    A G C T T A C G\n"
      "S2:    A C T T A A C G\n"
      "index: 1 2 3 4 5 6 7 8\n"
      "```\n"
      r"המרחק $d(S_1,S_2)=3$ כי יש 3 מקומות $(2,3,5)$ בהם התווים של הסדרות שונים זה מזה." "\n"
      r"בעיית יישור סדרות. בהינתן שתי סדרות $S_1$ ו-$S_2$ באורך $n_1$ ו-$n_2$ בהתאמה, נדרש ליצור 2 סדרות $T_1$ ו-$T_2$ "
      r"באותו אורך $\max\{n_1,n_2\}\le m$ על ידי הוספת תווים '-' בין האותיות של $S_1$ ו-$S_2$, כך שהמרחק בין הסדרות "
      r"$T_1$ ו-$T_2$ יהיה מינימלי. למשל, עבור הסדרות $S_1,S_2$ לעיל, היישור האופטימלי הינו:" "\n"
      "```\n"
      "T1:    A G C T T - A C G\n"
      "T2:    A - C T T A A C G\n"
      "index: 1 2 3 4 5 6 7 8 9\n"
      "```\n"
      r"המרחק בין $T_1$ ו-$T_2$ הינו $d(T_1,T_2)=2$ (בין $T_1$ ו-$T_2$ יש אי-התאמה רק בשני מקומות, 2 ו-6).")

C2 = (r"**שאלה 2**" "\n"
      r"נתונה הבעיה הבאה:" "\n"
      r"קלט: שני מערכים בגודל $n$," "\n"
      r"- מערך $Val[1..n]$ שמייצג את הערכים (שווי) של פריטים." "\n"
      r"- מערך $Wt[1..n]$ שמייצג את המשקלים של אותם פריטים." "\n"
      r"ומספר שלם $capacity$ שמייצג את משקל התרמיל המרבי שאפשר לשאת." "\n"
      r"פלט: הערך המרבי שניתן להשיג על ידי הכנסת פריטים לתרמיל אך מותר לפרק פריטים לחלקים, כלומר, לקחת גם חלק מפריט "
      r"(למשל חצי או רבע פריט)." "\n"
      r"דוגמא:" "\n"
      r"בהינתן הקלט:" "\n"
      "```\n"
      "Val = [60,100,120]\n"
      "Wt = [10,20,30]\n"
      "Capacity = 50\n"
      "```\n"
      r"פלט: 240" "\n"
      r"הסבר:" "\n"
      r"ניקח:" "\n"
      r"- את הפריט הראשון כולו (משקל 10, ערך 60)," "\n"
      r"- את הפריט השני כולו (משקל 20, ערך 100)," "\n"
      r"- שני שלישים מהפריט השלישי (20 ק\"ג מתוך 30 ק\"ג, כלומר ערך של $(2/3)\times 120=80$)." "\n"
      r"סה\"כ: $60+100+80=240$" "\n"
      r"הבעיה ניתנת לפתרון באופן חמדני.")

C3 = (r"**שאלה 3**" "\n"
      r"קלט:" "\n"
      r"הקלט מורכב משני קלטים (מערך ומספר):" "\n"
      r"- מערך של $n$ מספרים שלמים $nums[0..n-1]$ אשר היה ממוין בסדר עולה ולאחר מכן סובב (Rotated) במקום כלשהו לא ידוע "
      r"מראש." "\n"
      r"לדוגמה: `[4,5,6,7,0,1,2]` הוא סיבוב של המערך `[0,1,2,4,5,6,7]`." "\n"
      r"- מספר מטרה $t$." "\n"
      r"פלט:" "\n"
      r"החזר את האינדקס שבו מספר מטרה $t$ מופיע במערך. אם מספר $t$ אינו מופיע במערך, החזר $-1$." "\n"
      r"דוגמא:" "\n"
      r"קלט: `Nums = [4,5,6,7,0,1,2]`, `t=0`" "\n"
      r"פלט: 4 (המערך ממוספר מאינדקס 0)")

C4 = (r"**שאלה 4**" "\n"
      r"הגדרה: נאמר שמחרוזת $P_1$ מסתתרת במחרוזת $P_2$ אם המחרוזת ההפוכה של $P_1$ היא תת מחרוזת של $P_2$." "\n"
      r"לדוגמא, המחרוזת `abc` מסתתרת במחרוזת `dfzcbau`." "\n"
      r"להלן בעיית המחרוזת המסתתרת:" "\n"
      r"קלט: טקסט $T$ באורך $n$ ותבנית $P$ באורך $m$ כאשר: $m<n$" "\n"
      r"פלט: אמת אם $P$ מסתתרת ב-$T$ אחרת יחזיר שקר")

questions = [
    Q(1, "א", "algorithm", "dp_sequences",
      r"(15 נקודות) בהינתן שתי סדרות $S_1$ ו-$S_2$ באורך $i$ ו-$j$ בהתאמה, הציגו נוסחה רקורסיבית לחישוב של המרחק של "
      r"היישור האופטימלי בין $S_1$ ו-$S_2$." "\n"
      r"$$OPT(i,j)=\begin{cases}\ldots\\ \ldots\\ \ldots\end{cases}$$",
      15, contextId="c1"),
    Q(1, "ב", "computation", "dp_sequences",
      r"(10 נקודות) מהי סיבוכיות זמן הריצה של אלגוריתם תכנון דינמי המבוסס על הנוסחה שכתבתם בסעיף א', ומהי סיבוכיות "
      r"המקום שלו לחישוב המרחק של היישור האופטימלי בין $S_1$ ו-$S_2$?" "\n"
      r"אין צורך לפרט את האלגוריתם עצמו.",
      10, contextId="c1"),

    Q(2, "א", "algorithm", "greedy",
      r"כתבו אלגוריתם חמדני לפתרון הבעיה.",
      contextId="c2"),
    Q(2, "ב", "proof", "greedy",
      r"(10 נקודות) הוכחו את נכונות הפתרון שהצגת בסעיף א'.",
      10, contextId="c2"),

    Q(3, "א", "algorithm", "divide_conquer",
      r"(15 נקודות) הציעו אלגוריתם הפרד ומשול יעיל ככל הניתן לפתרון הבעיה.",
      15, contextId="c3"),
    Q(3, "ב", "computation", "divide_conquer",
      r"(10 נקודות) מה סיבוכיות זמן הריצה של האלגוריתם שהצעתם? נמקו תשובתכם.",
      10, contextId="c3"),

    Q(4, "א", "algorithm", "kmp_strings",
      r"(15 נקודות) הציעו אלגוריתם לינארי לפתרון הבעיה ללא שימוש בעצי סיפות או מערכי סיפות.",
      15, contextId="c4"),
    Q(4, "ב", "computation", "kmp_strings",
      r"(10 נקודות) הסבירו מדוע זמן הריצה לינארי בגודל הקלט? מה סיבוכיות המקום של האלגוריתם שהצעתם?",
      10, contextId="c4"),
]

exam = {
    "examCode": "25A-C",
    "examLabel": "אלגוריתמים 1, סמסטר א' תשפ\"ה, מועד ג",
    "year": 2025,
    "examDate": "2025",
    "sourceFile": "25A-C exam pp.1-4 (scan)",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1: מרחק ויישור סדרות", "text": C1},
        "c2": {"kind": "text", "title": "שאלה 2: תרמיל עם פירוק פריטים", "text": C2},
        "c3": {"kind": "text", "title": "שאלה 3: חיפוש במערך מסובב", "text": C3},
        "c4": {"kind": "text", "title": "שאלה 4: המחרוזת המסתתרת", "text": C4},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
