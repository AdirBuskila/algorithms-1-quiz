"""Machine check of every stored answer in courses/kmp_prefix/C01..C08.

Run:  PYTHONUTF8=1 py tools/verify/needhelp/kmp_prefix/check.py
Every pi array, border list, fallback count, comparison count, match position and existence claim is recomputed
by brute force (definition of a border, naive substring search, exhaustive enumeration of strings) and compared
with what the level files store.  Exits non-zero on the first failure.
"""
import itertools
import json
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[3]
sys.path.insert(0, str(HERE))
from kmp_ref import (all_strings, borders_brute, chain, check_run, compares_for_char, feasible_pis, is_power,  # noqa: E402
                     min_period, occurrences_naive, pi_brute, pi_of, pi_pseudo, rgs, run_kmp)

FAILS = []
CHECKS = 0


def ok(cond, msg):
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILS.append(msg)
        print("FAIL:", msg)


def arr(p):
    return ",".join(str(x) for x in p[1:])


def load():
    r = subprocess.run(["node", str(HERE / "load_levels.js"), str(APP / "courses" / "kmp_prefix")],
                       capture_output=True, check=True)
    return json.loads(r.stdout.decode("utf8"))


LEVELS = load()
Q = {}          # question id -> (levelid, question)
LV = {}
for L in LEVELS:
    lv = L["level"]
    LV[lv["id"]] = lv
    for q in lv["questions"]:
        if "id" in q:
            Q[q["id"]] = (lv["id"], q)


def clean(v):
    return v.replace("$", "").replace("`", "").replace(" ", "").strip()


def body(q):
    return q["step"] if "step" in q else q


def opt_map(b):
    return {o["id"]: clean(o["value"]) for o in b["options"]}


def choice(qid, expected, also_wrong=None):
    """the correct option equals `expected`; no other option equals it; option values are distinct"""
    b = body(Q[qid][1])
    m = opt_map(b)
    vals = list(m.values())
    ok(len(set(vals)) == len(vals), f"{qid}: duplicate option values {vals}")
    ok(m[b["correctId"]] == clean(expected), f"{qid}: correct option {m[b['correctId']]!r} != computed {clean(expected)!r}")
    ok(sum(1 for v in vals if v == clean(expected)) == 1, f"{qid}: computed answer matches {sum(1 for v in vals if v == clean(expected))} options")
    return m, b


def num(qid, expected):
    b = body(Q[qid][1])
    ok(b["type"] == "numeric" and b["answer"] == expected and b.get("tol", 0) == 0, f"{qid}: stored {b.get('answer')} != computed {expected}")


def ticks(s):
    return re.findall(r"`([^`]*)`", s)


# ------------------------------------------------------------------ C01
P = "ABABA"
pi = pi_of(P)
ok(arr(pi) == "0,0,1,2,3", "C01 lesson table")
ok(borders_brute("ABABA") == [3, 1, 0] and borders_brute("ABAB") == [2, 0] and borders_brute("ABA") == [1, 0], "C01 lesson borders")

pi = pi_of("AABAA")
choice("C01-Q1", str(pi[5]))
ok(borders_brute("AABAA") == [2, 1, 0], "C01-Q1 borders A, AA")
ok("AAB" != "BAA" and "AABA" != "ABAA", "C01-Q1 sanity")
pi = pi_of("ABCABD")
num("C01-Q2", pi[5])
ok(borders_brute("ABCAB") == [2, 0], "C01-Q2 borders")
choice("C01-Q3", arr(pi_of("ABABA")))
ok(arr(pi_of("AAAAA")) == "0,1,2,3,4", "C01-Q3 distractor is the table of AAAAA")
# Q4: pi[q] < q always; the other three claims have counterexamples
alpha = "abc"
always = True
for n in range(1, 8):
    for s in all_strings(n, alpha):
        p = pi_brute(s)
        if not all(p[q] < q for q in range(1, n + 1)):
            always = False
ok(always, "C01-Q4 pi[q]<q must hold for every string over {a,b,c} up to length 7")
b, bq = choice("C01-Q4", r"\pi[q]<q")
ok(arr(pi_brute("AAB")) == "0,1,0", "C01-Q4 counterexample AAB (non-monotone)")
ok(arr(pi_brute("ABB")) == "0,0,0" and len(set("ABB")) < 3, "C01-Q4 counterexample ABB (repeat, pi[m]=0)")
ok(arr(pi_brute("AB")) == "0,0", "C01-Q4 counterexample AB (pi[q]=q-1 fails)")
num("C01-Q5", pi_of("AAAAA")[5])
ok(all(pi_of("A" * m)[m] == m - 1 for m in range(2, 11)), "C01-Q5 pi[a^m]=m-1")

# ------------------------------------------------------------------ C02
pi = pi_of("ABAABAB")
fb = []
pi_pseudo("ABAABAB", fb)
ok(arr(pi) == "0,0,1,1,2,3,2" and fb[7] == 1 and fb[4] == 1, "C02 lesson example ABAABAB: table and fallbacks of q=7 and q=4")
P = "ABACABAB"
pi = pi_of(P)
fb = []
pi_pseudo(P, fb)
ok(pi[1:8] == [0, 0, 1, 0, 1, 2, 3], "C02-Q1 given prefix")
num("C02-Q1", pi[8])
num("C02-Q2", fb[8])


def pi_variant(P, fallback):
    m = len(P)
    p = [None, 0]
    k = 0
    for q in range(2, m + 1):
        while k > 0 and P[k] != P[q - 1]:
            k = fallback(k, p)
        if P[k] == P[q - 1]:
            k += 1
        p.append(k)
    return p


def pi_nofallback(P):
    p = [None, 0]
    k = 0
    for q in range(2, len(P) + 1):
        k = k + 1 if P[k] == P[q - 1] else 0
        p.append(k)
    return p


P = "AABAABAAAB"
m, b = choice("C02-Q3", arr(pi_of(P)))
ok(m["a"] == arr(pi_variant(P, lambda k, p: k - 1)), "C02-Q3 distractor a = fallback k-1")
ok(m["c"] == arr(pi_variant(P, lambda k, p: 0)), "C02-Q3 distractor c = fallback to 0")
ok(m["d"] == arr(pi_nofallback(P)), "C02-Q3 distractor d = no fallback")
pi = pi_of(P)
fb = []
pi_pseudo(P, fb)
ok(pi[9] == 2 and fb[9] == 2 and pi[10] == 3 and pi[8] == 5, "C02-Q3 explanation (q=9 two fallbacks, q=10)")

# Q4: findbug
CANON = ["pi[1] <- 0", "k <- 0", "for q <- 2 to m", "    while k > 0 and P[k+1] != P[q]", "        k <- pi[k]",
         "    if P[k+1] = P[q]", "        k <- k + 1", "    pi[q] <- k"]
b = body(Q["C02-Q4"][1])
diff = [i for i, (x, y) in enumerate(zip(b["lines"], CANON)) if x != y]
ok(len(b["lines"]) == len(CANON) and diff == [b["bugIndex"]] and b["lines"][b["bugIndex"]] == "k <- 1",
   f"C02-Q4 exactly one changed line, the bug line {diff}")


def pi_k0(P, k0):
    m = len(P)
    p = [None, 0]
    k = k0
    for q in range(2, m + 1):
        while k > 0 and P[k] != P[q - 1]:
            k = p[k]
        if P[k] == P[q - 1]:
            k += 1
        p.append(k)
    return p


ok(pi_k0("ABACABAB", 1)[2] == 2 and pi_of("ABACABAB")[2] == 0, "C02-Q4 observable failure: pi[2]=2 with k<-1")
ok(all(pi_k0(s, 1)[2] == 2 for s in all_strings(3, "AB")), "C02-Q4 the bug always gives pi[2]=2")
P = "ABCABCABD"
pi = pi_of(P)
fb = []
pi_pseudo(P, fb)
ok(pi[1:9] == [0, 0, 0, 1, 2, 3, 4, 5], "C02-Q5 given prefix")
choice("C02-Q5", str(pi[9]))
ok(fb[9] == 2 and chain(pi, 8) == [5, 2], "C02-Q5 explanation chain 5->2->0")

# ------------------------------------------------------------------ C03
P = "ABABABA"
pi = pi_of(P)
ok(arr(pi) == "0,0,1,2,3,4,5" and chain(pi, 7) == [5, 3, 1] and borders_brute(P) == [5, 3, 1, 0], "C03 lesson example")
P = "AABAABAA"
pi = pi_of(P)
ok(pi[1:] == [0, 1, 0, 1, 2, 3, 4, 5], "C03 given table")
num("C03-Q1", len(chain(pi, 8)))
ok(len(chain(pi, 8)) == len(borders_brute(P)) - 1, "C03-Q1 chain length = number of non-empty borders (brute force)")
b_ = [x for x in borders_brute(P) if x > 0]
choice("C03-Q2", ",".join(map(str, b_)))
ok(chain(pi, 8) == b_ == [5, 2, 1], "C03-Q2 chain equals brute-force borders")
ok(P[:4] != P[-4:] and P[:3] != P[-3:], "C03-Q2 lengths 4 and 3 are not borders")
num("C03-Q3", chain(pi, 8)[1])
num("C03-Q4", pi[5])
ok(pi[8] == 5 and P[5] == "B" and borders_brute(P[:5]) == [2, 1, 0] and 4 not in borders_brute(P[:5]),
   "C03-Q4 setup: k=5, P[6]=B, k-1=4 is not a border")
# the whole chain claim, exhaustively
for n in range(1, 9):
    for s in all_strings(n, "ab"):
        p = pi_brute(s)
        for q in range(1, n + 1):
            ok(chain(p, q) == [x for x in borders_brute(s[:q]) if x > 0], f"chain claim fails on {s} q={q}")
            if FAILS:
                break
# Q5 fillblank
b = body(Q["C03-Q5"][1])
ok(b["lines"][b["blankIndex"]].strip() == "k <- ___", "C03-Q5 blank line")
m = opt_map(b)
ok(m[b["correctId"]] == "pi[k]", "C03-Q5 correct option is pi[k]")
variants = {"k-1": lambda k, p: k - 1, "0": lambda k, p: 0, "pi[k-1]": lambda k, p: p[k - 1] if k > 1 else 0, "pi[k]": lambda k, p: p[k]}
ok(set(m.values()) == set(variants), f"C03-Q5 options {sorted(m.values())}")
bad = {"k-1": "ABABB", "0": "AABAAA", "pi[k-1]": "AABAAA"}
for name, s in bad.items():
    ok(pi_variant(s, variants[name]) != pi_of(s), f"C03-Q5 variant {name} must fail on {s}")
ok(all(pi_variant(s, variants["pi[k]"]) == pi_of(s) for n in range(1, 9) for s in all_strings(n, "AB")), "C03-Q5 pi[k] correct everywhere")

# ------------------------------------------------------------------ C04
P = "ABABAC"
r = check_run("ABABABA", P)
ok(r["pi"][1:] == [0, 0, 1, 2, 3, 0] and r["states"] == [1, 2, 3, 4, 5, 4, 5] and r["comps"] == [1, 1, 1, 1, 1, 2, 1] and r["total"] == 8,
   f"C04 lesson example {r}")
P = "AABAAC"
pi = pi_of(P)
ok(pi[1:] == [0, 1, 0, 1, 2, 0], "C04 given pi")
r = check_run("AABAAD", P)
ok(r["states"][4] == 5, "C04-Q1 q=5 before D")
num("C04-Q1", r["comps"][-1])
ok(chain(pi, 5) == [2, 1], "C04-Q1 explanation chain")
r = check_run("AABAAB", P)
num("C04-Q2", r["comps"][-1])
r = check_run("AABAABAA", P)
num("C04-Q3", r["states"][-1])
num("C04-Q4", r["total"])
ok(r["comps"] == [1, 1, 1, 1, 1, 2, 1, 1] and r["ends"] == [], "C04-Q4 explanation 5+2+1+1")
b = body(Q["C04-Q5"][1])
ok(b["correctId"] == "a", "C04-Q5 correct id")
r = check_run("AAAAAB", "AAAAAC")
ok(r["comps"][-1] == 6 and r["comps"][-1] > 2, "C04-Q5 one char costs 6 comparisons for m=6 (refutes 'at most twice')")
random.seed(7)
for _ in range(3000):
    n = random.randint(1, 30)
    m = random.randint(1, 8)
    T = "".join(random.choice("ab") for _ in range(n))
    Pp = "".join(random.choice("ab") for _ in range(m))
    rr = check_run(T, Pp)
    ok(rr["while_iters"] <= n and rr["total"] <= 2 * n, f"C04-Q5 amortised bound fails on {T!r}, {Pp!r}")
    if FAILS:
        break

# ------------------------------------------------------------------ C05
r = check_run("ABABABAB", "ABAB")
ok(r["ends"] == [4, 6, 8] and r["states"] == [1, 2, 3, 2, 3, 2, 3, 2] and occurrences_naive("ABABABAB", "ABAB") == [1, 3, 5], "C05 lesson example")


def kmp_reset(T, P, reset_zero):
    pi = pi_of(P)
    m = len(P)
    q = 0
    ends = []
    for i, c in enumerate(T, 1):
        while q > 0 and P[q] != c:
            q = pi[q]
        if P[q] == c:
            q += 1
        if q == m:
            ends.append(i)
            q = 0 if reset_zero else pi[q]
    return ends


ok(kmp_reset("ABABABAB", "ABAB", True) == [4, 8], "C05 lesson: reset to 0 misses the occurrence starting at 3")
r = check_run("AAAAAA", "AAA")
num("C05-Q1", len(occurrences_naive("AAAAAA", "AAA")))
ok(len(r["ends"]) == 4, "C05-Q1 simulation agrees")
num("C05-Q2", r["while_iters"])
for T in ("a" * 9, "b" * 9):
    ok(check_run(T, "aaaa")["while_iters"] == 0, f"C05 lesson: a^m on {T} never runs the inner loop")
choice("C05-Q3", str(pi_of("AABAA")[5]))
ok(pi_of("AABAA")[1:] == [0, 1, 0, 1, 2], "C05-Q3 given pi")
occ = occurrences_naive("ABABABA", "ABA")
num("C05-Q4", occ[-1])
ok(occ == [1, 3, 5] and check_run("ABABABA", "ABA")["ends"] == [3, 5, 7], "C05-Q4 explanation")
CANON = ["q <- 0", "for i <- 1 to n", "    while q > 0 and P[q+1] != T[i]", "        q <- pi[q]", "    if P[q+1] = T[i]",
         "        q <- q + 1", "    if q = m", "        report an occurrence ending at i", "        q <- pi[q]"]
b = body(Q["C05-Q5"][1])
diff = [i for i, (x, y) in enumerate(zip(b["lines"], CANON)) if x != y]
ok(len(b["lines"]) == len(CANON) and diff == [b["bugIndex"]] and b["lines"][b["bugIndex"]] == "        q <- 0",
   f"C05-Q5 exactly one changed line {diff}")
ok(kmp_reset("ABABA", "ABA", False) == [3, 5] and kmp_reset("ABABA", "ABA", True) == [3], "C05-Q5 explanation counts")
b = body(Q["C05-Q6"][1])
misses = {}
for o in b["options"]:
    Pp, T = ticks(o["value"])
    misses[o["id"]] = len(kmp_reset(T, Pp, True)) != len(occurrences_naive(T, Pp))
ok([k for k, v in misses.items() if v] == [b["correctId"]], f"C05-Q6 only the correct option loses an occurrence: {misses}")
ok([ticks(o["value"]) for o in b["options"] if o["id"] == b["correctId"]] == [["ABA", "ABABA"]], "C05-Q6 correct pair is ABA / ABABA")

# ------------------------------------------------------------------ C06
F6 = feasible_pis(6)
tup = lambda s: tuple(int(x) for x in s.split(","))  # noqa: E731
b = body(Q["C06-Q1"][1])
mm = opt_map(b)
bad = [k for k, v in mm.items() if tup(v) not in F6]
ok(bad == [b["correctId"]], f"C06-Q1 exactly the correct option is infeasible: {bad}")
ok(all(tup(v)[i] <= tup(v)[i - 1] + 1 for k, v in mm.items() if k != b["correctId"] for i in range(1, 6)), "C06-Q1 the feasible ones obey the bound")
ok(tup(mm[b["correctId"]])[5] > tup(mm[b["correctId"]])[4] + 1, "C06-Q1 the infeasible one violates pi[q]<=pi[q-1]+1")
ok(arr(pi_brute("AABAAB")) == "0,1,0,1,2,3" and arr(pi_brute("ABABAB")) == "0,0,1,2,3,4" and arr(pi_brute("AAABBA")) == "0,1,2,0,0,1",
   "C06-Q1 witnesses")
# Q2
ok((0, 0, 1, 2, 1) not in feasible_pis(5), "C06-Q2 no string has pi=0,0,1,2,1 (any alphabet)")
b = body(Q["C06-Q2"][1])
ok(b["correctId"] == "a", "C06-Q2 correct id")
ok(pi_of("ABABA")[5] == 3 and pi_of("ABAB")[1:] == [0, 0, 1, 2], "C06-Q2 explanation: ABAB then A forces pi[5]=3")
ok(1 <= 2 + 1, "C06-Q2 distractor b: bound holds")
ok(all(pi_brute(s)[3] != 1 or s[2] == s[0] for n in (3, 4, 5) for s in rgs(n)), "C06-Q2 distractor d false: pi[3]=1 forces P[3]=P[1]")
# lesson example
ok((0, 1, 2, 1) not in feasible_pis(4) and 1 <= 2 + 1, "C06 lesson example 0,1,2,1")
ok(pi_of("AAAA")[4] == 3 and pi_of("AAAB")[4] == 0, "C06 lesson: aaa then a/non-a")
# Q3
t = (0, 0, 0, 1, 2, 0)
alph = {}
for s in rgs(6):
    if tuple(pi_brute(s)[1:]) == t:
        alph[s] = len(set(s))
num("C06-Q3", min(alph.values()))
ok(arr(pi_brute("ABBABC")) == "0,0,0,1,2,0" and "ABBABC" in {s.upper() for s in alph}, "C06-Q3 witness ABBABC")
ok(all(not (set(s) <= set("ab")) for s in alph), "C06-Q3 no 2-letter string")
# Q4
b = body(Q["C06-Q4"][1])
mm = opt_map(b)
hit = [k for k, v in mm.items() if tuple(pi_brute(v)[1:]) == (0, 0, 1, 2, 0, 1)]
ok(hit == [b["correctId"]] and mm[hit[0]] == "ABABCA", f"C06-Q4 unique match {hit}")
ok(pi_of("ABABAA")[5] == 3 and arr(pi_of("ABACAB")) == "0,0,1,0,1,2" and pi_of("ABABCB")[6] == 0, "C06-Q4 explanation")
# Q5
cnt = sum(1 for s in all_strings(5, "ab") if tuple(pi_brute(s)[1:]) == (0, 1, 0, 1, 2))
num("C06-Q5", cnt)
ok(sorted(s for s in all_strings(5, "ab") if tuple(pi_brute(s)[1:]) == (0, 1, 0, 1, 2)) == ["aabaa", "bbabb"], "C06-Q5 witnesses")

# ------------------------------------------------------------------ C07
S = "aba#ababa"
pi = pi_brute(S)
ok(arr(pi) == "0,0,1,0,1,2,3,2,3" and [j for j in range(1, len(S) + 1) if pi[j] == 3] == [7, 9]
   and [j - 6 for j in (7, 9)] == occurrences_naive("ababa", "aba"), "C07 lesson P#T example")
for A, p_, power in (("abcabcabc", 3, True), ("abcabcab", 3, False)):
    pi = pi_of(A)
    n = len(A)
    ok(n - pi[n] == p_ == min_period(A) and is_power(A) == power and (pi[n] > 0 and n % (n - pi[n]) == 0) == power, f"C07 lesson periodic {A}")
ok(pi_of("abcabcabc")[9] == 6 and pi_of("abcabcab")[8] == 5, "C07 lesson pi values")
A = "abcdabcdab"
pi = pi_of(A)
ok(pi[10] == 6, "C07-Q1 given pi[10]")
num("C07-Q1", len(A) - pi[10])
ok(min_period(A) == 4 and not is_power(A), "C07-Q1 brute force period, not a power")
b = body(Q["C07-Q2"][1])
mm = opt_map(b)
ok([k for k, v in mm.items() if is_power(v)] == [b["correctId"]] and mm[b["correctId"]] == "abcabcabc", "C07-Q2 unique periodic option")
ok(min_period("abaabaab") == 3 and min_period("aabaabaa") == 3, "C07-Q2 explanation periods")
# Q3
P, T = "aab", "aabaabaab"
S = P + "#" + T
pi = pi_brute(S)
js = [j for j in range(1, len(S) + 1) if pi[j] == len(P)]
ok(js == [7, 10, 13], "C07-Q3 given indices")
num("C07-Q3", js[-1] - 2 * len(P))
ok([j - 2 * len(P) for j in js] == occurrences_naive(T, P) == [1, 4, 7], "C07-Q3 starts match naive search")
# Q4
b = body(Q["C07-Q4"][1])
ok(b["correctId"] == "a", "C07-Q4 correct id")
ok(max(pi_brute("aa" + "aaa")[1:]) == 4 and max(pi_brute("aa#aaa")[1:]) == 2, "C07-Q4 explanation numbers")
for m_ in range(1, 5):
    for P in all_strings(m_, "ab"):
        for n_ in range(1, 9):
            for T in all_strings(n_, "ab"):
                pp = pi_brute(P + "#" + T)
                ok(max(pp[1:]) <= m_, f"C07-Q4 pi<=m violated {P} {T}")
                js = [j for j in range(1, len(pp)) if pp[j] == m_]
                ok([j - 2 * m_ for j in js] == occurrences_naive(T, P), f"C07 P#T claim fails {P} {T}")
                if FAILS:
                    break
            if FAILS:
                break
        if FAILS:
            break
# Q5
T = "cbacbaxcba"
Pp = "abc"
num("C07-Q5", len(occurrences_naive(T, Pp[::-1])))
ok(occurrences_naive(T, Pp[::-1]) == [1, 4, 8] and occurrences_naive(T, Pp) == [], "C07-Q5 explanation")
ok(check_run(T, Pp[::-1])["ends"] == [3, 6, 10], "C07-Q5 KMP run agrees")
# Q6
b = body(Q["C07-Q6"][1])
mm = opt_map(b)
S1 = "abcde"
rot = [k for k, v in mm.items() if len(v) == len(S1) and v in S1 + S1]
ok(rot == [b["correctId"]] and mm[rot[0]] == "cdeab", "C07-Q6 unique rotation")
ok(all(any(S1[i:] + S1[:i] == v for i in range(5)) == (k in rot) for k, v in mm.items()), "C07-Q6 rotation by definition agrees")
ok(all(sorted(v) == sorted(S1) for v in mm.values()), "C07-Q6 all options are permutations")
ok((S1 + S1).find("cdeab") == 2, "C07-Q6 explanation: third position")
# rotation / reversal / period reductions, exhaustively
for n in range(1, 8):
    for s1 in all_strings(n, "ab"):
        for s2 in all_strings(n, "ab"):
            by_def = any(s1[i:] + s1[:i] == s2 for i in range(n))
            ok(by_def == (len(occurrences_naive(s1 + s1, s2)) > 0), f"rotation claim {s1} {s2}")
    for A in all_strings(n, "ab"):
        pi = pi_of(A)
        ok(is_power(A) == (pi[n] > 0 and n % (n - pi[n]) == 0), f"periodicity claim {A}")
        ok(min_period(A) == n - pi[n], f"min period claim {A}")
    if FAILS:
        break

# ------------------------------------------------------------------ C08 (boss) + bank facts used by the lessons
bank = json.loads((APP / "questions.json").read_text(encoding="utf8"))
bank = bank["questions"] if isinstance(bank, dict) else bank
B = {x["id"]: x for x in bank}
boss = LV["C08"]
ok(boss.get("boss") is True and boss["id"] == "C08", "C08 is the boss")
ids = [q["bankId"] for q in boss["questions"]]
ok(len(ids) == len(set(ids)) and 4 <= len(ids) <= 6, "C08 bank ids")
for i in ids:
    x = B.get(i)
    ok(x is not None and not x.get("hold") and x.get("topic") == "kmp_strings" and (x.get("official") or x.get("stepsSource") in ("official", "ai-verified") or x["kind"] in ("mcq", "truefalse")),
       f"C08 bank id {i} usable")
P = "ABABBAAABABA"
pi = pi_of(P)
ok(arr(pi) == "0,0,1,2,0,1,1,1,2,3,4,3" and "0 0 1 2 0 1 1 1 2 3 4 3" in B["25B-A-Q3c"]["solution"], "25B-A-Q3c")
r = run_kmp(P[:11] + "C", P)
ok(r["states"][10] == 11 and r["comps"][-1] == 4 and chain(pi, 11) == [4, 2], "25B-A-Q3d: 4 comparisons for C")
ok("4" in B["25B-A-Q3d"]["solution"], "25B-A-Q3d solution says 4")
P = "AABAABAABAAA"
ok(arr(pi_of(P)) == "0,1,0,1,2,3,4,5,6,7,8,2" and "2" in B["26B-A-Q4e"]["solution"], "26B-A-Q4e")
ok((0, 0, 1, 1, 2, 1) not in feasible_pis(6), "22B-A-Q1b: 0,0,1,1,2,1 has no string")
ok((0, 0, 0, 0, 0, 1) in feasible_pis(6) and arr(pi_of("abbbba")) == "0,0,0,0,0,1", "22B-A-Q1a witness (brief)")
ok((0, 1, 2, 3, 1) not in feasible_pis(5), "23B-C-Q1a (brief): 0,1,2,3,1 has no string")
for T in ("b" * 8, "a" * 8):
    ok(run_kmp(T, "aaaa")["while_iters"] == 0, f"26A-B-Q5b: inner loop never runs on {T}")
ok(B["26A-B-Q5b"]["verdict"] is True, "26A-B-Q5b verdict true")
ok("T1 * T1, T2" in B["SAMP-1-Q2a"]["solution"], "SAMP-1-Q2a solution")

# ------------------------------------------------------------------ global hygiene
ok([lv["order"] for lv in LV.values()] == list(range(1, 9)), "level orders 1..8")
ORD = re.compile("האפשרות ה|האפשרות הראשונה|האפשרות השנייה|\\([א-ד]\\)|תשובה [א-ד]\\b")


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, list):
        for x in o:
            yield from strings(x)
    elif isinstance(o, dict):
        for x in o.values():
            yield from strings(x)


seen = set()
for lv in LV.values():
    n_own = [q for q in lv["questions"]]
    ok(4 <= len(n_own) <= 6, f"{lv['id']}: {len(n_own)} questions")
    for q in n_own:
        qid = q.get("id") or q.get("bankId")
        ok(qid not in seen, f"duplicate {qid}")
        seen.add(qid)
        ok(bool(q.get("recap")), f"{qid}: recap")
        if "id" in q:
            b = body(q)
            ok(bool(b.get("explanation") or b.get("explain")), f"{qid}: explanation")
    for s in strings(lv):
        ok(not ORD.search(s), f"{lv['id']}: positional reference in {s[:60]!r}")
        for mth in re.findall(r"\$([^$]*)\$", s):
            ok(not re.search("[֐-׿]", mth), f"{lv['id']}: Hebrew inside math {mth[:40]!r}")

print(f"{CHECKS} checks, {len(FAILS)} failures")
sys.exit(1 if FAILS else 0)
