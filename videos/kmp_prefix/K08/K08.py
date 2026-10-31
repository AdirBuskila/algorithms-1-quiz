# -*- coding: utf-8 -*-
"""K08 · מבחן אמיתי: KMP ופונקציית רישא (boss walkthrough) — video script (build: tools/video/vid.py K08).

Source: courses/kmp_prefix/C08.js (boss: true; lesson = the course's toolbox). Exam anchors, none used by any guided
quiz or boss: 22A-B-Q3 (all positions where every letter differs, over {a,b}: KMP with the complemented pattern),
23A-B-Q3b (the pattern "under a substitution" over {a,b,c}: KMP for each of the 6 permutations), 26A-A-Q5c (the naive
search is not linear in the worst case).
Not used on purpose: the six boss items (25B-A-Q3c, 25B-A-Q3d, 26B-A-Q4e, 22B-A-Q1b, 26A-B-Q5b, SAMP-1-Q2a) and every
level quiz; 26A-B-Q5a (the a^m table) is skipped because its answer is C01-Q5's; the anchors of K01..K07 are not
repeated. All texts/patterns shown (bba in abbabbab, aab in cbbaacca, a^(m-1)b in a^n) are new.
Every position and count is computed below and checked by brute force (naive search, every permutation, a counting
naive matcher, and the instrumented KMP of w_kmp_prefix / the course checker's kmp_ref).
"""
import itertools
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_kmp_prefix as w
from w_kmp_prefix import C, spell

# ---------------------------------------------------------------- 22A-B-Q3: mismatch everywhere = match of the complement
SWAP = {"a": "b", "b": "a"}


def mismatch_all(T, P):
    m = len(P)
    return [i + 1 for i in range(len(T) - m + 1) if all(P[j] != T[i + j] for j in range(m))]


def comp(P):
    return "".join(SWAP[c] for c in P)


for m in range(1, 4):
    for P_ in w.all_strings(m, "ab"):
        for T_ in w.all_strings(7, "ab"):
            assert mismatch_all(T_, P_) == w.occ_naive(T_, comp(P_))
# over three letters the trick breaks: "different" no longer names one letter
assert mismatch_all("c", "a") == [1] and w.occ_naive("c", "b") == []
T1, P1 = "abbabbab", "aab"
assert comp(P1) == "bba" and mismatch_all(T1, P1) == [2, 5] == w.occ_naive(T1, "bba")
TR1 = w.kmp_trace(T1, "bba")
assert [e["i"] - 2 for e in TR1 if e["match"]] == [2, 5]
Q1 = BANK["22A-B-Q3"]
assert "KMP" in Q1["solution"] and "\\Theta(n)" in Q1["solution"]

# ---------------------------------------------------------------- 23A-B-Q3b: 6 permutations, 6 KMP runs
def subst_brute(T, P):
    m = len(P)
    out = []
    for i in range(len(T) - m + 1):
        W = T[i:i + m]
        if any("".join(dict(zip("abc", f))[c] for c in P) == W for f in itertools.permutations("abc")):
            out.append(i + 1)
    return out


def subst_kmp(T, P):
    pos = set()
    for f in itertools.permutations("abc"):
        Pf = "".join(dict(zip("abc", f))[c] for c in P)
        pos |= {e["i"] - len(P) + 1 for e in w.kmp_trace(T, Pf) if e["match"]}
    return sorted(pos)


for P_ in w.all_strings(3, "abc"):
    for T_ in itertools.islice(w.all_strings(6, "abc"), 0, 729, 7):
        assert subst_kmp(T_, P_) == subst_brute(T_, P_)
T2, P2 = "cbbaacca", "aab"
PATS = sorted({"".join(dict(zip("abc", f))[c] for c in P2) for f in itertools.permutations("abc")})
assert PATS == ["aab", "aac", "bba", "bbc", "cca", "ccb"]
assert subst_kmp(T2, P2) == [2, 4, 6] and T2[1:4] == "bba" and T2[3:6] == "aac" and T2[5:8] == "cca"
assert len({"".join(dict(zip("abc", f))[c] for c in "aaa") for f in itertools.permutations("abc")}) == 3
Q2 = BANK["23A-B-Q3b"]
assert "6" in Q2["solution"] and "KMP" in Q2["solution"]

# ---------------------------------------------------------------- 26A-A-Q5c: the naive search is quadratic
def naive_count(T, P):
    c = 0
    for i in range(len(T) - len(P) + 1):
        for j in range(len(P)):
            c += 1
            if T[i + j] != P[j]:
                break
    return c


for n in (10, 20, 40):
    m = n // 2
    Pn, Tn = "a" * (m - 1) + "b", "a" * n
    assert naive_count(Tn, Pn) == (n - m + 1) * m
    assert sum(len(e["comps"]) for e in w.kmp_trace(Tn, Pn)) <= 2 * n
assert naive_count("a" * 20, "a" * 9 + "b") == 110 and sum(len(e["comps"]) for e in w.kmp_trace("a" * 20, "a" * 9 + "b")) == 31 == 9 + 11 * 2
Q3 = BANK["26A-A-Q5c"]
assert "לא נכון" in Q3["solution"]

for qid in ("22A-B-Q3", "23A-B-Q3b", "26A-A-Q5c"):
    assert BANK[qid].get("correctId") is None

# ---------------------------------------------------------------- widgets
S1 = w.Strip("t1", 8, [w.row("T", "T", w.cells_of(T1)),
                       w.row("P2", "P'", w.cells_of("bba", 2), slot="P", hidden=True),
                       w.row("P5", "P'", w.cells_of("bba", 5), slot="P", hidden=True)],
             cw=72, ch=58, gap=32, fs=34, idx_label="i")
S2 = w.Strip("t2", 8, [w.row("T", "T", w.cells_of(T2))], cw=72, ch=58, gap=34, fs=34, idx_label="i")
B2 = [S2.bracket("T", 2, 4, "pre"), S2.bracket("T", 4, 6, "suf"), S2.bracket("T", 6, 8, "pre")]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("שלב הבוס: שלוש שאלות אמיתיות ממבחנים, עם כל הכלים של הקורס.",
      say="שלב הבּוֹס: שלוש שאלות אמיתיות ממבחנים, עם כל הכלים של הקורס."),
    P("שתי רדוקציות, שבהן KMP הוא קופסה שחורה, ושאלה על האלגוריתם הנאיבי.",
      say="שתי רדוקציות, שבהן קֵיי אֶם פִּי הוא קופסה שחורה, ושאלה על האלגוריתם הנאיבי.", hold=0.4),
], stage='<div class="kicker">K08 · KMP ופונקציית רישא</div><h1>🏆 מבחן אמיתי: KMP ופונקציית רישא</h1>'
         '<p>שלוש שאלות אמיתיות: התאמה הפוכה, חיפוש בחילוף אותיות, והאלגוריתם הנאיבי.</p>', layout="title")

q1 = Scene("q1", "שאלה 1: אי-התאמה", [
    P("שאלה ראשונה. טקסט ותבנית מעל $a$ ו-$b$. מחפשים מקומות שבהם **כל** אות בתבנית שונה מהאות שמולה בטקסט.",
      say="שאלה ראשונה. טקסט ותבנית מעל אֵיי ובִּי. מחפשים מקומות שבהם כל אות בתבנית שונה מהאות שמולה בטקסט."),
    P("המפתח: יש רק שתי אותיות. אם אות שונה מ-$a$, היא בהכרח $b$. ולהפך.", do=show("a-1"),
      say="המפתח: יש רק שתי אותיות. אם אות שונה מאֵיי, היא בהכרח בִּי. ולהפך."),
    P("אז שונה בכל מקום פירושו שווה בכל מקום לתבנית המשלימה: מחליפים בה כל a ב-b, וכל b ב-a.", do=show("a-2"),
      say="אז שונה בכל מקום, פירושו שווה בכל מקום לתבנית המשלימה: מחליפים בה כל אֵיי בבִּי, וכל בִּי באֵיי."),
    P("דוגמה: התבנית aab, המשלימה שלה היא bba. ובטקסט abbabbab, bba מופיעה במקומות 2 ו-5.", do=show("a-s", "t1-row-P2"),
      say="דוגמה: התבנית " + spell(P1) + ", המשלימה שלה היא " + spell("bba") + ". ובטקסט " + spell(T1) + ", התבנית המשלימה מופיעה במקומות שתיים וחמש."),
    P("ובשני המקומות האלה באמת כל אות של aab שונה מזו שמולה.", do=hide("t1-row-P2") + show("t1-row-P5"),
      say="ובשני המקומות האלה באמת, כל אות של " + spell(P1) + " שונה מזו שמולה."),
    P("ולמה לא לבדוק כל מקום ישירות? זה האלגוריתם הנאיבי, ובשאלה השלישית נראה שהוא ריבועי במקרה הגרוע."),
    P("האלגוריתם: בונים את התבנית המשלימה ב-$O(m)$, ומריצים KMP. הזמן $\\Theta(n)$.", do=show("a-ans"),
      say="האלגוריתם: בונים את התבנית המשלימה בזמן לינארי, ומריצים קֵיי אֶם פִּי. הזמן תטא של אֶן."),
    P("והמלכודת: עם שלוש אותיות זה נשבר. אות ששונה מ-$a$ יכולה להיות $b$ וגם $c$.", do=show("a-t"),
      say="והמלכודת: עם שלוש אותיות זה נשבר. אות ששונה מאֵיי יכולה להיות בִּי, וגם סִי.", hold=0.4),
], stage=f'<div class="kp-stack"><div id="a-s" class="h">{S1.html()}</div>'
         + st.card("a-2", "rule", "🔑 שונה בכל מקום ⟺ שווה ל-$P'$, התבנית המשלימה: $a\\leftrightarrow b$") + "</div>",
   panel=f'<div class="kp-q"><span class="qid">{Q1["id"]}</span>מעל $\\{{a,b\\}}$: כל המיקומים $i$ שבהם '
         '$p_j\\ne t_{i+j-1}$ לכל $j$. הציעו את האלגוריתם היעיל ביותר וציינו סיבוכיות.</div>'
         + st.card("a-1", "ex", "שתי אותיות: אם $x\\ne a$ אז $x=b$")
         + st.card("a-ans", "rule", "🔑 KMP על $T$ עם $P'$: $\\Theta(n)$")
         + st.card("a-t", "trap", "⚠️ מעל 3 אותיות ההחלפה לא עובדת"))

q2 = Scene("q2", "שאלה 2: חילוף אותיות", [
    P("שאלה שנייה, מעל $a$, $b$ ו-$c$. התבנית נמצאת בחילוף אם אחרי החלפת שמות האותיות, בהתאמה חד-חד-ערכית, היא מופיעה בטקסט.",
      say="שאלה שנייה, מעל אֵיי, בִּי וסִי. התבנית נמצאת בחילוף, אם אחרי החלפת שמות האותיות, בהתאמה חד חד ערכית, היא מופיעה בטקסט."),
    P("יש רק 3 כפול 2 כפול 1, כלומר שש התאמות כאלה. מספר קבוע!", do=show("b-1"),
      say="יש רק שלוש כפול שתיים כפול אחת, כלומר שש התאמות כאלה. מספר קבוע!"),
    P("אז בונים את שש התבניות, ומריצים KMP על כל אחת. שש פעמים זמן לינארי זה עדיין לינארי.", do=show("b-2"),
      say="אז בונים את שש התבניות, ומריצים קֵיי אֶם פִּי על כל אחת. שש פעמים זמן לינארי, זה עדיין לינארי."),
    P("דוגמה: aab נותנת שש תבניות: aab, aac, bba, bbc, cca ו-ccb.", do=show("b-p"),
      say="דוגמה: " + spell(P2) + " נותנת שש תבניות: שתי אותיות זהות, ואחריהן אות אחרת. למשל "
          + spell("aac") + ", או " + spell("bba") + "."),
    P("בטקסט cbbaacca נמצאות שלוש מהן: bba במקום 2, aac במקום 4, ו-cca במקום 6.", do=show("b-s", *B2),
      say="בטקסט " + spell(T2) + " נמצאות שלוש מהן: " + spell("bba") + " במקום שתיים, " + spell("aac") + " במקום ארבע, ו" + spell("cca") + " במקום שש."),
    P("ושימו לב: המופעים חופפים, וכל אחד מגיע מהחלפה אחרת.", do=show("b-3")),
    P("ולמה זה נכון? אם התבנית נמצאת בחילוף $f$, אז $f(P)$ היא אחת משש התבניות, והיא מופיעה. וגם להפך.",
      say="ולמה זה נכון? אם התבנית נמצאת בחילוף אֶף, אז התבנית אחרי ההחלפה היא אחת משש התבניות, והיא מופיעה. וגם להפך."),
    P("מלכודת: תבנית עם פחות משלוש אותיות שונות, כמו aaa, נותנת רק שלוש תבניות שונות. אסור לספור מקום פעמיים.",
      do=show("b-t"),
      say="מלכודת: תבנית עם פחות משלוש אותיות שונות, כמו " + spell("aaa") + ", נותנת רק שלוש תבניות שונות. אסור לספור מקום פעמיים.",
      hold=0.4),
], stage=f'<div class="kp-stack"><div id="b-s" class="h">{S2.html()}</div>'
         + st.card("b-p", "ex", '<span dir="ltr">' + " · ".join(C(p) for p in PATS) + "</span>")
         + st.card("b-3", "ex", '<span dir="ltr">2: ' + C("bba") + " · 4: " + C("aac") + " · 6: " + C("cca") + "</span>") + "</div>",
   panel=f'<div class="kp-q"><span class="qid">{Q2["id"]}</span>מעל $\\Sigma=\\{{a,b,c\\}}$: $P$ נמצאת בחילוף ב-$T$ אם '
         'יש $f$ חח״ע ועל כך ש-$f(p_1)\\cdots f(p_m)$ מופיעה ב-$T$. אלגוריתם לינארי שמחזיר את כל המיקומים.</div>'
         + st.card("b-1", "rule", "🔑 $3!=6$ החלפות, מספר קבוע")
         + st.card("b-2", "rule", "🔑 6 הרצות KMP: $O(n)$")
         + st.card("b-t", "trap", "⚠️ תבניות זהות: לא לדווח מקום פעמיים"))

q3 = Scene("q3", "שאלה 3: הנאיבי", [
    P("שאלה שלישית, נכון או לא נכון: האלגוריתם הנאיבי לחיפוש תבנית רץ במקרה הגרוע בזמן לינארי.",
      say="שאלה שלישית, נכון או לא נכון: האלגוריתם הנאיבי לחיפוש תבנית, רץ במקרה הגרוע בזמן לינארי."),
    P("הנאיבי בודק כל הזזה מהתחלה, ונעצר באי-ההתאמה הראשונה. היקר הוא כשהכישלון מגיע בסוף.", do=show("c-1"),
      say="הנאיבי בודק כל הזזה מהתחלה, ונעצר באי ההתאמה הראשונה. היקר הוא כשהכישלון מגיע בסוף."),
    P("טקסט של $n$ פעמים a, ותבנית של $m-1$ פעמים a ואחריהן b.", do=show("c-2"),
      say="טקסט של אֶן פעמים אֵיי, ותבנית של אֶם פחות אחת פעמים אֵיי, ואחריהן בִּי."),
    P("בכל הזזה כל ה-a מתאימות, וה-b נכשלת רק בסוף: $m$ השוואות. ויש $n-m+1$ הזזות.", do=show("c-3"),
      say="בכל הזזה כל האֵיי מתאימות, והבִּי נכשלת רק בסוף: אֶם השוואות. ויש אֶן פחות אֶם, ועוד אחת, הזזות."),
    P("כש-$m$ הוא חצי מ-$n$, זה בערך $n$ בריבוע חלקי 4. למשל ל-20 אותיות ותבנית של 10: 110 השוואות.",
      do=show("c-4"),
      say="כשאֶם הוא חצי מאֶן, זה בערך אֶן בריבוע חלקי ארבע. למשל לעשרים אותיות ותבנית של עשר: מאה ועשר השוואות."),
    P("KMP על אותו קלט: 31 השוואות. הוא אף פעם לא חוזר אחורה בטקסט.", do=show("c-5"),
      say="קֵיי אֶם פִּי על אותו קלט: שלושים ואחת השוואות. הוא אף פעם לא חוזר אחורה בטקסט."),
    P("אז הטענה **לא נכונה**: המקרה הגרוע של הנאיבי הוא $\\Theta(nm)$.", do=show("c-v"),
      say="אז הטענה לא נכונה: המקרה הגרוע של הנאיבי הוא תטא של אֶן כפול אֶם."),
    P("המלכודת: דוגמה שבה האות הראשונה נכשלת תמיד. שם יש רק $n$ השוואות, והיא לא מוכיחה כלום.", do=show("c-t"),
      say="המלכודת: דוגמה שבה האות הראשונה נכשלת תמיד. שם יש רק כאֶן השוואות, והיא לא מוכיחה כלום.", hold=0.4),
], stage='<div class="kp-stack">'
         + st.card("c-2", "ex", "$T=a^n$, $P=a^{m-1}b$")
         + st.card("c-3", "rule", "🔑 $(n-m+1)\\cdot m$ השוואות")
         + st.card("c-4", "ex", "$n=20,\\ m=10$: $11\\cdot10=110$")
         + st.card("c-5", "ex", "KMP על אותו קלט: 31") + "</div>",
   panel=f'<div class="kp-q"><span class="qid">{Q3["id"]}</span>נכון / לא נכון: האלגוריתם הנאיבי לחיפוש $P$ באורך $m$ '
         'בטקסט $T$ באורך $n$ רץ במקרה הגרוע בזמן לינארי.</div>'
         + st.card("c-1", "plain", "כל הזזה מההתחלה, עד אי-התאמה")
         + st.verdict("c", False, no="לא נכון ✗")
         + st.card("c-t", "trap", "⚠️ כישלון באות הראשונה: רק $n$ השוואות"))

recap = Scene("recap", "סיכום", [
    P("לסיכום שלב הבוס: KMP הוא קופסה שחורה לינארית. שינוי קטן בתבנית פותר בעיה אחרת.", do=show("s-1"),
      say="לסיכום שלב הבּוֹס: קֵיי אֶם פִּי הוא קופסה שחורה לינארית. שינוי קטן בתבנית פותר בעיה אחרת."),
    P("מספר קבוע של הרצות, כמו שש החלפות, משאיר את הזמן לינארי.", do=show("s-2")),
    P("והנאיבי הוא $\\Theta(nm)$ במקרה הגרוע. בהצלחה במבחן!", do=show("s-3"),
      say="והנאיבי הוא תטא של אֶן כפול אֶם במקרה הגרוע. בהצלחה במבחן!", hold=0.6),
], stage='<div class="kp-stack">' + st.card("s-1", "rule", "🔑 משנים את התבנית, ומריצים KMP")
         + st.card("s-2", "rule", "🔑 קבוע כפול לינארי = לינארי") + "</div>",
   panel=st.card("s-3", "trap", "⚠️ נאיבי: $\\Theta(nm)$ במקרה הגרוע"))

VIDEO = Video("K08", "kmp_prefix", "מבחן אמיתי: KMP ופונקציית רישא", [title, q1, q2, q3, recap],
              bank={"22A-B-Q3": None, "23A-B-Q3b": None, "26A-A-Q5c": None})
