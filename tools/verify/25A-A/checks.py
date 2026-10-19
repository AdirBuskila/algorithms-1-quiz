# -*- coding: utf-8 -*-
"""Verification harness for 25A-A (algorithms-1). Run: PYTHONUTF8=1 py tools/verify/25A-A/checks.py
Checks the official answers (never modifies them). ASCII output."""
import itertools, random
from functools import lru_cache

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


# ---------- Q1a: official Mid pseudocode (base case i=j tested first) ----------
def mid(A, i, j, B, k, l):
    """1-indexed inclusive ranges of equal even-or-1 length; returns the median of the union."""
    if i == j:
        return (A[i] + B[k]) / 2
    a1, a2 = A[(i + j - 1) // 2], A[(i + j + 1) // 2]
    b1, b2 = B[(k + l - 1) // 2], B[(k + l + 1) // 2]
    if a1 < b1 < b2 < a2:
        return (b1 + b2) / 2
    if b1 < a1 < a2 < b2:
        return (a1 + a2) / 2
    ma, mb = (i + j - 1) // 2, (k + l - 1) // 2
    if a1 < b1:   # cases 4,5: keep A upper half, B lower half
        return mid(A, ma + 1, j, B, k, mb)
    return mid(A, i, ma, B, mb + 1, l)   # cases 6,7: keep A lower half, B upper half


def median_brute(A, B):
    s = sorted(A + B)
    n = len(s)
    return (s[n // 2 - 1] + s[n // 2]) / 2


random.seed(11)
bad = 0
for _ in range(3000):
    m = random.choice([1, 2, 4, 8, 16])
    vals = random.sample(range(1, 200), 2 * m)
    A = sorted(vals[:m])
    B = sorted(vals[m:])
    if mid([0] + A, 1, m, [0] + B, 1, m) != median_brute(A, B):
        bad += 1
check("Q1a official Mid (base case first, 4 recursive cases) equals the brute-force median (3000 random)", bad == 0,
      "bad=%d" % bad)

# ---------- Q1c: mid(A[1..r],B[1..r]) is NOT the r-th smallest of the union ----------
A, B, r = [1, 2], [3, 4], 2
kth = sorted(A + B)[r - 1]
check("Q1c official 'Return(mid(A[1..r],B[1..r]))' gives the average of two middles, not the r-th smallest",
      median_brute(A[:r], B[:r]) == 2.5 and kth == 2)

# ---------- Q2a: recurrence as printed in the official solution ----------
def interleave_brute(s1, s2, s3):
    if len(s3) != len(s1) + len(s2):
        return False
    n = len(s3)
    for pos in itertools.combinations(range(n), len(s1)):
        a = [s3[p] for p in pos]
        b = [s3[p] for p in range(n) if p not in pos]
        if "".join(a) == s1 and "".join(b) == s2:
            return True
    return False


def printed(s1, s2, s3):
    """The official piecewise recurrence exactly as printed (rows 3 and 8 keep k)."""
    @lru_cache(None)
    def T(i, j, k):
        if i == j == k == 0:
            return True
        if i > 0 and j > 0 and k > 0:
            e1, e2 = s1[i - 1] == s3[k - 1], s2[j - 1] == s3[k - 1]
            if e1 and e2:
                return T(i - 1, j, k - 1) or T(i, j - 1, k - 1)
            if e1 and not e2:
                return T(i - 1, j, k - 1)
            if not e1 and e2:
                return T(i, j - 1, k)          # printed: k is not decremented
            return None                        # case missing from the printed recurrence
        if i > 0 and k > 0 and j == 0:
            return False if s1[i - 1] != s3[k - 1] else T(i - 1, j, k - 1)
        if j > 0 and k > 0 and i == 0:
            return False if s2[j - 1] != s3[k - 1] else T(i, j - 1, k)   # printed: k not decremented
        return None
    return T(len(s1), len(s2), len(s3))


random.seed(3)
bad = 0
undefined = 0
for _ in range(2000):
    s1 = "".join(random.choice("ab") for _ in range(random.randint(0, 3)))
    s2 = "".join(random.choice("ab") for _ in range(random.randint(0, 3)))
    s3 = "".join(random.choice("ab") for _ in range(len(s1) + len(s2)))
    r = printed(s1, s2, s3)
    if r is None:
        undefined += 1
    elif r != interleave_brute(s1, s2, s3):
        bad += 1
check("Q2a printed recurrence disagrees with brute force or is undefined (confirms the typo, key held)",
      bad + undefined > 0, "wrong=%d undefined=%d of 2000" % (bad, undefined))
check("Q2a with k decremented in rows 3 and 8 and a false row for the missing case it would be correct (sanity of idea)",
      interleave_brute("abc", "def", "adbcef") and not interleave_brute("abc", "def", "bdacef")
      and not interleave_brute("abc", "def", "adbce") and interleave_brute("abc", "dec", "adbcec"))

# ---------- Q3: greedy max count with sum <= n ----------
def greedy(L, n):
    L = sorted(L)
    s = c = 0
    for x in L:
        if s + x <= n:
            s += x
            c += 1
        else:
            return c
    return c


def brute_count(L, n):
    best = 0
    for mask in range(1 << len(L)):
        sub = [L[i] for i in range(len(L)) if mask >> i & 1]
        if sum(sub) <= n:
            best = max(best, len(sub))
    return best


check("Q3 example n=6, L=[2,5,3,8,10] -> 2", greedy([2, 5, 3, 8, 10], 6) == 2 == brute_count([2, 5, 3, 8, 10], 6))
bad = 0
for _ in range(3000):
    L = [random.randint(1, 12) for _ in range(random.randint(1, 8))]
    n = random.randint(1, 40)
    if greedy(L, n) != brute_count(L, n):
        bad += 1
check("Q3a official Greedy-Subset-Sum equals brute force (3000 random)", bad == 0, "bad=%d" % bad)

# ---------- Q4a: pi array; the official note says 'return the maximum of pi' ----------
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


def longest_border(S):
    for L in range(len(S) - 1, 0, -1):
        if S[:L] == S[-L:]:
            return L
    return 0


check("Q4a pi[n-1] equals the longest proper border (brute force, ab strings n<=10)",
      all(pi_table(S)[-1] == longest_border(S) for n in range(1, 11) for S in map("".join, itertools.product("ab", repeat=n))))
check("Q4a 'max of pi' differs from pi[n-1] on abcabcd (official note unsafe)",
      max(pi_table("abcabcd")) == 3 and pi_table("abcabcd")[-1] == 0)
check("Q4a example aabcdaabc -> 4", pi_table("aabcdaabc")[-1] == 4)


# ---------- Q4b: official suffix-tree search on a compacted suffix tree ----------
class Node:
    def __init__(self):
        self.letters = ""
        self.children = []   # sorted by first letter
        self.leaf = None


def build(T):
    T = T + "$"
    root = Node()

    def insert(node, s, idx):
        # find child starting with s[0]
        for ch in node.children:
            if ch.letters[0] == s[0]:
                L = 0
                while L < len(ch.letters) and L < len(s) and ch.letters[L] == s[L]:
                    L += 1
                if L == len(ch.letters):
                    return insert(ch, s[L:], idx)
                mid = Node()
                mid.letters = ch.letters[:L]
                ch.letters = ch.letters[L:]
                mid.children = [ch]
                node.children[node.children.index(ch)] = mid
                leaf = Node()
                leaf.letters = s[L:]
                leaf.leaf = idx
                mid.children.append(leaf)
                mid.children.sort(key=lambda c: c.letters[0])
                return
        leaf = Node()
        leaf.letters = s
        leaf.leaf = idx
        node.children.append(leaf)
        node.children.sort(key=lambda c: c.letters[0])

    for i in range(len(T)):
        insert(root, T[i:], i)
    return root


def leaves(node):
    if node.leaf is not None:
        return [node.leaf]
    out = []
    for c in node.children:
        out += leaves(c)
    return out


def official_find(root, w):
    node = root
    ptr = 0
    m = len(w)
    while m > 0:
        nxt = None
        for c in node.children:           # bin_search on the first letter
            if c.letters[0] == w[ptr]:
                nxt = c
        if nxt is None:
            return None
        node = nxt
        num = 0
        while num < len(node.letters) and num < m and node.letters[num] == w[ptr + num]:
            num += 1                      # maximum_match
        if num == m:
            return sorted(leaves(node))
        elif num == len(node.letters):
            ptr += num
            m -= num
        else:
            return None
    return None


bad = 0
for _ in range(1500):
    T = "".join(random.choice("abc") for _ in range(random.randint(1, 12)))
    root = build(T)
    w = "".join(random.choice("abc") for _ in range(random.randint(1, 4)))
    got = official_find(root, w) or []
    want = [i for i in range(len(T)) if T.startswith(w, i)]
    if got != want:
        bad += 1
check("Q4b official find_all_occurrences_in_suffix_tree equals naive search (1500 random)", bad == 0, "bad=%d" % bad)
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
