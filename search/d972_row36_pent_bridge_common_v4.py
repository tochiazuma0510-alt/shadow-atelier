#!/usr/bin/env python3
"""P3-only inverse-table portability layer for row36 bridge v3.

The p=3 exported collector can make dense generic inverse expansion exceed the
token rewrite cap.  V4 constructs all 2,187 inverses by a complete marked BFS
using the independently exported x^-1,y^-1 coordinates and positive pc products.
"""

from __future__ import annotations

import argparse
import math
from collections import deque
from pathlib import Path
from typing import Any, Sequence

import d972_row36_pent_bridge_common_v1 as base
import d972_row36_pent_bridge_common_v3 as v3


def install_marked_inverse_table(qcol: base.PcCollector, qmarks: Sequence[bytes],
                                 qinverse_marks: Sequence[bytes],
                                 expected_order: int) -> dict[str, Any]:
    steps = (qmarks[0], qinverse_marks[0], qmarks[1], qinverse_marks[1])
    inverse_steps = (qinverse_marks[0], qmarks[0], qinverse_marks[1], qmarks[1])
    identity = qcol.one()
    inverse_table = {identity: identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for step, inverse_step in zip(steps, inverse_steps):
            nxt = qcol.mul(current, step)
            inverse_nxt = qcol.mul(inverse_step, inverse_table[current])
            if nxt in inverse_table:
                base.require(inverse_table[nxt] == inverse_nxt,
                             "MARKED_INVERSE_BFS_CONSISTENCY", repr(nxt))
            else:
                inverse_table[nxt] = inverse_nxt
                queue.append(nxt)
    base.require(len(inverse_table) == expected_order,
                 "MARKED_INVERSE_BFS_COVER", repr((len(inverse_table), expected_order)))
    for value, inverse in inverse_table.items():
        base.require(qcol.mul(value, inverse) == identity and
                     qcol.mul(inverse, value) == identity,
                     "MARKED_INVERSE_TWO_SIDED_REPLAY", repr(value))

    def inverse_lookup(value: bytes) -> bytes:
        base.require(value in inverse_table, "MARKED_INVERSE_LOOKUP_MISSING", repr(value))
        return inverse_table[value]

    qcol.inverse = inverse_lookup  # type: ignore[method-assign]
    return {"algorithm": "complete right-Cayley BFS with steps x,x^-1,y,y^-1; inv(q*s)=inv(s)*inv(q)",
            "source": "exported marked coords and exported inverse-mark coords",
            "entry_count": len(inverse_table),
            "all_two_sided_products_identity": True,
            "generic_dense_inverse_expansion_used_after_install": False}


def validate_pc_receipt_v4(prime: int, q2: dict[str, Any], q4: dict[str, Any],
                           qcol: base.PcCollector, q4col: base.PcCollector):
    base.require(prime == 3, "V4_PRIME_LOCAL", str(prime))
    expected_order = 2187
    base.require(math.prod(qcol.orders) == expected_order and
                 int(q2["order_decimal"]) == expected_order and
                 q2["nilpotency_class"] == 3, "Q2_COLLECTOR_ORDER_CLASS")
    base.require(math.prod(q4col.orders) == int(q4["order_decimal"]) and
                 q4["nilpotency_class"] == 3, "Q4_COLLECTOR_ORDER_CLASS")
    qmarks = tuple(qcol.coord(row["coords"]) for row in q2["marked_generators"])
    qinverse_marks = tuple(qcol.coord(row["inverse_coords"])
                           for row in q2["marked_generators"])
    q4marks = tuple(q4col.coord(row["coords"]) for row in q4["marked_generators"])
    base.require(len(qmarks) == len(qinverse_marks) == 2 and len(q4marks) == 6,
                 "MARK_COUNTS")
    gate = install_marked_inverse_table(qcol, qmarks, qinverse_marks, expected_order)
    setattr(qcol, "marked_inverse_table_gate", gate)
    coarse, _ = base.marked_bfs_map(
        qcol, qmarks, 0, (1, 1), lambda a, b: (a + b) % 3,
        lambda a: (-a) % 3, expected_order)
    base.require(len(coarse) == expected_order, "Q3_MARKED_COVER")
    return qmarks, q4marks


def install(prime: int, out_dir: str | None) -> None:
    base.require(prime == 3, "V4_PRIME_LOCAL", str(prime))
    v3.install(prime, out_dir)
    build_raw_v3 = base.build_raw_universe
    execute_v3 = base.execute
    build_manifest_v3 = base.build_manifest
    base.validate_pc_receipt = validate_pc_receipt_v4

    def source_pins(_: int) -> list[dict[str, Any]]:
        return [
            base.file_pin("search/d972_row36_pent_bridge_common_v1.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v2.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v3.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v4.py"),
            base.file_pin("search/d972_row36_pent_bridge_p3_producer_v4.py"),
        ]

    def paths_for(_: int) -> dict[str, str]:
        prefix = Path(out_dir).as_posix().rstrip("/") if out_dir else "search/certs"
        return {
            "prereg": f"search/certs/d972_row36_pent_bridge_p3_prereg_v4_{base.DATE}.json",
            "receipt": f"{prefix}/d972_row36_pent_bridge_p3_receipt_v4_{base.DATE}.json",
            "manifest": f"{prefix}/d972_row36_pent_bridge_p3_manifest_v4_{base.DATE}.json",
        }

    def build_raw(prime_arg: int, receipt: dict[str, Any]):
        prereg, runtime = build_raw_v3(prime_arg, receipt)
        prereg["schema"] = "d972-row36-pent-bridge-p3-prereg/v4"
        prereg["source_pins"] = source_pins(prime_arg)
        prereg["execution_routing"]["p3_v3_prepare_stop"] = {
            "elapsed_seconds": 16.6,
            "exact_stop": "PC_COLLECTION_CAP: (25, 7)",
            "phase": "Q3 marked inverse expansion before Hall/L/Schreier",
            "classification": "implementation resource trap; no prereg or outcome emitted",
        }
        prereg["execution_routing"]["p3_v4_inverse_repair"] = \
            runtime["qcol"].marked_inverse_table_gate
        prereg["status"] = "PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME"
        prereg["terminal_token"] = "PENT159O_ROW36_P3_PREREG_V4_FROZEN"
        return prereg, runtime

    def execute(prime_arg: int, prereg_pin: dict[str, Any], prereg: dict[str, Any],
                runtime: dict[str, Any], input_pins: list[dict[str, Any]]):
        receipt, extra = execute_v3(prime_arg, prereg_pin, prereg, runtime, input_pins)
        receipt["schema"] = "d972-row36-pent-bridge-p3-receipt/v4"
        receipt["source_pins"] = source_pins(prime_arg)
        receipt["Q3_marked_inverse_table_gate"] = runtime["qcol"].marked_inverse_table_gate
        receipt["terminal_token"] = \
            "PENT159O_ROW36_P3_PRODUCER_V4_CANDIDATE__CHECKER_REQUIRED"
        return receipt, extra

    def build_manifest(prime_arg: int, prereg_pin: dict[str, Any], receipt_pin: dict[str, Any]):
        manifest = build_manifest_v3(prime_arg, prereg_pin, receipt_pin)
        manifest["schema"] = "d972-row36-pent-bridge-p3-manifest/v4"
        manifest["source_pins"] = source_pins(prime_arg)
        manifest["execution"]["local_command_prepare"] = \
            "python search/d972_row36_pent_bridge_p3_producer_v4.py prepare"
        manifest["execution"]["GHA_command"] = \
            "python3 search/d972_row36_pent_bridge_p3_producer_v4.py execute --out-dir ci/out"
        manifest["terminal_token"] = "PENT159O_ROW36_P3_MANIFEST_V4_FROZEN"
        return manifest

    base.source_pins = source_pins
    base.paths_for = paths_for
    base.build_raw_universe = build_raw
    base.execute = execute
    base.build_manifest = build_manifest


def main_for_prime(prime: int) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare", "execute"))
    parser.add_argument("--out-dir")
    args = parser.parse_args()
    if args.phase == "prepare":
        base.require(args.out_dir is None, "PREPARE_OUT_DIR_FORBIDDEN")
    else:
        base.require(args.out_dir is not None, "EXECUTE_OUT_DIR_REQUIRED")
        rel = Path(args.out_dir)
        base.require(not rel.is_absolute() and ".." not in rel.parts,
                     "EXECUTE_OUT_DIR_UNSAFE", args.out_dir)
    install(prime, args.out_dir)
    raise SystemExit(base.run(prime, [args.phase]))

