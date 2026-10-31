# -*- coding: utf-8 -*-
"""D01 · מגדירים תת-בעיה במילים — video script (build: tools/video/vid.py D01).

Source: courses/dp_ladder/C01.js (lesson + goal). Exam anchor: 24A-C-Q4a (minimum jumps to the end of an array, open
question): define the function in words, give the recurrence, say where the answer is. No guided quiz uses it.
Not used on purpose: the C01 quiz (LCS definition, grid paths, squares N=30, palindrome prefix, L(n,m)) and the bank
questions of the boss C09 and of the other levels (22A-B-Q1, 22B-A-Q4a/c, 25A-A-Q2a/c, 25A-C-Q1a/b, 25B-A-Q4a). The
LIS example is an original one (the boss 25B-A-Q4a has the same "ends at A[i]" idea on divisible subsets; its own
numbers and wording are not shown).
Every value on screen is computed by w_dp_ladder and compared with a brute force below.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_dp_ladder as w

# ---------------------------------------------------------------- data (verified)
A = [2, 7, 9, 3, 1]                                   # scene "rob": no two neighbours, maximum sum
R = w.robber(A)
assert R == [w.robber_bf(A, i) for i in range(len(A) + 1)] == [0, 2, 7, 11, 11, 12]

# scene "lis": the prefix value alone does not decide the next value
assert w.lis_prefix_bf([1, 9], 1) == w.lis_prefix_bf([1, 3], 1) == 2
assert w.lis_prefix_bf([1, 9, 5], 2) == 2 and w.lis_prefix_bf([1, 3, 5], 2) == 3
B = [1, 9, 3, 5, 2]
E = w.lis_end(B)
assert E == [w.lis_end_bf(B, i) for i in range(len(B))] == [1, 2, 2, 3, 2]
assert max(E) == 3 == w.lis_prefix_bf(B, len(B) - 1) and E[-1] == 2      # the answer is the max, not E(n)

# exam 24A-C-Q4a
Q = BANK["24A-C-Q4a"]
assert "קפיצות" in Q["question"] and Q.get("correctId") is None
J = [1, 4, 6, 4, 5, 3, 3, 2, 1, 3]
n = len(J)
C = w.jumps_to_end(J)                                  # C(i): from i to the end
Dst = w.jumps_from_start(J)                            # D(i): from the start to i
assert [C[i] for i in range(1, n + 1)] == [w.jumps_bf(J, i, n) for i in range(1, n + 1)]
assert [Dst[i] for i in range(1, n + 1)] == [w.jumps_bf(J, 1, i) for i in range(1, n + 1)]
assert C[1] == Dst[n] == 3 and C[1:] == [3, 2, 2, 2, 1, 2, 1, 1, 1, 0]
assert C[5] == 1 and 5 + J[4] >= n and C[2] == 1 + C[5] and 2 + J[1] >= 5 and 1 + J[0] == 2   # path 1 -> 2 -> 5 -> 10
# the trap: always jumping as far as possible takes 4 jumps here
pos, far, gpath = 1, 0, [1]
while pos < n:
    pos, far = min(n, pos + J[pos - 1]), far + 1
    gpath.append(pos)
assert far == 4 and gpath == [1, 2, 6, 9, 10]
# the narration of the fill: 7, 8, 9 reach the end directly, 6 does not; 2, 3, 4 reach 5 but not the end
assert all(i + J[i - 1] >= n for i in (7, 8, 9)) and 6 + J[5] < n and C[6] == 2
assert all(i + J[i - 1] >= 5 and i + J[i - 1] < n and C[i] == 2 for i in (2, 3, 4))

# ---------------------------------------------------------------- widgets
GR = w.Grid("gr", ["A", "R"], ["0"] + [str(i) for i in range(1, 6)],
            {**{(0, i): str(A[i - 1]) for i in range(1, 6)}, **{(1, i): str(R[i]) for i in range(6)}},
            given={(0, i) for i in range(1, 6)}, void={(0, 0)}, cw=96, ch=70, fs=36)
GL = w.Grid("gl", ["A", "E"], [str(i) for i in range(1, 6)],
            {**{(0, i): str(B[i]) for i in range(5)}, **{(1, i): str(E[i]) for i in range(5)}},
            given={(0, i) for i in range(5)}, cw=96, ch=70, fs=36)
GJ = w.Grid("gj", ["A", "C"], [str(i) for i in range(1, n + 1)],
            {**{(0, i - 1): str(J[i - 1]) for i in range(1, n + 1)}, **{(1, i - 1): str(C[i]) for i in range(1, n + 1)}},
            given={(0, i) for i in range(n)}, cw=80, ch=66, fs=32)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד את השלב הראשון בכל פתרון בתכנות דינמי: להגדיר את תת-הבעיה במילים."),
    P("נראה מה הגדרה טובה חייבת להגיד, ונראה הגדרה שנראית טובה ונכשלת."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">D01 · תכנות דינמי</div><h1>מגדירים תת-בעיה במילים</h1>'
         '<p>מה הפונקציה מחזירה, מה כל פרמטר מציין, ואיפה נמצאת התשובה לבעיה המלאה.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("פתרון נאיבי עובר על כל האפשרויות, ולפעמים יש אקספוננציאלית הרבה כאלה.", do=show("i-1")),
    P("תכנות דינמי פותר במקום זה תת-בעיות קטנות. כל אחת נפתרת פעם אחת, ונשמרת בטבלה.", do=show("i-2")),
    P("אבל לפני כל נוסחה צריך משפט אחד, שאומר שלושה דברים.", do=show("i-3")),
    P("ראשון: **מה** הפונקציה מחזירה. מספר, אורך, אמת או שקר.", do=show("i-a")),
    P("שני: **על איזה חלק** של הקלט. מה כל פרמטר מציין.", do=show("i-b")),
    P("ושלישי: **איפה התשובה** לבעיה המלאה, באיזה תא של הטבלה.", do=show("i-c"), hold=0.4),
    P("במבחן ההגדרה מקבלת ניקוד משלה. נוסחה בלי הגדרה נחשבת נוסחה לא מוגדרת.", do=show("i-r")),
], stage='<div class="dl-stack">'
         + st.card("i-1", "plain", "נאיבי: כל $2^n$ תתי-הקבוצות")
         + st.card("i-2", "ex", "תכנות דינמי: כל תת-בעיה פעם אחת, בטבלה")
         + st.card("i-3", "plain", "<b>ההגדרה במילים</b> אומרת שלושה דברים:")
         + "</div>",
   panel=st.card("i-a", "rule", "1. <b>מה</b> מוחזר: מספר, אורך, אמת/שקר")
         + st.card("i-b", "rule", "2. <b>על איזה חלק</b> של הקלט: מה כל פרמטר")
         + st.card("i-c", "rule", "3. <b>איפה התשובה</b>: באיזה תא")
         + st.card("i-r", "trap", "⚠️ נוסחה בלי הגדרה = לא מוגדרת"))

rob_ph = [
    P("דוגמה ראשונה. נתון מערך מספרים, ובוחרים מתוכו איברים בלי לבחור שני שכנים.", do=show("r-g")),
    P("רוצים את הסכום המקסימלי של איברים כאלה.", do=show("r-q")),
    P("ההגדרה: $R(i)$ הוא הסכום המקסימלי של איברים לא שכנים מתוך הרישא $A[1..i]$.", do=show("r-d"),
      say="ההגדרה: אָר שֶל אַיי הוא הסכום המקסימלי של איברים לא שכנים, מתוך הרישא של אֵיי עד המקום אַיי."),
    P("יש בה את שלושת הדברים: מה מוחזר, סכום מקסימלי. על איזה חלק, הרישא עד $i$.",
      say="יש בה את שלושת הדברים: מה מוחזר, סכום מקסימלי. על איזה חלק, הרישא עד המקום אַיי."),
    P("ואיפה התשובה: $R(n)$, כי הרישא באורך $n$ היא המערך כולו.", do=show("r-ans"),
      say="ואיפה התשובה: אָר שֶל אֶן, כי הרישא באורך אֶן היא המערך כולו."),
    P("רישא ריקה נותנת סכום 0. רישא של איבר אחד נותנת 2.", do=GR.step((1, 0)) + GR.step((1, 1))),
    P("עם שלושה איברים: 2 ועוד 9, כלומר 11. את 7 אי אפשר לקחת יחד עם אף אחד מהם.", do=GR.vals_do([(1, 2)]) + GR.step((1, 3))),
    P("ועם כל החמישה: 2 ועוד 9 ועוד 1, כלומר 12. זו התשובה.", do=GR.vals_do([(1, 4)]) + GR.step((1, 5))),
    P("ושימו לב למשפט שנראה כמו הגדרה: \"$R(i)$ הוא הפתרון\".", do=GR.off() + show("r-t"),
      say="ושימו לב למשפט שנראה כמו הגדרה: אָר שֶל אַיי הוא הפתרון."),
    P("הוא לא אומר על איזו רישא מדובר, וגם לא אם מוחזר סכום או רשימת איברים.", hold=0.4),
]
rob = Scene("rob", "דוגמה: בלי שכנים", rob_ph,
            stage=f'<div class="dl-stack"><div id="r-g" class="h">{GR.html()}</div>'
                  + st.card("r-d", "ex", "$R(i)$ = הסכום המקסימלי של איברים לא שכנים מתוך $A[1..i]$")
                  + "</div>",
            panel=st.card("r-q", "plain", "בוחרים איברים, <b>אף שניים לא שכנים</b>, וסכומם מקסימלי.")
                  + st.card("r-ans", "rule", "🔑 התשובה: $R(n)$")
                  + st.card("r-t", "trap", "⚠️ \"$R(i)$ הוא הפתרון\": איזו רישא? סכום או רשימה?"))

lis_ph = [
    P("דוגמה שנייה, ובה הגדרה שנראית טובה ונכשלת: תת-סדרה עולה ארוכה ביותר.", do=show("l-q")),
    P("ננסה להגדיר לפי רישא: האורך של תת-הסדרה העולה הארוכה ביותר ברישא $A[1..i]$.", do=show("l-bad"),
      say="ננסה להגדיר לפי רישא: האורך של תת הסדרה העולה הארוכה ביותר, ברישא עד המקום אַיי."),
    P("לרישא 1, 9 ולרישא 1, 3 יש אותו ערך: 2.", do=show("l-x1")),
    P("עכשיו מוסיפים לשתיהן 5. בראשונה הערך נשאר 2, ובשנייה הוא עולה ל-3.", do=show("l-x2")),
    P("אותו ערך קודם, אותו איבר חדש, ותוצאה שונה. אז מהערך הקודם לבד אי אפשר לחשב את הבא.", do=show("l-x3"), hold=0.3),
    P("מה חסר? לדעת **במה** תת-הסדרה נגמרת. לכן מגדירים אחרת.", do=show("l-g")),
    P("$E(i)$ הוא האורך של תת-הסדרה העולה הארוכה ביותר ש**מסתיימת בדיוק** ב-$A[i]$.", do=show("l-def"),
      say="אִי שֶל אַיי הוא האורך של תת הסדרה העולה הארוכה ביותר, שמסתיימת בדיוק באֵיי במקום אַיי."),
    P("עכשיו יודעים את האיבר האחרון, ואפשר לבדוק אם האיבר החדש גדול ממנו.", do=GL.step((1, 0)) + GL.vals_do([(1, 1), (1, 2)])),
    P("למשל 5 בא אחרי 3, ולכן $E(4)$ הוא 3: הסדרה 1, 3, 5.", do=GL.step((1, 3), [(1, 2)]),
      say="למשל חמש בא אחרי שלוש, ולכן אִי של ארבע הוא שלוש: הסדרה אחת, שלוש, חמש."),
    P("והאיבר האחרון, 2, מקבל רק 2.", do=GL.step((1, 4), [(1, 0)])),
    P("לכן התשובה כאן **איננה** $E(n)$, אלא המקסימום על כל המקומות: 3.", do=GL.off() + show("l-ans"),
      say="לכן התשובה כאן איננה אִי שֶל אֶן, אלא המקסימום על כל המקומות: שלוש."),
]
lis = Scene("lis", "הגדרה שנכשלת", lis_ph,
            stage='<div class="dl-stack">'
                  + st.card("l-bad", "plain", "ניסיון: האורך הכי ארוך ברישא $A[1..i]$")
                  + '<div class="dl-row">'
                  + st.card("l-x1", "ex", "$1,9 \\to 2$ &nbsp; $1,3 \\to 2$")
                  + st.card("l-x2", "ex", "$1,9,5 \\to 2$ &nbsp; $1,3,5 \\to 3$")
                  + "</div>"
                  + st.card("l-x3", "trap", "⚠️ אותו ערך קודם, אותו איבר חדש, תוצאה שונה")
                  + f'<div id="l-g" class="h">{GL.html()}</div></div>',
            panel=st.card("l-q", "plain", "תת-סדרה <b>עולה</b> ארוכה ביותר של $A$")
                  + st.card("l-def", "rule", "🔑 $E(i)$ = אורך העולה הארוכה ביותר ש<b>מסתיימת ב-</b>$A[i]$")
                  + st.card("l-ans", "trap", "⚠️ התשובה: $\\max_i E(i)$, לא $E(n)$"))

ex_ph = [
    P("ועכשיו שאלה ממבחן. במערך, כל איבר אומר כמה צעדים לכל היותר אפשר לקפוץ קדימה ממנו.", do=show("x-g")),
    P("מתחילים במקום הראשון, ורוצים להגיע למקום האחרון במספר מינימלי של קפיצות."),
    P("השאלה מבקשת להגדיר במילים את הפונקציה, לתת נוסחה, ולנמק."),
    P("יש שתי הגדרות נכונות, וההבדל ביניהן הוא בדיוק מה שהמשפט צריך להגיד.", do=show("x-d1")),
    P("הראשונה: $C(i)$ הוא מספר הקפיצות המינימלי **מהמקום $i$ עד הסוף**. התשובה היא $C(1)$.",
      say="הראשונה: סִי שֶל אַיי הוא מספר הקפיצות המינימלי מהמקום אַיי עד הסוף. התשובה היא סִי של אחת."),
    P("השנייה: $D(i)$ הוא המינימום **מההתחלה עד המקום $i$**. ואז התשובה היא $D(n)$.", do=show("x-d2"),
      say="השנייה: דִּי שֶל אַיי הוא המינימום מההתחלה עד המקום אַיי. ואז התשובה היא דִּי שֶל אֶן."),
    P("נמשיך עם הראשונה. הצעד הראשון מ-$i$ הוא קפיצה של $j$ צעדים, בין 1 לבין $A[i]$.", do=show("x-f"),
      say="נמשיך עם הראשונה. הצעד הראשון מאַיי הוא קפיצה של גֵ'יי צעדים, בין אחת לבין אֵיי במקום אַיי."),
    P("משם צריך להגיע לסוף במינימום קפיצות, אחרת היינו מחליפים את ההמשך בטוב יותר.",),
    P("ולכן הנוסחה: אחת ועוד המינימום של $C(i+j)$, בלי לקפוץ מעבר למקום $n$. והבסיס: $C(n)$ הוא 0.",
      say="ולכן הנוסחה: אחת ועוד המינימום של סִי של, בסוגריים, אַיי ועוד גֵ'יי, בלי לקפוץ מעבר למקום אֶן. והבסיס: סִי של אֶן הוא אפס."),
    P("ההגדרה קובעת גם את סדר המילוי: מהסוף להתחלה.", do=GJ.step((1, 9))),
    P("מהמקום 9 קופצים ישר לסוף, וגם מ-8 ומ-7. מהמקום 6 צריך כבר שתי קפיצות.",
      do=GJ.vals_do([(1, 8), (1, 7), (1, 6)]) + GJ.step((1, 5), [(1, 6), (1, 7), (1, 8)])),
    P("מהמקום 5 קופצים עד 5 צעדים, כלומר ישר לסוף: קפיצה אחת.", do=GJ.step((1, 4), [(1, 9)])),
    P("מ-4, מ-3 ומ-2 מגיעים ל-5 בקפיצה אחת, ולכן לכל אחד מהם 2.",
      do=GJ.vals_do([(1, 3), (1, 2)]) + GJ.step((1, 1), [(1, 4)])),
    P("ומהמקום הראשון יש רק קפיצה אחת, אל 2. לכן $C(1)$ הוא 3: אחת, שתיים, חמש, עשר.",
      do=GJ.step((1, 0), [(1, 1)]) + show("x-ok") + GJ.path([(1, 0), (1, 1), (1, 4), (1, 9)]),
      say="ומהמקום הראשון יש רק קפיצה אחת, אל שתיים. לכן סִי של אחת הוא שלוש: אחת, שתיים, חמש, עשר."),
    P("והמלכודת: לקפוץ תמיד הכי רחוק. כאן זה נותן ארבע קפיצות, ולא שלוש.", do=GJ.off() + show("x-t"), hold=0.5),
]
exam = Scene("exam", "שאלה ממבחן", ex_ph,
             stage='<div class="dl-stack">'
                   + f'<div id="x-g" class="h">{GJ.html()}</div>'
                   + w.eqs("x-f", ["$C(i)=1+\\min_{1\\le j\\le \\min(A[i],\\,n-i)} C(i+j),\\qquad C(n)=0$"], 36)
                   .replace('id="x-f-0"', 'id="x-f"')
                   + st.card("x-ok", "rule", "🔑 התשובה: $C(1)=3$, המסלול $1\\to2\\to5\\to10$")
                   + "</div>",
             panel=f'<div class="dl-q"><span class="qid">{Q["id"]}</span>מערך $A$: מכל מקום $i$ אפשר לקפוץ עד '
                   '$A[i]$ צעדים קדימה. מינימום קפיצות מהמקום 1 עד המקום $n$. הגדירו במילים, תנו נוסחה ונמקו.</div>'
                   + st.card("x-d1", "ex", "$C(i)$: מינימום קפיצות <b>מ-$i$ עד הסוף</b>. התשובה $C(1)$")
                   + st.card("x-d2", "ex", "$D(i)$: מינימום <b>מההתחלה עד $i$</b>. התשובה $D(n)$")
                   + st.card("x-t", "trap", "⚠️ תמיד הכי רחוק: $1\\to2\\to6\\to9\\to10$, ארבע קפיצות"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: לפני כל נוסחה כותבים משפט אחד.", do=show("s-1")),
    P("מה מוחזר, על איזה חלק של הקלט, ואיפה התשובה.", do=show("s-2")),
    P("ובלי המשפט הזה, הנוסחה נחשבת לא מוגדרת. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage='<div class="dl-stack">'
         + st.card("s-1", "rule", "🔑 משפט אחד לפני כל נוסחה")
         + st.card("s-2", "rule", "🔑 מה מוחזר · על איזה חלק · איפה התשובה")
         + "</div>",
   panel=st.card("s-3", "trap", "⚠️ נוסחה בלי הגדרה = לא מוגדרת"))

VIDEO = Video("D01", "dp_ladder", "מגדירים תת-בעיה במילים", [title, idea, rob, lis, exam, recap],
              bank={"24A-C-Q4a": None})
