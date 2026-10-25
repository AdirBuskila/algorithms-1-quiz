# -*- coding: utf-8 -*-
"""Learn-brief checks: randomized (brief 10). Exact probabilities by full enumeration, no sampling.
Run: PYTHONUTF8=1 py tools/verify/learn/v08_randomized.py     (ASCII output, exits 1 on a failure)"""
import itertools, math, random, sys
from fractions import Fraction

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


random.seed(31337)


def matvec(M, y):
    return [sum(M[i][j] * y[j] for j in range(len(y))) for i in range(len(M))]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


# ---------------------------------------------------------------- matrix product check (SAMP-1 Q3)
worst = Fraction(0)
exact_half = False
bad = 0
for _ in range(300):
    k = random.randint(2, 6)
    A = [[random.randint(-3, 3) for _ in range(k)] for _ in range(k)]
    B = [[random.randint(-3, 3) for _ in range(k)] for _ in range(k)]
    C = [row[:] for row in matmul(A, B)]
    if random.random() < 0.2:
        pass  # C = AB exactly
    else:
        for _ in range(random.randint(1, 3)):
            C[random.randrange(k)][random.randrange(k)] += random.choice([-2, -1, 1, 3])
    wrong = 0
    ys = list(itertools.product((0, 1), repeat=k))
    for y in ys:
        lhs = matvec(A, matvec(B, list(y)))
        rhs = matvec(C, list(y))
        same = lhs == rhs
        wrong += same
    equal = C == matmul(A, B)
    if equal:
        bad += wrong != len(ys)  # always answers "equal"
    else:
        frac = Fraction(wrong, len(ys))
        worst = max(worst, frac)
        bad += frac > Fraction(1, 2)
check("Freivalds: if C = AB the test always says equal; otherwise it wrongly says equal on at most half of all 0/1 vectors y (300 random, exhaustive in y)", bad == 0, "worst error fraction %s" % worst)
# a single wrong entry gives exactly 1/2
k = 4
A = [[1 if i == j else 0 for j in range(k)] for i in range(k)]
B = [[2 if i == j else 0 for j in range(k)] for i in range(k)]
C = matmul(A, B)
C[1][2] += 5
ys = list(itertools.product((0, 1), repeat=k))
w = sum(matvec(A, matvec(B, list(y))) == matvec(C, list(y)) for y in ys)
check("one wrong entry: the test is fooled by exactly half of the vectors (those with y_j = 0)", Fraction(w, len(ys)) == Fraction(1, 2), "%d of %d" % (w, len(ys)))
check("error after t independent runs: (1/2)^t : t=10 -> 1/1024; t=2 -> 1/4", Fraction(1, 2) ** 10 == Fraction(1, 1024) and Fraction(1, 2) ** 2 == Fraction(1, 4))
# cost shape: naive k^3 multiplications vs two matrix-vector products 2*k^2 ; input size n = k^2
kk = 100
check("n = k^2 entries: naive product k^3 = n^1.5 operations, the randomised test 2 k^2 = 2n", kk ** 3 == (kk * kk) ** 1.5 and 2 * kk ** 2 == 2 * (kk * kk))

# ---------------------------------------------------------------- polynomial identity (22A-A Q3)
bad = 0
for _ in range(200):
    n = random.randint(1, 6)
    P = [random.randint(-4, 4) for _ in range(n + 1)]
    G = P[:]
    G[random.randrange(n + 1)] += random.choice([-2, -1, 1, 2])
    ev = lambda c, t: sum(c[i] * t ** i for i in range(len(c)))
    agree = sum(ev(P, t) == ev(G, t) for t in range(0, n + 1))
    bad += agree > n  # P - G is a nonzero polynomial of degree <= n: at most n roots
check("two different polynomials of degree <= n agree on at most n of the n+1 points 0..n (200 random)", bad == 0)
bad = 0
for _ in range(200):
    n = random.randint(1, 6)
    P = [random.randint(-4, 4) for _ in range(n + 1)]
    G = P[:]
    G[random.randrange(n + 1)] += random.choice([-2, -1, 1, 2])
    ev = lambda c, t: sum(c[i] * t ** i for i in range(len(c)))
    R = 2 * n
    agree = sum(ev(P, t) == ev(G, t) for t in range(1, R + 1))
    bad += Fraction(agree, R) > Fraction(1, 2)
check("choosing the point from a set of size 2n makes the one-run error at most 1/2 (200 random)", bad == 0)

# ---------------------------------------------------------------- fair coin from a biased one (23A-A Q3)
for p in (Fraction(1, 3), Fraction(1, 10), Fraction(3, 4)):
    pq = p * (1 - p)          # probability of "heads then tails" (= "tails then heads")
    q = 2 * pq                # a round ends
    p0 = pq / q               # P(output 0 | round ends)
    exp_rounds = 1 / q
    # numeric series for the expectation
    s = sum(Fraction(t) * (1 - q) ** (t - 1) * q for t in range(1, 400))
    check("fair coin from p=%s: a round ends with prob %s, then each output has prob 1/2, expected rounds %s" % (p, q, exp_rounds),
          p0 == Fraction(1, 2) and abs(float(s) - float(exp_rounds)) < 1e-6)
tbl = {"TH": (1 - Fraction(1, 3)) * Fraction(1, 3), "HT": Fraction(1, 3) * (1 - Fraction(1, 3)), "HH": Fraction(1, 9), "TT": Fraction(4, 9)}
check("23A-A Q3b table with p = 1/3 : (1-p)p, p(1-p), p^2, (1-p)^2 sum to 1 and the first two are equal", sum(tbl.values()) == 1 and tbl["TH"] == tbl["HT"])

# ---------------------------------------------------------------- Alice / Bob equality (24A-A Q3)
n = 8
bad = 0
for _ in range(200):
    x = [random.randint(0, 1) for _ in range(n)]
    y = x[:]
    d = random.randint(0, n)
    for i in random.sample(range(n), d):
        y[i] ^= 1
    wrong = sum(1 for i in range(n) if x[i] == y[i])  # Bob says "equal" although x != y when the sampled bit agrees
    if d == 0:
        continue
    bad += Fraction(wrong, n) != Fraction(n - d, n) or Fraction(wrong, n) > Fraction(n - 1, n)
check("random index: for x != y the error probability is (n-d)/n <= (n-1)/n, worst case when one bit differs", bad == 0)
check("bits Alice sends: ceil(log2 n) + 1 : n=8 -> 4, n=1000 -> 11", math.ceil(math.log2(8)) + 1 == 4 and math.ceil(math.log2(1000)) + 1 == 11)
# half of the positions (24A-A Q3c): x and y differ in exactly one bit, Alice sends n/2 random distinct bits
n = 8
pos = 3
hits = sum(1 for S in itertools.combinations(range(n), n // 2) if pos in S)
total = math.comb(n, n // 2)
check("Alice sends n/2 random positions; one differing bit is among them with probability 1/2", Fraction(hits, total) == Fraction(1, 2))


# ---------------------------------------------------------------- fingerprint with a random prime (24A-B Q3)
def primes_upto(m):
    return [p for p in range(2, m + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]

bad = 0
for n in range(2, 40):
    P = primes_upto(n * n)
    for i in range(n):
        diff = 2 ** i
        errors = [q for q in P if diff % q == 0]
        bad += errors not in ([], [2]) or (i >= 1 and errors != [2])
    bad += 1 / len(P) > 0.5
check("x and y differ in a single bit: x - y = +-2^i, for i>=1 only the prime 2 divides it (for i=0 none does), so the error probability is at most 1/pi(n^2) <= 1/2 for n>=2 (n<40)", bad == 0)
check("two independent runs: (1/2)^2 = 1/4 <= 1/4", Fraction(1, 2) ** 2 == Fraction(1, 4))
check("bits for q and z: 2*ceil(log2 n^2) , n = 100 -> 28", 2 * math.ceil(math.log2(100 ** 2)) == 28)
# general: the number of distinct primes dividing a number below 2^n is at most n
def omega(m):
    c, d = 0, 2
    while d * d <= m:
        if m % d == 0:
            c += 1
            while m % d == 0:
                m //= d
        d += 1
    return c + (1 if m > 1 else 0)

check("a number m has at most log2(m) distinct prime factors (m <= 20000)", all(omega(m) <= math.log2(m) for m in range(2, 20001)))

# ---------------------------------------------------------------- the worked example of brief 10
A = [[1, 2], [3, 4]]
B = [[0, 1], [1, 0]]
AB = matmul(A, B)
C = [[2, 1], [4, 4]]
D = [[C[i][j] - AB[i][j] for j in range(2)] for i in range(2)]
liars = [y for y in itertools.product((0, 1), repeat=2) if matvec(D, list(y)) == [0, 0]]
check("brief 10 example: AB = [[2,1],[4,3]], C differs in one entry (+1), D = [[0,0],[0,1]]; liars are y=(0,0),(1,0): 2 of 4",
      AB == [[2, 1], [4, 3]] and D == [[0, 0], [0, 1]] and liars == [(0, 0), (1, 0)])
By = matvec(B, [1, 1])
check("for y=(1,1): B y = (1,1), A(By) = (3,7), C y = (3,8): different, so the test answers 'not equal' (certain)", By == [1, 1] and matvec(A, By) == [3, 7] and matvec(C, [1, 1]) == [3, 8])

sys.exit(0 if ok else 1)
