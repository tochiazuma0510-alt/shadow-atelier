#!/usr/bin/env python
# crosscheck/check_sg_chir2.py
# Independent checker for search/certs/sg_chir2_20260806.json (CHIR-2,
# 裁定696, theorem_check_mirrorall_l3vacuous_v1.md SSG.11.3).
#
# CROSSCHECK, NOT VERIFICATION: reads ONLY the cert JSON (no GAP call).
# Re-derives the primary/secondary predictions and canaries from rows[]
# alone.
import json, sys

PATH = "search/certs/sg_chir2_20260806.json"
LAYER3 = {(1944, 826), (1944, 921)}
LAYER2 = {(1296, 2889), (1296, 3487), (1728, 31096)}

def main():
    fails = []
    def fail(msg):
        fails.append(msg); print("[FAIL]", msg)
    def ok(msg):
        print("[PASS]", msg)

    doc = json.load(open(PATH, encoding="utf-8"))

    if doc.get("schema") != "shadow-atelier/sg-chir2/v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/sg-chir2/v1")

    rows = doc.get("rows", [])
    keys = {(r["order"], r["id"]) for r in rows}
    if keys != (LAYER3 | LAYER2):
        fail(f"rows cover {keys}, expected {LAYER3 | LAYER2}")
    else:
        ok("rows cover exactly the 5 target windows (2 layer-3 + 3 layer-2)")

    ok_rows = [r for r in rows if r["status"] == "OK"]
    if doc.get("windows_ok") != len(ok_rows):
        fail(f"windows_ok cert={doc.get('windows_ok')} rederived={len(ok_rows)}")
    else:
        ok(f"windows_ok = {len(ok_rows)}")

    layer3_rows = [r for r in ok_rows if (r["order"], r["id"]) in LAYER3]
    layer2_rows = [r for r in ok_rows if (r["order"], r["id"]) in LAYER2]
    if len(layer3_rows) != 2:
        fail(f"layer3 OK rows = {len(layer3_rows)}, want 2")
    if len(layer2_rows) != 3:
        fail(f"layer2 OK rows = {len(layer2_rows)}, want 3")

    # primary prediction: dim_H2 >= 2 for both layer-3
    rederived_p1 = all(r.get("dim_H2_ge2") is True for r in layer3_rows) if len(layer3_rows) == 2 else None
    cert_p1 = doc.get("predictions", {}).get("primary_dim_H2_ge2_both_layer3", {})
    if cert_p1.get("holds") != rederived_p1:
        fail(f"primary prediction: cert={cert_p1.get('holds')} rederived={rederived_p1}")
    else:
        ok(f"primary prediction (dim_H2>=2, both layer-3) rederived matches cert: {rederived_p1}")
    for r in layer3_rows:
        if not isinstance(r.get("dim_H2"), int) or r["dim_H2"] < 0:
            fail(f"({r['order']},{r['id']}): dim_H2 missing/invalid: {r.get('dim_H2')}")
        elif r["dim_H2"] < 2:
            fail(f"({r['order']},{r['id']}): dim_H2={r['dim_H2']} < 2 -- FRAT-CHIR falsification, must be reported prominently")

    # secondary: eigenvector_lift_exists == False for both layer-3
    rederived_p2 = all(r.get("eigenvector_lift_exists") is False for r in layer3_rows) if len(layer3_rows) == 2 else None
    cert_p2 = doc.get("predictions", {}).get("secondary_eigenvector_lift_false_both_layer3_FRAT_CHIR", {})
    if cert_p2.get("holds") != rederived_p2:
        fail(f"secondary prediction: cert={cert_p2.get('holds')} rederived={rederived_p2}")
    else:
        ok(f"secondary prediction (eigenvector_lift=False, both layer-3) rederived matches cert: {rederived_p2}")

    # canary a: nonsplit, layer-3 only
    rederived_ca = all(r.get("canary_a_nonsplit") is True for r in layer3_rows) if len(layer3_rows) == 2 else None
    cert_ca = doc.get("canaries", {}).get("a_nonsplit_layer3", {})
    if cert_ca.get("holds_both") != rederived_ca:
        fail(f"canary a: cert={cert_ca.get('holds_both')} rederived={rederived_ca}")
    else:
        ok(f"canary a (NONSPLIT, layer-3) rederived matches cert: {rederived_ca}")

    # canary b: arithmetic, ALL windows: kappa*R_order == order
    for r in ok_rows:
        if r["kappa"] * r["R_order"] != r["order"]:
            fail(f"({r['order']},{r['id']}): canary b arithmetic fails: kappa*R_order={r['kappa']*r['R_order']} != order={r['order']}")
    ok("canary b (kappa * R_order == |Ghat|) holds for all OK rows")

    # chi checks for module_framework_applies rows with module_dim==1
    for r in ok_rows:
        if r.get("module_framework_applies") and r.get("module_dim") == 1:
            if r.get("chi_W_is_trivial_as_predicted") is not True:
                fail(f"({r['order']},{r['id']}): chi(W) not trivial -- contradicts Syl_3(R)<=ker(chi) argument")
            if r.get("chi_nontrivial") is not True:
                fail(f"({r['order']},{r['id']}): chi is trivial overall -- contradicts non-central X")

    print()
    print("=== 5-row table ===")
    print(f"{'order':>6} {'id':>7} {'layer':>5} {'kappa':>6} {'R_order':>8} {'X_abelian':>10} {'dim_H2':>7} {'eigvec_lift':>12}")
    for r in sorted(rows, key=lambda r: (r["layer"], r["order"], r["id"])):
        dim_h2 = r.get("dim_H2", "-")
        eig = r.get("eigenvector_lift_exists", "-")
        print(f"{r['order']:>6} {r['id']:>7} {r['layer']:>5} {r['kappa']:>6} {r['R_order']:>8} {str(r['X_abelian']):>10} {str(dim_h2):>7} {str(eig):>12}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
