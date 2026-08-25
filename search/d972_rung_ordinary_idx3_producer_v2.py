#!/usr/bin/env python3
"""Prepare and, only after an explicit mode freeze, evaluate the first fair C3 shell.

The prepare path authenticates the complete LINS normal-node export, closes the
degree-2/3 core shell, reconstructs the marked K1/C3 joint quotient, and emits
the complete raw reduction fibre above frozen D972 row 36.  It deliberately
does not call the shadow predicate.

The execute path is hard-gated by an immutable parent-issued mode token.  It
evaluates the registered 48 points only; it has no special-pentagon or Dpap
branch.  This v2 compatibility repair rebinds the current launch-task pin and rechecks
all immutable inputs again at execute entry.  It is producer-only and must never
be imported by the independently authored checker.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
import hashlib
import json
import math
from pathlib import Path
from typing import Callable, Iterable, TypeVar


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REL = "search/d972_rung_ordinary_idx3_producer_v2.py"
PREREG_REL = "search/certs/d972_rung_ordinary_idx3_prereg_v2_20260824.json"
LAUNCH_MANIFEST_REL = "search/certs/d972_rung_ordinary_idx3_launch_manifest_v2_20260824.json"

NODE_ID = "16437e56512d99ab2c7ca8328293863fe6b7792504ebd592fa21da9d7952bc37"
NODE_SOURCE_DIGEST = "c6f20bd5c6edc071c48a6ecd10f09e0dcfd0ef232bfa0ee7d3bf4aba45a60158"
MODE = "ORDINARY_FAIR_SHELL_FIRST"

TARGET_ROW_INDEX = 36
TARGET_KEY = [0, [[4, 0], [5, 0], [0, 0]], [1, 2, 3, 4, 5, 6, 7, 8, 9]]
TARGET_WORD = [-2, -2, -1, -1, 2, 2, 1, -2, -1, -1, 2, 2, 2, -1, -2, -2, 1, 1, 1, 1]
TARGET_FULL_ROW = [0, TARGET_KEY, TARGET_WORD]
TARGET_DIGESTS = {
    "full_row_compact_sha256": "31d19295b8b5c2f5e36387f6bb63cec508a7b8770e30bfa6d02909b1f16f4cd8",
    "target_key_compact_sha256": "3940557ee6c0118f2563ff7d19a41059d0fcdd5c7c876bc56c84b4fa9ae242ac",
    "word_compact_sha256": "b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d",
}

ROSTER_DIGESTS = {
    "seed_pool_432": {
        "definition": "X \\ (IDX3-NN-09 union IDX3-NN-12)",
        "count": 432,
        "row_index_list_sha256": "99acd3ce41ff6e2d1a6430abea3de0bfb7ee1e82fa825da9118cbd0714339d36",
        "canonical_key_list_sha256": "ab3c1867a11b5f425b55c40d2582ca586b8774f4b282a69addd763a26abd105b",
    },
    "symdiff_432": {
        "definition": "IDX3-NN-09 symmetric_difference IDX3-NN-12",
        "count": 432,
        "row_index_list_sha256": "29f65cd6951bb0f3c19f4982b4f0be4b6e6841f990f8a96a6f1b235495de2e81",
        "canonical_key_list_sha256": "263d3d57fc179406b6d146dac52f31f312c7c27a2e879cfcd4ec9aba4671e0ab",
    },
}

EXPECTED = {
    "ops/inbox_codex/sol_task_159o_ladder_launch.txt": (2829, "aa234d0a4ce138aa3e8c8de24c37a601cc8169a9f75d7d04cfc7f0b6d4e16b84"),
    "sol/luna_task_159o_ladder_launch.md": (12324, "08be5089fcedd8232b39feb3e7491a83b3dad001ca4c2be122491c5acc7dc85a"),
    "scratchpad/d972_idx3_arith_datum_independent_v1.md": (96640, "a2fae0a0365a8f1587781c797120a25532b6d274dedc609bad11c0c22082e31a"),
    "papers/2401.06870-gt-shadows-gentle-version.pdf": (500548, "4e0a29e19825810eb9db24ebda120a6805c42fee4eb51679d409c5437e0943ab"),
    "ci/lins_marked_artifacts_32626064970/lins_marked_export/lins_marked_strictness_export_v1_20260823.json": (51546606, "9fa4fff101d641688b858550e77e3543d7461bc00d149470b81dfdce91fa8324"),
    "search/certs/lins_census_2000_v1_20260811.json": (3395546, "d0832df8a4e61adff45c5c24c8eba32f5d388f55412907ed5ffdf714b2b4b958"),
    "search/lins_marked_strictness_export_v1.g": (14064, "74924dd639470a48d94770578c9ae9b5e22657483461f2063632150948979ec1"),
    "certificates/K36.v1.json": (727834, "feac2a0202e5b78a017272a972e105ac7daf7eb5ca0b4de102b6664b098d8719"),
    "crosscheck/verdicts/K36.v1.verdict.json": (71093, "4436da2643a0577b06761cd310f0032d98fefe67bab10c16f74c534aabb1a92b"),
    "certificates/K9.v1.json": (173224, "ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e"),
    "crosscheck/verdicts/K9.v1.verdict.json": (20991, "9c299baba6cd3c49296621ecfe5efbc260d7971fa874f44465fa5e968cc065f9"),
    "certificates/S4.v2.json": (287984, "c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d"),
    "crosscheck/verdicts/S4.psl.verdict.json": (470, "8d9d98965e270c2130b56fd6240c3b7460fe906ef5523f5e90396280dd043b28"),
    "search/certs/b3_gentle_source_census_preflight_v1_20260823.json": (887124, "c30077133305c07ca0e58c9eaa700d42a512a6bbbce96c9c27d161e921e1aaf2"),
    "crosscheck/verdicts/b3_gentle_source_census_v1_20260823.json": (4931, "e308a71323dc429d771d7fb86f507b3c17936716505dd6ca3ee3fbfdeecf7f4e"),
    "search/certs/d972_b4_word_key_artifact_v1_20260816.json": (176474, "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"),
    "search/certs/d972_idx3_arithmetic_receipt_v2_20260823.json": (249817, "1fca084f396605a8755534d19412a47f60af76406ca01a2ef99bc0c06f00e7d9"),
    "crosscheck/verdicts/d972_idx3_arithmetic_crosscheck_v2_20260823.json": (8804, "6fd63e3453854a02f504695876e246f1f9fa388a0b3018db4a15c84ec35db525"),
}


def canonical_compact(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")


def canonical_file_bytes(value: object) -> bytes:
    return canonical_compact(value) + b"\n"


def digest(value: object) -> str:
    return hashlib.sha256(canonical_compact(value)).hexdigest()


def fail(code: str, detail: str) -> None:
    raise RuntimeError(f"STATE_STOP {code}: {detail}")


def require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        fail(code, detail)


def pin(rel: str, expected: bool = True) -> dict:
    path = ROOT / rel
    require(path.is_file(), "MISSING_PINNED_INPUT", rel)
    raw = path.read_bytes()
    out = {"path": rel, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    if expected:
        require(rel in EXPECTED, "UNREGISTERED_EXPECTED_PIN", rel)
        require((out["bytes"], out["sha256"]) == EXPECTED[rel], "PIN_MISMATCH", f"{rel}: {out}")
        out["expected_match"] = True
    return out


def load_json(rel: str) -> object:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_new(rel: str, value: object) -> dict:
    rel_path = Path(rel)
    require(not rel_path.is_absolute() and ".." not in rel_path.parts, "OUTPUT_PATH_OUTSIDE_REPOSITORY", rel)
    path = ROOT / rel_path
    raw = canonical_file_bytes(value)
    if path.exists():
        existing = path.read_bytes()
        require(existing == raw, "IMMUTABLE_VERSIONED_OUTPUT_MISMATCH", rel)
        return {"path": rel, "bytes": len(existing), "sha256": hashlib.sha256(existing).hexdigest()}
    path.write_bytes(raw)
    return {"path": rel, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


# GAP/right-action permutation convention: i^(left*right)=(i^left)^right.
Perm = tuple[int, ...]


def pid(n: int) -> Perm:
    return tuple(range(n))


def pmul(left: Perm, right: Perm) -> Perm:
    return tuple(right[left[i]] for i in range(len(left)))


def pinv(value: Perm) -> Perm:
    out = [0] * len(value)
    for i, image in enumerate(value):
        out[image] = i
    return tuple(out)


def ppow(value: Perm, exponent: int) -> Perm:
    if exponent < 0:
        return ppow(pinv(value), -exponent)
    out = pid(len(value))
    base = value
    n = exponent
    while n:
        if n & 1:
            out = pmul(out, base)
        base = pmul(base, base)
        n //= 2
    return out


def gf8_mul(a: int, b: int) -> int:
    product = 0
    left, right = a, b
    while right:
        if right & 1:
            product ^= left
        left <<= 1
        right >>= 1
    for bit in (4, 3):
        if product & (1 << bit):
            product ^= 11 << (bit - 3)  # x^3+x+1
    return product


def gf8_inv(value: int) -> int:
    require(value != 0, "GF8_ZERO_INVERSE", "0")
    for candidate in range(1, 8):
        if gf8_mul(value, candidate) == 1:
            return candidate
    fail("GF8_INVERSE_ABSENT", str(value))
    raise AssertionError("unreachable")


def mat_to_perm(matrix: tuple[tuple[int, int], tuple[int, int]]) -> Perm:
    (a, b), (c, d) = matrix
    out = [0 if c == 0 else 1 + gf8_mul(a, gf8_inv(c))]
    for value in range(8):
        num = gf8_mul(a, value) ^ b
        den = gf8_mul(c, value) ^ d
        out.append(0 if den == 0 else 1 + gf8_mul(num, gf8_inv(den)))
    require(sorted(out) == list(range(9)), "PSL_PERM_NOT_BIJECTIVE", repr(out))
    return tuple(out)


S_PSL = mat_to_perm(((1, 0), (1, 1)))
T_PSL = mat_to_perm(((4, 3), (1, 5)))
W_PSL = pmul(S_PSL, pinv(T_PSL))
X_PSL = ppow(W_PSL, 2)
Y_PSL = pmul(pmul(pinv(S_PSL), X_PSL), S_PSL)
PSL_ID = pid(9)


D = tuple[int, int]  # r^a s^e
G = tuple[D, D, D]
Component = tuple[G, int]  # G36 x C3
Residual = tuple[Perm, int]  # PSL(2,8) x C3


def dmul(left: D, right: D, modulus: int) -> D:
    a, e = left
    b, f = right
    return ((a + (b if e == 0 else -b)) % modulus, e ^ f)


def dinv(value: D, modulus: int) -> D:
    a, e = value
    return ((-a if e == 0 else a) % modulus, e)


def gmul(left: G, right: G, modulus: int) -> G:
    return tuple(dmul(left[i], right[i], modulus) for i in range(3))  # type: ignore[return-value]


def ginv(value: G, modulus: int) -> G:
    return tuple(dinv(part, modulus) for part in value)  # type: ignore[return-value]


def gpow(value: G, exponent: int, modulus: int) -> G:
    if exponent < 0:
        return gpow(ginv(value, modulus), -exponent, modulus)
    out = gid()
    base = value
    n = exponent
    while n:
        if n & 1:
            out = gmul(out, base, modulus)
        base = gmul(base, base, modulus)
        n //= 2
    return out


def gid() -> G:
    return ((0, 0), (0, 0), (0, 0))


def gx(modulus: int) -> G:
    return ((1 % modulus, 0), (0, 1), (0, 1))


def gy(modulus: int) -> G:
    return ((1 % modulus, 1), (1 % modulus, 0), (1 % modulus, 1))


def reduce_g36(value: G) -> G:
    return tuple((a % 9, e) for a, e in value)  # type: ignore[return-value]


T = TypeVar("T")


def closure(identity: T, generators: Iterable[T], mul: Callable[[T, T], T], inv: Callable[[T], T]) -> set[T]:
    base = list(generators)
    steps = base + [inv(value) for value in base]
    seen = {identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for step in steps:
            nxt = mul(current, step)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def element_order(identity: T, value: T, mul: Callable[[T, T], T], cap: int) -> int:
    out = identity
    for order in range(1, cap + 1):
        out = mul(out, value)
        if out == identity:
            return order
    fail("ELEMENT_ORDER_CAP", repr(value))
    raise AssertionError("unreachable")


def extend_generator_map(
    identity: T,
    source_generators: list[T],
    target_generators: list[T],
    mul: Callable[[T, T], T],
    inv: Callable[[T], T],
) -> dict[T, T]:
    source_steps = source_generators + [inv(x) for x in source_generators]
    target_steps = target_generators + [inv(x) for x in target_generators]
    mapping = {identity: identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for source_step, target_step in zip(source_steps, target_steps):
            source_next = mul(current, source_step)
            target_next = mul(mapping[current], target_step)
            if source_next in mapping:
                require(mapping[source_next] == target_next, "GENERATOR_MAP_NOT_WELL_DEFINED", repr(source_next))
            else:
                mapping[source_next] = target_next
                queue.append(source_next)
    return mapping


def inverse_word(word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(-letter for letter in reversed(word))


def eval_word_g(word: Iterable[int], modulus: int) -> G:
    out = gid()
    x, y = gx(modulus), gy(modulus)
    for letter in word:
        value = x if abs(letter) == 1 else y
        if letter < 0:
            value = ginv(value, modulus)
        out = gmul(out, value, modulus)
    return out


def eval_word_perm(word: Iterable[int]) -> Perm:
    out = PSL_ID
    for letter in word:
        value = X_PSL if abs(letter) == 1 else Y_PSL
        if letter < 0:
            value = pinv(value)
        out = pmul(out, value)
    return out


def eval_word_c3(word: Iterable[int]) -> int:
    # sigma1=sigma2=q, hence x=sigma1^2 and y=sigma2^2 both map to q^2.
    return sum((2 if letter > 0 else -2) for letter in word) % 3


def encode_g(value: G) -> list[list[int]]:
    return [[int(a), int(e)] for a, e in value]


def encode_perm(value: Perm) -> list[int]:
    return [image + 1 for image in value]


def build_g36_transversal() -> tuple[dict[G, tuple[int, ...]], dict[G, Perm], dict[G, int]]:
    steps = [
        (1, gx(36), X_PSL, 2),
        (-1, ginv(gx(36), 36), pinv(X_PSL), 1),
        (2, gy(36), Y_PSL, 2),
        (-2, ginv(gy(36), 36), pinv(Y_PSL), 1),
    ]
    words = {gid(): ()}
    psl_values = {gid(): PSL_ID}
    c3_values = {gid(): 0}
    queue = deque([gid()])
    while queue:
        current = queue.popleft()
        for letter, step_g, step_p, step_c in steps:
            nxt = gmul(current, step_g, 36)
            next_p = pmul(psl_values[current], step_p)
            next_c = (c3_values[current] + step_c) % 3
            if nxt not in words:
                words[nxt] = words[current] + (letter,)
                psl_values[nxt] = next_p
                c3_values[nxt] = next_c
                queue.append(nxt)
            else:
                # Different words for the same G36 element need not agree in the
                # residual factors; that difference is exactly a Schreier image.
                pass
    require(len(words) == 23328, "G36_TRANSVERSAL_ORDER", str(len(words)))
    return words, psl_values, c3_values


def residual_mul(left: Residual, right: Residual) -> Residual:
    return (pmul(left[0], right[0]), (left[1] + right[1]) % 3)


def residual_inv(value: Residual) -> Residual:
    return (pinv(value[0]), (-value[1]) % 3)


def residual_correction_words(
    words: dict[G, tuple[int, ...]], psl_values: dict[G, Perm], c3_values: dict[G, int]
) -> tuple[dict[Residual, tuple[int, ...]], list[dict]]:
    edge_steps = [
        (1, gx(36), X_PSL, 2),
        (-1, ginv(gx(36), 36), pinv(X_PSL), 1),
        (2, gy(36), Y_PSL, 2),
        (-2, ginv(gy(36), 36), pinv(Y_PSL), 1),
    ]
    residual_identity: Residual = (PSL_ID, 0)
    chosen: list[tuple[Residual, tuple[int, ...]]] = []
    chosen_closure = {residual_identity}
    trace = []
    for current in words:  # insertion/BFS order is deterministic
        for letter, step_g, step_p, step_c in edge_steps:
            nxt = gmul(current, step_g, 36)
            residual = (
                pmul(pmul(psl_values[current], step_p), pinv(psl_values[nxt])),
                (c3_values[current] + step_c - c3_values[nxt]) % 3,
            )
            if residual in chosen_closure:
                continue
            kernel_word = words[current] + (letter,) + inverse_word(words[nxt])
            require(eval_word_g(kernel_word, 36) == gid(), "SCHREIER_NOT_IN_G36_KERNEL", repr(kernel_word))
            require((eval_word_perm(kernel_word), eval_word_c3(kernel_word)) == residual, "SCHREIER_RESIDUAL_MISMATCH", repr(kernel_word))
            chosen.append((residual, kernel_word))
            chosen_closure = closure(
                residual_identity,
                [item[0] for item in chosen],
                residual_mul,
                residual_inv,
            )
            trace.append({"selected_generator": len(chosen), "kernel_word": list(kernel_word), "residual_psl_one_line": encode_perm(residual[0]), "residual_c3_exp": residual[1], "closure_order": len(chosen_closure)})
            if len(chosen_closure) == 1512:
                break
        if len(chosen_closure) == 1512:
            break
    require(len(chosen_closure) == 1512, "SCHREIER_RESIDUAL_NOT_SURJECTIVE", str(len(chosen_closure)))

    steps: list[tuple[Residual, tuple[int, ...]]] = []
    for value, word in chosen:
        steps.append((value, word))
        steps.append((residual_inv(value), inverse_word(word)))
    corrections = {residual_identity: ()}
    queue = deque([residual_identity])
    while queue:
        current = queue.popleft()
        for step, step_word in steps:
            nxt = residual_mul(current, step)
            if nxt not in corrections:
                corrections[nxt] = corrections[current] + step_word
                queue.append(nxt)
    require(len(corrections) == 1512, "RESIDUAL_WORD_COVERAGE", str(len(corrections)))
    return corrections, trace


def build_raw_fibre() -> tuple[list[dict], dict]:
    words, psl_values, c3_values = build_g36_transversal()
    corrections, schreier_trace = residual_correction_words(words, psl_values, c3_values)
    target_g9: G = ((4, 0), (5, 0), (0, 0))
    lifts = sorted((value for value in words if reduce_g36(value) == target_g9), key=lambda value: tuple(x for pair in value for x in pair))
    require(len(lifts) == 8, "G36_TO_G9_TARGET_FIBRE", str(len(lifts)))
    fibre = []
    for m in (0, 18):
        for g in lifts:
            base_word = words[g]
            for c3_exp in range(3):
                needed: Residual = (pinv(psl_values[g]), (c3_exp - c3_values[g]) % 3)
                word = base_word + corrections[needed]
                require(eval_word_g(word, 36) == g, "SOURCE_WORD_G36", repr(g))
                require(eval_word_perm(word) == PSL_ID, "SOURCE_WORD_PSL", repr(g))
                require(eval_word_c3(word) == c3_exp, "SOURCE_WORD_C3", f"{g}:{c3_exp}")
                row = {
                    "raw_id": f"R{len(fibre) + 1:02d}",
                    "m_mod_36": m,
                    "f": {"g36": encode_g(g), "psl_one_line": encode_perm(PSL_ID), "c3_exp": c3_exp},
                    "source_word_signed_xy": list(word),
                    "source_word_sha256": digest(list(word)),
                    "reduction": {"m_mod_18": m % 18, "g9": encode_g(reduce_g36(g)), "psl_one_line": encode_perm(PSL_ID), "target_row_index_zero_based": TARGET_ROW_INDEX},
                }
                row["row_sha256"] = digest(row)
                fibre.append(row)
    require(len(fibre) == 48, "RAW_FIBRE_CARDINALITY", str(len(fibre)))
    require(len({row["row_sha256"] for row in fibre}) == 48, "RAW_FIBRE_DUPLICATE", "row digest collision")
    word_meta = {
        "algorithm": "right-Cayley BFS transversal for G36; deterministic Schreier generators for ker(F2->G36); residual BFS in PSL(2,8)xC3",
        "generator_step_order": ["x", "x^-1", "y", "y^-1"],
        "G36_transversal_count": len(words),
        "residual_target_order": 1512,
        "schreier_selected_generator_count": len(schreier_trace),
        "schreier_trace": schreier_trace,
        "schreier_trace_sha256": digest(schreier_trace),
        "max_source_word_length": max(len(row["source_word_signed_xy"]) for row in fibre),
        "source_word_roster_sha256": digest([row["source_word_signed_xy"] for row in fibre]),
    }
    return fibre, word_meta


def normal_closure_commutator_g36() -> tuple[set[G], list[dict]]:
    x, y = gx(36), gy(36)
    comm = gmul(gmul(gmul(ginv(x, 36), ginv(y, 36), 36), x, 36), y, 36)
    generators = {comm}
    trace = []
    for iteration in range(20):
        subgroup = closure(gid(), generators, lambda a, b: gmul(a, b, 36), lambda a: ginv(a, 36))
        expanded = set(generators)
        for value in generators:
            for by in (x, y, ginv(x, 36), ginv(y, 36)):
                expanded.add(gmul(gmul(ginv(by, 36), value, 36), by, 36))
        trace.append({"iteration": iteration, "normal_generators": len(generators), "subgroup_order": len(subgroup), "expanded_normal_generators": len(expanded)})
        if expanded == generators:
            require(len(subgroup) == 1458, "G36_DERIVED_ORDER", str(len(subgroup)))
            return subgroup, trace
        generators = expanded
    fail("G36_DERIVED_CLOSURE_CAP", "20")
    raise AssertionError("unreachable")


def source_digest_from_export(row: dict) -> str:
    q = row["marked_quotient_map"]
    canonical = (
        f"node_key={row['node_id']}\n"
        f"index={row['b3_index']}\n"
        f"degree={q['permutation_degree']}\n"
        f"sigma1={q['sigma1']}\n"
        f"sigma2={q['sigma2']}\n"
        f"x={q['x_eq_sigma1_sq']}\n"
        f"y={q['y_eq_sigma2_sq']}\n"
        f"c={q['c_eq_delta_sq']}\n"
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def authenticate_inputs() -> tuple[dict[str, dict], dict]:
    pins = {rel: pin(rel) for rel in EXPECTED}
    lins = load_json("ci/lins_marked_artifacts_32626064970/lins_marked_export/lins_marked_strictness_export_v1_20260823.json")
    require(isinstance(lins, dict), "LINS_SCHEMA_TYPE", type(lins).__name__)
    require(lins["schema"] == "lins-marked-strictness-export/v1" and lins["status"] == "CANDIDATE_GAP_PRODUCER" and lins["verified"] is False, "LINS_SCHEMA_STATUS", repr({k: lins[k] for k in ("schema", "status", "verified")}))
    require(lins["universe"] == {"group": "B3=<sigma1,sigma2 | sigma1 sigma2 sigma1=sigma2 sigma1 sigma2>", "method": "one LowIndexNormalSubgroupsSearch call", "index_upper_bound": 2000, "nodes_total": 4266, "identity_nodes_excluded": 1, "nonidentity_rows": 4265}, "LINS_UNIVERSE", repr(lins["universe"]))
    require(lins["claim_cover"] == {"claim": "all 4,265 nonidentity nodes of the fixed index<=2000 LINS call", "complete": True, "mode": "bound_2000"}, "LINS_CLAIM_COVER", repr(lins["claim_cover"]))
    require(lins["source_pins"] == {"reference_census_path": "search/certs/lins_census_2000_v1_20260811.json", "reference_census_sha256": EXPECTED["search/certs/lins_census_2000_v1_20260811.json"][1], "producer_path": "search/lins_marked_strictness_export_v1.g", "producer_sha256": EXPECTED["search/lins_marked_strictness_export_v1.g"][1]}, "LINS_SOURCE_PINS", repr(lins["source_pins"]))
    require(len(lins["rows"]) == 4265, "LINS_ROW_COUNT", str(len(lins["rows"])))
    selected = [(index, row) for index, row in enumerate(lins["rows"]) if row["node_id"] == NODE_ID]
    require(len(selected) == 1, "SELECTED_NODE_UNIQUENESS", str(len(selected)))
    node_index, node = selected[0]
    expected_node = {
        "node_id": NODE_ID,
        "b3_index": 3,
        "canonical_id_words": ["a^3", "b*a^-1", "b^-1*a"],
        "marked_quotient_map": {"quotient_order": 3, "permutation_degree": 3, "sigma1": "(1,2,3)", "sigma2": "(1,2,3)", "x_eq_sigma1_sq": "(1,3,2)", "y_eq_sigma2_sq": "(1,3,2)", "c_eq_delta_sq": "()", "F2_image_order": 3, "PB3_image_order": 3},
        "core_B3_L": {"construction": "L (normality is part of the LINS node contract)", "equals_L": True, "index": 3, "canonical_id_words": ["a^3", "b*a^-1", "b^-1*a"]},
        "joint_image": {"F2_order": 4408992, "PB3_order": 4408992},
        "source_K": "M cap Core_B3(L)",
        "strictness": {"F2_ratio_MF_over_KF": 3, "PB3_ratio_M_over_K": 3, "strict_F2": True, "strict_PB3": True, "class": "STRICT_F2"},
        "source_digest_sha256": NODE_SOURCE_DIGEST,
    }
    require(node == expected_node, "SELECTED_NODE_EXACT_ROW", repr(node))
    require(source_digest_from_export(node) == NODE_SOURCE_DIGEST, "SELECTED_NODE_SOURCE_DIGEST", source_digest_from_export(node))
    index2 = [(i, row) for i, row in enumerate(lins["rows"]) if row["b3_index"] == 2]
    index3 = [(i, row) for i, row in enumerate(lins["rows"]) if row["b3_index"] == 3]
    require(len(index2) == len(index3) == 1, "LINS_LOW_NORMAL_SHELL_COUNTS", repr((len(index2), len(index3))))
    require(index2[0][1]["strictness"]["class"] == "NO_REFINEMENT" and index2[0][1]["marked_quotient_map"]["PB3_image_order"] == 1, "INDEX2_LINS_NOOP", repr(index2[0]))
    require(index3[0][0] == node_index == 357, "INDEX3_NODE_ARRAY_INDEX", repr((index3[0][0], node_index)))
    return pins, node


def reconstruct_rosters(word_artifact: dict, arithmetic: dict) -> dict:
    require(word_artifact["schema"] == "d972-b4-word-key-artifact/v1" and word_artifact["count"] == 972 and len(word_artifact["rows"]) == 972, "WORD_ARTIFACT_COVER", repr((word_artifact.get("schema"), word_artifact.get("count"))))
    candidates = {row["candidate_id"]: row for row in arithmetic["finite_index3_census"]["nonnormal_candidates"]}
    require({"IDX3-NN-09", "IDX3-NN-12"} <= set(candidates), "ROSTER_SOURCE_CANDIDATES", repr(candidates.keys()))
    nn09 = set(candidates["IDX3-NN-09"]["row_indices"])
    nn12 = set(candidates["IDX3-NN-12"]["row_indices"])
    require(len(nn09) == len(nn12) == 324 and len(nn09 & nn12) == 108, "NN_ROSTER_COUNTS", repr((len(nn09), len(nn12), len(nn09 & nn12))))
    rosters = {
        "seed_pool_432": sorted(set(range(972)) - (nn09 | nn12)),
        "symdiff_432": sorted(nn09 ^ nn12),
    }
    out = {}
    for name, rows in rosters.items():
        keys = [word_artifact["rows"][i][1] for i in rows]
        observed = {"definition": ROSTER_DIGESTS[name]["definition"], "count": len(rows), "row_index_list_sha256": digest(rows), "canonical_key_list_sha256": digest(keys)}
        require(observed == ROSTER_DIGESTS[name], "ROSTER_DIGEST_MISMATCH", f"{name}:{observed}")
        out[name] = {**observed, "row_indices": rows}
    require(TARGET_ROW_INDEX in rosters["seed_pool_432"] and TARGET_ROW_INDEX not in rosters["symdiff_432"], "TARGET_ROSTER_MEMBERSHIP", str(TARGET_ROW_INDEX))
    return out


def structural_bundle() -> tuple[dict, dict[str, dict]]:
    pins, node = authenticate_inputs()
    k36 = load_json("certificates/K36.v1.json")
    vk36 = load_json("crosscheck/verdicts/K36.v1.verdict.json")
    k9 = load_json("certificates/K9.v1.json")
    vk9 = load_json("crosscheck/verdicts/K9.v1.verdict.json")
    s4 = load_json("certificates/S4.v2.json")
    vs4 = load_json("crosscheck/verdicts/S4.psl.verdict.json")
    k1_receipt = load_json("search/certs/b3_gentle_source_census_preflight_v1_20260823.json")
    k1_verdict = load_json("crosscheck/verdicts/b3_gentle_source_census_v1_20260823.json")
    word_artifact = load_json("search/certs/d972_b4_word_key_artifact_v1_20260816.json")
    arithmetic = load_json("search/certs/d972_idx3_arithmetic_receipt_v2_20260823.json")
    arithmetic_verdict = load_json("crosscheck/verdicts/d972_idx3_arithmetic_crosscheck_v2_20260823.json")

    require(k36["target"]["invariants"] == {"index_PB3": 23328, "index_B3": 139968, "N_ord": 36, "derived_order": 1458}, "K36_INVARIANTS", repr(k36["target"]["invariants"]))
    require(vk36["all_pass"] and vk36["cross_checked"], "K36_CROSSCHECK", repr((vk36.get("all_pass"), vk36.get("cross_checked"))))
    require(k9["target"]["invariants"] == {"index_PB3": 2916, "index_B3": 17496, "N_ord": 18, "derived_order": 729}, "K9_INVARIANTS", repr(k9["target"]["invariants"]))
    require(vk9["all_pass"] and vk9["cross_checked"], "K9_CROSSCHECK", repr((vk9.get("all_pass"), vk9.get("cross_checked"))))
    require(s4["ambient_group"] == "PSL(2,8)" and s4["generation_checks"] == {"gen_ambient": 504, "gen_derived": 504} and s4["marking"]["ord_X"] == 9, "S4_INVARIANTS", repr((s4.get("ambient_group"), s4.get("generation_checks"), s4.get("marking"))))
    require(vs4["ok"], "S4_CROSSCHECK", repr(vs4))
    require(k1_receipt["SOURCE_OBJECT"] == "K=K^(36) intersection N_S4" and k1_receipt["CLAIM-COVER-1"]["fibre_size_histogram"] == {"2": 972}, "K1_RECEIPT", repr((k1_receipt.get("SOURCE_OBJECT"), k1_receipt.get("CLAIM-COVER-1"))))
    require(k1_verdict["status"] == "PASS" and k1_verdict["replay"]["cross_checked"] and k1_verdict["replay"]["controls"]["all_pass"], "K1_VERDICT", repr((k1_verdict.get("status"), k1_verdict.get("replay", {}).get("cross_checked"))))
    require(arithmetic_verdict.get("all_checks_pass") is True and arithmetic_verdict.get("cross_checked_finite_census") is True, "ARITHMETIC_ROSTER_VERDICT", repr((arithmetic_verdict.get("all_checks_pass"), arithmetic_verdict.get("cross_checked_finite_census"))))

    require(word_artifact["rows"][TARGET_ROW_INDEX] == TARGET_FULL_ROW, "TARGET_LITERAL_ROW", repr(word_artifact["rows"][TARGET_ROW_INDEX]))
    require(digest(TARGET_FULL_ROW) == TARGET_DIGESTS["full_row_compact_sha256"], "TARGET_FULL_DIGEST", digest(TARGET_FULL_ROW))
    require(digest(TARGET_KEY) == TARGET_DIGESTS["target_key_compact_sha256"], "TARGET_KEY_DIGEST", digest(TARGET_KEY))
    require(digest(TARGET_WORD) == TARGET_DIGESTS["word_compact_sha256"], "TARGET_WORD_DIGEST", digest(TARGET_WORD))
    require(eval_word_g(TARGET_WORD, 9) == ((4, 0), (5, 0), (0, 0)), "TARGET_WORD_G9_REPLAY", repr(eval_word_g(TARGET_WORD, 9)))
    require(eval_word_perm(TARGET_WORD) == PSL_ID and eval_word_c3(TARGET_WORD) == 0, "TARGET_WORD_MARKED_REPLAY", repr((encode_perm(eval_word_perm(TARGET_WORD)), eval_word_c3(TARGET_WORD))))

    psl = closure(PSL_ID, [X_PSL, Y_PSL], pmul, pinv)
    require(len(psl) == 504 and element_order(PSL_ID, X_PSL, pmul, 100) == element_order(PSL_ID, Y_PSL, pmul, 100) == 9, "PSL_MARKED_RECONSTRUCTION", repr((len(psl), element_order(PSL_ID, X_PSL, pmul, 100), element_order(PSL_ID, Y_PSL, pmul, 100))))
    g36 = closure(gid(), [gx(36), gy(36)], lambda a, b: gmul(a, b, 36), lambda a: ginv(a, 36))
    g9 = closure(gid(), [gx(9), gy(9)], lambda a, b: gmul(a, b, 9), lambda a: ginv(a, 9))
    require(len(g36) == 23328 and len(g9) == 2916 and len({reduce_g36(value) for value in g36}) == 2916, "DIHEDRAL_MARKED_RECONSTRUCTION", repr((len(g36), len(g9))))
    derived, derived_trace = normal_closure_commutator_g36()
    require(len(g36) // len(derived) == 16, "G36_ABELIANIZATION_ORDER", str(len(g36) // len(derived)))
    component = closure((gid(), 0), [(gx(36), 2), (gy(36), 2)], lambda a, b: (gmul(a[0], b[0], 36), (a[1] + b[1]) % 3), lambda a: (ginv(a[0], 36), (-a[1]) % 3))
    require(len(component) == 69984, "G36_C3_DIRECT_MARKED_ORDER", str(len(component)))
    require(element_order((gid(), 0), (gx(36), 2), lambda a, b: (gmul(a[0], b[0], 36), (a[1] + b[1]) % 3), 100) == 36, "JOINT_X_ORDER", "not 36")

    rosters = reconstruct_rosters(word_artifact, arithmetic)
    fibre, word_meta = build_raw_fibre()
    require(all(row["reduction"]["m_mod_18"] == 0 and row["reduction"]["g9"] == [[4, 0], [5, 0], [0, 0]] and row["reduction"]["psl_one_line"] == list(range(1, 10)) for row in fibre), "RAW_FIBRE_REDUCTION", "not all rows reduce to target")

    shell_cover = {
        "fair_shells_closed": [2, 3],
        "LINS_normal_node_counts": {"index_2": 1, "index_3": 1},
        "index_2": {
            "all_transitive_images": ["C2"],
            "classification_proof": "Every index-2 subgroup is normal. In C2 the braid relation forces sigma1=sigma2; the unique kernel is exponent parity. PB3, hence K1, lies in it.",
            "core_effect_on_K1": "NO_OP_K1_CONTAINED",
        },
        "index_3": {
            "all_transitive_images": ["C3 regular", "S3 natural"],
            "C3_classification": "In the abelian transitive image the braid relation forces sigma1=sigma2; the two generator choices have the same kernel L3=ker(exp mod 3). This is the unique normal row in the complete LINS export.",
            "S3_classification": "Every surjective degree-3 action sends sigma1,sigma2 to distinct transpositions up to conjugacy. Its core is ker(B3->S3)=PB3, so intersection with K1 is a no-op; the three point stabilizers share that core.",
            "strict_core": NODE_ID,
            "strict_core_array_index_zero_based": 357,
            "strict_core_ordinal_one_based": 358,
            "S3_core_effect_on_K1": "NO_OP_K1_CONTAINED",
        },
        "earliest_fair_strict_source": NODE_ID,
        "no_shell_omission": True,
    }
    isolation = {
        "selected_PB3_source": "N3=PB3 cap ker(exp_B3 mod 3)",
        "marked_PB3_quotient": {"group": "C3=<q>", "x": "q^2", "y": "q^2", "c": "1"},
        "isolation_proof": "For any actual shadow with target N3, the derived quotient C3' is trivial, so f=1. The odd unit u=2m+1 is a unit mod 3; x,y map to q^(2u), hence the induced endomorphism is an automorphism and its kernel is exactly N3. Thus every shadow with target N3 settles.",
        "component_set": ["N3"],
        "component_set_cardinality": 1,
        "source_diamond": "N3^diamond=N3 by Proposition 3.14",
        "parent_isolation_pin": "K1 isolation is an accepted input of the launch contract and its pinned component receipts",
        "intersection_isolation": "K1 and N3 are isolated; Proposition 3.15 gives H=K1 cap N3 isolated",
        "intersection_component_set": ["H=K1 cap N3"],
        "intersection_diamond": "H^diamond=H by Proposition 3.14",
        "verified": False,
    }
    joint = {
        "parent": "K1=K^(36) cap N_S4",
        "selected_core": "L3=ker(exp_B3 mod 3)",
        "candidate_definition": "H=K1 cap L3=K1 cap N3",
        "inclusions": {"H_le_K1": True, "K1_le_M": True, "H_le_M": True, "all_maps": "coordinate projection G36->G9, identity PSL, forget C3"},
        "PB3_marked_quotient": "G36 x PSL(2,8) x C3",
        "marked_maps": {
            "selected_B3_C3": {"sigma1": "q", "sigma2": "q", "x=sigma1^2": "q^2", "y=sigma2^2": "q^2", "c=Delta^2": "1"},
            "G36": {"x": [[1, 0], [0, 1], [0, 1]], "y": [[1, 1], [1, 0], [1, 1]]},
            "PSL2_8": {"x_one_line": encode_perm(X_PSL), "y_one_line": encode_perm(Y_PSL), "c_one_line": encode_perm(PSL_ID)},
            "C3": {"x_exp": 2, "y_exp": 2, "c_exp": 0},
        },
        "relation_replay": {"B3_C3_braid": True, "x_sigma1_square": True, "y_sigma2_square": True, "c_delta_square": True},
        "orders": {"G36": 23328, "PSL2_8": 504, "C3": 3, "PB3_joint": 35271936, "B3_index": 211631616, "N_ord": 36},
        "strictness": {"parent_PB3_quotient_order": 11757312, "candidate_PB3_quotient_order": 35271936, "ratio": 3, "strict": True},
        "kernel_equality": "The marked product map has kernel ker(K1-map) cap ker(exp mod 3)=K1 cap L3=H.",
        "direct_product_proof": {
            "G36_times_PSL": "cross-checked K1 split roof: solvable G36 and nonabelian-simple PSL(2,8) have no common nontrivial quotient",
            "times_C3": "G36 has derived order 1458 and abelianization order 16; PSL(2,8) is perfect. Thus the K1 quotient has abelianization order 16 and no C3 quotient. The marked G36xC3 closure independently has order 69,984.",
        },
        "duplicate_decision": "STRICT_NOT_DUPLICATE_OF_K1",
        "special_pent_mode_used": False,
    }
    fibre_contract = {
        "target_row_index_zero_based": TARGET_ROW_INDEX,
        "raw_fibre_formula": "{0,18} x ker(G36->G9) x {identity_PSL} x C3",
        "kernel_G36_to_G9_order": 8,
        "m_lift_count": 2,
        "C3_lift_count": 3,
        "raw_cardinality": 48,
        "deterministic_order": "m in [0,18], then flattened G36 triple lexicographically, then C3 exponent [0,1,2]",
        "raw_roster_sha256": digest(fibre),
        "raw_row_digest_roster_sha256": digest([row["row_sha256"] for row in fibre]),
        "raw_roster": fibre,
        "word_lift_certificate": word_meta,
    }
    predicate_contract = {
        "evaluation_status": "NOT_RUN_MODE_TOKEN_REQUIRED",
        "domain": "all 48 raw_roster points in deterministic order",
        "candidate_steps": ["exact reduction", "charming unit gcd(2m+1,36)=1", "f in derived quotient", "hexagon (3.10)", "hexagon (3.11)", "onto full marked quotient"],
        "hexagon_convention": {"theta": "x->y,y->x", "tau": "x->y,y->(xy)^-1", "h10": "f*theta(f)=1", "h11": "tau^2(y^m f)*tau(y^m f)*(y^m f)=1", "multiplication": "natural abstract product; permutation coordinates use GAP right-action composition"},
        "onto_generators": ["x^(2m+1)", "f^-1 y^(2m+1) f"],
        "positive_policy": "evaluate and retain the complete 48-row trace (stronger than allowed lex-first stop)",
        "negative_policy": "evaluate all 48; no early stop; close CLAIM-COVER-RUNG-1",
        "same_representative_Dpap": "NOT_APPLICABLE_ORDINARY_MODE",
        "result_tokens_before_checker": "FORBIDDEN",
    }
    mutants = [
        {"id": "SHELL-INDEX2-OMISSION", "mutation": "delete the index-2 core class", "reject_by": "fair_shells_closed and exact class inventory"},
        {"id": "SHELL-S3-CORE-OMISSION", "mutation": "delete the nonnormal degree-3/S3 core", "reject_by": "degree-3 transitive image classification"},
        {"id": "SOURCE-NODE-DIGEST-FLIP", "mutation": "alter node id/source digest/export row", "reject_by": "full export byte pin plus row equality and digest replay"},
        {"id": "DUPLICATE-AS-STRICT", "mutation": "use index-2 or S3-core no-op as strict", "reject_by": "joint ratio must equal 3"},
        {"id": "DIAMOND-FORGE", "mutation": "replace singleton component/equality", "reject_by": "isolation proof and exact component-set digest"},
        {"id": "ROW-35-37-ONE-BASED", "mutation": "select adjacent or one-based row", "reject_by": "literal row/key/word digests"},
        {"id": "WRONG-432-SYMDIFF", "mutation": "substitute symdiff_432 for seed_pool_432", "reject_by": "separate roster definitions and four distinct digests"},
        {"id": "REVERSED-WORD-MULTIPLICATION", "mutation": "reverse signed source word/product convention", "reject_by": "all 48 word-to-coordinate replays"},
        {"id": "TARGET-KEY-MUTATION", "mutation": "change any target coordinate", "reject_by": "target-key digest and all 48 exact reductions"},
        {"id": "ONE-HEXAGON-OMITTED", "mutation": "accept after only h10 or h11", "reject_by": "both boolean fields required before onto"},
        {"id": "CHARMING-WITHOUT-ONTO", "mutation": "accept charming candidate without generation", "reject_by": "full quotient order required"},
        {"id": "SINGLE-REPRESENTATIVE-FIBRE", "mutation": "report one word instead of raw fibre", "reject_by": "2*8*3=48 count, uniqueness, roster digest"},
        {"id": "EARLY-STOP-NEGATIVE", "mutation": "negative with evaluated_count<48", "reject_by": "CLAIM-COVER-RUNG-1"},
        {"id": "COUNT-DIGEST-RECEIPT-FLIP", "mutation": "alter count, aggregate digest, or immutable receipt", "reject_by": "manifest pins and independent checker"},
        {"id": "SPECIAL-PENT-CARGO-INJECTION", "mutation": "add Dpap/W2/prime-local conclusion to ordinary mode", "reject_by": "exclusive mode token and absent Dpap branch"},
    ]
    bundle = {
        "schema": "d972-rung-ordinary-idx3-prereg/v2",
        "compatibility_repair": {
            "lineage": "v2-current-task-pin-and-execute-reauthentication",
            "supersedes_prepare_bundle_only": "v1",
            "old_task_pin": {"bytes": 11010, "sha256": "0fbda66074adc29caa51b240e28aa649fddd3ee51101b7246e77f0ea9c028670"},
            "current_task_pin": pins["sol/luna_task_159o_ladder_launch.md"],
            "predicate_or_raw_universe_changed": False,
            "execute_reauthenticates_all_input_pins": True,
        },
        "artifact_kind": "producer-only immutable structural preregistration",
        "status": "PREREGISTERED_NOT_RUN",
        "selected_mode": "UNFROZEN_PENDING_CANARY_DERIVED_MODE_TOKEN",
        "rung_name_assigned": False,
        "outcome_evaluated": False,
        "outcome_value": "UNSET",
        "producer_pin": pin(SOURCE_REL, expected=False),
        "input_pins": list(pins.values()),
        "LINS_full_shell_authentication": {"artifact_pin": pins["ci/lins_marked_artifacts_32626064970/lins_marked_export/lins_marked_strictness_export_v1_20260823.json"], "source_pins": [pins["search/certs/lins_census_2000_v1_20260811.json"], pins["search/lins_marked_strictness_export_v1.g"]], "claim_cover": "all 4,265 nonidentity normal nodes in one bound-2000 call", "selected_node": node},
        "fair_shell_cover": shell_cover,
        "isolation_and_diamond": isolation,
        "joint_marked_quotient": joint,
        "target": {"row_index_zero_based": TARGET_ROW_INDEX, "full_row": TARGET_FULL_ROW, "digests": TARGET_DIGESTS},
        "rung_and_control_rosters": rosters,
        "row36_raw_fibre": fibre_contract,
        "one_seed_predicate_contract": predicate_contract,
        "destructive_controls_and_mutants": mutants,
        "derived_reconstruction": {"G36_derived_order": len(derived), "G36_abelianization_order": 16, "normal_closure_trace": derived_trace, "normal_closure_trace_sha256": digest(derived_trace)},
        "producer_checker_firewall": {"role": "producer", "checker_source_opened_or_imported": False, "checker_may_receive_only": ["future immutable execution receipt path/bytes/SHA", "future immutable execution manifest path/bytes/SHA"], "checker_must_not_read": [SOURCE_REL, "producer helpers", "producer report"]},
        "mode_gate": {
            "required_token_schema": "d972-rung-mode-freeze/v1",
            "required_mode": MODE,
            "required_fields": {"corrected_canary_gate": "CROSS_CHECKED_CLOSED", "four_freeze_gates": "CLOSED", "special_pent_selected": False, "ordinary_node_id": NODE_ID, "ordinary_prereg_sha256": "filled from this preregistration pin"},
            "token_file_sha256_must_be_supplied_separately": True,
            "no_token_behavior": "STATE_STOP MODE_TOKEN_REQUIRED",
        },
        "first_missing_datum": "PARENT_ISSUED_IMMUTABLE_CANARY_DERIVED_MODE_TOKEN_THEN_OUTCOME_RUN_AND_HELPER_DISJOINT_CHECKER",
        "cross_checked": False,
        "verified": False,
    }
    return bundle, pins


def prepare() -> None:
    bundle, pins = structural_bundle()
    prereg_pin = write_new(PREREG_REL, bundle)
    manifest = {
        "schema": "d972-rung-ordinary-idx3-launch-manifest/v2",
        "compatibility_repair": bundle["compatibility_repair"],
        "status": "PREREGISTERED_NOT_RUN",
        "selected_mode": "UNFROZEN_PENDING_CANARY_DERIVED_MODE_TOKEN",
        "rung_name_assigned": False,
        "outcome_evaluated": False,
        "producer": bundle["producer_pin"],
        "preregistration": prereg_pin,
        "input_pins": list(pins.values()),
        "prepare_command": "python -B search/d972_rung_ordinary_idx3_producer_v2.py --prepare",
        "future_execute_command_template": "python -B search/d972_rung_ordinary_idx3_producer_v2.py --execute --mode-token <immutable-json> --mode-token-sha256 <sha256> --receipt-rel <new-versioned-receipt.json> --execution-manifest-rel <new-versioned-manifest.json>",
        "future_venue": {"local_prepare": True, "outcome_run": "GHA_DEFAULT_UNLESS_PARENT_REFREEZES", "SAT": "FORBIDDEN_WITHOUT_NEW_SAME_PREDICATE_ENCODER_AND_INDEPENDENT_LRAT_REPLAY"},
        "mode_token_contract": {**bundle["mode_gate"], "required_fields": {**bundle["mode_gate"]["required_fields"], "ordinary_prereg_sha256": prereg_pin["sha256"]}},
        "independent_checker_contract": {
            "author_separation_required": True,
            "checker_receives_only": ["future receipt path/bytes/SHA", "future execution manifest path/bytes/SHA"],
            "must_not_open_or_import": [SOURCE_REL, "producer helpers", "producer report"],
            "must_reconstruct": ["full degree-2/3 shell including S3 no-op", "selected LINS row and source digest", "K1/core direct joint", "isolation singleton and diamond equality", "all 48 raw points and signed words", "both hexagons/charming/onto/reduction on the complete trace", "CLAIM-COVER-RUNG-1", "all registered mutants"],
        },
        "selective_publish_if_parent_later_uses_GHA": [SOURCE_REL, PREREG_REL, LAUNCH_MANIFEST_REL],
        "git_GHA_workflow_es7ops_actions": [],
        "first_missing_datum": bundle["first_missing_datum"],
    }
    manifest_pin = write_new(LAUNCH_MANIFEST_REL, manifest)
    print(json.dumps({"status": bundle["status"], "preregistration": prereg_pin, "launch_manifest": manifest_pin, "outcome_evaluated": False}, sort_keys=True))


def validate_mode_token(path: Path, expected_sha256: str, prereg_pin: dict) -> dict:
    require(path.is_file(), "MODE_TOKEN_REQUIRED", str(path))
    raw = path.read_bytes()
    observed = hashlib.sha256(raw).hexdigest()
    require(len(expected_sha256) == 64 and observed == expected_sha256.lower(), "MODE_TOKEN_PIN_MISMATCH", f"observed={observed},expected={expected_sha256}")
    token = json.loads(raw.decode("utf-8"))
    required = {
        "schema": "d972-rung-mode-freeze/v1",
        "mode": MODE,
        "corrected_canary_gate": "CROSS_CHECKED_CLOSED",
        "four_freeze_gates": "CLOSED",
        "special_pent_selected": False,
        "ordinary_node_id": NODE_ID,
        "ordinary_prereg_sha256": prereg_pin["sha256"],
    }
    for key, value in required.items():
        require(token.get(key) == value, "MODE_TOKEN_FIELD", f"{key}: observed={token.get(key)!r},expected={value!r}")
    return {"path": str(path), "bytes": len(raw), "sha256": observed, "content": token}


def decode_g(value: list[list[int]]) -> G:
    require(len(value) == 3 and all(len(pair) == 2 for pair in value), "G_ENCODING", repr(value))
    return tuple((int(a) % 36, int(e) % 2) for a, e in value)  # type: ignore[return-value]


def execute(args: argparse.Namespace) -> None:
    live_pins, _ = authenticate_inputs()
    prereg_pin = pin(PREREG_REL, expected=False)
    launch_pin = pin(LAUNCH_MANIFEST_REL, expected=False)
    prereg = load_json(PREREG_REL)
    require(prereg["input_pins"] == list(live_pins.values()), "PREREG_INPUT_PIN_DRIFT", "live inputs differ from frozen v2 preregistration")
    require(prereg["status"] == "PREREGISTERED_NOT_RUN" and prereg["outcome_evaluated"] is False and prereg["selected_mode"].startswith("UNFROZEN_"), "PREREG_STATE", repr((prereg.get("status"), prereg.get("outcome_evaluated"), prereg.get("selected_mode"))))
    token_pin = validate_mode_token(Path(args.mode_token), args.mode_token_sha256, prereg_pin)
    require(args.receipt_rel and args.execution_manifest_rel, "VERSIONED_OUTPUT_PATHS_REQUIRED", "receipt and manifest")
    require(args.receipt_rel not in (PREREG_REL, LAUNCH_MANIFEST_REL) and args.execution_manifest_rel not in (PREREG_REL, LAUNCH_MANIFEST_REL), "OUTPUT_OVERWRITE_FORBIDDEN", repr((args.receipt_rel, args.execution_manifest_rel)))
    for rel in (args.receipt_rel, args.execution_manifest_rel):
        rel_path = Path(rel)
        require(not rel_path.is_absolute() and ".." not in rel_path.parts and rel_path.parts[:2] == ("search", "certs") and rel_path.suffix == ".json" and "_v" in rel_path.name, "VERSIONED_OUTPUT_PATH_CONTRACT", rel)

    raw = prereg["row36_raw_fibre"]["raw_roster"]
    require(len(raw) == 48 and digest(raw) == prereg["row36_raw_fibre"]["raw_roster_sha256"], "REGISTERED_RAW_ROSTER", str(len(raw)))
    derived, derived_trace = normal_closure_commutator_g36()
    gtheta = extend_generator_map(gid(), [gx(36), gy(36)], [gy(36), gx(36)], lambda a, b: gmul(a, b, 36), lambda a: ginv(a, 36))
    gtau = extend_generator_map(gid(), [gx(36), gy(36)], [gy(36), ginv(gmul(gx(36), gy(36), 36), 36)], lambda a, b: gmul(a, b, 36), lambda a: ginv(a, 36))
    ptheta = extend_generator_map(PSL_ID, [X_PSL, Y_PSL], [Y_PSL, X_PSL], pmul, pinv)
    ptau = extend_generator_map(PSL_ID, [X_PSL, Y_PSL], [Y_PSL, pinv(pmul(X_PSL, Y_PSL))], pmul, pinv)
    require(len(gtheta) == len(gtau) == 23328 and len(ptheta) == len(ptau) == 504, "ACTION_MAP_COVER", repr((len(gtheta), len(gtau), len(ptheta), len(ptau))))

    def cp_mul(left: Component, right: Component) -> Component:
        return (gmul(left[0], right[0], 36), (left[1] + right[1]) % 3)

    def cp_inv(value: Component) -> Component:
        return (ginv(value[0], 36), (-value[1]) % 3)

    cp_id: Component = (gid(), 0)
    cp_x: Component = (gx(36), 2)
    cp_y: Component = (gy(36), 2)
    trace = []
    stages: Counter[str] = Counter()
    for row in raw:
        m = int(row["m_mod_36"])
        g = decode_g(row["f"]["g36"])
        p = tuple(int(x) - 1 for x in row["f"]["psl_one_line"])
        c = int(row["f"]["c3_exp"]) % 3
        word = tuple(int(x) for x in row["source_word_signed_xy"])
        reduction_ok = m % 18 == 0 and reduce_g36(g) == ((4, 0), (5, 0), (0, 0)) and p == PSL_ID
        word_replay = eval_word_g(word, 36) == g and eval_word_perm(word) == p and eval_word_c3(word) == c
        unit = math.gcd(2 * m + 1, 36) == 1
        commutator_member = g in derived and c == 0  # PSL is perfect.
        h10 = h11 = onto = False
        onto_component_order = onto_psl_order = 0
        if reduction_ok and word_replay and unit and commutator_member:
            h10 = gmul(g, gtheta[g], 36) == gid() and pmul(p, ptheta[p]) == PSL_ID and (2 * c) % 3 == 0
            if h10:
                ymf_g = gmul(gpow(gy(36), m, 36), g, 36)
                ymf_p = pmul(ppow(Y_PSL, m), p)
                ymf_c = (2 * m + c) % 3
                h11 = gmul(gmul(gtau[gtau[ymf_g]], gtau[ymf_g], 36), ymf_g, 36) == gid() and pmul(pmul(ptau[ptau[ymf_p]], ptau[ymf_p]), ymf_p) == PSL_ID and (3 * ymf_c) % 3 == 0
                if h11:
                    u = 2 * m + 1
                    fcp: Component = (g, c)
                    gen_a = (gpow(gx(36), u, 36), (2 * u) % 3)
                    ypow = (gpow(gy(36), u, 36), (2 * u) % 3)
                    gen_b = cp_mul(cp_mul(cp_inv(fcp), ypow), fcp)
                    onto_component_order = len(closure(cp_id, [gen_a, gen_b], cp_mul, cp_inv))
                    gen_a_p = ppow(X_PSL, u)
                    gen_b_p = pmul(pmul(pinv(p), ppow(Y_PSL, u)), p)
                    onto_psl_order = len(closure(PSL_ID, [gen_a_p, gen_b_p], pmul, pinv))
                    onto = onto_component_order == 69984 and onto_psl_order == 504
        if not reduction_ok:
            stage = "reduction_fail"
        elif not word_replay:
            stage = "word_replay_fail"
        elif not unit:
            stage = "charming_unit_fail"
        elif not commutator_member:
            stage = "charming_commutator_fail"
        elif not h10:
            stage = "h10_fail"
        elif not h11:
            stage = "h11_fail"
        elif not onto:
            stage = "onto_fail"
        else:
            stage = "pass"
        stages[stage] += 1
        trace.append({"raw_id": row["raw_id"], "raw_row_sha256": row["row_sha256"], "reduction_ok": reduction_ok, "word_replay": word_replay, "charming_unit": unit, "charming_commutator": commutator_member, "h10": h10, "h11": h11, "onto": onto, "onto_component_order": onto_component_order, "onto_psl_order": onto_psl_order, "stage": stage})
    require(len(trace) == 48 and sum(stages.values()) == 48, "PREDICATE_TRACE_COVER", repr((len(trace), stages)))
    positives = [row for row in trace if row["stage"] == "pass"]
    claim_cover = {"claim_id": "CLAIM-COVER-RUNG-1", "registered_raw_count": 48, "evaluated_count": len(trace), "unique_raw_ids": len({row["raw_id"] for row in trace}), "rejected_count": 48 - len(positives), "positive_count": len(positives), "reason_histogram": dict(sorted(stages.items())), "trace_sha256": digest(trace), "no_early_stop": True, "complete": len(trace) == 48 and len({row["raw_id"] for row in trace}) == 48}
    require(claim_cover["complete"], "CLAIM_COVER_RUNG_1", repr(claim_cover))
    observation = "FIXED_ROW36_HAS_LIFT" if positives else "FULL_RAW_FIBRE_NO_LIFT"
    checker_snapshot = {
        "LINS_full_shell_authentication": prereg["LINS_full_shell_authentication"],
        "fair_shell_cover": prereg["fair_shell_cover"],
        "isolation_and_diamond": prereg["isolation_and_diamond"],
        "joint_marked_quotient": prereg["joint_marked_quotient"],
        "target": prereg["target"],
        "rung_and_control_rosters": prereg["rung_and_control_rosters"],
        "row36_raw_fibre": prereg["row36_raw_fibre"],
        "one_seed_predicate_contract": prereg["one_seed_predicate_contract"],
        "destructive_controls_and_mutants": prereg["destructive_controls_and_mutants"],
        "derived_reconstruction": prereg["derived_reconstruction"],
    }
    receipt = {
        "schema": "d972-rung-ordinary-idx3-producer-receipt/v2",
        "artifact_kind": "producer-only outcome candidate; independent replay required",
        "mode": MODE,
        "rung_name_assigned": False,
        "mode_token_pin": token_pin,
        "producer": pin(SOURCE_REL, expected=False),
        "preregistration": prereg_pin,
        "launch_manifest": launch_pin,
        "selected_node_id": NODE_ID,
        "registered_contract_snapshot": checker_snapshot,
        "registered_contract_snapshot_sha256": digest(checker_snapshot),
        "raw_roster_sha256": prereg["row36_raw_fibre"]["raw_roster_sha256"],
        "predicate_trace": trace,
        "CLAIM-COVER-RUNG-1": claim_cover,
        "registered_mutants": prereg["destructive_controls_and_mutants"],
        "mutant_execution_contract": "Independent checker must inject and reject every registered mutation; producer structural guards were active, but this receipt is not a checker verdict.",
        "producer_observation": observation,
        "terminal_token": "UNKNOWN_PENDING_INDEPENDENT_CHECKER_AND_PARENT_RUNG_ADJUDICATION",
        "cross_checked": False,
        "verified": False,
    }
    receipt_pin = write_new(args.receipt_rel, receipt)
    execution_manifest = {
        "schema": "d972-rung-ordinary-idx3-execution-manifest/v2",
        "mode": MODE,
        "rung_name_assigned": False,
        "producer": receipt["producer"],
        "preregistration": prereg_pin,
        "launch_manifest": launch_pin,
        "mode_token": {k: token_pin[k] for k in ("path", "bytes", "sha256")},
        "receipt": receipt_pin,
        "claim_cover_sha256": digest(claim_cover),
        "independent_checker_contract": {"author_separation_required": True, "checker_receives_only": [receipt_pin, "this manifest pin after writing"], "must_not_open_or_import": [SOURCE_REL, "producer helpers", "producer report"], "must_reconstruct_all_48": True, "must_inject_all_registered_mutants": True},
        "terminal_token": receipt["terminal_token"],
        "git_GHA_workflow_es7ops_actions": [],
    }
    execution_manifest_pin = write_new(args.execution_manifest_rel, execution_manifest)
    print(json.dumps({"receipt": receipt_pin, "execution_manifest": execution_manifest_pin, "producer_observation": observation, "terminal_token": receipt["terminal_token"]}, sort_keys=True))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prepare", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--mode-token")
    parser.add_argument("--mode-token-sha256")
    parser.add_argument("--receipt-rel")
    parser.add_argument("--execution-manifest-rel")
    args = parser.parse_args()
    if args.execute:
        require(bool(args.mode_token and args.mode_token_sha256), "MODE_TOKEN_REQUIRED", "--mode-token and --mode-token-sha256")
    return args


if __name__ == "__main__":
    parsed = parse_args()
    if parsed.prepare:
        prepare()
    else:
        execute(parsed)

