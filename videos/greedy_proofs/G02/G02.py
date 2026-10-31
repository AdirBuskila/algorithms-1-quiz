# -*- coding: utf-8 -*-
"""G02 · לבדוק כלל מול דוגמה נגדית — video script (build: tools/video/vid.py G02).

Source: courses/greedy_proofs/C02.js (goal: refute a plausible greedy rule with a small example, and identify the right
rule for disjoint intervals). Exam anchor: SAMP-1-Q4b (disjoint circles centred on the x axis: write a greedy
algorithm), an open question no guided level uses. The circles become intervals [c-r, c+r]; touching = not disjoint.
Avoided on purpose: the C02 quiz/lesson data ([1,10],[2,3],[4,5](,[6,7]); [1,10],[9,12],[11,20]; the 11-interval
input; budget 12 with 2,3,4,7,8), and 24A-A-Q5 / 24A-B-Q5 (twins of the shortest-first counterexample).
New counterexamples: start-first on [2,11],[3,5],[7,9]; shortest-first on [0,6],[5,8],[7,12].
Every pick and every optimum is computed below (W.iv_greedy_run) and checked against brute force (CHK.iv_opt).
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_greedy_proofs as W

CHK = W.CHK
ES = lambda x: (x[0], x[1])            # starts first
SHORT = lambda x: (x[1] - x[0], x[0])  # shortest first
EF = lambda x: (x[1], x[0])            # ends first

# ---------------------------------------------------------------- counterexample 1: starts first
A = [(2, 11), (3, 5), (7, 9)]
RA = W.iv_greedy_run(A, ES)
assert RA == [(0, [1, 2])] and CHK.iv_opt(A) == 2 and not W.conflict(A[1], A[2])
assert len(W.iv_greedy_run(A, EF)) == 2

# ---------------------------------------------------------------- counterexample 2: shortest first
B = [(0, 6), (5, 8), (7, 12)]
assert [b - a for a, b in B] == [6, 3, 5]
RB = W.iv_greedy_run(B, SHORT)
assert RB == [(1, [0, 2])] and CHK.iv_opt(B) == 2 and not W.conflict(B[0], B[2])
assert len(W.iv_greedy_run(B, EF)) == 2

# ---------------------------------------------------------------- exam SAMP-1-Q4b: seven circles (c, r)
Q = BANK["SAMP-1-Q4b"]
assert Q["contextId"] == "SAMP-1-c4"
CIRC = [(-4.5, 2), (0, 2), (0, 3), (5, 4), (6, 2), (7, 5), (8, 3)]     # c5 read with r5 = 2 (see the bank's note)
IV = [(c - r, c + r) for c, r in CIRC]
assert IV == [(-6.5, -2.5), (-2, 2), (-3, 3), (1, 9), (4, 8), (2, 12), (5, 11)]
RX = W.iv_greedy_run(IV, EF)
assert RX == [(0, [2]), (1, [3, 5]), (4, [6])]
assert IV[5][0] == IV[1][1]                       # c6 only touches c2: dropped because touching is a conflict
assert CHK.iv_opt(IV) == 3 == len(RX)
assert len(W.iv_greedy_run(IV, ES)) == 3 and len(W.iv_greedy_run(IV, SHORT)) == 3   # the exam input does not separate the rules
NAMES = [f"c{i + 1}" for i in range(7)]

TA = W.timeline("ta", A, 0, 12, w=900)
TB = W.timeline("tb", B, 0, 12, w=900)
TX = W.timeline("tx", IV, -7, 12, names=NAMES, w=980, row=50, ticks=range(-6, 13, 2))
IMG = st.raster("img", "images/exams/SAMP-1-Q4-circles.png", 980, (1578, 387))

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לשבור כלל חמדני בעזרת דוגמה נגדית קטנה."),
    P("ננסה שלושה כללים לבעיית הקטעים הזרים, ונגלה איזה מהם שורד."),
    P("ובסוף נפתור שאלת מבחן על מעגלים, שמתחפשת לאותה בעיה.", hold=0.4),
], stage='<div class="kicker">G02 · אלגוריתם חמדן והוכחת נכונות</div><h1>לבדוק כלל מול דוגמה נגדית</h1>'
         '<p>להפריך כלל חמדני שנראה סביר בעזרת דוגמה קטנה, ולזהות את הכלל הנכון בבעיית הקטעים הזרים.</p>',
   layout="title")

idea = Scene("idea", "הבעיה", [
    P("הבעיה הקלאסית: כל משימה היא קטע על ציר הזמן, עם התחלה וסיום."),
    P("שני קטעים **מתנגשים** אם יש להם נקודה משותפת. גם נגיעה בקצה היא התנגשות.", do=show("i-c")),
    P("צריך לבחור כמה שיותר קטעים, כך שאף שניים מהם לא מתנגשים."),
    P("יש שלושה כללים חמדניים שנשמעים סבירים.", do=show("i-1", "i-2", "i-3")),
    P("רק אחד מהם נכון תמיד. את שני האחרים נשבור בדוגמה נגדית.", hold=0.3),
    P("המתכון: כותבים את הכלל במדויק, ומחפשים שלושה קטעים שבהם הבחירה הראשונה **חוסמת** פתרון גדול יותר.",
      do=show("i-r")),
    P("ובסוף מציגים **שני מספרים**: כמה קטעים הכלל קיבל, וכמה אפשר לקבל.", do=show("i-t"), hold=0.4),
], stage='<div class="gp-stack"><div class="gp-steps">'
         '<div id="i-1" class="h"><span class="n">?</span>הקצר ביותר קודם</div>'
         '<div id="i-2" class="h"><span class="n">?</span>המתחיל ראשון קודם</div>'
         '<div id="i-3" class="h"><span class="n">?</span>המסתיים ראשון קודם</div></div></div>',
   panel=st.card("i-c", "plain", "קטעים סגורים: $[1,4]$ ו-$[4,6]$ <b>מתנגשים</b>")
         + st.card("i-r", "rule", "🔑 דוגמה נגדית: הבחירה הראשונה של הכלל חוסמת פתרון גדול יותר")
         + st.card("i-t", "trap", "⚠️ חייבים שני מספרים: כמה הכלל קיבל, וכמה אפשר"))

ex1 = Scene("ex1", "המתחיל ראשון", [
    P("נתחיל מהכלל: בוחרים את הקטע שמתחיל ראשון, וזורקים את כל מי שמתנגש בו."),
    P("שלושה קטעים: מ-2 עד 11, מ-3 עד 5, ומ-7 עד 9.", do=show("ta")),
    P("הראשון שמתחיל הוא הקטע מ-2 עד 11, והכלל בוחר אותו.", do=show("ta-g0")),
    P("הוא מכסה את שני האחרים, ולכן שניהם נזרקים. הכלל קיבל קטע **אחד**.", do=show("ta-x1", "ta-x2")),
    P("אבל שני הקטעים הקצרים זרים זה לזה, כי 5 קטן מ-7. יחד הם **שניים**.",
      do=hide("ta-g0", "ta-x1", "ta-x2") + show("ta-x0", "ta-g1", "ta-g2")),
    P("אחד מול שניים: זו דוגמה נגדית מלאה, והכלל המתחיל ראשון נפל.", do=show("a-c"), hold=0.4),
], stage=f'<div class="gp-stack"><div id="ta" class="h">{TA}</div></div>',
   panel=st.card("a-c", "ex", "המתחיל ראשון: <b>1</b> קטע. אפשר: <b>2</b>, $[3,5]$ ו-$[7,9]$"))

ex2 = Scene("ex2", "הקצר ביותר", [
    P("עכשיו הכלל השני: הקצר ביותר קודם."),
    P("הקטעים: מאפס עד 6, מ-5 עד 8, ומ-7 עד 12. האורכים הם 6, 3 ו-5.", do=show("tb")),
    P("הקצר הוא הקטע מ-5 עד 8, והכלל בוחר אותו.", do=show("tb-g1")),
    P("הוא חופף לראשון בין 5 ל-6, ולשלישי בין 7 ל-8. שניהם נזרקים.", do=show("tb-x0", "tb-x2")),
    P("הכלל קיבל קטע אחד. אבל הראשון והשלישי זרים, כי 6 קטן מ-7. שניים.",
      do=hide("tb-g1", "tb-x0", "tb-x2") + show("tb-x1", "tb-g0", "tb-g2", "b-c")),
    P("שני כללים נפלו. נשאר הכלל **המסתיים ראשון**, ובשתי הדוגמאות האלה הוא אכן בוחר שני קטעים.", do=show("b-r")),
    P("הוא נכון תמיד, ואת ההוכחה נבנה ברמה הבאה.", hold=0.4),
], stage=f'<div class="gp-stack"><div id="tb" class="h">{TB}</div></div>',
   panel=st.card("b-c", "ex", "הקצר ביותר: <b>1</b> קטע. אפשר: <b>2</b>, $[0,6]$ ו-$[7,12]$")
         + st.card("b-r", "rule", "🔑 הכלל הנכון: <b>המסתיים ראשון</b>. בוחרים, זורקים מתנגשים, חוזרים"))

say_c = {i: f"סִי {w}" for i, w in enumerate(["אחת", "שתיים", "שלוש", "ארבע", "חמש", "שש", "שבע"])}
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מעגלים במישור, וכל המרכזים על ציר האיקס. מחפשים כמה שיותר מעגלים זרים בזוגות.",
      do=show("img")),
    P("כל מעגל נתון כמרכז ורדיוס. ושימו לב: מעגלים **משיקים** אינם זרים."),
    P("הצעד הראשון: לזהות בעיה מוכרת. כל מעגל תופס על הציר את הקטע מ-$c-r$ עד $c+r$.", do=show("x-k"),
      say="הצעד הראשון: לזהות בעיה מוכרת. כל מעגל תופס על הציר את הקטע מהמרכז פחות הרדיוס, עד המרכז ועוד הרדיוס."),
    P("ושני מעגלים כאלה זרים בדיוק כשהקטעים שלהם זרים. זו בעיית הקטעים הזרים, בתחפושת.",
      do=hide("img") + show("tx")),
    P("האלגוריתם: ממיינים לפי הקצה הימני, בוחרים את הראשון, ומסירים כל מעגל שמתחיל לפני סוף הנבחר, או בדיוק בו.",
      do=show("x-a")),
    P("הקצה הימני הקטן ביותר: $c_1$, שנגמר במינוס 2.5. בוחרים אותו, ו-$c_3$, שמתחיל במינוס 3, נזרק.",
      do=show("tx-g0", "tx-x2"),
      say=f"הקצה הימני הקטן ביותר: {say_c[0]}, שנגמר במינוס שתיים וחצי. בוחרים אותו, ו{say_c[2]}, שמתחיל במינוס שלוש, נזרק."),
    P("הבא: $c_2$, שנגמר ב-2. נזרקים $c_4$, שמתחיל ב-1, ו-$c_6$, שמתחיל בדיוק ב-2.",
      do=show("tx-g1", "tx-x3", "tx-x5", "tx-h5"),
      say=f"הבא: {say_c[1]}, שנגמר בשתיים. נזרקים {say_c[3]}, שמתחיל באחת, ו{say_c[5]}, שמתחיל בדיוק בשתיים."),
    P("וזו המלכודת: $c_6$ רק **משיק** ל-$c_2$, ובכל זאת נזרק. לכן התנאי הוא קטן **או שווה**.", do=show("x-t"),
      say=f"וזו המלכודת: {say_c[5]} רק משיק ל{say_c[1]}, ובכל זאת נזרק. לכן התנאי הוא קטן או שווה."),
    P("הבא: $c_5$, שנגמר ב-8. נזרק $c_7$, שמתחיל ב-5, ולא נשאר אף מעגל.",
      do=hide("tx-h5") + show("tx-g4", "tx-x6"),
      say=f"הבא: {say_c[4]}, שנגמר בשמונה. נזרק {say_c[6]}, שמתחיל בחמש, ולא נשאר אף מעגל."),
    P("התוצאה: שלושה מעגלים זרים. חיפוש על כל 128 תתי הקבוצות מאשר ששלושה הוא המקסימום.", do=show("x-ok"), hold=0.3),
    P("ומעניין: על הקלט הזה גם המתחיל ראשון וגם הקצר ביותר נותנים שלושה."),
    P("אז הדוגמה שבשאלה לא מבדילה בין הכללים. בוחרים את הכלל לפי ההוכחה, לא לפי הדוגמה."),
    P("והזמן: מיון ב-$O(n\\,\\log\\,n)$, ועוד מעבר אחד על הרשימה.",
      say="והזמן: מיון באו של אֶן לוֹג אֶן, ועוד מעבר אחד על הרשימה.", hold=0.5),
], stage=f'<div class="swap" style="--swap-h:560px"><div id="img" class="h" style="justify-content:center">{IMG}'
         '<div class="gp-note">סקיצה מהמבחן. המספרים הם הקובעים</div></div>'
         f'<div id="tx" class="h">{TX}</div></div>'
         + st.card("x-ok", "ex", "✓ $c_1, c_2, c_5$: שלושה מעגלים, וזה המקסימום"),
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>$n$ מעגלים שמרכזיהם על ציר ה-$x$, כל אחד נתון כזוג '
         '$(c, r)$. מחפשים את המספר המקסימלי של מעגלים זרים בזוגות (משיקים אינם זרים). כתבו אלגוריתם חמדני.</div>'
         + st.card("x-k", "rule", "🔑 מעגל $\\to$ קטע $[c-r,\\ c+r]$")
         + st.card("x-a", "rule", "🔑 מיון לפי $c+r$; מסירים כל מעגל עם $c-r \\le$ הסוף של הנבחר")
         + st.card("x-t", "trap", "⚠️ משיקים אינם זרים: מסירים גם כשההתחלה <b>שווה</b> לסוף"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: דוגמה נגדית היא קלט קטן שבו הבחירה הראשונה של הכלל חוסמת פתרון גדול יותר.", do=show("r-1")),
    P("והיא כוללת שני מספרים: כמה הכלל קיבל, וכמה אפשר.", do=show("r-2")),
    P("בקטעים זרים, המתחיל ראשון והקצר ביותר נופלים. המסתיים ראשון נכון, ואת זה נוכיח ברמה הבאה.", do=show("r-3"),
      hold=0.6),
], stage=f'<div class="gp-stack">{W.timeline("tr", [(0, 6), (7, 12)], 0, 12, w=900)}</div>',
   panel=st.card("r-1", "rule", "🔑 דוגמה נגדית: הבחירה הראשונה חוסמת")
         + st.card("r-2", "trap", "⚠️ שני מספרים: הכלל מול האופטימום")
         + st.card("r-3", "rule", "🔑 קטעים זרים: <b>המסתיים ראשון</b>"))

VIDEO = Video("G02", "greedy_proofs", "לבדוק כלל מול דוגמה נגדית", [title, idea, ex1, ex2, exam, recap],
              bank={"SAMP-1-Q4b": None})
