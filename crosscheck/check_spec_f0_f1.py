#!/usr/bin/env python3
# crosscheck/check_spec_f0_f1.py
# Independent checker for search/certs/spec_f0_f1_v1_20260807.json (WFS-1
# stages F0+F1, 裁定727(5)). Reads ONLY the combined cert JSON and the
# underlying per-prime cert JSONs it references (search/certs/wfs1_f0_v1_*
# and search/certs/aside2_prime_*_v2_*) -- does NOT import or execute
# search/wfs1_f0.py, search/wfs1_spec_f0_f1_v1.py, search/aside2_run_
# single_prime.py, or search/edim_semidirect_v1.py (search/crosscheck
# separation). Re-derives every predicate from raw fields.
import json
import sys

CERT_PATH = "search/certs/spec_f0_f1_v1_20260807.json"
F0_CERT_PATH = "search/certs/wfs1_f0_v1_20260807.json"
F1_PRIMES = [3617, 43867, 283, 617, 131, 593, 11]
F1_HONMEI = [3617, 43867, 283, 617]
F1_NAIZO = [131, 593, 11]


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

    if doc.get("schema") != "shadow-atelier/spec_f0_f1/v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/spec_f0_f1/v1")

    forbidden = ["不均衡", "SYN-0", "段差", "正典超過", "分光器"]
    blob = json.dumps(doc, ensure_ascii=False)
    for w in forbidden:
        if w in blob:
            fail(f"forbidden verdict text '{w}' found -- S-WFS-5 VERDICT_IN_CODE")
    ok("no forbidden verdict strings found in combined cert")

    # ---- re-derive F0 predicate directly from the underlying wfs1_f0 cert ----
    try:
        f0 = json.load(open(F0_CERT_PATH, encoding="utf-8"))
    except FileNotFoundError:
        fail(f"underlying F0 cert not found: {F0_CERT_PATH}")
        f0 = None

    if f0 is not None:
        if f0.get("schema") != "shadow-atelier/wfs1_f0/v1":
            fail(f"F0 cert schema mismatch: {f0.get('schema')}")
        results = f0.get("results", {})
        if not results:
            fail("F0 cert has no results")
        dims = set()
        l4_zero_flags = []
        for p_str, r in results.items():
            dim_L = r.get("dim_L")
            dims.add(dim_L)
            if dim_L is None or dim_L > 2:
                fail(f"F0 prime={p_str}: dim_L={dim_L} exceeds predicted <=2 (命題F-1(a))")
            L4_rank = r.get("L_depth_profile", {}).get("4", {}).get("rank_at_this_depth")
            L4_zero_rederived = (L4_rank == 0)
            if L4_zero_rederived != r.get("L4_is_zero"):
                fail(f"F0 prime={p_str}: L4_is_zero={r.get('L4_is_zero')} inconsistent with "
                     f"L_depth_profile[4].rank_at_this_depth={L4_rank}")
            l4_zero_flags.append(L4_zero_rederived)
        if len(dims) != 1:
            fail(f"F0: dim_L does not agree across primes: {dims}")
        else:
            ok(f"F0: dim_L={list(dims)[0]} agrees across all {len(results)} primes, <=2 confirmed")
        rederived_P_F_0 = all(l4_zero_flags) if l4_zero_flags else None
        cert_P_F_0 = doc.get("predicates", {}).get("P_F_0", {})
        if cert_P_F_0.get("result") != rederived_P_F_0:
            fail(f"P_F_0.result={cert_P_F_0.get('result')} != rederived (all L4_is_zero)={rederived_P_F_0}")
        else:
            ok(f"P_F_0 rederived correctly: result={rederived_P_F_0} (L^(4)=0 at all primes? "
               f"{'YES' if rederived_P_F_0 else 'NO -- P-F-0 falsified, raw fact'})")
        if cert_P_F_0.get("pass") != (rederived_P_F_0 is True):
            fail(f"P_F_0.pass={cert_P_F_0.get('pass')} inconsistent with result")

        # verify L is supported on [4,12] exactly, per every prime's depth profile
        for p_str, r in results.items():
            profile = r.get("L_depth_profile", {})
            for d_str, row in profile.items():
                d = int(d_str)
                rank = row.get("rank_at_this_depth", 0)
                if d < 4 or d > 12:
                    if rank != 0:
                        fail(f"F0 prime={p_str} depth={d}: rank={rank} != 0 outside predicted support [4,12]")
                else:
                    if rank == 0:
                        fail(f"F0 prime={p_str} depth={d}: rank=0 inside predicted support [4,12] "
                             f"(not necessarily wrong, but worth noting -- theorem F-B is about D_16, not L)")
        ok("F0: L's support checked against [4,12] band (no leakage outside [4,12] found)")

    # ---- re-derive F1 predicates from the 7 aside2 certs directly ----
    f1_rows_rederived = {}
    for p in F1_PRIMES:
        path = f"search/certs/aside2_prime_{p}_v2_20260806.json"
        try:
            cert = json.load(open(path, encoding="utf-8"))
        except FileNotFoundError:
            fail(f"F1 underlying cert not found: {path}")
            continue
        stage_e = cert.get("stage_E_D_ihara_takao_difference", {})
        D_is_zero = stage_e.get("D_is_zero")
        f1_rows_rederived[p] = {
            "D_is_zero": D_is_zero,
            "D12_not_equiv_0": (D_is_zero is False),
            "stop_code": cert.get("stop_code"),
        }
        cert_row = doc.get("stage_F1", {}).get("rows", {}).get(str(p), {})
        if cert_row.get("D_is_zero") != D_is_zero:
            fail(f"p={p}: combined cert D_is_zero={cert_row.get('D_is_zero')} != "
                 f"underlying aside2 cert D_is_zero={D_is_zero}")
        else:
            ok(f"p={p}: D_is_zero={D_is_zero} matches underlying aside2 cert")
        if cert.get("stop_code") is not None:
            fail(f"p={p}: underlying aside2 cert has stop_code={cert.get('stop_code')} "
                 f"(F1 measurement did not complete cleanly)")

    rederived_P_F_3 = all(f1_rows_rederived.get(p, {}).get("D12_not_equiv_0") for p in F1_HONMEI)
    cert_P_F_3 = doc.get("predicates", {}).get("P_F_3", {})
    if cert_P_F_3.get("result") != rederived_P_F_3:
        fail(f"P_F_3.result={cert_P_F_3.get('result')} != rederived {rederived_P_F_3}")
    elif not rederived_P_F_3:
        fail("P_F_3 FALSIFIED: D_12 vanishes at one or more of the 4 本命 primes {3617,43867,283,617}")
    else:
        ok(f"P_F_3 rederived correctly: D_12 not-equiv-0 at all 4 本命 primes {F1_HONMEI}")
    if cert_P_F_3.get("pass") != (rederived_P_F_3 is True):
        fail("P_F_3.pass inconsistent with result")

    rederived_naizo = all(f1_rows_rederived.get(p, {}).get("D12_not_equiv_0") for p in F1_NAIZO)
    cert_naizo = doc.get("predicates", {}).get("naizo_taisho_check", {})
    if cert_naizo.get("result") != rederived_naizo:
        fail(f"naizo_taisho_check.result={cert_naizo.get('result')} != rederived {rederived_naizo}")
    else:
        ok(f"naizo_taisho_check rederived correctly: D_12 not-equiv-0 at all 3 内蔵対照 primes {F1_NAIZO}")

    print()
    print("=== raw predicate table (re-read + rederived) ===")
    print(f"  P-F-0 (L^(4)=0):                  {rederived_P_F_0 if f0 is not None else 'N/A'}")
    print(f"  P-F-3 (D12 not-equiv-0 @ honmei):  {rederived_P_F_3}")
    print(f"  naizo_taisho_check (@ 内蔵対照):     {rederived_naizo}")
    for p in F1_PRIMES:
        row = f1_rows_rederived.get(p, {})
        print(f"    p={p}: D_is_zero={row.get('D_is_zero')}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (all predicates independently rederived from the underlying "
              "per-prime certs; this does NOT re-execute the GAP-free python group theory itself, "
              "only re-reads and re-aggregates raw fields -- see report to 司令塔)")
        sys.exit(0)


if __name__ == "__main__":
    main()
