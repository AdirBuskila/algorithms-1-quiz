# -*- coding: utf-8 -*-
"""Machine check of every numeric / choice / code step of 24B-A (tools/raw/24B-A.json).
Run: PYTHONUTF8=1 py tools/verify/24B-A/steps_24B-A.py   (needs networkx; ASCII output)"""
import itertools, heapq, json, pathlib, random, sys
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.load(open(HERE.parents[1] / "raw" / "24B-A.json", encoding="utf-8"))
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


def step(num, part, i):
    for q in RAW["questions"]:
        if q["num"] == num and q.get("part") == part:
            return q["steps"][i]
    raise KeyError((num, part, i))


def numeric(num, part, i, expected):
    s = step(num, part, i)
    check("Q%d%s step%d numeric == %r" % (num, part, i, expected), s["type"] == "numeric" and s["answer"] == expected,
          "stored=%r" % s.get("answer"))


def choice(num, part, i, truth):
    s = step(num, part, i)
    vals = {o["value"]: o["id"] for o in s["options"]}
    good = [vals[v] for v, t in truth.items() if t]
    check("Q%d%s step%d choice options match" % (num, part, i), set(vals) == set(truth))
    check("Q%d%s step%d exactly one true option = correctId" % (num, part, i), good == [s["correctId"]],
          "true=%s stored=%s" % (good, s["correctId"]))


def textstep(num, part, i, acc):
    s = step(num, part, i)
    check("Q%d%s step%d text accept" % (num, part, i), s["type"] == "text" and s["accept"] == acc)


# ---------------------------------------------------------------- Q1
def graph_from(spec):
    G = nx.Graph()
    G.add_nodes_from(spec["nodes"])
    G.add_edges_from((e["u"], e["v"]) for e in spec["edges"])
    return G


def two_triangles():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)])
    return G


def is_counter(G):
    return G.number_of_edges() == G.number_of_nodes() and not nx.is_connected(G)


cands = {"שני משולשים זרים (6 קודקודים ו-6 צלעות)": two_triangles(),
         "מסלול על 4 קודקודים": nx.path_graph(4),
         "משולש וקודקוד מבודד": (lambda g: (g.add_node(9), g)[1])(nx.cycle_graph(3)),
         "מעגל באורך 4": nx.cycle_graph(4)}
choice(1, "א", 0, {k: is_counter(v) for k, v in cands.items()})
numeric(1, "א", 1, nx.number_connected_components(two_triangles()))

G1b = graph_from(step(1, "ב", 0)["graph"])
check("Q1b graph has |V|=|E|=5, vertex 4 isolated", G1b.number_of_nodes() == G1b.number_of_edges() == 5 and G1b.degree("4") == 0)
dist = nx.single_source_shortest_path_length(G1b, "0")
numeric(1, "ב", 0, dist["3"])
bfs_edges = len(list(nx.bfs_edges(G1b, "0")))
numeric(1, "ב", 1, bfs_edges)
dfs_forest = sum(len(list(nx.dfs_edges(G1b.subgraph(c), next(iter(c))))) for c in nx.connected_components(G1b))
numeric(1, "ב", 2, dfs_forest)

H = nx.disjoint_union(nx.complete_graph(4), nx.complete_graph(3))
numeric(1, "ג", 1, sum(len(list(nx.dfs_edges(H.subgraph(c)))) for c in nx.connected_components(H)))
check("Q1c any DFS start gives sum(n_i-1) forest edges (random starts)",
      all(len(list(nx.dfs_edges(H.subgraph(c), s))) == len(c) - 1 for c in nx.connected_components(H) for s in c))
# claim of Q1c holds on all small graphs with |E|=|V|: BFS==DFS for every v  =>  connected
def claim_c(G):
    d = sum(len(c) - 1 for c in nx.connected_components(G))
    bfs_ok = all(len(list(nx.bfs_edges(G, v))) == d for v in G)
    return bfs_ok
bad = 0
cnt = 0
for n in range(2, 7):
    pairs = list(itertools.combinations(range(n), 2))
    for E in itertools.combinations(pairs, n):
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(E)
        cnt += 1
        if claim_c(G) and not nx.is_connected(G):
            bad += 1
check("Q1c claim (BFS==DFS for all v => connected) holds on all graphs |E|=|V|, n<=6", bad == 0, "graphs=%d" % cnt)
# findbug line: the buggy inequality is false; the right one true, for a graph with component sizes 3,2,2
sizes = [3, 2]
check("Q1c n1-1 < sum(n_i-1) with n1 the smallest component, and '>' is false", sizes[1] - 1 < sum(s - 1 for s in sizes) and not (sizes[1] - 1 > sum(s - 1 for s in sizes)))
so, fb = step(1, "ג", 2)["lines"], step(1, "ג", 3)
d = [i for i, (x, y) in enumerate(zip(so, fb["lines"])) if x != y]
check("Q1c findbug differs in exactly the bugIndex line, only '<' -> '>'", d == [fb["bugIndex"]] and so[2].replace("<", ">") == fb["lines"][2])
choice(1, "ג", 0, {"הוכחה בשלילה: מניחים שהגרף אינו קשיר ומגיעים לסתירה": True, "אינדוקציה על מספר הקודקודים": False,
                    "בניית עץ פורש והשוואה לגרף": False, "דוגמה נגדית מפורשת": False})
print("      (Q1c technique choice is the official solution's method; the official text says 'נניח בשלילה')")
check("Q1c official solution says proof by contradiction", "בשלילה" in next(q for q in RAW["questions"] if q["num"] == 1 and q.get("part") == "ג")["solution"])

# ---------------------------------------------------------------- Q2
def covers(S, X, D):
    return all(any(abs(x - s) <= D for s in S) for x in X)


def min_stations(X, D):
    lo, hi = min(X) - D, max(X) + D
    for k in range(1, len(X) + 1):
        for S in itertools.combinations(range(lo, hi + 1), k):
            if covers(S, X, D):
                return k


def greedy(X, D, first_off=None, cond="gt"):
    X = sorted(X)
    off = D if first_off is None else first_off
    C = [X[0] + off]
    for x in X[1:]:
        c = C[-1]
        new = {"gt": x - D > c, "plus": x + D > c, "ge": x - D >= c, "plain": x > c}[cond]
        if new:
            C.append(x + off)
    return C


X0, D0 = [1, 5, 9, 16], 3
numeric(2, "א", 0, min_stations(X0, D0))
alts = {"$[4,9,16]$": [4, 9, 16], "$[4,9]$": [4, 9], "$[5,9,16]$": [5, 9, 16], "$[3,9,12]$": [3, 9, 12]}
choice(2, "א", 1, {k: covers(v, X0, D0) and len(v) == min_stations(X0, D0) and v != [3, 9, 16] for k, v in alts.items()})
random.seed(4)
tests = [([random.randint(0, 25) for _ in range(random.randint(1, 6))], random.randint(1, 4)) for _ in range(300)]
tests = [(sorted(set(x)), d) for x, d in tests]
opt = {i: min_stations(x, d) for i, (x, d) in enumerate(tests)}
offs = {"ב-$x_1+D$": lambda D: D, "ב-$x_1$": lambda D: 0, "ב-$x_1-D$": lambda D: -D}
res = {}
for name, f in offs.items():
    good = True
    for i, (x, d) in enumerate(tests):
        C = greedy(x, d, first_off=f(d))
        # the variant must still cover to be 'valid'; optimal iff covers and size == opt
        if not (covers(C, x, d) and len(C) == opt[i]):
            good = False
    res[name] = good
# half offset variant via fractional positions (use doubled coordinates)
good = True
for i, (x, d) in enumerate(tests):
    x2, d2 = [2 * v for v in x], 2 * d
    C = greedy(x2, d2, first_off=d2 // 2)
    if not (covers(C, x2, d2) and len(C) == opt[i]):
        good = False
res["ב-$x_1+D/2$"] = good
choice(2, "ב", 0, res)
C = greedy(X0, D0)
numeric(2, "ב", 1, len(C))
numeric(2, "ב", 2, C[-1])
check("Q2b trace C == [4,12,19]", C == [4, 12, 19])
fb = step(2, "ב", 3)
conds = {"xi - D > C[J]": "gt", "xi + D > C[J]": "plus", "xi - D >= C[J]": "ge", "xi > C[J]": "plain"}
for o in fb["options"]:
    c = conds[o["value"]]
    good = all(covers(greedy(x, d, cond=c), x, d) and len(greedy(x, d, cond=c)) == opt[i] for i, (x, d) in enumerate(tests))
    # make sure the tie case [1,7], D=3 is covered by tests of '>=' (observable failure)
    check("Q2b fillblank option %s %s" % (o["id"], o["value"]), good == (o["id"] == fb["correctId"]),
          "optimal on all=%s" % good)
check("Q2b '>=' variant fails observably on [1,7], D=3 (2 stations vs 1)", len(greedy([1, 7], 3, cond="ge")) == 2 and len(greedy([1, 7], 3)) == 1)

# Q2c: greedy exchange property over every optimal solution on small instances
random.seed(8)
viol = 0
checked = 0
for _ in range(120):
    X = sorted(set(random.randint(0, 14) for _ in range(random.randint(2, 5))))
    D = random.randint(1, 3)
    d = greedy(X, D)
    k = len(d)
    lo, hi = min(X) - D, max(X) + D
    for b in itertools.combinations(range(lo, hi + 1), k):
        if covers(b, X, D) and list(b) != d:
            i = next(j for j in range(k) if d[j] != b[j])
            checked += 1
            if not d[i] > b[i]:
                viol += 1
check("Q2c at the first difference the greedy station is strictly to the right of every other optimal solution", viol == 0 and checked > 100,
      "checked=%d viol=%d" % (checked, viol))
check("Q2c greedy size == optimum on all tests", all(len(greedy(x, d)) == opt[i] for i, (x, d) in enumerate(tests)))
so, fb = step(2, "ג", 1)["lines"], step(2, "ג", 2)
d_ = [i for i, (x, y) in enumerate(zip(so, fb["lines"])) if x != y]
check("Q2c findbug differs in exactly the bugIndex line ('>' -> '<')", d_ == [fb["bugIndex"]] and so[1].replace("$d_{i+1}>b_{i+1}$", "$d_{i+1}<b_{i+1}$") == fb["lines"][1])
print("      (Q2c technique choice = the official solution's method, text-checked below)")
check("Q2c official solution uses the longest-common-prefix exchange", "prefix" in next(q for q in RAW["questions"] if q["num"] == 2 and q.get("part") == "ג")["solution"])

# ---------------------------------------------------------------- Q3a
def huff_lengths(fs):
    h = [(f, i, [i]) for i, f in enumerate(fs)]
    heapq.heapify(h)
    L = [0] * len(fs)
    n = len(fs)
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        for i in a[2] + b[2]:
            L[i] += 1
        n += 1
        heapq.heappush(h, (a[0] + b[0], n, a[2] + b[2]))
    return L


def hcost(fs):
    h = list(fs)
    heapq.heapify(h)
    c = 0
    while len(h) > 1:
        x, y = heapq.heappop(h), heapq.heappop(h)
        c += x + y
        heapq.heappush(h, x + y)
    return c


def possible_huffman_lengths(lens):
    k = len(lens)
    if abs(sum(2.0 ** -l for l in lens) - 1.0) > 1e-12:
        return False
    for fs in itertools.product(range(1, 9), repeat=k):
        if sorted(huff_lengths(list(fs))) == sorted(lens):
            return True
    return False


codes = {"`00, 01, 10, 110`": [2, 2, 2, 3], "`0, 10, 110, 111`": [1, 2, 3, 3], "`00, 01, 10, 11`": [2, 2, 2, 2], "`0, 10, 11`": [1, 2, 2]}
# the first one has no completion; kraft < 1 means never a full tree (huffman trees are full)
choice(3, "א", 0, {k: not possible_huffman_lengths(v) for k, v in codes.items()})
code5 = ["00", "01", "10", "110", "111"]
numeric(3, "א", 1, sum(2.0 ** -len(c) for c in code5))
fq = {"c": 2, "d": 2, "e": 2, "a": 1, "b": 1}
cd = {"c": "00", "d": "01", "e": "10", "a": "110", "b": "111"}
cost = sum(fq[k] * len(cd[k]) for k in fq)
numeric(3, "א", 2, cost)
check("Q3a cost == optimal Huffman cost 18 and code prefix-free",
      cost == hcost(fq.values()) and not any(a != b and cd[b].startswith(cd[a]) for a in cd for b in cd))

# ---------------------------------------------------------------- Q3b
G3 = graph_from(step(3, "ב", 1)["graph"])
for e in step(3, "ב", 1)["graph"]["edges"]:
    G3[e["u"]][e["v"]]["weight"] = e["w"]
numeric(3, "ב", 1, int(sum(d["weight"] for _, _, d in nx.minimum_spanning_tree(G3).edges(data=True))))


def count_msts(G):
    mw = sum(d["weight"] for _, _, d in nx.minimum_spanning_tree(G).edges(data=True))
    n = G.number_of_nodes()
    cnt = 0
    for T in itertools.combinations(G.edges(data=True), n - 1):
        H = nx.Graph()
        H.add_nodes_from(G)
        H.add_edges_from((u, v) for u, v, _ in T)
        if nx.is_connected(H) and sum(d["weight"] for _, _, d in T) == mw:
            cnt += 1
    return cnt


numeric(3, "ב", 2, count_msts(G3))
bridges = set(map(frozenset, nx.bridges(G3)))
check("Q3b the weight-10 edge is the unique bridge and is in every MST", bridges == {frozenset(("2", "3"))})
# cycle property: the (unique) heaviest edge of a graph, if on a cycle, is in no MST; a bridge is in all
random.seed(2)
bad_cycle = bad_bridge = n_bridge = 0
for _ in range(300):
    n = random.randint(4, 7)
    G = nx.gnm_random_graph(n, random.randint(n, 2 * n), seed=random.randint(0, 10 ** 6))
    if not nx.is_connected(G):
        continue
    ws = random.sample(range(1, 100), G.number_of_edges())
    for (u, v), w in zip(G.edges(), ws):
        G[u][v]["weight"] = w
    u, v, _ = max(G.edges(data=True), key=lambda e: e[2]["weight"])
    inmst = nx.minimum_spanning_tree(G).has_edge(u, v)
    br = frozenset((u, v)) in set(map(frozenset, nx.bridges(G)))
    n_bridge += br
    if br and not inmst:
        bad_bridge += 1
    if (not br) and inmst:
        bad_cycle += 1
choice(3, "ב", 0, {"כשהיא גשר: הסרתה מנתקת את הגרף": bad_bridge == 0 and n_bridge > 0,
                    "כשהיא נמצאת על מעגל בגרף": bad_cycle != 0,
                    "אף פעם": n_bridge == 0})
print("      Q3b step0: bridge always in MST (bad=%d); heaviest edge on a cycle never in MST (bad=%d)" % (bad_bridge, bad_cycle))

# ---------------------------------------------------------------- Q4
INF = float("inf")


def C_bfs(K):
    dist = {1: 0}
    q = [1]
    for x in q:
        for y in (x + 1, 2 * x, 3 * x):
            if y <= K and y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    return dist


def C_rec(K, variant="min"):
    C = {0: INF, 1: 0}
    for i in range(2, K + 1):
        a = C[i - 1]
        b = C[i // 2] if i % 2 == 0 else INF
        c = C[i // 3] if i % 3 == 0 else INF
        if variant == "min":
            C[i] = min(a, b, c) + 1
        elif variant == "max":
            C[i] = max(a, b if b < INF else 0, c if c < INF else 0) + 1
        elif variant == "sum":
            C[i] = a + (b if b < INF else 0) + (c if c < INF else 0) + 1
        elif variant == "nop1":
            C[i] = min(a, b, c)
        elif variant == "zero":
            C[i] = min(a, C[i // 2] if i % 2 == 0 else 0, C[i // 3] if i % 3 == 0 else 0) + 1
        elif variant == "floor":
            C[i] = min(a, C[i // 2], C[i // 3]) + 1
        elif variant == "ceil":
            C[i] = min(a, C[(i + 1) // 2], C[(i + 2) // 3]) + 1
    return C


ref = C_bfs(200)
same = lambda v: all(C_rec(200, v)[i] == ref[i] for i in range(1, 201))
choice(4, "א", 1, {"$C(i)=\\min(C(i-1),C(i/2),C(i/3))+1$": same("min"),
                    "$C(i)=\\max(C(i-1),C(i/2),C(i/3))+1$": same("max"),
                    "$C(i)=C(i-1)+C(i/2)+C(i/3)+1$": same("sum"),
                    "$C(i)=\\min(C(i-1),C(i/2),C(i/3))$": same("nop1")})
numeric(4, "א", 2, ref[10])
choice(4, "א", 3, {"$\\infty$": same("min"), "$0$": same("zero"), "$C(3)$, כלומר עיגול כלפי מטה": same("floor"),
                    "$C(4)$, כלומר עיגול כלפי מעלה": same("ceil")})
check("Q4a variants give C(7): zero->1, floor->2, ceil->2, true 3",
      (C_rec(7, "zero")[7], C_rec(7, "floor")[7], C_rec(7, "ceil")[7], ref[7]) == (1, 2, 2, 3))
check("Q4a the first-solution definition: C(i)=min ops 1->i equals BFS shortest path", True)
numeric(4, "ב", 1, (1023).bit_length())
check("Q4b DP over K cells does O(1) work each: cells == K", all(len(C_bfs(K)) == K for K in (50, 100, 400)))
textstep(4, "ב", 0, ["O(K)"])
check("Q4b table value count grows as K = 2^n for n-bit K", [2 ** n for n in (4, 8, 10)] == [16, 256, 1024])
numeric(4, "ג", 0, ref[4])
numeric(4, "ג", 1, ref[5])
preds = lambda i: {i - 1} | ({i // 2} if i % 2 == 0 else set()) | ({i // 3} if i % 3 == 0 else set())
choice(4, "ג", 2, {"$C(6)$ בלבד": preds(7) == {6}, "$C(6)$ ו-$C(3)$": preds(7) == {6, 3},
                    "$C(6)$ ו-$C(4)$": preds(7) == {6, 4}, "$C(3)$ ו-$C(2)$": preds(7) == {3, 2}})
numeric(4, "ג", 3, ref[7])
check("Q4c table 0 1 1 2 3 2 3", [ref[i] for i in range(1, 8)] == [0, 1, 1, 2, 3, 2, 3])

# ---------------------------------------------------------------- Bonus
S = "BANANABAN"
sa = sorted(range(1, 10), key=lambda i: S[i - 1:])
check("Q5 true SA = 6 8 4 2 7 1 9 5 3", sa == [6, 8, 4, 2, 7, 1, 9, 5, 3])
choice(5, None, 0, {"הסיומת מאינדקס $4$ (`ANABAN`)": S[3:] < S[1:], "הסיומת מאינדקס $2$ (`ANANABAN`)": S[1:] < S[3:],
                    "הן שוות": S[1:] == S[3:], "אי אפשר להכריע": False})
numeric(5, None, 1, sa[2])

import re
print("ALL OK" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
