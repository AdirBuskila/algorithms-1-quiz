# -*- coding: utf-8 -*-
"""Reference checks for 25A-B (algorithms-1). No official key exists (all items are held as no-key);
these compute the reference values the solver/refuter can compare against. ASCII output.
Run: PYTHONUTF8=1 py tools/verify/25A-B/checks.py"""
import heapq, itertools, random
from collections import Counter

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


# Q1: largest all-zero square ending at (i,j)
M = [[0, 1, 1, 0, 1, 1],
     [0, 0, 1, 0, 0, 0],
     [1, 0, 0, 0, 0, 0],
     [1, 1, 0, 0, 0, 1],
     [1, 1, 0, 0, 0, 0]]
n, m = len(M), len(M[0])


def T_dp():
    T = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if M[i][j] == 1:
                T[i][j] = 0
            elif i == 0 or j == 0:
                T[i][j] = 1
            else:
                T[i][j] = 1 + min(T[i - 1][j], T[i][j - 1], T[i - 1][j - 1])
    return T


def T_brute(i, j):
    best = 0
    for s in range(1, min(i, j) + 2):
        if all(M[a][b] == 0 for a in range(i - s + 1, i + 1) for b in range(j - s + 1, j + 1)):
            best = s
    return best


T = T_dp()
check("Q1 T(4,4)=3, answer max T = 3", T[4][4] == 3 and max(map(max, T)) == 3)
check("Q1 recurrence T=1+min(up,left,diag) equals brute force on every cell",
      all(T[i][j] == T_brute(i, j) for i in range(n) for j in range(m)))
print("     reference T (rows 0..4):", T)


# Q2: remove k letters to minimise the sum of squared frequencies (greedy with a max-heap)
def value(s):
    return sum(c * c for c in Counter(s).values())


def greedy_min(s, k):
    h = [-c for c in Counter(s).values()]
    heapq.heapify(h)
    for _ in range(k):
        x = -heapq.heappop(h)
        heapq.heappush(h, -(x - 1))
    return sum(x * x for x in h)


def brute_min(s, k):
    best = None
    for rem in itertools.combinations(range(len(s)), k):
        t = "".join(s[i] for i in range(len(s)) if i not in rem)
        v = value(t)
        best = v if best is None or v < best else best
    return best


check("Q2 value(character)=15 and k=2 -> charter has value 9=min",
      value("character") == 15 and value("charter") == 9 == brute_min("character", 2) == greedy_min("character", 2))
random.seed(1)
bad = 0
for _ in range(400):
    s = "".join(random.choice("abcd") for _ in range(random.randint(2, 9)))
    k = random.randint(1, len(s) - 1)
    if greedy_min(s, k) != brute_min(s, k):
        bad += 1
check("Q2 greedy (decrement the largest frequency) equals brute force (400 random)", bad == 0, "bad=%d" % bad)


# Q3: inversions
def inversions(A):
    return sum(1 for i in range(len(A)) for j in range(i + 1, len(A)) if A[i] > A[j])


def merge_count(A):
    if len(A) <= 1:
        return A, 0
    mid = len(A) // 2
    L, a = merge_count(A[:mid])
    R, b = merge_count(A[mid:])
    out, c, i, j = [], a + b, 0, 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1; c += len(L) - i
    return out + L[i:] + R[j:], c


check("Q3 example [30,10,40,20] has 3 inversions", inversions([30, 10, 40, 20]) == 3 == merge_count([30, 10, 40, 20])[1])
check("Q3 merge-sort counting equals brute force (500 random)",
      all(merge_count(A)[1] == inversions(A) for A in ([random.randint(1, 9) for _ in range(random.randint(0, 9))] for _ in range(500))))


# Q4: almost match (at most one mismatch) in O(n+m) via prefix and suffix match lengths (Z-function)
def z(s):
    zz = [0] * len(s)
    l = r = 0
    for i in range(1, len(s)):
        if i < r:
            zz[i] = min(r - i, zz[i - l])
        while i + zz[i] < len(s) and s[zz[i]] == s[i + zz[i]]:
            zz[i] += 1
        if i + zz[i] > r:
            l, r = i, i + zz[i]
    return zz


def almost(T_, P):
    nn, mm = len(T_), len(P)
    zf = z(P + "\x00" + T_)[mm + 1:]                 # forward match length at each text position
    zb = z(P[::-1] + "\x00" + T_[::-1])[mm + 1:][::-1]   # backward: match length of suffixes ending at position
    out = []
    for i in range(nn - mm + 1):
        f = zf[i]
        if f >= mm:
            out.append(i)
        else:
            end = i + mm - 1
            if f + 1 + zb[end] >= mm if True else False:
                out.append(i)
    return out


def almost_naive(T_, P):
    return [i for i in range(len(T_) - len(P) + 1) if sum(a != b for a, b in zip(T_[i:i + len(P)], P)) <= 1]


check("Q4 'aababa' vs 'aaaaba' differ in one position", sum(a != b for a, b in zip("aababa", "aaaaba")) == 1)
check("Q4 linear Z-function method equals naive (1500 random)",
      all(almost(t, p) == almost_naive(t, p)
          for t, p in ((("".join(random.choice("ab") for _ in range(random.randint(2, 14)))),
                        "".join(random.choice("ab") for _ in range(random.randint(1, 4)))) for _ in range(1500))
          if len(p) < len(t)))
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
