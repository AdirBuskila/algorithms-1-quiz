# -*- coding: utf-8 -*-
"""Graph-search widgets for the graph_search videos (B01..B08), plus the runs the scripts assert with.

Every run comes from tools/graph_ref.py (the Python twin of the app's graph.js: same neighbour order, same events) and
is re-checked here against an independent BFS/DFS written below and against networkx. So the animation on screen is
exactly what the app's step-through visualizer shows for the same graph.

Stage widget (every class prefixed gs-; SVG never contains TeX):
  Graph(pfx, nodes, edges, directed, pos)          nodes: ["A", ...]; edges: [("A", "B"), ...]; pos: {v: (x, y)}
    ids  {pfx}-g-{v} / {pfx}-k-{v}   the node painted gray / black (hidden; white is the base)
         {pfx}-c-{v}                 ring around the node being handled (hidden)
         {pfx}-m-{v}                 an amber mark around a node (hidden; for "this one" in a claim)
         {pfx}-e-{u}-{v}-{kind}      edge overlay, kind in tree/back/fwd/cross/hl/dim (hidden; undirected: the
                                     edge as listed, see eid())
         {pfx}-l-{v}-{key}           a label registered with lab(v, key, text) (hidden)
  queue(pfx, order)   the BFS queue as a strip: slot k = the k-th vertex ever enqueued; ids {pfx}-q-{k} (the
                      vertex enters), {pfx}-qx-{k} (it left: dimmed). The live queue is what is not dimmed.
  stack(pfx, run)     the DFS recursion stack: a slot per depth; id {pfx}-s-{v} (v is on the stack)
  parens(pfx, run)    the parenthesis string of a DFS run: token t = "(v" or "v)"; id {pfx}-p-{t}

Narration helpers: say(sub) speaks a subtitle that has vertex letters / BFS / DFS / d[v] in it (raises on anything it
does not know); S(sub, ...) = P(sub, say=say(sub), ...).
"""
import html as _html
import itertools
import math
import pathlib
import re
import sys
from collections import deque

import networkx as nx

from vid import P, show, hide

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
import graph_ref  # noqa: E402

INF = float("inf")


def esc(s):
    return _html.escape(str(s), quote=True)


# ====================================================================== speech
NAME = {"A": "אֵיי", "B": "בִּי", "C": "סִי", "D": "דִּי", "E": "אִי", "F": "אֶף", "G": "גִ'י", "H": "אֵייץ'",
        "I": "אַיי", "J": "גֵ'יי", "K": "קֵיי", "L": "אֶל", "M": "אֶם", "N": "אֶן", "P": "פִּי", "Q": "קְיוּ",
        "R": "אָר", "S": "אֶס", "T": "טִי", "U": "יוּ", "V": "וִי", "W": "דַאבֶּל יוּ", "X": "אֶקְס", "Y": "וַואי",
        "Z": "זֶד"}
LOW = {"s": "אֶס", "x": "אִקְס", "y": "וַואי", "z": "זֶד", "u": "יוּ", "v": "וִי", "w": "דַאבֶּל יוּ", "a": "אֵיי",
       "b": "בִּי", "c": "סִי", "n": "אֶן", "k": "קֵיי", "t": "טִי", "e": "אִי"}
ACR = {"BFS": "בִּי אֶף אֶס", "DFS": "דִּי אֶף אֶס", "DAG": "דָאג", "NIL": "נִיל"}
DIG = {"0": "אפס", "1": "אחת", "2": "שתיים", "3": "שלוש", "4": "ארבע", "5": "חמש", "6": "שש", "7": "שבע",
       "8": "שמונה", "9": "תשע"}


def vname(v):
    if v in NAME:
        return NAME[v]
    if v in LOW:
        return LOW[v]
    raise ValueError(f"no spoken name for vertex {v!r}")


def _sym(t):
    """a symbol inside TeX: a vertex letter, a lower-case variable, a digit string"""
    t = t.strip()
    if re.fullmatch(r"\d+", t):
        return t
    if t in NAME or t in LOW:
        return vname(t)
    raise ValueError(t)


def tex_say(t):
    """the TeX shapes the graph videos use; ValueError on anything else"""
    t = t.strip()
    t = t.replace(r"\,", " ").replace(r"\ ", " ")
    m = re.fullmatch(r"([A-Za-z])\s*\\to\s*([A-Za-z])", t)                 # X \to Y
    if m:
        return f"מ{_sym(m.group(1))} ל{_sym(m.group(2))}"
    m = re.fullmatch(r"([dfD])\[([A-Za-z])\]\s*=\s*(\d+)", t)               # d[X]=3
    if m:
        k = {"d": "דִּי", "f": "אֶף", "D": "דִּי"}[m.group(1)]
        return f"{k} של {_sym(m.group(2))} שווה {m.group(3)}"
    m = re.fullmatch(r"([dfD])\[([A-Za-z])\]", t)                           # d[X]
    if m:
        k = {"d": "דִּי", "f": "אֶף", "D": "דִּי"}[m.group(1)]
        return f"{k} של {_sym(m.group(2))}"
    m = re.fullmatch(r"\\pi\[([A-Za-z])\]\s*=\s*([A-Za-z])", t)
    if m:
        return f"פַּאי של {_sym(m.group(1))} שווה {_sym(m.group(2))}"
    m = re.fullmatch(r"\\pi\[([A-Za-z])\]", t)
    if m:
        return f"פַּאי של {_sym(m.group(1))}"
    m = re.fullmatch(r"\\delta\(([A-Za-z]),\s*([A-Za-z])\)", t)
    if m:
        return f"המרחק מ{_sym(m.group(1))} ל{_sym(m.group(2))}"
    if re.fullmatch(r"[A-Za-z]|\d+", t):
        return _sym(t)
    m = re.fullmatch(r"([A-Za-z](?:\s*,\s*[A-Za-z])+)", t)                 # A, B, C
    if m:
        parts = [vname(x.strip()) for x in t.split(",")]
        return ", ".join(parts)
    raise ValueError(t)


def say(sub):
    s = sub.replace("**", "")
    s = re.sub(r"<[^>]+>", "", s)

    def m(mm):
        try:
            return tex_say(mm.group(1))
        except ValueError:
            raise ValueError(f"w_graph_search.say: no spoken form for ${mm.group(1)}$ in: {sub}")
    s = re.sub(r"\$([^$]+)\$", m, s)
    for k, v in ACR.items():
        s = s.replace(k, v)
    s = re.sub(r"\b([A-Z])\b", lambda mm: vname(mm.group(1)), s)          # a bare vertex letter outside TeX
    if re.search(r"[A-Za-z]", s):
        raise ValueError(f"w_graph_search.say: Latin left in: {s}")
    return s


def S(sub, do=(), hold=0.0, say_=None):
    return P(sub, say=say_ if say_ is not None else say(sub), do=do, hold=hold)


def lst(vs, conj="ו"):
    """'$A$, $B$ ו-$C$' (subtitle)"""
    vs = [f"${v}$" for v in vs]
    if len(vs) == 1:
        return vs[0]
    return ", ".join(vs[:-1]) + f" {conj}-" + vs[-1]


# ====================================================================== independent algorithms (checks)
def adjacency(nodes, edges, directed, order=None):
    """neighbour lists: alphabetical, or order = {v: [neighbours in scan order]}"""
    adj = {v: set() for v in nodes}
    for u, v in edges:
        adj[u].add(v)
        if not directed:
            adj[v].add(u)
    if order:
        for v in nodes:
            assert sorted(order.get(v, sorted(adj[v]))) == sorted(adj[v]), (v, order.get(v))
        return {v: list(order.get(v, sorted(adj[v]))) for v in nodes}
    return {v: sorted(adj[v]) for v in nodes}


def my_bfs(adj, s):
    d, pi, order, q = {s: 0}, {s: None}, [s], deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in d:
                d[v], pi[v] = d[u] + 1, u
                order.append(v)
                q.append(v)
    return d, pi, order


def my_dfs(adj, roots, directed):
    disc, fin, pi, cls, order, clock = {}, {}, {}, {}, [], [0]
    state, used = {}, set()

    def visit(u):
        clock[0] += 1
        disc[u] = clock[0]
        order.append(u)
        state[u] = "g"
        for v in adj[u]:
            if not directed:
                if frozenset((u, v)) in used:
                    continue
                used.add(frozenset((u, v)))
            st = state.get(v, "w")
            if st == "w":
                cls[(u, v)] = "tree"
                pi[v] = u
                visit(v)
            elif st == "g":
                cls[(u, v)] = "back"
            else:
                cls[(u, v)] = "fwd" if disc[u] < disc[v] else "cross"
        clock[0] += 1
        fin[u] = clock[0]
        state[u] = "b"

    for r in roots:
        if r not in state:
            pi[r] = None
            visit(r)
    return disc, fin, pi, cls, order


def depth(pi):
    out = {}
    for v in pi:
        x, k = v, 0
        while pi[x] is not None:
            x, k = pi[x], k + 1
        out[v] = k
    return out


def nxg(nodes, edges, directed):
    g = nx.DiGraph() if directed else nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return g


# ====================================================================== the graph widget
class Graph:
    def __init__(self, pfx, nodes, edges, directed, pos, w=640, h=440, r=32, bend=None, lab_at=None, scale=1.0):
        self.pfx, self.nodes, self.edges, self.directed = pfx, list(nodes), list(edges), directed
        self.pos, self.w, self.h, self.r, self.scale = pos, w, h, r, scale
        self.bend = dict(bend or {})
        self.lab_at = dict(lab_at or {})          # {v: (dx, dy)} where the node's label sits (default below)
        self.labels = []                          # (v, key, text, cls)
        assert len(set(self.nodes)) == len(self.nodes)
        for u, v in self.edges:
            assert u in pos and v in pos and u != v, (u, v)
        assert len({self.key(u, v) for u, v in self.edges}) == len(self.edges), "duplicate edge"

    # ---- ids
    def key(self, u, v):
        return (u, v) if self.directed else tuple(sorted((u, v)))

    def eid(self, u, v, kind):
        a, b = self.key(u, v)
        return f"{self.pfx}-e-{a}-{b}-{kind}"

    def gray(self, v):
        return f"{self.pfx}-g-{v}"

    def black(self, v):
        return f"{self.pfx}-k-{v}"

    def ring(self, v):
        return f"{self.pfx}-c-{v}"

    def mark(self, v):
        return f"{self.pfx}-m-{v}"

    def lid(self, v, key):
        return f"{self.pfx}-l-{v}-{key}"

    def lab(self, v, key, text, cls="", dx=None, dy=None):
        """register a hidden label next to v; returns its id"""
        self.labels.append((v, key, text, cls, dx, dy))
        return self.lid(v, key)

    # ---- runs
    def spec(self, source=None, order=None):
        if order:          # graph_ref "given" order = edge list order: emit edges in each vertex's scan order
            seq, seen = [], set()
            adj = adjacency(self.nodes, self.edges, self.directed, order)
            rank = {v: i for i, v in enumerate(sorted(self.nodes))}
            # undirected "given" order sorts each vertex's list by edge index: the order must be consistent, checked below
            for u in sorted(self.nodes, key=lambda x: rank[x]):
                for v in adj[u]:
                    k = self.key(u, v)
                    if k not in seen:
                        seen.add(k)
                        seq.append(k)
            edges = [{"u": a, "v": b} for a, b in seq]
            nodes = list(self.nodes)
            sp = {"nodes": nodes, "edges": edges, "directed": self.directed, "order": "given"}
        else:
            sp = {"nodes": list(self.nodes), "edges": [{"u": a, "v": b} for a, b in self.edges],
                  "directed": self.directed}
        if source is not None:
            sp["source"] = source
        return sp

    def bfs(self, s, order=None):
        return BfsRun(self, s, order)

    def dfs(self, source=None, order=None):
        return DfsRun(self, source, order)

    # ---- drawing
    def _edge_path(self, u, v):
        (x1, y1), (x2, y2) = self.pos[u], self.pos[v]
        k = self.bend.get((u, v), self.bend.get((v, u), 0.0) * (-1 if self.directed else 1))
        if self.directed and (v, u) in self.edges and (u, v) not in self.bend and (v, u) not in self.bend:
            k = 0.18
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy) or 1
        ux, uy = dx / dist, dy / dist
        nx_, ny_ = uy, -ux
        cx, cy = (x1 + x2) / 2 + nx_ * k * dist, (y1 + y2) / 2 + ny_ * k * dist
        s1 = math.hypot(cx - x1, cy - y1) or 1
        s2 = math.hypot(cx - x2, cy - y2) or 1
        sx, sy = x1 + self.r * (cx - x1) / s1, y1 + self.r * (cy - y1) / s1
        end = self.r + (5 if self.directed else 0)
        ex, ey = x2 + end * (cx - x2) / s2, y2 + end * (cy - y2) / s2
        return f"M{sx:.1f},{sy:.1f} Q{cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}"

    def html(self, kinds=("tree", "back", "fwd", "cross", "hl", "dim"), hidden=False, cls=""):
        p, r = self.pfx, self.r
        W, H = self.w * self.scale, self.h * self.scale
        out = [f'<svg class="gs-graph {cls}{" h" if hidden else ""}" id="{p}" viewBox="0 0 {self.w} {self.h}" '
               f'width="{W:.0f}" height="{H:.0f}" direction="ltr"><defs>']
        for k, col in (("base", "#8d92bb"), ("tree", "#2dd4bf"), ("back", "#fb7185"), ("fwd", "#fbbf24"),
                       ("cross", "#38bdf8"), ("hl", "#fbbf24"), ("dim", "#3a3f63")):
            out.append(f'<marker id="{p}-ah-{k}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" '
                       f'markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
        out.append("</defs>")
        base, over = [], []
        for u, v in self.edges:
            d = self._edge_path(u, v)
            mk = (lambda k: f' marker-end="url(#{p}-ah-{k})"') if self.directed else (lambda k: "")
            base.append(f'<path d="{d}" class="gs-e"{mk("base")}/>')
            for k in kinds:
                over.append(f'<path id="{self.eid(u, v, k)}" d="{d}" class="gs-e-{k} h"{mk(k)}/>')
        nodes = []
        for v in self.nodes:
            x, y = self.pos[v]
            nodes.append(f'<circle id="{self.mark(v)}" cx="{x}" cy="{y}" r="{r + 13}" class="gs-mark h"/>'
                         f'<circle id="{self.ring(v)}" cx="{x}" cy="{y}" r="{r + 8}" class="gs-ring h"/>'
                         f'<circle cx="{x}" cy="{y}" r="{r}" class="gs-n"/>'
                         f'<circle id="{self.gray(v)}" cx="{x}" cy="{y}" r="{r}" class="gs-ng h"/>'
                         f'<circle id="{self.black(v)}" cx="{x}" cy="{y}" r="{r}" class="gs-nk h"/>'
                         f'<text x="{x}" y="{y + 1}" class="gs-nl">{esc(v)}</text>')
        labs = []
        for v, key, text, c, dx, dy in self.labels:
            x, y = self.pos[v]
            ddx, ddy = self.lab_at.get(v, (0, r + 26))
            if dx is not None:
                ddx = dx
            if dy is not None:
                ddy = dy
            labs.append(f'<text id="{self.lid(v, key)}" x="{x + ddx}" y="{y + ddy}" class="gs-lab {c} h">{esc(text)}</text>')
        out += base + over + nodes + labs + ["</svg>"]
        return "".join(out)


# ====================================================================== BFS
class BfsRun:
    """BFS from s. events (graph_ref): ["start", s], ["deq", u], ["edge", u, v], ["disc", v, u, d]"""

    def __init__(self, g, s, order=None):
        self.g, self.s = g, s
        adj = adjacency(g.nodes, g.edges, g.directed, order)
        d2, pi2, order2 = my_bfs(adj, s)
        if order and not g.directed:
            # graph_ref's "given" order is one global edge order, which cannot express every per-vertex order of an
            # undirected graph: the events come from the own BFS (checked against networkx below)
            self.events, q, seen = [["start", s]], deque([s]), {s}
            while q:
                u = q.popleft()
                self.events.append(["deq", u])
                for v in adj[u]:
                    self.events.append(["edge", u, v])
                    if v not in seen:
                        seen.add(v)
                        q.append(v)
                        self.events.append(["disc", v, u, d2[v]])
            self.order, self.d, self.pi = order2, d2, pi2
        else:
            G = graph_ref.build(g.spec(s, order))
            self.events, res = graph_ref.bfs(G)
            self.order = res["order"]
            self.d = {v: x for v, x in res["d"].items() if x is not None}
            self.pi = {v: res["pi"][v] for v in self.d}
            for u in g.nodes:                      # graph_ref scans exactly our neighbour order
                assert [v for v, _, _ in G["adj"][u]] == adj[u], (u, G["adj"][u], adj[u])
            assert (d2, pi2, order2) == (self.d, self.pi, self.order), (d2, pi2, order2, self.d, self.pi, self.order)
        ref = nx.single_source_shortest_path_length(nxg(g.nodes, g.edges, g.directed), s)
        assert ref == self.d
        self.adj = adj
        self.height = max(self.d.values())
        # dequeue blocks: (u, [discovered v...])
        self.blocks = []
        for e in self.events:
            if e[0] == "deq":
                self.blocks.append((e[1], []))
            elif e[0] == "disc":
                self.blocks[-1][1].append(e[1])
        self.pos_in_q = {v: k for k, v in enumerate(self.order)}

    def queue_at(self, nblocks):
        """queue content after nblocks dequeues were fully handled"""
        q = deque([self.s])
        for u, vs in self.blocks[:nblocks]:
            assert q.popleft() == u
            q.extend(vs)
        return list(q)

    def labels(self, key="d", fmt="d={}", pi=False):
        """register d labels (and π labels) on the graph; returns nothing"""
        for v in self.d:
            self.g.lab(v, key, fmt.format(self.d[v]), "gs-ld")

    def start_do(self, qpfx=None, key="d"):
        g = self.g
        do = show(g.gray(self.s), g.lid(self.s, key) if key else None)
        do = [x for x in do if x[1]]
        if qpfx:
            do += show(f"{qpfx}-q-0")
        return do

    def block_do(self, i, qpfx=None, key="d", prev_black=True):
        """the show/hide list of dequeue block i: previous u turns black, u gets the ring and leaves the queue,
        every discovered v turns gray, its tree edge and its label appear, it enters the queue"""
        g = self.g
        u, vs = self.blocks[i]
        do = []
        if i > 0:
            pu = self.blocks[i - 1][0]
            do += hide(g.ring(pu)) + (show(g.black(pu)) if prev_black else [])
        do += show(g.ring(u))
        if qpfx:
            do += show(f"{qpfx}-qx-{self.pos_in_q[u]}")
        for v in vs:
            do += show(g.gray(v), g.eid(u, v, "tree"))
            if key:
                do += show(g.lid(v, key))
            if qpfx:
                do += show(f"{qpfx}-q-{self.pos_in_q[v]}")
        return do

    def all_do(self, qpfx=None, key="d"):
        """the whole run at once (start, every dequeue, end): for a run shown in one phrase"""
        do = self.start_do(qpfx, key)
        for i in range(len(self.blocks)):
            do += self.block_do(i, qpfx, key)
        return do + self.end_do()

    def end_do(self):
        u = self.blocks[-1][0]
        return hide(self.g.ring(u)) + show(self.g.black(u))

    def block_sub(self, i):
        u, vs = self.blocks[i]
        if not vs:
            return f"שולפים את ${u}$: אין לו שכן לבן."
        lay = self.d[vs[0]]
        return f"שולפים את ${u}$ ומגלים את {lst(vs, 'ו')}: שכבה {lay}, והאב הוא ${u}$." if len(vs) > 1 else \
            f"שולפים את ${u}$ ומגלים את ${vs[0]}$: שכבה {lay}, והאב הוא ${u}$."

    def phrases(self, qpfx=None, key="d", subs=None, first=0, last=None):
        """one phrase per dequeue (blocks first..last-1); subs: {i: subtitle} overrides"""
        subs = subs or {}
        last = len(self.blocks) if last is None else last
        out, i = [], first
        while i < last:
            j = i
            while j + 1 < last and not self.blocks[i][1] and not self.blocks[j + 1][1] and i not in subs:
                j += 1
            if j > i:                                      # consecutive dequeues that discover nothing: one phrase
                us = [self.blocks[k][0] for k in range(i, j + 1)]
                do = []
                for k in range(i, j + 1):
                    do += self.block_do(k, qpfx, key)
                out.append(S(f"שולפים את {lst(us)}: לאף אחד מהם אין שכן לבן.", do=do))
            else:
                out.append(S(subs.get(i, self.block_sub(i)), do=self.block_do(i, qpfx, key)))
            i = j + 1
        return out


def queue(pfx, order, label="תור"):
    slots = "".join(f'<span class="gs-slot"><b id="{pfx}-q-{k}" class="gs-qv h">{esc(v)}</b>'
                    f'<i id="{pfx}-qx-{k}" class="gs-qx h"></i></span>' for k, v in enumerate(order))
    return (f'<div class="gs-strip" id="{pfx}" dir="ltr"><span class="gs-slab">{label}</span>'
            f'<span class="gs-head">⟵</span>{slots}</div>')


# ====================================================================== DFS
class DfsRun:
    """DFS over the whole graph: the outer loop takes `source` first (if given), then alphabetical order.
    events (graph_ref): ["disc", u, t], ["edge", u, v, kind], ["fin", u, t]  (kind tree/back/forward/cross)"""

    def __init__(self, g, source=None, order=None):
        self.g = g
        G = graph_ref.build(g.spec(source, order))
        self.events, res = graph_ref.dfs(G)
        self.disc, self.fin, self.pi = res["disc"], res["fin"], res["pi"]
        self.order = res["order"]
        adj = adjacency(g.nodes, g.edges, g.directed, order)
        for u in g.nodes:
            assert [v for v, _, _ in G["adj"][u]] == adj[u], (u, G["adj"][u], adj[u])
        roots = ([source] if source else []) + [v for v in (g.nodes if order else sorted(g.nodes)) if v != source]
        d2, f2, pi2, cls2, order2 = my_dfs(adj, roots, g.directed)
        assert (d2, f2, pi2, order2) == (self.disc, self.fin, self.pi, self.order)
        kindmap = {"tree": "tree", "back": "back", "forward": "fwd", "cross": "cross"}
        self.cls = {}
        for e in self.events:
            if e[0] == "edge":
                self.cls[g.key(e[1], e[2])] = kindmap[e[3]]
        assert self.cls == {g.key(u, v): k for (u, v), k in cls2.items()}, (self.cls, cls2)
        assert len(self.cls) == len(g.edges)
        # the classification agrees with the parenthesis rule (interval nesting)
        anc = lambda a, b: self.disc[a] <= self.disc[b] and self.fin[b] <= self.fin[a]     # a ancestor-or-self of b
        for e in self.events:
            if e[0] == "edge":
                u, v, k = e[1], e[2], kindmap[e[3]]
                if k in ("tree", "fwd"):
                    assert anc(u, v) and u != v
                elif k == "back":
                    assert anc(v, u)
                else:
                    assert self.fin[v] < self.disc[u]
        # networkx: the DFS forest has the same trees (reachability inside each tree) and back edge <=> cycle
        gx = nxg(g.nodes, g.edges, g.directed)
        if g.directed:
            assert nx.is_directed_acyclic_graph(gx) == ("back" not in self.cls.values())
        self.adj = adj
        self.roots = [v for v in self.order if self.pi[v] is None]
        self.depth = depth(self.pi)
        self.height = max(self.depth.values())
        self.topo = sorted(g.nodes, key=lambda v: -self.fin[v])
        self.T = 2 * len(g.nodes)

    def kind(self, u, v):
        return self.cls[self.g.key(u, v)]

    def time_labels(self, kd="d", kf="f", dxd=-4, dxf=4):
        """d label ("1/") and f label ("8") under each node"""
        g = self.g
        for v in g.nodes:
            ddx, ddy = g.lab_at.get(v, (0, g.r + 26))
            g.lab(v, kd, f"{self.disc[v]}/", "gs-ld gs-end", dx=ddx + dxd, dy=ddy)
            g.lab(v, kf, f"{self.fin[v]}", "gs-lf gs-start", dx=ddx + dxf, dy=ddy)

    def ev_do(self, e, kd="d", kf="f", spfx=None, ppfx=None, edges=("tree", "back", "fwd", "cross")):
        g, do = self.g, []
        if e[0] == "disc":
            u = e[1]
            do += show(g.gray(u), g.ring(u))
            if self.pi[u] is not None:
                do += hide(g.ring(self.pi[u]))
            if kd:
                do += show(g.lid(u, kd))
            if spfx:
                do += show(f"{spfx}-s-{u}")
            if ppfx:
                do += show(f"{ppfx}-p-{e[2]}")
        elif e[0] == "fin":
            u = e[1]
            do += show(g.black(u)) + hide(g.ring(u))
            if self.pi[u] is not None:
                do += show(g.ring(self.pi[u]))
            if kf:
                do += show(g.lid(u, kf))
            if spfx:
                do += hide(f"{spfx}-s-{u}")
            if ppfx:
                do += show(f"{ppfx}-p-{e[2]}")
        elif e[0] == "edge":
            k = {"tree": "tree", "back": "back", "forward": "fwd", "cross": "cross"}[e[3]]
            if k in edges:
                do += show(g.eid(e[1], e[2], k))
        return do

    def groups(self, narrate=("back", "forward", "cross")):
        """split the events into narration groups: a run of discoveries (with their tree edges), a run of
        finishes, or one narrated non-tree edge. Silent non-tree edges join the group around them."""
        groups, cur, kind = [], [], None
        for e in self.events:
            if e[0] == "edge" and e[3] != "tree" and e[3] in narrate:
                if cur:
                    groups.append((kind, cur))
                groups.append(("edge", [e]))
                cur, kind = [], None
                continue
            k = {"disc": "disc", "fin": "fin"}.get(e[0])
            if k is None:                      # tree edge (or a silent non-tree edge): goes with the next discovery
                cur.append(e)
                continue
            if k == "disc" and self.pi[e[1]] is None and cur:          # a new root starts its own group
                groups.append((kind, cur))
                cur, kind = [], None
            if kind not in (None, k) or len([x for x in cur if x[0] in ("disc", "fin")]) >= 3:
                tail = []
                while cur and cur[-1][0] == "edge":       # a tree edge belongs to the discovery after it
                    tail.insert(0, cur.pop())
                groups.append((kind, cur))
                cur = tail
            cur.append(e)
            kind = k
        if cur:
            groups.append((kind, cur))
        return groups

    def group_sub(self, kind, evs):
        if kind == "edge":
            _, u, v, k = evs[0]
            arrow = f"${u}\\to {v}$" if self.g.directed else f"${u}$–${v}$"
            if k == "back":
                return f"הצלע {arrow}: ${v}$ אפור, ולכן זו צלע **אחורה**."
            if k == "forward":
                return f"הצלע {arrow}: ${v}$ שחור והתגלה אחרי ${u}$, ולכן זו צלע **קדימה**."
            return f"הצלע {arrow}: ${v}$ שחור והתגלה לפני ${u}$, ולכן זו צלע **חוצה**."
        items = [e for e in evs if e[0] in ("disc", "fin")]
        if kind == "disc":
            pre = ""
            if self.pi[items[0][1]] is None and items[0][1] != self.order[0]:
                pre = f"${items[0][1]}$ עדיין לבן: עץ חדש. "
            if len(items) == 1:
                return pre + f"מגלים את ${items[0][1]}$ בזמן {items[0][2]}."
            parts = [f"את ${e[1]}$ בזמן {e[2]}" for e in items]
            return pre + "מגלים " + ", ".join(parts[:-1]) + ", ו" + parts[-1] + "."
        if len(items) == 1:
            return f"${items[0][1]}$ מסתיים בזמן {items[0][2]}."
        parts = [f"את ${e[1]}$ בזמן {e[2]}" for e in items]
        return "מסיימים " + ", ".join(parts[:-1]) + ", ו" + parts[-1] + "."

    def phrases(self, kd="d", kf="f", spfx=None, ppfx=None, narrate=("back", "forward", "cross"), subs=None,
                extra=None, edges=("tree", "back", "fwd", "cross")):
        """auto-narrated run; subs {group index: subtitle}, extra {group index: [more actions]}"""
        subs, extra = subs or {}, extra or {}
        out = []
        for i, (kind, evs) in enumerate(self.groups(narrate)):
            do = []
            for e in evs:
                do += self.ev_do(e, kd, kf, spfx, ppfx, edges)
            do += extra.get(i, [])
            out.append(S(subs.get(i, self.group_sub(kind, evs)), do=do))
        return out


def stack(pfx, run, label="מחסנית"):
    """recursion stack: a slot per depth (deepest = rightmost); every vertex sits at its depth"""
    by_depth = {}
    for v in run.order:
        by_depth.setdefault(run.depth[v], []).append(v)
    slots = []
    for dpt in range(run.height + 1):
        items = "".join(f'<b id="{pfx}-s-{v}" class="gs-qv h">{esc(v)}</b>' for v in by_depth.get(dpt, []))
        slots.append(f'<span class="gs-slot">{items}</span>')
    return (f'<div class="gs-strip" id="{pfx}" dir="ltr"><span class="gs-slab">{label}</span>{"".join(slots)}'
            f'<span class="gs-head">⟵ ראש</span></div>')


def parens(pfx, run):
    toks = {}
    for v in run.g.nodes:
        toks[run.disc[v]] = f"({v}"
        toks[run.fin[v]] = f"{v})"
    spans = "".join(f'<span id="{pfx}-p-{t}" class="gs-par h"><i>{t}</i>{esc(toks[t])}</span>'
                    for t in range(1, run.T + 1))
    return f'<div class="gs-parens" id="{pfx}" dir="ltr">{spans}</div>'


# ====================================================================== small tables
def table(pfx, head, rows, hidden=True, cls=""):
    """LTR table; ids {pfx}-r{i} row (hidden), {pfx}-c{i}-{j} cell highlight"""
    hd = "".join(f"<th>{c}</th>" for c in head)
    body = []
    for i, r in enumerate(rows):
        cells = "".join(f'<td><i id="{pfx}-c{i}-{j}" class="cell-hi h"></i>{c}</td>' for j, c in enumerate(r))
        body.append(f'<tr id="{pfx}-r{i}"{" class=\"h\"" if hidden else ""}>{cells}</tr>')
    return (f'<table class="delta gs-tab {cls}" id="{pfx}" dir="ltr"><thead><tr>{hd}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table>')


def legend(pfx, kinds, hidden=True):
    names = {"tree": "עץ", "back": "אחורה", "fwd": "קדימה", "cross": "חוצה"}
    items = "".join(f'<span id="{pfx}-{k}" class="gs-lg{" h" if hidden else ""}"><i class="gs-sw gs-sw-{k}"></i>'
                    f'{names[k]}</span>' for k in kinds)
    return f'<div class="gs-legend" id="{pfx}">{items}</div>'


# ====================================================================== brute force helpers
def all_graphs(n, directed):
    """every simple graph on vertices 0..n-1 (labelled)"""
    V = list(range(n))
    pairs = list(itertools.permutations(V, 2)) if directed else list(itertools.combinations(V, 2))
    for mask in range(1 << len(pairs)):
        yield V, [pairs[i] for i in range(len(pairs)) if mask >> i & 1]


def all_orders(adj):
    """every neighbour-order assignment of an adjacency dict"""
    keys = list(adj)
    for combo in itertools.product(*[list(itertools.permutations(adj[k])) for k in keys]):
        yield {k: list(c) for k, c in zip(keys, combo)}


# ====================================================================== DFS intervals [d, f] on a time axis
def intervals(pfx, rows, T, unit=46, row=50, hidden=True):
    """rows: [(v, d, f)] drawn in the given order; ids {pfx}-b-{v} the bar (hidden), {pfx}-h-{v} amber frame"""
    left = 60
    W, H = left + T * unit + 20, row * len(rows) + 50
    out = [f'<svg class="gs-iv" id="{pfx}" viewBox="0 0 {W} {H}" width="{W}" height="{H}" direction="ltr">']
    for t in range(1, T + 1):
        x = left + (t - 0.5) * unit
        out.append(f'<line x1="{x}" y1="6" x2="{x}" y2="{H - 34}" class="gs-iv-grid"/>'
                   f'<text x="{x}" y="{H - 10}" class="gs-iv-t">{t}</text>')
    for i, (v, d, f) in enumerate(rows):
        y = 10 + i * row
        x1, x2 = left + (d - 1) * unit + 4, left + f * unit - 4
        out.append(f'<text x="{left - 14}" y="{y + row / 2 - 4}" class="gs-iv-n">{esc(v)}</text>')
        out.append(f'<g id="{pfx}-b-{v}"{" class=\"h\"" if hidden else ""}><rect x="{x1}" y="{y}" width="{x2 - x1}" '
                   f'height="{row - 14}" rx="9" class="gs-iv-bar"/>'
                   f'<text x="{x1 + 10}" y="{y + row / 2 - 6}" class="gs-iv-l gs-start">{d}</text>'
                   f'<text x="{x2 - 10}" y="{y + row / 2 - 6}" class="gs-iv-l gs-end">{f}</text></g>')
        out.append(f'<rect id="{pfx}-h-{v}" x="{x1 - 4}" y="{y - 4}" width="{x2 - x1 + 8}" height="{row - 6}" rx="11" '
                   f'class="gs-iv-hi h"/>')
    out.append("</svg>")
    return "".join(out)


def unhide(html, ids):
    """drop the start-hidden class of the given ids (a final state drawn from the start)"""
    for i in ids:
        html, n = re.subn(r'(id="' + re.escape(i) + r'"[^>]*?class="[^"]*?) h(")', r"\1\2", html)
        if n == 0:
            html, n = re.subn(r'(id="' + re.escape(i) + r'"[^>]*?) class="h"', r"\1", html)
        assert n == 1, i
    return html


def final_dfs_html(g, run, kinds=("tree",)):
    """the graph after the run: black nodes, time labels, the edges of the given kinds"""
    ids = [g.black(v) for v in g.nodes] + [g.lid(v, k) for v in g.nodes for k in ("d", "f")]
    ids += [g.eid(u, v, run.kind(u, v)) for u, v in g.edges if run.kind(u, v) in kinds]
    return unhide(g.html(kinds=tuple(sorted(set(kinds) | {"hl"}))), ids)
