#!/usr/bin/env python3
"""Producer-side total ordinary K2 fibre roster over the frozen 972 roofs.

This is deliberately not an independent checker.  It authenticates and then
reuses the finite-group primitives and deterministic Schreier word lift from
``d972_rung_ordinary_idx3_producer_v2.py``.  The fixed-row36 receipt is replayed
as a lineage control before the same quotient/reduction law is applied to every
row of the frozen 972-row word-key artifact.

The full computation is intended for GitHub Actions.  ``--selftest`` performs
only input authentication, small-group tests, and destructive schema controls.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from copy import deepcopy
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys
import time
from types import ModuleType
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REL = "search/d972_k2_total_fibre_roster_producer_v1.py"
FIXED_PRODUCER_REL = "search/d972_rung_ordinary_idx3_producer_v2.py"
TUPLES_REL = "search/certs/nf972_sourcemap_a_tuples_v2_20260804.json"
WORDS_REL = "search/certs/d972_b4_word_key_artifact_v1_20260816.json"
PREREG_REL = "search/certs/d972_rung_ordinary_idx3_prereg_v2_20260824.json"
FIXED_RECEIPT_REL = (
    "ci/ordinary_idx3_artifacts_32682548731/"
    "d972_rung_ordinary_idx3_producer_receipt_v2_20260824.json"
)
DEFAULT_OUTPUT_REL = "ci/out/d972_k2_total_fibre_roster_v1_20260825.json"

SCHEMA = "d972-k2-total-fibre-roster-producer/v1"
FINAL_MARKER = "D972_K2_TOTAL_FIBRE_ROSTER_PRODUCER_V1_FINAL"
SELFTEST_MARKER = "D972_K2_TOTAL_FIBRE_ROSTER_SELFTEST_PASS"

EXPECTED = {
    FIXED_PRODUCER_REL: (
        54993,
        "b8dd453f7647dacc87356b13cb5428674a21bfabe6aa5af3850ac89129eb7211",
    ),
    TUPLES_REL: (
        43751,
        "cfa1f3a917e2cd9d21ceaa7f77539633ccb22e8585da8b3248609008d0391801",
    ),
    WORDS_REL: (
        176474,
        "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9",
    ),
    PREREG_REL: (
        46928,
        "1273f6050afaaba01f8dc137042ae191cecd91dea44a1618f665c2e3048e4656",
    ),
    FIXED_RECEIPT_REL: (
        62680,
        "48512270d265753944ff9b86d19fa5e84095ffffd8ae78beba969088c31053e9",
    ),
    "search/certs/b3_gentle_source_census_preflight_v1_20260823.json": (
        887124,
        "c30077133305c07ca0e58c9eaa700d42a512a6bbbce96c9c27d161e921e1aaf2",
    ),
    "crosscheck/verdicts/b3_gentle_source_census_v1_20260823.json": (
        4931,
        "e308a71323dc429d771d7fb86f507b3c17936716505dd6ca3ee3fbfdeecf7f4e",
    ),
    "certificates/K36.v1.json": (
        727834,
        "feac2a0202e5b78a017272a972e105ac7daf7eb5ca0b4de102b6664b098d8719",
    ),
    "crosscheck/verdicts/K36.v1.verdict.json": (
        71093,
        "4436da2643a0577b06761cd310f0032d98fefe67bab10c16f74c534aabb1a92b",
    ),
    "certificates/K9.v1.json": (
        173224,
        "ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e",
    ),
    "crosscheck/verdicts/K9.v1.verdict.json": (
        20991,
        "9c299baba6cd3c49296621ecfe5efbc260d7971fa874f44465fa5e968cc065f9",
    ),
    "certificates/S4.v2.json": (
        287984,
        "c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d",
    ),
    "crosscheck/verdicts/S4.psl.verdict.json": (
        470,
        "8d9d98965e270c2130b56fd6240c3b7460fe906ef5523f5e90396280dd043b28",
    ),
}


def canonical_compact(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")


def digest(value: object) -> str:
    return hashlib.sha256(canonical_compact(value)).hexdigest()


def fail(code: str, detail: str) -> None:
    raise RuntimeError(f"STATE_STOP {code}: {detail}")


def require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        fail(code, detail)


def pin(rel: str) -> dict:
    require(rel in EXPECTED, "UNREGISTERED_INPUT", rel)
    path = ROOT / rel
    require(path.is_file(), "MISSING_INPUT", rel)
    raw = path.read_bytes()
    record = {
        "path": rel,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
    require(
        (record["bytes"], record["sha256"]) == EXPECTED[rel],
        "INPUT_PIN_MISMATCH",
        repr(record),
    )
    return record


def load_json(rel: str) -> object:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def authenticate_inputs() -> tuple[list[dict], dict, dict, dict, dict]:
    pins = [pin(rel) for rel in EXPECTED]
    tuples = load_json(TUPLES_REL)
    words = load_json(WORDS_REL)
    prereg = load_json(PREREG_REL)
    receipt = load_json(FIXED_RECEIPT_REL)
    require(isinstance(tuples, dict), "TUPLES_TYPE", type(tuples).__name__)
    require(isinstance(words, dict), "WORDS_TYPE", type(words).__name__)
    require(
        tuples.get("schema") == "nf972-sourcemap-a-tuples/v2"
        and tuples.get("count") == 972
        and len(tuples.get("tuples", [])) == 972,
        "TUPLES_SCHEMA",
        repr({k: tuples.get(k) for k in ("schema", "count")}),
    )
    require(
        words.get("schema") == "d972-b4-word-key-artifact/v1"
        and words.get("count") == 972
        and len(words.get("rows", [])) == 972,
        "WORDS_SCHEMA",
        repr({k: words.get(k) for k in ("schema", "count")}),
    )
    require(
        digest(tuples["tuples"])
        == tuples["canonical_bytes_sha256"]
        == "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91",
        "TUPLE_ROSTER_DIGEST",
        digest(tuples["tuples"]),
    )
    require(
        [row[1] for row in words["rows"]] == tuples["tuples"],
        "WORD_TUPLE_ORDER_BINDING",
        "word-key targets differ from frozen tuple order",
    )
    require(
        digest(words["rows"])
        == words["canonical_bytes_sha256"]
        == "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930",
        "WORD_ROSTER_DIGEST",
        digest(words["rows"]),
    )
    require(
        prereg.get("schema") == "d972-rung-ordinary-idx3-prereg/v2"
        and prereg.get("status") == "PREREGISTERED_NOT_RUN",
        "FIXED_PREREG_SCHEMA",
        repr((prereg.get("schema"), prereg.get("status"))),
    )
    require(
        receipt.get("schema") == "d972-rung-ordinary-idx3-producer-receipt/v2"
        and receipt.get("cross_checked") is False
        and receipt.get("verified") is False,
        "FIXED_RECEIPT_SCHEMA",
        repr(
            (
                receipt.get("schema"),
                receipt.get("cross_checked"),
                receipt.get("verified"),
            )
        ),
    )
    return pins, tuples, words, prereg, receipt


def load_fixed_producer() -> ModuleType:
    # The source was byte/SHA authenticated before this function is called.
    path = ROOT / FIXED_PRODUCER_REL
    spec = importlib.util.spec_from_file_location("d972_fixed_row36_v2", path)
    require(spec is not None and spec.loader is not None, "FIXED_IMPORT_SPEC", str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def determinant(matrix: Sequence[Sequence[int]]) -> int:
    """Exact Bareiss determinant (the matrices here have dimension at most 4)."""
    n = len(matrix)
    require(n > 0 and all(len(row) == n for row in matrix), "DET_SHAPE", repr(matrix))
    work = [list(map(int, row)) for row in matrix]
    sign = 1
    previous = 1
    for k in range(n - 1):
        pivot = next((r for r in range(k, n) if work[r][k] != 0), None)
        if pivot is None:
            return 0
        if pivot != k:
            work[k], work[pivot] = work[pivot], work[k]
            sign *= -1
        value = work[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = work[i][j] * value - work[i][k] * work[k][j]
                require(numerator % previous == 0, "BAREISS_DIVISION", repr(matrix))
                work[i][j] = numerator // previous
        previous = value
        for i in range(k + 1, n):
            work[i][k] = 0
    return sign * work[-1][-1]


def p_valuation(value: int, prime: int) -> int:
    require(value != 0, "VALUATION_ZERO", str(prime))
    value = abs(value)
    exponent = 0
    while value % prime == 0:
        value //= prime
        exponent += 1
    return exponent


def exponent_in(value: int, prime: int) -> int:
    exponent = 0
    while value % prime == 0:
        value //= prime
        exponent += 1
    return exponent


def additive_subgroup_order(
    generators: Iterable[Sequence[int]], moduli: Sequence[int]
) -> int:
    """Order of a generated subgroup of a product of cyclic groups.

    For each primary part, the quotient has presentation rows consisting of
    the diagonal modulus relations and the supplied generators.  Its order is
    the gcd of maximal minors; only the corresponding p-valuation is needed.
    """
    moduli = tuple(map(int, moduli))
    rows = [tuple(int(x) for x in row) for row in generators]
    require(all(len(row) == len(moduli) for row in rows), "ADDITIVE_ROW_SHAPE", repr(rows[:1]))
    primes: list[int] = []
    for modulus in moduli:
        require(modulus > 0, "BAD_MODULUS", str(modulus))
        rest = modulus
        candidate = 2
        while candidate * candidate <= rest:
            if rest % candidate == 0:
                primes.append(candidate)
                while rest % candidate == 0:
                    rest //= candidate
            candidate += 1
        if rest > 1:
            primes.append(rest)
    order = 1
    for prime in sorted(set(primes)):
        active = [i for i, modulus in enumerate(moduli) if modulus % prime == 0]
        powers = [prime ** exponent_in(moduli[i], prime) for i in active]
        dimension = len(active)
        ambient_exponent = sum(exponent_in(moduli[i], prime) for i in active)
        presentation: list[list[int]] = []
        for i, power in enumerate(powers):
            diagonal = [0] * dimension
            diagonal[i] = power
            presentation.append(diagonal)
        presentation.extend(
            [[row[index] % powers[j] for j, index in enumerate(active)] for row in rows]
        )
        minimum = ambient_exponent
        for choice in itertools.combinations(presentation, dimension):
            det = determinant(choice)
            if det == 0:
                continue
            minimum = min(minimum, p_valuation(det, prime))
            if minimum == 0:
                break
        require(0 <= minimum <= ambient_exponent, "SMITH_VALUATION_RANGE", repr((prime, minimum)))
        order *= prime ** (ambient_exponent - minimum)
    return order


def component_order_exact(fixed: ModuleType, m: int, g: tuple) -> int:
    """Exact order of the onto-test subgroup in G36 x C3 without Cayley BFS."""
    modulus = 36
    u = 2 * m + 1
    alpha = (2 * u) % 3
    a = fixed.gpow(fixed.gx(modulus), u, modulus)
    b = fixed.gmul(
        fixed.gmul(fixed.ginv(g, modulus), fixed.gpow(fixed.gy(modulus), u, modulus), modulus),
        g,
        modulus,
    )
    expected_a_e = fixed.gx(modulus)
    expected_b_e = fixed.gy(modulus)
    require(
        tuple(part[1] for part in a) == tuple(part[1] for part in expected_a_e)
        and tuple(part[1] for part in b) == tuple(part[1] for part in expected_b_e),
        "ONTO_V4_PROJECTION",
        repr((a, b)),
    )

    def cp_mul(left: tuple[tuple, int], right: tuple[tuple, int]) -> tuple[tuple, int]:
        return (
            fixed.gmul(left[0], right[0], modulus),
            (left[1] + right[1]) % 3,
        )

    def cp_inv(value: tuple[tuple, int]) -> tuple[tuple, int]:
        return (fixed.ginv(value[0], modulus), (-value[1]) % 3)

    aa = (a, alpha)
    bb = (b, alpha)
    ab = cp_mul(aa, bb)
    relators = [cp_mul(aa, aa), cp_mul(bb, bb), cp_mul(ab, ab)]
    representatives = [
        (fixed.gid(), 0),
        aa,
        bb,
        ab,
    ]
    additive_generators: list[tuple[int, int, int, int]] = []
    for relator in relators:
        for by in representatives:
            conjugate = cp_mul(cp_mul(cp_inv(by), relator), by)
            require(
                all(e == 0 and translation % 2 == 0 for translation, e in conjugate[0]),
                "ONTO_KERNEL_TRANSLATION",
                repr(conjugate),
            )
            additive_generators.append(
                tuple(translation // 2 for translation, _ in conjugate[0])
                + (conjugate[1],)
            )
    kernel_order = additive_subgroup_order(additive_generators, (18, 18, 18, 3))
    return 4 * kernel_order


def component_order_bruteforce(fixed: ModuleType, modulus: int, m: int, g: tuple) -> int:
    """Small-modulus control used only by selftest."""
    u = 2 * m + 1
    alpha = (2 * u) % 3
    a = (fixed.gpow(fixed.gx(modulus), u, modulus), alpha)
    y = fixed.gpow(fixed.gy(modulus), u, modulus)
    b_g = fixed.gmul(fixed.gmul(fixed.ginv(g, modulus), y, modulus), g, modulus)
    b = (b_g, alpha)

    def mul(left: tuple[tuple, int], right: tuple[tuple, int]) -> tuple[tuple, int]:
        return (fixed.gmul(left[0], right[0], modulus), (left[1] + right[1]) % 3)

    def inv(value: tuple[tuple, int]) -> tuple[tuple, int]:
        return (fixed.ginv(value[0], modulus), (-value[1]) % 3)

    return len(fixed.closure((fixed.gid(), 0), [a, b], mul, inv))


def component_order_formula_generic(fixed: ModuleType, modulus: int, m: int, g: tuple) -> int:
    require(modulus % 2 == 0, "GENERIC_MODULUS_PARITY", str(modulus))
    u = 2 * m + 1
    alpha = (2 * u) % 3
    a = fixed.gpow(fixed.gx(modulus), u, modulus)
    b = fixed.gmul(
        fixed.gmul(fixed.ginv(g, modulus), fixed.gpow(fixed.gy(modulus), u, modulus), modulus),
        g,
        modulus,
    )

    def mul(left: tuple[tuple, int], right: tuple[tuple, int]) -> tuple[tuple, int]:
        return (fixed.gmul(left[0], right[0], modulus), (left[1] + right[1]) % 3)

    def inv(value: tuple[tuple, int]) -> tuple[tuple, int]:
        return (fixed.ginv(value[0], modulus), (-value[1]) % 3)

    aa, bb = (a, alpha), (b, alpha)
    ab = mul(aa, bb)
    additive = []
    for relator in (mul(aa, aa), mul(bb, bb), mul(ab, ab)):
        for by in ((fixed.gid(), 0), aa, bb, ab):
            conjugate = mul(mul(inv(by), relator), by)
            require(
                all(e == 0 and translation % 2 == 0 for translation, e in conjugate[0]),
                "GENERIC_KERNEL_TRANSLATION",
                repr(conjugate),
            )
            additive.append(
                tuple(translation // 2 for translation, _ in conjugate[0])
                + (conjugate[1],)
            )
    return 4 * additive_subgroup_order(
        additive, (modulus // 2, modulus // 2, modulus // 2, 3)
    )


def decode_g36(fixed: ModuleType, value: list[list[int]]) -> tuple:
    require(
        isinstance(value, list)
        and len(value) == 3
        and all(isinstance(pair, list) and len(pair) == 2 for pair in value),
        "G36_ENCODING",
        repr(value),
    )
    return tuple((int(a) % 36, int(e) % 2) for a, e in value)


def decode_g9(value: list[list[int]]) -> tuple:
    require(
        isinstance(value, list)
        and len(value) == 3
        and all(isinstance(pair, list) and len(pair) == 2 for pair in value),
        "G9_ENCODING",
        repr(value),
    )
    return tuple((int(a) % 9, int(e) % 2) for a, e in value)


def decode_perm(value: list[int]) -> tuple[int, ...]:
    result = tuple(int(image) - 1 for image in value)
    require(sorted(result) == list(range(9)), "PERM_ENCODING", repr(value))
    return result


def source_pair(fixed: ModuleType, m: int, g: tuple, p: tuple[int, ...], c: int) -> list:
    # Exact serialized [m,f] convention for this artifact.
    return [
        m,
        [m, fixed.encode_g(g), fixed.encode_perm(p), c % 3],
    ]


def coordinate_lookup_key(pair: list) -> str:
    return canonical_compact(pair).decode("ascii")


def first_failure(predicates: dict) -> str:
    order = (
        ("exact_reduction", "reduction_fail"),
        ("source_word_replay", "word_replay_fail"),
        ("charming_unit", "charming_unit_fail"),
        ("charming_commutator", "charming_commutator_fail"),
        ("hexagon_h10", "h10_fail"),
        ("hexagon_h11", "h11_fail"),
        ("onto", "onto_fail"),
    )
    for key, stage in order:
        if not predicates[key]:
            return stage
    return "pass"


def validate_result(
    result: dict, expected_targets: int = 972, expected_raw_per_target: int = 48
) -> None:
    require(result.get("schema") == SCHEMA, "RESULT_SCHEMA", repr(result.get("schema")))
    claim = result.get("claim_cover", {})
    raw = result.get("raw_roster", [])
    valid = result.get("valid_roster", [])
    targets = result.get("per_target", [])
    lookup = result.get("coordinate_to_valid_id", {})
    require(
        claim.get("target_count") == len(targets) == expected_targets,
        "TARGET_COVER",
        repr((claim.get("target_count"), len(targets), expected_targets)),
    )
    require(
        claim.get("raw_count")
        == claim.get("evaluated_count")
        == len(raw)
        == expected_targets * expected_raw_per_target,
        "RAW_COVER",
        repr((claim.get("raw_count"), claim.get("evaluated_count"), len(raw))),
    )
    raw_ids = [row["raw_id"] for row in raw]
    require(len(set(raw_ids)) == len(raw_ids), "RAW_ID_UNIQUENESS", str(len(set(raw_ids))))
    require(all(row["stage"] == first_failure(row["predicates"]) for row in raw), "STAGE_REPLAY", "first-failure mismatch")
    observed_reasons = dict(sorted(Counter(row["stage"] for row in raw).items()))
    require(
        claim.get("reason_histogram") == observed_reasons,
        "REASON_HISTOGRAM",
        repr((claim.get("reason_histogram"), observed_reasons)),
    )
    for row in raw:
        require(
            digest(row["source_word_signed_xy"]) == row["source_word_sha256"],
            "RAW_WORD_DIGEST",
            row["raw_id"],
        )
        core = {
            key: value
            for key, value in row.items()
            if key not in ("raw_record_sha256", "valid_id")
        }
        require(
            digest(core) == row["raw_record_sha256"],
            "RAW_RECORD_DIGEST",
            row["raw_id"],
        )
    valid_raw = [row for row in raw if row["stage"] == "pass"]
    require(len(valid) == len(valid_raw) == claim.get("valid_count"), "VALID_COUNT", repr((len(valid), len(valid_raw), claim.get("valid_count"))))
    valid_ids = [row["valid_id"] for row in valid]
    require(len(set(valid_ids)) == len(valid_ids), "VALID_ID_UNIQUENESS", str(len(set(valid_ids))))
    require(set(lookup.values()) == set(valid_ids) and len(lookup) == len(valid), "LOOKUP_COVER", repr((len(lookup), len(valid))))
    for row in valid:
        require(
            lookup.get(coordinate_lookup_key(row["source_pair_m_f"])) == row["valid_id"],
            "LOOKUP_ROUNDTRIP",
            row["valid_id"],
        )
    by_target: dict[str, list[dict]] = defaultdict(list)
    for row in raw:
        by_target[row["target_id"]].append(row)
    observed_histogram = Counter()
    all_target_valid_ids: list[str] = []
    for target in targets:
        rows = by_target[target["target_id"]]
        require(
            len(rows) == target["raw_count"] == expected_raw_per_target,
            "TARGET_RAW_COVER",
            target["target_id"],
        )
        require([row["raw_id"] for row in rows] == target["raw_ids"], "TARGET_RAW_BINDING", target["target_id"])
        ids = [row["valid_id"] for row in rows if row["stage"] == "pass"]
        require(ids == target["valid_ids"] and len(ids) == target["valid_count"], "TARGET_VALID_BINDING", target["target_id"])
        require(
            [entry["valid_id"] for entry in target["valid_fibre"]] == ids,
            "TARGET_VALID_FIBRE_IDS",
            target["target_id"],
        )
        for entry, row in zip(target["valid_fibre"], (row for row in rows if row["stage"] == "pass")):
            require(
                entry["source_pair_m_f"] == row["source_pair_m_f"]
                and entry["source_word_signed_xy"] == row["source_word_signed_xy"]
                and entry["source_word_sha256"] == row["source_word_sha256"],
                "TARGET_VALID_FIBRE_COORDINATE",
                entry["valid_id"],
            )
        require(digest(target["raw_ids"]) == target["raw_id_roster_sha256"], "TARGET_RAW_DIGEST", target["target_id"])
        require(digest(target["valid_ids"]) == target["valid_id_roster_sha256"], "TARGET_VALID_DIGEST", target["target_id"])
        observed_histogram[target["valid_count"]] += 1
        all_target_valid_ids.extend(ids)
    expected_histogram = {str(k): v for k, v in sorted(observed_histogram.items())}
    require(result.get("valid_count_histogram") == expected_histogram, "VALID_HISTOGRAM", repr(expected_histogram))
    require(all_target_valid_ids == valid_ids, "VALID_TARGET_ORDER", "per-target order differs")
    require(
        claim.get("rejected_count") == len(raw) - len(valid)
        and claim.get("valid_count") == len(valid),
        "CLAIM_COUNTS",
        repr(claim),
    )
    require(claim.get("no_early_stop") is True and claim.get("complete") is True, "CLAIM_COMPLETE", repr(claim))


def selftest() -> None:
    authenticate_inputs()
    fixed = load_fixed_producer()
    require(determinant([[1, 2], [3, 4]]) == -2, "SELFTEST_DET", "2x2")
    require(additive_subgroup_order([(1, 0)], (6, 4)) == 6, "SELFTEST_SMITH_A", "C6")
    require(additive_subgroup_order([(2, 0), (0, 2)], (6, 4)) == 6, "SELFTEST_SMITH_B", "C3xC2")
    mutations = 0
    for modulus in (4, 6):
        sample_g = fixed.gmul(fixed.gx(modulus), fixed.gy(modulus), modulus)
        for m in (0, 1, 2):
            formula = component_order_formula_generic(fixed, modulus, m, sample_g)
            brute = component_order_bruteforce(fixed, modulus, m, sample_g)
            require(formula == brute, "SELFTEST_ONTO_FORMULA", repr((modulus, m, formula, brute)))
    require(
        fixed.eval_word_perm((1, 2)) != fixed.eval_word_perm((2, 1)),
        "SELFTEST_NONCOMMUTATIVE_WORD_CONTROL",
        "xy unexpectedly equals yx",
    )
    mutations += 1

    p1 = source_pair(fixed, 0, fixed.gid(), fixed.PSL_ID, 0)
    p2 = source_pair(fixed, 18, fixed.gid(), fixed.PSL_ID, 0)
    toy_raw = []
    for index, (target, pair, passed) in enumerate((("X0001", p1, True), ("X0002", p2, False)), 1):
        predicates = {
            "exact_reduction": True,
            "source_word_replay": True,
            "charming_unit": True,
            "charming_commutator": True,
            "hexagon_h10": True,
            "hexagon_h11": True,
            "onto": passed,
        }
        toy_raw.append(
            {
                "raw_id": f"R{index}",
                "target_id": target,
                "source_pair_m_f": pair,
                "predicates": predicates,
                "stage": first_failure(predicates),
                "valid_id": "V1" if passed else None,
            }
        )
    toy = {
        "schema": SCHEMA,
        "raw_roster": toy_raw,
        "valid_roster": [{"valid_id": "V1", "source_pair_m_f": p1}],
        "coordinate_to_valid_id": {coordinate_lookup_key(p1): "V1"},
        "per_target": [
            {"target_id": "X0001", "raw_count": 1, "raw_ids": ["R1"], "raw_id_roster_sha256": digest(["R1"]), "valid_count": 1, "valid_ids": ["V1"], "valid_id_roster_sha256": digest(["V1"]), "valid_fibre": [{"valid_id": "V1", "source_pair_m_f": p1, "source_word_signed_xy": [], "source_word_sha256": digest([])}]},
            {"target_id": "X0002", "raw_count": 1, "raw_ids": ["R2"], "raw_id_roster_sha256": digest(["R2"]), "valid_count": 0, "valid_ids": [], "valid_id_roster_sha256": digest([]), "valid_fibre": []},
        ],
        "valid_count_histogram": {"0": 1, "1": 1},
        "claim_cover": {"target_count": 2, "raw_count": 2, "evaluated_count": 2, "rejected_count": 1, "valid_count": 1, "reason_histogram": {"onto_fail": 1, "pass": 1}, "no_early_stop": True, "complete": True},
    }

    for row in toy["raw_roster"]:
        row["source_word_signed_xy"] = []
        row["source_word_sha256"] = digest([])
        core = {key: value for key, value in row.items() if key not in ("raw_record_sha256", "valid_id")}
        row["raw_record_sha256"] = digest(core)

    validate_result(toy, expected_targets=2, expected_raw_per_target=1)
    for label, mutate in (
        ("drop_raw", lambda x: x["raw_roster"].pop()),
        ("duplicate_raw_id", lambda x: x["raw_roster"][-1].update(raw_id=x["raw_roster"][0]["raw_id"])),
        ("lookup_drop", lambda x: x["coordinate_to_valid_id"].pop(next(iter(x["coordinate_to_valid_id"])))),
        ("histogram_forge", lambda x: x.update(valid_count_histogram={"48": 971})),
        ("target_binding", lambda x: x["per_target"][0].update(raw_ids=["R2"])),
        ("h10_bit", lambda x: x["raw_roster"][0]["predicates"].update(hexagon_h10=False)),
        ("reduction_bit", lambda x: x["raw_roster"][0]["predicates"].update(exact_reduction=False)),
    ):
        mutant = deepcopy(toy)
        mutate(mutant)
        try:
            validate_result(mutant, expected_targets=2, expected_raw_per_target=1)
        except RuntimeError:
            mutations += 1
        else:
            fail("SELFTEST_MUTANT_SURVIVED", label)
    print(f"{SELFTEST_MARKER} mutations={mutations} small_component_cases=6 inputs={len(EXPECTED)}")


def execute(output_rel: str) -> None:
    started = time.monotonic()
    pins, tuples, words_artifact, prereg, fixed_receipt = authenticate_inputs()
    fixed = load_fixed_producer()
    output_path = (ROOT / output_rel).resolve()
    allowed_root = (ROOT / "ci" / "out").resolve()
    require(output_path.parent == allowed_root, "OUTPUT_DIRECTORY", str(output_path))
    require(output_path.name == Path(DEFAULT_OUTPUT_REL).name, "OUTPUT_FILENAME", output_path.name)
    require(not output_path.exists(), "OUTPUT_PREEXISTS", output_rel)

    print("D972_K2_TOTAL_FIBRE_ROSTER_INPUTS_PASS count=" + str(len(pins)), flush=True)
    trans_words, trans_psl, trans_c3 = fixed.build_g36_transversal()
    corrections, schreier_trace = fixed.residual_correction_words(trans_words, trans_psl, trans_c3)
    lifts_by_g9: dict[tuple, list[tuple]] = defaultdict(list)
    for g in trans_words:
        lifts_by_g9[fixed.reduce_g36(g)].append(g)
    for g9 in lifts_by_g9:
        lifts_by_g9[g9].sort(key=lambda value: tuple(x for pair in value for x in pair))
        require(len(lifts_by_g9[g9]) == 8, "G36_G9_FIBRE", repr((g9, len(lifts_by_g9[g9]))))
    require(len(lifts_by_g9) * 8 == 23328, "G36_G9_PARTITION", str(len(lifts_by_g9)))

    derived, derived_trace = fixed.normal_closure_commutator_g36()
    mul36 = lambda a, b: fixed.gmul(a, b, 36)
    inv36 = lambda a: fixed.ginv(a, 36)
    gtheta = fixed.extend_generator_map(fixed.gid(), [fixed.gx(36), fixed.gy(36)], [fixed.gy(36), fixed.gx(36)], mul36, inv36)
    gtau = fixed.extend_generator_map(fixed.gid(), [fixed.gx(36), fixed.gy(36)], [fixed.gy(36), fixed.ginv(fixed.gmul(fixed.gx(36), fixed.gy(36), 36), 36)], mul36, inv36)
    ptheta = fixed.extend_generator_map(fixed.PSL_ID, [fixed.X_PSL, fixed.Y_PSL], [fixed.Y_PSL, fixed.X_PSL], fixed.pmul, fixed.pinv)
    ptau = fixed.extend_generator_map(fixed.PSL_ID, [fixed.X_PSL, fixed.Y_PSL], [fixed.Y_PSL, fixed.pinv(fixed.pmul(fixed.X_PSL, fixed.Y_PSL))], fixed.pmul, fixed.pinv)
    require((len(gtheta), len(gtau), len(ptheta), len(ptau)) == (23328, 23328, 504, 504), "ACTION_MAP_COVER", repr((len(gtheta), len(gtau), len(ptheta), len(ptau))))

    target_rows = words_artifact["rows"]
    # Authenticate every frozen representative before lifting any target.
    for index, row in enumerate(target_rows):
        require(isinstance(row, list) and len(row) == 3, "TARGET_ROW_SHAPE", str(index))
        outer_m, target_key, target_word = row
        require(isinstance(target_key, list) and len(target_key) == 3 and int(outer_m) == int(target_key[0]), "TARGET_M_BINDING", str(index))
        target_g9 = decode_g9(target_key[1])
        target_p = decode_perm(target_key[2])
        signed = tuple(map(int, target_word))
        require(all(abs(letter) in (1, 2) for letter in signed), "TARGET_WORD_ALPHABET", str(index))
        require(fixed.eval_word_g(signed, 9) == target_g9 and fixed.eval_word_perm(signed) == target_p, "TARGET_WORD_REPLAY", str(index))

    raw_roster: list[dict] = []
    valid_roster: list[dict] = []
    per_target: list[dict] = []
    lookup: dict[str, str] = {}
    reason_histogram: Counter[str] = Counter()
    valid_count_histogram: Counter[int] = Counter()
    component_cache: dict[tuple, int] = {}
    psl_cache: dict[tuple, int] = {}

    fixed_prereg_rows = prereg["row36_raw_fibre"]["raw_roster"]
    fixed_trace_by_id = {row["raw_id"]: row for row in fixed_receipt["predicate_trace"]}
    row36_local_records: list[dict] = []

    for target_index, target_row in enumerate(target_rows):
        target_id = f"X{target_index + 1:04d}"
        target_m = int(target_row[0])
        target_key = target_row[1]
        target_g9 = decode_g9(target_key[1])
        target_p = decode_perm(target_key[2])
        target_word = list(map(int, target_row[2]))
        lifts = lifts_by_g9[target_g9]
        local_records: list[dict] = []
        for source_m in (target_m, target_m + 18):
            for g in lifts:
                base_word = trans_words[g]
                for c in range(3):
                    correction_key = (
                        fixed.pmul(fixed.pinv(trans_psl[g]), target_p),
                        (c - trans_c3[g]) % 3,
                    )
                    require(correction_key in corrections, "RESIDUAL_CORRECTION_MISSING", repr((target_index, correction_key)))
                    source_word = base_word + corrections[correction_key]
                    local_ordinal = len(local_records) + 1
                    raw_id = f"K2RAW-{target_id}-R{local_ordinal:02d}"
                    pair = source_pair(fixed, source_m, g, target_p, c)
                    reduced_key = [
                        source_m % 18,
                        fixed.encode_g(fixed.reduce_g36(g)),
                        fixed.encode_perm(target_p),
                    ]
                    exact_reduction = reduced_key == target_key
                    word_replay = (
                        fixed.eval_word_g(source_word, 36) == g
                        and fixed.eval_word_perm(source_word) == target_p
                        and fixed.eval_word_c3(source_word) == c
                    )
                    unit = math.gcd(2 * source_m + 1, 36) == 1
                    commutator_member = g in derived and c == 0
                    h10 = (
                        fixed.gmul(g, gtheta[g], 36) == fixed.gid()
                        and fixed.pmul(target_p, ptheta[target_p]) == fixed.PSL_ID
                        and (2 * c) % 3 == 0
                    )
                    ymf_g = fixed.gmul(fixed.gpow(fixed.gy(36), source_m, 36), g, 36)
                    ymf_p = fixed.pmul(fixed.ppow(fixed.Y_PSL, source_m), target_p)
                    ymf_c = (2 * source_m + c) % 3
                    h11 = (
                        fixed.gmul(fixed.gmul(gtau[gtau[ymf_g]], gtau[ymf_g], 36), ymf_g, 36) == fixed.gid()
                        and fixed.pmul(fixed.pmul(ptau[ptau[ymf_p]], ptau[ymf_p]), ymf_p) == fixed.PSL_ID
                        and (3 * ymf_c) % 3 == 0
                    )
                    u = 2 * source_m + 1
                    component_key = (u % 36, g)
                    if component_key not in component_cache:
                        component_cache[component_key] = component_order_exact(fixed, source_m, g)
                    psl_key = (u, target_p)
                    if psl_key not in psl_cache:
                        gen_a_p = fixed.ppow(fixed.X_PSL, u)
                        gen_b_p = fixed.pmul(fixed.pmul(fixed.pinv(target_p), fixed.ppow(fixed.Y_PSL, u)), target_p)
                        psl_cache[psl_key] = len(fixed.closure(fixed.PSL_ID, [gen_a_p, gen_b_p], fixed.pmul, fixed.pinv))
                    component_order = component_cache[component_key]
                    psl_order = psl_cache[psl_key]
                    onto = component_order == 69984 and psl_order == 504
                    predicates = {
                        "exact_reduction": exact_reduction,
                        "source_word_replay": word_replay,
                        "charming_unit": unit,
                        "charming_commutator": commutator_member,
                        "charming": unit and commutator_member,
                        "hexagon_h10": h10,
                        "hexagon_h11": h11,
                        "onto_component_order": component_order,
                        "onto_psl_order": psl_order,
                        "onto": onto,
                    }
                    stage = first_failure(predicates)
                    core = {
                        "raw_id": raw_id,
                        "target_id": target_id,
                        "target_index_zero_based": target_index,
                        "local_raw_ordinal": local_ordinal,
                        "source_pair_m_f": pair,
                        "source_word_signed_xy": list(source_word),
                        "source_word_sha256": digest(list(source_word)),
                        "reduced_target_key": reduced_key,
                        "predicates": predicates,
                        "stage": stage,
                    }
                    core["raw_record_sha256"] = digest(core)
                    core["valid_id"] = None
                    if stage == "pass":
                        valid_id = f"K2V{len(valid_roster) + 1:06d}"
                        core["valid_id"] = valid_id
                        lookup_key = coordinate_lookup_key(pair)
                        require(lookup_key not in lookup, "VALID_COORDINATE_DUPLICATE", lookup_key)
                        lookup[lookup_key] = valid_id
                        valid_roster.append(
                            {
                                "valid_id": valid_id,
                                "raw_id": raw_id,
                                "target_id": target_id,
                                "source_pair_m_f": pair,
                                "source_word_signed_xy": list(source_word),
                                "source_word_sha256": core["source_word_sha256"],
                                "raw_record_sha256": core["raw_record_sha256"],
                            }
                        )
                    reason_histogram[stage] += 1
                    raw_roster.append(core)
                    local_records.append(core)

        require(len(local_records) == 48, "TARGET_RAW_CARDINALITY", repr((target_id, len(local_records))))
        valid_ids = [row["valid_id"] for row in local_records if row["valid_id"] is not None]
        valid_fibre = [
            {
                "valid_id": row["valid_id"],
                "source_pair_m_f": row["source_pair_m_f"],
                "source_word_signed_xy": row["source_word_signed_xy"],
                "source_word_sha256": row["source_word_sha256"],
            }
            for row in local_records
            if row["valid_id"] is not None
        ]
        valid_count_histogram[len(valid_ids)] += 1
        raw_ids = [row["raw_id"] for row in local_records]
        per_target.append(
            {
                "target_id": target_id,
                "target_index_zero_based": target_index,
                "target_tuple": target_row,
                "target_tuple_sha256": digest(target_row),
                "target_word_sha256": digest(target_word),
                "raw_count": len(raw_ids),
                "raw_ids": raw_ids,
                "raw_id_roster_sha256": digest(raw_ids),
                "valid_count": len(valid_ids),
                "valid_ids": valid_ids,
                "valid_id_roster_sha256": digest(valid_ids),
                "valid_fibre": valid_fibre,
                "valid_fibre_sha256": digest(valid_fibre),
                "reason_histogram": dict(sorted(Counter(row["stage"] for row in local_records).items())),
            }
        )
        if target_index == 36:
            row36_local_records = local_records
        if (target_index + 1) % 27 == 0 or target_index + 1 == 972:
            print(
                f"D972_K2_TOTAL_FIBRE_PROGRESS targets={target_index + 1}/972 "
                f"raw={len(raw_roster)} valid={len(valid_roster)} "
                f"component_cache={len(component_cache)} psl_cache={len(psl_cache)}",
                flush=True,
            )

    # Exact fixed-row36 lineage replay: same coordinate and signed-word roster,
    # same first-failure stages, and every fixed receipt onto order that was run.
    require(len(row36_local_records) == len(fixed_prereg_rows) == 48, "ROW36_LINEAGE_COUNT", str(len(row36_local_records)))
    for local_index, (observed, registered) in enumerate(zip(row36_local_records, fixed_prereg_rows), 1):
        observed_projection = {
            "m_mod_36": observed["source_pair_m_f"][0],
            "f": {
                "g36": observed["source_pair_m_f"][1][1],
                "psl_one_line": observed["source_pair_m_f"][1][2],
                "c3_exp": observed["source_pair_m_f"][1][3],
            },
            "source_word_signed_xy": observed["source_word_signed_xy"],
            "source_word_sha256": observed["source_word_sha256"],
        }
        registered_projection = {key: registered[key] for key in observed_projection}
        require(observed_projection == registered_projection, "ROW36_WORD_LINEAGE", str(local_index))
        old = fixed_trace_by_id[f"R{local_index:02d}"]
        require(observed["stage"] == old["stage"], "ROW36_STAGE_LINEAGE", repr((local_index, observed["stage"], old["stage"])))
        if old["onto_component_order"]:
            require(observed["predicates"]["onto_component_order"] == old["onto_component_order"], "ROW36_COMPONENT_ORDER_LINEAGE", str(local_index))
        if old["onto_psl_order"]:
            require(observed["predicates"]["onto_psl_order"] == old["onto_psl_order"], "ROW36_PSL_ORDER_LINEAGE", str(local_index))
    row36_hist = dict(sorted(Counter(row["stage"] for row in row36_local_records).items()))
    require(row36_hist == fixed_receipt["CLAIM-COVER-RUNG-1"]["reason_histogram"], "ROW36_HISTOGRAM_LINEAGE", repr(row36_hist))

    claim_cover = {
        "claim_id": "K2-TOTAL-FIBRE-ROSTER-OVER-X-V1",
        "target_count": len(per_target),
        "raw_per_target": 48,
        "raw_count": len(raw_roster),
        "evaluated_count": len(raw_roster),
        "rejected_count": len(raw_roster) - len(valid_roster),
        "valid_count": len(valid_roster),
        "reason_histogram": dict(sorted(reason_histogram.items())),
        "no_early_stop": True,
        "all_predicates_materialized_for_every_raw_point": True,
        "complete": len(per_target) == 972 and len(raw_roster) == 972 * 48,
    }
    result = {
        "schema": SCHEMA,
        "artifact_kind": "producer-side candidate; independent checker required",
        "status": "CANDIDATE_PYTHON_PRODUCER",
        "cross_checked": False,
        "verified": False,
        "producer": {
            "path": SOURCE_REL,
            "self_pin": {
                "bytes": (ROOT / SOURCE_REL).stat().st_size,
                "sha256": hashlib.sha256((ROOT / SOURCE_REL).read_bytes()).hexdigest(),
            },
            "lineage": "explicit reuse of authenticated fixed-row36 producer primitives; not independent",
            "reused_source": next(record for record in pins if record["path"] == FIXED_PRODUCER_REL),
        },
        "input_pins": pins,
        "conventions": {
            "roof_order": "X0001..X0972 is zero-based rows 0..971 of the frozen word-key artifact; it is not the unrelated preflight T-order",
            "permutation_product": "GAP right action: i^(left*right)=(i^left)^right",
            "dihedral_coordinates": "r^a s^e with (a,e)(b,f)=(a+(-1)^e b,e+f)",
            "source_pair_m_f": "[m,[m,g36_as_three_[a,e],psl_one_line,c3_exp]]",
            "reduction": "m mod 36 -> m mod 18; G36 -> G9 by a mod 9; PSL unchanged; C3 killed",
            "word_alphabet": "1=x, -1=x^-1, 2=y, -2=y^-1; products read left-to-right",
            "theta": "x->y, y->x",
            "tau": "x->y, y->(xy)^-1",
            "hexagon_h10": "f*theta(f)=1",
            "hexagon_h11": "tau^2(y^m f)*tau(y^m f)*(y^m f)=1",
            "charming": "gcd(2m+1,36)=1 and f in the derived group; PSL is perfect; C3 requires exponent 0",
            "onto_generators": ["x^(2m+1)", "f^-1*y^(2m+1)*f"],
            "onto_component_method": "exact V4-kernel presentation plus maximal-minor/Smith p-valuations in C18^3 x C3; no probabilistic test",
        },
        "word_lift_certificate": {
            "algorithm": "fixed producer right-Cayley G36 transversal plus deterministic Schreier residual BFS in PSL(2,8)xC3",
            "G36_transversal_count": len(trans_words),
            "residual_correction_count": len(corrections),
            "schreier_selected_generator_count": len(schreier_trace),
            "schreier_trace_sha256": digest(schreier_trace),
        },
        "fixed_row36_lineage_control": {
            "target_index_zero_based": 36,
            "raw_count": 48,
            "exact_coordinate_and_word_roster_match": True,
            "first_failure_histogram_match": True,
            "reason_histogram": row36_hist,
            "receipt_positive_count": fixed_receipt["CLAIM-COVER-RUNG-1"]["positive_count"],
        },
        "cache_statistics": {
            "component_exact_order_cases": len(component_cache),
            "psl_exact_closure_cases": len(psl_cache),
            "component_order_histogram": dict(sorted(Counter(component_cache.values()).items())),
            "psl_order_histogram": dict(sorted(Counter(psl_cache.values()).items())),
        },
        "claim_cover": claim_cover,
        "valid_count_histogram": {str(k): v for k, v in sorted(valid_count_histogram.items())},
        "per_target": per_target,
        "raw_roster": raw_roster,
        "valid_roster": valid_roster,
        "coordinate_to_valid_id": lookup,
        "roster_digests": {
            "target_roster_sha256": digest(per_target),
            "raw_roster_sha256": digest(raw_roster),
            "valid_roster_sha256": digest(valid_roster),
            "coordinate_to_valid_id_sha256": digest(lookup),
        },
        "destructive_controls": {
            "selftest_mutants": ["reverse noncommuting word", "drop raw row", "duplicate raw ID", "drop lookup entry", "forge valid-count histogram", "permute per-target raw binding"],
            "full_run_fail_closed": ["all immutable pin mismatches", "target word replay", "48-point fibre cardinality", "source word replay", "fixed row36 lineage", "all-roster coverage/roundtrip"],
        },
        "observed_not_preregistered": {
            "valid_total": len(valid_roster),
            "valid_per_target_histogram": {str(k): v for k, v in sorted(valid_count_histogram.items())},
            "acceptance_did_not_assume_1944_or_two_per_target": True,
        },
        "terminal_marker": FINAL_MARKER,
    }
    validate_result(result)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = canonical_compact(result) + b"\n"
    output_path.write_bytes(payload)
    readback = output_path.read_bytes()
    require(readback == payload, "OUTPUT_READBACK", output_rel)
    print(
        f"D972_K2_TOTAL_FIBRE_RESULT path={output_rel} bytes={len(readback)} "
        f"sha256={hashlib.sha256(readback).hexdigest()} valid={len(valid_roster)} "
        f"histogram={json.dumps(result['valid_count_histogram'], sort_keys=True, separators=(',', ':'))} "
        f"elapsed_seconds={time.monotonic() - started:.6f}",
        flush=True,
    )
    print(FINAL_MARKER, flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true")
    group.add_argument("--execute", action="store_true")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_REL)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    if arguments.selftest:
        selftest()
    else:
        execute(arguments.output)
