# Q4 alternative: pre/suf from the KMP prefix function (pi of P#T and of reverse(P)#reverse(T)) via a linear
# pi -> Z conversion; compared with the naive "almost match" check on random strings.
import random


def prefix_function(s):
    pi = [0] * len(s)
    q = 0
    for k in range(1, len(s)):
        while q > 0 and s[k] != s[q]:
            q = pi[q - 1]
        if s[k] == s[q]:
            q += 1
        pi[k] = q
    return pi


def z_from_pi(pi):
    L = len(pi)
    z = [0] * L
    for k in range(1, L):
        if pi[k] > 0:
            z[k - pi[k] + 1] = pi[k]
    z[0] = L
    i = 1
    while i < L:
        t = i
        if z[i] > 0:
            for j in range(1, z[i]):
                if z[i + j] > z[j]:
                    break
                z[i + j] = min(z[j], z[i] - j)
                t = i + j
        i = t + 1
    return z


def z_naive(s):
    L = len(s)
    z = [0] * L
    z[0] = L
    for k in range(1, L):
        while k + z[k] < L and s[z[k]] == s[k + z[k]]:
            z[k] += 1
    return z


def almost(T, P):
    n, m = len(T), len(P)
    out = []
    for i in range(n - m + 1):
        if sum(1 for a, b in zip(P, T[i:i + m]) if a != b) <= 1:
            out.append(i + 1)
    return out


def almost_pi(T, P):
    n, m = len(T), len(P)
    Z1 = z_from_pi(prefix_function(P + "#" + T))
    Z2 = z_from_pi(prefix_function(P[::-1] + "#" + T[::-1]))
    pre = [Z1[m + 1 + i] for i in range(n)]
    suf = [Z2[m + 1 + (n - 1 - i)] for i in range(n)]
    return [i + 1 for i in range(n - m + 1) if pre[i] >= m or pre[i] + suf[i + m - 1] >= m - 1]


random.seed(3)
for _ in range(20000):
    L = random.randint(1, 14)
    s = "".join(random.choice("ab#") for _ in range(L))
    assert z_from_pi(prefix_function(s)) == z_naive(s), s
cnt = 0
for _ in range(6000):
    m = random.randint(1, 6)
    n = random.randint(m + 1, 14)
    sig = random.choice(["ab", "abc"])
    P = "".join(random.choice(sig) for _ in range(m))
    T = "".join(random.choice(sig) for _ in range(n))
    assert almost_pi(T, P) == almost(T, P), (T, P)
    cnt += 1
print("pi->Z conversion and the pi-based almost-match agree with brute force on", cnt, "cases")
print(almost_pi("aaaaba", "aababa"), almost("aaaaba", "aababa"))
