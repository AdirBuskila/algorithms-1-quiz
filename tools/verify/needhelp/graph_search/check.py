# -*- coding: utf-8 -*-
"""Machine checks for the guided course `graph_search` (courses/graph_search/C01..C08.js).

What is checked
  1. every graph in the course (lesson figures, question graphs, step graphs) runs through graph.js, through the independent
     Python reference tools/graph_ref.py and through networkx: identical event sequences and outputs; graph_check.js accepts
     every graph, every `expect` block and every step `key`;
  2. every stored answer of every own question is recomputed here with an implementation of BFS/DFS that is independent
     of graph.js and graph_ref.py (plain Python + networkx);
  3. every claim and counterexample used in a lesson or an explanation is brute-forced with networkx on all small graphs;
  4. structure: the levels, the boss, the bankIds (present in the bank, steps verified), no option cited by position.

Run:  PYTHONUTF8=1 py tools/verify/needhelp/graph_search/check.py        (ASCII output, exit 1 on any failure)
"""
import itertools, json, os, random, re, subprocess, sys
from collections import deque
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ENV = {**os.environ, "PYTHONUTF8": "1"}
random.seed(20261025)
ok = True
nchecks = 0


def check(name, cond, extra=""):
    global ok, nchecks
    nchecks += 1
    if not cond:
        print("FAIL " + name + (" " + str(extra)[:300] if extra != "" else ""))
    ok &= bool(cond)


def asc(s):
    return s.encode("ascii", "replace").decode()


# ---------------------------------------------------------------------------------------------- load the course
ld = subprocess.run(["node", str(ROOT / "tools" / "course_load.js")], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=ROOT)
loaded = json.loads(ld.stdout)
check("course files load without errors", not loaded["errors"], loaded["errors"])
LEVELS = sorted([e["level"] for e in loaded["levels"] if e["courseId"] == "graph_search"], key=lambda l: l["order"])
check("8 levels C01..C08", [l["id"] for l in LEVELS] == ["C0%d" % i for i in range(1, 9)])
check("only the last level is the boss", [bool(l.get("boss")) for l in LEVELS] == [False] * 7 + [True])
Q = {}
for lv in LEVELS:
    for q in lv["questions"]:
        if "id" in q:
            Q[q["id"]] = q
BANK = {x["id"]: x for x in json.load(open(ROOT / "questions.json", encoding="utf-8"))["questions"]}
GRAPH_ATTR = re.compile(r"""data-graph=(['"])(.*?)\1""", re.S)


def step_of(qid):
    return Q[qid]["step"]


def gspec(qid):
    q = Q[qid]
    g = (q.get("step") or {}).get("graph") or q.get("graph")
    assert g is not None, qid
    return g


# ---------------------------------------------------------------------------------------------- 1. graph traces
specs, where = [], []
for lv in LEVELS:
    for m in GRAPH_ATTR.finditer(lv["lesson"]["html"]):
        specs.append(json.loads(m.group(2)))
        where.append(lv["id"] + " lesson")
    for q in lv["questions"]:
        for g, tag in ((q.get("graph"), "graph"), ((q.get("step") or {}).get("graph"), "step graph")):
            if g is not None:
                for gg in (g if isinstance(g, list) else [g]):
                    specs.append(gg)
                    where.append("%s %s %s" % (lv["id"], q.get("id"), tag))
print("graphs in the course:", len(specs), "| with an algorithm:", sum(1 for s in specs if s.get("algo")))
check("the course embeds graphs", len(specs) >= 25)
for lv in LEVELS[:7]:
    check(lv["id"] + " lesson has a graph figure", "graph-fig" in lv["lesson"]["html"])
check("step keys used", sum(1 for q in Q.values() if (q.get("step") or {}).get("key")) >= 8)

algo_idx = [i for i, s in enumerate(specs) if s.get("algo")]
bare = [{k: v for k, v in specs[i].items() if k != "expect"} for i in algo_idx]
py = subprocess.run([sys.executable, str(ROOT / "tools" / "graph_ref.py")], input=json.dumps(bare), capture_output=True, text=True, env=ENV)
check("graph_ref.py ran", py.returncode == 0, py.stderr[:300])
js = subprocess.run(["node", str(ROOT / "tools" / "verify" / "learn" / "graph_js.js")], input=json.dumps(bare), capture_output=True, text=True, encoding="utf-8", env=ENV)
check("graph.js ran", js.returncode == 0, js.stderr[:300])
canon = lambda x: json.dumps(x, sort_keys=True)
if py.returncode == 0 and js.returncode == 0:
    ref, got = json.loads(py.stdout), json.loads(js.stdout)
    for n, i in enumerate(algo_idx):
        w = asc(where[i])
        check(w + ": events graph.js == graph_ref.py", canon(got[n]["events"]) == canon(ref[n]["events"]))
        check(w + ": outputs graph.js == graph_ref.py", all(canon(got[n]["result"].get(k)) == canon(v) for k, v in ref[n]["result"].items()))
        check(w + ": networkx agrees (graph_ref cross-check)", not ref[n]["nx"], ref[n]["nx"])
        check(w + ": graph.js has no problem", not got[n]["problems"], got[n]["problems"])

jobs = [{"where": asc(w), "spec": s} for w, s in zip(where, specs)]
for lv in LEVELS:
    for q in lv["questions"]:
        st = q.get("step")
        if st and st.get("key"):
            jobs.append({"where": "%s %s key %s" % (lv["id"], q["id"], st["key"]), "spec": st["graph"], "key": st["key"], "step": st})
gc = subprocess.run(["node", str(ROOT / "tools" / "graph_check.js")], input=json.dumps(jobs), capture_output=True, text=True, encoding="utf-8", env=ENV)
res = json.loads(gc.stdout)
check("graph_check.js judged every job", len(res) == len(jobs))
for r in res:
    check(r["where"] + ": graph_check.js accepts", r["ok"], r["problems"])
for w, s in zip(where, specs):
    if s.get("algo") and "lesson" in w:
        check(asc(w) + ": lesson trace carries an expect block", bool(s.get("expect")))


# ---------------------------------------------------------------------------------------------- independent algorithms
def build_adj(spec):
    nodes = [str(n["id"] if isinstance(n, dict) else n) for n in spec["nodes"]]
    adj = {v: set() for v in nodes}
    for e in spec["edges"]:
        adj[str(e["u"])].add(str(e["v"]))
        if not spec["directed"]:
            adj[str(e["v"])].add(str(e["u"]))
    return nodes, {v: sorted(adj[v]) for v in nodes}


def my_bfs(adj, s):
    d, pi, order, q = {s: 0}, {s: None}, [s], deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in d:
                d[v], pi[v] = d[u] + 1, u
                order.append(v)
                q.append(v)
    return d, pi, order


def my_dfs(adj, roots, directed):
    """returns disc, fin, pi, classes(dict (u,v)->kind), order. Undirected: every edge classified once, at its first examination."""
    state, disc, fin, pi, cls, order = {}, {}, {}, {}, {}, []
    clock = [0]
    seen_und = set()

    def visit(u):
        clock[0] += 1
        disc[u] = clock[0]
        order.append(u)
        state[u] = "g"
        for v in adj[u]:
            if not directed:
                key = frozenset((u, v))
                if key in seen_und:
                    continue
            st = state.get(v, "w")
            if st == "w":
                if not directed:
                    seen_und.add(frozenset((u, v)))
                cls[(u, v)] = "tree"
                pi[v] = u
                visit(v)
            elif st == "g":
                if not directed:
                    seen_und.add(frozenset((u, v)))
                cls[(u, v)] = "back"
            else:
                if not directed:
                    seen_und.add(frozenset((u, v)))
                    cls[(u, v)] = "back"
                else:
                    cls[(u, v)] = "forward" if disc[u] < disc[v] else "cross"
        clock[0] += 1
        fin[u] = clock[0]
        state[u] = "b"

    for r in roots:
        if state.get(r, "w") == "w":
            pi[r] = None
            visit(r)
    return disc, fin, pi, cls, order


def nxg(spec):
    nodes, adj = build_adj(spec)
    g = nx.DiGraph() if spec["directed"] else nx.Graph()
    g.add_nodes_from(nodes)
    for e in spec["edges"]:
        g.add_edge(str(e["u"]), str(e["v"]))
    return g, nodes, adj


def tree_edges(pi):
    return {frozenset((v, p)) for v, p in pi.items() if p is not None}


def depth_of(pi):
    dep = {}
    for v in pi:
        x, k = v, 0
        while pi[x] is not None:
            x, k = pi[x], k + 1
        dep[v] = k
    return dep


# ---------------------------------------------------------------------------------------------- 2. own questions
# ---- C01
g, nodes, adj = nxg(gspec("C01-Q2"))
d, pi, order = my_bfs(adj, "A")
check("C01-Q2 order", order == "A C D B E F G".split() and "A, C, D, B, E, F, G" in step_of("C01-Q2")["accept"])
check("C01-Q3 d[G] via networkx", nx.shortest_path_length(g, "A", "G") == 4 == step_of("C01-Q3")["answer"] == d["G"])
check("C01-Q4 pi[E]=C", pi["E"] == "C" and {o["id"]: o["value"] for o in step_of("C01-Q4")["options"]}[step_of("C01-Q4")["correctId"]] == "C")
check("C01-Q4 D is a neighbour of E but not the parent (distractor fails observably)", "D" in adj["E"] and pi["E"] != "D")
q5 = deque(["A"])
seen = {"A"}
for _ in range(2):
    u = q5.popleft()
    for v in adj[u]:
        if v not in seen:
            seen.add(v)
            q5.append(v)
Q5opts = {o["id"]: o["value"] for o in Q["C01-Q5"]["options"]}
check("C01-Q5 queue after A, C = D, B, E", list(q5) == ["D", "B", "E"] and Q5opts[Q["C01-Q5"]["correctId"]] == "D, B, E")
check("C01-Q5 the other options differ from the queue", sum(1 for v in Q5opts.values() if v.replace(" ", "") == "D,B,E") == 1)
# lesson example matches the BFS above
check("C01 lesson example d", d == {"A": 0, "C": 1, "D": 1, "B": 2, "E": 2, "F": 3, "G": 4})

# ---- C02
g, nodes, adj = nxg(gspec("C02-Q1"))
check("C02-Q1 components = 4", nx.number_connected_components(g) == 4 == step_of("C02-Q1")["answer"])
comps = 0
white = set(nodes)
while white:
    s = sorted(white)[0]
    white -= set(my_bfs(adj, s)[0])
    comps += 1
check("C02-Q1 BFS-restart count = 4", comps == 4)
g, nodes, adj = nxg(gspec("C02-Q2"))
on_sp = set()
for p in nx.all_shortest_paths(g, "P", "V"):
    on_sp |= set(p)
opts = {o["id"]: o["value"] for o in Q["C02-Q2"]["options"]}
check("C02-Q2 exactly T is on no shortest path among the options", [v for v in opts.values() if v not in on_sp] == ["T"] and opts[Q["C02-Q2"]["correctId"]] == "T")
dP, dV = nx.single_source_shortest_path_length(g, "P"), nx.single_source_shortest_path_length(g, "V")
check("C02-Q2 sums used in the explanation", (dP["Q"] + dV["Q"], dP["R"] + dV["R"], dP["S"] + dV["S"], dP["T"] + dV["T"], dP["V"]) == (3, 3, 3, 4, 3))
g, nodes, adj = nxg(gspec("C02-Q3"))
check("C02-Q3 cut vertices = {B, D, E}", sorted(nx.articulation_points(g)) == ["B", "D", "E"] and step_of("C02-Q3")["answer"] == 3)


def cut_vertex_alg(adjd, x):
    nb = adjd[x]
    if len(nb) <= 1:
        return False
    h = {v: [w for w in ws if w != x] for v, ws in adjd.items() if v != x}
    dd, _, _ = my_bfs(h, nb[0])
    return any(u not in dd for u in nb)


def rand_graph(n, p, directed=False):
    names = [chr(65 + i) for i in range(n)]
    g = nx.DiGraph() if directed else nx.Graph()
    g.add_nodes_from(names)
    for u in names:
        for v in names:
            if u != v and (directed or u < v) and random.random() < p:
                g.add_edge(u, v)
    return g


def adj_of(g):
    return {v: sorted(g.neighbors(v)) if not g.is_directed() else sorted(g.successors(v)) for v in g.nodes}


bad = 0
for _ in range(400):
    g = rand_graph(random.randint(3, 8), random.random())
    ad = adj_of(g)
    ap = set(nx.articulation_points(g)) if nx.is_connected(g) else None
    for x in g.nodes:
        base = nx.number_connected_components(g)
        h = g.copy()
        h.remove_node(x)
        more = nx.number_connected_components(h) > base
        if cut_vertex_alg(ad, x) != more:
            bad += 1
check("C02 lesson: the BFS cut-vertex recipe equals 'G-x has more components' (400 random graphs)", bad == 0, bad)
bad = 0
for _ in range(400):
    g = rand_graph(random.randint(2, 9), random.random())
    ad = adj_of(g)
    col, ok_bip = {}, True
    for s in sorted(g.nodes):
        if s in col:
            continue
        dd, _, _ = my_bfs(ad, s)
        for v, k in dd.items():
            col[v] = k % 2
    ok_bip = all(col[u] != col[v] for u, v in g.edges)
    if ok_bip != nx.is_bipartite(g):
        bad += 1
check("C02 lesson: parity-of-distance colouring decides bipartiteness (400 random graphs)", bad == 0, bad)
bad = 0
for _ in range(300):
    g = rand_graph(random.randint(3, 8), random.random())
    ad = adj_of(g)
    ns = sorted(g.nodes)
    x, y, z = random.sample(ns, 3)
    if not nx.has_path(g, x, y):
        continue
    ex = any(z in p for p in nx.all_shortest_paths(g, x, y))
    dx, dy = my_bfs(ad, x)[0], my_bfs(ad, y)[0]
    f = z in dx and dx[z] + dy[z] == dx[y]
    if ex != f:
        bad += 1
    # walk through z exists iff x and y both in z's component
    wk = nx.has_path(g, x, z) and nx.has_path(g, z, y)
    dz = my_bfs(ad, z)[0]
    if wk != (x in dz and y in dz):
        bad += 1
check("C02 lesson: shortest-through-z sum test and walk-through-z test (300 random graphs)", bad == 0, bad)

# ---- C03
g, nodes, adj = nxg(gspec("C03-Q1"))
disc, fin, pi, cls, order = my_dfs(adj, nodes, False)
check("C03-Q1 d[E]=8", disc["E"] == 8 == step_of("C03-Q1")["answer"])
check("C03-Q2 f[A]=12", fin["A"] == 12 == step_of("C03-Q2")["answer"])
k = sum(1 for v in pi if pi[v] is None)
check("C03-Q3 |E_DFS| = 5 = |V| - trees, trees = 2", len(tree_edges(pi)) == 5 == step_of("C03-Q3")["answer"] and k == 2 and len(nodes) - k == 5)
check("C03 lesson example times", disc == {"A": 1, "B": 2, "C": 3, "D": 5, "E": 8, "F": 9, "G": 13} and fin == {"C": 4, "D": 6, "B": 7, "F": 10, "E": 11, "A": 12, "G": 14})
check("C03 lesson: A tree of 6 vertices finishes its root at 12", fin["A"] == 2 * 6)
# parenthesis theorem, leaf rule, forest edge count, on random graphs of both kinds
bad = 0
for _ in range(600):
    directed = random.random() < 0.5
    g = rand_graph(random.randint(2, 9), random.random() * 0.6, directed)
    ad = adj_of(g)
    disc, fin, pi, cls, order = my_dfs(ad, sorted(g.nodes), directed)
    ns = sorted(g.nodes)
    for u, v in itertools.combinations(ns, 2):
        a, b, c, e = disc[u], fin[u], disc[v], fin[v]
        disjoint = b < c or e < a
        nested = (a < c and e < b) or (c < a and b < e)
        if disjoint == nested:
            bad += 1
    children = {v: 0 for v in ns}
    for v, p in pi.items():
        if p is not None:
            children[p] += 1
    for v in ns:
        if (children[v] == 0) != (fin[v] == disc[v] + 1):
            bad += 1
    roots = sum(1 for v in pi if pi[v] is None)
    if len(tree_edges(pi)) != len(ns) - roots:
        bad += 1
    if len(set(disc.values()) | set(fin.values())) != 2 * len(ns):
        bad += 1
    # white path theorem
    for u in ns:
        anc = set()
        for v in ns:
            x = v
            while x is not None:
                if x == u and v != u:
                    anc.add(v)
                x = pi[x]
        # a path of vertices all white at disc[u]  <=> descendant
        for v in ns:
            if v == u:
                continue
            h = nx.DiGraph() if directed else nx.Graph()
            allowed = [w for w in ns if disc[w] > disc[u] or w == u]
            h = g.subgraph(allowed)
            if (v in h and nx.has_path(h, u, v)) != (v in anc):
                bad += 1
check("C03/C04 lessons: parenthesis theorem, leaf rule f=d+1, |E_DFS|=|V|-k, 2|V| clock values, white-path theorem (600 random graphs)", bad == 0, bad)
# Q4 options
d_u, f_u, d_v, f_v = 2, 9, 4, 5
check("C03-Q4 v nested in u => v descendant (a); the other options contradict the theorem",
      d_u < d_v and f_v < f_u and not (d_v < d_u and f_u < f_v) and not (f_u < d_v or f_v < d_u))
found = False
for _ in range(20000):
    g = rand_graph(random.randint(5, 7), random.random() * 0.5)
    dsc, fn, pi, cls, order = my_dfs(adj_of(g), sorted(g.nodes), False)
    if any(dsc[u] == 2 and fn[u] == 9 and dsc[v] == 4 and fn[v] == 5 for u in g.nodes for v in g.nodes):
        found = True
        break
check("C03-Q4 such a run exists (so 'impossible' is wrong)", found)
check("C03-Q4 correct option text says v is a descendant of u", "צאצא של $u$" in {o["id"]: o["value"] for o in Q["C03-Q4"]["options"]}[Q["C03-Q4"]["correctId"]])

# ---- C04
g, nodes, adj = nxg(gspec("C04-Q1"))
disc, fin, pi, cls, order = my_dfs(adj, nodes, True)
names = {"tree": "קשת עץ", "back": "קשת אחורה", "forward": "קשת קדימה", "cross": "קשת חוצה"}


def right_option_is(qid, kind):
    st = Q[qid].get("step") or Q[qid]
    return {o["id"]: o["value"] for o in st["options"]}[st["correctId"]] == names[kind]


check("C04-Q1 C->A is a back edge", cls[("C", "A")] == "back" and right_option_is("C04-Q1", "back"))
check("C04-Q2 A->C is a forward edge", cls[("A", "C")] == "forward" and right_option_is("C04-Q2", "forward"))
check("C04 lesson example: E->D cross, the four classes all appear", cls[("E", "D")] == "cross" and set(cls.values()) == {"tree", "back", "forward", "cross"})
check("C04 lesson example times", disc == {"A": 1, "B": 2, "C": 3, "D": 6, "E": 9, "F": 10} and fin == {"C": 4, "B": 5, "D": 7, "A": 8, "F": 11, "E": 12})
# Q3: times rule, validated on random digraphs: an edge with disjoint intervals and f[v] < d[u] is always a cross edge, and conversely
bad, seen_cross = 0, 0
for _ in range(600):
    g = rand_graph(random.randint(3, 9), random.random() * 0.5, True)
    dsc, fn, pi, cls, order = my_dfs(adj_of(g), sorted(g.nodes), True)
    for (u, v), kind in cls.items():
        if u == v:
            continue
        crossish = fn[v] < dsc[u]
        if crossish != (kind == "cross"):
            bad += 1
        if kind == "cross":
            seen_cross += 1
        if kind == "back" and not (dsc[v] < dsc[u] and fn[u] < fn[v]):
            bad += 1
        if kind in ("tree", "forward") and not (dsc[u] < dsc[v] and fn[v] < fn[u]):
            bad += 1
check("C04 lesson: classification by times (cross: f[v]<d[u]; back: u inside v; tree/forward: v inside u) on 600 random digraphs", bad == 0 and seen_cross > 50, (bad, seen_cross))
found = False
for _ in range(60000):
    g = rand_graph(random.randint(5, 7), random.random() * 0.5, True)
    dsc, fn, pi, cls, order = my_dfs(adj_of(g), sorted(g.nodes), True)
    if any(k == "cross" and dsc[u] == 7 and fn[u] == 10 and dsc[v] == 2 and fn[v] == 5 for (u, v), k in cls.items()):
        found = True
        break
check("C04-Q3 a real run with a cross edge and exactly these times exists", found)
check("C04-Q3 intervals [7,10] and [2,5] are disjoint with f[v]<d[u]: cross", 5 < 7 and right_option_is("C04-Q3", "cross"))
# Q4: undirected only tree/back
bad, back_seen = 0, 0
for _ in range(600):
    g = rand_graph(random.randint(3, 9), random.random() * 0.7)
    dsc, fn, pi, cls, order = my_dfs(adj_of(g), sorted(g.nodes), False)
    if not set(cls.values()) <= {"tree", "back"}:
        bad += 1
    back_seen += sum(1 for k in cls.values() if k == "back")
    # every edge is between an ancestor and a descendant
    for u, v in g.edges:
        if not ((dsc[u] < dsc[v] and fn[v] < fn[u]) or (dsc[v] < dsc[u] and fn[u] < fn[v])):
            bad += 1
    if len(cls) != g.number_of_edges():
        bad += 1
check("C04-Q4 undirected DFS: only tree/back, each edge classified once, every edge joins ancestor and descendant (600 random graphs)", bad == 0 and back_seen > 100, (bad, back_seen))
check("C04-Q4 correct option says only tree and back", "רק צלעות עץ וצלעות אחורה" == {o["id"]: o["value"] for o in Q["C04-Q4"]["options"]}[Q["C04-Q4"]["correctId"]])
# Q5
g, nodes, adj = nxg(gspec("C04-Q5"))
disc, fin, pi, cls, order = my_dfs(adj, nodes, True)
check("C04-Q5 T->R back, P->S forward, the graph has a directed cycle R,S,T", cls[("T", "R")] == "back" and cls[("P", "S")] == "forward" and not nx.is_directed_acyclic_graph(g) and nx.has_path(g, "R", "T"))
check("C04-Q5 the 'no cycle' options are wrong: cycle exists, and there is a back edge", any(k == "back" for k in cls.values()))
# cycle <=> back edge on random digraphs
bad = 0
for _ in range(600):
    g = rand_graph(random.randint(2, 8), random.random() * 0.5, True)
    dsc, fn, pi, cls, order = my_dfs(adj_of(g), sorted(g.nodes), True)
    if nx.is_directed_acyclic_graph(g) == any(k == "back" for k in cls.values()):
        bad += 1
check("C04/C05 lessons: directed cycle iff a back edge (600 random digraphs)", bad == 0, bad)
# Q6
g, nodes, adj = nxg(gspec("C04-Q6"))
disc, fin, pi, cls, order = my_dfs(adj, nodes, True)


def descendants(pi, u):
    out = set()
    for v in pi:
        x = pi[v]
        while x is not None:
            if x == u:
                out.add(v)
            x = pi[x]
    return out


desc_A = descendants(pi, "A")
check("C04-Q6 descendants of A = {B,C,D} = vertices reachable from A; E,F are not", desc_A == {"B", "C", "D"} == nx.descendants(g, "A") and {"E", "F"} == set(nodes) - desc_A - {"A"})

# ---- C05
g, nodes, adj = nxg(gspec("C05-Q1"))
disc, fin, pi, cls, order = my_dfs(adj, nodes, True)
topo = sorted(nodes, key=lambda v: -fin[v])
check("C05-Q1 topo by decreasing finish time", topo == "F A D E B C".split() and "F, A, D, E, B, C" in step_of("C05-Q1")["accept"])
check("C05 lesson: finish times", fin == {"C": 4, "B": 5, "E": 8, "D": 9, "A": 10, "F": 12})
check("C05-Q3 f[D] = 9", fin["D"] == 9 == step_of("C05-Q3")["answer"])


def is_topo(order_, g):
    pos = {v: i for i, v in enumerate(order_)}
    return len(pos) == g.number_of_nodes() and all(pos[u] < pos[v] for u, v in g.edges)


Q2o = {o["id"]: [x.strip() for x in o["value"].split(",")] for o in Q["C05-Q2"]["options"]}
valid = [k for k, o in Q2o.items() if is_topo(o, g)]
check("C05-Q2 exactly one option is a valid topological order, and it is the stored one", valid == [Q["C05-Q2"]["correctId"]], valid)
check("C05 lesson: topological sort via finish times is valid on random DAGs",
      all(is_topo(sorted(h.nodes, key=lambda v: -my_dfs(adj_of(h), sorted(h.nodes), True)[1][v]), h)
          for h in [nx.relabel_nodes(nx.gnp_random_graph(random.randint(2, 9), 0.4, directed=True), lambda i: chr(65 + i)) for _ in range(300)]
          if nx.is_directed_acyclic_graph(h)))
g4, _, _ = nxg(gspec("C05-Q4"))
cnt = len(list(nx.all_topological_sorts(g4)))
check("C05-Q4 number of topological orders = 8", cnt == 8 == step_of("C05-Q4")["answer"], cnt)
Q5o = {o["id"]: o["value"].replace("$", "").replace("\\to", ">").strip() for o in Q["C05-Q5"]["options"]}
cyc = []
for k, t in Q5o.items():
    a, b = t.split(">")
    h = g.copy()
    h.add_edge(a.strip(), b.strip())
    if not nx.is_directed_acyclic_graph(h):
        cyc.append(k)
check("C05-Q5 exactly one added edge makes a cycle, and it is the stored answer", cyc == [Q["C05-Q5"]["correctId"]] and Q5o[cyc[0]].startswith("C"), (cyc, Q5o))

# ---- C06
Q1o = {o["id"]: o["value"] for o in Q["C06-Q1"]["options"]}
cands = {
    "a": nx.Graph([(1, 2), (3, 4)]),
    "b": nx.path_graph([1, 2, 3, 4]),
    "c": None,
    "d": nx.star_graph(3),
}
tri = nx.Graph([(1, 2), (2, 3), (1, 3)])
tri.add_node(4)
cands["c"] = tri
is_ce = {k: all(dg >= 1 for _, dg in h.degree()) and not nx.is_connected(h) for k, h in cands.items()}
check("C06-Q1 only the two disjoint edges are a counterexample to 'min degree >= 1 => connected'", [k for k, v in is_ce.items() if v] == ["a"] == [Q["C06-Q1"]["correctId"]], is_ce)
check("C06 lesson example: triangle + isolated vertex has |E|=|V|-1 and is not a tree", tri.number_of_edges() == tri.number_of_nodes() - 1 and not nx.is_tree(tri))
# the claim of Q2/Q3 on every graph with <= 6 vertices (all of them), BFS from every vertex, several neighbour orders
bad, runs = 0, 0
for n in range(2, 7):
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        if n == 6 and mask % 7:   # thin out the 32768 graphs of n = 6
            continue
        es = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(es)
        if not nx.is_connected(g):
            continue
        for s in range(n):
            ad = {v: sorted(g.neighbors(v)) for v in g.nodes}
            for _ in range(2):
                for v in ad:
                    random.shuffle(ad[v])
                dd, _, _ = my_bfs(ad, s)
                runs += 1
                if any(abs(dd[u] - dd[v]) > 1 for u, v in es):
                    bad += 1
check("C06-Q2/Q3 undirected BFS: |d[u]-d[v]|<=1 on every edge (all connected graphs up to 5 vertices, a sample of 6)", bad == 0 and runs > 20000, (bad, runs))
# dequeue order has non-decreasing d (used by the proof lines)
bad = 0
for _ in range(500):
    g = rand_graph(random.randint(3, 9), random.random() * 0.6)
    ad = adj_of(g)
    s = sorted(g.nodes)[0]
    dd, _, order = my_bfs(ad, s)
    if any(dd[order[i]] > dd[order[i + 1]] for i in range(len(order) - 1)):
        bad += 1
check("C06-Q3 BFS discovers/dequeues vertices in non-decreasing d (the fact the proof uses)", bad == 0)
st3 = step_of("C06-Q3")
check("C06-Q3 findbug: index 3 has the flipped inequality, the other four lines carry no >= claim", st3["bugIndex"] == 3 and "\\ge d[u]" in st3["lines"][3] and all("\\ge d[" not in l for i, l in enumerate(st3["lines"]) if i != 3))
check("C06-Q2 the stored verdict is 'true' (option a), matching the brute force", step_of("C06-Q2")["correctId"] == "a")
# Q4: directed
Q4o = {o["id"]: o["value"] for o in Q["C06-Q4"]["options"]}
holds = {"a": lambda du, dv: dv <= du + 1, "b": lambda du, dv: abs(du - dv) <= 1, "c": lambda du, dv: dv == du + 1, "d": lambda du, dv: dv >= du}
always = {k: True for k in holds}
for n in range(2, 5):
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v]
    for mask in range(1 << len(pairs)):
        es = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        ad = {v: sorted(w for u, w in es if u == v) for v in range(n)}
        dd, _, _ = my_bfs(ad, 0)
        for u, v in es:
            if u in dd:
                for k, f in holds.items():
                    if not f(dd[u], dd[v]):
                        always[k] = False
check("C06-Q4 directed BFS: only d[v]<=d[u]+1 holds on every edge with u reachable (all digraphs up to 4 vertices)", [k for k, v in always.items() if v] == ["a"] == [Q["C06-Q4"]["correctId"]], always)
dd, _, _ = my_bfs({"s": ["a"], "a": ["b"], "b": ["c"], "c": ["a"]}, "s")
check("C06-Q4 the explanation's example: d[a]=1, d[c]=3", dd["a"] == 1 and dd["c"] == 3)

# ---- C07
g, nodes, adj = nxg(gspec("C07-Q1"))
d, pi, order = my_bfs(adj, "A")
check("C07-Q1 BFS height 2", max(d.values()) == 2 == step_of("C07-Q1")["answer"])
disc, fin, pi2, cls, order2 = my_dfs(adj, nodes, False)
check("C07-Q2 DFS height 4 (chain A,B,E,F,D), C hangs below E at depth 3", max(depth_of(pi2).values()) == 4 == step_of("C07-Q2")["answer"] and pi2["C"] == "E" and depth_of(pi2)["C"] == 3 and order2 == "A B E C F D".split())
check("C07 lesson: BFS d table", d == {"A": 0, "B": 1, "C": 1, "D": 1, "E": 2, "F": 2})
# DFS height >= BFS height; BFS levels differ by <=1 across non-tree edges; DFS non-tree edges skip >= 2 depth
bad = 0
for _ in range(500):
    g = rand_graph(random.randint(3, 9), random.random() * 0.6)
    if not nx.is_connected(g):
        continue
    ad = adj_of(g)
    s = sorted(g.nodes)[0]
    dB, pB, _ = my_bfs(ad, s)
    dsc, fn, pD, cls, _ = my_dfs(ad, [s], False)
    if max(depth_of(pD).values()) < max(dB.values()):
        bad += 1
    dep = depth_of(pD)
    te = tree_edges(pD)
    for u, v in g.edges:
        if frozenset((u, v)) not in te and abs(dep[u] - dep[v]) < 2:
            bad += 1
check("C07 lesson: DFS height >= BFS height; DFS non-tree edges join depths differing by >= 2 (500 random graphs)", bad == 0, bad)


# Q3: can T_BFS = T_DFS?  all connected graphs up to 5 vertices, every start, many neighbour orders
def all_orders_trees(g, s, limit):
    ns = list(g.nodes)
    base = {v: sorted(g.neighbors(v)) for v in ns}
    perms = [list(itertools.permutations(base[v])) for v in ns]
    total = 1
    for p in perms:
        total *= len(p)
    if total <= limit:
        combos = itertools.product(*perms)
    else:
        combos = ([random.choice(p) for p in perms] for _ in range(limit))
    bt, dt = set(), set()
    for c in combos:
        ad = {v: list(c[i]) for i, v in enumerate(ns)}
        bt.add(frozenset(tree_edges(my_bfs(ad, s)[1])))
        dt.add(frozenset(tree_edges(my_dfs(ad, [s], False)[2])))
    return bt, dt


bad, ntrees, ncyc = 0, 0, 0
for n in range(2, 6):
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        es = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(es)
        if not nx.is_connected(g):
            continue
        if n == 5 and mask % 3:
            continue
        for s in range(n):
            bt, dt = all_orders_trees(g, s, 300)
            same = bool(bt & dt)
            if same != nx.is_tree(g):
                bad += 1
            ntrees += nx.is_tree(g)
            ncyc += not nx.is_tree(g)
check("C07-Q3 / lesson rule: T_BFS = T_DFS is possible exactly when G is a tree (connected graphs up to 5 vertices, every start, up to 300 neighbour orders)", bad == 0 and ntrees > 20 and ncyc > 300, (bad, ntrees, ncyc))
for name, h, s in (("unicyclic, s off the cycle", nx.Graph([(0, 1), (1, 2), (2, 0), (2, 3), (3, 4)]), 4), ("C4 (bipartite)", nx.cycle_graph(4), 0), ("cycle with s of degree 1", nx.Graph([(0, 1), (1, 2), (2, 3), (3, 1)]), 0)):
    bt, dt = all_orders_trees(h, s, 2000)
    check("C07-Q3 distractor fails: " + name, not (bt & dt))
check("C07-Q3 correct option says G is a tree", "עץ" in {o["id"]: o["value"] for o in Q["C07-Q3"]["options"]}[Q["C07-Q3"]["correctId"]])
# Q4: directed, s a root
bad, n_root = 0, 0
for n in range(2, 5):
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v]
    for mask in range(1 << len(pairs)):
        es = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        ad = {v: sorted(w for u, w in es if u == v) for v in range(n)}
        dd, pB, _ = my_bfs(ad, 0)
        if len(dd) != n:
            continue
        n_root += 1
        pD = my_dfs(ad, [0] + [v for v in range(n)], True)[2]
        if len({(p, v) for v, p in pB.items() if p is not None}) != n - 1:
            bad += 1
        if len({(p, v) for v, p in pD.items() if p is not None}) != n - 1:
            bad += 1
check("C07-Q4 s a root: |E_BFS| = |E_DFS| = |V|-1 (all digraphs up to 4 vertices with root 0)", bad == 0 and n_root > 300, (bad, n_root))
check("C07-Q4 stored option is the 'both |V|-1' one", "$|V|-1$" in {o["id"]: o["value"] for o in Q["C07-Q4"]["options"]}[Q["C07-Q4"]["correctId"]])
# lesson trap of C07: E_DFS = E_BFS while s is not a root (the exam's counterexample)
ad = {"s": ["a"], "a": [], "b": ["s"]}
dd, pB, _ = my_bfs(ad, "s")
pD = my_dfs(ad, ["s", "a", "b"], True)[2]
check("C07 lesson trap: V={s,a,b}, E={(s,a),(b,s)} gives E_BFS = E_DFS = {(s,a)} though b is unreachable",
      {(p, v) for v, p in pB.items() if p} == {(p, v) for v, p in pD.items() if p} == {("s", "a")} and "b" not in dd)

# ---------------------------------------------------------------------------------------------- 3. lesson numbers in prose
# C06 lesson: |E_BFS(G,v)| = n_v - 1 and E_DFS = sum (n_i - 1), from any start (undirected)
bad = 0
for _ in range(400):
    g = rand_graph(random.randint(3, 9), random.random() * 0.4)
    ad = adj_of(g)
    comps = [len(c) for c in nx.connected_components(g)]
    for s in g.nodes:
        dd, pB, _ = my_bfs(ad, s)
        nB = len([1 for p in pB.values() if p is not None])
        nv = len(nx.node_connected_component(g, s))
        if nB != nv - 1:
            bad += 1
        order_ = [s] + [v for v in sorted(g.nodes) if v != s]
        pD = my_dfs(ad, order_, False)[2]
        if len(tree_edges(pD)) != sum(c - 1 for c in comps):
            bad += 1
check("C06/C08 lessons: |E_BFS(G,v)| = n_v - 1 and |E_DFS(G)| = sum(n_i - 1) from any start (400 random graphs)", bad == 0, bad)

# ---------------------------------------------------------------------------------------------- 4. structure
allq = [(lv["id"], q) for lv in LEVELS for q in lv["questions"]]
nown = sum(1 for _, q in allq if "id" in q)
nbank = sum(1 for _, q in allq if "bankId" in q)
print("questions: own %d, bank pulls %d" % (nown, nbank))
per = {lv["id"]: len(lv["questions"]) for lv in LEVELS}
check("4-6 questions per level (boss 6)", all(4 <= n <= 6 for n in per.values()), per)
for lid, q in allq:
    if "bankId" in q:
        b = BANK.get(q["bankId"])
        check("bank id %s exists in the bank" % q["bankId"], b is not None)
        if b:
            check("bank id %s has verified steps and is not held" % q["bankId"], b.get("stepsSource") == "ai-verified" and not b.get("hold"), b.get("stepsSource"))
boss = LEVELS[-1]
check("boss: all questions are real exam questions", all("bankId" in q for q in boss["questions"]))
bank_ids = [q["bankId"] for _, q in allq if "bankId" in q]
check("no bank question is pulled twice", len(bank_ids) == len(set(bank_ids)), bank_ids)
check("no 2026A pull (privacy)", not any(b.startswith("26A") for b in bank_ids))
POSITION = re.compile(r"(האפשרות|התשובה|אופציה|סעיף)\s+(הראשונ|השני|השלישי|הרביעי|[א-ד]\b)|\(א\)|\(ב\)|\(ג\)|\(ד\)|\boption\s+[a-d]\b", re.I)
bad = []


def walk(x, path):
    if isinstance(x, str):
        if POSITION.search(x):
            bad.append(path)
    elif isinstance(x, dict):
        for k, v in x.items():
            walk(v, path + "." + str(k))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            walk(v, "%s[%d]" % (path, i))


for lv in LEVELS:
    walk(lv, lv["id"])
check("no option or part cited by position in any lesson, question, explanation or recap", not bad, bad)
for lid, q in allq:
    if "id" in q and "step" not in q:
        o = q["options"]
        check(q["id"] + " correctId is an option and ids unique", q["correctId"] in [x["id"] for x in o] and len({x["id"] for x in o}) == len(o))
        check(q["id"] + " has an explanation and a recap", bool(q.get("explanation")) and bool(q.get("recap")))
    elif "step" in q:
        check(q["id"] + " step has explain and recap", bool(q["step"].get("explain")) and bool(q.get("recap")))
check("every level is ai-verified only because this script passes", all(lv["source"] == "ai-verified" for lv in LEVELS))

print("%d checks" % nchecks)
print("ALL OK" if ok else "FAILURES ABOVE")
sys.exit(0 if ok else 1)
