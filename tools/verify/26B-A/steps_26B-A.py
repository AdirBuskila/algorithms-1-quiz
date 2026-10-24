# -*- coding: utf-8 -*-
"""Machine check of every numeric / choice / complexity / trace step of 26B-A (tools/raw/26B-A.json).
Run: PYTHONUTF8=1 py tools/verify/26B-A/steps_26B-A.py   (needs networkx; ASCII output)
Choice steps are checked by option position in the stored raw file: the truth of every option is computed and the
list of true options must be exactly [correctId]. Ties (Huffman, Prim) are arbitrary: validity is checked, never one
sequence."""
import itertools, json, math, pathlib, random
from collections import deque
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.load(open(HERE.parents[1] / "raw" / "26B-A.json", encoding="utf-8"))
GR = json.load(open(HERE / "graphs.json"))
ok = True
PA, PB, PC, PD, PE, PF = "א", "ב", "ג", "ד", "ה", "ו"   # item parts a..f


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
    check("Q%d%s s%d numeric == %r" % (num, part, i, expected), s["type"] == "numeric" and s["answer"] == expected,
          "stored=%r" % s.get("answer"))


def choice2(num, part, i, correct_ok, wrong_oks):
    """correct_ok: computed truth of the correct option; wrong_oks: computed truths of the wrong options in the
    order written in the generator (all must be False). The correct one sits at the index of correctId."""
    s = step(num, part, i)
    pos = ord(s["correctId"]) - ord("a")
    truth = list(wrong_oks)
    truth.insert(pos, correct_ok)
    assert len(truth) == len(s["options"])
    good = [s["options"][k]["id"] for k, t in enumerate(truth) if t]
    check("Q%d%s s%d choice: exactly one true option == correctId" % (num, part, i), good == [s["correctId"]],
          "true=%s stored=%s" % (good, s["correctId"]))


def textstep(num, part, i, accept_subset):
    s = step(num, part, i)
    check("Q%d%s s%d text accepts %s" % (num, part, i, accept_subset),
          s["type"] == "text" and all(a in s["accept"] for a in accept_subset))


# ================================================================ Q1: task selection DP
def table(tasks, T):
    n = len(tasks)
    P = [[0] * (T + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        t, v = tasks[i - 1]
        for c in range(T + 1):
            P[i][c] = P[i - 1][c] if t > c else max(P[i - 1][c], v + P[i - 1][c - t])
    return P


def table_bug(tasks, T):
    n = len(tasks)
    P = [[0] * (T + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        t, v = tasks[i - 1]
        for c in range(T + 1):
            P[i][c] = P[i - 1][c] if t > c else max(P[i - 1][c], v + P[i][c - t])
    return P


def brute(tasks, T):
    best, arg = 0, ()
    for r in range(len(tasks) + 1):
        for s in itertools.combinations(range(len(tasks)), r):
            if sum(tasks[i][0] for i in s) <= T:
                v = sum(tasks[i][1] for i in s)
                if v > best:
                    best, arg = v, s
    return best, arg


random.seed(7)
ex = [(2, 4), (3, 5), (4, 10)]
Pex = table(ex, 6)
q1 = [(1, 1), (2, 3), (4, 7), (5, 10)]
P1 = table(q1, 6)


def f_one(i, c):
    return ex[i - 1][1] if ex[i - 1][0] <= c else 0


def f_count(i, c):
    return max(len(s) for r in range(i + 1) for s in itertools.combinations(range(i), r)
               if sum(ex[k][0] for k in s) <= c)


def f_mint(i, c):
    best = 10 ** 9
    for r in range(i + 1):
        for s in itertools.combinations(range(i), r):
            if sum(ex[k][1] for k in s) >= c:
                best = min(best, sum(ex[k][0] for k in s))
    return best


def same_as_P(f):
    return all(f(i, c) == Pex[i][c] for i in range(1, 4) for c in range(1, 7))


check("Q1a P == brute force max profit", all(Pex[i][c] == brute(ex[:i], c)[0] for i in range(4) for c in range(7)))
choice2(1, PA, 0, True, [same_as_P(f_one), same_as_P(f_count), same_as_P(f_mint)])
numeric(1, PA, 1, brute(ex[:2], 5)[0])
opt = brute(ex, 6)[0]
choice2(1, PA, 2, Pex[3][6] == opt, [Pex[3][0] == opt, Pex[0][6] == opt, 6 <= 3])   # P(T,n): index T=6 > n=3

# Q1b
numeric(1, PB, 0, P1[3][6])
check("Q1b P(2,6)=4, P(2,2)=3 as stated in the prompt", P1[2][6] == 4 and P1[2][2] == 3)
choice2(1, PB, 1, P1[2][1] == P1[1][1] and 2 > 1, [P1[2][1] == 0, P1[2][1] == q1[1][1], False])  # last: index c-t_i<0
check("Q1b buggy recurrence gives 10 instead of 5 for one task (2,5), T=4",
      table_bug([(2, 5)], 4)[1][4] == 10 and table([(2, 5)], 4)[1][4] == 5 == brute([(2, 5)], 4)[0])
check("Q1b findbug index 2", step(1, PB, 2)["bugIndex"] == 2)
bad = 0
for _ in range(2000):
    tasks = [(random.randint(1, 6), random.randint(1, 12)) for _ in range(random.randint(0, 6))]
    T = random.randint(0, 14)
    bad += table(tasks, T)[len(tasks)][T] != brute(tasks, T)[0]
check("Q1b recurrence == brute force (2000 random)", bad == 0)

# Q1c
numeric(1, PC, 0, (4 + 1) * (6 + 1))
textstep(1, PC, 1, ["O(nT)"])
textstep(1, PC, 2, ["O(T)"])


def rolling(tasks, T):
    prev = [0] * (T + 1)
    for t, v in tasks:
        prev = [prev[c] if t > c else max(prev[c], v + prev[c - t]) for c in range(T + 1)]
    return prev[T]


check("Q1c two rows (2*(T+1) cells) give the same answer as the full table", all(rolling(q1[:k], 6) == P1[k][6] for k in range(5)))

# Q1d
numeric(1, PD, 0, P1[3][5])
numeric(1, PD, 1, P1[4][5])
numeric(1, PD, 2, P1[4][6])


def backtrack(P, tasks, T):
    S, c, reads = [], T, []
    for i in range(len(tasks), 0, -1):
        reads.append(i)
        if P[i][c] != P[i - 1][c]:
            S.append(i)
            c -= tasks[i - 1][0]
    return sorted(S), reads


S, reads = backtrack(P1, q1, 6)


def okset(S_):
    return sum(q1[k - 1][0] for k in S_) <= 6 and sum(q1[k - 1][1] for k in S_) == P1[4][6]


choice2(1, PD, 3, okset([1, 4]), [okset([2, 3]), okset([4]), okset([1, 2, 3])])
check("Q1d unique optimum set {1,4}",
      S == [1, 4] and sum(1 for r in range(5) for s in itertools.combinations(range(1, 5), r) if okset(s)) == 1)

# Q1e
textstep(1, PE, 0, ["O(nT)"])
numeric(1, PE, 1, len(reads))
check("Q1e backtracking reads rows 4,3,2,1 (and row i-1 each time): all n+1 rows needed", reads == [4, 3, 2, 1])
choice2(1, PE, 2, len(reads) + 1 > 2, [False, False, False])

# ================================================================ Q2: greedy
def ratio_greedy(tasks, T):
    tot = 0
    for t, v in sorted(tasks, key=lambda x: -x[1] / x[0]):
        if t <= T:
            T -= t
            tot += v
    return tot


def is_ce(tasks, T):
    return ratio_greedy(tasks, T) < brute(tasks, T)[0]


ce = [(1, 2), (5, 9)]
choice2(2, PA, 0, is_ce(ce, 5), [is_ce([(1, 1), (2, 3)], 3), is_ce(ex, 6), is_ce([(2, 4), (3, 6)], 5)])
numeric(2, PA, 1, ratio_greedy(ce, 5))
numeric(2, PA, 2, brute(ce, 5)[0])

numeric(2, PB, 0, 17 // 5)
prof = [4, 9, 1, 7, 3, 8]
best_eq = brute([(2, v) for v in prof], 7)[0]
numeric(2, PB, 1, best_eq)
k = 7 // 2


def good(sel):
    return len(sel) <= k and sum(sel) == best_eq


choice2(2, PB, 2, good(sorted(prof, reverse=True)[:k]),
        [good(sorted(prof)[:k]), good(prof[:k]), good([v for v in prof if v >= 4])])
bad = 0
for _ in range(3000):
    n = random.randint(0, 8)
    t = random.randint(1, 4)
    T = random.randint(0, 15)
    vs = [random.randint(-3, 12) for _ in range(n)]
    kk = T // t
    g = sum(v for v in sorted(vs, reverse=True)[:kk] if v > 0)
    b = max(sum(vs[i] for i in s) for r in range(min(kk, n) + 1) for s in itertools.combinations(range(n), r))
    bad += g != b
check("Q2b/c top-k positive profits == brute force (3000 random)", bad == 0)
viol_ge = viol_le = 0
for _ in range(3000):
    n = random.randint(1, 8)
    vs = [random.randint(1, 12) for _ in range(n)]
    kk = random.randint(1, n)
    G = set(sorted(range(n), key=lambda i: -vs[i])[:kk])
    O = set(random.sample(range(n), kk))
    for i in G - O:
        for j in O - G:
            viol_ge += not vs[i] >= vs[j]
            viol_le += vs[i] > vs[j]
check("Q2c exchange direction: v_i >= v_j always; the buggy v_i <= v_j fails on some instance", viol_ge == 0 and viol_le > 0)
check("Q2c order has 4 lines; findbug bug index 1", len(step(2, PC, 1)["lines"]) == 4 and step(2, PC, 2)["bugIndex"] == 1)
textstep(2, PC, 3, ["O(n log n)"])

# ================================================================ Q3
C5 = {"s": ["u", "w"], "u": ["s", "x"], "x": ["u", "v"], "v": ["x", "w"], "w": ["s", "v"]}   # edge-list order


def bfs(adj, s):
    color = {v: "W" for v in adj}
    par, disc, white_at, queues = {s: None}, [s], {}, []
    color[s] = "G"
    Q = deque([s])
    while Q:
        u = Q.popleft()
        white_at[u] = {v for v in adj if color[v] == "W"}
        for v in adj[u]:
            if color[v] == "W":
                color[v] = "G"
                par[v] = u
                disc.append(v)
                Q.append(v)
        color[u] = "B"
        queues.append((u, list(Q)))
    return par, disc, white_at, queues


par, disc, white_at, queues = bfs(C5, "s")
check("Q3a BFS order s,u,w,x,v", disc == ["s", "u", "w", "x", "v"])
textstep(3, PA, 0, ["s, u, w, x, v"])
choice2(3, PA, 1, par["v"] == "w", [par["v"] == "u", par["v"] == "x", par["v"] == "s"])
check("Q3a trace: queues [u,w], [w,x], [x,v]; v white and path u-x-v when u dequeued; pi(v)=w",
      queues[0] == ("s", ["u", "w"]) and queues[1] == ("u", ["w", "x"]) and queues[2] == ("w", ["x", "v"])
      and {"v", "x"} <= white_at["u"] and par["x"] == "u" and par["v"] == "w")


def is_desc(par_, v, u):
    while v is not None:
        if v == u:
            return True
        v = par_[v]
    return False


check("Q3a v is not a descendant of u; order step has 4 lines", not is_desc(par, "v", "u") and len(step(3, PA, 2)["lines"]) == 4)
C4 = {"s": ["u", "w"], "u": ["s", "v"], "v": ["u", "w"], "w": ["s", "v"]}
p4, d4, _w, _q = bfs(C4, "s")
check("Q3a pitfall: in the exam's 4-cycle v is a descendant of u", d4 == ["s", "u", "w", "v"] and is_desc(p4, "v", "u"))


def dfs(adj, s):
    color, par_, cls = {}, {s: None}, {}

    def visit(u):
        color[u] = "G"
        for v in adj[u]:
            key = frozenset((u, v))
            if v not in color:
                par_[v] = u
                cls[key] = "tree"
                visit(v)
            elif key not in cls:
                cls[key] = "back" if color[v] == "G" else "other"
        color[u] = "B"
    visit(s)
    return par_, cls


random.seed(11)
first_white = no_cross = True
nback = 0
for _ in range(3000):
    n = random.randint(3, 8)
    G = nx.gnp_random_graph(n, 0.45, seed=random.randint(0, 10 ** 6))
    if not nx.is_connected(G):
        continue
    adj = {v: random.sample(list(G[v]), len(G[v])) for v in G}
    s = random.choice(list(G))
    pb, _d, wb, _q = bfs(adj, s)
    first_white &= wb[s] == set(adj) - {s} and all(pb.get(v) == s for v in adj[s])
    pd, cls = dfs(adj, s)
    no_cross &= not any(c == "other" for c in cls.values())
    nback += any(c == "back" for c in cls.values())
check("Q3b BFS: all neighbours of s are white at its dequeue and become its children", first_white)
check("Q3b undirected DFS: every non-tree edge is a back edge; such edges exist", no_cross and nback > 0)
choice2(3, PB, 0, first_white, [False, False, False])
choice2(3, PB, 1, no_cross and nback > 0, [False, False, False])
bad = 0
for _ in range(3000):
    n = random.randint(3, 7)
    G = nx.gnp_random_graph(n, 0.5, seed=random.randint(0, 10 ** 6))
    if not nx.is_connected(G):
        continue
    cyc = set()
    for u, v in G.edges():
        H = G.copy()
        H.remove_edge(u, v)
        if nx.has_path(H, u, v):
            cyc |= {u, v}
    if not cyc:
        continue
    s = random.choice(sorted(cyc))
    adj = {v: random.sample(list(G[v]), len(G[v])) for v in G}
    pb = bfs(adj, s)[0]
    pd = dfs(adj, s)[0]
    eb = {frozenset((v, p)) for v, p in pb.items() if p is not None}
    ed = {frozenset((v, p)) for v, p in pd.items() if p is not None}
    bad += eb == ed
check("Q3b T_BFS != T_DFS when s lies on a cycle (random graphs and orders)", bad == 0)
check("Q3b order has 5 lines; findbug bug index 1", len(step(3, PB, 2)["lines"]) == 5 and step(3, PB, 3)["bugIndex"] == 1)


def msts(edges, nv=4):
    best, trees = None, []
    for es in itertools.combinations(edges, nv - 1):
        H = nx.Graph([(a, b) for a, b, _ in es])
        if H.number_of_nodes() == nv and nx.is_connected(H):
            w = sum(x for *_, x in es)
            if best is None or w < best:
                best, trees = w, [frozenset(es)]
            elif w == best:
                trees.append(frozenset(es))
    return best, trees


K = [("A", "B", 1), ("B", "C", 2), ("C", "D", 2), ("A", "C", 4), ("B", "D", 5), ("A", "D", 6)]
w_new, trees_new = msts(K)
numeric(3, PC, 0, w_new)
numeric(3, PC, 1, len(trees_new))
base = [("A", "B", 1), ("B", "C", 3), ("C", "D", 2), ("A", "C", 4), ("B", "D", 5), ("A", "D", 6)]
b_w, b_t = msts(base)
check("Q3c original MST {AB,BC,CD} weight 6 unique; after BC 3->2 still the unique MST",
      b_w == 6 and b_t == [frozenset({("A", "B", 1), ("B", "C", 3), ("C", "D", 2)})]
      and trees_new == [frozenset({("A", "B", 1), ("B", "C", 2), ("C", "D", 2)})])
eff = True
for es in itertools.combinations(base, 3):
    H = nx.Graph([(a, b) for a, b, _ in es])
    if H.number_of_nodes() == 4 and nx.is_connected(H):
        w0 = sum(x for *_, x in es)
        w1 = sum(x - 1 if (a, b) == ("B", "C") else x for a, b, x in es)
        eff &= w1 == (w0 - 1 if ("B", "C", 3) in es else w0)
choice2(3, PC, 2, eff, [False, False, False])
check("Q3c findbug bug index 2", step(3, PC, 3)["bugIndex"] == 2)
bad = 0
for _ in range(1500):
    n = random.randint(3, 6)
    G = nx.gnp_random_graph(n, 0.7, seed=random.randint(0, 10 ** 6))
    if not nx.is_connected(G):
        continue
    for (a, b), w in zip(G.edges(), random.sample(range(1, 1000), G.number_of_edges())):
        G[a][b]["weight"] = w
    T = nx.minimum_spanning_tree(G)
    e = random.choice(list(T.edges()))
    G[e[0]][e[1]]["weight"] -= 1
    bad += {frozenset(x) for x in T.edges()} != {frozenset(x) for x in nx.minimum_spanning_tree(G).edges()}
check("Q3c T stays the MST after lowering a tree edge by 1 (random)", bad == 0)

# ================================================================ Q4
codes = {"a": "0", "b": "1100", "c": "1101", "d": "111"}
numeric(4, PA, 0, sum(2 ** -len(w) for w in codes.values()))


def full(w):
    ws = list(codes.values()) + [w]
    return sum(2 ** -len(x) for x in ws) == 1 and all(not y.startswith(x) for x in ws for y in ws if x != y)


check("Q4a(i) only e=10 completes a full prefix-free tree",
      [w for w in ["10", "100", "01", "110", "1111", "1110"] if full(w)] == ["10"])
choice2(4, PA, 1, full("10"), [False, False, False])
check("Q4a(i) distractors: code lengths differ; 1111 starts with 111",
      len({len(w) for w in codes.values()}) > 1 and "1111".startswith("111"))
textstep(4, PA, 2, ["10"])


def huffman_all(freq):
    results = set()

    def rec(nodes):
        if len(nodes) == 1:
            out = {}

            def walk(t, p):
                if isinstance(t[1], str):
                    out[t[1]] = p
                else:
                    walk(t[1], p + "0")
                    walk(t[2], p + "1")
            walk(nodes[0], "")
            results.add(tuple(sorted(out.items())))
            return
        idx = range(len(nodes))
        for i, j in itertools.permutations(idx, 2):
            x, y = nodes[i], nodes[j]
            others = [nodes[k_][0] for k_ in idx if k_ not in (i, j)]
            if x[0] > y[0] or (others and max(x[0], y[0]) > min(others)):
                continue
            rec([nodes[k_] for k_ in idx if k_ not in (i, j)] + [(x[0] + y[0], x, y)])
    rec([(f, c) for c, f in freq.items()])
    return results


target = tuple(sorted(dict(codes, e="10").items()))
goodf = [fe for fe in range(1, 30) if target in huffman_all({"a": 13, "b": 1, "c": 2, "d": 4, "e": fe})]
check("Q4b f(e) in {6,7} exactly (every tie-break, left <= right)", goodf == [6, 7])
numeric(4, PB, 0, 1 + 2)
numeric(4, PB, 1, 1 + 2 + 4)
numeric(4, PB, 2, min(goodf))
choice2(4, PB, 3, goodf == [6, 7], [goodf == [6], goodf == [7], goodf == list(range(4, 14))])

W = GR["26B-A-Q4b"]["edges"]


def graph(X):
    G = nx.Graph()
    for e in W:
        G.add_edge(e["u"], e["v"], weight=X if e["w"] is None else e["w"])
    return G


def all_msts(G):
    n = G.number_of_nodes()
    best, trees = None, []
    for es in itertools.combinations(list(G.edges(data="weight")), n - 1):
        H = nx.Graph([(a, b) for a, b, _ in es])
        if H.number_of_nodes() == n and nx.is_connected(H):
            w = sum(x for *_, x in es)
            k_ = frozenset(frozenset((a, b)) for a, b, _ in es)
            if best is None or w < best:
                best, trees = w, [k_]
            elif w == best:
                trees.append(k_)
    return best, trees


DF = frozenset(("D", "F"))
in_all = {X: all(DF in t for t in all_msts(graph(X))[1]) for X in range(0, 8)}
Xmax = max(X for X, v in in_all.items() if v)
Gm = graph(3)
Gm.remove_edge("D", "F")
bott = min(max(Gm[p[i]][p[i + 1]]["weight"] for i in range(len(p) - 1)) for p in nx.all_simple_paths(Gm, "D", "F"))
numeric(4, PC, 1, bott)
numeric(4, PC, 2, Xmax)
check("Q4c X=3 largest; bottleneck 4", Xmax == 3 and bott == 4 and in_all[3] and not in_all[4])
crit = {X: X < bott for X in range(8)}
lightest_overall = {X: X < min(e["w"] for e in W if e["w"] is not None) for X in range(8)}   # D-F lighter than all
not_heaviest = {X: X < 9 for X in range(8)}   # the heaviest other edge is C-F = 9
no_cycle = {X: False for X in range(8)}
check("Q4c criterion 'every cycle has a strictly heavier edge' == in every MST for X=0..7", crit == in_all)
choice2(4, PC, 0, crit == in_all, [lightest_overall == in_all, not_heaviest == in_all, no_cycle == in_all])


def prim_valid(seq, G, r):
    inT = {r}
    for a, b in seq:
        if (a in inT) == (b in inT) or not G.has_edge(a, b):
            return False
        cross = [G[x][y]["weight"] for x in inT for y in G[x] if y not in inT]
        if G[a][b]["weight"] != min(cross):
            return False
        inT.add(b if a in inT else a)
    return len(inT) == G.number_of_nodes()


def seq_of(s):
    return [tuple(x.strip("()").split(",")) for x in s.split()]


G3 = graph(3)
opts = ["(C,D) (C,A) (D,F) (C,B) (F,H) (H,G) (G,E)",
        "(C,D) (C,A) (D,E) (C,B) (D,F) (E,G) (G,H)",
        "(C,D) (C,B) (C,A) (D,F) (D,E) (E,G) (G,H)",
        "(C,D) (C,A) (C,B) (D,F) (D,E) (E,G) (F,H)"]
v = [prim_valid(seq_of(o), G3, "C") for o in opts]
choice2(4, PD, 1, v[0], v[1:])


def prim_all(G, r):
    res = []

    def rec(inT, seq):
        if len(inT) == G.number_of_nodes():
            res.append(tuple(seq))
            return
        cand = [(G[a][b]["weight"], a, b) for a in inT for b in G[a] if b not in inT]
        m = min(c[0] for c in cand)
        for w, a, b in cand:
            if w == m:
                rec(inT | {b}, seq + [(a, b)])
    rec({r}, [])
    return set(res)


orders = prim_all(G3, "C")
listed = {tuple(seq_of(x)) for x in ["(C,D) (C,A) (C,B) (D,F) (D,E) (E,G) (G,H)", "(C,D) (C,A) (C,B) (D,F) (F,H) (H,G) (G,E)",
                                     "(C,D) (C,A) (D,F) (C,B) (D,E) (E,G) (G,H)", "(C,D) (C,A) (D,F) (C,B) (F,H) (H,G) (G,E)"]}
check("Q4d the four orders listed in the solution are exactly all valid Prim orders, each of weight 18",
      listed == orders and all(sum(G3[a][b]["weight"] for a, b in o) == 18 for o in orders))
msts_x3 = all_msts(G3)
mst_of_orders = {frozenset(frozenset(e) for e in o) for o in orders}
check("Q4d two MSTs of weight 18, both reached by the orders", msts_x3[0] == 18 and len(msts_x3[1]) == 2
      and mst_of_orders == set(msts_x3[1]))
inT = {"C", "D", "A"}
cand = sorted((G3[a][b]["weight"], tuple(sorted((a, b)))) for a in inT for b in G3[a] if b not in inT)
tie = {e for w, e in cand if w == cand[0][0]}
choice2(4, PD, 0, tie == {("B", "C"), ("D", "F")},
        [tie == {("A", "B"), ("B", "C")}, tie == {("D", "E"), ("F", "H")}, tie == {("C", "F"), ("A", "F")}])
numeric(4, PD, 2, msts_x3[0])
numeric(4, PD, 3, len(msts_x3[1]))


def pi_fn(Pp):
    pi, trace = [0] * len(Pp), []
    k_ = 0
    last = len(Pp) - 1
    for i in range(1, len(Pp)):
        while k_ and Pp[i] != Pp[k_]:
            if i == last:
                trace.append(k_)
            k_ = pi[k_ - 1]
        if i == last:
            trace.append(k_)
        if Pp[i] == Pp[k_]:
            k_ += 1
        pi[i] = k_
    return pi, trace


PP = "AABAABAABAAA"
pi, trace = pi_fn(PP)
brute_pi = [max(k_ for k_ in range(i + 1) if PP[:k_] == PP[i + 1 - k_:i + 1] and k_ != i + 1) for i in range(12)]
check("Q4e pi == brute force", pi == brute_pi == [0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 2])
numeric(4, PE, 0, pi[5])
numeric(4, PE, 1, pi[10])
numeric(4, PE, 3, pi[11])
check("Q4e fallback trace k = 8,5,2,1 and pi[12]=2; order step has 4 lines", trace == [8, 5, 2, 1] and pi[11] == 2
      and len(step(4, PE, 2)["lines"]) == 4)
check("Q4e pitfall: AABAABAAB (9) is not a suffix of P", PP[:9] != PP[3:])


def variants(A_):
    k_ = math.isqrt(len(A_))
    x = sorted(A_)[k_ - 1]
    less = [y for y in A_ if y < x]
    return (sorted(less + [x] * (k_ - len(less))), sorted(less), sorted(y for y in A_ if y <= x),
            sorted([y for y in A_ if y <= x][:k_]), sorted(A_)[:k_])


res, fails = True, [False, False, False]
for _ in range(4000):
    A_ = [random.randint(-10, 10) for _ in range(random.randint(1, 60))]
    c, o, le, fl, ref = variants(A_)
    res &= c == ref
    fails[0] |= o != ref
    fails[1] |= le != ref
    fails[2] |= fl != ref
numeric(4, PF, 0, math.isqrt(50))
check("Q4f correct variant == k smallest sorted; each distractor fails on some array", res and all(fails))
choice2(4, PF, 2, res, [not f for f in fails])
textstep(4, PF, 3, ["O(n)"])

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
