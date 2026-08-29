#!/usr/bin/env python3
"""Independent checker for the A4 legal relative-source extractor v1.

The new producer is authenticated as inert source bytes and is never
imported.  Frozen checker arithmetic, reverse Gamma scans, reverse word
action, and a latest-pivot echelon provide the independent routes.
"""
from __future__ import annotations

import argparse
import ast
import base64
import hashlib
import json
import os
import struct
import tempfile
import zlib
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-a4-legal-source-extractor/v1/crosscheck/v1"
PRODUCER_SCHEMA = "d972-r07-a4-legal-source-extractor/v1"
A4_SCHEMA = "d972-r07-word-independent-successor-kernel/v6"
A4_PASS = "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS"
PASS = "A4_LEGAL_RELATIVE_SOURCE_COMPLETE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
PREFIX = "R07_A4_LEGAL_SOURCE_EXTRACTOR_V1_CHECKER_TERMINAL"
NO_A4_REASON = "UNKNOWN_INPUT:A4_POSITIVE_AMBIENT_K_NOT_AVAILABLE"

MAX_A4_BYTES = 2_000_000_000
MAX_PRODUCER_BYTES = 2_000_000_000
MAX_OUTPUT_BYTES = 2_000_000_000
MAX_GAMMA_RAW_BYTES = 1_000_000
MAX_K_RANK = 200_000
MAX_LITERAL_LETTERS = 20_000_000

PINS: dict[str, tuple[str, int, str]] = {
    "new_producer": (
        "search/d972_r07_a4_legal_source_extractor_v1.py", 45551,
        "e0a70e81e8ebad95e95bd30784b3150b4e06608236d22d00569cde1c17a0a885"),
    "a4_producer_v12": (
        "search/d972_r07_word_independent_successor_kernel_v12.py", 7209,
        "816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5"),
    "a4_checker_v14": (
        "crosscheck/check_d972_r07_word_independent_successor_kernel_v14.py", 8074,
        "7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47"),
    "a4_checker_base_v6": (
        "crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py", 258847,
        "432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf"),
    "e4_arithmetic": (
        "search/d972_b345_seedspan_triple4_v1.py", 535219,
        "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
    "q3_receipt": (
        "ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570,
        "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "task157ee_receipt": (
        "ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json",
        2166036,
        "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    "task157ee_producer": (
        "search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945,
        "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    "task157ee_checker": (
        "search/check_d972_b345_joint_kernel_qstar_closure_v2.py", 5942,
        "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88"),
    "task157ee_driver": (
        "search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g", 3912,
        "8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7"),
}


class Reject(Exception):
    pass


class ResourceStop(Exception):
    pass


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise Reject(reason)


def resource(condition: bool, reason: str) -> None:
    if not condition:
        raise ResourceStop(reason)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def object_hash(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def bytes_hash(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def pinned(path: Path, expected: tuple[str, int, str], label: str) -> bytes:
    require(path.is_file() and not path.is_symlink(), label + ":regular")
    raw = path.read_bytes()
    require(len(raw) == expected[1] and bytes_hash(raw) == expected[2], label + ":pin")
    return raw


def json_object(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ":ascii_json") from exc
    require(isinstance(value, dict) and raw in (canonical(value), canonical(value) + b"\n"),
            label + ":canonical_json")
    return value


def check_seal(value: dict[str, Any], label: str) -> None:
    body = dict(value)
    claimed = body.pop("self_digest_sha256", None)
    require(isinstance(claimed, str) and claimed == object_hash(body), label + ":seal")


def input_path(text: str, label: str) -> Path:
    result = (ROOT / text).resolve()
    base = (ROOT / "ci" / "in").resolve()
    require(result.parent == base and result.name == Path(text).name, label + ":ci_in")
    return result


def producer_path(text: str) -> Path:
    result = (ROOT / text).resolve()
    base = (ROOT / "ci" / "out").resolve()
    require(result.parent == base and result.name == Path(text).name, "producer:ci_out")
    return result


def output_path(text: str) -> Path:
    result = (ROOT / text).resolve()
    base = (ROOT / "ci" / "out").resolve()
    require(result.parent == base and result.name == Path(text).name, "output:ci_out")
    return result


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(value) for value in word[::-1]]


def reduced_word(*parts: Sequence[int]) -> list[int]:
    stack: list[int] = []
    for raw in (letter for part in parts for letter in part):
        letter = int(raw)
        require(letter in (-2, -1, 1, 2), "word:letter")
        if stack and stack[-1] + letter == 0:
            stack.pop()
        else:
            stack.append(letter)
    resource(len(stack) <= MAX_LITERAL_LETTERS, "literal_letter_cap")
    return stack


def abelianization(word: Sequence[int]) -> list[int]:
    result = [0, 0]
    for letter in word:
        result[abs(int(letter)) - 1] += 1 if letter > 0 else -1
    return result


def sparse_add(left: dict[str, int], right: dict[str, int], scalar: int = 1) -> dict[str, int]:
    answer = dict(left)
    for key, raw in right.items():
        value = (answer.get(key, 0) + int(scalar) * int(raw)) % 3
        if value:
            answer[key] = value
        else:
            answer.pop(key, None)
    return answer


def sparse_scale(value: dict[str, int], scalar: int) -> dict[str, int]:
    return {key: int(raw) * int(scalar) % 3 for key, raw in value.items()
            if int(raw) * int(scalar) % 3}


def sum_rows(coefficients: dict[str, int], rows: dict[str, dict[str, int]]) -> dict[str, int]:
    result: dict[str, int] = {}
    for label in sorted(coefficients, reverse=True):
        require(label in rows, "fine_sum:label")
        result = sparse_add(result, rows[label], coefficients[label])
    return result


def parse_column(raw: Any, labels: set[str], label: str) -> dict[str, int]:
    require(isinstance(raw, dict) and set(raw) <= labels, label + ":support")
    require(all(type(value) is int and value in (1, 2) for value in raw.values()),
            label + ":coefficient")
    return {str(key): int(value) for key, value in raw.items()}


def apply_matrix(matrix: dict[str, dict[str, int]], vector: dict[str, int]) -> dict[str, int]:
    result: dict[str, int] = {}
    for source, coefficient in vector.items():
        for target, value in matrix[source].items():
            result[target] = (result.get(target, 0) + int(coefficient) * int(value)) % 3
            if result[target] == 0:
                result.pop(target)
    return result


def matrix_on_word_reverse(word: Sequence[int], source: str,
                           matrices: dict[str, dict[str, dict[str, int]]]) -> dict[str, int]:
    vector = {source: 1}
    for letter in reversed(word):
        vector = apply_matrix(matrices[str(int(letter))], vector)
    return vector


def validate_a4(producer: dict[str, Any], verdict: dict[str, Any]) -> tuple[
        list[str], dict[str, dict[str, dict[str, int]]]]:
    check_seal(producer, "a4.producer")
    check_seal(verdict, "a4.verdict")
    for value, name in ((producer, "producer"), (verdict, "verdict")):
        require(value.get("schema") == A4_SCHEMA and value.get("status") == "COMPLETE" and
                value.get("terminal") == A4_PASS and value.get("complete") is True and
                value.get("A4_presentation_input") == 1 and
                value.get("A4_invariant_closure") == 1 and
                value.get("A4_word_bearing_K") == 1, "a4:" + name + ":positive")
    require(verdict.get("accepted") is True and verdict.get("independent") is True,
            "a4:independent_verdict")
    pk, ck = producer.get("kernel"), verdict.get("kernel")
    require(isinstance(pk, dict) and isinstance(ck, dict) and pk.get("complete") is True and
            ck.get("complete") is True, "a4:kernel_complete")
    proster, croster = pk.get("K_roster"), ck.get("K_roster")
    require(isinstance(proster, list) and proster == croster and
            0 < len(proster) <= MAX_K_RANK, "a4:K_roster_two_way")
    labels: list[str] = []
    for item in proster:
        require(isinstance(item, dict) and isinstance(item.get("label"), str) and
                item["label"] not in labels and item.get("strict_rank_rise") is True and
                isinstance(item.get("ancestry"), dict), "a4:K_item")
        word, fine = item.get("word"), item.get("rho1_actual_flattened")
        require(isinstance(word, list) and all(type(x) is int and x in (-2, -1, 1, 2) for x in word),
                "a4:K_word")
        resource(len(word) <= MAX_LITERAL_LETTERS, "K_literal_letter_cap")
        require(isinstance(fine, dict) and all(type(x) is int and x in (1, 2) for x in fine.values()),
                "a4:K_fine")
        labels.append(item["label"])
    label_set = set(labels)
    matrices: dict[str, dict[str, dict[str, int]]] = {}
    require(pk.get("action_matrices") == ck.get("action_matrices"), "a4:action_two_way")
    for letter in ("-2", "2", "-1", "1"):
        raw = pk["action_matrices"].get(letter)
        require(isinstance(raw, dict) and set(raw) == label_set, "a4:action_columns")
        matrices[letter] = {source: parse_column(raw[source], label_set, "a4:action:" + letter)
                            for source in labels}
    for source in labels:
        require(apply_matrix(matrices["-1"], apply_matrix(matrices["1"], {source: 1})) == {source: 1} and
                apply_matrix(matrices["1"], apply_matrix(matrices["-1"], {source: 1})) == {source: 1} and
                apply_matrix(matrices["-2"], apply_matrix(matrices["2"], {source: 1})) == {source: 1} and
                apply_matrix(matrices["2"], apply_matrix(matrices["-2"], {source: 1})) == {source: 1},
                "a4:inverse_action")
    require(pk.get("inverse_laws") == ck.get("inverse_laws") ==
            {"1-1": True, "-11": True, "2-2": True, "-22": True},
            "a4:inverse_owner")
    require(pk.get("queue") == ck.get("queue") ==
            {"accepted": len(labels), "cursor": len(labels), "next": len(labels)},
            "a4:queue_exhaustion")
    require(isinstance(pk.get("actions"), list) and len(pk["actions"]) == 4 * len(labels) and
            isinstance(ck.get("actions"), list) and len(ck["actions"]) == 4 * len(labels),
            "a4:action_events")
    require(producer.get("authority") == verdict.get("authority") and
            producer.get("authority", {}).get("receipt_sha256") ==
            "82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5" and
            producer.get("authority", {}).get("task176", {}).get("receipt", {}).get("sha256") ==
            "715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41",
            "a4:typed_roof_square")
    return labels, matrices


def restore_v14() -> dict[str, Any]:
    wrapper_pin = PINS["a4_checker_v14"]
    path = ROOT / wrapper_pin[0]
    raw = pinned(path, wrapper_pin, "a4.checker_v14")
    pinned(ROOT / PINS["a4_producer_v12"][0], PINS["a4_producer_v12"], "a4.producer_v12")
    wrapper: dict[str, Any] = {"__name__": "d382_v14_wrapper", "__file__": str(path),
                               "__package__": None}
    exec(compile(raw, str(path), "exec"), wrapper, wrapper)
    source = Path(wrapper["SOURCE"])
    base_pin = PINS["a4_checker_base_v6"]
    require(source.resolve() == (ROOT / base_pin[0]).resolve(), "a4.checker_wrapper:source")
    patched = pinned(source, base_pin, "a4.checker_base_v6")
    for old, new in wrapper["PATCHES"]:
        require(patched.count(old) == 1, "a4.checker_wrapper:patch_site")
        patched = patched.replace(old, new)
    owner: dict[str, Any] = {"__name__": "d382_frozen_v14_owner",
                             "__file__": str(source), "__package__": None}
    exec(compile(patched, str(source), "exec"), owner, owner)
    return owner


def instantiate_checker(owner: dict[str, Any]) -> tuple[Any, Any, Any]:
    require(tuple(owner["E4_SOURCE"]) == PINS["e4_arithmetic"] and
            tuple(owner["Q3_SOURCE"]) == PINS["q3_receipt"],
            "a4:frozen_checker_arithmetic_pin_constants")
    args = SimpleNamespace(**{"task198_" + key: "ci/in/" + value
                              for key, value in owner["AUTH"].items()})
    meter = owner["Meter"](dict(owner["CAPS"]))
    authority = owner["Authority"](args, meter)
    arithmetic = owner["CheckerArithmetic"](authority, meter)
    return authority, arithmetic, meter


def factor_words() -> tuple[list[list[int]], list[list[int]], dict[str, Any]]:
    source = pinned(ROOT / PINS["task157ee_producer"][0], PINS["task157ee_producer"],
                    "task157ee.producer")
    for name in ("task157ee_checker", "task157ee_driver"):
        pinned(ROOT / PINS[name][0], PINS[name], "task157ee." + name)
    try:
        tree = ast.parse(source.decode("ascii"))
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject("task157ee:source_ast") from exc
    assignments: dict[str, Any] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in {"P_RELATORS", "SPLIT_WORDS"}:
                assignments[name] = ast.literal_eval(node.value)
    require(set(assignments) == {"P_RELATORS", "SPLIT_WORDS"}, "task157ee:literals")
    relators, split = assignments["P_RELATORS"], assignments["SPLIT_WORDS"]
    require(len(relators) == 5 and len(split) == 4 and all(
        isinstance(word, list) and word and all(type(x) is int and x in (-2, -1, 1, 2) for x in word)
        for word in relators + split), "task157ee:literal_shape")
    receipt = json_object(pinned(ROOT / PINS["task157ee_receipt"][0],
                                 PINS["task157ee_receipt"], "task157ee.receipt"),
                          "task157ee.receipt")
    q0 = receipt.get("q0_presentation", {})
    require(receipt.get("terminal_token") == "B345_JOINT_KERNEL_QSTAR_CLOSED" and
            q0.get("P_order") == 504 and q0.get("Q0_order") == 1469664 and
            q0.get("P_relator_count") == len(relators) and
            q0.get("split_word_lengths") == list(map(len, split)) and
            q0.get("split_word_sha256") == object_hash(split) ==
            "e016a4762e8e89e6dcdb7f63d9c39426245af6e9fa5eb94f980106561e103622",
            "task157ee:factor_owner")
    return split, relators, q0


def strict_unpack(owner: Any, width: int, count: int, label: str) -> bytes:
    require(isinstance(owner, dict) and owner.get("codec") == "zlib+base64" and
            owner.get("record_width_bytes") == width and owner.get("record_count") == count and
            owner.get("raw_bytes") == width * count <= MAX_GAMMA_RAW_BYTES,
            label + ":envelope")
    try:
        compressed = base64.b64decode(owner.get("data", ""), validate=True)
    except Exception as exc:
        raise Reject(label + ":base64") from exc
    require(len(compressed) == owner.get("compressed_bytes") and
            bytes_hash(compressed) == owner.get("compressed_sha256"), label + ":compressed")
    decoder = zlib.decompressobj()
    raw = decoder.decompress(compressed, width * count + 1) + decoder.flush()
    require(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail and
            len(raw) == width * count and bytes_hash(raw) == owner.get("raw_sha256"),
            label + ":raw")
    return raw


def split_value(raw: bytes, coordinate: int) -> tuple[bytes, bytes]:
    degree = 36 if coordinate < 5 else 144
    expected = 40 if coordinate < 5 else 154
    require(len(raw) == expected and set(raw[:degree]) == set(range(degree)),
            "Gamma:value_blob")
    return raw[:degree], raw[degree:]


def blob(value: Any) -> bytes:
    require(isinstance(value, tuple) and len(value) == 2 and
            all(isinstance(part, bytes) for part in value), "roof:value")
    return value[0] + value[1]


class ProductRoof:
    def __init__(self, arithmetic: Any):
        self.groups = [arithmetic.quotient(index) for index in range(10)]
        self.one = tuple(group.identity for group in self.groups)

    def product(self, left: Sequence[Any], right: Sequence[Any]) -> tuple[Any, ...]:
        require(len(left) == len(right) == 10, "roof:width")
        return tuple(group.mul(a, b) for group, a, b in zip(self.groups, left, right))

    def inv(self, value: Sequence[Any]) -> tuple[Any, ...]:
        return tuple(group.inverse(item) for group, item in zip(self.groups, value))

    def conjugate(self, outer: Sequence[Any], inner: Sequence[Any]) -> tuple[Any, ...]:
        return self.product(self.product(outer, inner), self.inv(outer))

    def key(self, value: Sequence[Any]) -> tuple[bytes, ...]:
        return tuple(blob(item) for item in value)

    def display(self, value: Sequence[Any]) -> list[str]:
        return [item.hex() for item in self.key(value)]

    def evaluate(self, relator: Sequence[int], generators: Sequence[Sequence[Any]]) -> tuple[Any, ...]:
        inverses = [self.inv(value) for value in generators]
        current = self.one
        for raw in relator:
            index = abs(int(raw)) - 1
            require(0 <= index < len(generators), "relator:letter")
            current = self.product(current, generators[index] if raw > 0 else inverses[index])
        return current


def inverse_permutation(value: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0] * len(value)
    for source, target in enumerate(value, 1):
        answer[target - 1] = source
    return tuple(answer)


def pointwise_word_map(word: Sequence[int], generators: Sequence[tuple[int, ...]]) -> tuple[int, ...]:
    signed = {index + 1: value for index, value in enumerate(generators)}
    signed.update({-index - 1: inverse_permutation(value)
                   for index, value in enumerate(generators)})
    answer = []
    for source in range(1, len(generators[0]) + 1):
        image = source
        for letter in reversed(word):
            image = signed[int(letter)][image - 1]
        answer.append(image)
    return tuple(answer)


def independent_projection(q3: dict[str, Any], split_words: list[list[int]],
                           relators: list[list[int]], final_words: list[list[int]]) -> dict[str, Any]:
    marked = q3.get("coarse_models", {}).get("Q0", {}).get("marked_permutations")
    require(isinstance(marked, list) and len(marked) == 2 and
            all(isinstance(row, list) and len(row) == 36 for row in marked),
            "v360:Q0_projection_owner")
    qgens = [tuple(int(value) for value in row) for row in marked]
    pgens = [tuple(row[:9]) for row in qgens]
    ggens = [tuple(value - 9 for value in row[9:]) for row in qgens]
    pid, gid = tuple(range(1, 10)), tuple(range(1, 28))
    targets = [(pgens[0], gid), (pgens[1], gid), (pid, ggens[0]), (pid, ggens[1])]
    split_images = [(pointwise_word_map(word, pgens), pointwise_word_map(word, ggens))
                    for word in split_words]
    require(split_images == targets and all(pointwise_word_map(row, pgens) == pid
                                             for row in relators),
            "v360:split_projection_replay")
    final = [(pointwise_word_map(word, pgens), pointwise_word_map(word, ggens))
             for word in final_words]
    require(final == targets[:2], "v360:final_projection_replay")
    return {"Q0_order": 1469664, "P_order": 504, "G9_order": 2916,
            "all_four_split_factor_images_replayed": True,
            "final_generators_project_to_fixed_P_generators": True,
            "final_projection_sha256": object_hash(final)}


def reconstruct_gamma(receipt: dict[str, Any], arithmetic: Any, roof: ProductRoof) -> dict[str, Any]:
    result = receipt.get("result", {})
    gamma = result.get("Gamma", {})
    require(result.get("extension", {}).get("Gamma_order") == 243 and
            result.get("extension", {}).get("Q0_order") == 1469664 and
            gamma.get("order") == 243, "task176:extension")
    words = gamma.get("record_words")
    require(isinstance(words, list) and len(words) == 26 and all(
        isinstance(word, list) and word and all(type(x) is int and x in (-2, -1, 1, 2) for x in word)
        for word in words), "Gamma:record_words")
    widths = [40] * 5 + [154] * 5
    packed_states = strict_unpack(gamma.get("ten_coordinate_states"), sum(widths), 243,
                                  "Gamma.states")
    packed_parents = strict_unpack(gamma.get("section_parent_states_u16le"), 2, 243,
                                   "Gamma.parents")
    packed_records = strict_unpack(gamma.get("section_parent_record_u8"), 1, 243,
                                   "Gamma.records")
    states: list[tuple[Any, ...]] = []
    cursor = 0
    for _ in range(243):
        row = []
        for coordinate, width in enumerate(widths):
            row.append(split_value(packed_states[cursor:cursor + width], coordinate))
            cursor += width
        states.append(tuple(row))
    parents = [struct.unpack_from("<H", packed_parents, 2 * index)[0] for index in range(243)]
    record_ids = list(packed_records)
    require(parents[0] == record_ids[0] == 0 and roof.key(states[0]) == roof.key(roof.one),
            "Gamma:root")
    record_values = [tuple(arithmetic.direct(word, coordinate).a for coordinate in range(10))
                     for word in reversed(words)]
    reverse_to_original = list(reversed(range(26)))
    original_values = {index: value for index, value in zip(reverse_to_original, record_values)}
    source_words: list[list[int]] = [[]]
    for index in range(1, 243):
        parent, record = parents[index] - 1, record_ids[index] - 1
        require(0 <= parent < index and record in original_values, "Gamma:parent")
        require(roof.key(roof.product(states[parent], original_values[record])) == roof.key(states[index]),
                "Gamma:edge_replay")
        source_words.append(reduced_word(source_words[parent], words[record]))
    require(len({roof.key(value) for value in states}) == 243, "Gamma:unique")
    for index in (242, 9, 6, 3, 2, 1):
        replay = tuple(arithmetic.direct(source_words[index], coordinate).a for coordinate in range(10))
        require(roof.key(replay) == roof.key(states[index]), "Gamma:literal_canary")
    return {"states": states, "words": source_words,
            "record_values": [original_values[index] for index in reversed(range(26))],
            "record_words": [words[index] for index in reversed(range(26))],
            "raw_sha256": gamma["ten_coordinate_states"]["raw_sha256"],
            "parent_sha256": object_hash({"parents": parents, "records": record_ids})}


def independent_residual(arithmetic: Any, task176: dict[str, Any],
                         split_words: list[list[int]], relators: list[list[int]]) -> dict[str, Any]:
    roof = ProductRoof(arithmetic)
    gamma = reconstruct_gamma(task176, arithmetic, roof)
    states = gamma["states"]
    gamma_words = gamma["words"]
    generators = gamma["record_values"]
    p_values = [tuple(arithmetic.direct(word, coordinate).a for coordinate in range(10))
                for word in split_words[:2]]
    solution_lists: list[list[int]] = []
    for p_value in p_values:
        target = [roof.key(roof.conjugate(p_value, value)) for value in generators]
        candidates = []
        for index in reversed(range(243)):
            if all(roof.key(roof.conjugate(states[index], value)) == wanted
                   for value, wanted in zip(generators, target)):
                candidates.append(index)
        require(len(candidates) == 27, "v360:inner_coset")
        chosen = states[candidates[0]]
        require(all(roof.key(roof.conjugate(p_value, value)) ==
                    roof.key(roof.conjugate(chosen, value)) for value in reversed(states)),
                "v360:inner_full_replay")
        solution_lists.append(candidates)
    centers = [index for index in reversed(range(243)) if all(
        roof.key(roof.product(states[index], generator)) ==
        roof.key(roof.product(generator, states[index])) for generator in generators)]
    require(len(centers) == 27 and all(all(
        roof.key(roof.product(states[index], value)) == roof.key(roof.product(value, states[index]))
        for value in reversed(states)) for index in centers), "v360:center_27")
    c_values, c_words = [], []
    for p_value, p_word, candidates in zip(p_values, split_words[:2], solution_lists):
        selected = candidates[0]
        c_values.append(roof.product(roof.inv(states[selected]), p_value))
        c_words.append(reduced_word(inverse_word(gamma_words[selected]), p_word))
    passing = []
    for left in centers:
        for right in centers:
            pair = (roof.product(states[left], c_values[0]),
                    roof.product(states[right], c_values[1]))
            if all(roof.key(roof.evaluate(relator, pair)) == roof.key(roof.one)
                   for relator in reversed(relators)):
                passing.append((left, right, pair))
    require(len(passing) == 1, "v360:unique_729_pair")
    left, right, values = passing[0]
    final_words = [reduced_word(gamma_words[left], c_words[0]),
                   reduced_word(gamma_words[right], c_words[1])]
    for word, value in zip(final_words, values):
        replay = tuple(arithmetic.direct(word, coordinate).a for coordinate in range(10))
        require(roof.key(replay) == roof.key(value), "v360:literal_replay")
    signed = [values[1], values[0], roof.inv(values[1]), roof.inv(values[0])]
    known = {roof.key(roof.one): roof.one}
    queue = [roof.one]
    while queue:
        current = queue.pop()
        for generator in signed:
            nxt = roof.product(current, generator)
            key = roof.key(nxt)
            if key not in known:
                known[key] = nxt
                queue.append(nxt)
                require(len(known) <= 504, "v360:subgroup_cap")
    require(len(known) == 504 and
            set(known).intersection({roof.key(value) for value in states}) == {roof.key(roof.one)},
            "v360:complement_order_and_intersection")
    projection = independent_projection(arithmetic.q3, split_words, relators, final_words)
    return {"roof": roof, "words": final_words, "values": list(values),
            "inner_counts": [len(value) for value in solution_lists],
            "center_order": len(centers), "passing": len(passing),
            "projection": projection,
            "raw_sha256": gamma["raw_sha256"], "parent_sha256": gamma["parent_sha256"]}


def read_new_producer(path: Path) -> tuple[bytes, dict[str, Any]]:
    require(path.is_file() and not path.is_symlink(), "producer:regular")
    size = path.stat().st_size
    resource(0 < size <= MAX_PRODUCER_BYTES, "producer_byte_cap")
    raw = path.read_bytes()
    require(len(raw) == size, "producer:stable_read")
    value = json_object(raw, "producer")
    check_seal(value, "producer")
    return raw, value


def compare_residual(receipt: dict[str, Any], independent: dict[str, Any],
                     arithmetic: Any) -> list[list[int]]:
    public = receipt.get("canonical_residual_action")
    require(isinstance(public, dict) and public.get("Gamma_order") == 243 and
            public.get("Gamma_record_count") == 26 and
            public.get("Gamma_table_raw_sha256") == independent["raw_sha256"] and
            public.get("Gamma_parent_recurrence_sha256") == independent["parent_sha256"] and
            public.get("inner_solution_counts") == [27, 27] and
            public.get("center_order") == 27 and public.get("central_pairs_exhausted") == 729 and
            public.get("complete_PSL_relator_count") == 5 and
            public.get("passing_central_pairs") == 1 and
            public.get("subgroup_order") == 504 and public.get("Gamma_intersection_order") == 1,
            "producer:residual_summary")
    require(public.get("Q0_projection_replay") == independent["projection"],
            "producer:Q0_projection_replay")
    producer_generators = public.get("generators")
    require(isinstance(producer_generators, list) and len(producer_generators) == 2,
            "producer:residual_generators")
    producer_words = []
    for index, item in enumerate(producer_generators):
        require(isinstance(item, dict) and item.get("id") == "s" + str(index + 1) and
                isinstance(item.get("word"), list) and
                item.get("word_sha256") == object_hash(item["word"]),
                "producer:residual_word")
        word = reduced_word(item["word"])
        require(word == item["word"], "producer:residual_word_reduced")
        values = tuple(arithmetic.direct(word, coordinate).a for coordinate in range(10))
        require(independent["roof"].key(values) == independent["roof"].key(independent["values"][index]) and
                item.get("value_hex") == independent["roof"].display(values),
                "producer:canonical_residual_value")
        producer_words.append(word)
    return producer_words


def direct_word(arithmetic: Any, word: Sequence[int]) -> list[Any]:
    return [arithmetic.direct(word, coordinate) for coordinate in range(10)]


def direct_row(arithmetic: Any, word: Sequence[int]) -> tuple[dict[str, int], bool]:
    states = direct_word(arithmetic, word)
    coarse = all(state.identity_roof() for state in states)
    return arithmetic.row(states) if coarse else {}, coarse


def reduce_latest(value: dict[str, int], labels: list[str],
                  rows: dict[int, dict[str, int]]) -> dict[str, int]:
    remainder = dict(value)
    for pivot in sorted(rows, reverse=True):
        coefficient = remainder.get(labels[pivot], 0)
        if coefficient:
            remainder = sparse_add(remainder, rows[pivot], -coefficient)
    return remainder


def insert_latest(raw: dict[str, int], labels: list[str],
                  rows: dict[int, dict[str, int]]) -> bool:
    remainder = reduce_latest(raw, labels, rows)
    if not remainder:
        return False
    pivot = next(index for index in reversed(range(len(labels))) if remainder.get(labels[index], 0))
    rows[pivot] = sparse_scale(remainder, 1 if remainder[labels[pivot]] == 1 else 2)
    return True


def reduce_earliest_with_trace(raw: dict[str, int], seed_id: str, labels: list[str],
                               rows: dict[int, dict[str, int]],
                               formals: dict[int, dict[str, int]]) -> dict[str, Any]:
    remainder, formal, trace = dict(raw), {seed_id: 1}, []
    for pivot in sorted(rows):
        coefficient = remainder.get(labels[pivot], 0)
        if coefficient:
            remainder = sparse_add(remainder, rows[pivot], -coefficient)
            formal = sparse_add(formal, formals[pivot], -coefficient)
            trace.append({"pivot": labels[pivot], "coefficient": coefficient})
    if not remainder:
        return {"rank_rise": False}
    pivot = next(index for index, label in enumerate(labels) if remainder.get(label, 0))
    scale = 1 if remainder[labels[pivot]] == 1 else 2
    rows[pivot] = sparse_scale(remainder, scale)
    formals[pivot] = sparse_scale(formal, scale)
    return {"rank_rise": True, "pivot_index": pivot, "pivot": labels[pivot],
            "normalization_scale": scale, "echelon_row": rows[pivot],
            "change_of_basis": formals[pivot], "reduction_trace": trace}


def check_c_rel(receipt: dict[str, Any], a4: dict[str, Any], labels: list[str],
                matrices: dict[str, dict[str, dict[str, int]]], residual: dict[str, Any],
                producer_words: list[list[int]], arithmetic: Any) -> dict[str, Any]:
    c_rel = receipt.get("C_rel")
    require(isinstance(c_rel, dict) and
            c_rel.get("formula") == "C_rel=R_S(Delta1) intersect K=[R_S(Delta0),K]" and
            c_rel.get("ambient_K_dimension") == len(labels) and
            c_rel.get("ambient_K_labels") == labels and
            c_rel.get("block_count") == 2 * len(labels) and
            c_rel.get("commutator_convention") == "[s,u]=s*u*s^-1*u^-1" and
            c_rel.get("extra_side_gate_intersection") is False,
            "producer:C_rel_header")
    roster = a4["kernel"]["K_roster"]
    k_words = {item["label"]: list(item["word"]) for item in roster}
    k_fine = {item["label"]: {str(key): int(value) for key, value in
                              item["rho1_actual_flattened"].items()} for item in roster}
    producer_blocks = c_rel.get("block_columns")
    require(isinstance(producer_blocks, list) and len(producer_blocks) == 2 * len(labels),
            "producer:block_columns")
    by_id = {item.get("seed_id"): item for item in producer_blocks if isinstance(item, dict)}
    require(len(by_id) == len(producer_blocks), "producer:block_ids")
    independent_blocks: dict[str, dict[str, int]] = {}
    latest_rows: dict[int, dict[str, int]] = {}
    for generator_index in (2, 1):
        s_word = residual["words"][generator_index - 1]
        for basis_index in reversed(range(len(labels))):
            label = labels[basis_index]
            seed_id = "s" + str(generator_index) + ":" + label
            action_column = matrix_on_word_reverse(s_word, label, matrices)
            seed = sparse_add(action_column, {label: 1}, -1)
            independent_blocks[seed_id] = seed
            insert_latest(seed, labels, latest_rows)
            commutator = reduced_word(s_word, k_words[label], inverse_word(s_word),
                                      inverse_word(k_words[label]))
            row, coarse = direct_row(arithmetic, commutator)
            require(coarse and abelianization(commutator) == [0, 0] and
                    row == sum_rows(seed, k_fine), "checker:independent_literal_commutator")
    require(set(by_id) == set(independent_blocks), "producer:block_roster")
    earliest_rows: dict[int, dict[str, int]] = {}
    earliest_formals: dict[int, dict[str, int]] = {}
    selected = []
    expected_order = ["s" + str(g) + ":" + label for g in (1, 2) for label in labels]
    for seed_id in expected_order:
        item = by_id[seed_id]
        seed = independent_blocks[seed_id]
        generator_index = int(seed_id[1])
        label = seed_id.split(":", 1)[1]
        source_word = reduced_word(producer_words[generator_index - 1], k_words[label],
                                   inverse_word(producer_words[generator_index - 1]),
                                   inverse_word(k_words[label]))
        conjugate_word = reduced_word(producer_words[generator_index - 1], k_words[label],
                                      inverse_word(producer_words[generator_index - 1]))
        conjugate_row, conjugate_coarse = direct_row(arithmetic, conjugate_word)
        commutator_row, commutator_coarse = direct_row(arithmetic, source_word)
        conjugate_vector = matrix_on_word_reverse(producer_words[generator_index - 1], label, matrices)
        require(item.get("full_K_vector") == seed and item.get("conjugate_K_vector") == conjugate_vector and
                conjugate_coarse and commutator_coarse and
                conjugate_row == sum_rows(conjugate_vector, k_fine) and
                commutator_row == sum_rows(seed, k_fine) and
                item.get("literal_commutator_word_sha256") == object_hash(source_word) and
                item.get("conjugate_fine_value_sha256") == object_hash(conjugate_row) and
                item.get("commutator_fine_value_sha256") == object_hash(commutator_row) and
                item.get("integer_exponent_sums") == [0, 0] and
                abelianization(source_word) == [0, 0] and item.get("coarse_identity") is True,
                "producer:block_literal_replay")
        detail = reduce_earliest_with_trace(seed, seed_id, labels, earliest_rows, earliest_formals)
        require(item.get("rank_rise") is detail["rank_rise"], "producer:block_rank_rise")
        if detail["rank_rise"]:
            selected.append((seed_id, source_word, commutator_row, detail))
    producer_basis = c_rel.get("basis")
    require(isinstance(producer_basis, list) and len(producer_basis) == len(selected) ==
            c_rel.get("rank"), "producer:basis_rank")
    for item, (seed_id, source_word, fine, detail) in zip(producer_basis, selected):
        label = seed_id.split(":", 1)[1]
        gid = seed_id.split(":", 1)[0]
        require(item.get("seed_id") == seed_id and item.get("literal_commutator_word") == source_word and
                item.get("direct_fine_value") == fine and
                item.get("literal_commutator_ancestry") == [[gid, label, 1]] and
                item.get("pivot") == detail["pivot"] and
                item.get("pivot_index") == detail["pivot_index"] and
                item.get("normalization_scale") == detail["normalization_scale"] and
                item.get("echelon_row") == detail["echelon_row"] and
                item.get("change_of_basis") == detail["change_of_basis"] and
                item.get("reduction_trace") == detail["reduction_trace"] and
                item.get("formation_ancestry", {}).get("not_claimed") ==
                "identity with the displayed literal commutator",
                "producer:basis_ancestry_pivot")
    producer_echelon = c_rel.get("echelon")
    expected_echelon = [{"pivot_index": pivot, "pivot": labels[pivot], "row": earliest_rows[pivot],
                         "change_of_basis": earliest_formals[pivot]} for pivot in sorted(earliest_rows)]
    require(producer_echelon == expected_echelon and
            c_rel.get("final_span_coordinates") == [item["row"] for item in expected_echelon] and
            c_rel.get("rank_proof_sha256") == object_hash(
                {"blocks": producer_blocks, "echelon": expected_echelon}),
            "producer:echelon_certificate")
    for row in earliest_rows.values():
        require(not reduce_latest(row, labels, latest_rows), "span:producer_to_checker")
    producer_rows = {item["pivot_index"]: item["row"] for item in expected_echelon}
    for row in latest_rows.values():
        remainder = dict(row)
        for pivot in sorted(producer_rows):
            coefficient = remainder.get(labels[pivot], 0)
            if coefficient:
                remainder = sparse_add(remainder, producer_rows[pivot], -coefficient)
        require(not remainder, "span:checker_to_producer")
    require(len(latest_rows) == len(earliest_rows), "span:rank_equality")
    return {"rank": len(latest_rows),
            "latest_pivots": [labels[index] for index in sorted(latest_rows, reverse=True)],
            "two_way_span_equality": True, "all_literal_commutators_replayed": True}


def sealed(value: dict[str, Any]) -> bytes:
    body = dict(value)
    body["self_digest_sha256"] = object_hash(body)
    raw = canonical(body)
    if len(raw) > MAX_OUTPUT_BYTES:
        raise ResourceStop("output_byte_cap")
    return raw


def atomic(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".task382-check-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def terminal_result(status: str, reason: str) -> bytes:
    body = {"schema": SCHEMA, "status": status, "terminal": status,
            "accepted": False, "independent": True, "complete": False,
            "reason": reason, "checkpoint": None}
    body["self_digest_sha256"] = object_hash(body)
    return canonical(body)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", required=True)
    p.add_argument("--producer", required=True)
    p.add_argument("--a4-receipt")
    p.add_argument("--a4-receipt-bytes", type=int)
    p.add_argument("--a4-receipt-sha256")
    p.add_argument("--a4-verdict")
    p.add_argument("--a4-verdict-bytes", type=int)
    p.add_argument("--a4-verdict-sha256")
    p.add_argument("--output", required=True)
    return p


def main() -> int:
    args = parser().parse_args()
    output: Path | None = None
    terminal = UNKNOWN_INPUT
    try:
        require(args.mode == "PRODUCTION", "mode:production_only")
        output = output_path(args.output)
        require(not output.exists(), "output:stale")
        pinned(ROOT / PINS["new_producer"][0], PINS["new_producer"], "new_producer.code")
        producer_raw, producer = read_new_producer(producer_path(args.producer))
        a4_fields = (args.a4_receipt, args.a4_receipt_bytes, args.a4_receipt_sha256,
                     args.a4_verdict, args.a4_verdict_bytes, args.a4_verdict_sha256)
        has_a4 = all(value is not None for value in a4_fields)
        require(has_a4 or all(value is None for value in a4_fields), "a4:partial_pin_tuple")
        print("A4_LEGAL_SOURCE_CHECK_PROGRESS phase=restore_independent_arithmetic", flush=True)
        owner = restore_v14()
        authority, arithmetic, meter = instantiate_checker(owner)
        split_words, relators, q0 = factor_words()
        print("A4_LEGAL_SOURCE_CHECK_PROGRESS phase=reverse_v360_243_plus_729", flush=True)
        residual = independent_residual(arithmetic, authority.task176, split_words, relators)
        producer_words = compare_residual(producer, residual, arithmetic)
        if not has_a4:
            require(producer.get("schema") == PRODUCER_SCHEMA and
                    producer.get("status") == UNKNOWN_INPUT and
                    producer.get("terminal") == UNKNOWN_INPUT and
                    producer.get("complete") is False and producer.get("reason") == NO_A4_REASON and
                    producer.get("A4_ambient_owner") is None and producer.get("C_rel") is None and
                    producer.get("claim_boundary", {}).get("canonical_residual_action_materialized") is True and
                    producer.get("claim_boundary", {}).get("C_rel_basis_computed") is False,
                    "producer:typed_missing_A4")
            body = {"schema": SCHEMA, "status": UNKNOWN_INPUT, "terminal": UNKNOWN_INPUT,
                    "accepted": True, "independent": True, "complete": False,
                    "reason": NO_A4_REASON,
                    "producer": {"path": args.producer, "bytes": len(producer_raw),
                                 "sha256": bytes_hash(producer_raw)},
                    "canonical_residual_action": {
                        "accepted": True, "word_values_independently_replayed": True,
                        "Gamma_order": 243, "center_order": residual["center_order"],
                        "central_pairs_exhausted": 729, "passing_pairs": residual["passing"],
                        "subgroup_order": 504, "Gamma_intersection_order": 1},
                    "A4_ambient_owner": None, "C_rel": None,
                    "claim_boundary": {"C_rel_basis_computed": False,
                                       "occurrence_image": False, "compatible_lift": False,
                                       "fake": False, "Ihara_witness": False},
                    "resource_caps": {"producer_bytes": MAX_PRODUCER_BYTES,
                                      "output_bytes": MAX_OUTPUT_BYTES,
                                      "Gamma_raw_bytes": MAX_GAMMA_RAW_BYTES,
                                      "frozen_runtime": meter.public()},
                    "checkpoint": None}
            atomic(output, sealed(body))
            terminal = UNKNOWN_INPUT
            print(PREFIX + " " + terminal, flush=True)
            return 0
        require(isinstance(args.a4_receipt_bytes, int) and
                isinstance(args.a4_verdict_bytes, int) and
                0 < args.a4_receipt_bytes <= MAX_A4_BYTES and
                0 < args.a4_verdict_bytes <= MAX_A4_BYTES and all(
                    isinstance(value, str) and len(value) == 64 and value == value.lower() and
                    all(ch in "0123456789abcdef" for ch in value)
                    for value in (args.a4_receipt_sha256, args.a4_verdict_sha256)),
                "a4:pin_shape")
        a4_raw = pinned(input_path(args.a4_receipt, "a4.receipt"),
                        (args.a4_receipt, args.a4_receipt_bytes, args.a4_receipt_sha256),
                        "a4.receipt")
        verdict_raw = pinned(input_path(args.a4_verdict, "a4.verdict"),
                             (args.a4_verdict, args.a4_verdict_bytes, args.a4_verdict_sha256),
                             "a4.verdict")
        a4, a4_verdict = json_object(a4_raw, "a4.receipt"), json_object(verdict_raw, "a4.verdict")
        labels, matrices = validate_a4(a4, a4_verdict)
        require(a4.get("authority") == authority.identity and
                producer.get("schema") == PRODUCER_SCHEMA and producer.get("status") == "COMPLETE" and
                producer.get("terminal") == PASS and producer.get("complete") is True and
                producer.get("A4_ambient_owner", {}).get("receipt", {}).get("sha256") ==
                args.a4_receipt_sha256 and
                producer.get("A4_ambient_owner", {}).get("verdict", {}).get("sha256") ==
                args.a4_verdict_sha256,
                "producer:positive_A4_binding")
        print("A4_LEGAL_SOURCE_CHECK_PROGRESS phase=latest_pivot_C_rel", flush=True)
        c_rel_check = check_c_rel(producer, a4, labels, matrices, residual,
                                  producer_words, arithmetic)
        body = {"schema": SCHEMA, "status": "COMPLETE", "terminal": PASS,
                "accepted": True, "independent": True, "complete": True,
                "producer": {"path": args.producer, "bytes": len(producer_raw),
                             "sha256": bytes_hash(producer_raw)},
                "A4_ambient_owner": {
                    "receipt": {"path": args.a4_receipt, "bytes": args.a4_receipt_bytes,
                                "sha256": args.a4_receipt_sha256},
                    "verdict": {"path": args.a4_verdict, "bytes": args.a4_verdict_bytes,
                                "sha256": args.a4_verdict_sha256}},
                "canonical_residual_action": {
                    "accepted": True, "reverse_243_scan": True,
                    "reverse_729_scan": True, "word_values_independently_replayed": True,
                    "subgroup_order": 504, "Gamma_intersection_order": 1},
                "C_rel": c_rel_check,
                "claim_boundary": {"occurrence_image": False, "A_over_JA": False,
                                   "L_over_JL": False, "compatible_lift": False,
                                   "fake": False, "Ihara_witness": False},
                "resource_caps": {"A4_input_bytes_each": MAX_A4_BYTES,
                                  "producer_bytes": MAX_PRODUCER_BYTES,
                                  "output_bytes": MAX_OUTPUT_BYTES,
                                  "Gamma_raw_bytes": MAX_GAMMA_RAW_BYTES,
                                  "K_rank": MAX_K_RANK,
                                  "literal_letters_each": MAX_LITERAL_LETTERS,
                                  "frozen_runtime": meter.public()},
                "checkpoint": None}
        atomic(output, sealed(body))
        terminal = PASS
    except Reject as exc:
        reason = UNKNOWN_INPUT + ":" + str(exc).replace(" ", "_")
        terminal = UNKNOWN_INPUT
        if output is not None and not output.exists():
            atomic(output, terminal_result(UNKNOWN_INPUT, reason))
    except ResourceStop as exc:
        reason = UNKNOWN_RESOURCE + ":" + str(exc).replace(" ", "_")
        terminal = UNKNOWN_RESOURCE
        if output is not None and not output.exists():
            atomic(output, terminal_result(UNKNOWN_RESOURCE, reason))
    except Exception as exc:
        name = exc.__class__.__name__
        status = UNKNOWN_RESOURCE if name in {"ResourceStop", "HardStop"} else UNKNOWN_INPUT
        reason = status + ":FROZEN_CHECKER_OWNER_" + name + ":" + str(exc).replace(" ", "_")
        terminal = status
        if output is not None and not output.exists():
            atomic(output, terminal_result(status, reason))
    print(PREFIX + " " + terminal, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
