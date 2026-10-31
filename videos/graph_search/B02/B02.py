# -*- coding: utf-8 -*-
"""B02 · BFS בפעולה: מרחק, קשירות וטיולים — video script (build: tools/video/vid.py B02).

Source: courses/graph_search/C02.js (lesson + goal: use BFS to answer questions: reachability, components, walks).
Exam anchor: 24A-B-Q1b (open question: the length of the shortest walk from x to y that passes through a set A),
which no guided quiz uses. Solved on an own example graph, with its algorithm, its correctness and its running time.
Not used on purpose: the C02 quiz (components of A..I, the P..V shortest-path graph, the cut-vertex graph, 25A-B-Q5c,
25A-B-Q5a, 24A-A-Q1a) and the boss items 24A-A-Q1b (the test "shortest PATH through z") and 24A-C-Q1a (cut vertex):
the video never states the "path through z" test or the cut-vertex algorithm. 24A-B-Q1a (does such a walk exist) is
the B08 boss walkthrough. Both graphs here are new.
Every distance, component and the walk length are computed by w_graph_search (graph_ref.py, an own BFS, networkx);
the walk length is also brute-forced by a BFS over (vertex, "already passed through A") states.
"""
from collections import deque

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_graph_search as w
from w_graph_search import S, INF

# ---------------------------------------------------------------- components (verified)
NC = list("ABCDEFGH")
EC = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("E", "F"), ("F", "G")]
PC = {"A": (70, 90), "B": (220, 40), "C": (180, 230), "D": (330, 170), "E": (440, 60), "F": (560, 170),
      "G": (450, 300), "H": (180, 390)}
GC = w.Graph("c", NC, EC, False, PC, scale=1.0)
RUNS = []
white = list(NC)
while white:
    r = GC.bfs(white[0])
    RUNS.append(r)
    white = [v for v in white if v not in r.d]
assert [sorted(r.d) for r in RUNS] == [["A", "B", "C", "D"], ["E", "F", "G"], ["H"]]
assert len(RUNS) == w.nx.number_connected_components(w.nxg(NC, EC, False)) == 3
for k, r in enumerate(RUNS):
    for v in r.d:
        GC.lab(v, "k", f"#{k + 1}", "gs-lp")
assert len(RUNS[0].d) < len(NC)                     # BFS from A alone misses E, F, G, H: not connected


def comp_do(k):
    r = RUNS[k]
    return r.all_do(key="k")


# ---------------------------------------------------------------- exam 24A-B-Q1b
Q = BANK["24A-B-Q1b"]
assert "הטיול הקצר ביותר" in Q["question"] and Q.get("correctId") is None
assert "dx[v] + dy[v]" in Q["solution"]
NX = ["x", "y", "B", "C", "D", "E", "F", "G", "H", "K", "M"]
EX = [("x", "B"), ("B", "C"), ("C", "y"), ("C", "D"), ("x", "E"), ("E", "F"), ("F", "G"), ("G", "H"), ("H", "K"),
      ("K", "y")]
SETA = ["D", "G", "M"]
PX = {"x": (50, 190), "B": (190, 120), "C": (350, 120), "y": (580, 190), "D": (480, 50), "E": (90, 330),
      "F": (210, 400), "G": (340, 420), "H": (460, 390), "K": (560, 320), "M": (150, 40)}
GX = w.Graph("x", NX, EX, False, PX, scale=0.84)
RX, RY = GX.bfs("x"), GX.bfs("y")
dx = {v: RX.d.get(v, INF) for v in NX}
dy = {v: RY.d.get(v, INF) for v in NX}
SUM = {v: dx[v] + dy[v] for v in SETA}
assert dx["y"] == 3 and (dx["D"], dy["D"]) == (3, 2) and (dx["G"], dy["G"]) == (3, 3) and dx["M"] == dy["M"] == INF
BEST = min(SUM.values())
assert BEST == 5 and [v for v in SETA if SUM[v] == BEST] == ["D"] and SUM["G"] == 6 and SUM["M"] == INF


def walk_bf(adj, x, y, A):
    """shortest walk x -> y that visits A: BFS over states (vertex, passed A yet)"""
    start = (x, x in A)
    dist, q = {start: 0}, deque([start])
    while q:
        u, f = q.popleft()
        if u == y and f:
            return dist[(u, f)]
        for v in adj[u]:
            s = (v, f or v in A)
            if s not in dist:
                dist[s] = dist[(u, f)] + 1
                q.append(s)
    return INF


assert walk_bf(RX.adj, "x", "y", set(SETA)) == BEST
WALK = ["x", "B", "C", "D", "C", "y"]
assert len(WALK) - 1 == BEST and all(b in RX.adj[a] for a, b in zip(WALK, WALK[1:])) and WALK.count("C") == 2
assert walk_bf(RX.adj, "x", "y", {"M"}) == INF                                   # only M: no walk at all
for v in NX:
    GX.lab(v, "dx", "∞" if dx[v] == INF else str(dx[v]), "", dx=-26, dy=-48)
    GX.lab(v, "dy", "∞" if dy[v] == INF else str(dy[v]), "gs-lp", dx=26, dy=-48)
fmt = lambda a: "∞" if a == INF else str(a)
TAB = w.table("t", ["$v\\in A$", "$d_x[v]$", "$d_y[v]$", "סכום"],
              [[f"${v}$", fmt(dx[v]), fmt(dy[v]), fmt(SUM[v])] for v in SETA])
CODE = ('<div id="x-code" class="gs-code gs-sm h"><span class="k">minWalk</span>(G, x, y, A):\n'
        '  dx ← BFS(G, x)\n  <span class="k">if</span> dx[y] = ∞: <span class="k">return</span> ∞\n'
        '  dy ← BFS(G, y)\n  best ← ∞\n  <span class="k">for</span> v <span class="k">in</span> A:\n'
        '    best ← min(best, dx[v] + dy[v])\n  <span class="k">return</span> best</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    S("בסרטון הקודם הרצנו BFS. בסרטון הזה נשתמש בו כדי לענות על שאלות."),
    S("מי ישיג ממי, כמה רכיבי קשירות יש, ומה אורך הטיול הקצר ביותר."),
    S("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">B02 · גרפים: BFS ו-DFS</div><h1>BFS בפעולה: מרחק, קשירות וטיולים</h1>'
         '<p>להשתמש ב-BFS כדי לענות על שאלות: מי ישיג, כמה רכיבי קשירות, ואורך של טיול קצר.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    S("המשפט שעליו הכל בנוי: בגרף לא ממושקל, BFS מהמקור נותן לכל קודקוד את המרחק האמיתי אליו.", do=show("i-1")),
    S("כלומר מספר הצלעות במסלול הקצר ביותר מהמקור.", say_="כלומר, מספר הצלעות במסלול הקצר ביותר מהמקור."),
    S("קודקוד ש-BFS לא גילה אינו ישיג מהמקור, והמרחק אליו הוא אינסוף.", do=show("i-2")),
    S("ומכאן כמה שימושים, כולם בזמן לינארי בגודל הגרף: רכיבי קשירות, ישיגות, ומרחקים דרך קודקוד.",
      do=show("i-3")),
    S("ועוד הבחנה אחת שהמבחן אוהב: טיול מול מסלול.", do=show("i-4")),
    S("**מסלול** לא חוזר על קודקודים. **טיול** רשאי לחזור על קודקודים ועל צלעות.", do=show("i-5"), hold=0.4),
], stage='<div class="gs-stack">'
         + st.card("i-1", "rule", "🔑 בגרף לא ממושקל: $d[v]=\\delta(s,v)$")
         + st.card("i-2", "ex", "לא התגלה ← לא ישיג ← $\\delta(s,v)=\\infty$")
         + st.card("i-3", "plain", "כל שימוש: $O(|V|+|E|)$ לכל הרצה")
         + "</div>",
   panel=st.card("i-4", "plain", "<b>טיול מול מסלול</b>")
         + st.card("i-5", "trap", "⚠️ מסלול: בלי חזרות. טיול: מותר לחזור על קודקודים וצלעות"))

comp = Scene("comp", "רכיבי קשירות", [
    S("דוגמה ראשונה: כמה רכיבי קשירות יש בגרף הזה?", do=show("c-g")),
    S("רכיב קשירות הוא תת-גרף קשיר **מקסימלי**: אי אפשר להוסיף לו קודקוד ולהישאר קשיר.", do=show("c-def")),
    S("מריצים BFS מ-$A$. הוא מגלה את $A$, $B$, $C$ ו-$D$, ושם התור מתרוקן. זה הרכיב הראשון.", do=comp_do(0)),
    S("שימו לב: התור התרוקן, אבל לא כל הקודקודים התגלו. לכן הגרף **לא** קשיר.", do=show("c-t")),
    S("ממשיכים מהקודקוד הלבן הבא, $E$: הוא מגלה את $F$ ואת $G$. רכיב שני.", do=comp_do(1)),
    S("ואז $H$, שאין לו שכנים בכלל. גם קודקוד מבודד הוא רכיב בפני עצמו: רכיב שלישי.", do=comp_do(2)),
    S("אז יש שלושה רכיבים: מספר הפעמים שהתחלנו BFS מקודקוד לבן.", do=show("c-ans")),
    S("וכל קודקוד וכל צלע נסרקים פעם אחת בסך הכל, ולכן הזמן לינארי.", hold=0.4),
], stage=f'<div id="c-g" class="h">{GC.html()}</div>',
   panel=st.card("c-def", "ex", "רכיב קשירות = תת-גרף קשיר <b>מקסימלי</b>")
         + st.card("c-t", "trap", "⚠️ התור מתרוקן תמיד. קשיר ⇔ <b>כולם</b> התגלו")
         + st.card("c-ans", "rule", "🔑 מספר הרכיבים = מספר ההתחלות מקודקוד לבן: 3"))

ex_ph = [
    S("ועכשיו סעיף ממבחן. גרף לא מכוון, שני קודקודים $x$ ו-$y$, וקבוצת קודקודים $A$ שלא מכילה אותם."),
    S("צריך להחזיר את אורך הטיול הקצר ביותר מ-$x$ ל-$y$ שעובר דרך $A$, ואינסוף אם אין כזה.", do=show("x-g")),
    S("כאן $A$ היא $D$, $G$ ו-$M$, המסומנים.", do=show(GX.mark("D"), GX.mark("G"), GX.mark("M")),
      say_="כאן, הקבוצה אֵיי היא דִּי, גִ'י ואֶם, המסומנים."),
    S("הרעיון: טיול דרך קודקוד $v$ מ-$A$ הוא שני חלקים. מ-$x$ אל $v$, ואחר כך מ-$v$ אל $y$.", do=show("x-i1"),
      say_="הרעיון: טיול דרך קודקוד וִי מהקבוצה אֵיי הוא שני חלקים. מאִקְס אל וִי, ואחר כך מוִי אל וַואי."),
    S("כל חלק לבד הכי קצר כשהוא מסלול קצר ביותר. ובטיול מותר לחזור, אז אין התנגשות בין החלקים."),
    S("לכן האורך דרך $v$ הוא המרחק מ-$x$ ל-$v$ ועוד המרחק מ-$v$ ל-$y$, ובוחרים את ה-$v$ הכי טוב.",
      say_="לכן האורך דרך וִי הוא המרחק מאִקְס לוִי, ועוד המרחק מוִי לוַואי, ובוחרים את הוִי הכי טוב."),
    S("את כל המרחקים מ-$x$ נותן BFS אחד מ-$x$: המספרים הכתומים.", do=RX.all_do(key="dx")),
    S("והמרחק מ-$v$ ל-$y$? הגרף לא מכוון, אז הוא שווה למרחק מ-$y$ ל-$v$: BFS אחד מ-$y$, המספרים הכחולים.",
      do=RY.all_do(key="dy")),
    S("עכשיו טבלה קטנה. דרך $D$: 3 ועוד 2, חמש.", do=show("x-tab", "t-r0")),
    S("דרך $G$: 3 ועוד 3, שש. ו-$M$ לא ישיג בכלל: אינסוף, והוא לא משנה את המינימום.", do=show("t-r1", "t-r2")),
    S("התשובה: 5. הטיול הוא $x$, $B$, $C$, $D$, ושוב $C$ ו-$y$.",
      do=show("t-c0-3") + show(*[GX.eid(a, b, "hl") for a, b in zip(WALK, WALK[1:])]),
      say_="התשובה: חמש. הטיול הוא אִקְס, בִּי, סִי, דִּי, ושוב סִי ווַואי."),
    S("שימו לב: הוא עובר פעמיים ב-$C$. מותר, זה טיול.", do=show("x-t1"),
      say_="שימו לב: הוא עובר פעמיים בסִי. מותר, זה טיול."),
    S("והאלגוריתם: שתי הרצות BFS, ולולאה על $A$. הזמן לינארי בגודל הגרף.", do=show("x-code"),
      say_="והאלגוריתם: שתי הרצות בִּי אֶף אֶס, ולולאה על הקבוצה אֵיי. הזמן לינארי בגודל הגרף."),
    S("והמלכודות: לקחת רק את המרחק מ-$x$, או את המקסימום של שני המרחקים במקום הסכום.", do=show("x-t2"),
      say_="והמלכודות: לקחת רק את המרחק מאִקְס, או את המקסימום של שני המרחקים במקום הסכום.", hold=0.5),
]
exam = Scene("exam", "שאלה ממבחן", ex_ph,
             stage=f'<div class="gs-stack"><div id="x-g" class="h">{GX.html()}</div>'
                   f'<div class="gs-row"><div id="x-tab" class="h">{TAB}</div>{CODE}</div></div>',
             panel=f'<div class="gs-q"><span class="qid">{Q["id"]}</span>גרף לא מכוון, $x,y\\notin A$. החזירו את '
                   'אורך הטיול הקצר ביותר מ-$x$ ל-$y$ שעובר דרך $A$ (אינסוף אם אין).</div>'
                   + st.card("x-i1", "rule", "🔑 $\\min_{v\\in A}\\,(d_x[v]+d_y[v])$")
                   + st.card("x-t1", "ex", "הטיול חוזר על $C$: מותר")
                   + st.card("x-t2", "trap", "⚠️ לא $d_x[v]$ לבד, ולא $\\max$: סכום"))

recap = Scene("recap", "סיכום", [
    S("לסיכום: BFS בגרף לא ממושקל נותן מרחקים אמיתיים, ומי שלא התגלה לא ישיג.", do=show("s-1")),
    S("קשירות: BFS אחד, ובודקים שכולם התגלו. רכיבים: סופרים כמה פעמים התחלנו מקודקוד לבן.", do=show("s-2")),
    S("וטיול דרך קבוצה: שני BFS, אחד מכל קצה, וסכום של שני מרחקים. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage='<div class="gs-stack">'
         + st.card("s-1", "rule", "🔑 $d[v]=\\delta(s,v)$, ולא התגלה ← $\\infty$")
         + st.card("s-2", "rule", "🔑 רכיבים = מספר ההתחלות מקודקוד לבן")
         + "</div>",
   panel=st.card("s-3", "rule", "🔑 טיול דרך $A$: $\\min_{v\\in A}(d_x[v]+d_y[v])$"))

VIDEO = Video("B02", "graph_search", "BFS בפעולה: מרחק, קשירות וטיולים", [title, idea, comp, exam, recap],
              bank={"24A-B-Q1b": None})
