#!/usr/bin/env python
# crosscheck/check_meas_chi_m5.py
# Independent checker for search/certs/meas_chi_m5_v1_20260811.json (MEAS-CHI-M5, 裁定805,
# docs/notes/card_pchi_m5_v1.md).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT call GAP, does NOT import search/meas_chi_m5_v1.g.
#
# DISCLOSED LIMITATION: the core per-chief-factor measurement (ChiefSeries + conjugation
# action orbit/kernel computation on the reconstructed 3240-element permutation group G_M5) is
# a GAP-only primitive. Not independently re-derived here (same convention as
# crosscheck/check_m5_win_chk.py / crosscheck/check_hcen_ab.py / crosscheck/check_pchi1.py).
#
# What IS independently checked:
#  (A) order/order_ok consistency, and cross-cert match against the EARLIER, separately
#      committed search/certs/m5_win_chk_v1_20260811.json (115ffeb) and
#      search/certs/hcen_ab_v1_20260811.json (fa7b125/fa7b175)'s M5_control -- THREE
#      independent GAP runs (three different scripts) of "order of B3/M5" should all agree.
#  (B) |G| = 3240 = 2^3*3^4*5 factorization sanity: every reported chief-factor characteristic
#      p (where elementary abelian) must divide 3240, and must be in {2,3,5}.
#  (C) product-of-chief-factor-sizes = |G| (a basic chief-series sanity check, independently
#      recomputed from the raw w_size list).
#  (D) downstream boolean re-derivation: dim1_summary fields, dimGe2_factors_count,
#      nonabelian_factors_count, dimGe2_with_5_in_g_mod_cg_w_count -- all recomputed from the
#      raw chief_factors[] list and compared against the cert's own reported values.
#  (E) theorem-consistency check (TWIST-GCD, card_pchi_m5_v1.md §2.1): for each dim=1 factor,
#      gcd(e,p-1) with e=10 (the already cross-checked M5 e value) must be DIVISIBLE BY
#      ord_chi_w (i.e. ord_chi_w must divide gcd(10,p-1)) -- pure arithmetic, independently
#      checked without trusting the card's own precomputed table.
import json
from math import gcd

CERT_PATH = "search/certs/meas_chi_m5_v1_20260811.json"
M5_WIN_CHK_PATH = "search/certs/m5_win_chk_v1_20260811.json"
HCEN_AB_PATH = "search/certs/hcen_ab_v1_20260811.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


def main():
    cert = json.load(open(CERT_PATH, encoding="utf-8"))
    m5win = json.load(open(M5_WIN_CHK_PATH, encoding="utf-8"))
    hcen = json.load(open(HCEN_AB_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/meas_chi_m5_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/meas_chi_m5_v1")

    # (A) cross-cert order consistency (THREE independent GAP runs)
    order = cert.get("order")
    if order != cert.get("order_expected") or not cert.get("order_ok"):
        fail(f"order/order_expected/order_ok inconsistency in this cert: {order}/{cert.get('order_expected')}/{cert.get('order_ok')}")
    else:
        ok(f"order={order} matches order_expected, order_ok=True")

    if order != m5win.get("order_of_B3_mod_M5"):
        fail(f"order={order} != m5_win_chk_v1's order_of_B3_mod_M5={m5win.get('order_of_B3_mod_M5')}")
    else:
        ok(f"order={order} matches m5_win_chk_v1_20260811.json (115ffeb) independently")

    hcen_order = hcen.get("m5_control", {}).get("order")
    if order != hcen_order:
        fail(f"order={order} != hcen_ab_v1's m5_control.order={hcen_order}")
    else:
        ok(f"order={order} matches hcen_ab_v1_20260811.json's m5_control.order independently "
           f"(THREE separate GAP runs across 3 scripts all agree: order=3240)")

    if order != 3240:
        fail(f"order={order}, expected 3240 = 2^3*3^4*5")
    factors_of_3240 = {2: 3, 3: 4, 5: 1}  # 2^3 * 3^4 * 5^1 = 8*81*5 = 3240
    if 8 * 81 * 5 != 3240:
        fail("internal arithmetic error: 8*81*5 != 3240")

    chief_factors = cert.get("chief_factors", [])

    # (B) characteristic sanity: elementary abelian factors' p must be in {2,3,5}
    bad_p = [cf for cf in chief_factors if cf["is_elementary_abelian"] and cf["p"] not in (2, 3, 5)]
    if bad_p:
        for b in bad_p:
            fail(f"chief factor {b['factor_index']}: p={b['p']} not in {{2,3,5}} (|G|=3240=2^3*3^4*5)")
    else:
        ok("all elementary-abelian chief-factor characteristics are in {2,3,5} "
           "(consistent with |G|=3240=2^3*3^4*5)")

    # dim vs w_size consistency
    dim_mismatches = []
    for cf in chief_factors:
        if cf["is_elementary_abelian"] and cf["dim"] is not None:
            if cf["p"] ** cf["dim"] != cf["w_size"]:
                dim_mismatches.append(cf)
    if dim_mismatches:
        for d in dim_mismatches:
            fail(f"chief factor {d['factor_index']}: p^dim = {d['p']}^{d['dim']} != w_size={d['w_size']}")
    else:
        ok("all elementary-abelian chief factors satisfy p^dim = w_size")

    # (C) product of chief factor sizes = |G|
    prod = 1
    for cf in chief_factors:
        prod *= cf["w_size"]
    if prod != order:
        fail(f"product of chief-factor w_size = {prod}, != order = {order}")
    else:
        ok(f"product of chief-factor sizes = {prod} = order (chief series sanity)")

    # (D) downstream boolean re-derivation
    dim1 = [cf for cf in chief_factors if cf["dim"] == 1]
    dim1_orders = [cf["ord_chi_w"] for cf in dim1]
    rederived_max = max(dim1_orders) if dim1_orders else 0
    rederived_all_div_2 = all((2 % x == 0) for x in dim1_orders) if dim1_orders else True
    rederived_any_5 = any((x % 5 == 0) for x in dim1_orders)

    ds = cert.get("dim1_summary", {})
    if rederived_max != ds.get("max_ord_dim1"):
        fail(f"max_ord_dim1 rederived={rederived_max} cert={ds.get('max_ord_dim1')}")
    else:
        ok(f"max_ord_dim1 = {rederived_max}")
    if rederived_all_div_2 != ds.get("all_dim1_divide_2"):
        fail(f"all_dim1_divide_2 rederived={rederived_all_div_2} cert={ds.get('all_dim1_divide_2')}")
    else:
        ok(f"all_dim1_divide_2 = {rederived_all_div_2}")
    if rederived_any_5 != ds.get("any_5_divides_ord"):
        fail(f"any_5_divides_ord rederived={rederived_any_5} cert={ds.get('any_5_divides_ord')}")
    else:
        ok(f"any_5_divides_ord = {rederived_any_5}")

    dimGe2 = [cf for cf in chief_factors if cf["is_elementary_abelian"] and cf["dim"] is not None and cf["dim"] >= 2]
    nonAbelian = [cf for cf in chief_factors if not cf["is_elementary_abelian"]]
    dimGe2With5 = [cf for cf in dimGe2 if cf["g_mod_cg_w"] % 5 == 0]

    if len(dimGe2) != cert.get("dimGe2_factors_count"):
        fail(f"dimGe2_factors_count rederived={len(dimGe2)} cert={cert.get('dimGe2_factors_count')}")
    else:
        ok(f"dimGe2_factors_count = {len(dimGe2)}")
    if len(nonAbelian) != cert.get("nonabelian_factors_count"):
        fail(f"nonabelian_factors_count rederived={len(nonAbelian)} cert={cert.get('nonabelian_factors_count')}")
    else:
        ok(f"nonabelian_factors_count = {len(nonAbelian)}")
    if len(dimGe2With5) != cert.get("dimGe2_with_5_in_g_mod_cg_w_count"):
        fail(f"dimGe2_with_5_in_g_mod_cg_w_count rederived={len(dimGe2With5)} "
             f"cert={cert.get('dimGe2_with_5_in_g_mod_cg_w_count')}")
    else:
        ok(f"dimGe2_with_5_in_g_mod_cg_w_count = {len(dimGe2With5)}")

    # (E) TWIST-GCD theorem-consistency check (independent arithmetic, not trusting the card's table)
    e = hcen.get("m5_control", {}).get("d")  # e=10, independently cross-checked elsewhere already
    theorem_violations = []
    for cf in dim1:
        p = cf["p"]
        bound = gcd(e, p - 1) if e is not None else None
        if bound is not None and cf["ord_chi_w"] is not None and bound % cf["ord_chi_w"] != 0:
            theorem_violations.append((cf["factor_index"], p, cf["ord_chi_w"], bound))
    if theorem_violations:
        for v in theorem_violations:
            fail(f"TWIST-GCD violation candidate: factor_index={v[0]} p={v[1]} ord_chi_w={v[2]} "
                 f"does not divide gcd(e={e},p-1)={v[3]}")
    else:
        ok(f"TWIST-GCD consistency: every dim=1 factor's ord_chi_w divides gcd(e={e}, p-1) "
           f"(independently recomputed, not read from the card's precomputed table)")

    print()
    print(f"raw summary: chief_factors={[(cf['p'],cf['dim'],cf['g_mod_cg_w'],cf['ord_chi_w']) for cf in chief_factors]}")
    print("DISCLOSED LIMITATION: the core GAP computation (ChiefSeries + action-image order per "
          "chief factor on the 3240-point permutation group) is NOT independently re-derived by "
          "this checker (see module docstring).")

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
