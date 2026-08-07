#!/usr/bin/env python3
"""
search/t2_hecke_v1.py -- T2-HECKE (裁定769(3), 司令塔), per
docs/notes/cone_design_v1_addendum_d.md §3.2 発注仕様 T2-HECKE (段
H-a..H-g), implemented within the addendum's own scope note: "これは
「C_k の住む環」の同定であって P-CONE-6' の枝判定ではない(ρ 側は σ̃
待ち)". This is infrastructure (Hecke action on the period-polynomial
lattice P_k^Z), not a resonance test.

*** Coboundary-projection disclosure (self-discovered, not in the
addendum's text -- see search/t2_hecke_common.py's module docstring for
full derivation/verification trail) ***
Applying the Heilbronn-Merel-style matrix-set Hecke action directly to
Brown's period-polynomial representative f_k does NOT land purely inside
P_k^Z -- it lands in P_k^Z + <X^(k-2)-Y^(k-2)> (a coboundary direction),
requiring an explicit projection step (search/t2_hecke_common.decompose)
before the action on P_k^Z itself can be read off. This was found via
several FAILED attempts at guessing the classical formula (all violating
H-b's calibration), then resolved via a from-scratch derivation dispatched
to the mathematician role (internal mathematical reasoning, NOT external
literature -- 文献ゲート compliant) and independently re-verified by this
implementer (direct hand+machine check: T_2 f_12 = -24 f_12 + 108(X^10-Y^10)
exactly, matching both the mathematician's derivation and this
implementer's own independent computation before trusting it further).

No verdict language -- raw values, integer matrices, factorizations, and
booleans only.
"""
import json
import sys
import time

sys.path.insert(0, "search")
import t2_hecke_common as t2

CANON_K = [12, 16, 18, 20, 22, 26]  # dim P_k = 1
DIM2_K = [24, 28, 30, 32]           # dim P_k = 2
NUM_BK_144169_CROSSCHECK = 103 * 2294797  # num(B_24), addendum §2.3: 144169 does NOT divide this


def write_out(out, path="search/certs/t2_hecke_v1_20260807.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {path}", flush=True)


def write_stop(stop_code, detail):
    out = {
        "schema": "shadow-atelier/t2_hecke_v1",
        "authority": "裁定769(3) (司令塔), docs/notes/cone_design_v1_addendum_d.md §3.2 発注仕様 T2-HECKE (verbatim)",
        "stop_code": stop_code,
        "stop_detail": detail,
    }
    write_out(out)
    print("T2_HECKE_STOP", flush=True)
    sys.exit(1)


def mat_to_jsonable(M):
    return [[str(c) if not isinstance(c, int) else c for c in row] for row in M]


def main():
    t_start = time.time()
    print("=== T2-HECKE: JOB START ===", flush=True)

    per_k = t2.load_per_k()

    # ---- H-a/H-b: k=12 calibration (S-T2-1, absolute STOP gate) ----
    M12, lambdas12, allint12, resid12, mats12 = t2.hecke_matrix_on_Pk(12, 2, per_k)
    t2_weight12 = M12[0][0]
    print(f"H-b calibration: T2_weight12={t2_weight12} (expect -24) lambda={lambdas12[0]} "
          f"all_integer={allint12} residual_zero={resid12}", flush=True)
    if not (allint12 and resid12):
        write_stop("H_B_NOT_INTEGER_OR_RESIDUAL", {"M12": M12, "lambdas12": [str(x) for x in lambdas12],
                                                     "all_integer": allint12, "residual_zero": resid12})
        return
    if t2_weight12 != -24:
        write_stop("H_B_CALIBRATION_FAIL", {"T2_weight12": t2_weight12, "expected": -24})
        return

    # ---- extra due-diligence cross-check: T_3 at k=12 (independent
    # calibration point, not addendum-mandated but strengthens confidence
    # in the coboundary-projection formula before trusting it further) ----
    M12_T3, lambdas12_T3, allint12_T3, resid12_T3, _ = t2.hecke_matrix_on_Pk(12, 3, per_k)
    t3_weight12 = M12_T3[0][0]
    t3_weight12_matches_known = (t3_weight12 == 252)  # classical tau(3)=252, independent literature-free cross-check
    print(f"[due diligence, not addendum-mandated] T3_weight12={t3_weight12} "
          f"(classical tau(3)=252): matches={t3_weight12_matches_known}", flush=True)

    # ---- H-c: dim P_k=1 weights ----
    a2_by_weight = {}
    for k in CANON_K:
        M, lambdas, allint, resid, mats = t2.hecke_matrix_on_Pk(k, 2, per_k)
        if not (allint and resid):
            write_stop("H_C_NOT_INTEGER_OR_RESIDUAL", {"k": k, "M": mat_to_jsonable(M),
                                                          "all_integer": allint, "residual_zero": resid})
            return
        a2_by_weight[k] = {"T2_scalar": M[0][0], "lambda_coboundary": str(lambdas[0])}
        print(f"H-c: k={k} T2={M[0][0]} lambda={lambdas[0]}", flush=True)

    # ---- H-d/H-e: dim P_k=2 weights ----
    disc_by_weight = {}
    T2_matrices = {}
    for k in DIM2_K:
        M, lambdas, allint, resid, mats = t2.hecke_matrix_on_Pk(k, 2, per_k)
        if not (allint and resid):
            write_stop("H_D_NOT_INTEGER_OR_RESIDUAL", {"k": k, "M": mat_to_jsonable(M),
                                                          "all_integer": allint, "residual_zero": resid})
            return
        trace, det = t2.charpoly_2x2(M)
        disc = t2.discriminant_2x2(M)
        T2_matrices[k] = M
        disc_by_weight[k] = {
            "T2_matrix": M,
            "lambdas_coboundary": [str(x) for x in lambdas],
            "trace": trace, "det": det, "disc": disc,
            "disc_factorization": {str(p): e for p, e in t2.factorize(disc).items()},
            "squarefree_part_disc": t2.squarefree_part(disc),
        }
        print(f"H-d/e: k={k} T2_matrix={M} trace={trace} det={det} disc={disc} "
              f"factorization={disc_by_weight[k]['disc_factorization']}", flush=True)

    # ---- P-T2-1: k=24, 144169 | disc ----
    disc_24 = disc_by_weight[24]["disc"]
    p_t2_1 = {
        "k": 24,
        "disc": disc_24,
        "144169_divides_disc": (disc_24 % 144169 == 0),
        "disc_equals_576_times_144169": (disc_24 == 576 * 144169),
        "trace": disc_by_weight[24]["trace"],
        "det": disc_by_weight[24]["det"],
        "a2_540_plus_minus_12sqrt144169_matches_charpoly": (
            disc_by_weight[24]["trace"] == 1080 and disc_by_weight[24]["det"] == -20468736
        ),
        "144169_divides_num_B24_cross_check": (NUM_BK_144169_CROSSCHECK % 144169 == 0),
    }
    print(f"P-T2-1: {p_t2_1}", flush=True)

    # ---- P-T2-2: k=28,30,32, disc raw values (new data, no established pin) ----
    p_t2_2 = {str(k): {"disc": disc_by_weight[k]["disc"],
                        "disc_factorization": disc_by_weight[k]["disc_factorization"],
                        "squarefree_part": disc_by_weight[k]["squarefree_part_disc"]}
              for k in [28, 30, 32]}
    print(f"P-T2-2: {p_t2_2}", flush=True)

    # ---- H-f: T_2 T_3 = T_3 T_2 commutativity (at k=24, the addendum's calibration weight) ----
    M24_T3, lambdas24_T3, allint24_T3, resid24_T3, _ = t2.hecke_matrix_on_Pk(24, 3, per_k)
    if not (allint24_T3 and resid24_T3):
        write_stop("H_F_T3_NOT_INTEGER_OR_RESIDUAL", {"k": 24, "M": mat_to_jsonable(M24_T3)})
        return
    T2_24 = T2_matrices[24]
    prod_23 = t2.matmul(T2_24, M24_T3)
    prod_32 = t2.matmul(M24_T3, T2_24)
    commute_24 = (prod_23 == prod_32)
    print(f"H-f: k=24 T2*T3={prod_23} T3*T2={prod_32} commute={commute_24}", flush=True)
    if not commute_24:
        write_stop("H_F_COMMUTATIVITY_FAIL", {"k": 24, "T2_T3": prod_23, "T3_T2": prod_32})
        return

    # ---- H-g: End_Hecke(P_k^Z) order identification (index of Z[T_2] in
    # the maximal order of the Hecke field Q(sqrt(squarefree part))) ----
    order_index = {}
    for k in DIM2_K:
        disc = disc_by_weight[k]["disc"]
        sf = disc_by_weight[k]["squarefree_part_disc"]
        # field discriminant of Q(sqrt(sf)): sf if sf%4==1, else 4*sf
        field_disc = sf if (sf % 4 == 1) else 4 * sf
        idx_sq = disc // field_disc if field_disc != 0 and disc % field_disc == 0 else None
        idx = None
        idx_is_perfect_square = None
        if idx_sq is not None and idx_sq >= 0:
            r = int(round(idx_sq ** 0.5))
            idx_is_perfect_square = (r * r == idx_sq)
            if idx_is_perfect_square:
                idx = r
        order_index[k] = {
            "disc_Z_T2": disc, "squarefree_part": sf, "field_disc_Q_sqrt_sf": field_disc,
            "index_squared_raw": idx_sq, "index_is_perfect_square": idx_is_perfect_square,
            "index_Z_T2_in_maximal_order": idx,
        }
        print(f"H-g: k={k} disc={disc} field_disc={field_disc} index_squared={idx_sq} "
              f"index={idx}", flush=True)

    out = {
        "schema": "shadow-atelier/t2_hecke_v1",
        "authority": "裁定769(3) (司令塔), docs/notes/cone_design_v1_addendum_d.md §3.2 発注仕様 T2-HECKE (verbatim)",
        "scope_disclosure": "これは「C_k が住む環 End_Hecke(P_k^Z)」の同定であって P-CONE-6' の枝判定ではない "
                            "(ρ側はσ̃待ち・addendum §3.1限定②)。disc(Z[T_2])はfull Hecke環の判別式の上界に "
                            "すぎない(addendum限定①)。",
        "coboundary_projection_disclosure": "T2_matrix values reported here are AFTER projecting out the "
                                            "coboundary direction X^(k-2)-Y^(k-2) (see "
                                            "search/t2_hecke_common.py module docstring) -- Brown's raw "
                                            "period-polynomial representative is not itself a Hecke "
                                            "eigenvector without this projection.",
        "H_a_matrix_set_T2": t2.hecke_matrix_set(2),
        "H_b_calibration": {
            "T2_weight12": t2_weight12, "expected": -24, "pass": (t2_weight12 == -24),
            "lambda_coboundary": str(lambdas12[0]), "all_integer": allint12, "residual_zero": resid12,
        },
        "due_diligence_T3_weight12": {
            "T3_weight12": t3_weight12, "classical_tau3_crosscheck": 252,
            "matches": t3_weight12_matches_known,
            "note": "not addendum-mandated -- extra self-imposed calibration point before trusting the "
                    "coboundary-projected formula at untested weights",
        },
        "H_c_a2_by_weight": {str(k): v for k, v in a2_by_weight.items()},
        "H_d_H_e_disc_by_weight": {str(k): {kk: (vv if not isinstance(vv, list) or kk != "T2_matrix" else vv)
                                              for kk, vv in v.items()} for k, v in disc_by_weight.items()},
        "P_T2_1": p_t2_1,
        "P_T2_2": p_t2_2,
        "H_f_commutativity": {
            "k": 24, "T2_T3": prod_23, "T3_T2": prod_32, "commute": commute_24,
        },
        "H_g_order_index": {str(k): v for k, v in order_index.items()},
        "no_verdict_note": "S-T2-3 compliance: raw numeric values, integer matrices, factorizations, and "
                           "booleans only. Judgment words are reserved for 司令塔/Sol.",
        "stop_code": None,
        "total_elapsed_sec": round(time.time() - t_start, 2),
    }
    write_out(out)
    print(f"=== T2-HECKE: JOB END total_elapsed_sec={out['total_elapsed_sec']} stop_code=None ===", flush=True)
    print("T2_HECKE_DONE", flush=True)


if __name__ == "__main__":
    main()
