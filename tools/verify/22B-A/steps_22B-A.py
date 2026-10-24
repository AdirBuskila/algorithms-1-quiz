# -*- coding: utf-8 -*-
"""Machine check of the numeric / choice / text / code steps of 22B-A (tools/raw/22B-A.json).
Run: PYTHONUTF8=1 py tools/verify/22B-A/steps_22B-A.py   (ASCII output)"""
import itertools, json, math, pathlib, random
from functools import lru_cache

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.load(open(HERE.parents[1] / "raw" / "22B-A.json", encoding="utf-8"))
ok = True
random.seed(2201)


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
    check("Q%d%s step%d numeric == %r" % (num, part or "", i, expected), s["type"] == "numeric" and s["answer"] == expected,
          "stored=%r" % s.get("answer"))


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


def pi_table(P):
    pi = [0] * len(P)
    k = 0
    for i in range(1, len(P)):
        while k and P[i] != P[k]:
            k = pi[k - 1]
        if P[i] == P[k]:
            k += 1
        pi[i] = k
    return pi


# ----------------------------------------------------------------- Q1a
TARGET = [0, 0, 0, 0, 0, 1]
strings = ["".join(p) for p in itertools.product("ab", repeat=6)]
good = [s for s in strings if pi_table(s) == TARGET]
numeric(1, "א", 2, len(good))
check("Q1a solutions are abbbba and baaaab", sorted(good) == ["abbbba", "baaaab"])
with6 = [s for s in strings if pi_table(s)[-1] == 1]
imp = lambda f: all(f(s) for s in with6)
choice(1, "א", 0, {"$P[6]=P[1]$": imp(lambda s: s[5] == s[0]), "$P[6]=P[2]$": imp(lambda s: s[5] == s[1]),
                   "$P[5]=P[1]$": imp(lambda s: s[4] == s[0]), "$P[6]\\ne P[1]$": imp(lambda s: s[5] != s[0])})
choice(1, "א", 1, {"`abbbba`": pi_table("abbbba") == TARGET, "`abbbbb`": pi_table("abbbbb") == TARGET,
                   "`aabbba`": pi_table("aabbba") == TARGET, "`abbbab`": pi_table("abbbab") == TARGET})

# ----------------------------------------------------------------- Q1b
T1B = [0, 0, 1, 1, 2, 1]
check("Q1b no string over {a,b} of length 6 has pi = 0,0,1,1,2,1", not any(pi_table(s) == T1B for s in strings))
check("Q1b the forced string abaaba has pi[6]=3", pi_table("abaaba") == [0, 0, 1, 1, 2, 3])
numeric(1, "ב", 3, pi_table("abaaba")[-1])
# derivation: pi[1..5] constraints force abaab then P[6]=a
prefix = [s for s in ("".join(p) for p in itertools.product("ab", repeat=5)) if pi_table(s) == T1B[:5]]
check("Q1b pi[1..5] = 0,0,1,1,2 forces abaab or its swap", sorted(prefix) == ["abaab", "babba"])
fb = step(1, "ב", 2)
check("Q1b findbug line carries P[6]=P[1]=b", "P[6]=P[1]=b" in fb["lines"][fb["bugIndex"]])

# ----------------------------------------------------------------- Q1c
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


want = {"a": "0", "b": "100", "c": "101", "d": "11"}
pairs = [(x, y) for x in range(1, 30) for y in range(1, 40)
         if any(codes(t) == want for t in all_huff([(y, "a"), (2, "b"), (x, "c"), (5, "d")]))]
numeric(1, "ג", 0, min(x for x, y in pairs))
numeric(1, "ג", 1, max(x for x, y in pairs))
numeric(1, "ג", 2, max(y for x, y in pairs if x == 3))
numeric(1, "ג", 3, len(pairs))
check("Q1c official answer x=2:5..9, x=3:5..10", sorted(pairs) == sorted([(2, y) for y in range(5, 10)] + [(3, y) for y in range(5, 11)]))

# ----------------------------------------------------------------- Q1d
def lines(n):
    return 0 if n <= 1 else 1 + 2 * lines(n // 2)


numeric(1, "ד", 1, lines(16))
check("Q1d lines(2^k) = 2^k - 1", all(lines(2 ** k) == 2 ** k - 1 for k in range(1, 12)))
accept(1, "ד", 2, ["O(n)", "Θ(n)"])
choice(1, "ד", 0, {"$T(n)=2T(n/2)+O(1)$": True, "$T(n)=T(n/2)+O(1)$": False, "$T(n)=2T(n/2)+O(n)$": False, "$T(n)=T(n-1)+O(1)$": False})
check("Q1d the single-call recurrence would give 2^k-1 only as T(n)=2T(n/2)+1 (T(n/2)+1 gives k)",
      all(lines(2 ** k) != k for k in range(2, 8)))
# polynomial in input size: lines grows as 2^bits
check("Q1d work is exponential in the number of input bits", all(lines(2 ** k) + 1 == 2 ** (k) for k in range(1, 10)))

# ----------------------------------------------------------------- Q2
def brute_pair(A):
    n = len(A)
    vals = sorted(set(A))
    need = math.ceil(n / 2)
    cnt = {v: A.count(v) for v in vals}
    return any(cnt[vals[i]] + cnt[vals[i + 1]] >= need for i in range(len(vals) - 1))


def check_one(A, M, strict=False):
    n = len(A)
    need = math.ceil(n / 2)
    cm = A.count(M)
    if need <= cm < n:
        return True
    smaller = [v for v in A if v < M]
    if smaller:
        L = max(smaller)
        s = A.count(L) + cm
        if (s > n / 2) if strict else (s >= need):
            return True
    larger = [v for v in A if v > M]
    if larger:
        R = min(larger)
        sr = A.count(R) + cm
        if (sr > n / 2) if strict == "both" else (sr >= need):
            return True
    return False


def pair(A, cands="both", strict=False):
    n = len(A)
    s = sorted(A)
    m1, m2 = s[math.ceil(n / 2) - 1], s[n // 2]
    if cands == "both":
        c = [m1, m2]
    elif cands == "lower":
        c = [m1]
    elif cands == "minmax":
        c = [s[0], s[-1]]
    else:
        c = []
    r = any(check_one(A, M, strict) for M in c)
    if cands == "median_only":
        # median alone: only the count of the median itself, no neighbours
        r = any(math.ceil(n / 2) <= A.count(M) for M in [m1, m2])
    return r


numeric(2, None, 0, [5, 2, 8, 3, 2, 5, 8].count(5) + [5, 2, 8, 3, 2, 5, 8].count(8))
res = {}
for name in ("both", "lower", "minmax", "median_only"):
    bad = 0
    for _ in range(4000):
        n = random.randint(1, 8)
        A = [random.randint(1, 5) for _ in range(n)]
        if pair(A, name) != brute_pair(A):
            bad += 1
    res[name] = bad
check("Q2 candidates: both medians + neighbours is exact, every other option fails somewhere",
      res["both"] == 0 and all(res[k] > 0 for k in ("lower", "minmax", "median_only")), str(res))
choice(2, None, 1, {"שני החציונים (המקום $\\lceil n/2\\rceil$ והמקום $\\lfloor n/2\\rfloor+1$ במערך הממוין) ושכניהם": res["both"] == 0,
                    "רק החציון התחתון ושכניו": res["lower"] == 0,
                    "המינימום והמקסימום ושכניהם": res["minmax"] == 0,
                    "החציון בלבד, בלי שכנים": res["median_only"] == 0})
check("Q2 [1,2,3,4,5,5]: lower median alone misses the pair 4,5", brute_pair([1, 2, 3, 4, 5, 5]) and not pair([1, 2, 3, 4, 5, 5], "lower"))
check("Q2 [1,2,3,4]: true, and the '> n/2' bug returns False", brute_pair([1, 2, 3, 4]) and not pair([1, 2, 3, 4], strict="both"))
check("Q2 [1,1,3,4,5,6]: true; the findbug variant (> n/2) returns False", brute_pair([1, 1, 3, 4, 5, 6]) and not pair([1, 1, 3, 4, 5, 6], strict=True))
bad = sum(1 for _ in range(4000) if (lambda A: pair(A, strict=True) != brute_pair(A))([random.randint(1, 5) for _ in range(random.randint(1, 8))]))
check("Q2 '> n/2' variant observably wrong on random inputs", bad > 0, "wrong=%d" % bad)
fb = step(2, None, 2)
check("Q2 findbug line is the Count_L line with '> n/2'", fb["lines"][fb["bugIndex"]].strip() == "if (Count_L + Count_M > n/2) return True")
accept(2, None, 3, ["O(n)", "Θ(n)"])

# ----------------------------------------------------------------- Q3a
def trees(nodes, edges):
    out = []
    for sub in itertools.combinations(edges, len(nodes) - 1):
        par = {v: v for v in nodes}

        def f(x):
            while par[x] != x:
                x = par[x]
            return x
        okk = True
        for e in sub:
            a, b = f(e["u"]), f(e["v"])
            if a == b:
                okk = False
                break
            par[a] = b
        if okk:
            out.append(sub)
    return out


g = step(3, "א", 0)["graph"]
ts = trees(g["nodes"], g["edges"])
w = lambda t: sum(e["w"] for e in t)
bn = lambda t: max(e["w"] for e in t)
mw = min(w(t) for t in ts)
mb = min(bn(t) for t in ts)
numeric(3, "א", 0, mw)
numeric(3, "א", 1, bn([t for t in ts if w(t) == mw][0]))
tt = [t for t in ts if bn(t) == mb and w(t) != mw]
numeric(3, "א", 2, w(tt[0]))
check("Q3a exactly one MBST that is not an MST (weights 2+2)", len(tt) == 1 and sorted(e["w"] for e in tt[0]) == [2, 2])
name = lambda t: sorted(e["u"] + e["v"] for e in t)
check("Q3a other trees are MSTs", all(w(t) == mw for t in ts if t is not tt[0]) and len(ts) == 3)
choice(3, "א", 3, {"העץ שמורכב משתי הצלעות במשקל 2": True,
                   "העץ שמורכב מהצלע במשקל 1 ומהצלע $T$-$L$": w([e for e in g["edges"] if e["w"] == 1] + [g["edges"][0]]) != mw,
                   "העץ שמורכב מהצלע במשקל 1 ומהצלע $L$-$R$": w([e for e in g["edges"] if e["w"] == 1] + [g["edges"][2]]) != mw,
                   "כל שלושת העצים הפורשים": False})

# ----------------------------------------------------------------- Q3b
g = step(3, "ב", 1)["graph"]
ts = trees(g["nodes"], g["edges"])
mw = min(w(t) for t in ts)
mst = [t for t in ts if w(t) == mw]
numeric(3, "ב", 1, bn(mst[0]))
check("Q3b MST bottleneck equals the minimum bottleneck over all spanning trees of the 4-cycle", bn(mst[0]) == min(bn(t) for t in ts))
bad = 0
for _ in range(300):
    n = random.randint(3, 6)
    nodes = list(range(n))
    edges = []
    for u, v in itertools.combinations(nodes, 2):
        if random.random() < 0.6:
            edges.append({"u": u, "v": v, "w": random.randint(1, 6)})
    ts = trees(nodes, edges)
    if not ts:
        continue
    mw = min(w(t) for t in ts)
    mb = min(bn(t) for t in ts)
    if any(bn(t) != mb for t in ts if w(t) == mw):
        bad += 1
check("Q3b every MST is an MBST (300 random graphs)", bad == 0)

# ----------------------------------------------------------------- Q4
def count_sub(T, P):
    @lru_cache(None)
    def C(i, j):
        if j == 0:
            return 1
        if j > i:
            return 0
        if T[i - 1] != P[j - 1]:
            return C(i - 1, j)
        return C(i - 1, j - 1) + C(i - 1, j)
    return C(len(T), len(P))


def brute_sub(T, P):
    return sum(1 for idx in itertools.combinations(range(len(T)), len(P)) if all(T[i] == c for i, c in zip(idx, P)))


numeric(4, "א", 0, count_sub("subsequence", "see"))
check("Q4a 'subsequence','see' brute force", brute_sub("subsequence", "see") == 6)
mism = {"minus": 0, "prod": 0, "same": 0, "neq": 0}


def variant(T, P, kind):
    @lru_cache(None)
    def C(i, j):
        if j == 0:
            return 1
        if j > i:
            return 0
        if T[i - 1] != P[j - 1]:
            return C(i - 1, j - 1) if kind == "neq" else C(i - 1, j)
        a, b = C(i - 1, j - 1), C(i - 1, j)
        if kind == "minus":
            return a
        if kind == "prod":
            return a * b
        if kind == "same":
            return a + C(i, j - 1)
        return a + b
    return C(len(T), len(P))


for _ in range(1500):
    T = "".join(random.choice("ab") for _ in range(random.randint(1, 8)))
    P = "".join(random.choice("ab") for _ in range(random.randint(1, 4)))
    assert count_sub(T, P) == brute_sub(T, P)
    for k in mism:
        if variant(T, P, k) != brute_sub(T, P):
            mism[k] += 1
check("Q4a recurrence == brute force; each distractor and the findbug variant are observably wrong", all(v > 0 for v in mism.values()), str(mism))
choice(4, "א", 1, {"$C(i,j)=C(i-1,j-1)+C(i-1,j)$": True, "$C(i,j)=C(i-1,j-1)$": mism["minus"] == 0,
                   "$C(i,j)=C(i-1,j-1)\\cdot C(i-1,j)$": mism["prod"] == 0, "$C(i,j)=C(i-1,j-1)+C(i,j-1)$": mism["same"] == 0})
check("Q4a findbug example T=ba,P=a: correct 1, buggy 2 or more", count_sub("ba", "a") == 1 and variant("ba", "a", "neq") != 1)
numeric(4, "ב", 0, len("abcbac") * len("abc"))
accept(4, "ב", 1, ["O(|T||P|)", "O(|T|·|P|)", "O(|T|*|P|)", "O(nm)", "O(mn)"])
numeric(4, "ג", 0, count_sub("abcb", "ab"))
numeric(4, "ג", 1, count_sub("abcba", "abc"))
numeric(4, "ג", 2, count_sub("abcbac", "abc"))
check("Q4c brute force agrees", (brute_sub("abcb", "ab"), brute_sub("abcba", "abc"), brute_sub("abcbac", "abc")) == (2, 1, 3))

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
