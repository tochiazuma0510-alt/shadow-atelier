#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
N = 12
MASK = (1 << N) - 1


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1 << 20), b""):
            h.update(part)
    return h.hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def ident(n=N):
    return tuple(1 << i for i in range(n))


def apply(a, vector):
    value = 0
    bit = 0
    while vector:
        if vector & 1:
            value ^= a[bit]
        vector >>= 1
        bit += 1
    return value


def mm(a, b):
    return tuple(apply(a, column) for column in b)


def madd(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def mpow(a, exponent):
    if exponent < 0:
        a = minv(a)
        exponent = -exponent
    answer = ident(len(a))
    while exponent:
        if exponent & 1:
            answer = mm(answer, a)
        a = mm(a, a)
        exponent >>= 1
    return answer


def rows_of(a):
    rows = [0] * len(a)
    for col, value in enumerate(a):
        for row in range(len(a)):
            if (value >> row) & 1:
                rows[row] |= 1 << col
    return rows


def from_rows(rows, n):
    cols = [0] * n
    for row, value in enumerate(rows):
        for col in range(n):
            if (value >> col) & 1:
                cols[col] |= 1 << row
    return tuple(cols)


def minv(a):
    n = len(a)
    rows = [rows_of(a)[i] | (1 << (n + i)) for i in range(n)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if (rows[i] >> col) & 1)
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for i in range(n):
            if i != col and ((rows[i] >> col) & 1):
                rows[i] ^= rows[col]
    return from_rows([(row >> n) & ((1 << n) - 1) for row in rows], n)


def rank_vectors(vectors):
    basis = {}
    for value in vectors:
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def rank_matrix(a):
    return rank_vectors(rows_of(a))


R = (2, 3)
J = (2, 1)
THETA3 = ((0, 1, 0), (1, 0, 0), (0, 0, 2))
TAU3 = ((0, 0, 1), (1, 0, 0), (0, 1, 0))
REPS = ((1, 1, 0), (1, 2, 0), (0, 1, 1), (0, 1, 2), (1, 0, 1), (1, 0, 2))


def qvec(q, a):
    return tuple(sum(q[i][j] * a[j] for j in range(3)) % 3 for i in range(3))


def block_embed(columns2, target, source, blocks=6):
    columns = [0] * (2 * blocks)
    for local_col, value in enumerate(columns2):
        for local_row in range(2):
            if (value >> local_row) & 1:
                columns[2 * source + local_col] |= 1 << (2 * target + local_row)
    return columns


def qop(q):
    columns = [0] * N
    for source, a in enumerate(REPS):
        weight = qvec(q, a)
        for target, b in enumerate(REPS):
            if weight == b:
                block = (1, 2)
                break
            if weight == tuple((-x) % 3 for x in b):
                block = J
                break
        piece = block_embed(block, target, source)
        columns = [x ^ y for x, y in zip(columns, piece)]
    return tuple(columns)


def aop(vector):
    columns = [0] * N
    for block, a in enumerate(REPS):
        exponent = sum(a[i] * vector[i] for i in range(3)) % 3
        piece = mpow(R, exponent)
        embedded = block_embed(piece, block, block)
        columns = [x ^ y for x, y in zip(columns, embedded)]
    return tuple(columns)


THETA = qop(THETA3)
TAU = mm(aop((1, 2, 0)), qop(TAU3))
SIGMA1 = mm(mpow(TAU, -1), THETA)
SIGMA2 = mm(mpow(THETA, -1), mpow(TAU, 2))
RHO_X = mpow(SIGMA1, 2)
RHO_Y = mpow(SIGMA2, 2)


def group_elements(generators):
    one = ident(len(generators[0]))
    known = {one}
    queue = [one]
    for value in queue:
        for generator in generators:
            new = mm(value, generator)
            if new not in known:
                known.add(new)
                queue.append(new)
    return queue


def affine_mul(left, right):
    lv, la = left
    rv, ra = right
    return lv ^ apply(la, rv), mm(la, ra)


def affine_inv(value):
    vector, action = value
    inverse = minv(action)
    return apply(inverse, vector), inverse


def affine_pow(value, exponent):
    if exponent < 0:
        return affine_pow(affine_inv(value), -exponent)
    answer = (0, ident(len(value[1])))
    while exponent:
        if exponent & 1:
            answer = affine_mul(answer, value)
        value = affine_mul(value, value)
        exponent >>= 1
    return answer


def word_action(word):
    answer = ident()
    for letter, exponent in word:
        answer = mm(answer, mpow(RHO_X if letter == "x" else RHO_Y, int(exponent)))
    return answer


def marked(representative):
    delta_big = (sum((int(representative[i]) & 1) << i for i in range(12)), THETA)
    delta_small = (sum((int(representative[12 + i]) & 1) << i for i in range(12)), TAU)
    sigma1 = affine_mul(affine_inv(delta_small), delta_big)
    sigma2 = affine_mul(affine_inv(delta_big), affine_pow(delta_small, 2))
    return {
        "Delta": delta_big,
        "delta": delta_small,
        "sigma1": sigma1,
        "sigma2": sigma2,
        "x": affine_pow(sigma1, 2),
        "y": affine_pow(sigma2, 2),
    }


def relations(elements, f_vector, f_action, m):
    f = (f_vector, f_action)
    s1, s2 = elements["sigma1"], elements["sigma2"]
    x, y = elements["x"], elements["y"]
    c = affine_pow(elements["Delta"], 2)
    exponent = 2 * m + 1
    left1 = affine_mul(affine_mul(affine_mul(affine_pow(s1, exponent), affine_inv(f)), affine_pow(s2, exponent)), f)
    right1 = affine_mul(affine_mul(affine_mul(affine_inv(f), s1), s2), affine_mul(affine_pow(x, -m), affine_pow(c, m)))
    rel1 = affine_mul(left1, affine_inv(right1))
    left2 = affine_mul(affine_mul(affine_mul(affine_inv(f), affine_pow(s2, exponent)), f), affine_pow(s1, exponent))
    right2 = affine_mul(affine_mul(affine_mul(s2, s1), affine_pow(y, -m)), affine_mul(affine_pow(c, m), f))
    rel2 = affine_mul(left2, affine_inv(right2))
    gen_a = affine_pow(x, exponent)
    gen_b = affine_mul(affine_mul(affine_inv(f), affine_pow(y, exponent)), f)
    return rel1, rel2, gen_a, gen_b


def build_roof():
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
                raise RuntimeError("checker CRT mismatch")
            m = choices[0]
            preimages = sum(1 for j, target in enumerate(reduction) if int(target) == k3_index and int(k9["shadows"][j]["m"]) == m)
            rows.append({
                "t_index": len(rows), "m": m, "t2_index": t2_index,
                "k3_index": k3_index, "k_mod3": int(second["kernel_cert"]["k"]) % 3,
                "preimages": preimages, "f_action": word_action(second["f_word"]),
            })
    return rows


def is_block_bad(gen_a, gen_b, block):
    av, aa = gen_a
    bv, ba = gen_b
    shift = 4 * block
    block_mask = 15 << shift
    target_a = (av & block_mask) >> shift
    target_b = (bv & block_mask) >> shift
    for u in range(16):
        full = u << shift
        image_a = (full ^ apply(aa, full)) >> shift
        image_b = (full ^ apply(ba, full)) >> shift
        if image_a == target_a and image_b == target_b:
            return True
    return False


def descends_to_g3(elements):
    generators = ((RHO_X, elements["x"][0]), (RHO_Y, elements["y"][0]))
    one = ident()
    values = {one: 0}
    queue = [one]
    for old_action in queue:
        old_cocycle = values[old_action]
        for generator_action, generator_cocycle in generators:
            new_action = mm(old_action, generator_action)
            new_cocycle = old_cocycle ^ apply(old_action, generator_cocycle)
            if new_action in values:
                if values[new_action] != new_cocycle:
                    return False
            else:
                values[new_action] = new_cocycle
                queue.append(new_action)
    return len(values) == 108


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", required=True)
    parser.add_argument("--producer", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--hard-timeout-seconds", type=int, default=180)
    args = parser.parse_args()
    began = time.monotonic()
    checkpoint = Path(args.checkpoint)
    state = {"schema": "escape2_checker_checkpoint/v1", "stage": "start", "complete": False}
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
        preflight = json.loads(Path(args.preflight).read_text(encoding="utf-8"))
        producer = json.loads(Path(args.producer).read_text(encoding="utf-8"))
        mismatches = []
        full_order = len(group_elements((THETA, TAU)))
        pure_order = len(group_elements((RHO_X, RHO_Y)))
        if (full_order, pure_order) != (648, 108):
            mismatches.append("group orders")
        theta_norm = madd(ident(), THETA)
        tau_norm = madd(madd(ident(), TAU), mm(TAU, TAU))
        theta_fixed = N - rank_matrix(madd(THETA, ident()))
        tau_fixed = N - rank_matrix(madd(TAU, ident()))
        h2 = {
            "theta_fixed_dimension": theta_fixed,
            "rank_1_plus_theta": rank_matrix(theta_norm),
            "H2_C2_dimension": theta_fixed - rank_matrix(theta_norm),
            "tau_fixed_dimension": tau_fixed,
            "rank_1_plus_tau_plus_tau2": rank_matrix(tau_norm),
            "H2_C3_dimension": tau_fixed - rank_matrix(tau_norm),
        }
        if h2["H2_C2_dimension"] != 2 or h2["H2_C3_dimension"] != 0:
            mismatches.append("H2 dimensions")
        classes = [entry for entry in preflight["cohomology"]["classes"] if entry["surjective"]]
        descent = []
        for entry in preflight["cohomology"]["classes"]:
            elements = marked(entry["representative"])
            descent.append(descends_to_g3(elements))
        if descent != [True] + [False] * 7:
            mismatches.append("SURJ descent census")
        rows = build_roof()
        if len(rows) != 324 or collections.Counter(row["preimages"] for row in rows) != collections.Counter({3: 324}):
            mismatches.append("roof census")
        solution_counts = collections.Counter()
        generation_counts = collections.Counter()
        obstruction_zero = 0
        image_nw = collections.Counter()
        image_km = collections.Counter()
        per_class = []
        for class_position, entry in enumerate(classes):
            elements = marked(entry["representative"])
            lifts = nonzero = absent = 0
            class_generation = collections.Counter()
            masks = [0] * 54
            for row in rows:
                base1, base2, _, _ = relations(elements, 0, row["f_action"], row["m"])
                if base1[1] != ident() or base2[1] != ident():
                    raise RuntimeError("checker roof relation action")
                constant = base1[0] | (base2[0] << N)
                columns = []
                for bit in range(N):
                    one1, one2, _, _ = relations(elements, 1 << bit, row["f_action"], row["m"])
                    columns.append((one1[0] | (one2[0] << N)) ^ constant)
                solutions = []
                for candidate in range(1 << N):
                    residual = constant
                    bits = candidate
                    bit = 0
                    while bits:
                        if bits & 1:
                            residual ^= columns[bit]
                        bits >>= 1
                        bit += 1
                    if residual == 0:
                        solutions.append(candidate)
                generating = 0
                for candidate in solutions:
                    _, _, gen_a, gen_b = relations(elements, candidate, row["f_action"], row["m"])
                    if all(not is_block_bad(gen_a, gen_b, block) for block in range(3)):
                        generating += 1
                zero = bool(solutions)
                lift = generating > 0
                obstruction_zero += int(zero)
                solution_counts[len(solutions)] += 1
                generation_counts[generating] += 1
                class_generation[generating] += 1
                nonzero += int(not zero)
                absent += int(not lift)
                lifts += int(lift)
                if lift:
                    masks[row["t2_index"]] |= 1 << row["k_mod3"]
            image_nw[lifts] += 1
            image_km[3 * lifts] += 1
            per_class.append({
                "class_position": class_position,
                "obstruction_nonzero_rows": nonzero,
                "generation_absent_rows": absent,
                "lift_rows": lifts,
                "generating_solution_count_distribution": dict(class_generation),
                "theta2_counts": [mask.bit_count() for mask in masks],
            })
            update("class_complete", classes_complete=class_position + 1, classes_total=7)
        expected = producer["campaign"]
        measured = {
            "evaluated_rows": len(classes) * len(rows),
            "nonzero_obstruction_row_count": len(classes) * len(rows) - obstruction_zero,
            "generation_absent_row_count": generation_counts[0],
            "solution_count_distribution": {str(k): v for k, v in solution_counts.items()},
            "generating_solution_count_distribution": {str(k): v for k, v in generation_counts.items()},
            "Im_R_N_E_N_W_distribution": {str(k): v for k, v in image_nw.items()},
            "Im_R_K_M_distribution": {str(k): v for k, v in image_km.items()},
        }
        for key, value in measured.items():
            if expected[key] != value:
                mismatches.append(key)
        for got, want in zip(per_class, expected["per_class"]):
            for key in ("obstruction_nonzero_rows", "generation_absent_rows", "lift_rows"):
                if got[key] != want[key]:
                    mismatches.append(f"per_class[{got['class_position']}].{key}")
            if {str(k): v for k, v in got["generating_solution_count_distribution"].items()} != want["generating_solution_count_distribution"]:
                mismatches.append(f"per_class[{got['class_position']}].generation")
            if got["theta2_counts"] != want["theta2_counts"]:
                mismatches.append(f"per_class[{got['class_position']}].theta2")
        verdict = {
            "schema": "escape2_checker/v1",
            "generated_by": {"script": str(Path(__file__)), "script_sha256": sha_file(Path(__file__)), "method": "pure-Python bit matrices; explicit affine evaluation; exhaustive 2^12 f translations per row; no NumPy or producer helpers"},
            "inputs": {"preflight_sha256": sha_file(Path(args.preflight)), "producer_sha256": sha_file(Path(args.producer))},
            "group_orders": {"full": full_order, "pure": pure_order},
            "H2": h2,
            "descent_census": {"classes": 8, "descends": sum(descent), "surjective": len(descent) - sum(descent), "flags": descent},
            "measured": measured,
            "per_class": per_class,
            "mismatch_count": len(mismatches), "mismatches": mismatches,
            "agreement": not mismatches,
            "preregistration_status_inherited": producer["preregistration_status"],
        }
        write_json(Path(args.output), verdict)
        update("checker_complete", complete=True, output_sha256=sha_file(Path(args.output)), mismatch_count=len(mismatches))
    finally:
        alarm.cancel()


if __name__ == "__main__":
    main()
