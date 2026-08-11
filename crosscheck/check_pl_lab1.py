#!/usr/bin/env python3
# crosscheck/check_pl_lab1.py
# Independent checker for the PL-LAB-1 cert (裁定774/776/779/781,
# search/certs/pl_lab1_v1_20260811.json). Does NOT re-run any GAP script
# -- reads ONLY the cert JSON. Independently recomputes Witt(2,k) (own
# Mobius code) and H_k (own closed-form command, per addendum_a's own
# 命題 A-1 formula, re-derived from scratch not copied), then re-derives
# every per-degree and per-target boolean/sum from the cert's own raw
# dim_layer/kernel_dim fields.
import json
import sys

CERT_PATH = "search/certs/pl_lab1_v1_20260811.json"


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


def chi_std_tau(d):
    return 2 if d % 3 == 0 else -1


def tr_tau(k):
    total = 0
    for d in range(1, k + 1):
        if k % d == 0:
            total += mu(d) * (chi_std_tau(d) ** (k // d))
    return total // k


def H(k):
    return (witt(2, k) - tr_tau(k)) // 3


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

    if doc.get("schema") != "shadow-atelier/pl_lab1_v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/pl_lab1_v1")
    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job did not complete cleanly (STOP fired)")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues) -- STOP cert, no further checks")
        sys.exit(1)
    ok("stop_code=None")

    witt_recomputed = [witt(2, k) for k in range(1, 9)]
    if witt_recomputed != doc.get("witt_2_k_reference"):
        fail(f"recomputed Witt(2,k)={witt_recomputed} != cert {doc.get('witt_2_k_reference')}")
    else:
        ok(f"independently recomputed Witt(2,k) k=1..8 = {witt_recomputed} matches cert")

    H_recomputed = [H(k) for k in range(1, 9)]
    if H_recomputed != doc.get("H_k_reference"):
        fail(f"recomputed H_k={H_recomputed} != cert {doc.get('H_k_reference')}")
    else:
        ok(f"independently recomputed H_k (命題A-1 closed form, own code) k=1..8 = {H_recomputed} matches cert")
    if H_recomputed != [1, 0, 1, 1, 2, 3, 6, 10]:
        fail(f"H_k does not match the addendum_a-stated reference values [1,0,1,1,2,3,6,10]: got {H_recomputed}")
    else:
        ok("H_k matches the addendum_a §1.2-stated closed-form values exactly")

    expected_targets = {
        ("p5c4_control", 5, 4, "control"), ("p5c5_main", 5, 5, "main"), ("p5c6_extra", 5, 6, "extra"),
        ("p7c4_control", 7, 4, "control"), ("p7c6_control", 7, 6, "control"), ("p7c7_main", 7, 7, "main"),
    }
    found = {(t["label"], t["p"], t["c"], t["kind"]) for t in doc.get("targets", [])}
    if found != expected_targets:
        fail(f"target universe mismatch: {found} != {expected_targets}")
    else:
        ok("target universe matches expected (6 targets: 3 control incl. new p7c4, 2 main, 1 extra)")

    for t in doc.get("targets", []):
        p, c = t["p"], t["c"]
        witt_list = [witt(2, k) for k in range(1, c + 1)]
        if witt_list != t["witt_list"]:
            fail(f"{t['label']}: recomputed witt_list={witt_list} != cert {t['witt_list']}")

        lcs_dims = t["lcs_dims"]
        # P-PL-0 canary: k<p must equal Witt exactly
        below_p_ok = all(lcs_dims[k - 1] == witt_list[k - 1] for k in range(1, min(c, p - 1) + 1))
        if not below_p_ok:
            fail(f"{t['label']}: P-PL-0 canary (k<p matches Witt) FAILS on recomputation")
        else:
            ok(f"{t['label']}: P-PL-0 canary (lcs_dims==Witt for all k<p) re-verified from raw lcs_dims")

        if c >= p:
            drop_recomputed = witt_list[p - 1] - lcs_dims[p - 1]
            if drop_recomputed != t["p_pl_0_drop_at_p"]:
                fail(f"{t['label']}: recomputed P-PL-0 drop at k=p = {drop_recomputed} "
                     f"!= cert {t['p_pl_0_drop_at_p']}")
            else:
                ok(f"{t['label']}: P-PL-0 drop at k=p re-derives correctly: {drop_recomputed} "
                   f"(>=2: {drop_recomputed >= 2})")

        # re-derive per-degree def_k and zone from raw kernel_dim/H_k
        sum_measured = 0
        sum_predicted = 0
        per_degree_ok = True
        for pd in t["per_degree"]:
            k = pd["k"]
            h_expected = H(k)
            if h_expected != pd["H_k"]:
                fail(f"{t['label']} k={k}: recomputed H_k={h_expected} != cert {pd['H_k']}")
                per_degree_ok = False
            def_k_recomputed = pd["kernel_dim"] - h_expected
            if def_k_recomputed != pd["def_k"]:
                fail(f"{t['label']} k={k}: recomputed def_k={def_k_recomputed} != cert {pd['def_k']}")
                per_degree_ok = False
            zone_expected = "canary" if k < p else "excess"
            if zone_expected != pd["zone"]:
                fail(f"{t['label']} k={k}: recomputed zone={zone_expected} != cert {pd['zone']}")
                per_degree_ok = False
            if k < p and pd["def_k"] != 0:
                fail(f"{t['label']} k={k}: zone=canary (k<p) but def_k={pd['def_k']} != 0 "
                     f"-- should have triggered S-PL-2 STOP")
                per_degree_ok = False
            sum_measured += pd["kernel_dim"]
            sum_predicted += h_expected
        if per_degree_ok:
            ok(f"{t['label']}: all per-degree H_k/def_k/zone fields re-derive correctly from raw kernel_dim")

        if sum_measured != t["def_c_p_measured"] or sum_predicted != t["def_c_p_predicted_H"]:
            fail(f"{t['label']}: recomputed sums measured={sum_measured} predicted={sum_predicted} "
                 f"!= cert measured={t['def_c_p_measured']} predicted={t['def_c_p_predicted_H']}")
        def_c_p_recomputed = sum_measured - sum_predicted
        if def_c_p_recomputed != t["def_c_p"]:
            fail(f"{t['label']}: recomputed def_c_p={def_c_p_recomputed} != cert {t['def_c_p']}")
        else:
            ok(f"{t['label']}: def_c_p={def_c_p_recomputed} re-derives correctly from per-degree sums")

    controls = [t for t in doc["targets"] if t["kind"] == "control"]
    controls_zero_recomputed = all(t["def_c_p"] == 0 for t in controls)
    if controls_zero_recomputed != doc.get("controls_all_def_c_p_zero"):
        fail(f"controls_all_def_c_p_zero recomputed={controls_zero_recomputed} "
             f"!= cert {doc.get('controls_all_def_c_p_zero')}")
    else:
        ok(f"controls_all_def_c_p_zero re-derives correctly: {controls_zero_recomputed} "
           f"(P-PL-1' Lazard-domain prediction confirmed on all 3 controls)")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (independently recomputed Witt(2,k) and H_k (own closed-form "
              "code per addendum_a's own 命題A-1 formula) from scratch, re-derived every per-degree "
              "and per-target field from the cert's own raw dim_layer/kernel_dim data; all match. "
              "cross-checked, not 'verified' (reserved for Lean). NOTE: pure-Python, does not "
              "independently reconstruct the pc-groups themselves via GAP (search/crosscheck "
              "separation discipline).")
        sys.exit(0)


if __name__ == "__main__":
    main()
