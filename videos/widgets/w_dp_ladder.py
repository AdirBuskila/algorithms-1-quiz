# -*- coding: utf-8 -*-
"""Dynamic-programming widgets for the dp_ladder videos (D01..D09), plus the solvers the scripts assert with.

Stage widget (SVG, no TeX inside; every class is prefixed dl- so other courses are untouched):
  Grid(pfx, rows, cols, vals, given=…)   a DP table filled cell by cell. Ids, for a cell (r, c) (0-based positions in
      the drawn table, not the course indices):
        {pfx}-v-r-c    the value (hidden unless the cell is in `given`)
        {pfx}-cur-r-c  the cell being computed (teal frame)
        {pfx}-dep-r-c  a cell it reads (blue fill)
        {pfx}-pth-r-c  a cell on the traceback path (amber frame)
        {pfx}-ar-r-c-R-C an arrow from (r, c) to the cell (R, C) it reads
        {pfx}-rh-r / {pfx}-ch-c  a highlight behind a row / column header
      G.step(cell, deps) returns the show/hide list that moves the "current cell" marker to `cell`, marks the cells
      it reads and draws the arrows (and shows its value); G.off() clears the markers; G.path(cells) marks a path.
      Arrows are registered by step(): build the phrases first, then call G.html().
  eqs(pfx, lines, size)  a column of display formulas, revealed one by one: ids {pfx}-0, {pfx}-1, … (hidden)

Solvers (each with an independent brute force; the scripts assert table == brute force on the data they show).
"""
import html as _html
import itertools
import math
from functools import lru_cache

from vid import show, hide

INF = float("inf")


def esc(s):
    return _html.escape(str(s), quote=True)


# ====================================================================== stage widgets
class Grid:
    def __init__(self, pfx, rows, cols, vals, given=(), cw=88, ch=62, hw=None, corner="", fs=32, void=(),
                 scale=1.0, colw=None):
        """rows / cols: header labels (strings, may be ''), vals: {(r, c): text}; given: cells shown from the start;
        void: cells drawn greyed (outside the table's region, e.g. j > i); colw: {c: width} per-column override"""
        self.pfx, self.rows, self.cols, self.vals = pfx, list(rows), list(cols), dict(vals)
        self.given, self.void = set(given), set(void)
        self.cw, self.ch, self.hw, self.corner, self.fs, self.scale = cw, ch, hw or cw, corner, fs, scale
        self.colw = dict(colw or {})
        self.arrows = []                 # registered (cell, dep)
        self.on = []                     # ids currently shown by step()

    # geometry
    def _x(self, c):
        x = self.hw
        for k in range(c):
            x += self.colw.get(k, self.cw)
        return x

    def _w(self, c):
        return self.colw.get(c, self.cw)

    def box(self, r, c):
        return self._x(c), self.ch + r * self.ch, self._w(c), self.ch

    def center(self, r, c):
        x, y, w, h = self.box(r, c)
        return x + w / 2, y + h / 2

    def size(self):
        return self._x(len(self.cols)), self.ch * (len(self.rows) + 1)

    # timeline helpers
    def step(self, cell, deps=(), value=True, extra=()):
        ids = [f"{self.pfx}-cur-{cell[0]}-{cell[1]}"]
        for d in deps:
            ids.append(f"{self.pfx}-dep-{d[0]}-{d[1]}")
            if (cell, d) not in self.arrows:
                self.arrows.append((cell, d))
            ids.append(f"{self.pfx}-ar-{cell[0]}-{cell[1]}-{d[0]}-{d[1]}")
        ids += list(extra)
        do = hide(*[i for i in self.on if i not in ids]) + show(*ids)
        if value:
            do += show(self.v(cell))
        self.on = ids
        return do

    def off(self):
        do = hide(*self.on)
        self.on = []
        return do

    def v(self, cell):
        return f"{self.pfx}-v-{cell[0]}-{cell[1]}"

    def vals_do(self, cells):
        return show(*[self.v(c) for c in cells])

    def path(self, cells):
        return show(*[f"{self.pfx}-pth-{r}-{c}" for r, c in cells])

    # drawing
    def html(self):
        W, H = self.size()
        p = self.pfx
        o = [f'<svg class="dl-grid" id="{p}" viewBox="-4 -4 {W + 8} {H + 8}" width="{(W + 8) * self.scale:.0f}" '
             f'height="{(H + 8) * self.scale:.0f}" direction="ltr" style="--dl-fs:{self.fs}px">',
             '<defs>',
             f'<marker id="{p}-ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" '
             f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dl-ahead"/></marker>',
             '</defs>']
        # header highlights + headers
        for r, lab in enumerate(self.rows):
            y = self.ch + r * self.ch
            o.append(f'<rect id="{p}-rh-{r}" x="2" y="{y + 2}" width="{self.hw - 4}" height="{self.ch - 4}" rx="8" '
                     f'class="dl-hhl h"/>')
            o.append(f'<text x="{self.hw / 2}" y="{y + self.ch / 2}" class="dl-head">{esc(lab)}</text>')
        for c, lab in enumerate(self.cols):
            x = self._x(c)
            o.append(f'<rect id="{p}-ch-{c}" x="{x + 2}" y="2" width="{self._w(c) - 4}" height="{self.ch - 4}" rx="8" '
                     f'class="dl-hhl h"/>')
            o.append(f'<text x="{x + self._w(c) / 2}" y="{self.ch / 2}" class="dl-head">{esc(lab)}</text>')
        if self.corner:
            o.append(f'<text x="{self.hw / 2}" y="{self.ch / 2}" class="dl-corner">{esc(self.corner)}</text>')
        # cells
        for r in range(len(self.rows)):
            for c in range(len(self.cols)):
                x, y, w, h = self.box(r, c)
                cls = "dl-cell void" if (r, c) in self.void else "dl-cell"
                o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{cls}"/>')
        for r in range(len(self.rows)):
            for c in range(len(self.cols)):
                x, y, w, h = self.box(r, c)
                o.append(f'<rect id="{p}-dep-{r}-{c}" x="{x + 3}" y="{y + 3}" width="{w - 6}" height="{h - 6}" rx="7" '
                         f'class="dl-dep h"/>')
        for r in range(len(self.rows)):
            for c in range(len(self.cols)):
                x, y, w, h = self.box(r, c)
                o.append(f'<rect id="{p}-pth-{r}-{c}" x="{x + 4}" y="{y + 4}" width="{w - 8}" height="{h - 8}" rx="9" '
                         f'class="dl-pth h"/>')
                o.append(f'<rect id="{p}-cur-{r}-{c}" x="{x + 3}" y="{y + 3}" width="{w - 6}" height="{h - 6}" rx="8" '
                         f'class="dl-cur h"/>')
        for (r, c), t in self.vals.items():
            cx, cy = self.center(r, c)
            hid = "" if (r, c) in self.given else " h"
            o.append(f'<text id="{p}-v-{r}-{c}" x="{cx}" y="{cy}" class="dl-val{hid}">{esc(t)}</text>')
        # arrows: from the computed cell to the read cell; a neighbour gets a straight arrow, a far cell a curve
        # (bulging up, or left for a column) so that it does not run over the values in between
        def out(w, h, ux, uy):
            tx = (w / 2) / abs(ux) if ux else INF
            ty = (h / 2) / abs(uy) if uy else INF
            return min(tx, ty)

        def unit(dx, dy):
            d = math.hypot(dx, dy) or 1
            return dx / d, dy / d
        for (a, b) in self.arrows:
            (x1, y1), (x2, y2) = self.center(*a), self.center(*b)
            aid = f'{p}-ar-{a[0]}-{a[1]}-{b[0]}-{b[1]}'
            if abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1:
                ux, uy = unit(x2 - x1, y2 - y1)
                s1 = out(self._w(a[1]), self.ch, ux, uy) * 0.55
                s2 = out(self._w(b[1]), self.ch, ux, uy) * 0.55
                o.append(f'<line id="{aid}" x1="{x1 + ux * s1:.1f}" y1="{y1 + uy * s1:.1f}" '
                         f'x2="{x2 - ux * s2:.1f}" y2="{y2 - uy * s2:.1f}" class="dl-arrow h" marker-end="url(#{p}-ah)"/>')
                continue
            ux, uy = unit(x2 - x1, y2 - y1)
            nx, ny = uy, -ux
            if ny > 0 or (ny == 0 and nx > 0):
                nx, ny = -nx, -ny
            dist = math.hypot(x2 - x1, y2 - y1)
            k = 0.32 if a[0] == b[0] or a[1] == b[1] else 0.18
            cx, cy = (x1 + x2) / 2 + nx * k * dist, (y1 + y2) / 2 + ny * k * dist
            u1, u2 = unit(cx - x1, cy - y1), unit(cx - x2, cy - y2)
            s1 = out(self._w(a[1]), self.ch, *u1) * 0.62
            s2 = out(self._w(b[1]), self.ch, *u2) * 0.62
            o.append(f'<path id="{aid}" d="M{x1 + u1[0] * s1:.1f},{y1 + u1[1] * s1:.1f} Q{cx:.1f},{cy:.1f} '
                     f'{x2 + u2[0] * s2:.1f},{y2 + u2[1] * s2:.1f}" class="dl-arrow h" marker-end="url(#{p}-ah)"/>')
        o.append("</svg>")
        return "".join(o)


def eqs(pfx, lines, size=40, hidden=True):
    """a column of display formulas ($TeX$ inside), ids {pfx}-0 …"""
    h = " h" if hidden else ""
    rows = "".join(f'<div id="{pfx}-{k}" class="dl-eq{h}">{ln}</div>' for k, ln in enumerate(lines))
    return f'<div class="dl-eqs" style="font-size:{size}px">{rows}</div>'


def chips(pfx, items, hidden=True):
    """a row of small boxes (an array): ids {pfx}-<k>; items = [(top label, value)]"""
    h = " h" if hidden else ""
    cells = "".join(f'<span id="{pfx}-{k}" class="dl-chip{h}"><i>{esc(a)}</i><b>{esc(b)}</b></span>'
                    for k, (a, b) in enumerate(items))
    return f'<div class="dl-chips" dir="ltr">{cells}</div>'


# ====================================================================== solvers + brute force
def robber(A):
    """R(i) = max sum of pairwise non-adjacent elements of A[1..i]; R(0)=0, R(1)=A1"""
    R = [0] * (len(A) + 1)
    for i in range(1, len(A) + 1):
        R[i] = max(R[i - 1], A[i - 1] + (R[i - 2] if i >= 2 else 0))
    return R


def robber_bf(A, i=None):
    i = len(A) if i is None else i
    best = 0
    for mask in range(1 << i):
        idx = [k for k in range(i) if mask >> k & 1]
        if all(b - a > 1 for a, b in zip(idx, idx[1:])):
            best = max(best, sum(A[k] for k in idx))
    return best


def lis_end(A):
    """L(i) = length of the longest strictly increasing subsequence that ENDS at A[i]"""
    L = []
    for i in range(len(A)):
        L.append(1 + max([L[j] for j in range(i) if A[j] < A[i]], default=0))
    return L


def lis_end_bf(A, i):
    best = 0
    for r in range(1, i + 2):
        for c in itertools.combinations(range(i + 1), r):
            if c[-1] == i and all(A[a] < A[b] for a, b in zip(c, c[1:])):
                best = max(best, r)
    return best


def lis_prefix_bf(A, i):
    """longest increasing subsequence anywhere in A[1..i]"""
    return max([lis_end_bf(A, k) for k in range(i + 1)], default=0)


def jumps_to_end(A):
    """C(i) (1-based) = min jumps from index i to index n; C(n) = 0"""
    n = len(A)
    C = [None] * (n + 1)
    C[n] = 0
    for i in range(n - 1, 0, -1):
        C[i] = 1 + min((C[i + j] for j in range(1, min(A[i - 1], n - i) + 1)), default=INF)
    return C


def jumps_from_start(A):
    """D(i) (1-based) = min jumps from index 1 to index i; D(1) = 0"""
    n = len(A)
    D = [None] * (n + 1)
    D[1] = 0
    for i in range(2, n + 1):
        D[i] = 1 + min((D[j] for j in range(1, i) if j + A[j - 1] >= i), default=INF)
    return D


def jumps_bf(A, src, dst):
    """BFS over indices (1-based)"""
    from collections import deque
    dist = {src: 0}
    q = deque([src])
    while q:
        u = q.popleft()
        for j in range(1, A[u - 1] + 1):
            v = u + j
            if v <= len(A) and v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist.get(dst, INF)


def stairs(n, steps=(1, 2)):
    W = [0] * (n + 1)
    W[0] = 1
    for i in range(1, n + 1):
        W[i] = sum(W[i - s] for s in steps if s <= i)
    return W


def stairs_bf(n, steps=(1, 2)):
    cnt = 0
    for k in range(n + 1):
        for seq in itertools.product(steps, repeat=k):
            cnt += sum(seq) == n
    return cnt


def ops1k(K):
    """C(i) = min operations (+1, *2, *3) turning 1 into i; C(1)=0; C(i/2), C(i/3) = inf when not an integer"""
    C = [None, 0] + [None] * (K - 1)
    for i in range(2, K + 1):
        opts = [C[i - 1]] + ([C[i // 2]] if i % 2 == 0 else [INF]) + ([C[i // 3]] if i % 3 == 0 else [INF])
        C[i] = 1 + min(opts)
    return C


def ops1k_bf(K):
    from collections import deque
    dist = {1: 0}
    q = deque([1])
    while q:
        u = q.popleft()
        for v in (u + 1, 2 * u, 3 * u):
            if v <= K and v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def tri_path(A):
    """M(i, j) (1-based, j <= i) = max value of a path from [1,1] to [i,j], steps down or down-right"""
    n = len(A)
    M = {}
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            a = A[i - 1][j - 1]
            if i == 1:
                M[i, j] = a
            elif j == 1:
                M[i, j] = a + M[i - 1, 1]
            elif j == i:
                M[i, j] = a + M[i - 1, i - 1]
            else:
                M[i, j] = a + max(M[i - 1, j - 1], M[i - 1, j])
    return M


def tri_path_bf(A, i, j):
    best = -INF
    for steps in itertools.product((0, 1), repeat=i - 1):
        if sum(steps) == j - 1:
            r, c, s = 0, 0, A[0][0]
            for d in steps:
                r, c = r + 1, c + d
                s += A[r][c]
            best = max(best, s)
    return best


def grid_min(G):
    """S(i, j) = min sum of a path from the top-left cell to (i, j), steps right or down (0-based)"""
    n, m = len(G), len(G[0])
    S = {}
    for i in range(n):
        for j in range(m):
            prev = [S[i - 1, j]] if i else []
            prev += [S[i, j - 1]] if j else []
            S[i, j] = G[i][j] + (min(prev) if prev else 0)
    return S


def grid_min_bf(G, i, j):
    best = INF
    for mv in set(itertools.permutations("D" * i + "R" * j)):
        r = c = 0
        s = G[0][0]
        for d in mv:
            r, c = (r + 1, c) if d == "D" else (r, c + 1)
            s += G[r][c]
        best = min(best, s)
    return best


def lcs_table(X, Y):
    L = [[0] * (len(Y) + 1) for _ in range(len(X) + 1)]
    for i in range(1, len(X) + 1):
        for j in range(1, len(Y) + 1):
            L[i][j] = L[i - 1][j - 1] + 1 if X[i - 1] == Y[j - 1] else max(L[i - 1][j], L[i][j - 1])
    return L


def is_subseq(s, t):
    it = iter(t)
    return all(ch in it for ch in s)


def lcs_bf(X, Y):
    for r in range(len(X), -1, -1):
        for c in itertools.combinations(range(len(X)), r):
            if is_subseq("".join(X[k] for k in c), Y):
                return r
    return 0


def all_lcs(X, Y):
    b = lcs_bf(X, Y)
    return {"".join(X[k] for k in c) for c in itertools.combinations(range(len(X)), b)
            if is_subseq("".join(X[k] for k in c), Y)}


def lcs_back(X, Y, L, tie="up"):
    """traceback from (n, m): returns (cells visited, collected letters in collection order)"""
    i, j = len(X), len(Y)
    cells, got = [(i, j)], []
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            got.append(X[i - 1])
            i, j = i - 1, j - 1
        elif L[i - 1][j] > L[i][j - 1] or (L[i - 1][j] == L[i][j - 1] and tie == "up"):
            i -= 1
        else:
            j -= 1
        cells.append((i, j))
    return cells, got


def edit_table(X, Y):
    D = [[0] * (len(Y) + 1) for _ in range(len(X) + 1)]
    for i in range(len(X) + 1):
        D[i][0] = i
    for j in range(len(Y) + 1):
        D[0][j] = j
    for i in range(1, len(X) + 1):
        for j in range(1, len(Y) + 1):
            D[i][j] = D[i - 1][j - 1] if X[i - 1] == Y[j - 1] else 1 + min(D[i - 1][j - 1], D[i - 1][j], D[i][j - 1])
    return D


def edit_bf(X, Y):
    """BFS over strings: insert / delete / replace one letter (alphabet = letters of X and Y)"""
    from collections import deque
    alpha = sorted(set(X + Y))
    lim = len(X) + len(Y)
    dist = {X: 0}
    q = deque([X])
    while q:
        s = q.popleft()
        if s == Y:
            return dist[s]
        nxt = set()
        for k in range(len(s) + 1):
            for a in alpha:
                nxt.add(s[:k] + a + s[k:])
        for k in range(len(s)):
            nxt.add(s[:k] + s[k + 1:])
            for a in alpha:
                nxt.add(s[:k] + a + s[k + 1:])
        for t in nxt:
            if t not in dist and len(t) <= lim:
                dist[t] = dist[s] + 1
                q.append(t)
    return INF


def zero_square(M):
    n, m = len(M), len(M[0])
    T = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if M[i][j] == 1:
                T[i][j] = 0
            elif i == 0 or j == 0:
                T[i][j] = 1
            else:
                T[i][j] = 1 + min(T[i - 1][j], T[i][j - 1], T[i - 1][j - 1])
    return T


def zero_square_bf(M, i, j):
    best = 0
    s = 1
    while s <= min(i, j) + 1:
        if all(M[r][c] == 0 for r in range(i - s + 1, i + 1) for c in range(j - s + 1, j + 1)):
            best = s
        s += 1
    return best


def paint(cost):
    """cost[h] = (R, B, G); returns tables {color: [values per house]}"""
    T = {c: [cost[0][k]] for k, c in enumerate("RBG")}
    for h in range(1, len(cost)):
        for k, c in enumerate("RBG"):
            T[c].append(cost[h][k] + min(T[o][h - 1] for o in "RBG" if o != c))
    return T


def paint_bf(cost):
    best, arg = INF, None
    for cols in itertools.product(range(3), repeat=len(cost)):
        if all(a != b for a, b in zip(cols, cols[1:])):
            s = sum(cost[h][c] for h, c in enumerate(cols))
            if s < best:
                best, arg = s, ["RBG"[c] for c in cols]
    return best, arg


def hotels(p, t):
    """OPT(i, j): min effort to reach p_i in at most j days (p[0] = 0)"""
    n = len(p) - 1
    O = {}
    ops = 0
    for j in range(t + 1):
        O[0, j] = 0
    for i in range(1, n + 1):
        O[i, 0] = INF
    for j in range(1, t + 1):
        for i in range(1, n + 1):
            best = INF
            for l in range(i):
                ops += 1
                best = min(best, O[l, j - 1] + (p[i] - p[l]) ** 2)
            O[i, j] = best
    return O, ops


def hotels_bf(p, i, j):
    best = INF
    for r in range(0, j):
        for stops in itertools.combinations(range(1, i), r):
            pts = [0] + [p[s] for s in stops] + [p[i]]
            best = min(best, sum((b - a) ** 2 for a, b in zip(pts, pts[1:])))
    return best


def dice(n, m):
    T = [[0] * (m + 1) for _ in range(n + 1)]
    T[0][0] = 1
    for i in range(1, n + 1):
        for j in range(m + 1):
            T[i][j] = sum(T[i - 1][j - k] for k in range(1, 7) if j - k >= 0)
    return T


def dice_bf(i, j):
    return sum(1 for r in itertools.product(range(1, 7), repeat=i) if sum(r) == j)


def cut_min_count(S, ok):
    """C(i) min parts, N(i) number of cuts of S[1..i]; ok(a, b) for the 1-based piece S[a..b]"""
    n = len(S)
    C, N = [0] + [INF] * n, [1] + [0] * n
    for i in range(1, n + 1):
        for j in range(i):
            if ok(j + 1, i):
                C[i] = min(C[i], C[j] + 1)
                N[i] += N[j]
    return C, N


def cuts_bf(S, ok):
    """all cuts of S into valid pieces (lists of pieces)"""
    n = len(S)
    out = []
    for mask in range(1 << (n - 1)):
        bounds = [0] + [k + 1 for k in range(n - 1) if mask >> k & 1] + [n]
        if all(ok(a + 1, b) for a, b in zip(bounds, bounds[1:])):
            out.append([S[a:b] for a, b in zip(bounds, bounds[1:])])
    return out


def knap(t, v, T):
    n = len(t)
    P = [[0] * (T + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for c in range(T + 1):
            P[i][c] = P[i - 1][c]
            if t[i - 1] <= c:
                P[i][c] = max(P[i][c], v[i - 1] + P[i - 1][c - t[i - 1]])
    return P


def knap_bf(t, v, i, c):
    best = 0
    for r in range(i + 1):
        for s in itertools.combinations(range(i), r):
            if sum(t[k] for k in s) <= c:
                best = max(best, sum(v[k] for k in s))
    return best


def knap_back(t, v, P, T):
    i, c, cells, take = len(t), T, [], []
    while i > 0:
        cells.append((i, c))
        if P[i][c] != P[i - 1][c]:
            take.append(i)
            c -= t[i - 1]
        i -= 1
    cells.append((0, c))
    return cells, sorted(take)


def removal(A, k):
    """C(i, j) (0-based, i <= j): min removals from A[i..j] so that max - min <= k (A sorted)"""
    n = len(A)
    C = {}
    for L in range(n):
        for i in range(n - L):
            j = i + L
            C[i, j] = 0 if A[j] - A[i] <= k else 1 + min(C[i + 1, j], C[i, j - 1])
    return C


def removal_bf(A, k):
    n = len(A)
    best = n
    for mask in range(1, 1 << n):
        keep = [A[q] for q in range(n) if mask >> q & 1]
        if max(keep) - min(keep) <= k:
            best = min(best, n - len(keep))
    return best


def restaurants(d, p, k):
    n = len(d)
    prev = [0] * (n + 1)
    for i in range(1, n + 1):
        prev[i] = max([j for j in range(1, i) if d[i - 1] - d[j - 1] >= k], default=0)
    O = [0] * (n + 1)
    for i in range(1, n + 1):
        O[i] = max(O[i - 1], p[i - 1] + O[prev[i]])
    return O, prev


def restaurants_bf(d, p, k, i=None):
    i = len(d) if i is None else i
    best, arg = 0, ()
    for r in range(i + 1):
        for s in itertools.combinations(range(i), r):
            if all(d[b] - d[a] >= k for a, b in zip(s, s[1:])):
                val = sum(p[q] for q in s)
                if val > best:
                    best, arg = val, s
    return best, arg


def tasks(A):
    """T(i) (0-based) = min sum of a valid selection that ENDS with task i; T(i<0) = 0"""
    T = {}
    g = lambda i: 0 if i < 0 else T[i]
    for i in range(len(A)):
        T[i] = A[i] + min(g(i - 1), g(i - 2))
    ans = min(g(len(A) - 1), g(len(A) - 2))
    return T, ans


def tasks_bf(A):
    """min sum over subsets with no two consecutive tasks skipped"""
    n = len(A)
    best = INF
    for mask in range(1 << n):
        sk = [q for q in range(n) if not mask >> q & 1]
        if all(b - a > 1 for a, b in zip(sk, sk[1:])):
            best = min(best, sum(A[q] for q in range(n) if mask >> q & 1))
    return best
