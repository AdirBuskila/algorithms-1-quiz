# -*- coding: utf-8 -*-
"""Solver checks for 25A-B (algorithms-1). Every algorithm written in the solutions of gen_25A-B.py is transcribed
here and tested against a brute force (and networkx for the graph bonus). ASCII output.
Run: PYTHONUTF8=1 py tools/verify/25A-B/solve_25AB.py"""
import heapq, itertools, random
from collections import Counter, deque

import networkx as nx

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


random.seed(2025)

# ---------------------------------------------------------------- Q1 (largest all-zero square)
M0 = [[0, 1, 1, 0, 1, 1],
      [0, 0, 1, 0, 0, 0],
      [1, 0, 0, 0, 0, 0],
      [1, 1, 0, 0, 0, 1],
      [1, 1, 0, 0, 0, 0]]


def T_table(M):  # the recurrence of the solution, 0-based
    n, m = len(M), len(M[0])
    T = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if M[i][j] == 1:
                T[i][j] = 0
            elif i == 0 or j == 0:
                T[i][j] = 1
            else:
                T[i][j] = 1 + min(T[i - 1][j], T[i][j - 1], T[i - 1][j - 1])
    return T


def T_brute(M, i, j):
    best = 0
    for s in range(1, min(i, j) + 2):
        if all(M[a][b] == 0 for a in range(i - s + 1, i + 1) for b in range(j - s + 1, j + 1)):
            best = s
    return best


T = T_table(M0)
EXPECT_1A = [[1, 0, 0, 1, 0, 0],
             [1, 1, 0, 1, 1, 1],
             [0, 1, 1, 1, 2, 2],
             [0, 0, 1, 2, 2, 0],
             [0, 0, 1, 2, 3, 1]]
check("Q1a table as written in the solution", T == EXPECT_1A, str(T))
check("Q1a T(4,4)=3 and max=3", T[4][4] == 3 and max(map(max, T)) == 3)
bad = 0
for _ in range(400):
    n, m = random.randint(1, 6), random.randint(1, 6)
    M = [[1 if random.random() < 0.3 else 0 for _ in range(m)] for _ in range(n)]
    TT = T_table(M)
    bad += any(TT[i][j] != T_brute(M, i, j) for i in range(n) for j in range(m))
check("Q1b recurrence equals brute force on 400 random 0/1 matrices", bad == 0)


# ---------------------------------------------------------------- Q2 (reduce string value)
def value(s):
    return sum(c * c for c in Counter(s).values())


def greedy_string(S, k):  # transcription of the solution: heap of (-freq, letter), then one scan
    f = Counter(S)
    h = [(-c, ch) for ch, c in f.items()]
    heapq.heapify(h)
    r = Counter()
    for _ in range(k):
        c, ch = heapq.heappop(h)
        r[ch] += 1
        heapq.heappush(h, (c + 1, ch))
    out = []
    for ch in S:
        if r[ch] > 0:
            r[ch] -= 1
        else:
            out.append(ch)
    return "".join(out)


def brute_min(S, k):
    best = None
    for rem in itertools.combinations(range(len(S)), k):
        v = value("".join(S[i] for i in range(len(S)) if i not in rem))
        best = v if best is None or v < best else best
    return best


g = greedy_string("character", 2)
check("Q2 example: value(character)=15, greedy keeps length 7 with value 9 = optimum", value("character") == 15 and
      len(g) == 7 and value(g) == 9 == brute_min("character", 2) and value("charter") == 9, g)
bad = 0
for _ in range(500):
    S = "".join(random.choice("abcd") for _ in range(random.randint(2, 10)))
    k = random.randint(1, len(S) - 1)
    G = greedy_string(S, k)
    sub_ok = all(Counter(G)[c] <= Counter(S)[c] for c in Counter(G))  # S' is S minus k letters (order kept by scan)
    it = iter(S)
    is_subseq = all(ch in it for ch in G)
    bad += not (len(G) == len(S) - k and is_subseq and sub_ok and value(G) == brute_min(S, k))
check("Q2a greedy string is a k-deletion of S with optimal value (500 random)", bad == 0)


# the proof's identity: x^2 = sum_{j=1..x}(2j-1); the k largest terms of the multiset are what greedy removes
def terms_bound(S, k):
    allterms = sorted((2 * j - 1 for c in Counter(S).values() for j in range(1, c + 1)), reverse=True)
    return value(S) - sum(allterms[:k])


check("Q2b proof: optimum = value(S) - (sum of the k largest terms 2j-1) (500 random)",
      all(terms_bound(S, k) == brute_min(S, k) for S, k in
          ((s, random.randint(1, len(s) - 1)) for s in
           ("".join(random.choice("abc") for _ in range(random.randint(2, 9))) for _ in range(500)))))


# ---------------------------------------------------------------- Q3 (inversions)
def inv_brute(A):
    return sum(1 for i in range(len(A)) for j in range(i + 1, len(A)) if A[i] > A[j])


def sort_count(A):  # transcription of the solution pseudocode
    if len(A) <= 1:
        return A[:], 0
    mid = len(A) // 2
    L, x = sort_count(A[:mid])
    R, y = sort_count(A[mid:])
    out, z, i, j = [], 0, 0, 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1; z += len(L) - i
    out += L[i:] + R[j:]
    return out, x + y + z


check("Q3 example [30,10,40,20] -> 3", sort_count([30, 10, 40, 20])[1] == 3)
check("Q3 sorted -> 0, reversed n=6 -> 15", sort_count(list(range(6)))[1] == 0 and sort_count(list(range(6, 0, -1)))[1] == 15)
check("Q3a merge counting equals brute force with duplicates (800 random)",
      all(sort_count(A)[1] == inv_brute(A) and sort_count(A)[0] == sorted(A)
          for A in ([random.randint(1, 6) for _ in range(random.randint(0, 12))] for _ in range(800))))


# ---------------------------------------------------------------- Q4 (almost match), Z-function as in the solution
def zfun(s):
    L = len(s)
    Z = [0] * L
    if L:
        Z[0] = L
    l = r = 0
    steps = 0
    for k in range(1, L):
        Z[k] = min(r - k, Z[k - l]) if k < r else 0
        while k + Z[k] < L and s[Z[k]] == s[k + Z[k]]:
            Z[k] += 1
            steps += 1
        if k + Z[k] > r:
            l, r = k, k + Z[k]
    return Z, steps


def almost(T_, P):
    n, m = len(T_), len(P)
    Z1, s1 = zfun(P + "#" + T_)
    Z2, s2 = zfun(P[::-1] + "#" + T_[::-1])
    pre = [Z1[m + 1 + i] for i in range(n)]
    suf = [Z2[m + 1 + (n - 1 - e)] for e in range(n)]
    out = [i + 1 for i in range(n - m + 1) if pre[i] >= m or pre[i] + suf[i + m - 1] >= m - 1]
    return out, s1 + s2


def almost_naive(T_, P):
    m = len(P)
    return [i + 1 for i in range(len(T_) - m + 1) if sum(a != b for a, b in zip(T_[i:i + m], P)) <= 1]


check("Q4 example pair differs in exactly one place", sum(a != b for a, b in zip("aababa", "aaaaba")) == 1)
bad = 0
maxratio = 0
for _ in range(3000):
    t = "".join(random.choice("ab") for _ in range(random.randint(2, 18)))
    p = "".join(random.choice("ab") for _ in range(random.randint(1, len(t) - 1)))
    res, st = almost(t, p)
    bad += res != almost_naive(t, p)
    maxratio = max(maxratio, st / (len(t) + len(p) + 1))
check("Q4a Z-based algorithm equals naive (3000 random, alphabet ab)", bad == 0)
check("Q4b successful while-loop comparisons <= 2(n+m+1) overall", maxratio <= 2, "max ratio %.2f" % maxratio)
_, st = almost("a" * 2000, "a" * 999)
check("Q4b worst case a^n / a^m: comparisons linear", st <= 2 * 3000, str(st))


# ---------------------------------------------------------------- Q5 bonus (a, c)
def bfs_bipartite(n, adj):
    col = [-1] * n
    for s in range(n):
        if col[s] != -1:
            continue
        col[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if col[v] == -1:
                    col[v] = 1 - col[u]; q.append(v)
                elif col[v] == col[u]:
                    return False
    return True


def bfs_connected(n, adj):
    seen = [False] * n
    seen[0] = True
    q = deque([0])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True; q.append(v)
    return all(seen)


bad_a = bad_c = 0
for _ in range(600):
    n = random.randint(1, 9)
    G = nx.gnp_random_graph(n, random.choice([0.15, 0.3, 0.5]), seed=random.randint(0, 10 ** 6))
    adj = [list(G.neighbors(v)) for v in range(n)]
    bad_a += bfs_bipartite(n, adj) != nx.is_bipartite(G)
    bad_c += bfs_connected(n, adj) != nx.is_connected(G)
check("Q5a BFS 2-colouring decides bipartiteness = networkx (600 random graphs)", bad_a == 0)
check("Q5c one BFS decides connectivity = networkx (600 random graphs)", bad_c == 0)

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
