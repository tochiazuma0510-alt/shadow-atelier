#!/usr/bin/env python
# crosscheck/check_w691_scan_canary.py
# Independent checker for search/certs/w691_scan_canary_v1_20260812.json (W691-SCAN canary,
# 裁定823, docs/見立て_相2_v1_1.md §3).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT call GAP, does NOT import search/w691_scan_canary_v1.g.
#
# GL(2,7) is small enough (order 2016, entries mod 7) that this checker independently
# reconstructs the ENTIRE group in pure Python and re-derives every claim from scratch --
# a stronger form of crosscheck than most others in this session (which had to disclose GAP
# primitives as unverifiable). This is possible here specifically because of the canary's small
# size; it would NOT be feasible for the actual p=691-scale targets (which is exactly why this
# script covers only the canary).
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


def mat_pow_order(A):
    cur = A
    order = 1
    while cur != I2:
        cur = mat_mul(cur, A)
        order += 1
        if order > 100:
            raise ValueError("order search exceeded reasonable bound")
    return order


def gen_all_gl27():
    elts = []
    for a, b, c, d in product(range(P), repeat=4):
        M = ((a, b), (c, d))
        if mat_det(M) != 0:
            elts.append(M)
    return elts


def subgroup_order(gens, all_elts_set):
    """BFS closure under multiplication starting from gens (and I2), within all_elts_set."""
    frontier = {I2}
    for g in gens:
        frontier.add(g)
    closure = set(frontier)
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


CERT_PATH = "search/certs/w691_scan_canary_v1_20260812.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


def main():
    cert = json.load(open(CERT_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/w691_scan_canary_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/w691_scan_canary_v1")

    elts = gen_all_gl27()
    n = len(elts)
    if n != 2016:
        fail(f"|GL(2,7)| rederived = {n}, want 2016")
    else:
        ok(f"|GL(2,7)| = {n} rederived independently (pure Python enumeration)")
    if n != cert.get("group_order"):
        fail(f"group_order cert={cert.get('group_order')} rederived={n}")
    else:
        ok(f"group_order matches cert: {n}")

    elts_set = set(elts)
    orders = {e: mat_pow_order(e) for e in elts}
    ord2 = [e for e in elts if orders[e] == 2]
    ord3 = [e for e in elts if orders[e] == 3]

    if len(ord2) != cert["check1_23_generation"]["order2_element_count"]:
        fail(f"order2 count rederived={len(ord2)} cert={cert['check1_23_generation']['order2_element_count']}")
    else:
        ok(f"order-2 element count = {len(ord2)}")
    if len(ord3) != cert["check1_23_generation"]["order3_element_count"]:
        fail(f"order3 count rederived={len(ord3)} cert={cert['check1_23_generation']['order3_element_count']}")
    else:
        ok(f"order-3 element count = {len(ord3)}")

    # check1: (2,3)-generation, ALL pairs (full pure-Python re-derivation)
    gen_count_23 = 0
    at_least_one_23 = False
    for a in ord2:
        for b in ord3:
            if subgroup_order([a, b], elts_set) == n:
                gen_count_23 += 1
                at_least_one_23 = True

    pairs_checked_23 = len(ord2) * len(ord3)
    if pairs_checked_23 != cert["check1_23_generation"]["pairs_checked"]:
        fail(f"pairs_checked (2,3) rederived={pairs_checked_23} cert={cert['check1_23_generation']['pairs_checked']}")
    else:
        ok(f"pairs_checked (2,3)-gen = {pairs_checked_23}")
    if gen_count_23 != cert["check1_23_generation"]["generating_pairs_found"]:
        fail(f"generating_pairs_found (2,3) rederived={gen_count_23} "
             f"cert={cert['check1_23_generation']['generating_pairs_found']}")
    else:
        ok(f"generating_pairs_found (2,3)-gen = {gen_count_23} (independently re-derived, "
           f"full pure-Python BFS closure per pair)")
    if at_least_one_23 != cert["check1_23_generation"]["at_least_one_generates"]:
        fail(f"at_least_one_generates (2,3) rederived={at_least_one_23} "
             f"cert={cert['check1_23_generation']['at_least_one_generates']}")
    else:
        ok(f"at_least_one_generates (2,3)-gen = {at_least_one_23}")

    # check2: order-8 det=1 elements
    ord8_det1 = [e for e in elts if orders[e] == 8 and mat_det(e) == 1]
    if len(ord8_det1) != cert["check2_order8_det1"]["order8_det1_element_count"]:
        fail(f"order8_det1 count rederived={len(ord8_det1)} "
             f"cert={cert['check2_order8_det1']['order8_det1_element_count']}")
    else:
        ok(f"order-8 det=1 element count = {len(ord8_det1)}")
    exists8 = len(ord8_det1) > 0
    if exists8 != cert["check2_order8_det1"]["exists"]:
        fail(f"exists (order8 det1) rederived={exists8} cert={cert['check2_order8_det1']['exists']}")
    else:
        ok(f"order-8 det=1 element exists = {exists8}")

    # check3: braid-realization, ALL pairs (this is O(n^2)=~4M pairs -- feasible in Python but
    # slow; use a reasonably efficient double loop with early relation check before the
    # expensive subgroup-order computation, matching the search script's own approach)
    braid_total = 0
    gen_count_braid = 0
    for a in elts:
        for b in elts:
            ab_a = mat_mul(mat_mul(a, b), a)
            ba_b = mat_mul(mat_mul(b, a), b)
            if ab_a == ba_b:
                braid_total += 1
                if subgroup_order([a, b], elts_set) == n:
                    gen_count_braid += 1

    if braid_total != cert["check3_braid_realization"]["braid_pairs_total_found"]:
        fail(f"braid_pairs_total_found rederived={braid_total} "
             f"cert={cert['check3_braid_realization']['braid_pairs_total_found']}")
    else:
        ok(f"braid_pairs_total_found = {braid_total}")
    if gen_count_braid != cert["check3_braid_realization"]["generating_pairs_found"]:
        fail(f"braid generating_pairs_found rederived={gen_count_braid} "
             f"cert={cert['check3_braid_realization']['generating_pairs_found']}")
    else:
        ok(f"braid generating_pairs_found = {gen_count_braid} (independently re-derived)")
    at_least_one_braid = gen_count_braid > 0
    if at_least_one_braid != cert["check3_braid_realization"]["at_least_one_generates"]:
        fail(f"at_least_one_generates (braid) rederived={at_least_one_braid} "
             f"cert={cert['check3_braid_realization']['at_least_one_generates']}")
    else:
        ok(f"at_least_one_generates (braid) = {at_least_one_braid}")

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} mismatches)")
        return 1
    else:
        print("RESULT: PASS (cross-checked, not verified -- 検証は Lean 専有; NOTE: unlike "
              "most crosschecks this session, this one is a FULL independent re-derivation, "
              "not limited by GAP-primitive disclosure, thanks to GL(2,7)'s small size)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
