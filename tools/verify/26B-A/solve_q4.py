# -*- coding: utf-8 -*-
"""Solver checks for 26B-A Q4 (Huffman reverse, MST with unknown X, Prim from C, prefix function, sqrt(n) smallest).
Run: PYTHONUTF8=1 py tools/verify/26B-A/solve_q4.py   (ASCII output)"""
import heapq, itertools, json, math, pathlib, random
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


# ---- Q4a(i): the code is a full binary tree -> the only free leaf is 10
codes = {"a": "0", "b": "1100", "c": "1101", "d": "111", "e": "10"}
words = list(codes.values())
check("Q4a(i) e=10 keeps the code prefix-free", all(not y.startswith(x) for x in words for y in words if x != y))
check("Q4a(i) Kraft sum = 1 (full tree)", sum(2 ** -len(w) for w in words) == 1)
for cand in ["10", "100", "101", "1000"]:
    ws = [w for k, w in codes.items() if k != "e"] + [cand]
    full = sum(2 ** -len(w) for w in ws) == 1
    pf = all(not y.startswith(x) for x in ws for y in ws if x != y)
    print("INFO  e=%s prefix-free=%s full=%s" % (cand, pf, full))


# ---- Q4a(ii): which f(e) let Huffman (with the sibling rule left<=right) produce exactly this code?
def huffman_codes_all(freq):
    """Every code Huffman can output when ties are broken in any way; children ordered left<=right
    (when the two merged weights are equal both left/right placements are allowed)."""
    results = set()

    def rec(nodes):
        if len(nodes) == 1:
            out = {}

            def walk(t, p):
                if isinstance(t[1], str):
                    out[t[1]] = p
                else:
                    walk(t[1], p + "0")
                    walk(t[2], p + "1")
            walk(nodes[0], "")
            results.add(tuple(sorted(out.items())))
            return
        ws = sorted(set(x[0] for x in nodes))
        idx = range(len(nodes))
        for i, j in itertools.permutations(idx, 2):
            x, y = nodes[i], nodes[j]
            # x, y must be two minimum-weight nodes; x goes left, y right, need w(x) <= w(y)
            others = [nodes[k][0] for k in idx if k not in (i, j)]
            if x[0] > y[0] or (others and max(x[0], y[0]) > min(others)):
                continue
            rest = [nodes[k] for k in idx if k not in (i, j)]
            rec(rest + [(x[0] + y[0], x, y)])

    rec([(f, ch) for ch, f in freq.items()])
    return results


target = tuple(sorted(codes.items()))
good = [fe for fe in range(1, 30) if target in huffman_codes_all({"a": 13, "b": 1, "c": 2, "d": 4, "e": fe})]
print("FACT  f(e) values for which Huffman can output the given code:", good)
check("Q4a(ii) possible f(e) are exactly 6 and 7", good == [6, 7])

# ---- Q4b: graph with unknown X on D-F
g = json.load(open(HERE / "graphs.json"))["26B-A-Q4b"]


def graph(X):
    G = nx.Graph()
    for e in g["edges"]:
        G.add_edge(e["u"], e["v"], weight=X if e["w"] is None else e["w"])
    return G


def all_msts(G):
    n = G.number_of_nodes()
    best, trees = None, []
    E = list(G.edges(data="weight"))
    for es in itertools.combinations(E, n - 1):
        H = nx.Graph([(a, b) for a, b, _ in es])
        if H.number_of_nodes() == n and nx.is_connected(H):
            w = sum(x for _, _, x in es)
            k = frozenset(frozenset((a, b)) for a, b, _ in es)
            if best is None or w < best:
                best, trees = w, [k]
            elif w == best:
                trees.append(k)
    return best, trees


DF = frozenset(("D", "F"))
in_all = {X: all(DF in t for t in all_msts(graph(X))[1]) for X in range(0, 8)}
print("FACT  X -> D-F in every MST:", in_all)
check("Q4b(i) largest integer X with D-F in every MST is 3",
      max(X for X, v in in_all.items() if v) == 3 and all(in_all[X] for X in range(0, 4)))
w3, trees3 = all_msts(graph(3))
print("FACT  X=3: MST weight", w3, "number of MSTs", len(trees3))
for t in trees3:
    print("      ", sorted("".join(sorted(e)) for e in t))


# Prim from C with every tie-breaking: list all possible insertion orders
def prim_orders(G, r):
    res = []

    def rec(inT, seq):
        if len(inT) == G.number_of_nodes():
            res.append(seq)
            return
        cand = [(G[a][b]["weight"], a, b) for a in inT for b in G[a] if b not in inT]
        m = min(c[0] for c in cand)
        for w, a, b in cand:
            if w == m:
                rec(inT | {b}, seq + [(a, b)])
    rec({r}, [])
    return res


orders = prim_orders(graph(3), "C")
uniq = sorted(set(tuple(o) for o in orders))
print("FACT  X=3: Prim from C, distinct edge orders over all tie-breaks:", len(uniq))
for o in uniq:
    print("      ", " ".join("(%s,%s)" % e for e in o))
check("Q4b(ii) Prim order is NOT unique for X=3 (ties C-B/D-F at 3 and D-E/F-H at 4)", len(uniq) > 1)


# ---- Q4c(i) prefix function
def pi_fn(P):
    pi = [0] * len(P)
    k = 0
    for i in range(1, len(P)):
        while k and P[i] != P[k]:
            k = pi[k - 1]
        if P[i] == P[k]:
            k += 1
        pi[i] = k
    return pi


def pi_brute(P):
    return [max(k for k in range(i + 1) if P[:k] == P[i + 1 - k:i + 1] and k <= i) for i in range(len(P))]


P = "AABAABAABAAA"
check("Q4c(i) pi(AABAABAABAAA) = 0,1,0,1,2,3,4,5,6,7,8,2",
      pi_fn(P) == pi_brute(P) == [0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 2])


# ---- Q4c(ii) select-based: k-th smallest by quickselect, partition, sort the k
def select(A, k):  # k-th smallest, 1-based (randomized; Select median-of-medians gives worst case O(n))
    p = random.choice(A)
    L = [x for x in A if x < p]
    E = [x for x in A if x == p]
    if k <= len(L):
        return select(L, k)
    if k <= len(L) + len(E):
        return p
    return select([x for x in A if x > p], k - len(L) - len(E))


def smallest_sqrt(A):
    k = math.isqrt(len(A))
    if k == 0:
        return []
    x = select(A, k)
    less = [y for y in A if y < x]
    return sorted(less + [x] * (k - len(less)))


bad = 0
for _ in range(3000):
    n = random.randint(0, 60)
    A = [random.randint(-20, 20) for _ in range(n)]
    if smallest_sqrt(A) != sorted(A)[:math.isqrt(n)]:
        bad += 1
check("Q4c(ii) select + partition + sort == sorted(A)[:floor(sqrt n)] (3000 random arrays, duplicates)", bad == 0)

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
