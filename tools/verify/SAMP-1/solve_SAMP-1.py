# -*- coding: utf-8 -*-
"""Solver checks for SAMP-1 Q4a (is the solution unique?) on the printed circle data.
Run: PYTHONUTF8=1 py tools/verify/SAMP-1/solve_SAMP-1.py. ASCII output."""
import itertools

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


ex = {"c1": (-4.5, 2), "c2": (0, 2), "c3": (0, 3), "c4": (5, 4), "c5": (6, 2), "c6": (7, 5), "c7": (8, 3)}


def disjoint(a, b):          # touching counts as not disjoint
    return abs(a[0] - b[0]) > a[1] + b[1]


def ok_set(S):
    return all(disjoint(ex[a], ex[b]) for a, b in itertools.combinations(S, 2))


best = max(len(S) for r in range(1, 8) for S in itertools.combinations(ex, r) if ok_set(S))
sols = [S for S in itertools.combinations(ex, best) if ok_set(S)]
check("Q4a maximum is 3 and the optimal sets are exactly {c1,c2,c5}, {c1,c2,c7}",
      best == 3 and sols == [("c1", "c2", "c5"), ("c1", "c2", "c7")], str(sols))
check("Q4a printed sets {c1,c3,c7}, {c1,c3,c6} are not disjoint (c1-c3 overlap: [-6.5,-2.5] vs [-3,3])",
      not ok_set(("c1", "c3", "c7")) and not ok_set(("c1", "c3", "c6")))
# greedy of Q4b (smallest right end first) on the example
order = sorted(ex, key=lambda c: ex[c][0] + ex[c][1])
chosen = []
for c in order:
    if all(disjoint(ex[c], ex[d]) for d in chosen):
        chosen.append(c)
check("Q4a greedy of Q4b picks c1, c2, c5 (3 circles)", chosen == ["c1", "c2", "c5"], str(chosen))
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
