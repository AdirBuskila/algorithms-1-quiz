# -*- coding: utf-8 -*-
"""D09 · מבחן גמר: תכנות דינמי — boss walkthrough (build: tools/video/vid.py D09).

Source: courses/dp_ladder/C09.js (boss level: definition, recurrence and base cases, table and run, complexity).
Three exam questions that no guided quiz or boss uses, each solved on screen with its trap:
  22B-B-Q4a (+ its run 22B-B-Q4c): minimum removals from a sorted array so that max - min <= k (interval table).
      The solution file's table has two misprinted cells (noted in the bank); the table shown is computed.
  24B-B-Q3a: restaurants along a road at least k km apart, maximum profit (prev(i), not i - k). The example data
      (d = 1,3,5,8,10, p = 4,6,5,7,3, k = 4) is original: the question gives none.
  26A-A-Q1b: minimum time of tasks when two consecutive tasks may not both be skipped (T(i) ends with task i, the
      answer is min(T(n-1), T(n-2))), run on the question's own second example.
Not used on purpose: the six boss questions of C09 (22A-B-Q1, 22B-A-Q4a, 25A-A-Q2a, 25A-C-Q1a, 25B-A-Q4a,
25A-C-Q1b) and every quiz item of C01..C08. Every value is computed by w_dp_ladder and compared with a brute force.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_dp_ladder as w

# ---------------------------------------------------------------- data (verified)
Q1a, Q1c = BANK["22B-B-Q4a"], BANK["22B-B-Q4c"]
assert "להסיר" in Q1a["question"] and "k=2" in Q1c["question"].replace(" ", "")
A1, K1 = [1, 3, 4, 9, 10, 12, 17, 20], 4
assert w.removal(A1, K1)[0, 7] == w.removal_bf(A1, K1) == 5                 # the example of the question
A2, K2 = [1, 2, 5, 6, 8], 2
R2 = w.removal(A2, K2)
assert R2[0, 4] == w.removal_bf(A2, K2) == 3
assert all(R2[i, j] == w.removal_bf(A2[i:j + 1], K2) for i in range(5) for j in range(i, 5))
assert R2[0, 4] == 1 + min(R2[1, 4], R2[0, 3]) and R2[1, 4] == R2[0, 3] == 2
assert R2[1, 3] == 1 and A2[3] - A2[1] == 4 > K2 and R2[3, 4] == 0 and A2[4] - A2[3] == 2
B3, K3 = [1, 2, 3, 10], 2
CB = w.removal(B3, K3)
assert CB[0, 3] == 1 and 2 + CB[1, 2] == 2 and w.removal_bf(B3, K3) == 1

Q2 = BANK["24B-B-Q3a"]
assert "מסעדה" in Q2["question"] or "רווח" in Q2["question"]
d, p, k = [1, 3, 5, 8, 10], [4, 6, 5, 7, 3], 4
O, prev = w.restaurants(d, p, k)
best, arg = w.restaurants_bf(d, p, k)
assert O == [0, 4, 6, 9, 13, 13] and prev == [0, 0, 0, 1, 2, 3]
assert all(O[i] == w.restaurants_bf(d, p, k, i)[0] for i in range(6))
assert O[5] == best == 13 and arg == (1, 3)                                  # restaurants at 3 km and 8 km
assert O[4] == max(O[3], p[3] + O[prev[4]]) == p[3] + O[2] == 13
assert d[3] - d[1] >= k and d[3] - d[2] < k                                  # prev(4) = 2: 8-3 >= 4, 8-5 < 4
assert 4 - k == 0 and p[3] + O[0] == 7 != 13                                 # i - k as an index would give 7

Q3 = BANK["26A-A-Q1b"]
assert "רקורסיבית" in Q3["question"] and Q3.get("correctId") is None
A3 = [10, 5, 2, 4, 8, 6, 7, 10]
T3, ans3 = w.tasks(A3)
assert ans3 == w.tasks_bf(A3) == 22 and [T3[i] for i in range(8)] == [10, 5, 7, 9, 15, 15, 22, 25]
assert T3[6] == A3[6] + min(T3[5], T3[4]) and ans3 == min(T3[7], T3[6])
assert w.tasks([10, 5, 7, 10])[1] == w.tasks_bf([10, 5, 7, 10]) == 12 and w.tasks([10])[1] == 0
assert T3[7] == 25 != 22                                                     # T(n-1) alone is not the answer
for Q in (Q1a, Q1c, Q2, Q3):
    assert Q.get("correctId") is None

# ---------------------------------------------------------------- widgets
GR = w.Grid("gr", [str(a) for a in A2], [str(a) for a in A2],
            {(i, j): str(R2[i, j]) for i in range(5) for j in range(i, 5)},
            given={(i, i) for i in range(5)}, void={(i, j) for i in range(5) for j in range(i)},
            cw=88, ch=66, fs=32)
GS = w.Grid("gs", ["d", "p", "prev", "OPT"], ["0", "1", "2", "3", "4", "5"],
            {**{(0, i): str(d[i - 1]) for i in range(1, 6)}, **{(1, i): str(p[i - 1]) for i in range(1, 6)},
             **{(2, i): str(prev[i]) for i in range(1, 6)}, **{(3, i): str(O[i]) for i in range(6)}},
            given={(r, i) for r in (0, 1) for i in range(1, 6)}, void={(0, 0), (1, 0), (2, 0)},
            cw=88, ch=62, fs=30, hw=110)
GT = w.Grid("gt", ["A", "T"], [str(i) for i in range(8)],
            {**{(0, i): str(A3[i]) for i in range(8)}, **{(1, i): str(T3[i]) for i in range(8)}},
            given={(0, i) for i in range(8)}, cw=84, ch=66, fs=32)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה מבחן הגמר של הקורס: שלוש שאלות אמיתיות ממבחנים, כל אחת עם הסולם המלא."),
    P("הגדרה במילים, נוסחה ומקרי בסיס, טבלה והרצה. ובכל אחת, המלכודת שלה.", hold=0.4),
], stage='<div class="kicker">D09 · תכנות דינמי</div><h1>מבחן גמר: תכנות דינמי</h1>'
         '<p>שלוש שאלות ממבחנים: קטע במערך, מסעדות לאורך כביש, ומשימות בלי שני דילוגים.</p>', layout="title")

q1_ph = [
    P("שאלה ראשונה. מערך ממוין ומספר $k$. מה המספר המינימלי של איברים שצריך להסיר,",
      say="שאלה ראשונה. מערך ממוין ומספר קֵיי. מה המספר המינימלי של איברים שצריך להסיר,"),
    P("כדי שההפרש בין הגדול לקטן שנשארו יהיה לכל היותר $k$?",
      say="כדי שההפרש בין הגדול לקטן שנשארו יהיה לכל היותר קֵיי?"),
    P("ההגדרה: $C(i,j)$ הוא מספר ההסרות המינימלי מהקטע $A[i..j]$. התשובה: $C(1,n)$.", do=show("a-d"),
      say="ההגדרה: סִי שֶל אַיי וגֵ'יי הוא מספר ההסרות המינימלי מהקטע שבין אַיי לגֵ'יי. התשובה: סִי של אחת ואֶן."),
    P("המערך ממוין, ולכן ההפרש של הקטע הוא הקצה הימני פחות הקצה השמאלי. אם הוא לכל היותר $k$, לא מסירים כלום.",
      do=show("a-0"),
      say="המערך ממוין, ולכן ההפרש של הקטע הוא הקצה הימני פחות הקצה השמאלי. אם הוא לכל היותר קֵיי, לא מסירים כלום."),
    P("אחרת, אם שני הקצוות נשארים, ההפרש גדול מדי. אז חייבים להסיר את אחד הקצוות.", do=show("a-f")),
    P("לכן אחת ועוד המינימום של שני הקטעים הקצרים יותר. וזו טבלה של קטעים: ממלאים לפי אורך הקטע.",
      do=show("a-g")),
    P("נריץ על 1, 2, 5, 6, 8 עם $k$ שווה 2. בקטע מ-2 עד 6 ההפרש 4, ולכן מסירים אחד.",
      do=GR.vals_do([(i, i + 1) for i in range(4)]) + GR.step((1, 3), [(2, 3), (1, 2)]),
      say="נריץ על אחת, שתיים, חמש, שש ושמונה, עם קֵיי שווה שתיים. בקטע משתיים עד שש ההפרש ארבע, ולכן מסירים אחד."),
    P("וכך עד הקטע המלא: אחת ועוד המינימום של 2 ו-2, כלומר 3. למשל להסיר 1, 2 ו-8.",
      do=GR.vals_do([(0, 2), (2, 4), (0, 3), (1, 4)]) + GR.step((0, 4), [(1, 4), (0, 3)]) + show("a-ok")),
    P("המלכודת: להסיר את שני הקצוות בבת אחת. במערך 1, 2, 3, 10 זה נותן 2, ומספיק להסיר רק את 10.",
      do=GR.off() + show("a-t"), hold=0.5),
]
q1 = Scene("q1", "שאלה 1: קטע במערך", q1_ph,
           stage='<div class="dl-stack">'
                 + w.eqs("a", ["$C(i,j)=0\\quad (A[j]-A[i]\\le k)$",
                               "$C(i,j)=1+\\min\\bigl(C(i+1,j),\\ C(i,j-1)\\bigr)\\quad (A[j]-A[i]>k)$"], 32)
                 .replace('id="a-0"', 'id="a-0x"').replace('id="a-1"', 'id="a-f"').replace('id="a-0x"', 'id="a-0"')
                 + f'<div id="a-g" class="h">{GR.html()}</div>'
                 + "</div>",
           panel=f'<div class="dl-q"><span class="qid">{Q1a["id"]} · {Q1c["id"]}</span>מערך ממוין $A$ ומספר $k$: '
                 'מינימום הסרות כך שהגדול פחות הקטן יהיה לכל היותר $k$.</div>'
                 + st.card("a-d", "ex", "$C(i,j)$: מינימום הסרות מ-$A[i..j]$. התשובה $C(1,n)$")
                 + st.card("a-ok", "rule", "🔑 $C(1,n)=3$ עבור $1,2,5,6,8$, $k=2$")
                 + st.card("a-t", "trap", "⚠️ לא להסיר את שני הקצוות יחד: $1,2,3,10$ צריך רק הסרה אחת"))

q2_ph = [
    P("שאלה שנייה. מקומות לאורך כביש, במרחקים עולים $d_i$. במקום $i$ אפשר לפתוח מסעדה ברווח $p_i$.",
      say="שאלה שנייה. מקומות לאורך כביש, במרחקים עולים. בכל מקום אפשר לפתוח מסעדה, ולכל מקום יש רווח."),
    P("כל שתי מסעדות צריכות להיות במרחק $k$ קילומטר לפחות. רוצים רווח מקסימלי.",
      say="כל שתי מסעדות צריכות להיות במרחק קֵיי קילומטר לפחות. רוצים רווח מקסימלי."),
    P("ההגדרה: $OPT(i)$ הוא הרווח המקסימלי כשמותר לפתוח רק במקומות 1 עד $i$. התשובה: $OPT(n)$.", do=show("b-d"),
      say="ההגדרה: אוֹפְּט שֶל אַיי הוא הרווח המקסימלי כשמותר לפתוח רק במקומות אחת עד אַיי. התשובה: אוֹפְּט של אֶן."),
    P("ההחלטה האחרונה: לפתוח במקום $i$ או לא. אם לא, זה $OPT(i-1)$.", do=show("b-f"),
      say="ההחלטה האחרונה: לפתוח במקום אַיי או לא. אם לא, זה אוֹפְּט של, בסוגריים, אַיי פחות אחת."),
    P("ואם כן, מותר להשאיר רק מקומות רחוקים לפחות $k$. מגדירים $prev(i)$: המקום האחרון שרחוק מספיק.",
      do=show("b-p"),
      say="ואם כן, מותר להשאיר רק מקומות רחוקים לפחות קֵיי. מגדירים את פְּרֶב שֶל אַיי: המקום האחרון שרחוק מספיק."),
    P("כי המקומות ממוינים: כל מה שלפניו רחוק מספיק, וכל מה שאחריו קרוב מדי.", do=show("b-g")),
    P("נריץ עם $k$ שווה 4. המקום הרביעי, ב-8 קילומטר: המקום 3 ב-5 קרוב מדי, והמקום 2 ב-3 רחוק מספיק.",
      do=GS.vals_do([(2, i) for i in range(1, 6)] + [(3, i) for i in range(4)]) + GS.step((2, 4), [(0, 2), (0, 3)], value=False),
      say="נריץ עם קֵיי שווה ארבע. המקום הרביעי, בשמונה קילומטר: המקום השלישי, בחמש, קרוב מדי, והמקום השני, בשלוש, רחוק מספיק."),
    P("לכן המקסימום של 9, בלי המקום, ושל 7 ועוד 6, איתו. יוצא 13. והתשובה הסופית 13.",
      do=GS.step((3, 4), [(3, 3), (3, 2)]) + GS.vals_do([(3, 5)]) + show("b-ok")),
    P("המלכודת: לכתוב $OPT(i-k)$. אבל $k$ הוא קילומטרים, לא מספר מקומות. כאן זה היה נותן 7 במקום 13.",
      do=GS.off() + show("b-t"),
      say="המלכודת: לכתוב אוֹפְּט של, בסוגריים, אַיי פחות קֵיי. אבל קֵיי הוא קילומטרים, לא מספר מקומות. כאן זה היה נותן שבע במקום שלוש עשרה.",
      hold=0.5),
]
q2 = Scene("q2", "שאלה 2: מסעדות", q2_ph,
           stage='<div class="dl-stack">'
                 + w.eqs("b", ["$OPT(i)=\\max\\bigl(OPT(i-1),\\ p_i+OPT(prev(i))\\bigr),\\qquad OPT(0)=0$"], 32)
                 .replace('id="b-0"', 'id="b-f"')
                 + f'<div id="b-g" class="h">{GS.html()}</div>'
                 + "</div>",
           panel=f'<div class="dl-q"><span class="qid">{Q2["id"]}</span>מקומות $d_1<\\dots<d_n$, רווח $p_i$, '
                 'מרחק של $k$ לפחות בין מסעדות. נוסחה לרווח המקסימלי.</div>'
                 + st.card("b-d", "ex", "$OPT(i)$: מקסימום כשפותחים רק ב-$1..i$")
                 + st.card("b-p", "rule", "🔑 $prev(i)$ = המקום האחרון עם $d_i-d_j\\ge k$")
                 + st.card("b-ok", "rule", "🔑 $13$: מסעדות ב-3 וב-8 קילומטר")
                 + st.card("b-t", "trap", "⚠️ לא $OPT(i-k)$: $k$ הוא מרחק"))

q3_ph = [
    P("שאלה שלישית. מערך זמנים של משימות. מותר לדלג על משימה, אבל לא על שתי משימות רצופות.", do=show("c-g")),
    P("רוצים את הזמן הכולל המינימלי של המשימות שנבחרו."),
    P("ההגדרה הנוחה: $T(i)$ הוא הזמן המינימלי של בחירה חוקית **שמסתיימת במשימה** $i$.", do=show("c-d"),
      say="ההגדרה הנוחה: טִי שֶל אַיי הוא הזמן המינימלי של בחירה חוקית שמסתיימת במשימה אַיי."),
    P("המשימה שנבחרה לפניה היא $i-1$ או $i-2$, אחרת היו שני דילוגים רצופים.", do=show("c-f"),
      say="המשימה שנבחרה לפניה היא אַיי פחות אחת, או אַיי פחות שתיים. אחרת היו שני דילוגים רצופים."),
    P("לכן $A[i]$ ועוד המינימום של שני אלה, והבסיס: אינדקס שלילי נותן 0, כלומר עוד לא בחרנו כלום.",
      say="לכן אֵיי במקום אַיי, ועוד המינימום של שני אלה. והבסיס: אינדקס שלילי נותן אפס, כלומר עוד לא בחרנו כלום."),
    P("נריץ. למשל במקום 6: שבע ועוד המינימום של 15 ו-15, כלומר 22.",
      do=GT.vals_do([(1, i) for i in range(6)]) + GT.step((1, 6), [(1, 5), (1, 4)])),
    P("ואיפה התשובה? מותר לדלג על המשימה האחרונה, ולכן הבחירה נגמרת באחת משתי האחרונות.",
      do=GT.vals_do([(1, 7)]) + GT.off() + show("c-a")),
    P("התשובה: המינימום של 25 ו-22, כלומר 22. כמו בדוגמה של השאלה.", do=GT.path([(1, 6)]) + show("c-ok")),
    P("המלכודת: להחזיר את התא האחרון בלבד. כאן הוא 25, ולא 22.", do=show("c-t"), hold=0.5),
]
q3 = Scene("q3", "שאלה 3: משימות", q3_ph,
           stage='<div class="dl-stack">'
                 + w.eqs("c", ["$T(i)=A[i]+\\min\\bigl(T(i-1),\\ T(i-2)\\bigr),\\qquad T(i<0)=0$"], 32).replace('id="c-0"', 'id="c-f"')
                 + f'<div id="c-g" class="h">{GT.html()}</div>'
                 + st.card("c-a", "rule", "🔑 התשובה: $\\min\\bigl(T(n-1),\\,T(n-2)\\bigr)$")
                 + "</div>",
           panel=f'<div class="dl-q"><span class="qid">{Q3["id"]}</span>זמן מינימלי של משימות שנבחרו, '
                 'בלי לדלג על שתי משימות רצופות. נוסחה עם מקרי בסיס.</div>'
                 + st.card("c-d", "ex", "$T(i)$: מינימום של בחירה ש<b>מסתיימת ב-</b>$i$")
                 + st.card("c-ok", "rule", "🔑 $\\min(25,22)=22$")
                 + st.card("c-t", "trap", "⚠️ לא רק $T(n-1)$: מותר לדלג על האחרונה"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בכל שאלה הגדרנו קודם מה מוחזר ועל איזה חלק, ורק אז כתבנו נוסחה.", do=show("s-1")),
    P("הנוסחה באה מההחלטה האחרונה: איזה קצה להסיר, לפתוח או לא, ואיזו משימה קודמת.", do=show("s-2")),
    P("ובכל אחת המלכודת הייתה במקרה שלא חשבו עליו: שני קצוות, מרחק לעומת אינדקס, ודילוג על האחרונה.", do=show("s-3")),
    P("זהו, סיימתם את הסולם. בהצלחה במבחן!", hold=0.6),
], stage='<div class="dl-stack">'
         + st.card("s-1", "rule", "🔑 קודם הגדרה, אחר כך נוסחה")
         + st.card("s-2", "rule", "🔑 הנוסחה = ההחלטה האחרונה")
         + "</div>",
   panel=st.card("s-3", "trap", "⚠️ בדקו את המקרה שלא חשבתם עליו"))

VIDEO = Video("D09", "dp_ladder", "מבחן גמר: תכנות דינמי", [title, q1, q2, q3, recap],
              bank={"22B-B-Q4a": None, "22B-B-Q4c": None, "24B-B-Q3a": None, "26A-A-Q1b": None})
