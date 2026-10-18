"use strict";
/* Guided courses — "צריך עזרה?": level map → lesson → level quiz → summary.
   Generalized from machine-learning-quiz's course-ui.js (same flow, same bidi isolation for lessons).
   Data:  course.config.json "needHelp" → questions.js meta.course.needHelp (the courses to offer; [] hides the feature)
          courses.js  window.COURSES[id].levels (built by tools/build_courses.py from courses/<id>/*.js,
          math already rendered to MathML)
   Hooks: app.js exposes window.CC_APP (screens, bank access, renderers); steps.js provides window.Steps (the
          guided-step widgets). app.js fires "cc:home" whenever the
          start screen is shown again. This file never touches the bank progress (<prefix>_progress_v1);
          each course keeps its own <prefix>_course_<id>_v1 (every storage access is in try/catch, and an
          in-memory copy is the fallback, so a blocked localStorage cannot break the flow).

   level    = {id, order, icon, title, goal, boss?, source, lesson:{html, figs?}, questions:[…]}
   question = {id, questionHtml, options:[{id,type,value,html}], correctId, acceptedIds?, explanationHtml, recapHtml}
            | {id, step:{type, prompt…}, recapHtml?}          ← a guided step (Steps.render), the step IS the question
            | {bankId:"<exam question id>", recapHtml?}       ← a real exam question, rendered from the bank
   Soft unlock: every level is open; a level is passed at PASS % and the first unpassed level is highlighted. */
(function(){
  const PASS = 80;
  const APP = window.CC_APP;
  const META = ((window.OPEN_BANK && window.OPEN_BANK.meta) || {}).course || {};
  const ALL = (window.COURSES && typeof window.COURSES === "object") ? window.COURSES : {};
  const $ = s => document.querySelector(s);
  const entry = $("#helpEntry"), cardsBox = $("#helpCards"), screen = $("#screen-course");
  const has = id => ALL[id] && Array.isArray(ALL[id].levels) && ALL[id].levels.length > 0;
  const COURSES = (Array.isArray(META.needHelp) ? META.needHelp : []).filter(c => c && c.id && has(c.id));
  if(!APP || !window.Steps || !screen || !COURSES.length){
    if(entry) entry.style.display = "none";
    if(cardsBox){ cardsBox.innerHTML = ""; cardsBox.classList.add("hidden"); }
    return;
  }
  const esc = APP.escapeHtml;
  const NOTE = { "ai-verified": "נבנה בעזרת AI ונבדק", "ai-draft": "טיוטת AI — טרם נבדק" };

  /* ---------- state + storage ---------- */
  let C = null;                       // the open course: {id, meta, levels, prog}
  let cur = null;                     // the level being studied / played
  let S = null;                       // the running quiz: {L, items, i, run:{key:ok}}
  const progs = {};
  const storeKey = id => `${APP.prefix}_course_${id}_v1`;
  function loadProg(id){
    try{ const p = JSON.parse(localStorage.getItem(storeKey(id))); if(p && p.levels && typeof p.levels === "object") return p; }catch(e){}
    return { levels: {} };
  }
  function saveProg(){ try{ localStorage.setItem(storeKey(C.id), JSON.stringify(C.prog)); }catch(e){} }
  function course(id){
    progs[id] = progs[id] || loadProg(id);
    return { id, meta: COURSES.find(c => c.id === id), levels: ALL[id].levels, prog: progs[id] };
  }
  const passedIn = (c, L) => ((c.prog.levels[L.id] || {}).best || 0) >= PASS;
  const recommendedIn = c => c.levels.find(L => !passedIn(c, L));
  const levelName = L => `שלב ${L.order} · ${L.title}`;
  /* level title / goal as HTML: the goal's math is pre-rendered by build_courses.py (goalHtml); both get bidi isolates */
  const titleH = L => isolate(esc(L.title || ""));
  const goalH = L => isolate(L.goalHtml || esc(L.goal || ""));
  const levelNameH = L => `שלב ${L.order} · ${titleH(L)}`;

  /* bidi: Latin labels / formulas / runs inside Hebrew are isolated by Bidi (normalize.js, loaded before this file) */
  const isolate = window.Bidi.render;
  function lessonHtml(L){
    const les = L.lesson || {};
    let h = isolate(String(les.html || "").replace(/<table>/g, '<div class="tbl-wrap"><table>').replace(/<\/table>/g, "</table></div>"));
    (les.figs || []).forEach(f => { h += `<figure class="learn-fig"><img class="q-img" src="${esc(f.src)}" alt="${esc(f.alt || "")}" loading="lazy">${f.caption ? `<figcaption>${isolate(esc(f.caption))}</figcaption>` : ""}</figure>`; });
    return h;
  }
  const html = q => isolate(q);

  /* ---------- views ---------- */
  const VIEWS = ["crsMapView", "crsLessonView", "crsQuizView", "crsSumView"];
  function view(id){ if(id !== "crsQuizView") $("#crsQBody").innerHTML = ""; APP.show("screen-course"); VIEWS.forEach(v => $("#" + v).classList.toggle("hidden", v !== id)); }

  /* ---------- map ---------- */
  function renderMap(){
    const LV = C.levels, rec = recommendedIn(C), nPass = LV.filter(L => passedIn(C, L)).length;
    $("#crsTitle").textContent = `${C.meta.icon} ${C.meta.titleHe}`;
    $("#crsIntro").textContent = C.meta.introHe || C.meta.entryLabelHe;
    $("#crsOverall").innerHTML =
      `עברת <b>${nPass}</b> מתוך <b>${LV.length}</b> שלבים` +
      `<div class="progress" style="margin-top:.5rem"><div class="progress-fill" style="width:${nPass / LV.length * 100}%"></div></div>` +
      (nPass === LV.length ? `<p class="crs-done">🏆 סיימת את כל הקורס. הצעד הבא: שאלות אמיתיות מהמבחנים.</p><button type="button" class="btn primary" data-act="real">לשאלות האמיתיות בנושא ⟵</button>` : "");
    $("#crsMap").innerHTML = LV.map(L => {
      const st = C.prog.levels[L.id], ok = passedIn(C, L);
      const cls = ["crs-lvl", ok ? "passed" : "", L === rec ? "next" : "", L.boss ? "boss" : ""].join(" ").replace(/\s+/g, " ").trim();
      const status = !st ? `עוד לא התחלת · ${L.questions.length} שאלות`
        : ok ? `✓ עברת · שיא ${st.best}%` : `ניסיון אחרון ${st.last}% · שיא ${st.best}% (צריך ${PASS}%)`;
      return `<button class="${cls}" data-id="${esc(L.id)}" type="button">
        <span class="num">שלב ${L.order}${L.boss ? " · מבחן גמר" : ""}</span>
        <span class="ttl">${esc(L.icon || "")} ${titleH(L)}</span>
        <span class="gl">${goalH(L)}</span>
        <span class="st">${status}</span></button>`;
    }).join("");
    $("#crsMap").querySelectorAll(".crs-lvl").forEach(b => b.onclick = () => openLesson(LV.find(L => L.id === b.dataset.id)));
    const real = $("#crsOverall [data-act=real]"); if(real) real.onclick = realExam;
  }
  function openMap(id){ if(id) C = course(id); cur = null; S = null; renderMap(); view("crsMapView"); }

  /* ---------- lesson ---------- */
  const nReal = L => L.questions.filter(q => q.bankId).length;
  function openLesson(L){
    cur = L; S = null;
    $("#crsLesson").innerHTML =
      `<div class="q-head"><span class="chip">שלב ${L.order} מתוך ${C.levels.length}</span>` +
      `<span class="chip soft">${L.questions.length} שאלות${nReal(L) ? ` · ${nReal(L)} מהמבחנים` : ""}</span></div>` +
      `<h2 class="learn-h">${esc(L.icon || "")} ${titleH(L)}</h2><p class="sub crs-goal">${goalH(L)}</p>` +
      `<div class="lesson-body">${lessonHtml(L)}</div>` +
      (NOTE[L.source] ? `<div class="crs-note">${NOTE[L.source]}</div>` : "");
    view("crsLessonView");
  }

  /* ---------- level quiz ----------
     An item is one of:  mcq (own MCQ, or a bank mcq) · step (own {step}, rendered by Steps.render) ·
     tf (bank true/false: verdict first) · steps (bank question with guided steps: all steps must be right) ·
     self (bank question without steps: reveal the solution, then mark yourself).  One point each. */
  function itemType(q){
    if(q.kind === "mcq" || (!q.kind && q.options)) return "mcq";
    if(q.kind === "truefalse") return "tf";
    return (Array.isArray(q.steps) && q.steps.length) ? "steps" : "self";
  }
  function items(L){
    return L.questions.map(q => {
      if(q.bankId){ const b = APP.bank(q.bankId); return b ? { key: "bank:" + q.bankId, bank: true, type: itemType(b), q: b, recap: q.recapHtml || "" } : null; }
      if(q.step) return { key: q.id, bank: false, type: "step", q, recap: q.recapHtml || "" };
      return { key: q.id, bank: false, type: "mcq", q, recap: q.recapHtml || "" };
    }).filter(Boolean);
  }
  function startLevel(L){
    cur = L;
    S = { L, items: items(L), i: 0, run: {} };
    if(!S.items.length) return openLesson(L);
    view("crsQuizView");
    renderQuestion();
  }
  const srcNote = q => `<span class="note">מקור: ${esc(APP.examLabelOf(q))}${Number.isInteger(q.num) ? ` · שאלה ${q.num}${q.part ? " " + esc(q.part) : ""}` : ""}</span>`;
  // settle the item once: one verdict per item, then the next button
  function settle(it, ok){
    if(it.answered) return;
    it.answered = true;
    if(!(it.key in S.run)) S.run[it.key] = !!ok;
    const nb = $("#crsNextBtn");
    nb.classList.remove("hidden");
    nb.focus({ preventScroll: true });
  }
  const solutionPanel = (q, open) => (q.solutionHtml || q.solution)
    ? `<details class="panel crs-sol"${open ? " open" : ""}><summary><span class="sum-t">פתרון מלא</span></summary><div class="panel-body"><div class="solution-text">${isolate(q.solutionHtml || esc(q.solution))}</div>${srcNote(q)}</div></details>` : "";

  function renderQuestion(){
    const it = S.items[S.i], q = it.q, n = S.items.length;
    it.answered = false;
    $("#crsQHead").innerHTML = `<span class="chip">${levelNameH(S.L)}</span>` +
      (it.bank ? `<span class="chip soft">${esc(APP.examLabelOf(q))}${Number.isInteger(q.num) ? ` · שאלה ${q.num}${q.part ? " " + esc(q.part) : ""}` : ""}</span><span class="chip official">מבחן אמיתי</span>` : "");
    $("#crsQContext").innerHTML = it.bank && q.contextId ? APP.contextHtml(APP.ctx(q.contextId)) : "";
    const qt = $("#crsQText");
    qt.innerHTML = it.type === "step" ? "" : (it.bank ? APP.questionHtml(q) : html(q.questionHtml || esc(q.question || "")));
    qt.dataset.key = it.key; qt.dataset.type = it.type;
    if(it.bank) qt.dataset.bank = q.id; else delete qt.dataset.bank;
    $("#crsQExtras").innerHTML = it.type === "step" ? "" : APP.extrasHtml(q);
    if(window.Feedback) window.Feedback.slot($("#crsQExtras"), "crs", {
      id: `${C.id}-L${S.L.order}-Q${S.i + 1}`,
      exam: `${C.meta.titleHe} · ${levelName(S.L)}` + (it.bank ? ` · ${APP.examLabelOf(q)} (${q.id})` : ""),
      html: it.type === "step" ? (q.step.promptHtml || esc(q.step.prompt || "")) : (q.questionHtml || esc(q.question || ""))
    });
    $("#crsProgressFill").style.width = (S.i / n * 100) + "%";
    $("#crsQuizMeta").textContent = `שאלה ${S.i + 1} מתוך ${n}`;
    const nb = $("#crsNextBtn");
    nb.classList.add("hidden");
    nb.textContent = S.i >= n - 1 ? "לסיכום ⟵" : "הבאה ⟵";
    const body = $("#crsQBody");
    ({ mcq: mcqBody, step: stepBody, tf: tfBody, steps: stepsBody, self: selfBody })[it.type](it, body);
  }

  function mcqBody(it, body){
    const q = it.q;
    it.order = it.order || (q.lockOrder ? q.options.map(o => o.id) : APP.shuffle(q.options.map(o => o.id)));
    const byId = id => q.options.find(o => o.id === id);
    $("#crsQText").dataset.correct = q.correctId || "";
    body.innerHTML =
      `<div class="options-list">` + it.order.map((oid, d) =>
        `<button class="opt" type="button" data-oid="${esc(oid)}"><span class="key">${APP.HE_KEYS[d] || d + 1}</span><span class="txt">${APP.optionHtml(byId(oid))}</span></button>`).join("") +
      `</div><div class="feedback hidden"></div>`;
    body.querySelectorAll(".opt").forEach(b => b.onclick = () => {
      if(it.answered) return;
      const oid = b.dataset.oid, acc = APP.acceptedIdsOf(q), ok = acc.includes(oid);
      body.querySelectorAll(".opt").forEach(x => {
        x.disabled = true;
        if(acc.includes(x.dataset.oid)) x.classList.add("correct");
        else if(x.dataset.oid === oid) x.classList.add("wrong");
      });
      const expl = html(q.explanationHtml || "");   // bank items too: same bidi isolates as in the bank
      const fb = body.querySelector(".feedback");
      fb.className = "feedback " + (ok ? "good" : "bad");
      fb.innerHTML = `<div class="verdict">${ok ? "✓ נכון" : "✗ לא נכון"}</div>` +
        (expl ? `<div class="expl">${expl}</div>` : `<div class="expl expl-none">אין הסבר במקור.</div>`) +
        (acc.length > 1 ? `<span class="accept-note">בשאלה זו התקבלה יותר מתשובה אחת כנכונה.</span>` : "") +
        (it.bank ? srcNote(q) : "");
      settle(it, ok);
    });
  }

  // an own {step} question: the step widget IS the question (prompt, input, check, explanation)
  function stepBody(it, body){
    body.innerHTML = `<div class="step-card"><div class="step-mount"></div></div>`;
    window.Steps.render(it.q.step, body.querySelector(".step-mount"), r => settle(it, r.ok));
  }

  // bank true/false: the verdict is the point; the proof is read in the solution
  function tfBody(it, body){
    const q = it.q;
    body.innerHTML = `<div class="tf-row"><span class="tf-label">מה דעתכם — הטענה נכונה?</span>` +
      `<button type="button" class="tf-btn" data-v="true">נכונה</button><button type="button" class="tf-btn" data-v="false">לא נכונה</button></div>` +
      `<div class="tf-result hidden"></div><div class="crs-after"></div>`;
    body.querySelectorAll(".tf-btn").forEach(b => b.onclick = () => {
      if(it.answered) return;
      const val = b.dataset.v === "true", ok = val === q.verdict;
      body.querySelectorAll(".tf-btn").forEach(x => { x.disabled = true; x.classList.toggle("correct", x.dataset.v === String(q.verdict)); x.classList.toggle("wrong", x.dataset.v === String(val) && !ok); });
      const res = body.querySelector(".tf-result");
      res.className = "tf-result " + (ok ? "good" : "bad");
      res.textContent = (ok ? "✓ צדקתם: " : "✗ לא בדיוק: ") + "הטענה " + (q.verdict ? "נכונה" : "אינה נכונה") + ".";
      body.querySelector(".crs-after").innerHTML = solutionPanel(q, true);
      settle(it, ok);
    });
  }

  // bank question with guided steps: every step is graded by Steps; the item is right when all of them are
  function stepsBody(it, body){
    const q = it.q, n = q.steps.length, res = [];
    body.innerHTML = q.steps.map((_, i) => `<div class="step-card"><div class="step-n">${i + 1}</div><div class="step-mount" data-i="${i}"></div></div>`).join("") +
      `<div class="crs-after"></div><div class="crs-skip"><button type="button" class="btn ghost" id="crsGiveUp">לא יודע/ת — להראות פתרון</button></div>`;
    const done = () => {
      body.querySelector(".crs-after").innerHTML = solutionPanel(q, false);
      const g = body.querySelector("#crsGiveUp"); if(g) g.remove();
    };
    body.querySelectorAll(".step-mount").forEach(m => {
      const i = +m.dataset.i;
      window.Steps.render(q.steps[i], m, r => {
        if(res[i] === undefined) res[i] = !!r.ok;
        if(res.filter(v => v !== undefined).length === n && !it.answered){ done(); settle(it, res.every(Boolean)); }
      });
    });
    body.querySelector("#crsGiveUp").onclick = () => { if(it.answered) return; body.querySelector(".crs-after").innerHTML = solutionPanel(q, true); const g = body.querySelector("#crsGiveUp"); if(g) g.remove(); settle(it, false); };
  }

  // bank question with nothing to auto-grade: reveal the solution, then mark yourself
  function selfBody(it, body){
    const q = it.q;
    body.innerHTML = `<div class="crs-after"><button type="button" class="btn ghost" id="crsRevealBtn">הצגת פתרון</button></div>`;
    body.querySelector("#crsRevealBtn").onclick = () => {
      body.querySelector(".crs-after").innerHTML = solutionPanel(q, true) +
        `<div class="crs-selfmark"><span>איך הלך לכם?</span><button type="button" class="btn primary" data-self="ok">פתרתי נכון</button><button type="button" class="btn ghost" data-self="no">טעיתי</button></div>`;
      body.querySelectorAll("[data-self]").forEach(b => b.onclick = () => {
        body.querySelectorAll("[data-self]").forEach(x => { x.disabled = true; });
        settle(it, b.dataset.self === "ok");
      });
    };
  }
  function nextQuestion(){
    if(!S || !S.items[S.i].answered) return;
    if(S.i < S.items.length - 1){ S.i++; renderQuestion(); } else finishLevel();
  }

  /* ---------- summary ---------- */
  function finishLevel(){
    const L = S.L, total = S.items.length;
    const correct = S.items.filter(it => S.run[it.key]).length;
    const pct = Math.round(correct / total * 100);
    const prev = C.prog.levels[L.id] || {};
    C.prog.levels[L.id] = { best: Math.max(prev.best || 0, pct), last: pct, at: Date.now() };
    saveProg();
    const ok = pct >= PASS, LV = C.levels, nextL = LV[LV.indexOf(L) + 1];
    const wrong = S.items.filter(it => !S.run[it.key]);
    const hasReal = APP.topicCount(C.meta.topic) > 0;
    $("#crsSum").innerHTML =
      `<div class="q-head" style="justify-content:center"><span class="chip">${levelNameH(L)}</span></div>` +
      `<div class="big">${pct}%</div><div><b><bdi dir="ltr">${correct} / ${total}</bdi></b> תשובות נכונות</div>` +
      `<p class="msg">${ok ? (L.boss ? `🏆 עברת את מבחן הגמר של ${esc(C.meta.titleHe)}` : "✓ עברת את השלב! אפשר להתקדם.") :
        `עוד לא ${PASS}%. כדאי לקרוא שוב את השיעור ולנסות שוב, זה בדיוק השלב שבו זה נבנה.`}</p>` +
      (wrong.length ? `<div class="crs-review"><div class="crs-review-t">כדאי לחזור על:</div>${
        wrong.map(it => `<div>• ${it.recap ? html(it.recap) : it.type === "step" ? html(it.q.step.promptHtml || "") : it.bank ? APP.questionHtml(it.q) : html(it.q.questionHtml)}</div>`).join("")}</div>` : "") +
      `<div class="crs-actions">` +
        (nextL ? `<button class="btn ${ok ? "primary" : "ghost"}" data-act="next">לשלב הבא: ${titleH(nextL)} ⟵</button>` : "") +
        ((L.boss || !nextL) && hasReal ? `<button class="btn primary" data-act="real">לשאלות האמיתיות מהמבחנים ⟵</button>` : "") +
        `<button class="btn ${ok ? "ghost" : "primary"}" data-act="retry">🔁 לנסות שוב</button>` +
        `<button class="btn ghost" data-act="lesson">📘 לשיעור</button>` +
        `<button class="btn ghost" data-act="map">🗺️ למפת השלבים</button>` +
      `</div>`;
    $("#crsSum").querySelectorAll("[data-act]").forEach(b => b.onclick = () => {
      const a = b.dataset.act;
      if(a === "next") openLesson(nextL);
      else if(a === "retry") startLevel(L);
      else if(a === "lesson") openLesson(L);
      else if(a === "real") realExam();
      else openMap();
    });
    view("crsSumView");
  }
  // hand off to free practice on the course's topic (the real exam questions)
  function realExam(){ if(!APP.practiceTopic(C.meta.topic)) openMap(); }

  /* ---------- start-screen cards + header entry ---------- */
  function paintCards(){
    cardsBox.classList.remove("hidden");
    cardsBox.innerHTML = COURSES.map(c =>
      `<div class="card crs-promo" data-course="${esc(c.id)}" role="button" tabindex="0">
        <span class="big-ico">${esc(c.icon)}</span>
        <div><b>${esc(c.titleHe)}</b><span class="crs-promo-sub">${esc(c.entryLabelHe)}</span></div>
        <span class="btn primary go">להתחיל ⟵</span></div>`).join("");
    cardsBox.querySelectorAll(".crs-promo").forEach(el => {
      const id = el.dataset.course, c = course(id), n = c.levels.filter(L => passedIn(c, L)).length, rec = recommendedIn(c);
      if(n) el.querySelector(".crs-promo-sub").textContent = `עברת ${n} מתוך ${c.levels.length} שלבים${rec ? ". הבא בתור: " + rec.title : ". סיימת, כל הכבוד!"}`;
      el.onclick = () => openMap(id);
      el.onkeydown = e => { if(e.key === "Enter" || e.key === " "){ e.preventDefault(); openMap(id); } };
    });
  }

  /* ---------- wiring ---------- */
  $("#crsLessonGo").onclick = () => cur && startLevel(cur);
  $("#crsLessonBack").onclick = () => openMap();
  $("#crsHomeBtn").onclick = () => APP.quit();
  $("#crsQuitBtn").onclick = () => cur ? openLesson(cur) : openMap();
  $("#crsNextBtn").onclick = nextQuestion;
  $("#crsResetBtn").onclick = () => { if(confirm(`לאפס את ההתקדמות בקורס ${C.meta.titleHe}?`)){ C.prog.levels = {}; saveProg(); renderMap(); } };
  entry.style.display = "";
  entry.onclick = () => { APP.quit(); setTimeout(() => { cardsBox.scrollIntoView({ behavior: "smooth", block: "start" }); }, 60); };
  paintCards();
  document.addEventListener("cc:home", () => { $("#crsQBody").innerHTML = ""; paintCards(); });
  document.addEventListener("keydown", e => {
    if(screen.classList.contains("hidden") || $("#crsQuizView").classList.contains("hidden")) return;
    const lb = $("#lightbox"); if(lb && !lb.classList.contains("hidden")) return;
    if(e.target && /^(SELECT|INPUT|TEXTAREA)$/.test(e.target.tagName)) return;
    if(/^[1-8]$/.test(e.key)){ const b = document.querySelector(`#crsQBody .opt:nth-child(${+e.key})`); if(b && !b.disabled) b.click(); }
    else if(e.key === "Enter" && !$("#crsNextBtn").classList.contains("hidden")){ e.preventDefault(); nextQuestion(); }
  });

  window.COURSE_UI = { PASS, openMap, openLesson, startLevel };

  // deep link: ?course=ID (map) · ?course=ID&level=C01 (that lesson) · …&play=1 (its quiz)
  try{
    const p = new URLSearchParams(location.search), id = p.get("course");
    if(id && has(id) && COURSES.some(c => c.id === id)){
      C = course(id);
      const L = C.levels.find(l => l.id === p.get("level"));
      if(!L) openMap(); else if(p.get("play")) startLevel(L); else openLesson(L);
    }
  }catch(e){}
})();
