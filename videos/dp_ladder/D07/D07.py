# -*- coding: utf-8 -*-
"""D07 · חיתוך ופיצול, וספירה — video script (build: tools/video/vid.py D07).

Source: courses/dp_ladder/C07.js (lesson + goal). Exam anchor: 24A-B-Q4a (number of outcomes of i dice of different
colours whose sum is j, open question): the last part is the last die, the cases are disjoint so they are summed,
and the base T(0,0)=1. No guided quiz uses it.
Not used on purpose: the C07 quiz (catsanddog with its dictionary: minimum 2 and 3 cuts, the N(i) formula, abacdc
into palindromes, the ∞ question, rabbit in rabbbit) and the boss 22A-B-Q1 (minimum cut into Hebrew words).
The worked example (abaab cut into palindromes: minimum parts and number of cuts) is original. Every value is computed
by w_dp_ladder and compared with a brute force (all cuts / all dice outcomes) below.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_dp_ladder as w

# ---------------------------------------------------------------- data (verified)
S = "abaab"
ok = lambda a, b: S[a - 1:b] == S[a - 1:b][::-1]
C, N = w.cut_min_count(S, ok)
allc = w.cuts_bf(S, ok)
assert C == [0, 1, 2, 1, 2, 2] and N == [1, 1, 1, 2, 3, 4]
assert N[5] == len(allc) == 4 and C[5] == min(len(c) for c in allc) == 2
assert sorted("|".join(c) for c in allc) == sorted(["a|b|a|a|b", "a|b|aa|b", "aba|a|b", "a|baab"])
assert [j for j in range(5) if ok(j + 1, 5)] == [1, 4]                       # pieces ending at 5: baab, b
assert C[5] == min(C[1], C[4]) + 1 and N[5] == N[1] + N[4] == 1 + 3
assert [j for j in range(4) if ok(j + 1, 4)] == [2, 3] and N[4] == N[2] + N[3] == 3   # pieces ending at 4: aa, a
assert C[3] == 1 and ok(1, 3)                                                # aba is one piece

# exam 24A-B-Q4a
Q = BANK["24A-B-Q4a"]
assert "קוביות" in Q["question"] and Q.get("correctId") is None
NI, MJ = 3, 8
T = w.dice(NI, MJ)
assert all(T[i][j] == w.dice_bf(i, j) for i in range(NI + 1) for j in range(MJ + 1))
assert T[2][3] == 2 == T[1][2] + T[1][1]                                     # the example of the question
assert T[3][8] == sum(T[2][8 - k] for k in range(1, 7)) == 1 + 2 + 3 + 4 + 5 + 6 == 21
assert T[2][7] == 6 and T[1][7] == 0 and T[1][0] == 0
bad = [[0] * (MJ + 1) for _ in range(NI + 1)]                                # the same recurrence with T(0,0) = 0
for i in range(1, NI + 1):
    for j in range(MJ + 1):
        bad[i][j] = sum(bad[i - 1][j - k] for k in range(1, 7) if j - k >= 0)
assert all(v == 0 for r in bad for v in r)

# ---------------------------------------------------------------- widgets
GC = w.Grid("gc", ["S", "C", "N"], [str(i) for i in range(6)],
            {**{(0, i): S[i - 1] for i in range(1, 6)}, **{(1, i): str(C[i]) for i in range(6)},
             **{(2, i): str(N[i]) for i in range(6)}},
            given={(0, i) for i in range(1, 6)}, void={(0, 0)}, cw=96, ch=70, fs=36)
GT = w.Grid("gt", [str(i) for i in range(NI + 1)], [str(j) for j in range(MJ + 1)],
            {(i, j): str(T[i][j]) for i in range(NI + 1) for j in range(MJ + 1)}, cw=82, ch=66, fs=32, corner="i\\j")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר שתי צורות שחוזרות במבחנים: חיתוך של מחרוזת לחלקים, וספירה."),
    P("בשתיהן הצעד האחרון הוא **החלק האחרון**. ובסוף נפתור שאלת ספירה ממבחן.", hold=0.4),
], stage='<div class="kicker">D07 · תכנות דינמי</div><h1>חיתוך ופיצול, וספירה</h1>'
         '<p>נוסחה שבה הצעד האחרון הוא החלק האחרון: מינימום חלקים, או מספר הדרכים.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("חותכים מחרוזת לחלקים רצופים, וכל חלק צריך להיות חוקי. למשל פולינדרום.", do=show("i-1")),
    P("ההחלטה האחרונה היא החלק האחרון. אם הוא מתחיל אחרי המקום $j$, נשארת הרישא עד $j$.", do=show("i-2"),
      say="ההחלטה האחרונה היא החלק האחרון. אם הוא מתחיל אחרי המקום גֵ'יי, נשארת הרישא עד גֵ'יי."),
    P("כשמחפשים מינימום חלקים, לוקחים מינימום על $j$, ומוסיפים אחד בשביל החלק האחרון.", do=show("i-m"),
      say="כשמחפשים מינימום חלקים, לוקחים מינימום על גֵ'יי, ומוסיפים אחד בשביל החלק האחרון."),
    P("וכשסופרים חיתוכים, שני חיתוכים עם חלק אחרון שונה הם שונים. לכן מחברים, ובלי להוסיף אחד.", do=show("i-s")),
    P("ובבסיס: למחרוזת הריקה אפס חלקים, ויש לה חיתוך **אחד**: לא חותכים כלום.", do=show("i-b"), hold=0.3),
], stage='<div class="dl-stack">'
         + st.card("i-1", "ex", "חיתוך לחלקים רצופים, כל חלק חוקי")
         + st.card("i-2", "rule", "🔑 הצעד האחרון: החלק האחרון $S[j+1..i]$")
         + "</div>",
   panel=st.card("i-m", "plain", "מינימום: $C(i)=1+\\min_j C(j)$")
         + st.card("i-s", "plain", "ספירה: $N(i)=\\sum_j N(j)$")
         + st.card("i-b", "rule", "🔑 $C(0)=0$, $N(0)=1$"))

cut_ph = [
    P("נחתוך את $abaab$ לפולינדרומים. $C(i)$ הוא מינימום החלקים של הרישא עד $i$, ו-$N(i)$ מספר החיתוכים שלה.",
      do=show("c-g") + GC.vals_do([(1, 0), (2, 0)]),
      say="נחתוך את אֵיי בִּי אֵיי אֵיי בִּי לפולינדרומים. סִי שֶל אַיי הוא מינימום החלקים של הרישא עד אַיי, ואֶן שֶל אַיי מספר החיתוכים שלה."),
    P("רישא באורך 1 או 2: כל אות היא חלק, כי $ab$ אינו פולינדרום.", do=GC.vals_do([(1, 1), (2, 1), (1, 2), (2, 2)]),
      say="רישא באורך אחת או שתיים: כל אות היא חלק, כי אֵיי בִּי אינו פולינדרום."),
    P("באורך 3, $aba$ כולה פולינדרום, ולכן מספיק חלק אחד. ויש שני חיתוכים: היא עצמה, או שלוש אותיות.",
      do=GC.step((1, 3), [(1, 0)]) + GC.vals_do([(2, 3)]),
      say="באורך שלוש, אֵיי בִּי אֵיי כולה פולינדרום, ולכן מספיק חלק אחד. ויש שני חיתוכים: היא עצמה, או שלוש אותיות."),
    P("באורך 4, החלק האחרון הוא $a$ או $aa$. מחברים את מספרי החיתוכים שלפניהם: 2 ועוד 1, כלומר 3.",
      do=GC.vals_do([(1, 4)]) + GC.step((2, 4), [(2, 3), (2, 2)]),
      say="באורך ארבע, החלק האחרון הוא אֵיי, או אֵיי אֵיי. מחברים את מספרי החיתוכים שלפניהם: שתיים ועוד אחת, כלומר שלוש."),
    P("ובאורך 5 החלק האחרון הוא $b$, או $baab$ כולו.", do=show("c-p") + GC.step((1, 5), [(1, 4), (1, 1)], value=False),
      say="ובאורך חמש החלק האחרון הוא בִּי, או בִּי אֵיי אֵיי בִּי כולו."),
    P("מינימום: אחת ועוד המינימום של 2 ו-1, כלומר 2. החיתוך $a$, $baab$.", do=show(GC.v((1, 5))) + show("c-1"),
      say="מינימום: אחת ועוד המינימום של שתיים ואחת, כלומר שתיים. החיתוך אֵיי, ואחריו בִּי אֵיי אֵיי בִּי."),
    P("ספירה: 3 ועוד 1, כלומר 4 חיתוכים. אם נספור את כל האפשרויות, נמצא בדיוק ארבעה.", do=GC.step((2, 5), [(2, 4), (2, 1)]) + show("c-2")),
    P("המלכודת: לבלבל בין השניים. במינימום יש אחת ועוד, ובספירה לא.", do=GC.off() + show("c-t"), hold=0.3),
]
cut = Scene("cut", "חיתוך לפולינדרומים", cut_ph,
            stage=f'<div class="dl-stack"><div id="c-g" class="h">{GC.html()}</div>'
                  + st.card("c-p", "plain", "החלק האחרון של $abaab$: $b$ או $baab$")
                  + "</div>",
            panel=st.card("c-1", "rule", "🔑 $C(5)=1+\\min\\bigl(C(4),C(1)\\bigr)=2$")
                  + st.card("c-2", "rule", "🔑 $N(5)=N(4)+N(1)=4$")
                  + st.card("c-t", "trap", "⚠️ מינימום: $1+\\min$ · ספירה: $\\sum$ בלי $+1$"))

ex_ph = [
    P("שאלה ממבחן. מטילים $n$ קוביות בצבעים שונים. בכמה תוצאות סכום הפאות העליונות הוא $m$?",
      say="שאלה ממבחן. מטילים אֶן קוביות בצבעים שונים. בכמה תוצאות סכום הפאות העליונות הוא אֶם?"),
    P("הקוביות בצבעים שונים, ולכן אחת ואז שתיים, ושתיים ואז אחת, הן שתי תוצאות. לשתי קוביות וסכום 3 יש 2.",
      do=show("x-e")),
    P("ההגדרה: $T(i,j)$ הוא מספר התוצאות של $i$ קוביות שסכומן $j$.", do=show("x-d"),
      say="ההגדרה: טִי שֶל אַיי וגֵ'יי הוא מספר התוצאות של אַיי קוביות שסכומן גֵ'יי."),
    P("החלק האחרון כאן הוא הקובייה האחרונה. אם יצא בה $k$, שאר הקוביות צריכות סכום $j-k$.", do=show("x-k"),
      say="החלק האחרון כאן הוא הקובייה האחרונה. אם יצא בה קֵיי, שאר הקוביות צריכות סכום גֵ'יי פחות קֵיי."),
    P("תוצאות עם $k$ שונה בקובייה האחרונה הן שונות, ולכן מחברים על $k$ מ-1 עד 6, כל עוד הסכום לא שלילי.",
      do=show("x-f"),
      say="תוצאות עם קֵיי שונה בקובייה האחרונה הן שונות, ולכן מחברים על קֵיי מאחת עד שש, כל עוד הסכום לא שלילי."),
    P("והבסיס: אפס קוביות נותנות סכום 0 בדרך אחת. אחרת אפס דרכים.", do=show("x-b") + show("x-g")
      + GT.vals_do([(0, j) for j in range(MJ + 1)] + [(i, 0) for i in range(1, NI + 1)])),
    P("קובייה אחת: אחת לכל סכום מ-1 עד 6, ואפס מעל.", do=GT.vals_do([(1, j) for j in range(1, MJ + 1)])),
    P("שתי קוביות וסכום 3: מחברים את הסכום 2 ואת הסכום 1 של קובייה אחת. יוצא 2, כמו בדוגמה.",
      do=GT.step((2, 3), [(1, 2), (1, 1)])),
    P("וכך ממלאים את כל השורה: אפס, ואז 1, 2, 3, 4, 5, 6, ואז 5.", do=GT.vals_do([(2, j) for j in range(1, MJ + 1)]) + GT.off()),
    P("שלוש קוביות וסכום 8: מחברים שישה תאים, מסכום 7 עד סכום 2. יוצא 21.",
      do=GT.vals_do([(3, j) for j in range(1, MJ)]) + GT.step((3, 8), [(2, k) for k in range(2, 8)])),
    P("אם נספור את כל 216 התוצאות של שלוש קוביות, נמצא בדיוק 21 עם סכום 8.", do=show("x-ok")),
    P("המלכודת: לשים 0 בבסיס. אז כל סכום הוא סכום של אפסים, וכל הטבלה מתאפסת.", do=GT.off() + show("x-t"), hold=0.5),
]
exam = Scene("exam", "שאלה ממבחן", ex_ph,
             stage='<div class="dl-stack">'
                   + w.eqs("x", ["$T(i,j)=\\sum_{k=1}^{6} T(i-1,\\,j-k)\\quad (j-k\\ge 0)$",
                                 "$T(0,0)=1,\\qquad T(0,j)=0\\ (j>0),\\qquad T(i,0)=0\\ (i\\ge1)$"], 32)
                   .replace('id="x-0"', 'id="x-f"').replace('id="x-1"', 'id="x-b"')
                   + f'<div id="x-g" class="h">{GT.html()}</div>'
                   + st.card("x-ok", "rule", "🔑 $T(3,8)=1+2+3+4+5+6=21$")
                   + "</div>",
             panel=f'<div class="dl-q"><span class="qid">{Q["id"]}</span>$n$ קוביות בצבעים שונים ומספר $m$. '
                   'כתבו נוסחה ל-$T(i,j)$: מספר התוצאות של $i$ קוביות שסכומן $j$.</div>'
                   + st.card("x-e", "plain", "$n=2,\\ m=3$: $(1,2)$ ו-$(2,1)$, שתי תוצאות")
                   + st.card("x-d", "ex", "$T(i,j)$ = מספר התוצאות של $i$ קוביות עם סכום $j$")
                   + st.card("x-k", "ex", "קובייה אחרונה $k$ ← שאר הקוביות: סכום $j-k$")
                   + st.card("x-t", "trap", "⚠️ $T(0,0)=0$ מאפס את כל הטבלה"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בחיתוך ובספירה, הצעד האחרון הוא החלק האחרון.", do=show("s-1")),
    P("מינימום חלקים: אחת ועוד המינימום. מספר דרכים: סכום, כי המקרים זרים.", do=show("s-2")),
    P("והבסיס של ספירה הוא 1: יש דרך אחת לא לעשות כלום. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage='<div class="dl-stack">'
         + st.card("s-1", "rule", "🔑 הצעד האחרון = החלק האחרון")
         + st.card("s-2", "rule", "🔑 מינימום: $1+\\min$ · ספירה: $\\sum$")
         + "</div>",
   panel=st.card("s-3", "trap", "⚠️ בסיס של ספירה: 1, לא 0"))

VIDEO = Video("D07", "dp_ladder", "חיתוך ופיצול, וספירה", [title, idea, cut, exam, recap],
              bank={"24A-B-Q4a": None})
