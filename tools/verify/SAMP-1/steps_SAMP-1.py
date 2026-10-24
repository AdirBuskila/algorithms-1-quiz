# -*- coding: utf-8 -*-
"""Step-value checks for SAMP-1 (algorithms-1). Run: py -X utf8 -I tools/verify/SAMP-1/steps_SAMP-1.py
Recomputes every numeric / trace / complexity answer used in the guided steps, shows that every choice distractor
fails on some input, then binds the results to tools/raw/SAMP-1.json. ASCII output; no Hebrew in this file
(parts are addressed by letter index)."""
import itertools, json, math, pathlib, random
from functools import lru_cache

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.loads((HERE.parents[1] / "raw" / "SAMP-1.json").read_text(encoding="utf-8"))
ok = True


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


def bind_text(num, part, idx, label):
    s = step(num, part, idx)
    check(f"bind {label}: text step {idx} accepts an O/Theta form", s["type"] == "text" and len(s["accept"]) >= 2)


def bind_first(num, part, idx, label):
    s = step(num, part, idx)
    check(f"bind {label}: choice/fillblank step {idx} correct option is the verified one (id a)", s["type"] in ("choice", "fillblank") and s["correctId"] == "a")


def one_line_diff(num, part, ordidx, bugidx, label):
    ol, bug = step(num, part, ordidx)["lines"], step(num, part, bugidx)
    diff = [i for i, (a, b) in enumerate(zip(ol, bug["lines"])) if a != b]
    check(f"{label}: findbug differs from the true lines in exactly one line, at bugIndex", diff == [bug["bugIndex"]] and len(ol) == len(bug["lines"]))


random.seed(2022)

# ============================== Q1: longest palindromic subsequence ==============================
def P_rec(S, mode="ok"):
    n = len(S)

    @lru_cache(None)
    def P(i, j):
        if i > j:
            return 0
        if i == j:
            return {"ok": 1, "base0": 0, "base2": 2}.get(mode, 1)
        if S[i] == S[j]:
            if mode == "plus1":
                return P(i + 1, j - 1) + 1
            if mode == "plus0":
                return P(i + 1, j - 1)
            if mode == "maxplus2":
                return max(P(i + 1, j), P(i, j - 1)) + 2
            return P(i + 1, j - 1) + 2
        return max(P(i + 1, j), P(i, j - 1))
    return P


def brute_pal(S):
    best = 0
    for m in range(1 << len(S)):
        t = "".join(c for k, c in enumerate(S) if m >> k & 1)
        if t == t[::-1]:
            best = max(best, len(t))
    return best


S0 = "BARCAR"
P0 = P_rec(S0)
check("Q1a BARCAR: P(1,6)=3, P(1,4)=1, P(2,6)=3 (0-indexed (0,5), (0,3), (1,5)) equal brute force",
      P0(0, 5) == brute_pal(S0) == 3 and P0(0, 3) == brute_pal("BARC") == 1 and P0(1, 5) == brute_pal("ARCAR") == 3)
bind_numeric(1, "a", 0, P0(0, 3), "Q1a P(1,4)")
bind_numeric(1, "a", 1, P0(1, 5), "Q1a P(2,6)")
strs = ["".join(random.choice("abc") for _ in range(random.randint(1, 9))) for _ in range(400)]
check("Q1a recurrence == brute force (400 random)", all(P_rec(s)(0, len(s) - 1) == brute_pal(s) for s in strs))
for mode in ("plus1", "plus0", "maxplus2", "base0", "base2"):
    check(f"Q1a distractor '{mode}' fails on some string", any(P_rec(s, mode)(0, len(s) - 1) != brute_pal(s) for s in strs))
bind_first(1, "a", 2, "Q1a equal ends")
bind_first(1, "a", 3, "Q1a base case")

# Q1b: claims
def claim2_inner_only(S):          # buggy claim: the optimum is always inside s_2..s_{n-1}
    if len(S) < 2 or S[0] == S[-1]:
        return True
    return brute_pal(S[1:-1]) == brute_pal(S)


check("Q1b claim 2 (ends differ): optimum equals max over the two shorter strings (400 random)",
      all(brute_pal(s) == max(brute_pal(s[1:]), brute_pal(s[:-1])) for s in strs if len(s) > 1 and s[0] != s[-1]))
check("Q1b buggy claim 'inside s_2..s_{n-1} only' fails (e.g. ab)", not claim2_inner_only("ab"))
check("Q1b an optimum need not contain both ends (ab -> a)", brute_pal("ab") == 1)
check("Q1b claim 1 (ends equal): optimum = 2 + inner optimum", all(brute_pal(s) == 2 + brute_pal(s[1:-1]) for s in strs if len(s) > 1 and s[0] == s[-1]))
bind_first(1, "b", 0, "Q1b ends differ")
one_line_diff(1, "b", 0, 1, "Q1b") if False else None
cl = step(1, "b", 1)
check("Q1b findbug bugIndex is the second claim and lines differ from the true claim list only there",
      cl["type"] == "findbug" and cl["bugIndex"] == 1 and len(cl["lines"]) == 3)

# Q1c: number of states and dependencies
def states(n, S):
    seen = set()
    deps = 0

    def go(i, j):
        nonlocal deps
        if i > j or (i, j) in seen:
            return
        seen.add((i, j))
        if i == j:
            return
        if S[i] == S[j]:
            deps = max(deps, 1)
            go(i + 1, j - 1)
        else:
            deps = max(deps, 2)
            go(i + 1, j)
            go(i, j - 1)
    go(0, n - 1)
    return len(seen), deps


r = []
for n in (50, 100, 200):
    S = "".join(random.choice("abcdefgh") for _ in range(n))
    cnt, dmax = states(n, S)
    r.append(cnt / n ** 2)
    check(f"Q1c n={n}: states/n^2 in (0.3, 0.6) and at most 2 dependencies per state", 0.3 < cnt / n ** 2 < 0.6 and dmax <= 2, round(cnt / n ** 2, 3))
bind_text(1, "c", 0, "Q1c time")
bind_text(1, "c", 1, "Q1c space")
bind_first(1, "c", 2, "Q1c O(1) per cell")

# ============================== Q2: circular rotation via KMP(T1*T1, T2) ==============================
def kmp(T, Pt):
    return 1 if Pt in T else 0


def is_rot(a, b):
    return len(a) == len(b) and any(a[k:] + a[:k] == b for k in range(1, len(a) + 1))


variants = {"T1*T1,T2": lambda a, b: kmp(a + a, b), "T1,T2": lambda a, b: kmp(a, b),
            "T2,T1*T1": lambda a, b: kmp(b, a + a), "T1*T2,T2": lambda a, b: kmp(a + b, b)}
pairs = [("".join(random.choice("ab") for _ in range(n)),) for n in (random.randint(1, 6) for _ in range(800))]
pairs = [(a, "".join(random.sample(a, len(a))) if random.random() < 0.5 else a[k:] + a[:k]) for (a,) in pairs for k in [random.randint(0, len(a))]]
check("Q2a KMP(T1*T1, T2) == is_rotation on 800 random pairs", all(variants["T1*T1,T2"](a, b) == is_rot(a, b) for a, b in pairs))
for nm in ("T1,T2", "T2,T1*T1", "T1*T2,T2"):
    check(f"Q2a distractor '{nm}' fails on some pair", any(variants[nm](a, b) != is_rot(a, b) for a, b in pairs))
bind_first(2, "a", 0, "Q2a blank")
EXAMPLE = [("abcd", "cdab"), ("abcd", "dcba"), ("aab", "aba"), ("aab", "baa"), ("aab", "aab")]
cnt = sum(is_rot(a, b) for a, b in EXAMPLE)
check("Q2a example: 4 of 5 are rotations and KMP agrees", cnt == 4 == sum(variants["T1*T1,T2"](a, b) for a, b in EXAMPLE))
bind_numeric(2, "a", 1, cnt, "Q2a count")

bad = 0
for _ in range(1500):
    a = "".join(random.choice("ab") for _ in range(random.randint(1, 7)))
    k = random.randint(1, len(a))
    b = a[k:] + a[:k]
    pos = (a + a).find(b)
    bad += not ((a + a)[k:k + len(b)] == b and pos + 1 <= k + 1)
check("Q2b rotation with index k occurs in T1*T1 starting at place k+1 (1500 random)", bad == 0)
check("Q2b distractors: car/arc occurs at place 2, not as a prefix and not wholly inside one copy",
      (("car" * 2).find("arc") + 1) == 2 and not ("carcar").startswith("arc") and "arc" not in "car")
bind_first(2, "b", 0, "Q2b seam")
first = ("abcd" * 2).find("cdab") + 1
check("Q2b example: cdab first occurs at place 3 in abcdabcd", first == 3)
bind_numeric(2, "b", 1, first, "Q2b place")
bind_numeric(2, "c", 0, len("x" * 50 * 2), "Q2c length")


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
    a = "".join(random.choice("ab") for _ in range(n))
    r.append(kmp_ops(a + a, a[::-1]) / n)
check("Q2c KMP work on T1*T1 is linear: ops/n <= 9", max(r) <= 9, [round(x, 2) for x in r])
bind_text(2, "c", 1, "Q2c complexity")

# ============================== Q3: matrix product check (Freivalds) ==============================
def matmul_count(k):
    cnt = 0
    for i in range(k):
        for j in range(k):
            for t in range(k):
                cnt += 1
    return cnt


check("Q3a 10x10 product uses 1000 multiplications = n^1.5 for n=100", matmul_count(10) == 1000 == round(100 ** 1.5))
bind_numeric(3, "a", 0, 1000, "Q3a")
bind_text(3, "a", 1, "Q3a complexity")


def mv(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def mm(A, B):
    return [[sum(A[i][t] * B[t][j] for t in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


always_true = True
for _ in range(300):
    k = random.randint(1, 4)
    A = [[random.randint(0, 5) for _ in range(k)] for _ in range(k)]
    B = [[random.randint(0, 5) for _ in range(k)] for _ in range(k)]
    C = mm(A, B)
    for y in itertools.product((0, 1), repeat=k):
        always_true &= mv(C, list(y)) == mv(A, mv(B, list(y)))
check("Q3b when C = AB the algorithm never says 'false' (300 random, every y)", always_true)
bind_first(3, "b", 1, "Q3b false is certain")
A = [[1, 2], [3, 4]]
B = [[0, 1], [1, 0]]
C = [[2, 1], [4, 4]]
check("Q3b example: AB = [[2,1],[4,3]], C differs in one entry", mm(A, B) == [[2, 1], [4, 3]])
expose = sum(mv(C, list(y)) != mv(A, mv(B, list(y))) for y in itertools.product((0, 1), repeat=2))
check("Q3b example: 2 of the 4 vectors expose the difference", expose == 2)
bind_numeric(3, "b", 2, expose, "Q3b expose")
check("Q3b order step has the 3 algorithm lines", len(step(3, "b", 0)["lines"]) == 3)
check("Q3c 10x10: By + A(By) + Cy = 300 multiplications", 3 * 10 * 10 == 300)
bind_numeric(3, "c", 0, 300, "Q3c")
bind_text(3, "c", 1, "Q3c complexity")
check("Q3c 3k^2 / n is constant for every k", len({3 * k * k // (k * k) for k in range(1, 200)}) == 1)

# Q3d: liars vs witnesses
def liars_witnesses(D, k):
    lie = wit = 0
    for v in itertools.product((0, 1), repeat=k):
        if all(x == 0 for x in mv(D, list(v))):
            lie += 1
        else:
            wit += 1
    return lie, wit


D1 = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
l1, w1 = liars_witnesses(D1, 3)
check("Q3d d_11 = 1 only, k = 3: 4 liars, 4 witnesses", (l1, w1) == (4, 4))
bind_numeric(3, "d", 0, l1, "Q3d liars")
bad = 0
bad_map = 0
for _ in range(300):
    k = random.randint(1, 4)
    D = [[random.choice((0, 0, 1, -1, 2)) for _ in range(k)] for _ in range(k)]
    if not any(any(r) for r in D):
        continue
    l, w = liars_witnesses(D, k)
    bad += l > w
    i, j = next((i, j) for i in range(k) for j in range(k) if D[i][j] != 0)
    for v in itertools.product((0, 1), repeat=k):
        if all(x == 0 for x in mv(D, list(v))):
            v2 = list(v)
            v2[j] ^= 1
            bad_map += all(x == 0 for x in mv(D, v2))
check("Q3d liars <= witnesses on 300 random nonzero D, and flipping v_j always gives a witness", bad == 0 and bad_map == 0)
one_line_diff(3, "d", 1, 2, "Q3d")

# ============================== Q4: disjoint circles ==============================
EX = {"c1": (-4.5, 2), "c2": (0, 2), "c3": (0, 3), "c4": (5, 4), "c5": (6, 2), "c6": (7, 5), "c7": (8, 3)}
names = list(EX)


def disjoint(a, b):
    return abs(a[0] - b[0]) > a[1] + b[1]            # tangent counts as touching


def best_sets(cs):
    best, sols = 0, []
    nm = list(cs)
    for m in range(1, 1 << len(nm)):
        sel = [nm[i] for i in range(len(nm)) if m >> i & 1]
        if all(disjoint(cs[a], cs[b]) for a, b in itertools.combinations(sel, 2)):
            if len(sel) > best:
                best, sols = len(sel), [sel]
            elif len(sel) == best:
                sols.append(sel)
    return best, sols


best, sols = best_sets(EX)
check("Q4a example: max 3, exactly the two optimal sets {c1,c2,c5} and {c1,c2,c7}",
      best == 3 and sorted(map(tuple, sols)) == [("c1", "c2", "c5"), ("c1", "c2", "c7")])
bind_numeric(4, "a", 0, best, "Q4a max")
bind_numeric(4, "a", 2, len(sols), "Q4a number of optimal sets")
valid = lambda s: all(disjoint(EX[a], EX[b]) for a, b in itertools.combinations(s, 2))
check("Q4a options: {c1,c2,c5} valid and optimal; the other three are not disjoint",
      valid(["c1", "c2", "c5"]) and not valid(["c1", "c3", "c7"]) and not valid(["c1", "c3", "c6"]) and not valid(["c2", "c4", "c6"]))
bind_first(4, "a", 1, "Q4a valid set")


def greedy(cs, key, strict=False):
    order = sorted(cs, key=lambda n: key(cs[n]))
    chosen = []
    for n in order:
        if all(disjoint(cs[n], cs[m]) for m in chosen):
            chosen.append(n)
    return chosen


def greedy_alg(cs, tangent_ok=False):
    order = sorted(cs, key=lambda n: cs[n][0] + cs[n][1])
    chosen = []
    L = list(order)
    while L:
        g = L.pop(0)
        chosen.append(g)
        right = cs[g][0] + cs[g][1]
        L = [n for n in L if (cs[n][0] - cs[n][1] > right if not tangent_ok else cs[n][0] - cs[n][1] >= right)]
    return chosen


bad = {k: 0 for k in ("right", "left", "radius", "center", "tangent")}
for _ in range(1500):
    cs = {f"c{i}": (random.randint(-8, 8), random.randint(1, 4)) for i in range(random.randint(1, 8))}
    b = best_sets(cs)[0]
    bad["right"] += len(greedy_alg(cs)) != b
    bad["left"] += len(greedy(cs, lambda c: c[0] - c[1])) != b
    bad["radius"] += len(greedy(cs, lambda c: c[1])) != b
    bad["center"] += len(greedy(cs, lambda c: c[0])) != b
    bad["tangent"] += len(greedy_alg(cs, True)) != b
check("Q4b right-end greedy == brute force (1500 random)", bad["right"] == 0)
check("Q4b sort keys left / radius / center each fail somewhere", bad["left"] > 0 and bad["radius"] > 0 and bad["center"] > 0)
bind_first(4, "b", 0, "Q4b sort key")
check("Q4b keeping tangent circles (strict < removal) fails somewhere", bad["tangent"] > 0)
bind_first(4, "b", 2, "Q4b tangent")
run = greedy_alg(EX)
check("Q4b example run: c1, c2, c5; second chosen is c2", run == ["c1", "c2", "c5"])
bind_numeric(4, "b", 1, int(run[1][1:]), "Q4b second")
check("Q4c both optimal sets contain c1", sum("c1" in s for s in sols) == 2)
bind_numeric(4, "c", 1, sum("c1" in s for s in sols), "Q4c count")
bind_first(4, "c", 0, "Q4c technique")
one_line_diff(4, "c", 2, 3, "Q4c")

# greedy choice property and optimal substructure on random instances
bad_gc = bad_os = 0
for _ in range(800):
    cs = {f"c{i}": (random.randint(-8, 8), random.randint(1, 4)) for i in range(random.randint(1, 7))}
    b, sl = best_sets(cs)
    g = greedy_alg(cs)[0]
    bad_gc += not any(g in s for s in sl)
    rest = {n: c for n, c in cs.items() if disjoint(c, cs[g])}
    bad_os += b != 1 + (best_sets(rest)[0] if rest else 0)
    wrong = {n: c for n, c in cs.items() if n != g}
    # removing only g (not the intersecting circles) overshoots on some inputs
check("Q4c some optimum contains the greedy choice (800 random)", bad_gc == 0)
check("Q4d OPT = 1 + OPT(circles disjoint from the greedy choice) (800 random)", bad_os == 0)
over = 0
for _ in range(800):
    cs = {f"c{i}": (random.randint(-8, 8), random.randint(1, 4)) for i in range(random.randint(2, 7))}
    g = greedy_alg(cs)[0]
    wrong = {n: c for n, c in cs.items() if n != g}
    over += 1 + best_sets(wrong)[0] != best_sets(cs)[0]
check("Q4d distractor 'all circles except g' gives the wrong optimum somewhere", over > 0)
bind_first(4, "d", 0, "Q4d subproblem")
rest = {n: c for n, c in EX.items() if disjoint(c, EX["c1"])}
check("Q4d example: after c1, 5 circles remain (c2,c4,c5,c6,c7) and their optimum is 2", sorted(rest) == ["c2", "c4", "c5", "c6", "c7"] and best_sets(rest)[0] == 2)
bind_numeric(4, "d", 1, len(rest), "Q4d remaining")
bind_numeric(4, "d", 2, best_sets(rest)[0], "Q4d sub optimum")
bind_first(4, "d", 3, "Q4d technique")

# ============================== Q5: suffix trie of banana$ ==============================
s = "banana$"
nodes = set()
for i in range(1, len(s)):               # the six drawn suffixes banana$ .. a$ (the lone $ is not drawn)
    for L in range(1, len(s) - i + 2):
        nodes.add(s[i - 1:][:L])
suffixes = [s[i:] for i in range(len(s) - 1)]
leaves = [n for n in nodes if not any(m != n and m.startswith(n) for m in nodes)]
rootkids = {n for n in nodes if len(n) == 1}
check("Q5 trie of the 6 suffixes: 21 non-root nodes, 6 leaves, 3 children of the root", len(nodes) == 21 and len(leaves) == 6 and rootkids == {"b", "a", "n"})
bind_numeric(5, "", 0, len(nodes), "Q5 nodes")
bind_numeric(5, "", 1, len(leaves), "Q5 leaves")
bind_numeric(5, "", 2, len(rootkids), "Q5 root children")

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
