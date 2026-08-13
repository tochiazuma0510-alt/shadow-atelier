#!/usr/bin/env python3
"""Helper-disjoint checker for the Phase-2b nonsplit certificate.

Only standard-library tuple permutations are used.  In particular, the
producer's SymPy presentation helper is not imported: all 432 candidate
endomorphisms are checked by synchronized Cayley-graph traversal.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import threading
import time
from collections import Counter, deque
from pathlib import Path
from typing import Callable, Iterable


ROOT = Path(__file__).resolve().parents[1]
GF8_MOD = 0b1011
P1 = tuple([(1, value) for value in range(8)] + [(0, 1)])
NAMES = "abcuvwxyz"
Perm = tuple[int, ...]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def one(degree: int) -> Perm:
    return tuple(range(degree))


def compose(first: Perm, second: Perm) -> Perm:
    return tuple(second[first[index]] for index in range(len(first)))


def invert(value: Perm) -> Perm:
    result = [0] * len(value)
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)


def exp(value: Perm, exponent: int) -> Perm:
    if exponent < 0:
        return exp(invert(value), -exponent)
    result = one(len(value))
    while exponent:
        if exponent & 1:
            result = compose(result, value)
        value = compose(value, value)
        exponent >>= 1
    return result


def order(value: Perm, limit: int = 100000) -> int:
    current = one(len(value))
    for exponent in range(1, limit + 1):
        current = compose(current, value)
        if current == one(len(value)):
            return exponent
    raise RuntimeError("order limit")


def generated(generators: Iterable[Perm], degree: int | None = None) -> set[Perm]:
    generators = tuple(generators)
    if degree is None:
        degree = len(generators[0])
    identity = one(degree)
    result = {identity}
    queue = deque([identity])
    while queue:
        value = queue.popleft()
        for generator in generators:
            nxt = compose(value, generator)
            if nxt not in result:
                result.add(nxt)
                queue.append(nxt)
    return result


def paper_product(values: Iterable[Perm], degree: int) -> Perm:
    result = one(degree)
    for value in reversed(tuple(values)):
        result = compose(result, value)
    return result


def conj(value: Perm, acting: Perm) -> Perm:
    return compose(compose(invert(acting), value), acting)


def comm(left: Perm, right: Perm) -> Perm:
    return compose(compose(compose(invert(left), invert(right)), left), right)


def normal_generated(seed: Perm, actors: tuple[Perm, ...]) -> set[Perm]:
    basis = [seed]
    while True:
        subgroup = generated(basis)
        extra = None
        for basis_value in tuple(basis):
            for actor in actors:
                for direction in (actor, invert(actor)):
                    candidate = conj(basis_value, direction)
                    if candidate not in subgroup:
                        extra = candidate
                        break
                if extra is not None:
                    break
            if extra is not None:
                break
        if extra is None:
            return subgroup
        basis.append(extra)


def word_value(word: str, named: dict[str, Perm]) -> Perm:
    result = one(len(next(iter(named.values()))))
    for letter in word:
        result = compose(result, named[letter])
    return result


def gf_mul(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
        if left & 8:
            left ^= GF8_MOD
    return result & 7


def gf_inv(value: int) -> int:
    return next(candidate for candidate in range(1, 8) if gf_mul(value, candidate) == 1)


def matrix_action(matrix: tuple[tuple[int, int], tuple[int, int]]) -> Perm:
    result = []
    for left, right in P1:
        a = gf_mul(left, matrix[0][0]) ^ gf_mul(right, matrix[1][0])
        b = gf_mul(left, matrix[0][1]) ^ gf_mul(right, matrix[1][1])
        line = (1, gf_mul(b, gf_inv(a))) if a else (0, 1)
        result.append(P1.index(line))
    return tuple(result)


def canonical_group() -> tuple[Perm, Perm, Perm, Perm, set[Perm]]:
    s = matrix_action(((1, 0), (1, 1)))
    t = matrix_action(((4, 3), (1, 5)))
    w = compose(s, invert(t))
    x = exp(w, 2)
    y = compose(compose(invert(s), x), s)
    return s, t, x, y, generated((x, y))


def quotient_data(
    group: set[Perm], kernel: set[Perm]
) -> tuple[list[tuple[Perm, ...]], dict[Perm, int], Callable[[int, int], int]]:
    pending = set(group)
    cosets = []
    while pending:
        representative = min(pending)
        coset = tuple(sorted(compose(value, representative) for value in kernel))
        cosets.append(coset)
        pending.difference_update(coset)
    cosets.sort()
    which = {value: index for index, coset in enumerate(cosets) for value in coset}
    representatives = [coset[0] for coset in cosets]

    def operation(left: int, right: int) -> int:
        return which[compose(representatives[left], representatives[right])]

    return cosets, which, operation


def q_generated(gens: Iterable[int], identity: int, operation: Callable[[int, int], int]) -> set[int]:
    gens = tuple(gens)
    result = {identity}
    queue = deque([identity])
    while queue:
        value = queue.popleft()
        for generator in gens:
            nxt = operation(value, generator)
            if nxt not in result:
                result.add(nxt)
                queue.append(nxt)
    return result


def q_inverse(value: int, identity: int, operation: Callable[[int, int], int], size: int) -> int:
    return next(candidate for candidate in range(size) if operation(value, candidate) == identity)


def q_to_p(
    size: int, identity: int, qx: int, qy: int, operation: Callable[[int, int], int],
    px: Perm, py: Perm
) -> tuple[bool, dict[int, Perm]]:
    steps = (
        (qx, px), (q_inverse(qx, identity, operation, size), invert(px)),
        (qy, py), (q_inverse(qy, identity, operation, size), invert(py)),
    )
    mapping = {identity: one(9)}
    queue = deque([identity])
    while queue:
        value = queue.popleft()
        for qstep, pstep in steps:
            nxt = operation(value, qstep)
            image = compose(mapping[value], pstep)
            if nxt in mapping:
                if mapping[nxt] != image:
                    return False, mapping
            else:
                mapping[nxt] = image
                queue.append(nxt)
    return len(mapping) == size and len(set(mapping.values())) == size, mapping


def has_kernel_element(left: Perm, right: Perm, kernel: set[Perm]) -> bool:
    identity = one(len(left))
    result = {identity}
    queue = deque([identity])
    while queue:
        value = queue.popleft()
        for generator in (left, right):
            nxt = compose(value, generator)
            if nxt in kernel and nxt != identity:
                return True
            if nxt not in result:
                result.add(nxt)
                queue.append(nxt)
            if len(result) > 504:
                return True
    return False


def hom_table(
    group_size: int, domain_gens: tuple[Perm, Perm], image_gens: tuple[Perm, Perm]
) -> tuple[bool, dict[Perm, Perm]]:
    d_one = one(len(domain_gens[0]))
    i_one = one(len(image_gens[0]))
    result = {d_one: i_one}
    queue = deque([d_one])
    steps = (
        (domain_gens[0], image_gens[0]),
        (invert(domain_gens[0]), invert(image_gens[0])),
        (domain_gens[1], image_gens[1]),
        (invert(domain_gens[1]), invert(image_gens[1])),
    )
    while queue:
        value = queue.popleft()
        for d_step, i_step in steps:
            nxt = compose(value, d_step)
            image = compose(result[value], i_step)
            if nxt in result:
                if result[nxt] != image:
                    return False, result
            else:
                result[nxt] = image
                queue.append(nxt)
    return len(result) == group_size, result


def scan(
    elements: list[Perm], x: Perm, y: Perm, generation: Callable[[Perm, Perm], bool]
) -> tuple[list[tuple[int, Perm]], dict[str, int | bool]]:
    degree = len(x)
    identity = one(degree)
    z = invert(paper_product((x, y), degree))
    theta_ok, theta = hom_table(len(elements), (x, y), (y, x))
    tau_ok, tau = hom_table(len(elements), (x, y), (y, z))
    if not theta_ok or not tau_ok:
        raise RuntimeError("theta/tau")
    charming = (0, 2, 3, 5, 6, 8)
    counters: dict[str, int | bool] = {
        "candidate_total": len(elements) * 6,
        "h10_fail": 0, "h11_fail": 0, "generation_fail": 0,
    }
    shadows = []
    for f in elements:
        h10 = paper_product((f, theta[f]), degree) == identity
        for m in charming:
            if not h10:
                counters["h10_fail"] += 1
                continue
            ymf = paper_product((exp(y, m), f), degree)
            tau1 = tau[ymf]
            tau2 = tau[tau1]
            if paper_product((tau2, tau1, ymf), degree) != identity:
                counters["h11_fail"] += 1
                continue
            u = 2 * m + 1
            ga = exp(x, u)
            gb = paper_product((invert(f), exp(y, u), f), degree)
            if not generation(ga, gb):
                counters["generation_fail"] += 1
                continue
            shadows.append((m, f))
    counters["shadow_total"] = len(shadows)
    counters["bookkeeping_identity"] = (
        counters["candidate_total"] - counters["h10_fail"] - counters["h11_fail"]
        - counters["generation_fail"] == len(shadows)
    )
    return shadows, counters


def relation_value(raw_relation: list[list[int]], x: Perm, y: Perm) -> Perm:
    result = one(len(x))
    generators = (x, y)
    for index, exponent in raw_relation:
        result = compose(result, exp(generators[index], exponent))
    return result


def right_transition(elements: list[Perm], index: dict[Perm, int], step: Perm) -> tuple[list[int], list[int]]:
    forward = [index[compose(value, step)] for value in elements]
    backward = [0] * len(forward)
    for start, end in enumerate(forward):
        backward[end] = start
    return forward, backward


def synchronized_automorphism_checks(
    elements: list[Perm], x: Perm, y: Perm, shadow_images: list[tuple[Perm, Perm]],
    progress: Callable[[int], None]
) -> tuple[int, int]:
    index = {value: i for i, value in enumerate(elements)}
    identity_index = index[one(len(x))]
    x_forward, x_backward = right_transition(elements, index, x)
    y_forward, y_backward = right_transition(elements, index, y)
    domain_transitions = (x_forward, x_backward, y_forward, y_backward)
    first_cache: dict[Perm, tuple[list[int], list[int]]] = {}
    well_defined = 0
    bijective = 0
    size = len(elements)
    for number, (image_x, image_y) in enumerate(shadow_images, 1):
        if image_x not in first_cache:
            first_cache[image_x] = right_transition(elements, index, image_x)
        ix_forward, ix_backward = first_cache[image_x]
        iy_forward, iy_backward = right_transition(elements, index, image_y)
        image_transitions = (ix_forward, ix_backward, iy_forward, iy_backward)
        mapping = [-1] * size
        mapping[identity_index] = identity_index
        queue = [identity_index]
        cursor = 0
        consistent = True
        while cursor < len(queue) and consistent:
            domain_value = queue[cursor]
            cursor += 1
            image_value = mapping[domain_value]
            for d_transition, i_transition in zip(domain_transitions, image_transitions):
                d_next = d_transition[domain_value]
                i_next = i_transition[image_value]
                if mapping[d_next] == -1:
                    mapping[d_next] = i_next
                    queue.append(d_next)
                elif mapping[d_next] != i_next:
                    consistent = False
                    break
        if consistent and len(queue) == size:
            well_defined += 1
            if len(set(mapping)) == size:
                bijective += 1
        if number % 24 == 0 or number == len(shadow_images):
            progress(number)
    return well_defined, bijective


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", default="search/certs/d972_phase2b_nonsplit_v1_20260813.json"
    )
    parser.add_argument(
        "--output", default="search/certs/d972_phase2b_nonsplit_v1_check_20260813.json"
    )
    parser.add_argument(
        "--checkpoint", default="search/certs/d972_phase2b_nonsplit_v1_check_checkpoint.json"
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    source_path = ROOT / args.input
    output_path = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    started = time.monotonic()
    state: dict[str, object] = {
        "schema": "d972_phase2b_nonsplit_check_checkpoint/v1",
        "stage": "start", "complete": False,
    }
    write_json(checkpoint, state)

    def update(stage: str, **fields: object) -> None:
        state.update(stage=stage, elapsed_ms=int(1000 * (time.monotonic() - started)), **fields)
        write_json(checkpoint, state)

    def timeout() -> None:
        time.sleep(args.hard_timeout_seconds)
        if not state.get("complete"):
            update("hard_timeout")
            os._exit(124)

    threading.Thread(target=timeout, daemon=True).start()
    try:
        source = json.loads(source_path.read_text(encoding="utf-8"))
        named = {
            name: tuple(source["candidate"]["original_generator_arrays"][name]) for name in NAMES
        }
        E = generated((named["a"], named["b"]))
        V = generated(tuple(named[name] for name in "uvwxyz"))
        S = word_value(source["candidate"]["selected_words"]["S"], named)
        T = word_value(source["candidate"]["selected_words"]["T"], named)
        W = compose(S, invert(T))
        X = exp(W, 2)
        Y = compose(compose(invert(S), X), S)
        selected_arrays_match = all(
            tuple(source["candidate"]["selected_arrays"][name]) == value
            for name, value in (("S", S), ("T", T), ("X", X), ("Y", Y))
        )
        update("reconstructed_group", E_order=len(E), V_order=len(V))

        normal = all(
            conj(named[module_name], actor) in V
            for module_name in "uvwxyz" for actor in (X, Y, invert(X), invert(Y))
        )
        elementary = len(V) == 64 and all(value == one(72) or order(value) == 2 for value in V)
        cosets, which, qop = quotient_data(E, V)
        qone = which[one(72)]
        qX, qY, qS, qT = (which[value] for value in (X, Y, S, T))
        pS, pT, pX, pY, P = canonical_group()
        iso_ok, iso = q_to_p(504, qone, qX, qY, qop, pX, pY)
        p_distribution = Counter(order(value) for value in P)
        marked_pairs = 0
        for ps in (value for value in P if order(value) == 2):
            for pt in (value for value in P if order(value) == 3):
                pw = compose(ps, invert(pt))
                if order(pw) == 9:
                    px = exp(pw, 2)
                    py = compose(compose(invert(ps), px), ps)
                    if len(generated((px, py))) == 504:
                        marked_pairs += 1

        perfect_order = len(normal_generated(comm(X, Y), (X, Y)))
        irreducible_orders = sorted({
            len(normal_generated(value, (X, Y))) for value in V if value != one(72)
        })
        s_lifts = [value for value in cosets[qS] if order(value) == 2]
        t_lifts = [value for value in cosets[qT] if order(value) == 3]
        kernel_bools = [
            has_kernel_element(left, right, V) for left in s_lifts for right in t_lifts
        ]
        update("structural_gates", lift_pairs=len(kernel_bools))

        def source_generation(ga: Perm, gb: Perm) -> bool:
            return len(q_generated((which[ga], which[gb]), qone, qop)) == 504

        elements = sorted(E)
        source_shadows, source_counts = scan(elements, X, Y, source_generation)
        source_index = {value: index for index, value in enumerate(elements)}
        source_records = [[m, source_index[f]] for m, f in source_shadows]
        update("source_rescan", source_shadows=len(source_shadows))

        frozen_relators = source["isolatedness"]["marked_relators"]
        run_relators = source["isolatedness"]["regenerated_relators"]
        frozen_all = True
        run_all = True
        shadow_images = []
        for m, f in source_shadows:
            u = 2 * m + 1
            image_x = exp(X, u)
            image_y = paper_product((invert(f), exp(Y, u), f), 72)
            shadow_images.append((image_x, image_y))
            frozen_all = frozen_all and all(
                relation_value(relator, image_x, image_y) == one(72)
                for relator in frozen_relators
            )
            run_all = run_all and all(
                relation_value(relator, image_x, image_y) == one(72)
                for relator in run_relators
            )

        def direct_progress(processed: int) -> None:
            update("direct_cayley_checks", processed=processed, total=len(shadow_images))

        direct_well_defined, direct_bijective = synchronized_automorphism_checks(
            elements, X, Y, shadow_images, direct_progress
        )
        update(
            "direct_cayley_complete", well_defined=direct_well_defined,
            bijective=direct_bijective
        )

        p_elements = sorted(P)
        p_index = {value: index for index, value in enumerate(p_elements)}

        def target_generation(ga: Perm, gb: Perm) -> bool:
            return len(generated((ga, gb))) == 504

        target_shadows, target_counts = scan(p_elements, pX, pY, target_generation)
        target_keys = {(m, p_index[f]) for m, f in target_shadows}
        reduced_keys = {(m, p_index[iso[which[f]]]) for m, f in source_shadows}
        raw = 18 * len(reduced_keys)

        input_hashes = True
        for path_text, expected in source["input_sha256"].items():
            path = Path(path_text)
            if not path.is_absolute():
                path = ROOT / path
            input_hashes = input_hashes and digest(path) == expected

        checks = {
            "schema": source.get("schema") == "d972_phase2b_nonsplit/v1",
            "source_digest_readable": digest(source_path) == digest(source_path),
            "bound_input_hashes": input_hashes,
            "selected_arrays": selected_arrays_match,
            "group_orders": len(E) == 32256 and len(V) == 64 and len(cosets) == 504,
            "kernel_structure": normal and elementary,
            "quotient_marking": iso_ok and len(q_generated((qX, qY), qone, qop)) == 504,
            "canonical_P": len(P) == 504 and marked_pairs == 1512,
            "canonical_P_distribution": {
                str(key): value for key, value in sorted(p_distribution.items())
            } == source["G1_receipt"]["canonical_P_order_distribution"],
            "perfect_irreducible": perfect_order == 32256 and irreducible_orders == [64],
            "nonsplit_lift_census": (
                len(s_lifts) == 8 and len(t_lifts) == 64
                and len(kernel_bools) == 512 and all(kernel_bools)
            ),
            "PH2_VOID_raw_boolean": not source["G2_receipt"]["PH2_VOID_applies"],
            "source_scan": source_counts == {
                key: source["source_scan"][key] for key in source_counts
            } and source_records == source["source_scan"]["shadow_records_m_findex"],
            "nonempty_before_measurement": len(source_shadows) > 0,
            "frozen_relator_regression": frozen_all,
            "run_relators": run_all,
            "direct_well_defined_all": direct_well_defined == len(source_shadows) == 432,
            "direct_bijective_all": direct_bijective == len(source_shadows) == 432,
            "isolated_receipt": source["isolatedness"]["N_E_isolated"],
            "target_scan": target_counts == source["measurement"]["target_scan"],
            "reduction_keys": (
                [list(row) for row in sorted(reduced_keys)]
                == source["measurement"]["reduced_keys_m_pindex"]
            ),
            "target_keys": (
                [list(row) for row in sorted(target_keys)]
                == source["measurement"]["target_keys_m_pindex"]
            ),
            "raw_image": raw == source["measurement"]["raw_image_size"],
            "frozen_spectrum": source["preregistration"]["frozen_spectrum"] == [324, 972],
            "unknown_boundary": (
                source["measurement"]["branch"]["status"] == "UNKNOWN"
                and not source["measurement"]["branch"]["finite_depth_B_type_recognition"]
            ),
            "execution_order": all(source["execution_order"].values()),
            "noncontact": (
                not source["u_touched"] and not source["c_touched"]
                and not source["sealed_k5_touched"]
                and not source["preregistered_quantities_changed"]
            ),
        }
        result = {
            "schema": "d972_phase2b_nonsplit_check/v1",
            "checker": "search/check_d972_phase2b_nonsplit_v1.py",
            "helper_disjointness": (
                "Python standard-library tuple permutations; no SymPy and no producer import; "
                "all source endomorphisms checked by synchronized Cayley traversal"
            ),
            "source_run_id": source["run_id"],
            "source_sha256": digest(source_path),
            "checks": checks,
            "all_checks_true": all(checks.values()),
            "recomputed": {
                "E_order": len(E), "V_order": len(V), "quotient_order": len(cosets),
                "source_shadow_count": len(source_shadows),
                "direct_well_defined": direct_well_defined,
                "direct_bijective": direct_bijective,
                "target_shadow_count": len(target_shadows),
                "reduced_candidate_count": len(reduced_keys),
                "raw_image_size": raw,
            },
            "producer_sha256": digest(ROOT / "search/d972_phase2b_nonsplit_v1.py"),
            "elapsed_ms": int(1000 * (time.monotonic() - started)),
            "u_touched": False,
            "c_touched": False,
            "sealed_k5_touched": False,
        }
        write_json(output_path, result)
        update(
            "complete", complete=True, output=args.output,
            all_checks_true=result["all_checks_true"], raw_image_size=raw
        )
        print(json.dumps({
            "all_checks_true": result["all_checks_true"],
            "direct_bijective": direct_bijective,
            "source_shadows": len(source_shadows),
            "raw_image_size": raw,
        }, sort_keys=True))
        return 0 if result["all_checks_true"] else 1
    except Exception as exc:
        update("error", error=repr(exc))
        raise


if __name__ == "__main__":
    raise SystemExit(main())
