"""SSG1-GAP-1 / Sol 122 B4 sec.4.3 -- U_true literal (brute-force) rail.

Independent literal enumeration cross-check of the symbolic closed forms
J2=p^3(p+1) and J3=1+p^3(p+1) (and the SL(2,Z/p^2) fiber order
p^4(p^2-1)), for a small p == 7 (mod 12), by exhaustively enumerating all
2x2 matrices A over R=Z/p^2 and testing the exact algebraic conditions
directly (no group-theoretic shortcuts, no import of sol/sol_reply_122's
SOL122_SCRIPT or of any producer/checker helper in this repo).

This is a fresh, from-scratch implementation written against the plain
matrix conditions:
  J2  = #{ A in M(2,R) : det(A)=-1 (mod p^2), A^2 = I (mod p^2) }
  J3  = #{ A in M(2,R) : det(A)=+1 (mod p^2), A^3 = I (mod p^2) }
  SLp = #{ A in M(2,R) : det(A)=+1 (mod p^2) }   (== det(A)=-1 count too)

Runs with numpy for speed; the outer loop is over the first matrix entry
so peak memory stays at O(p^6) not O(p^8).

Raw output only -- no verdict language.
"""
import argparse
import json

import numpy as np


def literal_rail(p: int) -> dict:
    if p % 12 != 7:
        raise ValueError(f"p={p} is not congruent to 7 mod 12")
    N = p * p  # modulus = |R| = |Z/p^2|

    idx = np.arange(N, dtype=np.int64)
    Bg = idx.reshape(N, 1, 1)
    Cg = idx.reshape(1, N, 1)
    Dg = idx.reshape(1, 1, N)

    J2_count = 0
    J3_count = 0
    SLp_count = 0       # det == 1
    SLp_minus_count = 0  # det == N-1 (i.e. -1 mod N), independent check
    total_matrices = 0

    for A in range(N):
        det = (A * Dg - Bg * Cg) % N
        total_matrices += det.size

        SLp_count += int(np.count_nonzero(det == 1))
        SLp_minus_count += int(np.count_nonzero(det == N - 1))

        # A^2 entries: [[a^2+bc, b(a+d)], [c(a+d), d^2+bc]]
        e11 = (A * A + Bg * Cg) % N
        e12 = (Bg * (A + Dg)) % N
        e21 = (Cg * (A + Dg)) % N
        e22 = (Dg * Dg + Bg * Cg) % N
        sq_eq_I = (e11 == 1) & (e12 == 0) & (e21 == 0) & (e22 == 1)
        J2_count += int(np.count_nonzero(sq_eq_I & (det == N - 1)))

        # A^3 = (A^2) . A entries
        m3_11 = (e11 * A + e12 * Cg) % N
        m3_12 = (e11 * Bg + e12 * Dg) % N
        m3_21 = (e21 * A + e22 * Cg) % N
        m3_22 = (e21 * Bg + e22 * Dg) % N
        cube_eq_I = (m3_11 == 1) & (m3_12 == 0) & (m3_21 == 0) & (m3_22 == 1)
        J3_count += int(np.count_nonzero(cube_eq_I & (det == 1)))

    J2_formula = p**3 * (p + 1)
    J3_formula = 1 + p**3 * (p + 1)
    SLp_formula = p**4 * (p**2 - 1)

    return {
        "p_prime": p,
        "R_cardinality": N,
        "total_matrices_enumerated": total_matrices,
        "expected_total_matrices": N**4,
        "J2_literal": J2_count,
        "J2_formula_value": J2_formula,
        "J2_match": J2_count == J2_formula,
        "J3_literal": J3_count,
        "J3_formula_value": J3_formula,
        "J3_match": J3_count == J3_formula,
        "SLp_det1_literal": SLp_count,
        "SLp_detminus1_literal": SLp_minus_count,
        "SLp_formula_value": SLp_formula,
        "SLp_det1_match": SLp_count == SLp_formula,
        "SLp_detminus1_match": SLp_minus_count == SLp_formula,
        "SLp_det1_eq_detminus1": SLp_count == SLp_minus_count,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=7)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()
    out = literal_rail(args.p)
    text = json.dumps(out, indent=2, sort_keys=True)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
