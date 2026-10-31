# -*- coding: utf-8 -*-
"""G07 · הופמן כאלגוריתם חמדני — video script (build: tools/video/vid.py G07).

Source: courses/greedy_proofs/C07.js (goal: build a Huffman tree and its cost, the exchange lemma, ropes in disguise,
arbitrary ties). Exam anchor: 26A-A-Q3a (the Huffman code of a=22, b=15, c=3, d=24, e=4, f=10, g=8), an open question
no guided level uses.
Avoided on purpose: the C07 quiz/lesson data (5,9,12,13,16,45; ropes 1..5; 1,1,2,2) and 22A-B-Q4a/b (the ropes,
boss items of C08). New worked data: frequencies 2,3,5,7,11. Every merge is a valid Huffman run
(W.huffman_is_valid_run), every cost is computed twice (internal nodes and sum f*depth) and checked with
CHK.huffman_cost; the tie in the exam is resolved both ways and both give 219.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_greedy_proofs as W

CHK = W.CHK

# ---------------------------------------------------------------- worked: 2, 3, 5, 7, 11
IT = [("a", 2), ("b", 3), ("c", 5), ("d", 7), ("e", 11)]
NODES, MER = W.huffman_run(IT)
assert W.huffman_is_valid_run(IT, MER)
assert [m[3] for m in MER] == [5, 10, 17, 28] and sum(m[3] for m in MER) == 60 == CHK.huffman_cost([2, 3, 5, 7, 11])
ROOT = MER[-1][2]
DEP = W.huffman_depths(NODES, ROOT)
assert DEP == {"a": 4, "b": 4, "c": 3, "d": 2, "e": 1}
assert sum(w * DEP[n] for n, w in IT) == 60
# the exchange lemma on a bad tree: the same shape with a (2) and e (11) swapped
BAD = dict(DEP)
BAD["a"], BAD["e"] = DEP["e"], DEP["a"]
cost_bad = sum(w * BAD[n] for n, w in IT)
assert cost_bad == 87 and cost_bad - 60 == (11 - 2) * (4 - 1) == 27

# ---------------------------------------------------------------- exam 26A-A-Q3a
Q = BANK["26A-A-Q3a"]
FX = [("a", 22), ("b", 15), ("c", 3), ("d", 24), ("e", 4), ("f", 10), ("g", 8)]
assert "`a`=22, `b`=15, `c`=3, `d`=24, `e`=4, `f`=10, `g`=8" in Q["question"]
NX, MX = W.huffman_run(FX, prefer=["b"])                 # the tie 15 = 15: b is merged with f
assert W.huffman_is_valid_run(FX, MX)
assert [(m[0], m[1], m[3]) for m in MX] == [("c", "e", 7), ("m1", "g", 15), ("f", "b", 25), ("m2", "a", 37),
                                            ("d", "m3", 49), ("m4", "m5", 86)]
assert sum(m[3] for m in MX) == 219 == CHK.huffman_cost([w for _, w in FX])
CODES = W.huffman_codes(NX, MX[-1][2])
assert CODES == {"a": "01", "b": "111", "c": "0000", "d": "10", "e": "0001", "f": "110", "g": "001"}   # = the solution
DX = W.huffman_depths(NX, MX[-1][2])
assert sum(w * DX[n] for n, w in FX) == 219
NY, MY = W.huffman_run(FX, prefer=["m2"])                              # the other tie-break: f with the inner node 15
assert W.huffman_is_valid_run(FX, MY) and MY[2][:2] == ("f", "m2")
DY = W.huffman_depths(NY, MY[-1][2])
assert sum(m[3] for m in MY) == 219 and DY["b"] == 2 and DX["b"] == 3 and DY["g"] == 4 and DX["g"] == 3

TW = W.tree_svg("tw", NODES, MER, w=760, h=470)
TX = W.tree_svg("tx", NX, MX, w=980, h=520, r=32)
FCH = W.chips("fx", [f"{n}: {w}" for n, w in FX], hidden=False, cls="small")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את קוד הופמן כאלגוריתם חמדני."),
    P("נבנה עץ ונחשב את העלות שלו, נראה למה הבחירה של שני הקלים בטוחה, ונטפל בשוויונות."),
    P("ובסוף נבנה קוד הופמן לשאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">G07 · אלגוריתם חמדן והוכחת נכונות</div><h1>הופמן כאלגוריתם חמדני</h1>'
         '<p>לבנות עץ הופמן ולחשב את עלותו, להוכיח את הלמה של ההחלפה, ולהתמודד עם שוויונות.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("נתונות אותיות עם שכיחויות. בונים עץ בינארי, והאותיות הן העלים. הקוד של אות הוא המסלול אליה."),
    P("העלות: לכל אות, השכיחות כפול העומק שלה, ומסכמים. רוצים עלות מינימלית.", do=show("i-b")),
    P("האלגוריתם החמדן: מוציאים את שני הצמתים הקלים ביותר, מחברים אותם לצומת שמשקלו הסכום, ומחזירים אותו.",
      do=show("i-r")),
    P("חוזרים על זה עד שנשאר צומת אחד. עם ערימה, זה $O(n\\,\\log\\,n)$.",
      say="חוזרים על זה עד שנשאר צומת אחד. עם ערימה, זה או של אֶן לוֹג אֶן."),
    P("ועובדה שימושית: העלות שווה לסכום המשקלים של כל הצמתים הפנימיים. כל חיבור משלם את משקל הצומת החדש.",
      do=show("i-e"), hold=0.4),
], stage='<div class="gp-stack"><div id="i-b" class="gp-big h">$B(T) = \\sum_c f(c) \\cdot d_T(c)$</div></div>',
   panel=st.card("i-r", "rule", "🔑 בכל צעד: שני הקלים ביותר מתחברים")
         + st.card("i-e", "ex", "עלות = סכום משקלי הצמתים הפנימיים"))

ex = Scene("ex", "בונים עץ", [
    P("חמש אותיות, בשכיחויות 2, 3, 5, 7 ו-11.", do=show("tw")),
    P("שני הקלים הם 2 ו-3. מחברים לצומת 5.", do=show("tw-m0")),
    P("עכשיו יש שני צמתים במשקל 5: העלה, והצומת החדש. הם שני הקלים, ומתחברים ל-10.", do=show("tw-m1")),
    P("הקלים הבאים: 7 ו-10. מתחברים ל-17.", do=show("tw-m2")),
    P("ונשארו 11 ו-17, שמתחברים לשורש 28.", do=show("tw-m3")),
    P("העלות: סכום הצמתים הפנימיים, 5 ועוד 10 ועוד 17 ועוד 28. כלומר 60.", do=show("w-1")),
    P("ובדיקה בדרך השנייה: שכיחות כפול עומק. 2 ו-3 בעומק 4, 5 בעומק 3, 7 בעומק 2, ו-11 בעומק 1. שוב 60.",
      do=show("w-2", "tw-bits"), hold=0.4),
], stage=f'<div class="gp-stack"><div id="tw" class="h">{TW}</div></div>',
   panel=st.card("w-1", "ex", "$5 + 10 + 17 + 28 = 60$")
         + st.card("w-2", "ex", "$2 \\cdot 4 + 3 \\cdot 4 + 5 \\cdot 3 + 7 \\cdot 2 + 11 \\cdot 1 = 60$"))

lemma = Scene("lemma", "למה זה נכון", [
    P("למה מותר לחבר דווקא את שני הקלים? זו תכונת הבחירה החמדנית, ומוכיחים אותה בהחלפה."),
    P("יהיו $x, y$ שתי האותיות הקלות, ו-$b, c$ שני עלים אחים בעומק המקסימלי של עץ אופטימלי.", do=show("l-1"),
      say="יהיו אִקְס ווַואי שתי האותיות הקלות, ובִּי וסִי שני עלים אחים בעומק המקסימלי של עץ אופטימלי."),
    P("מחליפים בין $x$ ל-$b$. העלות יורדת בדיוק בהפרש השכיחויות, כפול הפרש העומקים.", do=show("l-f"),
      say="מחליפים בין אִקְס לבִּי. העלות יורדת בדיוק בהפרש השכיחויות, כפול הפרש העומקים."),
    P("שני הגורמים אי-שליליים: $b$ לא קל מ-$x$, ו-$b$ עמוק לפחות כמוהו. אז ההחלפה לא מייקרת.", do=show("l-2"),
      say="שני הגורמים אי שליליים: בִּי לא קל מאִקְס, ובִּי עמוק לפחות כמוהו. אז ההחלפה לא מייקרת."),
    P("למשל בעץ שלנו, אילו 2 היה בעומק 1 ו-11 בעומק 4, העלות הייתה 87.", do=show("l-3")),
    P("החלפה ביניהם חוסכת 11 פחות 2, כפול 4 פחות 1: עשרים ושבע. ומגיעים ל-60.",
      say="החלפה ביניהם חוסכת את ההפרש בין אחת עשרה לשתיים, כפול ההפרש בין ארבע לאחת: עשרים ושבע. ומגיעים לשישים."),
    P("אותו דבר ל-$y$ ו-$c$. אז יש עץ אופטימלי שבו שתי הקלות הן אחיות עמוקות, וזה בדיוק החיבור הראשון.",
      say="אותו דבר לוַואי ולסִי. אז יש עץ אופטימלי שבו שתי הקלות הן אחיות עמוקות, וזה בדיוק החיבור הראשון."),
    P("ותת-המבנה: מחליפים את שתיהן באות אחת, ששכיחותה הסכום, ופותרים את הבעיה הקטנה.", do=show("l-r"), hold=0.4),
], stage='<div class="gp-stack">'
         '<div id="l-f" class="gp-big h">$B(T) - B(T\') = (f[b] - f[x]) \\cdot (d(b) - d(x)) \\ge 0$</div>'
         '<div id="l-3" class="gp-mid h">$87 - 60 = (11 - 2) \\cdot (4 - 1) = 27$</div></div>',
   panel=st.card("l-1", "plain", "$x, y$ הקלות; $b, c$ אחים בעומק מקסימלי")
         + st.card("l-2", "rule", "🔑 $f[b] \\ge f[x]$ וגם $d(b) \\ge d(x)$")
         + st.card("l-r", "rule", "🔑 תת-מבנה: $x, y \\to$ אות אחת בשכיחות $f[x] + f[y]$"))

SAYL = {"a": "אֵיי", "b": "בִּי", "c": "סִי", "d": "דִּי", "e": "אִי", "f": "אֶף", "g": "גִ'י"}
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מהו קוד הופמן לשבע האותיות האלה? פרטו את דרך החישוב.", do=show("fx")),
    P("שני הקלים: 3 ו-4. מתחברים ל-7.", do=show("tx")),
    P("הקלים הבאים: הצומת 7, ו-8. מתחברים ל-15.", do=show("tx-m0", "tx-m1")),
    P("עכשיו יש שוויון: האות שבשכיחות 15, והצומת החדש, שגם הוא 15. ו-10 הוא הקל ביותר.", do=show("x-t")),
    P("בשוויון מותר לבחור כל אחד מהם. כאן מחברים את 10 עם האות 15, ומקבלים 25.", do=show("tx-m2")),
    P("נשארו 15, 22, 24 ו-25. הצומת 15 מתחבר עם 22, ל-37.", do=show("tx-m3")),
    P("24 מתחבר עם 25, ל-49. ולבסוף 37 עם 49 נותנים את השורש, 86.", do=show("tx-m4", "tx-m5")),
    P("שמאלה אפס, ימינה אחת. האותיות השכיחות קיבלו קודים קצרים: שתי סיביות לשתי השכיחות ביותר.",
      do=show("tx-bits", "x-c")),
    P("העלות: 7, 15, 25, 37, 49 ו-86. ביחד 219.", do=show("x-k")),
    P("ובשבירת השוויון השנייה? מתקבל עץ אחר, עם אורכי קוד אחרים. אבל העלות שלו בדיוק אותו 219.", do=show("x-o")),
    P("זו המלכודת: אין קוד הופמן אחד נכון. כל שבירת שוויון חוקית נותנת קוד אופטימלי, באותה עלות.", hold=0.5),
], stage=f'<div class="gp-stack"><div id="fx" class="h">{FCH}</div><div id="tx" class="h">{TX}</div></div>',
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>מהו קוד הופמן לטבלת השכיחויות? פרטו את דרך החישוב.</div>'
         + st.card("x-t", "trap", "⚠️ שוויון $15 = 15$: מותר לבחור כל אחד")
         + st.card("x-c", "ex", r"$a{=}01,\ d{=}10,\ g{=}001,\ f{=}110$<br>$b{=}111,\ c{=}0000,\ e{=}0001$")
         + st.card("x-k", "rule", "🔑 $7 + 15 + 25 + 37 + 49 + 86 = 219$")
         + st.card("x-o", "plain", "בחירה אחרת בשוויון: עץ אחר, אותה עלות 219"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: הופמן מחבר כל פעם את שני הקלים, והעלות היא סכום הצמתים הפנימיים.", do=show("r-1")),
    P("הוא נכון בגלל החלפה: להעביר אות קלה לעומק לא מייקר, כי השינוי הוא מכפלה של שני הפרשים אי-שליליים.",
      do=show("r-2")),
    P("ובשוויון בוחרים כרצונכם: העץ יכול להשתנות, העלות לא. נתראה במבחן המסכם.", do=show("r-3"), hold=0.6),
], stage='<div class="gp-stack"><div class="gp-big">$B(T) = \\sum_c f(c) \\cdot d_T(c)$</div></div>',
   panel=st.card("r-1", "rule", "🔑 שני הקלים; עלות = סכום הפנימיים")
         + st.card("r-2", "rule", "🔑 $(f[b]-f[x])(d(b)-d(x)) \\ge 0$")
         + st.card("r-3", "trap", "⚠️ שוויון: עצים שונים, אותה עלות"))

VIDEO = Video("G07", "greedy_proofs", "הופמן כאלגוריתם חמדני", [title, idea, ex, lemma, exam, recap],
              bank={"26A-A-Q3a": None})
