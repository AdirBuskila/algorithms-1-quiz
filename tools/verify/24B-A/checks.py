# -*- coding: utf-8 -*-
"""Verification harness for 24B-A (algorithms-1). Run: PYTHONUTF8=1 py tools/verify/24B-A/checks.py
Checks the official answers (never modifies them). ASCII output."""
import itertools, heapq, random, json, pathlib
import networkx as nx
from networkx.algorithms.tree.mst import SpanningTreeIterator

HERE = pathlib.Path(__file__).resolve().parent
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


gj = json.load(open(HERE / "graphs.json"))


def load(key):
    g = gj[key]
    G = nx.Graph()
    G.add_nodes_from(g["vertices"])
    for e in g["edges"]:
        G.add_edge(e["u"], e["v"], weight=e.get("w", 1))
    return G


# ---------- Q1: |E|=|V| undirected ----------
def e_bfs(G, v):
    return nx.bfs_tree(G, v).number_of_edges()


def e_dfs(G):
    return sum(1 for _ in nx.dfs_edges(G))


G1 = load("24B-A-Q1a")
check("Q1a counterexample: 6 vertices, 6 edges, not connected",
      G1.number_of_nodes() == 6 and G1.number_of_edges() == 6 and not nx.is_connected(G1))
G2 = load("24B-A-Q1b")
check("Q1b counterexample: 5 vertices, 5 edges, not connected",
      G2.number_of_nodes() == 5 and G2.number_of_edges() == 5 and not nx.is_connected(G2))
check("Q1b BFS from 0 has 3 edges, DFS forest has 3 edges", e_bfs(G2, "0") == 3 == e_dfs(G2))
bad = tested = 0
for G in nx.graph_atlas_g():
    if G.number_of_nodes() == 0 or G.number_of_edges() != G.number_of_nodes():
        continue
    tested += 1
    allv = all(e_bfs(G, v) == e_dfs(G) for v in G)
    if allv and not nx.is_connected(G):
        bad += 1
check("Q1c (for ALL v equal => connected) over all graphs with |E|=|V|, n<=7", bad == 0 and tested > 0,
      "graphs=%d bad=%d" % (tested, bad))
# claims a and b are indeed false on the counterexamples (b), and a: some graph is disconnected with |E|=|V|
check("Q1a: disconnected graph with |E|=|V| exists (G1)", not nx.is_connected(G1))


# ---------- Q2: train stations ----------
def official(X, D):
    C = [X[0] + D]
    for x in X[1:]:
        if x - D > C[-1]:
            C.append(x + D)
    return C


def covers(X, C, D):
    return all(any(abs(x - c) <= D for c in C) for x in X)


def brute_min(X, D):
    lo, hi = min(X) - D, max(X) + D
    cand = range(lo, hi + 1)
    for k in range(1, len(X) + 1):
        for C in itertools.combinations(cand, k):
            if covers(X, C, D):
                return k
    return None


check("Q2 example: [1,5,9,16], D=3: official gives 3 stations and covers",
      covers([1, 5, 9, 16], official([1, 5, 9, 16], 3), 3) and len(official([1, 5, 9, 16], 3)) == 3)
check("Q2a [3,9,16] and [4,9,16] both cover (not unique)",
      covers([1, 5, 9, 16], [3, 9, 16], 3) and covers([1, 5, 9, 16], [4, 9, 16], 3))
random.seed(5)
bad = 0
for _ in range(300):
    D = random.randint(1, 4)
    X = sorted(random.sample(range(0, 16), random.randint(1, 5)))
    C = official(X, D)
    if not covers(X, C, D) or len(C) != brute_min(X, D):
        bad += 1
check("Q2b official algorithm is valid and optimal vs brute force (300 random)", bad == 0, "bad=%d" % bad)

# ---------- Q3a: Huffman ----------
code = {"c": "00", "d": "01", "e": "10", "a": "110", "b": "111"}
freq = {"a": 1, "b": 1, "c": 2, "d": 2, "e": 2}


def huff_cost(fs):
    h = list(fs)
    heapq.heapify(h)
    c = 0
    while len(h) > 1:
        x = heapq.heappop(h)
        y = heapq.heappop(h)
        c += x + y
        heapq.heappush(h, x + y)
    return c


check("Q3a code is prefix-free with Kraft sum 1",
      not any(p != q and code[q].startswith(code[p]) for p in code for q in code)
      and sum(2.0 ** -len(c) for c in code.values()) == 1.0)
check("Q3a frequencies 1,1,2,2,2: code cost equals the optimal Huffman cost",
      sum(freq[k] * len(code[k]) for k in freq) == huff_cost(freq.values()),
      "cost=%d" % huff_cost(freq.values()))
g = gj["24B-A-Q3a"]
D = nx.DiGraph()
for e in g["edges"]:
    D.add_edge(e["u"], e["v"], bit=e["w"])
dec = {}
for n in D:
    if D.out_degree(n) == 0:
        path = nx.shortest_path(D, "8", n)
        dec[n[0]] = "".join(str(D[a][b]["bit"]) for a, b in zip(path, path[1:]))
check("Q3a graphs.json tree reproduces the code table", dec == code)

# ---------- Q3b: max-weight edge ----------
G3 = load("24B-A-Q3b")
w = {frozenset(e): d["weight"] for *e, d in G3.edges(data=True)}
best = min(sum(d["weight"] for *_, d in T.edges(data=True)) for T in SpanningTreeIterator(G3, "weight"))
trees = [T for T in SpanningTreeIterator(G3, "weight")
         if sum(d["weight"] for *_, d in T.edges(data=True)) == best]
check("Q3b every MST contains the weight-10 edge (counterexample to 'no MST contains e1')",
      len(trees) == 3 and all(T.has_edge("2", "3") for T in trees), "msts=%d weight=%d" % (len(trees), best))
check("Q3b e1 is a bridge", frozenset(("2", "3")) in {frozenset(e) for e in nx.bridges(G3)})
bad = 0
random.seed(7)
for _ in range(300):
    n = random.randint(3, 7)
    H = nx.gnp_random_graph(n, 0.5, seed=random.randint(0, 10 ** 6))
    if not nx.is_connected(H):
        continue
    for u, v in H.edges():
        H[u][v]["weight"] = random.randint(1, 5)
    for u, v in nx.bridges(H):
        T = nx.minimum_spanning_tree(H)
        if not T.has_edge(u, v):
            bad += 1
check("Q3b a bridge is always in every spanning tree (random)", bad == 0)


# ---------- Q4: 1 -> K operations ----------
def bfs_ops(K):
    dist = {1: 0}
    q = [1]
    for x in q:
        for y in (x + 1, 2 * x, 3 * x):
            if y <= 3 * K + 3 and y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    return dist[K]


def c1(K):
    INF = float("inf")
    C = {1: 0}
    for i in range(2, K + 1):
        opts = [C[i - 1]]
        if i % 2 == 0:
            opts.append(C[i // 2])
        if i % 3 == 0:
            opts.append(C[i // 3])
        C[i] = min(opts) + 1
    return C


def c2(K):  # C(i): min ops to turn K into i by -1, /2 (even), /3 (divisible); answer C(1)
    INF = float("inf")
    memo = {}

    def C(i):
        if i == K:
            return 0
        if i > K:
            return INF
        if i in memo:
            return memo[i]
        memo[i] = min(C(i + 1), C(2 * i), C(3 * i)) + 1
        return memo[i]
    return C(1)


bad = 0
for K in range(1, 400):
    if not (c1(K)[K] == c2(K) == bfs_ops(K)):
        bad += 1
check("Q4a both recurrences equal BFS shortest ops for K=1..399", bad == 0, "bad=%d" % bad)
check("Q4a K=10 needs 3 operations", c1(10)[10] == 3)
check("Q4c table for K=7 is 0 1 1 2 3 2 3", [c1(7)[i] for i in range(1, 8)] == [0, 1, 1, 2, 3, 2, 3])

# ---------- Bonus: suffix array of BANANABAN ----------
s = "BANANABAN"
sa = [i + 1 for i in sorted(range(len(s)), key=lambda i: s[i:])]
given = [6, 8, 2, 4, 7, 1, 9, 5, 3]
check("Bonus: true suffix array is [6,8,4,2,7,1,9,5,3]", sa == [6, 8, 4, 2, 7, 1, 9, 5, 3], str(sa))
check("Bonus: given array is wrong, entries 2 and 4 swapped",
      given != sa and [i for i in range(9) if given[i] != sa[i]] == [2, 3])
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
