#!/usr/bin/env python3
"""
search/cb_recon_sweep_v1.py -- CB-RECON e-side depth-4 sweep, k=16..32
(裁定763(8), 司令塔), per docs/notes/cone_design_v1_addendum_b.md §3.1
発注仕様 CB-RECON (段 W-a..W-e, 注意 N-1..N-6), verbatim within the
explicitly authorized scope.

*** SCOPE (裁定763(8) explicit restriction) ***
The rho-side (needing filtered sigma_tilde_m, m<=k-3 -- addendum N-1,
【CB-GAP-4】: sigma_13 not yet open even for k=16, k=32 needs
sigma_29 = out of scope entirely) is EXCLUDED from this order. Only the
"e-side" is implemented: this is the CR-1 (e_bar_12, 第二系統, 裁定759)
construction -- Definition 8.1 (8.4)(8.5)(8.6)(8.7) applied to a period
polynomial f -- generalized from the single weight-12 case to every
k=16..32, using the ALREADY-INDEPENDENTLY-DERIVED, ALREADY-CROSS-CHECKED
beta_k kernel vectors (search/certs/d2_snf_sweep_v1_20260807.json,
裁定752/756) as the period-polynomial source (see
search/cb_recon_common.py's module docstring for the full W-a methodology
disclosure -- a deviation from the addendum's literally-specified "direct
construction from S_2n's symmetry equations", justified by an explicit
canon-matching canary at k=12,16,18,20).

W-b/W-c (L_{k,4} rank from sigma-length-4 brackets, rho_matrix from
filtered lift) are OUT OF SCOPE per this order and are NOT attempted here
-- this script implements W-a, W-d, W-e only, treating "e" (my computed
object) as the direct proxy for the saturation question, per CONE-A's
claimed rho_k = c_k * e relation (c_k a scalar/matrix EXTERNAL to e,
carrying the Bernoulli-numerator "echo" -- already confirmed for k=12 in
CR-1/P-CONE-2, where e_12's own gcd=1 with 691 living entirely in c_12,
not in e's coordinates).

*** IMPORTANT SELF-CAUGHT BUG (disclosed, not hidden) ***
The first run of this script (against D2-SNF-1's kernel_basis_primitive
vectors AS-IS) found spurious torsion at every dim(P_k)=2 weight
(k=24,28,30,32: gcd_abs = 323,437,483,115 respectively) with prime
factors matching NONE of num(B_k)'s factors and NOT matching P-CONE-3's
built-in controls either -- a "surprise value" pattern investigated before
being reported as a finding (fail-closed discipline). Diagnosis: D2-SNF-1's
kernel_basis_primitive made EACH vector individually primitive (gcd of its
own entries = 1) but did NOT check that the PAIR of vectors jointly spans
a SATURATED rank-2 sublattice of the ambient pairs-space -- exactly the
addendum's own N-4 warning ("P_k の整基底は原始でなければならない(HNF
正準化必須)"). Direct check: SNF of the raw 2xN kernel-vector matrix
itself (BEFORE any e_f construction) already showed elementary divisors
[1,323]/[1,437]/[1,483]/[1,115] at k=24/28/30/32 -- an artifact of the
INPUT basis choice, propagating unchanged through the (injective) e_f
construction into the OUTPUT. Fixed via search/cb_recon_common.py's
saturate_kernel_basis() (uses sympy's smith_normal_decomp to extract the
true saturated Z-basis via the SNF transformation matrix's inverse -- see
that function's docstring for the linear-algebra justification). After
the fix, ALL weights (including the previously-spurious dim=2 ones) show
gcd_abs=1 / SNF=diag(1,1) exactly. This diagnostic trail (raw vs
saturated kernel, index found, before/after SNF) is recorded in this
cert's saturation_diagnostic fields for every dim=2 weight, not erased.

No verdict language anywhere -- raw values, integer vectors, and booleans
only. Judgment words ("保証延長", "本物", etc.) are reserved for 司令塔.
"""
import json
import sys
import time

sys.path.insert(0, "search")
import cb_recon_common as cb

# ---- addendum §1.3/§1.4 frozen tables (prereg, verbatim) ----
NUM_BK_FACTORIZATION = {
    12: {691: 1},
    16: {3617: 1},
    18: {43867: 1},
    20: {283: 1, 617: 1},
    22: {11: 1, 131: 1, 593: 1},
    24: {103: 1, 2294797: 1},
    26: {13: 1, 657931: 1},
    28: {7: 1, 9349: 1, 362903: 1},
    30: {5: 1, 1721: 1, 1001259881: 1},
    32: {37: 1, 683: 1, 305065927: 1},
}
BUILT_IN_CONTROLS = {22: 11, 26: 13, 28: 7, 30: 5}  # k -> control prime (p < k+3, divides num(B_k), NOT an irregular pair)
GUARANTEED_RANGE = [16, 18, 20, 22, 24, 26, 28, 30]  # P-CONE-4 (Brown motivicity check to weight 30)
CANON_K = [12, 16, 18, 20]
SWEEP_ORDER = [24, 16, 18, 20, 22, 26, 28, 30, 32]  # (103,24) calibration FIRST per 裁定763③, then dim=1 weights, then remaining dim=2, then (37,32) LAST


def canon_check():
    """W-a canary: f_k reindexing reproduces Brown's canon-verbatim
    coefficients EXACTLY for k=12,16,18,20 (the 'pin突合' the addendum's
    W-a table requires)."""
    canon_expected = {
        12: {(8, 2): 1, (2, 8): -1, (6, 4): -3, (4, 6): 3},
        16: {(12, 2): 2, (2, 12): -2, (10, 4): -7, (4, 10): 7, (8, 6): 11, (6, 8): -11},
        18: {(14, 2): 8, (2, 14): -8, (12, 4): -25, (4, 12): 25, (10, 6): 26, (6, 10): -26},
        20: {(16, 2): 3, (2, 16): -3, (14, 4): -10, (4, 14): 10, (12, 6): 14, (6, 12): -14,
             (10, 8): -13, (8, 10): 13},
    }
    per_k = cb.load_beta_k_kernels()
    results = {}
    for k in CANON_K:
        polys = cb.f_k_period_polynomials(k, per_k)
        assert len(polys) == 1, f"k={k} expected dim P_k=1"
        match = (polys[0] == canon_expected[k])
        results[k] = {"computed": {f"{i},{j}": c for (i, j), c in polys[0].items()},
                      "expected": {f"{i},{j}": c for (i, j), c in canon_expected[k].items()},
                      "match": match}
    return results


def process_weight(k, per_k):
    t0 = time.time()
    row = {"k": k}

    kernels_raw = per_k[str(k)]["kernel_basis_primitive"]
    dim_P_k = len(kernels_raw)
    row["dim_P_k"] = dim_P_k

    # ---- saturation diagnostic (self-caught bug, always recorded) ----
    if dim_P_k > 1:
        kernels_saturated = cb.saturate_kernel_basis(kernels_raw)
        from sympy import Matrix, ZZ
        from sympy.matrices.normalforms import smith_normal_form
        raw_snf = smith_normal_form(Matrix(kernels_raw), domain=ZZ)
        raw_diag = [int(raw_snf[i, i]) for i in range(min(raw_snf.rows, raw_snf.cols))]
        sat_snf = smith_normal_form(Matrix(kernels_saturated), domain=ZZ)
        sat_diag = [int(sat_snf[i, i]) for i in range(min(sat_snf.rows, sat_snf.cols))]
        row["saturation_diagnostic"] = {
            "kernel_basis_raw_from_D2_SNF_1": kernels_raw,
            "kernel_basis_raw_SNF": raw_diag,
            "raw_basis_was_already_saturated": (raw_diag == [1] * dim_P_k),
            "kernel_basis_saturated": kernels_saturated,
            "kernel_basis_saturated_SNF": sat_diag,
        }
    else:
        row["saturation_diagnostic"] = {"note": "dim_P_k=1: single primitive vector is automatically saturated"}

    # ---- W-a: f_k period polynomials (via saturated beta_k-kernel route) ----
    polys = cb.f_k_period_polynomials(k, per_k)
    row["f_k_degree"] = k - 2
    row["f_k_num_terms"] = [len(p) for p in polys]

    # ---- Definition 8.1 construction (f -> f0,f1 -> e_f), both routes ----
    e_rows = []
    internal_checks = []
    for idx, f in enumerate(polys):
        f0, f1, rem_zero = cb.deriv_f0_f1(f)
        if not rem_zero:
            return {"k": k, "stop_code": "REMAINDER_NONZERO", "poly_index": idx}
        eA = cb.build_e_f_route_A(f0, f1)
        eB = cb.build_e_f_route_B(f0, f1)
        route_match = (eA == eB)
        internal_checks.append({"poly_index": idx, "f0_num_terms": len(f0), "f1_num_terms": len(f1),
                                 "route_a_route_b_match": route_match, "e_f_num_terms": len(eA)})
        if not route_match:
            return {"k": k, "stop_code": "ROUTE_MISMATCH", "poly_index": idx}
        e_rows.append(eA)
    row["internal_checks"] = internal_checks
    row["e_f_degree"] = k - 4

    # ---- W-e: saturation judgment (gcd for dim1, SNF for dim2) ----
    snf_result = cb.snf_torsion_witness(e_rows)
    row["snf_result"] = snf_result
    row["saturated"] = (snf_result["gcd_abs"] == 1)

    # ---- P-CONE-3: built-in control prime test ----
    if k in BUILT_IN_CONTROLS:
        p = BUILT_IN_CONTROLS[k]
        row["P_CONE_3_control_prime"] = p
        row["P_CONE_3_control_prime_appears_in_torsion"] = (p in snf_result["torsion_primes"])

    # ---- P-CONE-6 ((103,24): rank_F103 direct computation) ----
    if k == 24:
        rank_103 = rank_mod_p(e_rows, 103)
        row["P_CONE_6_rank_F103"] = rank_103

    row["stop_code"] = None
    row["elapsed_sec"] = round(time.time() - t0, 3)
    return row


def rank_mod_p(rows, p):
    """rank over F_p of the integer matrix with given rows (dict-based
    sparse vectors), computed via straightforward Gaussian elimination
    mod p (small matrix: <=2 rows here)."""
    support = sorted(set().union(*[set(r.keys()) for r in rows])) if rows else []
    col_index = {w: i for i, w in enumerate(support)}
    M = [[0] * len(support) for _ in rows]
    for ridx, r in enumerate(rows):
        for w, c in r.items():
            M[ridx][col_index[w]] = c % p
    # gaussian elimination mod p
    rank = 0
    ncols = len(support)
    row_idx = 0
    for col in range(ncols):
        pivot = None
        for r in range(row_idx, len(M)):
            if M[r][col] % p != 0:
                pivot = r
                break
        if pivot is None:
            continue
        M[row_idx], M[pivot] = M[pivot], M[row_idx]
        inv = pow(M[row_idx][col], p - 2, p)
        M[row_idx] = [(x * inv) % p for x in M[row_idx]]
        for r in range(len(M)):
            if r != row_idx and M[r][col] % p != 0:
                factor = M[r][col]
                M[r] = [(M[r][c2] - factor * M[row_idx][c2]) % p for c2 in range(ncols)]
        row_idx += 1
        rank += 1
        if row_idx == len(M):
            break
    return rank


def write_out(out, path="search/certs/cb_recon_sweep_v1_20260807.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {path}", flush=True)


def write_stop(stop_code, detail):
    out = {
        "schema": "shadow-atelier/cb_recon_sweep_v1",
        "authority": "裁定763(8) (司令塔), docs/notes/cone_design_v1_addendum_b.md 発注仕様 CB-RECON (verbatim, e-side scope only)",
        "stop_code": stop_code,
        "stop_detail": detail,
    }
    write_out(out)
    print("CB_RECON_SWEEP_STOP", flush=True)
    sys.exit(1)


def main():
    t_start = time.time()
    print("=== CB-RECON e-side sweep: JOB START ===", flush=True)

    # ---- W-a canary: canon reproduction (STOP if fail) ----
    canon_results = canon_check()
    canon_all_match = all(r["match"] for r in canon_results.values())
    print(f"W-a canary (canon reproduction k=12,16,18,20): all_match={canon_all_match}", flush=True)
    if not canon_all_match:
        write_stop("WA_CANARY_FAIL", {"canon_results": {str(k): v for k, v in canon_results.items()}})
        return

    per_k = cb.load_beta_k_kernels()

    per_k_out = {}
    stop_hit = None
    for k in SWEEP_ORDER:
        row = process_weight(k, per_k)
        per_k_out[k] = row
        if row.get("stop_code") is not None:
            stop_hit = row
            print(f"k={k}: STOP {row['stop_code']} detail={row}", flush=True)
            break
        sat = row["saturated"]
        ed = row["snf_result"]["elementary_divisors"]
        tp = row["snf_result"]["torsion_primes"]
        print(f"k={k}: dim_P_k={row['dim_P_k']} saturated={sat} elementary_divisors={ed} "
              f"torsion_primes={tp} elapsed={row['elapsed_sec']}s", flush=True)

    if stop_hit is not None:
        write_stop("WEIGHT_PROCESSING_FAILED", {"failed_at_k": stop_hit["k"], "detail": stop_hit})
        return

    # ---- score P-CONE-3/4/5/6 (raw only) ----
    p_cone_3 = {}
    for k, p in BUILT_IN_CONTROLS.items():
        p_cone_3[k] = {
            "control_prime": p,
            "appears_in_torsion_primes": per_k_out[k]["P_CONE_3_control_prime_appears_in_torsion"],
            "torsion_primes_observed": per_k_out[k]["snf_result"]["torsion_primes"],
        }

    p_cone_4 = {
        "guaranteed_range": GUARANTEED_RANGE,
        "per_k_saturated": {str(k): per_k_out[k]["saturated"] for k in GUARANTEED_RANGE},
        "all_saturated": all(per_k_out[k]["saturated"] for k in GUARANTEED_RANGE),
    }

    p_cone_5 = {
        "k": 32,
        "elementary_divisors": per_k_out[32]["snf_result"]["elementary_divisors"],
        "torsion_primes": per_k_out[32]["snf_result"]["torsion_primes"],
        "saturated": per_k_out[32]["saturated"],
        "num_B32_factorization": NUM_BK_FACTORIZATION[32],
        "prime_37_appears_in_torsion_primes": (37 in per_k_out[32]["snf_result"]["torsion_primes"]),
        "branch_note": "branch E (SNF=diag(1,1)) vs branch X (SNF!=diag(1,1)) per addendum §2.2 -- "
                       "raw fact only, no 予想成立側/一級 language written here.",
        "scope_note": "E_32 here is the 'e' object (Definition 8.1 applied directly to the period "
                      "polynomial f_32), NOT rho_32 (which needs sigma_tilde_29, out of scope). Per "
                      "CONE-A (rho=c*e), c_32's numerator (37) is external to e's own coordinates and "
                      "is not expected to appear in E_32's elementary divisors regardless of branch -- "
                      "this differs from the addendum's literal framing ('c_32 で割った後の E_32 で判定') "
                      "which appears to assume E_32 as computed would already contain the c_32 factor "
                      "(i.e. assumes access to rho, not e alone); disclosed as an interpretive gap, not "
                      "resolved here.",
    }

    p_cone_6 = {
        "k": 24,
        "rank_F103_E24": per_k_out[24]["P_CONE_6_rank_F103"],
        "predicted_rank": 1,
        "matches_prediction": (per_k_out[24]["P_CONE_6_rank_F103"] == 1),
        "E24_saturated": per_k_out[24]["saturated"],
        "num_B24_factorization": NUM_BK_FACTORIZATION[24],
        "scope_note": "rank_F103(E_24) computed directly on 'e' (Definition 8.1 applied to f_24), NOT "
                      "on rho_24 (needs sigma_tilde_21, out of scope). P-CONE-6's stated mechanism "
                      "(Hecke-field splitting of 103 selecting exactly one of two eigenforms) is a "
                      "statement about rho's Hecke-module structure, which 'e' (built purely "
                      "combinatorially from the period polynomial, with no Hecke input) has no a priori "
                      "reason to reproduce -- disclosed as an interpretive gap, not resolved here. The "
                      "raw computed value is reported regardless.",
    }

    out = {
        "schema": "shadow-atelier/cb_recon_sweep_v1",
        "authority": "裁定763(8) (司令塔), docs/notes/cone_design_v1_addendum_b.md 発注仕様 CB-RECON (verbatim, e-side scope only)",
        "scope_disclosure": "rho-side (needs filtered sigma_tilde_m, out of scope per 裁定763(8) explicit "
                            "instruction: 'ρ側(σ̃必要分)は本発注の射程外'). W-b/W-c not attempted. Only "
                            "W-a (P_k^Z basis, via the already-cross-checked beta_k-kernel route, see "
                            "search/cb_recon_common.py docstring) and W-d/W-e (saturation of 'e' itself, "
                            "as a direct proxy object per CONE-A's rho=c*e claim) are implemented.",
        "self_caught_bug_disclosure": "first run (raw D2-SNF-1 kernel_basis_primitive, not jointly "
                                      "saturated) produced spurious torsion at all dim(P_k)=2 weights -- "
                                      "diagnosed and fixed via saturate_kernel_basis() BEFORE reporting "
                                      "any P-CONE score; see per_k[k].saturation_diagnostic for every "
                                      "dim=2 weight (24,28,30,32) -- both raw and saturated bases and "
                                      "their own SNF are recorded, nothing erased.",
        "sweep_order": SWEEP_ORDER,
        "W_a_canary_canon_reproduction": {str(k): v for k, v in canon_results.items()},
        "W_a_canary_all_match": canon_all_match,
        "per_k": {str(k): v for k, v in per_k_out.items()},
        "P_CONE_3": {str(k): v for k, v in p_cone_3.items()},
        "P_CONE_4": p_cone_4,
        "P_CONE_5": p_cone_5,
        "P_CONE_6": p_cone_6,
        "num_Bk_factorization_all_k": {str(k): {str(p): e for p, e in v.items()} for k, v in NUM_BK_FACTORIZATION.items()},
        "no_verdict_note": "S-D2-2-style compliance: raw numeric values, integer vectors, "
                           "factorizations, and booleans only. Judgment words ('保証延長', '本物', "
                           "'一級' etc.) and the go/no-go for QUAR-TOR firing on (37,32) are reserved "
                           "for 司令塔/Sol.",
        "stop_code": None,
        "total_elapsed_sec": round(time.time() - t_start, 2),
    }
    write_out(out)
    print(f"=== CB-RECON e-side sweep: JOB END total_elapsed_sec={out['total_elapsed_sec']} "
          f"stop_code=None ===", flush=True)
    print("CB_RECON_SWEEP_DONE", flush=True)


if __name__ == "__main__":
    main()
