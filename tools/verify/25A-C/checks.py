# -*- coding: utf-8 -*-
"""Transcription checks for 25A-C (algorithms-1, NO KEY: every item is held as no-key).
Run: PYTHONUTF8=1 py tools/verify/25A-C/checks.py
Confirms that the examples printed in the exam agree with the transcribed text. ASCII output."""
ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    ok &= bool(cond)


def d(a, b):
    return sum(x != y for x, y in zip(a, b))


S1, S2 = "AGCTTACG", "ACTTAACG"
check("Q1 d(S1,S2)=3 at positions 2,3,5",
      d(S1, S2) == 3 and [i + 1 for i in range(8) if S1[i] != S2[i]] == [2, 3, 5])
T1, T2 = "AGCTT-ACG", "A-CTTAACG"
check("Q1 alignment T1,T2 has length 9 and distance 2 at positions 2,6",
      len(T1) == len(T2) == 9 and d(T1, T2) == 2 and [i + 1 for i in range(9) if T1[i] != T2[i]] == [2, 6])
check("Q1 T1,T2 are S1,S2 with '-' inserted", T1.replace("-", "") == S1 and T2.replace("-", "") == S2)


def frac_knap(val, wt, cap):
    tot = 0.0
    for v, w in sorted(zip(val, wt), key=lambda p: -p[0] / p[1]):
        take = min(w, cap)
        tot += v * take / w
        cap -= take
    return tot


check("Q2 example Val=[60,100,120] Wt=[10,20,30] cap=50 -> 240", abs(frac_knap([60, 100, 120], [10, 20, 30], 50) - 240) < 1e-9)
check("Q3 [4,5,6,7,0,1,2] is a rotation of [0,1,2,4,5,6,7] and t=0 is at index 4",
      [4, 5, 6, 7, 0, 1, 2] == [0, 1, 2, 4, 5, 6, 7][3:] + [0, 1, 2, 4, 5, 6, 7][:3]
      and [4, 5, 6, 7, 0, 1, 2].index(0) == 4)
check("Q4 'abc' hides in 'dfzcbau' (reverse 'cba' is a substring)", "abc"[::-1] in "dfzcbau")
print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
