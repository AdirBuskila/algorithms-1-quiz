# -*- coding: utf-8 -*-
"""B06 · טענות על גרפים: הוכח או הפרך — video script (build: tools/video/vid.py B06).

Source: courses/graph_search/C06.js (lesson + goal: read a claim, decide refute-by-counterexample or prove, and build
the counterexample or the proof).
Exam anchor: 26A-B-Q2b (refute: in a DIRECTED graph two DFS trees rooted at s need not have the same depth), which no
guided quiz uses; solved with its counterexample run in code with both neighbour orders.
Not used on purpose: the C06 quiz claims ("degree >= 1 => connected", |d[u]-d[v]| <= 1 and its proof with the wrong line,
the directed d[v] <= d[u]+1, 24B-A-Q1a/b) and the lesson's "|E|=|V|-1 => tree" example. The two worked claims here are
new: "equal BFS layers => no edge between them" (refuted by a triangle) and "minimum degree 2 => a cycle" (proved with a
DFS leaf). 26A-B-Q2a (the BFS twin of the exam claim) is the B07 exam and is only mentioned, not solved, here.
Every run is computed by w_graph_search; the proved claim is brute-forced on all graphs up to 6 vertices.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_graph_search as w
from w_graph_search import S

# ---------------------------------------------------------------- claim 1 (false): equal layers => no edge
T = w.Graph("t", ["s", "a", "b"], [("s", "a"), ("s", "b"), ("a", "b")], False,
            {"s": (150, 40), "a": (50, 210), "b": (250, 210)}, w=300, h=260, lab_at={"s": (60, 0), "a": (-62, 0),
                                                                                      "b": (62, 0)})
RT = T.bfs("s")
assert RT.d == {"s": 0, "a": 1, "b": 1} and ("a", "b") in T.edges
RT.labels()

# ---------------------------------------------------------------- claim 2 (true): min degree >= 2 => a cycle


def has_cycle_undirected(V, Ed):
    g = w.nxg(V, Ed, False)
    return len(Ed) > 0 and len(w.nx.cycle_basis(g)) > 0


def dfs_leaf_back_edge(V, Ed):
    """the proof's construction: a leaf of the DFS forest has a back edge to a proper ancestor (not its parent)"""
    names = [str(v) for v in V]
    g = w.Graph("z", names, [(str(a), str(b)) for a, b in Ed], False, {v: (0, 0) for v in names})
    r = g.dfs()
    leaves = [v for v in names if v not in r.pi.values()]
    for leaf in leaves:
        others = [u for u in r.adj[leaf] if u != r.pi[leaf]]
        assert others, (V, Ed, leaf)                                         # degree >= 2
        for u in others:
            assert r.kind(leaf, u) == "back" and r.disc[u] < r.disc[leaf] < r.fin[leaf] < r.fin[u]
    return True


checked = 0
for n in range(3, 7):
    for V, Ed in w.all_graphs(n, False):
        deg = {v: 0 for v in V}
        for a, b in Ed:
            deg[a] += 1
            deg[b] += 1
        if min(deg.values()) >= 2:
            assert has_cycle_undirected(V, Ed) and dfs_leaf_back_edge(V, Ed)
            checked += 1
assert checked > 1000

NB = list("ABCDE")
EB = [("A", "B"), ("B", "C"), ("A", "C"), ("C", "D"), ("D", "E"), ("C", "E")]
GB = w.Graph("b", NB, EB, False, {"A": (60, 60), "B": (60, 260), "C": (230, 160), "D": (400, 60), "E": (400, 260)},
             w=460, h=320)
RB = GB.dfs()
assert RB.order == ["A", "B", "C", "D", "E"] and RB.pi["E"] == "D"
LEAF = [v for v in NB if v not in RB.pi.values()]
assert LEAF == ["E"] and RB.kind("E", "C") == "back" and RB.pi["D"] == "C"
TREE_IDS = [GB.eid(u, v, "tree") for u, v in EB if RB.kind(u, v) == "tree"]

# ---------------------------------------------------------------- exam 26A-B-Q2b
Q = BANK["26A-B-Q2b"]
assert "מכוון" in Q["question"] and "DFS" in Q["question"] and Q.get("correctId") is None
assert "הפרכה" in Q["solution"]
NX, EX = ["s", "a", "b"], [("s", "a"), ("s", "b"), ("a", "b")]
PX = {"s": (150, 40), "a": (50, 200), "b": (250, 200)}
G1 = w.Graph("x1", NX, EX, True, PX, w=300, h=330, lab_at={"s": (60, 0), "a": (-62, 0), "b": (62, 0)})
G2 = w.Graph("x2", NX, EX, True, PX, w=300, h=330, lab_at={"s": (60, 0), "a": (-62, 0), "b": (62, 0)})
R1 = G1.dfs("s", order={"s": ["a", "b"]})
R2 = G2.dfs("s", order={"s": ["b", "a"]})
assert all(w.nx.has_path(w.nxg(NX, EX, True), "s", v) for v in NX)          # every vertex reachable from s
assert R1.roots == R2.roots == ["s"]                                         # each run is one tree rooted at s
assert R1.pi == {"s": None, "a": "s", "b": "a"} and R2.pi == {"s": None, "a": "s", "b": "s"}
assert R1.pi != R2.pi and (R1.height, R2.height) == (2, 1)
assert R2.kind("a", "b") == "cross"
for G, R in ((G1, R1), (G2, R2)):
    for v in NX:
        G.lab(v, "dp", str(R.depth[v]), "gs-lp")


def tree_do(G, R):
    return show(*[G.eid(u, v, "tree") for u, v in EX if R.kind(u, v) == "tree"])


# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    S("רוב שאלות הגרפים במבחן הן: הוכיחו או הפריכו."),
    S("בסרטון הזה נלמד להחליט מה עושים, ונבנה הפרכה אחת והוכחה אחת."),
    S("ובסוף נפריך טענה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">B06 · גרפים: BFS ו-DFS</div><h1>טענות על גרפים: הוכח או הפרך</h1>'
         '<p>להחליט אם להפריך בדוגמה נגדית או להוכיח, ולבנות את הדוגמה או את ההוכחה.</p>', layout="title")

idea = Scene("idea", "הכמתים", [
    S("הצעד הראשון: לקרוא את הכמתים. ״בהכרח״, ״לכל גרף״, ״לכל סדר שכנים״: הטענה צריכה להתקיים **תמיד**.",
      do=show("i-1")),
    S("אז **דוגמה נגדית אחת** מפריכה אותה. ולהוכיח צריך נימוק כללי: דוגמאות שמתאימות לא מוכיחות כלום.",
      do=show("i-2")),
    S("ובטענה עם ״קיים״ זה הפוך: להוכיח מספיקה דוגמה, ולהפריך צריך להראות שכל בחירה נכשלת.", do=show("i-3")),
    S("ודוגמה נגדית טובה היא הקטנה ביותר, ומקיימת את **כל** התנאים של הטענה, ורק המסקנה נשברת בה.",
      do=show("i-4"), hold=0.4),
], stage='<div class="gs-stack">'
         + st.card("i-1", "plain", "״בהכרח״ / ״לכל״: חייב להתקיים <b>תמיד</b>")
         + st.card("i-2", "rule", "🔑 להפריך: דוגמה נגדית אחת. להוכיח: נימוק כללי")
         + st.card("i-3", "ex", "״קיים״: להוכיח בדוגמה, להפריך לכל בחירה")
         + "</div>",
   panel=st.card("i-4", "trap", "⚠️ הדוגמה מקיימת את <b>כל</b> התנאים, ורק המסקנה נשברת"))

refute = Scene("refute", "הפרכה", [
    S("טענה ראשונה: ב-BFS על גרף לא מכוון, אם לשני קודקודים יש אותה שכבה, אז אין ביניהם צלע.", do=show("a-c")),
    S("״אם״ בלי ״קיים״: זו טענה על **כל** גרף. נחפש דוגמה נגדית קטנה."),
    S("משולש: $s$, $a$ ו-$b$, וכל שלוש הצלעות.", do=show("a-g")),
    S("BFS מ-$s$ מגלה את $a$ ואת $b$, ושניהם בשכבה 1.", do=RT.all_do()),
    S("והצלע בין $a$ ל-$b$ קיימת. התנאי מתקיים, המסקנה נשברת: הטענה מופרכת.",
      do=show(T.eid("a", "b", "hl"), "a-ok"),
      say_="והצלע בין אֵיי לבִּי קיימת. התנאי מתקיים, המסקנה נשברת: הטענה מופרכת."),
    S("ומה כן נכון? שבגרף לא מכוון, השכבות של שני קצוות של צלע נבדלות **לכל היותר** באחת.", do=show("a-t"),
      hold=0.4),
], stage=f'<div id="a-g" class="h">{T.html(kinds=("tree", "hl"))}</div>',
   panel=st.card("a-c", "plain", "טענה: $d[u]=d[v]$ ← אין צלע $(u,v)$")
         + st.card("a-ok", "rule", "🔑 משולש: $d[a]=d[b]=1$, והצלע $(a,b)$ קיימת")
         + st.card("a-t", "ex", "מה שנכון: $|d[u]-d[v]|\\le 1$ לכל צלע"))

prove = Scene("prove", "הוכחה", [
    S("טענה שנייה: בגרף לא מכוון שבו לכל קודקוד יש לפחות שני שכנים, יש מעגל.", do=show("b-c")),
    S("ניסיונות לבנות דוגמה נגדית נכשלים, אז נוכיח. נריץ DFS ונסתכל על **עלה** בעץ.", do=show("b-g")),
    S("עלה קיים תמיד, כי העץ סופי. בגרף הזה זה $E$.",
      do=show(*TREE_IDS) + show(GB.mark("E"))),
    S("ל-$E$ יש לפחות שני שכנים. רק אחד מהם הוא האב שלו, $D$. אז יש לו שכן נוסף, $C$.", do=show("b-1")),
    S("הצלע אליו אינה צלע עץ: לעלה אין בנים, ו-$C$ אינו האב. ובגרף לא מכוון כל צלע היא עץ או אחורה.",
      do=show("b-2")),
    S("לכן זו צלע אחורה, ו-$C$ הוא אב קדמון של $E$.", do=show(GB.eid("C", "E", "back"))),
    S("מסלול העץ מ-$C$ אל $E$, ועוד הצלע חזרה, הם מעגל. וזה עובד בכל גרף, לא רק כאן.",
      do=show(GB.eid("C", "D", "hl"), GB.eid("D", "E", "hl"), "b-3")),
    S("ושימו לב לשימוש בתנאי: שני שכנים. עם שכן אחד, העלה היה מחובר רק לאב שלו.", hold=0.4),
], stage=f'<div id="b-g" class="h">{GB.html(kinds=("tree", "back", "hl"))}</div>',
   panel=st.card("b-c", "plain", "טענה: $\\deg(v)\\ge 2$ לכל $v$ ← יש מעגל")
         + st.card("b-1", "ex", "עלה $\\ell$: שכן נוסף מלבד האב")
         + st.card("b-2", "rule", "🔑 לא מכוון: כל צלע היא עץ או אחורה")
         + st.card("b-3", "rule", "🔑 צלע אחורה + מסלול העץ = מעגל"))

ex_ph = [
    S("ועכשיו סעיף ממבחן. בגרף $G$ כל הקודקודים ישיגים מ-$s$, ויש שני עצי DFS שונים, שניהם מושרשים ב-$s$."),
    S("הטענה: אם $G$ מכוון, אז בהכרח לשני העצים יש אותו עומק. הוכיחו או הפריכו.", do=show("x-c")),
    S("״בהכרח״: מספיקה דוגמה אחת. ועומק של DFS תלוי במה שהוא בוחר ללכת קודם, אז ננסה להפריך."),
    S("הגרף הכי קטן: $s$, $a$, $b$, עם צלעות מ-$s$ ל-$a$, מ-$s$ ל-$b$, ומ-$a$ ל-$b$.", do=show("x-g1", "x-g2"),
      say_="הגרף הכי קטן: אֶס, אֵיי ובִּי, עם צלעות מאֶס לאֵיי, מאֶס לבִּי, ומאֵיי לבִּי."),
    S("כל הקודקודים ישיגים מ-$s$, אז התנאי מתקיים.", do=show("x-k1")),
    S("סדר ראשון: $s$ בוחר קודם את $a$. מ-$a$ מגיעים ל-$b$, ומקבלים שרשרת בעומק 2.",
      do=tree_do(G1, R1) + show(*[G1.lid(v, "dp") for v in NX])),
    S("סדר שני: $s$ בוחר קודם את $b$. ל-$b$ אין צלעות יוצאות, אז חוזרים ל-$s$, והוא מגלה את $a$.",
      do=tree_do(G2, R2)),
    S("הצלע מ-$a$ ל-$b$ מוצאת את $b$ כבר שחור, ולא נכנסת לעץ. העומק: 1.",
      do=show(G2.eid("a", "b", "cross"), *[G2.lid(v, "dp") for v in NX]),
      say_="הצלע מאֵיי לבִּי מוצאת את בִּי כבר שחור, ולא נכנסת לעץ. העומק: אחת."),
    S("שני עצי DFS שונים מ-$s$, בעומקים 2 ו-1. הטענה מופרכת.", do=show("x-ok")),
    S("והמלכודת: מסלול כדוגמה. בו כל סדר נותן אותו עץ, ולכן הוא לא מפריך.",
      do=show("x-t"), hold=0.5),
]
exam = Scene("exam", "שאלה ממבחן", ex_ph,
             stage=f'<div class="gs-row"><div class="gs-col"><div id="x-g1" class="h">{G1.html(kinds=("tree",))}</div>'
                   '<div class="gs-cap">$s$ בוחר קודם את $a$ (בכחול: העומק)</div></div>'
                   f'<div class="gs-col"><div id="x-g2" class="h">{G2.html(kinds=("tree", "cross"))}</div>'
                   '<div class="gs-cap">$s$ בוחר קודם את $b$ (בכחול: העומק)</div></div></div>',
             panel=f'<div class="gs-q"><span class="qid">{Q["id"]}</span>כל הקודקודים ישיגים מ-$s$. '
                   '$T_{DFS}, T\'_{DFS}$ שני עצי DFS שונים המושרשים ב-$s$.</div>'
                   + st.card("x-c", "plain", "טענה: $G$ מכוון ← בהכרח $\\mathrm{depth}(T_{DFS})=\\mathrm{depth}(T'_{DFS})$")
                   + st.card("x-k1", "ex", "תנאים: מכוון ✓, הכל ישיג מ-$s$ ✓")
                   + st.card("x-ok", "rule", "🔑 עומקים $2\\ne1$: הטענה <b>לא נכונה</b>")
                   + st.card("x-t", "trap", "⚠️ מסלול לא מפריך: בו יש רק עץ אחד"))

recap = Scene("recap", "סיכום", [
    S("לסיכום: קוראים כמתים. ״בהכרח״ מופרך בדוגמה נגדית אחת, ומוכח רק בנימוק כללי.", do=show("s-1")),
    S("הדוגמה הנגדית קטנה, ומקיימת את כל התנאים. כותבים את הגרף, את ההרצה, ואת המקום שבו המסקנה נשברת.",
      do=show("s-2")),
    S("וההוכחה נשענת על מה שהאלגוריתם מבטיח, כמו עלה וצלע אחורה ב-DFS. נתראה ברמה הבאה.", do=show("s-3"),
      hold=0.6),
], stage='<div class="gs-stack">'
         + st.card("s-1", "rule", "🔑 ״בהכרח״: דוגמה נגדית אחת מפריכה")
         + st.card("s-2", "rule", "🔑 דוגמה: קטנה, כל התנאים, הרצה, המסקנה נשברת")
         + "</div>",
   panel=st.card("s-3", "ex", "הוכחה: עובדות האלגוריתם (עלה, צלע אחורה, שכבות)"))

VIDEO = Video("B06", "graph_search", "טענות על גרפים: הוכח או הפרך", [title, idea, refute, prove, exam, recap],
              bank={"26A-B-Q2b": None})
