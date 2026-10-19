# -*- coding: utf-8 -*-
"""Reference checks for 24B-B (algorithms-1). No answer source exists (all items held as no-key); these compute
reference values for the solver/refuter. ASCII output. Run: PYTHONUTF8=1 py tools/verify/24B-B/checks.py"""
import itertools, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


# ---------- Q2a: letters a,b,e fixed, c,d unknown; code a10 b00 c010 d011 e11, left sibling <= right sibling ----------
def huffman_trees(ws):
    """All unordered Huffman trees reachable by some tie-breaking. ws: dict letter -> weight.
    A tree is a letter or a frozenset of two subtrees."""
    out = set()

    def rec(items):
        if len(items) == 1:
            out.add(items[0][1])
            return
        items = sorted(items, key=lambda t: t[0])
        w1 = items[0][0]
        w2 = items[1][0]
        # choose any two items among those allowed by ties
        cand = [i for i, t in enumerate(items) if t[0] <= w2]
        for i, j in itertools.combinations(cand, 2):
            if sorted([items[i][0], items[j][0]]) != [w1, w2]:
                continue
            a, b = items[i], items[j]
            rest = [t for k, t in enumerate(items) if k not in (i, j)]
            rec(rest + [(a[0] + b[0], frozenset([a[1], b[1]]))])
    rec([(w, l) for l, w in ws.items()])
    return out


target = frozenset([frozenset(["b", frozenset(["c", "d"])]), frozenset(["a", "e"])])


def weight(t, ws):
    return ws[t] if isinstance(t, str) else sum(weight(x, ws) for x in t)


def ordered_ok(ws):
    """Left sibling weight <= right sibling weight for the given code tree."""
    def w(x):
        return weight(x, ws)
    pairs = [("b", frozenset(["c", "d"])), ("a", "e"), ("c", "d"),
             (frozenset(["b", frozenset(["c", "d"])]), frozenset(["a", "e"]))]
    # left, right as in the code: 0-subtree = {b, {c,d}}, 1-subtree = {a, e}; b=00 left of {c,d}=01; a=10 left of e=11; c=010 left of d=011
    return (w("b") <= w(frozenset(["c", "d"])) and w("a") <= w("e") and w("c") <= w("d")
            and w(frozenset(["b", frozenset(["c", "d"])])) <= w(frozenset(["a", "e"])))


sols = []
for fc in range(1, 15):
    for fd in range(1, 15):
        ws = {"a": 7, "b": 4, "e": 7, "c": fc, "d": fd}
        if target in huffman_trees(ws) and ordered_ok(ws):
            sols.append((fc, fd))
print("     reference solutions (c,d) =", sols)
check("Q2a reference set is non-empty and every pair has c<=d", bool(sols) and all(c <= d for c, d in sols))


# ---------- Q4: example n=8, k=10 ----------
def max_restaurants(pos, k):
    cnt, last = 0, None
    for x in sorted(pos):
        if last is None or x - last >= k:
            cnt += 1
            last = x
    return cnt


def brute(pos, k):
    best = 0
    for r in range(len(pos) + 1):
        for sub in itertools.combinations(sorted(pos), r):
            if all(b - a >= k for a, b in zip(sub, sub[1:])):
                best = max(best, r)
    return best


P = [1, 2, 15, 20, 26, 27, 30, 35]
check("Q4 example: greedy = 3 = brute force", max_restaurants(P, 10) == 3 == brute(P, 10))
sols4 = [s for r in (3,) for s in itertools.combinations(P, r) if all(b - a >= 10 for a, b in zip(s, s[1:]))]
check("Q4a [2,20,30] is optimal and other optimal solutions exist (not unique)", (2, 20, 30) in sols4 and len(sols4) > 1,
      "optimal 3-subsets=%d" % len(sols4))

# ---------- Bonus: longest repeated substring of RATATAT (text read from the suffix tree figure) ----------
T = "RATATAT"
best = max((T[i:i + L] for i in range(len(T)) for L in range(1, len(T) - i + 1)
            if T.count(T[i:i + L]) >= 1 and sum(1 for j in range(len(T)) if T.startswith(T[i:i + L], j)) >= 2),
           key=len)
check("Bonus: the longest repeated substring of RATATAT is ATAT", best == "ATAT", best)
g = json.load(open(HERE / "graphs.json"))["24B-B-Q5"]
leaves = {e["v"]: e for e in g["edges"] if e["v"].isdigit()}
sufs = sorted(T + "$"[0:0] + "$")
check("Bonus: graphs.json leaves 0..7 are the suffixes of RATATAT$",
      sorted(leaves) == [str(i) for i in range(8)])
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
