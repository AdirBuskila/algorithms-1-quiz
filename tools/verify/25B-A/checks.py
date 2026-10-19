# -*- coding: utf-8 -*-
"""Verification harness for 25B-A (algorithms-1). Run: PYTHONUTF8=1 py tools/verify/25B-A/checks.py
Checks the official answers (never modifies them). ASCII output."""
import itertools, heapq, random, json, pathlib
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


# ---------- Q1a: DFS that always takes the lightest edge is not an MST ----------
g = json.load(open(HERE / "graphs.json"))["25B-A-Q1a"]
G = nx.Graph()
for e in g["edges"]:
    G.add_edge(e["u"], e["v"], weight=e["w"])
mst_w = sum(d["weight"] for _, _, d in nx.minimum_spanning_tree(G).edges(data=True))


def lightest_dfs(G, s):
    seen, tree = {s}, []

    def go(u):
        for v, d in sorted(G[u].items(), key=lambda t: t[1]["weight"]):
            if v not in seen:
                seen.add(v)
                tree.append((u, v, d["weight"]))
                go(v)
    go(s)
    return tree


w_from = {s: sum(t[2] for t in lightest_dfs(G, s)) for s in G}
check("Q1a MST weight is 9", mst_w == 9)
check("Q1a start c gives DFS tree {cb, ba} (not an MST): claim false", w_from["c"] > mst_w)
check("Q1a official says total 13 but 4+7 = 11 (transcription note)", w_from["c"] == 11, "weights=%s" % w_from)

# ---------- Q1b: a path between two vertices of a component stays inside it ----------
random.seed(5)
bad = 0
for _ in range(300):
    n = random.randint(2, 9)
    H = nx.gnp_random_graph(n, random.random() * 0.5, seed=random.randint(0, 10**6))
    for comp in nx.connected_components(H):
        for x, y in itertools.combinations(comp, 2):
            for p in nx.all_simple_paths(H, x, y):
                if not set(p) <= comp:
                    bad += 1
check("Q1b every simple path inside a component stays in it (300 random graphs)", bad == 0)

# ---------- Q2: children and money ----------
def brute(D, K):
    best = 0
    for r in range(len(D) + 1):
        for c in itertools.combinations(D, r):
            if sum(c) <= K:
                best = max(best, r)
    return best


def greedy(D, K):
    tot = cnt = 0
    for d in sorted(D):
        if tot + d <= K:
            tot += d
            cnt += 1
        else:
            break
    return cnt


check("Q2 example [1,9,4,2,4], K=10 -> 3", brute([1, 9, 4, 2, 4], 10) == 3 == greedy([1, 9, 4, 2, 4], 10))
check("Q2a printed example (1,4,4) and official (1,2,4) both cost <= 10 with 3 kids", 1 + 4 + 4 <= 10 and 1 + 2 + 4 <= 10)
bad = 0
for _ in range(3000):
    D = [random.randint(1, 12) for _ in range(random.randint(1, 8))]
    K = random.randint(0, 40)
    if brute(D, K) != greedy(D, K):
        bad += 1
check("Q2b official greedy == brute force (3000 random)", bad == 0, "mismatches=%d" % bad)

# ---------- Q3a: Huffman, e = 11, d = 7 ----------
lens = {"a": 3, "b": 3, "c": 2, "d": 2, "e": 2}
code = {"a": "011", "b": "010", "c": "00", "d": "10"}
check("Q3a(i) e=11 completes a full prefix-free tree",
      sum(2.0 ** -len(c) for c in list(code.values()) + ["11"]) == 1.0
      and not any(a != b and code[b].startswith(code[a]) for a in code for b in code))


def hcost(fs):
    h = list(fs)
    heapq.heapify(h)
    c = 0
    while len(h) > 1:
        x, y = heapq.heappop(h), heapq.heappop(h)
        c += x + y
        heapq.heappush(h, x + y)
    return c


def huffman_shapes(f):
    """All tree shapes (unordered) the Huffman ALGORITHM can produce, over every tie-break."""
    out = set()

    def rec(items):
        if len(items) == 1:
            out.add(items[0][1])
            return
        items = sorted(items, key=lambda t: t[0])
        w1, w2 = items[0][0], items[1][0]
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if items[i][0] == w1 and items[j][0] == w2 or (items[i][0] == w1 and items[j][0] == w1 and w1 == w2):
                    rest = [x for k, x in enumerate(items) if k not in (i, j)]
                    rec(rest + [(items[i][0] + items[j][0], frozenset([items[i][1], items[j][1]]))])
    rec([(v, k) for k, v in f.items()])
    return out


target = frozenset([frozenset([frozenset([frozenset(["b", "a"]), "c"]), frozenset(["d", "e"])])]) if False else     frozenset([frozenset([frozenset(["b", "a"]), "c"]), frozenset(["d", "e"])])
sols = []
opt_only = []
for d in range(1, 40):
    f = {"a": 5, "b": 2, "c": 5, "d": d, "e": 7}
    rule = f["b"] <= f["a"] and f["c"] <= f["a"] + f["b"] and f["a"] + f["b"] + f["c"] <= f["d"] + f["e"] and f["d"] <= f["e"]
    if rule and target in huffman_shapes(f):
        sols.append(d)
    if rule and sum(f[k] * lens[k] for k in f) == hcost(f.values()):
        opt_only.append(d)
check("Q3a(ii) only d=7 gives this shape through the Huffman algorithm (sibling-order rule)", sols == [7], "d=%s" % sols)
print("NOTE  d=%s give an optimal-cost code of this shape, but only d=7 is producible by the algorithm (official answer 7)" % opt_only)

# ---------- Q3b: prefix function and comparisons ----------
def pi_fn(P):
    pi = [0] * len(P)
    k = 0
    for i in range(1, len(P)):
        while k and P[i] != P[k]:
            k = pi[k - 1]
        if P[i] == P[k]:
            k += 1
        pi[i] = k
    return pi


P = "ABABBAAABABA"
check("Q3b(i) pi = 0 0 1 2 0 1 1 1 2 3 4 3", pi_fn(P) == [0, 0, 1, 2, 0, 1, 1, 1, 2, 3, 4, 3])
T = "ABABBAAABABCXXXX"
pi = pi_fn(P)
j = 0
cmp_c = 0
for ch in T:
    while True:
        if j == len(P):
            j = pi[j - 1]
        if ch == "C":
            cmp_c += 1
        if P[j] == ch:
            j += 1
            break
        if j == 0:
            break
        j = pi[j - 1]
check("Q3b(ii) comparisons of C against P during KMP = 4", cmp_c == 4, "got %d" % cmp_c)

# ---------- Q4: divisibility-closed subsets ----------
def brute_div(A):
    best = 0
    for r in range(len(A), 0, -1):
        for c in itertools.combinations(A, r):
            if all(x % y == 0 or y % x == 0 for x, y in itertools.combinations(c, 2)):
                return r
    return best


def dp_fwd(A):
    n = len(A)
    C = [0] * n
    for i in range(n):
        C[i] = max([C[j] for j in range(i) if A[i] % A[j] == 0] + [0]) + 1
    return C


def dp_bwd(A):
    n = len(A)
    C = [0] * n
    for i in range(n - 1, -1, -1):
        C[i] = max([C[j] for j in range(i + 1, n) if A[j] % A[i] == 0] + [0]) + 1
    return C


ex = [1, 2, 3, 4, 5, 6, 8, 10, 11]
check("Q4c table 1 2 2 3 2 3 4 3 2", dp_fwd(ex) == [1, 2, 2, 3, 2, 3, 4, 3, 2])
check("Q4 sample {1,2,3,4,5,6,8,10} max closed subset has size 4", brute_div([1, 2, 3, 4, 5, 6, 8, 10]) == 4)
bad = 0
for _ in range(1500):
    A = sorted(random.sample(range(1, 40), random.randint(1, 9)))
    b = brute_div(A)
    if not (max(dp_fwd(A)) == max(dp_bwd(A)) == b):
        bad += 1
check("Q4a both recurrences == brute force (1500 random sorted arrays)", bad == 0, "mismatches=%d" % bad)

# ---------- graphs.json tree ----------
t = json.load(open(HERE / "graphs.json"))["25B-A-Q3a"]
D = nx.DiGraph()
for e in t["edges"]:
    D.add_edge(e["u"], e["v"], bit=e["w"])
dec = {}
for n in D:
    if D.out_degree(n) == 0:
        path = nx.shortest_path(D, "26", n)
        dec[n[0]] = "".join(str(D[a][b]["bit"]) for a, b in zip(path, path[1:]))
check("graphs.json Q3a tree reproduces the code table (+ e=11, d=10)",
      dec == {"a": "011", "b": "010", "c": "00", "d": "10", "e": "11"})

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
