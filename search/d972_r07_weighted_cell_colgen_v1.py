#!/usr/bin/env python3
"""R07 weighted-cell column-generation skeleton.

The production branch is deliberately held at the typed prerequisite gate
until task175 and task176 have authenticated positive run pins.  The
SELFTEST is a small, genuinely non-commutative linked extension.  It runs
the weighted merge, Boolean-cell, lazy projection, source-word, typed
boundary, target, and replay checks through the same validator used by the
mutation suite.

This file has no runtime import of any predecessor producer or checker.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-weighted-cell-colgen/v1"
SELFTEST_SCHEMA = "d972-r07-weighted-cell-colgen-selftest/v1"
PASS = "R07_WEIGHTED_CELL_COLGEN_COMMON_WORD"
SEPARATOR = "R07_WEIGHTED_CELL_COLGEN_SEPARATOR"
UNKNOWN_INPUT = "UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
FIXTURE = ROOT / "search/certs/d972_r07_weighted_cell_colgen_selftest_v1_20260827.json"

# Filled after the immutable fixture is sealed.  The driver carries the
# final values as well; a mismatch is an input failure, never a PASS.
FIXTURE_BYTES = 4932
FIXTURE_SHA256 = "d118633552b5d827d62101f063ba9d7d60fd4335f3744169f85f6cbb2b95da8b"

CAPS = {
    "iterations": 0,
    "sparse_nonzeros": 0,
    "subset_queries": 64,
    "cell_terms": 4096,
    "q0_scans": 1,
    "source_pair_tests": 250000,
    "disk_bytes": 3_000_000_000,
    "wall_seconds": 20_000,
    "rss_bytes": 16_000_000_000,
}

# The parent has not yet supplied authenticated positive task175/task176 run
# ids, head SHAs, receipt digests, and checker verdict digests.
REGISTERED_PREREQUISITE_MANIFEST: Path | None = None

PROOF_PINS = {
    "v110": {
        "path": "sol/proof_r07_full_e4_seven_evaluation_orbit_selector_v110.md",
        "bytes": 12136,
        "sha256": "dd0b75d6dc85229405a3a95e3631a709aa40a0ad21f2c17b96106dae2c7989dc",
    },
    "v118": {
        "path": "sol/proof_r07_context_fibre_dual_correlation_v118.md",
        "bytes": 8776,
        "sha256": "6ef2cbf4ebf5ff3466b5eaf21ef4da572684517eb2f6d18c23fd12c8ad3ada3b",
    },
    "v125": {
        "path": "sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md",
        "bytes": 8545,
        "sha256": "b82c81e0a053658fdb48cbb4d3054a094a57a81b2fd5d0153bcd0735ef4852b3",
    },
    "v132": {
        "path": "sol/proof_r07_weighted_context_cell_selector_v132.md",
        "bytes": 13394,
        "sha256": "a6096938bf5a8b0bdb4844ea973f2687d7eb1b28438ef2d8cc08cdf273667614",
    },
}


class Reject(RuntimeError):
    """A deterministic certificate or fixture rejection."""


class InputStop(RuntimeError):
    """A missing or not-yet-registered production input."""


class ResourceStop(RuntimeError):
    """A registered streaming or solver cap."""


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
    out: list[int] = []
    for letter in word:
        require(isinstance(letter, int) and letter in (-2, -1, 1, 2),
                "free word letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


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


# D6 = C3 semidirect C2.  The first coordinate is the rotation exponent and
# the second is the reflection bit.  This is a linked extension, not a
# direct product: a reflection inverts the rotation.
def d6_mul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    r1, f1 = left
    r2, f2 = right
    sign = -1 if f1 else 1
    return ((r1 + sign * r2) % 3, (f1 + f2) % 2)


def d6_inverse(value: tuple[int, int]) -> tuple[int, int]:
    for r in range(3):
        for f in range(2):
            if d6_mul(value, (r, f)) == (0, 0) and d6_mul((r, f), value) == (0, 0):
                return (r, f)
    raise Reject("D6 inverse")


def d6_word(word: Iterable[int]) -> tuple[int, int]:
    result = (0, 0)
    generators = {1: (0, 1), 2: (1, 0)}
    for letter in word:
        generator = generators[abs(letter)]
        if letter < 0:
            generator = d6_inverse(generator)
        result = d6_mul(result, generator)
    return result


def pair_text(value: tuple[int, int]) -> str:
    return f"{value[0]}:{value[1]}"


def parse_pair(value: str) -> tuple[int, int]:
    parts = value.split(":")
    require(len(parts) == 2, "pair spelling")
    result = (int(parts[0]), int(parts[1]))
    require(result[0] in range(3) and result[1] in range(2), "pair range")
    return result


def gamma_words() -> list[list[int]]:
    return [[], [2], [2, 2]]


def section_words() -> list[list[int]]:
    return [[], [1]]


def expected_delta() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for q0 in range(2):
        for gamma in range(3):
            word = concat_word(gamma_words()[gamma], section_words()[q0])
            value = d6_word(word)
            rows.append({
                "id": f"d{gamma}{q0}", "gamma": gamma, "q0": q0,
                "word": word, "value": pair_text(value),
                "coordinates": [pair_text(value), str(value[0])],
            })
    return rows


def record_map(records: list[dict[str, Any]], key: str) -> dict[Any, dict[str, Any]]:
    result: dict[Any, dict[str, Any]] = {}
    for row in records:
        require(row[key] not in result, f"duplicate {key}")
        result[row[key]] = row
    return result


def tuple_key(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(str(value) for value in values)


def query_key(indices: Iterable[int]) -> str:
    return ",".join(str(index) for index in indices)


def query_values(state: dict[str, Any], indices: tuple[int, ...]) -> tuple[str, ...]:
    return tuple(state["coordinates"][index] for index in indices)


def calculate_query(states: list[dict[str, Any]], indices: tuple[int, ...]) -> dict[str, Any]:
    gamma_rows = [
        {"coordinates": [pair_text(d6_word(word)), str(d6_word(word)[0])]}
        for word in gamma_words()
    ]
    # The above is intentionally recomputed from words rather than copied
    # from the fixture's coordinate table.
    a_values = sorted({query_values(row, indices) for row in gamma_rows})
    q_rows = [{"q0": q, "coordinates": [pair_text(d6_word(section_words()[q])),
                                             str(d6_word(section_words()[q])[0])]} for q in range(2)]
    l_rows = [row for row in q_rows if query_values(row, indices) in a_values]
    d_values = sorted({query_values(row, indices) for row in states})
    kernel_order = 6 // len(d_values)
    n_values = [{"a": list(value), "count": kernel_order} for value in d_values]
    return {
        "indices": list(indices), "key": query_key(indices),
        "A": [list(value) for value in a_values],
        "L_order": len(l_rows), "D_order": len(d_values),
        "kernel_order": kernel_order, "n_values": n_values,
    }


def raw_occurrence_merge(row: dict[str, Any]) -> list[dict[str, Any]]:
    merged: dict[tuple[int, str], int] = {}
    for occurrence in row["raw_occurrences"]:
        coord = int(occurrence["coord"])
        target = str(occurrence["target"])
        weight = int(occurrence["weight"]) % 3
        require(coord in (0, 1) and weight in (0, 1, 2), "occurrence range")
        key = (coord, target)
        merged[key] = (merged.get(key, 0) + weight) % 3
    result = [
        {"coord": coord, "target": target, "coefficient": coefficient}
        for (coord, target), coefficient in sorted(merged.items())
        if coefficient
    ]
    return result


def query_index(queries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for query in queries:
        key = str(query["key"])
        require(key not in result, "duplicate subset query")
        result[key] = query
    return result


def n_value(queries: dict[str, dict[str, Any]],
            fixed: dict[int, str], states: list[dict[str, Any]]) -> int:
    if not fixed:
        return len(states)
    indices = tuple(sorted(fixed))
    key = query_key(indices)
    query = queries[key]
    target = tuple(fixed[index] for index in indices)
    for row in query["n_values"]:
        if tuple_key(row["a"]) == target:
            return int(row["count"])
    return 0


def inclusion_exclusion_count(pattern: list[str], targets: list[list[str]],
                              queries: dict[str, dict[str, Any]],
                              states: list[dict[str, Any]],
                              signs: dict[str, int]) -> int:
    fixed = {index: pattern[index] for index in range(2) if pattern[index] != "*"}
    stars = [index for index in range(2) if pattern[index] == "*"]
    result = 0
    for mask in range(1 << len(stars)):
        assigned = dict(fixed)
        bit_count = 0
        choices: list[list[str]] = []
        for position, index in enumerate(stars):
            if mask & (1 << position):
                choices.append(targets[index])
            else:
                choices.append([None])
        assignments: list[dict[int, str]] = [assigned]
        for position, values in enumerate(choices):
            if values == [None]:
                continue
            bit_count += 1
            expanded: list[dict[int, str]] = []
            for base in assignments:
                for value in values:
                    current = dict(base)
                    current[stars[position]] = value
                    expanded.append(current)
            assignments = expanded
        sign = int(signs[str(bit_count)])
        for assignment in assignments:
            result += sign * n_value(queries, assignment, states)
    return result


def cell_value(row: dict[str, Any], pattern: list[str]) -> int:
    value = int(row["kappa"]) % 3
    for occurrence in raw_occurrence_merge(row):
        if pattern[occurrence["coord"]] == occurrence["target"]:
            value += int(occurrence["coefficient"])
    return value % 3


def cell_patterns(targets: list[list[str]]) -> list[list[str]]:
    result: list[list[str]] = [[]]
    for values in targets:
        result = [prefix + [value] for prefix in result for value in ["*"] + values]
    return result


def sparse_rows(rows: list[dict[str, Any]]) -> dict[tuple[int, str, str], int]:
    result: dict[tuple[int, str, str], int] = {}
    for row in rows:
        tag = int(row["block_tag"])
        component = str(row["component"])
        element = str(row["element"])
        coefficient = int(row["coefficient"]) % 3
        require(tag in (1, 2, 3), "block tag")
        key = (tag, component, element)
        result[key] = (result.get(key, 0) + coefficient) % 3
    return {key: value for key, value in result.items() if value}


def add_sparse(left: dict[tuple[int, str, str], int],
               right: dict[tuple[int, str, str], int], scale: int = 1) -> dict[tuple[int, str, str], int]:
    result = dict(left)
    for key, value in right.items():
        result[key] = (result.get(key, 0) + scale * value) % 3
        if result[key] == 0:
            del result[key]
    return result


def expected_target(model: dict[str, Any]) -> dict[tuple[int, str, str], int]:
    tags = {"H1": 1, "H2": 2, "P": 3}
    result: dict[tuple[int, str, str], int] = {}
    for block, data in model["raw_base_targets"].items():
        tag = tags[block]
        result[(tag, str(data["component"]), str(data["element"]))] = (-int(data["coefficient"])) % 3
    return {key: value for key, value in result.items() if value}


def expected_pentagon(model: dict[str, Any]) -> tuple[int, int]:
    result = (0, 0)
    words = model["pentagon"]["factor_words"]
    for index, sign in zip(model["pentagon"]["ordered_indices"],
                           model["pentagon"]["ordered_signs"]):
        value = d6_word(words[index])
        if int(sign) < 0:
            value = d6_inverse(value)
        result = d6_mul(result, value)
    return result


def validate_model(model: dict[str, Any]) -> None:
    """Validate the semantic selftest certificate, not a dictionary digest."""
    states = model["delta_states"]
    require(states == expected_delta(), "linked extension section table")
    require(d6_word([1, 2]) != d6_word([2, 1]), "noncommutative witness")
    require(model["noncommutative"]["different"] is True, "noncommutative marker")

    queries = query_index(model["queries"])
    for indices in ((0,), (1,), (0, 1)):
        expected = calculate_query(states, indices)
        actual = queries[query_key(indices)]
        for key in ("A", "L_order", "D_order", "kernel_order", "n_values"):
            require(actual[key] == expected[key], f"subset query {key}")

    row = model["weighted_rows"][0]
    merged = raw_occurrence_merge(row)
    require(row["merged"] == merged, "merged occurrence coefficients")
    targets = [sorted({item["target"] for item in merged if item["coord"] == index})
               for index in range(2)]
    require(targets == [["0:1"], ["1", "2"]], "weighted target sets")
    require(row["include_complement"] is True, "all-star complement registered")
    require(row["ie_sign_table"] == {"0": 1, "1": -1, "2": 1},
            "inclusion-exclusion signs")
    cells = {tuple(cell["pattern"]): cell for cell in row["cells"]}
    patterns = cell_patterns(targets)
    require(set(cells) == {tuple(pattern) for pattern in patterns}, "Boolean cell coverage")
    for pattern in patterns:
        cell = cells[tuple(pattern)]
        count = inclusion_exclusion_count(pattern, targets, queries, states,
                                          row["ie_sign_table"])
        require(count >= 0, "cell count nonnegative")
        require(int(cell["count"]) == count, "cell inclusion-exclusion count")
        require(int(cell["value"]) == cell_value(row, pattern), "cell weighted value")
        require(bool(cell["active"]) == (count > 0 and int(cell["value"]) != 0),
                "cell active type")
    require(cells[("*", "*")]["count"] == 1, "all-star complement count")

    witness = model["active_witness"]
    state = record_map(states, "id")[witness["delta_id"]]
    require(witness["pattern"] == ["0:1", "*"], "active witness pattern")
    witness_cell = cells[tuple(witness["pattern"])]
    require(witness_cell["active"] is True, "active witness cell")
    require(state["word"] == witness["section_word"], "section word replay")
    require(witness["gamma_word"] == [], "Gamma adjustment replay")
    require(witness["conjugator"] == concat_word(witness["gamma_word"],
                                                   witness["section_word"]),
            "source transversal word")
    source = concat_word(witness["conjugator"], witness["relation_word"],
                         inverse_word(witness["conjugator"]))
    require(witness["source_word"] == source, "conjugate source spelling")
    require(d6_word(witness["relation_word"]) == (0, 0), "relation replay")
    require(d6_word(source) == (0, 0), "conjugate replay")
    require(exponent_sums(source) == [0, 0], "source exponent sums")

    expected_tags = {"PB3_H1": 1, "PB3_H2": 2, "PB4_P": 3}
    for boundary in model["boundary_columns"]:
        require(int(boundary["block_tag"]) == expected_tags[boundary["id"]],
                "typed PB3/PB4 block tag")
        require(boundary["kind"] in ("PB3", "PB4"), "boundary kind")
        if boundary["kind"] == "PB3":
            require(int(boundary["block_tag"]) in (1, 2), "PB3 block")
        else:
            require(int(boundary["block_tag"]) == 3, "PB4 block")

    target = expected_target(model)
    target_rows = sparse_rows(model["target"]["rows"])
    require(target_rows == target, "negative base-defect target")
    require(model["target"]["exponents"] == [0, 0], "target exponent coordinates")
    column = model["correction_column"]
    require(column["delta_id"] == witness["delta_id"], "column witness identity")
    require(column["exponents"] == exponent_sums(witness["source_word"]),
            "column exponent coordinates")
    correction = sparse_rows(column["rows"])
    require(correction == target, "word-bearing correction column")
    solution = model["solution"]
    require(solution["correction_coefficients"] == {"C0": 1},
            "final correction coefficient")
    boundary_by_id = {row["id"]: row for row in model["boundary_columns"]}
    total: dict[tuple[int, str, str], int] = {}
    for boundary_id, coefficient in solution["boundary_coefficients"].items():
        total = add_sparse(total, sparse_rows(boundary_by_id[boundary_id]["rows"]),
                           int(coefficient))
    total = add_sparse(total, correction, 1)
    require(total == target, "typed sparse target sum")
    require(solution["correction_word"] == witness["source_word"],
            "one common correction word")
    require(reduce_word(model["g760"] + solution["correction_word"]) ==
            model["corrected_word"], "right correction convention")
    require(exponent_sums(solution["correction_word"]) == [0, 0],
            "final correction exponent sums")

    require(d6_word(model["hexagons"]["H1"]) == (0, 0), "H1 replay")
    require(d6_word(model["hexagons"]["H2"]) == (0, 0), "H2 replay")
    require(expected_pentagon(model) == (0, 0), "ordered pentagon replay")


MUTATIONS = [
    "merged_same_target_cancellation",
    "multi_coordinate_target",
    "inclusion_exclusion_sign",
    "kernel_order",
    "complement_all_star",
    "section_gamma_adjustment",
    "source_word_transversal",
    "pb3_pb4_block_tag",
    "target_base_defect_coordinate",
    "exponent_coordinate",
    "final_correction_coefficient",
    "pentagon_factor_order_sign",
]


def mutate(model: dict[str, Any], name: str) -> dict[str, Any]:
    mutated = copy.deepcopy(model)
    if name == "merged_same_target_cancellation":
        mutated["weighted_rows"][0]["raw_occurrences"][2]["weight"] = 1
    elif name == "multi_coordinate_target":
        for query in mutated["queries"]:
            if query["key"] == "0,1":
                query["n_values"][3]["count"] = 0
    elif name == "inclusion_exclusion_sign":
        mutated["weighted_rows"][0]["ie_sign_table"]["1"] = 1
    elif name == "kernel_order":
        for query in mutated["queries"]:
            if query["key"] == "1":
                query["kernel_order"] = 1
    elif name == "complement_all_star":
        mutated["weighted_rows"][0]["include_complement"] = False
    elif name == "section_gamma_adjustment":
        mutated["active_witness"]["section_word"] = [2]
    elif name == "source_word_transversal":
        mutated["active_witness"]["conjugator"] = [2]
    elif name == "pb3_pb4_block_tag":
        mutated["boundary_columns"][0]["block_tag"] = 2
    elif name == "target_base_defect_coordinate":
        mutated["raw_base_targets"]["H1"]["coefficient"] = 1
    elif name == "exponent_coordinate":
        mutated["correction_column"]["exponents"][0] = 1
    elif name == "final_correction_coefficient":
        mutated["solution"]["correction_coefficients"]["C0"] = 2
    elif name == "pentagon_factor_order_sign":
        mutated["pentagon"]["ordered_signs"][4] = 1
    else:
        raise Reject(f"unknown mutation {name}")
    return mutated


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
                "immutable selftest fixture")


def load_fixture(path: Path) -> dict[str, Any]:
    fixture_identity(path)
    value = json.loads(path.read_text(encoding="ascii"))
    require(value["schema"] == SELFTEST_SCHEMA and
            value["status"] == "SELFTEST" and
            value["terminal"] == "FIXTURE_PASS", "fixture envelope")
    require(value["model"]["noncommutative"]["linked_extension"] is True,
            "linked noncommutative fixture")
    return value


def selftest(path: Path) -> int:
    fixture = load_fixture(path)
    model = fixture["model"]
    validate_model(model)
    attempted, rejected = run_mutations(model)
    require(attempted == 12 and rejected == 12, "semantic mutation suite")
    print("R07_WEIGHTED_CELL_COLGEN_PRODUCER_SELFTEST_PASS "
          "mutations=12 rejected=12 linked_nonabelian_order=6", flush=True)
    return 0


def stream_fixed_rows(rows: Iterable[bytes], width: int) -> dict[str, Any]:
    """Production skeleton: stream fixed-width rows outside the repository."""
    require(width > 0, "fixed row width")
    total = 0
    digest = hashlib.sha256()
    with tempfile.NamedTemporaryFile(prefix="r07_colgen_", suffix=".bin",
                                     dir=tempfile.gettempdir(), delete=False) as handle:
        temporary = Path(handle.name)
        for row in rows:
            require(len(row) == width, "fixed row length")
            handle.write(row)
            digest.update(row)
            total += len(row)
            if total > CAPS["disk_bytes"]:
                raise ResourceStop("fixed_width_disk_bytes")
    return {"path": str(temporary), "bytes": total, "sha256": digest.hexdigest(),
            "record_width": width}


def load_pinned_json(path: Path, expected_bytes: int,
                     expected_sha256: str) -> dict[str, Any]:
    """Read an authenticated receipt as data, never as executable code."""
    raw = path.read_bytes()
    require(len(raw) == expected_bytes and sha_bytes(raw) == expected_sha256,
            f"prerequisite receipt pin {path}")
    value = json.loads(raw.decode("ascii"))
    require(isinstance(value, dict), "prerequisite receipt object")
    return value


def prerequisite_manifest_shape(manifest: dict[str, Any]) -> None:
    """Schema-only gate used after a parent registers positive run pins."""
    for label, terminal in (("task175", "R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_READY"),
                            ("task176", "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS")):
        row = manifest.get(label)
        require(isinstance(row, dict), f"missing prerequisite {label}")
        require(isinstance(row.get("run_id"), int) and row["run_id"] > 0,
                f"{label} run id")
        require(isinstance(row.get("head_sha"), str) and len(row["head_sha"]) == 40,
                f"{label} head sha")
        require(isinstance(row.get("receipt_path"), str), f"{label} receipt path")
        require(isinstance(row.get("receipt_bytes"), int) and row["receipt_bytes"] > 0,
                f"{label} receipt bytes")
        require(isinstance(row.get("receipt_sha256"), str) and
                len(row["receipt_sha256"]) == 64, f"{label} receipt digest")
        require(isinstance(row.get("checker_verdict_path"), str),
                f"{label} checker verdict path")
        require(isinstance(row.get("checker_verdict_sha256"), str) and
                len(row["checker_verdict_sha256"]) == 64,
                f"{label} checker verdict digest")
        require(row.get("terminal") == terminal, f"{label} positive terminal")


def ingest_prerequisites(manifest_path: Path) -> dict[str, Any]:
    """Bounded future handoff; this is unreachable while pins are unresolved."""
    manifest = json.loads(manifest_path.read_text(encoding="ascii"))
    prerequisite_manifest_shape(manifest)
    receipts: dict[str, Any] = {}
    for label in ("task175", "task176"):
        row = manifest[label]
        receipt = load_pinned_json(Path(row["receipt_path"]),
                                   int(row["receipt_bytes"]),
                                   str(row["receipt_sha256"]))
        require(receipt.get("terminal") == row["terminal"],
                f"{label} receipt terminal")
        receipts[label] = receipt
    return {"manifest": manifest, "receipts": receipts}


def weighted_column_generation(_inputs: dict[str, Any]) -> None:
    """Reserved production phase after authenticated task175/task176 runs."""
    raise ResourceStop("weighted_column_generation_not_registered")


def authenticated_prerequisite_gate(manifest: Path | None) -> None:
    # No task175/task176 positive run ids, head SHAs, receipt digests, or
    # checker verdict digests have been registered for this version.  Keeping
    # this gate closed is intentional; a caller cannot promote a checked-in
    # UNKNOWN fixture or an old selftest log into production input.
    if REGISTERED_PREREQUISITE_MANIFEST is not None:
        require(manifest is not None and manifest == REGISTERED_PREREQUISITE_MANIFEST,
                "PREREQUISITE_NOT_PINNED")
        # Parsing is deliberately kept behind the unregistered promotion
        # switch.  It cannot turn a checked-in UNKNOWN into a positive run.
        _ = ingest_prerequisites(manifest)
    raise InputStop("PREREQUISITE_NOT_PINNED")


def production_receipt() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "UNKNOWN_INPUT",
        "terminal": UNKNOWN_INPUT,
        "reason": "PREREQUISITE_NOT_PINNED",
        "result": None,
        "pins": {
            "task175_run": None,
            "task176_run": None,
            "task175_receipt_sha256": None,
            "task176_receipt_sha256": None,
            "task175_checker_verdict_sha256": None,
            "task176_checker_verdict_sha256": None,
            "proofs": PROOF_PINS,
        },
        "caps": CAPS,
        "streaming": {
            "fixed_width_binary_outside_repository": True,
            "gamma_order": 243,
            "q0_order": 1469664,
            "coordinate_widths": [40, 40, 40, 40, 40, 154, 154, 154, 154, 154],
            "direct_delta_enumeration": False,
            "q0_scan_shared_per_iteration": True,
        },
        "phases": {
            "prerequisite_gate": "NOT_PINNED",
            "weighted_occurrences": "NOT_RUN",
            "lazy_projection_oracle": "NOT_RUN",
            "boundary_correlation": "NOT_RUN",
            "column_generation": "NOT_RUN",
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
        "unknowns": ["task175 positive run pins", "task176 positive run pins"],
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    unsigned = dict(value)
    unsigned.pop("self_digest_sha256", None)
    value = dict(unsigned)
    value["self_digest_sha256"] = sha_obj(unsigned)
    path.write_bytes(json.dumps(value, sort_keys=True, separators=(",", ":"),
                              ensure_ascii=True).encode("ascii") + b"\n")


def production(args: argparse.Namespace) -> int:
    receipt = production_receipt()
    try:
        authenticated_prerequisite_gate(Path(args.prerequisites) if args.prerequisites else None)
        # This branch is unreachable until the parent reseals registered run
        # pins.  It remains here to make the streaming handoff explicit.
        raise InputStop("PREREQUISITE_NOT_PINNED")
    except InputStop:
        pass
    write_json(Path(args.output), receipt)
    print(f"R07_WEIGHTED_CELL_COLGEN_PRODUCER_TERMINAL {receipt['terminal']}", flush=True)
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    mode = result.add_mutually_exclusive_group(required=True)
    mode.add_argument("--selftest", action="store_true")
    mode.add_argument("--run-colgen", action="store_true")
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
        print(f"R07_WEIGHTED_CELL_COLGEN_PRODUCER_STOP {exc}",
              file=sys.stderr, flush=True)
        raise SystemExit(1)
