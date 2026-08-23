#!/usr/bin/env python3
"""P3 row36 v11 outcome adapter over the frozen v8 preregistration."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Sequence

import d972_row36_pent_bridge_common_v1 as base
import d972_row36_pent_bridge_common_p3_v6 as v6
import d972_row36_pent_bridge_common_p3_v8 as v8


PREREG_PATH = "search/certs/d972_row36_pent_bridge_p3_prereg_v8_20260824.json"
PREREG_PIN = (66337660,
              "2d33542ba797440ec96d16e02f9f8d7ea537048eb84d02b2ce57153d147faea4")
RESULT_PATH = "ci/out/d972_row36_pent_bridge_p3_q4_results_v11_20260824.json"
WORKER_PATH = "search/d972_row36_pent_bridge_p3_q4_outcome_worker_v11.g"
GENERATOR_PATH = "search/d972_row36_pent_bridge_p3_q4_worker_generator_v11.py"
SOURCE_PATH = "search/d972_row36_pent_bridge_common_p3_v11.py"
PRODUCER_PATH = "search/d972_row36_pent_bridge_p3_producer_v11.py"
WORD_ROSTER_DIGEST = "25a1192cb60321035feb5f36045c4417eb0a92a07e1be7918cbabadff19a04a1"
RAW_ROSTER_DIGEST = "644e254535d210c2cf16778ee2d09b762358fb80ea0a82c839f5a8e1c01561ee"

_BACKEND: dict[str, dict[str, Any]] = {}
_RESULT_PIN: dict[str, Any] | None = None


def source_pins() -> list[dict[str, Any]]:
    paths = (
        "search/d972_row36_pent_bridge_common_v1.py",
        "search/d972_row36_pent_bridge_common_v2.py",
        "search/d972_row36_pent_bridge_common_v3.py",
        "search/d972_row36_pent_bridge_common_v4.py",
        "search/d972_row36_pent_bridge_common_p3_v5.py",
        "search/d972_row36_pent_bridge_common_p3_v6.py",
        "search/d972_row36_pent_bridge_p3_producer_v1.py",
        "search/d972_row36_pent_bridge_p3_producer_v2.py",
        "search/d972_row36_pent_bridge_p3_producer_v3.py",
        "search/d972_row36_pent_bridge_p3_producer_v4.py",
        "search/d972_row36_pent_bridge_p3_producer_v5.py",
        "search/d972_row36_pent_bridge_p3_producer_v6.py",
        "search/d972_row36_pent_bridge_common_p3_v7.py",
        "search/d972_row36_pent_bridge_p3_producer_v7.py",
        "search/d972_row36_pent_bridge_p3_transition_worker_generator_v7.py",
        "search/d972_row36_pent_bridge_p3_transition_worker_v7.g",
        "search/d972_row36_pent_bridge_common_p3_v8.py",
        "search/d972_row36_pent_bridge_p3_producer_v8.py",
        "search/d972_row36_pent_bridge_p3_transition_worker_generator_v8.py",
        "search/d972_row36_pent_bridge_p3_transition_worker_v8.g",
        SOURCE_PATH, PRODUCER_PATH, GENERATOR_PATH, WORKER_PATH,
    )
    return [base.file_pin(path) for path in paths]


def authenticate_prereg() -> tuple[dict[str, Any], dict[str, Any]]:
    prereg_pin = base.file_pin(PREREG_PATH, PREREG_PIN)
    prereg = base.load_json(PREREG_PATH)
    base.require(prereg.get("schema") == "d972-row36-pent-bridge-p3-prereg/v8" and
                 prereg.get("status") ==
                 "PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME" and
                 prereg.get("terminal_token") ==
                 "PENT159O_ROW36_P3_PREREG_V8_FROZEN",
                 "P3_V11_PREREG_SCHEMA_STATUS")
    coverage = prereg.get("coverage_freeze", {})
    words = prereg.get("canonical_word_roster")
    rows = prereg.get("raw_rows")
    base.require(isinstance(words, list) and len(words) == 17496 and
                 isinstance(rows, list) and len(rows) == 34992 and
                 coverage.get("canonical_word_roster_sha256") ==
                 WORD_ROSTER_DIGEST and
                 coverage.get("raw_roster_sha256") == RAW_ROSTER_DIGEST and
                 coverage.get("predicate_outcomes_not_evaluated") is True,
                 "P3_V11_PREREG_ROSTER_BINDING")
    base.require(all(row.get("word_id") == f"W{index + 1:05d}" and
                     row.get("word_sha256") ==
                     base.digest(row.get("canonical_signed_xy"))
                     for index, row in enumerate(words)),
                 "P3_V11_PREREG_WORD_ORDER_DIGEST")
    base.require(all(row.get("row_id") == f"P3R{index + 1:05d}" and
                     row.get("m") == (0 if index < 17496 else 18) and
                     row.get("word_id") == f"W{index % 17496 + 1:05d}"
                     for index, row in enumerate(rows)),
                 "P3_V11_PREREG_RAW_ORDER")
    return prereg_pin, prereg


def install_backend(prereg: dict[str, Any]) -> dict[str, Any]:
    global _BACKEND, _RESULT_PIN
    result_pin = base.file_pin(RESULT_PATH)
    raw = base.load_json(RESULT_PATH)
    words = prereg["canonical_word_roster"]
    base.require(isinstance(raw, list) and len(raw) == len(words) == 17496,
                 "P3_V11_Q4_RESULT_COUNT")
    backend: dict[str, dict[str, Any]] = {}
    for index, (result, frozen) in enumerate(zip(raw, words)):
        base.require(isinstance(result, list) and len(result) == 4,
                     "P3_V11_Q4_RESULT_SCHEMA", str(index))
        word, defect, mutant, factors = result
        base.require(word == frozen["canonical_signed_xy"],
                     "P3_V11_Q4_WORD_ORDER", str(index))
        word_sha = base.digest(word)
        base.require(word_sha == frozen["word_sha256"] and word_sha not in backend,
                     "P3_V11_Q4_WORD_DIGEST", str(index))
        base.require(len(defect) == len(mutant) == 26 and
                     all(isinstance(x, int) and 0 <= x < 3
                         for x in defect + mutant) and
                     isinstance(factors, list) and len(factors) == 5 and
                     all(len(row) == 26 and
                         all(isinstance(x, int) and 0 <= x < 3 for x in row)
                         for row in factors),
                     "P3_V11_Q4_COORDINATE_SCHEMA", str(index))
        backend[word_sha] = {
            "literal_Dpap_coords": defect,
            "literal_Dpap_sha256": base.digest(defect),
            "literal_Dpap_identity": all(x == 0 for x in defect),
            "old_section_9_1_mutant_coords": mutant,
            "old_section_9_1_mutant_sha256": base.digest(mutant),
            "coface_factor_coords": factors,
            "coface_factor_roster_sha256": base.digest(factors),
        }
    base.require(len(backend) == 17496, "P3_V11_Q4_BACKEND_UNIQUENESS")
    _BACKEND = backend
    _RESULT_PIN = result_pin
    return {
        "worker_source": base.file_pin(WORKER_PATH),
        "worker_generator": base.file_pin(GENERATOR_PATH),
        "result": result_pin,
        "word_count": len(backend),
        "row_count": 34992,
        "coordinate_width": 26,
        "coordinate_basis": "reconstructed defining collector Exponents",
        "direct_same_signed_word": True,
        "literal_A18_10_of_10_before_census": True,
        "old_reversal_mutant_rejected_before_census": True,
        "lookup_key": (
            "canonical signed-word SHA-256 after exact ordered word equality replay"
        ),
        "quotient_canary_rerun": False,
    }


def q4_contexts_backend(*_args: Any) -> str:
    base.require(len(_BACKEND) == 17496, "P3_V11_Q4_BACKEND_NOT_INSTALLED")
    return "P3_V11_GAP_DIRECT_SAME_WORD_RESULTS"


def evaluate_dpap_backend(word: Sequence[int], _q4col: base.PcCollector,
                          contexts: Any) -> dict[str, Any]:
    base.require(contexts == "P3_V11_GAP_DIRECT_SAME_WORD_RESULTS",
                 "P3_V11_Q4_CONTEXT_TOKEN")
    word_sha = base.digest(list(word))
    base.require(word_sha in _BACKEND, "P3_V11_Q4_WORD_MISSING", word_sha)
    return dict(_BACKEND[word_sha])


def run_execute(out_dir: str) -> int:
    try:
        rel = Path(out_dir)
        base.require(not rel.is_absolute() and ".." not in rel.parts,
                     "P3_V11_OUT_DIR_UNSAFE", out_dir)
        v8.install(3)
        input_pins, canary = base.authenticate_inputs(3)
        prereg_pin, prereg = authenticate_prereg()

        q2 = canary["quotients"]["Q2"]
        q4 = canary["quotients"]["Q4"]
        qcol = base.PcCollector(q2)
        q4col = base.PcCollector(q4, cache_capacity=16)
        v6._ACTIVE_RECEIPT = canary
        # The preregistration layer installs this validator inside its
        # build_raw wrapper.  Outcome v11 consumes an already frozen prereg and
        # therefore must select the same transition-table validator explicitly,
        # before any generic rank-seven inverse collection can be attempted.
        base.validate_pc_receipt = v6.validate_pc_receipt_v6
        qmarks, q4marks = base.validate_pc_receipt(3, q2, q4, qcol, q4col)
        q4_inverse_marks = tuple(q4col.coord(row["inverse_coords"])
                                 for row in q4["marked_generators"])
        runtime = {
            "qcol": qcol, "q4col": q4col, "qmarks": qmarks,
            "q4marks": q4marks, "q4_inverse_marks": q4_inverse_marks,
        }
        transition_gate = getattr(qcol, "p3_transition_gate_v6")
        base.require(transition_gate["state_count"] == 2187 and
                     transition_gate["paper_projection_signed_replay_count"] == 2187 and
                     transition_gate["native_product_bridge_rows"] == 8748,
                     "P3_V11_TRANSITION_PREREQUISITE")
        projection, projection_words = v6.projection_from_canary(canary)
        right_positive = transition_gate["native_right_positive_zero_based"]
        right_inverse = transition_gate["native_right_inverse_zero_based"]
        paper_positive = transition_gate["paper_left_positive_zero_based"]
        paper_inverse = transition_gate["paper_left_inverse_zero_based"]
        right_tables = {
            1: tuple(right_positive["x"]), 2: tuple(right_positive["y"]),
            -1: tuple(right_inverse["x_inverse"]),
            -2: tuple(right_inverse["y_inverse"]),
        }
        paper_tables = {
            1: tuple(paper_positive["x"]), 2: tuple(paper_positive["y"]),
            -1: tuple(paper_inverse["x_inverse"]),
            -2: tuple(paper_inverse["y_inverse"]),
        }

        def replay_transition(word: Sequence[int], tables: dict[int, tuple[int, ...]]) -> int:
            state = 0
            for letter in word:
                state = tables[int(letter)][state]
            return state

        state2_word = tuple(transition_gate["state2_orientation_canary"]["paper_word"])
        inverse_state2_word = base.inverse_word(state2_word)
        native_state = replay_transition(state2_word, right_tables)
        paper_state = replay_transition(state2_word, paper_tables)
        native_inverse_state = replay_transition(inverse_state2_word, right_tables)
        paper_inverse_state = replay_transition(inverse_state2_word, paper_tables)
        state_roster = transition_gate["state_roster"]
        transition_cell_count = sum(len(row) for row in right_tables.values()) + \
            sum(len(row) for row in paper_tables.values())
        prefix_count = sum(len(word) for word in projection_words.values())
        base.require(transition_cell_count == 17496 and prefix_count == 14748 and
                     len(projection) == len(projection_words) == 2187 and
                     (native_state, paper_state, native_inverse_state,
                      paper_inverse_state) == (7, 1, 5, 2) and
                     state_roster[native_state] == [0, 0, 0, 0, 0, 2, 1] and
                     state_roster[paper_state] == [0, 0, 0, 0, 0, 0, 1] and
                     state_roster[native_inverse_state] == [0, 0, 0, 0, 0, 1, 2] and
                     state_roster[paper_inverse_state] == [0, 0, 0, 0, 0, 0, 2],
                     "P3_V11_EXHAUSTIVE_TRANSITION_ORIENTATION")
        transition_audit = {
            "state_count": 2187,
            "signed_transition_cells": transition_cell_count,
            "transition_cell_breakdown": {
                "native_right_positive": 4374,
                "native_right_inverse": 4374,
                "paper_left_positive": 4374,
                "paper_left_inverse": 4374,
            },
            "projection_word_count": len(projection_words),
            "projection_signed_prefix_steps": prefix_count,
            "projection_sha256": transition_gate["projection_sha256"],
            "canary_trace_provenance": {
                "full_gate_trace_rows": 19683,
                "rows_per_Q3_state": 9,
                "m_values_per_state": list(range(9)),
                "predicate_fields_used": False,
            },
            "inverse_word_inverse_state_rows": 2187,
            "two_sided_inverse_product_rows": 4374,
            "inverse_law_gate": (
                "v8 constructs each inverse state by paper replay of inverse_word "
                "and requires state*inverse=inverse*state=identity for all states"
            ),
            "state2_four_way_discriminator": {
                "paper_word": list(state2_word),
                "target_state_one_based": 2,
                "target_coords": state_roster[paper_state],
                "native_written_right_state_one_based": native_state + 1,
                "native_written_right_coords": state_roster[native_state],
                "reversed_native_paper_left_state_one_based": paper_state + 1,
                "native_eval_inverse_word_state_one_based": native_inverse_state + 1,
                "native_eval_inverse_word_coords": state_roster[native_inverse_state],
                "native_eval_reverse_inverse_word_state_one_based":
                    paper_inverse_state + 1,
                "native_eval_reverse_inverse_word_coords":
                    state_roster[paper_inverse_state],
                "no_inversion_or_sign_flip": True,
            },
            "all_gates_passed_before_predicate_outcome": True,
        }
        backend_gate = install_backend(prereg)
        base.q4_contexts = q4_contexts_backend
        base.evaluate_dpap = evaluate_dpap_backend

        receipt, _ = base.execute(3, prereg_pin, prereg, runtime, input_pins)
        pins = source_pins()
        receipt["schema"] = "d972-row36-pent-bridge-p3-receipt/v11"
        receipt["status"] = "CANDIDATE_P3_FIXED_ROW36_FULL_OUTCOME__CHECKER_REQUIRED"
        receipt["scope"] = (
            "complete fixed zero-based row36 p3 bridge over the exact frozen v8 "
            "34,992-row roster; no quotient-canary rerun"
        )
        receipt["source_pins"] = pins
        receipt["preregistration_pin"] = prereg_pin
        receipt["Q3_transition_prerequisite"] = transition_gate
        receipt["Q3_exhaustive_orientation_certificate"] = transition_audit
        receipt["Q4_direct_same_word_GAP_backend"] = backend_gate
        receipt["firewall"]["NQ_or_GAP_invoked"] = True
        receipt["firewall"]["GAP_static_Q4_worker_invoked"] = True
        receipt["firewall"]["NQ_invoked"] = False
        receipt["firewall"]["quotient_canary_rerun"] = False
        receipt["promotion_boundary"] = {
            "independent_row_checker_pending": True,
            "row_gate_crosschecked": False,
            "mode_token": None, "K2_name": None,
            "all_prime_promotion": False,
        }
        receipt["terminal_token"] = (
            "PENT159O_ROW36_P3_PRODUCER_V11_CANDIDATE__CHECKER_REQUIRED"
        )
        prefix = rel.as_posix().rstrip("/")
        receipt_path = (
            f"{prefix}/d972_row36_pent_bridge_p3_receipt_v11_{base.DATE}.json"
        )
        manifest_path = (
            f"{prefix}/d972_row36_pent_bridge_p3_manifest_v11_{base.DATE}.json"
        )
        receipt_pin = base.immutable_write(receipt_path, receipt)
        manifest = {
            "schema": "d972-row36-pent-bridge-p3-manifest/v11",
            "date": base.DATE,
            "prime": 3,
            "role": "immutable producer manifest; checker handoff receipt+manifest only",
            "source_pins": pins,
            "input_pins": input_pins,
            "preregistration": prereg_pin,
            "Q3_transition_result": transition_gate["result_pin"],
            "Q4_worker_result": _RESULT_PIN,
            "producer_receipt": receipt_pin,
            "checker_handoff_allowlist": [receipt_path, manifest_path],
            "checker_handoff_forbidden": [
                "producer source", "producer helpers", "producer report",
                "producer logs", "GAP worker/result", "transition tables",
                "other checker artifacts",
            ],
            "execution": {
                "GHA_command": (
                    "reconstruct and hash-gate v8 prereg; read GAP v11 Q4 worker; "
                    "python3 p3 producer v11 execute --out-dir ci/out"
                ),
                "quotient_canary_rerun": False,
                "GAP_static_Q4_worker": True,
                "NQ": False,
                "deterministic": True,
            },
            "coverage": {
                "canonical_words": 17496,
                "raw_rows": 34992,
                "central_m_lifts_in_order": [0, 18],
                "literal_A18_relator_rows": 10,
                "same_word_Dpap_for_every_canonical_word": True,
                "onto_evaluated_for_every_materialized_row": True,
                "CLAIM_COVER_token": "CLAIM-COVER-PENT-CANARY-2",
            },
            "promotion_boundary": {
                "independent_checker_required": True,
                "mode_token": None, "K2_name": None,
                "all_prime_inference": False,
            },
            "terminal_token": "PENT159O_ROW36_P3_MANIFEST_V11_FROZEN",
        }
        manifest_pin = base.immutable_write(manifest_path, manifest)
        print("PENT159O_ROW36_P3_V11_RECEIPT_WRITTEN "
              f"path={receipt_pin['path']} bytes={receipt_pin['bytes']} "
              f"sha256={receipt_pin['sha256']}", flush=True)
        print("PENT159O_ROW36_P3_V11_MANIFEST_WRITTEN "
              f"path={manifest_pin['path']} bytes={manifest_pin['bytes']} "
              f"sha256={manifest_pin['sha256']}", flush=True)
        print("PENT159O_ROW36_P3_V11_FINAL PRODUCER_CANDIDATE_CHECKER_REQUIRED",
              flush=True)
        return 0
    except base.ProducerStop as exc:
        print(f"PENT159O_ROW36_P3_V11_STATE_STOP {exc}", file=sys.stderr,
              flush=True)
        return 2


def main_for_prime(prime: int) -> None:
    base.require(prime == 3, "P3_V11_PRIME_LOCAL", str(prime))
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("execute",))
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    base.require(args.phase == "execute", "P3_V11_EXECUTE_ONLY")
    raise SystemExit(run_execute(args.out_dir))
