# -*- coding: utf-8 -*-
"""Verification harness for 24A-C (algorithms-1). Run: PYTHONUTF8=1 py tools/verify/24A-C/checks.py
Checks the official answers (never modifies them). ASCII output."""
import heapq, random, itertools, json, pathlib
from collections import deque
import networkx as nx

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


random.seed(7)

# ---------- Q1: cut vertex via BFS on G-x from one neighbour ----------
def is_cut_vertex(adj, x):
    nb = adj[x]
    if len(nb) <= 1:
        return False
    v = nb[0]
    seen = {v}
    dq = deque([v])
    while dq:
        a = dq.popleft()
        for b in adj[a]:
            if b != x and b not in seen:
                seen.add(b)
                dq.append(b)
    return any(u not in seen for u in nb)


bad = 0
for _ in range(3000):
    n = random.randint(1, 9)
    G = nx.gnp_random_graph(n, random.random() * 0.6, seed=random.randint(0, 10**6))
    adj = {u: list(G[u]) for u in G}
    arts = set(nx.articulation_points(G))
    for x in G:
        if is_cut_vertex(adj, x) != (x in arts):
            bad += 1
check("Q1 official cut-vertex algorithm == networkx articulation_points (3000 graphs, incl. disconnected)", bad == 0)

# ---------- Q2: 0-1 knapsack when values are non-increasing in weight order -> take lightest items ----------
def greedy(w, v, S):
    G, i = [], 0
    while i < len(w) and S >= w[i]:
        G.append(i)
        S -= w[i]
        i += 1
    return G


def brute(w, v, S):
    best = 0
    for mask in range(1 << len(w)):
        sw = sum(w[i] for i in range(len(w)) if mask >> i & 1)
        if sw <= S:
            best = max(best, sum(v[i] for i in range(len(w)) if mask >> i & 1))
    return best


bad = 0
for _ in range(4000):
    n = random.randint(1, 9)
    w = sorted(random.randint(1, 12) for _ in range(n))
    v = sorted((random.randint(1, 15) for _ in range(n)), reverse=True)
    S = random.randint(0, 40)
    if sum(v[i] for i in greedy(w, v, S)) != brute(w, v, S):
        bad += 1
check("Q2a greedy (lightest first) value == brute-force optimum, values non-increasing (4000 inputs)", bad == 0)
check("Q2 example weights 1,4,5,7,10 values 8,6,5,4,2: greedy is a prefix", greedy([1, 4, 5, 7, 10], [8, 6, 5, 4, 2], 10) == [0, 1, 2])

# ---------- Q3: Huffman ----------
def huff_lengths(freqs):
    h = [(f, i, [i]) for i, f in enumerate(freqs)]
    heapq.heapify(h)
    L = [0] * len(freqs)
    c = len(freqs)
    while len(h) > 1:
        f1, _, s1 = heapq.heappop(h)
        f2, _, s2 = heapq.heappop(h)
        for i in s1 + s2:
            L[i] += 1
        heapq.heappush(h, (f1 + f2, c, s1 + s2))
        c += 1
    return L


def huff_cost(freqs):
    return sum(f * l for f, l in zip(freqs, huff_lengths(freqs)))


code = {"a1": "00", "a2": "11", "a3": "01", "a4": "100", "a5": "101"}
freq = {"a1": 3, "a2": 4, "a3": 3, "a4": 1, "a5": 2}
prefix_free = not any(a != b and code[b].startswith(code[a]) for a in code for b in code)
kraft = sum(2.0 ** -len(c) for c in code.values())
check("Q3a code is prefix-free and complete (Kraft sum 1)", prefix_free and abs(kraft - 1) < 1e-12)
cost = sum(freq[k] * len(code[k]) for k in code)
check("Q3a official frequencies give the code's cost = optimal Huffman cost", cost == huff_cost(list(freq.values())), f"(cost {cost})")
# the printed tree: 13 -> 6 (a1 3, a3 3) and 7 (3 (a4 1, a5 2), a2 4)
check("Q3a internal node weights of the printed tree: 3, 6, 7, 13", 1 + 2 == 3 and 3 + 3 == 6 and 3 + 4 == 7 and 6 + 7 == 13)
# Is there any frequency vector at all (small range) with exactly these code lengths as an optimal code? yes, the official one
check("Q3a code lengths (2,2,2,3,3) are optimal for the official frequencies", sorted(len(c) for c in code.values()) == sorted(huff_lengths(list(freq.values()))))

# Q3b geometric 1,3,9,27,81: chain tree, depths of a1..a5 = 4,4,3,2,1; cost
f3 = [1, 3, 9, 27, 81]
check("Q3b code lengths for 1,3,9,27,81 are 4,4,3,2,1", huff_lengths(f3) == [4, 4, 3, 2, 1])
check("Q3b internal weights 4, 13, 40, 121", [sum(f3[:k]) for k in range(2, 6)] == [4, 13, 40, 121])
# Q3c: every geometric sequence of 5 terms with integer ratio q>=2 gives the chain; q=1 does not
chain = [4, 4, 3, 2, 1]
all_chain = all(huff_lengths([q ** i for i in range(5)]) == chain for q in range(2, 12))
check("Q3c ratio q=2..11 gives the same chain tree", all_chain)
check("Q3c ratio q=1 (all equal) gives a different tree", sorted(huff_lengths([1] * 5)) == [2, 2, 2, 3, 3] and huff_lengths([1] * 5) != chain)
# also non-integer ratios
diff = [q for q in (1.1, 1.3, 1.5, 1.6, 1.7, 1.9) if sorted(huff_lengths([q ** i for i in range(5)]), reverse=True) != [4, 4, 3, 2, 1]]
check("Q3c some ratios in (1,2) also break the chain (side note)", len(diff) > 0, f"{diff}")

# ---------- Q4: jumping game ----------
def min_jumps_bfs(A):
    n = len(A)
    dist = [None] * (n + 1)
    dist[1] = 0
    dq = deque([1])
    while dq:
        i = dq.popleft()
        for j in range(1, A[i - 1] + 1):
            if i + j <= n and dist[i + j] is None:
                dist[i + j] = dist[i] + 1
                dq.append(i + j)
    return dist[n]


def rec_forward(A):  # C(i)=0 if i=n else 1+min_{1<=j<=min(A[i],n-i)} C(i+j)
    n = len(A)
    INF = 10 ** 9
    C = [INF] * (n + 2)
    C[n] = 0
    for i in range(n - 1, 0, -1):
        m = min(A[i - 1], n - i)
        if m >= 1:
            C[i] = 1 + min(C[i + j] for j in range(1, m + 1))
    return C[1]


def rec_backward(A):  # C(i)=0 if i=1 else 1+min_{1<=j<i, j+A[j]>=i} C(j)
    n = len(A)
    INF = 10 ** 9
    C = [INF] * (n + 1)
    C[1] = 0
    for i in range(2, n + 1):
        c = [C[j] for j in range(1, i) if j + A[j - 1] >= i]
        if c:
            C[i] = 1 + min(c)
    return C[n]


ex = [1, 4, 6, 4, 5, 3, 3, 2, 1, 3]
check("Q4 example array gives 3 jumps by BFS and both recurrences", min_jumps_bfs(ex) == rec_forward(ex) == rec_backward(ex) == 3)
bad = 0
for _ in range(5000):
    n = random.randint(1, 9)
    A = [random.randint(1, 5) for _ in range(n)]  # A[i] >= 1 so the end is reachable
    b = min_jumps_bfs(A)
    if not (b == rec_forward(A) == rec_backward(A)):
        bad += 1
check("Q4a both official recurrences == BFS optimum (5000 random arrays, A[i]>=1)", bad == 0)

# ---------- Bonus: Prim from C, can the weights come in the order 8,9,9,8,11,12,13 ----------
E = [("L", "TL", 12), ("TL", "TM", 9), ("TM", "TR", 11), ("TM", "C", 8), ("TR", "BR", 13),
     ("C", "BL", 10), ("C", "BM", 9), ("BL", "BM", 8), ("BM", "BR", 13), ("L", "BL", 15)]
G = nx.Graph()
for u, v, w in E:
    G.add_edge(u, v, weight=w)
mst_w = sum(d["weight"] for _, _, d in nx.minimum_spanning_edges(G, data=True))
orders = set()


def prim_all(visited, seq):
    if len(visited) == len(G):
        orders.add(tuple(seq))
        return
    cands = [(d["weight"], u, v) for u in visited for v, d in G[u].items() if v not in visited]
    mn = min(c[0] for c in cands)
    for w, u, v in cands:
        if w == mn:
            prim_all(visited | {v}, seq + [w])


prim_all({"C"}, [])
check("Bonus MST weight = 8+9+9+8+11+12+13 = 70", mst_w == 70 and sum([8, 9, 9, 8, 11, 12, 13]) == 70)
check("Bonus Prim from C can add edges in weight order 8,9,9,8,11,12,13 (some tie-break)", (8, 9, 9, 8, 11, 12, 13) in orders, f"({len(orders)} possible orders)")

json.dump({"24A-C-Qb": {"directed": False, "note": "Bonus graph (Prim from C); distinct names for the unlabelled vertices",
                        "vertices": list(G.nodes), "edges": [{"u": u, "v": v, "w": w} for u, v, w in E],
                        "mst": [list(e[:2]) for e in nx.minimum_spanning_edges(G, data=False)]}},
          open(pathlib.Path(__file__).resolve().parent / "graphs_generated_check.json", "w"))
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
