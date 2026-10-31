# -*- coding: utf-8 -*-
"""B05 · מיון טופולוגי ומעגלים — video script (build: tools/video/vid.py B05).

Source: courses/graph_search/C05.js (lesson + goal: sort a DAG by finish times, check a given order, recognise when
there is no topological order at all).
Exam part: an original "בסגנון מבחן" question (bank={}): which of four orders is a topological order. The bank has no
topological-sort question.
Not used on purpose: the C05 quiz DAGs (A→B, A→D, B→C, D→C, D→E, F→E and A→B, A→C, B→D, C→D, E→D) and their
questions (the DFS order F, A, D, E, B, C, the four orders, f[D], the count 8, the added edges). The two DAGs here are
new; the "added edge" remark uses the run graph of this video.
Every finish time, the order, the validity of each order and every cycle claim are computed by w_graph_search
(graph_ref.py = the app's graph.js, an own DFS, networkx).
"""
import itertools

from vid import P, Scene, Video, show, hide
import stage as st
import w_graph_search as w
from w_graph_search import S

# ---------------------------------------------------------------- the run (verified)
N = list("ABCDEFG")
E = [("A", "D"), ("B", "A"), ("B", "E"), ("C", "E"), ("D", "F"), ("E", "D"), ("E", "G")]
POS = {"B": (60, 170), "A": (210, 60), "D": (380, 60), "F": (560, 60), "E": (330, 240), "C": (110, 350),
       "G": (540, 320)}
LAB = {"A": (0, -54), "D": (0, -54), "F": (0, -54)}
G1 = w.Graph("g", N, E, True, POS, w=620, h=400, lab_at=LAB, scale=1.0)
R = G1.dfs()
gx = w.nxg(N, E, True)
assert w.nx.is_directed_acyclic_graph(gx) and "back" not in R.cls.values()
assert R.fin == {"F": 4, "D": 5, "A": 6, "G": 10, "E": 11, "B": 12, "C": 14}
TOPO = R.topo
assert TOPO == ["C", "B", "E", "G", "A", "D", "F"]


def valid(order, edges):
    pos = {v: i for i, v in enumerate(order)}
    return all(pos[u] < pos[v] for u, v in edges)


assert valid(TOPO, E) and all(R.fin[u] > R.fin[v] for u, v in E)
assert TOPO[0] != R.order[0]                       # DFS starts at A, but A is not first in the order
ALL = [p for p in itertools.permutations(N) if valid(p, E)]
assert len(ALL) > 1 and list(TOPO) in [list(p) for p in ALL]         # not unique
assert valid(["B", "C", "A", "E", "D", "F", "G"], E)                   # another valid order (shown)
# added edges: a cycle exactly when the head already reaches the tail
assert w.nx.has_path(gx, "B", "F")
assert not w.nx.is_directed_acyclic_graph(w.nxg(N, E + [("F", "B")], True))
assert not w.nx.has_path(gx, "G", "F") and w.nx.is_directed_acyclic_graph(w.nxg(N, E + [("F", "G")], True))
CYC = ["B", "A", "D", "F"]
R.time_labels()
GR = R.groups(narrate=())
k = len(N)
EXTRA = {}
for i, (kind, evs) in enumerate(GR):
    for e in evs:
        if e[0] == "fin":
            EXTRA.setdefault(i, []).extend(show(f"tp-{e[1]}"))
PH = R.phrases(narrate=(), edges=("tree",), extra=EXTRA)
assert [kk for kk, _ in GR] == ["disc", "fin", "disc", "fin", "disc", "fin"], [kk for kk, _ in GR]
TP = ('<div class="gs-strip" dir="ltr"><span class="gs-slab">מיון</span>'
      + "".join(f'<span class="gs-slot"><b id="tp-{v}" class="gs-qv h">{v}</b></span>' for v in TOPO) + "</div>")

# ---------------------------------------------------------------- exam (original): which order is valid
NX = list("PQRTUW")
EX = [("P", "Q"), ("P", "R"), ("Q", "T"), ("R", "T"), ("U", "R"), ("U", "W"), ("W", "T")]
PX = {"P": (70, 80), "Q": (260, 40), "R": (260, 220), "T": (470, 130), "U": (90, 330), "W": (420, 340)}
G2 = w.Graph("x", NX, EX, True, PX, w=560, h=400, scale=0.95)
assert w.nx.is_directed_acyclic_graph(w.nxg(NX, EX, True))
ORD = {"a": list("UPWRQT"), "b": list("PQRUWT"), "c": list("PURWTQ"), "d": list("PQURTW")}
VIOL = {k: [(u, v) for u, v in EX if v in o[:o.index(u)]] for k, o in ORD.items()}
assert [k for k in ORD if valid(ORD[k], EX)] == ["a"]
assert VIOL == {"a": [], "b": [("U", "R")], "c": [("Q", "T")], "d": [("W", "T")]}, VIOL
OPTS = [(k, ", ".join(ORD[k])) for k in ("b", "d", "a", "c")]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    S("בסרטון הזה נמיין גרף מכוון חסר מעגלים, כך שכל צלע תצביע קדימה."),
    S("נשתמש בזמני הסיום של DFS, ונראה מתי אין מיון בכלל."),
    S("ובסוף שאלה בסגנון מבחן: איזה סדר תקין.", hold=0.4),
], stage='<div class="kicker">B05 · גרפים: BFS ו-DFS</div><h1>מיון טופולוגי ומעגלים</h1>'
         '<p>למיין גרף מכוון חסר מעגלים לפי זמני סיום, לבדוק אם סדר נתון תקין, ולזהות מתי אין מיון.</p>',
   layout="title")

idea = Scene("idea", "הרעיון", [
    S("גרף מכוון בלי מעגלים נקרא DAG. למשל קורסים, וצלע מקורס לקורס שדורש אותו.", do=show("i-1"),
      say_="גרף מכוון בלי מעגלים נקרא דָאג. למשל קורסים, וצלע מקורס לקורס שדורש אותו."),
    S("**מיון טופולוגי** הוא סידור של כל הקודקודים בשורה, כך שכל צלע הולכת משמאל לימין.", do=show("i-2")),
    S("האלגוריתם: מריצים DFS על כל הגרף, ומסדרים לפי זמן סיום **יורד**. מי שסיים אחרון, ראשון בשורה.",
      do=show("i-3")),
    S("למה זה עובד? ב-DAG אין צלעות אחורה. וכל צלע אחרת, מ-$u$ ל-$v$, מקיימת $f[v]<f[u]$.",
      say_="למה זה עובד? בדָאג אין צלעות אחורה. וכל צלע אחרת, מיוּ לוִי, מקיימת: אֶף של וִי קטן מאֶף של יוּ."),
    S("בצלע עץ או קדימה, $v$ צאצא ומסיים קודם. בצלע חוצה, $v$ סיים עוד לפני ש-$u$ התגלה.", do=show("i-4"),
      say_="בצלע עץ או קדימה, וִי צאצא ומסיים קודם. בצלע חוצה, וִי סיים עוד לפני שיוּ התגלה.", hold=0.4),
], stage='<div class="gs-stack">'
         + st.card("i-1", "plain", "DAG: גרף מכוון <b>חסר מעגלים</b>")
         + st.card("i-2", "ex", "מיון טופולוגי: לכל צלע $(u,v)$, $u$ לפני $v$")
         + "</div>",
   panel=st.card("i-3", "rule", "🔑 DFS, ואז סדר יורד של $f$")
         + st.card("i-4", "rule", "🔑 ב-DAG: לכל צלע $(u,v)$, $f[u]>f[v]$"))

run_ph = [
    S("נריץ DFS על ה-DAG הזה, בסדר אלפביתי. כל קודקוד שמסתיים נכנס **לתחילת** השורה.", do=show("r-g"),
      say_="נריץ דִּי אֶף אֶס על הדָאג הזה, בסדר אלפביתי. כל קודקוד שמסתיים נכנס לתחילת השורה."),
    *PH[:2],
    S("עכשיו $B$, עדיין לבן: עץ חדש, בזמן 7. הצלע אל $A$ פוגשת קודקוד שחור, אז ממשיכים ל-$E$, בזמן 8.",
      do=PH[2].do),
    S("גם $E$ מוצא את $D$ כבר שחור, ומגלה את $G$ בזמן 9."),
    *PH[3:],
    S("והשורה: $C$, $B$, $E$, $G$, $A$, $D$, $F$. כל צלע הולכת משמאל לימין.", do=show("r-c1")),
    S("שימו לב: התחלנו מ-$A$, אבל $A$ לא ראשון בשורה. זה בסדר, הסדר נקבע רק לפי זמני הסיום.", hold=0.4),
]
run = Scene("run", "הרצה", run_ph,
            stage=f'<div class="gs-stack"><div id="r-g" class="h">{G1.html(kinds=("tree",))}</div>{TP}</div>',
            panel=st.card("r-c1", "ex", "סדר יורד של $f$: " + ", ".join(TOPO)))

facts = Scene("facts", "מה חשוב לזכור", [
    S("שני דברים חשובים. ראשון: המיון **אינו יחיד**. גם $B$, $C$, $A$, $E$, $D$, $F$, $G$ תקין.", do=show("f-1"),
      say_="שני דברים חשובים. ראשון: המיון אינו יחיד. גם בִּי, סִי, אֵיי, אִי, דִּי, אֶף, גִ'י תקין."),
    S("לכן כדי לבדוק סדר נתון לא משווים לתשובה אחת, אלא עוברים על **כל צלע** ובודקים שהיא הולכת קדימה.",
      do=show("f-2")),
    S("שני: יש מיון טופולוגי **אם ורק אם** אין מעגל. מעגל דורש שכל קודקוד בו יופיע לפני עצמו.",
      do=show("f-3")),
    S("ו-DFS מזהה מעגל בדיוק כשהוא מוצא צלע אחורה.",),
    S("למשל, אם נוסיף צלע מ-$F$ ל-$B$, ייסגר מעגל, כי כבר יש מסלול מ-$B$ ל-$F$.",
      do=show("f-g", *[f"fg-m-{v}" for v in CYC], "f-4")),
    S("אבל צלע מ-$F$ ל-$G$ לא סוגרת מעגל: אין מסלול מ-$G$ ל-$F$. צלע יוצרת מעגל רק אם יש מסלול חזרה.",
      do=hide(*[f"fg-m-{v}" for v in CYC]) + show("f-5"), hold=0.4),
], stage='<div class="gs-stack"><div id="f-g" class="h">{}</div></div>',
   panel=st.card("f-1", "ex", "גם $B,C,A,E,D,F,G$ תקין")
         + st.card("f-2", "rule", "🔑 בדיקת סדר: כל צלע $(u,v)$, $u$ לפני $v$")
         + st.card("f-3", "rule", "🔑 יש מיון ⇔ אין מעגל ⇔ אין צלע אחורה")
         + st.card("f-4", "trap", "⚠️ $F\\to B$: מעגל $B\\to A\\to D\\to F\\to B$")
         + st.card("f-5", "ex", "$F\\to G$: אין מסלול $G\\leadsto F$, אין מעגל"))

ex_ph = [
    S("ועכשיו שאלה בסגנון מבחן: איזה מהסדרים הוא מיון טופולוגי של הגרף?", do=show("x-gw", "x-opts")),
    S("לא מריצים שום דבר. עוברים על כל צלע ובודקים שההתחלה שלה לפני הסוף שלה."),
    S("בסדר שמתחיל ב-$P$, $Q$, $R$: הצלע מ-$U$ ל-$R$ נשברת, כי $R$ מופיע לפני $U$.",
      do=show(G2.eid("U", "R", "back"), "x-x-b", "x-n-b")),
    S("בסדר שמסתיים ב-$T$ ו-$W$: הצלע מ-$W$ ל-$T$ נשברת, כי $T$ לפני $W$.",
      do=hide(G2.eid("U", "R", "back")) + show(G2.eid("W", "T", "back"), "x-x-d", "x-n-d")),
    S("בסדר שמסתיים ב-$T$ ו-$Q$: הצלע מ-$Q$ ל-$T$ נשברת, כי $T$ לפני $Q$.",
      do=hide(G2.eid("W", "T", "back")) + show(G2.eid("Q", "T", "back"), "x-x-c", "x-n-c")),
    S("ובסדר הנותר כל שבע הצלעות הולכות קדימה. זו התשובה.",
      do=hide(G2.eid("Q", "T", "back")) + show(*[G2.eid(u, v, "tree") for u, v in EX], "x-ok-a")),
    S("המלכודת: לחשוב שיש מיון אחד נכון, ולפסול סדר רק כי DFS אלפביתי היה נותן סדר אחר.", do=show("x-t"),
      hold=0.5),
]
exam = Scene("exam", "שאלה בסגנון מבחן", ex_ph,
             stage=f'<div id="x-gw" class="h">{G2.html(kinds=("tree", "back"))}</div>',
             panel='<div class="gs-q"><span class="qid">בסגנון מבחן</span>איזה מהסדרים הבאים הוא מיון טופולוגי של '
                   'הגרף?</div>'
                   + '<div id="x-opts" class="h gs-opts">'
                   + st.options("x", OPTS, notes={"b": "$U\\to R$", "c": "$Q\\to T$", "d": "$W\\to T$"})
                   + "</div>"
                   + st.card("x-t", "trap", "⚠️ המיון לא יחיד: בודקים צלעות, לא משווים לריצה אחת"))

recap = Scene("recap", "סיכום", [
    S("לסיכום: מיון טופולוגי הוא DFS, ואז סדר יורד של זמני הסיום.", do=show("s-1")),
    S("הוא קיים בדיוק כשאין מעגל, כלומר כש-DFS לא מוצא צלע אחורה.", do=show("s-2")),
    S("והוא לא יחיד: בודקים סדר נתון צלע אחרי צלע. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage='<div class="gs-stack">'
         + st.card("s-1", "rule", "🔑 מיון = סדר יורד של $f$")
         + st.card("s-2", "rule", "🔑 קיים ⇔ אין מעגל ⇔ אין צלע אחורה")
         + "</div>",
   panel=st.card("s-3", "trap", "⚠️ לא יחיד: בודקים כל צלע"))

# the "added edge" figure: the run graph, finished, with the cycle vertices marked
G3 = w.Graph("fg", N, E, True, POS, w=620, h=400, lab_at=LAB, scale=0.95)
R3 = G3.dfs()
assert R3.fin == R.fin
facts.stage = facts.stage.replace("{}", G3.html(kinds=()))
for v in CYC:
    assert f'id="fg-m-{v}"' in facts.stage

VIDEO = Video("B05", "graph_search", "מיון טופולוגי ומעגלים", [title, idea, run, facts, exam, recap], bank={})
