# -*- coding: utf-8 -*-
"""Solver checks for 23B-C (algorithms-1; no answer source). Each claim of the solutions in gen_23B-C.py is
recomputed here: prefix functions by exhaustive search, the suffix tree / array of algogoal, the circular
max-subarray formula and the sort-except-K algorithm against brute force, the house-painting DP table, and the
Huffman options of Q4 by enumerating every Huffman run (all tie breaks). ASCII output.
Run: PYTHONUTF8=1 py tools/verify/23B-C/solve_23BC.py"""
import itertools, random

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


random.seed(23)


# ---------------------------------------------------------------- Q1a prefix function
def pi(P):
    p = [0] * len(P)
    k = 0
    for q in range(1, len(P)):
        while k > 0 and P[k] != P[q]:
            k = p[k - 1]
        if P[k] == P[q]:
            k += 1
        p[q] = k
    return p


pis = {tuple(pi("".join(w))) for w in itertools.product("abcde", repeat=5)}
check("Q1a no string of length 5 has pi = 0,1,2,3,1 (all 5^5 strings)", (0, 1, 2, 3, 1) not in pis)
check("Q1a nor the reversed reading 1,3,2,1,0 (pi[1] is always 0)", (1, 3, 2, 1, 0) not in pis and all(t[0] == 0 for t in pis))
check("Q1a prefix aaaa forces pi[5] in {0,4}", {pi("aaaa" + c)[4] for c in "abcde"} == {0, 4})
check("Q1a 0,1,2,3,4 and 0,1,2,3,0 do exist", (0, 1, 2, 3, 4) in pis and (0, 1, 2, 3, 0) in pis)

# ---------------------------------------------------------------- Q1b suffix array / tree of algogoal
S = "algogoal"
SA = sorted(range(1, len(S) + 1), key=lambda i: S[i - 1:])
check("Q1b suffix array (1-based, no $) = 7 1 5 3 8 2 6 4", SA == [7, 1, 5, 3, 8, 2, 6, 4], str(SA))


def suffix_tree(t):
    """Compressed trie of all suffixes of t (t ends with a unique $). Returns nested dict label -> subtree or leaf id."""
    def build(items):  # items: list of (string, leaf id)
        groups = {}
        for s, i in items:
            groups.setdefault(s[0], []).append((s, i))
        node = {}
        for _, grp in sorted(groups.items()):
            if len(grp) == 1:
                node[grp[0][0]] = grp[0][1]
                continue
            lcp = grp[0][0]
            for s, _ in grp[1:]:
                k = 0
                while k < min(len(lcp), len(s)) and lcp[k] == s[k]:
                    k += 1
                lcp = lcp[:k]
            node[lcp] = build([(s[len(lcp):], i) for s, i in grp])
        return node
    return build([(t[i:], i + 1) for i in range(len(t))])


tree = suffix_tree(S + "$")
EXPECT_TREE = {"$": 9,
               "al": {"$": 7, "gogoal$": 1},
               "go": {"al$": 5, "goal$": 3},
               "l": {"$": 8, "gogoal$": 2},
               "o": {"al$": 6, "goal$": 4}}
check("Q1b suffix tree of algogoal$ as written in the solution", tree == EXPECT_TREE, str(tree))


# ---------------------------------------------------------------- Q2a circular maximum subarray
def kadane(A):  # the black box: max sum of a non-empty contiguous subarray
    best = cur = A[0]
    for x in A[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


def circ(A):  # transcription of the solution
    m1 = kadane(A)
    if m1 < 0:
        return m1
    mn = -kadane([-x for x in A])
    return max(m1, sum(A) - mn)


def circ_brute(A):
    n = len(A)
    return max(sum(A[(s + t) % n] for t in range(L)) for s in range(n) for L in range(1, n + 1))


check("Q2a example 4,-6,5,-6,10,-5,3 -> 12", circ([4, -6, 5, -6, 10, -5, 3]) == 12 == circ_brute([4, -6, 5, -6, 10, -5, 3]))
check("Q2a formula equals brute force over all circular segments (3000 random, incl. all-negative)",
      all(circ(A) == circ_brute(A) for A in ([random.randint(-9, 9) for _ in range(random.randint(1, 9))] for _ in range(3000))))
check("Q2a all-negative arrays", all(circ(A) == max(A) for A in ([random.randint(-9, -1) for _ in range(random.randint(1, 7))] for _ in range(300))))


# ---------------------------------------------------------------- Q2b sort all but position K
def sort_but_k(A, K):  # transcription: take x=A[K], merge sort the rest, put x back at K (1-based)
    x = A[K - 1]
    B = sorted(A[:K - 1] + A[K:])
    return B[:K - 1] + [x] + B[K - 1:]


def brute_sort_but_k(A, K):
    for perm in itertools.permutations(A):
        if perm[K - 1] == A[K - 1] and list(perm[:K - 1] + perm[K:]) == sorted(perm[:K - 1] + perm[K:]):
            if sorted(perm) == sorted(A):
                return list(perm)


check("Q2b example K=5", sort_but_k([4, 10, -6, 3, 15, -8, 7], 5) == [-8, -6, 3, 4, 15, 7, 10])
check("Q2b equals brute force (400 random)",
      all(sort_but_k(A, K) == brute_sort_but_k(A, K) for A, K in
          ((A, random.randint(1, len(A))) for A in ([random.randint(-5, 5) for _ in range(random.randint(1, 6))] for _ in range(400)))))

# ---------------------------------------------------------------- Q3 house painting
cost = [[14, 2, 11], [11, 14, 5], [14, 3, 19]]


def paint(cost):
    R, B, G = [cost[0][0]], [cost[0][1]], [cost[0][2]]
    for i in range(1, len(cost)):
        R.append(cost[i][0] + min(B[-1], G[-1]))
        B.append(cost[i][1] + min(R[-2], G[-1]))
        G.append(cost[i][2] + min(R[-2], B[-2]))
    return R, B, G


def paint_brute(cost):
    n = len(cost)
    return min(sum(cost[i][c[i]] for i in range(n)) for c in itertools.product(range(3), repeat=n)
               if all(c[i] != c[i + 1] for i in range(n - 1)))


R, B, G = paint(cost)
check("Q3b table R=14,13,21 B=2,25,10 G=11,7,32, answer 10",
      (R, B, G) == ([14, 13, 21], [2, 25, 10], [11, 7, 32]) and min(R[-1], B[-1], G[-1]) == 10 == paint_brute(cost),
      str((R, B, G)))
check("Q3a recurrence equals brute force (500 random)",
      all(min(x[-1] for x in paint(c)) == paint_brute(c) for c in
          ([[random.randint(1, 20) for _ in range(3)] for _ in range(random.randint(1, 6))] for _ in range(500))))


# ---------------------------------------------------------------- Q4 Huffman options for c, d
def huffman_trees(items):
    """All trees Huffman can build (every tie break). items: list of (weight, tree). Yields (weight, tree) roots."""
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
    """Is there an orientation (left weight <= right weight; equal weights either way) giving exactly target codes?"""
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
found = []
for c in range(0, 25):
    for d in range(0, 25):
        items = [(10, "a"), (7, "b"), (c, "c"), (d, "d"), (10, "e")]
        if any(codes_ok(t, TARGET) for t in huffman_trees(items)):
            found.append((c, d))
pos = [x for x in found if x[0] >= 1]
EXPECT_Q4 = [(1, 6), (1, 7), (2, 5), (2, 6), (2, 7), (3, 4), (3, 5), (3, 6), (3, 7), (4, 4), (4, 5), (4, 6), (5, 5)]
check("Q4 positive options are the 13 pairs of the solution", pos == EXPECT_Q4, str(pos))
check("Q4 they are exactly 1<=c<=d<=7, 7<=c+d<=10", pos == [(c, d) for c in range(1, 8) for d in range(c, 8) if 7 <= c + d <= 10])
check("Q4 with c=0 allowed the only extra pair is (0,7)", [x for x in found if x[0] == 0] == [(0, 7)], str(found[:3]))

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
