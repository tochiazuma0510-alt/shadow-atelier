#!/usr/bin/env python3
"""Corrected-parser preflight for PerfectGroups family [16,10,1]."""

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

from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.free_groups import free_group

import campaign138_higher_perfect_preflight_v1 as base


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / (
    "GAP-4.16.0/runtime/opt/gap-4.16.0/grp/perf10.grp"
)
LABEL = "L2(8) N ( 2^6 E ( 2^1 x 2^1 x 2^1 A ) ) C 2^1"
PREREG = ROOT / "search/certs/campaign138_d10_preflight_prereg_v1_20260815.json"


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def matching_square(text: str, start: int) -> int:
    if text[start] != "[":
        raise ValueError("list start")
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "[":
            depth += 1
        elif text[index] == "]":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unterminated list")


def parse() -> dict:
    library = LIBRARY.read_text(encoding="utf-8", errors="replace")
    label_at = library.index(f'"{LABEL}"')
    start = library.rfind("# 516096.", 0, label_at)
    finish = library.find("PERFGRP[", label_at)
    segment = library[start:finish]
    uncommented = re.sub(r"#[^\r\n]*", "", segment)
    compact = re.sub(r"\s+", "", uncommented)
    names = re.search(r'\[\[1,"([a-z]+)"', compact).group(1)
    expression_start = compact.index("return") + len("return")
    expression_end = matching_square(compact, expression_start)
    outer = base.list_items(compact[expression_start : expression_end + 1])
    free_data = free_group(",".join(names))
    namespace = dict(zip(names, free_data[1:]))

    def translate(expression: str):
        return eval(expression.replace("^", "**"), {"__builtins__": {}}, namespace)

    return {
        "names": names,
        "free": free_data[0],
        "generators": tuple(free_data[1:]),
        "relations": [translate(item) for item in base.list_items(outer[0])],
        "subgroup_lists": [
            [translate(item) for item in base.list_items(subgroup)]
            for subgroup in base.list_items(outer[1])
        ],
        "segment_sha256": hashlib.sha256(segment.encode()).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", default="search/certs/campaign138_d10_preflight_v1_20260815.json"
    )
    parser.add_argument(
        "--checkpoint", default="search/certs/campaign138_d10_preflight_v1_checkpoint.json"
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=240)
    args = parser.parse_args()
    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    began = time.monotonic()
    state = {
        "schema": "campaign138_d10_preflight_checkpoint/v1",
        "stage": "start",
        "complete": False,
        "preregistration_sha256": sha_file(PREREG),
    }
    atomic_json(checkpoint, state)

    def update(stage: str, **extra: object) -> None:
        state.update(stage=stage, elapsed_ms=int(1000 * (time.monotonic() - began)), **extra)
        atomic_json(checkpoint, state)

    def timeout() -> None:
        if not state["complete"]:
            update("hard_timeout", hard_timeout_seconds=args.hard_timeout_seconds)
            os._exit(124)

    alarm = threading.Timer(args.hard_timeout_seconds, timeout)
    alarm.daemon = True
    alarm.start()
    try:
        record = parse()
        update("parsed", generator_names=record["names"])
        action, block_sizes = base.permutation_action(record)
        update("action", block_sizes=block_sizes)
        named = dict(zip(record["names"], action))
        module = base.closure(tuple(named[name] for name in record["names"][3:]))
        group_size = base.group_order(action)
        s = base.positive_word("accbxbccb", named)
        t = base.positive_word("cacaccwb", named)
        lifts_s = sorted({
            base.product(value, s)
            for value in module
            if base.order(base.product(value, s)) == 2
        })
        lifts_t = sorted({
            base.product(value, t)
            for value in module
            if base.order(base.product(value, t)) == 3
        })
        remaining = {(left, right) for left in lifts_s for right in lifts_t}
        pair_count = len(remaining)
        orbits = []
        while remaining:
            seed = min(remaining)
            orbit = {
                (
                    base.conjugate(seed[0], value),
                    base.conjugate(seed[1], value),
                )
                for value in module
            } & remaining
            representative = min(orbit)
            generated_order = base.group_order(representative)
            orbits.append({
                "orbit_size": len(orbit),
                "generated_order": generated_order,
                "generates_full_group": generated_order == group_size,
                "is_complement": generated_order == 504,
                "S_sha256": base.sha_obj(list(representative[0])),
                "T_sha256": base.sha_obj(list(representative[1])),
                "S": list(representative[0]),
                "T": list(representative[1]),
            })
            remaining -= orbit
        orbits.sort(key=lambda item: (item["S"], item["T"]))
        for index, item in enumerate(orbits):
            item["orbit_index"] = index
        cert = {
            "schema": "campaign138_d10_preflight/v1",
            "status": "PREFLIGHT_ONLY",
            "producer_sha256": sha_file(Path(__file__)),
            "preregistration_sha256": sha_file(PREREG),
            "library_sha256": sha_file(LIBRARY),
            "segment_sha256": record["segment_sha256"],
            "candidate": {
                "family_key": [16, 10, 1],
                "label": LABEL,
                "generator_names": record["names"],
                "block_sizes": block_sizes,
                "coset_degree": sum(block_sizes),
                "group_order": group_size,
                "kernel_order": len(module),
                "kernel_element_order_distribution": {
                    str(key): value
                    for key, value in sorted(Counter(base.order(item) for item in module).items())
                },
                "base_lift_orders": [base.order(s), base.order(t)],
                "order2_lift_count": len(lifts_s),
                "order3_lift_count": len(lifts_t),
                "marked_pair_count": pair_count,
                "marked_pair_orbit_count": len(orbits),
                "generating_orbit_count": sum(item["generates_full_group"] for item in orbits),
                "complement_orbit_count": sum(item["is_complement"] for item in orbits),
                "marked_pair_orbits": orbits,
            },
            "positive_control": {
                "expected_group_order": 516096,
                "expected_kernel_order": 1024,
                "passed": group_size == 516096 and len(module) == 1024,
            },
            "outcomes_opened": {"shadow": 0, "reduction": 0, "element_survival": 0},
            "noncontact": {
                "u": False,
                "c": False,
                "sealed_three_quantities": False,
                "sealed_K5": False,
            },
        }
        atomic_json(output, cert)
        state["complete"] = True
        update("complete", output_sha256=sha_file(output))
        print(json.dumps({
            "order2_lift_count": len(lifts_s),
            "order3_lift_count": len(lifts_t),
            "marked_pair_orbit_count": len(orbits),
            "generating_orbit_count": cert["candidate"]["generating_orbit_count"],
        }, sort_keys=True))
        return 0
    finally:
        alarm.cancel()


if __name__ == "__main__":
    raise SystemExit(main())
