#!/usr/bin/env python
# crosscheck/check_jac_chk2_modq_p17.py
# Independent checker for search/certs/jac_chk2_modq_v1_20260811_p17.json (裁定843, mod-q
# construction rewrite, p=17).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT import search/jac_chk2_modq_v1.py or
# search/jac_construct_modq_v1.py -- this checker does NOT re-run the same construction code
# (that would not be independent, merely a repeat execution). Instead it checks:
#  (A) internal arithmetic consistency: the isotypic multiplicities (m_triv,m_sgn,m_std) are
#      correctly derived from (dim, chi_theta, chi_tau) via the standard S3 character-table
#      projection formulas (re-derived here from scratch, not copied).
#  (B) agreement with the addendum C closed-form THEORETICAL prediction (JAC-SYM,
#      docs/notes/post_lazard_window_design_v1_addendum_c.md §1.3): m_triv=m_sgn=round(p/6),
#      m_std=floor((p-1)/3) -- this is a genuinely INDEPENDENT check (a different, purely
#      mathematical derivation, not a re-run of the same construction code).
#  (C) the regression test cert (search/certs/jac_construct_modq_regression_test_v1_20260812.json)
#      itself is checked for internal consistency against the ORIGINAL exact-Fraction cert
#      (search/certs/jac_chk_v1_20260811.json), independently re-read (not trusting the
#      regression script's own self-report blindly).
import json
import math

P17_CERT = "search/certs/jac_chk2_modq_v1_20260811_p17.json"
REGRESSION_CERT = "search/certs/jac_construct_modq_regression_test_v1_20260812.json"
EXACT_CERT = "search/certs/jac_chk_v1_20260811.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


def main():
    cert = json.load(open(P17_CERT, encoding="utf-8"))
    r = cert["per_p"]["17"]

    if cert.get("schema") != "shadow-atelier/jac_chk2_modq_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/jac_chk2_modq_v1")

    if not r["rank_agrees_across_q"]:
        fail("rank_agrees_across_q is False")
    else:
        ok(f"rank_agrees_across_q = True (q1_rank={r['modq1']['rank']}, "
           f"q2_rank={r['modq2']['rank']})")

    dim = r["dim_R_p"]
    if dim != 16:
        fail(f"dim_R_p = {dim}, want 16 (=p-1 for p=17)")
    else:
        ok(f"dim_R_p = {dim} = p-1")

    # (A) isotypic multiplicities re-derived from (dim, chi_theta, chi_tau) via the standard
    # S3 character-table projection formulas (independently re-derived arithmetic)
    chi_theta = r["chi_theta"]
    chi_tau = r["chi_tau"]
    num_triv = dim + 3 * chi_theta + 2 * chi_tau
    num_sgn = dim - 3 * chi_theta + 2 * chi_tau
    num_std = dim - chi_tau
    if num_triv % 6 != 0 or num_sgn % 6 != 0 or num_std % 3 != 0:
        fail(f"isotypic projection formulas do not divide evenly: num_triv={num_triv} "
             f"num_sgn={num_sgn} num_std={num_std}")
    else:
        m_triv_r = num_triv // 6
        m_sgn_r = num_sgn // 6
        m_std_r = num_std // 3
        cert_iso = r["isotypic"]
        if (m_triv_r, m_sgn_r, m_std_r) != (cert_iso["m_triv"], cert_iso["m_sgn"], cert_iso["m_std"]):
            fail(f"isotypic rederived=({m_triv_r},{m_sgn_r},{m_std_r}) cert={cert_iso}")
        else:
            ok(f"isotypic (m_triv,m_sgn,m_std)=({m_triv_r},{m_sgn_r},{m_std_r}) independently "
               f"re-derived from (dim={dim}, chi_theta={chi_theta}, chi_tau={chi_tau}) via the "
               f"standard S3 character projection formulas")
        if m_triv_r + m_sgn_r + 2 * m_std_r != dim:
            fail(f"isotypic sum {m_triv_r + m_sgn_r + 2*m_std_r} != dim {dim}")
        else:
            ok("isotypic dimension sum consistency confirmed")

    # (B) theoretical closed-form prediction (JAC-SYM, addendum C SS1.3) -- INDEPENDENT
    # mathematical check, not a re-run of the construction
    p = 17
    pred_triv_sgn = math.floor(p / 6 + 0.5)  # round(p/6)
    pred_std = (p - 1) // 3
    cert_iso = r["isotypic"]
    if (cert_iso["m_triv"], cert_iso["m_sgn"], cert_iso["m_std"]) != (pred_triv_sgn, pred_triv_sgn, pred_std):
        fail(f"cert isotypic {cert_iso} does NOT match JAC-SYM theoretical prediction "
             f"(round(p/6),round(p/6),floor((p-1)/3))=({pred_triv_sgn},{pred_triv_sgn},{pred_std})")
    else:
        ok(f"cert isotypic matches JAC-SYM theoretical closed-form prediction "
           f"({pred_triv_sgn},{pred_triv_sgn},{pred_std}) -- independent mathematical check, "
           f"not a re-run of the mod-q construction")

    # (C) regression test cert cross-check against the ORIGINAL exact cert (independently re-read)
    regression = json.load(open(REGRESSION_CERT, encoding="utf-8"))
    exact = json.load(open(EXACT_CERT, encoding="utf-8"))
    if not regression.get("all_anchors_pass"):
        fail("regression cert reports all_anchors_pass=False")
    else:
        ok("regression cert reports all_anchors_pass=True")

    mismatch = []
    for reg_r in regression["results"]:
        p_anchor = reg_r["p"]
        exact_r = exact["per_p"][str(p_anchor)]
        if reg_r["exact_dim"] != exact_r["rank_span_s_i"]:
            mismatch.append(f"p={p_anchor}: regression cert's exact_dim={reg_r['exact_dim']} "
                             f"!= original exact cert's rank_span_s_i={exact_r['rank_span_s_i']}")
        if reg_r["exact_isotypic"] != exact_r["isotypic"]:
            mismatch.append(f"p={p_anchor}: regression cert's exact_isotypic mismatch vs original")
        if not reg_r["point_pass"]:
            mismatch.append(f"p={p_anchor}: point_pass=False in regression cert")
    if mismatch:
        for m in mismatch:
            fail(m)
    else:
        ok("regression cert's claimed 'exact' reference values (p=5,7,11,13) independently "
           "verified against the ORIGINAL search/certs/jac_chk_v1_20260811.json (not just "
           "trusting the regression script's self-report)")

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} mismatches)")
        return 1
    else:
        print("RESULT: PASS (cross-checked, not verified -- 検証は Lean 専有; core mod-q "
              "construction/rank computation is NOT independently re-implemented here (same "
              "language/no independent algorithm available in reasonable time) -- checked via "
              "(A) internal arithmetic consistency, (B) an INDEPENDENT theoretical closed-form "
              "prediction match, and (C) independent re-verification of the regression anchors "
              "against the original exact cert)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
