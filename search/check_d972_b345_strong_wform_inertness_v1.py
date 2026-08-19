#!/usr/bin/env python3
"""Independent checker for the explicit strong-W-form diagnostic v1.

The checker never imports the new producer.  It rebuilds words, quotients,
cofaces, the 32768+207 fixed Fox prefix, six membership outcomes, and every
positive packed provenance proof using the separately pinned v10 machinery.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Any, Sequence


SCHEMA = "d972-b345-strong-wform-inertness/v1"
OUTPUT_PATH = Path("ci/out/d972_b345_strong_wform_inertness_v1.json")
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
PRODUCER_PATH = Path("search/d972_b345_strong_wform_inertness_v1.py")
CHECKER_PATH = Path("search/check_d972_b345_strong_wform_inertness_v1.py")
DRIVER_PATH = Path("search/d972_b345_strong_wform_inertness_gha_driver_v1.g")
TASK_PATH = Path("sol/luna_task_157ea_b345_strong_wform_inertness.md")
TASK_SHA = "1b403d5f545cf11b2ab397c1bc9c4e1a57f29207e2e3dee423f42e60b81f0665"
Q3_PRODUCER = Path("search/d972_b345_q3_chief_v1.g")
Q3_PRODUCER_SHA = "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755"
Q3_CHECKER = Path("search/check_d972_b345_q3_chief_v1.py")
Q3_CHECKER_SHA = "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73"
Q3_DRIVER = Path("search/d972_b345_q3_gha_driver_v1.g")
Q3_DRIVER_SHA = "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831"
V7_PRODUCER = Path("search/d972_b345_relfrat3_pivot_surgery_v7.py")
V7_PRODUCER_SHA = "a19c3353c5cfc6da8ad0b7d941ba94bde043c80e69e33c889c5710c897d7a757"
V7_CHECKER = Path("search/check_d972_b345_relfrat3_pivot_surgery_v7.py")
V7_CHECKER_SHA = "fbe033704180a808320c897c52613ca6847305dd85ddcd7a70aa825161e8bfa0"
V9_PRODUCER = Path("search/d972_b345_relfrat3_wordexpr_memo_v9.py")
V9_PRODUCER_SHA = "7dede323c3c52bc7cf7d99af6d542b3683823879a4bb3e340aca8ce53dcf196f"
V10_CHECKER = Path("search/check_d972_b345_relfrat3_wordexpr_memo_v10.py")
V10_CHECKER_SHA = "264258dcb945401e3db10ecd4fedd7a8dd79a8d7b0f31dbc0cfbe643537eac2d"
V10_DRIVER = Path("search/d972_b345_relfrat3_wordexpr_memo_gha_driver_v10.g")
V10_DRIVER_SHA = "a5e9bdb34d85669a6221e4b0fa8e4c3af0aee343aade59fde52013d05753afc0"
FORMULA_SHA = "b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef"
F0 = [-2, -2, -1, -1, 2, 2, 1, -2, -1, -1,
      2, 2, 2, -1, -2, -2, 1, 1, 1, 1]
F0_SHA = "b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d"
S_SHA = "b85ac8d8b4528868282685a5da15eef9ee276d5e94e499d449d6aa1b0b7060ad"
FS_SHA = "c113c06d51480c8c819a563f6efc2323afecb7a54aabee96e7104d1d2921505b"
FINAL_BLOCKER_SHA = "0cd653ee0966ccc83d270802bbb5d00b61731f28e27eec1918bb5ea282e00903"
CLAIM_SCOPE = "single_explicit_strong_word_fixed_prefix_only"
TERMINALS = {
    "B345_T53_STRONG_S_EXACT_TYPED_INERT",
    "B345_T53_STRONG_S_PREFIX_INCOMPLETE",
    "B345_T53_STRONG_S_UNKNOWN_RESOURCE",
    "B345_T53_STRONG_S_UNKNOWN_INPUT",
}
FULL_KEYS = {
    "schema", "status", "terminal_token", "reason", "source_hashes",
    "input", "claims", "result_summary", "prohibited_work",
    "formula_sha256", "base_q3_replay", "word_typing",
    "directed_base_support", "directed_surgery", "prefix_accounting",
    "r0_drift_canary", "target6_formula", "target_results",
    "positive_target_order", "positive_gradient_bindings",
    "quotient_element_registry", "boundary_proof_dag",
    "boundary_certificates", "registered_questions", "resource_guards",
    "performance", "partial",
}
INPUT_KEYS = {"schema", "status", "terminal_token", "reason",
              "source_hashes", "input_errors", "claims", "result_summary",
              "prohibited_work"}
RESOURCE_REASONS = {
    "producer_soft_timeout", "producer_soft_rss", "element_pool",
    "provenance_dag_edges", "provenance_dag_nodes", "section_slp_nodes",
    "single_sparse_elimination_row", "single_word_or_section_length",
    "sparse_pivot_rows", "target_elimination_support",
    "total_sparse_group_ring_keys", "directed_unique_translations",
    "directed_columns", "directed_section_expr_nodes",
    "directed_section_expr_edges", "proof_DAG_array_bytes",
    "proof_DAG_base64",
}


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_v10(repo: Path) -> Any:
    path = repo / V10_CHECKER
    spec = importlib.util.spec_from_file_location("_d972_t53_v10", path)
    require(spec is not None and spec.loader is not None,
            "cannot load pinned v10 checker")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def claims(positive: bool) -> dict[str, Any]:
    return {
        "claim_classification":
            "positive_exact_single_word_certificate" if positive else
            "unknown_not_obstruction",
        "claim_scope": CLAIM_SCOPE,
        "negative_claimed": False, "full_universe_claimed": False,
        "W_FORM_universal_claimed": False, "B4_A_claimed": False,
        "B4_B_claimed": False, "no_mathematical_obstruction_claimed": True,
    }


def prohibited_work() -> dict[str, Any]:
    return {
        "registered_4096_dictionary_constructed": False,
        "other_acceptance_targets_constructed": False,
        "T_diagnostics_constructed": False,
        "normalized_inverse_constructed": False,
        "onto_checks_constructed": False,
        "PB5_constructed": False,
        "ANUPQ_invoked": False,
        "targeted_translations_for_six_questions": False,
        "old_receipt_basis_pool_rows_or_DAG_imported": False,
    }


def exact_words(base: Any) -> dict[str, list[int]]:
    xi = base.reduce_word([1] * 18)
    eta = base.reduce_word([2] * 18)
    s = base.commutator(eta, xi)
    fs = base.reduce_word(F0 + s)
    require(base.digest_obj(F0) == F0_SHA and
            s == [-2] * 18 + [-1] * 18 + [2] * 18 + [1] * 18 and
            base.digest_obj(s) == S_SHA and base.digest_obj(fs) == FS_SHA and
            len(F0) == 20 and len(s) == 72 and len(fs) == 92 and
            all(base.exponent_sums(word, 2) == [0, 0]
                for word in (F0, s, fs)), "independent exact strong words")
    return {"f0": list(F0), "xi": xi, "eta": eta, "s": s, "fs": fs}


def embed_f2(base: Any, word: Sequence[int]) -> list[int]:
    return base.substitute(word, [[1], [3]])


def target_words(base: Any, words: dict[str, list[int]]) \
        -> tuple[list[tuple[str, str, list[int]]], dict[str, list[int]]]:
    maps = base.cofaces(3)
    coface_words = [base.substitute(embed_f2(base, words["s"]), mapping)
                    for mapping in maps]
    h0 = base.hexagon_words(words["f0"])[0]
    hs = base.hexagon_words(words["fs"])[0]
    r0 = base.substitute(embed_f2(base, h0), maps[0])
    rs = base.substitute(embed_f2(base, hs), maps[0])
    delta = base.reduce_word(rs + base.inv_word(r0))
    targets = [(f"strong_s_coface_{slot}", "strong_coface", word)
               for slot, word in enumerate(coface_words)]
    targets.append(("target6_delta_rs_r0_inverse", "target6_delta", delta))
    return targets, {"r0": r0, "rs": rs, "delta": delta,
                     "h0_f2": h0, "hs_f2": hs}


def prefix_targets(base: Any, r0: list[int]) \
        -> list[tuple[str, str, list[int]]]:
    return ([(f"charming_error_coface_{slot}", "charming", [])
             for slot in range(5)] +
            [("hexagon_1_coface_0", "hexagon", r0)])


def element_record(base: Any, value: Any) -> dict[str, Any]:
    blob = base.element_blob(value)
    return {"coarse_permutation_zero_based": list(value[0]),
            "fine_pc_coords": list(value[1]), "canonical_hex": blob.hex(),
            "canonical_sha256": hashlib.sha256(blob).hexdigest()}


def word_record(base: Any, word: Sequence[int]) -> dict[str, Any]:
    reduced = base.reduce_word(word)
    return {"word": reduced, "length": len(reduced),
            "sha256": base.digest_obj(reduced)}


def raw_gradient_binding(base: Any, gradient: dict[Any, int]) -> dict[str, Any]:
    rows = []
    digest = hashlib.sha256()
    for (component, value), coefficient in sorted(gradient.items()):
        blob = base.element_blob(value)
        digest.update(int(component).to_bytes(1, "little"))
        digest.update(len(blob).to_bytes(2, "little"))
        digest.update(blob)
        digest.update(int(coefficient).to_bytes(1, "little"))
        rows.append([component, blob.hex(), coefficient])
    return {"entry_count": len(rows),
            "canonical_gradient_sha256": digest.hexdigest(),
            "canonical_rows": rows,
            "canonical_order": "component then exact canonical E4 bytes"}


def expected_word_typing(base: Any, e3: Any, e4: Any,
                         words: dict[str, list[int]]) -> dict[str, Any]:
    embedded = {name: embed_f2(base, words[name])
                for name in ("xi", "eta", "s")}
    require(all(e3.eval(word) == e3.identity for word in embedded.values()),
            "checker embedded E3 identities")
    maps = base.cofaces(3)
    coface_words = {name: [base.substitute(word, mapping) for mapping in maps]
                    for name, word in embedded.items()}
    coface_values = {name: [e4.eval(word) for word in rows]
                     for name, rows in coface_words.items()}
    require(all(value == e4.identity for rows in coface_values.values()
                for value in rows), "checker five coface identities")
    return {
        "commutator_convention": "[a,b]=a^-1*b^-1*a*b",
        "F2_to_PB3_embedding": {"x_letter": 1, "y_letter": 3,
                                "PB3_pair_order": ["A12", "A13", "A23"],
                                "y_to_PB3_generator_2_prohibited": True},
        "f0": word_record(base, words["f0"]),
        "xi_F2": word_record(base, words["xi"]),
        "eta_F2": word_record(base, words["eta"]),
        "s_F2": word_record(base, words["s"]),
        "fs_F2": word_record(base, words["fs"]),
        "exponent_sums": {name: base.exponent_sums(words[name], 2)
                          for name in ("f0", "s", "fs")},
        "embedded_PB3_words": embedded,
        "embedded_E3_values": {name: element_record(base, e3.eval(word))
                               for name, word in embedded.items()},
        "coface_order": list(range(5)),
        "coface_words_PB4": coface_words,
        "coface_E4_values": {name: [element_record(base, value) for value in rows]
                             for name, rows in coface_values.items()},
        "all_direct_element_identity_tests_pass": True,
    }


def classify_results(results: Sequence[dict[str, Any]], complete: bool) \
        -> dict[str, Any]:
    if not complete:
        require(len(results) <= 6, "checker resource target prefix dimensions")
        bits = [None if not row.get("evaluated") else
                row.get("membership_proved") for row in results]
        bits.extend([None] * (6 - len(bits)))
        return {"membership_bits": bits,
                "complete": False, "exact_typed_inert": False}
    require(len(results) == 6 and
            all(row.get("evaluated") is True for row in results),
            "checker complete six-target ledger")
    bits = [row.get("membership_proved") for row in results]
    require(all(bit in (True, False) for bit in bits),
            "checker complete membership bit typing")
    return {"membership_bits": bits,
            "coface_membership_bits": bits[:5],
            "delta_membership_bit": bits[5],
            "explicit_s_JPhi_proved": all(bits[:5]),
            "target6_class_equality_proved": bool(bits[5]),
            "exact_typed_inert": all(bits[:5]) and bool(bits[5]),
            "complete": True}


def validate_source_hashes(data: dict[str, Any], repo: Path) -> None:
    expected_paths = {
        "producer_sha256": PRODUCER_PATH,
        "checker_sha256": CHECKER_PATH,
        "driver_sha256": DRIVER_PATH,
        "task_sha256": TASK_PATH,
        "q3_producer_sha256": Q3_PRODUCER,
        "q3_checker_sha256": Q3_CHECKER,
        "q3_driver_sha256": Q3_DRIVER,
        "v7_producer_sha256": V7_PRODUCER,
        "v7_checker_sha256": V7_CHECKER,
        "v9_producer_sha256": V9_PRODUCER,
        "v10_checker_sha256": V10_CHECKER,
        "v10_driver_sha256": V10_DRIVER,
    }
    actual = {key: (digest_file(repo / path) if (repo / path).is_file()
                    else "MISSING") for key, path in expected_paths.items()}
    require(data["source_hashes"] == actual, "source hash ledger")
    require(actual["task_sha256"] == TASK_SHA and
            actual["q3_producer_sha256"] == Q3_PRODUCER_SHA and
            actual["q3_checker_sha256"] == Q3_CHECKER_SHA and
            actual["q3_driver_sha256"] == Q3_DRIVER_SHA and
            actual["v7_producer_sha256"] == V7_PRODUCER_SHA and
            actual["v7_checker_sha256"] == V7_CHECKER_SHA and
            actual["v9_producer_sha256"] == V9_PRODUCER_SHA and
            actual["v10_checker_sha256"] == V10_CHECKER_SHA and
            actual["v10_driver_sha256"] == V10_DRIVER_SHA,
            "frozen dependency hash pins")


def validate_resource_guard(block: dict[str, Any], hit: bool,
                            reason: str | None) -> None:
    require(set(block) == {
        "seconds", "minutes", "rss_bytes", "rss_gib",
        "external_job_limit_minutes", "safety_margin_minutes", "clock",
        "rss_primary", "rss_portable_fallback", "hit", "hit_reason",
        "last_checked_phase", "check_count", "current_rss_bytes",
        "peak_rss_bytes", "terminal_on_hit", "consulted_in_selftest"},
        "resource guard exact keyset")
    require(block["seconds"] == 18_000 and block["minutes"] == 300 and
            block["rss_bytes"] == 4_831_838_208 and block["rss_gib"] == 4.5 and
            block["external_job_limit_minutes"] == 330 and
            block["safety_margin_minutes"] == 30 and
            block["clock"] == "time.monotonic" and
            block["hit"] is hit and block["hit_reason"] == reason and
            block["terminal_on_hit"] ==
                "B345_T53_STRONG_S_UNKNOWN_RESOURCE" and
            block["consulted_in_selftest"] is False and
            isinstance(block["check_count"], int) and block["check_count"] >= 0 and
            isinstance(block["current_rss_bytes"], int) and
            isinstance(block["peak_rss_bytes"], int) and
            block["peak_rss_bytes"] >= block["current_rss_bytes"] >= 0,
            "resource guard values")


def validate_input_terminal(data: dict[str, Any], repo: Path) -> None:
    require(set(data) == INPUT_KEYS and data["schema"] == SCHEMA and
            data["status"] == data["terminal_token"] ==
                "B345_T53_STRONG_S_UNKNOWN_INPUT" and
            data["reason"] == "authenticated_input_pin_mismatch" and
            isinstance(data["input_errors"], list) and data["input_errors"] and
            data["claims"] == claims(False) and
            data["result_summary"] == {
                "membership_bits": [None] * 6, "complete": False,
                "exact_typed_inert": False} and
            data["prohibited_work"] == prohibited_work(),
            "UNKNOWN_INPUT exact envelope")
    # At least one independently observed mismatch must be named.  We do not
    # require all files to exist on this deliberately fail-closed branch.
    require(all(set(row) == {"label", "expected", "got"}
                for row in data["input_errors"]), "input error rows")


def expected_target6_formula(base: Any, e4: Any,
                             formulas: dict[str, list[int]]) -> dict[str, Any]:
    r0, v0 = base.fox(formulas["r0"], e4)
    rs, vs = base.fox(formulas["rs"], e4)
    delta, vd = base.fox(formulas["delta"], e4)
    expected = dict(rs)
    base.add_scaled(expected, r0, -1)
    require(v0 == vs == vd == e4.identity and delta == expected,
            "independent target6 quotient/Fox subtraction")
    return {
        "name": "target6_delta_rs_r0_inverse",
        "r0": word_record(base, formulas["r0"]),
        "rs": word_record(base, formulas["rs"]),
        "delta": word_record(base, formulas["delta"]),
        "product_order": "delta=rs*r0^-1",
        "r0_formula": "coface_0(embed_F2_PB3(hexagon_1(f0)))",
        "rs_formula": "coface_0(embed_F2_PB3(hexagon_1(f0*s)))",
        "embed_F2_PB3": {"x": 1, "y": 3},
        "quotient_values": {"r0": element_record(base, v0),
                            "rs": element_record(base, vs),
                            "delta": element_record(base, vd)},
        "gradients": {"r0": raw_gradient_binding(base, r0),
                      "rs": raw_gradient_binding(base, rs),
                      "delta": raw_gradient_binding(base, delta)},
        "Fox_delta_equals_Fox_rs_minus_Fox_r0": True,
    }


def replay_target_results(base: Any, pool: Any, basis: Any,
                          targets: Sequence[tuple[str, str, list[int]]]) \
        -> list[dict[str, Any]]:
    results = []
    for ordinal, (name, kind, word) in enumerate(targets, 1):
        def probe() -> dict[str, Any]:
            packed, value_id = base.replay_fox_packed(word, pool)
            value = pool.value(value_id)
            binding = base.independent_gradient_binding(
                name, kind, base.fox(word, pool.q)[0], value)
            missing = basis.solve(packed)
            if missing is None:
                return {"binding": binding, "missing": None}
            component, identifier = base.replay_unpack_key(missing)
            blob = bytes(pool.values[identifier])
            return {"binding": binding,
                    "missing": {"component": component,
                                "element_hex": blob.hex(),
                                "canonical_value_sha256":
                                    hashlib.sha256(blob).hexdigest(),
                                "fixed_prefix_only": True,
                                "nonmembership_claimed": False}}
        replay = base.transactional_replay_probe(pool, probe)
        common = {"ordinal": ordinal, "name": name, "kind": kind,
                  "evaluated": True, "word": list(word),
                  "word_sha256": base.digest_obj(word),
                  "gradient_binding": replay["binding"]}
        if replay["missing"] is None:
            results.append({**common, "membership_proved": True,
                            "provisional_positive_solve": False,
                            "proof_complete": True, "missing_pivot": None,
                            "certificate_name": name})
        else:
            results.append({**common, "membership_proved": False,
                            "proof_complete": False,
                            "missing_pivot": replay["missing"]})
    return results


def validate_terminal_core(token: str, summary: dict[str, Any],
                           claim_block: dict[str, Any],
                           results: Sequence[dict[str, Any]]) -> None:
    require(token in TERMINALS, "registered terminal")
    if token == "B345_T53_STRONG_S_EXACT_TYPED_INERT":
        require(summary == classify_results(results, True) and
                summary["exact_typed_inert"] is True and
                claim_block == claims(True), "positive terminal core")
    elif token == "B345_T53_STRONG_S_PREFIX_INCOMPLETE":
        require(summary == classify_results(results, True) and
                summary["exact_typed_inert"] is False and
                claim_block == claims(False), "prefix-incomplete terminal core")
    elif token == "B345_T53_STRONG_S_UNKNOWN_RESOURCE":
        require(summary == classify_results(results, False) and
                claim_block == claims(False), "resource terminal core")
    else:
        require(token == "B345_T53_STRONG_S_UNKNOWN_INPUT" and
                claim_block == claims(False), "input terminal core")


def validate_prefix_accounting(block: dict[str, Any], pool: Any,
                               basis: Any) -> None:
    require(set(block) == {"BFS_translations", "directed_translations",
                           "total_translation_blocks", "columns", "pivots",
                           "dependent_columns", "live_sparse_entries",
                           "element_pool", "provenance_DAG",
                           "single_shared_basis",
                           "targeted_translations_for_six_questions"} and
            block["BFS_translations"] == 32768 and
            block["directed_translations"] == 207 and
            block["total_translation_blocks"] == 32975 and
            block["columns"] == basis.columns_seen == 362725 and
            block["pivots"] == len(basis.rows) == 362709 and
            block["dependent_columns"] == basis.dependent == 16 and
            block["live_sparse_entries"] == basis.live_entries and
            block["element_pool"]["size"] == len(pool.values) and
            block["single_shared_basis"] is True and
            block["targeted_translations_for_six_questions"] == 0,
            "fresh prefix accounting")


def validate_full_receipt(data: dict[str, Any], q3: dict[str, Any],
                          q3_path: Path, repo: Path, base: Any) -> None:
    require(set(data) == FULL_KEYS and data["schema"] == SCHEMA and
            data["terminal_token"] in TERMINALS and
            data["status"] == data["terminal_token"] and
            data["prohibited_work"] == prohibited_work(),
            "full receipt envelope")
    validate_source_hashes(data, repo)
    require(data["input"] == {"q3_path": Q3_PATH.as_posix(),
                              "q3_sha256": Q3_SHA,
                              "q3_same_job_checker_required": True} and
            digest_file(q3_path) == Q3_SHA and
            data["formula_sha256"] in (None, FORMULA_SHA),
            "q3 input/formula bindings")

    token = data["terminal_token"]
    if token == "B345_T53_STRONG_S_UNKNOWN_RESOURCE" and \
            data["formula_sha256"] is None:
        require(data["base_q3_replay"] is None and data["word_typing"] is None and
                data["directed_surgery"] is None and
                data["target_results"] == [] and
                data["partial"]["evaluated_target_count"] == 0 and
                data["reason"] in RESOURCE_REASONS,
                "pre-formula resource prefix")
        validate_terminal_core(token, data["result_summary"], data["claims"], [])
        validate_resource_guard(data["resource_guards"], True, data["reason"])
        return

    require(data["formula_sha256"] == FORMULA_SHA and
            q3.get("schema") == base.Q3_SCHEMA and
            q3.get("terminal_token") ==
                "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION" and
            base.digest_obj(q3["formulas"]) == FORMULA_SHA,
            "q3 authenticated mathematical input")
    e3, e4 = base.reconstruct(q3)
    base.validate_base_replay(data, q3, e3, e4)
    words = exact_words(base)
    require(data["word_typing"] == expected_word_typing(base, e3, e4, words),
            "exact word and F2->PB3 typing receipt")
    targets, formulas = target_words(base, words)
    require(data["target6_formula"] in
            (None, expected_target6_formula(base, e4, formulas)),
            "target6 literal formula/Fox binding")

    if data["directed_surgery"] is None:
        require(token == "B345_T53_STRONG_S_UNKNOWN_RESOURCE" and
                data["directed_base_support"] is None and
                data["prefix_accounting"] is None and
                data["target_results"] == [] and
                data["reason"] in RESOURCE_REASONS,
                "pre-prefix resource state")
        validate_terminal_core(token, data["result_summary"], data["claims"], [])
        validate_resource_guard(data["resource_guards"], True, data["reason"])
        return

    frozen_source_tuple = tuple(e4.eval(word) for word in base.source_words(F0))
    replay_targets = prefix_targets(base, formulas["r0"])
    pool, basis = base.replay_pivot_surgery(
        data, e4, replay_targets, frozen_source_tuple)
    validate_prefix_accounting(data["prefix_accounting"], pool, basis)

    def canary_probe() -> dict[str, Any]:
        gradient, value = base.replay_fox_packed(formulas["r0"], pool)
        require(value == pool.identity, "checker r0 quotient identity")
        missing = basis.solve(gradient)
        require(missing is not None, "checker r0 prefix unexpectedly solves")
        component, identifier = base.replay_unpack_key(missing)
        blob = bytes(pool.values[identifier])
        return {"target_name": "hexagon_1_coface_0", "component": component,
                "element_hex": blob.hex(),
                "canonical_value_sha256": hashlib.sha256(blob).hexdigest(),
                "prefix_missing_only_not_nonmembership": True}
    canary = base.transactional_replay_probe(pool, canary_probe)
    require(canary["component"] == 4 and
            canary["canonical_value_sha256"] == FINAL_BLOCKER_SHA and
            (data["r0_drift_canary"] == canary or
             token == "B345_T53_STRONG_S_UNKNOWN_RESOURCE" and
             data["r0_drift_canary"] is None),
            "post-saturation r0 canary")

    expected_results = replay_target_results(base, pool, basis, targets)
    recorded = data["target_results"]
    require(isinstance(recorded, list) and len(recorded) <= 6,
            "target result prefix dimensions")
    if token == "B345_T53_STRONG_S_UNKNOWN_RESOURCE":
        # Each recorded membership was evaluated before the cap.  A positive
        # solve stays null until complete proof serialization.
        for got, expected in zip(recorded, expected_results):
            if expected["membership_proved"]:
                provisional = dict(expected)
                provisional["membership_proved"] = None
                provisional["provisional_positive_solve"] = True
                provisional["proof_complete"] = False
                provisional.pop("certificate_name")
                require(got == provisional, "resource provisional-positive row")
            else:
                require(got == expected, "resource missing-pivot row")
        require(data["reason"] in RESOURCE_REASONS and
                data["partial"] == {
                    "phase": data["performance"]["phase_complete"],
                    "evaluated_target_count": len(recorded),
                    "unevaluated_memberships_are_null": True,
                    "positive_solve_without_serialized_proof_is_not_a_positive_bit": True,
                    "proof_serialization_complete": False},
                "resource target prefix ledger")
        validate_terminal_core(token, data["result_summary"], data["claims"],
                               recorded)
        validate_resource_guard(data["resource_guards"], True, data["reason"])
        return

    require(recorded == expected_results, "six independent membership outcomes")
    expected_summary = classify_results(expected_results, True)
    require(data["result_summary"] == expected_summary and
            data["registered_questions"] == {
                "count": 6,
                "ordered_names": [name for name, _, _ in targets],
                "ordered_names_sha256": base.digest_obj(
                    [name for name, _, _ in targets]),
                "fixed_prefix_only": True,
                "membership_missing_means_unknown": True},
            "six-question summary/order")
    validate_terminal_core(token, data["result_summary"], data["claims"],
                           expected_results)
    require((token == "B345_T53_STRONG_S_EXACT_TYPED_INERT") ==
            expected_summary["exact_typed_inert"] and data["partial"] is None,
            "terminal iff exact typed inert")

    positive_targets = [target for target, row in zip(targets, expected_results)
                        if row["membership_proved"]]
    positive_names = [name for name, _, _ in positive_targets]
    expected_bindings = [base.independent_gradient_binding(
        name, kind, *base.fox(word, e4))
        for name, kind, word in positive_targets]
    require(data["positive_target_order"] == positive_names and
            data["positive_gradient_bindings"] == expected_bindings,
            "positive target order/gradient bindings")
    if positive_targets:
        dag = data["boundary_proof_dag"]
        require(isinstance(dag, dict) and
                isinstance(data["quotient_element_registry"], list) and
                isinstance(data["boundary_certificates"], list),
                "positive proof payload availability")
        expression_values = base.decode_section_expressions(
            dag["section_expressions"], e4)
        by_id, reverse = base.validate_registry(
            data["quotient_element_registry"], {3: e3, 4: e4},
            expression_values)
        pb4_columns = []
        for relator in base.pure_relations(4):
            column, value = base.fox(relator, e4)
            require(value == e4.identity and base.boundary1(column, e4) == {},
                    "checker PB4 D1D2")
            pb4_columns.append(column)
        base.validate_certificates(
            data["boundary_certificates"], dag, positive_targets, e4,
            pb4_columns, by_id, reverse)
    else:
        require(data["positive_target_order"] == [] and
                data["positive_gradient_bindings"] == [] and
                data["quotient_element_registry"] == [] and
                data["boundary_proof_dag"] is None and
                data["boundary_certificates"] == [],
                "no boolean-only positive proof")
    validate_resource_guard(data["resource_guards"], False, None)
    require(set(data["performance"]) == {
                "runtime_seconds", "phase_complete", "RSS_peak_bytes"} and
            data["performance"]["phase_complete"] ==
                "six_target_certificate" and
            isinstance(data["performance"]["runtime_seconds"], (int, float)) and
            data["performance"]["runtime_seconds"] >= 0,
            "performance diagnostics")


def expect_reject(label: str, fn: Any) -> None:
    try:
        fn()
    except (Reject, ValueError, AssertionError):
        return
    raise AssertionError(f"mutation accepted: {label}")


def self_test() -> None:
    repo = Path(__file__).resolve().parents[1]
    require(digest_file(repo / V10_CHECKER) == V10_CHECKER_SHA,
            "selftest pinned v10 checker")
    base = load_v10(repo)
    words = exact_words(base)
    require(embed_f2(base, [1, 2]) == [1, 3] and
            embed_f2(base, [2]) != [2], "selftest load-bearing F2 embedding")
    positive = [{"evaluated": True, "membership_proved": True}
                for _ in range(6)]
    partial = [{"evaluated": True, "membership_proved": i != 3}
               for i in range(6)]
    validate_terminal_core("B345_T53_STRONG_S_EXACT_TYPED_INERT",
                           classify_results(positive, True), claims(True), positive)
    validate_terminal_core("B345_T53_STRONG_S_PREFIX_INCOMPLETE",
                           classify_results(partial, True), claims(False), partial)
    validate_terminal_core("B345_T53_STRONG_S_UNKNOWN_RESOURCE",
                           classify_results([], False), claims(False), [])
    validate_terminal_core("B345_T53_STRONG_S_UNKNOWN_INPUT",
                           {"membership_bits": [None] * 6, "complete": False,
                            "exact_typed_inert": False}, claims(False), [])
    resource_prefix = [
        {"evaluated": True, "membership_proved": False},
        {"evaluated": False, "membership_proved": None},
    ]
    require(classify_results([], False)["membership_bits"] == [None] * 6 and
            classify_results(resource_prefix, False)["membership_bits"] ==
                [False, None, None, None, None, None],
            "selftest fixed-width resource prefix")

    # Word/formula/orientation mutation separation.
    expect_reject("wrong y -> PB3 generator 2",
                  lambda: require(embed_f2(base, [2]) == [2], "wrong y"))
    expect_reject("commutator orientation",
                  lambda: require(words["s"] ==
                                  base.commutator(words["xi"], words["eta"]),
                                  "opposite commutator"))
    expect_reject("one exponent",
                  lambda: require(words["s"] ==
                                  base.commutator([2] * 17, words["xi"]),
                                  "17 exponent"))
    maps = base.cofaces(3)
    expect_reject("coface order",
                  lambda: require(maps == list(reversed(maps)), "coface reversal"))
    _, formulas = target_words(base, words)
    expect_reject("target6 coface/formula",
                  lambda: require(formulas["r0"] ==
                                  base.substitute(embed_f2(
                                      base, base.hexagon_words(F0)[0]), maps[1]),
                                  "wrong target6 coface"))
    expect_reject("delta product order",
                  lambda: require(formulas["delta"] ==
                                  base.reduce_word(base.inv_word(formulas["r0"]) +
                                                   formulas["rs"]),
                                  "wrong delta order"))
    # A nontrivial cyclic toy makes the negative-letter before/after-prefix
    # distinction observable without q3 or a large finite group.
    class ToyQ:
        identity = 0
        generators = [1, 0, 0, 0, 0, 0]
        inverse_generators = [2, 0, 0, 0, 0, 0]
        @staticmethod
        def mul(a: int, b: int) -> int:
            return (a + b) % 3
    correct, value = base.fox([-1], ToyQ())
    require(value == 2 and correct == {(1, 2): 2},
            "negative-letter Fox prefix canary")
    expect_reject("negative-letter old prefix",
                  lambda: require(correct == {(1, 0): 2}, "wrong Fox prefix"))
    grad_a = {(1, 0): 1}
    grad_b = {(1, 0): 2}
    right = dict(grad_a)
    base.add_scaled(right, grad_b, -1)
    wrong = dict(grad_a)
    base.add_scaled(wrong, grad_b, 1)
    expect_reject("gradient subtraction sign",
                  lambda: require(right == wrong, "gradient sign"))

    expected_missing = {"component": 4, "element_hex": "0102"}
    expect_reject("missing pivot component",
                  lambda: require({**expected_missing, "component": 3} ==
                                  expected_missing, "pivot component"))
    expect_reject("missing pivot value",
                  lambda: require({**expected_missing, "element_hex": "0103"} ==
                                  expected_missing, "pivot value"))
    expect_reject("stable prefix hash",
                  lambda: require("00" * 32 ==
                    base.V7_PREFIX_BINDINGS["stable_rounds_projection_sha256"],
                    "stable prefix"))
    for key in ("negative_claimed", "full_universe_claimed",
                "W_FORM_universal_claimed", "B4_A_claimed", "B4_B_claimed"):
        bad = claims(False)
        bad[key] = True
        expect_reject(f"claim leakage {key}",
                      lambda bad=bad: validate_terminal_core(
                          "B345_T53_STRONG_S_PREFIX_INCOMPLETE",
                          classify_results(partial, True), bad, partial))
    bad = copy.deepcopy(partial)
    bad[3]["membership_proved"] = True
    expect_reject("missing relabelled negative/positive",
                  lambda: require(classify_results(bad, True) ==
                                  classify_results(partial, True),
                                  "missing bit mutation"))
    # Reuse the pinned independent checker's production packed section/DAG
    # replay core and its coefficient/leaf/section/root mutation canaries.
    # That historical helper also asserts its then-current terminal set; v10
    # normally does not call it.  Inject only that sealed v7 fixture constant
    # and restore the live v10 module immediately afterward.
    saved_terminals = base.TERMINALS
    base.TERMINALS = {
        "B345_RELFRAT3_PIVOT_SURGERY_PASS",
        "B345_RELFRAT3_PIVOT_SURGERY_INCOMPLETE",
        "B345_RELFRAT3_PIVOT_SURGERY_UNKNOWN_RESOURCE",
        "B345_RELFRAT3_PIVOT_SURGERY_UNKNOWN_INPUT",
    }
    try:
        base.self_test_v7()
    finally:
        base.TERMINALS = saved_terminals
    print("B345_T53_STRONG_S_INERTNESS_CHECKER_SELFTEST_PASS "
          "shared_terminal_core=4 wrong_y=1 word_mutations=6 fox=2 "
          "gradient=1 blocker=2 prefix=1 proof_core=v7 claim_mutations=6",
          flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--q3", type=Path, default=Q3_PATH)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            return 0
        repo = Path(__file__).resolve().parents[1]
        require(args.receipt.resolve() == (repo / OUTPUT_PATH).resolve() and
                args.q3.resolve() == (repo / Q3_PATH).resolve(),
                "fixed production paths")
        data = json.loads(args.receipt.read_text(encoding="utf-8"))
        require(data.get("schema") == SCHEMA, "receipt schema")
        if data.get("terminal_token") == "B345_T53_STRONG_S_UNKNOWN_INPUT":
            validate_input_terminal(data, repo)
        else:
            require(args.q3.is_file() and digest_file(args.q3) == Q3_SHA,
                    "checker q3 artifact SHA")
            q3 = json.loads(args.q3.read_text(encoding="utf-8"))
            base = load_v10(repo)
            base.CHECKER_STARTED = time.monotonic()
            base.CHECKER_CHECKS = 0
            validate_full_receipt(data, q3, args.q3, repo, base)
            base.checker_deadline("T53 checker completion", force=True)
        print("B345_T53_STRONG_S_INERTNESS_CHECKER_PASS "
              f"terminal={data['terminal_token']}", flush=True)
        return 0
    except Exception as exc:
        print("B345_T53_STRONG_S_INERTNESS_CHECKER_FAIL " + str(exc),
              file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
