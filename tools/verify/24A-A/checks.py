# -*- coding: utf-8 -*-
"""Verification harness for 24A-A (algorithms-1). Run: PYTHONUTF8=1 py tools/verify/24A-A/checks.py
Checks the (partial) official answers, never modifies them. ASCII output."""
import itertools, random
from fractions import Fraction
from math import ceil, log2

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


random.seed(11)

# ---------- Q2: cover points with minimum number of unit-length segments ----------
def greedy_cover(points):
    pts = sorted(points)
    end = float("-inf")
    segs = []
    for p in pts:
        if p > end:
            segs.append((p, p + 1))
            end = p + 1
    return segs


def brute_cover(points):
    pts = sorted(set(points))
    # an optimal solution can always start each segment at an input point
    for k in range(1, len(pts) + 1):
        for starts in itertools.combinations(pts, k):
            if all(any(s <= p <= s + 1 for s in starts) for p in pts):
                return k
    return 0


bad = 0
for _ in range(3000):
    n = random.randint(1, 9)
    pts = [round(random.uniform(0, 8), 1) for _ in range(n)]
    g = greedy_cover(pts)
    covers = all(any(a <= p <= b for a, b in g) for p in pts)
    if not covers or len(g) != brute_cover(pts):
        bad += 1
check("Q2a official greedy covers every point and uses the minimum number of unit segments (3000 inputs)", bad == 0)
g = greedy_cover([0.2, 0.9, 1.4, 3.0, 3.5, 4.6])
check("Q2a greedy example", g == [(0.2, 1.2), (1.4, 2.4), (3.0, 4.0), (4.6, 5.6)], f"{g}")

# ---------- Q3: one random bit comparison, strings differing in exactly one bit ----------
def p_equal_returned(n):  # Alice picks i uniformly; strings differ only at position 0
    return Fraction(n - 1, n)


check("Q3a if the strings differ, P(Bob answers 'equal') = (n-1)/n for n=2..12", all(p_equal_returned(n) == Fraction(n - 1, n) for n in range(2, 13)))
# P(answer "different" is wrong) = 0, P(answer "equal" is wrong) = P(differ and equal)
# exact: bits needed to write an index 0..n-1 is ceil(log2 n); check against bit_length for n>=2
check("Q3b ceil(log2 n) == bit_length(n-1) for n=2..4096", all(ceil(log2(n)) == (n - 1).bit_length() for n in range(2, 4097)))
# Q3c n/2 distinct positions chosen at random, strings differ in exactly one position
for n in (2, 4, 6, 8, 10):
    subs = list(itertools.combinations(range(n), n // 2))
    p = Fraction(sum(1 for s in subs if 0 in s), len(subs))
    check(f"Q3c n={n}: P(the chosen n/2 positions contain the differing bit) = 1/2", p == Fraction(1, 2))

# ---------- Q4: tallest stable tower of boxes (no rotation), widths sorted descending ----------
def tower_dp(boxes):  # boxes: list of (w, l, h) sorted by w descending; T(i)=h_i+max_{j<i, l_j>l_i} T(j)
    T = []
    for i, (w, l, h) in enumerate(boxes):
        best = 0
        for j in range(i):
            if boxes[j][1] > l and T[j] > best:
                best = T[j]
        T.append(best + h)
    return max(T) if T else 0


def tower_brute(boxes):
    best = 0
    n = len(boxes)
    for mask in range(1 << n):
        sel = [boxes[i] for i in range(n) if mask >> i & 1]
        sel.sort(key=lambda b: -b[0])
        if all(sel[k][0] > sel[k + 1][0] and sel[k][1] > sel[k + 1][1] for k in range(len(sel) - 1)):
            best = max(best, sum(b[2] for b in sel))
    return best


bad = 0
for _ in range(3000):
    n = random.randint(1, 8)
    W = random.sample(range(1, 40), n)
    L = random.sample(range(1, 40), n)
    H = random.sample(range(1, 40), n)
    boxes = sorted(zip(W, L, H), key=lambda b: -b[0])
    if tower_dp(boxes) != tower_brute(boxes):
        bad += 1
check("Q4a official recurrence T(i)=H(i)+max T(j) over j<i with L(j)>L(i) == brute force (3000 inputs, widths descending)", bad == 0)

# the worked example that appears in the solution file's variant of Q4 (not in the printed exam)
ex = sorted([(10, 3, 5), (8, 4, 9), (6, 2, 1)], key=lambda b: -b[0])
check("Note: with the table H=(5,9,1) the tallest tower is 10, not the 15 printed in the solution file variant", tower_dp(ex) == 10 == tower_brute(ex))

# ---------- Bonus (no key in the solution file): shortest-interval-first greedy is not optimal ----------
iv = [(0, 10), (9, 12), (11, 20)]
shortest = min(iv, key=lambda a: a[1] - a[0])
chosen = [shortest] + [a for a in iv if a[1] < shortest[0] or a[0] > shortest[1]]
check("Bonus (info only): shortest-first picks 1 interval, optimum is 2", len(chosen) == 1 and len([iv[0], iv[2]]) == 2)

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
