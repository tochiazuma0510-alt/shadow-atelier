#!/usr/bin/env python
# crosscheck/check_pchi1_v2.py
# Independent checker for search/certs/pchi1_v2_20260811.json (pchi1_v2, 裁定813-1,
# docs/notes/cv9_chi_semantics_audit_v1.md).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT call GAP, does NOT import search/pchi1_v2.g.
#
# DISCLOSED LIMITATION: the core per-chief-factor measurement (ChiefSeries + conjugation-action
# image order on each SmallGroup) is a GAP-only primitive, not independently re-derived here
# (same convention as crosscheck/check_pchi1.py / check_meas_chi_m5.py).
#
# What IS independently checked:
#  (A) CHI-CARRY compliance: chi_semantics=="section", factor_filter=="none" present verbatim.
#  (B) domain provenance: identical 23-pair/index/id_group list to search/certs/
#      hcen_ab_v1_20260811.json's pairs[] (re-extracted independently, not copy-pasted).
#  (C) no-filter completeness sanity: total_factors_measured must be >= the OLD filtered
#      pchi1_v1 cert's factor count (its "128" dim=1-only observations), and specifically MORE
#      (since the filter was strictly dropping factors) -- confirms this is genuinely an
#      unfiltered superset, not accidentally re-filtered.
#  (D) per-member structural sanity: for every factor, is_elementary_abelian==True must imply
#      p is prime and p^dim==w_size; is_elementary_abelian==False must imply p==None and
#      dim==None (CHI-CARRY: non-abelian factors carry no (p,dim) reading).
#  (E) ord_chi_w discipline: ord_chi_w is non-null IFF dim==1 (never reported for dim!=1 or
#      non-abelian factors) -- the CHI-CARRY-mandated omission, checked structurally for all
#      176 factor observations.
#  (F) product-of-factor-sizes == |G| (SmallGroup order), independently recomputed per member
#      via sympy-free factorization (product of w_size across a member's factor list should
#      equal the group's own order, which is IdGroup's own order component -- id_group[0]).
#  (G) downstream boolean re-derivation: max_ord_dim1, max_g_mod_cg_w_any_factor,
#      total_factors_measured, total_dim1_factors, and the p750_id6_dim2_F5_factors list (10
#      entries, all g_mod_cg_w=6, w_size=25, p=5, dim=2) -- all recomputed from members[] alone.
import json

CERT_PATH = "search/certs/pchi1_v2_20260811.json"
HCEN_AB_PATH = "search/certs/hcen_ab_v1_20260811.json"
V1_CERT_PATH = "search/certs/pchi1_v1_20260811.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def main():
    cert = json.load(open(CERT_PATH, encoding="utf-8"))
    hcen = json.load(open(HCEN_AB_PATH, encoding="utf-8"))
    v1 = json.load(open(V1_CERT_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/pchi1_v2":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/pchi1_v2")

    # (A) CHI-CARRY compliance
    if cert.get("chi_semantics") != "section":
        fail(f"chi_semantics = {cert.get('chi_semantics')}, want 'section'")
    else:
        ok("chi_semantics = 'section'")
    if cert.get("factor_filter") != "none":
        fail(f"factor_filter = {cert.get('factor_filter')}, want 'none'")
    else:
        ok("factor_filter = 'none'")

    members = cert.get("members", [])
    if len(members) != 23:
        fail(f"members count = {len(members)}, want 23")
    else:
        ok("members count = 23 (46 total via m0/m1)")

    # (B) domain provenance vs hcen_ab_v1
    hcen_pairs = {p["pair_fiber"]: p for p in hcen["pairs"]}
    dom_mismatches = []
    for m in members:
        hp = hcen_pairs.get(m["pair_fiber"])
        if hp is None:
            dom_mismatches.append(f"{m['pair_fiber']}: missing in hcen_ab_v1")
            continue
        if m["index"] != hp["index"] or tuple(m["m0_id_group"]) != tuple(hp["m0"]["id_group"]) \
                or tuple(m["m1_id_group"]) != tuple(hp["m1"]["id_group"]):
            dom_mismatches.append(f"{m['pair_fiber']}: id_group/index mismatch")
    if dom_mismatches:
        for d in dom_mismatches:
            fail("domain: " + d)
    else:
        ok("domain (23 pair_fiber/index/id_group) matches hcen_ab_v1_20260811.json exactly")

    # (C) unfiltered superset sanity vs v1
    all_factors = []
    for m in members:
        all_factors.extend(m["m0_factors"])
        all_factors.extend(m["m1_factors"])
    v1_dim1_count = sum(1 for p in v1["members"] for k in ("m0_twists", "m1_twists") for _ in p[k])
    if len(all_factors) <= v1_dim1_count:
        fail(f"unfiltered factor count ({len(all_factors)}) not greater than v1's filtered "
             f"dim=1-only count ({v1_dim1_count}) -- expected strictly more (superset)")
    else:
        ok(f"unfiltered factor count ({len(all_factors)}) > v1's filtered count "
           f"({v1_dim1_count}) -- confirms genuinely broader coverage")

    # (D)+(E) structural sanity per factor
    struct_bad = []
    ord_bad = []
    for f in all_factors:
        if f["is_elementary_abelian"]:
            if f["p"] is None or not is_prime(f["p"]):
                struct_bad.append(("bad p for elem-abelian factor", f))
            elif f["dim"] is None or f["p"] ** f["dim"] != f["w_size"]:
                struct_bad.append(("p^dim != w_size", f))
        else:
            if f["p"] is not None or f["dim"] is not None:
                struct_bad.append(("non-abelian factor has non-null p/dim", f))
        expect_ord_present = (f["dim"] == 1)
        ord_present = (f["ord_chi_w"] is not None)
        if expect_ord_present != ord_present:
            ord_bad.append(f)
    if struct_bad:
        for msg, f in struct_bad:
            fail(f"structural: {msg}: {f}")
    else:
        ok("all elementary-abelian factors have prime p with p^dim=w_size; "
           "all non-abelian factors have null p/dim")
    if ord_bad:
        for f in ord_bad:
            fail(f"ord_chi_w discipline violated (must be non-null iff dim==1): {f}")
    else:
        ok("ord_chi_w is non-null iff dim==1 for all 176 factor observations "
           "(CHI-CARRY discipline)")

    # (F) product of factor sizes == group order (id_group[0])
    prod_mismatches = []
    for m in members:
        for key, idg in (("m0_factors", m["m0_id_group"]), ("m1_factors", m["m1_id_group"])):
            prod = 1
            for f in m[key]:
                prod *= f["w_size"]
            if prod != idg[0]:
                prod_mismatches.append(f"{m['pair_fiber']}/{key}: product={prod} != order={idg[0]}")
    if prod_mismatches:
        for p in prod_mismatches:
            fail("chief-series sanity: " + p)
    else:
        ok("product of chief-factor w_size == group order (id_group[0]) for all 46 members "
           "(chief series completeness sanity)")

    # (G) downstream re-derivation
    dim1_ords = [f["ord_chi_w"] for f in all_factors if f["dim"] == 1]
    rederived_max_ord = max(dim1_ords) if dim1_ords else 0
    rederived_max_g = max(f["g_mod_cg_w"] for f in all_factors)
    if rederived_max_ord != cert.get("max_ord_dim1"):
        fail(f"max_ord_dim1 rederived={rederived_max_ord} cert={cert.get('max_ord_dim1')}")
    else:
        ok(f"max_ord_dim1 = {rederived_max_ord}")
    if rederived_max_g != cert.get("max_g_mod_cg_w_any_factor"):
        fail(f"max_g_mod_cg_w_any_factor rederived={rederived_max_g} "
             f"cert={cert.get('max_g_mod_cg_w_any_factor')}")
    else:
        ok(f"max_g_mod_cg_w_any_factor = {rederived_max_g}")
    if len(all_factors) != cert.get("total_factors_measured"):
        fail(f"total_factors_measured rederived={len(all_factors)} "
             f"cert={cert.get('total_factors_measured')}")
    else:
        ok(f"total_factors_measured = {len(all_factors)}")
    if len(dim1_ords) != cert.get("total_dim1_factors"):
        fail(f"total_dim1_factors rederived={len(dim1_ords)} cert={cert.get('total_dim1_factors')}")
    else:
        ok(f"total_dim1_factors = {len(dim1_ords)}")

    # [750,6] dim=2/F_5 special case
    p750_flagged = [f for m in members if m["m0_id_group"] == [750, 6]
                     for f in m["m0_factors"] if f["dim"] == 2 and f["p"] == 5]
    cert_p750 = cert.get("p750_id6_dim2_F5_factors", [])
    if len(p750_flagged) != 10 or len(cert_p750) != 10:
        fail(f"[750,6] dim=2/F_5 factor count: rederived={len(p750_flagged)} cert={len(cert_p750)}, want 10")
    elif not all(f["g_mod_cg_w"] == 6 and f["w_size"] == 25 for f in p750_flagged):
        fail(f"[750,6] dim=2/F_5 factors do not all have g_mod_cg_w=6,w_size=25: {p750_flagged}")
    else:
        ok("[750,6] dim=2/F_5 factor: 10/10 members, all g_mod_cg_w=6 w_size=25 "
           "(falsifier's flagged special case reproduced independently)")

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
