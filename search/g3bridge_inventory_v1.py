#!/usr/bin/env python3
"""Task 129 producer: finite inventory scan and modular size gate.

The finite universe is pinned to the artifacts named by the vNext design:
the explicit task-125 refinements, the 83 marked records, and the atlas CSV.
The task-125 effective dovetail is not treated as a completed infinite scan.
No arithmetic image, blind payload, u/c payload, or sealed quantity is read.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAP_ROOT = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / (
    "GAP-4.16.0/runtime/opt/gap-4.16.0"
)
ATLAS_MINDEG = GAP_ROOT / "pkg/atlasrep/gap/mindeg.g"
ATLAS_BBOX = GAP_ROOT / "pkg/atlasrep/gap/bbox.gd"
CTBL_BRAUER = GAP_ROOT / "pkg/ctbllib/data/ctbline1.tbl"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def atlasrep_minimum() -> dict[str, object]:
    text = ATLAS_MINDEG.read_text(encoding="utf-8")
    characteristic = re.search(
        r'\["L2\(8\)",\["Characteristic",3\],(\d+),"computed \(char\. table\)"\]',
        text,
    )
    field_size = re.search(
        r'\["L2\(8\)",\["Size",3\],(\d+),"computed \(char\. table\)"\]',
        text,
    )
    complete = (
        '["L2(8)",["Characteristic",3,"complete"],true,'
        '"computed (char. table)"]'
    )
    if characteristic is None or field_size is None or complete not in text:
        raise RuntimeError("AtlasRep minimum-degree records were not found")
    return {
        "characteristic_3_minimum": int(characteristic.group(1)),
        "field_F3_minimum": int(field_size.group(1)),
        "characteristic_3_complete": True,
        "source": str(ATLAS_MINDEG),
        "source_sha256": digest(ATLAS_MINDEG),
    }


def attempt_gap(script: Path, raw_path: Path) -> dict[str, object]:
    started = time.time_ns()
    command = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(ROOT / "gap.ps1"),
        str(script.relative_to(ROOT)),
    ]
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        fresh_raw = raw_path.exists() and raw_path.stat().st_mtime_ns >= started
        record: dict[str, object] = {
            "wrapper": "gap.ps1",
            "returncode": result.returncode,
            "fresh_raw_created": fresh_raw,
            "stdout_tail": result.stdout[-1200:],
            "stderr_tail": result.stderr[-1200:],
        }
        if fresh_raw:
            record["raw_sha256"] = digest(raw_path)
            record["raw"] = json.loads(raw_path.read_text(encoding="utf-8"))
        return record
    except subprocess.TimeoutExpired:
        return {
            "wrapper": "gap.ps1",
            "returncode": None,
            "fresh_raw_created": False,
            "timeout_seconds": 30,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="search/certs/g3bridge_inventory_v1_20260813.json",
    )
    parser.add_argument(
        "--checkpoint",
        default="search/certs/g3bridge_inventory_v1_checkpoint.json",
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    started = time.monotonic()
    state: dict[str, object] = {
        "schema": "g3bridge_inventory_checkpoint/v1",
        "stage": "start",
        "complete": False,
        "raw_image_size": None,
    }
    atomic_json(checkpoint, state)

    def update(stage: str, **fields: object) -> None:
        state.update(
            stage=stage,
            elapsed_ms=int(1000 * (time.monotonic() - started)),
            **fields,
        )
        atomic_json(checkpoint, state)

    def hard_timeout() -> None:
        if not state.get("complete"):
            update("hard_timeout")
            os._exit(124)

    timer = threading.Timer(args.hard_timeout_seconds, hard_timeout)
    timer.daemon = True
    timer.start()
    try:
        repo_inputs = [
            "ops/inbox_codex/sol_task_129_g3bridge.txt",
            "docs/notes/ab_instrument_redesign_v2.md",
            "sol/sol_reply_125_phase2_p3p5.md",
            "search/certs/d972_phase2_coord_v1_20260813.json",
            "search/certs/d972_entangled_hand2_v1_20260813.json",
            "search/certs/wincnotn_v1_20260812.json",
            "search/certs/iso_census83_deep15_v1_20260812.json",
            "search/probe/atlas_stats/atlas_features_v1.csv",
            "docs/notes/atlas_stats_survey_v2.md",
            "search/d972_phase2b_nonsplit_v1.py",
        ]
        input_hashes = {name: digest(ROOT / name) for name in repo_inputs}

        phase2 = json.loads(
            (ROOT / "search/certs/d972_phase2_coord_v1_20260813.json").read_text(
                encoding="utf-8"
            )
        )
        receipts = phase2["group_order_receipts"]
        gn_orders = {int(k): int(v) for k, v in receipts["canonical_gn_orders"].items()}
        roof_orders = {int(k): int(v) for k, v in receipts["roof_orders"].items()}
        roles = {
            9: "base_M",
            27: "task125_N1",
            36: "task125_N2_cross_probe",
            108: "task125_L2_cumulative",
        }
        explicit_rows = []
        for level in (9, 27, 36, 108):
            g_order = gn_orders[level]
            e_order = roof_orders[level]
            if e_order != 504 * g_order or g_order % 108:
                raise RuntimeError("task125 order receipt mismatch")
            v_order = g_order // 108
            explicit_rows.append(
                {
                    "inventory_id": f"K{level}_cap_NS4",
                    "role": roles[level],
                    "isolated_typed": True,
                    "E_order": e_order,
                    "V_order": v_order,
                    "G_vN_0": True,
                    "G_vN_1": level != 9,
                    "G_vN_2": v_order != 1,
                    "P_action_on_V_nontrivial": False,
                    "G3_action_on_V_nontrivial": None,
                    "G_vN_3": False,
                    "tensor_type_raw_boolean": False,
                    "direct_product_order_identity": e_order == 504 * g_order,
                    "reason_code": "P_factor_acts_trivially_on_kernel_of_Glevel_to_G3",
                }
            )
        update("task125_inventory", explicit_count=len(explicit_rows))

        target83 = json.loads(
            (ROOT / "search/certs/wincnotn_v1_20260812.json").read_text(
                encoding="utf-8"
            )
        )["win_cnotn_target_members"]
        if len(target83) != 83:
            raise RuntimeError("83-record inventory count changed")
        b3_orders = [int(row["index"]) for row in target83]
        if max(b3_orders) > 2000:
            raise RuntimeError("83-record band boundary changed")
        deep15 = json.loads(
            (ROOT / "search/certs/iso_census83_deep15_v1_20260812.json").read_text(
                encoding="utf-8"
            )
        )["deep15_windows"]
        deep15_isolated_candidates = [
            row for row in deep15 if row["all_kernel_trivial"]
        ]
        target83_summary = {
            "marked_record_count": len(target83),
            "B3_quotient_order_min": min(b3_orders),
            "B3_quotient_order_max": max(b3_orders),
            "G_vN_0_false_count": sum(order < 54432 for order in b3_orders),
            "order_obstruction": (
                "G_vN_0 would give E -> P x G3 and hence a B3 quotient "
                "of order at least 54432; every recorded B3 quotient has order <=2000"
            ),
            "deep15_record_count": len(deep15),
            "deep15_all_kernel_trivial_record_count": len(
                deep15_isolated_candidates
            ),
            "deep15_all_kernel_trivial_id_groups": sorted(
                {tuple(row["id_group"]) for row in deep15_isolated_candidates}
            ),
            "tensor_type_hit_count": 0,
        }
        update("target83_inventory", target83_count=len(target83))

        atlas_path = ROOT / "search/probe/atlas_stats/atlas_features_v1.csv"
        with atlas_path.open(encoding="utf-8", newline="") as source:
            atlas_rows = list(csv.DictReader(source))
        typed_atlas = [
            row
            for row in atlas_rows
            if re.search(r"isolated\s*=\s*TRUE", row.get("note", ""), re.I)
        ]
        if len(typed_atlas) != 1 or not typed_atlas[0]["window_id"].startswith("W-5"):
            raise RuntimeError("atlas isolated-typed row inventory changed")
        w5_order = int(typed_atlas[0]["G_order"])
        atlas_summary = {
            "csv_record_count": len(atlas_rows),
            "isolated_typed_record_count": len(typed_atlas),
            "isolated_typed_rows": [
                {
                    "window_id": typed_atlas[0]["window_id"],
                    "E_order": w5_order,
                    "G_vN_0": False,
                    "reason_code": "E_order_not_divisible_by_order_P_times_G3",
                    "tensor_type_raw_boolean": False,
                }
            ],
            "isolated_untyped_or_unknown_record_count": len(atlas_rows)
            - len(typed_atlas),
            "tensor_type_hit_count": 0,
        }

        controls = [
            {
                "inventory_id": "K3_cap_NS4",
                "E_order": 54432,
                "V_order": 1,
                "G_vN_0": True,
                "G_vN_1": False,
                "G_vN_2": False,
                "G_vN_3": False,
                "tensor_type_raw_boolean": False,
            },
            {
                "inventory_id": "NS4",
                "E_order": 504,
                "G_vN_0": False,
                "tensor_type_raw_boolean": False,
            },
            {
                "inventory_id": "K3",
                "E_order": 108,
                "G_vN_0": False,
                "tensor_type_raw_boolean": False,
            },
        ]
        inventory = {
            "universe_pin": {
                "task125_explicit_refinements": 4,
                "target83_marked_records": 83,
                "atlas_csv_records": len(atlas_rows),
                "task125_effective_dovetail_exhausted": False,
                "global_absence_claimed": False,
            },
            "task125_rows": explicit_rows,
            "target83": target83_summary,
            "atlas": atlas_summary,
            "controls": controls,
            "finite_inventory_tensor_type_hit_count": 0,
        }

        raw_gap = ROOT / "search/certs/g3bridge_moddim_v1_gap_raw_20260813.json"
        gap_attempt = attempt_gap(ROOT / "search/g3bridge_moddim_v1.g", raw_gap)
        min_degree = atlasrep_minimum()
        if min_degree["field_F3_minimum"] != 7:
            raise RuntimeError("unexpected AtlasRep F3 minimum degree")
        orbit = json.loads(
            (ROOT / "search/certs/d972_entangled_hand2_v1_20260813.json").read_text(
                encoding="utf-8"
            )
        )["surjective_kernel_orbit"]
        if orbit["intersection_quotient_abelianization_order"] != 4:
            raise RuntimeError("G3 abelianization receipt changed")
        dimension_gate = {
            "P": {
                "group": "PSL(2,8)",
                "order": 504,
                "field": "F3",
                "minimum_nontrivial_module_dimension": 7,
                "atlasrep_record": min_degree,
            },
            "G3": {
                "order": 108,
                "abelianization_order": 4,
                "minimum_nontrivial_module_dimension": 1,
                "one_dimensional_character_reason": (
                    "a nontrivial quotient C2 acts through F3^x"
                ),
            },
            "gap_attempt": gap_attempt,
            "gap_startup_unavailable_in_this_run": gap_attempt["returncode"] != 0,
            "package_data_fallback_used": gap_attempt["returncode"] != 0,
            "external_sources": {
                str(ATLAS_BBOX): digest(ATLAS_BBOX),
                str(CTBL_BRAUER): digest(CTBL_BRAUER),
            },
        }
        update("dimension_gate", dim_V_P=7, dim_V_G3=1)

        size_rows = []
        for dim_g3 in (1, 2):
            dim_v = 7 * dim_g3
            e_order = 54432 * (3**dim_v)
            roof_upper = 27 * e_order
            permutation_degree_floor = 1
            while math.factorial(permutation_degree_floor) < e_order:
                permutation_degree_floor += 1
            tuple_bytes = sys.getsizeof(tuple(range(permutation_degree_floor)))
            tuple_floor = tuple_bytes * e_order
            size_rows.append(
                {
                    "dim_V_P": 7,
                    "dim_V_G3": dim_g3,
                    "dim_V": dim_v,
                    "E_order": e_order,
                    "PB3_over_K9_cap_NE_order_exact": None,
                    "PB3_over_K9_cap_NE_order_lower_bound": e_order,
                    "PB3_over_K9_cap_NE_order_upper_bound": roof_upper,
                    "common_quotient_order_lower_bound": 108,
                    "common_quotient_order_upper_bound": 2916,
                    "faithful_permutation_degree_lower_bound": permutation_degree_floor,
                    "python_tuple_bytes_at_degree_lower_bound": tuple_bytes,
                    "one_tuple_per_E_element_bytes": tuple_floor,
                    "tuple_floor_GiB": tuple_floor / (2**30),
                    "within_8GiB_existing_tuple_floor": tuple_floor
                    <= 8 * (2**30),
                }
            )
        minimum_row = size_rows[0]
        if minimum_row["E_order"] != 119042784:
            raise RuntimeError("minimum size arithmetic mismatch")
        scale_gate = {
            "formula_E_order": "54432 * 3^dim_V",
            "formula_roof_order": "|G9|*|E|/|Q| with 108 <= |Q| <= 2916",
            "roof_exact_order_before_E_construction": None,
            "rows": size_rows,
            "machine_physical_memory_bytes": 8 * (2**30),
            "gap_wrapper_heap_cap_bytes": 2 * (2**30),
            "existing_enumerator_materializes_elements": True,
            "permutation_degree_floor_reason": "|E| <= d! for E embedded in S_d",
            "tuple_floor_excludes_set_table_and_point_objects": True,
            "existing_enumerator_source_refs": [
                "search/d972_phase2_v1.g:37,167",
                "search/d972_phase2b_nonsplit_v1.py:515,698",
            ],
            "minimum_case_within_existing_enumerator_memory_gate": False,
            "compact_symbolic_extension_not_assessed_as_measurement_backend": True,
        }

        result = {
            "schema": "g3bridge_inventory/v1",
            "run_id": "g3bridge-inventory-"
            + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "generated_by": {
                "script": "search/g3bridge_inventory_v1.py",
                "python": os.sys.version.split()[0],
            },
            "input_sha256": input_hashes,
            "inventory_scan": inventory,
            "dimension_gate": dimension_gate,
            "scale_gate": scale_gate,
            "stage_boundary": {
                "stage_reached": 2,
                "inventory_scan_performed": True,
                "finite_inventory_tensor_type_hit_count": 0,
                "dimension_gate_performed": True,
                "E_constructed": False,
                "BLIND_vNext_machine_gate_performed": False,
                "P_vN_1_instantiated": False,
                "P_vN_1_frozen_values_untouched": [972, 324],
                "blind_declaration_created": False,
                "rigidity_measurement_performed": False,
                "pair_target_formed": False,
                "reduction_image_set_formed": False,
                "raw_image_size": None,
                "status": "UNKNOWN",
                "stop_reason": "minimum_E_case_exceeds_existing_enumerator_tuple_memory_gate",
            },
            "scope": {
                "u_touched": False,
                "c_touched": False,
                "sealed_quantities_touched": False,
                "sealed_k5_touched": False,
                "preregistered_quantities_read": False,
                "finite_depth_B_type_recognition": False,
            },
            "elapsed_ms": int(1000 * (time.monotonic() - started)),
        }
        atomic_json(output, result)
        state["complete"] = True
        update("complete", output=str(output.relative_to(ROOT)))
        return 0
    finally:
        timer.cancel()


if __name__ == "__main__":
    raise SystemExit(main())
