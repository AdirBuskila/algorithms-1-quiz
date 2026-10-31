# -*- coding: utf-8 -*-
"""B08 · מבחן גמר: גרפים — boss walkthrough (build: tools/video/vid.py B08).

Source: courses/graph_search/C08.js (boss: real exam questions on BFS, DFS and graph claims, proofs and refutations).
Exam anchors (two parts, none used by any guided quiz or boss): 24A-B-Q1a (does a walk from x to y through a set A
exist: algorithm, correctness, time) and 24B-B-Q1b (directed graph: E_DFS = E_BFS and every in/out degree nonzero =>
s is a root: proof by contradiction).
Not used on purpose: every C08 boss item (24A-A-Q1b, 24A-C-Q1a, 24B-A-Q1c, 24B-B-Q1c, 26B-A-Q3b, 25B-A-Q1b) and every
level quiz item. 24B-B-Q1b is a sibling of 24B-B-Q1a (C07 quiz) and 24B-B-Q1c (boss): the video proves only Q1b's
claim and does not discuss what happens under Q1c's weaker condition or Q1a's missing one. 24A-B-Q1a's sibling Q1b is
the B02 exam. The graphs here are new.
Every run is computed by w_graph_search; both exam claims are brute-forced on small graphs below.
"""
import itertools
from collections import deque

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_graph_search as w
from w_graph_search import S, INF

# ---------------------------------------------------------------- part 1: 24A-B-Q1a (verified)
Q1 = BANK["24A-B-Q1a"]
assert "טיול" in Q1["question"] and Q1.get("correctId") is None and "dx[v] != INF" in Q1["solution"]


def walk_through(adj, x, y, A):
    """brute force: BFS over (vertex, passed A yet)"""
    st0 = (x, x in A)
    seen, q = {st0}, deque([st0])
    while q:
        u, f = q.popleft()
        if u == y and f:
            return True
        for v in adj[u]:
            s = (v, f or v in A)
            if s not in seen:
                seen.add(s)
                q.append(s)
    return False


def alg(adj, x, y, A):
    d, _, _ = w.my_bfs(adj, x)
    return y in d and any(v in d for v in A)


for n in range(2, 6):                                   # the algorithm == the brute force, all graphs, all x, y, A
    for V, Ed in w.all_graphs(n, False):
        adj = w.adjacency(V, Ed, False)
        for x, y in itertools.permutations(V, 2):
            rest = [v for v in V if v not in (x, y)]
            for k in range(1, len(rest) + 1):
                for A in itertools.combinations(rest, k):
                    assert alg(adj, x, y, set(A)) == walk_through(adj, x, y, set(A))

N1 = ["x", "B", "y", "C", "K", "M"]
E1 = [("x", "B"), ("B", "y"), ("y", "C"), ("K", "M")]
P1 = {"x": (60, 120), "B": (220, 60), "y": (380, 120), "C": (520, 60), "K": (220, 320), "M": (440, 320)}
G1 = w.Graph("p", N1, E1, False, P1, w=600, h=400, scale=1.0)
R1 = G1.bfs("x")
assert set(R1.d) == {"x", "B", "y", "C"}
ADJ1 = w.adjacency(N1, E1, False)
assert not alg(ADJ1, "x", "y", {"M"}) and not walk_through(ADJ1, "x", "y", {"M"})
assert alg(ADJ1, "x", "y", {"M", "C"}) and walk_through(ADJ1, "x", "y", {"M", "C"})
WALK = ["x", "B", "y", "C", "y"]
assert all(b in ADJ1[a] for a, b in zip(WALK, WALK[1:])) and WALK.count("y") == 2
for v in N1:
    G1.lab(v, "dx", "∞" if v not in R1.d else str(R1.d[v]), "")
CODE = ('<div id="a-code" class="gs-code gs-sm h"><span class="k">walkThrough</span>(G, x, y, A):\n'
        '  dx ← BFS(G, x)\n  <span class="k">if</span> dx[y] = ∞: <span class="k">return</span> false\n'
        '  <span class="k">for</span> v <span class="k">in</span> A:\n'
        '    <span class="k">if</span> dx[v] ≠ ∞: <span class="k">return</span> true\n'
        '  <span class="k">return</span> false</div>')

AFT = (st.card("a-f", "ex gs-sm", "$A=\\{M\\}$: שקר") + st.card("a-t", "ex gs-sm", "$A=\\{M,C\\}$: אמת"))

# ---------------------------------------------------------------- part 2: 24B-B-Q1b (verified)
Q2 = BANK["24B-B-Q1b"]
assert "deg^-" in Q2["question"] and "deg^+" in Q2["question"] and "**נכון**" in Q2["solution"]


def tree_edges_bfs(adj, s):
    _, pi, _ = w.my_bfs(adj, s)
    return {(p, v) for v, p in pi.items() if p is not None}


def tree_edges_dfs(adj, s, V):
    _, _, pi, _, _ = w.my_dfs(adj, [s] + [v for v in V if v != s], True)
    return {(p, v) for v, p in pi.items() if p is not None}


cases = 0
for n in range(2, 5):                                    # all directed graphs without self-loops, up to 4 vertices
    for V, Ed in w.all_graphs(n, True):
        if not Ed:
            continue
        adj = w.adjacency(V, Ed, True)
        indeg = {v: 0 for v in V}
        for a, b in Ed:
            indeg[b] += 1
        if any(indeg[v] == 0 or not adj[v] for v in V):
            continue
        for s in V:
            if tree_edges_dfs(adj, s, V) == tree_edges_bfs(adj, s):
                assert all(w.nx.has_path(w.nxg(V, Ed, True), s, v) for v in V)
                cases += 1
assert cases > 50

N2 = ["s", "a", "b", "c"]
E2 = [("s", "a"), ("a", "s"), ("b", "c"), ("c", "b"), ("c", "a")]
P2 = {"s": (70, 80), "a": (70, 300), "b": (380, 80), "c": (380, 300)}
G2 = w.Graph("q", N2, E2, True, P2, w=460, h=380, scale=1.0)
RB2, RD2 = G2.bfs("s"), G2.dfs("s")
EB = {(p, v) for v, p in RB2.pi.items() if p is not None}
ED = {(p, v) for v, p in RD2.pi.items() if p is not None}
assert EB == {("s", "a")} and ED == {("s", "a"), ("b", "c")} and EB != ED
assert set(RB2.d) == {"s", "a"}                                          # R = {s, a}, U = {b, c}
assert not any(u in RB2.d and v not in RB2.d for u, v in E2)             # no edge R -> U
indeg2 = {v: sum(1 for a, b in E2 if b == v) for v in N2}
assert all(indeg2[v] and RB2.adj[v] for v in N2)                         # every in/out degree nonzero
assert RD2.disc["b"] > max(RD2.fin[v] for v in ("s", "a"))              # U is discovered after all of R
R_IDS = [G2.mark(v) for v in ("s", "a")]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    S("זה סרטון הגמר של הקורס: שני סעיפים אמיתיים ממבחנים."),
    S("סעיף אחד הוא אלגוריתם עם BFS, והשני הוא הוכחה על BFS ו-DFS בגרף מכוון."),
    S("עצרו את הסרטון לפני כל פתרון, ונסו לבד על דף.", hold=0.4),
], stage='<div class="kicker">B08 · גרפים: BFS ו-DFS</div><h1>מבחן גמר: גרפים</h1>'
         '<p>שני סעיפים אמיתיים: אלגוריתם עם BFS, והוכחה בשלילה על עצי BFS ו-DFS.</p>', layout="title")

p1 = Scene("walk", "סעיף 1: טיול דרך קבוצה", [
    S("סעיף ראשון. גרף לא מכוון, שני קודקודים $x$ ו-$y$, וקבוצת קודקודים $A$ שלא מכילה אותם.", do=show("a-g")),
    S("כתבו אלגוריתם שמחזיר אמת אם יש **טיול** מ-$x$ ל-$y$ שעובר דרך $A$.",
      say_="כתבו אלגוריתם שמחזיר אמת, אם יש טיול מאִקְס לוַואי שעובר דרך הקבוצה אֵיי."),
    S("המילה החשובה היא טיול: מותר לחזור על קודקודים. אז לא צריך מסלול פשוט, רק ישיגות.", do=show("a-1")),
    S("נניח ש-$v$ מ-$A$ ישיג מ-$x$, וגם $y$ ישיג מ-$x$. הולכים מ-$x$ ל-$v$, חוזרים ל-$x$, וממשיכים ל-$y$.",
      say_="נניח שוִי מהקבוצה אֵיי ישיג מאִקְס, וגם וַואי ישיג מאִקְס. הולכים מאִקְס לוִי, חוזרים לאִקְס, וממשיכים לוַואי."),
    S("וזה טיול חוקי, כי הגרף לא מכוון. ובכיוון השני: טיול דרך $v$ אומר ש-$v$ ו-$y$ ישיגים מ-$x$.",
      say_="וזה טיול חוקי, כי הגרף לא מכוון. ובכיוון השני: טיול דרך וִי אומר שוִי ווַואי ישיגים מאִקְס."),
    S("לכן: BFS אחד מ-$x$. אם $y$ לא התגלה, שקר. אחרת, אמת אם **לפחות קודקוד אחד** מ-$A$ התגלה.",
      do=show("a-code"),
      say_="לכן: בִּי אֶף אֶס אחד מאִקְס. אם וַואי לא התגלה, שקר. אחרת, אמת אם לפחות קודקוד אחד מהקבוצה אֵיי התגלה."),
    S("נבדוק על הגרף. BFS מ-$x$ מגלה את $B$, $y$ ו-$C$. אל $K$ ואל $M$ הוא לא מגיע.",
      do=R1.all_do(key="dx")),
    S("אם $A$ היא רק $M$: הוא לא התגלה, אז אין טיול כזה. התשובה שקר.", do=show(G1.mark("M"), "a-f"),
      say_="אם הקבוצה אֵיי היא רק אֶם: הוא לא התגלה, אז אין טיול כזה. התשובה שקר."),
    S("ואם $A$ היא $M$ ו-$C$: הקודקוד $C$ התגלה, אז אמת. הטיול: $x$, $B$, $y$, $C$ ושוב $y$.",
      do=show(G1.mark("C"), "a-t") + show(*[G1.eid(a, b, "hl") for a, b in zip(WALK, WALK[1:])]),
      say_="ואם הקבוצה אֵיי היא אֶם וסִי: הקודקוד סִי התגלה, אז אמת. הטיול: אִקְס, בִּי, וַואי, סִי, ושוב וַואי."),
    S("הזמן: BFS אחד ולולאה על $A$, כלומר לינארי בגודל הגרף.", do=show("a-3"),
      say_="הזמן: בִּי אֶף אֶס אחד, ולולאה על הקבוצה אֵיי. כלומר, לינארי בגודל הגרף."),
    S("והמלכודות: לבדוק רק את $y$ ולשכוח את $A$, או לדרוש שכל $A$ תהיה ישיגה. מספיק קודקוד אחד.",
      do=show("a-4"), hold=0.5,
      say_="והמלכודות: לבדוק רק את וַואי ולשכוח את הקבוצה אֵיי, או לדרוש שכל הקבוצה תהיה ישיגה. מספיק קודקוד אחד."),
], stage=f'<div class="gs-stack"><div id="a-g" class="h">{G1.html(kinds=("tree", "hl"))}</div>'
         f'<div class="gs-row">{CODE}<div class="gs-col">{AFT}</div></div></div>',
   panel=f'<div class="gs-q"><span class="qid">{Q1["id"]}</span>גרף לא מכוון, $x,y\\notin A$. האם קיים <b>טיול</b> '
         'מ-$x$ ל-$y$ שעובר דרך $A$?</div>'
         + st.card("a-1", "ex", "טיול: מותר לחזור. צריך רק ישיגות")
         + st.card("a-3", "rule", "🔑 $O(|V|+|E|)$")
         + st.card("a-4", "trap", "⚠️ לא רק $y$, ולא כל $A$: קודקוד אחד"))

p2 = Scene("claim", "סעיף 2: הטענה", [
    S("סעיף שני. $G$ גרף מכוון ו-$s$ קודקוד. מריצים BFS מ-$s$, ו-DFS שמתחיל ב-$s$ וממשיך על כל הגרף.",
      do=show("b-0")),
    S("$E_{BFS}$ הן צלעות עץ ה-BFS, ו-$E_{DFS}$ הן צלעות יער ה-DFS.",
      say_="קבוצת צלעות הבִּי אֶף אֶס היא צלעות העץ שלו, וקבוצת צלעות הדִּי אֶף אֶס היא צלעות היער שלו."),
    S("הטענה: אם שתי הקבוצות שוות, ולכל קודקוד יש גם צלע נכנסת וגם צלע יוצאת, אז $s$ שורש.", do=show("b-c")),
    S("שורש פירושו: כל הקודקודים ישיגים ממנו. הטענה נכונה, בהנחה הרגילה שאין לולאות עצמיות.", do=show("b-ok")),
    S("קודם נבין למה, על גרף ש**לא** מקיים את המסקנה. כאן $s$ מגיע רק ל-$a$.", do=show("b-g", *R_IDS)),
    S("BFS מ-$s$ מוצא רק את $a$: צלע אחת.", do=RB2.all_do(key=None) + show(G2.eid("s", "a", "tree"))),
    S("אבל DFS ממשיך: $b$ עדיין לבן, הוא מתחיל עץ חדש, ומגלה את $c$. נוספה צלע עץ בתוך החלק הלא ישיג.",
      do=show(G2.eid("b", "c", "hl"), G2.black("b"), G2.black("c"))),
    S("אז כאן הקבוצות שונות. ההוכחה מראה שזה קורה **תמיד** כש-$s$ לא שורש והדרגות לא אפס.", hold=0.4),
], stage=f'<div id="b-g" class="h">{G2.html(kinds=("tree", "hl"))}</div>',
   panel=f'<div class="gs-q"><span class="qid">{Q2["id"]}</span>$G$ מכוון. $E_{{BFS}}$: עץ BFS מ-$s$. '
         '$E_{DFS}$: יער DFS שמתחיל ב-$s$.</div>'
         + st.card("b-0", "plain", "נכון או לא נכון, עם נימוק")
         + st.card("b-c", "ex", "$E_{DFS}=E_{BFS}$ וגם $\\deg^-(x)\\ne0$, $\\deg^+(x)\\ne0$ לכל $x$ ← $s$ שורש")
         + st.card("b-ok", "rule", "🔑 <b>נכון</b> (בלי לולאות עצמיות)"))

STEPS = [
    ("1", "$R$: הישיגים מ-$s$. $U=V\\setminus R$. נניח בשלילה $U\\ne\\emptyset$"),
    ("2", "אין צלע מ-$R$ אל $U$, וצלעות $E_{BFS}$ כולן בתוך $R$"),
    ("3", "לכל $x\\in U$ צלע נכנסת, והיא מ-$U$. הולכים אחורה: מעגל $C$ בתוך $U$"),
    ("4", "DFS מתחיל ב-$s$: העץ הראשון הוא $R$, לפני כל קודקוד של $U$"),
    ("5", "$v$ הראשון שמתגלה ב-$C$, $w$ אחריו: $w$ צאצא של $v$, וצלע העץ אליו בתוך $U$"),
    ("6", "צלע של $E_{DFS}$ בתוך $U$ אינה ב-$E_{BFS}$: סתירה"),
]
p3 = Scene("proof", "סעיף 2: ההוכחה", [
    S("עכשיו ההוכחה, בשלילה. נסמן ב-$R$ את הקודקודים הישיגים מ-$s$, וב-$U$ את כל השאר, ונניח ש-$U$ לא ריקה.",
      do=show("st-1"),
      say_="עכשיו ההוכחה, בשלילה. נסמן באָר את הקודקודים הישיגים מאֶס, וביוּ את כל השאר, ונניח שיוּ לא ריקה."),
    S("אין צלע מ-$R$ אל $U$: הקצה שלה היה ישיג. ו-BFS מגלה רק ישיגים, אז כל צלעות ה-BFS בתוך $R$.",
      do=show("st-2"),
      say_="אין צלע מאָר אל יוּ: הקצה שלה היה ישיג. ובִּי אֶף אֶס מגלה רק ישיגים, אז כל צלעות הבִּי אֶף אֶס בתוך אָר."),
    S("לכל קודקוד ב-$U$ יש צלע נכנסת, והיא חייבת לבוא מ-$U$. הולכים אחורה בצלעות נכנסות, והגרף סופי.",
      do=show("st-3"),
      say_="לכל קודקוד ביוּ יש צלע נכנסת, והיא חייבת לבוא מיוּ. הולכים אחורה בצלעות נכנסות, והגרף סופי."),
    S("אז חוזרים על קודקוד: יש מעגל מכוון בתוך $U$. בלי לולאות, אורכו לפחות שתיים.",
      say_="אז חוזרים על קודקוד: יש מעגל מכוון בתוך יוּ. בלי לולאות, אורכו לפחות שתיים."),
    S("DFS מתחיל ב-$s$. לפי משפט השביל הלבן, העץ של $s$ הוא בדיוק $R$. לכן כל $R$ מתגלה לפני $U$.",
      do=show("st-4"),
      say_="דִּי אֶף אֶס מתחיל באֶס. לפי משפט השביל הלבן, העץ של אֶס הוא בדיוק אָר. לכן כל אָר מתגלה לפני יוּ."),
    S("יהי $v$ הקודקוד הראשון במעגל שמתגלה, ו-$w$ הבא אחריו. ברגע הגילוי של $v$, הצלע אל $w$ היא שביל לבן.",
      do=show("st-5"),
      say_="יהי וִי הקודקוד הראשון במעגל שמתגלה, ודַאבֶּל יוּ הבא אחריו. ברגע הגילוי של וִי, הצלע אל דַאבֶּל יוּ היא שביל לבן."),
    S("לכן $w$ צאצא של $v$, והאב שלו בעץ התגלה אחרי $v$. כל $R$ התגלה לפני $v$, אז גם האב ב-$U$.",
      say_="לכן דַאבֶּל יוּ צאצא של וִי, והאב שלו בעץ התגלה אחרי וִי. כל אָר התגלה לפני וִי, אז גם האב ביוּ."),
    S("קיבלנו צלע עץ של DFS ששני קצותיה ב-$U$. היא לא צלע של BFS, וזו סתירה לשוויון. לכן $s$ שורש.",
      do=show("st-6", "pf-ok"),
      say_="קיבלנו צלע עץ של דִּי אֶף אֶס ששני קצותיה ביוּ. היא לא צלע של בִּי אֶף אֶס, וזו סתירה לשוויון. לכן אֶס שורש."),
    S("המלכודת: לחשוב שצלע נכנסת לכל קודקוד מבטיחה מסלול מ-$s$. היא יכולה להגיע מקודקוד אחר שלא ישיג.",
      do=show("pf-t"), hold=0.5,
      say_="המלכודת: לחשוב שצלע נכנסת לכל קודקוד מבטיחה מסלול מאֶס. היא יכולה להגיע מקודקוד אחר שלא ישיג."),
], stage='<div class="gs-steps">'
         + "".join(f'<div id="st-{n}" class="h"><span class="n">{n}.</span>{t}</div>' for n, t in STEPS)
         + "</div>",
   panel=st.card("pf-ok", "rule", "🔑 $U=\\emptyset$, ולכן $s$ שורש")
         + st.card("pf-t", "trap", "⚠️ צלע נכנסת ≠ ישיג מ-$s$: היא יכולה לבוא מתוך $U$"))

recap = Scene("recap", "סיכום הקורס", [
    S("לסיכום הקורס: BFS נותן מרחקים ושכבות, ובודקים איתו ישיגות, קשירות וטיולים.", do=show("s-1")),
    S("DFS נותן זמני גילוי וסיום, סוגי צלעות, מעגלים ומיון טופולוגי.", do=show("s-2")),
    S("ובטענות: קוראים כמתים, מפריכים בדוגמה קטנה שמקיימת הכל, ומוכיחים, הרבה פעמים בשלילה. בהצלחה במבחן!",
      do=show("s-3"), hold=0.6),
], stage='<div class="gs-stack">'
         + st.card("s-1", "rule", "🔑 BFS: מרחקים, ישיגות, רכיבים, טיולים")
         + st.card("s-2", "rule", "🔑 DFS: זמנים, סוגי צלעות, מעגלים, מיון טופולוגי")
         + "</div>",
   panel=st.card("s-3", "ex", "טענות: כמתים · דוגמה נגדית קטנה · הוכחה בשלילה"))

VIDEO = Video("B08", "graph_search", "מבחן גמר: גרפים", [title, p1, p2, p3, recap],
              bank={"24A-B-Q1a": None, "24B-B-Q1b": None})
