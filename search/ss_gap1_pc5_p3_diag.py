#!/usr/bin/env python3
"""
search/ss_gap1_pc5_p3_diag.py
SS-GAP-1 Stage 0 / PC-5 diagnostic: 3rd independent implementation
(direct matrix multiplication in python, NO GAP import, NO import of
search/ss_gap1_pc5_crosscheck.py's closed-form code either -- written
from scratch) used solely to pin down the root cause of the p=3
mismatch found between the raw Cayley-Hamilton closed form
(search/ss_gap1_pc5_crosscheck.py) and GAP's brute-force full
enumeration (search/ss_gap1_pc5_v1.g -> search/certs/ss_gap1_pc5_gap_v1_20260813.json).

Brute-forces SL(2,Z/9) fully by actual 2x2 matrix multiplication (B*B*B)
and classifies every B with B^3=I into: scalar / (tr=-1,det=1) nonscalar /
"other". Confirms "other" == elements congruent to I mod 3 (the
3-congruence kernel), beyond the identity itself.
"""
n = 9
cnt = 0
scalar = 0
tr_neg1_det1_nonscalar = 0
other = 0
detail = []
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                if (a * d - b * c) % n == 1:
                    e = (a * a + b * c) % n
                    f = (a * b + b * d) % n
                    g = (c * a + d * c) % n
                    h = (c * b + d * d) % n
                    p_ = (e * a + f * c) % n
                    q_ = (e * b + f * d) % n
                    r_ = (g * a + h * c) % n
                    s_ = (g * b + h * d) % n
                    if p_ == 1 and q_ == 0 and r_ == 0 and s_ == 1:
                        cnt += 1
                        isscalar = (b == 0 and c == 0 and a == d)
                        trace = (a + d) % n
                        det = (a * d - b * c) % n
                        is_kernel3 = (a % 3 == 1 and d % 3 == 1 and b % 3 == 0 and c % 3 == 0)
                        if isscalar:
                            scalar += 1
                        elif trace == 8 and det == 1:
                            tr_neg1_det1_nonscalar += 1
                        else:
                            other += 1
                            detail.append((a, b, c, d, trace, det, is_kernel3))

print("total i3:", cnt, "scalar:", scalar, "tr=-1 nonscalar:", tr_neg1_det1_nonscalar, "other:", other)
print("other all kernel-mod-3 (cong I mod 3)?", all(x[6] for x in detail))
print("other count:", len(detail))
print("sample other:", detail[:8])
