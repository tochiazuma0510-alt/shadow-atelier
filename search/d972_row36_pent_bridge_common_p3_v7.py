#!/usr/bin/env python3
"""P3 row36 v7 explicit state-serialization repair.

This layer preserves the complete v6 outcome-free universe and derivation
contract.  It changes only the GAP transition result and preregistration paths,
binding the explicit base-three lexicographic state roster used consistently by
GAP's index function and Python's state table.
"""

from __future__ import annotations

import argparse

import d972_row36_pent_bridge_common_v1 as base
import d972_row36_pent_bridge_common_p3_v6 as v6


RESULT_PATH = "ci/out/d972_row36_pent_bridge_p3_transition_results_v7_20260824.json"
GENERATOR_PATH = "search/d972_row36_pent_bridge_p3_transition_worker_generator_v7.py"
WORKER_PATH = "search/d972_row36_pent_bridge_p3_transition_worker_v7.g"


def install(prime: int) -> None:
    base.require(prime == 3, "P3_V7_PRIME_LOCAL", str(prime))
    v6.RESULT_PATH = RESULT_PATH
    v6.GENERATOR_PATH = GENERATOR_PATH
    v6.WORKER_PATH = WORKER_PATH
    v6.install(prime)
    build_raw_v6 = base.build_raw_universe

    def source_pins(_: int):
        return [
            base.file_pin("search/d972_row36_pent_bridge_common_v1.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v2.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v3.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_p3_v6.py"),
            base.file_pin("search/d972_row36_pent_bridge_p3_producer_v6.py"),
            base.file_pin("search/d972_row36_pent_bridge_p3_transition_worker_v6.g"),
            base.file_pin("search/d972_row36_pent_bridge_common_p3_v7.py"),
            base.file_pin("search/d972_row36_pent_bridge_p3_producer_v7.py"),
            base.file_pin(GENERATOR_PATH),
            base.file_pin(WORKER_PATH),
        ]

    def paths_for(_: int):
        return {
            "prereg": f"search/certs/d972_row36_pent_bridge_p3_prereg_v7_{base.DATE}.json",
            "receipt": f"search/certs/d972_row36_pent_bridge_p3_receipt_v7_{base.DATE}.json",
            "manifest": f"search/certs/d972_row36_pent_bridge_p3_manifest_v7_{base.DATE}.json",
        }

    def build_raw(prime_arg: int, receipt):
        prereg, runtime = build_raw_v6(prime_arg, receipt)
        prereg["schema"] = "d972-row36-pent-bridge-p3-prereg/v7"
        prereg["source_pins"] = source_pins(prime_arg)
        prereg["execution_routing"]["p3_v6_run_stop"] = {
            "run_id": 32668331588,
            "commit": "8f933154",
            "last_passed_marker": (
                "PENT159O_ROW36_P3_WORKER_V6_PUBLIC_PC_PASS units=7 powers=7 "
                "inverses=7 conjugates=21 inverse_conjugates=21 marks=2 "
                "source_relators=0"
            ),
            "exact_stop": (
                "PENT159O_ROW36_P3_WORKER_V6: signed projection replay drift state=2"
            ),
            "classification": (
                "state serialization mismatch: implicit GAP Tuples order was mixed "
                "with explicit base-three lex coordinate indices"
            ),
            "artifact_or_preregistration": False,
            "mathematical_result": False,
        }
        prereg["execution_routing"]["p3_v7_state_serialization_repair"] = {
            "universe_or_predicate_change": False,
            "state_roster": (
                "explicit [floor(n/3^6) mod3,...,n mod3] for n=0..2186"
            ),
            "coordinate_index": "one plus the base-three value of the seven coordinates",
            "mandatory_roundtrip": "Index(states[i])=i for all i=1..2187",
            "Python_state_order": "itertools.product(range(3),repeat=7)",
            "all_three_serializations_identical": True,
            "outcome_free": True,
        }
        certificate = prereg["canonical_section_derivation_certificate"]
        certificate["schema"] = \
            "d972-row36-pent-bridge-p3-canonical-section-certificate/v7"
        certificate["transition_state_serialization"] = {
            "GAP": "explicit base-three lex roster",
            "GAP_index_roundtrip_count": 2187,
            "Python": "itertools.product lex roster",
            "same_order": True,
        }
        certificate["terminal_token"] = \
            "PENT159O_ROW36_P3_V7_CANONICAL_SECTION_PREREGISTERED"
        prereg["status"] = "PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME"
        prereg["terminal_token"] = "PENT159O_ROW36_P3_PREREG_V7_FROZEN"
        return prereg, runtime

    base.source_pins = source_pins
    base.paths_for = paths_for
    base.build_raw_universe = build_raw


def main_for_prime(prime: int) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare",))
    args = parser.parse_args()
    base.require(args.phase == "prepare", "P3_V7_PREREG_ONLY")
    install(prime)
    raise SystemExit(base.run(prime, ["prepare"]))

