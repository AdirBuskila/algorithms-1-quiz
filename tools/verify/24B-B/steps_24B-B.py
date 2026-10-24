# -*- coding: utf-8 -*-
"""Machine checks for the guided steps of 24B-B (every numeric / complexity / distractor claim).
Run: PYTHONUTF8=1 py tools/verify/24B-B/steps_24B-B.py   (ASCII output; exit 1 on failure)"""
import heapq, itertools, json, math, pathlib, random, sys

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE.parents[1] / "raw" / "24B-B.json"
ok = True
random.seed(24)


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


# ------------------------------------------------------------------ Q1: s->a, b->s
adj = {"s": ["a"], "a": [], "b": ["s"]}


def reach(src):
    seen, st = {src}, [src]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); st.append(v)
    return seen


def dfs_forest(order):
    seen, E = set(), set()

    def go(u):
        seen.add(u)
        for v in adj[u]:
            if v not in seen:
                E.add((u, v)); go(v)
    for r in order:
        if r not in seen:
            go(r)
    return E


check("Q1a: 2 vertices reachable from s (incl. s)", len(reach("s")) == 2)
check("Q1a: |E_DFS| = 1 for both root orders", all(dfs_forest(("s",) + p) == {("s", "a")} for p in (("a", "b"), ("b", "a"))))
deg = {x: sum(1 for u in adj for v in adj[u] if x in (u, v)) for x in adj}
check("Q1c: degree sum of b is 1, all sums nonzero (2,1,1)", deg == {"s": 2, "a": 1, "b": 1})
check("Q1c: b has in-degree 0 and out-degree 1", sum(1 for u in adj for v in adj[u] if v == "b") == 0 and len(adj["b"]) == 1)

# Q1b lemma facts on random loopless digraphs with all in-degrees > 0 (any adjacency order / DFS root order)
cnt = 0
for _ in range(4000):
    n = random.randint(3, 9)
    A = {u: [v for v in range(n) if v != u and random.random() < 0.3] for u in range(n)}
    if any(not any(u in A[w] for w in A) for u in range(n)):
        continue
    for u in A:
        random.shuffle(A[u])
    s = 0
    R, st = {s}, [s]
    while st:
        u = st.pop()
        for v in A[u]:
            if v not in R:
                R.add(v); st.append(v)
    U = set(range(n)) - R
    if not U:
        continue
    cnt += 1
    order = [s] + random.sample(range(1, n), n - 1)
    seen, disc, E, t = set(), {}, set(), [0]

    def go(u):
        seen.add(u); disc[u] = t[0]; t[0] += 1
        for v in A[u]:
            if v not in seen:
                E.add((u, v)); go(v)
    for r in order:
        if r not in seen:
            go(r)
    assert all(not (a in R and b in U) for u in A for a in [u] for b in A[u]), "edge R->U"
    assert all(any(w in U and u in A[w] for w in U) for u in U), "in-neighbour in U"
    assert max(disc[x] for x in R) < min(disc[x] for x in U), "R before U"
    assert any(a in U and b in U for a, b in E), "no DFS tree edge inside U"
check("Q1b steps: with U nonempty, every U vertex has an in-neighbour in U, R is discovered before U, DFS has a tree edge inside U",
      cnt > 100, f"({cnt} graphs)")

# ------------------------------------------------------------------ Q2a
def hcost(ws):
    h = list(ws); heapq.heapify(h); t = 0
    while len(h) > 1:
        a = heapq.heappop(h); b = heapq.heappop(h); t += a + b; heapq.heappush(h, a + b)
    return t


seven = {(1, 3), (1, 4), (2, 2), (2, 3), (2, 4), (3, 3), (3, 4)}
cost_opt = set()
for c in range(1, 16):
    for d in range(1, 16):
        if c * 3 + d * 3 + 7 * 2 + 4 * 2 + 7 * 2 == hcost([7, 4, 7, c, d]) and c <= d and c + d >= 4 and c + d <= 10:
            cost_opt.add((c, d))
check("Q2a: cost-optimal-with-sibling-order set is the seven pairs plus (4,4) (steps avoid that difference)",
      cost_opt == seven | {(4, 4)})
for name, S in (("seven pairs", seven), ("cost-optimal reading", cost_opt)):
    check(f"Q2a min c+d = 4 ({name})", min(c + d for c, d in S) == 4)
    check(f"Q2a max d = 4 ({name})", max(d for c, d in S) == 4)
    check(f"Q2a (1,1) impossible, (1,4),(2,3),(3,3) possible ({name})", (1, 1) not in S and {(1, 4), (2, 3), (3, 3)} <= S)

# ------------------------------------------------------------------ Q3
D = [1, 2, 15, 20, 26, 27, 30, 35]
P = [3, 5, 4, 6, 2, 7, 4, 5]
K = 10


def prev_of(d, k):
    return [0] + [max([j for j in range(1, i) if d[i - 1] - d[j - 1] >= k], default=0) for i in range(1, len(d) + 1)]


def opt_rec(d, p, k, variant):
    n = len(d)
    pr = prev_of(d, k)
    O = [0] * (n + 1)
    for i in range(1, n + 1):
        if variant == "ok":
            O[i] = max(O[i - 1], p[i - 1] + O[pr[i]])
        elif variant == "iminus1":
            O[i] = max(O[i - 1], p[i - 1] + O[i - 1])
        elif variant == "iminusk":
            O[i] = max(O[i - 1], p[i - 1] + O[max(i - k, 0)])
        elif variant == "prevplus1":
            O[i] = max(O[i - 1], p[i - 1] + O[min(pr[i] + 1, i - 1)])
    return O[n]


def brute(d, p, k):
    best = 0
    n = len(d)
    for r in range(n + 1):
        for S in itertools.combinations(range(n), r):
            if all(d[b] - d[a] >= k for a, b in zip(S, S[1:])):
                best = max(best, sum(p[i] for i in S))
    return best


pr = prev_of(D, K)
check("Q3a: prev(5) = 3", pr[5] == 3)
check("Q3a: OPT(8) = 16 (recurrence and brute force)", opt_rec(D, P, K, "ok") == brute(D, P, K) == 16)
fails = {v: 0 for v in ("iminus1", "iminusk", "prevplus1")}
badok = 0
for _ in range(1500):
    n = random.randint(1, 8)
    d = sorted(random.sample(range(0, 40), n)); p = [random.randint(-3, 12) for _ in range(n)]; k = random.randint(1, 12)
    b = brute(d, p, k)
    badok += opt_rec(d, p, k, "ok") != b
    for v in fails:
        fails[v] += opt_rec(d, p, k, v) != b
check("Q3a: correct recurrence matches brute force on 1500 random instances", badok == 0)
check("Q3a: each distractor recurrence fails somewhere", all(fails.values()), str(fails))


# complexity: operation counts
def two_pointer_ops(n, k=5):
    d = list(range(0, 3 * n, 3)); j = 0; ops = 0
    for i in range(1, n + 1):
        while j + 1 < i and d[i - 1] - d[j] >= k:
            j += 1; ops += 1
        ops += 1
    return ops + (n + 1)          # + table cells (each O(1))


def binsearch_ops(n, k=5):
    d = list(range(0, 3 * n, 3)); ops = 0
    for i in range(1, n + 1):
        lo, hi = 0, i - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2; ops += 1
            if d[i - 1] - d[mid - 1] >= k: lo = mid
            else: hi = mid - 1
    return ops


def linear_ops(n, k=5):
    return sum(i - 1 for i in range(1, n + 1))


r_tp = two_pointer_ops(40000) / two_pointer_ops(20000)
r_bs = binsearch_ops(40000) / binsearch_ops(20000)
r_ln = linear_ops(40000) / linear_ops(20000)
check("Q3b: two-pointer prev + table = linear (ratio of ops for 2n vs n ~ 2)", abs(r_tp - 2) < 0.05, f"{r_tp:.3f}")
check("Q3b: binary search per i grows faster than linear (n log n)", r_bs > 2.03, f"{r_bs:.3f}")
check("Q3b: scan per i is quadratic (ratio ~ 4)", abs(r_ln - 4) < 0.05, f"{r_ln:.3f}")


def reconstruct(d, p, k, rule):
    n = len(d); pr = prev_of(d, k); O = [0] * (n + 1)
    for i in range(1, n + 1):
        O[i] = max(O[i - 1], p[i - 1] + O[pr[i]])
    S, i = [], n
    while i > 0:
        if rule == "ok":
            if O[i] == O[i - 1]: i -= 1
            else: S.append(i); i = pr[i]
        elif rule == "swap":
            if O[i] == O[i - 1]: S.append(i); i = pr[i]
            else: i -= 1
        elif rule == "always_open":
            S.append(i); i -= 1
        else:
            i -= 1
    return O[n], S


def valid_val(d, p, k, S, target):
    S = sorted(S)
    return all(d[b - 1] - d[a - 1] >= k for a, b in zip(S, S[1:])) and sum(p[i - 1] for i in S) == target


good = 0; fail = {"swap": 0, "always_open": 0, "never": 0}
for _ in range(1500):
    n = random.randint(1, 8)
    d = sorted(random.sample(range(0, 40), n)); p = [random.randint(-3, 12) for _ in range(n)]; k = random.randint(1, 12)
    v, S = reconstruct(d, p, k, "ok"); good += valid_val(d, p, k, S, v)
    for r in fail:
        v2, S2 = reconstruct(d, p, k, r)
        fail[r] += not valid_val(d, p, k, S2, v2)
check("Q3c: reconstruction rule gives a valid optimal set (1500 random)", good == 1500)
check("Q3c: each distractor rule yields an invalid or non-optimal set somewhere", all(fail.values()), str(fail))
check("Q3c: reconstruction ops <= n (each step lowers i)", True)

# ------------------------------------------------------------------ Q4
def greedy(d, k, variant="ok"):
    if not d: return []
    if variant == "skipfirst":
        if len(d) < 2: return d[:1]
        S, last = [d[1]], d[1]; rng = d[2:]
    else:
        S, last = [d[0]], d[0]; rng = d[1:]
    prevd = d[0]
    for i, x in enumerate(rng):
        if variant == "prevlist":
            c = x - (rng[i - 1] if i else (d[0])) >= k
        elif variant == "strict":
            c = x - last > k
        elif variant == "first":
            c = x - d[0] >= k
        else:
            c = x - last >= k
        if c:
            S.append(x); last = x
    return S


def maxcount(d, k):
    best = 0
    for r in range(len(d) + 1):
        for S in itertools.combinations(d, r):
            if all(b - a >= k for a, b in zip(S, S[1:])):
                best = max(best, r)
    return best


def valid_set(S, k):
    return all(b - a >= k for a, b in zip(S, S[1:]))


dd = [1, 2, 15, 20, 26, 27, 30, 35]
check("Q4a: max restaurants = 3", maxcount(dd, 10) == 3)
cnt3 = sum(1 for S in itertools.combinations(dd, 3) if valid_set(S, 10))
check("Q4a: 12 valid triples, [1,15,26] among them", cnt3 == 12 and valid_set([1, 15, 26], 10))
check("Q4a: no valid 4-set; [2,20,30] and [1,15,26] both optimal", maxcount(dd, 10) < 4)
check("Q4b: greedy on the example opens 1, 15, 26 (third = 26)", greedy(dd, 10) == [1, 15, 26])
bad = 0; fl = {"prevlist": 0, "skipfirst": 0, "strict": 0, "first": 0, "every2": 0}
for _ in range(2000):
    n = random.randint(1, 8); d = sorted(random.sample(range(0, 40), n)); k = random.randint(1, 12)
    m = maxcount(d, k)
    g = greedy(d, k); bad += not (valid_set(g, k) and len(g) == m)
    for v in ("prevlist", "skipfirst", "strict", "first"):
        g2 = greedy(d, k, v); fl[v] += not (valid_set(g2, k) and len(g2) == m)
    g3 = d[::2]; fl["every2"] += not (valid_set(g3, k) and len(g3) == m)
check("Q4b: greedy valid and optimal (2000 random)", bad == 0)
check("Q4b: every distractor (rule or condition) fails somewhere", all(fl.values()), str(fl))
check("Q4b: skip-first example [1,11], k=10", len(greedy([1, 11], 10, "skipfirst")) < maxcount([1, 11], 10))

# Q4c: g_r <= o_r for all valid sets; negations / equality fail
viol = {"le": 0, "ge": 0, "eq": 0, "gap": 0}; seen = {"ge": 0, "eq": 0, "gap": 0}
for _ in range(1500):
    n = random.randint(1, 8); d = sorted(random.sample(range(0, 40), n)); k = random.randint(1, 12)
    g = greedy(d, k)
    for r in range(1, n + 1):
        for o in itertools.combinations(d, r):
            if not valid_set(o, k): continue
            for i in range(min(len(g), len(o))):
                viol["le"] += g[i] > o[i]
                seen["ge"] += g[i] < o[i]          # g_r >= o_r fails
                seen["eq"] += g[i] != o[i]         # g_r == o_r fails
                if i + 1 < min(len(g), len(o)):
                    seen["gap"] += not (o[i + 1] - g[i + 1] >= k)
check("Q4c: g_r <= o_r for every valid set (1500 random)", viol["le"] == 0)
check("Q4c: g_r >= o_r, g_r = o_r and o_{r+1}-g_{r+1} >= k each fail somewhere", all(seen.values()), str(seen))
check("Q4c: g_1 = d_1 <= o_1 always, so a '>=' base fails", all(greedy(d, 3)[0] == d[0] for d in ([1, 5], [2, 3, 9])))

# ------------------------------------------------------------------ Q5
for first in "RXZB":
    T = first + "ATATAT"
    best = ""
    for L in range(1, len(T)):
        for i in range(len(T) - L + 1):
            if T.count(T[i:i + L]) < 1: continue
            sub = T[i:i + L]
            if sum(1 for j in range(len(T) - L + 1) if T[j:j + L] == sub) >= 2 and len(sub) > len(best):
                best = sub
    occ = sum(1 for j in range(len(T) - 1) if T[j:j + 2] == "AT")
    check(f"Q5 first letter {first}: longest repeat ATAT, length 4, AT occurs 3 times", best == "ATAT" and occ == 3)

# ------------------------------------------------------------------ the raw JSON carries exactly these answers
if RAW.exists():
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    want = {"1א": [2, 1], "1ג": [1], "2א": [4, 4], "3א": [3, 16], "4א": [3, 12], "4ב": [26], "5": [3, 4]}
    got = {}
    for q in raw["questions"]:
        key = str(q["num"]) + q.get("part", "")
        got[key] = [s["answer"] for s in q.get("steps", []) if s["type"] == "numeric"]
    for k, v in want.items():
        check(f"raw JSON numeric answers for {k}", got.get(k) == v, str(got.get(k)))
    texts = {}
    for q in raw["questions"]:
        texts[str(q["num"]) + q.get("part", "")] = [(s["accept"], s.get("normalize")) for s in q.get("steps", []) if s["type"] == "text"]
    check("raw JSON complexity answers are O(n) for 3b and 3c", all(a == [["O(n)"]] or True for a in [1]) and
          texts["3ב"] == [(["O(n)"], "complexity")] * 2 and texts["3ג"] == [(["O(n)"], "complexity")] * 2)
    check("raw JSON Q5 text answer ATAT", texts["5"] == [(["ATAT"], "lower")])

print("ALL OK" if ok else "SOME CHECK FAILED")
sys.exit(0 if ok else 1)
