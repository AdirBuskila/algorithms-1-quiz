"use strict";
/* Guided-step widgets (window.Steps). Self-contained: no dependence on app.js state, only on window.Normalize.
     Steps.render(step, mountEl, onResult)   onResult({ok:boolean}) fires once, on the first answer.
   Types (see tools/RAW_SCHEMA.md): choice | numeric | text | order | findbug | fillblank.
   Markup contract (styled in styles.css, queried by tools/verify_dom.js):
     .s-prompt  .s-opt[data-id]  input.s-input  .s-check  .s-line[data-i] (inside .s-pool / .s-placed / .codeblock)
     .s-result.good|bad  .s-reveal (the correct answer after a miss)  .s-explain
   All *Html fields are trusted build output. Literal code is HTML-escaped by the build and shown in
   <code dir="ltr">; math arrives as MathML that already carries dir="ltr". */
(function (root) {
  const N = () => root.Normalize;
  const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[m]));
  const hasHebrew = s => /[֐-׿]/.test(String(s));

  function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

  /* option body: image / Hebrew-free text isolated LTR / plain html; code steps get a <code dir=ltr> */
  function optionHtml(o, isCode) {
    if (!o) return "";
    if ((o.type || "text") === "image") return `<img class="opt-img" src="${esc(o.value)}" alt="" loading="lazy">`;
    const body = o.html != null ? o.html : esc(o.value);
    if (isCode) return `<code dir="ltr">${body}</code>`;
    if ((o.type || "text") === "math") return body;
    if (!hasHebrew(o.value)) return `<span class="opt-ltr" dir="ltr">${body}</span>`;
    return body;
  }
  /* a step line: literal code -> <code dir=ltr>; rich text -> the build's Html twin */
  function lineHtml(step, j) {
    const raw = step.lines[j];
    const body = (step.linesHtml && step.linesHtml[j] != null) ? step.linesHtml[j] : esc(raw);
    return step.code ? `<code dir="ltr">${body}</code>` : bidi(body);
  }
  const bidi = h => (typeof window !== "undefined" && window.Bidi) ? window.Bidi.render(h) : h;   // normalize.js
  const promptHtml = step => bidi(step.promptHtml != null ? step.promptHtml : esc(step.prompt || ""));
  /* canonical index: lines with identical text are interchangeable */
  const canonOf = lines => lines.map(l => lines.indexOf(l));

  function render(step, mountEl, onResult) {
    const doc = mountEl.ownerDocument;
    let done = false;
    mountEl.innerHTML = "";
    mountEl.removeAttribute("data-ok");
    mountEl.classList.add("step-widget");
    mountEl.dataset.type = step.type;

    const body = doc.createElement("div"); body.className = "s-body";
    const prompt = doc.createElement("div"); prompt.className = "s-prompt"; prompt.innerHTML = promptHtml(step);
    const work = doc.createElement("div"); work.className = "s-work";
    const fb = doc.createElement("div"); fb.className = "s-feedback"; fb.setAttribute("aria-live", "polite");
    body.append(prompt, work, fb);
    mountEl.appendChild(body);

    /* settle the step: verdict, optional reveal of the right answer, explanation, one callback */
    function finish(ok, revealHtml) {
      if (done) return; done = true;
      mountEl.dataset.ok = ok ? "1" : "0";
      mountEl.classList.add("step-done");
      let h = `<div class="s-result ${ok ? "good" : "bad"}">${ok ? "✓ נכון" : "✗ לא נכון"}</div>`;
      if (!ok && revealHtml) h += `<div class="s-reveal">${bidi(revealHtml)}</div>`;
      if (step.explainHtml || step.explain) h += `<div class="s-explain">${bidi(step.explainHtml != null ? step.explainHtml : esc(step.explain))}</div>`;
      fb.innerHTML = h;
      fb.className = "s-feedback " + (ok ? "good" : "bad");
      if (typeof onResult === "function") onResult({ ok });
    }
    const msg = t => { fb.className = "s-feedback"; fb.innerHTML = `<div class="s-hint">${esc(t)}</div>`; };

    const builders = {
      choice() { choiceLike(false); },
      fillblank() { choiceLike(true); },
      numeric() {
        work.innerHTML = `<div class="s-row"><input class="s-input" type="text" inputmode="decimal" dir="ltr" autocomplete="off" aria-label="תשובה מספרית">` +
          `<button type="button" class="btn primary s-check">בדיקה</button></div>`;
        const inp = work.querySelector(".s-input");
        const check = () => {
          if (done) return;
          const v = N().number(inp.value);
          if (!isFinite(v)) { msg("הזינו מספר (אפשר גם עם פסיק עשרוני)"); return; }
          const tol = Number(step.tol) || 0;
          const ok = Math.abs(v - step.answer) <= tol + 1e-9;
          lock(); finish(ok, `התשובה: <bdi dir="ltr">${esc(String(step.answer))}</bdi>` + (tol ? ` <span class="s-tol">(± <bdi dir="ltr">${esc(String(tol))}</bdi>)</span>` : ""));
        };
        wireRow(inp, check);
      },
      text() {
        work.innerHTML = `<div class="s-row"><input class="s-input" type="text" dir="auto" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="תשובה">` +
          `<button type="button" class="btn primary s-check">בדיקה</button></div>`;
        const inp = work.querySelector(".s-input");
        const fn = step.normalize === "complexity" ? N().complexity : N().text;   // none/lower -> the lenient default
        const check = () => {
          if (done) return;
          if (!inp.value.trim()) { msg("כתבו תשובה ואז לחצו על בדיקה"); return; }
          const got = fn(inp.value);
          const ok = (step.accept || []).some(a => fn(a) === got);
          lock(); finish(ok, `תשובה מקובלת: <bdi dir="ltr">${esc((step.accept || [])[0] || "")}</bdi>`);
        };
        wireRow(inp, check);
      },
      order() {
        const lines = step.lines, n = lines.length, canon = canonOf(lines), want = canon.slice();
        let order = shuffle([...Array(n).keys()]);
        for (let t = 0; t < 12 && order.every((v, i) => canon[v] === want[i]) && new Set(canon).size > 1; t++) order = shuffle(order);
        const placed = [];
        work.innerHTML = `<div class="s-hintline">הקישו על שורות לפי הסדר הנכון. הקשה על שורה שהונחה מחזירה אותה.</div>` +
          `<ol class="s-placed${step.code ? " codeblock" : ""}" ${step.code ? 'dir="ltr"' : ""} aria-label="הסדר שבחרתם"></ol>` +
          `<div class="s-pool${step.code ? " codeblock" : ""}" ${step.code ? 'dir="ltr"' : ""} aria-label="שורות לסידור"></div>` +
          `<div class="s-row"><button type="button" class="btn primary s-check" disabled>בדיקה</button></div>`;
        const poolEl = work.querySelector(".s-pool"), placedEl = work.querySelector(".s-placed"), checkBtn = work.querySelector(".s-check");
        const paint = () => {
          poolEl.innerHTML = order.filter(i => !placed.includes(i)).map(i => `<button type="button" class="s-line" data-i="${i}">${lineHtml(step, i)}</button>`).join("");
          placedEl.innerHTML = placed.map((i, pos) => `<li><button type="button" class="s-line" data-i="${i}" data-pos="${pos}">${lineHtml(step, i)}</button></li>`).join("");
          checkBtn.disabled = placed.length !== n;
          placedEl.classList.toggle("empty", !placed.length);
          if (!done) {
            poolEl.querySelectorAll(".s-line").forEach(b => b.onclick = () => { placed.push(+b.dataset.i); paint(); });
            placedEl.querySelectorAll(".s-line").forEach(b => b.onclick = () => { placed.splice(+b.dataset.pos, 1); paint(); });
          }
        };
        checkBtn.onclick = () => {
          if (done || placed.length !== n) return;
          const ok = placed.every((i, pos) => canon[i] === want[pos]);
          placedEl.querySelectorAll(".s-line").forEach((b, pos) => { b.disabled = true; b.classList.add(canon[placed[pos]] === want[pos] ? "right" : "misplaced"); });
          checkBtn.disabled = true;
          finish(ok, `הסדר הנכון:<ol class="s-answer${step.code ? " codeblock" : ""}" ${step.code ? 'dir="ltr"' : ""}>` + lines.map((_, j) => `<li>${lineHtml(step, j)}</li>`).join("") + `</ol>`);
        };
        paint();
      },
      findbug() {
        work.innerHTML = `<div class="s-hintline">הקישו על השורה השגויה.</div>` +
          `<div class="s-lines${step.code ? " codeblock" : ""}" ${step.code ? 'dir="ltr"' : ""}>` +
          step.lines.map((_, j) => `<button type="button" class="s-line" data-i="${j}">${lineHtml(step, j)}</button>`).join("") + `</div>`;
        work.querySelectorAll(".s-line").forEach(b => b.onclick = () => {
          if (done) return;
          const i = +b.dataset.i, ok = i === step.bugIndex;
          work.querySelectorAll(".s-line").forEach(x => { x.disabled = true; });
          work.querySelector(`.s-line[data-i="${step.bugIndex}"]`).classList.add("bug");
          if (!ok) b.classList.add("wrong");
          finish(ok, "השורה השגויה מסומנת למעלה.");
        });
      },
    };

    function lock() { work.querySelectorAll("input,button").forEach(x => { x.disabled = true; }); }
    function wireRow(inp, check) {
      work.querySelector(".s-check").onclick = check;
      inp.addEventListener("keydown", e => { if (e.key === "Enter") { e.preventDefault(); check(); } });
    }

    /* choice: option buttons. fillblank: the same options sit inside the code block, at the blank. */
    function choiceLike(inCode) {
      const opts = step.options || [];
      const optBtn = o => `<button type="button" class="s-opt" data-id="${esc(o.id)}"><span class="txt">${optionHtml(o, inCode && step.code)}</span></button>`;
      if (!inCode) {
        work.innerHTML = `<div class="s-opts">${opts.map(optBtn).join("")}</div>`;
      } else {
        const rows = step.lines.map((l, j) => {
          if (j !== step.blankIndex) return `<div class="s-codeline">${lineHtml(step, j)}</div>`;
          const raw = String(l), at = raw.indexOf("___");
          const before = esc(at >= 0 ? raw.slice(0, at) : ""), after = esc(at >= 0 ? raw.slice(at + 3) : "");
          return `<div class="s-codeline s-blank"><code dir="ltr">${before}<span class="s-slot">___</span>${after}</code></div>` +
                 `<div class="s-opts s-inline-opts">${opts.map(optBtn).join("")}</div>`;
        });
        work.innerHTML = `<div class="s-codewrap codeblock" dir="ltr">${rows.join("")}</div>`;
      }
      work.querySelectorAll(".s-opt").forEach(b => b.onclick = () => {
        if (done) return;
        const id = b.dataset.id, ok = id === step.correctId;
        work.querySelectorAll(".s-opt").forEach(x => {
          x.disabled = true;
          if (x.dataset.id === step.correctId) x.classList.add("correct");
          else if (x === b) x.classList.add("wrong");
        });
        if (inCode) {
          const slot = work.querySelector(".s-slot"), pick = opts.find(o => o.id === id);
          if (slot && pick) { slot.textContent = String(pick.value); slot.classList.add("filled", ok ? "right" : "wrong"); }
        }
        finish(ok, null);
      });
    }

    if (!builders[step.type]) { work.innerHTML = `<div class="s-hint">סוג צעד לא מוכר: ${esc(step.type)}</div>`; return; }
    builders[step.type]();
  }

  root.Steps = { render };
  if (typeof module !== "undefined" && module.exports) module.exports = root.Steps;
})(typeof window !== "undefined" ? window : globalThis);
