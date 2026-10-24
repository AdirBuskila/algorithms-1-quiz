# -*- coding: utf-8 -*-
"""Verification harness for 24A-B (algorithms-1), a graded student paper (refuter step). Run:
PYTHONUTF8=1 py tools/verify/24A-B/checks.py   ASCII output. Checks the transcribed student answers; never edits them."""
import itertools, random
from collections import deque
import networkx as nx

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


random.seed(5)
INF = float("inf")

# ---------- Q1: walks x -> y through the set A (some vertex of A on the walk), undirected graph ----------
def bfs(G, s):
    d = {u: INF for u in G}
    d[s] = 0
    dq = deque([s])
    while dq:
        a = dq.popleft()
        for b in G[a]:
            if d[b] == INF:
                d[b] = d[a] + 1
                dq.append(b)
    return d


def student_exists(G, A, x, y):
    dx = bfs(G, x)
    if dx[y] == INF:
        return False
    return any(dx[v] != INF for v in A)


def student_min(G, A, x, y):
    dx = bfs(G, x)
    if dx[y] == INF:
        return INF
    dy = bfs(G, y)
    m = INF
    for v in A:
        if dx[v] + dy[v] < m:
            m = dx[v] + dy[v]
    return m


def ref_min_walk(G, A, x, y):  # BFS on states (vertex, visitedA)
    start = (x, x in A)
    dist = {start: 0}
    dq = deque([start])
    while dq:
        v, f = dq.popleft()
        for w in G[v]:
            s = (w, f or w in A)
            if s not in dist:
                dist[s] = dist[(v, f)] + 1
                dq.append(s)
    return dist.get((y, True), INF)


bad = 0
for _ in range(3000):
    n = random.randint(3, 9)
    G = nx.gnp_random_graph(n, random.random() * 0.5, seed=random.randint(0, 10**6))
    verts = list(G)
    x, y = random.sample(verts, 2)
    rest = [v for v in verts if v not in (x, y)]
    A = set(random.sample(rest, random.randint(1, len(rest))))
    r = ref_min_walk(G, A, x, y)
    if student_min(G, A, x, y) != r or student_exists(G, A, x, y) != (r != INF):
        bad += 1
check("Q1a/b student algorithms == product-graph BFS reference (3000 graphs, x,y not in A)", bad == 0)

# ---------- Q2: minimum number of tapes, barrels closed in order, leftovers of an old tape are discarded ----------
def next_fit(ls, m):
    count, rem = 0, 0
    for l in ls:
        if l <= rem:
            rem -= l
        else:
            count += 1
            rem = m - l
    return count


def dp_groups(ls, m):  # minimum number of consecutive groups with sum <= m
    n = len(ls)
    best = [0] + [INF] * n
    for i in range(1, n + 1):
        s = 0
        for j in range(i, 0, -1):
            s += ls[j - 1]
            if s > m:
                break
            best[i] = min(best[i], best[j - 1] + 1)
    return best[n]


check("Q2 example lengths 2,1,4,2 with m=5 needs 3 tapes", next_fit([2, 1, 4, 2], 5) == 3 == dp_groups([2, 1, 4, 2], 5))
bad = 0
for _ in range(5000):
    m = random.randint(3, 15)
    ls = [random.randint(1, m) for _ in range(random.randint(1, 12))]
    if next_fit(ls, m) != dp_groups(ls, m):
        bad += 1
check("Q2a student greedy (use the current tape if it fits, else a new one) == DP optimum (5000 inputs)", bad == 0)

# ---------- Q3: bit counts of the Karp-Rabin message ----------
from math import ceil, log2
check("Q3b q <= n^2 and z < q need ceil(log2(n^2)) bits each: 2*ceil(log2 n^2) total, for n=2..1000",
      all(2 * ceil(log2(n * n)) == 2 * (n * n - 1).bit_length() for n in range(2, 1001)))
# repetition: independent runs multiply the error probability
check("Q3c k independent runs with single-run error p0 <= 1/2 give p0^k <= 1/4 for k=2", all(p ** 2 <= 0.25 for p in (0.01, 0.25, 0.5)))

# ---------- Q4: n coloured dice, number of outcomes with sum m ----------
def T(i, j, memo={}):
    if (i, j) in memo:
        return memo[(i, j)]
    if i == 0:
        r = 1 if j == 0 else 0
    elif j <= 0:
        r = 0
    else:
        r = sum(T(i - 1, j - k) for k in range(1, 7) if j - k >= 0)
    memo[(i, j)] = r
    return r


def brute(n, m):
    return sum(1 for t in itertools.product(range(1, 7), repeat=n) if sum(t) == m)


check("Q4 example n=2, m=3 -> 2 outcomes", T(2, 3) == 2 == brute(2, 3))
check("Q4a recurrence (full base cases T(0,0)=1, T(0,j>0)=0, T(i,0)=0) == brute force for n<=6, m<=40",
      all(T(n, m) == brute(n, m) for n in range(1, 7) for m in range(0, 41)))


def rolling(n, m):  # O(m) space, two rows
    prev = [1] + [0] * m
    for _ in range(n):
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            cur[j] = sum(prev[j - k] for k in range(1, 7) if j - k >= 0)
        prev = cur
    return prev[m]


check("Q4b two-row table (O(m) space) gives the same counts as the full n x m table", all(rolling(n, m) == T(n, m) for n in range(1, 9) for m in range(1, 45)))

# ---------- Bonus: shortest-first interval scheduling is not optimal ----------
iv = [(0, 10), (9, 12), (11, 20)]
shortest = min(iv, key=lambda a: a[1] - a[0])
greedy_sel = [shortest] + [a for a in iv if a[1] <= shortest[0] or a[0] >= shortest[1]]
best = max(k for k in range(1, 4) for c in itertools.combinations(iv, k)
           if all(a[1] <= b[0] or b[1] <= a[0] for a, b in itertools.combinations(c, 2)))
check("Bonus shortest-first is not optimal on [0,10],[9,12],[11,20] (greedy 1, optimum 2)", len(greedy_sel) == 1 and best == 2)

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
