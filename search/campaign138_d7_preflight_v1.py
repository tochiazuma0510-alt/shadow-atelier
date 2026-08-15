#!/usr/bin/env python3
"""Preflight for the three unmeasured [16,7,2..4] library records.

The GAP source function is translated to a SymPy finitely presented group.
Only group construction, the elementary kernel, and marked lift orbits are
opened.  No shadow or reduction image is formed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import threading
import time
from collections import Counter, deque
from pathlib import Path

from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.free_groups import free_group


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / (
    "GAP-4.16.0/runtime/opt/gap-4.16.0/grp/perf6.grp"
)
LABELS = (
    "L2(8) N 2^6 E 2^1 I",
    "L2(8) N 2^6 E 2^1 II",
    "L2(8) N 2^6 E 2^1 III",
)
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
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def identity(degree: int) -> Perm:
    return tuple(range(degree))


def mul(left: Perm, right: Perm) -> Perm:
    return tuple(right[left[index]] for index in range(len(left)))


def inv(value: Perm) -> Perm:
    answer = [0] * len(value)
    for source, target in enumerate(value):
        answer[target] = source
    return tuple(answer)


def power(value: Perm, exponent: int) -> Perm:
    if exponent < 0:
        return power(inv(value), -exponent)
    answer = identity(len(value))
    factor = value
    while exponent:
        if exponent & 1:
            answer = mul(answer, factor)
        factor = mul(factor, factor)
        exponent >>= 1
    return answer


def element_order(value: Perm, bound: int = 1024) -> int:
    answer = identity(len(value))
    for exponent in range(1, bound + 1):
        answer = mul(answer, value)
        if answer == identity(len(value)):
            return exponent
    raise RuntimeError("element order bound")


def closure(generators: tuple[Perm, ...], degree: int | None = None) -> set[Perm]:
    if degree is None:
        degree = len(generators[0])
    one = identity(degree)
    seen = {one}
    queue = deque([one])
    while queue:
        current = queue.popleft()
        for generator in generators:
            new = mul(current, generator)
            if new not in seen:
                seen.add(new)
                queue.append(new)
    return seen


def conjugate(value: Perm, by: Perm) -> Perm:
    return mul(mul(inv(by), value), by)


def split_expressions(text: str) -> list[str]:
    answer = []
    depth = 0
    start = 0
    for index, character in enumerate(text):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            answer.append(text[start:index])
            start = index + 1
    answer.append(text[start:])
    return [item for item in answer if item]


def parse_entry(library_text: str, label: str) -> dict:
    label_position = library_text.index(f'"{label}"')
    marker_position = library_text.rfind("# 64512.", 0, label_position)
    next_marker = library_text.find("# 64512.", label_position)
    if next_marker < 0:
        next_marker = library_text.find("PERFGRP[99]", label_position)
    segment = library_text[marker_position:next_marker]
    compact = re.sub(r"\s+", "", segment)
    generator_names = re.search(r'\[\[1,"([a-z]+)"', compact).group(1)
    return_position = compact.index("return[[") + len("return[[")
    separator = compact.index("],[[", return_position)
    end = compact.index("]]];", separator)
    relation_text = compact[return_position:separator]
    subgroup_text = compact[separator + len("],[[") : end]
    marker = re.search(r'\[16,(\d+),(\d+)\]', compact)
    free_data = free_group(",".join(generator_names))
    free = free_data[0]
    generators = tuple(free_data[1:])
    namespace = dict(zip(generator_names, generators))

    def translate(expression: str):
        return eval(expression.replace("^", "**"), {"__builtins__": {}}, namespace)

    relations = [translate(item) for item in split_expressions(relation_text)]
    subgroup = [translate(item) for item in split_expressions(subgroup_text)]
    return {
        "label": label,
        "family_key": [16, int(marker.group(1)), int(marker.group(2))],
        "generator_names": generator_names,
        "free": free,
        "generators": generators,
        "relations": relations,
        "subgroup": subgroup,
        "segment_sha256": hashlib.sha256(segment.encode()).hexdigest(),
    }


def permutation_action(entry: dict) -> tuple[tuple[Perm, ...], int]:
    group = FpGroup(entry["free"], entry["relations"])
    table = group.coset_enumeration(
        entry["subgroup"], strategy="relator_based", max_cosets=1_000_000
    )
    table.compress()
    table.standardize()
    if any(value is None for row in table.table for value in row):
        raise RuntimeError("incomplete coset table")
    degree = len(table.table)
    action = tuple(
        tuple(int(table.table[row][2 * column]) for row in range(degree))
        for column in range(len(entry["generators"]))
    )
    return action, degree


def positive_word(word: str, generators: dict[str, Perm]) -> Perm:
    answer = identity(len(next(iter(generators.values()))))
    for letter in word:
        answer = mul(answer, generators[letter])
    return answer


def marked_pair_orbits(
    module: set[Perm], base_s: Perm, base_t: Perm
) -> tuple[list[Perm], list[Perm], list[dict]]:
    lifts_s = sorted({mul(value, base_s) for value in module if element_order(mul(value, base_s)) == 2})
    lifts_t = sorted({mul(value, base_t) for value in module if element_order(mul(value, base_t)) == 3})
    pairs = {(left, right) for left in lifts_s for right in lifts_t}
    unseen = set(pairs)
    orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {
            (conjugate(representative[0], value), conjugate(representative[1], value))
            for value in module
        } & pairs
        if not orbit:
            raise RuntimeError("empty module conjugacy orbit")
        canonical = min(orbit)
        orbits.append(
            {
                "representative": canonical,
                "orbit_size": len(orbit),
            }
        )
        unseen -= orbit
    orbits.sort(key=lambda item: item["representative"])
    return lifts_s, lifts_t, orbits


def summarize_candidate(entry: dict) -> dict:
    action, degree = permutation_action(entry)
    generators = dict(zip(entry["generator_names"], action))
    full_group = closure(action)
    module_generators = tuple(generators[name] for name in entry["generator_names"][3:])
    module = closure(module_generators)
    base_s = positive_word("accbxbccb", generators)
    base_t = positive_word("cacaccwb", generators)
    lifts_s, lifts_t, orbits = marked_pair_orbits(module, base_s, base_t)
    orbit_records = []
    for index, orbit in enumerate(orbits):
        left, right = orbit["representative"]
        generated_order = len(closure((left, right)))
        orbit_records.append(
            {
                "orbit_index": index,
                "orbit_size": orbit["orbit_size"],
                "generated_order": generated_order,
                "generates_full_group": generated_order == len(full_group),
                "S_sha256": sha_obj(list(left)),
                "T_sha256": sha_obj(list(right)),
                "S": list(left),
                "T": list(right),
            }
        )
    return {
        "label": entry["label"],
        "family_key": entry["family_key"],
        "segment_sha256": entry["segment_sha256"],
        "generator_names": entry["generator_names"],
        "coset_degree": degree,
        "group_order": len(full_group),
        "module_order": len(module),
        "module_generator_count": len(module_generators),
        "module_element_order_distribution": {
            str(key): value for key, value in sorted(Counter(element_order(item) for item in module).items())
        },
        "base_lift_orders": [element_order(base_s), element_order(base_t)],
        "order2_lift_count": len(lifts_s),
        "order3_lift_count": len(lifts_t),
        "marked_pair_count": len(lifts_s) * len(lifts_t),
        "module_conjugacy_orbit_count": len(orbits),
        "marked_pair_orbits": orbit_records,
        "generating_orbit_count": sum(item["generates_full_group"] for item in orbit_records),
        "split_complement_orbit_count": sum(item["generated_order"] == 504 for item in orbit_records),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prereg", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--hard-timeout-seconds", type=int, default=240)
    args = parser.parse_args()
    began = time.monotonic()
    prereg_path = Path(args.prereg)
    output_path = Path(args.output)
    checkpoint_path = Path(args.checkpoint)
    state = {"schema": "campaign138_d7_preflight_checkpoint/v1", "stage": "start", "complete": False}
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
        prereg = json.loads(prereg_path.read_text(encoding="utf-8"))
        if prereg["producer_sha256"] != sha_file(Path(__file__)):
            raise RuntimeError("preregistration binding mismatch")
        library_text = LIBRARY.read_text(encoding="utf-8")
        candidates = []
        for index, label in enumerate(LABELS):
            update("candidate", candidate_index=index, label=label)
            candidates.append(summarize_candidate(parse_entry(library_text, label)))
        positive_control = all(
            item["coset_degree"] == 112
            and item["group_order"] == 64512
            and item["module_order"] == 128
            and item["module_element_order_distribution"] == {"1": 1, "2": 127}
            for item in candidates
        )
        result = {
            "schema": "campaign138_d7_preflight/v1",
            "status": "PREFLIGHT_ONLY",
            "preregistration_sha256": sha_file(prereg_path),
            "producer_sha256": sha_file(Path(__file__)),
            "library_path": str(LIBRARY),
            "library_sha256": sha_file(LIBRARY),
            "candidates": candidates,
            "positive_control": {"passed": positive_control, "expected_degree": 112, "expected_order": 64512, "expected_module_order": 128},
            "aggregate": {
                "candidate_count": len(candidates),
                "marked_pair_count": sum(item["marked_pair_count"] for item in candidates),
                "marked_pair_orbit_count": sum(item["module_conjugacy_orbit_count"] for item in candidates),
                "generating_orbit_count": sum(item["generating_orbit_count"] for item in candidates),
                "split_complement_orbit_count": sum(item["split_complement_orbit_count"] for item in candidates),
            },
            "outcomes_opened": {"shadow": 0, "reduction": 0, "element_survival": 0},
            "noncontact": {"u": False, "c": False, "sealed_three_quantities": False, "sealed_K5": False},
        }
        if not positive_control:
            raise RuntimeError("group construction positive control failed")
        atomic_json(output_path, result)
        update("complete", complete=True, output_sha256=sha_file(output_path), **result["aggregate"])
    finally:
        alarm.cancel()


if __name__ == "__main__":
    main()
