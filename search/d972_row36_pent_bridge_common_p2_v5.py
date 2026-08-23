#!/usr/bin/env python3
"""P2 row36 v5: defining-collector coordinate serialization repair."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import d972_row36_pent_bridge_common_v1 as base
import d972_row36_pent_bridge_common_p2_v4 as v4


RESULT_PATH = "ci/out/d972_row36_pent_bridge_p2_dpap_results_v5_20260824.json"
WORKER_PATH = "search/d972_row36_pent_bridge_p2_dpap_worker_v5.g"
GENERATOR_PATH = "search/d972_row36_pent_bridge_p2_worker_generator_v5.py"


def install(prime: int, out_dir: str | None) -> None:
    base.require(prime == 2, "P2_V5_PRIME_LOCAL", str(prime))
    # The v4 adapter is reused without changing its universe or predicates.
    # Its direct-result paths are versioned before its closures are installed.
    v4.RESULT_PATH = RESULT_PATH
    v4.WORKER_PATH = WORKER_PATH
    v4.GENERATOR_PATH = GENERATOR_PATH
    v4.install(prime, out_dir)
    build_raw_v4 = base.build_raw_universe
    execute_v4 = base.execute
    build_manifest_v4 = base.build_manifest

    def source_pins(_: int) -> list[dict[str, Any]]:
        return [
            base.file_pin("search/d972_row36_pent_bridge_common_v1.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v2.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v3.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_p2_v4.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_p2_v5.py"),
            base.file_pin("search/d972_row36_pent_bridge_p2_producer_v5.py"),
            base.file_pin(GENERATOR_PATH),
            base.file_pin(WORKER_PATH),
        ]

    def paths_for(_: int) -> dict[str, str]:
        prefix = Path(out_dir).as_posix().rstrip("/") if out_dir else "search/certs"
        return {
            "prereg": f"search/certs/d972_row36_pent_bridge_p2_prereg_v5_{base.DATE}.json",
            "receipt": f"{prefix}/d972_row36_pent_bridge_p2_receipt_v5_{base.DATE}.json",
            "manifest": f"{prefix}/d972_row36_pent_bridge_p2_manifest_v5_{base.DATE}.json",
        }

    def build_raw(prime_arg: int, receipt: dict[str, Any]):
        prereg, runtime = build_raw_v4(prime_arg, receipt)
        prereg["schema"] = "d972-row36-pent-bridge-p2-prereg/v5"
        prereg["source_pins"] = source_pins(prime_arg)
        prereg["execution_routing"]["p2_v4_run_stop"] = {
            "run_id": 32665138236,
            "commit": "7cc3179c",
            "elapsed_seconds": 49,
            "exact_stop": "PENT159O_ROW36_P2_WORKER_V4: marked coordinate drift",
            "phase": "after static Q4 construction and before Python/maps/BFS/census",
            "artifact_or_receipt": False,
            "classification": "coordinate-basis serialization mismatch; no semantic row result",
        }
        prereg["execution_routing"]["p2_v5_coordinate_repair"] = {
            "universe_or_predicate_change": False,
            "word_or_formula_change": False,
            "exported_basis": "NQ receipt Pcgs basis used to export all relation and marked coordinate vectors",
            "reconstructed_basis": "PcpGroupByCollectorNC defining generator sequence",
            "serialization": "List(Exponents(element),Int) in the defining collector basis",
            "rejected_serialization": "ExponentsOfPcElement(Pcgs(reconstructed_group),element), because Pcgs may be a different valid sequence",
            "defining_unit_gate_count": 26,
            "marked_positive_and_inverse_gate_count": 12,
            "v4_actual_diagnostic_printed_before_repaired_gate": True,
            "official_GAP_source_provenance": [
                "pkg/polycyclic/gap/basic/pcpgrps.gi: PcpGroupByCollectorNC constructs defining unit exponent elements and SetCgs",
                "lib/grppc.gi and lib/pcgscomp.gi: Pcgs may use an induced or composition-series sequence",
            ],
        }
        prereg["status"] = "PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME"
        prereg["terminal_token"] = "PENT159O_ROW36_P2_PREREG_V5_FROZEN"
        return prereg, runtime

    def execute(prime_arg: int, prereg_pin: dict[str, Any], prereg: dict[str, Any],
                runtime: dict[str, Any], input_pins: list[dict[str, Any]]):
        receipt, extra = execute_v4(prime_arg, prereg_pin, prereg, runtime, input_pins)
        receipt["schema"] = "d972-row36-pent-bridge-p2-receipt/v5"
        receipt["source_pins"] = source_pins(prime_arg)
        receipt["Q4_coordinate_serialization"] = {
            "basis": "reconstructed defining collector basis",
            "GAP_expression": "List(Exponents(element),Int)",
            "defining_generator_unit_gates": 26,
            "marked_positive_inverse_gates": 12,
            "canonical_Pcgs_diagnostic_only": True,
            "same_word_or_predicate_change": False,
        }
        receipt["terminal_token"] = \
            "PENT159O_ROW36_P2_PRODUCER_V5_CANDIDATE__CHECKER_REQUIRED"
        return receipt, extra

    def build_manifest(prime_arg: int, prereg_pin: dict[str, Any],
                       receipt_pin: dict[str, Any]):
        manifest = build_manifest_v4(prime_arg, prereg_pin, receipt_pin)
        manifest["schema"] = "d972-row36-pent-bridge-p2-manifest/v5"
        manifest["source_pins"] = source_pins(prime_arg)
        manifest["execution"]["local_command_prepare"] = \
            "python search/d972_row36_pent_bridge_p2_producer_v5.py prepare"
        manifest["execution"]["GHA_command"] = \
            "Read GAP v5 worker, then python3 search/d972_row36_pent_bridge_p2_producer_v5.py execute --out-dir ci/out"
        manifest["coordinate_basis"] = {
            "accepted": "defining collector Exponents",
            "canonical_Pcgs": "diagnostic only; never used to serialize receipt coordinates",
        }
        manifest["terminal_token"] = "PENT159O_ROW36_P2_MANIFEST_V5_FROZEN"
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
