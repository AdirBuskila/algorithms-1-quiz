/* KMP course, level 1 - borders and the definition of the prefix function (pi) */
COURSE_LEVEL("kmp_prefix", {
  id: "C01", order: 1, icon: "🔤", title: "רישא, סיפא ו-border: מהו π",
  goal: "להגדיר border ולחשב ערך בודד של π לפי ההגדרה, בלי אלגוריתם.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>מחרוזת $P$ באורך $m$ נכתבת $P[1]P[2]\cdots P[m]$ (האינדקסים מתחילים מ-1). <b>רישא</b> היא קטע מההתחלה, <b>סיפא</b> היא קטע מהסוף, ו-<b>אמיתית</b> פירושו קצרה מהמחרוזת כולה. הסימון $P[1..q]$ הוא הרישא באורך $q$.</p>
    <div class="lesson-rule">🔑 <b>border</b> של מחרוזת הוא רישא אמיתית שהיא גם סיפא שלה. <b>$\pi[q]$</b> הוא האורך של ה-border <b>הארוך ביותר</b> של $P[1..q]$ (ו-$0$ אם אין אף border לא ריק).</div>
    <div class="lesson-ex">דוגמה: $P=$<code>ABABA</code>. ל-<code>ABABA</code> יש שני borders לא ריקים: <code>A</code> (אורך 1) ו-<code>ABA</code> (אורך 3). הארוך ביותר באורך $3$, ולכן $\pi[5]=3$.</div>
    <table><thead><tr><th>$q$</th><th>הרישא $P[1..q]$</th><th>ה-border הארוך ביותר</th><th>$\pi[q]$</th></tr></thead>
    <tbody>
    <tr><td>1</td><td><code>A</code></td><td>אין</td><td>0</td></tr>
    <tr><td>2</td><td><code>AB</code></td><td>אין</td><td>0</td></tr>
    <tr><td>3</td><td><code>ABA</code></td><td><code>A</code></td><td>1</td></tr>
    <tr><td>4</td><td><code>ABAB</code></td><td><code>AB</code></td><td>2</td></tr>
    <tr><td>5</td><td><code>ABABA</code></td><td><code>ABA</code></td><td>3</td></tr>
    </tbody></table>
    <p>שני דברים שנכונים תמיד: $\pi[1]=0$ (לרישא באורך 1 אין רישא אמיתית לא ריקה), ו-$\pi[q]<q$ (כי ה-border אמיתי).</p>
    <div class="lesson-trap">⚠️ המחרוזת עצמה אינה border של עצמה, ולכן לא נספר אותה. ⚠️ $\pi[q]$ מתייחס רק לרישא $P[1..q]$ ולא לתבנית כולה, וכל $q$ נבדק לחוד.</div>
    <p>איך בודקים border באורך $k$? משווים את $k$ האותיות הראשונות של $P[1..q]$ ל-$k$ האותיות האחרונות שלה. מנסים מהארוך אל הקצר, ועוצרים בהתאמה הראשונה.</p>` },
  questions: [
    { id: "C01-Q1",
      question: "מהו $\\pi[5]$ עבור התבנית $P=$`AABAA` ?",
      options: [{ id: "a", value: "1" }, { id: "b", value: "2" }, { id: "c", value: "3" }, { id: "d", value: "5" }],
      correctId: "b",
      explanation: "הרישאות של `AABAA` הן `A`, `AA`, `AAB`, `AABA`. הסיפאות הן `A`, `AA`, `BAA`, `ABAA`. הם שווים עבור `A` ו-`AA`, ולכן ה-border הארוך ביותר הוא `AA` באורך 2. הערך 1 הוא border קצר יותר, לא הארוך ביותר. הערך 3 לא תקין כי `AAB` שונה מ-`BAA`. הערך 5 הוא המחרוזת עצמה, וזו לא רישא אמיתית.",
      recap: "π[q] = אורך ה-border הארוך ביותר; המחרוזת עצמה לא נספרת" },
    { id: "C01-Q2",
      step: { type: "numeric", prompt: "עבור $P=$`ABCABD` חשבו את $\\pi[5]$. כלומר, מהו האורך של ה-border הארוך ביותר של הרישא `ABCAB` ?", answer: 2, tol: 0,
              explain: "הרישא היא `ABCAB`. הסיפא `AB` שווה לרישא `AB`. באורך 3 משווים את `ABC` ל-`CAB` ואין התאמה, ובאורך 4 את `ABCA` ל-`BCAB`, גם אין. לכן $\\pi[5]=2$." },
      recap: "מנסים אורכים מהארוך לקצר, ועוצרים בהתאמה הראשונה" },
    { id: "C01-Q3",
      step: { type: "choice", prompt: "מהי טבלת $\\pi$ המלאה של $P=$`ABABA` ?",
              options: [{ id: "a", value: "$0,0,1,1,1$" }, { id: "b", value: "$0,0,1,2,2$" }, { id: "c", value: "$0,0,1,2,3$" }, { id: "d", value: "$0,1,2,3,4$" }],
              correctId: "c",
              explain: "הטבלה שחושבה בשיעור: $0,0,1,2,3$. הטבלה $0,1,2,3,4$ היא של `AAAAA` (שם `AB` אינה border כי $P[2]=B$). בשתי הטבלאות האחרות הערכים של $q=4$ ו-$q=5$ קטנים מדי, כי `AB` הוא border של `ABAB` ו-`ABA` הוא border של `ABABA`." },
      recap: "ל-ABABA הטבלה היא 0,0,1,2,3" },
    { id: "C01-Q4",
      question: "איזה משפט נכון לכל מחרוזת $P$ ולכל $q$ ?",
      options: [
        { id: "a", value: "$\\pi[q]<q$" },
        { id: "b", value: "$\\pi[q]\\ge\\pi[q-1]$, כלומר הטבלה לא יורדת לעולם" },
        { id: "c", value: "אם אות מסוימת מופיעה ב-$P$ פעמיים, אז $\\pi[m]\\ge 1$" },
        { id: "d", value: "$\\pi[q]=q-1$ לכל $q\\ge 2$" }],
      correctId: "a",
      explanation: "ה-border אמיתי, ולכן קצר מהרישא: $\\pi[q]<q$. הטענה על טבלה שלא יורדת שגויה: ל-`AAB` הטבלה היא $0,1,0$. הטענה על אות שחוזרת שגויה: ל-`ABB` הטבלה היא $0,0,0$ ו-$\\pi[3]=0$. הטענה על $q-1$ שגויה: ל-`AB` הטבלה היא $0,0$.",
      recap: "הכלל היחיד שתמיד נכון: π[q] < q" },
    { id: "C01-Q5",
      step: { type: "numeric", prompt: "עבור $P=$`AAAAA` מה הערך של $\\pi[5]$ ?", answer: 4, tol: 0,
              explain: "הרישא `AAAA` היא גם סיפא של `AAAAA`, והיא רישא אמיתית באורך 4. אי אפשר 5, כי זו המחרוזת עצמה. בכלל, ל-$P=a^m$ מתקבל $\\pi[m]=m-1$." },
      recap: "למחרוזת של m פעמים a: π[m] = m−1" },
  ],
});
