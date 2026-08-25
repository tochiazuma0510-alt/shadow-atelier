#!/usr/bin/env python3
"""Independent checker for the frozen R07 relative-Frattini type audit.

The checker imports only the frozen *old independent checker* implementation,
never the new producer.  It reconstructs E3/E4, all five coface values, both
literal hexagons, the printed A.18 value, the complete 27-element coarse q3
source fibre, and the registered 4096-word dictionary order.  Required
mutations are destructive in-memory tests.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence


SCHEMA = "d972-r07-relfrat3-actual-class/v1"
TERMINAL = "R07_RELFRAT3_TYPE_MISMATCH_STOP"
FINAL_MARKER = "R07_RELFRAT3_ACTUAL_CLASS_V1_CHECKER_PASS"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECEIPT = Path("search/certs/d972_r07_relfrat3_actual_class_preflight_v1_20260826.json")
Q3_PATH = Path("ci/b345_157dp_artifacts_32171982444/d972_b345_q3_chief_v1.json")
Q3_BYTES = 231_570
Q3_SHA256 = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
OLD_CHECKER_PATH = Path("search/check_d972_b345_relfrat3_v1.py")
OLD_CHECKER_BYTES = 52_315
OLD_CHECKER_SHA256 = "3d86240237229b250943c4795c24c32ac75af9229534c73d16bd838f6d6d0101"
R07_SHA256 = "3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90"
OLD_WORD_SHA256 = "b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d"
DICTIONARY_SHA256 = "3410bbab776fbe1da267d3c3932bf63f9e09bdd02415ee82926619e312d7bbf5"

W2 = (
    1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -2, 1, 1,
    2, 1, 1, -2, 1, 1, 2, 1, 1, 2, 1, 1, -2, 1, 1, -2, 1, 1,
    2, 2, -1, -1, -2, -1,
)
W3 = (
    1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -1, -1, 2,
    -1, -1, -2, -2, 1, 1, 2, 1, 2, 2, 1, 2, 2, -1, 2, 2, 1, 2,
    1, 1, 2, 2, -1, -1, -2, -1, -1, 2, -1, -1, -2, -2, -2, -1,
    -2, -2, 1, 2, 1, 1, -2, 1,
)


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, token: str) -> None:
    if not condition:
        raise CheckFailure(token)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(type(letter) is int and letter in (-2, -1, 1, 2),
                "word alphabet")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-letter for letter in reversed(word)]


def substitute(word: Sequence[int], images: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for letter in word:
        image = list(images[abs(letter)-1])
        out.extend(image if letter > 0 else inverse_word(image))
        out = reduce_word(out)
    return out


def free_reduce(word: Iterable[int], rank: int) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(type(letter) is int and 1 <= abs(letter) <= rank,
                "free word alphabet")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def word_substitute(word: Sequence[int],
                    images: Sequence[Sequence[int]]) -> list[int]:
    rank = max((abs(letter) for image in images for letter in image), default=1)
    out: list[int] = []
    for letter in word:
        require(1 <= abs(letter) <= len(images), "substitution source rank")
        image = list(images[abs(letter)-1])
        out.extend(image if letter > 0 else inverse_word(image))
        out = free_reduce(out, rank)
    return out


def source_words_m0(f: Sequence[int]) -> list[list[int]]:
    ff = word_substitute(f, [[1], [4]])
    g = word_substitute(f, [[1], [2]])
    gs = word_substitute(f, [[4], [5]])
    f1234 = word_substitute(f, [[4, 2], [6]])
    h = word_substitute(f, [[2, 1], [3]])
    middle = word_substitute(f, [[2, 1], [6, 5]])
    return [
        [1],
        free_reduce(inverse_word(g)+[2]+g, 6),
        free_reduce(inverse_word(ff)+inverse_word(h)+[3]+h+ff, 6),
        free_reduce(inverse_word(ff)+[4]+ff, 6),
        free_reduce(inverse_word(ff)+inverse_word(middle)+inverse_word(gs)+
                    [5]+gs+middle+ff, 6),
        free_reduce(inverse_word(f1234)+[6]+f1234, 6),
    ]


def two_sided_residuals(source: Sequence[Sequence[int]],
                        inverse_words: Sequence[Sequence[int]]) \
        -> tuple[list[list[int]], list[list[int]]]:
    st = [free_reduce(word_substitute(inverse_words[i], source)+[-(i+1)], 6)
          for i in range(6)]
    ts = [free_reduce(word_substitute(source[i], inverse_words)+[-(i+1)], 6)
          for i in range(6)]
    return st, ts


def r07_word() -> list[int]:
    step = reduce_word(inverse_word(W3)+list(W2))
    word = reduce_word(list(W2)+step*8)
    require(len(word) == 616 and digest_obj(word) == R07_SHA256,
            "base hash gate")
    return word


def exponent_sums(word: Sequence[int]) -> list[int]:
    return [sum((1 if letter > 0 else -1)
                for letter in word if abs(letter) == i) for i in (1, 2)]


def load_old_checker() -> Any:
    path = ROOT/OLD_CHECKER_PATH
    require(path.is_file() and path.stat().st_size == OLD_CHECKER_BYTES and
            digest_file(path) == OLD_CHECKER_SHA256,
            "old checker pin gate")
    spec = importlib.util.spec_from_file_location(
        "_d972_r07_relfrat3_independent_old_checker", path)
    require(spec is not None and spec.loader is not None,
            "old checker module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def encode_element(value: Any) -> dict[str, Any]:
    row = {"coarse_one_line": [int(x)+1 for x in value[0]],
           "fine_pc_coords": list(value[1])}
    row["sha256"] = digest_obj(row)
    return row


def product(quotient: Any, values: Sequence[Any]) -> Any:
    out = quotient.identity
    for value in values:
        out = quotient.mul(out, value)
    return out


def direct_two_sided_residual_values(
        quotient: Any, source_words: Sequence[Sequence[int]],
        inverse_words: Sequence[Sequence[int]]) -> tuple[list[Any], list[Any]]:
    require(len(source_words) == len(inverse_words) == 6,
            "two-sided residual arity")
    source_values = [quotient.eval(word) for word in source_words]
    inverse_values = [quotient.eval(word) for word in inverse_words]
    st = [quotient.mul(quotient.eval(inverse_words[i], source_values),
                       quotient.inverse(quotient.generators[i]))
          for i in range(6)]
    ts = [quotient.mul(quotient.eval(source_words[i], inverse_values),
                       quotient.inverse(quotient.generators[i]))
          for i in range(6)]
    return st, ts


def literal_hexagons(word: Sequence[int]) -> list[list[int]]:
    theta = substitute(word, ([2], [1]))
    tau = substitute(word, ([2], [-1, -2]))
    tau2 = substitute(tau, ([2], [-1, -2]))
    return [reduce_word(theta+list(word)), reduce_word(list(word)+tau+tau2)]


def a18(quotient: Any, values: Sequence[Any]) -> Any:
    return product(quotient, [values[4], values[2], values[0],
                              quotient.inverse(values[3]),
                              quotient.inverse(values[1])])


def sign_canary(quotient: Any, values: Sequence[Any]) -> dict[str, Any]:
    factors = [values[4], values[2], values[0],
               quotient.inverse(values[3]), quotient.inverse(values[1])]
    labels = ["F", "E", "C", "B^-1", "A^-1"]
    for index, factor in enumerate(factors):
        changed = list(factors)
        changed[index] = quotient.inverse(factor)
        value = product(quotient, changed)
        if value != quotient.identity:
            return {"factor_index_zero_based": index, "factor": labels[index],
                    "mutated_value": encode_element(value), "rejected": True}
    raise CheckFailure("A18 mutation canary unavailable")


def order_canary(quotient: Any, values: Sequence[Any]) -> dict[str, Any]:
    for i in range(5):
        for j in range(i+1, 5):
            changed = list(values)
            changed[i], changed[j] = changed[j], changed[i]
            value = a18(quotient, changed)
            if value != quotient.identity:
                return {"swap_zero_based": [i, j],
                        "mutated_value": encode_element(value),
                        "rejected": True}
    raise CheckFailure("coface order canary unavailable")


def independent_expected(q3: dict[str, Any],
                         include_dictionary: bool = True) -> dict[str, Any]:
    module = load_old_checker()
    e3, e4 = module.reconstruct(q3)
    r07 = r07_word()
    old = list(q3["selected_solution"]["typed_source_word"])
    require(digest_obj(old) == OLD_WORD_SHA256, "old word hash gate")
    context3 = [e3.generators[0], e3.generators[2]]
    contexts4 = [(e4.eval(mapping[0]), e4.eval(mapping[2]))
                 for mapping in module.cofaces(3)]
    rv3, ov3 = e3.eval(r07, context3), e3.eval(old, context3)
    rv4 = [e4.eval(r07, context) for context in contexts4]
    ov4 = [e4.eval(old, context) for context in contexts4]
    require(rv3[0] == ov3[0] and rv3[1] != ov3[1], "E3 mismatch gate")
    require(all(x != y for x, y in zip(rv4, ov4)), "E4 mismatch gate")
    rhex_words, ohex_words = literal_hexagons(r07), literal_hexagons(old)
    rhex = [e3.eval(word, context3) for word in rhex_words]
    ohex = [e3.eval(word, context3) for word in ohex_words]
    require(rhex == ohex == [e3.identity, e3.identity], "hexagon gate")
    require(a18(e4, rv4) == a18(e4, ov4) == e4.identity, "A18 gate")

    coordinate_rows = []
    right_source: list[int] = []
    left_source: list[int] = []
    right_all: list[int] = []
    left_all: list[int] = []
    source_diagnostics = []
    values3 = []
    for index, record in enumerate(q3["correction_fibre"]["records"], 1):
        word = record["word"]
        cv3 = e3.eval(word, context3)
        cv4 = [e4.eval(word, context) for context in contexts4]
        require(cv3[0] == e3.identity[0] and
                list(cv3[1]) == record["ambient_Pi3_coords"],
                "coarse fibre coordinate gate")
        values3.append(cv3)
        coordinate_rows.append({
            "index_one_based": index,
            "word_length": len(word), "word_sha256": digest_obj(word),
            "artifact_ambient_Pi3_coords": record["ambient_Pi3_coords"],
            "direct_source_value": encode_element(cv3),
            "coface_values_sha256": digest_obj(
                [encode_element(value) for value in cv4]),
        })
        r3 = e3.mul(rv3, cv3); l3 = e3.mul(cv3, rv3)
        r4 = [e4.mul(x, y) for x, y in zip(rv4, cv4)]
        l4 = [e4.mul(y, x) for x, y in zip(rv4, cv4)]
        if r3 == ov3: right_source.append(index)
        if l3 == ov3: left_source.append(index)
        if r3 == ov3 and r4 == ov4: right_all.append(index)
        if l3 == ov3 and l4 == ov4: left_all.append(index)
        if r3 == ov3 or l3 == ov3:
            source_diagnostics.append({
                "index_one_based": index,
                "right_equal_by_coface": [x == y for x, y in zip(r4, ov4)],
                "left_equal_by_coface": [x == y for x, y in zip(l4, ov4)],
                "correction_coarse_identity_by_coface": [
                    value[0] == e4.identity[0] for value in cv4],
                "correction_fine_pc_coords_by_coface": [
                    list(value[1]) for value in cv4],
            })
    require(len(set(values3)) == 27 and right_source == left_source == [2] and
            right_all == left_all == [], "27-fibre side gate")

    powers = q3["canonical_roof_powers"]
    require([row["exponent"] for row in powers["rows"]] == [1, 2, 4, 5, 7, 8] and
            powers["canonicalized_each_step"] is True and
            powers["literal_power_words_retained"] is False,
            "fresh inverse canonical power gate")
    row7s = [row for row in powers["rows"] if row["exponent"] == 7]
    require(len(row7s) == 1, "fresh inverse exponent-seven gate")
    row7 = row7s[0]
    records = q3["correction_fibre"]["records"]
    certificate = q3["correction_fibre"]["certificate"]
    require(len(records) == certificate["order"] ==
            certificate["enumerated_count"] == 27 and
            certificate["all_words_coarse_identity"] is True,
            "fresh inverse correction fibre gate")
    base_source = source_words_m0(r07)
    base_values = [e4.eval(word) for word in base_source]
    base_key = [encode_element(value) for value in base_values]
    tested: list[int] = []
    passing: list[int] = []
    candidate_evaluations: list[dict[str, Any]] = []
    passing_payloads: dict[int, dict[str, Any]] = {}
    for index, record in enumerate(records, 1):
        candidate = reduce_word(row7["word"]+record["word"])
        inverse_words = source_words_m0(candidate)
        st_values, ts_values = direct_two_sided_residual_values(
            e4, base_source, inverse_words)
        st_identity = [value == e4.identity for value in st_values]
        ts_identity = [value == e4.identity for value in ts_values]
        passed = all(st_identity+ts_identity)
        tested.append(index)
        if passed:
            passing.append(index)
            passing_payloads[index] = {
                "candidate_word": candidate,
                "selected_inverse_words": inverse_words,
            }
        candidate_evaluations.append({
            "index_one_based": index,
            "correction_word_sha256": digest_obj(record["word"]),
            "candidate_word_length": len(candidate),
            "candidate_word_sha256": digest_obj(candidate),
            "source_words_m0_candidate": inverse_words,
            "source_words_m0_candidate_sha256": digest_obj(inverse_words),
            "ST_E4_values": [encode_element(value) for value in st_values],
            "TS_E4_values": [encode_element(value) for value in ts_values],
            "ST_identity_by_generator": st_identity,
            "TS_identity_by_generator": ts_identity,
            "all_twelve_residuals_identity": passed,
        })
    require(tested == list(range(1, 28)), "fresh inverse tested-index gate")
    selected = passing[0] if passing else None
    cache_entry = None
    if selected is not None:
        payload = passing_payloads[selected]
        cache_entry = {
            "source_key_kind": "exact ordered six E4 images of source_words_m0(R07)",
            "source_key_exact_six_E4_images": base_key,
            "source_key_sha256": digest_obj(base_key),
            "selection_policy": ("unique" if len(passing) == 1 else
                                 "deterministic first; full passing set retained"),
            "selected_correction_index_one_based": selected,
            **payload,
            "max_inverse_word_length": max(map(len, payload["selected_inverse_words"])),
            "direct_ST_and_TS_replay_identity": True,
        }
    inverse_fibre = {
        "base_source": base_source,
        "base_key": base_key,
        "row7": row7,
        "tested": tested,
        "passing": passing,
        "candidate_evaluations": candidate_evaluations,
        "cache_entry": cache_entry,
    }

    dictionary_count = dictionary_sha = seed_count = seed_sha = None
    if include_dictionary:
        dictionary = module.rebuild_dictionary(q3, e3)
        word_hashes = [digest_obj(word) for word in dictionary["words"]]
        require(len(word_hashes) == 4096 and digest_obj(word_hashes) ==
                DICTIONARY_SHA256, "4096 dictionary gate")
        dictionary_count = len(word_hashes)
        dictionary_sha = digest_obj(word_hashes)
        seed_count = len(dictionary["seed_words"])
        seed_sha = digest_obj(dictionary["seed_words"])
    return {
        "r07": r07, "old": old,
        "source_r07": encode_element(rv3), "source_old": encode_element(ov3),
        "cofaces_r07": [encode_element(value) for value in rv4],
        "cofaces_old": [encode_element(value) for value in ov4],
        "rhex_word_sha": [digest_obj(word) for word in rhex_words],
        "ohex_word_sha": [digest_obj(word) for word in ohex_words],
        "rhex": [encode_element(value) for value in rhex],
        "ohex": [encode_element(value) for value in ohex],
        "a18_r": encode_element(a18(e4, rv4)),
        "a18_o": encode_element(a18(e4, ov4)),
        "sign_canary": sign_canary(e4, rv4),
        "order_canary": order_canary(e4, rv4),
        "coordinate_rows": coordinate_rows,
        "right_source": right_source, "left_source": left_source,
        "right_all": right_all, "left_all": left_all,
        "source_diagnostics": source_diagnostics,
        "inverse_fibre": inverse_fibre,
        "dictionary_replayed": include_dictionary,
        "dictionary_count": dictionary_count,
        "dictionary_sha": dictionary_sha,
        "seed_count": seed_count,
        "seed_sha": seed_sha,
    }


def validate_receipt(data: dict[str, Any], q3: dict[str, Any],
                     expected: dict[str, Any]) -> None:
    require(data.get("schema") == SCHEMA, "schema gate")
    require(data.get("status") == data.get("terminal_token") == TERMINAL,
            "terminal gate")
    scope = data["scope"]
    require(scope["frozen_finite_616_branch_only"] is True and
            scope["abstract_profinite_F07C_identified"] is False and
            scope["fresh_R07_branch_rejected"] is False and
            scope["old_inheritance_rejected"] is True and
            scope["cross_checked_claimed"] is False and
            scope["Lean_verified"] is False, "scope gate")
    base = data["frozen_R07_base"]
    require(base["signed_word"] == expected["r07"] and
            base["word_length"] == 616 and
            base["word_sha256"] == R07_SHA256 and
            base["exponent_sums_xy"] == [108, -36] and base["m"] == 0,
            "base hash gate")
    audit = data["type_audit"]
    require(audit["old_selected_base"]["signed_word"] == expected["old"] and
            audit["old_selected_base"]["word_sha256"] == OLD_WORD_SHA256,
            "old base gate")
    source = audit["source_E3"]
    require(source["r07"] == expected["source_r07"] and
            source["old"] == expected["source_old"] and
            source["lossless_equal"] is False and
            source["coarse_equal"] is True and source["fine_equal"] is False and
            source["first_mismatch"] == {
                "coordinate": "E3.fine_pc_coords", "r07": [0, 0, 0, 0],
                "old": [0, 0, 0, 1]}, "E3 type gate")
    cofaces = audit["ordered_five_E4_cofaces"]
    require(cofaces["r07"] == expected["cofaces_r07"] and
            cofaces["old"] == expected["cofaces_old"] and
            cofaces["lossless_equal_by_slot"] == [False]*5 and
            cofaces["all_equal"] is False, "E4 coface gate")
    hexagon = audit["literal_hexagons"]
    require(hexagon["r07_word_sha256"] == expected["rhex_word_sha"] and
            hexagon["old_word_sha256"] == expected["ohex_word_sha"] and
            hexagon["r07_values"] == expected["rhex"] and
            hexagon["old_values"] == expected["ohex"] and
            hexagon["both_identity_for_both_bases"] is True,
            "hexagon gate")
    printed = audit["printed_A18"]
    require(printed["native_factor_order"] == "F*E*C*B^-1*A^-1" and
            printed["r07_value"] == expected["a18_r"] and
            printed["old_value"] == expected["a18_o"] and
            printed["both_identity"] is True, "A18 gate")
    require(audit["marked_quotients"]["G9_equality_classification"] ==
            "coarse equality only" and
            audit["marked_quotients"]["G36_not_present_in_legacy_E3"] is True,
            "G9/G36 type gate")
    settled = audit["marked_quotients"]["settled_R07_joint_factors"]
    require(settled == {
        "source": "independent GHA replay run 32808165839",
        "G36": [[4, 0], [32, 0], [0, 0]],
        "PSL2_8_identity": True,
        "p2_source_and_five_cofaces_identity": True,
        "p3_source_and_five_cofaces_identity": True,
        "old_20_letter_word_not_evaluated_in_that_receipt": True,
        "no_cross_type_inference": True}, "settled p target gate")

    fibre = data["coarse_q3_source_fibre"]
    require(fibre["classification"] == "complete coarse q3 source fibre only" and
            fibre["coordinate_records"] == expected["coordinate_rows"] and
            fibre["coordinate_records_sha256"] ==
            digest_obj(expected["coordinate_rows"]), "coarse fibre coordinate gate")
    sides = fibre["multiplication_sides"]
    require(sides["fixed_search_side"] == "right" and
            sides["right_source_match_indices"] == expected["right_source"] and
            sides["left_source_match_indices"] == expected["left_source"] and
            sides["right_source_plus_all_five_cofaces_match_indices"] ==
            expected["right_all"] and
            sides["left_source_plus_all_five_cofaces_match_indices"] ==
            expected["left_all"] and
            fibre["source_match_coface_diagnostic"] ==
            expected["source_diagnostics"], "multiplication side gate")

    inverse = data["fresh_R07_normalized_inverse_fibre"]
    inverse_expected = expected["inverse_fibre"]
    require(inverse["classification"] ==
            "registered 27-point compact positive inverse diagnostic" and
            inverse["base_source_words"] == inverse_expected["base_source"] and
            inverse["base_source_words_sha256"] ==
            digest_obj(inverse_expected["base_source"]) and
            inverse["base_source_key_exact_six_E4_images"] ==
            inverse_expected["base_key"] and
            inverse["base_source_key_sha256"] ==
            digest_obj(inverse_expected["base_key"]) and
            inverse["residual_evaluation_formulas"] == {
                "ST_i": "eval(T_i; S_1,...,S_6) * x_i^-1",
                "TS_i": "eval(S_i; T_1,...,T_6) * x_i^-1",
                "expanded_residual_words_materialized": False,
                "reason": "exact direct E4 evaluation avoids legacy bounded-word cap",
            } and
            inverse["canonical_exponent_seven_row"] == inverse_expected["row7"] and
            inverse["canonical_exponent_seven_row_sha256"] ==
            digest_obj(inverse_expected["row7"]) and
            inverse["tested_indices"] == inverse_expected["tested"] ==
            list(range(1, 28)) and
            inverse["passing_indices"] == inverse_expected["passing"] and
            inverse["passing_indices_sha256"] ==
            digest_obj(inverse_expected["passing"]) and
            inverse["candidate_evaluations"] ==
            inverse_expected["candidate_evaluations"] and
            inverse["candidate_evaluations_sha256"] ==
            digest_obj(inverse_expected["candidate_evaluations"]) and
            inverse["fresh_inverse_cache_entry"] ==
            inverse_expected["cache_entry"] and
            inverse["positive_inverse_available"] is
            (inverse_expected["cache_entry"] is not None) and
            inverse["negative_or_obstruction_claim_allowed"] is False,
            "fresh inverse fibre gate")

    dictionary = data["relative_dictionary"]
    require(dictionary["count"] == 4096 and
            dictionary["candidate_order_sha256"] == DICTIONARY_SHA256 and
            dictionary["full_J_H_fibre_complete"] is False and
            dictionary["full_J_H_over_J_Phi_complete"] is False and
            dictionary["negative_claim_allowed"] is False and
            dictionary["R07_full_sparse_scan_executed_here"] is False,
            "registered dictionary gate")
    if expected["dictionary_replayed"]:
        require(dictionary["count"] == expected["dictionary_count"] and
                dictionary["candidate_order_sha256"] == expected["dictionary_sha"] and
                dictionary["seed_count"] == expected["seed_count"] and
                dictionary["seed_manifest_sha256"] == expected["seed_sha"],
                "independent dictionary replay gate")
    mutations = data["mutations"]
    require(mutations["A18_inverse_sign"] == expected["sign_canary"],
            "A18 mutation gate")
    require(mutations["coface_order"] == expected["order_canary"],
            "coface order mutation gate")
    require(mutations["multiplication_side"] == {
        "expected": "right", "mutant": "left", "checker_must_reject": True},
        "side mutation declaration gate")
    require(mutations["fresh_inverse_residual"] == {
        "candidate_index_one_based": 1,
        "field": "ST_identity_by_generator[0]",
        "checker_must_reject": True}, "fresh inverse mutation declaration gate")
    require(data["fresh_R07_handoff"]["actual_residual_beta_constructed"] is False and
            data["fresh_R07_handoff"]["actual_arity_correction_map_constructed"] is False and
            data["fresh_R07_handoff"]["no_dimension_inference"] is True and
            data["fresh_R07_handoff"][
                "compact_27_inverse_diagnostic_empty_is_resource_blocker"] is False and
            data["fresh_R07_handoff"]["alternative_exact_onto_certificate_v88"][
                "heavy_Q4_generation_run_here"] is False and
            data["fresh_R07_handoff"]["alternative_exact_onto_certificate_v88"][
                "status"] == "UNKNOWN",
            "unbuilt handoff gate")
    retarget = data["target6_157em_retarget"]
    require(retarget["registered_108_is_full_universe"] is False and
            retarget["minimal_safe_terminal_before_rebuild"] ==
            "UNKNOWN, never obstruction" and
            retarget["change_points_sha256"] ==
            digest_obj(retarget["old_base_dependent_change_points"]),
            "157em retarget gate")
    require(data["negative_or_obstruction_claimed"] is False and
            data["claim_classification"] ==
            "typed_inheritance_mismatch; fresh branch remains UNKNOWN",
            "claim boundary gate")
    saved = data.get("self_digest_sha256")
    body = copy.deepcopy(data); body.pop("self_digest_sha256", None)
    require(saved == digest_obj(body), "self digest gate")


def expect_reject(data: dict[str, Any], q3: dict[str, Any], expected: dict[str, Any],
                  mutate: Any, label: str, intended_gate: str) -> dict[str, str]:
    bad = copy.deepcopy(data)
    mutate(bad)
    try:
        validate_receipt(bad, q3, expected)
    except CheckFailure as exc:
        require(intended_gate in str(exc), f"{label}: wrong rejection {exc}")
        return {"label": label, "intended_gate": intended_gate,
                "observed": str(exc)}
    raise CheckFailure(f"mutation accepted: {label}")


def run_mutations(data: dict[str, Any], q3: dict[str, Any],
                  expected: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    rows.append(expect_reject(
        data, q3, expected,
        lambda d: d["mutations"]["A18_inverse_sign"].__setitem__("factor", "MUTANT"),
        "A18 inverse/sign", "A18 mutation gate"))
    rows.append(expect_reject(
        data, q3, expected,
        lambda d: d["mutations"]["coface_order"].__setitem__("swap_zero_based", [0, 2]),
        "coface order", "coface order mutation gate"))
    rows.append(expect_reject(
        data, q3, expected,
        lambda d: d["coarse_q3_source_fibre"]["multiplication_sides"].__setitem__(
            "fixed_search_side", "left"),
        "multiplication side", "multiplication side gate"))
    rows.append(expect_reject(
        data, q3, expected,
        lambda d: d["coarse_q3_source_fibre"]["coordinate_records"][0][
            "artifact_ambient_Pi3_coords"].__setitem__(0, 1),
        "coarse fibre coordinate", "coarse fibre coordinate gate"))
    rows.append(expect_reject(
        data, q3, expected,
        lambda d: d["frozen_R07_base"].__setitem__("word_sha256", "0"*64),
        "base signed-list hash", "base hash gate"))
    rows.append(expect_reject(
        data, q3, expected,
        lambda d: d["type_audit"]["marked_quotients"][
            "settled_R07_joint_factors"].__setitem__(
                "p3_source_and_five_cofaces_identity", False),
        "settled p3 target", "settled p target gate"))
    rows.append(expect_reject(
        data, q3, expected,
        lambda d: d["fresh_R07_normalized_inverse_fibre"][
            "candidate_evaluations"][0]["ST_identity_by_generator"].__setitem__(
                0, not d["fresh_R07_normalized_inverse_fibre"][
                    "candidate_evaluations"][0]["ST_identity_by_generator"][0]),
        "fresh inverse residual", "fresh inverse fibre gate"))
    return rows


def self_test() -> None:
    require(exponent_sums(r07_word()) == [108, -36], "selftest word")
    require(len(literal_hexagons([])) == 2, "selftest formulas")
    print("R07_RELFRAT3_ACTUAL_CLASS_V1_CHECKER_SELFTEST_PASS "
          "stdlib_adapter=1 mutations=7 negative=0", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--mutations", action="store_true")
    parser.add_argument("--fibre-only", action="store_true",
                        help="skip the independent 4096-order rebuild")
    args = parser.parse_args()
    if args.self_test:
        self_test(); return 0
    q3_full = ROOT/Q3_PATH
    require(q3_full.is_file() and q3_full.stat().st_size == Q3_BYTES and
            digest_file(q3_full) == Q3_SHA256, "q3 pin gate")
    receipt_full = args.receipt if args.receipt.is_absolute() else ROOT/args.receipt
    require(receipt_full.is_file(), "receipt missing")
    q3 = json.loads(q3_full.read_text(encoding="utf-8"))
    data = json.loads(receipt_full.read_text(encoding="ascii"))
    expected = independent_expected(q3, include_dictionary=not args.fibre_only)
    validate_receipt(data, q3, expected)
    mutation_rows = run_mutations(data, q3, expected) if args.mutations else []
    print(f"{FINAL_MARKER} terminal={TERMINAL} mutations={len(mutation_rows)} "
          f"dictionary_replayed={str(not args.fibre_only).lower()} "
          f"receipt_sha256={digest_file(receipt_full)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
