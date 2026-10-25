# -*- coding: utf-8 -*-
"""Learn-brief checks: approximation (brief 13) and the vertex-cover trace of 22A-C Q5.
Run: PYTHONUTF8=1 py tools/verify/learn/v10_approx.py     (ASCII output, exits 1 on a failure)"""
import itertools, math, random, sys

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


random.seed(2718)


def vc_approx(edges, order=None):
    """the course's algorithm: pick an arbitrary remaining edge, add both ends, delete every edge touching them.
    order = the sequence of edges to prefer (used for a deterministic run)."""
    Eprime = list(edges)
    C, trace = [], []
    pick = list(order) if order else None
    while Eprime:
        if pick:
            e = next(x for x in pick if x in Eprime)
        else:
            e = random.choice(Eprime)
        u, v = e
        C += [u, v]
        Eprime = [x for x in Eprime if u not in x and v not in x]
        trace.append((e, sorted(C), list(Eprime)))
    return C, trace


def all_outputs(edges):
    """every set that some run can output (all choices of the edge in each step)"""
    outs = set()

    def rec(Eprime, C):
        if not Eprime:
            outs.add(frozenset(C))
            return
        seen = set()
        for e in Eprime:
            u, v = e
            rest = [x for x in Eprime if u not in x and v not in x]
            key = (frozenset(C | {u, v}), tuple(sorted(rest)))
            if key in seen:
                continue
            seen.add(key)
            rec(rest, C | {u, v})
    rec(list(edges), frozenset())
    return outs


def min_cover(n, edges):
    for k in range(0, n + 1):
        for S in itertools.combinations(range(n), k):
            s = set(S)
            if all(u in s or v in s for u, v in edges):
                return k
    return n


def has_perfect_matching(vs, edges):
    vs = sorted(vs)
    if not vs:
        return True
    v = vs[0]
    for u, w in edges:
        if v in (u, w):
            o = w if u == v else u
            if o in vs and o != v:
                if has_perfect_matching([x for x in vs if x not in (v, o)], edges):
                    return True
    return False


# ---- factor 2
bad = bad2 = bad3 = 0
for _ in range(400):
    n = random.randint(2, 8)
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if random.random() < 0.4]
    if not edges:
        continue
    C, trace = vc_approx(edges)
    cover = all(u in C or v in C for u, v in edges)
    opt = min_cover(n, edges)
    bad += not cover
    bad2 += len(C) > 2 * opt
    M = [t[0] for t in trace]
    bad3 += len(C) != 2 * len(M) or opt < len(M)
check("the matching algorithm returns a cover (400 random graphs)", bad == 0)
check("|C| <= 2 * OPT, with |C| = 2|M| and OPT >= |M| for the chosen matching M (400 random graphs, brute-force OPT)", bad2 == 0 and bad3 == 0)
# tight examples
check("tight: a single edge gives |C| = 2 = 2*OPT (OPT=1); K_{3,3} with a perfect matching run gives 6 vs OPT 3",
      len(vc_approx([(0, 1)])[0]) == 2 and min_cover(2, [(0, 1)]) == 1
      and len(vc_approx([(0, 3), (1, 4), (2, 5)] + [(i, j) for i in range(3) for j in range(3, 6) if (i, j) not in [(0, 3), (1, 4), (2, 5)]], order=[(0, 3), (1, 4), (2, 5)])[0]) == 6
      and min_cover(6, [(i, j) for i in range(3) for j in range(3, 6)]) == 3)

# ---- which sets can be the output: cover + perfect matching inside
bad = tested = 0
for _ in range(120):
    n = random.randint(3, 7)
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if random.random() < 0.45]
    if not edges:
        continue
    outs = all_outputs(edges)
    for k in range(0, n + 1):
        for S in itertools.combinations(range(n), k):
            s = set(S)
            cand = all(u in s or v in s for u, v in edges) and len(s) % 2 == 0 and has_perfect_matching(sorted(s), [e for e in edges if e[0] in s and e[1] in s])
            tested += 1
            bad += cand != (frozenset(s) in outs)
check("a set is a possible output iff it is a vertex cover and the graph induced on it has a perfect matching (%d sets, 120 random graphs)" % tested, bad == 0)
# a leaf in C forces its neighbour into C
bad = 0
for _ in range(120):
    n = random.randint(3, 8)
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if random.random() < 0.35]
    if not edges:
        continue
    deg = {v: sum(v in e for e in edges) for v in range(n)}
    for C in all_outputs(edges):
        for v in C:
            if deg[v] == 1:
                nb = [e[0] if e[1] == v else e[1] for e in edges if v in e][0]
                bad += nb not in C
check("a degree-1 vertex in a possible output forces its only neighbour into the output (120 random graphs)", bad == 0)

# ---- 22A-C Q5 trace
names = "abcdefghij"
idx = {c: i for i, c in enumerate(names)}
E = [("a", "b"), ("a", "h"), ("a", "f"), ("h", "g"), ("g", "f"), ("b", "i"), ("i", "h"), ("i", "d"), ("b", "c"), ("c", "d"), ("d", "e"), ("g", "d"), ("d", "j"), ("j", "f"), ("f", "e")]
check("22A-C Q5: the graph has 15 edges", len(E) == 15)
C, trace = vc_approx(E, order=[("a", "b"), ("h", "g"), ("i", "d"), ("f", "e")])
fmt = lambda es: sorted("".join(sorted(e)) for e in es)
want_E = [fmt([("h", "g"), ("g", "f"), ("i", "h"), ("i", "d"), ("c", "d"), ("d", "e"), ("g", "d"), ("d", "j"), ("j", "f"), ("f", "e")]),
          fmt([("i", "d"), ("c", "d"), ("d", "e"), ("d", "j"), ("j", "f"), ("f", "e")]),
          fmt([("j", "f"), ("f", "e")]),
          []]
check("22A-C Q5: remaining edge sets after the four steps", [fmt(t[2]) for t in trace] == want_E, [fmt(t[2]) for t in trace])
check("22A-C Q5: the sets C after each step: {a,b}, {a,b,g,h}, {a,b,d,g,h,i}, {a,b,d,e,f,g,h,i}",
      [t[1] for t in trace] == [["a", "b"], ["a", "b", "g", "h"], ["a", "b", "d", "g", "h", "i"], ["a", "b", "d", "e", "f", "g", "h", "i"]])
Ei = [(idx[u], idx[v]) for u, v in E]
opt = min_cover(10, Ei)
check("22A-C Q5: |C| = 8, the optimum cover has 4 vertices, ratio 2 (the bound is met)", len(C) == 8 and opt == 4, opt)
# the removed edges per step (as listed in the solution)
rem1 = {"ab", "ah", "af", "bi", "bc"}
touched = lambda e, ends: ends[0] in e or ends[1] in e
removed1 = {"".join(sorted(e)) for e in E if touched(e, ("a", "b"))}
removed2 = {"".join(sorted(e)) for e in [x for x in E if not touched(x, ("a", "b"))] if touched(e, ("h", "g"))}
check("22A-C Q5: step 1 removes ab,ah,af,bi,bc ; step 2 removes hg,gf,ih,gd", removed1 == rem1 and removed2 == {"gh", "fg", "hi", "dg"})

# ---- set cover greedy
def greedy_set_cover(U, sets):
    C, T = set(U), []
    while C:
        i = max(range(len(sets)), key=lambda i: len(sets[i] & C))
        T.append(i)
        C -= sets[i]
    return T


def opt_set_cover(U, sets):
    for k in range(1, len(sets) + 1):
        for S in itertools.combinations(range(len(sets)), k):
            if set().union(*[sets[i] for i in S]) >= set(U):
                return k


H = lambda n: sum(1 / i for i in range(1, n + 1))
bad = 0
for _ in range(300):
    n = random.randint(2, 9)
    U = set(range(n))
    sets = [set(random.sample(range(n), random.randint(1, n))) for _ in range(random.randint(2, 7))]
    sets.append({x for x in U} if random.random() < 0.0 else set(random.sample(range(n), 1)))
    covered = set().union(*sets)
    if covered != U:
        sets.append(U - covered)
    g = len(greedy_set_cover(U, sets))
    o = opt_set_cover(U, sets)
    bad += g > o * H(max(len(s) for s in sets)) + 1e-9
check("greedy set cover <= OPT * H(largest set size) (300 random instances)", bad == 0)
check("H(n) <= ln n + 1 for n up to 5000", all(H(n) <= math.log(n) + 1 for n in range(1, 5001)))
check("sum_{t=1..n} 1/(n-t+1) is the harmonic number H(n)", abs(sum(1 / (n - t + 1) for n in [10] for t in range(1, 11)) - H(10)) < 1e-12)

# tight family: two rows, blocks of sizes 2, 4, ..., 2^t ; OPT = 2, greedy picks t sets (t >= 2)
fam_bad = []
for t in range(2, 9):
    blocks, elems, top, bot = [], 0, set(), set()
    for i in range(1, t + 1):
        size = 2 ** i
        blk = set(range(elems, elems + size))
        blocks.append(blk)
        top |= {x for x in blk if (x - elems) < size // 2}
        bot |= {x for x in blk if (x - elems) >= size // 2}
        elems += size
    U = set(range(elems))
    sets = blocks + [top, bot]
    g = len(greedy_set_cover(U, sets))
    o = opt_set_cover(U, sets) if t <= 4 else (2 if top | bot == U else None)
    if g != t or o != 2 or elems != 2 ** (t + 1) - 2:
        fam_bad.append((t, g, o, elems))
check("tight family: universe of 2^(t+1)-2 elements, OPT = 2 sets (the two rows), greedy takes t sets (t=2..8)", not fam_bad, fam_bad)

path = [(0, 1), (1, 2), (2, 3)]  # a-b-c-d
check("brief 13 worked example: path a-b-c-d: possible outputs are {b,c} (size 2 = OPT) and {a,b,c,d} (size 4 = 2 OPT)",
      all_outputs(path) == {frozenset({1, 2}), frozenset({0, 1, 2, 3})} and min_cover(4, path) == 2)

sys.exit(0 if ok else 1)
