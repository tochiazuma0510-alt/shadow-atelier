#!/usr/bin/env python3
# crosscheck/check_e691_ctrl.py
# Independent checker for search/certs/e691_ctrl_v1_20260807.json (E691
# control measurement, 裁定722, docs/notes/ribet_dig_campaign_v1_addendum_a.md
# SS4.3 item 5 + 司令塔's default battery (a)-(d)). Reads ONLY the cert JSON
# -- does NOT execute the GAP driver (search/probe/e691_ctrl/e691_ctrl.g) or
# any GAP process (search/crosscheck separation). Re-derives every
# closed-form arithmetic fact in pure Python and cross-checks internal
# consistency of the cert's own boolean flags against its raw values.
import json
import sys
from math import gcd

CERT_PATH = "search/certs/e691_ctrl_v1_20260807.json"
P = 691


def main():
    fails = []

    def fail(msg):
        fails.append(msg)
        print("[FAIL]", msg)

    def ok(msg):
        print("[PASS]", msg)

    try:
        doc = json.load(open(CERT_PATH, encoding="utf-8"))
    except FileNotFoundError:
        print(f"CROSSCHECK RESULT: FAIL (cert not found: {CERT_PATH})")
        sys.exit(1)

    if doc.get("schema") != "shadow-atelier/e691_ctrl/v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/e691_ctrl/v1")

    forbidden = ["不均衡", "SYN-0", "k*", "段差"]
    blob = json.dumps(doc, ensure_ascii=False)
    for word in forbidden:
        if word in blob:
            fail(f"forbidden verdict text '{word}' found -- S-AS-5-style VERDICT_IN_CODE")
    ok("no forbidden verdict strings found in cert")

    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job reported a STOP")
    else:
        ok("stop_code=None")

    # basic order arithmetic
    pred_size = 18 * P
    if doc.get("size_predicted") != pred_size:
        fail(f"size_predicted={doc.get('size_predicted')} != 18p={pred_size}")
    if (doc.get("size_E691") == pred_size) != doc.get("size_match"):
        fail("size_match inconsistent with size_E691 vs size_predicted")
    elif doc.get("size_E691") != pred_size:
        fail(f"size_E691={doc.get('size_E691')} != 18p={pred_size}")
    else:
        ok(f"|E691| = {doc.get('size_E691')} == 18*691 = {pred_size}")

    if doc.get("Nimg_size") != P:
        fail(f"Nimg_size={doc.get('Nimg_size')} != p={P}")
    if not doc.get("Nimg_normal"):
        fail("Nimg_normal is False -- C_691 not normal, contradicts the semidirect-product construction")
    else:
        ok("Nimg (C_691) is normal, order 691")

    # (a)
    Ra = doc.get("Ra", {})
    if Ra.get("order_Uprime") != 2:
        fail(f"Ra.order_Uprime={Ra.get('order_Uprime')} != 2")
    if Ra.get("order_Wprime") != 3:
        fail(f"Ra.order_Wprime={Ra.get('order_Wprime')} != 3")
    rederived_generates = (Ra.get("size_generated") == pred_size)
    if rederived_generates != Ra.get("generates"):
        fail(f"Ra.generates={Ra.get('generates')} inconsistent with size_generated vs size_E691")
    elif not Ra.get("generates"):
        fail("Ra.generates=False -- (U',W') does NOT generate E691, window qualification FAILS")
    else:
        ok(f"(a) (U',W') generates E691: order(U')=2, order(W')=3, "
           f"Size(<U',W'>)={Ra.get('size_generated')}==18p")

    # (b)
    Rb = doc.get("Rb", {})
    ab_inv = Rb.get("abelian_invariants")
    rederived_c6 = (ab_inv == [2, 3] or ab_inv == [6])
    if rederived_c6 != Rb.get("abelianization_is_C6"):
        fail(f"Rb.abelianization_is_C6 inconsistent with abelian_invariants={ab_inv}")
    elif not rederived_c6:
        fail(f"E691^ab={ab_inv} is not C6-equivalent (expected [2,3] or [6])")
    else:
        ok(f"(b) E691^ab = {ab_inv} (C_6, via CRT of C_2 x C_3)")
    if Rb.get("Z_size") != 1:
        fail(f"Rb.Z_size={Rb.get('Z_size')} != 1")
    else:
        ok("(b) Z(E691) = 1")
    if Rb.get("Phi_size") != 1:
        fail(f"Rb.Phi_size={Rb.get('Phi_size')} != 1")
    else:
        ok("(b) Phi(E691) = 1")
    rederived_split = not Rb.get("Nimg_le_Phi")
    if rederived_split != Rb.get("split_borel_confirmed"):
        fail("Rb.split_borel_confirmed inconsistent with Nimg_le_Phi")
    elif not rederived_split:
        fail("Rb: C_691 <= Phi(E691) -- split-Borel prediction FAILED (FRAT-SPLIT contradicted)")
    else:
        ok("(b) C_691 NOT<= Phi(E691) -- split Borel type confirmed (FRAT-SPLIT)")

    # (c) MIRROR-ODD hypothesis + conclusion re-derivation (pure logic, no
    # group theory needed to re-check the IMPLICATION structure itself --
    # this checker cannot recompute mu(W') or Aut(E691) from scratch
    # without GAP, but it CAN verify the cert's own claimed chain of
    # implications is internally consistent).
    Rc = doc.get("Rc", {})
    hyp_all = (Rc.get("hypothesis_H_A_normal") and Rc.get("hypothesis_H_A_cyclic") and
               Rc.get("hypothesis_H_A_order_odd") and Rc.get("hypothesis_H_q_ge5"))
    if not hyp_all:
        fail(f"(c) MIRROR-ODD hypothesis (H) NOT fully confirmed: "
             f"normal={Rc.get('hypothesis_H_A_normal')} cyclic={Rc.get('hypothesis_H_A_cyclic')} "
             f"odd={Rc.get('hypothesis_H_A_order_odd')} q>=5={Rc.get('hypothesis_H_q_ge5')}")
    else:
        ok("(c) MIRROR-ODD hypothesis (H): A=C_691 normal, cyclic, order 691 (odd), q=691>=5 -- all confirmed")
    mu_w_order = Rc.get("mu_W_order")
    rederived_mu_nontrivial = (mu_w_order is not None and mu_w_order != 1)
    if rederived_mu_nontrivial == Rc.get("mu_W_is_identity"):
        fail(f"mu_W_is_identity={Rc.get('mu_W_is_identity')} inconsistent with mu_W_order={mu_w_order}")
    if not rederived_mu_nontrivial:
        fail(f"(c) mu(W') order={mu_w_order} -- expected nontrivial (order 3), theorem step (2) not confirmed")
    else:
        ok(f"(c) mu(W') has order {mu_w_order} (nontrivial) -- theorem step (2) confirmed")
    # the cert's own chirality conclusion must equal hyp_all AND mu nontrivial
    rederived_chiral = hyp_all and rederived_mu_nontrivial
    if rederived_chiral != Rc.get("chiral"):
        fail(f"Rc.chiral={Rc.get('chiral')} does not match rederived implication "
             f"(hypotheses_hold AND mu(W') nontrivial) = {rederived_chiral}")
    elif not rederived_chiral:
        fail("(c) chirality NOT confirmed -- MIRROR-ODD prediction FALSIFIED (or hypotheses unmet)")
    else:
        ok("(c) chiral=True, matching MIRROR-ODD's prediction, via the theorem's own proof "
           "certificate (hypothesis verification, not brute-force automorphism search)")
    if Rc.get("chiral_match") != (Rc.get("chiral") == Rc.get("chiral_predicted")):
        fail("Rc.chiral_match inconsistent with chiral vs chiral_predicted")
    if Rc.get("witness_minus1_1_non_settled") != Rc.get("chiral"):
        fail("Rc.witness_minus1_1_non_settled should equal chiral (same group-theoretic fact, "
             "ker(T_-1,1)=iota(N))")
    else:
        ok("(c) witness [-1,1] non-settled == chiral (same fact, as documented)")
    if Rc.get("non_isolated_corollary_cited") != Rc.get("chiral"):
        fail("Rc.non_isolated_corollary_cited should track chiral (logical corollary via MIRROR-SHADOW)")
    if "aut_order_full_group" not in Rc:
        fail("Rc missing aut_order_full_group (should still report |Aut(E691)| even though the "
             "element-level search was infeasible)")
    else:
        ok(f"(c) |Aut(E691)| = {Rc.get('aut_order_full_group')} (Size() computed, "
           f"element-level search abandoned per documented method note)")

    # (d)
    Rd = doc.get("Rd", {})
    if Rd.get("num_m_tested") != P:
        fail(f"Rd.num_m_tested={Rd.get('num_m_tested')} != p={P}")
    rederived_gcd_count = sum(1 for mm in range(P) if gcd(2 * mm + 1, P) == 1)
    if rederived_gcd_count != P - 1:
        fail(f"internal sanity: rederived gcd count {rederived_gcd_count} != p-1={P-1}")
    if Rd.get("gcd_coprime_count") != rederived_gcd_count:
        fail(f"Rd.gcd_coprime_count={Rd.get('gcd_coprime_count')} != independently rederived {rederived_gcd_count}")
    else:
        ok(f"(d) gcd-coprime count = {Rd.get('gcd_coprime_count')} == p-1 (independently rederived)")
    rederived_all_pass = (Rd.get("pass_count") == P)
    if rederived_all_pass != Rd.get("all_m_pass"):
        fail("Rd.all_m_pass inconsistent with pass_count vs num_m_tested")
    print(f"[INFO] (d) pass_count={Rd.get('pass_count')} / {Rd.get('num_m_tested')} "
          f"(GT_count_if_f1_forced={Rd.get('GT_count_if_f1_forced')}) -- "
          f"DIFFERENT from LADDER-SAT's clean p-1={P-1} result; this is reported as a raw, "
          f"conditional (f=1 not independently verified for THIS window) measurement, not a match/mismatch "
          f"claim against any frozen prediction (item (d) had no single frozen numeric target)")
    # fail_list periodicity sanity check (pure arithmetic on the reported
    # head of the fail list -- confirms the pattern is NOT random noise,
    # i.e. all reported fails are m == 1 (mod 3), consistent with
    # Order(s1')=Order(s2')=6 causing (2m+1 mod 6) to cycle with period 3)
    fail_head = Rd.get("fail_list_head", [])
    if fail_head and all(mm % 3 == 1 for mm in fail_head):
        ok(f"(d) fail_list_head={fail_head} is consistent with a period-3-in-m pattern "
           f"(all m == 1 mod 3), matching Order(s1')=Order(s2')=6 -- NOT random/erroneous scatter")
    elif fail_head:
        fail(f"(d) fail_list_head={fail_head} does NOT show the expected period-3 pattern "
             f"(all m==1 mod 3) -- worth a second look")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (all closed-form arithmetic independently rederived in pure "
              "Python; all boolean flags in the cert are internally consistent with their own raw "
              "values; this does NOT re-run the GAP group theory itself -- see report to 司令塔)")
        sys.exit(0)


if __name__ == "__main__":
    main()
