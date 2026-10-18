# Raw exam JSON (open engine) — `tools/raw/<CODE>.json` (THE source of truth)

Written by `tools/gen/gen_<CODE>.py`, linted by `tools/validate.py`, merged by
`tools/build_questions.py` into `questions.json` / `questions.js` (`window.OPEN_BANK`).
Every validator/build message starts with the **question id**. Unknown keys (at exam, context, question,
step, rubric-item and option level) are errors, so a misspelt key such as `stepSource` cannot slip through.

```jsonc
{
  "examCode": "24B-A",                 // YY[A|B|S]-[A|B|C], SAMP-N or DEMO-X; must equal the file name
  "examLabel": "…", "year": 2024, "examDate": "…", "sourceFile": "…", "solutionFile": "…",
  "contexts": {                        // optional shared blocks; ids local, build namespaces <CODE>-<id>
    "c1": { "kind": "image", "title": "…", "image": "images/exams/24B-A-c1.png", "caption": "…" },
    "c2": { "kind": "text",  "title": "…", "text": "rich text" },
    "c3": { "kind": "code",  "title": "…", "code": "literal code, escaped not parsed" }
  },
  "questions": [{
    "num": 3, "part": "ב",            // part optional; sub-parts are separate items grouped by num
    "kind": "proof",                  // computation|proof|algorithm|code|mcq|truefalse
    "topic": "induction",             // key from course.config.json "topics" (closed list)
    "points": 15,                     // optional; warns if it differs from the rubric sum
    "question": "rich text",
    "contextId": "c1", "image": "images/exams/24B-A-Q3b.png",   // optional
    "solution": "rich text -- the model answer",
    "solutionSource": "official-pdf",  // official-pdf | lecturer-solution | student-solution | solved
    "official": true, "confidence": "high",   // high | med | low
    "hold": "reason (optional)",       // held questions are listed in the report, NOT in the bank
    "rubric": [ { "text": "rich text", "points": 3 } ],
    "rubricSource": "official",        // official | ai-draft | ai-verified (required with rubric)
    "pitfalls": [ "rich text" ],
    "steps": [ /* step objects, below */ ],
    "stepsSource": "ai-verified",      // official | ai-draft | ai-verified (required with steps)
    // kind "mcq" only:   options, correctId, acceptedIds, lockOrder, explanation  (as the mcq engine)
    // kind "truefalse":  verdict: true|false
  }]
}
```

## Held questions (`hold`)
A question you cannot transcribe or solve honestly gets `"hold": "<reason>"` instead of an invented answer, plus an
entry in `docs/ASK_ADIR.md`. A held question needs only `num` and `kind`; `topic`, `question`, `official`,
`confidence`, `solution`/`solutionSource`, an mcq's `correctId` and a truefalse's `verdict` may be missing (whatever
text exists is still checked for structure, math and `redact.txt`). `build_questions.py` leaves held questions out of
the bank and lists them (id + reason) in `build_report.md`.

## Question id (`<CODE>-Q<num><part>`)
`id = examCode + "-Q" + num + partKey`. `partKey` is the ASCII suffix of `part`:
Hebrew letters map by alphabet position, final forms fold onto the regular letter
(`א→a ב→b ג→c ד→d ה→e ו→f ז→g ח→h ט→i י→j כ/ך→k ל→l מ/ם→m נ/ן→n ס→o ע→p פ/ף→q צ/ץ→r ק→s ר→t ש→u ת→v`);
ASCII `a-z` is accepted as-is. A trailing `'` / geresh / `.` / `)` is ignored. So `num 3, part "ב"` is
`DEMO-A-Q3b`. No part: `DEMO-A-Q3`. (`num`, `part`) must be unique per exam.

## Kinds and requirements
- Every kind except `mcq` needs `solution` (+ `solutionSource`) **or** a `hold` reason.
- `steps` and `rubric` require a `solution` (they are derived from it); `rubric`/`steps` are optional
  (warned as "not yet") so a bank can be transcribed before the step-author phase.
- `mcq`: `options` (2–8, ids `a..h`), `correctId`, optional `acceptedIds` (>=2, starts with `correctId`),
  `lockOrder`, `explanation`; `solution` optional. `options`/`correctId`/… on any other kind is an error.
- `truefalse`: `verdict` boolean (the student's first choice); proof steps follow.

## Steps (2–6 typical; each gets `prompt` rich text, optional `explain`)
| type | fields |
|---|---|
| `choice` | `options` (as mcq, ids a..h), `correctId`. Also used for a **trace** ("state after step k") |
| `numeric` | `answer` number, `tol` >= 0 (default 0). A numeric **trace** is just this |
| `text` | `accept` [strings], `normalize`: `none` (default) \| `complexity` (`O(n log n)` ~ `O(nlogn)`) \| `lower` |
| `order` | `lines` — stored in the **correct order**; the UI shuffles. Identical lines are allowed (two `}`) |
| `findbug` | `lines` (the broken version) + `bugIndex` (0 <= bugIndex < len(lines)) |
| `fillblank` | `lines` (one contains the `___` placeholder) + `blankIndex` + `options` + `correctId` |

`"code": true` on `order` / `findbug` / `fillblank` marks the lines (and fillblank text options) as literal
code: HTML-escaped only, no `$`/backtick/`**` parsing. Without it, lines are rich text.
Invariants (not machine-checked): every `order`/`findbug` line derives from `solution`; a `findbug`
variant changes exactly one line; steps never contradict the solution.

## Rich text
- Inline math `$…$`, display math `$$…$$` — TeX for KaTeX, rendered to MathML at build time.
  **No Hebrew inside `$…$`.** Literal `$` → `\$`.
- `**bold**`, `` `code` `` (LTR), `\n` = line break.
- **Fenced code block** (multi-line code: C, MIPS, C++): a line that is exactly three backticks (optionally followed by a short language tag: `c`, `cpp`, `asm`) opens it and a line that is exactly three backticks closes it. The content is literal: HTML-escaped only, no `$` math, no `**`, no backtick parsing, indentation and blank lines preserved. It renders as an LTR, left-aligned `<pre class="code-block">` that scrolls sideways by itself. An unclosed fence fails `validate.py` and the build, naming the item id. Never write multi-line code as one `` `backtick span` `` per line.
- **Inline figure** (a plot or sketch inside a solution, explanation or brief): a line consisting only of `![alt text](images/exams/<file>.png)`. It renders as `<figure class="rt-fig"><img ...><figcaption>alt text</figcaption></figure>` (responsive, click to zoom). The file must exist under `images/exams/` (crop it with `tools/crop.py`); a missing file fails `validate.py`, the build and `course_lint.js`, naming the item id. The alt text is shown as the caption and goes through the `redact.txt` check. Any other use of `![` is an error.

## Learn mode (briefs)
Every app has a learn mode: one Hebrew brief per topic, built to `learn.js` (never hand-edited, gitignored).
- `course.config.json` `briefs`: `[["01 - topic.md", "chapter_id", "topic_key", "topic"|"cheat"], ...]` in study order.
  `"topic"` chapters get a "practice this topic" button (jumps to topic practice) and an auto list of that topic's
  exam questions; `"cheat"` chapters are cross-topic cheat sheets. Empty `briefs` = no learn mode (entry button hidden,
  `build_learn.py` writes nothing). A topic without a brief only warns.
- `docs/briefs/<file>.md`: first `# ` line = chapter title; the rest is markdown (`## ` sections, lists, tables,
  `> 💡/🪤/⚠️/🔑/✅/❌` callouts) plus the bank's rich text: `$..$` / `$$..$$` math (rendered to MathML at build, no Hebrew
  inside), `` `code` ``, ``` fenced code blocks (LTR `<pre class="code-block">`), inline figure lines
  `![alt](images/exams/<file>.png)`, `` `24B-A-Q3` `` (a backticked question id becomes a button that peeks at the question;
  an unknown id fails), `[[chapter_id]]` / `[[chapter_id|label]]` (cross-reference; unknown id fails).
- Build: `PYTHONUTF8=1 py tools/build_learn.py` (after `build_questions.py`; rerun when the bank changes).
  `tools/redact.txt` names in a brief fail the build. Check: `node tools/verify_learn.js` (390px/1000px, no overflow, no
  console errors) and the learn section of `node tools/verify_dom.js` (skipped with a message when `learn.js` is absent).
- Deep link: `index.html?learn=<chapter_id>`. Files named `*demo*` under `docs/briefs/` are template demos; `new_app.py`
  does not copy them.

## Derived at build (do NOT put in raw)
`id`, `partKey`, `examCode`, `examLabel`, `year`, `source`, `topicLabel`, `pointsTotal` (sum of rubric
points; falls back to `points`), `lockOrder` (mcq, auto), namespaced `contextId`, and the Html twins:
`questionHtml`, `solutionHtml`, `explanationHtml`, `rubric[i].html`, `pitfallsHtml[i]`,
`steps[i].promptHtml` / `explainHtml` / `linesHtml[j]`, option `.html`, context `textHtml` /
`captionHtml` / `titleHtml` / `codeHtml`.

## Build output
`window.OPEN_BANK = { meta:{course, topics, kinds, built, exams, counts}, contexts, questions }`.
Held questions are never in the bank. Unless `course.config.json` sets `"includeDrafts": true`, AI-drafted
parts are stripped but the question still ships with its solution: `stepsSource: "ai-draft"` removes `steps`;
`rubricSource: "ai-draft"` removes `rubric`, `pitfalls` and `pointsTotal`. Stripped parts are listed in
`build_report.md`.
Any validation problem, missing figure, KaTeX error or Hebrew in math exits non-zero, names the
question id, and writes nothing.

## Blind verification
`py tools/gen/verify_strip.py strip <CODE>` writes `_blind_<CODE>.json` with no `solution`, `steps`,
`rubric`, `pitfalls`, `correctId`, `acceptedIds`, `verdict` or `explanation` anywhere.


## Anonymization (`tools/redact.txt`)
Student solutions ship with **no author names**. Optional file `tools/redact.txt`: one name per line, `#` starts a
comment, blank lines ignored. List FULL names only: matching is a case-insensitive whole-word match (a name is not
matched inside a longer word, so a prefixed form such as ל+name needs its own line). `tools/validate.py` fails on any
listed name found (Unicode-NFC, Hebrew-safe) in **any** shipped text field -- exam fields (`examLabel`, `sourceFile`, `solutionFile` ...),
contexts, questions, options, solutions/explanations, rubric, pitfalls, steps. The message starts with the item id and
names the field (`DEMO-A-Q3: redact.txt entry #2 found in solution ...`); it does not echo the name. `tools/course_lint.js`
applies the same list to every string of every course level. The triager fills the file from folder/file names that look
like person names; keep it out of git (it is a list of the very names being hidden). The solution label in the UI is
"פתרון סטודנט"; the transcriber strips names, initials, student ids and handles from the text and from figure crops.

## Guided courses ("צריך עזרה?")
Per hard topic area (2-5 per app, chosen at the triage gate) a ladder of 6-10 levels, small to exam-sized. Each level
runs **lesson -> quiz -> summary**; levels are all open (soft unlock), a level is passed at **PASS = 80%** (constant in
`course-ui.js`; `course_lint.js` checks it), the first unpassed level is highlighted, progress lives in
`localStorage` under `<storePrefix>_course_<id>_v1` (every access in try/catch, in-memory fallback), separate from the
bank stats. The last level is the **boss** (`boss: true`): built from real exam questions and offering a jump to bank
practice on the course topic.

**Config** (`course.config.json`): `"needHelp": [{"id","titleHe","icon","topic","entryLabelHe","introHe?"}]`
(0-8 entries; `id` = the folder `courses/<id>/`, `[A-Za-z0-9_-]+`; `topic` from the closed topics list). An empty list
hides the header entry and the start-screen cards.

**Files**: `courses/<id>/<LEVEL>.js` (source, hand-written -- like `tools/raw`, they are the source of truth) ->
`tools/build_courses.py` (run at the end of `build_questions.py`) -> `courses.js` (`window.COURSES`, built, gitignored)
-> `course-ui.js` (screens). Deep links: `?course=<id>`, `?course=<id>&level=<LEVEL>`, `...&play=1`.

**Level file** -- plain data, one `COURSE_LEVEL` call per file (the file name is the level id):
```js
COURSE_LEVEL("DEMO", {
  id: "C01", order: 1, icon: "...", title: "short", goal: "one sentence: what you can do after this level",
  boss: false,                      // true only on the last level
  source: "ai-verified",            // ai-draft | ai-verified -- labels the authored content like steps are labelled
  lesson: { html: String.raw`<p>...</p>`, figs: [{ src: "images/...", alt: "", caption: "" }] },   // figs optional
  questions: [
    { id: "C01-Q1", question: "rich text", options: [{ id: "a", value: "..." }, { id: "b", value: "..." }],
      correctId: "b", explanation: "why right AND why each distractor is wrong", recap: "one-line rule" },
    { bankId: "24B-A-Q7", recap: "..." },          // a real exam question, rendered from the bank verbatim
    { id: "C01-Q2", step: { type: "numeric", prompt: "rich text", answer: 20, tol: 0, explain: "..." }, recap: "..." },   // open template only: a guided step IS the question
  ],
});
```
- **Math**: pre-rendered at build time with the SAME KaTeX -> MathML path as the bank (`render_math.js`, `dir="ltr"` on
  every `<math>`), so lessons ship no math JS. In `lesson.html` write `$...$` / `$$...$$` TeX; in `question`, `option
  value`, `explanation`, `recap` use the bank's rich text (`$..$`, `` `code` ``, `**bold**`, `\n`). No Hebrew inside a
  math span (build fails). Literal dollar: `&#36;` in lesson html, `\$` in rich text.
- **Write lessons with the JS tag `String.raw`** (a template literal prefixed by `String.raw`): in a normal JS string `\frac`, `\times` and `\neq` turn into a form feed, a tab and a newline. `course_lint.js` reports such control characters.
- Lesson html: `<p> <h3> <ul>/<li> <table> <b> <code> <pre>` plus the boxes `<div class="lesson-rule">🔑 ...</div>`,
  `lesson-trap` (⚠️), `lesson-ex` (worked example), `lesson-formula`. Bidi: at runtime every Latin/number run inside
  Hebrew text is isolated LTR (ported from machine-learning-quiz c034e8f); MathML is left alone. Two formulas joined only
  by a comma form one run -- separate them with a Hebrew word.
- **Teach before you ask**: every concept a level's questions rely on is taught in that level's lesson or an earlier one.
  Original questions have no letter references ("תשובות א ו-ג") -- options are shuffled.
- Question ids are unique per course. A `bankId` question keeps the bank's own `lockOrder` and explanation. Never cite an exam id inside a question stem (the explanation may).
- `explanation` is required (it is what the student reads after a miss); `recap` is shown in the summary list for missed
  questions. `source: "ai-draft"` is a lint warning (an error with `--strict`); a course ships `ai-verified` only after
  the refuter passed it (`course_dump.js`).

**Tools** (all ASCII on stdout):
- `node tools/course_lint.js [--strict] [courseId]` -- level ids/orders unique, at most one boss and it is last, boss
  has `bankId` questions, every `bankId` exists in the built bank (`questions.json`), `correctId`/`acceptedIds` among the
  options, explanations present, no Hebrew in math, no redacted name, no eaten TeX backslash, PASS sane. Exits 1 on
  errors; every message starts with `[<course>/<level>]`.
- `node tools/course_dump.js <courseId>` -> `tools/raw/_blind_course_<id>.json`: the questions with **no answers** (no
  `correctId`, explanation, recap or lesson) for the blind refuter. `--claims` writes the key
  (`_claims_course_<id>.json`); `--compare` checks the refuter's `_verify_course_<id>.json`
  (`{"answers": {"<question id>": {"answer": ...}}}`) against it and exits 1 on any disagreement.
- `py tools/build_courses.py` -- rebuild only `courses.js`.

**Open template extras.** A level question may be a guided step, rendered by `Steps.render` (steps.js, unchanged):
`{ id: "C01-Q2", step: { type: "numeric", prompt: "rich text", answer: 20, tol: 0, explain: "..." }, recap: "..." }`
-- `type` is any of `choice|numeric|text|order|findbug|fillblank` with the fields of the bank's steps (see "Steps" above);
the step is validated by `validate.check_step` at build and re-checked by the lint, and the step IS the question (its
prompt is the stem). A `bankId` question renders by its bank kind: `mcq` as an MCQ, `truefalse` as the verdict buttons
(then the solution), a question **with steps** as its guided steps (right = every step right; a "show me the solution"
button counts as a miss), anything else (steps stripped as ai-draft, say) as reveal-the-solution then a
self-mark. `--compare` answers for steps: option id (choice/fillblank), number (numeric), string (text), the lines in
order (order), the line index (findbug).
