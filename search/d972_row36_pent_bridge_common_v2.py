#!/usr/bin/env python3
"""Versioned GHA portability layer for row36 bridge producer v1 primitives.

The v1 source and its first preregistration are immutable.  V2 changes only
execution routing and replaces an unnecessarily huge joint automorphism replay
by complete, helper-local replays on the three finite projection factors.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path
from typing import Any, Callable, Sequence, TypeVar

import d972_row36_pent_bridge_common_v1 as base


T = TypeVar("T")
VERSION = 2
_ORIGINAL_BUILD_RAW = base.build_raw_universe
_ORIGINAL_EXECUTE = base.execute
_ORIGINAL_BUILD_MANIFEST = base.build_manifest


def finite_marked_map(identity: T, source_marks: Sequence[T], target_marks: Sequence[T],
                      mul: Callable[[T, T], T], inv: Callable[[T], T],
                      expected_order: int, label: str) -> dict[T, T]:
    source_steps = (source_marks[0], inv(source_marks[0]),
                    source_marks[1], inv(source_marks[1]))
    target_steps = (target_marks[0], inv(target_marks[0]),
                    target_marks[1], inv(target_marks[1]))
    mapping = {identity: identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for source_step, target_step in zip(source_steps, target_steps):
            nxt = mul(current, source_step)
            image = mul(mapping[current], target_step)
            if nxt in mapping:
                base.require(mapping[nxt] == image, "FACTOR_AUTOMORPHISM_DESCENT", label)
            else:
                mapping[nxt] = image
                queue.append(nxt)
    base.require(len(mapping) == expected_order, "FACTOR_AUTOMORPHISM_SOURCE_COVER",
                 repr((label, len(mapping), expected_order)))
    base.require(len(set(mapping.values())) == expected_order,
                 "FACTOR_AUTOMORPHISM_BIJECTIVITY", label)
    return mapping


def validate_automorphism_descent_v2(prime: int, qcol: base.PcCollector,
                                     qmarks: Sequence[bytes]) -> dict[str, Any]:
    expected_q = 128 if prime == 2 else 2187
    transforms = ((base.theta_word, "theta"), (base.tau_word, "tau"))
    factor_rows = []
    for transform, name in transforms:
        tx = transform((1,))
        ty = transform((2,))
        target_g = (base.eval_word_g(tx, 36), base.eval_word_g(ty, 36))
        target_p = (base.eval_word_perm(tx), base.eval_word_perm(ty))
        target_q = (qcol.eval(tx, qmarks), qcol.eval(ty, qmarks))
        gmap = finite_marked_map(base.gid(), (base.gx(36), base.gy(36)), target_g,
                                 lambda a, b: base.gmul(a, b, 36),
                                 lambda a: base.ginv(a, 36), 23328, f"G36/{name}")
        pmap = finite_marked_map(base.PSL_ID, (base.X_PSL, base.Y_PSL), target_p,
                                 base.pmul, base.pinv, 504, f"PSL2_8/{name}")
        qmap = finite_marked_map(qcol.one(), qmarks, target_q,
                                 qcol.mul, qcol.inverse, expected_q, f"Qp/{name}")
        factor_rows.append({"automorphism": name,
                            "G36_source_and_image_order": len(gmap),
                            "PSL2_8_source_and_image_order": len(pmap),
                            "Qp_source_and_image_order": len(qmap)})
    return {"theta": "x->y,y->x", "tau_native": "x->y,y->x^-1*y^-1",
            "factor_complete_descent_and_bijection": factor_rows,
            "joint_descent_reason": "the marked joint image is generated diagonally; componentwise descended maps preserve that image"}


def install(prime: int, out_dir: str | None) -> None:
    def source_pins(_: int) -> list[dict[str, Any]]:
        return [
            base.file_pin("search/d972_row36_pent_bridge_common_v1.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v2.py"),
            base.file_pin(f"search/d972_row36_pent_bridge_p{prime}_producer_v2.py"),
        ]

    def paths_for(_: int) -> dict[str, str]:
        prefix = Path(out_dir).as_posix().rstrip("/") if out_dir else "search/certs"
        return {
            "prereg": f"search/certs/d972_row36_pent_bridge_p{prime}_prereg_v2_{base.DATE}.json",
            "receipt": f"{prefix}/d972_row36_pent_bridge_p{prime}_receipt_v2_{base.DATE}.json",
            "manifest": f"{prefix}/d972_row36_pent_bridge_p{prime}_manifest_v2_{base.DATE}.json",
        }

    def build_raw(prime_arg: int, receipt: dict[str, Any]):
        prereg, runtime = _ORIGINAL_BUILD_RAW(prime_arg, receipt)
        prereg["schema"] = f"d972-row36-pent-bridge-p{prime_arg}-prereg/v2"
        prereg["source_pins"] = source_pins(prime_arg)
        prereg["execution_routing"] = {
            "local_v1_prepare_observations": [
                {"timeout_seconds": 120, "last_marker": "COLLECTORS_START",
                 "classification": "generic rank-26 token-collector resource trap; no prereg emitted"},
                {"timeout_seconds": 180, "last_marker": "COLLECTORS_PASS",
                 "classification": "generic rank-26 A.18 replay resource trap; no prereg emitted"},
            ],
            "v2_prepare_rule": "bind immutable canary-exported A.18 10/10 gate; do not rerun quotient canary",
            "v2_execute_rule": "evaluate every row's same signed word directly in exported Q4 pc collector using preauthenticated positive/inverse marked coordinates",
            "GHA_required": True,
        }
        prereg["status"] = "PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME__GHA_ROUTE"
        prereg["terminal_token"] = f"PENT159O_ROW36_P{prime_arg}_PREREG_V2_FROZEN"
        return prereg, runtime

    def execute(prime_arg: int, prereg_pin: dict[str, Any], prereg: dict[str, Any],
                runtime: dict[str, Any], input_pins: list[dict[str, Any]]):
        receipt, extra = _ORIGINAL_EXECUTE(prime_arg, prereg_pin, prereg, runtime, input_pins)
        receipt["schema"] = f"d972-row36-pent-bridge-p{prime_arg}-receipt/v2"
        receipt["source_pins"] = source_pins(prime_arg)
        receipt["execution_routing"] = prereg["execution_routing"]
        receipt["terminal_token"] = f"PENT159O_ROW36_P{prime_arg}_PRODUCER_V2_CANDIDATE__CHECKER_REQUIRED"
        return receipt, extra

    def build_manifest(prime_arg: int, prereg_pin: dict[str, Any], receipt_pin: dict[str, Any]):
        manifest = _ORIGINAL_BUILD_MANIFEST(prime_arg, prereg_pin, receipt_pin)
        manifest["schema"] = f"d972-row36-pent-bridge-p{prime_arg}-manifest/v2"
        manifest["source_pins"] = source_pins(prime_arg)
        manifest["execution"]["local_command_prepare"] = f"python search/d972_row36_pent_bridge_p{prime_arg}_producer_v2.py prepare"
        manifest["execution"]["GHA_command"] = f"python3 search/d972_row36_pent_bridge_p{prime_arg}_producer_v2.py execute --out-dir ci/out"
        manifest["terminal_token"] = f"PENT159O_ROW36_P{prime_arg}_MANIFEST_V2_FROZEN"
        return manifest

    base.source_pins = source_pins
    base.paths_for = paths_for
    base.build_raw_universe = build_raw
    base.execute = execute
    base.build_manifest = build_manifest
    base.validate_automorphism_descent = validate_automorphism_descent_v2


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

