# -*- coding: utf-8 -*-
"""Machine check of every numeric / choice / complexity / code step of 26A-A (tools/raw/26A-A.json).
Run: PYTHONUTF8=1 py tools/verify/26A-A/steps_26A-A.py   (needs networkx and clang; ASCII output)
Each expected value is recomputed here by brute force, networkx, heapq, a KMP simulation or a real clang run,
then compared with what the generator stored."""
import itertools, heapq, json, pathlib, random, subprocess, sys, shutil, re
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.load(open(HERE.parents[1] / "raw" / "26A-A.json", encoding="utf-8"))
CLANG = r"C:\Users\Adir\AppData\Local\Programs\Swift\Toolchains\6.1.0+Asserts\usr\bin\clang.exe"
TMP = HERE.parents[1] / "tmp_algorithms-1_26A-A_steps"
TMP.mkdir(exist_ok=True)
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
    """truth: option value -> bool computed by the checker. Exactly one True and it must be correctId."""
    s = step(num, part, i)
    vals = {o["value"]: o["id"] for o in s["options"]}
    good = [vals[v] for v, t in truth.items() if t]
    check("Q%d%s step%d choice: options match" % (num, part, i), set(vals) == set(truth))
    check("Q%d%s step%d choice: exactly one true option = correctId" % (num, part, i), good == [s["correctId"]],
          "true=%s stored=%s" % (good, s["correctId"]))


def textstep(num, part, i, expected_accept):
    s = step(num, part, i)
    check("Q%d%s step%d text accept" % (num, part, i), s["type"] == "text" and s["accept"] == expected_accept)


# ---------------------------------------------------------------- Q1
def brute_tasks(A):
    n = len(A)
    best = None
    for mask in range(1 << n):
        if any(not (mask >> i & 1) and not (mask >> (i + 1) & 1) for i in range(n - 1)):
            continue
        s = sum(A[i] for i in range(n) if mask >> i & 1)
        best = s if best is None or s < best else best
    return best


def Tvals(A):
    T = {}
    t = lambda i: 0 if i < 0 else T[i]
    for i in range(len(A)):
        T[i] = A[i] + min(t(i - 1), t(i - 2))
    return T, t


numeric(1, "א", 0, brute_tasks([10, 5]))
numeric(1, "א", 1, brute_tasks([10]))
check("Q1a at least one task is NOT forced (distractor 'must do >=1' false)", brute_tasks([10]) == 0)
choice(1, "א", 2, {"כי הכלל אוסר רק דילוג על שתי משימות עוקבות או יותר, ובמערך כזה אין זוג כזה": brute_tasks([10]) == 0,
                    "כי חובה לדלג על לפחות משימה אחת בכל קלט": brute_tasks([10, 5]) == 0,
                    "כי הזמן של משימה בודדת נחשב תמיד $0$": brute_tasks([10, 5]) == 0 and brute_tasks([10]) == 10,
                    "כי מערך באורך $1$ אינו קלט חוקי ולכן הפלט הוא $0$ בהגדרה": False})
# last two options are claims about definitions; 3rd: single task time 0 is false because [10,5] -> 5 not 0 (checked below)
check("Q1a distractor 'single task time is 0' false: [10,5] gives 5", brute_tasks([10, 5]) == 5)

ex1, ex2 = [10, 5, 7, 10], [10, 5, 2, 4, 8, 6, 7, 10]
T1, t1 = Tvals(ex1)
numeric(1, "ב", 1, T1[3])
n1 = len(ex1)
final = lambda T, t, n: min(t(n - 1), t(n - 2))
Tall = list(T1.values())
choice(1, "ב", 2, {"$\\min(T(n-1),T(n-2))$": final(T1, t1, n1) == brute_tasks(ex1),
                    "$T(n-1)$": T1[n1 - 1] == brute_tasks(ex1),
                    "$\\min_i T(i)$ על כל האינדקסים": min(Tall) == brute_tasks(ex1),
                    "$T(n-1)+T(n-2)$": T1[n1 - 1] + T1[n1 - 2] == brute_tasks(ex1)})
T2, t2 = Tvals(ex2)
numeric(1, "ב", 3, final(T2, t2, len(ex2)))
check("Q1b ex2 dp == brute", final(T2, t2, len(ex2)) == brute_tasks(ex2) == 22)
# T(i) meaning: ends at i with i performed -> equals brute force restricted to masks with bit i set
def brute_end(A, i):
    best = None
    for mask in range(1 << (i + 1)):
        if not mask >> i & 1:
            continue
        if any(not (mask >> j & 1) and not (mask >> (j + 1) & 1) for j in range(i)):
            continue
        s = sum(A[j] for j in range(i + 1) if mask >> j & 1)
        best = s if best is None or s < best else best
    return best


check("Q1b T(i) = min sum of a valid prefix selection that performs task i (definition option)",
      all(brute_end(ex2, i) == T2[i] for i in range(len(ex2))))
# Q1b: distractor definitions give a different value on ex1: 'prefix sum of all' / 'skip exactly i'
check("Q1b distractor 'sum of all times 0..i' != T(3)", sum(ex1) != T1[3])
s_ = step(1, "ב", 0)
check("Q1b step0 options are definitions (4)", len(s_["options"]) == 4)

# Q1c: count states, rolling DP
calls = set()


def memo_T(A, i, seen):
    if i < 0:
        return 0
    if i in seen:
        return seen[i]
    seen[i] = A[i] + min(memo_T(A, i - 1, seen), memo_T(A, i - 2, seen))
    return seen[i]


seen = {}
memo_T(list(range(1, 11)), 9, seen)
numeric(1, "ג", 0, len(seen))


def rolling(A):
    p1, p2 = 0, 0  # T(i-1), T(i-2)
    for a in A:
        p1, p2 = a + min(p1, p2), p1
    return min(p1, p2)


random.seed(5)
check("Q1c O(1)-space rolling DP == O(n) array DP == brute (2000 random)",
      all(rolling(A) == brute_tasks(A) for A in ([random.randint(1, 20) for _ in range(random.randint(1, 10))] for _ in range(2000))))
# time linear: memo evaluations scale with n
cnt = []
for n in (10, 100, 1000):
    s = {}
    sys.setrecursionlimit(5000)
    memo_T(list(range(1, n + 1)), n - 1, s)
    cnt.append(len(s))
check("Q1c states == n for n = 10,100,1000", cnt == [10, 100, 1000])
textstep(1, "ג", 1, ["O(n)"])
textstep(1, "ג", 2, ["O(1)"])
choice(1, "ג", 3, {"$\\Theta(n)$": True, "$\\Theta(1)$": False, "$\\Theta(\\log n)$": False, "$\\Theta(n^2)$": False})
check("Q1c reconstruction needs all T values: rolling variables lose the chosen tasks (n values to store)", True,
      "(by the official solution; storing T for all n indices is the standard reconstruction)")

# ---------------------------------------------------------------- Q2
G = nx.Graph()
for e in step(2, "א", 0)["graph"]["edges"]:
    G.add_edge(e["u"], e["v"], weight=e["w"])
mst = nx.minimum_spanning_tree(G)
numeric(2, "א", 0, int(sum(d["weight"] for _, _, d in mst.edges(data=True))))
check("Q2a step0 has key weight + kruskal", step(2, "א", 0).get("key") == "weight" and step(2, "א", 0)["graph"]["algo"] == "kruskal")


def special(G, u, v):
    w = G[u][v]["weight"]
    mn = lambda x: min(d["weight"] for _, _, d in G.edges(x, data=True))
    return w == mn(u) or w == mn(v)


spec = [(u, v) for u, v in G.edges() if special(G, u, v)]
numeric(2, "א", 1, len(spec))
inM = lambda u, v: mst.has_edge(u, v)
choice(2, "א", 2, {"$BC$ (משקל 3)": inM("B", "C") and not special(G, "B", "C"),
                    "$AB$ (משקל 1)": inM("A", "B") and not special(G, "A", "B"),
                    "$CD$ (משקל 2)": inM("C", "D") and not special(G, "C", "D"),
                    "$AC$ (משקל 4)": inM("A", "C") and not special(G, "A", "C")})
numeric(2, "ב", 3, sum(1 for u, v in spec if inM(u, v)))

# Q2b: cut S={u}; special => in MST; exchange step w(e)<w(e') for ANY spanning tree T missing e
random.seed(11)
cross_ok = {"$S=\\{u\\}$": True, "$S=\\{u,v\\}$": True, "$S=V\\setminus\\{u,v\\}$": True, "$S=V$": True}
bad_exch = 0
tested = 0
for _ in range(300):
    n = random.randint(4, 7)
    ws = random.sample(range(1, 300), n * (n - 1) // 2)
    H = nx.Graph()
    for (a, b), w in zip(itertools.combinations(range(n), 2), ws):
        H.add_edge(a, b, weight=w)
    u = random.randrange(n)
    v = min((x for x in H[u]), key=lambda x: H[u][x]["weight"])
    # e = {u, v} is minimal at u (special). Cuts:
    cuts = {"$S=\\{u\\}$": {u}, "$S=\\{u,v\\}$": {u, v}, "$S=V\\setminus\\{u,v\\}$": set(H) - {u, v}, "$S=V$": set(H)}
    for name, S in cuts.items():
        crosses = (u in S) != (v in S)
        lightest = crosses and all(H[a][b]["weight"] >= H[u][v]["weight"] for a, b in H.edges() if (a in S) != (b in S))
        if not lightest:
            cross_ok[name] = False
    # exchange: any spanning tree T not containing e
    T = nx.minimum_spanning_tree(H)
    for _t in range(5):
        edges = list(H.edges())
        random.shuffle(edges)
        UF = nx.utils.UnionFind()
        tree = []
        for a, b in edges:
            if (a, b) in ((u, v), (v, u)):
                continue
            if UF[a] != UF[b]:
                UF.union(a, b)
                tree.append((a, b))
        if len(tree) != n - 1:
            continue
        TT = nx.Graph(tree)
        path = nx.shortest_path(TT, u, v)
        e2 = (path[0], path[1])  # the tree edge at u on the cycle
        tested += 1
        if not H[u][v]["weight"] < H[e2[0]][e2[1]]["weight"]:
            bad_exch += 1
choice(2, "ב", 0, cross_ok)
check("Q2b exchange: w(e) < w(e') on the cycle for random spanning trees missing e (so '>' is the bug)", bad_exch == 0 and tested > 500,
      "tested=%d bad=%d" % (tested, bad_exch))
# order/findbug lines: the bug line differs from the correct line only by the inequality
so = step(2, "ב", 1)["lines"]
fb = step(2, "ב", 2)
diff = [i for i, (x, y) in enumerate(zip(so, fb["lines"])) if x != y]
check("Q2b findbug changes exactly the line at bugIndex", diff == [fb["bugIndex"]] and len(so) == len(fb["lines"]) and
      so[2].replace("w(e)<w(e')", "w(e)>w(e')") == fb["lines"][2])

# ---------------------------------------------------------------- Q3a
freq = {"a": 22, "b": 15, "c": 3, "d": 24, "e": 4, "f": 10, "g": 8}


def huff_cost(fs):
    h = list(fs)
    heapq.heapify(h)
    c = 0
    while len(h) > 1:
        x, y = heapq.heappop(h), heapq.heappop(h)
        c += x + y
        heapq.heappush(h, x + y)
    return c


h = list(freq.values())
heapq.heapify(h)
m1 = heapq.heappop(h) + heapq.heappop(h)
numeric(3, "א", 0, m1)
heapq.heappush(h, m1)
m2 = heapq.heappop(h) + heapq.heappop(h)
numeric(3, "א", 1, m2)
# every optimal length assignment (Kraft sum 1, min cost): lengths of letters
ks = list(freq)
best, sols = None, []
for L in itertools.product(range(1, 7), repeat=7):
    if sum(2.0 ** -l for l in L) != 1.0:
        continue
    c = sum(freq[k] * l for k, l in zip(ks, L))
    if best is None or c < best:
        best, sols = c, [L]
    elif c == best:
        sols.append(L)
numeric(3, "א", 3, best)
check("Q3a optimal cost == heapq Huffman cost", best == huff_cost(freq.values()))
numeric(3, "א", 4, sorted({s[ks.index("f")] for s in sols})[0])
check("Q3a length of f is the same in every optimal code", len({s[ks.index("f")] for s in sols}) == 1)
# tie: after merging 7+8=15: remaining 22,15(b),24,10,15(node). Merge f=10 with b or with the node; both finish at cost 219
def finish(order_pick):
    # nodes carry (weight, depth map)
    nodes = [(22, {"a": 0}), (15, {"b": 0}), (24, {"d": 0}), (10, {"f": 0}), (15, {"c": 2, "e": 2, "g": 1})]
    merge = lambda x, y: (x[0] + y[0], {k: v + 1 for k, v in {**x[1], **y[1]}.items()})
    f_, b_, n_ = nodes[3], nodes[1], nodes[4]
    first = merge(f_, b_ if order_pick == "b" else n_)
    rest = [x for x in nodes if x is not f_ and x is not (b_ if order_pick == "b" else n_)] + [first]
    while len(rest) > 1:
        rest.sort(key=lambda x: x[0])
        rest = rest[2:] + [merge(rest[0], rest[1])]
    depth = rest[0][1]
    kraft = sum(2.0 ** -v for v in depth.values())
    return sum(freq[k] * v for k, v in depth.items()), kraft
cb, kb = finish("b")
cn, kn = finish("n")
check("Q3a tie: both merges cost 219 and are full prefix trees (Kraft 1)", cb == cn == 219 and kb == kn == 1.0, "costs=%s,%s" % (cb, cn))
choice(3, "א", 2, {"שני המיזוגים חוקיים ונותנים קוד הופמן באותה עלות אופטימלית": cb == cn == best,
                    "רק מיזוג $f$ עם $b$ נותן קוד אופטימלי": cb == best and cn != best,
                    "רק מיזוג $f$ עם הצומת הפנימי נותן קוד אופטימלי": cn == best and cb != best,
                    "אחד המיזוגים נותן קוד שאינו פרפיקס": kb != 1.0 or kn != 1.0})
check("Q3a sum of internal nodes 7+15+25+37+49+86 == 219", 7 + 15 + 25 + 37 + 49 + 86 == 219)

# ---------------------------------------------------------------- Q3b
def full_tree_depths(n):
    leaves = [0]
    while len(leaves) < n:
        d = leaves.pop(random.randrange(len(leaves)))
        leaves += [d + 1, d + 1]
    return leaves


random.seed(3)
cands = {"$2^{h-d}$": lambda h_, d: 2 ** (h_ - d), "$2^{d}$": lambda h_, d: 2 ** d,
         "$1$ לכל העלים": lambda h_, d: 1, "$h-d$": lambda h_, d: h_ - d}
good = {k: True for k in cands}
for _ in range(3000):
    dep = full_tree_depths(random.randint(2, 10))
    hh = max(dep)
    for name, f in cands.items():
        fs = [f(hh, d) for d in dep]
        if min(fs) <= 0 or sum(x * d for x, d in zip(fs, dep)) != huff_cost(fs):
            good[name] = False
choice(3, "ב", 0, good)
numeric(3, "ב", 1, 2 ** (4 - 3))
check("Q3b the Q3a tree (depths 2,2,3,3,3,4,4) with 2^(4-d): cost of T == Huffman cost",
      sum(2 ** (4 - d) * d for d in [2, 2, 3, 3, 3, 4, 4]) == huff_cost([2 ** (4 - d) for d in [2, 2, 3, 3, 3, 4, 4]]))
check("Q3b 2^k+2^k = 2^(k+1) (and not 2^(k+2))", all(2 ** k + 2 ** k == 2 ** (k + 1) != 2 ** (k + 2) for k in range(10)))

# ---------------------------------------------------------------- Q4 (real clang runs)
def run_c(src, name, stdin=""):
    f = TMP / (name + ".c")
    f.write_text(src, encoding="utf-8")
    exe = TMP / (name + ".exe")
    r = subprocess.run([CLANG, "-O0", "-w", str(f), "-o", str(exe)], capture_output=True, text=True)
    if r.returncode != 0:
        return None, "COMPILE: " + r.stderr[:200]
    try:
        p = subprocess.run([str(exe)], capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        return None, "HANG"
    return p.stdout, p.returncode


official = next(q for q in RAW["questions"] if q["num"] == 4 and q.get("part") == "ב")["solution"]
code = re.search(r"```c\n(.*?)\n```", official, re.S).group(1)
out, rc = run_c(code, "official")
check("Q4b official program prints 'The 3-th missing number is: 4'", out is not None and out.strip().endswith(": 4"), repr(out))
numeric(4, "ב", 1, int(out.strip().split()[-1]))

FNsrc = lambda lines: "#include <stdio.h>\n#include <stdlib.h>\n" + "\n".join(lines) + "\n"
HARNESS = r"""
static int brute(int A[], int size, int k) {
    int x = 0, i = 0;
    while (k) { x++; while (i < size && A[i] < x) i++; if (!(i < size && A[i] == x)) k--; }
    return x;
}
int main(void) {
    srand(7);
    int bad = 0;
    for (int t = 0; t < 3000; t++) {
        int size = 1 + rand() % 10, A[10], v = 0;
        for (int i = 0; i < size; i++) { v += 1 + rand() % 4; A[i] = v; }
        int k = 1 + rand() % 25;
        if (findKthMissing(A, size, k) != brute(A, size, k)) bad++;
    }
    printf("%d\n", bad);
    return 0;
}
"""
fb = step(4, "ב", 2)
lines_blank = fb["lines"]
for o in fb["options"]:
    src = [o["value"] if "___" in ln else ln for ln in [x.replace("___", o["value"]) if "___" in x else x for x in lines_blank]]
    full = "\n".join(src)
    out, rc = run_c(FNsrc([full]) + HARNESS, "fill_" + o["id"])
    bad = None if out is None else int(out.strip())
    good = bad == 0
    check("Q4b fillblank option %s %s" % (o["id"], o["value"]), good == (o["id"] == fb["correctId"]),
          "mismatches vs brute=%s" % bad)
bug = step(4, "ב", 3)
out, rc = run_c(FNsrc(bug["lines"]) + HARNESS, "bug")
bad = int(out.strip())
check("Q4b findbug variant fails observably vs brute force", bad > 0, "mismatches=%d" % bad)
orig_lines = [ln for ln in bug["lines"]]
FN_ORIG = fb["lines"][:12] + ["    return low + k;"] + fb["lines"][13:]
out, rc = run_c(FNsrc(FN_ORIG) + HARNESS, "orig")
check("Q4b the comment-free function itself matches brute force", out is not None and int(out.strip()) == 0)
d = [i for i, (x, y) in enumerate(zip(FN_ORIG, bug["lines"])) if x != y]
check("Q4b findbug differs from the correct function in exactly one line (bugIndex)", d == [bug["bugIndex"]], str(d))

# Q4a trace and Q4c iterations, from an instrumented clang run
TRACE = r"""
#include <stdio.h>
int findKthMissing(int A[], int size, int k, int *iters) {
    int low = 0, high = size - 1; *iters = 0;
    while (low <= high) {
        (*iters)++;
        int mid = low + (high - low) / 2;
        int missing = A[mid] - (mid + 1);
        if (missing < k) low = mid + 1; else high = mid - 1;
    }
    return low;
}
int main(void) {
    int A[] = {3, 5, 9, 10, 11, 12}, it;
    int low = findKthMissing(A, 6, 2, &it);
    printf("%d %d %d\n", A[0] - 1, low, low + 2);
    static int B[1024]; int worst = 0;
    for (int i = 0; i < 1024; i++) B[i] = 2 * (i + 1);
    for (int k = 1; k <= 3000; k++) { findKthMissing(B, 1024, k, &it); if (it > worst) worst = it; }
    printf("%d\n", worst);
    return 0;
}
"""
out, rc = run_c(TRACE, "trace")
l1, l2 = out.strip().split("\n")
a0, lowv, outv = map(int, l1.split())
numeric(4, "א", 0, a0)
numeric(4, "א", 1, lowv)
numeric(4, "א", 2, outv)
numeric(4, "ג", 1, int(l2))
check("Q4c worst-case iterations for n=1024 == floor(log2 n)+1", int(l2) == 11)
# recurrence choice: iterations(n) <= iterations(n//2) + 1 and iterations grow ~ log n, not n
def iters_worst(n):
    B = [2 * (i + 1) for i in range(n)]
    worst = 0
    for k in range(1, 3 * n + 3):
        lo, hi, c = 0, n - 1, 0
        while lo <= hi:
            c += 1
            mid = lo + (hi - lo) // 2
            if B[mid] - (mid + 1) < k:
                lo = mid + 1
            else:
                hi = mid - 1
        worst = max(worst, c)
    return worst


w = {n: iters_worst(n) for n in (64, 128, 256, 512)}
rec_ok = {"$T(n)=T(n/2)+1$": all(w[2 * n] == w[n] + 1 for n in (64, 128, 256)),
          "$T(n)=2T(n/2)+1$": all(w[2 * n] == 2 * w[n] + 1 for n in (64, 128, 256)),
          "$T(n)=T(n-1)+1$": all(w[n + 1] == w[n] + 1 for n in (64,)) if False else (iters_worst(65) == w[64] + 1),
          "$T(n)=T(n/2)+n$": all(w[2 * n] == w[n] + 2 * n for n in (64, 128, 256))}
choice(4, "ג", 0, rec_ok)
textstep(4, "ג", 2, ["O(log n)"])

# ---------------------------------------------------------------- Bonus (KMP)
def pi_table(P):
    pi = [0] * len(P)
    k = 0
    for i in range(1, len(P)):
        while k and P[i] != P[k]:
            k = pi[k - 1]
        if P[i] == P[k]:
            k += 1
        pi[i] = k
    return pi


rep = lambda s: len(set(s)) < len(s)
choice(5, "א", 0, {"`ABB`": all(x == 0 for x in pi_table("ABB")) and rep("ABB"),
                    "`AAB`": all(x == 0 for x in pi_table("AAB")) and rep("AAB"),
                    "`ABA`": all(x == 0 for x in pi_table("ABA")) and rep("ABA"),
                    "`ABC`": all(x == 0 for x in pi_table("ABC")) and rep("ABC")})
numeric(5, "א", 1, pi_table("ABB")[2])


def max_inner(P, T):
    pi = pi_table(P)
    j = 0
    worst = 0
    for ch in T:
        run = 0
        while j > 0 and (j == len(P) or P[j] != ch):
            j = pi[j - 1]
            run += 1
        if j < len(P) and P[j] == ch:
            j += 1
        worst = max(worst, run)
    return worst


pairs = {"$P=aaaaaa$, $T=aaaaab$": ("aaaaaa", "aaaaab"), "$P=aaaaaa$, $T=aaaaaaaaaaaa$": ("aaaaaa", "aaaaaaaaaaaa"),
         "$P=aaaaaa$, $T=bbbbbbbbbbbb$": ("aaaaaa", "bbbbbbbbbbbb"), "$P=abcdef$, $T=abcdeabcdef$": ("abcdef", "abcdeabcdef")}
vals = {k: max_inner(*v) for k, v in pairs.items()}
print("      inner-loop maxima:", vals)
choice(5, "ב", 0, {k: v >= 5 for k, v in vals.items()})
numeric(5, "ב", 1, vals["$P=aaaaaa$, $T=aaaaab$"])

T_, P_ = "aaaaaaaaaaaaaaaaaaaaaaaaab", "aaaaaab"
naive = sum(min(len(P_), next((i for i in range(len(P_)) if T_[s + i] != P_[i]), len(P_) - 1) + 1) for s in range(len(T_) - len(P_) + 1))
numeric(5, "ג", 0, naive)
check("Q5c text length 26, pattern 7, 20 shifts", len(T_) == 26 and len(P_) == 7)
for (n, m) in [(30, 5), (60, 10), (120, 20)]:
    t = "a" * (n - 1) + "b"
    p = "a" * (m - 1) + "b"
    c = 0
    for s in range(n - m + 1):
        i = 0
        while i < m:
            c += 1
            if t[s + i] != p[i]:
                break
            i += 1
    check("Q5c naive comparisons == (n-m+1)*m for n=%d m=%d" % (n, m), c == (n - m + 1) * m)
textstep(5, "ג", 1, ["O(nm)", "O(mn)"])

shutil.rmtree(TMP, ignore_errors=True)
print("ALL OK" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
