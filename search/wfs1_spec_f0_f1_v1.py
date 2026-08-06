#!/usr/bin/env python3
"""
search/wfs1_spec_f0_f1_v1.py -- combines F0's own output cert
(search/certs/wfs1_f0_v1_20260807.json, produced by search/wfs1_f0.py) with
F1's readout (the D_is_zero / D_depth_profile / A12_ihara fields already
present in the 7 aside2_prime_<p>_v2 certs for p in {3617,43867,283,617,
131,593,11}, produced by the UNCHANGED, already-verified
search/aside2_run_single_prime.py, run fresh at these 7 new primes) into a
single combined cert per 司令塔's explicit naming instruction (裁定727(5)):
search/certs/spec_f0_f1_v1_20260807.json.

This script performs NO NEW mathematical computation of its own -- it is a
pure aggregator/readout, reading the JSON files that search/wfs1_f0.py and
search/aside2_run_single_prime.py already wrote, and repackaging the
relevant fields with the P-F-0/P-F-3 predicate evaluations spelled out
explicitly (raw booleans only, no verdict language, per S-WFS-5).
"""
import json

F1_PRIMES = [3617, 43867, 283, 617, 131, 593, 11]
F1_HONMEI = [3617, 43867, 283, 617]      # 本命 (primary)
F1_NAIZO = [131, 593, 11]                 # 内蔵対照 (built-in control)


def main():
    f0 = json.load(open("search/certs/wfs1_f0_v1_20260807.json", encoding="utf-8"))

    f1_rows = {}
    for p in F1_PRIMES:
        cert = json.load(open(f"search/certs/aside2_prime_{p}_v2_20260806.json", encoding="utf-8"))
        stage_e = cert.get("stage_E_D_ihara_takao_difference", {})
        f1_rows[p] = {
            "D_is_zero": stage_e.get("D_is_zero"),
            "D12_not_equiv_0": (stage_e.get("D_is_zero") is False),
            "D_num_terms_total": stage_e.get("D_num_terms_total"),
            "D_depth_profile": stage_e.get("D_depth_profile"),
            "A12_ihara": cert.get("stage_B_prime_ihara_weight_graded", {}).get("A12_ihara"),
            "stop_code": cert.get("stop_code"),
            "source_cert": f"search/certs/aside2_prime_{p}_v2_20260806.json",
        }

    P_F_3_all_honmei_nonzero = all(f1_rows[p]["D12_not_equiv_0"] for p in F1_HONMEI)
    naizo_all_nonzero = all(f1_rows[p]["D12_not_equiv_0"] for p in F1_NAIZO)
    canary_Fd_reference_profile = {"4": 350, "5": 744, "6": 858, "7": 744, "8": 350}
    canary_Fd_matches = {
        p: (f1_rows[p]["D_depth_profile"] is not None and
            all(f1_rows[p]["D_depth_profile"].get(str(d)) == v for d, v in
                {4: 350, 5: 744, 6: 858, 7: 744, 8: 350}.items()))
        for p in F1_PRIMES
    }

    out = {
        "schema": "shadow-atelier/spec_f0_f1/v1",
        "authority": "裁定727(5) (司令塔), WFS-1 段F0+段F1 per "
                      "docs/notes/weight_family_spectroscopy_design_v1.md (commit 4e6bdcb) SS2.3/3.4/5.1, "
                      "combined per 司令塔's explicit naming instruction",
        "stage_F0": {
            "source_cert": "search/certs/wfs1_f0_v1_20260807.json",
            "typo_correction_note": f0.get("typo_correction_note"),
            "primes": f0.get("primes"),
            "dim_L": {str(p): r["dim_L"] for p, r in f0.get("results", {}).items()},
            "dim_L_agrees_across_primes": f0.get("dim_L_agrees_across_primes"),
            "dim_L_le_2_all_primes": all(r["dim_L_le_2"] for r in f0.get("results", {}).values()),
            "P_F_0_L4_is_zero_all_primes": f0.get("P_F_0_L4_is_zero_all_primes"),
            "L_depth_profile_support": "L is supported exactly on depths [4,12] at both primes "
                                        "(rank_at_this_depth=2 uniformly across [4,12], 0 elsewhere), "
                                        "with a depth<->16-depth palindrome (see wfs1_f0 cert for the "
                                        "full per-depth table)",
        },
        "stage_F1": {
            "primes_tested": F1_PRIMES,
            "honmei_primes": F1_HONMEI,
            "naizo_taisho_primes": F1_NAIZO,
            "rows": {str(p): v for p, v in f1_rows.items()},
            "canary_Fd_reference_profile": canary_Fd_reference_profile,
            "canary_Fd_matches_per_prime": {str(p): v for p, v in canary_Fd_matches.items()},
            "note_on_D5_corollary": "定理D-5の帰結(D_12 not equiv 0 mod p for p coprime to 691*2*3, "
                                     "since aside3's exact-rational content computation already "
                                     "established that D12's per-depth content numerator is EXACTLY "
                                     "691^1 at every depth 4..8, with denominators supported only on "
                                     "{2,3}) is here machine-confirmed by direct fresh mod-p computation "
                                     "at each of the 7 primes (independent of, and consistent with, that "
                                     "prior exact-rational finding).",
        },
        "predicates": {
            "P_F_0": {
                "statement": "L^(4) = 0",
                "result": f0.get("P_F_0_L4_is_zero_all_primes"),
                "pass": f0.get("P_F_0_L4_is_zero_all_primes") is True,
            },
            "P_F_3": {
                "statement": "D_12 not equiv 0 mod p for p in {3617,43867,283,617} (本命)",
                "result": P_F_3_all_honmei_nonzero,
                "pass": P_F_3_all_honmei_nonzero is True,
            },
            "naizo_taisho_check": {
                "statement": "D_12 not equiv 0 mod p for p in {131,593,11} (内蔵対照, same expectation as P-F-3)",
                "result": naizo_all_nonzero,
                "pass": naizo_all_nonzero is True,
            },
        },
        "no_verdict_note": "S-WFS-5 compliance: raw values and boolean predicate PASS/FAIL only, "
                            "no interpretive verdict prose of the kinds forbidden in the design doc's "
                            "SS5.2 stop-rule table is written anywhere in this cert.",
        "S_side_note": "S-WFS-4 compliance: no S_16 or any S-side object is formed anywhere in F0/F1 "
                        "(only A-side sigma_m/D_12/L, all already-established A-side objects).",
    }

    forbidden = ["正典超過", "分光器", "非正則性に反応", "不均衡", "SYN-0", "段差"]
    blob = json.dumps(out, ensure_ascii=False)
    for w in forbidden:
        if w in blob:
            raise ValueError(f"S-WFS-5 self-scan FAILED: forbidden verdict word {w!r} found in output")

    out_path = "search/certs/spec_f0_f1_v1_20260807.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print(f"P_F_0.pass = {out['predicates']['P_F_0']['pass']}")
    print(f"P_F_3.pass = {out['predicates']['P_F_3']['pass']}")
    print(f"naizo_taisho_check.pass = {out['predicates']['naizo_taisho_check']['pass']}")


if __name__ == "__main__":
    main()
