# -*- coding: utf-8 -*-
"""K06 · האם קיימת מחרוזת עם π נתון? — video script (build: tools/video/vid.py K06).

Source: courses/kmp_prefix/C06.js (lesson + goal). Exam anchor: 22B-A-Q1a (a string over {a,b} with π = 0,0,0,0,0,1:
yes, abbbba), an open question that no guided quiz uses.
Not used on purpose: every table of the C06 quiz (0,1,0,1,2,3 / 0,0,1,2,3,4 / 0,0,1,0,1,3 / 0,1,2,0,0,1 / 0,0,1,2,1 /
0,0,0,1,2,0 / 0,0,1,2,0,1 / 0,1,0,1,2), the lesson's 0,1,2,1, the boss 22B-A-Q1b (0,0,1,1,2,1, the sibling part of the
exam anchor), and 23B-C-Q1a (used in K03). Also no table whose derivation would rebuild a quiz answer (ABABA, ABAAB...).
The worked tables 0,1,0,2,0 / 0,1,0,0,1,2 / 0,1,0,0,1,1 are new.
Every verdict is checked exhaustively below (w_kmp_prefix.feasible over restricted-growth strings, and all strings over
small alphabets), every example string by recomputing its π.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_kmp_prefix as w
from w_kmp_prefix import C, spell, nums

# ---------------------------------------------------------------- data (verified)
T1 = (0, 1, 0, 2, 0)                                     # fails the quick test: pi[4] = 2 > pi[3] + 1
assert T1[3] > T1[2] + 1 and w.feasible(T1) is None
T2 = (0, 1, 0, 0, 1, 2)                                  # exists
S2 = "AABBAA"
assert tuple(w.pi_brute(S2)[1:]) == T2 and w.feasible(T2) is not None
assert tuple(w.pi_brute("AABCAA")[1:]) == T2             # the 4th letter only has to differ from A
T3 = (0, 1, 0, 0, 1, 1)                                  # passes the quick test, still impossible
assert T3[0] == 0 and all(T3[q] <= T3[q - 1] + 1 for q in range(1, 6)) and w.feasible(T3) is None
for s in w.all_strings(6, "abcd"):
    assert tuple(w.pi_brute(s)[1:]) != T3
    p = w.pi_brute(s)[1:]
    if tuple(p[:5]) == T3[:5]:                           # first five values force P1=P2, P5=P1 ...
        assert s[0] == s[1] and s[4] == s[0] and p[5] != 1   # ... and then pi[6] is never 1
# the reason in words: pi[6]=1 forces P6 = P1 = a, and P5 = a, so "aa" is a border and pi[6] >= 2
assert w.pi_brute("AABBAA")[6] == 2

TE = (0, 0, 0, 0, 0, 1)                                  # exam
SOL = [s for s in w.all_strings(6, "ab") if tuple(w.pi_brute(s)[1:]) == TE]
assert SOL == ["abbbba", "baaaab"]
assert w.pi_brute("aabbba")[2] == 1                       # the trap example
assert w.borders("abbbba") == [1, 0]

Q = BANK["22B-A-Q1a"]
assert "0,0,0,0,0,1" in Q["question"].replace(" ", "") and "abbbba" in Q["solution"]

# ---------------------------------------------------------------- widgets
def tstrip(pfx, letters, table, **kw):
    m = len(table)
    rows = [w.row("P", "P", w.cells_of(letters), shown=False),
            w.row("pi", "π", {q: str(table[q - 1]) for q in range(1, m + 1)})]
    kw.setdefault("idx_label", "q")
    return w.Strip(pfx, m, rows, cw=82, ch=62, gap=34, fs=36, **kw)


S1 = tstrip("a", "?????", T1)
SB = tstrip("b", S2, T2)
SC = tstrip("c", "AABBAA", T3)
SE = tstrip("e", "abbbba", TE)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("שאלה קלאסית במבחן: נותנים טבלת $\\pi$, ושואלים אם יש מחרוזת שזו הטבלה שלה.",
      say="שאלה קלאסית במבחן: נותנים טבלת פאי, ושואלים אם יש מחרוזת שזו הטבלה שלה."),
    P("נלמד לתרגם כל ערך לשוויונות בין אותיות, ולמצוא סתירה, או דוגמה.", hold=0.2),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">K06 · KMP ופונקציית רישא</div><h1>האם קיימת מחרוזת עם π נתון?</h1>'
         '<p>להכריע אם טבלה נתונה היא π של איזושהי מחרוזת: לתרגם ערכים לשוויונות בין אותיות ולמצוא סתירה.</p>',
   layout="title")

idea = Scene("idea", "מתרגמים לאותיות", [
    P("$\\pi[q]=k$ גדול מאפס אומר: $k$ האותיות האחרונות של $P[1..q]$ שוות ל-$k$ הראשונות.", do=show("i-1"),
      say="פאי של קְיוּ שווה קֵיי, גדול מאפס, אומר: קֵיי האותיות האחרונות של הרישא עד קְיוּ, שוות לקֵיי הראשונות."),
    P("בפרט האות האחרונה: $P[q]=P[k]$.", do=show("i-2"), say="בפרט האות האחרונה: פִּי במקום קְיוּ שווה לפִּי במקום קֵיי."),
    P("$\\pi[q]=0$ אומר שאין אף border. בפרט $P[q]$ שונה מ-$P[1]$.", do=show("i-3"),
      say="פאי של קְיוּ שווה אפס, אומר שאין אף בּוֹרדֶר. בפרט, פִּי במקום קְיוּ שונה מפִּי במקום אחת."),
    P("ו-$\\pi[q]$ הוא **הארוך ביותר**: אסור שיהיה border ארוך יותר. כאן נמצאות רוב הסתירות.", do=show("i-4"),
      say="ופאי של קְיוּ הוא הארוך ביותר: אסור שיהיה בּוֹרדֶר ארוך יותר. כאן נמצאות רוב הסתירות."),
    P("שתי בדיקות מהירות: $\\pi[1]=0$, ו-$\\pi[q]$ לא עולה על $\\pi[q-1]$ ועוד 1.", do=show("i-5"),
      say="שתי בדיקות מהירות: פאי של אחת שווה אפס, ופאי של קְיוּ לא עולה על פאי של, בסוגריים, קְיוּ פחות אחת, ועוד אחת."),
    P("הסיבה: border חדש הוא border ישן שהתארך באות אחת.", hold=0.2,
      say="הסיבה: בּוֹרדֶר חדש הוא בּוֹרדֶר ישן, שהתארך באות אחת."),
    P("והשיטה: בונים את המחרוזת אות אחרי אות, ואז **מחשבים את ה-$\\pi$ שלה** ומשווים לטבלה.", do=show("i-6"),
      say="והשיטה: בונים את המחרוזת אות אחרי אות, ואז מחשבים את הפאי שלה, ומשווים לטבלה.", hold=0.4),
], stage='<div class="kp-stack">' + st.card("i-1", "ex", "$\\pi[q]=k>0$: $P[q-k+1..q]=P[1..k]$")
         + st.card("i-2", "rule", "🔑 בפרט $P[q]=P[k]$")
         + st.card("i-3", "rule", "🔑 $\\pi[q]=0$: בפרט $P[q]\\ne P[1]$")
         + st.card("i-4", "trap", "⚠️ ואין border ארוך מ-$\\pi[q]$") + "</div>",
   panel=st.card("i-5", "rule", "בדיקה מהירה: $\\pi[1]=0$ ו-$\\pi[q]\\le\\pi[q-1]+1$")
         + st.card("i-6", "ex", "בונים, ואז מחשבים את $\\pi$ של התוצאה ומשווים"))

ex = Scene("ex", "שלוש טבלאות", [
    P("טבלה ראשונה: 0, 1, 0, 2, 0.", do=show("a-s"), say="טבלה ראשונה: " + nums(T1) + "."),
    P("$\\pi[4]=2$ אחרי $\\pi[3]=0$: קפיצה של 2. אין מחרוזת כזו, בלי לבנות כלום.",
      do=S1.mark(S1.c("bad", "pi", 4), S1.c("cmp", "pi", 3)) + show("a-v"),
      say="פאי של ארבע שווה שתיים, אחרי פאי של שלוש שווה אפס: קפיצה של שתיים. אין מחרוזת כזו, בלי לבנות כלום."),
    P("טבלה שנייה: 0, 1, 0, 0, 1, 2. נבנה: האות הראשונה היא A.", do=S1.clear() + hide("a-s", "a-v") + show("b-s") + SB.vals("P", [1]),
      say="טבלה שנייה: " + nums(T2) + ". נבנה: האות הראשונה היא אֵיי."),
    P("$\\pi[2]=1$: $P[2]=P[1]$, עוד A. $\\pi[3]=0$: האות השלישית שונה מ-A. נקרא לה B.", do=SB.vals("P", [2, 3]),
      say="פאי של שתיים שווה אחת: האות השנייה שווה לראשונה, עוד אֵיי. פאי של שלוש שווה אפס: האות השלישית שונה מאֵיי. נקרא לה בִּי."),
    P("$\\pi[4]=0$: הרביעית שונה מ-A. ניקח שוב B.", do=SB.vals("P", [4]),
      say="פאי של ארבע שווה אפס: הרביעית שונה מאֵיי. ניקח שוב בִּי."),
    P("$\\pi[5]=1$: A. ו-$\\pi[6]=2$: $P[6]=P[2]$, כלומר A. יצא AABBAA.", do=SB.vals("P", [5, 6]),
      say="פאי של חמש שווה אחת: אֵיי. ופאי של שש שווה שתיים: האות השישית שווה לשנייה, כלומר אֵיי. יצא " + spell(S2) + "."),
    P("בדיקה: ה-$\\pi$ של AABBAA הוא בדיוק 0, 1, 0, 0, 1, 2. קיימת.", do=show("b-v"),
      say="בדיקה: הפאי של " + spell(S2) + " הוא בדיוק " + nums(T2) + ". קיימת."),
    P("טבלה שלישית: אותו דבר, רק שבסוף 1 במקום 2. ההתחלה מכריחה שוב AABBA.",
      do=hide("b-s", "b-v") + show("c-s") + SC.vals("P", [1, 2, 3, 4, 5]),
      say="טבלה שלישית: אותו דבר, רק שבסוף אחת במקום שתיים. ההתחלה מכריחה שוב " + spell("AABBA") + "."),
    P("$\\pi[6]=1$ מכריח $P[6]=P[1]=\\mathrm{A}$. אבל אז AA בסוף, ו-AA בהתחלה. $\\pi[6]$ יוצא 2, לא 1.",
      do=SC.mark(SC.bracket("P", 1, 2, "pre"), SC.bracket("P", 5, 6, "suf"), SC.c("bad", "pi", 6)) + SC.vals("P", [6])
      + show("c-x"),
      say="פאי של שש שווה אחת, מכריח שהאות השישית תהיה אֵיי. אבל אז אֵיי אֵיי בסוף, ואֵיי אֵיי בהתחלה. פאי של שש יוצא שתיים, לא אחת."),
    P("סתירה, ואין מחרוזת כזו. והבדיקה המהירה עברה! היא הכרחית, אבל לא מספיקה.", do=show("c-v"), hold=0.4),
], stage='<div class="kp-stack">'
         + f'<div class="swap" style="--swap-h:300px"><div id="a-s" class="h">{S1.html()}</div>'
         + f'<div id="b-s" class="h">{SB.html()}</div><div id="c-s" class="h">{SC.html()}</div></div>'
         + st.card("c-x", "ex", "$P[6]=\\mathrm{A}$, וגם $P[5]=\\mathrm{A}$: border באורך 2") + "</div>",
   panel=st.verdict("a", False, no="0,1,0,2,0: אין ✗")
         + st.verdict("b", True, yes="0,1,0,0,1,2: " + C(S2) + " ✓")
         + st.verdict("c", False, no="0,1,0,0,1,1: אין ✗"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: האם קיימת מחרוזת מעל $a$ ו-$b$ בלבד, עם $\\pi$ 0, 0, 0, 0, 0, 1?",
      say="שאלה ממבחן: האם קיימת מחרוזת מעל אֵיי ובִּי בלבד, עם פאי: אפס, אפס, אפס, אפס, אפס, אחת?"),
    P("$\\pi[2]$ עד $\\pi[5]$ הם 0, ולכן האותיות 2 עד 5 שונות מהראשונה.", do=show("x-s") + SE.vals("P", [1]),
      say="פאי של שתיים עד פאי של חמש הם אפס, ולכן האותיות שתיים עד חמש שונות מהראשונה."),
    P("נקרא לראשונה a. יש רק שתי אותיות, ולכן ארבע האותיות הבאות הן כולן b.", do=SE.vals("P", [2, 3, 4, 5]),
      say="נקרא לראשונה אֵיי. יש רק שתי אותיות, ולכן ארבע האותיות הבאות הן כולן בִּי."),
    P("$\\pi[6]=1$ מכריח $P[6]=P[1]$, כלומר a. יצא abbbba.", do=SE.vals("P", [6]),
      say="פאי של שש שווה אחת, מכריח שהאות השישית שווה לראשונה, כלומר אֵיי. יצא " + spell("abbbba") + "."),
    P("עכשיו בודקים שאין border ארוך יותר: באורך 2, ab בהתחלה ו-ba בסוף. שונות.",
      do=SE.mark(SE.bracket("P", 1, 2, "pre"), SE.bracket("P", 5, 6, "suf")),
      say="עכשיו בודקים שאין בּוֹרדֶר ארוך יותר: באורך שתיים, " + spell("ab") + " בהתחלה, ו" + spell("ba") + " בסוף. שונות."),
    P("וכל אורך גדול יותר מתחיל ב-a מצד אחד וב-b מצד שני. אז $\\pi[6]$ הוא בדיוק 1, והטבלה כולה מתאימה.",
      do=SE.clear() + show("x-v"),
      say="וכל אורך גדול יותר מתחיל באֵיי מצד אחד, ובבִּי מצד שני. אז פאי של שש הוא בדיוק אחת, והטבלה כולה מתאימה."),
    P("התשובה: קיימת, למשל abbbba. ויש עוד אחת בלבד: baaaab, עם השמות מוחלפים.", do=show("x-a"),
      say="התשובה: קיימת, למשל " + spell("abbbba") + ". ויש עוד אחת בלבד: " + spell("baaaab") + ", עם השמות מוחלפים."),
    P("המלכודת: לשים באמצע עוד a, כמו aabbba. אז $\\pi[2]$ כבר 1, ולא 0.", do=show("x-t"),
      say="המלכודת: לשים באמצע עוד אֵיי, כמו " + spell("aabbba") + ". אז פאי של שתיים כבר אחת, ולא אפס.", hold=0.5),
], stage=f'<div class="kp-stack"><div id="x-s" class="h">{SE.html()}</div></div>',
   panel=f'<div class="kp-q"><span class="qid">{Q["id"]}</span>האם קיימת מחרוזת $P$ מעל א״ב $\\{{a,b\\}}$ כך שפונקציית $\\pi$ '
         'שלה היא $0,0,0,0,0,1$? אם לא, נמקו. אם כן, תנו דוגמה.</div>'
         + st.verdict("x", True, yes="קיימת ✓")
         + st.card("x-a", "rule", f"🔑 {C('abbbba')} (או {C('baaaab')})")
         + st.card("x-t", "trap", f"⚠️ {C('aabbba')}: $\\pi[2]=1$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: קודם הבדיקות המהירות, $\\pi[1]=0$ ועלייה של 1 לכל היותר.", do=show("s-1"),
      say="לסיכום: קודם הבדיקות המהירות, פאי של אחת שווה אפס, ועלייה של אחת לכל היותר."),
    P("אחר כך מתרגמים כל ערך לשוויונות ואי-שוויונות בין אותיות, ובונים.", do=show("s-2"),
      say="אחר כך מתרגמים כל ערך לשוויונות ואי שוויונות בין אותיות, ובונים."),
    P("ובסוף מחשבים את $\\pi$ של מה שבנינו. ערך גבוה מדי הוא הסתירה הנפוצה. נתראה ברמה הבאה.", do=show("s-3"),
      say="ובסוף מחשבים את הפאי של מה שבנינו. ערך גבוה מדי הוא הסתירה הנפוצה. נתראה ברמה הבאה.", hold=0.6),
], stage='<div class="kp-stack">' + st.card("s-1", "rule", "🔑 $\\pi[1]=0$, $\\pi[q]\\le\\pi[q-1]+1$")
         + st.card("s-2", "rule", "🔑 ערכים → שוויונות בין אותיות") + "</div>",
   panel=st.card("s-3", "trap", "⚠️ תמיד לחשב את $\\pi$ של הדוגמה עד הסוף"))

VIDEO = Video("K06", "kmp_prefix", "האם קיימת מחרוזת עם π נתון?", [title, idea, ex, exam, recap],
              bank={"22B-A-Q1a": None})
