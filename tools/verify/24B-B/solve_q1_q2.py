# -*- coding: utf-8 -*-
"""Solver checks for 24B-B Q1 (BFS/DFS edge sets, directed) and Q2a (Huffman frequencies of c, d).
Run: PYTHONUTF8=1 py tools/verify/24B-B/solve_q1_q2.py   (ASCII output)"""
import itertools, heapq
import networkx as nx

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


def bfs_edges(n, adj, s):
    seen, q, out = {s}, [s], set()
    while q:
        u = q.pop(0)
        for v in adj[u]:
            if v not in seen:
                seen.add(v); out.add((u, v)); q.append(v)
    return out


def dfs_edges(n, adj, order):
    seen, out = set(), set()

    def visit(u):
        seen.add(u)
        for v in adj[u]:
            if v not in seen:
                out.add((u, v)); visit(v)
    for r in order:
        if r not in seen:
            visit(r)
    return out


# ---- Q1: exhaustive over all directed graphs on n<=4 vertices, s=0, every DFS root order and two adjacency orders
cnt = {"a": 0, "b": 0, "c": 0}
cex = {"a": None, "b": None, "c": None}
for n in range(2, 5):
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v]
    for mask in range(1, 1 << len(pairs)):
        E = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        G = nx.DiGraph(); G.add_nodes_from(range(n)); G.add_edges_from(E)
        root = len(nx.descendants(G, 0)) == n - 1
        indeg = [G.in_degree(x) for x in range(n)]; outdeg = [G.out_degree(x) for x in range(n)]
        cond_b = all(indeg[x] and outdeg[x] for x in range(n))
        cond_c = all(indeg[x] + outdeg[x] for x in range(n))
        for rev in (False, True):
            adj = {u: sorted(G.successors(u), reverse=rev) for u in range(n)}
            eb = bfs_edges(n, adj, 0)
            for perm in itertools.permutations(range(1, n)):
                ed = dfs_edges(n, adj, (0,) + perm)
                if ed == eb and not root:
                    cnt["a"] += 1; cex["a"] = cex["a"] or E
                    if cond_b: cnt["b"] += 1; cex["b"] = cex["b"] or E
                    if cond_c: cnt["c"] += 1; cex["c"] = cex["c"] or E
check("Q1a false: equal edge sets with s not a root occur", cnt["a"] > 0, str(cex["a"]))
check("Q1b true: no graph with in/out-degree>0 everywhere has equal sets and s not a root (n<=4, all orders)",
      cnt["b"] == 0)
check("Q1c false: counterexamples with deg+ + deg- > 0 exist", cnt["c"] > 0, str(cex["c"]))
# the counterexample used in the solution: s->a, b->s  (0=s, 1=a, 2=b)
adj = {0: [1], 1: [], 2: [0]}
check("Q1a/Q1c solution example s->a, b->s: E_BFS = E_DFS = {s->a}, b unreachable",
      bfs_edges(3, adj, 0) == dfs_edges(3, adj, (0, 1, 2)) == {(0, 1)} == dfs_edges(3, adj, (0, 2, 1)))

# Q1b argument on random larger graphs: if U (unreachable from s) is nonempty and every vertex has in-degree>0,
# the DFS forest has an edge inside U.
import random
random.seed(1)
bad = 0; tested = 0
for _ in range(3000):
    n = random.randint(3, 9)
    G = nx.gnp_random_graph(n, random.uniform(0.1, 0.5), directed=True, seed=random.randint(0, 10**9))
    if not all(G.in_degree(x) for x in G): continue
    R = nx.descendants(G, 0) | {0}
    if len(R) == n: continue
    tested += 1
    adj = {u: list(G.successors(u)) for u in G}
    order = [0] + random.sample(range(1, n), n - 1)
    ed = dfs_edges(n, adj, order)
    if not any(u not in R and v not in R for u, v in ed): bad += 1
check("Q1b lemma: in-degree>0 everywhere and U nonempty => DFS tree edge inside U", bad == 0 and tested > 50,
      "tested=%d" % tested)


# ---- Q2a: derive the (c,d) set by the hand argument and compare with an exhaustive Huffman search
def hand(c, d):
    x = c + d
    return c >= 1 and c <= d and d <= 4 and 4 <= x <= 7 and x + 4 <= 14


def huffman_shapes(ws):
    out = set()

    def rec(items):
        if len(items) == 1:
            out.add(items[0][1]); return
        items = sorted(items, key=lambda t: t[0])
        w1, w2 = items[0][0], items[1][0]
        for i, j in itertools.combinations(range(len(items)), 2):
            if sorted([items[i][0], items[j][0]]) != [w1, w2]: continue
            rest = [t for k, t in enumerate(items) if k not in (i, j)]
            rec(rest + [(items[i][0] + items[j][0], frozenset([items[i][1], items[j][1]]))])
    rec([(w, l) for l, w in ws.items()])
    return out


target = frozenset([frozenset(["b", frozenset(["c", "d"])]), frozenset(["a", "e"])])
brute = []
for c in range(1, 20):
    for d in range(1, 20):
        ws = {"a": 7, "b": 4, "e": 7, "c": c, "d": d}
        if target in huffman_shapes(ws) and c <= d and 4 <= c + d and 4 + c + d <= 14:
            brute.append((c, d))
handset = [(c, d) for c in range(1, 20) for d in range(1, 20) if hand(c, d)]
check("Q2a hand conditions == exhaustive Huffman search", brute == handset, str(handset))
check("Q2a answer set", handset == [(1, 3), (1, 4), (2, 2), (2, 3), (2, 4), (3, 3), (3, 4)])
# with zero allowed only (0,4) would join
z = [(c, d) for c in range(0, 1) for d in range(0, 20)
     if target in huffman_shapes({"a": 7, "b": 4, "e": 7, "c": c, "d": d}) and c <= d and 4 <= c + d <= 10]
print("     (if c=0 were allowed:", z, ")")
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
