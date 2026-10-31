# -*- coding: utf-8 -*-
"""KMP / prefix-function widgets for the kmp_prefix videos (K01..K08), plus the solvers the scripts assert with.

Stage widget (SVG, no TeX inside; every class is prefixed kp- so other courses are untouched):
  Strip(pfx, n, rows)   aligned rows of cells over the columns 1..n (course indices, 1-based), with an optional index
      header. A row is row(key, label, cells={col: text}, shown=True|False|{cols}, slot=None, hidden=False):
      rows that share a `slot` are drawn on the same line (a pattern under the text at several shifts); a row with
      hidden=True starts invisible as a whole (group id {pfx}-row-<key>).
      Ids, for a cell of row `key` at column c:
        {pfx}-v-<key>-<c>    the value (hidden unless shown)
        {pfx}-cur-<key>-<c>  teal frame            {pfx}-cmp-<key>-<c>  blue fill (being compared)
        {pfx}-ok-<key>-<c>   green fill (equal)     {pfx}-bad-<key>-<c>  red fill (different)
      S.bracket(key, a, b, kind) registers a bracket over cells a..b: kind "pre" above the row (teal), "suf" below
      the row (amber); S.arc(key, a, b) registers a fallback arrow under the row from column a to column b.
      Register brackets/arcs while building the phrases, then call S.html().
      S.mark(*ids) is the transient highlight: hides the previous marks not in ids, shows ids; S.clear() hides them.

Solvers (each checked against an independent brute force and against the course checker's kmp_ref):
  pi_brute(P) / prefix_trace(P) / borders(s) / chain(pi, q) / kmp_trace(T, P) / occ_naive(T, P)
"""
import html as _html
import itertools
import math

from vid import show, hide
from kmp_prefix import kmp_ref as REF          # tools/verify/needhelp/kmp_prefix/kmp_ref.py (SIM_PATHS)


def esc(s):
    return _html.escape(str(s), quote=True)


# ====================================================================== solvers
def borders(s):
    """lengths of all proper borders of s, longest first, 0 included (straight from the definition)"""
    return [k for k in range(len(s) - 1, -1, -1) if s[:k] == s[len(s) - k:]]


def pi_brute(P):
    """[None, pi[1], ..., pi[m]] by the definition: the longest proper border of P[1..q]"""
    return [None] + [borders(P[:q])[0] for q in range(1, len(P) + 1)]


def prefix_trace(P):
    """Compute-Prefix literally. Returns (pi, steps) with steps[q] = [(k, equal?), ...]: every comparison of
    P[k+1] with P[q] made while computing pi[q] (q = 2..m), in order. pi is checked against the definition."""
    m = len(P)
    pi = [None, 0] + [None] * (m - 1)
    steps = {}
    k = 0
    for q in range(2, m + 1):
        st = []
        while True:
            eq = P[k] == P[q - 1]               # P[k+1] vs P[q] (1-based)
            st.append((k, eq))
            if eq:
                k += 1
                break
            if k == 0:
                break
            k = pi[k]
        pi[q] = k
        steps[q] = st
    assert pi == pi_brute(P) == REF.pi_of(P), P
    return pi, steps


def chain(pi, q):
    """pi[q], pi[pi[q]], ... down to and excluding 0"""
    out, k = [], pi[q]
    while k > 0:
        out.append(k)
        k = pi[k]
    assert out == REF.chain(pi, q)
    return out


def kmp_trace(T, P):
    """the CLRS match loop. Returns a list, one entry per text letter i (1-based):
    dict(i, q0 = state before, comps = [(j, equal?)] comparisons T[i] vs P[j], q = state after the letter (before the
    reset), match = q == m, q1 = state carried to the next letter). Checked against kmp_ref.run_kmp and a naive search."""
    pi = pi_brute(P)
    m, q, out = len(P), 0, []
    for i, c in enumerate(T, 1):
        q0, comps = q, []
        while True:
            eq = P[q] == c
            comps.append((q + 1, eq))
            if eq:
                q += 1
                break
            if q == 0:
                break
            q = pi[q]
        match = q == m
        e = dict(i=i, q0=q0, comps=comps, q=q, match=match, q1=pi[m] if match else q)
        out.append(e)
        q = e["q1"]
    r = REF.run_kmp(T, P)
    assert [len(e["comps"]) for e in out] == r["comps"] and [e["q1"] for e in out] == r["states"]
    assert [e["i"] for e in out if e["match"]] == r["ends"]
    assert [e["i"] - m + 1 for e in out if e["match"]] == occ_naive(T, P)
    return out


def occ_naive(T, P):
    """1-based starts of all (overlapping) occurrences"""
    return [i + 1 for i in range(len(T) - len(P) + 1) if T[i:i + len(P)] == P]


def feasible(table, alpha="abcdefgh"):
    """some string over an unbounded alphabet with this pi table (restricted-growth strings), or None"""
    n = len(table)
    for s in REF.rgs(n):
        if pi_brute(s)[1:] == list(table):
            return s
    return None


def all_strings(n, alpha):
    return ("".join(t) for t in itertools.product(alpha, repeat=n))


# ====================================================================== speech
LETTER_SAY = {"A": "אֵיי", "B": "בִּי", "C": "סִי", "D": "דִּי", "a": "אֵיי", "b": "בִּי", "c": "סִי", "d": "דִּי",
              "#": "סולמית"}
NUM_SAY = {0: "אפס", 1: "אחת", 2: "שתיים", 3: "שלוש", 4: "ארבע", 5: "חמש", 6: "שש", 7: "שבע", 8: "שמונה", 9: "תשע",
           10: "עשר", 11: "אחת עשרה", 12: "שתים עשרה", 13: "שלוש עשרה", 14: "ארבע עשרה"}


def spell(s):
    """'ABBA' -> 'אֵיי בִּי בִּי אֵיי' (letter by letter, for say=)"""
    return " ".join(LETTER_SAY[c] for c in s)


def num(k):
    return NUM_SAY[k]


def nums(seq):
    return ", ".join(NUM_SAY[k] for k in seq)


def C(s):
    """a string in monospace inside Hebrew text (cards, panel)"""
    return f'<code class="kp-c">{esc(s)}</code>'


def cmp_line(a, b, mark=True):
    """'<code>ABB</code> ≠ <code>BBA</code> ✗' (prefix vs suffix of one length)"""
    eq = a == b
    sym = "=" if eq else "≠"
    tail = (' <span class="kp-yes">✓</span>' if eq else ' <span class="kp-no">✗</span>') if mark else ""
    return f'<code>{esc(a)}</code> {sym} <code>{esc(b)}</code>{tail}'


# ====================================================================== stage widget
def row(key, label, cells, shown=True, slot=None, hidden=False):
    return dict(key=key, label=label, cells=dict(cells), shown=shown, slot=slot or key, hidden=hidden)


def cells_of(s, start=1):
    """'ABA' -> {1: 'A', 2: 'B', 3: 'A'}"""
    return {start + k: ch for k, ch in enumerate(s)}


class Strip:
    def __init__(self, pfx, n, rows, cw=70, ch=62, hw=80, gap=30, fs=36, idx=True, below=0, scale=1.0, idx_label="", idx_n=None):
        self.pfx, self.n, self.rows, self.idx_n = pfx, n, rows, idx_n
        self.cw, self.ch, self.hw, self.gap, self.fs, self.idx = cw, ch, hw, gap, fs, idx
        self.below, self.scale, self.idx_label = below, scale, idx_label
        self.slots = list(dict.fromkeys(r["slot"] for r in rows))
        self.hh = 40 if idx else 0
        self.brackets, self.arcs, self.on = [], [], []

    # geometry
    def x(self, c):
        return self.hw + (c - 1) * self.cw

    def y(self, key):
        r = next(r for r in self.rows if r["key"] == key)
        return self.hh + self.gap + self.slots.index(r["slot"]) * (self.ch + self.gap)

    def size(self):
        return self.hw + self.n * self.cw, self.hh + self.gap + len(self.slots) * (self.ch + self.gap) + self.below

    # ids + timeline helpers
    def c(self, kind, key, col):
        return f"{self.pfx}-{kind}-{key}-{col}"

    def v(self, key, col):
        return self.c("v", key, col)

    def vals(self, key, cols):
        return show(*[self.v(key, c) for c in cols])

    def bracket(self, key, a, b, kind):
        if (key, a, b, kind) not in self.brackets:
            self.brackets.append((key, a, b, kind))
        return f"{self.pfx}-br-{kind}-{key}-{a}-{b}"

    def arc(self, key, a, b):
        if (key, a, b) not in self.arcs:
            self.arcs.append((key, a, b))
        return f"{self.pfx}-ar-{key}-{a}-{b}"

    def mark(self, *ids):
        ids = list(ids)
        do = hide(*[i for i in self.on if i not in ids]) + show(*ids)
        self.on = ids
        return do

    def clear(self):
        do = hide(*self.on)
        self.on = []
        return do

    # drawing
    def html(self):
        W, H = self.size()
        p = self.pfx
        o = [f'<svg class="kp-strip" id="{p}" viewBox="-6 -6 {W + 12} {H + 12}" width="{(W + 12) * self.scale:.0f}" '
             f'height="{(H + 12) * self.scale:.0f}" direction="ltr" style="--kp-fs:{self.fs}px">',
             f'<defs><marker id="{p}-ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" '
             f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="kp-ahead"/></marker></defs>']
        if self.idx:
            if self.idx_label:
                o.append(f'<text x="{self.hw / 2}" y="{self.hh / 2 + 4}" class="kp-idxl">{esc(self.idx_label)}</text>')
            for c in range(1, (self.idx_n or self.n) + 1):
                o.append(f'<text x="{self.x(c) + self.cw / 2}" y="{self.hh / 2 + 4}" class="kp-idx">{c}</text>')
        for r in self.rows:
            k, y = r["key"], self.y(r["key"])
            g = [f'<g id="{p}-row-{k}" class="{"h" if r["hidden"] else ""}">',
                 f'<text x="{self.hw / 2}" y="{y + self.ch / 2}" class="kp-label">{esc(r["label"])}</text>']
            for col in sorted(r["cells"]):
                x = self.x(col)
                g.append(f'<rect x="{x}" y="{y}" width="{self.cw}" height="{self.ch}" class="kp-cell"/>')
                for kind in ("cmp", "ok", "bad"):
                    g.append(f'<rect id="{self.c(kind, k, col)}" x="{x + 3}" y="{y + 3}" width="{self.cw - 6}" '
                             f'height="{self.ch - 6}" rx="7" class="kp-{kind} h"/>')
                g.append(f'<rect id="{self.c("cur", k, col)}" x="{x + 2}" y="{y + 2}" width="{self.cw - 4}" '
                         f'height="{self.ch - 4}" rx="8" class="kp-cur h"/>')
                sh = r["shown"] is True or (r["shown"] not in (True, False) and col in r["shown"])
                g.append(f'<text id="{self.v(k, col)}" x="{x + self.cw / 2}" y="{y + self.ch / 2}" '
                         f'class="kp-val{"" if sh else " h"}">{esc(r["cells"][col])}</text>')
            g.append("</g>")
            o += g
        for key, a, b, kind in self.brackets:
            y = self.y(key)
            x1, x2 = self.x(a) + 5, self.x(b) + self.cw - 5
            if kind == "pre":
                yy, t = y - self.gap / 2 + 2, 9
            else:
                yy, t = y + self.ch + self.gap / 2 - 2, -9
            o.append(f'<path id="{p}-br-{kind}-{key}-{a}-{b}" d="M{x1},{yy + t} L{x1},{yy} L{x2},{yy} L{x2},{yy + t}" '
                     f'class="kp-br {kind} h"/>')
        for key, a, b in self.arcs:
            y = self.y(key) + self.ch + 4
            xa, xb = self.x(a) + self.cw / 2, self.x(b) + self.cw / 2
            depth = 26 + 13 * abs(a - b)
            o.append(f'<path id="{p}-ar-{key}-{a}-{b}" d="M{xa},{y} Q{(xa + xb) / 2},{y + depth} {xb + (6 if xb < xa else -6)},{y + 2}" '
                     f'class="kp-arc h" marker-end="url(#{p}-ah)"/>')
        o.append("</svg>")
        return "".join(o)


def pi_strip(pfx, P, shown_pi=(), shown_p=True, **kw):
    """the standard q / P / π strip of a pattern; π values hidden unless in shown_pi"""
    pi = pi_brute(P.replace("?", "#"))
    m = len(P)
    rows = [row("P", "P", cells_of(P), shown=shown_p if shown_p is True else set(shown_p)),
            row("pi", "π", {q: str(pi[q]) for q in range(1, m + 1)}, shown=set(shown_pi))]
    kw.setdefault("idx_label", "q")
    return Strip(pfx, m, rows, **kw)


def matcher(pfx, T, P, shifts, qrow="q1", **kw):
    """text T on top, the pattern under it at every shift in `shifts` (one visible at a time: row P<s>), and the state
    q after each letter (hidden values; qrow="q" shows m at a match instead of the state carried on). Comparisons of T[i] with P[j] mark cells (T, i) and (P<i-j>, i)."""
    tr = kmp_trace(T, P)
    m = len(P)
    rows = [row("T", "T", cells_of(T))]
    for s in shifts:
        rows.append(row(f"P{s}", "P", {s + j: P[j - 1] for j in range(1, m + 1) if s + j >= 1}, slot="P", hidden=True))
    rows.append(row("q", "q", {e["i"]: str(e[qrow]) for e in tr}, shown=False))
    kw.setdefault("idx_label", "i")
    n = max([len(T)] + [s + m for s in shifts])
    kw.setdefault("idx_n", len(T))
    return Strip(pfx, n, rows, **kw), tr


def needed_shifts(tr):
    return sorted({e["i"] - j for e in tr for j, _ in e["comps"]})


def compare_do(S, i, j, eq):
    """mark the comparison of T[i] with P[j] (pattern drawn at shift i - j)"""
    s = i - j
    return S.mark(S.c("cmp", "T", i), S.c("ok" if eq else "bad", f"P{s}", i))


def shift_do(S, s, prev=None):
    """show the pattern row at shift s (hiding the previous one)"""
    do = []
    if prev is not None and prev != s:
        do += hide(f"{S.pfx}-row-P{prev}")
    return do + show(f"{S.pfx}-row-P{s}")


class Lines:
    """one status line at a time in a fixed slot (each new line replaces the previous): ids {pfx}-<k>"""
    def __init__(self, pfx, height=64, size=34):
        self.pfx, self.height, self.size, self.items, self.cur = pfx, height, size, [], None

    def say(self, html_):
        k = len(self.items)
        self.items.append(html_)
        do = (hide(f"{self.pfx}-{self.cur}") if self.cur is not None else []) + show(f"{self.pfx}-{k}")
        self.cur = k
        return do

    def off(self):
        do = hide(f"{self.pfx}-{self.cur}") if self.cur is not None else []
        self.cur = None
        return do

    def html(self):
        rows = "".join(f'<div id="{self.pfx}-{k}" class="h"><span class="kp-line" style="font-size:{self.size}px">{t}</span></div>'
                       for k, t in enumerate(self.items))
        return f'<div class="swap kp-swap" style="--swap-h:{self.height}px">{rows}</div>'


def eqs(pfx, lines, size=36, hidden=True):
    """a column of display lines ($TeX$ / text inside), ids {pfx}-0 …"""
    h = " h" if hidden else ""
    rows = "".join(f'<div id="{pfx}-{k}" class="kp-eq{h}">{ln}</div>' for k, ln in enumerate(lines))
    return f'<div class="kp-eqs" style="font-size:{size}px">{rows}</div>'


def code(pfx, lines, hidden=False, size=27):
    """pseudo code, line ids {pfx}-hl-<k> (highlight behind line k)"""
    h = " h" if hidden else ""
    rows = "".join(f'<div class="kp-cl"><i id="{pfx}-hl-{k}" class="kp-clhl h"></i><span>{esc(t)}</span></div>'
                   for k, t in enumerate(lines))
    return f'<div id="{pfx}" class="kp-code{h}" dir="ltr" style="font-size:{size}px">{rows}</div>'
