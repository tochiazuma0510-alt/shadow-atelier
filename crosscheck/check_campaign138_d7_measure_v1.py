#!/usr/bin/env python3
"""Helper-independent checker for the campaign 138 d=7 measurement."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import threading
import time
from collections import deque
from pathlib import Path

from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.free_groups import free_group


Perm = tuple[int, ...]
GF8_POLY = 0b1011
LINES = tuple([(1, value) for value in range(8)] + [(0, 1)])


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
    temporary.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def identity(degree: int) -> Perm:
    return tuple(range(degree))


def compose(left: Perm, right: Perm) -> Perm:
    return tuple(right[left[index]] for index in range(len(left)))


def invert(value: Perm) -> Perm:
    result = [0] * len(value)
    for source, target in enumerate(value):
        result[target] = source
    return tuple(result)


def power(value: Perm, exponent: int) -> Perm:
    if exponent < 0:
        return power(invert(value), -exponent)
    result = identity(len(value))
    factor = value
    while exponent:
        if exponent & 1:
            result = compose(result, factor)
        factor = compose(factor, factor)
        exponent >>= 1
    return result


def reverse_product(values: tuple[Perm, ...]) -> Perm:
    result = identity(len(values[0]))
    for value in reversed(values):
        result = compose(result, value)
    return result


def generated(generators: tuple[Perm, ...], degree: int | None = None) -> set[Perm]:
    if degree is None:
        degree = len(generators[0])
    one = identity(degree)
    seen = {one}
    queue = deque([one])
    steps = generators + tuple(invert(item) for item in generators)
    while queue:
        current = queue.popleft()
        for step in steps:
            nxt = compose(current, step)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def sympy_elements(generators: tuple[Perm, ...]) -> set[Perm]:
    group = PermutationGroup(*[Permutation(list(value)) for value in generators])
    return {
        tuple(int(element(index)) for index in range(element.size))
        for element in group.generate_schreier_sims()
    }


def split_top_level(text: str) -> list[str]:
    result = []
    depth = 0
    beginning = 0
    for index, character in enumerate(text):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            result.append(text[beginning:index])
            beginning = index + 1
    result.append(text[beginning:])
    return [item for item in result if item]


def library_action(library_path: Path, label: str) -> tuple[tuple[Perm, ...], str]:
    library = library_path.read_text(encoding="utf-8", errors="replace")
    label_at = library.index(f'"{label}"')
    start = library.rfind("# 64512.", 0, label_at)
    finish = library.find("# 64512.", label_at)
    segment = library[start:finish]
    compact = re.sub(r"\s+", "", segment)
    names = re.search(r'\[\[1,"([a-z]+)"', compact).group(1)
    relation_start = compact.index("return[[") + len("return[[")
    middle = compact.index("],[[", relation_start)
    end = compact.index("]]];", middle)
    free_data = free_group(",".join(names))
    namespace = dict(zip(names, free_data[1:]))

    def convert(expression: str):
        return eval(expression.replace("^", "**"), {"__builtins__": {}}, namespace)

    relations = [
        convert(item)
        for item in split_top_level(compact[relation_start:middle])
    ]
    subgroup = [
        convert(item)
        for item in split_top_level(compact[middle + len("],[[") : end])
    ]
    fp_group = FpGroup(free_data[0], relations)
    table = fp_group.coset_enumeration(
        subgroup, strategy="relator_based", max_cosets=1_000_000
    )
    table.compress()
    table.standardize()
    if any(value is None for row in table.table for value in row):
        raise RuntimeError("incomplete coset table")
    degree = len(table.table)
    action = tuple(
        tuple(int(table.table[row][2 * column]) for row in range(degree))
        for column in range(len(free_data) - 1)
    )
    return action, names


def quotient_data(
    group: set[Perm], normal: set[Perm]
) -> tuple[list[tuple[Perm, ...]], dict[Perm, int], list[list[int]], int]:
    remaining = set(group)
    cosets = []
    while remaining:
        representative = min(remaining)
        coset = tuple(sorted(compose(value, representative) for value in normal))
        cosets.append(coset)
        remaining.difference_update(coset)
    cosets.sort()
    coset_of = {value: index for index, coset in enumerate(cosets) for value in coset}
    representatives = [coset[0] for coset in cosets]
    table = [
        [coset_of[compose(left, right)] for right in representatives]
        for left in representatives
    ]
    return cosets, coset_of, table, coset_of[identity(len(representatives[0]))]


def q_inverse(value: int, one: int, table: list[list[int]]) -> int:
    return next(candidate for candidate in range(len(table)) if table[value][candidate] == one)


def quotient_isomorphism(
    qx: int, qy: int, one: int, table: list[list[int]], px: Perm, py: Perm
) -> dict[int, Perm]:
    steps = (
        (qx, px),
        (q_inverse(qx, one, table), invert(px)),
        (qy, py),
        (q_inverse(qy, one, table), invert(py)),
    )
    mapping = {one: identity(len(px))}
    queue = deque([one])
    while queue:
        current = queue.popleft()
        for qstep, pstep in steps:
            nxt = table[current][qstep]
            image = compose(mapping[current], pstep)
            if nxt in mapping:
                if mapping[nxt] != image:
                    raise RuntimeError("quotient map conflict")
            else:
                mapping[nxt] = image
                queue.append(nxt)
    if len(mapping) != len(table) or len(set(mapping.values())) != len(table):
        raise RuntimeError("quotient map not bijective")
    return mapping


def hom_table(
    domain_size: int,
    domain_generators: tuple[Perm, Perm],
    image_generators: tuple[Perm, Perm],
) -> dict[Perm, Perm]:
    one_domain = identity(len(domain_generators[0]))
    one_image = identity(len(image_generators[0]))
    steps = []
    for domain, image in zip(domain_generators, image_generators):
        steps.extend(((domain, image), (invert(domain), invert(image))))
    mapping = {one_domain: one_image}
    queue = deque([one_domain])
    while queue:
        current = queue.popleft()
        for domain_step, image_step in steps:
            nxt = compose(current, domain_step)
            image = compose(mapping[current], image_step)
            if nxt in mapping:
                if mapping[nxt] != image:
                    raise RuntimeError("homomorphism conflict")
            else:
                mapping[nxt] = image
                queue.append(nxt)
    if len(mapping) != domain_size:
        raise RuntimeError("marked generators do not generate domain")
    return mapping


def gf8_product(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
        if left & 8:
            left ^= GF8_POLY
    return result & 7


def gf8_inverse(value: int) -> int:
    return next(candidate for candidate in range(1, 8) if gf8_product(value, candidate) == 1)


def line_action(matrix: tuple[tuple[int, int], tuple[int, int]]) -> Perm:
    result = []
    for left, right in LINES:
        first = gf8_product(left, matrix[0][0]) ^ gf8_product(right, matrix[1][0])
        second = gf8_product(left, matrix[0][1]) ^ gf8_product(right, matrix[1][1])
        line = (1, gf8_product(second, gf8_inverse(first))) if first else (0, 1)
        result.append(LINES.index(line))
    return tuple(result)


def canonical_group() -> tuple[Perm, Perm, set[Perm]]:
    s = line_action(((1, 0), (1, 1)))
    t = line_action(((4, 3), (1, 5)))
    w = compose(s, invert(t))
    x = power(w, 2)
    y = compose(compose(invert(s), x), s)
    return x, y, generated((x, y))


def target_keys(elements: set[Perm], x: Perm, y: Perm) -> tuple[set[tuple[int, int]], dict]:
    ordered = sorted(elements)
    index = {value: position for position, value in enumerate(ordered)}
    z = invert(reverse_product((x, y)))
    theta = hom_table(len(elements), (x, y), (y, x))
    tau = hom_table(len(elements), (x, y), (y, z))
    one = identity(len(x))
    charming = (0, 2, 3, 5, 6, 8)
    counters = {
        "candidate_total": len(elements) * len(charming),
        "h10_fail": 0,
        "h11_fail": 0,
        "generation_fail": 0,
    }
    keys = set()
    for f in ordered:
        h10 = reverse_product((f, theta[f])) == one
        for m in charming:
            if not h10:
                counters["h10_fail"] += 1
                continue
            ymf = reverse_product((power(y, m), f))
            tau1 = tau[ymf]
            tau2 = tau[tau1]
            if reverse_product((tau2, tau1, ymf)) != one:
                counters["h11_fail"] += 1
                continue
            exponent = 2 * m + 1
            left = power(x, exponent)
            right = reverse_product((invert(f), power(y, exponent), f))
            if len(generated((left, right))) != len(elements):
                counters["generation_fail"] += 1
                continue
            keys.add((m, index[f]))
    counters["shadow_total"] = len(keys)
    counters["bookkeeping_identity"] = (
        counters["candidate_total"]
        - counters["h10_fail"]
        - counters["h11_fail"]
        - counters["generation_fail"]
        == len(keys)
    )
    return keys, counters


def source_result(
    elements: list[Perm],
    coset_of: dict[Perm, int],
    quotient_map: dict[int, Perm],
    quotient_index: dict[Perm, int],
    target: set[tuple[int, int]],
    s: Perm,
    t: Perm,
) -> dict:
    w = compose(s, invert(t))
    x = power(w, 2)
    y = compose(compose(invert(s), x), s)
    z = invert(reverse_product((x, y)))
    theta = hom_table(len(elements), (x, y), (y, x))
    tau = hom_table(len(elements), (x, y), (y, z))
    one = identity(len(x))
    charming = (0, 2, 3, 5, 6, 8)
    counters = {
        "candidate_total": len(elements) * len(charming),
        "h10_fail": 0,
        "h11_fail": 0,
        "generation_fail": 0,
    }
    keys = set()
    shadow_count = 0
    for f in elements:
        h10 = reverse_product((f, theta[f])) == one
        for m in charming:
            if not h10:
                counters["h10_fail"] += 1
                continue
            ymf = reverse_product((power(y, m), f))
            tau1 = tau[ymf]
            tau2 = tau[tau1]
            if reverse_product((tau2, tau1, ymf)) != one:
                counters["h11_fail"] += 1
                continue
            key = (m, quotient_index[quotient_map[coset_of[f]]])
            if key not in target:
                counters["generation_fail"] += 1
                continue
            shadow_count += 1
            keys.add(key)
    counters["shadow_total"] = shadow_count
    counters["bookkeeping_identity"] = (
        counters["candidate_total"]
        - counters["h10_fail"]
        - counters["h11_fail"]
        - counters["generation_fail"]
        == shadow_count
    )
    return {
        "source_scan": counters,
        "source_shadow_count": shadow_count,
        "reduced_keys": [list(value) for value in sorted(keys)],
        "reduced_key_count": len(keys),
        "raw_image_size": 18 * len(keys),
        "missing_key_count": len(target - keys),
        "first_missing_key": list(min(target - keys)) if target - keys else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--preflight", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--hard-timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    began = time.monotonic()
    source_path = Path(args.source)
    preflight_path = Path(args.preflight)
    output_path = Path(args.output)
    checkpoint_path = Path(args.checkpoint)
    state = {
        "schema": "campaign138_d7_measure_check_checkpoint/v1",
        "stage": "start",
        "complete": False,
        "orbit_results": [],
    }
    atomic_json(checkpoint_path, state)

    def update(stage: str, **extra: object) -> None:
        state.update(stage=stage, elapsed_ms=int(1000 * (time.monotonic() - began)), **extra)
        atomic_json(checkpoint_path, state)

    def timeout() -> None:
        if not state["complete"]:
            update("hard_timeout")
            os._exit(124)

    alarm = threading.Timer(args.hard_timeout_seconds, timeout)
    alarm.daemon = True
    alarm.start()
    try:
        source = json.loads(source_path.read_text(encoding="utf-8"))
        preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
        library_path = Path(preflight["library_path"])
        action, names = library_action(library_path, source["candidate"]["label"])
        group = sympy_elements(action)
        named = dict(zip(names, action))
        module = sympy_elements(tuple(named[name] for name in names[3:]))
        cosets, coset_of, qtable, qone = quotient_data(group, module)
        update("group_ready", group_order=len(group), module_order=len(module))

        px, py, quotient_group = canonical_group()
        target, target_counts = target_keys(quotient_group, px, py)
        quotient_ordered = sorted(quotient_group)
        quotient_index = {value: index for index, value in enumerate(quotient_ordered)}
        selected = next(
            item for item in preflight["candidates"] if item["family_key"] == [16, 7, 3]
        )
        reconstructed = []
        elements = sorted(group)
        for orbit in selected["marked_pair_orbits"]:
            index = orbit["orbit_index"]
            update("orbit", current_orbit=index)
            s, t = tuple(orbit["S"]), tuple(orbit["T"])
            w = compose(s, invert(t))
            x = power(w, 2)
            y = compose(compose(invert(s), x), s)
            qmap = quotient_isomorphism(
                coset_of[x], coset_of[y], qone, qtable, px, py
            )
            result = source_result(
                elements, coset_of, qmap, quotient_index, target, s, t
            )
            result.update(
                orbit_index=index,
                S_sha256=sha_obj(list(s)),
                T_sha256=sha_obj(list(t)),
            )
            reconstructed.append(result)
            state["orbit_results"] = reconstructed
            update("orbit_complete", completed_orbit=index)

        source_results = source["orbit_results"]
        scalar_fields = (
            "orbit_index",
            "S_sha256",
            "T_sha256",
            "source_shadow_count",
            "reduced_key_count",
            "raw_image_size",
            "missing_key_count",
            "first_missing_key",
            "reduced_keys",
        )
        checks = {
            "schema": source["schema"] == "campaign138_d7_measure/v1",
            "source_bound": source["input_sha256"]["preflight"] == sha_file(preflight_path),
            "library_bound": source["input_sha256"]["library"] == sha_file(library_path),
            "group_scalars": (
                len(group) == 64512
                and len(module) == 128
                and len(cosets) == len(quotient_group) == 504
            ),
            "target": (
                len(target) == 54
                and [list(value) for value in sorted(target)] == source["target_keys"]
                and target_counts == source["target_scan"]
            ),
            "orbit_count": len(reconstructed) == len(source_results) == 16,
            "orbit_scalars": all(
                all(actual[field] == expected[field] for field in scalar_fields)
                and actual["source_scan"] == expected["source_scan"]
                for actual, expected in zip(reconstructed, source_results)
            ),
            "positive_control": source["positive_control"]["passed"],
            "stop_rule": (
                source["first_loss"] is None
                and not source["stopped_at_first_loss"]
                and source["all_frozen_orbits_consumed"]
                and source["status"] == "NO_LOSS_IN_RELAXED_DETECTOR"
            ),
            "noncontact": source["noncontact"] == {
                "u": False,
                "c": False,
                "sealed_three_quantities": False,
                "sealed_K5": False,
            },
        }
        verdict = {
            "schema": "campaign138_d7_measure_check/v1",
            "source_sha256": sha_file(source_path),
            "checker_sha256": sha_file(Path(__file__)),
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
        atomic_json(output_path, verdict)
        state["complete"] = True
        update(
            "complete",
            all_checks_true=verdict["all_checks_true"],
            output_sha256=sha_file(output_path),
        )
        print(json.dumps(verdict["reconstructed"], sort_keys=True))
        if not verdict["all_checks_true"]:
            raise SystemExit(2)
    finally:
        alarm.cancel()


if __name__ == "__main__":
    main()
