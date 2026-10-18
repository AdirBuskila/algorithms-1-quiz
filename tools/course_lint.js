// Lint for the guided "need help?" courses:  node tools/course_lint.js [--strict] [courseId]
//
// Reads courses/<courseId>/*.js (through tools/course_load.js), course.config.json (needHelp),
// the built bank (questions.json) and the shipped PASS threshold in course-ui.js. Exits 1 on any ERROR.
// Every message starts with [<courseId>/<levelId>] so the author knows which level to open.
//   --strict   warnings become errors (ai-draft content, level count outside 6-10, ...)
//
// Checks: level ids unique and orders unique/positive (gaps warn); at most one boss and it is the last
// level; a boss pulls real exam questions; every bankId exists in the built bank; own questions have a
// unique id, >=2 options with unique ids, correctId (and acceptedIds) among them, an explanation; a
// {id, step:{...}} question is a guided step (choice|numeric|text|order|findbug|fillblank) checked like a
// bank step (the build re-checks it with validate.check_step); lesson
// and question texts have no Hebrew inside $math$; no author name from tools/redact.txt in ANY string;
// no JS-escape corruption of TeX (\frac -> form feed); content labelled via `source`.
"use strict";
const fs = require("fs"), path = require("path");
const { load } = require("./course_load.js");

const ROOT = process.env.APP_ROOT || path.join(__dirname, "..");
const args = process.argv.slice(2);
const STRICT = args.includes("--strict");
const ONLY = args.find(a => !a.startsWith("--"));

const errors = [], warns = [], notes = [];
const asc = s => String(s).replace(/[^\x20-\x7e]/g, c => "\\u" + c.charCodeAt(0).toString(16).padStart(4, "0"));
const ERR = (w, m) => errors.push(`ERROR [${w}] ${asc(m)}`);
const NOTE = (w, m) => notes.push(`WARN  [${w}] ${asc(m)}`); // advisory: printed, never fails --strict
const WARN = (w, m) => warns.push(`WARN  [${w}] ${asc(m)}`);

const HEB = /[֐-׿]/;
const nonblank = x => typeof x === "string" && x.trim().length > 0;
const isInt = x => Number.isInteger(x);
const SOURCES = new Set(["ai-draft", "ai-verified"]);
const OPT_IDS = ["a", "b", "c", "d", "e", "f", "g", "h"], OPT_TYPES = new Set(["text", "math", "image"]);
const LEVEL_KEYS = new Set(["id", "order", "icon", "title", "goal", "boss", "source", "lesson", "questions"]);
const OWN_KEYS = new Set(["id", "question", "options", "correctId", "acceptedIds", "explanation", "recap", "image"]);
const BANK_KEYS = new Set(["bankId", "recap"]);
const STEP_Q_KEYS = new Set(["id", "step", "recap"]);
const STEP_TYPES = new Set(["choice", "numeric", "text", "order", "findbug", "fillblank"]);
const STEP_KEYS = new Set(["type", "prompt", "explain", "code", "options", "correctId", "answer", "tol", "accept", "normalize", "lines", "bugIndex", "blankIndex"]);

const cfg = JSON.parse(fs.readFileSync(path.join(ROOT, "course.config.json"), "utf8"));
const needHelp = cfg.needHelp || [];
const loaded = load(ROOT);
for (const e of loaded.errors) ERR("load", e);

// ---- bank (needed only for bankId checks)
let bankIds = null;
try { bankIds = new Set(JSON.parse(fs.readFileSync(path.join(ROOT, "questions.json"), "utf8")).questions.map(q => q.id)); } catch (e) { /* reported below if needed */ }

// ---- shipped constants
{
  const ui = path.join(ROOT, "course-ui.js");
  const m = fs.existsSync(ui) && fs.readFileSync(ui, "utf8").match(/const\s+PASS\s*=\s*(\d+)/);
  if (!m) ERR("config", "course-ui.js does not define const PASS");
  else if (+m[1] < 60 || +m[1] > 100) ERR("config", `PASS=${m[1]} is not sane (expected 60-100; the design is 80)`);
}

// ---- redact list (tools/redact.txt: one name per line, # comments)
const fold = s => String(s).normalize("NFC").toLowerCase();
const REDACT_FILE = path.join(ROOT, "tools", "redact.txt");
// Full names only: a name matches as a whole word (no letter/digit/mark/underscore right before or after
// it), so it is not found inside a longer word. List prefixed forms (e.g. Hebrew ל+name) on their own line.
const WORDCH = /[\p{L}\p{N}\p{M}_]/u;
function hasName(t, n) {
  for (let i = t.indexOf(n); i !== -1; i = t.indexOf(n, i + 1)) {
    const before = [...t.slice(Math.max(0, i - 2), i)].pop();
    const after = [...t.slice(i + n.length, i + n.length + 2)][0];
    if (!(before && WORDCH.test(before)) && !(after && WORDCH.test(after))) return true;
  }
  return false;
}
if (STRICT && !fs.existsSync(REDACT_FILE)) ERR("config", "tools/redact.txt is missing (--strict needs it, even an empty commented file: student names must be checked before shipping)");
const redact = (() => {
  const p = REDACT_FILE;
  if (!fs.existsSync(p)) return [];
  return fs.readFileSync(p, "utf8").replace(/^﻿/, "").split(/\r?\n/).map(l => l.split("#")[0].trim()).filter(Boolean).map(fold);
})();

function* strings(x, p) {
  if (typeof x === "string") yield [p, x];
  else if (Array.isArray(x)) for (let i = 0; i < x.length; i++) yield* strings(x[i], `${p}[${i}]`);
  else if (x && typeof x === "object") for (const k of Object.keys(x)) yield* strings(x[k], p ? `${p}.${k}` : k);
}
const CTRL = /[\x00-\x08\x0b\x0c\x0e-\x1f]|\t(?:imes|ext|heta|au|ilde)|\n(?:eq|otin|abla|ot\b|eg\b)/;
const MATH = /\$\$([\s\S]+?)\$\$|(?<![$\\])\$([^$\n]+?)\$/g;

function textChecks(w, p, s) {
  if (/[0-9)}](?:cdot|times|neq|leq|geq|frac|sqrt|ldots|dots|infty)\b/.test(s)) ERR(w, `${p}: a TeX command lost its backslash (e.g. 2cdot): in a normal JS string write \\cdot, or use String.raw`);
  if (CTRL.test(s)) ERR(w, `${p}: control character (a TeX backslash was eaten by a JS string escape, e.g. \\frac or \\times; write the text with String.raw\`...\`)`);
  const t = fold(s);
  redact.forEach((n, i) => { if (hasName(t, n)) ERR(w, `${p}: redact.txt entry #${i + 1} found (author names must not ship)`); });
}
function mathChecks(w, p, s) {
  // fenced ``` code blocks are literal (no math); an unclosed fence is an error
  if (s.includes("```")) {
    const lines = s.replace(/\r\n/g, "\n").split("\n"), keep = [];
    for (let i = 0; i < lines.length; i++) {
      if (/^```[A-Za-z0-9+#_-]{0,12}[ \t]*$/.test(lines[i])) {
        let j = i + 1; while (j < lines.length && !/^```[ \t]*$/.test(lines[j])) j++;
        if (j >= lines.length) { ERR(w, `${p}: unclosed \`\`\` code fence`); break; }
        i = j;
      } else keep.push(lines[i]);
    }
    s = keep.join("\n");
  }
  // inline figures: a line of exactly ![alt](images/exams/<file>.png); the file must exist
  if (s.includes("![")) {
    const keep = [];
    for (const ln of s.replace(/\r\n/g, "\n").split("\n")) {
      const im = /^!\[([^\]\n]*)\]\((images\/exams\/[A-Za-z0-9._-]+\.png)\)[ \t]*$/.exec(ln);
      if (im) { if (!fs.existsSync(path.join(ROOT, im[2]))) ERR(w, `${p}: image file missing ${im[2]}`); }
      else if (/^\s*!\[/.test(ln)) ERR(w, `${p}: an inline figure must be a line of exactly ![alt](images/exams/<file>.png)`);
      else keep.push(ln);
    }
    s = keep.join("\n");
  }
  let m; MATH.lastIndex = 0;
  while ((m = MATH.exec(s))) {
    const tex = m[1] != null ? m[1] : m[2];
    if (HEB.test(tex)) ERR(w, `${p}: Hebrew inside a math span`);
    if (!tex.trim()) ERR(w, `${p}: empty math span`);
  }
}

// ---- per level
function lintStepQuestion(w, q, label, ctx) {
  for (const k of Object.keys(q)) if (!STEP_Q_KEYS.has(k)) ERR(w, `question ${label}: unknown key '${k}' on a step question`);
  if (!nonblank(q.id)) ERR(w, `question ${label}: a step question needs an id`);
  else if (ctx.qids.has(q.id)) ERR(w, `question ${label}: duplicate question id in this course`);
  else ctx.qids.add(q.id);
  if (!nonblank(q.recap)) WARN(w, `question ${label}: no recap (the summary shows it when the question is missed)`);
  const s = q.step, sw = `question ${label} step`;
  if (!s || typeof s !== "object") return ERR(w, `${sw}: must be an object`);
  if (!STEP_TYPES.has(s.type)) return ERR(w, `${sw}: type '${s.type}' is not one of ${[...STEP_TYPES]}`);
  for (const k of Object.keys(s)) {
    if (/Html$/.test(k)) ERR(w, `${sw}: derived field '${k}' must not be authored`);
    else if (!STEP_KEYS.has(k)) ERR(w, `${sw}: unknown key '${k}'`);
  }
  if (!nonblank(s.prompt)) ERR(w, `${sw}: empty prompt`);
  else mathChecks(w, `${sw} prompt`, s.prompt);
  if (s.explain != null && !nonblank(s.explain)) ERR(w, `${sw}: explain must be non-blank when present`);
  else if (!s.explain) WARN(w, `${sw}: no explain (say why the answer is right)`);
  else mathChecks(w, `${sw} explain`, s.explain);
  const lines = Array.isArray(s.lines) ? s.lines : null;
  const needLines = () => { if (!lines || lines.length < 2 || !lines.every(nonblank)) ERR(w, `${sw}: lines must be a list of >= 2 non-blank strings`); };
  const needOptions = () => {
    const opts = Array.isArray(s.options) ? s.options : [];
    const ids = opts.map(o => o && o.id);
    if (opts.length < 2) ERR(w, `${sw}: needs at least 2 options`);
    if (new Set(ids).size !== ids.length) ERR(w, `${sw}: duplicate option ids [${ids}]`);
    opts.forEach(o => { if (!o || !OPT_IDS.includes(o.id) || !nonblank(o.value)) ERR(w, `${sw}: every option needs an id a..h and a value`); });
    if (!ids.includes(s.correctId)) ERR(w, `${sw}: correctId '${s.correctId}' is not among the options [${ids}]`);
  };
  switch (s.type) {
    case "choice": needOptions(); break;
    case "numeric":
      if (typeof s.answer !== "number" || !isFinite(s.answer)) ERR(w, `${sw}: numeric answer must be a number`);
      if (s.tol != null && (typeof s.tol !== "number" || s.tol < 0)) ERR(w, `${sw}: tol must be a number >= 0`);
      break;
    case "text":
      if (!Array.isArray(s.accept) || !s.accept.length || !s.accept.every(nonblank)) ERR(w, `${sw}: accept must be a non-empty list of strings`);
      break;
    case "order": needLines(); break;
    case "findbug":
      needLines();
      if (!isInt(s.bugIndex) || !lines || s.bugIndex < 0 || s.bugIndex >= lines.length) ERR(w, `${sw}: bugIndex ${s.bugIndex} is out of range`);
      break;
    case "fillblank":
      needLines(); needOptions();
      if (!isInt(s.blankIndex) || !lines || s.blankIndex < 0 || s.blankIndex >= lines.length) ERR(w, `${sw}: blankIndex ${s.blankIndex} is out of range`);
      else if (!String(lines[s.blankIndex]).includes("___")) ERR(w, `${sw}: line blankIndex must contain the ___ placeholder`);
      break;
  }
}

function lintQuestion(w, q, i, ctx) {
  const label = (q && (q.id || q.bankId)) || `#${i + 1}`;
  const qw = `${w}`;
  if (!q || typeof q !== "object") return ERR(qw, `question ${label}: must be an object`);
  if ("bankId" in q) {
    for (const k of Object.keys(q)) if (!BANK_KEYS.has(k)) ERR(qw, `question ${label}: unknown key '${k}' on a bankId question`);
    if (!nonblank(q.bankId)) return ERR(qw, `question ${label}: empty bankId`);
    ctx.bank++;
    if (!bankIds) ERR(qw, `question ${label}: bankId '${q.bankId}' cannot be checked, the bank is not built (run tools/build_questions.py)`);
    else if (!bankIds.has(q.bankId)) ERR(qw, `question ${label}: bankId '${q.bankId}' is not in the built bank`);
    if (ctx.bankSeen.has(q.bankId)) WARN(qw, `bankId '${q.bankId}' appears twice in this level`);
    ctx.bankSeen.add(q.bankId);
    if (q.recap != null && !nonblank(q.recap)) ERR(qw, `question ${label}: recap must be non-blank text`);
    return;
  }
  if ("step" in q) return lintStepQuestion(qw, q, label, ctx);
  for (const k of Object.keys(q)) {
    if (/Html$/.test(k)) ERR(qw, `question ${label}: derived field '${k}' must not be authored (the build derives it)`);
    else if (!OWN_KEYS.has(k)) ERR(qw, `question ${label}: unknown key '${k}'`);
  }
  if (!nonblank(q.id)) ERR(qw, `question #${i + 1}: missing id`);
  else if (ctx.qids.has(q.id)) ERR(qw, `question ${label}: duplicate question id in this course`);
  else ctx.qids.add(q.id);
  if (!nonblank(q.question)) ERR(qw, `question ${label}: empty question`);
  const opts = Array.isArray(q.options) ? q.options : [];
  if (opts.length < 2 || opts.length > 8) ERR(qw, `question ${label}: needs 2-8 options (has ${opts.length})`);
  const ids = opts.map(o => o && o.id);
  if (new Set(ids).size !== ids.length) ERR(qw, `question ${label}: duplicate option ids [${ids}]`);
  opts.forEach(o => {
    const ow = `question ${label} option ${o && o.id}`;
    if (!o || typeof o !== "object") return ERR(qw, `${ow}: must be an object`);
    for (const k of Object.keys(o)) if (!["id", "type", "value"].includes(k)) ERR(qw, `${ow}: unknown key '${k}'`);
    if (!OPT_IDS.includes(o.id)) ERR(qw, `${ow}: option id must be one of a..h`);
    if (o.type != null && !OPT_TYPES.has(o.type)) ERR(qw, `${ow}: bad type '${o.type}'`);
    if (!nonblank(o.value)) ERR(qw, `${ow}: blank value`);
    else if (o.type === "math" && HEB.test(o.value)) ERR(qw, `${ow}: Hebrew inside a math option`);
    else if (o.type === "image" && !fs.existsSync(path.join(ROOT, o.value))) ERR(qw, `${ow}: image file missing ${o.value}`);
  });
  if (!ids.includes(q.correctId)) ERR(qw, `question ${label}: correctId '${q.correctId}' is not among the options [${ids}]`);
  if (q.acceptedIds != null) {
    if (!Array.isArray(q.acceptedIds) || q.acceptedIds.length < 2) ERR(qw, `question ${label}: acceptedIds only when more than one answer is accepted (list of >=2)`);
    else {
      if (q.acceptedIds.some(a => !ids.includes(a))) ERR(qw, `question ${label}: acceptedIds has an id that is not among the options`);
      if (q.acceptedIds[0] !== q.correctId) ERR(qw, `question ${label}: acceptedIds must start with correctId`);
    }
  }
  if (!nonblank(q.explanation)) ERR(qw, `question ${label}: missing explanation (say why the answer is right and why each distractor is wrong)`);
  if (!nonblank(q.recap)) WARN(qw, `question ${label}: no recap (the summary shows it when the question is missed)`);
  if (q.image && !fs.existsSync(path.join(ROOT, q.image))) ERR(qw, `question ${label}: image file missing ${q.image}`);
  for (const f of ["question", "explanation", "recap"]) if (typeof q[f] === "string") mathChecks(qw, `question ${label} ${f}`, q[f]);
  opts.forEach(o => { if (o && (o.type || "text") === "text" && typeof o.value === "string") mathChecks(qw, `question ${label} option ${o.id}`, o.value); });
}

function lintLevel(courseId, L, file, seen, isLast) {
  const w = `${courseId}/${(L && L.id) || path.basename(file, ".js")}`;
  if (!L || typeof L !== "object") return ERR(w, "level must be an object");
  for (const k of Object.keys(L)) if (!LEVEL_KEYS.has(k)) ERR(w, `unknown level key '${k}'`);
  if (!nonblank(L.id) || !/^[A-Za-z0-9_-]+$/.test(L.id)) ERR(w, `level id '${L.id}' must match [A-Za-z0-9_-]+`);
  else if (L.id !== path.basename(file, ".js")) WARN(w, `level id '${L.id}' differs from its file name ${path.basename(file)}`);
  if (seen.ids.has(L.id)) ERR(w, `duplicate level id '${L.id}' in course ${courseId}`);
  seen.ids.add(L.id);
  if (!isInt(L.order) || L.order < 1) ERR(w, `order must be a positive integer (got ${JSON.stringify(L.order)})`);
  else if (seen.orders.has(L.order)) ERR(w, `duplicate order ${L.order} in course ${courseId}`);
  else seen.orders.add(L.order);
  for (const k of ["icon", "title", "goal"]) if (!nonblank(L[k])) ERR(w, `missing ${k}`);
  if (L.boss != null && typeof L.boss !== "boolean") ERR(w, "boss must be true/false");
  if (!SOURCES.has(L.source)) ERR(w, `source must be one of ${[...SOURCES]} (labels the authored content like steps are labelled; got ${JSON.stringify(L.source)})`);
  else if (L.source === "ai-draft") (STRICT ? ERR : WARN)(w, "content is still an ai-draft (not verified yet)");
  const les = L.lesson;
  if (!les || typeof les !== "object" || !nonblank(les.html)) ERR(w, "lesson.html is missing (every level opens with a lesson: teach before you ask)");
  else {
    for (const k of Object.keys(les)) if (!["html", "figs"].includes(k)) ERR(w, `unknown lesson key '${k}'`);
    mathChecks(w, "lesson.html", les.html);
    if (les.figs != null) {
      if (!Array.isArray(les.figs)) ERR(w, "lesson.figs must be a list of {src, alt?, caption?}");
      else les.figs.forEach((f, i) => { if (!f || !nonblank(f.src) || !fs.existsSync(path.join(ROOT, f.src))) ERR(w, `lesson.figs[${i}]: image file missing ${f && f.src}`); });
    }
  }
  const qs = L.questions;
  if (!Array.isArray(qs) || !qs.length) { ERR(w, "questions must be a non-empty list"); return { bank: 0 }; }
  if (qs.length < 3) WARN(w, `only ${qs.length} questions (a level quiz wants 3-8)`);
  const ctx = { bank: 0, qids: seen.qids, bankSeen: new Set() };
  qs.forEach((q, i) => lintQuestion(w, q, i, ctx));
  for (const [p, s] of strings(L, "")) textChecks(w, p, s);
  if (L.boss && ctx.bank === 0) ERR(w, "the boss level must be built from real exam questions (add {bankId: ...} questions)");
  if (STRICT && (L.boss === true || isLast) && ctx.bank < 3) ERR(w, `the boss level needs >= 3 real exam questions (bankId, present in the bank and not held); has ${ctx.bank}`);
  if (!L.boss && ctx.bank === 0) NOTE(w, "no real exam question (bankId) in this level; early levels are drills, only the boss must use real exam questions");
  return ctx;
}

// ---- per course
const byCourse = {};
for (const e of loaded.levels) (byCourse[e.courseId] = byCourse[e.courseId] || []).push(e);
const declared = new Set(needHelp.map(c => c.id));
for (const d of loaded.courseDirs) if (!declared.has(d)) ERR(d, `courses/${d} is not declared in course.config.json needHelp`);
for (const c of needHelp) if (!(byCourse[c.id] || []).length) WARN(c.id, "declared in needHelp but has no level files in courses/" + c.id);

for (const courseId of Object.keys(byCourse).sort()) {
  if (ONLY && ONLY !== courseId) continue;
  const entries = byCourse[courseId];
  const seen = { ids: new Set(), orders: new Set(), qids: new Set() };
  const lv = entries.map(e => e.level).filter(l => l && isInt(l.order)).sort((a, b) => a.order - b.order);
  for (const e of entries) lintLevel(courseId, e.level, e.file, seen, lv.length > 0 && e.level === lv[lv.length - 1]);
  const bosses = lv.filter(l => l.boss === true);
  if (bosses.length > 1) ERR(courseId, `more than one boss level (${bosses.map(b => b.id)})`);
  if (bosses.length === 1 && lv[lv.length - 1] !== bosses[0]) ERR(`${courseId}/${bosses[0].id}`, "the boss must be the last level of the course");
  if (!bosses.length) WARN(courseId, "no boss level (the last level should be a mixed exam-sized final with boss: true)");
  if (lv.some((l, i) => l.order !== i + 1) && lv.every(l => isInt(l.order))) WARN(courseId, `level orders are not 1..${lv.length} without gaps`);
  if (lv.length < 6 || lv.length > 10) WARN(courseId, `${lv.length} levels (the design is 6-10 per course)`);
}

for (const m of notes) console.log(m);
for (const m of warns) console.log(STRICT ? m.replace("WARN ", "ERROR") : m);
for (const m of errors) console.log(m);
const bad = errors.length + (STRICT ? warns.length : 0);
const nQ = loaded.levels.reduce((s, e) => s + ((e.level && e.level.questions) || []).length, 0);
console.log(`\ncourses: ${Object.keys(byCourse).length}, levels: ${loaded.levels.length}, questions: ${nQ}, errors: ${errors.length}, warnings: ${warns.length + notes.length}`);
process.exit(bad ? 1 : 0);
