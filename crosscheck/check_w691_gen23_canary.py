#!/usr/bin/env python
# crosscheck/check_w691_gen23_canary.py
# Independent checker for search/certs/w691_gen23_canary_v1_20260812.json (裁定829).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT call GAP, does NOT import search/w691_gen23_canary_v1.g.
#
# GL(2,7) (order 2016) is small enough for a FULL independent pure-Python re-derivation (same
# situation as crosscheck/check_w691_scan_canary.py).
import json
from itertools import product

P = 7


def mat_mul(A, B, mod=P):
    return (
        ((A[0][0]*B[0][0] + A[0][1]*B[1][0]) % mod, (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % mod),
        ((A[1][0]*B[0][0] + A[1][1]*B[1][0]) % mod, (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % mod),
    )


def mat_det(A, mod=P):
    return (A[0][0]*A[1][1] - A[0][1]*A[1][0]) % mod


I2 = ((1, 0), (0, 1))
negI2 = ((P-1, 0), (0, P-1))


def mat_order(A):
    cur = A
    order = 1
    while cur != I2:
        cur = mat_mul(cur, A)
        order += 1
        if order > 100:
            raise ValueError("order search exceeded bound")
    return order


def gen_all_gl(p=P):
    elts = []
    for a, b, c, d in product(range(p), repeat=4):
        M = ((a, b), (c, d))
        if mat_det(M, p) != 0:
            elts.append(M)
    return elts


def mu_d(d, p=P):
    # find a generator of F_p^*, then take d-th roots (elements of order dividing d)
    def order_mod(x, p):
        o = 1
        cur = x % p
        while cur != 1:
            cur = (cur * x) % p
            o += 1
        return o
    gen = None
    for cand in range(2, p):
        if order_mod(cand, p) == p - 1:
            gen = cand
            break
    step = (p - 1) // d
    return set(pow(gen, i * step, p) for i in range(d))


def subgroup_order(gens, universe_set):
    ident = I2
    closure = {ident}
    for g in gens:
        closure.add(g)
    changed = True
    while changed:
        changed = False
        new_elts = set()
        for x in closure:
            for g in gens:
                y = mat_mul(x, g)
                if y not in closure:
                    new_elts.add(y)
        if new_elts:
            closure |= new_elts
            changed = True
    return len(closure)


CERT_PATH = "search/certs/w691_gen23_canary_v1_20260812.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


def main():
    cert = json.load(open(CERT_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/w691_gen23_canary_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/w691_gen23_canary_v1")

    all_elts = gen_all_gl()
    if len(all_elts) != 2016:
        fail(f"|GL(2,7)| rederived = {len(all_elts)}, want 2016")
    else:
        ok(f"|GL(2,7)| = {len(all_elts)} rederived independently")

    orders = {e: mat_order(e) for e in all_elts}

    cert_canary = {r["d"]: r for r in cert["canary_4point"]}
    all_agree_rederived = True
    for d in [1, 2, 3, 6]:
        mu = mu_d(d)
        hd = [e for e in all_elts if mat_det(e) in mu]
        hd_set = set(hd)
        hd_order = len(hd)
        cert_r = cert_canary.get(d)
        if cert_r is None:
            fail(f"d={d}: missing from cert")
            continue
        if hd_order != cert_r["hd_order"]:
            fail(f"d={d}: hd_order rederived={hd_order} cert={cert_r['hd_order']}")
        else:
            ok(f"d={d}: |H_d| = {hd_order}")

        ord2 = [e for e in hd if orders[e] == 2]
        ord3 = [e for e in hd if orders[e] == 3]
        if len(ord2) != cert_r["order2_count"] or len(ord3) != cert_r["order3_count"]:
            fail(f"d={d}: order2/order3 counts rederived=({len(ord2)},{len(ord3)}) "
                 f"cert=({cert_r['order2_count']},{cert_r['order3_count']})")
        else:
            ok(f"d={d}: order2_count={len(ord2)} order3_count={len(ord3)}")

        gen_count = 0
        generates = False
        for a in ord2:
            for b in ord3:
                if subgroup_order([a, b], hd_set) == hd_order:
                    gen_count += 1
                    generates = True

        if gen_count != cert_r["generating_pairs_found"]:
            fail(f"d={d}: generating_pairs_found rederived={gen_count} "
                 f"cert={cert_r['generating_pairs_found']}")
        else:
            ok(f"d={d}: generating_pairs_found = {gen_count}")
        if generates != cert_r["generates"]:
            fail(f"d={d}: generates rederived={generates} cert={cert_r['generates']}")
        else:
            ok(f"d={d}: generates = {generates}")

        expected_gen23_det = (generates == (d % 2 == 0))
        if expected_gen23_det != cert_r["agrees_with_GEN23_DET_prediction"]:
            fail(f"d={d}: agrees_with_GEN23_DET_prediction rederived={expected_gen23_det} "
                 f"cert={cert_r['agrees_with_GEN23_DET_prediction']}")
        else:
            ok(f"d={d}: agrees_with_GEN23_DET_prediction = {expected_gen23_det}")
        if not expected_gen23_det:
            all_agree_rederived = False

    if all_agree_rederived != cert.get("all_canary_points_agree_with_GEN23_DET"):
        fail(f"all_canary_points_agree rederived={all_agree_rederived} "
             f"cert={cert.get('all_canary_points_agree_with_GEN23_DET')}")
    else:
        ok(f"all_canary_points_agree_with_GEN23_DET = {all_agree_rederived}")

    # ---- z-check on ALL generating braid pairs of GL(2,7) ----
    all_set = set(all_elts)
    total_gen_braid = 0
    all_z_I = True
    any_z_negI = False
    for a in all_elts:
        for b in all_elts:
            aba = mat_mul(mat_mul(a, b), a)
            bab = mat_mul(mat_mul(b, a), b)
            if aba == bab:
                if subgroup_order([a, b], all_set) == 2016:
                    total_gen_braid += 1
                    z = mat_mul(aba, aba)
                    if z != I2:
                        all_z_I = False
                    if z == negI2:
                        any_z_negI = True

    zc = cert["z_check"]
    if total_gen_braid != zc["total_generating_braid_pairs"]:
        fail(f"total_generating_braid_pairs rederived={total_gen_braid} "
             f"cert={zc['total_generating_braid_pairs']}")
    else:
        ok(f"total_generating_braid_pairs = {total_gen_braid}")
    if all_z_I != zc["all_z_equal_I"]:
        fail(f"all_z_equal_I rederived={all_z_I} cert={zc['all_z_equal_I']}")
    else:
        ok(f"all_z_equal_I = {all_z_I} (fully independently re-derived over all "
           f"{total_gen_braid} generating braid pairs)")
    if any_z_negI != zc["any_z_equal_negI"]:
        fail(f"any_z_equal_negI rederived={any_z_negI} cert={zc['any_z_equal_negI']}")
    else:
        ok(f"any_z_equal_negI = {any_z_negI}")

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} mismatches)")
        return 1
    else:
        print("RESULT: PASS (cross-checked, not verified -- 検証は Lean 専有; FULL independent "
              "re-derivation, GL(2,7)'s small size permits no GAP-primitive disclosure needed)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
