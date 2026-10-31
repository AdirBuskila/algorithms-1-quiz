# -*- coding: utf-8 -*-
"""Widgets for the greedy_proofs videos (G01-G08): interval timelines, chip rows, item tables, tape rows and Huffman
trees, all computed in Python. Every widget is an HTML/SVG fragment with stable ids that the timeline shows/hides
(class `h` = starts invisible). Class names are prefixed gp- so they never clash with other courses' widgets.

The course checker (tools/verify/needhelp/greedy_proofs/check.py) is loaded as CHK, so the scripts can compare
their own greedy runs with the checker's brute force (coins_opt, iv_opt, knap01_opt, huffman_cost, ...).
"""
import heapq
import html as _html
import importlib.util
import itertools
import pathlib

_ROOT = pathlib.Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "gp_check", _ROOT / "tools" / "verify" / "needhelp" / "greedy_proofs" / "check.py")
CHK = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CHK)


def esc(s):
    return _html.escape(str(s), quote=True)


def num(x):
    """3.0 -> '3', -6.5 -> '-6.5' (the minus as a real minus sign for SVG text)"""
    s = f"{x:g}"
    return s.replace("-", "−")


# ---------------------------------------------------------------- solvers shared by the scripts
def conflict(a, b):
    """closed intervals that share a point (touching = conflict)"""
    return not (a[1] < b[0] or b[1] < a[0])


def iv_greedy_run(ivs, key):
    """the generic interval greedy: pick the best by key, drop everything that conflicts with it, repeat.
    Returns [(picked index, [indices dropped with it])]."""
    left = list(range(len(ivs)))
    steps = []
    while left:
        left.sort(key=lambda i: key(ivs[i]))
        g = left[0]
        drop = sorted(i for i in left[1:] if conflict(ivs[i], ivs[g]))
        steps.append((g, drop))
        left = [i for i in left[1:] if i not in drop]
    return steps


def iv_all_optima(ivs):
    """every maximum set of pairwise disjoint intervals (index tuples), brute force"""
    best, res = 0, []
    for r in range(len(ivs), 0, -1):
        for sub in itertools.combinations(range(len(ivs)), r):
            if all(not conflict(ivs[a], ivs[b]) for a, b in itertools.combinations(sub, 2)):
                res.append(sub)
        if res:
            return res
    return [()]


def huffman_run(items, prefer=None):
    """items: [(name, weight)]. Merge the two lightest nodes n-1 times. Ties are broken by `prefer` (a list of node
    names to take first among equal weights) and then by creation order. Returns (nodes, merges):
    nodes[name] = (weight, left, right) (left/right None for a leaf); merges = [(left, right, new name, weight)].
    The lighter node goes left (equal weights: the one picked first)."""
    prefer = list(prefer or [])
    nodes = {n: (w, None, None) for n, w in items}
    pool = [(w, n) for n, w in items]
    merges = []
    k = 0
    while len(pool) > 1:
        order = {p[1]: i for i, p in enumerate(pool)}
        pool.sort(key=lambda e: (e[0], 0 if e[1] in prefer else 1, order[e[1]]))
        (wa, a), (wb, b) = pool[0], pool[1]
        k += 1
        name = f"m{k}"
        nodes[name] = (wa + wb, a, b)
        merges.append((a, b, name, wa + wb))
        pool = pool[2:] + [(wa + wb, name)]
    return nodes, merges


def huffman_depths(nodes, root):
    out = {}

    def go(n, d):
        w, l, r = nodes[n]
        if l is None:
            out[n] = d
        else:
            go(l, d + 1)
            go(r, d + 1)
    go(root, 0)
    return out


def huffman_codes(nodes, root):
    out = {}

    def go(n, c):
        w, l, r = nodes[n]
        if l is None:
            out[n] = c or "0"
        else:
            go(l, c + "0")
            go(r, c + "1")
    go(root, "")
    return out


def huffman_is_valid_run(items, merges):
    """every merge takes two nodes of minimum weight among the current pool (any tie-break allowed)"""
    pool = {n: w for n, w in items}
    for a, b, name, w in merges:
        ws = sorted(pool.values())
        if sorted([pool[a], pool[b]]) != ws[:2]:
            return False
        del pool[a], pool[b]
        pool[name] = w
    return len(pool) == 1


# ---------------------------------------------------------------- interval timeline (SVG)
def timeline(pfx, ivs, lo, hi, names=None, w=940, row=58, ticks=None, guides=(), hidden_rows=False, label_iv=True):
    """one row per interval [s, f] over an axis lo..hi.
    Ids: {pfx}-r{i} the row (hidden if hidden_rows), {pfx}-g{i} green 'chosen' overlay, {pfx}-x{i} 'dropped'
    overlay (dim + strike), {pfx}-h{i} outline highlight, {pfx}-v{j} vertical guide j (guides = [(x, text)])."""
    names = names or [None] * len(ivs)
    padl, padr = 92, 30
    sx = lambda x: padl + (x - lo) * (w - padl - padr) / (hi - lo)
    top = 26
    h = top + row * len(ivs) + 56
    o = [f'<svg class="gp-tl" id="{pfx}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">']
    for i, ((s, f), nm) in enumerate(zip(ivs, names)):
        y = top + i * row
        x1, x2 = sx(s), sx(f)
        bh = row * 0.46
        by = y + row * 0.40
        lab = f"[{num(s)}, {num(f)}]" if label_iv else ""
        tx = (x1 + x2) / 2
        o.append(f'<g id="{pfx}-r{i}"{" class=\"h\"" if hidden_rows else ""}>')
        if nm:
            o.append(f'<text x="{padl - 16}" y="{by + bh * 0.78:.1f}" class="gp-tl-nm">{_name_svg(nm)}</text>')
        o.append(f'<rect x="{x1:.1f}" y="{by:.1f}" width="{max(6, x2 - x1):.1f}" height="{bh:.1f}" rx="7" class="gp-bar"/>')
        o.append(f'<rect id="{pfx}-g{i}" x="{x1:.1f}" y="{by:.1f}" width="{max(6, x2 - x1):.1f}" height="{bh:.1f}" rx="7" '
                 f'class="gp-bar-ok h"/>')
        o.append(f'<g id="{pfx}-x{i}" class="h"><rect x="{x1 - 2:.1f}" y="{by - 2:.1f}" width="{max(6, x2 - x1) + 4:.1f}" '
                 f'height="{bh + 4:.1f}" rx="8" class="gp-bar-x"/><line x1="{x1 - 6:.1f}" y1="{by + bh / 2:.1f}" '
                 f'x2="{x2 + 6:.1f}" y2="{by + bh / 2:.1f}" class="gp-strike"/></g>')
        o.append(f'<rect id="{pfx}-h{i}" x="{x1 - 6:.1f}" y="{by - 6:.1f}" width="{max(6, x2 - x1) + 12:.1f}" '
                 f'height="{bh + 12:.1f}" rx="10" class="gp-bar-hi h"/>')
        if lab:
            o.append(f'<text x="{tx:.1f}" y="{by - 7:.1f}" class="gp-tl-lab">{lab}</text>')
        o.append("</g>")
    ay = top + row * len(ivs) + 10
    o.append(f'<line x1="{padl - 10}" y1="{ay}" x2="{w - padr + 10}" y2="{ay}" class="gp-axis"/>')
    for t in (ticks if ticks is not None else range(int(lo), int(hi) + 1)):
        o.append(f'<line x1="{sx(t):.1f}" y1="{ay - 6}" x2="{sx(t):.1f}" y2="{ay + 6}" class="gp-axis"/>'
                 f'<text x="{sx(t):.1f}" y="{ay + 34}" class="gp-tick">{num(t)}</text>')
    for j, (x, text) in enumerate(guides):
        o.append(f'<g id="{pfx}-v{j}" class="h"><line x1="{sx(x):.1f}" y1="{top - 18}" x2="{sx(x):.1f}" y2="{ay}" '
                 f'class="gp-guide"/><text x="{sx(x) + 8:.1f}" y="{top - 4}" class="gp-guide-t">{esc(text)}</text></g>')
    o.append("</svg>")
    return "".join(o)


def _name_svg(nm):
    """'c1' -> c with a subscript 1; anything else as is"""
    if len(nm) >= 2 and nm[0].isalpha() and nm[1:].isdigit():
        return f'{esc(nm[0])}<tspan dy="8" font-size="22">{esc(nm[1:])}</tspan>'
    return esc(nm)


# ---------------------------------------------------------------- chips, tables, tapes
def chips(pfx, items, hidden=True, cls="", label=None):
    """a row of boxes. items: [html]. Ids: {pfx}-{i} the chip, {pfx}-{i}-ok green mark, {pfx}-{i}-x red strike.
    label: a caption (RTL) at the start of the row."""
    out = [f'<div class="gp-chips {cls}" id="{pfx}" dir="ltr">']
    if label:
        out.append(f'<span class="gp-chiplab">{label}</span>')
    for i, t in enumerate(items):
        out.append(f'<span class="gp-chip{" h" if hidden else ""}" id="{pfx}-{i}"><span class="gp-ct">{t}</span>'
                   f'<i id="{pfx}-{i}-ok" class="gp-cok h"></i><i id="{pfx}-{i}-x" class="gp-cx h"></i></span>')
    out.append("</div>")
    return "".join(out)


def table(pfx, head, rows, hidden_rows=True, cls="", rtl=True):
    """an LTR table. head: [html]; rows: [[html]]. Ids: {pfx}-r{i} row (hidden if hidden_rows),
    {pfx}-c{i}-{j} highlight of cell (i, j), {pfx}-k{i} the row's ✓ mark (hidden), {pfx}-n{i} the row's ✗ mark."""
    hd = "".join(f"<th>{c}</th>" for c in head) + "<th></th>"
    body = []
    for i, r in enumerate(rows):
        cells = "".join(f'<td><i id="{pfx}-c{i}-{j}" class="cell-hi h"></i>{c}</td>' for j, c in enumerate(r))
        mark = (f'<td class="gp-mk"><b id="{pfx}-k{i}" class="gp-yes h">✓</b><b id="{pfx}-n{i}" class="gp-no h">✗</b></td>')
        body.append(f'<tr id="{pfx}-r{i}"{" class=\"h\"" if hidden_rows else ""}>{cells}{mark}</tr>')
    return (f'<table class="delta gp-tab {cls}" id="{pfx}" dir="{"rtl" if rtl else "ltr"}"><thead><tr>{hd}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table>')


def tapes(pfx, blocks, m, unit=34, label="סרט", hidden=True):
    """boxes packed onto tapes of length m: blocks = [[box lengths on tape 1], ...]. A row per tape (id {pfx}-t{r},
    hidden), box segments labelled with their length, the thrown-away rest hatched."""
    rows = []
    for r, blk in enumerate(blocks):
        segs = "".join(f'<span class="gp-box" style="width:{L * unit - 4}px">{L}</span>' for L in blk)
        rest = m - sum(blk)
        assert rest >= 0, (blk, m)
        waste = f'<span class="gp-waste" style="width:{rest * unit - 4}px"></span>' if rest else ""
        rows.append(f'<div class="gp-tape-row{" h" if hidden else ""}" id="{pfx}-t{r}"><span class="gp-tlab">{label} {r + 1}'
                    f'</span><span class="gp-tape" style="width:{m * unit}px">{segs}{waste}</span></div>')
    return f'<div class="gp-tapes" id="{pfx}" dir="ltr">{"".join(rows)}</div>'


def pack_greedy(boxes, m):
    """the tape greedy: keep the current tape while the box fits in its rest, else open a new one"""
    blocks, rest = [], 0
    for b in boxes:
        assert b <= m
        if blocks and b <= rest:
            blocks[-1].append(b)
            rest -= b
        else:
            blocks.append([b])
            rest = m - b
    return blocks


def pack_opt(boxes, m):
    """minimum number of tapes, in order (each tape takes a contiguous run of boxes): DP over prefixes"""
    n = len(boxes)
    best = [0] + [10 ** 9] * n
    for j in range(1, n + 1):
        for i in range(j):
            if sum(boxes[i:j]) <= m:
                best[j] = min(best[j], best[i] + 1)
    return best[n]


# ---------------------------------------------------------------- Huffman tree (SVG)
def tree_svg(pfx, nodes, merges, w=900, h=520, r=34, leaf_label=None, show_bits=True):
    """the final Huffman tree laid out by depth; leaves visible from the start, merge j (internal node + its two edges)
    is the group {pfx}-m{j} (hidden). {pfx}-bits = the 0/1 edge labels (hidden). {pfx}-hl-{leaf} = leaf highlight.
    leaf_label(name, weight) -> text under/inside a leaf."""
    root = merges[-1][2]
    depth = {}
    order = []

    def go(n, d):
        depth[n] = d
        _, l, rr = nodes[n]
        if l is None:
            order.append(n)
        else:
            go(l, d + 1)
            go(rr, d + 1)
    go(root, 0)
    maxd = max(depth.values())
    xs = {}
    for i, n in enumerate(order):
        xs[n] = r + 20 + i * (w - 2 * r - 40) / max(1, len(order) - 1)

    def fill(n):
        _, l, rr = nodes[n]
        if l is not None:
            fill(l)
            fill(rr)
            xs[n] = (xs[l] + xs[rr]) / 2
    fill(root)
    ys = {n: r + 14 + depth[n] * (h - 2 * r - 60) / max(1, maxd) for n in depth}
    o = [f'<svg class="gp-tree" id="{pfx}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">']
    bits = []
    for j, (a, b, name, wt) in enumerate(merges):
        g = [f'<g id="{pfx}-m{j}" class="h">']
        for c, bit in ((a, "0"), (b, "1")):
            dx, dy = xs[c] - xs[name], ys[c] - ys[name]
            dd = (dx * dx + dy * dy) ** 0.5 or 1.0
            g.append(f'<line x1="{xs[name] + dx / dd * r:.1f}" y1="{ys[name] + dy / dd * r:.1f}" '
                     f'x2="{xs[c] - dx / dd * r:.1f}" y2="{ys[c] - dy / dd * r:.1f}" class="gp-te"/>')
            mx, my = (xs[name] + xs[c]) / 2, (ys[name] + ys[c]) / 2
            bits.append(f'<text x="{mx + (-20 if bit == "0" else 20):.1f}" y="{my:.1f}" class="gp-bit">{bit}</text>')
        g.append(f'<circle cx="{xs[name]:.1f}" cy="{ys[name]:.1f}" r="{r}" class="gp-tn-in"/>'
                 f'<text x="{xs[name]:.1f}" y="{ys[name] + 10:.1f}" class="gp-tw">{wt}</text></g>')
        o += g
    for n in order:
        wt = nodes[n][0]
        o.append(f'<circle id="{pfx}-hl-{n}" cx="{xs[n]:.1f}" cy="{ys[n]:.1f}" r="{r + 8}" class="gp-tn-hi h"/>'
                 f'<rect x="{xs[n] - r:.1f}" y="{ys[n] - r:.1f}" width="{2 * r}" height="{2 * r}" rx="10" class="gp-tn-leaf"/>'
                 f'<text x="{xs[n]:.1f}" y="{ys[n] + 10:.1f}" class="gp-tw">{wt}</text>'
                 f'<text x="{xs[n]:.1f}" y="{ys[n] + r + 30:.1f}" class="gp-tl-leaf">'
                 f'{esc(leaf_label(n, wt) if leaf_label else n)}</text>')
    if show_bits:
        o.append(f'<g id="{pfx}-bits" class="h">{"".join(bits)}</g>')
    o.append("</svg>")
    return "".join(o)
