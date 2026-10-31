# -*- coding: utf-8 -*-
"""D04 · ממלאים טבלה ביד — video script (build: tools/video/vid.py D04).

Source: courses/dp_ladder/C04.js (lesson + goal). Exam anchor: 25A-B-Q1a (fill the table T of the largest all-zero
square whose bottom-right corner is (i, j), for the 5×6 matrix M of the question, open question). The matrix is the
original exam figure images/exams/25A-B-Q1-matrix.png (shown, never redrawn); M below is transcribed from it and the
table computed from M equals the solution's table. No guided quiz uses it.
Not used on purpose: the C04 quiz (LCS of ACBAB/ABCB, edit distance ABC/BCD, ab in aabab) and its bank question
22B-A-Q4c (counting abc in abcbac), and every boss question of C09.
The LCS (BAC/ABC) and edit-distance (CAB/CBA) examples are original. Every value is computed by w_dp_ladder and
compared with a brute force below.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_dp_ladder as w

# ---------------------------------------------------------------- data (verified)
X1, Y1 = "BAC", "ABC"                                   # LCS
L = w.lcs_table(X1, Y1)
assert L[3][3] == w.lcs_bf(X1, Y1) == 2 and w.all_lcs(X1, Y1) == {"BC", "AC"}
assert all(L[i][j] == w.lcs_bf(X1[:i], Y1[:j]) for i in range(4) for j in range(4))
assert L == [[0, 0, 0, 0], [0, 0, 1, 1], [0, 1, 1, 1], [0, 1, 1, 2]]
assert X1[0] == Y1[1] and L[1][2] == L[0][1] + 1 and X1[1] == Y1[0] and L[2][1] == L[1][0] + 1
assert X1[2] == Y1[2] and L[3][3] == L[2][2] + 1

X2, Y2 = "CAB", "CBA"                                   # edit distance
D = w.edit_table(X2, Y2)
assert all(D[i][j] == w.edit_bf(X2[:i], Y2[:j]) for i in range(4) for j in range(4))
assert D == [[0, 1, 2, 3], [1, 0, 1, 2], [2, 1, 1, 1], [3, 2, 1, 2]]
assert X2[0] == Y2[0] and D[1][1] == D[0][0] == 0
assert X2[2] == Y2[1] and D[3][2] == D[2][1] == 1           # equal letters: the diagonal, no +1
assert X2[2] != Y2[2] and D[3][3] == 1 + min(D[2][2], D[2][3], D[3][2]) == 2

# exam 25A-B-Q1a: the matrix of the figure, row by row
Q = BANK["25A-B-Q1a"]
assert "T" in Q["question"] and Q.get("correctId") is None
M = [[0, 1, 1, 0, 1, 1],
     [0, 0, 1, 0, 0, 0],
     [1, 0, 0, 0, 0, 0],
     [1, 1, 0, 0, 0, 1],
     [1, 1, 0, 0, 0, 0]]
T = w.zero_square(M)
assert all(T[i][j] == w.zero_square_bf(M, i, j) for i in range(5) for j in range(6))
OFFICIAL = [[1, 0, 0, 1, 0, 0], [1, 1, 0, 1, 1, 1], [0, 1, 1, 1, 2, 2], [0, 0, 1, 2, 2, 0], [0, 0, 1, 2, 3, 1]]
assert T == OFFICIAL and max(map(max, T)) == 3 == T[4][4]
assert T[2][4] == 2 and M[0][2] == 1                       # the 3×3 square at (2,4) is blocked by M[0][2]
assert max(T[1]) == 1 and all(M[0][j] or M[0][j + 1] for j in range(5))
assert T[3][3] == 2 and T[2][5] == 2 and T[4][5] == 1 and M[3][5] == 1

# ---------------------------------------------------------------- widgets
def lab(s):
    return ["∅"] + list(s)


GL = w.Grid("gl", lab(X1), lab(Y1), {(i, j): str(L[i][j]) for i in range(4) for j in range(4)},
            given={(0, j) for j in range(4)} | {(i, 0) for i in range(4)}, cw=92, ch=72, fs=36)
GD = w.Grid("gd", lab(X2), lab(Y2), {(i, j): str(D[i][j]) for i in range(4) for j in range(4)},
            cw=92, ch=72, fs=36)
GT = w.Grid("gt", [str(i) for i in range(5)], [str(j) for j in range(6)],
            {(i, j): str(T[i][j]) for i in range(5) for j in range(6)}, cw=84, ch=68, fs=34, corner="T")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("במבחן כמעט תמיד מבקשים להראות הרצה על דוגמה. בסרטון הזה נמלא טבלאות ביד."),
    P("טבלה של תת-סדרה משותפת, טבלה של מרחק עריכה, וטבלה משאלת מבחן.", hold=0.4),
], stage='<div class="kicker">D04 · תכנות דינמי</div><h1>ממלאים טבלה ביד</h1>'
         '<p>ממלאים טבלה קטנה תא אחרי תא לפי הנוסחה: תת-סדרה משותפת, מרחק עריכה, ושאלת מבחן.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("מציירים טבלה, כותבים את הבסיס, וממלאים בסדר חוקי.", do=show("i-1")),
    P("ובכל תא יש שני שלבים. קודם קובעים **איזה מקרה** בנוסחה חל, ורק אחר כך מציבים.", do=show("i-2")),
    P("בתת-סדרה משותפת: אם התווים שווים, הולכים לאלכסון ומוסיפים אחד. אחרת, המקסימום של השכנים.", do=show("i-l")),
    P("במרחק עריכה: אם התווים שווים, האלכסון **בלי** תוספת. אחרת, אחד ועוד המינימום של שלושה שכנים.", do=show("i-e")),
    P("ובספירת מופעים: אם התווים שווים, מחברים את האלכסון ואת התא שמעל.", do=show("i-c"), hold=0.3),
], stage='<div class="dl-stack">'
         + st.card("i-1", "ex", "טבלה → בסיס → מילוי בסדר חוקי")
         + st.card("i-2", "rule", "🔑 בכל תא: קודם <b>איזה מקרה</b>, אחר כך מציבים")
         + "</div>",
   panel=st.card("i-l", "plain", "<b>LCS</b>: שווים → $L(i-1,j-1)+1$, אחרת $\\max$ של שני שכנים")
         + st.card("i-e", "plain", "<b>עריכה</b>: שווים → $D(i-1,j-1)$, אחרת $1+\\min$ של שלושה")
         + st.card("i-c", "plain", "<b>ספירה</b>: שווים → $C(i-1,j-1)+C(i-1,j)$"))
idea.phrases[2].say_override = ("בתת סדרה משותפת: אם התווים שווים, הולכים לאלכסון ומוסיפים אחד. "
                                "אחרת, המקסימום של השכנים.")

lcs_ph = [
    P("תת-סדרה משותפת ארוכה ביותר של $BAC$ ושל $ABC$. השורות לפי הראשונה, העמודות לפי השנייה.", do=show("l-g"),
      say="תת סדרה משותפת ארוכה ביותר, של בִּי אֵיי סִי, ושל אֵיי בִּי סִי. השורות לפי הראשונה, העמודות לפי השנייה."),
    P("השורה והעמודה של המחרוזת הריקה הן אפסים. עכשיו שורה ראשונה, של $B$.",
      say="השורה והעמודה של המחרוזת הריקה הן אפסים. עכשיו שורה ראשונה, של בִּי."),
    P("$B$ מול $A$: שונים. המקסימום של שני השכנים, אפס.", do=show("gl-rh-1", "gl-ch-1") + GL.step((1, 1), [(0, 1), (1, 0)]),
      say="בִּי מול אֵיי: שונים. המקסימום של שני השכנים, אפס."),
    P("$B$ מול $B$: שווים. האלכסון ועוד אחד: אחד.", do=hide("gl-ch-1") + show("gl-ch-2") + GL.step((1, 2), [(0, 1)]),
      say="בִּי מול בִּי: שווים. האלכסון ועוד אחד: אחת."),
    P("$B$ מול $C$: שונים, ולוקחים את האחד משמאל.", do=hide("gl-ch-2") + show("gl-ch-3") + GL.step((1, 3), [(0, 3), (1, 2)]),
      say="בִּי מול סִי: שונים, ולוקחים את האחת משמאל."),
    P("בשורה של $A$: מול $A$ שווים, אז האלכסון אפס ועוד אחד. ושאר השורה אחדות.",
      do=hide("gl-rh-1", "gl-ch-3") + show("gl-rh-2", "gl-ch-1") + GL.step((2, 1), [(1, 0)]) + GL.vals_do([(2, 2), (2, 3)]),
      say="בשורה של אֵיי: מול אֵיי שווים, אז האלכסון אפס ועוד אחד. ושאר השורה אחדות."),
    P("בשורה של $C$: מול $A$ ומול $B$ שונים, ושם אחת. ומול $C$ שווים.",
      do=hide("gl-rh-2", "gl-ch-1") + show("gl-rh-3", "gl-ch-3") + GL.vals_do([(3, 1), (3, 2)]) + GL.step((3, 3), [(2, 2)]),
      say="בשורה של סִי: מול אֵיי ומול בִּי שונים, ושם אחת. ומול סִי שווים."),
    P("האלכסון הוא אחת, ועוד אחד: שתיים. אורך התת-סדרה המשותפת הוא 2.", do=show("l-ok")),
    P("המלכודת: בתווים שווים הולכים ל**אלכסון**, לא לשכן שמעל. הוא עשוי כבר להשתמש באותו תו.",
      do=GL.off() + hide("gl-rh-3", "gl-ch-3") + show("l-t"), hold=0.3),
]
lcs = Scene("lcs", "תת-סדרה משותפת", lcs_ph,
            stage=f'<div class="dl-stack"><div id="l-g" class="h">{GL.html()}</div></div>',
            panel=st.card("l-f", "plain", "שווים: $L(i-1,j-1)+1$<br>שונים: $\\max\\bigl(L(i-1,j),L(i,j-1)\\bigr)$")
                  .replace(' h"', '"')
                  + st.card("l-ok", "rule", "🔑 $L(3,3)=2$: למשל $BC$")
                  + st.card("l-t", "trap", "⚠️ שווים → האלכסון, לא השכן שמעל"))

ed_ph = [
    P("מרחק עריכה: כמה פעולות של הוספה, מחיקה או החלפה של תו הופכות את $CAB$ ל-$CBA$.", do=show("e-g"),
      say="מרחק עריכה: כמה פעולות של הוספה, מחיקה או החלפה של תו, הופכות את סִי אֵיי בִּי, לסִי בִּי אֵיי."),
    P("כאן גם הבסיס לא אפסים: מרישא באורך $i$ למחרוזת ריקה צריך $i$ מחיקות.",
      do=GD.vals_do([(i, 0) for i in range(4)] + [(0, j) for j in range(4)]),
      say="כאן גם הבסיס לא אפסים: מרישא באורך אַיי למחרוזת ריקה, צריך אַיי מחיקות."),
    P("$C$ מול $C$: שווים, ולוקחים את האלכסון בלי תוספת: אפס.", do=GD.step((1, 1), [(0, 0)]),
      say="סִי מול סִי: שווים, ולוקחים את האלכסון בלי תוספת: אפס."),
    P("$C$ מול $B$: שונים. אחת ועוד המינימום של שלושה שכנים, והמינימום הוא האפס משמאל.",
      do=GD.step((1, 2), [(0, 1), (0, 2), (1, 1)]),
      say="סִי מול בִּי: שונים. אחת ועוד המינימום של שלושה שכנים, והמינימום הוא האפס משמאל."),
    P("כך ממלאים את שתי השורות הבאות.", do=GD.vals_do([(1, 3), (2, 1), (2, 2), (2, 3), (3, 1)]) + GD.off()),
    P("ועכשיו $B$ מול $B$. שווים, ולכן האלכסון: אחת.", do=GD.step((3, 2), [(2, 1)]),
      say="ועכשיו בִּי מול בִּי. שווים, ולכן האלכסון: אחת."),
    P("מי שמוסיף כאן אחד, מקבל 2. ההתאמה לא עולה כלום.", do=show("e-t")),
    P("והתא האחרון: $B$ מול $A$, שונים. אחת ועוד המינימום, שהוא 1: התשובה היא 2.",
      do=GD.step((3, 3), [(2, 2), (2, 3), (3, 2)]) + show("e-ok"),
      say="והתא האחרון: בִּי מול אֵיי, שונים. אחת ועוד המינימום, שהוא אחת: התשובה היא שתיים."),
]
ed = Scene("edit", "מרחק עריכה", ed_ph,
           stage=f'<div class="dl-stack"><div id="e-g" class="h">{GD.html()}</div></div>',
           panel=st.card("e-f", "plain", "שווים: $D(i-1,j-1)$<br>שונים: $1+\\min$ של שלושה שכנים").replace(' h"', '"')
                 + st.card("e-t", "trap", "⚠️ תווים שווים: <b>בלי</b> $+1$")
                 + st.card("e-ok", "rule", "🔑 $D(3,3)=2$: מחליפים את $A$ ואת $B$"))

ex_ph = [
    P("ועכשיו שאלה ממבחן. נתונה מטריצה של אפסים ואחדים, ומחפשים את ריבוע האפסים הגדול ביותר.", do=show("x-m")),
    P("הטבלה $T(i,j)$ היא אורך הצלע של ריבוע האפסים הגדול ביותר, שהפינה **הימנית התחתונה** שלו היא $(i,j)$.",
      do=show("x-d"),
      say="הטבלה טִי שֶל אַיי וגֵ'יי היא אורך הצלע של ריבוע האפסים הגדול ביותר, שהפינה הימנית התחתונה שלו היא אַיי, גֵ'יי."),
    P("הסעיף מבקש למלא את הטבלה לפי המשמעות, עוד בלי נוסחה."),
    P("תא שיש בו 1 לא יכול להיות פינה של ריבוע אפסים, ולכן מקבל 0.", do=show("x-g") + show("x-r1")),
    P("תא אפס בשורה הראשונה או בעמודה הראשונה: אין מקום לריבוע גדול מ-1.",
      do=GT.vals_do([(0, j) for j in range(6)] + [(i, 0) for i in range(5)])),
    P("שורה 1: אחדות, ו-0 בתא שבו יש 1 במטריצה. אין כאן ריבוע של 2, כי בשורה 0 יש 1 בכל זוג עמודות סמוכות.",
      do=GT.vals_do([(1, j) for j in range(1, 6)])),
    P("שורה 2. בתא $(2,4)$ השורות 1 ו-2 והעמודות 3 ו-4 כולן אפס: ריבוע של 2.", do=GT.vals_do([(2, 1), (2, 2), (2, 3)])
      + GT.step((2, 4), [(1, 3), (1, 4), (2, 3)]),
      say="שורה שתיים. בתא שתיים, ארבע, השורות אחת ושתיים, והעמודות שלוש וארבע, כולן אפס: ריבוע של שתיים."),
    P("ריבוע של 3 שם היה צריך גם את שורה 0, ושם, בעמודה 2, יש 1. לכן רק 2.", do=show("x-b")),
    P("גם $(2,5)$ מקבל 2. בשורה 3, התא $(3,3)$ מקבל 2, ובקצה יש 1 במטריצה, ולכן 0.",
      do=GT.vals_do([(2, 5), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5)]) + GT.off(),
      say="גם שתיים, חמש מקבל שתיים. בשורה שלוש, התא שלוש, שלוש מקבל שתיים, ובקצה יש אחת במטריצה, ולכן אפס."),
    P("ובשורה האחרונה, התא $(4,4)$: שלוש שורות ושלוש עמודות של אפסים. ריבוע של 3.",
      do=GT.vals_do([(4, j) for j in range(4)] + [(4, 5)]) + GT.step((4, 4), [(3, 3), (3, 4), (4, 3)]),
      say="ובשורה האחרונה, התא ארבע, ארבע: שלוש שורות ושלוש עמודות של אפסים. ריבוע של שלוש."),
    P("זה הריבוע המודגש בשאלה, ו-3 הוא הערך הגדול ביותר בטבלה. זו התשובה.", do=show("x-ok")),
    P("שימו לב לתאים הכחולים: ריבוע של 3 בפינה דורש ריבועים של 2 בשלושת השכנים. זו הנוסחה של הסעיף הבא.",
      do=show("x-n"), hold=0.5),
]
exam = Scene("exam", "שאלה ממבחן", ex_ph,
             stage=f'<div class="dl-stack"><div id="x-g" class="h">{GT.html()}</div>'
                   + st.card("x-ok", "rule", "🔑 $\\max_{i,j} T(i,j)=T(4,4)=3$")
                   + st.card("x-n", "ex", "ריבוע $s$ בפינה ← ריבועים $s-1$ בשלושת השכנים")
                   + "</div>",
             panel=f'<div class="dl-q"><span class="qid">{Q["id"]}</span>מלאו את $T$ עבור המטריצה $M$ שבשאלה.</div>'
                   + f'<div id="x-m" class="h">{st.raster("x-mr", "images/exams/25A-B-Q1-matrix.png", 280, (557, 462))}</div>'
                   + st.card("x-d", "ex", "$T(i,j)$ = צלע ריבוע האפסים הגדול ביותר שפינתו הימנית התחתונה $(i,j)$")
                   + st.card("x-r1", "plain", "$M[i][j]=1 \\Rightarrow T(i,j)=0$")
                   + st.card("x-b", "trap", "⚠️ $(2,4)$: ריבוע של 3 נחסם ב-$M[0][2]=1$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: טבלה, בסיס, ואז תא אחרי תא בסדר חוקי.", do=show("s-1")),
    P("בכל תא קודם קובעים איזה מקרה חל, למשל אם התווים שווים, ורק אז מציבים.", do=show("s-2")),
    P("בתת-סדרה משותפת התאמה הולכת לאלכסון ועוד אחד. במרחק עריכה התאמה הולכת לאלכסון בלי תוספת.", do=show("s-3")),
    P("והתשובה נקראת מהתא שההגדרה אומרת, או מהמקסימום של הטבלה. נתראה ברמה הבאה.", do=show("s-4"), hold=0.6),
], stage='<div class="dl-stack">'
         + st.card("s-1", "rule", "🔑 טבלה → בסיס → תא אחרי תא")
         + st.card("s-2", "rule", "🔑 קודם המקרה, אחר כך ההצבה")
         + "</div>",
   panel=st.card("s-3", "trap", "⚠️ LCS: אלכסון $+1$ · עריכה: אלכסון בלי $+1$")
         + st.card("s-4", "ex", "התשובה: התא שההגדרה קובעת, או $\\max$"))

VIDEO = Video("D04", "dp_ladder", "ממלאים טבלה ביד", [title, idea, lcs, ed, exam, recap],
              bank={"25A-B-Q1a": None})
