# -*- coding: utf-8 -*-
"""Lint tools/raw/*.json against tools/RAW_SCHEMA.md. Run before build_questions.py
(the build runs the same checks and aborts on any problem).

    PYTHONUTF8=1 py tools/validate.py            # all raw files (skips names starting "_")
    PYTHONUTF8=1 py tools/validate.py DEMO-A     # just one exam code (or a path)

Every message starts with the question id (<CODE>-Q<num><part>, e.g. DEMO-A-Q3b).
Exit code 1 if any PROBLEM is found. Prints ASCII only.
"""
import json, pathlib, re, sys, collections, unicodedata

TOOLS = pathlib.Path(__file__).resolve().parent
EXAM_RE = re.compile(r"^(\d{2}[A-Z]-[A-Z]|SAMP-\d+|DEMO-[A-Z])\.json$")  # only real exam files; tmp_*/_verify_*/_blind_* are ignored
RAW = TOOLS / "raw"
ROOT = TOOLS.parent

sys.path.insert(0, str(TOOLS))
from course_config import load as _load_cfg  # noqa: E402
from richtext import part_suffix, question_id  # noqa: E402

TOPICS = {k for k, _ in _load_cfg()["topics"]}   # closed list, single source
KINDS = ("computation", "proof", "algorithm", "code", "mcq", "truefalse")
STEP_TYPES = ("choice", "numeric", "text", "order", "findbug", "fillblank")
OPT_TYPES = {"text", "math", "image"}
OPT_IDS = ("a", "b", "c", "d", "e", "f", "g", "h")
CONFIDENCE = {"high", "med", "low"}
RUBRIC_SOURCES = {"official", "ai-draft", "ai-verified"}
STEPS_SOURCES = {"official", "ai-draft", "ai-verified"}
SOLUTION_SOURCES = {"official-pdf", "lecturer-solution", "student-solution", "solved"}
CONTEXT_KINDS = {"image", "text", "code"}
NORMALIZE = {"none", "complexity", "lower"}
DERIVED = {"id", "examCode", "examLabel", "year", "source", "topicLabel", "dedupKey", "pointsTotal"}
EXAM_KEYS = {"examCode", "examLabel", "year", "examDate", "sourceFile", "solutionFile", "contexts", "questions"}
CONTEXT_KEYS = {"kind", "title", "text", "image", "caption", "code"}
QUESTION_KEYS = {"num", "part", "kind", "topic", "points", "question", "contextId", "image", "solution",
                 "solutionSource", "official", "confidence", "hold", "rubric", "rubricSource", "pitfalls",
                 "steps", "stepsSource", "options", "correctId", "acceptedIds", "lockOrder", "explanation",
                 "verdict"}
STEP_KEYS = {"type", "prompt", "explain", "code", "options", "correctId", "answer", "tol", "accept",
             "normalize", "lines", "bugIndex", "blankIndex"}
RUBRIC_KEYS = {"text", "points"}
OPTION_KEYS = {"id", "type", "value"}
CODE_RE = re.compile(r"^(\d{2}[ABS]-[A-H]|SAMP-\d+|DEMO-[A-Z])$")
HEB = re.compile(r"[֐-׿]")
TOKEN = re.compile(r"(\$\$.+?\$\$|\$[^$]+?\$|`[^`]+`)", re.S)


# ---------------------------------------------------------------- anonymization (tools/redact.txt)
def load_redact():
    """Author names that must never ship (student solutions are anonymized). Optional file
    tools/redact.txt: one FULL name per line, '#' starts a comment. Matching is a case-insensitive
    whole-word match on NFC-normalized text (a name is not matched inside a longer word, so list
    prefixed or inflected forms as their own lines); Hebrew names (no case) match exactly."""
    fp = TOOLS / "redact.txt"
    if not fp.is_file():
        return []
    out = []
    for ln in fp.read_text(encoding="utf-8-sig").splitlines():
        ln = ln.split("#", 1)[0].strip()
        if ln:
            out.append(ln)
    return out


def _fold(s):
    return unicodedata.normalize("NFC", str(s)).casefold()


def _wordchar(c):
    return c == "_" or unicodedata.category(c)[0] in "LNM"


def contains_word(text, name):
    """name occurs in text with no letter/digit/mark/underscore directly before or after it
    (both arguments already folded). Hebrew-aware: a name inside a longer word does not match."""
    start = text.find(name)
    while start != -1:
        end = start + len(name)
        if (start == 0 or not _wordchar(text[start - 1])) and (end == len(text) or not _wordchar(text[end])):
            return True
        start = text.find(name, start + 1)
    return False


def _strings(x, path):
    """Yield (path, text) for every string value inside x."""
    if isinstance(x, str):
        yield path, x
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from _strings(v, f"{path}[{i}]")
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from _strings(v, f"{path}.{k}" if path else str(k))


def redact_problems(data, code, qid_of, names):
    """A listed name in ANY shipped text field (questions, options, solutions/explanations, rubric,
    pitfalls, steps, contexts, sourceFile/solutionFile/examLabel ...) is a problem; the message
    starts with the item id. The name itself is not echoed (logs would leak it)."""
    if not names:
        return []
    folded = [_fold(n) for n in names]
    out = []

    def scan(where, obj, base):
        seen = set()
        for path, text in _strings(obj, base):
            t = _fold(text)
            for i, n in enumerate(folded):
                if contains_word(t, n) and (path, i) not in seen:
                    seen.add((path, i))
                    out.append(f"{where}: redact.txt entry #{i + 1} found in {path} (author names must not ship)")

    scan(code, {k: v for k, v in data.items() if k not in ("questions", "contexts")}, "")
    for cid, c in (data.get("contexts") or {}).items():
        scan(f"{code} ctx {cid}", c, "")
    for q in data.get("questions") or []:
        if isinstance(q, dict):
            scan(qid_of(q), q, "")
    return out


IMG_LINE = re.compile(r"^!\[([^\]\n]*)\]\((images/exams/[A-Za-z0-9._-]+\.png)\)[ \t]*$")
FENCE_OPEN = re.compile(r"^```([A-Za-z0-9+#_-]{0,12})[ \t]*$")
FENCE_CLOSE = re.compile(r"^```[ \t]*$")


def split_fences(s):
    """Yield (kind, payload): ('text', str) | ('fence', (lang, body)) | ('unclosed', str).
    A fence opens on a line that is exactly ``` or ```lang and closes on a line that is exactly ```."""
    s = str(s)
    if "```" not in s:
        yield "text", s
        return
    lines, buf, i = s.replace("\r\n", "\n").split("\n"), [], 0
    while i < len(lines):
        m = FENCE_OPEN.match(lines[i])
        if not m:
            buf.append(lines[i])
            i += 1
            continue
        j = i + 1
        while j < len(lines) and not FENCE_CLOSE.match(lines[j]):
            j += 1
        if buf:
            yield "text", "\n".join(buf)
            buf = []
        if j >= len(lines):
            yield "unclosed", "\n".join(lines[i:])
            return
        yield "fence", (m.group(1), "\n".join(lines[i + 1:j]))
        i = j + 1
    if buf:
        yield "text", "\n".join(buf)


def rich_problems(s, where):
    """Balanced $, no Hebrew inside math. Returns a list of problem strings."""
    out = []
    if "```" in str(s):
        keep = []
        for fk, fp in split_fences(s):
            if fk == "unclosed":
                out.append(f"{where}: unclosed ``` code fence (close it with a line that is exactly ```)")
            elif fk == "text":
                keep.append(fp)
        s = "\n".join(keep)
    if "![" in str(s):
        keep = []
        for ln in str(s).replace("\r\n", "\n").split("\n"):
            m = IMG_LINE.match(ln)
            if m:
                if not (ROOT / m.group(2)).is_file():
                    out.append(f"{where}: image file missing {m.group(2)}")
            elif ln.lstrip().startswith("!["):
                out.append(f"{where}: an inline figure must be a line of exactly ![alt](images/exams/<file>.png)")
            else:
                keep.append(ln)
        s = "\n".join(keep)
    s = str(s).replace("\\$", "")
    for part in TOKEN.split(s):
        if part.startswith("$$") and part.endswith("$$") and len(part) > 4:
            tex = part[2:-2]
        elif part.startswith("$") and part.endswith("$") and len(part) > 2:
            tex = part[1:-1]
        elif part.startswith("`"):
            continue
        else:
            if "$" in part:
                out.append(f"{where}: unbalanced $ (use \\$ for a literal dollar)")
            continue
        if HEB.search(tex):
            out.append(f"{where}: Hebrew inside math ${tex}$")
        if not tex.strip():
            out.append(f"{where}: empty math span")
    return out


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def nonblank(x):
    return isinstance(x, str) and bool(x.strip())


def unknown_keys(w, obj, allowed, P):
    """Unknown keys are errors (a misspelt stepsSource would otherwise silently skip the draft gate).
    Derived keys (*Html, html, DERIVED) get their own message elsewhere."""
    for k in sorted(k for k in obj if k not in allowed and k not in DERIVED
                    and not k.endswith("Html") and k != "html"):
        P(f"{w}: unknown key {k!r}")


def check_options(w, opts, P, root, rich=True):
    """Shared by mcq questions and choice/fillblank steps. Returns the option ids."""
    if not isinstance(opts, list) or len(opts) < 2:
        P(f"{w}: needs at least 2 options")
        return []
    ids = [o.get("id") for o in opts]
    if len(set(ids)) != len(ids):
        P(f"{w}: duplicate option ids {ids}")
    for o in opts:
        ow = f"{w} opt {o.get('id')}"
        unknown_keys(ow, o, OPTION_KEYS, P)
        if o.get("id") not in OPT_IDS:
            P(f"{ow}: option id must be one of a..h")
        t = o.get("type", "text")
        if t not in OPT_TYPES:
            P(f"{ow}: bad type {t}")
        v = str(o.get("value", ""))
        if not v.strip():
            P(f"{ow}: blank value")
        if "html" in o:
            P(f"{ow}: derived field html must not be in raw")
        if t == "math":
            if HEB.search(v):
                P(f"{ow}: Hebrew inside math option")
            if v.strip().startswith("$"):
                P(f"{ow}: math option value must be TeX without $")
        elif t == "image":
            if not (root / v).is_file():
                P(f"{ow}: image file missing {v}")
        elif rich:
            for x in rich_problems(v, ow):
                P(x)
    return ids


def check_step(w, s, P, root):
    if not isinstance(s, dict):
        P(f"{w}: step must be an object")
        return
    t = s.get("type")
    if t not in STEP_TYPES:
        P(f"{w}: step type {t!r} not in {list(STEP_TYPES)}")
        return
    unknown_keys(w, s, STEP_KEYS, P)
    for k in s:
        if k.endswith("Html"):
            P(f"{w}: derived field {k} must not be in raw")
    if not nonblank(s.get("prompt")):
        P(f"{w}: empty prompt")
    else:
        for x in rich_problems(s["prompt"], w + " prompt"):
            P(x)
    if s.get("explain"):
        for x in rich_problems(s["explain"], w + " explain"):
            P(x)
    if "code" in s and not isinstance(s["code"], bool):
        P(f"{w}: code must be true/false")
    code = s.get("code") is True

    def lines_ok():
        ln = s.get("lines")
        if not isinstance(ln, list) or len(ln) < 2 or not all(isinstance(x, str) and x.strip() for x in ln):
            P(f"{w}: lines must be a list of >= 2 non-blank strings")
            return None
        if not code:
            for i, x in enumerate(ln):
                for y in rich_problems(x, f"{w} line {i}"):
                    P(y)
        return ln

    if t == "choice":
        ids = check_options(w, s.get("options"), P, root)
        if s.get("correctId") not in ids:
            P(f"{w}: correctId {s.get('correctId')} not among option ids")
    elif t == "numeric":
        if not is_num(s.get("answer")):
            P(f"{w}: numeric answer must be a number")
        if "tol" in s and (not is_num(s["tol"]) or s["tol"] < 0):
            P(f"{w}: tol must be a number >= 0")
    elif t == "text":
        acc = s.get("accept")
        if not isinstance(acc, list) or not acc or not all(nonblank(a) for a in acc):
            P(f"{w}: accept must be a non-empty list of strings")
        if s.get("normalize", "none") not in NORMALIZE:
            P(f"{w}: normalize {s.get('normalize')!r} not in {sorted(NORMALIZE)}")
    elif t == "order":
        lines_ok()
    elif t == "findbug":
        ln = lines_ok()
        bi = s.get("bugIndex")
        if not is_int(bi):
            P(f"{w}: bugIndex must be an int")
        elif ln is not None and not (0 <= bi < len(ln)):
            P(f"{w}: bugIndex {bi} out of range 0..{len(ln) - 1}")
    elif t == "fillblank":
        ln = lines_ok()
        bi = s.get("blankIndex")
        if not is_int(bi):
            P(f"{w}: blankIndex must be an int")
        elif ln is not None:
            if not (0 <= bi < len(ln)):
                P(f"{w}: blankIndex {bi} out of range 0..{len(ln) - 1}")
            elif "___" not in ln[bi]:
                P(f"{w}: line blankIndex {bi} must contain the ___ placeholder")
        ids = check_options(w, s.get("options"), P, root, rich=not code)
        if s.get("correctId") not in ids:
            P(f"{w}: correctId {s.get('correctId')} not among option ids")


def check_question(code, q, ctxs, P, W, root):
    qid = question_id(code, q)
    kind = q.get("kind")
    unknown_keys(qid, q, QUESTION_KEYS, P)
    if not is_int(q.get("num")):
        P(f"{qid}: num must be an int")
    if q.get("part") not in (None, "") and part_suffix(q.get("part")) is None:
        P(f"{qid}: part {q.get('part')!r} is not a single letter (Hebrew or a-z)")
    if kind not in KINDS:
        P(f"{qid}: kind {kind!r} not in {list(KINDS)}")
    hold = q.get("hold")
    # a held question is left out of the bank: it needs no key/verdict/solution/source, only what identifies it
    for k in (() if hold else ("topic", "question", "official", "confidence")):
        if k not in q:
            P(f"{qid}: missing {k}")
    if q.get("topic") not in TOPICS and not (hold and "topic" not in q):
        P(f"{qid}: topic {q.get('topic')} not in closed list")
    if not nonblank(q.get("question")) and not hold:
        P(f"{qid}: empty question")
    if "official" in q and not isinstance(q["official"], bool):
        P(f"{qid}: official must be true/false")
    if "confidence" in q and q["confidence"] not in CONFIDENCE:
        P(f"{qid}: confidence must be high|med|low")
    for k in sorted(k for k in q if k in DERIVED or k.endswith("Html")):
        P(f"{qid}: derived field {k} must not be in raw")
    if "points" in q and (not is_num(q["points"]) or q["points"] < 0):
        P(f"{qid}: points must be a number >= 0")
    if q.get("contextId") and q["contextId"] not in ctxs:
        P(f"{qid}: contextId {q['contextId']} not defined in this file")
    if q.get("image") and not (root / q["image"]).is_file():
        P(f"{qid}: image file missing {q['image']}")
    if "hold" in q and not nonblank(hold):
        P(f"{qid}: hold must be a non-empty reason string")
    for k in ("question", "solution", "explanation"):
        if q.get(k):
            for x in rich_problems(q[k], f"{qid} {k}"):
                P(x)

    # ---- solution (mcq carries its key + explanation instead)
    has_sol = nonblank(q.get("solution"))
    if has_sol:
        if q.get("solutionSource") not in SOLUTION_SOURCES:
            P(f"{qid}: solutionSource {q.get('solutionSource')!r} not in {sorted(SOLUTION_SOURCES)}")
    elif not hold and kind != "mcq":
        P(f"{qid}: missing solution (a question without one must carry a hold reason)")
    if not has_sol and kind != "mcq":
        if q.get("steps"):
            P(f"{qid}: steps without a solution")
        if q.get("rubric"):
            P(f"{qid}: rubric without a solution")

    # ---- mcq options / key; forbidden elsewhere
    if kind == "mcq":
        held_bare = bool(hold) and not q.get("options")
        ids = [] if held_bare else check_options(qid, q.get("options"), P, root)
        if q.get("correctId") not in ids and not (hold and "correctId" not in q):
            P(f"{qid}: correctId {q.get('correctId')} not among option ids")
        acc = q.get("acceptedIds")
        if acc is not None:
            if not isinstance(acc, list) or len(acc) < 2:
                P(f"{qid}: acceptedIds only when >1 accepted (non-empty list of >=2)")
            else:
                if any(a not in ids for a in acc):
                    P(f"{qid}: acceptedIds {acc} contains an unknown option id")
                if acc[0] != q.get("correctId") and not (hold and "correctId" not in q):
                    P(f"{qid}: acceptedIds must start with correctId")
                if len(set(acc)) != len(acc):
                    P(f"{qid}: duplicate acceptedIds")
        if "lockOrder" in q and not isinstance(q["lockOrder"], bool):
            P(f"{qid}: lockOrder must be a boolean")
    else:
        for k in ("options", "correctId", "acceptedIds", "lockOrder"):
            if k in q:
                P(f"{qid}: {k} is only for kind mcq")
    if kind == "truefalse":
        if not isinstance(q.get("verdict"), bool) and not (hold and "verdict" not in q):
            P(f"{qid}: truefalse needs verdict true/false")
    elif "verdict" in q:
        P(f"{qid}: verdict is only for kind truefalse")

    # ---- rubric
    rub = q.get("rubric")
    if rub is not None:
        if not isinstance(rub, list) or not rub:
            P(f"{qid}: rubric must be a non-empty list")
        else:
            tot = 0
            for i, r in enumerate(rub):
                rw = f"{qid} rubric[{i}]"
                if not isinstance(r, dict) or not nonblank(r.get("text")):
                    P(f"{rw}: needs text")
                    continue
                if not is_num(r.get("points")) or r["points"] <= 0:
                    P(f"{rw}: points must be a number > 0")
                else:
                    tot += r["points"]
                unknown_keys(rw, r, RUBRIC_KEYS, P)
                if "html" in r:
                    P(f"{rw}: derived field html must not be in raw")
                for x in rich_problems(r["text"], rw):
                    P(x)
            if is_num(q.get("points")) and tot != q["points"]:
                W(f"{qid}: rubric points sum {tot} != points {q['points']}")
        if q.get("rubricSource") not in RUBRIC_SOURCES:
            P(f"{qid}: rubricSource {q.get('rubricSource')!r} not in {sorted(RUBRIC_SOURCES)}")
    elif kind != "mcq" and not hold:
        W(f"{qid}: no rubric yet")
    # ---- pitfalls
    pf = q.get("pitfalls")
    if pf is not None:
        if not isinstance(pf, list) or not all(nonblank(x) for x in pf):
            P(f"{qid}: pitfalls must be a list of non-blank strings")
        else:
            for i, x in enumerate(pf):
                for y in rich_problems(x, f"{qid} pitfalls[{i}]"):
                    P(y)
    # ---- steps
    steps = q.get("steps")
    if steps is not None:
        if not isinstance(steps, list) or not steps:
            P(f"{qid}: steps must be a non-empty list")
        else:
            for i, s in enumerate(steps):
                check_step(f"{qid} step[{i}]", s, P, root)
        if q.get("stepsSource") not in STEPS_SOURCES:
            P(f"{qid}: stepsSource {q.get('stepsSource')!r} not in {sorted(STEPS_SOURCES)}")
    elif kind != "mcq" and not hold:
        W(f"{qid}: no steps yet")
    if q.get("confidence") == "low":
        W(f"{qid}: confidence low")


BIDI_FACT = re.compile(r"(?<![A-Za-z0-9_])(?:[0-9]+|[A-Za-z])!(?!=)")
BIDI_CHAIN = re.compile(r"(?<![A-Za-z0-9_])[0-9A-Za-z()]+(?:\s*[·×]\s*[0-9A-Za-z()]+!?)+")


def bidi_lint(data, code):
    """Warnings (never problems) for digit+"!" (a factorial) or a product chain (a middle dot or x between digits)
    written OUTSIDE $...$ in raw text. The open renderer (Bidi in normalize.js) isolates both correctly, but math mode
    ($4!$ or a LaTeX cdot product) is the intended form and always renders right. Message prefix: "bidi:"."""
    out = []
    for path, text in _strings(data, ""):
        if not isinstance(text, str) or not (re.search(r"[0-9A-Za-z]!", text) or re.search(r"[·×]", text)):
            continue
        for fk, fp in split_fences(text):
            if fk != "text":
                continue
            for part in TOKEN.split(fp):
                if part.startswith("$") or part.startswith("`"):
                    continue
                part = "\n".join(ln for ln in part.split("\n") if not IMG_LINE.match(ln))
                hits = [m.group(0).strip() for m in BIDI_FACT.finditer(part)] + [m.group(0).strip() for m in BIDI_CHAIN.finditer(part)]
                for h in hits[:3]:
                    out.append(f"bidi: {code} {path}: '{h}' outside $...$ (wrap it in math mode)")
    return out


def check_file(fp):
    """Returns (problems, warnings, n_questions, by_topic Counter)."""
    problems, warns = [], []
    P, W = problems.append, warns.append
    try:
        data = json.loads(fp.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"{fp.name}: JSON parse error: {str(e).encode('ascii', 'backslashreplace').decode()}"], [], 0, collections.Counter()
    unknown_keys(fp.name, data, EXAM_KEYS, P)
    code = data.get("examCode")
    if not code:
        P(f"{fp.name}: missing examCode")
        code = fp.stem
    elif not CODE_RE.match(code):
        W(f"{fp.name}: examCode {code} not YY[A|B|S]-[A..H] or SAMP-N")
    if code != fp.stem:
        P(f"{fp.name}: examCode {code} != file name")
    for k in ("examLabel", "year"):
        if data.get(k) in (None, ""):
            P(f"{code}: missing {k}")
    ctxs = data.get("contexts") or {}
    for cid, c in ctxs.items():
        w = f"{code} ctx {cid}"
        unknown_keys(w, c, CONTEXT_KEYS, P)
        if c.get("kind") not in CONTEXT_KINDS:
            P(f"{w}: kind must be image|text|code")
        if c.get("kind") == "image":
            if not c.get("image"):
                P(f"{w}: image context without image")
            elif not (ROOT / c["image"]).is_file():
                P(f"{w}: image file missing {c['image']}")
        if c.get("kind") == "text" and not nonblank(c.get("text")):
            P(f"{w}: text context without text")
        if c.get("kind") == "code" and not nonblank(c.get("code")):
            P(f"{w}: code context without code")
        for k in ("text", "caption", "title"):
            if c.get(k):
                for x in rich_problems(c[k], f"{w} {k}"):
                    P(x)
    problems += redact_problems(data, code, lambda q: question_id(code, q), load_redact())
    warns += bidi_lint(data, code)
    qs = data.get("questions")
    if not isinstance(qs, list) or not qs:
        P(f"{code}: no questions")
        qs = []
    seen, by_topic = set(), collections.Counter()
    for q in qs:
        qid = question_id(code, q)
        if qid in seen:
            P(f"{qid}: duplicate question id (num + part)")
        seen.add(qid)
        check_question(code, q, ctxs, P, W, ROOT)
        if q.get("topic") in TOPICS:
            by_topic[q["topic"]] += 1
    return problems, warns, len(qs), by_topic


def main():
    args = sys.argv[1:]
    if args:
        files = []
        for a in args:
            p = pathlib.Path(a)
            files.append(p if p.suffix == ".json" else RAW / f"{a}.json")
    else:
        files = [p for p in sorted(RAW.glob("*.json")) if EXAM_RE.match(p.name)]
    total, all_p, all_w, topics = 0, [], [], collections.Counter()
    for fp in files:
        if not fp.is_file():
            all_p.append(f"{fp}: not found")
            continue
        p, w, n, bt = check_file(fp)
        total += n
        topics.update(bt)
        all_p += p
        all_w += w
        print(f"{fp.stem}: {n} questions, {len(p)} problems")
    print(f"\nTOTAL: {total} questions across {len(files)} files")
    print("by topic:", dict(topics))
    print("bidi lint hits (factorial / product chain outside $..$):", sum(1 for x in all_w if x.startswith("bidi:")))
    if all_w:
        print(f"\nWARNINGS ({len(all_w)}):")
        for x in all_w:
            print("  -", x.encode("ascii", "backslashreplace").decode())
    # string-escape corruption (e.g. "\notin" in a non-raw generator string -> newline + "otin")
    import subprocess
    lint = subprocess.run([sys.executable, str(TOOLS / "gen" / "lint_escapes.py")],
                          capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT))
    if lint.returncode:
        all_p += ["escape-lint: " + l for l in lint.stdout.splitlines() if not l.startswith("escape problems")]
    print(f"\nPROBLEMS ({len(all_p)}):")
    for x in all_p:
        print("  -", x.encode("ascii", "backslashreplace").decode())
    sys.exit(1 if all_p else 0)


if __name__ == "__main__":
    main()
