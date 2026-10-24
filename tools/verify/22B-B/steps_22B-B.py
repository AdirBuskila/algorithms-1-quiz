# -*- coding: utf-8 -*-
"""Machine check of the numeric / choice / text / code steps of 22B-B (tools/raw/22B-B.json).
Run: PYTHONUTF8=1 py tools/verify/22B-B/steps_22B-B.py   (ASCII output)"""
import heapq, itertools, json, pathlib, random
from functools import lru_cache

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.load(open(HERE.parents[1] / "raw" / "22B-B.json", encoding="utf-8"))
ok = True
random.seed(2222)


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
    check("Q%d%s step%d numeric == %r" % (num, part, i, expected), s["type"] == "numeric" and s["answer"] == expected,
          "stored=%r" % s.get("answer"))


def choice(num, part, i, truth):
    s = step(num, part, i)
    vals = {o["value"]: o["id"] for o in s["options"]}
    check("Q%d%s step%d options match" % (num, part, i), set(vals) == set(truth))
    good = [vals[v] for v, t in truth.items() if t]
    check("Q%d%s step%d exactly one true option = correctId" % (num, part, i), good == [s["correctId"]],
          "true=%s stored=%s" % (good, s["correctId"]))


def accept(num, part, i, acc):
    s = step(num, part, i)
    check("Q%d%s step%d text accept" % (num, part, i), s["type"] == "text" and s["accept"] == acc)


# ----------------------------------------------------------------- Huffman helpers
def huff_cost(f):
    h = list(f)
    heapq.heapify(h)
    c = 0
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        c += a + b
        heapq.heappush(h, a + b)
    return c


def optimal_lengths(f):
    n = len(f)
    best, sols = None, []
    for L in itertools.product(range(1, n), repeat=n):
        if sum(2.0 ** -l for l in L) != 1:
            continue
        c = sum(a * b for a, b in zip(f, L))
        if best is None or c < best:
            best, sols = c, [L]
        elif c == best:
            sols.append(L)
    return best, set(sols)


f1, f2 = (1, 1, 2, 3), (3, 3, 4, 5)
numeric(1, "א", 0, huff_cost(f1))
numeric(1, "א", 1, huff_cost(f2))
c1, s1 = optimal_lengths(f1)
c2, s2 = optimal_lengths(f2)
check("Q1a optimal length vectors are unique before and after and differ", len(s1) == 1 and len(s2) == 1 and not (s1 & s2),
      "%s %s" % (s1, s2))
(L1,), (L2,) = s1, s2
check("Q1a heaviest letter has length 1 before and 2 after", L1[3] == 1 and L2[3] == 2)
choice(1, "א", 2, {"אורך 1 לפני, ואורך 2 אחרי": (L1[3], L2[3]) == (1, 2),
                   "אורך 1 גם לפני וגם אחרי": (L1[3], L2[3]) == (1, 1),
                   "אורך 2 גם לפני וגם אחרי": (L1[3], L2[3]) == (2, 2),
                   "אורך 2 לפני, ואורך 1 אחרי": (L1[3], L2[3]) == (2, 1)})


def codes(tree, pre=""):
    if isinstance(tree, str):
        return {tree: pre}
    d = {}
    d.update(codes(tree[0], pre + "0"))
    d.update(codes(tree[1], pre + "1"))
    return d


def all_huff(nodes):
    if len(nodes) == 1:
        yield nodes[0][1]
        return
    nodes = sorted(nodes, key=lambda t: t[0])
    w1, w2 = nodes[0][0], nodes[1][0]
    for i, j in itertools.combinations(range(len(nodes)), 2):
        if sorted([nodes[i][0], nodes[j][0]]) != [w1, w2]:
            continue
        rest = [n for k, n in enumerate(nodes) if k not in (i, j)]
        a, b = nodes[i], nodes[j]
        orders = [(a, b)] if a[0] < b[0] else [(b, a)] if b[0] < a[0] else [(a, b), (b, a)]
        for l, r in orders:
            yield from all_huff(rest + [(l[0] + r[0], (l[1], r[1]))])


# ----------------------------------------------------------------- Q1b
sol = [(8 - y, y) for y in range(1, 8)
       if any(codes(t) == {"a": "1", "b": "00", "c": "01"} for t in all_huff([(8 - y, "a"), (2, "b"), (y, "c")]))]
numeric(1, "ב", 0, min(y for x, y in sol))
numeric(1, "ב", 1, max(y for x, y in sol))
choice(1, "ב", 2, {"$(6,2)$ ו-$(5,3)$": sorted(sol) == [(5, 3), (6, 2)],
                   "$(6,2)$ בלבד": sorted(sol) == [(6, 2)],
                   "$(6,2)$, $(5,3)$ ו-$(4,4)$": sorted(sol) == [(4, 4), (5, 3), (6, 2)],
                   "$(7,1)$, $(6,2)$ ו-$(5,3)$": sorted(sol) == [(5, 3), (6, 2), (7, 1)]})


# ----------------------------------------------------------------- suffix tree
class Node:
    def __init__(self):
        self.letters = ""
        self.children = []
        self.leaf = None


def build(T):
    T = T + "$"
    root = Node()

    def insert(node, s, idx):
        for ch in node.children:
            if ch.letters[0] == s[0]:
                L = 0
                while L < len(ch.letters) and L < len(s) and ch.letters[L] == s[L]:
                    L += 1
                if L == len(ch.letters):
                    return insert(ch, s[L:], idx)
                m = Node()
                m.letters = ch.letters[:L]
                ch.letters = ch.letters[L:]
                m.children = [ch]
                node.children[node.children.index(ch)] = m
                leaf = Node()
                leaf.letters = s[L:]
                leaf.leaf = idx
                m.children.append(leaf)
                m.children.sort(key=lambda c: c.letters[0])
                return
        leaf = Node()
        leaf.letters = s
        leaf.leaf = idx
        node.children.append(leaf)
    for i in range(len(T)):
        insert(root, T[i:], i)
    return root


def walk(node, depth=0, path=""):
    """yield (node, string depth, path string)"""
    yield node, depth, path
    for c in node.children:
        yield from walk(c, depth + len(c.letters), path + c.letters)


def leaves(node):
    if node.leaf is not None:
        return [node.leaf]
    return [x for c in node.children for x in leaves(c)]


T = "ABABABA"
root = build(T)
inner = [(n, d, p) for n, d, p in walk(root) if n.leaf is None and n is not root]
numeric(1, "ג", 0, len(inner))
a_node = [n for n, d, p in inner if p == "A"][0]
numeric(1, "ג", 1, len(leaves(a_node)))
numeric(1, "ג", 2, max(d for n, d, p in inner))
check("Q1c internal nodes are exactly A, ABA, ABABA, BA, BABA", sorted(p for n, d, p in inner) == sorted(["A", "ABA", "ABABA", "BA", "BABA"]))

# ----------------------------------------------------------------- Q1d
def longest_repeated(T):
    best = ""
    for i in range(len(T)):
        for j in range(i + 1, len(T) + 1):
            s = T[i:j]
            if len(s) > len(best) and T.count(s) < 1:
                pass
            if len(s) > len(best) and sum(1 for k in range(len(T)) if T.startswith(s, k)) >= 2:
                best = s
    return best


lr = longest_repeated(T)
numeric(1, "ד", 1, len(lr))
st = step(1, "ד", 2)
check("Q1d text answer", st["accept"] == [lr] and st["normalize"] == "lower", lr)
deepest = max(inner, key=lambda t: t[1])
check("Q1d deepest internal node by string depth is the longest repeat", deepest[2] == lr)
deepest_leaf = max([(n, d, p) for n, d, p in walk(root) if n.leaf is not None], key=lambda t: t[1])
check("Q1d the deepest leaf is a whole suffix with a single occurrence (not a repeat)", T.count(deepest_leaf[2].rstrip("$")) == 1 or deepest_leaf[2].rstrip("$") == T)
most = max(inner, key=lambda t: len(leaves(t[0])))
check("Q1d the internal node with most leaves is not the longest repeat", most[2] != lr)
choice(1, "ד", 0, {"הצומת הפנימי שאורך המחרוזת מהשורש אליו הוא המקסימלי": deepest[2] == lr,
                   "העלה העמוק ביותר בעץ": False,
                   "הצומת הפנימי עם הכי הרבה עלים מתחתיו": most[2] == lr,
                   "הילד הראשון של השורש": False})


# ----------------------------------------------------------------- Q2
def best_diff(A, k):
    best = -1
    for idx in itertools.combinations(range(len(A)), k):
        sb = sum(A[i] for i in idx)
        best = max(best, abs(sb - (sum(A) - sb)))
    return best


def split(A, k, branch_flip=False, pivot_else=None):
    n = len(A)
    sel = lambda i: sorted(A)[i - 1]
    B, C = [], []
    cond = (k < n - k)
    if branch_flip:
        cond = (k > n - k)
    if cond:
        S = sel(k)
        for v in A:
            (C if v > S else B).append(v)
    else:
        S = sel(pivot_else(n, k) if pivot_else else n - k)
        for v in A:
            (B if v > S else C).append(v)
    return B, C


def diff(A, k, **kw):
    B, C = split(A, k, **kw)
    return abs(sum(B) - sum(C)), len(B)


numeric(2, "א", 0, best_diff([13, 5, 7], 2))
check("Q2a fixed split on [13,5,7],k=2 is optimal", diff([13, 5, 7], 2) == (15, 2))
variants = {"n-k": lambda n, k: n - k, "k": lambda n, k: k, "k+1": lambda n, k: min(k + 1, n), "n": lambda n, k: n}
res = {}
for name, pf in variants.items():
    good = True
    for _ in range(600):
        n = random.randint(2, 7)
        k = random.randint(1, n - 1)
        A = random.sample(range(1, 40), n)
        if k < n - k:
            continue  # the else branch is only taken when k >= n-k
        d, sz = diff(A, k, pivot_else=pf)
        if sz != k or d != best_diff(A, k):
            good = False
    res[name] = good
check("Q2a else-branch pivot: only Select(A,n,n-k) is right", res == {"n-k": True, "k": False, "k+1": False, "n": False}, str(res))
choice(2, "א", 1, {"$Select(A,n,n-k)$ ואז הגדולים ממנו הם $B$ ($k$ איברים)": res["n-k"],
                   "$Select(A,n,k)$ ואז הגדולים ממנו הם $B$": res["k"],
                   "$Select(A,n,k+1)$ ואז הקטנים ממנו הם $B$": res["k+1"],
                   "$Select(A,n,n)$": res["n"]})
fb = step(2, "א", 2)
check("Q2a findbug line is the flipped condition", fb["lines"][fb["bugIndex"]].strip() == "if (k>n-k) do")
check("Q2a flipped condition gives 7 instead of 17 on [8,4,5,2,10],k=2",
      diff([8, 4, 5, 2, 10], 2, branch_flip=True)[0] == 7 and diff([8, 4, 5, 2, 10], 2)[0] == 17 == best_diff([8, 4, 5, 2, 10], 2))
bad = sum(1 for _ in range(500)
          if (lambda A, k: diff(A, k, branch_flip=True)[0] != best_diff(A, k))(*(lambda n: (random.sample(range(1, 40), n), random.randint(1, n - 1)))(random.randint(2, 7))))
check("Q2a flipped condition is observably wrong on random inputs", bad > 50, "wrong=%d" % bad)
accept(2, "א", 3, ["O(n)", "Θ(n)"])

numeric(2, "ב", 0, best_diff([1, 2, 3, 4, 5, 10], 2))
numeric(2, "ב", 1, best_diff([1, 2, 3, 4, 10], 3))
A = [1, 2, 3, 4, 5, 10]
check("Q2b k smallest vs k largest on step example: 19 vs 5", (sum(A) - 2 * sum(A[:2]), 2 * sum(A[-2:]) - sum(A)) == (19, 5))
A = [1, 2, 3, 4, 10]
check("Q2b k smallest vs k largest on second example: 8 vs 14", (sum(A) - 2 * sum(A[:3]), 2 * sum(A[-3:]) - sum(A)) == (8, 14))
bad = 0
for _ in range(3000):
    n = random.randint(2, 9)
    k = random.randint(1, n - 1)
    A = sorted(random.sample(range(1, 50), n))
    small, large = sum(A) - 2 * sum(A[:k]), 2 * sum(A[n - k:]) - sum(A)
    if max(small, large) != best_diff(A, k) or (k <= n - k and small < large) or (k > n - k and large < small):
        bad += 1
choice(2, "ב", 2, {"$k$ הקטנים כאשר $k\\le n-k$, ו-$k$ הגדולים כאשר $k>n-k$": bad == 0,
                   "תמיד $k$ הקטנים": False, "תמיד $k$ הגדולים": False,
                   "$k$ הגדולים כאשר $k\\le n-k$, ו-$k$ הקטנים אחרת": False})
check("Q2b rule k<=n-k -> smallest else largest verified (3000 random)", bad == 0)
accept(2, "ב", 3, ["O(n)", "Θ(n)"])

# ----------------------------------------------------------------- Q3a / Q3b : Prim on the step graph
g = step(3, "א", 1)["graph"]
adj = {v: [] for v in g["nodes"]}
for e in g["edges"]:
    adj[e["u"]].append((e["w"], e["v"]))
    adj[e["v"]].append((e["w"], e["u"]))
seen, order, tw, pq = set(), [], 0, [(0, "A")]
while pq:
    w, v = heapq.heappop(pq)
    if v in seen:
        continue
    seen.add(v)
    order.append(v)
    tw += w
    for w2, u in adj[v]:
        if u not in seen:
            heapq.heappush(pq, (w2, u))
s = step(3, "א", 1)
check("Q3a Prim order", s["accept"] == [", ".join(order)], ", ".join(order))
numeric(3, "א", 2, tw)


def msts(g):
    nodes, edges = g["nodes"], g["edges"]
    best, cnt = None, 0
    for sub in itertools.combinations(edges, len(nodes) - 1):
        par = {v: v for v in nodes}

        def f(x):
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x
        okk = True
        for e in sub:
            a, b = f(e["u"]), f(e["v"])
            if a == b:
                okk = False
                break
            par[a] = b
        if not okk:
            continue
        w = sum(e["w"] for e in sub)
        if best is None or w < best:
            best, cnt = w, 1
        elif w == best:
            cnt += 1
    return best, cnt


best, cnt = msts(g)
check("Q3a MST weight == Prim weight", best == tw == 50)
numeric(3, "ב", 0, cnt)
choice(3, "א", 0, {"הצלע הקלה ביותר המחברת קודקוד שבעץ לקודקוד שמחוץ לעץ": True,
                   "הצלע הקלה ביותר בגרף שעוד לא נבחרה": False,
                   "הצלע הקלה ביותר שיוצאת מהקודקוד האחרון שנוסף": False,
                   "הצלע הכבדה ביותר שאינה סוגרת מעגל": False})
check("Q3a the lightest edge of the graph (C-D, 1) is not Prim's first pick from A", order[1] == "J")

# ----------------------------------------------------------------- Q4
A = [1, 2, 5, 6, 8]


def C_rec(A, k, mode="ok"):
    @lru_cache(None)
    def C(i, j):
        if i >= j:
            return 0
        d = abs(A[i] - A[j])
        if (d < k) if mode == "lt" else (d <= k):
            return 0
        if mode == "max":
            return max(C(i + 1, j), C(i, j - 1)) + 1
        if mode == "both":
            return C(i + 1, j - 1) + 2
        if mode == "nop1":
            return min(C(i + 1, j), C(i, j - 1))
        return min(C(i + 1, j), C(i, j - 1)) + 1
    return C(0, len(A) - 1)


def brute_rem(A, k):
    n = len(A)
    best = 0
    for i in range(n):
        for j in range(i, n):
            if A[j] - A[i] <= k:
                best = max(best, j - i + 1)
    return n - best


numeric(4, "א", 0, brute_rem([1, 3, 4, 9, 10, 12, 17, 20], 4))
check("Q4a recurrence on example 1", C_rec([1, 3, 4, 9, 10, 12, 17, 20], 4) == 5)
numeric(4, "א", 1, brute_rem(A, 2))
check("Q4a recurrence on example 2", C_rec(A, 2) == 3)
mism = {m: 0 for m in ("max", "both", "nop1", "lt")}
for _ in range(1500):
    n = random.randint(2, 9)
    AA = sorted(random.sample(range(1, 40), n))
    k = random.randint(0, 12)
    want = brute_rem(AA, k)
    assert C_rec(AA, k) == want
    for m in mism:
        if C_rec(AA, k, m) != want:
            mism[m] += 1
check("Q4a recurrence == brute force; every distractor and the '<' bug are observably wrong", all(v > 0 for v in mism.values()), str(mism))
choice(4, "א", 2, {"$C(i,j)=\\min\\bigl(C(i+1,j),\\,C(i,j-1)\\bigr)+1$": True,
                   "$C(i,j)=\\max\\bigl(C(i+1,j),\\,C(i,j-1)\\bigr)+1$": mism["max"] == 0,
                   "$C(i,j)=C(i+1,j-1)+2$": mism["both"] == 0,
                   "$C(i,j)=\\min\\bigl(C(i+1,j),\\,C(i,j-1)\\bigr)$": mism["nop1"] == 0})
fb = step(4, "א", 3)
check("Q4a findbug bug line has '<k'", "|<k$" in fb["lines"][fb["bugIndex"]].replace(" ", "") or "<k$" in fb["lines"][fb["bugIndex"]].replace(" ", "") and fb["bugIndex"] == 0)
check("Q4a '<' bug fails on A={1,5},k=4", C_rec([1, 5], 4, "lt") == 1 and C_rec([1, 5], 4) == 0)
numeric(4, "ב", 0, sum(1 for i in range(5) for j in range(i, 5)))
accept(4, "ב", 1, ["O(n^2)", "Θ(n^2)", "O(n²)", "Θ(n²)"])
# step counts grow quadratically
check("Q4b cell count n(n+1)/2 ~ n^2", all(sum(1 for i in range(n) for j in range(i, n)) == n * (n + 1) // 2 for n in (5, 10, 20)))

# Q4c table cells by element value
vals = {v: i for i, v in enumerate(A)}
numeric(4, "ג", 0, C_rec(A[vals[6]:vals[8] + 1], 2))
numeric(4, "ג", 1, C_rec(A[vals[2]:vals[6] + 1], 2))
numeric(4, "ג", 2, C_rec(A, 2))
check("Q4c C(2,6)=1+min(C(5,6),C(2,5)) = 1+min(0,1)", C_rec([5, 6], 2) == 0 and C_rec([2, 5], 2) == 1)

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
