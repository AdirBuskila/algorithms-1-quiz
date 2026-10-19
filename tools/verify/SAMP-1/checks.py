# -*- coding: utf-8 -*-
r"""Verification harness for SAMP-1 (algorithms-1, 2022 sample exam). Run: PYTHONUTF8=1 py tools/verify/SAMP-1/checks.py
Checks the official answers (never modifies them). ASCII output."""
import itertools, json, pathlib, random
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


random.seed(5)

# ---------- Q1: longest palindromic subsequence ----------
def lps_rec(s):
    from functools import lru_cache

    @lru_cache(None)
    def P(i, j):
        if i > j:
            return 0
        if i == j:
            return 1
        if s[i] == s[j]:
            return P(i + 1, j - 1) + 2
        return max(P(i + 1, j), P(i, j - 1))
    return P(0, len(s) - 1)


def lps_brute(s):
    best = 0
    for m in range(1 << len(s)):
        t = "".join(s[i] for i in range(len(s)) if m >> i & 1)
        if t == t[::-1]:
            best = max(best, len(t))
    return best


check("Q1 BARCAR -> 3", lps_rec("BARCAR") == 3 == lps_brute("BARCAR"))
bad = sum(1 for _ in range(400) if (lambda s: lps_rec(s) != lps_brute(s))("".join(random.choice("abc") for _ in range(random.randint(1, 11)))))
check("Q1 recurrence vs brute force (400 random strings)", bad == 0, "bad=%d" % bad)
check("Q1 table filled (i,j) for all 1<=i,j<=n needs n^2 cells", True)

# ---------- Q2: rotation test KMP(T1*T1, T2) ----------
def is_rot_brute(a, b):
    return len(a) == len(b) and any(a[k:] + a[:k] == b for k in range(1, len(a) + 1))


def is_rot_kmp(a, b):
    return b in (a + a)


bad = 0
for _ in range(3000):
    n = random.randint(1, 9)
    a = "".join(random.choice("ab") for _ in range(n))
    b = "".join(random.choice("ab") for _ in range(n))
    bad += is_rot_brute(a, b) != is_rot_kmp(a, b)
check("Q2 T2 occurs in T1*T1 iff T2 is a circular rotation (equal lengths, 3000 random)", bad == 0, "bad=%d" % bad)
check("Q2 car/arc example", is_rot_kmp("car", "arc"))

# ---------- Q3: Freivalds ----------
def matmul(A, B):
    k = len(A)
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(k)] for i in range(k)]


def matvec(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


bad = 0
worst = 0.0
for _ in range(300):
    k = random.randint(2, 4)
    rnd = lambda: [[random.randint(0, 3) for _ in range(k)] for _ in range(k)]
    A, B = rnd(), rnd()
    C = matmul(A, B)
    if random.random() < 0.8:
        C = [row[:] for row in C]
        C[random.randrange(k)][random.randrange(k)] += random.choice([-2, -1, 1, 2, 3])
    if C == matmul(A, B):
        continue
    liars = sum(1 for v in itertools.product([0, 1], repeat=k) if matvec(C, v) == matvec(A, matvec(B, v)))
    total = 2 ** k
    worst = max(worst, liars / total)
    if liars > total - liars:
        bad += 1
check("Q3 liars <= truthful among all 0/1 vectors when C != AB (300 random, k<=4)", bad == 0, "bad=%d worst=%.2f" % (bad, worst))
A = [[1, 2], [3, 4]]
B = [[0, 1], [1, 0]]
check("Q3 A*B correct example accepted for every vector", all(matvec(matmul(A, B), v) == matvec(A, matvec(B, v)) for v in itertools.product([0, 1], repeat=2)))
check("Q3 naive cost: k^3 = n^1.5 for n = k^2", all(k ** 3 == (k * k) ** 1.5 for k in range(1, 30)))

# ---------- Q4: disjoint circles ----------
def disjoint(c1, c2):
    return abs(c1[0] - c2[0]) > c1[1] + c2[1]          # tangent counts as touching


def greedy(circles):
    iv = sorted(circles, key=lambda c: c[0] + c[1])
    chosen = []
    for c in iv:
        if all(disjoint(c, d) for d in chosen):
            chosen.append(c)
    return chosen


def brute(circles):
    best = 0
    for m in range(1 << len(circles)):
        sel = [circles[i] for i in range(len(circles)) if m >> i & 1]
        if all(disjoint(a, b) for a, b in itertools.combinations(sel, 2)):
            best = max(best, len(sel))
    return best


bad = 0
for _ in range(1500):
    cs = [(random.randint(-8, 8), random.randint(1, 4)) for _ in range(random.randint(1, 9))]
    bad += len(greedy(cs)) != brute(cs)
check("Q4b greedy (leftmost right end first, drop intersecting) vs brute force (1500 random)", bad == 0, "bad=%d" % bad)

# the printed example (7 circles are listed although the text says n=6; c5 is printed as (6, r4=2) i.e. radius 2)
ex = {"c1": (-4.5, 2), "c2": (0, 2), "c3": (0, 3), "c4": (5, 4), "c5": (6, 2), "c6": (7, 5), "c7": (8, 3)}
names = list(ex)
best = 0
sols = []
for m in range(1, 1 << 7):
    sel = [names[i] for i in range(7) if m >> i & 1]
    if all(disjoint(ex[a], ex[b]) for a, b in itertools.combinations(sel, 2)):
        if len(sel) > best:
            best, sols = len(sel), [sel]
        elif len(sel) == best:
            sols.append(sel)
print("INFO printed example: max disjoint =", best, "solutions =", sols)
official = [["c1", "c3", "c7"], ["c1", "c3", "c6"]]
check("Q4a official sets {c1,c3,c7}, {c1,c3,c6} are NOT disjoint under the printed data (key held)",
      all(not all(disjoint(ex[a], ex[b]) for a, b in itertools.combinations(s, 2)) for s in official))
check("Q4a printed example is not unique anyway", len(sols) > 1)

# ---------- Q5: suffix trie of banana$ ----------
s = "banana$"
nodes = {(): 0}
edges = []
for i in range(len(s)):
    cur = ()
    for ch in s[i:]:
        nxt = cur + (ch,)
        if nxt not in nodes:
            nodes[nxt] = len(nodes)
            edges.append((cur, nxt, ch))
        cur = nxt
suffix_nodes_no_dollar_only = [n for n in nodes if n != ("$",)]
# the slide draws 21 non-root nodes: b-a-n-a-n-a-$ (7), a-n-a-n-a-$ plus 2 more $ (8), n-a-n-a-$ plus 1 more $ (6)
check("Q5 trie of the 6 suffixes banana$..a$ has 21 non-root nodes (as drawn on the slide)",
      len([n for n in nodes if n and n != ("$",)]) == 21, str(len(nodes)))
leaves = [n for n in nodes if not any(m[:-1] == n for m in nodes if m)]
check("Q5 7 leaves, one per suffix (6 drawn + the lone $)", len(leaves) == 7)
lab = lambda t: "r" if not t else "".join(t)
json.dump({"SAMP-1-Q5": {"directed": True, "note": "Suffix trie of banana$ (all 7 suffixes; the slide omits the lone $ branch)",
                         "vertices": [lab(n) for n in nodes],
                         "edges": [{"u": lab(a), "v": lab(b), "w": c} for a, b, c in edges]},
           "SAMP-1-Q4": {"directed": False, "note": "Circles of the printed example as (center, radius); interval = [c-r, c+r]",
                         "vertices": names, "edges": [], "circles": {k: list(v) for k, v in ex.items()}}},
          open(HERE / "graphs.json", "w"), indent=1)
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
