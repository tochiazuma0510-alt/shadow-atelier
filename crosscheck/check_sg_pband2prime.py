#!/usr/bin/env python
# crosscheck/check_sg_pband2prime.py
# Independent checker for search/certs/sg_pband2prime_20260806.json
# (P-BAND-2' / SECT predicate test, 裁定679,
# theorem_check_mirrorall_l3vacuous_v1.md SSG.8.3).
#
# CROSSCHECK, NOT VERIFICATION: reads ONLY the cert JSON (no GAP call).
# Re-derives all_pass/matches_prediction from factors[] alone, re-derives
# the summary counts from rows[], and independently checks the structural
# claim (SSG.8.3: obstruction only possible on non-cyclic, i.e. d>=2,
# factors) against the actual per-factor data. Does NOT independently
# recompute Centralizer/IsConjugate in GL(d,p) itself (single-lane/
# GAP-internal for that specific claim, same disclosed caveat as the
# G4/G5 and P-BAND-2 passes).
import json, sys

PATH = "search/certs/sg_pband2prime_20260806.json"

def main():
    fails = []
    def fail(msg):
        fails.append(msg); print("[FAIL]", msg)
    def ok(msg):
        print("[PASS]", msg)

    doc = json.load(open(PATH, encoding="utf-8"))

    if doc.get("schema") != "shadow-atelier/sg-pband2prime/v1":
        fail("schema mismatch: " + str(doc.get("schema")))
    else:
        ok("schema = shadow-atelier/sg-pband2prime/v1")

    rows = doc.get("rows", [])
    if len(rows) != 36:
        fail(f"rows has {len(rows)} entries, want 36")
    else:
        ok("rows has 36 entries")
    if len(doc.get("handoff_mismatches", [])) != 0:
        fail("handoff_mismatches nonzero")
    else:
        ok("handoff_mismatches = 0")

    n_match = n_mismatch = 0
    refl_count = refl_allpass = 0
    chir_count = chir_broken = 0
    d_ge2_fail_count = 0
    d1_fail_count = 0

    for r in rows:
        is_chiral = (r["classification"] == "single_mirror_pair_non_exotic")
        if r["is_chiral"] != is_chiral:
            fail(f"({r['order']},{r['id']}): is_chiral mismatch")

        factors = r["factors"]
        rederived_all_pass = all(f["sect_holds"] for f in factors)
        if rederived_all_pass != r["all_pass"]:
            fail(f"({r['order']},{r['id']}): all_pass cert={r['all_pass']} rederived={rederived_all_pass}")

        # first_fail_index rederivation (1-based)
        ffi = None
        for idx, f in enumerate(factors, start=1):
            if not f["sect_holds"]:
                ffi = idx
                break
        if ffi != r["first_fail_index"]:
            fail(f"({r['order']},{r['id']}): first_fail_index cert={r['first_fail_index']} rederived={ffi}")

        predicted_all_pass = not is_chiral
        expected_match = (r["all_pass"] == predicted_all_pass)
        if r["matches_prediction"] != expected_match:
            fail(f"({r['order']},{r['id']}): matches_prediction cert={r['matches_prediction']} rederived={expected_match}")
        if expected_match:
            n_match += 1
        else:
            n_mismatch += 1

        if is_chiral:
            chir_count += 1
            if not r["all_pass"]:
                chir_broken += 1
        else:
            refl_count += 1
            if r["all_pass"]:
                refl_allpass += 1

        # structural check (SSG.8.3): any failing factor must have d>=2
        # (non-cyclic Aut(A)); d=1 factors can never fail per the theorem's
        # own argument (Aut(A) abelian for cyclic A -- centralizer is
        # everything, and mu(W)~mu(W)^-1 always for order-3 elements over
        # p in {2,3}, so SECT is forced true when d=1)
        for f in factors:
            if f["d"] is None:
                continue
            if not f["sect_holds"]:
                if f["d"] >= 2:
                    d_ge2_fail_count += 1
                else:
                    d1_fail_count += 1

    if d1_fail_count != 0:
        fail(f"{d1_fail_count} factor(s) with d=1 (cyclic) show sect_holds=false -- contradicts SSG.8.3's proof that d=1 forces SECT true (mu(W)~mu(W)^-1 always for p in {{2,3}})")
    else:
        ok("no d=1 (cyclic) factor ever fails SECT -- consistent with SSG.8.3's proof")
    ok(f"{d_ge2_fail_count} failing factor(s) found, all with d>=2 (non-cyclic Aut(A)), matching the theorem's own necessary condition for an obstruction")

    if refl_count != 31:
        fail(f"reflexible_count={refl_count}, expected 31")
    else:
        ok("reflexible_count = 31")
    if chir_count != 5:
        fail(f"chiral_count={chir_count}, expected 5")
    else:
        ok("chiral_count = 5")

    if refl_allpass != refl_count:
        fail(f"reflexible health check: only {refl_allpass}/{refl_count} all_pass -- implementation health check FAILED")
    else:
        ok(f"reflexible health check: {refl_allpass}/{refl_count} all_pass (implementation sound)")

    ps = doc.get("prediction_summary", {})
    if (ps.get("reflexible_count") != refl_count or ps.get("reflexible_all_pass_count") != refl_allpass or
        ps.get("chiral_count") != chir_count or ps.get("chiral_broken_count") != chir_broken or
        ps.get("total_matches") != n_match or ps.get("total_mismatches") != n_mismatch):
        fail(f"prediction_summary mismatch: cert={ps} rederived matches={n_match} mismatches={n_mismatch} "
             f"refl_allpass={refl_allpass} chir_broken={chir_broken}")
    else:
        ok(f"prediction_summary fully rederived matches cert")

    print()
    print("=== 36-row table (chief-factor detail) ===")
    print(f"{'order':>6} {'id':>7} {'classification':30} {'#factors':>9} {'all_pass':>9} {'first_fail':>11} {'match':6}")
    for r in sorted(rows, key=lambda r: (r["order"], r["id"])):
        print(f"{r['order']:>6} {r['id']:>7} {r['classification']:30} {r['num_chief_factors']:>9} "
              f"{str(r['all_pass']):>9} {str(r['first_fail_index']):>11} {str(r['matches_prediction']):6}")

    print()
    print("=== factor-level breakdown for the 5 chiral windows ===")
    for r in rows:
        if r["classification"] == "single_mirror_pair_non_exotic":
            types = [f"{f['p']}^{f['d']}" for f in r["factors"]]
            holds = [f["sect_holds"] for f in r["factors"]]
            print(f"  ({r['order']},{r['id']}): types={types} sect_holds={holds} all_pass={r['all_pass']}")

    print()
    print(f"REFLEXIBLE (health check): {refl_allpass}/{refl_count} all_pass")
    print(f"CHIRAL (real test): {chir_broken}/{chir_count} have >=1 failing factor")
    print(f"CHIRAL that pass everything (undetectable-by-local-invariants cases): {chir_count - chir_broken}/{chir_count}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (cert bookkeeping + structural (d=1 always holds) claim")
        print("cross-checked; Centralizer/IsConjugate in GL(d,p) itself remains single-lane/GAP-internal)")
        sys.exit(0)


if __name__ == "__main__":
    main()
