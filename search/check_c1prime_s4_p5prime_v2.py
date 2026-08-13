"""Helper-disjoint checker for c1prime_s4_p5prime/v2.

Standard-library tuple permutations and integer polynomial arithmetic only.
No SymPy and no producer import.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GF8_MOD = 0b1011
POINTS = tuple([(1, t) for t in range(8)] + [(0, 1)])
ID = tuple(range(9))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
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


def matrix_perm(matrix: tuple[tuple[int, int], tuple[int, int]]) -> tuple[int, ...]:
    image = []
    for a, b in POINTS:
        c = gf_mul(a, matrix[0][0]) ^ gf_mul(b, matrix[1][0])
        d = gf_mul(a, matrix[0][1]) ^ gf_mul(b, matrix[1][1])
        line = (1, gf_mul(d, gf_inv(c))) if c else (0, 1)
        image.append(POINTS.index(line))
    return tuple(image)


def mul(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(b[a[i]] for i in range(9))


def inv(a: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * 9
    for i, value in enumerate(a):
        result[value] = i
    return tuple(result)


def power(a: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    if exponent < 0:
        return power(inv(a), -exponent)
    result = ID
    while exponent:
        if exponent & 1:
            result = mul(result, a)
        a = mul(a, a)
        exponent //= 2
    return result


def order(a: tuple[int, ...]) -> int:
    value = ID
    for exponent in range(1, 100):
        value = mul(value, a)
        if value == ID:
            return exponent
    raise RuntimeError("order bound")


def closure(generators: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    seen = {ID}
    queue = deque([ID])
    while queue:
        value = queue.popleft()
        for generator in generators:
            nxt = mul(value, generator)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def cycle_type(p: tuple[int, ...]) -> tuple[int, ...]:
    seen: set[int] = set()
    lengths = []
    for i in range(9):
        if i in seen:
            continue
        j = i
        length = 0
        while j not in seen:
            seen.add(j)
            length += 1
            j = p[j]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def poly_add(a: list[int], b: list[int]) -> list[int]:
    out = [0] * max(len(a), len(b))
    for i, value in enumerate(a):
        out[i] += value
    for i, value in enumerate(b):
        out[i] += value
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, left in enumerate(a):
        for j, right in enumerate(b):
            out[i + j] += left * right
    return out


def shanks_discriminant() -> list[int]:
    # For X^3+bX^2+cX+d, Delta=b^2c^2-4c^3-4b^3d-27d^2+18bcd.
    b = [0, -1]
    c = [-3, 1]
    d = [1]
    terms = [
        poly_mul(poly_mul(b, b), poly_mul(c, c)),
        [-4 * value for value in poly_mul(poly_mul(c, c), c)],
        [-4 * value for value in poly_mul(poly_mul(b, b), poly_mul(b, d))],
        [-27 * value for value in poly_mul(d, d)],
        [18 * value for value in poly_mul(poly_mul(b, c), d)],
    ]
    out = [0]
    for term in terms:
        out = poly_add(out, term)
    return out


def structural_prefix(path: Path) -> tuple[dict[str, object], bool]:
    prefix = []
    stopped = False
    with path.open("r", encoding="utf-8") as source:
        for line in source:
            if line.startswith(' "measurement"'):
                stopped = True
                break
            prefix.append(line)
    text = "".join(prefix).rstrip()
    if text.endswith(","):
        text = text[:-1]
    return json.loads(text + "\n}\n")["gate_schema_v2"], stopped


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="search/certs/c1prime_s4_p5prime_v2_20260813.json")
    parser.add_argument("--output", default="search/certs/c1prime_s4_p5prime_v2_check_20260813.json")
    args = parser.parse_args()
    source_path = ROOT / args.input
    source = json.loads(source_path.read_text(encoding="utf-8"))
    gate, stopped = structural_prefix(ROOT / "search/certs/u_meas_uloc_v2_20260731.json")

    s = matrix_perm(((1, 0), (1, 1)))
    t = matrix_perm(((4, 3), (1, 5)))
    w = mul(s, inv(t))
    x = power(w, 2)
    y = mul(mul(inv(s), x), s)
    p_group = closure([x, y])
    order9 = [g for g in p_group if order(g) == 9]
    order9_types = sorted({cycle_type(g) for g in order9})

    a = source["requirement_A_passport_binding"]
    g = source["requirement_G_nine_cycle_incidence"]
    checks = {
        "schema": source["schema"] == "c1prime_s4_p5prime/v2",
        "input_hashes": all(
            sha256(ROOT / path) == digest for path, digest in source["input_sha256"].items()
        ),
        "structural_boundary": stopped and not source["structural_boundary"]["measurement_payload_read"],
        "shanks_discriminant_integer_expansion": (
            shanks_discriminant() == poly_mul([9, -3, 1], [9, -3, 1])
            and a["discriminant"] == "(t^2-3*t+9)^2"
            and a["branch_points"] == ["3*zeta_6", "3*zeta_6^-1"]
        ),
        "tau_partitions": all(
            gate[name]["degree"] == 9
            and gate[name]["deg_radical"] == 3
            and gate[name]["deg_gcd_with_derivative"] == 6
            and gate[name]["equals_kappa_g_cubed"]
            and a["tau_rows"][name]["ramification_partition"] == [3, 3, 3]
            for name in ("N_tau1", "N_tau2")
        ),
        "passport_pin": (
            a["shanks_branch_equals_C_order3_branch"]
            and a["measured_C_passport"] == [[3, 3, 3], [3, 3, 3], [9]]
            and a["riemann_hurwitz"]["g_C"] == 2
        ),
        "specialization_t_line": (
            source["requirement_B_specialization"]["witness_coordinate_line"] == "t-line"
            and source["requirement_B_specialization"]["seven_cycle_witness_count"]
            == len(gate["frobenius"]["seven_cycle_witnesses_p_t0"])
        ),
        "prior_and_Q_model_pins": (
            source["requirement_C_intrinsic_Q_model"]["pin"] == "section (I), LEDGER 633"
            and "monodromy" in source["requirement_C_intrinsic_Q_model"]["rigidity_reading"]
            and "FINDING U-8" in source["requirement_D_prior_work"]["pin"]
        ),
        "P_order": len(p_group) == 504 and g["P_order"] == 504,
        "all_order9_are_nine_cycles": (
            len(order9) == 168
            and order9_types == [(9,)]
            and g["all_168_are_nine_cycles_in_this_action"]
        ),
        "incidence": g["incidence_total"] == 40320 == g["S9_nine_cycle_total"],
        "tautology_demoted": (
            not a["legacy_reconstruction_XYZ_exact_role"]["independent_information"]
            and a["legacy_reconstruction_XYZ_exact_role"]["retained_only_as_regression"]
        ),
        "arithmetic_upper_bound_not_from_negative_sample": (
            source["monodromy_arithmetic"]["order"] == 1512
            and not source["monodromy_arithmetic"]["outside_PGammaL_empty_sample_used_as_upper_bound"]
        ),
        "p5_noncontact": (
            source["p5prime"]["generated_cyclic_subgroups_equal"]
            and not source["p5prime"]["representative_equality_claimed"]
            and not source["p5prime"]["numeric_local_class_read"]
        ),
        "global_noncontact": (
            not source["u_touched"]
            and not source["c_touched"]
            and not source["sealed_k5_touched"]
            and source["prereg_quantities_untouched"]
        ),
    }
    result = {
        "schema": "c1prime_s4_p5prime_check/v2",
        "checker": "search/check_c1prime_s4_p5prime_v2.py",
        "helper_disjointness": "stdlib tuple permutations; no SymPy and no producer import",
        "source_run_id": source["run_id"],
        "source_sha256": sha256(source_path),
        "checks": checks,
        "all_checks_true": all(checks.values()),
        "recomputed": {
            "P_order": len(p_group),
            "abstract_order9_element_count": len(order9),
            "order9_cycle_types": [list(row) for row in order9_types],
            "seven_cycle_witness_count": len(gate["frobenius"]["seven_cycle_witnesses_p_t0"]),
        },
        "u_touched": False,
        "c_touched": False,
    }
    atomic_json(ROOT / args.output, result)
    print(json.dumps({
        "all_checks_true": result["all_checks_true"],
        "P_order": len(p_group),
        "order9": len(order9),
    }, sort_keys=True))
    return 0 if result["all_checks_true"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
