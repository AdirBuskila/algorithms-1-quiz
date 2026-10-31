# -*- coding: utf-8 -*-
"""B07 · BFS מול DFS: עצים וטענות — video script (build: tools/video/vid.py B07).

Source: courses/graph_search/C07.js (lesson + goal: compare a BFS tree with a DFS tree: heights, who discovered each
vertex, and claims about them).
Exam anchor: 26A-B-Q2a (prove: two BFS trees rooted at s have the same depth), which no guided quiz uses; the two BFS
trees are run in code with two neighbour orders.
Not used on purpose: the C07 quiz graph (A-B, A-C, A-D, B-E, C-E, D-F, E-F) and its heights, and the C07 quiz claims:
"T_BFS = T_DFS only when G is a tree" (C07-Q3), "s is a root => |V|-1 edges in both trees" (C07-Q4), 24B-B-Q1a and
26B-A-Q3a; the video does not state any of their answers. The graph here is new.
Every tree, depth and height comes from w_graph_search (graph_ref.py / an own BFS for a custom neighbour order, an own
DFS, networkx); the two general facts used are brute-forced on all connected graphs up to 5 vertices.
"""
import random

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_graph_search as w
from w_graph_search import S

# ---------------------------------------------------------------- the graph (verified)
N = list("ABCDEF")
E = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "F"), ("E", "F")]
POS = {"A": (50, 200), "B": (190, 70), "C": (190, 330), "D": (330, 200), "E": (330, 400), "F": (470, 300)}
LAB = {"A": (0, 56), "B": (0, -54), "C": (-56, 26), "D": (0, -54), "E": (60, 0), "F": (0, 56)}
ADJ = w.adjacency(N, E, False)
REV = {v: sorted(ADJ[v], reverse=True) for v in N}
DELTA = w.nx.single_source_shortest_path_length(w.nxg(N, E, False), "A")


def graph(pfx):
    return w.Graph(pfx, N, E, False, POS, w=520, h=440, lab_at=LAB, scale=0.9)


GB, GD = graph("cb"), graph("cd")
RB, RD = GB.bfs("A"), GD.dfs("A")
assert RB.height == 3 and RD.height == 5 and RD.order == ["A", "B", "D", "C", "E", "F"]
assert all(RD.depth[v] >= DELTA[v] for v in N) and RB.d == DELTA
assert RB.pi["F"] == "D" and RD.pi["F"] == "E" and RB.order.index("D") < RB.order.index("E")
assert RD.pi["C"] == "D" and DELTA["C"] == 1 and RD.depth["C"] == 3
for G, dep in ((GB, RB.d), (GD, RD.depth)):
    for v in N:
        G.lab(v, "dp", str(dep[v]), "gs-lp")

# exam 26A-B-Q2a: two BFS trees from A
Q = BANK["26A-B-Q2a"]
assert "BFS" in Q["question"] and "עומק" in Q["question"] and Q.get("correctId") is None
assert "הוכחה" in Q["solution"]
G1, G2 = graph("x1"), graph("x2")
R1, R2 = G1.bfs("A"), G2.bfs("A", order=REV)
assert R1.pi != R2.pi and (R1.pi["D"], R2.pi["D"]) == ("B", "C") and (R1.pi["F"], R2.pi["F"]) == ("D", "E")
assert R1.d == R2.d == DELTA and R1.height == R2.height == max(DELTA.values()) == 3
for G, R in ((G1, R1), (G2, R2)):
    for v in N:
        G.lab(v, "dp", str(R.d[v]), "gs-lp")


def tree_ids(G, R):
    return [G.eid(v, R.pi[v], "tree") for v in N if R.pi.get(v)]


# the two general facts, brute-forced: every BFS tree has depth(v) = δ(s, v) for every neighbour order; a DFS tree has
# depth(v) >= δ(s, v)
rng = random.Random(7)
cnt = 0
for n in range(2, 6):
    for V, Ed in w.all_graphs(n, False):
        gx = w.nxg(V, Ed, False)
        if not w.nx.is_connected(gx):
            continue
        dl = w.nx.single_source_shortest_path_length(gx, 0)
        adj = w.adjacency(V, Ed, False)
        for _ in range(3):
            o = {v: rng.sample(adj[v], len(adj[v])) for v in V}
            d, pi, _ = w.my_bfs(o, 0)
            assert w.depth(pi) == dl == d
            _, _, pid, _, _ = w.my_dfs(o, [0] + [v for v in V if v], False)
            assert all(w.depth(pid)[v] >= dl[v] for v in V)
        cnt += 1
assert cnt > 700

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    S("אותו גרף, אותו מקור, ושני עצים שונים: עץ BFS ועץ DFS."),
    S("בסרטון הזה נשווה ביניהם, ונראה מה כל אחד מהם מבטיח."),
    S("ובסוף נוכיח טענה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">B07 · גרפים: BFS ו-DFS</div><h1>BFS מול DFS: עצים וטענות</h1>'
         '<p>להשוות עץ BFS לעץ DFS: גבהים, מי גילה כל קודקוד, ומה נשאר זהה כשמשנים את סדר השכנים.</p>',
   layout="title")

idea = Scene("idea", "מה כל עץ מבטיח", [
    S("עץ BFS: העומק של כל קודקוד בעץ הוא בדיוק המרחק שלו מהמקור.", do=show("i-1")),
    S("כי כל צלע עץ מגדילה את השכבה באחת בדיוק, והשכבה של BFS היא המרחק האמיתי."),
    S("ולכן **גובה** עץ ה-BFS הוא המרחק הגדול ביותר מהמקור.", do=show("i-2")),
    S("עץ DFS לא מבטיח מרחקים. הוא הולך לעומק כל עוד יש שכן לבן, ולכן הוא ארוך ומסועף מעט.", do=show("i-3")),
    S("אבל דבר אחד נכון בכל עץ שמושרש במקור: המסלול בעץ הוא מסלול בגרף, ולכן הוא לא קצר מהמרחק.",
      do=show("i-4")),
    S("מכאן: גובה עץ ה-DFS גדול או שווה לגובה עץ ה-BFS.", do=show("i-5"), hold=0.4),
], stage='<div class="gs-stack">'
         + st.card("i-1", "rule", "🔑 עץ BFS: עומק $v$ הוא $\\delta(s,v)$")
         + st.card("i-2", "ex", "גובה עץ BFS הוא $\\max_v \\delta(s,v)$")
         + st.card("i-3", "plain", "עץ DFS: עמוק, בלי הבטחה על מרחקים")
         + "</div>",
   panel=st.card("i-4", "rule", "🔑 כל עץ מ-$s$: עומק $v$ לפחות $\\delta(s,v)$")
         + st.card("i-5", "rule", "🔑 גובה DFS $\\ge$ גובה BFS"))

cmp_ph = [
    S("נראה את זה על גרף. משמאל BFS מהקודקוד $A$, ומימין DFS מ-$A$, שניהם בסדר אלפביתי.", do=show("c-b", "c-d")),
    S("ב-BFS: $B$ ו-$C$ בעומק 1, $D$ ו-$E$ בעומק 2, ו-$F$ בעומק 3.",
      do=RB.all_do(key=None) + show(*[GB.lid(v, "dp") for v in N])),
    S("ב-DFS: מ-$A$ ל-$B$, ל-$D$, ל-$C$, ל-$E$ ול-$F$. שרשרת אחת, בגובה 5.",
      do=show(*[GD.eid(v, RD.pi[v], "tree") for v in N if RD.pi[v]], *[GD.black(v) for v in N],
              *[GD.lid(v, "dp") for v in N])),
    S("שימו לב ל-$C$: הוא שכן של $A$, במרחק 1, ובעץ ה-DFS הוא בעומק 3. העץ לא מבטיח מרחק.",
      do=show(GD.mark("C"), GB.mark("C"))),
    S("וגם האבות שונים. מי גילה את $F$? ב-BFS זה $D$: מבין השכנים של $F$, הוא יצא ראשון מהתור.",
      do=hide(GD.mark("C"), GB.mark("C")) + show(GB.mark("F"), GB.mark("D"))),
    S("ב-DFS זה $E$: כשהריצה הגיעה ל-$E$, הקודקוד $F$ עוד היה לבן, ו-DFS המשיך אליו מיד.",
      do=hide(GB.mark("F"), GB.mark("D")) + show(GD.mark("F"), GD.mark("E"))),
    S("ב-DFS, מי שמגלה קודקוד הוא מי שהגיע אליו ראשון בירידה לעומק, לא מי שקרוב למקור.", do=show("c-pi")),
    S("שלוש מול חמש: גובה ה-DFS גדול יותר, כמו שראינו שחייב להיות.", do=hide(GD.mark("F"), GD.mark("E")) +
      show("c-ok"), hold=0.4),
]
cmp_ = Scene("cmp", "אותו גרף, שני עצים", cmp_ph,
             stage=f'<div class="gs-row"><div class="gs-col"><div id="c-b" class="h">{GB.html(kinds=("tree",))}</div>'
                   '<div class="gs-cap">BFS מ-$A$</div></div>'
                   f'<div class="gs-col"><div id="c-d" class="h">{GD.html(kinds=("tree",))}</div>'
                   '<div class="gs-cap">DFS מ-$A$</div></div></div>',
             panel=st.card("c-pi", "rule", "🔑 $\pi[F]$: ב-BFS $D$, ב-DFS $E$")
                   + st.card("c-ok", "ex", "גובה BFS: 3 · גובה DFS: 5 (בכחול: העומק)"))

ex_ph = [
    S("ועכשיו סעיף ממבחן. כל הקודקודים ישיגים מ-$s$, ויש שני עצי BFS **שונים**, שניהם מושרשים ב-$s$."),
    S("הטענה: אם הגרף לא מכוון, אז בהכרח לשני העצים יש אותו עומק. הוכיחו או הפריכו.", do=show("x-c")),
    S("קודם נבין איך בכלל יש שני עצי BFS שונים: משנים את סדר השכנים.", do=show("x-g1", "x-g2")),
    S("משמאל סדר אלפביתי: $D$ מתגלה דרך $B$, ו-$F$ דרך $D$.",
      do=show(*tree_ids(G1, R1), *[G1.black(v) for v in N], *[G1.lid(v, "dp") for v in N])),
    S("מימין סדר הפוך: $D$ מתגלה דרך $C$, ו-$F$ דרך $E$. עץ אחר.",
      do=show(*tree_ids(G2, R2), *[G2.black(v) for v in N], *[G2.lid(v, "dp") for v in N],
              G1.mark("D"), G2.mark("D"))),
    S("אבל המספרים הכחולים זהים, וגם העומק: 3. אז ננסה להוכיח.", do=hide(G1.mark("D"), G2.mark("D")) +
      show(G1.mark("F"), G2.mark("F"))),
    S("שלב ראשון: בכל עץ BFS, העומק של קודקוד שווה למרחק הקצר ביותר אליו מ-$s$.", do=show("x-1"),
      say_="שלב ראשון: בכל עץ בִּי אֶף אֶס, העומק של קודקוד שווה למרחק הקצר ביותר אליו מאֶס."),
    S("שלב שני: המרחק נקבע על ידי הגרף בלבד. סדר השכנים משנה את האבות, לא את המרחקים.", do=show("x-2")),
    S("שלב שלישי: עומק עץ הוא העומק המקסימלי של קודקוד. כל הקודקודים ישיגים, ולכן כולם בשני העצים.",
      do=show("x-3")),
    S("לכן שני העומקים שווים למרחק המקסימלי מ-$s$. הטענה נכונה.", do=show("x-ok"),
      say_="לכן שני העומקים שווים למרחק המקסימלי מאֶס. הטענה נכונה."),
    S("המלכודות: לכתוב שעץ BFS יחיד, הוא לא. ולבלבל עם DFS, שבו העומק כן תלוי בסדר.", do=show("x-t"), hold=0.5),
]
exam = Scene("exam", "שאלה ממבחן", ex_ph,
             stage=f'<div class="gs-row"><div class="gs-col"><div id="x-g1" class="h">{G1.html(kinds=("tree",))}</div>'
                   '<div class="gs-cap">סדר אלפביתי</div></div>'
                   f'<div class="gs-col"><div id="x-g2" class="h">{G2.html(kinds=("tree",))}</div>'
                   '<div class="gs-cap">סדר הפוך</div></div></div>',
             panel=f'<div class="gs-q"><span class="qid">{Q["id"]}</span>$G$ לא מכוון, הכל ישיג מ-$s$. '
                   '$T_{BFS}\\ne T\'_{BFS}$ מושרשים ב-$s$. האם בהכרח יש להם אותו עומק?</div>'
                   + st.card("x-c", "plain", "צריך: $\\mathrm{depth}(T_{BFS})=\\mathrm{depth}(T'_{BFS})$")
                   + '<div class="gs-steps">'
                   + '<div id="x-1" class="h"><span class="n">1.</span>עומק $v$ בעץ BFS הוא $\\delta(s,v)$</div>'
                   + '<div id="x-2" class="h"><span class="n">2.</span>$\\delta(s,v)$ תלוי רק ב-$G$</div>'
                   + '<div id="x-3" class="h"><span class="n">3.</span>בשני העצים העומק הוא $\\max_v\\delta(s,v)$</div>'
                   + "</div>"
                   + st.card("x-ok", "rule", "🔑 <b>נכונה</b>: שני העומקים הם $\\max_v\\delta(s,v)$")
                   + st.card("x-t", "trap", "⚠️ העצים שונים, העומקים לא"))

recap = Scene("recap", "סיכום", [
    S("לסיכום: בעץ BFS העומק של כל קודקוד הוא המרחק שלו, ולכן הגובה הוא המרחק הגדול ביותר.", do=show("s-1")),
    S("בכל עץ שמושרש במקור העומק לא קטן מהמרחק, ולכן גובה ה-DFS לפחות כמו של ה-BFS.", do=show("s-2")),
    S("וסדר שכנים אחר משנה את עץ ה-BFS, אבל לא את העומקים. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage='<div class="gs-stack">'
         + st.card("s-1", "rule", "🔑 עץ BFS: עומק $v$ הוא $\\delta(s,v)$")
         + st.card("s-2", "rule", "🔑 גובה DFS $\\ge$ גובה BFS")
         + "</div>",
   panel=st.card("s-3", "ex", "סדר אחר: אבות אחרים, אותם עומקים"))

VIDEO = Video("B07", "graph_search", "BFS מול DFS: עצים וטענות", [title, idea, cmp_, exam, recap],
              bank={"26A-B-Q2a": None})
