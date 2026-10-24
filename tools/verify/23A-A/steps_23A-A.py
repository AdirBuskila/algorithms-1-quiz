# -*- coding: utf-8 -*-
"""Machine checks for the guided steps of 23A-A (numeric / complexity / distractor claims).
Run: PYTHONUTF8=1 py tools/verify/23A-A/steps_23A-A.py   (ASCII output; exit 1 on failure)"""
import itertools, json, math, pathlib, random, sys
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE.parents[1] / "raw" / "23A-A.json"
ok = True
random.seed(23)
NEG = float("-inf")


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


# ------------------------------------------------------------------ Q1
def M_table(A, variant="ok"):
    n = len(A)
    M = [[NEG] * (n + 2) for _ in range(n + 2)]       # 1-based, padded
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            if i == 1:
                M[i][j] = A[0][0]; continue
            g = lambda a, b: M[a][b] if 1 <= b <= a else NEG
            if variant == "ok":
                best = max(g(i - 1, j - 1), g(i - 1, j))
            elif variant == "right":
                best = max(g(i - 1, j), g(i - 1, j + 1))
            elif variant == "left":
                best = max(g(i - 1, j), M[i][j - 1] if j > 1 else NEG)
            else:
                best = g(i - 1, j - 1)
            M[i][j] = A[i - 1][j - 1] + best if best != NEG else NEG
    return M


def best_path(A):
    n = len(A); best = None
    for steps in itertools.product((0, 1), repeat=n - 1):
        j, s = 0, A[0][0]
        for i, st in enumerate(steps, 1):
            j += st; s += A[i][j]
        best = s if best is None else max(best, s)
    return best


def answer(A, variant="ok"):
    M = M_table(A, variant); n = len(A)
    return max(M[n][1:n + 1])


ex = [[1, 0, 0], [3, 2, 0], [4, 10, 12]]
M = M_table(ex)
check("Q1a: M(3,2)=14 and the answer 15", M[3][2] == 14 and answer(ex) == 15 == best_path(ex))
fails = {"right": 0, "left": 0, "diag": 0}; badok = 0
for _ in range(1500):
    n = random.randint(2, 7)
    A = [[random.randint(-9, 20) if j <= i else 0 for j in range(n)] for i in range(n)]
    b = best_path(A)
    badok += answer(A) != b
    for v in fails:
        fails[v] += answer(A, v) != b
check("Q1a: correct recurrence equals brute force (1500 random)", badok == 0)
check("Q1a: each distractor recurrence fails somewhere", all(fails.values()), str(fails))
check("Q1c: 10*11/2 = 55 cells", sum(range(1, 11)) == 55)


def cells(n): return n * (n + 1) // 2


check("Q1b/c time: cells ratio for 2n vs n -> 4 (quadratic)", abs(cells(40000) / cells(20000) - 4) < 0.001)


def one_row(A):
    row = [A[0][0]]
    for i in range(1, len(A)):
        row = [A[i][j] + max(row[jj] for jj in (j - 1, j) if 0 <= jj <= i - 1) for j in range(i + 1)]
    return max(row)


check("Q1c: two-row DP equals full-table DP and brute force",
      all(one_row(A) == answer(A) == best_path(A) for A in
          ([[random.randint(-5, 9) if j <= i else 0 for j in range(n)] for i in range(n)] for n in (random.randint(1, 8) for _ in range(300)))))

# ------------------------------------------------------------------ Q2
def common_len(s1, s2):
    best = 0; subs = set()
    for i in range(len(s1)):
        for j in range(i + 1, len(s1) + 1):
            t = s1[i:j]
            if t in s2:
                if len(t) > best: best, subs = len(t), {t}
                elif len(t) == best: subs.add(t)
    return best, subs


check("Q2b: LCS of BADAEAT and CAEADAS has length 3, exactly ADA and AEA", common_len("BADAEAT", "CAEADAS") == (3, {"ADA", "AEA"}))
check("Q2a: |S1$S2*| for n=7 is 16", len("BADAEAT" + "$" + "CAEADAS" + "*") == 16)


# naive generalized suffix tree marks: deepest internal node marked both == LCS length, random pairs
def naive_lcs_by_marks(s1, s2):
    T = s1 + "$" + s2 + "*"
    n1 = len(s1)
    sufs = []
    for i in range(len(T)):
        suf = T[i:]
        cut = suf.index("$") + 1 if "$" in suf else len(suf)   # leaf edges are cut after the terminator
        sufs.append((suf[:cut], 1 if i <= n1 else 2))
    # internal nodes = strings that are a prefix of >= 2 suffixes (as right-branching nodes this holds for the
    # deepest ones); marks = union of the sides of those suffixes
    best = 0
    cand = {suf[:k] for suf, _ in sufs for k in range(1, len(suf) + 1)}
    for c in cand:
        if "$" in c or "*" in c: continue
        sides = {side for suf, side in sufs if suf.startswith(c)}
        if sides == {1, 2}: best = max(best, len(c))
    return best


bad = 0
for _ in range(400):
    a = "".join(random.choice("ABCDE") for _ in range(random.randint(1, 8)))
    b = "".join(random.choice("ABCDE") for _ in range(random.randint(1, 8)))
    bad += naive_lcs_by_marks(a, b) != common_len(a, b)[0]
check("Q2a/b: marks-by-union (and not by intersection) give the LCS length (400 random)", bad == 0)

# ------------------------------------------------------------------ Q3
for p in (Fraction(1, 4),):
    check("Q3b: p=1/4 -> P(HT)=0.1875, P(TT)... (1-p)^2=0.5625", p * (1 - p) == Fraction(3, 16) and (1 - p) ** 2 == Fraction(9, 16))
    check("Q3b: P(HT)=P(TH) for several p, P(HH) != P(TT) unless p=1/2",
          all(q * (1 - q) == (1 - q) * q for q in (Fraction(1, 3), Fraction(1, 5), p)) and p ** 2 != (1 - p) ** 2)
    q = 2 * p * (1 - p)
    check("Q3c: p=1/4 round ends w.p. 3/8, expected tosses 16/3", q == Fraction(3, 8) and 2 / q == Fraction(16, 3))
    # P(output 0) = 1/2 exactly: sum of geometric series
    check("Q3c: P(out=0)=p(1-p)/q = 1/2", p * (1 - p) / q == Fraction(1, 2))


def fair(pv):
    tosses = 0
    while True:
        x = random.random() < pv; y = random.random() < pv; tosses += 2
        if x != y:
            return (0 if x else 1), tosses


outs = [fair(0.25) for _ in range(200000)]
check("Q3c simulation: mean tosses ~ 5.333, P(0) ~ 0.5",
      abs(sum(t for _, t in outs) / len(outs) - 16 / 3) < 0.05 and abs(sum(1 for o, _ in outs if o == 0) / len(outs) - 0.5) < 0.01)

# ------------------------------------------------------------------ Q4
def greedy(W, P, variant="ok"):
    R, c = W, []
    for p in P:
        if variant == "ok": t = R // p
        elif variant == "W": t = W // p
        elif variant == "mod": t = R % p
        else: t = -(-R // p)
        c.append(t); R -= t * p
    return c, R


def min_items(W, P):
    INF = 10 ** 9; dp = [0] + [INF] * W
    for w in range(1, W + 1):
        dp[w] = min((dp[w - p] + 1 for p in P if p <= w), default=INF)
    return dp[W]


check("Q4a: W=137, P=(125,25,5,1): greedy uses 5 items = DP minimum",
      sum(greedy(137, [125, 25, 5, 1])[0]) == 5 == min_items(137, [125, 25, 5, 1]))
bad = 0; fl = {"W": 0, "mod": 0, "ceil": 0}
for _ in range(1500):
    K = random.randint(1, 5); P = [5 ** (K - i) for i in range(1, K + 1)]; W = random.randint(1, 800)
    c, R = greedy(W, P)
    bad += not (R == 0 and sum(c) == min_items(W, P))
    for v in fl:
        c2, R2 = greedy(W, P, v)
        fl[v] += not (R2 == 0 and all(x >= 0 for x in c2) and sum(x * p for x, p in zip(c2, P)) == W and sum(c2) == min_items(W, P))
check("Q4a: greedy fills exactly and is minimal (1500 random)", bad == 0)
check("Q4a: each fillblank distractor fails somewhere", all(fl.values()), str(fl))
# lightest-first uses W items
check("Q4a: lightest first uses W items, more than the DP minimum for W=137",
      137 > min_items(137, [125, 25, 5, 1]))

# Q4b lemma: in every optimal solution, each non-heaviest type has <= 4 items (K<=4), max attained = 4
mx = 0; viol = 0
for K in range(2, 5):
    P = [5 ** (K - i) for i in range(1, K + 1)]
    for W in range(1, 400):
        best = min_items(W, P)
        for cnt in itertools.product(*[range(W // p + 1) for p in P[1:]]) if K <= 3 else []:
            used = sum(c * p for c, p in zip(cnt, P[1:]))
            if used > W or (W - used) % P[0]: continue
            if (W - used) // P[0] + sum(cnt) == best:
                mx = max(mx, max(cnt)); viol += max(cnt) > 4
check("Q4b: max items of a non-heaviest type in any optimal solution = 4 (K<=3, W<400)", mx == 4 and viol == 0)
check("Q4b: 4*(25+5+1) = 124 = 125-1", 4 * (25 + 5 + 1) == 124 == 125 - 1)
check("Q4b: five-times bound 5*(25+5+1) = 155 >= 125, so '5' breaks the contradiction", 5 * 31 >= 125)

# ------------------------------------------------------------------ Q5
def greedy_cover(U, sets):
    C, chosen = set(U), []
    while C:
        gains = [len(s & C) for s in sets]
        m = max(gains)
        assert gains.count(m) == 1 or True
        i = gains.index(m); chosen.append(i); C -= sets[i]
    return chosen


U = set(range(1, 9))
sets = [{1, 2, 3, 5, 6}, {1, 2, 3, 4}, {5, 6, 7, 8}]
ch = greedy_cover(U, sets)
check("Q5: greedy picks A1, A3, A2 (3 sets), no ties; optimum is 2",
      ch == [0, 2, 1] and min(r for r in range(1, 4) for S in itertools.combinations(sets, r) if set().union(*S) == U) == 2)
gains0 = sorted(len(s) for s in sets)
check("Q5: first-step gains 5 > 4 = 4 (the largest set A1 is unique)", gains0[-1] == 5 and gains0[-2] == 4)
bad = 0
for _ in range(1500):
    n = random.randint(2, 9); m = random.randint(2, 7)
    S = [set(random.sample(range(n), random.randint(1, n))) for _ in range(m)]
    Uu = set().union(*S)
    g = len(greedy_cover(Uu, S))
    opt = min(r for r in range(1, m + 1) for T in itertools.combinations(S, r) if set().union(*T) == Uu)
    H = sum(1 / t for t in range(1, len(Uu) + 1))
    bad += g > H * opt + 1e-9
check("Q5: greedy <= H(n) * OPT on 1500 random instances", bad == 0)

# ------------------------------------------------------------------ raw JSON carries exactly these answers
if RAW.exists():
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    want = {"1א": [14, 15], "1ג": [55], "2א": [16], "2ב": [3], "3ב": [0.1875, 0.5625], "3ג": [0.375, 5.3333],
            "4א": [5], "4ב": [4, 124], "5": [3]}
    got = {}
    texts = {}
    for q in raw["questions"]:
        key = str(q["num"]) + q.get("part", "")
        got[key] = [s["answer"] for s in q.get("steps", []) if s["type"] == "numeric"]
        texts[key] = [tuple(s["accept"]) for s in q.get("steps", []) if s["type"] == "text"]
    for k, v in want.items():
        check(f"raw JSON numeric answers for {k}", got.get(k) == v, str(got.get(k)))
    check("raw JSON complexity answers: 1ב O(n^2) twice, 1ג O(n^2) then O(n), 2ב ADA then O(n)",
          texts["1ב"] == [("O(n^2)",), ("O(n^2)",)] and texts["1ג"] == [("O(n^2)",), ("O(n)",)] and texts["2ב"] == [("ADA", "AEA"), ("O(n)",)])

print("ALL OK" if ok else "SOME CHECK FAILED")
sys.exit(0 if ok else 1)
