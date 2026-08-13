#!/usr/bin/env python3
"""Official Phase-2b producer for the nonsplit 2^6.PSL(2,8) window.

The reduction image is not formed until the PH2-VOID, nonempty, and
isolatedness gates have all been recorded.  The local u/c payload and the
sealed K5 quantities are never read.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import threading
import time
from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable

from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.free_groups import free_group


ROOT = Path(__file__).resolve().parents[1]
GF8_MOD = 0b1011
P1_GF8 = tuple([(1, value) for value in range(8)] + [(0, 1)])
GENERATOR_NAMES = "abcuvwxyz"
RELATORS: tuple[tuple[tuple[int, int], ...], ...] = (
    ((0, 9),),
    ((1, 9),),
    ((1, -1), (0, 4), (1, -1), (0, 4)),
    ((1, 4), (0, -1), (1, 4), (0, -1)),
    ((1, -1), (0, -2), (1, -1), (0, -1), (1, 1), (0, -1),
     (1, 1), (0, -1), (1, 1), (0, -1), (1, -1), (0, -2)),
    ((1, -2), (0, -2), (1, -2), (0, 2), (1, -1), (0, -1),
     (1, -1), (0, -1), (1, 2), (0, -2)),
    ((1, 1), (0, 1), (1, -1), (0, 1), (1, 1), (0, 1),
     (1, -1), (0, 1), (1, 1), (0, 1), (1, -1), (0, 1),
     (1, 1), (0, -3)),
    ((1, 1), (0, 1), (1, 1), (0, -1), (1, -1), (0, -1),
     (1, -2), (0, 1), (1, 2), (0, -2), (1, -1), (0, 2)),
    ((1, 3), (0, 1), (1, 1), (0, -1), (1, -1), (0, 1),
     (1, 1), (0, -1), (1, -2), (0, 4)),
    ((1, 1), (0, -2), (1, -1), (0, 1), (1, -1), (0, 2),
     (1, -1), (0, 1), (1, -1), (0, 2), (1, -1), (0, -3)),
)


Perm = tuple[int, ...]


def gap_library_path() -> Path:
    return Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / (
        "GAP-4.16.0/runtime/opt/gap-4.16.0/grp/perf5.grp"
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def identity(degree: int) -> Perm:
    return tuple(range(degree))


def mul(left: Perm, right: Perm) -> Perm:
    """Right-action product: apply left, then right."""
    return tuple(right[left[i]] for i in range(len(left)))


def inverse(value: Perm) -> Perm:
    result = [0] * len(value)
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)


def power(value: Perm, exponent: int) -> Perm:
    if exponent < 0:
        return power(inverse(value), -exponent)
    result = identity(len(value))
    while exponent:
        if exponent & 1:
            result = mul(result, value)
        value = mul(value, value)
        exponent //= 2
    return result


def element_order(value: Perm, bound: int = 100000) -> int:
    result = identity(len(value))
    for exponent in range(1, bound + 1):
        result = mul(result, value)
        if result == identity(len(value)):
            return exponent
    raise RuntimeError("element-order bound exceeded")


def closure(generators: Iterable[Perm], degree: int | None = None) -> set[Perm]:
    generators = tuple(generators)
    if degree is None:
        if not generators:
            raise ValueError("degree is needed for an empty generator list")
        degree = len(generators[0])
    one = identity(degree)
    seen = {one}
    queue = deque([one])
    while queue:
        current = queue.popleft()
        for generator in generators:
            nxt = mul(current, generator)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def abstract_prod(items: Iterable[Perm], degree: int) -> Perm:
    result = identity(degree)
    for item in reversed(tuple(items)):
        result = mul(result, item)
    return result


def commutator(left: Perm, right: Perm) -> Perm:
    return mul(mul(mul(inverse(left), inverse(right)), left), right)


def conjugate(value: Perm, by: Perm) -> Perm:
    return mul(mul(inverse(by), value), by)


def normal_closure(seed: Perm, acting_generators: tuple[Perm, ...]) -> set[Perm]:
    subgroup_generators = [seed]
    while True:
        subgroup = closure(subgroup_generators)
        added = None
        for generator in tuple(subgroup_generators):
            for acting in acting_generators:
                for by in (acting, inverse(acting)):
                    candidate = conjugate(generator, by)
                    if candidate not in subgroup:
                        added = candidate
                        break
                if added is not None:
                    break
            if added is not None:
                break
        if added is None:
            return subgroup
        subgroup_generators.append(added)


def build_hom(
    domain_size: int,
    domain_generators: tuple[Perm, ...],
    image_generators: tuple[Perm, ...],
) -> tuple[bool, dict[Perm, Perm]]:
    domain_one = identity(len(domain_generators[0]))
    image_one = identity(len(image_generators[0]))
    mapping = {domain_one: image_one}
    queue = deque([domain_one])
    steps = []
    for domain_generator, image_generator in zip(domain_generators, image_generators):
        steps.extend((
            (domain_generator, image_generator),
            (inverse(domain_generator), inverse(image_generator)),
        ))
    while queue:
        current = queue.popleft()
        current_image = mapping[current]
        for domain_step, image_step in steps:
            nxt = mul(current, domain_step)
            nxt_image = mul(current_image, image_step)
            if nxt in mapping:
                if mapping[nxt] != nxt_image:
                    return False, mapping
            else:
                mapping[nxt] = nxt_image
                queue.append(nxt)
    return len(mapping) == domain_size, mapping


def gf8_mul(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
        if left & 8:
            left ^= GF8_MOD
    return result & 7


def gf8_inv(value: int) -> int:
    if value == 0:
        raise ZeroDivisionError
    return next(candidate for candidate in range(1, 8) if gf8_mul(value, candidate) == 1)


def matrix_line_perm(matrix: tuple[tuple[int, int], tuple[int, int]]) -> Perm:
    images = []
    for left, right in P1_GF8:
        first = gf8_mul(left, matrix[0][0]) ^ gf8_mul(right, matrix[1][0])
        second = gf8_mul(left, matrix[0][1]) ^ gf8_mul(right, matrix[1][1])
        line = (1, gf8_mul(second, gf8_inv(first))) if first else (0, 1)
        images.append(P1_GF8.index(line))
    return tuple(images)


def canonical_p() -> tuple[Perm, Perm, Perm, Perm, set[Perm]]:
    s = matrix_line_perm(((1, 0), (1, 1)))
    t = matrix_line_perm(((4, 3), (1, 5)))
    w = mul(s, inverse(t))
    x = power(w, 2)
    y = mul(mul(inverse(s), x), s)
    return s, t, x, y, closure((x, y))


def perfect_group_action() -> tuple[tuple[Perm, ...], str]:
    F, a, b, c, u, v, w, x, y, z = free_group("a,b,c,u,v,w,x,y,z")
    module = (u, v, w, x, y, z)
    relations = [a**2, b**3, (a * b)**7, b**-1 * (a * b)**3 * c**-1]
    relations.append(
        b**-1 * c**-1 * b * c**-1 * a**-1 * c * b**-1 * c * b * a * (y * z)**-1
    )
    relations.extend(generator**2 for generator in module)
    for i, left in enumerate(module):
        for right in module[i + 1:]:
            relations.append(left**-1 * right**-1 * left * right)
    relations.extend((
        a**-1 * u * a * (u * x)**-1,
        a**-1 * v * a * (v * y)**-1,
        a**-1 * w * a * (w * z)**-1,
        a**-1 * x * a * x**-1,
        a**-1 * y * a * y**-1,
        a**-1 * z * a * z**-1,
        b**-1 * u * b * (x * y)**-1,
        b**-1 * v * b * (y * z)**-1,
        b**-1 * w * b * (x * y * z)**-1,
        b**-1 * x * b * (v * w * x)**-1,
        b**-1 * y * b * (u * v * w * y)**-1,
        b**-1 * z * b * (u * w * z)**-1,
        c**-1 * u * c * v**-1,
        c**-1 * v * c * w**-1,
        c**-1 * w * c * (u * v)**-1,
        c**-1 * x * c * (x * z)**-1,
        c**-1 * y * c * x**-1,
        c**-1 * z * c * y**-1,
    ))
    fp_group = FpGroup(F, relations)
    table = fp_group.coset_enumeration(
        [a * v * w, c, x], strategy="relator_based", max_cosets=500000
    )
    table.compress()
    table.standardize()
    if any(value is None for row in table.table for value in row):
        raise RuntimeError("incomplete coset table")
    action = tuple(
        tuple(int(table.table[row][2 * column]) for row in range(len(table.table)))
        for column in range(9)
    )
    return action, str(fp_group)


def eval_positive_word(word: str, generators: dict[str, Perm]) -> Perm:
    result = identity(len(next(iter(generators.values()))))
    for letter in word:
        result = mul(result, generators[letter])
    return result


def make_quotient(
    group: set[Perm], normal_subgroup: set[Perm]
) -> tuple[list[tuple[Perm, ...]], dict[Perm, int], Callable[[int, int], int]]:
    remaining = set(group)
    cosets = []
    while remaining:
        representative = min(remaining)
        coset = tuple(sorted(mul(value, representative) for value in normal_subgroup))
        cosets.append(coset)
        remaining.difference_update(coset)
    cosets.sort()
    coset_of = {value: index for index, coset in enumerate(cosets) for value in coset}
    representatives = [coset[0] for coset in cosets]

    def quotient_mul(left: int, right: int) -> int:
        return coset_of[mul(representatives[left], representatives[right])]

    return cosets, coset_of, quotient_mul


def quotient_inverse(value: int, one: int, operation: Callable[[int, int], int], size: int) -> int:
    return next(candidate for candidate in range(size) if operation(value, candidate) == one)


def quotient_closure(
    generators: Iterable[int], one: int, operation: Callable[[int, int], int]
) -> set[int]:
    generators = tuple(generators)
    seen = {one}
    queue = deque([one])
    while queue:
        current = queue.popleft()
        for generator in generators:
            nxt = operation(current, generator)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def quotient_to_p_hom(
    quotient_size: int,
    one: int,
    qx: int,
    qy: int,
    operation: Callable[[int, int], int],
    px: Perm,
    py: Perm,
) -> tuple[bool, dict[int, Perm]]:
    qx_inv = quotient_inverse(qx, one, operation, quotient_size)
    qy_inv = quotient_inverse(qy, one, operation, quotient_size)
    steps = ((qx, px), (qx_inv, inverse(px)), (qy, py), (qy_inv, inverse(py)))
    mapping = {one: identity(9)}
    queue = deque([one])
    while queue:
        current = queue.popleft()
        for qstep, pstep in steps:
            nxt = operation(current, qstep)
            image = mul(mapping[current], pstep)
            if nxt in mapping:
                if mapping[nxt] != image:
                    return False, mapping
            else:
                mapping[nxt] = image
                queue.append(nxt)
    return len(mapping) == quotient_size and len(set(mapping.values())) == quotient_size, mapping


def kernel_encountered(left: Perm, right: Perm, kernel: set[Perm]) -> bool:
    one = identity(len(left))
    seen = {one}
    queue = deque([one])
    while queue:
        current = queue.popleft()
        for generator in (left, right):
            nxt = mul(current, generator)
            if nxt in kernel and nxt != one:
                return True
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
            if len(seen) > 504:
                return True
    return False


def eval_relator(relator: tuple[tuple[int, int], ...], x: Perm, y: Perm) -> Perm:
    result = identity(len(x))
    generators = (x, y)
    for index, exponent in relator:
        result = mul(result, power(generators[index], exponent))
    return result


def canonical_relator(relator: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    """Canonicalize a relator up to cyclic rotation and inversion."""
    letters = []
    for index, exponent in relator:
        signed = index + 1 if exponent > 0 else -(index + 1)
        letters.extend([signed] * abs(exponent))
    if not letters:
        return ()
    inverse_letters = [-letter for letter in reversed(letters)]
    candidates = []
    for word in (letters, inverse_letters):
        candidates.extend(tuple(word[offset:] + word[:offset]) for offset in range(len(word)))
    return min(candidates)


def regenerated_marked_presentation(
    x: Perm, y: Perm
) -> tuple[int, tuple[tuple[tuple[int, int], ...], ...]]:
    """Regenerate a strong presentation from the actual finite permutation group."""
    finite_group = PermutationGroup([Permutation(list(x)), Permutation(list(y))])
    presentation = finite_group.presentation()
    generator_index = {str(generator): index for index, generator in enumerate(presentation.generators)}
    normalized = tuple(
        tuple((generator_index[str(generator)], int(exponent)) for generator, exponent in word.array_form)
        for word in presentation.relators
    )
    return int(finite_group.order()), normalized


def scan_shadows(
    elements: list[Perm],
    x: Perm,
    y: Perm,
    generation_test: Callable[[Perm, Perm], bool],
    checkpoint_callback: Callable[[int, dict[str, int]], None] | None = None,
) -> tuple[list[tuple[int, Perm]], dict[str, int | bool]]:
    degree = len(x)
    one = identity(degree)
    group_size = len(elements)
    z = inverse(abstract_prod((x, y), degree))
    theta_ok, theta = build_hom(group_size, (x, y), (y, x))
    tau_ok, tau = build_hom(group_size, (x, y), (y, z))
    if not theta_ok or not tau_ok:
        raise RuntimeError("theta/tau is not well-defined")
    charming = tuple(m for m in range(9) if __import__("math").gcd(2 * m + 1, 9) == 1)
    counters = {
        "candidate_total": len(elements) * len(charming),
        "h10_fail": 0,
        "h11_fail": 0,
        "generation_fail": 0,
    }
    shadows = []
    processed = 0
    for f in elements:
        h10 = abstract_prod((f, theta[f]), degree) == one
        for m in charming:
            processed += 1
            if not h10:
                counters["h10_fail"] += 1
                continue
            ymf = abstract_prod((power(y, m), f), degree)
            tau1 = tau[ymf]
            tau2 = tau[tau1]
            if abstract_prod((tau2, tau1, ymf), degree) != one:
                counters["h11_fail"] += 1
                continue
            exponent = 2 * m + 1
            gen_a = power(x, exponent)
            gen_b = abstract_prod((inverse(f), power(y, exponent), f), degree)
            if not generation_test(gen_a, gen_b):
                counters["generation_fail"] += 1
                continue
            shadows.append((m, f))
        if checkpoint_callback is not None and processed % 12000 < len(charming):
            checkpoint_callback(processed, counters)
    counters["shadow_total"] = len(shadows)
    counters["bookkeeping_identity"] = (
        counters["candidate_total"]
        - counters["h10_fail"]
        - counters["h11_fail"]
        - counters["generation_fail"]
        == len(shadows)
    )
    return shadows, counters


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", default="search/certs/d972_phase2b_nonsplit_v1_20260813.json"
    )
    parser.add_argument(
        "--checkpoint", default="search/certs/d972_phase2b_nonsplit_v1_checkpoint.json"
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    started = time.monotonic()
    state: dict[str, object] = {
        "schema": "d972_phase2b_nonsplit_checkpoint/v1",
        "stage": "start",
        "complete": False,
        "raw_image_size": None,
    }
    atomic_json(checkpoint, state)

    def update(stage: str, **fields: object) -> None:
        state.update(stage=stage, elapsed_ms=int(1000 * (time.monotonic() - started)), **fields)
        atomic_json(checkpoint, state)

    def watchdog() -> None:
        time.sleep(args.hard_timeout_seconds)
        if not state.get("complete"):
            update("hard_timeout")
            os._exit(124)

    threading.Thread(target=watchdog, daemon=True).start()
    try:
        prereg_parent = ROOT / "docs/notes/d972_phase2b_nonsplit_prereg_v1.md"
        prereg = ROOT / "docs/notes/d972_phase2b_nonsplit_prereg_v1_1.md"
        gate_cert = ROOT / "search/certs/d972_phase2b_gate_v1_20260813.json"
        gate_check = ROOT / "search/certs/d972_phase2b_gate_v1_check_20260813.json"
        gate = json.loads(gate_cert.read_text(encoding="utf-8"))
        gate_checker = json.loads(gate_check.read_text(encoding="utf-8"))
        if gate["measurement_performed"] or not gate_checker["all_checks_true"]:
            raise RuntimeError("preflight boundary mismatch")

        original_generators, fp_description = perfect_group_action()
        degree = len(original_generators[0])
        named = dict(zip(GENERATOR_NAMES, original_generators))
        E = closure((named["a"], named["b"]))
        V = closure(tuple(named[name] for name in "uvwxyz"))
        update("G0_library_action", E_order=len(E), degree=degree)

        S = eval_positive_word("accbxbccb", named)
        T = eval_positive_word("cacaccwb", named)
        W = mul(S, inverse(T))
        X = power(W, 2)
        Y = mul(mul(inverse(S), X), S)
        marked_orders = {
            "S": element_order(S), "T": element_order(T), "W": element_order(W),
            "X": element_order(X), "Y": element_order(Y),
        }
        marked_generates = len(closure((X, Y))) == 32256

        normal = all(
            conjugate(module_generator, acting) in V
            for module_generator in tuple(named[name] for name in "uvwxyz")
            for acting in (X, Y, inverse(X), inverse(Y))
        )
        elementary = len(V) == 64 and all(
            value == identity(degree) or element_order(value) == 2 for value in V
        )
        cosets, coset_of, qmul = make_quotient(E, V)
        qone = coset_of[identity(degree)]
        qX, qY, qS, qT = (coset_of[value] for value in (X, Y, S, T))
        quotient_generated = len(quotient_closure((qX, qY), qone, qmul)) == 504

        pS, pT, pX, pY, P = canonical_p()
        quotient_iso_ok, quotient_to_p = quotient_to_p_hom(
            len(cosets), qone, qX, qY, qmul, pX, pY
        )
        marked_pairs = 0
        p_order_distribution = Counter(element_order(value) for value in P)
        for candidate_s in (value for value in P if element_order(value) == 2):
            for candidate_t in (value for value in P if element_order(value) == 3):
                candidate_w = mul(candidate_s, inverse(candidate_t))
                if element_order(candidate_w) != 9:
                    continue
                candidate_x = power(candidate_w, 2)
                candidate_y = mul(mul(inverse(candidate_s), candidate_x), candidate_s)
                if len(closure((candidate_x, candidate_y))) == 504:
                    marked_pairs += 1
        G1 = (
            len(E) == 32256 and degree == 72 and normal and elementary
            and len(cosets) == 504 and quotient_generated and quotient_iso_ok
            and marked_pairs == 1512 and marked_generates
        )
        update("G1_kernel_quotient", raw_boolean=G1, quotient_order=len(cosets))
        if not G1:
            raise RuntimeError("G1 raw boolean is false")

        perfect_closure = normal_closure(commutator(X, Y), (X, Y))
        irreducible_sizes = sorted({
            len(normal_closure(value, (X, Y)))
            for value in V if value != identity(degree)
        })
        lifts_s = [value for value in cosets[qS] if element_order(value) == 2]
        lifts_t = [value for value in cosets[qT] if element_order(value) == 3]
        lift_kernel_bools = [
            kernel_encountered(left, right, V) for left in lifts_s for right in lifts_t
        ]
        nonsplit = (
            len(lifts_s) == 8 and len(lifts_t) == 64
            and len(lift_kernel_bools) == 512 and all(lift_kernel_bools)
        )
        perfect = len(perfect_closure) == len(E)
        irreducible = irreducible_sizes == [64]
        ph2_void_applies = perfect and len(E) == 504
        G2 = perfect and irreducible and nonsplit and not ph2_void_applies
        update("G2_PH2_VOID", raw_boolean=G2, ph2_void_applies=ph2_void_applies)
        if not G2:
            raise RuntimeError("G2 raw boolean is false")

        # A solvable group and a perfect group have no nontrivial common quotient.
        source_common_quotient_trivial = perfect
        source_pure_quotient_order = 2916 * len(E)
        G3 = source_common_quotient_trivial and source_pure_quotient_order == 94058496
        update("G3_source_roof", raw_boolean=G3, source_pure_order=source_pure_quotient_order)
        if not G3:
            raise RuntimeError("G3 raw boolean is false")

        def source_generation(gen_a: Perm, gen_b: Perm) -> bool:
            qa, qb = coset_of[gen_a], coset_of[gen_b]
            return len(quotient_closure((qa, qb), qone, qmul)) == 504

        def source_progress(processed: int, counters: dict[str, int]) -> None:
            update("G4_source_enumeration", processed=processed, counters=dict(counters))

        source_elements = sorted(E)
        source_shadows, source_counts = scan_shadows(
            source_elements, X, Y, source_generation, source_progress
        )
        G4 = len(source_shadows) > 0 and bool(source_counts["bookkeeping_identity"])
        update("G4_nonempty", raw_boolean=G4, source_shadow_count=len(source_shadows))
        if not G4:
            raise RuntimeError("G4 raw boolean is false")

        original_relations_hold = all(
            eval_relator(relator, X, Y) == identity(degree) for relator in RELATORS
        )
        presentation_order, regenerated_relators = regenerated_marked_presentation(X, Y)
        presentation_matches_frozen = (
            {canonical_relator(relator) for relator in regenerated_relators}
            == {canonical_relator(relator) for relator in RELATORS}
        )
        update(
            "G5_marked_presentation", presentation_order=presentation_order,
            presentation_matches_frozen=presentation_matches_frozen
        )
        settled = []
        frozen_regression = []
        quotient_surjective = []
        regenerated_relations_hold_in_E = all(
            eval_relator(relator, X, Y) == identity(degree)
            for relator in regenerated_relators
        )
        for m, f in source_shadows:
            exponent = 2 * m + 1
            image_x = power(X, exponent)
            image_y = abstract_prod((inverse(f), power(Y, exponent), f), degree)
            relations_hold = all(
                eval_relator(relator, image_x, image_y) == identity(degree)
                for relator in regenerated_relators
            )
            frozen_relations_hold = all(
                eval_relator(relator, image_x, image_y) == identity(degree)
                for relator in RELATORS
            )
            q_surj = source_generation(image_x, image_y)
            quotient_surjective.append(q_surj)
            frozen_regression.append(frozen_relations_hold)
            settled.append(relations_hold and q_surj and nonsplit and irreducible)
        isolated_NE = (
            regenerated_relations_hold_in_E and presentation_order == len(E)
            and len(settled) == len(source_shadows) and all(settled)
        )
        isolated_intersection = isolated_NE
        G5 = isolated_NE and isolated_intersection
        update("G5_isolated", raw_boolean=G5, settled_count=sum(settled))
        if not G5:
            raise RuntimeError("G5 raw boolean is false")

        # Measurement boundary: no reduction image set was formed above this line.
        update("measurement_authorized", G0_to_G5_all_true=True)

        p_elements = sorted(P)
        p_index = {value: index for index, value in enumerate(p_elements)}

        def target_generation(gen_a: Perm, gen_b: Perm) -> bool:
            return len(closure((gen_a, gen_b))) == 504

        target_shadows, target_counts = scan_shadows(p_elements, pX, pY, target_generation)
        target_keys = {(m, p_index[f]) for m, f in target_shadows}
        reduced_keys = {
            (m, p_index[quotient_to_p[coset_of[f]]]) for m, f in source_shadows
        }
        reduction_subset = reduced_keys <= target_keys
        reduced_candidate_count = len(reduced_keys)
        raw_image_size = 18 * reduced_candidate_count
        source_roof_shadow_count = 18 * len(source_shadows)
        target_roof_shadow_count = 18 * len(target_shadows)
        if raw_image_size == 324:
            branch = {
                "raw_value": 324,
                "status": "finite-A-side-certificate-stored",
                "finite_depth_B_type_recognition": False,
            }
        elif raw_image_size == 972:
            branch = {
                "raw_value": 972,
                "status": "UNKNOWN",
                "candidate_exhausted": True,
                "finite_depth_B_type_recognition": False,
            }
        else:
            branch = {
                "raw_value": raw_image_size,
                "status": "uninterpreted-outside-frozen-spectrum",
                "finite_depth_B_type_recognition": False,
            }
        update("measurement_complete", raw_image_size=raw_image_size)

        source_index = {value: index for index, value in enumerate(source_elements)}
        now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        library = gap_library_path()
        inputs = (prereg_parent, prereg, gate_cert, gate_check, library)
        cert = {
            "schema": "d972_phase2b_nonsplit/v1",
            "run_id": f"d972-phase2b-nonsplit-{now}",
            "generated_by": {
                "script": "search/d972_phase2b_nonsplit_v1.py",
                "tool": "Python 3.13 + SymPy 1.14",
            },
            "preregistration": {
                "path": "docs/notes/d972_phase2b_nonsplit_prereg_v1_1.md",
                "sha256": sha256(prereg),
                "parent_path": "docs/notes/d972_phase2b_nonsplit_prereg_v1.md",
                "parent_sha256": sha256(prereg_parent),
                "engineering_probe_before_freeze": True,
                "preregistration_blind": False,
                "frozen_spectrum": [324, 972],
            },
            "execution_order": {
                "G0_library_action": True,
                "G1_kernel_quotient": G1,
                "G2_PH2_VOID": G2,
                "G3_source_roof": G3,
                "G4_nonempty_before_measurement": G4,
                "G5_isolated_before_measurement": G5,
                "reduction_image_formed_only_after_G5": True,
            },
            "candidate": {
                "library_id": "PerfectGroup(32256,2)",
                "library_label": "L2(8) N 2^6",
                "library_sha256": sha256(library),
                "coset_degree": degree,
                "order": len(E),
                "V_order": len(V),
                "quotient_order": len(cosets),
                "fp_description_sha256": hashlib.sha256(fp_description.encode()).hexdigest(),
                "original_generator_arrays": {
                    name: list(value) for name, value in zip(GENERATOR_NAMES, original_generators)
                },
                "selected_words": {"S": "accbxbccb", "T": "cacaccwb"},
                "selected_arrays": {
                    "S": list(S), "T": list(T), "X": list(X), "Y": list(Y)
                },
                "marked_orders": marked_orders,
                "marked_generates_E": marked_generates,
            },
            "G1_receipt": {
                "V_normal": normal,
                "V_elementary_abelian": elementary,
                "quotient_generated_by_marking": quotient_generated,
                "quotient_marked_isomorphism_to_canonical_P": quotient_iso_ok,
                "canonical_P_order_distribution": {
                    str(key): value for key, value in sorted(p_order_distribution.items())
                },
                "canonical_marked_pair_count": marked_pairs,
            },
            "G2_receipt": {
                "E_perfect": perfect,
                "commutator_normal_closure_order": len(perfect_closure),
                "V_irreducible": irreducible,
                "nonzero_vector_normal_closure_orders": irreducible_sizes,
                "fixed_qS_order2_lift_count": len(lifts_s),
                "fixed_qT_order3_lift_count": len(lifts_t),
                "lift_pairs_checked": len(lift_kernel_bools),
                "all_lift_pairs_have_nontrivial_kernel": all(lift_kernel_bools),
                "extension_nonsplit": nonsplit,
                "PH2_VOID_applies": ph2_void_applies,
                "solvable_direct_PSL_factorization": False,
            },
            "G3_receipt": {
                "G9_solvable": True,
                "E_perfect": perfect,
                "nontrivial_common_quotient_exists": False,
                "source_pure_quotient": "G9 direct-product E",
                "source_pure_quotient_order": source_pure_quotient_order,
            },
            "source_scan": {
                **source_counts,
                "shadow_records_m_findex": [
                    [m, source_index[f]] for m, f in source_shadows
                ],
            },
            "isolatedness": {
                "marked_relators": [
                    [[index, exponent] for index, exponent in relator] for relator in RELATORS
                ],
                "marked_relator_count": len(RELATORS),
                "marked_relations_hold_in_E": original_relations_hold,
                "marked_relations_hold_for_all_source_images": all(frozen_regression),
                "marked_presentation_order": presentation_order,
                "strong_presentation_regenerated_from_finite_group": True,
                "regenerated_relators_equal_frozen_relators": presentation_matches_frozen,
                "regenerated_relators": [
                    [[index, exponent] for index, exponent in relator]
                    for relator in regenerated_relators
                ],
                "regenerated_relations_hold_in_E": regenerated_relations_hold_in_E,
                "load_bearing_relator_source": "run-regenerated strong presentation",
                "settled_count": sum(settled),
                "all_source_shadow_images_quotient_surjective": all(quotient_surjective),
                "N_E_isolated": isolated_NE,
                "K9_intersection_N_E_isolated": isolated_intersection,
            },
            "measurement": {
                "target_NS4_shadow_count": len(target_shadows),
                "target_scan": target_counts,
                "source_roof_shadow_count": source_roof_shadow_count,
                "target_roof_shadow_count": target_roof_shadow_count,
                "reduced_candidate_shadow_count": reduced_candidate_count,
                "reduced_keys_m_pindex": [list(row) for row in sorted(reduced_keys)],
                "target_keys_m_pindex": [list(row) for row in sorted(target_keys)],
                "reduction_subset_of_target": reduction_subset,
                "K9_fibre_per_candidate_shadow": 18,
                "raw_image_size": raw_image_size,
                "branch": branch,
            },
            "model_boundary": {
                "old_product_family_PH2_VOID_applied_first": True,
                "new_candidate_nonempty_before_measurement": True,
                "finite_depth_B_type_recognition": False,
                "status": branch["status"],
                "grade": "cross-checked candidate after independent checker only",
            },
            "input_sha256": {
                (str(path.relative_to(ROOT)).replace("\\", "/") if path.is_relative_to(ROOT)
                 else str(path)): sha256(path)
                for path in inputs
            },
            "elapsed_ms": int(1000 * (time.monotonic() - started)),
            "u_touched": False,
            "c_touched": False,
            "sealed_k5_touched": False,
            "preregistered_quantities_changed": False,
        }
        atomic_json(output, cert)
        update(
            "complete", complete=True, output=args.output, run_id=cert["run_id"],
            raw_image_size=raw_image_size
        )
        print(json.dumps({
            "run_id": cert["run_id"],
            "source_shadows": len(source_shadows),
            "target_shadows": len(target_shadows),
            "settled": sum(settled),
            "raw_image_size": raw_image_size,
            "status": branch["status"],
        }, sort_keys=True))
        return 0
    except Exception as exc:
        update("error", error=repr(exc))
        raise


if __name__ == "__main__":
    raise SystemExit(main())
