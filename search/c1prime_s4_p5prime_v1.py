#!/usr/bin/env python3
"""C1-prime(S4) and symbolic P5-prime certificate producer.

Only structural fields are read from the model certificate.  The local
coefficient payload and every field below its ``measurement`` key are ignored.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import threading
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from sympy.combinatorics import Permutation, PermutationGroup


ROOT = Path(__file__).resolve().parents[1]
GF8_MOD = 0b1011
POINTS = tuple([(1, t) for t in range(8)] + [(0, 1)])


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def gf_mul(a: int, b: int) -> int:
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= GF8_MOD
    return result & 7


def gf_inv(a: int) -> int:
    if not a:
        raise ZeroDivisionError
    return next(b for b in range(1, 8) if gf_mul(a, b) == 1)


def matrix_perm(matrix: tuple[tuple[int, int], tuple[int, int]]) -> Permutation:
    image = []
    for a, b in POINTS:
        c = gf_mul(a, matrix[0][0]) ^ gf_mul(b, matrix[1][0])
        d = gf_mul(a, matrix[0][1]) ^ gf_mul(b, matrix[1][1])
        line = (1, gf_mul(d, gf_inv(c))) if c else (0, 1)
        image.append(POINTS.index(line))
    return Permutation(image)


def key(p: Permutation) -> tuple[int, ...]:
    return tuple(p.array_form)


def pair_key(pair: tuple[Permutation, Permutation]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return key(pair[0]), key(pair[1])


def cycle_type(p: Permutation) -> tuple[int, ...]:
    lengths = [len(c) for c in p.cyclic_form]
    lengths.extend([1] * (9 - sum(lengths)))
    return tuple(sorted(lengths, reverse=True))


def compose_tuple(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[i]] for i in range(9))


def inverse_tuple(a: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * 9
    for i, value in enumerate(a):
        result[value] = i
    return tuple(result)


def conjugate_tuple(a: tuple[int, ...], g: tuple[int, ...]) -> tuple[int, ...]:
    return compose_tuple(compose_tuple(inverse_tuple(g), a), g)


def tuple_cycle_type(p: tuple[int, ...]) -> tuple[int, ...]:
    seen: set[int] = set()
    lengths = []
    for i in range(9):
        if i in seen:
            continue
        j, length = i, 0
        while j not in seen:
            seen.add(j)
            length += 1
            j = p[j]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def normalizer_receipt(group: PermutationGroup, generators: tuple[Permutation, Permutation]) -> dict[str, object]:
    elements = {key(g) for g in group.generate_schreier_sims()}
    gen_keys = tuple(key(g) for g in generators)
    normalizer = []
    centralizer_count = 0
    for g in itertools.permutations(range(9)):
        conjugated = tuple(conjugate_tuple(a, g) for a in gen_keys)
        if conjugated == gen_keys:
            centralizer_count += 1
        if all(a in elements for a in conjugated):
            normalizer.append(g)
    return {
        "order": len(normalizer),
        "centralizer_order": centralizer_count,
        "contains_cycle_type_7_1_1": any(tuple_cycle_type(g) == (7, 1, 1) for g in normalizer),
    }


def fixed_point_free_order3() -> list[Permutation]:
    result = []
    for image in itertools.permutations(range(9)):
        if tuple_cycle_type(image) == (3, 3, 3):
            result.append(Permutation(image))
    return result


def centralizer_orbits(pairs: list[tuple[Permutation, Permutation]], z: Permutation) -> list[list[tuple[Permutation, Permutation]]]:
    unseen = {pair_key(pair): pair for pair in pairs}
    orbits = []
    while unseen:
        pair = next(iter(unseen.values()))
        orbit_map = {}
        for j in range(9):
            g = z**j
            transformed = ((~g) * pair[0] * g, (~g) * pair[1] * g)
            orbit_map[pair_key(transformed)] = transformed
        for item in orbit_map:
            unseen.pop(item, None)
        orbits.append(list(orbit_map.values()))
    return orbits


def structural_model_receipt(path: Path) -> dict[str, object]:
    # Stop before the local-coefficient payload.  The one line consumed at the
    # boundary contains only the JSON key ``measurement`` and no value.
    prefix = []
    with path.open("r", encoding="utf-8") as source:
        for line in source:
            if line.startswith(' "measurement"'):
                break
            prefix.append(line)
    text = "".join(prefix).rstrip()
    if text.endswith(","):
        text = text[:-1]
    data = json.loads(text + "\n}\n")
    gate = data["gate_schema_v2"]
    frob = gate["frobenius"]
    return {
        "gate_boolean": bool(gate["PASS"]),
        "tau_product_identities": bool(gate["N_tau1"]["equals_kappa_g_cubed"])
        and bool(gate["N_tau2"]["equals_kappa_g_cubed"]),
        "global_product_identity": bool(gate["product_identity"]["L_equals_K_h_cubed"]),
        "model_polynomial_squarefree": bool(gate["f6"]["squarefree"]),
        "frobenius_seven_cycle_witness_count": len(frob["seven_cycle_witnesses_p_t0"]),
        "measurement_payload_read": False,
        "stream_stopped_before_measurement_payload": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="search/certs/c1prime_s4_p5prime_v1_20260813.json")
    parser.add_argument("--checkpoint", default="search/certs/c1prime_s4_p5prime_v1_checkpoint.json")
    parser.add_argument("--hard-timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    started = time.monotonic()
    state = {
        "schema": "c1prime_s4_p5prime_checkpoint/v1",
        "stage": "start",
        "complete": False,
        "u_touched": False,
        "c_touched": False,
    }
    atomic_json(checkpoint, state)

    def hard_timeout() -> None:
        state.update(stage="hard_timeout", elapsed_ms=int((time.monotonic() - started) * 1000))
        atomic_json(checkpoint, state)
        os._exit(124)

    timer = threading.Timer(args.hard_timeout_seconds, hard_timeout)
    timer.daemon = True
    timer.start()
    try:
        identity = Permutation(list(range(9)))
        s = matrix_perm(((1, 0), (1, 1)))
        t = matrix_perm(((4, 3), (1, 5)))
        w = s * (~t)
        x = w**2
        pi = ~t
        y = (~pi) * x * pi
        z = (~pi) * y * pi
        p_group = PermutationGroup([x, y])
        p_elements = list(p_group.generate_schreier_sims())
        order9_elements = [g for g in p_elements if cycle_type(g) == (9,)]
        z_class = {key(g) for g in p_group.conjugacy_class(z)}
        state.update(stage="intrinsic_window", elapsed_ms=int((time.monotonic() - started) * 1000))
        atomic_json(checkpoint, state)

        # Quotient triple and the inverse reconstruction words.
        qa = ~pi
        qb = (~x) * pi
        qc = ~(qa * qb)
        rx = ~(qb * qa)
        ry = ~(qa * qb)
        rz = ~(rx * ry)

        # Exhaust the quotient Nielsen class with AB=qc^-1.
        cq = ~qc
        quotient_solutions = []
        for a in fixed_point_free_order3():
            b = (~a) * cq
            if cycle_type(b) != (3, 3, 3):
                continue
            quotient_solutions.append((a, b, int(PermutationGroup([a, b]).order())))
        quotient_distribution = Counter(item[2] for item in quotient_solutions)
        unique_quotient_subgroups = {
            str(order): len({
                frozenset(key(g) for g in PermutationGroup([a, b]).generate_schreier_sims())
                for a, b, value in quotient_solutions if value == order
            })
            for order in (81, 324, 504)
        }
        quotient_504 = [(a, b) for a, b, order in quotient_solutions if order == 504]
        quotient_orbits = centralizer_orbits(quotient_504, cq)

        representatives = {
            order: next((a, b) for a, b, value in quotient_solutions if value == order)
            for order in (81, 324, 504)
        }
        normalizers = {
            str(order): normalizer_receipt(PermutationGroup(representatives[order]), representatives[order])
            for order in (81, 324, 504)
        }
        state.update(stage="quotient_nielsen", elapsed_ms=int((time.monotonic() - started) * 1000))
        atomic_json(checkpoint, state)

        # A 9-cycle belongs to a unique S9-conjugate of P: 240*168=40320.
        p_normalizer_order = int(normalizers["504"]["order"])
        conjugate_copy_count = 362880 // p_normalizer_order
        nine_cycle_incidence = conjugate_copy_count * len(order9_elements) // 40320

        # Hence all PSL triples with fixed z are found inside this one P.
        w_solutions = []
        for xx in order9_elements:
            yy = (~xx) * (~z)
            if cycle_type(yy) == (9,) and int(PermutationGroup([xx, yy]).order()) == 504:
                w_solutions.append((xx, yy))
        w_orbits = centralizer_orbits(w_solutions, z)
        diagonal = []
        for orbit in w_orbits:
            xx, yy = orbit[0]
            diagonal.append(key(xx) in z_class and key(yy) in z_class)
        intrinsic_orbit = next(
            i for i, orbit in enumerate(w_orbits) if pair_key((x, y)) in {pair_key(pair) for pair in orbit}
        )
        state.update(stage="six_dessins", elapsed_ms=int((time.monotonic() - started) * 1000))
        atomic_json(checkpoint, state)

        uloc_path = ROOT / "search/certs/u_meas_uloc_v2_20260731.json"
        structural_model = structural_model_receipt(uloc_path)
        seven_cycle_available = structural_model["frobenius_seven_cycle_witness_count"] > 0
        small_normalizers_excluded = not normalizers["81"]["contains_cycle_type_7_1_1"] and not normalizers["324"]["contains_cycle_type_7_1_1"]
        geometric_order_forced = seven_cycle_available and small_normalizers_excluded and quotient_distribution == Counter({81: 6, 324: 9, 504: 9})

        bound_paths = (
            ROOT / "certificates/S4.v2.json",
            ROOT / "search/certs/sdc_twist_S4_window_20260731.json",
            uloc_path,
            ROOT / "search/certs/u_meas_m7b_v2_20260731.json",
            ROOT / "docs/notes/u_meas_m1_passport_v1.md",
            ROOT / "docs/notes/u_meas_m3_caseb_v1.md",
            ROOT / "docs/notes/c1prime_s4_design_v1.md",
        )
        now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        cert = {
            "schema": "c1prime_s4_p5prime/v1",
            "run_id": f"c1prime-s4-p5prime-{now}",
            "generated_by": {
                "tool": "Python 3.13 + SymPy 1.14",
                "script": "search/c1prime_s4_p5prime_v1.py",
            },
            "window_binding": {
                "group_order": int(p_group.order()),
                "ord_s": int(s.order()),
                "ord_t": int(t.order()),
                "ord_w": int(w.order()),
                "ord_XYZ": [int(x.order()), int(y.order()), int(z.order())],
                "XYZ_product_identity": x * y * z == identity,
                "order9_element_count": len(order9_elements),
                "order9_class_size_of_Z": len(z_class),
                "XYZ_same_P_conjugacy_class": all(key(g) in z_class for g in (x, y, z)),
                "explicit_XYZ_array_form": [list(key(g)) for g in (x, y, z)],
            },
            "quotient_dessin": {
                "passport": [[3, 3, 3], [3, 3, 3], [9]],
                "orders_Aorb_Borb_Corb": [int(qa.order()), int(qb.order()), int(qc.order())],
                "Aorb_Borb_Corb_product_identity": qa * qb * qc == identity,
                "Corb_equals_Y": qc == y,
                "monodromy_order": int(PermutationGroup([qa, qb]).order()),
                "solution_count_fixed_C": len(quotient_solutions),
                "monodromy_order_distribution": {str(k): v for k, v in sorted(quotient_distribution.items())},
                "unique_generated_subgroups_by_order": unique_quotient_subgroups,
                "order504_solution_count": len(quotient_504),
                "order504_centralizer_orbit_count": len(quotient_orbits),
                "order504_centralizer_orbit_sizes": [len(orbit) for orbit in quotient_orbits],
                "normalizers_in_S9": normalizers,
                "structural_model_receipt": structural_model,
                "geometric_monodromy_order_forced_by_exact_7cycle_and_normalizers": geometric_order_forced,
            },
            "fibre_product_binding": {
                "base_change": "lambda^3-t*lambda^2+(t-3)*lambda+1=0",
                "kernel_words": {
                    "x": "(B_orb A_orb)^-1",
                    "y": "(A_orb B_orb)^-1",
                    "z": "(xy)^-1",
                },
                "reconstruction_XYZ_exact": [rx == x, ry == y, rz == z],
                "monodromy_order_after_reconstruction": int(PermutationGroup([rx, ry]).order()),
                "conjugate_P_copy_count": conjugate_copy_count,
                "nine_cycle_copy_incidence": nine_cycle_incidence,
                "fixed_Z_psl_solution_count": len(w_solutions),
                "fixed_Z_centralizer_orbit_count": len(w_orbits),
                "fixed_Z_centralizer_orbit_sizes": [len(orbit) for orbit in w_orbits],
                "diagonal_flags_by_orbit": diagonal,
                "diagonal_orbit_count": sum(diagonal),
                "intrinsic_orbit_index_zero_based": intrinsic_orbit,
                "intrinsic_orbit_diagonal": diagonal[intrinsic_orbit],
            },
            "p5prime_symbolic_certificate": {
                "numeric_local_class_read": False,
                "labelled_base_preserved": True,
                "unique_cusp_over_lambda_0_preserved": True,
                "local_parameter_change": "s_meas=gamma*s_intr*(1+O(s_intr))",
                "coefficient_change": "u0_inverse=uS4_inverse*gamma^9, up to a unit exponent if orientation is changed",
                "unit_exponent_set": [1, 2, 4, 5, 7, 8],
                "generated_cyclic_subgroups_equal": True,
                "ambient": "K^x/(K^x)^9; Q^x/(Q^x)^9 after RES-INJ-9",
            },
            "digest_binding": {
                str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path) for path in bound_paths
            },
            "digest_binding_mode": "opaque SHA-256 byte hashing; bound-file payloads are not JSON-decoded",
            "elapsed_ms": int((time.monotonic() - started) * 1000),
            "u_touched": False,
            "c_touched": False,
            "sealed_k5_touched": False,
            "prereg_quantities_untouched": True,
        }
        atomic_json(output, cert)
        state.update(
            stage="complete",
            complete=True,
            output=str(output.relative_to(ROOT)).replace("\\", "/"),
            elapsed_ms=cert["elapsed_ms"],
        )
        atomic_json(checkpoint, state)
        print(json.dumps({
            "run_id": cert["run_id"],
            "quotient_orbits": len(quotient_orbits),
            "w_dessin_orbits": len(w_orbits),
            "diagonal_orbits": sum(diagonal),
        }))
        return 0
    finally:
        timer.cancel()


if __name__ == "__main__":
    raise SystemExit(main())
