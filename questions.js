window.OPEN_BANK = {
 "meta": {
  "course": {
   "slug": "algorithms-1",
   "title": "אלגוריתמים 1",
   "description": "תרגול מבחנים - אלגוריתמים 1",
   "accent": "#c4b5fd",
   "accent2": "#7c3aed",
   "storePrefix": "algorithms-1",
   "needHelp": [
    {
     "id": "dp_ladder",
     "titleHe": "תכנות דינמי: מנוסחת נסיגה לאלגוריתם",
     "icon": "🧩",
     "topic": "dp_sequences",
     "entryLabelHe": "צריך עזרה בתכנות דינמי?"
    },
    {
     "id": "greedy_proofs",
     "titleHe": "אלגוריתם חמדן והוכחת נכונות",
     "icon": "🎯",
     "topic": "greedy",
     "entryLabelHe": "צריך עזרה באלגוריתמים חמדניים?"
    },
    {
     "id": "kmp_prefix",
     "titleHe": "KMP ופונקציית רישא",
     "icon": "🔤",
     "topic": "kmp_strings",
     "entryLabelHe": "צריך עזרה ב-KMP?"
    },
    {
     "id": "graph_search",
     "titleHe": "גרפים: BFS, DFS וטענות על גרפים",
     "icon": "🕸️",
     "topic": "graphs_search",
     "entryLabelHe": "צריך עזרה בגרפים?"
    }
   ]
  },
  "topics": [
   {
    "key": "complexity_recurrence",
    "label": "סיבוכיות ונוסחאות נסיגה"
   },
   {
    "key": "divide_conquer",
    "label": "הפרד ומשול ו-Select"
   },
   {
    "key": "dp_sequences",
    "label": "תכנות דינמי: סדרות ותת-סדרות"
   },
   {
    "key": "dp_optimization",
    "label": "תכנות דינמי: תרמיל, מסלולים ומטריצות"
   },
   {
    "key": "graphs_search",
    "label": "גרפים: ייצוג, BFS ו-DFS"
   },
   {
    "key": "graph_proofs",
    "label": "גרפים: טענות והוכחות"
   },
   {
    "key": "mst",
    "label": "עצים פורשים מינימליים"
   },
   {
    "key": "greedy",
    "label": "אלגוריתמים חמדניים"
   },
   {
    "key": "huffman",
    "label": "קוד הופמן"
   },
   {
    "key": "randomized",
    "label": "אלגוריתמים הסתברותיים"
   },
   {
    "key": "kmp_strings",
    "label": "מחרוזות: KMP ופונקציית רישא"
   },
   {
    "key": "suffix_structures",
    "label": "עצי סיפות ומערכי סיפות"
   },
   {
    "key": "approximation",
    "label": "אלגוריתמי קירוב"
   }
  ],
  "kinds": [
   "computation",
   "proof",
   "algorithm",
   "truefalse"
  ],
  "built": "2026-10-18T19:25:10Z",
  "exams": [
   {
    "examCode": "26A-A",
    "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
    "year": 2026,
    "source": "exam",
    "examDate": "2.02.2026"
   }
  ],
  "counts": {
   "total": 13,
   "contexts": 3,
   "math": 102,
   "steps": 0
  }
 },
 "contexts": {
  "26A-A-c1": {
   "kind": "text",
   "title": "שאלה 1: בעיית המשימות",
   "text": "להלן בעיית הזמן המינימלי לסיום משימות ללא דילוג על משימות עוקבות:\n**קלט:** מערך $A$ בגודל $n$ כאשר $A[i]$ לכל $0\\le i\\le n-1$ הוא זמן משך הביצוע של משימה $i$.\n**פלט:** הזמן המינימלי הנדרש לביצוע המשימות שנבחרו ממערך $A$.\nשימו לב: **מותר לדלג על משימות**, אך **אסור לדלג על שתי משימות (או יותר) ברצף**.\n**דוגמאות:**\nקלט: $A=[10,5,7,10]$, פלט: $12$. הסבר: נבחרו המשימות באינדקסים $1,2$.\nקלט: $A=[10,5,2,4,8,6,7,10]$, פלט: $22$. הסבר: נבחרו המשימות באינדקסים $1,3,5,6$.",
   "id": "26A-A-c1",
   "textHtml": "להלן בעיית הזמן המינימלי לסיום משימות ללא דילוג על משימות עוקבות:<br><strong>קלט:</strong> מערך <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi></mrow><annotation encoding=\"application/x-tex\">A</annotation></semantics></math></span> בגודל <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>n</mi></mrow><annotation encoding=\"application/x-tex\">n</annotation></semantics></math></span> כאשר <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi><mo stretchy=\"false\">[</mo><mi>i</mi><mo stretchy=\"false\">]</mo></mrow><annotation encoding=\"application/x-tex\">A[i]</annotation></semantics></math></span> לכל <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>0</mn><mo>≤</mo><mi>i</mi><mo>≤</mo><mi>n</mi><mo>−</mo><mn>1</mn></mrow><annotation encoding=\"application/x-tex\">0\\le i\\le n-1</annotation></semantics></math></span> הוא זמן משך הביצוע של משימה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>i</mi></mrow><annotation encoding=\"application/x-tex\">i</annotation></semantics></math></span>.<br><strong>פלט:</strong> הזמן המינימלי הנדרש לביצוע המשימות שנבחרו ממערך <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi></mrow><annotation encoding=\"application/x-tex\">A</annotation></semantics></math></span>.<br>שימו לב: <strong>מותר לדלג על משימות</strong>, אך <strong>אסור לדלג על שתי משימות (או יותר) ברצף</strong>.<br><strong>דוגמאות:</strong><br>קלט: <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi><mo>=</mo><mo stretchy=\"false\">[</mo><mn>10</mn><mo separator=\"true\">,</mo><mn>5</mn><mo separator=\"true\">,</mo><mn>7</mn><mo separator=\"true\">,</mo><mn>10</mn><mo stretchy=\"false\">]</mo></mrow><annotation encoding=\"application/x-tex\">A=[10,5,7,10]</annotation></semantics></math></span>, פלט: <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>12</mn></mrow><annotation encoding=\"application/x-tex\">12</annotation></semantics></math></span>. הסבר: נבחרו המשימות באינדקסים <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>1</mn><mo separator=\"true\">,</mo><mn>2</mn></mrow><annotation encoding=\"application/x-tex\">1,2</annotation></semantics></math></span>.<br>קלט: <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi><mo>=</mo><mo stretchy=\"false\">[</mo><mn>10</mn><mo separator=\"true\">,</mo><mn>5</mn><mo separator=\"true\">,</mo><mn>2</mn><mo separator=\"true\">,</mo><mn>4</mn><mo separator=\"true\">,</mo><mn>8</mn><mo separator=\"true\">,</mo><mn>6</mn><mo separator=\"true\">,</mo><mn>7</mn><mo separator=\"true\">,</mo><mn>10</mn><mo stretchy=\"false\">]</mo></mrow><annotation encoding=\"application/x-tex\">A=[10,5,2,4,8,6,7,10]</annotation></semantics></math></span>, פלט: <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>22</mn></mrow><annotation encoding=\"application/x-tex\">22</annotation></semantics></math></span>. הסבר: נבחרו המשימות באינדקסים <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>1</mn><mo separator=\"true\">,</mo><mn>3</mn><mo separator=\"true\">,</mo><mn>5</mn><mo separator=\"true\">,</mo><mn>6</mn></mrow><annotation encoding=\"application/x-tex\">1,3,5,6</annotation></semantics></math></span>.",
   "titleHtml": "שאלה 1: בעיית המשימות"
  },
  "26A-A-c2": {
   "kind": "text",
   "title": "שאלה 2: צלעות מיוחדות בגרף מלא",
   "text": "תזכורת מקורס בדידה - הגדרת גרף מלא לא מכוון: נאמר כי $G$ גרף לא מכוון מלא אם קיימת קשת בין כל זוג קודקודים שונים בגרף, ז\"א, לכל $u,v\\in V$ מתקיים $\\{u,v\\}\\in E$.\nיהי $G=(V,E)$ גרף לא מכוון מלא עם משקלי צלעות שהם מספרים שלמים חיוביים וייחודיים, ז\"א לכל $e\\in E$ מתקיים $w(e)>0$ וגם לכל $e_1,e_2\\in E$ מתקיים שאם $e_1\\neq e_2$ אזי $w(e_1)\\neq w(e_2)$.\nנאמר שצלע $e=\\{u,v\\}\\in E$ היא **צלע מזערית של הקודקוד** $u$, אם המשקל שלה $w(e)$ הוא הקטן ביותר (המזערי) ביחס לכל הצלעות היוצאות מקודקוד $u$.\nנאמר שצלע $e=\\{u,v\\}\\in E$ היא **צלע מיוחדת**, אם מתקיימת אחת משתי האפשרויות הבאות: או שהצלע $e$ הינה צלע מזערית של $u$, או שהצלע $e$ הינה צלע מזערית של $v$.\nהוכיחו או הפריכו כל אחת מהטענות הבאות. נדרשת הוכחה מדויקת או לחלופין דוגמה נגדית של גרף עם מספר קודקודים גדול כרצוננו עם הסבר מפורט מדוע הוא מהווה דוגמה נגדית.",
   "id": "26A-A-c2",
   "textHtml": "תזכורת מקורס בדידה - הגדרת גרף מלא לא מכוון: נאמר כי <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>G</mi></mrow><annotation encoding=\"application/x-tex\">G</annotation></semantics></math></span> גרף לא מכוון מלא אם קיימת קשת בין כל זוג קודקודים שונים בגרף, ז\"א, לכל <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>u</mi><mo separator=\"true\">,</mo><mi>v</mi><mo>∈</mo><mi>V</mi></mrow><annotation encoding=\"application/x-tex\">u,v\\in V</annotation></semantics></math></span> מתקיים <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mo stretchy=\"false\">{</mo><mi>u</mi><mo separator=\"true\">,</mo><mi>v</mi><mo stretchy=\"false\">}</mo><mo>∈</mo><mi>E</mi></mrow><annotation encoding=\"application/x-tex\">\\{u,v\\}\\in E</annotation></semantics></math></span>.<br>יהי <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>G</mi><mo>=</mo><mo stretchy=\"false\">(</mo><mi>V</mi><mo separator=\"true\">,</mo><mi>E</mi><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">G=(V,E)</annotation></semantics></math></span> גרף לא מכוון מלא עם משקלי צלעות שהם מספרים שלמים חיוביים וייחודיים, ז\"א לכל <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi><mo>∈</mo><mi>E</mi></mrow><annotation encoding=\"application/x-tex\">e\\in E</annotation></semantics></math></span> מתקיים <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>w</mi><mo stretchy=\"false\">(</mo><mi>e</mi><mo stretchy=\"false\">)</mo><mo>&gt;</mo><mn>0</mn></mrow><annotation encoding=\"application/x-tex\">w(e)&gt;0</annotation></semantics></math></span> וגם לכל <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><msub><mi>e</mi><mn>1</mn></msub><mo separator=\"true\">,</mo><msub><mi>e</mi><mn>2</mn></msub><mo>∈</mo><mi>E</mi></mrow><annotation encoding=\"application/x-tex\">e_1,e_2\\in E</annotation></semantics></math></span> מתקיים שאם <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><msub><mi>e</mi><mn>1</mn></msub><mo mathvariant=\"normal\">≠</mo><msub><mi>e</mi><mn>2</mn></msub></mrow><annotation encoding=\"application/x-tex\">e_1\\neq e_2</annotation></semantics></math></span> אזי <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>w</mi><mo stretchy=\"false\">(</mo><msub><mi>e</mi><mn>1</mn></msub><mo stretchy=\"false\">)</mo><mo mathvariant=\"normal\">≠</mo><mi>w</mi><mo stretchy=\"false\">(</mo><msub><mi>e</mi><mn>2</mn></msub><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">w(e_1)\\neq w(e_2)</annotation></semantics></math></span>.<br>נאמר שצלע <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi><mo>=</mo><mo stretchy=\"false\">{</mo><mi>u</mi><mo separator=\"true\">,</mo><mi>v</mi><mo stretchy=\"false\">}</mo><mo>∈</mo><mi>E</mi></mrow><annotation encoding=\"application/x-tex\">e=\\{u,v\\}\\in E</annotation></semantics></math></span> היא <strong>צלע מזערית של הקודקוד</strong> <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>u</mi></mrow><annotation encoding=\"application/x-tex\">u</annotation></semantics></math></span>, אם המשקל שלה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>w</mi><mo stretchy=\"false\">(</mo><mi>e</mi><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">w(e)</annotation></semantics></math></span> הוא הקטן ביותר (המזערי) ביחס לכל הצלעות היוצאות מקודקוד <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>u</mi></mrow><annotation encoding=\"application/x-tex\">u</annotation></semantics></math></span>.<br>נאמר שצלע <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi><mo>=</mo><mo stretchy=\"false\">{</mo><mi>u</mi><mo separator=\"true\">,</mo><mi>v</mi><mo stretchy=\"false\">}</mo><mo>∈</mo><mi>E</mi></mrow><annotation encoding=\"application/x-tex\">e=\\{u,v\\}\\in E</annotation></semantics></math></span> היא <strong>צלע מיוחדת</strong>, אם מתקיימת אחת משתי האפשרויות הבאות: או שהצלע <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi></mrow><annotation encoding=\"application/x-tex\">e</annotation></semantics></math></span> הינה צלע מזערית של <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>u</mi></mrow><annotation encoding=\"application/x-tex\">u</annotation></semantics></math></span>, או שהצלע <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi></mrow><annotation encoding=\"application/x-tex\">e</annotation></semantics></math></span> הינה צלע מזערית של <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>v</mi></mrow><annotation encoding=\"application/x-tex\">v</annotation></semantics></math></span>.<br>הוכיחו או הפריכו כל אחת מהטענות הבאות. נדרשת הוכחה מדויקת או לחלופין דוגמה נגדית של גרף עם מספר קודקודים גדול כרצוננו עם הסבר מפורט מדוע הוא מהווה דוגמה נגדית.",
   "titleHtml": "שאלה 2: צלעות מיוחדות בגרף מלא"
  },
  "26A-A-c4": {
   "kind": "text",
   "title": "שאלה 4: המספר החסר ה-k",
   "text": "בהינתן מערך $A$ ממוין של מספרים שלמים חיוביים ושונים, יש למצוא את המספר החיובי ה-$k$-י החסר במערך.\n**דוגמה:** קלט: $A=[2,3,4,7,11]$, $k=5$. פלט: $9$.\nהסבר: המספרים החסרים הם $1,5,6,8,9,10,\\ldots$ והמספר החסר החמישי הוא $9$.",
   "id": "26A-A-c4",
   "textHtml": "בהינתן מערך <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi></mrow><annotation encoding=\"application/x-tex\">A</annotation></semantics></math></span> ממוין של מספרים שלמים חיוביים ושונים, יש למצוא את המספר החיובי ה-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>k</mi></mrow><annotation encoding=\"application/x-tex\">k</annotation></semantics></math></span>-י החסר במערך.<br><strong>דוגמה:</strong> קלט: <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi><mo>=</mo><mo stretchy=\"false\">[</mo><mn>2</mn><mo separator=\"true\">,</mo><mn>3</mn><mo separator=\"true\">,</mo><mn>4</mn><mo separator=\"true\">,</mo><mn>7</mn><mo separator=\"true\">,</mo><mn>11</mn><mo stretchy=\"false\">]</mo></mrow><annotation encoding=\"application/x-tex\">A=[2,3,4,7,11]</annotation></semantics></math></span>, <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>k</mi><mo>=</mo><mn>5</mn></mrow><annotation encoding=\"application/x-tex\">k=5</annotation></semantics></math></span>. פלט: <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>9</mn></mrow><annotation encoding=\"application/x-tex\">9</annotation></semantics></math></span>.<br>הסבר: המספרים החסרים הם <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>1</mn><mo separator=\"true\">,</mo><mn>5</mn><mo separator=\"true\">,</mo><mn>6</mn><mo separator=\"true\">,</mo><mn>8</mn><mo separator=\"true\">,</mo><mn>9</mn><mo separator=\"true\">,</mo><mn>10</mn><mo separator=\"true\">,</mo><mo>…</mo></mrow><annotation encoding=\"application/x-tex\">1,5,6,8,9,10,\\ldots</annotation></semantics></math></span> והמספר החסר החמישי הוא <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>9</mn></mrow><annotation encoding=\"application/x-tex\">9</annotation></semantics></math></span>.",
   "titleHtml": "שאלה 4: המספר החסר ה-k"
  }
 },
 "questions": [
  {
   "num": 1,
   "kind": "computation",
   "topic": "dp_optimization",
   "question": "מה הפלט של הקלט הבא: $A=[10]$? נמקו תשובתכם.",
   "solution": "**פתרון רשמי** (26A-A פתרון עמ' 2):\n$0$. לפי הגדרת השאלה, ניתן לדלג על המשימה.",
   "solutionSource": "official-pdf",
   "official": true,
   "confidence": "high",
   "part": "א",
   "points": 5,
   "contextId": "26A-A-c1",
   "id": "26A-A-Q1a",
   "partKey": "a",
   "examCode": "26A-A",
   "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
   "year": 2026,
   "source": "exam",
   "topicLabel": "תכנות דינמי: תרמיל, מסלולים ומטריצות",
   "questionHtml": "מה הפלט של הקלט הבא: <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi><mo>=</mo><mo stretchy=\"false\">[</mo><mn>10</mn><mo stretchy=\"false\">]</mo></mrow><annotation encoding=\"application/x-tex\">A=[10]</annotation></semantics></math></span>? נמקו תשובתכם.",
   "solutionHtml": "<strong>פתרון רשמי</strong> (26A-A פתרון עמ' 2):<br><span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>0</mn></mrow><annotation encoding=\"application/x-tex\">0</annotation></semantics></math></span>. לפי הגדרת השאלה, ניתן לדלג על המשימה.",
   "pointsTotal": 5
  },
  {
   "num": 1,
   "kind": "algorithm",
   "topic": "dp_optimization",
   "question": "כתבו נוסחה רקורסיבית לפתרון הבעיה. שימו לב גם לציין את מקרי הבסיס של הנוסחה. נמקו תשובתכם.",
   "solution": "**פתרון רשמי** (26A-A פתרון עמ' 2-3):\nנגדיר $T(i)$ - סכום מינימלי של תת-סדרה ללא דילוג על משימות עוקבות המסתיימת במשימה $i$:\n$$T(i)=\\begin{cases}0 & ;\\ i<0\\\\ A[i]+\\min\\bigl(T(i-1),T(i-2)\\bigr) & ;\\ \\text{else}\\end{cases}$$\nלפי הגדרת הנוסחה, אם אין משימות, הפתרון הוא $0$.\nבכל מקרה אחר, אנו בוחרים את המשימה $i$ ופותרים את תת-הבעיה ללא דילוג $(i-1)$ או דילוג בצעד אחד $(i-2)$. לפי נוסחה זו, אנו יוצאים מנקודת הנחה כי האיבר במקום ה-$i$ הוא חלק מתוך תת-סדרת המשימות.\nאם תת-סדרה מסתיימת במשימה $i$, אז האיבר לפני האחרון הוא איבר $i-1$ או $i-2$, לכן:\n$$\\min\\bigl(T(n-1),T(n-2)\\bigr)$$\n**פתרון נוסף:**\nנגדיר $T(i,c)$ - כזמן המינימלי הנדרש להשלמת המשימות מאינדקס $i$ ועד $0$, כאשר $c$ דגל המציין את חופש הבחירה לגבי משימה $i$:\n- אם $c=1$: ניתן לדלג על משימה $i$.\n- אם $c=0$: חובה לבצע את המשימה $i$.\n\n$$T(i,c)=\\begin{cases}0 & ;\\ i<0\\\\ A[i]+T(i-1,1) & ;\\ c=0\\\\ \\min\\bigl(A[i]+T(i-1,1),\\,T(i-1,0)\\bigr) & ;\\ c=1\\end{cases}$$\nהסבר: אם בחרנו משימה $A[i]$ אז המשימה הקודמת לא חייבת להיות נבחרת $T(i-1,1)$, אך אם לא בחרנו $A[i]$ אז המשימה הקודמת חייבת להיות בתוך הפתרון $T(i-1,0)$.\nפתרון הבעיה בקריאה: $T(n-1,1)$.",
   "solutionSource": "official-pdf",
   "official": true,
   "confidence": "high",
   "part": "ב",
   "points": 15,
   "contextId": "26A-A-c1",
   "id": "26A-A-Q1b",
   "partKey": "b",
   "examCode": "26A-A",
   "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
   "year": 2026,
   "source": "exam",
   "topicLabel": "תכנות דינמי: תרמיל, מסלולים ומטריצות",
   "questionHtml": "כתבו נוסחה רקורסיבית לפתרון הבעיה. שימו לב גם לציין את מקרי הבסיס של הנוסחה. נמקו תשובתכם.",
   "solutionHtml": "<strong>פתרון רשמי</strong> (26A-A פתרון עמ' 2-3):<br>נגדיר <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi><mo stretchy=\"false\">(</mo><mi>i</mi><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">T(i)</annotation></semantics></math></span> - סכום מינימלי של תת-סדרה ללא דילוג על משימות עוקבות המסתיימת במשימה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>i</mi></mrow><annotation encoding=\"application/x-tex\">i</annotation></semantics></math></span>:<br><span class=\"math-block\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\" display=\"block\"><semantics><mrow><mi>T</mi><mo stretchy=\"false\">(</mo><mi>i</mi><mo stretchy=\"false\">)</mo><mo>=</mo><mrow><mo fence=\"true\">{</mo><mtable rowspacing=\"0.36em\" columnalign=\"left left\" columnspacing=\"1em\"><mtr><mtd><mstyle scriptlevel=\"0\" displaystyle=\"false\"><mn>0</mn></mstyle></mtd><mtd><mstyle scriptlevel=\"0\" displaystyle=\"false\"><mrow><mo separator=\"true\">;</mo><mtext> </mtext><mi>i</mi><mo>&lt;</mo><mn>0</mn></mrow></mstyle></mtd></mtr><mtr><mtd><mstyle scriptlevel=\"0\" displaystyle=\"false\"><mrow><mi>A</mi><mo stretchy=\"false\">[</mo><mi>i</mi><mo stretchy=\"false\">]</mo><mo>+</mo><mi>min</mi><mo>⁡</mo><mo fence=\"true\" stretchy=\"true\" minsize=\"1.2em\" maxsize=\"1.2em\">(</mo><mi>T</mi><mo stretchy=\"false\">(</mo><mi>i</mi><mo>−</mo><mn>1</mn><mo stretchy=\"false\">)</mo><mo separator=\"true\">,</mo><mi>T</mi><mo stretchy=\"false\">(</mo><mi>i</mi><mo>−</mo><mn>2</mn><mo stretchy=\"false\">)</mo><mo fence=\"true\" stretchy=\"true\" minsize=\"1.2em\" maxsize=\"1.2em\">)</mo></mrow></mstyle></mtd><mtd><mstyle scriptlevel=\"0\" displaystyle=\"false\"><mrow><mo separator=\"true\">;</mo><mtext> else</mtext></mrow></mstyle></mtd></mtr></mtable></mrow></mrow><annotation encoding=\"application/x-tex\">T(i)=\\begin{cases}0 &amp; ;\\ i&lt;0\\\\ A[i]+\\min\\bigl(T(i-1),T(i-2)\\bigr) &amp; ;\\ \\text{else}\\end{cases}</annotation></semantics></math></span><br>לפי הגדרת הנוסחה, אם אין משימות, הפתרון הוא <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>0</mn></mrow><annotation encoding=\"application/x-tex\">0</annotation></semantics></math></span>.<br>בכל מקרה אחר, אנו בוחרים את המשימה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>i</mi></mrow><annotation encoding=\"application/x-tex\">i</annotation></semantics></math></span> ופותרים את תת-הבעיה ללא דילוג <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mo stretchy=\"false\">(</mo><mi>i</mi><mo>−</mo><mn>1</mn><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">(i-1)</annotation></semantics></math></span> או דילוג בצעד אחד <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mo stretchy=\"false\">(</mo><mi>i</mi><mo>−</mo><mn>2</mn><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">(i-2)</annotation></semantics></math></span>. לפי נוסחה זו, אנו יוצאים מנקודת הנחה כי האיבר במקום ה-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>i</mi></mrow><annotation encoding=\"application/x-tex\">i</annotation></semantics></math></span> הוא חלק מתוך תת-סדרת המשימות.<br>אם תת-סדרה מסתיימת במשימה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>i</mi></mrow><annotation encoding=\"application/x-tex\">i</annotation></semantics></math></span>, אז האיבר לפני האחרון הוא איבר <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>i</mi><mo>−</mo><mn>1</mn></mrow><annotation encoding=\"application/x-tex\">i-1</annotation></semantics></math></span> או <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>i</mi><mo>−</mo><mn>2</mn></mrow><annotation encoding=\"application/x-tex\">i-2</annotation></semantics></math></span>, לכן:<br><span class=\"math-block\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\" display=\"block\"><semantics><mrow><mi>min</mi><mo>⁡</mo><mo fence=\"true\" stretchy=\"true\" minsize=\"1.2em\" maxsize=\"1.2em\">(</mo><mi>T</mi><mo stretchy=\"false\">(</mo><mi>n</mi><mo>−</mo><mn>1</mn><mo stretchy=\"false\">)</mo><mo separator=\"true\">,</mo><mi>T</mi><mo stretchy=\"false\">(</mo><mi>n</mi><mo>−</mo><mn>2</mn><mo stretchy=\"false\">)</mo><mo fence=\"true\" stretchy=\"true\" minsize=\"1.2em\" maxsize=\"1.2em\">)</mo></mrow><annotation encoding=\"application/x-tex\">\\min\\bigl(T(n-1),T(n-2)\\bigr)</annotation></semantics></math></span><br><strong>פתרון נוסף:</strong><br>נגדיר <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi><mo stretchy=\"false\">(</mo><mi>i</mi><mo separator=\"true\">,</mo><mi>c</mi><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">T(i,c)</annotation></semantics></math></span> - כזמן המינימלי הנדרש להשלמת המשימות מאינדקס <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>i</mi></mrow><annotation encoding=\"application/x-tex\">i</annotation></semantics></math></span> ועד <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>0</mn></mrow><annotation encoding=\"application/x-tex\">0</annotation></semantics></math></span>, כאשר <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>c</mi></mrow><annotation encoding=\"application/x-tex\">c</annotation></semantics></math></span> דגל המציין את חופש הבחירה לגבי משימה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>i</mi></mrow><annotation encoding=\"application/x-tex\">i</annotation></semantics></math></span>:<br>- אם <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>c</mi><mo>=</mo><mn>1</mn></mrow><annotation encoding=\"application/x-tex\">c=1</annotation></semantics></math></span>: ניתן לדלג על משימה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>i</mi></mrow><annotation encoding=\"application/x-tex\">i</annotation></semantics></math></span>.<br>- אם <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>c</mi><mo>=</mo><mn>0</mn></mrow><annotation encoding=\"application/x-tex\">c=0</annotation></semantics></math></span>: חובה לבצע את המשימה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>i</mi></mrow><annotation encoding=\"application/x-tex\">i</annotation></semantics></math></span>.<br><br><span class=\"math-block\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\" display=\"block\"><semantics><mrow><mi>T</mi><mo stretchy=\"false\">(</mo><mi>i</mi><mo separator=\"true\">,</mo><mi>c</mi><mo stretchy=\"false\">)</mo><mo>=</mo><mrow><mo fence=\"true\">{</mo><mtable rowspacing=\"0.36em\" columnalign=\"left left\" columnspacing=\"1em\"><mtr><mtd><mstyle scriptlevel=\"0\" displaystyle=\"false\"><mn>0</mn></mstyle></mtd><mtd><mstyle scriptlevel=\"0\" displaystyle=\"false\"><mrow><mo separator=\"true\">;</mo><mtext> </mtext><mi>i</mi><mo>&lt;</mo><mn>0</mn></mrow></mstyle></mtd></mtr><mtr><mtd><mstyle scriptlevel=\"0\" displaystyle=\"false\"><mrow><mi>A</mi><mo stretchy=\"false\">[</mo><mi>i</mi><mo stretchy=\"false\">]</mo><mo>+</mo><mi>T</mi><mo stretchy=\"false\">(</mo><mi>i</mi><mo>−</mo><mn>1</mn><mo separator=\"true\">,</mo><mn>1</mn><mo stretchy=\"false\">)</mo></mrow></mstyle></mtd><mtd><mstyle scriptlevel=\"0\" displaystyle=\"false\"><mrow><mo separator=\"true\">;</mo><mtext> </mtext><mi>c</mi><mo>=</mo><mn>0</mn></mrow></mstyle></mtd></mtr><mtr><mtd><mstyle scriptlevel=\"0\" displaystyle=\"false\"><mrow><mi>min</mi><mo>⁡</mo><mo fence=\"true\" stretchy=\"true\" minsize=\"1.2em\" maxsize=\"1.2em\">(</mo><mi>A</mi><mo stretchy=\"false\">[</mo><mi>i</mi><mo stretchy=\"false\">]</mo><mo>+</mo><mi>T</mi><mo stretchy=\"false\">(</mo><mi>i</mi><mo>−</mo><mn>1</mn><mo separator=\"true\">,</mo><mn>1</mn><mo stretchy=\"false\">)</mo><mo separator=\"true\">,</mo><mtext> </mtext><mi>T</mi><mo stretchy=\"false\">(</mo><mi>i</mi><mo>−</mo><mn>1</mn><mo separator=\"true\">,</mo><mn>0</mn><mo stretchy=\"false\">)</mo><mo fence=\"true\" stretchy=\"true\" minsize=\"1.2em\" maxsize=\"1.2em\">)</mo></mrow></mstyle></mtd><mtd><mstyle scriptlevel=\"0\" displaystyle=\"false\"><mrow><mo separator=\"true\">;</mo><mtext> </mtext><mi>c</mi><mo>=</mo><mn>1</mn></mrow></mstyle></mtd></mtr></mtable></mrow></mrow><annotation encoding=\"application/x-tex\">T(i,c)=\\begin{cases}0 &amp; ;\\ i&lt;0\\\\ A[i]+T(i-1,1) &amp; ;\\ c=0\\\\ \\min\\bigl(A[i]+T(i-1,1),\\,T(i-1,0)\\bigr) &amp; ;\\ c=1\\end{cases}</annotation></semantics></math></span><br>הסבר: אם בחרנו משימה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi><mo stretchy=\"false\">[</mo><mi>i</mi><mo stretchy=\"false\">]</mo></mrow><annotation encoding=\"application/x-tex\">A[i]</annotation></semantics></math></span> אז המשימה הקודמת לא חייבת להיות נבחרת <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi><mo stretchy=\"false\">(</mo><mi>i</mi><mo>−</mo><mn>1</mn><mo separator=\"true\">,</mo><mn>1</mn><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">T(i-1,1)</annotation></semantics></math></span>, אך אם לא בחרנו <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi><mo stretchy=\"false\">[</mo><mi>i</mi><mo stretchy=\"false\">]</mo></mrow><annotation encoding=\"application/x-tex\">A[i]</annotation></semantics></math></span> אז המשימה הקודמת חייבת להיות בתוך הפתרון <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi><mo stretchy=\"false\">(</mo><mi>i</mi><mo>−</mo><mn>1</mn><mo separator=\"true\">,</mo><mn>0</mn><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">T(i-1,0)</annotation></semantics></math></span>.<br>פתרון הבעיה בקריאה: <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi><mo stretchy=\"false\">(</mo><mi>n</mi><mo>−</mo><mn>1</mn><mo separator=\"true\">,</mo><mn>1</mn><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">T(n-1,1)</annotation></semantics></math></span>.",
   "pointsTotal": 15
  },
  {
   "num": 1,
   "kind": "computation",
   "topic": "dp_optimization",
   "question": "מהי סיבוכיות זמן הריצה של אלגוריתם תכנון דינמי המבוסס על הנוסחה שכתבתם בסעיף ב', ומהי סיבוכיות המקום שלו?\nאין צורך לפרט את האלגוריתם עצמו.",
   "solution": "**פתרון רשמי** (26A-A פתרון עמ' 3):\n**סיבוכיות זמן:** יש $n$ תת-בעיות שונות (אחת לכל אינדקס). לכל תת-בעיה $dp[i]$ יש פתרון יחיד שמחושב פעם אחת בלבד. חישוב $dp[i]$ כולל פעולת $min$ אחת ובדיקה של שני ערכים קודמים בזמן קבוע, ולכן הזמן הכולל הוא $\\Theta(n)$.\n**סיבוכיות מקום:** ניתן להגיע לסיבוכיות מקום קבועה של $\\Theta(1)$ עבור חישוב הזמן המינימלי בלבד, וזאת על ידי שמירת שני הערכים האחרונים שחושבו בכל שלב (מכיוון שהחישוב הנוכחי תלוי רק בהם). אולם, במידה ונדרש **שחזור של הפתרון** (כלומר, זיהוי המשימות שנבחרו בפועל), עלינו לשמור את פתרונות כל תת-הבעיות במערך בגודל $n$, במקרה זה סיבוכיות המקום תהיה $\\Theta(n)$.",
   "solutionSource": "official-pdf",
   "official": true,
   "confidence": "high",
   "part": "ג",
   "points": 5,
   "contextId": "26A-A-c1",
   "id": "26A-A-Q1c",
   "partKey": "c",
   "examCode": "26A-A",
   "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
   "year": 2026,
   "source": "exam",
   "topicLabel": "תכנות דינמי: תרמיל, מסלולים ומטריצות",
   "questionHtml": "מהי סיבוכיות זמן הריצה של אלגוריתם תכנון דינמי המבוסס על הנוסחה שכתבתם בסעיף ב', ומהי סיבוכיות המקום שלו?<br>אין צורך לפרט את האלגוריתם עצמו.",
   "solutionHtml": "<strong>פתרון רשמי</strong> (26A-A פתרון עמ' 3):<br><strong>סיבוכיות זמן:</strong> יש <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>n</mi></mrow><annotation encoding=\"application/x-tex\">n</annotation></semantics></math></span> תת-בעיות שונות (אחת לכל אינדקס). לכל תת-בעיה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>d</mi><mi>p</mi><mo stretchy=\"false\">[</mo><mi>i</mi><mo stretchy=\"false\">]</mo></mrow><annotation encoding=\"application/x-tex\">dp[i]</annotation></semantics></math></span> יש פתרון יחיד שמחושב פעם אחת בלבד. חישוב <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>d</mi><mi>p</mi><mo stretchy=\"false\">[</mo><mi>i</mi><mo stretchy=\"false\">]</mo></mrow><annotation encoding=\"application/x-tex\">dp[i]</annotation></semantics></math></span> כולל פעולת <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>m</mi><mi>i</mi><mi>n</mi></mrow><annotation encoding=\"application/x-tex\">min</annotation></semantics></math></span> אחת ובדיקה של שני ערכים קודמים בזמן קבוע, ולכן הזמן הכולל הוא <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi mathvariant=\"normal\">Θ</mi><mo stretchy=\"false\">(</mo><mi>n</mi><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">\\Theta(n)</annotation></semantics></math></span>.<br><strong>סיבוכיות מקום:</strong> ניתן להגיע לסיבוכיות מקום קבועה של <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi mathvariant=\"normal\">Θ</mi><mo stretchy=\"false\">(</mo><mn>1</mn><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">\\Theta(1)</annotation></semantics></math></span> עבור חישוב הזמן המינימלי בלבד, וזאת על ידי שמירת שני הערכים האחרונים שחושבו בכל שלב (מכיוון שהחישוב הנוכחי תלוי רק בהם). אולם, במידה ונדרש <strong>שחזור של הפתרון</strong> (כלומר, זיהוי המשימות שנבחרו בפועל), עלינו לשמור את פתרונות כל תת-הבעיות במערך בגודל <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>n</mi></mrow><annotation encoding=\"application/x-tex\">n</annotation></semantics></math></span>, במקרה זה סיבוכיות המקום תהיה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi mathvariant=\"normal\">Θ</mi><mo stretchy=\"false\">(</mo><mi>n</mi><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">\\Theta(n)</annotation></semantics></math></span>.",
   "pointsTotal": 5
  },
  {
   "num": 2,
   "kind": "truefalse",
   "topic": "mst",
   "question": "אם הצלע $e$ שייכת לכל עץ פורש מינימלי $T$ של הגרף $G$ הנתון, אז הצלע $e$ הינה מיוחדת.",
   "solution": "**פתרון רשמי** (26A-A פתרון עמ' 4):\nהטענה לא נכונה.\nדוגמה נגדית, נתבונן בגרף מלא בעל 4 קודקודים $\\{A,B,C,D\\}$ עם משקלי הקשתות הבאים. העץ הפורש כולל את הקשתות הבאים:\n- $w(A,B)=1$ (מיוחדת ל-A ול-B).\n- $w(C,D)=2$ (מיוחדת ל-C ול-D).\n- $w(B,C)=3$ (צלע שאינה מיוחדת ל-B או ל-C).\n\n![דוגמה נגדית: גרף מלא על ארבעה קודקודים עם המשקלים 1 עד 6](images/exams/26A-A-Q2a-graph.png)\nראינו דוגמה לגרף שבו קיימת צלע השייכת ל-MST אך אינה צלע מיוחדת עבור אף אחד מקודקודיה, ולכן הטענה אינה נכונה באופן כללי.",
   "solutionSource": "official-pdf",
   "official": true,
   "confidence": "high",
   "part": "א",
   "points": 10,
   "contextId": "26A-A-c2",
   "verdict": false,
   "id": "26A-A-Q2a",
   "partKey": "a",
   "examCode": "26A-A",
   "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
   "year": 2026,
   "source": "exam",
   "topicLabel": "עצים פורשים מינימליים",
   "questionHtml": "אם הצלע <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi></mrow><annotation encoding=\"application/x-tex\">e</annotation></semantics></math></span> שייכת לכל עץ פורש מינימלי <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">T</annotation></semantics></math></span> של הגרף <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>G</mi></mrow><annotation encoding=\"application/x-tex\">G</annotation></semantics></math></span> הנתון, אז הצלע <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi></mrow><annotation encoding=\"application/x-tex\">e</annotation></semantics></math></span> הינה מיוחדת.",
   "solutionHtml": "<strong>פתרון רשמי</strong> (26A-A פתרון עמ' 4):<br>הטענה לא נכונה.<br>דוגמה נגדית, נתבונן בגרף מלא בעל 4 קודקודים <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mo stretchy=\"false\">{</mo><mi>A</mi><mo separator=\"true\">,</mo><mi>B</mi><mo separator=\"true\">,</mo><mi>C</mi><mo separator=\"true\">,</mo><mi>D</mi><mo stretchy=\"false\">}</mo></mrow><annotation encoding=\"application/x-tex\">\\{A,B,C,D\\}</annotation></semantics></math></span> עם משקלי הקשתות הבאים. העץ הפורש כולל את הקשתות הבאים:<br>- <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>w</mi><mo stretchy=\"false\">(</mo><mi>A</mi><mo separator=\"true\">,</mo><mi>B</mi><mo stretchy=\"false\">)</mo><mo>=</mo><mn>1</mn></mrow><annotation encoding=\"application/x-tex\">w(A,B)=1</annotation></semantics></math></span> (מיוחדת ל-A ול-B).<br>- <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>w</mi><mo stretchy=\"false\">(</mo><mi>C</mi><mo separator=\"true\">,</mo><mi>D</mi><mo stretchy=\"false\">)</mo><mo>=</mo><mn>2</mn></mrow><annotation encoding=\"application/x-tex\">w(C,D)=2</annotation></semantics></math></span> (מיוחדת ל-C ול-D).<br>- <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>w</mi><mo stretchy=\"false\">(</mo><mi>B</mi><mo separator=\"true\">,</mo><mi>C</mi><mo stretchy=\"false\">)</mo><mo>=</mo><mn>3</mn></mrow><annotation encoding=\"application/x-tex\">w(B,C)=3</annotation></semantics></math></span> (צלע שאינה מיוחדת ל-B או ל-C).<br><figure class=\"rt-fig\"><img src=\"images/exams/26A-A-Q2a-graph.png\" alt=\"דוגמה נגדית: גרף מלא על ארבעה קודקודים עם המשקלים 1 עד 6\" loading=\"lazy\"><figcaption>דוגמה נגדית: גרף מלא על ארבעה קודקודים עם המשקלים 1 עד 6</figcaption></figure>ראינו דוגמה לגרף שבו קיימת צלע השייכת ל-MST אך אינה צלע מיוחדת עבור אף אחד מקודקודיה, ולכן הטענה אינה נכונה באופן כללי.",
   "pointsTotal": 10
  },
  {
   "num": 2,
   "kind": "truefalse",
   "topic": "mst",
   "question": "אם הצלע $e\\in E$ בגרף $G$ הינה מיוחדת, אז הצלע $e$ שייכת לכל עץ פורש מינימלי $T$ של הגרף $G$.",
   "solution": "**פתרון רשמי** (26A-A פתרון עמ' 5):\nהטענה נכונה.\nלפני שנצלול אל ההוכחות עצמן, נבסס את עקרונות היסוד של השאלה:\n**עקרונות היסוד:**\nראשית, נתון כי הגרף הוא גרף מלא. תכונה זו מבטיחה כי כל צלע בגרף היא חלק ממעגל אחד לפחות, ולכן אף צלע אינה מהווה \"גשר\" (צלע שהסרתה מנתקת את הגרף). שנית, נתון כי לכל הקשתות משקלים שונים (ייחודיים). עובדה זו היא קריטית, שכן היא מבטיחה כי קיים עץ פורש מינימלי ($MST$) אחד ויחיד לגרף. אם נמצא צלע שחייבת להיות ב-$MST$ היא בהכרח תהיה ב-$MST$ היחיד הזה.\nלהלן שתי הדרכים להוכיח כי כל צלע מיוחדת שייכת ל-$MST$:\n**הוכחה 1: מבוססת על שיטת ההחלפה (Exchange Argument)**\nיהי $T$ עץ פורש מינימלי. נניח בשלילה כי קיימת צלע מיוחדת $e=\\{u,v\\}$ כך ש-$e\\notin T$. ונניח ללא הגבלת הכלליות שהיא הצלע בעלת המשקל המינימלי מבין כל הצלעות היוצאות מהקודקוד $u$. מכיוון ש-$T$ הוא עץ פורש, אם נוסיף לו את הצלע $e$ ייווצר בגרף מעגל יחיד $C$. בתוך המעגל הזה, לכל קודקוד יש בדיוק שתי צלעות מהמעגל שמחוברות אליו. לכן, עבור קודקוד $u$, קיימת צלע נוספת $e'\\in T$ השייכת למעגל $C$ ויוצאת מ-$u$. מכיוון שנתון ש-$e$ היא הצלע בעלת המשקל הקטן ביותר מבין כל הצלעות המחוברות ל-$u$, וכל המשקלים ייחודיים, הרי שמתקיים $w(e)<w(e')$. כעת נבנה עץ חדש $T'$ על ידי הוספת $e$ והסרת $e'$. הגרף שנוצר הוא עץ פורש (שכן הוספת צלע לעץ סוגרת מעגל, והסרת צלע אחרת מאותו המעגל מבטלת אותו ושומרת על הקשירות ועל מספר הצלעות $(n-1)$), אך משקלו הכולל קטן ממש ממשקלו של $T$ (שכן החלפנו צלע כבדה בצלע קלה יותר). זוהי סתירה לכך ש-$T$ הוא העץ הפורש המינימלי. לכן, ההנחה שגויה והצלע המיוחדת $e$ חייבת להיות ב-$MST$.\n**הוכחה 2: מבוססת על תכונת החתך (Cut Property)**\nנתבונן בצלע מיוחדת $e=\\{u,v\\}$, ונניח ללא הגבלת הכלליות שהיא הצלע בעלת המשקל המינימלי מבין כל הצלעות היוצאות מהקודקוד $u$. נגדיר חתך בגרף $(S,V\\setminus S)$ כך שקבוצה $S$ מכילה אך ורק את הקודקוד $u$ ($S=\\{u\\}$), והקבוצה המשלימה מכילה את כל שאר קודקודי הגרף. הצלעות ש\"חוצות\" את החתך הזה (כלומר, צלע שקצה אחד שלה ב-$S$ והשני ב-$V\\setminus S$) הן בדיוק כל הצלעות המחוברות לקודקוד $u$. על פי הנתון, הצלע $e=\\{u,v\\}$ היא בעלת המשקל המינימלי מבין כל הצלעות הללו, ולכן היא הצלע הקלה ביותר שחוצה את החתך. תכונת החתך קובעת כי עבור כל חתך בגרף, הצלע המינימלית החוצה אותו חייבת להיות שייכת לכל עץ פורש מינימלי. מכיוון ש-$e$ היא הצלע המינימלית בחתך שהגדרנו, היא חייבת להיות חלק מה-$MST$.",
   "solutionSource": "official-pdf",
   "official": true,
   "confidence": "high",
   "part": "ב",
   "points": 15,
   "contextId": "26A-A-c2",
   "verdict": true,
   "id": "26A-A-Q2b",
   "partKey": "b",
   "examCode": "26A-A",
   "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
   "year": 2026,
   "source": "exam",
   "topicLabel": "עצים פורשים מינימליים",
   "questionHtml": "אם הצלע <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi><mo>∈</mo><mi>E</mi></mrow><annotation encoding=\"application/x-tex\">e\\in E</annotation></semantics></math></span> בגרף <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>G</mi></mrow><annotation encoding=\"application/x-tex\">G</annotation></semantics></math></span> הינה מיוחדת, אז הצלע <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi></mrow><annotation encoding=\"application/x-tex\">e</annotation></semantics></math></span> שייכת לכל עץ פורש מינימלי <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">T</annotation></semantics></math></span> של הגרף <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>G</mi></mrow><annotation encoding=\"application/x-tex\">G</annotation></semantics></math></span>.",
   "solutionHtml": "<strong>פתרון רשמי</strong> (26A-A פתרון עמ' 5):<br>הטענה נכונה.<br>לפני שנצלול אל ההוכחות עצמן, נבסס את עקרונות היסוד של השאלה:<br><strong>עקרונות היסוד:</strong><br>ראשית, נתון כי הגרף הוא גרף מלא. תכונה זו מבטיחה כי כל צלע בגרף היא חלק ממעגל אחד לפחות, ולכן אף צלע אינה מהווה \"גשר\" (צלע שהסרתה מנתקת את הגרף). שנית, נתון כי לכל הקשתות משקלים שונים (ייחודיים). עובדה זו היא קריטית, שכן היא מבטיחה כי קיים עץ פורש מינימלי (<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>M</mi><mi>S</mi><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">MST</annotation></semantics></math></span>) אחד ויחיד לגרף. אם נמצא צלע שחייבת להיות ב-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>M</mi><mi>S</mi><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">MST</annotation></semantics></math></span> היא בהכרח תהיה ב-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>M</mi><mi>S</mi><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">MST</annotation></semantics></math></span> היחיד הזה.<br>להלן שתי הדרכים להוכיח כי כל צלע מיוחדת שייכת ל-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>M</mi><mi>S</mi><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">MST</annotation></semantics></math></span>:<br><strong>הוכחה 1: מבוססת על שיטת ההחלפה (Exchange Argument)</strong><br>יהי <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">T</annotation></semantics></math></span> עץ פורש מינימלי. נניח בשלילה כי קיימת צלע מיוחדת <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi><mo>=</mo><mo stretchy=\"false\">{</mo><mi>u</mi><mo separator=\"true\">,</mo><mi>v</mi><mo stretchy=\"false\">}</mo></mrow><annotation encoding=\"application/x-tex\">e=\\{u,v\\}</annotation></semantics></math></span> כך ש-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi><mo mathvariant=\"normal\">∉</mo><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">e\\notin T</annotation></semantics></math></span>. ונניח ללא הגבלת הכלליות שהיא הצלע בעלת המשקל המינימלי מבין כל הצלעות היוצאות מהקודקוד <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>u</mi></mrow><annotation encoding=\"application/x-tex\">u</annotation></semantics></math></span>. מכיוון ש-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">T</annotation></semantics></math></span> הוא עץ פורש, אם נוסיף לו את הצלע <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi></mrow><annotation encoding=\"application/x-tex\">e</annotation></semantics></math></span> ייווצר בגרף מעגל יחיד <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>C</mi></mrow><annotation encoding=\"application/x-tex\">C</annotation></semantics></math></span>. בתוך המעגל הזה, לכל קודקוד יש בדיוק שתי צלעות מהמעגל שמחוברות אליו. לכן, עבור קודקוד <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>u</mi></mrow><annotation encoding=\"application/x-tex\">u</annotation></semantics></math></span>, קיימת צלע נוספת <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><msup><mi>e</mi><mo mathvariant=\"normal\" lspace=\"0em\" rspace=\"0em\">′</mo></msup><mo>∈</mo><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">e&#x27;\\in T</annotation></semantics></math></span> השייכת למעגל <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>C</mi></mrow><annotation encoding=\"application/x-tex\">C</annotation></semantics></math></span> ויוצאת מ-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>u</mi></mrow><annotation encoding=\"application/x-tex\">u</annotation></semantics></math></span>. מכיוון שנתון ש-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi></mrow><annotation encoding=\"application/x-tex\">e</annotation></semantics></math></span> היא הצלע בעלת המשקל הקטן ביותר מבין כל הצלעות המחוברות ל-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>u</mi></mrow><annotation encoding=\"application/x-tex\">u</annotation></semantics></math></span>, וכל המשקלים ייחודיים, הרי שמתקיים <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>w</mi><mo stretchy=\"false\">(</mo><mi>e</mi><mo stretchy=\"false\">)</mo><mo>&lt;</mo><mi>w</mi><mo stretchy=\"false\">(</mo><msup><mi>e</mi><mo mathvariant=\"normal\" lspace=\"0em\" rspace=\"0em\">′</mo></msup><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">w(e)&lt;w(e&#x27;)</annotation></semantics></math></span>. כעת נבנה עץ חדש <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><msup><mi>T</mi><mo mathvariant=\"normal\" lspace=\"0em\" rspace=\"0em\">′</mo></msup></mrow><annotation encoding=\"application/x-tex\">T&#x27;</annotation></semantics></math></span> על ידי הוספת <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi></mrow><annotation encoding=\"application/x-tex\">e</annotation></semantics></math></span> והסרת <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><msup><mi>e</mi><mo mathvariant=\"normal\" lspace=\"0em\" rspace=\"0em\">′</mo></msup></mrow><annotation encoding=\"application/x-tex\">e&#x27;</annotation></semantics></math></span>. הגרף שנוצר הוא עץ פורש (שכן הוספת צלע לעץ סוגרת מעגל, והסרת צלע אחרת מאותו המעגל מבטלת אותו ושומרת על הקשירות ועל מספר הצלעות <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mo stretchy=\"false\">(</mo><mi>n</mi><mo>−</mo><mn>1</mn><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">(n-1)</annotation></semantics></math></span>), אך משקלו הכולל קטן ממש ממשקלו של <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">T</annotation></semantics></math></span> (שכן החלפנו צלע כבדה בצלע קלה יותר). זוהי סתירה לכך ש-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">T</annotation></semantics></math></span> הוא העץ הפורש המינימלי. לכן, ההנחה שגויה והצלע המיוחדת <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi></mrow><annotation encoding=\"application/x-tex\">e</annotation></semantics></math></span> חייבת להיות ב-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>M</mi><mi>S</mi><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">MST</annotation></semantics></math></span>.<br><strong>הוכחה 2: מבוססת על תכונת החתך (Cut Property)</strong><br>נתבונן בצלע מיוחדת <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi><mo>=</mo><mo stretchy=\"false\">{</mo><mi>u</mi><mo separator=\"true\">,</mo><mi>v</mi><mo stretchy=\"false\">}</mo></mrow><annotation encoding=\"application/x-tex\">e=\\{u,v\\}</annotation></semantics></math></span>, ונניח ללא הגבלת הכלליות שהיא הצלע בעלת המשקל המינימלי מבין כל הצלעות היוצאות מהקודקוד <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>u</mi></mrow><annotation encoding=\"application/x-tex\">u</annotation></semantics></math></span>. נגדיר חתך בגרף <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mo stretchy=\"false\">(</mo><mi>S</mi><mo separator=\"true\">,</mo><mi>V</mi><mo>∖</mo><mi>S</mi><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">(S,V\\setminus S)</annotation></semantics></math></span> כך שקבוצה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>S</mi></mrow><annotation encoding=\"application/x-tex\">S</annotation></semantics></math></span> מכילה אך ורק את הקודקוד <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>u</mi></mrow><annotation encoding=\"application/x-tex\">u</annotation></semantics></math></span> (<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>S</mi><mo>=</mo><mo stretchy=\"false\">{</mo><mi>u</mi><mo stretchy=\"false\">}</mo></mrow><annotation encoding=\"application/x-tex\">S=\\{u\\}</annotation></semantics></math></span>), והקבוצה המשלימה מכילה את כל שאר קודקודי הגרף. הצלעות ש\"חוצות\" את החתך הזה (כלומר, צלע שקצה אחד שלה ב-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>S</mi></mrow><annotation encoding=\"application/x-tex\">S</annotation></semantics></math></span> והשני ב-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>V</mi><mo>∖</mo><mi>S</mi></mrow><annotation encoding=\"application/x-tex\">V\\setminus S</annotation></semantics></math></span>) הן בדיוק כל הצלעות המחוברות לקודקוד <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>u</mi></mrow><annotation encoding=\"application/x-tex\">u</annotation></semantics></math></span>. על פי הנתון, הצלע <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi><mo>=</mo><mo stretchy=\"false\">{</mo><mi>u</mi><mo separator=\"true\">,</mo><mi>v</mi><mo stretchy=\"false\">}</mo></mrow><annotation encoding=\"application/x-tex\">e=\\{u,v\\}</annotation></semantics></math></span> היא בעלת המשקל המינימלי מבין כל הצלעות הללו, ולכן היא הצלע הקלה ביותר שחוצה את החתך. תכונת החתך קובעת כי עבור כל חתך בגרף, הצלע המינימלית החוצה אותו חייבת להיות שייכת לכל עץ פורש מינימלי. מכיוון ש-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>e</mi></mrow><annotation encoding=\"application/x-tex\">e</annotation></semantics></math></span> היא הצלע המינימלית בחתך שהגדרנו, היא חייבת להיות חלק מה-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>M</mi><mi>S</mi><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">MST</annotation></semantics></math></span>.",
   "pointsTotal": 15
  },
  {
   "num": 3,
   "kind": "computation",
   "topic": "huffman",
   "question": "שאלה זו עוסקת בקוד הופמן (בשאלה זו שני סעיפים בלתי תלויים).\nמהו קוד הופמן המתקבל מטבלת השכיחויות הבאה? פרטו את דרך החישוב.\n**שכיחות:** `a`=22, `b`=15, `c`=3, `d`=24, `e`=4, `f`=10, `g`=8",
   "solution": "**פתרון רשמי** (26A-A פתרון עמ' 6):\n![עץ הופמן לשכיחויות a=22, b=15, c=3, d=24, e=4, f=10, g=8: השורש 86, ענף 0 לשמאל וענף 1 לימין](images/exams/26A-A-Q3a-tree.png)\nעץ הופמן הוא עץ בינארי מלא (כל צומת הוא עלה או בעל שני בנים בדיוק). הקידוד של כל אות הוא המסלול מהשורש ועד לעלה המייצג אותה, כאשר כל קשת לאורך המסלול מתורגמת לספרה בינארית (0 או 1) בהתאם למוסכמה שנבחרה (לרוב משמאלה '0' ולימינה '1').\nלהלן הקידוד שהתקבל מבניית עץ הופמן באמצעות Huffman Tree Generator שזמין באינטרנט. הקידוד מייצג את המסלולים מהשורש לעלים עבור כל אות במילון.\n\n**שכיחות:** `a`=22, `b`=15, `c`=3, `d`=24, `e`=4, `f`=10, `g`=8\n**קידוד:** `a`=01, `b`=111, `c`=0000, `d`=10, `e`=0001, `f`=110, `g`=001",
   "solutionSource": "official-pdf",
   "official": true,
   "confidence": "high",
   "part": "א",
   "points": 10,
   "id": "26A-A-Q3a",
   "partKey": "a",
   "examCode": "26A-A",
   "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
   "year": 2026,
   "source": "exam",
   "topicLabel": "קוד הופמן",
   "questionHtml": "שאלה זו עוסקת בקוד הופמן (בשאלה זו שני סעיפים בלתי תלויים).<br>מהו קוד הופמן המתקבל מטבלת השכיחויות הבאה? פרטו את דרך החישוב.<br><strong>שכיחות:</strong> <code class=\"tok\" dir=\"ltr\">a</code>=22, <code class=\"tok\" dir=\"ltr\">b</code>=15, <code class=\"tok\" dir=\"ltr\">c</code>=3, <code class=\"tok\" dir=\"ltr\">d</code>=24, <code class=\"tok\" dir=\"ltr\">e</code>=4, <code class=\"tok\" dir=\"ltr\">f</code>=10, <code class=\"tok\" dir=\"ltr\">g</code>=8",
   "solutionHtml": "<strong>פתרון רשמי</strong> (26A-A פתרון עמ' 6):<figure class=\"rt-fig\"><img src=\"images/exams/26A-A-Q3a-tree.png\" alt=\"עץ הופמן לשכיחויות a=22, b=15, c=3, d=24, e=4, f=10, g=8: השורש 86, ענף 0 לשמאל וענף 1 לימין\" loading=\"lazy\"><figcaption>עץ הופמן לשכיחויות a=22, b=15, c=3, d=24, e=4, f=10, g=8: השורש 86, ענף 0 לשמאל וענף 1 לימין</figcaption></figure>עץ הופמן הוא עץ בינארי מלא (כל צומת הוא עלה או בעל שני בנים בדיוק). הקידוד של כל אות הוא המסלול מהשורש ועד לעלה המייצג אותה, כאשר כל קשת לאורך המסלול מתורגמת לספרה בינארית (0 או 1) בהתאם למוסכמה שנבחרה (לרוב משמאלה '0' ולימינה '1').<br>להלן הקידוד שהתקבל מבניית עץ הופמן באמצעות Huffman Tree Generator שזמין באינטרנט. הקידוד מייצג את המסלולים מהשורש לעלים עבור כל אות במילון.<br><br><strong>שכיחות:</strong> <code class=\"tok\" dir=\"ltr\">a</code>=22, <code class=\"tok\" dir=\"ltr\">b</code>=15, <code class=\"tok\" dir=\"ltr\">c</code>=3, <code class=\"tok\" dir=\"ltr\">d</code>=24, <code class=\"tok\" dir=\"ltr\">e</code>=4, <code class=\"tok\" dir=\"ltr\">f</code>=10, <code class=\"tok\" dir=\"ltr\">g</code>=8<br><strong>קידוד:</strong> <code class=\"tok\" dir=\"ltr\">a</code>=01, <code class=\"tok\" dir=\"ltr\">b</code>=111, <code class=\"tok\" dir=\"ltr\">c</code>=0000, <code class=\"tok\" dir=\"ltr\">d</code>=10, <code class=\"tok\" dir=\"ltr\">e</code>=0001, <code class=\"tok\" dir=\"ltr\">f</code>=110, <code class=\"tok\" dir=\"ltr\">g</code>=001",
   "pointsTotal": 10
  },
  {
   "num": 3,
   "kind": "proof",
   "topic": "huffman",
   "question": "יהי $T$ עץ בינארי מלא עם $n$ עלים כאשר $n\\ge 2$.\nהוכיחו כי קיימת סדרת שכיחויות $f_1,f_2,\\ldots,f_n$ כך שאחד מעצי הופמן של הסדרה הוא $T$.",
   "solution": "**פתרון רשמי** (26A-A פתרון עמ' 7):\nכדי להתאים סדרת שכיחויות לכל עץ בינארי מלא $T$ בעל גובה $h$, ניתן לכל עלה שכיחות של $2^{h-d}$ (כאשר $d$ הוא העומק של העלה). בשיטה זו, ככל שהעלה עמוק יותר הוא מקבל משקל קטן יותר. בכל שלב, שני אחים בעץ יהיו בעלי המשקל המינימלי, וסכומם ייתן בדיוק את המשקל של אביהם בקומה שמעל ($2^k+2^k=2^{k+1}$).\n**קביעת המשקל (מלמעלה למטה):**\n1. נסתכל על העץ $T$ ונחשב את הגובה שלו - $h$.\n2. לשורש ניתן את הערך $2^h$.\n3. בכל פיצול של העץ לשניים, נחלק את הערך של האבא חצי-חצי ($2^{h-1}$) בין שני בניו.\n4. השכיחות של כל עלה ($f_i$) תהיה המספר ש-\"נשאר\" אצלו בסוף התהליך.\n\nפתרון זה נכון לכל עץ בינארי מלא מכיוון שחלוקת המשקלים כחצאים של $2$ יוצרת 'היררכיה קשיחה': בכל שלב, הצמתים בעומק המקסימלי הם בהכרח בעלי המשקל המינימלי במערכת. מכיוון שהעץ מלא, צמתים אלו תמיד מופיעים כזוגות 'אחים' שאיחודם מניב בדיוק את משקל אביהם בעץ $T$. תכונה זו מבטיחה שאלגוריתם הופמן 'יקפל' את העץ מהעלים לשורש שכבה אחר שכבה, מבלי לדלג על רמות או לאחד צמתים שאינם אחים.",
   "solutionSource": "official-pdf",
   "official": true,
   "confidence": "high",
   "part": "ב",
   "points": 10,
   "id": "26A-A-Q3b",
   "partKey": "b",
   "examCode": "26A-A",
   "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
   "year": 2026,
   "source": "exam",
   "topicLabel": "קוד הופמן",
   "questionHtml": "יהי <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">T</annotation></semantics></math></span> עץ בינארי מלא עם <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>n</mi></mrow><annotation encoding=\"application/x-tex\">n</annotation></semantics></math></span> עלים כאשר <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>n</mi><mo>≥</mo><mn>2</mn></mrow><annotation encoding=\"application/x-tex\">n\\ge 2</annotation></semantics></math></span>.<br>הוכיחו כי קיימת סדרת שכיחויות <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><msub><mi>f</mi><mn>1</mn></msub><mo separator=\"true\">,</mo><msub><mi>f</mi><mn>2</mn></msub><mo separator=\"true\">,</mo><mo>…</mo><mo separator=\"true\">,</mo><msub><mi>f</mi><mi>n</mi></msub></mrow><annotation encoding=\"application/x-tex\">f_1,f_2,\\ldots,f_n</annotation></semantics></math></span> כך שאחד מעצי הופמן של הסדרה הוא <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">T</annotation></semantics></math></span>.",
   "solutionHtml": "<strong>פתרון רשמי</strong> (26A-A פתרון עמ' 7):<br>כדי להתאים סדרת שכיחויות לכל עץ בינארי מלא <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">T</annotation></semantics></math></span> בעל גובה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>h</mi></mrow><annotation encoding=\"application/x-tex\">h</annotation></semantics></math></span>, ניתן לכל עלה שכיחות של <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><msup><mn>2</mn><mrow><mi>h</mi><mo>−</mo><mi>d</mi></mrow></msup></mrow><annotation encoding=\"application/x-tex\">2^{h-d}</annotation></semantics></math></span> (כאשר <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>d</mi></mrow><annotation encoding=\"application/x-tex\">d</annotation></semantics></math></span> הוא העומק של העלה). בשיטה זו, ככל שהעלה עמוק יותר הוא מקבל משקל קטן יותר. בכל שלב, שני אחים בעץ יהיו בעלי המשקל המינימלי, וסכומם ייתן בדיוק את המשקל של אביהם בקומה שמעל (<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><msup><mn>2</mn><mi>k</mi></msup><mo>+</mo><msup><mn>2</mn><mi>k</mi></msup><mo>=</mo><msup><mn>2</mn><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msup></mrow><annotation encoding=\"application/x-tex\">2^k+2^k=2^{k+1}</annotation></semantics></math></span>).<br><strong>קביעת המשקל (מלמעלה למטה):</strong><br>1. נסתכל על העץ <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">T</annotation></semantics></math></span> ונחשב את הגובה שלו - <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>h</mi></mrow><annotation encoding=\"application/x-tex\">h</annotation></semantics></math></span>.<br>2. לשורש ניתן את הערך <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><msup><mn>2</mn><mi>h</mi></msup></mrow><annotation encoding=\"application/x-tex\">2^h</annotation></semantics></math></span>.<br>3. בכל פיצול של העץ לשניים, נחלק את הערך של האבא חצי-חצי (<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><msup><mn>2</mn><mrow><mi>h</mi><mo>−</mo><mn>1</mn></mrow></msup></mrow><annotation encoding=\"application/x-tex\">2^{h-1}</annotation></semantics></math></span>) בין שני בניו.<br>4. השכיחות של כל עלה (<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><msub><mi>f</mi><mi>i</mi></msub></mrow><annotation encoding=\"application/x-tex\">f_i</annotation></semantics></math></span>) תהיה המספר ש-\"נשאר\" אצלו בסוף התהליך.<br><br>פתרון זה נכון לכל עץ בינארי מלא מכיוון שחלוקת המשקלים כחצאים של <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>2</mn></mrow><annotation encoding=\"application/x-tex\">2</annotation></semantics></math></span> יוצרת 'היררכיה קשיחה': בכל שלב, הצמתים בעומק המקסימלי הם בהכרח בעלי המשקל המינימלי במערכת. מכיוון שהעץ מלא, צמתים אלו תמיד מופיעים כזוגות 'אחים' שאיחודם מניב בדיוק את משקל אביהם בעץ <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">T</annotation></semantics></math></span>. תכונה זו מבטיחה שאלגוריתם הופמן 'יקפל' את העץ מהעלים לשורש שכבה אחר שכבה, מבלי לדלג על רמות או לאחד צמתים שאינם אחים.",
   "pointsTotal": 10
  },
  {
   "num": 4,
   "kind": "computation",
   "topic": "divide_conquer",
   "question": "בהינתן הקלט הבא: $A=[3,5,9,10,11,12]$, $k=2$. מה הפלט? נמקו תשובתכם.",
   "solution": "**פתרון רשמי** (26A-A פתרון עמ' 8):\nהמספרים החיוביים החסרים הם: $1,2,4,6,7,8,\\ldots$ המספר החסר השני הוא $2$.",
   "solutionSource": "official-pdf",
   "official": true,
   "confidence": "high",
   "part": "א",
   "points": 3,
   "contextId": "26A-A-c4",
   "id": "26A-A-Q4a",
   "partKey": "a",
   "examCode": "26A-A",
   "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
   "year": 2026,
   "source": "exam",
   "topicLabel": "הפרד ומשול ו-Select",
   "questionHtml": "בהינתן הקלט הבא: <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi><mo>=</mo><mo stretchy=\"false\">[</mo><mn>3</mn><mo separator=\"true\">,</mo><mn>5</mn><mo separator=\"true\">,</mo><mn>9</mn><mo separator=\"true\">,</mo><mn>10</mn><mo separator=\"true\">,</mo><mn>11</mn><mo separator=\"true\">,</mo><mn>12</mn><mo stretchy=\"false\">]</mo></mrow><annotation encoding=\"application/x-tex\">A=[3,5,9,10,11,12]</annotation></semantics></math></span>, <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>k</mi><mo>=</mo><mn>2</mn></mrow><annotation encoding=\"application/x-tex\">k=2</annotation></semantics></math></span>. מה הפלט? נמקו תשובתכם.",
   "solutionHtml": "<strong>פתרון רשמי</strong> (26A-A פתרון עמ' 8):<br>המספרים החיוביים החסרים הם: <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>1</mn><mo separator=\"true\">,</mo><mn>2</mn><mo separator=\"true\">,</mo><mn>4</mn><mo separator=\"true\">,</mo><mn>6</mn><mo separator=\"true\">,</mo><mn>7</mn><mo separator=\"true\">,</mo><mn>8</mn><mo separator=\"true\">,</mo><mo>…</mo></mrow><annotation encoding=\"application/x-tex\">1,2,4,6,7,8,\\ldots</annotation></semantics></math></span> המספר החסר השני הוא <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>2</mn></mrow><annotation encoding=\"application/x-tex\">2</annotation></semantics></math></span>.",
   "pointsTotal": 3
  },
  {
   "num": 4,
   "kind": "algorithm",
   "topic": "divide_conquer",
   "question": "כתבו אלגוריתם יעיל לפתרון הבעיה.",
   "solution": "**פתרון רשמי** (26A-A פתרון עמ' 8-9):\nנשתמש באסטרטגיית **חיפוש בינארי** על המערך הממוין $A$. נניח כי המערך מתחיל באינדקס $0$ וגודלו $n$.\nעבור כל אינדקס $i$ ניתן לחשב כמה מספרים חיוביים חסרים עד $A[i]$ באמצעות הנוסחה:\n$$Missing(i)=A[i]-(i+1)$$\n**מקרי קצה:** כדי להבטיח פתרון מלא, נבחין במצבים מחוץ לטווח המערך:\n- לפני איברי המערך: אם $k$ קטן מכמות המספרים החסרים לפני האיבר הראשון ($A[0]-1$), המספר החסר ה-$k$ הוא פשוט $k$. (החיפוש הבינארי יטפל בזה וייתן $low=0$).\n- אחרי איברי המערך: אם לאחר סיום החיפוש הבינארי מתברר ש-$k$ גדול מכמות המספרים החסרים בכל המערך, המספר יימצא אחרי האיבר האחרון. הנוסחה $low+k$ תיתן את התשובה הנכונה גם במקרה זה ($low=n$).\n\n**מהלך החיפוש:**\nנחפש את האינדקס $i$ הקטן ביותר עבורו $Missing(i)\\ge k$.\n- נגדיר גבולות $low=0$, $high=n-1$.\n- בכל שלב נחשב את $mid$. אם $Missing(mid)<k$, נמשיך לחפש מימין ($low=mid+1$), אחרת נחפש משמאל ($high=mid-1$).\n\nלאחר סיום החיפוש, המספר החסר ה-$k$ מתקבל על ידי: $low+k$.\n(מצורף מימוש בשפת C עם הערות בעמוד הבא)\n```c\n#include <stdio.h>\n\nint findKthMissing(int A[], int size, int k) {\n    int low = 0;\n    int high = size - 1;\n\n    //We perform a binary search on the sorted array.\n    //\n    //Key observation:\n    //At index i, the number of missing positive integers\n    //before A[i] is given by:\n    //    A[i] - (i + 1)\n    //\n    //This is because, in a perfect sequence without missing numbers,\n    //the value at index i should be exactly (i + 1).\n\n    while (low <= high) {\n        int mid = low + (high - low) / 2;\n\n        // Number of missing positive integers up to index mid\n        int missing = A[mid] - (mid + 1);\n\n        //If the number of missing values is smaller than k,\n        //then the k-th missing number must be located\n        //to the right of mid.\n\n        if (missing < k) {\n            low = mid + 1;\n        }\n        //Otherwise, there are already at least k missing numbers\n        //up to index mid, so we continue searching on the left side.\n        else {\n            high = mid - 1;\n        }\n    }\n\n    //After the loop terminates:\n    //'low' points to the first index where the number of\n    //missing values is greater than or equal to k.\n    //\n    //The k-th missing positive integer is therefore:\n    //    k + low\n\n    return low + k;\n}\n\nint main() {\n    int A[] = { 3, 5, 9, 10, 11, 12 };\n    int k = 3;\n    int size = sizeof(A) / sizeof(A[0]);\n\n    printf(\"The %d-th missing number is: %d\\n\", k, findKthMissing(A, size, k));\n    return 0;\n}\n```",
   "solutionSource": "official-pdf",
   "official": true,
   "confidence": "high",
   "part": "ב",
   "points": 15,
   "contextId": "26A-A-c4",
   "id": "26A-A-Q4b",
   "partKey": "b",
   "examCode": "26A-A",
   "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
   "year": 2026,
   "source": "exam",
   "topicLabel": "הפרד ומשול ו-Select",
   "questionHtml": "כתבו אלגוריתם יעיל לפתרון הבעיה.",
   "solutionHtml": "<strong>פתרון רשמי</strong> (26A-A פתרון עמ' 8-9):<br>נשתמש באסטרטגיית <strong>חיפוש בינארי</strong> על המערך הממוין <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi></mrow><annotation encoding=\"application/x-tex\">A</annotation></semantics></math></span>. נניח כי המערך מתחיל באינדקס <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mn>0</mn></mrow><annotation encoding=\"application/x-tex\">0</annotation></semantics></math></span> וגודלו <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>n</mi></mrow><annotation encoding=\"application/x-tex\">n</annotation></semantics></math></span>.<br>עבור כל אינדקס <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>i</mi></mrow><annotation encoding=\"application/x-tex\">i</annotation></semantics></math></span> ניתן לחשב כמה מספרים חיוביים חסרים עד <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi><mo stretchy=\"false\">[</mo><mi>i</mi><mo stretchy=\"false\">]</mo></mrow><annotation encoding=\"application/x-tex\">A[i]</annotation></semantics></math></span> באמצעות הנוסחה:<br><span class=\"math-block\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\" display=\"block\"><semantics><mrow><mi>M</mi><mi>i</mi><mi>s</mi><mi>s</mi><mi>i</mi><mi>n</mi><mi>g</mi><mo stretchy=\"false\">(</mo><mi>i</mi><mo stretchy=\"false\">)</mo><mo>=</mo><mi>A</mi><mo stretchy=\"false\">[</mo><mi>i</mi><mo stretchy=\"false\">]</mo><mo>−</mo><mo stretchy=\"false\">(</mo><mi>i</mi><mo>+</mo><mn>1</mn><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">Missing(i)=A[i]-(i+1)</annotation></semantics></math></span><br><strong>מקרי קצה:</strong> כדי להבטיח פתרון מלא, נבחין במצבים מחוץ לטווח המערך:<br>- לפני איברי המערך: אם <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>k</mi></mrow><annotation encoding=\"application/x-tex\">k</annotation></semantics></math></span> קטן מכמות המספרים החסרים לפני האיבר הראשון (<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>A</mi><mo stretchy=\"false\">[</mo><mn>0</mn><mo stretchy=\"false\">]</mo><mo>−</mo><mn>1</mn></mrow><annotation encoding=\"application/x-tex\">A[0]-1</annotation></semantics></math></span>), המספר החסר ה-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>k</mi></mrow><annotation encoding=\"application/x-tex\">k</annotation></semantics></math></span> הוא פשוט <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>k</mi></mrow><annotation encoding=\"application/x-tex\">k</annotation></semantics></math></span>. (החיפוש הבינארי יטפל בזה וייתן <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>l</mi><mi>o</mi><mi>w</mi><mo>=</mo><mn>0</mn></mrow><annotation encoding=\"application/x-tex\">low=0</annotation></semantics></math></span>).<br>- אחרי איברי המערך: אם לאחר סיום החיפוש הבינארי מתברר ש-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>k</mi></mrow><annotation encoding=\"application/x-tex\">k</annotation></semantics></math></span> גדול מכמות המספרים החסרים בכל המערך, המספר יימצא אחרי האיבר האחרון. הנוסחה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>l</mi><mi>o</mi><mi>w</mi><mo>+</mo><mi>k</mi></mrow><annotation encoding=\"application/x-tex\">low+k</annotation></semantics></math></span> תיתן את התשובה הנכונה גם במקרה זה (<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>l</mi><mi>o</mi><mi>w</mi><mo>=</mo><mi>n</mi></mrow><annotation encoding=\"application/x-tex\">low=n</annotation></semantics></math></span>).<br><br><strong>מהלך החיפוש:</strong><br>נחפש את האינדקס <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>i</mi></mrow><annotation encoding=\"application/x-tex\">i</annotation></semantics></math></span> הקטן ביותר עבורו <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>M</mi><mi>i</mi><mi>s</mi><mi>s</mi><mi>i</mi><mi>n</mi><mi>g</mi><mo stretchy=\"false\">(</mo><mi>i</mi><mo stretchy=\"false\">)</mo><mo>≥</mo><mi>k</mi></mrow><annotation encoding=\"application/x-tex\">Missing(i)\\ge k</annotation></semantics></math></span>.<br>- נגדיר גבולות <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>l</mi><mi>o</mi><mi>w</mi><mo>=</mo><mn>0</mn></mrow><annotation encoding=\"application/x-tex\">low=0</annotation></semantics></math></span>, <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>h</mi><mi>i</mi><mi>g</mi><mi>h</mi><mo>=</mo><mi>n</mi><mo>−</mo><mn>1</mn></mrow><annotation encoding=\"application/x-tex\">high=n-1</annotation></semantics></math></span>.<br>- בכל שלב נחשב את <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>m</mi><mi>i</mi><mi>d</mi></mrow><annotation encoding=\"application/x-tex\">mid</annotation></semantics></math></span>. אם <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>M</mi><mi>i</mi><mi>s</mi><mi>s</mi><mi>i</mi><mi>n</mi><mi>g</mi><mo stretchy=\"false\">(</mo><mi>m</mi><mi>i</mi><mi>d</mi><mo stretchy=\"false\">)</mo><mo>&lt;</mo><mi>k</mi></mrow><annotation encoding=\"application/x-tex\">Missing(mid)&lt;k</annotation></semantics></math></span>, נמשיך לחפש מימין (<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>l</mi><mi>o</mi><mi>w</mi><mo>=</mo><mi>m</mi><mi>i</mi><mi>d</mi><mo>+</mo><mn>1</mn></mrow><annotation encoding=\"application/x-tex\">low=mid+1</annotation></semantics></math></span>), אחרת נחפש משמאל (<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>h</mi><mi>i</mi><mi>g</mi><mi>h</mi><mo>=</mo><mi>m</mi><mi>i</mi><mi>d</mi><mo>−</mo><mn>1</mn></mrow><annotation encoding=\"application/x-tex\">high=mid-1</annotation></semantics></math></span>).<br><br>לאחר סיום החיפוש, המספר החסר ה-<span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>k</mi></mrow><annotation encoding=\"application/x-tex\">k</annotation></semantics></math></span> מתקבל על ידי: <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>l</mi><mi>o</mi><mi>w</mi><mo>+</mo><mi>k</mi></mrow><annotation encoding=\"application/x-tex\">low+k</annotation></semantics></math></span>.<br>(מצורף מימוש בשפת C עם הערות בעמוד הבא)<pre class=\"code-block\" dir=\"ltr\" data-lang=\"c\"><code>#include &lt;stdio.h&gt;\n\nint findKthMissing(int A[], int size, int k) {\n    int low = 0;\n    int high = size - 1;\n\n    //We perform a binary search on the sorted array.\n    //\n    //Key observation:\n    //At index i, the number of missing positive integers\n    //before A[i] is given by:\n    //    A[i] - (i + 1)\n    //\n    //This is because, in a perfect sequence without missing numbers,\n    //the value at index i should be exactly (i + 1).\n\n    while (low &lt;= high) {\n        int mid = low + (high - low) / 2;\n\n        // Number of missing positive integers up to index mid\n        int missing = A[mid] - (mid + 1);\n\n        //If the number of missing values is smaller than k,\n        //then the k-th missing number must be located\n        //to the right of mid.\n\n        if (missing &lt; k) {\n            low = mid + 1;\n        }\n        //Otherwise, there are already at least k missing numbers\n        //up to index mid, so we continue searching on the left side.\n        else {\n            high = mid - 1;\n        }\n    }\n\n    //After the loop terminates:\n    //'low' points to the first index where the number of\n    //missing values is greater than or equal to k.\n    //\n    //The k-th missing positive integer is therefore:\n    //    k + low\n\n    return low + k;\n}\n\nint main() {\n    int A[] = { 3, 5, 9, 10, 11, 12 };\n    int k = 3;\n    int size = sizeof(A) / sizeof(A[0]);\n\n    printf(\"The %d-th missing number is: %d\\n\", k, findKthMissing(A, size, k));\n    return 0;\n}</code></pre>",
   "pointsTotal": 15
  },
  {
   "num": 4,
   "kind": "computation",
   "topic": "complexity_recurrence",
   "question": "מה סיבוכיות זמן הריצה של האלגוריתם שהצעת בסעיף ב'? נמקו תשובתכם.",
   "solution": "**פתרון רשמי** (26A-A פתרון עמ' 8):\nהאלגוריתם מבצע חיפוש בינארי על מערך בגודל $n$. כמו כן נוסחת הנסיגה היא:\n$$T(n)=T(n/2)+1$$\nולכן, סיבוכיות זמן הריצה היא: $O(\\log n)$.",
   "solutionSource": "official-pdf",
   "official": true,
   "confidence": "high",
   "part": "ג",
   "points": 7,
   "contextId": "26A-A-c4",
   "id": "26A-A-Q4c",
   "partKey": "c",
   "examCode": "26A-A",
   "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
   "year": 2026,
   "source": "exam",
   "topicLabel": "סיבוכיות ונוסחאות נסיגה",
   "questionHtml": "מה סיבוכיות זמן הריצה של האלגוריתם שהצעת בסעיף ב'? נמקו תשובתכם.",
   "solutionHtml": "<strong>פתרון רשמי</strong> (26A-A פתרון עמ' 8):<br>האלגוריתם מבצע חיפוש בינארי על מערך בגודל <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>n</mi></mrow><annotation encoding=\"application/x-tex\">n</annotation></semantics></math></span>. כמו כן נוסחת הנסיגה היא:<br><span class=\"math-block\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\" display=\"block\"><semantics><mrow><mi>T</mi><mo stretchy=\"false\">(</mo><mi>n</mi><mo stretchy=\"false\">)</mo><mo>=</mo><mi>T</mi><mo stretchy=\"false\">(</mo><mi>n</mi><mi mathvariant=\"normal\">/</mi><mn>2</mn><mo stretchy=\"false\">)</mo><mo>+</mo><mn>1</mn></mrow><annotation encoding=\"application/x-tex\">T(n)=T(n/2)+1</annotation></semantics></math></span><br>ולכן, סיבוכיות זמן הריצה היא: <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>O</mi><mo stretchy=\"false\">(</mo><mi>log</mi><mo>⁡</mo><mi>n</mi><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">O(\\log n)</annotation></semantics></math></span>.",
   "pointsTotal": 7
  },
  {
   "num": 5,
   "kind": "truefalse",
   "topic": "kmp_strings",
   "question": "**שאלת בונוס (15 נקודות)** - יש להקיף את התשובה הנכונה ולציין נימוק קצר. אין קשר בין הסעיפים השונים, כל סעיף 5 נקודות.\nאם הטבלה של $\\pi$ המתקבלת כחלק מהרצת אלגוריתם KMP היא כולה אפסים אזי בתבנית אין אות שחוזרת על עצמה.",
   "solution": "**פתרון רשמי** (26A-A פתרון עמ' 1): לא נכון.\nנימוק: דוגמה נגדית: `ABB` - מספק לנו טבלת $\\pi$ שכולה אפסים.",
   "solutionSource": "official-pdf",
   "official": true,
   "confidence": "high",
   "part": "א",
   "points": 5,
   "verdict": false,
   "id": "26A-A-Q5a",
   "partKey": "a",
   "examCode": "26A-A",
   "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
   "year": 2026,
   "source": "exam",
   "topicLabel": "מחרוזות: KMP ופונקציית רישא",
   "questionHtml": "<strong>שאלת בונוס (15 נקודות)</strong> - יש להקיף את התשובה הנכונה ולציין נימוק קצר. אין קשר בין הסעיפים השונים, כל סעיף 5 נקודות.<br>אם הטבלה של <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>π</mi></mrow><annotation encoding=\"application/x-tex\">\\pi</annotation></semantics></math></span> המתקבלת כחלק מהרצת אלגוריתם KMP היא כולה אפסים אזי בתבנית אין אות שחוזרת על עצמה.",
   "solutionHtml": "<strong>פתרון רשמי</strong> (26A-A פתרון עמ' 1): לא נכון.<br>נימוק: דוגמה נגדית: <code class=\"tok\" dir=\"ltr\">ABB</code> - מספק לנו טבלת <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>π</mi></mrow><annotation encoding=\"application/x-tex\">\\pi</annotation></semantics></math></span> שכולה אפסים.",
   "pointsTotal": 5
  },
  {
   "num": 5,
   "kind": "truefalse",
   "topic": "kmp_strings",
   "question": "**שאלת בונוס** (סעיף בלתי תלוי, 5 נקודות).\nיתכן שבאלגוריתם KMP הלולאה הפנימית תתבצע בזמן $\\Theta(m)$, כאשר $m$ הוא אורך התבנית $P$.",
   "solution": "**פתרון רשמי** (26A-A פתרון עמ' 1): נכון.\nנימוק: $P=aaaaaa$, $T=aaaaab\\ldots aaa$.\nב-KMP במקרה של כשל התאמה הלולאה הפנימית יכולה לרדת דרך ערכי ה-LPS עד תחילת התבנית - זמן ריצה $\\Theta(m)$.",
   "solutionSource": "official-pdf",
   "official": true,
   "confidence": "high",
   "part": "ב",
   "points": 5,
   "verdict": true,
   "id": "26A-A-Q5b",
   "partKey": "b",
   "examCode": "26A-A",
   "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
   "year": 2026,
   "source": "exam",
   "topicLabel": "מחרוזות: KMP ופונקציית רישא",
   "questionHtml": "<strong>שאלת בונוס</strong> (סעיף בלתי תלוי, 5 נקודות).<br>יתכן שבאלגוריתם KMP הלולאה הפנימית תתבצע בזמן <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi mathvariant=\"normal\">Θ</mi><mo stretchy=\"false\">(</mo><mi>m</mi><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">\\Theta(m)</annotation></semantics></math></span>, כאשר <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>m</mi></mrow><annotation encoding=\"application/x-tex\">m</annotation></semantics></math></span> הוא אורך התבנית <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>P</mi></mrow><annotation encoding=\"application/x-tex\">P</annotation></semantics></math></span>.",
   "solutionHtml": "<strong>פתרון רשמי</strong> (26A-A פתרון עמ' 1): נכון.<br>נימוק: <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>P</mi><mo>=</mo><mi>a</mi><mi>a</mi><mi>a</mi><mi>a</mi><mi>a</mi><mi>a</mi></mrow><annotation encoding=\"application/x-tex\">P=aaaaaa</annotation></semantics></math></span>, <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi><mo>=</mo><mi>a</mi><mi>a</mi><mi>a</mi><mi>a</mi><mi>a</mi><mi>b</mi><mo>…</mo><mi>a</mi><mi>a</mi><mi>a</mi></mrow><annotation encoding=\"application/x-tex\">T=aaaaab\\ldots aaa</annotation></semantics></math></span>.<br>ב-KMP במקרה של כשל התאמה הלולאה הפנימית יכולה לרדת דרך ערכי ה-LPS עד תחילת התבנית - זמן ריצה <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi mathvariant=\"normal\">Θ</mi><mo stretchy=\"false\">(</mo><mi>m</mi><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">\\Theta(m)</annotation></semantics></math></span>.",
   "pointsTotal": 5
  },
  {
   "num": 5,
   "kind": "truefalse",
   "topic": "kmp_strings",
   "question": "**שאלת בונוס** (סעיף בלתי תלוי, 5 נקודות).\nהאלגוריתם הנאיבי לפתרון בעיית חיפוש מחרוזת $P$ באורך $m$ בטקסט $T$ באורך $n$ רץ במקרה הגרוע בזמן לינארי.",
   "solution": "**פתרון רשמי** (26A-A פתרון עמ' 1): לא נכון.\nנימוק:\n`T = aaaaaaaaaaaaaaaaaaaaaaaaab`\n`P = aaaaaab`\nבכל היסט יש התאמה כמעט מלאה עד התו האחרון ונכשלת רק בסוף, מה שגורם לחזרה על $m$ השוואות בכל מיקום. ולכן זמן הריצה במקרה הגרוע הוא $\\Theta(n\\cdot m)$.",
   "solutionSource": "official-pdf",
   "official": true,
   "confidence": "high",
   "part": "ג",
   "points": 5,
   "verdict": false,
   "id": "26A-A-Q5c",
   "partKey": "c",
   "examCode": "26A-A",
   "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ו, מועד א (2.02.2026)",
   "year": 2026,
   "source": "exam",
   "topicLabel": "מחרוזות: KMP ופונקציית רישא",
   "questionHtml": "<strong>שאלת בונוס</strong> (סעיף בלתי תלוי, 5 נקודות).<br>האלגוריתם הנאיבי לפתרון בעיית חיפוש מחרוזת <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>P</mi></mrow><annotation encoding=\"application/x-tex\">P</annotation></semantics></math></span> באורך <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>m</mi></mrow><annotation encoding=\"application/x-tex\">m</annotation></semantics></math></span> בטקסט <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>T</mi></mrow><annotation encoding=\"application/x-tex\">T</annotation></semantics></math></span> באורך <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>n</mi></mrow><annotation encoding=\"application/x-tex\">n</annotation></semantics></math></span> רץ במקרה הגרוע בזמן לינארי.",
   "solutionHtml": "<strong>פתרון רשמי</strong> (26A-A פתרון עמ' 1): לא נכון.<br>נימוק:<br><code class=\"tok\" dir=\"ltr\">T = aaaaaaaaaaaaaaaaaaaaaaaaab</code><br><code class=\"tok\" dir=\"ltr\">P = aaaaaab</code><br>בכל היסט יש התאמה כמעט מלאה עד התו האחרון ונכשלת רק בסוף, מה שגורם לחזרה על <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi>m</mi></mrow><annotation encoding=\"application/x-tex\">m</annotation></semantics></math></span> השוואות בכל מיקום. ולכן זמן הריצה במקרה הגרוע הוא <span class=\"math-inline\"><math dir=\"ltr\" xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mi mathvariant=\"normal\">Θ</mi><mo stretchy=\"false\">(</mo><mi>n</mi><mo>⋅</mo><mi>m</mi><mo stretchy=\"false\">)</mo></mrow><annotation encoding=\"application/x-tex\">\\Theta(n\\cdot m)</annotation></semantics></math></span>.",
   "pointsTotal": 5
  }
 ]
};
