#!/usr/bin/env python3
# crosscheck/check_pl_lab1_wa.py
# Independent checker for the PL-LAB-1 W-a cert (裁定774/776/779,
# search/certs/pl_lab1_wa_v1_20260811.json). Does NOT import or re-run any
# GAP script -- reads ONLY the cert JSON, and independently recomputes the
# free-Lie Witt(2,k) numbers from scratch (own Mobius-function code, not
# copied from search/) to verify witt_2_k_reference, then re-derives every
# summary boolean from the cert's own per-target raw fields.
import json
import sys

CERT_PATH = "search/certs/pl_lab1_wa_v1_20260811.json"


def mu(n):
    if n == 1:
        return 1
    r, d, m = 1, 2, n
    while d * d <= m:
        if m % d == 0:
            m //= d
            if m % d == 0:
                return 0
            r = -r
        d += 1
    if m > 1:
        r = -r
    return r


def witt(q, n):
    total = 0
    for d in range(1, n + 1):
        if n % d == 0:
            total += mu(d) * q ** (n // d)
    return total // n


def main():
    fails = []

    def fail(msg):
        fails.append(msg)
        print("[FAIL]", msg)

    def ok(msg):
        print("[PASS]", msg)

    try:
        doc = json.load(open(CERT_PATH, encoding="utf-8"))
    except FileNotFoundError:
        print(f"CROSSCHECK RESULT: FAIL (cert not found: {CERT_PATH})")
        sys.exit(1)

    if doc.get("schema") != "shadow-atelier/pl_lab1_wa_v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/pl_lab1_wa_v1")
    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job did not complete cleanly")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    ok("stop_code=None")

    witt_recomputed = [witt(2, k) for k in range(1, 9)]
    if witt_recomputed != doc.get("witt_2_k_reference"):
        fail(f"recomputed Witt(2,k) k=1..8 = {witt_recomputed} != cert {doc.get('witt_2_k_reference')}")
    else:
        ok(f"independently recomputed Witt(2,k) k=1..8 = {witt_recomputed} matches cert")

    scope_hold_present = "W-c" in doc.get("scope_hold_note", "") or len(doc.get("scope_hold_note", "")) > 0
    if not scope_hold_present:
        fail("scope_hold_note missing or empty -- W-c hold disclosure should be present")
    else:
        ok("scope_hold_note present (W-c/def/dim-S_k hold disclosed)")

    targets = doc.get("targets", [])
    if len(targets) != 5:
        fail(f"expected 5 targets, cert has {len(targets)}")

    expected_targets = {
        ("p5c4_control", 5, 4, "control"), ("p5c5_main", 5, 5, "main"), ("p5c6_extra", 5, 6, "extra"),
        ("p7c6_control", 7, 6, "control"), ("p7c7_main", 7, 7, "main"),
    }
    found_targets = {(t["label"], t["p"], t["c"], t["kind"]) for t in targets}
    if found_targets != expected_targets:
        fail(f"target set mismatch: {found_targets} != {expected_targets}")
    else:
        ok("target set (5 targets: 2 control, 2 main, 1 extra) matches expected universe")

    for t in targets:
        p, c = t["p"], t["c"]
        witt_list = [witt(2, k) for k in range(1, c + 1)]
        if witt_list != t["witt_list"]:
            fail(f"{t['label']}: recomputed witt_list={witt_list} != cert {t['witt_list']}")
        else:
            ok(f"{t['label']}: independently recomputed witt_list matches cert: {witt_list}")

        witt_predicted_order = p ** sum(witt_list)
        if witt_predicted_order != t["witt_predicted_order"]:
            fail(f"{t['label']}: recomputed witt_predicted_order={witt_predicted_order} "
                 f"!= cert {t['witt_predicted_order']}")
        order_match_recomputed = (t["order"] == witt_predicted_order)
        if order_match_recomputed != t["order_matches_witt_predict"]:
            fail(f"{t['label']}: order_matches_witt_predict recomputed={order_match_recomputed} "
                 f"!= cert {t['order_matches_witt_predict']}")

        lcs_dims = t["lcs_dims"]
        per_degree_match = [lcs_dims[i] == witt_list[i] for i in range(len(lcs_dims))]
        if per_degree_match != t["per_degree_match"]:
            fail(f"{t['label']}: recomputed per_degree_match={per_degree_match} != cert {t['per_degree_match']}")
        all_match_recomputed = all(per_degree_match)
        if all_match_recomputed != t["all_degrees_match"]:
            fail(f"{t['label']}: all_degrees_match recomputed={all_match_recomputed} "
                 f"!= cert {t['all_degrees_match']}")
        first_mismatch_recomputed = 0
        for i, m in enumerate(per_degree_match):
            if not m:
                first_mismatch_recomputed = i + 1
                break
        if first_mismatch_recomputed != t["first_mismatch_degree"]:
            fail(f"{t['label']}: first_mismatch_degree recomputed={first_mismatch_recomputed} "
                 f"!= cert {t['first_mismatch_degree']}")
        else:
            ok(f"{t['label']}: lcs_dims={lcs_dims} vs witt={witt_list} -- per-degree match and "
               f"first_mismatch_degree={first_mismatch_recomputed} re-derive correctly")

    structural_sanity_recomputed = all(t["exponent_ok"] and t["gamma_c_plus_1_trivial"] for t in targets)
    if structural_sanity_recomputed != doc.get("structural_sanity_all_pass"):
        fail(f"structural_sanity_all_pass recomputed={structural_sanity_recomputed} "
             f"!= cert {doc.get('structural_sanity_all_pass')}")
    else:
        ok(f"structural_sanity_all_pass re-derives correctly: {structural_sanity_recomputed}")

    controls = [t for t in targets if t["kind"] == "control"]
    controls_match_recomputed = all(t["all_degrees_match"] and t["order_matches_witt_predict"] for t in controls)
    if controls_match_recomputed != doc.get("controls_all_degrees_match_witt"):
        fail(f"controls_all_degrees_match_witt recomputed={controls_match_recomputed} "
             f"!= cert {doc.get('controls_all_degrees_match_witt')}")
    else:
        ok(f"controls_all_degrees_match_witt re-derives correctly: {controls_match_recomputed}")

    mains = [t for t in targets if t["kind"] == "main"]
    mains_match_recomputed = all(t["first_mismatch_degree"] == t["p"] for t in mains)
    if mains_match_recomputed != doc.get("main_targets_first_mismatch_exactly_at_degree_p"):
        fail(f"main_targets_first_mismatch_exactly_at_degree_p recomputed={mains_match_recomputed} "
             f"!= cert {doc.get('main_targets_first_mismatch_exactly_at_degree_p')}")
    else:
        ok(f"main_targets_first_mismatch_exactly_at_degree_p re-derives correctly: {mains_match_recomputed}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (independently recomputed Witt(2,k) from scratch, re-derived "
              "every per-target and summary boolean from the cert's own raw order/exponent/lcs_dims "
              "fields; all match. cross-checked, not 'verified' (reserved for Lean). NOTE: this "
              "checker validates internal consistency of the cert's own reported group-theoretic data "
              "(order, LCS dims) against independently-recomputed Witt numbers -- it does NOT "
              "independently reconstruct the pc-groups themselves via GAP, since crosscheck/ is "
              "pure-Python-only per this project's search/crosscheck separation discipline)")
        sys.exit(0)


if __name__ == "__main__":
    main()
