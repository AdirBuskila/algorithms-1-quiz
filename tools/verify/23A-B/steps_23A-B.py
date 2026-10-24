# -*- coding: utf-8 -*-
"""Step-value checks for 23A-B (algorithms-1). Run: PYTHONUTF8=1 py -I tools/verify/23A-B/steps_23A-B.py
Recomputes every numeric / trace / complexity answer used in the guided steps, shows that each choice-distractor fails
on some input, and binds the results to tools/raw/23A-B.json. ASCII output."""
import heapq, itertools, json, math, pathlib, random
from collections import Counter
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
RAW = json.loads((HERE.parents[1] / "raw" / "23A-B.json").read_text(encoding="utf-8"))
ok = True
random.seed(31)


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


def step(num, part, idx):
    for q in RAW["questions"]:
        if q["num"] == num and q.get("part", "") == part:
            return q["steps"][idx]
    raise KeyError((num, part))


def bind_numeric(num, part, idx, expected, label):
    s = step(num, part, idx)
    check(f"bind {label}: numeric step {idx} == {expected}", s["type"] == "numeric" and s["answer"] == expected)


def bind_choice(num, part, idx, text, label):
    s = step(num, part, idx)
    got = [o["value"] for o in s["options"] if o["id"] == s["correctId"]]
    check(f"bind {label}: choice step {idx} correct option", s["type"] == "choice" and got == [text], got)


def bind_text(num, part, idx, expected, label):
    s = step(num, part, idx)
    check(f"bind {label}: text step {idx} accepts {expected}", s["type"] == "text" and expected in s["accept"])


# ======================= Q1: snake path =======================
def brute_snake_all(A):
    n = len(A)
    best = 0

    def dfs(i, j):
        r = 1
        for ni, nj in ((i, j + 1), (i + 1, j)):
            if ni < n and nj < n and abs(A[i][j] - A[ni][nj]) <= 1:
                r = max(r, 1 + dfs(ni, nj))
        return r
    return max(dfs(i, j) for i in range(n) for j in range(n))


def T_table(A, both_rule="max"):
    n = len(A)
    T = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            a = A[i - 1][j - 1]
            left = j > 1 and abs(a - A[i - 1][j - 2]) <= 1
            up = i > 1 and abs(a - A[i - 2][j - 1]) <= 1
            if left and up:
                x, y = T[i][j - 1], T[i - 1][j]
                T[i][j] = {"max": 1 + max(x, y), "min": 1 + min(x, y), "sum": x + y, "nopl1": max(x, y)}[both_rule]
            elif left:
                T[i][j] = 1 + T[i][j - 1]
            elif up:
                T[i][j] = 1 + T[i - 1][j]
            else:
                T[i][j] = 1
    return T


M = [[10, 20, 30, 40, 50], [20, 10, 7, 20, 40], [30, 20, 8, 8, 30], [40, 30, 20, 9, 20], [50, 40, 30, 20, 30]]
routes = 0
valid = 0
for moves in set(itertools.permutations("DRD")):
    i, j = 1, 2
    cells = [M[i][j]]
    for mv in moves:
        i, j = (i + 1, j) if mv == "D" else (i, j + 1)
        cells.append(M[i][j])
    routes += 1
    valid += all(abs(cells[k] - cells[k + 1]) <= 1 for k in range(3))
check("Q1a every monotone route (2,3) -> (4,4) has 4 cells (3 moves: 2 down, 1 right); 3 routes, exactly 1 valid",
      routes == 3 and valid == 1)
bind_numeric(1, "א", 0, 4, "Q1a")
bind_numeric(1, "א", 1, 1, "Q1a")

EX = [[10, 1, 3], [12, 2, 2], [1, 2, 1]]
T = T_table(EX)
check("Q1b example 3x3: T(2,2)=2, T(3,3)=4, max T = 4 = brute force", T[2][2] == 2 and T[3][3] == 4 and brute_snake_all(EX) == 4
      and max(max(r) for r in T) == 4)
bind_numeric(1, "ב", 0, 2, "Q1b")
bind_numeric(1, "ב", 1, 4, "Q1b")
for rule in ("min", "sum", "nopl1"):
    bad = 0
    for _ in range(2000):
        n = random.randint(2, 5)
        A = [[random.randint(0, 3) for _ in range(n)] for _ in range(n)]
        bad += max(max(r) for r in T_table(A, rule)) != brute_snake_all(A)
    check(f"Q1b distractor rule '{rule}' disagrees with brute force on some array", bad > 0, bad)
bad = 0
for _ in range(2000):
    n = random.randint(1, 6)
    A = [[random.randint(0, 3) for _ in range(n)] for _ in range(n)]
    bad += max(max(r) for r in T_table(A)) != brute_snake_all(A)
check("Q1b correct rule 1+max equals brute force on 2000 arrays", bad == 0)
bind_choice(1, "ב", 2, r"$1+\max\bigl(T(i-1,j),\,T(i,j-1)\bigr)$", "Q1b")


def rolling_len(A):
    n = len(A)
    prev = [0] * (n + 1)
    best, stored = 0, 0
    for i in range(1, n + 1):
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            a = A[i - 1][j - 1]
            left = j > 1 and abs(a - A[i - 1][j - 2]) <= 1
            up = i > 1 and abs(a - A[i - 2][j - 1]) <= 1
            cur[j] = 1 + max(cur[j - 1] if left else 0, prev[j] if up else 0)
            best = max(best, cur[j])
        stored = max(stored, len(prev) - 1 + len(cur) - 1)
        prev = cur
    return best, stored


bad = 0
for _ in range(1500):
    n = random.randint(1, 6)
    A = [[random.randint(0, 3) for _ in range(n)] for _ in range(n)]
    best, stored = rolling_len(A)
    bad += best != brute_snake_all(A) or stored != 2 * n
check("Q1c two rows (2n cells) suffice for the length, on 1500 arrays", bad == 0)
bind_text(1, "ג", 0, "O(n^2)", "Q1c time")
bind_text(1, "ג", 1, "O(n^2)", "Q1c space")
bind_numeric(1, "ג", 2, 2 * 5, "Q1c")

# ======================= Q2: GPT detection =======================
for n in (4, 6, 10):
    exposed = all(any(q not in good for q in qs) for good in itertools.combinations(range(n), n // 2)
                  for qs in itertools.combinations(range(n), n // 2 + 1))
    hidden = any(all(q in good for q in qs) for good in itertools.combinations(range(n), n // 2)
                 for qs in itertools.combinations(range(n), n // 2))
    check(f"Q2a n={n}: n/2+1 questions always expose a half-right model; n/2 questions may not", exposed and hidden)
bind_numeric(2, "א", 0, 10 // 2 + 1, "Q2a")
bind_text(2, "א", 1, "O(mn)", "Q2a time")

for n, k in ((40, 3), (40, 7), (20, 3)):
    p = math.comb(n // 2, k) / math.comb(n, k)
    check(f"Q2b survival of a half-right model, n={n}, k={k}: {p:.4f} <= (1/2)^k", p <= 0.5 ** k)
check("Q2b (1/2)^3 = 0.125", 0.5 ** 3 == 0.125)
bind_numeric(2, "ב", 0, 0.125, "Q2b")
kmin = next(k for k in range(1, 30) if 0.5 ** k < 0.01)
check("Q2b smallest k with (1/2)^k < 0.01 is 7", kmin == 7 and 0.5 ** 6 >= 0.01)
bind_numeric(2, "ב", 1, kmin, "Q2b")
# one-sided error: flagging 'sometimes wrong' is certain, 'always right' can be wrong
false_flag, missed = 0, 0
for _ in range(20000):
    n, k = 12, 3
    qs = random.sample(range(n), k)
    right = set(random.sample(range(n), n // 2))
    half = random.random() < 0.5
    flagged = half and any(q not in right for q in qs)
    if flagged is True and not half:
        false_flag += 1
    if half and not flagged:
        missed += 1
check("Q2b a model flagged 'sometimes wrong' is certainly half-right; a half-right model can pass as 'always right'",
      false_flag == 0 and missed > 0, f"missed={missed}")
bind_choice(2, "ב", 2, "אם מחשב סומן כשוגה לפעמים זה בטוח; אם סומן כצודק תמיד ייתכן שהוא טועה", "Q2b")
bind_text(2, "ב", 3, "O(mk)", "Q2b time")

random.seed(5)
tot = 0
for _ in range(60000):
    right = set(random.sample(range(40), 20))
    c = 0
    while True:
        c += 1
        if random.randrange(40) not in right:
            break
    tot += c
check("Q2c expected questions to expose a half-right model is 2 (mean %.3f)" % (tot / 60000), abs(tot / 60000 - 2) < 0.05)
bind_numeric(2, "ג", 0, 2, "Q2c")
bind_choice(2, "ג", 1, "כשנחשפו $m/2$ מחשבים ששוגים לפעמים: כל השאר בוודאי צודקים תמיד", "Q2c")

# ======================= Q3a: 4-mer frequencies =======================
words = ["".join(random.choice("ACGT") for _ in range(50)) for _ in range(40)]
truth = Counter(w[i:i + 4] for w in words for i in range(len(w) - 3))
check("Q3a total frequency = words * (50 - 3) (1000 words -> 47000)", sum(truth.values()) == len(words) * 47 and 1000 * 47 == 47000)
bind_numeric(3, "א", 1, 47000, "Q3a")
text = "".join(w + "$%d$" % (i + 1) for i, w in enumerate(words))
sa = sorted(range(len(text)), key=lambda s: text[s:])
groups = Counter()
for s in sa:   # leaves of the suffix tree in left-to-right order; a depth-4 node = a contiguous range sharing a 4-prefix
    pre = text[s:s + 4]
    if len(pre) == 4 and all(c in "ACGT" for c in pre):
        groups[pre] += 1
check("Q3a number of leaves under the depth-4 node of a 4-mer == its frequency (suffix array ranges)", groups == truth)
check("Q3a without markers some suffixes would cross word boundaries (4-mers spanning two words exist)",
      sum(1 for i in range(len(words) - 1) for t in range(1, 4)
          if len((words[i] + words[i + 1])[len(words[i]) - 4 + t: len(words[i]) + t]) == 4) > 0)
bind_choice(3, "א", 0, "מספר העלים בתת-העץ של הצומת שמייצג אותה", "Q3a")

# ======================= Q3b: pattern under letter permutation =======================
def kmp_all(Tx, P):
    m = len(P)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k and P[k] != P[q]:
            k = pi[k - 1]
        if P[k] == P[q]:
            k += 1
        pi[q] = k
    out, k = [], 0
    for i, ch in enumerate(Tx):
        while k and (k == m or P[k] != ch):
            k = pi[k - 1]
        if P[k] == ch:
            k += 1
        if k == m:
            out.append(i - m + 1)
    return out


def official_perm(Tx, P):
    hits = set()
    for perm in itertools.permutations("abc"):
        f = dict(zip("abc", perm))
        hits.update(kmp_all(Tx, "".join(f[c] for c in P)))
    return sorted(hits)


def brute_perm(Tx, P):
    return [s for s in range(len(Tx) - len(P) + 1)
            if any(all(Tx[s + t] == dict(zip("abc", pm))[P[t]] for t in range(len(P))) for pm in itertools.permutations("abc"))]


check("Q3b there are 3! = 6 bijections of {a,b,c}", len(list(itertools.permutations("abc"))) == 6)
bind_numeric(3, "ב", 0, 6, "Q3b")
pats = {"".join(dict(zip("abc", pm))[c] for c in "aaa") for pm in itertools.permutations("abc")}
check("Q3b the pattern aaa yields only 3 distinct patterns under the 6 bijections", len(pats) == 3)
bind_numeric(3, "ב", 1, 3, "Q3b")
Tx, P = "abccbaabb", "abb"
hits = official_perm(Tx, P)
check("Q3b T=abccbaabb, P=abb: 3 positions (1, 4, 6), six KMP runs == brute force", hits == brute_perm(Tx, P) == [1, 4, 6])
bind_numeric(3, "ב", 2, 3, "Q3b")
bind_text(3, "ב", 3, "O(n+m)", "Q3b time")

# ======================= Q4a: Huffman cost 13 =======================
def huff(freqs):
    h = [(f, i, [i]) for i, f in enumerate(freqs)]
    heapq.heapify(h)
    L = [0] * len(freqs)
    merges = []
    c = len(freqs)
    while len(h) > 1:
        f1, _, s1 = heapq.heappop(h)
        f2, _, s2 = heapq.heappop(h)
        merges.append((f1, f2, s1 + s2))
        for i in s1 + s2:
            L[i] += 1
        heapq.heappush(h, (f1 + f2, c, s1 + s2))
        c += 1
    return L, merges


L, merges = huff([3, 2, 1, 1])
check("Q4a f=(3,2,1,1): the first merge joins c and d (indices 2,3), then 2+2=4, root 7; cost 13",
      sorted(merges[0][2]) == [2, 3] and merges[1][0] + merges[1][1] == 4 and merges[2][0] + merges[2][1] == 7
      and sum(f * l for f, l in zip([3, 2, 1, 1], L)) == 13)
bind_choice(4, "א", 0, "$c$ ו-$d$", "Q4a")
bind_numeric(4, "א", 1, 4, "Q4a")
bind_numeric(4, "א", 2, 13, "Q4a")


# ======================= Q4b: spanning trees =======================
def n_trees(G):
    nodes = list(G)
    idx = {v: i for i, v in enumerate(nodes)}
    n = len(nodes)
    Lm = [[0] * n for _ in range(n)]
    for u, v in G.edges():
        i, j = idx[u], idx[v]
        Lm[i][i] += 1
        Lm[j][j] += 1
        Lm[i][j] -= 1
        Lm[j][i] -= 1
    from fractions import Fraction
    Mx = [[Fraction(x) for x in r[1:]] for r in Lm[1:]]
    det, m = Fraction(1), len(Mx)
    for c in range(m):
        p = next((r for r in range(c, m) if Mx[r][c] != 0), None)
        if p is None:
            return 0
        if p != c:
            Mx[c], Mx[p] = Mx[p], Mx[c]
            det = -det
        det *= Mx[c][c]
        for r in range(c + 1, m):
            f = Mx[r][c] / Mx[c][c]
            for k in range(c, m):
                Mx[r][k] -= f * Mx[c][k]
    return int(det)


mx3 = max(n_trees(nx.complete_graph(3)), 1)
check("Q4b triangle K3 has 3 spanning trees, the maximum on 3 vertices", mx3 == 3 == n_trees(nx.complete_graph(3)))
bind_numeric(4, "ב", 0, 3, "Q4b")
check("Q4b the 4-cycle has 4 spanning trees (< 5)", n_trees(nx.cycle_graph(4)) == 4)
bind_numeric(4, "ב", 1, 4, "Q4b")
G = nx.Graph([("TL", "TR"), ("TL", "BL"), ("TL", "BR"), ("TR", "BR"), ("BL", "BR")])
brute = sum(1 for es in itertools.combinations(G.edges(), 3) if nx.is_tree(nx.Graph(list(es))) and len({x for e in es for x in e}) == 4)
check("Q4b the official drawing (K4 minus an edge) has 8 spanning trees (Kirchhoff == brute force)", n_trees(G) == brute == 8)
bind_numeric(4, "ב", 2, 8, "Q4b")
check("Q4b all weights 1: every spanning tree is minimum, weight 3", nx.minimum_spanning_tree(G).size() == 3)
bind_numeric(4, "ב", 3, 3, "Q4b")

# ======================= Q5: vertex cover 2-approximation =======================
def approx_vc(G, rng):
    E = [tuple(e) for e in G.edges()]
    rng.shuffle(E)
    C, M = set(), []
    while E:
        a, b = E[0]
        C |= {a, b}
        M.append((a, b))
        E = [e for e in E if a not in e and b not in e]
    return C, M


def opt_vc(G):
    V = list(G)
    for r in range(len(V) + 1):
        for S in itertools.combinations(V, r):
            s = set(S)
            if all(u in s or v in s for u, v in G.edges()):
                return r


rng = random.Random(3)
all_ok, matching_ok = True, True
for _ in range(300):
    n = random.randint(2, 9)
    Gr = nx.gnp_random_graph(n, random.random() * 0.7 + 0.15, seed=random.randint(0, 10 ** 6))
    if Gr.number_of_edges() == 0:
        continue
    C, Mt = approx_vc(Gr, rng)
    verts = [x for e in Mt for x in e]
    matching_ok &= len(verts) == len(set(verts)) and len(C) == 2 * len(Mt)
    all_ok &= all(u in C or v in C for u, v in Gr.edges()) and len(C) <= 2 * opt_vc(Gr)
check("Q5 the chosen edges form a matching, |C| = 2|M| <= 2 OPT, C is a cover (300 graphs)", matching_ok and all_ok)
K = nx.complete_bipartite_graph(3, 3)
sizes = {len(approx_vc(K, random.Random(s))[0]) for s in range(200)}
check("Q5 K_{3,3}: the algorithm returns 6 for every edge order, the optimum is 3; max degree is 3 (> 2)",
      sizes == {6} and opt_vc(K) == 3 and max(d for _, d in K.degree()) == 3)
bind_choice(5, "", 0, "כיסוי קודקודים מינימלי: אנשים הם קודקודים, שיחות הן קשתות, ובוחרים קבוצה שנוגעת בכל קשת", "Q5 reduction")
bind_choice(5, "", 1, "הקשתות שנבחרו הן זיווג, וכל כיסוי חייב להכיל קודקוד מכל אחת מהן, ולכן $|C|=2|M|\\le 2\\cdot OPT$", "Q5 ratio")
bind_numeric(5, "", 2, 6, "Q5")
bind_numeric(5, "", 3, 3, "Q5")

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
