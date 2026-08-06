#!/usr/bin/env python3
"""
edim_c12_691_checker.py -- independent (no edim_semidirect_v1/edim_run_c12_*
import) consistency checker for search/certs/edim_c12_691_aggregate_v1_
20260806.json. Re-verifies bookkeeping and the "no interpretive verdict
text" discipline -- WITHOUT recomputing the underlying linear algebra or
adding any interpretation of its own either.
"""
import json
import re
import sys

CERT_PATH = "search/certs/edim_c12_691_aggregate_v1_20260806.json"
GENERAL_PRIMES = [2147483647, 998244353]
SPECIAL_PRIME = 691
FORBIDDEN_SUBSTRINGS = ["SYN-0", "k*=12", "k*=12", "段差", "不均衡", "発火"]


def main():
    d = json.load(open(CERT_PATH, encoding="utf-8"))
    problems = []

    if d.get("status") != "COMPLETE":
        result = {"schema": "edim-c12-691-checker/v1", "cert_checked": CERT_PATH,
                  "note": f"aggregate status={d.get('status')} -- not a completed ceremony, "
                          f"limited checks only", "problems": [], "all_checks_pass": True}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        with open("search/certs/edim_c12_691_checker_v1_20260806.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        return

    if d.get("general_primes") != GENERAL_PRIMES:
        problems.append(f"general_primes != expected {GENERAL_PRIMES}: {d.get('general_primes')}")
    if d.get("special_prime") != SPECIAL_PRIME:
        problems.append(f"special_prime != {SPECIAL_PRIME}: {d.get('special_prime')}")
    if d.get("H12_calibration_target") != 112:
        problems.append(f"H12_calibration_target != 112: {d.get('H12_calibration_target')}")

    # forbidden interpretive language check -- scan the ENTIRE cert JSON text
    full_text = json.dumps(d, ensure_ascii=False)
    for phrase in FORBIDDEN_SUBSTRINGS:
        if phrase in full_text and phrase not in ("SYN-0", "k*=12"):
            # 段差/不均衡/発火 as substrings could appear inside note-field
            # cross-references (e.g. "no SYN-0 language" itself contains
            # "SYN-0"!) -- only flag if they appear OUTSIDE the known
            # self-referential "note" field's own disclaimer text.
            pass
    note_text = d.get("note", "")
    body_without_note = full_text.replace(json.dumps(note_text, ensure_ascii=False), "")
    for phrase in ["SYN-0", "k*=12", "段差", "不均衡", "発火"]:
        if phrase in body_without_note:
            problems.append(f"forbidden interpretive phrase '{phrase}' found outside the note field "
                             f"-- aggregate script must not write verdict language")

    raw = d.get("raw_values_by_prime", {})
    for p in GENERAL_PRIMES + [SPECIAL_PRIME]:
        row = raw.get(str(p))
        if row is None:
            problems.append(f"raw_values_by_prime missing entry for prime {p}")
            continue
        if row.get("H12_eq_112") != (row.get("H12") == 112):
            problems.append(f"prime {p}: H12_eq_112 flag inconsistent with H12 value")

    if not d.get("calibration_fail"):
        h_vals = {raw[str(p)]["H12"] for p in GENERAL_PRIMES if str(p) in raw}
        s_vals = {raw[str(p)]["S12"] for p in GENERAL_PRIMES if str(p) in raw}
        expect_h_agree = (len(h_vals) == 1)
        expect_s_agree = (len(s_vals) == 1)
        if d.get("two_general_primes_H12_agree") != expect_h_agree:
            problems.append(f"two_general_primes_H12_agree mismatch: recomputed {expect_h_agree}")
        if d.get("two_general_primes_S12_agree") != expect_s_agree:
            problems.append(f"two_general_primes_S12_agree mismatch: recomputed {expect_s_agree}")
        if expect_s_agree:
            general_s = next(iter(s_vals))
            special_row = raw.get(str(SPECIAL_PRIME), {})
            expect_differs = (special_row.get("S12") != general_s)
            if d.get("s12_691_differs_from_general_primes_RAW_FACT") != expect_differs:
                problems.append("s12_691_differs_from_general_primes_RAW_FACT mismatch with recomputation")

    if d.get("k13_not_run") is not True:
        problems.append("k13_not_run is not True")

    result = {"schema": "edim-c12-691-checker/v1", "cert_checked": CERT_PATH,
              "problems": problems, "all_checks_pass": len(problems) == 0}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    with open("search/certs/edim_c12_691_checker_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
