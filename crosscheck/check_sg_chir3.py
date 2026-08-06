#!/usr/bin/env python
# crosscheck/check_sg_chir3.py
# Independent checker for search/certs/sg_chir3_20260806.json (CHIR-3,
# 裁定699). Reads ONLY the cert JSON (+ the already-committed CHIR-2 cert
# for the dim_H2 cross-check, both are read-only inputs, not recomputed).
import json, sys

PATH = "search/certs/sg_chir3_20260806.json"
CHIR2_PATH = "search/certs/sg_chir2_20260806.json"

def main():
    fails = []
    def fail(msg):
        fails.append(msg); print("[FAIL]", msg)
    def ok(msg):
        print("[PASS]", msg)

    doc = json.load(open(PATH, encoding="utf-8"))
    chir2 = json.load(open(CHIR2_PATH, encoding="utf-8"))
    chir2_by_key = {(r["order"], r["id"]): r for r in chir2["rows"]}

    if doc.get("schema") != "shadow-atelier/sg-chir3/v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/sg-chir3/v1")

    rows = doc.get("rows", [])
    if {(r["order"], r["id"]) for r in rows} != {(1944, 826), (1944, 921)}:
        fail(f"rows cover wrong windows: {[(r['order'],r['id']) for r in rows]}")
    else:
        ok("rows cover exactly the 2 layer-3 windows")

    for r in rows:
        if r["status"] != "OK":
            fail(f"({r['order']},{r['id']}): status={r['status']}, want OK")
            continue
        # dim_H2 cross-check against CHIR-2
        c2 = chir2_by_key.get((r["order"], r["id"]), {})
        rederived_match = (r.get("dim_H2_crosscheck") == c2.get("dim_H2"))
        if r.get("dim_H2_matches_chir2") != rederived_match:
            fail(f"({r['order']},{r['id']}): dim_H2_matches_chir2 cert={r.get('dim_H2_matches_chir2')} rederived={rederived_match}")
        if not rederived_match:
            fail(f"({r['order']},{r['id']}): dim_H2 cross-check with CHIR-2 FAILED: chir3={r.get('dim_H2_crosscheck')} chir2={c2.get('dim_H2')}")

        # arithmetic: dim_Z1 = dim_B1 + dim_H1
        if r.get("dim_B1") is not None and r.get("dim_H1") is not None:
            if r["dim_Z1"] != r["dim_B1"] + r["dim_H1"]:
                fail(f"({r['order']},{r['id']}): dim_Z1 != dim_B1+dim_H1: {r['dim_Z1']} != {r['dim_B1']}+{r['dim_H1']}")
        # image_dim = min(dim_Z1, 2)
        if r.get("dim_Z1") is not None:
            if r["image_dim"] != min(r["dim_Z1"], 2):
                fail(f"({r['order']},{r['id']}): image_dim != min(dim_Z1,2): {r['image_dim']} vs min({r['dim_Z1']},2)")
        # correction_possible_general = (image_dim == 2)
        if r.get("image_dim") is not None:
            expected = (r["image_dim"] == 2)
            if r["correction_possible_general"] != expected:
                fail(f"({r['order']},{r['id']}): correction_possible_general={r['correction_possible_general']} rederived={expected}")
        # dim_H1_ge1
        if r.get("dim_H1") is not None:
            expected_ge1 = (r["dim_H1"] >= 1)
            if r["dim_H1_ge1"] != expected_ge1:
                fail(f"({r['order']},{r['id']}): dim_H1_ge1={r['dim_H1_ge1']} rederived={expected_ge1}")

    ok_rows = [r for r in rows if r["status"] == "OK"]
    rederived_p5 = all(r.get("dim_H1_ge1") is True for r in ok_rows) if len(ok_rows) == 2 else None
    cert_p5 = doc.get("predictions", {}).get("P_CHIR_5_dim_H1_ge1_both", {})
    if cert_p5.get("holds") != rederived_p5:
        fail(f"P-CHIR-5: cert={cert_p5.get('holds')} rederived={rederived_p5}")
    else:
        ok(f"P-CHIR-5 (dim_H1>=1, both) rederived matches cert: {rederived_p5}")

    rederived_closure = all(r.get("correction_possible_general") is True for r in ok_rows) if len(ok_rows) == 2 else None
    cert_closure = doc.get("gap_g11_1_closure", {}).get("closed_general")
    if cert_closure != rederived_closure:
        fail(f"gap_g11_1_closure: cert={cert_closure} rederived={rederived_closure}")
    else:
        ok(f"GAP-G11-1 general closure rederived matches cert: {rederived_closure}")

    # step3 must be explicitly disclosed as skipped with a reason for both
    for r in ok_rows:
        if r.get("step3_skipped") is not True or not r.get("step3_skip_reason"):
            fail(f"({r['order']},{r['id']}): step3_skipped not properly disclosed")
    ok("step3 skip disclosed with reason for both windows")

    print()
    print("=== 2-row table ===")
    for r in rows:
        print(f"  ({r['order']},{r['id']}): status={r['status']} dim_H1={r.get('dim_H1')} "
              f"dim_H2_crosscheck={r.get('dim_H2_crosscheck')} image_dim={r.get('image_dim')} "
              f"correction_possible_general={r.get('correction_possible_general')}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
