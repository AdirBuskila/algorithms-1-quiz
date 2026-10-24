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

Solver pass (2026-10-24; solutionSource "solved", official false, pending refuter):
- Q1c, Q2a, Q4a: typo ruling ("הפתרון הרשמי עם תיקון"). Q1c binary search over the split of A[1..r], B[1..r];
  Q2a k-1 in rows 4 and 8 plus a final "false otherwise" row; Q4a return pi[n] instead of max(pi) (both official
  readings, |S| and the proper border, are stated).
- Bonus a (false: roots need a scan of all |V| entries) and b (true: leaves are the v with F[v]=D[v]+1, O(|V|)).
- Still held: Q2b (S3 is not printed), bonus c (ambiguous for an adjacency matrix: linear in V^2 vs in V+E).
Solver checks: tools/verify/25A-A/solve_25A-A.py (brute force for Q1c, Q2a, Q4a, bonus b).
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

SOLVED = {"solutionSource": "solved", "official": False, "confidence": "high"}

CODE_1C = r"""Find_r(A[1..n/2], B[1..n/2], r)
   // A[0] = B[0] = -inf ; an index above r is read as +inf
   // (only A[1..r] and B[1..r] take part)
   lo <- 0 ; hi <- r
   while lo <= hi
      i <- floor((lo+hi)/2)        // i elements are taken from A
      j <- r - i                   // and r-i elements from B
      if A[i+1] < B[j]   then lo <- i+1     // too few from A
      else if B[j+1] < A[i] then hi <- i-1  // too many from A
      else return max(A[i], B[j])"""

SOL_1C = (r"""הפתרון הרשמי עם תיקון: הודפס `Return(mid(A[1..r],B[1..r]))`, שמחזיר את הממוצע של שני האיברים האמצעיים מבין $2r$ האיברים (עבור $A=[1,2]$, $B=[3,4]$, $r=2$ יוחזר $2.5$); הנכון הוא להחזיר את האיבר ה-$r$ בגודלו מבין $A[1..r]$ ו-$B[1..r]$ (הקטן מבין שני האמצעיים), למשל בחיפוש בינארי:
""" + "```\n" + CODE_1C + "\n```\n" + r"""**רעיון.** $r$ האיברים הקטנים ביותר במערך המאוחד מורכבים מ-$i$ האיברים הראשונים של $A$ ומ-$j=r-i$ האיברים הראשונים של $B$, עבור $i$ כלשהו בין $0$ ל-$r$. לכן מספיק להתבונן ב-$A[1..r]$ וב-$B[1..r]$. החלוקה $(i,j)$ נכונה בדיוק כאשר $A[i]<B[j+1]$ וגם $B[j]<A[i+1]$, ואז האיבר ה-$r$ בגודלו הוא $\max(A[i],B[j])$.
- אם $A[i+1]<B[j]$, גם $A[i+1]$ צריך להיות בין $r$ הקטנים, ולכן צריך לקחת יותר איברים מ-$A$ ($i$ גדל).
- אם $B[j+1]<A[i]$, לקחנו יותר מדי איברים מ-$A$ ($i$ קטן).

**זמן ריצה.** טווח החיפוש $[lo,hi]$ מכיל בהתחלה $r+1$ ערכים, ובכל איטרציה הוא קטן לפחות בחצי בעבודה של $O(1)$. לכן מספר האיטרציות הוא $O(\log r)$, ובמקרה הגרוע $\Theta(\log r)$.""")

SOL_2A = r"""הפתרון הרשמי עם תיקון: בשורה הרביעית ובשורה האחרונה הודפס $T(i,j-1,k)$ ולא הייתה שורה למקרה $S_1[i]\ne S_3[k]$ וגם $S_2[j]\ne S_3[k]$; הנכון הוא $T(i,j-1,k-1)$ בשתי השורות, ושורה נוספת שמחזירה שקר בכל מקרה אחר.
**משמעות הקלט:** האינדקסים הם התו האחרון בכל מחרוזת בהתאמה. $T(i,j,k)$ הוא אמת אם ורק אם הרישא $S_3[1..k]$ היא מחרוזת שילוב של הרישות $S_1[1..i]$ ו-$S_2[1..j]$. התשובה לבעיה היא $T(|S_1|,|S_2|,|S_3|)$.
$$T(i,j,k)=\begin{cases}true & i=j=k=0\\ T(i-1,j,k-1)\ \lor\ T(i,j-1,k-1) & i,j,k>0,\ S_1[i]=S_2[j]=S_3[k]\\ T(i-1,j,k-1) & i,j,k>0,\ S_1[i]=S_3[k],\ S_2[j]\ne S_3[k]\\ T(i,j-1,k-1) & i,j,k>0,\ S_1[i]\ne S_3[k],\ S_2[j]=S_3[k]\\ false & i,k>0,\ j=0,\ S_1[i]\ne S_3[k]\\ false & i=0,\ j,k>0,\ S_2[j]\ne S_3[k]\\ T(i-1,j,k-1) & i,k>0,\ j=0,\ S_1[i]=S_3[k]\\ T(i,j-1,k-1) & i=0,\ j,k>0,\ S_2[j]=S_3[k]\\ false & \text{otherwise}\end{cases}$$
**הסבר.** התו האחרון $S_3[k]$ של מחרוזת שילוב הוא התו האחרון של $S_1[1..i]$ או של $S_2[1..j]$. אם הוא שווה ל-$S_1[i]$ אפשר לשייך אותו ל-$S_1$ ולהמשיך עם $(i-1,j,k-1)$, ואם הוא שווה ל-$S_2[j]$ אפשר לשייך אותו ל-$S_2$ ולהמשיך עם $(i,j-1,k-1)$; בכל צעד גם $k$ קטן באחד. אם הוא שונה משניהם, אין שילוב. השורה האחרונה מכסה גם את המקרים $k=0<i+j$ ו-$i=j=0<k$, כך שאם $|S_3|\ne|S_1|+|S_2|$ התשובה היא שקר."""

CODE_4A = r"""Longest_Border(S[1..n])
   pi[1] <- 0
   k <- 0
   for q <- 2 to n
      while k > 0 and S[k+1] != S[q]
         k <- pi[k]
      if S[k+1] = S[q]
         k <- k+1
      pi[q] <- k
   return pi[n]"""

SOL_4A = (r"""הפתרון הרשמי עם תיקון: הודפס "חישוב מערך $\pi$ כפי שהוגדר באלגוריתם KMP והחזרת הערך המקסימלי במערך"; הנכון הוא להחזיר את הערך האחרון $\pi[n]$ (עבור `abcabcd` המקסימום הוא $3$ אבל אין רישא שהיא גם סיפא, והתשובה $0$).
הפתרון הרשמי מציין שלפי נוסח השאלה התשובה היא אורך המחרוזת (כל מחרוזת היא רישא וסיפא של עצמה), אבל הדוגמה `aabcdaabc` מתייחסת לרישא קצרה מהמחרוזת, ולכן התקבלה גם התשובה לפי ההגדרה הזו (רישא אמיתית שהיא גם סיפא). לפי ההגדרה הזו:
""" + "```\n" + CODE_4A + "\n```\n" + r"""**נכונות.** לפי הגדרת פונקציית הרישא, $\pi[q]$ הוא אורך הרישא האמיתית הארוכה ביותר של $S[1..q]$ שהיא גם סיפא של $S[1..q]$. עבור $q=n$ זה בדיוק הפלט המבוקש. הערך המקסימלי במערך מתאר רישא שהיא סיפא של רישא כלשהי של $S$, ולא בהכרח של $S$ כולה.
**זמן ריצה.** $O(n)$, כמו חישוב פונקציית הרישא ב-KMP: $k$ גדל לכל היותר $n-1$ פעמים, וכל איטרציה של לולאת ה-while מקטינה אותו.
דוגמה: עבור `aabcdaabc` מתקבל $\pi[9]=4$ (`aabc`). עבור `aaaa` מתקבל $\pi[4]=3$; התשובה $4$ שבדוגמה מתאימה לקריאה המילולית, שבה מחזירים את $n$.""")

SOL_5A = r"""**לא נכון.** שורש בעץ של היער $\Pi$ הוא קודקוד $v$ שעבורו $\Pi[v]=NIL$. כדי לדעת אם קודקוד הוא שורש צריך לבדוק את הערך שלו: אלגוריתם שלא בודק את $\Pi[v]$ (או את $D[v]$, $F[v]$) של קודקוד כלשהו לא יכול לדעת אם $v$ הוא שורש. לכן צריך לעבור על כל $|V|$ הקודקודים, וזמן הריצה הוא $\Theta(|V|)$, לא לינארי בכמות השורשים (למשל כשיש שורש אחד בלבד)."""

SOL_5B = r"""**נכון.** עלה ביער $\Pi$ הוא קודקוד שאינו אב של אף קודקוד. אפשר לעבור פעם אחת על המערך $\Pi$ ולסמן כל קודקוד $\Pi[v]\ne NIL$ כ"אב"; הקודקודים שלא סומנו הם העלים. לחלופין, $v$ הוא עלה אם ורק אם $F[v]=D[v]+1$ (בין הגילוי לסיום של $v$ לא התגלה אף קודקוד). בשני המקרים הזמן הוא $O(|V|)$."""

questions = [
    Q(1, "א", "algorithm", "divide_conquer",
      r"כתבו פסודו קוד/אלגוריתם רקורסיבי למציאת החציון במערך המאוחד של $A,B$. זמן הריצה הנדרש $\theta(\log n)$.",
      SOL_1A, points=10, contextId="c1", confidence="med"),
    Q(1, "ב", "proof", "complexity_recurrence",
      r"הוכח שסיבוכיות זמן הריצה של הפסודו קוד/אלגוריתם שהצגתם בסעיף הקודם הינו $\theta(\log n)$.",
      SOL_1B, points=5, contextId="c1"),
    Q(1, "ג", "algorithm", "divide_conquer",
      r"כתבו פסודו קוד/אלגוריתם למציאת האיבר ה-$r$ בגודלו במערך המאוחד של $A,B$, כאשר $1\le r\le\frac{n}{2}$. זמן הריצה הנדרש $\theta(\log r)$.",
      SOL_1C, points=10, contextId="c1", **SOLVED),

    Q(2, "א", "algorithm", "dp_sequences",
      r"כתבו נוסחה רקורסיבית $T(i,j,k)$ המקבלת שלושה אינדקסים אי שליליים מחזירה אמת אם המחרוזת $S_3$ הינה \"מחרוזת שילוב\" של $S_1,S_2$, אחרת, שקר." "\n"
      r"פרטו מה מייצג הקלט בנוסחה $T$.",
      SOL_2A, points=15, contextId="c2", **SOLVED),
    Q(2, "ב", "computation", "dp_sequences",
      r"הדגימו בצורה ברורה את חישוב הנוסחה הרקורסיבית עבור הקלט הבא: $S_1=$`ebc`, $S_2=$`dec`.",
      None, points=5, contextId="c2",
      hold="no-text: the printed input gives only S1=ebc and S2=dec; S3 is missing, so the demonstration cannot be "
           "written (the solution file only says that similar demonstrations were done in the course)"),
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
      SOL_4A, points=10, contextId="c4a", **SOLVED),
    Q(4, "ב", "algorithm", "suffix_structures",
      r"כתוב פסודו קוד/אלגוריתם היעיל ביותר לפתרון הבעיה.", SOL_4B, points=10, contextId="c4b"),
    Q(4, "ג", "computation", "suffix_structures",
      r"מהו זמן הריצה של האלגוריתם שהצעתם לבעיה בסעיף (ב)? נמקו קביעתכם.", SOL_4C, points=5, contextId="c4b"),

    Q(5, "א", "truefalse", "graphs_search",
      r"ניתן לאפיין את כל שורשי העצים ביער $\Pi$ בזמן לינארי בכמות שורשי העצים ביער." "\n" r"נכון / לא נכון",
      SOL_5A, points=5, contextId="c5", verdict=False, **SOLVED),
    Q(5, "ב", "truefalse", "graphs_search",
      r"ניתן לאפיין את כל העלים ביער $\Pi$ בזמן לינארי בכמות הקודקודים ביער." "\n" r"נכון / לא נכון",
      SOL_5B, points=5, contextId="c5", verdict=True, **SOLVED),
    Q(5, "ג", "truefalse", "graphs_search",
      r"לא ניתן לאפיין בזמן לינארי בגודל הגרף את כל סוגי הצלעות (צלע מהעץ, צלע חוזרת, צלע מקצרת מסלול בעץ, צלע חוצה בין עצים/תתי עצים)." "\n" r"נכון / לא נכון",
      None, points=5, contextId="c5",
      hold="ambiguous: the answer depends on what 'linear in the size of the graph' means for an adjacency matrix. "
           "With D, F and Pi every edge is classified in O(1), so the classification is linear in the matrix size "
           "Theta(V^2) (statement false); but listing the edges of a matrix takes Theta(V^2), not O(V+E) (statement "
           "true). No key; see docs/ASK_ADIR.md"),
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
