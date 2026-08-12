"""
[S0-RECHECK] [R-3] python-side independent implementation (different language
from search/ss_gap1_recheck_r3_v1.g, same algorithm: primitive-first-column
generation of SL(2,Z/p^2), NO trace shortcut, literal A^2/A^3 matrix
multiplication classification).
"""
import json

p = 13
n = p * p

total_elts = 0
count_A2_I = 0
count_A2_negI = 0
count_A3_I = 0
count_A3_negI = 0

inv = [0] * n
for a in range(1, n):
    # extended gcd to find inverse mod n if gcd(a,n)==1
    import math
    if math.gcd(a, n) == 1:
        inv[a] = pow(a, -1, n)


def is_unit(x):
    import math
    return math.gcd(x, n) == 1


for a in range(n):
    for c in range(n):
        if a % p == 0 and c % p == 0:
            continue
        if is_unit(a):
            ai = inv[a]
            for b in range(n):
                d = (ai * (1 + b * c)) % n
                total_elts += 1
                e = (a * a + b * c) % n
                f = (a * b + b * d) % n
                g = (c * a + d * c) % n
                h = (c * b + d * d) % n
                if e == 1 and f == 0 and g == 0 and h == 1:
                    count_A2_I += 1
                elif e == n - 1 and f == 0 and g == 0 and h == n - 1:
                    count_A2_negI += 1
                p1 = (e * a + f * c) % n
                q1 = (e * b + f * d) % n
                r1 = (g * a + h * c) % n
                s1 = (g * b + h * d) % n
                if p1 == 1 and q1 == 0 and r1 == 0 and s1 == 1:
                    count_A3_I += 1
                elif p1 == n - 1 and q1 == 0 and r1 == 0 and s1 == n - 1:
                    count_A3_negI += 1
        else:
            ci = inv[c]
            for d in range(n):
                b = (ci * (a * d - 1)) % n
                total_elts += 1
                e = (a * a + b * c) % n
                f = (a * b + b * d) % n
                g = (c * a + d * c) % n
                h = (c * b + d * d) % n
                if e == 1 and f == 0 and g == 0 and h == 1:
                    count_A2_I += 1
                elif e == n - 1 and f == 0 and g == 0 and h == n - 1:
                    count_A2_negI += 1
                p1 = (e * a + f * c) % n
                q1 = (e * b + f * d) % n
                r1 = (g * a + h * c) % n
                s1 = (g * b + h * d) % n
                if p1 == 1 and q1 == 0 and r1 == 0 and s1 == 1:
                    count_A3_I += 1
                elif p1 == n - 1 and q1 == 0 and r1 == 0 and s1 == n - 1:
                    count_A3_negI += 1

SL_order_formula = p**4 * (p**2 - 1)
i2_full = (count_A2_I + count_A2_negI) // 2
i3_full = (count_A3_I + count_A3_negI) // 2

result = {
    "p": p, "n": n,
    "total_elts_generated": total_elts,
    "SL_order_formula": SL_order_formula,
    "total_elts_match_formula": total_elts == SL_order_formula,
    "count_A2_eq_I": count_A2_I,
    "count_A2_eq_negI": count_A2_negI,
    "count_A3_eq_I": count_A3_I,
    "count_A3_eq_negI": count_A3_negI,
    "i2_Qp_full_enum": i2_full,
    "i3_Qp_full_enum": i3_full,
}
print(json.dumps(result, indent=2))
with open(r"C:\Users\81905\Desktop\shadow-atelier\scratchpad\recheck_r3_python_out.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
