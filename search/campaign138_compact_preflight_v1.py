#!/usr/bin/env python3
"""Campaign 138: prospective compact/nonsemisimple rank preflight.

No class-lift or element-survival outcome is evaluated here.  A candidate is
passed to a later outcome stage only if some frozen roof row has positive
obstruction rank.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import os
import sys
import threading
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
import escape2_producer_v1 as p2
import escape28_mainrun_v1 as p3

old = p2.old
aff = p2.aff


def set_field(prime: int) -> None:
    old.F = prime
    aff.F = prime


def eye(n: int) -> np.ndarray:
    return np.eye(n, dtype=np.int64)


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha_obj(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def counter_json(counter: collections.Counter) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(counter.items())}


def all_gl2(prime: int) -> list[np.ndarray]:
    set_field(prime)
    answer = []
    for values in itertools.product(range(prime), repeat=4):
        matrix = np.asarray(values, dtype=np.int64).reshape(2, 2)
        if old.rank(matrix) == 2:
            answer.append(matrix)
    return answer


def duplicate_blocks(matrix: np.ndarray, block_size: int, block_count: int) -> np.ndarray:
    """Duplicate each block, ordered block-major then multiplicity-major."""
    dimension = 2 * block_size * block_count
    answer = np.zeros((dimension, dimension), dtype=np.int64)
    for target_block in range(block_count):
        for source_block in range(block_count):
            piece = matrix[
                block_size * target_block : block_size * (target_block + 1),
                block_size * source_block : block_size * (source_block + 1),
            ]
            for multiplicity in range(2):
                target = 2 * block_size * target_block + block_size * multiplicity
                source = 2 * block_size * source_block + block_size * multiplicity
                answer[target : target + block_size, source : source + block_size] = piece
    return answer % old.F


def p2_centralizer(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    block_size = 4
    answer = np.zeros((24, 24), dtype=np.int64)
    for block, matrix in enumerate(matrices):
        for target in range(2):
            for source in range(2):
                if int(matrix[target, source]):
                    row = 8 * block + 4 * target
                    column = 8 * block + 4 * source
                    answer[row : row + 4, column : column + 4] = eye(block_size)
    return answer % 2


def p3_centralizer(matrix: np.ndarray) -> np.ndarray:
    unit = eye(7)
    return np.block(
        [
            [matrix[0, 0] * unit, matrix[0, 1] * unit],
            [matrix[1, 0] * unit, matrix[1, 1] * unit],
        ]
    ) % 3


def anchor_census(
    prime: int,
    theta_base: np.ndarray,
    tau_base: np.ndarray,
    centralizers: list[np.ndarray],
) -> tuple[list[dict], np.ndarray, np.ndarray]:
    set_field(prime)
    sigma_1 = old.mm(old.mpow(tau_base, -1), theta_base)
    sigma_2 = old.mm(old.mpow(theta_base, -1), old.mpow(tau_base, 2))
    rho_x = old.mpow(sigma_1, 2)
    rho_y = old.mpow(sigma_2, 2)
    identity = eye(theta_base.shape[0])
    valid: dict[tuple[int, int], tuple[np.ndarray, np.ndarray]] = {}
    for theta_index, theta_twist in enumerate(centralizers):
        theta = old.mm(theta_base, theta_twist)
        if not np.array_equal(old.mpow(theta, 2), identity):
            continue
        for tau_index, tau_twist in enumerate(centralizers):
            tau = old.mm(tau_base, tau_twist)
            if not np.array_equal(old.mpow(tau, 3), identity):
                continue
            sigma_1_new = old.mm(old.mpow(tau, -1), theta)
            sigma_2_new = old.mm(old.mpow(theta, -1), old.mpow(tau, 2))
            if np.array_equal(old.mpow(sigma_1_new, 2), rho_x) and np.array_equal(
                old.mpow(sigma_2_new, 2), rho_y
            ):
                valid[(theta_index, tau_index)] = (theta, tau)

    lookup = {matrix.tobytes(): index for index, matrix in enumerate(centralizers)}
    unseen = set(valid)
    orbits = []
    while unseen:
        seed = min(unseen)
        theta, tau = valid[seed]
        orbit = set()
        for gauge in centralizers:
            inverse = old.mpow(gauge, -1)
            theta_g = old.mm(old.mm(inverse, theta), gauge)
            tau_g = old.mm(old.mm(inverse, tau), gauge)
            a = old.mm(old.mpow(theta_base, -1), theta_g)
            b = old.mm(old.mpow(tau_base, -1), tau_g)
            key = (lookup[a.tobytes()], lookup[b.tobytes()])
            if key in valid:
                orbit.add(key)
        if not orbit:
            raise RuntimeError("empty gauge orbit")
        representative = min(orbit)
        rep_theta, rep_tau = valid[representative]
        orbits.append(
            {
                "representative": representative,
                "orbit": sorted(orbit),
                "theta": rep_theta,
                "tau": rep_tau,
            }
        )
        unseen -= orbit
    orbits.sort(key=lambda entry: entry["representative"])
    if sum(len(entry["orbit"]) for entry in orbits) != len(valid):
        raise RuntimeError("gauge orbit partition mismatch")
    return orbits, rho_x, rho_y


def matrix_group_order(generators: tuple[np.ndarray, ...]) -> int:
    identity = eye(generators[0].shape[0])
    seen = {identity.tobytes()}
    queue = [identity]
    for value in queue:
        for generator in generators:
            new = old.mm(value, generator)
            key = new.tobytes()
            if key not in seen:
                seen.add(key)
                queue.append(new)
    return len(queue)


def cyclic_h2(prime: int, theta: np.ndarray, tau: np.ndarray) -> dict:
    set_field(prime)
    operator = theta if prime == 2 else tau
    identity = eye(operator.shape[0])
    norm = (identity + operator) % prime
    if prime == 3:
        norm = (norm + old.mm(operator, operator)) % prime
    fixed = operator.shape[0] - old.rank((operator - identity) % prime)
    return {
        "cyclic_order": prime,
        "fixed_dimension": fixed,
        "norm_rank": old.rank(norm),
        "H2_dimension": fixed - old.rank(norm),
    }


def gamma_dimensions(prime: int, theta: np.ndarray, tau: np.ndarray) -> dict:
    set_field(prime)
    dimension = theta.shape[0]
    condition = np.zeros((2 * dimension, 2 * dimension), dtype=np.int64)
    condition[:dimension, :dimension] = (eye(dimension) + theta) % prime
    condition[dimension:, dimension:] = (
        eye(dimension) + tau + old.mm(tau, tau)
    ) % prime
    z_basis = old.nullspace(condition)
    coboundaries = np.concatenate((eye(dimension) - theta, eye(dimension) - tau), axis=0) % prime
    return {
        "Z1_dimension": int(z_basis.shape[1]),
        "B1_dimension": old.rank(coboundaries),
        "H1_dimension": int(z_basis.shape[1]) - old.rank(coboundaries),
        "Z_basis": z_basis,
    }


def rank_gate(
    prime: int,
    theta: np.ndarray,
    tau: np.ndarray,
    rows: list[dict],
) -> dict:
    set_field(prime)
    cohomology = gamma_dimensions(prime, theta, tau)
    z_basis = cohomology.pop("Z_basis")
    symbols = aff.marked_symbols(theta, tau)
    rank_a = collections.Counter()
    rank_cz = collections.Counter()
    rank_observation = collections.Counter()
    digest = hashlib.sha256()
    first_positive = None
    for row in rows:
        first, second, _, _ = aff.relation_symbols(symbols, row["f_action"], int(row["m"]))
        identity = eye(theta.shape[0])
        if not np.array_equal(first.action, identity) or not np.array_equal(second.action, identity):
            raise RuntimeError("roof relation action is nontrivial")
        matrix_a = np.concatenate((first.f_coefficient, second.f_coefficient), axis=0) % prime
        matrix_c = np.concatenate((first.z_coefficient, second.z_coefficient), axis=0) % prime
        cz = old.mm(matrix_c, z_basis)
        a_rank = old.rank(matrix_a)
        c_rank = old.rank(cz)
        observation_rank = old.rank(np.concatenate((matrix_a, cz), axis=1)) - a_rank
        record = {
            "t_index": int(row["t_index"]),
            "rank_A": a_rank,
            "rank_CZ": c_rank,
            "rank_observation": observation_rank,
        }
        digest.update(json.dumps(record, sort_keys=True, separators=(",", ":")).encode() + b"\n")
        rank_a[a_rank] += 1
        rank_cz[c_rank] += 1
        rank_observation[observation_rank] += 1
        if observation_rank and first_positive is None:
            first_positive = record
    return {
        **cohomology,
        "rows": len(rows),
        "rank_A_distribution": counter_json(rank_a),
        "rank_CZ_distribution": counter_json(rank_cz),
        "rank_observation_distribution": counter_json(rank_observation),
        "first_positive_rank_row": first_positive,
        "rank_row_digest": digest.hexdigest(),
    }


def p2_multiplicity_lane() -> dict:
    set_field(2)
    theta, tau = p2.support_module(p2.SUPPORT2_REPS)
    theta_base = duplicate_blocks(theta, 4, 3)
    tau_base = duplicate_blocks(tau, 4, 3)
    gl2 = all_gl2(2)
    centralizers = [p2_centralizer(matrices) for matrices in itertools.product(gl2, repeat=3)]
    orbits, rho_x, rho_y = anchor_census(2, theta_base, tau_base, centralizers)
    rows = p2.roof_rows(rho_x, rho_y)
    identity_index = next(index for index, value in enumerate(centralizers) if np.array_equal(value, eye(24)))
    records = []
    for orbit_index, orbit in enumerate(orbits):
        gate = rank_gate(2, orbit["theta"], orbit["tau"], rows)
        records.append(
            {
                "orbit_index": orbit_index,
                "representative_twist_indices": list(orbit["representative"]),
                "orbit_size": len(orbit["orbit"]),
                "contains_block_duplicate": (identity_index, identity_index) in orbit["orbit"],
                "marked_group_order": matrix_group_order((orbit["theta"], orbit["tau"])),
                "cyclic_H2": cyclic_h2(2, orbit["theta"], orbit["tau"]),
                "rank_gate": gate,
                "theta_sha256": sha_obj(orbit["theta"].tolist()),
                "tau_sha256": sha_obj(orbit["tau"].tolist()),
            }
        )
    return {
        "candidate_id": "C1",
        "prime": 2,
        "dimension": 24,
        "GL2_order": len(gl2),
        "centralizer_order": len(centralizers),
        "twist_pairs_scanned": len(centralizers) ** 2,
        "anchor_solutions": sum(len(orbit["orbit"]) for orbit in orbits),
        "gauge_orbits": len(orbits),
        "orbit_sizes": sorted(len(orbit["orbit"]) for orbit in orbits),
        "orbits": records,
        "formal_class_outcomes_opened": 0,
    }


def p3_multiplicity_lane() -> dict:
    set_field(3)
    preflight = json.loads(
        (ROOT / "search/certs/escape28_preflight_v1r2_20260813.json").read_text(encoding="utf-8")
    )
    base = preflight["components"]["trivial_character"]["+"]
    theta = np.asarray(base["theta_matrix"], dtype=np.int64)
    tau = np.asarray(base["tau_matrix"], dtype=np.int64)
    theta_base = old.block_diag([theta, theta])
    tau_base = old.block_diag([tau, tau])
    gl2 = all_gl2(3)
    centralizers = [p3_centralizer(matrix) for matrix in gl2]
    orbits, rho_x, rho_y = anchor_census(3, theta_base, tau_base, centralizers)
    # old.roof_rows only uses its arguments to evaluate the stored S4 words.
    # Rebuild with the actual 7-dimensional pure anchors and then duplicate.
    sigma_1 = old.mm(old.mpow(tau, -1), theta)
    sigma_2 = old.mm(old.mpow(theta, -1), old.mpow(tau, 2))
    rho_x_7 = old.mpow(sigma_1, 2)
    rho_y_7 = old.mpow(sigma_2, 2)
    base_rows, _ = old.roof_rows(rho_x_7, rho_y_7)
    rows = []
    for row in base_rows:
        item = dict(row)
        action = old.word_action(row["s4_f_word"], rho_x_7, rho_y_7)
        item["f_action"] = old.block_diag([action, action])
        rows.append(item)
    identity_index = next(index for index, value in enumerate(centralizers) if np.array_equal(value, eye(14)))
    records = []
    for orbit_index, orbit in enumerate(orbits):
        gate = rank_gate(3, orbit["theta"], orbit["tau"], rows)
        records.append(
            {
                "orbit_index": orbit_index,
                "representative_twist_indices": list(orbit["representative"]),
                "orbit_size": len(orbit["orbit"]),
                "contains_block_duplicate": (identity_index, identity_index) in orbit["orbit"],
                "marked_group_order": matrix_group_order((orbit["theta"], orbit["tau"])),
                "cyclic_H2": cyclic_h2(3, orbit["theta"], orbit["tau"]),
                "rank_gate": gate,
                "theta_sha256": sha_obj(orbit["theta"].tolist()),
                "tau_sha256": sha_obj(orbit["tau"].tolist()),
            }
        )
    return {
        "candidate_id": "C2",
        "prime": 3,
        "dimension": 14,
        "GL2_order": len(gl2),
        "centralizer_order": len(centralizers),
        "twist_pairs_scanned": len(centralizers) ** 2,
        "anchor_solutions": sum(len(orbit["orbit"]) for orbit in orbits),
        "gauge_orbits": len(orbits),
        "orbit_sizes": sorted(len(orbit["orbit"]) for orbit in orbits),
        "orbits": records,
        "formal_class_outcomes_opened": 0,
    }


def hom_action(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    right_inverse = old.mpow(right, -1)
    left_dim, right_dim = left.shape[0], right.shape[0]
    answer = np.zeros((left_dim * right_dim, left_dim * right_dim), dtype=np.int64)
    for row in range(left_dim):
        for column in range(right_dim):
            image = np.outer(left[:, row], right_inverse[column, :]).reshape(-1)
            answer[:, right_dim * row + column] = image % 2
    return answer


def p2_simple_modules() -> list[dict]:
    set_field(2)
    modules = [
        ("one", eye(1), eye(1)),
        ("D", p2.J.copy(), p2.R.copy()),
        ("orbit1", *p2.support_module([(1, 0, 0), (0, 1, 0), (0, 0, 1)])),
        ("orbit2", *p2.support_module(p2.SUPPORT2_REPS)),
        ("orbit3", *p2.support_module([(1, b, c) for b in (1, 2) for c in (1, 2)])),
    ]
    answer = []
    for name, theta, tau in modules:
        sigma_1 = old.mm(old.mpow(tau, -1), theta)
        sigma_2 = old.mm(old.mpow(theta, -1), old.mpow(tau, 2))
        answer.append(
            {
                "name": name,
                "theta": theta,
                "tau": tau,
                "rho_x": old.mpow(sigma_1, 2),
                "rho_y": old.mpow(sigma_2, 2),
            }
        )
    return answer


def extension_spaces(submodule: dict, quotient: dict) -> dict:
    set_field(2)
    theta_hom = hom_action(submodule["theta"], quotient["theta"])
    tau_hom = hom_action(submodule["tau"], quotient["tau"])
    x_hom = hom_action(submodule["rho_x"], quotient["rho_x"])
    y_hom = hom_action(submodule["rho_y"], quotient["rho_y"])
    dimension = theta_hom.shape[0]
    gx, gy = p2.g3_permutations()
    pure_graph = old.cocycle_graph(gx, gy, x_hom, y_hom)
    pure_z_dimension = 2 * dimension - pure_graph["relation_rank"]
    pure_b = np.concatenate((eye(dimension) - x_hom, eye(dimension) - y_hom), axis=0) % 2
    pure_h1_dimension = pure_z_dimension - old.rank(pure_b)

    condition = np.zeros((2 * dimension, 2 * dimension), dtype=np.int64)
    condition[:dimension, :dimension] = (eye(dimension) + theta_hom) % 2
    condition[dimension:, dimension:] = (eye(dimension) + tau_hom + old.mm(tau_hom, tau_hom)) % 2
    symbols = aff.marked_symbols(theta_hom, tau_hom)
    restriction = np.concatenate((symbols["x"].z_coefficient, symbols["y"].z_coefficient), axis=0) % 2
    descent = old.mm(pure_graph["constraints"], restriction)
    marked_z = old.nullspace(np.concatenate((condition, descent), axis=0) % 2)
    marked_b = np.concatenate((eye(dimension) - theta_hom, eye(dimension) - tau_hom), axis=0) % 2
    marked_b_basis = marked_b[:, old.rref(marked_b)[1]]
    extended = old.extend_columns(marked_b_basis, marked_z)
    marked_h_basis = extended[:, marked_b_basis.shape[1] :]
    restricted_h = old.mm(restriction, marked_h_basis)
    pure_image_dimension = old.rank(np.concatenate((pure_b, restricted_h), axis=1)) - old.rank(pure_b)
    return {
        "theta_hom": theta_hom,
        "tau_hom": tau_hom,
        "pure_H1_dimension": pure_h1_dimension,
        "marked_H1_dimension": int(marked_h_basis.shape[1]),
        "marked_to_pure_image_dimension": pure_image_dimension,
        "marked_H_basis": marked_h_basis,
        "restriction": restriction,
        "pure_B": pure_b,
    }


def build_extension(submodule: dict, quotient: dict, vector: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    sub_dim = submodule["theta"].shape[0]
    quotient_dim = quotient["theta"].shape[0]
    hom_dim = sub_dim * quotient_dim
    z_theta = vector[:hom_dim].reshape(sub_dim, quotient_dim)
    z_tau = vector[hom_dim:].reshape(sub_dim, quotient_dim)
    zero = np.zeros((quotient_dim, sub_dim), dtype=np.int64)
    theta = np.block(
        [
            [submodule["theta"], old.mm(z_theta, quotient["theta"])],
            [zero, quotient["theta"]],
        ]
    ) % 2
    tau = np.block(
        [
            [submodule["tau"], old.mm(z_tau, quotient["tau"])],
            [zero, quotient["tau"]],
        ]
    ) % 2
    return theta, tau


def p2_nonsemisimple_lane() -> dict:
    set_field(2)
    modules = p2_simple_modules()
    ext_table = []
    marked_table = []
    candidates = []
    for submodule in modules:
        ext_row = []
        marked_row = []
        for quotient in modules:
            spaces = extension_spaces(submodule, quotient)
            ext_row.append(spaces["pure_H1_dimension"])
            marked_row.append(
                {
                    "marked_H1_dimension": spaces["marked_H1_dimension"],
                    "pure_image_dimension": spaces["marked_to_pure_image_dimension"],
                }
            )
            if spaces["marked_to_pure_image_dimension"]:
                good_vectors = []
                pure_b = spaces["pure_B"]
                pure_b_rank = old.rank(pure_b)
                for column in range(spaces["marked_H_basis"].shape[1]):
                    vector = spaces["marked_H_basis"][:, column]
                    restricted = old.mm(spaces["restriction"], vector.reshape(-1, 1))
                    if old.rank(np.concatenate((pure_b, restricted), axis=1)) > pure_b_rank:
                        good_vectors.append(vector)
                if spaces["marked_to_pure_image_dimension"] != 1 or len(good_vectors) != 1:
                    raise RuntimeError("unexpected marked extension multiplicity")
                theta, tau = build_extension(submodule, quotient, good_vectors[0])
                sigma_1 = old.mm(old.mpow(tau, -1), theta)
                sigma_2 = old.mm(old.mpow(theta, -1), old.mpow(tau, 2))
                rho_x = old.mpow(sigma_1, 2)
                rho_y = old.mpow(sigma_2, 2)
                rows = p2.roof_rows(rho_x, rho_y)
                candidates.append(
                    {
                        "extension_id": f"{submodule['name']}<-{quotient['name']}",
                        "dimension": theta.shape[0],
                        "unique_nonzero_marked_pure_class": True,
                        "cyclic_H2": cyclic_h2(2, theta, tau),
                        "rank_gate": rank_gate(2, theta, tau, rows),
                        "theta_sha256": sha_obj(theta.tolist()),
                        "tau_sha256": sha_obj(tau.tolist()),
                    }
                )
        ext_table.append(ext_row)
        marked_table.append(marked_row)
    return {
        "candidate_id": "C3",
        "prime": 2,
        "simple_modules": [
            {"name": module["name"], "dimension": module["theta"].shape[0]} for module in modules
        ],
        "table_convention": "row=submodule, column=quotient",
        "pure_Ext1_dimension_table": ext_table,
        "marked_extension_table": marked_table,
        "nonsplit_marked_candidates": candidates,
        "formal_class_outcomes_opened": 0,
    }


def positive_control() -> dict:
    escape2_path = ROOT / "search/certs/escape2_mainrun_v1_20260815.json"
    escape28_path = ROOT / "search/certs/escape28_mainrun_raw_v1_20260813.json"
    escape2 = json.loads(escape2_path.read_text(encoding="utf-8"))
    escape28 = json.loads(escape28_path.read_text(encoding="utf-8"))
    e2_distribution = escape2["campaign"]["Im_R_K_M_distribution"]
    e28_rows = escape28["full_campaign"]["evaluated_full_rows"]
    passed = e2_distribution == {"972": 7} and e28_rows == 1099008
    return {
        "passed": passed,
        "escape2_Im_R_K_M_distribution": e2_distribution,
        "escape28_evaluated_full_rows": e28_rows,
        "minimum_required": 324,
        "source_sha256": {
            str(escape2_path.relative_to(ROOT)).replace("\\", "/"): sha_file(escape2_path),
            str(escape28_path.relative_to(ROOT)).replace("\\", "/"): sha_file(escape28_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prereg", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--hard-timeout-seconds", type=int, default=240)
    args = parser.parse_args()
    began = time.monotonic()
    output_path = Path(args.output)
    checkpoint_path = Path(args.checkpoint)
    prereg_path = Path(args.prereg)
    state = {"schema": "campaign138_checkpoint/v1", "stage": "start", "complete": False}
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
            raise RuntimeError("producer/prereg binding mismatch")
        update("C1")
        c1 = p2_multiplicity_lane()
        update("C2")
        c2 = p3_multiplicity_lane()
        update("C3")
        c3 = p2_nonsemisimple_lane()
        control = positive_control()
        observed_counts = {
            "C1_anchor_solutions": c1["anchor_solutions"],
            "C1_gauge_orbits": c1["gauge_orbits"],
            "C2_anchor_solutions": c2["anchor_solutions"],
            "C2_gauge_orbits": c2["gauge_orbits"],
            "C3_nonsplit_marked_candidates": len(c3["nonsplit_marked_candidates"]),
            "rank_templates": sum(
                orbit["rank_gate"]["rows"] for orbit in c1["orbits"] + c2["orbits"]
            )
            + sum(candidate["rank_gate"]["rows"] for candidate in c3["nonsplit_marked_candidates"]),
        }
        if observed_counts != prereg["frozen_universe_counts"]:
            raise RuntimeError(f"frozen universe mismatch: {observed_counts}")
        positive = []
        for candidate_id, entries in (
            ("C1", c1["orbits"]),
            ("C2", c2["orbits"]),
            ("C3", c3["nonsplit_marked_candidates"]),
        ):
            for index, entry in enumerate(entries):
                if entry["rank_gate"]["first_positive_rank_row"] is not None:
                    positive.append(
                        {
                            "candidate_id": candidate_id,
                            "entry_index": index,
                            "row": entry["rank_gate"]["first_positive_rank_row"],
                        }
                    )
        result = {
            "schema": "campaign138_compact_preflight/v1",
            "run_id": "campaign138-compact-preflight-20260815",
            "preregistration_sha256": sha_file(prereg_path),
            "producer_sha256": sha_file(Path(__file__)),
            "positive_control": control,
            "C1": c1,
            "C2": c2,
            "C3": c3,
            "aggregate": {
                **observed_counts,
                "positive_rank_entries": positive,
                "formal_class_outcomes_opened": 0,
                "element_survival_outcomes_opened": 0,
                "rank_gate_stop_applied": not positive,
            },
            "noncontact": {
                "u": False,
                "c": False,
                "sealed_three_quantities": False,
                "sealed_K5": False,
            },
            "generated_by": {
                "python": sys.version.split()[0],
                "numpy": np.__version__,
                "script": str(Path(__file__).relative_to(ROOT)).replace("\\", "/"),
            },
        }
        if not control["passed"]:
            raise RuntimeError("positive control failed")
        atomic_json(output_path, result)
        update("complete", complete=True, output_sha256=sha_file(output_path), **observed_counts)
    finally:
        alarm.cancel()


if __name__ == "__main__":
    main()
