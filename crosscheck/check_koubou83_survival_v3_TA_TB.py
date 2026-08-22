#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crosscheck/check_koubou83_survival_v3_TA_TB.py

Mathematician-directed final arbitration tests (commander instruction,
2026-08-22, following dispute_resolution ruling 1438) for this crosscheck's
own A1/A2 construction (crosscheck/check_koubou83_survival_v3.py):

T-A (linearization identity, word-level, no A on the LHS):
  For every basis vector w (this crosscheck's own basis = accepted window-
  defining words spanning V), for every representative (order2, order3), for
  both R1 and R2:
      Phi_red(R_i(m, f.w)) == r_i XOR (A_i . [w])      where [w] := Phi_red(w)
  LHS is computed purely via PBcoords + Fox2 + red (no A matrices). RHS uses
  this crosscheck's own A_i as a matrix-vector product. This is the defining
  property of "A_i is the correct linearization of R_i near f" -- a single
  failure anywhere would mean this crosscheck's A is wrong.

T-B (mathematician's paper prediction, independent of the whole basis-
  extraction/A-construction machinery):
  For the order3 representative (f = y*x^-1, confirmed below via PBcoords(F)),
  the mathematician predicts on paper that a specific test element
      w4 := x*y^3*x^-4   (sigma-word [1,1,2,2,2,2,2,2,-1,-1,-1,-1,-1,-1,-1,-1])
  is annihilated by BOTH A1 and A2 (claimed coincidence probability 2^-95 if
  this crosscheck's A were wrong), independent of the window (both windows
  tested).

Independence: producer GAP code is still never opened. All engine code is
imported from crosscheck/check_koubou83_survival_v3.py (this crosscheck's own
prior, from-scratch implementation) -- not producer code.
"""

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_koubou83_survival_v3 as C

REPO_ROOT = C.REPO_ROOT

W4_SIGMA_WORD = [1, 1, 2, 2, 2, 2, 2, 2, -1, -1, -1, -1, -1, -1, -1, -1]


def matvec(A, x, d):
    out = 0
    xx = x
    while xx:
        k = (xx & -xx).bit_length() - 1
        out ^= A[k]
        xx &= xx - 1
    return out


def run_T_A(id2, rep_name, cert):
    bs = C.build_basis_and_S(id2)
    d = bs["d"]
    key = "1152_%d" % id2
    rep_cert = next(r for r in cert["windows"][key]["representatives"] if r["representative"] == rep_name)
    res = C.process_representative(bs, rep_cert)
    A1, A2, r1, r2 = res["A1"], res["A2"], res["r1"], res["r2"]

    F = rep_cert["f_sigma_word"]
    m0 = bs["m0"]
    X, Xinv, Y, Yinv, degree = bs["X"], bs["Xinv"], bs["Y"], bs["Yinv"], bs["degree"]
    red_coords = bs["red_coords"]
    accepted_words = bs["accepted_words"]

    n_pass = 0
    n_fail = 0
    fail_examples = []
    for j, wj in enumerate(accepted_words):
        wcoord = red_coords(C.Phi_vec(wj, m0, X, Xinv, Y, Yinv, degree))
        fw = C.concat_reduced(F, wj)
        invfw = C.invert_word(fw)
        R1p = [1] + invfw + [2] + fw + [-2, -1] + fw
        R2p = invfw + [2] + fw + [1] + invfw + [-1, -2]
        lhs1 = red_coords(C.Phi_vec(R1p, m0, X, Xinv, Y, Yinv, degree))
        lhs2 = red_coords(C.Phi_vec(R2p, m0, X, Xinv, Y, Yinv, degree))
        rhs1 = r1 ^ matvec(A1, wcoord, d)
        rhs2 = r2 ^ matvec(A2, wcoord, d)
        ok = (lhs1 == rhs1) and (lhs2 == rhs2)
        if ok:
            n_pass += 1
        else:
            n_fail += 1
            if len(fail_examples) < 5:
                fail_examples.append({
                    "basis_index_j": j,
                    "wcoord_is_unit_e_j": (wcoord == (1 << j)),
                    "lhs1": lhs1, "rhs1": rhs1, "R1_identity_holds": (lhs1 == rhs1),
                    "lhs2": lhs2, "rhs2": rhs2, "R2_identity_holds": (lhs2 == rhs2),
                })

    return {
        "window_id2": id2, "representative": rep_name, "d": d,
        "n_basis_vectors_tested": len(accepted_words),
        "n_pass": n_pass, "n_fail": n_fail,
        "all_pass": (n_fail == 0),
        "fail_examples": fail_examples,
    }


def run_T_B(id2, cert):
    bs = C.build_basis_and_S(id2)
    d = bs["d"]
    key = "1152_%d" % id2
    rep_cert = next(r for r in cert["windows"][key]["representatives"] if r["representative"] == "order3")
    res = C.process_representative(bs, rep_cert)
    A1, A2 = res["A1"], res["A2"]

    m0 = bs["m0"]
    X, Xinv, Y, Yinv, degree = bs["X"], bs["Xinv"], bs["Y"], bs["Yinv"], bs["degree"]
    red_coords = bs["red_coords"]

    F = rep_cert["f_sigma_word"]
    F_xy_word, F_k = C.pbcoords(F)
    f_matches_paper_claim_yx_inv = (F_xy_word == [2, -1] and F_k == 0)

    w4_xy_word, w4_k = C.pbcoords(W4_SIGMA_WORD)
    w4_matches_paper_claim_xy3x4inv = (w4_xy_word == [1, 2, 2, 2, -1, -1, -1, -1] and w4_k == 0)

    w4_coord = red_coords(C.Phi_vec(W4_SIGMA_WORD, m0, X, Xinv, Y, Yinv, degree))
    a1w4 = matvec(A1, w4_coord, d)
    a2w4 = matvec(A2, w4_coord, d)

    return {
        "window_id2": id2, "d": d,
        "F_sigma_word": F,
        "PBcoords_F_xy_word": F_xy_word, "PBcoords_F_k": F_k,
        "F_matches_paper_claim_f_eq_y_xinv": f_matches_paper_claim_yx_inv,
        "w4_sigma_word": W4_SIGMA_WORD,
        "PBcoords_w4_xy_word": w4_xy_word, "PBcoords_w4_k": w4_k,
        "w4_matches_paper_claim_x_y3_xinv4": w4_matches_paper_claim_xy3x4inv,
        "w4_coord_bits": [(w4_coord >> i) & 1 for i in range(d)],
        "w4_coord_popcount": bin(w4_coord).count("1"),
        "A1_dot_w4": a1w4, "A2_dot_w4": a2w4,
        "A1_dot_w4_is_zero": (a1w4 == 0), "A2_dot_w4_is_zero": (a2w4 == 0),
        "both_annihilated": (a1w4 == 0 and a2w4 == 0),
    }


def main():
    cert = C.load_cert()

    T_A_results = []
    for id2 in (154161, 154163):
        for rep in ("order2", "order3"):
            T_A_results.append(run_T_A(id2, rep, cert))
    T_A_all_pass = all(r["all_pass"] for r in T_A_results)

    T_B_results = []
    for id2 in (154161, 154163):
        T_B_results.append(run_T_B(id2, cert))
    T_B_all_pass = all(r["both_annihilated"] for r in T_B_results)
    T_B_paper_claims_confirmed = all(
        r["F_matches_paper_claim_f_eq_y_xinv"] and r["w4_matches_paper_claim_x_y3_xinv4"]
        for r in T_B_results
    )

    out = {
        "schema": "shadow-atelier/koubou83-survival-v3-TA-TB/v1",
        "generated_by": "crosscheck/check_koubou83_survival_v3_TA_TB.py "
                         "(mathematician-directed final arbitration; uses this crosscheck's own "
                         "check_koubou83_survival_v3.py engine; producer GAP code never opened)",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "task": ("T-A: word-level linearization identity Phi_red(R_i(f.w)) == r_i XOR A_i.[w] "
                 "for every basis vector w, every representative, both windows -- no A on LHS. "
                 "T-B: mathematician's paper prediction that w4 = x*y^3*x^-4 is annihilated by "
                 "both A1 and A2 for the order3 (f=y*x^-1) representative, both windows."),
        "provenance": {
            "checker_script_path": "crosscheck/check_koubou83_survival_v3.py",
            "checker_script_sha256": C.sha256_of(os.path.join(REPO_ROOT, "crosscheck", "check_koubou83_survival_v3.py")),
            "producer_cert_path": C.PRODUCER_CERT_PATH,
            "producer_cert_sha256": C.sha256_of(os.path.join(REPO_ROOT, C.PRODUCER_CERT_PATH)),
            "producer_impl_gap_opened": False,
        },
        "T_A": {
            "results": T_A_results,
            "all_pass": T_A_all_pass,
            "total_checks": sum(r["n_basis_vectors_tested"] for r in T_A_results),
            "total_pass": sum(r["n_pass"] for r in T_A_results),
            "total_fail": sum(r["n_fail"] for r in T_A_results),
        },
        "T_B": {
            "results": T_B_results,
            "paper_claims_f_and_w4_confirmed_via_PBcoords": T_B_paper_claims_confirmed,
            "all_pass": T_B_all_pass,
        },
        "summary": {
            "T_A_all_pass": T_A_all_pass,
            "T_B_all_pass": T_B_all_pass,
            "both_tests_pass": (T_A_all_pass and T_B_all_pass),
        },
    }

    out_path = os.path.join(REPO_ROOT, "crosscheck", "koubou83_survival_v3_TA_TB_v1_20260822.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)

    print(json.dumps({
        "T_A": {"all_pass": T_A_all_pass, "total_checks": out["T_A"]["total_checks"],
                "total_pass": out["T_A"]["total_pass"], "total_fail": out["T_A"]["total_fail"]},
        "T_B": {"all_pass": T_B_all_pass,
                "paper_claims_confirmed": T_B_paper_claims_confirmed,
                "per_window": [{"id2": r["window_id2"], "A1_dot_w4": r["A1_dot_w4"],
                                "A2_dot_w4": r["A2_dot_w4"]} for r in T_B_results]},
    }, ensure_ascii=False, indent=2))
    return out


if __name__ == "__main__":
    main()
