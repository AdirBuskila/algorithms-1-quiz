# -*- coding: utf-8 -*-
"""Solver checks for 26B-A Q1 (0/1 task-selection DP) and Q2 (greedy). ASCII output.
Run: PYTHONUTF8=1 py tools/verify/26B-A/solve_q1_q2.py"""
import itertools, random

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


def brute(tasks, T):
    best, arg = 0, ()
    for r in range(len(tasks) + 1):
        for s in itertools.combinations(range(len(tasks)), r):
            if sum(tasks[i][0] for i in s) <= T:
                v = sum(tasks[i][1] for i in s)
                if v > best:
                    best, arg = v, s
    return best, arg


def table(tasks, T):
    """P[i][c] = max profit from tasks 1..i with total time <= c (the recurrence of the solution)."""
    n = len(tasks)
    P = [[0] * (T + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        t, v = tasks[i - 1]
        for c in range(T + 1):
            P[i][c] = P[i - 1][c] if t > c else max(P[i - 1][c], v + P[i - 1][c - t])
    return P


def backtrack(P, tasks, T):
    S, c = [], T
    for i in range(len(tasks), 0, -1):
        if P[i][c] != P[i - 1][c]:
            S.append(i)
            c -= tasks[i - 1][0]
    return sorted(S)


random.seed(1)
bad = 0
for _ in range(3000):
    n = random.randint(0, 7)
    tasks = [(random.randint(1, 6), random.randint(1, 12)) for _ in range(n)]
    T = random.randint(0, 15)
    P = table(tasks, T)
    b, _ = brute(tasks, T)
    S = backtrack(P, tasks, T)
    if P[n][T] != b or sum(tasks[i - 1][0] for i in S) > T or sum(tasks[i - 1][1] for i in S) != b:
        bad += 1
check("Q1a recurrence + backtrack == brute force on 3000 random instances", bad == 0)

ex = [(2, 4), (3, 5), (4, 10)]
check("Q1 printed example: T=5 -> 10, T=6 -> 14", table(ex, 5)[3][5] == 10 and table(ex, 6)[3][6] == 14)

q1c = [(1, 1), (2, 3), (4, 7), (5, 10)]
P = table(q1c, 6)
for i, row in enumerate(P):
    print("TABLE i=%d" % i, row)
check("Q1c table rows", P == [[0] * 7, [0, 1, 1, 1, 1, 1, 1], [0, 1, 3, 4, 4, 4, 4], [0, 1, 3, 4, 7, 8, 10],
                              [0, 1, 3, 4, 7, 10, 11]])
check("Q1c answer 11 with tasks {1,4}", P[4][6] == 11 and backtrack(P, q1c, 6) == [1, 4] and brute(q1c, 6)[0] == 11)


# ---- Q2a: ratio greedy counterexample
def ratio_greedy(tasks, T):
    tot = 0
    for t, v in sorted(tasks, key=lambda x: -x[1] / x[0]):
        if t <= T:
            T -= t
            tot += v
    return tot


ce = [(1, 2), (5, 9)]
check("Q2a counterexample T=5: greedy 2, optimum 9", ratio_greedy(ce, 5) == 2 and brute(ce, 5)[0] == 9)


# ---- Q2b/c: equal times -> take the floor(T/t) largest positive profits
def eq_greedy(vals, t, T):
    k = T // t
    return sum(v for v in sorted(vals, reverse=True)[:k] if v > 0)


bad = 0
for _ in range(3000):
    n = random.randint(0, 8)
    t = random.randint(1, 4)
    vals = [random.randint(-3, 12) for _ in range(n)]
    T = random.randint(0, 20)
    if eq_greedy(vals, t, T) != brute([(t, v) for v in vals], T)[0]:
        bad += 1
check("Q2b equal-time greedy == brute force on 3000 random instances", bad == 0)

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
