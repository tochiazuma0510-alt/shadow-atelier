#!/usr/bin/env python3
"""Independent checker for the campaign 138 d=7 preflight."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import threading
import time
from collections import Counter
from pathlib import Path

from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.free_groups import free_group


Perm = tuple[int, ...]
LABELS = (
    "L2(8) N 2^6 E 2^1 I",
    "L2(8) N 2^6 E 2^1 II",
    "L2(8) N 2^6 E 2^1 III",
)


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha_obj(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def one(degree: int) -> Perm:
    return tuple(range(degree))


def product(left: Perm, right: Perm) -> Perm:
    return tuple(right[left[index]] for index in range(len(left)))


def inverse(value: Perm) -> Perm:
    answer = [0] * len(value)
    for source, target in enumerate(value):
        answer[target] = source
    return tuple(answer)


def conjugate(value: Perm, by: Perm) -> Perm:
    return product(product(inverse(by), value), by)


def order(value: Perm, bound: int = 1024) -> int:
    current = one(len(value))
    for exponent in range(1, bound + 1):
        current = product(current, value)
        if current == one(len(value)):
            return exponent
    raise RuntimeError("order bound")


def sympy_group_order(generators: list[Perm] | tuple[Perm, ...]) -> int:
    return int(PermutationGroup(*[Permutation(list(value)) for value in generators]).order())


def sympy_elements(generators: tuple[Perm, ...]) -> set[Perm]:
    group = PermutationGroup(*[Permutation(list(value)) for value in generators])
    return {tuple(int(item(index)) for index in range(item.size)) for item in group.generate_schreier_sims()}


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


def extract(library: str, label: str) -> dict:
    label_at = library.index(f'"{label}"')
    start = library.rfind("# 64512.", 0, label_at)
    finish = library.find("# 64512.", label_at)
    if finish < 0:
        finish = library.find("PERFGRP[99]", label_at)
    segment = library[start:finish]
    compact = "".join(segment.split())
    names = re.search(r'\[\[1,"([a-z]+)"', compact).group(1)
    relation_start = compact.index("return[[") + len("return[[")
    middle = compact.index("],[[", relation_start)
    end = compact.index("]]];", middle)
    relation_source = compact[relation_start:middle]
    subgroup_source = compact[middle + 4 : end]
    family = re.search(r'\[16,(\d+),(\d+)\]', compact)
    free_data = free_group(",".join(names))
    namespace = dict(zip(names, free_data[1:]))
    convert = lambda expression: eval(expression.replace("^", "**"), {"__builtins__": {}}, namespace)
    return {
        "label": label,
        "family_key": [16, int(family.group(1)), int(family.group(2))],
        "names": names,
        "free": free_data[0],
        "generators": tuple(free_data[1:]),
        "relations": [convert(item) for item in split_top_level(relation_source)],
        "subgroup": [convert(item) for item in split_top_level(subgroup_source)],
        "segment_sha256": hashlib.sha256(segment.encode()).hexdigest(),
    }


def action(entry: dict) -> tuple[tuple[Perm, ...], int]:
    fp_group = FpGroup(entry["free"], entry["relations"])
    table = fp_group.coset_enumeration(entry["subgroup"], strategy="relator_based", max_cosets=1_000_000)
    table.compress()
    table.standardize()
    degree = len(table.table)
    if any(value is None for row in table.table for value in row):
        raise RuntimeError("incomplete table")
    generators = tuple(
        tuple(int(table.table[row][2 * column]) for row in range(degree))
        for column in range(len(entry["generators"]))
    )
    return generators, degree


def positive_word(word: str, generators: dict[str, Perm]) -> Perm:
    result = one(len(next(iter(generators.values()))))
    for letter in word:
        result = product(result, generators[letter])
    return result


def candidate_summary(entry: dict) -> dict:
    generators, degree = action(entry)
    named = dict(zip(entry["names"], generators))
    module_generators = tuple(named[name] for name in entry["names"][3:])
    module = sympy_elements(module_generators)
    base_s = positive_word("accbxbccb", named)
    base_t = positive_word("cacaccwb", named)
    lifts_s = sorted({product(value, base_s) for value in module if order(product(value, base_s)) == 2})
    lifts_t = sorted({product(value, base_t) for value in module if order(product(value, base_t)) == 3})
    all_pairs = {(left, right) for left in lifts_s for right in lifts_t}
    remaining = set(all_pairs)
    orbits = []
    while remaining:
        seed = min(remaining)
        orbit = {(conjugate(seed[0], value), conjugate(seed[1], value)) for value in module} & all_pairs
        representative = min(orbit)
        generated_order = sympy_group_order(representative)
        orbits.append(
            {
                "representative": representative,
                "orbit_size": len(orbit),
                "generated_order": generated_order,
            }
        )
        remaining -= orbit
    orbits.sort(key=lambda item: item["representative"])
    return {
        "label": entry["label"],
        "family_key": entry["family_key"],
        "segment_sha256": entry["segment_sha256"],
        "generator_names": entry["names"],
        "coset_degree": degree,
        "group_order": sympy_group_order(generators),
        "module_order": len(module),
        "module_generator_count": len(module_generators),
        "module_element_order_distribution": {
            str(key): value for key, value in sorted(Counter(order(item) for item in module).items())
        },
        "base_lift_orders": [order(base_s), order(base_t)],
        "order2_lift_count": len(lifts_s),
        "order3_lift_count": len(lifts_t),
        "marked_pair_count": len(all_pairs),
        "module_conjugacy_orbit_count": len(orbits),
        "orbits": orbits,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--hard-timeout-seconds", type=int, default=240)
    args = parser.parse_args()
    began = time.monotonic()
    source_path = Path(args.source)
    output_path = Path(args.output)
    checkpoint_path = Path(args.checkpoint)
    state = {"schema": "campaign138_d7_check_checkpoint/v1", "stage": "start", "complete": False}
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
        library_path = Path(source["library_path"])
        library = library_path.read_text(encoding="utf-8")
        reconstructed = []
        for index, label in enumerate(LABELS):
            update("candidate", candidate_index=index)
            reconstructed.append(candidate_summary(extract(library, label)))
        checks = {
            "schema": source["schema"] == "campaign138_d7_preflight/v1",
            "library": sha_file(library_path) == source["library_sha256"],
            "candidate_count": len(source["candidates"]) == len(reconstructed) == 3,
            "candidate_scalars": all(
                all(
                    actual[key] == expected[key]
                    for key in (
                        "label", "family_key", "segment_sha256", "generator_names",
                        "coset_degree", "group_order", "module_order", "module_generator_count",
                        "module_element_order_distribution", "base_lift_orders",
                        "order2_lift_count", "order3_lift_count", "marked_pair_count",
                        "module_conjugacy_orbit_count",
                    )
                )
                for actual, expected in zip(source["candidates"], reconstructed)
            ),
            "pair_orbits": all(
                len(actual["marked_pair_orbits"]) == len(expected["orbits"])
                and all(
                    a["orbit_index"] == orbit_index
                    and a["orbit_size"] == e["orbit_size"]
                    and a["generated_order"] == e["generated_order"]
                    and a["generates_full_group"] == (e["generated_order"] == 64512)
                    and a["S"] == list(e["representative"][0])
                    and a["T"] == list(e["representative"][1])
                    and a["S_sha256"] == sha_obj(list(e["representative"][0]))
                    and a["T_sha256"] == sha_obj(list(e["representative"][1]))
                    for orbit_index, (a, e) in enumerate(zip(actual["marked_pair_orbits"], expected["orbits"]))
                )
                for actual, expected in zip(source["candidates"], reconstructed)
            ),
            "aggregate": source["aggregate"] == {
                "candidate_count": 3,
                "marked_pair_count": sum(item["marked_pair_count"] for item in reconstructed),
                "marked_pair_orbit_count": sum(item["module_conjugacy_orbit_count"] for item in reconstructed),
                "generating_orbit_count": sum(
                    orbit["generated_order"] == 64512 for item in reconstructed for orbit in item["orbits"]
                ),
                "split_complement_orbit_count": sum(
                    orbit["generated_order"] == 504 for item in reconstructed for orbit in item["orbits"]
                ),
            },
            "no_outcomes": source["outcomes_opened"] == {"shadow": 0, "reduction": 0, "element_survival": 0},
            "positive_control": source["positive_control"]["passed"],
        }
        result = {
            "schema": "campaign138_d7_preflight_check/v1",
            "source_sha256": sha_file(source_path),
            "checker_sha256": sha_file(Path(__file__)),
            "checks": checks,
            "all_checks_true": all(checks.values()),
            "reconstructed": source["aggregate"],
        }
        atomic_json(output_path, result)
        update("complete", complete=True, all_checks_true=result["all_checks_true"], output_sha256=sha_file(output_path))
        if not result["all_checks_true"]:
            raise SystemExit(2)
    finally:
        alarm.cancel()


if __name__ == "__main__":
    main()
