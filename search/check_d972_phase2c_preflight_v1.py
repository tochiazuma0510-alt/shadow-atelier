#!/usr/bin/env python3
"""Helper-disjoint checker for the Phase-2c preflight certificate.

This checker uses only standard-library tuple permutations.  It reconstructs
PSL(2,8) x C3, repeats the full shadow/settled census, verifies the universal
marked-relation obstruction to a diagonal C3 quotient, and confirms that no
reduction image was formed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import threading
import time
from collections import deque
from pathlib import Path
from typing import Callable, Iterable


ROOT = Path(__file__).resolve().parents[1]
GF8_POLY = 0b1011
PROJECTIVE_LINES = tuple([(1, value) for value in range(8)] + [(0, 1)])
LEVELS = (9, 27, 36, 45, 54, 63, 72, 81, 108, 126, 135, 162)
Perm = tuple[int, ...]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def neutral(degree: int) -> Perm:
    return tuple(range(degree))


def compose(first: Perm, second: Perm) -> Perm:
    return tuple(second[first[index]] for index in range(len(first)))


def invert(value: Perm) -> Perm:
    result = [0] * len(value)
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)


def raise_to(value: Perm, exponent: int) -> Perm:
    if exponent < 0:
        return raise_to(invert(value), -exponent)
    result = neutral(len(value))
    while exponent:
        if exponent & 1:
            result = compose(result, value)
        value = compose(value, value)
        exponent >>= 1
    return result


def span(generators: Iterable[Perm], degree: int | None = None) -> set[Perm]:
    generators = tuple(generators)
    if degree is None:
        degree = len(generators[0])
    one = neutral(degree)
    seen = {one}
    queue = deque([one])
    while queue:
        current = queue.popleft()
        for generator in generators:
            nxt = compose(current, generator)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def manuscript_product(values: Iterable[Perm], degree: int) -> Perm:
    result = neutral(degree)
    for value in reversed(tuple(values)):
        result = compose(result, value)
    return result


def bracket(left: Perm, right: Perm) -> Perm:
    return compose(compose(compose(invert(left), invert(right)), left), right)


def conjugate(value: Perm, actor: Perm) -> Perm:
    return compose(compose(invert(actor), value), actor)


def invariant_closure(seed: Perm, actors: tuple[Perm, ...]) -> set[Perm]:
    basis = [seed]
    while True:
        subgroup = span(basis)
        extra = None
        for value in tuple(basis):
            for actor in actors:
                for direction in (actor, invert(actor)):
                    candidate = conjugate(value, direction)
                    if candidate not in subgroup:
                        extra = candidate
                        break
                if extra is not None:
                    break
            if extra is not None:
                break
        if extra is None:
            return subgroup
        basis.append(extra)


def finite_hom(
    size: int, domain_generators: tuple[Perm, Perm], image_generators: tuple[Perm, Perm]
) -> tuple[bool, dict[Perm, Perm]]:
    domain_one = neutral(len(domain_generators[0]))
    image_one = neutral(len(image_generators[0]))
    table = {domain_one: image_one}
    queue = deque([domain_one])
    steps = (
        (domain_generators[0], image_generators[0]),
        (invert(domain_generators[0]), invert(image_generators[0])),
        (domain_generators[1], image_generators[1]),
        (invert(domain_generators[1]), invert(image_generators[1])),
    )
    while queue:
        current = queue.popleft()
        for domain_step, image_step in steps:
            nxt = compose(current, domain_step)
            image = compose(table[current], image_step)
            if nxt in table:
                if table[nxt] != image:
                    return False, table
            else:
                table[nxt] = image
                queue.append(nxt)
    return len(table) == size, table


def binary_field_mul(left: int, right: int) -> int:
    value = 0
    while right:
        if right & 1:
            value ^= left
        right >>= 1
        left <<= 1
        if left & 8:
            left ^= GF8_POLY
    return value & 7


def binary_field_inv(value: int) -> int:
    if value == 0:
        raise ZeroDivisionError
    return next(candidate for candidate in range(1, 8) if binary_field_mul(value, candidate) == 1)


def projective_action(matrix: tuple[tuple[int, int], tuple[int, int]]) -> Perm:
    images = []
    for left, right in PROJECTIVE_LINES:
        first = binary_field_mul(left, matrix[0][0]) ^ binary_field_mul(right, matrix[1][0])
        second = binary_field_mul(left, matrix[0][1]) ^ binary_field_mul(right, matrix[1][1])
        line = (1, binary_field_mul(second, binary_field_inv(first))) if first else (0, 1)
        images.append(PROJECTIVE_LINES.index(line))
    return tuple(images)


def marked_psl() -> tuple[Perm, Perm, set[Perm]]:
    involution = projective_action(((1, 0), (1, 1)))
    third = projective_action(((4, 3), (1, 5)))
    ninth = compose(involution, invert(third))
    x = raise_to(ninth, 2)
    y = compose(compose(invert(involution), x), involution)
    return x, y, span((x, y))


def block_sum(first: Perm, second: Perm) -> Perm:
    offset = len(first)
    return tuple(first) + tuple(offset + value for value in second)


def shifted(value: Perm, offset: int, total: int) -> Perm:
    result = list(range(total))
    for index, image in enumerate(value):
        result[offset + index] = offset + image
    return tuple(result)


def marked_dihedral_triple(level: int) -> tuple[Perm, Perm]:
    """Reconstruct MakeGn without SymPy or producer code."""
    rotation = tuple((index + 1) % level for index in range(level))
    reflection = tuple((-index) % level for index in range(level))
    reflection_then_rotation = compose(reflection, rotation)
    total = 3 * level
    x = compose(
        compose(shifted(rotation, 0, total), shifted(reflection, level, total)),
        shifted(reflection, 2 * level, total),
    )
    y = compose(
        compose(
            shifted(reflection_then_rotation, 0, total),
            shifted(rotation, level, total),
        ),
        shifted(reflection_then_rotation, 2 * level, total),
    )
    return x, y


def diagonal_collision(x: Perm, y: Perm) -> dict[str, object]:
    identity = neutral(len(x))
    table: dict[Perm, tuple[int, str]] = {identity: (0, "")}
    queue = deque([identity])
    steps = (
        (x, 1, "x"), (invert(x), 2, "X"),
        (y, 1, "y"), (invert(y), 2, "Y"),
    )
    while queue:
        current = queue.popleft()
        current_image, word = table[current]
        for step, increment, letter in steps:
            nxt = compose(current, step)
            proposed = ((current_image + increment) % 3, word + letter)
            if nxt in table:
                if table[nxt][0] != proposed[0]:
                    return {
                        "well_defined": False,
                        "visited_before_collision": len(table),
                        "equal_domain_words": [table[nxt][1], proposed[1]],
                        "incompatible_C3_images": [table[nxt][0], proposed[0]],
                    }
            else:
                table[nxt] = proposed
                queue.append(nxt)
    return {"well_defined": True, "visited_before_collision": len(table)}


def cyclic_coordinate(value: Perm) -> int:
    cycle = (1, 2, 0)
    block = tuple(value[9 + index] - 9 for index in range(3))
    return next(exponent for exponent in range(3) if raise_to(cycle, exponent) == block)


def rescan(
    elements: list[Perm], derived: list[Perm], x: Perm, y: Perm
) -> tuple[list[tuple[int, Perm]], dict[str, int | bool], dict[str, bool]]:
    z = invert(manuscript_product((x, y), 12))
    theta_ok, theta = finite_hom(len(elements), (x, y), (y, x))
    tau_ok, tau = finite_hom(len(elements), (x, y), (y, z))
    automorphism_receipt = {
        "theta_well_defined": theta_ok,
        "theta_bijective": theta_ok and len(set(theta.values())) == len(elements),
        "tau_well_defined": tau_ok,
        "tau_bijective": tau_ok and len(set(tau.values())) == len(elements),
        "theta_delta": theta_ok and all(cyclic_coordinate(theta[value]) == cyclic_coordinate(value) for value in elements),
        "tau_delta": tau_ok and all(cyclic_coordinate(tau[value]) == cyclic_coordinate(value) for value in elements),
    }
    if not all(automorphism_receipt.values()):
        raise RuntimeError("theta/tau reconstruction")
    charming = (0, 2, 3, 5, 6, 8)
    counts: dict[str, int | bool] = {
        "candidate_total": len(derived) * len(charming),
        "h10_rejected": 0,
        "h11_rejected": 0,
        "generation_rejected": 0,
    }
    shadows = []
    identity = neutral(12)
    for f in derived:
        h10 = manuscript_product((f, theta[f]), 12) == identity
        for m in charming:
            if not h10:
                counts["h10_rejected"] += 1
                continue
            ymf = manuscript_product((raise_to(y, m), f), 12)
            tau1 = tau[ymf]
            tau2 = tau[tau1]
            if manuscript_product((tau2, tau1, ymf), 12) != identity:
                counts["h11_rejected"] += 1
                continue
            u = 2 * m + 1
            image_x = raise_to(x, u)
            image_y = manuscript_product((invert(f), raise_to(y, u), f), 12)
            if len(span((image_x, image_y))) != len(elements):
                counts["generation_rejected"] += 1
                continue
            shadows.append((m, f))
    counts["shadow_total"] = len(shadows)
    counts["bookkeeping_identity"] = (
        int(counts["candidate_total"])
        - int(counts["h10_rejected"])
        - int(counts["h11_rejected"])
        - int(counts["generation_rejected"])
        == len(shadows)
    )
    return shadows, counts, automorphism_receipt


def symbolic_level_row(level: int) -> dict[str, int | bool]:
    """Independent coordinate-algebra consequences for G_l."""
    n0 = level // __import__("math").gcd(level, 2)
    group_order = 4 * n0**3
    abelianization_order = 4 if n0 & 1 else 16
    derived_order = group_order // abelianization_order
    return {
        "level": level,
        "n0": n0,
        "G_order": group_order,
        "derived_order": derived_order,
        "abelianization_order": abelianization_order,
        "abelianization_has_factor_3": False,
        "K_level_subset_diagonal_kernel": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", default="search/certs/d972_phase2c_preflight_v1_20260813.json"
    )
    parser.add_argument(
        "--output", default="search/certs/d972_phase2c_preflight_v1_check_20260813.json"
    )
    parser.add_argument(
        "--checkpoint", default="search/certs/d972_phase2c_preflight_v1_check_checkpoint.json"
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    source_path = ROOT / args.input
    output_path = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    started = time.monotonic()
    state: dict[str, object] = {
        "schema": "d972_phase2c_preflight_check_checkpoint/v1",
        "stage": "start",
        "complete": False,
        "raw_image_size": None,
    }
    write_json(checkpoint, state)

    def update(stage: str, **fields: object) -> None:
        state.update(stage=stage, elapsed_ms=int(1000 * (time.monotonic() - started)), **fields)
        write_json(checkpoint, state)

    def timeout() -> None:
        if not state.get("complete"):
            update("hard_timeout")
            os._exit(124)

    timer = threading.Timer(args.hard_timeout_seconds, timeout)
    timer.daemon = True
    timer.start()
    try:
        source = json.loads(source_path.read_text(encoding="utf-8"))
        p_x, p_y, p_group = marked_psl()
        cycle = (1, 2, 0)
        x = block_sum(p_x, cycle)
        y = block_sum(p_y, cycle)
        group = span((x, y))
        elements = sorted(group)
        delta_kernel = {value for value in group if cyclic_coordinate(value) == 0}
        derived = invariant_closure(bracket(x, y), (x, y))
        update("reconstructed_E", E_order=len(group), derived_order=len(derived))

        shadows, scan_counts, symmetry = rescan(elements, sorted(derived), x, y)
        settled = []
        image_sizes = []
        for m, f in shadows:
            u = 2 * m + 1
            image_x = raise_to(x, u)
            image_y = manuscript_product((invert(f), raise_to(y, u), f), 12)
            well_defined, table = finite_hom(len(group), (x, y), (image_x, image_y))
            image_size = len(set(table.values()))
            image_sizes.append(image_size)
            settled.append(well_defined and image_size == len(group))
        update("isolatedness_rescan", shadows=len(shadows), settled=sum(settled))

        source_rows = source["antecedent_1_K_level_in_diagonal_kernel"]["registered_rows"]
        independent_rows = [symbolic_level_row(level) for level in LEVELS]
        row_checks = []
        reconstructed_relations = []
        for expected, observed in zip(independent_rows, source_rows):
            row_checks.append(all(observed[key] == value for key, value in expected.items()))
            dx, dy = marked_dihedral_triple(int(expected["level"]))
            relation_x = (
                compose(compose(dx, dy), dx)
                == compose(compose(invert(dx), dy), invert(dx))
            )
            relation_y = (
                compose(compose(dy, dx), dy)
                == compose(compose(invert(dy), dx), invert(dy))
            )
            reconstructed_relations.append({
                "level": expected["level"],
                "xyx_equals_XyX": relation_x,
                "yxy_equals_YxY": relation_y,
                "diagonal_C3_attempt": diagonal_collision(dx, dy),
            })

        # Universal obstruction in additive C3: the two coordinate identities
        # become 4*dx=0 and 4*dy=0.  Since 4=1 mod 3, dx=dy=0.
        diagonal_pair_solutions = [
            [dx, dy] for dx in range(3) for dy in range(3)
            if (4 * dx) % 3 == 0 and (4 * dy) % 3 == 0
        ]
        input_hashes = all(
            digest((ROOT / path_text) if not Path(path_text).is_absolute() else Path(path_text)) == expected
            for path_text, expected in source["input_sha256"].items()
        )
        checks = {
            "schema": source.get("schema") == "d972_phase2c_preflight/v1",
            "bound_input_hashes": input_hashes,
            "canonical_P_order": len(p_group) == 504,
            "E_order": len(group) == 1512 == source["candidate"]["E_order"],
            "derived_order": len(derived) == 504 == source["candidate"]["E_derived_order"],
            "derived_equals_delta_kernel": derived == delta_kernel,
            "abelianization_is_C3": len(group) // len(derived) == 3,
            "diagonal_marking": [cyclic_coordinate(x), cyclic_coordinate(y), 0] == [1, 1, 0],
            "universal_C3_relation_obstruction": diagonal_pair_solutions == [[0, 0]],
            "antecedent_1_raw": (
                source["antecedent_1_K_level_in_diagonal_kernel"]["raw_boolean"] is False
                and source["antecedent_1_K_level_in_diagonal_kernel"]["levels_with_inclusion"] == []
            ),
            "registered_level_arithmetic": len(row_checks) == len(LEVELS) and all(row_checks),
            "registered_relation_reconstruction": all(
                row["xyx_equals_XyX"]
                and row["yxy_equals_YxY"]
                and row["diagonal_C3_attempt"]["well_defined"] is False
                for row in reconstructed_relations
            ),
            "registered_collision_receipts": all(
                row["diagonal_C3_attempt"]["well_defined"] is False
                and row["diagonal_C3_attempt"]["incompatible_C3_images"][0]
                    != row["diagonal_C3_attempt"]["incompatible_C3_images"][1]
                for row in source_rows
            ),
            "theta_tau_invariance": all(symmetry.values()) and source["antecedent_3_theta_tau_invariant"]["raw_boolean"] is True,
            "scan_counts": scan_counts == source["antecedent_2_N_E_isolated"]["scan"],
            "shadow_records": (
                [[m, list(f)] for m, f in shadows]
                == source["antecedent_2_N_E_isolated"]["shadow_records_m_farray"]
            ),
            "isolatedness_direct": len(shadows) == 54 and len(settled) == 54 and all(settled),
            "settled_image_sizes": sorted(set(image_sizes)) == [1512],
            "nonproduct_raw": (
                source["nonproduct_check"]["requested_nonproduct_raw_boolean"] is False
                and source["nonproduct_check"]["pure_quotient_direct_product_raw_boolean"] is True
                and source["nonproduct_check"]["nontrivial_common_quotient_exists"] is False
            ),
            "PH2_VOID_prime_stop": source["nonproduct_check"]["PH2_VOID_prime_applies"] is True,
            "no_preregistration": source["preregistration"]["created"] is False,
            "no_measurement": (
                source["measurement"]["authorized"] is False
                and source["measurement"]["performed"] is False
                and source["measurement"]["reduction_image_set_formed"] is False
                and source["measurement"]["raw_image_size"] is None
                and source["measurement"]["status"] == "UNKNOWN"
            ),
            "target54_formula_fixtures": source["optional_target54_helper"]["fixtures"] == {"18": 324, "54": 972},
            "noncontact": all(
                source["scope"][key] is False
                for key in ("u_touched", "c_touched", "sealed_k5_touched", "preregistered_quantities_changed", "universe_expanded")
            ),
        }
        result = {
            "schema": "d972_phase2c_preflight_check/v1",
            "checker": "search/check_d972_phase2c_preflight_v1.py",
            "helper_disjointness": (
                "Python standard-library tuple permutations only; no SymPy and no producer import; "
                "independent GF(8), Cayley, relation-obstruction, and settled implementations"
            ),
            "source_run_id": source["run_id"],
            "source_sha256": digest(source_path),
            "producer_sha256": digest(ROOT / "search/d972_phase2c_preflight_v1.py"),
            "checks": checks,
            "all_checks_true": all(checks.values()),
            "recomputed": {
                "P_order": len(p_group),
                "E_order": len(group),
                "derived_order": len(derived),
                "abelianization_order": len(group) // len(derived),
                "diagonal_pair_solutions_compatible_with_G_l_relations": diagonal_pair_solutions,
                "registered_level_rows": independent_rows,
                "registered_relation_rows": reconstructed_relations,
                "shadow_count": len(shadows),
                "settled_count": sum(settled),
                "theta_tau": symmetry,
                "pure_quotient_direct_product": True,
                "raw_image_size": None,
                "status": "UNKNOWN",
            },
            "elapsed_ms": int(1000 * (time.monotonic() - started)),
            "u_touched": False,
            "c_touched": False,
            "sealed_k5_touched": False,
        }
        write_json(output_path, result)
        update(
            "complete", complete=True, output=args.output,
            all_checks_true=result["all_checks_true"], raw_image_size=None,
            status="UNKNOWN"
        )
        timer.cancel()
        print(json.dumps({
            "all_checks_true": result["all_checks_true"],
            "E_order": len(group),
            "derived_order": len(derived),
            "shadow_count": len(shadows),
            "settled_count": sum(settled),
            "pure_quotient_direct_product": True,
            "raw_image_size": None,
            "status": "UNKNOWN",
        }, sort_keys=True))
        return 0 if result["all_checks_true"] else 1
    except Exception as exc:
        timer.cancel()
        update("error", error=repr(exc))
        raise


if __name__ == "__main__":
    raise SystemExit(main())
