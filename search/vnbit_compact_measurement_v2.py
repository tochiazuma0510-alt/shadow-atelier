#!/usr/bin/env python3
"""Task 131 producer: fail-closed marked-action gate for compact route v2.

The 324-row measurement is downstream of a marked representation of
``B3/<c> = C2 * C3`` extending the frozen pure action.  This program checks
that compatibility before classifying marked lifts or opening the blind
measurement.  It writes only a pre-measurement certificate when the anchor
does not agree.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
P = 3
DIM = 21


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def value_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def matrix(value: object) -> np.ndarray:
    return np.asarray(value, dtype=np.int64) % P


def mm(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return (left @ right) % P


def matrix_power(value: np.ndarray, exponent: int) -> np.ndarray:
    result = np.eye(value.shape[0], dtype=np.int64)
    factor = value.copy()
    while exponent:
        if exponent & 1:
            result = mm(result, factor)
        factor = mm(factor, factor)
        exponent >>= 1
    return result


def rank_mod3(value: np.ndarray) -> int:
    work = value.copy() % P
    pivot_row = 0
    for column in range(work.shape[1]):
        choices = np.flatnonzero(work[pivot_row:, column])
        if not len(choices):
            continue
        choice = pivot_row + int(choices[0])
        work[[pivot_row, choice]] = work[[choice, pivot_row]]
        if work[pivot_row, column] == 2:
            work[pivot_row] = (2 * work[pivot_row]) % P
        for row in range(work.shape[0]):
            if row != pivot_row and work[row, column]:
                work[row] = (
                    work[row] - work[row, column] * work[pivot_row]
                ) % P
        pivot_row += 1
        if pivot_row == work.shape[0]:
            break
    return pivot_row


def equal(left: np.ndarray, right: np.ndarray) -> bool:
    return bool(np.array_equal(left % P, right % P))


def monomial(destinations: tuple[int, int, int], scalars: tuple[int, int, int]) -> np.ndarray:
    result = np.zeros((3, 3), dtype=np.int64)
    for source, target in enumerate(destinations):
        result[target, source] = scalars[source]
    return result


def scalar_repairs() -> list[dict[str, list[int]]]:
    """Enumerate the unfrozen scalar factors missing from block transport."""
    theta_destinations = (1, 0, 2)
    tau_destinations = (2, 0, 1)
    target_x = np.diag((2, 1, 2))
    target_y = np.diag((1, 2, 2))
    identity = np.eye(3, dtype=np.int64)
    answers: list[dict[str, list[int]]] = []
    for theta_scalars in itertools.product((1, 2), repeat=3):
        theta = monomial(theta_destinations, theta_scalars)
        for tau_scalars in itertools.product((1, 2), repeat=3):
            tau = monomial(tau_destinations, tau_scalars)
            tau_inverse = mm(tau, tau)
            sigma_1 = mm(tau_inverse, theta)
            sigma_2 = mm(theta, tau_inverse)
            if not equal(mm(theta, theta), identity):
                continue
            if not equal(mm(mm(tau, tau), tau), identity):
                continue
            if not equal(mm(sigma_1, sigma_1), target_x):
                continue
            if not equal(mm(sigma_2, sigma_2), target_y):
                continue
            answers.append(
                {
                    "theta_source_scalars": list(theta_scalars),
                    "tau_source_scalars": list(tau_scalars),
                }
            )
    return answers


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="search/certs/vnbit_affine_gate_raw_v1_20260813.json",
    )
    parser.add_argument(
        "--output",
        default="search/certs/vnbit_compact_measurement_raw_v2_20260813.json",
    )
    parser.add_argument(
        "--checkpoint",
        default="search/certs/vnbit_compact_measurement_v2_checkpoint.json",
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=120)
    args = parser.parse_args()

    input_path = ROOT / args.input
    output_path = ROOT / args.output
    checkpoint_path = ROOT / args.checkpoint
    started = time.monotonic()
    checkpoint: dict[str, object] = {
        "schema": "vnbit_compact_measurement_checkpoint/v2",
        "stage": "start",
        "complete": False,
    }
    atomic_json(checkpoint_path, checkpoint)

    def update(stage: str, **fields: object) -> None:
        checkpoint.update(
            stage=stage,
            elapsed_ms=int(1000 * (time.monotonic() - started)),
            **fields,
        )
        atomic_json(checkpoint_path, checkpoint)

    def timeout() -> None:
        if not checkpoint.get("complete"):
            update("hard_timeout")
            os._exit(124)

    alarm = threading.Timer(args.hard_timeout_seconds, timeout)
    alarm.daemon = True
    alarm.start()
    try:
        raw = json.loads(input_path.read_text(encoding="utf-8"))
        c2 = raw["C2"]
        rho_x = matrix(c2["rho_X"])
        rho_y = matrix(c2["rho_Y"])
        theta = matrix(c2["theta_operator"])
        tau = matrix(c2["tau_operator"])
        identity = np.eye(DIM, dtype=np.int64)
        update("inputs_loaded")

        # BU-S35 section 43/61, in the repository's paper/left-action order:
        # sigma_1 = delta^-1 Delta and sigma_2 = Delta^-1 delta^2.
        tau_inverse = matrix_power(tau, 2)
        sigma_1 = mm(tau_inverse, theta)
        sigma_2 = mm(theta, tau_inverse)
        marked_x = mm(sigma_1, sigma_1)
        marked_y = mm(sigma_2, sigma_2)
        reconstructed_delta = mm(sigma_1, sigma_2)
        reconstructed_Delta = mm(mm(sigma_1, sigma_2), sigma_1)
        braid_left = mm(mm(sigma_1, sigma_2), sigma_1)
        braid_right = mm(mm(sigma_2, sigma_1), sigma_2)

        anchor_x = equal(marked_x, rho_x)
        anchor_y = equal(marked_y, rho_y)
        marking_gate = {
            "presentation": "B3 = <Delta,delta | Delta^2=delta^3>",
            "word_convention": "paper left action; matrices multiply in paper order",
            "sigma_1_formula": "delta^-1 Delta",
            "sigma_2_formula": "Delta^-1 delta^2",
            "theta_order_two": equal(mm(theta, theta), identity),
            "tau_order_three": equal(mm(mm(tau, tau), tau), identity),
            "Delta_reconstructed": equal(reconstructed_Delta, theta),
            "delta_reconstructed": equal(reconstructed_delta, tau),
            "braid_relation": equal(braid_left, braid_right),
            "center_in_linear_kernel": equal(mm(theta, theta), identity)
            and equal(mm(mm(tau, tau), tau), identity),
            "sigma_1_squared_matches_frozen_rho_X": anchor_x,
            "sigma_2_squared_matches_frozen_rho_Y": anchor_y,
            "marked_projection_matches_frozen_C2_W_action": anchor_x and anchor_y,
            "rank_difference_x": rank_mod3((marked_x - rho_x) % P),
            "rank_difference_y": rank_mod3((marked_y - rho_y) % P),
            "marked_x_sha256": value_sha256(marked_x.tolist()),
            "frozen_rho_X_sha256": value_sha256(rho_x.tolist()),
            "marked_y_sha256": value_sha256(marked_y.tolist()),
            "frozen_rho_Y_sha256": value_sha256(rho_y.tolist()),
            "difference_x_sha256": value_sha256(((marked_x - rho_x) % P).tolist()),
            "difference_y_sha256": value_sha256(((marked_y - rho_y) % P).tolist()),
        }
        update(
            "marked_action_compared",
            marked_projection_matches=marking_gate[
                "marked_projection_matches_frozen_C2_W_action"
            ],
        )

        repairs = scalar_repairs()
        # The lexicographically first repair leaves theta unchanged and changes
        # tau by source-block signs (1,2,2).  It is diagnostic only: v2 did not
        # freeze this factor, and no repair is used below.
        diagnostic = {
            "zero_scalar_transport_used_by_task130": {
                "theta_source_scalars": [1, 1, 1],
                "tau_source_scalars": [1, 1, 1],
            },
            "repair_candidate_count": len(repairs),
            "repair_candidates": repairs,
            "lexicographically_first_candidate": repairs[0] if repairs else None,
            "candidate_status": "not_frozen_and_not_used",
            "reason_not_used": (
                "Choosing a scalar factor changes the marked linear action and is "
                "an input repair outside compact-route v2. Gauge/kernel equivalence "
                "of the listed choices is not supplied by the specification."
            ),
        }

        source_paths = (
            "ops/inbox_codex/sol_task_131_measurement.txt",
            "docs/notes/vnbit_compact_route_v2.md",
            "docs/notes/bu_s35_embedding_v1.md",
            "docs/week1-定義ノート.md",
            args.input,
        )
        source_hashes = {
            name: file_sha256(ROOT / name) for name in source_paths
        }

        result = {
            "schema": "vnbit_compact/v2_premeasurement_stop",
            "run_id": "vnbit-compact-measurement-"
            + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "generated_by": {
                "script": "search/vnbit_compact_measurement_v2.py",
                "script_sha256": file_sha256(Path(__file__)),
                "runtime": f"Python {os.sys.version.split()[0]} + NumPy {np.__version__}",
            },
            "source_sha256": source_hashes,
            "marking": marking_gate,
            "diagnostic_unfrozen_scalar_factor": diagnostic,
            "stage_boundary": {
                "stage": "stopped_before_SURJ_LIN",
                "reason": "marked_pure_anchor_mismatch",
                "SURJ_LIN_classification_computed": False,
                "preregistration_created": False,
                "target_rows_formed": 0,
                "surjective_classes_measured": 0,
                "lift_table_rows": 0,
                "obstruction_classes_measured": 0,
                "generating_solution_exists_measured": 0,
                "per_class_distribution": None,
                "per_t2_distribution": None,
                "Im_R_K_M_size": None,
            },
            "A_shape": {
                "rows": 42,
                "cols": 21,
                "rank_A1": None,
                "rank_A2": None,
                "rank_A1_equals_rank_A2": None,
                "note": "No row was expanded because the marked-action input stopped first.",
            },
            "isolated": {
                "N_E_isolated": "UNKNOWN",
                "gate_policy": "measure anyway only after a well-typed marked action (C-4-prime)",
                "vNB_GAP_1": "open",
            },
            "endgame_scope": (
                "gentle side only. Elevation of a B-branch countercandidate requires "
                "the B4 layer PENT_W-PASS and then FAKE-KILL^{B4}/U-10. No finite-"
                "depth B-type identification is made here."
            ),
            "noncontact": {
                "u": False,
                "c": False,
                "sealed_three_quantities": False,
                "sealed_K5": False,
                "blind_324_outcomes": False,
            },
            "status_note": (
                "Raw machine values only. The frozen pure action and the v2 marked "
                "linear operators do not define one representation of the specified "
                "B3 quotient; downstream rows would measure a different module."
            ),
        }
        atomic_json(output_path, result)
        update(
            "complete_premeasurement_stop",
            complete=True,
            output_sha256=file_sha256(output_path),
        )
        return 0
    finally:
        alarm.cancel()


if __name__ == "__main__":
    raise SystemExit(main())
