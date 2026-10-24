# -*- coding: utf-8 -*-
"""Python reference for graph.js (the step-through visualizer). Reads a JSON list of graph specs on stdin and
writes, for each, {"events": [...], "result": {...}, "nx": [problems]} on stdout.

Two independent checks per spec:
  1. an own implementation of every algorithm with the SAME conventions as graph.js (alphabetical / natural
     neighbour order, extract-min ties to the earlier vertex, Kruskal ties by endpoint names, DFS with
     discovery/finish times and edge classes, Kosaraju SCC, topo = decreasing finish time). Its event
     sequence and final outputs must equal graph.js's (tools/test_graph.js compares them).
  2. networkx on the same graph: BFS distances and discovery order, the DFS preorder of the first tree,
     acyclicity vs back edges, topological validity, the SCC partition, Dijkstra distances, MST weight
     (and the MST edge set when the weights are distinct). Any disagreement is listed in "nx".

    node tools/test_graph.js        (the driver: random graphs -> graph.js + this script -> compare)
Prints JSON only (ASCII-safe).
"""
import json, re, sys

import networkx as nx

INF = float("inf")
NUM = re.compile(r"^-?\d+(\.\d+)?$")


def nat_key(s):
    return (0, float(s), s) if NUM.match(s) else (1, 0.0, s)


def build(spec):
    given = [str(n["id"] if isinstance(n, dict) else n) for n in spec["nodes"]]
    alpha = spec.get("order", "alpha") == "alpha"
    ids = sorted(given, key=nat_key) if alpha else given
    rank = {v: i for i, v in enumerate(ids)}
    edges = [{"u": str(e["u"]), "v": str(e["v"]), "w": e.get("w"), "i": i} for i, e in enumerate(spec["edges"])]
    directed = bool(spec["directed"])
    adj = {v: [] for v in ids}
    radj = {v: [] for v in ids}
    for e in edges:
        adj[e["u"]].append((e["v"], e["w"], e["i"]))
        if directed:
            radj[e["v"]].append((e["u"], e["w"], e["i"]))
        elif e["u"] != e["v"]:
            adj[e["v"]].append((e["u"], e["w"], e["i"]))
    key = (lambda a: (nat_key(a[0]), a[2])) if alpha else (lambda a: a[2])
    for v in ids:
        adj[v].sort(key=key)
        radj[v].sort(key=key)
    src = str(spec["source"]) if "source" in spec else ids[0]
    return dict(ids=ids, rank=rank, edges=edges, adj=adj, radj=radj, directed=directed, alpha=alpha, source=src)


def num(x):
    return None if x == INF else x


def bfs(G):
    s, ev = G["source"], []
    d = {v: INF for v in G["ids"]}
    pi = {v: None for v in G["ids"]}
    color = {v: "w" for v in G["ids"]}
    d[s], color[s], q, order = 0, "g", [s], [s]
    ev.append(["start", s])
    while q:
        u = q.pop(0)
        ev.append(["deq", u])
        for v, _, _ in G["adj"][u]:
            ev.append(["edge", u, v])
            if color[v] == "w":
                color[v], d[v], pi[v] = "g", d[u] + 1, u
                q.append(v)
                order.append(v)
                ev.append(["disc", v, u, d[v]])
        color[u] = "b"
    return ev, {"order": order, "d": {k: num(x) for k, x in d.items()}, "pi": pi}


KIND = {"tree": "tree", "back": "back", "fwd": "forward", "cross": "cross"}


def dfs_pass(G, ev, topo=None):
    color = {v: "w" for v in G["ids"]}
    d, f, pi, cls, pi_edge, order = {}, {}, {v: None for v in G["ids"]}, {}, {}, []
    t = [0]
    sys.setrecursionlimit(10000)

    def visit(u):
        t[0] += 1
        d[u] = t[0]
        color[u] = "g"
        order.append(u)
        ev.append(["disc", u, t[0]])
        for v, _, e in G["adj"][u]:
            if not G["directed"] and (e == pi_edge.get(u) or e in cls):
                continue
            if color[v] == "w":
                k = "tree"
            elif color[v] == "g":
                k = "back"
            else:
                k = "fwd" if d[u] < d[v] else "cross"
            cls[e] = k
            ev.append(["edge", u, v, KIND[k]])
            if k == "tree":
                pi[v], pi_edge[v] = u, e
                visit(v)
        t[0] += 1
        f[u] = t[0]
        color[u] = "b"
        ev.append(["fin", u, t[0]])
        if topo is not None:
            topo.insert(0, u)

    main = [G["source"]] + [v for v in G["ids"] if v != G["source"]]
    for u in main:
        if color[u] == "w":
            visit(u)
    classes = {f'{e["u"]}-{e["v"]}': KIND[cls[e["i"]]] for e in G["edges"] if e["i"] in cls}
    return {"order": order, "disc": d, "fin": f, "pi": pi, "classes": classes}


def dfs(G):
    ev = []
    return ev, dfs_pass(G, ev)


def topo(G):
    ev, lst = [], []
    r = dfs_pass(G, ev, lst)
    r["topo"] = lst
    r["acyclic"] = "back" not in r["classes"].values()
    return ev, r


def scc(G):
    ev = []
    r = dfs_pass(G, ev)
    by_f = sorted(G["ids"], key=lambda v: -r["fin"][v])
    color = {v: "w" for v in G["ids"]}
    comps, comp = [], {}

    def visit2(u, k):
        color[u] = "g"
        comp[u] = k
        comps[-1].append(u)
        for v, _, _ in G["radj"][u]:
            if color[v] != "w":
                continue
            ev.append(["tree2", u, v])
            visit2(v, k)
        color[u] = "b"

    for u in by_f:
        if color[u] != "w":
            continue
        comps.append([])
        ev.append(["root", u, len(comps)])
        visit2(u, len(comps))
    r["scc"] = comps
    r["comp"] = comp
    return ev, r


def extract_min(G, val, closed):
    best = None
    for v in G["ids"]:
        if v not in closed and (best is None or val[v] < val[best]):
            best = v
    return best


def dijkstra(G):
    s, ev, closed, order = G["source"], [], set(), []
    d = {v: INF for v in G["ids"]}
    pi = {v: None for v in G["ids"]}
    d[s] = 0
    while True:
        u = extract_min(G, d, closed)
        if u is None or d[u] == INF:
            break
        closed.add(u)
        order.append(u)
        ev.append(["extract", u, d[u]])
        for v, w, _ in G["adj"][u]:
            if v in closed:
                continue
            nd = d[u] + w
            if nd < d[v]:
                d[v], pi[v] = nd, u
                ev.append(["relax", u, v, 1, nd])
            else:
                ev.append(["relax", u, v, 0, nd])
    return ev, {"d": {k: num(x) for k, x in d.items()}, "pi": pi, "order": order}


def prim(G):
    r, ev, closed, order, mst, weight = G["source"], [], set(), [], [], 0
    key = {v: INF for v in G["ids"]}
    pi = {v: None for v in G["ids"]}
    key[r] = 0
    while True:
        u = extract_min(G, key, closed)
        if u is None or key[u] == INF:
            break
        closed.add(u)
        order.append(u)
        if pi[u] is not None:
            mst.append([pi[u], u])
            weight += key[u]
        ev.append(["extract", u, key[u], pi[u]])
        for v, w, _ in G["adj"][u]:
            if v in closed:
                continue
            if w < key[v]:
                key[v], pi[v] = w, u
                ev.append(["upd", u, v, 1, w])
            else:
                ev.append(["upd", u, v, 0, w])
    return ev, {"mst": mst, "weight": weight, "pi": pi, "order": order, "key": {k: num(x) for k, x in key.items()}}


def kruskal(G):
    ev = []

    def k(e):
        a, b = sorted([e["u"], e["v"]], key=nat_key)
        return (e["w"], nat_key(a), nat_key(b), e["i"]) if G["alpha"] else (e["w"], e["i"])

    parent = {v: v for v in G["ids"]}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    mst, weight, need = [], 0, len(G["ids"]) - 1
    for e in sorted(G["edges"], key=k):
        if len(mst) >= need:
            break
        a, b = find(e["u"]), find(e["v"])
        if a != b:
            parent[b] = a
            mst.append([e["u"], e["v"]])
            weight += e["w"]
            ev.append(["take", e["u"], e["v"], e["w"]])
        else:
            ev.append(["skip", e["u"], e["v"], e["w"]])
    return ev, {"mst": mst, "weight": weight}


RUN = {"bfs": bfs, "dfs": dfs, "topo": topo, "scc": scc, "dijkstra": dijkstra, "prim": prim, "kruskal": kruskal}


# ------------------------------------------------------------------ networkx cross-checks
def nx_graph(G):
    X = nx.DiGraph() if G["directed"] else nx.Graph()
    X.add_nodes_from(G["ids"])
    for e in G["edges"]:
        X.add_edge(e["u"], e["v"], weight=e["w"] if e["w"] is not None else 1)
    return X


def nat_sorted(it):
    return sorted(it, key=nat_key)


def nx_problems(G, algo, res):
    X, P, s = nx_graph(G), [], G["source"]
    if algo == "bfs":
        sp = nx.single_source_shortest_path_length(X, s)
        for v in G["ids"]:
            if res["d"][v] != sp.get(v):
                P.append(f"bfs d[{v}]={res['d'][v]} nx={sp.get(v)}")
        nxo = [s] + [v for _, v in nx.bfs_edges(X, s, sort_neighbors=nat_sorted)]
        if G["alpha"] and nxo != res["order"]:
            P.append(f"bfs order {res['order']} nx {nxo}")
    if algo in ("dfs", "topo", "scc"):
        pre = list(nx.dfs_preorder_nodes(X, s, sort_neighbors=nat_sorted))
        if G["alpha"] and pre != res["order"][:len(pre)]:
            P.append(f"dfs preorder {res['order'][:len(pre)]} nx {pre}")
        d, f = res["disc"], res["fin"]
        for u in G["ids"]:
            for v in G["ids"]:
                if u != v and d[u] < d[v] < f[u] and not d[u] < f[v] < f[u]:
                    P.append(f"parenthesis theorem broken for {u},{v}")
        if G["directed"]:
            has_back = "back" in res["classes"].values()
            if has_back == nx.is_directed_acyclic_graph(X):
                P.append(f"back edges={has_back} but nx acyclic={nx.is_directed_acyclic_graph(X)}")
        else:
            trees = sum(1 for v in G["ids"] if res["pi"][v] is None)
            if trees != nx.number_connected_components(X):
                P.append(f"dfs trees {trees} vs nx components {nx.number_connected_components(X)}")
    if algo == "topo" and res["acyclic"]:
        pos = {v: i for i, v in enumerate(res["topo"])}
        if any(pos[u] >= pos[v] for u, v in X.edges()):
            P.append("topo order violates an edge")
    if algo == "scc":
        a = sorted(sorted(c) for c in res["scc"])
        b = sorted(sorted(c) for c in nx.strongly_connected_components(X))
        if a != b:
            P.append(f"scc {a} nx {b}")
    if algo == "dijkstra":
        sp = nx.single_source_dijkstra_path_length(X, s)
        for v in G["ids"]:
            if res["d"][v] != sp.get(v):
                P.append(f"dijkstra d[{v}]={res['d'][v]} nx={sp.get(v)}")
    if algo in ("prim", "kruskal"):
        H = X.subgraph(nx.node_connected_component(X, s)) if algo == "prim" else X
        T = nx.minimum_spanning_tree(H, weight="weight")
        wt = T.size(weight="weight")
        if abs(wt - res["weight"]) > 1e-9:
            P.append(f"{algo} weight {res['weight']} nx {wt}")
        ws = [e["w"] for e in G["edges"]]
        if len(set(ws)) == len(ws):
            a = sorted(tuple(sorted(p)) for p in res["mst"])
            b = sorted(tuple(sorted(e)) for e in T.edges())
            if a != b:
                P.append(f"{algo} edges {a} nx {b}")
    return P


def main():
    specs = json.loads(sys.stdin.read())
    out = []
    for spec in specs:
        G = build(spec)
        ev, res = RUN[spec["algo"]](G)
        out.append({"events": ev, "result": res, "nx": nx_problems(G, spec["algo"], res)})
    sys.stdout.write(json.dumps(out, ensure_ascii=True))


if __name__ == "__main__":
    main()
