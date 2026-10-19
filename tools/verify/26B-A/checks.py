# -*- coding: utf-8 -*-
"""Transcription checks for 26B-A (algorithms-1, NO KEY: every item is held as no-key).
Run: PYTHONUTF8=1 py tools/verify/26B-A/checks.py
These checks only confirm that the examples printed in the exam are self-consistent with the transcribed text, and
print reference facts for the solver (not an official answer). ASCII output."""
import itertools, json, pathlib
import networkx as nx

HERE = pathlib.Path(__file__).resolve().parent
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


def knap(tasks, T):  # tasks = (time, profit)
    best = [0] * (T + 1)
    for t, v in tasks:
        for c in range(T, t - 1, -1):
            best[c] = max(best[c], best[c - t] + v)
    return best[T]


ex = [(2, 4), (3, 5), (4, 10)]
check("Q1 example T=5 -> 10 (task 3 only), T=6 -> 14", knap(ex, 5) == 10 and knap(ex, 6) == 14)
sub = [s for r in range(4) for s in itertools.combinations(range(3), r) if sum(ex[i][0] for i in s) == 6 and sum(ex[i][1] for i in s) == 14]
check("Q1 example T=6 optimum is tasks 1 and 3", sub == [(0, 2)])
print("FACT  Q1c table data (1,1),(2,3),(4,7),(5,10), T=6 -> max profit", knap([(1, 1), (2, 3), (4, 7), (5, 10)], 6))

# Q2a reference: ratio-greedy fails (instance for the solver to cross-check any counterexample)
def ratio_greedy(tasks, T):
    tot = 0
    for t, v in sorted(tasks, key=lambda x: -x[1] / x[0]):
        if t <= T:
            T -= t
            tot += v
    return tot


ce = [(1, 2), (5, 9)]  # reference only: ratio 2 vs 1.8, T=5
print("FACT  tasks (t,v)=(1,2),(5,9), T=5: ratio-greedy", ratio_greedy(ce, 5), "optimum", knap(ce, 5))

# Q3a example graph: BFS order s,u,w,v
g = json.load(open(HERE / "graphs.json"))
G3 = nx.Graph([(e["u"], e["v"]) for e in g["26B-A-Q3a"]["edges"]])
check("Q3a example: BFS discovery order s,u,w,v (neighbours in the order u before w)",
      list(nx.bfs_tree(G3, "s", sort_neighbors=lambda n: sorted(n, key=lambda x: {"u": 0, "w": 1, "v": 2}[x] if x in "uwv" else 9)).nodes()) == ["s", "u", "w", "v"])

# Q4b graph facts (reference for the solver)
G4 = nx.Graph()
for e in g["26B-A-Q4b"]["edges"]:
    if e["w"] is not None:
        G4.add_edge(e["u"], e["v"], weight=e["w"])
check("Q4b graph transcribed: 8 vertices, 13 fixed edges + the unknown D-F", G4.number_of_nodes() == 8 and G4.number_of_edges() == 13)


# direct: D-F is in every MST iff w(D-F) < the bottleneck of the best D..F path in G minus D-F
def bottleneck(u, v):
    T = nx.minimum_spanning_tree(G4)
    p = nx.shortest_path(T, u, v)
    return max(G4[a][b]["weight"] for a, b in zip(p, p[1:]))


bn = bottleneck("D", "F")
print("FACT  minimax path weight D..F without edge D-F =", bn, "-> D-F is in every MST exactly when X <", bn)

# Q4c(i) prefix function
def pi_fn(P):
    pi = [0] * len(P)
    k = 0
    for i in range(1, len(P)):
        while k and P[i] != P[k]:
            k = pi[k - 1]
        if P[i] == P[k]:
            k += 1
        pi[i] = k
    return pi


P = "AABAABAABAAA"
check("Q4c(i) pattern has 12 characters", len(P) == 12)
print("FACT  pi(AABAABAABAAA) =", pi_fn(P))

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
