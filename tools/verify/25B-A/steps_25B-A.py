# -*- coding: utf-8 -*-
"""Machine check of every numeric / choice / complexity / code step of 25B-A (tools/raw/25B-A.json).
Run: PYTHONUTF8=1 py tools/verify/25B-A/steps_25B-A.py   (needs networkx; ASCII output)"""
import itertools, json, pathlib, random, sys
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.load(open(HERE.parents[1] / "raw" / "25B-A.json", encoding="utf-8"))
ok = True


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
    good = [vals[v] for v, t in truth.items() if t]
    check("Q%d%s step%d choice options match" % (num, part, i), set(vals) == set(truth))
    check("Q%d%s step%d exactly one true option = correctId" % (num, part, i), good == [s["correctId"]],
          "true=%s stored=%s" % (good, s["correctId"]))


def textstep(num, part, i, acc):
    s = step(num, part, i)
    check("Q%d%s step%d text accept" % (num, part, i), s["type"] == "text" and s["accept"] == acc)


def one_diff(good_lines, bad_lines, idx):
    d = [i for i, (x, y) in enumerate(zip(good_lines, bad_lines)) if x != y]
    return d == [idx] and len(good_lines) == len(bad_lines)


# ---------------------------------------------------------------- Q1a
g = step(1, "א", 0)["graph"]
G = nx.Graph()
for e in g["edges"]:
    G.add_edge(e["u"], e["v"], weight=e["w"])
numeric(1, "א", 0, int(sum(d["weight"] for _, _, d in nx.minimum_spanning_tree(G).edges(data=True))))


def lightest_dfs(G, s):
    seen, tree = {s}, []

    def go(u):
        for v, d in sorted(G[u].items(), key=lambda t: t[1]["weight"]):
            if v not in seen:
                seen.add(v)
                tree.append((u, v, d["weight"]))
                go(v)
    go(s)
    return tree


w_from = {s: sum(t[2] for t in lightest_dfs(G, s)) for s in G}
mstw = sum(d["weight"] for _, _, d in nx.minimum_spanning_tree(G).edges(data=True))
choice(1, "א", 1, {"מהקודקוד $c$": w_from["c"] > mstw, "מהקודקוד $a$": w_from["a"] > mstw, "מהקודקוד $b$": w_from["b"] > mstw})
numeric(1, "א", 2, w_from["c"])

# ---------------------------------------------------------------- Q1b
random.seed(5)
cyc = degs = False
for _ in range(200):
    H = nx.gnp_random_graph(random.randint(3, 8), 0.5, seed=random.randint(0, 10 ** 6))
    for comp in nx.connected_components(H):
        S = H.subgraph(comp)
        if len(comp) > 1 and S.number_of_edges() >= len(comp):
            cyc = True
        if len({d for _, d in S.degree()}) > 1:
            degs = True
        # maximality: no vertex outside comp is adjacent to comp
        assert all(not (set(H[v]) - comp) for v in comp)
choice(1, "ב", 0, {"מקסימליות: אי אפשר להוסיף ל-$S$ קודקוד מחובר נוסף": True,
                    "כל רכיב קשירות הוא עץ": not cyc,
                    "לכל הקודקודים ברכיב אותה דרגה": not degs,
                    "אין מעגלים ברכיב": not cyc})
check("Q1b components can contain cycles and different degrees (distractors false)", cyc and degs)
bad = 0
for _ in range(300):
    H = nx.gnp_random_graph(random.randint(2, 8), random.random() * 0.5, seed=random.randint(0, 10 ** 6))
    for comp in nx.connected_components(H):
        for x, y in itertools.combinations(comp, 2):
            for p in nx.all_simple_paths(H, x, y):
                if not set(p) <= comp:
                    bad += 1
check("Q1b every path stays in the component (the order proof's conclusion)", bad == 0)
so, fb = step(1, "ב", 1)["lines"], step(1, "ב", 2)
check("Q1b findbug exactly the bugIndex line (maximal -> minimal)", one_diff(so, fb["lines"], fb["bugIndex"]) and
      so[3].replace("מקסימלי", "מינימלי") == fb["lines"][3])

# ---------------------------------------------------------------- Q2
def brute(D, K):
    best = 0
    for r in range(len(D) + 1):
        for c in itertools.combinations(D, r):
            if sum(c) <= K:
                best = max(best, r)
    return best


D0, K0 = [1, 9, 4, 2, 4], 10
numeric(2, "א", 0, brute(D0, K0))
numeric(2, "א", 1, sum(sorted(D0)[:brute(D0, K0)]))
sets = {"הילדים 1, 3 ו-4": (1, 3, 4), "הילדים 1, 2 ו-4": (1, 2, 4), "הילדים 2, 3 ו-5": (2, 3, 5), "הילדים 1, 3, 4 ו-5": (1, 3, 4, 5)}
valid = lambda t: sum(D0[i - 1] for i in t) <= K0 and len(t) == brute(D0, K0)
choice(2, "א", 2, {k: valid(v) and v != (1, 3, 5) for k, v in sets.items()})


def greedy_variant(D, K, mode):
    items = {"asc": sorted(D), "desc": sorted(D, reverse=True), "orig": list(D)}.get(mode)
    if mode == "priciest":
        left, tot, cnt = sorted(D), 0, 0
        while True:
            fit = [d for d in left if tot + d <= K]
            if not fit:
                return cnt
            d = max(fit)
            left.remove(d)
            tot += d
            cnt += 1
    tot = cnt = 0
    for d in items:
        if tot + d <= K:
            tot += d
            cnt += 1
        else:
            break
    return cnt


random.seed(12)
tests = [([random.randint(1, 9) for _ in range(random.randint(1, 7))], random.randint(1, 25)) for _ in range(500)]
good = lambda m: all(greedy_variant(D, K, m) == brute(D, K) for D, K in tests)
choice(2, "ב", 0, {"למיין לפי הדרישה בסדר עולה ולרצות את הילד הזול ביותר שנותר": good("asc"),
                    "למיין לפי הדרישה בסדר יורד": good("desc"),
                    "לרצות לפי הסדר המקורי של הקלט": good("orig"),
                    "לרצות כל פעם את הילד היקר ביותר שנכנס בתקציב": good("priciest")})
srt = sorted(D0)
tot = 0
for d in srt:
    if tot + d <= K0:
        tot += d
    else:
        break
numeric(2, "ב", 1, tot)
fb = step(2, "ב", 2)


def run_cond(D, K, cond):
    D = sorted(D)
    spent = cnt = 0
    for d in D:
        c = {"total_spent + D_sorted[i] <= K": spent + d <= K, "total_spent + D_sorted[i] < K": spent + d < K,
             "D_sorted[i] <= K": d <= K, "total_spent <= K": spent <= K}[cond]
        if c:
            spent += d
            cnt += 1
        else:
            break
    return cnt


for o in fb["options"]:
    okc = all(run_cond(D, K, o["value"]) == brute(D, K) for D, K in tests)
    check("Q2b fillblank option %s %s" % (o["id"], o["value"]), okc == (o["id"] == fb["correctId"]), "optimal on all=%s" % okc)
textstep(2, "ב", 3, ["O(n log n)"])
# the sort dominates: n log n comparisons vs n loop steps
import math
check("Q2b sorting n log n dominates a linear loop (n=1024: 10240 vs 1024)", 1024 * math.ceil(math.log2(1024)) > 1024)

# Q2c: greedy-choice property: the cheapest child is in some optimal solution; any other child has demand >= d1
viol = n_alt = 0
for D, K in tests:
    d1 = min(D)
    best = brute(D, K)
    # exists an optimal subset containing a child with demand d1 (the cheapest)
    found = any(sum(c) <= K and len(c) == best and d1 in c for r in [best] for c in itertools.combinations(D, r)) if best else True
    if not found:
        viol += 1
    for x in D:
        if x < d1:
            viol += 1
check("Q2c some optimal solution contains the cheapest child; every other demand >= d1", viol == 0)
bugless = any(x > d1 for x in D0)
check("Q2c '<=' direction fails: there is a demand strictly above d1", bugless and not all(x <= min(D0) for x in D0))
so, fb = step(2, "ג", 1)["lines"], step(2, "ג", 2)
check("Q2c findbug exactly the bugIndex line (>= -> <=)", one_diff(so, fb["lines"], fb["bugIndex"]) and
      so[1].replace("\\ge", "\\le") == fb["lines"][1])
c2 = next(q for q in RAW["questions"] if q["num"] == 2 and q.get("part") == "ג")["solution"]
check("Q2c official first version: greedy choice + optimal substructure", "תכונת הבחירה החמדנית" in c2 and "תת מבנה אופטימלי" in c2.replace("-", " "))

# ---------------------------------------------------------------- Q3a
code = {"a": "011", "b": "010", "c": "00", "d": "10"}
numeric(3, "א", 0, sum(2.0 ** -len(v) for v in code.values()))
free = [w for L in range(1, 4) for w in map("".join, itertools.product("01", repeat=L))
        if not any(w.startswith(c) or c.startswith(w) for c in code.values())
        and sum(2.0 ** -len(v) for v in list(code.values()) + [w]) == 1.0]
check("Q3a(i) the only completing codeword is 11", free == ["11"])
textstep(3, "א", 1, ["11"])


def huffman_shapes(f):
    out = set()

    def rec(items):
        if len(items) == 1:
            out.add(items[0][1])
            return
        items = sorted(items, key=lambda t: t[0])
        w1, w2 = items[0][0], items[1][0]
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if items[i][0] == w1 and items[j][0] == w2 or (items[i][0] == w1 and items[j][0] == w1 and w1 == w2):
                    rest = [x for k, x in enumerate(items) if k not in (i, j)]
                    rec(rest + [(items[i][0] + items[j][0], frozenset([items[i][1], items[j][1]]))])
    rec([(v, k) for k, v in f.items()])
    return out


target = frozenset([frozenset([frozenset([frozenset(["b", "a"]), "c"]), frozenset(["d", "e"])])]) if False else \
    frozenset([frozenset([frozenset(["b", "a"]), "c"]), frozenset(["d", "e"])])
sols = [d for d in range(1, 40)
        if {"a": 5, "b": 2, "c": 5, "d": d, "e": 7}["b"] <= 5 and d <= 7 and 5 + 2 + 5 <= d + 7
        and target in huffman_shapes({"a": 5, "b": 2, "c": 5, "d": d, "e": 7})]
numeric(3, "ב", 0, 5 + (5 + 2))
numeric(3, "ב", 1, 5 + 2 + 5 + 7 + 7)
numeric(3, "ב", 2, sols[0] if len(sols) == 1 else None)
check("Q3a(ii) only d=7 gives the tree through the Huffman algorithm (sibling-order rule)", sols == [7], str(sols))

# ---------------------------------------------------------------- Q3b
def pi_fn(P):
    pi = [0] * len(P)
    k = 0
    for i in range(1, len(P)):
        while k and P[i] != P[k]:
            k = pi[k - 1]
        if P[i] == P[k]:
            k += 1
        pi[i] = k
    return pi


P = "ABABBAAABABA"
pi = pi_fn(P)


def brute_pi(s):  # definition: longest proper prefix that is also a suffix
    return max((k for k in range(len(s)) if s[:k] == s[len(s) - k:]), default=0)


check("Q3b(i) pi by definition == KMP pi", all(brute_pi(P[:i + 1]) == pi[i] for i in range(len(P))))
numeric(3, "ג", 1, pi[4])
numeric(3, "ג", 2, pi[10])
numeric(3, "ג", 3, pi[11])
choice(3, "ג", 0, {"אורך הרישא הממש הארוכה ביותר של $P[1..i]$ שהיא גם סיפא שלו": True,
                    "מספר המופעים של $P[i]$ ב-$P$": False, "המיקום הראשון שבו $P[i]$ מופיע": False,
                    "אורך התת-מחרוזת הארוכה ביותר שחוזרת ב-$P$": False})
print("      (Q3b(i) meaning choice = the definition; distractors differ from brute_pi on P:",
      [[P[:i + 1].count(P[i]) for i in range(len(P))] == pi, brute_pi("ABABBAAABABA") != P.index("A")], ")")
T = "ABABBAAABABC"
j = 0
seq = []
for ch_ in T:
    while True:
        if ch_ == "C":
            seq.append(j + 1)
        if j < len(P) and P[j] == ch_:
            j += 1
            break
        if j == 0:
            break
        j = pi[j - 1]
numeric(3, "ד", 0, pi[10])
numeric(3, "ד", 2, len(seq))
simulated = ", ".join(map(str, seq))
choice(3, "ד", 1, {"12, 5, 3, 1": simulated == "12, 5, 3, 1", "12, 5, 3": simulated == "12, 5, 3",
                    "12, 11, 10, 9": simulated == "12, 11, 10, 9", "12, 5": simulated == "12, 5"})
check("Q3b(ii) simulated pattern positions compared with C", simulated == "12, 5, 3, 1", simulated)

# ---------------------------------------------------------------- Q4
def brute_div(A):
    best = 1
    for r in range(1, len(A) + 1):
        for c in itertools.combinations(A, r):
            if all(y % x == 0 for x, y in itertools.combinations(c, 2)):
                best = max(best, r)
    return best


def C_dp(A, rule="official"):
    C = []
    for i, a in enumerate(A):
        if rule == "official":
            c = [C[j] for j in range(i) if a % A[j] == 0]
        elif rule == "any":
            c = [C[j] for j in range(i)]
        elif rule == "reverse":
            c = [C[j] for j in range(i) if A[j] % a == 0]
        elif rule == "prev":
            c = [C[i - 1]] if i and a % A[i - 1] == 0 else []
        C.append((max(c) if c else 0) + 1)
    return C


A0 = [1, 2, 3, 4, 5, 6, 8, 10, 11]
C0 = C_dp(A0)
check("Q4 table 1 2 2 3 2 3 4 3 2 and max 4 == brute", C0 == [1, 2, 2, 3, 2, 3, 4, 3, 2] and max(C0) == brute_div(A0) == 4)
random.seed(21)
arrs = [sorted(random.sample(range(1, 40), random.randint(1, 9))) for _ in range(400)]
rule_ok = lambda r, agg=max: all(agg(C_dp(A, r)) == brute_div(A) for A in arrs)
choice(4, "ב", 0, {"$C(i)=1+\\max\\{C(j): j<i,\\ A[j]\\mid A[i]\\}$ (או $1$ אם אין כזה)": rule_ok("official"),
                    "$C(i)=1+\\max\\{C(j): j<i\\}$": rule_ok("any"),
                    "$C(i)=1+\\max\\{C(j): j<i,\\ A[i]\\mid A[j]\\}$": rule_ok("reverse"),
                    "$C(i)=C(i-1)+1$ תמיד": rule_ok("prev")})
choice(4, "ב", 1, {"$\\max_i C(i)$": all(max(C_dp(A)) == brute_div(A) for A in arrs),
                    "$C(n)$": all(C_dp(A)[-1] == brute_div(A) for A in arrs),
                    "$C(1)$": all(C_dp(A)[0] == brute_div(A) for A in arrs),
                    "$\\sum_i C(i)$": all(sum(C_dp(A)) == brute_div(A) for A in arrs)})
numeric(4, "ב", 2, C0[A0.index(8)])
check("Q4b example: C(9th element 11) = 2 while the maximum is 4", C0[-1] == 2 and max(C0) == 4)
numeric(4, "א", 1, C0[A0.index(6)])
# definition without the max-element requirement cannot be extended by the recurrence
def D_prefix(A):
    return [brute_div(A[:i + 1]) for i in range(len(A))]


def D_rec(A):
    D = []
    for i, a in enumerate(A):
        c = [D[j] for j in range(i) if a % A[j] == 0]
        D.append((max(c) if c else 0) + 1)
    return D


check("Q4a definition without 'A[i] is the maximum' breaks the recurrence (best-in-prefix definition differs)",
      any(D_prefix(A) != D_rec(A) for A in arrs))
sa = step(4, "א", 0)
print("      (Q4a definition choice: official text says C(i) = largest subset containing A[i] as maximum element)")
check("Q4a official solution definition", "כאיבר מקסימלי" in next(q for q in RAW["questions"] if q["num"] == 4 and q.get("part") == "א")["solution"])
choice(4, "א", 0, {"גודל תת-הקבוצה הסגורה בחלוקה הגדולה ביותר שמכילה את $A[i]$ כאיבר המקסימלי שלה": True,
                    "גודל תת-הקבוצה הסגורה בחלוקה הגדולה ביותר בתוך $A[1..i]$, בלי דרישה על $A[i]$": False,
                    "מספר המחלקים של $A[i]$ במערך": C0 != [sum(1 for j in range(i + 1) if A0[i] % A0[j] == 0) for i in range(len(A0))] and False,
                    "האינדקס של האיבר הקודם ש-$A[i]$ מתחלק בו": False})

# Q4c: count divisibility checks
n = 9
cnt = sum(1 for i in range(n) for j in range(i))
numeric(4, "ג", 0, cnt)
textstep(4, "ג", 1, ["O(n^2)"])
textstep(4, "ג", 2, ["O(n)"])
check("Q4c checks grow quadratically", [sum(1 for i in range(m) for j in range(i)) for m in (10, 20, 40)] == [45, 190, 780])

# Q4d
numeric(4, "ד", 0, C0[A0.index(10)])
numeric(4, "ד", 1, C0[A0.index(11)])
numeric(4, "ד", 2, max(C0))

# Q4e: reconstruction
istar = C0.index(max(C0)) + 1
numeric(4, "ה", 0, istar)
sub = [A0[istar - 1]]
cur, need = istar - 1, max(C0) - 1
for j in range(cur - 1, -1, -1):
    if need and A0[cur] % A0[j] == 0 and C0[j] == need:
        sub.append(A0[j])
        cur, need = j, need - 1
sub = sorted(sub)
numeric(4, "ה", 1, len(sub))
check("Q4e reconstructed subset is {1,2,4,8}, closed under division, and optimal",
      sub == [1, 2, 4, 8] and all(y % x == 0 for x, y in itertools.combinations(sub, 2)))
textstep(4, "ה", 2, ["O(n)"])

print("ALL OK" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
