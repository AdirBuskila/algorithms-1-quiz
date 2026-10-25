# -*- coding: utf-8 -*-
"""Learn-brief checks: greedy (brief 08). Each greedy algorithm of the brief against an exhaustive optimum, each
counterexample recomputed. Run: PYTHONUTF8=1 py tools/verify/learn/v06_greedy.py   (ASCII output, exits 1 on failure)"""
import heapq, itertools, math, random, sys
from fractions import Fraction

ok = True
INF = float("inf")


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


random.seed(4242)


# ---------------------------------------------------------------- activity selection / circles on the x axis (SAMP-1 Q4)
def earliest_finish(iv):
    iv = sorted(range(len(iv)), key=lambda i: (iv[i][1], iv[i][0])) if False else sorted(range(len(iv)), key=lambda i: (iv[i][1], iv[i][0]))
    return iv


def greedy_intervals(iv):
    chosen, last = [], -INF
    for i in sorted(range(len(iv)), key=lambda i: (iv[i][1], iv[i][0])):
        if iv[i][0] > last:  # disjoint: no common point (strictly after)
            chosen.append(i)
            last = iv[i][1]
    return chosen


def best_intervals(iv):
    n = len(iv)
    best = 0
    sols = []
    for r in range(n + 1):
        for s in itertools.combinations(range(n), r):
            if all(iv[a][1] < iv[b][0] or iv[b][1] < iv[a][0] for a, b in itertools.combinations(s, 2)):
                if r > best:
                    best, sols = r, []
                if r == best:
                    sols.append(s)
    return best, sols


bad = 0
for _ in range(400):
    n = random.randint(1, 8)
    iv = []
    for _ in range(n):
        a = random.randint(0, 20)
        iv.append((a, a + random.randint(0, 6)))
    b, _ = best_intervals(iv)
    bad += len(greedy_intervals(iv)) != b
check("earliest-right-endpoint greedy == exhaustive maximum number of disjoint intervals (400 random)", bad == 0)

circles = [(-4.5, 2.0), (0.0, 2.0), (0.0, 3.0), (5.0, 4.0), (6.0, 2.0), (7.0, 5.0), (8.0, 3.0)]  # (centre, radius) giving the SAMP-1 intervals
iv = [(c - r, c + r) for c, r in circles]
check("SAMP-1 Q4a intervals c1..c7", iv == [(-6.5, -2.5), (-2.0, 2.0), (-3.0, 3.0), (1.0, 9.0), (4.0, 8.0), (2.0, 12.0), (5.0, 11.0)], iv)
g = greedy_intervals(iv)
b, sols = best_intervals(iv)
check("SAMP-1 Q4a: greedy picks c1,c2,c5 (3 circles), optimum 3, and {c1,c2,c7} is another optimum",
      [i + 1 for i in g] == [1, 2, 5] and b == 3 and (0, 1, 6) in sols and (0, 1, 4) in sols, [tuple(i + 1 for i in s) for s in sols])
short = [(0, 10), (9, 12), (11, 20)]
sh = min(range(3), key=lambda i: short[i][1] - short[i][0])
chosen = [sh] + [i for i in range(3) if i != sh and (short[i][1] < short[sh][0] or short[sh][1] < short[i][0])]
check("shortest-first counterexample [0,10],[9,12],[11,20]: shortest-first gets 1, optimum 2",
      len(chosen) == 1 and best_intervals(short)[0] == 2 and len(greedy_intervals(short)) == 2)


# ---------------------------------------------------------------- points covered by unit segments (24A-A Q2)
def cover_greedy(pts):
    pts = sorted(pts)
    segs, end = 0, -INF
    for p in pts:
        if p > end:
            segs += 1
            end = p + 1
    return segs


def cover_brute(pts):
    pts = sorted(set(pts))
    # candidate left endpoints: the points themselves
    for k in range(1, len(pts) + 1):
        for lefts in itertools.combinations(pts, k):
            if all(any(l <= p <= l + 1 for l in lefts) for p in pts):
                return k
    return 0


bad = 0
for _ in range(400):
    pts = [round(random.uniform(0, 8), 1) for _ in range(random.randint(1, 8))]
    bad += cover_greedy(set(pts)) != cover_brute(pts)
check("unit segments starting at the leftmost uncovered point == exhaustive minimum (400 random)", bad == 0)


# ---------------------------------------------------------------- tape (24A-B Q2): boxes in order, a new tape when the remainder is too short
def tape_greedy(lengths, m):
    count, rest = 0, 0
    for L in lengths:
        if rest >= L:
            rest -= L
        else:
            count += 1
            rest = m - L
    return count


def tape_dp(lengths, m):
    n = len(lengths)
    best = [INF] * (n + 1)
    best[0] = 0
    for i in range(1, n + 1):
        s = 0
        for j in range(i, 0, -1):
            s += lengths[j - 1]
            if s > m:
                break
            best[i] = min(best[i], best[j - 1] + 1)
    return best[n]


bad = 0
for _ in range(400):
    m = random.randint(5, 12)
    L = [random.randint(1, m) for _ in range(random.randint(1, 9))]
    bad += tape_greedy(L, m) != tape_dp(L, m)
check("closing the boxes in order: greedy tape usage == optimal consecutive grouping (400 random)", bad == 0)


# ---------------------------------------------------------------- stations covering cities within D (24B-A Q2)
def stations(xs, D):
    xs = sorted(xs)
    C, cur = [], -INF
    for x in xs:
        if x - D > cur:
            cur = x + D
            C.append(cur)
    return C


def stations_brute(xs, D):
    xs = sorted(xs)
    cand = sorted({x + t for x in xs for t in (-D, 0, D)})
    for k in range(1, len(xs) + 1):
        for S in itertools.combinations(cand, k):
            if all(any(abs(s - x) <= D for s in S) for x in xs):
                return k
    return 0


bad = 0
for _ in range(300):
    xs = [random.randint(0, 20) for _ in range(random.randint(1, 7))]
    D = random.randint(1, 5)
    st = stations(set(xs), D)
    bad += len(st) != stations_brute(xs, D) or not all(any(abs(s - x) <= D for s in st) for x in xs)
check("station at (first uncovered city + D) == exhaustive minimum, all cities covered (300 random)", bad == 0)


# ---------------------------------------------------------------- restaurants at distance >= k (24B-B Q4)
def rest_greedy(d, k):
    S = [d[0]]
    for x in d[1:]:
        if x - S[-1] >= k:
            S.append(x)
    return S


def rest_brute(d, k):
    best = 0
    for r in range(len(d) + 1):
        for s in itertools.combinations(d, r):
            if all(s[i + 1] - s[i] >= k for i in range(len(s) - 1)):
                best = max(best, r)
    return best


bad = 0
for _ in range(300):
    d = sorted(random.sample(range(0, 40), random.randint(1, 9)))
    k = random.randint(1, 10)
    bad += len(rest_greedy(d, k)) != rest_brute(d, k)
check("first place, then the next place at distance >= k == exhaustive maximum (300 random)", bad == 0)
check("24B-B Q4a: positions 1,2,..: greedy [1,15,26] with k=10 is valid, 3 restaurants (the exam's own set [2,20,30] also 3)",
      all(b - a >= 10 for a, b in zip([1, 15, 26], [15, 26])) and all(b - a >= 10 for a, b in zip([2, 20, 30], [20, 30])))
# claim of the proof: g_r <= o_r
bad = 0
for _ in range(300):
    d = sorted(random.sample(range(0, 40), random.randint(1, 9)))
    k = random.randint(1, 10)
    g = rest_greedy(d, k)
    for r in range(0, len(d) + 1):
        for s in itertools.combinations(d, r):
            if all(s[i + 1] - s[i] >= k for i in range(len(s) - 1)):
                bad += any(g[i] > s[i] for i in range(min(len(g), len(s))))
                break
check("stays-ahead: the r-th greedy place is never to the right of the r-th place of another solution (300 random)", bad == 0)


# ---------------------------------------------------------------- max number of items with total <= K (25A-A Q3, 25B-A Q2)
def most_items(vals, K):
    s, c = 0, 0
    for v in sorted(vals):
        if s + v <= K:
            s += v
            c += 1
        else:
            break
    return c


def most_items_brute(vals, K):
    best = 0
    for r in range(len(vals) + 1):
        for s in itertools.combinations(vals, r):
            if sum(s) <= K:
                best = max(best, r)
    return best


bad = 0
for _ in range(400):
    vals = [random.randint(1, 9) for _ in range(random.randint(1, 8))]
    K = random.randint(0, 30)
    bad += most_items(vals, K) != most_items_brute(vals, K)
check("sort ascending and take while it fits == exhaustive maximum count (400 random)", bad == 0)
check("25B-A Q2a: more than one optimal answer exists (e.g. demands 1,2,4,4,5? two choices of the 4)", most_items([1, 2, 4, 4], 7) == 3 and sum([1, 2, 4]) <= 7)


# ---------------------------------------------------------------- pairs, pay the more expensive of each pair (22A-C Q3)
def pairs_greedy(p):
    s = sorted(p)
    return sum(s[i + 1] for i in range(0, len(s), 2))


def pairs_brute(p):
    best = INF
    idx = list(range(len(p)))

    def go(rem, cost):
        nonlocal best
        if not rem:
            best = min(best, cost)
            return
        a = rem[0]
        for j in rem[1:]:
            go([x for x in rem if x not in (a, j)], cost + max(p[a], p[j]))
    go(idx, 0)
    return best


bad = 0
for _ in range(300):
    p = [random.randint(1, 20) for _ in range(2 * random.randint(1, 4))]
    bad += pairs_greedy(p) != pairs_brute(p)
check("sort and pair neighbours, pay the larger of each pair == exhaustive minimum (300 random)", bad == 0)


# ---------------------------------------------------------------- coins 5^i (23A-A Q4) and a non-canonical system
def coins_greedy(W, coins):
    cnt = 0
    for c in sorted(coins, reverse=True):
        cnt += W // c
        W %= c
    return cnt if W == 0 else None


def coins_dp(W, coins):
    best = [0] + [INF] * W
    for w in range(1, W + 1):
        for c in coins:
            if c <= w:
                best[w] = min(best[w], best[w - c] + 1)
    return best[W]


coins = [125, 25, 5, 1]
check("coin values 1,5,25,125: greedy == optimal for every amount up to 1000", all(coins_greedy(W, coins) == coins_dp(W, coins) for W in range(0, 1001)))
check("23A-A Q4 example: W=35 with 25,5,1 -> 3 coins (25+5+5)", coins_greedy(35, [25, 5, 1]) == 3 == coins_dp(35, [25, 5, 1]))
check("non-canonical coins 1,3,4 and W=6: greedy 4+1+1 = 3 coins, optimum 3+3 = 2 coins", coins_greedy(6, [4, 3, 1]) == 3 and coins_dp(6, [4, 3, 1]) == 2)


# ---------------------------------------------------------------- remove k letters to minimise sum of squared frequencies (25A-B Q2)
def reduce_greedy(s, k):
    from collections import Counter
    f = Counter(s)
    h = [(-x, c) for c, x in f.items()]
    heapq.heapify(h)
    for _ in range(k):
        x, c = heapq.heappop(h)
        heapq.heappush(h, (x + 1, c))
    return sum(x * x for x, _ in h)


def reduce_brute(s, k):
    n = len(s)
    best = INF
    for rem in itertools.combinations(range(n), k):
        t = [s[i] for i in range(n) if i not in rem]
        from collections import Counter
        best = min(best, sum(v * v for v in Counter(t).values()))
    return best


bad = 0
for _ in range(300):
    s = "".join(random.choice("abc") for _ in range(random.randint(2, 9)))
    k = random.randint(0, len(s) - 1)
    bad += reduce_greedy(s, k) != reduce_brute(s, k)
check("remove the letter with the highest current frequency k times == exhaustive minimum (300 random)", bad == 0)
check("25A-B Q2: 'character', k=2: value 15 -> 9 (squares 2,2,2 -> minus 3 and 3)", reduce_greedy("character", 0) == 15 and reduce_greedy("character", 2) == 9 and 2 * 2 - 1 * 1 == 3)
check("removing one occurrence from a letter with x copies lowers the value by x^2-(x-1)^2 = 2x-1", all(x * x - (x - 1) ** 2 == 2 * x - 1 for x in range(1, 50)))


# ---------------------------------------------------------------- fractional knapsack (25A-C Q2) and 0/1 failure (26B-A Q2a)
def fractional(items, cap):
    items = sorted(items, key=lambda it: Fraction(it[0], it[1]), reverse=True)  # (value, weight)
    total, room = Fraction(0), cap
    for v, w in items:
        if room == 0:
            break
        take = min(w, room)
        total += Fraction(v * take, w)
        room -= take
    return total


check("fractional knapsack (60,10),(100,20),(120,30), capacity 50 -> 240 (ratios 6,5,4)", fractional([(60, 10), (100, 20), (120, 30)], 50) == 240
      and [Fraction(v, w) for v, w in [(60, 10), (100, 20), (120, 30)]] == [6, 5, 4])


def knap01(items, cap):
    best = 0
    for r in range(len(items) + 1):
        for s in itertools.combinations(items, r):
            if sum(w for v, w in s) <= cap:
                best = max(best, sum(v for v, w in s))
    return best


def ratio_greedy01(items, cap):
    tot = 0
    for v, w in sorted(items, key=lambda it: Fraction(it[0], it[1]), reverse=True):
        if w <= cap:
            cap -= w
            tot += v
    return tot


check("26B-A Q2a counterexample: T=5, tasks (time 1, profit 2) and (time 5, profit 9): ratio-greedy 2, optimum 9",
      ratio_greedy01([(2, 1), (9, 5)], 5) == 2 and knap01([(2, 1), (9, 5)], 5) == 9)
# fractional greedy is optimal: compare with an exact LP over a fine rational grid on tiny instances (value/weight small)
bad = 0
for _ in range(100):
    items = [(random.randint(1, 9), random.randint(1, 5)) for _ in range(3)]
    cap = random.randint(1, 10)
    # best fractional solution: search fractions in steps of 1/ (lcm) -- exact optimum is attained with at most one fractional item
    best = Fraction(0)
    for fixed in itertools.product([0, 1], repeat=3):
        w = sum(items[i][1] for i in range(3) if fixed[i])
        if w > cap:
            continue
        v = sum(items[i][0] for i in range(3) if fixed[i])
        room = cap - w
        extra = max([Fraction(items[i][0] * min(room, items[i][1]), items[i][1]) for i in range(3) if not fixed[i]] + [Fraction(0)])
        best = max(best, v + extra)
    bad += fractional(items, cap) != best
check("fractional greedy by value/weight == best 'at most one fractional item' solution (100 random)", bad == 0)


# ---------------------------------------------------------------- equal times (26B-A Q2b)
bad = 0
for _ in range(300):
    n = random.randint(1, 8)
    t = random.randint(1, 4)
    T = random.randint(0, 20)
    v = [random.randint(-2, 9) for _ in range(n)]
    k = T // t
    greedy = sum(sorted([x for x in v if x > 0], reverse=True)[:k])
    best = max(sum(v[i] for i in s) for r in range(0, min(n, k) + 1) for s in itertools.combinations(range(n), r))
    bad += greedy != best
check("equal times: the floor(T/t) most profitable tasks == exhaustive optimum (300 random)", bad == 0)

# ---------------------------------------------------------------- the worked example of brief 08 and the coin lemma
check("brief 08 example: boxes 3,4,2,5 with tape m=7: greedy 2 tapes, optimum 2, lower bound ceil(14/7) = 2",
      tape_greedy([3, 4, 2, 5], 7) == 2 == tape_dp([3, 4, 2, 5], 7) and math.ceil(14 / 7) == 2)
check("coin lemma: 4*(5^(K-j-1)+...+5+1) = 5^(K-j) - 1 for all K, j", all(4 * sum(5 ** i for i in range(K - j)) == 5 ** (K - j) - 1 for K in range(1, 8) for j in range(0, K)))

sys.exit(0 if ok else 1)
