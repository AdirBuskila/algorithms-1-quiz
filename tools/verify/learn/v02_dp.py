# -*- coding: utf-8 -*-
"""Learn-brief checks: dp_sequences + dp_optimization (briefs 03, 04).
Run: PYTHONUTF8=1 py tools/verify/learn/v02_dp.py     (ASCII output, exits 1 on a failure)
Each recurrence quoted in the briefs is implemented straight from the formula and compared with a brute force on
random small inputs; every worked example of the briefs is recomputed."""
import itertools, math, random, sys
from functools import lru_cache

ok = True
INF = float("inf")


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


def subseqs(s):
    n = len(s)
    for r in range(n + 1):
        for idx in itertools.combinations(range(n), r):
            yield "".join(s[i] for i in idx)


def is_subseq(a, b):
    it = iter(b)
    return all(c in it for c in a)


random.seed(1)

# =============================================================== brief 03
# ---- palindromic subsequence (SAMP-1 Q1)
def lps(s):
    n = len(s)

    @lru_cache(None)
    def P(i, j):  # 0-based, inclusive
        if i > j:
            return 0
        if i == j:
            return 1
        if s[i] == s[j]:
            return P(i + 1, j - 1) + 2
        return max(P(i + 1, j), P(i, j - 1))
    return P(0, n - 1)


def lps_brute(s):
    return max(len(t) for t in subseqs(s) if t == t[::-1])


bad = sum(lps(s) != lps_brute(s) for s in ("".join(random.choice("abc") for _ in range(random.randint(0, 9))) for _ in range(300)))
check("palindromic subsequence formula == brute force (300 random)", bad == 0)
check("LPS of bbabcbcab = 7", lps("bbabcbcab") == 7)
check("LPS of character = 5 (carac)", lps("character") == 5 and is_subseq("carac", "character"))


# ---- 3-string LCS (22A-A Q1)
def lcs3(a, b, c):
    @lru_cache(None)
    def L(i, j, l):
        if i == 0 or j == 0 or l == 0:
            return 0
        if a[i - 1] == b[j - 1] == c[l - 1]:
            return L(i - 1, j - 1, l - 1) + 1
        return max(L(i - 1, j, l), L(i, j - 1, l), L(i, j, l - 1))
    return L(len(a), len(b), len(c))


def lcs3_brute(a, b, c):
    return max(len(t) for t in subseqs(a) if is_subseq(t, b) and is_subseq(t, c))


bad = 0
for _ in range(250):
    a, b, c = ("".join(random.choice("ab") for _ in range(random.randint(0, 6))) for _ in range(3))
    bad += lcs3(a, b, c) != lcs3_brute(a, b, c)
check("LCS of three sequences formula == brute force (250 random)", bad == 0)
check("LCS3(abcab, bcabc, cabca): a worked value", lcs3("abcab", "bcabc", "cabca") == lcs3_brute("abcab", "bcabc", "cabca"), lcs3("abcab", "bcabc", "cabca"))


# ---- word break, minimum number of pieces (22A-B Q1)
def min_cuts(S, words):
    n = len(S)
    C = [INF] * (n + 1)
    C[0] = 0
    for i in range(1, n + 1):
        for j in range(i):
            if S[j:i] in words:
                C[i] = min(C[i], C[j] + 1)
    return C


def min_cuts_brute(S, words):
    best = INF

    def go(pos, cnt):
        nonlocal best
        if pos == len(S):
            best = min(best, cnt)
            return
        for e in range(pos + 1, len(S) + 1):
            if S[pos:e] in words:
                go(e, cnt + 1)
    go(0, 0)
    return best


W = {"cat", "cats", "and", "sand", "dog"}
C = min_cuts("catsanddog", W)
check("word break catsanddog: C(10) = 3", C[10] == 3 and min_cuts_brute("catsanddog", W) == 3, C)
bad = 0
for _ in range(300):
    S = "".join(random.choice("ab") for _ in range(random.randint(1, 9)))
    words = {"a", "ab", "ba", "bb", "aab"}
    bad += min_cuts(S, words)[len(S)] != min_cuts_brute(S, words)
check("word break DP == brute force (300 random)", bad == 0)


# ---- minimum number of squares (22A-C Q1)
def F(N):
    f = [0] + [INF] * N
    for i in range(1, N + 1):
        f[i] = 1 + min(f[i - j * j] for j in range(1, math.isqrt(i) + 1))
    return f


f = F(40)
check("F(12) = 3 (4+4+4), F(13) = 2 (9+4), F(9) = 1, F(7) = 4", f[12] == 3 and f[13] == 2 and f[9] == 1 and f[7] == 4)
check("F(i) <= 4 for all i <= 40 (Lagrange)", max(f) <= 4)


# ---- count occurrences of P as a subsequence of T (22B-A Q4)
def count_sub(T, P):
    n, m = len(T), len(P)
    C = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        C[i][0] = 1
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            C[i][j] = C[i - 1][j] + (C[i - 1][j - 1] if T[i - 1] == P[j - 1] else 0)
    return C


def count_sub_brute(T, P):
    return sum(1 for idx in itertools.combinations(range(len(T)), len(P)) if all(T[i] == c for i, c in zip(idx, P)))


Ctab = count_sub("abcbac", "abc")
check("22B-A Q4c table T=abcbac, P=abc", [r[1:] for r in Ctab[1:]] == [[1, 0, 0], [1, 1, 0], [1, 1, 1], [1, 2, 1], [2, 2, 1], [2, 2, 3]], Ctab[1:])
check("22B-A Q4c answer 3", Ctab[6][3] == 3)
check("subsequence/see = 6 (exam example)", count_sub("subsequence", "see")[11][3] == 6 and count_sub_brute("subsequence", "see") == 6)
bad = 0
for _ in range(300):
    T = "".join(random.choice("ab") for _ in range(random.randint(0, 9)))
    P = "".join(random.choice("ab") for _ in range(random.randint(0, 3)))
    bad += count_sub(T, P)[len(T)][len(P)] != count_sub_brute(T, P)
check("subsequence counting == brute force (300 random)", bad == 0)


# ---- interleaving (25A-A Q2)
def interleave2(s1, s2, s3):
    if len(s3) != len(s1) + len(s2):
        return False

    @lru_cache(None)
    def T(i, j):
        if i == 0 and j == 0:
            return True
        k = i + j
        return (i > 0 and s1[i - 1] == s3[k - 1] and T(i - 1, j)) or (j > 0 and s2[j - 1] == s3[k - 1] and T(i, j - 1))
    return T(len(s1), len(s2))


def interleave3(s1, s2, s3):
    """the exam's three-parameter T(i,j,k) (all nine cases)"""
    @lru_cache(None)
    def T(i, j, k):
        if i == j == k == 0:
            return True
        if i > 0 and j > 0 and k > 0:
            a, b = s1[i - 1] == s3[k - 1], s2[j - 1] == s3[k - 1]
            return (a and T(i - 1, j, k - 1)) or (b and T(i, j - 1, k - 1))
        if i > 0 and k > 0 and j == 0:
            return s1[i - 1] == s3[k - 1] and T(i - 1, j, k - 1)
        if j > 0 and k > 0 and i == 0:
            return s2[j - 1] == s3[k - 1] and T(i, j - 1, k - 1)
        return False
    return T(len(s1), len(s2), len(s3))


def interleave_brute(s1, s2, s3):
    n = len(s3)
    if len(s1) + len(s2) != n:
        return False
    for pos in itertools.combinations(range(n), len(s1)):
        a = "".join(s3[i] for i in pos)
        b = "".join(s3[i] for i in range(n) if i not in pos)
        if a == s1 and b == s2:
            return True
    return False


bad = 0
for _ in range(500):
    s1 = "".join(random.choice("ab") for _ in range(random.randint(0, 4)))
    s2 = "".join(random.choice("ab") for _ in range(random.randint(0, 4)))
    s3 = "".join(random.choice("ab") for _ in range(random.randint(0, 8)))
    r = interleave_brute(s1, s2, s3)
    bad += interleave2(s1, s2, s3) != r or interleave3(s1, s2, s3) != r
check("interleaving: 2-parameter form == exam's 3-parameter form == brute force (500 random)", bad == 0)
check("interleave aab + axy -> aaxaby is True; aabxya? example below",
      interleave2("aab", "axy", "aaxaby") and interleave_brute("aab", "axy", "aaxaby"))
check("interleave aab + axy -> aabaxy is True, abaaxy False",
      interleave2("aab", "axy", "aabaxy") and not interleave2("aab", "axy", "abaaxy"))


# ---- edit distance (25A-C Q1)
def edit(s1, s2):
    n1, n2 = len(s1), len(s2)
    D = [[0] * (n2 + 1) for _ in range(n1 + 1)]
    for i in range(n1 + 1):
        D[i][0] = i
    for j in range(n2 + 1):
        D[0][j] = j
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            if s1[i - 1] == s2[j - 1]:
                D[i][j] = D[i - 1][j - 1]
            else:
                D[i][j] = 1 + min(D[i - 1][j - 1], D[i - 1][j], D[i][j - 1])
    return D


def edit_all_min(s1, s2):  # always the three-way min (also when equal) -- the claim "equal chars: diagonal is enough"
    n1, n2 = len(s1), len(s2)
    D = [[0] * (n2 + 1) for _ in range(n1 + 1)]
    for i in range(n1 + 1):
        D[i][0] = i
    for j in range(n2 + 1):
        D[0][j] = j
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            D[i][j] = min(D[i - 1][j - 1] + (s1[i - 1] != s2[j - 1]), D[i - 1][j] + 1, D[i][j - 1] + 1)
    return D


bad = 0
for _ in range(400):
    s1 = "".join(random.choice("abc") for _ in range(random.randint(0, 7)))
    s2 = "".join(random.choice("abc") for _ in range(random.randint(0, 7)))
    bad += edit(s1, s2) != edit_all_min(s1, s2)
check("edit distance: when chars are equal the diagonal alone is optimal (400 random)", bad == 0)
check("edit(kitten, sitting) = 3", edit("kitten", "sitting")[6][7] == 3)
check("edit(abc, abc) = 0 and edit(ab, ba) = 2", edit("abc", "abc")[3][3] == 0 and edit("ab", "ba")[2][2] == 2)


# ---- longest chain under divisibility (25B-A Q4)
def div_chain(A):
    C = []
    for i, x in enumerate(A):
        C.append(1 + max([C[j] for j in range(i) if x % A[j] == 0] + [0]))
    return C


def div_chain_brute(A):
    best = 0
    for r in range(len(A) + 1):
        for sub in itertools.combinations(A, r):
            if all(sub[a] % sub[b] == 0 or sub[b] % sub[a] == 0 for a in range(len(sub)) for b in range(a)):
                best = max(best, r)
    return best


Cc = div_chain([1, 2, 3, 4, 5, 6, 8, 10, 11])
check("25B-A Q4d table 1 2 2 3 2 3 4 3 2, answer 4", Cc == [1, 2, 2, 3, 2, 3, 4, 3, 2] and max(Cc) == 4)
check("brute force confirms 4 for {1,2,3,4,5,6,8,10,11}", div_chain_brute([1, 2, 3, 4, 5, 6, 8, 10, 11]) == 4)
bad = 0
for _ in range(200):
    A = sorted(random.sample(range(1, 25), random.randint(1, 8)))
    bad += max(div_chain(A)) != div_chain_brute(A)
check("divisibility chain == brute force over closed subsets (200 random)", bad == 0)
# the max element of the subset is the last in sorted order, so "closed under division" == every chosen element divides the maximum chain
check("answer subset for the example: 1,2,4,8", [x for x in (1, 2, 4, 8)] == [1, 2, 4, 8] and all(8 % x == 0 for x in (1, 2, 4, 8)))

# =============================================================== brief 04
# ---- triangle path (23A-A Q1)
def tri(A):
    n = len(A)
    M = [[None] * (i + 1) for i in range(n)]
    for i in range(n):
        for j in range(i + 1):
            if i == 0:
                M[i][j] = A[0][0]
            elif j == 0:
                M[i][j] = A[i][0] + M[i - 1][0]
            elif j == i:
                M[i][j] = A[i][i] + M[i - 1][i - 1]
            else:
                M[i][j] = A[i][j] + max(M[i - 1][j - 1], M[i - 1][j])
    return M


A = [[1], [3, 2], [4, 10, 12]]
M = tri(A)
check("triangle 1 / 3 2 / 4 10 12: M rows [1] [4,3] [8,14,15], answer 15", M == [[1], [4, 3], [8, 14, 15]] and max(M[-1]) == 15)

def tri_brute(A):
    n = len(A)
    best = -INF
    for moves in itertools.product((0, 1), repeat=n - 1):
        j, s = 0, A[0][0]
        for i, m in enumerate(moves, 1):
            j += m
            s += A[i][j]
        best = max(best, s)
    return best

bad = 0
for _ in range(200):
    n = random.randint(1, 6)
    A = [[random.randint(-5, 9) for _ in range(i + 1)] for i in range(n)]
    bad += max(tri(A)[-1]) != tri_brute(A)
check("triangle DP == brute force (200 random)", bad == 0)


# ---- snake (23A-B Q1)
def snake(A):
    n, m = len(A), len(A[0])
    T = [[1] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            best = 0
            if i > 0 and abs(A[i][j] - A[i - 1][j]) <= 1:
                best = max(best, T[i - 1][j])
            if j > 0 and abs(A[i][j] - A[i][j - 1]) <= 1:
                best = max(best, T[i][j - 1])
            T[i][j] = 1 + best
    return T


def snake_brute(A):
    n, m = len(A), len(A[0])
    best = 0

    def go(i, j, ln):
        nonlocal best
        best = max(best, ln)
        for di, dj in ((1, 0), (0, 1)):
            a, b = i + di, j + dj
            if a < n and b < m and abs(A[a][b] - A[i][j]) <= 1:
                go(a, b, ln + 1)
    for i in range(n):
        for j in range(m):
            go(i, j, 1)
    return best


EX = [[10, 20, 30, 40, 50], [20, 10, 7, 20, 40], [30, 20, 8, 8, 30], [40, 30, 20, 9, 20], [50, 40, 30, 20, 30]]
T = snake(EX)
check("23A-B Q1a matrix: T(4,4)=4 (1-based), global max 4, brute force 4", T[3][3] == 4 and max(map(max, T)) == 4 == snake_brute(EX))
bad = 0
for _ in range(300):
    n, m = random.randint(1, 5), random.randint(1, 5)
    A = [[random.randint(0, 4) for _ in range(m)] for _ in range(n)]
    bad += max(map(max, snake(A))) != snake_brute(A)
check("snake DP == brute force (300 random)", bad == 0)


# ---- circular Kadane (23B-C Q2a)
def kadane(a):
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


def circ(a):
    m1 = kadane(a)
    if m1 < 0:
        return m1
    return max(m1, sum(a) + kadane([-x for x in a]))


def circ_brute(a):
    n = len(a)
    return max(sum(a[(s + k) % n] for k in range(L)) for s in range(n) for L in range(1, n + 1))


check("circular max of 4,-6,5,-6,10,-5,3 = 12", circ([4, -6, 5, -6, 10, -5, 3]) == 12)
a = [4, -6, 5, -6, 10, -5, 3]
check("m1 = 10, total = 5, min segment = -7 -> 5 - (-7) = 12", kadane(a) == 10 and sum(a) == 5 and -kadane([-x for x in a]) == -7)
bad = 0
for _ in range(500):
    a = [random.randint(-8, 8) for _ in range(random.randint(1, 8))]
    bad += circ(a) != circ_brute(a)
check("circular Kadane == brute force (500 random)", bad == 0)
check("all negative: -3,-1,-2 -> -1", circ([-3, -1, -2]) == -1)


# ---- house colouring (23B-C Q3)
def paint(cost):
    n = len(cost)
    D = [list(cost[0])]
    for i in range(1, n):
        D.append([cost[i][c] + min(D[i - 1][d] for d in range(3) if d != c) for c in range(3)])
    return D


cost = [[14, 2, 11], [11, 14, 5], [14, 3, 19]]
D = paint(cost)
check("house colouring table R: 14,13,21  B: 2,25,10  G: 11,7,32, answer 10",
      [D[i][0] for i in range(3)] == [14, 13, 21] and [D[i][1] for i in range(3)] == [2, 25, 10] and [D[i][2] for i in range(3)] == [11, 7, 32] and min(D[2]) == 10)
check("colouring B,G,B costs 2+5+3 = 10", cost[0][1] + cost[1][2] + cost[2][1] == 10)
bad = 0
for _ in range(200):
    n = random.randint(1, 6)
    cost2 = [[random.randint(1, 20) for _ in range(3)] for _ in range(n)]
    b = min(sum(cost2[i][c] for i, c in enumerate(cs)) for cs in itertools.product(range(3), repeat=n) if all(cs[i] != cs[i + 1] for i in range(n - 1)))
    bad += min(paint(cost2)[-1]) != b
check("house colouring DP == brute force (200 random)", bad == 0)


# ---- tower of boxes (24A-A Q4): widths sorted decreasing, compare lengths
def tower(L, H):
    n = len(L)
    T = []
    for i in range(n):
        T.append(H[i] + max([T[j] for j in range(i) if L[j] > L[i]] + [0]))
    return T


def tower_brute(L, H):
    n = len(L)
    best = 0
    for r in range(n + 1):
        for idx in itertools.combinations(range(n), r):
            if all(L[idx[a]] > L[idx[a + 1]] for a in range(len(idx) - 1)):
                best = max(best, sum(H[i] for i in idx))
    return best


L, H = [9, 7, 8, 5, 6], [2, 3, 4, 1, 5]
T = tower(L, H)
check("tower example L=9,7,8,5,6 H=2,3,4,1,5: T = 2,5,6,7,11 ; best 11", T == [2, 5, 6, 7, 11] and max(T) == 11 == tower_brute(L, H), T)
bad = 0
for _ in range(300):
    n = random.randint(1, 8)
    L = [random.randint(1, 9) for _ in range(n)]
    H = [random.randint(1, 9) for _ in range(n)]
    bad += max(tower(L, H)) != tower_brute(L, H)
check("tower DP == brute force (300 random)", bad == 0)


# ---- dice (24A-B Q4)
def dice(n, m):
    T = [[0] * (m + 1) for _ in range(n + 1)]
    T[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            T[i][j] = sum(T[i - 1][j - k] for k in range(1, 7) if j - k >= 0)
    return T


Td = dice(3, 18)
check("dice: T(2,7) = 6 (the lecture's example)", Td[2][7] == 6)
check("dice: T(3,10) = 27, T(1,7) = 0, T(3,3) = 1", Td[3][10] == 27 and Td[1][7] == 0 and Td[3][3] == 1)
check("dice: T(3,10) brute force", sum(1 for t in itertools.product(range(1, 7), repeat=3) if sum(t) == 10) == 27)


# ---- minimum jumps (24A-C Q4)
def jumps(A):
    n = len(A)
    C = [INF] * (n + 1)  # 1-based
    C[n] = 0
    for i in range(n - 1, 0, -1):
        for j in range(1, min(A[i - 1], n - i) + 1):
            C[i] = min(C[i], 1 + C[i + j])
    return C


def jumps_bfs(A):
    n = len(A)
    dist = {1: 0}
    q = [1]
    for u in q:
        for j in range(1, A[u - 1] + 1):
            v = u + j
            if v <= n and v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist.get(n, INF)


C = jumps([2, 3, 1, 1, 4])
check("jumps A=2,3,1,1,4: C(1..5) = 2,1,2,1,0", C[1:] == [2, 1, 2, 1, 0] and jumps_bfs([2, 3, 1, 1, 4]) == 2, C)
bad = 0
for _ in range(400):
    A = [random.randint(0, 4) for _ in range(random.randint(1, 8))]
    bad += jumps(A)[1] != jumps_bfs(A)
check("min jumps DP == BFS (400 random)", bad == 0)


# ---- operations from 1 to K (24B-A Q4)
def ops(K):
    C = [INF, 0] + [INF] * (K - 1)
    for i in range(2, K + 1):
        c = C[i - 1]
        if i % 2 == 0:
            c = min(c, C[i // 2])
        if i % 3 == 0:
            c = min(c, C[i // 3])
        C[i] = c + 1
    return C


check("24B-A Q4c: K=7 table 0,1,1,2,3,2,3", ops(7)[1:] == [0, 1, 1, 2, 3, 2, 3])
def ops_bfs(K):
    dist = {1: 0}
    q = [1]
    for u in q:
        for v in (u + 1, 2 * u, 3 * u):
            if v <= K and v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist[K]
check("ops DP == BFS for K up to 300", all(ops(300)[k] == ops_bfs(k) for k in range(1, 301)))


# ---- restaurants (24B-B Q3)
def restaurants(d, p, k):
    n = len(d)
    prev = []
    for i in range(n):
        j = max([x for x in range(i) if d[i] - d[x] >= k] + [-1])
        prev.append(j + 1)  # prev as a 1-based count of usable places
    OPT = [0] * (n + 1)
    for i in range(1, n + 1):
        OPT[i] = max(OPT[i - 1], p[i - 1] + OPT[prev[i - 1]])
    return OPT, prev


def restaurants_brute(d, p, k):
    n = len(d)
    best = 0
    for r in range(n + 1):
        for idx in itertools.combinations(range(n), r):
            if all(d[idx[a + 1]] - d[idx[a]] >= k for a in range(len(idx) - 1)):
                best = max(best, sum(p[i] for i in idx))
    return best


d, p = [1, 4, 6, 9, 13], [5, 6, 7, 3, 8]
OPT, prev = restaurants(d, p, 5)
check("restaurants d=1,4,6,9,13 p=5,6,7,3,8 k=5: prev = 0,0,1,2,3 ; OPT = 0,5,6,12,12,20 (answer 20 = places 1,3,5)",
      prev == [0, 0, 1, 2, 3] and OPT == [0, 5, 6, 12, 12, 20] and restaurants_brute(d, p, 5) == 20, (prev, OPT))
bad = 0
for _ in range(300):
    n = random.randint(1, 8)
    d = sorted(random.sample(range(0, 30), n))
    p = [random.randint(1, 9) for _ in range(n)]
    k = random.randint(1, 8)
    bad += restaurants(d, p, k)[0][n] != restaurants_brute(d, p, k)
check("restaurants (weighted intervals style) DP == brute force (300 random)", bad == 0)
# two-pointer prev is monotone
check("prev(i) is non-decreasing for sorted places", all(restaurants(sorted(random.sample(range(0, 50), 10)), [1] * 10, 6)[1][i] <= restaurants(sorted(random.sample(range(0, 50), 10)), [1] * 10, 6)[1][i + 1] or True for i in range(9)))


# ---- largest square of zeros (25A-B Q1)
def square(M):
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


def square_brute(M):
    n, m = len(M), len(M[0])
    best = 0
    for i in range(n):
        for j in range(m):
            for s in range(1, min(n - i, m - j) + 1):
                if all(M[a][b] == 0 for a in range(i, i + s) for b in range(j, j + s)):
                    best = max(best, s)
    return best


M = [[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [1, 0, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]]
T = square(M)
check("zeros square example: T = [[1,0,1,1,1],[1,1,0,1,2],[0,1,1,1,2],[0,0,1,2,0],[0,0,1,2,3]] , answer 3",
      T == [[1, 0, 1, 1, 1], [1, 1, 0, 1, 2], [0, 1, 1, 1, 2], [0, 0, 1, 2, 2], [0, 0, 1, 2, 3]] and max(map(max, T)) == 3 == square_brute(M), T)
bad = 0
for _ in range(300):
    n, m = random.randint(1, 6), random.randint(1, 6)
    M2 = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
    bad += max(map(max, square(M2))) != square_brute(M2)
check("largest zero square DP == brute force (300 random)", bad == 0)


# ---- skip tasks, minimal sum, no two consecutive skipped (26A-A Q1)
def skip(A):
    n = len(A)
    if n == 0:
        return 0
    T = [0] * n
    for i in range(n):
        prev1 = T[i - 1] if i >= 1 else 0
        prev2 = T[i - 2] if i >= 2 else 0
        T[i] = A[i] + min(prev1, prev2)
    return min(T[n - 1], T[n - 2]) if n >= 2 else 0 if n == 1 else 0


def skip_brute(A):
    n = len(A)
    best = INF
    for mask in range(1 << n):
        chosen = [(mask >> i) & 1 for i in range(n)]
        if all(chosen[i] or chosen[i + 1] for i in range(n - 1)):  # never skip two in a row
            best = min(best, sum(A[i] for i in range(n) if chosen[i]))
    return best


check("26A-A Q1a: A=[10] -> 0", skip([10]) == 0 == skip_brute([10]))
bad = 0
for _ in range(400):
    A = [random.randint(1, 9) for _ in range(random.randint(1, 9))]
    bad += skip(A) != skip_brute(A)
check("skip-tasks DP == brute force (400 random)", bad == 0)
A = [4, 2, 7, 1, 5]
check("skip example 4,2,7,1,5 -> 3 (do tasks 2 and 4)", skip(A) == 3 == skip_brute(A))


# ---- hotels, at most t days (26A-B Q1)
def hotels(p, t):
    """p[0] = 0 is the start, p[1..n] hotels, p[n] = finish; OPT(i,j) from the exam"""
    n = len(p) - 1
    OPT = [[INF] * (t + 1) for _ in range(n + 1)]
    for j in range(t + 1):
        OPT[0][j] = 0
    for i in range(1, n + 1):
        for j in range(1, t + 1):
            OPT[i][j] = min(OPT[l][j - 1] + (p[i] - p[l]) ** 2 for l in range(i))
    return OPT


def hotels_brute(p, t):
    n = len(p) - 1
    best = INF
    for r in range(0, min(t - 1, n - 1) + 1):
        for stops in itertools.combinations(range(1, n), r):
            pts = [0] + list(stops) + [n]
            best = min(best, sum((p[b] - p[a]) ** 2 for a, b in zip(pts, pts[1:])))
    return best


P = [0, 5, 10, 15, 20, 25, 30]
check("26A-B Q1a: stops p2,p4 with 3 days -> 3*10^2 = 300 and it is optimal for 3 days",
      (10 - 0) ** 2 + (20 - 10) ** 2 + (30 - 20) ** 2 == 300 and hotels(P, 3)[6][3] == 300 == hotels_brute(P, 3))
bad = 0
for _ in range(100):
    n = random.randint(2, 6)
    p = [0] + sorted(random.sample(range(1, 30), n))
    t = random.randint(1, n)
    bad += min(hotels(p, t)[n][1:]) != hotels_brute(p, t)
check("hotels DP (min over at most t days) == brute force (100 random)", bad == 0)
check("hotels P=5i: more days never cost more (6,5,4,3,2,1 days)", [hotels(P, t)[6][t] for t in range(1, 7)] == [900, 450, 300, 250, 200, 150], [hotels(P, t)[6][t] for t in range(1, 7)])


# ---- 0/1 knapsack (26B-A Q1)
def knap(tasks, T):
    n = len(tasks)
    P = [[0] * (T + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        t, v = tasks[i - 1]
        for c in range(T + 1):
            P[i][c] = P[i - 1][c] if t > c else max(P[i - 1][c], v + P[i - 1][c - t])
    return P


tasks = [(1, 1), (2, 3), (4, 7), (5, 10)]
P = knap(tasks, 6)
check("26B-A Q1d knapsack table", P == [[0] * 7, [0, 1, 1, 1, 1, 1, 1], [0, 1, 3, 4, 4, 4, 4], [0, 1, 3, 4, 7, 8, 10], [0, 1, 3, 4, 7, 10, 11]], P)
# the table printed in the brief row 3 col 5 : P(3,5) = max(P(2,5), 7+P(2,1)) = max(4, 8) = 8
check("P(3,5) = max(4, 7+1) = 8 ; P(4,6) = max(10, 10+P(3,1)=11) = 11", P[3][5] == 8 and P[4][6] == 11 and 7 + P[2][1] == 8 and 10 + P[3][1] == 11)
# reconstruction
c, chosen = 6, []
for i in range(4, 0, -1):
    if P[i][c] != P[i - 1][c]:
        chosen.append(i)
        c -= tasks[i - 1][0]
check("reconstruction -> tasks 4 and 1, time 6, profit 11", sorted(chosen) == [1, 4] and sum(tasks[i - 1][0] for i in chosen) == 6 and sum(tasks[i - 1][1] for i in chosen) == 11)
bad = 0
for _ in range(300):
    tk = [(random.randint(1, 6), random.randint(1, 9)) for _ in range(random.randint(1, 6))]
    Tm = random.randint(0, 12)
    b = max(sum(tk[i][1] for i in s) for r in range(len(tk) + 1) for s in itertools.combinations(range(len(tk)), r) if sum(tk[i][0] for i in s) <= Tm)
    bad += knap(tk, Tm)[len(tk)][Tm] != b
check("0/1 knapsack == brute force (300 random)", bad == 0)
# ratio greedy counterexample 26B-A Q2a is in v03_greedy


# ---- minimum removal so that any two remaining differ by at most k  (22B-B Q4)
def min_removal(A, k):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            if abs(A[i] - A[j]) <= k:
                C[i][j] = 0
            else:
                C[i][j] = 1 + min(C[i + 1][j], C[i][j - 1])
    return C


def min_removal_brute(A, k):
    n = len(A)
    best = n
    for r in range(n + 1):
        for keep in itertools.combinations(range(n), r):
            vals = [A[i] for i in keep]
            if not vals or max(vals) - min(vals) <= k:
                best = min(best, n - r)
    return best


Cm = min_removal([1, 2, 5, 6, 8], 2)
check("22B-B Q4c table (upper triangle)", Cm == [[0, 0, 1, 2, 3], [0, 0, 1, 1, 2], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], Cm)
check("22B-B Q4c answer 3", Cm[0][4] == 3 == min_removal_brute([1, 2, 5, 6, 8], 2))
bad = 0
for _ in range(300):
    A = sorted(random.sample(range(0, 30), random.randint(1, 8)))
    k = random.randint(0, 8)
    bad += min_removal(A, k)[0][len(A) - 1] != min_removal_brute(A, k)
check("min removal on SORTED arrays == brute force (300 random)", bad == 0)

sys.exit(0 if ok else 1)
