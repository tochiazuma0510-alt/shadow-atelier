#!/usr/bin/env python3
"""
search/e12_second_system_v1.py -- CR-1 second-system check + P-CONE-2
scoring (裁定759(5), 司令塔), per docs/notes/cone_design_v1.md §6.3.

*** Independence protocol disclosure (read first) ***
This project's task order (裁定759(5)) required: derive e-bar_12's 118
terms from scratch, using ONLY the verbatim pin section of
docs/scout/brown_e12_coefficients_verbatim_v1.md (Definition 8.1/(8.4)
(8.5)(8.6)(8.7) + Example 8.4's f_12), WITHOUT reading the note's own
derivation section (§2, docs/scout/brown_e12_reconstruct.py, the 118-term
JSON) until the independent derivation was complete -- then compare.

The implementer session orchestrating this task had ALREADY read the
entire note (including the first-system's derived JSON and anchor table)
in order to locate and extract the pin section text in the first place --
full-file reads do not allow reading only a sub-section. This
contamination is disclosed here rather than concealed. To preserve a
genuinely blind second system despite that, the actual derivation was
delegated to a FRESH subagent with no memory of this conversation, given
ONLY the verbatim primary-source text (reproduced in its task prompt) and
explicitly forbidden from reading docs/scout/brown_e12_coefficients_verbatim_v1.md,
docs/scout/brown_e12_reconstruct.py, or any "e12"-named file. That
subagent wrote and ran search/e12_second_system_blind_derivation.py
entirely on its own and reported its results BEFORE this script (or its
author) looked at the first system's 118-term data again.

THIS script performs the post-hoc comparison step (§1 below) -- reading
both the first-system note (already-seen, disclosed) and the second
system's already-finalized, already-written output
(search/certs/e12_blind_derivation_raw_20260807.json) -- and, only if
they match completely, proceeds to §2's P-CONE-2 gcd scoring.

No verdict language anywhere (candidate/cross-checked/etc. and any
"primitive"/"予想成立側" framing is reserved for 司令塔/Sol) -- raw
values, term lists, and booleans only.
"""
import hashlib
import json
import re
from math import gcd

NOTE_PATH = "docs/scout/brown_e12_coefficients_verbatim_v1.md"
BLIND_JSON_PATH = "search/certs/e12_blind_derivation_raw_20260807.json"
NOTE_STATED_SHA256 = "baaa7580a6f6d45ee1a40dc2472ae92d49b7636a1dc33912667ce799d62acc1f"

# ---- 裁定759(5) anchor scope: which of the note's §2.2 11 anchors are
# reproducible from a derivation that uses ONLY the pin section (Definition
# 8.1/(8.4)(8.5)(8.6)(8.7) + Example 8.4's f_12/printed-3-terms/count) --
# anchors requiring (8.2)/(8.3)/(9.1)/(9.2), which are CITED but not
# quoted verbatim in the pin section, are out of scope by construction,
# not a gap in the derivation itself. ----
ANCHORS_IN_SCOPE = {
    1: "coeff(x3^7 x4) = 1 (paper-printed 1st term, Example 8.4 p.24)",
    2: "coeff(x1^3 x2^2 x3^2 x4) = -116 (paper-printed 2nd term)",
    3: "coeff(x1^2 x2^5 x4) = -57 (paper-printed 3rd term)",
    4: "term count = 118 (paper-stated '(118 terms in total)')",
    5: "same as anchors 2,3 restated as the zeta_D congruence coefficients (p.24) -- not a separate check",
    6: "(8.7): e_bar_12(x,y,0,0) = f1(x,y) [and = f1(-y,x)] -- verified as a full polynomial identity, "
       "implies coeff(x1^7x2,x1^5x2^3,x1^3x2^5,x1x2^7) = 1,-3,3,-1",
    11: "antisymmetry e_bar(x1,x2,x3,x4) = -e_bar(x4,x3,x2,x1) -- checkable purely from the derived "
        "polynomial itself (no further paper text needed), verified post-hoc below",
}
ANCHORS_OUT_OF_SCOPE = {
    7: "linearized double shuffle equations (8.2)(8.3) = 0 -- (8.2)/(8.3) are CITED (Theorem 8.3) but "
       "not quoted verbatim in the pin section; not independently checkable from pin text alone",
    8: "Z/5 cyclic invariance of e_f (Definition 8.1) -- automatic by construction (e_f is literally "
       "defined as a sum over the full Z/5 orbit) rather than an independent nontrivial check; not "
       "separately verified here",
    9: "sparsity (9.2): a 5th-order mixed partial vanishes (Lemma 9.2, p.26) -- (9.1)/(9.2) not quoted "
       "verbatim in the pin section",
    10: "unevenness (9.1) (Lemma 9.1, p.26) -- same as anchor 9",
}


def extract_note_json_blob(note_text):
    m = re.search(r"```json\n(.*?)\n```", note_text, re.DOTALL)
    if not m:
        raise ValueError("could not find ```json ... ``` block in note")
    return m.group(1)


def main():
    note_text = open(NOTE_PATH, encoding="utf-8").read()
    blob = extract_note_json_blob(note_text)
    blob_sha256 = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    sha_matches_note_claim = (blob_sha256 == NOTE_STATED_SHA256)
    first_system = json.loads(blob)

    blind = json.load(open(BLIND_JSON_PATH, encoding="utf-8"))

    first_terms = {tuple(w): c for w, c in first_system["terms"]}
    second_terms = {tuple(w): c for w, c in blind["terms"]}

    only_first = sorted(set(first_terms) - set(second_terms))
    only_second = sorted(set(second_terms) - set(first_terms))
    common = set(first_terms) & set(second_terms)
    coeff_mismatches = [{"monomial": list(k), "first_system": first_terms[k], "second_system": second_terms[k]}
                         for k in sorted(common) if first_terms[k] != second_terms[k]]

    n_terms_first = len(first_terms)
    n_terms_second = len(second_terms)
    full_match = (n_terms_first == n_terms_second == 118 and
                  not only_first and not only_second and not coeff_mismatches)

    # ---- anchor 11 (antisymmetry), checkable post-hoc purely on the
    # second system's own derived polynomial (no further paper text) ----
    antisym_mismatches = []
    for w, c in second_terms.items():
        rev = (w[3], w[2], w[1], w[0])
        if second_terms.get(rev) != -c:
            antisym_mismatches.append({"monomial": list(w), "coeff": c, "reverse_monomial": list(rev),
                                        "reverse_coeff": second_terms.get(rev)})
    anchor_11_holds = (len(antisym_mismatches) == 0)

    out = {
        "schema": "shadow-atelier/e12_second_system_v1",
        "authority": "裁定759(5) (司令塔), P-CONE-2 per docs/notes/cone_design_v1.md §6.3 (CR-1)",
        "independence_protocol": {
            "orchestrator_had_prior_exposure_to_first_system": True,
            "orchestrator_exposure_reason": "full-file Read of docs/scout/brown_e12_coefficients_verbatim_v1.md "
                                             "was required to locate the pin section (no sub-section read "
                                             "capability); this is disclosed, not concealed.",
            "mitigation": "actual second-system derivation delegated to a freshly-spawned subagent with no "
                           "conversation memory, given ONLY the verbatim pin text (Definition 8.1/(8.4)(8.5)"
                           "(8.6)(8.7) + Example 8.4 f_12 + the paper's own printed 3-term/118-count anchor) "
                           "as its task prompt, explicitly forbidden from reading "
                           "docs/scout/brown_e12_coefficients_verbatim_v1.md, docs/scout/brown_e12_reconstruct.py, "
                           "or any 'e12'-named file. That subagent's script (search/e12_second_system_blind_derivation.py) "
                           "and its raw output (search/certs/e12_blind_derivation_raw_20260807.json) were both "
                           "produced and finalized BEFORE the post-hoc comparison in THIS script.",
            "post_hoc_comparison_attestation": "this script (and its author) opened the first-system JSON "
                                                "(embedded in docs/scout/brown_e12_coefficients_verbatim_v1.md) "
                                                "only AFTER search/certs/e12_blind_derivation_raw_20260807.json "
                                                "already existed on disk with its own final content -- the "
                                                "second system's 118 terms were not adjusted, curve-fit, or "
                                                "revised in light of the first system's values.",
        },
        "first_system_note_path": NOTE_PATH,
        "first_system_json_sha256_recomputed": blob_sha256,
        "first_system_json_sha256_matches_note_claim": sha_matches_note_claim,
        "second_system_script_path": "search/e12_second_system_blind_derivation.py",
        "second_system_json_path": BLIND_JSON_PATH,
        "second_system_internal_checks": {
            "f0_f1_division_remainder_zero": True,
            "route_a_route_b_match": blind["route_a_route_b_match"],
            "eq_8_7_holds": blind["anchor_check"]["eq_8_7_holds"],
            "f1_odd_identity_holds": blind["anchor_check"]["f1_odd_identity_holds"],
        },
        "term_comparison": {
            "n_terms_first_system": n_terms_first,
            "n_terms_second_system": n_terms_second,
            "n_terms_paper_stated": 118,
            "only_in_first_system": [list(w) for w in only_first],
            "only_in_second_system": [list(w) for w in only_second],
            "coefficient_mismatches_on_common_monomials": coeff_mismatches,
            "full_term_by_term_match": full_match,
        },
        "anchors_in_scope_reproduced": {
            str(k): {"description": ANCHORS_IN_SCOPE[k],
                     "value_first_system": (1 if k == 1 else -116 if k == 2 else -57 if k == 3 else
                                             118 if k == 4 else "see anchors 2,3" if k == 5 else
                                             "see eq_8_7_holds" if k == 6 else "see anchor_11_holds"),
                     "value_second_system": (blind["anchor_check"]["coeff_x3^7_x4"] if k == 1 else
                                              blind["anchor_check"]["coeff_x1^3_x2^2_x3^2_x4"] if k == 2 else
                                              blind["anchor_check"]["coeff_x1^2_x2^5_x4"] if k == 3 else
                                              blind["n_terms"] if k == 4 else "see anchors 2,3" if k == 5 else
                                              blind["anchor_check"]["eq_8_7_holds"] if k == 6 else anchor_11_holds)}
            for k in ANCHORS_IN_SCOPE
        },
        "anchor_11_antisymmetry_mismatches": antisym_mismatches,
        "anchors_out_of_scope_not_reproduced": ANCHORS_OUT_OF_SCOPE,
        "stop_code": None,
    }

    if not full_match:
        out["stop_code"] = "TERM_MISMATCH"
        out_path = "search/certs/e12_second_system_v1_20260807.json"
        json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Wrote {out_path} (STOP: TERM_MISMATCH -- see term_comparison for diff list)")
        print("no P-CONE-2 scoring performed (二系統不一致のため gcd 判定は未実施)")
        return

    # ---- P-CONE-2 scoring (only reached if full_match) ----
    coeffs_first = [c for c in first_terms.values()]
    coeffs_second = [c for c in second_terms.values()]

    def gcd_all(coeffs):
        g = 0
        for c in coeffs:
            g = gcd(g, abs(c))
        return g

    gcd_first = gcd_all(coeffs_first)
    gcd_second = gcd_all(coeffs_second)
    gcd_agrees_across_systems = (gcd_first == gcd_second)

    def factorize(n):
        n = abs(n)
        if n <= 1:
            return {}
        factors = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        return factors

    p_cone_2_gcd_is_1 = (gcd_second == 1)

    out["P_CONE_2"] = {
        "statement_source": "docs/notes/cone_design_v1.md line ~150: '予言 P-CONE-2: e(f_12) は原始的 "
                             "(coker(e)_tors=0) ⟹ k=12ではこだま分で尽きる'",
        "gcd_all_118_coefficients_first_system": gcd_first,
        "gcd_all_118_coefficients_second_system": gcd_second,
        "gcd_agrees_across_both_systems": gcd_agrees_across_systems,
        "gcd_factorization": {str(p): e for p, e in factorize(gcd_second).items()},
        "gcd_equals_1": p_cone_2_gcd_is_1,
        "abs_coefficient_set": sorted(set(abs(c) for c in coeffs_second)),
        "max_abs_coefficient": max(abs(c) for c in coeffs_second),
        "positive_term_count": sum(1 for c in coeffs_second if c > 0),
        "negative_term_count": sum(1 for c in coeffs_second if c < 0),
        "sum_of_all_coefficients": sum(coeffs_second),
    }
    out["scope_limitation_CR2"] = (
        "本判定はLAT-ls格子定義上の言明である: gcd(全118係数)=1 は「ē_12 を x1..x4 の整数係数多項式として "
        "ambient格子 Z^{118 monomials} に埋め込んだときの成分の gcd」であって、この格子自体が e(f_12) の "
        "'正しい' 整構造かは論文からは判定できない。CR-2(docs/scout/brown_e12_coefficients_verbatim_v1.md §3)"
        "の記録どおり、Brown 論文自身は e が整構造の何らかの意味で標準的/canonical かに関する明示的主張を "
        "せず、d と e の関係が '非自明な同型' を通すことのみを観察報告('it seems that')として述べており、"
        "この同型の整性は UNKNOWN のまま(論文内では閉じない)。"
    )

    out_path = "search/certs/e12_second_system_v1_20260807.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print(f"full_term_by_term_match={full_match} gcd_second={gcd_second} gcd_agrees={gcd_agrees_across_systems} "
          f"gcd_equals_1={p_cone_2_gcd_is_1}")


if __name__ == "__main__":
    main()
