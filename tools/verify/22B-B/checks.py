# -*- coding: utf-8 -*-
r"""Verification harness for 22B-B (algorithms-1). Run: PYTHONUTF8=1 py tools/verify/22B-B/checks.py
Checks the official answers (never modifies them). ASCII output. FINDING lines are official-key problems (evidence for
a hold / transcription note); they do not make the script fail."""
import itertools, heapq, random
from collections import Counter
import networkx as nx

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


def finding(name, extra=""):
    print("FINDING " + name + (" " + extra if extra else ""))


# ---------- Huffman helpers (standard rule: pop two smallest, first popped is the 0/left child) ----------
def huffman_codes(freq):
    heap = [(f, i, {s: ""}) for i, (s, f) in enumerate(sorted(freq.items()))]
    heapq.heapify(heap)
    cnt = len(heap)
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        d = {s: "0" + c for s, c in a[2].items()}
        d.update({s: "1" + c for s, c in b[2].items()})
        heapq.heappush(heap, (a[0] + b[0], cnt, d))
        cnt += 1
    return heap[0][2]


# ---------- Q1a: add k to every frequency ----------
S = "bbabbc"
base = Counter(S)
check("Q1a example string bbabbc has counts a=1,b=4,c=1; adding k=1 gives a=2,b=5,c=2 (the printed frequencies)",
      base == Counter({"a": 1, "b": 4, "c": 1}) and {c: base[c] + 1 for c in base} == {"a": 2, "b": 5, "c": 2})
f1 = {c: base[c] + 1 for c in base}
f3 = {c: base[c] + 3 for c in base}
check("Q1a official trees: k=1 sums 2,2,5 -> 4 -> 9 ; k=3 gives 4,4,7 -> 8 -> 15 (matches the drawn weights)",
      sorted(f1.values()) == [2, 2, 5] and sorted(f3.values()) == [4, 4, 7] and sum(f1.values()) == 9 and sum(f3.values()) == 15)
c1, c3 = huffman_codes(f1), huffman_codes(f3)
lens = lambda c: {s: len(v) for s, v in c.items()}
check("Q1a the two official trees have the SAME code lengths (they differ only by mirror orientation)", lens(c1) == lens(c3))
check("Q1a ... but under the 'pop two smallest, first is left' rule the codes themselves differ", c1 != c3,
      "k=1 %s k=3 %s" % (c1, c3))
# a counterexample whose code LENGTHS change when k is added
found = None
for fr in itertools.product(range(1, 7), repeat=4):
    f = {"a": fr[0], "b": fr[1], "c": fr[2], "d": fr[3]}
    for k in range(1, 6):
        g = {s: v + k for s, v in f.items()}
        if sorted(lens(huffman_codes(f)).values()) != sorted(lens(huffman_codes(g)).values()):
            found = (fr, k)
            break
    if found:
        break
check("Q1a a counterexample with genuinely different tree shapes exists (e.g. freqs %s, k=%s)" % (found[0], found[1]) if found else
      "Q1a no shape-changing counterexample found", found is not None)
finding("Q1a official counterexample (4,4,7 vs 2,2,5) has identical tree shape; it only differs in left/right orientation. "
        "The answer 'no' is right; the strong counterexample is e.g. %s with k=%s." % (found[0], found[1]))

# ---------- Q1b: S over {a,b,c}, b appears 2 times, a x times, c y times, code a=1 b=00 c=01, 2+x+y=10 ----------
sol = []
for x in range(1, 9):
    y = 8 - x
    if y < 1:
        continue
    # huffman validity: step 1 merges b and c (the two smallest, ties allowed), then (b,c) with a
    valid = max(2, y) <= x or (max(2, y) <= x)  # b and c are the two smallest of {2,x,y}: needs x >= max(2,y)
    orient = (y + 2 <= x) and (2 <= y)           # left child (b,c: y+2) not heavier than right (a: x); b (left) <= c (right)
    if valid and orient:
        sol.append((x, y))
check("Q1b brute force gives exactly (x,y) in {(6,2),(5,3)} as the official solution", sol == [(5, 3), (6, 2)], str(sol))

# ---------- Q1c: suffix tree of ABABABA ----------
T = "ABABABA$"


def suffix_tree_edges(T):
    """Naive compact suffix tree as set of (parent_path, edge_label, child_path_or_leaf_index)."""
    sufs = {i: T[i:] for i in range(len(T))}
    edges = []

    def build(prefix, idxs):
        groups = {}
        for i in idxs:
            rest = sufs[i][len(prefix):]
            groups.setdefault(rest[0], []).append(i)
        for ch, g in sorted(groups.items()):
            rests = [sufs[i][len(prefix):] for i in g]
            l = 0
            while all(len(r) > l and r[l] == rests[0][l] for r in rests):
                l += 1
            label = rests[0][:l]
            child = prefix + label
            if len(g) == 1:
                edges.append((prefix, label, "leaf%d" % g[0]))
            else:
                edges.append((prefix, label, child))
                build(child, g)
    build("", list(sufs))
    return edges


E = suffix_tree_edges(T)
official = {("", "BA", "BA"), ("", "A", "A"), ("BA", "$", "leaf5"), ("BA", "BA", "BABA"), ("BABA", "$", "leaf3"),
            ("BABA", "BA$", "leaf1"), ("A", "$", "leaf6"), ("A", "BA", "ABA"), ("ABA", "$", "leaf4"), ("ABA", "BA", "ABABA"),
            ("ABABA", "$", "leaf2"), ("ABABA", "BA$", "leaf0")}
true = set(E)
check("Q1c official (hand-drawn) tree equals the true suffix tree of ABABABA$ except the empty-suffix leaf (root --$--> leaf 7)",
      true - official == {("", "$", "leaf7")} and official - true == set())
finding("Q1c official tree has 7 leaves: the leaf for the suffix '$' (index 7) is missing.")

# ---------- Q1d: longest repeated substring = deepest internal node ----------
Ttxt = "ABABABA"
best = ""
for l in range(1, len(Ttxt)):
    for i in range(len(Ttxt) - l + 1):
        s = Ttxt[i:i + l]
        if Ttxt.count(s) < 2:  # overlapping occurrences matter, str.count does not count them
            occ = sum(1 for j in range(len(Ttxt) - l + 1) if Ttxt[j:j + l] == s)
        else:
            occ = sum(1 for j in range(len(Ttxt) - l + 1) if Ttxt[j:j + l] == s)
        if occ >= 2 and len(s) > len(best):
            best = s
deepest_internal = max((c for (_, _, c) in true if not c.startswith("leaf") and c), key=len)
check("Q1d the longest repeated substring of ABABABA is ABABA = the deepest internal node of the suffix tree",
      best == "ABABA" == deepest_internal)
finding("Q1d the official text never states the answer for T=ABABABA (it is ABABA).")

# ---------- Q2: split into B (size k) and C (size n-k) maximizing |Sum(B)-Sum(C)| ----------


def best_diff(A, k):
    n = len(A)
    best = -1
    for idx in itertools.combinations(range(n), k):
        sb = sum(A[i] for i in idx)
        best = max(best, abs(sb - (sum(A) - sb)))
    return best


def official_split(A, k):
    n = len(A)
    S = sorted(A)[k - 1]  # Select(A, n, k): the k-th smallest (distinct values)
    B, C = [], []
    if k < n - k:
        for v in A:
            (C if v > S else B).append(v)
    else:
        for v in A:
            (B if v > S else C).append(v)
    return B, C


check("Q2 example 8,4,5,2,10 with k=2: best difference 17 and the official code reaches it",
      best_diff([8, 4, 5, 2, 10], 2) == 17 and abs(sum(official_split([8, 4, 5, 2, 10], 2)[0]) - sum(official_split([8, 4, 5, 2, 10], 2)[1])) == 17)
random.seed(8)
size_bad = val_bad = 0
ex = None
for _ in range(3000):
    n = random.randint(2, 8)
    k = random.randint(1, n - 1)
    A = random.sample(range(1, 30), n)
    B, C = official_split(A, k)
    if len(B) != k or len(C) != n - k:
        size_bad += 1
    if abs(sum(B) - sum(C)) != best_diff(A, k):
        val_bad += 1
        if ex is None:
            ex = (A, k)
check("Q2 official code is optimal whenever k <= n-k", all(
    abs(sum(official_split(A, k)[0]) - sum(official_split(A, k)[1])) == best_diff(A, k)
    for A, k in [(random.sample(range(1, 30), n), kk) for n in range(2, 9) for kk in range(1, n // 2 + 1) for _ in range(40)]))
if val_bad:
    finding("Q2 official code is NOT optimal for k > n-k (%d of 3000 random cases; e.g. A=%s k=%s: best %d, code %d); "
            "its B/C sizes are also swapped in the else branch (%d cases)" %
            (val_bad, ex[0], ex[1], best_diff(*ex), abs(sum(official_split(*ex)[0]) - sum(official_split(*ex)[1])), size_bad))

# ---------- Q3: Prim from A ----------
EDGES = [("B", "C", 12), ("C", "D", 1), ("B", "J", 10), ("J", "C", 11), ("C", "A", 16), ("C", "E", 2), ("D", "E", 3),
         ("J", "A", 13), ("A", "E", 15), ("J", "H", 9), ("J", "G", 8), ("A", "G", 14), ("E", "G", 5), ("E", "F", 4),
         ("H", "G", 7), ("G", "F", 6)]
G = nx.Graph()
G.add_weighted_edges_from(EDGES)


def prim_order(G, start):
    seen = {start}
    out = []
    while len(seen) < G.number_of_nodes():
        e = min(((u, v, d["weight"]) for u in seen for v, d in G[u].items() if v not in seen), key=lambda t: t[2])
        out.append(e)
        seen.add(e[1])
    return out


order = prim_order(G, "A")
check("Q3a Prim from A inserts weights 13,8,5,2,1,4,7,10 (total 50)",
      [w for *_, w in order] == [13, 8, 5, 2, 1, 4, 7, 10] and sum(w for *_, w in order) == 50)
check("Q3a official edge sequence (A,J),(J,G),(G,E),(E,C),(C,D),(E,F),(G,H),(J,B)",
      [(u, v) for u, v, _ in order] == [("A", "J"), ("J", "G"), ("G", "E"), ("E", "C"), ("C", "D"), ("E", "F"), ("G", "H"), ("J", "B")])
check("Q3b all 16 weights distinct", len({w for *_, w in EDGES}) == 16)
mst_w = sum(d["weight"] for *_, d in nx.minimum_spanning_edges(G, data=True))
count = 0
for es in itertools.combinations(EDGES, 8):
    if sum(e[2] for e in es) != mst_w:
        continue
    H = nx.Graph()
    H.add_edges_from((u, v) for u, v, _ in es)
    if H.number_of_nodes() == 9 and nx.is_tree(H):
        count += 1
check("Q3b exactly one minimum spanning tree (brute force over all 8-edge subsets), weight 50", count == 1 and mst_w == 50)

# ---------- Q4: remove fewest elements so that max-min <= k ----------


def brute_remove(A, k):
    n = len(A)
    for r in range(n + 1):
        for keep in itertools.combinations(range(n), n - r):
            vals = [A[i] for i in keep]
            if not vals or max(vals) - min(vals) <= k:
                return r


def official_C(A, k):
    n = len(A)
    memo = {}

    def C(i, j):
        if i > j:
            return 0
        if (i, j) in memo:
            return memo[(i, j)]
        if abs(A[i] - A[j]) <= k:
            r = 0
        else:
            r = min(C(i + 1, j), C(i, j - 1)) + 1
        memo[(i, j)] = r
        return r
    return C, memo


C, _ = official_C([1, 3, 4, 9, 10, 12, 17, 20], 4)
check("Q4 example 1 -> 5", C(0, 7) == 5 == brute_remove([1, 3, 4, 9, 10, 12, 17, 20], 4))
C, _ = official_C([1, 2, 5, 6, 8], 2)
check("Q4 example 2 -> 3", C(0, 4) == 3 == brute_remove([1, 2, 5, 6, 8], 2))
random.seed(9)
bad = 0
for _ in range(1500):
    n = random.randint(1, 8)
    A = sorted(random.sample(range(1, 30), n))
    k = random.randint(0, 12)
    C, _ = official_C(A, k)
    if C(0, n - 1) != brute_remove(A, k):
        bad += 1
check("Q4a official recurrence C(1,n) equals brute force on 1500 random sorted arrays", bad == 0)
A = [1, 2, 5, 6, 8]
C, _ = official_C(A, 2)
true_tab = [[(C(i, j) if j >= i else None) for j in range(5)] for i in range(5)]
printed = [[0, 0, 1, 2, 3], [None, 0, 1, 2, 2], [None, None, 0, 0, 1], [None, None, None, 0, 1], [None, None, None, None, 0]]
diff = [(i + 1, j + 1, printed[i][j], true_tab[i][j]) for i in range(5) for j in range(5) if printed[i][j] != true_tab[i][j]]
check("Q4c printed table agrees with the recurrence except for cells %s" % diff, len(diff) == 2)
finding("Q4c printed 5x5 table has 2 wrong cells (row,col,printed,true): %s; the final answer 3 is unaffected." % diff)

print("ALL OK" if ok else "SOME CHECK FAILED")
raise SystemExit(0 if ok else 1)
