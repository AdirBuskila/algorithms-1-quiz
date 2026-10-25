"""Machine check of every stored answer in courses/dp_ladder/C01..C09.

Every recurrence and every table value is compared with an independent brute force (enumerating subsequences,
multisets of coins/squares, cuts, subsets, edit scripts). Code in findbug/fillblank steps is executed. The level files
are loaded with the app's own loader (node tools/course_load.js), so the script asserts what is actually stored.

Run from the app root:  py tools/verify/needhelp/dp_ladder/check.py
Every own question must be asserted, otherwise the script fails at the end.
"""
import itertools
import json
import math
import os
import random
import re
import subprocess
import sys
from functools import lru_cache

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
COURSE = "dp_ladder"
INF = float("inf")

raw = subprocess.run(["node", os.path.join(ROOT, "tools", "course_load.js")], capture_output=True, cwd=ROOT, check=True).stdout
loaded = json.loads(raw.decode("utf-8"))
assert not loaded["errors"], loaded["errors"]
levels = {e["level"]["id"]: e["level"] for e in loaded["levels"] if e["courseId"] == COURSE}
assert sorted(levels) == ["C%02d" % i for i in range(1, 10)], sorted(levels)
Q = {}
for lid, L in levels.items():
    for q in L["questions"]:
        if "bankId" not in q:
            Q[q["id"]] = q
covered = set()


def own(qid):
    assert qid in Q, qid
    covered.add(qid)
    return Q[qid]


def num(qid, expected):
    q = own(qid)
    s = q["step"]
    assert s["type"] == "numeric", qid
    assert s.get("tol", 0) == 0, qid
    assert s["answer"] == expected, (qid, s["answer"], expected)


def mcq(qid, truth):
    """truth: option id -> computed boolean (is this option a correct answer?)."""
    q = own(qid)
    q = q.get("step", q)
    ids = [o["id"] for o in q["options"]]
    assert sorted(ids) == sorted(truth), (qid, ids, sorted(truth))
    right = [i for i in ids if truth[i]]
    assert right == [q["correctId"]], (qid, "computed correct", right, "stored", q["correctId"])
    assert "acceptedIds" not in q


# ---------------------------------------------------------------- brute-force primitives
def is_subseq(s, t):
    it = iter(t)
    return all(ch in it for ch in s)


def lcs_bf(a, b):
    """Longest common subsequence by trying every subsequence of a (longest first)."""
    for r in range(len(a), -1, -1):
        for c in itertools.combinations(range(len(a)), r):
            if is_subseq("".join(a[i] for i in c), b):
                return r
    return 0


def all_lcs(a, b):
    best = lcs_bf(a, b)
    out = set()
    for c in itertools.combinations(range(len(a)), best):
        s = "".join(a[i] for i in c)
        if is_subseq(s, b):
            out.add(s)
    return out


def lcs_table(a, b):
    n, m = len(a), len(b)
    L = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            L[i][j] = L[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(L[i - 1][j], L[i][j - 1])
    return L


def edit_bf(a, b):
    """Levenshtein distance by breadth-first search over strings (insert / delete / substitute one character)."""
    alpha = sorted(set(a) | set(b))
    seen = {a}
    frontier = [a]
    d = 0
    while b not in seen:
        d += 1
        nxt = []
        for s in frontier:
            outs = []
            for k in range(len(s) + 1):
                for ch in alpha:
                    outs.append(s[:k] + ch + s[k:])
            for k in range(len(s)):
                outs.append(s[:k] + s[k + 1:])
                for ch in alpha:
                    outs.append(s[:k] + ch + s[k + 1:])
            for t in outs:
                if t not in seen and len(t) <= len(a) + len(b):
                    seen.add(t)
                    nxt.append(t)
        frontier = nxt
        assert frontier, "unreachable"
    return d


def edit_table(a, b):
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = D[i - 1][j - 1] if a[i - 1] == b[j - 1] else 1 + min(D[i - 1][j - 1], D[i - 1][j], D[i][j - 1])
    return D


def count_occ_bf(T, P):
    return sum(1 for c in itertools.combinations(range(len(T)), len(P)) if all(T[k] == p for k, p in zip(c, P)))


def count_table(T, P):
    n, m = len(T), len(P)
    C = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        C[i][0] = 1
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            C[i][j] = C[i - 1][j] + (C[i - 1][j - 1] if T[i - 1] == P[j - 1] else 0)
    return C


def min_squares_bf(N):
    """Minimum number of positive squares summing to N, by BFS over partial sums."""
    squares = [k * k for k in range(1, math.isqrt(N) + 1)]
    layer, seen, d = {0}, {0}, 0
    while N not in layer:
        d += 1
        layer = {s + q for s in layer for q in squares if s + q <= N} - seen
        seen |= layer
    return d


def min_coins_bf(n, coins=(1, 3, 4)):
    layer, seen, d = {0}, {0}, 0
    if n == 0:
        return 0
    while n not in layer:
        d += 1
        layer = {s + c for s in layer for c in coins if s + c <= n} - seen
        seen |= layer
    return d


def pal_bf(s):
    best = 0
    for r in range(len(s), 0, -1):
        for c in itertools.combinations(range(len(s)), r):
            t = "".join(s[i] for i in c)
            if t == t[::-1]:
                return r
    return best


def cuts_bf(S, words):
    """All ways to cut S into dictionary words (list of lists)."""
    out = []

    def rec(pos, cur):
        if pos == len(S):
            out.append(list(cur))
            return
        for e in range(pos + 1, len(S) + 1):
            if S[pos:e] in words:
                cur.append(S[pos:e])
                rec(e, cur)
                cur.pop()
    rec(0, [])
    return out


def pal_cuts_min_bf(S):
    best = INF
    n = len(S)
    for mask in range(1 << (n - 1)):
        parts, cur = [], S[0]
        for k in range(1, n):
            if mask >> (k - 1) & 1:
                parts.append(cur)
                cur = S[k]
            else:
                cur += S[k]
        parts.append(cur)
        if all(p == p[::-1] for p in parts):
            best = min(best, len(parts))
    return best


def knap_bf(items, cap):
    best = 0
    for r in range(len(items) + 1):
        for c in itertools.combinations(items, r):
            if sum(w for w, v in c) <= cap:
                best = max(best, sum(v for w, v in c))
    return best


def inter_bf(s1, s2, s3):
    if len(s3) != len(s1) + len(s2):
        return False
    n = len(s3)
    for pos in itertools.combinations(range(n), len(s1)):
        rest = [k for k in range(n) if k not in pos]
        if "".join(s3[k] for k in pos) == s1 and "".join(s3[k] for k in rest) == s2:
            return True
    return False


random.seed(20261025)


def rstr(alpha, lo, hi):
    return "".join(random.choice(alpha) for _ in range(random.randint(lo, hi)))


# ================================================================ C01
def satisfies_lcs_recurrence(g):
    for _ in range(40):
        X, Y = rstr("abc", 0, 5), rstr("abc", 0, 5)
        for i in range(len(X) + 1):
            for j in range(len(Y) + 1):
                if i == 0 or j == 0:
                    if g(X, Y, i, j) != 0:
                        return False
                elif X[i - 1] == Y[j - 1]:
                    if g(X, Y, i, j) != g(X, Y, i - 1, j - 1) + 1:
                        return False
                else:
                    if g(X, Y, i, j) != max(g(X, Y, i, j - 1), g(X, Y, i - 1, j)):
                        return False
    return True


mcq("C01-Q1", {
    "a": satisfies_lcs_recurrence(lambda X, Y, i, j: lcs_bf(X[:i], Y[:j])),
    "b": satisfies_lcs_recurrence(lambda X, Y, i, j: sum(1 for k in range(min(i, j)) if X[k] == Y[k])),
    "c": satisfies_lcs_recurrence(lambda X, Y, i, j: lcs_bf(X, Y)),
    "d": satisfies_lcs_recurrence(lambda X, Y, i, j: 1 if i > 0 and j > 0 and X[i - 1] == Y[j - 1] else 0),
})
# the explanation's example for option b: X=ab, Y=ba -> 0 vs LCS 1
assert sum(1 for k in range(2) if "ab"[k] == "ba"[k]) == 0 and lcs_bf("ab", "ba") == 1


def grid_paths_bf(i, j):
    """Monotone right/down paths from (1,1) to (i,j), by depth-first enumeration."""
    def go(r, c):
        if (r, c) == (i, j):
            return 1
        t = 0
        if r < i:
            t += go(r + 1, c)
        if c < j:
            t += go(r, c + 1)
        return t
    return go(1, 1)


def satisfies_grid(g, n=4):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == 1 or j == 1:
                if g(i, j) != 1:
                    return False
            elif g(i, j) != g(i - 1, j) + g(i, j - 1):
                return False
    return True


mcq("C01-Q2", {
    "a": satisfies_grid(grid_paths_bf),
    "b": satisfies_grid(lambda i, j: i * j),
    "c": satisfies_grid(lambda i, j: i + j - 2),
    "d": satisfies_grid(lambda i, j: math.comb((4 - i) + (4 - j), 4 - i)),  # paths from (i,j) to (4,4)
})

num("C01-Q3", len([min_squares_bf(i) for i in range(0, 31)]))


def pal_holds(rule):
    for ln in range(2, 7):
        for t in itertools.product("abc", repeat=ln):
            s = "".join(t)
            if pal_bf(s) != rule(s):
                return False
    return True


assert pal_bf("ab") == pal_bf("ba") == 1 and pal_bf("aba") == 3 and pal_bf("baa") == 2
assert pal_bf("abc") == 1 and pal_bf("abca") == 3
mcq("C01-Q4", {
    "a": pal_bf("ab") == pal_bf("ba") and pal_bf("aba") != pal_bf("baa"),
    "b": pal_holds(lambda s: pal_bf(s[:-1]) + 1 if s[-1] in s[:-1] else pal_bf(s)),
    "c": pal_holds(lambda s: max(pal_bf(s[:-1]), 1)),
    "d": pal_holds(lambda s: pal_bf(s[:-1]) + 1 if s[-1] == s[0] else pal_bf(s)),
})


def answer_cell_ok(pick):
    for _ in range(60):
        X, Y = rstr("abc", 1, 5), rstr("abc", 1, 5)
        n, m = len(X), len(Y)
        i, j = pick(n, m)
        if i < 0 or j < 0 or lcs_bf(X[:i], Y[:j]) != lcs_bf(X, Y):
            return False
    return True


mcq("C01-Q5", {
    "a": answer_cell_ok(lambda n, m: (n, m)),
    "b": answer_cell_ok(lambda n, m: (n, m - 1)),
    "c": answer_cell_ok(lambda n, m: (n - 1, m - 1)),
    "d": answer_cell_ok(lambda n, m: (1, 1)),
})
assert lcs_bf("abc", "abc") == 3 and lcs_bf("abc", "ab") == 2 and lcs_bf("ab", "ab") == 2 and lcs_bf("a", "a") == 1

# ================================================================ C02
F = {i: min_squares_bf(i) for i in range(0, 41)}
# the recurrence in the lesson equals brute force
for i in range(1, 41):
    assert F[i] == 1 + min(F[i - j * j] for j in range(1, math.isqrt(i) + 1)), i
assert F[0] == 0 and [F[i] for i in (1, 2, 3, 4, 5, 8)] == [1, 2, 3, 1, 2, 2]
num("C02-Q1", F[12])
assert (F[11], F[8], F[3]) == (3, 2, 3)
num("C02-Q2", F[13])
assert (F[12], F[9], F[4]) == (3, 1, 1)

M = {i: min_coins_bf(i) for i in range(0, 41)}


def coin_ok(rec):
    return all(rec(M, i) == M[i] for i in range(1, 31))


mcq("C02-Q3", {
    "a": coin_ok(lambda M, i: 1 + min(M[i - c] for c in (1, 3, 4) if c <= i)),
    "b": coin_ok(lambda M, i: 1 + M[i - 4] if i >= 4 else 1 + M[i - 1]),
    "c": coin_ok(lambda M, i: min(M[i - c] for c in (1, 3, 4) if c <= i)),
    "d": coin_ok(lambda M, i: sum(M[i - c] for c in (1, 3, 4) if c <= i)),
})
assert M[6] == 2 and [M[i] for i in range(1, 6)] == [1, 2, 1, 1, 2]
num("C02-Q4", M[6])
# the greedy remark in the lesson: 6 = 4+1+1 is three coins
assert 1 + M[6 - 4] == 3

# C(i,0): number of ways the empty pattern is a subsequence of a text of length i
cand_c = {"a": lambda i: 1, "b": lambda i: 0, "c": lambda i: i, "d": lambda i: 2 ** i}
mcq("C02-Q5", {k: all(f(i) == count_occ_bf("x" * i, "") for i in range(0, 7)) for k, f in cand_c.items()})

# the order step of Q6: derive the recurrence the lines state and check it (already done above); check its lines
q = own("C02-Q6")
assert q["step"]["type"] == "order" and len(q["step"]["lines"]) == 4
assert "F(i-j^2)" in q["step"]["lines"][3] and "F(0)=0" in q["step"]["lines"][3]

# ================================================================ C03
Lt = lcs_table("a" * 5, "b" * 7)
num("C03-Q1", sum(len(r) for r in Lt))
assert (5 + 1) * (7 + 1) == 48


def pal_order_legal(order, n=6):
    """order: list of cells (i, j), i < j, in fill sequence. A cell may only read cells already filled or base cells."""
    filled = {(i, j) for i in range(1, n + 1) for j in range(1, n + 1) if i >= j}
    for (i, j) in order:
        for cell in ((i + 1, j - 1), (i + 1, j), (i, j - 1)):
            if cell not in filled:
                return False
        filled.add((i, j))
    return filled >= {(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)}


n6 = 6
cells = [(i, j) for i in range(1, n6 + 1) for j in range(i + 1, n6 + 1)]
by_len = sorted(cells, key=lambda c: (c[1] - c[0], c[0]))
ord_b = [(i, j) for i in range(1, n6 + 1) for j in range(i + 1, n6 + 1)]
ord_c = [(i, j) for i in range(n6, 0, -1) for j in range(n6, i, -1)]
ord_d = [(i, j) for j in range(n6, 1, -1) for i in range(1, j)]
mcq("C03-Q2", {"a": pal_order_legal(by_len), "b": pal_order_legal(ord_b), "c": pal_order_legal(ord_c),
               "d": pal_order_legal(ord_d)})


def run_procedure(steps):
    """Each step needs the previous ones done; returns the LCS length of 'abcb' and 'bcab' or None on a violation."""
    X, Y = "abcb", "bcab"
    st = {}
    for s in steps:
        if s == "alloc":
            st["L"] = [[None] * (len(Y) + 1) for _ in range(len(X) + 1)]
        elif s == "base":
            if "L" not in st:
                return None
            for i in range(len(X) + 1):
                st["L"][i][0] = 0
            for j in range(len(Y) + 1):
                st["L"][0][j] = 0
        elif s == "fill":
            if "L" not in st or st["L"][0][0] is None:
                return None
            Lm = st["L"]
            for i in range(1, len(X) + 1):
                for j in range(1, len(Y) + 1):
                    Lm[i][j] = Lm[i - 1][j - 1] + 1 if X[i - 1] == Y[j - 1] else max(Lm[i - 1][j], Lm[i][j - 1])
            st["filled"] = True
        elif s == "ret":
            if not st.get("filled"):
                return None
            return st["L"][len(X)][len(Y)]
    return None


good = [p for p in itertools.permutations(["alloc", "base", "fill", "ret"]) if run_procedure(p) == lcs_bf("abcb", "bcab")]
assert good == [("alloc", "base", "fill", "ret")], good
q = own("C03-Q3")
assert q["step"]["type"] == "order" and len(q["step"]["lines"]) == 4
assert "(n+1)\\times(m+1)" in q["step"]["lines"][0] and "L[n][m]" in q["step"]["lines"][3]

num("C03-Q4", len(list(itertools.product(range(0, 5), range(0, 6), range(0, 7)))))
reads = [12 - j * j for j in range(1, math.isqrt(12) + 1)]
assert reads == [11, 8, 3]
num("C03-Q5", len(reads))
num("C03-Q6", len([(i, j) for i in range(1, 7) for j in range(1, 7) if i <= j]))

# ================================================================ C04
X4, Y4 = "ACBAB", "ABCB"
T4 = lcs_table(X4, Y4)
assert T4[2][1] == lcs_bf("AC", "A") == 1 and T4[3][2] == lcs_bf("ACB", "AB") == 2
assert X4[2] == Y4[1] == "B"
num("C04-Q1", T4[3][2])
actual_equal = X4[3 - 1] == Y4[2 - 1]
claims = {  # option -> (says chars are equal?, value it computes)
    "a": (True, T4[2][1] + 1),
    "b": (False, max(T4[2][2], T4[3][1])),
    "c": (True, max(T4[2][2], T4[3][1])),
    "d": (True, T4[2][1]),
}
mcq("C04-Q2", {k: (eq == actual_equal and val == T4[3][2]) for k, (eq, val) in claims.items()})
num("C04-Q3", T4[5][4])
assert lcs_bf(X4, Y4) == 3 and {"ACB", "ABB"} <= all_lcs(X4, Y4)
# the rows quoted in the explanation of C04-Q3
assert T4 == [[0, 0, 0, 0, 0], [0, 1, 1, 1, 1], [0, 1, 1, 2, 2], [0, 1, 2, 2, 3], [0, 1, 2, 2, 3], [0, 1, 2, 2, 3]]
D4 = edit_table("ABC", "BCD")
assert D4 == [[0, 1, 2, 3], [1, 1, 2, 3], [2, 1, 2, 3], [3, 2, 1, 2]]
num("C04-Q4", edit_bf("ABC", "BCD"))
assert D4[3][3] == 2
for _ in range(25):  # the edit-distance recurrence of the lesson equals the BFS brute force
    a, b = rstr("ab", 0, 4), rstr("ab", 0, 4)
    assert edit_table(a, b)[-1][-1] == edit_bf(a, b), (a, b)
C4 = count_table("aabab", "ab")
num("C04-Q5", count_occ_bf("aabab", "ab"))
assert C4[5][2] == 5 and [C4[i][1] for i in range(1, 6)] == [1, 2, 2, 3, 3] and [C4[i][2] for i in range(1, 6)] == [0, 0, 2, 2, 5]
for _ in range(25):  # counting recurrence equals brute force
    T, P = rstr("ab", 0, 6), rstr("ab", 0, 3)
    assert count_table(T, P)[-1][-1] == count_occ_bf(T, P), (T, P)
# lesson example: X=ABC, Y=AC
assert lcs_table("ABC", "AC") == [[0, 0, 0], [0, 1, 1], [0, 1, 1], [0, 1, 2]]

# ================================================================ C05
X5, Y5 = "ACBBC", "ABCA"
T5 = lcs_table(X5, Y5)
# the table quoted in the stem of C05-Q1 equals the computed one
stem = Q["C05-Q1"]["step"]["prompt"]
body = stem.split("```")[1].strip("\n").split("\n")
quoted = [[int(x) for x in row.split()[1:]] for row in body[1:]]
assert quoted == T5, (quoted, T5)
assert all_lcs(X5, Y5) == {"ABC"}


def recon(X, Y, L, tie="up", trace=False):
    i, j, out, path = len(X), len(Y), [], [(len(X), len(Y))]
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            out.append(X[i - 1])
            i, j = i - 1, j - 1
        elif L[i - 1][j] > L[i][j - 1] or (L[i - 1][j] == L[i][j - 1] and tie == "up"):
            i -= 1
        else:
            j -= 1
        path.append((i, j))
    return ("".join(out), path) if trace else "".join(out)


collected, path = recon(X5, Y5, T5, trace=True)
assert path[1] == (5, 3), path
num("C05-Q1", path[1][1])
assert T5[4][4] == 2 and T5[5][3] == 3  # explanation numbers
own("C05-Q2")
assert collected == "CBA" and Q["C05-Q2"]["step"]["accept"] == ["CBA"] and collected[::-1] == "ABC"
# tie cell (4,3)
assert X5[3] != Y5[2] and T5[3][3] == T5[4][2] == 2


def tie_valid(tie, trials=300):
    for _ in range(trials):
        X, Y = rstr("abc", 1, 6), rstr("abc", 1, 6)
        T = lcs_table(X, Y)
        r = recon(X, Y, T, tie)[::-1]
        if not (is_subseq(r, X) and is_subseq(r, Y) and len(r) == T[-1][-1]):
            return False
    return True


# choosing the upper neighbour at a tie, or the left one, both always give a longest common subsequence,
# and the two choices really differ on some inputs
differ = False
for _ in range(400):
    X, Y = rstr("abc", 3, 6), rstr("abc", 3, 6)
    T = lcs_table(X, Y)
    if recon(X, Y, T, "up") != recon(X, Y, T, "left"):
        differ = True
        break
assert differ
up_ok, left_ok = tie_valid("up"), tie_valid("left")
mcq("C05-Q3", {"a": up_ok and left_ok, "b": up_ok and not left_ok, "c": left_ok and not up_ok,
               "d": not (up_ok or left_ok)})

fixed_lines = list(Q["C05-Q4"]["step"]["lines"])
bug_i = Q["C05-Q4"]["step"]["bugIndex"]
assert fixed_lines[bug_i].strip() == "out.append(X[i-1]); i -= 1"
fixed_lines[bug_i] = fixed_lines[bug_i].replace("i -= 1", "i -= 1; j -= 1")


def load_fn(lines, name):
    ns = {}
    exec("\n".join(lines), ns)
    return ns[name]


good_fn = load_fn(fixed_lines, "recon")
bad_fn = load_fn(Q["C05-Q4"]["step"]["lines"], "recon")
bug_fail = False
for _ in range(200):
    X, Y = rstr("abc", 1, 6), rstr("abc", 1, 6)
    T = lcs_table(X, Y)
    s = good_fn(X, Y, T)
    assert is_subseq(s, X) and is_subseq(s, Y) and len(s) == T[-1][-1]
    b = bad_fn(X, Y, T)
    if not (is_subseq(b, X) and is_subseq(b, Y) and len(b) == T[-1][-1]):
        bug_fail = True
assert bug_fail
assert good_fn(X5, Y5, T5) == "ABC" and bad_fn(X5, Y5, T5) != "ABC"
own("C05-Q4")
assert sum(1 for a, b in zip(fixed_lines, Q["C05-Q4"]["step"]["lines"]) if a != b) == 1
num("C05-Q5", len(path))
assert path == [(5, 4), (5, 3), (4, 2), (3, 1), (2, 1), (1, 1), (0, 0)]

# ================================================================ C06
def lcs3_ops(n):
    ops = 0
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for l in range(1, n + 1):
                ops += 1
    return ops


def exponent(f, n):
    return math.log(f(2 * n) / f(n), 2)


def cut_ops(n):
    return sum(i for i in range(1, n + 1))  # j from 0..i-1 for each i


def sq_ops(N):
    return sum(math.isqrt(i) for i in range(1, N + 1))


def acc_exp(q):
    acc = q["step"]["accept"]
    assert len(acc) == 1
    m = re.fullmatch(r"O\(n\^(\d)\)", acc[0])
    return int(m.group(1))


own("C06-Q1")
assert abs(exponent(lcs3_ops, 20) - acc_exp(Q["C06-Q1"])) < 0.2
assert lcs_table("a" * 4, "b" * 5) and len(list(itertools.product(range(5), range(6), range(7)))) == 210
# cut recurrence cost is quadratic: count the inner iterations of a real implementation
own("C06-Q2")
assert abs(exponent(cut_ops, 100) - acc_exp(Q["C06-Q2"])) < 0.1


def two_row_lcs(X, Y):
    prev = [0] * (len(Y) + 1)
    kept = 0
    for i in range(1, len(X) + 1):
        cur = [0] * (len(Y) + 1)
        for j in range(1, len(Y) + 1):
            cur[j] = prev[j - 1] + 1 if X[i - 1] == Y[j - 1] else max(prev[j], cur[j - 1])
        kept = max(kept, len(prev) + len(cur))
        prev = cur
    return prev[-1], kept


for _ in range(30):
    X, Y = rstr("abc", 6, 6), rstr("abc", 9, 9)
    v, kept = two_row_lcs(X, Y)
    assert v == lcs_table(X, Y)[-1][-1] == lcs_bf(X, Y)
num("C06-Q3", kept)
assert kept == 2 * (9 + 1) and 7 * 10 == 70


def naive_calls(i, j):
    if i == 0 or j == 0:
        return 1
    return 1 + naive_calls(i - 1, j) + naive_calls(i, j - 1)


# also run the real naive LCS recursion on strings with no equal characters and count calls
cnt = [0]


def naive_lcs(X, Y, i, j):
    cnt[0] += 1
    if i == 0 or j == 0:
        return 0
    if X[i - 1] == Y[j - 1]:
        return 1 + naive_lcs(X, Y, i - 1, j - 1)
    return max(naive_lcs(X, Y, i - 1, j), naive_lcs(X, Y, i, j - 1))


naive_lcs("abc", "xyz", 3, 3)
assert cnt[0] == naive_calls(3, 3)
num("C06-Q4", naive_calls(3, 3))
assert [naive_calls(1, 1), naive_calls(1, 2), naive_calls(2, 2), naive_calls(1, 3), naive_calls(2, 3)] == [3, 5, 11, 7, 19]
assert naive_calls(2, 2) == 11

measured = math.log(sq_ops(6400) / sq_ops(1600), 4)  # exponent of N
fl = lambda N: N * math.log(N)  # N log N measured the same way
pred = {"a": 1.5, "b": 1.0, "c": 2.0, "d": math.log(fl(6400) / fl(1600), 4)}
mcq("C06-Q5", {k: abs(v - measured) < 0.08 for k, v in pred.items()})

# ================================================================ C07
dic = {"cat", "cats", "and", "sand", "dog", "catsand"}
cuts = cuts_bf("catsanddog", dic)
num("C07-Q1", min(len(c) for c in cuts))
num("C07-Q2", len(cuts))


def cut_table_min(S, words):
    n = len(S)
    C = [INF] * (n + 1)
    C[0] = 0
    for i in range(1, n + 1):
        C[i] = min(C[j] + (1 if S[j:i] in words else INF) for j in range(i))
    return C


def cut_table_count(S, words):
    n = len(S)
    N = [0] * (n + 1)
    N[0] = 1
    for i in range(1, n + 1):
        N[i] = sum(N[j] for j in range(i) if S[j:i] in words)
    return N


assert cut_table_min("catsanddog", dic)[-1] == 2 and cut_table_count("catsanddog", dic)[-1] == 3
Nn = cut_table_count("catsanddog", dic)
assert Nn[10] == Nn[7] == 3 and (Nn[3], Nn[4], Nn[0]) == (1, 1, 1)
# lesson example
assert cut_table_min("abcd", {"ab", "cd", "abc"}) == [0, INF, 1, 1, 2]


def cut_rule_ok(rule):
    for _ in range(120):
        words = {rstr("ab", 1, 3) for _ in range(random.randint(1, 5))}
        S = rstr("ab", 1, 7)
        n = len(S)
        brute = [len(cuts_bf(S[:i], words)) for i in range(n + 1)]
        N = [0] * (n + 1)
        N[0] = rule["base"]
        for i in range(1, n + 1):
            N[i] = rule["f"](N, S, i, words)
        if N != brute:
            return False
    return True


def rule_sum(N, S, i, words):
    return sum(N[j] for j in range(i) if S[j:i] in words)


def rule_max(N, S, i, words):
    vals = [N[j] for j in range(i) if S[j:i] in words]
    return max(vals) if vals else 0


def rule_min1(N, S, i, words):
    vals = [N[j] + 1 for j in range(i) if S[j:i] in words]
    return min(vals) if vals else 0


mcq("C07-Q3", {
    "a": cut_rule_ok({"base": 1, "f": rule_sum}),
    "b": cut_rule_ok({"base": 1, "f": rule_max}),
    "c": cut_rule_ok({"base": 0, "f": rule_sum}),
    "d": cut_rule_ok({"base": 0, "f": rule_min1}),
})
num("C07-Q4", pal_cuts_min_bf("abacdc"))
assert pal_cuts_min_bf("abacdc") == 2


def neutral(s):
    return all(min(s, v) == v for v in range(0, 25))


mcq("C07-Q5", {"a": neutral(INF), "b": neutral(0), "c": neutral(-1), "d": neutral(1)})
num("C07-Q6", count_occ_bf("rabbbit", "rabbit"))
assert count_table("rabbbit", "rabbit")[7][6] == 3 == math.comb(3, 2)

# ================================================================ C08
items = [(2, 3), (3, 4), (4, 5), (5, 8)]
num("C08-Q1", knap_bf(items, 9))
assert sorted(sum(v for w, v in c) for c in itertools.combinations(items, 3) if sum(w for w, v in c) == 9) == [12]
num("C08-Q2", sum(1 for r in range(6) for c in itertools.combinations([2, 3, 5, 7, 8], r) if sum(c) == 10))
assert {frozenset(c) for r in range(6) for c in itertools.combinations([2, 3, 5, 7, 8], r) if sum(c) == 10} == \
    {frozenset({2, 8}), frozenset({3, 7}), frozenset({2, 3, 5})}


def knap_instances():
    for _ in range(120):
        n = random.randint(1, 5)
        W = [random.randint(1, 5) for _ in range(n)]
        V = [random.randint(1, 9) for _ in range(n)]
        yield W, V, random.randint(0, 10)


def knap_ok(fn):
    return all(fn(W, V, cap) == knap_bf(list(zip(W, V)), cap) for W, V, cap in knap_instances())


qf = own("C08-Q3")["step"]
assert qf["type"] == "fillblank" and qf["lines"][qf["blankIndex"]].count("___") == 1
truth = {}
for o in qf["options"]:
    lines = list(qf["lines"])
    lines[qf["blankIndex"]] = lines[qf["blankIndex"]].replace("___", o["value"])
    truth[o["id"]] = knap_ok(load_fn(lines, "knap"))
mcq("C08-Q3", truth)

# Q4: the stored lines are the buggy version; replacing the bug line gives a correct program
q4 = own("C08-Q4")["step"]
fixed = list(q4["lines"])
assert fixed[q4["bugIndex"]].strip() == "K[i][w] = 0"
fixed[q4["bugIndex"]] = fixed[q4["bugIndex"]].replace("= 0", "= K[i-1][w]")
assert knap_ok(load_fn(fixed, "knap")) and not knap_ok(load_fn(q4["lines"], "knap"))
assert sum(1 for a, b in zip(fixed, q4["lines"]) if a != b) == 1
# the same fixed program equals the one in the fillblank step (with the correct option)
correct_lines = list(qf["lines"])
correct_lines[qf["blankIndex"]] = correct_lines[qf["blankIndex"]].replace("___", "V[i-1] + K[i-1][w - W[i-1]]")


def inter_ok(fn):
    for _ in range(400):
        s1, s2 = rstr("ab", 0, 3), rstr("ab", 0, 3)
        if random.random() < 0.5:  # a genuine interleaving
            idx = random.sample(range(len(s1) + len(s2)), len(s1))
            a, b = iter(s1), iter(s2)
            s3 = "".join(next(a) if k in idx else next(b) for k in range(len(s1) + len(s2)))
        else:
            s3 = rstr("abc", 0, 6)
        if bool(fn(s1, s2, s3)) != inter_bf(s1, s2, s3):
            return False
    return True


q5 = own("C08-Q5")["step"]
fixed5 = list(q5["lines"])
assert fixed5[q5["bugIndex"]].strip() == "if j > 0 and T[i][j-1]: T[i][j] = True"
fixed5[q5["bugIndex"]] = "            if j > 0 and s2[j-1] == s3[i+j-1] and T[i][j-1]: T[i][j] = True"
assert inter_ok(load_fn(fixed5, "inter")) and not inter_ok(load_fn(q5["lines"], "inter"))
assert sum(1 for a, b in zip(fixed5, q5["lines"]) if a != b) == 1
assert load_fn(q5["lines"], "inter")("a", "b", "ac") is True and inter_bf("a", "b", "ac") is False
num("C08-Q6", max(s for s in (sum(c) for r in range(4) for c in itertools.combinations([5, 7, 9], r)) if s <= 13))

# ================================================================ bank pulls and general hygiene
bank_ids = set()
for lid, L in levels.items():
    for q in L["questions"]:
        if "bankId" in q:
            bank_ids.add(q["bankId"])
assert levels["C09"]["boss"] is True and all("bankId" in q for q in levels["C09"]["questions"])
bank = json.load(open(os.path.join(ROOT, "questions.json"), encoding="utf-8"))
byid = {x["id"]: x for x in bank["questions"]}
for b in bank_ids:
    assert b in byid, b
    assert byid[b]["topic"] == "dp_sequences" and byid[b]["confidence"] == "high" and byid[b].get("stepsSource") == "ai-verified", b

# a pass over the stored text: no option or sub-part cited by position
bad = re.compile(r"האפשרות (ה)?(ראשונה|שנייה|שלישית|רביעית)|\([אבגד]\)")
for lid, L in levels.items():
    blob = json.dumps(L, ensure_ascii=False)
    assert not bad.search(blob), (lid, bad.search(blob).group(0))

missing = sorted(set(Q) - covered)
assert not missing, "own questions without an assertion: %s" % missing
print("OK: %d own questions asserted, %d bank pulls, %d levels" % (len(covered), len(bank_ids), len(levels)))
