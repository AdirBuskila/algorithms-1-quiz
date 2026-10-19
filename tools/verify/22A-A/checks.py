# -*- coding: utf-8 -*-
r"""Verification harness for 22A-A (algorithms-1). Run: PYTHONUTF8=1 py tools/verify/22A-A/checks.py
Checks the lecturer solution (never modifies it). ASCII output."""
import itertools, random, pathlib, json
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


random.seed(7)

# ---------- Q1: LCS of three strings ----------
def lcs3_rec(S1, S2, S3):
    from functools import lru_cache

    @lru_cache(None)
    def f(i, j, l):
        if i == 0 or j == 0 or l == 0:
            return 0
        if S1[i - 1] == S2[j - 1] == S3[l - 1]:
            return f(i - 1, j - 1, l - 1) + 1
        return max(f(i - 1, j, l), f(i, j - 1, l), f(i, j, l - 1))
    return f(len(S1), len(S2), len(S3))


def subseqs(s):
    out = set()
    for m in range(1 << len(s)):
        out.add("".join(s[i] for i in range(len(s)) if m >> i & 1))
    return out


bad = 0
for _ in range(300):
    n = random.randint(1, 7)
    S = ["".join(random.choice("abc") for _ in range(n)) for _ in range(3)]
    common = subseqs(S[0]) & subseqs(S[1]) & subseqs(S[2])
    if max(len(c) for c in common) != lcs3_rec(*S):
        bad += 1
check("Q1 LCS3 recurrence vs brute force (300 random triples, n<=7)", bad == 0, "bad=%d" % bad)

# ---------- Q2: A = B^k (k>=2) iff t = KMP(A*A, A) >= 3 ----------
def occ(text, pat):
    return sum(1 for i in range(len(text) - len(pat) + 1) if text[i:i + len(pat)] == pat)


def is_power(A):
    n = len(A)
    return any(n % d == 0 and A[:d] * (n // d) == A for d in range(1, n // 2 + 1))


bad = 0
for n in range(2, 13):
    for tup in itertools.product("ab", repeat=n):
        A = "".join(tup)
        t = occ(A + A, A)
        if (t >= 3) != is_power(A):
            bad += 1
check("Q2 t>=3 iff A=B^k, k>=2 (all binary strings n<=12)", bad == 0, "bad=%d" % bad)
check("Q2 example abbabbabbabb: t=5 (k=4), true", occ("abbabbabbabb" * 2, "abbabbabbabb") == 5)

# ---------- Q3: polynomial identity, random point in 0..n ----------
# degree <= n-1 polynomials differing: at most n-1 agreeing points among the n+1 points 0..n
bad = 0
for _ in range(2000):
    n = random.randint(1, 8)
    P = [random.randint(-3, 3) for _ in range(n)]
    G = [random.randint(-3, 3) for _ in range(n)]
    if P == G:
        continue
    agree = sum(1 for t in range(n + 1) if sum(c * t ** i for i, c in enumerate(P)) == sum(c * t ** i for i, c in enumerate(G)))
    if agree > n - 1:
        bad += 1
check("Q3 distinct deg<n polynomials agree on <= n-1 of the n+1 sample points (2000 random)", bad == 0, "bad=%d" % bad)
check("Q3 example x^2-10x+21 = (x-3)(x-7)", all(t * t - 10 * t + 21 == (t - 3) * (t - 7) for t in range(-20, 21)))

# ---------- Q4: increasing-sum arrays ----------
def greedy(arrs):
    m = len(arrs)
    tmax = max(arrs[-1])
    total = tmax
    for t in range(m - 2, -1, -1):
        c = [x for x in arrs[t] if x < tmax]
        if not c:
            return 0
        tmax = max(c)
        total += tmax
    return total


def brute(arrs):
    best = None
    for pick in itertools.product(*arrs):
        if all(pick[i] < pick[i + 1] for i in range(len(pick) - 1)):
            s = sum(pick)
            best = s if best is None or s > best else best
    return 0 if best is None else best


ex = [[-3, -4, -8, -1], [20, 17, -8, 9], [-7, 4, 3, 19]]
check("Q4 example -> 35", greedy(ex) == 35 == brute(ex))
bad = 0
for _ in range(3000):
    m = random.randint(1, 4)
    arrs = [[random.randint(-6, 12) for _ in range(random.randint(1, 4))] for _ in range(m)]
    if greedy(arrs) != brute(arrs):
        bad += 1
check("Q4 greedy vs brute force (3000 random, 0 when impossible)", bad == 0, "bad=%d" % bad)

# ---------- Q5: which option can be the output of the 2-approximation ----------
edges = [("X4", "X1"), ("X4", "X9"), ("X1", "X9"), ("X1", "X6"), ("X9", "X0"), ("X2", "X6"),
         ("X7", "X6"), ("X6", "X5"), ("X5", "X3"), ("X5", "X8"), ("X3", "X8")]
G = nx.Graph(edges)
opts = {
    "a": {"X5", "X3", "X2", "X7", "X1", "X9"},
    "b": {"X3", "X4", "X1", "X9", "X0", "X6"},
    "c": {"X1", "X8", "X3", "X4", "X9", "X6"},
    "e": {"X1", "X9", "X6", "X3", "X5", "X8"},
    "f": {"X6", "X3", "X1", "X8", "X0", "X4"},
}


def approx_outputs():
    """Every vertex set the algorithm (pick an arbitrary remaining edge, add both ends,
    delete incident edges) can return, over all edge orders of all maximal matchings."""
    res = set()

    def rec(rem, C):
        if not rem:
            res.add(frozenset(C))
            return
        for (u, v) in list(rem):
            rem2 = [e for e in rem if u not in e and v not in e]
            rec(rem2, C | {u, v})
    rec(edges, frozenset())
    return res


outs = approx_outputs()
valid = sorted(k for k, s in opts.items() if frozenset(s) in outs)
# FINDING: both c and e are reachable (c = ends of matching X3X8, X4X9, X1X6). The page marks only e
# (radio button), so the key is ambiguous -> Q5 is held (ASK_ADIR).
check("Q5 options reachable by the algorithm == ['c','e'] (key marks only e)", valid == ["c", "e"], str(valid))
check("Q5 option e is a vertex cover", all(u in opts["e"] or v in opts["e"] for u, v in edges))
check("Q5 a, b, f are not reachable", all(not (frozenset(opts[k]) in outs) for k in "abf"))

json.dump({"22A-A-Q5": {"directed": False, "note": "Graph of the vertex-cover question (lecturer solution file)",
                        "vertices": sorted(G.nodes), "edges": [{"u": u, "v": v} for u, v in edges]}},
          open(HERE / "graphs.json", "w"), indent=1)
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
