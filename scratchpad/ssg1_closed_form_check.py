"""
[SS-GAP-1 / PRED-S0-4] closed-form integer generator (exact rational arithmetic).

    i_2(PSL(2,Z/p^2)) = 1 + p^3 (p + eps2) / 2 ,  eps2 = (-1|p)
    i_3(PSL(2,Z/p^2)) = 1 + p^3 (p + eps3)     ,  eps3 = (-3|p)
    |Q_p|             = p^4 (p^2 - 1) / 2
    U(p)              = 2 i_2 i_3 / |Q_p|        (exact Fraction)

Every value quoted in docs/notes/ssg1_stage0_pred_repair_v1.md is produced here.
No hand arithmetic (m1102-1 / m1102-2 discipline).
"""
from fractions import Fraction


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def closed_form(p):
    e2 = legendre(-1, p)
    e3 = legendre(-3, p)
    i2 = 1 + p**3 * (p + e2) // 2
    i3 = 1 + p**3 * (p + e3)
    Q = p**4 * (p * p - 1) // 2
    U = Fraction(2 * i2 * i3, Q)
    kappa = Fraction((p + e2) * (p + e3), p * p - 1)
    return dict(p=p, cls=p % 12, e2=e2, e3=e3, i2=i2, i3=i3, Q=Q, U=U,
                kappa=kappa, lead=2 * p * p * kappa)


if __name__ == "__main__":
    print("=== already measured (cert ss_gap1_s0_predcheck_v1) ===")
    for p in (19, 23, 29, 31):
        r = closed_form(p)
        print(f"p={r['p']:4d} mod12={r['cls']:2d}  i2={r['i2']}  i3={r['i3']}  |Q|={r['Q']}")
        print(f"      U = {r['U']} = {float(r['U']):.9f}")

    print()
    print("=== PRED-S0-4 : re-freeze on fresh primes, all four classes mod 12 ===")
    for p in (37, 41, 43, 47):
        r = closed_form(p)
        print(f"p={r['p']:4d} mod12={r['cls']:2d} eps=({r['e2']:+d},{r['e3']:+d}) kappa={r['kappa']}")
        print(f"      i2={r['i2']}  i3={r['i3']}  |Q|={r['Q']}")
        print(f"      U = {r['U']} = {float(r['U']):.9f}   (leading 2p^2*kappa = {float(r['lead']):.6f})")

    print()
    print("=== p = 691 (restored only after PRED-S0-4 passes) ===")
    r = closed_form(691)
    print(f"      i2={r['i2']}")
    print(f"      i3={r['i3']}")
    print(f"      |Q|={r['Q']}")
    print(f"      U = {float(r['U']):.9f}   kappa={r['kappa']}   2p^2={2*691*691}")
