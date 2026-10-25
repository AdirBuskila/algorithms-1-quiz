/* graph_search, level 5 - topological sort and cycles (ai-verified: tools/verify/needhelp/graph_search/check.py) */
COURSE_LEVEL("graph_search", {
  id: "C05", order: 5, icon: "⛓️", title: "מיון טופולוגי ומעגלים",
  goal: "למיין גרף מכוון חסר מעגלים לפי זמני סיום, לבדוק אם סדר נתון תקין, ולזהות מתי אין מיון בכלל.",
  boss: false,
  source: "ai-verified",
  lesson: { html: String.raw`
<p>גרף מכוון <b>חסר מעגלים</b> נקרא DAG. <b>מיון טופולוגי</b> של DAG הוא סידור של כל הקודקודים בשורה כך שלכל צלע $(u,v)$ הקודקוד $u$ מופיע <b>לפני</b> $v$. כך מתארים סדרי תלות: קורס לפני הקורס שדורש אותו, מוצר לפני מה שמורכב ממנו.</p>
<h3>האלגוריתם</h3>
<ol>
<li>מריצים DFS על כל הגרף ורושמים זמני סיום $f[v]$.</li>
<li>מסדרים את הקודקודים לפי <b>זמן סיום יורד</b>: הקודקוד שסיים אחרון ראשון בשורה.</li>
</ol>
<p>הסיבה: לכל צלע $(u,v)$ ב-DAG מתקיים $f[u]>f[v]$ (הצלע היא עץ, קדימה או חוצה, אף פעם לא אחורה), ולכן $u$ מופיע לפני $v$. זמן הריצה $O(|V|+|E|)$.</p>
<div class="lesson-ex"><b>דוגמה.</b> ה-DAG עם הצלעות A→B, A→D, B→C, D→C, D→E, F→E. ריצת DFS אלפביתית נותנת זמני סיום $f[C]=4,\ f[B]=5,\ f[E]=8,\ f[D]=9,\ f[A]=10,\ f[F]=12$. בסדר יורד: F, A, D, E, B, C.
<div class="graph-fig" data-graph='{"directed": true, "algo": "topo", "caption": "מיון טופולוגי", "nodes": ["A", "B", "C", "D", "E", "F"], "edges": [{"u": "A", "v": "B"}, {"u": "A", "v": "D"}, {"u": "B", "v": "C"}, {"u": "D", "v": "C"}, {"u": "D", "v": "E"}, {"u": "F", "v": "E"}], "expect": {"topo": ["F", "A", "D", "E", "B", "C"], "fin": {"C": 4, "B": 5, "E": 8, "D": 9, "A": 10, "F": 12}}}'></div>
</div>
<h3>מה חשוב לזכור</h3>
<div class="lesson-rule">🔑 המיון <b>אינו יחיד</b>. סדר שכנים אחר או סדר שורשים אחר נותן סדר אחר ותקין. כדי לבדוק סדר נתון בודקים כל צלע: ההתחלה שלה חייבת להופיע לפני הסוף.</div>
<div class="lesson-rule">🔑 לגרף מכוון יש מיון טופולוגי אם ורק אם הוא <b>חסר מעגלים</b>, כלומר אם ורק אם DFS לא מוצא בו צלע אחורה. מעגל $a\to b\to c\to a$ דורש ש-$a$ לפני $b$, $b$ לפני $c$ ו-$c$ לפני $a$, וזה בלתי אפשרי.</div>
<div class="lesson-trap">⚠️ מוסיפים צלע חדשה ל-DAG: היא יוצרת מעגל בדיוק כשכבר יש מסלול מסוף הצלע להתחלתה. הוספת צלע "נגד הכיוון" בין שני קודקודים שאין ביניהם מסלול לא יוצרת מעגל.</div>
` },
  questions: [
    { id: "C05-Q1",
      step: { type: "text", normalize: "lower", key: "topo",
        prompt: String.raw`ב-DAG עם הצלעות $A\to B,\ A\to D,\ B\to C,\ D\to C,\ D\to E,\ F\to E$ מריצים DFS (שכנים והלולאה החיצונית בסדר אלפביתי) ומסדרים לפי זמן סיום יורד. מהו המיון הטופולוגי המתקבל? כתבו את האותיות מופרדות בפסיקים.`,
        accept: ["F, A, D, E, B, C", "F,A,D,E,B,C", "F A D E B C"],
        graph: { nodes: ["A", "B", "C", "D", "E", "F"], directed: true, algo: "topo",
          edges: [{ u: "A", v: "B" }, { u: "A", v: "D" }, { u: "B", v: "C" }, { u: "D", v: "C" }, { u: "D", v: "E" }, { u: "F", v: "E" }] },
        explain: String.raw`DFS מ-$A$: $A,B,C$ (C מסתיים 4, B מסתיים 5), אחר כך $D$ מגלה את $E$ ($E$ מסתיים 8, $D$ מסתיים 9), ו-$A$ מסתיים 10. $F$ שורש חדש ומסתיים 12. הסדר היורד של זמני הסיום: $F(12),A(10),D(9),E(8),B(5),C(4)$.` },
      recap: "מיון טופולוגי = זמן סיום יורד" },
    { id: "C05-Q2", question: String.raw`ל-DAG עם הצלעות $A\to B,\ A\to D,\ B\to C,\ D\to C,\ D\to E,\ F\to E$ מוצעים ארבעה סדרים. איזה מהם הוא מיון טופולוגי תקין?`,
      options: [
        { id: "a", value: "A, B, F, D, C, E" },
        { id: "b", value: "A, B, C, D, E, F" },
        { id: "c", value: "A, D, B, C, E, F" },
        { id: "d", value: "B, A, F, D, C, E" }],
      correctId: "a",
      explanation: String.raw`בסדר התקין כל צלע הולכת קדימה: $A$ לפני $B$ ו-$D$, $B$ ו-$D$ לפני $C$, $D$ ו-$F$ לפני $E$. הסדר שמתחיל ב-$A,B,C,D$ שובר את $D\to C$ ($C$ לפני $D$). הסדר שמסיים ב-$E,F$ שובר את $F\to E$. הסדר שמתחיל ב-$B,A$ שובר את $A\to B$.`,
      recap: "בודקים כל צלע: ההתחלה לפני הסוף",
      graph: { nodes: ["A", "B", "C", "D", "E", "F"], directed: true,
        edges: [{ u: "A", v: "B" }, { u: "A", v: "D" }, { u: "B", v: "C" }, { u: "D", v: "C" }, { u: "D", v: "E" }, { u: "F", v: "E" }] } },
    { id: "C05-Q3",
      step: { type: "numeric", answer: 9, tol: 0, key: "fin.D",
        prompt: String.raw`באותו DAG ובאותה ריצת DFS (סדר אלפביתי): מהו זמן הסיום $f[D]$?`,
        graph: { nodes: ["A", "B", "C", "D", "E", "F"], directed: true, algo: "topo",
          edges: [{ u: "A", v: "B" }, { u: "A", v: "D" }, { u: "B", v: "C" }, { u: "D", v: "C" }, { u: "D", v: "E" }, { u: "F", v: "E" }] },
        explain: String.raw`$A$ מתגלה ב-1, $B$ ב-2, $C$ ב-3 ומסתיים ב-4, $B$ מסתיים ב-5. $D$ מתגלה ב-6 (הצלע $D\to C$ מוצאת את $C$ שחור), $E$ ב-7 ומסתיים ב-8, ו-$D$ מסתיים ב-9.` },
      recap: "זמני סיום: הפנימי מסיים לפני החיצוני" },
    { id: "C05-Q4",
      step: { type: "numeric", answer: 8, tol: 0,
        prompt: String.raw`כמה מיונים טופולוגיים שונים יש ל-DAG עם הצלעות $A\to B,\ A\to C,\ B\to D,\ C\to D,\ E\to D$?`,
        graph: { nodes: ["A", "B", "C", "D", "E"], directed: true,
          edges: [{ u: "A", v: "B" }, { u: "A", v: "C" }, { u: "B", v: "D" }, { u: "C", v: "D" }, { u: "E", v: "D" }] },
        explain: String.raw`$D$ חייב להיות אחרון (כולם מובילים אליו). נשארים $A,B,C,E$ עם האילוץ ש-$A$ לפני $B$ ולפני $C$. מבין $4!=24$ הסידורים של $A,B,C,E$, ב-$A$ הוא הראשון מבין $A,B,C$ בשליש מהם: $24/3=8$.` },
      recap: "מיון טופולוגי אינו יחיד: סופרים סידורים שמכבדים את הצלעות" },
    { id: "C05-Q5", question: String.raw`ל-DAG עם הצלעות $A\to B,\ A\to D,\ B\to C,\ D\to C,\ D\to E,\ F\to E$ מוסיפים צלע אחת. איזו הוספה יוצרת מעגל, כך שלא יהיה עוד מיון טופולוגי?`,
      options: [
        { id: "a", value: String.raw`$C\to A$` },
        { id: "b", value: String.raw`$B\to D$` },
        { id: "c", value: String.raw`$F\to A$` },
        { id: "d", value: String.raw`$E\to B$` }],
      correctId: "a",
      explanation: String.raw`$C\to A$ סוגרת את המעגל $A\to B\to C\to A$, כי כבר יש מסלול מ-$A$ אל $C$. $B\to D$: אין מסלול מ-$D$ אל $B$, ולכן אין מעגל. $F\to A$: אין מסלול מ-$A$ אל $F$. $E\to B$: מ-$B$ אפשר להגיע רק אל $C$, ולא אל $E$.`,
      recap: String.raw`צלע $u\to v$ יוצרת מעגל אם ורק אם כבר יש מסלול מ-$v$ ל-$u$`,
      graph: { nodes: ["A", "B", "C", "D", "E", "F"], directed: true,
        edges: [{ u: "A", v: "B" }, { u: "A", v: "D" }, { u: "B", v: "C" }, { u: "D", v: "C" }, { u: "D", v: "E" }, { u: "F", v: "E" }] } },
    { id: "C05-Q6", question: "ריצת DFS על גרף מכוון מצאה צלע אחורה. מה מסיקים?",
      options: [
        { id: "a", value: "יש בגרף מעגל מכוון, ולכן אין לו מיון טופולוגי" },
        { id: "b", value: "יש מיון טופולוגי, אבל הוא אינו יחיד" },
        { id: "c", value: "אפשר לתקן את המיון אם מתעלמים מהצלע האחורה, והסדר נשאר תקין" },
        { id: "d", value: "הגרף אינו קשיר" }],
      correctId: "a",
      explanation: String.raw`צלע אחורה $(u,v)$ מחברת את $u$ לאב קדמון $v$, ויחד עם מסלול העץ מ-$v$ אל $u$ היא סוגרת מעגל מכוון. בגרף עם מעגל אין מיון טופולוגי. התעלמות מהצלע משנה את הגרף ואינה נותנת מיון שלו. ומעגל אינו קשור לקשירות.`,
      recap: "צלע אחורה ← מעגל ← אין מיון טופולוגי" },
  ],
});
