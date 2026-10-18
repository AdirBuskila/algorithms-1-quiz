# -*- coding: utf-8 -*-
"""Build the guided "need help?" courses bundle:  courses/<id>/*.js  ->  ../courses.js

Level files are authored as JS data (window.COURSE_LEVEL("<id>", {...}); see tools/RAW_SCHEMA.md,
"Guided courses"). This build loads them (tools/course_load.js), renders every rich-text field and
writes  window.COURSES = { "<id>": { levels: [...] } };  with the math PRE-RENDERED to MathML by the same
KaTeX path as the bank (render_math.js, dir="ltr" on every <math>), so the page ships no math JS:

  lesson.html              author-written HTML; every $..$ / $$..$$ span becomes MathML
  question / explanation / recap / option value   rich text like the bank ($..$, `code`, **bold**, \\n)
                           -> questionHtml / explanationHtml / recapHtml / option html
  step (open engine)       a guided-step object exactly as in a bank question's steps (tools/RAW_SCHEMA.md);
                           checked with validate.check_step, built with build_questions.make_step

Run by tools/build_questions.py after the bank is written (or alone:  PYTHONUTF8=1 py tools/build_courses.py).
A KaTeX error, Hebrew inside a math span, an unbalanced $ or an invalid step fails the build and writes nothing.
Structural problems (bad bankId, correctId ...) are tools/course_lint.js's job. Prints ASCII only.
"""
import html, json, pathlib, re, subprocess, sys

TOOLS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import richtext as rt  # noqa: E402
import validate  # noqa: E402
from build_questions import OUT, locks_order, make_option, make_step  # noqa: E402

MathBank, HEB, rich_html = rt.MathBank, rt.HEB, rt.rich_html

LESSON_MATH = re.compile(r"\$\$([\s\S]+?)\$\$|(?<![$\\])\$([^$\n]+?)\$")
ESC = "\x00"


def lesson_html(h, bank, where, errs):
    """Author HTML with $..$ / $$..$$ -> HTML with @@M<n>@@ / @@D<n>@@ placeholders. Literal dollar: \\$ or &#36;."""
    h = h.replace("\\$", ESC)

    def sub(m):
        display = m.group(1) is not None
        tex = (m.group(1) if display else m.group(2)).strip()
        if HEB.search(tex):
            errs.append((where, tex, "Hebrew inside math span"))
            return ""
        if not tex:
            errs.append((where, "", "empty math span"))
            return ""
        return f"@@{'D' if display else 'M'}{bank.add(tex, display, where)}@@"

    h = LESSON_MATH.sub(sub, h)
    if "$" in h:
        errs.append((where, "", "unbalanced $ in lesson html (use \\$ or &#36; for a literal dollar)"))
    return h.replace(ESC, "$")


def load_levels():
    proc = subprocess.run(["node", str(TOOLS / "course_load.js")], capture_output=True, text=True,
                          encoding="utf-8", cwd=str(TOOLS))
    if proc.returncode != 0:
        sys.stderr.write("course_load.js failed:\n" + proc.stderr.encode("ascii", "backslashreplace").decode() + "\n")
        sys.exit(2)
    return json.loads(proc.stdout)


def main():
    loaded = load_levels()
    if loaded["errors"]:
        sys.stderr.write(f"COURSES BUILD FAILED -- {len(loaded['errors'])} level file(s) do not load, nothing written:\n")
        for e in loaded["errors"]:
            sys.stderr.write("  - " + e.encode("ascii", "backslashreplace").decode() + "\n")
        sys.exit(1)

    bank, errs = MathBank(), []
    step_problems = []
    courses = {}
    for entry in loaded["levels"]:
        cid, lv = entry["courseId"], entry["level"]
        lid = lv.get("id") or entry["file"]
        w = f"{cid}/{lid}"
        L = {k: lv[k] for k in ("id", "order", "icon", "title", "goal", "source") if k in lv}
        L["boss"] = lv.get("boss") is True
        goal = str(L.get("goal") or "")
        if any(t in goal for t in ("$", "`", "**")):   # a rich goal: math / code / bold rendered like the questions
            L["goalHtml"] = rich_html(goal, bank, w + " goal", errs)
        lesson = dict(lv.get("lesson") or {})
        lesson["html"] = lesson_html(str(lesson.get("html") or ""), bank, w + " lesson", errs)
        L["lesson"] = lesson
        qs = []
        for i, q in enumerate(lv.get("questions") or []):
            if not isinstance(q, dict):
                continue
            qw = f"{w} q{i + 1}"
            q = dict(q)
            if "bankId" in q:
                if q.get("recap"):
                    q["recapHtml"] = rich_html(q["recap"], bank, qw + " recap", errs)
                qs.append(q)
                continue
            if "step" in q:
                sp = []
                validate.check_step(qw + " step", q["step"], sp.append, OUT)
                step_problems.extend(sp)
                if not sp:
                    q["step"] = make_step(q["step"], qw + " step", bank, errs)
                if q.get("recap"):
                    q["recapHtml"] = rich_html(q["recap"], bank, qw + " recap", errs)
                qs.append(q)
                continue
            q["questionHtml"] = rich_html(q.get("question") or "", bank, qw, errs)
            q["explanationHtml"] = rich_html(q.get("explanation") or "", bank, qw + " expl", errs)
            if q.get("recap"):
                q["recapHtml"] = rich_html(q["recap"], bank, qw + " recap", errs)
            q["options"] = [make_option(o, f"{qw} opt {o.get('id')}", bank, errs, False) for o in (q.get("options") or [])]
            if "lockOrder" not in q and locks_order(q["options"]):
                q["lockOrder"] = True
            qs.append(q)
        L["questions"] = qs
        courses.setdefault(cid, {"levels": []})["levels"].append(L)

    if step_problems:
        sys.stderr.write(f"COURSES BUILD FAILED -- {len(step_problems)} invalid step(s), nothing written:\n")
        for p in step_problems:
            sys.stderr.write("  - " + p.encode("ascii", "backslashreplace").decode() + "\n")
        sys.exit(1)
    errs += bank.render()
    if errs:
        sys.stderr.write(f"COURSES BUILD FAILED -- {len(errs)} math/text error(s), nothing written:\n")
        for where, tex, err in errs:
            sys.stderr.write(f"  - {where}: ${tex}$ -> {err}\n".encode("ascii", "backslashreplace").decode())
        sys.exit(1)

    def sub(m):
        kind, i = m.group(1), int(m.group(2))
        cls = {"D": "math-block", "M": "math-inline", "N": "math-inline opt-math"}[kind]
        return f'<span class="{cls}">{bank.html[i]}</span>'

    def fix(x):
        if isinstance(x, str):
            return re.sub(r"@@([MDN])(\d+)@@", sub, x) if "@@" in x else x
        if isinstance(x, list):
            return [fix(v) for v in x]
        if isinstance(x, dict):
            return {k: fix(v) for k, v in x.items()}
        return x

    courses = fix(courses)
    for c in courses.values():
        c["levels"].sort(key=lambda l: l.get("order", 0))
    payload = json.dumps(courses, ensure_ascii=False, indent=1)
    (OUT / "courses.js").write_text("window.COURSES = " + payload + ";\n", encoding="utf-8")
    n_lv = sum(len(c["levels"]) for c in courses.values())
    n_q = sum(len(L["questions"]) for c in courses.values() for L in c["levels"])
    print(f"courses={len(courses)} levels={n_lv} questions={n_q} math={len(bank.items)}")


if __name__ == "__main__":
    main()
