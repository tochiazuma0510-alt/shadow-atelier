#!/usr/bin/env python3
"""Prospectively registered scan of all [16,8,4] marked orbits."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import campaign138_higher_perfect_preflight_v1 as pre
import d972_phase2b_nonsplit_v1 as core


ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / "search/certs/campaign138_higher_perfect_preflight_v1_20260815.json"
PREFLIGHT_CHECK = ROOT / "crosscheck/verdicts/campaign138_higher_perfect_preflight_v1_20260815.json"
METADATA = ROOT / "search/certs/campaign138_perfect_metadata_v1_20260815.json"
OLD_CONTROL = ROOT / "search/certs/campaign138_d7_measure_v1_20260815.json"
OLD_CONTROL_CHECK = ROOT / "crosscheck/verdicts/campaign138_d7_measure_v1_20260815.json"
PREREG = ROOT / "search/certs/campaign138_d8_measure_prereg_v1_20260815.json"
FAMILY_KEY = [16, 8, 4]


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", default="search/certs/campaign138_d8_measure_v1_20260815.json"
    )
    parser.add_argument(
        "--checkpoint", default="search/certs/campaign138_d8_measure_v1_checkpoint.json"
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=600)
    args = parser.parse_args()
    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    began = time.monotonic()
    prereg_hash = sha_file(PREREG)
    prior_results: list[dict] = []
    if checkpoint.exists():
        old_state = json.loads(checkpoint.read_text(encoding="utf-8"))
        if (
            old_state.get("schema") == "campaign138_d8_measure_checkpoint/v1"
            and old_state.get("preregistration_sha256") == prereg_hash
        ):
            prior_results = list(old_state.get("orbit_results", []))
    state: dict[str, object] = {
        "schema": "campaign138_d8_measure_checkpoint/v1",
        "preregistration_sha256": prereg_hash,
        "stage": "start",
        "complete": False,
        "orbit_results": prior_results,
    }
    atomic_json(checkpoint, state)

    def update(stage: str, **fields: object) -> None:
        state.update(stage=stage, elapsed_ms=int(1000 * (time.monotonic() - began)), **fields)
        atomic_json(checkpoint, state)

    def timeout() -> None:
        time.sleep(args.hard_timeout_seconds)
        if not state["complete"]:
            update("hard_timeout", hard_timeout_seconds=args.hard_timeout_seconds)
            os._exit(124)

    threading.Thread(target=timeout, daemon=True).start()
    try:
        prereg = json.loads(PREREG.read_text(encoding="utf-8"))
        preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
        preflight_check = json.loads(PREFLIGHT_CHECK.read_text(encoding="utf-8"))
        metadata = json.loads(METADATA.read_text(encoding="utf-8"))
        old_control = json.loads(OLD_CONTROL.read_text(encoding="utf-8"))
        old_control_check = json.loads(OLD_CONTROL_CHECK.read_text(encoding="utf-8"))
        frozen_inputs = {
            "preflight": sha_file(PREFLIGHT),
            "preflight_check": sha_file(PREFLIGHT_CHECK),
            "metadata": sha_file(METADATA),
            "old_control": sha_file(OLD_CONTROL),
            "old_control_check": sha_file(OLD_CONTROL_CHECK),
        }
        if (
            not prereg["blind_before_measurement"]
            or prereg["input_sha256"] != frozen_inputs
            or not preflight_check["all_checks_true"]
            or not old_control_check["all_checks_true"]
        ):
            raise RuntimeError("frozen input mismatch")
        old_distribution = {
            str(key): sum(item["raw_image_size"] == key for item in old_control["orbit_results"])
            for key in sorted({item["raw_image_size"] for item in old_control["orbit_results"]})
        }
        if old_distribution != {"972": 16}:
            raise RuntimeError("bound positive control mismatch")
        selected = next(item for item in preflight["results"] if item["family_key"] == FAMILY_KEY)
        if not (
            selected["status"] == "CONSTRUCTED"
            and selected["group_order"] == 129024
            and selected["module_order"] == 256
            and selected["module_element_order_distribution"] == {"1": 1, "2": 255}
            and selected["generating_orbit_count"] == 32
        ):
            raise RuntimeError("local preflight gate failed")
        update("inputs_bound")

        meta = next(item for item in metadata["records"] if item["family_key"] == FAMILY_KEY)
        record_meta = {**meta, "library_root": metadata["library_root"]}
        library_path = Path(record_meta["library_root"]) / record_meta["file"]
        parsed = pre.parse_record(library_path, record_meta["label"], record_meta["order_if_2_kernel"])
        action, block_sizes = pre.permutation_action(parsed)
        named = dict(zip(parsed["names"], action))
        group = pre.closure(action)
        module_generators = tuple(named[name] for name in parsed["names"][3:])
        module = pre.closure(module_generators)
        degree = len(action[0])
        one = core.identity(degree)
        normal = all(
            core.conjugate(value, acting) in module
            for value in module_generators
            for acting in action[:3]
        )
        elementary = len(module) == 256 and all(
            value == one or core.element_order(value) == 2 for value in module
        )
        if not (
            block_sizes == [112, 112]
            and degree == 224
            and len(group) == 129024
            and normal
            and elementary
        ):
            raise RuntimeError("group/kernel positive control failed")
        cosets, coset_of, qmul = core.make_quotient(group, module)
        qone = coset_of[one]
        if len(cosets) != 504:
            raise RuntimeError("quotient order mismatch")
        update("group_ready", degree=degree, group_order=len(group), module_order=len(module))

        pS, pT, pX, pY, target_group = core.canonical_p()
        del pS, pT
        target_elements = sorted(target_group)
        target_index = {value: index for index, value in enumerate(target_elements)}

        def target_generation(left: core.Perm, right: core.Perm) -> bool:
            return len(core.closure((left, right))) == 504

        target_shadows, target_counts = core.scan_shadows(
            target_elements, pX, pY, target_generation
        )
        target_keys = {(m, target_index[f]) for m, f in target_shadows}
        if len(target_keys) != 54 or not target_counts["bookkeeping_identity"]:
            raise RuntimeError("target positive control failed")
        update("target_ready", target_key_count=len(target_keys))

        orbits = selected["marked_pair_orbits"]
        if [item["orbit_index"] for item in orbits] != list(range(32)):
            raise RuntimeError("frozen orbit universe mismatch")
        completed = {item["orbit_index"] for item in state["orbit_results"]}
        first_loss = next(
            (item for item in state["orbit_results"] if item["first_missing_key"] is not None),
            None,
        )
        source_elements = sorted(group)
        for orbit in orbits:
            orbit_index = orbit["orbit_index"]
            if first_loss is not None or orbit_index in completed:
                continue
            S, T = tuple(orbit["S"]), tuple(orbit["T"])
            W = core.mul(S, core.inverse(T))
            X = core.power(W, 2)
            Y = core.mul(core.mul(core.inverse(S), X), S)
            quotient_iso_ok, quotient_to_p = core.quotient_to_p_hom(
                len(cosets), qone, coset_of[X], coset_of[Y], qmul, pX, pY
            )
            if not quotient_iso_ok:
                raise RuntimeError("marked quotient gate failed")

            def relaxed_generation(left: core.Perm, right: core.Perm) -> bool:
                return len(core.quotient_closure(
                    (coset_of[left], coset_of[right]), qone, qmul
                )) == 504

            def progress(processed: int, counters: dict[str, int]) -> None:
                update(
                    "source_scan",
                    current_orbit=orbit_index,
                    current_processed=processed,
                    current_counters=dict(counters),
                )

            source_shadows, source_counts = core.scan_shadows(
                source_elements, X, Y, relaxed_generation, progress
            )
            reduced_keys = {
                (m, target_index[quotient_to_p[coset_of[f]]])
                for m, f in source_shadows
            }
            if not reduced_keys <= target_keys:
                raise RuntimeError("reduction subset failure")
            missing = sorted(target_keys - reduced_keys)
            raw_image_size = 18 * len(reduced_keys)
            if raw_image_size < 324:
                raise RuntimeError("internal positive-control floor failed")
            result = {
                "orbit_index": orbit_index,
                "S_sha256": orbit["S_sha256"],
                "T_sha256": orbit["T_sha256"],
                "source_scan": source_counts,
                "source_shadow_count": len(source_shadows),
                "reduced_key_count": len(reduced_keys),
                "raw_image_size": raw_image_size,
                "missing_key_count": len(missing),
                "first_missing_key": list(missing[0]) if missing else None,
                "reduced_keys": [list(value) for value in sorted(reduced_keys)],
                "necessary_condition_relaxation": True,
            }
            state["orbit_results"].append(result)
            state["orbit_results"].sort(key=lambda item: item["orbit_index"])
            update("orbit_complete", completed_orbit=orbit_index)
            if result["first_missing_key"] is not None:
                first_loss = result
                break

        complete = first_loss is not None or len(state["orbit_results"]) == len(orbits)
        if not complete:
            raise RuntimeError("incomplete without timeout")
        status = "RAW_LOSS" if first_loss is not None else "NO_LOSS_IN_RELAXED_DETECTOR"
        cert = {
            "schema": "campaign138_d8_measure/v1",
            "run_id": "campaign138-d8-measure-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "status": status,
            "generated_by": {
                "script": "search/campaign138_d8_measure_v1.py",
                "tool": "Python 3.13 + SymPy 1.14",
                "producer_sha256": sha_file(Path(__file__)),
            },
            "preregistration": {
                "path": "search/certs/campaign138_d8_measure_prereg_v1_20260815.json",
                "sha256": prereg_hash,
                "blind_before_measurement": True,
            },
            "input_sha256": frozen_inputs,
            "candidate": {
                "family_key": FAMILY_KEY,
                "label": selected["label"],
                "degree": degree,
                "group_order": len(group),
                "module_order": len(module),
                "quotient_order": len(cosets),
                "marked_orbit_count": len(orbits),
            },
            "positive_control": {
                "old_raw_image_size_distribution": old_distribution,
                "canonical_target_key_count": len(target_keys),
                "canonical_target_roof_shadow_count": 18 * len(target_keys),
                "passed": True,
            },
            "measurement_semantics": {
                "source_generation": "surjective after quotient by the full 256-element kernel",
                "actual_source_images_are_subset": True,
                "missing_target_key_is_load_bearing": True,
                "full_relaxed_image_has_only_negative_force": True,
                "rows_per_marked_orbit": 6 * 129024,
                "roof_fibre_per_target_key": 18,
            },
            "target_scan": target_counts,
            "target_keys": [list(value) for value in sorted(target_keys)],
            "orbit_results": state["orbit_results"],
            "first_loss": first_loss,
            "stopped_at_first_loss": first_loss is not None,
            "all_frozen_orbits_consumed": len(state["orbit_results"]) == len(orbits),
            "noncontact": {
                "u": False,
                "c": False,
                "sealed_three_quantities": False,
                "sealed_K5": False,
            },
            "endgame_scope": {
                "mode": "gentle",
                "PENT_W": "NOT_RUN",
                "B4_U10": "NOT_RUN",
                "required_order": "PENT_W-PASS -> B4/U-10",
                "B4_in_scope": False,
            },
            "elapsed_ms_this_invocation": int(1000 * (time.monotonic() - began)),
        }
        atomic_json(output, cert)
        state["complete"] = True
        update("complete", status=status, output_sha256=sha_file(output))
        print(json.dumps({
            "status": status,
            "orbit_results": len(state["orbit_results"]),
            "first_loss": first_loss,
        }, sort_keys=True))
        return 0
    except BaseException as exc:
        update("error", error_type=type(exc).__name__, error=str(exc))
        raise


if __name__ == "__main__":
    raise SystemExit(main())
