# -*- coding: utf-8 -*-
"""B04 · DFS: ארבעת סוגי הצלעות — video script (build: tools/video/vid.py B04).

Source: courses/graph_search/C04.js (lesson + goal: classify every edge of a DFS run as tree / back / forward / cross,
and conclude about cycles and descendants).
Exam part: an original "בסגנון מבחן" question (bank={}): how many edges of each kind in a DFS run. The bank has no
edge-classification question.
Not used on purpose: the C04 quiz graphs (A→B, A→C, A→D, B→C, C→A, E→D, E→F and P→Q, Q→R, R→S, P→S, S→T, T→R) and
their questions (C→A, A→C, the 7/10 2/5 times, undirected kinds, the cycle question, descendants of A). Both graphs
here are new.
Every class is computed by w_graph_search (graph_ref.py = the app's graph.js, an own DFS, the interval rule, networkx
for the cycle claim).
"""
from collections import Counter

from vid import P, Scene, Video, show, hide
import stage as st
import w_graph_search as w
from w_graph_search import S

# ---------------------------------------------------------------- the run (verified)
N = list("ABCDEF")
E = [("A", "C"), ("A", "D"), ("C", "B"), ("B", "D"), ("D", "C"), ("E", "B"), ("E", "F"), ("F", "D")]
POS = {"A": (70, 190), "C": (240, 60), "B": (440, 60), "D": (330, 280), "E": (610, 130), "F": (570, 340)}
LAB = {"C": (0, -54), "B": (0, -54), "E": (0, -54), "A": (0, 58), "D": (0, 58), "F": (0, 58)}
G1 = w.Graph("g", N, E, True, POS, w=680, h=400, lab_at=LAB, scale=1.05)
R = G1.dfs()
assert R.cls == {("A", "C"): "tree", ("C", "B"): "tree", ("B", "D"): "tree", ("D", "C"): "back", ("A", "D"): "fwd",
                 ("E", "B"): "cross", ("E", "F"): "tree", ("F", "D"): "cross"}
assert R.disc["A"] < R.disc["D"] and R.fin["D"] < R.fin["A"]                     # A→D: D is a finished descendant
assert R.fin["B"] < R.disc["E"] and R.fin["D"] < R.disc["F"]                     # cross edges point to the past
assert not w.nx.is_directed_acyclic_graph(w.nxg(N, E, True))
CYC = ["C", "B", "D"]                                                             # the cycle the back edge closes
assert R.pi["B"] == "C" and R.pi["D"] == "B"
R.time_labels()
PH = R.phrases()
GR = R.groups()
assert [k for k, _ in GR] == ["disc", "disc", "edge", "fin", "edge", "fin", "disc", "edge", "disc", "edge", "fin"], [k for k, _ in GR]

# ---------------------------------------------------------------- exam (original): count the kinds
NX = list("PQRTUW")
EX = [("P", "Q"), ("Q", "R"), ("R", "P"), ("P", "R"), ("T", "Q"), ("T", "U"), ("U", "W"), ("W", "T"), ("U", "R")]
PX = {"P": (80, 70), "Q": (290, 70), "R": (180, 270), "T": (470, 70), "U": (450, 280), "W": (630, 180)}
LX = {"P": (0, -54), "Q": (0, -54), "T": (0, -54), "R": (0, 58), "U": (0, 58), "W": (0, 58)}
G2 = w.Graph("x", NX, EX, True, PX, w=680, h=380, lab_at=LX, scale=0.95)
X = G2.dfs()
CNT = Counter(X.cls.values())
TRUE = (CNT["tree"], CNT["back"], CNT["fwd"], CNT["cross"])
assert TRUE == (4, 2, 1, 2)
assert CNT["tree"] == len(NX) - len(X.roots) and X.roots == ["P", "T"]
assert X.kind("P", "R") == "fwd" and X.kind("T", "Q") == "cross" and X.kind("U", "R") == "cross"
OPT = {"a": TRUE,
       "b": (4, 2, 0, 3),     # the forward edge counted as cross (black, without comparing d)
       "c": (4, 4, 1, 0),     # every edge to a visited vertex counted as back
       "d": (5, 2, 1, 1)}     # |V|-1 tree edges, as if the forest were one tree
assert TRUE[0] + TRUE[1] + TRUE[2] + TRUE[3] == len(EX) and all(sum(v) == len(EX) for v in OPT.values())
assert [k for k, v in OPT.items() if v == TRUE] == ["a"]
X.time_labels()
XPH = X.phrases()
fmt = lambda t: f"עץ {t[0]} · אחורה {t[1]} · קדימה {t[2]} · חוצה {t[3]}"
OPTS = [(k, fmt(OPT[k])) for k in ("c", "a", "d", "b")]

KINDS = w.table("kt", ["צבע $v$ כשבוחנים את $(u,v)$", "סוג"],
                [["לבן", "עץ"], ["אפור", "אחורה"], ["שחור, $d[u]<d[v]$", "קדימה"], ["שחור, $d[u]>d[v]$", "חוצה"]]).replace('dir="ltr"', 'dir="rtl"')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    S("בסרטון הזה נסווג כל צלע בריצת DFS לאחד מארבעה סוגים."),
    S("ונראה מה הסוגים אומרים: מתי יש מעגל, ומה קורה בגרף לא מכוון."),
    S("ובסוף שאלה בסגנון מבחן: לספור צלעות מכל סוג.", hold=0.4),
], stage='<div class="kicker">B04 · גרפים: BFS ו-DFS</div><h1>DFS: ארבעת סוגי הצלעות</h1>'
         '<p>לסווג כל צלע לעץ, אחורה, קדימה או חוצה, ולהסיק מכך על מעגלים וצאצאים.</p>', layout="title")

idea = Scene("idea", "הכלל", [
    S("כשהריצה בוחנת צלע מכוונת מ-$u$ ל-$v$, הכל תלוי בצבע של $v$ **באותו רגע**."),
    S("$v$ לבן: הוא מתגלה עכשיו דרך הצלע. זו צלע **עץ**.", do=show("kt-r0")),
    S("$v$ אפור: הוא עדיין פתוח, כלומר אב קדמון של $u$ על המחסנית. זו צלע **אחורה**.", do=show("kt-r1")),
    S("$v$ שחור: הוא כבר סיים. כאן משווים זמני גילוי.", do=show("kt-r2", "kt-r3")),
    S("אם $u$ התגלה קודם, $v$ הוא צאצא שכבר סיים: צלע **קדימה**.", do=show("kt-c2-1")),
    S("ואם $v$ התגלה קודם, הוא בענף אחר או בעץ אחר, שסיים לפני ש-$u$ התחיל: צלע **חוצה**.",
      do=hide("kt-c2-1") + show("kt-c3-1"), hold=0.4),
], stage=f'<div class="gs-stack">{KINDS}{w.legend("lg", ["tree", "back", "fwd", "cross"], hidden=False)}</div>',
   panel=st.card("i-1", "rule", "🔑 קובע: הצבע של $v$ ברגע הבדיקה")
         .replace('class="card rule h"', 'class="card rule"'))

run_ph = [
    S("נריץ DFS על הגרף המכוון הזה, בסדר אלפביתי, ונסווג כל צלע ברגע שהיא נבחנת.", do=show("r-g", "r-lg")),
    *PH[:2],
    *PH[2:3],
    S("ולכן $D\\to C$ סוגרת מעגל: מ-$C$ ל-$B$, ל-$D$, וחזרה ל-$C$.",
      do=show(*[G1.mark(v) for v in CYC], "r-c1"),
      say_="ולכן הצלע מדִּי לסִי סוגרת מעגל: מסִי לבִּי, לדִּי, וחזרה לסִי."),
    PH[3],
    S(PH[4].sub, do=hide(*[G1.mark(v) for v in CYC]) + PH[4].do),
    *PH[5:],
    S("ספרו: ארבע צלעות עץ, אחת אחורה, אחת קדימה, ושתיים חוצות.", do=show("r-c2"), hold=0.4),
]
run = Scene("run", "הרצה", run_ph,
            stage=f'<div class="gs-stack"><div id="r-g" class="h">{G1.html()}</div>'
                  f'<div id="r-lg" class="h">{w.legend("rl", ["tree", "back", "fwd", "cross"], hidden=False)}</div></div>',
            panel=st.card("r-c1", "rule", "🔑 צלע אחורה ← מעגל: $C\\to B\\to D\\to C$")
                  + st.card("r-c2", "ex", "עץ 4 · אחורה 1 · קדימה 1 · חוצה 2"))

rules = Scene("rules", "מה זה נותן", [
    S("קודם כלי אחד, **משפט השביל הלבן**: $v$ יהיה צאצא של $u$ אם ורק אם ברגע הגילוי של $u$ יש אליו מסלול לבן.",
      do=show("u-4"),
      say_="קודם כלי אחד, משפט השביל הלבן: וִי יהיה צאצא של יוּ, אם ורק אם ברגע הגילוי של יוּ יש אליו מסלול שכולו לבן."),
    S("ועכשיו שתי מסקנות. ראשונה: בגרף מכוון יש מעגל **אם ורק אם** DFS מוצא צלע אחורה.", do=show("u-1")),
    S("כיוון אחד ראינו: צלע אחורה ומסלול העץ שמתחתיה סוגרים מעגל."),
    S("ובכיוון השני: על מעגל יש קודקוד שמתגלה ראשון. ברגע הזה כל שאר המעגל עדיין לבן."),
    S("לפי השביל הלבן, הקודקוד שלפניו במעגל יהיה צאצא שלו, והצלע ממנו חזרה אליו תהיה צלע אחורה."),
    S("צלעות קדימה וחוצות לבדן לא יוצרות מעגל.", do=show("u-2")),
    S("שנייה: בגרף **לא מכוון** יש רק צלעות עץ וצלעות אחורה.", do=show("u-3")),
    S("כי אם $u$ ו-$v$ שכנים, מי שהתגלה ראשון עוד פתוח כשהשני מתגלה. אז השני צאצא שלו, ואין חוצה.",
      say_="כי אם יוּ ווִי שכנים, מי שהתגלה ראשון עוד פתוח כשהשני מתגלה. אז השני צאצא שלו, ואין חוצה."),
    S("ואין קדימה: הצלע נבחנת לראשונה מהקצה שהתגלה מאוחר, כשהקצה השני עוד אפור. לכן היא צלע אחורה.",
      hold=0.4),
], stage='<div class="gs-stack">'
         + st.card("u-1", "rule", "🔑 מכוון: מעגל ⇔ צלע <b>אחורה</b>")
         + st.card("u-2", "ex", "קדימה וחוצה: לא מעידות על מעגל")
         + "</div>",
   panel=st.card("u-3", "rule", "🔑 לא מכוון: רק עץ ואחורה")
         + st.card("u-4", "rule", "🔑 שביל לבן ברגע $d[u]$ ⇔ צאצא של $u$"))

ex_ph = [
    S("ועכשיו שאלה בסגנון מבחן. מריצים DFS על הגרף, בסדר אלפביתי. כמה צלעות יש מכל סוג?", do=show("x-gw", "x-opts")),
    *XPH,
    S("סופרים: ארבע עץ, שתיים אחורה, אחת קדימה, ושתיים חוצות. זו האפשרות הנכונה.", do=show("x-ok-a")),
    S("מי שספר את $P\\to R$ כחוצה, שכח להשוות זמני גילוי: $R$ שחור, אבל הוא צאצא של $P$.",
      do=show("x-x-b", "x-n-b"),
      say_="מי שספר את הצלע מפִּי לאָר כחוצה, שכח להשוות זמני גילוי: אָר שחור, אבל הוא צאצא של פִּי."),
    S("מי שספר כל צלע אל קודקוד שכבר התגלה כאחורה, פספס את הצבע: אחורה רק אל קודקוד **אפור**.",
      do=show("x-x-c", "x-n-c")),
    S("ומי שספר חמש צלעות עץ, הניח עץ אחד. אבל יש שני שורשים, $P$ ו-$T$, ולכן שש פחות שתיים: ארבע.",
      do=show("x-x-d", "x-n-d")),
    S("ושתי צלעות האחורה אומרות שיש בגרף מעגלים. למשל $P$, $Q$, $R$ וחזרה ל-$P$.", hold=0.5),
]
exam = Scene("exam", "שאלה בסגנון מבחן", ex_ph,
             stage=f'<div class="gs-stack"><div id="x-gw" class="h">{G2.html()}</div>'
                   f'{w.legend("xl", ["tree", "back", "fwd", "cross"], hidden=False)}</div>',
             panel='<div class="gs-q"><span class="qid">בסגנון מבחן</span>מריצים DFS על הגרף (שכנים והלולאה '
                   'החיצונית בסדר אלפביתי). כמה צלעות מכל סוג?</div>'
                   + '<div id="x-opts" class="h gs-opts">'
                   + st.options("x", OPTS, notes={"b": "קדימה≠חוצה", "c": "רק אפור", "d": "2 עצים"})
                   + "</div>")

recap = Scene("recap", "סיכום", [
    S("לסיכום: לבן זה עץ, אפור זה אחורה, ושחור זה קדימה או חוצה, לפי מי התגלה קודם.", do=show("s-1")),
    S("בגרף מכוון, מעגל קיים בדיוק כשיש צלע אחורה.", do=show("s-2")),
    S("ובגרף לא מכוון יש רק עץ ואחורה. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage='<div class="gs-stack">'
         + st.card("s-1", "rule", "🔑 לבן: עץ · אפור: אחורה · שחור: קדימה / חוצה")
         + st.card("s-2", "rule", "🔑 מעגל מכוון ⇔ צלע אחורה")
         + "</div>",
   panel=st.card("s-3", "trap", "⚠️ לא מכוון: אין קדימה ואין חוצה"))

VIDEO = Video("B04", "graph_search", "DFS: ארבעת סוגי הצלעות", [title, idea, run, rules, exam, recap], bank={})
