// Node driver for tools/validate.py (and build_courses.py): reads [{where, spec, key?, step?}] as JSON on stdin and
// writes [{where, ok, problems}] as JSON on stdout, using the very graph.js the page loads.
//   no key: Graph.check(spec)  (shape, preconditions such as a DAG for topo, and spec.expect vs graph.js output)
//   key:    the step's stored answer must equal Graph.answerOf(spec, key):
//           numeric -> answer; text -> any `accept`; choice / fillblank -> the correct option's value.
//           Lists (order, topo) compare as id sequences ("A, B, C", "A B C", "A→B→C" are all A,B,C).
"use strict";
const path = require("path");
const Graph = require(path.join(__dirname, "..", "graph.js"));

const CLASS_SYN = { tree: ["tree", "עץ", "קשת עץ"], back: ["back", "אחורה", "קשת אחורה"],
  forward: ["forward", "fwd", "קדימה", "קשת קדימה"], cross: ["cross", "חוצה", "קשת חוצה"] };
const toks = s => String(s).replace(/\$/g, "").replace(/\\to|\\rightarrow|->/g, " ").split(/[\s,;→←⟵⟶()[\]{}<>]+/).filter(Boolean);
const NIL = new Set(["–", "-", "—", "nil", "NIL", "null", "None"]);
function same(value, raw, key) {
  if (/^class\./.test(key)) return (CLASS_SYN[value] || [value]).includes(String(raw).trim().toLowerCase()) || (CLASS_SYN[value] || []).includes(String(raw).trim());
  if (Array.isArray(value)) return toks(raw).join(",") === value.join(",");
  if (value === null) return NIL.has(String(raw).trim());
  if (value === Infinity) return ["∞", "inf", "infinity", "\\infty"].includes(String(raw).replace(/\$/g, "").trim().toLowerCase());
  const t = toks(raw);
  return t.length === 1 && (t[0] === String(value) || (typeof value === "number" && Number(t[0]) === value));
}
function stepAnswers(s) {
  if (s.type === "numeric") return [s.answer];
  if (s.type === "text") return s.accept || [];
  if (s.type === "choice" || s.type === "fillblank") { const o = (s.options || []).find(o => o.id === s.correctId); return o ? [o.value] : []; }
  return null;
}

function checkJob(j) {
    const problems = [];
    if (j.key == null) {
      problems.push(...Graph.check(j.spec));
    } else if (!j.spec || typeof j.spec !== "object") {
      problems.push("a step key needs a graph on the step or a single graph on the question");
    } else {
      const bare = Object.assign({}, j.spec); delete bare.expect;   // `expect` is reported by the graph's own job
      const pre = Graph.check(bare);
      if (pre.length) problems.push(...pre);
      else {
        let value;
        try { value = Graph.answerOf(j.spec, j.key); } catch (e) { problems.push(e.message); }
        if (!problems.length) {
          const ans = stepAnswers(j.step || {});
          const show = v => Array.isArray(v) ? v.join(",") : v === Infinity ? "∞" : String(v);
          if (ans === null) problems.push(`key on a ${j.step.type} step: only numeric, text, choice and fillblank steps carry an answer`);
          else if (j.step.type === "text" ? !ans.some(a => same(value, a, j.key)) : !ans.length || !same(value, ans[0], j.key))
            problems.push(`the step's answer ${JSON.stringify(j.step.type === "text" ? ans : ans[0])} but graph.js gives ${show(value)}`);
        }
      }
    }
    return problems;
}
module.exports = { checkJob };

if (require.main === module) {
  let input = "";
  process.stdin.on("data", d => { input += d; });
  process.stdin.on("end", () => {
    const out = JSON.parse(input).map(j => { const problems = checkJob(j); return { where: j.where, ok: !problems.length, problems }; });
    process.stdout.write(JSON.stringify(out));
    process.exit(out.every(r => r.ok) ? 0 : 1);
  });
}
