#!/usr/bin/env python3
"""Producer for task 128, hand 2: the pure S3 bridge gate.

Inputs and scope:
  * public definitions of theta and tau on F2;
  * the marked quotient G_9 = PB3/K^(9);
  * all 36 assignments (x,y) in S3^2.
No u/c payload, sealed K5 quantity, preregistered measurement, or reduction
image is read.  If no surjective S3 kernel is theta- and tau-invariant, the
conditional pipeline stops before constructing an entangled roof.

Output schema: d972_entangled_hand2/v1.
Invariants checked: kernel classes, theta/tau action, G9 factorization, marked
intersection quotient, SPLIT-TWIN pure/outer quotient type, stop boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import threading
import time
from collections import Counter, deque
from datetime import datetime, timezone
from itertools import permutations, product
from pathlib import Path
from typing import Iterable

from sympy.combinatorics import Permutation, PermutationGroup


ROOT = Path(__file__).resolve().parents[1]
Perm = tuple[int, ...]
S3 = tuple(tuple(value) for value in permutations(range(3)))
ID3: Perm = (0, 1, 2)


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def identity(degree: int) -> Perm:
    return tuple(range(degree))


def mul(left: Perm, right: Perm) -> Perm:
    """Right action: apply left, then right."""
    return tuple(right[left[index]] for index in range(len(left)))


def inverse(value: Perm) -> Perm:
    result = [0] * len(value)
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)


def power(value: Perm, exponent: int) -> Perm:
    if exponent < 0:
        return power(inverse(value), -exponent)
    result = identity(len(value))
    while exponent:
        if exponent & 1:
            result = mul(result, value)
        value = mul(value, value)
        exponent >>= 1
    return result


def element_order(value: Perm) -> int:
    current = identity(len(value))
    for exponent in range(1, 1000):
        current = mul(current, value)
        if current == identity(len(value)):
            return exponent
    raise RuntimeError("element order bound")


def closure(generators: Iterable[Perm], degree: int | None = None) -> set[Perm]:
    generators = tuple(generators)
    if degree is None:
        degree = len(generators[0])
    one = identity(degree)
    seen = {one}
    queue = deque([one])
    steps = generators + tuple(inverse(value) for value in generators)
    while queue:
        current = queue.popleft()
        for step in steps:
            nxt = mul(current, step)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def paper_product(values: Iterable[Perm], degree: int) -> Perm:
    result = identity(degree)
    for value in reversed(tuple(values)):
        result = mul(result, value)
    return result


def marked_hom(
    domain_size: int,
    domain_pair: tuple[Perm, Perm],
    image_pair: tuple[Perm, Perm],
) -> tuple[bool, dict[Perm, Perm], dict[str, object] | None]:
    domain_one = identity(len(domain_pair[0]))
    image_one = identity(len(image_pair[0]))
    table = {domain_one: image_one}
    words = {domain_one: ""}
    queue = deque([domain_one])
    steps = (
        (domain_pair[0], image_pair[0], "x"),
        (inverse(domain_pair[0]), inverse(image_pair[0]), "X"),
        (domain_pair[1], image_pair[1], "y"),
        (inverse(domain_pair[1]), inverse(image_pair[1]), "Y"),
    )
    while queue:
        current = queue.popleft()
        for domain_step, image_step, letter in steps:
            nxt = mul(current, domain_step)
            proposed = mul(table[current], image_step)
            proposed_word = words[current] + letter
            if nxt in table:
                if table[nxt] != proposed:
                    return False, table, {
                        "equal_domain_words": [words[nxt], proposed_word],
                        "incompatible_images": [list(table[nxt]), list(proposed)],
                        "visited_before_collision": len(table),
                    }
            else:
                table[nxt] = proposed
                words[nxt] = proposed_word
                queue.append(nxt)
    return len(table) == domain_size, table, None


def same_free_kernel(first: tuple[Perm, Perm], second: tuple[Perm, Perm]) -> bool:
    first_group = closure(first)
    second_group = closure(second)
    if len(first_group) != len(second_group):
        return False
    ok, table, _ = marked_hom(len(first_group), first, second)
    return ok and len(table) == len(first_group) and len(set(table.values())) == len(first_group)


def class_signature(pair: tuple[Perm, Perm]) -> str:
    left, right = pair
    image_order = len(closure(pair))
    xy = paper_product((left, right), 3)
    return (
        f"q{image_order}_o{element_order(left)}"
        f"{element_order(right)}{element_order(xy)}"
    )


def classify_pairs(pairs: list[tuple[Perm, Perm]]) -> list[list[tuple[Perm, Perm]]]:
    classes: list[list[tuple[Perm, Perm]]] = []
    for pair in pairs:
        for current in classes:
            if same_free_kernel(pair, current[0]):
                current.append(pair)
                break
        else:
            classes.append([pair])
    classes.sort(key=lambda current: class_signature(current[0]))
    return classes


def class_id(pair: tuple[Perm, Perm], classes: list[list[tuple[Perm, Perm]]]) -> str:
    for current in classes:
        if same_free_kernel(pair, current[0]):
            return class_signature(current[0])
    raise RuntimeError("unclassified pair")


def theta_pair(pair: tuple[Perm, Perm]) -> tuple[Perm, Perm]:
    return pair[1], pair[0]


def tau_pair(pair: tuple[Perm, Perm]) -> tuple[Perm, Perm]:
    z = inverse(paper_product(pair, 3))
    return pair[1], z


def shift(value: Permutation, offset: int, total: int) -> Permutation:
    array = list(range(total))
    for index in range(value.size):
        array[offset + index] = offset + int(value(index))
    return Permutation(array, size=total)


def make_gn(level: int) -> tuple[Permutation, Permutation]:
    rotation = Permutation(list(range(1, level)) + [0])
    reflection = Permutation([(-index) % level for index in range(level)])
    total = 3 * level

    def block(value: Permutation, coordinate: int) -> Permutation:
        return shift(value, coordinate * level, total)

    x = block(rotation, 0) * block(reflection, 1) * block(reflection, 2)
    y = (
        block(reflection * rotation, 0)
        * block(rotation, 1)
        * block(reflection * rotation, 2)
    )
    return x, y


def as_tuple(value: Permutation, degree: int) -> Perm:
    return tuple(int(value(index)) for index in range(degree))


def direct_blocks(values: tuple[Perm, ...]) -> Perm:
    result = []
    offset = 0
    for value in values:
        result.extend(offset + image for image in value)
        offset += len(value)
    return tuple(result)


def commutator(left: Perm, right: Perm) -> Perm:
    return mul(mul(mul(inverse(left), inverse(right)), left), right)


def derived_subgroup(group: set[Perm], generators: tuple[Perm, Perm]) -> set[Perm]:
    seeds = [commutator(value, generator) for value in group for generator in generators]
    return closure(seeds, len(generators[0]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", default="search/certs/d972_entangled_hand2_v1_20260813.json"
    )
    parser.add_argument(
        "--checkpoint", default="search/certs/d972_entangled_hand2_v1_checkpoint.json"
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    started = time.monotonic()
    state: dict[str, object] = {
        "schema": "d972_entangled_hand2_checkpoint/v1",
        "stage": "start",
        "complete": False,
        "raw_image_size": None,
    }
    atomic_json(checkpoint, state)

    def update(stage: str, **fields: object) -> None:
        state.update(stage=stage, elapsed_ms=int(1000 * (time.monotonic() - started)), **fields)
        atomic_json(checkpoint, state)

    def timeout() -> None:
        if not state.get("complete"):
            update("hard_timeout")
            os._exit(124)

    timer = threading.Timer(args.hard_timeout_seconds, timeout)
    timer.daemon = True
    timer.start()
    try:
        all_pairs = list(product(S3, repeat=2))
        classes = classify_pairs(all_pairs)
        pair_records = []
        class_records = []
        for current in classes:
            representative = current[0]
            signature = class_signature(representative)
            theta_target = class_id(theta_pair(representative), classes)
            tau_target = class_id(tau_pair(representative), classes)
            image_order = len(closure(representative))
            class_records.append({
                "kernel_id": signature,
                "map_count": len(current),
                "image_order": image_order,
                "surjective_to_S3": image_order == 6,
                "representative_pair": [list(representative[0]), list(representative[1])],
                "theta_target_kernel_id": theta_target,
                "tau_target_kernel_id": tau_target,
                "theta_invariant": theta_target == signature,
                "tau_invariant": tau_target == signature,
                "theta_tau_invariant": theta_target == signature and tau_target == signature,
            })
            for pair in current:
                pair_records.append({
                    "x_image": list(pair[0]),
                    "y_image": list(pair[1]),
                    "kernel_id": signature,
                    "image_order": image_order,
                })
        pair_records.sort(key=lambda row: (row["x_image"], row["y_image"]))
        image_distribution = Counter(row["image_order"] for row in pair_records)
        invariant_classes = [row for row in class_records if row["theta_tau_invariant"]]
        invariant_surjective = [row for row in invariant_classes if row["surjective_to_S3"]]
        update(
            "hom_F2_S3",
            assignment_count=len(all_pairs), kernel_class_count=len(classes),
            invariant_surjective_kernel_count=len(invariant_surjective)
        )

        gx_sympy, gy_sympy = make_gn(9)
        g9_sympy = PermutationGroup([gx_sympy, gy_sympy])
        g9_order = int(g9_sympy.order())
        gx = as_tuple(gx_sympy, 27)
        gy = as_tuple(gy_sympy, 27)
        g9_records = []
        for pair in all_pairs:
            well_defined, table, collision = marked_hom(g9_order, (gx, gy), pair)
            image_size = len(set(table.values())) if well_defined else None
            kernel_size = (
                sum(value == ID3 for value in table.values()) if well_defined else None
            )
            g9_records.append({
                "x_image": list(pair[0]),
                "y_image": list(pair[1]),
                "kernel_id_in_F2": class_id(pair, classes),
                "well_defined_on_G9": well_defined,
                "image_order": image_size,
                "surjective_to_S3": well_defined and image_size == 6,
                "kernel_order_in_G9": kernel_size,
                "collision": collision,
            })
        g9_records.sort(key=lambda row: (row["x_image"], row["y_image"]))
        g9_epi = [row for row in g9_records if row["surjective_to_S3"]]
        g9_epi_ids = sorted({row["kernel_id_in_F2"] for row in g9_epi})
        free_epi_ids = sorted(
            row["kernel_id"] for row in class_records if row["surjective_to_S3"]
        )
        eligible_ids = sorted(
            row["kernel_id"] for row in class_records
            if row["surjective_to_S3"] and row["theta_tau_invariant"]
        )
        unrestricted_common_ids = sorted(set(g9_epi_ids) & set(free_epi_ids))
        eligible_common_ids = sorted(set(g9_epi_ids) & set(eligible_ids))
        update(
            "G9_S3",
            G9_order=g9_order, epimorphism_count=len(g9_epi),
            epimorphism_kernel_class_count=len(g9_epi_ids)
        )

        epi_representatives = tuple(
            tuple(tuple(value) for value in row["representative_pair"])
            for row in class_records if row["surjective_to_S3"]
        )
        orbit_x = direct_blocks(tuple(pair[0] for pair in epi_representatives))
        orbit_y = direct_blocks(tuple(pair[1] for pair in epi_representatives))
        orbit_quotient = closure((orbit_x, orbit_y))
        orbit_derived = derived_subgroup(orbit_quotient, (orbit_x, orbit_y))
        g3x_sympy, g3y_sympy = make_gn(3)
        g3_order = int(PermutationGroup([g3x_sympy, g3y_sympy]).order())
        g3x = as_tuple(g3x_sympy, 9)
        g3y = as_tuple(g3y_sympy, 9)
        marked_iso_g3, marked_iso_table, _ = marked_hom(
            g3_order, (g3x, g3y), (orbit_x, orbit_y)
        )
        orbit_receipt = {
            "surjective_kernel_ids": free_epi_ids,
            "theta_action": {
                row["kernel_id"]: row["theta_target_kernel_id"]
                for row in class_records if row["surjective_to_S3"]
            },
            "tau_action": {
                row["kernel_id"]: row["tau_target_kernel_id"]
                for row in class_records if row["surjective_to_S3"]
            },
            "orbit_size": len(free_epi_ids),
            "intersection_quotient_order": len(orbit_quotient),
            "intersection_quotient_derived_order": len(orbit_derived),
            "intersection_quotient_abelianization_order": len(orbit_quotient) // len(orbit_derived),
            "marked_isomorphic_to_G3": (
                marked_iso_g3
                and len(marked_iso_table) == g3_order
                and len(set(marked_iso_table.values())) == len(orbit_quotient)
                and len(orbit_quotient) == g3_order == 108
            ),
            "interpretation": (
                "the three S3 kernels form one theta/tau orbit; their invariant "
                "intersection has marked quotient G3, not S3"
            ),
        }

        hand2_raw = len(eligible_common_ids) > 0
        split_twin_audit = {
            "source_statement": "E_p = C_p semidirect (C3 x S3), order 18p, is a B3 quotient",
            "B3_quotient_order_formula": "18*p",
            "outer_quotient": "B3/PB3 = S3",
            "pure_subgroup_image_order_formula": "(18*p)/6 = 3*p",
            "pure_subgroup_image_order_is_odd_for_odd_p": True,
            "pure_subgroup_image_can_surject_to_S3": False,
            "type_distinction": (
                "the displayed E_p -> S3 is the outer B3/PB3 quotient; it does not "
                "supply PB3/N -> S3"
            ),
            "imports_pure_S3_antecedent_i": False,
        }
        stage_boundary = {
            "stage_reached": 1,
            "hand2_same_invariant_PB3_S3_quotient_raw_boolean": hand2_raw,
            "unrestricted_same_S3_kernel_class_count": len(unrestricted_common_ids),
            "eligible_invariant_same_S3_kernel_class_count": len(eligible_common_ids),
            "stopped_after_hand2": not hand2_raw,
            "stage2_entangled_roof_constructed": False,
            "stage3_gating_run": False,
            "preregistration_created": False,
            "measurement_authorized": False,
            "measurement_performed": False,
            "reduction_image_set_formed": False,
            "raw_image_size": None,
            "status": "UNKNOWN",
            "finite_depth_B_type_recognition": False,
        }
        logical_scope = {
            "specified_invariant_kernel_gate_raw_boolean": hand2_raw,
            "direct_stable_S3_factor_candidate_closed": not hand2_raw,
            "global_absence_of_entangled_roofs_claimed": False,
            "reason": (
                "G9 itself is theta/tau-stable while its three S3 quotient kernels "
                "are permuted; therefore absence of an individually invariant S3 "
                "kernel does not exclude S3 quotients permuted inside a larger stable E"
            ),
            "permuted_quotient_witness": "G9 with three S3 kernel classes",
            "axis_1_global_death_authorized_by_this_gate": False,
        }
        if hand2_raw:
            raise RuntimeError("hand 2 unexpectedly opened later stages; producer is fail-closed")
        update(
            "hand2_false_stop", hand2_raw_boolean=False,
            eligible_common_kernel_class_count=0, raw_image_size=None
        )

        inputs = (
            ROOT / "ops/inbox_codex/sol_task_128_entangled.txt",
            ROOT / "docs/notes/ab_instrument_redesign_v1.md",
            ROOT / "docs/notes/ribet_dig_campaign_v1_addendum_a.md",
            ROOT / "docs/week1-定義ノート.md",
        )
        now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        cert = {
            "schema": "d972_entangled_hand2/v1",
            "run_id": f"d972-entangled-hand2-{now}",
            "generated_by": {
                "script": "search/d972_entangled_hand2_v1.py",
                "tool": "Python 3.13 + SymPy 1.14",
            },
            "universe": {
                "all_Hom_F2_S3_assignments": 36,
                "level_set": [9],
                "expanded_after_false": False,
            },
            "F2_to_S3": {
                "assignment_count": len(pair_records),
                "image_order_distribution": {
                    str(key): value for key, value in sorted(image_distribution.items())
                },
                "kernel_class_count": len(class_records),
                "kernel_classes": class_records,
                "map_records": pair_records,
                "theta_tau_invariant_kernel_ids": sorted(
                    row["kernel_id"] for row in invariant_classes
                ),
                "theta_tau_invariant_surjective_kernel_ids": eligible_ids,
            },
            "G9_to_S3": {
                "G9_order": g9_order,
                "assignment_count_checked": len(g9_records),
                "well_defined_map_count": sum(row["well_defined_on_G9"] for row in g9_records),
                "epimorphism_count": len(g9_epi),
                "epimorphism_kernel_class_ids_in_F2": g9_epi_ids,
                "map_records": g9_records,
            },
            "kernel_match": {
                "unrestricted_F2_epi_kernel_ids": free_epi_ids,
                "G9_epi_kernel_ids": g9_epi_ids,
                "unrestricted_common_kernel_ids": unrestricted_common_ids,
                "eligible_theta_tau_invariant_F2_epi_kernel_ids": eligible_ids,
                "eligible_common_kernel_ids": eligible_common_ids,
                "antecedent_iii_raw_boolean": hand2_raw,
            },
            "surjective_kernel_orbit": orbit_receipt,
            "SPLIT_TWIN_type_audit": split_twin_audit,
            "logical_scope": logical_scope,
            "stage_boundary": stage_boundary,
            "input_sha256": {
                str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
                for path in inputs
            },
            "scope": {
                "u_touched": False,
                "c_touched": False,
                "sealed_k5_touched": False,
                "preregistered_quantities_changed": False,
                "finite_depth_B_type_recognition": False,
            },
            "elapsed_ms": int(1000 * (time.monotonic() - started)),
        }
        atomic_json(output, cert)
        update(
            "complete", complete=True, output=args.output, run_id=cert["run_id"],
            hand2_raw_boolean=False, raw_image_size=None, status="UNKNOWN"
        )
        timer.cancel()
        print(json.dumps({
            "run_id": cert["run_id"],
            "hom_F2_S3": len(pair_records),
            "image_distribution": cert["F2_to_S3"]["image_order_distribution"],
            "surjective_kernel_classes": len(free_epi_ids),
            "theta_tau_invariant_surjective_kernel_classes": len(eligible_ids),
            "G9_epimorphisms": len(g9_epi),
            "G9_epimorphism_kernel_classes": len(g9_epi_ids),
            "unrestricted_common_kernel_classes": len(unrestricted_common_ids),
            "eligible_common_kernel_classes": len(eligible_common_ids),
            "hand2_raw_boolean": hand2_raw,
            "stage_reached": 1,
            "raw_image_size": None,
            "status": "UNKNOWN",
        }, sort_keys=True))
        return 0
    except Exception as exc:
        timer.cancel()
        update("error", error=repr(exc))
        raise


if __name__ == "__main__":
    raise SystemExit(main())
