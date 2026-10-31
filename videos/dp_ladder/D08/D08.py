# -*- coding: utf-8 -*-
"""D08 · תרמיל, ספירת תת-קבוצות ומקרה חסר — video script (build: tools/video/vid.py D08).

Source: courses/dp_ladder/C08.js (lesson + goal). Exam anchors: 26B-A-Q1b (the recurrence for the maximum profit of
tasks with times t_i under a total time T, a 0/1 knapsack, with both cases and the base) and 26B-A-Q1d (run it for
T=6 on the four tasks of the question: P(4,6)=11, tasks {1,4}). No guided quiz uses them.
Not used on purpose: the C08 quiz (items (2,3),(3,4),(4,5),(5,8) with W=9, subsets of {2,3,5,7,8} summing to 10,
the fill-in / find-the-bug code of the knapsack and of the interleaving check, {5,7,9} under 13) and the boss
25A-A-Q2a (interleaving). The code questions are not discussed; the "missing case" is shown on an original counting
example ({2,3,5}).
Every table value is computed below and compared with a brute force over all subsets.
"""
import itertools
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_dp_ladder as w

# ---------------------------------------------------------------- data (verified)
A = [2, 3, 5]                                          # counting subsets with sum exactly s
SM = 8
Cnt = [[0] * (SM + 1) for _ in range(len(A) + 1)]
Cnt[0][0] = 1
for i in range(1, len(A) + 1):
    for s in range(SM + 1):
        Cnt[i][s] = Cnt[i - 1][s] + (Cnt[i - 1][s - A[i - 1]] if A[i - 1] <= s else 0)
bf = lambda i, s: sum(1 for r in range(i + 1) for c in itertools.combinations(A[:i], r) if sum(c) == s)
assert all(Cnt[i][s] == bf(i, s) for i in range(len(A) + 1) for s in range(SM + 1))
assert Cnt[3][5] == 2 == Cnt[2][5] + Cnt[2][0]                 # {5} and {2,3}
assert Cnt[2][2] == Cnt[1][2] == 1 and A[1] > 2                 # 3 does not fit into 2: copy the row above
assert 2 - A[1] < 0                                             # without that case the formula reads Cnt(1, -1)

# exam 26B-A-Q1b / Q1d
Qb, Qd = BANK["26B-A-Q1b"], BANK["26B-A-Q1d"]
assert "רקורסיבית" in Qb["question"] and "T=6" in Qd["question"]
assert Qb.get("correctId") is None and Qd.get("correctId") is None
t, v, TT = [1, 2, 4, 5], [1, 3, 7, 10], 6
PT = w.knap(t, v, TT)
assert all(PT[i][c] == w.knap_bf(t, v, i, c) for i in range(5) for c in range(TT + 1))
assert PT == [[0] * 7, [0, 1, 1, 1, 1, 1, 1], [0, 1, 3, 4, 4, 4, 4], [0, 1, 3, 4, 7, 8, 10], [0, 1, 3, 4, 7, 10, 11]]
assert PT[3][6] == max(PT[2][6], v[2] + PT[2][2]) == 10 and PT[4][6] == max(PT[3][6], v[3] + PT[3][1]) == 11
assert PT[2][1] == PT[1][1] and t[1] > 1                         # task 2 (time 2) does not fit into 1
cells, take = w.knap_back(t, v, PT, TT)
assert take == [1, 4] and sum(t[k - 1] for k in take) == 6 and sum(v[k - 1] for k in take) == 11
assert cells == [(4, 6), (3, 1), (2, 1), (1, 1), (0, 0)]

# ---------------------------------------------------------------- widgets
GN = w.Grid("gn", ["∅", "2", "3", "5"], [str(s) for s in range(SM + 1)],
            {(i, s): str(Cnt[i][s]) for i in range(4) for s in range(SM + 1)},
            given={(0, s) for s in range(SM + 1)}, cw=84, ch=66, fs=32, corner="a\\s")
GP = w.Grid("gp", ["0", "1", "2", "3", "4"], [str(c) for c in range(TT + 1)],
            {(i, c): str(PT[i][c]) for i in range(5) for c in range(TT + 1)},
            given={(0, c) for c in range(TT + 1)}, cw=84, ch=62, fs=32, corner="i\\c")
GI = w.Grid("gi", ["t", "v"], ["1", "2", "3", "4"], {**{(0, k): str(t[k]) for k in range(4)},
                                                      **{(1, k): str(v[k]) for k in range(4)}},
            given={(r, k) for r in range(2) for k in range(4)}, cw=70, ch=54, fs=28, corner="task")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נפתור בעיות בצורת תרמיל: בוחרים פריטים, ולכל אחד יש משקל, ויש קיבולת."),
    P("נראה למה צריך שני פרמטרים, ואיך מוצאים מקרה שחסר בנוסחה. ובסוף, שאלת מבחן מלאה.", hold=0.4),
], stage='<div class="kicker">D08 · תכנות דינמי</div><h1>תרמיל, ספירת תת-קבוצות ומקרה חסר</h1>'
         '<p>בחירה עם משקל וקיבולת, ובדיקה שכל מקרה מכוסה בנוסחה.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("ההחלטה האחרונה היא: האם לקחת את הפריט האחרון?", do=show("i-1")),
    P("אבל אחרי שלוקחים אותו, נשארת פחות קיבולת. לכן צריך לזכור גם כמה פריטים נשארו וגם כמה מקום נשאר.", do=show("i-2")),
    P("שני פרמטרים: $i$, הפריטים הראשונים, ו-$c$, הקיבולת שנשארה.", do=show("i-3"),
      say="שני פרמטרים: אַיי, הפריטים הראשונים, וסִי, הקיבולת שנשארה."),
    P("ואיך מוצאים מקרה חסר? לכל תא שואלים: מה אם הפריט לא נכנס? מה אם האינדקס יוצא מהטווח?", do=show("i-r")),
    P("לכל תשובה צריכה להיות שורה בנוסחה.", hold=0.3),
], stage='<div class="dl-stack">'
         + st.card("i-1", "ex", "ההחלטה האחרונה: לקחת את הפריט האחרון, או לא")
         + st.card("i-2", "ex", "אחרי לקיחה: פחות קיבולת")
         + st.card("i-3", "rule", "🔑 שני פרמטרים: $i$ (פריטים) ו-$c$ (קיבולת)")
         + "</div>",
   panel=st.card("i-r", "trap", "⚠️ לכל תא: מה אם הפריט לא נכנס? מה אם יוצאים מהטווח?"))

cnt_ph = [
    P("דוגמה: כמה תת-קבוצות של 2, 3 ו-5 סכומן בדיוק $s$? הפריט האחרון נלקח, או לא.", do=show("n-g"),
      say="דוגמה: כמה תת קבוצות של שתיים, שלוש וחמש, סכומן בדיוק אֶס? הפריט האחרון נלקח, או לא."),
    P("שני המקרים זרים, ולכן מחברים: בלי הפריט, ועם הפריט וסכום קטן יותר.", do=show("n-f")),
    P("הבסיס: בלי פריטים, סכום 0 מתקבל בדרך אחת, הקבוצה הריקה. כל סכום אחר: אפס דרכים."),
    P("כשמוסיפים את 5, הסכום 5 מקבל 1 מהשורה שמעל, ועוד 1 מהסכום 0. כלומר 2: $\\{5\\}$ ו-$\\{2,3\\}$.",
      do=GN.vals_do([(1, s) for s in range(SM + 1)] + [(2, s) for s in range(SM + 1)]) + GN.step((3, 5), [(2, 5), (2, 0)]),
      say="כשמוסיפים את חמש, הסכום חמש מקבל אחת מהשורה שמעל, ועוד אחת מהסכום אפס. כלומר שתיים: חמש לבד, או שתיים ושלוש."),
    P("המקרה החסר: בשורה של 3, בסכום 2, המקרה \"לוקחים\" קורא את הסכום 2 פחות 3, כלומר מינוס 1: תא שלא קיים.",
      do=GN.vals_do([(3, s) for s in range(SM + 1)]) + GN.step((2, 2), [(1, 2)]) + show("n-t"),
      say="המקרה החסר: בשורה של שלוש, בסכום שתיים, המקרה של לוקחים קורא את הסכום שתיים פחות שלוש, כלומר מינוס אחת: תא שלא קיים."),
    P("כשהפריט לא נכנס, הנוסחה חייבת שורה משלה: מעתיקים את הערך שמעל.", do=show("n-c")),
]
cnt = Scene("count", "ספירה ומקרה חסר", cnt_ph,
            stage=f'<div class="dl-stack"><div id="n-g" class="h">{GN.html()}</div>'
                  + w.eqs("n", ["$\\mathrm{Cnt}(i,s)=\\mathrm{Cnt}(i-1,s)+\\mathrm{Cnt}(i-1,s-a_i)$"], 34).replace('id="n-0"', 'id="n-f"')
                  + "</div>",
            panel=st.card("n-t", "trap", "⚠️ $a_i>s$: הקריאה $\\mathrm{Cnt}(i-1,s-a_i)$ יוצאת מהטבלה")
                  + st.card("n-c", "rule", "🔑 $a_i>s$: $\\mathrm{Cnt}(i,s)=\\mathrm{Cnt}(i-1,s)$"))

ex_ph = [
    P("שאלה ממבחן. יש משימות, לכל אחת זמן ביצוע ורווח, ויש זמן כולל $T$.", do=show("x-i"),
      say="שאלה ממבחן. יש משימות, לכל אחת זמן ביצוע ורווח, ויש זמן כולל טִי."),
    P("כל משימה נבחרת לכל היותר פעם אחת, והזמנים לא עוברים את $T$. רוצים רווח מקסימלי.",
      say="כל משימה נבחרת לכל היותר פעם אחת, והזמנים לא עוברים את טִי. רוצים רווח מקסימלי."),
    P("ההגדרה: $P(i,c)$ הוא הרווח המקסימלי מהמשימות 1 עד $i$, כשסכום הזמנים **לכל היותר** $c$.", do=show("x-d"),
      say="ההגדרה: פִּי שֶל אַיי וסִי הוא הרווח המקסימלי מהמשימות אחת עד אַיי, כשסכום הזמנים לכל היותר סִי."),
    P("משימה $i$ לא נבחרה: נשארות המשימות שלפניה, עם אותו זמן.", do=show("x-1"),
      say="משימה אַיי לא נבחרה: נשארות המשימות שלפניה, עם אותו זמן."),
    P("נבחרה: מרוויחים את הרווח שלה, ולשאר נשאר זמן קטן יותר. גם השאר חייב להיות אופטימלי.", do=show("x-2")),
    P("והמקרה שאסור לשכוח: אם המשימה ארוכה מ-$c$, היא לא יכולה להיבחר, ונשאר רק המקרה הראשון.", do=show("x-3"),
      say="והמקרה שאסור לשכוח: אם המשימה ארוכה מסִי, היא לא יכולה להיבחר, ונשאר רק המקרה הראשון."),
    P("הבסיס: בלי משימות הרווח 0. והתשובה: $P(n,T)$.", do=show("x-b"),
      say="הבסיס: בלי משימות הרווח אפס. והתשובה: פִּי של אֶן וטִי."),
    P("עכשיו ההרצה, עם $T=6$. שורה 1: משימה של זמן 1 ורווח 1. מכל זמן מ-1 ומעלה מקבלים 1.",
      do=show("x-g") + GP.vals_do([(1, c) for c in range(TT + 1)]),
      say="עכשיו ההרצה, עם טִי שווה שש. שורה אחת: משימה של זמן אחת ורווח אחת. מכל זמן מאחת ומעלה מקבלים אחת."),
    P("שורה 2: משימה של זמן 2 ורווח 3. בזמן 1 היא לא נכנסת, ומעתיקים את 1 מלמעלה.",
      do=GP.vals_do([(2, 0)]) + GP.step((2, 1), [(1, 1)])),
    P("מזמן 3 ומעלה לוקחים את שתיהן: 4.", do=GP.vals_do([(2, c) for c in range(2, TT + 1)]) + GP.off()),
    P("שורה 3, זמן 6: בלי המשימה הערך הוא 4. איתה, 7 ועוד הערך בזמן 2 בשורה הקודמת, שהוא 3. יוצא 10.",
      do=GP.vals_do([(3, c) for c in range(TT)]) + GP.step((3, 6), [(2, 6), (2, 2)])),
    P("שורה 4, זמן 6: בלי המשימה הערך הוא 10. איתה, 10 ועוד הערך בזמן 1, שהוא 1. יוצא 11. זו התשובה.",
      do=GP.vals_do([(4, c) for c in range(TT)]) + GP.step((4, 6), [(3, 6), (3, 1)]) + show("x-ok")),
    P("ואיזו קבוצה? 11 שונה מ-10 שמעליו, ולכן משימה 4 נבחרה, וקופצים לזמן 1.", do=GP.off() + GP.path([(4, 6), (3, 1)])),
    P("בזמן 1 הערך לא משתנה עד שורה 1, ושם הוא עולה מ-0 ל-1: משימה 1 נבחרה. הקבוצה: משימות 1 ו-4.",
      do=GP.path([(2, 1), (1, 1), (0, 0)]) + show("x-s"), hold=0.5),
]
exam = Scene("exam", "שאלה ממבחן", ex_ph,
             stage='<div class="dl-stack">'
                   + w.eqs("x", ["$P(i,c)=\\max\\bigl(P(i-1,c),\\ v_i+P(i-1,c-t_i)\\bigr)\\quad (t_i\\le c)$",
                                 "$P(i,c)=P(i-1,c)\\quad (t_i>c),\\qquad P(0,c)=0$"], 32)
                   .replace('id="x-0"', 'id="x-f"').replace('id="x-1"', 'id="x-b"')
                   + f'<div id="x-g" class="h">{GP.html()}</div>'
                   + '<div class="dl-row">' + st.card("x-ok", "rule", "🔑 $P(4,6)=11$")
                   + st.card("x-s", "ex", "משימות 1 ו-4: זמן 6, רווח 11") + "</div>"
                   + "</div>",
             panel=f'<div class="dl-q"><span class="qid">{Qb["id"]} · {Qd["id"]}</span>משימות עם זמן $t_i$ ורווח '
                   '$v_i$, זמן כולל $T$. נוסחה לרווח המקסימלי, והרצה עבור $T=6$.</div>'
                   + f'<div id="x-i" class="h">{GI.html()}</div>'
                   + st.card("x-d", "ex", "$P(i,c)$: מקסימום מהמשימות $1..i$ בזמן לכל היותר $c$")
                   + '<div class="dl-row">' + st.card("x-1", "plain", "לא: $P(i-1,c)$")
                   + st.card("x-2", "plain", "כן: $v_i+P(i-1,c-t_i)$") + "</div>"
                   + st.card("x-3", "trap", "⚠️ $t_i>c$: רק $P(i-1,c)$")
                   )
# the formula lines appear with the cases
exam.phrases[3].do = exam.phrases[3].do + show("x-f")
exam.phrases[5].do = exam.phrases[5].do + show("x-b")

recap = Scene("recap", "סיכום", [
    P("לסיכום: בתרמיל ההחלטה האחרונה היא לקחת או לא, ולכן שני פרמטרים: פריטים וקיבולת.", do=show("s-1")),
    P("בספירה מחברים את שני המקרים, ובאופטימיזציה לוקחים מקסימום.", do=show("s-2")),
    P("ולכל תא שואלים מה אם הפריט לא נכנס. אם אין לזה שורה, הנוסחה חסרה. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage='<div class="dl-stack">'
         + st.card("s-1", "rule", "🔑 לקחת או לא → פרמטרים $i$ ו-$c$")
         + st.card("s-2", "rule", "🔑 ספירה: $+$ · אופטימיזציה: $\\max$")
         + "</div>",
   panel=st.card("s-3", "trap", "⚠️ פריט שלא נכנס: שורה משלו בנוסחה"))

VIDEO = Video("D08", "dp_ladder", "תרמיל, ספירת תת-קבוצות ומקרה חסר", [title, idea, cnt, exam, recap],
              bank={"26B-A-Q1b": None, "26B-A-Q1d": None})
