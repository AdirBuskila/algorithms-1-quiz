// Parity + unit tests for graph.js:  node tools/test_graph.js [--n 60] [--seed 7]
//
// 1. Fixtures with known answers (CLRS fig 22.4 DFS times, a BFS by hand, natural sort of numeric ids).
// 2. Random small graphs (seeded) for every algorithm, run through graph.js AND tools/graph_ref.py (its own
//    implementation with the same conventions, plus networkx cross-checks). The EVENT SEQUENCE and the FINAL
//    outputs must be identical, and networkx must agree.
// 3. Frame invariants: every frame is complete, the last frame shows the final values, the widget renders.
// 4. Graph.check: precondition errors (cycle for topo, negative weight, undirected scc ...) and `expect`.
// Python: $PYTHON, else py (Windows launcher), else python3 / python. Prints ASCII only.
"use strict";
const path = require("path"), { spawnSync } = require("child_process");
const Graph = require(path.join(__dirname, "..", "graph.js"));

const args = process.argv.slice(2);
const argOf = (k, d) => { const i = args.indexOf(k); return i >= 0 ? +args[i + 1] : d; };
const N = argOf("--n", 60), SEED = argOf("--seed", 20261018);
let fail = 0, ok = 0;
function assert(c, msg) { if (c) ok++; else { fail++; console.log("FAIL  " + msg); } }
const J = x => JSON.stringify(x, (k, v) => v === Infinity ? null : v);

/* ---------------- 1. fixtures ---------------- */
{
  // CLRS 3rd ed. fig 22.4 (the course's DFS lesson): u v w x y z, alphabetical adjacency
  const clrs = { directed: true, algo: "dfs", nodes: ["u", "v", "w", "x", "y", "z"],
    edges: [{ u: "u", v: "v" }, { u: "u", v: "x" }, { u: "v", v: "y" }, { u: "w", v: "y" }, { u: "w", v: "z" },
            { u: "x", v: "v" }, { u: "y", v: "x" }, { u: "z", v: "z" }] };
  const r = Graph.compute(clrs).result;
  assert(J(r.disc) === J({ u: 1, v: 2, y: 3, x: 4, w: 9, z: 10 }), "CLRS 22.4 discovery times " + J(r.disc));
  assert(J(r.fin) === J({ x: 5, y: 6, v: 7, u: 8, z: 11, w: 12 }), "CLRS 22.4 finish times " + J(r.fin));
  assert(r.classes["x-v"] === "back" && r.classes["u-x"] === "forward" && r.classes["w-y"] === "cross" && r.classes["z-z"] === "back",
    "CLRS 22.4 edge classes " + J(r.classes));
  // BFS by hand (the Algorithms 2 widget's graph): A-B A-C B-D C-D C-E D-F
  const b = Graph.compute({ directed: false, algo: "bfs", source: "A", nodes: ["A", "B", "C", "D", "E", "F"],
    edges: [["A", "B"], ["A", "C"], ["B", "D"], ["C", "D"], ["C", "E"], ["D", "F"]].map(([u, v]) => ({ u, v })) }).result;
  assert(b.order.join("") === "ABCDEF" && J(b.d) === J({ A: 0, B: 1, C: 1, D: 2, E: 2, F: 3 }) && b.pi.D === "B" && b.pi.E === "C", "BFS by hand " + J(b));
  // natural sort: 2 before 10
  const ns = Graph.compute({ directed: true, algo: "dfs", nodes: [10, 2, 1], edges: [{ u: 1, v: 10 }, { u: 1, v: 2 }] }).result;
  assert(ns.order.join(",") === "1,2,10", "numeric ids sort naturally: " + ns.order.join(","));
  // order "given": neighbours in edge-list order
  const gv = Graph.compute({ directed: true, algo: "bfs", order: "given", nodes: ["A", "C", "B"], edges: [{ u: "A", v: "C" }, { u: "A", v: "B" }] }).result;
  assert(gv.order.join("") === "ACB", "order given keeps the edge order: " + gv.order.join(""));
  // undirected DFS: tree + back only, each edge once
  const ud = Graph.compute({ directed: false, algo: "dfs", nodes: ["A", "B", "C", "D"], edges: [["A", "B"], ["B", "C"], ["C", "A"], ["C", "D"]].map(([u, v]) => ({ u, v })) }).result;
  assert(J(ud.classes) === J({ "A-B": "tree", "B-C": "tree", "C-A": "back", "C-D": "tree" }), "undirected DFS classes " + J(ud.classes));
  // Kruskal ties: equal weights go by endpoint names
  const kr = Graph.compute({ directed: false, algo: "kruskal", nodes: ["A", "B", "C"], edges: [{ u: "B", v: "C", w: 1 }, { u: "A", v: "C", w: 1 }, { u: "A", v: "B", w: 1 }] }).result;
  assert(J(kr.mst) === J([["A", "B"], ["A", "C"]]), "Kruskal tie order " + J(kr.mst));
}

/* ---------------- 4. checks ---------------- */
{
  const cyc = { directed: true, algo: "topo", nodes: ["A", "B"], edges: [{ u: "A", v: "B" }, { u: "B", v: "A" }] };
  assert(Graph.check(cyc).some(p => /cycle/.test(p)), "topo on a cycle is rejected");
  assert(Graph.check({ directed: true, algo: "dijkstra", nodes: ["A", "B"], edges: [{ u: "A", v: "B", w: -1 }] }).some(p => /non-negative/.test(p)), "negative dijkstra weight rejected");
  assert(Graph.check({ directed: false, algo: "scc", nodes: ["A"], edges: [] }).some(p => /directed/.test(p)), "undirected scc rejected");
  assert(Graph.check({ directed: false, algo: "prim", nodes: ["A", "B"], edges: [{ u: "A", v: "B" }] }).some(p => /weight/.test(p)), "prim without weights rejected");
  assert(Graph.check({ directed: false, nodes: ["A", "A"], edges: [] }).some(p => /duplicate node/.test(p)), "duplicate node rejected");
  assert(Graph.check({ directed: false, nodes: ["A", "B"], edges: [{ u: "A", v: "B" }, { u: "B", v: "A" }] }).some(p => /duplicate edge/.test(p)), "duplicate undirected edge rejected");
  assert(Graph.check({ directed: false, nodes: ["A"], edges: [{ u: "A", v: "Z" }] }).some(p => /not a node/.test(p)), "unknown endpoint rejected");
  assert(Graph.check({ directed: false, nodes: [{ id: "A", x: 1, y: 2 }, "B"], edges: [] }).some(p => /every node/.test(p)), "partial x/y rejected");
  assert(Graph.check({ directed: false, nodes: ["A"], edges: [], color: 1 }).some(p => /unknown graph key/.test(p)), "unknown key rejected");
  const good = { directed: false, algo: "bfs", source: "A", nodes: ["A", "B", "C"], edges: [{ u: "A", v: "B" }, { u: "B", v: "C" }],
    expect: { order: ["A", "B", "C"], d: { C: 2 }, pi: { A: null, C: "B" } } };
  assert(Graph.check(good).length === 0, "matching expect passes: " + Graph.check(good).join("; "));
  const bad = Object.assign({}, good, { expect: { d: { C: 1 } } });
  assert(Graph.check(bad).some(p => /expect\.d\[C\] = 1 but bfs gives 2/.test(p)), "wrong expect.d is reported");
  assert(Graph.check(Object.assign({}, good, { expect: { fin: {} } })).some(p => /not an output of bfs/.test(p)), "expect key not of the algo rejected");
  assert(Graph.answerOf(good, "d.C") === 2 && Graph.answerOf(good, "order").join("") === "ABC", "answerOf d.C / order");
  let threw = false; try { Graph.answerOf(good, "fin.C"); } catch (e) { threw = true; }
  assert(threw, "answerOf rejects a key the algo does not produce");
}

/* ---------------- 2. random graphs vs the Python reference ---------------- */
function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const R = rng(SEED);
const ri = (a, b) => a + Math.floor(R() * (b - a + 1));
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(R() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
function randSpec(algo) {
  const n = ri(2, 9), numeric = R() < 0.25;
  const ids = numeric ? shuffle([...Array(n)].map((_, i) => String(ri(0, 1) ? i + 1 : i * 5 + 1))).filter((v, i, a) => a.indexOf(v) === i)
    : shuffle("ABCDEFGHIJ".slice(0, n).split(""));
  const directed = ["topo", "scc"].includes(algo) ? true : ["prim", "kruskal"].includes(algo) ? false : R() < 0.5;
  const p = 0.2 + R() * 0.5, weighted = ["dijkstra", "prim", "kruskal"].includes(algo), distinct = R() < 0.5;
  const perm = shuffle(ids), edges = [], used = new Set();
  let wNext = 1;
  for (const u of ids) for (const v of ids) {
    if (u === v && (!directed || R() > 0.08)) continue;
    if (algo === "topo" && perm.indexOf(u) >= perm.indexOf(v)) continue;   // a DAG
    const k = directed ? u + ">" + v : [u, v].sort().join("~");
    if (used.has(k) || R() > p) continue;
    used.add(k);
    const e = { u, v };
    if (weighted) e.w = distinct ? wNext++ * 3 % 97 + 1 : ri(1, 4);
    edges.push(e);
  }
  if ((algo === "prim" || algo === "kruskal") && R() < 0.85) {   // mostly connected: chain any isolated parts
    for (let i = 1; i < ids.length; i++) {
      const k = [ids[i - 1], ids[i]].sort().join("~");
      if (!used.has(k) && R() < 0.6) { used.add(k); edges.push({ u: ids[i - 1], v: ids[i], w: distinct ? 100 + i : ri(1, 4) }); }
    }
  }
  const spec = { directed, algo, nodes: ids, edges: shuffle(edges) };
  if (R() < 0.7) spec.source = ids[ri(0, ids.length - 1)];
  if (R() < 0.25) spec.order = "given";
  return spec;
}
function python() {
  const tries = process.env.PYTHON ? [process.env.PYTHON] : ["py", "python3", "python"];
  for (const t of tries) { const r = spawnSync(t, ["-c", "import networkx"], { encoding: "utf8" }); if (r.status === 0) return t; }
  return null;
}
const specs = [];
for (const algo of Graph.ALGOS) for (let k = 0; k < N; k++) specs.push(randSpec(algo));
const py = python();
if (!py) { console.log("FAIL  no python with networkx found (set PYTHON)"); fail++; }
else {
  const proc = spawnSync(py, [path.join(__dirname, "graph_ref.py")], { input: JSON.stringify(specs), encoding: "utf8", maxBuffer: 1 << 28, env: Object.assign({}, process.env, { PYTHONUTF8: "1" }) });
  if (proc.status !== 0) { console.log("FAIL  graph_ref.py: " + (proc.stderr || "").slice(0, 600)); fail++; }
  else {
    const ref = JSON.parse(proc.stdout);
    const perAlgo = {};
    specs.forEach((spec, i) => {
      const where = `${spec.algo} #${i} ${J(spec)}`;
      let out;
      try { out = Graph.compute(spec); } catch (e) { assert(false, `${where}: graph.js threw ${e.message}`); return; }
      const want = ref[i], got = out.result;
      perAlgo[spec.algo] = (perAlgo[spec.algo] || 0) + 1;
      assert(J(out.events) === J(want.events), `${where}: event sequence differs\n   js ${J(out.events)}\n   py ${J(want.events)}`);
      for (const k of Object.keys(want.result)) {
        const g = k === "classes" ? got.classes : got[k];
        assert(J(g) === J(want.result[k]), `${where}: result.${k} js ${J(g)} py ${J(want.result[k])}`);
      }
      assert(want.nx.length === 0, `${where}: networkx disagrees: ${want.nx.join("; ")}`);
      assert(Graph.check(spec).length === 0 || spec.algo === "topo", `${where}: check() reports ${Graph.check(spec).join("; ")}`);
      /* 3. frame invariants */
      const fr = out.frames, last = fr[fr.length - 1];
      assert(fr.length >= 2 && fr.every(f => typeof f.t === "string" && f.t && typeof f.n === "string"), `${where}: frames have titles and notes`);
      assert(fr.every(f => !/undefined|NaN|\[object/.test(f.t + f.n)), `${where}: no undefined/NaN in narration`);
      if (spec.algo === "bfs" || spec.algo === "dijkstra") assert(J(last.d) === J(got.d), `${where}: last frame shows the final d`);
      if (["dfs", "topo", "scc"].includes(spec.algo)) assert(J(last.f) === J(got.fin), `${where}: last frame shows the final f`);
      if (spec.algo === "prim" || spec.algo === "kruskal") assert(last.mst.length === got.mst.length, `${where}: last frame shows the whole tree`);
    });
    console.log("random graphs per algorithm: " + Object.entries(perAlgo).map(([a, n]) => `${a} ${n}`).join(", "));
  }
}

/* ---------------- 3b. the widget renders in a DOM ---------------- */
try {
  const { JSDOM } = require("jsdom");
  const dom = new JSDOM(`<!doctype html><body><div id="m"></div></body>`, { runScripts: "outside-only" });
  const w = dom.window;
  w.eval(require("fs").readFileSync(path.join(__dirname, "..", "graph.js"), "utf8"));
  for (const spec of specs.filter((s, i) => i % N === 0)) {
    const host = w.document.getElementById("m");
    host.innerHTML = w.Graph.figure(spec);
    w.Graph.hydrate(host);
    const fig = host.querySelector(".graph-fig");
    assert(fig.querySelector("svg.gv-svg") && fig.querySelector(".gv-count").textContent.includes("1 / "), `${spec.algo}: widget mounted with a step counter`);
    assert(fig.querySelectorAll(".gv-n").length === spec.nodes.length, `${spec.algo}: one node group per node`);
    const next = fig.querySelector(".gv-next");
    while (!next.disabled) next.click();
    assert(fig.dataset.step === String(Graph.compute(spec).frames.length - 1), `${spec.algo}: next reaches the last frame`);
    assert(!/undefined|NaN|\[object/.test(fig.textContent), `${spec.algo}: no undefined/NaN in the widget`);
  }
} catch (e) { if (/Cannot find module 'jsdom'/.test(e.message)) console.log("(jsdom not installed: widget render check skipped)"); else { fail++; console.log("FAIL  widget render: " + e.stack); } }

console.log(fail ? `\n${fail} FAILED, ${ok} ok` : `\nall ok (${ok} checks)`);
process.exit(fail ? 1 : 0);
