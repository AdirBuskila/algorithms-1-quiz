# Q4b step 3: removing circles whose left end is "<" (instead of "<=") the chosen right end gives the same answer on the
# printed example, so the step must not claim otherwise; it differs on a tangent input.
def greedy(circles, weak=True):
    iv = sorted(((c - r, c + r, i + 1) for i, (c, r) in enumerate(circles)), key=lambda t: t[1])
    out = []
    while iv:
        l, rgt, i = iv[0]
        out.append(i)
        iv = [t for t in iv[1:] if not ((t[0] <= rgt) if weak else (t[0] < rgt))]
    return out


printed = [(-4.5, 2), (0, 2), (0, 3), (5, 4), (6, 2), (7, 5), (8, 3)]
assert greedy(printed, True) == [1, 2, 5]
assert greedy(printed, False) == [1, 2, 5]
tangent = [(0, 1), (2, 1)]                           # [-1,1] and [1,3] touch at x=1 -> not disjoint
assert greedy(tangent, True) == [1]
assert len(greedy(tangent, False)) == 2              # the strict version keeps a tangent circle: 2 > optimum 1
print("printed example: same answer with < and <=; tangent input: <= gives 1 (correct), < gives 2 (too many)")
