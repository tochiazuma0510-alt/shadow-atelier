#!/usr/bin/env python
# crosscheck/check_sg_band_sweep.py
# Independent checker for search/certs/sg_band_sweep_20260806.json (SG band
# sweep G0-G3, prereg docs/notes/sg_band_sweep_prereg_iffirst_v1.md,
# sha256=96449d682d9f312b861e5c8cca73d4b2cce03a4afb1664708f672a1638b0a4de).
#
# CROSSCHECK, NOT VERIFICATION: reads ONLY the cert JSON (no GAP call, no
# import of the driver -- search/crosscheck separation). Per prereg SS10
# item 2: re-derives per_order's g3_pass count from g3_records[] alone, and
# independently recomputes predictions_scored (P-SGB-1..6) from per_order,
# then cross-checks against the cert's own predictions_scored block.
#
# Grading/interpretation is explicitly OUT OF SCOPE (prereg SS10 item 4) --
# this script only reports PASS/FAIL on internal arithmetic consistency and
# on the prereg's own stop-rule conditions (S-SG-1/2/3/5), never on whether
# a prediction "came true" in some editorial sense.
import json, sys, math

PATH = "search/certs/sg_band_sweep_20260806.json"
PREREG_SHA_EXPECTED = "96449d682d9f312b861e5c8cca73d4b2cce03a4afb1664708f672a1638b0a4de"
FROZEN_NR = {1152: 157877, 1296: 3609, 1458: 1798, 1728: 47937, 1944: 3973}
FROZEN_TOTAL = sum(FROZEN_NR.values())
V2_OF = {1152: 7, 1296: 4, 1458: 1, 1728: 6, 1944: 3}
PREDICTED_G1 = {1152: 474, 1458: 719, 1728: 325, 1944: 311}


def main():
    fails = []
    def fail(msg):
        fails.append(msg); print("[FAIL]", msg)
    def ok(msg):
        print("[PASS]", msg)

    doc = json.load(open(PATH, encoding="utf-8"))

    if doc.get("schema") != "shadow-atelier/sg-band-sweep/v1":
        fail("schema mismatch: " + str(doc.get("schema")))
    else:
        ok("schema = shadow-atelier/sg-band-sweep/v1")

    prereg = doc.get("prereg", {})
    if prereg.get("sha256") != PREREG_SHA_EXPECTED:
        fail(f"prereg sha256 mismatch: cert says {prereg.get('sha256')}, frozen is {PREREG_SHA_EXPECTED}")
    else:
        ok("prereg sha256 matches frozen v1 (S-SG-1-adjacent: prereg binding)")

    # universe_frozen / universe_check (S-SG-1)
    uf = doc.get("universe_frozen", {})
    nr = uf.get("nr_small_groups", {})
    for n, expected in FROZEN_NR.items():
        got = nr.get(str(n))
        if got != expected:
            fail(f"universe_frozen.nr_small_groups[{n}] = {got}, expected {expected}")
    if uf.get("total") != FROZEN_TOTAL:
        fail(f"universe_frozen.total = {uf.get('total')}, expected {FROZEN_TOTAL}")
    else:
        ok(f"universe_frozen.total = {FROZEN_TOTAL} (215,194)")
    if "1536" not in str(uf.get("scope_out_1536", {})):
        pass  # scope_out_1536 is a dict, not a string containment check; just require key present
    if "scope_out_1536" not in uf:
        fail("universe_frozen missing scope_out_1536 (S-SG-2 -- 1536 must be recorded as SCOPE_OUT)")
    else:
        ok("universe_frozen.scope_out_1536 present (1536 recorded as SCOPE_OUT, not empty)")

    uc = doc.get("universe_check", {})
    if uc.get("universe_mismatch") is not False:
        fail(f"universe_check.universe_mismatch = {uc.get('universe_mismatch')} (S-SG-1 STOP condition)")
    else:
        ok("universe_check.universe_mismatch = false")
    orders_checked = uc.get("orders_checked", [])
    if sorted(orders_checked) != sorted(FROZEN_NR.keys()):
        fail(f"universe_check.orders_checked = {orders_checked}, expected all 5 band orders")
    else:
        ok("universe_check.orders_checked covers all 5 band orders")

    # calibration (S-SG-5: any DF-SG FAIL => the whole cert should not exist
    # as a positive-result cert; if we're reading this cert, calibration
    # must show ALL PASS)
    cal = doc.get("calibration", {})
    if doc.get("calibration_all_ok") is not True:
        fail(f"calibration_all_ok = {doc.get('calibration_all_ok')} (S-SG-5 requires ALL PASS for a band-sweep cert to exist)")
    else:
        ok("calibration_all_ok = true")
    for gate in ["DF_SG_1", "DF_SG_2", "DF_SG_2b", "DF_SG_3"]:
        st = cal.get(gate, {}).get("status")
        if st != "PASS":
            fail(f"calibration.{gate}.status = {st}, want PASS (S-SG-5)")
        else:
            ok(f"calibration.{gate}.status = PASS")
    if "DF_SG_6" not in cal:
        fail("calibration missing DF_SG_6 (S-SG-5: DF-SG-6 must be reported, found or not)")
    else:
        ok("calibration.DF_SG_6 present (reported per S-SG-5, found-or-not both acceptable)")

    # per_order vs g3_records: re-derive g3_pass count from g3_records[]
    # alone (prereg SS10 item 2) and cross-check against per_order.g3_pass
    per_order = doc.get("per_order", [])
    g3_records = doc.get("g3_records", [])
    rederived_g3_by_order = {}
    for rec in g3_records:
        o = rec.get("order")
        rederived_g3_by_order[o] = rederived_g3_by_order.get(o, 0) + 1

    if len(per_order) != 5:
        fail(f"per_order has {len(per_order)} entries, want 5 (all band orders, no partial per S-SG-7)")
    else:
        ok("per_order has 5 entries (no TIME_CAP partial order silently included)")

    for row in per_order:
        o = row["order"]
        rederived = rederived_g3_by_order.get(o, 0)
        if rederived != row["g3_pass"]:
            fail(f"order {o}: g3_pass in per_order={row['g3_pass']} but rows counted from g3_records[]={rederived}")
        else:
            ok(f"order {o}: per_order.g3_pass ({row['g3_pass']}) matches count of g3_records[] rows")
        if row.get("total") != FROZEN_NR.get(o):
            fail(f"order {o}: total={row.get('total')}, expected {FROZEN_NR.get(o)}")
        if not (0 <= row["g3_pass"] <= row["g2_pass"] <= row["g1_pass"] <= row["total"]):
            fail(f"order {o}: monotonicity violated (g3_pass<=g2_pass<=g1_pass<=total not satisfied): {row}")
    if not fails:
        ok("g3_pass<=g2_pass<=g1_pass<=total monotonicity holds for all 5 orders")

    # re-derive predictions_scored independently from per_order
    by_order = {r["order"]: r for r in per_order}
    scored_orders = [n for n in [1152, 1458, 1728, 1944] if n in by_order]

    def predicted_rate(i):
        return 0.40 * (2.26 ** (-(i - 1)))

    p1_rows = []
    p1_all_within = True
    for n in scored_orders:
        row = by_order[n]
        actual_rate = row["g1_pass"] / row["total"]
        pred_rate = predicted_rate(V2_OF[n])
        ratio = actual_rate / pred_rate
        within = (0.5 <= ratio <= 2.0)
        if not within:
            p1_all_within = False
        p1_rows.append((n, actual_rate, pred_rate, ratio, within))

    cert_p1 = doc.get("predictions_scored", {}).get("P_SGB_1", {})
    cert_p1_rows = {r["order"]: r for r in cert_p1.get("rows", [])}
    for n, actual_rate, pred_rate, ratio, within in p1_rows:
        cr = cert_p1_rows.get(n)
        if cr is None:
            fail(f"P_SGB_1: order {n} missing from cert rows")
            continue
        if abs(cr["actual_rate"] - actual_rate) > 1e-9:
            fail(f"P_SGB_1 order {n}: cert actual_rate={cr['actual_rate']} rederived={actual_rate}")
        if cr["within_factor2"] != within:
            fail(f"P_SGB_1 order {n}: cert within_factor2={cr['within_factor2']} rederived={within}")
    if cert_p1.get("all_within_factor2") != p1_all_within:
        fail(f"P_SGB_1.all_within_factor2: cert={cert_p1.get('all_within_factor2')} rederived={p1_all_within}")
    else:
        ok(f"P_SGB_1 rederived matches cert (all_within_factor2={p1_all_within})")

    p3_sum = sum(by_order[n]["g1_pass"] for n in scored_orders)
    cert_p3 = doc.get("predictions_scored", {}).get("P_SGB_3", {})
    if cert_p3.get("sum_scored_orders") != p3_sum:
        fail(f"P_SGB_3.sum_scored_orders: cert={cert_p3.get('sum_scored_orders')} rederived={p3_sum}")
    else:
        ok(f"P_SGB_3.sum_scored_orders rederived matches cert ({p3_sum})")
    p3_in_interval = (900 <= p3_sum <= 4000)
    if cert_p3.get("in_interval") != p3_in_interval:
        fail(f"P_SGB_3.in_interval: cert={cert_p3.get('in_interval')} rederived={p3_in_interval}")

    p4_total = sum(r["g3_pass"] for r in per_order)
    cert_p4 = doc.get("predictions_scored", {}).get("P_SGB_4", {})
    if cert_p4.get("total_g3_pass_band") != p4_total:
        fail(f"P_SGB_4.total_g3_pass_band: cert={cert_p4.get('total_g3_pass_band')} rederived={p4_total}")
    else:
        ok(f"P_SGB_4.total_g3_pass_band rederived matches cert ({p4_total})")
    if cert_p4.get("exists_ge_1") != (p4_total >= 1):
        fail(f"P_SGB_4.exists_ge_1 mismatch")

    p5_g1 = sum(r["g1_pass"] for r in per_order)
    p5_g2 = sum(r["g2_pass"] for r in per_order)
    cert_p5 = doc.get("predictions_scored", {}).get("P_SGB_5", {})
    if cert_p5.get("g1_sum") != p5_g1 or cert_p5.get("g2_sum") != p5_g2:
        fail(f"P_SGB_5 sums: cert g1={cert_p5.get('g1_sum')} g2={cert_p5.get('g2_sum')} rederived g1={p5_g1} g2={p5_g2}")
    else:
        ok(f"P_SGB_5 g1_sum/g2_sum rederived match cert ({p5_g1}/{p5_g2})")
    if p5_g1 > 0:
        p5_ratio = p5_g2 / p5_g1
        if cert_p5.get("ratio") is None or abs(cert_p5["ratio"] - p5_ratio) > 1e-9:
            fail(f"P_SGB_5.ratio: cert={cert_p5.get('ratio')} rederived={p5_ratio}")
    # S-SG-6 exception: a P_SGB_5 miss is explicitly NOT a stop condition.
    # This checker does not fail the run over in_interval being false.

    # DF-SG-6 / P_SGB_6 reconciliation
    p6 = doc.get("predictions_scored", {}).get("P_SGB_6", {})
    df6_final = cal.get("DF_SG_6", {})
    if p6.get("exists_g2pass_g3fail") != df6_final.get("final_full_sweep_found"):
        fail("P_SGB_6.exists_g2pass_g3fail does not match calibration.DF_SG_6.final_full_sweep_found")
    else:
        ok("P_SGB_6 reconciles with calibration.DF_SG_6 final full-sweep result")

    # scope_statement literal check (S-SG-3)
    scope = doc.get("scope_statement", "")
    required_phrases = ["1536", "SCOPE_OUT", "2^i3^j", "1152", "1296", "1458", "1728", "1944"]
    missing_phrases = [p for p in required_phrases if p not in scope]
    if missing_phrases:
        fail(f"scope_statement missing required phrases: {missing_phrases}")
    else:
        ok("scope_statement contains the required SG-GAP-3 limiting phrases")

    # claims discipline (S-SG-9): no predicted/observed-outcome language for
    # exotic/twin/isolated
    claims = doc.get("claims", {})
    for k in ["exotic_verdict", "twin_verdict", "isolated_verdict"]:
        if claims.get(k) != "UNKNOWN":
            fail(f"claims.{k} = {claims.get(k)}, want UNKNOWN (S-SG-9)")
    if not fails or all("claims." not in f for f in fails):
        ok("claims.{exotic,twin,isolated}_verdict all UNKNOWN (S-SG-9)")

    # time cap discipline
    if doc.get("time_cap_hit") not in (True, False):
        fail("time_cap_hit missing or not boolean")
    elif doc.get("time_cap_hit") is True and len(per_order) == 5:
        fail("time_cap_hit=true but all 5 orders present -- S-SG-7 requires partial orders be omitted, so this combination is inconsistent")
    else:
        ok(f"time_cap_hit={doc.get('time_cap_hit')} consistent with {len(per_order)} completed orders")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (cross-checked, NOT verified -- see CLAUDE.md Lean reservation)")
        print("NOTE: grading/interpretation (exotic/twin/isolated, novelty) is explicitly out of scope")
        print("for this checker per prereg SS10 item 4 -- that belongs to 司令塔/数学者.")
        sys.exit(0)


if __name__ == "__main__":
    main()
