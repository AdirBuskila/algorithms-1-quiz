# -*- coding: utf-8 -*-
"""Solver checks for 22A-A Q5 (which sets can the 2-approximation for vertex cover return).
Run: PYTHONUTF8=1 py tools/verify/22A-A/solve_22A-A.py. ASCII output.
The algorithm returns the endpoints of a maximal matching, so a set is a possible output iff it is the vertex set of
some maximal matching. Each option is tested that way and by running the algorithm over all edge orders."""
import itertools, json, pathlib
import networkx as nx

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


g = json.load(open(pathlib.Path(__file__).with_name("graphs.json"), encoding="utf-8"))["22A-A-Q5"]
edges = [(e["u"], e["v"]) for e in g["edges"]]
G = nx.Graph(edges)
opts = {
    "a": {"X5", "X3", "X2", "X7", "X1", "X9"},
    "b": {"X3", "X4", "X1", "X9", "X0", "X6"},
    "c": {"X1", "X8", "X3", "X4", "X9", "X6"},
    "e": {"X1", "X9", "X6", "X3", "X5", "X8"},
    "f": {"X6", "X3", "X1", "X8", "X0", "X4"},
}


def perfect_maximal_matchings(S):
    """All perfect matchings of G[S] that are maximal matchings of G."""
    out = []
    H = G.subgraph(S)
    for M in itertools.combinations(H.edges(), len(S) // 2):
        if len({x for e in M for x in e}) == len(S) and all(u in S or v in S for u, v in G.edges()):
            out.append(sorted(tuple(sorted(e)) for e in M))
    return out


def outputs():
    res = set()

    def rec(rem, C):
        if not rem:
            res.add(frozenset(C))
            return
        for (u, v) in rem:
            rec([e for e in rem if u not in e and v not in e], C | {u, v})
    rec(edges, frozenset())
    return res


outs = outputs()
for k in sorted(opts):
    mm = perfect_maximal_matchings(opts[k])
    print("INFO option %s: cover=%s, maximal matchings on it=%s" %
          (k, all(u in opts[k] or v in opts[k] for u, v in edges), mm))
reach = sorted(k for k in opts if frozenset(opts[k]) in outs)
check("Q5 reachable options == ['c','e'] (all edge orders)", reach == ["c", "e"], str(reach))
check("Q5 reachable == has a perfect matching that is maximal in G",
      reach == sorted(k for k in opts if perfect_maximal_matchings(opts[k])))
check("Q5 b is not a vertex cover (X5-X8 uncovered); a holds X2 and X7 whose only neighbour X6 is outside a; "
      "f holds X0 and X4, unmatched leaves of X9 / X1 inside f",
      not all(u in opts["b"] or v in opts["b"] for u, v in edges) and "X6" not in opts["a"]
      and set(G["X0"]) == {"X9"} and "X9" not in opts["f"])
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
