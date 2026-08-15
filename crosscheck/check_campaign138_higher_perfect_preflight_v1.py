#!/usr/bin/env python3
"""Independent reconstruction of all higher PerfectGroups preflight records."""

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


def order(value: Perm, bound: int = 2048) -> int:
    current = one(len(value))
    for exponent in range(1, bound + 1):
        current = product(current, value)
        if current == one(len(value)):
            return exponent
    raise RuntimeError("order bound")


def group(generators: tuple[Perm, ...]) -> PermutationGroup:
    return PermutationGroup(*[Permutation(list(value)) for value in generators])


def elements(generators: tuple[Perm, ...]) -> set[Perm]:
    permutation_group = group(generators)
    degree = len(generators[0])
    return {
        tuple(int(element(index)) for index in range(degree))
        for element in permutation_group.generate_schreier_sims()
    }


def split_top_level(text: str) -> list[str]:
    result = []
    round_depth = 0
    square_depth = 0
    beginning = 0
    for index, character in enumerate(text):
        if character == "(":
            round_depth += 1
        elif character == ")":
            round_depth -= 1
        elif character == "[":
            square_depth += 1
        elif character == "]":
            square_depth -= 1
        elif character == "," and round_depth == square_depth == 0:
            result.append(text[beginning:index])
            beginning = index + 1
    result.append(text[beginning:])
    return [item for item in result if item]


def list_items(text: str) -> list[str]:
    if not text.startswith("[") or not text.endswith("]"):
        raise ValueError("expected list")
    return split_top_level(text[1:-1])


def matching_square(text: str, start: int) -> int:
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "[":
            depth += 1
        elif text[index] == "]":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unterminated list")


def parse_action(library_path: Path, meta: dict) -> tuple[tuple[Perm, ...], dict]:
    library = library_path.read_text(encoding="utf-8", errors="replace")
    label_at = library.index(f'"{meta["label"]}"')
    marker = f'# {meta["order_if_2_kernel"]}.'
    start = library.rfind(marker, 0, label_at)
    finish = library.find(marker, label_at)
    if finish < 0:
        finish = library.find("PERFGRP[", label_at)
    segment = library[start:finish]
    compact = re.sub(r"\s+", "", re.sub(r"#[^\r\n]*", "", segment))
    names = re.search(r'\[\[1,"([a-z]+)"', compact).group(1)
    expression_start = compact.index("return") + len("return")
    expression_end = matching_square(compact, expression_start)
    outer = list_items(compact[expression_start : expression_end + 1])
    free_data = free_group(",".join(names))
    namespace = dict(zip(names, free_data[1:]))

    def translate(expression: str):
        expression = re.sub(
            r"\b([a-z])\^([a-z])\b",
            lambda match: f"({match.group(2)}**-1*{match.group(1)}*{match.group(2)})",
            expression,
        )
        return eval(expression.replace("^", "**"), {"__builtins__": {}}, namespace)

    relations = [translate(item) for item in list_items(outer[0])]
    subgroups = [
        [translate(item) for item in list_items(subgroup)]
        for subgroup in list_items(outer[1])
    ]
    fp_group = FpGroup(free_data[0], relations)
    tables = []
    for subgroup in subgroups:
        table = fp_group.coset_enumeration(
            subgroup, strategy="relator_based", max_cosets=2_000_000
        )
        table.compress()
        table.standardize()
        if any(value is None for row in table.table for value in row):
            raise RuntimeError("incomplete table")
        tables.append(table)
    block_sizes = [len(table.table) for table in tables]
    action = []
    for column in range(len(free_data) - 1):
        value = []
        offset = 0
        for table in tables:
            value.extend(
                offset + int(table.table[row][2 * column])
                for row in range(len(table.table))
            )
            offset += len(table.table)
        action.append(tuple(value))
    return tuple(action), {
        "names": names,
        "block_sizes": block_sizes,
        "segment_sha256": hashlib.sha256(segment.encode()).hexdigest(),
    }


def positive_word(word: str, named: dict[str, Perm]) -> Perm:
    result = one(len(next(iter(named.values()))))
    for letter in word:
        result = product(result, named[letter])
    return result


def summarize(library_root: Path, meta: dict) -> dict:
    library_path = library_root / meta["file"]
    action, parsed = parse_action(library_path, meta)
    named = dict(zip(parsed["names"], action))
    module = elements(tuple(named[name] for name in parsed["names"][3:]))
    group_order = int(group(action).order())
    base_s = positive_word("accbxbccb", named)
    base_t = positive_word("cacaccwb", named)
    lifts_s = sorted({
        product(value, base_s)
        for value in module
        if order(product(value, base_s)) == 2
    })
    lifts_t = sorted({
        product(value, base_t)
        for value in module
        if order(product(value, base_t)) == 3
    })
    remaining = {(left, right) for left in lifts_s for right in lifts_t}
    pair_count = len(remaining)
    orbits = []
    while remaining:
        seed = min(remaining)
        orbit = {
            (conjugate(seed[0], value), conjugate(seed[1], value))
            for value in module
        } & remaining
        representative = min(orbit)
        generated_order = int(group(representative).order())
        orbits.append({
            "orbit_size": len(orbit),
            "generated_order": generated_order,
            "generates_full_group": generated_order == group_order,
            "is_complement": generated_order == 504,
            "S_sha256": sha_obj(list(representative[0])),
            "T_sha256": sha_obj(list(representative[1])),
            "S": list(representative[0]),
            "T": list(representative[1]),
        })
        remaining -= orbit
    orbits.sort(key=lambda item: (item["S"], item["T"]))
    for index, orbit in enumerate(orbits):
        orbit["orbit_index"] = index
    return {
        "family_key": meta["family_key"],
        "label": meta["label"],
        "file": meta["file"],
        "library_sha256": sha_file(library_path),
        "segment_sha256": parsed["segment_sha256"],
        "generator_names": parsed["names"],
        "block_sizes": parsed["block_sizes"],
        "coset_degree": sum(parsed["block_sizes"]),
        "group_order": group_order,
        "module_order": len(module),
        "module_element_order_distribution": {
            str(key): value for key, value in sorted(Counter(order(item) for item in module).items())
        },
        "base_lift_orders": [order(base_s), order(base_t)],
        "order2_lift_count": len(lifts_s),
        "order3_lift_count": len(lifts_t),
        "marked_pair_count": pair_count,
        "marked_pair_orbit_count": len(orbits),
        "generating_orbit_count": sum(item["generates_full_group"] for item in orbits),
        "complement_orbit_count": sum(item["is_complement"] for item in orbits),
        "marked_pair_orbits": orbits,
    }


def normalize_d10(source: dict) -> dict:
    candidate = source["candidate"]
    return {
        "family_key": candidate["family_key"],
        "label": candidate["label"],
        "file": "perf10.grp",
        "library_sha256": source["library_sha256"],
        "segment_sha256": source["segment_sha256"],
        "generator_names": candidate["generator_names"],
        "block_sizes": candidate["block_sizes"],
        "coset_degree": candidate["coset_degree"],
        "group_order": candidate["group_order"],
        "module_order": candidate["kernel_order"],
        "module_element_order_distribution": candidate["kernel_element_order_distribution"],
        "base_lift_orders": candidate["base_lift_orders"],
        "order2_lift_count": candidate["order2_lift_count"],
        "order3_lift_count": candidate["order3_lift_count"],
        "marked_pair_count": candidate["marked_pair_count"],
        "marked_pair_orbit_count": candidate["marked_pair_orbit_count"],
        "generating_orbit_count": candidate["generating_orbit_count"],
        "complement_orbit_count": candidate["complement_orbit_count"],
        "marked_pair_orbits": candidate["marked_pair_orbits"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--d10-source", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--hard-timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    source_path = Path(args.source)
    d10_path = Path(args.d10_source)
    metadata_path = Path(args.metadata)
    output_path = Path(args.output)
    checkpoint_path = Path(args.checkpoint)
    began = time.monotonic()
    state = {
        "schema": "campaign138_higher_perfect_check_checkpoint/v1",
        "stage": "start",
        "complete": False,
        "reconstructed": [],
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
        d10_source = json.loads(d10_path.read_text(encoding="utf-8"))
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        expected_six = [item for item in source["results"] if item["status"] == "CONSTRUCTED"]
        expected = expected_six + [normalize_d10(d10_source)]
        expected.sort(key=lambda item: item["family_key"])
        meta_by_key = {tuple(item["family_key"]): item for item in metadata["records"]}
        reconstructed = []
        for item in expected:
            update("candidate", current_family_key=item["family_key"])
            actual = summarize(Path(metadata["library_root"]), meta_by_key[tuple(item["family_key"])])
            reconstructed.append(actual)
            state["reconstructed"] = reconstructed
            update("candidate_complete", completed_family_key=item["family_key"])
        fields = (
            "family_key", "label", "file", "library_sha256", "segment_sha256",
            "generator_names", "block_sizes", "coset_degree", "group_order",
            "module_order", "module_element_order_distribution", "base_lift_orders",
            "order2_lift_count", "order3_lift_count", "marked_pair_count",
            "marked_pair_orbit_count", "generating_orbit_count",
            "complement_orbit_count", "marked_pair_orbits",
        )
        non_elementary = [
            item["family_key"]
            for item in reconstructed
            if set(item["module_element_order_distribution"]) - {"1", "2"}
        ]
        checks = {
            "source_schemas": (
                source["schema"] == "campaign138_higher_perfect_preflight/v1"
                and d10_source["schema"] == "campaign138_d10_preflight/v1"
            ),
            "record_count": len(expected) == len(reconstructed) == 7,
            "all_fields": all(
                all(actual[field] == wanted[field] for field in fields)
                for actual, wanted in zip(reconstructed, expected)
            ),
            "group_kernel_orders": all(
                item["group_order"] == 504 * item["module_order"]
                for item in reconstructed
            ),
            "non_elementary_reclassification": non_elementary == [[16, 8, 2], [16, 9, 2], [16, 10, 1]],
            "parent_control_failure_explained": source["positive_control"]["passed"] is False,
            "only_generating_family": [
                item["family_key"] for item in reconstructed if item["generating_orbit_count"]
            ] == [[16, 8, 4]],
            "no_complements": all(item["complement_orbit_count"] == 0 for item in reconstructed),
            "no_outcomes": (
                source["outcomes_opened"] == {"shadow": 0, "reduction": 0, "element_survival": 0}
                and d10_source["outcomes_opened"] == {"shadow": 0, "reduction": 0, "element_survival": 0}
            ),
        }
        verdict = {
            "schema": "campaign138_higher_perfect_preflight_check/v1",
            "source_sha256": sha_file(source_path),
            "d10_source_sha256": sha_file(d10_path),
            "checker_sha256": sha_file(Path(__file__)),
            "checks": checks,
            "all_checks_true": all(checks.values()),
            "reconstructed": {
                "candidate_count": len(reconstructed),
                "non_elementary_family_keys": non_elementary,
                "generating_family_keys": [
                    item["family_key"] for item in reconstructed if item["generating_orbit_count"]
                ],
                "generating_orbit_count": sum(item["generating_orbit_count"] for item in reconstructed),
                "zero_order2_lift_family_count": sum(item["order2_lift_count"] == 0 for item in reconstructed),
            },
        }
        atomic_json(output_path, verdict)
        state["complete"] = True
        update("complete", all_checks_true=verdict["all_checks_true"], output_sha256=sha_file(output_path))
        print(json.dumps(verdict["reconstructed"], sort_keys=True))
        if not verdict["all_checks_true"]:
            raise SystemExit(2)
    finally:
        alarm.cancel()


if __name__ == "__main__":
    main()
