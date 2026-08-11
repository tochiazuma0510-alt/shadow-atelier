#!/usr/bin/env python
# crosscheck/check_m5_win_chk.py
# Independent checker for search/certs/m5_win_chk_v1_20260811.json (M5-WIN-CHK,
# 裁定803[1]/HA-GAP-3, docs/notes/hunting_chapter_v1_addendum_a.md).
#
# CROSSCHECK, NOT VERIFICATION. This checker does NOT call GAP and does NOT import
# search/m5_win_chk_v1.g or search/hcen_ab_v1.g.
#
# DISCLOSED LIMITATION: the core result (M5_leq_PB3, i.e. whether
# GroupHomomorphismByImages(G_M5, S3, ...) succeeds) is a GAP-only group-theoretic
# primitive computation (existence of a specific homomorphism on a 3240-element
# permutation group). This checker CANNOT independently re-derive that primitive
# without either re-running GAP (which would violate search/crosscheck independence)
# or reimplementing the entire BuildQTGeneral construction + permutation group
# machinery in a second language -- neither is attempted here, following the same
# established convention as crosscheck/check_hcen_ab.py and crosscheck/check_sg_chir1.py
# (GAP/SmallGroup primitives are treated as machine ground truth; the checker's job
# is provenance/consistency/downstream-logic re-derivation, not re-deriving the
# primitive itself).
#
# What IS independently checked:
#  (A) internal consistency: order_ok==True implies order_of_B3_mod_M5==3240 (the
#      script's own documented expectation, re-derived from raw fields, not trusted
#      as asserted).
#  (B) cross-cert consistency: e_abelianization_order in this cert (independently
#      GAP-recomputed within m5_win_chk_v1.g via a SEPARATE DerivedSubgroup call on
#      the SAME reconstructed G_M5 object) matches the M5 control's "d" field already
#      recorded in the EARLIER, SEPARATELY-COMMITTED search/certs/hcen_ab_v1_20260811.json
#      (fa7b175) -- two independent GAP computations (different scripts, different runs)
#      of the same quantity (|(B3/M5)^ab|) converging is itself a form of cross-validation,
#      even though this checker only compares the two JSON outputs rather than re-running
#      either computation.
#  (C) e_even_necessary_condition is correctly derived from e_abelianization_order (pure
#      arithmetic, independently recomputed here).
#  (D) logical necessary-condition direction: if M5_leq_PB3 is True, then
#      e_even_necessary_condition must ALSO be True (per addendum_a theorem (I),
#      N<=PB3 implies e even) -- this is a NECESSARY-condition sanity check on the
#      cert's own two reported booleans, not a re-derivation of theorem (I) itself.
import json

CERT_PATH = "search/certs/m5_win_chk_v1_20260811.json"
HCEN_AB_PATH = "search/certs/hcen_ab_v1_20260811.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)

def main():
    cert = json.load(open(CERT_PATH, encoding="utf-8"))
    hcen = json.load(open(HCEN_AB_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/m5_win_chk_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/m5_win_chk_v1")

    # (A) order consistency
    order = cert.get("order_of_B3_mod_M5")
    order_expected = cert.get("order_expected")
    order_ok = cert.get("order_ok")
    if order_expected != 3240:
        fail(f"order_expected = {order_expected}, want 3240 (documented |B3:M5|)")
    else:
        ok("order_expected = 3240")
    rederived_order_ok = (order == order_expected)
    if rederived_order_ok != order_ok:
        fail(f"order_ok rederived={rederived_order_ok} (order={order} vs expected={order_expected}) cert={order_ok}")
    else:
        ok(f"order_ok rederived correctly (order={order})")

    # (B) cross-cert consistency: e value matches the EARLIER, independently-committed
    # hcen_ab_v1 cert's M5 control (fa7b175, committed before this script existed)
    e_here = cert.get("e_abelianization_order")
    m5_control = hcen.get("m5_control", {})
    e_hcen_ab = m5_control.get("d")
    if e_here != e_hcen_ab:
        fail(f"e_abelianization_order={e_here} (this cert) != hcen_ab_v1's M5_control.d={e_hcen_ab} "
             f"(search/certs/hcen_ab_v1_20260811.json, fa7b175) -- two independent GAP "
             f"computations of the same quantity disagree")
    else:
        ok(f"e_abelianization_order={e_here} matches hcen_ab_v1's independently-computed "
           f"M5_control.d={e_hcen_ab} (cross-cert consistency across two separate GAP runs)")

    # also cross-check order field against hcen_ab_v1's M5 control order
    hcen_order = m5_control.get("order")
    if order != hcen_order:
        fail(f"order={order} (this cert) != hcen_ab_v1's M5_control.order={hcen_order}")
    else:
        ok(f"order={order} matches hcen_ab_v1's M5_control.order={hcen_order}")

    # (C) e_even arithmetic re-derivation
    e_even_cert = cert.get("e_even_necessary_condition")
    e_even_rederived = (e_here is not None and e_here % 2 == 0)
    if e_even_rederived != e_even_cert:
        fail(f"e_even_necessary_condition rederived={e_even_rederived} (e={e_here}) cert={e_even_cert}")
    else:
        ok(f"e_even_necessary_condition={e_even_cert} correctly derived from e={e_here}")

    # (D) necessary-condition direction sanity check (addendum_a theorem (I): N<=PB3 => e even)
    m5_leq_pb3 = cert.get("M5_leq_PB3")
    if m5_leq_pb3 is True and e_even_cert is not True:
        fail(f"M5_leq_PB3=True but e_even_necessary_condition={e_even_cert} -- violates the "
             f"necessary-condition direction of addendum_a theorem (I) (N<=PB3 => e even); "
             f"this would indicate an internal inconsistency in the cert or in theorem (I) itself")
    else:
        ok(f"M5_leq_PB3={m5_leq_pb3} is consistent with e_even_necessary_condition={e_even_cert} "
           f"(necessary-condition direction of theorem (I) not violated)")

    # raw summary values (no verdict language)
    print()
    print(f"raw summary: M5_leq_PB3={m5_leq_pb3}, e={e_here}, j={e_here//2 if e_here else None} "
          f"(if e even), j_divides_3={(3 % (e_here//2) == 0) if (e_here and e_here % 2 == 0) else None}")
    print("DISCLOSED LIMITATION: the core boolean M5_leq_PB3 (GAP GroupHomomorphismByImages "
          "existence on a 3240-point permutation group) is NOT independently re-derived by this "
          "checker (see module docstring) -- only its internal/cross-cert consistency is checked.")

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} mismatches)")
        return 1
    else:
        print("RESULT: PASS (cross-checked, not verified -- 検証は Lean 専有; core GAP primitive not independently re-derived, see docstring)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
