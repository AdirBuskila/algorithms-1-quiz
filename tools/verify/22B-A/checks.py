# -*- coding: utf-8 -*-
r"""Verification harness for 22B-A (algorithms-1). Run: PYTHONUTF8=1 py tools/verify/22B-A/checks.py
Checks the official answers (never modifies them). ASCII output. Findings marked FINDING are official-key problems
(they do not make the script fail; they are the evidence behind a hold / transcription note)."""
import itertools, random, math
import networkx as nx

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


def finding(name, extra=""):
    print("FINDING " + name + (" " + extra if extra else ""))


def pi_table(P):
    pi = [0] * len(P)
    k = 0
    for q in range(1, len(P)):
        while k and P[k] != P[q]:
            k = pi[k - 1]
        if P[k] == P[q]:
            k += 1
        pi[q] = k
    return pi


# ---------- Q1a / Q1b: prefix function existence ----------
check("Q1a P=abbbba has pi = 0,0,0,0,0,1", pi_table("abbbba") == [0, 0, 0, 0, 0, 1])
hits = ["".join(s) for s in itertools.product("ab", repeat=6) if pi_table("".join(s)) == [0, 0, 1, 1, 2, 1]]
check("Q1b no string over {a,b} of length 6 has pi = 0,0,1,1,2,1", hits == [])
hits3 = ["".join(s) for s in itertools.product("abc", repeat=6) if pi_table("".join(s)) == [0, 0, 1, 1, 2, 1]]
check("Q1b (extra) not even over a 3-letter alphabet", hits3 == [])

# ---------- Q1c: Huffman code a=0 b=100 c=101 d=11; b=2, d=5, c=x, a=y ----------
sol = set()
for x in range(1, 30):
    for y in range(1, 40):
        # Huffman validity (any tie-breaking): step 1 merges b,c ; step 2 merges (b,c) with d ; a is last
        step1 = max(2, x) <= min(5, y)
        step2 = max(x + 2, 5) <= y
        # left child (bit 0) not heavier than right child (bit 1) at every internal node
        orient = (y <= x + 7) and (x + 2 <= 5) and (2 <= x)
        if step1 and step2 and orient:
            sol.add((x, y))
official = {(2, y) for y in range(5, 10)} | {(3, y) for y in range(5, 11)}
check("Q1c official answer set {x=2,5<=y<=9} u {x=3,5<=y<=10} equals the brute-force set", sol == official,
      "brute=%d official=%d" % (len(sol), len(official)))


def huff_codes_tiebreaks(freq):
    """All code-length vectors reachable by Huffman with arbitrary tie-breaking."""
    out = set()

    def rec(nodes):
        if len(nodes) == 1:
            out.add(tuple(sorted(nodes[0][1].items())))
            return
        nodes = sorted(nodes, key=lambda t: t[0])
        w = [n[0] for n in nodes]
        # choose any pair that consists of two minimum-weight nodes
        m1 = w[0]
        m2 = w[1]
        for i, j in itertools.combinations(range(len(nodes)), 2):
            if sorted([w[i], w[j]]) == [m1, m2]:
                a, b = nodes[i], nodes[j]
                d = {k: v + 1 for k, v in a[1].items()}
                d.update({k: v + 1 for k, v in b[1].items()})
                rest = [nodes[t] for t in range(len(nodes)) if t not in (i, j)]
                rec(rest + [(a[0] + b[0], d)])
    rec([(f, {s: 0}) for s, f in freq.items()])
    return out


for x, y in sorted(official):
    lens = huff_codes_tiebreaks({"a": y, "b": 2, "c": x, "d": 5})
    want = tuple(sorted({"a": 1, "b": 3, "c": 3, "d": 2}.items()))
    if want not in lens:
        check("Q1c (x=%d,y=%d) cannot give the printed code lengths" % (x, y), False)
check("Q1c every official (x,y) yields code lengths a1 b3 c3 d2 for some Huffman tie-breaking", True)

# ---------- Q1d: Print_lines ----------


def print_lines(n, cnt):
    if n > 1:
        cnt[0] += 1
        print_lines(n // 2, cnt)
        print_lines(n // 2, cnt)


good = True
for k in range(0, 14):
    c = [0]
    print_lines(2 ** k, c)
    good &= c[0] == 2 ** k - 1
check("Q1d Print_lines(2^k) prints 2^k-1 lines: T(n)=2T(n/2)+O(1)=Theta(n); exponential in the bit length of n", good)

# ---------- Q2: consecutive pair with total count >= ceil(n/2) ----------


def truth(A):
    n = len(A)
    cnt = {}
    for v in A:
        cnt[v] = cnt.get(v, 0) + 1
    vals = sorted(cnt)
    need = -(-n // 2)
    return any(cnt[vals[i]] + cnt[vals[i + 1]] >= need for i in range(len(vals) - 1))


def official_code(A, strict_real=True):
    """The official pseudo-code with its loop bugs removed but its conditions kept literally."""
    n = len(A)
    M = sorted(A)[(n + 1) // 2 - 1]
    cm = A.count(M)
    if -(-n // 2) <= cm < n:
        return True
    lows = [v for v in A if v < M]
    if lows:
        L = max(lows)
        if cm + A.count(L) > (n / 2 if strict_real else n // 2):
            return True
    highs = [v for v in A if v > M]
    if highs:
        R = min(highs)
        if cm + A.count(R) > (n / 2 if strict_real else n // 2):
            return True
    return False


def fixed_code(A):
    n = len(A)
    M = sorted(A)[(n + 1) // 2 - 1]
    cm = A.count(M)
    need = -(-n // 2)
    if need <= cm < n:
        return True
    lows = [v for v in A if v < M]
    highs = [v for v in A if v > M]
    if lows and cm + A.count(max(lows)) >= need:
        return True
    if highs and cm + A.count(min(highs)) >= need:
        return True
    return False


bad_off, bad_fix, odd_bad, ex = 0, 0, 0, None
for n in range(1, 9):
    for A in itertools.product(range(1, 5), repeat=n):
        A = list(A)
        t = truth(A)
        if official_code(A) != t:
            bad_off += 1
            if n % 2:
                odd_bad += 1
            if ex is None and n % 2 == 0:
                ex = A
        if fixed_code(A) != t:
            bad_fix += 1
check("Q2 idea (test the median and its two neighbours with >= ceil(n/2)) equals brute force for all arrays n<=8 over 1..4", bad_fix == 0,
      "mismatches=%d" % bad_fix)
check("Q2 official code is right for every ODD n tested", odd_bad == 0)
if bad_off:
    finding("Q2 official code (strict '>' n/2) disagrees with brute force on %d arrays, all with even n; e.g. A=%s truth=%s code=%s" %
            (bad_off, ex, truth(ex), official_code(ex)))

# ---------- Q3: bottleneck spanning trees ----------
G = nx.Graph()
G.add_weighted_edges_from([("T", "L", 2), ("T", "R", 1), ("L", "R", 2)])
trees = []
for es in itertools.combinations(G.edges(data="weight"), 2):
    H = nx.Graph()
    H.add_weighted_edges_from(es)
    if nx.is_tree(H) and H.number_of_nodes() == 3:
        trees.append((sum(w for *_, w in es), max(w for *_, w in es), sorted(tuple(sorted(e[:2])) for e in es)))
minbn = min(t[1] for t in trees)
minw = min(t[0] for t in trees)
mbst_not_mst = [t for t in trees if t[1] == minbn and t[0] != minw]
check("Q3a triangle (1,2,2): MST weight 3 bottleneck 2; the tree {TL,LR} is an MBST (bottleneck 2) of weight 4, not an MST",
      minw == 3 and minbn == 2 and len(mbst_not_mst) == 1 and mbst_not_mst[0][0] == 4)

random.seed(2)
bad = 0
for _ in range(300):
    n = random.randint(3, 6)
    G = nx.gnp_random_graph(n, 0.7, seed=random.randint(0, 10 ** 6))
    if not nx.is_connected(G):
        continue
    for u, v in G.edges():
        G[u][v]["weight"] = random.randint(1, 4)
    best_bn = None
    sts = []
    for es in itertools.combinations(G.edges(data="weight"), n - 1):
        H = nx.Graph()
        H.add_nodes_from(G.nodes())
        H.add_weighted_edges_from(es)
        if nx.is_connected(H):
            sts.append((sum(w for *_, w in es), max(w for *_, w in es)))
    mw = min(s[0] for s in sts)
    mb = min(s[1] for s in sts)
    if any(s[0] == mw and s[1] != mb for s in sts):
        bad += 1
check("Q3b every MST is an MBST on 300 random weighted graphs (all spanning trees enumerated)", bad == 0)

# ---------- Q4: count occurrences of P in T as a subsequence ----------


def count_dp(T, P):
    C = [[0] * (len(P) + 1) for _ in range(len(T) + 1)]
    for i in range(len(T) + 1):
        C[i][0] = 1
    for i in range(1, len(T) + 1):
        for j in range(1, len(P) + 1):
            if j > i:
                C[i][j] = 0
            elif T[i - 1] != P[j - 1]:
                C[i][j] = C[i - 1][j]
            else:
                C[i][j] = C[i - 1][j - 1] + C[i - 1][j]
    return C


def count_brute(T, P):
    return sum(1 for idx in itertools.combinations(range(len(T)), len(P)) if all(T[i] == c for i, c in zip(idx, P)))


check("Q4a example subsequence/see -> 6", count_dp("subsequence", "see")[-1][-1] == 6 == count_brute("subsequence", "see"))
random.seed(4)
bad = 0
for _ in range(1500):
    T = "".join(random.choice("abc") for _ in range(random.randint(0, 9)))
    P = "".join(random.choice("abc") for _ in range(random.randint(0, 4)))
    if count_dp(T, P)[-1][-1] != count_brute(T, P):
        bad += 1
check("Q4a official recurrence equals brute force on 1500 random pairs", bad == 0)
C = count_dp("abcbac", "abc")
printed = [[1, 0, 0], [1, 1, 0], [1, 1, 1], [1, 2, 1], [2, 2, 1], [2, 2, 3]]
check("Q4c printed 6x3 table for T=abcbac, P=abc matches the recurrence cell by cell", [r[1:] for r in C[1:]] == printed)

print("ALL OK" if ok else "SOME CHECK FAILED")
raise SystemExit(0 if ok else 1)
