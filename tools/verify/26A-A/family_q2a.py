# Q2a: the counterexample family for every n >= 4 (even n directly, odd n with one extra vertex whose edges are the
# heaviest): matching edges {v(2i-1), v(2i)} get weight i (the lightest), {v2, v3} gets weight n/2+1, every other edge a
# larger distinct weight.  The edge {v2, v3} is in the MST but is the lightest edge at neither endpoint.
import itertools
import random

random.seed(2)


def family(n):
    pairs = n // 2
    w = {}
    for i in range(1, pairs + 1):
        w[(2 * i - 1, 2 * i)] = i
    w[(2, 3)] = pairs + 1
    rest = [e for e in itertools.combinations(range(1, n + 1), 2) if e not in w]
    heavy = list(range(pairs + 2, pairs + 2 + len(rest)))
    random.shuffle(heavy)
    for e, x in zip(rest, heavy):
        w[e] = x
    return w


def mst(n, w):
    par = list(range(n + 1))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    T = set()
    for e, _ in sorted(w.items(), key=lambda kv: kv[1]):
        a, b = f(e[0]), f(e[1])
        if a != b:
            par[a] = b
            T.add(e)
    return T


for n in range(4, 23):
    w = family(n)
    assert len(set(w.values())) == len(w)
    T = mst(n, w)
    e = (2, 3)
    assert e in T, n
    for v in e:
        lightest = min((x for x in w if v in x), key=lambda x: w[x])
        assert lightest != e, (n, v)
print("family verified for n = 4..22: the edge {v2,v3} is in the MST and special for neither endpoint")
