# -*- coding: utf-8 -*-
"""Solver checks for 23A-A (no answer source): Q1 triangle DP, Q2 generalized suffix tree LCSubstring,
Q3 von Neumann fair coin, Q4 greedy with weights 5^j, Q5 greedy set cover ratio.
Run: PYTHONUTF8=1 py tools/verify/23A-A/solve_all.py   (ASCII output)"""
import itertools, math, random
from fractions import Fraction

ok = True
random.seed(2023)


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


# ---------------- Q1: M(i,j) = A[i][j] + max(M(i-1,j-1), M(i-1,j)) on the lower triangle
def q1_dp(A):
    n = len(A)
    M = [[None] * n for _ in range(n)]
    M[0][0] = A[0][0]
    for i in range(1, n):
        for j in range(i + 1):
            cand = [M[i - 1][jj] for jj in (j - 1, j) if 0 <= jj <= i - 1]
            M[i][j] = A[i][j] + max(cand)
    j = max(range(n), key=lambda t: M[n - 1][t])
    path = [j]
    for i in range(n - 1, 0, -1):          # reconstruction from the full table
        jj = max([x for x in (j - 1, j) if 0 <= x <= i - 1], key=lambda x: M[i - 1][x])
        path.append(jj); j = jj
    return M[n - 1][path[0]], path[::-1]


def q1_dp_one_row(A):
    row = [A[0][0]]
    for i in range(1, len(A)):
        row = [A[i][j] + max(row[jj] for jj in (j - 1, j) if 0 <= jj <= i - 1) for j in range(i + 1)]
    return max(row)


def q1_brute(A):
    n = len(A); best = None
    for steps in itertools.product((0, 1), repeat=n - 1):
        j, s = 0, A[0][0]
        for i, st in enumerate(steps, 1):
            j += st; s += A[i][j]
        best = s if best is None else max(best, s)
    return best


ex = [[1, 0, 0], [3, 2, 0], [4, 10, 12]]
check("Q1 example: max path 1->2->12 = 15", q1_dp(ex) == (15, [0, 1, 2]))
bad = 0
for _ in range(2000):
    n = random.randint(1, 8)
    A = [[random.randint(-9, 20) if j <= i else 0 for j in range(n)] for i in range(n)]
    v, path = q1_dp(A)
    pv = sum(A[i][path[i]] for i in range(n))
    valid = path[0] == 0 and all(path[i + 1] - path[i] in (0, 1) for i in range(n - 1))
    if not (v == q1_brute(A) == q1_dp_one_row(A) == pv and valid): bad += 1
check("Q1 DP (full table + reconstruction, and one-row value-only) == brute force, 2000 random", bad == 0)


# ---------------- Q2: naive generalized suffix tree of S1$ S2*, string depth + marks, deepest 'both' node
def lcsub_brute(a, b):
    best = ""
    for i in range(len(a)):
        for j in range(i + 1, len(a) + 1):
            if j - i > len(best) and a[i:j] in b: best = a[i:j]
    return best


def build_gst(s1, s2):
    """Compressed suffix tree of all suffixes of s1+'$' and s2+'*' (naive insertion). node: dict char->[label, child]."""
    root = {"ch": {}, "leaf": None}
    for src, s in ((1, s1 + "$"), (2, s2 + "*")):
        for i in range(len(s)):
            suf, node = s[i:], root
            while True:
                c = suf[0]
                if c not in node["ch"]:
                    node["ch"][c] = [suf, {"ch": {}, "leaf": src}]; break
                lab, child = node["ch"][c]
                t = 0
                while t < len(lab) and t < len(suf) and lab[t] == suf[t]: t += 1
                if t == len(lab):
                    node, suf = child, suf[t:]; continue
                mid = {"ch": {lab[t]: [lab[t:], child]}, "leaf": None}
                node["ch"][c] = [lab[:t], mid]
                mid["ch"][suf[t]] = [suf[t:], {"ch": {}, "leaf": src}]
                break
    return root


def deepest_both(root):
    best = [""]

    def dfs(node, path):
        if not node["ch"]:
            return {node["leaf"]}
        marks = set()
        for lab, child in node["ch"].values():
            marks |= dfs(child, path + lab)
        if marks == {1, 2} and len(path) > len(best[0]):
            best[0] = path
        return marks
    dfs(root, "")
    return best[0]


check("Q2 example BADAEAT / CAEADAS: longest common substring has length 3 (ADA, AEA)",
      len(deepest_both(build_gst("BADAEAT", "CAEADAS"))) == 3 == len(lcsub_brute("BADAEAT", "CAEADAS"))
      and "ADA" in "CAEADAS")
bad = 0
for _ in range(1500):
    n = random.randint(1, 12)
    a = "".join(random.choice("ABCDE") for _ in range(n)); b = "".join(random.choice("ABCDE") for _ in range(n))
    r = deepest_both(build_gst(a, b))
    if len(r) != len(lcsub_brute(a, b)) or (r and (r not in a or r not in b)): bad += 1
check("Q2 deepest node marked {S1,S2} == brute-force longest common substring, 1500 random", bad == 0)


# ---------------- Q3: probabilities of pairs and the von Neumann procedure
for p in (Fraction(1, 3), Fraction(7, 10), Fraction(1, 2)):
    probs = {"PE": (1 - p) * p, "EP": p * (1 - p), "EE": p * p, "PP": (1 - p) ** 2}
    check("Q3b table sums to 1, P(EP)=P(PE) for p=%s" % p, sum(probs.values()) == 1 and probs["EP"] == probs["PE"])
    stop = 2 * p * (1 - p)
    # P(output 0) = sum_k (1-stop)^k * p(1-p) = p(1-p)/stop = 1/2 ; expected pairs 1/stop
    check("Q3c output exactly 1/2 and expected pairs = 1/(2p(1-p)) for p=%s" % p,
          probs["EP"] / stop == Fraction(1, 2), str(1 / stop))
p = 0.8
res = [0, 0]; pairs = 0
for _ in range(100000):
    while True:
        pairs += 1
        x, y = random.random() < p, random.random() < p
        if x != y:
            res[0 if x else 1] += 1; break
check("Q3c simulation p=0.8: frequency of each output near 1/2", abs(res[0] / 100000 - 0.5) < 0.01,
      "%.4f, pairs/run=%.3f (1/(2pq)=%.3f)" % (res[0] / 100000, pairs / 100000, 1 / (2 * p * (1 - p))))


# ---------------- Q4: weights 5^(K-1),...,5,1 ; greedy = minimum number of items
def greedy(W, Ps):
    cnt = 0
    for P in sorted(Ps, reverse=True):
        cnt += W // P; W %= P
    return cnt


def opt(W, Ps):
    INF = 10**9; f = [0] + [INF] * W
    for w in range(1, W + 1):
        f[w] = min(f[w - P] + 1 for P in Ps if P <= w)
    return f


bad = 0
for K in range(1, 6):
    Ps = [5 ** (K - i) for i in range(1, K + 1)]
    f = opt(3200, Ps)
    bad += sum(greedy(W, Ps) != f[W] for W in range(0, 3201))
check("Q4 greedy == optimal coin-count DP for K=1..5, W=0..3200", bad == 0)
check("Q4 example W=35, K=3 (25,5,1): 25+5+5 -> 3 items", greedy(35, [25, 5, 1]) == 3 == opt(35, [25, 5, 1])[35])
# lemma: in an optimal solution each lighter type is used at most 4 times, and 4*(5^(j-1)+...+1) = 5^j - 1
check("Q4 lemma: 4*sum_{i<j}5^i = 5^j - 1 for j<=10", all(4 * sum(5 ** i for i in range(j)) == 5 ** j - 1 for j in range(11)))


# ---------------- Q5: greedy set cover <= H(n) * OPT
def greedy_cover(U, S):
    unc, T = set(U), []
    while unc:
        i = max(range(len(S)), key=lambda t: len(S[t] & unc))
        T.append(i); unc -= S[i]
    return T


def opt_cover(U, S):
    for r in range(1, len(S) + 1):
        for C in itertools.combinations(range(len(S)), r):
            if set().union(*(S[c] for c in C)) == U: return r


worst = 0; bad = 0
for _ in range(1500):
    n = random.randint(1, 9); m = random.randint(1, 7)
    S = [set(x for x in range(n) if random.random() < 0.35) for _ in range(m)]
    U = set().union(*S)
    if not U: continue
    g, o = len(greedy_cover(U, S)), opt_cover(U, S)
    H = sum(1 / i for i in range(1, len(U) + 1))
    worst = max(worst, g / o)
    if g > H * o + 1e-9: bad += 1
check("Q5 greedy cover size <= H(|U|) * OPT, 1500 random", bad == 0, "worst ratio %.3f" % worst)
# the classic lower-bound family: ratio grows like log n
k = 4
U = set(range(2 ** (k + 1) - 2))
rows = [set(x for x in U if x % 2 == 0), set(x for x in U if x % 2 == 1)]
blocks, start = [], 0
for t in range(1, k + 1):
    blocks.append(set(range(start, start + 2 ** t))); start += 2 ** t
S = rows + blocks
check("Q5 tight family k=4: OPT=2, greedy takes k=4 sets (ratio ~ log n)",
      opt_cover(U, S) == 2 and len(greedy_cover(U, S)) == k)
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
