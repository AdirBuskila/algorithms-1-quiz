# -*- coding: utf-8 -*-
"""Generator for tools/raw/26A-B.json -- algorithms-1 (70162), semester A 2026, moed B (05/03/2026).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_26A-B.py

Source: exam booklet, 18 pages (cover with formulas p.1, bonus p.2, Q1 pp.3-6, Q2 pp.7-10, Q3 pp.11-14, Q4 pp.15-16,
answer lines only; pp.8, 10, 12, 15, 17, 18 are continuation pages with no text). Cap printed on the cover: 115.
There is NO answer source for this sitting (GATE1: no-key), so every item was held "no-key" and went to
the solver. The question text is transcribed character-exact from the rendered pages.

Items: Q1 a,b,c (5/15/5), Q2 a,b (12.5/12.5), Q3 a,b,c (5/10/10), Q4 (25), bonus a,b,c (5 each, num 5).
Notes
- The bonus block is printed on p.2, before Q1 (it is the second page of the booklet). Transcribed as num 5 like 26A-A.
- Q2 sub-points are 12.5 each, transcribed as printed.
- Q3's algorithm is the reverse-delete algorithm (remove an edge when the graph stays connected).
Solver pass (2026-10-24): all 12 items solved (solutionSource "solved", official false), pending the refuter.
Checks: tools/verify/26A-B/solve_all.py (all OK):
- Q1: OPT(i,j) "at most j days" recurrence == brute force over all night choices (3000 random); Q1a = 300.
- Q2a: BFS tree depth == eccentricity of s for random undirected graphs and random neighbour orders.
- Q2b: s->a, s->b, a->b gives DFS depths {1, 2} over all neighbour orders.
- Q3: reverse-delete on random connected graphs with distinct weights: n-1 edges, a tree, equal to the networkx MST;
  every removed edge closes a cycle of lighter edges (the cycle-property argument of Q3c).
- Q4: pivot = SELECT on the first half of C, partition C, keep the side holding rank k, until |C| <= n/2: equal to
  sorted(A)[k-1] on 20000 arrays (duplicates too), every SELECT call on <= n/2 elements; one round keeps <= 3N/4+1.
- Bonus: pi(aa)=[0,1] (a false); P=a^m, T=b^n never runs the fall-back loop (b true); (n-m+1)m is linear for m=1 or
  m=n (c true; 26A-A's version said "in the worst case", this one says "it is possible").
Figures: images/exams/26A-B-Q1-route.png (the route diagram, a context figure). No data graph is needed (Q2/Q3 are
abstract claims with no printed graph).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "26A-B.json"
HOLD = "no-key"


def Q(num, part, kind, topic, question, points, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "points": points}
    if "solution" in kw:   # solved by the solver (no official key exists)
        q.update({"solutionSource": "solved", "official": False, "confidence": "high"})
    else:
        q["hold"] = HOLD
    if part:
        q["part"] = part
    q.update(kw)
    return q


# ---------------------------------------------------------------- solver solutions (no official key)
SOL_1A = (r"נקודות הלינה הן $p_2=10$ ו-$p_4=20$, והסיום ב-$f=p_6=30$ (המלונות במרחק 5 קילומטר זה מזה, $p_i=5i$)." "\n"
          r"יום 1: מ-$0$ עד $10$, $d=10$, מאמץ $100$." "\n"
          r"יום 2: מ-$10$ עד $20$, $d=10$, מאמץ $100$." "\n"
          r"יום 3: מ-$20$ עד $30$, $d=10$, מאמץ $100$." "\n"
          r"סכום המאמץ: $100+100+100=300$." "\n"
          r"(זו גם הבחירה האופטימלית ל-3 ימים: המרחק הכולל 30 מחולק לשלושה ימים שווים.)")

SOL_1B = (r"נסמן $p_0=s=0$. נגדיר $OPT(i,j)$ = סכום המאמצים המזערי כדי להגיע ממוצא המסלול עד מלון $i$ (המיקום $p_i$) "
          r"בלכל היותר $j$ ימים, כאשר בסוף כל יום לנים באחד המלונות." "\n"
          r"**מקרי בסיס:**" "\n"
          r"$OPT(0,j)=0$ לכל $0\le j\le t$ (כבר נמצאים בנקודת ההתחלה)." "\n"
          r"$OPT(i,0)=\infty$ לכל $1\le i\le n$ (בלי ימי הליכה אי אפשר להתקדם)." "\n"
          r"**הנוסחה** לכל $1\le i\le n$ ו-$1\le j\le t$:" "\n"
          r"$$OPT(i,j)=\min_{0\le l<i}\Bigl\{OPT(l,j-1)+(p_i-p_l)^2\Bigr\}$$" "\n"
          r"**משמעות:** נסתכל על היום האחרון במסלול אופטימלי שמגיע ל-$p_i$. הוא מתחיל בנקודה $p_l$ כלשהי עם $l<i$ "
          r"(המלון של הלילה הקודם, או נקודת ההתחלה כש-$l=0$), ומאמצו $(p_i-p_l)^2$. החלק שלפניו הוא מסלול שמגיע ל-$p_l$ "
          r"בלכל היותר $j-1$ ימים, ובמסלול אופטימלי גם הוא חייב להיות מזערי (אחרת נחליף אותו בזול יותר ונשפר). "
          r"לכן מספיק לעבור על כל הבחירות של $l$ ולקחת את המינימום." "\n"
          r"**התשובה:** $OPT(n,t)$ (המלון ה-$n$ נמצא בנקודת הסיום, $p_n=f$)." "\n"
          r"הערה: כיוון ש-$t<n$ תמיד יש פתרון, ובגלל שהמאמץ $d^2$ קמור, פיצול יום לשני ימים לא מגדיל את המאמץ, "
          r"כך שבפועל הפתרון האופטימלי משתמש בדיוק ב-$t$ ימים.")

SOL_1C = (r"**זמן:** בטבלה $(n+1)\times(t+1)$ תאים. חישוב תא $OPT(i,j)$ עובר על כל $l<i$, כלומר $O(n)$ פעולות. "
          r'סה"כ $O(n\cdot t\cdot n)=O(n^2t)$ (ובגלל $t<n$ זה גם $O(n^3)$).' "\n"
          r"**מקום:** $O(nt)$ לטבלה כולה. מכיוון ששורה $j$ תלויה רק בשורה $j-1$, אפשר לשמור רק שתי שורות ולחשב את "
          r"הערך בזיכרון $O(n)$ (אם רוצים לשחזר את נקודות הלינה שומרים את הטבלה, $O(nt)$).")

SOL_2A = (r"**הטענה נכונה (הוכחה).**" "\n"
          r"תכונת BFS מהקורס: בעץ BFS המושרש ב-$s$, העומק של כל קודקוד $v$ בעץ שווה למרחק הקצר ביותר "
          r"$\delta(s,v)$ ב-$G$ (מספר הצלעות במסלול קצר ביותר)." "\n"
          r"תכונה זו נכונה לכל עץ BFS, בלי קשר לסדר שבו נסרקו השכנים, כי $\delta(s,v)$ מוגדר על ידי הגרף בלבד." "\n"
          r"עומק עץ הוא העומק המרבי של קודקוד בו, ולכן" "\n"
          r"$$\operatorname{depth}(T_{BFS})=\max_{v\in V}\delta(s,v)=\operatorname{depth}(T'_{BFS})$$" "\n"
          r"(כל הקודקודים נגישים מ-$s$, ולכן כולם מופיעים בשני העצים.)")

SOL_2B = (r"**הטענה אינה נכונה (הפרכה).**" "\n"
          r"דוגמה נגדית: $V=\{s,a,b\}$ והצלעות המכוונות $s\to a$, $s\to b$, $a\to b$. כל הקודקודים נגישים מ-$s$." "\n"
          r"- אם DFS מ-$s$ סורק קודם את $a$: מ-$a$ מגיעים ל-$b$, ומתקבל העץ $s\to a\to b$ שעומקו $2$." "\n"
          r"- אם DFS מ-$s$ סורק קודם את $b$: $b$ הוא עלה (אין לו צלעות יוצאות), חוזרים ל-$s$ ומגיעים ל-$a$; "
          r"הצלע $a\to b$ כבר לא נכנסת לעץ ($b$ כבר התגלה). מתקבל העץ עם הצלעות $s\to b$ ו-$s\to a$, שעומקו $1$." "\n"
          r"שני עצי DFS שונים המושרשים ב-$s$ עם עומקים $2\neq 1$, ולכן העומק אינו נקבע בהכרח.")

SOL_3A = (r"נוכיח ש-$T$ קשיר וחסר מעגלים; עץ על $n$ קודקודים מכיל בדיוק $n-1$ צלעות." "\n"
          r"**קשירות:** בתחילה הגרף קשיר. צלע מוסרת רק אם אחרי ההסרה הגרף נשאר קשיר, לכן אחרי כל צעד הגרף קשיר, "
          r"ובפרט $T$ קשיר. הקודקודים לא מוסרים, כך ש-$T$ מכיל את כל $n$ הקודקודים." "\n"
          r"**חוסר מעגלים:** נניח בשלילה שב-$T$ יש מעגל $C$, ותהי $e$ צלע על $C$. כשהאלגוריתם בחן את $e$, הגרף הנוכחי "
          r"הכיל את כל הצלעות של $T$ (צלעות רק מוסרות), ולכן הכיל את $C$. הסרת צלע שעל מעגל לא פוגעת בקשירות "
          r"(בין קצותיה נשאר המסלול שהוא שאר המעגל), ולכן האלגוריתם היה מסיר את $e$, בסתירה לכך ש-$e\in T$." "\n"
          r"לכן $T$ גרף קשיר וחסר מעגלים על $n$ קודקודים, כלומר עץ, ולכן $|T|=n-1$.")

SOL_3B = (r"מסעיף א': $T$ מכיל את כל $n$ הקודקודים של $G$ (האלגוריתם מסיר רק צלעות), הוא קשיר (כל הסרה שומרת על "
          r"קשירות) וחסר מעגלים (צלע על מעגל הייתה מוסרת בזמן שנבחנה, כי הגרף אז הכיל את המעגל)." "\n"
          r"גרף קשיר וחסר מעגלים הוא עץ, ו-$T\subseteq E$ מכיל את כל קודקודי $G$, ולכן $T$ עץ פורש של $G$.")

SOL_3C = (r"**תכונת המעגל:** אם $e$ היא הצלע הכבדה ביותר על מעגל כלשהו ב-$G$ (המשקלים שונים), אז $e$ אינה באף MST." "\n"
          r"הוכחה: נניח ש-$e=\{u,v\}$ בעץ פורש מינימלי $M$. הסרת $e$ מ-$M$ מפרקת אותו לשני רכיבים, ו-$u,v$ ברכיבים "
          r"שונים. שאר המעגל הוא מסלול מ-$u$ ל-$v$, ולכן יש עליו צלע $f\neq e$ שמחברת את שני הרכיבים. "
          r"$M-e+f$ הוא עץ פורש, ומשקלו קטן ממש ממשקל $M$ כי $w(f)<w(e)$. סתירה." "\n"
          r"**כל צלע שהאלגוריתם מסיר היא הכבדה ביותר על מעגל:** תהי $e=\{u,v\}$ צלע שהוסרה, ויהי $G'$ הגרף רגע לפני "
          r"הסרתה. הגרף $G'-e$ קשיר, ולכן יש בו מסלול $P$ מ-$u$ ל-$v$, ו-$P+e$ מעגל ב-$G$." "\n"
          r"כל צלע $f$ ב-$G'$ שכבדה מ-$e$ כבר נבחנה ונשארה, כלומר בזמן הבחינה שלה היא הייתה גשר (הסרתה ניתקה את הגרף). "
          r"$G'$ הוא תת-גרף של הגרף שהיה אז (על אותם קודקודים), ולכן $f$ גשר גם ב-$G'$, וגשר אינו נמצא על אף מעגל. "
          r"לכן כל הצלעות של $P$ קלות מ-$e$, ו-$e$ היא הצלע הכבדה ביותר על המעגל $P+e$." "\n"
          r"**סיום:** לפי תכונת המעגל אף צלע שהוסרה אינה ב-MST, ולכן ה-MST (שהמשקלים השונים הופכים ליחיד) מוכל ב-$T$. "
          r"לשניהם בדיוק $n-1$ צלעות (סעיף א'), ולכן $T$ הוא ה-MST.")

SOL_4 = (r"**רעיון:** את SELECT מפעילים רק על **חצי** מהמערך הנוכחי כדי לקבל ציר (pivot) טוב, ואת החלוקה (Partition) "
         r"עושים בעצמנו על כל המערך. כל סיבוב מקטין את המערך לכל היותר לכשלושה רבעים מגודלו, וכשהוא קטן מספיק "
         r"(לכל היותר $\frac n2$) מפעילים SELECT ישירות." "\n"
         "```\n"
         "KTH(A[1..n], k):\n"
         "    C <- A\n"
         "    while |C| > n/2:\n"
         "        C1 <- the first floor(|C|/2) elements of C      // |C1| <= n/2\n"
         "        p  <- SELECT(C1, ceil(|C1|/2))                    // median of C1\n"
         "        L <- {x in C : x < p} ; E <- {x in C : x = p} ; R <- {x in C : x > p}   // O(|C|)\n"
         "        if k <= |L|:            C <- L\n"
         "        else if k <= |L|+|E|:   return p\n"
         "        else:                   k <- k - |L| - |E| ; C <- R\n"
         "    return SELECT(C, k)                                   // |C| <= n/2\n"
         "```\n"
         r"**נכונות:** בכל סיבוב נשמרת השמורה: התשובה היא האיבר ה-$k$-י הקטן ב-$C$. כל איברי $L$ קטנים מכל איברי "
         r"$E$, שקטנים מכל איברי $R$, ולכן האיבר ה-$k$-י נמצא ב-$L$ (באותו דירוג), ב-$E$ (ואז הוא $p$), או ב-$R$ בדירוג "
         r"$k-|L|-|E|$. SELECT נקרא רק על $C_1$ שגודלו $\lfloor |C|/2\rfloor\le\frac n2$, ובסוף על $C$ כש-$|C|\le\frac n2$, "
         r"כך שהמגבלה נשמרת." "\n"
         r"**זמן:** נסמן $N=|C|$. $p$ הוא חציון של $C_1$, ולכן לפחות כרבע מאיברי $C$ (חצי מ-$C_1$) הם $\le p$ ולפחות כרבע "
         r"הם $\ge p$. מכאן $|L|,|R|\le\frac34N+1$. כל סיבוב עולה $O(N)$ (SELECT על $\frac N2$ איברים בזמן לינארי וחלוקה "
         r'אחת), והגדלים יורדים גאומטרית, לכן הזמן הכולל' "\n"
         r"$$O\Bigl(n+\tfrac34n+(\tfrac34)^2n+\cdots\Bigr)+O(n)=O(n)$$" "\n"
         r"(למעשה אחרי מספר קבוע של סיבובים $|C|\le\frac n2$). הקריאה האחרונה ל-SELECT לינארית בגודל $C$, כלומר $O(n)$." "\n"
         r"הערה: האלגוריתם אינו צריך את ההנחה $k<\frac n2$, והוא עובד לכל $k$.")

SOL_5A = (r"**לא נכון.** עבור התבנית $P=aa$ (כאן $m=2$) מתקבל $\pi=[0,1]$, כלומר מופיע הערך $m-1=1$. באופן כללי עבור "
          r"$P=a^m$ מתקבל $\pi[m]=m-1$: הרישא $a^{m-1}$ היא גם סיפא ממש של $P$.")

SOL_5B = (r"**נכון.** למשל $P=a^m$ ו-$T=b^n$: אף תו של הטקסט אינו מתאים לתו הראשון של התבנית, והמצב נשאר $q=0$, "
          r"כך שהלולאה הפנימית (לולאת הנסיגה $q\leftarrow\pi[q]$, שרצה רק כש-$q>0$) לא מתבצעת אף פעם, כלומר $O(1)$. "
          r"(ובכל מקרה, בניתוח לשיעורין מספר ההרצות הכולל שלה הוא $O(n)$, כלומר $O(1)$ בממוצע לכל תו של הטקסט.)")

SOL_5C = (r"**נכון.** זמן הריצה של האלגוריתם הנאיבי הוא $\Theta\bigl((n-m+1)\cdot m\bigr)$, וזה לינארי בחלק "
          r"מהמקרים: עבור $m=1$ מתקבל $\Theta(n)$, וכך גם עבור $m=n$ (הזזה אחת בלבד, $m=n$ השוואות), ובאופן כללי כש-$m$ "
          r"קבוע. רק כש-$m$ ו-$n-m$ שניהם בסדר גודל של $n$ (למשל $m\approx\frac n2$) הזמן הוא $\Theta(n^2)$.")


C1 = (r"ברצוננו לערוך מסע לאורך מסלול ישר מנקודת-התחלה $s=0$ לנקודת-סיום $f>0$." "\n"
      r"נתון מערך $p$ של מיקומי-מלונות $0<p_1<\cdots<p_n=f$ קילומטרים, כך שמלון $i$ ממוקם בדיוק $p_i$ קילומטרים "
      r"מנקודת תחילת המסלול." "\n"
      r"להלן סרטוט המסלול עבור $n=6$:" "\n"
      r"![סרטוט המסלול עבור n=6: נקודת ההתחלה s, ששה מלונות ונקודת הסיום f, עם המרחקים p1 עד p6 מהתחלת המסלול]"
      r"(images/exams/26A-B-Q1-route.png)" "\n"
      r"במהלך המסע לנים בכל לילה במלון אחד." "\n"
      r"החופשה מוגבלת בזמן, ולכן חייבים לסיים את המסע תוך לכל היותר $t$ ימים (נתון $t<n$)." "\n"
      r"המאמץ שנדרש ביום-הליכה הינה $d^2$, כאשר $d$ הוא המרחק שהולכים באותו יום." "\n"
      r"עלינו לבחור את נקודות-הלינה, כך שנמזער את סכום המאמצים בכל המסע." "\n"
      r"הערה: הבעיה ניתנת לפתרון בעזרת תכנון דינמי.")

C2 = (r"נתון גרף $G=(V,E)$ עם קודקוד מוצא $s\in V$. נתון כי כל יתר הקודקודים בגרף נגישים מהמוצא, כלומר ניתן להגיע "
      r"מקודקוד המוצא $s$ לכל קודקוד $v\in V$." "\n"
      r"נסמן ב: $T_{BFS},T'_{BFS}$ שני עצי BFS שונים של $G$ המושרשים ב-$s$. בדומה נסמן ב-$T_{DFS},T'_{DFS}$ שני עצי DFS "
      r"שונים של $G$ המושרשים ב-$s$." "\n"
      r"בשני הסעיפים הבאים מובאת טענה שיש להוכיח או להפריך. אם הטענה נכונה אז נדרשת הוכחה מדויקת וקצרה. "
      r"אם הטענה אינה נכונה אז נדרשת דוגמה נגדית.")

C3 = (r"יהי $G=(V,E)$ גרף קשיר עם $|V|=n$." "\n"
      r"לכל צלע משקל חיובי, וכל המשקלים שונים זה מזה." "\n"
      r"נבחן את האלגוריתם הבא:" "\n"
      r"1. מיין את הצלעות לפי סדר משקל יורד." "\n"
      r"2. עבור על הצלעות לפי הסדר הזה. לכל צלע $e$:" "\n"
      r"- הסר את $e$ מן הגרף אם לאחר הסרתה הגרף נשאר קשיר." "\n"
      r"- אחרת, נשאיר אותה." "\n"
      r"3. בסיום נסמן ב-$T$ את קבוצת הצלעות שנותרה.")

BONUS = (r"**שאלת בונוס - (15 נקודות)** יש להקיף את התשובה הנכונה ולציין נימוק קצר. "
         r"אין קשר בין הסעיפים השונים, כל סעיף 5 נקודות." "\n")

questions = [
    Q(1, "א", "computation", "dp_optimization",
      r"(5 נקודות) בהמשך לסרטוט בשאלה, הנח שהמרחק בין כל מלון הוא בדיוק 5 קילומטר, ואנו רוצים לסיים את המסע ב-3 ימים. "
      r"מהו סכום המאמץ אם נבחר כנקודות לינה את $p_2$ ואת $p_4$. נמקו תשובתכם.",
      5, contextId="c1", solution=SOL_1A),
    Q(1, "ב", "algorithm", "dp_optimization",
      r"(15 נקודות) בהינתן נקודת-התחלה $s=0$ ונקודת-סיום $f>0$ ומערך $p$ של מיקומי-מלונות וכן $t$, כמות הימים שניתן "
      r"לכל היותר לטייל:" "\n"
      r"כתבו נוסחה רקורסיבית לחישוב העלות המזערית לסכום המאמצים בכל המסע." "\n"
      r"יש לפרט גם את מקרי הבסיס. יש לפרט את משמעות הנוסחה.",
      15, contextId="c1", solution=SOL_1B),
    Q(1, "ג", "computation", "dp_optimization",
      r"(5 נקודות) מהי סיבוכיות זמן הריצה של אלגוריתם תכנון דינמי המבוסס על הנוסחה שכתבתם בסעיף ב', "
      r"ומהי סיבוכיות המקום שלו?",
      5, contextId="c1", solution=SOL_1C),

    Q(2, "א", "truefalse", "graph_proofs",
      r"(12.5 נקודות) אם $G$ גרף לא מכוון, אז בהכרח לשני עצי ה-BFS יש אותו עומק "
      r"$\operatorname{depth}(T_{BFS})=\operatorname{depth}(T'_{BFS})$." "\n"
      r"(בחרתי ב: הוכחה/הפרכה - יש להקיף את בחירתך.)",
      12.5, contextId="c2", solution=SOL_2A, verdict=True),
    Q(2, "ב", "truefalse", "graph_proofs",
      r"(12.5 נקודות) אם $G$ גרף מכוון, אז בהכרח לשני עצי ה-DFS יש אותו עומק "
      r"$\operatorname{depth}(T_{DFS})=\operatorname{depth}(T'_{DFS})$." "\n"
      r"(בחרתי ב: הוכחה/הפרכה - יש להקיף את בחירתך.)",
      12.5, contextId="c2", solution=SOL_2B, verdict=False),

    Q(3, "א", "proof", "mst",
      r"(5 נקודות) הוכח כי כאשר האלגוריתם נעצר, ב-$T$ יש בדיוק $n-1$ צלעות.",
      5, contextId="c3", solution=SOL_3A),
    Q(3, "ב", "proof", "mst",
      r"(10 נקודות) הוכח כי הגרף המתקבל הוא עץ פורש של $G$.",
      10, contextId="c3", solution=SOL_3B),
    Q(3, "ג", "proof", "mst",
      r"(10 נקודות) הוכח כי $T$ הוא עץ פורש מינימלי (MST).",
      10, contextId="c3", solution=SOL_3C),

    Q(4, None, "algorithm", "divide_conquer",
      r"נתון מערך בגודל $n$." "\n"
      r"רוצים למצוא את האיבר שהוא ה-$k$-י הקטן ביותר כאשר $k<\frac{n}{2}$." "\n"
      r"מותר להשתמש ב-SELECT רק על תתי מערכים בגודל לכל היותר $\frac{n}{2}$:" "\n"
      r"הראו אלגוריתם הרץ בזמן $O(n)$ לפתרון הבעיה המוצגת. נמקו תשובתכם.",
      25, solution=SOL_4),

    Q(5, "א", "truefalse", "kmp_strings",
      BONUS + r"נסתכל על הטבלה של $\pi$ המתקבלת בהרצת אלגוריתם KMP עבור תבנית באורך $m>1$ אזי לא יתכן כי בטבלה יש את "
      r"הערך $m-1$." "\n"
      r"נכון / לא נכון. נימוק:",
      5, solution=SOL_5A, verdict=False),
    Q(5, "ב", "truefalse", "kmp_strings",
      r"**שאלת בונוס** (סעיף בלתי תלוי, 5 נקודות)." "\n"
      r"יתכן שבאלגוריתם KMP עם טקסט $T$ באורך $n$ ותבנית $P$ באורך $m$, הלולאה הפנימית תתבצע $O(1)$." "\n"
      r"נכון / לא נכון. נימוק:",
      5, solution=SOL_5B, verdict=True),
    Q(5, "ג", "truefalse", "kmp_strings",
      r"**שאלת בונוס** (סעיף בלתי תלוי, 5 נקודות)." "\n"
      r"יתכן שהאלגוריתם הנאיבי לפתרון בעיית חיפוש מחרוזת $P$ באורך $m$ בטקסט $T$ באורך $n$ רץ בזמן לינארי." "\n"
      r"נכון / לא נכון. נימוק:",
      5, solution=SOL_5C, verdict=True),
]

exam = {
    "examCode": "26A-B",
    "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד ב (05/03/2026)",
    "year": 2026,
    "examDate": "05/03/2026",
    "sourceFile": "26A-B exam pp.1-18",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1: מסע עם לינה במלונות", "text": C1},
        "c2": {"kind": "text", "title": "שאלה 2: עצי BFS ו-DFS", "text": C2},
        "c3": {"kind": "text", "title": "שאלה 3: אלגוריתם הסרת צלעות", "text": C3},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
