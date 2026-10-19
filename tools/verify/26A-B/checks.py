# -*- coding: utf-8 -*-
"""26A-B (algorithms-1): NO KEY, every item is held as no-key. Almost nothing printed in the exam is checkable by
script (Q2/Q3 are abstract claims, Q4 has no example). These are reference facts for the solver, not answers.
Run: PYTHONUTF8=1 py tools/verify/26A-B/checks.py   (ASCII output)"""
import itertools

# Q1a: n=6, p_i = 5*i km, f = p_6 = 30; nights at hotels 2 and 4 -> days of 10, 10, 10 km, effort d^2 per day
p = [5 * i for i in range(1, 7)]
stops = [0, p[1], p[3], p[5]]
print("FACT  Q1a total effort for nights at p2 and p4:", sum((b - a) ** 2 for a, b in zip(stops, stops[1:])))


# Q2b reference: possible DFS-tree depths of a small directed graph from s (all neighbour orders)
def all_dfs_depths(adj, s):
    res = set()
    nodes = list(adj)
    for perm in itertools.product(*[list(itertools.permutations(adj[n])) for n in nodes]):
        order = dict(zip(nodes, perm))
        depth, seen = {s: 0}, {s}

        def go(u):
            for v in order[u]:
                if v not in seen:
                    seen.add(v)
                    depth[v] = depth[u] + 1
                    go(v)
        go(s)
        res.add(max(depth.values()))
    return res


adj = {"s": ["a", "b"], "a": ["b"], "b": []}
print("FACT  directed s->a, s->b, a->b: DFS tree depths from s over all neighbour orders:", sorted(all_dfs_depths(adj, "s")))
