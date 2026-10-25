# -*- coding: utf-8 -*-
"""Learn-brief checks: complexity_recurrence + divide_conquer (briefs 01, 02).
Run: PYTHONUTF8=1 py tools/verify/learn/v01_complexity.py     (ASCII output, exits 1 on a failure)
Every number printed in the two briefs is recomputed here."""
import itertools, math, random, sys
from functools import lru_cache

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


# ---------------------------------------------------------------- Master theorem (course form a*T(n/b)+O(n^d))
def master(a, b, d):
    """Return the Theta class as text for T(n) = a T(n/b) + Theta(n^d), course notation (d may be 0)."""
    e = math.log(a, b)
    if abs(e - d) < 1e-12:
        return "n^%g log n" % d if d else "log n"
    if e < d:
        return "n^%g" % d if d else "1"
    return "n^%.3f" % e


check("master 2T(n/2)+1 (log_2 2 = 1 > 0) -> n^1", master(2, 2, 0) == "n^1.000")
check("master T(n/2)+1 (log_2 1 = 0 = d) -> log n", master(1, 2, 0) == "log n")
check("master 2T(n/2)+n (log_2 2 = d) -> n log n", master(2, 2, 1) == "n^1 log n")
check("master 7T(n/2)+n^2 -> n^2.807", master(7, 2, 2) == "n^2.807")
check("master T(n/2)+n (log_2 1 = 0 < 1) -> n", master(1, 2, 1) == "n^1")
check("master 4T(n/2)+n^2 -> n^2 log n", master(4, 2, 2) == "n^2 log n")
check("master 3T(n/3)+n (merge-style) -> n log n", master(3, 3, 1) == "n^1 log n")
check("log_2 7 = 2.807", abs(math.log2(7) - 2.8074) < 1e-3, round(math.log2(7), 4))


def solve_num(a, b, f, n):
    """T(n) = a*T(n/b) + f(n), T(1)=1, n a power of b; iterative (no recursion limit)."""
    t, m = 1.0, 1
    while m < n:
        m *= b
        t = a * t + f(m)
    return t


def ratio(a, b, f, g, n):
    return solve_num(a, b, f, n) / g(n)


# ratios settle to a constant => Theta(g)
for name, a, b, f, g in [("2T(n/2)+1", 2, 2, lambda m: 1, lambda n: n),
                         ("T(n/2)+1", 1, 2, lambda m: 1, lambda n: math.log2(n) + 1),
                         ("2T(n/2)+n", 2, 2, lambda m: m, lambda n: n * math.log2(n)),
                         ("7T(n/2)+n^2", 7, 2, lambda m: m * m, lambda n: n ** math.log2(7))]:
    r1, r2 = ratio(a, b, f, g, 2 ** 14), ratio(a, b, f, g, 2 ** 18)
    check("numeric Theta for " + name, abs(r1 - r2) / r2 < 0.08, "ratios %.3f %.3f" % (r1, r2))

# T(n) = T(3n/4) + n : geometric series, O(n) (26B-A Q4 style); sum of (3/4)^i = 4
tot = sum(0.75 ** i for i in range(200))
check("sum (3/4)^i = 4 -> T(n) <= 4n", abs(tot - 4) < 1e-9)
# T(n) = T(n/2) + n -> 2n
check("sum (1/2)^i = 2", abs(sum(0.5 ** i for i in range(200)) - 2) < 1e-9)

# median of medians: T(n) <= T(n/5) + T(7n/10) + c n  =>  T(n) <= 10 c n  (since 1/5 + 7/10 = 9/10 < 1)
check("1/5 + 7/10 = 9/10", abs(1 / 5 + 7 / 10 - 0.9) < 1e-12)
T = {}
def tt(n):
    if n <= 5:
        return n
    if n not in T:
        T[n] = tt(n // 5) + tt(7 * n // 10 + 1) + n
    return T[n]
check("T(n)=T(n/5)+T(7n/10)+n stays <= 10 n up to 10^6", all(tt(n) <= 10 * n for n in (10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6)))

# groups of 5: at least 3 of each 5 are <= the group median; about half the groups have median <= pivot
# => at least 3 * ceil(n/10) elements <= pivot, so recursion side is at most 7n/10 + O(1)
n = 1000
check("3*(n/10) = 3n/10 elements on each side", 3 * (n // 10) == 300 and n - 300 == 700)

# ---------------------------------------------------------------- DP table sizes (space saving)
check("knapsack table (n+1)(T+1) cells = 5*7 for n=4,T=6", (4 + 1) * (6 + 1) == 35)

# ---------------------------------------------------------------- pseudo-polynomial: input size log K
K = 1000
bits = K.bit_length()
check("K=1000 needs 10 bits; K steps = 2^n scale", bits == 10 and 2 ** bits > K >= 2 ** (bits - 1))
# 22B-A Q1d: Print_lines(n): T(n)=2T(n/2)+O(1); count of prints for n power of 2 is n-1
def prints(n):
    return 0 if n <= 1 else 1 + 2 * prints(n // 2)
check("Print_lines(2^k) prints 2^k - 1 lines", all(prints(2 ** k) == 2 ** k - 1 for k in range(1, 16)))

# ---------------------------------------------------------------- D&C : Select applications
def kth(a, k):  # 1-based k-th smallest
    return sorted(a)[k - 1]


# heavy hitters: a value with count >= n/q sits at a sorted position that is a multiple of ceil(n/q)
random.seed(11)
bad = 0
for _ in range(4000):
    n = random.randint(1, 30)
    a = [random.randint(0, 4) for _ in range(n)]
    s = sorted(a)
    for q in (2, 3):
        h = math.ceil(n / q)
        cand = {s[p - 1] for p in range(h, n + 1, h)}
        for v in set(a):
            if a.count(v) * q >= n and v not in cand:  # count >= n/q
                bad += 1
check("value with count >= n/q is a sorted element at a multiple of ceil(n/q) (q=2,3), 4000 random arrays", bad == 0)
check("at most 2 candidates for q=2, at most 3 for q=3", all(len(range(math.ceil(n / 2), n + 1, math.ceil(n / 2))) <= 2 and
                                                           len(range(math.ceil(n / 3), n + 1, math.ceil(n / 3))) <= 3 for n in range(1, 200)))

# 22A-B Q2: >= 34% of points on a line through the origin => slope value occurring >= 0.34 n times => sorted positions n/3, 2n/3
random.seed(5)
bad = 0
for _ in range(3000):
    n = random.randint(3, 40)
    a = [random.randint(0, 5) for _ in range(n)]
    s = sorted(a)
    c = {s[math.ceil(n / 3) - 1], s[math.ceil(2 * n / 3) - 1]}
    for v in set(a):
        if 100 * a.count(v) >= 34 * n and v not in c:
            bad += 1
check("34%% heavy value is at sorted position ceil(n/3) or ceil(2n/3) (3000 random)", bad == 0)

# 51% majority: the median (position ceil(n/2)) must be the value
bad = 0
for _ in range(3000):
    n = random.randint(1, 40)
    a = [random.randint(0, 3) for _ in range(n)]
    s = sorted(a)
    for v in set(a):
        if 100 * a.count(v) >= 51 * n and s[math.ceil(n / 2) - 1] != v:
            bad += 1
check("51%% value is the median (3000 random)", bad == 0)

# Boyer-Moore majority vote returns the strict majority if one exists
def boyer_moore(a):
    cand, c = None, 0
    for x in a:
        if c == 0:
            cand, c = x, 1
        elif x == cand:
            c += 1
        else:
            c -= 1
    return cand

bad = 0
for _ in range(3000):
    n = random.randint(1, 25)
    a = [random.randint(0, 2) for _ in range(n)]
    for v in set(a):
        if 2 * a.count(v) > n and boyer_moore(a) != v:
            bad += 1
check("Boyer-Moore finds a strict majority (3000 random)", bad == 0)

# 22B-B Q2: split into B (size k) and C maximizing |Sum B - Sum C| (positive numbers): k smallest or k largest
random.seed(3)
bad = 0
for _ in range(1500):
    n = random.randint(2, 7)
    a = random.sample(range(1, 30), n)
    k = random.randint(1, n - 1)
    best = max(abs(sum(b) - (sum(a) - sum(b))) for b in itertools.combinations(a, k))
    s = sorted(a)
    small = abs(sum(s[:k]) - sum(s[k:]))
    large = abs(sum(s[n - k:]) - sum(s[:n - k]))
    if max(small, large) != best:
        bad += 1
check("max |Sum B - Sum C| is k smallest or k largest (1500 random)", bad == 0)
check("22B-B example 8,4,5,2,10 with k=2 -> 17", abs(sum([2, 4]) - sum([5, 8, 10])) == 17)
# choosing which one: k <= n-k => k smallest is at least as good
bad = 0
for _ in range(2000):
    n = random.randint(2, 9)
    a = sorted(random.sample(range(1, 40), n))
    k = random.randint(1, n)
    small = abs(sum(a[:k]) - sum(a[k:]))
    large = abs(sum(a[n - k:]) - sum(a[:n - k]))
    if k <= n - k and small < large:
        bad += 1
    if k > n - k and large < small:
        bad += 1
check("k <= n-k: k smallest is at least as good; k > n-k: k largest (2000 random)", bad == 0)

# 23B-C Q2b sort except position K
def sort_except(a, K):
    x = a[K - 1]
    b = sorted(a[:K - 1] + a[K:])
    return b[:K - 1] + [x] + b[K - 1:]

check("sort except K=5 on 4,10,-6,3,15,-8,7", sort_except([4, 10, -6, 3, 15, -8, 7], 5) == [-8, -6, 3, 4, 15, 7, 10])

# 26B-A Q4f : floor(sqrt n) smallest, sorted
def smallest_sqrt(a):
    k = math.isqrt(len(a))
    return sorted(a)[:k]
check("sqrt(n) smallest of a 10-element array", smallest_sqrt([9, 4, 7, 1, 8, 3, 6, 2, 5, 0]) == [0, 1, 2])
check("sqrt(n) log n = o(n): ratio shrinks", (1e6 ** 0.5 * math.log2(1e6)) / 1e6 < (1e4 ** 0.5 * math.log2(1e4)) / 1e4)

# 22A-C Q4: k appears >= n/2, m appears >= n/3, k < m : example n=12, six 1s and six 2s
a = [1] * 6 + [2] * 6
n = len(a)
h, t = math.ceil(n / 2), math.ceil(n / 3)
cand_k = {sorted(a)[p - 1] for p in range(h, n + 1, h)}
cand_m = {sorted(a)[p - 1] for p in range(t, n + 1, t)}
pairs = [(k, m) for k in cand_k for m in cand_m if k < m and a.count(k) * 2 >= n and a.count(m) * 3 >= n]
check("22A-C Q4 example six 1s six 2s: (1,2)", pairs == [(1, 2)], (sorted(cand_k), sorted(cand_m)))

# 22B-A Q2: consecutive-value pair with total count >= ceil(n/2): the pair contains the value at sorted position ceil(n/2) or floor(n/2)+1
def brute_pair(a):
    n = len(a)
    vals = sorted(set(a))
    return any(a.count(vals[i]) + a.count(vals[i + 1]) >= math.ceil(n / 2) for i in range(len(vals) - 1))

def via_select(a):
    n = len(a)
    s = sorted(a)
    vals = sorted(set(a))
    res = False
    for M in {s[math.ceil(n / 2) - 1], s[n // 2]}:
        i = vals.index(M)
        for j in (i - 1, i + 1):
            if 0 <= j < len(vals) and a.count(M) + a.count(vals[j]) >= math.ceil(n / 2):
                res = True
    return res

random.seed(2)
bad = 0
for _ in range(4000):
    n = random.randint(2, 14)
    a = [random.randint(0, 6) for _ in range(n)]
    if len(set(a)) >= 2 and brute_pair(a) != via_select(a):
        bad += 1
check("22B-A Q2 select + neighbours matches brute force (4000 random)", bad == 0)
check("22B-A Q2 example 5,2,8,3,2,5,8 : pair 5,8 has 4 = ceil(7/2)", brute_pair([5, 2, 8, 3, 2, 5, 8]) and [5, 2, 8, 3, 2, 5, 8].count(5) + [5, 2, 8, 3, 2, 5, 8].count(8) == 4)

# ---------------------------------------------------------------- inversions (25A-B Q3)
def sort_count(a):
    if len(a) <= 1:
        return a, 0
    m = len(a) // 2
    L, x = sort_count(a[:m])
    R, y = sort_count(a[m:])
    i = j = z = 0
    out = []
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1; z += len(L) - i
    out += L[i:] + R[j:]
    return out, x + y + z

random.seed(9)
bad = 0
for _ in range(1000):
    a = [random.randint(0, 8) for _ in range(random.randint(0, 12))]
    brute = sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])
    if sort_count(a)[1] != brute:
        bad += 1
check("merge-sort inversion count matches brute force (1000 random, ties not counted)", bad == 0)
s, c = sort_count([30, 10, 40, 20])
check("inversions of 30,10,40,20 = 3 (1 left, 1 right, 1 crossing)", c == 3 and sort_count([30, 10])[1] == 1 and sort_count([40, 20])[1] == 1)

# ---------------------------------------------------------------- rotated array search (25A-C Q3)
def search(nums, t, lo, hi):
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if nums[mid] == t:
        return mid
    if nums[lo] <= nums[mid]:
        if nums[lo] <= t < nums[mid]:
            return search(nums, t, lo, mid - 1)
        return search(nums, t, mid + 1, hi)
    if nums[mid] < t <= nums[hi]:
        return search(nums, t, mid + 1, hi)
    return search(nums, t, lo, mid - 1)

bad = 0
for n in range(1, 15):
    base = list(range(0, 3 * n, 3))
    for r in range(n):
        rot = base[r:] + base[:r]
        for t in range(-1, 3 * n + 1):
            want = rot.index(t) if t in rot else -1
            if search(rot, t, 0, n - 1) != want:
                bad += 1
check("rotated sorted array search (distinct) correct for all n<=14, all rotations", bad == 0)
check("25A-C example: [4,5,6,7,0,1,2], t=0 -> index 4 (shape of the exam example)", search([4, 5, 6, 7, 0, 1, 2], 0, 0, 6) == 4)

# ---------------------------------------------------------------- k-th missing positive (26A-A Q4)
def kth_missing(A, k):
    lo, hi = 0, len(A) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if A[mid] - (mid + 1) < k:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo + k

def kth_missing_brute(A, k):
    s, x = set(A), 0
    while k:
        x += 1
        if x not in s:
            k -= 1
    return x

random.seed(4)
bad = 0
for _ in range(3000):
    A = sorted(random.sample(range(1, 25), random.randint(0, 10)))
    k = random.randint(1, 12)
    if kth_missing(A, k) != kth_missing_brute(A, k):
        bad += 1
check("k-th missing: binary search == brute force (3000 random)", bad == 0)
A = [3, 5, 9, 10, 11, 12]
check("26A-A Q4a: A=[3,5,9,10,11,12], k=2 -> 2; Missing(i) = A[i]-(i+1) = [2,3,6,6,6,6]",
      kth_missing(A, 2) == 2 and [A[i] - (i + 1) for i in range(6)] == [2, 3, 6, 6, 6, 6])

# ---------------------------------------------------------------- median / r-th of two sorted arrays (25A-A Q1)
def rth_of_two(A, B, r):
    lo, hi = 0, r
    INF = float("inf")
    while lo <= hi:
        i = (lo + hi) // 2
        j = r - i
        def at(X, p):
            if p == 0:
                return -INF
            if p > len(X):
                return INF
            return X[p - 1]
        if at(A, i + 1) < at(B, j):
            lo = i + 1
        elif at(B, j + 1) < at(A, i):
            hi = i - 1
        else:
            return max(at(A, i), at(B, j))
    raise RuntimeError

random.seed(6)
bad = 0
for _ in range(3000):
    n = random.randint(1, 8)
    A = sorted(random.sample(range(0, 40), n))
    B = sorted(random.sample(range(0, 40), n))
    r = random.randint(1, n)
    if rth_of_two(A, B, r) != sorted(A + B)[r - 1]:
        bad += 1
check("r-th smallest of two sorted arrays via prefixes of length r (3000 random, distinct-in-array)", bad == 0)

# ---------------------------------------------------------------- 26B-A Q3 / 26A-B Q4 : select on half array, quarter guarantee
# pivot = median of a half of C : at least 1/4 of C is <= p and 1/4 >= p, so a side is at most 3/4 |C| + 1
random.seed(8)
bad = 0
for _ in range(2000):
    N = random.randint(4, 60)
    C = [random.randint(0, 100) for _ in range(N)]
    C1 = C[:N // 2]
    p = sorted(C1)[(len(C1) + 1) // 2 - 1]
    L = sum(1 for x in C if x < p)
    R = sum(1 for x in C if x > p)
    if max(L, R) > 3 * N / 4 + 1:
        bad += 1
check("median of half of C splits C into sides of size <= 3N/4+1 (2000 random)", bad == 0)

# ---------------------------------------------------------------- the worked example of brief 02
A = [7, 1, 7, 3, 7, 2, 2, 2, 5, 2]
n = len(A)
h = math.ceil(n / 3)
s = sorted(A)
check("brief 02 example: sorted order", s == [1, 2, 2, 2, 2, 3, 5, 7, 7, 7])
check("brief 02 example: h = 4, multiples 4 and 8", h == 4 and list(range(h, n + 1, h)) == [4, 8])
cands = [s[p - 1] for p in range(h, n + 1, h)]
check("brief 02 example: candidates 2 and 7", cands == [2, 7])
check("brief 02 example: 2 occurs 4 times (4 >= 10/3), 7 occurs 3 times (3 < 10/3)",
      A.count(2) == 4 and 3 * 4 >= 10 and A.count(7) == 3 and 3 * 3 < 10)
check("brief 02 example: only 2 is a heavy value", [v for v in set(A) if 3 * A.count(v) >= n] == [2])

sys.exit(0 if ok else 1)
