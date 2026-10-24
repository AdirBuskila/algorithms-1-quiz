# Q3b remark: in a connected simple graph that contains a cycle, T_BFS != T_DFS from EVERY source (also a leaf), for
# every neighbour order.  Exhaustive over all labelled graphs with n <= 4 (all sources, all adjacency orders) plus random
# larger graphs / orders.
import itertools
import random


def bfs_edges(adj, s):
    seen = {s}
    q = [s]
    E = set()
    for u in q:
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
                E.add(frozenset((u, v)))
    return E


def dfs_edges(adj, s):
    seen = {s}
    E = set()

    def go(u):
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                E.add(frozenset((u, v)))
                go(v)
    go(s)
    return E


def connected(n, edges):
    adj = {i: [] for i in range(n)}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return len(bfs_edges(adj, 0)) == n - 1


cases = 0
for n in (3, 4):
    allE = list(itertools.combinations(range(n), 2))
    for k in range(n, len(allE) + 1):                     # >= n edges and connected => has a cycle
        for edges in itertools.combinations(allE, k):
            if not connected(n, edges):
                continue
            base = {i: [] for i in range(n)}
            for a, b in edges:
                base[a].append(b)
                base[b].append(a)
            orders = [list(itertools.permutations(base[i])) for i in range(n)]
            for choice in itertools.product(*orders):
                adj = {i: list(choice[i]) for i in range(n)}
                for s in range(n):
                    assert bfs_edges(adj, s) != dfs_edges(adj, s), (edges, s, adj)
                    cases += 1
random.seed(9)
for _ in range(20000):
    n = random.randint(4, 9)
    allE = list(itertools.combinations(range(n), 2))
    edges = random.sample(allE, random.randint(n, min(len(allE), n + 6)))
    if not connected(n, edges):
        continue
    adj = {i: [] for i in range(n)}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    for i in adj:
        random.shuffle(adj[i])
    for s in range(n):
        assert bfs_edges(adj, s) != dfs_edges(adj, s), (edges, s, adj)
        cases += 1
print("T_BFS != T_DFS in all", cases, "checked (graph, order, source) cases, sources that are leaves included")
