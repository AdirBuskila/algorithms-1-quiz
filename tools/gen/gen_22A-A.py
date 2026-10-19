# -*- coding: utf-8 -*-
"""Generator for tools/raw/22A-A.json -- algorithms-1 (60072), semester A 5782 (2022), moed A.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_22A-A.py

Source: ONE file, a 4-page typed "solution" document (no separate exam file). Each question is a shaded box holding the
question text, followed by the solution text under it (page 1: Q1; page 2: Q2, Q3; pages 3-4: Q4, then an unnumbered
box with a graph and six options, which is transcribed as Q5). The moed (A) and year are inferred from the title
(it says only "מועד א' באלגוריתמים 1 תשפ"ב").
Items: Q1; Q2; Q3 a,b; Q4 a,b; Q5 (multiple choice, held).

Transcription notes
- No points are printed anywhere, so no `points` are set.
- Q1: the file shows the recurrence and then the two lemmas (claims 1-2) it follows from. Transcribed as the solution.
- Q3: the printed solution is the algorithm plus one sentence on the cost; Q3b's answer (Theta(k*n)) is that sentence.
- Q4 b: the proof of the greedy-choice property is split over the page break (pp.3-4); joined here.
- Q5: unnumbered box after Q4 (no "שאלה 5" header). The page shows option e pre-marked (radio button), but
  option c is also a possible output of the algorithm (see checks), so the key is ambiguous -> HELD (ASK_ADIR).

Checks (tools/verify/22A-A/checks.py, brute force + networkx):
- Q1: the recurrence equals a brute force over all common subsequences (300 random triples).
- Q2: t = (#occurrences of A in A*A) >= 3 iff A = B^k with k >= 2, for all binary strings up to length 12; example.
- Q3: two distinct polynomials of degree < n agree on at most n-1 of the n+1 points 0..n (so one round errs < 1).
- Q4: the greedy algorithm equals a brute force over all choices on 3000 random inputs; the example gives 35.
- Q5: the set of outputs of the 2-approximation was enumerated: options c and e are reachable, a, b, f are not.
Graph data: tools/verify/22A-A/graphs.json (Q5).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "22A-A.json"
SRC = "lecturer-solution"


def Q(num, part, kind, topic, question, solution, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution,
         "solutionSource": SRC, "official": False, "confidence": "med"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


# ---------------------------------------------------------------- Q1
Q1 = (r"להלן תיאור בעיית אורך תת הסדרה המשותפת משולשת הארוכה ביותר:" "\n"
      r"**קלט:** שלוש הסדרות $S_1,S_2,S_3$ כל אחת באורך $n$." "\n"
      r"**פלט:** אורך הסדרה $S$ שהיא תת סדרה משותפת ארוכה ביותר של $S_1,S_2,S_3$." "\n"
      r"הבעיה ניתנת לפתרון בעזרת תכנון דינמי." "\n"
      r"**הציגו** נוסחה רקורסיבית לפתרון הבעיה הנתונה. נמקו בקצרה את נכונות הנוסחה "
      r"(המלצה: פרטו בנימוק לכל פרמטר בנוסחה את תפקידו).")

S1 = r"""$$\mathrm{LCS}(i,j,l)=\begin{cases}0 & ;\ i=0\ \vee\ j=0\ \vee\ l=0\\ \mathrm{LCS}(i-1,j-1,l-1)+1 & ;\ S_1[i]=S_2[j]=S_3[l]\\ \max\bigl(\mathrm{LCS}(i-1,j,l),\,\mathrm{LCS}(i,j-1,l),\,\mathrm{LCS}(i,j,l-1)\bigr) & ;\ \text{otherwise}\end{cases}$$
בדומה להוכחות שהוכחנו במסגרת ההרצאה, ניתן להוכיח את הטענות הבאות, מהם נובעת נכונות הנוסחה.
**טענה 1:** יהיו $X=\langle x_1,x_2,\ldots,x_m\rangle$ ו-$Y=\langle y_1,y_2,\ldots,y_n\rangle$ ו-$Z=\langle z_1,z_2,\ldots,z_k\rangle$ סדרות, ותהי $W=\langle w_1,w_2,\ldots,w_t\rangle$ תמ"א של $X$ ו-$Y$ ו-$Z$. אם $x_m=y_n=z_k$ ו-$w_t=x_m=y_n=z_k$, אזי $W_{t-1}$ היא תמ"א של $X_{m-1}$ ו-$Y_{n-1}$ ו-$Z_{k-1}$.
**טענה 2:** יהיו $X,Y,Z$ סדרות כמקודם ותהי $W$ תמ"א של $X$ ו-$Y$ ו-$Z$. אם $x_m\neq y_n$ או $x_m\neq z_k$ או $y_n\neq z_k$ (כלומר לא כל שלושת התווים האחרונים שווים), אזי: אם $w_t\neq x_m$ אז $W$ היא תמ"א של $X_{m-1}$ ו-$Y$ ו-$Z$; אם $w_t\neq y_n$ אז $W$ היא תמ"א של $X$ ו-$Y_{n-1}$ ו-$Z$; אחרת ($w_t\neq z_k$) $W$ היא תמ"א של $X$ ו-$Y$ ו-$Z_{k-1}$.
האינדקסים $i,j,l$ מציינים את $S_1[1..i],\,S_2[1..j],\,S_3[1..l]$ בהתאמה. והפונקציה LCS מחזירה את אורך תת הסדרה המשותפת."""

# ---------------------------------------------------------------- Q2
Q2 = (r"מחרוזת $A$ תקרא מחזורית אם קיימת מחרוזת $B$ וקבוע $k\ge 2$ כך שמתקיים $A=B^k$." "\n"
      r"דוגמה: המחרוזת $A=abbabbabbabb$ מחזורית כאשר $B=abb$, $k=4$." "\n"
      r"הציעו אלגוריתם לינארי המקבל מחרוזת $A$ ומחזיר אמת אם $A$ מחזורית, כלומר אם קיימת מחרוזת $B$ וקבוע $k\ge 2$ "
      r"כך שמתקיים $A=B^k$, אחרת מחזיר לא. רמז: היעזרו באלגוריתם KMP." "\n"
      r"נניח כי $KMP(X,Y)$ הוא מספר המופעים של $Y$ ב-$X$, וכן שהסימן $*$ הוא שרשור בין 2 מחרוזות.")

S2 = r"""1. יהי $t=KMP(A*A,A)$.
2. אם $t\ge 3$ החזר אמת אחרת החזר שקר."""

# ---------------------------------------------------------------- Q3
Q3 = (r"להלן תיאור בעיית הפולינומים הזהים:" "\n"
      r"**קלט:** פולינום $P(x)=\sum_{i=0}^{n-1}a_i x^i$ כסכום חזקות וכן פולינום $G(x)=\prod_{i=0}^{n-1}(x-b_i)$ "
      r"כמכפלת גורמים ליניאריים." "\n"
      r"**פלט:** החזר אמת אם $G(x)=P(x)$ כן, אחרת, החזר שקר." "\n"
      r"לדוגמה: $P(x)=x^2-10x+21=(x-3)\cdot(x-7)=G(x)$")

S3A = r"""כזכור, כל פולינום מדרגה $n$ מוגדר על ידי $n+1$ נקודות במישור.
האלגוריתם:
1. בצע $k$ פעמים את התהליך מסעיף 2 עד 3:
2. בחר באופן אקראי מספר בין $0$ ל-$n$ נסמנו $t$
3. אם $P(t)\neq G(t)$ החזר שקר (וסיים)
4. החזר אמת"""

S3B = r"""האלגוריתם יבצע במקרה הגרוע $k$ פעמים חישוב של ערך על הפולינום (בחרנו להציב ערכים "קטנים" בפולינום וכך נרשה ל"התעלם" מגודל תוצאות החישוב ונניח כי גודל זה ניתן לייצוג במשתנה סטנדרטי) החישוב דורש $n$ פעולות חשבון (בהנחה בסיסיות) ולכן העלות $\Theta(k\cdot n)$."""

# ---------------------------------------------------------------- Q4
Q4 = (r"בהינתן סדרה של $m$ מערכים מספריים (ממשיים), כל מערך בסדרה בגודל $n$:" "\n"
      r"$A_1[0..(n-1)],\ A_2[0..(n-1)],\ A_3[0..(n-1)],\ldots,A_m[0..(n-1)]$" "\n"
      r"נאמר ש-$k$ הוא **סכום נציגים עולים של סדרת המערכים**, אם קיימים $m$ אינדקסים $i_1,i_2,\ldots,i_m$ "
      r"כך שמתקיימים שני התנאים הבאים:" "\n"
      r"$A_1[i_1]<A_2[i_2]<\ldots<A_m[i_m]$" "\n"
      r"$k=A_1[i_1]+A_2[i_2]+\ldots+A_m[i_m]$" "\n"
      r"להלן תיאור בעיית **סכום נציגים עולים של סדרת מערכים המקסימלי**:" "\n"
      r"**קלט:** סדרה של $m$ מערכים (ממשיים), כל מערך בסדרה בגודל $n$, $A_1[0..(n-1)],\ldots,A_m[0..(n-1)]$." "\n"
      r"**פלט:** אם קיים $k$ שהוא **סכום נציגים עולים של סדרת המערכים** הנתונה, החזר את **סכום נציגים עולים של "
      r"סדרת המערכים המקסימלי**, אחרת, החזר $0$." "\n"
      r"**דוגמה:** עבור הקלט הבא של 3 המערכים הבאים הפלט יהיה $35$:" "\n"
      r"$A_1=[-3,-4,-8,-1]$" "\n"
      r"$A_2=[20,17,-8,9]$" "\n"
      r"$A_3=[-7,4,3,19]$")

S4A = r"""**אלג' חמדן:**
1. בחר בערך הגדול ביותר במערך $A_m$ לקבוצת הפתרון $A$, סמנו ב-$TEMPMAX$.
2. לכל $t$ מ-$m-1$ עד $1$ בצע:
    - (א) אם לא קיימים ערכים הקטנים מ-$TEMPMAX$ ב-$A_t$ החזר $0$ (וסיים).
    - (ב) מצא את הערך הגדול ביותר ב-$A_t$ ושקטן מ-$TEMPMAX$, הוסף ערך זה לפתרון $A$ ועדכן אותו להיות הערך של $TEMPMAX$.
3. החזר את $A$."""

S4B = r"""**הוכחת הבחירה החמדנית:**
נסמן ב-$MAX$ את הערך הגדול ביותר של המערך $A_m$.
יהי $A^*$ פתרון אופטימלי של הבעיה.
אם הערך $MAX$ בפתרון האופטימלי $A^*$ סימנו.
נסתכל על הערך הנמצא בפתרון האופטימלי ושייך למערך $A_m$, נסמנו ב-$K$.
נבחן כל אחד מהמצבים שיתכנו בהשוואה בין 2 מספרים:
- $K=MAX$ סימנו, הבחירה החמדנית הראשונה נמצאת בפתרון אופטימלי.
- $MAX<K$ לא יתכן, כי שני הערכים נלקחו מהמערך $A_m$ אבל לפי האלג' $MAX$ הוא הערך הגדול ביותר במערך $A_m$.
- $K<MAX$ לא יתכן, כי בהחלפת $K$ עם $MAX$ בפתרון $A^*$ נקבל גם פתרון העומד בדרישה של סדרה עולה (כי שני הערכים נלקחו מהמערך האחרון ו-$MAX$ גדול מ-$K$, בפרט גדול מהאיבר הקודם ל-$K$ בפתרון $A^*$ שקטן מ-$K$), בסתירה לכך ש-$A^*$ פתרון אופטימלי, כי מצאנו פתרון שערכו גדול מהפתרון האופטימלי."""

# ---------------------------------------------------------------- Q5 (held)
Q5 = (r"נתון הגרף הבא, מי מהקבוצות הבאות יכול להיות כיסוי קודקודים שהתקבל מהפעלת אלגוריתם הקירוב שלמדנו בהרצאה "
      r"לבעיית כיסוי קודקודים.")

OPT5 = [
    {"id": "a", "value": r"$C=\{X_5,X_3,X_2,X_7,X_1,X_9\}$"},
    {"id": "b", "value": r"$C=\{X_3,X_4,X_1,X_9,X_0,X_6\}$"},
    {"id": "c", "value": r"$C=\{X_1,X_8,X_3,X_4,X_9,X_6\}$"},
    {"id": "d", "value": "לא הוצג פתרון התואם את האלגוריתם הקרובי שלמדנו"},
    {"id": "e", "value": r"$C=\{X_1,X_9,X_6,X_3,X_5,X_8\}$"},
    {"id": "f", "value": r"$C=\{X_6,X_3,X_1,X_8,X_0,X_4\}$"},
]

questions = [
    Q(1, None, "algorithm", "dp_sequences", Q1, S1),
    Q(2, None, "algorithm", "kmp_strings", Q2, S2),
    Q(3, "א", "algorithm", "randomized",
      r"הציעו אלגוריתם הסתברותי מסוג מונטה קרלו לפתרון הבעיה.", S3A, contextId="c3"),
    Q(3, "ב", "computation", "randomized",
      r"מה זמן הריצה של האלגוריתם? אין צורך לנמק.", S3B, contextId="c3"),
    Q(4, "א", "algorithm", "greedy",
      r"כתבו אלגוריתם חמדני לפתרון הבעיה. (ניתן לנסח את האלגוריתם במילים או בפסודו קוד).", S4A, contextId="c4"),
    Q(4, "ב", "proof", "greedy",
      r"הוכח שהאלגוריתם שהצעת מקיים את תכונת הבחירה החמדנית.", S4B, contextId="c4"),
    {"num": 5, "kind": "mcq", "topic": "approximation", "question": Q5,
     "image": "images/exams/22A-A-Q5-graph.png", "options": OPT5,
     "hold": "key-ambiguous: the page marks only option e, but option c is also a possible output of the 2-approximation (checked by enumeration)"},
]

exam = {
    "examCode": "22A-A",
    "examLabel": "אלגוריתמים 1 (60072), סמסטר א' תשפ\"ב, מועד א (2022)",
    "year": 2022,
    "examDate": "2022",
    "sourceFile": "22A-A lecturer solution pp.1-4 (questions embedded in the solution file)",
    "solutionFile": "22A-A lecturer solution pp.1-4",
    "contexts": {
        "c3": {"kind": "text", "title": "שאלה 3: בעיית הפולינומים הזהים", "text": Q3},
        "c4": {"kind": "text", "title": "שאלה 4: סכום נציגים עולים", "text": Q4},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
