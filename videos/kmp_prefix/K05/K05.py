# -*- coding: utf-8 -*-
"""K05 · אחרי התאמה מלאה: q ← π[m] ומיקומי מופעים — video script (build: tools/video/vid.py K05).

Source: courses/kmp_prefix/C05.js (lesson + goal). Exam anchor: 22A-A-Q2 (a linear test for "A = B^k, k >= 2":
count the occurrences of A in A*A with KMP, periodic iff at least 3), an open question that no guided quiz uses.
It needs exactly this level's point: overlapping occurrences, found only because q <- π[m].
Not used on purpose: the C05 quiz cases (AAA in AAAAAA, AABAA, ABA in ABABABA / ABABA, ABC/AB/ABCD), the lesson's
ABAB in ABABABAB, the boss 26A-B-Q5b (inner loop O(1)), and the C07 periodicity-by-π[n] strings (abcabcabc, ...).
The worked pattern ABACA in ABACABACABACA and the exam strings abbabb / abbab are new.
Every state, occurrence and count comes from w_kmp_prefix.kmp_trace (checked against the course checker's kmp_ref and
a naive search); the reset-to-0 variant and the periodicity claim are checked exhaustively below.
"""
import math
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_kmp_prefix as w
from w_kmp_prefix import C, spell

# ---------------------------------------------------------------- data (verified)
PT, T = "ABACA", "ABACABACABACA"
PI = w.pi_brute(PT)
assert PI[1:] == [0, 0, 1, 0, 1] and PI[5] == 1
SH = [0, 4, 8]
MT, TR = w.matcher("m", T, PT, SH, qrow="q", cw=64, ch=58, gap=34, fs=33)
assert w.needed_shifts(TR) == SH
ENDS = [e["i"] for e in TR if e["match"]]
assert ENDS == [5, 9, 13] and [i - 5 + 1 for i in ENDS] == [1, 5, 9] == w.occ_naive(T, PT)
assert all(len(e["comps"]) == 1 and e["comps"][0][1] for e in TR)          # every letter matches at once
assert [e["q1"] for e in TR if e["match"]] == [1, 1, 1]


def kmp_reset(T, P):
    """the buggy variant: q <- 0 after an occurrence. Returns 1-based starts."""
    pi, m, q, out = w.pi_brute(P), len(P), 0, []
    for i, c in enumerate(T, 1):
        while q > 0 and P[q] != c:
            q = pi[q]
        if P[q] == c:
            q += 1
        if q == m:
            out.append(i - m + 1)
            q = 0
    return out


assert kmp_reset(T, PT) == [1, 9]                                         # misses the occurrence at 5

# exam 22A-A-Q2: A periodic  <=>  KMP(A*A, A) >= 3
def t_count(A):
    return len([e for e in w.kmp_trace(A + A, A) if e["match"]])


def periodic(A):
    n = len(A)
    return any(n % d == 0 and n // d >= 2 and A == A[:d] * (n // d) for d in range(1, n))


for n in range(1, 9):
    for A in w.all_strings(n, "ab"):
        t = t_count(A)
        assert t >= 2 and (t >= 3) == periodic(A), A
        for s in range(1, n):                                 # occurrence at shift s  =>  period gcd(s, n) divides n
            if (A + A)[s:s + n] == A:
                g = math.gcd(s, n)
                assert A == A[:g] * (n // g)
A1, A2 = "abbabb", "abbab"
assert w.occ_naive(A1 + A1, A1) == [1, 4, 7] and t_count(A1) == 3 and periodic(A1)
assert w.occ_naive(A2 + A2, A2) == [1, 6] and t_count(A2) == 2 and not periodic(A2)
assert w.pi_brute(A1)[6] == 3 and kmp_reset(A1 + A1, A1) == [1, 7]       # q <- 0 counts 2: "not periodic", wrong

Q = BANK["22A-A-Q2"]
assert "KMP(A*A,A)" in Q["solution"].replace(" ", "") and "t\\ge 3" in Q["solution"]

# ---------------------------------------------------------------- widgets
PS = w.pi_strip("ps", PT, shown_pi=range(1, 6), cw=62, ch=54, gap=26, fs=30)
cur_shift = [None]


def cmp(i, j, extra=()):
    s = i - j
    do = []
    if cur_shift[0] != s:
        do += w.shift_do(MT, s, cur_shift[0])
        cur_shift[0] = s
    return do + MT.mark(MT.c("cmp", "T", i), MT.c("ok", f"P{s}", i), *extra)


def occ(a, b, kind):
    return MT.bracket("T", a, b, kind)


O1, O2, O3 = occ(1, 5, "pre"), occ(5, 9, "suf"), occ(9, 13, "pre")
AA1 = w.Strip("e1", 12, [w.row("T", "AA", w.cells_of(A1 + A1))], cw=62, ch=56, gap=34, fs=32, idx_label="")
E1 = [AA1.bracket("T", 1, 6, "pre"), AA1.bracket("T", 4, 9, "suf"), AA1.bracket("T", 7, 12, "pre")]
AA2 = w.Strip("e2", 10, [w.row("T", "AA", w.cells_of(A2 + A2))], cw=62, ch=56, gap=34, fs=32, idx_label="")
E2 = [AA2.bracket("T", 1, 5, "pre"), AA2.bracket("T", 6, 10, "pre")]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נראה מה KMP עושה ברגע שהתבנית כולה מתאימה.",
      say="בסרטון הזה נראה מה קֵיי אֶם פִּי עושה ברגע שהתבנית כולה מתאימה."),
    P("נמצא מופעים חופפים, ונמקם אותם בטקסט.", say="נמצא מופעים חופפים, ונמקם אותם בטקסט."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">K05 · KMP ופונקציית רישא</div><h1>אחרי התאמה מלאה: q ← π[m]</h1>'
         '<p>לדעת מה קורה כש-q מגיע ל-m, למצוא מופעים חופפים ולמקם אותם בטקסט.</p>', layout="title")

idea = Scene("idea", "q מגיע ל-m", [
    P("כש-$q$ מגיע ל-$m$, כל התבנית התאימה: יש **מופע** שמסתיים באות $T[i]$.", do=show("i-1"),
      say="כשקְיוּ מגיע לאֶם, כל התבנית התאימה: יש מופע שמסתיים באות הנוכחית של הטקסט."),
    P("הוא מתחיל $m-1$ מקומות לפני, כלומר במקום $i-m+1$.", do=show("i-2"),
      say="הוא מתחיל אֶם פחות אחת מקומות לפני, כלומר במקום אַיי פחות אֶם, ועוד אחת."),
    P("מדווחים עליו, וצריך להמשיך לחפש. מאיזה $q$ ממשיכים?", say="מדווחים עליו, וצריך להמשיך לחפש. מאיזה קְיוּ ממשיכים?"),
    P("מ-$\\pi[m]$. ה-border הארוך ביותר של $P$ הוא הסוף הארוך ביותר של מה שהתאים, שיכול לפתוח מופע חדש.",
      do=show("i-3"),
      say="מפאי של אֶם. הבּוֹרדֶר הארוך ביותר של פִּי, הוא הסוף הארוך ביותר של מה שהתאים, שיכול לפתוח מופע חדש."),
    P("ולכן המופע הבא יכול **לחפוף** לקודם.", do=show("i-4"), hold=0.4),
], stage=f'<div class="kp-stack">{w.code("i-code", ["    if q = m", "      report: starts at i - m + 1", "      q <- pi[q]"], size=32)}</div>',
   panel=st.card("i-1", "ex", "$q=m$: מופע שמסתיים ב-$T[i]$")
         + st.card("i-2", "rule", "🔑 ההתחלה: $i-m+1$")
         + st.card("i-3", "rule", "🔑 אחרי מופע: $q\\leftarrow\\pi[m]$")
         + st.card("i-4", "ex", "המופע הבא יכול לחפוף"))

run = Scene("run", "מופעים חופפים", [
    P("התבנית ABACA, עם $\\pi[5]=1$. הטקסט ABACABACABACA.", do=show("r-pi") + w.shift_do(MT, 0),
      say="התבנית " + spell(PT) + ", עם פאי של חמש שווה אחת. הטקסט " + spell(T) + "."),
    P("חמש האותיות הראשונות מתאימות, ו-$q$ מגיע ל-5, שזה $m$. מופע!", do=cmp(5, 5) + MT.vals("q", range(1, 6)) + show(O1),
      say="חמש האותיות הראשונות מתאימות, וקְיוּ מגיע לחמש, שזה אֶם. מופע!"),
    P("הוא מסתיים ב-$i=5$, ולכן מתחיל ב-$5-5+1$, כלומר 1.", do=show("r-o1"),
      say="הוא מסתיים באַיי שווה חמש, ולכן מתחיל בחמש פחות חמש ועוד אחת, כלומר אחת."),
    P("עכשיו $q\\leftarrow\\pi[5]$, כלומר 1. ה-A האחרונה כבר נחשבת תחילה של מופע חדש.",
      do=w.shift_do(MT, 4, 0) + MT.mark(MT.c("ok", "P4", 5), PS.c("cur", "pi", 5)),
      say="עכשיו קְיוּ מקבל פאי של חמש, כלומר אחת. האֵיי האחרונה כבר נחשבת תחילה של מופע חדש."),
    P("האותיות 6 עד 9 ממשיכות מ-$P[2]$, ו-$q$ שוב מגיע ל-5. מופע שני, שמתחיל ב-5.",
      do=MT.mark(MT.c("cmp", "T", 9), MT.c("ok", "P4", 9)) + MT.vals("q", range(6, 10)) + show(O2, "r-o2"),
      say="האותיות שש עד תשע ממשיכות מפִּי במקום שתיים, וקְיוּ שוב מגיע לחמש. מופע שני, שמתחיל בחמש."),
    P("ושוב $q\\leftarrow1$, והמופע השלישי מסתיים ב-13 ומתחיל ב-9.",
      do=w.shift_do(MT, 8, 4) + MT.mark(MT.c("cmp", "T", 13), MT.c("ok", "P8", 13)) + MT.vals("q", range(10, 14)) + show(O3, "r-o3"),
      say="ושוב קְיוּ מקבל אחת, והמופע השלישי מסתיים בשלוש עשרה ומתחיל בתשע."),
    P("שלושה מופעים: ב-1, ב-5 וב-9. כל שניים סמוכים חולקים אות אחת, A.", do=MT.clear() + show("r-c"),
      say="שלושה מופעים: באחת, בחמש ובתשע. כל שניים סמוכים חולקים אות אחת, אֵיי.", hold=0.4),
], stage=f'<div class="kp-stack">{MT.html()}</div>',
   panel=f'<div id="r-pi" class="h">{PS.html()}</div>'
         + st.card("r-o1", "ex", "מסתיים ב-5: מתחיל ב-1")
         + st.card("r-o2", "ex", "מסתיים ב-9: מתחיל ב-5")
         + st.card("r-o3", "ex", "מסתיים ב-13: מתחיל ב-9")
         + st.card("r-c", "rule", "🔑 3 מופעים, חופפים באות אחת"))

trap = Scene("trap", "המלכודות", [
    P("מה אם אחרי מופע מאפסים את $q$ ל-0?", do=show("t-1"), say="מה אם אחרי מופע מאפסים את קְיוּ לאפס?"),
    P("אחרי המופע הראשון, האות B מושווית ל-$P[1]$, ונכשלת. אבד המידע שה-A כבר התאימה.", do=show("t-2"),
      say="אחרי המופע הראשון, האות בִּי מושווית לפִּי במקום אחת, ונכשלת. אבד המידע שהאֵיי כבר התאימה."),
    P("המופע שמתחיל ב-5 הולך לאיבוד. הגרסה הזו מוצאת רק את 1 ואת 9.", do=show("t-3"),
      say="המופע שמתחיל בחמש הולך לאיבוד. הגרסה הזו מוצאת רק את אחת ואת תשע."),
    P("ולהשאיר $q=m$? אז ההשוואה הבאה היא מול $P[m+1]$, שלא קיים.", do=show("t-4"),
      say="ולהשאיר את קְיוּ שווה אֶם? אז ההשוואה הבאה היא מול פִּי במקום, בסוגריים, אֶם ועוד אחת, שלא קיים."),
    P("השורה $q\\leftarrow\\pi[q]$ אחרי מופע היא שורה נפרדת: היא לא חלק מלולאת הנסיגה, ולא עולה השוואה.", do=show("t-5"),
      say="השורה קְיוּ מקבל פאי של קְיוּ אחרי מופע, היא שורה נפרדת: היא לא חלק מלולאת הנסיגה, ולא עולה השוואה."),
    P("ומקום ההתחלה הוא $i-m+1$: לא $i-m$, ולא $i$.", do=show("t-6"),
      say="ומקום ההתחלה הוא אַיי פחות אֶם, ועוד אחת. לא אַיי פחות אֶם, ולא אַיי.", hold=0.4),
], stage='<div class="kp-stack">' + st.card("t-1", "plain", "גרסה שגויה: אחרי מופע $q\\leftarrow0$")
         + st.card("t-2", "ex", "$q=0$: B מול $P[1]$, נכשלת")
         + st.card("t-3", "trap", "⚠️ נמצאים רק 1 ו-9. המופע ב-5 אבד") + "</div>",
   panel=st.card("t-4", "trap", "⚠️ $q=m$ נשאר: אין $P[m+1]$")
         + st.card("t-5", "rule", "🔑 $q\\leftarrow\\pi[q]$ אחרי מופע: מחוץ ללולאת הנסיגה")
         + st.card("t-6", "trap", "⚠️ התחלה: $i-m+1$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מחרוזת $A$ מחזורית אם $A=B^k$ עבור $k$ גדול או שווה ל-2. בדקו זאת בזמן לינארי, בעזרת KMP.",
      say="שאלה ממבחן: מחרוזת אֵיי מחזורית, אם היא שרשור של קֵיי עותקים של מחרוזת בִּי, עבור קֵיי גדול או שווה לשתיים. בדקו זאת בזמן לינארי, בעזרת קֵיי אֶם פִּי."),
    P("הרעיון: סופרים כמה פעמים $A$ מופיעה בתוך $A$ משורשרת לעצמה.", do=show("x-1"),
      say="הרעיון: סופרים כמה פעמים אֵיי מופיעה בתוך אֵיי משורשרת לעצמה."),
    P("דוגמה: abbabb. בתוך abbabbabbabb היא מופיעה במקומות 1, 4 ו-7. שלוש פעמים.", do=show("x-s1", *E1),
      say="דוגמה: " + spell(A1) + ". בתוך המחרוזת המשורשרת היא מופיעה במקומות אחת, ארבע ושבע. שלוש פעמים."),
    P("ודוגמה שאינה מחזורית: abbab. בשרשור שלה יש רק שני מופעים, בהתחלה ובאמצע.", do=show("x-s2", *E2),
      say="ודוגמה שאינה מחזורית: " + spell(A2) + ". בשרשור שלה יש רק שני מופעים, בהתחלה ובאמצע."),
    P("שני מופעים יש תמיד: בהתחלה ובמקום $n+1$. מופע שלישי אומר ש-$A$ שווה לסיבוב שלה ב-$s$ מקומות.",
      do=show("x-2"),
      say="שני מופעים יש תמיד: בהתחלה ובמקום אֶן ועוד אחת. מופע שלישי אומר שאֵיי שווה לסיבוב שלה באֶס מקומות."),
    P("סיבוב ב-$s$ וסיבוב ב-$n$ מחזירים את $A$, ולכן גם כל צירוף שלהם, כולל המחלק המשותף הגדול שלהם.",
      do=show("x-3"),
      say="סיבוב באֶס וסיבוב באֶן מחזירים את אֵיי, ולכן גם כל צירוף שלהם, כולל המחלק המשותף הגדול שלהם."),
    P("סיבוב במחלק הזה, שקטן מ-$n$ ומחלק אותו, מחזיר את $A$. לכן $A$ היא חזרה על הרישא באורך הזה.",
      say="סיבוב במחלק הזה, שקטן מאֶן ומחלק אותו, מחזיר את אֵיי. לכן אֵיי היא חזרה על הרישא באורך הזה."),
    P("ובכיוון השני: אם $A=B^k$, אז $A$ מופיעה בשרשור גם במקום $|B|+1$. זה המופע השלישי.", do=show("x-4"),
      say="ובכיוון השני: אם אֵיי היא קֵיי עותקים של בִּי, אז אֵיי מופיעה בשרשור גם מיד אחרי העותק הראשון של בִּי. זה המופע השלישי."),
    P("התשובה: $t=KMP(A{*}A, A)$, ומחזירים אמת אם ורק אם $t$ לפחות 3. הזמן לינארי.", do=show("x-ans"),
      say="התשובה: סופרים עם קֵיי אֶם פִּי את המופעים של אֵיי בשרשור, ומחזירים אמת אם ורק אם יש לפחות שלושה. הזמן לינארי."),
    P("מלכודת: $t\\ge2$. זה מתקיים תמיד, ואז כל מחרוזת יוצאת מחזורית.", do=show("x-t1"),
      say="מלכודת: לפחות שניים. זה מתקיים תמיד, ואז כל מחרוזת יוצאת מחזורית."),
    P("ומלכודת שנייה: המופעים חופפים. KMP שמאפס את $q$ אחרי מופע מוצא ב-abbabb רק שניים, ועונה לא.",
      do=show("x-t2"),
      say="ומלכודת שנייה: המופעים חופפים. קֵיי אֶם פִּי שמאפס את קְיוּ אחרי מופע, מוצא ב" + spell(A1) + " רק שניים, ועונה לא.",
      hold=0.5),
], stage='<div class="kp-stack">'
         + f'<div id="x-s1" class="h">{AA1.html()}</div><div id="x-s2" class="h">{AA2.html()}</div>'
         + st.card("x-2", "ex", "מופע ב-$s+1$, $0<s<n$: $A$ שווה לסיבוב שלה ב-$s$")
         + st.card("x-3", "ex", "ולכן $A=(A[1..g])^{n/g}$, עם $g=\\gcd(s,n)<n$")
         + st.card("x-4", "ex", "$A=B^k$: מופע גם ב-$|B|+1$") + "</div>",
   panel=f'<div class="kp-q"><span class="qid">{Q["id"]}</span>$A$ מחזורית אם $A=B^k$ עבור $k\\ge2$. הציעו אלגוריתם '
         'לינארי שבודק אם $A$ מחזורית. $KMP(X,Y)$ = מספר המופעים של $Y$ ב-$X$.</div>'
         + st.card("x-1", "plain", "סופרים את $A$ בתוך $A{*}A$")
         + st.card("x-ans", "rule", "🔑 $t=KMP(A{*}A,A)$; מחזורית ⟺ $t\\ge3$")
         + st.card("x-t1", "trap", "⚠️ $t\\ge2$ תמיד מתקיים")
         + st.card("x-t2", "trap", "⚠️ חופפים! עם $q\\leftarrow0$: רק 2 מופעים"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: כש-$q=m$ יש מופע, והוא מתחיל ב-$i-m+1$.", do=show("s-1"),
      say="לסיכום: כשקְיוּ שווה אֶם יש מופע, והוא מתחיל באַיי פחות אֶם, ועוד אחת."),
    P("אחרי מופע: $q\\leftarrow\\pi[m]$. לא 0, ולא להשאיר $m$.", do=show("s-2"),
      say="אחרי מופע: קְיוּ מקבל פאי של אֶם. לא אפס, ולא להשאיר אֶם."),
    P("כך נמצאים גם מופעים חופפים, ובשאלות סופרים את כולם. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage='<div class="kp-stack">' + st.card("s-1", "rule", "🔑 $q=m$: מופע שמתחיל ב-$i-m+1$")
         + st.card("s-2", "rule", "🔑 $q\\leftarrow\\pi[m]$") + "</div>",
   panel=st.card("s-3", "trap", "⚠️ מופעים חופפים נספרים כולם"))

VIDEO = Video("K05", "kmp_prefix", "אחרי התאמה מלאה: q ← π[m]", [title, idea, run, trap, exam, recap],
              bank={"22A-A-Q2": None})
