# -*- coding: utf-8 -*-
"""G03 · טיעון ההחלפה, צעד אחר צעד — video script (build: tools/video/vid.py G03).

Source: courses/greedy_proofs/C03.js (goal: prove that some optimal solution contains the first greedy choice, and spot
the step that is missing in a failed proof). Exam anchors: 22A-C-Q3a (pair 2n products, the cheaper of each pair is
free: a greedy) and 22A-C-Q3b (prove the greedy choice property), open questions no guided level uses.
Avoided on purpose: the C03 quiz items (the earliest-finish proof lines, O={[1,10],[11,20]} with g=[9,12], the budget
exchange with the cheapest item) and the lesson's data. The worked exchange uses a new 5-interval input; the broken
exchange uses G02's own counterexample [0,6],[5,8],[7,12].
All picks, optima and payments are computed below and checked by brute force.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_greedy_proofs as W

CHK = W.CHK
EF = lambda x: (x[1], x[0])

# ---------------------------------------------------------------- worked exchange (earliest finish)
IV = [(2, 5), (1, 4), (6, 8), (3, 7), (9, 11)]
G_I, O_SET = 1, (0, 2, 4)                            # g = [1,4]; O = {[2,5],[6,8],[9,11]}
assert W.iv_greedy_run(IV, EF)[0][0] == G_I and min(IV, key=EF) == IV[G_I]
assert CHK.iv_opt(IV) == 3 and O_SET in W.iv_all_optima(IV) and G_I not in O_SET
O_I = min(O_SET, key=lambda i: IV[i][1])              # o = the interval of O that ends first
assert O_I == 0 and IV[G_I][1] <= IV[O_I][1]
O2 = tuple(sorted(set(O_SET) - {O_I} | {G_I}))
assert O2 in W.iv_all_optima(IV)                      # O' = {[1,4],[6,8],[9,11]}: legal and the same size
assert all(IV[i][0] > IV[O_I][1] for i in O_SET if i != O_I)   # the rest of O starts after f(o) >= f(g)

# ---------------------------------------------------------------- the broken exchange (shortest first)
B = [(0, 6), (5, 8), (7, 12)]
assert min(range(3), key=lambda i: (B[i][1] - B[i][0], B[i][0])) == 1
assert W.iv_all_optima(B) == [(0, 2)]
assert W.conflict(B[1], B[2]) and W.conflict(B[1], B[0])        # g clashes with whichever interval stays

# ---------------------------------------------------------------- exam 22A-C-Q3: pairs, the cheaper one free
QA, QB = BANK["22A-C-Q3a"], BANK["22A-C-Q3b"]
assert QA["contextId"] == QB["contextId"] == "22A-C-c3"
PR = [3, 8, 5, 12, 6, 9]


def pay(pairs):
    return sum(max(p) for p in pairs)


def all_pairings(items):
    if not items:
        yield []
        return
    a, rest = items[0], items[1:]
    for i in range(len(rest)):
        for more in all_pairings(rest[:i] + rest[i + 1:]):
            yield [(a, rest[i])] + more


S = sorted(PR)
GREEDY = [(S[2 * i], S[2 * i + 1]) for i in range(3)]
assert GREEDY == [(3, 5), (6, 8), (9, 12)] and pay(GREEDY) == 25
PAIRINGS = list(all_pairings(PR))
assert len(PAIRINGS) == 15 and min(pay(p) for p in PAIRINGS) == 25
ANY = [(3, 8), (5, 12), (6, 9)]
SWAP = [(3, 5), (8, 12), (6, 9)]
assert sorted(sum(ANY, ())) == S and sorted(sum(SWAP, ())) == S       # both are partitions into pairs
x, y = 8, 12
assert pay(ANY) == 29 and pay(SWAP) == 26 and x + y == 20 and 5 + max(x, y) == 17 and min(x, y) >= S[1]
# the proof on every multiset of 6 prices from 1..6: in every pairing where p1, p2 are apart, the swap never raises the
# payment of the two changed pairs, and the greedy pairing is optimal
import itertools
for prices in itertools.combinations_with_replacement(range(1, 7), 6):
    s = list(prices)                                   # already sorted
    pairings = list(all_pairings(list(range(6))))      # pair positions, so equal prices stay distinct items
    for p in pairings:
        k1 = next(q for q in p if 0 in q)
        k2 = next(q for q in p if 1 in q)
        if k1 == k2:
            continue
        xo, yo = s[k1[0] + k1[1] - 0], s[k2[0] + k2[1] - 1]
        assert xo >= s[1] and yo >= s[1] and s[1] + max(xo, yo) <= xo + yo
    best = min(sum(max(s[a], s[b]) for a, b in p) for p in pairings)
    assert pay([(s[2 * i], s[2 * i + 1]) for i in range(3)]) == best


def pair_chip(a, b):
    return f'<span class="gp-pair"><span class="gp-free">{a}</span><span class="gp-paid">{b}</span></span>'


def pair_row(rid, label, pairs, total):
    return (f'<div id="{rid}" class="gp-row h"><span class="gp-rl">{label}</span>'
            + W.chips(f"{rid}-c", [pair_chip(*p) for p in pairs], hidden=False)
            + f'<span class="gp-sum">{total}</span></div>')


TL = W.timeline("tl", IV, 0, 12, w=900)
TB = W.timeline("tb", B, 0, 12, w=900)
SORTED = W.chips("ps", [str(p) for p in S], hidden=False, cls="small")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נבנה את החלק הראשון של כל הוכחה חמדנית: טיעון ההחלפה."),
    P("נעבור על ארבעת הצעדים, ונראה בדיוק איפה הוכחה של כלל שגוי נשברת."),
    P("ובסוף נוכיח סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">G03 · אלגוריתם חמדן והוכחת נכונות</div><h1>טיעון ההחלפה, צעד אחר צעד</h1>'
         '<p>להוכיח שיש פתרון אופטימלי שמכיל את הבחירה החמדנית הראשונה, ולזהות את הצעד שחסר בהוכחה כושלת.</p>',
   layout="title")

idea = Scene("idea", "ארבעה צעדים", [
    P("הוכחה של אלגוריתם חמדן בנויה משני חלקים. הראשון נקרא **תכונת הבחירה החמדנית**."),
    P("היא אומרת: **קיים** פתרון אופטימלי שמכיל את הבחירה הראשונה של החמדן.", do=show("i-r")),
    P("מוכיחים אותה בארבעה צעדים. אחד: נותנים שמות. $g$ הבחירה החמדנית, ו-$O$ פתרון אופטימלי כלשהו.",
      do=show("i-1"), say="מוכיחים אותה בארבעה צעדים. אחד: נותנים שמות. גִ'י הבחירה החמדנית, ואוֹ פתרון אופטימלי כלשהו."),
    P("שתיים: אם $g$ לא ב-$O$, מוצאים ב-$O$ איבר $o$ שתופס את המקום של $g$.", do=show("i-2"),
      say="שתיים: אם גִ'י לא באוֹ, מוצאים באוֹ איבר, נקרא לו אוֹ קטנה, שתופס את המקום של גִ'י."),
    P("שלוש: מחליפים את $o$ ב-$g$, ומנמקים בעזרת הכלל למה $g$ טוב לפחות כמו $o$.", do=show("i-3"),
      say="שלוש: מחליפים את האיבר הזה בגִ'י, ומנמקים בעזרת הכלל למה גִ'י טוב לפחות כמוהו."),
    P("ארבע: מראים **שני** דברים על הפתרון החדש. שהוא חוקי, ושערכו לא גרוע.", do=show("i-4", "i-t"), hold=0.4),
], stage='<div class="gp-stack"><div class="gp-steps">'
         '<div id="i-1" class="h"><span class="n">1</span>$g$ = הבחירה החמדנית, $O$ = אופטימלי כלשהו. אם $g \\in O$, סיימנו</div>'
         '<div id="i-2" class="h"><span class="n">2</span>מוצאים $o \\in O$ שתופס את המקום של $g$</div>'
         '<div id="i-3" class="h"><span class="n">3</span>$O\' = (O \\setminus \\{o\\}) \\cup \\{g\\}$, ונימוק מהכלל</div>'
         '<div id="i-4" class="h"><span class="n">4</span>$O\'$ <b>חוקי</b>, וערכו <b>לא גרוע</b> מזה של $O$</div>'
         '</div></div>',
   panel=st.card("i-r", "rule", "🔑 תכונת הבחירה החמדנית: <b>קיים</b> אופטימלי שמכיל את $g$")
         + st.card("i-t", "trap", "⚠️ צריך את שניהם: חוקיות וערך. אחד מהם לא מספיק"))

SAY_O = "אוֹ קטנה"
ex = Scene("ex", "החלפה בקטעים", [
    P("נראה את ארבעת הצעדים על הכלל המסתיים ראשון, עם חמישה קטעים.", do=show("tl")),
    P("צעד אחד: $g$ הוא הקטע שמסתיים ראשון, מ-1 עד 4. ו-$O$ הוא פתרון אופטימלי, שלושת הקטעים המסומנים.",
      do=show("tl-g1", "tl-h0", "tl-h2", "tl-h4"),
      say="צעד אחד: גִ'י הוא הקטע שמסתיים ראשון, מאחת עד ארבע. ואוֹ הוא פתרון אופטימלי, שלושת הקטעים המסומנים."),
    P("$g$ לא נמצא ב-$O$, אז צריך להחליף.", say="גִ'י לא נמצא באוֹ, אז צריך להחליף."),
    P("צעד שתיים: ב-$O$, הקטע שמסתיים ראשון הוא $o$, מ-2 עד 5.", do=show("tl-v1"),
      say=f"צעד שתיים: באוֹ, הקטע שמסתיים ראשון הוא {SAY_O}, משתיים עד חמש."),
    P("צעד שלוש: מוציאים את $o$ ומכניסים את $g$.", do=hide("tl-h0") + show("tl-x0", "tl-h1"),
      say=f"צעד שלוש: מוציאים את {SAY_O} ומכניסים את גִ'י."),
    P("הנימוק מהכלל: $g$ מסתיים ראשון מכולם, ולכן $f(g) \\le f(o)$. כאן 4 מול 5.", do=show("tl-v0", "e-1"),
      say=f"הנימוק מהכלל: גִ'י מסתיים ראשון מכולם, ולכן הסוף של גִ'י קטן או שווה לסוף של {SAY_O}. כאן ארבע מול חמש."),
    P("צעד ארבע, חוקיות: שאר הקטעים של $O$ זרים ל-$o$ ומסתיימים אחריו, ולכן מתחילים אחרי $f(o)$.",
      say=f"צעד ארבע, חוקיות: שאר הקטעים של אוֹ זרים ל{SAY_O} ומסתיימים אחריו, ולכן מתחילים אחרי סופו."),
    P("ומכיוון ש-$f(o) \\ge f(g)$, הם מתחילים גם אחרי הסוף של $g$. אין אף התנגשות.", do=show("e-2"),
      say="ומכיוון שסופו גדול או שווה לסוף של גִ'י, הם מתחילים גם אחרי הסוף של גִ'י. אין אף התנגשות."),
    P("וערך: הגודל לא השתנה, שלושה קטעים. לכן $O'$ אופטימלי, והוא מכיל את $g$.", do=show("e-3"),
      say="וערך: הגודל לא השתנה, שלושה קטעים. לכן אוֹ פְּרַיים אופטימלי, והוא מכיל את גִ'י.", hold=0.4),
], stage=f'<div class="gp-stack"><div id="tl" class="h">{W.timeline("tl", IV, 0, 12, w=900, guides=[(4, "f(g)"), (5, "f(o)")])}</div></div>',
   panel=st.card("e-1", "ex", "$f(g) = 4 \\le 5 = f(o)$")
         + st.card("e-2", "rule", "🔑 חוקי: שאר $O$ מתחילים אחרי $f(o) \\ge f(g)$")
         + st.card("e-3", "rule", "🔑 $|O'| = |O| = 3$, ולכן $O'$ אופטימלי ומכיל את $g$"))

broken = Scene("broken", "איפה זה נשבר", [
    P("ועכשיו ננסה להוכיח כלל שגוי: הקצר ביותר קודם, על הדוגמה הנגדית שראינו.", do=show("tb")),
    P("$g$ הוא הקטע הקצר, מ-5 עד 8. ו-$O$ הוא האופטימום: מאפס עד 6, ומ-7 עד 12.",
      do=show("tb-g1", "tb-h0", "tb-h2"),
      say="גִ'י הוא הקטע הקצר, מחמש עד שמונה. ואוֹ הוא האופטימום: מאפס עד שש, ומשבע עד שתים עשרה."),
    P("נחליף את הקטע הראשון ב-$g$: נשאר הקטע מ-7 עד 12, וחופף ל-$g$ בין 7 ל-8.",
      do=show("tb-x0", "b-1"), say="נחליף את הקטע הראשון בגִ'י: נשאר הקטע משבע עד שתים עשרה, וחופף לגִ'י בין שבע לשמונה."),
    P("נחליף את השני במקומו: נשאר הקטע מאפס עד 6, וחופף ל-$g$ בין 5 ל-6.",
      do=hide("tb-x0") + show("tb-x2", "b-2"), say="נחליף את השני במקומו: נשאר הקטע מאפס עד שש, וחופף לגִ'י בין חמש לשש."),
    P("בשתי הדרכים הפתרון החדש **לא חוקי**. הערך בסדר, אבל החוקיות נשברה.", do=show("b-t")),
    P("וזה הסימן: כשצעד החוקיות לא מסתדר, כנראה שיש לכלל דוגמה נגדית. וכאן באמת יש.", hold=0.4),
], stage=f'<div class="gp-stack"><div id="tb" class="h">{TB}</div></div>',
   panel=st.card("b-1", "plain", "$[5,8]$ ו-$[7,12]$: חפיפה ב-$[7,8]$")
         + st.card("b-2", "plain", "$[0,6]$ ו-$[5,8]$: חפיפה ב-$[5,6]$")
         + st.card("b-t", "trap", "⚠️ הצעד שנשבר בכלל שגוי הוא <b>החוקיות</b>"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: במבצע, מי שקונה זוג מוצרים מקבל את הזול מביניהם בחינם."),
    P("יש $2n$ מוצרים, ומחלקים אותם ל-$n$ זוגות. רוצים לשלם כמה שפחות.",
      say="יש שתיים אֶן מוצרים, ומחלקים אותם לאֶן זוגות. רוצים לשלם כמה שפחות."),
    P("בכל זוג משלמים רק על היקר. הסעיף הראשון: אלגוריתם חמדני.", do=show("ps")),
    P("ממיינים מהזול ליקר, ומזווגים לפי הסדר: הראשון עם השני, השלישי עם הרביעי, וכן הלאה.", do=show("x-a")),
    P("במחירים 3, 8, 5, 12, 6 ו-9: הזוגות הם 3 עם 5, 6 עם 8, ו-9 עם 12. משלמים 5, 8 ו-12, כלומר 25.",
      do=show("rg")),
    P("בדיקה של כל 15 החלוקות לזוגות מאשרת ש-25 הוא המינימום.", hold=0.3),
    P("סעיף ההוכחה: הבחירה הראשונה היא הזוג של שני הזולים, $p_1$ ו-$p_2$. יהי $OPT$ אופטימלי.",
      say="סעיף ההוכחה: הבחירה הראשונה היא הזוג של שני הזולים, פִּי אחת ופִּי שתיים. יהי אוֹפְּט פתרון אופטימלי."),
    P("אם הם כבר באותו זוג, סיימנו. אחרת יש בו זוג של $p_1$ עם $x$, וזוג של $p_2$ עם $y$.", do=show("x-1"),
      say="אם הם כבר באותו זוג, סיימנו. אחרת יש בו זוג של פִּי אחת עם אִקְס, וזוג של פִּי שתיים עם וַואי."),
    P("כל מוצר אחר עולה לפחות $p_2$, ולכן $x, y \\ge p_2$. בשני הזוגות משלמים $x + y$.",
      say="כל מוצר אחר עולה לפחות פִּי שתיים, ולכן אִקְס ווַואי גדולים או שווים לפִּי שתיים. בשני הזוגות משלמים אִקְס ועוד וַואי."),
    P("מחליפים: $p_1$ עם $p_2$, ו-$x$ עם $y$. עכשיו משלמים $p_2$ ועוד המקסימום של $x$ ו-$y$.", do=show("x-2"),
      say="מחליפים: פִּי אחת עם פִּי שתיים, ואִקְס עם וַואי. עכשיו משלמים פִּי שתיים ועוד המקסימום של אִקְס ווַואי."),
    P("חוקיות: עדיין יש $n$ זוגות, וכל מוצר נמצא בדיוק בזוג אחד.", say="חוקיות: עדיין יש אֶן זוגות, וכל מוצר נמצא בדיוק בזוג אחד."),
    P("ערך: $x+y$ הוא המקסימום ועוד המינימום, והמינימום לפחות $p_2$. לכן התשלום לא עלה.", do=show("x-3"),
      say="ערך: אִקְס ועוד וַואי הוא המקסימום ועוד המינימום, והמינימום לפחות פִּי שתיים. לכן התשלום לא עלה."),
    P("בדוגמה: החלוקה 3 עם 8, 5 עם 12, ו-6 עם 9 עולה 29.", do=show("ra")),
    P("ההחלפה נותנת 3 עם 5, ו-8 עם 12. בזוגות האלה משלמים 17 במקום 20, ובסך הכול 26.", do=show("rs")),
    P("לכן החלוקה החדשה אופטימלית לפחות כמו $OPT$, והיא מכילה את הבחירה החמדנית.",
      say="לכן החלוקה החדשה אופטימלית לפחות כמו אוֹפְּט, והיא מכילה את הבחירה החמדנית."),
    P("המלכודת: לחשב רק את הזוג החדש. צריך את התשלום על **שני** הזוגות שהשתנו.", do=show("x-t"), hold=0.5),
], stage=f'<div class="gp-stack"><div id="ps" class="h">{SORTED}</div>'
         + pair_row("rg", "חמדן:", GREEDY, 25) + pair_row("ra", "חלוקה כלשהי:", ANY, 29)
         + pair_row("rs", "אחרי ההחלפה:", SWAP, 26)
         + '<div id="x-3" class="gp-big h">$x + y = \\max + \\min \\ \\ge\\ \\max(x,y) + p_2$</div></div>',
   panel='<div class="qstem"><span class="qid">22A-C-Q3a/b</span>$2n$ מוצרים נקנים ב-$n$ זוגות, ובכל זוג הזול '
         'בחינם. (א) אלגוריתם חמדני לתשלום מינימלי. (ב) הוכיחו את תכונת הבחירה החמדנית.</div>'
         + st.card("x-a", "rule", "🔑 ממיינים, ומזווגים צמודים: $(p_1,p_2), (p_3,p_4), \\dots$")
         + st.card("x-1", "plain", "$(p_1, x), (p_2, y)$, עם $x, y \\ge p_2$")
         + st.card("x-2", "ex", "$\\to\\ (p_1, p_2), (x, y)$")
         + st.card("x-t", "trap", "⚠️ מחשבים את התשלום על <b>שני</b> הזוגות שהשתנו"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: תכונת הבחירה החמדנית אומרת שקיים אופטימלי שמכיל את הבחירה הראשונה.", do=show("r-1")),
    P("מוכיחים בהחלפה: שמות, מה מחליפים, ההחלפה עם נימוק מהכלל, ואז חוקיות וערך.", do=show("r-2")),
    P("וכשהחוקיות נשברת, מחפשים דוגמה נגדית. ברמה הבאה נשלים את החלק השני של ההוכחה.", do=show("r-3"), hold=0.6),
], stage='<div class="gp-stack"><div class="gp-big">$O\' = (O \\setminus \\{o\\}) \\cup \\{g\\}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 קיים אופטימלי שמכיל את $g$")
         + st.card("r-2", "rule", "🔑 החלפה, ואז <b>חוקי</b> + <b>לא גרוע</b>")
         + st.card("r-3", "trap", "⚠️ חוקיות נשברת? כנראה יש דוגמה נגדית"))

VIDEO = Video("G03", "greedy_proofs", "טיעון ההחלפה, צעד אחר צעד", [title, idea, ex, broken, exam, recap],
              bank={"22A-C-Q3a": None, "22A-C-Q3b": None})
