#!/usr/bin/env python3
"""Independent checker for the [16,8,4] full marked-orbit scan."""

from __future__ import annotations

import argparse
import json
import os
import threading
import time
from pathlib import Path

import check_campaign138_d7_measure_v1 as independent_scan
import check_campaign138_higher_perfect_preflight_v1 as independent_library


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--preflight", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--hard-timeout-seconds", type=int, default=600)
    args = parser.parse_args()
    source_path = Path(args.source)
    preflight_path = Path(args.preflight)
    metadata_path = Path(args.metadata)
    output_path = Path(args.output)
    checkpoint_path = Path(args.checkpoint)
    began = time.monotonic()
    source_hash = independent_scan.sha_file(source_path)
    reconstructed: list[dict] = []
    if checkpoint_path.exists():
        old = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        if (
            old.get("schema") == "campaign138_d8_measure_check_checkpoint/v1"
            and old.get("source_sha256") == source_hash
        ):
            reconstructed = list(old.get("orbit_results", []))
    state = {
        "schema": "campaign138_d8_measure_check_checkpoint/v1",
        "source_sha256": source_hash,
        "stage": "start",
        "complete": False,
        "orbit_results": reconstructed,
    }
    independent_scan.atomic_json(checkpoint_path, state)

    def update(stage: str, **extra: object) -> None:
        state.update(stage=stage, elapsed_ms=int(1000 * (time.monotonic() - began)), **extra)
        independent_scan.atomic_json(checkpoint_path, state)

    def timeout() -> None:
        if not state["complete"]:
            update("hard_timeout", hard_timeout_seconds=args.hard_timeout_seconds)
            os._exit(124)

    alarm = threading.Timer(args.hard_timeout_seconds, timeout)
    alarm.daemon = True
    alarm.start()
    try:
        source = json.loads(source_path.read_text(encoding="utf-8"))
        preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        meta = next(item for item in metadata["records"] if item["family_key"] == [16, 8, 4])
        library_path = Path(metadata["library_root"]) / meta["file"]
        action, parsed = independent_library.parse_action(library_path, meta)
        named = dict(zip(parsed["names"], action))
        group = independent_scan.sympy_elements(action)
        module = independent_scan.sympy_elements(
            tuple(named[name] for name in parsed["names"][3:])
        )
        cosets, coset_of, qtable, qone = independent_scan.quotient_data(group, module)
        update("group_ready", group_order=len(group), module_order=len(module))

        px, py, quotient_group = independent_scan.canonical_group()
        target, target_counts = independent_scan.target_keys(quotient_group, px, py)
        quotient_ordered = sorted(quotient_group)
        quotient_index = {value: index for index, value in enumerate(quotient_ordered)}
        selected = next(item for item in preflight["results"] if item["family_key"] == [16, 8, 4])
        orbits = selected["marked_pair_orbits"]
        source_results = source["orbit_results"]
        completed = {item["orbit_index"] for item in reconstructed}
        elements = sorted(group)
        for orbit in orbits[: len(source_results)]:
            index = orbit["orbit_index"]
            if index in completed:
                continue
            update("orbit", current_orbit=index)
            s, t = tuple(orbit["S"]), tuple(orbit["T"])
            w = independent_scan.compose(s, independent_scan.invert(t))
            x = independent_scan.power(w, 2)
            y = independent_scan.compose(
                independent_scan.compose(independent_scan.invert(s), x), s
            )
            qmap = independent_scan.quotient_isomorphism(
                coset_of[x], coset_of[y], qone, qtable, px, py
            )
            result = independent_scan.source_result(
                elements, coset_of, qmap, quotient_index, target, s, t
            )
            result.update(
                orbit_index=index,
                S_sha256=independent_scan.sha_obj(list(s)),
                T_sha256=independent_scan.sha_obj(list(t)),
            )
            reconstructed.append(result)
            reconstructed.sort(key=lambda item: item["orbit_index"])
            state["orbit_results"] = reconstructed
            update("orbit_complete", completed_orbit=index)

        fields = (
            "orbit_index", "S_sha256", "T_sha256", "source_shadow_count",
            "reduced_key_count", "raw_image_size", "missing_key_count",
            "first_missing_key", "reduced_keys",
        )
        checks = {
            "schema": source["schema"] == "campaign138_d8_measure/v1",
            "input_binding": (
                source["input_sha256"]["preflight"] == independent_scan.sha_file(preflight_path)
                and source["input_sha256"]["metadata"] == independent_scan.sha_file(metadata_path)
                and source["input_sha256"]["preflight_check"]
                == independent_scan.sha_file(Path("crosscheck/verdicts/campaign138_higher_perfect_preflight_v1_20260815.json"))
            ),
            "group_scalars": len(group) == 129024 and len(module) == 256 and len(cosets) == 504,
            "target": (
                len(target) == 54
                and [list(value) for value in sorted(target)] == source["target_keys"]
                and target_counts == source["target_scan"]
            ),
            "orbit_count": len(reconstructed) == len(source_results),
            "orbit_values": all(
                all(actual[field] == expected[field] for field in fields)
                and actual["source_scan"] == expected["source_scan"]
                for actual, expected in zip(reconstructed, source_results)
            ),
            "positive_control": source["positive_control"]["passed"],
            "stop_rule": (
                (source["first_loss"] is not None and source["stopped_at_first_loss"])
                or (
                    source["first_loss"] is None
                    and not source["stopped_at_first_loss"]
                    and source["all_frozen_orbits_consumed"]
                    and len(source_results) == 32
                )
            ),
            "noncontact": source["noncontact"] == {
                "u": False,
                "c": False,
                "sealed_three_quantities": False,
                "sealed_K5": False,
            },
        }
        verdict = {
            "schema": "campaign138_d8_measure_check/v1",
            "source_sha256": source_hash,
            "checker_sha256": independent_scan.sha_file(Path(__file__)),
            "checks": checks,
            "all_checks_true": all(checks.values()),
            "reconstructed": {
                "target_key_count": len(target),
                "orbit_count": len(reconstructed),
                "raw_image_size_distribution": {
                    str(value): sum(item["raw_image_size"] == value for item in reconstructed)
                    for value in sorted({item["raw_image_size"] for item in reconstructed})
                },
                "source_shadow_count_distribution": {
                    str(value): sum(item["source_shadow_count"] == value for item in reconstructed)
                    for value in sorted({item["source_shadow_count"] for item in reconstructed})
                },
            },
        }
        independent_scan.atomic_json(output_path, verdict)
        state["complete"] = True
        update("complete", all_checks_true=verdict["all_checks_true"], output_sha256=independent_scan.sha_file(output_path))
        print(json.dumps(verdict["reconstructed"], sort_keys=True))
        if not verdict["all_checks_true"]:
            raise SystemExit(2)
    finally:
        alarm.cancel()


if __name__ == "__main__":
    main()
