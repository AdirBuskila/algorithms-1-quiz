# -*- coding: utf-8 -*-
"""Step-value checks for 22A-B (algorithms-1). Run: py -X utf8 -I tools/verify/22A-B/steps_22A-B.py
Recomputes every numeric / trace / complexity answer used in the guided steps, shows that every choice distractor
fails on some input, then binds the results to tools/raw/22A-B.json. ASCII output.
Hebrew parts are addressed by letter index (a=first Hebrew letter) so this file holds no Hebrew."""
import heapq, itertools, json, math, pathlib, random
from fractions import Fraction
from functools import lru_cache

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.loads((HERE.parents[1] / "raw" / "22A-B.json").read_text(encoding="utf-8"))
ok = True
INF = float("inf")


def H(letter):
    return "" if letter == "" else chr(0x05d0 + "abcdefgh".index(letter))


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


def item(num, part=""):
    for q in RAW["questions"]:
        if q["num"] == num and q.get("part", "") == H(part):
            return q
    raise KeyError((num, part))


def step(num, part, idx):
    return item(num, part)["steps"][idx]


def bind_numeric(num, part, idx, expected, label):
    s = step(num, part, idx)
    check(f"bind {label}: numeric step {idx} answer == recomputed {expected}", s["type"] == "numeric" and s["answer"] == expected)


def bind_text(num, part, idx, expected, label):
    s = step(num, part, idx)
    check(f"bind {label}: text step {idx} accepts it", s["type"] == "text" and expected in s["accept"])


def bind_first(num, part, idx, label):
    s = step(num, part, idx)
    check(f"bind {label}: choice step {idx} correct option is the verified one (id a)", s["type"] == "choice" and s["correctId"] == "a")


random.seed(22)

# ============================== Q1: minimal cut DP ==============================
WORDS = {"BA", "BAH", "HR", "GE", "RGE", "HRGE"}      # Latin stand-ins for the Hebrew letters of the example string


def dp_cut(S, words, mode="ok"):
    n = len(S)
    T = (lambda a, b: 1 if S[a - 1:b] in words else (0 if mode == "T0" else INF))
    C = [0] * (n + 1)
    if mode == "base1":
        C[0] = 1
    if mode == "baseinf":
        C[0] = INF
    if mode == "baseneg":
        C[0] = -1
    for i in range(1, n + 1):
        cand = []
        for j in range(0, i):
            if mode == "max":
                cand.append(C[j] + T(j + 1, i))
            elif mode == "plus1":
                cand.append(C[j] + T(j + 1, i) + 1)
            elif mode == "noT":
                cand.append(C[j])
            else:
                cand.append(C[j] + T(j + 1, i))
        C[i] = max(cand) if mode == "max" else min(cand)
    return C


def brute_cut(S, words):
    n = len(S)
    best = INF
    for mask in range(1 << (n - 1)):
        parts, last = [], 0
        for k in range(n - 1):
            if mask >> k & 1:
                parts.append(S[last:k + 1])
                last = k + 1
        parts.append(S[last:])
        if all(p in words for p in parts):
            best = min(best, len(parts))
    return best


S0 = "BAHRGE"
C = dp_cut(S0, WORDS)
check("Q1 example C(6) = 2 = brute force, C(4) = 2, C(5) = inf", C[6] == brute_cut(S0, WORDS) == 2 and C[4] == 2 and C[5] == INF, C)
bind_numeric(1, "", 0, C[4], "Q1 C(4)")
bind_numeric(1, "", 1, C[6], "Q1 C(6)")
bad = 0
for _ in range(500):
    n = random.randint(1, 9)
    S = "".join(random.choice("ab") for _ in range(n))
    words = {"".join(random.choice("ab") for _ in range(random.randint(1, 3))) for _ in range(4)}
    bad += dp_cut(S, words)[n] != brute_cut(S, words)
check("Q1 recurrence vs brute force (500 random)", bad == 0)
for mode in ("T0", "max", "plus1", "noT", "base1", "baseinf", "baseneg"):
    check(f"Q1 distractor '{mode}' fails on the example", dp_cut(S0, WORDS, mode)[6] != 2 or dp_cut(S0, WORDS, mode)[4] != 2)
bind_first(1, "", 2, "Q1 T value")
bind_first(1, "", 3, "Q1 recurrence")
bind_first(1, "", 4, "Q1 base case")

# ============================== Q2a: majority slope ==============================
def slope(p):
    return "inf" if p[0] == 0 else Fraction(p[1], p[0])


def boyer_moore(a):
    cand, cnt = None, 0
    for v in a:
        if cnt == 0:
            cand, cnt = v, 1
        elif v == cand:
            cnt += 1
        else:
            cnt -= 1
    return cand


PTS = [(1, 2), (2, 4), (3, 6), (1, 5), (0, 3), (0, 7)]
sl = [slope(p) for p in PTS]
maxline = max(sl.count(s) for s in set(sl))
check("Q2a example: at most 3 points on a line through the origin (brute force over all pairs)",
      maxline == 3 and max(sum(1 for q in PTS if p[0] * q[1] == p[1] * q[0]) for p in PTS) == 3)
bind_numeric(2, "a", 1, maxline, "Q2a")
# collinear-with-origin == same slope; distractors are not
bad = bad_y = bad_sum = bad_dist = 0
for _ in range(2000):
    p, q = [(random.randint(-4, 4), random.randint(-4, 4)) for _ in range(2)]
    if p == (0, 0) or q == (0, 0):
        continue
    col = p[0] * q[1] == p[1] * q[0]
    bad += col != (slope(p) == slope(q))
    bad_y += col != (p[1] == q[1])
    bad_sum += col != (p[0] + p[1] == q[0] + q[1])
    bad_dist += col != (p[0] ** 2 + p[1] ** 2 == q[0] ** 2 + q[1] ** 2)
check("Q2a same slope <=> same line through origin; the three distractors disagree somewhere", bad == 0 and bad_y > 0 and bad_sum > 0 and bad_dist > 0)
bind_first(2, "a", 0, "Q2a collinearity")
bm = boyer_moore(sl)
check("Q2a Boyer-Moore returns a candidate although no line has 51 percent (so counting is required)",
      bm is not None and sl.count(bm) < Fraction(51, 100) * len(sl))
bind_first(2, "a", 2, "Q2a verify count")
def majority_alg(points):
    work = 0
    slopes = []
    for q in points:
        slopes.append(slope(q))
        work += 1
    cand, cnt = None, 0
    for v in slopes:
        work += 1
        if cnt == 0:
            cand, cnt = v, 1
        elif v == cand:
            cnt += 1
        else:
            cnt -= 1
    c = 0
    for v in slopes:
        work += 1
        c += v == cand
    return c * 100 >= 51 * len(points), work


ratios = []
for n in (100, 1000, 10000):
    pts = [(random.randint(0, 9), random.randint(1, 9)) for _ in range(n)]
    ratios.append(majority_alg(pts)[1] / n)
check("Q2a measured work is exactly 3 touches per point (linear)", ratios == [3.0, 3.0, 3.0], ratios)
truth_bad = 0
for _ in range(500):
    n = random.randint(1, 12)
    pts = [(random.randint(0, 2), random.randint(1, 3)) for _ in range(n)]
    best = max(sum(1 for q in pts if p[0] * q[1] == p[1] * q[0]) for p in pts)
    truth_bad += majority_alg(pts)[0] != (best * 100 >= 51 * n)
check("Q2a algorithm decision == brute force over all lines through the origin (500 random)", truth_bad == 0)
bind_text(2, "a", 3, "O(n)", "Q2a complexity")

# ============================== Q2b: 34 percent, SELECT at ceil(n/3), ceil(2n/3) ==============================
def reps(a, num):
    s = sorted(a)
    n = len(a)
    return {s[math.ceil(n / 3) - 1], s[math.ceil(2 * n / 3) - 1]}


bad = bad_half = bad_third = bad_two = 0
for _ in range(4000):
    n = random.randint(1, 40)
    a = [random.randint(0, random.randint(1, 6)) for _ in range(n)]
    s = sorted(a)
    thr = Fraction(34, 100) * n
    frequent = {v for v in set(a) if a.count(v) >= thr}
    bad += any(v not in reps(a, n) for v in frequent)
    bad_half += any(v != s[math.ceil(n / 2) - 1] for v in frequent)
    bad_third += any(v != s[math.ceil(n / 3) - 1] for v in frequent)
    bad_two += any(v != s[math.ceil(2 * n / 3) - 1] for v in frequent)
check("Q2b every value with >= 34 percent equals the element at rank ceil(n/3) or ceil(2n/3) (4000 random)", bad == 0)
check("Q2b a single rank (n/2, n/3 or 2n/3) misses a frequent value on some input", bad_half > 0 and bad_third > 0 and bad_two > 0)
bind_first(2, "b", 0, "Q2b ranks")
need = math.ceil(Fraction(34, 100) * 50)
check("Q2b n=50 needs 17 points", need == 17)
bind_numeric(2, "b", 1, need, "Q2b threshold")
arr = [3, 1, 2, 3, 1, 3, 4, 3, 5, 6]
v = sorted(arr)[math.ceil(2 * len(arr) / 3) - 1]
check("Q2b example: rank-7 element is 3, appears 4 times, 4 >= 3.4", v == 3 and arr.count(v) == 4)
bind_numeric(2, "b", 2, arr.count(v), "Q2b example")

# ============================== Q3: mismatch positions via KMP on swapped pattern ==============================
def mismatch_positions(T, P):
    return [i for i in range(len(T) - len(P) + 1) if all(P[j] != T[i + j] for j in range(len(P)))]


def match_positions(T, P):
    return [i for i in range(len(T) - len(P) + 1) if T[i:i + len(P)] == P]


swap = lambda P: P.translate(str.maketrans("ab", "ba"))
check("Q3 swap(aabab) = bbaba", swap("aabab") == "bbaba")
bind_first(3, "", 0, "Q3 pattern")
bad = 0
cases = []
for _ in range(3000):
    n, m = random.randint(1, 12), random.randint(1, 5)
    if m > n:
        continue
    T = "".join(random.choice("ab") for _ in range(n))
    P = "".join(random.choice("ab") for _ in range(m))
    cases.append((T, P))
    bad += mismatch_positions(T, P) != match_positions(T, swap(P))
check("Q3 mismatch positions == KMP matches of the swapped pattern (3000 random)", bad == 0)
check("Q3 distractors (reversed / unchanged / all b) fail on some input",
      all(any(mismatch_positions(T, P) != match_positions(T, f(P)) for T, P in cases)
          for f in (lambda P: swap(P)[::-1], lambda P: P, lambda P: "b" * len(P))))
Tx, Px = "abbaabba", "ab"
pos = mismatch_positions(Tx, Px)
check("Q3 example: positions 3 and 7 (1-indexed), count 2", [i + 1 for i in pos] == [3, 7] and len(pos) == 2 == len(match_positions(Tx, swap(Px))))
bind_numeric(3, "", 1, len(pos), "Q3 example")
# alphabet of size 3: p != t does not imply the swapped letter equals t
check("Q3 over three letters the swap trick fails (p=a, t=c)", ("a" != "c") and not ("b" == "c"))
bind_first(3, "", 2, "Q3 why alphabet two")


def kmp_ops(text, pat):
    pi = [0] * len(pat)
    ops, k = 0, 0
    for i in range(1, len(pat)):
        while k and pat[i] != pat[k]:
            k = pi[k - 1]
            ops += 1
        if pat[i] == pat[k]:
            k += 1
        pi[i] = k
        ops += 1
    k = 0
    for ch in text:
        while k and (k == len(pat) or ch != pat[k]):
            k = pi[k - 1]
            ops += 1
        if ch == pat[k]:
            k += 1
        ops += 1
    return ops


r = []
for n in (100, 1000, 10000):
    T = "".join(random.choice("ab") for _ in range(n))
    P = "".join(random.choice("ab") for _ in range(n // 10))
    r.append(kmp_ops(T, swap(P)) / n)
check("Q3 KMP work is linear: ops/n bounded by 5", max(r) < 5, [round(x, 2) for x in r])
bind_text(3, "", 3, "O(n)", "Q3 complexity")

# ============================== Q4a: rope merging ==============================
def merge_cost(ropes, pick="min2"):
    a = list(ropes)
    total = 0
    if pick == "input":
        cur = a[0]
        for x in a[1:]:
            cur += x
            total += cur
        return total
    while len(a) > 1:
        a.sort()
        if pick == "min2":
            x, y = a[0], a[1]
            a = a[2:]
        elif pick == "max2":
            x, y = a[-1], a[-2]
            a = a[:-2]
        elif pick == "minmax":
            x, y = a[0], a[-1]
            a = a[1:-1]
        elif pick == "extractmax_first":      # the findbug variant: x is extracted with EXTRACT-MAX, y with EXTRACT-MIN
            x, y = a[-1], a[0]
            a = a[1:-1]
        total += x + y
        a.append(x + y)
    return total


def exhaustive(ropes):
    @lru_cache(None)
    def f(t):
        if len(t) == 1:
            return 0
        best = INF
        for i, j in itertools.combinations(range(len(t)), 2):
            rest = [t[k] for k in range(len(t)) if k not in (i, j)] + [t[i] + t[j]]
            best = min(best, t[i] + t[j] + f(tuple(sorted(rest))))
        return best
    return f(tuple(sorted(ropes)))


R = [4, 3, 2, 6]
check("Q4a example: greedy = exhaustive = 29", merge_cost(R) == exhaustive(R) == 29)
bind_numeric(4, "a", 0, 29, "Q4a total")
costs = []
a = sorted(R)
while len(a) > 1:
    x, y = a[0], a[1]
    a = sorted(a[2:] + [x + y])
    costs.append(x + y)
check("Q4a merge costs 5, 9, 15", costs == [5, 9, 15])
bind_numeric(4, "a", 1, costs[2], "Q4a last merge")
check("Q4a alternatives cost 38 / 34 / 31 on the example",
      (merge_cost(R, "max2"), merge_cost(R, "minmax"), merge_cost(R, "input")) == (38, 34, 31))
bind_first(4, "a", 2, "Q4a which ropes")
bad = 0
for _ in range(400):
    rr = [random.randint(1, 20) for _ in range(random.randint(2, 6))]
    bad += merge_cost(rr) != exhaustive(rr)
check("Q4a greedy == exhaustive minimum (400 random)", bad == 0)
check("Q4a findbug variant (EXTRACT-MAX for x) costs 34 on the example, not 29", merge_cost(R, "extractmax_first") == 34)
lines = step(4, "a", 4)["lines"]
check("Q4a findbug bugIndex points at the EXTRACT-MAX line", "EXTRACT-MAX" in lines[step(4, "a", 4)["bugIndex"]] and sum("EXTRACT-MAX" in l for l in lines) == 1)

# ============================== Q4b: exchange argument ==============================
def build_tree_cost(depths_f):
    return sum(f * d for f, d in depths_f)


T_leaves = {"x": (2, 1), "a": (3, 2), "b": (6, 3), "c": (7, 3)}
BT = sum(f * d for f, d in T_leaves.values())
T2 = dict(T_leaves)
T2["x"] = (T_leaves["x"][0], T_leaves["b"][1])
T2["b"] = (T_leaves["b"][0], T_leaves["x"][1])
BT2 = sum(f * d for f, d in T2.values())
check("Q4b example: B(T)=47, B(T')=39, difference 8 = (6-2)*(3-1)", (BT, BT2, BT - BT2) == (47, 39, 8) and (6 - 2) * (3 - 1) == 8)
bind_numeric(4, "b", 1, BT - BT2, "Q4b difference")
bad = 0
for _ in range(2000):
    fx, fb = random.randint(1, 9), random.randint(1, 9)
    dx, db = random.randint(1, 6), random.randint(1, 6)
    before = fx * dx + fb * db
    after = fx * db + fb * dx
    bad += (before - after) != (fb - fx) * (db - dx)
check("Q4b identity B(T)-B(T') = (f[b]-f[x])(d(b)-d(x)) on 2000 random values", bad == 0)
check("Q4b the difference is >= 0 whenever f[b]>=f[x] and d(b)>=d(x)",
      all((fb - fx) * (db - dx) >= 0 for fx in range(1, 6) for fb in range(fx, 8) for dx in range(1, 5) for db in range(dx, 6)))
ol, bug = step(4, "b", 2)["lines"], step(4, "b", 3)
diff = [i for i, (p, q) in enumerate(zip(ol, bug["lines"])) if p != q]
check("Q4b findbug: exactly one line changed, at bugIndex", diff == [bug["bugIndex"]] and len(ol) == len(bug["lines"]))
bind_first(4, "b", 0, "Q4b technique")

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
