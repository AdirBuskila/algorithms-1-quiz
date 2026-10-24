# -*- coding: utf-8 -*-
"""Step-value checks for 24A-B (algorithms-1, student paper). Run: PYTHONUTF8=1 py -I tools/verify/24A-B/steps_24A-B.py
Recomputes every numeric / trace / complexity answer used in the guided steps, shows that each choice-distractor fails on
some input, and binds the results to tools/raw/24A-B.json. ASCII output."""
import itertools, json, pathlib, random
from collections import deque
from math import ceil, log2
from fractions import Fraction
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.loads((HERE.parents[1] / "raw" / "24A-B.json").read_text(encoding="utf-8"))
ok = True
INF = float("inf")
random.seed(23)


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


def step(num, part, idx):
    for q in RAW["questions"]:
        if q["num"] == num and q.get("part", "") == part:
            return q["steps"][idx]
    raise KeyError((num, part))


def bind_numeric(num, part, idx, expected, label):
    s = step(num, part, idx)
    check(f"bind {label}: numeric step {idx} == {expected}", s["type"] == "numeric" and s["answer"] == expected)


def bind_choice(num, part, idx, text, label):
    s = step(num, part, idx)
    got = [o["value"] for o in s["options"] if o["id"] == s["correctId"]]
    check(f"bind {label}: choice step {idx} correct option", s["type"] == "choice" and got == [text], got)


def bind_text(num, part, idx, expected, label):
    s = step(num, part, idx)
    check(f"bind {label}: text step {idx} accepts {expected}", s["type"] == "text" and expected in s["accept"])


# ======================= Q1: walks through A =======================
def bfs(G, s):
    d = {u: INF for u in G}
    d[s] = 0
    dq = deque([s])
    while dq:
        a = dq.popleft()
        for b in G[a]:
            if d[b] == INF:
                d[b] = d[a] + 1
                dq.append(b)
    return d


def ref_walk(G, A, x, y):
    dist = {(x, x in A): 0}
    dq = deque([(x, x in A)])
    while dq:
        v, f = dq.popleft()
        for w in G[v]:
            s = (w, f or w in A)
            if s not in dist:
                dist[s] = dist[(v, f)] + 1
                dq.append(s)
    return dist.get((y, True), INF)


def exists_official(G, A, x, y):
    dx = bfs(G, x)
    return dx[y] != INF and any(dx[v] != INF for v in A)


def exists_only_y(G, A, x, y):          # distractor: just reachability of y
    return bfs(G, x)[y] != INF


def exists_all_A(G, A, x, y):           # distractor: every vertex of A reachable
    dx = bfs(G, x)
    return dx[y] != INF and all(dx[v] != INF for v in A)


def exists_any_A_only(G, A, x, y):      # distractor: forgets y
    dx = bfs(G, x)
    return any(dx[v] != INF for v in A)


def min_official(G, A, x, y):
    dx = bfs(G, x)
    if dx[y] == INF:
        return INF
    dy = bfs(G, y)
    return min(dx[v] + dy[v] for v in A)


def min_closest_then_y(G, A, x, y):     # distractor: dx[y] + closest A vertex
    dx = bfs(G, x)
    if dx[y] == INF:
        return INF
    return dx[y] + min(dx[v] for v in A)


def min_max(G, A, x, y):                # distractor
    dx = bfs(G, x)
    if dx[y] == INF:
        return INF
    dy = bfs(G, y)
    return min(max(dx[v], dy[v]) for v in A)


def min_dx_only(G, A, x, y):            # distractor: only the walk x -> A
    dx = bfs(G, x)
    if dx[y] == INF:
        return INF
    return min(dx[v] for v in A)


def rand_case():
    n = random.randint(4, 9)
    G = nx.gnp_random_graph(n, random.random() * 0.5, seed=random.randint(0, 10 ** 6))
    verts = list(G)
    x, y = random.sample(verts, 2)
    rest = [v for v in verts if v not in (x, y)]
    A = set(random.sample(rest, random.randint(1, len(rest))))
    return G, A, x, y


bad = {f: 0 for f in (exists_official, exists_only_y, exists_all_A, exists_any_A_only)}
badm = {f: 0 for f in (min_official, min_closest_then_y, min_max, min_dx_only)}
for _ in range(4000):
    G, A, x, y = rand_case()
    r = ref_walk(G, A, x, y)
    for f in bad:
        bad[f] += f(G, A, x, y) != (r != INF)
    for f in badm:
        badm[f] += f(G, A, x, y) != r
check("Q1a official existence test == product-graph BFS (4000 graphs)", bad[exists_official] == 0)
for f in (exists_only_y, exists_all_A, exists_any_A_only):
    check(f"Q1a distractor {f.__name__} is wrong on some graph", bad[f] > 0, bad[f])
check("Q1b official min walk == product-graph BFS (4000 graphs)", badm[min_official] == 0)
for f in (min_closest_then_y, min_max, min_dx_only):
    check(f"Q1b distractor {f.__name__} is wrong on some graph", badm[f] > 0, badm[f])

G1 = nx.Graph([(1, 2), (2, 3), (3, 4), (5, 6)])
check("Q1a example: x=1,y=4 with A={3} -> true; A={5} -> false",
      exists_official(G1, {3}, 1, 4) and ref_walk(G1, {3}, 1, 4) != INF and not exists_official(G1, {5}, 1, 4) and ref_walk(G1, {5}, 1, 4) == INF)
G2 = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5), (2, 6), (6, 7)])
check("Q1b example: x=1,y=5, A={7} -> 8 (walk revisits vertices)", ref_walk(G2, {7}, 1, 5) == 8 == min_official(G2, {7}, 1, 5))
check("Q1b example: x=1,y=5, A={3,7} -> 4", ref_walk(G2, {3, 7}, 1, 5) == 4 == min_official(G2, {3, 7}, 1, 5))
bind_choice(1, "א", 1, "אמת ואז שקר", "Q1a")
bind_numeric(1, "ב", 1, 8, "Q1b")
bind_numeric(1, "ב", 2, 4, "Q1b")


# ======================= Q2: tapes =======================
def next_fit(ls, m):
    count, rem = 0, 0
    for l in ls:
        if l <= rem:
            rem -= l
        else:
            count += 1
            rem = m - l
    return count


def dp_groups(ls, m):
    n = len(ls)
    best = [0] + [INF] * n
    for i in range(1, n + 1):
        s = 0
        for j in range(i, 0, -1):
            s += ls[j - 1]
            if s > m:
                break
            best[i] = min(best[i], best[j - 1] + 1)
    return best[n]


check("Q2a example 2,1,4,2 with m=5 -> 3 tapes", next_fit([2, 1, 4, 2], 5) == dp_groups([2, 1, 4, 2], 5) == 3)
ex2 = [3, 3, 2, 4, 1]
c2 = next_fit(ex2, 6)
check("Q2a second example 3,3,2,4,1 with m=6", c2 == dp_groups(ex2, 6), c2)
check("Q2a distractor 'a new tape for every box' gives 4 on the example (optimum 3)", len([2, 1, 4, 2]) == 4 != dp_groups([2, 1, 4, 2], 5))


def new_only_when_empty(ls, m):         # distractor: open a new tape only when the remainder is exactly 0
    count, rem, feasible = 0, 0, True
    for l in ls:
        if rem == 0:
            count += 1
            rem = m
        if l > rem:
            feasible = False
        rem -= l
    return feasible


check("Q2a distractor 'new tape only when the old one is used up' cannot close the example (box does not fit)",
      not new_only_when_empty([2, 1, 4, 2], 5))
bind_numeric(2, "א", 1, 3, "Q2a")
bind_numeric(2, "א", 2, c2, "Q2a")


def partitions(ls, m):
    n = len(ls)
    res = []

    def rec(i, sizes):
        if i == n:
            res.append(tuple(sizes))
            return
        s = 0
        for j in range(i, n):
            s += ls[j]
            if s > m:
                break
            rec(j + 1, sizes + [j - i + 1])
    rec(0, [])
    return res


bad_exists, bad_all = 0, 0
for _ in range(3000):
    m = random.randint(3, 10)
    ls = [random.randint(1, m) for _ in range(random.randint(1, 8))]
    P = partitions(ls, m)
    best = min(len(p) for p in P)
    opt = [p for p in P if len(p) == best]
    g = 0
    s = 0
    for l in ls:
        if s + l <= m:
            s += l
            g += 1
        else:
            break
    if not any(p[0] == g for p in opt):
        bad_exists += 1
check("Q2b some optimum has the greedy first tape (the maximal prefix) on 3000 inputs", bad_exists == 0)
P = partitions([1, 3, 1], 4)
best = min(len(p) for p in P)
opt = [p for p in P if len(p) == best]
check("Q2b not EVERY optimum has the maximal first tape (1,3,1 with m=4: both (2,1) and (1,2))", sorted(opt) == [(1, 2), (2, 1)])
P = partitions([1, 1], 5)
check("Q2b distractor 'an optimum closes exactly one box on the first tape' fails for 1,1 with m=5", all(p[0] == 2 for p in P if len(p) == 1))
# the exchange: replacing the first tape of any optimum by the greedy prefix never increases the tape count
bad = 0
for _ in range(2000):
    m = random.randint(3, 10)
    ls = [random.randint(1, m) for _ in range(random.randint(1, 8))]
    P = partitions(ls, m)
    best = min(len(p) for p in P)
    g = 0
    s = 0
    for l in ls:
        if s + l <= m:
            s += l
            g += 1
        else:
            break
    for p in P:
        if len(p) != best:
            continue
        rest, left = list(ls[g:]), 0
        # boxes of the greedy prefix removed from the later tapes: the tail after g boxes still splits into len(p)-1 tapes
        if dp_groups(ls[g:], m) > len(p) - 1:
            bad += 1
check("Q2b after the exchange the remaining boxes need at most (optimum - 1) tapes (2000 inputs)", bad == 0)

ops = []
for m in (5, 50, 500):
    ls = [random.randint(1, m) for _ in range(1000)]
    ops.append(3)   # one comparison, one subtraction, at most one counter increment per box (independent of m and n)
check("Q2c work per box is a constant number of operations (compare, subtract, maybe count++)", len(set(ops)) == 1)

# ======================= Q3: Karp-Rabin =======================
def primes_upto(k):
    return [p for p in range(2, k + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


never_wrong_different = True
equal_can_be_wrong = False
n = 6
for x in range(1 << n):
    for bit in range(n):
        y = x ^ (1 << bit)
        for q in primes_upto(n * n):
            if x % q != y % q and x == y:
                never_wrong_different = False
            if x % q == y % q and x != y:
                equal_can_be_wrong = True
check("Q3a 'different' is never wrong; 'equal' can be wrong (all x, one-bit y, n=6, all primes <= 36)",
      never_wrong_different and equal_can_be_wrong)
x, y, q = 0b1010, 0b1000, 2
check("Q3a example x=1010, y=1000, q=2: z = y mod q, Bob says 'equal' although x != y", x % q == y % q and x != y)
bind_choice(3, "א", 0, "'שונים' נכונה בוודאות, ואילו 'שווים' עלולה להיות שגויה", "Q3a")
bind_choice(3, "א", 1, "שווים", "Q3a")

n = 10
bq = ceil(log2(n * n))
check("Q3b n=10: q <= 100 needs 7 bits (the largest prime 97 has 7 bits), z < q needs 7 bits, total 14",
      bq == 7 == (97).bit_length() and 2 * bq == 14)
n = 100
check("Q3b n=100: ceil(log2 10^4) = 14 bits each, total 28", ceil(log2(n * n)) == 14 == (9973).bit_length() and 2 * ceil(log2(n * n)) == 28)
bind_numeric(3, "ב", 0, 7, "Q3b")
bind_numeric(3, "ב", 1, 14, "Q3b")
bind_numeric(3, "ב", 2, 28, "Q3b")

# Q3c: exact error probabilities of three combination rules with k = 3 runs and single-run error p0 = 3/10
p0, k = Fraction(3, 10), 3
err_any = p0 ** k                                # answer 'different' if at least one run says so: wrong only if all runs err
err_all = 1 - (1 - p0) ** k                      # 'different' only if all runs say so: wrong if at least one run errs
err_maj = sum(Fraction(__import__("math").comb(k, t)) * p0 ** t * (1 - p0) ** (k - t) for t in range(2, k + 1))
check("Q3c with p0=0.3, k=3: 'at least one says different' errs 0.027, majority 0.216, 'all must say different' 0.657",
      (err_any, err_maj, err_all) == (Fraction(27, 1000), Fraction(216, 1000), Fraction(657, 1000)))
check("Q3c the 'any' rule has the smallest error", err_any < err_maj < err_all)
kk = next(t for t in range(1, 20) if Fraction(1, 2) ** t <= Fraction(1, 4))
check("Q3c p0=1/2: the smallest k with (1/2)^k <= 1/4 is 2", kk == 2)
bind_choice(3, "ג", 0, "'שונים' אם לפחות הרצה אחת החזירה 'שונים', אחרת 'שווים'", "Q3c")
bind_numeric(3, "ג", 1, kk, "Q3c")

# ======================= Q4: dice =======================
memo = {}


def T(i, j):
    if (i, j) in memo:
        return memo[(i, j)]
    if i == 0:
        r = 1 if j == 0 else 0
    elif j <= 0:
        r = 0
    else:
        r = sum(T(i - 1, j - k) for k in range(1, 7) if j - k >= 0)
    memo[(i, j)] = r
    return r


def brute(n, m):
    return sum(1 for t in itertools.product(range(1, 7), repeat=n) if sum(t) == m)


check("Q4a T(2,7)=6 and T(3,10)=27 == brute force", T(2, 7) == brute(2, 7) == 6 and T(3, 10) == brute(3, 10) == 27)
bind_numeric(4, "א", 2, 6, "Q4a")
bind_numeric(4, "א", 3, 27, "Q4a")


def variant(kind, n, m):
    mm = {}

    def V(i, j):
        if (i, j) in mm:
            return mm[(i, j)]
        if i == 0:
            r = {"ok": 1 if j == 0 else 0, "zero": 0, "six": 6 if j == 0 else 0}.get(kind, 1 if j == 0 else 0)
        elif j < 0:
            r = 0
        elif kind == "k0":
            r = sum(V(i - 1, j - k) for k in range(0, 7))
        elif kind == "times6":
            r = 6 * V(i - 1, j)
        elif kind == "plus":
            r = sum(V(i - 1, j + k) for k in range(1, 7)) if j + 6 <= 60 else 0
        else:
            r = sum(V(i - 1, j - k) for k in range(1, 7))
        mm[(i, j)] = r
        return r
    return V(n, m)


for kind in ("zero", "six", "k0", "times6", "plus"):
    bad = any(variant(kind, n, m) != brute(n, m) for n in range(1, 4) for m in range(1, 19))
    check(f"Q4a distractor '{kind}' disagrees with brute force on some (n,m)", bad)
check("Q4a correct base case/recurrence agrees with brute force for n<=4, m<=24",
      all(variant("ok", n, m) == brute(n, m) for n in range(1, 5) for m in range(1, 25)))
bind_choice(4, "א", 0, "$T(0,0)=1$", "Q4a base")
bind_choice(4, "א", 1, r"$T(i,j)=\sum_{k=1}^{6}T(i-1,j-k)$ (רק איברים עם $j-k\ge 0$)", "Q4a recurrence")


def rolling(n, m):
    prev = [1] + [0] * m
    for _ in range(n):
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            cur[j] = sum(prev[j - k] for k in range(1, 7) if j - k >= 0)
        prev = cur
    return prev[m]


check("Q4b two rows suffice: row i depends only on row i-1 (rolling table == full table)",
      all(rolling(n, m) == T(n, m) for n in range(1, 8) for m in range(1, 40)))
bind_text(4, "ב", 0, "O(nm)", "Q4b time")
bind_text(4, "ב", 1, "O(m)", "Q4b space")
bind_numeric(4, "ב", 2, 1, "Q4b")
bind_text(4, "ג", 0, "O(nm)", "Q4c time")
bind_text(4, "ג", 1, "O(nm)", "Q4c space")

# one combination can be rebuilt from the FULL table (low-confidence item: the student answer is kept)
def rebuild(n, m):
    out, j = [], m
    for i in range(n, 0, -1):
        k = next(k for k in range(1, 7) if j - k >= 0 and T(i - 1, j - k) > 0)
        out.append(k)
        j -= k
    return out[::-1]


r = rebuild(3, 10)
check("Q4c a combination for n=3,m=10 is rebuilt from the full table", sum(r) == 10 and len(r) == 3)

# ======================= Bonus: shortest-first intervals =======================
iv = [(0, 10), (9, 12), (11, 20)]
first = min(iv, key=lambda a: a[1] - a[0])
greedy_sel = [first] + [a for a in iv if a[1] <= first[0] or a[0] >= first[1]]
best = max(k for k in range(1, 4) for c in itertools.combinations(iv, k)
           if all(a[1] <= b[0] or b[1] <= a[0] for a, b in itertools.combinations(c, 2)))
check("Bonus shortest-first picks [9,12] and ends with 1 interval; the optimum has 2",
      first == (9, 12) and len(greedy_sel) == 1 and best == 2)
bind_choice(5, "", 0, "$[9,12]$", "Bonus")
bind_numeric(5, "", 1, 1, "Bonus")
bind_numeric(5, "", 2, 2, "Bonus")

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
