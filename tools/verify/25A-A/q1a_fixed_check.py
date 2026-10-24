# Q1a: the official Mid pseudocode after the silent transcription fixes (average /2 in rows 2-3, the second half of B
# starts at (k+l+1)/2 in rows 7-8, the base case i=j first). Compared with the true median of the merged arrays.
import random


def mid(A, i, j, B, k, l):
    if i == j:
        return (A[i] + B[k]) / 2
    a1, a2 = A[(i + j - 1) // 2], A[(i + j + 1) // 2]
    b1, b2 = B[(k + l - 1) // 2], B[(k + l + 1) // 2]
    if a1 < b1 < b2 < a2:
        return (b1 + b2) / 2
    if b1 < a1 < a2 < b2:
        return (a1 + a2) / 2
    if a1 < a2 < b1 < b2 or a1 < b1 < a2 < b2:
        return mid(A, (i + j + 1) // 2, j, B, k, (k + l - 1) // 2)
    if b1 < b2 < a1 < a2 or b1 < a1 < b2 < a2:
        return mid(B, (k + l + 1) // 2, l, A, i, (i + j - 1) // 2)
    raise AssertionError("no row applies")


random.seed(11)
bad = 0
total = 0
for h in (1, 2, 4, 8, 16):                        # |A| = |B| = n/2 = h, n a power of 2
    for _ in range(3000):
        vals = random.sample(range(1, 400), 2 * h)
        A = sorted(vals[:h])
        B = sorted(vals[h:])
        merged = sorted(vals)
        want = (merged[h - 1] + merged[h]) / 2
        got = mid([None] + A, 1, h, [None] + B, 1, h) if h > 1 else (A[0] + B[0]) / 2
        total += 1
        if got != want:
            bad += 1
print("cases:", total, "mismatches:", bad)
assert bad == 0
