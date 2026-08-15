#!/usr/bin/env python3
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
import vnbit_compact_mainrun_v3 as old
import escape28_mainrun_v1 as aff

old.F = 2
aff.F = 2
aff.BLOCK = 4
F = 2
DIM = 12
BLOCK = 4


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1 << 20), b""):
            h.update(part)
    return h.hexdigest()


def sha_obj(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def eye(n: int) -> np.ndarray:
    return np.eye(n, dtype=np.int64)


R = np.array([[0, 1], [1, 1]], dtype=np.int64)
J = np.array([[0, 1], [1, 0]], dtype=np.int64)
THETA3 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 2]], dtype=np.int64)
TAU3 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=np.int64)
SUPPORT2_REPS = [
    (1, 1, 0), (1, 2, 0),
    (0, 1, 1), (0, 1, 2),
    (1, 0, 1), (1, 0, 2),
]


def q_operator(reps, q: np.ndarray) -> np.ndarray:
    n = 2 * len(reps)
    answer = np.zeros((n, n), dtype=np.int64)
    for source, a in enumerate(reps):
        target_weight = tuple(int(x) for x in (q @ np.asarray(a, dtype=np.int64)) % 3)
        hit = None
        for target, b in enumerate(reps):
            if target_weight == b:
                hit = (target, eye(2))
                break
            if target_weight == tuple((-x) % 3 for x in b):
                hit = (target, J)
                break
        if hit is None:
            raise RuntimeError("weight orbit is not stable")
        target, block = hit
        answer[2 * target : 2 * target + 2, 2 * source : 2 * source + 2] = block
    return answer % 2


def a_operator(reps, vector) -> np.ndarray:
    blocks = []
    for a in reps:
        exponent = sum(x * y for x, y in zip(a, vector)) % 3
        blocks.append(old.mpow(R, exponent))
    return old.block_diag(blocks)


def support_module(reps):
    theta = q_operator(reps, THETA3)
    tau = old.mm(a_operator(reps, (1, 2, 0)), q_operator(reps, TAU3))
    return theta, tau


def matrix_group_order(generators) -> int:
    one = eye(generators[0].shape[0])
    seen = {one.tobytes()}
    queue = [one]
    for element in queue:
        for generator in generators:
            new = old.mm(element, generator)
            key = new.tobytes()
            if key not in seen:
                seen.add(key)
                queue.append(new)
    return len(queue)


def h2_record(theta: np.ndarray, tau: np.ndarray) -> dict:
    n = theta.shape[0]
    i = eye(n)
    theta_norm = (i + theta) % 2
    tau_norm = (i + tau + old.mm(tau, tau)) % 2
    theta_fixed = n - old.rank((theta - i) % 2)
    tau_fixed = n - old.rank((tau - i) % 2)
    theta_rank = old.rank(theta_norm)
    tau_rank = old.rank(tau_norm)
    j1 = theta_fixed - theta_rank
    return {
        "dimension": n,
        "theta_jordan_partition": [2] * theta_rank + [1] * j1,
        "theta_fixed_dimension": theta_fixed,
        "rank_1_plus_theta": theta_rank,
        "H2_C2_dimension": theta_fixed - theta_rank,
        "tau_fixed_dimension": tau_fixed,
        "rank_1_plus_tau_plus_tau2": tau_rank,
        "H2_C3_dimension": tau_fixed - tau_rank,
    }


def gf8_mul(a: int, b: int) -> int:
    raw = 0
    for bit in range(3):
        if (b >> bit) & 1:
            raw ^= a << bit
    for bit in (4, 3):
        if (raw >> bit) & 1:
            raw ^= 0b1011 << (bit - 3)
    return raw


def gf8_inv(a: int) -> int:
    return next(b for b in range(1, 8) if gf8_mul(a, b) == 1)


def gf8_matmul(a, b):
    rows, middle, cols = len(a), len(b), len(b[0])
    return [[sum((gf8_mul(a[i][k], b[k][j]) for k in range(middle)), 0) for j in range(cols)] for i in range(rows)]


def gf8_add_terms(terms):
    value = 0
    for term in terms:
        value ^= term
    return value


def gf8_matmul(a, b):
    return [[gf8_add_terms(gf8_mul(a[i][k], b[k][j]) for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def gf8_matinv2(a):
    det = gf8_mul(a[0][0], a[1][1]) ^ gf8_mul(a[0][1], a[1][0])
    q = gf8_inv(det)
    return [[gf8_mul(q, a[1][1]), gf8_mul(q, a[0][1])], [gf8_mul(q, a[1][0]), gf8_mul(q, a[0][0])]]


def gf8_matpow(a, n: int):
    if n < 0:
        return gf8_matpow(gf8_matinv2(a), -n)
    answer = [[1, 0], [0, 1]]
    while n:
        if n & 1:
            answer = gf8_matmul(answer, a)
        a = gf8_matmul(a, a)
        n >>= 1
    return answer


def restrict_scalars(a) -> np.ndarray:
    rows = len(a)
    answer = np.zeros((3 * rows, 3 * rows), dtype=np.int64)
    for column in range(3 * rows):
        source_row, source_bit = divmod(column, 3)
        for target_row in range(rows):
            value = gf8_mul(a[target_row][source_row], 1 << source_bit)
            for bit in range(3):
                answer[3 * target_row + bit, column] = (value >> bit) & 1
    return answer


def kron_gf8(a, b):
    return [[gf8_mul(a[i // len(b)][j // len(b[0])], b[i % len(b)][j % len(b[0])]) for j in range(len(a[0]) * len(b[0]))] for i in range(len(a) * len(b))]


def augmentation_matrix(permutation) -> np.ndarray:
    answer = np.zeros((8, 8), dtype=np.int64)
    for col in range(8):
        images = [permutation[col], permutation[8]]
        for image in images:
            if image < 8:
                answer[image, col] ^= 1
    return answer


def centralizer_dimension(generators) -> int:
    n = generators[0].shape[0]
    equations = []
    for g in generators:
        for row in range(n):
            for col in range(n):
                eq = np.zeros(n * n, dtype=np.int64)
                for mid in range(n):
                    eq[n * row + mid] ^= int(g[mid, col])
                    eq[n * mid + col] ^= int(g[row, mid])
                equations.append(eq)
    return n * n - old.rank(np.asarray(equations, dtype=np.int64))


def p_simple_inventory() -> list[dict]:
    s8 = [[1, 0], [1, 1]]
    t8 = [[4, 3], [1, 5]]
    s_perm = old.mobius((1, 0, 1, 1))
    t_perm = old.mobius((4, 3, 1, 5))
    natural_s, natural_t = restrict_scalars(s8), restrict_scalars(t8)
    pair_s = restrict_scalars(kron_gf8(s8, [[gf8_mul(x, x) for x in row] for row in s8]))
    pair_t = restrict_scalars(kron_gf8(t8, [[gf8_mul(x, x) for x in row] for row in t8]))
    stein_s, stein_t = augmentation_matrix(s_perm), augmentation_matrix(t_perm)
    data = [
        ("trivial", eye(1), eye(1), 1),
        ("natural Frobenius orbit", natural_s, natural_t, 3),
        ("Steinberg", stein_s, stein_t, 1),
        ("two-factor Frobenius orbit", pair_s, pair_t, 3),
    ]
    answer = []
    for name, theta, tau, expected_end in data:
        entry = {"name": name, **h2_record(theta, tau)}
        entry["End_P_dimension_over_F2"] = centralizer_dimension((theta, tau))
        entry["expected_End_dimension"] = expected_end
        answer.append(entry)
    return answer


def g3_small_inventory() -> list[dict]:
    support1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    support3 = [(1, b, c) for b in (1, 2) for c in (1, 2)]
    modules = [
        ("trivial", eye(1), eye(1), "relative H1 dimension 0"),
        ("S4/V4 simple D", J, R, "H2(C2)=0"),
    ]
    for name, reps in (("support-one orbit", support1), ("support-two orbit", SUPPORT2_REPS), ("support-three orbit", support3)):
        theta, tau = support_module(reps)
        modules.append((name, theta, tau, "selected" if name == "support-two orbit" else "H2(C2)=0"))
    return [{"name": name, **h2_record(theta, tau), "gate_note": note} for name, theta, tau, note in modules]


def g3_permutations():
    def compose(a, b):
        return tuple(a[b[i]] for i in range(len(a)))
    r = (1, 2, 0)
    s = (0, 2, 1)
    rs = compose(r, s)
    def blocks(parts):
        value = []
        for block, p in enumerate(parts):
            value.extend(3 * block + p[i] for i in range(3))
        return tuple(value)
    return blocks((r, s, s)), blocks((rs, r, rs))


def gamma_classes(theta, tau):
    condition = np.zeros((24, 24), dtype=np.int64)
    condition[:12, :12] = (eye(12) + theta) % 2
    condition[12:, 12:] = (eye(12) + tau + old.mm(tau, tau)) % 2
    z_basis = old.nullspace(condition)
    cob = np.concatenate((eye(12) - theta, eye(12) - tau), axis=0) % 2
    b_basis = cob[:, old.rref(cob)[1]]
    full = old.extend_columns(b_basis, z_basis)
    h_basis = full[:, b_basis.shape[1] :]
    representatives = []
    for coordinates in itertools.product(range(2), repeat=h_basis.shape[1]):
        vector = (h_basis @ np.asarray(coordinates, dtype=np.int64)) % 2
        representatives.append((tuple(int(x) for x in vector), tuple(coordinates)))
    representatives.sort()
    classes = []
    for index, (vector, coordinates) in enumerate(representatives):
        classes.append({
            "class_index": index,
            "coordinates": list(coordinates),
            "representative": list(vector),
            "surjective": any(coordinates),
        })
    return {
        "Z1_dimension": z_basis.shape[1],
        "B1_dimension": b_basis.shape[1],
        "H1_dimension": h_basis.shape[1],
        "H1_order": 2 ** h_basis.shape[1],
        "basis_sha256": sha_obj(h_basis.tolist()),
        "classes": classes,
    }


def word_action(word, x, y):
    answer = eye(x.shape[0])
    for letter, exponent in word:
        answer = old.mm(answer, old.mpow(x if letter == "x" else y, int(exponent)))
    return answer


def roof_rows(rx, ry):
    s4 = json.loads((ROOT / "certificates/S4.v2.json").read_text(encoding="utf-8"))
    k3 = json.loads((ROOT / "certificates/K3.v1.json").read_text(encoding="utf-8"))
    k9 = json.loads((ROOT / "certificates/K9.v1.json").read_text(encoding="utf-8"))
    s4_pass = [entry for entry in s4["generation_detail"] if entry.get("pass")]
    reduction = k9["reduction"][0]["image"]
    rows = []
    for t2_index, first in enumerate(s4_pass):
        for k3_index, second in enumerate(k3["shadows"]):
            if int(first["m"]) % 3 != int(second["m"]) % 3:
                continue
            choices = [m for m in range(18) if m % 9 == int(first["m"]) and m % 6 == int(second["m"])]
            if len(choices) != 1:
                raise RuntimeError("CRT row mismatch")
            m = choices[0]
            preimages = sum(1 for j, target in enumerate(reduction) if int(target) == k3_index and int(k9["shadows"][j]["m"]) == m)
            rows.append({
                "t_index": len(rows), "m": m, "t2_index": t2_index,
                "k3_index": k3_index,
                "k_mod3": int(second["kernel_cert"]["k"]) % 3,
                "K9_preimage_count": preimages,
                "k3_f_word": second["f_word"],
                "f_action": word_action(second["f_word"], rx, ry),
            })
    if len(rows) != 324 or collections.Counter(row["K9_preimage_count"] for row in rows) != collections.Counter({3: 324}):
        raise RuntimeError("roof universe mismatch")
    return rows


def templates(theta, tau, rows):
    symbols = aff.marked_symbols(theta, tau)
    answer = []
    public = []
    for row in rows:
        first, second, gen_a, gen_b = aff.relation_symbols(symbols, row["f_action"], row["m"])
        if not np.array_equal(first.action, eye(DIM)) or not np.array_equal(second.action, eye(DIM)):
            raise RuntimeError("roof action relation mismatch")
        a1, a2 = first.f_coefficient, second.f_coefficient
        matrix = np.concatenate((a1, a2), axis=0)
        class_coefficient = np.concatenate((first.z_coefficient, second.z_coefficient), axis=0)
        constant = np.concatenate((first.constant, second.constant)) % 2
        hex_template = old.system_template(matrix)
        subsets = {}
        for mask in range(1, 8):
            selected = [block for block in range(3) if (mask >> block) & 1]
            variable_count = DIM + BLOCK * len(selected)
            base = np.zeros((2 * DIM, variable_count), dtype=np.int64)
            base[:, :DIM] = matrix
            pieces = [base]
            for position, block in enumerate(selected):
                section = slice(BLOCK * block, BLOCK * block + BLOCK)
                aux = slice(DIM + BLOCK * position, DIM + BLOCK * (position + 1))
                first_bad = np.zeros((BLOCK, variable_count), dtype=np.int64)
                first_bad[:, aux] = (eye(BLOCK) - gen_a.action[section, section]) % 2
                second_bad = np.zeros((BLOCK, variable_count), dtype=np.int64)
                second_bad[:, :DIM] = gen_b.f_coefficient[section, :]
                second_bad[:, aux] = -(eye(BLOCK) - gen_b.action[section, section]) % 2
                pieces.extend((first_bad, second_bad))
            subsets[mask] = (selected, old.system_template(np.concatenate(pieces, axis=0)))
        answer.append({
            "class_coefficient": class_coefficient, "constant": constant,
            "hex": hex_template, "subsets": subsets, "gen_a": gen_a, "gen_b": gen_b,
        })
        public.append({
            "rank_A1": old.rank(a1), "rank_A2": old.rank(a2),
            "rank_A": hex_template["rank"],
            "left_null_sha256": hex_template["left_null_sha256"],
            "A_sha256": sha_obj(matrix.tolist()),
        })
    return answer, public


def build_model():
    theta, tau = support_module(SUPPORT2_REPS)
    sigma1 = old.mm(old.mpow(tau, -1), theta)
    sigma2 = old.mm(old.mpow(theta, -1), old.mpow(tau, 2))
    rx, ry = old.mpow(sigma1, 2), old.mpow(sigma2, 2)
    if matrix_group_order((theta, tau)) != 648 or matrix_group_order((rx, ry)) != 108:
        raise RuntimeError("marked group order mismatch")
    gx, gy = g3_permutations()
    graph = old.cocycle_graph(gx, gy, rx, ry)
    z_g3 = old.nullspace(graph["constraints"])
    b_g3 = np.concatenate((eye(DIM) - rx, eye(DIM) - ry), axis=0) % 2
    h1_g3 = z_g3.shape[1] - old.rank(b_g3)
    if h1_g3 != 0:
        raise RuntimeError("SURJ-LIN H1(G3,V) changed")
    classes = gamma_classes(theta, tau)
    rows = roof_rows(rx, ry)
    row_templates, public_templates = templates(theta, tau, rows)
    block_gates = []
    for block in range(3):
        section = slice(BLOCK * block, BLOCK * block + BLOCK)
        distribution = collections.Counter()
        for coordinates in itertools.product(range(2), repeat=BLOCK):
            if any(coordinates):
                distribution[old.cyclic_dimension(np.asarray(coordinates), (rx[section, section], ry[section, section]))] += 1
        block_gates.append(dict(distribution))
    preflight = {
        "schema": "escape2_preflight/v1",
        "module": {
            "description": "support-two orbit bundle for C3^3 under S4",
            "dimension": DIM,
            "W_constituent_dimensions": [4, 4, 4],
            "theta_matrix": theta.tolist(), "tau_matrix": tau.tolist(),
            "rho_x": rx.tolist(), "rho_y": ry.tolist(),
            "full_marked_group_order": 648, "pure_G3_image_order": 108,
            "H2": h2_record(theta, tau),
            "P_simple_inventory": p_simple_inventory(),
            "G3_small_stable_inventory": g3_small_inventory(),
            "block_nonzero_cyclic_dimension_distributions": block_gates,
            "End_W_V": "F_2^3", "End_W_V_unit_group_order": 1,
        },
        "anchor": {
            "A1_holds": bool(np.array_equal(aff.marked_symbols(theta, tau)["x"].action, rx)),
            "A2_holds": bool(np.array_equal(aff.marked_symbols(theta, tau)["y"].action, ry)),
            "anchor_solutions": 1, "gauge_group_order": 1,
            "effective_gauge_order": 1, "window_count": 1,
        },
        "cohomology": {
            **classes,
            "H1_G3_V_dimension": h1_g3,
            "H1_barW_V_dimension": 0,
            "surjective_class_count": sum(entry["surjective"] for entry in classes["classes"]),
            "SURJ_LIN_note": "H1(G3,V)=0 from full 108-element Cayley collision system; P is perfect and acts trivially",
        },
        "template_gate": {
            "rows": len(public_templates), "A_shape": [24, 12],
            "rank_A1_distribution": dict(collections.Counter(x["rank_A1"] for x in public_templates)),
            "rank_A2_distribution": dict(collections.Counter(x["rank_A2"] for x in public_templates)),
            "rank_A_distribution": dict(collections.Counter(x["rank_A"] for x in public_templates)),
            "template_sha256": sha_obj(public_templates),
        },
        "universe": {"windows": 1, "surjective_classes": 7, "rows_per_class": 324, "full_rows": 2268},
        "source_sha256": {
            name: sha_file(ROOT / name) for name in (
                "ops/inbox_codex/sol_task_136_escape2.txt",
                "docs/notes/vnbit_compact_route_v3.md",
                "docs/notes/entangled972_reading_v1.md",
                "search/vnbit_compact_mainrun_v3.py",
                "search/escape28_mainrun_v1.py",
                "certificates/S4.v2.json", "certificates/K3.v1.json", "certificates/K9.v1.json",
            )
        },
        "stage_boundary": {"stage": "template_gate", "lift_outcomes_opened_by_this_stage": 0},
        "noncontact": {"u": False, "c": False, "sealed_three_quantities": False, "sealed_K5": False},
    }
    runtime = {"theta": theta, "tau": tau, "rx": rx, "ry": ry, "rows": rows, "templates": row_templates}
    return preflight, runtime


def measure(preflight, runtime):
    classes = [entry for entry in preflight["cohomology"]["classes"] if entry["surjective"]]
    obstruction = collections.Counter()
    solutions = collections.Counter()
    generation = collections.Counter()
    image_nw = collections.Counter()
    image_km = collections.Counter()
    theta_counts = collections.Counter()
    first_lift = None
    first_nonzero = None
    per_class = []
    digest = hashlib.sha256()
    for class_position, cls in enumerate(classes):
        representative = np.asarray(cls["representative"], dtype=np.int64)
        lifts = nonzero = absent = 0
        masks = [0] * 54
        class_generation = collections.Counter()
        for row, template in zip(runtime["rows"], runtime["templates"]):
            rhs = -(template["class_coefficient"] @ representative + template["constant"]) % 2
            obs = tuple(int(x) for x in (template["hex"]["left_null"] @ rhs) % 2)
            zero = not any(obs)
            total = old.system_count(template["hex"], rhs)
            bad = {}
            if total:
                for mask, (selected, subset) in template["subsets"].items():
                    parts = [rhs]
                    for block in selected:
                        section = slice(BLOCK * block, BLOCK * block + BLOCK)
                        parts.append((template["gen_a"].z_coefficient[section, :] @ representative + template["gen_a"].constant[section]) % 2)
                        parts.append(-(template["gen_b"].z_coefficient[section, :] @ representative + template["gen_b"].constant[section]) % 2)
                    bad[mask] = old.system_count(subset, np.concatenate(parts))
                union = sum(value if mask.bit_count() % 2 else -value for mask, value in bad.items())
                generating = total - union
            else:
                generating = 0
            lift = zero and generating > 0
            obstruction[zero] += 1
            solutions[total] += 1
            generation[generating] += 1
            class_generation[generating] += 1
            lifts += int(lift)
            nonzero += int(not zero)
            absent += int(generating == 0)
            if lift:
                masks[row["t2_index"]] |= 1 << row["k_mod3"]
            raw = {
                "class_position": class_position, "class_index": cls["class_index"],
                "class_coordinates": cls["coordinates"], "t_index": row["t_index"],
                "t2_index": row["t2_index"], "k3_index": row["k3_index"],
                "k_mod3": row["k_mod3"], "left_null_obstruction": list(obs),
                "H2_C2_coordinates": [0, 0] if zero else "not_projected",
                "H2_C3_coordinates": [], "solution_count": total,
                "generating_solution_count": generating, "lift": lift,
            }
            digest.update(json.dumps(raw, sort_keys=True, separators=(",", ":")).encode() + b"\n")
            if lift and first_lift is None:
                first_lift = raw
            if not zero and first_nonzero is None:
                first_nonzero = raw
        counts = [int(mask).bit_count() for mask in masks]
        theta_counts.update(counts)
        image_nw[lifts] += 1
        image_km[3 * lifts] += 1
        per_class.append({
            "class_position": class_position, "class_index": cls["class_index"],
            "class_coordinates": cls["coordinates"], "obstruction_nonzero_rows": nonzero,
            "generation_absent_rows": absent, "lift_rows": lifts,
            "generating_solution_count_distribution": dict(class_generation),
            "theta2_k_masks": masks, "theta2_counts": counts,
            "Im_R_N_E_N_W_size": lifts, "Im_R_K_M_size": 3 * lifts,
        })
    return {
        "schema": "escape2_mainrun/v1",
        "inputs": {"preflight_sha256": sha_file(Path(preflight["_path"])), "preregistration_sha256": preflight["_prereg_sha256"]},
        "module_H2": preflight["module"]["H2"], "universe": preflight["universe"],
        "campaign": {
            "evaluated_rows": sum(obstruction.values()),
            "obstruction_zero_distribution": {str(k).lower(): v for k, v in obstruction.items()},
            "nonzero_obstruction_row_count": obstruction[False],
            "H2_C2_class_distribution": {"[0,0]": obstruction[True]},
            "H2_C3_class_distribution": {"[]": sum(obstruction.values())},
            "solution_count_distribution": dict(solutions),
            "generating_solution_count_distribution": dict(generation),
            "generation_absent_row_count": generation[0],
            "first_nonzero_obstruction": first_nonzero,
            "first_lift_row": first_lift,
            "Im_R_N_E_N_W_distribution": dict(image_nw),
            "Im_R_K_M_distribution": dict(image_km),
            "theta2_count_distribution": dict(theta_counts),
            "per_class": per_class,
            "outcome_sha256": digest.hexdigest(),
        },
        "preregistration_status": {
            "blind_before_formal_measurement": False,
            "reason": "an engineering pilot opened all 2268 outcomes before the versioned freeze",
            "pilot_outcomes_opened_before_freeze": 2268,
            "directional_prediction_in_freeze": None,
        },
        "endgame_scope": "gentle side only; PENT_W=NOT_RUN; FAKE-KILL^{B4}/U-10=NOT_RUN; no finite-depth type adjudication",
        "noncontact": preflight["noncontact"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("preflight", "freeze", "measure"), required=True)
    parser.add_argument("--preflight", required=True)
    parser.add_argument("--prereg", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--hard-timeout-seconds", type=int, default=180)
    args = parser.parse_args()
    began = time.monotonic()
    checkpoint = Path(args.checkpoint)
    state = {"schema": "escape2_checkpoint/v1", "mode": args.mode, "stage": "start", "complete": False}
    write_json(checkpoint, state)
    def update(stage, **kw):
        state.update(stage=stage, elapsed_ms=int(1000 * (time.monotonic() - began)), **kw)
        write_json(checkpoint, state)
    def timeout():
        if not state["complete"]:
            update("hard_timeout")
            os._exit(124)
    alarm = threading.Timer(args.hard_timeout_seconds, timeout)
    alarm.daemon = True
    alarm.start()
    try:
        preflight_path, prereg_path, output_path = Path(args.preflight), Path(args.prereg), Path(args.output)
        rebuilt, runtime = build_model()
        rebuilt["generated_by"] = {"script": str(Path(__file__)), "script_sha256": sha_file(Path(__file__)), "python": sys.version.split()[0], "numpy": np.__version__}
        if args.mode == "preflight":
            write_json(preflight_path, rebuilt)
            update("preflight_complete", complete=True, output_sha256=sha_file(preflight_path), outcomes_opened=0)
            return
        if args.mode == "freeze":
            loaded = json.loads(preflight_path.read_text(encoding="utf-8"))
            if sha_obj({k: v for k, v in loaded.items() if k != "generated_by"}) != sha_obj({k: v for k, v in rebuilt.items() if k != "generated_by"}):
                raise RuntimeError("preflight reconstruction changed")
            freeze = {
                "schema": "escape2_prereg/v1-contaminated",
                "preflight_sha256": sha_file(preflight_path),
                "producer_sha256": sha_file(Path(__file__)),
                "universe": loaded["universe"], "template_gate": loaded["template_gate"],
                "blind_before_measurement": False,
                "pilot_outcomes_opened_before_freeze": 2268,
                "directional_obstruction_prediction": None,
                "rank_consistency_required": True,
                "status": "procedural downgrade; not prospective",
            }
            write_json(prereg_path, freeze)
            update("freeze_complete", complete=True, output_sha256=sha_file(prereg_path))
            return
        loaded = json.loads(preflight_path.read_text(encoding="utf-8"))
        freeze = json.loads(prereg_path.read_text(encoding="utf-8"))
        if freeze["preflight_sha256"] != sha_file(preflight_path) or freeze["producer_sha256"] != sha_file(Path(__file__)):
            raise RuntimeError("freeze binding failed")
        if freeze["universe"] != loaded["universe"] or freeze["template_gate"] != loaded["template_gate"]:
            raise RuntimeError("frozen universe changed")
        loaded["_path"] = str(preflight_path)
        loaded["_prereg_sha256"] = sha_file(prereg_path)
        result = measure(loaded, runtime)
        result["generated_by"] = rebuilt["generated_by"]
        write_json(output_path, result)
        update("measure_complete", complete=True, output_sha256=sha_file(output_path), evaluated_rows=result["campaign"]["evaluated_rows"])
    finally:
        alarm.cancel()


if __name__ == "__main__":
    main()
