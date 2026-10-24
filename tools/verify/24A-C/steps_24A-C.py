# -*- coding: utf-8 -*-
"""Step-value checks for 24A-C (algorithms-1). Run: PYTHONUTF8=1 py -I tools/verify/24A-C/steps_24A-C.py
Recomputes every numeric / trace / complexity answer used in the guided steps (and shows that every choice-distractor
fails on some input), then binds the results to tools/raw/24A-C.json. ASCII output."""
import itertools, json, pathlib, random, heapq
from collections import deque
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.loads((HERE.parents[1] / "raw" / "24A-C.json").read_text(encoding="utf-8"))
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


def item(num, part=""):
    for q in RAW["questions"]:
        if q["num"] == num and q.get("part", "") == part:
            return q
    raise KeyError((num, part))


def step(num, part, idx):
    return item(num, part)["steps"][idx]


def bind_numeric(num, part, idx, expected, label):
    s = step(num, part, idx)
    check(f"bind {label}: numeric step {idx} answer == recomputed {expected}", s["type"] == "numeric" and s["answer"] == expected)


def bind_choice(num, part, idx, text, label):
    s = step(num, part, idx)
    got = [o["value"] for o in s["options"] if o["id"] == s["correctId"]]
    check(f"bind {label}: choice step {idx} correct option text", s["type"] == "choice" and got == [text], got)


def bind_text(num, part, idx, expected, label):
    s = step(num, part, idx)
    check(f"bind {label}: text step {idx} accepts {expected}", s["type"] == "text" and expected in s["accept"])


random.seed(11)

# ============================== Q1: cut vertex ==============================
def bfs_reach(adj, start, banned):
    seen = {start}
    dq = deque([start])
    while dq:
        a = dq.popleft()
        for b in adj[a]:
            if b != banned and b not in seen:
                seen.add(b)
                dq.append(b)
    return seen


def official(adj, x):
    nb = adj[x]
    if len(nb) <= 1:
        return False
    seen = bfs_reach(adj, nb[0], x)
    return any(u not in seen for u in nb)


def var_bfs_in_G(adj, x):          # BFS in G (x kept) from a neighbour: always reaches every neighbour
    nb = adj[x]
    if len(nb) <= 1:
        return False
    seen = bfs_reach(adj, nb[0], None)
    return any(u not in seen for u in nb)


def var_arbitrary_start(adj, x):   # BFS in G-x from an arbitrary other vertex w
    nb = adj[x]
    if len(nb) <= 1:
        return False
    others = [u for u in adj if u != x]
    w = others[0]
    seen = bfs_reach(adj, w, x)
    return any(u not in seen for u in nb)


def var_any_unreached(adj, x):     # any vertex of G-x not reached from v
    nb = adj[x]
    if len(nb) <= 1:
        return False
    seen = bfs_reach(adj, nb[0], x)
    return any(u not in seen for u in adj if u != x)


def var_others_unreached(adj, x):  # cut only if ALL other neighbours are unreached
    nb = adj[x]
    if len(nb) <= 1:
        return False
    seen = bfs_reach(adj, nb[0], x)
    return all(u not in seen for u in nb[1:])


def var_deg2(adj, x):
    return len(adj[x]) >= 2


def comps(G):
    return nx.number_connected_components(G)


def var_Gx_disconnected(adj, x):
    G = nx.Graph()
    G.add_nodes_from(adj)
    for u in adj:
        for v in adj[u]:
            G.add_edge(u, v)
    H = G.copy()
    H.remove_node(x)
    return H.number_of_nodes() > 0 and not nx.is_connected(H)


def var_no_cycle(adj, x):
    G = nx.Graph()
    G.add_nodes_from(adj)
    for u in adj:
        for v in adj[u]:
            G.add_edge(u, v)
    on_cycle = any(x in c and len(c) >= 3 for c in nx.biconnected_components(G))
    return not on_cycle


def pair_cond(adj, x):             # two neighbours in different components of G-x
    nb = adj[x]
    cs = {}
    seen_all = set()
    for u in nb:
        if u in seen_all:
            continue
        r = bfs_reach(adj, u, x)
        seen_all |= r
        cs[u] = r
    return len(cs) >= 2


def rand_graphs(count):
    for _ in range(count):
        n = random.randint(1, 8)
        G = nx.gnp_random_graph(n, random.random() * 0.6, seed=random.randint(0, 10 ** 6))
        yield G, {u: list(G[u]) for u in G}


good = {"official": 0, "pair": 0}
broken = {f: 0 for f in (var_bfs_in_G, var_arbitrary_start, var_any_unreached, var_others_unreached, var_deg2, var_Gx_disconnected, var_no_cycle)}
for G, adj in rand_graphs(4000):
    arts = set(nx.articulation_points(G))
    for x in G:
        t = x in arts
        good["official"] += official(adj, x) != t
        good["pair"] += pair_cond(adj, x) != t
        for f in broken:
            broken[f] += f(adj, x) != t
check("Q1 official algorithm == articulation points (4000 graphs)", good["official"] == 0)
check("Q1b 'two neighbours of x in different components of G-x' == articulation points", good["pair"] == 0)
for f, c in broken.items():
    check(f"Q1 distractor {f.__name__} is wrong on some input", c > 0, f"(wrong {c} times)")

G1 = {"nodes": ["1", "2", "3", "4", "5", "6"],
      "edges": [("1", "2"), ("2", "3"), ("3", "4"), ("4", "2"), ("4", "5"), ("5", "6")]}
g = nx.Graph(G1["edges"])
adj1 = {u: list(g[u]) for u in g}
cnt = sum(official(adj1, x) for x in g)
check("Q1a example graph: official algorithm marks vertices 2,4,5 (3 cut vertices)",
      {x for x in g if official(adj1, x)} == {"2", "4", "5"} == set(nx.articulation_points(g)) and cnt == 3)
bind_numeric(1, "א", 2, cnt, "Q1a")

# operation count: BFS in G-x touches each vertex once and each adjacency entry once, the loop touches deg(x) entries
worst = 0
for G, adj in rand_graphs(500):
    E = G.number_of_edges()
    V = G.number_of_nodes()
    for x in G:
        if len(adj[x]) <= 1:
            continue
        seen = bfs_reach(adj, adj[x][0], x)
        ops = len(seen) + sum(len(adj[u]) for u in seen) + len(adj[x])
        worst = max(worst, ops - (V + 2 * E))
check("Q1c operation count <= V + 2E (BFS) + deg(x) <= 2(V+E) on 500 random graphs", worst <= 0)

# ============================== Q2: knapsack with non-increasing values ==============================
def greedy_val(w, v, S):
    order = sorted(range(len(w)), key=lambda i: w[i])
    tot = 0
    for i in order:
        if w[i] > S:
            break
        S -= w[i]
        tot += v[i]
    return tot


def brute_knap(w, v, S):
    best = 0
    for mask in range(1 << len(w)):
        sw = sum(w[i] for i in range(len(w)) if mask >> i & 1)
        if sw <= S:
            best = max(best, sum(v[i] for i in range(len(w)) if mask >> i & 1))
    return best


W, V = [1, 4, 5, 7, 10], [8, 6, 5, 4, 2]
check("Q2a S=10: greedy value 19 == brute-force optimum", greedy_val(W, V, 10) == brute_knap(W, V, 10) == 19)
check("Q2a S=9: greedy value 14 == brute-force optimum", greedy_val(W, V, 9) == brute_knap(W, V, 9) == 14)
bind_numeric(2, "א", 1, 19, "Q2a")
bind_numeric(2, "א", 2, 14, "Q2a")


def heavy_first(w, v, S):
    tot = 0
    for i in sorted(range(len(w)), key=lambda i: -w[i]):
        if w[i] <= S:
            S -= w[i]
            tot += v[i]
    return tot


def input_order(w, v, S):
    tot = 0
    for i in range(len(w)):
        if w[i] > S:
            break
        S -= w[i]
        tot += v[i]
    return tot


check("Q2a distractor 'heaviest first' loses on the example (S=10 gives 2)", heavy_first(W, V, 10) == 2 != brute_knap(W, V, 10))
check("Q2a distractor 'input order' loses on w=[10,1,4] v=[2,8,6] S=10", input_order([10, 1, 4], [2, 8, 6], 10) == 2 and brute_knap([10, 1, 4], [2, 8, 6], 10) == 14)

# greedy-choice property: with w sorted ascending, v non-increasing, w1 <= S, SOME optimum contains item 1; not every optimum does
def all_optima(w, v, S):
    best, sols = -1, []
    for mask in range(1 << len(w)):
        sw = sum(w[i] for i in range(len(w)) if mask >> i & 1)
        if sw <= S:
            val = sum(v[i] for i in range(len(w)) if mask >> i & 1)
            if val > best:
                best, sols = val, [mask]
            elif val == best:
                sols.append(mask)
    return sols


bad_exists, bad_swap = 0, 0
for _ in range(3000):
    n = random.randint(1, 8)
    w = sorted(random.randint(1, 12) for _ in range(n))
    v = sorted((random.randint(1, 15) for _ in range(n)), reverse=True)
    S = random.randint(0, 35)
    if w[0] > S:
        continue
    sols = all_optima(w, v, S)
    if not any(m & 1 for m in sols):
        bad_exists += 1
    for m in sols:                      # exchange step: replace the first chosen item i1 by item 1
        if m & 1:
            continue
        i1 = min(i for i in range(n) if m >> i & 1) if m else None
        if i1 is None:
            bad_swap += 1               # empty optimum although item 1 fits: impossible when values are positive
            continue
        m2 = (m & ~(1 << i1)) | 1
        sw = sum(w[i] for i in range(n) if m2 >> i & 1)
        sv = sum(v[i] for i in range(n) if m2 >> i & 1)
        if sw > S or sv < sum(v[i] for i in range(n) if m >> i & 1):
            bad_swap += 1
check("Q2b some optimum contains item 1 whenever w1 <= S (3000 inputs)", bad_exists == 0)
check("Q2b the exchange B = A - {i1} + {1} stays feasible and no worse (3000 inputs)", bad_swap == 0)
sols = all_optima([1, 1], [1, 1], 1)
check("Q2b not EVERY optimum contains item 1 and the optimum is not unique (w=[1,1], v=[1,1], S=1)", len(sols) == 2 and any(not m & 1 for m in sols))
sols = all_optima([1, 2], [5, 1], 1)
check("Q2b distractor 'an optimum contains the heaviest item' fails on w=[1,2], v=[5,1], S=1", all(not m & 2 for m in sols))
check("Q2c n log n dominates n for n=1000", 1000 * 9.97 > 1000)

# ============================== Q3: Huffman ==============================
def huff_cost(freqs):
    h = list(freqs)
    heapq.heapify(h)
    tot = 0
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        tot += a + b
        heapq.heappush(h, a + b)
    return tot


def all_huffman_depths(freqs):
    """Set of sorted depth tuples over ALL tie-breakings of the Huffman merges."""
    res = set()

    def rec(nodes):
        if len(nodes) == 1:
            res.add(tuple(sorted(nodes[0][1])))
            return
        nodes = sorted(nodes, key=lambda t: t[0])
        a = nodes[0][0]
        b = nodes[1][0]
        i_cands = [i for i, t in enumerate(nodes) if t[0] == a]
        for i in i_cands:
            rest = nodes[:i] + nodes[i + 1:]
            rest_sorted = sorted(range(len(rest)), key=lambda k: rest[k][0])
            m = rest[rest_sorted[0]][0]
            for j in [k for k in range(len(rest)) if rest[k][0] == m]:
                n1, n2 = nodes[i], rest[j]
                others = [rest[k] for k in range(len(rest)) if k != j]
                merged = (n1[0] + n2[0], [d + 1 for d in n1[1]] + [d + 1 for d in n2[1]])
                rec(others + [merged])
    rec([(f, [0]) for f in freqs])
    return res


F3a = [3, 4, 3, 1, 2]
code = {"a1": "00", "a2": "11", "a3": "01", "a4": "100", "a5": "101"}
cost_code = sum(f * len(c) for f, c in zip(F3a, code.values()))
check("Q3a cost of the printed code for f=3,4,3,1,2 is 29 == Huffman optimum", cost_code == huff_cost(F3a) == 29)
bind_numeric(3, "א", 1, 3, "Q3a first merge")
check("Q3a first Huffman merge: the two smallest (1 and 2) give 3", sorted(F3a)[:2] == [1, 2] and sum(sorted(F3a)[:2]) == 3)
check("Q3a codes 100 and 101 are siblings (same parent prefix 10)", code["a4"][:-1] == code["a5"][:-1] == "10")
bind_numeric(3, "א", 2, 29, "Q3a cost")
bind_choice(3, "א", 0, "הן אחיות: אותו אב בעץ, וההבדל ביניהן בביט האחרון", "Q3a")

F3b = [1, 3, 9, 27, 81]
check("Q3b chain merges 4, 13, 40, 121", [sum(F3b[:k]) for k in range(2, 6)] == [4, 13, 40, 121])
d3b = all_huffman_depths(F3b)
check("Q3b depths of the optimal tree are unique: 1,2,3,4,4", d3b == {(1, 2, 3, 4, 4)}, d3b)
check("Q3b cost 178 == 4+13+40+121", huff_cost(F3b) == 178 == 4 + 13 + 40 + 121)
bind_numeric(3, "ב", 0, 13, "Q3b")
bind_numeric(3, "ב", 1, 4, "Q3b")
bind_numeric(3, "ב", 2, 178, "Q3b")

chain = {(1, 2, 3, 4, 4)}
for q in (2, 3, 10):
    check(f"Q3c ratio q={q} gives the chain tree", all_huffman_depths([q ** i for i in range(5)]) == chain)
d1 = all_huffman_depths([1] * 5)
check("Q3c ratio q=1: every tie-breaking gives depths 2,2,2,3,3 (max 3, not the chain)", d1 == {(2, 2, 2, 3, 3)}, d1)
bind_choice(3, "ג", 0, "$q=1$", "Q3c")
bind_numeric(3, "ג", 1, 3, "Q3c")

# ============================== Q4: jumping game ==============================
def bfs_jumps(A):
    n = len(A)
    dist = {1: 0}
    dq = deque([1])
    while dq:
        i = dq.popleft()
        for j in range(1, A[i - 1] + 1):
            if i + j <= n and i + j not in dist:
                dist[i + j] = dist[i] + 1
                dq.append(i + j)
    return dist.get(n)


def table_forward(A):
    n = len(A)
    INF = 10 ** 9
    C = [INF] * (n + 2)
    C[n] = 0
    for i in range(n - 1, 0, -1):
        m = min(A[i - 1], n - i)
        if m >= 1:
            C[i] = 1 + min(C[i + j] for j in range(1, m + 1))
    return C


EX = [1, 4, 6, 4, 5, 3, 3, 2, 1, 3]
C = table_forward(EX)
check("Q4a example: C(5)=1, C(2)=2, C(1)=3", (C[5], C[2], C[1]) == (1, 2, 3) and bfs_jumps(EX) == 3)
bind_numeric(4, "א", 0, C[5], "Q4a")
bind_numeric(4, "א", 1, C[2], "Q4a")
bind_numeric(4, "א", 3, C[1], "Q4a")


def rec_variant(A, kind):
    n = len(A)
    INF = 10 ** 9
    C = [INF] * (n + 2)
    C[n] = 0
    for i in range(n - 1, 0, -1):
        m = min(A[i - 1], n - i)
        if kind == "greedy_far":
            C[i] = 1 + C[min(i + A[i - 1], n)]
        elif m >= 1:
            vals = [C[i + j] for j in range(1, m + 1)]
            C[i] = {"max": 1 + max(vals), "nopl1": min(vals)}[kind]
    return C[1]


for kind in ("greedy_far", "max", "nopl1"):
    bad = 0
    for _ in range(2000):
        n = random.randint(2, 9)
        A = [random.randint(1, 4) for _ in range(n)]
        bad += rec_variant(A, kind) != bfs_jumps(A)
    check(f"Q4a distractor recurrence '{kind}' disagrees with BFS on some array", bad > 0, f"({bad})")
check("Q4a distractor 'farthest jump' gives 4 on the example (optimum 3)", rec_variant(EX, "greedy_far") == 4)
bad = sum(table_forward(A)[1] != bfs_jumps(A) for A in ([random.randint(1, 4) for _ in range(random.randint(1, 9))] for _ in range(3000)))
check("Q4a correct recurrence == BFS on 3000 arrays", bad == 0)

n = 10
inner = sum(n - i for i in range(1, n))
check("Q4b A[i]=n for all i, n=10: the recurrence examines sum (n-i) = 45 values", inner == 45)
bind_numeric(4, "ב", 2, inner, "Q4b")
bind_text(4, "ב", 0, "O(n^2)", "Q4b time")
bind_text(4, "ב", 1, "O(n)", "Q4b space")

# path reconstruction: unique argmin from each position along the example
C = table_forward(EX)
path, i, unique = [1], 1, True
while i != len(EX):
    m = min(EX[i - 1], len(EX) - i)
    cands = [j for j in range(1, m + 1) if C[i + j] == C[i] - 1]
    unique &= len(cands) == 1
    i += cands[0]
    path.append(i)
check("Q4c example: unique optimal path 1,2,5,10", path == [1, 2, 5, 10] and unique)
bind_numeric(4, "ג", 0, path[2], "Q4c")
bind_numeric(4, "ג", 1, len(path), "Q4c")
bind_text(4, "ג", 2, "O(n)", "Q4c space")

# ============================== Bonus: Prim from C ==============================
E = [("L", "TL", 12), ("TL", "TM", 9), ("TM", "TR", 11), ("TM", "C", 8), ("TR", "BR", 13),
     ("C", "BL", 10), ("C", "BM", 9), ("BL", "BM", 8), ("BM", "BR", 13), ("L", "BL", 15)]
H = nx.Graph()
for u, v, w in E:
    H.add_edge(u, v, weight=w)
orders = set()
ties_at_step = {}


def prim_all(vis, seq):
    if len(vis) == len(H):
        orders.add(tuple(seq))
        return
    cands = [(d["weight"], u, v) for u in vis for v, d in H[u].items() if v not in vis]
    mn = min(c[0] for c in cands)
    tied = [c for c in cands if c[0] == mn]
    ties_at_step.setdefault(len(seq), set()).add(len(tied))
    for w, u, v in tied:
        prim_all(vis | {v}, seq + [w])


prim_all({"C"}, [])
check("Bonus first weight is 8 in every tie-break", {o[0] for o in orders} == {8})
check("Bonus at the second step exactly 2 edges of weight 9 are tied", ties_at_step[1] == {2})
check("Bonus after 8,9,9 the next weight is 8 in every order that starts 8,9,9", {o[3] for o in orders if o[:3] == (8, 9, 9)} == {8})
check("Bonus the sequence 8,9,9,8,11,12,13 is a possible Prim order; total 70", (8, 9, 9, 8, 11, 12, 13) in orders and sum(o for o in (8, 9, 9, 8, 11, 12, 13)) == 70)
check("Bonus MST weight 70", sum(d["weight"] for _, _, d in nx.minimum_spanning_edges(H, data=True)) == 70)
bind_numeric(5, "", 0, 8, "Bonus")
bind_numeric(5, "", 1, 2, "Bonus")
bind_numeric(5, "", 2, 8, "Bonus")
bind_numeric(5, "", 3, 70, "Bonus")

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
