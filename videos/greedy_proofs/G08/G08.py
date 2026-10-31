# -*- coding: utf-8 -*-
"""G08 · מבחן מסכם: חמדנים והוכחות (boss walkthrough) — video script (build: tools/video/vid.py G08).

Source: courses/greedy_proofs/C08.js (boss: real exam questions, greedy algorithm, correctness proof, Huffman).
Exam anchors (none is a quiz/boss item, none is a content twin of one):
  25A-B-Q2a + 25A-B-Q2b  (reduce the value of a string by deleting k letters: a heap greedy, and its proof)
  24B-B-Q2a              (Huffman code given: all possible frequencies of c and d)
Avoided on purpose: the six C08 boss items (25B-A-Q2a, 24A-A-Q2b, 24A-C-Q2a, 24B-A-Q2c, 22A-B-Q4a/b) and their
sittings' sibling parts, and every level's quiz data.
25A-B is checked by brute force over every way to delete k letters (the example and random strings); 24B-B-Q2a by
enumerating every Huffman run (every tie-break) and every left/right orientation allowed by "left <= right".
"""
import itertools
import random
from collections import Counter
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_greedy_proofs as W


# ---------------------------------------------------------------- 25A-B-Q2: the value of a string
def value(s):
    return sum(v * v for v in Counter(s).values())


def greedy_reduce(s, k):
    """k times: delete one occurrence of a letter whose current count is maximal. Returns (counts after, steps)"""
    cnt = Counter(s)
    steps = []
    for _ in range(k):
        c = max(cnt, key=lambda ch: (cnt[ch], -ord(ch)))
        steps.append((c, cnt[c], 2 * cnt[c] - 1))
        cnt[c] -= 1
        if cnt[c] == 0:
            del cnt[c]
    return cnt, steps


def best_reduce(s, k):
    return min(value("".join(ch for i, ch in enumerate(s) if i not in drop))
               for drop in itertools.combinations(range(len(s)), k))


QA, QB = BANK["25A-B-Q2a"], BANK["25A-B-Q2b"]
assert QA["contextId"] == QB["contextId"] == "25A-B-c2"
S, K = "character", 2
assert Counter(S) == Counter({"c": 2, "a": 2, "r": 2, "h": 1, "t": 1, "e": 1}) and value(S) == 15
CNT, STEPS = greedy_reduce(S, K)
assert [d for _, _, d in STEPS] == [3, 3] and sum(CNT[c] ** 2 for c in CNT) == 9 == best_reduce(S, K)
ODD = sorted([2 * j - 1 for v in Counter(S).values() for j in range(1, v + 1)], reverse=True)
assert ODD == [3, 3, 3, 1, 1, 1, 1, 1, 1] and sum(ODD) == 15 and 15 - sum(ODD[:K]) == 9
rng = random.Random(7)
for _ in range(300):
    s = "".join(rng.choice("abcd") for _ in range(rng.randint(2, 9)))
    k = rng.randint(1, len(s) - 1)
    c2, _ = greedy_reduce(s, k)
    assert sum(v * v for v in c2.values()) == best_reduce(s, k)
    odd = sorted([2 * j - 1 for v in Counter(s).values() for j in range(1, v + 1)], reverse=True)
    assert sum(v * v for v in c2.values()) == value(s) - sum(odd[:k])      # the lower bound is reached

# ---------------------------------------------------------------- 24B-B-Q2a: Huffman code -> possible (c, d)
QH = BANK["24B-B-Q2a"]
assert "$a$ - `10`, $b$ - `00`, $c$ - `010`, $d$ - `011`, $e$ - `11`" in QH["question"]
TARGET = (("b", ("c", "d")), ("a", "e"))       # 0 = left, 1 = right


def runs(pool):
    """every tree a Huffman run can build (any choice among equal minimum weights). pool: [(w, tree)]"""
    if len(pool) == 1:
        yield pool[0]
        return
    ws = sorted(w for w, _ in pool)
    for i, j in itertools.combinations(range(len(pool)), 2):
        if sorted([pool[i][0], pool[j][0]]) == ws[:2]:
            rest = [pool[t] for t in range(len(pool)) if t not in (i, j)]
            yield from runs(rest + [(pool[i][0] + pool[j][0], (pool[i], pool[j]))])


def match(node, tgt):
    """node = (w, leaf name | (child, child)); left/right free but the left child may not be heavier"""
    w, t = node
    if isinstance(tgt, str):
        return t == tgt
    if isinstance(t, str):
        return False
    for l, r in ((t[0], t[1]), (t[1], t[0])):
        if l[0] <= r[0] and match(l, tgt[0]) and match(r, tgt[1]):
            return True
    return False


def possible(c, d):
    pool = [(7, "a"), (4, "b"), (c, "c"), (d, "d"), (7, "e")]
    return any(match(t, TARGET) for t in runs(pool))


ANS = [(c, d) for c in range(1, 16) for d in range(1, 16) if possible(c, d)]
assert ANS == [(1, 3), (1, 4), (2, 2), (2, 3), (2, 4), (3, 3), (3, 4)]
assert ANS == [(c, d) for c in range(1, 16) for d in range(1, 16) if c <= d <= 4 and 4 <= c + d <= 7]

# ---------------------------------------------------------------- widgets
CH = W.table("ch", ["אות", "c", "h", "a", "r", "t", "e"],
             [["מופעים", "2", "1", "2", "2", "1", "1"], ["תרומה לערך", "4", "1", "4", "4", "1", "1"]],
             hidden_rows=False)
ODDS = W.chips("od", ["1", "3", "1", "3", "1", "3", "1", "1", "1"], hidden=False, cls="small", label="")
HN = {"a": (7, None, None), "b": (4, None, None), "c": ("c", None, None), "d": ("d", None, None),
      "e": (7, None, None), "Y": ("c+d", "c", "d"), "X": ("4+c+d", "b", "Y"), "Z": (14, "a", "e"),
      "R": ("", "X", "Z")}
HM = [("c", "d", "Y", "c+d"), ("b", "Y", "X", "4+c+d"), ("a", "e", "Z", 14), ("X", "Z", "R", "")]
HT = W.tree_svg("ht", HN, HM, w=760, h=420, r=40)
PAIRS = W.chips("pp", [f"({c},{d})" for c, d in ANS], hidden=False, cls="small")

LETTER = {"c": "סִי", "h": "אֵייץ'", "a": "אֵיי", "r": "אָר", "t": "טִי", "e": "אִי", "d": "דִּי", "b": "בִּי"}

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה המבחן המסכם של המסלול: שתי שאלות אמיתיות, מתחילתן ועד סופן."),
    P("שאלת חמדן עם אלגוריתם והוכחה, ושאלת הופמן הפוכה: מהקוד אל השכיחויות.", hold=0.4),
], stage='<div class="kicker">G08 · אלגוריתם חמדן והוכחת נכונות</div><h1>מבחן מסכם: חמדנים והוכחות</h1>'
         '<p>לפתור שאלות חמדן אמיתיות מהמבחנים: אלגוריתם, הוכחת נכונות והופמן.</p>', layout="title")

plan = Scene("plan", "הרשימה", [
    P("לפני שמתחילים, הרשימה שחוזרת בכל שאלה חמדנית.", do=show("c1")),
    P("כלל: מה בוחרים, ובודקים אותו מול דוגמה קטנה. הוכחה: החלפה, או החמדן מקדים, ותמיד חוקיות וערך.",
      do=show("c2", "c3")),
    P("ובהופמן: שני הקלים מתחברים, ובשוויון מותר לבחור כל אחד.", do=show("c4"), hold=0.4),
], stage='<div class="gp-stack"><div class="gp-steps">'
         '<div id="c1" class="h"><span class="n">1</span>כלל: מה בוחרים בכל צעד. בודקים מול דוגמה קטנה</div>'
         '<div id="c2" class="h"><span class="n">2</span>הוכחה: החלפה, או "החמדן מקדים"</div>'
         '<div id="c3" class="h"><span class="n">3</span>בכל החלפה: <b>חוקי</b> וגם <b>לא גרוע</b></div>'
         '<div id="c4" class="h"><span class="n">4</span>הופמן: שני הקלים; שוויון = בחירה חופשית</div>'
         '</div></div>')

say_l = lambda c: LETTER[c]
q1 = Scene("q1", "שאלה 1: אלגוריתם", [
    P("שאלה ראשונה. הערך של מחרוזת הוא סכום הריבועים של מספרי המופעים של כל אות."),
    P("למשל ב-character: שלוש אותיות מופיעות פעמיים, ושלוש פעם אחת. הערך 4 ועוד 4 ועוד 4, ועוד 1, 1, 1: כלומר 15.",
      do=show("ch"), say="למשל במילה קָרַקְטֶר: שלוש אותיות מופיעות פעמיים, ושלוש פעם אחת. הערך ארבע ועוד ארבע ועוד ארבע, ועוד אחת, אחת, אחת: כלומר חמש עשרה."),
    P("צריך למחוק $k$ אותיות כך שהערך יהיה מינימלי, בזמן $O(n + k\\,\\log\\,k)$.",
      say="צריך למחוק קֵיי אותיות כך שהערך יהיה מינימלי, בזמן או של, בסוגריים, אֶן ועוד קֵיי לוֹג קֵיי."),
    P("מה קורה כשמוחקים מופע אחד של אות שמופיעה $x$ פעמים? הערך יורד מ-$x^2$ ל-$(x-1)^2$, כלומר ב-$2x-1$.",
      do=show("a-1"),
      say="מה קורה כשמוחקים מופע אחד של אות שמופיעה אִקְס פעמים? הערך יורד מאִקְס בריבוע, לריבוע של, בסוגריים, אִקְס פחות אחת. כלומר בשתיים אִקְס פחות אחת."),
    P("ככל שהאות שכיחה יותר, המחיקה חוסכת יותר. אז החמדן: כל פעם מוחקים מופע של האות השכיחה ביותר כרגע.",
      do=show("a-r")),
    P("איך עושים את זה מהר? סופרים מופעים במעבר אחד, ובונים ערימת מקסימום לפי מספר המופעים.", do=show("a-2")),
    P("$k$ פעמים: מוציאים את המקסימום, מורידים אחד, ומחזירים לערימה. ובסוף בונים את המחרוזת במעבר נוסף.",
      say="קֵיי פעמים: מוציאים את המקסימום, מורידים אחד, ומחזירים לערימה. ובסוף בונים את המחרוזת במעבר נוסף."),
    P("בערימה יש לכל היותר 26 אותיות, ולכן כל פעולה זולה, והזמן נכנס בחסם הנדרש."),
    P("ב-character עם $k$ שווה 2: מוחקים מופע של אות עם שני מופעים, וחוסכים 3. ושוב, עוד 3. הערך 9.",
      do=show("a-3"), say="בקָרַקְטֶר עם קֵיי שווה שתיים: מוחקים מופע של אות עם שני מופעים, וחוסכים שלוש. ושוב, עוד שלוש. הערך תשע."),
    P("ובדיקה של כל 36 הדרכים למחוק שתי אותיות מאשרת: 9 הוא המינימום.", hold=0.4),
], stage=f'<div class="gp-stack"><div id="ch" class="h">{CH}</div>'
         '<div id="a-1" class="gp-big h">$x^2 - (x-1)^2 = 2x - 1$</div>'
         '<div id="a-3" class="gp-mid h">$15 - 3 - 3 = 9$</div></div>',
   panel='<div class="qstem"><span class="qid">25A-B-Q2a</span>ערך מחרוזת = סכום ריבועי השכיחויות. מוחקים $k$ אותיות '
         'כך שהערך מינימלי. אלגוריתם חמדני בזמן $O(n + k\\,\\log\\,k)$.</div>'
         + st.card("a-r", "rule", "🔑 בכל צעד: מופע של האות השכיחה ביותר")
         + st.card("a-2", "ex", "ספירה $O(n)$, ערימת מקסימום, $k$ פעמים מוציאים ומחזירים"))
assert len(list(itertools.combinations(range(len(S)), 2))) == 36

q1b = Scene("q1b", "שאלה 1: הוכחה", [
    P("עכשיו ההוכחה. הטריק: ריבוע הוא סכום של מספרים אי-זוגיים. 4 הוא 1 ועוד 3, 9 הוא 1 ועוד 3 ועוד 5.",
      do=show("b-1")),
    P("אז הערך של המחרוזת הוא סכום של אוסף מספרים: לכל אות, 1, 3, 5, וכן הלאה, עד פעמיים מספר המופעים פחות אחת.",
      do=show("od")),
    P("ומחיקה של מופע אחד מוציאה מהאוסף בדיוק מספר אחד: את הגדול ביותר שנשאר לאותה אות."),
    P("חסם תחתון: כל דרך למחוק $k$ אותיות מוציאה $k$ מספרים מהאוסף. והסכום שלהם לכל היותר סכום $k$ הגדולים.",
      do=show("b-2"), say="חסם תחתון: כל דרך למחוק קֵיי אותיות מוציאה קֵיי מספרים מהאוסף. והסכום שלהם לכל היותר סכום קֵיי הגדולים."),
    P("לכן הערך שנשאר הוא לפחות הערך המקורי, פחות סכום $k$ המספרים הגדולים באוסף.",
      say="לכן הערך שנשאר הוא לפחות הערך המקורי, פחות סכום קֵיי המספרים הגדולים באוסף."),
    P("והחמדן משיג בדיוק את החסם: המספר הגדול ביותר שנשאר באוסף שייך לאות השכיחה ביותר, וזה מה שהוא מוחק.",
      do=show("b-3")),
    P("באינדוקציה על הצעדים, אחרי $k$ צעדים הוא הוציא את $k$ הגדולים. בדוגמה: 3 ו-3, ו-15 פחות 6 זה 9.",
      say="באינדוקציה על הצעדים, אחרי קֵיי צעדים הוא הוציא את קֵיי הגדולים. בדוגמה: שלוש ושלוש, וחמש עשרה פחות שש זה תשע."),
    P("זו הוכחה בלי החלפה: חסם תחתון לכל פתרון, ואלגוריתם שמגיע אליו.", do=show("b-t"), hold=0.4),
], stage=f'<div class="gp-stack"><div id="b-1" class="gp-big h">$x^2 = 1 + 3 + \\dots + (2x - 1)$</div>'
         f'<div id="od" class="h">{ODDS}</div>'
         '<div id="b-2" class="gp-mid h">$v(S\') \\ \\ge\\ v(S) - D_k$</div>'
         '<div class="gp-note">$D_k$ = סכום $k$ המספרים הגדולים באוסף</div></div>',
   panel='<div class="qstem"><span class="qid">25A-B-Q2b</span>הוכיחו את נכונות האלגוריתם.</div>'
         + st.card("b-3", "rule", "🔑 החמדן מוציא בכל צעד את המספר הגדול ביותר שנשאר")
         + st.card("b-t", "ex", "חסם תחתון + אלגוריתם שמשיג אותו = אופטימליות"))

q2 = Scene("q2", "שאלה 2: הופמן", [
    P("שאלה שנייה, הופמן הפוך. $a$ ו-$e$ מופיעות 7 פעמים, $b$ ארבע פעמים, וידועים הקודים של כל האותיות.",
      say="שאלה שנייה, הופמן הפוך. אֵיי ואִי מופיעות שבע פעמים, בִּי ארבע פעמים, וידועים הקודים של כל האותיות."),
    P("בכל צומת, האח השמאלי לא כבד מהימני. מחפשים את כל האפשרויות לשכיחויות של $c$ ו-$d$.",
      say="בכל צומת, האח השמאלי לא כבד מהימני. מחפשים את כל האפשרויות לשכיחויות של סִי ודִּי."),
    P("קודם משרטטים את העץ מהקודים. אפס שמאלה ואחת ימינה.", do=show("ht", "ht-m0", "ht-m1", "ht-m2", "ht-m3")),
    P("החיבור הראשון של הופמן יוצר צומת ששני ילדיו עלים. כאן זה $c$ עם $d$, או $a$ עם $e$.",
      say="החיבור הראשון של הופמן יוצר צומת ששני ילדיו עלים. כאן זה סִי עם דִּי, או אֵיי עם אִי."),
    P("$a$ עם $e$ לא יכול להיות ראשון: 4 קטן מ-7. אז $c$ ו-$d$ הם שני הקלים, ולכן שניהם לכל היותר 4.",
      do=show("h-1"), say="אֵיי עם אִי לא יכול להיות ראשון, כי ארבע קטן משבע. אז סִי ודִּי הם שני הקלים, ולכן שניהם לכל היותר ארבע."),
    P("החיבור השני: $b$ עם הצומת של $c$ ו-$d$. שוב $a$ עם $e$ לא קודם, ולכן $c+d$ לכל היותר 7.",
      do=show("h-2"), say="החיבור השני: בִּי עם הצומת של סִי ודִּי. שוב, אֵיי ואִי לא חוברו לפניו, ולכן סִי ועוד דִּי לכל היותר שבע."),
    P("החיבור השלישי הוא $a$ עם $e$, ולכן 7 ו-7 הם הקלים: $4 + c + d$ לפחות 7.", do=show("h-3"),
      say="החיבור השלישי הוא אֵיי עם אִי, ולכן שבע ושבע הם הקלים: ארבע ועוד סִי ועוד דִּי, לפחות שבע."),
    P("ועכשיו תנאי האחים: $c$ לא כבד מ-$d$, ו-$b$, שהוא 4, לא כבד מהצומת $c+d$.", do=show("h-4"),
      say="ועכשיו תנאי האחים: סִי לא כבד מדִּי, ובִּי, שהוא ארבע, לא כבד מהצומת של סִי ועוד דִּי."),
    P("יחד: $c \\le d \\le 4$, וגם $c+d$ בין 4 ל-7. ומקבלים שבעה זוגות.", do=show("pp"),
      say="יחד: סִי קטן או שווה לדִּי, שקטן או שווה לארבע. וסִי ועוד דִּי בין ארבע לשבע. ומקבלים שבעה זוגות."),
    P("ובדיקה מלאה, על כל ריצות הופמן וכל שבירות השוויון, מוצאת בדיוק את שבעת הזוגות האלה.", do=show("h-ok")),
    P("המלכודת: לשכוח שוויונות. למשל בזוג 3 ו-4, הצומת 7 שווה ל-$a$ ול-$e$, והשוויון נשבר לטובת העץ הנתון.",
      do=show("h-t"), say="המלכודת: לשכוח שוויונות. למשל בזוג שלוש וארבע, הצומת שבע שווה לאֵיי ולאִי, והשוויון נשבר לטובת העץ הנתון.",
      hold=0.5),
], stage=f'<div class="gp-stack"><div id="ht" class="h">{HT}</div><div id="pp" class="h">{PAIRS}</div>'
         + st.card("h-ok", "ex", "✓ נבדק על כל ריצות הופמן האפשריות") + "</div>",
   panel='<div class="qstem"><span class="qid">24B-B-Q2a</span>$a{=}7,\\ b{=}4,\\ e{=}7$; הקודים: '
         '$a{=}10,\\ b{=}00,\\ c{=}010,\\ d{=}011,\\ e{=}11$. כל האפשרויות ל-$c, d$.</div>'
         + st.card("h-1", "plain", "חיבור 1 = $\\{c, d\\}$: $c, d \\le 4$")
         + st.card("h-2", "plain", "חיבור 2 = $\\{b, cd\\}$: $c + d \\le 7$")
         + st.card("h-3", "plain", "חיבור 3 = $\\{a, e\\}$: $4 + c + d \\ge 7$")
         + st.card("h-4", "rule", "🔑 אחים: $c \\le d$ וגם $4 \\le c + d$")
         + st.card("h-t", "trap", "⚠️ שוויון נשבר לטובת העץ הנתון"))

recap = Scene("recap", "סיכום", [
    P("לסיכום המסלול: חמדן הוא כלל ומעבר, ודוגמה נגדית אחת מספיקה כדי להפיל כלל.", do=show("r-1")),
    P("הוכחה היא החלפה עם חוקיות וערך, ותת-מבנה. או החמדן מקדים. או חסם תחתון שהחמדן משיג.", do=show("r-2")),
    P("ובהופמן: שני הקלים, עלות כסכום הפנימיים, ושוויונות לטובתכם. בהצלחה במבחן!", do=show("r-3"), hold=0.6),
], stage='<div class="gp-stack"><div class="gp-big">$\\text{greedy} = \\text{rule} + \\text{proof}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 כלל + דוגמה נגדית")
         + st.card("r-2", "rule", "🔑 החלפה · החמדן מקדים · חסם תחתון")
         + st.card("r-3", "trap", "⚠️ הופמן: שוויון נשבר לטובת העץ"))

VIDEO = Video("G08", "greedy_proofs", "מבחן מסכם: חמדנים והוכחות", [title, plan, q1, q1b, q2, recap],
              bank={"25A-B-Q2a": None, "25A-B-Q2b": None, "24B-B-Q2a": None})
