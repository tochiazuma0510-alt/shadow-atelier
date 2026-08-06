#!/usr/bin/env python
# crosscheck/check_sg_g4_g5.py
# Independent checker + "lane B" for search/certs/sg_g4_g5_orb_20260806.json
# (G4/G5 ORB analysis of the 36 g3_records windows, 裁定649).
#
# CROSSCHECK, NOT VERIFICATION: reads ONLY the cert JSON (no GAP call, no
# import of the G4 driver -- search/crosscheck separation preserved).
#
# SCOPE DISCLOSURE (honest, per this project's grading discipline): this
# script does NOT recompute Aut(Ghat) from first principles -- doing so in
# pure python for groups up to order 1944 would require reimplementing a
# nontrivial fraction of GAP's automorphism-group machinery, which is out
# of proportion for a cross-check pass. Instead it independently verifies
# the STRUCTURAL/COMBINATORIAL invariants that this project has already
# PROVEN as theorems (theorem_check_mirrorall_l3vacuous_v1.md SSF.10.1/
# F.10.2, reused verbatim, not re-derived here):
#   (a) regularity: |M| = num_orbits * |Aut(Ghat)|, and every orbit's
#       recorded size equals |Aut(Ghat)| (SSF.10.1: stabilizer of a
#       generating pair under Aut is always trivial -- a genuine
#       group-theoretic FACT this checker treats as a external theorem, not
#       something to re-derive).
#   (b) nu-involution consistency (SSF.10.2, PROVEN): nu_maps_to_orbit_index
#       must be a fixed-point-free involution on the NON-reflexible orbit
#       subset, and must fix every reflexible orbit -- and, crucially,
#       reflexible[i] must equal (nu_maps_to_orbit_index[i] == i) EXACTLY
#       (this is the theorem "軌道Oがreflexible <=> nu(O)=O" applied as a
#       cross-check of the GAP driver's own two INDEPENDENTLY computed
#       fields -- reflexible[] came from a direct Aut-search, nu_image[]
#       came from a separate orbit-membership lookup; if GAP's automorphism
#       search or its orbit bookkeeping had a bug, these two fields would
#       very likely disagree, and this check would catch it).
#   (c) G5 classification is independently RE-DERIVED from num_orbits/
#       num_reflexible/num_chiral_pairs alone (not trusted from the cert's
#       own classification string) and cross-checked against the cert.
#   (d) exotic pair count C(K,2)-t is independently recomputed.
# This is a genuine, language-independent, algorithm-independent structural
# audit -- it WOULD catch orbit-counting bugs, mislabeled reflexibility,
# broken involution bookkeeping, or arithmetic errors in the classification/
# exotic-pair-count step. It does NOT independently confirm that
# AutomorphismGroup(Ghat) itself is complete (that specific claim remains
# single-lane / GAP-internal, exactly as theorem_check_mirrorall's own
# 432/486 precedent already discloses -- "同一GAPプロセス内なのでcross-
# checkedが上限").
import json, sys
from math import comb

PATH = "search/certs/sg_g4_g5_orb_20260806.json"
INPUT_CERT_PATH = "search/certs/sg_band_sweep_20260806.json"


def main():
    fails = []
    def fail(msg):
        fails.append(msg); print("[FAIL]", msg)
    def ok(msg):
        print("[PASS]", msg)

    doc = json.load(open(PATH, encoding="utf-8"))

    if doc.get("schema") != "shadow-atelier/sg-g4-g5-orb/v1":
        fail("schema mismatch: " + str(doc.get("schema")))
    else:
        ok("schema = shadow-atelier/sg-g4-g5-orb/v1")

    # input cert binding
    ic = doc.get("input_cert", {})
    try:
        import hashlib
        actual_sha = hashlib.sha256(open(INPUT_CERT_PATH, "rb").read()).hexdigest()
        if ic.get("sha256") != actual_sha:
            fail(f"input_cert.sha256 = {ic.get('sha256')} but actual file hash = {actual_sha}")
        else:
            ok("input_cert.sha256 matches the actual sg_band_sweep cert on disk")
    except FileNotFoundError:
        fail(f"input cert {INPUT_CERT_PATH} not found for hash verification")

    windows_total = doc.get("windows_total")
    windows_processed = doc.get("windows_processed")
    handoff = doc.get("handoff_mismatches", [])
    if windows_total != 36:
        fail(f"windows_total = {windows_total}, expected 36 (the g3_records count from the SG sweep)")
    else:
        ok("windows_total = 36")
    if windows_processed + len(handoff) != windows_total:
        fail(f"windows_processed ({windows_processed}) + handoff_mismatches ({len(handoff)}) != windows_total ({windows_total})")
    else:
        ok("windows_processed + handoff_mismatches accounts for all windows_total")
    if len(handoff) != 0:
        fail(f"{len(handoff)} HANDOFF_MISMATCH windows present -- prereg SS7.2 item 2 requires investigation, not silent pass-through")

    g4 = doc.get("g4_orb_records", [])
    g5 = doc.get("g5_classification", [])
    if len(g4) != windows_processed or len(g5) != windows_processed:
        fail(f"g4_orb_records ({len(g4)}) / g5_classification ({len(g5)}) length mismatch with windows_processed ({windows_processed})")
    else:
        ok(f"g4_orb_records and g5_classification both have {windows_processed} entries")

    g4_by_key = {(r["order"], r["id"]): r for r in g4}
    g5_by_key = {(r["order"], r["id"]): r for r in g5}
    if set(g4_by_key) != set(g5_by_key):
        fail("g4_orb_records and g5_classification do not cover the same (order,id) window set")

    total_exotic_pairs = 0
    class_recount = {}

    for key, gr in g4_by_key.items():
        order, wid = key
        orbits = gr["orbits"]
        K = gr["num_orbits"]

        # (a) regularity, structural theorem SSF.10.1
        if len(orbits) != K:
            fail(f"({order},{wid}): num_orbits={K} but len(orbits)={len(orbits)}")
        aut_order = gr["aut_order"]
        sizes = [o["size"] for o in orbits]
        if any(s != aut_order for s in sizes):
            fail(f"({order},{wid}): not all orbit sizes equal aut_order ({aut_order}): sizes={sizes}")
        if sum(sizes) != gr["M_size"]:
            fail(f"({order},{wid}): sum(orbit sizes)={sum(sizes)} != M_size={gr['M_size']}")
        if gr["M_size"] != K * aut_order:
            fail(f"({order},{wid}): M_size={gr['M_size']} != num_orbits*aut_order={K*aut_order}")
        if gr.get("regular_ok") is not True:
            fail(f"({order},{wid}): cert's own regular_ok is not true")

        # (b) nu-involution consistency, structural theorem SSF.10.2
        refl = {o["orbit_index"]: o["reflexible"] for o in orbits}
        nu = {o["orbit_index"]: o["nu_maps_to_orbit_index"] for o in orbits}
        for idx in refl:
            is_refl = refl[idx]
            nu_fixed = (nu[idx] == idx)
            if is_refl != nu_fixed:
                fail(f"({order},{wid}) orbit {idx}: reflexible={is_refl} but nu-fixed={nu_fixed} -- SSF.10.2 equivalence violated")
            if not is_refl:
                j = nu[idx]
                if j is None or j not in nu:
                    fail(f"({order},{wid}) orbit {idx}: non-reflexible but nu_maps_to_orbit_index={j} is invalid")
                elif nu[j] != idx:
                    fail(f"({order},{wid}) orbit {idx} -> {j}: nu is not an involution (nu({j})={nu[j]}, expected {idx})")

        # rederive f, t
        f_count = sum(1 for v in refl.values() if v)
        t_count = (K - f_count) // 2
        if (K - f_count) % 2 != 0:
            fail(f"({order},{wid}): K-f_count is odd ({K}-{f_count}) -- non-reflexible orbits must pair up evenly")

        # (c) re-derive classification
        if K == 1 and f_count == 1:
            expected_class = "isolated_self_mirror_no_twin"
        elif K == 2 and f_count == 0 and t_count == 1:
            expected_class = "single_mirror_pair_non_exotic"
        elif K == 2 and f_count == 2:
            expected_class = "both_fixed_twin_exotic"
        else:
            expected_class = "multi_orbit_mixed_structure"

        g5r = g5_by_key[key]
        if g5r["num_reflexible"] != f_count:
            fail(f"({order},{wid}): cert num_reflexible={g5r['num_reflexible']} rederived={f_count}")
        if g5r["num_chiral_pairs"] != t_count:
            fail(f"({order},{wid}): cert num_chiral_pairs={g5r['num_chiral_pairs']} rederived={t_count}")
        if g5r["classification"] != expected_class:
            fail(f"({order},{wid}): cert classification={g5r['classification']!r} rederived={expected_class!r}")

        # (d) exotic pair count, fiber formula C(K,2)-t
        expected_exotic = comb(K, 2) - t_count
        if g5r["exotic_pair_count"] != expected_exotic:
            fail(f"({order},{wid}): cert exotic_pair_count={g5r['exotic_pair_count']} rederived={expected_exotic}")
        total_exotic_pairs += expected_exotic

        class_recount[expected_class] = class_recount.get(expected_class, 0) + 1

    cert_class_counts = doc.get("g5_classification_counts", {})
    if cert_class_counts != class_recount:
        fail(f"g5_classification_counts mismatch: cert={cert_class_counts} rederived={class_recount}")
    else:
        ok(f"g5_classification_counts rederived matches cert: {class_recount}")

    ok(f"total exotic pair count across all {windows_processed} windows (rederived) = {total_exotic_pairs}")

    # alerts: any both_fixed or multi_orbit windows must appear in alerts
    alerts = doc.get("g5_alerts_nonstandard_structure", [])
    alert_keys = {(a["order"], a["id"]) for a in alerts}
    expected_alert_keys = {key for key, gr in g5_by_key.items()
                            if gr["classification"] in ("both_fixed_twin_exotic",) or
                               (gr["classification"] == "multi_orbit_mixed_structure" and (gr["num_reflexible"] > 0 or gr["num_chiral_pairs"] > 1))}
    if alert_keys != expected_alert_keys:
        fail(f"g5_alerts_nonstandard_structure keys mismatch: cert={alert_keys} rederived={expected_alert_keys}")
    else:
        ok(f"g5_alerts_nonstandard_structure covers exactly the expected {len(expected_alert_keys)} non-standard windows")

    # highlight: print all mirror pairs and any non-standard windows plainly
    print()
    print("=== per-window classification summary ===")
    for key in sorted(g5_by_key):
        r = g5_by_key[key]
        print(f"  ({key[0]},{key[1]}): {r['classification']} (K={r['num_orbits']}, reflexible={r['num_reflexible']}, chiral_pairs={r['num_chiral_pairs']}, exotic_pairs={r['exotic_pair_count']})")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (cross-checked, NOT verified -- Aut(Ghat) completeness remains")
        print("single-lane/GAP-internal per this project's own established grading; this checker")
        print("independently confirms orbit-regularity + nu-involution consistency + classification arithmetic.")
        sys.exit(0)


if __name__ == "__main__":
    main()
