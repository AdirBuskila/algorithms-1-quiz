# -*- coding: utf-8 -*-
r"""Verification harness for 22A-B (algorithms-1). Run: PYTHONUTF8=1 py tools/verify/22A-B/checks.py
Checks the official answers (never modifies them). ASCII output."""
import functools, heapq, itertools, math, random
from fractions import Fraction

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


random.seed(22)

# ---------- Q1: minimal legal cut ----------
def legal_factory(words):
    return lambda S, i, j: S[i - 1:j] in words      # 1-based, O(1)


INF = float("inf")


def cuts_rec(S, T):
    n = len(S)
    C = [0] + [INF] * n
    for i in range(1, n + 1):
        C[i] = min(C[j] + (1 if T(S, j + 1, i) else INF) for j in range(0, i))
    return C[n]


def cuts_brute(S, T):
    n = len(S)
    best = INF
    for mask in range(1 << (n - 1)):
        cuts = [0] + [i + 1 for i in range(n - 1) if mask >> i & 1] + [n]
        if all(T(S, cuts[k] + 1, cuts[k + 1]) for k in range(len(cuts) - 1)):
            best = min(best, len(cuts) - 1)
    return best


# the printed example, with a toy dictionary that contains the three splittings of the example
words = {"באה", "רגע", "בא", "הרגע", "הר", "גע"}
check("Q1 example S=baharga -> 2 (toy dictionary)", cuts_rec("באהרגע", legal_factory(words)) == 2 == cuts_brute("באהרגע", legal_factory(words)))
bad = 0
for _ in range(500):
    n = random.randint(1, 9)
    S = "".join(random.choice("ab") for _ in range(n))
    W = {"".join(random.choice("ab") for _ in range(random.randint(1, 4))) for _ in range(random.randint(1, 6))}
    if cuts_rec(S, legal_factory(W)) != cuts_brute(S, legal_factory(W)):
        bad += 1
check("Q1 recurrence C(i)=min_j C(j)+T(S,j+1,i) vs brute force (500 random)", bad == 0, "bad=%d" % bad)


# ---------- Q2: line through the origin holding >= 51% / 34% of the points ----------
def slopes(pts):
    return [("inf" if x == 0 else Fraction(y, x)) for x, y in pts]


def exists_line(pts, frac):
    sl = slopes(pts)
    from collections import Counter
    return max(Counter(sl).values()) >= frac * len(pts)


def boyer_moore(a):
    cand, cnt = None, 0
    for v in a:
        if cnt == 0:
            cand, cnt = v, 1
        elif v == cand:
            cnt += 1
        else:
            cnt -= 1
    return cand


def sel_rank(a, r):                     # r-th smallest, 1-based (stand-in for SELECT)
    key = lambda v: (1, 0) if v == "inf" else (0, v)
    return sorted(a, key=key)[r - 1]


def opt1_51(pts):
    sl = slopes(pts)
    c = boyer_moore(sl)
    return sum(1 for v in sl if v == c) >= 0.51 * len(pts)


def opt2_51(pts):
    sl = slopes(pts)
    c = sel_rank(sl, math.ceil(len(sl) / 2))
    return sum(1 for v in sl if v == c) >= 0.51 * len(pts)


def opt_34(pts):
    sl = slopes(pts)
    n = len(sl)
    for r in (math.ceil(n / 3), math.ceil(2 * n / 3)):
        c = sel_rank(sl, r)
        if sum(1 for v in sl if v == c) >= 0.34 * n:
            return True
    return False


b1 = b2 = b3 = 0
for _ in range(4000):
    n = random.randint(1, 14)
    pts = []
    base = [(random.randint(0, 3), random.randint(-3, 3)) for _ in range(2)]
    for _ in range(n):
        p = random.choice(base) if random.random() < 0.6 else (random.randint(0, 3), random.randint(-3, 3))
        if p == (0, 0):
            p = (1, 1)
        pts.append(p)
    b1 += opt1_51(pts) != exists_line(pts, 0.51)
    b2 += opt2_51(pts) != exists_line(pts, 0.51)
    b3 += opt_34(pts) != exists_line(pts, 0.34)
check("Q2a option 1 (majority + count) vs brute force", b1 == 0, "bad=%d" % b1)
check("Q2a option 2 (SELECT at n/2 + count) vs brute force", b2 == 0, "bad=%d" % b2)
check("Q2b (SELECT at n/3 and 2n/3 + counts) vs brute force", b3 == 0, "bad=%d" % b3)


# ---------- Q3: all alignments where P and T differ at every position ----------
def prefix_function(P):
    pi = [0] * len(P)
    k = 0
    for i in range(1, len(P)):
        while k and P[i] != P[k]:
            k = pi[k - 1]
        if P[i] == P[k]:
            k += 1
        pi[i] = k
    return pi


def kmp_all(T, P):
    pi = prefix_function(P)
    res, k = [], 0
    for i, ch in enumerate(T):
        while k and ch != P[k]:
            k = pi[k - 1]
        if ch == P[k]:
            k += 1
        if k == len(P):
            res.append(i - len(P) + 1)
            k = pi[k - 1]
    return res


swap = str.maketrans("ab", "ba")
bad = 0
for _ in range(3000):
    n = random.randint(1, 14)
    m = random.randint(1, n)
    T = "".join(random.choice("ab") for _ in range(n))
    P = "".join(random.choice("ab") for _ in range(m))
    want = [i for i in range(n - m + 1) if all(P[j] != T[i + j] for j in range(m))]
    if kmp_all(T, P.translate(swap)) != want:
        bad += 1
check("Q3 KMP(T, P with a<->b swapped) == all positions with total mismatch (3000 random)", bad == 0, "bad=%d" % bad)


# ---------- Q4: joining ropes == Huffman ----------
def huff_cost(a):
    h = list(a)
    heapq.heapify(h)
    tot = 0
    while len(h) > 1:
        x, y = heapq.heappop(h), heapq.heappop(h)
        tot += x + y
        heapq.heappush(h, x + y)
    return tot


@functools.lru_cache(None)
def brute_cost(t):
    if len(t) == 1:
        return 0
    best = INF
    for i, j in itertools.combinations(range(len(t)), 2):
        rest = [t[k] for k in range(len(t)) if k not in (i, j)] + [t[i] + t[j]]
        best = min(best, t[i] + t[j] + brute_cost(tuple(sorted(rest))))
    return best


check("Q4 example 4,3,2,6 -> 29", huff_cost([4, 3, 2, 6]) == 29 == brute_cost((2, 3, 4, 6)))
bad = 0
for _ in range(400):
    a = tuple(sorted(random.randint(1, 15) for _ in range(random.randint(1, 7))))
    if huff_cost(a) != brute_cost(a):
        bad += 1
check("Q4 greedy (join two shortest) vs exhaustive merge orders (400 random)", bad == 0, "bad=%d" % bad)
check("Q4 statement example 5+7 = 12, and 4,3,2,6: 7+9+15 = 31 is not optimal",
      5 + 7 == 12 and 7 + 9 + 15 == 31 and huff_cost([4, 3, 2, 6]) < 31)

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
