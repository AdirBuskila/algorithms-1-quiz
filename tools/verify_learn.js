// Learn-mode mobile guard (puppeteer-core + local Chrome):  node tools/verify_learn.js
// Opens index.html over file:// at 390px (mobile, both themes) and 1000px (desktop, dark),
// walks EVERY learn chapter and asserts:
//   - no horizontal page overflow (documentElement.scrollWidth <= clientWidth)
//   - nothing inside the chapter sticks out past the content card, except inside the
//     boxes that are meant to scroll (.math-block, .tbl-wrap, pre)
//   - every .qref resolves (opening one shows the peek with the question text, no overflow)
//   - no page errors / console errors
// Screenshots (first screen of each chapter + one peek) -> tools/raw/shots/learn-*.png
// Env: SHOTS=0 skips screenshots, FULL=1 takes full-page shots.
const puppeteer = require("puppeteer-core");
const path = require("path"), fs = require("fs"), url = require("url");

const CHROME = process.env.CHROME || "C:/Program Files/Google/Chrome/Application/chrome.exe";
const APP = process.env.APP_URL || url.pathToFileURL(path.join(__dirname, "..", "index.html")).href;
const THEME_KEY = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "course.config.json"), "utf8")).storePrefix + "_theme";
const OUT = path.join(__dirname, "raw", "shots");
const SHOTS = process.env.SHOTS !== "0", FULL = process.env.FULL === "1";
if (SHOTS) fs.mkdirSync(OUT, { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));

const RUNS = [
  ["m390", "dark", { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true }],
  ["m390", "light", { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true }],
  ["d1000", "dark", { width: 1000, height: 900, deviceScaleFactor: 1 }],
];

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: "new",
    args: ["--no-sandbox", "--force-color-profile=srgb", "--hide-scrollbars", "--allow-file-access-from-files"] });
  const problems = [];
  let checked = 0;
  for (const [vpName, theme, vp] of RUNS) {
    const tag = `${vpName}/${theme}`;
    const page = await browser.newPage();
    page.on("pageerror", e => problems.push(`${tag} PAGEERROR: ${e.message}`));
    page.on("console", m => { if (m.type() === "error" && !/goatcounter|gc\.zgo\.at|ERR_/.test(m.text())) problems.push(`${tag} CONSOLE: ${m.text()}`); });
    page.on("dialog", d => d.accept());
    await page.setViewport(vp);
    await page.evaluateOnNewDocument((t, KEY) => { try { localStorage.setItem(KEY, t); } catch (e) {} }, theme, THEME_KEY);
    await page.goto(APP, { waitUntil: "load" });

    const n = await page.evaluate(() => {
      const L = window.LEARN; return (Array.isArray(L) ? L : (L && L.chapters) || []).length; });
    if (!n) { console.log(`${tag}: learn: none built yet (skipped)`); await page.close(); continue; }
    await page.click("#learnEntry");
    await sleep(150);

    for (let i = 0; i < n; i++) {
      await page.evaluate(i => { const b = document.querySelectorAll("#learnToc button")[i]; b.click(); }, i);
      await sleep(120);
      const r = await page.evaluate(() => {
        const de = document.documentElement, content = document.getElementById("learnContent");
        const cr = content.getBoundingClientRect();
        const bad = [];
        for (const el of content.querySelectorAll("*")) {
          if (el.closest(".math-block,.tbl-wrap,pre")) continue;         // meant to scroll
          if (el.closest(".math-inline") && el.tagName.toLowerCase() !== "span") continue;  // box itself is checked
          const b = el.getBoundingClientRect();
          if (!b.width) continue;
          if (b.right > cr.right + 1 || b.left < cr.left - 1)
            bad.push(`${el.tagName.toLowerCase()}.${el.className && el.className.baseVal === undefined ? el.className : ""} "${(el.textContent || "").trim().slice(0, 40)}" [${Math.round(b.left)},${Math.round(b.right)}] card [${Math.round(cr.left)},${Math.round(cr.right)}]`);
        }
        const refs = [...content.querySelectorAll(".qref")].map(b => b.dataset.q);
        const ids = new Set((window.OPEN_BANK.questions || []).map(q => q.id));
        return { id: content.dataset.chapter, overflow: de.scrollWidth - de.clientWidth, bad: bad.slice(0, 5), nBad: bad.length,
                 dangling: refs.filter(q => !ids.has(q)), nRefs: refs.length };
      });
      checked++;
      if (r.overflow > 1) problems.push(`${tag} ${r.id}: page overflows horizontally by ${r.overflow}px`);
      if (r.nBad) problems.push(`${tag} ${r.id}: ${r.nBad} element(s) stick out of the card: ${r.bad.join(" | ")}`);
      if (r.dangling.length) problems.push(`${tag} ${r.id}: dangling qrefs ${r.dangling.join(", ")}`);
      console.log(`${tag} ${String(i + 1).padStart(2)} ${r.id.padEnd(20)} refs=${r.nRefs} overflow=${r.overflow} stickOut=${r.nBad}`);
      if (SHOTS && vpName === "m390") {
        await page.evaluate(() => window.scrollTo(0, 0));
        await sleep(350);
        await page.screenshot({ path: path.join(OUT, `learn-${vpName}-${theme}-${String(i + 1).padStart(2, "0")}-${r.id}.png`), fullPage: FULL });
      }
    }

    // peek: open the first question ref of the first chapter that has one
    const peek = await page.evaluate(() => {
      const btns = document.querySelectorAll("#learnToc button");
      for (let i = 0; i < btns.length; i++) {
        btns[i].click();
        const ref = document.querySelector("#learnContent .qref");
        if (ref) { ref.click(); return ref.dataset.q; }
      }
      return null;
    });
    if (peek) {
      await sleep(300);
      const pr = await page.evaluate(() => {
        const p = document.getElementById("qpeek"), de = document.documentElement;
        const panel = p.querySelector(".qpeek-panel").getBoundingClientRect();
        return { open: !p.classList.contains("hidden"), right: (document.querySelector("#qpeekBody .qpeek-q") || { textContent: "" }).textContent.trim().length,
                 overflow: de.scrollWidth - de.clientWidth, fits: panel.left >= -1 && panel.right <= window.innerWidth + 1 };
      });
      if (!pr.open || !pr.right) problems.push(`${tag}: peek ${peek} did not open with the question text`);
      if (pr.overflow > 1 || !pr.fits) problems.push(`${tag}: peek ${peek} overflows the viewport`);
      if (SHOTS && vpName === "m390") await page.screenshot({ path: path.join(OUT, `learn-${vpName}-${theme}-peek-${peek}.png`) });
      await page.keyboard.press("Escape");
    }
    // mobile TOC drawer opens in-flow without overflow
    if (vpName === "m390") {
      await page.click("#learnTocToggle");
      await sleep(150);
      const ov = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      if (ov > 1) problems.push(`${tag}: TOC open overflows by ${ov}px`);
      if (SHOTS) await page.screenshot({ path: path.join(OUT, `learn-${vpName}-${theme}-toc.png`) });
    }
    await page.close();
  }
  // deep link: index.html?learn=<chapterId> opens that chapter
  {
    const page = await browser.newPage();
    page.on("pageerror", e => problems.push(`deeplink PAGEERROR: ${e.message}`));
    await page.setViewport(RUNS[0][2]);
    const last = await (async () => { await page.goto(APP, { waitUntil: "load" });
      return page.evaluate(() => { const L = window.LEARN; const c = (Array.isArray(L) ? L : (L && L.chapters) || []); return c.length ? c[c.length - 1].id : null; }); })();
    if (last) {
      await page.goto(APP + "?learn=" + encodeURIComponent(last), { waitUntil: "load" });
      await sleep(200);
      const got = await page.evaluate(() => !document.getElementById("screen-learn").classList.contains("hidden") && document.getElementById("learnContent").dataset.chapter);
      if (got !== last) problems.push(`deeplink ?learn=${last} opened ${got}`);
      else console.log(`deeplink ?learn=${last} ok`);
    }
    await page.close();
  }
  await browser.close();
  console.log(`\nchapter views checked: ${checked}`);
  console.log(problems.length ? "PROBLEMS:\n  " + problems.join("\n  ") : "LEARN VERIFY PASSED");
  process.exit(problems.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
