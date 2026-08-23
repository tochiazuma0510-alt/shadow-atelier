#!/usr/bin/env python3
"""P2-only GAP Q4 same-word backend for the fixed-row36 bridge v4."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

import d972_row36_pent_bridge_common_v1 as base
import d972_row36_pent_bridge_common_v3 as v3


RESULT_PATH = "ci/out/d972_row36_pent_bridge_p2_dpap_results_v4_20260824.json"
WORKER_PATH = "search/d972_row36_pent_bridge_p2_dpap_worker_v4.g"
GENERATOR_PATH = "search/d972_row36_pent_bridge_p2_worker_generator_v4.py"
_BACKEND: dict[str, dict[str, Any]] = {}
_RESULT_PIN: dict[str, Any] | None = None


def install_backend(prereg: dict[str, Any]) -> dict[str, Any]:
    global _BACKEND, _RESULT_PIN
    result_pin = base.file_pin(RESULT_PATH)
    rows = base.load_json(RESULT_PATH)
    words = prereg["canonical_word_roster"]
    base.require(isinstance(rows, list) and len(rows) == len(words) == 32,
                 "P2_V4_GAP_BACKEND_ROW_COUNT", repr((len(rows), len(words))))
    backend: dict[str, dict[str, Any]] = {}
    for index, (result, frozen) in enumerate(zip(rows, words)):
        base.require(isinstance(result, list) and len(result) == 4,
                     "P2_V4_GAP_BACKEND_ROW_SCHEMA", str(index))
        word, defect, mutant, factors = result
        base.require(word == frozen["canonical_signed_xy"],
                     "P2_V4_GAP_BACKEND_WORD_ORDER", str(index))
        word_sha = base.digest(word)
        base.require(word_sha == frozen["word_sha256"] and word_sha not in backend,
                     "P2_V4_GAP_BACKEND_WORD_DIGEST", str(index))
        base.require(len(defect) == len(mutant) == 26 and
                     len(factors) == 5 and all(len(row) == 26 for row in factors),
                     "P2_V4_GAP_BACKEND_COORD_WIDTH", str(index))
        backend[word_sha] = {
            "literal_Dpap_coords": defect,
            "literal_Dpap_sha256": base.digest(defect),
            "literal_Dpap_identity": all(x == 0 for x in defect),
            "old_section_9_1_mutant_coords": mutant,
            "old_section_9_1_mutant_sha256": base.digest(mutant),
            "coface_factor_coords": factors,
            "coface_factor_roster_sha256": base.digest(factors),
        }
    base.require(len(backend) == 32, "P2_V4_GAP_BACKEND_UNIQUENESS")
    _BACKEND = backend
    _RESULT_PIN = result_pin
    return {"worker_source": base.file_pin(WORKER_PATH),
            "worker_generator": base.file_pin(GENERATOR_PATH),
            "result": result_pin,
            "word_count": len(backend),
            "direct_same_signed_word": True,
            "literal_A18_replayed_in_worker": True,
            "lookup_key": "canonical signed-word SHA-256 after exact word equality replay",
            "quotient_canary_rerun": False}


def q4_contexts_backend(*_args):
    base.require(len(_BACKEND) == 32, "P2_V4_GAP_BACKEND_NOT_INSTALLED")
    return "P2_V4_GAP_DIRECT_SAME_WORD_RESULTS"


def evaluate_dpap_backend(word: Sequence[int], _q4col: base.PcCollector,
                          contexts: Any) -> dict[str, Any]:
    base.require(contexts == "P2_V4_GAP_DIRECT_SAME_WORD_RESULTS",
                 "P2_V4_GAP_BACKEND_CONTEXT_TOKEN")
    word_sha = base.digest(list(word))
    base.require(word_sha in _BACKEND, "P2_V4_GAP_BACKEND_WORD_MISSING", word_sha)
    return dict(_BACKEND[word_sha])


def install(prime: int, out_dir: str | None) -> None:
    base.require(prime == 2, "P2_V4_PRIME_LOCAL", str(prime))
    v3.install(prime, out_dir)
    build_raw_v3 = base.build_raw_universe
    execute_v3 = base.execute
    build_manifest_v3 = base.build_manifest

    def source_pins(_: int) -> list[dict[str, Any]]:
        return [
            base.file_pin("search/d972_row36_pent_bridge_common_v1.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v2.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v3.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_p2_v4.py"),
            base.file_pin("search/d972_row36_pent_bridge_p2_producer_v4.py"),
            base.file_pin(GENERATOR_PATH),
            base.file_pin(WORKER_PATH),
        ]

    def paths_for(_: int) -> dict[str, str]:
        prefix = Path(out_dir).as_posix().rstrip("/") if out_dir else "search/certs"
        return {
            "prereg": f"search/certs/d972_row36_pent_bridge_p2_prereg_v4_{base.DATE}.json",
            "receipt": f"{prefix}/d972_row36_pent_bridge_p2_receipt_v4_{base.DATE}.json",
            "manifest": f"{prefix}/d972_row36_pent_bridge_p2_manifest_v4_{base.DATE}.json",
        }

    def build_raw(prime_arg: int, receipt: dict[str, Any]):
        prereg, runtime = build_raw_v3(prime_arg, receipt)
        prereg["schema"] = "d972-row36-pent-bridge-p2-prereg/v4"
        prereg["source_pins"] = source_pins(prime_arg)
        prereg["execution_routing"]["p2_v3_run_stop"] = {
            "run_id": 32664400481,
            "commit": "479d815faf5e577a6b9138bf88e4cc0369aab05d",
            "exact_inner_stop": "PC_COLLECTION_CAP: (27, 26)",
            "phase": "rank-26 Q4 direct same-word multiplication after residual coverage",
            "classification": "Python token-collector resource trap; no receipt/artifact",
        }
        prereg["execution_routing"]["p2_v4_repair"] = {
            "mathematical_change": False,
            "universe_or_predicate_change": False,
            "backend": "static GAP pc collector reconstructed from immutable v14 exported Q4 tables",
            "worker_source_pin": base.file_pin(WORKER_PATH),
            "worker_word_roster_source": "frozen p2-v3 preregistration; v4 execute requires exact ordered equality with the reconstructed v4 roster",
            "worker_direct_formula_native": "F*E*C*B^-1*A^-1",
        }
        prereg["status"] = "PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME"
        prereg["terminal_token"] = "PENT159O_ROW36_P2_PREREG_V4_FROZEN"
        return prereg, runtime

    def execute(prime_arg: int, prereg_pin: dict[str, Any], prereg: dict[str, Any],
                runtime: dict[str, Any], input_pins: list[dict[str, Any]]):
        backend_gate = install_backend(prereg)
        base.q4_contexts = q4_contexts_backend
        base.evaluate_dpap = evaluate_dpap_backend
        receipt, extra = execute_v3(prime_arg, prereg_pin, prereg, runtime, input_pins)
        receipt["schema"] = "d972-row36-pent-bridge-p2-receipt/v4"
        receipt["source_pins"] = source_pins(prime_arg)
        receipt["Q4_direct_same_word_GAP_backend"] = backend_gate
        receipt["firewall"]["NQ_or_GAP_invoked"] = True
        receipt["firewall"]["GAP_static_Q4_worker_invoked"] = True
        receipt["firewall"]["NQ_invoked"] = False
        receipt["firewall"]["quotient_canary_rerun"] = False
        receipt["terminal_token"] = \
            "PENT159O_ROW36_P2_PRODUCER_V4_CANDIDATE__CHECKER_REQUIRED"
        return receipt, extra

    def build_manifest(prime_arg: int, prereg_pin: dict[str, Any], receipt_pin: dict[str, Any]):
        manifest = build_manifest_v3(prime_arg, prereg_pin, receipt_pin)
        manifest["schema"] = "d972-row36-pent-bridge-p2-manifest/v4"
        manifest["source_pins"] = source_pins(prime_arg)
        manifest["execution"]["local_command_prepare"] = \
            "python search/d972_row36_pent_bridge_p2_producer_v4.py prepare"
        manifest["execution"]["GHA_command"] = \
            "Read GAP worker, then python3 search/d972_row36_pent_bridge_p2_producer_v4.py execute --out-dir ci/out"
        manifest["execution"]["GAP_or_NQ"] = True
        manifest["execution"]["GAP_static_Q4_worker"] = True
        manifest["execution"]["NQ"] = False
        manifest["execution"]["quotient_canary_rerun"] = False
        manifest["GAP_worker_result_pin"] = _RESULT_PIN
        manifest["terminal_token"] = "PENT159O_ROW36_P2_MANIFEST_V4_FROZEN"
        return manifest

    base.source_pins = source_pins
    base.paths_for = paths_for
    base.build_raw_universe = build_raw
    base.execute = execute
    base.build_manifest = build_manifest


def main_for_prime(prime: int) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare", "execute"))
    parser.add_argument("--out-dir")
    args = parser.parse_args()
    if args.phase == "prepare":
        base.require(args.out_dir is None, "PREPARE_OUT_DIR_FORBIDDEN")
    else:
        base.require(args.out_dir is not None, "EXECUTE_OUT_DIR_REQUIRED")
        rel = Path(args.out_dir)
        base.require(not rel.is_absolute() and ".." not in rel.parts,
                     "EXECUTE_OUT_DIR_UNSAFE", args.out_dir)
    install(prime, args.out_dir)
    raise SystemExit(base.run(prime, [args.phase]))
