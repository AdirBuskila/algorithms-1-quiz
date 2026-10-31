# -*- coding: utf-8 -*-
"""D03 · צורת הטבלה וסדר המילוי — video script (build: tools/video/vid.py D03).

Source: courses/dp_ladder/C03.js (lesson + goal). Exam anchor: 23A-A-Q1a (most valuable path in a lower-triangular
array, open question): the table is a triangle, it is filled row by row, the edges j=1 and j=i have one predecessor,
and the answer is the maximum of the bottom row. No guided quiz uses it.
Not used on purpose: the C03 quiz (LCS cell counts 5×7 and 4×5×6, the palindrome fill order, the LCS fill algorithm,
the reads of F(12), the triangle of length 6) and the bank questions of the boss C09; no palindrome or LCS table is
filled here.
The grid example (minimum path sum) and the small jump array are original. Every value is computed by w_dp_ladder and
compared with a brute force below.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_dp_ladder as w

# ---------------------------------------------------------------- data (verified)
G = [[1, 3, 1, 2], [1, 5, 1, 3], [4, 2, 1, 1]]          # minimum path sum, steps right or down
S = w.grid_min(G)
assert all(S[i, j] == w.grid_min_bf(G, i, j) for i in range(3) for j in range(4))
assert [[S[i, j] for j in range(4)] for i in range(3)] == [[1, 4, 5, 7], [2, 7, 6, 9], [6, 8, 7, 8]]
assert S[1, 1] == G[1][1] + min(S[0, 1], S[1, 0]) == 7 and S[1, 2] == G[1][2] + min(S[0, 2], S[1, 1]) == 6
assert S[2, 3] == 8 and S[2, 3] == G[2][3] + min(S[1, 3], S[2, 2])

J = [2, 3, 1, 1, 2]                                   # jumps from i to the end: the arrows point right
CJ = w.jumps_to_end(J)
assert CJ[1:] == [w.jumps_bf(J, i, 5) for i in range(1, 6)] == [2, 1, 2, 1, 0]

# exam 23A-A-Q1a
Q = BANK["23A-A-Q1a"]
assert "המסלול היקר" in Q["question"] and Q.get("correctId") is None
TA = [[1, 0, 0], [3, 2, 0], [4, 10, 12]]
M = w.tri_path(TA)
assert all(M[i, j] == w.tri_path_bf(TA, i, j) for i in range(1, 4) for j in range(1, i + 1))
assert [M[k] for k in [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3)]] == [1, 4, 3, 8, 14, 15]
assert max(M[3, j] for j in (1, 2, 3)) == 15 == 1 + 2 + 12
assert M[3, 2] == 10 + max(M[2, 1], M[2, 2]) and M[3, 3] == 12 + M[2, 2]
# the trap: the corner is not always the answer (the same array with 1 in the corner)
TB = [[1, 0, 0], [3, 2, 0], [4, 10, 1]]
MB = w.tri_path(TB)
assert MB[3, 3] == 4 and max(MB[3, j] for j in (1, 2, 3)) == 14 == MB[3, 2]
n = 3
assert n * (n + 1) // 2 == 6 == len(M)

# ---------------------------------------------------------------- widgets
GS = w.Grid("gs", ["1", "2", "3"], ["1", "2", "3", "4"],
            {(i, j): str(S[i, j]) for i in range(3) for j in range(4)}, cw=92, ch=70, fs=34, corner="S")
GG = w.Grid("gg", ["1", "2", "3"], ["1", "2", "3", "4"],
            {(i, j): str(G[i][j]) for i in range(3) for j in range(4)}, given={(i, j) for i in range(3) for j in range(4)},
            cw=70, ch=58, fs=30, corner="A")
GJ = w.Grid("gj", ["A", "C"], [str(i) for i in range(1, 6)],
            {**{(0, i): str(J[i]) for i in range(5)}, **{(1, i): str(CJ[i + 1]) for i in range(5)}},
            given={(0, i) for i in range(5)}, cw=92, ch=68, fs=34)
GA = w.Grid("ga", ["1", "2", "3"], ["1", "2", "3"], {(i, j): str(TA[i][j]) for i in range(3) for j in range(3)},
            given={(i, j) for i in range(3) for j in range(3)}, cw=70, ch=58, fs=30, corner="A")
GM = w.Grid("gm", ["1", "2", "3"], ["1", "2", "3"], {(i - 1, j - 1): str(M[i, j]) for (i, j) in M},
            void={(i, j) for i in range(3) for j in range(3) if j > i}, cw=100, ch=76, fs=36, corner="M")
m = lambda i, j: (i - 1, j - 1)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("יש לנו נוסחה. עכשיו צריך להחליט איך נראית הטבלה, ובאיזה סדר ממלאים אותה."),
    P("נראה טבלה מלבנית, טבלה שממלאים מהסוף להתחלה, וטבלה משולשת משאלת מבחן.", hold=0.4),
], stage='<div class="kicker">D03 · תכנות דינמי</div><h1>צורת הטבלה וסדר המילוי</h1>'
         '<p>גודל הטבלה, מיקום התשובה, וסדר מילוי שבו כל תא תלוי רק בתאים שכבר חושבו.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("אחרי הנוסחה עונים על ארבע שאלות. ראשונה: כמה ערכים יש לכל פרמטר. זה גודל הטבלה.", do=show("i-1")),
    P("שנייה: מה יש בכל תא. בדיוק מה שההגדרה במילים אומרת.", do=show("i-2")),
    P("שלישית: באיזה סדר ממלאים. ורביעית: באיזה תא נמצאת התשובה.", do=show("i-3", "i-4")),
    P("איך מוצאים סדר? מציירים חץ מכל תא אל התאים שהנוסחה שלו קוראת.", do=show("i-r")),
    P("סדר חוקי הוא סדר שבו כשמגיעים לתא, כל התאים שהחצים שלו מצביעים עליהם כבר מולאו.", hold=0.3),
    P("קריאה לתא שעוד לא מולא היא הטעות הקלאסית.", do=show("i-t")),
], stage='<div class="dl-stack">'
         + st.card("i-1", "ex", "1. <b>גודל</b>: כמה ערכים לכל פרמטר")
         + st.card("i-2", "ex", "2. <b>מה בתא</b>: מה שההגדרה אומרת")
         + st.card("i-3", "ex", "3. <b>סדר המילוי</b>")
         + st.card("i-4", "ex", "4. <b>איפה התשובה</b>")
         + "</div>",
   panel=st.card("i-r", "rule", "🔑 חץ מכל תא אל התאים שהוא קורא. כשמגיעים לתא, כל החצים שלו מצביעים על תאים מלאים.")
         + st.card("i-t", "trap", "⚠️ לקרוא תא שעוד לא מולא"))

gr_ph = [
    P("טבלה מלבנית: לוח מספרים, ומסלול מהפינה השמאלית העליונה שזז רק ימינה או למטה.", do=show("g-a")),
    P("רוצים את הסכום המינימלי של מסלול. $S(i,j)$ הוא הסכום המינימלי של מסלול שמגיע לתא $(i,j)$.", do=show("g-d"),
      say="רוצים את הסכום המינימלי של מסלול. אֶס שֶל אַיי וגֵ'יי הוא הסכום המינימלי של מסלול שמגיע לתא אַיי, גֵ'יי."),
    P("לתא מגיעים מלמעלה או משמאל, ולכן הנוסחה קוראת שני תאים: את זה שמעליו ואת זה שמשמאלו.", do=show("g-f")),
    P("גודל הטבלה כגודל הלוח: שלוש שורות וארבע עמודות. בתא הראשון אין ממה לבוא, ולכן הוא 1.",
      do=show("g-g") + GS.step((0, 0))),
    P("השורה הראשונה מגיעה רק משמאל: 4, 5, 7.", do=GS.vals_do([(0, 1), (0, 2)]) + GS.step((0, 3), [(0, 2)])),
    P("בשורה השנייה, התא $(2,2)$ קורא את 4 שמעליו ואת 2 שמשמאלו. הקטן הוא 2, ועם הערך 5 שבתא עצמו יוצא 7.",
      do=GS.vals_do([(1, 0)]) + GS.step((1, 1), [(0, 1), (1, 0)]),
      say="בשורה השנייה, התא שתיים, שתיים קורא את ארבע שמעליו ואת שתיים שמשמאלו. הקטן הוא שתיים, ועם הערך חמש שבתא עצמו יוצא שבע."),
    P("שני החצים מצביעים על תאים שכבר מולאו. לכן ממלאים שורה אחרי שורה, ובכל שורה משמאל לימין.", do=show("g-o")),
    P("ממשיכים כך עד הסוף, והתשובה בפינה הימנית התחתונה: 8.",
      do=GS.vals_do([(1, 2), (1, 3), (2, 0), (2, 1), (2, 2)]) + GS.step((2, 3), [(1, 3), (2, 2)]), hold=0.3),
]
gr = Scene("grid", "טבלה מלבנית", gr_ph,
           stage=f'<div class="dl-stack"><div id="g-g" class="h">{GS.html()}</div>'
                 + w.eqs("g", ["$S(i,j)=A[i][j]+\\min\\bigl(S(i-1,j),\\ S(i,j-1)\\bigr)$"], 36).replace('id="g-0"', 'id="g-f"')
                 + "</div>",
           panel=f'<div id="g-a" class="h">{GG.html()}</div>'
                 + st.card("g-d", "ex", "$S(i,j)$ = הסכום המינימלי של מסלול אל $(i,j)$")
                 + st.card("g-o", "rule", "🔑 שורה אחרי שורה, משמאל לימין"))

rv_ph = [
    P("אבל הסדר לא תמיד משמאל לימין. נזכרים בבעיית הקפיצות: $C(i)$ הוא המינימום מהמקום $i$ עד הסוף.", do=show("v-g"),
      say="אבל הסדר לא תמיד משמאל לימין. נזכרים בבעיית הקפיצות: סִי שֶל אַיי הוא המינימום מהמקום אַיי עד הסוף."),
    P("הנוסחה של $C(i)$ קוראת את התאים **שמימין** לו, כי קופצים קדימה.", do=GJ.step((1, 4)) + GJ.step((1, 1), [(1, 2), (1, 3), (1, 4)], value=False),
      say="הנוסחה של סִי שֶל אַיי קוראת את התאים שמימין לו, כי קופצים קדימה."),
    P("החצים מצביעים ימינה, ולכן ממלאים מימין לשמאל: מהסוף, שבו הערך 0, אל ההתחלה.",
      do=GJ.off() + show(GJ.v((1, 4))) + show("v-r")),
    P("מהמקום 4 קפיצה אחת, מ-3 שתיים, מ-2 אחת, ומהמקום הראשון שתיים.",
      do=GJ.vals_do([(1, 3), (1, 2), (1, 1)]) + GJ.step((1, 0), [(1, 1), (1, 2)])),
    P("והתשובה היא $C(1)$, בקצה השמאלי, כלומר בתא האחרון שממלאים.", do=GJ.off() + show("v-a"),
      say="והתשובה היא סִי של אחת, בקצה השמאלי, כלומר בתא האחרון שממלאים."),
]
rv = Scene("reverse", "סדר הפוך", rv_ph,
           stage=f'<div class="dl-stack"><div id="v-g" class="h">{GJ.html()}</div></div>',
           panel=st.card("v-r", "rule", "🔑 החצים ימינה → ממלאים מימין לשמאל")
                 + st.card("v-a", "ex", "התשובה $C(1)$: התא האחרון שממלאים"))

ex_ph = [
    P("שאלה ממבחן. במערך ריבועי, מעל האלכסון יש רק אפסים.", do=show("x-a")),
    P("מסלול מתחיל בתא העליון, ובכל צעד יורד שורה: ישר למטה, או למטה וימינה."),
    P("הוא נגמר בשורה התחתונה, ורוצים את המסלול שסכומו הגדול ביותר."),
    P("ההגדרה: $M(i,j)$ הוא הערך המקסימלי של מסלול מהתא העליון אל התא $(i,j)$.", do=show("x-d"),
      say="ההגדרה: אֶם שֶל אַיי וגֵ'יי הוא הערך המקסימלי של מסלול מהתא העליון אל התא אַיי, גֵ'יי."),
    P("אל $(i,j)$ מגיעים מהתא שמעליו או מהתא שמעליו ומשמאל. לכן לוקחים את הגדול מביניהם ומוסיפים את $A[i,j]$.",
      do=show("x-f"),
      say="אל אַיי, גֵ'יי מגיעים מהתא שמעליו, או מהתא שמעליו ומשמאל. לכן לוקחים את הגדול מביניהם, ומוסיפים את הערך שבתא."),
    P("צורת הטבלה: כל צעד מוסיף שורה, ולכל היותר עמודה. לכן תמיד $j\\le i$: הטבלה היא **משולש**.", do=show("x-g"),
      say="צורת הטבלה: כל צעד מוסיף שורה, ולכל היותר עמודה. לכן תמיד גֵ'יי קטן או שווה לאַיי: הטבלה היא משולש."),
    P("בשוליים יש רק קודם אחד: בעמודה הראשונה רק מלמעלה, ועל האלכסון רק באלכסון.", do=show("x-e", "x-e2")),
    P("הסדר: כל תא קורא רק את השורה שמעליו. לכן ממלאים שורה אחרי שורה.", do=GM.step(m(1, 1))),
    P("בשורה השנייה: 3 ועוד 1 זה 4, ו-2 ועוד 1 זה 3.", do=GM.step(m(2, 1), [m(1, 1)]) + GM.vals_do([m(2, 2)])),
    P("בשורה השלישית: בעמודה הראשונה 4 ועוד 4, כלומר 8.", do=GM.step(m(3, 1), [m(2, 1)])),
    P("באמצע: 10 ועוד המקסימום של 4 ו-3, כלומר 14.", do=GM.step(m(3, 2), [m(2, 1), m(2, 2)])),
    P("ועל האלכסון: 12 ועוד 3, כלומר 15.", do=GM.step(m(3, 3), [m(2, 2)])),
    P("איפה התשובה? המסלול יכול להיגמר בכל תא של השורה התחתונה, ולכן לוקחים את המקסימום שלה: 15.",
      do=GM.off() + show("x-ans") + GM.path([m(1, 1), m(2, 2), m(3, 3)])),
    P("כאן המקסימום יצא בפינה, אבל זה מקרה. אם בפינה היה 1, הערך שם היה 4, והתשובה 14.", do=show("x-t"), hold=0.5),
]
exam = Scene("exam", "שאלה ממבחן", ex_ph,
             stage='<div class="dl-stack">'
                   + w.eqs("x", ["$M(i,j)=A[i,j]+\\max\\bigl(M(i-1,j-1),\\ M(i-1,j)\\bigr)$",
                                 "$M(1,1)=A[1,1],\\quad M(i,1)=A[i,1]+M(i-1,1)$", "$M(i,i)=A[i,i]+M(i-1,i-1)$"], 32)
                   .replace('id="x-0"', 'id="x-f"').replace('id="x-1"', 'id="x-e"').replace('id="x-2"', 'id="x-e2"')
                   + f'<div id="x-g" class="h">{GM.html()}</div>'
                   + st.card("x-ans", "rule", "🔑 התשובה: $\\max_j M(n,j)=15$, המסלול $1\\to2\\to12$")
                   + "</div>",
             panel=f'<div class="dl-q"><span class="qid">{Q["id"]}</span>מסלול מ-$[1,1]$ אל השורה התחתונה, '
                   'בכל צעד אל $[i+1,j]$ או $[i+1,j+1]$. הציגו נוסחה לערך המסלול היקר ביותר.</div>'
                   + f'<div id="x-a" class="h">{GA.html()}</div>'

                   + st.card("x-d", "ex", "$M(i,j)$ = מקסימום מסלול אל $[i,j]$")
                   + st.card("x-t", "trap", "⚠️ התשובה היא מקסימום השורה, לא הפינה"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: לכל פרמטר סופרים את הערכים שלו. לפעמים רק חלק מהמלבן בשימוש, כמו משולש.", do=show("s-1")),
    P("מציירים חץ מכל תא אל התאים שהוא קורא, וממלאים כך שכל חץ מצביע על תא מלא.", do=show("s-2")),
    P("החצים למעלה ושמאלה: שורה אחרי שורה. החצים ימינה: מימין לשמאל.", do=show("s-3")),
    P("ואת התשובה קובעת ההגדרה: תא אחד, או מקסימום על שורה. נתראה ברמה הבאה.", do=show("s-4"), hold=0.6),
], stage='<div class="dl-stack">'
         + st.card("s-1", "rule", "🔑 גודל: מספר הערכים של כל פרמטר")
         + st.card("s-2", "rule", "🔑 סדר: כל חץ מצביע על תא מלא")
         + "</div>",
   panel=st.card("s-3", "ex", "↖ שורה אחרי שורה · → מימין לשמאל")
         + st.card("s-4", "trap", "⚠️ התשובה: לפי ההגדרה, לא תמיד בפינה"))

VIDEO = Video("D03", "dp_ladder", "צורת הטבלה וסדר המילוי", [title, idea, gr, rv, exam, recap],
              bank={"23A-A-Q1a": None})
