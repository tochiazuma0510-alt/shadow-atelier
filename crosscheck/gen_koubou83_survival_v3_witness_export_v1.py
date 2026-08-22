#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crosscheck/gen_koubou83_survival_v3_witness_export_v1.py

Generates crosscheck/koubou83_survival_v3_witness_export_v1_20260822.json.

Purpose (commander instruction, 2026-08-22, following review of
check_koubou83_survival_v3.py's reported A1/A2 discrepancy): settle the
order2/DIES-AT-K disagreement via a CONVENTION-INDEPENDENT, word-level test.

For each window's order2 representative, this script:
  1. Re-derives this crosscheck's own solution xi of A1.xi=r1 / A2.xi=r2 (found
     by Gaussian elimination + back-substitution over this script's own basis;
     directly re-verified here by matrix-vector multiplication before use).
  2. Builds an explicit sigma-word witness w by concatenating (in ascending
     basis-index order, then freely reducing) the basis representative words
     (this crosscheck's own basis = accepted window-defining words) for which
     xi has a 1-bit.
  3. Forms f.w := F ++ w (F = the producer cert's pinned f_sigma_word for this
     representative), builds R1(f.w), R2(f.w) via the SAME template as before,
     and evaluates red(Phi(R_i)) using ONLY this script's Phi/PBcoords/Fox2/red
     pipeline -- NO A1/A2 matrices are used in this verification step. This is
     the same pipeline whose r1/r2 outputs were already confirmed to match the
     producer cert bit-for-bit exactly (see check_koubou83_survival_v3.py
     "all_r1_r2_match_exact": true), so this word-level result does not depend
     on the unresolved A1/A2 matrix-convention question.

All engine code is imported from crosscheck/check_koubou83_survival_v3.py
(this crosscheck's own independent implementation -- NOT producer code).
Producer GAP code is still never opened.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_koubou83_survival_v3 as C

REPO_ROOT = C.REPO_ROOT


def sha256_of(path):
    return C.sha256_of(path)


def solve_for_xi(A1, A2, r1, r2, d):
    def cols_to_rows(A, d):
        rows = [0] * d
        for i in range(d):
            col = A[i]
            for k in range(d):
                if (col >> k) & 1:
                    rows[k] |= (1 << i)
        return rows
    rows1 = cols_to_rows(A1, d)
    rows2 = cols_to_rows(A2, d)
    all_rows = list(zip(rows1, [((r1 >> k) & 1) for k in range(d)])) + \
               list(zip(rows2, [((r2 >> k) & 1) for k in range(d)]))
    pivots = []
    for coef, rhs in all_rows:
        c, r = coef, rhs
        for pc, pcoef, prhs in pivots:
            if (c >> pc) & 1:
                c ^= pcoef
                r ^= prhs
        if c == 0:
            if r == 1:
                return False, None
            continue
        low = (c & -c).bit_length() - 1
        pivots.append((low, c, r))
    pivots_sorted = sorted(pivots, key=lambda t: -t[0])
    solved = {}
    for pc, c, r in pivots_sorted:
        val = r
        cc = c & ~(1 << pc)
        xx = cc
        while xx:
            k = (xx & -xx).bit_length() - 1
            if k in solved:
                val ^= solved[k]
            xx &= xx - 1
        solved[pc] = val
    xi = 0
    for pc, val in solved.items():
        if val:
            xi |= (1 << pc)
    return True, xi


def matvec(A, x, d):
    out = 0
    xx = x
    while xx:
        k = (xx & -xx).bit_length() - 1
        out ^= A[k]
        xx &= xx - 1
    return out


def build_witness_word(xi, accepted_words):
    w = []
    for i, aw in enumerate(accepted_words):
        if (xi >> i) & 1:
            w = C.concat_reduced(w, aw)
    return w


def render_sigma_word(tokens):
    """Compact GAP-style rendering with run-length compression of consecutive
    identical-generator runs (readability only; tokens list is the source of truth)."""
    if not tokens:
        return "<identity>"
    parts = []
    cur_gen = None
    cur_count = 0

    def flush():
        if cur_gen is None:
            return
        letter = 'a' if abs(cur_gen) == 1 else 'b'
        exp = cur_count if cur_gen > 0 else -cur_count
        parts.append("%s^%d" % (letter, exp) if exp != 1 else letter)

    for t in tokens:
        gen = 1 if t in (1, -1) else 2
        sign = 1 if t > 0 else -1
        if cur_gen is not None and (1 if cur_gen in (1, -1) else 2) == gen and \
           (1 if cur_gen > 0 else -1) == sign:
            cur_count += 1
        else:
            flush()
            cur_gen = t
            cur_count = 1
    flush()
    return "*".join(parts)


def process_window(id2):
    cert = C.load_cert()
    bs = C.build_basis_and_S(id2)
    d = bs['d']
    key = "1152_%d" % id2
    w_cert = cert["windows"][key]
    rep_cert = next(r for r in w_cert["representatives"] if r["representative"] == "order2")
    res = C.process_representative(bs, rep_cert)
    A1, A2, r1, r2 = res["A1"], res["A2"], res["r1"], res["r2"]

    consistent, xi = solve_for_xi(A1, A2, r1, r2, d)
    xi_check = None
    if consistent:
        xi_check = {
            "A1_dot_xi_eq_r1": (matvec(A1, xi, d) == r1),
            "A2_dot_xi_eq_r2": (matvec(A2, xi, d) == r2),
        }

    accepted_words = bs["accepted_words"]
    wword = build_witness_word(xi, accepted_words) if consistent else None

    F = rep_cert["f_sigma_word"]
    out = {
        "window_id": [1152, id2],
        "f_pin": {
            "f_sigma_word": F,
            "f_sigma_word_text": render_sigma_word(F),
            "source": "producer cert search/certs/koubou83_survival_v3_20260822.json, "
                       "windows.1152_%d.representatives[order2].f_sigma_word (used verbatim, as a pin)" % id2,
        },
        "xi": {
            "consistent_per_this_crosscheck_own_A1_A2": consistent,
            "xi_bits": [(xi >> i) & 1 for i in range(d)] if consistent else None,
            "xi_int_repr": xi if consistent else None,
            "popcount": bin(xi).count("1") if consistent else None,
            "d_dimension": d,
            "re_verification_against_own_A1_A2": xi_check,
        },
    }

    if not consistent:
        out["witness_sigma_word"] = None
        out["direct_verification"] = {
            "note": "This crosscheck's own A1/A2 system was INCONSISTENT for this window "
                    "(no xi to build a witness word from) -- not expected given the prior "
                    "run's result; recorded raw."
        }
        return out

    fw = C.concat_reduced(F, wword)
    invfw = C.invert_word(fw)
    R1p = [1] + invfw + [2] + fw + [-2, -1] + fw
    R2p = invfw + [2] + fw + [1] + invfw + [-1, -2]

    m0 = bs["m0"]
    X, Xinv, Y, Yinv, degree = bs["X"], bs["Xinv"], bs["Y"], bs["Yinv"], bs["degree"]
    red_coords = bs["red_coords"]

    r1p_vec = C.Phi_vec(R1p, m0, X, Xinv, Y, Yinv, degree)
    r2p_vec = C.Phi_vec(R2p, m0, X, Xinv, Y, Yinv, degree)
    r1p = red_coords(r1p_vec)
    r2p = red_coords(r2p_vec)

    out["witness_sigma_word"] = {
        "construction": "w := concat_reduced over i (ascending basis index) of accepted_words[i] "
                         "for each i with xi_bits[i]==1; f.w := concat_reduced(F, w)",
        "w_tokens": wword,
        "w_text": render_sigma_word(wword),
        "w_length_after_free_reduction": len(wword),
        "fw_tokens": fw,
        "fw_text": render_sigma_word(fw),
        "fw_length_after_free_reduction": len(fw),
    }
    out["direct_verification"] = {
        "method": "red(Phi(R_i(m=0, f.w))) computed via PBcoords + Fox2 + RREF-reduce ONLY -- "
                  "NO A1/A2 matrices used in this step.",
        "red_Phi_R1_fw_bits": [(r1p >> i) & 1 for i in range(d)],
        "red_Phi_R2_fw_bits": [(r2p >> i) & 1 for i in range(d)],
        "red_Phi_R1_fw_is_zero": (r1p == 0),
        "red_Phi_R2_fw_is_zero": (r2p == 0),
        "direct_verification_passes": (r1p == 0 and r2p == 0),
    }
    return out


def main():
    windows_out = {}
    for id2 in (154161, 154163):
        windows_out["1152_%d" % id2] = process_window(id2)

    all_pass = all(
        w.get("direct_verification", {}).get("direct_verification_passes") is True
        for w in windows_out.values()
    )

    out = {
        "schema": "shadow-atelier/koubou83-survival-v3-witness-export/v1",
        "generated_by": "crosscheck/gen_koubou83_survival_v3_witness_export_v1.py "
                         "(uses crosscheck/check_koubou83_survival_v3.py's own independent engine; "
                         "no A1/A2 matrices used in the direct_verification step; producer GAP code "
                         "never opened)",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "task": "Commander-directed convention-independent, word-level settlement of the order2/"
                "DIES-AT-K disagreement reported in koubou83_survival_v3_crosscheck_v1_20260822.json: "
                "build an explicit sigma-word witness from this crosscheck's own solution xi (of its "
                "own A1.xi=r1/A2.xi=r2), then verify red(Phi(R_i(f.w)))==0 using Phi/PBcoords/Fox2/red "
                "ONLY -- the same sub-pipeline whose r1/r2 outputs already matched the producer cert "
                "bit-for-bit exactly, so this result does not depend on the unresolved A1/A2 matrix "
                "storage/operator-order convention question.",
        "provenance": {
            "checker_script_path": "crosscheck/check_koubou83_survival_v3.py",
            "checker_script_sha256": sha256_of(os.path.join(REPO_ROOT, "crosscheck", "check_koubou83_survival_v3.py")),
            "producer_cert_path": C.PRODUCER_CERT_PATH,
            "producer_cert_sha256": sha256_of(os.path.join(REPO_ROOT, C.PRODUCER_CERT_PATH)),
            "producer_impl_gap_opened": False,
            "producer_impl_gap_path": C.PRODUCER_IMPL_PATH,
        },
        "windows": windows_out,
        "summary": {
            "all_direct_verifications_pass": all_pass,
            "interpretation": (
                "direct_verification_passes==True for a window means: this crosscheck's own A1/A2 "
                "system genuinely has a solution xi, AND the explicit sigma-word witness built from "
                "that xi independently satisfies red(Phi(R_i(f.w)))=0 via the Phi-only pipeline "
                "(no matrices) -- i.e. under this crosscheck's own construction, order2 is SURVIVES-K, "
                "confirmed at the word level, not merely at the matrix-algebra level. Recorded raw "
                "either way; no reconciliation attempted with the producer's DIES-AT-K claim."
            ),
        },
    }

    out_path = os.path.join(REPO_ROOT, "crosscheck", "koubou83_survival_v3_witness_export_v1_20260822.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)

    print(json.dumps({"summary": out["summary"]}, ensure_ascii=False, indent=2))
    return out


if __name__ == "__main__":
    main()
