#!/usr/bin/env python3
"""Preflight every higher 2-kernel PerfectGroups record marked nonsplit.

Each record is reconstructed in a separate subprocess.  The parent records a
hard timeout as an environment limitation and continues through the frozen
list.  No shadow or reduction image is formed here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter, deque
from pathlib import Path

from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.free_groups import free_group


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "search/certs/campaign138_perfect_metadata_v1_20260815.json"
PREREG = ROOT / "search/certs/campaign138_higher_perfect_preflight_prereg_v1_20260815.json"
FAMILY_KEYS = (
    (16, 8, 2),
    (16, 8, 3),
    (16, 8, 4),
    (16, 8, 5),
    (16, 9, 2),
    (16, 9, 3),
    (16, 10, 1),
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
    current = identity(len(value))
    for exponent in range(1, bound + 1):
        current = product(current, value)
        if current == identity(len(value)):
            return exponent
    raise RuntimeError("order bound")


def closure(generators: tuple[Perm, ...]) -> set[Perm]:
    one = identity(len(generators[0]))
    steps = generators + tuple(inverse(item) for item in generators)
    seen = {one}
    queue = deque([one])
    while queue:
        current = queue.popleft()
        for step in steps:
            nxt = product(current, step)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def group_order(generators: tuple[Perm, ...]) -> int:
    return int(
        PermutationGroup(*[Permutation(list(value)) for value in generators]).order()
    )


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
        elif character == "," and round_depth == 0 and square_depth == 0:
            result.append(text[beginning:index])
            beginning = index + 1
    result.append(text[beginning:])
    return [item for item in result if item]


def list_items(text: str) -> list[str]:
    if not text.startswith("[") or not text.endswith("]"):
        raise ValueError("expected list")
    return split_top_level(text[1:-1])


def parse_record(path: Path, label: str, order_value: int) -> dict:
    library = path.read_text(encoding="utf-8", errors="replace")
    label_at = library.index(f'"{label}"')
    marker = f"# {order_value}."
    start = library.rfind(marker, 0, label_at)
    finish = library.find(marker, label_at)
    if finish < 0:
        finish = library.find("PERFGRP[", label_at)
    segment = library[start:finish]
    compact = re.sub(r"\s+", "", segment)
    names = re.search(r'\[\[1,"([a-z]+)"', compact).group(1)
    expression_start = compact.index("return") + len("return")
    expression_end = compact.index(";end", expression_start)
    outer = list_items(compact[expression_start:expression_end])
    if len(outer) != 2:
        raise RuntimeError("unexpected return list")
    free_data = free_group(",".join(names))
    namespace = dict(zip(names, free_data[1:]))

    def translate(expression: str):
        return eval(expression.replace("^", "**"), {"__builtins__": {}}, namespace)

    relations = [translate(item) for item in list_items(outer[0])]
    subgroup_lists = [
        [translate(item) for item in list_items(subgroup)]
        for subgroup in list_items(outer[1])
    ]
    return {
        "names": names,
        "free": free_data[0],
        "generators": tuple(free_data[1:]),
        "relations": relations,
        "subgroup_lists": subgroup_lists,
        "segment_sha256": hashlib.sha256(segment.encode()).hexdigest(),
    }


def permutation_action(record: dict) -> tuple[tuple[Perm, ...], list[int]]:
    fp_group = FpGroup(record["free"], record["relations"])
    tables = []
    for subgroup in record["subgroup_lists"]:
        table = fp_group.coset_enumeration(
            subgroup, strategy="relator_based", max_cosets=2_000_000
        )
        table.compress()
        table.standardize()
        if any(value is None for row in table.table for value in row):
            raise RuntimeError("incomplete coset table")
        tables.append(table)
    block_sizes = [len(table.table) for table in tables]
    degree = sum(block_sizes)
    action = []
    for column in range(len(record["generators"])):
        value = []
        offset = 0
        for table in tables:
            value.extend(
                offset + int(table.table[row][2 * column])
                for row in range(len(table.table))
            )
            offset += len(table.table)
        if len(value) != degree:
            raise RuntimeError("action degree mismatch")
        action.append(tuple(value))
    return tuple(action), block_sizes


def positive_word(word: str, named: dict[str, Perm]) -> Perm:
    result = identity(len(next(iter(named.values()))))
    for letter in word:
        result = product(result, named[letter])
    return result


def worker(record_meta: dict) -> dict:
    library_path = Path(record_meta["library_root"]) / record_meta["file"]
    parsed = parse_record(
        library_path, record_meta["label"], record_meta["order_if_2_kernel"]
    )
    action, block_sizes = permutation_action(parsed)
    named = dict(zip(parsed["names"], action))
    module_generators = tuple(named[name] for name in parsed["names"][3:])
    module = closure(module_generators)
    group_size = group_order(action)
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
    orbit_records = []
    while remaining:
        seed = min(remaining)
        orbit = {
            (conjugate(seed[0], value), conjugate(seed[1], value))
            for value in module
        } & remaining
        representative = min(orbit)
        generated_order = group_order(representative)
        orbit_records.append({
            "orbit_size": len(orbit),
            "generated_order": generated_order,
            "generates_full_group": generated_order == group_size,
            "is_complement": generated_order == 504,
            "S_sha256": sha_obj(list(representative[0])),
            "T_sha256": sha_obj(list(representative[1])),
            "S": list(representative[0]),
            "T": list(representative[1]),
        })
        remaining -= orbit
    orbit_records.sort(key=lambda item: (item["S"], item["T"]))
    for index, item in enumerate(orbit_records):
        item["orbit_index"] = index
    return {
        "status": "CONSTRUCTED",
        "family_key": record_meta["family_key"],
        "label": record_meta["label"],
        "file": record_meta["file"],
        "library_sha256": sha_file(library_path),
        "segment_sha256": parsed["segment_sha256"],
        "generator_names": parsed["names"],
        "block_sizes": block_sizes,
        "coset_degree": sum(block_sizes),
        "group_order": group_size,
        "module_order": len(module),
        "module_element_order_distribution": {
            str(key): value
            for key, value in sorted(Counter(order(item) for item in module).items())
        },
        "base_lift_orders": [order(base_s), order(base_t)],
        "order2_lift_count": len(lifts_s),
        "order3_lift_count": len(lifts_t),
        "marked_pair_count": pair_count,
        "marked_pair_orbit_count": len(orbit_records),
        "generating_orbit_count": sum(item["generates_full_group"] for item in orbit_records),
        "complement_orbit_count": sum(item["is_complement"] for item in orbit_records),
        "marked_pair_orbits": orbit_records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-index", type=int)
    parser.add_argument(
        "--output",
        default="search/certs/campaign138_higher_perfect_preflight_v1_20260815.json",
    )
    parser.add_argument(
        "--checkpoint",
        default="search/certs/campaign138_higher_perfect_preflight_v1_checkpoint.json",
    )
    parser.add_argument("--hard-timeout-seconds-per-candidate", type=int, default=240)
    args = parser.parse_args()
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    selected = [
        {**record, "library_root": metadata["library_root"]}
        for record in metadata["records"]
        if tuple(record["family_key"]) in FAMILY_KEYS
    ]
    selected.sort(key=lambda item: item["family_key"])
    if [tuple(item["family_key"]) for item in selected] != list(FAMILY_KEYS):
        raise RuntimeError("frozen family universe mismatch")
    if args.worker_index is not None:
        print(json.dumps(worker(selected[args.worker_index]), sort_keys=True))
        return 0

    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    prereg_hash = sha_file(PREREG)
    results: list[dict] = []
    if checkpoint.exists():
        old = json.loads(checkpoint.read_text(encoding="utf-8"))
        if (
            old.get("schema") == "campaign138_higher_perfect_preflight_checkpoint/v1"
            and old.get("preregistration_sha256") == prereg_hash
        ):
            results = list(old.get("results", []))
    state = {
        "schema": "campaign138_higher_perfect_preflight_checkpoint/v1",
        "preregistration_sha256": prereg_hash,
        "stage": "start",
        "complete": False,
        "results": results,
    }
    atomic_json(checkpoint, state)
    completed = {tuple(item["family_key"]) for item in results}
    began = time.monotonic()
    for index, record in enumerate(selected):
        key = tuple(record["family_key"])
        if key in completed:
            continue
        state.update(
            stage="candidate",
            current_family_key=list(key),
            elapsed_ms=int(1000 * (time.monotonic() - began)),
        )
        atomic_json(checkpoint, state)
        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "--worker-index",
            str(index),
        ]
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        candidate_started = time.monotonic()
        try:
            completed_process = subprocess.run(
                command,
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
                timeout=args.hard_timeout_seconds_per_candidate,
                check=False,
            )
            if completed_process.returncode == 0:
                result = json.loads(completed_process.stdout)
            else:
                result = {
                    "status": "CONSTRUCTION_ERROR",
                    "family_key": list(key),
                    "label": record["label"],
                    "returncode": completed_process.returncode,
                    "stderr_tail": completed_process.stderr[-1000:],
                }
        except subprocess.TimeoutExpired:
            result = {
                "status": "CONSTRUCTION_TIMEOUT",
                "family_key": list(key),
                "label": record["label"],
                "hard_timeout_seconds": args.hard_timeout_seconds_per_candidate,
            }
        result["elapsed_ms"] = int(1000 * (time.monotonic() - candidate_started))
        results.append(result)
        results.sort(key=lambda item: item["family_key"])
        state["results"] = results
        state["stage"] = "candidate_complete"
        atomic_json(checkpoint, state)

    constructed = [item for item in results if item["status"] == "CONSTRUCTED"]
    cert = {
        "schema": "campaign138_higher_perfect_preflight/v1",
        "status": "PREFLIGHT_ONLY",
        "producer_sha256": sha_file(Path(__file__)),
        "preregistration_sha256": prereg_hash,
        "metadata_sha256": sha_file(METADATA),
        "candidate_count": len(selected),
        "results": results,
        "aggregate": {
            "constructed_count": len(constructed),
            "timeout_count": sum(item["status"] == "CONSTRUCTION_TIMEOUT" for item in results),
            "error_count": sum(item["status"] == "CONSTRUCTION_ERROR" for item in results),
            "marked_pair_count": sum(item["marked_pair_count"] for item in constructed),
            "marked_pair_orbit_count": sum(item["marked_pair_orbit_count"] for item in constructed),
            "generating_orbit_count": sum(item["generating_orbit_count"] for item in constructed),
            "complement_orbit_count": sum(item["complement_orbit_count"] for item in constructed),
        },
        "outcomes_opened": {"shadow": 0, "reduction": 0, "element_survival": 0},
        "positive_control": {
            "each_constructed_group": "order 504*2^d and elementary kernel order 2^d",
            "passed": all(
                item["group_order"] == 504 * item["module_order"]
                and item["module_element_order_distribution"] == {
                    "1": 1,
                    "2": item["module_order"] - 1,
                }
                for item in constructed
            ),
        },
        "noncontact": {
            "u": False,
            "c": False,
            "sealed_three_quantities": False,
            "sealed_K5": False,
        },
    }
    atomic_json(output, cert)
    state.update(stage="complete", complete=True, output_sha256=sha_file(output))
    atomic_json(checkpoint, state)
    print(json.dumps(cert["aggregate"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
