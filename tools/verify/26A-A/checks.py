# -*- coding: utf-8 -*-
"""Verification harness for 26A-A (algorithms-1). Run: PYTHONUTF8=1 py tools/verify/26A-A/checks.py
Checks the official answers (never modifies them). ASCII output."""
import itertools, heapq, random, json, pathlib
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


# ---------- Q1: tasks with no two consecutive skips ----------
def brute_tasks(A):
    n = len(A)
    best = None
    for mask in range(1 << n):  # bit i set = task i performed
        if any(not (mask >> i & 1) and not (mask >> (i + 1) & 1) for i in range(n - 1)):
            continue
        s = sum(A[i] for i in range(n) if mask >> i & 1)
        best = s if best is None or s < best else best
    return best


def dp_one(A):  # T(i)=A[i]+min(T(i-1),T(i-2)); answer min(T(n-1),T(n-2))
    n = len(A)
    T = {}

    def t(i):
        return 0 if i < 0 else T[i]
    for i in range(n):
        T[i] = A[i] + min(t(i - 1), t(i - 2))
    return min(t(n - 1), t(n - 2))


def dp_two(A):  # T(i,c): c=1 may skip i, c=0 must perform i
    n = len(A)

    def T(i, c):
        if i < 0:
            return 0
        if c == 0:
            return A[i] + T(i - 1, 1)
        return min(A[i] + T(i - 1, 1), T(i - 1, 0))
    return T(n - 1, 1)


check("Q1a A=[10] -> 0", dp_one([10]) == 0 and dp_two([10]) == 0 and brute_tasks([10]) == 0)
check("Q1 ex1 -> 12", brute_tasks([10, 5, 7, 10]) == 12 == dp_one([10, 5, 7, 10]) == dp_two([10, 5, 7, 10]))
ex2 = [10, 5, 2, 4, 8, 6, 7, 10]
check("Q1 ex2 -> 22", brute_tasks(ex2) == 22 == dp_one(ex2) == dp_two(ex2))
random.seed(1)
bad = 0
for _ in range(3000):
    A = [random.randint(1, 20) for _ in range(random.randint(1, 10))]
    b = brute_tasks(A)
    if not (b == dp_one(A) == dp_two(A)):
        bad += 1
check("Q1b both recurrences vs brute force (3000 random)", bad == 0, "mismatches=%d" % bad)

# ---------- Q2: MST special edges ----------
G = nx.Graph()
for u, v, w in [("A", "B", 1), ("C", "D", 2), ("B", "C", 3), ("A", "C", 4), ("B", "D", 5), ("A", "D", 6)]:
    G.add_edge(u, v, weight=w)
mst = nx.minimum_spanning_tree(G)
check("Q2a K4 MST = {AB,CD,BC}",
      {frozenset(e) for e in mst.edges()} == {frozenset("AB"), frozenset("CD"), frozenset("BC")})


def special(G, e):
    u, v = e
    w = G[u][v]["weight"]

    def smallest(x):
        return min(d["weight"] for _, _, d in G.edges(x, data=True))
    return w == smallest(u) or w == smallest(v)


check("Q2a BC in MST but not special",
      frozenset("BC") in {frozenset(e) for e in mst.edges()} and not special(G, ("B", "C")))
bad = 0
cnt = 0
random.seed(2)
for _ in range(400):
    n = random.randint(3, 7)
    ws = random.sample(range(1, 200), n * (n - 1) // 2)
    H = nx.Graph()
    for (u, v), w in zip(itertools.combinations(range(n), 2), ws):
        H.add_edge(u, v, weight=w)
    M = {frozenset(e) for e in nx.minimum_spanning_tree(H).edges()}
    for u, v in H.edges():
        if special(H, (u, v)):
            cnt += 1
            if frozenset((u, v)) not in M:
                bad += 1
check("Q2b special => in the (unique) MST, random complete graphs", bad == 0 and cnt > 0,
      "special edges tested=%d bad=%d" % (cnt, bad))

# ---------- Q3a: Huffman ----------
freq = {"a": 22, "b": 15, "c": 3, "d": 24, "e": 4, "f": 10, "g": 8}
code = {"a": "01", "b": "111", "c": "0000", "d": "10", "e": "0001", "f": "110", "g": "001"}


def huff_cost(fs):
    h = list(fs)
    heapq.heapify(h)
    c = 0
    while len(h) > 1:
        x = heapq.heappop(h)
        y = heapq.heappop(h)
        c += x + y
        heapq.heappush(h, x + y)
    return c


cost = sum(freq[k] * len(code[k]) for k in freq)
check("Q3a official code cost == optimal Huffman cost", cost == huff_cost(freq.values()), "cost=%d" % cost)
check("Q3a prefix-free, Kraft sum = 1",
      not any(a != b and code[b].startswith(code[a]) for a in code for b in code)
      and sum(2.0 ** -len(c) for c in code.values()) == 1.0)
check("Q3a total frequency 86, internal sums 7+15+25+37+49+86 == cost",
      sum(freq.values()) == 86 and 7 + 15 + 25 + 37 + 49 + 86 == cost)
g = json.load(open(HERE / "graphs.json"))["26A-A-Q3a"]
D = nx.DiGraph()
for e in g["edges"]:
    D.add_edge(e["u"], e["v"], bit=e["w"])
dec = {}
for n in D:
    if D.out_degree(n) == 0:
        path = nx.shortest_path(D, "86", n)
        dec[n[0]] = "".join(str(D[a][b]["bit"]) for a, b in zip(path, path[1:]))
check("Q3a graphs.json tree reproduces the code table", dec == code)


# ---------- Q3b: weights 2^(h-d) make T a Huffman tree ----------
def rand_full_tree(n):
    leaves = [0]
    while len(leaves) < n:
        d = leaves.pop(random.randrange(len(leaves)))
        leaves += [d + 1, d + 1]
    return leaves


bad = 0
random.seed(3)
for _ in range(2000):
    n = random.randint(2, 12)
    dep = rand_full_tree(n)
    h = max(dep)
    fs = [2 ** (h - d) for d in dep]
    tc = sum(f * d for f, d in zip(fs, dep))
    if tc != huff_cost(fs):
        bad += 1
check("Q3b freq 2^(h-d): T cost == optimal Huffman cost (2000 random trees)", bad == 0, "bad=%d" % bad)


# ---------- Q4: k-th missing positive ----------
def kth_brute(A, k):
    s = set(A)
    x = 0
    while k:
        x += 1
        if x not in s:
            k -= 1
    return x


def kth_official(A, k):
    low, high = 0, len(A) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if A[mid] - (mid + 1) < k:
            low = mid + 1
        else:
            high = mid - 1
    return low + k


check("Q4 ex [2,3,4,7,11] k=5 -> 9", kth_official([2, 3, 4, 7, 11], 5) == 9 == kth_brute([2, 3, 4, 7, 11], 5))
check("Q4a [3,5,9,10,11,12] k=2 -> 2", kth_official([3, 5, 9, 10, 11, 12], 2) == 2 == kth_brute([3, 5, 9, 10, 11, 12], 2))
check("Q4 main() [3,5,9,10,11,12] k=3 -> 4", kth_official([3, 5, 9, 10, 11, 12], 3) == 4)
bad = 0
for _ in range(5000):
    A = sorted(random.sample(range(1, 40), random.randint(1, 12)))
    k = random.randint(1, 30)
    if kth_official(A, k) != kth_brute(A, k):
        bad += 1
check("Q4b official binary search vs brute force (5000 random)", bad == 0, "bad=%d" % bad)


# ---------- Bonus: KMP ----------
def pi_table(P):
    pi = [0] * len(P)
    k = 0
    for i in range(1, len(P)):
        while k and P[i] != P[k]:
            k = pi[k - 1]
        if P[i] == P[k]:
            k += 1
        pi[i] = k
    return pi


check("Bonus1 pi(ABB) all zeros but B repeats (claim false)", pi_table("ABB") == [0, 0, 0] and "ABB".count("B") == 2)
bad = 0
for n in range(1, 9):
    for P in map("".join, itertools.product("ab", repeat=n)):
        if (all(x == 0 for x in pi_table(P))) != (P[0] not in P[1:]):
            bad += 1
check("Bonus1 true statement: pi all zeros <=> first letter never repeats (a,b strings n<=8)", bad == 0)


def kmp_fallbacks(P, T):
    pi = pi_table(P)
    q = 0
    falls = 0
    for ch in T:
        while q and P[q] != ch:
            q = pi[q - 1]
            falls += 1
        if P[q] == ch:
            q += 1
        if q == len(P):
            q = pi[q - 1]
    return falls


for m in (6, 20, 100):
    f = kmp_fallbacks("a" * m, "a" * (m - 1) + "b" + "a" * m)
    check("Bonus2 P=a^%d: fall-back loop runs %d >= m-1 times on one text char (Theta(m) possible)" % (m, f),
          f >= m - 1)


def naive_cmps(P, T):
    c = 0
    for s in range(len(T) - len(P) + 1):
        for j in range(len(P)):
            c += 1
            if P[j] != T[s + j]:
                break
    return c


for n, m in ((100, 7), (300, 20)):
    c = naive_cmps("a" * (m - 1) + "b", "a" * (n - 1) + "b")
    check("Bonus3 naive n=%d m=%d: %d comparisons == (n-m+1)*m (Theta(nm), not linear)" % (n, m, c),
          c == (n - m + 1) * m)
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
