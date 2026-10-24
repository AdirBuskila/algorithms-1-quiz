# -*- coding: utf-8 -*-
"""Solver checks for 26A-B (no key). Every claim in the solved items is tested here.
Run: PYTHONUTF8=1 py tools/verify/26A-B/solve_all.py   (ASCII output, exit 1 on any failure)"""
import itertools, random
import networkx as nx

random.seed(26)
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


# ---------------------------------------------------------------- Q1: hotels DP
INF = float("inf")


def dp_hotels(p, t):
    """p = [p_1..p_n] (p_n = f). OPT(i,j) = min effort to reach p_i in at most j days (p_0 = 0)."""
    n = len(p)
    P = [0] + list(p)
    opt = [[INF] * (t + 1) for _ in range(n + 1)]
    for j in range(t + 1):
        opt[0][j] = 0
    for j in range(1, t + 1):
        for i in range(1, n + 1):
            opt[i][j] = min(opt[l][j - 1] + (P[i] - P[l]) ** 2 for l in range(i))
    return opt[n][t]


def brute_hotels(p, t):
    n = len(p)
    best = INF
    for r in range(0, t):  # r intermediate nights among hotels 1..n-1 -> r+1 days <= t
        for stops in itertools.combinations(range(1, n), r):
            pts = [0] + [p[s - 1] for s in stops] + [p[-1]]
            best = min(best, sum((b - a) ** 2 for a, b in zip(pts, pts[1:])))
    return best


bad = 0
for _ in range(3000):
    n = random.randint(2, 8)
    p = sorted(random.sample(range(1, 40), n))
    t = random.randint(1, n - 1)
    if dp_hotels(p, t) != brute_hotels(p, t):
        bad += 1
check("Q1b recurrence OPT(n,t) == brute force over all night choices (3000 random)", bad == 0)
p6 = [5 * i for i in range(1, 7)]
check("Q1a nights at p2, p4 with 5 km spacing -> 10^2+10^2+10^2 = 300",
      sum((b - a) ** 2 for a, b in zip([0, 10, 20, 30], [10, 20, 30, 30][:3])) == 300)
check("Q1a also the optimum for t=3 on that route (300)", dp_hotels(p6, 3) == 300)
# exactly-t is enough because effort is convex: more days never hurts when t < n
bad = 0
for _ in range(1000):
    n = random.randint(2, 8)
    p = sorted(random.sample(range(1, 40), n))
    for t in range(1, n - 1):
        if dp_hotels(p, t + 1) > dp_hotels(p, t):
            bad += 1
check("Q1 extra: OPT is non-increasing in t", bad == 0)


# ---------------------------------------------------------------- Q2a: BFS tree depth = eccentricity of s
def bfs_tree_depth(G, s, order):
    from collections import deque
    d = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in sorted(G.neighbors(u), key=lambda x: order[x]):
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return max(d.values())


bad = 0
for _ in range(500):
    n = random.randint(2, 9)
    G = nx.gnp_random_graph(n, 0.4, seed=random.randint(0, 10 ** 6))
    if not nx.is_connected(G):
        continue
    ecc = nx.eccentricity(G, 0)
    for _ in range(10):
        order = {v: random.random() for v in G}
        if bfs_tree_depth(G, 0, order) != ecc:
            bad += 1
check("Q2a every BFS tree from s has depth = max distance from s (random undirected, random orders)", bad == 0)


# ---------------------------------------------------------------- Q2b: DFS depth can differ (directed)
def dfs_depths(adj, s):
    res = set()
    nodes = list(adj)
    for perm in itertools.product(*[list(itertools.permutations(adj[x])) for x in nodes]):
        order = dict(zip(nodes, perm))
        depth = {s: 0}

        def go(u):
            for v in order[u]:
                if v not in depth:
                    depth[v] = depth[u] + 1
                    go(v)
        go(s)
        res.add(max(depth.values()))
    return res


check("Q2b counterexample s->a, s->b, a->b: DFS depths {1,2}", dfs_depths({"s": ["a", "b"], "a": ["b"], "b": []}, "s") == {1, 2})


# ---------------------------------------------------------------- Q3: reverse-delete
def reverse_delete(G):
    H = G.copy()
    for u, v, w in sorted(G.edges(data="weight"), key=lambda e: -e[2]):
        H.remove_edge(u, v)
        if not nx.is_connected(H):
            H.add_edge(u, v, weight=w)
    return H


bad_cnt = bad_tree = bad_mst = bad_cycle = 0
for _ in range(800):
    n = random.randint(2, 9)
    G = nx.gnp_random_graph(n, 0.5, seed=random.randint(0, 10 ** 6))
    if not nx.is_connected(G):
        continue
    ws = random.sample(range(1, 1000), G.number_of_edges())
    for (u, v), w in zip(G.edges(), ws):
        G[u][v]["weight"] = w
    T = reverse_delete(G)
    bad_cnt += T.number_of_edges() != n - 1
    bad_tree += not nx.is_tree(T)
    M = nx.minimum_spanning_tree(G)
    bad_mst += set(map(frozenset, T.edges())) != set(map(frozenset, M.edges()))
    # cycle property used in 3c: every removed edge is the heaviest edge on some cycle of G
    for u, v, w in G.edges(data="weight"):
        if not T.has_edge(u, v):
            lighter = nx.Graph([(a, b) for a, b, x in G.edges(data="weight") if x < w])
            lighter.add_nodes_from(G)
            bad_cycle += not nx.has_path(lighter, u, v)
check("Q3a T has exactly n-1 edges (random connected graphs, distinct weights)", bad_cnt == 0)
check("Q3b T is a spanning tree", bad_tree == 0)
check("Q3c T equals the (unique) MST", bad_mst == 0)
check("Q3c every removed edge closes a cycle of lighter edges (cycle property)", bad_cycle == 0)


# ---------------------------------------------------------------- Q4: k-th smallest with SELECT on <= n/2
def solve_q4(A, k):
    n = len(A)
    calls = []

    def SELECT(B, i):  # black box; record the size it is called on
        calls.append(len(B))
        assert 2 * len(B) <= n, "SELECT called on more than n/2 elements"
        return sorted(B)[i - 1]

    C = list(A)
    while 2 * len(C) > n:
        if len(C) == 1:  # only possible when n = 1 (excluded by k < n/2)
            return C[0], calls
        C1 = C[:len(C) // 2]
        p = SELECT(C1, (len(C1) + 1) // 2)
        L = [x for x in C if x < p]
        E = [x for x in C if x == p]
        R = [x for x in C if x > p]
        if k <= len(L):
            C = L
        elif k <= len(L) + len(E):
            return p, calls
        else:
            k -= len(L) + len(E)
            C = R
    if not C:
        raise AssertionError
    return SELECT(C, k), calls


bad = worst = 0
for _ in range(20000):
    n = random.randint(1, 60)
    A = [random.randint(0, 30) for _ in range(n)] if random.random() < 0.3 else random.sample(range(1000), n)
    for k in range(1, n + 1):  # also k >= n/2: the method does not need k < n/2
        x, calls = solve_q4(A, k)
        if x != sorted(A)[k - 1]:
            bad += 1
        worst = max(worst, len(calls))
check("Q4 result == sorted(A)[k-1] for all k, SELECT only on <= n/2 elements (20000 arrays, with duplicates)", bad == 0,
      "max SELECT calls %d" % worst)
# shrink bound: each loop round keeps at most 3N/4 + 1 elements
bad = 0
for _ in range(3000):
    N = random.randint(2, 400)
    C = random.sample(range(10000), N)
    C1 = C[:N // 2]
    p = sorted(C1)[(len(C1) + 1) // 2 - 1]
    side = max(sum(x < p for x in C), sum(x > p for x in C))
    if 4 * side > 3 * N + 4:
        bad += 1
check("Q4 one round keeps at most 3N/4 + 1 elements", bad == 0)


# ---------------------------------------------------------------- bonus
def prefix(P):
    pi = [0] * len(P)
    k = 0
    for q in range(1, len(P)):
        while k and P[k] != P[q]:
            k = pi[k - 1]
        if P[k] == P[q]:
            k += 1
        pi[q] = k
    return pi


check("Bonus a: pi(aa)=[0,1] and pi(a^5) ends with m-1=4", prefix("aa") == [0, 1] and prefix("aaaaa")[-1] == 4)


def kmp_inner_count(T, P):
    pi = prefix(P)
    q = cnt = 0
    for c in T:
        while q and P[q] != c:
            q = pi[q - 1]
            cnt += 1
        if P[q] == c:
            q += 1
        if q == len(P):
            q = pi[q - 1]
    return cnt


check("Bonus b: P=a^m, T=b^n -> the KMP fall-back loop never runs", kmp_inner_count("b" * 50, "a" * 7) == 0)


def naive_ops(T, P):
    n, m = len(T), len(P)
    return (n - m + 1) * m


check("Bonus c: naive (n-m+1)m is linear for m=1 and for m=n", naive_ops("x" * 100, "x") == 100 and naive_ops("x" * 100, "x" * 100) == 100)

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
