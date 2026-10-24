# -*- coding: utf-8 -*-
"""Solver checks for 22A-C Q3b, Q4, Q5. Run: PYTHONUTF8=1 py tools/verify/22A-C/solve_22A-C.py. ASCII output.
Q5 graph (vertices a..j, 15 edges) is read off the printed figure (not the handwriting); the student's first E' list
(10 edges after picking (a,b)) confirms the edge set."""
import itertools, json, pathlib, random
from collections import Counter
import networkx as nx

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


random.seed(42)


# ---------- Q3b: greedy choice - some optimal pairing pairs the two cheapest items ----------
def pairings(items):
    if not items:
        yield []
        return
    a = items[0]
    for k in range(1, len(items)):
        for rest in pairings(items[1:k] + items[k + 1:]):
            yield [(a, items[k])] + rest


def cost(P):
    return sum(max(p) for p in P)


bad = 0
for _ in range(800):
    n = random.randint(1, 4)
    p = [random.randint(1, 20) for _ in range(2 * n)]
    idx = list(range(2 * n))
    best = min(cost([(p[i], p[j]) for i, j in P]) for P in pairings(idx))
    s = sorted(idx, key=lambda i: p[i])
    c1, c2 = s[0], s[1]
    with_pair = min(cost([(p[i], p[j]) for i, j in P]) for P in pairings(idx) if (c1, c2) in P or (c2, c1) in P)
    bad += with_pair != best
check("Q3b some optimal pairing contains the pair of the two cheapest items (800 random)", bad == 0, "bad=%d" % bad)
# the exchange step itself: x+y >= p2 + max(x,y) whenever p1<=p2<=x,y
check("Q3b exchange inequality x+y >= p2+max(x,y) for p2<=min(x,y) (exhaustive 1..12)",
      all(x + y >= p2 + max(x, y) for p2 in range(1, 13) for x in range(p2, 13) for y in range(p2, 13)))


# ---------- Q4: k (>= n/2 occurrences) < m (>= n/3 occurrences) in O(n) ----------
def select(A, i):
    return sorted(A)[i - 1]


def alg(A):
    n = len(A)
    h, t = -(-n // 2), -(-n // 3)
    K = {select(A, q) for q in range(h, n + 1, h)}          # positions ceil(n/2), 2ceil(n/2) <= n
    M = {select(A, q) for q in range(t, n + 1, t)}          # positions ceil(n/3), 2ceil(n/3), 3ceil(n/3) <= n
    cnt = {v: sum(1 for a in A if a == v) for v in K | M}   # one counting pass per candidate
    for k in K:
        for m in M:
            if k < m and cnt[k] >= n / 2 and cnt[m] >= n / 3:
                return (k, m)
    return None


def truth(A):
    n = len(A)
    c = Counter(A)
    return {(k, m) for k in c for m in c if k < m and c[k] >= n / 2 and c[m] >= n / 3}


bad = total = 0
for n in range(1, 9):
    for A in itertools.product(range(1, 5), repeat=n):
        A = list(A)
        total += 1
        r, T = alg(A), truth(A)
        if (r is None) != (not T) or (r is not None and r not in T):
            bad += 1
check("Q4 candidate algorithm == brute force for ALL arrays n<=8 over 1..4", bad == 0, "arrays=%d bad=%d" % (total, bad))
bad = 0
for _ in range(20000):
    n = random.randint(1, 40)
    vals = random.sample(range(1, 100), 3)
    A = [random.choice(vals + [random.randint(1, 100)]) for _ in range(n)]
    r, T = alg(A), truth(A)
    if (r is None) != (not T) or (r is not None and r not in T):
        bad += 1
check("Q4 candidate algorithm == brute force (20000 random, n<=40)", bad == 0, "bad=%d" % bad)
check("Q4 at most 5 candidates (2 for k, 3 for m), so O(n)",
      all(len(range(-(-n // 2), n + 1, -(-n // 2))) <= 2 and len(range(-(-n // 3), n + 1, -(-n // 3))) <= 3
          for n in range(1, 500)))
check("Q4 example from checks.py: 1*6 + 2*6 -> (1,2)", alg([1] * 6 + [2] * 6) == (1, 2))

# ---------- Q5: vertex-cover 2-approximation on the printed graph ----------
EDGES = [("a", "h"), ("h", "g"), ("g", "f"), ("a", "f"), ("a", "b"), ("b", "i"), ("i", "h"), ("i", "d"),
         ("b", "c"), ("c", "d"), ("d", "e"), ("g", "d"), ("d", "j"), ("j", "f"), ("f", "e")]
G = nx.Graph(EDGES)
check("Q5 graph: 10 vertices, 15 edges", G.number_of_nodes() == 10 and G.number_of_edges() == 15)
student_first_Eprime = {("h", "g"), ("i", "h"), ("c", "d"), ("d", "e"), ("i", "d"), ("d", "j"), ("f", "j"), ("f", "g"),
                        ("f", "e"), ("g", "d")}
after_ab = {frozenset(e) for e in EDGES if "a" not in e and "b" not in e}
check("Q5 edge set agrees with the student's E' after picking (a,b) (10 edges)",
      after_ab == {frozenset(e) for e in student_first_Eprime})

picks = [("a", "b"), ("h", "g"), ("i", "d"), ("f", "e")]
E = [frozenset(e) for e in EDGES]
C = set()
rows = []
for u, v in picks:
    assert frozenset((u, v)) in E, (u, v)
    C |= {u, v}
    E = [e for e in E if u not in e and v not in e]
    rows.append((sorted(C), sorted(tuple(sorted(e)) for e in E)))
for i, (c, e) in enumerate(rows, 1):
    print("INFO iteration %d: C=%s E'=%s" % (i, c, e))
check("Q5 run ends with E' empty after 4 iterations, C = {a,b,d,e,f,g,h,i}",
      not E and C == set("abdefghi"))
check("Q5 C is a vertex cover and |C| <= 2*OPT",
      all(u in C or v in C for u, v in EDGES) and
      len(C) <= 2 * min(len(S) for r in range(11) for S in itertools.combinations(G.nodes, r)
                        if all(x in S or y in S for x, y in EDGES)))
opt = min(len(S) for r in range(11) for S in itertools.combinations(G.nodes, r) if all(x in S or y in S for x, y in EDGES))
print("INFO minimum vertex cover size =", opt)

json.dump({"22A-C-Q5": {"directed": False, "note": "Graph of the vertex-cover bonus, redrawn from the printed figure",
                        "vertices": sorted(G.nodes), "edges": [{"u": u, "v": v} for u, v in EDGES],
                        "run": [{"pick": list(p), "C": c, "Eprime": [list(x) for x in e]} for p, (c, e) in zip(picks, rows)]}},
          open(pathlib.Path(__file__).with_name("graphs.json"), "w"), indent=1)
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
