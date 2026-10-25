# -*- coding: utf-8 -*-
"""Learn-brief checks: graphs_search + graph_proofs (briefs 05, 06): every claim and counterexample of the briefs.
Run: PYTHONUTF8=1 py tools/verify/learn/v03_graphs.py     (ASCII output, exits 1 on a failure)
The traces of the embedded ```graph figures are checked separately by v04_graph_embeds.py."""
import itertools, random, sys
from collections import deque

import networkx as nx

ok = True
INF = float("inf")


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


random.seed(20261025)


# ------------------------------------------------------------------ generic BFS / DFS with explicit neighbour orders
def bfs(adj, s, order=None):
    """adj: dict v -> list of neighbours (already in the order to scan). Returns d, pi, tree edge list."""
    d, pi, tree = {s: 0}, {s: None}, []
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in d:
                d[v] = d[u] + 1
                pi[v] = u
                tree.append((u, v))
                q.append(v)
    return d, pi, tree


def dfs(adj, roots, directed):
    """full DFS. Returns disc, fin, pi, classes {(u,v): kind} (undirected: each edge once, tree/back), tree edges"""
    color, disc, fin, pi, cls, tree = {}, {}, {}, {}, {}, []
    t = [0]
    seen_und = set()

    def visit(u):
        t[0] += 1
        disc[u] = t[0]
        color[u] = "g"
        for v in adj[u]:
            if not directed:
                key = frozenset((u, v))
                if key in seen_und and v != pi.get(u):
                    continue
            c = color.get(v, "w")
            if not directed:
                if c == "w":
                    seen_und.add(frozenset((u, v)))
                    cls[(u, v)] = "tree"
                    tree.append((u, v))
                    pi[v] = u
                    visit(v)
                elif v == pi.get(u):
                    continue
                elif c == "g":
                    seen_und.add(frozenset((u, v)))
                    cls[(u, v)] = "back"
                continue
            if c == "w":
                cls[(u, v)] = "tree"
                tree.append((u, v))
                pi[v] = u
                visit(v)
            elif c == "g":
                cls[(u, v)] = "back"
            else:
                cls[(u, v)] = "forward" if disc[u] < disc[v] else "cross"
        color[u] = "b"
        t[0] += 1
        fin[u] = t[0]

    for r in roots:
        if r not in color:
            pi[r] = None
            visit(r)
    return disc, fin, pi, cls, tree


def adjacency(n, edges, directed, shuffle=False):
    adj = {v: [] for v in range(n)}
    for u, v in edges:
        adj[u].append(v)
        if not directed and u != v:
            adj[v].append(u)
    for v in adj:
        adj[v].sort()
        if shuffle:
            random.shuffle(adj[v])
    return adj


def rand_graph(n, p, directed, loops=False):
    pairs = [(u, v) for u in range(n) for v in range(n) if (u != v or loops) and (directed or u < v)]
    return [e for e in pairs if random.random() < p]


# ================================================================== brief 05
# ---- BFS distances = shortest paths; depth of the BFS tree = max distance
bad = 0
for _ in range(300):
    n = random.randint(2, 9)
    E = rand_graph(n, random.random(), False)
    G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E)
    s = random.randrange(n)
    d, pi, tree = bfs(adjacency(n, E, False, True), s)
    sp = nx.single_source_shortest_path_length(G, s)
    bad += d != sp
    depth = max(d.values())
    bad += depth != max(sp.values())
check("BFS distance == shortest path length, tree depth == eccentricity (300 random, shuffled neighbour orders)", bad == 0)

# ---- DFS edge classes by colour == by time intervals; undirected: tree/back only; parenthesis + white path
bad = bad2 = bad3 = 0
for _ in range(300):
    n = random.randint(2, 8)
    directed = random.random() < 0.6
    E = rand_graph(n, random.random() * 0.6, directed, loops=directed and random.random() < 0.3)
    adj = adjacency(n, E, directed, True)
    roots = random.sample(range(n), n)
    disc, fin, pi, cls, tree = dfs(adj, roots, directed)
    for (u, v), k in cls.items():
        if directed:
            if u == v:
                want = "back"
            elif k == "tree":
                want = "tree" if pi[v] == u else None
            else:
                du, fu, dv, fv = disc[u], fin[u], disc[v], fin[v]
                want = ("forward" if du < dv < fv < fu else "back" if dv < du < fu < fv else "cross" if fv < du else None)
            bad += want != k
        else:
            bad2 += k not in ("tree", "back")
    # parenthesis theorem for every pair
    for u, v in itertools.combinations(range(n), 2):
        a, b = (disc[u], fin[u]), (disc[v], fin[v])
        disjoint = a[1] < b[0] or b[1] < a[0]
        nested = (a[0] < b[0] < b[1] < a[1]) or (b[0] < a[0] < a[1] < b[1])
        bad3 += disjoint == nested  # exactly one must hold
check("DFS edge classification by colour agrees with the time-interval definitions (300 random digraphs/graphs)", bad == 0)
check("undirected DFS has only tree and back edges", bad2 == 0)
check("parenthesis theorem: intervals disjoint or nested, never overlapping (300 random)", bad3 == 0)

# white-path theorem
bad = 0
for _ in range(300):
    n = random.randint(2, 8)
    E = rand_graph(n, random.random() * 0.5, True)
    adj = adjacency(n, E, True, True)
    disc, fin, pi, cls, tree = dfs(adj, random.sample(range(n), n), True)
    desc = {u: set() for u in range(n)}
    for v in range(n):
        x = pi.get(v)
        while x is not None:
            desc[x].add(v)
            x = pi.get(x)
    G = nx.DiGraph(); G.add_nodes_from(range(n)); G.add_edges_from(E)
    for u in range(n):
        white = [w for w in range(n) if disc[w] >= disc[u]]  # white (undiscovered) at time d[u], plus u itself
        H = G.subgraph(white)
        reach = nx.descendants(H, u) if u in H else set()
        bad += reach != desc[u]
check("white-path theorem: v is a descendant of u iff a white path u->v exists at d[u] (300 random)", bad == 0)

# cycle <=> back edge ; topological order by decreasing finish time
bad = bad2 = 0
for _ in range(400):
    n = random.randint(2, 8)
    E = rand_graph(n, random.random() * 0.5, True)
    adj = adjacency(n, E, True, True)
    disc, fin, pi, cls, tree = dfs(adj, random.sample(range(n), n), True)
    G = nx.DiGraph(); G.add_nodes_from(range(n)); G.add_edges_from(E)
    has_back = any(k == "back" for k in cls.values())
    bad += has_back != (not nx.is_directed_acyclic_graph(G))
    if nx.is_directed_acyclic_graph(G):
        order = sorted(range(n), key=lambda v: -fin[v])
        pos = {v: i for i, v in enumerate(order)}
        bad2 += any(pos[u] > pos[v] for u, v in E)
check("directed graph has a cycle iff DFS finds a back edge (400 random)", bad == 0)
check("decreasing finish time is a valid topological order of a DAG (400 random)", bad2 == 0)

# roots / leaves of the DFS forest
bad = 0
for _ in range(200):
    n = random.randint(1, 9)
    E = rand_graph(n, random.random() * 0.5, True)
    adj = adjacency(n, E, True, True)
    disc, fin, pi, cls, tree = dfs(adj, random.sample(range(n), n), True)
    roots = [v for v in range(n) if pi[v] is None]
    parents = {p for p in pi.values() if p is not None}
    leaves_pi = [v for v in range(n) if v not in parents]
    leaves_time = [v for v in range(n) if fin[v] == disc[v] + 1]
    bad += leaves_pi != leaves_time
    bad += len(roots) != sum(1 for v in range(n) if pi[v] is None)
check("leaf = never a parent in pi = (f = d + 1); roots = pi NIL (200 random)", bad == 0)

# ---- recipes: walk through z, shortest path through z, walk through A, cut vertex, bipartite
bad = bad2 = bad3 = bad4 = bad5 = 0
for _ in range(300):
    n = random.randint(3, 8)
    E = rand_graph(n, random.random() * 0.6, False)
    G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E)
    x, y, z = random.sample(range(n), 3)
    # walk x -> y through z exists iff x and y reachable from z
    comp = nx.node_connected_component(G, z)
    walk_exists = x in comp and y in comp
    # brute force on the product graph (vertex, passed z)
    P = nx.DiGraph()
    for u in range(n):
        for v in G[u]:
            for f in (0, 1):
                P.add_edge((u, f), (v, 1 if (f or v == z) else 0))
    start = (x, 1 if x == z else 0)
    bad += walk_exists != (start in P and (y, 1) in P and nx.has_path(P, start, (y, 1))) if start in P else walk_exists != (x == y == z)
    # shortest path through z
    if nx.has_path(G, x, y):
        dxy = nx.shortest_path_length(G, x, y)
        on_sp = any(z in p for p in nx.all_shortest_paths(G, x, y))
        f = z in comp and x in comp and nx.shortest_path_length(G, x, z) + nx.shortest_path_length(G, z, y) == dxy if nx.has_path(G, x, z) and nx.has_path(G, z, y) else False
        bad2 += on_sp != f
    # walk through set A
    A = set(random.sample([v for v in range(n) if v not in (x, y)], random.randint(1, max(1, n - 2)))) if n > 2 else set()
    if A and nx.has_path(G, x, y):
        dx, dy = nx.single_source_shortest_path_length(G, x), nx.single_source_shortest_path_length(G, y)
        formula = min((dx[a] + dy[a] for a in A if a in dx and a in dy), default=INF)
        # brute force: shortest walk visiting some vertex of A = BFS on (v, visitedA)
        Q = deque([(x, 0, 0)]); seen = {(x, 0)}; best = INF
        while Q:
            u, f, dist = Q.popleft()
            if u == y and f:
                best = dist; break
            for v in G[u]:
                nf = 1 if (f or v in A) else 0
                if (v, nf) not in seen:
                    seen.add((v, nf)); Q.append((v, nf, dist + 1))
        bad3 += formula != best
    # bipartite check by BFS level parity
    colour, okb = {}, True
    for r in range(n):
        if r in colour:
            continue
        colour[r] = 0
        q = deque([r])
        while q:
            u = q.popleft()
            for v in G[u]:
                if v not in colour:
                    colour[v] = 1 - colour[u]; q.append(v)
                elif colour[v] == colour[u]:
                    okb = False
    bad4 += okb != nx.is_bipartite(G)
    # cut vertex: neighbours of x not all in one component of G - x
    c = random.randrange(n)
    H = G.copy(); H.remove_node(c)
    nb = list(G[c])
    if len(nb) <= 1:
        alg = False
    else:
        reach = nx.node_connected_component(H, nb[0])
        alg = any(u not in reach for u in nb)
    brute = nx.number_connected_components(H) > nx.number_connected_components(G) - (1 if G.degree(c) == 0 else 0) if False else None
    comps_before = nx.number_connected_components(G)
    comps_after = nx.number_connected_components(H)
    # definition from the exam: more components in G - v than in G (an isolated vertex alone does not count: removing it lowers the count)
    bad5 += alg != (comps_after > comps_before)
check("walk x->y through z exists iff x, y in z's component (300 random)", bad == 0)
check("shortest x->y path through z iff d(x,z)+d(z,y)=d(x,y) (300 random)", bad2 == 0)
check("shortest walk through a set A is min over a of dx[a]+dy[a] (300 random)", bad3 == 0)
check("BFS parity colouring decides bipartiteness (300 random)", bad4 == 0)
check("cut-vertex test (BFS from one neighbour in G-x reaches all neighbours) (300 random)", bad5 == 0)

# the worked example of brief 05 : B1
B1 = nx.Graph([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "F"), ("E", "G"), ("F", "G")])
check("example: d(A,F)=3, d(A,D)=2, d(D,F)=1, d(A,E)=2, d(E,F)=2; D on a shortest A-F path, E not",
      nx.shortest_path_length(B1, "A", "F") == 3 and nx.shortest_path_length(B1, "A", "D") == 2 and nx.shortest_path_length(B1, "D", "F") == 1
      and nx.shortest_path_length(B1, "A", "E") == 2 and nx.shortest_path_length(B1, "E", "F") == 2
      and any("D" in p for p in nx.all_shortest_paths(B1, "A", "F")) and not any("E" in p for p in nx.all_shortest_paths(B1, "A", "F")))

# ================================================================== brief 06
# ---- 24B-A Q1: counting tree edges of BFS from v vs the DFS forest, undirected
def undirected_counts(n, E):
    adj = adjacency(n, E, False)
    _, _, _, _, tdfs = dfs(adj, range(n), False)
    return len(tdfs), [len(bfs(adj, v)[2]) for v in range(n)]

# a: two triangles, 6 vertices, 6 edges, not connected
tri2 = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]
G = nx.Graph(tri2); G.add_nodes_from(range(6))
check("24B-A Q1a: two disjoint triangles: 6 vertices, 6 edges, not connected", G.number_of_nodes() == 6 and G.number_of_edges() == 6 and not nx.is_connected(G))
# b: 5 vertices, 5 edges, vertex 4 isolated; BFS from 0 and DFS forest both have 3 tree edges
ex_b = [(0, 1), (1, 2), (2, 3), (0, 2), (1, 3)]
nd, nb = undirected_counts(5, ex_b)
check("24B-A Q1b: K4 minus an edge + isolated vertex: E_DFS = 3, BFS from 0 gives 3, graph not connected", nd == 3 and nb[0] == 3 and len(ex_b) == 5)
# c: exhaustive up to n=6: if |E_BFS(G,v)| = |E_DFS(G)| for ALL v and G has an edge, G is connected
bad = 0
cnt = 0
for n in range(2, 7):
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        E = [pairs[i] for i in range(len(pairs)) if (mask >> i) & 1]
        if not E:
            continue
        nd, nb = undirected_counts(n, E)
        cnt += 1
        if all(c == nd for c in nb):
            G = nx.Graph(E); G.add_nodes_from(range(n))
            bad += not nx.is_connected(G)
check("24B-A Q1c: for all v equal counts => connected, exhaustive over all graphs with an edge on n<=6 (%d graphs)" % cnt, bad == 0)
# the claim needs an edge: the edgeless graph on 2 vertices has all counts 0
nd, nb = undirected_counts(2, [])
check("without an edge the premise holds vacuously for a disconnected graph (n=2, no edges)", nd == 0 and nb == [0, 0])

# ---- 24B-B Q1 (directed): E_DFS = E_BFS
def digraph_runs(n, E, s, samples=6):
    out = []
    for _ in range(samples):
        adj = adjacency(n, E, True, True)
        others = [v for v in range(n) if v != s]
        random.shuffle(others)
        _, _, _, _, tdfs = dfs(adj, [s] + others, True)
        adj2 = adjacency(n, E, True, True)
        _, _, tb = bfs(adj2, s)
        out.append((frozenset(tdfs), frozenset(tb)))
    return out

# counterexample of (a) and (c): V={s,a,b}=0,1,2 with edges s->a, b->s
E = [(0, 1), (2, 0)]
runs = digraph_runs(3, E, 0, 20)
G = nx.DiGraph(E)
check("24B-B Q1a/c: s->a, b->s : E_DFS = E_BFS = {(s,a)} but s is not a root (b unreachable); every degree-sum is nonzero",
      all(a == b == frozenset({(0, 1)}) for a, b in runs) and (2 not in nx.descendants(G, 0))
      and all(G.in_degree(v) + G.out_degree(v) != 0 for v in G))
# b: all digraphs without loops on n=3 (exhaustive-ish) and n=4 (sampled): in- and out-degree nonzero for every vertex & E_DFS = E_BFS => s root
bad = tested = 0
for n in (3, 4):
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v]
    masks = range(1 << len(pairs)) if n == 3 else random.sample(range(1 << len(pairs)), 600)
    for mask in masks:
        E = [pairs[i] for i in range(len(pairs)) if (mask >> i) & 1]
        G = nx.DiGraph(E); G.add_nodes_from(range(n))
        if not all(G.in_degree(v) > 0 and G.out_degree(v) > 0 for v in range(n)):
            continue
        for s in range(n):
            for a, b in digraph_runs(n, E, s, 4):
                tested += 1
                if a == b and len(nx.descendants(G, s)) != n - 1:
                    bad += 1
check("24B-B Q1b: indeg, outdeg >= 1 for all and E_DFS = E_BFS => s is a root (no self-loops); %d runs" % tested, bad == 0 and tested > 100)
# with self loops the claim fails: V={s,x}, E={(s,s),(x,x)}
check("24B-B Q1b note: with self-loops s->s, x->x the premise holds and s is not a root",
      all(a == b == frozenset() for a, b in digraph_runs(2, [(0, 0), (1, 1)], 0, 4)))

# ---- 26A-B Q2a: BFS tree depth does not depend on the neighbour order
bad = 0
for _ in range(300):
    n = random.randint(2, 9)
    E = rand_graph(n, 0.45, False)
    G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E)
    s = random.randrange(n)
    depths = set()
    for _ in range(4):
        d, _, _ = bfs(adjacency(n, E, False, True), s)
        depths.add(max(d.values()))
    bad += len(depths) != 1
check("26A-B Q2a: BFS tree depth is the same for every neighbour order (300 random)", bad == 0)

# ---- 26A-B Q2b: DFS depth can differ : s->a, s->b, a->b
def depth_of(pi):
    best = 0
    for v in pi:
        k, x = 0, v
        while pi[x] is not None:
            x = pi[x]; k += 1
        best = max(best, k)
    return best

S, A_, B_ = 0, 1, 2
disc, fin, pi, cls, tree = dfs({S: [A_, B_], A_: [B_], B_: []}, [S], True)
d1 = depth_of(pi)
disc2, fin2, pi2, cls2, tree2 = dfs({S: [B_, A_], A_: [B_], B_: []}, [S], True)
d2 = depth_of(pi2)
check("26A-B Q2b: scanning a first gives depth 2, scanning b first gives depth 1 (a->b becomes a cross edge)",
      d1 == 2 and d2 == 1 and cls2[(A_, B_)] == "cross" and cls[(A_, B_)] == "tree", (d1, d2))

# ---- 26B-A Q3a: BFS counterexample, 5-cycle s-u-x-v-w-s
G5 = {"s": ["u", "w"], "u": ["s", "x"], "w": ["s", "v"], "x": ["u", "v"], "v": ["x", "w"]}
d, pi, tree = bfs(G5, "s")
check("26B-A Q3a: BFS order s,u,w,x,v with pi(v)=w, pi(x)=u", list(d) == ["s", "u", "w", "x", "v"] and pi["v"] == "w" and pi["x"] == "u", pi)
anc, x = [], "v"
while x is not None:
    anc.append(x); x = pi[x]
check("26B-A Q3a: at the moment u is dequeued v is white and u->x->v is a path, yet v is not a descendant of u",
      "u" not in anc and "v" not in {"s", "u"} and G5["u"] == ["s", "x"] and "v" in G5["x"])

# ---- 26B-A Q3b: connected graph with a cycle: T_BFS != T_DFS for every neighbour order and every source
bad = tested = 0
for n in range(3, 6):
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        E = [pairs[i] for i in range(len(pairs)) if (mask >> i) & 1]
        G = nx.Graph(E); G.add_nodes_from(range(n))
        if not nx.is_connected(G) or len(E) < n:
            continue  # connected with a cycle <=> |E| >= |V|
        for s in range(n):
            for _ in range(4):
                adj = adjacency(n, E, False, True)
                _, _, tb = bfs(adj, s)
                adj2 = adjacency(n, E, False, True)
                _, _, _, _, td = dfs(adj2, [s], False)
                tested += 1
                bad += {frozenset(e) for e in tb} == {frozenset(e) for e in td}
check("26B-A Q3b: T_BFS != T_DFS for every connected graph with a cycle on n<=5, all sources, random orders (%d runs)" % tested, bad == 0 and tested > 1000)

sys.exit(0 if ok else 1)
