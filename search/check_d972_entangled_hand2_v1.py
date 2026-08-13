#!/usr/bin/env python3
"""Independent checker for d972_entangled_hand2/v1.

Only Python standard-library tuple permutations are used.  Kernel classes are
formed as simultaneous-conjugacy orbits in S3 (not with the producer's marked
kernel mapper).  G9 is reconstructed directly on 27 points.  No producer
module or SymPy helper is imported.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import threading
import time
from collections import Counter, deque
from itertools import permutations, product
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
PermutationTuple = tuple[int, ...]
SMALL_SYMMETRIC = tuple(tuple(value) for value in permutations(range(3)))
SMALL_IDENTITY: PermutationTuple = (0, 1, 2)


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def write_receipt(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def unit(degree: int) -> PermutationTuple:
    return tuple(range(degree))


def compose(first: PermutationTuple, second: PermutationTuple) -> PermutationTuple:
    return tuple(second[first[index]] for index in range(len(first)))


def reciprocal(value: PermutationTuple) -> PermutationTuple:
    result = [0] * len(value)
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)


def generated(generators: Iterable[PermutationTuple], degree: int | None = None) -> set[PermutationTuple]:
    generators = tuple(generators)
    if degree is None:
        degree = len(generators[0])
    identity = unit(degree)
    result = {identity}
    queue = deque([identity])
    steps = generators + tuple(reciprocal(value) for value in generators)
    while queue:
        current = queue.popleft()
        for step in steps:
            nxt = compose(current, step)
            if nxt not in result:
                result.add(nxt)
                queue.append(nxt)
    return result


def exponent_order(value: PermutationTuple) -> int:
    current = unit(len(value))
    for exponent in range(1, 1000):
        current = compose(current, value)
        if current == unit(len(value)):
            return exponent
    raise RuntimeError("order bound")


def formal_product(values: Iterable[PermutationTuple], degree: int) -> PermutationTuple:
    result = unit(degree)
    for value in reversed(tuple(values)):
        result = compose(result, value)
    return result


def conjugated(value: PermutationTuple, by: PermutationTuple) -> PermutationTuple:
    return compose(compose(reciprocal(by), value), by)


def orbit_of_pair(pair: tuple[PermutationTuple, PermutationTuple]) -> set[tuple[PermutationTuple, PermutationTuple]]:
    return {
        (conjugated(pair[0], actor), conjugated(pair[1], actor))
        for actor in SMALL_SYMMETRIC
    }


def signature(pair: tuple[PermutationTuple, PermutationTuple]) -> str:
    image_order = len(generated(pair))
    xy = formal_product(pair, 3)
    return (
        f"q{image_order}_o{exponent_order(pair[0])}"
        f"{exponent_order(pair[1])}{exponent_order(xy)}"
    )


def simultaneous_conjugacy_classes() -> list[dict[str, object]]:
    remaining = set(product(SMALL_SYMMETRIC, repeat=2))
    records = []
    while remaining:
        representative = min(remaining)
        orbit = orbit_of_pair(representative)
        remaining.difference_update(orbit)
        records.append({
            "kernel_id": signature(representative),
            "representative": representative,
            "members": orbit,
            "image_order": len(generated(representative)),
        })
    records.sort(key=lambda row: row["kernel_id"])
    signatures = [row["kernel_id"] for row in records]
    if len(signatures) != len(set(signatures)):
        raise RuntimeError("S3 pair signature is not unique on conjugacy orbits")
    return records


def transformed_theta(pair: tuple[PermutationTuple, PermutationTuple]) -> tuple[PermutationTuple, PermutationTuple]:
    return pair[1], pair[0]


def transformed_tau(pair: tuple[PermutationTuple, PermutationTuple]) -> tuple[PermutationTuple, PermutationTuple]:
    z = reciprocal(formal_product(pair, 3))
    return pair[1], z


def marked_map(
    domain_size: int,
    domain_pair: tuple[PermutationTuple, PermutationTuple],
    range_pair: tuple[PermutationTuple, PermutationTuple],
) -> tuple[bool, dict[PermutationTuple, PermutationTuple]]:
    domain_identity = unit(len(domain_pair[0]))
    range_identity = unit(len(range_pair[0]))
    table = {domain_identity: range_identity}
    queue = deque([domain_identity])
    steps = (
        (domain_pair[0], range_pair[0]),
        (reciprocal(domain_pair[0]), reciprocal(range_pair[0])),
        (domain_pair[1], range_pair[1]),
        (reciprocal(domain_pair[1]), reciprocal(range_pair[1])),
    )
    while queue:
        current = queue.popleft()
        for domain_step, range_step in steps:
            nxt = compose(current, domain_step)
            image = compose(table[current], range_step)
            if nxt in table:
                if table[nxt] != image:
                    return False, table
            else:
                table[nxt] = image
                queue.append(nxt)
    return len(table) == domain_size, table


def inserted(value: PermutationTuple, offset: int, total: int) -> PermutationTuple:
    result = list(range(total))
    for index, image in enumerate(value):
        result[offset + index] = offset + image
    return tuple(result)


def marked_dihedral(level: int) -> tuple[PermutationTuple, PermutationTuple]:
    rotation = tuple((index + 1) % level for index in range(level))
    reflection = tuple((-index) % level for index in range(level))
    reflected_rotation = compose(reflection, rotation)
    total = 3 * level
    x = compose(
        compose(inserted(rotation, 0, total), inserted(reflection, level, total)),
        inserted(reflection, 2 * level, total),
    )
    y = compose(
        compose(
            inserted(reflected_rotation, 0, total),
            inserted(rotation, level, total),
        ),
        inserted(reflected_rotation, 2 * level, total),
    )
    return x, y


def block_diagonal(values: tuple[PermutationTuple, ...]) -> PermutationTuple:
    result = []
    offset = 0
    for value in values:
        result.extend(offset + image for image in value)
        offset += len(value)
    return tuple(result)


def bracket(first: PermutationTuple, second: PermutationTuple) -> PermutationTuple:
    return compose(
        compose(compose(reciprocal(first), reciprocal(second)), first), second
    )


def commutator_group(
    group: set[PermutationTuple], generators: tuple[PermutationTuple, PermutationTuple]
) -> set[PermutationTuple]:
    seeds = [bracket(value, generator) for value in group for generator in generators]
    return generated(seeds, len(generators[0]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", default="search/certs/d972_entangled_hand2_v1_20260813.json"
    )
    parser.add_argument(
        "--output", default="search/certs/d972_entangled_hand2_v1_check_20260813.json"
    )
    parser.add_argument(
        "--checkpoint", default="search/certs/d972_entangled_hand2_v1_check_checkpoint.json"
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    source_path = ROOT / args.input
    output_path = ROOT / args.output
    checkpoint_path = ROOT / args.checkpoint
    started = time.monotonic()
    state: dict[str, object] = {
        "schema": "d972_entangled_hand2_check_checkpoint/v1",
        "stage": "start",
        "complete": False,
        "raw_image_size": None,
    }
    write_receipt(checkpoint_path, state)

    def update(stage: str, **fields: object) -> None:
        state.update(stage=stage, elapsed_ms=int(1000 * (time.monotonic() - started)), **fields)
        write_receipt(checkpoint_path, state)

    def timeout() -> None:
        if not state.get("complete"):
            update("hard_timeout")
            os._exit(124)

    timer = threading.Timer(args.hard_timeout_seconds, timeout)
    timer.daemon = True
    timer.start()
    try:
        source = json.loads(source_path.read_text(encoding="utf-8"))
        classes = simultaneous_conjugacy_classes()
        class_by_id = {row["kernel_id"]: row for row in classes}
        member_to_id = {
            member: row["kernel_id"] for row in classes for member in row["members"]
        }
        class_rows = []
        for row in classes:
            representative = row["representative"]
            theta_id = member_to_id[transformed_theta(representative)]
            tau_id = member_to_id[transformed_tau(representative)]
            class_rows.append({
                "kernel_id": row["kernel_id"],
                "map_count": len(row["members"]),
                "image_order": row["image_order"],
                "surjective_to_S3": row["image_order"] == 6,
                "theta_target_kernel_id": theta_id,
                "tau_target_kernel_id": tau_id,
                "theta_invariant": theta_id == row["kernel_id"],
                "tau_invariant": tau_id == row["kernel_id"],
                "theta_tau_invariant": theta_id == row["kernel_id"] and tau_id == row["kernel_id"],
            })
        distribution = Counter(
            len(generated(pair)) for pair in product(SMALL_SYMMETRIC, repeat=2)
        )
        surjective_ids = sorted(
            row["kernel_id"] for row in class_rows if row["surjective_to_S3"]
        )
        invariant_surjective_ids = sorted(
            row["kernel_id"] for row in class_rows
            if row["surjective_to_S3"] and row["theta_tau_invariant"]
        )
        update(
            "F2_rescan", assignment_count=sum(distribution.values()),
            kernel_class_count=len(class_rows), invariant_surjective_count=len(invariant_surjective_ids)
        )

        g9x, g9y = marked_dihedral(9)
        g9 = generated((g9x, g9y))
        g9_rows = []
        for pair in product(SMALL_SYMMETRIC, repeat=2):
            well_defined, table = marked_map(len(g9), (g9x, g9y), pair)
            image_order = len(set(table.values())) if well_defined else None
            g9_rows.append({
                "pair": pair,
                "kernel_id": member_to_id[pair],
                "well_defined": well_defined,
                "image_order": image_order,
                "surjective": well_defined and image_order == 6,
                "kernel_order": (
                    sum(value == SMALL_IDENTITY for value in table.values())
                    if well_defined else None
                ),
            })
        g9_epi_rows = [row for row in g9_rows if row["surjective"]]
        g9_epi_ids = sorted({row["kernel_id"] for row in g9_epi_rows})
        update(
            "G9_rescan", G9_order=len(g9), epimorphisms=len(g9_epi_rows),
            kernel_class_count=len(g9_epi_ids)
        )

        representatives = tuple(
            class_by_id[kernel_id]["representative"] for kernel_id in surjective_ids
        )
        orbit_x = block_diagonal(tuple(pair[0] for pair in representatives))
        orbit_y = block_diagonal(tuple(pair[1] for pair in representatives))
        orbit_group = generated((orbit_x, orbit_y))
        orbit_derived = commutator_group(orbit_group, (orbit_x, orbit_y))
        g3x, g3y = marked_dihedral(3)
        g3 = generated((g3x, g3y))
        iso_ok, iso_table = marked_map(len(g3), (g3x, g3y), (orbit_x, orbit_y))
        orbit_is_g3 = (
            iso_ok and len(g3) == len(orbit_group) == 108
            and len(set(iso_table.values())) == 108
        )

        source_class_projection = [
            {
                key: row[key] for key in (
                    "kernel_id", "map_count", "image_order", "surjective_to_S3",
                    "theta_target_kernel_id", "tau_target_kernel_id",
                    "theta_invariant", "tau_invariant", "theta_tau_invariant",
                )
            }
            for row in source["F2_to_S3"]["kernel_classes"]
        ]
        input_hashes = all(
            file_digest((ROOT / path_text) if not Path(path_text).is_absolute() else Path(path_text)) == expected
            for path_text, expected in source["input_sha256"].items()
        )
        g9_source_rows = {
            (tuple(row["x_image"]), tuple(row["y_image"])): row
            for row in source["G9_to_S3"]["map_records"]
        }
        g9_row_match = all(
            g9_source_rows[row["pair"]]["kernel_id_in_F2"] == row["kernel_id"]
            and g9_source_rows[row["pair"]]["well_defined_on_G9"] == row["well_defined"]
            and g9_source_rows[row["pair"]]["image_order"] == row["image_order"]
            and g9_source_rows[row["pair"]]["surjective_to_S3"] == row["surjective"]
            and g9_source_rows[row["pair"]]["kernel_order_in_G9"] == row["kernel_order"]
            for row in g9_rows
        )
        checks = {
            "schema": source.get("schema") == "d972_entangled_hand2/v1",
            "bound_input_hashes": input_hashes,
            "F2_assignment_count": sum(distribution.values()) == 36 == source["F2_to_S3"]["assignment_count"],
            "image_distribution": {
                str(key): value for key, value in sorted(distribution.items())
            } == source["F2_to_S3"]["image_order_distribution"] == {"1": 1, "2": 9, "3": 8, "6": 18},
            "kernel_class_count": len(class_rows) == 11 == source["F2_to_S3"]["kernel_class_count"],
            "kernel_class_action_table": class_rows == source_class_projection,
            "invariant_kernel_ids": sorted(
                row["kernel_id"] for row in class_rows if row["theta_tau_invariant"]
            ) == source["F2_to_S3"]["theta_tau_invariant_kernel_ids"] == ["q1_o111", "q3_o333"],
            "no_invariant_surjective_kernel": invariant_surjective_ids == [] == source["F2_to_S3"]["theta_tau_invariant_surjective_kernel_ids"],
            "G9_order": len(g9) == 2916 == source["G9_to_S3"]["G9_order"],
            "G9_map_records": g9_row_match,
            "G9_well_defined_count": sum(row["well_defined"] for row in g9_rows) == 28 == source["G9_to_S3"]["well_defined_map_count"],
            "G9_epimorphism_count": len(g9_epi_rows) == 18 == source["G9_to_S3"]["epimorphism_count"],
            "G9_epimorphism_kernel_classes": g9_epi_ids == surjective_ids == source["G9_to_S3"]["epimorphism_kernel_class_ids_in_F2"],
            "unrestricted_match_three": source["kernel_match"]["unrestricted_common_kernel_ids"] == surjective_ids and len(surjective_ids) == 3,
            "eligible_match_empty": source["kernel_match"]["eligible_common_kernel_ids"] == [] and source["kernel_match"]["antecedent_iii_raw_boolean"] is False,
            "surjective_orbit_actions": (
                source["surjective_kernel_orbit"]["theta_action"]
                == {row["kernel_id"]: row["theta_target_kernel_id"] for row in class_rows if row["surjective_to_S3"]}
                and source["surjective_kernel_orbit"]["tau_action"]
                == {row["kernel_id"]: row["tau_target_kernel_id"] for row in class_rows if row["surjective_to_S3"]}
            ),
            "orbit_intersection_is_G3": (
                len(orbit_group) == 108
                and len(orbit_derived) == 27
                and len(orbit_group) // len(orbit_derived) == 4
                and orbit_is_g3
                and source["surjective_kernel_orbit"]["marked_isomorphic_to_G3"] is True
            ),
            "SPLIT_TWIN_outer_pure_type": (
                source["SPLIT_TWIN_type_audit"]["pure_subgroup_image_order_formula"] == "(18*p)/6 = 3*p"
                and source["SPLIT_TWIN_type_audit"]["pure_subgroup_image_order_is_odd_for_odd_p"] is True
                and source["SPLIT_TWIN_type_audit"]["pure_subgroup_image_can_surject_to_S3"] is False
                and source["SPLIT_TWIN_type_audit"]["imports_pure_S3_antecedent_i"] is False
            ),
            "logical_scope_not_overread": (
                source["logical_scope"]["specified_invariant_kernel_gate_raw_boolean"] is False
                and source["logical_scope"]["direct_stable_S3_factor_candidate_closed"] is True
                and source["logical_scope"]["global_absence_of_entangled_roofs_claimed"] is False
                and source["logical_scope"]["axis_1_global_death_authorized_by_this_gate"] is False
                and len(g9_epi_ids) == 3
            ),
            "stage1_false_boundary": (
                source["stage_boundary"]["stage_reached"] == 1
                and source["stage_boundary"]["hand2_same_invariant_PB3_S3_quotient_raw_boolean"] is False
                and source["stage_boundary"]["stopped_after_hand2"] is True
            ),
            "later_stages_not_run": (
                source["stage_boundary"]["stage2_entangled_roof_constructed"] is False
                and source["stage_boundary"]["stage3_gating_run"] is False
                and source["stage_boundary"]["preregistration_created"] is False
            ),
            "no_measurement": (
                source["stage_boundary"]["measurement_authorized"] is False
                and source["stage_boundary"]["measurement_performed"] is False
                and source["stage_boundary"]["reduction_image_set_formed"] is False
                and source["stage_boundary"]["raw_image_size"] is None
                and source["stage_boundary"]["status"] == "UNKNOWN"
            ),
            "noncontact": all(
                source["scope"][key] is False
                for key in (
                    "u_touched", "c_touched", "sealed_k5_touched",
                    "preregistered_quantities_changed", "finite_depth_B_type_recognition",
                )
            ),
        }
        result = {
            "schema": "d972_entangled_hand2_check/v1",
            "checker": "search/check_d972_entangled_hand2_v1.py",
            "helper_disjointness": (
                "standard-library tuple permutations; S3 simultaneous-conjugacy orbits; "
                "direct 27-point G9 reconstruction; no SymPy and no producer import"
            ),
            "source_run_id": source["run_id"],
            "source_sha256": file_digest(source_path),
            "producer_sha256": file_digest(ROOT / "search/d972_entangled_hand2_v1.py"),
            "checks": checks,
            "all_checks_true": all(checks.values()),
            "recomputed": {
                "hom_F2_S3": sum(distribution.values()),
                "image_distribution": {
                    str(key): value for key, value in sorted(distribution.items())
                },
                "kernel_classes": len(class_rows),
                "surjective_kernel_classes": len(surjective_ids),
                "theta_tau_invariant_surjective_kernel_classes": len(invariant_surjective_ids),
                "G9_order": len(g9),
                "G9_well_defined_maps": sum(row["well_defined"] for row in g9_rows),
                "G9_epimorphisms": len(g9_epi_rows),
                "G9_epimorphism_kernel_classes": len(g9_epi_ids),
                "unrestricted_common_kernel_classes": len(set(g9_epi_ids) & set(surjective_ids)),
                "eligible_common_kernel_classes": len(set(g9_epi_ids) & set(invariant_surjective_ids)),
                "surjective_kernel_intersection_quotient_order": len(orbit_group),
                "surjective_kernel_intersection_marked_G3": orbit_is_g3,
                "hand2_raw_boolean": False,
                "stage_reached": 1,
                "raw_image_size": None,
                "status": "UNKNOWN",
            },
            "elapsed_ms": int(1000 * (time.monotonic() - started)),
            "u_touched": False,
            "c_touched": False,
            "sealed_k5_touched": False,
        }
        write_receipt(output_path, result)
        update(
            "complete", complete=True, output=args.output,
            all_checks_true=result["all_checks_true"], hand2_raw_boolean=False,
            raw_image_size=None, status="UNKNOWN"
        )
        timer.cancel()
        print(json.dumps({
            "all_checks_true": result["all_checks_true"],
            **result["recomputed"],
        }, sort_keys=True))
        return 0 if result["all_checks_true"] else 1
    except Exception as exc:
        timer.cancel()
        update("error", error=repr(exc))
        raise


if __name__ == "__main__":
    raise SystemExit(main())
