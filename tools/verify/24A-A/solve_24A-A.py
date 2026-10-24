# -*- coding: utf-8 -*-
"""Solver checks for 24A-A Q1a, Q1b, Q4c and the bonus. Run: PYTHONUTF8=1 py tools/verify/24A-A/solve_24A-A.py
ASCII output."""
import itertools, random
from collections import deque
import networkx as nx

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


def bfs(adj, s):
    d = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return d


def walk_through(adj, x, y, z):          # Q1a: BFS from z, x and y must both be reached
    d = bfs(adj, z)
    return x in d and y in d


def shortest_through(adj, x, y, z):      # Q1b: BFS from x and from y
    dx, dy = bfs(adj, x), bfs(adj, y)
    return y in dx and z in dx and z in dy and dx[z] + dy[z] == dx[y]


def walk_brute(G, x, y, z):
    # independent reference: search the product graph (vertex, "z already visited") from (x, x==z) to (y, True)
    start = (x, x == z)
    seen = {start}
    q = deque([start])
    while q:
        u, f = q.popleft()
        if (u, f) == (y, True):
            return True
        for v in G[u]:
            st = (v, f or v == z)
            if st not in seen:
                seen.add(st)
                q.append(st)
    return False


def shortest_brute(G, x, y, z):
    if not nx.has_path(G, x, y):
        return False
    return any(z in p for p in nx.all_shortest_paths(G, x, y))


random.seed(24)
bad1 = bad2 = 0
for _ in range(3000):
    n = random.randint(1, 9)
    G = nx.gnp_random_graph(n, random.choice([0.15, 0.3, 0.5]), seed=random.randint(0, 10 ** 6))
    adj = {u: list(G[u]) for u in G}
    x, y, z = (random.randrange(n) for _ in range(3))
    bad1 += walk_through(adj, x, y, z) != walk_brute(G, x, y, z)
    bad2 += shortest_through(adj, x, y, z) != shortest_brute(G, x, y, z)
check("Q1a walk x->z->y exists iff BFS from z reaches x and y (3000 random graphs)", bad1 == 0, "bad=%d" % bad1)
check("Q1b some shortest x-y path contains z iff d(x,z)+d(z,y)=d(x,y) (3000 random graphs, all shortest paths)",
      bad2 == 0, "bad=%d" % bad2)


# ---------- Q4c: tower DP with a predecessor array, widths sorted descending ----------
def tower_with_boxes(boxes):     # boxes (w, l, h), w descending
    n = len(boxes)
    T, P = [0] * n, [-1] * n
    for i in range(n):
        T[i] = boxes[i][2]
        for j in range(i):
            if boxes[j][1] > boxes[i][1] and T[j] + boxes[i][2] > T[i]:
                T[i], P[i] = T[j] + boxes[i][2], j
    i = max(range(n), key=lambda t: T[t])
    best, out = T[i], []
    while i != -1:
        out.append(i)
        i = P[i]
    return best, out[::-1]


def brute(boxes):
    best = 0
    for r in range(1, len(boxes) + 1):
        for S in itertools.combinations(range(len(boxes)), r):
            if all(boxes[a][0] > boxes[b][0] and boxes[a][1] > boxes[b][1] for a, b in zip(S, S[1:])):
                best = max(best, sum(boxes[s][2] for s in S))
    return best


bad = 0
for _ in range(2000):
    n = random.randint(1, 8)
    ws = random.sample(range(1, 50), n)
    ls = random.sample(range(1, 50), n)
    hs = random.sample(range(1, 50), n)
    boxes = sorted(zip(ws, ls, hs), reverse=True)
    best, out = tower_with_boxes(boxes)
    stable = all(boxes[a][0] > boxes[b][0] and boxes[a][1] > boxes[b][1] for a, b in zip(out, out[1:]))
    if best != brute(boxes) or not stable or sum(boxes[i][2] for i in out) != best:
        bad += 1
check("Q4c DP + predecessor array returns a stable tower of maximal height (2000 random); time O(n^2), space O(n)",
      bad == 0, "bad=%d" % bad)


# ---------- bonus: shortest-interval-first is not optimal ----------
def shortest_first(iv):
    chosen = []
    for a, b in sorted(iv, key=lambda t: t[1] - t[0]):
        if all(b < c or d < a for c, d in chosen):
            chosen.append((a, b))
    return len(chosen)


iv = [(0, 10), (9, 12), (11, 20)]
check("bonus: shortest-first gives 1 interval on [0,10],[9,12],[11,20], the optimum is 2", shortest_first(iv) == 1)
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
