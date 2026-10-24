# -*- coding: utf-8 -*-
"""Solver checks for 22B-B Q2a/Q2b (corrected split) and Q4c (corrected table).
Run: PYTHONUTF8=1 py tools/verify/22B-B/solve_22B-B.py. ASCII output."""
import itertools, random

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


def best_diff(A, k):
    best = -1
    for idx in itertools.combinations(range(len(A)), k):
        sb = sum(A[i] for i in idx)
        best = max(best, abs(sb - (sum(A) - sb)))
    return best


def select(A, i):            # stands for Select(A, n, i): the i-th smallest
    return sorted(A)[i - 1]


def fixed_split(A, k):
    """The official code with the one fix: in the else branch the pivot is Select(A, n, n-k)."""
    n = len(A)
    B, C = [], []
    if k < n - k:
        S = select(A, k)
        for v in A:
            (C if v > S else B).append(v)
    else:
        S = select(A, n - k)
        for v in A:
            (B if v > S else C).append(v)
    return B, C


random.seed(22)
bad = 0
for _ in range(5000):
    n = random.randint(2, 9)
    k = random.randint(1, n - 1)
    A = random.sample(range(1, 40), n)
    B, C = fixed_split(A, k)
    if len(B) != k or len(C) != n - k or abs(sum(B) - sum(C)) != best_diff(A, k) or sorted(B + C) != sorted(A):
        bad += 1
check("Q2a corrected split: |B|=k, |C|=n-k and the difference is maximal (5000 random, all k)", bad == 0, "bad=%d" % bad)
B, C = fixed_split([13, 5, 7], 2)
check("Q2a counterexample of the held key A=[13,5,7], k=2 now gives B={13,7}, C={5}, difference 15",
      sorted(B) == [7, 13] and C == [5] and abs(sum(B) - sum(C)) == 15 == best_diff([13, 5, 7], 2))
B, C = fixed_split([8, 4, 5, 2, 10], 2)
check("Q2a example 8,4,5,2,10 k=2 -> {4,2} / {8,5,10}, 17", sorted(B) == [2, 4] and abs(sum(B) - sum(C)) == 17)
# correctness argument: diff(B) = |2 Sum(B) - Sum(A)| is maximal at the k smallest or the k largest, and the k smallest
# wins iff the n-k largest sum to at least the k largest, i.e. iff k <= n-k
bad = 0
for _ in range(3000):
    n = random.randint(2, 9)
    k = random.randint(1, n - 1)
    A = sorted(random.sample(range(1, 40), n))
    small = sum(A) - 2 * sum(A[:k])
    large = 2 * sum(A[n - k:]) - sum(A)
    if max(small, large) != best_diff(A, k) or (k <= n - k and small < large) or (k > n - k and large < small):
        bad += 1
check("Q2b argument: optimum is the k smallest (k<=n-k) or the k largest (k>n-k) (3000 random)", bad == 0)


# ---------- Q4c ----------
def C_rec(A, k):
    memo = {}

    def C(i, j):
        if i > j:
            return 0
        if (i, j) not in memo:
            memo[(i, j)] = 0 if abs(A[i] - A[j]) <= k else min(C(i + 1, j), C(i, j - 1)) + 1
        return memo[(i, j)]
    return C


A = [1, 2, 5, 6, 8]
C = C_rec(A, 2)
tab = [[C(i, j) if j >= i else None for j in range(5)] for i in range(5)]
corrected = [[0, 0, 1, 2, 3], [None, 0, 1, 1, 2], [None, None, 0, 0, 1], [None, None, None, 0, 0],
             [None, None, None, None, 0]]
check("Q4c corrected table == recurrence cell by cell (cells (2,6)=1 and (6,8)=0)", tab == corrected, str(tab))
check("Q4c answer C(1,8) = 3", tab[0][4] == 3)
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
