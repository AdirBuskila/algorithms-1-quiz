# -*- coding: utf-8 -*-
"""Rich text -> HTML / MathML helpers for the open engine (copied from the mcq template's
build_questions.py so the template stands alone; keep the two in step by hand).

Rich text: $..$ / $$..$$ TeX (rendered to MathML via render_math.js in one batch), `code`,
**bold**, newline -> <br>. Plus question ids (<CODE>-Q<num><part>) and plain-text escaping
for code lines.
"""
import html, json, pathlib, re, subprocess, sys

TOOLS = pathlib.Path(__file__).resolve().parent
HEB = re.compile(r"[֐-׿]")

# Hebrew part letters (sub-question markers) -> stable ASCII suffix, by alphabet position,
# final forms folded onto the regular letter. ASCII a-z is accepted as-is.
PART_MAP = dict(zip("אבגדהוזחטיכלמנסעפצקרשת", "abcdefghijklmnopqrstuv"))
PART_MAP.update({"ך": "k", "ם": "m", "ן": "n", "ף": "q", "ץ": "r"})


def part_suffix(part):
    """'ב' -> 'b', 'b' -> 'b', None/'' -> ''. Returns None for an unmappable part."""
    if part in (None, ""):
        return ""
    p = str(part).strip().rstrip("'׳.)")
    if len(p) == 1:
        if p in PART_MAP:
            return PART_MAP[p]
        if p.isascii() and p.isalpha():
            return p.lower()
    return None


def question_id(code, q):
    """DEMO-A-Q3 / DEMO-A-Q3b. Falls back to a '?' marker so messages still name the item."""
    s = part_suffix(q.get("part"))
    return f"{code}-Q{q.get('num')}{'?' if s is None else s}"


def code_html(s):
    """A literal code line: escaped only (no math / bold / backtick parsing)."""
    return html.escape(str(s), quote=False)


# ---------------------------------------------------------------- rich text
ESC_DOLLAR = "\x00"
TOKEN = re.compile(r"(\$\$.+?\$\$|\$[^$]+?\$|`[^`]+`)", re.S)


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


IMG_LINE = re.compile(r"^!\[([^\]\n]*)\]\((images/exams/[A-Za-z0-9._-]+\.png)\)[ \t]*$")


def split_images(s):
    """Yield ('text', str) | ('image', (alt, src)). An image is a line consisting only of
    ![alt text](images/exams/<file>.png)."""
    s = str(s)
    if "![" not in s:
        yield "text", s
        return
    buf = []
    for ln in s.replace("\r\n", "\n").split("\n"):
        m = IMG_LINE.match(ln)
        if not m:
            buf.append(ln)
            continue
        if buf:
            yield "text", "\n".join(buf)
            buf = []
        yield "image", (m.group(1), m.group(2))
    if buf:
        yield "text", "\n".join(buf)


def figure_html(alt, src):
    a = html.escape(alt, quote=True)
    return (f'<figure class="rt-fig"><img src="{html.escape(src, quote=True)}" alt="{a}" loading="lazy">'
            f'<figcaption>{html.escape(alt, quote=False)}</figcaption></figure>')


def split_rich(s):
    """Yield (kind, payload) for kind in text|imath|dmath|code|fence|image|unclosed. Literal \\$ -> '$'.
    Fenced blocks (a line of ```lang ... a line of ```) are literal: payload (lang, body)."""
    for fk, fp in split_fences(s):
        if fk != "text":
            yield fk, fp
            continue
        for ik, ip in split_images(fp):
            if ik == "image":
                yield "image", ip
            else:
                yield from _split_inline(ip)


def _split_inline(s):
    s = str(s).replace("\\$", ESC_DOLLAR)
    for part in TOKEN.split(s):
        if not part:
            continue
        if part.startswith("$$") and part.endswith("$$") and len(part) > 4:
            yield "dmath", part[2:-2].replace(ESC_DOLLAR, "\\$").strip()
        elif part.startswith("$") and part.endswith("$") and len(part) > 2:
            yield "imath", part[1:-1].replace(ESC_DOLLAR, "\\$").strip()
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            yield "code", part[1:-1].replace(ESC_DOLLAR, "$")
        else:
            yield "text", part.replace(ESC_DOLLAR, "$")


def math_spans(s):
    return [(p, k == "dmath") for k, p in split_rich(s) if k in ("imath", "dmath")]


class MathBank:
    """Collects (tex, display) pairs; renders them all in one node call."""

    def __init__(self):
        self.items, self.index, self.where = [], {}, []

    def add(self, tex, display, where):
        key = (tex, bool(display))
        if key not in self.index:
            self.index[key] = len(self.items)
            self.items.append({"tex": tex, "display": bool(display)})
            self.where.append(where)
        return self.index[key]

    def render(self):
        if not self.items:
            self.html = []
            return []
        proc = subprocess.run(["node", str(TOOLS / "render_math.js")],
                              input=json.dumps({"items": self.items}, ensure_ascii=False),
                              capture_output=True, text=True, encoding="utf-8", cwd=str(TOOLS))
        if proc.returncode != 0:
            sys.stdout.write("render_math.js failed:\n" +
                             proc.stderr.encode("ascii", "backslashreplace").decode() + "\n")
            sys.exit(2)
        res = json.loads(proc.stdout)
        self.html = [fix_overlines(h) if h else h for h in res["html"]]
        return [(self.where[e["i"]], e["tex"], e["err"]) for e in res["errors"]]


OVL_OPEN = '<mover accent="true">'
OVL_TAIL = '<mo stretchy="true">‾</mo></mover>'


def fix_overlines(m):
    r"""Chrome's MathML Core does not stretch KaTeX's \overline (<mover> + stretchy U+203E):
    it draws a short bar at the base's corner. Rewrite each one to <mrow class="ovl">BASE</mrow>;
    styles.css draws the bar as a border-top spanning the whole base. Innermost first."""
    starts, i = [], m.find(OVL_OPEN)
    while i != -1:
        starts.append(i)
        i = m.find(OVL_OPEN, i + 1)
    for st in reversed(starts):
        depth, j = 0, st
        while True:
            o, c = m.find("<mover", j), m.find("</mover>", j)
            if c == -1:
                return m
            if o != -1 and o < c:
                depth, j = depth + 1, o + 6
            else:
                depth, j = depth - 1, c + 8
                if depth == 0:
                    break
        seg = m[st:j]
        if seg.endswith(OVL_TAIL):
            base = seg[len(OVL_OPEN):-len(OVL_TAIL)]
            m = m[:st] + '<mrow class="ovl">' + base + "</mrow>" + m[j:]
    return m


def unescape_quotes(x):
    """Generators use Python raw strings, so a Hebrew gershayim written as \\" (מ\\"ט) arrives
    with its backslash. TeX here never uses \\" (umlaut), so strip it everywhere."""
    if isinstance(x, str):
        return x.replace('\\"', '"')
    if isinstance(x, list):
        return [unescape_quotes(v) for v in x]
    if isinstance(x, dict):
        return {k: unescape_quotes(v) for k, v in x.items()}
    return x


def rich_html(s, bank, where, math_errors):
    """Rich text -> HTML with MATH placeholders (@@M<n>@@) resolved later."""
    out, fences = [], []
    for kind, p in split_rich(s):
        if kind in ("imath", "dmath"):
            if HEB.search(p):
                math_errors.append((where, p, "Hebrew inside math span"))
                continue
            i = bank.add(p, kind == "dmath", where)
            out.append(f"@@{'D' if kind == 'dmath' else 'M'}{i}@@")
        elif kind == "code":
            out.append(f'<code class="tok" dir="ltr">{html.escape(p, quote=False)}</code>')
        elif kind == "fence":
            lang, body = p
            la = f' data-lang="{html.escape(lang, quote=True)}"' if lang else ""
            fences.append(f'<pre class="code-block" dir="ltr"{la}><code>{html.escape(body, quote=False)}</code></pre>')
            out.append(f"\x01F{len(fences) - 1}\x01")
        elif kind == "image":
            alt, src = p
            if not (TOOLS.parent / src).is_file():
                math_errors.append((where, src, "image file missing"))
                continue
            fences.append(figure_html(alt, src))
            out.append(f"\x01F{len(fences) - 1}\x01")
        elif kind == "unclosed":
            math_errors.append((where, p[:40], "unclosed ``` code fence"))
        else:
            t = html.escape(p, quote=False)
            t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t, flags=re.S)
            out.append(t)
    h = "".join(out)
    # bold may wrap math/code placeholders too: re-run across the joined string
    h = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", h, flags=re.S)
    h = h.replace("\r\n", "\n").replace("\n", "<br>")
    return re.sub(r"\x01F(\d+)\x01", lambda m: fences[int(m.group(1))], h)


def resolve(h, bank):
    def sub(m):
        kind, i = m.group(1), int(m.group(2))
        mm = bank.html[i]
        cls = "math-block" if kind == "D" else "math-inline"
        return f'<span class="{cls}">{mm}</span>'
    return re.sub(r"@@([MD])(\d+)@@", sub, h)
