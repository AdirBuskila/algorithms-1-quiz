# -*- coding: utf-8 -*-
"""K04 · לולאת ההתאמה של KMP וספירת השוואות — video script (build: tools/video/vid.py K04).

Source: courses/kmp_prefix/C04.js (lesson + goal). Exam anchor: 26A-A-Q5b (true/false: one run of KMP's inner loop can
take Θ(m)), an open question that no guided quiz uses.
Not used on purpose: the C04 quiz pattern AABAAC with its texts (AABAA+D, AABAA+B, AABAABAA), the C04 lesson's
ABABAC / ABABABA, the amortized-analysis argument (that is C04-Q5's answer: the video only says the total stays linear,
without the reason), and the boss 25B-A-Q3d (a letter not in the pattern, counted on ABABBAAABABA). The worked pattern
ABAABC with the text ABAABADAB is new; the exam is shown with m = 7, not the official m = 6.
Every state, comparison and count comes from w_kmp_prefix.kmp_trace (the CLRS loop), which asserts itself against the
course checker's kmp_ref.run_kmp and a naive search.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_kmp_prefix as w
from w_kmp_prefix import C, spell

# ---------------------------------------------------------------- data (verified)
PT, T = "ABAABC", "ABAABADAB"
PI = w.pi_brute(PT)
assert PI[1:] == [0, 0, 1, 1, 2, 0]
SH = [0, 3, 5, 6, 7]
MT, TR = w.matcher("m", T, PT, SH, cw=66, ch=58, gap=30, fs=34)
assert w.needed_shifts(TR) == SH
assert [e["q1"] for e in TR] == [1, 2, 3, 4, 5, 3, 0, 1, 2]
assert all(e["comps"] == [(e["i"], True)] for e in TR[:5])
assert TR[5]["comps"] == [(6, False), (3, True)] and PT[5] == "C" and PI[5] == 2
assert TR[6]["comps"] == [(4, False), (2, False), (1, False)] and PI[3] == 1 and PI[1] == 0 and "D" not in PT
assert [PT[j - 1] for j, _ in TR[6]["comps"]] == ["A", "B", "A"]
assert TR[7]["comps"] == [(1, True)] and TR[8]["comps"] == [(2, True)]
CNT = [len(e["comps"]) for e in TR]
assert CNT == [1, 1, 1, 1, 1, 2, 3, 1, 1] and sum(CNT) == 12 and not any(e["match"] for e in TR)

# exam: P = a^7, text a^6 b: the letter b costs m comparisons, m - 1 fallbacks (one run of the inner loop)
M = 7
PA = "a" * M
TA = "a" * (M - 1) + "b"
TRA = w.kmp_trace(TA, PA)
assert TRA[-1]["q0"] == M - 1 and len(TRA[-1]["comps"]) == M and [j for j, _ in TRA[-1]["comps"]] == list(range(M, 0, -1))
assert w.chain(w.pi_brute(PA), M - 1) == list(range(M - 2, 0, -1))
for m in range(2, 12):                                  # in general: m comparisons, m-1 fallbacks for the one letter
    tr = w.kmp_trace("a" * (m - 1) + "b", "a" * m)
    assert len(tr[-1]["comps"]) == m
assert sum(len(e["comps"]) for e in w.kmp_trace("a" * 10, "a" * 7)) == 10        # the trap: a full match never fails

Q = BANK["26A-A-Q5b"]
assert "\\Theta(m)" in Q["question"] and Q.get("correctId") is None and "נכון" in Q["solution"]

# ---------------------------------------------------------------- widgets
PS = w.pi_strip("ps", PT, shown_pi=range(1, 7), cw=62, ch=54, gap=26, fs=30)
SA = w.pi_strip("sa", PA, shown_pi=(), cw=80, ch=60, gap=30, fs=34, below=60)
CNTL = w.Lines("cn", height=54, size=32)
cur_shift = [None]


def cmp(i, j, eq, extra=()):
    s = i - j
    do = []
    if cur_shift[0] != s:
        do += w.shift_do(MT, s, cur_shift[0])
        cur_shift[0] = s
    return do + MT.mark(MT.c("cmp", "T", i), MT.c("ok" if eq else "bad", f"P{s}", i), *extra)


def qval(*i):
    return MT.vals("q", i)


CODE = ["KMP(T, P)",
        "  q <- 0",
        "  for i <- 1 to n",
        "    while q > 0 and P[q+1] != T[i]",
        "      q <- pi[q]",
        "    if P[q+1] = T[i]",
        "      q <- q + 1",
        "    if q = m   report ; q <- pi[q]"]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נריץ את לולאת החיפוש של KMP על טקסט, אות אחרי אות.",
      say="בסרטון הזה נריץ את לולאת החיפוש של קֵיי אֶם פִּי על טקסט, אות אחרי אות."),
    P("נעקוב אחרי המצב $q$, ונספור כמה השוואות עולה כל אות.", say="נעקוב אחרי המצב קְיוּ, ונספור כמה השוואות עולה כל אות."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">K04 · KMP ופונקציית רישא</div><h1>לולאת ההתאמה של KMP וספירת השוואות</h1>'
         '<p>לעקוב אחרי המצב q לאורך הטקסט, ולספור כמה השוואות עולה כל אות.</p>', layout="title")

idea = Scene("idea", "המצב q", [
    P("מחפשים תבנית $P$ בטקסט $T$. המשתנה $q$ אומר כמה אותיות מהתבנית מתאימות כרגע לסוף מה שקראנו.", do=show("i-1"),
      say="מחפשים תבנית פִּי בטקסט טִי. המשתנה קְיוּ אומר כמה אותיות מהתבנית מתאימות כרגע לסוף מה שקראנו."),
    P("לכן האות הבאה שמחכה בתבנית היא $P[q+1]$.", do=show("i-2"),
      say="לכן האות הבאה שמחכה בתבנית היא פִּי במקום, בסוגריים, קְיוּ ועוד אחת."),
    P("כל אות חדשה $T[i]$ מושווית אליה. שוות? $q$ גדל באחד.", do=show("i-3"),
      say="כל אות חדשה של הטקסט מושווית אליה. שוות? קְיוּ גדל באחד."),
    P("שונות ו-$q$ גדול מאפס? נסיגה $q\\leftarrow\\pi[q]$, ומשווים **את אותה אות** שוב.", do=show("i-4"),
      say="שונות, וקְיוּ גדול מאפס? נסיגה: קְיוּ מקבל פאי של קְיוּ, ומשווים את אותה אות שוב."),
    P("שונות ו-$q$ כבר 0? עוברים לאות הבאה. והאינדקס $i$ בטקסט אף פעם לא חוזר אחורה.", do=show("i-5"),
      say="שונות, וקְיוּ כבר אפס? עוברים לאות הבאה. והאינדקס בטקסט אף פעם לא חוזר אחורה."),
    P("ספירה: כל זוג של אות בטקסט ואות בתבנית נספר פעם אחת. גם השוואה מוצלחת, וגם האחרונה כש-$q=0$.",
      do=show("i-6"), say="ספירה: כל זוג של אות בטקסט ואות בתבנית נספר פעם אחת. גם השוואה מוצלחת, וגם האחרונה כשקְיוּ שווה אפס."),
    P("לכן אות שגורמת ל-$r$ נסיגות עולה $r+1$ השוואות.", do=show("i-7"),
      say="לכן אות שגורמת לאָר נסיגות, עולה אָר ועוד אחת השוואות.", hold=0.4),
], stage=f'<div class="kp-stack">{w.code("i-code", CODE, size=28)}'
         + st.card("i-1", "ex", "$q$ = כמה אותיות של $P$ מתאימות לסוף מה שנקרא") + "</div>",
   panel=st.card("i-2", "rule", "🔑 משווים $T[i]$ עם $P[q+1]$")
         + st.card("i-3", "rule", "שוות: $q\\leftarrow q+1$")
         + st.card("i-4", "rule", "שונות, $q>0$: $q\\leftarrow\\pi[q]$, ואותה אות שוב")
         + st.card("i-5", "rule", "שונות, $q=0$: לאות הבאה. $i$ לא חוזר")
         + st.card("i-6", "ex", "כל השוואה נספרת, גם המוצלחת")
         + st.card("i-7", "rule", "🔑 $r$ נסיגות = $r+1$ השוואות"))

run = Scene("run", "ריצה על טקסט", [
    P("התבנית ABAABC, והטקסט ABAABADAB. טבלת ה-$\\pi$ של התבנית בצד.", do=show("r-pi") + w.shift_do(MT, 0),
      say="התבנית " + spell(PT) + ", והטקסט " + spell(T) + ". טבלת הפאי של התבנית בצד."),
    P("חמש האותיות הראשונות מתאימות, אחת אחרי השנייה. $q$ עולה עד 5, בחמש השוואות.",
      do=cmp(5, 5, True) + qval(1, 2, 3, 4, 5) + CNTL.say("השוואות עד כה: 5"),
      say="חמש האותיות הראשונות מתאימות, אחת אחרי השנייה. קְיוּ עולה עד חמש, בחמש השוואות."),
    P("האות השישית, A, מושווית ל-$P[6]$, שהוא C. שונות.", do=cmp(6, 6, False),
      say="האות השישית, אֵיי, מושווית לפִּי במקום שש, שהוא סִי. שונות."),
    P("נסיגה: $q\\leftarrow\\pi[5]$, כלומר 2. התבנית זזה, ואותה A מושווית ל-$P[3]$. שוות! $q=3$.",
      do=cmp(6, 3, True, [PS.c("cur", "pi", 5)]) + qval(6) + CNTL.say("השוואות עד כה: 7"),
      say="נסיגה: קְיוּ מקבל פאי של חמש, כלומר שתיים. התבנית זזה, ואותה אֵיי מושווית לפִּי במקום שלוש. שוות! קְיוּ שווה שלוש."),
    P("האות הזו עלתה שתי השוואות: נסיגה אחת, ועוד השוואה.", do=show("r-c1")),
    P("האות השביעית, D, מול $P[4]$, שהוא A. שונות. נסיגה ל-$\\pi[3]$, שהוא 1.", do=cmp(7, 4, False, [PS.c("cur", "pi", 3)]),
      say="האות השביעית, דִּי, מול פִּי במקום ארבע, שהוא אֵיי. שונות. נסיגה לפאי של שלוש, שהוא אחת."),
    P("D מול $P[2]$, שהוא B. שונות. נסיגה ל-$\\pi[1]$, כלומר 0.", do=cmp(7, 2, False, [PS.c("cur", "pi", 1)]),
      say="דִּי מול פִּי במקום שתיים, שהוא בִּי. שונות. נסיגה לפאי של אחת, כלומר אפס."),
    P("ו-D מול $P[1]$. שוב שונות, ו-$q$ כבר 0. עוברים לאות הבאה עם $q=0$.",
      do=cmp(7, 1, False) + qval(7) + CNTL.say("השוואות עד כה: 10"),
      say="ודִּי מול פִּי במקום אחת. שוב שונות, וקְיוּ כבר אפס. עוברים לאות הבאה, עם קְיוּ שווה אפס."),
    P("D לא מופיעה בתבנית בכלל, אז השרשרת ירדה עד הסוף: שתי נסיגות, ושלוש השוואות.", do=show("r-c2"),
      say="דִּי לא מופיעה בתבנית בכלל, אז השרשרת ירדה עד הסוף: שתי נסיגות, ושלוש השוואות."),
    P("אחריה A ו-B מתאימות מההתחלה: $q$ שווה 1, ואז 2.", do=cmp(9, 2, True) + qval(8, 9) + CNTL.say("השוואות בסך הכול: 12"),
      say="אחריה אֵיי ובִּי מתאימות מההתחלה: קְיוּ שווה אחת, ואז שתיים."),
    P("סך הכול 12 השוואות ל-9 אותיות. והאינדקס בטקסט אף פעם לא חזר אחורה.", do=MT.clear() + show("r-c3"), hold=0.5,
      say="סך הכול שתים עשרה השוואות לתשע אותיות. והאינדקס בטקסט אף פעם לא חזר אחורה."),
], stage=f'<div class="kp-stack">{MT.html()}{CNTL.html()}</div>',
   panel=f'<div id="r-pi" class="h">{PS.html()}</div>'
         + st.card("r-c1", "ex", "A השישית: 2 השוואות (נסיגה אחת)")
         + st.card("r-c2", "trap", "⚠️ D לא בתבנית: 3 השוואות, $q$ חוזר ל-0")
         + st.card("r-c3", "rule", "🔑 12 השוואות ל-9 אותיות"))

ARCS = [SA.arc("pi", k, k - 1) for k in range(M - 1, 1, -1)]
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן, נכון או לא נכון: ייתכן שהלולאה הפנימית של KMP תרוץ בזמן $\\Theta(m)$.",
      say="שאלה ממבחן, נכון או לא נכון: ייתכן שהלולאה הפנימית של קֵיי אֶם פִּי תרוץ בזמן תטא של אֶם."),
    P("הלולאה הפנימית היא שרשרת הנסיגות של אות אחת. צריך אות שנופלת משרשרת ארוכה.", do=show("x-1")),
    P("ניקח תבנית של שבע פעמים a. כל רישא שלה היא border של הרישא הבאה.", do=show("x-s"),
      say="ניקח תבנית של שבע פעמים אֵיי. כל רישא שלה היא בּוֹרדֶר של הרישא הבאה."),
    P("והטקסט: שש פעמים a, ואז b. אחרי שש האותיות הראשונות $q=6$.", do=show("x-t"),
      say="והטקסט: שש פעמים אֵיי, ואז בִּי. אחרי שש האותיות הראשונות, קְיוּ שווה שש."),
    P("עכשיו b. היא מול $P[7]$, שונות. נסיגה ל-5, שוב שונות. ל-4, ל-3, ל-2, ל-1, ל-0.", do=SA.mark(*ARCS),
      say="עכשיו בִּי. היא מול פִּי במקום שבע, שונות. נסיגה לחמש, שוב שונות. לארבע, לשלוש, לשתיים, לאחת, לאפס."),
    P("שש נסיגות ושבע השוואות, לאות אחת. ובאופן כללי, עם $a^m$: $m-1$ נסיגות.", do=show("x-2"),
      say="שש נסיגות ושבע השוואות, לאות אחת. ובאופן כללי, עם אֶם פעמים אֵיי: אֶם פחות אחת נסיגות."),
    P("כלומר ריצה אחת של הלולאה הפנימית לוקחת $\\Theta(m)$. הטענה **נכונה**.", do=show("x-v"),
      say="כלומר ריצה אחת של הלולאה הפנימית לוקחת תטא של אֶם. הטענה נכונה."),
    P("מלכודת אחת: לבחור טקסט שמתאים לכל התבנית. בטקסט בלי אי-התאמה אין שרשרת נסיגות, והוא לא אומר כלום על הטענה.",
      do=SA.clear() + show("x-t1"),
      say="מלכודת אחת: לבחור טקסט שמתאים לכל התבנית. בטקסט בלי אי התאמה אין שרשרת נסיגות, והוא לא אומר כלום על הטענה."),
    P("ומלכודת שנייה: לחשוב שלכן KMP כולו ריבועי. השאלה שואלת על ריצה **אחת**, והזמן הכולל נשאר לינארי.",
      do=show("x-t2"),
      say="ומלכודת שנייה: לחשוב שלכן קֵיי אֶם פִּי כולו ריבועי. השאלה שואלת על ריצה אחת, והזמן הכולל נשאר לינארי.",
      hold=0.5),
], stage=f'<div class="kp-stack"><div id="x-s" class="h">{SA.html()}</div>'
         + f'<div id="x-t" class="kp-big h">T = {"a" * (M - 1)}<span style="color:var(--bad)">b</span>…</div>'
         + st.card("x-2", "rule", "🔑 $P=a^m$, טקסט $a^{m-1}b$: אות אחת, $m$ השוואות") + "</div>",
   panel=f'<div class="kp-q"><span class="qid">{Q["id"]}</span>נכון / לא נכון: ייתכן שבאלגוריתם KMP הלולאה הפנימית '
         'תתבצע בזמן $\\Theta(m)$, כאשר $m$ אורך התבנית.</div>'
         + st.card("x-1", "ex", "לולאה פנימית = שרשרת הנסיגות של אות אחת")
         + st.verdict("x", True, yes="נכון ✓")
         + st.card("x-t1", "trap", "⚠️ טקסט בלי אי-התאמה לא מוכיח כלום")
         + st.card("x-t2", "trap", "⚠️ ריצה אחת $\\Theta(m)$, הכול עדיין $O(n)$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: $q$ הוא כמה אותיות מהתבנית מתאימות כרגע, ומשווים את האות החדשה ל-$P[q+1]$.", do=show("s-1"),
      say="לסיכום: קְיוּ הוא כמה אותיות מהתבנית מתאימות כרגע, ומשווים את האות החדשה לפִּי במקום, בסוגריים, קְיוּ ועוד אחת."),
    P("אי-התאמה: נסיגה $q\\leftarrow\\pi[q]$ ואותה אות שוב. הטקסט לא חוזר אחורה.", do=show("s-2"),
      say="אי התאמה: נסיגה, קְיוּ מקבל פאי של קְיוּ, ואותה אות שוב. הטקסט לא חוזר אחורה."),
    P("ואות עם $r$ נסיגות עולה $r+1$ השוואות, כולל ההשוואה האחרונה. נתראה ברמה הבאה.", do=show("s-3"),
      say="ואות עם אָר נסיגות, עולה אָר ועוד אחת השוואות, כולל ההשוואה האחרונה. נתראה ברמה הבאה.", hold=0.6),
], stage='<div class="kp-stack">' + st.card("s-1", "rule", "🔑 $T[i]$ מול $P[q+1]$")
         + st.card("s-2", "rule", "🔑 שונות: $q\\leftarrow\\pi[q]$, אותה אות שוב") + "</div>",
   panel=st.card("s-3", "trap", "⚠️ $r$ נסיגות = $r+1$ השוואות"))

VIDEO = Video("K04", "kmp_prefix", "לולאת ההתאמה של KMP וספירת השוואות", [title, idea, run, exam, recap],
              bank={"26A-A-Q5b": None})
