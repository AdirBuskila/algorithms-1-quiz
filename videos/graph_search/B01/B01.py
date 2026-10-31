# -*- coding: utf-8 -*-
"""B01 · BFS: תור, שכבות ומרחקים — video script (build: tools/video/vid.py B01).

Source: courses/graph_search/C01.js (lesson + goal: run BFS by hand, discovery order, layer and parent of every vertex).
Exam part: an original "בסגנון מבחן" question (bank={}): the bank has no fresh BFS-run question; the graph questions it
has that no guided quiz uses are proofs/algorithms that later videos of this course take (B02, B06, B07, B08).
Not used on purpose: the C01 quiz graph (A-C, A-D, B-C, C-E, D-E, E-F, F-G) and its questions (order, d[G], π[E], the
queue after A and C), 25A-B-Q5b (the C01 bank item). The graph here is new and drawn only in this video.
Every order, layer, parent and queue content below comes from w_graph_search (graph_ref.py = the app's graph.js, an
independent BFS and networkx).
"""
from vid import P, Scene, Video, show, hide
import stage as st
import w_graph_search as w
from w_graph_search import S

# ---------------------------------------------------------------- the graph (verified)
N = list("ABCDEFGS")
E = [("S", "B"), ("S", "D"), ("A", "B"), ("A", "E"), ("B", "C"), ("C", "D"), ("C", "F"), ("E", "F"), ("D", "G"),
     ("F", "G")]
POS = {"S": (60, 230), "B": (210, 110), "D": (210, 350), "A": (370, 40), "C": (370, 230), "G": (370, 410),
       "E": (560, 60), "F": (560, 280)}
LAB = {"S": (0, 58), "A": (-58, 0), "E": (64, 0), "B": (-10, -56), "C": (52, -36), "G": (60, 20), "F": (52, 40),
       "D": (-58, 16)}

G1 = w.Graph("g", N, E, False, POS, lab_at=LAB, scale=1.08)
R = G1.bfs("S")
assert R.order == ["S", "B", "D", "A", "C", "G", "E", "F"]
assert R.d == {"S": 0, "B": 1, "D": 1, "A": 2, "C": 2, "G": 2, "E": 3, "F": 3}
assert R.pi["F"] == "C" and set(R.adj["F"]) == {"C", "E", "G"}
assert R.order.index("C") < R.order.index("E") and R.order.index("C") < R.order.index("G")   # C leaves first
assert R.pi["G"] == "D" and R.d["G"] == 2
assert R.queue_at(1) == ["B", "D"] and R.queue_at(2) == ["D", "A", "C"]
R.labels()

# exam (original): BFS from E on the same graph, discovery order
G2 = w.Graph("x", N, E, False, POS, lab_at=LAB, scale=0.92)
X = G2.bfs("E")
TRUE = X.order
assert TRUE == ["E", "A", "F", "B", "C", "G", "S", "D"]
LAYER_ALPHA = sorted(N, key=lambda v: (X.d[v], v))                    # the trap: alphabetical inside each layer
DFS_ORDER = G2.dfs("E").order


def lifo(adj, s):                                                     # a stack instead of the queue
    stk, seen, out = [s], {s}, [s]
    while stk:
        u = stk.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                out.append(v)
                stk.append(v)
    return out


LIFO = lifo(X.adj, "E")
OPTS_RAW = {"a": TRUE, "b": LAYER_ALPHA, "c": DFS_ORDER, "d": LIFO}
assert len({tuple(v) for v in OPTS_RAW.values()}) == 4                  # four different orders
assert [k for k, v in OPTS_RAW.items() if v == X.order] == ["a"]
assert LAYER_ALPHA[-2:] == ["D", "S"] and TRUE[-2:] == ["S", "D"]
assert X.pi["S"] == "B" and X.pi["D"] == "C" and X.d["S"] == X.d["D"] == 3
assert X.order.index("B") < X.order.index("C")                          # B leaves the queue before C
X.labels()
OPTS = [(k, ", ".join(OPTS_RAW[k])) for k in ("b", "d", "a", "c")]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    S("בסרטון הזה נריץ BFS בעיפרון, צעד אחר צעד."),
    S("נראה את התור, את השכבות, ואת האב של כל קודקוד."),
    S("ובסוף נפתור שאלה בסגנון מבחן, עם המלכודת שלה.", hold=0.4),
], stage='<div class="kicker">B01 · גרפים: BFS ו-DFS</div><h1>BFS: תור, שכבות ומרחקים</h1>'
         '<p>להריץ BFS בעיפרון: סדר הגילוי, השכבה של כל קודקוד והאב שלו.</p>', layout="title")

ADJ = w.table("adj", ["קודקוד", "שכנים"], [[f"${v}$", ", ".join(R.adj[v])] for v in sorted(N)], hidden=False)
idea = Scene("idea", "הרעיון", [
    S("במבחן הגרף נשמר כרשימת סמיכויות: לכל קודקוד, רשימה של השכנים שלו.", do=show("i-g", "i-adj")),
    S("כדי לעבור על השכנים של קודקוד, עוברים על הרשימה שלו."),
    S("BFS מתחיל בקודקוד מקור, ומתקדם שכבה אחר שכבה בעזרת **תור**: נכנס ראשון, יוצא ראשון.", do=show("i-c2")),
    S("כל קודקוד הוא לבן, אפור או שחור. לבן: עוד לא התגלה. אפור: התגלה ומחכה בתור. שחור: טופל.",
      do=show("i-c3")),
    S("שולפים קודקוד מראש התור, ועוברים על השכנים שלו לפי סדר הרשימה. כאן הסדר אלפביתי.", do=show("i-c4")),
    S("כל שכן **לבן** מתגלה: השכבה שלו גדולה באחת מזו של מי שגילה אותו, והוא נכנס לסוף התור.",
      do=show("i-c5"), hold=0.3),
    S("והאב שלו הוא מי שגילה אותו. שכן אפור או שחור? מדלגים עליו."),
], stage=f'<div class="gs-row"><div id="i-g" class="h">{w.Graph("ig", N, E, False, POS, lab_at=LAB, scale=0.9).html()}'
         f'</div><div id="i-adj" class="h">{ADJ}</div></div>',
   panel=st.card("i-c2", "ex", "תור: נכנס ראשון, יוצא ראשון")
         + st.card("i-c3", "ex", "⚪ לבן · 🔘 אפור · ⚫ שחור")
         + st.card("i-c4", "plain", "שכנים לפי סדר הרשימה (כאן: אלפביתי)")
         + st.card("i-c5", "rule", "🔑 שכן לבן $v$ של $u$: $d[v]=d[u]+1$, $\\pi[v]=u$"))

run_ph = [
    S("נריץ BFS מהמקור $S$. בהתחלה רק $S$ בתור, השכבה שלו 0, ואין לו אב.", do=R.start_do("q")),
    *R.phrases(qpfx="q"),
    S("התור התרוקן. כל הקודקודים שחורים, ולכל אחד שכבה ואב.", do=R.end_do() + show("r-c1")),
    S("שימו לב לשלושה דברים. ראשון: השכבה נקבעת ברגע ה**גילוי**, לא ברגע השליפה.", do=show("r-c2")),
    S("למשל $G$ קיבל שכבה 2 כש-$D$ גילה אותו, הרבה לפני שהוא עצמו יצא מהתור.",
      do=show(G1.mark("G"))),
    S("שני: ל-$F$ יש שלושה שכנים: $C$, $E$ ו-$G$. מי האב שלו?",
      do=hide(G1.mark("G")) + show(G1.mark("F"), "r-c3")),
    S("זה $C$, כי $C$ יצא מהתור ראשון מבין השלושה. מי שיוצא ראשון, מגלה ראשון.",
      do=show(G1.mark("C"))),
    S("ושלישי: קודקוד מתגלה **פעם אחת בלבד**. לכן יש לו אב אחד, והצלעות הירוקות יוצרות עץ.",
      do=hide(G1.mark("F"), G1.mark("C")) + show("r-c4"), hold=0.4),
]
run = Scene("run", "הרצה", run_ph,
            stage=f'<div class="gs-stack">{G1.html()}{w.queue("q", R.order)}</div>',
            panel=st.card("r-c1", "ex", "סדר הגילוי: " + ", ".join(R.order))
                  + st.card("r-c2", "rule", "🔑 $d[v]$ נקבע ב<b>גילוי</b>")
                  + st.card("r-c3", "rule", "🔑 האב: השכן שיצא <b>ראשון</b> מהתור")
                  + st.card("r-c4", "rule", "🔑 גילוי אחד ← אב אחד ← עץ BFS"))

ex_ph = [
    S("ועכשיו שאלה בסגנון מבחן. אותו גרף, אבל הפעם BFS מהקודקוד $E$, שכנים בסדר אלפביתי.", do=show("x-gw")),
    S("מה סדר הגילוי של הקודקודים? יש ארבע אפשרויות.", do=show("x-opts")),
    S("לא מנחשים: מריצים. התור מתחיל ב-$E$, בשכבה 0.", do=X.start_do("xq")),
    *X.phrases(qpfx="xq"),
    S("קיבלנו את הסדר, וזו האפשרות הנכונה.", do=X.end_do() + show("x-ok-a")),
    S("והמלכודת: ב-$S$ וב-$D$ יש אותה שכבה, 3. מי שממיין כל שכבה לפי האלף בית שם את $D$ לפני $S$.",
      do=show(G2.mark("S"), G2.mark("D"), "x-x-b", "x-n-b")),
    S("אבל $S$ התגלה דרך $B$, ו-$D$ דרך $C$. ו-$B$ יצא מהתור לפני $C$, ולכן $S$ התגלה קודם.",
      do=show(G2.mark("B"), G2.mark("C"))),
    S("שתי האפשרויות האחרות הן בכלל לא BFS: אחת היא סדר של DFS, והשנייה מחליפה את התור במחסנית.",
      do=hide(G2.mark("S"), G2.mark("D"), G2.mark("B"), G2.mark("C")) + show("x-x-c", "x-n-c", "x-x-d", "x-n-d"),
      hold=0.5),
]
exam = Scene("exam", "שאלה בסגנון מבחן", ex_ph,
             stage=f'<div class="gs-stack"><div id="x-gw" class="h">{G2.html()}</div>{w.queue("xq", X.order)}</div>',
             panel='<div class="gs-q"><span class="qid">בסגנון מבחן</span>מריצים BFS מ-$E$ על הגרף (שכנים בסדר '
                   'אלפביתי). מהו סדר הגילוי?</div>'
                   + f'<div id="x-opts" class="h gs-opts">'
                   + st.options("x", OPTS, notes={"b": "מיון בתוך שכבה", "c": "זה DFS", "d": "מחסנית"})
                   + "</div>")

recap = Scene("recap", "סיכום", [
    S("לסיכום: BFS מחזיק תור. שולפים מהראש, ומכניסים לסוף רק שכנים לבנים.", do=show("s-1")),
    S("השכבה והאב נקבעים ברגע הגילוי, והאב הוא מי ששלפנו ראשון מבין השכנים.", do=show("s-2")),
    S("וסדר הגילוי הוא סדר הכניסה לתור, לא סדר האלף בית. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage='<div class="gs-stack">'
         + st.card("s-1", "rule", "🔑 תור: שולפים מהראש, לבנים נכנסים לסוף")
         + st.card("s-2", "rule", "🔑 $d[v]=d[u]+1$ ו-$\\pi[v]=u$ ברגע הגילוי")
         + "</div>",
   panel=st.card("s-3", "trap", "⚠️ סדר הגילוי = סדר הכניסה לתור, לא אלפביתי"))

VIDEO = Video("B01", "graph_search", "BFS: תור, שכבות ומרחקים", [title, idea, run, exam, recap], bank={})
