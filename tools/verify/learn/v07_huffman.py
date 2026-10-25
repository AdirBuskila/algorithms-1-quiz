# -*- coding: utf-8 -*-
"""Learn-brief checks: huffman (brief 09). Huffman with ARBITRARY tie-breaking (the course convention, GATE1 ruling
2026-10-24): a code/tree is a Huffman outcome if SOME tie-break produces it. Siblings: the lighter one is the left child
(bit 0); equal weights may be placed either way.
Run: PYTHONUTF8=1 py tools/verify/learn/v07_huffman.py     (ASCII output, exits 1 on a failure)"""
import itertools, random, sys
from functools import lru_cache

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


random.seed(99)


def outcomes(freq, oriented=True):
    """freq: dict symbol -> weight. Returns the set of all codes (frozenset of (symbol, code)) reachable by some tie-break.
    oriented=True: lighter child on the left (0), either order when equal. oriented=False: only the unordered tree shape
    (set of frozenset leaf-sets at every node), used for the 'every full tree' claim."""
    start = [(w, ((s, ""),)) for s, w in freq.items()]
    res = set()
    seen = set()

    def rec(nodes):
        key = tuple(sorted(nodes))
        if key in seen:
            return
        seen.add(key)
        if len(nodes) == 1:
            res.add(frozenset(nodes[0][1]))
            return
        ws = sorted(w for w, _ in nodes)
        s1, s2 = ws[0], ws[1]
        for i, j in itertools.combinations(range(len(nodes)), 2):
            if sorted((nodes[i][0], nodes[j][0])) != [s1, s2]:
                continue
            a, b = nodes[i], nodes[j]
            rest = [nodes[k] for k in range(len(nodes)) if k not in (i, j)]
            if oriented:
                orders = []
                if a[0] < b[0]:
                    orders = [(a, b)]
                elif b[0] < a[0]:
                    orders = [(b, a)]
                else:
                    orders = [(a, b), (b, a)]
            else:
                orders = [(a, b)]
            for L, R in orders:
                merged = (L[0] + R[0], tuple((s, "0" + c) for s, c in L[1]) + tuple((s, "1" + c) for s, c in R[1]))
                rec(rest + [merged])
    rec(start)
    return res


def cost(freq, code):
    return sum(freq[s] * len(c) for s, c in code)


def huffman_cost(ws):
    import heapq
    h = list(ws)
    heapq.heapify(h)
    total = 0
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        total += a + b
        heapq.heappush(h, a + b)
    return total


def optimal_cost(ws):
    n = len(ws)

    @lru_cache(None)
    def f(mask):
        if mask & (mask - 1) == 0:
            return 0
        w = sum(ws[i] for i in range(n) if mask >> i & 1)
        best = float("inf")
        sub = (mask - 1) & mask
        while sub:
            other = mask ^ sub
            if sub < other:
                best = min(best, f(sub) + f(other))
            sub = (sub - 1) & mask
        return best + w
    return f((1 << n) - 1)


# ---- Huffman cost = optimum over all full binary trees
bad = 0
for _ in range(200):
    ws = [random.randint(1, 20) for _ in range(random.randint(2, 7))]
    bad += huffman_cost(ws) != optimal_cost(tuple(ws))
check("Huffman cost == optimal cost over all binary trees (DP over subsets) (200 random)", bad == 0)

# ---- every outcome of every tie-break has the same (optimal) cost
bad = 0
for _ in range(150):
    freq = {chr(97 + i): random.randint(1, 6) for i in range(random.randint(2, 6))}
    opt = huffman_cost(list(freq.values()))
    bad += any(cost(freq, code) != opt for code in outcomes(freq))
check("all tie-breaks give the same optimal total cost (150 random with many ties)", bad == 0)

# ---- ropes 4,3,2,6 (22A-B Q4): Huffman merges 2+3, 5+4, 9+6 -> 29
check("22A-B Q4 ropes 4,3,2,6: minimum cost 29 = 5 + 9 + 15 (sum of merged lengths); the quoted order 4+3,7+2,9+6 costs 31",
      huffman_cost([4, 3, 2, 6]) == 29 and 7 + 9 + 15 == 31)

# ---- 26A-A Q3a : a=22 b=15 c=3 d=24 e=4 f=10 g=8
F = dict(a=22, b=15, c=3, d=24, e=4, f=10, g=8)
outs = outcomes(F)
costs = {cost(F, o) for o in outs}
check("26A-A Q3a: total cost 219 in every outcome", costs == {219} and huffman_cost(list(F.values())) == 219, costs)
lens = {tuple(sorted((s, len(c)) for s, c in o)) for o in outs}
check("26A-A Q3a: the b-vs-internal-node tie gives two different code-length sets", len(lens) == 2, sorted(lens)[:2])
bits = {"a": "01", "b": "111", "c": "0000", "d": "10", "e": "0001", "f": "110", "g": "001"}
check("26A-A Q3a: the printed code a=01 b=111 c=0000 d=10 e=0001 f=110 g=001 is one of the outcomes", frozenset(bits.items()) in outs)

# ---- geometric 1,3,9,27,81 (24A-C Q3b,c)
G = dict(a=1, b=3, c=9, d=27, e=81)
outs = outcomes(G)
check("24A-C Q3b: weights 1,3,9,27,81 give one chain tree: lengths a4 b4 c3 d2 e1",
      len(outs) == 1 and dict((s, len(c)) for s, c in next(iter(outs))) == dict(a=4, b=4, c=3, d=2, e=1))
check("24A-C Q3b cost: 1*4+3*4+9*3+27*2+81*1 = 178", cost(G, next(iter(outs))) == 178 == 4 + 12 + 27 + 54 + 81)
H1 = dict(a=1, b=1, c=1, d=1, e=1)  # q = 1
lens = {tuple(sorted(len(c) for s, c in o)) for o in outcomes(H1)}
check("24A-C Q3c: ratio q=1 (all equal) does NOT give the chain: code lengths 2,2,2,3,3", lens == {(2, 2, 2, 3, 3)})
Q2 = dict(a=1, b=2, c=4, d=8, e=16)
check("ratio q=2 gives the chain again", {tuple(sorted(len(c) for s, c in o)) for o in outcomes(Q2)} == {(1, 2, 3, 4, 4)})

# ---- adding k to every frequency changes the tree (22B-B Q1a)
a1 = outcomes(dict(a=2, c=2, b=5))
a3 = outcomes(dict(a=4, c=4, b=7))
check("22B-A Q1a: freq (2,2,5): b gets code 1; freq (4,4,7): b gets code 0 (same shape, other code)",
      all(dict(o)["b"] == "1" for o in a1) and all(dict(o)["b"] == "0" for o in a3))
f1, f2 = dict(a=1, b=1, c=2, d=3), dict(a=3, b=3, c=4, d=5)
l1 = {tuple(sorted(len(c) for s, c in o)) for o in outcomes(f1)}
l2 = {tuple(sorted(len(c) for s, c in o)) for o in outcomes(f2)}
check("stronger example: freq 1,1,2,3 -> lengths 1,2,3,3 but +2 each (3,3,4,5) -> lengths 2,2,2,2", l1 == {(1, 2, 3, 3)} and l2 == {(2, 2, 2, 2)}, (l1, l2))

# ---- is a given code a Huffman code ? (24A-C Q3a, 24B-A Q3a)
def code_is_outcome(freq, code):
    return frozenset(code.items()) in outcomes(freq)

c1 = dict(a1="00", a2="11", a3="01", a4="100", a5="101")
check("24A-C Q3a: code 00,11,01,100,101 with freq 3,4,3,1,2 is a Huffman outcome (tie among 3,3,3 resolved)",
      code_is_outcome(dict(a1=3, a2=4, a3=3, a4=1, a5=2), c1))
check("and the same code is NOT a Huffman code for freq 1,1,1,1,1... (kraft ok but shape needs different weights)",
      not code_is_outcome(dict(a1=1, a2=1, a3=1, a4=1, a5=1), c1))
c2 = dict(c="00", d="01", e="10", a="110", b="111")
check("24B-A Q3a: code 00,01,10,110,111 with freq c2 d2 e2 a1 b1 is a Huffman outcome", code_is_outcome(dict(a=1, b=1, c=2, d=2, e=2), c2))
# a code that is a prefix code but not full can never be Huffman (e.g. 0, 10)
check("a non-full prefix code (0,10,110) has Kraft sum 7/8 < 1 and no Huffman outcome", sum(2 ** -len(x) for x in ("0", "10", "110")) < 1)

# ---- find the possible frequencies (the exam family)
def feasible(known, unknown, code, rng, extra=lambda f: True):
    out = []
    for vals in itertools.product(rng, repeat=len(unknown)):
        freq = dict(known)
        freq.update(dict(zip(unknown, vals)))
        if extra(freq) and frozenset(code.items()) in outcomes(freq):
            out.append(vals)
    return out

# 22B-A Q1c : b=2 d=5, c=x, a=y ; a-0 b-100 c-101 d-11
r = feasible(dict(b=2, d=5), ["c", "a"], dict(a="0", b="100", c="101", d="11"), range(1, 16))
want = {(2, y) for y in range(5, 10)} | {(3, y) for y in range(5, 11)}
check("22B-A Q1c: x=2 with 5<=y<=9, or x=3 with 5<=y<=10", set(r) == want, sorted(set(r) ^ want))
# 22B-B Q1b : b=2, a=x, c=y, x+y=8; a-1 b-00 c-01
r = feasible(dict(b=2), ["a", "c"], dict(a="1", b="00", c="01"), range(1, 10), lambda f: f["a"] + f["c"] == 8)
check("22B-B Q1b: (x,y) in {(6,2),(5,3)}", set(r) == {(6, 2), (5, 3)}, r)
# 23B-C Q4 : a=10 b=7 e=10 ; a-10 b-00 c-010 d-011 e-11 ; c,d >= 1
r = feasible(dict(a=10, b=7, e=10), ["c", "d"], dict(a="10", b="00", c="010", d="011", e="11"), range(1, 15))
want = {(1, 6), (1, 7), (2, 5), (2, 6), (2, 7), (3, 4), (3, 5), (3, 6), (3, 7), (4, 4), (4, 5), (4, 6), (5, 5)}
check("23B-C Q4: thirteen options for (c,d)", set(r) == want and len(r) == 13, sorted(set(r) ^ want))
# 24B-B Q2a : a=7 b=4 e=7 ; a-10 b-00 c-010 d-011 e-11
r = feasible(dict(a=7, b=4, e=7), ["c", "d"], dict(a="10", b="00", c="010", d="011", e="11"), range(1, 15))
want = {(1, 3), (1, 4), (2, 2), (2, 3), (2, 4), (3, 3), (3, 4)}
check("24B-B Q2a: seven options for (c,d)", set(r) == want, sorted(set(r) ^ want))
# 25B-A Q3b : a=5 b=2 c=5 e=7 ; a-011 b-010 c-00 d-10 e-11
r = feasible(dict(a=5, b=2, c=5, e=7), ["d"], dict(a="011", b="010", c="00", d="10", e="11"), range(1, 20))
check("25B-A Q3b: d must be 7", r == [(7,)], r)
# 26B-A Q4b : a=13 b=1 c=2 d=4 ; a-0 b-1100 c-1101 d-111 e-10
r = feasible(dict(a=13, b=1, c=2, d=4), ["e"], dict(a="0", b="1100", c="1101", d="111", e="10"), range(1, 20))
check("26B-A Q4b: e is 6 or 7", r == [(6,), (7,)], r)
# fixed tie-break rule can change the count: a deterministic 'earliest created first' rule vs all
def deterministic_outcome(freq, tie="small_first"):
    nodes = [(w, i, ((s, ""),)) for i, (s, w) in enumerate(freq.items())]
    cnt = len(nodes)
    while len(nodes) > 1:
        nodes.sort(key=lambda n: (n[0], n[1]) if tie == "old_first" else (n[0], -n[1]))
        a, b = nodes[0], nodes[1]
        nodes = nodes[2:]
        L, R = (a, b) if a[0] <= b[0] else (b, a)
        nodes.append((a[0] + b[0], cnt, tuple((s, "0" + c) for s, c in L[2]) + tuple((s, "1" + c) for s, c in R[2])))
        cnt += 1
    return frozenset(nodes[0][2])

n_fixed = n_all = 0
for vals in itertools.product(range(1, 15), repeat=2):
    freq = dict(a=7, b=4, e=7)
    freq.update(dict(c=vals[0], d=vals[1]))
    target = frozenset(dict(a="10", b="00", c="010", d="011", e="11").items())
    n_all += target in outcomes(freq)
    n_fixed += deterministic_outcome(freq, "old_first") == target
check("24B-B Q2a: with a fixed tie rule (older node first) fewer pairs qualify than with arbitrary ties", n_all == 7 and n_fixed < n_all, (n_fixed, n_all))

# ---- 25B-A Q3a / 26B-A Q4a: the missing code word completes a FULL tree
check("25B-A Q3a: codes 011, 010, 00, 10 and the missing one is 11 (full tree)", sum(2 ** -len(c) for c in ("011", "010", "00", "10", "11")) == 1)
check("26B-A Q4a: codes a=0 b=1100 c=1101 d=111 e=10: Kraft sum 1", sum(2 ** -len(c) for c in ("0", "1100", "1101", "111", "10")) == 1)

# ---- 26A-A Q3b : every full binary tree with n leaves is a Huffman tree for the weights 2^(h-d)
def full_trees(n):
    """all full binary trees (ordered) with n leaves as nested tuples"""
    if n == 1:
        return ["L"]
    out = []
    for k in range(1, n):
        for l in full_trees(k):
            for r in full_trees(n - k):
                out.append((l, r))
    return out

def leaves_depths(t, d=0):
    if t == "L":
        return [d]
    return leaves_depths(t[0], d + 1) + leaves_depths(t[1], d + 1)

def codes_of(t, pre=""):
    if t == "L":
        return [pre]
    return codes_of(t[0], pre + "0") + codes_of(t[1], pre + "1")

bad = tested = 0
for n in range(2, 8):
    for t in full_trees(n):
        cs = codes_of(t)
        depths = [len(c) for c in cs]
        h = max(depths)
        freq = {i: 2 ** (h - len(c)) for i, c in enumerate(cs)}
        target = frozenset((i, c) for i, c in enumerate(cs))
        tested += 1
        # orientation: lighter left; the tree may have equal siblings in either order, so compare up to swapping equal-weight siblings
        res = outcomes(freq)
        def canon(code_set):
            return frozenset(len(c) for s, c in code_set) and tuple(sorted(len(c) for s, c in code_set))
        good = any(tuple(sorted((s, len(c)) for s, c in o)) == tuple(sorted((s, len(c)) for s, c in target)) for o in res)
        bad += not good
check("26A-A Q3b: weights 2^(h-d) make every full binary tree (n<=7 leaves, %d trees) a Huffman outcome (code lengths)" % tested, bad == 0)

# ---- numbers of the worked examples in brief 09
check("26A-A Q3a merge weights 7,15,25,37,49,86 sum to 219", [3 + 4, 7 + 8, 10 + 15, 15 + 22, 24 + 25, 37 + 49] == [7, 15, 25, 37, 49, 86] and sum([7, 15, 25, 37, 49, 86]) == 219)
check("26A-A Q3a printed code cost 2*22+3*15+4*3+2*24+4*4+3*10+3*8 = 219", 2 * 22 + 3 * 15 + 4 * 3 + 2 * 24 + 4 * 4 + 3 * 10 + 3 * 8 == 219)
F = dict(a=22, b=15, c=3, d=24, e=4, f=10, g=8)
alt = [o for o in outcomes(F) if dict(o)["b"] == "11" or len(dict(o)["b"]) == 2]
check("26A-A Q3a other tie: b length 2, g length 4, c and e length 5 (cost 219)",
      alt and all(len(dict(o)["b"]) == 2 and len(dict(o)["g"]) == 4 and len(dict(o)["c"]) == 5 and len(dict(o)["e"]) == 5 and cost(F, o) == 219 for o in alt))
# 24A-C Q3a merge sequence: 1+2=3, then a1+a3=6, then X+a2=7, then 6+7
f = dict(a1=3, a2=4, a3=3, a4=1, a5=2)
check("24A-C Q3a: merges 3, 6, 7, 13 (root) with the tie a1+a3 chosen", [1 + 2, 3 + 3, 3 + 4, 6 + 7] == [3, 6, 7, 13] and sum(f.values()) == 13)
# 22B-B Q1b derivation: y >= 2, x >= y + 2, x + y = 8
sol = [(x, y) for y in range(1, 9) for x in [8 - y] if y >= 2 and x >= y + 2]
check("22B-B Q1b: constraints y>=2, x>=y+2, x+y=8 give exactly (6,2),(5,3)", sorted(sol) == [(5, 3), (6, 2)])
# cost = sum of internal node weights, ropes
check("ropes: cost equals the sum of merged weights; sum of ropes 15 is not the cost", huffman_cost([4, 3, 2, 6]) == 29 != 15)
# 23A-B Q4a: frequencies 3,2,1,1 give optimal cost 13 with code 1,01,001,000
check("23A-B Q4a: freq (3,2,1,1): optimal cost 13 = 3*1+2*2+1*3+1*3 for the printed code a=1 b=01 c=001 d=000",
      huffman_cost([3, 2, 1, 1]) == 13 == 3 * 1 + 2 * 2 + 1 * 3 + 1 * 3)
o = outcomes(dict(a=3, b=2, c=1, d=1))
check("23A-B Q4a: with the left-lighter convention the code lengths are a1 b2 c3 d3 (cost 13)",
      all(sorted(len(c) for s, c in x) == [1, 2, 3, 3] and cost(dict(a=3, b=2, c=1, d=1), x) == 13 for x in o))

sys.exit(0 if ok else 1)
