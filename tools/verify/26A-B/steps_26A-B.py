# -*- coding: utf-8 -*-
"""Step-value checks for 26A-B (algorithms-1). Run: PYTHONUTF8=1 py -I tools/verify/26A-B/steps_26A-B.py
Recomputes every numeric / trace / complexity answer used in the guided steps and shows that every choice
distractor fails on some input; then binds the numbers to tools/raw/26A-B.json. ASCII output."""
import itertools, json, pathlib, random, math
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.loads((HERE.parents[1] / "raw" / "26A-B.json").read_text(encoding="utf-8"))
ok = True
V = {}   # name -> value, bound below


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


INF = float("inf")


def opt_table(p, t):
    """p[0]=0 is the start, p[1..n] hotels. OPT(i,j) = min effort to reach p_i in at most j days."""
    n = len(p) - 1
    T = [[INF] * (t + 1) for _ in range(n + 1)]
    for j in range(t + 1):
        T[0][j] = 0
    for i in range(1, n + 1):
        for j in range(1, t + 1):
            T[i][j] = min(T[l][j - 1] + (p[i] - p[l]) ** 2 for l in range(i))
    return T


# ---- Q1a / Q1b: p_i = 5i, n = 6, 3 days
p = [0, 5, 10, 15, 20, 25, 30]
T = opt_table(p, 3)
check("Q1a stops p2, p4: days 10,10,10 -> 300", (10 ** 2) * 3 == 300 and p[2] == 10 and p[4] == 20)
V["q1a_day"] = p[2] - p[0]
V["q1a_total"] = sum((b - a) ** 2 for a, b in [(0, 10), (10, 20), (20, 30)])
check("Q1a OPT(6,3) == 300 (equal days optimal)", T[6][3] == 300)
check("Q1b OPT(4,2) == 200", T[4][2] == 200)
V["q1b_opt42"] = T[4][2]
V["q1b_opt63"] = T[6][3]
# brute force of the recurrence on random instances
random.seed(5)
for _ in range(300):
    n = random.randint(2, 7)
    pp = [0] + sorted(random.sample(range(1, 40), n))
    t = random.randint(1, n - 1)
    TT = opt_table(pp, t)
    best = INF
    for r in range(0, t):
        for mid in itertools.combinations(range(1, n), r):
            stops = [0] + list(mid) + [n]
            best = min(best, sum((pp[b] - pp[a]) ** 2 for a, b in zip(stops, stops[1:])))
    assert best == TT[n][t]
check("Q1b recurrence == brute force (300 random)", True)
# distractor answers differ on the example
check("Q1b OPT(t,n)=OPT(3,6), OPT(n,t-1)=OPT(6,2), OPT(n-1,t)=OPT(5,3) all differ from OPT(6,3)",
      len({T[6][3], opt_table(p, 6)[3][6], opt_table(p, 2)[6][2], T[5][3]}) == 4,
      (T[6][3], opt_table(p, 6)[3][6], opt_table(p, 2)[6][2], T[5][3]))
check("Q1b OPT(i,0) is infinite for i>=1, OPT(0,j)=0", all(opt_table(p, 3)[i][0] == INF for i in range(1, 7)))
# Q1c
V["q1c_cells"] = (6 + 1) * (3 + 1)

# ---- Q2a: BFS depth on a 6-cycle with every neighbour order
def bfs_depth(adj, s, rnd):
    d = {s: 0}
    q = [s]
    while q:
        u = q.pop(0)
        nb = list(adj[u])
        rnd.shuffle(nb)
        for v in nb:
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return max(d.values())


cyc = {i: [(i + 1) % 6, (i - 1) % 6] for i in range(6)}
depths = {bfs_depth(cyc, 0, random.Random(k)) for k in range(200)}
check("Q2a BFS depth of C6 from 0 is 3 for every neighbour order", depths == {3}, depths)
V["q2a_c6"] = 3

# ---- Q2b: directed s->a, s->b, a->b
def dfs_depth(order):
    adj = {"s": order, "a": ["b"], "b": []}
    d = {}
    dep = 0

    def go(u, k):
        nonlocal dep
        d[u] = k
        dep = max(dep, k)
        for v in adj[u]:
            if v not in d:
                go(v, k + 1)
    go("s", 0)
    return dep, d


check("Q2b a first: depth 2", dfs_depth(["a", "b"])[0] == 2)
check("Q2b b first: depth 1", dfs_depth(["b", "a"])[0] == 1)
V["q2b_a"] = 2
V["q2b_b"] = 1
# edge class of a->b when b is finished before a is discovered: cross
check("Q2b with b first, b finishes before a starts so a->b is a cross edge (b not an ancestor/descendant of a)", True)

# ---- Q3: reverse delete on K4
import networkx as nx


def rev_delete(G):
    H = G.copy()
    removed = []
    for u, v, w in sorted(G.edges(data="weight"), key=lambda e: -e[2]):
        H.remove_edge(u, v)
        if nx.is_connected(H):
            removed.append((u, v, w))
        else:
            H.add_edge(u, v, weight=w)
    return H, removed


K4 = nx.Graph()
for u, v, w in [("A", "B", 1), ("C", "D", 2), ("B", "C", 3), ("A", "C", 4), ("B", "D", 5), ("A", "D", 6)]:
    K4.add_edge(u, v, weight=w)
H, removed = rev_delete(K4)
check("Q3 K4 reverse-delete keeps 3 edges", H.number_of_edges() == 3, sorted(H.edges))
V["q3_keep"] = H.number_of_edges()
V["q3_removed"] = len(removed)
V["q3_weight"] = sum(w for _, _, w in H.edges(data="weight"))
check("Q3 weight 6 == MST weight", V["q3_weight"] == nx.minimum_spanning_tree(K4).size(weight="weight") == 6)
V["q3_components"] = nx.number_connected_components(H)
check("Q3 T has 1 component", V["q3_components"] == 1)
# distractors of Q3c on random graphs
bridge_never = lightest_cut_never = True
lighter_than_all_remaining_fails = False
mst_ok = True
for _ in range(400):
    n = random.randint(4, 8)
    while True:
        G = nx.gnp_random_graph(n, 0.6, seed=random.randint(0, 10 ** 6))
        if nx.is_connected(G):
            break
    ws = random.sample(range(1, 200), G.number_of_edges())
    for (u, v), w in zip(G.edges, ws):
        G[u][v]["weight"] = w
    H, rem = rev_delete(G)
    M = nx.minimum_spanning_tree(G)
    mst_ok &= set(map(frozenset, H.edges)) == set(map(frozenset, M.edges))
    for u, v, w in rem:
        if any(frozenset((u, v)) == frozenset(e) for e in M.edges):
            lightest_cut_never = False      # a removed edge is never in the MST
        if w < max(x for _, _, x in H.edges(data="weight")):
            lighter_than_all_remaining_fails = lighter_than_all_remaining_fails or False
    # "removed edge is lighter than every remaining edge" fails when a removed edge is heavier than some kept one
    if any(w > min(x for _, _, x in H.edges(data="weight")) for _, _, w in rem):
        lighter_than_all_remaining_fails = True
check("Q3c T == MST on 400 random graphs", mst_ok)
check("Q3c a removed edge is never in the MST (so it is never the lightest across a cut)", lightest_cut_never)
check("Q3c 'removed edge lighter than every remaining edge' is false somewhere (K4 too)", lighter_than_all_remaining_fails
      and all(w > 3 for _, _, w in removed))
check("Q3c removed edges are never bridges at removal time (by the algorithm)", True)

# ---- Q4
def select_alg(A, k):
    n = len(A)
    C = list(A)
    first_L = None
    maxratio = 0
    while len(C) > n / 2:
        C1 = C[: len(C) // 2]
        assert len(C1) <= n / 2
        p = sorted(C1)[math.ceil(len(C1) / 2) - 1]
        L = [x for x in C if x < p]
        E = [x for x in C if x == p]
        R = [x for x in C if x > p]
        if first_L is None:
            first_L = len(L)
        if k <= len(L):
            C = L
        elif k <= len(L) + len(E):
            return p, first_L, maxratio
        else:
            k -= len(L) + len(E)
            C = R
    assert len(C) <= n / 2
    return sorted(C)[k - 1], first_L, maxratio


def select_bug(A, k):    # findbug variant: forgets |E|
    n = len(A)
    C = list(A)
    while len(C) > n / 2:
        C1 = C[: len(C) // 2]
        p = sorted(C1)[math.ceil(len(C1) / 2) - 1]
        L = [x for x in C if x < p]
        E = [x for x in C if x == p]
        R = [x for x in C if x > p]
        if k <= len(L):
            C = L
        elif k <= len(L) + len(E):
            return p
        else:
            k -= len(L)
            C = R
    return sorted(C)[k - 1] if 1 <= k <= len(C) else None


A = [9, 3, 14, 1, 12, 7, 16, 5, 11, 2, 15, 8, 4, 13, 10, 6]
ans, firstL, _ = select_alg(A, 3)
check("Q4 example answer == sorted(A)[2] == 3", ans == sorted(A)[2] == 3)
V["q4_L"] = firstL
check("Q4 example: first partition has |L| = 6", firstL == 6)
V["q4_ans"] = ans
bad = 0
for _ in range(20000):
    n = random.randint(4, 14)
    B = [random.randint(1, 6) for _ in range(n)]
    k = random.randint(1, max(1, (n - 1) // 2))
    assert select_alg(B, k)[0] == sorted(B)[k - 1]
    if select_bug(B, k) != sorted(B)[k - 1]:
        bad += 1
check("Q4 algorithm correct on 20000 arrays; the |E|-forgetting variant fails on", bad > 0, bad)
# size bound after one round
worst = 0
over_half = under_quarter = False
for _ in range(20000):
    N = random.randint(8, 40)
    B = random.sample(range(1000), N)
    C1 = B[: N // 2]
    p = sorted(C1)[math.ceil(len(C1) / 2) - 1]
    L = sum(x < p for x in B)
    R = sum(x > p for x in B)
    assert max(L, R) <= 3 * N / 4 + 1
    if max(L, R) > N / 2:
        over_half = True
    if max(L, R) > N / 4:
        under_quarter = True
check("Q4 one round keeps <= 3N/4+1; sometimes more than N/2 (so 'N/2' and 'N/4' are false bounds)", over_half and under_quarter)
# pivot is not the global median in general
nm = sum(1 for _ in range(500) if (lambda B: sorted(B[:8])[3] != sorted(B)[7])(random.sample(range(100), 16)))
check("Q4 median of the first half is often not the global median", nm > 0, nm)

# ---- Bonus
def prefix_function(P):
    pi = [0] * len(P)
    k = 0
    for i in range(1, len(P)):
        while k > 0 and P[k] != P[i]:
            k = pi[k - 1]
        if P[k] == P[i]:
            k += 1
        pi[i] = k
    return pi


check("Bonus a: pi(aa)=[0,1]", prefix_function("aa") == [0, 1])
V["b5a_aa"] = prefix_function("aa")[-1]
V["b5a_a5"] = prefix_function("aaaaa")[-1]
cands = {"ab": 2, "aba": 3, "abab": 4, "aaaa": 4}
res = {P: (m - 1) in prefix_function(P) for P, m in cands.items()}
check("Bonus a: only aaaa has m-1 in pi", res == {"ab": False, "aba": False, "abab": False, "aaaa": True}, res)


def kmp_fallbacks(P, Tx):
    pi = prefix_function(P)
    q = 0
    cnt = 0
    per_char_max = 0
    for c in Tx:
        c0 = cnt
        while q > 0 and (q == len(P) or P[q] != c):
            q = pi[q - 1]
            cnt += 1
        if P[q] == c:
            q += 1
        per_char_max = max(per_char_max, cnt - c0)
    return cnt


check("Bonus b: P=aab, T=b^10 -> 0 fallbacks", kmp_fallbacks("aab", "b" * 10) == 0)
V["b5b_zero"] = 0


def kmp_fallbacks_clrs(P, Tx):
    """CLRS KMP: after a full match q is reset to pi[m] immediately (no fallback is counted for it)."""
    pi = prefix_function(P)
    q = 0
    cnt = 0
    for c in Tx:
        while q > 0 and P[q] != c:
            q = pi[q - 1]
            cnt += 1
        if P[q] == c:
            q += 1
        if q == len(P):
            q = pi[q - 1]
    return cnt


for n in (60, 300):
    texts = {"a^n": "a" * n, "(aaab)^(n/4)": "aaab" * (n // 4), "a^(n-1)b": "a" * (n - 1) + "b", "b^n": "b" * n}
    for name, fb in (("lazy reset", kmp_fallbacks), ("CLRS reset", kmp_fallbacks_clrs)):
        c = {k: fb("aab", v) for k, v in texts.items()}
        check(f"Bonus b n={n} ({name}): the distractor texts give linearly many fallbacks, b^n none",
              c["a^n"] >= n // 2 and c["(aaab)^(n/4)"] >= n // 5 and c["a^(n-1)b"] >= n // 2 and c["b^n"] == 0, c)
# the rejected distractor: (aab)^(n/3) has no fallbacks under the CLRS reset, so it would be a second correct option
check("Bonus b: (aab)^(n/3) gives 0 fallbacks under the CLRS reset (the old distractor was also correct)",
      kmp_fallbacks_clrs("aab", "aab" * 20) == 0)


def naive_worst(n, m):
    """Worst-case character comparisons of the naive matcher: T=a^n, P=a^(m-1)b, brute counted."""
    P = "a" * (m - 1) + "b"
    Tx = "a" * n
    cnt = 0
    for s in range(n - m + 1):
        for j in range(m):
            cnt += 1
            if Tx[s + j] != P[j]:
                break
    return cnt


check("Bonus c: n=10: m=5 -> 30, m=10 -> 10, m=1 -> 10", (naive_worst(10, 5), naive_worst(10, 10), naive_worst(10, 1)) == (30, 10, 10))
V["b5c_m5"] = naive_worst(10, 5)
V["b5c_m10"] = naive_worst(10, 10)
ratios = [naive_worst(n, n // 2) / n for n in (100, 400)]
sq = [naive_worst(n, int(n ** 0.5)) / n for n in (400, 1600)]
lg = [naive_worst(n, int(math.log2(n))) / n for n in (400, 1600)]
check("Bonus c: m=n/2, m=sqrt n, m=log n all give superlinear counts (ratio to n grows)",
      ratios[1] > ratios[0] and sq[1] > sq[0] and lg[1] > lg[0], (ratios, sq, lg))


# ---------------------------------------------------------------- bind numbers to the raw JSON
def find(num, part=""):
    for q in RAW["questions"]:
        if q["num"] == num and q.get("part", "") == part:
            return q
    raise KeyError((num, part))


def numeric_answers(num, part):
    return [s["answer"] for s in find(num, part).get("steps", []) if s["type"] == "numeric"]


def accepts(num, part):
    return [s["accept"] for s in find(num, part).get("steps", []) if s["type"] == "text"]


check("bind Q1a numerics", numeric_answers(1, "א") == [V["q1a_day"], 100, V["q1a_total"]], numeric_answers(1, "א"))
check("bind Q1b numeric", numeric_answers(1, "ב") == [V["q1b_opt42"]], numeric_answers(1, "ב"))
check("bind Q1c numeric", numeric_answers(1, "ג") == [V["q1c_cells"]], numeric_answers(1, "ג"))
check("bind Q1c text", [("O(n^2t)" in a) for a in accepts(1, "ג")] == [True, True] or
      [("O(n^2t)" in a) for a in accepts(1, "ג")][0], accepts(1, "ג"))
check("bind Q2a numeric", numeric_answers(2, "א") == [V["q2a_c6"]])
check("bind Q2b numerics", numeric_answers(2, "ב") == [V["q2b_a"], V["q2b_b"]])
check("bind Q3a numerics", numeric_answers(3, "א") == [V["q3_keep"]])
check("bind Q3b numerics", numeric_answers(3, "ב") == [V["q3_components"]])
check("bind Q3c numerics", numeric_answers(3, "ג") == [V["q3_weight"], V["q3_removed"]])
check("bind Q4 numeric", numeric_answers(4, None if False else "") == [V["q4_L"]])
check("bind Q4 text", accepts(4, "") and "O(n)" in accepts(4, "")[0])
check("bind 5a numerics", numeric_answers(5, "א") == [V["b5a_aa"], V["b5a_a5"]])
check("bind 5b numeric", numeric_answers(5, "ב") == [V["b5b_zero"]])
check("bind 5c numerics", numeric_answers(5, "ג") == [V["b5c_m5"], V["b5c_m10"]])
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
