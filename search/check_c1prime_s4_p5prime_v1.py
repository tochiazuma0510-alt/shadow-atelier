#!/usr/bin/env python3
"""Standard-library checker for c1prime_s4_p5prime/v1.

No producer helper and no permutation-group package is imported.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ID = tuple(range(9))
MOD = 0b1011
POINTS = tuple([(1, t) for t in range(8)] + [(0, 1)])


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def mul(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[i]] for i in range(9))


def inv(a: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * 9
    for i, value in enumerate(a):
        result[value] = i
    return tuple(result)


def power(a: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = ID
    base = a
    while exponent:
        if exponent & 1:
            result = mul(result, base)
        base = mul(base, base)
        exponent >>= 1
    return result


def conjugate(a: tuple[int, ...], g: tuple[int, ...]) -> tuple[int, ...]:
    return mul(mul(inv(g), a), g)


def cycle_type(a: tuple[int, ...]) -> tuple[int, ...]:
    seen: set[int] = set()
    lengths = []
    for i in range(9):
        if i in seen:
            continue
        j, length = i, 0
        while j not in seen:
            seen.add(j)
            length += 1
            j = a[j]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def order(a: tuple[int, ...]) -> int:
    return math.lcm(*cycle_type(a))


def closure(generators: tuple[tuple[int, ...], ...]) -> set[tuple[int, ...]]:
    steps = tuple(dict.fromkeys(generators + tuple(inv(g) for g in generators)))
    seen = {ID}
    stack = [ID]
    while stack:
        current = stack.pop()
        for step in steps:
            nxt = mul(current, step)
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen


def gf_mul(a: int, b: int) -> int:
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= MOD
    return result & 7


def gf_inv(a: int) -> int:
    return next(b for b in range(1, 8) if gf_mul(a, b) == 1)


def matrix_perm(matrix: tuple[tuple[int, int], tuple[int, int]]) -> tuple[int, ...]:
    result = []
    for a, b in POINTS:
        c = gf_mul(a, matrix[0][0]) ^ gf_mul(b, matrix[1][0])
        d = gf_mul(a, matrix[0][1]) ^ gf_mul(b, matrix[1][1])
        line = (1, gf_mul(d, gf_inv(c))) if c else (0, 1)
        result.append(POINTS.index(line))
    return tuple(result)


def orbits(pairs: list[tuple[tuple[int, ...], tuple[int, ...]]], z: tuple[int, ...]) -> list[set[tuple[tuple[int, ...], tuple[int, ...]]]]:
    unseen = set(pairs)
    result = []
    while unseen:
        pair = next(iter(unseen))
        orbit = set()
        for j in range(9):
            g = power(z, j)
            orbit.add((conjugate(pair[0], g), conjugate(pair[1], g)))
        unseen -= orbit
        result.append(orbit)
    return result


def normalizer(group: set[tuple[int, ...]], generators: tuple[tuple[int, ...], tuple[int, ...]]) -> tuple[int, int, bool]:
    count = 0
    centralizer_count = 0
    has7 = False
    for g in itertools.permutations(range(9)):
        images = tuple(conjugate(a, g) for a in generators)
        if images == generators:
            centralizer_count += 1
        if all(image in group for image in images):
            count += 1
            has7 = has7 or cycle_type(g) == (7, 1, 1)
    return count, centralizer_count, has7


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="search/certs/c1prime_s4_p5prime_v1_20260813.json")
    parser.add_argument("--output", default="search/certs/c1prime_s4_p5prime_v1_check_20260813.json")
    args = parser.parse_args()
    source_path = ROOT / args.input
    source = json.loads(source_path.read_text(encoding="utf-8"))

    s = matrix_perm(((1, 0), (1, 1)))
    t = matrix_perm(((4, 3), (1, 5)))
    w = mul(s, inv(t))
    x = power(w, 2)
    pi = inv(t)
    y = conjugate(x, pi)
    z = conjugate(y, pi)
    p = closure((x, y))
    p_order9 = [g for g in p if cycle_type(g) == (9,)]
    z_class = {conjugate(z, g) for g in p}

    qa = inv(pi)
    qb = mul(inv(x), pi)
    qc = inv(mul(qa, qb))
    cq = inv(qc)
    quotient = []
    for a in itertools.permutations(range(9)):
        if cycle_type(a) != (3, 3, 3):
            continue
        b = mul(inv(a), cq)
        if cycle_type(b) == (3, 3, 3):
            quotient.append((a, b, len(closure((a, b)))))
    qdist = Counter(item[2] for item in quotient)
    unique_quotient_subgroups = {
        str(size): len({frozenset(closure((a, b))) for a, b, value in quotient if value == size})
        for size in (81, 324, 504)
    }
    q504 = [(a, b) for a, b, size in quotient if size == 504]
    qorbits = orbits(q504, cq)

    normalizers = {}
    for size in (81, 324, 504):
        a, b, _ = next(item for item in quotient if item[2] == size)
        normalizers[str(size)] = normalizer(closure((a, b)), (a, b))

    w_solutions = []
    for xx in p_order9:
        yy = mul(inv(xx), inv(z))
        if cycle_type(yy) == (9,) and len(closure((xx, yy))) == 504:
            w_solutions.append((xx, yy))
    worbits = orbits(w_solutions, z)
    diagonal = []
    intrinsic_index = None
    for i, orbit in enumerate(worbits):
        xx, yy = next(iter(orbit))
        diagonal.append(xx in z_class and yy in z_class)
        if (x, y) in orbit:
            intrinsic_index = i

    rx = inv(mul(qb, qa))
    ry = inv(mul(qa, qb))
    rz = inv(mul(rx, ry))
    source_norm = source["quotient_dessin"]["normalizers_in_S9"]
    expected_norm = {
        size: {
            "order": normalizers[size][0],
            "centralizer_order": normalizers[size][1],
            "contains_cycle_type_7_1_1": normalizers[size][2],
        }
        for size in normalizers
    }
    bound_hashes = source["digest_binding"]
    hash_binding_true = all(sha(ROOT / rel) == value for rel, value in bound_hashes.items())

    checks = {
        "schema": source.get("schema") == "c1prime_s4_p5prime/v1",
        "intrinsic_group_order": len(p) == source["window_binding"]["group_order"] == 504,
        "intrinsic_triple": mul(mul(x, y), z) == ID and [order(g) for g in (x, y, z)] == [9, 9, 9],
        # SymPy's product convention and this checker's function-composition
        # convention exchange the first and third branch cycles.
        "intrinsic_explicit_arrays": source["window_binding"]["explicit_XYZ_array_form"] == [list(g) for g in (z, y, x)],
        "diagonal_intrinsic": all(g in z_class for g in (x, y, z)),
        "quotient_words": mul(mul(qa, qb), qc) == ID and qc == y,
        "quotient_distribution": source["quotient_dessin"]["monodromy_order_distribution"] == {str(k): v for k, v in sorted(qdist.items())},
        "quotient_unique_subgroups": source["quotient_dessin"]["unique_generated_subgroups_by_order"]
        == unique_quotient_subgroups == {"81": 1, "324": 1, "504": 1},
        "quotient_unique_orbit": len(quotient) == 24 and len(q504) == 9 and len(qorbits) == 1 and len(qorbits[0]) == 9,
        "normalizers": source_norm == expected_norm,
        "reconstruction": (rx, ry, rz) == (x, y, z),
        "six_w_dessins": len(w_solutions) == 54 and len(worbits) == 6 and all(len(orbit) == 9 for orbit in worbits),
        "unique_diagonal": sum(diagonal) == 1 and intrinsic_index is not None and diagonal[intrinsic_index],
        "p5_symbolic_noncontact": source["p5prime_symbolic_certificate"]["numeric_local_class_read"] is False
        and source["p5prime_symbolic_certificate"]["generated_cyclic_subgroups_equal"] is True,
        "digest_binding": hash_binding_true,
        "noncontact_flags": source.get("u_touched") is False and source.get("c_touched") is False
        and source.get("sealed_k5_touched") is False and source.get("prereg_quantities_untouched") is True,
    }
    result = {
        "schema": "c1prime_s4_p5prime_check/v1",
        "source_run_id": source.get("run_id"),
        "checker": "search/check_c1prime_s4_p5prime_v1.py",
        "helper_disjointness": "standard-library tuple permutations; no SymPy and no producer import; X/Z exchanged under the documented left/right composition transport",
        "recomputed": {
            "p_order": len(p),
            "p_order9_elements": len(p_order9),
            "quotient_solution_distribution": {str(k): v for k, v in sorted(qdist.items())},
            "normalizers": expected_norm,
            "quotient_orbits": [len(orbit) for orbit in qorbits],
            "w_dessin_orbits": [len(orbit) for orbit in worbits],
            "diagonal_flags": diagonal,
        },
        "checks": checks,
        "all_checks_true": all(checks.values()),
        "source_sha256": sha(source_path),
        "producer_sha256": sha(ROOT / "search/c1prime_s4_p5prime_v1.py"),
        "u_touched": False,
        "c_touched": False,
    }
    output = ROOT / args.output
    write(output, result)
    print(json.dumps({
        "all_checks_true": result["all_checks_true"],
        "quotient_orbits": len(qorbits),
        "w_dessin_orbits": len(worbits),
        "diagonal_orbits": sum(diagonal),
    }))
    return 0 if result["all_checks_true"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
