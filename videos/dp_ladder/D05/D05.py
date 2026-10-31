# -*- coding: utf-8 -*-
"""D05 · שחזור הפתרון לאחור — video script (build: tools/video/vid.py D05).

Source: courses/dp_ladder/C05.js (lesson + goal). Exam anchor: 23B-C-Q3b (painting houses: run the DP on the given
3×3 cost matrix, open question): the table R/B/G × houses is filled column by column, the minimum is read from the
last column, and the colouring itself is rebuilt backwards. No guided quiz uses it.
Not used on purpose: the C05 quiz (the LCS table of ACBBC/ABCA, its traceback, its tie at (4,3), the findbug code,
the 7 visited cells), the lesson's ABC/AC example, and every boss question of C09.
The LCS example (CABD/ACBD, a tie with two different correct answers) is original. Every value is computed by
w_dp_ladder and compared with a brute force below.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_dp_ladder as w

# ---------------------------------------------------------------- data (verified)
X, Y = "CABD", "ACBD"
L = w.lcs_table(X, Y)
assert all(L[i][j] == w.lcs_bf(X[:i], Y[:j]) for i in range(5) for j in range(5))
assert L[4][4] == 3 and w.all_lcs(X, Y) == {"ABD", "CBD"}
up_cells, up_got = w.lcs_back(X, Y, L, "up")
lf_cells, lf_got = w.lcs_back(X, Y, L, "left")
assert up_cells == [(4, 4), (3, 3), (2, 2), (1, 2), (0, 1)] and up_got == ["D", "B", "C"]
assert lf_cells == [(4, 4), (3, 3), (2, 2), (2, 1), (1, 0)] and lf_got == ["D", "B", "A"]
assert "".join(reversed(up_got)) == "CBD" and "".join(reversed(lf_got)) == "ABD"
assert X[3] == Y[3] and X[2] == Y[2] and X[1] != Y[1] and L[1][2] == L[2][1] == 1 == L[2][2]
assert X[0] == Y[1] and X[1] == Y[0]

# exam 23B-C-Q3b
Q = BANK["23B-C-Q3b"]
assert "14" in Q["question"] and Q.get("correctId") is None
COST = [(14, 2, 11), (11, 14, 5), (14, 3, 19)]                # house h: (R, B, G), as printed in the question
T = w.paint(COST)
best, arg = w.paint_bf(COST)
assert T == {"R": [14, 13, 21], "B": [2, 25, 10], "G": [11, 7, 32]}
assert min(T[c][2] for c in "RBG") == best == 10 == T["B"][2] and arg == ["B", "G", "B"]
assert T["B"][2] == COST[2][1] + T["G"][1] and T["G"][1] < T["R"][1]          # house 3 blue <- house 2 green
assert T["G"][1] == COST[1][2] + T["B"][0] and T["B"][0] < T["R"][0]          # house 2 green <- house 1 blue
assert COST[0][1] + COST[1][2] + COST[2][1] == 10
ROW = {"R": 0, "B": 1, "G": 2}

# ---------------------------------------------------------------- widgets
GL = w.Grid("gl", ["∅"] + list(X), ["∅"] + list(Y), {(i, j): str(L[i][j]) for i in range(5) for j in range(5)},
            given={(i, j) for i in range(5) for j in range(5)}, cw=88, ch=70, fs=34)
GP = w.Grid("gp", ["R", "B", "G"], ["1", "2", "3"], {(ROW[c], h): str(T[c][h]) for c in "RBG" for h in range(3)},
            cw=104, ch=74, fs=36)
GC = w.Grid("gc", ["R", "B", "G"], ["1", "2", "3"], {(k, h): str(COST[h][k]) for k in range(3) for h in range(3)},
            given={(k, h) for k in range(3) for h in range(3)}, cw=72, ch=56, fs=28, corner="cost")


def others(c, h):
    return [(ROW[o], h - 1) for o in "RBG" if o != c]


# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("הטבלה נותנת את **הערך** של הפתרון הטוב ביותר. אבל לפעמים מבקשים את הפתרון עצמו."),
    P("בסרטון הזה נלך בטבלה לאחור ונשחזר אותו, ובסוף נעשה את זה בשאלת מבחן.", hold=0.4),
], stage='<div class="kicker">D05 · תכנות דינמי</div><h1>שחזור הפתרון לאחור</h1>'
         '<p>לשחזר מהטבלה את הפתרון עצמו, לא רק את ערכו, ולזהות שחזור שגוי.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("מתחילים בתא של התשובה, ושואלים: **איזה מקרה** בנוסחה יצר את הערך הזה?", do=show("i-1")),
    P("המקרה הזה הוא ההחלטה האחרונה בפתרון. רושמים אותה, ועוברים לתא שהמקרה קרא.", do=show("i-2")),
    P("וכך ממשיכים עד הבסיס. ההחלטות נאספות מהסוף להתחלה, ולכן בסוף הופכים את הסדר.", do=show("i-3")),
    P("והשחזור צריך את הטבלה כולה, כי הוא קורא תאים מכל השורות.", do=show("i-4"), hold=0.3),
], stage='<div class="dl-stack">'
         + st.card("i-1", "rule", "🔑 בכל תא: <b>איזה מקרה</b> יצר את הערך?")
         + st.card("i-2", "ex", "רושמים את ההחלטה ועוברים לתא שהמקרה קרא")
         + st.card("i-3", "ex", "עד הבסיס, ואז הופכים את הסדר")
         + "</div>",
   panel=st.card("i-4", "trap", "⚠️ השחזור צריך את <b>כל</b> הטבלה"))

lcs_ph = [
    P("טבלת תת-הסדרה המשותפת של $CABD$ ושל $ACBD$ כבר מלאה. הערך בפינה הוא 3.", do=show("l-g") + GL.step((4, 4)),
      say="טבלת תת הסדרה המשותפת של סִי אֵיי בִּי דִּי, ושל אֵיי סִי בִּי דִּי, כבר מלאה. הערך בפינה הוא שלוש."),
    P("אבל איזו תת-סדרה? מתחילים בפינה: $D$ מול $D$, שווים.", do=GL.path([(4, 4)]),
      say="אבל איזו תת סדרה? מתחילים בפינה: דִּי מול דִּי, שווים."),
    P("הערך בא מהאלכסון ועוד אחד. לכן $D$ בתת-הסדרה. רושמים אותו ועולים באלכסון.", do=GL.step((4, 4), [(3, 3)]) + show("l-c1"),
      say="הערך בא מהאלכסון ועוד אחד. לכן דִּי בתת הסדרה. רושמים אותו ועולים באלכסון."),
    P("$B$ מול $B$: שוב שווים. רושמים $B$, ושוב באלכסון.", do=GL.path([(3, 3)]) + GL.step((3, 3), [(2, 2)]) + show("l-c2"),
      say="בִּי מול בִּי: שוב שווים. רושמים בִּי, ושוב באלכסון."),
    P("$A$ מול $C$: שונים. הערך בא מהשכן הגדול, אבל כאן שני השכנים שווים, 1 ו-1.",
      do=GL.path([(2, 2)]) + GL.step((2, 2), [(1, 2), (2, 1)]),
      say="אֵיי מול סִי: שונים. הערך בא מהשכן הגדול, אבל כאן שני השכנים שווים, אחת ואחת."),
    P("במצב כזה **כל בחירה נכונה**: שני השכנים שומרים את האורך המלא של מה שנשאר.", do=show("l-tie")),
    P("נעלה למעלה: שם $C$ מול $C$, שווים. רושמים $C$ ומגיעים לבסיס.", do=GL.step((1, 2), [(0, 1)]) + GL.path([(1, 2), (0, 1)]) + show("l-c3"),
      say="נעלה למעלה: שם סִי מול סִי, שווים. רושמים סִי ומגיעים לבסיס."),
    P("נאסף $D$, $B$, $C$. התווים נאספו מהסוף להתחלה, ולכן הופכים: $CBD$.", do=GL.off() + show("l-r1"),
      say="נאסף דִּי, בִּי, סִי. התווים נאספו מהסוף להתחלה, ולכן הופכים: סִי בִּי דִּי."),
    P("ואם היינו פונים שמאלה, היינו פוגשים $A$ מול $A$, ומקבלים $ABD$. גם היא באורך 3, וגם היא נכונה.",
      do=GL.path([(2, 1), (1, 0)]) + show("l-r2"),
      say="ואם היינו פונים שמאלה, היינו פוגשים אֵיי מול אֵיי, ומקבלים אֵיי בִּי דִּי. גם היא באורך שלוש, וגם היא נכונה."),
    P("שתי טעויות נפוצות: לשכוח להפוך, ובהתאמה להזיז רק אינדקס אחד במקום את שניהם.", do=show("l-t"), hold=0.3),
]
lcs = Scene("lcs", "שחזור תת-סדרה", lcs_ph,
            stage=f'<div class="dl-stack"><div id="l-g" class="h">{GL.html()}</div></div>',
            panel='<div class="dl-row">' + st.card("l-c1", "ex", "$D$") + st.card("l-c2", "ex", "$B$")
                  + st.card("l-c3", "ex", "$C$") + "</div>"
                  + st.card("l-tie", "rule", "🔑 שכנים שווים: כל בחירה נכונה")
                  + st.card("l-r1", "ex", "הפוך: $CBD$")
                  + st.card("l-r2", "ex", "שמאלה: $ABD$, גם נכון")
                  + st.card("l-t", "trap", "⚠️ להפוך בסוף · בהתאמה מזיזים את $i$ <b>ואת</b> $j$"))

ex_ph = [
    P("שאלה ממבחן. צובעים שלושה בתים בשורה: אדום, כחול או ירוק, ושני בתים שכנים בצבעים שונים.", do=show("x-c")),
    P("לכל בית ולכל צבע יש מחיר, ומבקשים להריץ את האלגוריתם על הטבלה הזאת."),
    P("הנוסחה מהסעיף הקודם: $R(i)$ הוא המחיר המינימלי לצבוע את הבתים עד $i$ כשהבית $i$ אדום. וכך גם כחול וירוק.",
      do=show("x-d"),
      say="הנוסחה מהסעיף הקודם: אָר שֶל אַיי הוא המחיר המינימלי לצבוע את הבתים עד אַיי, כשהבית אַיי אדום. וכך גם כחול וירוק."),
    P("בית אדום: המחיר שלו, ועוד המינימום של **שני הצבעים האחרים** בבית הקודם.", do=show("x-f")),
    P("עמודה ראשונה: רק המחירים של הבית הראשון. 14, 2 ו-11.", do=show("x-g") + GP.vals_do([(0, 0), (1, 0), (2, 0)])),
    P("בית שני, אדום: 11 ועוד המינימום של כחול וירוק בבית הראשון, כלומר 2. יוצא 13.",
      do=GP.step((0, 1), others("R", 1))),
    P("כחול: 14 ועוד 11, כלומר 25. וירוק: 5 ועוד 2, כלומר 7.",
      do=GP.vals_do([(1, 1)]) + GP.step((2, 1), others("G", 1))),
    P("בית שלישי: אדום 21, כחול 3 ועוד 7, כלומר 10, וירוק 32.",
      do=GP.vals_do([(0, 2), (2, 2)]) + GP.step((1, 2), others("B", 2))),
    P("הבית האחרון צבוע באחד משלושת הצבעים, ולכן המחיר המינימלי הוא המינימום של העמודה האחרונה: 10.",
      do=GP.off() + show("x-v")),
    P("ועכשיו השחזור. 10 נמצא בשורה הכחולה, ולכן הבית השלישי כחול.", do=GP.path([(1, 2)])),
    P("10 הוא 3 ועוד 7, ו-7 בא מהשורה הירוקה של הבית השני. לכן הבית השני ירוק.",
      do=GP.step((1, 2), [(2, 1)], value=False) + GP.path([(2, 1)])),
    P("ו-7 הוא 5 ועוד 2, שבא מהשורה הכחולה של הבית הראשון.", do=GP.step((2, 1), [(1, 0)], value=False) + GP.path([(1, 0)])),
    P("הצביעה היא כחול, ירוק, כחול. בדיקה: 2 ועוד 5 ועוד 3, כלומר 10.", do=GP.off() + show("x-ok")),
    P("והמלכודת: לקחת מינימום על **שלושת** הצבעים של הבית הקודם. כך אותו צבע יכול לחזור בשני בתים שכנים.",
      do=show("x-t"), hold=0.5),
]
exam = Scene("exam", "שאלה ממבחן", ex_ph,
             stage='<div class="dl-stack">'
                   + w.eqs("x", ["$R(i)=\\mathrm{cost}[i][1]+\\min\\bigl(B(i-1),\\,G(i-1)\\bigr)$"], 34).replace('id="x-0"', 'id="x-f"')
                   + f'<div id="x-g" class="h">{GP.html()}</div>'
                   + st.card("x-v", "rule", "🔑 $\\min\\bigl(R(3),B(3),G(3)\\bigr)=B(3)=10$")
                   + st.card("x-t", "trap", "⚠️ מינימום רק על <b>שני</b> הצבעים האחרים")
                   + "</div>",
             panel=f'<div class="dl-q"><span class="qid">{Q["id"]}</span>הריצו את האלגוריתם על מטריצת המחירים '
                   '($n=3$). שורות: הצבעים, עמודות: הבתים.</div>'
                   + f'<div id="x-c" class="h">{GC.html()}</div>'
                   + st.card("x-d", "ex", "$R(i),B(i),G(i)$: מינימום לבתים $1..i$, ובית $i$ בצבע הזה")
                   + st.card("x-ok", "rule", "🔑 כחול, ירוק, כחול: $2+5+3=10$"))


recap = Scene("recap", "סיכום", [
    P("לסיכום: מתחילים בתא התשובה, ושואלים איזה מקרה יצר את הערך.", do=show("s-1")),
    P("רושמים את ההחלטה, ועוברים לתא שהמקרה קרא, עד הבסיס.", do=show("s-2")),
    P("כששני מקרים נותנים אותו ערך, כל אחד מהם מוביל לפתרון נכון.", do=show("s-3")),
    P("ובסוף הופכים את הסדר. נתראה ברמה הבאה.", do=show("s-4"), hold=0.6),
], stage='<div class="dl-stack">'
         + st.card("s-1", "rule", "🔑 איזה מקרה יצר את הערך?")
         + st.card("s-2", "rule", "🔑 רושמים ועוברים לתא שהמקרה קרא")
         + "</div>",
   panel=st.card("s-3", "ex", "שוויון: כל בחירה נכונה")
         + st.card("s-4", "trap", "⚠️ בסוף הופכים את הסדר"))

VIDEO = Video("D05", "dp_ladder", "שחזור הפתרון לאחור", [title, idea, lcs, exam, recap],
              bank={"23B-C-Q3b": None})
