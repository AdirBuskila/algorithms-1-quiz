// Headless DOM test (jsdom, no browser):  node tools/verify_dom.js
// Boots index.html + the built bank (questions.js, courses.js) + normalize.js/steps.js/app.js and checks the
// open engine end to end. Nothing is hardcoded to a course: the store prefix comes from course.config.json,
// exam codes / question ids / step types / kinds come from the built bank.
//
//  (a) GENERIC checks, any bank:
//      1 boot (no console errors)          2 boot + open a question with throwing localStorage
//      3 the first question of every kind present (+ one per step type present): answer every step
//        right -> check, wrong -> cross + the correct answer revealed; mcq / true-false answered
//      4 dir=ltr on code/math in step widgets   5 "just show me"   6 rubric self-score
//      7 exam simulation total                  8 guided "need help?" courses (map, lesson, quiz of every
//        item type, summary, bank jump, blocked storage) for every needHelp course
//  (b) DEMO-A checks, only when the template's demo data (exam DEMO-A / course DEMO) is built:
//      every demo question right/wrong, progress counts, identical-line order step, the 2-level demo course.
// Env: APP_ROOT=<app folder> (default: the folder above tools/).
// Build the demo first:  py tools/gen/gen_DEMO-A.py && py tools/build_questions.py
const fs = require("fs"), path = require("path");
const { JSDOM, VirtualConsole } = require("jsdom");
const ROOT = process.env.APP_ROOT || path.join(__dirname, "..");
const html = fs.readFileSync(path.join(ROOT, "index.html"), "utf8");
const CFG = JSON.parse(fs.readFileSync(path.join(ROOT, "course.config.json"), "utf8"));
const STORE = `${CFG.storePrefix}_progress_v1`;

let fail = 0;
function assert(cond, msg) { console.log((cond ? "  ok  " : "FAIL  ") + msg); if (!cond) fail++; }

function boot(opts = {}) {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on("jsdomError", e => errors.push("jsdomError: " + (e.message || e)));
  vc.on("error", (...a) => errors.push("console.error: " + a.join(" ")));
  const dom = new JSDOM(html, { pretendToBeVisual: true, runScripts: "outside-only", url: "http://localhost/index.html" + (opts.search || ""), virtualConsole: vc });
  const { window } = dom;
  window.scrollTo = () => {};
  window.matchMedia = window.matchMedia || (q => ({ matches: false, media: q, addEventListener() {}, removeEventListener() {} }));
  window.HTMLElement.prototype.scrollIntoView = () => {};
  window.confirm = () => true;
  window.addEventListener("error", e => errors.push("window.onerror: " + e.message));
  if (opts.throwStorage) {
    const boom = () => { throw new window.Error("storage disabled"); };
    window.Storage.prototype.getItem = boom; window.Storage.prototype.setItem = boom; window.Storage.prototype.removeItem = boom;
  }
  const scripts = [...window.document.querySelectorAll("script[src]")]
    .map(s => s.getAttribute("src")).filter(s => !/^(https?:)?\/\//.test(s)).map(s => s.split("?")[0]);
  for (const f of scripts) {
    if (f === "learn.js" && !fs.existsSync(path.join(ROOT, f))) continue;   // no briefs built yet
    try { window.eval(fs.readFileSync(path.join(ROOT, f), "utf8")); }
    catch (e) { errors.push(`eval ${f}: ${e.message}`); }
  }
  const doc = window.document;
  const A = {
    window, doc, errors, scripts,
    $: s => doc.querySelector(s), $$: s => [...doc.querySelectorAll(s)],
    click(el) { if (!el) throw new Error("click: no element"); el.dispatchEvent(new window.MouseEvent("click", { bubbles: true, cancelable: true })); },
    change(el) { el.dispatchEvent(new window.Event("change", { bubbles: true })); },
    input(el, v) { el.value = v; el.dispatchEvent(new window.Event("input", { bubbles: true })); },
    setMode(m) { const r = A.$(`input[name=mode][value="${m}"]`); r.checked = true; A.change(r); },
    pickExam(code) { A.$("#examPick").value = code; A.change(A.$("#examPick")); },
    visible: el => el && !el.classList.contains("hidden"),
    qid: () => (A.$("#questionText") || {}).dataset.qid,
    progress: () => JSON.parse(window.localStorage.getItem(STORE) || "{}"),
  };
  return A;
}
const BANK = boot().window.OPEN_BANK;
const QS = BANK.questions;
const byId = id => QS.find(q => q.id === id);
const startExam = (A, code, mode = "exam") => { A.setMode(mode); A.pickExam(code); A.click(A.$("#startBtn")); };
// open one bank question in the real app: start its exam, press Next until it shows
function openQ(A, q) {
  startExam(A, q.examCode);
  for (let i = 0; i < 1000 && A.qid() !== q.id; i++) A.click(A.$("#nextBtn"));
  if (A.qid() !== q.id) throw new Error("could not reach " + q.id);
}
const examQs = code => QS.filter(q => q.examCode === code);
const hasSteps = q => Array.isArray(q.steps) && q.steps.length > 0;

/* ---- step helpers: act on a rendered .step-card ---- */
function solve(card, step, right) {
  const win = card.ownerDocument.defaultView;
  const q = s => card.querySelector(s);
  const click = el => el.dispatchEvent(new win.MouseEvent("click", { bubbles: true, cancelable: true }));
  const type = (el, v) => { el.value = v; el.dispatchEvent(new win.Event("input", { bubbles: true })); };
  switch (step.type) {
    case "choice":
    case "fillblank": {
      const id = right ? step.correctId : step.options.find(o => o.id !== step.correctId).id;
      click(q(`.s-opt[data-id="${id}"]`)); break;
    }
    case "numeric": type(q("input.s-input"), right ? String(step.answer).replace(".", ",") : String(step.answer + 1000)); click(q(".s-check")); break;
    case "text": type(q("input.s-input"), right ? step.accept[0] : "zzz-wrong"); click(q(".s-check")); break;
    case "findbug": {
      const i = right ? step.bugIndex : step.lines.findIndex((_, j) => j !== step.bugIndex);
      click(q(`.s-line[data-i="${i}"]`)); break;
    }
    case "order": {
      let seq = [...Array(step.lines.length).keys()];
      if (!right) { seq.reverse(); if (seq.every((v, i) => step.lines[v] === step.lines[i])) return false; }   // cannot be wrong
      for (const i of seq) click(q(`.s-pool .s-line[data-i="${i}"]`));
      click(q(".s-check")); break;
    }
    default: throw new Error("unknown step type " + step.type);
  }
  return true;
}
const resultOf = card => card.querySelector(".s-result");

// What to exercise: the first question of every kind present, preferring one with steps; plus the first
// question holding each step type that is not covered yet.
const KINDS = [...new Set(QS.map(q => q.kind))];
const PICKS = [];
for (const k of KINDS) { const of = QS.filter(q => q.kind === k); PICKS.push(of.find(hasSteps) || of[0]); }
{
  const seen = new Set(PICKS.flatMap(q => (q.steps || []).map(s => s.type)));
  for (const q of QS) {
    const miss = (q.steps || []).map(s => s.type).filter(t => !seen.has(t));
    if (miss.length) { PICKS.push(q); miss.forEach(t => seen.add(t)); }
  }
}
const PICKS_U = [...new Set(PICKS)];
const DEMO = BANK.meta.exams.some(e => e.examCode === "DEMO-A");

/* 1. boots with no console errors */
console.log("1. boot");
{
  const A = boot();
  const B = A.window.OPEN_BANK;
  assert(B && Array.isArray(B.questions) && B.questions.length > 0, "OPEN_BANK loaded with questions: " + QS.length);
  const SCRIPTS = ["questions.js", "learn.js", "courses.js", "normalize.js", "steps.js", "aiprompt.js", "app.js", "feedback.js", "course-ui.js"];
  assert(A.scripts.join() === SCRIPTS.join(), "scripts: " + A.scripts.join(", "));
  assert(A.doc.documentElement.getAttribute("dir") === "rtl", "page is dir=rtl");
  assert(B.meta.course.storePrefix === CFG.storePrefix, `bank meta storePrefix == course.config.json (${CFG.storePrefix})`);
  assert(A.$$("#topicGrid .topic-btn").length === B.meta.topics.length + 1, "topic buttons = topics + all");
  assert(A.doc.title === B.meta.course.title, "title configured from meta: " + A.doc.title);
  assert(A.doc.documentElement.style.getPropertyValue("--brand") === B.meta.course.accent, "accent applied to --brand");
  assert(!A.$("#startBtn").disabled, "start enabled");
  assert(A.errors.length === 0, "no errors: " + A.errors.join(" | "));
}

/* 2. localStorage throws */
console.log("2. throwing localStorage");
{
  const A = boot({ throwStorage: true });
  assert(A.errors.length === 0, "boots without errors: " + A.errors.join(" | "));
  const q = QS.find(x => x.kind !== "mcq" && x.kind !== "truefalse" && x.rubric) || QS[0];
  openQ(A, q);
  assert(A.visible(A.$("#screen-question")), "question screen shown");
  if (A.$(".sol-panel > summary")) A.click(A.$(".sol-panel > summary"));
  A.$$(".rubric input[type=checkbox]").forEach(c => { c.checked = true; A.change(c); });
  A.click(A.$("#nextBtn"));
  assert(A.errors.length === 0, "completes a question with no errors: " + A.errors.join(" | "));
}

/* 3. the first question of every kind (+ every step type): right -> check, wrong -> cross + reveal */
console.log("3. kinds and steps in the app: " + KINDS.join(","));
for (const mode of ["right", "wrong"]) {
  const A = boot();
  for (const q of PICKS_U) {
    openQ(A, q);
    const tag = `${mode} ${q.id} (${q.kind})`;
    assert(A.qid() === q.id, `${tag}: shown`);
    if (q.kind === "mcq") {
      const acc = q.acceptedIds || [q.correctId];
      const pick = mode === "right" ? q.correctId : q.options.find(o => !acc.includes(o.id)).id;
      A.click(A.$(`#mcqOptions .opt[data-oid="${pick}"]`));
      assert(A.$$("#mcqOptions .opt.correct").length >= 1, `${tag}: the correct option is shown`);
      assert(mode === "right" || A.$$("#mcqOptions .opt.wrong").length === 1, `${tag}: a wrong pick is marked`);
    } else if (q.kind === "truefalse") {
      A.click(A.$(`.tf-btn[data-v="${String(mode === "right" ? q.verdict : !q.verdict)}"]`));
      assert(A.$("#tfResult").classList.contains(mode === "right" ? "good" : "bad"), `${tag}: verdict graded`);
    }
    const cards = A.$$(".step-card");
    assert(cards.length === (q.steps || []).length, `${tag}: ${cards.length} step cards`);
    let graded = 0;
    (q.steps || []).forEach((st, i) => {
      if (!solve(cards[i], st, mode === "right")) return;      // an order step with identical lines cannot be wrong
      graded++;
      const r = resultOf(cards[i]);
      assert(r && r.classList.contains(mode === "right" ? "good" : "bad"), `${tag} step ${i + 1} (${st.type}) -> ${mode === "right" ? "ok" : "wrong"}`);
      if (mode === "wrong") assert(cards[i].querySelector(".s-reveal, .s-opt.correct, .s-line.bug"), `${tag} step ${i + 1}: correct answer revealed`);
      if (mode === "wrong" && st.type === "text") assert(cards[i].querySelector(".s-reveal bdi[dir=ltr]"), `${tag} step ${i + 1}: text reveal is bdi dir=ltr`);
      if (st.explainHtml) assert(cards[i].querySelector(".s-explain"), `${tag} step ${i + 1}: explanation shown`);
    });
    if (hasSteps(q) && mode === "right") {
      const sum = A.$(".steps-panel > summary").textContent;
      assert(sum.includes(`${q.steps.length}/${q.steps.length}`), `${tag}: summary count "${sum.trim().replace(/\s+/g, " ")}"`);
    }
    if (hasSteps(q) && mode === "right") {
      const pq = A.progress().perQ[q.id];
      assert(pq && pq.stepsOk === pq.stepsTotal && pq.stepsTotal === graded, `${tag}: progress records stepsOk/stepsTotal ${JSON.stringify(pq)}`);
    }
  }
  assert(A.errors.length === 0, `${mode}: no errors ${A.errors.join(" | ")}`);
}

/* 4. bidi: every code/math inside step widgets is dir=ltr */
console.log("4. dir=ltr in step widgets");
{
  const A = boot();
  let n = 0, bad = 0;
  for (const q of PICKS_U.filter(hasSteps)) {
    openQ(A, q);
    const cards = A.$$(".step-card");
    const all = () => cards.flatMap(c => [...c.querySelectorAll("code, math")]).filter(e => !e.closest("pre.code-block[dir=ltr]"));
    let b = all().filter(e => e.getAttribute("dir") !== "ltr"); n += all().length;
    q.steps.forEach((st, i) => solve(cards[i], st, false));
    b = b.concat(all().filter(e => e.getAttribute("dir") !== "ltr")); n += all().length;
    bad += b.length;
    assert(b.length === 0, `${q.id}: all code/math in steps dir=ltr`);
  }
  assert(PICKS_U.some(hasSteps) ? n > 0 : true, "checked " + n + " code/math elements");
}

/* 5. just-show-me renders the solution with no interaction */
console.log("5. just show me");
{
  const q = QS.find(x => x.kind !== "mcq" && x.kind !== "truefalse" && x.solutionHtml);
  if (!q) console.log("  skip  no open question with a solution in this bank");
  else {
    const A = boot();
    const jt = A.$("#justShow"); jt.checked = true; A.change(jt);
    openQ(A, q);
    const sol = A.$(".sol-panel");
    assert(sol && sol.hasAttribute("open"), "solution panel open by default");
    assert(sol.querySelector(".solution-text") && sol.querySelector(".solution-text").textContent.trim().length > 0, "solution text rendered");
    if (hasSteps(q)) assert(!A.$(".steps-panel").hasAttribute("open"), "steps collapsed");
    if (q.rubric) assert(A.$(".sol-panel .rubric"), "rubric visible with the solution");
    assert(A.progress().justShow === true, "justShow persisted");
    const B = boot(); openQ(B, q);
    assert(!B.$(".sol-panel").hasAttribute("open"), "default: solution collapsed");
    if (hasSteps(q)) assert(B.$(".steps-panel").hasAttribute("open"), "default: steps open");
    assert(B.$("#jumpSol"), "jump-to-solution shortcut present");
    B.click(B.$("#jumpSol"));
    assert(B.$(".sol-panel").hasAttribute("open"), "shortcut opens solution");
    assert(A.errors.length + B.errors.length === 0, "no errors");
  }
}

/* 6. ticking every rubric item -> selfScore == max */
console.log("6. rubric self-score");
{
  const q = QS.find(x => x.rubric && x.rubric.length);
  if (!q) console.log("  skip  no question with a rubric in this bank");
  else {
    const A = boot();
    openQ(A, q);
    const boxes = A.$$(".rubric input[type=checkbox]");
    assert(boxes.length === q.rubric.length, `${q.id}: rubric items rendered: ${boxes.length}`);
    boxes.forEach(c => { c.checked = true; A.change(c); });
    const r = A.progress().perQ[q.id];
    assert(r && r.max === q.pointsTotal && r.selfScore === r.max, `selfScore ${r && r.selfScore} == max ${r && r.max}`);
    const tot = A.$(".rubric-total").textContent;
    assert(new RegExp(`${q.pointsTotal}\\s*/\\s*${q.pointsTotal}`).test(tot), "live total shown: " + tot.trim());
    boxes[0].checked = false; A.change(boxes[0]);
    const r2 = A.progress().perQ[q.id];
    assert(r2.selfScore === r2.max - q.rubric[0].points, "unticking lowers the score");
    assert(A.errors.length === 0, "no errors");
  }
}

/* 7. exam simulation shows a total */
console.log("7. exam simulation");
{
  // a sitting whose questions are all on hold ships nothing: it must not be offered, and the sim runs on one that does
  const shipped = BANK.meta.exams.map(e => e.examCode).filter(c => examQs(c).length > 0);
  const code = shipped[0];
  const exam = examQs(code);
  const A = boot();
  const offered = A.$$("#examPick option").map(o => o.value);
  assert(offered.length === shipped.length && offered.every(c => shipped.includes(c)), "exam picker lists only sittings with shipped questions: " + offered.join(","));
  A.setMode("sim"); A.pickExam(code);
  assert(A.visible(A.$("#examOpts")), "sim options visible");
  A.click(A.$("#startBtn"));
  assert(A.visible(A.$("#screen-question")), "sim started: " + code);
  assert(!A.$(".sol-panel") && !A.$(".steps-panel"), "no steps/solution during the sitting");
  assert(A.$("#tmr"), "timer shown");
  for (let k = 0; k < exam.length; k++) {
    const q = byId(A.qid());
    if (q.kind === "mcq") A.click(A.$(`#mcqOptions .opt[data-oid="${q.correctId}"]`));
    else { const ta = A.$("#attempt"); if (ta) A.input(ta, "תשובה " + k); }
    if (k < exam.length - 1) A.click(A.$("#nextBtn"));
  }
  A.click(A.$("#submitExamBtn"));
  assert(A.visible(A.$("#screen-results")), "results screen shown");
  const maxPts = exam.reduce((s, q) => s + (q.pointsTotal || 0), 0);
  const mcqPts = exam.filter(q => q.kind === "mcq").reduce((s, q) => s + (q.pointsTotal || 0), 0);
  const txt = () => A.$("#resultsTotal").textContent.replace(/\s+/g, " ").trim();
  assert(new RegExp(`^${mcqPts} / ${maxPts}`).test(txt()), `auto-scored mcq counted: "${txt()}" starts with ${mcqPts} / ${maxPts}`);
  A.$$("#screen-results .rubric input[type=checkbox]").forEach(c => { c.checked = true; A.change(c); });
  const rubricMax = exam.reduce((s, q) => s + (q.kind === "mcq" ? q.pointsTotal || 0 : (q.rubric ? q.pointsTotal : 0)), 0);
  assert(new RegExp(`^${rubricMax} / ${maxPts}`).test(txt()), `all rubrics ticked -> ${rubricMax} / ${maxPts}: "${txt()}"`);
  assert(A.$$("#screen-results .rev").length === exam.length, "one review block per question");
  assert(A.errors.length === 0, "no errors: " + A.errors.join(" | "));
}

/* 7b. learn mode (learn.js from tools/build_learn.py); skipped when absent or empty */
console.log("7b. learn mode");
{
  const A = boot();
  const L = A.window.LEARN;
  const ch = Array.isArray(L) ? L : ((L || {}).chapters || []);
  if (!ch.length) {
    console.log("learn: none built yet (skipped)");
    assert(A.$("#learnEntry").style.display === "none", "learn entry hidden (no chapters)");
  } else {
    const TOPIC_KEYS = new Set(A.$$("#topicGrid .topic-btn").map(b => b.dataset.topic).filter(t => t !== "all"));
    const qids = new Set(QS.map(q => q.id));
    const chIds = ch.map(c => c.id);
    assert(A.$("#learnEntry").style.display !== "none", "learn entry visible");
    assert(new Set(chIds).size === chIds.length && chIds.every(Boolean), `learn: ${chIds.length} chapters, unique ids`);
    assert(ch.every(c => c.title && c.html), "learn: every chapter has a title and html");
    const badTopic = ch.filter(c => c.topic && !TOPIC_KEYS.has(c.topic)).map(c => c.id);
    assert(badTopic.length === 0, `learn: chapter topics are in the closed topic list${badTopic.length ? " BAD: " + badTopic : ""}`);
    const covered = new Set(ch.filter(c => c.kind !== "cheat").map(c => c.topic));
    for (const t of TOPIC_KEYS) if (!covered.has(t)) console.log(`WARN  learn: topic "${t}" has no brief`);
    const dangling = [], deadX = [], mathBad = [], preBad = [];
    let nRefs = 0, nMath = 0;
    for (const c of ch) {
      const frag = A.doc.createElement("div"); frag.innerHTML = c.html;
      for (const b of frag.querySelectorAll(".qref")) { nRefs++; if (!qids.has(b.dataset.q)) dangling.push(`${c.id}:${b.dataset.q}`); }
      for (const a of frag.querySelectorAll(".xref")) if (!chIds.includes(a.dataset.chapter)) deadX.push(`${c.id}->${a.dataset.chapter}`);
      for (const m of frag.querySelectorAll("math")) { nMath++; if (m.getAttribute("dir") !== "ltr" || /[֐-׿]/.test(m.textContent)) mathBad.push(c.id); }
      for (const p of frag.querySelectorAll("pre")) if (p.getAttribute("dir") !== "ltr") preBad.push(c.id);
    }
    assert(dangling.length === 0, `learn: all ${nRefs} question refs resolve${dangling.length ? " DANGLING: " + dangling.join(", ") : ""}`);
    assert(deadX.length === 0, `learn: all cross-references resolve${deadX.length ? " DEAD: " + deadX.join(", ") : ""}`);
    assert(mathBad.length === 0, `learn: all ${nMath} <math> are dir=ltr with no Hebrew${mathBad.length ? " BAD in: " + [...new Set(mathBad)] : ""}`);
    assert(preBad.length === 0, "learn: every code block is dir=ltr");
    for (const c of ch) if (c.kind !== "cheat" && c.topic && !QS.some(q => q.topic === c.topic))
      console.log(`WARN  learn: chapter "${c.id}" (topic ${c.topic}) has 0 questions in the bank`);

    A.click(A.$("#learnEntry"));
    assert(A.visible(A.$("#screen-learn")), "learn: screen opens from the entry button");
    assert(A.$$("#learnToc button").length === ch.length, `learn: TOC lists ${ch.length} chapters`);
    const seen = [];
    for (let i = 0; i < ch.length; i++) {
      seen.push(A.$("#learnContent").dataset.chapter);
      if (!A.$("#learnContent .learn-h")) { assert(false, `learn: chapter ${i} has no heading`); break; }
      const t = ch[i].topic, n = t ? QS.filter(q => q.topic === t).length : 0;
      if (n && !A.$("#learnContent .learn-drill")) assert(false, `learn: chapter ${ch[i].id} missing the practice button`);
      if (i < ch.length - 1) A.click(A.$("#learnNext"));
    }
    assert(seen.join() === chIds.join(), "learn: next-button walk visits every chapter in order");
    assert(A.$("#learnNext").disabled, "learn: next disabled on the last chapter");

    const withRef = ch.findIndex(c => /class="qref"/.test(c.html));
    if (withRef >= 0) {
      A.click(A.$$("#learnToc button")[withRef]);
      const ref = A.$$("#learnContent .qref").find(b => qids.has(b.dataset.q)) || A.$("#learnContent .qref");
      A.click(ref);
      assert(A.visible(A.$("#qpeek")), `learn: clicking ${ref.dataset.q} opens the peek`);
      assert(A.$("#qpeekBody .qpeek-q") && A.$("#qpeekBody .qpeek-q").textContent.trim().length > 0, "learn: the peek shows the question text");
      A.doc.dispatchEvent(new A.window.KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
      assert(!A.visible(A.$("#qpeek")) && A.visible(A.$("#screen-learn")), "learn: Escape closes the peek, stays in learn");
    }
    const withX = ch.findIndex(c => /class="xref"/.test(c.html));
    if (withX >= 0) {
      A.click(A.$$("#learnToc button")[withX]);
      const x = A.$("#learnContent .xref");
      A.click(x);
      assert(A.$("#learnContent").dataset.chapter === x.dataset.chapter, `learn: xref jumps to ${x.dataset.chapter}`);
    }
    // "practice this topic" -> topic practice in the open app
    const di = ch.findIndex(c => c.topic && QS.some(q => q.topic === c.topic));
    if (di >= 0) {
      A.click(A.$$("#learnToc button")[di]);
      A.click(A.$("#learnContent .learn-drill"));
      const shown = byId(A.qid());
      assert(A.visible(A.$("#screen-question")) && shown && shown.topic === ch[di].topic, `learn: practice button starts ${ch[di].topic} topic practice`);
      A.click(A.$("#quitBtn"));
      assert(A.visible(A.$("#screen-start")), "learn: back on the start screen after quitting practice");
    }
    // deep link ?learn=<id>
    const last = chIds[chIds.length - 1];
    const D = boot({ search: "?learn=" + encodeURIComponent(last) });
    assert(D.visible(D.$("#screen-learn")) && D.$("#learnContent").dataset.chapter === last, `learn: deep link ?learn=${last} opens it`);
    assert(A.errors.length === 0 && D.errors.length === 0, "learn: no JS errors: " + A.errors.concat(D.errors).join(" | "));
  }
}

/* 8. guided "צריך עזרה?" courses (course-ui.js + courses.js), any needHelp list */
// a configured course is hidden until it has >= 1 built level (phase 5b writes them); only built courses are checked
const NH_CFG = (CFG.needHelp || []).length;
const NH = (() => { const W = boot().window; return (CFG.needHelp || []).filter(c => (((W.COURSES || {})[c.id] || {}).levels || []).length > 0); })();
  const KEY = id => `${CFG.storePrefix}_course_${id}_v1`;
  const bankOf = A => A.window.OPEN_BANK.questions;
  const textOf = (A, h) => { const d = A.doc.createElement("div"); d.innerHTML = h; return d.textContent.replace(/\s+/g, ""); };
  const mapState = (A, id) => { const b = A.$(`#crsMap .crs-lvl[data-id="${id}"]`); return { passed: b.classList.contains("passed"), next: b.classList.contains("next") }; };
  const openCourse = (A, id) => { A.click(A.$(`#helpCards .crs-promo[data-course="${id}"]`)); return A.window.COURSES[id].levels; };
  const ownQ = (A, id, key) => A.window.COURSES[id].levels.flatMap(L => L.questions).find(q => q.id === key);

  // answer the question on screen, right or wrong; asserts the reveal on a miss; returns its type
  function answerItem(A, cid, right, tag) {
    const qt = A.$("#crsQText"), type = qt.dataset.type, bank = bankOf(A);
    const q = qt.dataset.bank ? bank.find(x => x.id === qt.dataset.bank) : ownQ(A, cid, qt.dataset.key);
    if (type === "mcq") {
      const acc = q.acceptedIds || [q.correctId], opts = A.$$("#crsQBody .opt");
      A.click(right ? opts.find(o => acc.includes(o.dataset.oid)) : opts.find(o => !acc.includes(o.dataset.oid)));
      assert(opts.every(b => b.disabled), `${tag}: options lock after answering`);
      assert(A.$$("#crsQBody .opt.correct").map(b => b.dataset.oid).sort().join() === acc.slice().sort().join(), `${tag}: the correct option is shown`);
      if (!right) assert(A.$$("#crsQBody .opt.wrong").length === 1 && /לא נכון/.test(A.$("#crsQBody .feedback .verdict").textContent), `${tag}: a wrong pick is marked and the verdict says so`);
    } else if (type === "step") {
      const card = A.$("#crsQBody .step-card");
      const done = solve(card, q.step, right);
      if (done) {
        assert(resultOf(card).classList.contains(right ? "good" : "bad"), `${tag}: step graded ${right ? "right" : "wrong"} by Steps.render`);
        if (!right) assert(card.querySelector(".s-reveal, .s-opt.correct, .s-line.bug"), `${tag}: the correct answer is revealed`);
      } else solve(card, q.step, true);
    } else if (type === "tf") {
      A.click(A.$(`#crsQBody .tf-btn[data-v="${String(right ? q.verdict : !q.verdict)}"]`));
      assert(A.$("#crsQBody .tf-result").classList.contains(right ? "good" : "bad") && !!A.$("#crsQBody .crs-sol"), `${tag}: true/false graded, solution shown`);
    } else if (type === "steps") {
      const cards = A.$$("#crsQBody .step-card");
      assert(cards.length === q.steps.length, `${tag}: ${cards.length} guided step cards from the bank question`);
      q.steps.forEach((st, i) => solve(cards[i], st, right));
      assert(!!A.$("#crsQBody .crs-sol"), `${tag}: solution offered after the steps`);
    } else {
      A.click(A.$("#crsRevealBtn"));
      assert(!!A.$("#crsQBody .crs-sol"), `${tag}: solution revealed`);
      A.click(A.$(`#crsQBody [data-self="${right ? "ok" : "no"}"]`));
    }
    assert(!A.$("#crsNextBtn").classList.contains("hidden"), `${tag}: next button appears after answering`);
    return type;
  }
  // play a whole level: plan(i) -> true (right) | false (wrong)
  function play(A, cid, L, plan, tag) {
    A.click(A.$(`#crsMap .crs-lvl[data-id="${L.id}"]`));
    assert(A.visible(A.$("#crsLessonView")) && A.$("#crsLesson").textContent.includes(L.title), `${tag}: lesson shown first`);
    A.click(A.$("#crsLessonGo"));
    assert(A.visible(A.$("#crsQuizView")), `${tag}: quiz opens after the lesson`);
    const types = [];
    for (let i = 0; i < L.questions.length; i++) {
      const lq = L.questions[i], key = lq.bankId ? "bank:" + lq.bankId : lq.id;
      assert(A.$("#crsQText").dataset.key === key, `${tag}: question ${i + 1} is ${key}`);
      types.push(answerItem(A, cid, plan(i), `${tag} q${i + 1}`));
      A.click(A.$("#crsNextBtn"));
    }
    assert(A.visible(A.$("#crsSumView")), `${tag}: summary shown`);
    return types;
  }

console.log("8. guided courses");
{
  if (!NH.length) {
    const A = boot();
    assert(A.$("#helpEntry").style.display === "none", "course: header entry hidden (no course has levels)");
    assert(A.$$("#helpCards .crs-promo").length === 0, "course: no start-screen cards (no course has levels)");
    assert(A.$("#helpCards").classList.contains("hidden"), "course: card container hidden (no course has levels)");
    if (NH_CFG) console.log("guided courses: none built yet (skipped)");
    assert(A.errors.length === 0, "course: no errors: " + A.errors.join(" | "));
  } else {
    const A = boot();
    assert(A.$("#helpEntry").style.display !== "none", "course: header entry visible");
    const cards = A.$$("#helpCards .crs-promo");
    assert(cards.length === NH.length && NH.every(c => cards.some(k => k.dataset.course === c.id)), `course: ${NH.length} start-screen card(s), one per needHelp entry`);
    assert(cards.every(k => k.textContent.includes(NH.find(c => c.id === k.dataset.course).titleHe)), "course: each card shows its title");
    for (const C of NH) {
      const snap = A.window.localStorage.getItem(STORE);
      const cl = openCourse(A, C.id);
      assert(A.visible(A.$("#screen-course")) && A.visible(A.$("#crsMapView")), `course ${C.id}: card opens the level map`);
      assert(cl.length > 0 && A.$$("#crsMap .crs-lvl").length === cl.length, `course ${C.id}: map lists ${cl.length} levels`);
      assert(cl.every(L => !mapState(A, L.id).passed) && mapState(A, cl[0].id).next, `course ${C.id}: fresh start, first level highlighted`);
      // a wrong run reveals every correct answer, and does not pass
      play(A, C.id, cl[0], () => false, `${C.id}/${cl[0].id} all wrong`);
      assert(/0%/.test(A.$("#crsSum .big").textContent) && !/עברת את השלב/.test(A.$("#crsSum").textContent), `course ${C.id}: all wrong scores 0% and does not pass`);
      A.click(A.$('#crsSum [data-act="map"]'));
      // every level, all right: passes and unlocks the next
      for (let i = 0; i < cl.length; i++) {
        const L = cl[i];
        if (i > 0) assert(mapState(A, L.id).next, `course ${C.id}: ${L.id} highlighted after ${cl[i - 1].id}`);
        play(A, C.id, L, () => true, `${C.id}/${L.id}`);
        assert(/100%/.test(A.$("#crsSum .big").textContent), `course ${C.id}/${L.id}: all-correct scores 100%`);
        const real = A.$('#crsSum [data-act="real"]');
        if (L.boss) assert(!!real && /גמר/.test(A.$("#crsSum").textContent), `course ${C.id}/${L.id}: boss message and a jump to the real exam questions`);
        A.click(A.$('#crsSum [data-act="map"]'));
        assert(mapState(A, L.id).passed, `course ${C.id}/${L.id}: marked passed`);
      }
      const saved = JSON.parse(A.window.localStorage.getItem(KEY(C.id)));
      assert(saved && cl.every(L => saved.levels[L.id] && saved.levels[L.id].best === 100), `course ${C.id}: progress saved under ${KEY(C.id)}`);
      assert(A.window.localStorage.getItem(STORE) === snap, `course ${C.id}: course answers stay out of the bank progress`);
      // the boss jump starts bank practice on the course topic
      const bossL = cl.find(L => L.boss);
      if (bossL) {
        play(A, C.id, bossL, () => true, `${C.id} boss again`);
        const real = A.$('#crsSum [data-act="real"]');
        if (real) {
          A.click(real);
          const shown = byId(A.qid());
          assert(A.visible(A.$("#screen-question")) && shown && shown.topic === C.topic, `course ${C.id}: the jump starts bank practice on topic ${C.topic}`);
          A.click(A.$("#quitBtn"));
          assert(A.visible(A.$("#screen-start")) && A.$$("#helpCards .crs-promo").length === NH.length, "course: back on the start screen, cards still there");
          assert(new RegExp(`${cl.length} מתוך ${cl.length}`).test(A.$(`#helpCards .crs-promo[data-course="${C.id}"]`).textContent), `course ${C.id}: card reports progress (${cl.length} of ${cl.length})`);
        }
      }
      if (!A.visible(A.$("#screen-start"))) A.click(A.$("#crsHomeBtn"));
      assert(A.visible(A.$("#screen-start")), "course: back on the start screen");
    }
    assert(A.errors.length === 0, "course: no errors: " + A.errors.join(" | "));

    // blocked localStorage: the whole flow still completes in memory
    const C0 = NH[0];
    const T = boot({ throwStorage: true });
    assert(T.errors.length === 0, "course: boots with localStorage throwing: " + T.errors.join(" | "));
    const tl = openCourse(T, C0.id);
    play(T, C0.id, tl[0], () => true, "storage-blocked " + tl[0].id);
    assert(/100%/.test(T.$("#crsSum .big").textContent), "course: flow completes with localStorage throwing");
    T.click(T.$('#crsSum [data-act="map"]'));
    assert(mapState(T, tl[0].id).passed, "course: progress is kept in memory when storage throws");
    T.click(T.$("#crsResetBtn"));
    assert(!mapState(T, tl[0].id).passed, "course: reset works with storage blocked");
    assert(T.errors.length === 0, "course: no errors with blocked storage: " + T.errors.join(" | "));
  }
}

/* ======================= (b) DEMO-A specific checks ======================= */
if (!DEMO) console.log("\n(b) demo-specific checks skipped: no DEMO-A exam in this bank");
else {
  const exam = examQs("DEMO-A").sort((a, b) => a.num - b.num);

  console.log("D1. every DEMO-A question: steps right/wrong, progress counts");
  for (const mode of ["right", "wrong"]) {
    const A = boot();
    startExam(A, "DEMO-A");
    for (let k = 0; k < exam.length; k++) {
      const q = exam[k];
      assert(A.qid() === q.id, `${mode}: showing ${q.id}`);
      const cards = A.$$(".step-card");
      assert(cards.length === (q.steps || []).length, `${mode} ${q.id}: ${cards.length} step cards`);
      (q.steps || []).forEach((st, i) => {
        solve(cards[i], st, mode === "right");
        const r = resultOf(cards[i]);
        assert(r && r.classList.contains(mode === "right" ? "good" : "bad"), `${mode} ${q.id} step ${i + 1} (${st.type}) -> ${mode === "right" ? "ok" : "wrong"}`);
      });
      if (q.steps && q.steps.length) {
        const sum = A.$(".steps-panel > summary").textContent;
        assert(sum.includes(`${mode === "right" ? q.steps.length : 0}/${q.steps.length}`), `${mode} ${q.id}: summary count "${sum.trim().replace(/\s+/g, " ")}"`);
      }
      if (k < exam.length - 1) A.click(A.$("#nextBtn"));
    }
    if (mode === "right") {
      const q1 = A.progress().perQ["DEMO-A-Q1"];
      assert(q1 && q1.stepsOk === 2 && q1.stepsTotal === 2, "progress records stepsOk/stepsTotal: " + JSON.stringify(q1));
    }
    assert(A.errors.length === 0, `${mode}: no errors ${A.errors.join(" | ")}`);
  }

  console.log("D2. order step: identical lines interchangeable (the duplicate-} case)");
  {
    const A = boot();
    const step = { type: "order", prompt: "p", promptHtml: "p", code: true, lines: ["f() {", "if (x) {", "}", "}"], linesHtml: ["f() {", "if (x) {", "}", "}"] };
    const run = seq => {
      const mount = A.doc.createElement("div"); A.doc.body.appendChild(mount);
      let res = null;
      A.window.Steps.render(step, mount, r => { res = r; });
      for (const i of seq) A.click(mount.querySelector(`.s-pool .s-line[data-i="${i}"]`));
      A.click(mount.querySelector(".s-check"));
      return res;
    };
    assert(run([0, 1, 2, 3]).ok === true, "order [0,1,2,3] accepted");
    assert(run([0, 1, 3, 2]).ok === true, "order [0,1,3,2] (the two identical lines swapped) accepted");
    assert(run([1, 0, 2, 3]).ok === false, "order with swapped distinct lines rejected");
    assert(A.errors.length === 0, "no errors: " + A.errors.join(" | "));
  }

  console.log("D3. DEMO-A rubric and demo course specifics");
  {
    const A = boot();
    startExam(A, "DEMO-A");
    const q = byId("DEMO-A-Q1");
    const boxes = A.$$(".rubric input[type=checkbox]");
    boxes.forEach(c => { c.checked = true; A.change(c); });
    assert(/10\s*\/\s*10/.test(A.$(".rubric-total").textContent), "live total shown: " + A.$(".rubric-total").textContent.trim());
    assert(A.progress().perQ[q.id].max === 10, "DEMO-A-Q1 is worth 10");
  }
  const C = NH.find(c => c.id === "DEMO");  // NH = configured courses that have built levels
  if (C) {
    const A = boot();
    const cl = A.window.COURSES.DEMO.levels;
    const [L1, L2] = cl;
    assert(cl.length === 2, "demo course has 2 levels");
    A.click(A.$(`#helpCards .crs-promo[data-course="DEMO"]`));
    const typeOf = lq => {
      const q = lq.bankId ? byId(lq.bankId) : lq;
      if (lq.bankId) return q.kind === "mcq" ? "mcq" : q.kind === "truefalse" ? "tf" : (hasSteps(q) ? "steps" : "self");
      return lq.step ? "step" : "mcq";
    };
    assert(L1.questions.map(typeOf).join() === "mcq,step,step,mcq", "C01 mixes own MCQ, step widgets and a bank question: " + L1.questions.map(typeOf));
    assert(L2.boss, "the last demo level is the boss");
    const bankIds = L2.questions.filter(q => q.bankId).map(q => byId(q.bankId).kind);
    assert(bankIds.includes("truefalse") && bankIds.includes("proof"), "the demo boss pulls a true/false and a proof question: " + bankIds);
    assert(A.errors.length === 0, "no errors: " + A.errors.join(" | "));

    // the "no steps -> reveal and self-mark" branch: strip the steps of the boss's bank proof
    const B = boot();
    B.click(B.$(`#helpCards .crs-promo[data-course="DEMO"]`));
    const proof = L2.questions.filter(q => q.bankId).map(q => bankOf(B).find(x => x.id === q.bankId)).find(x => x && x.kind === "proof");
    delete proof.steps;
    const types = play(B, "DEMO", B.window.COURSES.DEMO.levels[1], () => false, "DEMO boss all wrong");
    assert(types.includes("tf") && types.includes("self"), `boss exercises tf and self-marked kinds (${types})`);
    assert(/0%/.test(B.$("#crsSum .big").textContent), "boss all wrong scores 0%");
    assert(B.errors.length === 0, "no errors: " + B.errors.join(" | "));
  }
}

/* 9. inline figures in rich text (![alt](images/exams/x.png) lines) render as clickable .rt-fig */
console.log("9. inline figures");
{
  const withFig = QS.filter(q => /rt-fig/.test(JSON.stringify(q)));
  if (!withFig.length) console.log("no inline figures in the bank (skipped)");
  else {
    const q = withFig[0], A = boot();
    openQ(A, q);
    if (A.$(".sol-panel > summary")) A.click(A.$(".sol-panel > summary"));
    const img = A.$(".rt-fig img");
    assert(!!img && !!img.getAttribute("src") && !!A.$(".rt-fig figcaption"), `${q.id}: .rt-fig renders an img with a caption`);
    assert(img && fs.existsSync(path.join(ROOT, img.getAttribute("src"))), `${q.id}: the figure file exists on disk`);
    if (img) { A.click(img); assert(A.visible(A.$("#lightbox")), "clicking the figure opens the lightbox"); }
    assert(A.errors.length === 0, "no errors: " + A.errors.join(" | "));
  }
}

/* 10. feedback links (feedback.js): footer line + per-question report links with the right mailto subjects */
console.log("10. feedback links");
{
  const mailParts = a => { const h = a.getAttribute("href"), [head, qs] = h.split("?"); const p = new URLSearchParams(qs); return { to: head.replace(/^mailto:/, ""), subject: p.get("subject"), body: p.get("body") || "" }; };
  const A = boot(), title = A.window.document.title;
  const fl = A.$("#feedbackLine a");
  assert(!!fl && /^mailto:[^@?]+@[^@?]+\?/.test(fl.getAttribute("href")), "footer feedback link is a mailto");
  assert(fl && mailParts(fl).subject === title + " — משוב", "footer link subject is '<title> — משוב': " + (fl && mailParts(fl).subject));
  assert(fl && /מצאתם טעות\?.*📩 כתבו לי ואוסיף/.test(fl.textContent), "footer link text");
  assert(!/[\w.-]+@[\w-]+\.\w+/.test(html) && !/[\w.-]+@[\w-]+\.\w+/.test(fs.readFileSync(path.join(ROOT, "feedback.js"), "utf8")), "the address is never written out literally in index.html or feedback.js");
  const q = QS.find(x => x.kind !== "mcq" && hasSteps(x)) || QS[0];
  openQ(A, q);
  const rl = A.$("#qExtras + .reportrow a.reportlink");
  assert(!!rl, "question view has a report link");
  if (rl) {
    const m = mailParts(rl);
    assert(m.subject === `${title} — טעות בשאלה ${q.id}`, "report subject: " + m.subject);
    assert(m.body.includes(q.id) && m.body.includes(q.examLabel || q.examCode || "") && m.body.includes("תחילת השאלה: "), "report body has id, exam label and a snippet");
    const snip = (m.body.match(/תחילת השאלה: (.*)\n/) || [])[1] || "";
    assert(snip.length > 0 && snip.length <= 81, "snippet length ok (" + snip.length + ")");
  }
  if (A.$(".sol-panel")) assert(!!A.$(".sol-panel .reportlink"), "solution panel has a report link");
  A.click(A.$("#nextBtn"));
  const rl2 = A.$("#qExtras + .reportrow a.reportlink");
  assert(!!rl2 && A.$$(".reportrow").length === A.$$("#screen-question .reportrow").length, "report link follows the next question");
  const A2 = boot(); const code = BANK.meta.exams.map(e => e.examCode).find(c => examQs(c).length);
  startExam(A2, code, "sim");
  { const n = examQs(code).length; for (let k = 0; k < n - 1; k++) A2.click(A2.$("#nextBtn")); A2.click(A2.$("#submitExamBtn")); }
  const revs = A2.$$("#screen-results .rev");
  assert(revs.length > 0 && revs.every(r => r.querySelector("a.reportlink")), "every exam-review block has a report link");
  if (NH.length) {
    const A3 = boot(); A3.click(A3.$(`#helpCards .crs-promo[data-course="${NH[0].id}"]`));
    A3.click(A3.$("#crsMap .crs-lvl")); A3.click(A3.$("#crsLessonGo"));
    const cl = A3.$("#crsQExtras + .reportrow a.reportlink");
    assert(!!cl && new RegExp(`טעות בשאלה ${NH[0].id}-L\\d+-Q1$`).test(mailParts(cl).subject), "course question has a report link with course-level-index id: " + (cl && mailParts(cl).subject));
  }
  assert(A.errors.length === 0 && A2.errors.length === 0, "no errors");
}

// fenced code blocks in the built bank must all be dir=ltr
{
  const qsrc = fs.readFileSync(path.join(ROOT, "questions.js"), "utf8");
  const pres = qsrc.match(/<pre class=\\?"code-block\\?"[^>]*>/g) || [];
  const badPre = pres.filter(p => !/dir=\\?"ltr\\?"/.test(p));
  assert(badPre.length === 0, `${pres.length} .code-block <pre> in the bank, all dir=ltr`);
}

console.log(fail ? `\n${fail} FAILED` : "\nall ok");
process.exit(fail ? 1 : 0);
