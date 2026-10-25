"""Reference KMP pieces for the kmp_prefix course.  Everything 1-indexed in the API (pi[0] unused)."""
import itertools


def borders_brute(s):
    """lengths of all proper borders (0 included) of s, by definition"""
    return sorted((k for k in range(0, len(s)) if s[:k] == s[len(s) - k:]), reverse=True)


def pi_brute(P):
    """pi[q] = longest proper border of P[1..q], straight from the definition; pi[0] unused"""
    return [None] + [borders_brute(P[:q])[0] for q in range(1, len(P) + 1)]


def pi_pseudo(P, count_fallbacks=None):
    """the Compute-Prefix pseudo code of the brief, literally"""
    m = len(P)
    pi = [None, 0]
    k = 0
    fb = [0] * (m + 1)
    for q in range(2, m + 1):
        while k > 0 and P[k] != P[q - 1]:      # P[k+1] in 1-indexing
            k = pi[k]
            fb[q] += 1
        if P[k] == P[q - 1]:
            k += 1
        pi.append(k)
    if count_fallbacks is not None:
        count_fallbacks.extend(fb)
    return pi


def pi_of(P):
    a, b = pi_brute(P), pi_pseudo(P)
    assert a == b, (P, a, b)
    return a


def chain(pi, q):
    """pi[q], pi[pi[q]], ... down to (excluding) 0"""
    out = []
    k = pi[q]
    while k > 0:
        out.append(k)
        k = pi[k]
    return out


def compares_for_char(P, pi, q, c):
    """comparisons made for ONE text char c from state q (CLRS), counted once per (T[i] vs P[j]) pair; returns (comparisons, newq, fallbacks)"""
    cmp_ = 0
    fb = 0
    m = len(P)
    assert q < m
    while True:
        cmp_ += 1
        if P[q] == c:       # P[q+1] 1-indexed
            return cmp_, q + 1, fb
        if q == 0:
            return cmp_, 0, fb
        q = pi[q]
        fb += 1


def run_kmp(T, P, reset=True):
    """instrumented KMP.  returns dict(ends=[1-based end idx], comps=[per text char], states=[q after each char],
    while_iters=int, comps_total=int)"""
    pi = pi_of(P)
    m = len(P)
    q = 0
    ends, comps, states, wi = [], [], [], 0
    for i, c in enumerate(T, 1):
        assert q < m
        cmp_, q, fb = compares_for_char(P, pi, q, c)
        comps.append(cmp_)
        wi += fb
        if q == m:
            ends.append(i)
            q = pi[m]
        states.append(q)
    return dict(ends=ends, comps=comps, states=states, while_iters=wi, total=sum(comps), pi=pi)


def occurrences_naive(T, P):
    """1-based start positions of all (overlapping) occurrences, by brute force"""
    return [i + 1 for i in range(len(T) - len(P) + 1) if T[i:i + len(P)] == P]


def check_run(T, P):
    r = run_kmp(T, P)
    starts = [e - len(P) + 1 for e in r["ends"]]
    assert starts == occurrences_naive(T, P), (T, P, starts)
    return r


def all_strings(n, alpha):
    return ("".join(t) for t in itertools.product(alpha, repeat=n))


def rgs(n):
    """restricted-growth strings (canonical letter order) of length n"""
    def rec(pre, mx):
        if len(pre) == n:
            yield pre
            return
        for c in range(mx + 2):
            yield from rec(pre + [c], max(mx, c))
    for s in rec([], -1):
        yield "".join(chr(97 + c) for c in s)


_FEAS = {}


def feasible_pis(n):
    """set of all pi arrays (tuples, 1..n) realised by SOME string over an unbounded alphabet"""
    if n not in _FEAS:
        _FEAS[n] = {tuple(pi_brute(s)[1:]) for s in rgs(n)}
    return _FEAS[n]


def min_period(A):
    n = len(A)
    return min(p for p in range(1, n + 1) if all(A[i] == A[i + p] for i in range(n - p)))


def is_power(A):
    n = len(A)
    return any(n % d == 0 and A == A[:d] * (n // d) for d in range(1, n))
