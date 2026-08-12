"""SSG1-GAP-1 / Sol 122 B4 sec.4.3 -- U_true symbolic (closed-form) rail.

Independent re-derivation of the exact fiber-product upper bound for
H_tilde = {(A,s) in SL^pm(2,Z/p^2) x S3 : det(A) = sgn(s)}, following the
closed forms stated in sol/sol_reply_122_r1_line3.md sec 4.2 (SOL122_SCRIPT
is READ but this module is a fresh independent implementation, not a copy --
per task instruction).

Standard facts used (cited, not re-derived here):
  |SL(2, Z/p^2)| = p^4 (p^2-1)      (Lang-Weil / p-adic Sylow order for
                                      the reduction-mod-p kernel of
                                      SL(2,Z/p) times the group itself)
  Fiber of det: GL(2,Z/p^2) -> (Z/p^2)^x over any single unit value u has
  the same size p^4(p^2-1) as the det=1 fiber (translation by any matrix
  of that determinant is a bijection between fibers).

Raw output only -- no verdict language.
"""
import argparse
import json
from fractions import Fraction


def symbolic_rail(p: int) -> dict:
    if p % 12 != 7:
        raise ValueError(f"p={p} is not congruent to 7 mod 12 (required by the "
                          f"p^3(p+1) closed forms below)")
    R_card = p * p  # |Z/p^2|
    unit_group_order = p * (p - 1)  # |(Z/p^2)^x|, p odd
    SL_fiber_order = p**4 * (p**2 - 1)  # size of one det=const fiber in GL(2,Z/p^2)
    H_order = 6 * SL_fiber_order        # 6 = |S3|, each s contributes one fiber
    Z_order = 2                          # {I,-I}, see center_argument below

    # J2: matrices A with A^2=I, det A=-1.  Over R=Z/p^2 (2,3 invertible,
    # -1 not a square-of-unity collision issue here), A^2=I with det=-1
    # forces A to be conjugate (over R, ordered) to diag(1,-1); the count
    # of ordered direct-sum decompositions R^2 = L_+ (+) L_- into rank-1
    # free direct summands is |GL2(R)| / |R^x|^2 = p^3(p+1).
    J2 = p**3 * (p + 1)

    # J3: matrices A with A^3=I, det A=1.  p == 1 mod 3 (implied by p==7
    # mod 12 => p==1 mod 3), so R contains a primitive cube root of unity
    # omega, and R^2 splits as an ordered sum of omega/omega^2 eigenlines
    # for every non-identity such A; +1 for A=I itself.
    J3 = 1 + p**3 * (p + 1)

    i2T = 3 * J2   # 3 transpositions in S3, each pairs with the det=-1 fiber
    i3R = 2 * J3   # 2 three-cycles in S3, each pairs with the det=1 fiber

    U_true = Fraction(2 * i2T * i3R * Z_order, H_order)

    return {
        "p": p,
        "p_mod_12": p % 12,
        "p_mod_3": p % 3,
        "R_cardinality": R_card,
        "unit_group_order": unit_group_order,
        "SL_fiber_order": SL_fiber_order,
        "H_order": H_order,
        "H_order_formula": "6*p^4*(p^2-1)",
        "Z_order": Z_order,
        "center_argument": (
            "central elements must have identity S3-component (S3 has "
            "trivial center) hence det A=1 and A central in GL(2,R), i.e. "
            "A=lambda*I with lambda^2=1 in R=Z/p^2; since p is odd, "
            "x^2-1=(x-1)(x+1) with gcd(x-1,x+1) a unit in the local ring "
            "R, so exactly two roots lambda=+-1, giving Z(H_tilde)={I,-I}"
        ),
        "J2": J2,
        "J2_formula": "p^3*(p+1)",
        "J3": J3,
        "J3_formula": "1+p^3*(p+1)",
        "i2T": i2T,
        "i3R": i3R,
        "U_true": {
            "num": U_true.numerator,
            "den": U_true.denominator,
            "decimal_15dp": f"{float(U_true):.15f}",
            "floor": U_true.numerator // U_true.denominator,
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=691)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()
    out = symbolic_rail(args.p)
    text = json.dumps(out, indent=2, sort_keys=True)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
