# -*- coding: utf-8 -*-
"""Step-author checks for 23B-C (algorithms-1): every expected value of the steps in gen_23B-C.py is recomputed here,
and every wrong option is shown to fail on a concrete input. The Huffman step is also checked by COST: the target code
must have the optimal cost exactly for the accepted pairs.
Run: PYTHONUTF8=1 py tools/verify/23B-C/steps_23BC.py     (ASCII output)"""
import heapq, itertools, json, pathlib, random

ROOT = pathlib.Path(__file__).resolve().parents[3]
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


random.seed(23)


# ============================================================ Q1a prefix function
def pi_of(P):
    pi = [0] * len(P)
    k = 0
    for q in range(1, len(P)):
        while k and P[k] != P[q]:
            k = pi[k - 1]
        if P[k] == P[q]:
            k += 1
        pi[q] = k
    return pi


check("Q1a pi of aaaab ends in 0", pi_of("aaaab")[-1] == 0 and pi_of("aaaab") == [0, 1, 2, 3, 0])
check("Q1a pi of aaaaa ends in 4", pi_of("aaaaa")[-1] == 4)
ALPHA = "abcde"
five = ["".join(p) for p in itertools.product(ALPHA, repeat=5)]
check("Q1a no string of length 5 has pi = 0,1,2,3,1", not any(pi_of(p) == [0, 1, 2, 3, 1] for p in five))
four = ["".join(p) for p in itertools.product(ALPHA, repeat=4) if pi_of("".join(p)) == [0, 1, 2, 3]]
check("Q1a pi = 0,1,2,3 on 4 letters forces aaaa", four == ["aaaa", "bbbb", "cccc", "dddd", "eeee"] and all(len(set(x)) == 1 for x in four))
vals = {pi_of("aaaa" + c)[-1] for c in ALPHA} | {pi_of(x + "aaaa")[-1] for x in ALPHA}
check("Q1a with P[1..4]=aaaa, pi(5) is in {0,4} only", {pi_of("aaaa" + c)[-1] for c in ALPHA} == {0, 4})
check("Q1a pi(1) is always 0", all(pi_of(p)[0] == 0 for p in five))

# ============================================================ Q1b suffix array / tree
S = "algogoal"
SA = sorted(range(1, len(S) + 1), key=lambda i: S[i - 1:])
check("Q1b SA = [7,1,5,3,8,2,6,4]", SA == [7, 1, 5, 3, 8, 2, 6, 4])
check("Q1b SA[3] = 5 and the first suffix starts at 7 (without the terminator)", SA[2] == 5 and SA[0] == 7)
T = S + "$"


def build(sufs):
    groups = {}
    for s, i in sufs:
        groups.setdefault(s[0], []).append((s, i))
    node = {}
    for ch, grp in groups.items():
        if len(grp) == 1:
            node[grp[0][0]] = grp[0][1]
            continue
        lcp = grp[0][0]
        for s, _ in grp:
            k = 0
            while k < min(len(lcp), len(s)) and lcp[k] == s[k]:
                k += 1
            lcp = lcp[:k]
        node[lcp] = build([(s[len(lcp):], i) for s, i in grp])
    return node


def count(node):
    leaves = internal = 0
    for v in node.values():
        if isinstance(v, int):
            leaves += 1
        else:
            internal += 1
            a, b = count(v)
            leaves += a
            internal += b
    return leaves, internal


tree = build([(T[i:], i + 1) for i in range(len(T))])
lv, inn = count(tree)
check("Q1b suffix tree has 9 leaves and 4 internal nodes besides the root", (lv, inn) == (9, 4), str((lv, inn)))

# ============================================================ Q2a circular max
def kadane(A):
    best = cur = A[0]
    for x in A[1:]:
        cur = max(x, cur + x); best = max(best, cur)
    return best


def circ(A):
    m1 = kadane(A)
    if m1 < 0:
        return m1
    return max(m1, sum(A) - (-kadane([-x for x in A])))


def circ_brute(A):
    n = len(A)
    return max(sum(A[(s + t) % n] for t in range(L)) for s in range(n) for L in range(1, n + 1))


EX = [4, -6, 5, -6, 10, -5, 3]
check("Q2a minimal segment of the example is -7, total - min = 12", -kadane([-x for x in EX]) == -7 and sum(EX) == 5 and sum(EX) + 7 == 12)
A2 = [8, -1, -2, 7]
check("Q2a circular maximum of [8,-1,-2,7] is 15 (brute force)", circ_brute(A2) == 15 == circ(A2))
A3 = [-3, -1, -2]
check("Q2a all negative [-3,-1,-2]: answer -1; 'total - minSeg' would give 0, which no non-empty segment sums to",
      circ_brute(A3) == -1 and sum(A3) - (-kadane([-x for x in A3])) == 0 and all(
          sum(A3[(s + t) % 3] for t in range(L)) != 0 for s in range(3) for L in range(1, 4)))
check("Q2a formula equals brute force (2000 random)", all(
    circ(A) == circ_brute(A) for A in ([random.randint(-9, 9) for _ in range(random.randint(1, 8))] for _ in range(2000))))
check("Q2a ignoring wrapping (Kadane only) fails on some array", any(
    kadane(A) != circ_brute(A) for A in ([random.randint(-9, 9) for _ in range(random.randint(2, 8))] for _ in range(300))))
check("Q2a total - minSeg alone (no Kadane) fails on some array", any(
    sum(A) + kadane([-x for x in A]) != circ_brute(A) for A in ([random.randint(-9, 9) for _ in range(random.randint(2, 8))] for _ in range(300))))

# ============================================================ Q2b sort except position K
def sort_but_k(A, K):
    x = A[K - 1]
    B = sorted(A[:K - 1] + A[K:])
    return B[:K - 1] + [x] + B[K - 1:]


def valid(A, K, out):
    rest = out[:K - 1] + out[K:]
    return out[K - 1] == A[K - 1] and rest == sorted(rest) and sorted(out) == sorted(A)


def sort_all_swap_back(A, K):  # sort everything, then swap x back to position K
    x = A[K - 1]
    B = sorted(A)
    i = B.index(x)
    B[i], B[K - 1] = B[K - 1], B[i]
    return B


def sort_parts(A, K):  # sort left of K and right of K separately
    return sorted(A[:K - 1]) + [A[K - 1]] + sorted(A[K:])


A4, K4 = [9, -2, 6, 0, 5, 8, 1], 3
out = sort_but_k(A4, K4)
check("Q2b example 2: [9,-2,6,0,5,8,1], K=3 -> [-2,0,6,1,5,8,9], 4th element 1", out == [-2, 0, 6, 1, 5, 8, 9] and out[3] == 1 and valid(A4, K4, out))
cases = [(A, random.randint(1, len(A))) for A in ([random.randint(-9, 9) for _ in range(random.randint(2, 8))] for _ in range(500))]
check("Q2b remove x, sort the rest, reinsert is valid (500 random)", all(valid(A, K, sort_but_k(A, K)) for A, K in cases))
check("Q2b fully sorting fails to keep position K on some input", any(sorted(A)[K - 1] != A[K - 1] for A, K in cases))
check("Q2b sort-all then swap x back is invalid on some input", any(not valid(A, K, sort_all_swap_back(A, K)) for A, K in cases))
check("Q2b sorting the two sides separately is invalid on some input", any(not valid(A, K, sort_parts(A, K)) for A, K in cases))

# ============================================================ Q3 painting
cost = [[14, 2, 11], [11, 14, 5], [14, 3, 19]]


def paint(cost, variant="right"):
    R, B, G = [cost[0][0]], [cost[0][1]], [cost[0][2]]
    for i in range(1, len(cost)):
        if variant == "right":
            R.append(cost[i][0] + min(B[-1], G[-1]))
            B.append(cost[i][1] + min(R[-2], G[-1]))
            G.append(cost[i][2] + min(R[-2], B[-2]))
        elif variant == "G_allows_G":
            R.append(cost[i][0] + min(B[-1], G[-1]))
            B.append(cost[i][1] + min(R[-2], G[-1]))
            G.append(cost[i][2] + min(R[-2], G[-1]))
        elif variant == "min_all":
            m = min(R[-1], B[-1], G[-1])
            R.append(cost[i][0] + m); B.append(cost[i][1] + m); G.append(cost[i][2] + m)
        elif variant == "max":
            R.append(cost[i][0] + max(B[-1], G[-1]))
            B.append(cost[i][1] + max(R[-2], G[-1]))
            G.append(cost[i][2] + max(R[-2], B[-2]))
        elif variant == "same":
            R.append(cost[i][0] + min(R[-1], B[-1]))
            B.append(cost[i][1] + min(B[-1], G[-1]))
            G.append(cost[i][2] + min(R[-1], G[-1]))
    return R, B, G


def paint_all(cost):
    n = len(cost)
    return [(sum(cost[i][c[i]] for i in range(n)), c) for c in itertools.product(range(3), repeat=n)
            if all(c[i] != c[i + 1] for i in range(n - 1))]


R, B, G = paint(cost)
sols = paint_all(cost)
best = min(s for s, _ in sols)
check("Q3b table and answer 10, G(2)=7, R(2)=13", (R, B, G) == ([14, 13, 21], [2, 25, 10], [11, 7, 32]) and best == 10)
check("Q3b the optimal colouring is unique: B,G,B", [c for s, c in sols if s == best] == [(1, 2, 1)])
rnd = [[[random.randint(1, 20) for _ in range(3)] for _ in range(random.randint(2, 6))] for _ in range(400)]
check("Q3a recurrence equals brute force (400 random)", all(min(x[-1] for x in paint(c)) == min(s for s, _ in paint_all(c)) for c in rnd))
for v in ("G_allows_G", "min_all", "max", "same"):
    check("Q3a distractor '%s' fails on some matrix" % v, any(min(x[-1] for x in paint(c, v)) != min(s for s, _ in paint_all(c)) for c in rnd))
check("Q3b with house 2 red or blue the cost is > 10, with house 2 green it is 10",
      min(s for s, c in sols if c[1] == 0) > 10 and min(s for s, c in sols if c[1] == 1) > 10 and min(s for s, c in sols if c[1] == 2) == 10)
check("Q3c a 3 x n table has 30 cells for n=10", 3 * 10 == 30)

# ============================================================ Q4 Huffman, with cost checks
def huffman_cost(freqs):
    h = list(freqs)
    heapq.heapify(h)
    total = 0
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        total += a + b
        heapq.heappush(h, a + b)
    return total


def huffman_trees(items):
    if len(items) == 1:
        yield items[0]
        return
    ws = sorted(w for w, _ in items)
    lo, hi = ws[0], ws[1]
    seen = set()
    for i, j in itertools.combinations(range(len(items)), 2):
        a, b = items[i], items[j]
        if sorted([a[0], b[0]]) != [lo, hi]:
            continue
        rest = [items[k] for k in range(len(items)) if k not in (i, j)]
        key = (a[1], b[1])
        if key in seen:
            continue
        seen.add(key)
        yield from huffman_trees(rest + [(a[0] + b[0], (a, b))])


def codes_ok(tree, target):
    def options(node, prefix):
        if isinstance(node[1], str):
            return [{node[1]: prefix}]
        x, y = node[1]
        res = []
        for left, right in ((x, y), (y, x)):
            if left[0] <= right[0]:
                for c1 in options(left, prefix + "0"):
                    for c2 in options(right, prefix + "1"):
                        res.append({**c1, **c2})
        return res
    return any(o == target for o in options(tree, ""))


TARGET = {"a": "10", "b": "00", "c": "010", "d": "011", "e": "11"}


def code_cost(f):
    return sum(f[ch] * len(code) for ch, code in TARGET.items())


def first_merge(tree_pairs):
    return None


def accepted(c, d):
    f = {"a": 10, "b": 7, "c": c, "d": d, "e": 10}
    items = [(f[ch], ch) for ch in "abcde"]
    return any(codes_ok(t, TARGET) for t in huffman_trees(items))


def cost_ok(c, d):  # target code has the optimal cost AND satisfies left <= right at every node
    f = {"a": 10, "b": 7, "c": c, "d": d, "e": 10}
    return code_cost(f) == huffman_cost(f.values()) and 7 + c + d <= 20 and 10 <= 10 and c <= d and 7 <= c + d


pos = [(c, d) for c in range(1, 25) for d in range(1, 25) if accepted(c, d)]
check("Q4 the Huffman runs accept exactly 13 pairs with c,d>=1", len(pos) == 13, str(pos))
check("Q4 for those pairs the target code has the OPTIMAL cost", all(
    code_cost({"a": 10, "b": 7, "c": c, "d": d, "e": 10}) == huffman_cost([10, 7, c, d, 10]) for c, d in pos))
cost_pairs = [(c, d) for c in range(1, 41) for d in range(1, 41) if cost_ok(c, d)]
extra = sorted(set(cost_pairs) - set(pos))
print("     NOTE optimal-cost pairs (oriented, c,d>=1) that no Huffman run produces:", extra)
check("Q4 every Huffman-run pair is in the cost-optimal oriented set", set(pos) <= set(cost_pairs))
check("Q4 max d is 7 and min c+d is 7 under BOTH readings (Huffman run / any optimal oriented code)",
      max(d for _, d in pos) == 7 == max(d for _, d in cost_pairs) and min(c + d for c, d in pos) == 7 == min(c + d for c, d in cost_pairs))
check("Q4 (3,5) is accepted and cost-optimal", accepted(3, 5) and (3, 5) in cost_pairs)
for pair in [(8, 8), (2, 9), (1, 8)]:
    c, d = pair
    f = {"a": 10, "b": 7, "c": c, "d": d, "e": 10}
    check("Q4 distractor %s fails the Huffman run AND the target code is not cost-optimal" % (pair,),
          not accepted(c, d) and code_cost(f) > huffman_cost(f.values()))
# first merge is always c,d
first_ok = True
for c, d in pos:
    items = [(10, "a"), (7, "b"), (c, "c"), (d, "d"), (10, "e")]
    lo = sorted(w for w, _ in items)[:2]
    first_ok &= lo == sorted([c, d])
check("Q4 for every accepted pair the two smallest weights at the first merge are c and d", first_ok)
check("Q4 the Z subtree (a,e) weighs 20", 10 + 10 == 20)

# ============================================================ raw JSON consistency
raw = json.loads((ROOT / "tools" / "raw" / "23B-C.json").read_text(encoding="utf-8"))
nums = {}
for q in raw["questions"]:
    for s in q.get("steps", []):
        if s["type"] == "numeric":
            nums.setdefault((q["num"], q.get("part")), []).append(s["answer"])
print("     numeric answers in raw:", nums)
WANT = {(1, "א"): [0], (1, "ב"): [5, 9, 4], (2, "א"): [-7, 15], (2, "ב"): [1], (3, "א"): [7], (3, "ב"): [13, 10],
        (3, "ג"): [30], (4, None): [7]}
for key, want in WANT.items():
    check("raw numeric answers %s == %s" % (key, want), nums.get(key) == want, str(nums.get(key)))

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
