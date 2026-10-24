# -*- coding: utf-8 -*-
"""Solver checks for 22B-A Q2 (consecutive pair with total count >= ceil(n/2)).
Run: PYTHONUTF8=1 py tools/verify/22B-A/solve_22B-A.py. ASCII output.
Finding: testing only the median M = Select(A, ceil(n/2)) is NOT enough for even n (A=[1,2,3,4,5,5]: the pair 4,5
occupies positions 4..6 = n/2 places, and does not contain the median 3). The fix also tests M2 = Select(A, n/2+1)."""
import itertools, random
from collections import Counter

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


def truth(A):
    c = Counter(A)
    vals = sorted(c)
    need = -(-len(A) // 2)
    return any(c[vals[i]] + c[vals[i + 1]] >= need for i in range(len(vals) - 1))


def test_median(A, M):
    """The official per-median test with >= ceil(n/2) (Count_M, L = max below M, R = min above M)."""
    n = len(A)
    need = -(-n // 2)
    cm = sum(1 for v in A if v == M)
    if need <= cm < n:
        return True
    lows = [v for v in A if v < M]
    if lows and cm + A.count(max(lows)) >= need:
        return True
    highs = [v for v in A if v > M]
    if highs and cm + A.count(min(highs)) >= need:
        return True
    return False


def one_median(A):
    n = len(A)
    return test_median(A, sorted(A)[(n + 1) // 2 - 1])


def fixed(A):
    n = len(A)
    s = sorted(A)
    return test_median(A, s[(n + 1) // 2 - 1]) or test_median(A, s[n // 2])   # positions ceil(n/2), floor(n/2)+1


check("finding: one median is not enough, A=[1,2,3,4,5,5] truth True, one-median test False",
      truth([1, 2, 3, 4, 5, 5]) and not one_median([1, 2, 3, 4, 5, 5]))
bad = 0
total = 0
for n in range(1, 9):
    for A in itertools.product(range(1, n + 1), repeat=n):
        total += 1
        if fixed(list(A)) != truth(list(A)):
            bad += 1
check("Q2 fixed algorithm (both medians, >= ceil(n/2)) == brute force for ALL arrays n<=8 over values 1..n",
      bad == 0, "arrays=%d bad=%d" % (total, bad))
random.seed(5)
bad = 0
for _ in range(20000):
    n = random.randint(1, 30)
    A = [random.randint(1, random.randint(1, 2 * n)) for _ in range(n)]
    bad += fixed(A) != truth(A)
check("Q2 fixed algorithm == brute force (20000 random arrays, n<=30)", bad == 0, "bad=%d" % bad)
check("Q2 example 5,2,8,3,2,5,8 -> True", fixed([5, 2, 8, 3, 2, 5, 8]))
check("Q2 key counterexample A=[1,2,3,4] -> True", fixed([1, 2, 3, 4]))
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
