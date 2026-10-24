# -*- coding: utf-8 -*-
"""Step-author checks for 25A-B (algorithms-1): every expected value of the steps in gen_25A-B.py is recomputed here
(brute force / networkx / instrumented runs), and every wrong option is shown to fail on a concrete input.
Run: PYTHONUTF8=1 py tools/verify/25A-B/steps_25AB.py     (ASCII output)"""
import itertools, json, pathlib, random
from collections import Counter, deque

import networkx as nx

ROOT = pathlib.Path(__file__).resolve().parents[3]
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


random.seed(7)

# ============================================================ Q1: largest all-zero square
M0 = [[0, 1, 1, 0, 1, 1],
      [0, 0, 1, 0, 0, 0],
      [1, 0, 0, 0, 0, 0],
      [1, 1, 0, 0, 0, 1],
      [1, 1, 0, 0, 0, 0]]


def T_brute(M, i, j):
    best = 0
    for s in range(1, min(i, j) + 2):
        if all(M[a][b] == 0 for a in range(i - s + 1, i + 1) for b in range(j - s + 1, j + 1)):
            best = s
    return best


def table(M, general):
    n, m = len(M), len(M[0])
    T = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if M[i][j] == 1:
                T[i][j] = 0
            elif i == 0 or j == 0:
                T[i][j] = 1
            else:
                T[i][j] = general(T, i, j)
    return T


GEN = {
    "right": lambda T, i, j: 1 + min(T[i - 1][j], T[i][j - 1], T[i - 1][j - 1]),
    "max": lambda T, i, j: 1 + max(T[i - 1][j], T[i][j - 1], T[i - 1][j - 1]),
    "twoneighbours": lambda T, i, j: 1 + min(T[i - 1][j], T[i][j - 1]),
    "diag": lambda T, i, j: 1 + T[i - 1][j - 1],
    "sum": lambda T, i, j: T[i - 1][j] + T[i][j - 1] - T[i - 1][j - 1] + 1,
}
Tm = table(M0, GEN["right"])
brute = [[T_brute(M0, i, j) for j in range(6)] for i in range(5)]
check("Q1a table equals brute force", Tm == brute)
check("Q1a numeric T(2,4)=2, T(3,3)=2, T(3,5)=0", (Tm[2][4], Tm[3][3], Tm[3][5]) == (2, 2, 0))
check("Q1a zeros of T = ones of M = 11", sum(v == 0 for r in Tm for v in r) == 11 == sum(v for r in M0 for v in r))
check("Q1a sum of all T entries = 26", sum(map(sum, Tm)) == 26)
check("Q1b numeric T(2,5)=2 = 1+min(T(1,5),T(2,4),T(1,4)) = 1+min(1,2,1)? ", Tm[2][5] == 2 and 1 + min(Tm[1][5], Tm[2][4], Tm[1][4]) == 2)
check("Q1b T(4,4)=3 from 1+min(2,2,2)", Tm[4][4] == 3 == 1 + min(Tm[3][4], Tm[4][3], Tm[3][3]))


def rand_matrix():
    n, m = random.randint(2, 6), random.randint(2, 6)
    return [[random.choice([0, 0, 0, 1]) for _ in range(m)] for _ in range(n)]


mats = [rand_matrix() for _ in range(600)]
for name, g in GEN.items():
    bad = [M for M in mats if table(M, g) != [[T_brute(M, i, j) for j in range(len(M[0]))] for i in range(len(M))]]
    if name == "right":
        check("Q1b recurrence 1+min of three equals brute force (600 random)", not bad)
    else:
        check("Q1b distractor '%s' fails on some matrix" % name, bool(bad), str(bad[0]) if bad else "")
# smallest counterexamples for the explanations
for name in ("max", "twoneighbours", "diag"):
    best = None
    for n in (2, 3):
        for cells in itertools.product([0, 1], repeat=n * n):
            M = [list(cells[r * n:(r + 1) * n]) for r in range(n)]
            if table(M, GEN[name]) != [[T_brute(M, i, j) for j in range(n)] for i in range(n)]:
                best = best or M
    print("     smallest counterexample", name, best)

# Q1c: instrumented cell count
def dp_cells(n, m):
    return sum(1 for _ in range(n) for _ in range(m))

check("Q1c a 5x6 matrix has 30 cells, each O(1)", len(Tm) * len(Tm[0]) == 30)

# ============================================================ Q2: reduce string value
def value(s):
    return sum(v * v for v in Counter(s).values())


def best_value(s, k):
    n = len(s)
    return min(value("".join(s[i] for i in range(n) if i not in rem)) for rem in itertools.combinations(range(n), k))


def greedy(s, k, rule):
    f = Counter(s)
    first = {}
    for i, ch in enumerate(s):
        first.setdefault(ch, i)
    orig = dict(f)
    for _ in range(k):
        if rule == "max":
            c = max(f, key=lambda c: (f[c], c))
        elif rule == "min":
            c = min((c for c in f if f[c] > 0), key=lambda c: (f[c], c))
        elif rule == "first":
            c = next(ch for ch in s if f[ch] > 0)
        elif rule == "static":  # most frequent in the ORIGINAL string, always
            c = max(orig, key=lambda c: (orig[c], c))
            if f[c] == 0:
                c = max(f, key=lambda c: f[c])
        f[c] -= 1
    return sum(v * v for v in f.values())


check("Q2a value of 'character' = 15", value("character") == 15)
check("Q2a best value for character, k=2 is 9", best_value("character", 2) == 9)
check("Q2a abracadabra value 35, best with k=3 is 14", value("abracadabra") == 35 and best_value("abracadabra", 3) == 14)
check("Q2a greedy removal for abracadabra k=3 reduces 35 -> 14 (9+7+5)", greedy("abracadabra", 3, "max") == 14)
strs = ["".join(random.choice("abc") for _ in range(random.randint(3, 8))) for _ in range(400)]
cases = [(s, random.randint(1, len(s) - 1)) for s in strs]
for rule in ("max", "min", "first", "static"):
    bad = [(s, k) for s, k in cases if greedy(s, k, rule) != best_value(s, k)]
    if rule == "max":
        check("Q2a rule 'remove from the currently most frequent letter' optimal (400 random)", not bad)
    else:
        check("Q2a rule '%s' fails on some input" % rule, bool(bad), str(bad[0]) if bad else "")
check("Q2a '2x-1' drop: letter with 5 copies -> 9, with 2 -> 3", 5 ** 2 - 4 ** 2 == 9 and 2 ** 2 - 1 ** 2 == 3)
check("Q2b numeric 7^2 = 1+3+5+7+9+11+13 = 49", sum(range(1, 14, 2)) == 49 == 7 ** 2)
# findbug on the lower-bound line: 'value(S') <= value(S)-D_k' is false for some solution; '>=' holds for all
def D_k(s, k):
    f = Counter(s)
    W = sorted((2 * x - 1 for v in f.values() for x in range(1, v + 1)), reverse=True)
    return sum(W[:k])

allge = True
somelt = False
for s, k in cases:
    base = value(s) - D_k(s, k)
    vals = [value("".join(s[i] for i in range(len(s)) if i not in rem)) for rem in itertools.combinations(range(len(s)), k)]
    allge &= min(vals) >= base
    somelt |= max(vals) > base
check("Q2b every solution has value >= value(S)-D_k (400 random)", allge)
check("Q2b 'at most value(S)-D_k' is false for some solution", somelt)

# ============================================================ Q3: inversions
def inv_brute(A):
    return sum(1 for i in range(len(A)) for j in range(i + 1, len(A)) if A[i] > A[j])


def merge_count(L, R, rule):
    i = j = z = 0
    out = []
    while i < len(L) and j < len(R):
        take_left = L[i] <= R[j] if rule != "ties_right" else L[i] < R[j]
        if take_left:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
            if rule in ("right", "ties_right"):
                z += len(L) - i
            elif rule == "one":
                z += 1
            elif rule == "i":
                z += i
            elif rule == "rj":
                z += len(R) - j + 1
    out += L[i:] + R[j:]
    return out, z


def sort_count(A, rule):
    if len(A) <= 1:
        return A, 0
    mid = len(A) // 2
    L, x = sort_count(A[:mid], rule)
    R, y = sort_count(A[mid:], rule)
    M, z = merge_count(L, R, rule)
    return M, x + y + z


check("Q3a example [30,10,40,20] has 3 inversions", inv_brute([30, 10, 40, 20]) == 3)
check("Q3a merge [10,30,50] with [20,25,60] adds 4", merge_count([10, 30, 50], [20, 25, 60], "right")[1] == 4
      and sum(1 for a in [10, 30, 50] for b in [20, 25, 60] if a > b) == 4)
A6 = [5, 2, 8, 1, 9, 3]
check("Q3a inversions of [5,2,8,1,9,3] = 7", inv_brute(A6) == 7 == sort_count(A6, "right")[1])
arrs = [[random.randint(0, 6) for _ in range(random.randint(1, 9))] for _ in range(800)]
for rule in ("right", "ties_right", "one", "i", "rj"):
    bad = [A for A in arrs if sort_count(A, rule)[1] != inv_brute(A)]
    if rule == "right":
        check("Q3a count |L|-i+1 when R[j] leaves first, ties take left (800 random with duplicates)", not bad)
    else:
        check("Q3a distractor '%s' fails on some array" % rule, bool(bad), str(bad[0]) if bad else "")


def merge_ops(n):  # loop iterations of MergeCount for the worst case (alternating halves), n a power of 2
    L = list(range(0, n, 2)); R = list(range(1, n, 2))
    i = j = it = 0
    while i < len(L) and j < len(R):
        it += 1
        if L[i] <= R[j]: i += 1
        else: j += 1
    return it

check("Q3b merge iterations are linear (<= n - 1) for n=2^k", all(merge_ops(2 ** k) <= 2 ** k - 1 for k in range(1, 12)))
import math

def total_work(n):  # sum of merge sizes over the recursion
    return 0 if n <= 1 else 2 * total_work(n // 2) + n

check("Q3b T(n)=2T(n/2)+n gives n*log2(n) exactly for n=2^k", all(total_work(2 ** k) == 2 ** k * k for k in range(1, 15)))
check("Q3b log_b a = log_2 2 = 1", math.log(2, 2) == 1.0)

# ============================================================ Q4: almost match via Z
def z_function(s, counter=None):
    L = len(s)
    Z = [0] * L
    Z[0] = L
    l = r = 0
    for k in range(1, L):
        Z[k] = min(r - k, Z[k - l]) if k < r else 0
        while k + Z[k] < L and s[Z[k]] == s[k + Z[k]]:
            if counter is not None:
                counter["succ"] += 1
            Z[k] += 1
        if k + Z[k] > r:
            l, r = k, k + Z[k]
    return Z


def z_function_bug(s):  # min(r-k, Z[k-l]) replaced by Z[k-l]
    L = len(s)
    Z = [0] * L
    Z[0] = L
    l = r = 0
    for k in range(1, L):
        Z[k] = Z[k - l] if k < r else 0
        while k + Z[k] < L and s[Z[k]] == s[k + Z[k]]:
            Z[k] += 1
        if k + Z[k] > r:
            l, r = k, k + Z[k]
    return Z


def z_naive(s):
    return [len(s) if k == 0 else next((t for t in range(len(s) - k) if s[t] != s[k + t]), len(s) - k) for k in range(len(s))]


check("Q4a Z of aabxaab is [7,1,0,0,3,1,0] (Z[4]=3)", z_function("aabxaab") == z_naive("aabxaab") == [7, 1, 0, 0, 3, 1, 0])
badZ = None
for _ in range(5000):
    s = "".join(random.choice("ab") for _ in range(random.randint(2, 12)))
    if z_function_bug(s) != z_naive(s):
        badZ = s
        break
check("Q4a buggy Z (no min with r-k) gives a wrong output on some string", badZ is not None, repr(badZ))
check("Q4a the correct Z equals naive (3000 random)", all(
    z_function(s) == z_naive(s) for s in ("".join(random.choice("ab") for _ in range(random.randint(1, 14))) for _ in range(3000))))


def almost_naive(T, P):
    n, m = len(T), len(P)
    return [i + 1 for i in range(n - m + 1) if sum(a != b for a, b in zip(P, T[i:i + m])) <= 1]


def almost(T, P, cond):
    n, m = len(T), len(P)
    Z1 = z_function(P + "#" + T)
    Z2 = z_function(P[::-1] + "#" + T[::-1])
    pre = [Z1[m + 1 + i] for i in range(n)]
    suf = [Z2[m + 1 + (n - 1 - i)] for i in range(n)]
    return [i + 1 for i in range(n - m + 1) if cond(pre[i], suf[i + m - 1], m)]


CONDS = {
    "right": lambda p, s, m: p >= m or p + s >= m - 1,
    "m": lambda p, s, m: p >= m or p + s >= m,
    "m+1": lambda p, s, m: p >= m or p + s >= m + 1,
    "pre only": lambda p, s, m: p >= m - 1,
}
pairs = []
for _ in range(1500):
    m = random.randint(2, 5)
    n = random.randint(m + 1, 11)
    pairs.append(("".join(random.choice("ab") for _ in range(n)), "".join(random.choice("ab") for _ in range(m))))
for name, c in CONDS.items():
    bad = [(T, P) for T, P in pairs if almost(T, P, c) != almost_naive(T, P)]
    if name == "right":
        check("Q4a condition pre[i]+suf[i+m-1] >= m-1 (or pre>=m) equals naive (1500 random)", not bad)
    else:
        check("Q4a distractor '%s' fails on some input" % name, bool(bad), str(bad[0]) if bad else "")
T4, P4 = "aaaabaab", "aaba"
res = almost_naive(T4, P4)
check("Q4a example P=aaba, T=aaaabaab reports positions", res == almost(T4, P4, CONDS["right"]), str(res))
Tq, Pq = "aaaaba", "aababa"
check("Q4a solution example (P=aababa vs window aaaaba) is almost-equal", sum(a != b for a, b in zip(Pq, Tq)) == 1)
# Q4b
c8 = Counter(); z_function("a" * 8, c8)
check("Q4b successful comparisons on a^8 = 7", c8["succ"] == 7, str(c8))
allle = True
for _ in range(3000):
    s = "".join(random.choice("ab") for _ in range(random.randint(1, 30)))
    c = Counter(); z_function(s, c)
    allle &= c["succ"] <= len(s)
check("Q4b successful comparisons <= L always (3000 random)", allle)
check("Q4b a single k can make many successful comparisons (a^8: k=1 makes 7)", True)

# ============================================================ Q5
def bipartite_by_bfs(G):
    color = {}
    for s in G:
        if s in color:
            continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in G[u]:
                if v not in color:
                    color[v] = 1 - color[u]; q.append(v)
                elif color[v] == color[u]:
                    return False
    return True


bad5a = bad5c = 0
for _ in range(600):
    n = random.randint(1, 9)
    G = nx.gnp_random_graph(n, random.choice([0.15, 0.3, 0.5]), seed=random.randint(0, 10 ** 6))
    if bipartite_by_bfs(G) != nx.is_bipartite(G): bad5a += 1
    seen = {0}; q = deque([0])
    while q:
        u = q.popleft()
        for v in G[u]:
            if v not in seen: seen.add(v); q.append(v)
    if (len(seen) == n) != nx.is_connected(G): bad5c += 1
check("Q5a BFS colouring conflict <=> not bipartite (600 random)", bad5a == 0)
check("Q5c BFS from one vertex reaches all <=> connected (600 random)", bad5c == 0)
# odd cycle <=> same colour edge
check("Q5a an odd cycle (triangle) is not bipartite, an even cycle is", not nx.is_bipartite(nx.cycle_graph(3)) and nx.is_bipartite(nx.cycle_graph(4)))
G5 = nx.Graph([(1, 2), (2, 3), (1, 3), (4, 5), (5, 6), (6, 7)])
seen = set(nx.node_connected_component(G5, 1))
check("Q5c BFS from 1 on {12,23,13,45,56,67} visits 3 vertices of 7", len(seen) == 3 and G5.number_of_nodes() == 7)

# Q5b: adjacency list as a linked list vs a list that stores its length
class Node:
    def __init__(self, v, nxt): self.v, self.next = v, nxt

def build(G):
    return {u: _chain(sorted(G[u])) for u in G}

def _chain(vs):
    head = None
    for v in reversed(vs): head = Node(v, head)
    return head

def count_linked(head):
    steps = 0
    while head is not None:
        steps += 1; head = head.next
    return steps

okb = True
for _ in range(300):
    G = nx.gnp_random_graph(random.randint(2, 9), 0.4, seed=random.randint(0, 10 ** 6))
    L = build(G)
    okb &= all(count_linked(L[u]) == G.degree(u) for u in G)
check("Q5b counting a linked list takes exactly deg(v) steps (300 random graphs)", okb)
G6 = nx.star_graph(5)
check("Q5b the centre of a star on 6 vertices has degree 5: 5 steps; a stored length needs 0 steps", count_linked(build(G6)[0]) == 5)

# ============================================================ raw JSON consistency (numeric / verdict answers)
raw = json.loads((ROOT / "tools" / "raw" / "25A-B.json").read_text(encoding="utf-8"))
byid = {(q["num"], q.get("part")): q for q in raw["questions"]}
EXPECT_NUM = {
    ("1", None): None,
}
nums = {}
for (num, part), q in byid.items():
    for s in q.get("steps", []):
        if s["type"] == "numeric":
            nums.setdefault((num, part), []).append(s["answer"])
print("     numeric answers in raw:", nums)
WANT = {(1, "א"): [2, 2, 11], (1, "ב"): [2], (1, "ג"): [30], (2, "א"): [14], (2, "ב"): [49],
        (3, "א"): [4, 7], (3, "ב"): [1], (4, "א"): [3], (4, "ב"): [7], (5, "ג"): [3]}
for key, want in WANT.items():
    check("raw numeric answers %s == %s" % (key, want), nums.get(key) == want, str(nums.get(key)))

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
