# -*- coding: utf-8 -*-
"""Step-value checks for 22A-A (algorithms-1). Run: PYTHONUTF8=1 py -I tools/verify/22A-A/steps_22A-A.py
Recomputes every numeric / trace / complexity answer used in the guided steps, shows that every choice distractor
fails on some input, then binds the results to tools/raw/22A-A.json. ASCII output."""
import itertools, json, pathlib, random
from functools import lru_cache
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.loads((HERE.parents[1] / "raw" / "22A-A.json").read_text(encoding="utf-8"))
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


def item(num, part=""):
    for q in RAW["questions"]:
        if q["num"] == num and q.get("part", "") == part:
            return q
    raise KeyError((num, part))


def step(num, part, idx):
    return item(num, part)["steps"][idx]


def bind_numeric(num, part, idx, expected, label):
    s = step(num, part, idx)
    check(f"bind {label}: numeric step {idx} answer == recomputed {expected}", s["type"] == "numeric" and s["answer"] == expected)


def bind_text(num, part, idx, expected, label):
    s = step(num, part, idx)
    check(f"bind {label}: text step {idx} accepts {expected}", s["type"] == "text" and expected in s["accept"])


def bind_correct_is_first(num, part, idx, label):
    s = step(num, part, idx)
    check(f"bind {label}: choice step {idx} correct option is the verified one (id a)", s["type"] == "choice" and s["correctId"] == "a")


random.seed(5)

# ============================== Q1: LCS of three strings ==============================
def lcs3(S1, S2, S3, mode="ok"):
    @lru_cache(None)
    def f(i, j, l):
        if i == 0 or j == 0 or l == 0:
            return 0
        a, b, c = S1[i - 1], S2[j - 1], S3[l - 1]
        if mode == "ok":
            cond = a == b == c
        elif mode == "two":
            cond = (a == b) + (a == c) + (b == c) >= 1
        elif mode == "ab":
            cond = a == b
        elif mode == "always":
            cond = True
        else:
            cond = a == b == c
        if cond:
            return f(i - 1, j - 1, l - 1) + 1
        if mode == "max2":
            return max(f(i - 1, j, l), f(i, j - 1, l))
        if mode == "diag":
            return f(i - 1, j - 1, l - 1)
        if mode == "min3":
            return min(f(i - 1, j, l), f(i, j - 1, l), f(i, j, l - 1))
        return max(f(i - 1, j, l), f(i, j - 1, l), f(i, j, l - 1))
    return f(len(S1), len(S2), len(S3))


def subseqs(s):
    return {"".join(c for k, c in enumerate(s) if m >> k & 1) for m in range(1 << len(s))}


def brute3(S):
    return max(len(c) for c in subseqs(S[0]) & subseqs(S[1]) & subseqs(S[2]))


T = ("abcab", "bcbab", "cabba")
check("Q1 example LCS3 = 3 (recurrence == brute force)", lcs3(*T) == brute3(T) == 3)
bad = sum(lcs3(*S) != brute3(S) for S in (tuple("".join(random.choice("abc") for _ in range(random.randint(1, 6))) for _ in range(3)) for _ in range(300)))
check("Q1 recurrence vs brute force (300 random)", bad == 0)
inputs = [tuple("".join(random.choice("abc") for _ in range(random.randint(2, 6))) for _ in range(3)) for _ in range(400)]
for mode in ("two", "ab", "always", "max2", "diag", "min3"):
    check(f"Q1 distractor '{mode}' fails on some input", any(lcs3(*S, mode=mode) != brute3(S) for S in inputs))
bind_numeric(1, "", 0, lcs3(*T), "Q1")
bind_correct_is_first(1, "", 1, "Q1 match condition")
bind_correct_is_first(1, "", 2, "Q1 otherwise case")

# ============================== Q2: A = B^k iff KMP(A*A, A) >= 3 ==============================
def occ(text, pat):
    return sum(1 for i in range(len(text) - len(pat) + 1) if text[i:i + len(pat)] == pat)


def is_power(A):
    n = len(A)
    return any(n % d == 0 and A[:d] * (n // d) == A for d in range(1, n // 2 + 1))


A = "abbabbabbabb"
check("Q2 t(abbabbabbabb) = 5 and periodic", occ(A + A, A) == 5 and is_power(A))
check("Q2 t(abcab) = 2 and not periodic", occ("abcab" * 2, "abcab") == 2 and not is_power("abcab"))
bad_ge3 = bad_ge2 = bad_k3 = 0
for n in range(2, 13):
    for tup in itertools.product("ab", repeat=n):
        s = "".join(tup)
        t = occ(s + s, s)
        bad_ge3 += (t >= 3) != is_power(s)
        bad_ge2 += (t >= 2) != is_power(s)
check("Q2 t>=3 iff periodic for all binary strings up to length 12", bad_ge3 == 0)
check("Q2 distractor 't>=2' is wrong (it declares every string periodic)", bad_ge2 > 0 and all(occ(s + s, s) >= 2 for s in ("ab", "abc", "abcd")))
check("Q2 distractor 'needs k>=3' is wrong: abab has k=2, t=3", is_power("abab") and occ("abab" * 2, "abab") == 3)
bind_numeric(2, "", 0, 5, "Q2")
bind_numeric(2, "", 1, 2, "Q2")
bind_correct_is_first(2, "", 2, "Q2 threshold")


def kmp_count_ops(text, pat):
    pi = [0] * len(pat)
    ops = 0
    k = 0
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


ratios = []
for n in (100, 1000, 10000):
    s = "".join(random.choice("ab") for _ in range(n))
    ratios.append(kmp_count_ops(s + s, s) / n)
check("Q2 KMP work is linear in n (ops/n bounded by 9)", max(ratios) < 9, [round(r, 2) for r in ratios])
bind_text(2, "", 3, "O(n)", "Q2 complexity")

# ============================== Q3a/b: polynomial identity ==============================
P = lambda x: x * x - 10 * x + 21
G = lambda x: (x - 3) * (x - 5)
diff_count = sum(P(t) != G(t) for t in range(4))
check("Q3a example: P(t)!=G(t) for 3 of t in 0..3", diff_count == 3)
bind_numeric(3, "א", 0, diff_count, "Q3a")

# two different polynomials of degree <= n agree on at most n of the n+1 points 0..n
bad = 0
for _ in range(2000):
    n = random.randint(1, 6)
    d = [random.randint(-3, 3) for _ in range(n + 1)]   # difference polynomial, coefficients
    if not any(d):
        continue
    roots = sum(1 for t in range(n + 1) if sum(c * t ** e for e, c in enumerate(d)) == 0)
    bad += roots > n
check("Q3a a nonzero degree-<=n difference has at most n roots among 0..n (2000 random)", bad == 0)
check("Q3a distractor 'different polynomials never agree' is wrong (example agrees at t=3)", P(3) == G(3))
D = lambda t: t * (t - 1) * (t - 2)          # P-G for P=G+D, n=3
check("Q3a distractor 'differ in at least n of n+1 points': D differs only at t=3 of 0..3", sum(D(t) != 0 for t in range(4)) == 1)
bind_correct_is_first(3, "א", 1, "Q3a points")
check("Q3a order step has the 4 algorithm lines", len(step(3, "א", 2)["lines"]) == 4)


def run_alg(Pc, Gf, n, k, seed):
    rnd = random.Random(seed)
    rounds = 0
    for _ in range(k):
        rounds += 1
        t = rnd.randint(0, n)
        if sum(c * t ** e for e, c in enumerate(Pc)) != Gf(t):
            return False, rounds
    return True, rounds


# identical polynomials run all k rounds; clearly different ones stop early
n, k = 6, 10
coef = [1, 2, 3, 4, 5, 6]
Gid = lambda t: sum(c * t ** e for e, c in enumerate(coef))
res = [run_alg(coef, Gid, n, k, s) for s in range(50)]
check("Q3b identical polynomials: always k rounds and answer True", all(r == (True, k) for r in res))
Gdiff = lambda t: Gid(t) + 1
res2 = [run_alg(coef, Gdiff, n, k, s) for s in range(50)]
check("Q3b different polynomials: stops at round 1 (never all k rounds)", all(r == (False, 1) for r in res2))
check("Q3b with k<n identical polynomials still run exactly k rounds", run_alg(coef, Gid, 8, 3, 1) == (True, 3))
bind_correct_is_first(3, "ב", 0, "Q3b rounds")


def eval_ops(n):
    # evaluating G as a product of n linear factors: n subtractions + (n-1) multiplications; P by Horner: n mults + n adds
    return (n + (n - 1)) + 2 * n


rat = [eval_ops(n) * 7 / (7 * n) for n in (10, 100, 1000)]
check("Q3b work per round is Theta(n): ops/n between 2 and 5", all(2 <= r <= 5 for r in rat), rat)
bind_text(3, "ב", 1, "Θ(kn)", "Q3b complexity")

# ============================== Q4a/b: increasing representatives ==============================
def greedy(arrs):
    m = len(arrs)
    temp = max(arrs[-1])
    total = temp
    trace = [temp]
    for t in range(m - 2, -1, -1):
        c = [v for v in arrs[t] if v < temp]
        if not c:
            return 0, trace
        temp = max(c)
        total += temp
        trace.append(temp)
    return total, trace


def brute_best(arrs):
    best = None
    for idx in itertools.product(*[range(len(a)) for a in arrs]):
        vals = [arrs[t][i] for t, i in enumerate(idx)]
        if all(vals[t] < vals[t + 1] for t in range(len(vals) - 1)):
            s = sum(vals)
            best = s if best is None or s > best else best
    return 0 if best is None else best


def var_forward(arrs):
    temp = max(arrs[0])
    total = temp
    for t in range(1, len(arrs)):
        c = [v for v in arrs[t] if v > temp]
        if not c:
            return 0
        temp = max(c)
        total += temp
    return total


def var_smallest(arrs):
    temp = max(arrs[-1])
    total = temp
    for t in range(len(arrs) - 2, -1, -1):
        c = [v for v in arrs[t] if v < temp]
        if not c:
            return 0
        temp = min(c)
        total += temp
    return total


def var_unrestricted(arrs):
    return sum(max(a) for a in arrs)


EX = [[-3, -4, -8, -1], [20, 17, -8, 9], [-7, 4, 3, 19]]
tot, tr = greedy(EX)
check("Q4a example: greedy = 35 = brute force, trace 19,17,-1", tot == brute_best(EX) == 35 and tr == [19, 17, -1])
bind_numeric(4, "א", 0, tr[1], "Q4a TEMPMAX after A_2")
bind_numeric(4, "א", 1, tot, "Q4a total")
bad = 0
cases = []
for _ in range(3000):
    m = random.randint(1, 4)
    arrs = [[random.randint(-6, 12) for _ in range(random.randint(1, 4))] for _ in range(m)]
    cases.append(arrs)
    bad += greedy(arrs)[0] != brute_best(arrs)
check("Q4a greedy equals brute force on 3000 random inputs", bad == 0)
for name, fn in (("forward", var_forward), ("smallest", var_smallest), ("unrestricted", var_unrestricted)):
    check(f"Q4a distractor '{name}' fails on some input", any(fn(a) != brute_best(a) for a in cases))
bind_correct_is_first(4, "א", 2, "Q4a rule")
NONE = [[4, 5], [1, 3], [2]]
check("Q4a no increasing selection -> 0 (greedy and brute force)", greedy(NONE)[0] == 0 == brute_best(NONE))
bind_numeric(4, "א", 3, 0, "Q4a none")

# Q4b: greedy choice property and the example
opt_with_max = 0
for arrs in cases:
    best = brute_best(arrs)
    if best == 0:
        continue
    mx = max(arrs[-1])
    found = False
    for idx in itertools.product(*[range(len(a)) for a in arrs]):
        vals = [arrs[t][i] for t, i in enumerate(idx)]
        if all(vals[t] < vals[t + 1] for t in range(len(vals) - 1)) and sum(vals) == best and vals[-1] == mx:
            found = True
            break
    opt_with_max += not found
check("Q4b some optimal solution always uses MAX of A_m (greedy choice, 3000 random)", opt_with_max == 0)
opts = [vals for vals in itertools.product(*EX) if all(vals[t] < vals[t + 1] for t in range(2)) and sum(vals) == 35]
check("Q4b example: unique optimal solution (-1,17,19)", opts == [(-1, 17, 19)])
bind_numeric(4, "ב", 1, opts[0][-1], "Q4b")
# findbug line differs from the true line in exactly one place, order lines are the true ones
ol, bug = step(4, "ב", 2)["lines"], step(4, "ב", 3)
diff = [i for i, (a, b) in enumerate(zip(ol, bug["lines"])) if a != b]
check("Q4b findbug: exactly one line changed, at bugIndex", diff == [bug["bugIndex"]] and len(ol) == len(bug["lines"]))

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
