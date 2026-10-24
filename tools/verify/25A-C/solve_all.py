# -*- coding: utf-8 -*-
"""Solver checks for 25A-C (no key). Every claim in the solved items is tested here.
Run: PYTHONUTF8=1 py tools/verify/25A-C/solve_all.py   (ASCII output, exit 1 on any failure)"""
import itertools, random
from fractions import Fraction

random.seed(25)
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


# ---------------------------------------------------------------- Q1: alignment distance
def opt(S1, S2):
    n1, n2 = len(S1), len(S2)
    D = [[0] * (n2 + 1) for _ in range(n1 + 1)]
    for i in range(n1 + 1):
        for j in range(n2 + 1):
            if i == 0:
                D[i][j] = j
            elif j == 0:
                D[i][j] = i
            elif S1[i - 1] == S2[j - 1]:
                D[i][j] = D[i - 1][j - 1]
            else:
                D[i][j] = 1 + min(D[i - 1][j - 1], D[i - 1][j], D[i][j - 1])
    return D[n1][n2]


def brute(S1, S2):
    """All ways to insert '-' (total length m up to n1+n2), distance = number of differing columns."""
    best = None
    n1, n2 = len(S1), len(S2)
    for m in range(max(n1, n2), n1 + n2 + 1):
        for pos1 in itertools.combinations(range(m), n1):
            T1 = ["-"] * m
            for c, p in zip(S1, pos1):
                T1[p] = c
            for pos2 in itertools.combinations(range(m), n2):
                T2 = ["-"] * m
                for c, p in zip(S2, pos2):
                    T2[p] = c
                d = sum(a != b for a, b in zip(T1, T2))
                best = d if best is None else min(best, d)
    return best


bad = 0
for _ in range(400):
    S1 = "".join(random.choice("AC") for _ in range(random.randint(0, 4)))
    S2 = "".join(random.choice("ACG") for _ in range(random.randint(0, 4)))
    if opt(S1, S2) != brute(S1, S2):
        bad += 1
check("Q1a recurrence == brute force over all gap insertions (400 random pairs, length <= 4)", bad == 0)
check("Q1a printed example AGCTTACG / ACTTAACG gives 2", opt("AGCTTACG", "ACTTAACG") == 2)


# two-row version for the space claim of Q1b
def opt_two_rows(S1, S2):
    prev = list(range(len(S2) + 1))
    for i in range(1, len(S1) + 1):
        cur = [i] + [0] * len(S2)
        for j in range(1, len(S2) + 1):
            cur[j] = prev[j - 1] if S1[i - 1] == S2[j - 1] else 1 + min(prev[j - 1], prev[j], cur[j - 1])
        prev = cur
    return prev[-1]


bad = sum(opt_two_rows(a, b) != opt(a, b) for a, b in
          (("".join(random.choice("ACGT") for _ in range(random.randint(0, 12))),
            "".join(random.choice("ACGT") for _ in range(random.randint(0, 12)))) for _ in range(2000)))
check("Q1b two-row version equals the full table (2000 random pairs)", bad == 0)


# ---------------------------------------------------------------- Q2: fractional knapsack
def greedy(val, wt, cap):
    tot = Fraction(0)
    for v, w in sorted(zip(val, wt), key=lambda p: Fraction(-p[0], p[1])):
        take = min(w, cap)
        tot += Fraction(v * take, w)
        cap -= take
        if cap == 0:
            break
    return tot


def lp_opt(val, wt, cap):
    """Exact optimum: at most one item is fractional in an optimal vertex; try every subset + one fractional item."""
    n = len(val)
    best = Fraction(0)
    for mask in range(1 << n):
        W = sum(wt[i] for i in range(n) if mask >> i & 1)
        if W > cap:
            continue
        V = sum(val[i] for i in range(n) if mask >> i & 1)
        best = max(best, Fraction(V))
        for j in range(n):
            if not mask >> j & 1:
                best = max(best, V + Fraction(val[j] * min(wt[j], cap - W), wt[j]))
    return best


bad = 0
for _ in range(3000):
    n = random.randint(1, 7)
    val = [random.randint(1, 50) for _ in range(n)]
    wt = [random.randint(1, 20) for _ in range(n)]
    cap = random.randint(0, 60)
    if greedy(val, wt, cap) != lp_opt(val, wt, cap):
        bad += 1
check("Q2a greedy by value/weight == exact optimum (3000 random)", bad == 0)
check("Q2 printed example -> 240", greedy([60, 100, 120], [10, 20, 30], 50) == 240)


# ---------------------------------------------------------------- Q3: search in a rotated sorted array
def rsearch(a, t, lo, hi, probes):
    probes[0] += 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if a[mid] == t:
        return mid
    if a[lo] <= a[mid]:                      # left half a[lo..mid] is sorted
        if a[lo] <= t < a[mid]:
            return rsearch(a, t, lo, mid - 1, probes)
        return rsearch(a, t, mid + 1, hi, probes)
    else:                                    # right half a[mid..hi] is sorted
        if a[mid] < t <= a[hi]:
            return rsearch(a, t, mid + 1, hi, probes)
        return rsearch(a, t, lo, mid - 1, probes)


bad = worst_ratio = 0
for _ in range(20000):
    n = random.randint(1, 200)
    base = sorted(random.sample(range(-500, 500), n))
    r = random.randrange(n)
    a = base[r:] + base[:r]
    t = random.choice(a + [random.randint(-600, 600)])
    probes = [0]
    got = rsearch(a, t, 0, n - 1, probes)
    exp = a.index(t) if t in a else -1
    bad += got != exp
    import math
    worst_ratio = max(worst_ratio, probes[0] - (math.floor(math.log2(n)) + 2))
check("Q3a D&C search == linear search (20000 rotated arrays, distinct values)", bad == 0)
check("Q3b calls per search <= floor(log2 n) + 2", worst_ratio <= 0)
probes = [0]
check("Q3 printed example [4,5,6,7,0,1,2], t=0 -> 4", rsearch([4, 5, 6, 7, 0, 1, 2], 0, 0, 6, probes) == 4)


# ---------------------------------------------------------------- Q4: hidden string via KMP on reversed P
def prefix(P):
    pi = [0] * len(P)
    k = 0
    for q in range(1, len(P)):
        while k and P[k] != P[q]:
            k = pi[k - 1]
        if P[k] == P[q]:
            k += 1
        pi[q] = k
    return pi


def kmp_find(T, P):
    pi = prefix(P)
    q = 0
    for c in T:
        while q and P[q] != c:
            q = pi[q - 1]
        if P[q] == c:
            q += 1
        if q == len(P):
            return True
    return False


bad = 0
for _ in range(20000):
    n = random.randint(2, 15)
    m = random.randint(1, n - 1)
    T = "".join(random.choice("ab") for _ in range(n))
    P = "".join(random.choice("ab") for _ in range(m))
    bad += kmp_find(T, P[::-1]) != (P[::-1] in T)
check("Q4a KMP(T, reverse(P)) == 'reverse(P) is a substring of T' (20000 random)", bad == 0)
check("Q4 printed example abc hides in dfzcbau", kmp_find("dfzcbau", "abc"[::-1]))

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
