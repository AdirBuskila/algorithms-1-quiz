# -*- coding: utf-8 -*-
"""B03 · DFS: זמני גילוי וסיום — video script (build: tools/video/vid.py B03).

Source: courses/graph_search/C03.js (lesson + goal: run DFS by hand, discovery/finish time and parent of every vertex,
and read the DFS forest from the times).
Exam part: an original "בסגנון מבחן" question (bank={}): a table of discovery/finish times, which statement is true.
The bank has no fresh DFS-times question (25A-A-Q5a/b are the C03 quiz items).
Not used on purpose: the C03 quiz graph (A-B, A-E, B-C, B-D, E-F, G isolated) and its questions (d[E], f[A], |E_DFS|,
the 2/9, 4/5 intervals), 25A-A-Q5a/b. The run graph and the exam table here are new.
Every time, parent, root and leaf comes from w_graph_search (graph_ref.py = the app's graph.js, an own DFS, networkx).
"""
from vid import P, Scene, Video, show, hide
import stage as st
import w_graph_search as w
from w_graph_search import S

# ---------------------------------------------------------------- the run (verified)
N = list("ABCDEFGH")
E = [("A", "D"), ("A", "F"), ("B", "D"), ("D", "E"), ("E", "F"), ("C", "G"), ("C", "H")]
POS = {"A": (80, 230), "D": (260, 160), "B": (260, 340), "E": (440, 160), "F": (330, 30), "C": (600, 180),
       "G": (540, 340), "H": (660, 340)}
LAB = {"D": (62, 40), "C": (100, 0)}
G1 = w.Graph("g", N, E, False, POS, w=700, h=400, scale=1.0, lab_at=LAB)
R = G1.dfs()
assert R.order == ["A", "D", "B", "E", "F", "C", "G", "H"]
assert [R.disc[v] for v in R.order] == [1, 2, 3, 5, 6, 11, 12, 14]
assert R.fin == {"B": 4, "F": 7, "E": 8, "D": 9, "A": 10, "G": 13, "H": 15, "C": 16}
assert R.roots == ["A", "C"] and R.pi["F"] == "E" and R.kind("F", "A") == "back"
LEAVES = [v for v in N if R.fin[v] == R.disc[v] + 1]
assert sorted(LEAVES) == ["B", "F", "G", "H"] == sorted(v for v in N if v not in R.pi.values())
assert len([v for v in N if R.pi[v] is not None]) == len(N) - len(R.roots) == 6
R.time_labels()
PH = R.phrases(spfx="st", ppfx="pa", narrate=(), edges=("tree",))
GROUPS = R.groups(narrate=())
assert [k for k, _ in GROUPS] == ["disc", "fin", "disc", "fin", "fin", "disc", "fin", "disc", "fin"], GROUPS
assert [e[1] for e in GROUPS[4][1]] == ["A"]
# group 1 is B's finish only, group 3 finishes F, E, D (three), the F-A edge is examined (silently) before F finishes
assert [e[1] for e in GROUPS[1][1] if e[0] == "fin"] == ["B"]
assert [e[1] for e in GROUPS[3][1] if e[0] == "fin"] == ["F", "E", "D"]
# A examines F after D finished: F is already black, nothing new
assert R.adj["A"] == ["D", "F"] and R.fin["F"] < R.fin["D"]

# ---------------------------------------------------------------- exam (original): read a table of times
NX = list("PQRTUW")
EX = [("P", "Q"), ("Q", "R"), ("P", "U"), ("U", "R"), ("T", "W")]            # hidden: only the times are shown
X = w.Graph("hx", NX, EX, True, {v: (0, 0) for v in NX}).dfs()
TIMES = {v: (X.disc[v], X.fin[v]) for v in NX}
assert TIMES == {"P": (1, 8), "Q": (2, 5), "R": (3, 4), "U": (6, 7), "T": (9, 12), "W": (10, 11)}


def anc(a, b):                     # a is a proper ancestor of b in the forest (by π)
    x = X.pi[b]
    while x is not None:
        if x == a:
            return True
        x = X.pi[x]
    return False


nest = lambda a, b: TIMES[a][0] < TIMES[b][0] and TIMES[b][1] < TIMES[a][1]
for a in NX:
    for b in NX:
        if a != b:
            assert anc(a, b) == nest(a, b)                                 # the parenthesis theorem on this run
ROOTS = [v for v in NX if not any(nest(u, v) for u in NX if u != v)]
assert ROOTS == X.roots == ["P", "T"]
CLAIMS = {"a": anc("P", "R"), "b": anc("Q", "U"), "c": TIMES["Q"][1] == TIMES["Q"][0] + 1, "d": len(ROOTS) == 3}
assert CLAIMS == {"a": True, "b": False, "c": False, "d": False}
assert X.pi["R"] == "Q" and X.pi["U"] == "P"
OPTS = [("b", "$U$ צאצא של $Q$"), ("c", "$Q$ הוא עלה ביער"), ("a", "$R$ צאצא של $P$"), ("d", "ביער יש שלושה עצים")]
IV = w.intervals("iv", [(v, *TIMES[v]) for v in NX], 12, unit=50, row=52)
TAB = w.table("tt", ["", *NX], [["$d$", *[str(TIMES[v][0]) for v in NX]], ["$f$", *[str(TIMES[v][1]) for v in NX]]],
              hidden=False)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    S("בסרטון הזה נריץ DFS בעיפרון, ונרשום לכל קודקוד שני זמנים."),
    S("ואז נלמד לקרוא את הזמנים: מי צאצא של מי, מי עלה, וכמה עצים יש ביער."),
    S("ובסוף שאלה בסגנון מבחן, שנפתרת רק מטבלת זמנים.", hold=0.4),
], stage='<div class="kicker">B03 · גרפים: BFS ו-DFS</div><h1>DFS: זמני גילוי וסיום</h1>'
         '<p>להריץ DFS בעיפרון, לרשום לכל קודקוד זמן גילוי, זמן סיום ואב, ולקרוא מהם את יער ה-DFS.</p>',
   layout="title")

idea = Scene("idea", "הרעיון", [
    S("DFS הולך לעומק: מקודקוד עוברים לשכן לבן, ממנו לשכן לבן שלו, וחוזרים אחורה רק כשנתקעים.", do=show("i-1")),
    S("במקום תור יש רקורסיה, כלומר מחסנית.", do=show("i-2")),
    S("יש שעון אחד, שמתחיל באפס. כשקודקוד מתגלה, השעון מתקדם באחת, וזה זמן הגילוי שלו.", do=show("i-3")),
    S("כשסיימנו את כל השכנים שלו, השעון מתקדם שוב, וזה זמן הסיום.", do=show("i-4")),
    S("והלולאה החיצונית מתחילה DFS מכל קודקוד שעדיין לבן. לכן מקבלים **יער**, ולא בהכרח עץ אחד.",
      do=show("i-5"), hold=0.4),
], stage='<div class="gs-stack">'
         + st.card("i-1", "ex", "לעומק: שכן לבן ← השכן הלבן שלו ← … ← חזרה כשנתקעים")
         + st.card("i-2", "plain", "רקורסיה = מחסנית (ב-BFS: תור)")
         + "</div>",
   panel=st.card("i-3", "rule", "🔑 גילוי: $time{+}{+}$, $d[u]=time$, אפור")
         + st.card("i-4", "rule", "🔑 סיום: $time{+}{+}$, $f[u]=time$, שחור")
         + st.card("i-5", "ex", "לולאה חיצונית על כל לבן ← <b>יער</b>"))

run_ph = [
    S("נריץ DFS על הגרף הזה. השכנים, וגם הלולאה החיצונית, בסדר אלפביתי.", do=show("r-g")),
    *PH[:1],
    S("$B$ בלי שכנים לבנים: הוא נתקע מיד, ומסתיים בזמן 4. חוזרים ל-$D$.", do=PH[1].do),
    *PH[2:3],
    S("$F$ בוחן את $A$, אבל $A$ אפור: לא מגלים אותו שוב. אז $F$ מסתיים, ואחריו $E$ ו-$D$.", do=PH[3].do),
    S("$A$ בודק את השכן הבא שלו, $F$, אבל הוא כבר שחור. אז $A$ מסתיים בזמן 10.", do=PH[4].do),
    *PH[5:],
    S("כל קודקוד קיבל שני זמנים שונים, מ-1 עד 16, פעמיים מספר הקודקודים.", do=show("r-c1")),
    S("ושני שורשים, $A$ ו-$C$: יער של שני עצים.", do=show(G1.mark("A"), G1.mark("C"), "r-c2"), hold=0.4),
]
run = Scene("run", "הרצה", run_ph,
            stage=f'<div class="gs-stack"><div id="r-g" class="h">{G1.html(kinds=("tree",))}</div>'
                  f'{w.stack("st", R)}{w.parens("pa", R)}</div>',
            panel=st.card("r-c1", "ex", "הזמנים מ-1 עד $2|V|$, כל אחד פעם אחת")
                  + st.card("r-c2", "rule", "🔑 שורש: $\\pi=\\text{NIL}$. כאן $A$ ו-$C$"))

GP = w.Graph("gp", N, E, False, POS, w=700, h=400, scale=0.9, lab_at=LAB)
RP = GP.dfs()
assert RP.disc == R.disc and RP.fin == R.fin
RP.time_labels()
read = Scene("read", "קוראים את הזמנים", [
    S("עכשיו נקרא את הזמנים. כל קודקוד הוא זוג סוגריים: נפתח בגילוי, ונסגר בסיום.", do=show("p-par")),
    S("**משפט הסוגריים**: שני קטעים הם זרים, או שאחד מוכל לגמרי בשני. אף פעם לא חיתוך חלקי.", do=show("p-c1")),
    S("קטע מוכל בקטע אחר בדיוק כשהקודקוד הוא צאצא. למשל הקטע של $F$, משש עד שבע, בתוך הקטע של $D$.",
      do=show("p-c2")),
    S("**עלה**: לא התגלה אף קודקוד בין הגילוי לסיום שלו, כלומר $f=d+1$. כאן $B$, $F$, $G$ ו-$H$.",
      do=show("p-c3"), say_="עלה: לא התגלה אף קודקוד בין הגילוי לסיום שלו, כלומר אֶף שווה דִּי ועוד אחת. "
                            "כאן בִּי, אֶף, גִ'י ואֵייץ'."),
    S("ומספר צלעות העץ: שמונה קודקודים פחות שני עצים, שש צלעות.", do=show("p-c4"), hold=0.4),
], stage=f'<div class="gs-stack"><div id="p-par">{w.parens("pp", R).replace(" h", "")}</div>'
         f'<div>{w.final_dfs_html(GP, RP)}</div></div>',
   panel=st.card("p-c1", "rule", "🔑 קטעים: זרים או מוכלים, לא חיתוך חלקי")
         + st.card("p-c2", "ex", "$[6,7]\\subset[2,9]$: $F$ צאצא של $D$")
         + st.card("p-c3", "rule", "🔑 עלה: $f[v]=d[v]+1$")
         + st.card("p-c4", "rule", "🔑 $|E_{DFS}|=|V|-k=8-2=6$"))

ex_ph = [
    S("ועכשיו שאלה בסגנון מבחן. בריצת DFS על גרף כלשהו התקבלו הזמנים בטבלה. מה נכון?", do=show("x-opts")),
    S("את הגרף לא צריך. נצייר כל קודקוד כקטע, מזמן הגילוי עד זמן הסיום.",
      do=show(*[f"iv-b-{v}" for v in NX])),
    S("הקטע של $R$, שלוש עד ארבע, נמצא בתוך הקטע של $P$, אחת עד שמונה. לכן $R$ צאצא של $P$.",
      do=show("iv-h-R", "iv-h-P", "x-ok-a")),
    S("הקטע של $U$, שש עד שבע, והקטע של $Q$, שתיים עד חמש, זרים. אין ביניהם קשר של אב וצאצא.",
      do=hide("iv-h-R", "iv-h-P") + show("iv-h-U", "iv-h-Q", "x-x-b", "x-n-b")),
    S("$Q$ אינו עלה: בין שתיים לחמש התגלה $R$. עלה מקיים $f=d+1$.",
      do=hide("iv-h-U") + show("iv-h-R", "x-x-c", "x-n-c"),
      say_="קְיוּ אינו עלה: בין שתיים לחמש התגלה אָר. עלה מקיים אֶף שווה דִּי ועוד אחת."),
    S("ושורשים הם הקטעים שאף קטע לא מכיל אותם: $P$ ו-$T$. שני עצים, לא שלושה.",
      do=hide("iv-h-Q", "iv-h-R") + show("iv-h-P", "iv-h-T", "x-x-d", "x-n-d")),
    S("המלכודת: לחפש את הגרף. כל התשובות כאן נקראות מהזמנים בלבד, בזכות משפט הסוגריים.", do=show("x-t"),
      hold=0.5),
]
exam = Scene("exam", "שאלה בסגנון מבחן", ex_ph,
             stage=f'<div class="gs-stack">{TAB}{IV}</div>',
             panel='<div class="gs-q"><span class="qid">בסגנון מבחן</span>בריצת DFS התקבלו הזמנים שבטבלה. מה נכון '
                   'בהכרח?</div>'
                   + f'<div id="x-opts" class="h gs-opts">'
                   + st.options("x", OPTS, notes={"b": "קטעים זרים", "c": "$R$ בפנים", "d": "2 שורשים"})
                   + "</div>"
                   + st.card("x-t", "trap", "⚠️ לא צריך את הגרף: הכל בזמנים"))

recap = Scene("recap", "סיכום", [
    S("לסיכום: גילוי מקדם את השעון ונותן זמן גילוי, וסיום מקדם אותו שוב ונותן זמן סיום.", do=show("s-1")),
    S("הקטעים זרים או מוכלים. מוכל פירושו צאצא, ועלה מקיים $f=d+1$.", do=show("s-2"),
      say_="הקטעים זרים או מוכלים. מוכל פירושו צאצא, ועלה מקיים אֶף שווה דִּי ועוד אחת."),
    S("וביער עם $k$ עצים יש מספר הקודקודים פחות $k$ צלעות עץ. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6,
      say_="וביער עם קֵיי עצים, יש מספר הקודקודים פחות קֵיי צלעות עץ. נתראה ברמה הבאה."),
], stage='<div class="gs-stack">'
         + st.card("s-1", "rule", "🔑 $d[u]<f[u]$, כל הזמנים שונים")
         + st.card("s-2", "rule", "🔑 קטע בתוך קטע ⇔ צאצא · עלה: $f=d+1$")
         + "</div>",
   panel=st.card("s-3", "rule", "🔑 $|E_{DFS}|=|V|-k$"))

VIDEO = Video("B03", "graph_search", "DFS: זמני גילוי וסיום", [title, idea, run, read, exam, recap], bank={})
