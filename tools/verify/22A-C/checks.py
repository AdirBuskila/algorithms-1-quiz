# -*- coding: utf-8 -*-
r"""Verification harness for 22A-C (algorithms-1). Run: PYTHONUTF8=1 py tools/verify/22A-C/checks.py
Checks the student-solution answers against brute force (they are not official). ASCII output."""
import itertools, math, random

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


random.seed(10)

# ---------- Q1: minimal number of squares summing to N ----------
def F(N):
    f = [0] * (N + 1)
    for i in range(1, N + 1):
        f[i] = 1 + min(f[i - j * j] for j in range(1, math.isqrt(i) + 1))
    return f


def brute_sq(N):
    best = {0: 0}
    # BFS over sums
    frontier = {0}
    steps = 0
    while N not in frontier:
        steps += 1
        frontier = {s + j * j for s in frontier for j in range(1, math.isqrt(N) + 1) if s + j * j <= N}
    return steps


f = F(60)
check("Q1 F(12)=3 (4+4+4, the printed example)", f[12] == 3)
check("Q1 recurrence vs BFS for N=1..60", all(f[n] == brute_sq(n) for n in range(1, 61)))


# ---------- Q2: longest palindromic prefix via the prefix function of S$S^R ----------
def pi_last(t):
    pi = [0] * len(t)
    k = 0
    for i in range(1, len(t)):
        while k and t[i] != t[k]:
            k = pi[k - 1]
        if t[i] == t[k]:
            k += 1
        pi[i] = k
    return pi[-1]


def lpp(s):
    return max(L for L in range(1, len(s) + 1) if s[:L] == s[:L][::-1])


check("Q2 example aabaac -> 5", pi_last("aabaac" + "$" + "caabaa") == 5 == lpp("aabaac"))
bad = 0
for _ in range(3000):
    s = "".join(random.choice("abc") for _ in range(random.randint(1, 12)))
    bad += pi_last(s + "$" + s[::-1]) != lpp(s)
check("Q2 last value of pi(S$S^R) == longest palindromic prefix (3000 random)", bad == 0, "bad=%d" % bad)


# ---------- Q3a: pair sorted neighbours, pay the dearer of each pair ----------
def greedy_pairs(p):
    s = sorted(p)
    return sum(s[i] for i in range(1, len(s), 2))


def brute_pairs(p):
    def rec(rest):
        if not rest:
            return 0
        a = rest[0]
        return min(max(a, rest[k]) + rec(rest[1:k] + rest[k + 1:]) for k in range(1, len(rest)))
    return rec(list(p))


bad = 0
for _ in range(1500):
    n = random.randint(1, 4)
    p = [random.randint(1, 30) for _ in range(2 * n)]
    bad += greedy_pairs(p) != brute_pairs(p)
check("Q3a sort + pair neighbours (pay the larger) vs brute force over all pairings (1500 random)", bad == 0, "bad=%d" % bad)


# ---------- Q4 (held): the student's counting test uses '==' ----------
def student_alg(A):
    n = len(A)
    s = sorted(A)
    k = s[n // 2 - 1] if n >= 2 else s[0]       # the rank-n/2 and rank-2n/3 values
    m = s[(2 * n) // 3 - 1] if n >= 3 else s[-1]
    return sum(1 for v in A if v == m) == n / 3 or sum(1 for v in A if v == k) == n / 2


def truth(A):
    n = len(A)
    from collections import Counter
    c = Counter(A)
    return any(k < m and c[k] >= n / 2 and c[m] >= n / 3 for k in c for m in c)


A = [1] * 6 + [2] * 6                      # k=1 appears 6 >= 12/2, m=2 appears 6 >= 4
check("Q4 held: a valid instance exists in which the counts exceed n/2 and n/3", truth(A))
cnt_k = A.count(1)
cnt_m = A.count(2)
check("Q4 held: the student's test 'count == n/3' fails for m (count 6 != 4)", cnt_m != len(A) / 3 and cnt_k == len(A) / 2)
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
