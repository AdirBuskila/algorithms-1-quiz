# -*- coding: utf-8 -*-
"""Learn-brief checks: kmp_strings + suffix_structures (briefs 11, 12).
Run: PYTHONUTF8=1 py tools/verify/learn/v09_strings.py     (ASCII output, exits 1 on a failure)"""
import itertools, math, random, sys
from collections import Counter

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


random.seed(8675309)


def rnd(alpha, lo, hi):
    return "".join(random.choice(alpha) for _ in range(random.randint(lo, hi)))


# ================================================================== brief 11
def prefix_function(P):
    """pi[q] for q = 1..m (1-indexed, returned as a list of length m)"""
    m = len(P)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and P[k] != P[q]:
            k = pi[k - 1]
        if P[k] == P[q]:
            k += 1
        pi[q] = k
    return pi


def pi_brute(P):
    out = []
    for q in range(1, len(P) + 1):
        s = P[:q]
        best = 0
        for k in range(1, q):
            if s[:k] == s[q - k:]:
                best = k
        out.append(best)
    return out


bad = sum(prefix_function(P) != pi_brute(P) for P in (rnd("ab", 1, 12) for _ in range(500)))
check("prefix function == brute-force definition (longest proper prefix that is also a suffix) (500 random)", bad == 0)
check("25B-A Q3c: P = ABABBAAABABA -> 0 0 1 2 0 1 1 1 2 3 4 3", prefix_function("ABABBAAABABA") == [0, 0, 1, 2, 0, 1, 1, 1, 2, 3, 4, 3])
check("26B-A Q4e: P = AABAABAABAAA -> 0 1 0 1 2 3 4 5 6 7 8 2", prefix_function("AABAABAABAAA") == [0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 2])
check("lecture KMP example ABABCABAB -> 0 0 1 2 0 1 2 3 4", prefix_function("ABABCABAB") == [0, 0, 1, 2, 0, 1, 2, 3, 4])

# the step-by-step computation of pi[12] for AABAABAABAAA (26B-A Q4e): k = 8 -> 5 -> 2 -> 1 -> 2
P = "AABAABAABAAA"
pi = prefix_function(P)
chain, k = [], pi[10]
while True:
    chain.append(k)
    if P[k] == P[11] or k == 0:
        break
    k = pi[k - 1]
check("26B-A Q4e: for i=12 the fallback chain is k=8 -> 5 -> 2 -> 1 (P[k+1] vs P[12]) and the result is 2", chain == [8, 5, 2, 1] and pi[11] == 2, chain)


def kmp_search(T, P, count_comparisons_of=None):
    n, m = len(T), len(P)
    pi = prefix_function(P)
    q = 0
    occ, inner, cmp_special = [], 0, 0
    for i in range(n):
        while q > 0 and (q == m or P[q] != T[i]):
            if count_comparisons_of is not None and T[i] == count_comparisons_of and q < m:
                cmp_special += 1
            q = pi[q - 1]
            inner += 1
        if count_comparisons_of is not None and T[i] == count_comparisons_of:
            cmp_special += 1
        if P[q] == T[i]:
            q += 1
        if q == m:
            occ.append(i - m + 1)
    return occ, inner, cmp_special


def naive_search(T, P):
    return [i for i in range(len(T) - len(P) + 1) if T[i:i + len(P)] == P]


bad = 0
for _ in range(500):
    T, P = rnd("ab", 0, 20), rnd("ab", 1, 5)
    bad += kmp_search(T, P)[0] != naive_search(T, P)
check("KMP finds exactly the naive occurrences (500 random)", bad == 0)

# 25B-A Q3d : comparisons of the text letter C against pattern letters
P = "ABABBAAABABA"
T = "ABABBAAABAB" + "C" + "XXXX"
occ, inner, cmpC = kmp_search(T, P, "C")
check("25B-A Q3d: the letter C of T is compared 4 times (against P[12], P[5], P[3], P[1])", cmpC == 4, cmpC)

# amortised linearity
bad = 0
for _ in range(300):
    T, P = rnd("ab", 1, 60), rnd("ab", 1, 8)
    occ, inner, _c = kmp_search(T, P)
    bad += inner > len(T)
check("KMP: total number of fallback steps never exceeds n (300 random)", bad == 0)

# 26A-A Q5b : inner loop Theta(m); 26A-B Q5b : O(1)
m = 50
occ, inner, _ = kmp_search("a" * (m - 1) + "b" + "a" * 5, "a" * m)
check("26A-A Q5b: P = a^m, T = a^(m-1) b ...: one mismatch triggers m-1 fallback steps (Theta(m))", inner >= m - 1, inner)
occ, inner, _ = kmp_search("b" * 100, "a" * 20)
check("26A-B Q5b: P = a^m, T = b^n: the fallback loop never runs", inner == 0)

# 26A-A Q5c / 26A-B Q5c : naive search
def naive_comparisons(T, P):
    c = 0
    for i in range(len(T) - len(P) + 1):
        for j in range(len(P)):
            c += 1
            if T[i + j] != P[j]:
                break
    return c

n_, m_ = 60, 10
check("26A-A Q5c: T = a^(n-1)b, P = a^(m-1)b: naive search makes about (n-m+1)*m comparisons (quadratic)",
      naive_comparisons("a" * (n_ - 1) + "b", "a" * (m_ - 1) + "b") >= (n_ - m_) * (m_ - 1))
check("26A-B Q5c: naive is linear when m = 1 or m = n", naive_comparisons("a" * 40, "b") == 40 and naive_comparisons("a" * 40, "a" * 40) == 40)
check("26A-A Q5a: pi all zeros for ABB although B repeats", prefix_function("ABB") == [0, 0, 0])
check("26A-B Q5a: P = a^m gives pi[m] = m-1 (here m=2: [0,1])", prefix_function("aa") == [0, 1] and prefix_function("aaaaa")[-1] == 4)

# existence of pi sequences (22B-A Q1a,b ; 23B-C Q1a)
def exists_pi(seq, alphabet):
    return any(prefix_function("".join(s)) == list(seq) for s in itertools.product(alphabet, repeat=len(seq)))

check("22B-A Q1a: pi = 0,0,0,0,0,1 exists over {a,b} (abbbba)", exists_pi((0, 0, 0, 0, 0, 1), "ab") and prefix_function("abbbba") == [0, 0, 0, 0, 0, 1])
check("22B-A Q1b: pi = 0,0,1,1,2,1 exists over NO alphabet of size 5", not exists_pi((0, 0, 1, 1, 2, 1), "abcde"))
check("the forced string for 0,0,1,1,2,? is abaab and then 'a' gives pi[6]=3, not 1", prefix_function("abaaba")[:5] == [0, 0, 1, 1, 2] and prefix_function("abaaba")[5] == 3)
check("23B-C Q1a: pi = 0,1,2,3,1 exists over no alphabet of size 5; aaaa? gives 4 or 0", not exists_pi((0, 1, 2, 3, 1), "abcde") and prefix_function("aaaaa")[4] == 4 and prefix_function("aaaab")[4] == 0)

# rotation, periodic, border, palindromic prefix, mismatch problem, permutations of the alphabet
bad = 0
for _ in range(500):
    s1 = rnd("ab", 1, 8)
    s2 = rnd("ab", len(s1), len(s1))
    is_rot = any(s1[k:] + s1[:k] == s2 for k in range(len(s1)))
    bad += is_rot != (len(naive_search(s1 + s1, s2)) > 0)
check("S2 is a cyclic rotation of S1 iff S2 occurs in S1S1 (500 random, equal lengths)", bad == 0)

bad = bad2 = 0
for _ in range(600):
    A = rnd("ab", 1, 12)
    n = len(A)
    periodic = any(n % d == 0 and A == A[:d] * (n // d) for d in range(1, n))
    occ = len(naive_search(A + A, A))
    bad += periodic != (occ >= 3)
    pi = prefix_function(A)
    bad2 += periodic != (pi[-1] > 0 and n % (n - pi[-1]) == 0)
check("A = B^k with k>=2 iff A occurs at least 3 times in AA (positions 0, |B|, ..., n) (600 random)", bad == 0)
check("same test with the prefix function: pi[n] > 0 and (n - pi[n]) divides n (600 random)", bad2 == 0)
check("abbabbabbabb is periodic with B=abb, k=4: 5 occurrences in AA", len(naive_search("abbabbabbabb" * 2, "abbabbabbabb")) == 5 and "abb" * 4 == "abbabbabbabb")

bad = 0
for _ in range(400):
    S = rnd("ab", 1, 12)
    longest_border = prefix_function(S)[-1]
    brute = max([k for k in range(1, len(S)) if S[:k] == S[len(S) - k:]] + [0])
    bad += longest_border != brute
check("longest proper prefix that is also a suffix = pi[n] (400 random)", bad == 0)
check("25A-A Q4a: abcabcd -> pi[7] = 0 (the maximum of pi is 3, but not for the whole string); aabcdaabc -> 4; aaaa -> 3",
      prefix_function("abcabcd")[-1] == 0 and max(prefix_function("abcabcd")) == 3 and prefix_function("aabcdaabc")[-1] == 4 and prefix_function("aaaa")[-1] == 3)

bad = 0
for _ in range(400):
    S = rnd("ab", 1, 10)
    brute = max(k for k in range(1, len(S) + 1) if S[:k] == S[:k][::-1])
    pi = prefix_function(S + "#" + S[::-1])
    bad += pi[-1] != brute
check("22A-C Q2: longest palindromic prefix = last pi value of S#S^R (400 random)", bad == 0)
check("22A-C Q2 example: aabaac -> 5", prefix_function("aabaac" + "#" + "caabaa")[-1] == 5)

bad = 0
for _ in range(500):
    T, P = rnd("ab", 1, 15), rnd("ab", 1, 4)
    comp = P.translate(str.maketrans("ab", "ba"))
    want = [i for i in range(len(T) - len(P) + 1) if all(T[i + j] != P[j] for j in range(len(P)))]
    bad += want != naive_search(T, comp)
check("22A-B Q3: positions where every letter differs = occurrences of the complemented pattern over {a,b} (500 random)", bad == 0)

bad = 0
for _ in range(400):
    T, P = rnd("abc", 1, 14), rnd("abc", 1, 4)
    pos = set()
    for perm in itertools.permutations("abc"):
        mp = dict(zip("abc", perm))
        pos |= set(naive_search(T, "".join(mp[c] for c in P)))
    want = set()
    for i in range(len(T) - len(P) + 1):
        w = T[i:i + len(P)]
        f = {}
        okw = True
        for a, b in zip(P, w):
            if f.setdefault(a, b) != b:
                okw = False
        if okw and len(set(f.values())) == len(f):
            want.add(i)
    bad += pos != want
check("23A-B Q3b: matching under a bijection of {a,b,c} = union of 6 KMP searches (400 random)", bad == 0)
check("number of permutations of a 3-letter alphabet is 6", math.factorial(3) == 6)

# Z function and the one-mismatch search (25A-B Q4)
def z_function(s):
    L = len(s)
    Z = [0] * L
    Z[0] = L
    l = r = 0
    for k in range(1, L):
        if k < r:
            Z[k] = min(r - k, Z[k - l])
        while k + Z[k] < L and s[Z[k]] == s[k + Z[k]]:
            Z[k] += 1
        if k + Z[k] > r:
            l, r = k, k + Z[k]
    return Z


def almost(T, P):
    n, m = len(T), len(P)
    Z1 = z_function(P + "#" + T)
    Z2 = z_function(P[::-1] + "#" + T[::-1])
    pre = [Z1[m + 1 + i] for i in range(n)]
    suf = [Z2[m + 1 + (n - 1 - i)] for i in range(n)]
    return [i for i in range(n - m + 1) if pre[i] >= m or pre[i] + suf[i + m - 1] >= m - 1]


def almost_brute(T, P):
    return [i for i in range(len(T) - len(P) + 1) if sum(a != b for a, b in zip(T[i:i + len(P)], P)) <= 1]


bad = 0
for _ in range(600):
    T, P = rnd("ab", 1, 16), rnd("ab", 1, 5)
    bad += almost(T, P) != almost_brute(T, P)
check("25A-B Q4: Z-function method == brute force 'at most one mismatch' (600 random)", bad == 0)

# ================================================================== brief 12
def suffix_array(T):
    return sorted(range(len(T)), key=lambda i: T[i:])


check("23B-C Q1b: suffix array of algogoal (1-based) = 7 1 5 3 8 2 6 4", [i + 1 for i in suffix_array("algogoal")] == [7, 1, 5, 3, 8, 2, 6, 4])
check("with the terminator '$' (smallest) : 9 7 1 5 3 8 2 6 4", [i + 1 for i in sorted(range(9), key=lambda i: ("algogoal$"[i:]))] == [9, 7, 1, 5, 3, 8, 2, 6, 4])
sa = [i + 1 for i in suffix_array("BANANABAN")]
check("24B-A Q5: the true suffix array of BANANABAN is 6 8 4 2 7 1 9 5 3 ; the exam's 6 8 2 4 7 1 9 5 3 has 2 and 4 swapped",
      sa == [6, 8, 4, 2, 7, 1, 9, 5, 3] and sa != [6, 8, 2, 4, 7, 1, 9, 5, 3], sa)


def internal_nodes(T):
    """strings that label internal nodes of the suffix tree of T$ : right-branching substrings (>= 2 different next chars, $ counts)"""
    S = T + "$"
    nxt = {}
    for i in range(len(S)):
        for j in range(i, len(S)):
            sub = S[i:j]
            if j < len(S):
                nxt.setdefault(sub, set()).add(S[j])
    return sorted(w for w, c in nxt.items() if len(c) >= 2 and w != "")


def suffix_tree_nodes(T):
    internal = internal_nodes(T)
    return 1 + len(internal) + (len(T) + 1)


check("22B-B Q1c: internal nodes of the suffix tree of ABABABA are A, ABA, ABABA, BA, BABA ; 8 leaves ; 14 nodes with the root",
      internal_nodes("ABABABA") == ["A", "ABA", "ABABA", "BA", "BABA"] and suffix_tree_nodes("ABABABA") == 14)
check("23B-C Q1b: internal nodes of the suffix tree of algogoal$ are al, go, l, o ; 9 leaves", internal_nodes("algogoal") == ["al", "go", "l", "o"])
bad = 0
for _ in range(300):
    T = rnd("ab", 1, 14)
    bad += suffix_tree_nodes(T) > 2 * (len(T) + 1)
check("a suffix tree of a text of length n has at most 2(n+1) nodes (300 random)", bad == 0)


def longest_repeated(T):
    best = ""
    for L in range(len(T), 0, -1):
        c = Counter(T[i:i + L] for i in range(len(T) - L + 1))
        reps = [s for s, k in c.items() if k >= 2]
        if reps:
            return sorted(reps)
    return []


check("22B-B Q1d: longest repeated substring of ABABABA is ABABA (positions 0 and 2)", longest_repeated("ABABABA") == ["ABABA"] and [i for i in range(3) if "ABABABA".startswith("ABABA", i)] == [0, 2])
check("deepest internal node = longest repeated substring (300 random)", all(
    (sorted(internal_nodes(T), key=lambda s: -len(s))[0] if internal_nodes(T) else "") in (longest_repeated(T) or [""]) or not longest_repeated(T)
    for T in (rnd("ab", 2, 12) for _ in range(300))))
T = "RATATAT"
check("24B-B Q5: for RATATAT the longest repeated substring is ATAT (deepest internal node); internal nodes AT, ATAT, T, TAT", longest_repeated(T) == ["ATAT"], internal_nodes(T))


def lcs_sub(a, b):
    best = 0
    out = set()
    for L in range(min(len(a), len(b)), 0, -1):
        sa_ = {a[i:i + L] for i in range(len(a) - L + 1)}
        sb_ = {b[i:i + L] for i in range(len(b) - L + 1)}
        if sa_ & sb_:
            return sorted(sa_ & sb_)
    return []


check("23A-A Q2b: BADAEAT and CAEADAS : longest common substrings are ADA and AEA (length 3)", lcs_sub("BADAEAT", "CAEADAS") == ["ADA", "AEA"])


# generalised suffix tree: internal node marked by both strings = common substring
def common_nodes(S1, S2):
    S = S1 + "$" + S2 + "*"
    origin = {}
    best = []
    sufs = [(S[i:], 0 if i <= len(S1) else 1) for i in range(len(S))]
    # a substring w without terminators is common iff some suffix of each string starts with w
    cand = {S1[i:j] for i in range(len(S1)) for j in range(i + 1, len(S1) + 1)} & {S2[i:j] for i in range(len(S2)) for j in range(i + 1, len(S2) + 1)}
    return max(cand, key=len) if cand else ""


check("generalised tree reasoning: the longest common substring has length 3", len(common_nodes("BADAEAT", "CAEADAS")) == 3)

# 23A-B Q3a : frequencies of all substrings of length 4 via the sorted suffixes
words = ["abcab", "bcabc", "ccbca"]
S = "".join(w + "$%d" % i for i, w in enumerate(words))
cnt = Counter()
for w in words:
    for i in range(len(w) - 3):
        cnt[w[i:i + 4]] += 1
sufs = sorted(S[i:] for i in range(len(S)))
via = Counter()
for s in sufs:
    pre = s[:4]
    if len(pre) == 4 and all(c in "abc" for c in pre):
        via[pre] += 1
check("23A-B Q3a: counting suffixes with each length-4 prefix (no terminator) = frequency of that substring", via == cnt, dict(cnt))

# searching with a suffix array : the occurrences of w are the contiguous block of suffixes starting with w
bad = 0
for _ in range(300):
    T, w = rnd("ab", 1, 14), rnd("ab", 1, 3)
    SA = suffix_array(T)
    block = [i for i in SA if T[i:i + len(w)] == w]
    contiguous = [k for k, i in enumerate(SA) if T[i:i + len(w)] == w]
    bad += bool(sorted(block) != naive_search(T, w) or (contiguous and contiguous != list(range(contiguous[0], contiguous[-1] + 1))))
check("25A-A Q4b: the suffixes that start with w form one contiguous block of the suffix array; their number = number of occurrences (300 random)", bad == 0)

# suffix trie size (naive) for banana$ : n(n+1)/2 + ... count distinct substrings of banana$ + root
sub_banana = {("banana$")[i:j] for i in range(7) for j in range(i + 1, 8)}
check("SAMP-1 Q5: the suffix trie of banana$ has %d nodes (distinct non-empty substrings + the root)" % (len(sub_banana) + 1), len(sub_banana) + 1 == 23, len(sub_banana) + 1)

check("banana$: suffix tree has root + internal nodes a, ana, na + 7 leaves = 11 nodes (the trie has 23)", internal_nodes("banana") == ["a", "ana", "na"] and suffix_tree_nodes("banana") == 11)

# structure of the suffix tree of ABABABA$ (0-based leaf labels): edge labels from the root
def tree_edges(T):
    S = T + "$"
    internal = set(internal_nodes(T)) | {""}
    edges = []
    for node in sorted(internal, key=lambda w: (len(w), w)):
        children = {}
        for i in range(len(S)):
            if S[i:].startswith(node) and len(S) - i > len(node):
                children.setdefault(S[i + len(node)], []).append(i)
        for ch, starts in sorted(children.items()):
            # extend the edge until the next internal node or the end of the suffix
            L = 1
            while True:
                lab = node + S[starts[0] + len(node):starts[0] + len(node) + L]
                if lab in internal or all(len(S) - i == len(lab) for i in starts) or len(starts) == 1:
                    break
                L += 1
            if len(starts) == 1:
                lab = S[starts[0]:]
            edges.append((node or "root", lab[len(node):], lab if lab in internal else "leaf %d" % starts[0]))
    return edges

e = tree_edges("ABABABA")
want = [("root", "$", "leaf 7"), ("root", "A", "A"), ("root", "BA", "BA"), ("A", "$", "leaf 6"), ("A", "BA", "ABA"), ("BA", "$", "leaf 5"), ("BA", "BA", "BABA"),
        ("ABA", "$", "leaf 4"), ("ABA", "BA", "ABABA"), ("BABA", "$", "leaf 3"), ("BABA", "BA$", "leaf 1"), ("ABABA", "$", "leaf 2"), ("ABABA", "BA$", "leaf 0")]
check("22B-B Q1c: edge structure of the suffix tree of ABABABA$ (leaf labels = start index from 0)", sorted(e) == sorted(want), sorted(set(e) ^ set(want)))

check("brief 11 worked example: pi = 0,1,2,1 exists over no alphabet of size 4", not exists_pi((0, 1, 2, 1), "abcd") and prefix_function("aaaa") == [0, 1, 2, 3] and prefix_function("aaab") == [0, 1, 2, 0])

sa = [i + 1 for i in suffix_array("banana")]
check("brief 12 worked example: SA(banana) = 6 4 2 1 5 3 ; 'ana' occurs at 2 and 4 (block ana, anana)",
      sa == [6, 4, 2, 1, 5, 3] and naive_search("banana", "ana") == [1, 3])

sys.exit(0 if ok else 1)
