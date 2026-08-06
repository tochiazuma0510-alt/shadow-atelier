#!/usr/bin/env python3
"""
Independent crosscheck (照合器) for search/certs/rw_gap5_g2_r0_gen_cert_20260806.json.

Reads ONLY the cert JSON (no GAP source, no GAP intermediate state imported --
探索器/照合器分離 per CLAUDE.md). Recomputes, from scratch in pure Python:

  1. det(r), det(s), order(r), order(s) directly from the 2x2 matrices in the cert.
  2. Faithfulness of <r,s> as a subgroup of GL2(F_691) (brute matrix-group closure).
  3. x^2 = I, y^3 = I for the witness 3x3 matrices.
  4. |<x,y>| via brute-force group closure (BFS multiplication by generators over
     3x3 matrices mod 691), compared against the cert's claimed R0(p) order 6*p^2.

This is a cross-check, NOT a "verification" in the Lean sense (per project
vocabulary discipline) -- an independent re-derivation from the cert's raw data
that either agrees or disagrees with the GAP-side numbers.
"""
import json
import sys
from pathlib import Path

P = 691


def matmul(a, b, n, mod=P):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(n)) % mod for j in range(n))
        for i in range(n)
    )


def identity(n):
    return tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))


def mat_pow(a, e, n, mod=P):
    result = identity(n)
    base = a
    while e > 0:
        if e & 1:
            result = matmul(result, base, n, mod)
        base = matmul(base, base, n, mod)
        e >>= 1
    return result


def det2(m):
    return (m[0][0] * m[1][1] - m[0][1] * m[1][0]) % P


def order_of(m, n, max_order=1000):
    cur = m
    e = 1
    ident = identity(n)
    while cur != ident:
        cur = matmul(cur, m, n)
        e += 1
        if e > max_order:
            return None
    return e


def group_closure_size(gens, n, cap=10_000_000):
    """BFS closure of <gens> under right multiplication, starting from identity.
    Valid for finite matrix groups: since gens have finite order, the reachable
    set from the identity under right-multiplication by generators is exactly
    the generated subgroup."""
    ident = identity(n)
    seen = {ident}
    frontier = [ident]
    while frontier:
        new_frontier = []
        for g in frontier:
            for gen in gens:
                h = matmul(g, gen, n)
                if h not in seen:
                    seen.add(h)
                    new_frontier.append(h)
                    if len(seen) > cap:
                        raise RuntimeError(f"group closure exceeded cap {cap}")
        frontier = new_frontier
    return len(seen)


def main():
    cert_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "search/certs/rw_gap5_g2_r0_gen_cert_20260806.json"
    )
    cert = json.loads(cert_path.read_text(encoding="utf-8"))

    results = {}
    ok = True

    ai = cert["action_identification"]
    r_mat = tuple(tuple(row) for row in ai["r"]["matrix_mod_691"])
    s_mat = tuple(tuple(row) for row in ai["s"]["matrix_mod_691"])

    # 1. det / order recompute
    det_r = det2(r_mat)
    det_s = det2(s_mat)
    ord_r = order_of(r_mat, 2)
    ord_s = order_of(s_mat, 2)
    results["det_r_recomputed"] = det_r
    results["det_r_cert"] = ai["r"]["det_mod_691"]
    results["det_r_match"] = det_r == ai["r"]["det_mod_691"]
    results["det_s_recomputed"] = det_s
    results["det_s_cert"] = ai["s"]["det_mod_691"]
    results["det_s_match"] = det_s == ai["s"]["det_mod_691"]
    results["order_r_recomputed"] = ord_r
    results["order_r_cert"] = ai["r"]["order"]
    results["order_r_match"] = ord_r == ai["r"]["order"]
    results["order_s_recomputed"] = ord_s
    results["order_s_cert"] = ai["s"]["order"]
    results["order_s_match"] = ord_s == ai["s"]["order"]
    ok = ok and all(
        results[k] for k in
        ("det_r_match", "det_s_match", "order_r_match", "order_s_match")
    )

    # 2. faithfulness: size of <r,s> in GL2(F_691)
    faith_size = group_closure_size([r_mat, s_mat], 2)
    results["faithfulness_size_recomputed"] = faith_size
    results["faithfulness_size_cert"] = ai["faithfulness_check"]["size_of_matrix_group_generated_by_r_s"]
    results["faithfulness_match"] = faith_size == ai["faithfulness_check"]["size_of_matrix_group_generated_by_r_s"]
    ok = ok and results["faithfulness_match"]

    # 3 & 4. witness order conditions + generation
    gen = cert["checks"]["iii_generation"]
    if gen["status"] == "FOUND":
        wit = gen["witness"]
        x_mat = tuple(tuple(row) for row in wit["x"]["matrix_3x3_mod_691"])
        y_mat = tuple(tuple(row) for row in wit["y"]["matrix_3x3_mod_691"])

        x2 = mat_pow(x_mat, 2, 3)
        y3 = mat_pow(y_mat, 3, 3)
        results["x_squared_is_identity"] = x2 == identity(3)
        results["y_cubed_is_identity"] = y3 == identity(3)
        ok = ok and results["x_squared_is_identity"] and results["y_cubed_is_identity"]

        gen_size = group_closure_size([x_mat, y_mat], 3, cap=3_500_000)
        results["generated_subgroup_size_recomputed"] = gen_size
        results["generated_subgroup_size_cert"] = wit["size_of_subgroup_generated_by_x_y"]
        results["r0_size_cert"] = wit["size_of_R0"]
        results["generation_confirmed_recomputed"] = gen_size == wit["size_of_R0"]
        results["generation_match"] = (
            gen_size == wit["size_of_subgroup_generated_by_x_y"] == wit["size_of_R0"]
        )
        ok = ok and results["generation_match"]
    else:
        results["generation_status_cert"] = gen["status"]

    results["overall_cross_checked"] = ok  # cross-checked, NOT "verified" (Lean-reserved word)

    print(json.dumps(results, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
