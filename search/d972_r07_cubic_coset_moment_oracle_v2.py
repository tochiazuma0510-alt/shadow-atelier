#!/usr/bin/env python3
"""R07 cubic/coset moment oracle v2.

The checked-in production branch is intentionally closed until authenticated
task175 and task176 receipts are registered by the parent.  SELFTEST is a
small, noncommutative D6 implementation of the v134 moment expansion and the
v137 thick coarse-coset oracle.  The checker has a separate implementation;
this file imports no producer, checker, or predecessor API.

The v136 numerical resource claims are historical only.  Resource quantities
in this file are support-parametric toy quantities from v138 and all integer
arithmetic is arbitrary precision.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import mmap
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-cubic-coset-moment-oracle/v2"
SELFTEST_SCHEMA = "d972-r07-cubic-coset-moment-oracle-selftest/v2"
UNKNOWN_INPUT = "UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
R07_COORDINATE_COUNT = 10
FIXTURE = ROOT / "search/certs/d972_r07_cubic_coset_moment_oracle_selftest_v2_20260827.json"

# Updated after the fixture is sealed.  This is an immutable input gate, not
# a replacement for the semantic checks below.
FIXTURE_BYTES = 6486
FIXTURE_SHA256 = "8a7fb3ae2c389b75e98b5a750ab7a2c2c5bc3f00affca8ac57f8ef67ea829aca"

CAPS = {
    "dynamic_resource_ceiling": None,
    "fixed_width_disk_bytes": 3_000_000_000,
    "fixed_width_record_bytes": 256,
    "wall_seconds": 20_000,
    "rss_bytes": 16_000_000_000,
}

# Parent registration is deliberately absent in this version.
REGISTERED_PREREQUISITE_MANIFEST: Path | None = None

PROOF_PINS = {
    "v134": {
        "path": "sol/proof_r07_cubic_character_moment_selector_v134.md",
        "bytes": 9402,
        "sha256": "1cd3bc0ba0291ab07570a423e6473a54d9a2d4941e310f11e7a55fa16b709477",
    },
    "v136_historical_withdrawn": {
        "path": "sol/proof_r07_cubic_moment_exact_resource_cap_v136.md",
        "bytes": 4778,
        "sha256": "2af3b250aefed10933284847d39e204570b1fdf805313632988d1d49cb0e4a86",
    },
    "v137": {
        "path": "sol/proof_r07_coarse_anchor_multi_projection_oracle_v137.md",
        "bytes": 7908,
        "sha256": "8674eda702a099885da50b9c3feb664a72f345fa4574cffc138a7e892a3f3a67",
    },
    "v138_active": {
        "path": "sol/proof_r07_cubic_moment_resource_cap_erratum_v138.md",
        "bytes": 6371,
        "sha256": "9dc94b6de5120e54f3b5a5324fb58a24646ad5917b3bd85c36162af29aa86456",
    },
}

INSTRUCTION_PINS = {
    "task178": {
        "path": "sol/luna_task_178_r07_cubic_coset_moment_oracle_v2.md",
        "bytes": 6640,
        "sha256": "35890e33e18d0a6150f1173ef1e078eac3d8cbfb1a67dc5edf39abf9ae261ddb",
    },
    "task178a": {
        "path": "sol/luna_task_178a_r07_cubic_moment_resource_erratum.md",
        "bytes": 3213,
        "sha256": "ef5062f76d7198a1eaf31c839703513f74bf4f80fd97ec11816422d0b4b5bcee",
    },
}

TASK177_PINS = {
    "producer": {
        "path": "search/d972_r07_weighted_cell_colgen_v1.py",
        "bytes": 29523,
        "sha256": "d955d7717f55ffca3abb92229b96ce2b8ee092ddae3d5e6c7379df92f3892d2e",
    },
    "checker": {
        "path": "crosscheck/check_d972_r07_weighted_cell_colgen_v1.py",
        "bytes": 20157,
        "sha256": "b4d8d046c6850042e0c74778ff8410d9725ef8d0d9387ddb2f75325a6f72d50e",
    },
    "driver": {
        "path": "search/d972_r07_weighted_cell_colgen_gha_driver_v1.g",
        "bytes": 13670,
        "sha256": "cb32e46412622e55b53859d0e2f2684932204dfdff85477244d1619f9df71304",
    },
    "fixture": {
        "path": "search/certs/d972_r07_weighted_cell_colgen_selftest_v1_20260827.json",
        "bytes": 4932,
        "sha256": "d118633552b5d827d62101f063ba9d7d60fd4335f3744169f85f6cbb2b95da8b",
    },
}


class Reject(RuntimeError):
    """A certificate or fixture failed a semantic check."""


class InputStop(RuntimeError):
    """A production prerequisite is not authenticated and registered."""


class ResourceStop(RuntimeError):
    """A future registered dynamic resource ceiling was exceeded."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(canonical(value))


def reduce_word(word: Iterable[int]) -> list[int]:
    result: list[int] = []
    for letter in word:
        require(isinstance(letter, int) and letter in (-2, -1, 1, 2),
                "free word letter")
        if result and result[-1] == -letter:
            result.pop()
        else:
            result.append(letter)
    return result


def inverse_word(word: Iterable[int]) -> list[int]:
    return [-letter for letter in reversed(list(word))]


def concat_word(*words: Iterable[int]) -> list[int]:
    result: list[int] = []
    for word in words:
        result = reduce_word(result + list(word))
    return result


def exponent_sums(word: Iterable[int]) -> list[int]:
    result = [0, 0]
    for letter in word:
        result[0 if abs(letter) == 1 else 1] += 1 if letter > 0 else -1
    return [value % 3 for value in result]


# D6 is stored as r^a s^f.  This multiplication is deliberately ordered and
# therefore witnesses the noncommutativity needed by the fixture.
Pair = tuple[int, int]


def d6_mul(left: Pair, right: Pair) -> Pair:
    r1, f1 = left
    r2, f2 = right
    sign = -1 if f1 else 1
    return ((r1 + sign * r2) % 3, (f1 + f2) % 2)


def d6_inverse(value: Pair) -> Pair:
    for r in range(3):
        for f in range(2):
            candidate = (r, f)
            if d6_mul(value, candidate) == (0, 0) and d6_mul(candidate, value) == (0, 0):
                return candidate
    raise Reject("D6 inverse")


def d6_word(word: Iterable[int]) -> Pair:
    result: Pair = (0, 0)
    generators = {1: (0, 1), 2: (1, 0)}
    for letter in word:
        generator = generators[abs(letter)]
        if letter < 0:
            generator = d6_inverse(generator)
        result = d6_mul(result, generator)
    return result


def pair_text(value: Pair) -> str:
    return f"{value[0]}:{value[1]}"


def parse_pair(value: str) -> Pair:
    pieces = str(value).split(":")
    require(len(pieces) == 2, "D6 pair spelling")
    result = (int(pieces[0]), int(pieces[1]))
    require(result[0] in range(3) and result[1] in range(2), "D6 pair range")
    return result


def gamma_words() -> list[list[int]]:
    return [[], [2], [2, 2]]


def section_words() -> list[list[int]]:
    return [[], [1]]


def phi_text(value: Pair, coordinate: int) -> str:
    require(coordinate in (0, 1), "coordinate")
    if coordinate == 0:
        return pair_text(value)
    return pair_text(((-value[0]) % 3, value[1]))


def expected_delta() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for q0 in range(2):
        for gamma in range(3):
            word = concat_word(gamma_words()[gamma], section_words()[q0])
            value = d6_word(word)
            result.append({
                "id": f"d{gamma}{q0}",
                "gamma": gamma,
                "q0": q0,
                "word": word,
                "value": pair_text(value),
                "coordinates": [phi_text(value, 0), phi_text(value, 1)],
            })
    return result


def query_key(indices: Iterable[int]) -> str:
    return ",".join(str(i) for i in indices)


def query_values(state: dict[str, Any], indices: Iterable[int]) -> tuple[str, ...]:
    return tuple(state["coordinates"][i] for i in indices)


def linked_a(indices: tuple[int, ...]) -> set[tuple[str, ...]]:
    result: set[tuple[str, ...]] = set()
    for word in gamma_words():
        value = d6_word(word)
        result.add(tuple(phi_text(value, i) for i in indices))
    return result


def coarse_groups(model: dict[str, Any] | None = None) -> dict[int, set[Pair]]:
    expected = {0: {d6_word(word) for word in gamma_words()},
                1: {d6_word(word) for word in gamma_words()}}
    if model is None:
        return expected
    # The serialized groups are a candidate map used by the oracle, while
    # `expected` remains a fresh reconstruction used to authenticate it.
    result = {index: {parse_pair(value)
                      for value in model["coarse_groups"][str(index)]}
             for index in (0, 1)}
    require(result == expected, "candidate coarse C_i reconstruction")
    return result


def thick_bucket(target: str, coordinate: int, section: str,
                 groups: dict[int, set[Pair]]) -> bool:
    value = d6_mul(parse_pair(target), d6_inverse(parse_pair(section)))
    return value in groups[coordinate]


def literal_bucket(target: str, section: str) -> bool:
    return target == section


def canonical_coset_key(coordinate: int, value: str,
                        groups: dict[int, set[Pair]]) -> tuple[str, ...]:
    require(coordinate in groups, "coset coordinate")
    representative = parse_pair(value)
    return tuple(sorted(pair_text(d6_mul(element, representative))
                        for element in groups[coordinate]))


def oracle_count(indices: tuple[int, ...], target: tuple[str, ...],
                 model: dict[str, Any], states: list[dict[str, Any]]) -> int:
    groups = coarse_groups(model)
    gamma_image = linked_a(indices)
    reported_image = {tuple(str(value) for value in row)
                      for row in query_index(model["queries"])[query_key(indices)]["A"]}
    require(reported_image == gamma_image, "candidate linked A_S reconstruction")
    direct_values = {query_values(state, indices) for state in states}
    kernel_order = len(states) // len(direct_values)
    reported_kernel = int(query_index(model["queries"])[query_key(indices)]["kernel_order"])
    require(reported_kernel == kernel_order, "candidate kernel order")
    total = 0
    for q0, word in enumerate(section_words()):
        section_value = d6_word(word)
        sections = [phi_text(section_value, i) for i in indices]
        if not all(thick_bucket(target[pos], coordinate, sections[pos], groups)
                   for pos, coordinate in enumerate(indices)):
            continue
        residual = tuple(pair_text(d6_mul(parse_pair(target[pos]),
                                          d6_inverse(parse_pair(sections[pos]))))
                         for pos in range(len(indices)))
        if residual in gamma_image:
            total += reported_kernel
    return total


def calculate_query(states: list[dict[str, Any]], indices: tuple[int, ...],
                    model: dict[str, Any]) -> dict[str, Any]:
    a_values = sorted(linked_a(indices))
    d_values = sorted({query_values(row, indices) for row in states})
    l_order = 0
    for q0, word in enumerate(section_words()):
        section = d6_word(word)
        section_tuple = tuple(phi_text(section, i) for i in indices)
        if section_tuple in linked_a(indices):
            l_order += 1
    kernel_order = len(states) // len(d_values)
    return {
        "indices": list(indices),
        "key": query_key(indices),
        "A": [list(value) for value in a_values],
        "L_order": l_order,
        "D_order": len(d_values),
        "kernel_order": kernel_order,
        "n_values": [{"a": list(value),
                      "count": oracle_count(indices, value, model, states)}
                     for value in d_values],
    }


def query_index(queries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for query in queries:
        key = str(query["key"])
        require(key not in result, "duplicate query")
        result[key] = query
    return result


def raw_occurrence_merge(row: dict[str, Any], coordinate_count: int = 2) -> list[dict[str, Any]]:
    merged: dict[tuple[int, str], int] = {}
    for occurrence in row["raw_occurrences"]:
        coordinate = int(occurrence["coordinate"])
        weight = int(occurrence["weight"]) % 3
        target = str(occurrence["target"])
        require(coordinate in range(coordinate_count) and weight in (0, 1, 2),
                "raw occurrence range")
        parse_pair(target)
        key = (coordinate, target)
        merged[key] = (merged.get(key, 0) + weight) % 3
    return [{"coordinate": coordinate, "target": target,
             "coefficient": coefficient}
            for (coordinate, target), coefficient in sorted(merged.items())
            if coefficient]


def support_sizes(model: dict[str, Any]) -> dict[str, int]:
    result: dict[str, int] = {}
    for block, data in model["dual_support"].items():
        points = data["points"]
        seen: set[str] = set()
        count = 0
        for point in points:
            spelling = str(point["g"])
            parse_pair(spelling)
            require(spelling not in seen, "duplicate dual support point")
            seen.add(spelling)
            if int(point["coefficient"]) % 3 != 0:
                count += 1
        result[block] = count
    return result


def resource_values(row: dict[str, Any], model: dict[str, Any]) -> dict[str, Any]:
    support = support_sizes(model)
    weighted_m = sum(support[str(item["block"])]
                     for item in row["raw_occurrences"])
    arity = int(model.get("coordinate_count", 2))
    require(arity > 0, "resource coordinate arity")
    merged = raw_occurrence_merge(row, arity)
    sizes = [len({item["target"] for item in merged
                  if int(item["coordinate"]) == coordinate})
             for coordinate in range(arity)]
    actual_terms = 1
    for size in sizes:
        actual_terms *= 1 + size
    arity = len(sizes)
    q, remainder = divmod(weighted_m, arity)
    balanced_toy = (q + 2) ** remainder * (q + 1) ** (arity - remainder)
    q10, remainder10 = divmod(weighted_m, 10)
    balanced = (q10 + 2) ** remainder10 * (q10 + 1) ** (10 - remainder10)
    # v138 (4.2) is conditional and uses arbitrary precision here.  This is
    # a diagnostic toy bound, never a signed-64 production assertion.
    diagnostic_norm_bound = 2 * (3 ** arity) * len(model["delta_states"]) * actual_terms
    return {
        "support_weighted_M": weighted_m,
        "fox_occurrence_count": len(row["raw_occurrences"]),
        "merged_sizes": sizes,
        "actual_term_count": actual_terms,
        "balanced_cap_from_M": balanced,
        "balanced_cap_toy_arity": balanced_toy,
        "diagnostic_norm_bound": diagnostic_norm_bound,
        "diagnostic_signed64_fit": diagnostic_norm_bound < 2 ** 63,
        "support_multiplicities": support,
    }


def e_add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (left[0] + right[0], left[1] + right[1])


def e_scale(value: tuple[int, int], scalar: int) -> tuple[int, int]:
    return (scalar * value[0], scalar * value[1])


def e_mul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    a, b = left
    c, d = right
    return (a * c - b * d, a * d + b * c - b * d)


def omega_power(exponent: int) -> tuple[int, int]:
    return ((1, 0), (0, 1), (-1, -1))[exponent % 3]


def factor_pair(coefficient: int, constants: dict[str, Any]) -> tuple[int, int]:
    key = str(coefficient % 3)
    require(key in constants["omega_minus_one"], "missing omega factor")
    return tuple(int(x) for x in constants["omega_minus_one"][key])  # type: ignore[return-value]


def n_value_from_oracle(queries: dict[str, dict[str, Any]],
                        indices: tuple[int, ...], target: tuple[str, ...],
                        model: dict[str, Any], states: list[dict[str, Any]]) -> int:
    # The query table is an authenticated transcript, but the count is
    # rebuilt by the same thick-coset oracle instead of being trusted.
    calculated = oracle_count(indices, target, model, states)
    query = queries[query_key(indices)]
    for row in query["n_values"]:
        if tuple(row["a"]) == target:
            require(int(row["count"]) == calculated, "partial fibre transcript")
            return calculated
    require(calculated == 0, "missing partial fibre target")
    return 0


def moment_expansion(row: dict[str, Any], model: dict[str, Any],
                     states: list[dict[str, Any]],
                     queries: dict[str, dict[str, Any]]) -> tuple[tuple[int, int], list[dict[str, Any]]]:
    merged = raw_occurrence_merge(row)
    targets = [[item["target"] for item in merged
                if int(item["coordinate"]) == coordinate]
               for coordinate in range(2)]
    support = [coordinate for coordinate in range(2) if targets[coordinate]]
    constants = model["eisenstein_constants"]
    kappa = int(row["kappa"]) % 3
    result = (0, 0)
    terms: list[dict[str, Any]] = []
    # Empty subset and all nonempty partial tuples implement v134 (3.3).
    for mask in range(1 << len(support)):
        subset = [support[position] for position in range(len(support))
                  if mask & (1 << position)]
        choices = [targets[coordinate] for coordinate in subset]
        assignments: list[tuple[str, ...]] = [()]
        for values in choices:
            assignments = [prefix + (value,) for prefix in assignments
                           for value in values]
        if not subset:
            assignments = [()]
        for assignment in assignments:
            indices = tuple(subset)
            count = len(states) if not indices else n_value_from_oracle(
                queries, indices, assignment, model, states)
            product = (1, 0)
            for coordinate in subset:
                item = next(item for item in merged
                            if int(item["coordinate"]) == coordinate and
                            item["target"] == assignment[subset.index(coordinate)])
                product = e_mul(product, factor_pair(int(item["coefficient"]), constants))
            total_factor = e_mul(omega_power(kappa), product)
            term = e_scale(total_factor, count)
            result = e_add(result, term)
            terms.append({"subset": list(subset), "targets": list(assignment),
                          "count": count, "factor": list(total_factor),
                          "term": list(term)})
    return result, terms


def direct_moment(row: dict[str, Any], states: list[dict[str, Any]]) -> tuple[tuple[int, int], list[int]]:
    merged = raw_occurrence_merge(row)
    counts = [0, 0, 0]
    for state in states:
        value = int(row["kappa"]) % 3
        for item in merged:
            if state["coordinates"][int(item["coordinate"])] == item["target"]:
                value += int(item["coefficient"])
        counts[value % 3] += 1
    result = (0, 0)
    for value, count in enumerate(counts):
        result = e_add(result, e_scale(omega_power(value), count))
    return result, counts


def recover_counts(moment: tuple[int, int], total: int) -> list[int]:
    a, b = moment
    numerator = total - a - b
    require(numerator % 3 == 0, "nonintegral n2")
    n2 = numerator // 3
    result = [a + n2, b + n2, n2]
    require(all(value >= 0 for value in result), "negative recovered count")
    require(sum(result) == total, "recovered count total")
    return result


def record_map(rows: list[dict[str, Any]], key: str) -> dict[Any, dict[str, Any]]:
    result: dict[Any, dict[str, Any]] = {}
    for row in rows:
        require(row[key] not in result, f"duplicate {key}")
        result[row[key]] = row
    return result


def validate_anchor(model: dict[str, Any], states: list[dict[str, Any]]) -> None:
    groups = coarse_groups(model)
    anchor = model["anchor"]
    coordinate = int(anchor["coordinate"])
    target = str(anchor["target"])
    q = int(anchor["section_q"])
    section = phi_text(d6_word(section_words()[q]), coordinate)
    expected_thick = [q0 for q0, word in enumerate(section_words())
                      if thick_bucket(target, coordinate,
                                      phi_text(d6_word(word), coordinate), groups)]
    expected_literal = [q0 for q0, word in enumerate(section_words())
                        if literal_bucket(target,
                                         phi_text(d6_word(word), coordinate))]
    if anchor["bucket_mode"] == "THICK_CI_COSET":
        observed_bucket = expected_thick
    elif anchor["bucket_mode"] == "LITERAL_EQUALITY":
        observed_bucket = expected_literal
    else:
        raise Reject("anchor bucket mode")
    require(anchor["thick_bucket"] == observed_bucket, "anchor bucket execution")
    require(anchor["bucket_mode"] == "THICK_CI_COSET", "anchor bucket mode")
    if anchor["residual_side"] == "TARGET_TIMES_SECTION_INVERSE":
        residual_value = d6_mul(parse_pair(target), d6_inverse(parse_pair(section)))
    elif anchor["residual_side"] == "SECTION_INVERSE_TIMES_TARGET":
        residual_value = d6_mul(d6_inverse(parse_pair(section)), parse_pair(target))
    else:
        raise Reject("anchor residual side")
    require(anchor["residual_side"] == "TARGET_TIMES_SECTION_INVERSE",
            "anchor residual side")
    require(anchor["section_value"] == section, "anchor section value")
    require(anchor["coset_key"] == list(canonical_coset_key(coordinate, target, groups)),
            "anchor canonical left coset")
    require(anchor["thick_bucket"] == expected_thick, "anchor thick bucket")
    require(anchor["literal_bucket"] == expected_literal, "anchor literal bucket")
    require(anchor["selected_q"] == q and q in expected_thick,
            "anchor selected q")
    require(target != section and not expected_literal,
            "anchor literal distinction")
    residual = pair_text(residual_value)
    require(anchor["residual"] == residual, "anchor residual")
    require(anchor["literal_misses"] is True, "literal miss marker")


def validate_resource_row(row: dict[str, Any], model: dict[str, Any],
                         states: list[dict[str, Any]]) -> None:
    cancelled = [item for item in row["raw_occurrences"]
                  if str(item["target"]) == "1:1"]
    require(cancelled and sum(int(item["weight"]) for item in cancelled) % 3 == 0,
            "explicit same-target cancellation")
    merged = raw_occurrence_merge(row)
    require(row["merged"] == merged, "same-target merge and cancellation")
    resource = resource_values(row, model)
    for key in ("support_weighted_M", "merged_sizes", "actual_term_count",
                "fox_occurrence_count", "balanced_cap_from_M",
                "balanced_cap_toy_arity",
                "support_multiplicities"):
        require(row["resource"][key] == resource[key], f"resource {key}")
    require(row["resource"]["diagnostic_norm_bound"] == resource["diagnostic_norm_bound"],
            "toy diagnostic bound")
    require(resource["actual_term_count"] <= resource["balanced_cap_from_M"],
            "v138 balanced toy bound")
    require(len(row["partial_terms"]) == resource["actual_term_count"],
            "exact toy partial term count")
    require(row["resource"]["diagnostic_signed64_fit"] ==
            resource["diagnostic_signed64_fit"], "toy diagnostic fit")
    queries = query_index(model["queries"])
    moment, terms = moment_expansion(row, model, states, queries)
    direct, distribution = direct_moment(row, states)
    require(moment == direct, "partial/direct exact moment")
    require(row["partial_terms"] == terms, "partial term transcript")
    require(tuple(row["moment"]) == moment, "stored exact moment")
    require(row["distribution"] == distribution, "direct distribution")
    require(row["recovered_n"] == recover_counts(moment, len(states)),
            "recovered n_j")
    if row["id"] == "zero":
        require(moment == (len(states), 0), "negative zero control")
        require(row["recovered_n"] == [len(states), 0, 0], "zero control counts")
    else:
        require(moment != (0, 0) and sum(row["distribution"][1:]) > 0,
                "positive ACTIVE row")


def validate_model(model: dict[str, Any]) -> None:
    require(model["coordinate_count"] == 2, "toy coordinate arity")
    states = model["delta_states"]
    require(states == expected_delta(), "D6 section reconstruction")
    require(d6_word([1, 2]) != d6_word([2, 1]), "noncommutative D6 witness")
    require(model["noncommutative"]["linked_extension"] is True,
            "linked extension marker")
    require(model["noncommutative"]["order"] == 6, "D6 order")
    require(model["coarse_groups"] == {
        "0": sorted(pair_text(value) for value in coarse_groups()[0]),
        "1": sorted(pair_text(value) for value in coarse_groups()[1]),
    }, "nontrivial coarse C_i")
    require(model["gamma_coarse_order"] == len(coarse_groups()[0]) == 3,
            "gamma coarse order")
    require(model["linked_graph_order"] == len(linked_a((0, 1))) == 3,
            "linked graph order")

    queries = query_index(model["queries"])
    for indices in ((0,), (1,), (0, 1)):
        expected = calculate_query(states, indices, model)
        actual = queries[query_key(indices)]
        for key in ("indices", "A", "L_order", "D_order", "kernel_order", "n_values"):
            require(actual[key] == expected[key], f"query {query_key(indices)} {key}")
    require(queries["0,1"]["A"] == [["0:0", "0:0"],
                                     ["1:0", "2:0"],
                                     ["2:0", "1:0"]],
            "linked Gamma graph orientation")
    require(queries["0,1"]["kernel_order"] == 1, "linked kernel order")

    validate_anchor(model, states)
    witness = model["active_witness"]
    state = record_map(states, "id")[witness["delta_id"]]
    source = concat_word(gamma_words()[int(witness["gamma_state"])],
                         section_words()[int(witness["section_q"])])
    require(witness["gamma_state_coord0"] == witness["gamma_state_coord1"],
            "same Gamma state in linked coordinates")
    require(int(witness["gamma_state"]) == 1, "active Gamma state")
    gamma0_word = concat_word(gamma_words()[int(witness["gamma_state_coord0"])],
                              section_words()[int(witness["section_q"])])
    gamma1_word = concat_word(gamma_words()[int(witness["gamma_state_coord1"])],
                              section_words()[int(witness["section_q"])])
    require(phi_text(d6_word(gamma0_word), 0) == witness["target"][0],
            "coordinate zero Gamma replay")
    require(phi_text(d6_word(gamma1_word), 1) == witness["target"][1],
            "coordinate one Gamma replay")
    require(witness["source_word"] == source, "Gamma-section source concatenation")
    require(state["word"] == source, "source state replay")
    require(state["coordinates"] == witness["target"], "two-coordinate replay")
    require(tuple(witness["residual"]) == ("1:0", "2:0"), "witness residual")
    require(witness["fiber_order"] == queries["0,1"]["kernel_order"],
            "witness fibre order")
    require(witness["membership"] is True, "linked target membership")
    require(oracle_count((0, 1), tuple(witness["target"]), model, states) ==
            witness["fiber_order"], "witness oracle membership")
    require(exponent_sums(witness["source_word"]) == [1, 1],
            "fixture source exponent replay")

    require(model["eisenstein_constants"]["omega_minus_one"] == {
        "0": [0, 0], "1": [-1, 1], "2": [-2, -1]},
        "exact omega constants")
    require(model["resource_policy"] == "SUPPORT_PARAMETRIC_TOY_ONLY",
            "v138 resource policy")
    require(model["resource_policy_production"] == "DYNAMIC_REGISTERED_CEILING",
            "production resource policy")
    require(model["production_cap"] == "DYNAMIC_REGISTERED_CEILING",
            "production cap is not a withdrawn constant")
    require(model["withdrawn_v136_claims"] == [
        "UNCONDITIONAL_PER_ROW_CAP_1536",
        "UNCONDITIONAL_ALL_ROW_CAP_9893376",
        "UNCONDITIONAL_SIGNED64_SAFETY",
    ], "withdrawn v136 record")
    for row in model["weighted_rows"]:
        validate_resource_row(row, model, states)


MUTATIONS = [
    "same_target_merge_cancellation",
    "coarse_identity_replacement",
    "literal_equality_bucket",
    "residual_side_order",
    "wrong_anchor_bucket_state",
    "different_gamma_states",
    "graph_orientation",
    "kernel_order",
    "partial_membership_bit",
    "omega_minus_one_pair",
    "eisenstein_multiplication_coordinate",
    "constant_K",
    "recovered_nj",
    "word_section_gamma_concat",
    "block_support_multiplicity",
    "fox_occurrence_M",
    "withdrawn_v136_cap",
]


def mutate(model: dict[str, Any], name: str) -> dict[str, Any]:
    result = copy.deepcopy(model)
    if name == "same_target_merge_cancellation":
        result["weighted_rows"][0]["raw_occurrences"][1]["weight"] = 1
    elif name == "coarse_identity_replacement":
        result["coarse_groups"]["0"] = ["0:0"]
    elif name == "literal_equality_bucket":
        result["anchor"]["bucket_mode"] = "LITERAL_EQUALITY"
    elif name == "residual_side_order":
        result["anchor"]["residual_side"] = "SECTION_INVERSE_TIMES_TARGET"
    elif name == "wrong_anchor_bucket_state":
        result["anchor"]["selected_q"] = 0
        result["anchor"]["thick_bucket"] = [0]
    elif name == "different_gamma_states":
        result["active_witness"]["gamma_state_coord1"] = 2
    elif name == "graph_orientation":
        result["queries"][2]["A"][1] = ["1:0", "1:0"]
    elif name == "kernel_order":
        result["queries"][2]["kernel_order"] = 2
    elif name == "partial_membership_bit":
        for entry in result["queries"][2]["n_values"]:
            if entry["a"] == ["1:1", "2:1"]:
                entry["count"] = 0
                break
    elif name == "omega_minus_one_pair":
        result["eisenstein_constants"]["omega_minus_one"]["1"] = [1, 1]
    elif name == "eisenstein_multiplication_coordinate":
        result["weighted_rows"][0]["partial_terms"][1]["term"][0] += 1
    elif name == "constant_K":
        result["weighted_rows"][0]["kappa"] = 0
    elif name == "recovered_nj":
        result["weighted_rows"][0]["recovered_n"][0] += 1
    elif name == "word_section_gamma_concat":
        result["active_witness"]["source_word"] = [1, 2]
    elif name == "block_support_multiplicity":
        result["dual_support"]["H1"]["points"][1]["coefficient"] = 0
    elif name == "fox_occurrence_M":
        result["weighted_rows"][0]["resource"]["support_weighted_M"] = \
            len(result["weighted_rows"][0]["raw_occurrences"])
    elif name == "withdrawn_v136_cap":
        result["production_cap"] = 1536
    else:
        raise Reject(f"unknown mutation {name}")
    return result


def run_mutations(model: dict[str, Any]) -> tuple[int, int]:
    rejected = 0
    for name in MUTATIONS:
        try:
            validate_model(mutate(model, name))
        except (Reject, KeyError, TypeError, ValueError, IndexError):
            rejected += 1
    return len(MUTATIONS), rejected


def fixture_identity(path: Path) -> None:
    raw = path.read_bytes()
    if FIXTURE_BYTES and FIXTURE_SHA256:
        require((len(raw), sha_bytes(raw)) == (FIXTURE_BYTES, FIXTURE_SHA256),
                "immutable cubic fixture")


def load_fixture(path: Path) -> dict[str, Any]:
    fixture_identity(path)
    value = json.loads(path.read_text(encoding="ascii"))
    require(value["schema"] == SELFTEST_SCHEMA and
            value["status"] == "SELFTEST" and
            value["terminal"] == "FIXTURE_PASS", "fixture envelope")
    require(value["model"]["noncommutative"]["order"] == 6,
            "fixture D6 order")
    return value


def selftest(path: Path) -> int:
    fixture = load_fixture(path)
    model = fixture["model"]
    validate_model(model)
    attempted, rejected = run_mutations(model)
    require(attempted == 17 and rejected == 17, "semantic mutation suite")
    print("R07_CUBIC_COSET_MOMENT_ORACLE_V2_PRODUCER_SELFTEST_PASS "
          f"mutations={attempted} rejected={rejected} "
          f"gamma_coarse_order={len(coarse_groups()[0])} "
          f"linked_graph_order={len(linked_a((0, 1)))}", flush=True)
    return 0


def stream_fixed_width_index(rows: Iterable[bytes], width: int) -> dict[str, Any]:
    """Future production primitive; its file is outside the repository."""
    require(width > 0, "fixed-width record width")
    total = 0
    digest = hashlib.sha256()
    temporary: Path | None = None
    with tempfile.NamedTemporaryFile(prefix="r07_cubic_coset_", suffix=".bin",
                                     dir=tempfile.gettempdir(), delete=False) as handle:
        temporary = Path(handle.name)
        for row in rows:
            require(len(row) == width, "fixed-width record length")
            handle.write(row)
            digest.update(row)
            total += len(row)
            if total > int(CAPS["fixed_width_disk_bytes"]):
                raise ResourceStop("fixed_width_disk_bytes")
    if total:
        with temporary.open("rb") as handle:  # type: ignore[union-attr]
            mapped = mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ)
            mapped.close()
    return {"path": str(temporary), "bytes": total,
            "sha256": digest.hexdigest(), "record_width": width}


def typed_cache_key(subset: Iterable[int], target: Iterable[str]) -> bytes:
    """Canonical typed key for future partial-fibre memoization."""
    return canonical({"subset": list(subset), "target": list(target)})


def v138_conditional_norm_bound(total_states: int, actual_terms: int) -> int:
    """Conditional ten-coordinate bound; never an unconditional cap."""
    return 2 * (3 ** R07_COORDINATE_COUNT) * total_states * actual_terms


def canonical_ci_coset_key(coordinate: int, value: str,
                           groups: dict[int, set[Pair]]) -> bytes:
    """Canonical key for (coordinate, C_i-coset), independent of row order."""
    require(coordinate in groups, "coset coordinate")
    representative = parse_pair(value)
    members = sorted(pair_text(d6_mul(c, representative))
                     for c in groups[coordinate])
    return canonical({"coordinate": coordinate, "coset": members})


def fixed_width_index_record(coordinate: int, value: str,
                             q0_state_ids: Iterable[int], width: int = 256) -> bytes:
    """Serialize one future index row; callers must write it outside the repo."""
    key = canonical_ci_coset_key(coordinate, value, coarse_groups())
    payload = canonical({"key": key.decode("ascii"),
                         "q0_state_ids": sorted(int(x) for x in q0_state_ids)})
    require(len(payload) <= width, "fixed-width index payload")
    return payload + b" " * (width - len(payload))


def load_pinned_json(path: Path, expected_bytes: int,
                     expected_sha256: str) -> dict[str, Any]:
    raw = path.read_bytes()
    require(len(raw) == expected_bytes and sha_bytes(raw) == expected_sha256,
            f"prerequisite pin {path}")
    value = json.loads(raw.decode("ascii"))
    require(isinstance(value, dict), "pinned receipt object")
    return value


def prerequisite_manifest_shape(manifest: dict[str, Any]) -> None:
    for label, terminal in (("task175", "R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_READY"),
                            ("task176", "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS")):
        row = manifest.get(label)
        require(isinstance(row, dict), f"missing {label} prerequisite")
        require(isinstance(row.get("run_id"), int) and row["run_id"] > 0,
                f"{label} run id")
        require(isinstance(row.get("head_sha"), str) and len(row["head_sha"]) == 40,
                f"{label} head sha")
        require(isinstance(row.get("receipt_path"), str), f"{label} receipt path")
        require(isinstance(row.get("receipt_bytes"), int) and row["receipt_bytes"] > 0,
                f"{label} receipt bytes")
        require(isinstance(row.get("receipt_sha256"), str) and
                len(row["receipt_sha256"]) == 64, f"{label} receipt hash")
        require(isinstance(row.get("checker_verdict_path"), str),
                f"{label} checker verdict path")
        require(isinstance(row.get("checker_verdict_sha256"), str) and
                len(row["checker_verdict_sha256"]) == 64,
                f"{label} checker verdict hash")
        require(row.get("terminal") == terminal, f"{label} terminal")


def ingest_prerequisites(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="ascii"))
    prerequisite_manifest_shape(manifest)
    result: dict[str, Any] = {"manifest": manifest, "receipts": {}}
    for label in ("task175", "task176"):
        row = manifest[label]
        receipt = load_pinned_json(Path(row["receipt_path"]),
                                   int(row["receipt_bytes"]),
                                   str(row["receipt_sha256"]))
        require(receipt.get("terminal") == row["terminal"],
                f"{label} receipt terminal")
        result["receipts"][label] = receipt
    return result


def authenticate_prerequisites(path: Path | None) -> dict[str, Any]:
    if REGISTERED_PREREQUISITE_MANIFEST is None:
        raise InputStop("PREREQUISITE_NOT_PINNED")
    require(path is not None and path == REGISTERED_PREREQUISITE_MANIFEST,
            "PREREQUISITE_NOT_PINNED")
    return ingest_prerequisites(path)


def future_capped_expansion(actual_terms: int, ceiling: int | None) -> None:
    if ceiling is not None and actual_terms > ceiling:
        raise ResourceStop("dynamic_resource_ceiling")


def future_measure_before_expansion(rows: Iterable[dict[str, Any]],
                                    model: dict[str, Any],
                                    ceiling: int | None) -> list[dict[str, Any]]:
    """Future production gate: measure every row before any term expansion."""
    measurements: list[dict[str, Any]] = []
    for row in rows:
        measured = resource_values(row, model)
        future_capped_expansion(int(measured["actual_term_count"]), ceiling)
        measurements.append(measured)
    return measurements


def production_receipt() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "UNKNOWN_INPUT",
        "terminal": UNKNOWN_INPUT,
        "reason": "PREREQUISITE_NOT_PINNED",
        "result": None,
        "pins": {
            "task175": None,
            "task176": None,
            "proofs": PROOF_PINS,
            "instructions": INSTRUCTION_PINS,
            "task177": TASK177_PINS,
        },
        "resource_theorem": "v138_SUPPORT_PARAMETRIC_CAP",
        "withdrawn_resource_claims": [
            "v136_per_row_1536",
            "v136_all_rows_9893376",
            "v136_unconditional_signed64",
        ],
        "integer_arithmetic": "ARBITRARY_PRECISION_REQUIRED",
        "resource_contract": {
            "measure_before_expansion": True,
            "actual_coordinate_count": R07_COORDINATE_COUNT,
            "conditional_norm_formula": "2*3^10*N*P_actual",
            "support_weighted_M": "RECONSTRUCT_PER_ROW",
            "merged_sizes": "RECONSTRUCT_PER_ROW",
            "actual_product": "RECONSTRUCT_PER_ROW",
            "registered_dynamic_ceiling": CAPS["dynamic_resource_ceiling"],
            "cap_exhaustion": UNKNOWN_RESOURCE,
            "zero_correlation_on_cap": False,
        },
        "streaming": {
            "fixed_width_mmap_outside_repository": True,
            "index_key": "(coordinate,canonical_C_i_coset_key)",
            "cache_key": "(ordered_subset,complete_target_tuple)",
            "large_table_allocated": False,
        },
        "phases": {
            "prerequisite_gate": "NOT_PINNED",
            "dual_support_reconstruction": "NOT_RUN",
            "weighted_moment_rows": "NOT_RUN",
            "coarse_coset_oracle": "NOT_RUN",
            "common_word_replay": "NOT_RUN",
        },
        "boundaries": {
            "all_seven_solution": False,
            "correction_word": False,
            "separator": False,
            "cofinal_lift": False,
            "fake": False,
            "Ihara_witness": False,
        },
        "unknowns": [
            "task175 positive run pins",
            "task176 positive run pins",
            "actual R07 dual-support distribution",
        ],
        "self_digest_sha256": None,
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    unsigned = dict(value)
    unsigned.pop("self_digest_sha256", None)
    sealed = dict(unsigned)
    sealed["self_digest_sha256"] = sha_obj(unsigned)
    path.write_bytes(canonical(sealed) + b"\n")


def production(args: argparse.Namespace) -> int:
    receipt = production_receipt()
    try:
        _ = authenticate_prerequisites(Path(args.prerequisites)
                                       if args.prerequisites else None)
        raise InputStop("PREREQUISITE_NOT_PINNED")
    except InputStop:
        pass
    write_json(Path(args.output), receipt)
    print(f"R07_CUBIC_COSET_MOMENT_ORACLE_V2_PRODUCER_TERMINAL {receipt['terminal']}",
          flush=True)
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    modes = result.add_mutually_exclusive_group(required=True)
    modes.add_argument("--selftest", action="store_true")
    modes.add_argument("--run-oracle", action="store_true")
    result.add_argument("--fixture", default=str(FIXTURE))
    result.add_argument("--output")
    result.add_argument("--prerequisites")
    return result


def main() -> int:
    args = parser().parse_args()
    if args.selftest:
        return selftest(Path(args.fixture))
    if not args.output:
        raise SystemExit("--output is required for production")
    return production(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, InputStop, ResourceStop, OSError, ValueError, KeyError,
            TypeError, json.JSONDecodeError) as exc:
        print(f"R07_CUBIC_COSET_MOMENT_ORACLE_V2_PRODUCER_STOP {exc}",
              file=sys.stderr, flush=True)
        raise SystemExit(1)
