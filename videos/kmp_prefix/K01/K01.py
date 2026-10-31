# -*- coding: utf-8 -*-
"""K01 · רישא, סיפא ו-border: מהו π — video script (build: tools/video/vid.py K01).

Source: courses/kmp_prefix/C01.js (lesson + goal). Exam anchor: 26A-A-Q5a (true/false: "a π table of all zeros means
no letter repeats"), an open question that no guided quiz uses.
Not used on purpose: the C01 quiz strings (AABAA, ABCABD, ABABA, AAB/ABB/AB, AAAAA) and every other level's strings;
the official counterexample ABB (it is the C01-Q4 explanation) is replaced by ABCBC; 26A-B-Q5a (the a^m table) is
left alone because C01-Q5 asks π of AAAAA. The worked string ABBAABBA is new.
Every border, π value and claim on screen is computed below and compared with the definition (w_kmp_prefix.borders /
pi_brute, which the widget also checks against the course checker's kmp_ref).
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_kmp_prefix as w
from w_kmp_prefix import C, spell

# ---------------------------------------------------------------- data (verified)
S = "ABBAABBA"
PI = w.pi_brute(S)
assert PI[1:] == [0, 0, 0, 1, 1, 2, 3, 4]
assert w.borders(S) == [4, 1, 0]                                   # borders of the whole string: ABBA and A
assert S[:3] == "ABB" and S[-3:] == "BBA" and S[:3] != S[-3:]
TRY8 = [(k, S[:k], S[8 - k:]) for k in (7, 6, 5, 4)]
assert [a == b for _, a, b in TRY8] == [False, False, False, True]
assert S[0] != S[1] and S[0] != S[2]                               # length 7 and 6 fail on the first letter (A vs B)
assert S[:5][1] != S[3:][1] and S[:5][0] == S[3:][0]               # length 5 fails on the second letter
Q5 = S[:5]
assert [Q5[:k] == Q5[5 - k:] for k in (4, 3, 2, 1)] == [False, False, False, True]
assert w.borders("AB") == [0] and w.borders("ABB") == [0]
assert all(PI[q] < q for q in range(1, 9))

X = "ABCBC"                                                        # exam counterexample
assert w.pi_brute(X)[1:] == [0] * 5 and X.count("B") == 2 and X.count("C") == 2
assert w.pi_brute("ABCA")[1:] == [0, 0, 0, 1]                      # the trap: not all zeros, refutes nothing
for n in range(1, 8):                                              # all zeros  <=>  the first letter never returns
    for s in w.all_strings(n, "ABC"):
        assert (w.pi_brute(s)[1:] == [0] * n) == (s[0] not in s[1:]), s

Q = BANK["26A-A-Q5a"]
assert "אפסים" in Q["question"] and Q.get("correctId") is None and "לא נכון" in Q["solution"]

# ---------------------------------------------------------------- widgets
S1 = w.Strip("s1", 8, [w.row("P", "P", w.cells_of(S))], idx_label="q", cw=84, ch=70, gap=40, fs=40)
S2 = w.pi_strip("s2", S, cw=84, ch=66, gap=38, fs=38)
S3 = w.pi_strip("s3", S, cw=84, ch=66, gap=38, fs=38)
SX = w.pi_strip("sx", X, cw=84, ch=66, gap=34, fs=38)


def br(Sx, a, b, c, d):
    return [Sx.bracket("P", a, b, "pre"), Sx.bracket("P", c, d, "suf")]


# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את המושג שכל אלגוריתם KMP בנוי עליו: border, ופונקציית הרישא $\\pi$.",
      say="בסרטון הזה נכיר את המושג שכל אלגוריתם קֵיי אֶם פִּי בנוי עליו: בּוֹרדֶר, ופונקציית הרישא פאי."),
    P("נחשב ערך של $\\pi$ ישר מההגדרה, בלי שום אלגוריתם.", say="נחשב ערך של פאי ישר מההגדרה, בלי שום אלגוריתם."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">K01 · KMP ופונקציית רישא</div><h1>רישא, סיפא ו-border: מהו π</h1>'
         '<p>להגדיר border ולחשב ערך בודד של π לפי ההגדרה, בלי אלגוריתם.</p>', layout="title")

idea = Scene("idea", "רישא, סיפא, border", [
    P("מחרוזת $P$ באורך $m$ נכתבת אות אחרי אות, והמקומות ממוספרים מאחת.",
      say="מחרוזת פִּי באורך אֶם נכתבת אות אחרי אות, והמקומות ממוספרים מאחת."),
    P("**רישא** היא קטע מההתחלה. למשל שלוש האותיות הראשונות: ABB.", do=S1.mark(S1.bracket("P", 1, 3, "pre")) + show("i-pre"),
      say="רישא היא קטע מההתחלה. למשל שלוש האותיות הראשונות: " + spell("ABB") + "."),
    P("**סיפא** היא קטע מהסוף. למשל שלוש האותיות האחרונות: BBA.", do=S1.mark(S1.bracket("P", 6, 8, "suf")) + show("i-suf"),
      say="סיפא היא קטע מהסוף. למשל שלוש האותיות האחרונות: " + spell("BBA") + "."),
    P("ו**אמיתית** פירושה קצרה מהמחרוזת כולה. את $P$ עצמה לא סופרים.", do=show("i-prop"),
      say="ואמיתית פירושה קצרה מהמחרוזת כולה. את פִּי עצמה לא סופרים."),
    P("**border** הוא רישא אמיתית שהיא **גם** סיפא.", do=S1.clear() + show("i-bord"),
      say="בּוֹרדֶר הוא רישא אמיתית, שהיא גם סיפא."),
    P("באורך 3 זה לא עובד: בהתחלה ABB, ובסוף BBA. הן שונות.", do=S1.mark(*br(S1, 1, 3, 6, 8)),
      say="באורך שלוש זה לא עובד: בהתחלה " + spell("ABB") + ", ובסוף " + spell("BBA") + ". הן שונות."),
    P("באורך 4 כן: בהתחלה ABBA, וגם בסוף ABBA. זה border.", do=S1.mark(*br(S1, 1, 4, 5, 8)),
      say="באורך ארבע כן: בהתחלה " + spell("ABBA") + ", וגם בסוף " + spell("ABBA") + ". זה בּוֹרדֶר."),
    P("וגם באורך 1: האות A פותחת, והאות A סוגרת. גם זה border.", do=S1.mark(*br(S1, 1, 1, 8, 8)),
      say="וגם באורך אחת: האות אֵיי פותחת, והאות אֵיי סוגרת. גם זה בּוֹרדֶר.", hold=0.3),
    P("$\\pi[q]$ הוא האורך של ה-border **הארוך ביותר** של הרישא $P[1..q]$.", do=S1.clear() + show("i-pi"),
      say="פאי של קְיוּ הוא האורך של הבּוֹרדֶר הארוך ביותר, של הרישא של פִּי עד המקום קְיוּ."),
    P("ואם אין לה אף border לא ריק, $\\pi[q]$ שווה 0.", say="ואם אין לה אף בּוֹרדֶר לא ריק, פאי של קְיוּ שווה אפס.", hold=0.4),
], stage=f'<div class="kp-stack">{S1.html()}</div>',
   panel=st.card("i-pre", "plain", "<b>רישא</b>: קטע מההתחלה")
         + st.card("i-suf", "plain", "<b>סיפא</b>: קטע מהסוף")
         + st.card("i-prop", "plain", "<b>אמיתית</b>: קצרה מ-$P$ עצמה")
         + st.card("i-bord", "rule", "🔑 <b>border</b>: רישא אמיתית שהיא גם סיפא")
         + st.card("i-pi", "rule", "🔑 $\\pi[q]$ = אורך ה-border <b>הארוך ביותר</b> של $P[1..q]$"))

EQ8 = w.eqs("d-eq", [f'<span class="kp-line">{k}: {w.cmp_line(a, b)}</span>' for k, a, b in TRY8], size=34)
defn = Scene("def8", "π לפי ההגדרה", [
    P("נחשב את $\\pi[8]$: ה-border הארוך ביותר של המחרוזת כולה.", do=show("d-s"),
      say="נחשב את פאי של שמונה: הבּוֹרדֶר הארוך ביותר של המחרוזת כולה."),
    P("השיטה: מנסים אורכים מהארוך אל הקצר, ועוצרים בהתאמה הראשונה.", do=show("d-m")),
    P("אורך 8 לא נבדק בכלל: זו המחרוזת עצמה, והיא לא רישא אמיתית.", do=show("d-t1")),
    P("אורך 7: שבע הראשונות מול שבע האחרונות. כבר האות הראשונה שונה, A מול B.",
      do=S2.mark(*br(S2, 1, 7, 2, 8)) + show("d-eq-0"),
      say="אורך שבע: שבע הראשונות מול שבע האחרונות. כבר האות הראשונה שונה, אֵיי מול בִּי."),
    P("אורך 6: גם כאן A מול B בהתחלה.", do=S2.mark(*br(S2, 1, 6, 3, 8)) + show("d-eq-1"),
      say="אורך שש: גם כאן אֵיי מול בִּי בהתחלה."),
    P("אורך 5: האות הראשונה שווה, אבל השנייה כבר לא.", do=S2.mark(*br(S2, 1, 5, 4, 8)) + show("d-eq-2")),
    P("אורך 4: ABBA מול ABBA. התאמה, ועוצרים.", do=S2.mark(*br(S2, 1, 4, 5, 8)) + show("d-eq-3"),
      say="אורך ארבע: " + spell("ABBA") + " מול " + spell("ABBA") + ". התאמה, ועוצרים."),
    P("לכן $\\pi[8]$ שווה 4.", do=show(S2.v("pi", 8), S2.c("cur", "pi", 8)), say="לכן פאי של שמונה שווה ארבע."),
    P("גם A באורך 1 הוא border, אבל קצר יותר. $\\pi$ שומר רק את הארוך ביותר.", do=S2.mark(*br(S2, 1, 1, 8, 8)) + show("d-t2"),
      say="גם אֵיי באורך אחת הוא בּוֹרדֶר, אבל קצר יותר. פאי שומר רק את הארוך ביותר.", hold=0.4),
], stage=f'<div class="kp-stack"><div id="d-s" class="h">{S2.html()}</div>{EQ8}</div>',
   panel=st.card("d-m", "rule", "🔑 מהארוך אל הקצר, עוצרים בהתאמה הראשונה")
         + st.card("d-t1", "trap", "⚠️ המחרוזת עצמה <b>אינה</b> border שלה")
         + st.card("d-t2", "ex", f"borders של {C(S)}: {C('ABBA')} (4) ו-{C('A')} (1). הארוך: 4"))

each = Scene("each", "כל q לחוד", [
    P("עכשיו כל הטבלה. $\\pi[q]$ מסתכל רק על הרישא $P[1..q]$, ולא על כל התבנית.", do=show("e-t"),
      say="עכשיו כל הטבלה. פאי של קְיוּ מסתכל רק על הרישא של פִּי עד קְיוּ, ולא על כל התבנית."),
    P("$\\pi[1]$ הוא תמיד 0: לאות אחת אין רישא אמיתית לא ריקה.", do=S3.mark(S3.c("cur", "P", 1)) + show(S3.v("pi", 1), "e-r1"),
      say="פאי של אחת הוא תמיד אפס: לאות אחת אין רישא אמיתית לא ריקה."),
    P("ב-AB וב-ABB אף רישא לא שווה לסיפא באותו אורך. לכן 0 ו-0.", do=S3.mark() + S3.vals("pi", [2, 3]),
      say="באֵיי בִּי ובאֵיי בִּי בִּי, אף רישא לא שווה לסיפא באותו אורך. לכן אפס ואפס."),
    P("ב-ABBA האות A בשני הקצוות, ולכן $\\pi[4]$ שווה 1.", do=S3.mark(*br(S3, 1, 1, 4, 4)) + S3.vals("pi", [4]),
      say="באֵיי בִּי בִּי אֵיי, האות אֵיי בשני הקצוות, ולכן פאי של ארבע שווה אחת."),
    P("ב-ABBAA האורכים 4, 3 ו-2 נכשלים, ורק A מתאימה. גם $\\pi[5]$ שווה 1.",
      do=S3.mark(*br(S3, 1, 1, 5, 5)) + S3.vals("pi", [5]),
      say="באֵיי בִּי בִּי אֵיי אֵיי, האורכים ארבע, שלוש ושתיים נכשלים, ורק אֵיי מתאימה. גם פאי של חמש שווה אחת."),
    P("משם ה-border גדל: AB, אחר כך ABB, ובסוף ABBA. כלומר 2, 3 ו-4.",
      do=S3.mark(*br(S3, 1, 3, 5, 7)) + S3.vals("pi", [6, 7, 8]),
      say="משם הבּוֹרדֶר גדל: אֵיי בִּי, אחר כך אֵיי בִּי בִּי, ובסוף אֵיי בִּי בִּי אֵיי. כלומר שתיים, שלוש וארבע."),
    P("ובכל מקום $\\pi[q]$ קטן מ-$q$, כי ה-border אמיתי.", do=S3.clear() + show("e-r2"),
      say="ובכל מקום פאי של קְיוּ קטן מקְיוּ, כי הבּוֹרדֶר אמיתי.", hold=0.4),
], stage=f'<div class="kp-stack">{S3.html()}</div>',
   panel=st.card("e-t", "trap", "⚠️ $\\pi[q]$ שייך לרישא $P[1..q]$ בלבד, וכל $q$ נבדק לחוד")
         + st.card("e-r1", "rule", "🔑 $\\pi[1]=0$ תמיד")
         + st.card("e-r2", "rule", "🔑 $\\pi[q]<q$ תמיד"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן, נכון או לא נכון: אם טבלת $\\pi$ כולה אפסים, אז אין בתבנית אות שחוזרת.",
      say="שאלה ממבחן, נכון או לא נכון: אם טבלת פאי כולה אפסים, אז אין בתבנית אות שחוזרת."),
    P("מה דרוש כדי ש-$\\pi[q]$ יהיה גדול מאפס? כל border מתחיל באות הראשונה, $P[1]$.", do=show("x-1"),
      say="מה דרוש כדי שפאי של קְיוּ יהיה גדול מאפס? כל בּוֹרדֶר מתחיל באות הראשונה של פִּי."),
    P("והעותק שלו בסוף מתחיל במקום מאוחר יותר. לכן האות הראשונה חייבת להופיע שם שוב.", do=show("x-2")),
    P("כלומר הטבלה כולה אפסים בדיוק כשהאות הראשונה לא חוזרת. על שאר האותיות זה לא אומר כלום.", do=show("x-3")),
    P("דוגמה נגדית: ABCBC. האות B חוזרת, וגם C.", do=show("x-s"),
      say="דוגמה נגדית: " + spell("ABCBC") + ". האות בִּי חוזרת, וגם סִי."),
    P("אבל A מופיעה רק בהתחלה. אף סיפא לא מתחילה ב-A, ולכן כל הערכים 0.", do=SX.vals("pi", range(1, 6)),
      say="אבל אֵיי מופיעה רק בהתחלה. אף סיפא לא מתחילה באֵיי, ולכן כל הערכים אפס."),
    P("אז הטענה **לא נכונה**.", do=show("x-v"), hold=0.3),
    P("והמלכודת: דוגמה כמו ABCA. שם A חוזרת, ו-$\\pi[4]$ שווה 1. היא לא מפריכה כלום.", do=show("x-t"),
      say="והמלכודת: דוגמה כמו " + spell("ABCA") + ". שם אֵיי חוזרת, ופאי של ארבע שווה אחת. היא לא מפריכה כלום.", hold=0.5),
], stage=f'<div class="kp-stack"><div id="x-s" class="h">{SX.html()}</div>'
         + st.card("x-1", "ex", "border באורך $k$: מתחיל ב-$P[1]$, והעותק בסוף מתחיל ב-$P[q-k+1]$")
         + st.card("x-2", "ex", "לכן $\\pi[q]>0$ דורש שהאות $P[1]$ תופיע שוב")
         + st.card("x-3", "rule", "🔑 כולה אפסים ⟺ $P[1]$ לא מופיעה שוב")
         + "</div>",
   panel=f'<div class="kp-q"><span class="qid">{Q["id"]}</span>נכון / לא נכון: אם הטבלה של $\\pi$ המתקבלת בהרצת KMP '
         'היא כולה אפסים, אז בתבנית אין אות שחוזרת על עצמה. נמקו.</div>'
         + st.verdict("x", False, no="לא נכון ✗")
         + st.card("x-t", "trap", f"⚠️ {C('ABCA')} אינה דוגמה נגדית: $\\pi[4]=1$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: border הוא רישא אמיתית שהיא גם סיפא.", do=show("r-1"), say="לסיכום: בּוֹרדֶר הוא רישא אמיתית שהיא גם סיפא."),
    P("$\\pi[q]$ הוא האורך של הארוך ביותר, ברישא $P[1..q]$ בלבד.", do=show("r-2"),
      say="פאי של קְיוּ הוא האורך של הארוך ביותר, ברישא של פִּי עד קְיוּ בלבד."),
    P("בודקים מהארוך אל הקצר, ועוצרים בהתאמה הראשונה.", do=show("r-3")),
    P("ותמיד: $\\pi[1]$ שווה 0, ו-$\\pi[q]$ קטן מ-$q$. נתראה ברמה הבאה.", do=show("r-4"),
      say="ותמיד: פאי של אחת שווה אפס, ופאי של קְיוּ קטן מקְיוּ. נתראה ברמה הבאה.", hold=0.6),
], stage='<div class="kp-stack">'
         + st.card("r-1", "rule", "🔑 border = רישא אמיתית שהיא גם סיפא")
         + st.card("r-2", "rule", "🔑 $\\pi[q]$ = הארוך ביותר, של $P[1..q]$ בלבד")
         + "</div>",
   panel=st.card("r-3", "ex", "מהארוך אל הקצר, עד ההתאמה הראשונה")
         + st.card("r-4", "trap", "⚠️ $\\pi[1]=0$ ו-$\\pi[q]<q$"))

VIDEO = Video("K01", "kmp_prefix", "רישא, סיפא ו-border: מהו π", [title, idea, defn, each, exam, recap],
              bank={"26A-A-Q5a": None})
