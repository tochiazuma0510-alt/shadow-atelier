#!/usr/bin/env python3
"""Independent checker for the R07 cubic/coset moment oracle fixture.

This checker intentionally uses permutations of three points for D6.  It
does not import the producer, task177, or any predecessor implementation;
all group, coset, fibre, word, and Eisenstein operations are reconstructed
locally from the serialized fixture and the pinned paper conventions.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-cubic-coset-moment-oracle/v2"
CHECKER_SCHEMA = "d972-r07-cubic-coset-moment-oracle/v2/checker-v2"
SELFTEST_SCHEMA = "d972-r07-cubic-coset-moment-oracle-selftest/v2"
UNKNOWN_INPUT = "UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED"
FIXTURE = ROOT / "search/certs/d972_r07_cubic_coset_moment_oracle_selftest_v2_20260827.json"
FIXTURE_BYTES = 6486
FIXTURE_SHA256 = "8a7fb3ae2c389b75e98b5a750ab7a2c2c5bc3f00affca8ac57f8ef67ea829aca"


class Reject(RuntimeError):
    pass


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
                "checker free word letter")
        if result and result[-1] == -letter:
            result.pop()
        else:
            result.append(letter)
    return result


def concat_word(*words: Iterable[int]) -> list[int]:
    result: list[int] = []
    for word in words:
        result = reduce_word(result + list(word))
    return result


def inverse_word(word: Iterable[int]) -> list[int]:
    return [-x for x in reversed(list(word))]


Perm = tuple[int, int, int]
IDENTITY: Perm = (0, 1, 2)
ROTATION: Perm = (1, 2, 0)
REFLECTION: Perm = (0, 2, 1)


def perm_mul(left: Perm, right: Perm) -> Perm:
    """Composition left after right, unlike the producer's pair storage."""
    return tuple(left[right[index]] for index in range(3))  # type: ignore[return-value]


def perm_inverse(value: Perm) -> Perm:
    result = [0, 0, 0]
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)  # type: ignore[return-value]


def pair_perm(text: str) -> Perm:
    pieces = str(text).split(":")
    require(len(pieces) == 2, "checker pair spelling")
    r, f = int(pieces[0]), int(pieces[1])
    require(r in range(3) and f in range(2), "checker pair range")
    rotation = IDENTITY
    for _ in range(r):
        rotation = perm_mul(rotation, ROTATION)
    return perm_mul(rotation, REFLECTION) if f else rotation


PAIR_TEXT = {
    IDENTITY: "0:0",
    ROTATION: "1:0",
    perm_mul(ROTATION, ROTATION): "2:0",
    REFLECTION: "0:1",
    perm_mul(ROTATION, REFLECTION): "1:1",
    perm_mul(perm_mul(ROTATION, ROTATION), REFLECTION): "2:1",
}


def perm_text(value: Perm) -> str:
    require(value in PAIR_TEXT, "checker D6 permutation")
    return PAIR_TEXT[value]


def word_perm(word: Iterable[int]) -> Perm:
    result = IDENTITY
    generators = {1: REFLECTION, 2: ROTATION}
    for letter in word:
        generator = generators[abs(letter)]
        if letter < 0:
            generator = perm_inverse(generator)
        result = perm_mul(result, generator)
    return result


def alpha_text(text: str) -> str:
    pieces = str(text).split(":")
    require(len(pieces) == 2, "checker alpha spelling")
    return f"{(-int(pieces[0])) % 3}:{int(pieces[1])}"


def gamma_words() -> list[list[int]]:
    return [[], [2], [2, 2]]


def section_words() -> list[list[int]]:
    return [[], [1]]


def expected_delta() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for q0 in range(2):
        for gamma in range(3):
            word = concat_word(gamma_words()[gamma], section_words()[q0])
            value = perm_text(word_perm(word))
            result.append({
                "id": f"d{gamma}{q0}", "gamma": gamma, "q0": q0,
                "word": word, "value": value,
                "coordinates": [value, alpha_text(value)],
            })
    return result


def linked_a(indices: tuple[int, ...]) -> set[tuple[str, ...]]:
    result: set[tuple[str, ...]] = set()
    for word in gamma_words():
        value = perm_text(word_perm(word))
        coordinates = [value, alpha_text(value)]
        result.add(tuple(coordinates[i] for i in indices))
    return result


def coarse_groups(model: dict[str, Any] | None = None) -> dict[int, set[Perm]]:
    expected = {0: {word_perm(word) for word in gamma_words()},
                1: {word_perm(word) for word in gamma_words()}}
    if model is None:
        return expected
    result = {index: {pair_perm(value)
                      for value in model["coarse_groups"][str(index)]}
              for index in (0, 1)}
    require(result == expected, "checker candidate coarse C_i")
    return result


def thick_bucket(target: str, coordinate: int, section: str,
                 groups: dict[int, set[Perm]] | None = None) -> bool:
    if groups is None:
        groups = coarse_groups()
    return (perm_mul(pair_perm(target), perm_inverse(pair_perm(section))) in
            groups[coordinate])


def canonical_coset_key(coordinate: int, value: str) -> tuple[str, ...]:
    """Canonical left C_i-coset, independently sorted from permutations."""
    groups = coarse_groups()
    return tuple(sorted(perm_text(perm_mul(element, pair_perm(value)))
                        for element in groups[coordinate]))


def query_values(state: dict[str, Any], indices: Iterable[int]) -> tuple[str, ...]:
    return tuple(state["coordinates"][index] for index in indices)


def query_key(indices: Iterable[int]) -> str:
    return ",".join(str(index) for index in indices)


def oracle_count(indices: tuple[int, ...], target: tuple[str, ...],
                 states: list[dict[str, Any]],
                 model: dict[str, Any] | None = None) -> int:
    image = linked_a(indices)
    groups = coarse_groups(model)
    if model is not None:
        reported = {tuple(str(value) for value in row)
                    for row in query_index(model["queries"])[query_key(indices)]["A"]}
        require(reported == image, "checker candidate linked A_S")
    direct_values = {query_values(state, indices) for state in states}
    kernel = len(states) // len(direct_values)
    if model is not None:
        reported_kernel = int(query_index(model["queries"])[query_key(indices)]["kernel_order"])
        require(reported_kernel == kernel, "checker candidate kernel")
    else:
        reported_kernel = kernel
    total = 0
    for q0, word in enumerate(section_words()):
        section_value = perm_text(word_perm(word))
        section = [section_value if index == 0 else alpha_text(section_value)
                   for index in indices]
        if not all(thick_bucket(target[position], coordinate, section[position], groups)
                   for position, coordinate in enumerate(indices)):
            continue
        residual = tuple(perm_text(perm_mul(
            pair_perm(target[position]),
            perm_inverse(pair_perm(section[position]))))
                         for position in range(len(indices)))
        if residual in image:
            total += reported_kernel
    return total


def calculate_query(states: list[dict[str, Any]], indices: tuple[int, ...]) -> dict[str, Any]:
    image = linked_a(indices)
    values = sorted({query_values(state, indices) for state in states})
    l_order = 0
    for word in section_words():
        section_value = perm_text(word_perm(word))
        section = tuple(section_value if index == 0 else alpha_text(section_value)
                        for index in indices)
        if section in image:
            l_order += 1
    kernel = len(states) // len(values)
    return {
        "indices": list(indices), "key": query_key(indices),
        "A": [list(value) for value in sorted(image)],
        "L_order": l_order, "D_order": len(values),
        "kernel_order": kernel,
        "n_values": [{"a": list(value),
                      "count": oracle_count(indices, value, states)}
                     for value in values],
    }


def query_index(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = str(row["key"])
        require(key not in result, "checker duplicate query")
        result[key] = row
    return result


def raw_merge(row: dict[str, Any], coordinate_count: int = 2) -> list[dict[str, Any]]:
    merged: dict[tuple[int, str], int] = {}
    for occurrence in row["raw_occurrences"]:
        coordinate = int(occurrence["coordinate"])
        weight = int(occurrence["weight"]) % 3
        target = str(occurrence["target"])
        require(coordinate in range(coordinate_count) and weight in (0, 1, 2),
                "checker occurrence range")
        pair_perm(target)
        key = (coordinate, target)
        merged[key] = (merged.get(key, 0) + weight) % 3
    return [{"coordinate": coordinate, "target": target,
             "coefficient": coefficient}
            for (coordinate, target), coefficient in sorted(merged.items())
            if coefficient]


def support_sizes(model: dict[str, Any]) -> dict[str, int]:
    result: dict[str, int] = {}
    for block, data in model["dual_support"].items():
        seen: set[str] = set()
        count = 0
        for point in data["points"]:
            spelling = str(point["g"])
            pair_perm(spelling)
            require(spelling not in seen, "checker duplicate support point")
            seen.add(spelling)
            if int(point["coefficient"]) % 3 != 0:
                count += 1
        result[block] = count
    return result


def resource_values(row: dict[str, Any], model: dict[str, Any]) -> dict[str, Any]:
    support = support_sizes(model)
    weighted = sum(support[str(item["block"])]
                   for item in row["raw_occurrences"])
    arity = int(model.get("coordinate_count", 2))
    require(arity > 0, "checker resource coordinate arity")
    merged = raw_merge(row, arity)
    sizes = [len({item["target"] for item in merged
                  if int(item["coordinate"]) == coordinate})
             for coordinate in range(arity)]
    product = 1
    for size in sizes:
        product *= 1 + size
    q, remainder = divmod(weighted, len(sizes))
    balanced_toy = (q + 2) ** remainder * (q + 1) ** (len(sizes) - remainder)
    q10, remainder10 = divmod(weighted, 10)
    balanced = (q10 + 2) ** remainder10 * (q10 + 1) ** (10 - remainder10)
    norm_bound = 2 * (3 ** len(sizes)) * len(model["delta_states"]) * product
    return {"support_weighted_M": weighted,
            "fox_occurrence_count": len(row["raw_occurrences"]),
            "merged_sizes": sizes,
            "actual_term_count": product, "balanced_cap_from_M": balanced,
            "balanced_cap_toy_arity": balanced_toy,
            "diagnostic_norm_bound": norm_bound,
            "diagnostic_signed64_fit": norm_bound < 2 ** 63,
            "support_multiplicities": support}


def e_add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])


def e_scale(a: tuple[int, int], n: int) -> tuple[int, int]:
    return (a[0] * n, a[1] * n)


def e_mul(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    x, y = a
    z, t = b
    return (x * z - y * t, x * t + y * z - y * t)


def omega(exponent: int) -> tuple[int, int]:
    return ((1, 0), (0, 1), (-1, -1))[exponent % 3]


def factor(coefficient: int, model: dict[str, Any]) -> tuple[int, int]:
    values = model["eisenstein_constants"]["omega_minus_one"]
    key = str(coefficient % 3)
    require(key in values, "checker omega factor")
    pair = values[key]
    return (int(pair[0]), int(pair[1]))


def oracle_n(queries: dict[str, dict[str, Any]], indices: tuple[int, ...],
             target: tuple[str, ...], states: list[dict[str, Any]],
             model: dict[str, Any] | None = None) -> int:
    calculated = oracle_count(indices, target, states, model)
    for row in queries[query_key(indices)]["n_values"]:
        if tuple(row["a"]) == target:
            require(int(row["count"]) == calculated, "checker fibre transcript")
            return calculated
    require(calculated == 0, "checker missing fibre target")
    return 0


def expansion(row: dict[str, Any], model: dict[str, Any],
              states: list[dict[str, Any]],
              queries: dict[str, dict[str, Any]]) -> tuple[tuple[int, int], list[dict[str, Any]]]:
    merged = raw_merge(row)
    targets = [[item["target"] for item in merged
                if int(item["coordinate"]) == coordinate]
               for coordinate in range(2)]
    support = [coordinate for coordinate in range(2) if targets[coordinate]]
    result = (0, 0)
    terms: list[dict[str, Any]] = []
    for mask in range(1 << len(support)):
        subset = [support[position] for position in range(len(support))
                  if mask & (1 << position)]
        assignments: list[tuple[str, ...]] = [()]
        for coordinate in subset:
            assignments = [prefix + (value,) for prefix in assignments
                           for value in targets[coordinate]]
        for assignment in assignments:
            count = len(states) if not subset else oracle_n(
                queries, tuple(subset), assignment, states, model)
            product = (1, 0)
            for position, coordinate in enumerate(subset):
                chosen = assignment[position]
                item = next(item for item in merged
                            if int(item["coordinate"]) == coordinate and
                            item["target"] == chosen)
                product = e_mul(product, factor(int(item["coefficient"]), model))
            total_factor = e_mul(omega(int(row["kappa"])), product)
            term = e_scale(total_factor, count)
            result = e_add(result, term)
            terms.append({"subset": list(subset), "targets": list(assignment),
                          "count": count, "factor": list(total_factor),
                          "term": list(term)})
    return result, terms


def direct(row: dict[str, Any], states: list[dict[str, Any]]) -> tuple[tuple[int, int], list[int]]:
    merged = raw_merge(row)
    counts = [0, 0, 0]
    for state in states:
        value = int(row["kappa"])
        for item in merged:
            if state["coordinates"][int(item["coordinate"])] == item["target"]:
                value += int(item["coefficient"])
        counts[value % 3] += 1
    result = (0, 0)
    for index, count in enumerate(counts):
        result = e_add(result, e_scale(omega(index), count))
    return result, counts


def recovered(moment: tuple[int, int], total: int) -> list[int]:
    a, b = moment
    numerator = total - a - b
    require(numerator % 3 == 0, "checker n2 integrality")
    n2 = numerator // 3
    result = [a + n2, b + n2, n2]
    require(all(value >= 0 for value in result), "checker negative n")
    require(sum(result) == total, "checker n sum")
    return result


def validate_anchor(model: dict[str, Any]) -> None:
    anchor = model["anchor"]
    coordinate = int(anchor["coordinate"])
    target = str(anchor["target"])
    q = int(anchor["section_q"])
    groups = coarse_groups(model)
    section_word = section_words()[q]
    section_value = perm_text(word_perm(section_word))
    section = section_value if coordinate == 0 else alpha_text(section_value)
    thick = [q0 for q0, word in enumerate(section_words())
             if thick_bucket(target, coordinate,
                             (lambda value: value if coordinate == 0
                              else alpha_text(value))(perm_text(word_perm(word))),
                             groups)]
    literal = [q0 for q0, word in enumerate(section_words())
               if target == ((lambda value: value if coordinate == 0
                              else alpha_text(value))(perm_text(word_perm(word))))]
    if anchor["bucket_mode"] == "THICK_CI_COSET":
        observed_bucket = thick
    elif anchor["bucket_mode"] == "LITERAL_EQUALITY":
        observed_bucket = literal
    else:
        raise Reject("checker bucket mode")
    require(anchor["thick_bucket"] == observed_bucket,
            "checker bucket execution")
    require(anchor["bucket_mode"] == "THICK_CI_COSET", "checker bucket mode")
    if anchor["residual_side"] == "TARGET_TIMES_SECTION_INVERSE":
        residual_perm = perm_mul(pair_perm(target), perm_inverse(pair_perm(section)))
    elif anchor["residual_side"] == "SECTION_INVERSE_TIMES_TARGET":
        residual_perm = perm_mul(perm_inverse(pair_perm(section)), pair_perm(target))
    else:
        raise Reject("checker residual side")
    require(anchor["residual_side"] == "TARGET_TIMES_SECTION_INVERSE",
            "checker residual side")
    require(anchor["section_value"] == section and anchor["thick_bucket"] == thick,
            "checker thick anchor")
    require(anchor["coset_key"] == list(canonical_coset_key(coordinate, target)),
            "checker canonical left coset")
    require(anchor["literal_bucket"] == literal and not literal and target != section,
            "checker literal distinction")
    require(anchor["selected_q"] == q and q in thick, "checker selected q")
    residual = perm_text(residual_perm)
    require(anchor["residual"] == residual and anchor["literal_misses"] is True,
            "checker residual record")


def validate_row(row: dict[str, Any], model: dict[str, Any],
                states: list[dict[str, Any]]) -> None:
    cancelled = [item for item in row["raw_occurrences"]
                 if str(item["target"]) == "1:1"]
    require(cancelled and sum(int(item["weight"]) for item in cancelled) % 3 == 0,
            "checker explicit cancellation")
    merged = raw_merge(row)
    require(row["merged"] == merged, "checker merge cancellation")
    resources = resource_values(row, model)
    for key in ("support_weighted_M", "merged_sizes", "actual_term_count",
                "fox_occurrence_count", "balanced_cap_from_M",
                "balanced_cap_toy_arity",
                "diagnostic_norm_bound", "diagnostic_signed64_fit",
                "support_multiplicities"):
        require(row["resource"][key] == resources[key], f"checker resource {key}")
    require(resources["actual_term_count"] <= resources["balanced_cap_from_M"],
            "checker v138 balanced bound")
    require(len(row["partial_terms"]) == resources["actual_term_count"],
            "checker exact toy term count")
    queries = query_index(model["queries"])
    moment, terms = expansion(row, model, states, queries)
    direct_value, distribution = direct(row, states)
    require(moment == direct_value, "checker expansion/direct equality")
    require(row["partial_terms"] == terms, "checker term multiplication")
    require(tuple(row["moment"]) == moment, "checker moment")
    require(row["distribution"] == distribution, "checker distribution")
    require(row["recovered_n"] == recovered(moment, len(states)),
            "checker recovered counts")
    if row["id"] == "zero":
        require(moment == (len(states), 0) and row["recovered_n"] == [6, 0, 0],
                "checker all-zero control")
    else:
        require(moment != (0, 0) and sum(distribution[1:]) > 0,
                "checker active positive")


def validate_model(model: dict[str, Any]) -> None:
    require(model["coordinate_count"] == 2, "checker toy coordinate arity")
    states = model["delta_states"]
    require(states == expected_delta(), "checker section reconstruction")
    require(perm_mul(REFLECTION, ROTATION) != perm_mul(ROTATION, REFLECTION),
            "checker noncommutativity")
    require(model["noncommutative"] == {"linked_extension": True, "order": 6,
                                         "different_products": True},
            "checker noncommutative record")
    expected_groups = {"0": sorted(PAIR_TEXT[p] for p in coarse_groups()[0]),
                       "1": sorted(PAIR_TEXT[p] for p in coarse_groups()[1])}
    require(model["coarse_groups"] == expected_groups, "checker coarse C_i")
    require(model["gamma_coarse_order"] == len(coarse_groups()[0]) == 3,
            "checker gamma coarse order")
    require(model["linked_graph_order"] == len(linked_a((0, 1))) == 3,
            "checker linked graph order")
    queries = query_index(model["queries"])
    for indices in ((0,), (1,), (0, 1)):
        expected = calculate_query(states, indices)
        actual = queries[query_key(indices)]
        for key in ("indices", "A", "L_order", "D_order", "kernel_order", "n_values"):
            require(actual[key] == expected[key], f"checker query {query_key(indices)} {key}")
    require(queries["0,1"]["A"] == [["0:0", "0:0"],
                                     ["1:0", "2:0"],
                                     ["2:0", "1:0"]], "checker graph orientation")
    require(queries["0,1"]["kernel_order"] == 1, "checker kernel")
    validate_anchor(model)

    witness = model["active_witness"]
    source = concat_word(gamma_words()[int(witness["gamma_state"])],
                         section_words()[int(witness["section_q"])])
    require(witness["gamma_state_coord0"] == witness["gamma_state_coord1"] == 1,
            "checker Gamma state linkage")
    require(witness["source_word"] == source, "checker source concat")
    state = next(row for row in states if row["id"] == witness["delta_id"])
    replay0 = concat_word(gamma_words()[int(witness["gamma_state_coord0"])],
                          section_words()[int(witness["section_q"])])
    replay1 = concat_word(gamma_words()[int(witness["gamma_state_coord1"])],
                          section_words()[int(witness["section_q"])])
    require(perm_text(word_perm(replay0)) == witness["target"][0],
            "checker coordinate zero Gamma replay")
    require(alpha_text(perm_text(word_perm(replay1))) == witness["target"][1],
            "checker coordinate one Gamma replay")
    require(state["word"] == source and state["coordinates"] == witness["target"],
            "checker coordinate replay")
    require(witness["residual"] == ["1:0", "2:0"] and
            witness["fiber_order"] == 1 and witness["membership"] is True,
            "checker witness oracle")
    require(oracle_count((0, 1), tuple(witness["target"]), states, model) == 1,
            "checker witness membership")
    require(model["eisenstein_constants"]["omega_minus_one"] == {
        "0": [0, 0], "1": [-1, 1], "2": [-2, -1]}, "checker omega constants")
    require(model["resource_policy"] == "SUPPORT_PARAMETRIC_TOY_ONLY",
            "checker resource policy")
    require(model["resource_policy_production"] == "DYNAMIC_REGISTERED_CEILING",
            "checker production resource policy")
    require(model["production_cap"] == "DYNAMIC_REGISTERED_CEILING",
            "checker production cap is dynamic")
    require(model["withdrawn_v136_claims"] == [
        "UNCONDITIONAL_PER_ROW_CAP_1536",
        "UNCONDITIONAL_ALL_ROW_CAP_9893376",
        "UNCONDITIONAL_SIGNED64_SAFETY"], "checker withdrawn claims")
    for row in model["weighted_rows"]:
        validate_row(row, model, states)


MUTATIONS = [
    "same_target_merge_cancellation", "coarse_identity_replacement",
    "literal_equality_bucket", "residual_side_order",
    "wrong_anchor_bucket_state", "different_gamma_states", "graph_orientation",
    "kernel_order", "partial_membership_bit", "omega_minus_one_pair",
    "eisenstein_multiplication_coordinate", "constant_K", "recovered_nj",
    "word_section_gamma_concat", "block_support_multiplicity",
    "fox_occurrence_M", "withdrawn_v136_cap",
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
        raise Reject(f"unknown checker mutation {name}")
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
                "checker immutable fixture")


def load_fixture(path: Path) -> dict[str, Any]:
    fixture_identity(path)
    value = json.loads(path.read_text(encoding="ascii"))
    require(value["schema"] == SELFTEST_SCHEMA and value["status"] == "SELFTEST" and
            value["terminal"] == "FIXTURE_PASS", "checker fixture envelope")
    return value


def selftest(path: Path) -> int:
    fixture = load_fixture(path)
    validate_model(fixture["model"])
    attempted, rejected = run_mutations(fixture["model"])
    require(attempted == 17 and rejected == 17, "checker semantic mutations")
    print("R07_CUBIC_COSET_MOMENT_ORACLE_V2_CHECKER_SELFTEST_PASS "
          f"mutations={attempted} rejected={rejected} "
          f"gamma_coarse_order={len(coarse_groups()[0])} "
          f"linked_graph_order={len(linked_a((0, 1)))}", flush=True)
    return 0


def validate_receipt(value: dict[str, Any], raw: bytes) -> str:
    require(value["schema"] == SCHEMA and value["status"] == "UNKNOWN_INPUT",
            "checker receipt schema")
    require(value["terminal"] == UNKNOWN_INPUT and
            value["reason"] == "PREREQUISITE_NOT_PINNED" and
            value["result"] is None, "checker receipt terminal")
    require(value["resource_theorem"] == "v138_SUPPORT_PARAMETRIC_CAP" and
            value["integer_arithmetic"] == "ARBITRARY_PRECISION_REQUIRED",
            "checker active resource theorem")
    require(value["resource_contract"]["actual_coordinate_count"] == 10 and
            value["resource_contract"]["conditional_norm_formula"] ==
            "2*3^10*N*P_actual", "checker conditional v138 bound")
    require(value["withdrawn_resource_claims"] == [
        "v136_per_row_1536", "v136_all_rows_9893376",
        "v136_unconditional_signed64"], "checker withdrawn v136 claims")
    require(value["streaming"]["large_table_allocated"] is False,
            "checker repository table allocation")
    for key in ("all_seven_solution", "correction_word", "separator",
                "cofinal_lift", "fake", "Ihara_witness"):
        require(value["boundaries"][key] is False, f"checker receipt boundary {key}")
    unsigned = dict(value)
    digest = unsigned.pop("self_digest_sha256", None)
    require(digest == sha_obj(unsigned), "checker receipt digest")
    require(isinstance(raw, bytes) and len(raw) > 0, "checker receipt bytes")
    return str(value["terminal"])


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    unsigned = dict(value)
    unsigned.pop("self_digest_sha256", None)
    sealed = dict(unsigned)
    sealed["self_digest_sha256"] = sha_obj(unsigned)
    path.write_bytes(canonical(sealed) + b"\n")


def production(args: argparse.Namespace) -> int:
    receipt_path = Path(args.receipt)
    raw = receipt_path.read_bytes()
    receipt = json.loads(raw.decode("ascii"))
    terminal = validate_receipt(receipt, raw)
    verdict = {
        "schema": CHECKER_SCHEMA,
        "status": "PASS",
        "terminal": terminal,
        "receipt_terminal": terminal,
        "reason": "PREREQUISITE_NOT_PINNED",
        "producer_receipt_sha256": sha_bytes(raw),
        "result": None,
        "self_digest_sha256": None,
    }
    write_json(Path(args.verdict), verdict)
    print(f"R07_CUBIC_COSET_MOMENT_ORACLE_V2_CHECKER_PASS terminal={terminal}",
          flush=True)
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    modes = result.add_mutually_exclusive_group(required=True)
    modes.add_argument("--selftest", action="store_true")
    modes.add_argument("--check", action="store_true")
    result.add_argument("--fixture", default=str(FIXTURE))
    result.add_argument("--receipt")
    result.add_argument("--verdict")
    return result


def main() -> int:
    args = parser().parse_args()
    if args.selftest:
        return selftest(Path(args.fixture))
    if not args.receipt or not args.verdict:
        raise SystemExit("--receipt and --verdict are required")
    return production(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, OSError, ValueError, KeyError, TypeError,
            json.JSONDecodeError) as exc:
        print(f"R07_CUBIC_COSET_MOMENT_ORACLE_V2_CHECKER_STOP {exc}",
              file=sys.stderr, flush=True)
        raise SystemExit(1)
