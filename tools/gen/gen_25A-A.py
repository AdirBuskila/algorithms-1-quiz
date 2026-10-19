# -*- coding: utf-8 -*-
"""Generator for tools/raw/25A-A.json -- algorithms-1 (70162), semester A 2025, moed A (10.02.2025).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25A-A.py

Source: exam booklet pp.1-15 (cover, bonus on p.2, 4 questions with answer lines) and the official typed
solution file pp.1-6 (it repeats Q1-Q4 and gives informal pseudocode; the bonus is not solved). Cap 115.
Items: Q1 a,b,c (10/5/10), Q2 a,b,c (15/5/5), Q3 a,b (12.5/12.5), Q4 a,b,c (10/10/5), bonus a,b,c (5 each, num 5).

Shipped (official): Q1a, Q1b, Q2c, Q3a, Q3b, Q4b, Q4c.
Held:
- Q1c: key-disagreement. The official answer "Return(mid(A[1..r],B[1..r]))" returns the average of the two middle
  elements of the 2r chosen elements, not the r-th smallest (A=[1,2], B=[3,4], r=2: 2.5 vs 2).
- Q2a: key-disagreement. The printed recurrence keeps k in two rows (T(i,j-1,k)) and has no row for
  S1[i]!=S3[k] and S2[j]!=S3[k]; against brute force it is wrong or undefined.
- Q2b: no-key. The solution file only says that similar demonstrations were done in the course.
- Q4a: no-key. The solution file gives only a remark ("compute the KMP pi array and return its maximum"), not an
  algorithm, and the remark is unsafe (max(pi) != pi[n-1], e.g. abcabcd). The question's own examples also conflict
  with its wording (aaaa -> 4 counts the whole string, aabcdaabc -> 4 does not).
- Bonus a, b, c: no-key (no solution in the file).

Transcription notes
- Q1a: the official Mid pseudocode is informal (the base case i=j is listed after the first two cases, typos like
  "l1"); transcribed verbatim, confidence med. checks.py runs it with the base case tested first.
- Q4b: the official code and symbol table are transcribed; checks.py runs the same logic on a compacted suffix tree.
Checks: tools/verify/25A-A/checks.py (brute force + the official algorithms).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25A-A.json"


def Q(num, part, kind, topic, question, solution=None, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question}
    if solution is not None:
        q.update({"solution": solution, "solutionSource": "official-pdf", "official": True, "confidence": "high"})
    if part:
        q["part"] = part
    q.update(kw)
    return q


C1 = (r"נתונים שני מערכי מספרים ממוינים $A[1..\frac{n}{2}]$, $B[1..\frac{n}{2}]$ שכל אחד מהם בגודל $\frac{n}{2}$." "\n"
      r"הניחו שבכל מערך האיברים שונים זה מזה וכל איברי מערך אחד שונים מכל איברי המערך השני. כמו כן, הניחו כי המספר $n$ הוא חזקה של 2, "
      r"ז\"א קיים מספר טבעי $k$ כך ש: $n=2^k$." "\n"
      r"**תזכורת:** נניח שיש לנו $n$ מספרים מסודרים בסדר עולה: $x_1,x_2,\ldots,x_n$. כאשר $n$ זוגי ($2k=n$ עבור $k$ שלם), החציון ($M$) מחושב כך: "
      r"$M=\frac{x_k+x_{k+1}}{2}$. כלומר, הוא הממוצע של **האיבר במקום ה-$k$ והאיבר במקום ה-$1+k$** (**שני האיברים האמצעיים**)." "\n"
      r"**דוגמה:** נניח שיש לנו את הקבוצה הבאה של 6 מספרים (כמות זוגית): $2,3,5,8,10,12$. האיברים האמצעיים הם 5 ו-8 "
      r"(האיברים במקומות ה-3 וה-4). החציון יהיה: $M=\frac{5+8}{2}=\frac{13}{2}=6.5$.")

C2 = (r"**הגדרה:** יהיו $S_1,S_2,S_3$ שלוש מחרוזות. נאמר שמחרוזת $S_3$ הינה \"מחרוזת שילוב\" של $S_1,S_2$ אם:" "\n"
      r"1. $S_3$ מכילה את כל התווים של $S_1,S_2$ ורק אותם (ז\"א, ללא תווים נוספים מעבר לתווים שיש במחרוזות $S_1,S_2$)." "\n"
      r"2. סדר התווים שבמחרוזות $S_1,S_2$ נשמר כפי שהוא במחרוזת $S_3$." "\n"
      r"**דוגמה למחרוזת $S_3$ שהינה \"מחרוזת שילוב\" של $S_1,S_2$:**" "\n"
      r"`S1=\"abc\", s2=\"def\", s3=\"adbcef\"`" "\n"
      r"`S1=\"abc\", s2=\"dec\", s3=\"adbcec\"`" "\n"
      r"**דוגמה למחרוזת $S_3$ שאינה \"מחרוזת שילוב\" של $S_1,S_2$:**" "\n"
      r"`S1=\"abc\", s2=\"def\", s3=\"bdacef\"`" "\n"
      r"`S1=\"abc\", s2=\"def\", s3=\"adbce\"`" "\n"
      r"להלן בעיית מחרוזת שילוב:" "\n"
      r"**קלט:** שלוש מחרוזות $S_1,S_2,S_3$" "\n"
      r"**פלט:** אמת, אם המחרוזת $S_3$ הינה \"מחרוזת שילוב\" של $S_1,S_2$, אחרת, שקר" "\n"
      r"בעיית מחרוזת שילוב ניתנת לפתרון בעזרת תכנות דינמי.")

C3 = (r"להלן תיאור בעיית \"ריבוי איברים\":" "\n"
      r"**קלט:** מספר טבעי $n$ ורשימה $L$ של $m$ מספרים טבעים." "\n"
      r"**פלט:** הכמות המקסימלית של האיברים מהרשימה $L$ כך שסכומם לכל היותר $n$." "\n"
      r"**לדוגמה:** עבור הקלט $n=6$ והרשימה $L$ הבאה (של חמישה מספרים): $2,5,3,8,10$" "\n"
      r"הפלט הוא 2 כי סכום האיבר הראשון והשלישי הוא, $2+3=5<6$ ובמגבלה של $n=6$ קל לראות כי לא ניתן לבחור יותר מ-2 איברים מהרשימה." "\n"
      r"בעיית ריבוי איברים ניתנת לפתרון בעזרת אלגוריתם חמדני.")

C5 = (r"**שאלת בונוס - 15 נקודות** (יש להקיף את התשובה הנכונה)." "\n"
      r"הסעיפים הבאים מתייחסים לגרף $G$ המיוצג על ידי מטריצת סמיכויות." "\n"
      r"הנח כי הסריקה DFS בוצעה על הגרף $G$, וברשותנו, מערך $\Pi$ (תוצאת עץ הסריקה); מערך $D$ של זמני התחלה של כל קודקוד ב-$G$; "
      r"מערך $F$ של זמני הסיום של כל קודקוד ב-$G$:")

C4A = (r"להלן הגדרת \"בעיית הרישא סיפא הארוכה ביותר\":" "\n"
       r"**קלט:** מחרוזת $S$" "\n"
       r"**פלט:** אורך הרישא (prefix) הארוכה ביותר של $S$ שהיא גם סיפא (suffix) של $S$." "\n"
       r"להלן שתי דוגמאות:" "\n"
       r"קלט: `S=aabcdaabc`, פלט: 4 (`aabc` היא הרישא וגם הסיפא הארוכה ביותר של $S$)." "\n"
       r"קלט: `S=aaaa`, פלט: 4 (`aaaa` היא הרישא וגם הסיפא הארוכה ביותר של $S$).")

C4B = (r"נתונה הבעיה הבאה:" "\n"
       r"**קלט:** מילה $w$ ועץ סיפות עם **קיבוץ מסלולים** לטקסט $T$, שבו רשום בכל עלה, האינדקס בטקסט של מיקום תחילת הסיפא המתאימה לאותו עלה." "\n"
       r"**פלט:** מיקום כל המופעים של $w$ בטקסט (כלומר, כל האינדקסים בטקסט $T$ ששם מתחילה המילה $w$).")

CODE_1A = r"""Mid(A[i..j],B[k..l1])
If A[(i+j-1)/2]< B[(k+l-1)/2]< B[(k+l+1)/2)] <A[(i+j+1)/2] return((B[(k+l-1)/2]+ B[(k+l+1)/2)])
If B[(k+l-1)/2]<A[(i+j-1)/2]< A[(i+j+1)/2] <B[(k+l+1)/2)] return((A[(i+j-1)/2]+ A[(i+j+1)/2)])
If i=j return((A[i]+B[k])/2)
If A[(i+j-1)/2]< A[(i+j+1)/2]< B[(k+l-1)/2]< B[(k+l+1)/2)] mid(A[(i+j+1)/2..j],B[k.. (k+l-1)/2])
If A[(i+j-1)/2] < B[(k+l-1)/2] < A[(i+j+1)/2]< B[(k+l+1)/2)] mid(A[(i+j+1)/2..j],B[k.. (k+l-1)/2])
If B[(k+l-1)/2] < B[(k+l+1)/2)] < A[(i+j-1)/2]< A[(i+j+1)/2] mid(B[((k+l)-1/2)..l],A[(i..(i+j-1)/2]
If B[(k+l-1)/2] < A[(i+j-1)/2]< B[(k+l+1)/2)] < A[(i+j+1)/2] mid(B[((k+l)-1/2)..l],A[(i..(i+j-1)/2]"""

SOL_1A = (r"""**פתרון רשמי** (25A-A פתרון עמ' 1):
""" + "```\n" + CODE_1A + "\n```\n" + r"הקריאה תתבצע על: `Mid(A[1..n/2],B[1..n/2])`")

SOL_1B = r"""**פתרון רשמי** (25A-A פתרון עמ' 1):
$$T(n)=T(n/2)+1$$
לפי משפט האב, מקרה 2, הגענו לסיבוכיות הדרושה: $\Theta(\log n)$."""

SOL_2C = r"""**פתרון רשמי** (25A-A פתרון עמ' 3):
ללא חסכון במקום יש למלא טבלה ריבועית כתלות במחרוזת השלישית. ניתן למלא לפי עמודות או שורות.
בהנחה שהמחרוזות באורך $n$, זמן הפתרון הוא ריבועי ($\Theta(n^2)$), בעוד מקום הוא ריבועי, או לינארי בגודל הקלט (שמירת שורה אחת בלבד)."""

CODE_3A = r"""Greedy-Subset-Sum(L, n)
1. Sort L in non-decreasing order
2. sum <- 0
3. count <- 0
4. for i <- 1 to length(L) do
5.     if sum + L[i] <= n then
6.         sum <- sum + L[i]
7.         count <- count + 1
8.     else
9.         return count
10. return count"""

SOL_3A = (r"""**פתרון רשמי** (25A-A פתרון עמ' 3): פסאודו-קוד של האלגוריתם:
""" + "```\n" + CODE_3A + "\n```")

SOL_3B = r"""**פתרון רשמי** (25A-A פתרון עמ' 4):
**(א) בחירה חמדנית.** תהי $L[1..l]$ רשימה ממוינת בסדר עולה של האיברים. לכל $1\le i\le j\le l$ נסמן ב-$S_{i,j,k}$ תת-קבוצה בגודל מקסימלי מתוך תת-הרשימה $L[i..j]$ כך שהסכום שלהם לא גדול מ-$k$ (פתרון אופטימלי עבור תת-בעיה עם רשימה $L[i..j]$ וחסם $k$ על סכום האיברים, $(i,j,k)$). נוכיח שאם $L[1]\le n$, אזי קיים פתרון אופטימלי $S_{1,l,n}$ כך ש-$L[1]\in S_{1,l,n}$.
יהי $S'_{1,l,n}$ פתרון אופטימלי עבור תת-הבעיה $(1,l,n)$. יהי $x$ האיבר המינימלי ב-$S'_{1,l,n}$. הרשימה $L[1..n]$ ממוינת בסדר לא יורד. לכן אם נחליף את $x$ ב-$L[1]$, סכום האיברים ב-$S'_{1,l,n}$ לא יגדל, והגודל של $S'_{1,l,n}$ יישאר ללא שינוי. לכן
$$\bigl(S'_{1,l,n}-\{x\}\bigr)\cup L[1]$$
הוא פתרון אופטימלי עבור הבעיה $(1,l,n)$ שמכיל את $L[1]$.
**מבנה אופטימלי של תת-בעיה.** נוכיח שלכל $1\le i\le n$, קיים פתרון אופטימלי עבור הבעיה $(i,l,n)$:
$$S_{i,l,n}=L[i]\cup S_{i+1,l,(n-L[i])}$$
כפי שהוכחנו לעיל, קיים פתרון אופטימלי $S'_{i,l,n}$ שמכיל את $L[i]$. סכום האיברים ב-$\bigl(S'_{i,l,n}-\{L[i]\}\bigr)$ קטן או שווה ל-$(n-L[i])$, לכן $\bigl(S'_{i,l,n}-\{L[i]\}\bigr)$ היא פתרון אופטימלי עבור תת-בעיה $(i,l,n-L[i])$ (אחרת אפשר לשפר את $S'_{i,l,n}$).
בכל שלב $i$, אם $L[i]\le sum$, האלגוריתם מדפיס את $L[i]$ וממשיך לחפש פתרון עבור תת-בעיה $(i+1,l,sum-L[i])$.
לפי התכונה של הבחירה החמדנית והמבנה האופטימלי של הבעיה, האלגוריתם מחזיר פתרון אופטימלי $S_{1,l,n}$ עבור הבעיה $(1,l,n)$."""

CODE_4B = r"""find_all_occurrences_in_suffix_tree(suffix_tree, w):
   node=suffix_tree->root
   ptr_w=w
   m=len(w)
   while(m>0):
      node = bin_search(node ->children, ptr_w)   // children sorted lexicographically
      if node == NULL:                            // no match found
         return NULL
      num_let=maximum_match(node->letters, ptr_w, m)
      if (num_let==m):                            // full match inside the node
         return get_suffix_indexes_from_leafs(node)   // DFS over the subtree to get the indexes
      elif (num_let==len(node->letters)):         // the whole group of letters is covered, continue down
         ptr_w+=num_let                           // advance the pointer by the number of matched letters
         m-= num_let
      else:                                       // otherwise the string is not in the suffix tree
         return NULL"""

SOL_4B = (r"""**פתרון רשמי** (25A-A פתרון עמ' 5):
**הסבר סימוני משתנים ופונקציות לסעיפים ב', ג':**
$\Sigma$ - הא\"ב. $T$ - המחרוזת שמיוצגת על ידי עץ הסיפות. $w$ - המחרוזת לחיפוש. $ptr\_w$ - מצביע לתת המחרוזת. $m$ - אורך המחרוזת שנותר להשוות. `suffix_tree` - עץ הסיפות, `suffix_tree->root` - שורש העץ. `node` - מצביע לצומת בעץ או בתת העץ. `node->children` - הבנים של הצומת הנוכחי. `node->letters` - האותיות המקובצות בצומת הנוכחי (או האינדקסים במחרוזת המקורית $T$). `num_let` - אורך ההתחלה המשותפת. `maximum_match` - חיפוש ההתאמה התחילית המשותפת הארוכה ביותר, לכל היותר באורך $m$. `get_suffix_indexes_from_leafs` - סריקה פשוטה בתת העץ של הצומת המתאים (למשל על ידי DFS), לקבלת האינדקסים של הסיפות במחרוזת $T$. `k` - מספר ההתאמות של $w$. `bin_search` - חיפוש בינארי של האות הראשונה.
""" + "```\n" + CODE_4B + "\n```")

SOL_4C = r"""**פתרון רשמי** (25A-A פתרון עמ' 6):
`bin_search` - פונקציית חיפוש בינארי של האות הראשונה של $w$ (בחלק במחרוזת שטרם בדקנו) בבנים של הקודקוד הנוכחי הממוינים לקסיקוגרפית, לכן סיבוכיות הזמן של הפונקציה היא $O(\log|\Sigma|)$ (לעיתים בהרצאה התעלמנו מפקטור זה).
`maximum_match` - פונקציית ההשוואה בין האותיות המקובצות בצומת, לבין האותיות של $w$ (בחלק במחרוזת שטרם בדקנו). השוואת אות בודדת מתבצעת ב-$O(1)$. לכן, אם כל ההשוואות יבוצעו באותו הצומת (בגלל קיבוץ המסלולים), סיבוכיות הזמן של הפונקציה היא $O(m)$.
`get_suffix_indexes_from_leafs` - סריקה פשוטה בתת העץ של הצומת המתאים (למשל על ידי DFS), לקבלת האינדקסים של הסיפות במחרוזת $T$. כמות ההתאמות למחרוזת $w=k$ = כמות העלים בתת העץ. כמות הצמתים הפנימים היא $O(k)$, ולכן סיבוכיות הזמן של הסריקה היא $O(k)$.
**אם המחרוזת $w$ לא נמצאת בעץ הסיפות:** במקרה הגרוע חוסר ההתאמה באות האחרונה, לכן הסיבוכיות היא $O(m)$. ליתר דיוק $O(m\cdot\log(|\Sigma|))$ (מה שיתרחש במידה ואין שום קיבוץ מסלולים עבור התחילית של הסיפות המתחילה ב-$w$).
**אם המחרוזת $w$ נמצאת בעץ הסיפות:**
א. מציאת הצומת המתאים (עבור האותיות במסלול מהשורש עד אליו מתאים למחרוזת $w$) - סיבוכיות הזמן היא $O(m)$, או ליתר דיוק $O(m\cdot\log(|\Sigma|))$.
ב. סריקת תת העץ של הקודקוד המתאים - בסיבוכיות זמן של $O(k)$.
סה\"כ סיבוכיות הזמן - $O(m+k)$, או ליתר דיוק $O(m\cdot\log(|\Sigma|)+k)$."""

HOLD = "no-key: "

questions = [
    Q(1, "א", "algorithm", "divide_conquer",
      r"כתבו פסודו קוד/אלגוריתם רקורסיבי למציאת החציון במערך המאוחד של $A,B$. זמן הריצה הנדרש $\theta(\log n)$.",
      SOL_1A, points=10, contextId="c1", confidence="med"),
    Q(1, "ב", "proof", "complexity_recurrence",
      r"הוכח שסיבוכיות זמן הריצה של הפסודו קוד/אלגוריתם שהצגתם בסעיף הקודם הינו $\theta(\log n)$.",
      SOL_1B, points=5, contextId="c1"),
    Q(1, "ג", "algorithm", "divide_conquer",
      r"כתבו פסודו קוד/אלגוריתם למציאת האיבר ה-$r$ בגודלו במערך המאוחד של $A,B$, כאשר $1\le r\le\frac{n}{2}$. זמן הריצה הנדרש $\theta(\log r)$.",
      None, points=10, contextId="c1",
      hold="key-disagreement: the official answer Return(mid(A[1..r],B[1..r])) returns the average of the two middle elements of the 2r chosen elements, not the r-th smallest (A=[1,2], B=[3,4], r=2 gives 2.5, the r-th smallest is 2); see docs/ASK_ADIR.md"),

    Q(2, "א", "algorithm", "dp_sequences",
      r"כתבו נוסחה רקורסיבית $T(i,j,k)$ המקבלת שלושה אינדקסים אי שליליים מחזירה אמת אם המחרוזת $S_3$ הינה \"מחרוזת שילוב\" של $S_1,S_2$, אחרת, שקר." "\n"
      r"פרטו מה מייצג הקלט בנוסחה $T$.",
      None, points=15, contextId="c2",
      hold="key-disagreement: the official recurrence keeps k in two rows (T(i,j-1,k)) and has no row for S1[i]!=S3[k] and S2[j]!=S3[k]; against brute force it is wrong or undefined; see docs/ASK_ADIR.md"),
    Q(2, "ב", "computation", "dp_sequences",
      r"הדגימו בצורה ברורה את חישוב הנוסחה הרקורסיבית עבור הקלט הבא: $S_1=$`ebc`, $S_2=$`dec`.",
      None, points=5, contextId="c2",
      hold="no-key: the solution file only says that similar demonstrations were done in the course"),
    Q(2, "ג", "computation", "dp_sequences",
      r"מה סיבוכיות הזמן וסיבוכיות המקום במקרה הגרוע לאלגוריתם תכנות דינמי הפותר את בעיית מחרוזת שילוב?" "\n"
      r"נמקו תשובתכם בקצרה ובבהירות (אין צורך לפרט את האלגוריתם עצמו).",
      SOL_2C, points=5, contextId="c2"),

    Q(3, "א", "algorithm", "greedy",
      r"כתוב פסודו קוד/אלגוריתם היעיל ביותר לפתרון בעיית ריבוי איברים.",
      SOL_3A, points=12.5, contextId="c3"),
    Q(3, "ב", "proof", "greedy", r"הוכח את נכונות הפתרון שהצגת בסעיף א'.", SOL_3B, points=12.5, contextId="c3"),

    Q(4, "א", "algorithm", "kmp_strings",
      r"כתוב פסודו קוד/אלגוריתם היעיל ביותר לפתרון בעיית הרישא סיפא הארוכה ביותר.",
      None, points=10, contextId="c4a",
      hold="no-key: the solution file gives only a remark (compute the KMP pi array and return its maximum), not an algorithm, and the remark is unsafe (max(pi) != pi[n-1], e.g. abcabcd); the question examples also conflict with its wording; see docs/ASK_ADIR.md"),
    Q(4, "ב", "algorithm", "suffix_structures",
      r"כתוב פסודו קוד/אלגוריתם היעיל ביותר לפתרון הבעיה.", SOL_4B, points=10, contextId="c4b"),
    Q(4, "ג", "computation", "suffix_structures",
      r"מהו זמן הריצה של האלגוריתם שהצעתם לבעיה בסעיף (ב)? נמקו קביעתכם.", SOL_4C, points=5, contextId="c4b"),

    Q(5, "א", "truefalse", "graphs_search",
      r"ניתן לאפיין את כל שורשי העצים ביער $\Pi$ בזמן לינארי בכמות שורשי העצים ביער." "\n" r"נכון / לא נכון",
      None, points=5, contextId="c5", hold="no-key: bonus items have no solution in the solution file"),
    Q(5, "ב", "truefalse", "graphs_search",
      r"ניתן לאפיין את כל העלים ביער $\Pi$ בזמן לינארי בכמות הקודקודים ביער." "\n" r"נכון / לא נכון",
      None, points=5, contextId="c5", hold="no-key: bonus items have no solution in the solution file"),
    Q(5, "ג", "truefalse", "graphs_search",
      r"לא ניתן לאפיין בזמן לינארי בגודל הגרף את כל סוגי הצלעות (צלע מהעץ, צלע חוזרת, צלע מקצרת מסלול בעץ, צלע חוצה בין עצים/תתי עצים)." "\n" r"נכון / לא נכון",
      None, points=5, contextId="c5", hold="no-key: bonus items have no solution in the solution file"),
]

exam = {
    "examCode": "25A-A",
    "examLabel": "אלגוריתמים 1 (70162), סמסטר א' תשפ\"ה, מועד א (10.2.2025)",
    "year": 2025,
    "examDate": "10.2.2025",
    "sourceFile": "25A-A exam pp.1-15",
    "solutionFile": "25A-A official solution pp.1-6",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1: חציון של שני מערכים ממוינים", "text": C1},
        "c2": {"kind": "text", "title": "שאלה 2: מחרוזת שילוב", "text": C2},
        "c3": {"kind": "text", "title": "שאלה 3: בעיית ריבוי איברים", "text": C3},
        "c4a": {"kind": "text", "title": "שאלה 4א: הרישא סיפא הארוכה ביותר", "text": C4A},
        "c4b": {"kind": "text", "title": "שאלה 4ב: מופעי מילה בעץ סיפות", "text": C4B},
        "c5": {"kind": "text", "title": "שאלת בונוס: סריקת DFS", "text": C5},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
