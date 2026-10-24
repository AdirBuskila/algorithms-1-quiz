# -*- coding: utf-8 -*-
"""Machine check of the numeric / choice / text / code steps of 24A-A (tools/raw/24A-A.json).
Run: PYTHONUTF8=1 py tools/verify/24A-A/steps_24A-A.py   (ASCII output)"""
import itertools, json, math, pathlib, random
from collections import deque
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.load(open(HERE.parents[1] / "raw" / "24A-A.json", encoding="utf-8"))
ok = True
INF = float("inf")
random.seed(2401)


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


def step(num, part, i):
    for q in RAW["questions"]:
        if q["num"] == num and q.get("part") == part:
            return q["steps"][i]
    raise KeyError((num, part, i))


def numeric(num, part, i, expected):
    s = step(num, part, i)
    check("Q%d%s step%d numeric == %r" % (num, part or "", i, expected),
          s["type"] == "numeric" and abs(s["answer"] - expected) <= s.get("tol", 0), "stored=%r" % s.get("answer"))


def choice(num, part, i, truth):
    s = step(num, part, i)
    vals = {o["value"]: o["id"] for o in s["options"]}
    check("Q%d%s step%d options match" % (num, part or "", i), set(vals) == set(truth))
    good = [vals[v] for v, t in truth.items() if t]
    check("Q%d%s step%d exactly one true option = correctId" % (num, part or "", i), good == [s["correctId"]],
          "true=%s stored=%s" % (good, s["correctId"]))


def accept(num, part, i, acc):
    s = step(num, part, i)
    check("Q%d%s step%d text accept" % (num, part or "", i), s["type"] == "text" and s["accept"] == acc)


# ----------------------------------------------------------------- graphs
def adjacency(g):
    adj = {v: [] for v in g["nodes"]}
    for e in g["edges"]:
        adj[e["u"]].append(e["v"])
        adj[e["v"]].append(e["u"])
    return adj


def bfs(adj, s):
    d = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in sorted(adj[u]):
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return d


# Q1a
g = step(1, "א", 0)["graph"]
d = bfs(adjacency(g), "z")
numeric(1, "א", 0, d["y"])
check("Q1a yes-graph: x and y reachable from z", "x" in d and "y" in d)
g = step(1, "א", 1)["graph"]
d = bfs(adjacency(g), "z")
verdict = ("x" in d and "y" in d)
choice(1, "א", 1, {"אמת": verdict, "שקר": not verdict})
check("Q1a no-graph: only x reachable from z", "x" in d and "y" not in d)


def walk_exists(adj, x, y, z):
    dz = bfs(adj, z)
    return x in dz and y in dz


def walk_exists_bug(adj, x, y, z):
    # color[v] != WHITE variant: nothing is ever enqueued
    return x == z and y == z


def rand_graph(n, p):
    nodes = list(range(n))
    adj = {v: [] for v in nodes}
    for u, v in itertools.combinations(nodes, 2):
        if random.random() < p:
            adj[u].append(v)
            adj[v].append(u)
    return adj


# brute-force walk existence: x ~ z ~ y by connected components
def comp(adj, s):
    seen = {s}
    st = [s]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                st.append(v)
    return seen


bad = wrong = 0
for _ in range(1500):
    n = random.randint(3, 7)
    adj = rand_graph(n, 0.3)
    x, y, z = random.sample(range(n), 3)
    truth = (z in comp(adj, x)) and (y in comp(adj, z))
    if walk_exists(adj, x, y, z) != truth:
        bad += 1
    if walk_exists_bug(adj, x, y, z) != truth:
        wrong += 1
check("Q1a BFS from z == walk existence (1500 random)", bad == 0)
check("Q1a findbug variant is observably wrong", wrong > 50, "wrong=%d" % wrong)
fb = step(1, "א", 2)
check("Q1a findbug line", fb["lines"][fb["bugIndex"]].strip() == "if color[v] != WHITE")
accept(1, "א", 3, ["O(V+E)", "O(|V|+|E|)", "Θ(V+E)", "Θ(|V|+|E|)"])

# Q1b
g = step(1, "ב", 0)["graph"]
adj = adjacency(g)
dx = bfs(adj, "x")
dy = bfs(adj, "y")
numeric(1, "ב", 0, dx["z"])
v1 = dx["z"] + dy["z"] == dx["y"]
choice(1, "ב", 1, {"אמת": v1, "שקר": not v1})


def all_shortest_through(adj, x, y, z):
    dx_, dy_ = bfs(adj, x), bfs(adj, y)
    return y in dx_ and z in dx_ and z in dy_ and dx_[z] + dy_[z] == dx_[y]


def brute_shortest_through(adj, x, y, z):
    # enumerate simple paths x->y, keep shortest ones, test if any passes z
    best, paths = None, []

    def dfs(u, path):
        nonlocal best, paths
        if best is not None and len(path) - 1 > best:
            return
        if u == y:
            L = len(path) - 1
            if best is None or L < best:
                best, paths = L, [list(path)]
            elif L == best:
                paths.append(list(path))
            return
        for v in adj[u]:
            if v not in path:
                path.append(v)
                dfs(v, path)
                path.pop()
    dfs(x, [x])
    return any(z in p for p in paths)


bad = wrong = 0
for _ in range(1500):
    n = random.randint(3, 7)
    adj = rand_graph(n, 0.35)
    x, y, z = random.sample(range(n), 3)
    truth = brute_shortest_through(adj, x, y, z)
    if all_shortest_through(adj, x, y, z) != truth:
        bad += 1
    dx_, dy_ = bfs(adj, x), bfs(adj, y)
    bug = (y in dx_) and z in dx_ and z in dy_ and dx_[z] == dy_[z]
    if bug != truth:
        wrong += 1
check("Q1b d(x,z)+d(z,y)=d(x,y) == brute force (1500 random)", bad == 0)
check("Q1b findbug variant (dx[z]=dy[z]) is observably wrong", wrong > 50, "wrong=%d" % wrong)
fb = step(1, "ב", 2)
check("Q1b findbug line", fb["lines"][fb["bugIndex"]].strip() == "return (dx[z] = dy[z])")
accept(1, "ב", 3, ["O(V+E)", "O(|V|+|E|)", "Θ(V+E)", "Θ(|V|+|E|)"])


# ----------------------------------------------------------------- Q2: points and unit segments
def greedy_cover(points, strict=True):
    pts = sorted(points)
    segs, end = [], -INF
    for p in pts:
        if (p > end) if strict else (p >= end):
            segs.append((p, p + 1))
            end = p + 1
    return segs


def min_cover_brute(points):
    pts = sorted(set(points))
    for k in range(1, len(pts) + 1):
        for starts in itertools.combinations(pts, k):
            if all(any(s <= p <= s + 1 for s in starts) for p in pts):
                return k
    return 0


P = [0.2, 0.9, 1.3, 2.5, 2.7, 5.0]
numeric(2, "א", 0, len(greedy_cover(P)))
check("Q2a example is minimum", min_cover_brute(P) == 4)


def cover_valid(points, segs):
    return all(any(a <= p <= b for a, b in segs) for p in points)


def centered(points):
    segs, end = [], -INF
    for p in sorted(points):
        if p > end:
            segs.append((p - 0.5, p + 0.5))
            end = p + 0.5
    return segs


def ending(points):
    segs, end = [], -INF
    for p in sorted(points):
        if p > end:
            segs.append((p - 1, p))
            end = p
    return segs


def middle(points):
    pts = sorted(points)
    m = pts[len(pts) // 2]
    return [(m, m + 1)] if cover_valid(points, [(m, m + 1)]) else None


res = {"centered": 0, "ending": 0, "middle": 0, "bug": 0, "greedy": 0}
for _ in range(1500):
    pts = [random.choice([0, 0.5, 1, 1.5, 1.9, 2, 3, 3.5]) for _ in range(random.randint(1, 6))]
    opt = min_cover_brute(pts)
    if len(greedy_cover(pts)) != opt:
        res["greedy"] += 1
    if len(centered(pts)) != opt:
        res["centered"] += 1
    if len(ending(pts)) != opt:
        res["ending"] += 1
    m = middle(pts)
    if m is None or len(m) != opt:
        res["middle"] += 1
    if len(greedy_cover(pts, strict=False)) != opt:
        res["bug"] += 1
check("Q2a greedy exact; centered, ending, middle-start and the '>=' bug are each observably wrong",
      res["greedy"] == 0 and all(res[k] > 0 for k in ("centered", "ending", "middle", "bug")), str(res))
choice(2, "א", 1, {"מתחיל בנקודה הלא מכוסה השמאלית ביותר": res["greedy"] == 0,
                   "מרוכז סביב הנקודה הלא מכוסה השמאלית ביותר": res["centered"] == 0,
                   "מסתיים בנקודה הלא מכוסה השמאלית ביותר": res["ending"] == 0,
                   "מתחיל בנקודה האמצעית של הקלט": res["middle"] == 0})
check("Q2a 0,1,1.9 needs 2 (centered gives 3); 0,1 needs 1 (ending gives 2, '>=' gives 2)",
      min_cover_brute([0, 1, 1.9]) == 2 and len(centered([0, 1, 1.9])) == 3 and min_cover_brute([0, 1]) == 1
      and len(ending([0, 1])) == 2 and len(greedy_cover([0, 1], strict=False)) == 2)
fb = step(2, "א", 3)
check("Q2a findbug uses >=", fb["lines"][fb["bugIndex"]].strip() == "if point >= end:")
numeric(2, "ב", 1, len([p for p in [0, 0.5, 3, 3.2] if not any(a <= p <= b for a, b in greedy_cover([0, 0.5, 3, 3.2])[:1])]))
check("Q2b greedy first segment covers 0 and 0.5", greedy_cover([0, 0.5, 3, 3.2])[0] == (0, 1))
accept(2, "ג", 1, ["O(n log n)", "O(nlogn)", "Θ(n log n)"])
ratios = []
for n in (1024, 8192, 65536):
    cnt = [0]

    class W(float):
        def __lt__(self, o):
            cnt[0] += 1
            return float.__lt__(self, o)
    sorted([W(random.random()) for _ in range(n)])
    ratios.append((cnt[0], n))
check("Q2c sort comparisons dominate the linear scan (> n and ~ n log n)",
      all(c > n * 5 and c < n * math.log2(n) * 1.2 for c, n in ratios), str(ratios))
choice(2, "ג", 0, {"המיון ההתחלתי": ratios[-1][0] > ratios[-1][1], "המעבר על הנקודות": False,
                   "יצירת המקטעים": False, "החזרת רשימת המקטעים": False})

# ----------------------------------------------------------------- Q3: Alice and Bob
def run_probs(n, x, y):
    """exact distribution over Alice's index: returns (P[answer 'different'], P[answer 'equal'])"""
    diff = sum(1 for i in range(n) if x[i] != y[i])
    return Fraction(diff, n), Fraction(n - diff, n)


n = 10
x = [0] * n
y = list(x)
y[3] = 1
pd, pe = run_probs(n, x, y)
numeric(3, "א", 1, float(pd))
numeric(3, "א", 2, float(pe))
# 'different' is always correct: with equal strings the answer is never 'different'
allok = True
for n_ in (1, 2, 3, 4):
    for xs in itertools.product((0, 1), repeat=n_):
        pd_, _ = run_probs(n_, list(xs), list(xs))
        allok &= (pd_ == 0)
check("Q3a equal strings never produce 'different' (so 'different' is certain)", allok)
choice(3, "א", 0, {"נכונה בוודאות": allok, "נכונה בהסתברות $\\frac12$": False,
                   "נכונה בהסתברות $\\frac{n-1}{n}$": False, "נכונה בהסתברות $\\frac1n$": False})
for n_, want in ((1000, 11), (1025, 12)):
    pass
numeric(3, "ב", 0, math.ceil(math.log2(1000)) + 1)
numeric(3, "ב", 1, math.ceil(math.log2(1025)) + 1)
check("Q3b ceil(log2 n) == bit_length(n-1)", all(math.ceil(math.log2(m)) == (m - 1).bit_length() for m in (2, 3, 8, 9, 1000, 1025)))
# Q3c: n/2 distinct positions contain the differing position with probability exactly 1/2
n = 10
d = 3
cnt = sum(1 for S in itertools.combinations(range(n), n // 2) if d in S)
tot = math.comb(n, n // 2)
numeric(3, "ג", 0, cnt / tot)
choice(3, "ג", 1, {"$\\frac12$": Fraction(cnt, tot) == Fraction(1, 2), "$\\frac1n$": Fraction(cnt, tot) == Fraction(1, n),
                   "$\\frac{n-1}{n}$": Fraction(cnt, tot) == Fraction(n - 1, n), "$1$": Fraction(cnt, tot) == 1})

# ----------------------------------------------------------------- Q4: stable tower
L = [8, 5, 6, 3]
H = [3, 4, 2, 5]
W = [10, 9, 7, 6]   # widths, descending (the order given in the step)


def T_rec(L, H):
    n = len(L)
    Lx = [INF] + L
    Hx = [0] + H
    T = [0] * (n + 1)
    P = [0] * (n + 1)
    for i in range(1, n + 1):
        best, arg = -1, 0
        for j in range(0, i):
            if Lx[j] > Lx[i] and T[j] + Hx[i] > best:
                best, arg = T[j] + Hx[i], j
        T[i], P[i] = best, arg
    return T, P


def best_tower(L, H, W):
    n = len(L)
    best, argb = 0, []
    for k in range(1, n + 1):
        for sub in itertools.permutations(range(n), k):
            # sub is bottom -> top; each box above must have smaller length and width
            if all(L[sub[t + 1]] < L[sub[t]] and W[sub[t + 1]] < W[sub[t]] for t in range(k - 1)):
                h = sum(H[i] for i in sub)
                if h > best:
                    best, argb = h, [list(sub)]
                elif h == best:
                    argb.append(list(sub))
    return best, argb


T, P = T_rec(L, H)
bt, argb = best_tower(L, H, W)
numeric(4, "א", 1, T[3])
numeric(4, "א", 2, max(T))
check("Q4a recurrence == brute-force tower on the example", max(T) == bt == 12)
check("Q4a prefix-best (7) differs from T(3)=5, so the wrong meaning is observable", max(T[:3]) == 7 and T[3] == 5)
choice(4, "א", 0, {"גובה המגדל היציב הגבוה ביותר שהתיבה $i$ בראשו, מבין התיבות $1..i$": True,
                   "גובה המגדל הגבוה ביותר מבין התיבות $1..i$, בלי קשר לתיבה העליונה": False,
                   "מספר התיבות במגדל הגבוה ביותר": False, "גובה התיבה $i$ בלבד": False})
min_variant = [min(T_rec(L, H)[0][j] + H[i - 1] for j in range(0, i) if ([INF] + L)[j] > L[i - 1]) for i in range(1, 5)]
check("Q4a min-variant gives max 5 (= max H) instead of 12", max(min_variant) == 5 == max(H))
bad = 0
for _ in range(1000):
    n = random.randint(1, 6)
    Ws = sorted(random.sample(range(1, 30), n), reverse=True)
    Ls = random.sample(range(1, 30), n)
    Hs = [random.randint(1, 9) for _ in range(n)]
    if max(T_rec(Ls, Hs)[0]) != best_tower(Ls, Hs, Ws)[0]:
        bad += 1
check("Q4a recurrence == brute force on 1000 random box sets (widths descending)", bad == 0, "bad=%d" % bad)
fb = step(4, "א", 3)
check("Q4a findbug line has min", "\\min" in fb["lines"][fb["bugIndex"]])
numeric(4, "ב", 0, sum(1 for j in range(1, 7) for i in range(1, 7) if j < i))
accept(4, "ב", 1, ["O(n^2)", "Θ(n^2)", "O(n²)", "Θ(n²)"])
accept(4, "ב", 2, ["O(n)", "Θ(n)"])
# reconstruction
chain, i = [], max(range(1, 5), key=lambda t: T[t])
while i:
    chain.append(i)
    i = P[i]
numeric(4, "ג", 1, len(chain))
check("Q4c reconstructed tower is the unique best (boxes 4,2,1)", chain == [4, 2, 1] and len(argb) == 1 and sorted(argb[0]) == [0, 1, 3])
accept(4, "ג", 2, ["O(n^2)", "Θ(n^2)", "O(n²)", "Θ(n²)"])
accept(4, "ג", 3, ["O(n)", "Θ(n)"])
choice(4, "ג", 0, {"לכל $i$ את האינדקס $j$ של התיבה שמתחתיה במגדל הטוב ביותר שבראשו $i$": True,
                   "לכל $i$ את כל המגדל שבראשו $i$": False, "רק את הגובה המקסימלי": False,
                   "את התיבות ממוינות לפי גובה": False})

# ----------------------------------------------------------------- bonus
iv = [(0, 10), (9, 12), (11, 20)]


def disjoint(a, b):
    return a[1] < b[0] or b[1] < a[0]


def greedy_by(iv, key):
    chosen = []
    for a in sorted(iv, key=key):
        if all(disjoint(a, c) for c in chosen):
            chosen.append(a)
    return chosen


def opt(iv):
    best = 0
    for k in range(len(iv) + 1):
        for sub in itertools.combinations(iv, k):
            if all(disjoint(a, b) for a, b in itertools.combinations(sub, 2)):
                best = max(best, k)
    return best


numeric(5, None, 0, len(greedy_by(iv, lambda a: a[1] - a[0])))
numeric(5, None, 1, opt(iv))
m = {"end": 0, "start": 0, "short": 0}
for _ in range(1500):
    ivs = []
    for _ in range(random.randint(1, 6)):
        s = random.randint(0, 15)
        ivs.append((s, s + random.randint(1, 12)))
    o = opt(ivs)
    if len(greedy_by(ivs, lambda a: a[1])) != o:
        m["end"] += 1
    if len(greedy_by(ivs, lambda a: a[0])) != o:
        m["start"] += 1
    if len(greedy_by(ivs, lambda a: a[1] - a[0])) != o:
        m["short"] += 1
check("bonus: earliest-finish is exact; earliest-start and shortest-first are observably wrong",
      m["end"] == 0 and m["start"] > 0 and m["short"] > 0, str(m))
choice(5, None, 2, {"המקטע שמסתיים מוקדם ביותר": m["end"] == 0, "המקטע שמתחיל מוקדם ביותר": m["start"] == 0,
                    "המקטע הקצר ביותר": m["short"] == 0})
check("bonus: [0,100],[1,2],[3,4] breaks earliest-start", len(greedy_by([(0, 100), (1, 2), (3, 4)], lambda a: a[0])) == 1 and opt([(0, 100), (1, 2), (3, 4)]) == 2)

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
