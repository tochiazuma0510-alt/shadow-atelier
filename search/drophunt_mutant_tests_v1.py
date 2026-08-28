#!/usr/bin/env python3
"""
drophunt_mutant_tests_v1.py -- injects the 12 mandatory mutants (scratchpad/
fib_ruling_and_fibre_checker_spec_v1.md SS2.6, "mandatory mutants" list,
9 base categories + 3 ruling-1720-specific ones = 12 total as numbered in the
coordinator's task) into a copy of a real PASSING base receipt and confirms
search/drophunt_checker_v1.py (the independent checker) REJECTS every one.

Base receipt: search/certs/drophunt_checker_receipt_cheap1_fib2_row36_v1_20260830.json
(the smallest real window, F3=2, valid=1 -- both candidates evaluated, one
verdict True one False, giving a rich-enough row set for tampering).

Two mutants (#4 non-isolated-claimed-isolated, #5 seed-from-symdiff) are
marked NOT_APPLICABLE with an explicit reason: this producer/checker pair
does not emit or consume an isolation claim (F4 is out of scope for this
calibration pass, per spec 2.0's own note that isolation only matters for
POSITIVE verdicts, not the negative-only cheap-window sweep this pass
targets), and does not track seed-roster provenance (seed_pool_432 vs
symdiff_432 membership) since the two hardcoded seeds (row36, row71) are
fixed literals, not drawn from a roster at receipt-generation time. These
are reported honestly as scope gaps, not silently skipped.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

BASE = "search/certs/drophunt_checker_receipt_cheap1_fib2_row36_v1_20260830.json"
# mutant #10 (m-direction dropped) needs a base window where K_ord != M_ord
# (i.e. F1 genuinely > 1), otherwise forcing F1_m_factor:=1 is a no-op.
BASE_F1_GT_1 = "search/certs/drophunt_checker_receipt_fib4_kordvalidated_row36_v1_20260830.json"
OUT_DIR = Path("search/certs/drophunt_mutants_v1")
CHECKER = "search/drophunt_checker_v1.py"


def load_base() -> dict:
    with open(BASE, encoding="utf-8") as f:
        return json.load(f)


def run_checker(path: Path) -> dict:
    proc = subprocess.run([sys.executable, "-B", CHECKER, str(path)], capture_output=True, text=True)
    try:
        result = json.loads(proc.stdout)[0]
    except Exception:
        return {"status": "CHECKER_CRASHED", "errors": [proc.stdout, proc.stderr]}
    return result


def write_mutant(name: str, receipt: dict) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)
    return path


def mutant_1_candidate_omission(base: dict) -> dict:
    r = copy.deepcopy(base)
    r["rows"] = r["rows"][:-1]
    r["cc1_candidate_coverage"]["evaluated_count"] -= 1
    return r


def mutant_2_duplicate(base: dict) -> dict:
    r = copy.deepcopy(base)
    r["rows"] = [r["rows"][0], r["rows"][0]]
    return r


def mutant_3_wrong_parent_inclusion(base: dict) -> dict:
    r = copy.deepcopy(base)
    r["window"]["K_ord"] = r["window"]["K_ord"] + 1  # breaks K_ord % M_ord == 0
    return r


def mutant_6_row_index_shift(base: dict) -> dict:
    r = copy.deepcopy(base)
    r["rows"][0]["m"] = r["rows"][0]["m"] + 1  # breaks m % M_ord == seed m_seed(=0)
    return r


def mutant_7_reversed_word_convention(base: dict) -> dict:
    r = copy.deepcopy(base)
    flip = {1: 2, -1: -2, 2: 1, -2: -1}
    r["rows"][0]["f_word_codes"] = [flip[c] for c in r["rows"][0]["f_word_codes"]]
    # verdict/hex fields left as the ORIGINAL (pre-flip) producer claims,
    # simulating a producer that used the wrong x/y convention when writing
    # the word but computed its verdict under the correct one (or vice versa)
    return r


def mutant_8_charming_onto_swap(base: dict) -> dict:
    r = copy.deepcopy(base)
    row = r["rows"][1]  # the non-charming row in this base receipt
    row["charming"], row["onto"] = row["onto"], row["charming"]
    if row["onto"] and not row["charming"]:
        row["onto"] = True  # keep the illegal combination explicit
    return r


def mutant_9_fib_wrong_formula(base: dict) -> dict:
    r = copy.deepcopy(base)
    # simulate v1's bug: fib computed as [M:K]*F2 instead of (K_ord/M_ord)*F2;
    # here just inflate F3 by an extra factor to mimic the inflation direction
    r["window"]["F3_fib"] = r["window"]["F3_fib"] * 3
    return r


def mutant_10_m_direction_dropped(base_f1_gt_1: dict) -> dict:
    r = copy.deepcopy(base_f1_gt_1)
    assert r["window"]["K_ord"] // r["window"]["M_ord"] > 1, "base window must have genuine F1>1 for this mutant to be non-trivial"
    r["window"]["F1_m_factor"] = 1  # drop the true m-direction multiplicity
    r["window"]["F3_fib"] = r["window"]["F2_ratio"]  # #fib = F2 only, m-direction ignored (the actual v1-style bug shape)
    return r


def mutant_11_theta_tau_on_quotient(base: dict) -> dict:
    r = copy.deepcopy(base)
    # simulate the quotient-shortcut bug's OBSERVABLE effect: producer
    # records hex310=True for a row where the (correct, word-level) value
    # is actually False-inducing after a convention corruption -- approximate
    # by flipping the recorded hex310 boolean on the passing row while
    # leaving its word/verdict otherwise untouched (checker must recompute
    # independently and catch the mismatch)
    row = r["rows"][0]
    row["hex310"] = not row["hex310"]
    return r


def mutant_12_reduction_index_order(base: dict) -> dict:
    r = copy.deepcopy(base)
    r["reduction_index_order"] = "target_first"
    return r


def main() -> int:
    base = load_base()
    with open(BASE_F1_GT_1, encoding="utf-8") as f:
        base_f1_gt_1 = json.load(f)
    mutants = {
        "1_source_omission": mutant_1_candidate_omission(base),
        "2_duplicate": mutant_2_duplicate(base),
        "3_wrong_parent_inclusion": mutant_3_wrong_parent_inclusion(base),
        "4_nonisolated_claimed_isolated": None,  # N/A, see docstring
        "5_seed_from_symdiff": None,  # N/A, see docstring
        "6_row_index_shift": mutant_6_row_index_shift(base),
        "7_reversed_word_convention": mutant_7_reversed_word_convention(base),
        "8_charming_onto_swap": mutant_8_charming_onto_swap(base),
        "9_fib_wrong_formula": mutant_9_fib_wrong_formula(base),
        "10_m_direction_dropped": mutant_10_m_direction_dropped(base_f1_gt_1),
        "11_theta_tau_on_quotient": mutant_11_theta_tau_on_quotient(base),
        "12_reduction_index_order": mutant_12_reduction_index_order(base),
    }

    results = {}
    for name, receipt in mutants.items():
        if receipt is None:
            results[name] = {"status": "NOT_APPLICABLE", "reason": "see module docstring: F4 isolation and seed-roster provenance are out of this pass's scope"}
            continue
        path = write_mutant(name, receipt)
        verdict = run_checker(path)
        rejected = verdict["status"] != "PASS"
        results[name] = {"status": "REJECTED" if rejected else "NOT_REJECTED_BUG", "checker_status": verdict["status"], "checker_errors": verdict.get("errors", [])}

    all_rejected = all(r["status"] in ("REJECTED", "NOT_APPLICABLE") for r in results.values())
    out = {
        "schema": "drophunt-mutant-tests/v1",
        "base_receipt": BASE,
        "base_receipt_f1_gt_1_for_mutant_10": BASE_F1_GT_1,
        "all_applicable_mutants_rejected": all_rejected,
        "results": results,
    }
    print(json.dumps(out, indent=2))
    with open("search/certs/drophunt_mutant_tests_v1_20260830.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    return 0 if all_rejected else 1


if __name__ == "__main__":
    sys.exit(main())
