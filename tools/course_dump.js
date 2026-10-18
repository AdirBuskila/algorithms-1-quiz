// Blind-refuting support for the guided courses.
//   node tools/course_dump.js <courseId>            -> tools/raw/_blind_course_<id>.json
//        the level questions WITHOUT answers (no correctId/acceptedIds, no explanation, no recap, no lesson):
//        the refuter solves these cold. bankId questions are listed by id only (real exam questions are
//        refuted through the bank's own verify_strip flow).
//   node tools/course_dump.js <courseId> --claims   -> tools/raw/_claims_course_<id>.json   (the answer key; read AFTER solving)
//   node tools/course_dump.js <courseId> --compare  -> compares tools/raw/_verify_course_<id>.json with the key:
//        {"answers": {"<question id>": {"answer": "b"}}}  -> AGREE / DISAGREE per question, exit 1 on any miss
//        (answer: option id for mcq/choice/fillblank, a number for numeric, a string for text,
//         the lines in order for order, the line index for findbug)
// Prints ASCII only (Hebrew goes to the files).
"use strict";
const fs = require("fs"), path = require("path");
const { load } = require("./course_load.js");

const ROOT = process.env.APP_ROOT || path.join(__dirname, "..");
const RAW = path.join(ROOT, "tools", "raw");
const args = process.argv.slice(2);
const courseId = args.find(a => !a.startsWith("--"));
const mode = args.includes("--claims") ? "claims" : args.includes("--compare") ? "compare" : "blind";
if (!courseId) { console.error("usage: node tools/course_dump.js <courseId> [--claims|--compare]"); process.exit(2); }

const loaded = load(ROOT);
if (loaded.errors.length) { console.error("level files do not load:\n  " + loaded.errors.join("\n  ").replace(/[^\x20-\x7e\n]/g, "?")); process.exit(1); }
const levels = loaded.levels.filter(e => e.courseId === courseId).map(e => e.level).sort((a, b) => a.order - b.order);
if (!levels.length) { console.error(`no levels for course ${courseId}`); process.exit(1); }

// a step without its answer: no correctId / answer / tol / accept / bugIndex / explain; an `order` step's lines
// are stored in the correct order, so they are rotated (the refuter sees them scrambled)
const blindStep = s => {
  const out = { type: s.type, prompt: s.prompt };
  if (s.code) out.code = true;
  if (s.options) out.options = s.options.map(o => ({ id: o.id, type: o.type || "text", value: o.value }));
  if (s.lines) out.lines = s.type === "order" ? [...s.lines.slice(1), s.lines[0]] : s.lines;
  if (s.blankIndex != null) out.blankIndex = s.blankIndex;
  if (s.normalize) out.normalize = s.normalize;
  return out;
};
const blindQ = q => {
  if (q.bankId) return { id: `bank:${q.bankId}`, bankId: q.bankId };
  if (q.step) return { id: q.id, step: blindStep(q.step) };
  const out = { id: q.id, question: q.question, options: (q.options || []).map(o => ({ id: o.id, type: o.type || "text", value: o.value })) };
  if (q.image) out.image = q.image;
  return out;
};
const claimOf = q => {
  if (!q.step) return { correctId: q.correctId, ...(q.acceptedIds ? { acceptedIds: q.acceptedIds } : {}) };
  const s = q.step;
  return { type: s.type, ...(s.correctId != null ? { correctId: s.correctId } : {}), ...(s.answer != null ? { answer: s.answer, tol: s.tol || 0 } : {}),
    ...(s.accept ? { accept: s.accept } : {}), ...(s.type === "order" ? { lines: s.lines } : {}), ...(s.bugIndex != null ? { bugIndex: s.bugIndex } : {}) };
};
// verifier answers: choice/fillblank/mcq -> option id, numeric -> number, text -> string, order -> [lines in order], findbug -> line index
const agrees = (k, v) => {
  if (!v) return false;
  if (k.type === "numeric") return Math.abs(Number(v.answer) - k.answer) <= (k.tol || 0) + 1e-9;
  if (k.type === "text") return k.accept.map(a => String(a).trim().toLowerCase()).includes(String(v.answer).trim().toLowerCase());
  if (k.type === "order") return JSON.stringify(v.answer) === JSON.stringify(k.lines);
  if (k.type === "findbug") return Number(v.answer) === k.bugIndex;
  return (k.acceptedIds || [k.correctId]).includes(v.answer);
};
const write = (name, obj) => {
  fs.mkdirSync(RAW, { recursive: true });
  fs.writeFileSync(path.join(RAW, name), JSON.stringify(obj, null, 1) + "\n", "utf8");
  console.log(`wrote tools/raw/${name}`);
};

if (mode === "blind") {
  write(`_blind_course_${courseId}.json`, {
    courseId,
    levels: levels.map(L => ({ id: L.id, order: L.order, boss: !!L.boss, questions: L.questions.map(blindQ) })),
  });
} else {
  const key = {};
  for (const L of levels) for (const q of L.questions) if (!q.bankId) key[q.id] = claimOf(q);
  if (mode === "claims") write(`_claims_course_${courseId}.json`, { courseId, answers: key });
  else {
    const vf = path.join(RAW, `_verify_course_${courseId}.json`);
    if (!fs.existsSync(vf)) { console.error("missing " + vf); process.exit(1); }
    const ver = JSON.parse(fs.readFileSync(vf, "utf8")).answers || {};
    let bad = 0;
    for (const [id, k] of Object.entries(key)) {
      const v = ver[id];
      const ok = agrees(k, v);
      if (!ok) bad++;
      console.log(`${ok ? "AGREE   " : "DISAGREE"} ${id}${v ? "" : " (missing in verifier file)"}`);
    }
    console.log(`\n${Object.keys(key).length - bad}/${Object.keys(key).length} agree`);
    process.exit(bad ? 1 : 0);
  }
}
