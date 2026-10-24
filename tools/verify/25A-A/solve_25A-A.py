# -*- coding: utf-8 -*-
"""Solver checks for the held items of 25A-A. Run: PYTHONUTF8=1 py tools/verify/25A-A/solve_25A-A.py
Q1c (r-th smallest by binary search), Q2a (corrected recurrence), Q4a (pi[n]), bonus a/b. ASCII output."""
import itertools, random
from functools import lru_cache

ok = True
INF = float("inf")


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


random.seed(25)

# ---------- Q1c: r-th smallest of A u B, binary search on how many come from A ----------
def find_r(A, B, r):
    """A, B: 1-indexed (index 0 unused), sorted, length m each; 1 <= r <= m. Returns (value, iterations)."""
    m = len(A) - 1
    a = lambda t: -INF if t == 0 else (INF if t > r else A[t])
    b = lambda t: -INF if t == 0 else (INF if t > r else B[t])
    lo, hi, it = 0, r, 0
    while lo <= hi:
        it += 1
        i = (lo + hi) // 2
        j = r - i
        if a(i + 1) < b(j):
            lo = i + 1
        elif b(j + 1) < a(i):
            hi = i - 1
        else:
            return max(a(i), b(j)), it
    raise AssertionError("no split found")


bad = 0
maxit = {}
for _ in range(6000):
    m = random.choice([1, 2, 4, 8, 16, 32, 64])
    vals = random.sample(range(1, 1000), 2 * m)
    A, B = sorted(vals[:m]), sorted(vals[m:])
    r = random.randint(1, m)
    v, it = find_r([0] + A, [0] + B, r)
    if v != sorted(A + B)[r - 1]:
        bad += 1
    maxit[r] = max(maxit.get(r, 0), it)
check("Q1c binary search returns the r-th smallest of the union (6000 random)", bad == 0, "bad=%d" % bad)
import math
check("Q1c iterations <= floor(log2(r+1))+1 (Theta(log r))",
      all(it <= math.floor(math.log2(r + 1)) + 1 for r, it in maxit.items()))
check("Q1c the counterexample of the held key: A=[1,2], B=[3,4], r=2 -> 2", find_r([0, 1, 2], [0, 3, 4], 2)[0] == 2)

# ---------- Q2a: corrected recurrence ----------
def brute(s1, s2, s3):
    if len(s3) != len(s1) + len(s2):
        return False
    n = len(s3)
    for pos in itertools.combinations(range(n), len(s1)):
        if "".join(s3[p] for p in pos) == s1 and "".join(s3[p] for p in range(n) if p not in pos) == s2:
            return True
    return False


def corrected(s1, s2, s3):
    @lru_cache(None)
    def T(i, j, k):
        if i == j == k == 0:
            return True
        if i > 0 and j > 0 and k > 0:
            e1, e2 = s1[i - 1] == s3[k - 1], s2[j - 1] == s3[k - 1]
            if e1 and e2:
                return T(i - 1, j, k - 1) or T(i, j - 1, k - 1)
            if e1:
                return T(i - 1, j, k - 1)
            if e2:
                return T(i, j - 1, k - 1)       # fixed: k-1
            return False                         # added row
        if i > 0 and k > 0 and j == 0:
            return T(i - 1, j, k - 1) if s1[i - 1] == s3[k - 1] else False
        if j > 0 and k > 0 and i == 0:
            return T(i, j - 1, k - 1) if s2[j - 1] == s3[k - 1] else False   # fixed: k-1
        return False                             # otherwise (k = 0 < i+j, or i = j = 0 < k)
    return T(len(s1), len(s2), len(s3))


bad = 0
for _ in range(4000):
    s1 = "".join(random.choice("ab") for _ in range(random.randint(0, 4)))
    s2 = "".join(random.choice("ab") for _ in range(random.randint(0, 4)))
    L = len(s1) + len(s2) + random.choice([0, 0, 0, -1, 1])
    s3 = "".join(random.choice("ab") for _ in range(max(0, L)))
    if corrected(s1, s2, s3) != brute(s1, s2, s3):
        bad += 1
check("Q2a corrected recurrence == brute force (4000 random, incl. wrong lengths)", bad == 0, "bad=%d" % bad)
check("Q2a the four examples of the question",
      corrected("abc", "def", "adbcef") and corrected("abc", "dec", "adbcec")
      and not corrected("abc", "def", "bdacef") and not corrected("abc", "def", "adbce"))

# ---------- Q4a: longest proper border = pi[n] ----------
def pi_table(P):
    pi = [0] * len(P)
    k = 0
    for i in range(1, len(P)):
        while k and P[i] != P[k]:
            k = pi[k - 1]
        if P[i] == P[k]:
            k += 1
        pi[i] = k
    return pi


def border_brute(S):
    return max(L for L in range(0, len(S)) if S[:L] == S[len(S) - L:])


bad = 0
for _ in range(4000):
    S = "".join(random.choice("ab") for _ in range(random.randint(1, 14)))
    if pi_table(S)[-1] != border_brute(S):
        bad += 1
check("Q4a pi[n] == longest proper prefix that is also a suffix (4000 random)", bad == 0, "bad=%d" % bad)
check("Q4a max(pi) is wrong: abcabcd has max(pi)=3, border 0",
      max(pi_table("abcabcd")) == 3 and pi_table("abcabcd")[-1] == 0 == border_brute("abcabcd"))
check("Q4a examples: aabcdaabc -> pi[n]=4, aaaa -> pi[n]=3 (4 only under the literal reading |S|)",
      pi_table("aabcdaabc")[-1] == 4 and pi_table("aaaa")[-1] == 3)

# ---------- bonus b: leaves of the DFS forest are exactly the v with F[v] = D[v] + 1 ----------
def dfs_forest(n, adj):
    D, F, P = [0] * n, [0] * n, [None] * n
    t = [0]
    color = [0] * n

    def visit(u):
        t[0] += 1
        D[u] = t[0]
        color[u] = 1
        for v in range(n):
            if adj[u][v] and color[v] == 0:
                P[v] = u
                visit(v)
        t[0] += 1
        F[u] = t[0]
    for u in range(n):
        if color[u] == 0:
            visit(u)
    return D, F, P


bad = 0
for _ in range(1500):
    n = random.randint(1, 9)
    directed = random.random() < 0.5
    adj = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if u != v and random.random() < 0.3:
                adj[u][v] = 1
                if not directed:
                    adj[v][u] = 1
    D, F, P = dfs_forest(n, adj)
    leaves = {v for v in range(n) if v not in set(P)}
    if leaves != {v for v in range(n) if F[v] == D[v] + 1}:
        bad += 1
check("bonus b: leaves of Pi == {v : F[v] = D[v]+1} (1500 random graphs, matrix DFS)", bad == 0, "bad=%d" % bad)

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
