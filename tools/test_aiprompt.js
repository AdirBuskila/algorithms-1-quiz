// Tests for aiprompt.js:  node tools/test_aiprompt.js   (build the demo first: see verify_dom.js header)
const fs = require("fs"), path = require("path"), assert = require("assert");
const { JSDOM, VirtualConsole } = require("jsdom");
const ROOT = path.join(__dirname, "..");
const read = f => fs.readFileSync(path.join(ROOT, f), "utf8");
let fail = 0;
function t(name, fn) { try { fn(); console.log("  ok  " + name); } catch (e) { fail++; console.log("FAIL  " + name + "\n      " + e.message); } }

function boot(full) {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on("jsdomError", e => errors.push(e.message || String(e)));
  const dom = new JSDOM(read("index.html"), { pretendToBeVisual: true, runScripts: "outside-only", url: "http://localhost/index.html", virtualConsole: vc });
  const w = dom.window;
  w.scrollTo = () => {}; w.HTMLElement.prototype.scrollIntoView = () => {}; w.confirm = () => true;
  w.matchMedia = w.matchMedia || (q => ({ matches: false, media: q, addEventListener() {}, removeEventListener() {} }));
  w.opened = []; w.open = (...a) => { w.opened.push(a); return null; };
  const files = full
    ? [...w.document.querySelectorAll("script[src]")].map(s => s.getAttribute("src").split("?")[0]).filter(s => !/^(https?:)?\/\//.test(s))
    : ["aiprompt.js"];
  for (const f of files) { if (f === "learn.js" && !fs.existsSync(path.join(ROOT, f))) continue;   // optional: only built when briefs exist (same as verify_dom)
    try { w.eval(read(f)); } catch (e) { errors.push(f + ": " + e.message); } }
  return { w, errors };
}
const sleep = ms => new Promise(r => setTimeout(r, ms));
const noClipboard = w => Object.defineProperty(w.navigator, "clipboard", { value: undefined, configurable: true });
if (!fs.existsSync(path.join(ROOT, "questions.js"))) { console.log("test_aiprompt: skipped, no questions.js built yet (build the bank first: see verify_dom.js header)"); process.exit(0); }
const bank = boot(true).w.OPEN_BANK;
const AP = boot(false).w.AiPrompt;
const DEMO = bank.meta.exams.some(e => e.examCode === "DEMO-A");
const build = (q, o) => AP.build(q, Object.assign({ answerText: "ans", photo: false }, o));
// Real HTML tags only (known element names). `<stdio.h>`, `i<n`, `a<b>c` in C code or math are not tags.
const HTML_TAG = /<\/?(?:a|b|i|u|p|br|hr|em|strong|span|div|code|pre|sub|sup|img|ul|ol|li|table|thead|tbody|tr|td|th|svg|math|mrow|mi|mn|mo|semantics|annotation|font|h[1-6]|button|input|textarea|script|style|details|summary|section|figure|figcaption|blockquote|mjx-[a-z-]+)(?:\s[^<>]*)?\/?>/i;

t("API present", () => { assert.ok(AP && typeof AP.build === "function" && typeof AP.open === "function"); });
t("HTML_TAG check: catches tags, ignores comparisons and C includes", () => {
  for (const s of ["<b>x</b>", "a <span class=\"tok\">y</span>", "</div>", "<br/>", "<math dir=\"ltr\">", "<code class=\"tok\" dir=\"ltr\">int</code>"]) assert.ok(HTML_TAG.test(s), s);
  for (const s of ["for (i=0;i<n;i++) if (a[i]>b)", "$x<y$ and $y>z$", "#include <stdio.h>", "0<x<1, y>2", "if (a < b && c > d)"]) assert.ok(!HTML_TAG.test(s), s);
});

/* ---------- (a) generic: every question in the built bank ---------- */
t("bank is non-empty", () => assert.ok(bank.questions.length > 0));
t("every question builds a plain-text prompt without throwing (text answer and photo)", () => {
  for (const q of bank.questions) for (const o of [{ answerText: "ans" }, { answerText: "", photo: true }, { answerText: "" }]) {
    let s; try { s = build(q, o); } catch (e) { throw new Error(q.id + " (" + q.kind + "): " + e.message); }
    assert.strictEqual(typeof s, "string", q.id);
    assert.ok(!HTML_TAG.test(s), q.id + " has an HTML tag: " + (s.match(HTML_TAG) || [])[0]);
    assert.ok(!/undefined|\[object|NaN/.test(s), q.id + " leaks undefined/NaN");
  }
});
t("every prompt has the question text, the grading rules and the output format", () => {
  for (const q of bank.questions) {
    const s = build(q);
    assert.ok(s.includes(String(q.question).trim()), q.id + " question");
    assert.ok(s.includes("לפי המחוון") && s.includes("טיפ אחד"), q.id + " common sections");
    assert.ok(s.includes("התשובה שלי:\nans") && !s.includes("מצורפת תמונה"), q.id + " answer");
  }
});
t("solution (when present) is included and labelled by q.official", () => {
  for (const q of bank.questions) {
    if (!String(q.solution || "").trim()) continue;
    const s = build(q);
    assert.ok(s.includes((q.official ? "הפתרון הרשמי:\n" : "פתרון לדוגמה (לא רשמי):\n") + String(q.solution).trim()), q.id);
    assert.ok(q.official || (q.question + q.solution).includes("הפתרון הרשמי") || !s.includes("הפתרון הרשמי"), q.id + " unofficial never called official");
  }
});
t("questions without a solution: mcq gets options + correct answer, others a clear note, no empty section", () => {
  let n = 0;
  for (const q of bank.questions) {
    if (String(q.solution || "").trim()) continue;
    n++; const s = build(q);
    assert.ok(!/(הפתרון הרשמי|פתרון לדוגמה \(לא רשמי\)):\n\n/.test(s), q.id + " empty solution block");
    if (Array.isArray(q.options) && q.options.length && q.correctId != null) {
      assert.ok(s.includes("האפשרויות:") && s.includes("התשובה הנכונה: " + q.correctId), q.id);
      for (const o of q.options) assert.ok(s.includes(o.id + ". "), q.id + " option " + o.id);
    } else assert.ok(s.includes("אין פתרון זמין"), q.id);
  }
  console.log("      (" + n + " questions without a solution field)");
});
t("every rubric line + its points appear; no rubric -> no rubric section", () => {
  for (const q of bank.questions) {
    const s = build(q), rub = Array.isArray(q.rubric) ? q.rubric : [];
    if (!rub.length) { assert.ok(!s.includes("המחוון:"), q.id + " rubric section without rubric"); continue; }
    for (const r of rub) {
      assert.ok(s.includes(String(r.text).trim()), q.id + " " + r.text);
      if (r.points != null) assert.ok(s.includes(r.points + " נק"), q.id + " pts");
    }
  }
});
t("kind-specific instruction present for every known kind", () => {
  const marks = { proof: "תקפות לוגית", computation: "השורה השגויה הראשונה, ורק", algorithm: "סיבוכיות", code: "מקרי קצה", truefalse: "נכון/לא נכון", mcq: "אמריקאית" };
  for (const q of bank.questions) if (marks[q.kind]) assert.ok(build(q).includes(marks[q.kind]), q.id + " " + q.kind);
});
t("student answer / photo variants", () => {
  const q = bank.questions[0];
  assert.ok(build(q, { answerText: "התשובה שלי כאן" }).includes("התשובה שלי:\nהתשובה שלי כאן"));
  const X = build(q, { answerText: "", photo: true });
  assert.ok(X.includes("מצורפת תמונה של הפתרון שלי בכתב יד") && !X.includes("התשובה שלי:"));
  assert.ok(!build(q, { answerText: "   " }).includes("התשובה שלי:"), "blank text, no photo -> no empty block");
});
t("never throws on odd shapes (no rubric/solution/options, null fields, empty object)", () => {
  for (const q of [{}, { question: "q" }, { question: "q", rubric: null, solution: null, kind: "weird" }, { question: "q", rubric: [{ text: "x" }], steps: [] },
                   { question: "q", kind: "mcq", options: [{ id: "a" }], correctId: "a" }, { question: "q", rubric: [null] }])
    assert.strictEqual(typeof AP.build(q, undefined), "string");
  assert.strictEqual(typeof AP.build(bank.questions[0], { context: { kind: "code", code: "int a<b;" } }), "string");
});
t("TeX kept raw", () => {
  for (const q of bank.questions) if (/\$[^$]+\$/.test(q.question)) assert.ok(build(q).includes(q.question.trim()), q.id);
});

/* ---------- (b) DEMO-A specific checks (only when the demo exam is built) ---------- */
if (!DEMO) console.log("\n(b) demo-specific checks skipped: no DEMO-A exam in this bank");
else {
  const demoQs = bank.questions.filter(q => q.examCode === "DEMO-A");
  const byKind = k => demoQs.find(q => q.kind === k);
  const proof = byKind("proof"), comp = byKind("computation"), code = byKind("code");
  const P = build(proof, { answerText: "הוכחה שלי כאן" });
  t("demo: proof prompt has solution, every rubric line + points; official label", () => {
    assert.ok(P.includes(proof.question) && P.includes(proof.solution));
    for (const r of proof.rubric) { assert.ok(P.includes(r.text), r.text); assert.ok(P.includes(r.points + " נק"), "pts " + r.points); }
    assert.strictEqual(proof.official, true);
    assert.ok(P.includes("הפתרון הרשמי:\n" + proof.solution));
  });
  t("demo: proof / computation / code instructions are kind-specific", () => {
    const C = build(comp);
    assert.ok(P.includes("תקפות לוגית") && !C.includes("תקפות לוגית"));
    assert.ok(C.includes("השורה השגויה הראשונה") && C.includes("הערך הסופי") && !P.includes("הערך הסופי"));
    assert.ok(build(code).includes("מקרי קצה"));
  });
}

(async () => {
  let D = { errors: [] };
  const A = boot(true).w;
  noClipboard(A);
  A.AiPrompt.open("claude", "PROMPT TEXT");
  t("no clipboard -> modal read-only textarea with prompt", () => {
    const ta = A.document.querySelector(".aip-modal textarea");
    assert.ok(ta && ta.value === "PROMPT TEXT" && ta.readOnly);
  });
  t("opens target in new tab", () => { assert.strictEqual(A.opened[0][0], "https://claude.ai/new"); assert.strictEqual(A.opened[0][1], "_blank"); });
  t("modal closes", () => { A.document.querySelector(".aip-modal .aip-close").click(); assert.ok(!A.document.querySelector(".aip-modal")); });
  t("target urls", () => {
    A.AiPrompt.open("chatgpt", "x"); A.AiPrompt.open("gemini", "x");
    assert.strictEqual(A.opened[1][0], "https://chatgpt.com/"); assert.strictEqual(A.opened[2][0], "https://gemini.google.com/app");
  });

  const B = boot(true).w;
  Object.defineProperty(B.navigator, "clipboard", { value: { writeText: () => Promise.reject(new Error("no")) }, configurable: true });
  B.AiPrompt.open("gemini", "REJ"); await sleep(10);
  t("clipboard rejection -> modal", () => { assert.strictEqual(B.document.querySelector(".aip-modal textarea").value, "REJ"); });
  let copied = null;
  const C = boot(true).w;
  Object.defineProperty(C.navigator, "clipboard", { value: { writeText: s => { copied = s; return Promise.resolve(); } }, configurable: true });
  C.AiPrompt.open("chatgpt", "OK"); await sleep(10);
  t("clipboard ok -> copied, no modal", () => { assert.strictEqual(copied, "OK"); assert.ok(!C.document.querySelector(".aip-modal")); });

  const O = boot(true).w, order = [];
  Object.defineProperty(O.navigator, "clipboard", { value: { writeText: () => { order.push("write"); return Promise.resolve(); } }, configurable: true });
  O.open = () => { order.push("open"); return null; };
  O.AiPrompt.open("claude", "X");
  t("writeText is called before window.open", () => { assert.deepStrictEqual(order, ["write", "open"]); });

  if (DEMO) {
  // in-app: slot UI + photo toggle + click builds the prompt from the attempt textarea
    D = boot(true); const d = D.w, doc = d.document;
    noClipboard(d);
    const click = el => el.dispatchEvent(new d.MouseEvent("click", { bubbles: true, cancelable: true }));
    const r = doc.querySelector('input[name=mode][value="exam"]'); r.checked = true; r.dispatchEvent(new d.Event("change", { bubbles: true }));
    doc.querySelector("#examPick").value = "DEMO-A"; doc.querySelector("#examPick").dispatchEvent(new d.Event("change", { bubbles: true }));
    click(doc.querySelector("#startBtn"));
    for (let i = 0; i < 10 && !doc.querySelector(".ai-grade-slot"); i++) click(doc.querySelector("#nextBtn"));
    const slot = doc.querySelector(".ai-grade-slot");
    t("slot UI: photo toggle + 3 buttons", () => {
      assert.ok(slot.querySelector("input[type=checkbox]"));
      assert.strictEqual(slot.querySelectorAll("button[data-target]").length, 3);
    });
    const ta0 = doc.querySelector("#attempt"); ta0.value = "הניסיון שלי 123"; ta0.dispatchEvent(new d.Event("input", { bubbles: true }));
    click(slot.querySelector('button[data-target="gemini"]'));
    t("click -> modal prompt built from the attempt, gemini tab", () => {
      const m = doc.querySelector(".aip-modal textarea");
      assert.ok(m && m.value.includes("הניסיון שלי 123"));
      assert.strictEqual(d.opened.pop()[0], "https://gemini.google.com/app");
    });
    doc.querySelector(".aip-modal .aip-close").click();
    slot.querySelector("input[type=checkbox]").checked = true;
    click(slot.querySelector('button[data-target="chatgpt"]'));
    t("photo toggle -> photo line, attempt omitted", () => {
      const v = doc.querySelector(".aip-modal textarea").value;
      assert.ok(v.includes("מצורפת תמונה של הפתרון שלי בכתב יד") && !v.includes("הניסיון שלי 123"));
    });
}
  else console.log('  skip  in-app slot checks: no DEMO-A exam in this bank');
  t("no page errors", () => { assert.deepStrictEqual(D.errors, []); });
  console.log(fail ? `\n${fail} FAILED` : "\nall ok");
  process.exit(fail ? 1 : 0);
})();
