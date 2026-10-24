# -*- coding: utf-8 -*-
"""Step-value checks for 22A-C (algorithms-1). Run: py -X utf8 -I tools/verify/22A-C/steps_22A-C.py
Recomputes every numeric / trace / complexity answer used in the guided steps, shows that every choice distractor
fails on some input, then binds the results to tools/raw/22A-C.json. ASCII output. No Hebrew in this file:
parts are addressed by letter index."""
import itertools, json, math, pathlib, random
from collections import deque
from fractions import Fraction
from functools import lru_cache

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.loads((HERE.parents[1] / "raw" / "22A-C.json").read_text(encoding="utf-8"))
GR = json.loads((HERE / "graphs.json").read_text(encoding="utf-8"))
ok = True


def H(letter):
    return "" if letter == "" else chr(0x05d0 + "abcdefgh".index(letter))


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


def item(num, part=""):
    for q in RAW["questions"]:
        if q["num"] == num and q.get("part", "") == H(part):
            return q
    raise KeyError((num, part))


def step(num, part, idx):
    return item(num, part)["steps"][idx]


def bind_numeric(num, part, idx, expected, label):
    s = step(num, part, idx)
    check(f"bind {label}: numeric step {idx} answer == recomputed {expected}", s["type"] == "numeric" and s["answer"] == expected)


def bind_text(num, part, idx, expected, label):
    s = step(num, part, idx)
    check(f"bind {label}: text step {idx} accepts it", s["type"] == "text" and expected in s["accept"])


def bind_first(num, part, idx, label):
    s = step(num, part, idx)
    check(f"bind {label}: choice step {idx} correct option is the verified one (id a)", s["type"] == "choice" and s["correctId"] == "a")


random.seed(33)

# ============================== Q1: minimum number of squares ==============================
def F(N, jmax="sqrt"):
    f = [0] * (N + 1)
    for i in range(1, N + 1):
        best = 10 ** 9
        if jmax == "sqrt":
            rng = range(1, math.isqrt(i) + 1)
        elif jmax == "strict":
            rng = range(1, math.isqrt(i) if math.isqrt(i) ** 2 != i else math.isqrt(i))   # j < sqrt(i)
        for j in rng:
            best = min(best, f[i - j * j] + 1)
        f[i] = best
    return f


def bfs_squares(N):
    dist = [None] * (N + 1)
    dist[0] = 0
    dq = deque([0])
    while dq:
        a = dq.popleft()
        j = 1
        while a + j * j <= N:
            b = a + j * j
            if dist[b] is None:
                dist[b] = dist[a] + 1
                dq.append(b)
            j += 1
    return dist


f = F(60)
check("Q1 recurrence == BFS for N <= 60", f == bfs_squares(60))
check("Q1 F(12)=3 and F(13)=2", f[12] == 3 and f[13] == 2)
bind_numeric(1, "", 0, f[12], "Q1 F(12)")
bind_numeric(1, "", 1, f[13], "Q1 F(13)")


def greedy_count(N):
    c = 0
    while N:
        N -= math.isqrt(N) ** 2
        c += 1
    return c


check("Q1 greedy largest square uses 4 for N=12 (and is worse than optimal)", greedy_count(12) == 4 > f[12])
bind_numeric(1, "", 2, greedy_count(12), "Q1 greedy")
fs = F(20, "strict")
check("Q1 distractor 'j < sqrt(i)' gives a wrong F(4) (no way to use the square 4 itself)", fs[4] != 1 and f[4] == 1)
check("Q1 distractor 'j up to i' reaches negative index (i - j^2 < 0 for i=2, j=2)", 2 - 2 * 2 < 0)
check("Q1 distractor 'j from 0' refers to F(i) itself: i - 0^2 == i", 5 - 0 == 5)
bind_first(1, "", 3, "Q1 j range")

# ============================== Q2: palindromic prefix via prefix function ==============================
def prefix_function(s):
    pi = [0] * len(s)
    ops = 0
    for i in range(1, len(s)):
        k = pi[i - 1]
        while k and s[i] != s[k]:
            k = pi[k - 1]
            ops += 1
        if s[i] == s[k]:
            k += 1
        pi[i] = k
        ops += 1
    return pi, ops


def pal_prefix(S):
    return max(L for L in range(1, len(S) + 1) if S[:L] == S[:L][::-1])


def via(S, sep="#"):
    return prefix_function(S + sep + S[::-1])[0][-1]


bad = 0
for _ in range(3000):
    S = "".join(random.choice("abc") for _ in range(random.randint(1, 12)))
    bad += via(S) != pal_prefix(S)
check("Q2 last pi of S#S^R == longest palindromic prefix (3000 random)", bad == 0)
check("Q2 aabaac -> 5, abacdc -> 3", via("aabaac") == pal_prefix("aabaac") == 5 and via("abacdc") == pal_prefix("abacdc") == 3)
last = lambda s: prefix_function(s)[0][-1]
S = "aabaac"
check("Q2 distractors fail on aabaac: no reverse, both reversed, wrong order",
      last(S + "#" + S) != 5 and last(S[::-1] + "#" + S[::-1]) != 5 and last(S[::-1] + "#" + S) != 5)
bind_first(2, "", 0, "Q2 string")
bind_numeric(2, "", 1, last("aabaac#caabaa"), "Q2 aabaac")
bind_numeric(2, "", 2, last("abacdc#cdcaba"), "Q2 abacdc")
check("Q2 aaa without separator gives 5 (> |S|=3), with separator 3", last("aaaaaa") == 5 and via("aaa") == 3)
bind_numeric(2, "", 3, last("aaaaaa"), "Q2 no separator")
r = []
for n in (100, 1000, 10000):
    S = "".join(random.choice("ab") for _ in range(n))
    r.append(prefix_function(S + "#" + S[::-1])[1] / n)
check("Q2 prefix-function work is linear: ops/n <= 4", max(r) <= 4, [round(x, 2) for x in r])
bind_text(2, "", 4, "O(n)", "Q2 complexity")

# ============================== Q3a/b: pairing with a free cheaper item ==============================
def pairings(items):
    if not items:
        yield []
        return
    a = items[0]
    for k in range(1, len(items)):
        rest = items[1:k] + items[k + 1:]
        for p in pairings(rest):
            yield [(a, items[k])] + p


def pay(pairs):
    return sum(max(a, b) for a, b in pairs)


def greedy_pay(items):
    s = sorted(items)
    return sum(s[i] for i in range(1, len(s), 2))


P = [5, 1, 4, 2, 8, 3]
best = min(pay(p) for p in pairings(P))
check("Q3a example: greedy 14 == optimum over all 15 pairings", greedy_pay(P) == best == 14)
bind_numeric(3, "a", 0, best, "Q3a")
bad = 0
for _ in range(1500):
    n = random.choice([2, 4, 6, 8])
    it = [random.randint(1, 20) for _ in range(n)]
    bad += greedy_pay(it) != min(pay(p) for p in pairings(it))
check("Q3a greedy == optimum on 1500 random lists (rechecked while authoring)", bad == 0)
s = sorted(P)
smallest_largest = pay([(s[i], s[-1 - i]) for i in range(len(s) // 2)])
input_order = pay([(P[i], P[i + 1]) for i in range(0, len(P), 2)])
check("Q3a smallest-with-largest and input-order pairing both cost 17", smallest_largest == 17 == input_order)
bind_first(3, "a", 1, "Q3a pairing")
# Q3b: some optimum contains the pair of the two cheapest
bad = 0
for _ in range(1500):
    n = random.choice([2, 4, 6, 8])
    it = [random.randint(1, 20) for _ in range(n)]
    opt = min(pay(p) for p in pairings(it))
    s = sorted(it)
    hit = any(pay(p) == opt and any(sorted(pr) == s[:2] for pr in p) for p in pairings(it))
    bad += not hit
check("Q3b some optimal pairing contains the two cheapest items (1500 random)", bad == 0)
x, y, p2 = 5, 9, 3
check("Q3b example: old (1,5),(3,9) = 14, new (1,3),(5,9) = 12, saving 2 = min(x,y)-p2",
      pay([(1, 5), (3, 9)]) == 14 and pay([(1, 3), (5, 9)]) == 12 and 14 - 12 == min(x, y) - p2 == 2)
bad = 0
for _ in range(3000):
    p1, p2_ = sorted(random.sample(range(1, 10), 2))
    x, y = random.randint(p2_, 20), random.randint(p2_, 20)
    bad += pay([(p1, p2_), (x, y)]) > pay([(p1, x), (p2_, y)])
check("Q3b the swap never costs more (3000 random with x,y >= p2)", bad == 0)
bind_numeric(3, "b", 1, 2, "Q3b saving")
bind_first(3, "b", 0, "Q3b technique")
ol, bug = step(3, "b", 2)["lines"], step(3, "b", 3)
diff = [i for i, (a, b) in enumerate(zip(ol, bug["lines"])) if a != b]
check("Q3b findbug: exactly one line changed, at bugIndex", diff == [bug["bugIndex"]] and len(ol) == len(bug["lines"]))

# ============================== Q4: k < m, k >= n/2 times, m >= n/3 times ==============================
def candidates(a):
    n = len(a)
    s = sorted(a)
    h, t = math.ceil(n / 2), math.ceil(n / 3)
    kc = {s[q - 1] for q in range(h, n + 1, h)}
    mc = {s[q - 1] for q in range(t, n + 1, t)}
    return kc, mc, len(range(h, n + 1, h)) + len(range(t, n + 1, t))


def alg(a):
    n = len(a)
    kc, mc, _ = candidates(a)
    for k in sorted(kc):
        for m in sorted(mc):
            if k < m and a.count(k) * 2 >= n and a.count(m) * 3 >= n:
                return (k, m)
    return None


def brute(a):
    n = len(a)
    return {(k, m) for k in set(a) for m in set(a) if k < m and a.count(k) * 2 >= n and a.count(m) * 3 >= n}


bad = 0
for _ in range(4000):
    n = random.randint(2, 14)
    a = [random.randint(1, random.randint(2, 4)) for _ in range(n)]
    r_ = alg(a)
    bad += (r_ is None) != (not brute(a)) or (r_ is not None and r_ not in brute(a))
check("Q4 candidate algorithm == brute force on 4000 random arrays", bad == 0)
# every value with >= n/2 (resp n/3) copies is a candidate; k need not be min or max
bad = 0
for _ in range(3000):
    n = random.randint(1, 16)
    a = [random.randint(1, 4) for _ in range(n)]
    kc, mc, _ = candidates(a)
    bad += any(a.count(v) * 2 >= n and v not in kc for v in set(a)) or any(a.count(v) * 3 >= n and v not in mc for v in set(a))
check("Q4 every frequent value is among the multiples-of-h / multiples-of-t candidates (3000 random)", bad == 0)
check("Q4 distractors: in 1,2,2,2 the value 2 has >= n/2 copies and is not the minimum; in 1,1,1,2 the value 1 is not the maximum",
      [2].count(2) and [1, 2, 2, 2].count(2) * 2 >= 4 and min([1, 2, 2, 2]) != 2 and [1, 1, 1, 2].count(1) * 2 >= 4 and max([1, 1, 1, 2]) != 1)
bind_first(4, "", 0, "Q4 reasoning")
calls = lambda n: candidates(list(range(n)))[2]
check("Q4 n=12 -> 5 Select calls; never more than 5 for n up to 3000", calls(12) == 5 and max(calls(n) for n in range(1, 3001)) == 5)
bind_numeric(4, "", 1, calls(12), "Q4 calls")
A = [2, 1, 1, 3, 1, 2, 1, 2, 1]
check("Q4 example: unique pair (1,2), k+m = 3", brute(A) == {(1, 2)} and alg(A) == (1, 2))
bind_numeric(4, "", 2, sum(alg(A)), "Q4 k+m")
check("Q4 work: at most 5 Select calls + 5 counting passes + 6 pair tests, all independent of n beyond the linear passes",
      max(calls(n) for n in range(1, 3001)) + 5 + 6 <= 16)
bind_text(4, "", 3, "O(n)", "Q4 complexity")

# ============================== Q5: 2-approximation for vertex cover ==============================
EDGES_SOL = "ab ah af hg gf bi ih id bc cd de gd dj jf fe".split()
E_sol = {frozenset(e) for e in EDGES_SOL}
E_fig = {frozenset((e["u"], e["v"])) for e in GR["22A-C-Q5"]["edges"]}
check("Q5 the solution's 15 edges equal the redrawn figure's edge set", E_sol == E_fig and len(E_sol) == 15)
V = GR["22A-C-Q5"]["vertices"]


def run(order):
    Ep = set(E_sol)
    C = set()
    sizes = []
    for u, v in order:
        assert frozenset((u, v)) in Ep
        C |= {u, v}
        Ep = {e for e in Ep if u not in e and v not in e}
        sizes.append(len(Ep))
    return C, Ep, sizes


C, Ep, sizes = run([("a", "b"), ("h", "g"), ("i", "d"), ("f", "e")])
check("Q5 run: |E'| = 10, 6, 2, 0 and C = {a,b,d,e,f,g,h,i}", sizes == [10, 6, 2, 0] and C == set("abdefghi") and not Ep)
bind_numeric(5, "", 0, sizes[0], "Q5 E' after iteration 1")
bind_numeric(5, "", 1, sizes[1], "Q5 E' after iteration 2")
bind_numeric(5, "", 3, len(C), "Q5 |C|")
# the chosen edges are a maximal matching, on random runs too
bad = 0
for _ in range(500):
    Ep = set(E_sol)
    chosen = []
    while Ep:
        e = random.choice(sorted(Ep, key=sorted))
        u, v = sorted(e)
        chosen.append(e)
        Ep = {f_ for f_ in Ep if u not in f_ and v not in f_}
    disjoint = all(not (a & b) for a, b in itertools.combinations(chosen, 2))
    star = len({tuple(sorted(c))[0] for c in chosen}) >= 1 and not all(chosen[0] & c for c in chosen[1:]) if len(chosen) > 2 else True
    bad += not disjoint
check("Q5 chosen edges are pairwise disjoint on 500 random runs (a matching, not a star)", bad == 0)
vc = min(len(S) for r_ in range(len(V) + 1) for S in itertools.combinations(V, r_) if all(set(S) & e for e in E_sol))
check("Q5 minimum vertex cover = 4 and |C| = 8 <= 2*OPT", vc == 4 and len(C) <= 2 * vc)
bind_numeric(5, "", 4, vc, "Q5 OPT")
bind_first(5, "", 2, "Q5 matching")
ol_ = None

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
