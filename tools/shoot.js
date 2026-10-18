// Screenshot driver (puppeteer-core + local Chrome):  node tools/shoot.js
// Opens index.html over file:// at 390px (mobile) and 1000px (desktop) in both themes. Nothing is hardcoded to a
// course: the screens are picked from the built bank (questions.json) and course.config.json:
//   start screen; the guided "need help?" course (when needHelp is non-empty: map, lesson, question, feedback,
//   summary, boss); the first question of every kind present; a steps view (first question with steps: step 1
//   solved, step 2 answered wrong, one more half done); a solution + rubric view; "just show me"; the simulation
//   self-grade results.
// Also fails if any screen overflows horizontally (the mobile guard) or if display math is clipped by a parent
// (a math block must stay inside the viewport and scroll by itself).
// Env: CHROME=<path to chrome.exe>, APP_URL=<url>, APP_ROOT=<app folder>. Output: tools/raw/shots/<viewport>-<theme>-NN-<name>.png
// NOTE: --headless=new clamps the window to 512px wide, so the viewport is set with page.setViewport (works).
const puppeteer = require("puppeteer-core");
const path = require("path"), fs = require("fs"), url = require("url");

const ROOT = process.env.APP_ROOT || path.join(__dirname, "..");
const CHROME = process.env.CHROME || "C:/Program Files/Google/Chrome/Application/chrome.exe";
const APP = process.env.APP_URL || url.pathToFileURL(path.join(ROOT, "index.html")).href;
const CFG = JSON.parse(fs.readFileSync(path.join(ROOT, "course.config.json"), "utf8"));
const PREFIX = CFG.storePrefix;
const BANK = JSON.parse(fs.readFileSync(path.join(ROOT, "questions.json"), "utf8"));
const QS = BANK.questions;
const OUT = path.join(ROOT, "tools", "raw", "shots");
fs.mkdirSync(OUT, { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));

const hasSteps = q => Array.isArray(q.steps) && q.steps.length > 0;
const isOpen = q => q.kind !== "mcq" && q.kind !== "truefalse";
const KINDS = [...new Set(QS.map(q => q.kind))];
const FIRST = Object.fromEntries(KINDS.map(k => { const of = QS.filter(q => q.kind === k); return [k, of.find(hasSteps) || of[0]]; }));
const STEPS_Q = QS.find(q => hasSteps(q) && q.steps.length >= 2) || QS.find(hasSteps);
const SOL_Q = QS.find(q => isOpen(q) && q.solutionHtml && q.rubric) || QS.find(q => isOpen(q) && q.solutionHtml);

const VIEWPORTS = [
  ["m390", { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true }],
  ["d1000", { width: 1000, height: 900, deviceScaleFactor: 1 }],
];
const THEMES = ["dark", "light"];

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: "new",
    args: ["--no-sandbox", "--force-color-profile=srgb", "--hide-scrollbars", "--allow-file-access-from-files"] });
  const errors = [], overflow = [], clipped = [];
  for (const [vpName, vp] of VIEWPORTS) for (const theme of THEMES) {
    const page = await browser.newPage();
    page.on("pageerror", e => errors.push(`${vpName}/${theme} PAGEERROR: ${e.message}`));
    page.on("console", m => { if (m.type() === "error" && !/goatcounter|gc\.zgo\.at|ERR_/.test(m.text())) errors.push(`${vpName}/${theme} CONSOLE: ${m.text()}`); });
    page.on("dialog", d => d.accept());
    await page.setViewport(vp);
    await page.evaluateOnNewDocument((t, KEY) => { try { localStorage.setItem(KEY, t); } catch (e) {} }, theme, PREFIX + "_theme");
    await page.goto(APP, { waitUntil: "load" });
    let n = 0;
    const shot = async name => {
      await sleep(250);
      const ov = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      if (ov > 1) overflow.push(`${vpName}/${theme}/${name}: +${ov}px`);
      // display math must stay inside the viewport (not clipped by a parent) and scroll by itself when wide
      const bad = await page.evaluate(() => [...document.querySelectorAll(".math-block")].filter(m => m.offsetParent).flatMap(m => {
        const r = m.getBoundingClientRect(), out = [];
        if (r.right > window.innerWidth + 1 || r.left < -1) out.push(`block spans ${Math.round(r.left)}..${Math.round(r.right)} of ${window.innerWidth}px`);
        const host = m.closest(".panel,.card,.crs-lesson");
        if (host) { const h = host.getBoundingClientRect(); if (r.right > h.right + 1 || r.left < h.left - 1) out.push("block wider than its container"); }
        const ox = getComputedStyle(m).overflowX;
        if (m.scrollWidth > m.clientWidth + 1 && !(ox === "auto" || ox === "scroll")) out.push("wide math without its own horizontal scroll");
        return out;
      }));
      const badCode = await page.evaluate(() => [...document.querySelectorAll(".code-block")].filter(c => c.offsetParent).flatMap(c => {
        const r = c.getBoundingClientRect(), cs = getComputedStyle(c), out = [];
        if (c.getAttribute("dir") !== "ltr" || cs.direction !== "ltr") out.push("code block not LTR");
        if (cs.textAlign !== "left" && cs.textAlign !== "start") out.push("code block not left-aligned");
        if (r.right > window.innerWidth + 1 || r.left < -1) out.push(`code block spans ${Math.round(r.left)}..${Math.round(r.right)} of ${window.innerWidth}px`);
        if (c.scrollWidth > c.clientWidth + 1 && !(cs.overflowX === "auto" || cs.overflowX === "scroll")) out.push("wide code block without its own horizontal scroll");
        return out;
      }));
      if (badCode.length) clipped.push(`${vpName}/${theme}/${name}: ${badCode.join("; ")}`);
      if (bad.length) clipped.push(`${vpName}/${theme}/${name}: ${bad.join("; ")}`);
      const f = `${vpName}-${theme}-${String(++n).padStart(2, "0")}-${name}.png`;
      await page.screenshot({ path: path.join(OUT, f), fullPage: true });
      console.log("shot:", f);
    };
    const click = sel => page.evaluate(s => document.querySelector(s).click(), sel);
    const exists = sel => page.evaluate(s => !!document.querySelector(s), sel);
    const qidNow = () => page.evaluate(() => (document.querySelector("#questionText") || { dataset: {} }).dataset.qid);
    // open a bank question in the real app: its exam in exam mode, Next until it shows
    const openQ = async q => {
      if (await page.evaluate(() => { const s = document.querySelector("#screen-question"); return !!s && !s.classList.contains("hidden"); })) await click("#quitBtn");
      await page.evaluate(code => {
        const r = document.querySelector("input[name=mode][value=exam]"); r.checked = true; r.dispatchEvent(new Event("change", { bubbles: true }));
        const s = document.querySelector("#examPick"); s.value = code; s.dispatchEvent(new Event("change", { bubbles: true }));
        document.querySelector("#startBtn").click();
      }, q.examCode);
      for (let i = 0; i < 1000 && (await qidNow()) !== q.id; i++) await click("#nextBtn");
      if ((await qidNow()) !== q.id) throw new Error("could not reach " + q.id);
    };
    // act on step i of the open question from its data (right or wrong), inside the page
    const stepAct = (i, st, right) => page.evaluate((i, st, right) => {
      const m = document.querySelector(`.step-mount[data-i='${i}']`);
      const type = (el, v) => { el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); };
      if (st.type === "choice" || st.type === "fillblank") {
        const id = right ? st.correctId : st.options.find(o => o.id !== st.correctId).id;
        m.querySelector(`.s-opt[data-id="${id}"]`).click();
      } else if (st.type === "numeric") { type(m.querySelector("input.s-input"), right ? String(st.answer) : String(st.answer + 1000)); m.querySelector(".s-check").click(); }
      else if (st.type === "text") { type(m.querySelector("input.s-input"), right ? st.accept[0] : "zzz"); m.querySelector(".s-check").click(); }
      else if (st.type === "findbug") m.querySelector(`.s-line[data-i="${right ? st.bugIndex : st.lines.findIndex((_, j) => j !== st.bugIndex)}"]`).click();
      else if (st.type === "order") {
        const seq = [...Array(st.lines.length).keys()]; if (!right) seq.reverse();
        for (const k of seq) m.querySelector(`.s-pool .s-line[data-i="${k}"]`).click();
        m.querySelector(".s-check").click();
      }
    }, i, st, right);

    await shot("start");

    // guided "need help?" course: card -> map -> lesson -> quiz (bot answers) -> summary -> the boss's real question
    if (await exists("#helpCards .crs-promo")) {
      const quizOpen = () => page.evaluate(() => !document.querySelector("#crsQuizView").classList.contains("hidden"));
      const bot = () => page.evaluate(() => {          // answers whatever is on screen: option / verdict / step widgets / self-mark
        const q = s => document.querySelector(s), all = s => [...document.querySelectorAll(s)];
        const opt = q("#crsQBody .opt"); if (opt) { opt.click(); return; }
        const tf = q("#crsQBody .tf-btn"); if (tf) { tf.click(); return; }
        const rv = q("#crsRevealBtn"); if (rv) { rv.click(); q("#crsQBody [data-self=ok]").click(); return; }
        all("#crsQBody .step-mount").forEach(m => {
          const o = m.querySelector(".s-opt"); if (o) { o.click(); return; }
          const inp = m.querySelector("input.s-input"); if (inp) { inp.value = "0"; m.querySelector(".s-check").click(); return; }
          const ln = m.querySelector(".s-lines .s-line"); if (ln) { ln.click(); return; }
          let p; while ((p = m.querySelector(".s-pool .s-line"))) p.click();
          const c = m.querySelector(".s-check"); if (c) c.click();
        });
      });
      const playOut = async (shotAt, name) => {
        for (let i = 0; i < 12 && await quizOpen(); i++) {
          await bot();
          if (i === shotAt) await shot(name);
          if (!(await page.evaluate(() => document.querySelector("#crsNextBtn").classList.contains("hidden")))) await click("#crsNextBtn");
        }
      };
      await click("#helpCards .crs-promo");
      await shot("course-map");
      await click("#crsMap .crs-lvl");
      await shot("course-lesson");
      await click("#crsLessonGo");
      await shot("course-question");
      await playOut(0, "course-feedback");
      await shot("course-summary");
      await click('#crsSum [data-act="map"]');
      if (await exists("#crsMap .crs-lvl.boss")) {
        await click("#crsMap .crs-lvl.boss");
        await click("#crsLessonGo");
        await bot(); await click("#crsNextBtn");
        await shot("course-boss-bank-question");
        await playOut(99, "");
        await shot("course-boss-summary");
      }
      await click("#crsHomeBtn");
    }

    // the first question of every kind present
    for (const k of KINDS) {
      const q = FIRST[k];
      await openQ(q);
      if (q.kind === "mcq") { await click("#mcqOptions .opt"); }
      else if (q.kind === "truefalse") { await click(".tf-btn[data-v='true']"); }
      else if (await exists("#attempt")) await page.type("#attempt", "פתרון ניסיון");
      await shot("q-" + k);
    }
    // a steps view: step 1 right, step 2 wrong, the next one half done
    if (STEPS_Q) {
      await openQ(STEPS_Q);
      // the guided-steps panel is a collapsed <details>: expand it so the answered steps are on screen (else this shot equals the solution shot)
      await page.evaluate(() => { const d = document.querySelector(".steps-panel"); if (d) { d.open = true; d.scrollIntoView(); } });
      if (!(await exists(".steps-panel[open] .step-mount"))) throw new Error("steps panel did not open for " + STEPS_Q.id);
      await stepAct(0, STEPS_Q.steps[0], true);
      if (STEPS_Q.steps[1]) await stepAct(1, STEPS_Q.steps[1], false);
      if (STEPS_Q.steps[2] && STEPS_Q.steps[2].type === "order") await page.evaluate(() => { const l = document.querySelector(".step-mount[data-i='2'] .s-pool .s-line"); if (l) l.click(); });
      await shot("steps-" + STEPS_Q.kind);
    }
    // the solution + rubric view
    if (SOL_Q) {
      await openQ(SOL_Q);
      if (await exists("#jumpSol")) await click("#jumpSol");
      await shot("solution-rubric");
    }
    await click("#quitBtn");
    // "just show me"
    await click("#justShow");
    await click("#startBtn");
    await shot("just-show-me");
    await click("#quitBtn");
    // exam simulation -> self-grade
    await click("input[name=mode][value=sim]");
    await shot("start-sim");
    await click("#startBtn");
    if (await exists("#attempt")) await page.type("#attempt", "פתרון שלי");
    await shot("sim-question");
    while (await page.evaluate(() => document.querySelector("#submitExamBtn").classList.contains("hidden"))) await click("#nextBtn");
    await click("#submitExamBtn");
    await page.evaluate(() => document.querySelectorAll("#screen-results .rev:first-child .rubric input").forEach(c => c.click()));
    await shot("sim-results");
    await page.close();
  }
  await browser.close();
  console.log("\noverflow:", overflow.length ? overflow : "none");
  console.log("clipped math:", clipped.length ? clipped : "none");
  console.log("errors:", errors.length ? errors : "none");
  process.exit(errors.length || overflow.length || clipped.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
