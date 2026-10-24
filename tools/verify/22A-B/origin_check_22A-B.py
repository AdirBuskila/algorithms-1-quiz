# Check of the Q2a origin-point note: remove z origin points, need a slope with >= t = ceil(p*n) - z occurrences
# among the other n' points; candidates are the sorted values at positions t, 2t, ... (1-indexed).
import random, math
from fractions import Fraction
from collections import Counter

def slope(p):
    x, y = p
    return None if x == 0 else Fraction(y, x)   # None = vertical

def brute(pts, num, den):          # at least num/den of n on one line through the origin
    n = len(pts)
    need = -(-num * n // den)
    z = sum(1 for p in pts if p == (0, 0))
    rest = [slope(p) for p in pts if p != (0, 0)]
    if not rest:
        return z >= need
    best = max(Counter(rest).values())
    return z + best >= need

def key(s):
    return (1, 0) if s is None else (0, s)

def fixed(pts, num, den):
    n = len(pts)
    need = -(-num * n // den)
    z = sum(1 for p in pts if p == (0, 0))
    rest = sorted((slope(p) for p in pts if p != (0, 0)), key=key)
    t = need - z
    if t <= 0:
        return True
    n2 = len(rest)
    if n2 == 0:
        return False
    for pos in range(t, n2 + 1, t):          # sorted positions t, 2t, ... (1-indexed)
        v = rest[pos - 1]
        if sum(1 for s in rest if s == v) >= t:
            return True
    return False

def naive_plain(pts, num, den):     # official recipe applied blindly, (0,0) given slope infinity
    n = len(pts)
    need = -(-num * n // den)
    sl = [None if p[0] == 0 else Fraction(p[1], p[0]) for p in pts]
    return max(Counter(sl).values()) >= need

random.seed(5)
bad = fail_plain = 0
for _ in range(20000):
    n = random.randint(1, 12)
    pts = [(random.randint(-2, 2), random.randint(-2, 2)) for _ in range(n)]
    for num, den in ((51, 100), (34, 100)):
        if brute(pts, num, den) != fixed(pts, num, den):
            bad += 1
        if brute(pts, num, den) != naive_plain(pts, num, den):
            fail_plain += 1
print("mismatches of the fixed procedure:", bad, "| plain recipe wrong on", fail_plain)
assert bad == 0 and fail_plain > 0
