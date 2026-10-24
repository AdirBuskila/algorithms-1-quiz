# -*- coding: utf-8 -*-
"""Generator for tools/raw/25A-C.json -- algorithms-1, semester A 2025, moed C (special sitting).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25A-C.py

Source: 4-page scan-like PDF (no text layer, one question per page, no cover page and no date), read from the rendered
pages. NO answer source (GATE1: no-key): originally held "no-key"; solved by the solver (see below).
This is a short sitting: pages 1-4 hold Q1..Q4 only. The printed points are: Q1 (25) = a 15 + b 10; Q2: a (no points
printed; 25 - 10 = 15 by subtraction, NOT printed, so omitted) and b 10; Q3: a 15, b 10; Q4: a 15, b 10.
Items: Q1 a,b; Q2 a,b; Q3 a,b; Q4 a,b (8 items).
Notes
- Q1: "S1 ו-S2 באורך i ו-j" in part a is as printed (the lengths of the prefixes in the recurrence OPT(i,j)).
  The printed answer skeleton is OPT(i,j) = { ... / ... / ... / ... } (FOUR empty cases; the first transcription
  had three, corrected by the solver after re-checking page 1 at 200 dpi).
Solver pass (2026-10-24): the transcription was re-verified line by line against fresh 200-dpi renders of pp.1-4
(only the skeleton case count differed). All 8 items solved (solutionSource "solved", official false), pending the
refuter. Checks: tools/verify/25A-C/solve_all.py (all OK):
- Q1: the 4-case recurrence == brute force over every way of inserting '-' (400 random pairs); printed example -> 2;
  the two-row version equals the full table.
- Q2: greedy by Val/Wt == exact optimum (subset + one fractional item, Fractions, 3000 random); example -> 240.
- Q3: recursive rotated binary search == linear search (20000 rotated arrays, distinct values), at most
  floor(log2 n)+2 calls. Distinct values are assumed (as in the example); the solution says duplicates force Theta(n).
- Q4: KMP(T, reverse(P)) == "reverse(P) in T" (20000 random); printed example true.
- Q3: the example array shows a "0" printed with a slash in the scan ([4,5,6,7,0,1,2]); read as the digit zero.
- The scan is low resolution; every token was checked against the page image.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25A-C.json"
HOLD = "no-key"


def Q(num, part, kind, topic, question, points=None, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question}
    if "solution" in kw:   # solved by the solver (no official key exists)
        q.update({"solutionSource": "solved", "official": False, "confidence": "high"})
    else:
        q["hold"] = HOLD
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

# ---------------------------------------------------------------- solver solutions (no official key)
SOL_1A = (r"נגדיר $OPT(i,j)$ = המרחק של היישור האופטימלי בין הרישא $S_1[1..i]$ לרישא $S_2[1..j]$. "
          r"כל עמודה ביישור היא אחת משלוש: תו מול תו, תו של $S_1$ מול '-', או '-' מול תו של $S_2$. "
          r"תו מול '-' תמיד שונה, ולכן עולה 1 (כמו בדוגמה, עמודה 6)." "\n"
          r"$$OPT(i,j)=\begin{cases}j & i=0\\ i & j=0\\ OPT(i-1,j-1) & i,j>0,\ S_1[i]=S_2[j]\\ "
          r"1+\min\bigl\{OPT(i-1,j-1),\ OPT(i-1,j),\ OPT(i,j-1)\bigr\} & i,j>0,\ S_1[i]\neq S_2[j]\end{cases}$$" "\n"
          r"**משמעות:** מסתכלים על העמודה האחרונה של יישור אופטימלי." "\n"
          r"- אם רישא אחת ריקה, כל התווים של השנייה עומדים מול '-', ולכן המרחק הוא אורכה ($j$ או $i$)." "\n"
          r"- $S_1[i]$ מול $S_2[j]$: עלות $0$ אם הם שווים ו-$1$ אחרת, ועוד $OPT(i-1,j-1)$." "\n"
          r"- $S_1[i]$ מול '-': עלות $1$ ועוד $OPT(i-1,j)$." "\n"
          r"- '-' מול $S_2[j]$: עלות $1$ ועוד $OPT(i,j-1)$." "\n"
          r"כשהתווים שווים אין צורך להשוות לשתי האפשרויות האחרות: $OPT(i-1,j-1)\le OPT(i-1,j)+1$ ו-"
          r"$OPT(i-1,j-1)\le OPT(i,j-1)+1$ (מחיקת תו אחד מקלט משנה את המרחק לכל היותר ב-1), ולכן ההתאמה החינמית היא הטובה "
          r"ביותר." "\n"
          r"התשובה היא $OPT(n_1,n_2)$. עבור הדוגמה מתקבל $OPT(8,8)=2$, כמו ביישור המודפס." "\n"
          r"(עמודה של '-' מול '-' אינה משתלמת: היא לא משנה את המרחק, ולכן אפשר להניח שאין כזו.)")

SOL_1B = (r"**זמן:** הטבלה בגודל $(n_1+1)\times(n_2+1)$, וכל תא מחושב בזמן $O(1)$ משלושה תאים שכבר חושבו "
          r"(מילוי שורה אחרי שורה). סה\"כ $O(n_1n_2)$." "\n"
          r"**מקום:** $O(n_1n_2)$ אם שומרים את כל הטבלה (נדרש כדי לשחזר את היישור עצמו). לחישוב המרחק בלבד מספיקות שתי "
          r"שורות, כי שורה $i$ תלויה רק בשורה $i-1$ ובתא הקודם בשורה הנוכחית, ולכן מקום $O(\min\{n_1,n_2\})$ (נבחר את "
          r"הסדרה הקצרה כממד השורה).")

SOL_2A = (r"(מניחים משקלים חיוביים, $Wt[i]>0$.)" "\n"
          r"**רעיון חמדני:** לוקחים קודם את הפריטים עם הערך הגבוה ביותר לכל יחידת משקל, $\frac{Val[i]}{Wt[i]}$." "\n"
          "```\n"
          "FRACTIONAL_KNAPSACK(Val[1..n], Wt[1..n], capacity):\n"
          "    sort the items by Val[i]/Wt[i] in decreasing order\n"
          "    total <- 0 ; room <- capacity\n"
          "    for each item i in that order:\n"
          "        if room = 0: break\n"
          "        take <- min(Wt[i], room)          // the whole item, or the part that fits\n"
          "        total <- total + Val[i] * take / Wt[i]\n"
          "        room <- room - take\n"
          "    return total\n"
          "```\n"
          r"בדוגמה היחסים הם $6,5,4$: לוקחים את הפריט הראשון והשני במלואם ו-$20$ מתוך $30$ ק\"ג של השלישי, $240$." "\n"
          r"**זמן ריצה:** $O(n\log n)$ למיון ו-$O(n)$ למעבר, סה\"כ $O(n\log n)$.")

SOL_2B = (r"נסדר את הפריטים כך ש-$\frac{Val[1]}{Wt[1]}\ge\frac{Val[2]}{Wt[2]}\ge\cdots\ge\frac{Val[n]}{Wt[n]}$, ונסמן ב-"
          r"$x_i\in[0,1]$ את החלק שנלקח מפריט $i$. הפתרון החמדני $G$ הוא: $x_1=\cdots=x_{r-1}=1$, $x_r$ חלקי (אם צריך), "
          r"ו-$x_i=0$ אחריו; אם סך המשקל קטן מ-$capacity$ הוא לוקח את כל הפריטים, וזה ודאי אופטימלי." "\n"
          r"**טיעון החלפה:** יהי $O$ פתרון אופטימלי שמסכים עם $G$ על מספר מרבי של פריטים ראשונים, ונניח $O\neq G$. "
          r"יהי $i$ האינדקס הראשון שבו $y_i\neq x_i$ ($y$ הם החלקים ב-$O$). מאחר שהחמדן לוקח מכל פריט כמה שאפשר, $y_i<x_i$. "
          r"כיוון ש-$O$ אופטימלי הוא ממלא את התרמיל (אחרת אפשר להוסיף עוד מפריט $i$ ולהגדיל את הערך), ולכן יש $j>i$ עם $y_j>0$." "\n"
          r"נעביר משקל $\varepsilon=\min\{(x_i-y_i)Wt[i],\ y_jWt[j]\}>0$ מפריט $j$ לפריט $i$. המשקל הכולל לא משתנה, "
          r"והערך משתנה ב-" "\n"
          r"$$\varepsilon\Bigl(\frac{Val[i]}{Wt[i]}-\frac{Val[j]}{Wt[j]}\Bigr)\ge 0$$" "\n"
          r"כי $i<j$. לכן הפתרון החדש עדיין אופטימלי, ובו או ש-$y_i=x_i$ או ש-$y_j=0$. חזרה על הצעד (מספר סופי של פעמים, "
          r"כל פעם מתאפס פריט אחרי $i$ או ש-$i$ מתיישר) מביאה לפתרון אופטימלי שמסכים עם $G$ גם במקום $i$, בסתירה "
          r"לבחירת $O$. לכן $G=O$ והחמדן אופטימלי.")

SOL_3A = (r"(מניחים שהערכים שונים זה מזה, כמו בדוגמה.)" "\n"
          r"**רעיון:** חיפוש בינארי. אחרי סיבוב, בכל קטע $nums[lo..hi]$ ובאמצעו $mid$, לפחות אחד החצאים "
          r"$nums[lo..mid]$ או $nums[mid..hi]$ ממוין: נקודת הסיבוב (המעבר מהגדול לקטן) נמצאת לכל היותר באחד מהם. "
          r"בודקים אם $t$ בטווח של החצי הממוין; אם כן ממשיכים רק בו, ואחרת רק בחצי השני." "\n"
          "```\n"
          "SEARCH(nums, t, lo, hi):\n"
          "    if lo > hi: return -1\n"
          "    mid <- floor((lo + hi) / 2)\n"
          "    if nums[mid] = t: return mid\n"
          "    if nums[lo] <= nums[mid]:                 // the left half is sorted\n"
          "        if nums[lo] <= t < nums[mid]: return SEARCH(nums, t, lo, mid - 1)\n"
          "        else:                         return SEARCH(nums, t, mid + 1, hi)\n"
          "    else:                                     // the right half is sorted\n"
          "        if nums[mid] < t <= nums[hi]: return SEARCH(nums, t, mid + 1, hi)\n"
          "        else:                         return SEARCH(nums, t, lo, mid - 1)\n"
          "\n"
          "answer: SEARCH(nums, t, 0, n - 1)\n"
          "```\n"
          r"**נכונות:** אם $nums[lo]\le nums[mid]$ אין נקודת סיבוב בתוך $nums[lo..mid]$, ולכן הוא ממוין, ו-$t$ נמצא בו "
          r"אם ורק אם $nums[lo]\le t<nums[mid]$ (את $mid$ כבר בדקנו); אחרת $t$ יכול להיות רק בחצי הימני. "
          r"אחרת נקודת הסיבוב בחצי השמאלי, ולכן $nums[mid..hi]$ ממוין, והבדיקה סימטרית. כל קטע שנשאר הוא שוב "
          r"סיבוב של מערך ממוין, ולכן אפשר להמשיך ברקורסיה." "\n"
          r"בדוגמה: $mid=3$, $nums[3]=7$, החצי השמאלי $[4,5,6,7]$ ממוין ו-$0$ לא בטווח, ממשיכים ב-$[0,1,2]$ ומוצאים את "
          r"$0$ באינדקס $4$.")

SOL_3B = (r"בכל קריאה עושים $O(1)$ עבודה (כמה השוואות) וממשיכים בקריאה רקורסיבית אחת על לכל היותר חצי מהקטע:" "\n"
          r"$$T(n)=T\bigl(\tfrac n2\bigr)+O(1)$$" "\n"
          r"לפי משפט האב ($a=1$, $b=2$, $f(n)=\Theta(1)=\Theta(n^{\log_2 1})$, המקרה השני) $T(n)=O(\log n)$." "\n"
          r"הערה: ההנחה שהערכים שונים נחוצה. עם ערכים חוזרים (למשל $[1,1,1,0,1]$ מול $[1,0,1,1,1]$) אי אפשר לדעת איזה "
          r"חצי ממוין, ובמקרה הגרוע נדרש $\Theta(n)$.")

SOL_4A = (r"$P$ מסתתרת ב-$T$ אם ורק אם $P^R$ (ההפוכה של $P$) מופיעה ב-$T$ כתת-מחרוזת. לכן:" "\n"
          "```\n"
          "HIDDEN(T[1..n], P[1..m]):\n"
          "    R <- P reversed            // R[i] = P[m + 1 - i], O(m)\n"
          "    return KMP(T, R)           // true if R occurs in T\n"
          "```\n"
          r"KMP מחשב את פונקציית הרישא $\pi$ של $R$ ואז סורק את $T$ פעם אחת; אפשר לעצור ולהחזיר אמת במופע הראשון, "
          r"ואם הסריקה הסתיימה בלי מופע מחזירים שקר." "\n"
          r"בדוגמה: $P=abc$, $R=cba$, ו-$cba$ מופיעה ב-$dfzcbau$, ולכן אמת.")

SOL_4B = (r"**זמן:** היפוך $P$ עולה $O(m)$. חישוב $\pi$ עולה $O(m)$ ושלב החיפוש של KMP עולה $O(n)$: בניתוח לשיעורין, "
          r"המשתנה $q$ (אורך ההתאמה הנוכחית) גדל לכל היותר ב-1 לכל תו של הטקסט, וכל ביצוע של לולאת הנסיגה מקטין אותו "
          r"לפחות ב-1, ולכן מספר הנסיגות הכולל לכל היותר $n$. סה\"כ $O(n+m)=O(n)$ (כי $m<n$), לינארי בגודל הקלט." "\n"
          r"**מקום:** $O(m)$: המחרוזת ההפוכה ומערך $\pi$ בגודל $m$ (הטקסט נקרא במקום).")

questions = [
    Q(1, "א", "algorithm", "dp_sequences",
      r"(15 נקודות) בהינתן שתי סדרות $S_1$ ו-$S_2$ באורך $i$ ו-$j$ בהתאמה, הציגו נוסחה רקורסיבית לחישוב של המרחק של "
      r"היישור האופטימלי בין $S_1$ ו-$S_2$." "\n"
      r"$$OPT(i,j)=\begin{cases}\ldots\\ \ldots\\ \ldots\\ \ldots\end{cases}$$",
      15, contextId="c1", solution=SOL_1A),
    Q(1, "ב", "computation", "dp_sequences",
      r"(10 נקודות) מהי סיבוכיות זמן הריצה של אלגוריתם תכנון דינמי המבוסס על הנוסחה שכתבתם בסעיף א', ומהי סיבוכיות "
      r"המקום שלו לחישוב המרחק של היישור האופטימלי בין $S_1$ ו-$S_2$?" "\n"
      r"אין צורך לפרט את האלגוריתם עצמו.",
      10, contextId="c1", solution=SOL_1B),

    Q(2, "א", "algorithm", "greedy",
      r"כתבו אלגוריתם חמדני לפתרון הבעיה.",
      contextId="c2", solution=SOL_2A),
    Q(2, "ב", "proof", "greedy",
      r"(10 נקודות) הוכחו את נכונות הפתרון שהצגת בסעיף א'.",
      10, contextId="c2", solution=SOL_2B),

    Q(3, "א", "algorithm", "divide_conquer",
      r"(15 נקודות) הציעו אלגוריתם הפרד ומשול יעיל ככל הניתן לפתרון הבעיה.",
      15, contextId="c3", solution=SOL_3A),
    Q(3, "ב", "computation", "divide_conquer",
      r"(10 נקודות) מה סיבוכיות זמן הריצה של האלגוריתם שהצעתם? נמקו תשובתכם.",
      10, contextId="c3", solution=SOL_3B),

    Q(4, "א", "algorithm", "kmp_strings",
      r"(15 נקודות) הציעו אלגוריתם לינארי לפתרון הבעיה ללא שימוש בעצי סיפות או מערכי סיפות.",
      15, contextId="c4", solution=SOL_4A),
    Q(4, "ב", "computation", "kmp_strings",
      r"(10 נקודות) הסבירו מדוע זמן הריצה לינארי בגודל הקלט? מה סיבוכיות המקום של האלגוריתם שהצעתם?",
      10, contextId="c4", solution=SOL_4B),
]

# ---------------------------------------------------------------- rubric / pitfalls / steps (ai-draft)
# Every expected value below is recomputed by tools/verify/25A-C/steps_25A-C.py (brute force, exact fractions, KMP counters).
def rub(*items):
    return [{"text": t, "points": p} for t, p in items]


def ch(prompt, correct, wrong, pos, explain, **kw):
    """choice step: the correct option sits at index `pos`, wrong options fill the rest."""
    vals = list(wrong)
    vals.insert(pos, correct)
    s = {"type": "choice", "prompt": prompt,
         "options": [{"id": "abcdefgh"[i], "value": v} for i, v in enumerate(vals)],
         "correctId": "abcdefgh"[pos], "explain": explain}
    s.update(kw)
    return s


def num(prompt, answer, explain, **kw):
    s = {"type": "numeric", "prompt": prompt, "answer": answer, "tol": 0, "explain": explain}
    s.update(kw)
    return s


def txt(prompt, accept, explain, normalize="complexity"):
    return {"type": "text", "prompt": prompt, "accept": accept, "normalize": normalize, "explain": explain}


def add(num_, part, **kw):
    for q in questions:
        if q["num"] == num_ and q.get("part", "") == (part or ""):
            q.update(kw)
            return
    raise KeyError((num_, part))


SEARCH_LINES = ["SEARCH(nums, t, lo, hi):",
                "    if lo > hi: return -1",
                "    mid <- floor((lo + hi) / 2)",
                "    if nums[mid] = t: return mid",
                "    if nums[lo] <= nums[mid]:",
                "        if nums[lo] <= t < nums[mid]: return SEARCH(nums, t, lo, mid - 1)",
                "        else:                         return SEARCH(nums, t, mid + 1, hi)",
                "    else:",
                "        if nums[mid] < t <= nums[hi]: return SEARCH(nums, t, mid + 1, hi)",
                "        else:                         return SEARCH(nums, t, lo, mid - 1)"]
SEARCH_BLANK = list(SEARCH_LINES)
SEARCH_BLANK[6] = "        else:                         return ___"
SEARCH_BUG = list(SEARCH_LINES)
SEARCH_BUG[5] = "        if nums[lo] <= t <= nums[hi]: return SEARCH(nums, t, lo, mid - 1)"
_fb = ch("השלימו את השורה החסרה: כש-$t$ אינו בטווח של החצי השמאלי הממוין, לאן ממשיכים?",
         "SEARCH(nums, t, mid + 1, hi)",
         ["SEARCH(nums, t, mid, hi)", "SEARCH(nums, t, mid + 1, hi - 1)", "SEARCH(nums, t, lo, mid)"], 2,
         "ממשיכים בחצי הימני $mid+1..hi$. הקריאה עם $mid$ נתקעת בלולאה אינסופית כשהקטע כולל איבר אחד, "
         "זו עם $hi-1$ מפספסת את $t$ ב-$hi$, וזו עם $lo..mid$ חוזרת לחצי השמאלי שכבר נפסל (נבדק בהרצות).")
_fb.update({"type": "fillblank", "code": True, "lines": SEARCH_BLANK, "blankIndex": 6})

add(1, "א",
    rubric=rub(("מקרי בסיס: $OPT(0,j)=j$ ו-$OPT(i,0)=i$", 4),
               ("תווים שווים: $OPT(i,j)=OPT(i-1,j-1)$", 4),
               ("תווים שונים: $1+\\min\\{OPT(i-1,j-1),OPT(i-1,j),OPT(i,j-1)\\}$", 5),
               ("התשובה היא $OPT(n_1,n_2)$", 2)),
    rubricSource="ai-draft",
    pitfalls=["להוסיף $1$ גם כשהתווים שווים, ואז $OPT(1,1)$ של `A` מול `A` יוצא $1$ במקום $0$.",
              "לשכוח את שתי האפשרויות של תו מול '-' ולהסתפק בתו מול תו.",
              "לחשב מקרי בסיס כ-$0$ במקום אורך הרישא שמול '-'."],
    steps=[
        ch("מהו $OPT(0,j)$ (רישא ריקה של $S_1$ מול $j$ תווים של $S_2$)?", "$j$", ["$0$", "$\\infty$", "$1$"], 0,
           "כל $j$ התווים עומדים מול '-' ולכל אחד עלות $1$. הערך $0$ מתאים רק ל-$j=0$."),
        ch("כש-$S_1[i]=S_2[j]$, מה הערך של $OPT(i,j)$?", "$OPT(i-1,j-1)$",
           ["$1+OPT(i-1,j-1)$", "$\\min\\{OPT(i-1,j),OPT(i,j-1)\\}$", "$1+\\min\\{OPT(i-1,j-1),OPT(i-1,j),OPT(i,j-1)\\}$"], 2,
           "התאמה חינמית היא הטובה ביותר. עבור `A` מול `A` הנוסחאות האחרות נותנות $1$ ולא $0$ (נבדק)."),
        num("עבור הרישאות `AGC` ו-`ACT` ($S_1[1..3]$ ו-$S_2[1..3]$): מהו $OPT(3,3)$?", 2,
            "היישור `AGC-` מול `A-CT` נותן שתי אי-התאמות. הערך אומת בכוח גס על כל היישורים."),
        num("ומהו $OPT(8,8)$ עבור שתי הסדרות המלאות?", 2, "כמו ביישור שבשאלה, $d=2$ (נבדק בטבלה ובכוח גס)."),
    ],
    stepsSource="ai-draft")

add(1, "ב",
    rubric=rub(("טבלה $(n_1+1)(n_2+1)$ ותא ב-$O(1)$, ולכן זמן $O(n_1n_2)$", 4),
               ("מקום $O(n_1n_2)$ לטבלה המלאה (נדרש לשחזור היישור)", 2),
               ("שורה תלויה רק בקודמתה, ולכן מקום $O(\\min\\{n_1,n_2\\})$ לחישוב המרחק", 4)),
    rubricSource="ai-draft",
    pitfalls=["לענות $O(n_1+n_2)$ לזמן: יש $n_1n_2$ תאים.",
              "לא להבחין בין חישוב המרחק בלבד (שתי שורות) לבין שחזור היישור (כל הטבלה)."],
    steps=[
        num("כמה תאים יש בטבלה עבור $n_1=n_2=8$?", 81, "$(8+1)(8+1)=81$."),
        txt("מהי סיבוכיות הזמן? (למשל `O(n)`)", ["O(n1n2)", "O(n1*n2)", "O(n_1n_2)", "O(n1 n2)"],
            "כל תא ב-$O(1)$ מתוך $n_1n_2$ תאים."),
        txt("מהי סיבוכיות המקום לחישוב המרחק בלבד, בלי לשחזר את היישור? (למשל `O(n)`)",
            ["O(min(n1,n2))", "O(min{n1,n2})", "O(min(n_1,n_2))"],
            "מספיקות שתי שורות באורך הסדרה הקצרה (נבדק שהתוצאה זהה לטבלה המלאה)."),
    ],
    stepsSource="ai-draft")

add(2, "א",
    rubric=rub(("מיון הפריטים לפי היחס $\\frac{Val}{Wt}$ בסדר יורד", 4),
               ("לולאה: לוקחים $\\min(Wt[i],room)$ מהפריט", 5),
               ("הוספת הערך היחסי $Val[i]\\cdot take/Wt[i]$ ועדכון הקיבולת", 3),
               ("עצירה כשהתרמיל מלא", 1),
               ("זמן $O(n\\log n)$", 2)),
    rubricSource="ai-draft",
    pitfalls=["למיין לפי הערך או לפי המשקל בלבד: בשני המקרים יש קלט שבו התוצאה נמוכה מהאופטימום.",
              "לקחת פריט שלם בלבד, וכך לפספס את החלק היחסי של הפריט האחרון.",
              "לשכוח לעצור כשהתרמיל מלא, ולקחת משקל שלילי."],
    steps=[
        ch("לפי איזה קריטריון ממיינים את הפריטים?", "הערך ליחידת משקל $\\frac{Val[i]}{Wt[i]}$, מהגדול לקטן",
           ["הערך $Val[i]$, מהגדול לקטן", "המשקל $Wt[i]$, מהקטן לגדול", "המשקל $Wt[i]$, מהגדול לקטן"], 0,
           "לכל אחד מהקריטריונים האחרים נמצא קלט שבו התוצאה נמוכה מהאופטימום (נבדק באקראי)."),
        num("בדוגמה ($Val=[60,100,120]$, $Wt=[10,20,30]$, קיבולת $50$): מהו הערך שנלקח מהפריט השלישי כשלוקחים $20$ מתוך $30$?", 80,
            "$\\frac{20}{30}\\cdot120=80$."),
        num("מהו הערך הכולל של הפתרון החמדני בדוגמה?", 240, "$60+100+80=240$ (שווה לאופטימום בכוח גס)."),
        txt("מהי סיבוכיות הזמן של האלגוריתם? (למשל `O(n)`)", ["O(n log n)", "O(nlogn)"],
            "המיון $O(n\\log n)$ והמעבר $O(n)$."),
    ],
    stepsSource="ai-draft")

add(2, "ב",
    rubric=rub(("סידור לפי היחס והגדרת הפתרון החמדני $x$", 2),
               ("טיעון החלפה: האינדקס הראשון $i$ ש-$y_i\\ne x_i$, ו-$y_i<x_i$", 3),
               ("העברת משקל $\\varepsilon$ מפריט $j>i$ לפריט $i$ לא מקטינה את הערך", 3),
               ("הפתרון החדש מסכים עם החמדן על יותר פריטים, סתירה לבחירת $O$", 2)),
    rubricSource="ai-draft",
    pitfalls=["להוכיח רק על הדוגמה ולא באופן כללי.",
              "להחליף משקל בלי להראות שהמשקל הכולל נשמר ושהערך לא יורד.",
              "לא לטפל בכך שהחלק שנלקח מפריט נקבע בקיבולת שנותרה."],
    steps=[
        ch("איזו שיטת הוכחה משמש הפתרון הרשמי?",
           "טיעון החלפה: מעבירים משקל מפריט מאוחר לפריט הראשון שבו האופטימלי שונה מהחמדן",
           ["אינדוקציה על $n$ והסרת הפריט האחרון", "הפרכה בדוגמה נגדית", "תכונת החתך"], 2,
           "ההוכחה מתחילה באופטימלי שמסכים עם החמדן על הכי הרבה פריטים ראשונים, ומחליפה משקל כדי להתיישר איתו."),
        num("פריט $i$ ביחס $6$ ופריט $j$ ביחס $4$. מעבירים $5$ יחידות משקל מ-$j$ ל-$i$. בכמה משתנה הערך?", 10,
            "$\\varepsilon\\bigl(\\frac{Val[i]}{Wt[i]}-\\frac{Val[j]}{Wt[j]}\\bigr)=5(6-4)=10$."),
        {"type": "order", "prompt": "סדרו את שלבי הוכחת ההחלפה.",
         "lines": [r"נסדר לפי $\frac{Val}{Wt}$ יורד, ויהי $O$ אופטימלי שמסכים עם החמדן $G$ על מספר מרבי של פריטים ראשונים.",
                   r"יהי $i$ הראשון ש-$y_i\neq x_i$. החמדן לוקח כמה שאפשר, ולכן $y_i<x_i$, ובגלל האופטימליות יש $j>i$ עם $y_j>0$.",
                   r"נעביר משקל $\varepsilon>0$ מפריט $j$ לפריט $i$. המשקל הכולל נשמר, והערך משתנה ב-$\varepsilon(\frac{Val[i]}{Wt[i]}-\frac{Val[j]}{Wt[j]})\ge0$.",
                   r"הפתרון החדש אופטימלי ומסכים עם החמדן על יותר פריטים, בסתירה לבחירת $O$. לכן $G$ אופטימלי."],
         "explain": "כל שורה נשענת על הקודמת: בחירת $O$, הצעד הראשון שונה, ההחלפה, הסתירה."},
        {"type": "findbug", "prompt": "בגרסה הבאה של ההוכחה שורה אחת שונתה והיא שגויה. מצאו אותה.",
         "lines": [r"נסדר לפי $\frac{Val}{Wt}$ יורד, ויהי $O$ אופטימלי שמסכים עם החמדן $G$ על מספר מרבי של פריטים ראשונים.",
                   r"יהי $i$ הראשון ש-$y_i\neq x_i$. החמדן לוקח כמה שאפשר, ולכן $y_i<x_i$, ובגלל האופטימליות יש $j>i$ עם $y_j>0$.",
                   r"נעביר משקל $\varepsilon>0$ מפריט $i$ לפריט $j$. המשקל הכולל נשמר, והערך משתנה ב-$\varepsilon(\frac{Val[i]}{Wt[i]}-\frac{Val[j]}{Wt[j]})\ge0$.",
                   r"הפתרון החדש אופטימלי ומסכים עם החמדן על יותר פריטים, בסתירה לבחירת $O$. לכן $G$ אופטימלי."],
         "bugIndex": 2,
         "explain": "המשקל מועבר מ-$j$ (היחס הנמוך) אל $i$ (היחס הגבוה), לא להפך. בכיוון ההפוך הערך יורד."},
    ],
    stepsSource="ai-draft")

add(3, "א",
    rubric=rub(("תצפית: לפחות אחד החצאים $[lo..mid]$ או $[mid..hi]$ ממוין", 4),
               ("בדיקה אם $t$ בטווח של החצי הממוין, והמשך בחצי המתאים בלבד", 5),
               ("מקרה בסיס $lo>hi$ ובדיקת $nums[mid]=t$", 3),
               ("גבולות נכונים בקריאה הרקורסיבית", 3)),
    rubricSource="ai-draft",
    pitfalls=["לבצע חיפוש בינארי רגיל בלי לזהות איזה חצי ממוין.",
              "לבדוק אם החצי השמאלי ממוין לפי $nums[mid]<nums[hi]$ או $nums[lo]<nums[hi]$: שני התנאים שגויים על סיבובים מסוימים.",
              "לא לקצר את הקטע ב-$mid\\pm1$ ולהיתקע בלולאה אינסופית."],
    steps=[
        ch("איזה תנאי מזהה שהחצי השמאלי $nums[lo..mid]$ ממוין?", "$nums[lo]\\le nums[mid]$",
           ["$nums[mid]<nums[hi]$", "$nums[lo]<nums[hi]$", "$nums[mid]=t$"], 1,
           "אם אין נקודת סיבוב בתוך החצי השמאלי אז $nums[lo]\\le nums[mid]$. התנאים האחרים נכשלים, למשל על `[6,7,0,1,2,4,5]` ועל הדוגמה `[4,5,6,7,0,1,2]`."),
        num("בדוגמה `[4,5,6,7,0,1,2]` עם $t=0$: כמה קריאות ל-SEARCH מתבצעות עד שמוצאים את האיבר (כולל הקריאה הראשונה)?", 3,
            "הקריאות הן $(0,6)$, $(4,6)$ ו-$(4,4)$, ובאחרונה $nums[4]=0$ (נבדק בהרצה, האינדקס המוחזר $4$)."),
        _fb,
        {"type": "findbug", "prompt": "בגרסה הבאה שורה אחת שונתה והאלגוריתם שגוי על חלק מהקלטים. מצאו אותה.", "code": True,
         "lines": SEARCH_BUG, "bugIndex": 5,
         "explain": "הבדיקה צריכה להיות $nums[lo]\\le t<nums[mid]$, טווח החצי הממוין. הגרסה שבה $t\\le nums[hi]$ מפנה לחצי שגוי (נבדק בהרצות אקראיות)."},
    ],
    stepsSource="ai-draft")

add(3, "ב",
    rubric=rub(("נוסחת נסיגה $T(n)=T(\\frac n2)+O(1)$", 4),
               ("משפט האב, מקרה שני: $T(n)=O(\\log n)$", 4),
               ("ההנחה שהערכים שונים נחוצה, ובלעדיה $\\Theta(n)$ במקרה הגרוע", 2)),
    rubricSource="ai-draft",
    pitfalls=["לכתוב $2T(\\frac n2)$ כאילו שני החצאים נסרקים: נסרק חצי אחד בלבד.",
              "לשכוח את ההנחה שהערכים שונים."],
    steps=[
        ch("איזו נוסחת נסיגה מתארת את האלגוריתם?", "$T(n)=T(\\frac n2)+O(1)$",
           ["$T(n)=2T(\\frac n2)+O(1)$", "$T(n)=T(\\frac n2)+O(n)$", "$T(n)=T(n-1)+O(1)$"], 0,
           "בכל קריאה עבודה קבועה וקריאה אחת על לכל היותר חצי מהקטע."),
        txt("מהי סיבוכיות הזמן? (למשל `O(n)`)", ["O(log n)", "O(logn)"], "משפט האב עם $a=1,b=2$, מקרה שני."),
        num("מהו המספר המרבי של קריאות ל-SEARCH עבור $n=1000$, על פני כל הסיבובים וכל מטרה (כולל מטרות שאינן במערך)?", 11,
            "נבדק בהרצה על $1000$ סיבובים. הערך $11\\le\\lfloor\\log_2 1000\\rfloor+2=11$."),
    ],
    stepsSource="ai-draft")

add(4, "א",
    rubric=rub(("הרעיון: $P$ מסתתרת ב-$T$ אם ורק אם $P^R$ היא תת-מחרוזת של $T$", 5),
               ("היפוך $P$ בזמן $O(m)$", 3),
               ("הרצת KMP עם התבנית $P^R$ על $T$", 4),
               ("החזרת אמת במופע ושקר אחרת", 3)),
    rubricSource="ai-draft",
    pitfalls=["לחפש את $P$ עצמה ב-$T$ (בדוגמה `abc` לא נמצאת ב-`dfzcbau`).",
              "לחפש את ההפוכה כתת-סדרה ולא כתת-מחרוזת רציפה.",
              "להשתמש בעץ סיפות, בניגוד לדרישה."],
    steps=[
        ch("מה מחפש האלגוריתם?", "את $P^R$ (ההפוכה של $P$) כתת-מחרוזת של $T$",
           ["את $P$ עצמה כתת-מחרוזת של $T$", "את $P^R$ כתת-סדרה (לא בהכרח רציפה) של $T$",
            "את $P^R$ כתת-מחרוזת של $T^R$"], 0,
           "זו ההגדרה. חיפוש $P$ ב-`dfzcbau` נכשל על הדוגמה, וכתת-סדרה `ba` נמצאת ב-`bxa` אף שאינה תת-מחרוזת (נבדק)."),
        num("הפונקציה $\\pi$ של התבנית ההפוכה של `abaab` (כלומר `baaba`): מהו הערך האחרון בטבלה?", 2,
            "$\\pi=[0,0,0,1,2]$ (חושב בהרצה)."),
        num("בדוגמה: באיזה אינדקס (מ-$1$) מופיעה `cba` בתוך `dfzcbau`?", 4,
            "האותיות `d,f,z` אחריהן `cba`, כלומר התחלה באינדקס $4$ (KMP מחזיר את אותו מקום)."),
    ],
    stepsSource="ai-draft")

add(4, "ב",
    rubric=rub(("היפוך $O(m)$ וחישוב $\\pi$ ב-$O(m)$", 2),
               ("שלב החיפוש $O(n)$ בניתוח לשיעורין: $q$ גדל לכל היותר ב-$1$ לתו, ונסיגה מקטינה אותו", 4),
               ("סה\"כ $O(n+m)=O(n)$ כי $m<n$", 2),
               ("מקום $O(m)$: המחרוזת ההפוכה ומערך $\\pi$", 2)),
    rubricSource="ai-draft",
    pitfalls=["לטעון $O(nm)$ כי לולאת הנסיגה פנימית: מספר הנסיגות הכולל חסום ב-$n$.",
              "לשכוח את מקום ה-$\\pi$ ולענות $O(1)$."],
    steps=[
        ch("מדוע מספר הנסיגות הכולל ב-KMP לכל היותר $n$?",
           "$q$ גדל לכל היותר ב-$1$ לכל תו של הטקסט, כל נסיגה מקטינה אותו, והוא אף פעם לא שלילי",
           ["כי כל תו של הטקסט גורם לנסיגה אחת לכל היותר", "כי $\\pi$ מכילה $m$ ערכים בלבד", "כי $m<n$"], 1,
           "בהרצות נמצאו תווים שגורמים ליותר מנסיגה אחת, ובכל זאת הסכום הכולל תמיד $\\le n$ (נבדק על $20000$ קלטים)."),
        txt("מהי סיבוכיות הזמן הכוללת, כפונקציה של גודל הקלט? (למשל `O(n)`)", ["O(n)", "O(n+m)"],
            "$O(m)$ להיפוך ול-$\\pi$ ו-$O(n)$ לחיפוש, סה\"כ $O(n+m)=O(n)$."),
        txt("מהי סיבוכיות המקום? (למשל `O(1)`)", ["O(m)"], "המחרוזת ההפוכה ומערך $\\pi$ בגודל $m$."),
    ],
    stepsSource="ai-draft")

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
