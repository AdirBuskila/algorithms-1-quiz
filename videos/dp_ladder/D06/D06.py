# -*- coding: utf-8 -*-
"""D06 · סיבוכיות זמן ומקום — video script (build: tools/video/vid.py D06).

Source: courses/dp_ladder/C06.js (lesson + goal). Exam anchors: 26A-B-Q1c (time and space of the DP for the hotel
journey: (n+1)(t+1) cells, O(n) work per cell, so O(n²t); space O(nt), or O(n) for the value alone), with its warm-up
26A-B-Q1a (effort 300 for stops p2, p4) to set up the problem. No guided quiz uses them.
Not used on purpose: the C06 quiz (LCS of three sequences, word cutting O(n²), two rows of a 6×9 LCS, the naive call
count c(3,3)=39, squares Θ(N√N)) and its bank question 25A-A-Q2c, and the boss 25A-C-Q1b (alignment complexity).
The examples (a two-index table with O(1) per cell; the jump game with O(n) per cell) are generic. Every count and
every table value is computed below; the hotel table is compared with a brute force over all sets of stops.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_dp_ladder as w

# ---------------------------------------------------------------- data (verified)
NR, NC = 4, 6                                          # a two-index table with (n+1)(m+1) cells, O(1) each
assert (NR + 1) * (NC + 1) == 35 and 2 * (NC + 1) == 14

NJ = 8                                                 # jumps when every A[i] is large: cell i reads n - i cells
reads = sum(NJ - i for i in range(1, NJ))
assert reads == NJ * (NJ - 1) // 2 == 28

# exam 26A-B-Q1a / Q1c
Qa, Qc = BANK["26A-B-Q1a"], BANK["26A-B-Q1c"]
assert "p_2" in Qa["question"] and "סיבוכיות" in Qc["question"]
assert Qa.get("correctId") is None and Qc.get("correctId") is None
n, t = 6, 3
p = [5 * i for i in range(n + 1)]                      # p_0 = s = 0, hotels every 5 km, p_6 = f = 30
O, ops = w.hotels(p, t)
assert all(O[i, j] == w.hotels_bf(p, i, j) for i in range(1, n + 1) for j in range(1, t + 1))
assert O[n, t] == 300 == (10 ** 2) * 3                 # stops p2 = 10 and p4 = 20: three days of 10 km
assert ops == t * n * (n + 1) // 2 == 63               # one step per l < i, for every i and every j
assert [O[i, 2] for i in range(n + 1)] == [0, 25, 50, 125, 200, 325, 450]
assert O[4, 2] == min(O[l, 1] + (p[4] - p[l]) ** 2 for l in range(4)) == 200

# ---------------------------------------------------------------- widgets
GT = w.Grid("gt", ["0"] + [str(i) for i in range(1, NR + 1)], ["0"] + [str(j) for j in range(1, NC + 1)],
            {}, cw=84, ch=64, fs=30)
GJ = w.Grid("gj", ["C"], [str(i) for i in range(1, NJ + 1)], {}, cw=84, ch=66, fs=30)
fmt = lambda v: "∞" if v == float("inf") else str(v)
GH = w.Grid("gh", [str(j) for j in range(t + 1)], [str(i) for i in range(n + 1)],
            {(j, i): fmt(O[i, j]) for j in range(t + 1) for i in range(n + 1)},
            given={(j, i) for j in range(t + 1) for i in range(n + 1)}, cw=96, ch=62, fs=30, corner="j\\i")

row = lambda G, r, ncols: [f"{G.pfx}-dep-{r}-{c}" for c in range(ncols)]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("כמעט בכל שאלת תכנות דינמי במבחן יש סעיף של זמן ומקום."),
    P("בסרטון הזה נראה איך מחשבים אותם בשתי שורות של נימוק, ואיפה נופלים.", hold=0.4),
], stage='<div class="kicker">D06 · תכנות דינמי</div><h1>סיבוכיות זמן ומקום</h1>'
         '<p>מספר התאים כפול העבודה לתא, וחיסכון במקום כשלא משחזרים.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("הזמן של תכנות דינמי הוא מכפלה של שני מספרים: כמה תאים יש בטבלה, וכמה עבודה דורש תא אחד.", do=show("i-1")),
    P("את העבודה לתא קוראים מהנוסחה: כמה תאים היא קוראת. כלומר, כמה חצים יוצאים מהתא.", do=show("i-2")),
    P("והמקום הוא גודל הטבלה. אלא אם צריך רק את הערך, ואז אפשר לשמור רק את השורות שהנוסחה קוראת.", do=show("i-3")),
    P("אבל מי שצריך לשחזר את הפתרון עצמו, צריך את כל הטבלה.", do=show("i-4"), hold=0.3),
], stage='<div class="dl-stack">'
         + st.card("i-1", "rule", "🔑 זמן = (מספר התאים) × (עבודה לתא)")
         + st.card("i-2", "ex", "עבודה לתא = כמה תאים הנוסחה קוראת")
         + st.card("i-3", "rule", "🔑 מקום = הטבלה, או רק השורות שהנוסחה קוראת")
         + "</div>",
   panel=st.card("i-4", "trap", "⚠️ שחזור הפתרון צריך את <b>כל</b> הטבלה"))

two_ph = [
    P("טבלה עם שני אינדקסים, כמו בתת-סדרה משותפת של מחרוזות באורכים $n$ ו-$m$.", do=show("t-g"),
      say="טבלה עם שני אינדקסים, כמו בתת סדרה משותפת של מחרוזות באורכים אֶן ואֶם."),
    P("יש בה $n+1$ כפול $m+1$ תאים. כאן חמש כפול שבע: 35 תאים.", do=show("t-1"),
      say="יש בה, בסוגריים, אֶן ועוד אחת, כפול, בסוגריים, אֶם ועוד אחת, תאים. כאן חמש כפול שבע: שלושים וחמישה תאים."),
    P("כל תא קורא שלושה שכנים: מעליו, משמאלו ובאלכסון. זה זמן קבוע.", do=GT.step((3, 4), [(2, 3), (2, 4), (3, 3)], value=False)),
    P("ולכן הזמן הוא $O(nm)$.", do=show("t-2"), say="ולכן הזמן הוא או של אֶן כפול אֶם."),
    P("ומה עם המקום? שורה $i$ קוראת רק את שורה $i-1$, ואת עצמה.",
      do=GT.off() + show(*row(GT, 2, NC + 1), *row(GT, 3, NC + 1)),
      say="ומה עם המקום? שורה אַיי קוראת רק את שורה אַיי פחות אחת, ואת עצמה."),
    P("אם צריך רק את הערך, מספיקות שתי שורות: 14 תאים במקום 35. כלומר $O(m)$.", do=show("t-3"),
      say="אם צריך רק את הערך, מספיקות שתי שורות: ארבעה עשר תאים במקום שלושים וחמישה. כלומר או של אֶם."),
    P("אבל כדי לשחזר את הפתרון הולכים לאחור דרך כל השורות, ולכן שם המקום הוא $O(nm)$.", do=show("t-4"),
      say="אבל כדי לשחזר את הפתרון הולכים לאחור דרך כל השורות, ולכן שם המקום הוא או של אֶן כפול אֶם."),
]
two = Scene("table", "שני אינדקסים", two_ph,
            stage=f'<div class="dl-stack"><div id="t-g" class="h">{GT.html()}</div></div>',
            panel=st.card("t-1", "ex", "$(n+1)(m+1)$ תאים")
                  + st.card("t-2", "rule", "🔑 זמן: $O(1)$ לתא → $O(nm)$")
                  + st.card("t-3", "rule", "🔑 רק הערך: שתי שורות → $O(m)$")
                  + st.card("t-4", "trap", "⚠️ שחזור: כל הטבלה → $O(nm)$"))

jp_ph = [
    P("אבל העבודה לתא לא תמיד קבועה. נחזור לבעיית הקפיצות, שבה $C(i)$ הוא המינימום מהמקום $i$ עד הסוף.", do=show("j-g"),
      say="אבל העבודה לתא לא תמיד קבועה. נחזור לבעיית הקפיצות, שבה סִי שֶל אַיי הוא המינימום מהמקום אַיי עד הסוף."),
    P("יש רק $n$ תאים, אבל התא $C(i)$ קורא את כל התאים שאפשר לקפוץ אליהם.",
      do=GJ.step((0, 1), [(0, k) for k in range(2, NJ)], value=False),
      say="יש רק אֶן תאים, אבל התא סִי שֶל אַיי קורא את כל התאים שאפשר לקפוץ אליהם."),
    P("כשהמספרים במערך גדולים, זה עד $n$ תאים לכל תא. כאן, עם שמונה מקומות, 28 קריאות.", do=show("j-1"),
      say="כשהמספרים במערך גדולים, זה עד אֶן תאים לכל תא. כאן, עם שמונה מקומות, עשרים ושמונה קריאות."),
    P("ולכן הזמן הוא $O(n^2)$, ולא $O(n)$. המקום הוא $O(n)$.", do=show("j-2"),
      say="ולכן הזמן הוא או של אֶן בריבוע, ולא או של אֶן. המקום הוא או של אֶן."),
    P("וזו המלכודת: לספור תאים ולשכוח שתא אחד עושה לולאה.", do=GJ.off() + show("j-t"), hold=0.3),
]
jp = Scene("loop", "עבודה לתא", jp_ph,
           stage=f'<div class="dl-stack"><div id="j-g" class="h">{GJ.html()}</div></div>',
           panel=st.card("j-1", "ex", "$\\sum_i (n-i)=\\frac{n(n-1)}{2}$ קריאות")
                 + st.card("j-2", "rule", "🔑 $n$ תאים × $O(n)$ לתא = $O(n^2)$")
                 + st.card("j-t", "trap", "⚠️ לולאה בתוך תא: לא $O(1)$"))

ex_ph = [
    P("שאלה ממבחן. הולכים בקו ישר מהנקודה 0 אל הסוף, ולנים כל לילה באחד המלונות שלאורך הדרך.", do=show("x-img")),
    P("המאמץ של יום הוא ריבוע המרחק שהולכים בו, ויש לכל היותר $t$ ימים. רוצים מאמץ כולל מינימלי.",
      say="המאמץ של יום הוא ריבוע המרחק שהולכים בו, ויש לכל היותר טִי ימים. רוצים מאמץ כולל מינימלי."),
    P("סעיף ראשון: מלונות כל 5 קילומטר, שלושה ימים, ולנים במלון 2 ובמלון 4. מה המאמץ?"),
    P("כל יום הולכים 10 קילומטר, כלומר מאמץ של 100. שלושה ימים: 300.", do=show("x-a")),
    P("הנוסחה: $OPT(i,j)$ הוא המאמץ המינימלי להגיע למלון $i$ תוך לכל היותר $j$ ימים.", do=show("x-d"),
      say="הנוסחה: אוֹפְּט שֶל אַיי וגֵ'יי הוא המאמץ המינימלי להגיע למלון אַיי, תוך לכל היותר גֵ'יי ימים."),
    P("היום האחרון מתחיל במלון $l$ כלשהו לפני $i$. לכן לוקחים מינימום על כל $l$.", do=show("x-f"),
      say="היום האחרון מתחיל במלון אֶל כלשהו לפני אַיי. לכן לוקחים מינימום על כל אֶל."),
    P("עכשיו הסיבוכיות. יש $n+1$ כפול $t+1$ תאים.", do=hide("x-img") + show("x-g"),
      say="עכשיו הסיבוכיות. יש, בסוגריים, אֶן ועוד אחת, כפול, בסוגריים, טִי ועוד אחת, תאים."),
    P("אבל תא אחד, למשל מלון 4 ביומיים, קורא את **כל** המלונות שלפניו בשורה הקודמת.",
      do=GH.step((2, 4), [(1, 0), (1, 1), (1, 2), (1, 3)], value=False)),
    P("זה $O(n)$ עבודה לתא. ולכן הזמן הוא $O(n^2 t)$, ולא $O(nt)$.", do=show("x-1"),
      say="זה או של אֶן עבודה לתא. ולכן הזמן הוא או של אֶן בריבוע כפול טִי, ולא או של אֶן כפול טִי."),
    P("אם נספור את כל המעברים על $l$ בדוגמה שלנו, נקבל 63, כלומר שלוש כפול 21.", do=show("x-2"),
      say="אם נספור את כל המעברים על אֶל בדוגמה שלנו, נקבל שישים ושלושה, כלומר שלוש כפול עשרים ואחת."),
    P("והמקום: כל הטבלה, $O(nt)$, אם רוצים לשחזר איפה ללון.", do=GH.off() + show("x-3"),
      say="והמקום: כל הטבלה, או של אֶן כפול טִי, אם רוצים לשחזר איפה ללון."),
    P("אבל שורה $j$ קוראת רק את שורה $j-1$. לכן בשביל הערך בלבד מספיקות שתי שורות: $O(n)$.",
      do=show(*row(GH, 1, n + 1), *row(GH, 2, n + 1)) + show("x-4"),
      say="אבל שורה גֵ'יי קוראת רק את שורה גֵ'יי פחות אחת. לכן בשביל הערך בלבד מספיקות שתי שורות: או של אֶן."),
    P("ושימו לב לתשובה בפינה: 300, בדיוק המאמץ מהסעיף הראשון.", do=GH.path([(3, 6)]), hold=0.5),
]
exam = Scene("exam", "שאלה ממבחן", ex_ph,
             stage='<div class="dl-stack">'
                   + w.eqs("x", ["$OPT(i,j)=\\min_{0\\le l<i}\\Bigl(OPT(l,j-1)+(p_i-p_l)^2\\Bigr)$"], 34).replace('id="x-0"', 'id="x-f"')
                   + '<div class="swap" style="--swap-h:420px">'
                   + f'<div id="x-img" class="h">{st.raster("x-r", "images/exams/26A-B-Q1-route.png", 640, (2172, 1302))}</div>'
                   + f'<div id="x-g" class="h">{GH.html()}</div>'
                   + "</div>"
                   + st.card("x-2", "ex", "בדוגמה: $63=3\\cdot(1+\\dots+6)$ מעברים")
                   + "</div>",
             panel=f'<div class="dl-q"><span class="qid">{Qa["id"]} · {Qc["id"]}</span>מלונות $p_1<\\dots<p_n=f$, '
                   'לכל היותר $t$ ימים, מאמץ יומי $d^2$. מהי סיבוכיות הזמן והמקום?</div>'
                   + st.card("x-a", "ex", "$p_i=5i$: $10^2+10^2+10^2=300$")
                   + st.card("x-d", "plain", "$OPT(i,j)$: מינימום עד מלון $i$ תוך לכל היותר $j$ ימים")
                   + st.card("x-1", "rule", "🔑 זמן: $(n+1)(t+1)$ תאים × $O(n)$ = $O(n^2t)$")
                   + st.card("x-3", "plain", "מקום עם שחזור: $O(nt)$")
                   + st.card("x-4", "rule", "🔑 רק הערך: שתי שורות, $O(n)$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: זמן הוא מספר התאים כפול העבודה לתא.", do=show("s-1")),
    P("את העבודה לתא קוראים מהנוסחה. מינימום על $l$ כלשהו הוא לולאה, ולא זמן קבוע.", do=show("s-2"),
      say="את העבודה לתא קוראים מהנוסחה. מינימום על אֶל כלשהו הוא לולאה, ולא זמן קבוע."),
    P("מקום הוא הטבלה. בלי שחזור, רק השורות שהנוסחה קוראת.", do=show("s-3")),
    P("ועם שחזור, כל הטבלה. נתראה ברמה הבאה.", do=show("s-4"), hold=0.6),
], stage='<div class="dl-stack">'
         + st.card("s-1", "rule", "🔑 זמן = תאים × עבודה לתא")
         + st.card("s-2", "trap", "⚠️ $\\min$ על $l$ = לולאה בתוך התא")
         + "</div>",
   panel=st.card("s-3", "rule", "🔑 רק ערך: השורות שהנוסחה קוראת")
         + st.card("s-4", "ex", "שחזור: כל הטבלה"))

VIDEO = Video("D06", "dp_ladder", "סיבוכיות זמן ומקום", [title, idea, two, jp, exam, recap],
              bank={"26A-B-Q1a": None, "26A-B-Q1c": None})
