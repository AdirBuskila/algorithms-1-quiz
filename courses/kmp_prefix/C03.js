/* KMP course, level 3 - pi as border lengths: the chain pi[q], pi[pi[q]], ... */
COURSE_LEVEL("kmp_prefix", {
  id: "C03", order: 3, icon: "⛓️", title: "π כרשימת borders: שרשרת הנסיגה",
  goal: "לקרוא מטבלת π את כל ה-borders של כל רישא, ולהבין למה הנסיגה היא דווקא k ← π[k].",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>הערך $\pi[q]$ נותן את ה-border הארוך ביותר של $P[1..q]$. אבל יש לרישא הזו עוד borders, קצרים יותר. אפשר למצוא את כולם מהטבלה.</p>
    <div class="lesson-rule">🔑 <b>שרשרת ה-borders:</b> האורכים של כל ה-borders הלא ריקים של $P[1..q]$ הם בדיוק $\pi[q],\ \pi[\pi[q]],\ \pi[\pi[\pi[q]]],\dots$ עד שמגיעים ל-$0$. הסיבה: border של border הוא border. אם $B$ הוא border של $P[1..q]$ באורך $k=\pi[q]$, אז ה-border הארוך ביותר של $B$ עצמו, שאורכו $\pi[k]$, הוא גם border של $P[1..q]$.</div>
    <div class="lesson-ex">דוגמה: $P=$<code>ABABABA</code> עם $\pi=0,0,1,2,3,4,5$. עבור $q=7$ השרשרת היא $5,3,1$ ואז $0$. לכן ל-<code>ABABABA</code> שלושה borders לא ריקים: <code>ABABA</code> (5), <code>ABA</code> (3) ו-<code>A</code> (1). מספר ה-borders הלא ריקים הוא מספר האיברים בשרשרת לפני ה-$0$.</div>
    <p><b>למה הנסיגה היא $k\leftarrow\pi[k]$?</b> כשה-border באורך $k$ לא מצליח להתארך באות $P[q]$, מחפשים את ה-border הבא בגודלו של $P[1..q-1]$, כי רק border כזה יכול להתארך. ה-border הבא בגודלו של $P[1..k]$ הוא $\pi[k]$. ערכים באמצע, כמו $k-1$, בדרך כלל אינם borders בכלל, ובדיקה שלהם היא בזבוז או טעות.</p>
    <div class="lesson-trap">⚠️ אין לצפות שהשרשרת תרד ב-1 בכל פעם. בדוגמה למעלה היא יורדת $5\to3\to1$ (פעמיים ב-2), כי רק האורכים האלה הם borders.</div>` },
  questions: [
    { id: "C03-Q1",
      step: { type: "numeric", prompt: "טבלת $\\pi$ של $P=$`AABAABAA` היא $0,1,0,1,2,3,4,5$. כמה borders לא ריקים יש למחרוזת `AABAABAA` כולה ($q=8$) ?", answer: 3, tol: 0,
              explain: "השרשרת מ-$q=8$: $\\pi[8]=5$, אחר כך $\\pi[5]=2$, אחר כך $\\pi[2]=1$, ואז $\\pi[1]=0$. שלושה אורכים: 5, 2 ו-1. ה-borders הם `AABAA`, `AA` ו-`A`." },
      recap: "מספר ה-borders הלא ריקים = אורך שרשרת π עד 0" },
    { id: "C03-Q2",
      question: "מהם אורכי כל ה-borders הלא ריקים של `AABAABAA` (הטבלה: $0,1,0,1,2,3,4,5$) ?",
      options: [{ id: "a", value: "$5,4,3,2,1$" }, { id: "b", value: "$5,3,1$" }, { id: "c", value: "$5,2,1$" }, { id: "d", value: "$5,2$" }],
      correctId: "c",
      explanation: "השרשרת היא $\\pi[8]=5$, $\\pi[5]=2$, $\\pi[2]=1$. אפשר לוודא: `AABAA` היא רישא וסיפא, וגם `AA`, וגם `A`. אורך 4 אינו border כי הרישא `AABA` שונה מהסיפא `ABAA`. אורך 3 אינו border כי `AAB` שונה מ-`BAA`. הרשימה $5,2$ שוכחת את `A`.",
      recap: "borders: π[q], π[π[q]], ... עד 0" },
    { id: "C03-Q3",
      step: { type: "numeric", prompt: "מהו אורך ה-border השני בגודלו של `AABAABAA` ? (הטבלה: $0,1,0,1,2,3,4,5$)", answer: 2, tol: 0,
              explain: "ה-border הארוך ביותר הוא $\\pi[8]=5$, וה-border הבא אחריו הוא $\\pi[5]=2$ (`AA`)." },
      recap: "ה-border הבא: π של הקודם" },
    { id: "C03-Q4",
      step: { type: "numeric", prompt: "מחשבים $\\pi[9]$ עבור תבנית שמתחילה ב-`AABAABAA` (הטבלה עד $q=8$: $0,1,0,1,2,3,4,5$). אחרי $k=\\pi[8]=5$ מתברר ש-$P[6]\\ne P[9]$. לאיזה ערך $k$ הקוד נסוג ?", answer: 2, tol: 0,
              explain: "הנסיגה היא $k\\leftarrow\\pi[5]=2$. המועמד $k-1=4$ לא יכול להיות border של `AABAA`: הרישא `AABA` שונה מהסיפא `ABAA`." },
      recap: "נסיגה ל-π[k], לא ל-k−1" },
    { id: "C03-Q5",
      step: { type: "fillblank", prompt: "השלימו את שורת הנסיגה בלולאה של חישוב $\\pi$.", code: true, blankIndex: 3,
              lines: [
                "pi[1] <- 0 ; k <- 0",
                "for q <- 2 to m",
                "    while k > 0 and P[k+1] != P[q]",
                "        k <- ___",
                "    if P[k+1] = P[q]",
                "        k <- k + 1",
                "    pi[q] <- k"],
              options: [{ id: "a", value: "k - 1" }, { id: "b", value: "0" }, { id: "c", value: "pi[k]" }, { id: "d", value: "pi[k - 1]" }],
              correctId: "c",
              explain: "הנסיגה הנכונה היא `pi[k]`. נסיגה ל-`k - 1` נכשלת למשל על `ABABB`. נסיגה ל-`0` נכשלת למשל על `AABAAA`, ונסיגה ל-`pi[k - 1]` נכשלת גם היא על `AABAAA`. בכל אחד מהמקרים הטבלה שמתקבלת שונה מהטבלה הנכונה." },
      recap: "השורה: k ← π[k]" },
  ],
});
