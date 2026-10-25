# -*- coding: utf-8 -*-
"""Learn-brief checks: mst (brief 07). Every claim of the brief is checked against brute force over spanning trees.
Run: PYTHONUTF8=1 py tools/verify/learn/v05_mst.py     (ASCII output, exits 1 on a failure)"""
import itertools, random, sys

import networkx as nx

ok = True
INF = float("inf")


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


random.seed(777)


def spanning_trees(n, edges):
    """all spanning trees as tuples of edge indices (brute force)"""
    out = []
    for comb in itertools.combinations(range(len(edges)), n - 1):
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(edges[i][:2] for i in comb)
        if nx.is_connected(G):
            out.append(comb)
    return out


def all_msts(n, edges):
    trees = spanning_trees(n, edges)
    w = lambda t: sum(edges[i][2] for i in t)
    best = min(w(t) for t in trees)
    return [t for t in trees if w(t) == best], best, trees


def rand_connected(n, extra, distinct=False, wmax=5):
    es = set()
    for v in range(1, n):
        es.add((random.randrange(v), v))
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n) if (u, v) not in es]
    random.shuffle(pairs)
    es |= set(pairs[:extra])
    es = sorted(es)
    if distinct:
        ws = random.sample(range(1, 40), len(es))
    else:
        ws = [random.randint(1, wmax) for _ in es]
    return [(u, v, w) for (u, v), w in zip(es, ws)]


def kruskal(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    tree = []
    for i in sorted(range(len(edges)), key=lambda i: (edges[i][2], i)):
        a, b = find(edges[i][0]), find(edges[i][1])
        if a != b:
            parent[a] = b
            tree.append(i)
    return tree


def prim_orders(n, edges, root):
    """all insertion orders of Prim (every tie allowed): sets of tuples of edge indices"""
    adj = {v: [] for v in range(n)}
    for i, (u, v, w) in enumerate(edges):
        adj[u].append((v, w, i))
        adj[v].append((u, w, i))
    res = set()

    def go(intree, seq):
        if len(intree) == n:
            res.add(tuple(seq))
            return
        cand = [(w, i, v) for u in intree for (v, w, i) in adj[u] if v not in intree]
        m = min(c[0] for c in cand)
        for w, i, v in cand:
            if w == m:
                go(intree | {v}, seq + [i])
    go(frozenset([root]), [])
    return res


# ---- Kruskal == brute force optimum; the cut property; uniqueness for distinct weights
bad = bad2 = bad3 = 0
for _ in range(300):
    n = random.randint(2, 7)
    E = rand_connected(n, random.randint(0, 6), distinct=random.random() < 0.5)
    msts, best, trees = all_msts(n, E)
    kt = kruskal(n, E)
    bad += sum(E[i][2] for i in kt) != best
    if len({e[2] for e in E}) == len(E):
        bad2 += len(msts) != 1
    # cut property: for every cut, a lightest crossing edge lies in some MST; a strictly lightest one lies in all
    S = set(random.sample(range(n), random.randint(1, n - 1)))
    cross = [i for i, (u, v, w) in enumerate(E) if (u in S) != (v in S)]
    if cross:
        m = min(E[i][2] for i in cross)
        lights = [i for i in cross if E[i][2] == m]
        bad3 += not any(any(i in t for t in msts) for i in lights)
        if len(lights) == 1:
            bad3 += not all(lights[0] in t for t in msts)
check("Kruskal weight == brute-force MST weight (300 random)", bad == 0)
check("distinct weights => unique MST (300 random)", bad2 == 0)
check("cut property: a lightest crossing edge is in some MST, a unique lightest one in all (300 random)", bad3 == 0)

# ---- cycle property + "e in every MST iff every cycle through it has a strictly heavier edge"
bad = bad2 = bad3 = 0
for _ in range(300):
    n = random.randint(3, 7)
    E = rand_connected(n, random.randint(1, 6), distinct=False, wmax=4)
    msts, best, trees = all_msts(n, E)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i, (u, v, w) in enumerate(E):
        G.add_edge(u, v, w=w, i=i)
    for i, (u, v, w) in enumerate(E):
        in_all = all(i in t for t in msts)
        in_some = any(i in t for t in msts)
        # path from u to v in G - e using only edges of weight <= w  <=> a cycle through e where e is a weakly heaviest edge
        H = nx.Graph()
        H.add_nodes_from(range(n))
        H.add_edges_from((a, b) for j, (a, b, ww) in enumerate(E) if j != i and ww <= w)
        weak = nx.has_path(H, u, v)
        H2 = nx.Graph()
        H2.add_nodes_from(range(n))
        H2.add_edges_from((a, b) for j, (a, b, ww) in enumerate(E) if j != i and ww < w)
        strict = nx.has_path(H2, u, v)  # every... exists a cycle where e is strictly the heaviest
        # reading: e in all MSTs  iff  no cycle through e has e as a weakly heaviest edge
        bad += in_all != (not weak)
        # reading: e in no MST   iff  e is strictly heaviest on some cycle
        bad2 += (not in_some) != strict
check("e is in EVERY MST iff every cycle through e contains an edge strictly heavier than e (300 random, with ties)", bad == 0)
check("e is in NO MST iff e is the strictly heaviest edge of some cycle (300 random, with ties)", bad2 == 0)

# ---- bottleneck: every MST is an MBST ; the converse fails (triangle 1,2,2)
bad = 0
for _ in range(300):
    n = random.randint(2, 7)
    E = rand_connected(n, random.randint(0, 6), distinct=False, wmax=5)
    msts, best, trees = all_msts(n, E)
    bott = lambda t: max(E[i][2] for i in t)
    mb = min(bott(t) for t in trees)
    bad += any(bott(t) != mb for t in msts)
check("every MST is a minimum bottleneck spanning tree (300 random)", bad == 0)
tri = [(0, 1, 1), (0, 2, 2), (1, 2, 2)]
msts, best, trees = all_msts(3, tri)
bott = lambda t: max(tri[i][2] for i in t)
mbst = [t for t in trees if bott(t) == min(bott(x) for x in trees)]
check("triangle 1,2,2: MST weight 3 (one edge of weight 1), but the tree {2,2} (weight 4) is also an MBST", best == 3 and len(mbst) == 3 and any(sum(tri[i][2] for i in t) == 4 for t in mbst), (len(msts), len(mbst)))

# ---- counting spanning trees: K3, K4 - e, K4
K3 = [(0, 1, 1), (0, 2, 1), (1, 2, 1)]
K4e = [(0, 1, 1), (0, 2, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1)]
K4 = K4e + [(0, 3, 1)]
check("equal weights: #MSTs = #spanning trees: K3 -> 3, K4 minus an edge -> 8, K4 -> 16",
      len(all_msts(3, K3)[0]) == 3 and len(all_msts(4, K4e)[0]) == 8 and len(all_msts(4, K4)[0]) == 16)
check("no simple graph on 3 vertices has more than 3 spanning trees", max(len(spanning_trees(3, [e for e, keep in zip(K3, m) if keep])) for m in itertools.product((0, 1), repeat=3)) == 3)

# ---- special edges (26A-A Q2): complete graph, distinct weights
bad = bad2 = 0
for _ in range(200):
    n = random.randint(3, 7)
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    ws = random.sample(range(1, 100), len(pairs))
    E = [(u, v, w) for (u, v), w in zip(pairs, ws)]
    T = {tuple(sorted(E[i][:2])) for i in kruskal(n, E)}
    low = {x: min((w, (min(u, v), max(u, v))) for u, v, w in E if x in (u, v)) for x in range(n)}
    special = {low[x][1] for x in range(n)}
    bad += not special <= T
    if n >= 4:
        pass
check("special edge (lightest at some endpoint) belongs to the MST of a complete graph with distinct weights (200 random)", bad == 0)
K4w = [(0, 1, 1), (2, 3, 2), (1, 2, 3), (0, 2, 4), (0, 3, 5), (1, 3, 6)]  # A=0,B=1,C=2,D=3
T = {tuple(sorted(K4w[i][:2])) for i in kruskal(4, K4w)}
low = {x: min((w, (min(u, v), max(u, v))) for u, v, w in K4w if x in (u, v))[1] for x in range(4)}
check("26A-A Q2a family: K4 with AB=1, CD=2, BC=3: MST {AB,CD,BC}, weight 6, and BC is not special", T == {(0, 1), (2, 3), (1, 2)} and (1, 2) not in set(low.values()) and sum(w for u, v, w in K4w if (u, v) in T) == 6)

# ---- the heaviest edge e1 (24B-A Q3b) : in an MST iff it is a bridge
bad = 0
for _ in range(300):
    n = random.randint(3, 7)
    E = rand_connected(n, random.randint(0, 5), distinct=True)
    e1 = max(range(len(E)), key=lambda i: E[i][2])
    G = nx.Graph([E[i][:2] for i in range(len(E))])
    G.add_nodes_from(range(n))
    G.remove_edge(*E[e1][:2])
    bridge = not nx.is_connected(G)
    msts = all_msts(n, E)[0]
    bad += any(e1 in t for t in msts) != bridge
check("strictly heaviest edge is in the MST iff it is a bridge (300 random)", bad == 0)

# ---- DFS that always follows the lightest edge is not an MST (25B-A Q1a): triangle cb=2, ca=3, ab=9, start at c
a_, b_, c_ = 0, 1, 2
W = {frozenset((c_, b_)): 2, frozenset((c_, a_)): 3, frozenset((a_, b_)): 9}


def light_dfs(start):
    seen, tree = {start}, []

    def go(u):
        cand = sorted((W[frozenset((u, v))], v) for v in range(3) if v != u)
        for w, v in cand:
            if v not in seen:
                seen.add(v)
                tree.append((u, v, w))
                go(v)
    go(start)
    return tree


t = light_dfs(c_)
mst = all_msts(3, [(0, 1, 9), (0, 2, 3), (1, 2, 2)])
check("lightest-edge DFS from c: tree {cb,ba} = 11, MST = 5", sum(w for _, _, w in t) == 11 and mst[1] == 5, t)

# ---- decreasing the weight of a tree edge by 1 keeps the tree optimal (26B-A Q3c)
bad = 0
for _ in range(300):
    n = random.randint(2, 7)
    E = rand_connected(n, random.randint(0, 6), distinct=True)
    T = set(kruskal(n, E))
    e = random.choice(sorted(T))
    E2 = [(u, v, w - 1 if i == e else w) for i, (u, v, w) in enumerate(E)]
    msts, best, trees = all_msts(n, E2)
    bad += not all(tuple(sorted(t)) == tuple(sorted(T)) or False for t in msts) or len(msts) != 1 and not any(tuple(sorted(t)) == tuple(sorted(T)) for t in msts)
    bad += not any(tuple(sorted(t)) == tuple(sorted(T)) for t in msts)
check("lowering the weight of an MST edge by 1: the same tree is still an MST (300 random)", bad == 0)

# ---- reverse-delete (26A-B Q3): examine edges from heaviest to lightest, delete when the graph stays connected
def reverse_delete(n, edges):
    keep = set(range(len(edges)))
    for i in sorted(range(len(edges)), key=lambda i: -edges[i][2]):
        H = nx.Graph()
        H.add_nodes_from(range(n))
        H.add_edges_from(edges[j][:2] for j in keep if j != i)
        if nx.is_connected(H):
            keep.discard(i)
    return keep

bad = 0
for _ in range(300):
    n = random.randint(2, 7)
    E = rand_connected(n, random.randint(0, 6), distinct=True)
    rd = reverse_delete(n, E)
    bad += len(rd) != n - 1 or rd != set(kruskal(n, E))
check("reverse-delete returns the MST (n-1 edges, distinct weights) (300 random)", bad == 0)

# ---- Prim: the sequence of weights is not sorted; ties allowed (brief example P1: A..F = 0..5)
P1 = [(0, 1, 2), (0, 2, 2), (1, 2, 3), (1, 3, 4), (2, 4, 4), (3, 4, 1), (3, 5, 5), (4, 5, 3)]
msts, best, trees = all_msts(6, P1)
check("example graph P1: MST weight 12, exactly 2 MSTs (BD or CE completes the tree)", best == 12 and len(msts) == 2, (best, len(msts)))
orders = prim_orders(6, P1, 0)
wseqs = {tuple(P1[i][2] for i in o) for o in orders}
check("Prim from A on P1 can output the weight sequence 2,2,4,1,3 (not sorted)", (2, 2, 4, 1, 3) in wseqs, sorted(wseqs))
check("every Prim run ends in one of the two MSTs", {tuple(sorted(o)) for o in orders} == {tuple(sorted(t)) for t in msts})
check("Kruskal weights on P1 are sorted: 1,2,2,3,4", sorted(P1[i][2] for i in kruskal(6, P1)) == [1, 2, 2, 3, 4] and [P1[i][2] for i in kruskal(6, P1)] == sorted(P1[i][2] for i in kruskal(6, P1)))

# ---- the worked example: A..H = 0..7 ; X is the weight of (D,F)
def g26(X):
    return [(2, 0, 2), (2, 1, 3), (2, 3, 1), (3, 5, X), (3, 4, 4), (4, 5, 5), (2, 5, 9), (4, 6, 2), (6, 7, 3), (7, 5, 4)]

best_x = 0
for X in range(1, 12):
    E = g26(X)
    msts, best, trees = all_msts(8, E)
    if all(3 in t for t in msts) or False:
        pass
    df = 3
    if all(df in t for t in msts):
        best_x = X
check("example graph: the largest integer X for which (D,F) is in EVERY MST is 3", best_x == 3)
E = g26(4)
msts, best, trees = all_msts(8, E)
check("X=4: some MST avoids (D,F)", any(3 not in t for t in msts))
E = g26(3)
msts, best, trees = all_msts(8, E)
check("X=3: exactly two MSTs, both of weight 18", len(msts) == 2 and best == 18)
names = "ABCDEFGH"
ords = prim_orders(8, g26(3), 2)
named = {tuple(names[E[i][0]] + names[E[i][1]] for i in o) for o in ords}
as_sets = {tuple(sorted(o)) for o in ords}
check("Prim from C: 4 possible insertion orders, 2 resulting trees", len(ords) == 4 and len(as_sets) == 2, len(ords))
# C-D, C-A first in every order
check("in every order the first two edges are (C,D) then (C,A)", all(o[0] == 2 and o[1] == 0 for o in ords))

# ---- bank example 24A-C Q5: a Prim weight sequence need not be monotone, and a tie can place 9 before 8 ...
sys.exit(0 if ok else 1)
