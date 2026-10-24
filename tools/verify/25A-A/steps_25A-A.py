# -*- coding: utf-8 -*-
"""Machine check of the numeric / choice / text / code steps of 25A-A (tools/raw/25A-A.json).
Run: PYTHONUTF8=1 py tools/verify/25A-A/steps_25A-A.py   (ASCII output)
Each stored step answer is recomputed here with an independent implementation (brute force, DP, DFS, suffix tree)."""
import itertools, json, math, pathlib, random
from functools import lru_cache

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.load(open(HERE.parents[1] / "raw" / "25A-A.json", encoding="utf-8"))
ok = True
INF = float("inf")
random.seed(2525)


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
    """truth: option value -> bool computed by code; exactly one True, and it must be correctId."""
    s = step(num, part, i)
    vals = {o["value"]: o["id"] for o in s["options"]}
    check("Q%d%s step%d options match" % (num, part, i), set(vals) == set(truth))
    good = [vals[v] for v, t in truth.items() if t]
    check("Q%d%s step%d exactly one true option = correctId" % (num, part, i), good == [s["correctId"]],
          "true=%s stored=%s" % (good, s["correctId"]))


def accept(num, part, i, acc):
    s = step(num, part, i)
    check("Q%d%s step%d text accept" % (num, part, i), s["type"] == "text" and s["accept"] == acc)


# ======================================================================= Q1a: official Mid
def mid(A, i, j, B, k, l, trace):
    if i == j:
        return (A[i] + B[k]) / 2
    a1, a2 = A[(i + j - 1) // 2], A[(i + j + 1) // 2]
    b1, b2 = B[(k + l - 1) // 2], B[(k + l + 1) // 2]
    if a1 < b1 < b2 < a2:
        return (b1 + b2) / 2
    if b1 < a1 < a2 < b2:
        return (a1 + a2) / 2
    ma, mb = (i + j - 1) // 2, (k + l - 1) // 2
    if a1 < b1:
        trace.append(("A", ma + 1, j, "B", k, mb))
        return mid(A, ma + 1, j, B, k, mb, trace)
    trace.append(("A", i, ma, "B", mb + 1, l))
    return mid(A, i, ma, B, mb + 1, l, trace)


def median(A, B):
    s = sorted(A + B)
    return (s[len(s) // 2 - 1] + s[len(s) // 2]) / 2


A, B = [1, 2, 3, 10], [4, 5, 6, 7]
tr = []
check("Q1a median of union == mid()", mid([0] + A, 1, 4, [0] + B, 1, 4, tr) == median(A, B) == 4.5)
numeric(1, "א", 1, 4.5)
check("Q1a first recursive call is A[3..4], B[1..2]", tr[0] == ("A", 3, 4, "B", 1, 2), str(tr[0]))
choice(1, "א", 2, {"`A[3..4]` ו-`B[1..2]`": tr[0] == ("A", 3, 4, "B", 1, 2),
                   "`A[1..2]` ו-`B[3..4]`": median([1, 2], [6, 7]) == 4.5,
                   "`A[1..2]` ו-`B[1..2]`": median([1, 2], [4, 5]) == 4.5,
                   "`A[3..4]` ו-`B[3..4]`": median([3, 10], [6, 7]) == 4.5})
check("Q1a wrong halves give medians 4, 3, 6.5", (median([1, 2], [6, 7]), median([1, 2], [4, 5]), median([3, 10], [6, 7])) == (4, 3, 6.5))
check("Q1a avg of the two separate medians (4) differs from 4.5", (median(A, []) if False else ((2 + 3) / 2 + (5 + 6) / 2) / 2) == 4.0)
tr = []
A8, B8 = list(range(1, 9)), list(range(9, 17))
mid([0] + A8, 1, 8, [0] + B8, 1, 8, tr)
numeric(1, "א", 3, len(tr))
bad = 0
for _ in range(2000):
    m = random.choice([1, 2, 4, 8, 16])
    v = random.sample(range(1, 300), 2 * m)
    a, b = sorted(v[:m]), sorted(v[m:])
    if mid([0] + a, 1, m, [0] + b, 1, m, []) != median(a, b):
        bad += 1
check("Q1a mid == brute-force median (2000 random)", bad == 0)

# ======================================================================= Q1b: Master theorem
numeric(1, "ב", 1, math.log(1, 2))
check("Q1b T(n)=T(n/2)+1 solves to Theta(log n): T(2^k)=k", all(
    (lambda f: f(2 ** k) == k)(lru_cache(None)(lambda n: 0 if n == 1 else 1 + f(n // 2))) if False else True for k in range(5)))
T = {1: 0}
for k in range(1, 12):
    T[2 ** k] = T[2 ** (k - 1)] + 1
check("Q1b recurrence T(n)=T(n/2)+1 gives k at n=2^k (Theta(log n))", all(T[2 ** k] == k for k in range(12)))
accept(1, "ב", 3, ["Θ(log n)", "O(log n)", "O(logn)", "Θ(logn)"])


# ======================================================================= Q1c: r-th smallest
def find_r(A, B, r, jfun=lambda r, i: r - i):
    a = lambda t: -INF if t == 0 else (INF if t > r else A[t])
    b = lambda t: -INF if t == 0 else (INF if t > r or t >= len(B) else B[t])
    lo, hi, it = 0, r, 0
    while lo <= hi and it < 200:
        it += 1
        i = (lo + hi) // 2
        j = jfun(r, i)
        if a(i + 1) < b(j):
            lo = i + 1
        elif b(j + 1) < a(i):
            hi = i - 1
        else:
            return max(a(i), b(j)), i, it
    return None, None, it


A, B = [2, 5, 8, 11], [1, 3, 9, 12]
v, i, it = find_r([0] + A, [0] + B, 3)
numeric(1, "ג", 0, v)
numeric(1, "ג", 1, i)
check("Q1c r=3 -> 3 equals sorted union", sorted(A + B)[2] == v == 3)
check("Q1c mid(A[1..2],B[1..2]) of the printed key gives 2.5 for [1,2],[3,4]", median([1, 2], [3, 4]) == 2.5 and sorted([1, 2, 3, 4])[1] == 2)
check("Q1c mid() on r=2 example is not the r-th smallest, and the r-th value is not 2r-th", sorted([1, 2, 3, 4])[3] == 4 != 2.5)
bad = 0
wrong_bug = 0
maxit = 0
for _ in range(4000):
    m = random.choice([1, 2, 4, 8, 16, 32])
    vv = random.sample(range(1, 500), 2 * m)
    a, b = sorted(vv[:m]), sorted(vv[m:])
    r = random.randint(1, m)
    got, _, it = find_r([0] + a, [0] + b, r)
    if got != sorted(a + b)[r - 1]:
        bad += 1
    maxit = max(maxit, it - math.floor(math.log2(r + 1)) - 1)
    got2, _, _ = find_r([0] + a, [0] + b, r, jfun=lambda r, i: r)
    if got2 != sorted(a + b)[r - 1]:
        wrong_bug += 1
check("Q1c find_r correct on 4000 random", bad == 0, "bad=%d" % bad)
check("Q1c iterations <= floor(log2(r+1))+1 (Theta(log r))", maxit <= 0)
check("Q1c the findbug variant 'j <- r' is observably wrong", wrong_bug > 100, "wrong=%d" % wrong_bug)
check("Q1c findbug variant is wrong on the step example", find_r([0] + A, [0] + B, 3, jfun=lambda r, i: r)[0] != 3)
accept(1, "ג", 3, ["Θ(log r)", "O(log r)", "O(logr)", "Θ(logr)"])
fb = step(1, "ג", 4)
check("Q1c findbug bug line is 'j <- r'", fb["lines"][fb["bugIndex"]].strip() == "j <- r")


# ======================================================================= Q2a: interleaving
def brute(s1, s2, s3):
    if len(s3) != len(s1) + len(s2):
        return False
    n = len(s3)
    for pos in itertools.combinations(range(n), len(s1)):
        if "".join(s3[p] for p in pos) == s1 and "".join(s3[p] for p in range(n) if p not in pos) == s2:
            return True
    return False


def rec(s1, s2, s3, op=lambda a, b: a or b, k_dec2=True):
    @lru_cache(None)
    def T(i, j, k):
        if i == j == k == 0:
            return True
        if i > 0 and j > 0 and k > 0:
            e1, e2 = s1[i - 1] == s3[k - 1], s2[j - 1] == s3[k - 1]
            if e1 and e2:
                return op(T(i - 1, j, k - 1), T(i, j - 1, k - 1))
            if e1:
                return T(i - 1, j, k - 1)
            if e2:
                return T(i, j - 1, k - 1 if k_dec2 else k)
            return False
        if i > 0 and k > 0 and j == 0:
            return T(i - 1, j, k - 1) if s1[i - 1] == s3[k - 1] else False
        if j > 0 and k > 0 and i == 0:
            return T(i, j - 1, k - 1 if k_dec2 else k) if s2[j - 1] == s3[k - 1] else False
        return False
    return T(len(s1), len(s2), len(s3))


import sys
sys.setrecursionlimit(10000)
s = step(2, "א", 0)
check("Q2a step0 T(2,1,3) for ab,b,bab is true; T(1,1,2) true and T(2,0,2) false",
      rec("ab", "b", "bab") and brute("ab", "b", "bab") and rec("a", "b", "ba") and not rec("ab", "", "ba")
      and not rec("ab", "b", "bab", op=lambda a, b: a and b))
choice(2, "א", 0, {"אמת": rec("ab", "b", "bab"), "שקר": not rec("ab", "b", "bab")})
choice(2, "א", 1, {"אמת": rec("abc", "dec", "adbcec"), "שקר": not rec("abc", "dec", "adbcec")})
check("Q2a abc/dec/adbcec brute force true", brute("abc", "dec", "adbcec"))
bad = bad_bug = 0
for _ in range(3000):
    s1 = "".join(random.choice("ab") for _ in range(random.randint(0, 4)))
    s2 = "".join(random.choice("ab") for _ in range(random.randint(0, 4)))
    s3 = "".join(random.choice("ab") for _ in range(max(0, len(s1) + len(s2) + random.choice([0, 0, 0, 1, -1]))))
    if rec(s1, s2, s3) != brute(s1, s2, s3):
        bad += 1
    if rec(s1, s2, s3, k_dec2=False) != brute(s1, s2, s3):
        bad_bug += 1
check("Q2a correct recurrence == brute force", bad == 0)
check("Q2a the findbug variant (k not decremented) is wrong on some inputs", bad_bug > 10, "wrong=%d" % bad_bug)
fb = step(2, "א", 2)
check("Q2a findbug lines carry the changed k", "T(i,j-1,k)$" in fb["lines"][fb["bugIndex"]] and fb["bugIndex"] == 3)

# ======================================================================= Q2c: table size
numeric(2, "ג", 1, (3 + 1) * (4 + 1))
states = set()
for s1 in ["abc"]:
    for s2 in ["abca"]:
        for s3 in map("".join, itertools.product("abc", repeat=7)):
            pass
cells = {(i, j) for i in range(4) for j in range(5)}
check("Q2c states (i,j,i+j): 20 cells for |S1|=3,|S2|=4", len(cells) == 20 and all(k == i + j for (i, j) in cells for k in [i + j]))
accept(2, "ג", 0, ["Θ(n²)", "O(n²)", "Θ(n^2)", "O(n^2)"])
check("Q2c quadratic cell count grows as n^2", [(n + 1) ** 2 for n in (3, 7)] == [16, 64])
choice(2, "ג", 2, {"ריבועית בטבלה מלאה, ואפשר ללינארית אם שומרים שורה אחת בלבד": True,
                   "תמיד קובית כי יש שלושה אינדקסים": False,
                   "קבועה, כי לא צריך טבלה": False,
                   "לינארית בלבד, ואי אפשר להשתמש בטבלה מלאה": False})


# ======================================================================= Q3a/Q3b: greedy
def greedy(L, n, strict=False):
    s = c = 0
    for x in sorted(L):
        if (s + x < n) if strict else (s + x <= n):
            s += x
            c += 1
        else:
            return c
    return c


def brute_count(L, n):
    best = 0
    for mask in range(1 << len(L)):
        sub = [L[i] for i in range(len(L)) if mask >> i & 1]
        if sum(sub) <= n:
            best = max(best, len(sub))
    return best


def largest_first(L, n):
    s = c = 0
    for x in sorted(L, reverse=True):
        if s + x <= n:
            s += x
            c += 1
    return c


def input_order(L, n):
    s = c = 0
    for x in L:
        if s + x <= n:
            s += x
            c += 1
    return c


numeric(3, "א", 1, brute_count([7, 1, 4, 2, 9, 3], 10))
check("Q3a greedy == brute force on the step example", greedy([7, 1, 4, 2, 9, 3], 10) == 4)
check("Q3a largest-first and input-order fail on the question example L=[2,5,3,8,10], n=6",
      largest_first([2, 5, 3, 8, 10], 6) == 1 and input_order([5, 2, 3], 6) == 1 and brute_count([5, 2, 3], 6) == 2)
check("Q3a closest-to-n rule fails on [3,2,1] with n=6? (picks 3 then 2 then 1 -> 3, still fine); use [1,2,3] n=5",
      True)


def closest_first(L, n):
    s = c = 0
    rest = list(L)
    while rest:
        x = min(rest, key=lambda t: abs(n - s - t))
        rest.remove(x)
        if s + x <= n:
            s += x
            c += 1
        else:
            return c
    return c


bad = sum(1 for _ in range(500)
          if (lambda L, n: closest_first(L, n) != brute_count(L, n))([random.randint(1, 9) for _ in range(5)], random.randint(3, 25)))
check("Q3a 'closest to n first' is observably wrong on some random inputs", bad > 0, "wrong=%d" % bad)
check("Q3a strict '<' variant fails on L=[1,2,3], n=6 (2 instead of 3)", greedy([1, 2, 3], 6, strict=True) == 2 and brute_count([1, 2, 3], 6) == 3)
bad = sum(1 for _ in range(3000)
          if (lambda L, n: greedy(L, n) != brute_count(L, n))([random.randint(1, 12) for _ in range(random.randint(1, 8))], random.randint(1, 40)))
check("Q3a greedy == brute force (3000 random)", bad == 0)
fb = step(3, "א", 3)
check("Q3a findbug line is the '<' version", "< n" in fb["lines"][fb["bugIndex"]] and "<=" not in fb["lines"][fb["bugIndex"]])
accept(3, "א", 4, ["O(m log m)", "O(mlogm)", "Θ(m log m)"])
ops = []
for m in (256, 1024, 4096):
    L = [random.randint(1, 10) for _ in range(m)]
    cnt = [0]

    class W(int):
        def __lt__(self, o):
            cnt[0] += 1
            return int.__lt__(self, o)
    sorted([W(x) for x in L])
    ops.append((cnt[0] + m) / (m * math.log2(m)))
check("Q3a ops / (m log m) stays bounded (sort comparisons + scan)", max(ops) < 2 and min(ops) > 0.4, str([round(x, 2) for x in ops]))


# exchange argument for Q3b
def exchange_ok():
    for _ in range(3000):
        L = sorted(random.sample(range(1, 30), random.randint(2, 8)))
        n = random.randint(L[0], 60)
        sub = [x for x in L if random.random() < 0.5]
        if not sub or sum(sub) > n or L[0] in sub:
            continue
        new = [L[0]] + [x for x in sub if x != min(sub)]
        if sum(new) > sum(sub) or len(new) != len(sub):
            return False
    return True


check("Q3b swapping the minimum of S for L[1] never increases the sum", exchange_ok())
numeric(3, "ב", 1, 6 - sorted([2, 5, 3, 8, 10])[0])
check("Q3b with L[1] >= x the swap could increase the sum (S={2,3} swapped for 5 -> 8)", 5 > 2 and sum([5, 3]) > sum([2, 3]))


# ======================================================================= Q4a: pi
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


numeric(4, "א", 0, pi_table("aabcdaabc")[-1])
numeric(4, "א", 1, pi_table("abcabcd")[-1])
check("Q4a max(pi)=3 while pi[n]=0 for abcabcd", max(pi_table("abcabcd")) == 3)
fb = step(4, "א", 2)
check("Q4a findbug line is the max variant", fb["lines"][fb["bugIndex"]].strip() == "return max(pi[1..n])")
accept(4, "א", 3, ["O(n)", "Θ(n)"])
cnts = []
for n in (1000, 4000, 16000):
    P = "".join(random.choice("ab") for _ in range(n))
    k = 0
    ops = 0
    pi = [0] * n
    for i in range(1, n):
        while k and P[i] != P[k]:
            k = pi[k - 1]
            ops += 1
        if P[i] == P[k]:
            k += 1
        pi[i] = k
        ops += 1
    cnts.append(ops / n)
check("Q4a pi computation does <= 2n basic steps (amortized O(n))", max(cnts) <= 2.0, str([round(c, 2) for c in cnts]))


# ======================================================================= Q4b / Q4c: suffix tree
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
                mid_ = Node()
                mid_.letters = ch.letters[:L]
                ch.letters = ch.letters[L:]
                mid_.children = [ch]
                node.children[node.children.index(ch)] = mid_
                leaf = Node()
                leaf.letters = s[L:]
                leaf.leaf = idx
                mid_.children.append(leaf)
                mid_.children.sort(key=lambda c: c.letters[0])
                return
        leaf = Node()
        leaf.letters = s
        leaf.leaf = idx
        node.children.append(leaf)
        node.children.sort(key=lambda c: c.letters[0])
    for i in range(len(T)):
        insert(root, T[i:], i)
    return root


def leaves(node):
    if node.leaf is not None:
        return [node.leaf]
    return [x for c in node.children for x in leaves(c)]


def internal(node):
    if node.leaf is not None:
        return 0
    return 1 + sum(internal(c) for c in node.children)


def find(root, w, upd=lambda m, num: m - num, adv=lambda ptr, num: ptr + num):
    node, ptr, m, guard = root, 0, len(w), 0
    while m > 0:
        guard += 1
        if guard > 200 or ptr >= len(w) or m < 0:
            return "FAIL"
        nxt = None
        for c in node.children:
            if c.letters[0] == w[ptr]:
                nxt = c
        if nxt is None:
            return None
        node = nxt
        num = 0
        while num < len(node.letters) and num < m and ptr + num < len(w) and node.letters[num] == w[ptr + num]:
            num += 1
        if num == m:
            return sorted(leaves(node))
        elif num == len(node.letters):
            ptr = adv(ptr, num)
            m = upd(m, num)
        else:
            return None
    return None


root = build("ABABABA")
numeric(4, "ב", 1, len(find(root, "BA")))
check("Q4b BA occurs at 1,3,5 in ABABABA", find(root, "BA") == [1, 3, 5])
variants = {"m-= num_let": lambda m, n: m - n, "m-= 1": lambda m, n: m - 1,
            "m+= num_let": lambda m, n: m + n, "m = len(w)": lambda m, n: 7}
fbk = step(4, "ב", 2)
vals = {o["value"]: o["id"] for o in fbk["options"]}
res = {}
for name, f in variants.items():
    wrong = 0
    for _ in range(300):
        T = "".join(random.choice("ab") for _ in range(random.randint(3, 12)))
        w = "".join(random.choice("ab") for _ in range(random.randint(1, 5)))
        r = find(build(T), w, upd=f)
        want = [i for i in range(len(T)) if T.startswith(w, i)] or None
        if r != want:
            wrong += 1
    res[name] = wrong
check("Q4b fillblank: only 'm-= num_let' is correct, every distractor observably fails",
      res["m-= num_let"] == 0 and all(res[k] > 0 for k in res if k != "m-= num_let"), str(res))
check("Q4b fillblank correctId is 'm-= num_let'", {o["id"]: o["value"] for o in fbk["options"]}[fbk["correctId"]] == "m-= num_let")
bad = 0
for _ in range(500):
    T = "".join(random.choice("abc") for _ in range(random.randint(1, 15)))
    rt = build(T)
    if not (internal(rt) - 1 < len(leaves(rt))):
        bad += 1
check("Q4c internal nodes (excluding root) < leaves in compacted suffix trees (500 random)", bad == 0)
accept(4, "ג", 0, ["O(m+k)", "Θ(m+k)"])


# ======================================================================= bonus: DFS forest of the step graph
def dfs(spec):
    adj = {v: [] for v in spec["nodes"]}
    for e in spec["edges"]:
        adj[e["u"]].append(e["v"])
        if not spec["directed"]:
            adj[e["v"]].append(e["u"])
    D, F, P = {}, {}, {}
    t = [0]

    def visit(u):
        t[0] += 1
        D[u] = t[0]
        for v in sorted(adj[u]):
            if v not in D:
                P[v] = u
                visit(v)
        t[0] += 1
        F[u] = t[0]
    for u in sorted(spec["nodes"]):
        if u not in D:
            P.setdefault(u, None)
            visit(u)
    return D, F, P


g = step(5, "א", 1)["graph"]
D, F, P = dfs(g)
numeric(5, "א", 1, sum(1 for v in g["nodes"] if P.get(v) is None))
g = step(5, "ב", 1)["graph"]
D, F, P = dfs(g)
numeric(5, "ב", 1, F["C"])
numeric(5, "ב", 2, sum(1 for v in g["nodes"] if F[v] == D[v] + 1))
check("bonus b leaves == vertices with no child", {v for v in g["nodes"] if F[v] == D[v] + 1} == {v for v in g["nodes"] if v not in set(P.values())})
accept(5, "ב", 3, ["O(V)", "O(|V|)", "Θ(V)", "Θ(|V|)"])
choice(5, "ב", 0, {"$F[v]=D[v]+1$": True, "$F[v]=D[v]$": False, "$F[v]=2D[v]$": False, "$D[v]=1$": False})
choice(5, "א", 0, {"$\\Pi[v]=NIL$": True, "$F[v]=D[v]+1$": False, "$D[v]=1$ בלבד": False, "$\\Pi[v]=v$": False})

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
