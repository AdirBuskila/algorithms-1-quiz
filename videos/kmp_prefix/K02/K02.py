# -*- coding: utf-8 -*-
"""K02 · חישוב π ביד, תו אחרי תו — video script (build: tools/video/vid.py K02).

Source: courses/kmp_prefix/C02.js (lesson + goal). Exam anchor: 25A-A-Q4a (the longest prefix that is also a suffix:
compute π and return π[n], not the maximum), an open question that no guided quiz uses.
Not used on purpose: the C02 quiz strings (ABACABAB, AABAABAAAB, ABCABCABD, the k <- 1 bug) and the lesson's ABAABAB;
the boss questions 25B-A-Q3c / 26B-A-Q4e (π of a 12-letter pattern) are not shown. The worked pattern ABAABAAABB is new.
Every comparison, fallback and π value is taken from w_kmp_prefix.prefix_trace (Compute-Prefix run literally) and
asserted against the definition (pi_brute) and the course checker's kmp_ref.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_kmp_prefix as w
from w_kmp_prefix import C, spell, num

# ---------------------------------------------------------------- data (verified)
S = "ABAABAAABB"
PI, STEPS = w.prefix_trace(S)
assert PI[1:] == [0, 0, 1, 1, 2, 3, 4, 1, 2, 0]
assert STEPS[2] == [(0, False)] and STEPS[3] == [(0, True)]
assert STEPS[4] == [(1, False), (0, True)]
assert STEPS[5] == [(1, True)] and STEPS[6] == [(2, True)] and STEPS[7] == [(3, True)]
assert STEPS[8] == [(4, False), (1, False), (0, True)] and PI[4] == 1 and PI[1] == 0
assert STEPS[9] == [(1, True)]
assert STEPS[10] == [(2, False), (0, False)] and PI[2] == 0
assert [S[k] for k, _ in STEPS[8]] == ["B", "B", "A"] and S[7] == "A"       # P[5], P[2], P[1] vs P[8]
# the trap: falling back to k-1 at q=8 tries length 3+1 = 4 and "matches", but 4 is no border of P[1..8]
assert S[3] == S[7] == "A" and S[:4] == "ABAA" and S[4:8] == "BAAA" and 4 not in w.borders(S[:8])
assert 3 not in w.borders(S[:7]) and w.borders(S[:4]) == [1, 0]               # 3 is no border; the next one is pi[4] = 1


def wrong_k_minus_1(P):
    m, pi, k = len(P), [None, 0], 0
    for q in range(2, m + 1):
        while k > 0 and P[k] != P[q - 1]:
            k -= 1
        if P[k] == P[q - 1]:
            k += 1
        pi.append(k)
    return pi


assert wrong_k_minus_1(S)[8] == 4 != PI[8]
assert max(PI[1:]) == 4 and PI[7] == 4 and PI[10] == 0 and w.borders(S) == [0]   # max is not the answer

E = "aabcdaabc"                                                       # the exam's own example
PE, STE = w.prefix_trace(E)
assert PE[1:] == [0, 1, 0, 0, 0, 1, 2, 3, 4] and E[:4] == E[-4:] == "aabc" and w.borders(E)[0] == 4

Q = BANK["25A-A-Q4a"]
assert Q.get("correctId") is None and "pi[n]" in Q["solution"]

# ---------------------------------------------------------------- widgets
SS = w.pi_strip("s", S, shown_pi=(1,), cw=80, ch=62, gap=34, fs=36, below=70)
L = w.Lines("rl", height=60, size=36)


def cmpline(q, k):
    a, b = S[k], S[q - 1]
    rel = "=" if a == b else "\\ne"
    return f"$q={q},\\ k={k}:\\ \\ P[{k + 1}]=\\mathrm{{{a}}}\\ {rel}\\ \\mathrm{{{b}}}=P[{q}]$"


def cmp(q, k, extra=()):
    """mark the comparison P[k+1] vs P[q] (+ extra transient ids) and write the status line"""
    eq = S[k] == S[q - 1]
    return SS.mark(SS.c("cmp", "P", k + 1), SS.c("ok" if eq else "bad", "P", q), *extra) + L.say(cmpline(q, k))


def back(q, k_from):
    """fallback k <- pi[k]: the arc in the π row (when pi[k] > 0) and the π cell read"""
    k2 = PI[k_from]
    ids = [SS.c("cur", "pi", k_from)] + ([SS.arc("pi", k_from, k2)] if k2 > 0 else [])
    return ids


CODE = ["Compute-Prefix(P)",
        "  pi[1] <- 0 ; k <- 0",
        "  for q <- 2 to m",
        "    while k > 0 and P[k+1] != P[q]",
        "      k <- pi[k]",
        "    if P[k+1] = P[q]",
        "      k <- k + 1",
        "    pi[q] <- k"]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נחשב טבלת $\\pi$ שלמה, תו אחרי תו, בלי לבדוק כל border מחדש.",
      say="בסרטון הזה נחשב טבלת פאי שלמה, תו אחרי תו, בלי לבדוק כל בּוֹרדֶר מחדש."),
    P("נראה איך ממשיכים את ה-border הקודם, ומה עושים כשהוא נתקע: נסיגה.",
      say="נראה איך ממשיכים את הבּוֹרדֶר הקודם, ומה עושים כשהוא נתקע: נסיגה."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">K02 · KMP ופונקציית רישא</div><h1>חישוב π ביד, תו אחרי תו</h1>'
         '<p>לחשב טבלת π שלמה בשיטת המועמד k, כולל נסיגות, בלי לבדוק כל border מחדש.</p>', layout="title")

idea = Scene("idea", "המועמד k", [
    P("במקום לבדוק כל אורך מחדש: אם מורידים מ-border של $P[1..q]$ את האות האחרונה, נשאר border של $P[1..q-1]$.", do=show("i-1"),
      say="במקום לבדוק כל אורך מחדש: אם מורידים מבּוֹרדֶר של הרישא עד קְיוּ את האות האחרונה, נשאר בּוֹרדֶר של הרישא עד קְיוּ פחות אחת."),
    P("לכן כל border חדש הוא border ישן שהתארך באות אחת. המועמד הראשון: $k=\\pi[q-1]$.", do=show("i-2"),
      say="לכן כל בּוֹרדֶר חדש הוא בּוֹרדֶר ישן שהתארך באות אחת. המועמד הראשון: קֵיי שווה פאי של, בסוגריים, קְיוּ פחות אחת."),
    P("משווים את $P[k+1]$, האות שאחרי המועמד, לאות החדשה $P[q]$.", do=show("i-3"),
      say="משווים את פִּי במקום, בסוגריים, קֵיי ועוד אחת, האות שאחרי המועמד, לאות החדשה, פִּי במקום קְיוּ."),
    P("שוות? אז $\\pi[q]=k+1$, וסיימנו.", do=show("i-4"), say="שוות? אז פאי של קְיוּ שווה קֵיי ועוד אחת, וסיימנו."),
    P("שונות ו-$k$ גדול מאפס? **נסיגה**: $k$ מקבל את $\\pi[k]$, ומשווים שוב.", do=show("i-5"),
      say="שונות, וקֵיי גדול מאפס? נסיגה: קֵיי מקבל את פאי של קֵיי, ומשווים שוב."),
    P("שונות ו-$k$ כבר 0? אז $\\pi[q]=0$.", do=show("i-6"), say="שונות, וקֵיי כבר אפס? אז פאי של קְיוּ שווה אפס."),
    P("וזה בדיוק הקוד: לולאת ה-while היא הנסיגות, וה-if הוא ההתארכות.", do=show("i-code"),
      say="וזה בדיוק הקוד: לולאת הווייל היא הנסיגות, והאִיף הוא ההתארכות.", hold=0.4),
], stage=f'<div class="kp-stack">' + st.card("i-1", "ex", "border של $P[1..q]$ בלי האות האחרונה = border של $P[1..q-1]$")
         + w.code("i-code", CODE, hidden=True, size=28) + "</div>",
   panel=st.card("i-2", "rule", "1. מתחילים: $k=\\pi[q-1]$")
         + st.card("i-3", "rule", "2. משווים $P[k+1]$ עם $P[q]$")
         + st.card("i-4", "rule", "3. שוות: $\\pi[q]=k+1$")
         + st.card("i-5", "rule", "4. שונות, $k>0$: נסיגה $k\\leftarrow\\pi[k]$")
         + st.card("i-6", "rule", "5. שונות, $k=0$: $\\pi[q]=0$"))

run_ph = [
    P("נחשב את כל הטבלה של ABAABAAABB. $\\pi[1]$ הוא 0, ו-$k$ מתחיל ב-0.",
      say="נחשב את כל הטבלה של " + spell(S) + ". פאי של אחת הוא אפס, וקֵיי מתחיל באפס."),
    P("$q=2$: A מול B, שונות, ו-$k$ כבר 0. לכן $\\pi[2]=0$.", do=cmp(2, 0) + SS.vals("pi", [2]),
      say="קְיוּ שווה שתיים: אֵיי מול בִּי, שונות, וקֵיי כבר אפס. לכן פאי של שתיים שווה אפס."),
    P("$q=3$: A מול A, שוות. לכן $\\pi[3]=1$.", do=cmp(3, 0) + SS.vals("pi", [3]),
      say="קְיוּ שווה שלוש: אֵיי מול אֵיי, שוות. לכן פאי של שלוש שווה אחת."),
    P("$q=4$: $k=1$, ומשווים את $P[2]$, האות B, לאות A. שונות.", do=cmp(4, 1),
      say="קְיוּ שווה ארבע: קֵיי שווה אחת, ומשווים את פִּי במקום שתיים, האות בִּי, לאות אֵיי. שונות."),
    P("נסיגה: $k\\leftarrow\\pi[1]$, כלומר 0. עכשיו A מול A, שוות. לכן $\\pi[4]=1$.",
      do=cmp(4, 0, [SS.c("cur", "pi", 1)]) + SS.vals("pi", [4]),
      say="נסיגה: קֵיי מקבל את פאי של אחת, כלומר אפס. עכשיו אֵיי מול אֵיי, שוות. לכן פאי של ארבע שווה אחת."),
    P("ב-5, 6 ו-7 יש התאמה מיד: המועמד מתארך בכל פעם באות אחת. מקבלים 2, 3 ו-4.",
      do=cmp(7, 3) + SS.vals("pi", [5, 6, 7]),
      say="בחמש, שש ושבע יש התאמה מיד: המועמד מתארך בכל פעם באות אחת. מקבלים שתיים, שלוש וארבע.", hold=0.3),
    P("$q=8$, האות A. $k=4$, ו-$P[5]$ הוא B. שונות.", do=cmp(8, 4),
      say="קְיוּ שווה שמונה, האות אֵיי. קֵיי שווה ארבע, ופִּי במקום חמש הוא בִּי. שונות."),
    P("נסיגה: $k\\leftarrow\\pi[4]$, שהוא 1. עכשיו $P[2]$, שוב B. שונות.", do=cmp(8, 1, back(8, 4)),
      say="נסיגה: קֵיי מקבל את פאי של ארבע, שהוא אחת. עכשיו פִּי במקום שתיים, שוב בִּי. שונות."),
    P("נסיגה נוספת: $k\\leftarrow\\pi[1]=0$. ו-$P[1]$ הוא A. שוות! לכן $\\pi[8]=1$.",
      do=cmp(8, 0, [SS.c("cur", "pi", 1)]) + SS.vals("pi", [8]),
      say="נסיגה נוספת: קֵיי מקבל את פאי של אחת, אפס. ופִּי במקום אחת הוא אֵיי. שוות! לכן פאי של שמונה שווה אחת."),
    P("$q=9$: $k=1$, ו-$P[2]$ הוא B, כמו $P[9]$. לכן $\\pi[9]=2$.", do=cmp(9, 1) + SS.vals("pi", [9]),
      say="קְיוּ שווה תשע: קֵיי שווה אחת, ופִּי במקום שתיים הוא בִּי, כמו פִּי במקום תשע. לכן פאי של תשע שווה שתיים."),
    P("$q=10$, האות B. $k=2$, ו-$P[3]$ הוא A. שונות, ונסיגה ל-$\\pi[2]$, כלומר 0.", do=cmp(10, 2),
      say="קְיוּ שווה עשר, האות בִּי. קֵיי שווה שתיים, ופִּי במקום שלוש הוא אֵיי. שונות, ונסיגה לפאי של שתיים, כלומר אפס."),
    P("ו-$P[1]$ הוא A, שוב שונה. $k$ כבר 0, ולכן $\\pi[10]=0$.", do=cmp(10, 0) + SS.vals("pi", [10]),
      say="ופִּי במקום אחת הוא אֵיי, שוב שונה. קֵיי כבר אפס, ולכן פאי של עשר שווה אפס."),
    P("הטבלה המלאה: 0, 0, 1, 1, 2, 3, 4, 1, 2, 0.", do=SS.clear() + L.off() + show("r-done"),
      say="הטבלה המלאה: " + w.nums(PI[1:]) + ".", hold=0.5),
]
run = Scene("run", "טבלה שלמה", run_ph,
            stage=f'<div class="kp-stack">{SS.html()}{L.html()}</div>',
            panel=st.card("r-k", "rule", "מתחילים מ-$k=\\pi[q-1]$ ומשווים $P[k+1]$ עם $P[q]$").replace(" h\"", "\"")
                  + st.card("r-b", "rule", "שונות: $k\\leftarrow\\pi[k]$ (החץ בשורת $\\pi$)").replace(" h\"", "\"")
                  + st.card("r-done", "ex", "$\\pi = 0,0,1,1,2,3,4,1,2,0$"))

ST = w.pi_strip("t", S, shown_pi=range(1, 11), cw=80, ch=62, gap=34, fs=36)
trap = Scene("trap", "k−1 במקום π[k]", [
    P("הטעות הנפוצה: אחרי אי-התאמה לרדת ל-$k-1$, במקום ל-$\\pi[k]$.", do=show("t-0"),
      say="הטעות הנפוצה: אחרי אי התאמה לרדת לקֵיי פחות אחת, במקום לפאי של קֵיי."),
    P("ב-$q=8$, אחרי ש-$k=4$ נכשל, הטעות ממשיכה ל-$k=3$. ו-$P[4]$ הוא A, שווה ל-$P[8]$.",
      do=ST.mark(ST.c("cmp", "P", 4), ST.c("ok", "P", 8)),
      say="בקְיוּ שווה שמונה, אחרי שקֵיי שווה ארבע נכשל, הטעות ממשיכה לקֵיי שווה שלוש. ופִּי במקום ארבע הוא אֵיי, שווה לפִּי במקום שמונה."),
    P("אז יוצא $\\pi[8]=4$. אבל בהתחלה ABAA, ובסוף BAAA. זה בכלל לא border.",
      do=ST.mark(ST.bracket("P", 1, 4, "pre"), ST.bracket("P", 5, 8, "suf")) + show("t-1"),
      say="אז יוצא פאי של שמונה שווה ארבע. אבל בהתחלה " + spell("ABAA") + ", ובסוף " + spell("BAAA") + ". זה בכלל לא בּוֹרדֶר."),
    P("הסיבה: מועמד חייב להיות border של $P[1..7]$. אורך 3 לא כזה: ABA מול BAA.",
      do=ST.mark(ST.bracket("P", 1, 3, "pre"), ST.bracket("P", 5, 7, "suf")),
      say="הסיבה: מועמד חייב להיות בּוֹרדֶר של הרישא עד שבע. אורך שלוש לא כזה: " + spell("ABA") + " מול " + spell("BAA") + "."),
    P("ה-border הבא אחרי 4 הוא בדיוק $\\pi[4]$, כלומר 1. ברמה הבאה נראה למה זה תמיד כך.",
      do=ST.mark(ST.c("cur", "pi", 4), ST.arc("pi", 4, 1)) + show("t-2"),
      say="הבּוֹרדֶר הבא אחרי ארבע הוא בדיוק פאי של ארבע, כלומר אחת. ברמה הבאה נראה למה זה תמיד כך.", hold=0.4),
], stage=f'<div class="kp-stack">{ST.html()}</div>',
   panel=st.card("t-0", "trap", "⚠️ נסיגה ל-$k-1$ או ל-$0$: שגוי")
         + st.card("t-1", "ex", f"הטעות נותנת $\\pi[8]=4$, אבל {C('ABAA')} ≠ {C('BAAA')}")
         + st.card("t-2", "rule", "🔑 הנסיגה: $k\\leftarrow\\pi[k]$"))

SE = w.pi_strip("e", E, cw=80, ch=60, gap=30, fs=34)
CODE_E = ["Longest-Border(S[1..n])", "  compute pi (Compute-Prefix)", "  return pi[n]"]
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מקבלים מחרוזת $S$, ומחזירים את אורך הרישא הארוכה ביותר שלה שהיא גם סיפא.", do=show("x-q"),
      say="שאלה ממבחן: מקבלים מחרוזת אֶס, ומחזירים את אורך הרישא הארוכה ביותר שלה שהיא גם סיפא."),
    P("זה בדיוק $\\pi[n]$: ה-border הארוך ביותר של המחרוזת כולה.", do=show("x-code"),
      say="זה בדיוק פאי של אֶן: הבּוֹרדֶר הארוך ביותר של המחרוזת כולה."),
    P("לכן מחשבים את $\\pi$ כמו שראינו, ומחזירים את הערך **האחרון**.", do=show("x-code-hl-2"),
      say="לכן מחשבים את פאי כמו שראינו, ומחזירים את הערך האחרון."),
    P("על הדוגמה מהשאלה, aabcdaabc: הערכים 0, 1, 0, 0, 0.", do=show("x-s") + SE.vals("pi", range(1, 6)),
      say="על הדוגמה מהשאלה, " + spell(E) + ": הערכים אפס, אחת, אפס, אפס, אפס."),
    P("ואז ה-border נבנה מחדש, אות אחרי אות: 1, 2, 3, 4.", do=SE.vals("pi", range(6, 10)),
      say="ואז הבּוֹרדֶר נבנה מחדש, אות אחרי אות: אחת, שתיים, שלוש, ארבע."),
    P("$\\pi[9]=4$: הרישא aabc היא גם הסיפא. זו בדיוק התשובה שבשאלה.",
      do=SE.mark(SE.bracket("P", 1, 4, "pre"), SE.bracket("P", 6, 9, "suf"), SE.c("cur", "pi", 9)),
      say="פאי של תשע שווה ארבע: הרישא " + spell("aabc") + " היא גם הסיפא. זו בדיוק התשובה שבשאלה."),
    P("הזמן: $O(n)$. $k$ גדל לכל היותר $n-1$ פעמים, וכל נסיגה מקטינה אותו.", do=show("x-t0"),
      say="הזמן: סדר גודל של אֶן. קֵיי גדל לכל היותר אֶן פחות אחת פעמים, וכל נסיגה מקטינה אותו."),
    P("ו-$k$ לא יורד מתחת ל-0. לכן בכל הריצה יש לכל היותר $n-1$ נסיגות.",
      say="וקֵיי לא יורד מתחת לאפס. לכן בכל הריצה יש לכל היותר אֶן פחות אחת נסיגות."),
    P("המלכודת: להחזיר את הערך **הגדול ביותר** בטבלה. בטבלה של ABAABAAABB המקסימום 4.", do=SE.clear() + show("x-t"),
      say="המלכודת: להחזיר את הערך הגדול ביותר בטבלה. בטבלה של " + spell(S) + " המקסימום ארבע."),
    P("אבל ה-4 הזה שייך לרישא ABAABAA. למחרוזת כולה $\\pi[10]=0$, ואין לה border בכלל.",
      say="אבל הארבע הזה שייך לרישא " + spell("ABAABAA") + ". למחרוזת כולה, פאי של עשר שווה אפס, ואין לה בּוֹרדֶר בכלל."),
    P("אגב, בפתרון הרשמי הודפס דווקא המקסימום, וזו טעות. וגם קריאה שבה המחרוזת עצמה נספרת התקבלה.",
      do=show("x-n"), hold=0.5),
], stage=f'<div class="kp-stack">{w.code("x-code", CODE_E, hidden=True, size=30)}<div id="x-s" class="h">{SE.html()}</div></div>',
   panel=f'<div id="x-q" class="kp-q h"><span class="qid">{Q["id"]}</span>הרישא-סיפא הארוכה ביותר. קלט: מחרוזת $S$. '
         f'פלט: אורך הרישא הארוכה ביותר של $S$ שהיא גם סיפא. לדוגמה {C(E)} → 4. כתבו את האלגוריתם היעיל ביותר.</div>'
         + st.card("x-t0", "rule", "🔑 $\\pi[n]$, בזמן $O(n)$")
         + st.card("x-t", "trap", "⚠️ לא $\\max\\pi$: ב-" + C(S) + " המקסימום 4, אבל $\\pi[10]=0$")
         + st.card("x-n", "plain", "<span style=\"font-size:26px\">הבודקים קיבלו גם את הקריאה שבה $S$ עצמה נספרת</span>"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: מחשבים את $\\pi$ לפי הסדר, ומתחילים כל צעד מ-$k=\\pi[q-1]$.", do=show("s-1"),
      say="לסיכום: מחשבים את פאי לפי הסדר, ומתחילים כל צעד מקֵיי שווה פאי של, בסוגריים, קְיוּ פחות אחת."),
    P("משווים את $P[k+1]$ ל-$P[q]$. שוות: $k+1$. שונות: נסיגה ל-$\\pi[k]$, עד התאמה או עד 0.", do=show("s-2"),
      say="משווים את פִּי במקום, בסוגריים, קֵיי ועוד אחת, לפִּי במקום קְיוּ. שוות: קֵיי ועוד אחת. שונות: נסיגה לפאי של קֵיי, עד התאמה או עד אפס."),
    P("וה-border של המחרוזת כולה הוא הערך האחרון, לא המקסימום. נתראה ברמה הבאה.", do=show("s-3"),
      say="והבּוֹרדֶר של המחרוזת כולה הוא הערך האחרון, לא המקסימום. נתראה ברמה הבאה.", hold=0.6),
], stage='<div class="kp-stack">' + st.card("s-1", "rule", "🔑 $k=\\pi[q-1]$, משווים $P[k+1]$ עם $P[q]$")
         + st.card("s-2", "rule", "🔑 שונות: $k\\leftarrow\\pi[k]$ עד התאמה או 0") + "</div>",
   panel=st.card("s-3", "trap", "⚠️ לא $k-1$; והתשובה למחרוזת כולה: $\\pi[n]$, לא המקסימום"))

VIDEO = Video("K02", "kmp_prefix", "חישוב π ביד, תו אחרי תו", [title, idea, run, trap, exam, recap],
              bank={"25A-A-Q4a": None})
