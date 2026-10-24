# -*- coding: utf-8 -*-
"""Solver checks for 24B-B Q3 (restaurants DP), Q4 (greedy, constant profit), bonus (suffix tree text).
Run: PYTHONUTF8=1 py tools/verify/24B-B/solve_q3_q4_q5.py   (ASCII output)"""
import itertools, json, pathlib, random

HERE = pathlib.Path(__file__).resolve().parent
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


def brute(d, p, k):
    best, bestset = 0, ()
    n = len(d)
    for r in range(n + 1):
        for S in itertools.combinations(range(n), r):
            if all(d[b] - d[a] >= k for a, b in zip(S, S[1:])):
                v = sum(p[i] for i in S)
                if v > best: best, bestset = v, S
    return best


def dp(d, p, k):
    """OPT[i] = max(OPT[i-1], p_i + OPT[prev(i)]), prev by two pointers. 1-based OPT, OPT[0]=0. Returns value, chosen."""
    n = len(d)
    prev = [0] * (n + 1)
    j = 0
    for i in range(1, n + 1):
        while j + 1 < i and d[i - 1] - d[j] >= k:   # d[j] is d_{j+1}
            j += 1
        prev[i] = j
    OPT = [0] * (n + 1)
    for i in range(1, n + 1):
        OPT[i] = max(OPT[i - 1], p[i - 1] + OPT[prev[i]])
    # reconstruction
    S, i = [], n
    while i > 0:
        if p[i - 1] + OPT[prev[i]] >= OPT[i - 1] and p[i - 1] + OPT[prev[i]] == OPT[i]:
            S.append(i - 1); i = prev[i]
        else:
            i -= 1
    return OPT[n], S[::-1]


random.seed(7)
bad = 0
for _ in range(3000):
    n = random.randint(0, 9)
    d = sorted(random.sample(range(0, 40), n))
    p = [random.randint(-3, 12) for _ in range(n)]
    k = random.randint(1, 12)
    v, S = dp(d, p, k)
    valid = all(d[b] - d[a] >= k for a, b in zip(S, S[1:])) and sum(p[i] for i in S) == v
    if v != brute(d, p, k) or not valid: bad += 1
check("Q3 recurrence (two-pointer prev) + reconstruction == brute force, 3000 random (profits may be negative)", bad == 0)


def greedy(d, k):
    out = []
    for x in d:
        if not out or x - out[-1] >= k: out.append(x)
    return out


bad = 0
for _ in range(3000):
    n = random.randint(0, 10)
    d = sorted(random.sample(range(0, 50), n)); k = random.randint(1, 15)
    g = greedy(d, k)
    if len(g) != brute(d, [1] * n, k) or not all(b - a >= k for a, b in zip(g, g[1:])): bad += 1
check("Q4 greedy (leftmost first, then first at distance >= k) is optimal, 3000 random", bad == 0)
P = [1, 2, 15, 20, 26, 27, 30, 35]
check("Q4 example: greedy gives [1,15,26]", greedy(P, 10) == [1, 15, 26])
opt3 = [S for S in itertools.combinations(P, 3) if all(b - a >= 10 for a, b in zip(S, S[1:]))]
check("Q4a: [2,20,30] and [1,15,26] are both optimal (3 is max)", (2, 20, 30) in opt3 and (1, 15, 26) in opt3
      and brute(P, [1] * 8, 10) == 3, "%d optimal sets" % len(opt3))

# ---- bonus: what the drawn tree forces on T
g = json.load(open(HERE / "graphs.json", encoding="utf-8"))["24B-B-Q5"]
ch = {}
for e in g["edges"]:
    ch.setdefault(e["u"], []).append((e["w"], e["v"]))


def leaves(u, acc):
    if u.isdigit():
        yield int(u), acc
        return
    for w, v in ch[u]:
        yield from leaves(v, acc + w)


suf = dict(leaves("root", ""))
check("bonus: 8 leaves, suffix i has length 8-i", sorted(suf) == list(range(8)) and all(len(suf[i]) == 8 - i for i in suf))
check("bonus: suffixes 1..7 read from leaves 1..7 force T[1..6] = ATATAT",
      all(suf[i] == suf[1][i - 1:] for i in range(1, 8)) and suf[1] == "ATATAT$")
first = suf[0][0]
check("bonus: the leaf-0 edge starts with a letter other than A, T, $ (root children are $, A, T, leaf 0)",
      first not in "AT$", first)
# whatever T[0] is (any letter not A/T), the longest repeated substring is ATAT
for x in "BRXZ":
    T = x + "ATATAT"
    reps = [T[i:j] for i in range(7) for j in range(i + 1, 8)
            if sum(T.startswith(T[i:j], t) for t in range(7)) >= 2]
    lr = max(reps, key=len)
    if not (lr == "ATAT" and all(len(r) < 4 or r == "ATAT" for r in reps)): ok = False
check("bonus: for any first letter not in {A,T}, the unique longest repeated substring is ATAT", ok)
# deepest internal node by string depth
depth = {}


def walk(u, dd):
    depth[u] = dd
    for w, v in ch.get(u, []):
        walk(v, dd + len(w))


walk("root", 0)
internal = [u for u in ch if u != "root"]
deep = max(internal, key=lambda u: depth[u])
check("bonus: deepest internal node is root-AT-AT (string depth 4)", deep == "nAT" and depth[deep] == 4)
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
