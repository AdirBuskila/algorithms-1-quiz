# -*- coding: utf-8 -*-
"""K07 · טריקים: P#T, מחזוריות, הפוך ורוטציה — video script (build: tools/video/vid.py K07).

Source: courses/kmp_prefix/C07.js (lesson + goal). Exam anchor: 22A-C-Q2 (the longest palindromic prefix: the last
value of π on S#S^R), an open question that no guided quiz uses.
Not used on purpose: the C07 quiz cases (abcdabcdab, abaabaab, abcabcabc, aabaabaa, aab#aabaabaab, aa#aaa, cba in
cbacbaxcba, rotations of abcde), the lesson's aba#ababa, and the rotation trick itself (KMP on S1S1 is the answer of the
boss SAMP-1-Q2a, so the video does not state it); 25A-C-Q4a (the hidden/reversed pattern) is left alone because C07-Q5
asks the same thing. The worked cases bab#babbabab, abaaba / abaabaa and the exam's own aabaac are new.
Every π table, position and period is computed below and checked by brute force (naive search, every period, every
palindromic prefix over small alphabets).
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_kmp_prefix as w
from w_kmp_prefix import C, spell, nums

# ---------------------------------------------------------------- data (verified)
PP, TT = "bab", "babbabab"
SPT = PP + "#" + TT
PIS = w.pi_brute(SPT)
assert PIS[1:] == [0, 0, 1, 0, 1, 2, 3, 1, 2, 3, 2, 3] and max(PIS[1:]) <= 3
J = [j for j in range(1, len(SPT) + 1) if PIS[j] == 3]
assert J == [7, 10, 12] and [j - 2 * 3 for j in J] == [1, 4, 6] == w.occ_naive(TT, PP)
for p in w.all_strings(3, "ab"):                       # in general: pi = m exactly at the occurrence ends
    for t in w.all_strings(7, "ab"):
        pi = w.pi_brute(p + "#" + t)
        assert max(pi[1:]) <= 3 and [j - 6 for j in range(1, 12) if pi[j] == 3] == w.occ_naive(t, p)


def power(A):
    n = len(A)
    return any(n % d == 0 and n // d >= 2 and A == A[:d] * (n // d) for d in range(1, n))


def min_period(A):
    n = len(A)
    return min(p for p in range(1, n + 1) if all(A[i] == A[i + p] for i in range(n - p)))


for n in range(1, 10):
    for A in w.all_strings(n, "ab"):
        pn = w.pi_brute(A)[n]
        assert n - pn == min_period(A)
        assert power(A) == (pn > 0 and n % (n - pn) == 0)
A1, A2 = "abaaba", "abaabaa"
assert w.pi_brute(A1)[6] == 3 and 6 % 3 == 0 and A1 == "aba" * 2
assert w.pi_brute(A2)[7] == 4 and 7 % 3 != 0 and not power(A2)

# exam 22A-C-Q2
E = "aabaac"
SE_ = E + "#" + E[::-1]
PIE = w.pi_brute(SE_)
assert SE_ == "aabaac#caabaa" and PIE[1:] == [0, 1, 0, 1, 2, 0, 0, 0, 1, 2, 3, 4, 5] and PIE[-1] == 5
assert E[:5] == "aabaa" == E[:5][::-1] and max(PIE[1:]) == 5


def pal_prefix(S):
    return max(L for L in range(0, len(S) + 1) if S[:L] == S[:L][::-1])


for n in range(1, 8):
    for S in w.all_strings(n, "abc" if n <= 6 else "ab"):
        assert w.pi_brute(S + "#" + S[::-1])[-1] == pal_prefix(S), S
assert w.pi_brute("aaa" + "aaa")[6] == 5 > 3 and w.pi_brute("aaa#aaa")[7] == 3          # the trap: no separator
X = "abccabc"                                                          # a clear max-vs-last example
PX = w.pi_brute(X + "#" + X[::-1])
assert PX[1:] == [0, 0, 0, 0, 1, 2, 3, 0, 0, 0, 1, 0, 0, 0, 1] and max(PX[1:]) == 3 and PX[-1] == 1 == pal_prefix(X)
assert X[:3] == "abc" != X[:3][::-1]

Q = BANK["22A-C-Q2"]
assert "S#SR" in Q["solution"] and Q.get("correctId") is None

# ---------------------------------------------------------------- widgets
SS = w.pi_strip("s", SPT, cw=66, ch=56, gap=32, fs=32)
SA = w.pi_strip("a", A1, shown_pi=range(1, 7), cw=70, ch=56, gap=30, fs=32)
SB = w.pi_strip("b", A2, shown_pi=range(1, 8), cw=70, ch=56, gap=30, fs=32)
SX = w.pi_strip("x", SE_, cw=64, ch=56, gap=32, fs=32)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נשתמש בטבלת $\\pi$ לבד, בלי לולאת החיפוש, כדי לפתור שאלות שנראות אחרות.",
      say="בסרטון הזה נשתמש בטבלת פאי לבד, בלי לולאת החיפוש, כדי לפתור שאלות שנראות אחרות."),
    P("תו מפריד, מחזוריות, ותבנית הפוכה.", hold=0.2),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">K07 · KMP ופונקציית רישא</div><h1>טריקים: P#T, מחזוריות, הפוך</h1>'
         '<p>להשתמש בטבלת π לבד, או ב-KMP כקופסה שחורה, כדי לפתור את הרדוקציות הקלאסיות של המבחנים.</p>',
   layout="title")

sep = Scene("sep", "הטריק של P#T", [
    P("הטריק הראשון: במקום לחפש, מחשבים את $\\pi$ של התבנית, תו מפריד, ואחריו הטקסט.", do=show("p-1"),
      say="הטריק הראשון: במקום לחפש, מחשבים את הפאי של התבנית, תו מפריד, ואחריו הטקסט."),
    P("התבנית bab, הטקסט babbabab, והמפריד הוא סולמית, שלא מופיעה באף אחד מהם.", do=show("p-s"),
      say="התבנית " + spell(PP) + ", הטקסט " + spell(TT) + ", והמפריד הוא סולמית, שלא מופיעה באף אחד מהם."),
    P("שום border לא יכול לעבור את הסולמית, ולכן כל ערך בטבלה הוא לכל היותר 3, האורך של התבנית.",
      do=SS.vals("pi", range(1, 13)) + show("p-2"),
      say="שום בּוֹרדֶר לא יכול לעבור את הסולמית, ולכן כל ערך בטבלה הוא לכל היותר שלוש, האורך של התבנית."),
    P("ערך 3 בדיוק אומר: שלוש האותיות האחרונות הן התבנית כולה. כלומר מופע שמסתיים שם.",
      do=SS.mark(SS.c("cur", "pi", 7), SS.c("cur", "pi", 10), SS.c("cur", "pi", 12))),
    P("הערך 3 מופיע במקומות 7, 10 ו-12.", do=SS.mark(SS.c("cur", "pi", 7), SS.c("cur", "pi", 10), SS.c("cur", "pi", 12),
                                                    SS.bracket("P", 5, 7, "suf"), SS.bracket("P", 8, 10, "pre"),
                                                    SS.bracket("P", 10, 12, "suf")),
      say="הערך שלוש מופיע במקומות שבע, עשר ושתים עשרה."),
    P("כדי לעבור למקום ההתחלה בטקסט, מורידים $2m$: את התבנית, את הסולמית, ועוד $m-1$.", do=show("p-3"),
      say="כדי לעבור למקום ההתחלה בטקסט, מורידים פעמיים אֶם: את התבנית, את הסולמית, ועוד אֶם פחות אחת."),
    P("לכן המופעים מתחילים ב-1, ב-4 וב-6. שניים מהם חופפים.", do=show("p-4"),
      say="לכן המופעים מתחילים באחת, בארבע ובשש. שניים מהם חופפים.", hold=0.4),
], stage=f'<div class="kp-stack"><div id="p-s" class="h">{SS.html()}</div></div>',
   panel=st.card("p-1", "ex", "$S=P\\#T$, מחשבים רק את $\\pi$ של $S$")
         + st.card("p-2", "rule", "🔑 בגלל # : $\\pi[j]\\le m$")
         + st.card("p-3", "rule", "🔑 $\\pi[j]=m$: מופע שמתחיל ב-$j-2m$")
         + st.card("p-4", "ex", "$7-6=1,\\ 10-6=4,\\ 12-6=6$"))

per = Scene("per", "מחזוריות", [
    P("הטריק השני, על מחרוזת אחת $A$ באורך $n$: $n-\\pi[n]$ הוא התקופה הקצרה ביותר שלה.", do=show("q-1"),
      say="הטריק השני, על מחרוזת אחת אֵיי באורך אֶן: אֶן פחות פאי של אֶן, הוא התקופה הקצרה ביותר שלה."),
    P("למה? אם הרישא והסיפא באורך $\\pi[n]$ שוות, כל אות שווה לאות שנמצאת $n-\\pi[n]$ מקומות אחריה.", do=show("q-2"),
      say="למה? אם הרישא והסיפא באורך פאי של אֶן שוות, כל אות שווה לאות שנמצאת אֶן פחות פאי של אֶן מקומות אחריה."),
    P("ולהפך: כל תקופה $p$ נותנת border באורך $n-p$. לכן ה-border הארוך ביותר נותן את התקופה הקצרה ביותר.",
      say="ולהפך: כל תקופה פִּי נותנת בּוֹרדֶר באורך אֶן פחות פִּי. לכן הבּוֹרדֶר הארוך ביותר, נותן את התקופה הקצרה ביותר."),
    P("ו-$A$ היא חזרה על בלוק, לפחות פעמיים, בדיוק כש-$\\pi[n]>0$ והתקופה מחלקת את $n$.", do=show("q-3"),
      say="ואֵיי היא חזרה על בלוק, לפחות פעמיים, בדיוק כשפאי של אֶן גדול מאפס, והתקופה מחלקת את אֶן."),
    P("abaaba: $\\pi[6]=3$, התקופה 3, ו-3 מחלק 6. זו aba פעמיים.", do=show("q-a"),
      say=spell(A1) + ": פאי של שש שווה שלוש, התקופה שלוש, ושלוש מחלק שש. זו " + spell("aba") + " פעמיים."),
    P("abaabaa: $\\pi[7]=4$, התקופה שוב 3, אבל 3 לא מחלק 7. יש תקופה, אבל אין חלוקה שלמה.", do=show("q-b"),
      say=spell(A2) + ": פאי של שבע שווה ארבע, התקופה שוב שלוש, אבל שלוש לא מחלק שבע. יש תקופה, אבל אין חלוקה שלמה."),
    P("ועוד טריק קצר: תבנית שמופיעה הפוכה? הופכים אותה, ומריצים KMP רגיל.", do=show("q-r"),
      say="ועוד טריק קצר: תבנית שמופיעה הפוכה? הופכים אותה, ומריצים קֵיי אֶם פִּי רגיל.", hold=0.4),
], stage=f'<div class="kp-stack"><div id="q-a" class="h">{SA.html()}</div><div id="q-b" class="h">{SB.html()}</div></div>',
   panel=st.card("q-1", "rule", "🔑 התקופה הקצרה ביותר: $p=n-\\pi[n]$")
         + st.card("q-2", "ex", "רישא = סיפא באורך $\\pi[n]$: $A[i]=A[i+p]$")
         + st.card("q-3", "rule", "🔑 $A=B^k,\\ k\\ge2$ ⟺ $\\pi[n]>0$ ו-$p\\mid n$")
         + st.card("q-r", "ex", "הפוך: KMP על $P^R$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מקבלים מחרוזת $S$, ומחזירים את אורך הרישא הארוכה ביותר שלה שהיא פלינדרום.",
      say="שאלה ממבחן: מקבלים מחרוזת אֶס, ומחזירים את אורך הרישא הארוכה ביותר שלה שהיא פלינדרום."),
    P("למשל aabaac: הרישא aabaa נקראת אותו דבר משני הכיוונים, והתשובה 5. מה האלגוריתם היעיל ביותר?",
      say="למשל " + spell(E) + ": הרישא " + spell("aabaa") + " נקראת אותו דבר משני הכיוונים, והתשובה חמש. מה האלגוריתם היעיל ביותר?"),
    P("בונים את $S$, סולמית, ואחריה $S$ הפוכה. ומחשבים $\\pi$.", do=show("x-s"),
      say="בונים את אֶס, סולמית, ואחריה אֶס הפוכה. ומחשבים פאי."),
    P("ה-border של כל המחרוזת לא עובר את הסולמית: הוא רישא של $S$, שהיא גם סיפא של $S$ ההפוכה.", do=show("x-1"),
      say="הבּוֹרדֶר של כל המחרוזת לא עובר את הסולמית: הוא רישא של אֶס, שהיא גם סיפא של אֶס ההפוכה."),
    P("וסיפא של $S$ ההפוכה היא בדיוק הרישא באותו אורך, כשהיא הפוכה. אז הרישא שווה להיפוך של עצמה: פלינדרום.",
      do=show("x-2"),
      say="וסיפא של אֶס ההפוכה, היא בדיוק הרישא באותו אורך, כשהיא הפוכה. אז הרישא שווה להיפוך של עצמה: פלינדרום."),
    P("נחשב: עד הסולמית 0, 1, 0, 1, 2, 0. אחריה 0, 0, ואז ה-border נבנה: 1, 2, 3, 4, 5.",
      do=SX.vals("pi", range(1, 14)),
      say="נחשב: עד הסולמית " + nums(PIE[1:7]) + ". אחריה אפס, אפס, ואז הבּוֹרדֶר נבנה: " + nums(PIE[9:14]) + "."),
    P("הערך האחרון הוא 5: הרישא aabaa. זו התשובה. הזמן $O(n)$, כי המחרוזת באורך $2n+1$.",
      do=SX.mark(SX.c("cur", "pi", 13), SX.bracket("P", 1, 5, "pre"), SX.bracket("P", 9, 13, "suf")) + show("x-ans"),
      say="הערך האחרון הוא חמש: הרישא " + spell("aabaa") + ". זו התשובה. הזמן לינארי, כי המחרוזת באורך פעמיים אֶן ועוד אחת."),
    P("מלכודת: לקחת את הערך **הגדול ביותר**. ב-abccabc המקסימום 3, אבל התשובה 1: abc אינה פלינדרום.",
      do=SX.clear() + show("x-t1"),
      say="מלכודת: לקחת את הערך הגדול ביותר. ב" + spell(X) + " המקסימום שלוש, אבל התשובה אחת: " + spell("abc") + " אינה פלינדרום."),
    P("ומלכודת שנייה: לשכוח את הסולמית. ל-aaa בלי מפריד יוצא 5, יותר מאורך המחרוזת.", do=show("x-t2"),
      say="ומלכודת שנייה: לשכוח את הסולמית. ל" + spell("aaa") + " בלי מפריד יוצא חמש, יותר מאורך המחרוזת.", hold=0.5),
], stage=f'<div class="kp-stack"><div id="x-s" class="h">{SX.html()}</div>'
         + st.card("x-1", "ex", "border של $S\\#S^R$ = רישא של $S$ שהיא סיפא של $S^R$")
         + st.card("x-2", "ex", "סיפא של $S^R$ באורך $L$ = הרישא באורך $L$, הפוכה") + "</div>",
   panel=f'<div class="kp-q"><span class="qid">{Q["id"]}</span>קלט: מחרוזת $S$ באורך $n$. פלט: אורך הרישא המקסימלית של $S$ '
         f'שהיא פלינדרום. לדוגמה {C(E)} → 5. הציעו את האלגוריתם היעיל ביותר וציינו סיבוכיות.</div>'
         + st.card("x-ans", "rule", "🔑 הערך האחרון של $\\pi$ על $S\\#S^R$, בזמן $O(n)$")
         + st.card("x-t1", "trap", "⚠️ האחרון, לא המקסימום")
         + st.card("x-t2", "trap", "⚠️ בלי # : ל-" + C("aaa") + " יוצא 5"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: $P\\#T$ נותן מופעים במקומות שבהם $\\pi=m$, וההתחלה ב-$j-2m$.", do=show("s-1"),
      say="לסיכום: התבנית, סולמית והטקסט, נותנים מופעים במקומות שבהם פאי שווה אֶם, וההתחלה בגֵ'יי פחות פעמיים אֶם."),
    P("$n-\\pi[n]$ היא התקופה, ומחזורית פירושו גם $\\pi[n]>0$ וגם חלוקה שלמה.", do=show("s-2"),
      say="אֶן פחות פאי של אֶן היא התקופה, ומחזורית פירושו גם פאי של אֶן גדול מאפס, וגם חלוקה שלמה."),
    P("ו-$S\\#S^R$ נותן רישא פלינדרומית, בערך האחרון. בלי המפריד, הכול נשבר. נתראה ברמה הבאה.", do=show("s-3"),
      say="ואֶס, סולמית, ואֶס הפוכה, נותנים רישא פלינדרומית, בערך האחרון. בלי המפריד, הכול נשבר. נתראה ברמה הבאה.",
      hold=0.6),
], stage='<div class="kp-stack">' + st.card("s-1", "rule", "🔑 $P\\#T$: $\\pi[j]=m$ ⟹ מופע ב-$j-2m$")
         + st.card("s-2", "rule", "🔑 $p=n-\\pi[n]$; מחזורית ⟺ $\\pi[n]>0$, $p\\mid n$") + "</div>",
   panel=st.card("s-3", "trap", "⚠️ $S\\#S^R$: הערך האחרון; תמיד עם מפריד"))

VIDEO = Video("K07", "kmp_prefix", "טריקים: P#T, מחזוריות, הפוך", [title, sep, per, exam, recap],
              bank={"22A-C-Q2": None})
