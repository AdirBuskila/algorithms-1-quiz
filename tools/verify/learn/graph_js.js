// Helper for v04_graph_embeds.py: reads a JSON list of graph specs on stdin, runs each through the very graph.js the
// page loads (Graph.compute) and writes [{events, result, problems}] on stdout (Infinity -> null, like test_graph.js).
"use strict";
const path = require("path");
const Graph = require(path.join(__dirname, "..", "..", "..", "graph.js"));
let input = "";
process.stdin.on("data", d => { input += d; });
process.stdin.on("end", () => {
  const specs = JSON.parse(input);
  const out = specs.map(spec => {
    const bare = Object.assign({}, spec); delete bare.expect;
    const o = Graph.compute(bare);
    const result = Object.assign({}, o.result);
    return { events: o.events, result, problems: Graph.check(spec) };
  });
  process.stdout.write(JSON.stringify(out, (k, v) => v === Infinity ? null : v));
});
