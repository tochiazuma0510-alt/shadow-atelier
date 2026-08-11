#!/usr/bin/env python
# crosscheck/check_jac_chk2_modq_p17.py
# Independent checker for search/certs/jac_chk2_modq_v1_20260811_p17.json AND
# search/certs/jac_chk2_modq_v1_20260811_p19.json (裁定843/860, mod-q construction rewrite,
# p=17 and p=19 -- filename retained as "_p17" for git history continuity, now covers both).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT import search/jac_chk2_modq_v1.py or
# search/jac_construct_modq_v1.py -- this checker does NOT re-run the same construction code
# (that would not be independent, merely a repeat execution). Instead it checks, for EACH prime:
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
#      regression script's own self-report blindly) -- checked once, not per-prime.
import json
import math

CERTS = {
    17: "search/certs/jac_chk2_modq_v1_20260811_p17.json",
    19: "search/certs/jac_chk2_modq_v1_20260811_p19.json",
}
REGRESSION_CERT = "search/certs/jac_construct_modq_regression_test_v1_20260812.json"
EXACT_CERT = "search/certs/jac_chk_v1_20260811.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


def check_prime(p, cert_path):
    cert = json.load(open(cert_path, encoding="utf-8"))
    r = cert["per_p"][str(p)]

    if cert.get("schema") != "shadow-atelier/jac_chk2_modq_v1":
        fail(f"p={p}: schema mismatch")
    else:
        ok(f"p={p}: schema = shadow-atelier/jac_chk2_modq_v1")

    if not r["rank_agrees_across_q"]:
        fail(f"p={p}: rank_agrees_across_q is False")
    else:
        ok(f"p={p}: rank_agrees_across_q = True (q1_rank={r['modq1']['rank']}, "
           f"q2_rank={r['modq2']['rank']})")

    dim = r["dim_R_p"]
    if dim != p - 1:
        fail(f"p={p}: dim_R_p = {dim}, want {p-1} (=p-1)")
    else:
        ok(f"p={p}: dim_R_p = {dim} = p-1")

    # (A) isotypic multiplicities re-derived from (dim, chi_theta, chi_tau) via the standard
    # S3 character-table projection formulas (independently re-derived arithmetic)
    chi_theta = r["chi_theta"]
    chi_tau = r["chi_tau"]
    num_triv = dim + 3 * chi_theta + 2 * chi_tau
    num_sgn = dim - 3 * chi_theta + 2 * chi_tau
    num_std = dim - chi_tau
    if num_triv % 6 != 0 or num_sgn % 6 != 0 or num_std % 3 != 0:
        fail(f"p={p}: isotypic projection formulas do not divide evenly: num_triv={num_triv} "
             f"num_sgn={num_sgn} num_std={num_std}")
    else:
        m_triv_r = num_triv // 6
        m_sgn_r = num_sgn // 6
        m_std_r = num_std // 3
        cert_iso = r["isotypic"]
        if (m_triv_r, m_sgn_r, m_std_r) != (cert_iso["m_triv"], cert_iso["m_sgn"], cert_iso["m_std"]):
            fail(f"p={p}: isotypic rederived=({m_triv_r},{m_sgn_r},{m_std_r}) cert={cert_iso}")
        else:
            ok(f"p={p}: isotypic (m_triv,m_sgn,m_std)=({m_triv_r},{m_sgn_r},{m_std_r}) "
               f"independently re-derived from (dim={dim}, chi_theta={chi_theta}, "
               f"chi_tau={chi_tau}) via the standard S3 character projection formulas")
        if m_triv_r + m_sgn_r + 2 * m_std_r != dim:
            fail(f"p={p}: isotypic sum {m_triv_r + m_sgn_r + 2*m_std_r} != dim {dim}")
        else:
            ok(f"p={p}: isotypic dimension sum consistency confirmed")

    # (B) theoretical closed-form prediction (JAC-SYM, addendum C SS1.3) -- INDEPENDENT
    # mathematical check, not a re-run of the construction
    pred_triv_sgn = math.floor(p / 6 + 0.5)  # round(p/6)
    pred_std = (p - 1) // 3
    cert_iso = r["isotypic"]
    if (cert_iso["m_triv"], cert_iso["m_sgn"], cert_iso["m_std"]) != (pred_triv_sgn, pred_triv_sgn, pred_std):
        fail(f"p={p}: cert isotypic {cert_iso} does NOT match JAC-SYM theoretical prediction "
             f"(round(p/6),round(p/6),floor((p-1)/3))=({pred_triv_sgn},{pred_triv_sgn},{pred_std})")
    else:
        ok(f"p={p}: cert isotypic matches JAC-SYM theoretical closed-form prediction "
           f"({pred_triv_sgn},{pred_triv_sgn},{pred_std}) -- independent mathematical check, "
           f"not a re-run of the mod-q construction")

    # timing sanity (raw, informational)
    print(f"[INFO] p={p}: construction_time_sec q1={r['modq1'].get('construction_time_sec'):.1f} "
          f"q2={r['modq2'].get('construction_time_sec'):.1f}")


def main():
    for p, path in CERTS.items():
        check_prime(p, path)

    # (C) regression test cert cross-check against the ORIGINAL exact cert (independently re-read)
    # -- checked once (not tied to a specific prime)
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
              "against the original exact cert, for BOTH p=17 and p=19)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
