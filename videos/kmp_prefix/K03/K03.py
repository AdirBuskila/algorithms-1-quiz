# -*- coding: utf-8 -*-
"""K03 · π כרשימת borders: שרשרת הנסיגה — video script (build: tools/video/vid.py K03).

Source: courses/kmp_prefix/C03.js (lesson + goal). Exam anchor: 23B-C-Q1a (does a string with π = 0,1,2,3,1 exist?),
solved with the chain: π[5]-1 must be the first element of the chain of q=4 whose next letter matches. No guided quiz
uses it.
Not used on purpose: the C03 quiz pattern AABAABAA (chain 5,2,1), ABABB / AABAAA, the lesson's ABABABA, and the C06
lesson table 0,1,2,1 (same idea, shorter). The worked pattern ABACABACABAB is new (its first 7 letters appear as given
data in C02-Q1, whose asked value π[8] of ABACABAB is not shown).
Every border list, chain and fallback is computed below (w_kmp_prefix.borders / chain / prefix_trace) and checked
against the definition and the course checker's kmp_ref.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_kmp_prefix as w
from w_kmp_prefix import C, spell

# ---------------------------------------------------------------- data (verified)
S = "ABACABACABAB"
PI, STEPS = w.prefix_trace(S)
assert PI[1:] == [0, 0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 2]
H = S[:11]                                                          # ABACABACABA
assert w.borders(H) == [7, 3, 1, 0] and w.chain(PI, 11) == [7, 3, 1]
assert H[:7] == H[4:] == "ABACABA" and H[:3] == H[8:] == "ABA" and H[0] == H[10] == "A"
assert w.borders("ABACABA") == [3, 1, 0]                            # ABA is a border of the long border
assert H[:6] != H[5:] and H[:6] == "ABACAB" and H[5:] == "BACABA"   # 6 = 7-1 is no border
assert all(H[:k] != H[11 - k:] for k in (6, 5, 4, 2))
assert STEPS[12] == [(7, False), (3, False), (1, True)] and PI[12] == 2
assert [S[k] for k, _ in STEPS[12]] == ["C", "C", "B"] and S[11] == "B"
assert w.prefix_trace(H + "C")[1][12] == [(7, True)]                 # had the letter been C: one comparison, 8

T5 = (0, 1, 2, 3, 1)                                                # exam table
assert w.feasible(T5) is None
for s in w.all_strings(5, "abcde"):                                 # exhaustive: no string over 5 letters either
    assert tuple(w.pi_brute(s)[1:]) != T5
assert w.pi_brute("aaaaa")[1:] == [0, 1, 2, 3, 4] and w.pi_brute("aaaab")[1:] == [0, 1, 2, 3, 0]
assert w.chain(w.pi_brute("aaaa"), 4) == [3, 2, 1]
for s in w.all_strings(4, "ab"):                                    # the first four values force aaaa (up to renaming)
    if w.pi_brute(s)[1:] == [0, 1, 2, 3]:
        assert len(set(s)) == 1

Q = BANK["23B-C-Q1a"]
assert "0,1,2,3,1" in Q["question"].replace(" ", "") and Q.get("correctId") is None and "לא קיימת" in Q["solution"]

# ---------------------------------------------------------------- widgets
SH = w.pi_strip("h", H, shown_pi=range(1, 12), cw=76, ch=60, gap=34, fs=34, below=110)
SQ = w.pi_strip("w", S, shown_pi=range(1, 12), cw=76, ch=60, gap=34, fs=34, below=110)
LW = w.Lines("wl", height=56, size=34)
SA = w.pi_strip("a", "aaaa?", shown_pi=(1, 2, 3, 4), shown_p=(5,), cw=86, ch=62, gap=34, fs=36, below=70)


def brk(Sx, k, n):
    return [Sx.bracket("P", 1, k, "pre"), Sx.bracket("P", n - k + 1, n, "suf")]


def wline(k, eq):
    a, b = S[k], S[11]
    return f"$k={k}:\\ \\ P[{k + 1}]=\\mathrm{{{a}}}\\ {'=' if eq else '\\ne'}\\ \\mathrm{{{b}}}=P[12]$"


# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נראה שטבלת $\\pi$ יודעת יותר ממה שנראה: היא נותנת את **כל** ה-borders של כל רישא.",
      say="בסרטון הזה נראה שטבלת פאי יודעת יותר ממה שנראה: היא נותנת את כל הבּוֹרדֶרים של כל רישא."),
    P("ומשם נבין למה הנסיגה היא דווקא $k\\leftarrow\\pi[k]$.", say="ומשם נבין למה הנסיגה היא דווקא קֵיי מקבל פאי של קֵיי."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">K03 · KMP ופונקציית רישא</div><h1>π כרשימת borders: שרשרת הנסיגה</h1>'
         '<p>לקרוא מטבלת π את כל ה-borders של כל רישא, ולהבין למה הנסיגה היא דווקא k ← π[k].</p>', layout="title")

chain_sc = Scene("chain", "border של border", [
    P("המחרוזת ABACABACABA, וטבלת ה-$\\pi$ שלה.", say="המחרוזת " + spell(H) + ", וטבלת הפאי שלה."),
    P("$\\pi[11]=7$: ה-border הארוך ביותר הוא ABACABA.", do=SH.mark(*brk(SH, 7, 11), SH.c("cur", "pi", 11)),
      say="פאי של אחת עשרה שווה שבע: הבּוֹרדֶר הארוך ביותר הוא " + spell("ABACABA") + "."),
    P("אבל יש עוד borders, קצרים יותר. איך מוצאים אותם בלי לבדוק כל אורך?", do=show("c-q"),
      say="אבל יש עוד בּוֹרדֶרים, קצרים יותר. איך מוצאים אותם בלי לבדוק כל אורך?"),
    P("רעיון: ABACABA מופיעה גם בהתחלה וגם בסוף. מה שהוא border שלה, מופיע לכן בשני הקצוות.", do=show("c-1"),
      say="רעיון: " + spell("ABACABA") + " מופיעה גם בהתחלה וגם בסוף. מה שהוא בּוֹרדֶר שלה, מופיע לכן בשני הקצוות."),
    P("כלומר **border של border הוא border**. ה-border הארוך של ABACABA הוא $\\pi[7]=3$: ABA.",
      do=SH.mark(*brk(SH, 3, 11), SH.c("cur", "pi", 7), SH.arc("pi", 11, 7)) + show("c-2"),
      say="כלומר, בּוֹרדֶר של בּוֹרדֶר הוא בּוֹרדֶר. הבּוֹרדֶר הארוך של " + spell("ABACABA") + " הוא פאי של שבע, שלוש: " + spell("ABA") + "."),
    P("ושוב: $\\pi[3]=1$, האות A. ואז $\\pi[1]=0$, והשרשרת נגמרת.",
      do=SH.mark(*brk(SH, 1, 11), SH.c("cur", "pi", 3), SH.arc("pi", 11, 7), SH.arc("pi", 7, 3), SH.arc("pi", 3, 1)),
      say="ושוב: פאי של שלוש שווה אחת, האות אֵיי. ואז פאי של אחת שווה אפס, והשרשרת נגמרת."),
    P("כל ה-borders: 7, 3, 1. שלושה borders לא ריקים, כמספר האיברים בשרשרת.", do=show("c-3"),
      say="כל הבּוֹרדֶרים: שבע, שלוש, אחת. שלושה בּוֹרדֶרים לא ריקים, כמספר האיברים בשרשרת."),
    P("והשרשרת מקבלת **את כולם**: border קצר מ-7 הוא גם border של ABACABA, ולכן מגיעים אליו.", do=show("c-4"),
      say="והשרשרת מקבלת את כולם: בּוֹרדֶר קצר משבע הוא גם בּוֹרדֶר של " + spell("ABACABA") + ", ולכן מגיעים אליו."),
    P("ושימו לב: השרשרת לא יורדת באחד. 6 למשל לא border: ABACAB מול BACABA.",
      do=SH.mark(*brk(SH, 6, 11)) + show("c-t"),
      say="ושימו לב: השרשרת לא יורדת באחד. שש למשל לא בּוֹרדֶר: " + spell("ABACAB") + " מול " + spell("BACABA") + ".",
      hold=0.4),
], stage=f'<div class="kp-stack">{SH.html()}</div>',
   panel=st.card("c-q", "plain", "יש עוד borders, קצרים יותר?")
         + st.card("c-1", "ex", f"{C('ABACABA')} בהתחלה ובסוף, ולכן גם ה-borders שלה")
         + st.card("c-2", "rule", "🔑 border של border הוא border")
         + st.card("c-3", "rule", "🔑 כל ה-borders: $\\pi[q],\\ \\pi[\\pi[q]],\\ \\dots$ עד 0")
         + st.card("c-4", "ex", "border קצר מ-$\\pi[q]$ הוא border של ה-border הארוך")
         + st.card("c-t", "trap", "⚠️ השרשרת $7\\to3\\to1$ לא יורדת באחד"))

why = Scene("why", "למה k ← π[k]", [
    P("עכשיו מוסיפים אות: B. מה $\\pi[12]$?", do=show("w-s"), say="עכשיו מוסיפים אות: בִּי. מה פאי של שתים עשרה?"),
    P("ה-border החדש הוא border של $P[1..11]$ שהתארך ב-B. אז בודקים את ה-borders שלה, מהארוך.", do=show("w-1"),
      say="הבּוֹרדֶר החדש הוא בּוֹרדֶר של הרישא עד אחת עשרה, שהתארך בבִּי. אז בודקים את הבּוֹרדֶרים שלה, מהארוך."),
    P("$k=7$: האות שאחריו היא C. לא B.", do=SQ.mark(SQ.c("bad", "P", 8), SQ.c("cmp", "P", 12)) + LW.say(wline(7, False)),
      say="קֵיי שווה שבע: האות שאחריו היא סִי. לא בִּי."),
    P("ה-border הבא בשרשרת: $\\pi[7]=3$. האות שאחריו, שוב C.",
      do=SQ.mark(SQ.c("bad", "P", 4), SQ.c("cmp", "P", 12), SQ.c("cur", "pi", 7), SQ.arc("pi", 7, 3)) + LW.say(wline(3, False)),
      say="הבּוֹרדֶר הבא בשרשרת: פאי של שבע, שלוש. האות שאחריו, שוב סִי."),
    P("הבא: $\\pi[3]=1$. האות שאחרי A היא B. התאמה! לכן $\\pi[12]=2$.",
      do=SQ.mark(SQ.c("ok", "P", 2), SQ.c("cmp", "P", 12), SQ.c("cur", "pi", 3), SQ.arc("pi", 3, 1)) + LW.say(wline(1, True))
      + show(SQ.v("pi", 12)),
      say="הבא: פאי של שלוש, אחת. האות שאחרי אֵיי היא בִּי. התאמה! לכן פאי של שתים עשרה שווה שתיים."),
    P("זו בדיוק הנסיגה של האלגוריתם: $k\\leftarrow\\pi[k]$ עובר על השרשרת, border אחרי border.", do=show("w-2"),
      say="זו בדיוק הנסיגה של האלגוריתם: קֵיי מקבל פאי של קֵיי עובר על השרשרת, בּוֹרדֶר אחרי בּוֹרדֶר."),
    P("ולמה לא $k-1$? כי 6 בכלל לא border, ואין טעם לנסות להאריך אותו.", do=SQ.clear() + LW.off() + show("w-t"),
      say="ולמה לא קֵיי פחות אחת? כי שש בכלל לא בּוֹרדֶר, ואין טעם לנסות להאריך אותו."),
    P("ואילו האות החדשה הייתה C? כבר $k=7$ היה מתאים, ו-$\\pi[12]$ היה 8, בהשוואה אחת.", do=show("w-3"),
      say="ואילו האות החדשה הייתה סִי? כבר קֵיי שווה שבע היה מתאים, ופאי של שתים עשרה היה שמונה, בהשוואה אחת.", hold=0.4),
], stage=f'<div class="kp-stack"><div id="w-s" class="h">{SQ.html()}</div>{LW.html()}</div>',
   panel=st.card("w-1", "ex", "מועמדים: ה-borders של $P[1..11]$, מהארוך")
         + st.card("w-2", "rule", "🔑 $k\\leftarrow\\pi[k]$ = ה-border הבא בגודלו")
         + st.card("w-t", "trap", "⚠️ $k-1=6$ אינו border: לא בודקים אותו")
         + st.card("w-3", "plain", "אילו $P[12]$ היה C: $\\pi[12]=8$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: האם קיימת מחרוזת באורך 5 שטבלת ה-$\\pi$ שלה היא 0, 1, 2, 3, 1?",
      say="שאלה ממבחן: האם קיימת מחרוזת באורך חמש, שטבלת הפאי שלה היא אפס, אחת, שתיים, שלוש, אחת?"),
    P("$\\pi[2]=1$ אומר שהאות השנייה שווה לראשונה. נקרא לה a.", do=show("x-s") + SA.vals("P", [1, 2]),
      say="פאי של שתיים שווה אחת, אומר שהאות השנייה שווה לראשונה. נקרא לה אֵיי."),
    P("$\\pi[3]=2$ ו-$\\pi[4]=3$ מאריכים את אותו border, ולכן גם השלישית והרביעית הן a.", do=SA.vals("P", [3, 4]),
      say="פאי של שלוש שווה שתיים, ופאי של ארבע שווה שלוש, מאריכים את אותו בּוֹרדֶר. ולכן גם השלישית והרביעית הן אֵיי."),
    P("עכשיו $\\pi[5]$. המועמדים הם השרשרת של $q=4$: 3, 2, 1, ואז 0.",
      do=SA.mark(SA.arc("pi", 4, 3), SA.arc("pi", 3, 2), SA.arc("pi", 2, 1)) + show("x-1"),
      say="עכשיו פאי של חמש. המועמדים הם השרשרת של קְיוּ שווה ארבע: שלוש, שתיים, אחת, ואז אפס."),
    P("לכל מועמד משווים את האות שאחריו לאות החמישית. וכל האותיות האלה הן a.", do=show("x-2"),
      say="לכל מועמד משווים את האות שאחריו לאות החמישית. וכל האותיות האלה הן אֵיי."),
    P("אם האות החמישית היא a, כבר המועמד 3 מתאים, ו-$\\pi[5]$ יוצא גדול מ-1.", do=show("x-3"),
      say="אם האות החמישית היא אֵיי, כבר המועמד שלוש מתאים, ופאי של חמש יוצא גדול מאחת."),
    P("ואם היא לא a, אף מועמד לא מתאים, ו-$\\pi[5]=0$.", do=show("x-4"),
      say="ואם היא לא אֵיי, אף מועמד לא מתאים, ופאי של חמש שווה אפס."),
    P("הערך 1 דורש שהאות החמישית תהיה a, אבל שהמועמד 3 ייכשל. סתירה. אז **אין** מחרוזת כזו.", do=SA.clear() + show("x-v"),
      say="הערך אחת דורש שהאות החמישית תהיה אֵיי, אבל שהמועמד שלוש ייכשל. סתירה. אז אין מחרוזת כזו."),
    P("והמלכודת: לבנות aaaab, שמתאימה לארבעת הערכים הראשונים, ולא לבדוק את $\\pi[5]$. שם הוא 0.", do=show("x-t"),
      say="והמלכודת: לבנות " + spell("aaaab") + ", שמתאימה לארבעת הערכים הראשונים, ולא לבדוק את פאי של חמש. שם הוא אפס.",
      hold=0.5),
], stage=f'<div class="kp-stack"><div id="x-s" class="h">{SA.html()}</div>'
         + '<div class="kp-row">' + st.card("x-3", "ex", "חמישית a: $\\pi[5]>1$") + st.card("x-4", "ex", "חמישית לא a: $\\pi[5]=0$")
         + "</div></div>",
   panel=f'<div class="kp-q"><span class="qid">{Q["id"]}</span>האם קיימת מחרוזת $P$ באורך 5 כך שפונקציה $\\pi$ עבורה היא '
         '$0,1,2,3,1$? אם לא, נמקו. אם כן, תנו דוגמה.</div>'
         + st.card("x-1", "rule", "🔑 $\\pi[5]-1$ חייב להיות בשרשרת של $q=4$: $3,2,1,0$")
         + st.card("x-2", "ex", "האותיות שאחרי המועמדים: $P[4],P[3],P[2],P[1]$, כולן a")
         + st.verdict("x", False, no="לא קיימת ✗")
         + st.card("x-t", "trap", f"⚠️ {C('aaaab')}: $\\pi[5]=0$, לא 1"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: border של border הוא border.", do=show("r-1"), say="לסיכום: בּוֹרדֶר של בּוֹרדֶר הוא בּוֹרדֶר."),
    P("לכן כל ה-borders של $P[1..q]$ הם השרשרת $\\pi[q]$, $\\pi[\\pi[q]]$, וכן הלאה עד 0.", do=show("r-2"),
      say="לכן כל הבּוֹרדֶרים של הרישא עד קְיוּ הם השרשרת: פאי של קְיוּ, פאי של פאי של קְיוּ, וכן הלאה עד אפס."),
    P("הנסיגה $k\\leftarrow\\pi[k]$ עוברת על השרשרת הזו, ולא יורדת באחד. נתראה ברמה הבאה.", do=show("r-3"),
      say="הנסיגה, קֵיי מקבל פאי של קֵיי, עוברת על השרשרת הזו, ולא יורדת באחד. נתראה ברמה הבאה.", hold=0.6),
], stage='<div class="kp-stack">' + st.card("r-1", "rule", "🔑 border של border הוא border")
         + st.card("r-2", "rule", "🔑 $\\pi[q],\\ \\pi[\\pi[q]],\\ \\dots,\\ 0$ = כל ה-borders") + "</div>",
   panel=st.card("r-3", "trap", "⚠️ הנסיגה: $\\pi[k]$, לא $k-1$"))

VIDEO = Video("K03", "kmp_prefix", "π כרשימת borders: שרשרת הנסיגה", [title, chain_sc, why, exam, recap],
              bank={"23B-C-Q1a": None})
