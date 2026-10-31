# -*- coding: utf-8 -*-
"""G06 · תרמיל שברי מול תרמיל 0/1 — video script (build: tools/video/vid.py G06).

Source: courses/greedy_proofs/C06.js (goal: when the ratio greedy is optimal (fractional) and when it fails (0/1), and
special cases where a greedy is exact). Exam anchors: 26B-A-Q2a (a counterexample to the ratio greedy for tasks),
26B-A-Q2b (equal times: the greedy) and 26B-A-Q2c (its proof and running time), open questions no guided level uses.
Avoided on purpose: the C06 quiz/lesson data ((60,10),(100,20),(120,30) with 50; weights 2,3,6,8 / values 9,7,5,1
with 11; T=5 with (1,2),(5,9); t=3, T=10, profits 5,9,2,7,4) and 25A-C-Q2 (a twin of the C06 knapsack data).
New data: items (20,4),(12,3),(24,8) with W=12; the counterexample T=10 with (2,6),(10,20); equal times t=4, T=13,
profits 7,3,10,6,8,2. Every value is computed below and checked with CHK.knap_frac / CHK.knap01_opt / brute force.
"""
import itertools
from fractions import Fraction as F
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_greedy_proofs as W

CHK = W.CHK

# ---------------------------------------------------------------- worked: one item set, two versions
ITEMS = [(20, 4), (12, 3), (24, 8)]                        # (value, weight), already by ratio 5, 4, 3
CAP = 12
R = [F(v, w) for v, w in ITEMS]
assert R == [5, 4, 3]
assert CHK.knap_frac(ITEMS, CAP) == 47                     # all of 1 and 2 (weight 7), then 5 of 8 of item 3: 15
assert 4 + 3 + 5 == CAP and F(24) * 5 / 8 == 15 and 20 + 12 + 15 == 47
assert CHK.knap01_ratio_greedy(ITEMS, CAP) == 32 and 8 > CAP - 7   # 0/1: item 3 no longer fits
assert CHK.knap01_opt(ITEMS, CAP) == 44 and 4 + 8 == CAP and 20 + 24 == 44
# the exchange on a non-greedy fractional solution: 1/4 of item 1, all of 2 and 3 (weight 1+3+8 = 12, value 41)
before = F(20) * F(1, 4) + 12 + 24
d = 3                                                       # move 3 kg from item 3 (ratio 3) to item 1 (ratio 5)
after = F(20) * F(1 + d, 4) + 12 + F(24) * F(8 - d, 8)
assert before == 41 and after == 47 and after - before == d * (5 - 3)

# ---------------------------------------------------------------- exam 26B-A-Q2: tasks with time and profit, total T
QA, QB, QC = BANK["26B-A-Q2a"], BANK["26B-A-Q2b"], BANK["26B-A-Q2c"]
assert QA["contextId"] == "26B-A-c2"
CE, TT = [(6, 2), (20, 10)], 10                             # (profit, time): ratios 3 and 2
assert CHK.knap01_ratio_greedy(CE, TT) == 6 and CHK.knap01_opt(CE, TT) == 20
t, T = 4, 13
PROF = [7, 3, 10, 6, 8, 2]
k = T // t
assert k == 3 and (k + 1) * t > T
top = sorted(PROF, reverse=True)[:k]
assert top == [10, 8, 7] and sum(top) == 25
assert CHK.knap01_opt([(v, t) for v in PROF], T) == 25
# the greedy (top k profits) is optimal on every small equal-time instance
for n in range(1, 6):
    for prof in itertools.product(range(1, 5), repeat=n):
        for TT2 in range(0, 13):
            kk = TT2 // 3
            assert sum(sorted(prof, reverse=True)[:kk]) == CHK.knap01_opt([(v, 3) for v in prof], TT2)

TAB = W.table("it", ["פריט", "ערך", "משקל", "ערך למשקל"],
              [[str(i + 1), str(v), str(w), str(r)] for i, ((v, w), r) in enumerate(zip(ITEMS, R))], hidden_rows=False)
PCH = W.chips("pr", [str(v) for v in PROF], hidden=False, cls="small", label="רווחים:")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נשווה שתי גרסאות של בעיית התרמיל: השברית, וגרסת אפס-אחת."),
    P("נראה שאותו חמדן אופטימלי באחת ונכשל בשנייה, ונבין בדיוק למה."),
    P("ובסוף נפתור שאלה ממבחן עם מקרה מיוחד שבו חמדן כן עובד.", hold=0.4),
], stage='<div class="kicker">G06 · אלגוריתם חמדן והוכחת נכונות</div><h1>תרמיל שברי מול תרמיל 0/1</h1>'
         '<p>לדעת מתי חמדן לפי יחס ערך-משקל אופטימלי (שברי) ומתי הוא נכשל (0/1), ולזהות מקרים מיוחדים שבהם חמדן כן עובד.</p>',
   layout="title")

idea = Scene("idea", "שתי גרסאות", [
    P("בבעיית התרמיל יש פריטים עם ערך ומשקל, ותרמיל שמחזיק משקל מוגבל. רוצים כמה שיותר ערך."),
    P("בגרסה **השברית** מותר לקחת חלק מפריט. בגרסת **אפס-אחת** לוקחים פריט שלם, או לא לוקחים בכלל.",
      do=show("i-1", "i-2")),
    P("החמדן הטבעי: ממיינים לפי ערך ליחידת משקל, ולוקחים מהיחס הגבוה ביותר.", do=show("i-r")),
    P("בשברית הוא תמיד אופטימלי. באפס-אחת הוא יכול להיכשל, ושם פותרים בתכנות דינמי.", hold=0.4),
], stage='<div class="gp-stack"><div class="gp-steps">'
         '<div id="i-1" class="h"><span class="n">½</span><b>שברי:</b> מותר לקחת חלק מפריט. החמדן לפי יחס <b>אופטימלי</b></div>'
         '<div id="i-2" class="h"><span class="n">0/1</span><b>אפס-אחת:</b> פריט שלם או כלום. החמדן לפי יחס <b>נכשל</b></div>'
         '</div></div>',
   panel=st.card("i-r", "rule", "🔑 החמדן: מיון לפי $v_i / w_i$ בסדר יורד"))

frac = Scene("frac", "תרמיל שברי", [
    P("שלושה פריטים ותרמיל של 12 קילו. היחסים: 5, 4 ו-3 לקילו.", do=show("it")),
    P("לוקחים את הראשון כולו, 4 קילו. ואת השני כולו, 3 קילו. נשארו 5 קילו.", do=show("f-1")),
    P("מהשלישי לוקחים 5 מתוך 8 קילו, כלומר חמש שמיניות מהערך 24: זה 15.", do=show("f-2")),
    P("סך הכול 20 ועוד 12 ועוד 15: הערך 47.", do=show("f-3"), hold=0.3),
    P("ולמה זה אופטימלי? טיעון החלפה. ניקח פתרון אחר: רבע מהראשון, ואת השני והשלישי כולם. ערך 41.",
      do=show("f-4")),
    P("מעבירים 3 קילו מהשלישי, שנותן 3 לקילו, לראשון, שנותן 5 לקילו.", do=show("f-5")),
    P("המשקל לא השתנה, אז הפתרון עדיין חוקי. והערך עלה ב-3 כפול 5 פחות 3, כלומר ב-6.", do=show("f-6"),
      say="המשקל לא השתנה, אז הפתרון עדיין חוקי. והערך עלה בשלוש, כפול ההפרש בין חמש לשלוש, כלומר בשש."),
    P("באופן כללי, העברת דלתא קילו מיחס נמוך ליחס גבוה משנה את הערך בדלתא כפול הפרש היחסים. וזה אף פעם לא שלילי.",
      do=show("f-r")),
    P("לכן אפשר להזיז כל פתרון אופטימלי לעבר החמדן בלי להפסיד, והחמדן אופטימלי.", hold=0.4),
], stage=f'<div class="gp-stack"><div id="it" class="h">{TAB}</div>'
         '<div id="f-3" class="gp-mid h">$20 + 12 + 24 \\cdot \\frac{5}{8} = 47$</div>'
         '<div id="f-6" class="gp-mid h">$5 + 12 + 24 = 41 \\ \\to\\ 20 + 12 + 15 = 47$</div></div>',
   panel=st.card("f-1", "plain", "פריטים 1 ו-2 במלואם: משקל 7")
         + st.card("f-2", "plain", "פריט 3: $5$ מתוך $8$ קילו")
         + st.card("f-4", "ex", "פתרון אחר: $\\frac14$ מפריט 1, פריטים 2 ו-3 במלואם")
         + st.card("f-5", "ex", "מעבירים $\\delta = 3$ קילו מפריט 3 לפריט 1")
         + st.card("f-r", "rule", "🔑 שינוי הערך: $\\delta \\cdot (r_i - r_j) \\ge 0$"))

zo = Scene("zo", "תרמיל 0/1", [
    P("עכשיו אותם פריטים, אבל אסור לחתוך. החמדן לפי יחס לוקח את הראשון ואת השני: 7 קילו, ערך 32.", do=show("z-1")),
    P("השלישי שוקל 8, ונשארו רק 5. הוא לא נכנס, והחמדן נעצר על 32.", do=show("z-2")),
    P("אבל הראשון והשלישי יחד שוקלים בדיוק 12, ושווים 44. בדיקה של כל הצירופים מאשרת: 44 הוא המקסימום.",
      do=show("z-3")),
    P("למה ההחלפה נשברה? בשברית העברנו בדיוק 3 קילו. כאן אי אפשר להוציא חלק מפריט: או את כולו, או כלום.",
      do=show("z-t")),
    P("הפריט השני תפס 3 קילו והשאיר 5, מעט מדי לשלישי. הראשון והשלישי ממלאים בדיוק 12, ושווים 44.", hold=0.4),
], stage='<div class="gp-stack">'
         '<div id="z-1" class="gp-midr h">חמדן: $20 + 12 = 32$</div>'
         '<div id="z-2" class="gp-note h">נשארו 5 קילו, ופריט 3 שוקל 8</div>'
         '<div id="z-3" class="gp-midr h">אופטימום: $20 + 24 = 44$, משקל $4 + 8 = 12$</div></div>',
   panel=st.card("z-t", "trap", "⚠️ ב-0/1 אי אפשר להעביר $\\delta$ שרירותי, ולכן ההחלפה נשברת"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: משימות עם זמן ביצוע ורווח, וזמן כולל $T$. כל משימה פעם אחת לכל היותר. זה תרמיל אפס-אחת.",
      say="שאלה ממבחן: משימות עם זמן ביצוע ורווח, וזמן כולל טִי. כל משימה פעם אחת לכל היותר. זה תרמיל אפס-אחת."),
    P("סעיף ראשון: דוגמה נגדית לחמדן לפי רווח ליחידת זמן. מספיקות שתי משימות.", do=show("q-1")),
    P("זמן כולל 10. משימה קצרה, 2 שעות ורווח 6: יחס 3. ומשימה ארוכה, 10 שעות ורווח 20: יחס 2.", do=show("x-1")),
    P("החמדן לוקח את הקצרה, ונשארות 8 שעות. הארוכה כבר לא נכנסת, והרווח 6. אבל לבד, הארוכה נותנת 20.",
      do=show("x-2")),
    P("זו דוגמה מלאה: שני מספרים, 6 מול 20, ושתי הבחירות חוקיות.", hold=0.3),
    P("סעיף שני: לכל המשימות אותו זמן $t$. אז קבוצה חוקית אם ורק אם יש בה לכל היותר $k$ משימות.",
      do=show("q-2", "x-3"),
      say="סעיף שני: לכל המשימות אותו זמן טִי. אז קבוצה חוקית אם ורק אם יש בה לכל היותר קֵיי משימות."),
    P("כאשר $k$ הוא $T$ חלקי $t$, מעוגל למטה. והאלגוריתם: לוקחים את $k$ המשימות עם הרווח הגדול ביותר.",
      say="כאשר קֵיי הוא טִי חלקי טִי קטנה, מעוגל למטה. והאלגוריתם: לוקחים את קֵיי המשימות עם הרווח הגדול ביותר."),
    P("למשל זמן 4 לכל משימה, וזמן כולל 13: נכנסות שלוש משימות, כי ארבע כבר דורשות 16.", do=show("pr")),
    P("הרווחים 7, 3, 10, 6, 8 ו-2. לוקחים 10, 8 ו-7: רווח 25, וחיפוש מלא מאשר שזה המקסימום.",
      do=show("pr-2-ok", "pr-4-ok", "pr-0-ok")),
    P("סעיף שלישי, ההוכחה. נניח שהרווחים חיוביים, ויהי $O$ אופטימלי עם הכי הרבה משימות משותפות לחמדן.",
      do=show("q-3"), say="סעיף שלישי, ההוכחה. נניח שהרווחים חיוביים, ויהי אוֹ אופטימלי עם הכי הרבה משימות משותפות לחמדן."),
    P("אם יש ב-$O$ משימה שהחמדן לא לקח, אז החמדן כבר לקח $k$ משימות, וכל אחת מהן רווחית לפחות כמוה.",
      say="אם יש באוֹ משימה שהחמדן לא לקח, אז החמדן כבר לקח קֵיי משימות, וכל אחת מהן רווחית לפחות כמוה."),
    P("ב-$O$ יש לכל היותר $k$ משימות, אז יש משימה של החמדן שלא ב-$O$. מחליפים ביניהן.", do=show("x-4"),
      say="באוֹ יש לכל היותר קֵיי משימות, אז יש משימה של החמדן שלא באוֹ. מחליפים ביניהן."),
    P("אותו מספר משימות, אז חוקי. הרווח לא ירד, ויש יותר משותפות לחמדן: סתירה לבחירה.",
      say="אותו מספר משימות, אז חוקי. הרווח לא ירד, ויש יותר משותפות לחמדן: סתירה לבחירה."),
    P("ואם אין משימה כזאת, אז $O$ חלק מהחמדן. אם הוא חלק ממש, מוסיפים משימה רווחית וחורגים מהאופטימום. סתירה.",
      say="ואם אין משימה כזאת, אז אוֹ חלק מהחמדן. אם הוא חלק ממש, מוסיפים משימה רווחית וחורגים מהאופטימום. סתירה."),
    P("והזמן: מיון לפי רווח, $O(n\\,\\log\\,n)$, ועוד מעבר אחד.", do=show("x-5"),
      say="והזמן: מיון לפי רווח, או של אֶן לוֹג אֶן, ועוד מעבר אחד.", hold=0.5),
], stage='<div class="gp-stack">'
         '<div id="x-1" class="gp-mid h">$T = 10:\\ \\ (t=2,\\ v=6),\\ \\ (t=10,\\ v=20)$</div>'
         '<div id="x-2" class="gp-midr h">חמדן: $6$ &nbsp;&nbsp; אופטימום: $20$</div>'
         '<div id="x-3" class="gp-mid h">$k = \\lfloor T / t \\rfloor = \\lfloor 13 / 4 \\rfloor = 3$</div>'
         f'<div id="pr" class="h">{PCH}</div>'
         '<div id="x-4" class="gp-mid h">$O\' = (O \\setminus \\{j\\}) \\cup \\{i\\},\\ \\ v_i \\ge v_j$</div></div>',
   panel='<div class="qstem"><span class="qid">26B-A-Q2a/b/c</span>$n$ משימות עם זמן $t_i$ ורווח $v_i$, וזמן כולל $T$.</div>'
         + st.card("q-1", "plain", "(א) דוגמה נגדית לחמדן לפי $v / t$")
         + st.card("q-2", "plain", "(ב) כל הזמנים שווים $t$: אלגוריתם חמדני")
         + st.card("q-3", "plain", "(ג) הוכחה וסיבוכיות")
         + st.card("x-5", "rule", "🔑 $k$ הרווחים הגדולים; $O(n\\,\\log\\,n)$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בתרמיל שברי, החמדן לפי יחס אופטימלי, כי מעבירים משקל מיחס נמוך לגבוה בלי להפסיד.", do=show("r-1")),
    P("באפס-אחת אי אפשר לחתוך פריט, ולכן ההחלפה נשברת והחמדן נכשל.", do=show("r-2")),
    P("ובמקרים מיוחדים, כמו זמן זהה לכל המשימות, חמדן פשוט כן נכון. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage='<div class="gp-stack"><div class="gp-big">$\\delta \\cdot (r_i - r_j) \\ge 0$</div></div>',
   panel=st.card("r-1", "rule", "🔑 שברי: חמדן לפי $v/w$ אופטימלי")
         + st.card("r-2", "trap", "⚠️ 0/1: החמדן לפי יחס נכשל")
         + st.card("r-3", "rule", "🔑 זמן זהה: $k = \\lfloor T/t \\rfloor$ הרווחים הגדולים"))

VIDEO = Video("G06", "greedy_proofs", "תרמיל שברי מול תרמיל 0/1", [title, idea, frac, zo, exam, recap],
              bank={"26B-A-Q2a": None, "26B-A-Q2b": None, "26B-A-Q2c": None})
