# -*- coding: utf-8 -*-
"""DEMO-G: the graph-visualizer demo exam (never shipped). One question per graph.js algorithm, with question-level
graphs (drawn under the question + the step-through in the solution), a step-level graph (locked until answered),
`expect` answers and step `key`s that tools/validate.py checks against graph.js.

    PYTHONUTF8=1 py tools/gen/gen_DEMO-G.py && PYTHONUTF8=1 py tools/build_questions.py --demo && node tools/verify_dom.js
    (then rebuild WITHOUT --demo before committing anything built)
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "DEMO-G.json"


def E(*triples):
    return [dict(zip(("u", "v", "w"), t)) for t in triples]


BFS = {"directed": False, "algo": "bfs", "source": "A", "nodes": ["A", "B", "C", "D", "E", "F"],
       "edges": E(("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "F")),
       "expect": {"order": ["A", "B", "C", "D", "E", "F"], "d": {"D": 2, "F": 3}, "pi": {"E": "C"}}}
DFS = {"directed": True, "algo": "dfs", "caption": "הגרף מאיור 22.4 בספר CLRS",
       "nodes": [{"id": "u", "x": 0, "y": 0}, {"id": "v", "x": 1, "y": 0}, {"id": "w", "x": 2, "y": 0},
                 {"id": "x", "x": 0, "y": 1}, {"id": "y", "x": 1, "y": 1}, {"id": "z", "x": 2, "y": 1}],
       "edges": E(("u", "v"), ("u", "x"), ("v", "y"), ("w", "y"), ("w", "z"), ("x", "v"), ("y", "x"), ("z", "z")),
       "expect": {"disc": {"u": 1, "v": 2, "y": 3, "x": 4, "w": 9, "z": 10},
                  "fin": {"x": 5, "y": 6, "v": 7, "u": 8, "z": 11, "w": 12},
                  "classes": {"x-v": "back", "u-x": "forward", "w-y": "cross", "z-z": "back"}}}
TOPO = {"directed": True, "algo": "topo", "layout": "layers", "nodes": ["A", "B", "C", "D", "E"],
        "edges": E(("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")),
        "expect": {"topo": ["A", "C", "B", "D", "E"], "fin": {"A": 10}}}
SCC = {"directed": True, "algo": "scc", "nodes": ["A", "B", "C", "D", "E", "F"],
       "edges": E(("A", "B"), ("B", "C"), ("C", "A"), ("B", "D"), ("D", "E"), ("E", "D"), ("E", "F")),
       "expect": {"scc": [["A", "B", "C"], ["D", "E"], ["F"]]}}
DIJ = {"directed": True, "algo": "dijkstra", "source": "A", "nodes": ["A", "B", "C", "D", "E"],
       "edges": E(("A", "B", 4), ("A", "C", 1), ("C", "B", 2), ("B", "D", 1), ("C", "D", 5), ("D", "E", 3)),
       "expect": {"d": {"A": 0, "B": 3, "C": 1, "D": 4, "E": 7}, "pi": {"B": "C", "D": "B"}}}
WG = E(("A", "B", 2), ("A", "C", 3), ("B", "C", 1), ("B", "D", 4), ("C", "D", 5), ("C", "E", 6), ("D", "E", 7))
PRIM = {"directed": False, "algo": "prim", "source": "A", "nodes": ["A", "B", "C", "D", "E"], "edges": WG,
        "expect": {"weight": 13, "mst": [["A", "B"], ["B", "C"], ["B", "D"], ["C", "E"]]}}
KRU = {"directed": False, "algo": "kruskal", "nodes": ["A", "B", "C", "D", "E"], "edges": WG,
       "expect": {"weight": 13}}

BASE = {"kind": "computation", "solutionSource": "solved", "official": False, "confidence": "high",
        "stepsSource": "ai-verified"}


def Q(num, topic, question, solution, graph, steps):
    q = dict(BASE, num=num, topic=topic, question=question, solution=solution, steps=steps)
    if graph:
        q["graph"] = graph
    return q


questions = [
    Q(1, "graphs_search", "הריצו BFS מהקודקוד A על הגרף הלא מכוון. השכנים נסרקים לפי סדר אלפביתי.",
      "סדר הגילוי הוא A, B, C, D, E, F. המרחקים: $d[B] = d[C] = 1$, $d[D] = d[E] = 2$ ו-$d[F] = 3$.", BFS, [
          {"type": "numeric", "prompt": "מהו $d[F]$ בסוף הריצה?", "answer": 3, "key": "d.F", "explain": "המסלול A, B, D, F."},
          {"type": "text", "prompt": "כתבו את סדר הגילוי, מופרד בפסיקים.", "accept": ["A, B, C, D, E, F"], "key": "order",
           "explain": "BFS מגלה שכבה אחרי שכבה."},
          {"type": "choice", "prompt": "מיהו $\\pi[E]$?", "options": [{"id": "a", "value": "C"}, {"id": "b", "value": "D"},
                                                                {"id": "c", "value": "A"}], "correctId": "a", "key": "pi.E",
           "explain": "E מתגלה כשמוציאים את C מהתור."}]),
    Q(2, "graphs_search", "הריצו DFS על הגרף המכוון (הלולאה הראשית והשכנים בסדר אלפביתי) ורשמו זמני גילוי וסיום.",
      "זמני הגילוי והסיום: `u 1/8`, `v 2/7`, `y 3/6`, `x 4/5`, `w 9/12`, `z 10/11`. הקשת $x \\to v$ היא קשת אחורה, הקשת $u \\to x$ היא קשת קדימה והקשת $w \\to y$ היא קשת חוצה.", DFS, [
          {"type": "numeric", "prompt": "מהו $f[u]$?", "answer": 8, "key": "fin.u", "explain": "u נסגר אחרי v, y ו-x."},
          {"type": "choice", "prompt": "מה הסוג של הקשת $x \\to v$?", "options": [
              {"id": "a", "value": "קשת אחורה"}, {"id": "b", "value": "קשת קדימה"},
              {"id": "c", "value": "קשת חוצה"}, {"id": "d", "value": "קשת עץ"}], "correctId": "a", "key": "class.x-v",
           "explain": "כשבודקים את הקשת $x \\to v$, הקודקוד v עדיין אפור."}]),
    Q(3, "graphs_search", "מצאו מיון טופולוגי של הגרף בעזרת DFS (סדר אלפביתי).",
      "לפי זמני סיום יורדים: A, C, B, D, E.", TOPO, [
          {"type": "text", "prompt": "כתבו את המיון הטופולוגי.", "accept": ["A, C, B, D, E"], "key": "topo",
           "explain": "כל קודקוד שמסתיים נכנס לראש הרשימה."}]),
    Q(4, "graphs_search", "מצאו את הרכיבים הקשירים היטב בעזרת אלגוריתם קוסרג'ו.",
      "שלושה רכיבים: {A, B, C}, {D, E}, {F}.", SCC, [
          {"type": "numeric", "prompt": "כמה רכיבים קשירים היטב יש בגרף?", "answer": 3, "key": "sccCount",
           "explain": "כל שורש של ה-DFS השני פותח רכיב."}]),
    Q(5, "graphs_search", "הריצו את אלגוריתם דייקסטרה מהקודקוד A.",
      "המרחקים הסופיים: $d[A] = 0$, $d[C] = 1$, $d[B] = 3$, $d[D] = 4$ ו-$d[E] = 7$.", DIJ, [
          {"type": "numeric", "prompt": "מהו $d[E]$ בסוף הריצה?", "answer": 7, "key": "d.E", "explain": "המסלול הקצר עובר דרך C, B ו-D."}]),
    Q(6, "mst", "הריצו את אלגוריתם פרים מהקודקוד A.",
      "העץ: A–B, B–C, B–D, C–E, ומשקלו 13.", PRIM, [
          {"type": "numeric", "prompt": "מהו משקל העץ הפורש המינימלי?", "answer": 13, "key": "weight",
           "explain": "2 + 1 + 4 + 6 = 13."}]),
    Q(7, "mst", "הריצו את אלגוריתם קרוסקל על הגרף שבצעד.",
      "קרוסקל לוקח את B–C, A–B, B–D ו-C–E ומדלג על A–C ו-C–D. המשקל 13.", None, [
          {"type": "numeric", "prompt": "מהו משקל העץ שקרוסקל בונה?", "answer": 13, "key": "weight", "graph": KRU,
           "explain": "אותו עץ כמו בפרים, כי המשקלים שונים זה מזה."}]),
]

data = {"examCode": "DEMO-G", "examLabel": "הדגמה: מציג הגרפים", "year": 2026, "examDate": "",
        "sourceFile": "", "solutionFile": "", "questions": questions}
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
