# -*- coding: utf-8 -*-
"""Step-value checks for 25A-C (algorithms-1). Run: PYTHONUTF8=1 py -I tools/verify/25A-C/steps_25A-C.py
Recomputes every numeric / trace / complexity answer used in the guided steps and shows that every choice /
fillblank / findbug distractor fails on some input; then binds the numbers to tools/raw/25A-C.json. ASCII output."""
import itertools, json, pathlib, random, math
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.loads((HERE.parents[1] / "raw" / "25A-C.json").read_text(encoding="utf-8"))
ok = True
V = {}
random.seed(3)


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


# ============================== Q1: alignment distance ==============================
def opt(S1, S2, match_cost=0, variant="ok"):
    n, m = len(S1), len(S2)
    T = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        T[i][0] = i
    for j in range(m + 1):
        T[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if S1[i - 1] == S2[j - 1]:
                if variant == "ok":
                    T[i][j] = T[i - 1][j - 1]
                elif variant == "plus1":
                    T[i][j] = 1 + T[i - 1][j - 1]
                elif variant == "gaps_only":
                    T[i][j] = min(T[i - 1][j], T[i][j - 1])
            else:
                T[i][j] = 1 + min(T[i - 1][j - 1], T[i - 1][j], T[i][j - 1])
    return T


def brute(S1, S2):
    """min distance over every alignment (all ways to insert '-')."""
    n, m = len(S1), len(S2)
    best = 10 ** 9
    for L in range(max(n, m), n + m + 1):
        for g1 in itertools.combinations(range(L), L - n):
            T1 = []
            it = iter(S1)
            for k in range(L):
                T1.append("-" if k in g1 else next(it))
            for g2 in itertools.combinations(range(L), L - m):
                it2 = iter(S2)
                T2 = ["-" if k in g2 else next(it2) for k in range(L)]
                best = min(best, sum(a != b for a, b in zip(T1, T2)))
    return best


S1, S2 = "AGCTTACG", "ACTTAACG"
T = opt(S1, S2)
check("Q1 OPT(8,8) == 2", T[8][8] == 2)
V["q1_full"] = T[8][8]
V["q1_33"] = T[3][3]
check("Q1 OPT(3,3) for AGC vs ACT is " + str(T[3][3]) + " == brute force", T[3][3] == brute("AGC", "ACT"))
for _ in range(150):
    a = "".join(random.choice("AC") for _ in range(random.randint(0, 4)))
    b = "".join(random.choice("AC") for _ in range(random.randint(0, 4)))
    assert opt(a, b)[len(a)][len(b)] == brute(a, b)
check("Q1 recurrence == brute force on 150 random pairs", True)
check("Q1 distractor '1 + OPT(i-1,j-1)' on equal chars fails (A vs A)", opt("A", "A", variant="plus1")[1][1] == 1 != 0)
check("Q1 distractor 'min of the two gap cells' on equal chars fails (A vs A)", opt("A", "A", variant="gaps_only")[1][1] == 1 != 0)
check("Q1 base: OPT(0,j)=j", all(opt("", "ACGT"[:j])[0][j] == j for j in range(5)))
V["q1_cells"] = (8 + 1) * (8 + 1)


def two_rows(S1, S2):
    prev = list(range(len(S2) + 1))
    for i in range(1, len(S1) + 1):
        cur = [i] + [0] * len(S2)
        for j in range(1, len(S2) + 1):
            cur[j] = prev[j - 1] if S1[i - 1] == S2[j - 1] else 1 + min(prev[j - 1], prev[j], cur[j - 1])
        prev = cur
    return prev[-1]


check("Q1b two-row DP == full table", all(
    two_rows(a, b) == opt(a, b)[len(a)][len(b)]
    for a, b in [("".join(random.choice("ACGT") for _ in range(random.randint(0, 9))),
                  "".join(random.choice("ACGT") for _ in range(random.randint(0, 9)))) for _ in range(300)]))

# ============================== Q2: fractional knapsack ==============================
def greedy(val, wt, cap, key):
    tot = Fraction(0)
    for i in sorted(range(len(val)), key=key):
        take = min(wt[i], cap)
        tot += Fraction(val[i] * take, wt[i])
        cap -= take
    return tot


def exact(val, wt, cap):
    n = len(val)
    best = Fraction(0)
    for mask in range(1 << n):
        w = sum(wt[i] for i in range(n) if mask >> i & 1)
        if w > cap:
            continue
        v = sum(val[i] for i in range(n) if mask >> i & 1)
        room = cap - w
        extra = max([Fraction(val[i] * min(wt[i], room), wt[i]) for i in range(n) if not mask >> i & 1] + [Fraction(0)])
        best = max(best, v + extra)
    return best


val, wt = [60, 100, 120], [10, 20, 30]
ratio = lambda val, wt: (lambda i: -Fraction(val[i], wt[i]))
check("Q2 example 240", greedy(val, wt, 50, ratio(val, wt)) == 240)
V["q2_total"] = 240
V["q2_part"] = 80
check("Q2 third item part: 20/30 * 120 = 80", Fraction(20, 30) * 120 == 80)
# eps shift gain: ratios 6 and 4, move 5 units
V["q2_gain"] = 5 * (6 - 4)
check("Q2 exchange: moving 5 units from ratio 4 to ratio 6 gains 10", V["q2_gain"] == 10)
for _ in range(1500):
    n = random.randint(1, 5)
    v = [random.randint(1, 20) for _ in range(n)]
    w = [random.randint(1, 10) for _ in range(n)]
    c = random.randint(1, sum(w) + 3)
    assert greedy(v, w, c, ratio(v, w)) == exact(v, w, c)
check("Q2 ratio greedy == exact optimum (1500 random)", True)
found = {"value": None, "weight": None, "heavy": None}
for _ in range(20000):
    n = random.randint(2, 4)
    v = [random.randint(1, 20) for _ in range(n)]
    w = [random.randint(1, 10) for _ in range(n)]
    c = random.randint(1, sum(w))
    g = greedy(v, w, c, ratio(v, w))
    if found["value"] is None and greedy(v, w, c, lambda i: -v[i]) < g:
        found["value"] = (v, w, c)
    if found["weight"] is None and greedy(v, w, c, lambda i: w[i]) < g:
        found["weight"] = (v, w, c)
    if found["heavy"] is None and greedy(v, w, c, lambda i: -w[i]) < g:
        found["heavy"] = (v, w, c)
check("Q2 distractors (highest value, lowest weight, highest weight) each lose on some input", all(found.values()), found)

# ============================== Q3: rotated array ==============================
def search(nums, t, lo, hi, cnt, variant="ok"):
    cnt[0] += 1
    if cnt[0] > 500:
        raise RecursionError
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if nums[mid] == t:
        return mid
    if nums[lo] <= nums[mid]:
        cond = nums[lo] <= t < nums[mid]
        if variant == "bug_cond":
            cond = nums[lo] <= t <= nums[hi]
        if cond:
            return search(nums, t, lo, mid - 1, cnt, variant)
        r = {"ok": (mid + 1, hi), "bug_cond": (mid + 1, hi), "mid_hi": (mid, hi), "mid1_hi1": (mid + 1, hi - 1),
             "lo_mid": (lo, mid)}[variant]
        return search(nums, t, r[0], r[1], cnt, variant)
    else:
        if nums[mid] < t <= nums[hi]:
            return search(nums, t, mid + 1, hi, cnt, variant)
        return search(nums, t, lo, mid - 1, cnt, variant)


nums = [4, 5, 6, 7, 0, 1, 2]
cnt = [0]
check("Q3 example index 4", search(nums, 0, 0, 6, cnt) == 4)
V["q3_calls"] = cnt[0]
check("Q3 example uses 3 calls", cnt[0] == 3, cnt)
V["q3_mid0"] = (0 + 6) // 2
# max calls for n = 1000 over all rotations and targets
maxc = 0
base = list(range(0, 2000, 2))[:1000]
for r in range(1000):
    arr = base[r:] + base[:r]
    for t in list(range(-1, 2000, 7)):
        c = [0]
        res = search(arr, t, 0, 999, c)
        assert res == (arr.index(t) if t in arr else -1)
        maxc = max(maxc, c[0])
check("Q3 correct on 1000 rotations x targets; calls <= floor(log2 n)+2", maxc <= math.floor(math.log2(1000)) + 2, maxc)
V["q3_maxcalls"] = maxc


def run_variant(variant):
    for _ in range(3000):
        n = random.randint(1, 8)
        s = sorted(random.sample(range(20), n))
        r = random.randrange(n)
        arr = s[r:] + s[:r]
        t = random.randint(-1, 21)
        try:
            res = search(arr, t, 0, n - 1, [0], variant)
        except RecursionError:
            return True
        if res != (arr.index(t) if t in arr else -1):
            return True
    return False


check("Q3 variant 'mid, hi' hangs on some input", run_variant("mid_hi"))
check("Q3 variant 'mid+1, hi-1' wrong on some input", run_variant("mid1_hi1"))
check("Q3 variant 'lo, mid' hangs or is wrong", run_variant("lo_mid"))
check("Q3 findbug variant (t <= nums[hi] instead of t < nums[mid]) is wrong", run_variant("bug_cond"))
# which-half-sorted criteria
bad1 = bad2 = False
for _ in range(3000):
    n = random.randint(3, 9)
    s = sorted(random.sample(range(30), n))
    r = random.randrange(n)
    a = s[r:] + s[:r]
    lo, hi = 0, n - 1
    mid = (lo + hi) // 2
    left_sorted = all(a[i] < a[i + 1] for i in range(lo, mid))
    if (a[lo] <= a[mid]) != left_sorted:
        raise SystemExit("official criterion wrong")
    if (a[mid] < a[hi]) != left_sorted:
        bad1 = True
    if (a[lo] < a[hi]) != left_sorted:
        bad2 = True
check("Q3 criterion nums[lo]<=nums[mid] is exact; 'nums[mid]<nums[hi]' and 'nums[lo]<nums[hi]' are not", bad1 and bad2)

# ============================== Q4: hidden string ==============================
def pi_fn(P):
    pi = [0] * len(P)
    k = 0
    for i in range(1, len(P)):
        while k and P[k] != P[i]:
            k = pi[k - 1]
        if P[k] == P[i]:
            k += 1
        pi[i] = k
    return pi


def kmp_find(T, P):
    pi = pi_fn(P)
    q = 0
    falls = 0
    maxper = 0
    for i, ch in enumerate(T):
        c0 = falls
        while q and P[q] != ch:
            q = pi[q - 1]
            falls += 1
        if P[q] == ch:
            q += 1
        maxper = max(maxper, falls - c0)
        if q == len(P):
            return i - len(P) + 2, falls, maxper     # 1-based start
    return -1, falls, maxper


check("Q4 'abc' hides in 'dfzcbau', reversed 'cba' found at 1-based index 4", kmp_find("dfzcbau", "cba")[0] == 4)
V["q4_start"] = 4
R = "abaab"[::-1]
V["q4_pi"] = pi_fn(R)[-1]
check("Q4 pi of reverse('abaab')='baaba' ends with 2", pi_fn(R) == [0, 0, 0, 1, 2], pi_fn(R))
for _ in range(20000):
    T = "".join(random.choice("ab") for _ in range(random.randint(2, 12)))
    P = "".join(random.choice("ab") for _ in range(random.randint(1, len(T) - 1)))
    assert (kmp_find(T, P[::-1])[0] != -1) == (P[::-1] in T)
check("Q4 KMP(T, reverse P) == hides, 20000 random", True)
check("Q4 distractor 'search P in T' fails on abc/dfzcbau", "abc" not in "dfzcbau")
check("Q4 distractor 'reverse P in reverse T' == 'P in T' fails on abc/dfzcbau", ("cba" in "uabczfd") is False)
sub = lambda a, b: all(c in iter(b) for c in a)
check("Q4 distractor 'reverse P is a subsequence of T' fails: P=ab, T=bxa (ba subsequence, not substring)",
      sub("ba", "bxa") and "ba" not in "bxa")
mx_total_ok = True
multi = False
for _ in range(20000):
    n = random.randint(2, 30)
    T = "".join(random.choice("ab") for _ in range(n))
    P = "".join(random.choice("ab") for _ in range(random.randint(1, n - 1)))
    _, falls, maxper = kmp_find(T, P)
    mx_total_ok &= falls <= n
    multi |= maxper > 1
check("Q4 total fallbacks <= n always; a single text character can cause several fallbacks", mx_total_ok and multi)


# ---------------------------------------------------------------- bind numbers to raw JSON
def find(num, part=""):
    for q in RAW["questions"]:
        if q["num"] == num and q.get("part", "") == part:
            return q
    raise KeyError((num, part))


def nums_of(num, part):
    return [s["answer"] for s in find(num, part).get("steps", []) if s["type"] == "numeric"]


def texts_of(num, part):
    return [s["accept"] for s in find(num, part).get("steps", []) if s["type"] == "text"]


check("bind Q1a", nums_of(1, "א") == [V["q1_33"], V["q1_full"]], nums_of(1, "א"))
check("bind Q1b numeric", nums_of(1, "ב") == [V["q1_cells"]])
check("bind Q1b text", [("O(n1n2)" in a) for a in texts_of(1, "ב")][0] and any("O(min(n1,n2))" in a for a in texts_of(1, "ב")))
check("bind Q2a", nums_of(2, "א") == [V["q2_part"], V["q2_total"]], nums_of(2, "א"))
check("bind Q2a text", any("O(nlogn)" in a or "O(n log n)" in a for a in texts_of(2, "א")))
check("bind Q2b", nums_of(2, "ב") == [V["q2_gain"]], nums_of(2, "ב"))
check("bind Q3a", nums_of(3, "א") == [V["q3_calls"]], nums_of(3, "א"))
check("bind Q3b", nums_of(3, "ב") == [V["q3_maxcalls"]], nums_of(3, "ב"))
check("bind Q3b text", any("O(log n)" in a for a in texts_of(3, "ב")))
check("bind Q4a", nums_of(4, "א") == [V["q4_pi"], V["q4_start"]], nums_of(4, "א"))
check("bind Q4b text", len(texts_of(4, "ב")) == 2 and "O(n)" in texts_of(4, "ב")[0] and "O(m)" in texts_of(4, "ב")[1])
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
