#!/usr/bin/env python3
"""Independent checker for the R07 weighted-cell column-generation task.

The checker does not import the producer or any predecessor API.  Its
SELFTEST uses a permutation representation of the same small linked
extension, so all semantic mutations travel through an independent replay
path rather than through receipt or dictionary equality.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-weighted-cell-colgen/v1"
SELFTEST_SCHEMA = "d972-r07-weighted-cell-colgen-selftest/v1"
UNKNOWN_INPUT = "UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED"
FIXTURE = ROOT / "search/certs/d972_r07_weighted_cell_colgen_selftest_v1_20260827.json"
FIXTURE_BYTES = 4932
FIXTURE_SHA256 = "d118633552b5d827d62101f063ba9d7d60fd4335f3744169f85f6cbb2b95da8b"


class Reject(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def stable(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest_value(value: Any) -> str:
    return digest(stable(value))


def inverse_free(word: list[int]) -> list[int]:
    return [-letter for letter in word[::-1]]


def normalize(word: list[int]) -> list[int]:
    stack: list[int] = []
    for letter in word:
        need(letter in (-2, -1, 1, 2), "word alphabet")
        if stack and stack[-1] + letter == 0:
            stack.pop()
        else:
            stack.append(letter)
    return stack


def join(*parts: list[int]) -> list[int]:
    result: list[int] = []
    for part in parts:
        result = normalize(result + list(part))
    return result


Perm = tuple[int, int, int]
IDENTITY: Perm = (0, 1, 2)
GENERATOR_A: Perm = (0, 2, 1)
GENERATOR_B: Perm = (1, 2, 0)


def compose(first: Perm, second: Perm) -> Perm:
    return tuple(first[second[index]] for index in range(3))  # type: ignore[return-value]


def inverse_perm(value: Perm) -> Perm:
    result = [0, 0, 0]
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)  # type: ignore[return-value]


PAIR_PERM: dict[str, Perm] = {
    "0:0": (0, 1, 2),
    "1:0": (1, 2, 0),
    "2:0": (2, 0, 1),
    "0:1": (0, 2, 1),
    "1:1": (1, 0, 2),
    "2:1": (2, 1, 0),
}
PERM_PAIR = {value: key for key, value in PAIR_PERM.items()}


def permutation_word(word: list[int]) -> Perm:
    result = IDENTITY
    for letter in word:
        value = GENERATOR_A if abs(letter) == 1 else GENERATOR_B
        if letter < 0:
            value = inverse_perm(value)
        result = compose(result, value)
    return result


def pair_of(word: list[int]) -> str:
    value = permutation_word(word)
    need(value in PERM_PAIR, "permutation pair lookup")
    return PERM_PAIR[value]


def expected_states() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    gamma_words = [[], [2], [2, 2]]
    q_words = [[], [1]]
    for q0 in range(2):
        for gamma in range(3):
            word = join(gamma_words[gamma], q_words[q0])
            pair = pair_of(word)
            rows.append({
                "id": f"d{gamma}{q0}", "gamma": gamma, "q0": q0,
                "word": word, "value": pair,
                "coordinates": [pair, pair.split(":")[0]],
            })
    return rows


def by_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        need(row["id"] not in result, "duplicate delta id")
        result[row["id"]] = row
    return result


def projection(row: dict[str, Any], indices: tuple[int, ...]) -> tuple[str, ...]:
    return tuple(row["coordinates"][index] for index in indices)


def subset_name(indices: tuple[int, ...]) -> str:
    return ",".join(str(index) for index in indices)


def form_query(states: list[dict[str, Any]], indices: tuple[int, ...]) -> dict[str, Any]:
    gamma = [row for row in states if row["q0"] == 0]
    sections = [row for row in states if row["gamma"] == 0]
    image = sorted({projection(row, indices) for row in gamma})
    section_image = {projection(row, indices) for row in sections}
    d_image = sorted({projection(row, indices) for row in states})
    n = len(states) // len(d_image)
    return {
        "key": subset_name(indices), "indices": list(indices),
        "A": [list(item) for item in image],
        "L_order": sum(1 for row in sections if projection(row, indices) in image),
        "D_order": len(d_image), "kernel_order": n,
        "n_values": [{"a": list(item), "count": n} for item in d_image],
    }


def query_map(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    answer: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = str(row["key"])
        need(key not in answer, "duplicate query key")
        answer[key] = row
    return answer


def n_for(queries: dict[str, dict[str, Any]], fixed: dict[int, str],
          total_states: int) -> int:
    if not fixed:
        return total_states
    indices = tuple(sorted(fixed))
    target = tuple(fixed[index] for index in indices)
    for row in queries[subset_name(indices)]["n_values"]:
        if tuple(row["a"]) == target:
            return int(row["count"])
    return 0


def merge_occurrences(row: dict[str, Any]) -> list[dict[str, Any]]:
    sums: dict[tuple[int, str], int] = {}
    for item in row["raw_occurrences"]:
        key = (int(item["coord"]), str(item["target"]))
        value = int(item["weight"]) % 3
        need(key[0] in (0, 1) and value in (0, 1, 2), "occurrence domain")
        sums[key] = (sums.get(key, 0) + value) % 3
    return [
        {"coord": key[0], "target": key[1], "coefficient": value}
        for key, value in sorted(sums.items()) if value
    ]


def make_patterns(targets: list[list[str]]) -> list[list[str]]:
    patterns: list[list[str]] = [[]]
    for target_list in targets:
        expanded: list[list[str]] = []
        for prefix in patterns:
            expanded.append(prefix + ["*"])
            expanded.extend(prefix + [target] for target in target_list)
        patterns = expanded
    return patterns


def inclusion_count(pattern: list[str], targets: list[list[str]],
                    queries: dict[str, dict[str, Any]], total_states: int,
                    signs: dict[str, int]) -> int:
    fixed = {index: value for index, value in enumerate(pattern) if value != "*"}
    stars = [index for index, value in enumerate(pattern) if value == "*"]
    total = 0
    for mask in range(1 << len(stars)):
        assignments: list[dict[int, str]] = [dict(fixed)]
        included = 0
        for position, coordinate in enumerate(stars):
            if not (mask & (1 << position)):
                continue
            included += 1
            next_assignments: list[dict[int, str]] = []
            for assignment in assignments:
                for target in targets[coordinate]:
                    current = dict(assignment)
                    current[coordinate] = target
                    next_assignments.append(current)
            assignments = next_assignments
        sign = int(signs[str(included)])
        total += sign * sum(n_for(queries, assignment, total_states)
                            for assignment in assignments)
    return total


def weighted_value(row: dict[str, Any], pattern: list[str]) -> int:
    value = int(row["kappa"]) % 3
    for item in merge_occurrences(row):
        if pattern[int(item["coord"])] == item["target"]:
            value += int(item["coefficient"])
    return value % 3


def sparse(rows: list[dict[str, Any]]) -> dict[tuple[int, str, str], int]:
    result: dict[tuple[int, str, str], int] = {}
    for row in rows:
        key = (int(row["block_tag"]), str(row["component"]),
               str(row["element"]))
        value = int(row["coefficient"]) % 3
        need(key[0] in (1, 2, 3), "sparse block tag")
        result[key] = (result.get(key, 0) + value) % 3
    return {key: value for key, value in result.items() if value}


def add(left: dict[tuple[int, str, str], int],
        right: dict[tuple[int, str, str], int], scale: int = 1) -> dict[tuple[int, str, str], int]:
    result = dict(left)
    for key, value in right.items():
        result[key] = (result.get(key, 0) + scale * value) % 3
        if result[key] == 0:
            del result[key]
    return result


def target_from_base(model: dict[str, Any]) -> dict[tuple[int, str, str], int]:
    block_tag = {"H1": 1, "H2": 2, "P": 3}
    result: dict[tuple[int, str, str], int] = {}
    for block, value in model["raw_base_targets"].items():
        key = (block_tag[block], str(value["component"]), str(value["element"]))
        result[key] = (-int(value["coefficient"])) % 3
    return {key: value for key, value in result.items() if value}


def pentagon_value(model: dict[str, Any]) -> Perm:
    result = IDENTITY
    plan = model["pentagon"]
    for index, sign in zip(plan["ordered_indices"], plan["ordered_signs"]):
        value = permutation_word(plan["factor_words"][int(index)])
        if int(sign) < 0:
            value = inverse_perm(value)
        result = compose(result, value)
    return result


def validate_model(model: dict[str, Any]) -> None:
    expected = expected_states()
    actual = model["delta_states"]
    need(len(actual) == len(expected), "delta state count")
    for left, right in zip(actual, expected):
        for field in ("id", "gamma", "q0", "word", "value", "coordinates"):
            need(left[field] == right[field], f"delta {field}")

    left = pair_of(model["noncommutative"]["left_word"])
    right = pair_of(model["noncommutative"]["right_word"])
    need(left == model["noncommutative"]["left_value"], "left noncommutative value")
    need(right == model["noncommutative"]["right_value"], "right noncommutative value")
    need(left != right and model["noncommutative"]["different"] is True,
         "linked noncommutative extension")

    queries = query_map(model["queries"])
    for indices in ((0,), (1,), (0, 1)):
        calculated = form_query(actual, indices)
        supplied = queries[subset_name(indices)]
        for field in ("A", "L_order", "D_order", "kernel_order", "n_values"):
            need(supplied[field] == calculated[field], f"query {field}")

    row = model["weighted_rows"][0]
    merged = merge_occurrences(row)
    need(row["merged"] == merged, "same-target merge")
    targets = [sorted({item["target"] for item in merged if int(item["coord"]) == index})
               for index in range(2)]
    need(targets == [["0:1"], ["1", "2"]], "merged support")
    need(row["include_complement"] is True, "complement flag")
    need(row["ie_sign_table"] == {"0": 1, "1": -1, "2": 1}, "IE sign table")
    cells = {tuple(item["pattern"]): item for item in row["cells"]}
    patterns = make_patterns(targets)
    need(set(cells) == {tuple(item) for item in patterns}, "cell partition")
    for pattern in patterns:
        item = cells[tuple(pattern)]
        count = inclusion_count(pattern, targets, queries, len(actual),
                                row["ie_sign_table"])
        value = weighted_value(row, pattern)
        need(count >= 0 and int(item["count"]) == count, "cell count")
        need(int(item["value"]) == value, "weighted cell value")
        need(bool(item["active"]) == (count > 0 and value != 0), "active cell type")
    need(cells[("*", "*")]["count"] == 1, "all-star cell")

    witness = model["active_witness"]
    state = by_id(actual)[witness["delta_id"]]
    need(witness["pattern"] == ["0:1", "*"], "witness pattern")
    witness_cell = cells[tuple(witness["pattern"])]
    need(witness_cell["active"] is True, "active witness cell")
    need(state["word"] == witness["section_word"], "section provenance")
    need(witness["gamma_word"] == [], "gamma adjustment")
    need(witness["conjugator"] == join(witness["gamma_word"], witness["section_word"]),
         "transversal conjugator")
    source = join(witness["conjugator"], witness["relation_word"],
                  inverse_free(witness["conjugator"]))
    need(witness["source_word"] == source, "source word spelling")
    need(pair_of(witness["relation_word"]) == "0:0", "relation source replay")
    need(pair_of(source) == "0:0", "conjugate source replay")
    exponents = [0, 0]
    for letter in source:
        exponents[0 if abs(letter) == 1 else 1] += 1 if letter > 0 else -1
    need([value % 3 for value in exponents] == [0, 0], "source exponent replay")

    expected_boundary_tags = {"PB3_H1": 1, "PB3_H2": 2, "PB4_P": 3}
    for boundary in model["boundary_columns"]:
        need(int(boundary["block_tag"]) == expected_boundary_tags[boundary["id"]],
             "PB3/PB4 typed tag")
        need(boundary["kind"] == ("PB3" if int(boundary["block_tag"]) in (1, 2) else "PB4"),
             "boundary family type")

    target = target_from_base(model)
    need(sparse(model["target"]["rows"]) == target, "negative base target")
    need(model["target"]["exponents"] == [0, 0], "target exponents")
    column = model["correction_column"]
    need(column["delta_id"] == witness["delta_id"], "column delta")
    need(column["exponents"] == [0, 0], "column exponent coordinates")
    need(sparse(column["rows"]) == target, "correction column target")
    solution = model["solution"]
    need(solution["correction_coefficients"] == {"C0": 1}, "solution coefficient")
    boundary_lookup = {item["id"]: item for item in model["boundary_columns"]}
    total: dict[tuple[int, str, str], int] = {}
    for identifier, coefficient in solution["boundary_coefficients"].items():
        total = add(total, sparse(boundary_lookup[identifier]["rows"]),
                    int(coefficient))
    total = add(total, sparse(column["rows"]), 1)
    need(total == target, "sparse target sum")
    need(solution["correction_word"] == witness["source_word"], "common correction")
    need(normalize(model["g760"] + solution["correction_word"]) ==
         model["corrected_word"], "right correction convention")

    need(pair_of(model["hexagons"]["H1"]) == "0:0", "H1 direct replay")
    need(pair_of(model["hexagons"]["H2"]) == "0:0", "H2 direct replay")
    need(pentagon_value(model) == IDENTITY, "pentagon order/sign replay")


MUTATIONS = [
    "merged_same_target_cancellation", "multi_coordinate_target",
    "inclusion_exclusion_sign", "kernel_order", "complement_all_star",
    "section_gamma_adjustment", "source_word_transversal", "pb3_pb4_block_tag",
    "target_base_defect_coordinate", "exponent_coordinate",
    "final_correction_coefficient", "pentagon_factor_order_sign",
]


def altered(model: dict[str, Any], name: str) -> dict[str, Any]:
    value = copy.deepcopy(model)
    if name == "merged_same_target_cancellation":
        value["weighted_rows"][0]["raw_occurrences"][2]["weight"] = 1
    elif name == "multi_coordinate_target":
        for query in value["queries"]:
            if query["key"] == "0,1":
                query["n_values"][3]["count"] = 0
    elif name == "inclusion_exclusion_sign":
        value["weighted_rows"][0]["ie_sign_table"]["1"] = 1
    elif name == "kernel_order":
        for query in value["queries"]:
            if query["key"] == "1":
                query["kernel_order"] = 1
    elif name == "complement_all_star":
        value["weighted_rows"][0]["include_complement"] = False
    elif name == "section_gamma_adjustment":
        value["active_witness"]["section_word"] = [2]
    elif name == "source_word_transversal":
        value["active_witness"]["conjugator"] = [2]
    elif name == "pb3_pb4_block_tag":
        value["boundary_columns"][0]["block_tag"] = 2
    elif name == "target_base_defect_coordinate":
        value["raw_base_targets"]["H1"]["coefficient"] = 1
    elif name == "exponent_coordinate":
        value["correction_column"]["exponents"][0] = 1
    elif name == "final_correction_coefficient":
        value["solution"]["correction_coefficients"]["C0"] = 2
    elif name == "pentagon_factor_order_sign":
        value["pentagon"]["ordered_signs"][4] = 1
    else:
        raise Reject(f"unknown mutation {name}")
    return value


def run_mutations(model: dict[str, Any]) -> tuple[int, int]:
    rejected = 0
    for name in MUTATIONS:
        try:
            validate_model(altered(model, name))
        except (Reject, KeyError, TypeError, ValueError, IndexError):
            rejected += 1
    return len(MUTATIONS), rejected


def read_fixture(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if FIXTURE_BYTES and FIXTURE_SHA256:
        need((len(raw), digest(raw)) == (FIXTURE_BYTES, FIXTURE_SHA256),
             "fixture pin")
    value = json.loads(raw.decode("ascii"))
    need(value["schema"] == SELFTEST_SCHEMA and
         value["status"] == "SELFTEST" and value["terminal"] == "FIXTURE_PASS",
         "fixture envelope")
    return value


def selftest(path: Path) -> int:
    model = read_fixture(path)["model"]
    validate_model(model)
    attempted, rejected = run_mutations(model)
    need(attempted == 12 and rejected == 12, "mutation coverage")
    print("R07_WEIGHTED_CELL_COLGEN_CHECKER_SELFTEST_PASS "
          "mutations=12 rejected=12 linked_nonabelian_order=6", flush=True)
    return 0


def verify_unknown(receipt: dict[str, Any], raw: bytes) -> None:
    need(receipt["schema"] == SCHEMA, "receipt schema")
    need(receipt["status"] == "UNKNOWN_INPUT" and
         receipt["terminal"] == UNKNOWN_INPUT and
         receipt["reason"] == "PREREQUISITE_NOT_PINNED" and
         receipt["result"] is None, "typed prerequisite unknown")
    need(all(value is False for value in receipt["boundaries"].values()),
         "unknown boundary envelope")
    unsigned = dict(receipt)
    supplied = unsigned.pop("self_digest_sha256", None)
    need(supplied == digest_value(unsigned), "receipt self digest")
    need(len(raw) > 0, "receipt bytes")


def write_verdict(path: Path, receipt_raw: bytes, receipt: dict[str, Any]) -> None:
    result = {
        "schema": SCHEMA + "/checker-v1",
        "status": "PASS",
        "terminal": UNKNOWN_INPUT,
        "receipt_terminal": receipt["terminal"],
        "reason": "PREREQUISITE_NOT_PINNED",
        "producer_receipt_sha256": digest(receipt_raw),
        "all_seven_solution": False,
        "separator": False,
        "cofinal_lift": False,
        "fake": False,
        "Ihara_witness": False,
    }
    result["self_digest_sha256"] = digest_value(result)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(stable(result) + b"\n")


def check_production(receipt_path: Path, verdict_path: Path) -> int:
    raw = receipt_path.read_bytes()
    receipt = json.loads(raw.decode("ascii"))
    verify_unknown(receipt, raw)
    write_verdict(verdict_path, raw, receipt)
    print(f"R07_WEIGHTED_CELL_COLGEN_CHECKER_PASS terminal={receipt['terminal']}",
          flush=True)
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    mode = result.add_mutually_exclusive_group(required=True)
    mode.add_argument("--selftest", action="store_true")
    mode.add_argument("--check", action="store_true")
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
    return check_production(Path(args.receipt), Path(args.verdict))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, OSError, ValueError, KeyError, TypeError,
            json.JSONDecodeError) as exc:
        print(f"R07_WEIGHTED_CELL_COLGEN_CHECKER_STOP {exc}",
              file=sys.stderr, flush=True)
        raise SystemExit(1)
