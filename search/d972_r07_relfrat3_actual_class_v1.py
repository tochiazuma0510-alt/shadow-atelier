#!/usr/bin/env python3
"""Typed audit for the frozen 616-letter R07 relative-Frattini-3 branch.

This is a fail-closed adapter.  It authenticates the old q=3 receipt, rebuilds
the exact E3/E4 models through the frozen v9 implementation, compares the
literal R07 word with the old 20-letter base, and reconstructs the registered
4096-word positive dictionary.  The 27-element q=3 source fibre is audited
separately and is never promoted to the next J_H/J_Phi correction universe.

No sparse full-D2 search is run here.  A typed mismatch is a terminal for
inheritance only; it is not a rejection of a fresh R07 branch.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence


SCHEMA = "d972-r07-relfrat3-actual-class/v1"
TERMINAL = "R07_RELFRAT3_TYPE_MISMATCH_STOP"
FINAL_MARKER = "R07_RELFRAT3_ACTUAL_CLASS_V1_PRODUCER_PASS"
ROOT = Path(__file__).resolve().parents[1]
Q3_PATH = Path("ci/b345_157dp_artifacts_32171982444/d972_b345_q3_chief_v1.json")
Q3_BYTES = 231_570
Q3_SHA256 = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
LEGACY_PATH = Path("search/d972_b345_relfrat3_wordexpr_memo_v9.py")
LEGACY_BYTES = 392_086
LEGACY_SHA256 = "7dede323c3c52bc7cf7d99af6d542b3683823879a4bb3e340aca8ce53dcf196f"
LEGACY_CHECKER_PATH = Path("search/check_d972_b345_relfrat3_wordexpr_memo_v10.py")
LEGACY_CHECKER_BYTES = 410_844
LEGACY_CHECKER_SHA256 = "264258dcb945401e3db10ecd4fedd7a8dd79a8d7b0f31dbc0cfbe643537eac2d"
INDEPENDENT_OLD_CHECKER_PATH = Path("search/check_d972_b345_relfrat3_v1.py")
INDEPENDENT_OLD_CHECKER_BYTES = 52_315
INDEPENDENT_OLD_CHECKER_SHA256 = "3d86240237229b250943c4795c24c32ac75af9229534c73d16bd838f6d6d0101"
JOINT_PRODUCER_PATH = Path("search/d972_r07_p2_p3_joint_literal_producer_v1.g")
JOINT_PRODUCER_BYTES = 20_313
JOINT_PRODUCER_SHA256 = "598ffdf8fb185e92209da5ac4c59f0d187381e3e22b1e916ab32676203dee3f5"
JOINT_CHECKER_PATH = Path("crosscheck/check_d972_r07_p23_joint_literal_v1.py")
JOINT_CHECKER_BYTES = 32_201
JOINT_CHECKER_SHA256 = "56f479bbb17b0a7aa756ce79ce02dcccab5236b67ea85f90a90830f97e389bc2"
TARGET6_PRODUCER_PATH = Path("search/d972_b345_target6_dual_colgen_v1.py")
TARGET6_PRODUCER_BYTES = 410_757
TARGET6_PRODUCER_SHA256 = "8a3dd09811ec790b90f5f3d16890e9ef534a9fc0399597a0daa892605c58c8fc"
TARGET6_CHECKER_PATH = Path("search/check_d972_b345_target6_dual_colgen_v1.py")
TARGET6_CHECKER_BYTES = 228_980
TARGET6_CHECKER_SHA256 = "08cee7be18128b1dcc1376012854a828695c19a97bd1495e4cb0d7f7ddea035e"
DEFAULT_OUTPUT = Path("search/certs/d972_r07_relfrat3_actual_class_preflight_v1_20260826.json")

R07_SHA256 = "3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90"
R07_LENGTH = 616
OLD_WORD_SHA256 = "b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d"

# Embedded authoritative local words from the independent p2/p3 checker.
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


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


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


def pin(path: Path, size: int, sha256: str) -> dict[str, Any]:
    full = ROOT / path
    require(full.is_file(), f"missing pin: {path.as_posix()}")
    require(full.stat().st_size == size, f"byte drift: {path.as_posix()}")
    require(digest_file(full) == sha256, f"SHA drift: {path.as_posix()}")
    return {"path": path.as_posix(), "bytes": size, "sha256": sha256}


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(type(letter) is int and letter in (-2, -1, 1, 2),
                "signed F2 alphabet")
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


def r07_word() -> list[int]:
    # w23 = w2 * (w3^-1 * w2)^8, the balanced CRT exponent a=-8.
    discrepancy_inverse = reduce_word(inverse_word(W3) + list(W2))
    word = reduce_word(list(W2) + discrepancy_inverse * 8)
    require(len(word) == R07_LENGTH and digest_obj(word) == R07_SHA256,
            "frozen R07 reconstruction")
    return word


def exponent_sums(word: Sequence[int]) -> list[int]:
    return [sum((1 if x > 0 else -1) for x in word if abs(x) == i)
            for i in (1, 2)]


def load_legacy() -> Any:
    pin(LEGACY_PATH, LEGACY_BYTES, LEGACY_SHA256)
    path = ROOT / LEGACY_PATH
    spec = importlib.util.spec_from_file_location(
        "_d972_r07_relfrat3_legacy_v9_candidate", path)
    require(spec is not None and spec.loader is not None,
            "legacy module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def encode_element(value: Any) -> dict[str, Any]:
    permutation, fine = value
    one_line = [int(x)+1 for x in permutation]
    row = {"coarse_one_line": one_line, "fine_pc_coords": list(fine)}
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
    """Evaluate the twelve composition residuals without expanding huge words."""
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


def literal_hexagon_words(word: Sequence[int]) -> list[list[int]]:
    theta = substitute(word, ([2], [1]))
    tau = substitute(word, ([2], [-1, -2]))
    tau2 = substitute(tau, ([2], [-1, -2]))
    return [reduce_word(theta + list(word)),
            reduce_word(list(word) + tau + tau2)]


def printed_a18(quotient: Any, values: Sequence[Any]) -> Any:
    # Ordered cofaces are [C,A,E,B,F].  Native product is F*E*C*B^-1*A^-1.
    require(len(values) == 5, "A18 coface width")
    return product(quotient, [values[4], values[2], values[0],
                              quotient.inverse(values[3]),
                              quotient.inverse(values[1])])


def first_a18_sign_mutation(quotient: Any, values: Sequence[Any]) -> dict[str, Any]:
    factors = [values[4], values[2], values[0],
               quotient.inverse(values[3]), quotient.inverse(values[1])]
    labels = ["F", "E", "C", "B^-1", "A^-1"]
    for index in range(5):
        changed = list(factors)
        changed[index] = quotient.inverse(changed[index])
        value = product(quotient, changed)
        if value != quotient.identity:
            return {"factor_index_zero_based": index, "factor": labels[index],
                    "mutated_value": encode_element(value),
                    "rejected": True}
    raise AuditFailure("no detecting A18 sign mutation")


def first_coface_order_mutation(quotient: Any,
                                values: Sequence[Any]) -> dict[str, Any]:
    for left in range(5):
        for right in range(left+1, 5):
            changed = list(values)
            changed[left], changed[right] = changed[right], changed[left]
            value = printed_a18(quotient, changed)
            if value != quotient.identity:
                return {"swap_zero_based": [left, right],
                        "mutated_value": encode_element(value),
                        "rejected": True}
    raise AuditFailure("no detecting coface-order mutation")


def coarse_factors(encoded: dict[str, Any]) -> dict[str, Any]:
    row = encoded["coarse_one_line"]
    require(len(row) == 36, "Q0 degree")
    p = row[:9]
    g9 = [x-9 for x in row[9:]]
    require(sorted(p) == list(range(1, 10)) and
            sorted(g9) == list(range(1, 28)), "Q0 block decomposition")
    return {"P_degree9_one_line": p, "G9_degree27_one_line": g9,
            "factor_set": ["PSL(2,8)-degree9", "G9-degree27"],
            "not_G36": True}


def type_audit(module: Any, q3: dict[str, Any], r07: list[int],
               old_word: list[int]) -> tuple[dict[str, Any], dict[str, Any]]:
    e3, e4, _ = module.reconstruct_quotients(q3)
    context3 = [e3.generators[0], e3.generators[2]]
    coface_maps = module.cofaces(3)
    contexts4 = [(e4.eval(mapping[0]), e4.eval(mapping[2]))
                 for mapping in coface_maps]

    r07_e3 = e3.eval(r07, context3)
    old_e3 = e3.eval(old_word, context3)
    r07_e4 = [e4.eval(r07, context) for context in contexts4]
    old_e4 = [e4.eval(old_word, context) for context in contexts4]
    r07_hex_words = literal_hexagon_words(r07)
    old_hex_words = literal_hexagon_words(old_word)
    r07_hex = [e3.eval(word, context3) for word in r07_hex_words]
    old_hex = [e3.eval(word, context3) for word in old_hex_words]
    r07_a18 = printed_a18(e4, r07_e4)
    old_a18 = printed_a18(e4, old_e4)
    require(r07_hex == [e3.identity, e3.identity] and
            old_hex == [e3.identity, e3.identity], "literal hexagon replay")
    require(r07_a18 == e4.identity and old_a18 == e4.identity,
            "printed A18 replay")

    encoded_r07_e3, encoded_old_e3 = map(encode_element, (r07_e3, old_e3))
    encoded_r07_e4 = [encode_element(value) for value in r07_e4]
    encoded_old_e4 = [encode_element(value) for value in old_e4]
    equality_by_coface = [left == right for left, right in zip(r07_e4, old_e4)]
    require(r07_e3[0] == old_e3[0] and r07_e3[1] != old_e3[1],
            "expected first typed mismatch")
    require(not any(equality_by_coface), "expected five E4 mismatches")

    audit = {
        "old_selected_base": {
            "signed_word": old_word,
            "word_length": len(old_word),
            "word_sha256": digest_obj(old_word),
            "exponent_sums_xy": exponent_sums(old_word),
            "q3_row_one_based": 37,
            "q3_row_zero_based": 36,
        },
        "source_E3": {
            "r07": encoded_r07_e3,
            "old": encoded_old_e3,
            "lossless_equal": r07_e3 == old_e3,
            "coarse_equal": r07_e3[0] == old_e3[0],
            "fine_equal": r07_e3[1] == old_e3[1],
            "first_mismatch": {
                "coordinate": "E3.fine_pc_coords",
                "r07": list(r07_e3[1]), "old": list(old_e3[1]),
            },
        },
        "ordered_five_E4_cofaces": {
            "slot_order": [0, 1, 2, 3, 4],
            "semantic_order": ["C", "A", "E", "B", "F"],
            "r07": encoded_r07_e4,
            "old": encoded_old_e4,
            "lossless_equal_by_slot": equality_by_coface,
            "all_equal": all(equality_by_coface),
        },
        "literal_hexagons": {
            "formulas": ["theta(f)*f", "f*tau(f)*tau^2(f)"],
            "r07_word_sha256": [digest_obj(word) for word in r07_hex_words],
            "old_word_sha256": [digest_obj(word) for word in old_hex_words],
            "r07_values": [encode_element(value) for value in r07_hex],
            "old_values": [encode_element(value) for value in old_hex],
            "both_identity_for_both_bases": True,
        },
        "printed_A18": {
            "coface_semantic_order": ["C", "A", "E", "B", "F"],
            "native_factor_order": "F*E*C*B^-1*A^-1",
            "r07_value": encode_element(r07_a18),
            "old_value": encode_element(old_a18),
            "both_identity": True,
        },
        "marked_quotients": {
            "legacy_E3_coarse_factors_r07": coarse_factors(encoded_r07_e3),
            "legacy_E3_coarse_factors_old": coarse_factors(encoded_old_e3),
            "G9_equality_classification": "coarse equality only",
            "G36_not_present_in_legacy_E3": True,
            "settled_R07_joint_factors": {
                "source": "independent GHA replay run 32808165839",
                "G36": [[4, 0], [32, 0], [0, 0]],
                "PSL2_8_identity": True,
                "p2_source_and_five_cofaces_identity": True,
                "p3_source_and_five_cofaces_identity": True,
                "old_20_letter_word_not_evaluated_in_that_receipt": True,
                "no_cross_type_inference": True,
            },
        },
    }
    audit["audit_sha256"] = digest_obj(audit)
    mutations = {
        "A18_inverse_sign": first_a18_sign_mutation(e4, r07_e4),
        "coface_order": first_coface_order_mutation(e4, r07_e4),
    }
    return audit, {"e3": e3, "e4": e4, "context3": context3,
                   "contexts4": contexts4, "r07_e3": r07_e3,
                   "old_e3": old_e3, "r07_e4": r07_e4,
                   "old_e4": old_e4, "mutations": mutations}


def coarse_fibre_audit(module: Any, q3: dict[str, Any],
                       state: dict[str, Any]) -> dict[str, Any]:
    e3, e4 = state["e3"], state["e4"]
    context3, contexts4 = state["context3"], state["contexts4"]
    r07_e3, old_e3 = state["r07_e3"], state["old_e3"]
    r07_e4, old_e4 = state["r07_e4"], state["old_e4"]
    correction = q3["correction_fibre"]
    certificate = correction["certificate"]
    records = correction["records"]
    require(certificate["order"] == certificate["enumerated_count"] == 27 and
            certificate["projection_kernel_order"] == 27 and
            certificate["all_words_coarse_identity"] is True and
            certificate["all_q3_coordinates_unique"] is True and
            len(records) == 27, "q3 coarse fibre certificate")
    coordinate_rows = []
    source_values = []
    right_source_matches: list[int] = []
    left_source_matches: list[int] = []
    right_all_matches: list[int] = []
    left_all_matches: list[int] = []
    source_match_coface_rows = []
    for index, record in enumerate(records, 1):
        word = record["word"]
        value3 = e3.eval(word, context3)
        values4 = [e4.eval(word, context) for context in contexts4]
        require(value3[0] == e3.identity[0],
                f"correction coarse source identity {index}")
        require(list(value3[1]) == record["ambient_Pi3_coords"],
                f"correction fine coordinates {index}")
        source_values.append(value3)
        coordinate_rows.append({
            "index_one_based": index,
            "word_length": len(word), "word_sha256": digest_obj(word),
            "artifact_ambient_Pi3_coords": record["ambient_Pi3_coords"],
            "direct_source_value": encode_element(value3),
            "coface_values_sha256": digest_obj(
                [encode_element(value) for value in values4]),
        })
        right3 = e3.mul(r07_e3, value3)
        left3 = e3.mul(value3, r07_e3)
        right4 = [e4.mul(base, corr) for base, corr in zip(r07_e4, values4)]
        left4 = [e4.mul(corr, base) for base, corr in zip(r07_e4, values4)]
        if right3 == old_e3:
            right_source_matches.append(index)
        if left3 == old_e3:
            left_source_matches.append(index)
        if right3 == old_e3 and right4 == old_e4:
            right_all_matches.append(index)
        if left3 == old_e3 and left4 == old_e4:
            left_all_matches.append(index)
        if right3 == old_e3 or left3 == old_e3:
            source_match_coface_rows.append({
                "index_one_based": index,
                "right_equal_by_coface": [a == b for a, b in zip(right4, old_e4)],
                "left_equal_by_coface": [a == b for a, b in zip(left4, old_e4)],
                "correction_coarse_identity_by_coface": [
                    value[0] == e4.identity[0] for value in values4],
                "correction_fine_pc_coords_by_coface": [
                    list(value[1]) for value in values4],
            })
    require(len(set(source_values)) == 27, "q3 source value uniqueness")
    require(right_source_matches == [2] and left_source_matches == [2] and
            right_all_matches == [] and left_all_matches == [],
            "coarse fibre reindex result")
    return {
        "classification": "complete coarse q3 source fibre only",
        "explicitly_not": ["complete J_H/J_Phi correction universe",
                           "relative-Frattini obstruction universe"],
        "indexing": "one-based artifact order 1..27",
        "certificate": certificate,
        "coordinate_records": coordinate_rows,
        "coordinate_records_sha256": digest_obj(coordinate_rows),
        "multiplication_sides": {
            "fixed_search_side": "right",
            "right_candidate_word": "reduce(r07 || correction)",
            "left_diagnostic_word": "reduce(correction || r07)",
            "right_source_match_indices": right_source_matches,
            "left_source_match_indices": left_source_matches,
            "right_source_plus_all_five_cofaces_match_indices": right_all_matches,
            "left_source_plus_all_five_cofaces_match_indices": left_all_matches,
        },
        "source_match_coface_diagnostic": source_match_coface_rows,
        "inheritance_result": "no single old coarse-fibre word aligns E3 and all five E4 cofaces",
    }


def fresh_inverse_fibre_audit(module: Any, q3: dict[str, Any],
                              r07: list[int], e4: Any) -> dict[str, Any]:
    """Replay the registered 27 exponent-seven inverse diagnostics on R07.

    This deliberately copies only the mathematical recipe of the legacy
    normalized-inverse scan.  Passing is a compact positive certificate;
    failure is not an onto obstruction (see the alternative Goursat/Burnside
    handoff recorded in the receipt).
    """
    powers = q3["canonical_roof_powers"]
    rows = powers["rows"]
    require([row["exponent"] for row in rows] == [1, 2, 4, 5, 7, 8] and
            powers["canonicalized_each_step"] is True and
            powers["literal_power_words_retained"] is False,
            "fresh inverse canonical power receipt")
    row7s = [row for row in rows if row["exponent"] == 7]
    require(len(row7s) == 1, "fresh inverse exponent-seven row")
    row7 = row7s[0]
    correction = q3["correction_fibre"]
    records = correction["records"]
    certificate = correction["certificate"]
    require(len(records) == certificate["order"] ==
            certificate["enumerated_count"] == 27 and
            certificate["all_words_coarse_identity"] is True,
            "fresh inverse authenticated 27 fibre")

    base_source = module.source_words_m0(r07)
    require(len(base_source) == 6, "fresh inverse source arity")
    base_values = [e4.eval(word) for word in base_source]
    base_key = [encode_element(value) for value in base_values]
    tested: list[int] = []
    passing: list[int] = []
    candidate_rows: list[dict[str, Any]] = []
    passing_payloads: dict[int, dict[str, Any]] = {}
    for index, record in enumerate(records, 1):
        candidate = module.reduce_word(row7["word"] + record["word"])
        inverse_words = module.source_words_m0(candidate)
        st_values, ts_values = direct_two_sided_residual_values(
            e4, base_source, inverse_words)
        require(len(inverse_words) == len(st_values) == len(ts_values) == 6,
                f"fresh inverse residual arity {index}")
        st_identity = [value == e4.identity for value in st_values]
        ts_identity = [value == e4.identity for value in ts_values]
        passed = all(st_identity + ts_identity)
        tested.append(index)
        if passed:
            passing.append(index)
            passing_payloads[index] = {
                "candidate_word": candidate,
                "selected_inverse_words": inverse_words,
            }
        candidate_rows.append({
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
    require(tested == list(range(1, 28)), "fresh inverse full 1..27 test")

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
    return {
        "classification": "registered 27-point compact positive inverse diagnostic",
        "explicitly_not": ["necessary onto condition", "complete inverse universe",
                           "relative-Frattini obstruction universe"],
        "base_source_definition": "source_words_m0(frozen_R07_616)",
        "base_source_words": base_source,
        "base_source_words_sha256": digest_obj(base_source),
        "base_source_key_exact_six_E4_images": base_key,
        "base_source_key_sha256": digest_obj(base_key),
        "residual_evaluation_formulas": {
            "ST_i": "eval(T_i; S_1,...,S_6) * x_i^-1",
            "TS_i": "eval(S_i; T_1,...,T_6) * x_i^-1",
            "expanded_residual_words_materialized": False,
            "reason": "exact direct E4 evaluation avoids legacy bounded-word cap",
        },
        "normalized_exponent": 7,
        "normalized_roof_order": 9,
        "canonical_exponent_seven_row": row7,
        "canonical_exponent_seven_row_sha256": digest_obj(row7),
        "correction_fibre_size": 27,
        "tested_indices": tested,
        "passing_indices": passing,
        "passing_indices_sha256": digest_obj(passing),
        "candidate_evaluations": candidate_rows,
        "candidate_evaluations_sha256": digest_obj(candidate_rows),
        "fresh_inverse_cache_entry": cache_entry,
        "positive_inverse_available": cache_entry is not None,
        "empty_means": (None if passing else
                        "no inverse in this registered 27-point family; onto remains UNKNOWN"),
        "negative_or_obstruction_claim_allowed": False,
    }


def dictionary_audit(module: Any, q3: dict[str, Any], e3: Any) -> dict[str, Any]:
    dictionary = module.correction_dictionary(q3, e3)
    words = dictionary["words"]
    require(len(words) == dictionary["count"] == 4096 and words[0] == [],
            "registered 4096 dictionary")
    word_hashes = [digest_obj(word) for word in words]
    require(digest_obj(word_hashes) ==
            "3410bbab776fbe1da267d3c3932bf63f9e09bdd02415ee82926619e312d7bbf5",
            "frozen 4096 candidate order")
    return {
        "classification": "registered positive semidecision dictionary",
        "count": 4096,
        "candidate_order": "identity then BFS products of signed authenticated seeds",
        "candidate_order_sha256": digest_obj(word_hashes),
        "seed_count": len(dictionary["seed_words"]),
        "seed_manifest_sha256": digest_obj(dictionary["seed_words"]),
        "parent_edge_provenance_sha256": dictionary["provenance_sha256"],
        "all_words_E3_kernel_by_recurrence": True,
        "all_words_free_exponent_zero": True,
        "full_J_H_fibre_complete": False,
        "full_J_H_over_J_Phi_complete": False,
        "negative_claim_allowed": False,
        "old_run_32261068150_terminal": "B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE",
        "old_run_claim_classification": "unknown_not_obstruction",
        "R07_full_sparse_scan_executed_here": False,
    }


def target6_retarget_manifest() -> dict[str, Any]:
    rows = [
        ["target6 word injection", "search/d972_b345_target6_dual_colgen_v1.py:951",
         "replace old.FIXED_WORD in r0 and all 108 delta words by the exact 616 base; regenerate all word/gradient hashes"],
        ["authenticated base replay", "search/d972_b345_target6_dual_colgen_v1.py:5649",
         "old.replay_base_q3 is old-20-word typed and cannot authenticate R07"],
        ["inverse tuple", "search/d972_b345_target6_dual_colgen_v1.py:5650",
         "old.normalized_inverse_fibre belongs to the old source endomorphism; construct and replay a fresh R07 inverse"],
        ["source preflight", "search/d972_b345_target6_dual_colgen_v1.py:5662",
         "recompute raw_source_key, inverse_words, 31 correction contexts, and all source occurrence identities"],
        ["fixed B1", "search/d972_b345_target6_dual_colgen_v1.py:5712",
         "do not reuse frozen lex-first B1 block/dual hashes; rebuild from B0 for the new RHS"],
        ["initial affine RHS", "search/d972_b345_target6_dual_colgen_v1.py:5742",
         "recompute target6 system, 109 raw gradients/remainders, dual, parent manifest, and recovery map"],
        ["receipt validator", "search/d972_b345_target6_dual_colgen_v1.py:5194",
         "replace hard-coded old 20-letter base and every dependent stable digest with versioned R07 fields"],
        ["independent checker", "search/check_d972_b345_target6_dual_colgen_v1.py",
         "repeat all preceding reconstruction independently; do not import the new producer helper"],
    ]
    return {
        "runner": "157em full-D2 target-6 dual column generation",
        "old_base_dependent_change_points": rows,
        "change_points_sha256": digest_obj(rows),
        "reusable_only_after_retyping": [
            "generic B0 presentation columns and semantic translation engine",
            "dual reverse-lift/correlation/complete-11-column transaction logic",
            "registered 108 seed family as a positive family only",
        ],
        "not_reusable_as_frozen_data": [
            "old base replay", "old normalized inverse tuple",
            "fixed B1 block and dual", "old target6 RHS/remainders/hashes",
        ],
        "registered_108_is_full_universe": False,
        "minimal_safe_terminal_before_rebuild": "UNKNOWN, never obstruction",
    }


def build_receipt() -> dict[str, Any]:
    pins = {
        "q3_artifact": pin(Q3_PATH, Q3_BYTES, Q3_SHA256),
        "legacy_v9_producer": pin(LEGACY_PATH, LEGACY_BYTES, LEGACY_SHA256),
        "legacy_v10_checker": pin(LEGACY_CHECKER_PATH, LEGACY_CHECKER_BYTES,
                                    LEGACY_CHECKER_SHA256),
        "independent_old_v1_checker": pin(
            INDEPENDENT_OLD_CHECKER_PATH, INDEPENDENT_OLD_CHECKER_BYTES,
            INDEPENDENT_OLD_CHECKER_SHA256),
        "joint_p23_producer": pin(JOINT_PRODUCER_PATH, JOINT_PRODUCER_BYTES,
                                   JOINT_PRODUCER_SHA256),
        "joint_p23_independent_checker": pin(JOINT_CHECKER_PATH,
                                               JOINT_CHECKER_BYTES,
                                               JOINT_CHECKER_SHA256),
        "target6_157em_producer": pin(TARGET6_PRODUCER_PATH,
                                       TARGET6_PRODUCER_BYTES,
                                       TARGET6_PRODUCER_SHA256),
        "target6_157em_checker": pin(TARGET6_CHECKER_PATH,
                                      TARGET6_CHECKER_BYTES,
                                      TARGET6_CHECKER_SHA256),
    }
    module = load_legacy()
    q3 = json.loads((ROOT/Q3_PATH).read_text(encoding="utf-8"))
    require(q3["schema"] == "d972-b345-q-chief/v1" and
            q3["terminal_token"] ==
            "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION",
            "q3 artifact terminal")
    r07 = r07_word()
    old_word = list(q3["selected_solution"]["typed_source_word"])
    require(len(old_word) == 20 and digest_obj(old_word) == OLD_WORD_SHA256,
            "old selected word")
    audit, state = type_audit(module, q3, r07, old_word)
    fibre = coarse_fibre_audit(module, q3, state)
    inverse_fibre = fresh_inverse_fibre_audit(module, q3, r07, state["e4"])
    dictionary = dictionary_audit(module, q3, state["e3"])
    positive_inverse = inverse_fibre["positive_inverse_available"]
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "date": "20260826",
        "role": "Luna mechanical typed audit; candidate grade",
        "status": TERMINAL,
        "terminal_token": TERMINAL,
        "scope": {
            "frozen_finite_616_branch_only": True,
            "abstract_profinite_F07C_identified": False,
            "fresh_R07_branch_rejected": False,
            "old_inheritance_rejected": True,
            "arithmetic_or_fake_or_Ihara_claimed": False,
            "cofinal_or_all972_claimed": False,
            "cross_checked_claimed": False,
            "Lean_verified": False,
        },
        "pins": pins,
        "frozen_R07_base": {
            "construction": "w2*(w3^-1*w2)^8",
            "balanced_CRT_exponent": -8,
            "signed_word": r07,
            "word_length": len(r07),
            "word_sha256": digest_obj(r07),
            "exponent_sums_xy": exponent_sums(r07),
            "m": 0,
        },
        "type_audit": audit,
        "coarse_q3_source_fibre": fibre,
        "fresh_R07_normalized_inverse_fibre": inverse_fibre,
        "relative_dictionary": dictionary,
        "mutations": {
            **state["mutations"],
            "multiplication_side": {"expected": "right", "mutant": "left",
                                      "checker_must_reject": True},
            "coarse_fibre_coordinate": {"index_one_based": 1,
                                          "checker_must_reject": True},
            "base_hash": {"expected": R07_SHA256,
                            "checker_must_reject": True},
            "settled_p_target": {"field": "p3_source_and_five_cofaces_identity",
                                   "checker_must_reject": True},
            "fresh_inverse_residual": {
                "candidate_index_one_based": 1,
                "field": "ST_identity_by_generator[0]",
                "checker_must_reject": True,
            },
        },
        "fresh_R07_handoff": {
            "registered_4096_positive_scan_ready_without_retyping": False,
            "registered_4096_or_target6_retarget_has_exact_inverse_input":
                positive_inverse,
            "first_missing_typed_items": [
                "fresh finite-derived/charming witness for the R07 E4 five-coface tuple",
                "new base-specific target gradients and saturated-prefix canaries",
                "proof that a finite J_H/J_Phi correction quotient is complete (needed only for a negative terminal)",
            ] + ([] if positive_inverse else [
                "optional compact inverse witness in the registered 27-point family (not an onto necessity)"]),
            "compact_27_inverse_diagnostic_positive": positive_inverse,
            "compact_27_inverse_diagnostic_empty_is_resource_blocker": False,
            "alternative_exact_onto_certificate_v88": {
                "grade": "GHA-ready design; unexecuted here",
                "ambient": "E4=Q4 x Pi4[3]",
                "Q4_abelianization_order": 32,
                "conditions": [
                    "literal source tuple kills the 11 PB4 relators",
                    "literal source tuple projects onto Q4",
                    "literal source tuple spans Pi4[3]/Phi(Pi4[3]) over F3",
                ],
                "conclusion_if_all_three_hold":
                    "E4 generation and hence automorphism by Goursat plus Burnside",
                "heavy_Q4_generation_run_here": False,
                "status": "UNKNOWN",
            },
            "left_Fox_is_ordered_arity_coface_differential": False,
            "actual_residual_beta_constructed": False,
            "actual_arity_correction_map_constructed": False,
            "B1_literal_cocycle_zF": "UNBUILT",
            "B2_H_nulling_cochain_aH": "UNBUILT",
            "B3_chain_level_cyclic_comparison": "UNBUILT",
            "B4_relative_pair_class": "UNBUILT",
            "no_dimension_inference": True,
        },
        "target6_157em_retarget": target6_retarget_manifest(),
        "claim_classification": "typed_inheritance_mismatch; fresh branch remains UNKNOWN",
        "negative_or_obstruction_claimed": False,
    }
    receipt["self_digest_sha256"] = digest_obj(receipt)
    return receipt


def checked_write(path: Path, receipt: dict[str, Any]) -> None:
    full = path if path.is_absolute() else ROOT/path
    full.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical_bytes(receipt) + b"\n"
    if full.exists():
        require(full.read_bytes() == raw, f"immutable output mismatch: {full}")
    else:
        full.write_bytes(raw)
    require(full.read_bytes() == raw, "receipt readback")


def self_test() -> None:
    word = r07_word()
    require(exponent_sums(word) == [108, -36], "R07 exponent sums")
    require(len(literal_hexagon_words([])) == 2, "hexagon arity")
    require(printed_a18 is not None and target6_retarget_manifest()[
            "registered_108_is_full_universe"] is False, "static boundary")
    print("R07_RELFRAT3_ACTUAL_CLASS_V1_PRODUCER_SELFTEST_PASS "
          "word=616 terminal=type_mismatch negative=0", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    require(args.preflight, "use --preflight for the bounded typed audit")
    receipt = build_receipt()
    checked_write(args.output, receipt)
    full = args.output if args.output.is_absolute() else ROOT/args.output
    print(f"{FINAL_MARKER} terminal={TERMINAL} "
          f"output={args.output.as_posix()} bytes={full.stat().st_size} "
          f"sha256={digest_file(full)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
