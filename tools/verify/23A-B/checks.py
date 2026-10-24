# -*- coding: utf-8 -*-
r"""Verification harness for 23A-B (algorithms-1). Run: PYTHONUTF8=1 py tools/verify/23A-B/checks.py
Checks the official answers (never modifies them). ASCII output."""
import itertools, heapq, random, json, pathlib
from collections import Counter
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


# ---------- Q1: snake path in a 2-D array ----------
def brute_snake(A):
    n = len(A)
    best = 0
    # longest path ending at (i,j) by exhaustive DFS from every start (right/down only, |diff|<=1)

    def dfs(i, j):
        r = 1
        for ni, nj in ((i, j + 1), (i + 1, j)):
            if ni < n and nj < n and abs(A[i][j] - A[ni][nj]) <= 1:
                r = max(r, 1 + dfs(ni, nj))
        return r
    for i in range(n):
        for j in range(n):
            best = max(best, dfs(i, j))
    return best


def official_T(A):
    """Official recurrence of the solution page, transcribed case by case (1-indexed, T=0 outside)."""
    n = len(A)
    a = lambda i, j: A[i - 1][j - 1]
    memo = {}

    def T(i, j):
        if i == 0 or j == 0:
            return 0
        if (i, j) in memo:
            return memo[(i, j)]
        left = (j > 1) and abs(a(i, j) - a(i, j - 1)) <= 1   # can step from the left cell
        up = (i > 1) and abs(a(i, j) - a(i - 1, j)) <= 1     # can step from the upper cell
        if i == 1 and j == 1:
            r = 1
        elif not left and not up:
            r = 1
        elif up and not left:
            r = 1 + T(i - 1, j)
        elif left and not up:
            r = 1 + T(i, j - 1)
        else:
            r = 1 + max(T(i - 1, j), T(i, j - 1))
        memo[(i, j)] = r
        return r
    return max(T(i, j) for i in range(1, n + 1) for j in range(1, n + 1))


# the page-2 example: gray path 1,2,2,1 of length 4 (cells (1,2),(2,2),(3,2),(3,3))
EX = [[10, 1, 3], [12, 2, 2], [1, 2, 1]]
check("Q1 example array: longest snake = 4", brute_snake(EX) == 4 == official_T(EX))
# 1a official 5x5 answer: path 7,8,8,9 from A[2,3] to A[4,4]
M = [[10, 20, 30, 40, 50], [20, 10, 7, 20, 40], [30, 20, 8, 8, 30], [40, 30, 20, 9, 20], [50, 40, 30, 20, 30]]
path = [M[1][2], M[2][2], M[2][3], M[3][3]]
check("Q1a official 5x5: A[2,3]=7, A[4,4]=9, path 7,8,8,9 valid",
      path == [7, 8, 8, 9] and all(abs(path[k] - path[k + 1]) <= 1 for k in range(3)))


def longest_between(A, s, t):
    n = len(A)
    best = [0]

    def dfs(i, j, ln):
        if (i, j) == t:
            best[0] = max(best[0], ln)
            return
        for ni, nj in ((i, j + 1), (i + 1, j)):
            if ni < n and nj < n and ni <= t[0] and nj <= t[1] and abs(A[i][j] - A[ni][nj]) <= 1:
                dfs(ni, nj, ln + 1)
    dfs(s[0], s[1], 1)
    return best[0]


check("Q1a official 5x5: longest snake from (2,3) to (4,4) is 4 (every monotone route has 4 cells)",
      longest_between(M, (1, 2), (3, 3)) == 4)
random.seed(7)
bad = 0
for _ in range(4000):
    n = random.randint(1, 6)
    A = [[random.randint(0, 4) for _ in range(n)] for _ in range(n)]
    if brute_snake(A) != official_T(A):
        bad += 1
check("Q1b official recurrence equals brute force on 4000 random arrays", bad == 0, "mismatches=%d" % bad)

# ---------- Q2: GPT detection ----------
# 2a: a model that is right on exactly half of the n questions is exposed by ANY n/2+1 questions (pigeonhole)
exposed_all = True
for n in (2, 4, 6, 8):
    for good in itertools.combinations(range(n), n // 2):
        for qs in itertools.combinations(range(n), n // 2 + 1):
            if all(q in good for q in qs):
                exposed_all = False
check("Q2a pigeonhole: n/2+1 questions always include a wrong answer of a half-right model", exposed_all)

# 2b: Monte Carlo with k random questions: a half-right model survives with probability <= (1/2)^k
random.seed(3)
n, k, trials = 40, 5, 60000
survive = 0
for _ in range(trials):
    right = set(random.sample(range(n), n // 2))
    qs = random.sample(range(n), k)
    if all(q in right for q in qs):
        survive += 1
p = survive / trials
check("Q2b survival probability of a half-right model with k=5 is <= (1/2)^5", p <= 0.5 ** 5 + 0.004,
      "measured=%.4f bound=%.4f" % (p, 0.5 ** 5))

# 2c: Las Vegas: expected number of random questions until a half-right model is exposed is about 2
random.seed(5)
n, trials, tot = 40, 40000, 0
for _ in range(trials):
    right = set(random.sample(range(n), n // 2))
    c = 0
    while True:
        c += 1
        if random.randrange(n) not in right:
            break
    tot += c
check("Q2c expected questions to expose a half-right model is about 2 (geometric)", abs(tot / trials - 2.0) < 0.05,
      "mean=%.3f" % (tot / trials))

# ---------- Q3a: frequencies of all 4-mers via the (generalized) suffix tree idea ----------
random.seed(11)
words = ["".join(random.choice("ACGT") for _ in range(50)) for _ in range(60)]
truth = Counter(w[i:i + 4] for w in words for i in range(len(w) - 3))
text = "".join(w + "$%d$" % (i + 1) for i, w in enumerate(words))   # a distinct terminator after each word
# suffix-tree leaves under the first node of depth >= 4 with no terminator inside the first 4 characters
cnt = Counter()
for s in range(len(text)):
    pre = text[s:s + 4]
    if len(pre) == 4 and all(c in "ACGT" for c in pre):
        cnt[pre] += 1
check("Q3a counting suffixes by their 4-prefix (terminators excluded) equals the true 4-mer counts", cnt == truth)


# ---------- Q3b: pattern found under a letter permutation ----------
def brute_perm(T, P):
    res = []
    m = len(P)
    for s in range(len(T) - m + 1):
        for perm in itertools.permutations("abc"):
            f = dict(zip("abc", perm))
            if all(T[s + t] == f[P[t]] for t in range(m)):
                res.append(s)
                break
    return res


def kmp_all(T, P):
    m = len(P)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k and P[k] != P[q]:
            k = pi[k - 1]
        if P[k] == P[q]:
            k += 1
        pi[q] = k
    out, k = [], 0
    for i, ch in enumerate(T):
        while k and (k == m or P[k] != ch):
            k = pi[k - 1]
        if P[k] == ch:
            k += 1
        if k == m:
            out.append(i - m + 1)
    return out


def official_perm(T, P):
    hits = set()
    for perm in itertools.permutations("abc"):   # the six patterns of the official solution
        f = dict(zip("abc", perm))
        hits.update(kmp_all(T, "".join(f[c] for c in P)))
    return sorted(hits)


random.seed(13)
bad = 0
for _ in range(3000):
    m = random.randint(1, 5)
    n = random.randint(m + 1, 14)
    P = "".join(random.choice("abc") for _ in range(m))
    T = "".join(random.choice("abc") for _ in range(n))
    if brute_perm(T, P) != official_perm(T, P):
        bad += 1
check("Q3b six KMP runs (one per letter permutation) equal brute force on 3000 random cases", bad == 0, "mismatches=%d" % bad)


# ---------- Q4a: optimal prefix-code cost 13 ----------
def huff_cost(freqs):
    h = list(freqs)
    heapq.heapify(h)
    tot = 0
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        tot += a + b
        heapq.heappush(h, a + b)
    return tot


check("Q4a option 2: f=(3,2,1,1) has optimal cost 13", huff_cost([3, 2, 1, 1]) == 13)
check("Q4a option 1: f=(13,0,0,0) has optimal cost 13 but violates f>0 printed in the question", huff_cost([13, 0, 0, 0]) == 13)
for name, fr, codes in (("opt1", (13, 0, 0, 0), ("1", "01", "001", "000")), ("opt2", (3, 2, 1, 1), ("1", "01", "001", "000"))):
    prefix_free = not any(a != b and b.startswith(a) for a in codes for b in codes)
    cost = sum(f * len(c) for f, c in zip(fr, codes))
    check("Q4a %s official code is prefix-free and costs 13" % name, prefix_free and cost == 13)
# the official option 2 code is optimal: no assignment of 4 frequencies to any complete code beats 13
best = min(sum(f * l for f, l in zip(sorted((3, 2, 1, 1), reverse=True), lens))
           for lens in ((1, 2, 3, 3), (2, 2, 2, 2)))
check("Q4a option 2: 13 is the minimum over the two complete 4-leaf tree shapes", best == 13)

# ---------- Q4b: smallest graph with >= 5 minimum spanning trees ----------


def n_spanning(G):
    # Kirchhoff matrix-tree theorem via networkx/numpy-free exact integer determinant
    nodes = list(G.nodes())
    n = len(nodes)
    if n == 1:
        return 1
    idx = {v: i for i, v in enumerate(nodes)}
    L = [[0] * n for _ in range(n)]
    for u, v in G.edges():
        i, j = idx[u], idx[v]
        L[i][i] += 1
        L[j][j] += 1
        L[i][j] -= 1
        L[j][i] -= 1
    M = [row[1:] for row in L[1:]]
    from fractions import Fraction
    M = [[Fraction(x) for x in row] for row in M]
    det = Fraction(1)
    m = len(M)
    for c in range(m):
        p = next((r for r in range(c, m) if M[r][c] != 0), None)
        if p is None:
            return 0
        if p != c:
            M[c], M[p] = M[p], M[c]
            det = -det
        det *= M[c][c]
        for r in range(c + 1, m):
            f = M[r][c] / M[c][c]
            for k in range(c, m):
                M[r][k] -= f * M[c][k]
    return int(det)


# all simple graphs on 1..3 vertices have at most 3 spanning trees
mx3 = 0
for nv in (1, 2, 3):
    pairs = list(itertools.combinations(range(nv), 2))
    for r in range(len(pairs) + 1):
        for es in itertools.combinations(pairs, r):
            G = nx.Graph()
            G.add_nodes_from(range(nv))
            G.add_edges_from(es)
            if nx.is_connected(G):
                mx3 = max(mx3, n_spanning(G))
check("Q4b every graph on <=3 vertices has at most 3 spanning trees (so >=5 needs 4 vertices)", mx3 == 3)
# the official drawing: 4 vertices TL,TR,BL,BR, edges TL-TR, TL-BL, TL-BR, TR-BR, BL-BR, all weights 1
G = nx.Graph()
G.add_weighted_edges_from([("TL", "TR", 1), ("TL", "BL", 1), ("TL", "BR", 1), ("TR", "BR", 1), ("BL", "BR", 1)])
nst = n_spanning(G)
brute = sum(1 for es in itertools.combinations(G.edges(), 3) if nx.is_tree(nx.Graph(list(es))) and len(set(sum(es, ()))) == 4)
check("Q4b official drawing is K4 minus an edge with 8 spanning trees (all MSTs, equal weights)", nst == 8 == brute,
      "kirchhoff=%d brute=%d" % (nst, brute))
check("Q4b official text says '6 spanning trees': the true number is 8 (>=5 still holds; flagged)", nst != 6 and nst >= 5)
C4 = nx.cycle_graph(4)
check("Q4b a 4-cycle has only 4 spanning trees (not enough)", n_spanning(C4) == 4)

# ---------- Q5 bonus: matching-based vertex cover 2-approximation ----------


def approx_vc(G):
    E = set(frozenset(e) for e in G.edges())
    C = set()
    while E:
        e = next(iter(E))
        a, b = tuple(e)
        C |= {a, b}
        E = {x for x in E if a not in x and b not in x}
    return C


def opt_vc(G):
    V = list(G.nodes())
    for r in range(len(V) + 1):
        for S in itertools.combinations(V, r):
            s = set(S)
            if all(u in s or v in s for u, v in G.edges()):
                return r


random.seed(17)
worst, valid = 0.0, True
for _ in range(400):
    n = random.randint(2, 9)
    G = nx.gnp_random_graph(n, random.random() * 0.7 + 0.15, seed=random.randint(0, 10 ** 6))
    if G.number_of_edges() == 0:
        continue
    C = approx_vc(G)
    valid &= all(u in C or v in C for u, v in G.edges())
    o = opt_vc(G)
    worst = max(worst, len(C) / o)
check("Q5 official algorithm returns a valid vertex cover on 400 random graphs", valid)
check("Q5 approximation ratio never exceeds 2 (worst seen %.2f)" % worst, worst <= 2.0)
# a tight example: a perfect matching graph K_{n,n} ratio 2
K = nx.complete_bipartite_graph(3, 3)
check("Q5 ratio 2 is attained (K_{3,3}: cover of size 6 vs optimum 3)", len(approx_vc(K)) == 6 and opt_vc(K) == 3)

print("ALL OK" if ok else "SOME CHECK FAILED")
raise SystemExit(0 if ok else 1)
