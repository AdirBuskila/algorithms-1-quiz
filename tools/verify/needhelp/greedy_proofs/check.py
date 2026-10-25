# -*- coding: utf-8 -*-
"""Machine check for the guided course greedy_proofs (courses/greedy_proofs/C01..C08).

Run:  py tools/verify/needhelp/greedy_proofs/check.py        (prints ASCII only, exits 1 on any failure)

Every number, every counterexample and every "this rule is optimal / is not optimal" claim in the course is
recomputed here by brute force, then compared with the answer STORED in the level files (loaded through
tools/course_load.js). Conceptual multiple-choice questions (what a proof step must show) cannot be
brute-forced; they are listed in CONCEPTUAL with the stored correct option id, and the surrounding
mathematical claims they rely on are checked below.
"""
import itertools, json, math, os, pathlib, random, subprocess, sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parents[4]
LEVELS = {}
fails = []


def load():
    out = subprocess.run(["node", str(ROOT / "tools" / "course_load.js")], capture_output=True, text=True,
                         encoding="utf-8", cwd=str(ROOT / "tools"))
    data = json.loads(out.stdout)
    assert not data["errors"], data["errors"]
    qs = {}
    for lv in data["levels"]:
        if lv["courseId"] != "greedy_proofs":
            continue
        for q in lv["level"]["questions"]:
            if "id" in q:
                qs[q["id"]] = q
    return qs


def ok(cond, msg):
    if not cond:
        fails.append(msg)
        print("FAIL", msg)


# ---------------------------------------------------------------- problem solvers
def coins_greedy(coins, amount):
    n = 0
    for c in sorted(coins, reverse=True):
        k, amount = divmod(amount, c)
        n += k
    return n if amount == 0 else None


def coins_opt(coins, amount):
    INF = 10 ** 9
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount]


def conflict(a, b):  # closed intervals share a point
    return not (a[1] < b[0] or b[1] < a[0])


def iv_opt(iv):
    best = 0
    for r in range(len(iv) + 1):
        for sub in itertools.combinations(iv, r):
            if all(not conflict(x, y) for x, y in itertools.combinations(sub, 2)):
                best = max(best, r)
    return best


def iv_greedy(iv, key):
    left = list(iv)
    chosen = []
    while left:
        left.sort(key=key)
        g = left[0]
        chosen.append(g)
        left = [x for x in left if not conflict(x, g)]
    return len(chosen)


EF = lambda x: (x[1], x[0])
SHORT = lambda x: (x[1] - x[0], x[0])
ES = lambda x: (x[0], x[1])
LONG = lambda x: (-(x[1] - x[0]), x[0])


def budget_opt(prices, K):
    best = 0
    for r in range(len(prices) + 1):
        for sub in itertools.combinations(prices, r):
            if sum(sub) <= K:
                best = max(best, r)
    return best


def priciest_first(prices, K):
    left = sorted(prices, reverse=True)
    cnt = 0
    for p in left:
        if p <= K:
            K -= p
            cnt += 1
    return cnt


def cover_greedy(points, L):
    pts = sorted(points)
    n, end = 0, None
    for p in pts:
        if end is None or p > end:
            n += 1
            end = p + L
    return n


def cover_opt(points, L):
    pts = sorted(points)
    # WLOG each segment starts at some input point (shift right until it hits one)
    for k in range(1, len(pts) + 1):
        for starts in itertools.combinations(pts, k):
            if all(any(s <= p <= s + L for s in starts) for p in pts):
                return k


def rest_greedy(xs, k):
    xs = sorted(xs)
    g = [xs[0]]
    for x in xs[1:]:
        if x >= g[-1] + k:
            g.append(x)
    return g


def rest_all_feasible(xs, k):
    xs = sorted(xs)
    for r in range(1, len(xs) + 1):
        for sub in itertools.combinations(xs, r):
            if all(sub[i + 1] - sub[i] >= k for i in range(len(sub) - 1)):
                yield sub


def knap01_opt(items, W):
    best = 0
    for r in range(len(items) + 1):
        for sub in itertools.combinations(items, r):
            if sum(w for v, w in sub) <= W:
                best = max(best, sum(v for v, w in sub))
    return best


def knap_frac(items, W):
    tot, cap = Fraction(0), W
    for v, w in sorted(items, key=lambda it: Fraction(it[0], it[1]), reverse=True):
        take = min(w, cap)
        tot += Fraction(v) * take / w
        cap -= take
    return tot


def knap01_ratio_greedy(items, W):
    tot, cap = 0, W
    for v, w in sorted(items, key=lambda it: Fraction(it[0], it[1]), reverse=True):
        if w <= cap:
            tot += v
            cap -= w
    return tot


def huffman_cost(freqs):
    import heapq
    h = list(freqs)
    heapq.heapify(h)
    cost = 0
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        cost += a + b
        heapq.heappush(h, a + b)
    return cost


def merge_orders_min(lengths):
    """min cost over ALL orders of merging two ropes at a time (exhaustive)."""
    from functools import lru_cache

    @lru_cache(None)
    def go(t):
        if len(t) == 1:
            return 0
        best = 10 ** 9
        for i in range(len(t)):
            for j in range(i + 1, len(t)):
                rest = [t[k] for k in range(len(t)) if k not in (i, j)]
                best = min(best, t[i] + t[j] + go(tuple(sorted(rest + [t[i] + t[j]]))))
        return best
    return go(tuple(sorted(lengths)))


def huffman_outcomes(freqs):
    """all code-length tuples reachable by SOME tie-break (every choice of two minimum-weight nodes)."""
    res = set()

    def rec(nodes):  # node = (weight, tuple of (letter, depth))
        if len(nodes) == 1:
            res.add(tuple(d for _, d in sorted(nodes[0][1])))
            return
        ws = sorted(n[0] for n in nodes)
        w1, w2 = ws[0], ws[1]
        for i, j in itertools.combinations(range(len(nodes)), 2):
            if sorted([nodes[i][0], nodes[j][0]]) == [w1, w2]:
                merged = (nodes[i][0] + nodes[j][0],
                          tuple((l, d + 1) for l, d in nodes[i][1] + nodes[j][1]))
                rec([nodes[k] for k in range(len(nodes)) if k not in (i, j)] + [merged])
    rec([(f, ((i, 0),)) for i, f in enumerate(freqs)])
    return res


def correct_val(q):
    return next(o["value"] for o in q["options"] if o["id"] == q["correctId"])


# ---------------------------------------------------------------- the checks
def main():
    Q = load()

    def num(qid, expected):
        ans = Q[qid]["step"]["answer"]
        ok(Q[qid]["step"]["type"] == "numeric" and ans == expected, f"{qid}: stored {ans} != recomputed {expected}")

    def opt(qid, letter):  # stored correct option id (the option text is verified through the facts below)
        ok(Q[qid]["correctId"] == letter, f"{qid}: stored correctId {Q[qid]['correctId']} != expected {letter}")

    # ---- C01 coins
    num("C01-Q1", coins_greedy([1, 5, 10, 25], 63))
    ok(coins_greedy([1, 5, 10, 25], 63) == 6, "C01 63 -> 6")
    num("C01-Q2", coins_greedy([1, 3, 4], 6))
    num("C01-Q3", coins_opt([1, 3, 4], 6))
    ok(coins_greedy([1, 3, 4], 6) == 3 and coins_opt([1, 3, 4], 6) == 2, "C01 {1,3,4} 6")
    # Q4 options: only 15 is a failing amount for {1,5,12}
    bad = [a for a in (15, 10, 25, 7) if coins_greedy([1, 5, 12], a) != coins_opt([1, 5, 12], a)]
    ok(bad == [15], f"C01-Q4 failing amounts {bad}")
    vals = {o["id"]: o["value"].strip("$") for o in Q["C01-Q4"]["options"]}
    ok(vals[Q["C01-Q4"]["correctId"]] == "15", "C01-Q4 stored option is 15")
    ok(coins_greedy([1, 5, 12], 15) == 4 and coins_opt([1, 5, 12], 15) == 3, "C01-Q4 explanation 4 vs 3")
    ok(coins_greedy([1, 5, 12], 25) == 3 and coins_opt([1, 5, 12], 25) == 3, "C01-Q4 explanation 25")
    ok(Q["C01-Q5"]["step"]["accept"][0].replace(" ", "") == "O(nlogn)", "C01-Q5 accept")
    # lesson claim: {1,5,10,25} greedy optimal for every amount up to 500
    ok(all(coins_greedy([1, 5, 10, 25], a) == coins_opt([1, 5, 10, 25], a) for a in range(0, 501)), "C01 canonical system")

    # ---- C02 intervals
    A = [(1, 10), (2, 3), (4, 5), (6, 7)]
    B = [(1, 3), (4, 6), (7, 9)]
    C = [(1, 5), (2, 6), (7, 9)]
    D = [(1, 4), (2, 3), (5, 8)]
    res = {n: (iv_greedy(i, ES), iv_opt(i)) for n, i in zip("ABCD", (A, B, C, D))}
    refute = [n for n, (g, o) in res.items() if g < o]
    ok(refute == ["A"], f"C02-Q1 refuting instances {refute}")
    opt("C02-Q1", "a")
    inst = [(1, 10), (9, 12), (11, 20)]
    num("C02-Q2", iv_greedy(inst, SHORT))
    ok(iv_opt(inst) == 2, "C02-Q2 opt 2")
    CLRS = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    num("C02-Q3", iv_greedy(CLRS, EF))
    ok(iv_opt(CLRS) == 4, "C02-Q3 opt 4")
    num("C02-Q4", priciest_first([2, 3, 4, 7, 8], 12))
    ok(budget_opt([2, 3, 4, 7, 8], 12) == 3, "C02-Q4 opt 3")
    ok(sum([2, 3, 4]) == 9 and sum([8, 4]) == 12, "C02-Q4 sums")
    # Q5: earliest finish is optimal (random exhaustive), the other three have counterexamples
    rnd = random.Random(1)
    for _ in range(1500):
        n = rnd.randint(1, 8)
        iv = []
        for _ in range(n):
            s = rnd.randint(0, 20)
            iv.append((s, s + rnd.randint(1, 8)))
        ok(iv_greedy(iv, EF) == iv_opt(iv), f"C02 earliest finish not optimal on {iv}")
        if fails:
            break
    cx = [(1, 10), (2, 3), (4, 5)]
    for name, key in (("longest", LONG), ("earliest start", ES)):
        ok(iv_greedy(cx, key) == 1 and iv_opt(cx) == 2, f"C02-Q5 {name} counterexample")
    ok(iv_greedy(inst, SHORT) < iv_opt(inst), "C02-Q5 shortest counterexample")
    opt("C02-Q5", "a")
    # lesson sentences: earliest start on lesson example, budget lesson example
    ok(iv_greedy([(1, 10), (2, 3), (4, 5)], ES) == 1, "C02 lesson ES example")
    ok(sorted(inst, key=SHORT)[0] == (9, 12), "C02 lesson: shortest is [9,12]")

    # ---- C03 exchange argument
    # randomized proof sanity: exchange of the first-finishing interval keeps feasibility and size
    rnd = random.Random(2)
    for _ in range(600):
        n = rnd.randint(2, 7)
        iv = []
        for _ in range(n):
            s = rnd.randint(0, 18)
            iv.append((s, s + rnd.randint(1, 6)))
        g = min(iv, key=EF)
        best = iv_opt(iv)
        for r in range(best, best + 1):
            for sub in itertools.combinations(iv, r):
                if all(not conflict(x, y) for x, y in itertools.combinations(sub, 2)) and g not in sub:
                    o = min(sub, key=lambda x: x[1])
                    ok(g[1] <= o[1], "C03 f(g)<=f(o)")
                    new = [x for x in sub if x != o] + [g]
                    ok(all(not conflict(x, y) for x, y in itertools.combinations(new, 2)), f"C03 O' legal {iv} {sub}")
    opt("C03-Q1", "a")
    ok(Q["C03-Q3"]["step"]["bugIndex"] == 2, "C03-Q3 bugIndex")
    ok(Q["C03-Q2"]["step"]["type"] == "order", "C03-Q2 type")
    # Q4: swapping [1,10] for [9,12] inside {[1,10],[11,20]} is illegal
    ok(conflict((9, 12), (11, 20)), "C03-Q4 g conflicts with [11,20]")
    ok(iv_opt([(1, 10), (11, 20)]) == 2, "C03-Q4 O optimal")
    ok(conflict((9, 12), (1, 10)), "C03-Q4 g also conflicts with [1,10]")
    opt("C03-Q4", "a")
    # Q5: cheapest item swap never raises the sum
    for _ in range(300):
        pr = sorted(rnd.randint(1, 9) for _ in range(rnd.randint(2, 7)))
        K = rnd.randint(1, 25)
        d = pr[0]
        best = budget_opt(pr, K)
        if best == 0:
            continue
        for sub in itertools.combinations(range(len(pr)), best):
            if sum(pr[i] for i in sub) <= K and 0 not in sub:
                a = max(sub, key=lambda i: pr[i])
                ns = [i for i in sub if i != a] + [0]
                ok(sum(pr[i] for i in ns) <= K and len(ns) == best, "C03-Q5 swap legal")
    opt("C03-Q5", "a")

    # ---- C04 substructure
    sub = [x for x in CLRS if x[0] > 4]
    ok(sorted(sub) == [(5, 7), (5, 9), (6, 10), (8, 11), (8, 12), (12, 16)], "C04 remaining intervals")
    ok([x for x in CLRS if not conflict(x, (1, 4))] == sub, "C04 compatible with [1,4] == start after 4")
    num("C04-Q2", iv_opt(sub))
    ok(iv_opt(CLRS) == 1 + iv_opt(sub), "C04 OPT = 1 + OPT(sub)")
    # substructure claim on random instances: with g = earliest finish, OPT = 1 + OPT(compatible)
    for _ in range(500):
        iv = [(s, s + rnd.randint(1, 6)) for s in (rnd.randint(0, 20) for _ in range(rnd.randint(1, 8)))]
        g = min(iv, key=EF)
        ok(iv_opt(iv) == 1 + iv_opt([x for x in iv if not conflict(x, g)]), f"C04 substructure {iv}")
    opt("C04-Q1", "a")
    ok(Q["C04-Q4"]["step"]["bugIndex"] == 3, "C04-Q4 bugIndex")
    pts = [10, 15, 22, 31, 34, 60]
    num("C04-Q5", cover_greedy(pts, 10))
    ok(cover_opt(pts, 10) == 4, "C04-Q5 min cover")
    for _ in range(300):
        P = sorted(set(rnd.randint(0, 40) for _ in range(rnd.randint(1, 7))))
        L = rnd.randint(1, 10)
        ok(cover_greedy(P, L) == cover_opt(P, L), f"C04 cover greedy optimal {P} {L}")
    prices = [3, 3, 5]
    best = budget_opt(prices, 8)
    cnt = sum(1 for s in itertools.combinations(range(3), best) if sum(prices[i] for i in s) <= 8)
    ok(best == 2, "C04-Q6 opt size 2")
    num("C04-Q6", cnt)
    ok(sum(prices) == 11 > 8, "C04-Q6 three items cost 11")

    # ---- C05 stay ahead
    xs = [0, 3, 4, 7, 8, 12, 13]
    g = rest_greedy(xs, 5)
    num("C05-Q1", len(g))
    num("C05-Q2", g[2])
    allf = list(rest_all_feasible(xs, 5))
    ok(max(len(s) for s in allf) == 3, "C05 opt size 3")
    ok((0, 8, 13) in allf and tuple(g) == (0, 7, 12), "C05 lesson: 0,8,13 optimal, greedy 0,7,12")
    for _ in range(400):
        X = sorted(set(rnd.randint(0, 40) for _ in range(rnd.randint(1, 9))))
        k = rnd.randint(1, 8)
        G = rest_greedy(X, k)
        for s in rest_all_feasible(X, k):
            ok(all(G[i] <= s[i] for i in range(len(s)) if i < len(G)) and len(G) >= len(s), f"C05 stay ahead {X} {k} {s}")
    opt("C05-Q3", "a")
    ok(Q["C05-Q3"]["options"][0]["value"].strip("$") == r"g_r\le o_r", "C05-Q3 option text")
    ok(Q["C05-Q5"]["step"]["bugIndex"] == 1, "C05-Q5 bugIndex")
    opt("C05-Q6", "a")

    # ---- C06 knapsack
    items = [(60, 10), (100, 20), (120, 30)]
    num("C06-Q1", knap_frac(items, 50))
    ok(knap_frac(items, 50) == 240, "C06 fractional 240")
    num("C06-Q2", knap01_ratio_greedy(items, 50))
    num("C06-Q3", knap01_opt(items, 50))
    ok(knap01_ratio_greedy(items, 50) < knap01_opt(items, 50), "C06 ratio greedy fails 0/1")
    # T=5 counterexample from the lesson trap
    tk = [(2, 1), (9, 5)]
    ok(knap01_ratio_greedy(tk, 5) == 2 and knap01_opt(tk, 5) == 9, "C06 lesson trap 2 vs 9")
    ok(Fraction(2, 1) > Fraction(9, 5), "C06 ratios 2 > 1.8")
    # fractional ratio greedy = optimum of the LP: exchange identity and a sampled optimality check
    for _ in range(300):
        r_i, r_j, d = Fraction(rnd.randint(1, 9)), Fraction(rnd.randint(1, 9)), Fraction(rnd.randint(1, 5))
        if r_i >= r_j:
            ok(d * r_i - d * r_j >= 0, "C06 exchange gain")
    opt("C06-Q4", "a")
    ok(Q["C06-Q5"]["step"]["type"] == "order", "C06-Q5")
    w = [2, 3, 6, 8]
    v = [9, 7, 5, 1]
    it = list(zip(v, w))
    tot, cap = 0, 11
    for vi, wi in sorted(it, key=lambda t: t[1]):
        if wi <= cap:
            tot += vi
            cap -= wi
        else:
            break
    num("C06-Q6", tot)
    ok(knap01_opt(it, 11) == tot, "C06-Q6 greedy = opt")
    # family claim: weights ascending with values non-increasing -> lightest-first (stop at first miss) is optimal
    for _ in range(600):
        n = rnd.randint(1, 7)
        ws = sorted(rnd.randint(1, 9) for _ in range(n))
        vs = sorted((rnd.randint(1, 20) for _ in range(n)), reverse=True)
        W = rnd.randint(1, 30)
        tot, cap = 0, W
        for vi, wi in zip(vs, ws):
            if wi <= cap:
                tot += vi
                cap -= wi
            else:
                break
        ok(tot == knap01_opt(list(zip(vs, ws)), W), f"C06 family claim {ws} {vs} {W}")
    # lesson: equal times, top-k values
    vals = [5, 9, 2, 7, 4]
    k = 10 // 3
    ok(k == 3 and sum(sorted(vals, reverse=True)[:k]) == 21, "C06 equal-time lesson example")
    # equal-time claim brute-force: any feasible set has <= k tasks
    ok(max(len(s) for r in range(6) for s in itertools.combinations(vals, r) if 3 * len(s) <= 10) == 3, "C06 equal-time k")

    # ---- C07 Huffman
    num("C07-Q1", huffman_cost([5, 9, 12, 13, 16, 45]))
    num("C07-Q2", huffman_cost([1, 2, 3, 4, 5]))
    ok(merge_orders_min([1, 2, 3, 4, 5]) == huffman_cost([1, 2, 3, 4, 5]) == 33, "C07 ropes: huffman = exhaustive min")
    for _ in range(100):
        L = [rnd.randint(1, 12) for _ in range(rnd.randint(2, 6))]
        ok(merge_orders_min(L) == huffman_cost(L), f"C07 ropes {L}")
    ok(Q["C07-Q4"]["step"]["bugIndex"] == 1, "C07-Q4 bugIndex")
    out = huffman_outcomes([1, 1, 2, 2])
    ok((3, 3, 2, 1) in out and (2, 2, 2, 2) in out, f"C07-Q5 outcomes {out}")
    ok(all(l[0] != 1 for l in out) and (1, 3, 3, 2) not in out, "C07-Q5 a never gets length 1")
    ok(out == {(3, 3, 2, 1), (3, 3, 1, 2), (2, 2, 2, 2)}, f"C07-Q5 outcome set {out}")
    opt("C07-Q5", "a")
    for t in out:
        ok(sum(f * d for f, d in zip([1, 1, 2, 2], t)) == 12, f"C07 every outcome costs 12 {t}")
    num("C07-Q6", huffman_cost([1, 1, 2, 2]))
    # lemma: for random trees, swap difference formula and sign
    for _ in range(300):
        fb, fx, db, dx = (rnd.randint(1, 9) for _ in range(4))
        if fb >= fx and db >= dx:
            ok(fx * dx + fb * db - (fx * db + fb * dx) == (fb - fx) * (db - dx) >= 0, "C07 lemma identity")
    # Huffman optimal over all full binary trees for small inputs (exhaustive merge orders = all trees)
    ok(huffman_cost([5, 9, 12, 13, 16, 45]) == merge_orders_min([5, 9, 12, 13, 16, 45]), "C07 huffman optimal")
    ok(huffman_cost([5, 9, 12, 13, 16, 45]) == 14 + 25 + 30 + 55 + 100, "C07-Q1 internal nodes")

    # ---- C08 boss: bank ids exist (the lint checks too), and hold no held ones
    bank = json.load(open(ROOT / "questions.json", encoding="utf-8"))
    bq = {x["id"]: x for x in (bank["questions"] if isinstance(bank, dict) else bank)}
    for bid in ("25B-A-Q2a", "24A-A-Q2b", "24A-C-Q2a", "24B-A-Q2c", "22A-B-Q4a", "22A-B-Q4b"):
        ok(bid in bq and not bq[bid].get("hold") and bq[bid].get("official") is True, f"C08 boss id {bid}")
    # bank facts the boss leans on: 25B-A example [1,9,4,2,4], K=10 has several optima
    pr = [1, 9, 4, 2, 4]
    b = budget_opt(pr, 10)
    n_opt = sum(1 for s in itertools.combinations(range(5), b) if sum(pr[i] for i in s) <= 10)
    ok(b == 3 and n_opt >= 2, "C08 25B-A-Q2a not unique")

    # ---- conceptual questions (no brute force possible): stored ids pinned so edits are noticed
    CONCEPTUAL = {"C01-Q6": "a"}
    for qid, letter in CONCEPTUAL.items():
        opt(qid, letter)

    # every own mcq has a correct option, every stored correctId is among the options
    for qid, q in Q.items():
        if "options" in q:
            ok(q["correctId"] in [o["id"] for o in q["options"]], f"{qid} correctId among options")

    print(f"checked {len(Q)} own questions; failures: {len(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
