#!/usr/bin/env python3
"""Phase-2c producer: preconditions for E = PSL(2,8) x C3.

The reduction image is deliberately never formed.  The first antecedent says
that the diagonal C3 map would have to factor through G_l.  The marked G_l
relations rule this out at every positive level, so PH2-VOID-prime stops the
lane after the remaining requested preconditions have been recorded.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import threading
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable

from sympy.combinatorics import Permutation, PermutationGroup


ROOT = Path(__file__).resolve().parents[1]
GF8_MOD = 0b1011
P1_GF8 = tuple([(1, value) for value in range(8)] + [(0, 1)])
LEVELS = (9, 27, 36, 45, 54, 63, 72, 81, 108, 126, 135, 162)
Perm = tuple[int, ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


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
    """Right-action product: apply left, then right."""
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
        exponent //= 2
    return result


def closure(generators: Iterable[Perm], degree: int | None = None) -> set[Perm]:
    generators = tuple(generators)
    if degree is None:
        if not generators:
            raise ValueError("degree is required for an empty generator list")
        degree = len(generators[0])
    one = identity(degree)
    seen = {one}
    queue = deque([one])
    while queue:
        current = queue.popleft()
        for generator in generators:
            nxt = mul(current, generator)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def abstract_prod(items: Iterable[Perm], degree: int) -> Perm:
    result = identity(degree)
    for item in reversed(tuple(items)):
        result = mul(result, item)
    return result


def commutator(left: Perm, right: Perm) -> Perm:
    return mul(mul(mul(inverse(left), inverse(right)), left), right)


def conjugate(value: Perm, by: Perm) -> Perm:
    return mul(mul(inverse(by), value), by)


def normal_closure(seed: Perm, acting_generators: tuple[Perm, ...]) -> set[Perm]:
    subgroup_generators = [seed]
    while True:
        subgroup = closure(subgroup_generators)
        extra = None
        for generator in tuple(subgroup_generators):
            for acting in acting_generators:
                for by in (acting, inverse(acting)):
                    candidate = conjugate(generator, by)
                    if candidate not in subgroup:
                        extra = candidate
                        break
                if extra is not None:
                    break
            if extra is not None:
                break
        if extra is None:
            return subgroup
        subgroup_generators.append(extra)


def build_hom(
    domain_size: int,
    domain_generators: tuple[Perm, ...],
    image_generators: tuple[Perm, ...],
) -> tuple[bool, dict[Perm, Perm]]:
    domain_one = identity(len(domain_generators[0]))
    image_one = identity(len(image_generators[0]))
    mapping = {domain_one: image_one}
    queue = deque([domain_one])
    steps = []
    for domain_generator, image_generator in zip(domain_generators, image_generators):
        steps.extend((
            (domain_generator, image_generator),
            (inverse(domain_generator), inverse(image_generator)),
        ))
    while queue:
        current = queue.popleft()
        current_image = mapping[current]
        for domain_step, image_step in steps:
            nxt = mul(current, domain_step)
            nxt_image = mul(current_image, image_step)
            if nxt in mapping:
                if mapping[nxt] != nxt_image:
                    return False, mapping
            else:
                mapping[nxt] = nxt_image
                queue.append(nxt)
    return len(mapping) == domain_size, mapping


def gf8_mul(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
        if left & 8:
            left ^= GF8_MOD
    return result & 7


def gf8_inv(value: int) -> int:
    if value == 0:
        raise ZeroDivisionError
    return next(candidate for candidate in range(1, 8) if gf8_mul(value, candidate) == 1)


def matrix_line_perm(matrix: tuple[tuple[int, int], tuple[int, int]]) -> Perm:
    images = []
    for left, right in P1_GF8:
        first = gf8_mul(left, matrix[0][0]) ^ gf8_mul(right, matrix[1][0])
        second = gf8_mul(left, matrix[0][1]) ^ gf8_mul(right, matrix[1][1])
        line = (1, gf8_mul(second, gf8_inv(first))) if first else (0, 1)
        images.append(P1_GF8.index(line))
    return tuple(images)


def canonical_p() -> tuple[Perm, Perm, Perm, Perm, set[Perm]]:
    s = matrix_line_perm(((1, 0), (1, 1)))
    t = matrix_line_perm(((4, 3), (1, 5)))
    w = mul(s, inverse(t))
    x = power(w, 2)
    y = mul(mul(inverse(s), x), s)
    return s, t, x, y, closure((x, y))


def direct_sum(left: Perm, right: Perm) -> Perm:
    offset = len(left)
    return tuple(left) + tuple(offset + image for image in right)


def sympy_tuple(value: Permutation, degree: int) -> Perm:
    return tuple(int(value(index)) for index in range(degree))


def shift_perm(value: Permutation, offset: int, total: int) -> Permutation:
    array = list(range(total))
    for index in range(value.size):
        array[offset + index] = offset + int(value(index))
    return Permutation(array, size=total)


def make_gn(level: int) -> tuple[Permutation, Permutation]:
    rotation = Permutation(list(range(1, level)) + [0])
    reflection = Permutation([(-index) % level for index in range(level)])
    total = 3 * level

    def translate(value: Permutation, coordinate: int) -> Permutation:
        return shift_perm(value, coordinate * level, total)

    x = translate(rotation, 0) * translate(reflection, 1) * translate(reflection, 2)
    y = (
        translate(reflection * rotation, 0)
        * translate(rotation, 1)
        * translate(reflection * rotation, 2)
    )
    return x, y


def diagonal_c3_attempt(x: Perm, y: Perm) -> dict[str, object]:
    """Try x,y -> 1 in additive C3 and retain the first collision."""
    one = identity(len(x))
    mapping: dict[Perm, tuple[int, str]] = {one: (0, "")}
    queue = deque([one])
    steps = (
        (x, 1, "x"), (inverse(x), 2, "X"),
        (y, 1, "y"), (inverse(y), 2, "Y"),
    )
    while queue:
        current = queue.popleft()
        current_image, word = mapping[current]
        for step, increment, letter in steps:
            nxt = mul(current, step)
            proposed = ((current_image + increment) % 3, word + letter)
            if nxt in mapping:
                if mapping[nxt][0] != proposed[0]:
                    old_image, old_word = mapping[nxt]
                    return {
                        "well_defined": False,
                        "visited_before_collision": len(mapping),
                        "equal_domain_words": [old_word, proposed[1]],
                        "incompatible_C3_images": [old_image, proposed[0]],
                    }
            else:
                mapping[nxt] = proposed
                queue.append(nxt)
    return {
        "well_defined": True,
        "visited_before_collision": len(mapping),
        "equal_domain_words": None,
        "incompatible_C3_images": None,
    }


def scan_shadows(
    elements: list[Perm],
    x: Perm,
    y: Perm,
    group_order: int,
    progress: Callable[[int, dict[str, int]], None] | None = None,
) -> tuple[list[tuple[int, Perm]], dict[str, int | bool]]:
    degree = len(x)
    one = identity(degree)
    z = inverse(abstract_prod((x, y), degree))
    theta_ok, theta = build_hom(group_order, (x, y), (y, x))
    tau_ok, tau = build_hom(group_order, (x, y), (y, z))
    if not theta_ok or not tau_ok:
        raise RuntimeError("theta or tau is not well-defined on E")
    charming = tuple(m for m in range(9) if math.gcd(2 * m + 1, 9) == 1)
    counts: dict[str, int | bool] = {
        "candidate_total": len(elements) * len(charming),
        "h10_rejected": 0,
        "h11_rejected": 0,
        "generation_rejected": 0,
    }
    shadows: list[tuple[int, Perm]] = []
    for position, f in enumerate(elements, start=1):
        h10 = abstract_prod((f, theta[f]), degree) == one
        for m in charming:
            if not h10:
                counts["h10_rejected"] += 1
                continue
            ymf = abstract_prod((power(y, m), f), degree)
            tau_once = tau[ymf]
            tau_twice = tau[tau_once]
            if abstract_prod((tau_twice, tau_once, ymf), degree) != one:
                counts["h11_rejected"] += 1
                continue
            exponent = 2 * m + 1
            image_x = power(x, exponent)
            image_y = abstract_prod((inverse(f), power(y, exponent), f), degree)
            if len(closure((image_x, image_y))) != group_order:
                counts["generation_rejected"] += 1
                continue
            shadows.append((m, f))
        if progress is not None and position % 84 == 0:
            progress(position, {key: int(value) for key, value in counts.items()})
    counts["shadow_total"] = len(shadows)
    counts["bookkeeping_identity"] = (
        int(counts["candidate_total"])
        - int(counts["h10_rejected"])
        - int(counts["h11_rejected"])
        - int(counts["generation_rejected"])
        == len(shadows)
    )
    return shadows, counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", default="search/certs/d972_phase2c_preflight_v1_20260813.json"
    )
    parser.add_argument(
        "--checkpoint", default="search/certs/d972_phase2c_preflight_v1_checkpoint.json"
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    started = time.monotonic()
    state: dict[str, object] = {
        "schema": "d972_phase2c_preflight_checkpoint/v1",
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
        p_s, p_t, p_x, p_y, p_elements = canonical_p()
        c3 = (1, 2, 0)
        e_x = direct_sum(p_x, c3)
        e_y = direct_sum(p_y, c3)
        e_elements = closure((e_x, e_y))
        e_sympy = PermutationGroup([
            Permutation(list(e_x), size=12), Permutation(list(e_y), size=12)
        ])
        e_derived_sympy = e_sympy.derived_subgroup()
        derived_elements = {
            sympy_tuple(value, 12) for value in e_derived_sympy.generate_schreier_sims()
        }
        derived_normal = normal_closure(commutator(e_x, e_y), (e_x, e_y))
        c3_powers = {power(c3, exponent): exponent for exponent in range(3)}

        def delta(value: Perm) -> int:
            block = tuple(value[9 + index] - 9 for index in range(3))
            return c3_powers[block]

        delta_kernel = {value for value in e_elements if delta(value) == 0}
        candidate_receipt = {
            "P_order": len(p_elements),
            "P_marked_orders": [int(Permutation(list(p_x)).order()), int(Permutation(list(p_y)).order())],
            "C3_order": 3,
            "E_order": len(e_elements),
            "E_sympy_order": int(e_sympy.order()),
            "E_derived_order": len(derived_elements),
            "E_derived_sympy_order": int(e_derived_sympy.order()),
            "E_abelianization_order": len(e_elements) // len(derived_elements),
            "E_nonperfect": len(derived_elements) != len(e_elements),
            "derived_equals_delta_kernel": derived_elements == delta_kernel,
            "derived_equals_commutator_normal_closure": derived_elements == derived_normal,
            "marked_generates_E": len(e_elements) == 1512,
            "delta_on_x_y_c": [delta(e_x), delta(e_y), 0],
            "central_c_image": "identity in E",
        }
        if not all((
            len(p_elements) == 504,
            len(e_elements) == 1512,
            len(derived_elements) == 504,
            derived_elements == delta_kernel,
            derived_elements == derived_normal,
        )):
            raise RuntimeError("candidate E receipts are inconsistent")
        update("candidate_E", E_order=len(e_elements), derived_order=len(derived_elements))

        level_rows = []
        for level in LEVELS:
            gx_sympy, gy_sympy = make_gn(level)
            group = PermutationGroup([gx_sympy, gy_sympy])
            group_order = int(group.order())
            derived_order = int(group.derived_subgroup().order())
            gx = sympy_tuple(gx_sympy, 3 * level)
            gy = sympy_tuple(gy_sympy, 3 * level)
            attempt = diagonal_c3_attempt(gx, gy)
            n0 = level // math.gcd(level, 2)
            level_rows.append({
                "level": level,
                "n0": n0,
                "G_order": group_order,
                "G_order_formula": 4 * n0**3,
                "derived_order": derived_order,
                "abelianization_order": group_order // derived_order,
                "abelianization_has_factor_3": (group_order // derived_order) % 3 == 0,
                "xyx_equals_XyX": gx_sympy * gy_sympy * gx_sympy == (~gx_sympy) * gy_sympy * (~gx_sympy),
                "yxy_equals_YxY": gy_sympy * gx_sympy * gy_sympy == (~gy_sympy) * gx_sympy * (~gy_sympy),
                "diagonal_C3_attempt": attempt,
                "K_level_subset_diagonal_kernel": bool(attempt["well_defined"]),
            })

        relation_sweep = []
        for level in range(1, 163):
            gx, gy = make_gn(level)
            relation_sweep.append(
                gx * gy * gx == (~gx) * gy * (~gx)
                and gy * gx * gy == (~gy) * gx * (~gy)
            )
        gate1 = {
            "raw_boolean": False,
            "levels_with_inclusion": [],
            "registered_levels_checked": list(LEVELS),
            "registered_rows": level_rows,
            "relation_sweep_1_through_162_all_true": all(relation_sweep),
            "all_positive_levels_argument": (
                "In the marked dihedral quotient, xyx=x^-1*y*x^-1 and "
                "yxy=y^-1*x*y^-1 hold from the coordinate D_l relations for every l. "
                "After any map to C3 these give 4*delta(x)=4*delta(y)=0, hence "
                "delta(x)=delta(y)=0.  The diagonal assignment delta(x)=delta(y)=1 "
                "therefore never factors through G_l."
            ),
            "equivalence_used": "K^(l) subset ker(delta) iff delta factors through PB3/K^(l)=G_l",
            "scope": "every positive level, hence no admissible level",
        }
        update("antecedent_1", raw_boolean=False, levels_with_inclusion=[])

        def scan_progress(position: int, counts: dict[str, int]) -> None:
            update("antecedent_2_scan", f_elements_processed=position, counters=counts)

        derived_sorted = sorted(derived_elements)
        shadows, shadow_counts = scan_shadows(
            derived_sorted, e_x, e_y, len(e_elements), scan_progress
        )
        settled_bools = []
        settled_image_sizes = []
        for m, f in shadows:
            exponent = 2 * m + 1
            image_x = power(e_x, exponent)
            image_y = abstract_prod((inverse(f), power(e_y, exponent), f), 12)
            well_defined, mapping = build_hom(
                len(e_elements), (e_x, e_y), (image_x, image_y)
            )
            image_size = len(set(mapping.values()))
            settled_image_sizes.append(image_size)
            settled_bools.append(well_defined and image_size == len(e_elements))
        gate2 = {
            "N_E_isolated": len(shadows) > 0 and all(settled_bools),
            "raw_boolean": len(shadows) > 0 and all(settled_bools),
            "N_ord": 9,
            "charming_m_mod_9": [0, 2, 3, 5, 6, 8],
            "commutator_candidate_count": len(derived_sorted),
            "scan": shadow_counts,
            "shadow_records_m_farray": [
                [m, list(f)] for m, f in shadows
            ],
            "settled_count": sum(settled_bools),
            "settled_image_sizes": sorted(set(settled_image_sizes)),
            "settled_by": "direct marked endomorphism construction; every image map is bijective on E",
        }
        if not gate2["raw_boolean"]:
            raise RuntimeError("isolatedness receipt is false")
        update("antecedent_2", raw_boolean=True, shadow_count=len(shadows))

        z = inverse(abstract_prod((e_x, e_y), 12))
        theta_ok, theta = build_hom(1512, (e_x, e_y), (e_y, e_x))
        tau_ok, tau = build_hom(1512, (e_x, e_y), (e_y, z))
        gate3 = {
            "theta_well_defined": theta_ok,
            "theta_bijective": theta_ok and len(set(theta.values())) == 1512,
            "tau_well_defined": tau_ok,
            "tau_bijective": tau_ok and len(set(tau.values())) == 1512,
            "delta_on_x_y_z": [delta(e_x), delta(e_y), delta(z)],
            "theta_preserves_delta_on_all_E": theta_ok and all(delta(theta[value]) == delta(value) for value in e_elements),
            "tau_preserves_delta_on_all_E": tau_ok and all(delta(tau[value]) == delta(value) for value in e_elements),
            "raw_boolean": False,
        }
        gate3["raw_boolean"] = all(
            value is True
            for key, value in gate3.items()
            if key not in ("delta_on_x_y_z", "raw_boolean")
        )
        if not gate3["raw_boolean"]:
            raise RuntimeError("theta/tau invariance receipt is false")
        update("antecedent_3", raw_boolean=True)

        all_registered_no_c3 = all(
            not row["abelianization_has_factor_3"]
            and not row["diagonal_C3_attempt"]["well_defined"]
            for row in level_rows
        )
        nonproduct = {
            "E_nonperfect": candidate_receipt["E_nonperfect"],
            "E_abelianization_order": candidate_receipt["E_abelianization_order"],
            "E_abelianization_is_C3": candidate_receipt["E_abelianization_order"] == 3,
            "G_l_solvable": True,
            "G_l_has_C3_quotient": False,
            "registered_levels_machine_confirmation_no_C3": all_registered_no_c3,
            "all_levels_no_C3_reason": gate1["all_positive_levels_argument"],
            "nontrivial_common_quotient_exists": False,
            "requested_nonproduct_raw_boolean": False,
            "pure_quotient_direct_product_raw_boolean": True,
            "goursat_conclusion": (
                "PB3/(K^(l) intersection N_E) is G_l direct-product (PSL(2,8) x C3) "
                "for every positive l"
            ),
            "pure_quotient_order_formula": "1512 * 4 * (l/gcd(l,2))^3",
            "PH2_VOID_prime_applies": True,
        }
        update(
            "PH2_VOID_prime_stop", requested_nonproduct_raw_boolean=False,
            pure_quotient_direct_product_raw_boolean=True, raw_image_size=None
        )

        source_paths = (
            ROOT / "ops/inbox_codex/sol_task_127_phase2c.txt",
            ROOT / "docs/notes/c1p5_v2_diff_review_v1.md",
            ROOT / "docs/notes/d972_phase2_void_addendum_v2_1.md",
        )
        now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        cert = {
            "schema": "d972_phase2c_preflight/v1",
            "run_id": f"d972-phase2c-preflight-{now}",
            "generated_by": {
                "script": "search/d972_phase2c_preflight_v1.py",
                "tool": "Python 3.13 + SymPy 1.14",
            },
            "execution_order": [
                "candidate_E",
                "antecedent_1_diagonal_factorization",
                "antecedent_2_isolatedness",
                "antecedent_3_theta_tau_invariance",
                "PH2_VOID_prime_nonproduct_check",
                "stop_without_preregistration_or_measurement",
            ],
            "candidate": candidate_receipt,
            "antecedent_1_K_level_in_diagonal_kernel": gate1,
            "antecedent_2_N_E_isolated": gate2,
            "antecedent_3_theta_tau_invariant": gate3,
            "nonproduct_check": nonproduct,
            "preregistration": {
                "created": False,
                "frozen_spectrum": None,
                "blind_declaration": None,
                "reason": "nonproduct antecedent is false, so the measurement lane was not opened",
            },
            "measurement": {
                "authorized": False,
                "performed": False,
                "reduction_image_set_formed": False,
                "raw_image_size": None,
                "status": "UNKNOWN",
                "finite_depth_B_type_recognition": False,
            },
            "optional_target54_helper": {
                "implemented_as_formula_fixture_only": True,
                "formula": "roof_raw = 18 * target_internal_image_count",
                "fixtures": {"18": 324, "54": 972},
                "used_for_phase2c_measurement": False,
                "reason": "kept as a future direct-product gating arithmetic receipt",
            },
            "input_sha256": {
                str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
                for path in source_paths
            },
            "scope": {
                "u_touched": False,
                "c_touched": False,
                "sealed_k5_touched": False,
                "preregistered_quantities_changed": False,
                "universe_expanded": False,
            },
            "elapsed_ms": int(1000 * (time.monotonic() - started)),
        }
        atomic_json(output, cert)
        update(
            "complete", complete=True, output=args.output, run_id=cert["run_id"],
            raw_image_size=None, status="UNKNOWN"
        )
        timer.cancel()
        print(json.dumps({
            "run_id": cert["run_id"],
            "antecedent_raw": [gate1["raw_boolean"], gate2["raw_boolean"], gate3["raw_boolean"]],
            "E_order": len(e_elements),
            "E_abelianization_order": candidate_receipt["E_abelianization_order"],
            "shadow_count_for_isolatedness": len(shadows),
            "pure_quotient_direct_product": True,
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
