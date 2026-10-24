"use strict";
/* Step-through graph-algorithm visualizer (window.Graph) -- algorithms-1 extra, app-local (not part of the
   factory template). Ported from the Algorithms 2 site's static widgets (public/visualizations/bfs, dfs, scc,
   topological-sort, dijkstra, mst): same white/gray/black node colours, tree/back/forward/cross edge colours,
   queue strip, recursion stack, d/pi and d/f tables, prev/next controls; reimplemented as one data-driven,
   dependency-free widget with Hebrew labels.

   A graph spec (tools/RAW_SCHEMA.md, "Graphs"):
     { "nodes": ["A", {"id":"B","x":120,"y":40}, ...],      ids (strings or numbers); x/y all-or-none (else auto layout)
       "edges": [{"u":"A","v":"B","w":3}, ...],              w optional (required by dijkstra / prim / kruskal)
       "directed": true,
       "algo": "bfs"|"dfs"|"topo"|"scc"|"dijkstra"|"prim"|"kruskal",   omitted = a plain drawing
       "source": "A",                                        bfs / dijkstra / prim start; dfs/topo/scc: first root
       "order": "alpha"|"given",                             neighbour + main-loop order (default alpha, natural sort)
       "layout": "circle"|"layers", "caption": "text",
       "expect": {...}                                       stored answers, checked by tools/validate.py }
   Conventions (CLRS, as in the course): the DFS main loop and every adjacency list run in alphabetical order
   ("1" < "2" < "10" for numeric ids); ties in extract-min go to the earlier vertex; Kruskal ties by weight,
   then by endpoint names; topological sort = decreasing DFS finish time; SCC = Kosaraju (DFS on G, then DFS on
   G^T in decreasing f). In an undirected DFS an edge is classified on its first examination (tree or back).

   API: Graph.compute(spec) -> {frames, events, result}   (throws on an invalid spec)
        Graph.check(spec)   -> [problem strings] (shape, algorithm preconditions, expect)
        Graph.figure(spec, {locked|static}) -> host HTML; Graph.hydrate(rootEl) mounts every .graph-fig[data-graph]
        Graph.mount(el, spec, opts); Graph.unlock(el) turns a locked drawing into the step-through
        Graph.answerOf(spec, key) -> the value a step's `key` names (validate.py)
   Loadable in Node (module.exports) for tools/test_graph.js and tools/graph_check.js. */
(function (root) {
  const ALGOS = ["bfs", "dfs", "topo", "scc", "dijkstra", "prim", "kruskal"];
  const SPEC_KEYS = ["nodes", "edges", "directed", "algo", "source", "order", "layout", "caption", "expect"];
  const EXPECT_KEYS = {
    bfs: ["order", "d", "pi"], dfs: ["order", "disc", "fin", "pi", "classes"],
    topo: ["order", "disc", "fin", "pi", "classes", "topo"], scc: ["order", "disc", "fin", "classes", "scc"],
    dijkstra: ["d", "pi", "order"], prim: ["mst", "weight", "pi", "order"], kruskal: ["mst", "weight"] };
  const MAX_NODES = 16;
  const INF = Infinity;
  const NUM = /^-?\d+(\.\d+)?$/;
  function natCmp(a, b) {
    const na = NUM.test(a), nb = NUM.test(b);
    if (na && nb) { const d = parseFloat(a) - parseFloat(b); if (d) return d < 0 ? -1 : 1; }
    else if (na !== nb) return na ? -1 : 1;
    return a < b ? -1 : a > b ? 1 : 0;
  }
  const isNum = x => typeof x === "number" && isFinite(x);
  const nid = n => String(n && typeof n === "object" ? n.id : n);

  /* ================================ spec -> graph ================================ */
  function shapeProblems(spec) {
    const P = [];
    if (!spec || typeof spec !== "object" || Array.isArray(spec)) return ["graph must be an object"];
    for (const k of Object.keys(spec)) if (!SPEC_KEYS.includes(k)) P.push(`unknown graph key "${k}"`);
    if (typeof spec.directed !== "boolean") P.push("directed must be true or false");
    if (!Array.isArray(spec.nodes) || !spec.nodes.length) { P.push("nodes must be a non-empty list"); return P; }
    if (spec.nodes.length > MAX_NODES) P.push(`at most ${MAX_NODES} nodes`);
    const ids = new Set();
    let withXY = 0;
    for (const n of spec.nodes) {
      const o = n && typeof n === "object" ? n : { id: n };
      if (Array.isArray(n)) { P.push("a node is an id or {id, x?, y?}"); continue; }
      for (const k of Object.keys(o)) if (!["id", "x", "y"].includes(k)) P.push(`node ${o.id}: unknown key "${k}"`);
      if (!(typeof o.id === "string" && o.id.trim()) && !isNum(o.id)) { P.push("node id must be a non-blank string or a number"); continue; }
      const id = String(o.id);
      if (ids.has(id)) P.push(`duplicate node ${id}`);
      ids.add(id);
      if ("x" in o || "y" in o) { if (!isNum(o.x) || !isNum(o.y)) P.push(`node ${id}: x and y must both be numbers`); else withXY++; }
    }
    if (withXY && withXY !== spec.nodes.length) P.push("give x/y for every node or for none");
    if (!Array.isArray(spec.edges)) { P.push("edges must be a list"); return P; }
    const seen = new Set();
    spec.edges.forEach((e, i) => {
      if (!e || typeof e !== "object" || Array.isArray(e)) { P.push(`edges[${i}] must be {u, v, w?}`); return; }
      for (const k of Object.keys(e)) if (!["u", "v", "w"].includes(k)) P.push(`edges[${i}]: unknown key "${k}"`);
      const u = String(e.u), v = String(e.v);
      if (!ids.has(u) || !ids.has(v)) { P.push(`edges[${i}] ${u}-${v}: endpoint is not a node`); return; }
      if ("w" in e && !isNum(e.w)) P.push(`edges[${i}] ${u}-${v}: w must be a number`);
      if (u === v && !spec.directed) P.push(`edges[${i}]: self-loop ${u}-${u} in an undirected graph`);
      const k = spec.directed ? u + "\u0001" + v : [u, v].sort().join("\u0001");
      if (seen.has(k)) P.push(`edges[${i}] ${u}-${v}: duplicate edge`);
      seen.add(k);
    });
    if ("algo" in spec && !ALGOS.includes(spec.algo)) P.push(`algo must be one of ${ALGOS.join(", ")}`);
    if ("order" in spec && !["alpha", "given"].includes(spec.order)) P.push('order must be "alpha" or "given"');
    if ("layout" in spec && !["circle", "layers"].includes(spec.layout)) P.push('layout must be "circle" or "layers"');
    if ("caption" in spec && typeof spec.caption !== "string") P.push("caption must be a string");
    if ("source" in spec && !ids.has(String(spec.source))) P.push(`source ${spec.source} is not a node`);
    const a = spec.algo;
    if (["dijkstra", "prim", "kruskal"].includes(a) && spec.edges.some(e => e && !isNum(e.w))) P.push(`${a} needs a weight w on every edge`);
    if (a === "dijkstra" && spec.edges.some(e => e && isNum(e.w) && e.w < 0)) P.push("dijkstra needs non-negative weights");
    if (["prim", "kruskal"].includes(a) && spec.directed) P.push(`${a} needs an undirected graph`);
    if (["topo", "scc"].includes(a) && !spec.directed) P.push(`${a} needs a directed graph`);
    if ("expect" in spec) {
      if (!a) P.push("expect needs an algo");
      else if (!spec.expect || typeof spec.expect !== "object" || Array.isArray(spec.expect)) P.push("expect must be an object");
      else for (const k of Object.keys(spec.expect)) if (!EXPECT_KEYS[a].includes(k)) P.push(`expect.${k} is not an output of ${a} (${EXPECT_KEYS[a].join(", ")})`);
    }
    return P;
  }

  function build(spec) {
    const P = shapeProblems(spec);
    if (P.length) throw new Error("invalid graph: " + P.join("; "));
    const given = spec.nodes.map(nid);
    const alpha = (spec.order || "alpha") === "alpha";
    const ids = alpha ? given.slice().sort(natCmp) : given;
    const rank = {}; ids.forEach((id, i) => rank[id] = i);
    const edges = spec.edges.map((e, i) => ({ u: String(e.u), v: String(e.v), w: isNum(e.w) ? e.w : null, i }));
    const adj = {}, radj = {};
    ids.forEach(id => { adj[id] = []; radj[id] = []; });
    for (const e of edges) {
      adj[e.u].push({ v: e.v, w: e.w, e: e.i });
      if (spec.directed) radj[e.v].push({ v: e.u, w: e.w, e: e.i });
      else if (e.u !== e.v) adj[e.v].push({ v: e.u, w: e.w, e: e.i });
    }
    const sortAdj = l => l.sort((a, b) => alpha ? (natCmp(a.v, b.v) || a.e - b.e) : a.e - b.e);
    ids.forEach(id => { sortAdj(adj[id]); sortAdj(radj[id]); });
    const pos = {};
    spec.nodes.forEach(n => { if (n && typeof n === "object" && isNum(n.x)) pos[String(n.id)] = { x: n.x, y: n.y }; });
    const source = spec.source != null ? String(spec.source) : ids[0];
    return { ids, rank, edges, adj, radj, directed: !!spec.directed, algo: spec.algo || null, source,
      alpha, pos: Object.keys(pos).length ? pos : null, layout: spec.layout || "circle", caption: spec.caption || "" };
  }

  /* ================================ algorithms -> frames + events ================================ */
  const L = s => `<bdi dir="ltr">${esc(s)}</bdi>`;
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
  const fmt = x => x === INF || x == null ? "∞" : String(x);

  function runner(G) {
    const st = { color: {}, d: {}, pi: {}, f: {}, key: {}, comp: {}, queue: [], stack: [], order: [], cls: {}, topo: [],
      mst: [], skip: [], S: [], sets: null, sorted: null, idx: 0, cur: null, edge: null, from: null, phase: 1, flip: false };
    G.ids.forEach(v => { st.color[v] = "w"; st.pi[v] = null; });
    const frames = [], events = [];
    const clone = o => Array.isArray(o) ? o.map(x => Array.isArray(x) ? x.slice() : x) : Object.assign({}, o);
    function snap(t, n) {
      const fr = { t, n };
      for (const k of Object.keys(st)) fr[k] = st[k] && typeof st[k] === "object" ? clone(st[k]) : st[k];
      frames.push(fr);
    }
    return { st, frames, events, snap };
  }
  const arrow = G => G.directed ? "→" : "–";
  const edgeName = (G, u, v) => u + arrow(G) + v;

  function bfs(G) {
    const R = runner(G), { st, snap, events } = R, s = G.source;
    G.ids.forEach(v => st.d[v] = INF);
    st.d[s] = 0; st.color[s] = "g"; st.queue.push(s); st.order.push(s);
    events.push(["start", s]);
    snap("אתחול", `כל הקודקודים לבנים ו-${L("d = ∞")}. מקור החיפוש ${L(s)}: ${L(`d[${s}] = 0`)}, צובעים אותו באפור ומכניסים לתור.`);
    let prev = null;
    while (st.queue.length) {
      const u = st.queue.shift();
      if (prev) st.color[prev] = "b";
      prev = u; st.cur = u; st.edge = null;
      events.push(["deq", u]);
      const nb = G.adj[u].map(a => a.v);
      snap(`מוציאים את ${L(u)} מהתור`, nb.length ? `סורקים את השכנים של ${L(u)} לפי הסדר: ${L(nb.join(", "))}.` : `ל-${L(u)} אין שכנים.`);
      for (const a of G.adj[u]) {
        const v = a.v; st.edge = a.e; st.from = u;
        events.push(["edge", u, v]);
        if (st.color[v] === "w") {
          st.color[v] = "g"; st.d[v] = st.d[u] + 1; st.pi[v] = u; st.queue.push(v); st.order.push(v); st.cls[a.e] = "tree";
          events.push(["disc", v, u, st.d[v]]);
          snap(`הקשת ${L(edgeName(G, u, v))}: ${L(v)} לבן, מגלים אותו`,
            `${L(`d[${v}] = d[${u}] + 1 = ${st.d[v]}`)} ו-${L(`π[${v}] = ${u}`)}. צובעים את ${L(v)} באפור ומכניסים לסוף התור.`);
        } else {
          snap(`הקשת ${L(edgeName(G, u, v))}: ${L(v)} כבר התגלה`,
            `${L(v)} ${st.color[v] === "g" ? "אפור (מחכה בתור)" : "שחור"}, ולכן לא משנים דבר.`);
        }
      }
    }
    if (prev) st.color[prev] = "b";
    st.cur = null; st.edge = null;
    const unreached = G.ids.filter(v => st.d[v] === INF);
    snap("סיום: התור ריק", `${L("d[v]")} הוא מספר הקשתות המינימלי במסלול מ-${L(s)} אל ${L("v")}, וקשתות ה-${L("π")} יוצרות את עץ ה-BFS.` +
      (unreached.length ? ` הקודקודים ${L(unreached.join(", "))} אינם ישיגים ונשארים עם ${L("d = ∞")}.` : ""));
    const result = { order: st.order.slice(), d: Object.assign({}, st.d), pi: Object.assign({}, st.pi),
      tree: G.ids.filter(v => st.pi[v] != null).map(v => [st.pi[v], v]) };
    return { frames: R.frames, events, result };
  }

  const KIND_HE = { tree: "קשת עץ", back: "קשת אחורה", fwd: "קשת קדימה", cross: "קשת חוצה" };
  const KIND_EN = { tree: "tree", back: "back", fwd: "forward", cross: "cross" };

  /* DFS (also the first pass of topo / scc). mode: "dfs" | "topo" | "scc" */
  function dfsPass(G, R, mode) {
    const { st, snap, events } = R;
    const piEdge = {};
    let time = 0;
    const mainOrder = [G.source].concat(G.ids.filter(v => v !== G.source));
    const pre = mode === "scc" ? "שלב 1: " : "";
    snap(pre + "אתחול", `כל הקודקודים לבנים, ${L("time = 0")}. הלולאה הראשית עוברת על הקודקודים לפי הסדר ${L(mainOrder.join(", "))}, והשכנים נסרקים לפי סדר אלפביתי.`.replace("לפי סדר אלפביתי", G.alpha ? "לפי סדר אלפביתי" : "לפי סדר הקשתות בשאלה"));
    function visit(u, isRoot) {
      time++; st.d[u] = time; st.color[u] = "g"; st.stack.push(u); st.order.push(u); st.cur = u; st.edge = null;
      events.push(["disc", u, time]);
      snap(`${pre}מגלים את ${L(u)}`, `${L(`d[${u}] = ${time}`)}. ${L(u)} נצבע באפור ונכנס למחסנית` +
        (isRoot ? `, והוא שורש של עץ חדש ביער ה-DFS.` : "."));
      for (const a of G.adj[u]) {
        const v = a.v;
        if (!G.directed && (a.e === piEdge[u] || st.cls[a.e])) continue;   // the tree edge back up / already classified
        st.cur = u; st.edge = a.e; st.from = u;
        let k;
        if (st.color[v] === "w") k = "tree";
        else if (st.color[v] === "g") k = "back";
        else k = st.d[u] < st.d[v] ? "fwd" : "cross";
        st.cls[a.e] = k;
        events.push(["edge", u, v, KIND_EN[k]]);
        const en = L(edgeName(G, u, v));
        if (k === "tree") {
          st.pi[v] = u; piEdge[v] = a.e;
          snap(`${pre}הקשת ${en}: קשת עץ`, `${L(v)} לבן: ${L(`π[${v}] = ${u}`)}, ונכנסים אליו ברקורסיה.`);
          visit(v, false);
          st.cur = u; st.edge = null;
        } else if (k === "back") {
          snap(`${pre}הקשת ${en}: קשת אחורה`, `${L(v)} אפור, כלומר עדיין במחסנית: הקשת חוזרת אל אב קדמון ויש מעגל.`);
        } else if (k === "fwd") {
          snap(`${pre}הקשת ${en}: קשת קדימה`, `${L(v)} כבר שחור ו-${L(`d[${u}] = ${st.d[u]} < d[${v}] = ${st.d[v]}`)}: ${L(v)} צאצא של ${L(u)} שכבר הסתיים.`);
        } else {
          snap(`${pre}הקשת ${en}: קשת חוצה`, `${L(v)} כבר שחור ו-${L(`d[${v}] = ${st.d[v]} < d[${u}] = ${st.d[u]}`)}: ${L(v)} אינו צאצא של ${L(u)}.`);
        }
      }
      time++; st.f[u] = time; st.color[u] = "b"; st.stack.pop(); st.cur = u; st.edge = null;
      events.push(["fin", u, time]);
      if (mode === "topo") st.topo.unshift(u);
      snap(`${pre}${L(u)} הסתיים`, `כל השכנים של ${L(u)} נסרקו: ${L(`f[${u}] = ${time}`)}, ${L(u)} נצבע בשחור ויוצא מהמחסנית.` +
        (mode === "topo" ? ` מוסיפים את ${L(u)} לראש הרשימה.` : ""));
    }
    for (const u of mainOrder) if (st.color[u] === "w") visit(u, true);
    st.cur = null; st.edge = null;
  }
  function dfsResult(G, st) {
    const classes = {};
    for (const e of G.edges) if (st.cls[e.i]) classes[e.u + "-" + e.v] = KIND_EN[st.cls[e.i]];
    return { order: st.order.slice(), disc: Object.assign({}, st.d), fin: Object.assign({}, st.f), pi: Object.assign({}, st.pi), classes };
  }
  function dfs(G) {
    const R = runner(G);
    dfsPass(G, R, "dfs");
    const back = Object.values(R.st.cls).filter(k => k === "back").length;
    R.snap("סיום", `לכל קודקוד יש זמן גילוי ${L("d")} וזמן סיום ${L("f")}, והקטעים ${L("[d, f]")} מקוננים או זרים (משפט הסוגריים). ` +
      (back ? `נמצאו ${L(back)} קשתות אחורה, ולכן יש בגרף מעגל.` : "אין קשתות אחורה, ולכן אין בגרף מעגל."));
    return { frames: R.frames, events: R.events, result: dfsResult(G, R.st) };
  }
  function topo(G) {
    const R = runner(G);
    dfsPass(G, R, "topo");
    const cyc = Object.values(R.st.cls).includes("back");
    R.snap("סיום", cyc ? `נמצאה קשת אחורה: הגרף אינו חסר מעגלים ואין לו מיון טופולוגי.`
      : `הרשימה לפי זמן סיום יורד היא מיון טופולוגי: ${L(R.st.topo.join(", "))}.`);
    const res = dfsResult(G, R.st); res.topo = R.st.topo.slice(); res.acyclic = !cyc;
    return { frames: R.frames, events: R.events, result: res };
  }
  function scc(G) {
    const R = runner(G), { st, snap, events } = R;
    dfsPass(G, R, "scc");
    const first = dfsResult(G, st);
    const byF = G.ids.slice().sort((a, b) => st.f[b] - st.f[a]);
    G.ids.forEach(v => st.color[v] = "w");
    st.phase = 2; st.flip = true; st.cls = {}; st.stack = []; st.second = byF.slice();
    snap("שלב 2: הגרף המשוחלף", `הופכים את כיוון כל הקשתות (${L("Gᵀ")}) ומריצים DFS שני, שבו הלולאה הראשית עוברת לפי ${L("f")} יורד: ${L(byF.join(", "))}.`);
    let k = 0;
    const comps = [];
    function visit2(u) {
      st.color[u] = "g"; st.comp[u] = k; comps[k - 1].push(u);
      for (const a of G.radj[u]) {
        const v = a.v;
        if (st.color[v] !== "w") continue;
        st.cur = v; st.edge = a.e; st.from = u; st.cls[a.e] = "tree";
        events.push(["tree2", u, v]);
        snap(`${L(v)} מצטרף לרכיב ${L(k)}`, `הקשת ${L(u + "→" + v)} בגרף המשוחלף מגיעה אל ${L(v)} הלבן.`);
        visit2(v);
      }
      st.color[u] = "b";
    }
    for (const u of byF) {
      if (st.color[u] !== "w") continue;
      k++; comps.push([]);
      st.cur = u; st.edge = null;
      events.push(["root", u, k]);
      st.color[u] = "g"; st.comp[u] = k;
      snap(`רכיב ${L(k)} מתחיל ב-${L(u)}`, `${L(u)} הוא הלבן בעל ${L("f")} הגדול ביותר שנותר. כל מה שה-DFS בגרף המשוחלף יגיע אליו ממנו שייך לרכיב ${L(k)}.`);
      st.color[u] = "w"; delete st.comp[u];
      visit2(u);
      st.cur = null; st.edge = null;
      snap(`רכיב ${L(k)} הושלם`, `הרכיב הקשיר היטב: ${L("{" + comps[k - 1].join(", ") + "}")}.`);
    }
    snap("סיום", `בגרף ${L(k)} רכיבים קשירים היטב, ומצאנו אותם בסדר מיון טופולוגי של גרף הרכיבים.`);
    const res = Object.assign(first, { scc: comps.map(c => c.slice()), comp: Object.assign({}, st.comp) });
    return { frames: R.frames, events, result: res };
  }

  /* extract-min over the vertices not yet closed: smallest value, ties to the earlier vertex in G.ids */
  function extractMin(G, val, closed) {
    let best = null;
    for (const v of G.ids) if (!closed[v] && (best === null || val[v] < val[best])) best = v;
    return best;
  }
  function dijkstra(G) {
    const R = runner(G), { st, snap, events } = R, s = G.source, closed = {};
    G.ids.forEach(v => st.d[v] = INF);
    st.d[s] = 0;
    const pq = () => G.ids.filter(v => !closed[v] && st.d[v] < INF).sort((a, b) => st.d[a] - st.d[b] || G.rank[a] - G.rank[b]);
    st.queue = pq(); G.ids.forEach(v => st.color[v] = st.d[v] < INF ? "g" : "w");
    snap("אתחול", `${L(`d[${s}] = 0`)} ולכל שאר הקודקודים ${L("d = ∞")}. כל הקודקודים בתור העדיפויות, וקבוצת הסגורים ${L("S")} ריקה.`);
    const order = [];
    for (;;) {
      const u = extractMin(G, st.d, closed);
      if (u === null) break;
      if (st.d[u] === INF) {
        st.cur = null; st.edge = null;
        snap("שאר הקודקודים אינם ישיגים", `בתור נשארו רק קודקודים עם ${L("d = ∞")}: ${L(G.ids.filter(v => !closed[v]).join(", "))}.`);
        break;
      }
      closed[u] = true; st.S.push(u); order.push(u); st.color[u] = "b"; st.cur = u; st.edge = null; st.queue = pq();
      events.push(["extract", u, st.d[u]]);
      snap(`מוציאים את ${L(u)} מהתור, ${L(`d[${u}] = ${st.d[u]}`)}`, `זה הקודקוד עם ${L("d")} הקטן ביותר בתור, ולכן המרחק שלו סופי. מקלים את הקשתות היוצאות ממנו.`);
      for (const a of G.adj[u]) {
        const v = a.v;
        if (closed[v]) continue;
        st.edge = a.e; st.from = u;
        const nd = st.d[u] + a.w, old = st.d[v];
        if (nd < old) {
          st.d[v] = nd; st.pi[v] = u; st.color[v] = "g"; st.queue = pq();
          events.push(["relax", u, v, 1, nd]);
          snap(`מקלים את ${L(edgeName(G, u, v))}`, `${L(`d[${u}] + w = ${st.d[u]} + ${a.w} = ${nd} < ${fmt(old)}`)}: מעדכנים ${L(`d[${v}] = ${nd}`)} ו-${L(`π[${v}] = ${u}`)}.`);
        } else {
          events.push(["relax", u, v, 0, nd]);
          snap(`מקלים את ${L(edgeName(G, u, v))}`, `${L(`d[${u}] + w = ${st.d[u]} + ${a.w} = ${nd} ≥ ${fmt(old)}`)}: אין שיפור.`);
        }
      }
    }
    st.cur = null; st.edge = null;
    snap("סיום", `${L(`d[v] = δ(${s}, v)`)} לכל קודקוד, וקשתות ה-${L("π")} יוצרות עץ מסלולים קצרים.`);
    return { frames: R.frames, events, result: { d: Object.assign({}, st.d), pi: Object.assign({}, st.pi), order } };
  }
  function prim(G) {
    const R = runner(G), { st, snap, events } = R, r = G.source, closed = {}, piEdge = {};
    G.ids.forEach(v => st.key[v] = INF);
    st.key[r] = 0;
    const pq = () => G.ids.filter(v => !closed[v] && st.key[v] < INF).sort((a, b) => st.key[a] - st.key[b] || G.rank[a] - G.rank[b]);
    st.queue = pq(); G.ids.forEach(v => st.color[v] = st.key[v] < INF ? "g" : "w");
    snap("אתחול", `השורש ${L(r)}: ${L(`key[${r}] = 0`)}, ולכל השאר ${L("key = ∞")}. ${L("key[v]")} הוא משקל הקשת הקלה ביותר שמחברת את ${L("v")} לעץ.`);
    const order = [], mst = [];
    let weight = 0;
    for (;;) {
      const u = extractMin(G, st.key, closed);
      if (u === null) break;
      if (st.key[u] === INF) { st.cur = null; st.edge = null; snap("שאר הקודקודים אינם ישיגים", `הגרף אינו קשיר: ${L(G.ids.filter(v => !closed[v]).join(", "))} לא יצורפו לעץ.`); break; }
      closed[u] = true; st.S.push(u); order.push(u); st.color[u] = "b"; st.cur = u; st.edge = null; st.queue = pq();
      if (st.pi[u] != null) { st.mst.push(piEdge[u]); mst.push([st.pi[u], u]); weight += st.key[u]; st.edge = piEdge[u]; st.from = st.pi[u]; }
      events.push(["extract", u, st.key[u], st.pi[u]]);
      snap(`מוציאים את ${L(u)}` + (st.pi[u] != null ? ` ומוסיפים לעץ את ${L(st.pi[u] + "–" + u)}` : ""),
        `${L(`key[${u}] = ${st.key[u]}`)} הוא המינימלי בתור. ` + (st.pi[u] != null ? `משקל העץ עד כה: ${L(weight)}.` : "זה השורש."));
      for (const a of G.adj[u]) {
        const v = a.v;
        if (closed[v]) continue;
        st.edge = a.e; st.from = u;
        const old = st.key[v];
        if (a.w < old) {
          st.key[v] = a.w; st.pi[v] = u; piEdge[v] = a.e; st.color[v] = "g"; st.queue = pq();
          events.push(["upd", u, v, 1, a.w]);
          snap(`בודקים את ${L(edgeName(G, u, v))}`, `${L(v)} עדיין בתור ו-${L(`w = ${a.w} < key[${v}] = ${fmt(old)}`)}: מעדכנים ${L(`key[${v}] = ${a.w}`)} ו-${L(`π[${v}] = ${u}`)}.`);
        } else {
          events.push(["upd", u, v, 0, a.w]);
          snap(`בודקים את ${L(edgeName(G, u, v))}`, `${L(`w = ${a.w} ≥ key[${v}] = ${fmt(old)}`)}: אין שינוי.`);
        }
      }
    }
    st.cur = null; st.edge = null;
    snap("סיום", `עץ פורש מינימלי עם ${L(mst.length)} קשתות ומשקל כולל ${L(weight)}.`);
    return { frames: R.frames, events, result: { mst, weight, pi: Object.assign({}, st.pi), order, key: Object.assign({}, st.key) } };
  }
  function kruskal(G) {
    const R = runner(G), { st, snap, events } = R;
    const tie = e => { const [a, b] = [e.u, e.v].sort(natCmp); return [a, b]; };
    const sorted = G.edges.slice().sort((x, y) => {
      if (x.w !== y.w) return x.w - y.w;
      if (G.alpha) { const [a1, b1] = tie(x), [a2, b2] = tie(y); const c = natCmp(a1, a2) || natCmp(b1, b2); if (c) return c; }
      return x.i - y.i;
    });
    const setOf = {}; G.ids.forEach(v => setOf[v] = v);
    const members = {}; G.ids.forEach(v => members[v] = [v]);
    const showSets = () => { st.sets = G.ids.filter(v => setOf[v] === v).map(v => members[v].slice().sort((a, b) => G.rank[a] - G.rank[b])); };
    showSets(); st.sorted = sorted.map(e => e.i); st.idx = -1;
    const paint = () => { let c = 0; st.comp = {}; st.sets.forEach(s => { if (s.length > 1) { c++; s.forEach(v => st.comp[v] = c); } }); };
    snap("ממיינים את הקשתות לפי משקל", `בהתחלה כל קודקוד הוא קבוצה בפני עצמו. עוברים על הקשתות מהקלה לכבדה, ולוקחים קשת רק אם היא מחברת שתי קבוצות שונות.`);
    const mst = [], need = G.ids.length - 1;
    let weight = 0;
    for (let j = 0; j < sorted.length && mst.length < need; j++) {
      const e = sorted[j]; st.idx = j; st.edge = e.i; st.from = e.u; st.cur = null;
      const a = setOf[e.u], b = setOf[e.v];
      const en = L(e.u + "–" + e.v), wl = L(`w = ${e.w}`);
      if (a !== b) {
        const keep = G.rank[a] < G.rank[b] ? a : b, drop = keep === a ? b : a;
        members[keep] = members[keep].concat(members[drop]); members[drop].forEach(v => setOf[v] = keep); delete members[drop];
        mst.push([e.u, e.v]); weight += e.w; st.mst.push(e.i); showSets(); paint();
        events.push(["take", e.u, e.v, e.w]);
        snap(`לוקחים את ${en}, ${wl}`, `${L(e.u)} ו-${L(e.v)} בקבוצות שונות: מוסיפים את הקשת לעץ ומאחדים את הקבוצות. משקל העץ עד כה: ${L(weight)}.`);
      } else {
        st.skip.push(e.i);
        events.push(["skip", e.u, e.v, e.w]);
        snap(`מדלגים על ${en}, ${wl}`, `${L(e.u)} ו-${L(e.v)} כבר באותה קבוצה: הקשת הייתה סוגרת מעגל.`);
      }
    }
    st.edge = null; st.idx = sorted.length;
    snap("סיום", mst.length === need ? `נבחרו ${L(need)} קשתות, ${L("|V| − 1")}, ומשקל העץ הכולל ${L(weight)}.`
      : `הגרף אינו קשיר: התקבל יער פורש מינימלי עם ${L(mst.length)} קשתות ומשקל ${L(weight)}.`);
    return { frames: R.frames, events, result: { mst, weight } };
  }
  const RUN = { bfs, dfs, topo, scc, dijkstra, prim, kruskal };

  const cache = new WeakMap();
  function compute(spec) {
    if (spec && typeof spec === "object" && cache.has(spec)) return cache.get(spec);
    const G = build(spec);
    const out = G.algo ? RUN[G.algo](G) : { frames: [], events: [], result: {} };
    out.G = G;
    if (spec && typeof spec === "object") cache.set(spec, out);
    return out;
  }

  /* ================================ checks (validate.py / course_lint.js) ================================ */
  const toNum = x => (x === null || x === "∞" || x === "inf" || x === "INF") ? INF : x;
  const sameSet = (a, b) => a.length === b.length && a.every(x => b.includes(x));
  const pairKey = (p, directed) => directed ? p.join(">") : p.map(String).sort().join("~");
  function check(spec) {
    const P = shapeProblems(spec);
    if (P.length) return P;
    let out;
    try { out = compute(spec); } catch (e) { return [String(e.message || e)]; }
    const r = out.result, a = spec.algo, ex = spec.expect || {}, G = out.G;
    if (a === "topo" && !r.acyclic) P.push("topo: the graph has a cycle (no topological order)");
    const cmpMap = (name, got, want, num) => {
      if (!want || typeof want !== "object" || Array.isArray(want)) { P.push(`expect.${name} must be an object {node: value}`); return; }
      for (const k of Object.keys(want)) {
        if (!(k in got)) { P.push(`expect.${name}: ${k} is not a node`); continue; }
        const w = num ? toNum(want[k]) : (want[k] == null ? null : String(want[k]));
        if (got[k] !== w) P.push(`expect.${name}[${k}] = ${fmt(want[k])} but ${a} gives ${fmt(got[k])}`);
      }
    };
    const cmpList = (name, got, want) => {
      if (!Array.isArray(want)) { P.push(`expect.${name} must be a list`); return; }
      if (want.map(String).join(",") !== got.join(",")) P.push(`expect.${name} = ${want.join(",")} but ${a} gives ${got.join(",")}`);
    };
    for (const k of Object.keys(ex)) {
      const w = ex[k];
      if (k === "order") cmpList(k, r.order, w);
      else if (k === "topo") cmpList(k, r.topo, w);
      else if (k === "d") cmpMap(k, r.d, w, true);
      else if (k === "disc") cmpMap(k, r.disc, w, true);
      else if (k === "fin") cmpMap(k, r.fin, w, true);
      else if (k === "pi") cmpMap(k, r.pi, w, false);
      else if (k === "weight") { if (toNum(w) !== r.weight) P.push(`expect.weight = ${w} but ${a} gives ${r.weight}`); }
      else if (k === "classes") {
        if (!w || typeof w !== "object") { P.push("expect.classes must be an object {\"u-v\": kind}"); continue; }
        for (const ek of Object.keys(w)) {
          const [u, v] = ek.split("-");
          let got = r.classes[ek];
          if (got === undefined && !G.directed) got = r.classes[v + "-" + u];
          const want = String(w[ek]).replace(/^fwd$/, "forward");
          if (got === undefined) P.push(`expect.classes: ${ek} is not an edge (or was never examined)`);
          else if (got !== want) P.push(`expect.classes[${ek}] = ${w[ek]} but ${a} gives ${got}`);
        }
      } else if (k === "scc") {
        if (!Array.isArray(w) || !w.every(Array.isArray)) { P.push("expect.scc must be a list of lists"); continue; }
        const g = r.scc.map(c => c.slice().sort(natCmp).join(",")).sort(), want = w.map(c => c.map(String).sort(natCmp).join(",")).sort();
        if (g.join("|") !== want.join("|")) P.push(`expect.scc = ${want.join(" | ")} but scc gives ${g.join(" | ")}`);
      } else if (k === "mst") {
        if (!Array.isArray(w) || !w.every(p => Array.isArray(p) && p.length === 2)) { P.push("expect.mst must be a list of [u, v] pairs"); continue; }
        if (!sameSet(r.mst.map(p => pairKey(p)), w.map(p => pairKey(p.map(String))))) P.push(`expect.mst = ${w.map(p => p.join("-")).join(",")} but ${a} gives ${r.mst.map(p => p.join("-")).join(",")}`);
      }
    }
    return P;
  }

  /* a step's `key` -> the value it names: order | topo | weight | sccCount | d.X | pi.X | disc.X | fin.X | key.X | class.U-V */
  const KEYS = { order: ["bfs", "dfs", "topo", "scc", "dijkstra", "prim"], topo: ["topo"], weight: ["prim", "kruskal"], sccCount: ["scc"],
    d: ["bfs", "dijkstra"], pi: ["bfs", "dfs", "topo", "dijkstra", "prim"], disc: ["dfs", "topo", "scc"], fin: ["dfs", "topo", "scc"],
    key: ["prim"], class: ["dfs", "topo", "scc"] };
  function answerOf(spec, key) {
    const m = /^(order|topo|weight|sccCount)$|^(d|pi|disc|fin|key|class)\.(.+)$/.exec(String(key || ""));
    if (!m) throw new Error(`key "${key}": use order, topo, weight, sccCount, d.X, pi.X, disc.X, fin.X, key.X or class.U-V`);
    const name = m[1] || m[2];
    if (!KEYS[name].includes(spec.algo)) throw new Error(`key "${key}" is not an output of ${spec.algo || "a plain drawing"}`);
    const r = compute(spec).result, G = compute(spec).G;
    if (name === "order") return r.order;
    if (name === "topo") return r.topo;
    if (name === "weight") return r.weight;
    if (name === "sccCount") return r.scc.length;
    const arg = m[3];
    if (name === "class") {
      const [u, v] = arg.split("-");
      const got = r.classes[arg] !== undefined ? r.classes[arg] : (!G.directed ? r.classes[v + "-" + u] : undefined);
      if (got === undefined) throw new Error(`key "${key}": ${arg} is not a classified edge`);
      return got;
    }
    const map = { d: r.d, pi: r.pi, disc: r.disc, fin: r.fin, key: r.key }[name];
    if (!(arg in map)) throw new Error(`key "${key}": ${arg} is not a node`);
    return map[arg];
  }

  /* ================================ layout + SVG ================================ */
  /* viewBox width: 520 on a wide container, 340 on a phone (so a 390px screen draws the nodes and labels about
     1.5x larger instead of squeezing the wide drawing) */
  const WIDE = 520, NARROW = 340, NR = 20;
  let W = WIDE;
  const widthFor = el => (el && el.clientWidth > 0 && el.clientWidth < 460) ? NARROW : WIDE;
  function layout(G) {
    const pt = 46, pb = 28, px = W === NARROW ? 28 : 36;
    const P = {};
    if (G.pos) {
      const xs = G.ids.map(v => G.pos[v].x), ys = G.ids.map(v => G.pos[v].y);
      const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
      const bw = x1 - x0, bh = y1 - y0, iw = W - 2 * px;
      const ih = Math.max(110, Math.min(340, bw > 0 ? iw * bh / bw : 220));
      const sc = Math.min(bw > 0 ? iw / bw : INF, bh > 0 ? ih / bh : INF);
      const s = isFinite(sc) ? sc : 1;
      const ox = px + (iw - bw * s) / 2, oy = pt + (ih - bh * s) / 2;
      G.ids.forEach(v => P[v] = { x: ox + (G.pos[v].x - x0) * s, y: oy + (G.pos[v].y - y0) * s });
      return { P, H: Math.round(ih + pt + pb) };
    }
    const n = G.ids.length;
    if (G.layout === "layers") {
      const depth = {}, q = [G.source]; depth[G.source] = 0;
      const und = {}; G.ids.forEach(v => und[v] = []);
      G.edges.forEach(e => { und[e.u].push(e.v); und[e.v].push(e.u); });
      while (q.length) { const u = q.shift(); for (const v of und[u].slice().sort((a, b) => G.rank[a] - G.rank[b])) if (!(v in depth)) { depth[v] = depth[u] + 1; q.push(v); } }
      let maxD = Math.max(0, ...Object.values(depth));
      G.ids.forEach(v => { if (!(v in depth)) depth[v] = maxD + 1; });
      maxD = Math.max(...Object.values(depth));
      const gap = maxD ? Math.min(110, 300 / maxD) : 0;
      for (let k = 0; k <= maxD; k++) {
        const row = G.ids.filter(v => depth[v] === k);
        row.forEach((v, i) => P[v] = { x: px + (W - 2 * px) * (i + 1) / (row.length + 1), y: pt + k * gap });
      }
      return { P, H: Math.round(pt + maxD * gap + pb) };
    }
    const narrow = W === NARROW;
    const R = n <= 2 ? 90 : n <= 4 ? (narrow ? 105 : 120) : (narrow ? 125 : 150);
    const sx = n <= 2 ? (narrow ? 1.3 : 1.6) : (narrow ? 1.05 : 1.25);
    const cx = W / 2, cy = pt + R;
    G.ids.forEach((v, i) => {
      const a = -Math.PI / 2 + 2 * Math.PI * i / n;
      P[v] = n === 1 ? { x: cx, y: cy } : { x: cx + R * Math.cos(a) * sx, y: cy + R * Math.sin(a) };
    });
    return { P, H: Math.round(2 * R + pt + pb) };
  }
  const r1 = x => Math.round(x * 10) / 10;
  function edgeGeom(G, e, P, flip) {
    let u = e.u, v = e.v;
    if (flip) [u, v] = [v, u];
    const a = P[u], b = P[v];
    if (u === v) {   // self-loop at the node's lower right, clear of the time label above it
      const at = ang => ({ x: a.x + NR * Math.cos(ang), y: a.y + NR * Math.sin(ang) });
      const s0 = at(-0.15), s1 = at(1.05), c0 = { x: a.x + 58 * Math.cos(-0.25), y: a.y + 58 * Math.sin(-0.25) },
        c1 = { x: a.x + 58 * Math.cos(1.15), y: a.y + 58 * Math.sin(1.15) };
      const dx = s1.x - c1.x, dy = s1.y - c1.y, l = Math.hypot(dx, dy);
      return { d: `M ${r1(s0.x)} ${r1(s0.y)} C ${r1(c0.x)} ${r1(c0.y)} ${r1(c1.x)} ${r1(c1.y)} ${r1(s1.x)} ${r1(s1.y)}`,
        tip: s1, dir: { x: dx / l, y: dy / l }, mid: { x: a.x + 40 * Math.cos(0.45), y: a.y + 40 * Math.sin(0.45) } };
    }
    const dx = b.x - a.x, dy = b.y - a.y, len = Math.hypot(dx, dy) || 1, ux = dx / len, uy = dy / len;
    const curve = G.directed && G.edges.some(f => f.u === e.v && f.v === e.u) ? 22 : 0;
    if (curve) {
      const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2, cx = mx - uy * curve, cy = my + ux * curve;
      const d1x = cx - a.x, d1y = cy - a.y, l1 = Math.hypot(d1x, d1y), d2x = cx - b.x, d2y = cy - b.y, l2 = Math.hypot(d2x, d2y);
      const x1 = a.x + d1x / l1 * NR, y1 = a.y + d1y / l1 * NR, x2 = b.x + d2x / l2 * (NR + 1), y2 = b.y + d2y / l2 * (NR + 1);
      return { d: `M ${r1(x1)} ${r1(y1)} Q ${r1(cx)} ${r1(cy)} ${r1(x2)} ${r1(y2)}`, tip: { x: x2, y: y2 }, dir: { x: -d2x / l2, y: -d2y / l2 },
        mid: { x: (x1 + 2 * cx + x2) / 4, y: (y1 + 2 * cy + y2) / 4 } };
    }
    const x1 = a.x + ux * NR, y1 = a.y + uy * NR, x2 = b.x - ux * (NR + (G.directed ? 1 : 0)), y2 = b.y - uy * (NR + (G.directed ? 1 : 0));
    return { d: `M ${r1(x1)} ${r1(y1)} L ${r1(x2)} ${r1(y2)}`, tip: { x: x2, y: y2 }, dir: { x: ux, y: uy }, mid: { x: (x1 + x2) / 2, y: (y1 + y2) / 2 } };
  }
  function head(g) {
    const { tip, dir } = g, bx = tip.x - dir.x * 11, by = tip.y - dir.y * 11, px = -dir.y * 5.5, py = dir.x * 5.5;
    return `${r1(tip.x)},${r1(tip.y)} ${r1(bx + px)},${r1(by + py)} ${r1(bx - px)},${r1(by - py)}`;
  }
  const KCLS = { tree: "k-tree", back: "k-back", fwd: "k-fwd", cross: "k-cross" };
  function nodeLabel(algo, fr, v) {
    if (!fr || !algo) return "";
    if (algo === "bfs" || algo === "dijkstra") return "d=" + fmt(fr.d[v]);
    if (algo === "prim") return "key=" + fmt(fr.key[v]);
    if (algo === "dfs" || algo === "topo" || algo === "scc") return (fr.d[v] != null ? fr.d[v] : "—") + "/" + (fr.f[v] != null ? fr.f[v] : "—");
    return "";
  }
  function svg(G, fr, plain) {
    const { P, H } = layout(G);
    const algo = plain ? null : G.algo;
    let es = "", ws = "", ns = "";
    for (const e of G.edges) {
      const g = edgeGeom(G, e, P, fr && fr.flip);
      let c = "gv-e";
      if (fr && !plain) {
        if (fr.mst.includes(e.i)) c += " k-mst";
        else if (fr.skip.includes(e.i)) c += " k-skip";
        else if (fr.cls[e.i]) c += " " + KCLS[fr.cls[e.i]];
        if (fr.edge === e.i) c += " is-cur";
      }
      es += `<path class="${c}" d="${g.d}"/>`;
      if (G.directed) es += `<polygon class="gv-ah ${c}" points="${head(g)}"/>`;
      if (e.w != null) ws += `<text class="gv-w" x="${r1(g.mid.x)}" y="${r1(g.mid.y + 4.5)}" text-anchor="middle">${esc(e.w)}</text>`;
    }
    for (const v of G.ids) {
      const p = P[v];
      let c = "gv-n";
      if (fr && !plain) {
        if ((algo === "scc" && fr.phase === 2 || algo === "kruskal") && fr.comp[v]) c += " cc" + ((fr.comp[v] - 1) % 6);
        else c += " st-" + fr.color[v];
      }
      const cur = fr && !plain && fr.cur === v;
      const lab = plain ? "" : nodeLabel(algo, fr, v);
      ns += `<g class="${c}${cur ? " is-cur" : ""}" data-node="${esc(v)}">` +
        (cur ? `<circle class="gv-ring" cx="${r1(p.x)}" cy="${r1(p.y)}" r="${NR + 5}"/>` : "") +
        `<circle class="gv-c" cx="${r1(p.x)}" cy="${r1(p.y)}" r="${NR}"/>` +
        `<text class="gv-nt" x="${r1(p.x)}" y="${r1(p.y + 5.5)}" text-anchor="middle">${esc(v)}</text>` +
        (lab ? `<text class="gv-nl" x="${r1(p.x)}" y="${r1(p.y - NR - 8)}" text-anchor="middle">${esc(lab)}</text>` : "") + `</g>`;
    }
    const aria = `גרף ${G.directed ? "מכוון" : "לא מכוון"}: ${G.ids.length} קודקודים, ${G.edges.length} קשתות`;
    return `<svg class="gv-svg" viewBox="0 0 ${W} ${H}" direction="ltr" role="img" aria-label="${esc(aria)}" xmlns="http://www.w3.org/2000/svg">` +
      `<g class="gv-edges">${es}</g><g class="gv-weights">${ws}</g><g class="gv-nodes">${ns}</g></svg>`;
  }

  /* ================================ panels ================================ */
  const ALGO_HE = { bfs: ["חיפוש לרוחב", "BFS"], dfs: ["חיפוש לעומק", "DFS"], topo: ["מיון טופולוגי", "DFS"], scc: ["רכיבים קשירים היטב", "SCC"],
    dijkstra: ["דייקסטרה", "Dijkstra"], prim: ["פרים", "Prim"], kruskal: ["קרוסקל", "Kruskal"] };
  const chip = (v, cls) => `<span class="gv-chip${cls ? " " + cls : ""}">${esc(v)}</span>`;
  const seq = (list, emptyHe, cls, sep) => list.length
    ? `<div class="gv-seq" dir="ltr">${list.map((v, i) => (i && sep ? `<span class="gv-sep">${sep}</span>` : "") + chip(v, typeof cls === "function" ? cls(v, i) : cls)).join("")}</div>`
    : `<div class="gv-empty">${emptyHe}</div>`;
  const box = (titleHtml, body, cls) => `<div class="gv-box${cls ? " " + cls : ""}"><div class="gv-bt">${titleHtml}</div>${body}</div>`;
  function table(G, fr, rows) {
    const cellCls = v => fr.cur === v ? "c-cur" : (fr.color[v] === "g" ? "c-g" : fr.color[v] === "b" ? "c-b" : "");
    const vertical = G.ids.length > 8;
    if (vertical) {
      return `<table class="gv-table gv-vert" dir="ltr"><thead><tr><th>v</th>${rows.map(r => `<th>${r[0]}</th>`).join("")}</tr></thead><tbody>` +
        G.ids.map(v => `<tr class="${cellCls(v)}"><th>${esc(v)}</th>${rows.map(r => `<td>${esc(r[1](v))}</td>`).join("")}</tr>`).join("") + `</tbody></table>`;
    }
    return `<table class="gv-table" dir="ltr"><thead><tr><th></th>${G.ids.map(v => `<th>${esc(v)}</th>`).join("")}</tr></thead><tbody>` +
      rows.map(r => `<tr><th>${r[0]}</th>${G.ids.map(v => `<td class="${cellCls(v)}">${esc(r[1](v))}</td>`).join("")}</tr>`).join("") + `</tbody></table>`;
  }
  const dash = x => x == null ? "–" : String(x);
  function edgeLabel(G, i, flip) { const e = G.edges[i]; return flip ? e.v + arrow(G) + e.u : e.u + arrow(G) + e.v; }
  function panels(G, fr) {
    const a = G.algo, out = [];
    if (a === "bfs") {
      out.push(box("תור <bdi dir=\"ltr\">Q</bdi> · ראש התור משמאל", seq(fr.queue.map(v => `${v} (${fmt(fr.d[v])})`), "התור ריק", (v, i) => i ? "" : "head", "←")));
      out.push(box("סדר הגילוי", seq(fr.order, "עדיין לא התגלה דבר", "")));
      out.push(box("מרחקים וקודמים", table(G, fr, [["d", v => fmt(fr.d[v])], ["π", v => dash(fr.pi[v])]]), "gv-wide"));
    } else if (a === "dfs" || a === "topo" || (a === "scc" && fr.phase === 1)) {
      out.push(box("מחסנית הרקורסיה · הראש למעלה", fr.stack.length
        ? `<div class="gv-stack" dir="ltr">${fr.stack.map((v, i) => chip(`${v} (d=${fr.d[v]})`, i === fr.stack.length - 1 ? "head" : "")).join("")}</div>`
        : `<div class="gv-empty">המחסנית ריקה</div>`));
      out.push(box("זמני גילוי וסיום", table(G, fr, [["d", v => dash(fr.d[v])], ["f", v => dash(fr.f[v])], ["π", v => dash(fr.pi[v])]]), "gv-wide"));
      const cl = G.edges.filter(e => fr.cls[e.i]).map(e => [edgeLabel(G, e.i), fr.cls[e.i]]);
      out.push(box("סיווג הקשתות", cl.length ? `<div class="gv-classes">${cl.map(([n, k]) =>
        `<span class="gv-cl ${KCLS[k]}"><bdi dir="ltr">${esc(n)}</bdi> ${KIND_HE[k]}</span>`).join("")}</div>` : `<div class="gv-empty">עדיין לא סווגה קשת</div>`, "gv-wide"));
      if (a === "topo") out.push(box("הרשימה הטופולוגית · מוסיפים בראש", seq(fr.topo, "הרשימה ריקה", "", "→"), "gv-wide"));
    } else if (a === "scc") {
      out.push(box(`סדר המעבר השני · ${L("f")} יורד`, seq(fr.second.map(v => `${v} (${fr.f[v]})`), "", (v, i) => fr.comp[fr.second[i]] ? "done" : ""), "gv-wide"));
      const comps = {};
      G.ids.forEach(v => { if (fr.comp[v]) (comps[fr.comp[v]] = comps[fr.comp[v]] || []).push(v); });
      const ks = Object.keys(comps).sort((x, y) => x - y);
      out.push(box("רכיבים קשירים היטב", ks.length ? `<div class="gv-comps" dir="ltr">${ks.map(k =>
        `<span class="gv-comp cc${(k - 1) % 6}">${esc(`${k}: {${comps[k].join(", ")}}`)}</span>`).join("")}</div>` : `<div class="gv-empty">עדיין לא נמצא רכיב</div>`, "gv-wide"));
      out.push(box("זמני הסיום מהשלב הראשון", table(G, fr, [["f", v => dash(fr.f[v])], ["רכיב", v => dash(fr.comp[v])]]), "gv-wide"));
    } else if (a === "dijkstra" || a === "prim") {
      const val = a === "dijkstra" ? fr.d : fr.key, nm = a === "dijkstra" ? "d" : "key";
      out.push(box(`תור העדיפויות · לפי ${L(nm)}`, seq(fr.queue.map(v => `${v} (${fmt(val[v])})`), "אין בתור קודקוד עם ערך סופי", (v, i) => i ? "" : "head")));
      out.push(box(`${a === "dijkstra" ? "קבוצת הסגורים" : "קודקודי העץ"} ${L("S")}`, seq(fr.S, "ריקה", "")));
      out.push(box(a === "dijkstra" ? "מרחקים וקודמים" : "מפתחות וקודמים", table(G, fr, [[nm, v => fmt(val[v])], ["π", v => dash(fr.pi[v])]]), "gv-wide"));
      if (a === "prim") out.push(mstBox(G, fr));
    } else if (a === "kruskal") {
      out.push(box("הקשתות לפי משקל", `<div class="gv-classes">${fr.sorted.map((i, j) => {
        const s = fr.mst.includes(i) ? "k-mst" : fr.skip.includes(i) ? "k-skip" : j === fr.idx ? "is-cur" : "";
        const mark = fr.mst.includes(i) ? "✓" : fr.skip.includes(i) ? "✗" : "";
        return `<span class="gv-cl ${s}"><bdi dir="ltr">${esc(edgeLabel(G, i))} (${esc(G.edges[i].w)})</bdi>${mark ? " " + mark : ""}</span>`;
      }).join("")}</div>`, "gv-wide"));
      out.push(box(`קבוצות זרות ${L("(Union-Find)")}`, `<div class="gv-comps" dir="ltr">${fr.sets.map(s =>
        `<span class="gv-comp${s.length > 1 ? " cc" + ((fr.comp[s[0]] - 1) % 6) : ""}">${esc("{" + s.join(", ") + "}")}</span>`).join("")}</div>`, "gv-wide"));
      out.push(mstBox(G, fr));
    }
    return out.join("");
  }
  function mstBox(G, fr) {
    const w = fr.mst.reduce((s, i) => s + G.edges[i].w, 0);
    return box(`קשתות העץ שנבחרו · משקל ${L(w)}`, seq(fr.mst.map(i => `${G.edges[i].u}–${G.edges[i].v}`), "עדיין לא נבחרה קשת", "k-mst"), "gv-wide");
  }
  function legend(G) {
    const a = G.algo, it = [];
    const dot = (c, t) => `<span class="gv-key"><i class="gv-dot ${c}"></i>${t}</span>`;
    const line = (c, t) => `<span class="gv-key"><i class="gv-sw ${c}"></i>${t}</span>`;
    if (["bfs", "dfs", "topo", "scc", "dijkstra", "prim"].includes(a)) {
      const grayHe = { bfs: "בתור (אפור)", dijkstra: "בתור, d סופי", prim: "בתור, key סופי" }[a] || "במחסנית (אפור)";
      it.push(dot("st-g", grayHe.replace(/(d|key) סופי/, m => `${L(m.split(" ")[0])} סופי`)), dot("st-b", a === "dijkstra" ? "סגור" : a === "prim" ? "בעץ" : "הסתיים (שחור)"));
    }
    it.push(line("is-cur", "נבדקת עכשיו"));
    if (a === "bfs" || a === "dijkstra") it.push(line("k-tree", a === "bfs" ? "קשת עץ" : "קשת π"));
    if (a === "dfs" || a === "topo" || a === "scc") it.push(line("k-tree", "עץ"), line("k-back", "אחורה"), line("k-fwd", "קדימה"), line("k-cross", "חוצה"));
    if (a === "prim" || a === "kruskal") it.push(line("k-mst", "בעץ הפורש"));
    if (a === "kruskal") it.push(line("k-skip", "נדחתה (מעגל)"));
    return `<div class="gv-legend">${it.join("")}</div>`;
  }

  /* ================================ widget ================================ */
  const escAttr = s => esc(s);
  function figure(spec, opts) {
    const list = Array.isArray(spec) ? spec : [spec];
    const o = opts || {};
    return list.map(sp => `<div class="graph-fig" data-graph="${escAttr(JSON.stringify(sp))}"${o.locked ? ' data-locked="1"' : ""}${o.static ? ' data-static="1"' : ""}></div>`).join("");
  }
  function headHtml(G) {
    const nm = G.algo ? ALGO_HE[G.algo] : null;
    return `<div class="gv-head">${nm ? `<span class="gv-algo">${nm[0]} <bdi dir="ltr">(${esc(nm[1])})</bdi></span>` : ""}` +
      (G.caption ? `<span class="gv-cap">${esc(G.caption)}</span>` : "") + `</div>`;
  }
  function mount(el, spec, opts) {
    const o = opts || {};
    el.classList.add("graph-fig");
    el.setAttribute("data-gv", "1");
    if (el._gvTimer) { clearInterval(el._gvTimer); el._gvTimer = null; }
    let out;
    try { out = compute(spec); } catch (e) {
      el.innerHTML = `<div class="gv-error">לא ניתן לצייר את הגרף</div>`;
      if (typeof console !== "undefined") console.warn("graph.js: " + e.message);
      return el;
    }
    const G = out.G;
    const plain = !G.algo || o.static || o.locked;
    el.classList.toggle("gv-plain", !!plain);
    /* mounted inside a closed <details> the width is 0: redraw at the right scale once it is shown / resized */
    if (el._gvRO) { el._gvRO.disconnect(); el._gvRO = null; }
    if (typeof ResizeObserver !== "undefined") {
      let lastW = widthFor(el);
      el._gvRO = new ResizeObserver(() => {
        const w = widthFor(el);
        if (w === lastW || !el.clientWidth) return;
        lastW = w;
        if (el._gvShow && !plain) el._gvShow(+el.dataset.step || 0);
        else { const p = el.querySelector(".gv-plot"); if (p) { W = w; p.innerHTML = svg(G, null, true); } }
      });
      el._gvRO.observe(el);
    }
    if (plain) {
      W = widthFor(el);
      el.innerHTML = headHtml(G).replace('<div class="gv-head"></div>', "") + `<div class="gv-plot" dir="ltr">${svg(G, null, true)}</div>` +
        (o.locked && G.algo ? `<div class="gv-hint">אחרי שתענו אפשר להריץ כאן את האלגוריתם צעד אחר צעד.</div>` : "");
      el._gvSpec = spec;
      return el;
    }
    const frames = out.frames, n = frames.length;
    el.setAttribute("tabindex", "0");
    el.innerHTML = headHtml(G) +
      `<div class="gv-narr" aria-live="polite"><div class="gv-t"></div><div class="gv-note"></div></div>` +
      `<div class="gv-plot" dir="ltr"></div>` + legend(G) +
      `<div class="gv-ctrl"><button type="button" class="btn ghost gv-first" aria-label="לצעד הראשון">⏮</button>` +
      `<button type="button" class="btn ghost gv-prev">→ הקודם</button>` +
      `<button type="button" class="btn primary gv-play">▶ הפעלה</button>` +
      `<button type="button" class="btn ghost gv-next">הבא ←</button>` +
      `<span class="gv-count"></span></div>` +
      `<div class="gv-panels"></div>`;
    const q = s => el.querySelector(s);
    let i = 0;
    const stop = () => { if (el._gvTimer) { clearInterval(el._gvTimer); el._gvTimer = null; } q(".gv-play").textContent = "▶ הפעלה"; };
    function show(k) {
      i = Math.max(0, Math.min(n - 1, k));
      const fr = frames[i];
      el.dataset.step = String(i);
      q(".gv-t").innerHTML = fr.t;
      q(".gv-note").innerHTML = fr.n;
      W = widthFor(el);
      q(".gv-plot").innerHTML = svg(G, fr, false);
      q(".gv-panels").innerHTML = panels(G, fr);
      q(".gv-count").innerHTML = `צעד <bdi dir="ltr">${i + 1} / ${n}</bdi>`;
      q(".gv-prev").disabled = q(".gv-first").disabled = i === 0;
      q(".gv-next").disabled = i === n - 1;
      if (i === n - 1) stop();
    }
    q(".gv-first").onclick = () => { stop(); show(0); };
    q(".gv-prev").onclick = () => { stop(); show(i - 1); };
    q(".gv-next").onclick = () => { stop(); show(i + 1); };
    q(".gv-play").onclick = () => {
      if (el._gvTimer) { stop(); return; }
      if (i >= n - 1) show(0);
      q(".gv-play").textContent = "⏸ עצירה";
      el._gvTimer = setInterval(() => { if (!el.isConnected) { stop(); return; } show(i + 1); }, o.speed || 900);
    };
    el.onkeydown = ev => {   // RTL: the left arrow moves forward
      const k = ev.key;
      if (k === "ArrowLeft") { stop(); show(i + 1); } else if (k === "ArrowRight") { stop(); show(i - 1); }
      else if (k === "Home") { stop(); show(0); } else if (k === "End") { stop(); show(n - 1); } else return;
      ev.preventDefault(); ev.stopPropagation();   // the app's own arrow keys change the question
    };
    el._gvShow = show;
    show(o.step || 0);
    return el;
  }
  function unlock(el) {
    if (!el) return;
    const hosts = el.matches && el.matches(".graph-fig") ? [el] : [...el.querySelectorAll(".graph-fig[data-locked]")];
    for (const h of hosts) { if (!h._gvSpec) continue; h.removeAttribute("data-locked"); mount(h, h._gvSpec, {}); }
  }
  function hydrate(el) {
    if (!el || !el.querySelectorAll) return 0;
    const hosts = [...el.querySelectorAll(".graph-fig[data-graph]:not([data-gv])")];
    if (el.matches && el.matches(".graph-fig[data-graph]:not([data-gv])")) hosts.unshift(el);
    for (const h of hosts) {
      let spec;
      try { spec = JSON.parse(h.getAttribute("data-graph")); } catch (e) { h.setAttribute("data-gv", "1"); h.innerHTML = `<div class="gv-error">לא ניתן לקרוא את הגרף</div>`; continue; }
      mount(h, spec, { locked: h.hasAttribute("data-locked"), static: h.hasAttribute("data-static") });
    }
    return hosts.length;
  }
  /* learn mode / course lessons write <div class="graph-fig" data-graph='{...}'></div>; mount them as they appear */
  if (typeof document !== "undefined" && typeof MutationObserver !== "undefined") {
    const start = () => {
      hydrate(document.body);
      new MutationObserver(ms => { for (const m of ms) for (const nd of m.addedNodes) if (nd.nodeType === 1) hydrate(nd); })
        .observe(document.body, { childList: true, subtree: true });
    };
    if (document.body) start(); else document.addEventListener("DOMContentLoaded", start);
  }

  const Graph = { compute, check, figure, mount, unlock, hydrate, answerOf, natCmp, ALGOS, EXPECT_KEYS, _: { build, shapeProblems, layout } };
  root.Graph = Graph;
  if (typeof module !== "undefined" && module.exports) module.exports = Graph;
})(typeof window !== "undefined" ? window : globalThis);
