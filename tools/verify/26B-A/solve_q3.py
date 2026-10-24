# -*- coding: utf-8 -*-
"""Solver checks for 26B-A Q3 (BFS claim, BFS vs DFS trees, MST after decreasing a tree edge). ASCII output.
Run: PYTHONUTF8=1 py tools/verify/26B-A/solve_q3.py"""
import itertools, random
from collections import deque
import networkx as nx

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


def bfs(adj, s):
    """CLRS BFS; returns parent map and, for each dequeued u, the set of white vertices at that moment."""
    color = {v: "W" for v in adj}
    par = {s: None}
    color[s] = "G"
    Q = deque([s])
    white_at = {}
    while Q:
        u = Q.popleft()
        white_at[u] = {v for v in adj if color[v] == "W"}
        for v in adj[u]:
            if color[v] == "W":
                color[v] = "G"
                par[v] = u
                Q.append(v)
        color[u] = "B"
    return par, white_at


def dfs(adj, s):
    par = {s: None}

    def visit(u):
        for v in adj[u]:
            if v not in par:
                par[v] = u
                visit(v)
    visit(s)
    return par


def tree_edges(par):
    return {frozenset((v, p)) for v, p in par.items() if p is not None}


def is_desc(par, v, u):
    while v is not None:
        if v == u:
            return True
        v = par[v]
    return False


# ---- Q3a counterexample: 5-cycle s-u-x-v-w-s, neighbours of s in the order u, w
adj = {"s": ["u", "w"], "u": ["s", "x"], "w": ["s", "v"], "x": ["u", "v"], "v": ["x", "w"]}
par, white = bfs(adj, "s")
G = nx.Graph([(a, b) for a in adj for b in adj[a]])
cond = "v" in white["u"] and nx.has_path(G.subgraph(["u"] + sorted(white["u"])), "u", "v")
check("Q3a: when u is dequeued v is white and a path u-x-v of white vertices exists", cond)
check("Q3a: v's BFS parent is w, so v is not a descendant of u", par["v"] == "w" and not is_desc(par, "v", "u"))

# printed example (4-cycle) for completeness
adj4 = {"s": ["u", "w"], "u": ["s", "v"], "w": ["s", "v"], "v": ["u", "w"]}
p4, _ = bfs(adj4, "s")
check("Q3a printed example: v is a child of u", p4["v"] == "u")


# ---- Q3b: exhaustive over small connected graphs, s on a cycle, every neighbour order
def orders(G):
    nodes = sorted(G.nodes())
    for perms in itertools.product(*[list(itertools.permutations(sorted(G[v]))) for v in nodes]):
        yield dict(zip(nodes, [list(p) for p in perms]))


def cycle_vertices(G):
    # v lies on a cycle iff some incident edge is not a bridge
    bridges = {frozenset(e) for e in nx.bridges(G)}
    return {v for v in G if any(frozenset((v, x)) not in bridges for x in G[v])}


def random_order(G):
    return {v: random.sample(sorted(G[v]), len(G[v])) for v in G}


random.seed(3)
graphs = counter = 0
for n in range(3, 7):
    for edges in itertools.chain.from_iterable(itertools.combinations(itertools.combinations(range(n), 2), m)
                                               for m in range(n, n * (n - 1) // 2 + 1)):
        G = nx.Graph(list(edges))
        if G.number_of_nodes() != n or not nx.is_connected(G):
            continue
        if n == 6 and random.random() > 0.15:
            continue
        for s in cycle_vertices(G):
            graphs += 1
            adjs = orders(G) if n <= 4 else (random_order(G) for _ in range(30))
            for adj in adjs:
                if tree_edges(bfs(adj, s)[0]) == tree_edges(dfs(adj, s)):
                    counter += 1
check("Q3b: T_BFS != T_DFS (n<=4 every neighbour order; n=5,6 30 random orders), s on a cycle",
      counter == 0, "(%d graph/source pairs)" % graphs)

# and the claim fails if s is NOT on a cycle (shows the hypothesis matters): path a-s-b plus triangle away from s
H = nx.Graph([("s", "a"), ("a", "b"), ("b", "c"), ("c", "a")])
same = any(tree_edges(bfs(adj, "s")[0]) == tree_edges(dfs(adj, "s")) for adj in orders(H))
print("INFO  s not on the cycle: some order gives equal trees =", same)


# ---- Q3c: decrease a tree edge by 1 -> T stays the (unique) MST
def all_msts(G):
    n = G.number_of_nodes()
    best, trees = None, []
    for es in itertools.combinations(G.edges(data="weight"), n - 1):
        H = nx.Graph([(a, b) for a, b, _ in es])
        if H.number_of_nodes() == n and nx.is_tree(H):
            w = sum(x for _, _, x in es)
            k = frozenset(frozenset((a, b)) for a, b, _ in es)
            if best is None or w < best:
                best, trees = w, [k]
            elif w == best:
                trees.append(k)
    return trees


random.seed(7)
bad = trials = 0
for _ in range(400):
    n = random.randint(3, 6)
    G = nx.gnp_random_graph(n, 0.7, seed=random.randint(0, 10 ** 6))
    if not nx.is_connected(G):
        continue
    ws = random.sample(range(1, 3 * G.number_of_edges() + 2), G.number_of_edges())
    for (a, b), w in zip(G.edges(), ws):
        G[a][b]["weight"] = w
    T = all_msts(G)
    assert len(T) == 1
    for e in T[0]:
        a, b = tuple(e)
        G2 = G.copy()
        G2[a][b]["weight"] -= 1
        trials += 1
        if all_msts(G2) != T:
            bad += 1
check("Q3c: after decreasing any MST edge by 1, T is still the unique MST", bad == 0, "(%d trials)" % trials)

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
