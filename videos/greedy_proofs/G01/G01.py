# -*- coding: utf-8 -*-
"""G01 · מהו אלגוריתם חמדן — video script (build: tools/video/vid.py G01).

Source: courses/greedy_proofs/C01.js (lesson + goal: run a greedy on a small example, and explain why an example that
works is not a proof). Exam anchor: 23A-A-Q4a (fill a bag of W kg with the fewest items, weights P_i = 5 P_{i+1},
P_K = 1): an open question, not used by any guided level.
Avoided on purpose: the C01 quiz data (coins 1,5,10,25 with 63; coins 1,3,4 with 6; coins 1,5,12) and every other
level's quiz. The worked examples are new: coins 1,2,5,10 with 18, and coins 1,6,10 (greedy fails first at 12).
Every run is computed below and compared with the course checker's brute force (CHK.coins_opt).
"""
import itertools
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_greedy_proofs as W

CHK = W.CHK


def greedy_coins(coins, amount):
    """[(remaining before, coin taken, remaining after)]"""
    steps = []
    for c in sorted(coins, reverse=True):
        while amount >= c:
            steps.append((amount, c, amount - c))
            amount -= c
    assert amount == 0
    return steps


# ---------------------------------------------------------------- example 1: shekels, greedy is optimal
S1 = greedy_coins([1, 2, 5, 10], 18)
assert [c for _, c, _ in S1] == [10, 5, 2, 1]
assert CHK.coins_opt([1, 2, 5, 10], 18) == 4
assert not any(sum(t) == 18 for r in range(1, 4) for t in itertools.combinations_with_replacement([1, 2, 5, 10], r))

# ---------------------------------------------------------------- example 2: coins 1,6,10, greedy fails
S2 = greedy_coins([1, 6, 10], 12)
assert [c for _, c, _ in S2] == [10, 1, 1] and CHK.coins_opt([1, 6, 10], 12) == 2 and 6 + 6 == 12
GRID = list(range(1, 21))
OKS = {a: len(greedy_coins([1, 6, 10], a)) == CHK.coins_opt([1, 6, 10], a) for a in GRID}
FAILS = [a for a in GRID if not OKS[a]]
assert FAILS == [12, 13, 14, 15, 18, 19] and all(OKS[a] for a in range(1, 12))

# ---------------------------------------------------------------- exam 23A-A-Q4a: weights 125, 25, 5, 1 (K = 4)
Q = BANK["23A-A-Q4a"]
assert Q["contextId"] == "23A-A-c4" and "מספר מינימלי של פריטים" in Q["question"]
PW = [125, 25, 5, 1]
assert all(PW[i] == 5 * PW[i + 1] for i in range(3)) and PW[-1] == 1


def fill(Wkg):
    rows, R = [], Wkg
    for p in PW:
        c = R // p
        rows.append((R, p, c, R - c * p))
        R -= c * p
    assert R == 0
    return rows


ROWS = fill(143)
assert [r[2] for r in ROWS] == [1, 0, 3, 3] and sum(r[2] for r in ROWS) == 7
assert CHK.coins_opt(PW, 143) == 7
assert all(sum(r[2] for r in fill(w)) == CHK.coins_opt(PW, w) for w in range(1, 800))   # greedy = optimum, W < 800

# ---------------------------------------------------------------- widgets
T1 = W.table("t1", ["נשאר", "מטבע", "נשאר אחרי"], [[str(a), str(c), str(b)] for a, c, b in S1])
COINS1 = W.chips("k1", ["1", "2", "5", "10"], hidden=False, cls="coin")
G2 = W.chips("g2", ["10", "1", "1"], cls="coin", label="חמדן:")
O2 = W.chips("o2", ["6", "6"], cls="coin", label="אופטימום:")
GR = W.chips("gr", [str(a) for a in GRID], cls="small")
PWC = W.chips("pw", [str(p) for p in PW], hidden=False)
TX = W.table("tx", ["נשאר", "משקל", "כמה נכנסים", "נשאר אחרי"],
             [[str(R), str(p), str(c), str(a)] for R, p, c, a in ROWS])

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את האלגוריתם החמדן."),
    P("נריץ אותו על דוגמאות קטנות, ונראה למה דוגמה שעובדת עדיין איננה הוכחה."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">G01 · אלגוריתם חמדן והוכחת נכונות</div><h1>מהו אלגוריתם חמדן</h1>'
         '<p>להריץ אלגוריתם חמדן על דוגמה קטנה, ולהסביר למה דוגמה שעובדת עדיין אינה הוכחה.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("אלגוריתם חמדן בונה פתרון בשלבים."),
    P("בכל שלב הוא בוחר את מה שנראה הכי טוב **עכשיו**, ולא חוזר לתקן.", do=show("i-r")),
    P("כמעט תמיד המבנה הוא: קודם ממיינים את האיברים לפי כלל כלשהו.", do=show("i-1")),
    P("ואחר כך עוברים בסדר הזה, ולוקחים כל איבר שעדיין אפשר לקחת.", do=show("i-2")),
    P("לכן זמן הריצה הוא מיון ועוד מעבר אחד: $O(n\\,\\log\\,n)$.", do=show("i-o", "i-e"),
      say="לכן זמן הריצה הוא מיון ועוד מעבר אחד: או של אֶן לוֹג אֶן."),
    P("השאלה האמיתית היא לא איך מריצים, אלא **מתי** הכלל נותן תמיד את הפתרון הטוב ביותר.", hold=0.4),
], stage='<div class="gp-stack"><div class="gp-steps">'
         '<div id="i-1" class="h"><span class="n">1</span>ממיינים לפי כלל: הגדול, הקטן, המסתיים ראשון…</div>'
         '<div id="i-2" class="h"><span class="n">2</span>עוברים בסדר, ולוקחים כל איבר שעדיין אפשר</div></div>'
         '<div id="i-o" class="gp-big h">$O(n\\,\\log\\,n) + O(n) = O(n\\,\\log\\,n)$</div></div>',
   panel=st.card("i-r", "rule", "🔑 חמדן: בוחר את מה שנראה הכי טוב עכשיו, ולא חוזר אחורה")
         + st.card("i-e", "ex", "זמן: מיון, ועוד מעבר אחד על הרשימה"))

ex1 = Scene("ex1", "עודף בשקלים", [
    P("דוגמה ראשונה: מטבעות של 1, 2, 5 ו-10 שקלים, וצריך לתת עודף של 18 שקלים."),
    P("רוצים כמה שפחות מטבעות. הכלל החמדן: תמיד המטבע הגדול ביותר שעוד נכנס.", do=show("e1-c")),
    P("נשארו 18: המטבע הגדול שנכנס הוא 10, ונשארים 8.", do=show("t1-r0")),
    P("נשארו 8: עשר כבר לא נכנס, אז 5, ונשארים 3.", do=show("t1-r1")),
    P("נשארו 3: מטבע של 2, ונשאר 1.", do=show("t1-r2")),
    P("ומטבע אחרון של 1. סך הכול ארבעה מטבעות.", do=show("t1-r3"), hold=0.3),
    P("האם אפשר בפחות? בדקנו את כל הצירופים של שלושה מטבעות או פחות: אף אחד מהם לא מגיע ל-18.", do=show("e1-k")),
    P("אז כאן החמדן נתן את המינימום.", hold=0.4),
], stage=f'<div class="gp-stack">{COINS1}{T1}</div>',
   panel=st.card("e1-c", "rule", "🔑 הכלל: המטבע הגדול ביותר שעוד נכנס")
         + st.card("e1-k", "ex", "✓ $10+5+2+1$: ארבעה מטבעות, ואין צירוף של שלושה שנותן 18"))

ex2 = Scene("ex2", "כשהחמדן נכשל", [
    P("עכשיו נחליף את המטבעות: 1, 6 ו-10, וצריך לתת 12."),
    P("החמדן לוקח 10, ונשארים 2: עוד מטבע של 1, ועוד אחד. שלושה מטבעות.", do=show("g2-0", "g2-1", "g2-2")),
    P("אבל 6 ועוד 6 זה 12, בשני מטבעות בלבד.", do=show("o2-0", "o2-1")),
    P("אותו כלל בדיוק, והפעם הוא לא אופטימלי: הבחירה של 10 חסמה את הפתרון הקצר.", do=show("e2-t")),
    P("ועכשיו הנקודה החשובה. נריץ את החמדן על כל הסכומים, מ-1 עד 20.",
      do=show(*[f"gr-{i}" for i in range(len(GRID))])),
    P("בירוק: סכומים שבהם החמדן נתן את המינימום. באדום: סכומים שבהם הוא נכשל.",
      do=show(*[f"gr-{i}-{'ok' if OKS[a] else 'x'}" for i, a in enumerate(GRID)])),
    P("מ-1 עד 11 הוא תמיד צודק. מי שבדק רק אותם היה בטוח שהכלל נכון."),
    P("לכן דוגמאות יכולות רק **להפריך**. כדי לטעון שחמדן נכון, צריך הוכחה.", do=show("e2-r"), hold=0.4),
], stage=f'<div class="gp-stack">{G2}{O2}<div style="height:16px"></div>{GR}</div>',
   panel=st.card("e2-t", "trap", "⚠️ מטבעות 1, 6, 10 ותשלום 12: החמדן 3 מטבעות, האופטימום 2")
         + st.card("e2-r", "rule", "🔑 דוגמה שעובדת היא לא הוכחה. דוגמה נגדית אחת מספיקה כדי להפריך"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: שק שנושא בדיוק $W$ קילו, ופריטים מ-$K$ סוגים, בלי הגבלה על הכמות.",
      say="שאלה ממבחן: שק שנושא בדיוק דַאבְּלְיוּ קילו, ופריטים מקֵיי סוגים, בלי הגבלה על הכמות."),
    P("הסוג האחרון שוקל 1, וכל סוג שוקל פי חמישה מהסוג שאחריו. למשל 125, 25, 5 ו-1.", do=show("x-w")),
    P("צריך למלא את כל השק במספר מינימלי של פריטים. זו בעצם בעיית העודף, עם מטבעות מיוחדים."),
    P("האלגוריתם: עוברים מהסוג הכבד לקל, ומכל סוג לוקחים כמה שיותר פריטים שעוד נכנסים.", do=show("x-a")),
    P("בסוף השק מלא בדיוק, כי הסוג האחרון שוקל 1. כל סוג נבדק פעם אחת, אז הזמן $O(K)$.",
      say="בסוף השק מלא בדיוק, כי הסוג האחרון שוקל אחת. כל סוג נבדק פעם אחת, אז הזמן או של קֵיי."),
    P("נריץ על שק של 143 קילו. מ-125 נכנס פריט אחד, ונשארים 18.", do=show("tx-r0")),
    P("פריט של 25 כבר לא נכנס ב-18, אז אפס פריטים מהסוג הזה.", do=show("tx-r1")),
    P("מ-5 נכנסים שלושה, ונשארים 3. ומ-1 לוקחים שלושה.", do=show("tx-r2", "tx-r3")),
    P("סך הכול 7 פריטים. חיפוש מלא על כל האפשרויות מאשר: אי אפשר בפחות.", do=show("x-ok"), hold=0.3),
    P("אבל למה כאן החמדן תמיד צודק, ובמטבעות 1, 6, 10 לא? כי חמישה פריטים מסוג אחד שוקלים כמו פריט אחד מהסוג שמעליו.",
      do=show("x-t")),
    P("לכן בפתרון אופטימלי אין חמישה פריטים מאותו סוג קל: היינו מחליפים אותם בפריט אחד, וחוסכים ארבעה."),
    P("זה רעיון של **החלפה**. את ההוכחה המלאה, בחירה חמדנית ותת-מבנה, נלמד לבנות ברמות הבאות.", hold=0.5),
], stage=f'<div class="gp-stack"><div id="x-w" class="h">{PWC}</div>{TX}'
         + st.card("x-ok", "ex", "✓ $125+5+5+5+1+1+1$: שבעה פריטים, וזה המינימום") + "</div>",
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>שק בקיבולת $W$, פריטים מ-$K$ סוגים בכמות לא מוגבלת, '
         '$P_i = 5P_{i+1}$ ו-$P_K = 1$. מצאו אלגוריתם חמדני שממלא את כל השק במספר מינימלי של פריטים.</div>'
         + st.card("x-a", "rule", "🔑 מהכבד לקל: מכל סוג $\\lfloor R / P_i \\rfloor$ פריטים")
         + st.card("x-t", "trap", "⚠️ הסיבה: $5 \\cdot P_{i+1} = P_i$, חמישה קלים שווים לכבד אחד"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: חמדן ממיין לפי כלל ועובר פעם אחת, ובכל שלב לוקח את מה שנראה הכי טוב.", do=show("r-1")),
    P("הכלל של המטבע הגדול עבד ב-1, 2, 5, 10, ונכשל ב-1, 6, 10 כבר בסכום 12.", do=show("r-2")),
    P("דוגמאות מפריכות, הוכחה מוכיחה. ברמה הבאה נלמד לשבור כלל בעזרת דוגמה נגדית.", do=show("r-3"), hold=0.6),
], stage='<div class="gp-stack"><div class="gp-big">$O(n\\,\\log\\,n)$</div></div>',
   panel=st.card("r-1", "rule", "🔑 חמדן = מיון לפי כלל + מעבר אחד")
         + st.card("r-2", "trap", "⚠️ 1, 6, 10 ו-12: החמדן 3, האופטימום 2")
         + st.card("r-3", "rule", "🔑 דוגמאות מפריכות, הוכחה מוכיחה"))

VIDEO = Video("G01", "greedy_proofs", "מהו אלגוריתם חמדן", [title, idea, ex1, ex2, exam, recap],
              bank={"23A-A-Q4a": None})
