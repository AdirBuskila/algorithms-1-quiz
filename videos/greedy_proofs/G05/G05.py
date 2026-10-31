# -*- coding: utf-8 -*-
"""G05 · החמדן מקדים ו"הכי קרוב לחמדן" — video script (build: tools/video/vid.py G05).

Source: courses/greedy_proofs/C05.js (goal: prove optimality without a single swap: the greedy stays ahead of every
solution, or start from the optimal solution closest to the greedy). Exam anchors: 24A-B-Q2a (sealing boxes in order
with tapes of length m: an algorithm) and 24A-B-Q2b (prove it), open questions no guided level uses. The video proves
24A-B by "greedy stays ahead" (a_r >= b_r), the bank's student answer used a first-tape exchange.
Avoided on purpose: the C05 quiz data (positions 0,3,4,7,8,12,13 with k=5) and its proof lines are not shown; the
worked restaurants are not used at all: the worked example is refuelling (stations 3,4,7,9,12,14,17, range 5). 24B-B-Q4 (restaurants) and 24B-A-Q2 (the
stations; 24B-A-Q2c is a boss item) are not used.
Every run, every optimum and every inequality on screen is computed below.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_greedy_proofs as W

CHK = W.CHK

# ---------------------------------------------------------------- worked: refuelling, the greedy stays ahead
ST, DEST, RNG = [3, 4, 7, 9, 12, 14, 17], 20, 5          # stations on a road, the destination, the range of a full tank
import itertools as _it


def refuel_greedy(st, d, rng):
    pos, stops = 0, []
    while pos + rng < d:
        cand = [x for x in st if pos < x <= pos + rng]
        assert cand
        pos = max(cand)
        stops.append(pos)
    return stops


def refuel_ok(seq, d, rng):
    p = [0] + list(seq) + [d]
    return all(q - p0 <= rng for p0, q in zip(p, p[1:]))


G = refuel_greedy(ST, DEST, RNG)
assert G == [4, 9, 14, 17]
FEAS = [t for r in range(len(ST) + 1) for t in _it.combinations(ST, r) if refuel_ok(t, DEST, RNG)]
assert min(len(t) for t in FEAS) == 4
O = (3, 7, 12, 17)
assert O in FEAS and all(g >= o for g, o in zip(G, O))          # g_r >= o_r: the greedy is never behind
assert all(all(g >= o for g, o in zip(G, t)) for t in FEAS)    # ... against every feasible stop list
assert 4 <= 0 + RNG < 7 and 9 <= 4 + RNG < 12                   # each greedy stop = the farthest station in reach
# "closest to greedy": fix the first difference, one at a time; every step legal and of the same size
STEPS = [O]
cur = list(O)
for r in range(len(G)):
    if cur[r] != G[r]:
        cur[r] = G[r]
        assert tuple(cur) in FEAS
        STEPS.append(tuple(cur))
assert STEPS == [(3, 7, 12, 17), (4, 7, 12, 17), (4, 9, 12, 17), (4, 9, 14, 17)]

# ---------------------------------------------------------------- exam 24A-B-Q2: boxes in order, tapes of length m
QA, QB = BANK["24A-B-Q2a"], BANK["24A-B-Q2b"]
assert QA["contextId"] == QB["contextId"] == "24A-B-c2"
assert W.pack_greedy([2, 1, 4, 2], 5) == [[2, 1], [4], [2]] and W.pack_opt([2, 1, 4, 2], 5) == 3   # the stem's example
BOX, M = [3, 2, 4, 1, 3, 2, 5, 1], 6
GB = W.pack_greedy(BOX, M)
assert GB == [[3, 2], [4, 1], [3, 2], [5, 1]] and W.pack_opt(BOX, M) == 4
assert sum(BOX) == 21 > 3 * M                                   # three tapes hold at most 18: four is the minimum
OB = [[3], [2, 4], [1, 3, 2], [5, 1]]
assert sum(OB, []) == BOX and all(sum(b) <= M for b in OB)
cum = lambda blocks: [sum(len(b) for b in blocks[:r + 1]) for r in range(len(blocks))]
A_R, B_R = cum(GB), cum(OB)
assert A_R == [2, 4, 6, 8] and B_R == [1, 3, 6, 8] and all(a >= b for a, b in zip(A_R, B_R))
# stays ahead against EVERY in-order packing of this input, and the greedy is optimal on all small inputs
import itertools


def packings(boxes, m):
    n = len(boxes)
    for cuts in itertools.product([0, 1], repeat=n - 1):
        blocks, cur = [], [boxes[0]]
        for c, b in zip(cuts, boxes[1:]):
            if c:
                blocks.append(cur)
                cur = [b]
            else:
                cur.append(b)
        blocks.append(cur)
        if all(sum(b) <= m for b in blocks):
            yield blocks


for pk in packings(BOX, M):
    bb = cum(pk)
    assert all(A_R[r] >= bb[r] for r in range(min(len(A_R), len(bb))))
for n in range(1, 7):
    for boxes in itertools.product(range(1, 5), repeat=n):
        assert len(W.pack_greedy(list(boxes), 4)) == W.pack_opt(list(boxes), 4)

POS = W.chips("p", [str(x) for x in ST], hidden=False, label="תחנות:")
RT = W.table("rt", ["$r$", "$g_r$", "$o_r$"], [[str(r + 1), str(g), str(o)] for r, (g, o) in enumerate(zip(G, O))])
BOXES = W.chips("bx", [str(b) for b in BOX], hidden=False, cls="small", label="ארגזים:")
TG = W.tapes("tg", GB, M, unit=40)
TO = W.tapes("to", OB, M, unit=40)
AB = W.table("ab", ["$r$", "$a_r$", "$b_r$"], [[str(r + 1), str(a), str(b)] for r, (a, b) in enumerate(zip(A_R, B_R))])

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד שתי דרכים להוכיח חמדן בלי החלפה בודדת: החמדן מקדים, והכי קרוב לחמדן."),
    P("ובסוף נוכיח כך שאלה ממבחן על סרטי הדבקה.", hold=0.4),
], stage='<div class="kicker">G05 · אלגוריתם חמדן והוכחת נכונות</div><h1>החמדן מקדים ו"הכי קרוב לחמדן"</h1>'
         '<p>להוכיח אופטימליות בלי להחליף: להראות שהחמדן תמיד "לפני" כל פתרון אחר, או להתחיל מפתרון אופטימלי הכי קרוב '
         'לחמדן.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("השיטה הזאת מתאימה כשהפתרון הוא **רשימה של בחירות לפי הסדר**: עצירות בדרך, סרטים, תחנות."),
    P("משווים את החמדן לכל פתרון אחר, שלב אחרי שלב, ומוכיחים באינדוקציה שהחמדן **אף פעם לא מאחר**.",
      do=show("i-r")),
    P("ובסוף מסיקים מזה שהחמדן לא צריך יותר צעדים, או שהוא לא בוחר פחות.", do=show("i-e"), hold=0.4),
], stage='<div class="gp-stack"><div class="gp-big">$g_1, g_2, g_3, \\dots$<br>$o_1, o_2, o_3, \\dots$</div></div>',
   panel=st.card("i-r", "rule", "🔑 החמדן מקדים: אחרי $r$ שלבים, החמדן במצב טוב לפחות כמו כל פתרון")
         + st.card("i-e", "ex", "ובסוף: אילו לפתרון האחר היה יותר, החמדן לא היה עוצר"))

ex = Scene("ex", "תחנות דלק", [
    P("דוגמה: נוסעים מנקודה אפס לנקודה 20. מיכל מלא מספיק ל-5 קילומטרים, ויש תחנות דלק בדרך."),
    P("התחנות בנקודות 3, 4, 7, 9, 12, 14 ו-17. רוצים לעצור כמה שפחות פעמים.", do=show("p")),
    P("החמדן: נוסעים כמה שאפשר, ועוצרים בתחנה הרחוקה ביותר שעוד מגיעים אליה."),
    P("מאפס מגיעים עד 5: עוצרים ב-4. משם עד 9, ממנה עד 14, ומשם עד 17. ומ-17 מגיעים ל-20.",
      do=show(*[f"p-{ST.index(x)}-ok" for x in G])),
    P("ארבע עצירות, וחיפוש מלא מאשר שבפחות אי אפשר.", hold=0.2),
    P("פתרון אופטימלי אחר: 3, 7, 12 ו-17. השוו עצירה מול עצירה.", do=show("rt-r0", "rt-r1", "rt-r2", "rt-r3")),
    P("החמדן תמיד רחוק יותר או באותו מקום: 4 מול 3, 9 מול 7, 14 מול 12, ו-17 מול 17.",
      do=show("rt-k0", "rt-k1", "rt-k2", "rt-k3")),
    P("זו הטענה שמוכיחים באינדוקציה: אחרי כל מספר של עצירות, החמדן לא מאחורי אף פתרון.", do=show("e-c")),
    P("בסיס: העצירה הראשונה של כל פתרון היא בטווח 5 מההתחלה, והחמדן לוקח את הרחוקה ביותר בטווח הזה.",
      do=show("e-1")),
    P("צעד, מקרה ראשון: העצירה הבאה של הפתרון האחר לא אחרי החמדן. החמדן תמיד מתקדם, אז הוא שוב לא מאחור.",
      do=show("e-2")),
    P("מקרה שני: היא אחרי החמדן. היא רחוקה לכל היותר 5 מהעצירה הנוכחית של הפתרון, שאינה אחרי החמדן."),
    P("אז גם מהחמדן מגיעים אליה, והחמדן עוצר בתחנה הרחוקה ביותר שבטווח. לכן הוא שוב לא מאחור."),
    P("סיום: אם הפתרון האחר מגיע ליעד אחרי כמה עצירות, החמדן באותו שלב רחוק לפחות כמוהו, ולכן גם הוא מגיע.",
      do=show("e-3")),
    P("שימו לב: לא מוכיחים שהחמדן **שווה** לפתרון האופטימלי. כאן הם שונים. מוכיחים שהוא לא מאחר.", do=show("e-t"),
      hold=0.4),
], stage=f'<div class="gp-stack">{POS}{RT}</div>',
   panel=st.card("e-c", "rule", "🔑 $g_r \\ge o_r$ לכל $r$: החמדן לא מאחור")
         + st.card("e-1", "plain", "בסיס: $o_1 \\le 5$, והחמדן לוקח את הרחוקה עד $5$")
         + st.card("e-2", "plain", "צעד: אם $o_{r+1} \\le g_r$, אז $g_{r+1} > g_r \\ge o_{r+1}$<br>"
                                   "אחרת $o_{r+1} \\le o_r + 5 \\le g_r + 5$")
         + st.card("e-3", "plain", "סיום: $20 \\le o_m + 5 \\le g_m + 5$")
         + st.card("e-t", "trap", "⚠️ לא מאחר ≠ זהה"))

closest = Scene("closest", "הכי קרוב לחמדן", [
    P("שיטה שקולה: מבין כל הפתרונות האופטימליים, בוחרים את זה שמתחיל הכי הרבה צעדים כמו החמדן."),
    P("במקום הראשון שבו הם נבדלים, מחליפים את הבחירה שלו בבחירה של החמדן.", do=show("cl0")),
    P("כאן הם נבדלים כבר בעצירה הראשונה: מחליפים 3 ב-4. מ-4 עדיין מגיעים ל-7, אז זה חוקי, ובאותו מספר עצירות.",
      do=show("cl1")),
    P("ובאופן כללי: עד המקום הזה הפתרונות זהים, אז לעצירה של החמדן מגיעים. והחמדן מקדים, אז היא רחוקה לפחות כמו המוחלפת.",
      do=show("c-g")),
    P("העצירה הבאה של הפתרון רחוקה לכל היותר 5 מהמוחלפת, ולכן גם מעצירת החמדן. ההחלפה חוקית, ובאותו גודל."),
    P("אבל זה פתרון אופטימלי שמתחיל **יותר** צעדים כמו החמדן. וזו סתירה לבחירה של הפתרון הקרוב ביותר.",
      do=show("c-r")),
    P("לכן הפתרון הקרוב ביותר הוא החמדן עצמו. בדוגמה, עוד שתי החלפות כאלה מגיעות בדיוק אליו.",
      do=show("cl2", "cl3"), hold=0.4),
], stage=f'<div class="gp-stack"><div class="gp-steps">'
         + "".join(f'<div id="cl{i}" class="h" style="display:flex;justify-content:center">'
                   + W.chips(f"c{i}", [str(x) for x in s], hidden=False, cls="small") + "</div>"
                   for i, s in enumerate(STEPS)) + '</div></div>',
   panel=st.card("c-g", "plain", "$g_{i+1} \\ge o_{i+1}$, ולכן $o_{i+2} \\le o_{i+1} + 5 \\le g_{i+1} + 5$")
         + st.card("c-r", "rule", "🔑 ההחלפה נותנת אופטימלי <b>קרוב יותר</b> לחמדן: סתירה לבחירה"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: ארגזים יוצאים מפס ייצור בסדר קבוע, וסוגרים אותם בסרטי הדבקה באורך $m$.",
      say="שאלה ממבחן: ארגזים יוצאים מפס ייצור בסדר קבוע, וסוגרים אותם בסרטי הדבקה באורך אֶם."),
    P("מותר לגזור סרט ולהמשיך איתו לארגז הבא. אבל ברגע שפותחים סרט חדש, השארית של הקודם נזרקת."),
    P("האלגוריתם: עוברים לפי הסדר. אם הארגז נכנס בשארית של הסרט הנוכחי, סוגרים בה. אחרת פותחים סרט חדש.",
      do=show("x-a")),
    P("מעבר אחד, בלי מיון, כי הסדר נתון: $O(n)$.", say="מעבר אחד, בלי מיון, כי הסדר נתון: או של אֶן."),
    P("נריץ על שמונה ארגזים, עם סרטים באורך 6.", do=show("bx")),
    P("סרט ראשון: 3 ו-2, ונשאר 1. הארגז 4 לא נכנס, אז סרט חדש: 4 ו-1.", do=show("tg-t0", "tg-t1")),
    P("סרט שלישי: 3 ו-2. וסרט רביעי: 5 ו-1. סך הכול ארבעה סרטים.", do=show("tg-t2", "tg-t3")),
    P("ובפחות אי אפשר: האורך הכולל הוא 21, ושלושה סרטים מכסים לכל היותר 18.", do=show("x-ok"), hold=0.3),
    P("ההוכחה: $a_r$ הוא מספר הארגזים שהחמדן סגר ב-$r$ הסרטים הראשונים, ו-$b_r$ אותו דבר בפתרון אחר כלשהו.",
      do=hide("bx") + show("to-t0", "to-t1", "to-t2", "to-t3"),
      say="ההוכחה: אֵיי אָר הוא מספר הארגזים שהחמדן סגר באָר הסרטים הראשונים, ובִּי אָר אותו דבר בפתרון אחר כלשהו."),
    P("למשל הפתרון התחתון, גם הוא בארבעה סרטים. הטענה: $a_r \\ge b_r$. כאן 2 מול 1, 4 מול 3, 6 מול 6, ו-8 מול 8.",
      do=show("ab-r0", "ab-r1", "ab-r2", "ab-r3"),
      say="למשל הפתרון התחתון, גם הוא בארבעה סרטים. הטענה: אֵיי אָר גדול או שווה לבִּי אָר. כאן שתיים מול אחת, ארבע מול שלוש, שש מול שש, ושמונה מול שמונה."),
    P("בסיס: בסרט הראשון החמדן סוגר את הרצף הארוך ביותר שנכנס, ולכן $a_1 \\ge b_1$.",
      say="בסיס: בסרט הראשון החמדן סוגר את הרצף הארוך ביותר שנכנס, ולכן אֵיי אחת גדול או שווה לבִּי אחת."),
    P("צעד: בפתרון האחר, הסרט הבא סוגר את הארגזים שאחרי $b_r$ עד $b_{r+1}$, ואורכם יחד לכל היותר $m$.",
      say="צעד: בפתרון האחר, הסרט הבא סוגר רצף של ארגזים שמתחיל מיד אחרי בִּי אָר, ואורכם יחד לכל היותר אֶם."),
    P("החמדן פותח את הסרט שלו באותו מקום או מאוחר יותר. הארגזים שלו עד $b_{r+1}$ הם חלק מאותו רצף, ולכן נכנסים.",
      say="החמדן פותח את הסרט שלו באותו מקום או מאוחר יותר. הארגזים שלו עד סוף אותו רצף הם חלק ממנו, ולכן נכנסים."),
    P("לכן $a_{r+1} \\ge b_{r+1}$.", do=show("x-1"),
      say="לכן גם אחרי הסרט הבא, החמדן סגר לפחות כמו הפתרון האחר."),
    P("סיום: אם הפתרון האחר סוגר הכול ב-$t$ סרטים, אז $a_t \\ge b_t = n$. החמדן לא צריך יותר מ-$t$ סרטים.",
      do=show("x-3"), say="סיום: אם הפתרון האחר סוגר הכול בטִי סרטים, אז גם החמדן סגר את כל הארגזים בטִי סרטים, ולא צריך יותר."),
    P("המלכודת: להוכיח רק שהסרט הראשון של החמדן מלא ככל האפשר. בלי האינדוקציה, ההוכחה לא נגמרת.", do=show("x-t"),
      hold=0.5),
], stage=f'<div class="gp-stack"><div id="bx" class="h">{BOXES}</div>'
         '<div style="display:flex;gap:40px;align-items:flex-start;direction:rtl">'
         f'<div><div class="gp-note">חמדן</div>{TG}</div>'
         f'<div><div class="gp-note">פתרון אחר</div>{TO}</div></div>'
         '<div style="display:flex;gap:30px;align-items:center;direction:rtl">'
         f'<div id="x-ok" class="gp-mid h">$21 > 3 \\cdot 6$</div>{AB}</div></div>',
   panel='<div class="qstem"><span class="qid">24A-B-Q2a/b</span>ארגזים יוצאים לפי הסדר; סרטי הדבקה באורך $m$. '
         'מספר מינימלי של סרטים. (א) אלגוריתם. (ב) הוכחה.</div>'
         + st.card("x-a", "rule", "🔑 נכנס בשארית? סוגרים בה. אחרת: סרט חדש")
         + st.card("x-1", "plain", "$a_1 \\ge b_1$, ו-$a_r \\ge b_r \\Rightarrow a_{r+1} \\ge b_{r+1}$")
         + st.card("x-3", "rule", "🔑 $a_t \\ge b_t = n$: החמדן לא משתמש ביותר סרטים")
         + st.card("x-t", "trap", "⚠️ הסרט הראשון לבד אינו הוכחה"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: כשהפתרון הוא רשימה לפי הסדר, מוכיחים באינדוקציה שהחמדן אף פעם לא מאחר.", do=show("r-1")),
    P("ובסוף: אילו לפתרון האחר היה יותר, החמדן לא היה עוצר. או: מתחילים מהאופטימלי הקרוב ביותר לחמדן.", do=show("r-2")),
    P("ולא מוכיחים שהחמדן זהה לאופטימום, רק שהוא לא מאחר. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage='<div class="gp-stack"><div class="gp-big">$g_r \\ge o_r$</div><div class="gp-big">$a_r \\ge b_r$</div></div>',
   panel=st.card("r-1", "rule", "🔑 החמדן מקדים: אינדוקציה על השלבים")
         + st.card("r-2", "rule", "🔑 הכי קרוב לחמדן: ההחלפה מאריכה את הרישא, סתירה")
         + st.card("r-3", "trap", "⚠️ לא מאחר, ולא בהכרח זהה"))

VIDEO = Video("G05", "greedy_proofs", 'החמדן מקדים ו"הכי קרוב לחמדן"', [title, idea, ex, closest, exam, recap],
              bank={"24A-B-Q2a": None, "24A-B-Q2b": None})
