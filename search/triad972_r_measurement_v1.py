"""
search/triad972_r_measurement_v1.py -- TRIAD-972 (beta) simultaneous-disclosure r measurement.

Order: commander direct order, quarantine release ruling 1120 (protocol = ruling 1118).
Inputs (both frozen certs read under the declared simultaneous-disclosure release):
  - search/certs/sol123_p8_a_class_v1_20260813.json   (a_class -- [a] raw value)
  - search/certs/ds4_receipt_v1_20260812.json          ([b] raw exponents, re-normalized
    independently in THIS script -- third independent derivation, not imported from ds4_receipt_v1.py)
  - search/certs/sol123_u3_disc_v1_20260813.json       (S -- simultaneous-disclosure record only)

Procedure documents (sha256 reconfirmed at run time, hard-asserted):
  - docs/notes/p8_prereg_v3_2.md            (P8 v3.2 -- a_class accept test + d9 receipt procedure)
  - docs/notes/branchP_and_r_spec_v1.md     (r card v2 body, second half of file -- II.3/[3]/[2]/[4])
  - docs/notes/r_card_v2_addendum_1.md      (r card v2 addendum 1)

No interpretation, no verdict words. All values are machine-computed exact (Fraction/int only).
r-computation reuses search/r_intersection_template_v1.py (canary 4/4 reconfirmed before real
data is plugged in, per that module's own discipline).

NAME-COLLIDE: the a_class quantity here is a K^(9)-window-family instance object (Sol-123/DESC-9
task), distinct from the sealed K^(5) quantities. u is touched (unavoidable, a_class-derived) but
no sealed-quantity value is read or written by this script.
"""
import hashlib
import json
import sys
from math import gcd

sys.path.insert(0, "search")
from r_intersection_template_v1 import r_intersection  # noqa: E402

N = 9

PROC_DOCS = {
    "docs/notes/p8_prereg_v3_2.md": "3a9cfb060c5af3bef7e54d9c849709852b9579cacf49d5651d1417cb842161fc",
    "docs/notes/branchP_and_r_spec_v1.md": "b1300005cb9935a1951db4c58836a217b9ced0b815ba8a575805b4f77e3b97c9",
    "docs/notes/r_card_v2_addendum_1.md": "19baf388b2e62ef675cd2a1902fb8bdbff35501c40559ddd77aa5b32ccfc2346",
}

INPUT_CERTS = {
    "a_class": ("search/certs/sol123_p8_a_class_v1_20260813.json",
                "dd1cf38556d0eff58ab29f0cd47bf762df782c45c43e9b27741bba3e015210b8"),
    "ds4_b": ("search/certs/ds4_receipt_v1_20260812.json", None),
    "S": ("search/certs/sol123_u3_disc_v1_20260813.json",
          "d2f3b361d8bec47077c37017d26a9259d225c56daa9bea55b7a0306fb4af231e"),
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def normalize_class_mod9(raw_exponents: dict):
    """
    raw_exponents: {prime(str or int): integer exponent} (may be negative, may exceed 9).
    Returns (support_sorted, exponents_mod9_aligned, order) per Q^x/(Q^x)^9 convention:
    reduce mod 9, drop primes whose reduced exponent is 0.
    """
    reduced = {}
    for p, e in raw_exponents.items():
        p = int(p)
        vmod = e % N
        if vmod != 0:
            reduced[p] = vmod
    support = sorted(reduced.keys())
    exponents = [reduced[p] for p in support]
    order = 1
    for p in support:
        vmod = reduced[p]
        contrib = N // gcd(N, vmod)
        order = order * contrib // gcd(order, contrib)
    if not support:
        order = 1
    return support, exponents, order


def main():
    report = {"schema": "triad972_r_measurement/v1", "artifact_date": "2026-08-13",
              "task": "[CP] TRIAD-972 beta -- simultaneous disclosure + r cross-check",
              "authorisation": "ruling 1118 (protocol) / ruling 1120 (quarantine release, this task only)"}

    # -- sha reconfirmation of procedure docs --
    proc_sha = {}
    for path, expected in PROC_DOCS.items():
        actual = sha256_file(path)
        proc_sha[path] = {"sha256_actual": actual, "sha256_expected": expected,
                           "match": (expected is None or actual == expected)}
    report["procedure_doc_sha_reconfirmation"] = proc_sha

    # -- sha reconfirmation of input certs --
    cert_sha = {}
    raw_certs = {}
    for key, (path, expected) in INPUT_CERTS.items():
        actual = sha256_file(path)
        cert_sha[key] = {"path": path, "sha256_actual": actual, "sha256_expected": expected,
                          "match": (expected is None or actual == expected)}
        raw_certs[key] = load_json(path)
    report["input_cert_sha_reconfirmation"] = cert_sha

    # ================= [a] raw value (from a_class cert, machine transcription only) =================
    ac = raw_certs["a_class"]["a_class"]
    a_support = ac["support"]
    a_exponents = ac["exponents"]
    a_order = ac["order"]
    report["a_raw"] = {
        "source_cert": INPUT_CERTS["a_class"][0],
        "support": a_support,
        "exponents_mod9": a_exponents,
        "order": a_order,
        "name_collide_note": ("this a_class is a K^(9)-window-family instance object "
                               "(task tag Sol-123/DESC-9); distinct from the sealed K^(5) "
                               "quantities. u is touched (unavoidable, a_class-derived); "
                               "no sealed-quantity value is read or written here."),
    }

    # ================= P8 v3.2 accept test (S-1 score rule), raw result =================
    p8_precondition_pass = (a_support == [3] and a_order == 9)
    report["p8_accept_test_raw"] = {
        "rule": "a_class.support == [3] and a_class.order == 9  (P8 v3.2 S1, docs/notes/p8_prereg_v3_2.md sec.3)",
        "observed_support": a_support,
        "observed_order": a_order,
        "precondition_met": p8_precondition_pass,
        "p8_branch_if_not_met": "(u2) support != {3} -- see p8_prereg_v3_2.md sec.5",
        "cert_self_reported_score_rule_s1_result": raw_certs["a_class"]["score_rule_s1_measurement"]["result"],
    }

    # ================= P8 v3.2 (u2) branch outcome, machine-readable (ruling 1122) =================
    # Ruling 1122: the frozen document's internal branch ((u2): support != {3} => P-K9U-1 is a
    # miss) is the governing prereg outcome and takes precedence over a conservative paraphrase
    # ("stop as UNKNOWN") in the task's cover instructions. This is a determinate prereg outcome,
    # not an open/blocked state.
    report["p8_u2_branch_outcome"] = {
        "branch": "(u2)",
        "condition_observed": "support != {3}",
        "outcome": "P-K9U-1 is a miss, per P8 v3.2 (u2) prereg branch (docs/notes/p8_prereg_v3_2.md sec.5)",
        "outcome_type": "determinate prereg outcome (not UNKNOWN / not open)",
        "authorisation_for_this_reading": "ruling 1122 (commander) -- frozen doc's internal branch "
                                           "governs over the cover instruction's conservative paraphrase",
        "note": "this records that the specific prediction P-K9U-1 did not hit; it is not a verdict "
                "on TRIAD-972, r, or d9",
    }

    # ================= d9 receipt raw value (ord([a])) =================
    # Per Kummer theory (independent of whether the P8 S-1 precondition holds), the raw
    # order of [a] in Q^x/(Q^x)^9 is a machine fact already present in the a_class cert.
    # Its use AS a receipt confirming the specific P-K9U-1 field prediction requires the
    # precondition above; that interpretive step is withheld here per task instruction.
    report["d9_receipt_raw"] = {
        "value_ord_a": a_order,
        "precondition_for_p_k9u1_specific_receipt": p8_precondition_pass,
        "status": ("d9 = ord([a]) is a raw machine value in all cases; its interpretation as "
                    "confirming L_9,Aff = Q(zeta_9, 3^{1/9}) (P-K9U-1) requires the P8 S-1 "
                    "precondition, which is " + ("MET" if p8_precondition_pass else "NOT MET") +
                    " here. No verdict is asserted."),
    }

    # ================= d9 interpretation withheld (ruling 1122, explicit) =================
    report["d9_interpretation_withheld"] = {
        "withheld_question_1": "whether ord([a])=9 substantiates/instantiates the d9 used in the "
                                "TRIAD-972 reduction formula |X\\A| = 972 - 12*d9*dS4/r",
        "withheld_question_2": "the meaning of support([a]) = {2} (as opposed to the P-K9U-1 "
                                "prediction of {3})",
        "withheld_until": "commander gate + mathematician reading",
        "provenance_not_interpretation": "the value d9=9 used as a factor in the |X\\A| formula "
                                          "below is recorded as: the MEASURED VALUE of ord([a]) "
                                          "(a_class cert, sha dd1cf38556d0eff58ab29f0cd47bf762df782c45c43e9b27741bba3e015210b8), "
                                          "not as an asserted identification of that quantity with "
                                          "TRIAD-972's d9. This is a provenance record, not an "
                                          "interpretive claim.",
    }

    # ================= [b] independent re-derivation (third derivation) =================
    ds4 = raw_certs["ds4_b"]
    raw_b_exponents = ds4["d1_input_tamper_check"]["fresh_factorization_of_abs_value"]
    b_support, b_exponents, b_order = normalize_class_mod9(raw_b_exponents)
    report["b_raw_independent_rederivation"] = {
        "source_cert": INPUT_CERTS["ds4_b"][0],
        "raw_exponents_pre_normalization": raw_b_exponents,
        "normalization_rule": "reduce each exponent mod 9; drop primes whose reduced exponent is 0",
        "support": b_support,
        "exponents_mod9": b_exponents,
        "order": b_order,
        "cross_check_against_ds4_cert_ord_value": ds4.get("ord_value"),
        "match": (b_order == ds4.get("ord_value")),
    }

    # ================= r canary reconfirmation (must run before real data) =================
    canary_path = "search/certs/r_intersection_template_canary_20260812.json"
    canary = load_json(canary_path)
    report["r_canary_reconfirmation"] = {
        "canary_cert": canary_path,
        "all_pass": canary["all_pass"],
        "n_canaries": len(canary["canaries"]),
    }
    assert canary["all_pass"], "r_intersection_template_v1 canary did not pass 4/4 -- STOP"

    # ================= r value (real data) =================
    a_rep = 1
    for p, e in zip(a_support, a_exponents):
        a_rep *= p ** e
    b_rep = 1
    for p, e in zip(b_support, b_exponents):
        b_rep *= p ** e
    r_result = r_intersection(a_rep, b_rep, verbose=False)
    report["r_measurement_raw"] = {
        "a_representative_integer": a_rep,
        "b_representative_integer": b_rep,
        "support_primes_union": r_result["support_primes"],
        "a_vector_mod9": r_result["a_vector_mod_9"],
        "b_vector_mod9": r_result["b_vector_mod_9"],
        "ord_a": r_result["ord_a"],
        "ord_b": r_result["ord_b"],
        "subgroup_a_elements": r_result["subgroup_a_elements"],
        "subgroup_b_elements": r_result["subgroup_b_elements"],
        "intersection_elements": r_result["intersection_elements"],
        "r": r_result["r"],
    }

    # ================= TRIAD-972 raw factor comparison (no verdict) =================
    d9 = r_result["ord_a"]
    dS4 = r_result["ord_b"]
    r_val = r_result["r"]
    r_ge_3 = (r_val >= 3)
    numerator = 12 * d9 * dS4
    divisible = (numerator % r_val == 0)
    x_minus_a = (972 - numerator // r_val) if divisible else None
    non_trigger_triple = (d9, dS4, r_val) == (9, 9, 1)
    report["triad972_raw_comparison"] = {
        "formula": "|X\\A| = 972 - 12*d9*dS4/r",
        "d9": d9, "d_S4": dS4, "r": r_val,
        "d9_provenance": "d9 as used here is the MEASURED VALUE of ord([a]) from the r-measurement "
                          "above (== a_class cert's own reported order); its identification with "
                          "TRIAD-972's d9 is a provenance record, not an interpretive claim (see "
                          "d9_interpretation_withheld above)",
        "r_ge_3": r_ge_3,
        "twelve_d9_dS4": numerator,
        "divisible_by_r": divisible,
        "X_minus_A_raw_value": x_minus_a,
        "non_trigger_triple_is_9_9_1": non_trigger_triple,
        "observed_triple_equals_non_trigger_triple": ((d9, dS4, r_val) == (9, 9, 1)),
    }

    # ================= S simultaneous disclosure -- raw values only =================
    s_cert = raw_certs["S"]
    s_support = s_cert["candidate_S"]["support"]
    a_support_for_s_check = set(a_support)
    s_support_set = set(s_support)
    contains = a_support_for_s_check.issubset(s_support_set)
    report["S_simultaneous_disclosure_raw"] = {
        "source_cert": INPUT_CERTS["S"][0],
        "S_support": s_support,
        "supp_a": a_support,
        "S_contains_supp_a": contains,
        "note": ("raw containment fact only; no interpretation of what containment/non-containment "
                  "means for unram_gap_4 (recorded OPEN in the S cert) is asserted here"),
    }

    report["d_no_interpretation"] = "machine values only; verdict is commander's"
    report["u_touched"] = True
    report["c_contact"] = False
    report["sealed_three_quantities_contact"] = False

    out_path = "search/certs/triad972_r_measurement_v1_20260813.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)
    print("wrote", out_path)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
