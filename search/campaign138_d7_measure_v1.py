#!/usr/bin/env python3
"""Prospectively registered reduction scan for the d=7 perfect extension.

The source-generation test is deliberately relaxed to generation after
quotienting by the elementary 2-kernel.  Consequently each measured source
image is an upper bound for the image obtained with the exact generation
condition.  A missing target key is therefore load-bearing; a full relaxed
image is only a negative result for this detector.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import campaign138_d7_preflight_v1 as pre
import d972_phase2b_nonsplit_v1 as core


ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / "search/certs/campaign138_d7_preflight_v1_20260815.json"
PREFLIGHT_CHECK = ROOT / "crosscheck/verdicts/campaign138_d7_preflight_v1_20260815.json"
OLD_CONTROL = ROOT / "search/certs/d972_phase2b_nonsplit_v1_20260813.json"
PREREG = ROOT / "search/certs/campaign138_d7_measure_prereg_v1_20260815.json"
LABEL = "L2(8) N 2^6 E 2^1 II"


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha_obj(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="search/certs/campaign138_d7_measure_v1_20260815.json",
    )
    parser.add_argument(
        "--checkpoint",
        default="search/certs/campaign138_d7_measure_v1_checkpoint.json",
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=240)
    args = parser.parse_args()
    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    started = time.monotonic()

    prereg_hash = sha_file(PREREG)
    prior_results: list[dict] = []
    if checkpoint.exists():
        prior = json.loads(checkpoint.read_text(encoding="utf-8"))
        if (
            prior.get("schema") == "campaign138_d7_measure_checkpoint/v1"
            and prior.get("preregistration_sha256") == prereg_hash
        ):
            prior_results = list(prior.get("orbit_results", []))

    state: dict[str, object] = {
        "schema": "campaign138_d7_measure_checkpoint/v1",
        "preregistration_sha256": prereg_hash,
        "stage": "start",
        "complete": False,
        "orbit_results": prior_results,
    }
    atomic_json(checkpoint, state)

    def update(stage: str, **fields: object) -> None:
        state.update(
            stage=stage,
            elapsed_ms=int(1000 * (time.monotonic() - started)),
            **fields,
        )
        atomic_json(checkpoint, state)

    def watchdog() -> None:
        time.sleep(args.hard_timeout_seconds)
        if not state.get("complete"):
            update("hard_timeout", hard_timeout_seconds=args.hard_timeout_seconds)
            os._exit(124)

    threading.Thread(target=watchdog, daemon=True).start()

    try:
        prereg = json.loads(PREREG.read_text(encoding="utf-8"))
        preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
        preflight_check = json.loads(PREFLIGHT_CHECK.read_text(encoding="utf-8"))
        old_control = json.loads(OLD_CONTROL.read_text(encoding="utf-8"))
        frozen_hashes_ok = (
            prereg["blind_before_measurement"]
            and prereg["input_sha256"]["preflight"] == sha_file(PREFLIGHT)
            and prereg["input_sha256"]["preflight_check"] == sha_file(PREFLIGHT_CHECK)
            and prereg["input_sha256"]["old_control"] == sha_file(OLD_CONTROL)
            and preflight_check["all_checks_true"]
            and preflight_check["source_sha256"] == sha_file(PREFLIGHT)
        )
        if not frozen_hashes_ok:
            raise RuntimeError("frozen input mismatch")
        old_raw = old_control["measurement"]["raw_image_size"]
        old_target = old_control["measurement"]["target_roof_shadow_count"]
        old_control_passed = old_raw == 972 and old_target == 972
        if not old_control_passed:
            raise RuntimeError("old positive control failed")
        update("inputs_bound", old_control_raw=old_raw)

        library_text = pre.LIBRARY.read_text(encoding="utf-8", errors="replace")
        entry = pre.parse_entry(library_text, LABEL)
        action, degree = pre.permutation_action(entry)
        named = dict(zip(entry["generator_names"], action))
        group = pre.closure(action)
        module_generators = tuple(named[name] for name in entry["generator_names"][3:])
        module = pre.closure(module_generators)
        one = core.identity(degree)
        normal = all(
            core.conjugate(value, acting) in module
            for value in module_generators
            for acting in action[:3]
        )
        elementary = len(module) == 128 and all(
            value == one or core.element_order(value) == 2 for value in module
        )
        if not (
            degree == 112
            and len(group) == 64512
            and len(module) == 128
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
        target_positive_control = (
            len(target_keys) == 54
            and 18 * len(target_keys) == 972
            and bool(target_counts["bookkeeping_identity"])
        )
        if not target_positive_control:
            raise RuntimeError("target positive control failed")
        update("target_ready", target_key_count=len(target_keys))

        selected = next(
            item for item in preflight["candidates"] if item["family_key"] == [16, 7, 3]
        )
        orbits = selected["marked_pair_orbits"]
        if [item["orbit_index"] for item in orbits] != list(range(16)):
            raise RuntimeError("frozen orbit universe mismatch")
        results_by_index = {
            int(item["orbit_index"]): item for item in state["orbit_results"]
        }
        first_loss = next(
            (item for item in state["orbit_results"] if item.get("first_missing_key") is not None),
            None,
        )
        source_elements = sorted(group)

        for orbit in orbits:
            orbit_index = int(orbit["orbit_index"])
            if first_loss is not None or orbit_index in results_by_index:
                continue
            S = tuple(orbit["S"])
            T = tuple(orbit["T"])
            if (
                sha_obj(list(S)) != orbit["S_sha256"]
                or sha_obj(list(T)) != orbit["T_sha256"]
            ):
                raise RuntimeError("marked array digest mismatch")
            W = core.mul(S, core.inverse(T))
            X = core.power(W, 2)
            Y = core.mul(core.mul(core.inverse(S), X), S)
            qX, qY = coset_of[X], coset_of[Y]
            quotient_generated = len(
                core.quotient_closure((qX, qY), qone, qmul)
            ) == 504
            quotient_iso_ok, quotient_to_p = core.quotient_to_p_hom(
                len(cosets), qone, qX, qY, qmul, pX, pY
            )
            if not quotient_generated or not quotient_iso_ok:
                raise RuntimeError("marked quotient gate failed")

            def relaxed_generation(left: core.Perm, right: core.Perm) -> bool:
                qleft, qright = coset_of[left], coset_of[right]
                return len(
                    core.quotient_closure((qleft, qright), qone, qmul)
                ) == 504

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
                raise RuntimeError("reduction is not a target subset")
            missing = sorted(target_keys - reduced_keys)
            raw_image_size = 18 * len(reduced_keys)
            if raw_image_size < 324:
                raise RuntimeError("internal positive-control floor failed")
            first_missing_key = list(missing[0]) if missing else None
            result = {
                "orbit_index": orbit_index,
                "S_sha256": orbit["S_sha256"],
                "T_sha256": orbit["T_sha256"],
                "marked_orders": {
                    "S": core.element_order(S),
                    "T": core.element_order(T),
                    "W": core.element_order(W),
                    "X": core.element_order(X),
                    "Y": core.element_order(Y),
                },
                "source_scan": source_counts,
                "source_shadow_count": len(source_shadows),
                "reduced_key_count": len(reduced_keys),
                "raw_image_size": raw_image_size,
                "first_missing_key": first_missing_key,
                "missing_key_count": len(missing),
                "reduced_keys": [list(value) for value in sorted(reduced_keys)],
                "necessary_condition_relaxation": True,
            }
            state["orbit_results"].append(result)
            state["orbit_results"].sort(key=lambda item: item["orbit_index"])
            update("orbit_complete", completed_orbit=orbit_index)
            if first_missing_key is not None:
                first_loss = result
                break

        complete = first_loss is not None or len(state["orbit_results"]) == len(orbits)
        if not complete:
            raise RuntimeError("incomplete without timeout")
        status = "RAW_LOSS" if first_loss is not None else "NO_LOSS_IN_RELAXED_DETECTOR"
        target_key_records = [list(value) for value in sorted(target_keys)]
        cert = {
            "schema": "campaign138_d7_measure/v1",
            "run_id": "campaign138-d7-measure-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "status": status,
            "generated_by": {
                "script": "search/campaign138_d7_measure_v1.py",
                "tool": "Python 3.13 + SymPy 1.14",
                "producer_sha256": sha_file(Path(__file__)),
            },
            "preregistration": {
                "path": "search/certs/campaign138_d7_measure_prereg_v1_20260815.json",
                "sha256": prereg_hash,
                "blind_before_measurement": True,
            },
            "input_sha256": {
                "preflight": sha_file(PREFLIGHT),
                "preflight_check": sha_file(PREFLIGHT_CHECK),
                "old_control": sha_file(OLD_CONTROL),
                "library": sha_file(pre.LIBRARY),
            },
            "candidate": {
                "family_key": [16, 7, 3],
                "label": LABEL,
                "degree": degree,
                "group_order": len(group),
                "module_order": len(module),
                "quotient_order": len(cosets),
                "marked_orbit_count": len(orbits),
            },
            "positive_control": {
                "old_raw_image_size": old_raw,
                "old_target_roof_shadow_count": old_target,
                "canonical_target_key_count": len(target_keys),
                "canonical_target_roof_shadow_count": 18 * len(target_keys),
                "passed": old_control_passed and target_positive_control,
            },
            "measurement_semantics": {
                "source_generation": "surjective after quotient by the full 128-element kernel",
                "actual_source_images_are_subset": True,
                "missing_target_key_is_load_bearing": True,
                "full_relaxed_image_has_only_negative_force": True,
                "rows_per_marked_orbit": 6 * 64512,
                "roof_fibre_per_target_key": 18,
            },
            "target_scan": target_counts,
            "target_keys": target_key_records,
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
            "elapsed_ms_this_invocation": int(1000 * (time.monotonic() - started)),
        }
        atomic_json(output, cert)
        state["complete"] = True
        update("complete", status=status, output_sha256=sha_file(output))
        print(json.dumps({
            "status": status,
            "orbit_results": len(state["orbit_results"]),
            "first_loss": first_loss,
            "output": str(output),
        }, sort_keys=True))
        return 0
    except BaseException as exc:
        update("error", error_type=type(exc).__name__, error=str(exc))
        raise


if __name__ == "__main__":
    raise SystemExit(main())
