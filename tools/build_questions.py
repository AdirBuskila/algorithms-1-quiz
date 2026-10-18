# -*- coding: utf-8 -*-
"""Merge per-exam raw JSON files into the course question bank (config: ../course.config.json).

Inputs : tools/raw/<CODE>.json  (contract: tools/RAW_SCHEMA.md). Files whose name starts
         with "_" are skipped (fixtures / scratch).
Outputs: ../questions.json   { meta, contexts, questions }
         ../questions.js     window.OPEN_BANK = {...};
         ../courses.js       window.COURSES = {...};  the guided "need help?" courses (tools/build_courses.py, run at the end)
         build_report.md

Derived here (never in raw): id (<CODE>-Q<num><part>), examCode, examLabel, year, source,
topicLabel, partKey, pointsTotal, auto-lockOrder (mcq), namespaced contextId, and the *Html
twins of every rich-text field with math pre-rendered to MathML:
  questionHtml, solutionHtml, explanationHtml, rubric[i].html, pitfallsHtml[i],
  steps[i].promptHtml / explainHtml / linesHtml[j], option .html (question and step options),
  context textHtml / captionHtml / titleHtml / codeHtml.

Any validation problem (tools/validate.py rules), missing figure, KaTeX error or Hebrew inside
a math span fails the build loudly, names the question id, and writes nothing.
Questions on hold are left out of the bank. Unless config includeDrafts is true, AI-drafted parts
are stripped (the question still ships with its solution): stepsSource "ai-draft" removes `steps`;
rubricSource "ai-draft" removes `rubric`, `pitfalls` and `pointsTotal`. Listed in build_report.md.

Run:  PYTHONUTF8=1 py tools/build_questions.py
Prints ASCII only (the Windows console is cp1255); Hebrew goes to UTF-8 files.
"""
import collections, datetime, json, pathlib, re, sys

TOOLS = pathlib.Path(__file__).resolve().parent
EXAM_RE = re.compile(r"^(\d{2}[A-Z]-[A-Z]|SAMP-\d+|DEMO-[A-Z])\.json$")  # only real exam files; tmp_*/_verify_*/_blind_* are ignored
RAW = TOOLS / "raw"
OUT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from course_config import load as _load_cfg  # noqa: E402
import richtext as rt  # noqa: E402
import validate  # noqa: E402

CFG = _load_cfg()
TOPIC_LABEL = {k: v for k, v in CFG["topics"]}
HEB_LETTER = "א-ת"

# An option that cites its SIBLINGS by printed letter ("תשובות א ו-ב נכונות", "א' ו-ג'",
# "רק ב,ג") must keep the printed order -- shuffling would point the reference at whatever
# landed in those slots. "כל התשובות האחרות" / "אף אחת מהתשובות" cite no letter: no lock.
_L = r"(?<![%s])[אבגדה]['׳]?(?![%s])" % (HEB_LETTER, HEB_LETTER)
LETTER_PAIR = re.compile(_L + r"\s*(?:,|\+|&|-|/|או|וגם|ו-?)\s*" +
                         r"[אבגדה]['׳]?(?![%s])" % HEB_LETTER)
LETTER_NAMED = re.compile(r"(?:תשובה|תשובות|סעיף|סעיפים|אפשרות|אפשרויות)\s+[אבגדה]['׳]?(?![%s])"
                          % HEB_LETTER)


def locks_order(options):
    for o in options:
        if (o.get("type") or "text") != "text":
            continue
        v = str(o.get("value", ""))
        if LETTER_PAIR.search(v) or LETTER_NAMED.search(v):
            return True
    return False


def exam_order(code):
    m = re.match(r"^(\d{2})([ABS])-([A-H])$", code)
    if code.startswith("SAMP-"):
        return (0, 0, code)
    if m:
        return (1, int(m.group(1)), code)
    return (2, 0, code)


def fail(lines, header):
    sys.stderr.write(header + "\n")
    for ln in lines:
        sys.stderr.write("  - " + str(ln).encode("ascii", "backslashreplace").decode() + "\n")
    sys.exit(1)


def main():
    raw_files = [p for p in sorted(RAW.glob("*.json")) if EXAM_RE.match(p.name)]
    bank = rt.MathBank()
    math_errors = []
    contexts, questions = {}, []
    exams_meta, held, drafts = [], [], []

    # ---- 1. validate every raw file first: nothing is built from an invalid file
    problems, warnings = [], []
    for fp in raw_files:
        p, w, _n, _bt = validate.check_file(fp)
        problems += p
        warnings += w
    if problems:
        fail(problems, f"BUILD FAILED -- {len(problems)} problem(s), nothing written:")

    def rh(s, where):
        return rt.rich_html(s, bank, where, math_errors)

    # ---- 2. transform
    for fp in raw_files:
        data = rt.unescape_quotes(json.loads(fp.read_text(encoding="utf-8")))
        code = data.get("examCode") or fp.stem
        label = data.get("examLabel", code)
        year = data.get("year")
        source = "sample" if code.startswith("SAMP-") else "exam"
        exams_meta.append({"examCode": code, "examLabel": label, "year": year, "source": source,
                           "examDate": data.get("examDate")})

        cmap = {}
        for cid, ctx in (data.get("contexts") or {}).items():
            gid = f"{code}-{cid}"
            c = dict(ctx)
            c["id"] = gid
            where = f"{code} ctx {cid}"
            if c.get("text"):
                c["textHtml"] = rh(c["text"], where)
            if c.get("code"):
                c["codeHtml"] = rt.code_html(c["code"])
            if c.get("caption"):
                c["captionHtml"] = rh(c["caption"], where + " caption")
            if c.get("title"):
                c["titleHtml"] = rh(c["title"], where + " title")
            contexts[gid] = c
            cmap[cid] = gid

        for raw_q in data.get("questions", []):
            qid = rt.question_id(code, raw_q)
            if raw_q.get("hold"):
                held.append(f"{qid}: {raw_q['hold']}")
                continue
            q = dict(raw_q)
            if not CFG["includeDrafts"]:
                # ship the question with its solution, minus the AI-drafted parts
                if q.get("stepsSource") == "ai-draft":
                    for k in ("steps", "stepsSource"):
                        q.pop(k, None)
                    drafts.append(f"{qid}: steps")
                if q.get("rubricSource") == "ai-draft":
                    for k in ("rubric", "rubricSource", "pitfalls"):
                        q.pop(k, None)
                    q["_noRubric"] = True
                    drafts.append(f"{qid}: rubric+pitfalls")
            q["id"] = qid
            q["partKey"] = rt.part_suffix(q.get("part")) or ""
            q["examCode"], q["examLabel"], q["year"], q["source"] = code, label, year, source
            q["topicLabel"] = TOPIC_LABEL[q["topic"]]
            if q.get("contextId"):
                q["contextId"] = cmap[q["contextId"]]
            q["questionHtml"] = rh(q["question"], qid)
            if q.get("solution"):
                q["solutionHtml"] = rh(q["solution"], qid + " solution")
            if q["kind"] == "mcq":
                q["explanation"] = q.get("explanation") or ""
                q["explanationHtml"] = rh(q["explanation"], qid + " explanation")
                if "lockOrder" not in q and locks_order(q["options"]):
                    q["lockOrder"] = True
                if q.get("lockOrder") is False:
                    q.pop("lockOrder")
                q["options"] = [make_option(o, f"{qid} opt {o['id']}", bank, math_errors, False)
                                for o in q["options"]]
            if q.get("rubric"):
                q["rubric"] = [dict(r, html=rh(r["text"], f"{qid} rubric[{i}]"))
                               for i, r in enumerate(q["rubric"])]
                q["pointsTotal"] = sum(r["points"] for r in q["rubric"])
            elif not q.pop("_noRubric", False):
                q["pointsTotal"] = q.get("points") or 0
            if q.get("pitfalls"):
                q["pitfallsHtml"] = [rh(x, f"{qid} pitfalls[{i}]") for i, x in enumerate(q["pitfalls"])]
            if q.get("steps"):
                q["steps"] = [make_step(s, f"{qid} step[{i}]", bank, math_errors)
                              for i, s in enumerate(q["steps"])]
            questions.append(q)

    math_errors += bank.render()
    if math_errors:
        fail([f"{w}: ${t}$ -> {e}" for w, t, e in math_errors],
             f"BUILD FAILED -- {len(math_errors)} math error(s), nothing written:")

    # ---- 3. resolve math placeholders everywhere
    def sub(m):
        kind, i = m.group(1), int(m.group(2))
        mm = bank.html[i]
        cls = {"D": "math-block", "M": "math-inline", "N": "math-inline opt-math"}[kind]
        return f'<span class="{cls}">{mm}</span>'

    def resolve_all(x):
        if isinstance(x, str):
            return re.sub(r"@@([MDN])(\d+)@@", sub, x) if "@@" in x else x
        if isinstance(x, list):
            return [resolve_all(v) for v in x]
        if isinstance(x, dict):
            return {k: resolve_all(v) for k, v in x.items()}
        return x

    contexts = resolve_all(contexts)
    questions = resolve_all(questions)
    questions.sort(key=lambda q: (exam_order(q["examCode"]), q["num"], q["partKey"]))
    exams_meta.sort(key=lambda e: exam_order(e["examCode"]))

    present = {q["kind"] for q in questions}
    kinds = [k for k in validate.KINDS if k in present]
    n_steps = collections.Counter(s["type"] for q in questions for s in q.get("steps", []))
    payload_obj = {
        "meta": {
            "course": {"slug": CFG["slug"], "title": CFG["titleHe"], "description": CFG["descriptionHe"],
                       "accent": CFG["accent"], "accent2": CFG["accent2"],
                       "storePrefix": CFG["storePrefix"], "needHelp": CFG["needHelp"]},
            "topics": [{"key": k, "label": v} for k, v in TOPIC_LABEL.items()],
            "kinds": kinds,
            "built": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "exams": exams_meta,
            "counts": {"total": len(questions), "contexts": len(contexts), "math": len(bank.items),
                       "steps": sum(n_steps.values())},
        },
        "contexts": contexts,
        "questions": questions,
    }
    payload = json.dumps(payload_obj, ensure_ascii=False, indent=1)
    (OUT / "questions.json").write_text(payload + "\n", encoding="utf-8")
    (OUT / "questions.js").write_text("window.OPEN_BANK = " + payload + ";\n", encoding="utf-8")

    by_topic = collections.Counter(q["topic"] for q in questions)
    by_exam = collections.Counter(q["examCode"] for q in questions)
    by_kind = collections.Counter(q["kind"] for q in questions)
    L = ["# Build report - " + CFG["titleHe"] + " (open engine)", "",
         f"- Raw exam files: **{len(raw_files)}**",
         f"- **Final questions: {len(questions)}**",
         f"- Shared context blocks: **{len(contexts)}**",
         f"- Math spans rendered (distinct): **{len(bank.items)}**",
         f"- Guided steps: **{sum(n_steps.values())}** {dict(n_steps)}",
         f"- includeDrafts: **{CFG['includeDrafts']}**",
         f"- **ai-draft parts stripped: {len(drafts)}** " + ", ".join(drafts),
         f"- **On hold (not in bank): {len(held)}**", ""] + [f"  - {h}" for h in held] + ["",
         "## By kind", ""] + [f"- {k}: {by_kind.get(k, 0)}" for k in validate.KINDS] + ["",
         "## By topic", "", "| topic | label | n |", "|---|---|---|"]
    for k, v in TOPIC_LABEL.items():
        L.append(f"| `{k}` | {v} | {by_topic.get(k, 0)} |")
    L += ["", "## By exam", ""]
    for c in sorted(by_exam, key=exam_order):
        L.append(f"- {c}: {by_exam[c]}")
    if warnings:
        L += ["", "## Warnings", ""] + [f"- {w}" for w in warnings]
    (TOOLS / "build_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"files={len(raw_files)} final={len(questions)} kinds={','.join(kinds)} "
          f"drafts_excluded={len(drafts)} held={len(held)} contexts={len(contexts)} math={len(bank.items)}")
    print("by_topic:", dict(by_topic))
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print("  -", w.encode("ascii", "backslashreplace").decode())

    import build_courses  # the guided courses bundle (courses.js); needs only node + the level files
    build_courses.main()


def make_option(o, where, bank, math_errors, code):
    """Option dict + html twin. `code` = the option text is a literal code line."""
    o = dict(o)
    o["type"] = o.get("type") or "text"
    if o["type"] == "math":
        tex = str(o["value"]).strip()
        if rt.HEB.search(tex):
            math_errors.append((where, tex, "Hebrew inside math option"))
            o["html"] = ""
        else:
            o["html"] = f"@@N{bank.add(tex, False, where)}@@"
    elif o["type"] == "image":
        o["html"] = f'<img class="opt-img" src="{rt.html.escape(str(o["value"]))}" alt="" loading="lazy">'
    elif code:
        o["html"] = rt.code_html(o["value"])
    else:
        o["html"] = rt.rich_html(o["value"], bank, where, math_errors)
    return o


def make_step(s, where, bank, math_errors):
    s = dict(s)
    code = s.get("code") is True
    s["promptHtml"] = rt.rich_html(s["prompt"], bank, where + " prompt", math_errors)
    s["explainHtml"] = rt.rich_html(s.get("explain") or "", bank, where + " explain", math_errors)
    if "lines" in s:
        shown = s["lines"]
        if code:   # display only: drop the indentation all lines share (cut from deep inside a function, it pushed lines past a phone's width)
            ind = [len(r) - len(r.lstrip(" \t")) for x in shown for r in str(x).split("\n") if r.strip()]
            cut = min(ind) if ind else 0
            shown = ["\n".join(r[cut:] if r.strip() else r.strip() for r in str(x).split("\n")) for x in shown]
        s["linesHtml"] = [rt.code_html(x) if code
                          else rt.rich_html(x, bank, f"{where} line {j}", math_errors)
                          for j, x in enumerate(shown)]
    if "options" in s:
        s["options"] = [make_option(o, f"{where} opt {o['id']}", bank, math_errors, code)
                        for o in s["options"]]
    return s


if __name__ == "__main__":
    main()
