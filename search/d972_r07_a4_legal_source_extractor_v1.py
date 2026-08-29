#!/usr/bin/env python3
"""Bounded compiler for the legal A4 source [R_S(Delta0), K].

This program authenticates the frozen task157ee/task176/task198 owners,
materializes the canonical PSL(2,8) complement by the v360 243+729
algorithm, and applies its two word actions to a future positive A4 owner.
It does not construct a lift, fake, or Ihara witness.
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
SCHEMA = "d972-r07-a4-legal-source-extractor/v1"
A4_SCHEMA = "d972-r07-word-independent-successor-kernel/v6"
A4_PASS = "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS"
PASS = "A4_LEGAL_RELATIVE_SOURCE_COMPLETE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
PREFIX = "R07_A4_LEGAL_SOURCE_EXTRACTOR_V1_PRODUCER_TERMINAL"
MISSING_ACTION = "WORD_BEARING_CANONICAL_RESIDUAL_ACTION_NOT_AUTHENTICATED"

MAX_A4_BYTES = 2_000_000_000
MAX_OUTPUT_BYTES = 2_000_000_000
MAX_GAMMA_RAW_BYTES = 1_000_000
MAX_K_RANK = 200_000
MAX_LITERAL_LETTERS = 20_000_000

PINS: dict[str, tuple[str, int, str]] = {
    "a4_wrapper_v12": (
        "search/d972_r07_word_independent_successor_kernel_v12.py", 7209,
        "816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5"),
    "a4_base_v6": (
        "search/d972_r07_word_independent_successor_kernel_v6.py", 219187,
        "aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a"),
    "a4_checker_v14": (
        "crosscheck/check_d972_r07_word_independent_successor_kernel_v14.py", 8074,
        "7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47"),
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


class InputStop(Exception):
    pass


class ResourceStop(Exception):
    pass


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise InputStop(reason)


def resource(condition: bool, reason: str) -> None:
    if not condition:
        raise ResourceStop(reason)


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_pin(path: Path, size: int, expected: str, label: str) -> bytes:
    require(path.is_file() and not path.is_symlink(), label + ":regular_file")
    raw = path.read_bytes()
    require(len(raw) == size and sha(raw) == expected, label + ":physical_pin")
    return raw


def parse_json(raw: bytes, label: str, canonical: bool = True) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InputStop(label + ":ascii_json") from exc
    require(isinstance(value, dict), label + ":object")
    if canonical:
        require(raw in (canon(value), canon(value) + b"\n"), label + ":canonical_json")
    return value


def verify_self_digest(value: dict[str, Any], label: str) -> None:
    body = dict(value)
    claimed = body.pop("self_digest_sha256", None)
    require(isinstance(claimed, str) and claimed == digest(body), label + ":self_digest")


def safe_input(text: str, label: str) -> Path:
    path = (ROOT / text).resolve()
    base = (ROOT / "ci" / "in").resolve()
    require(path.parent == base and path.name == Path(text).name, label + ":ci_in_path")
    return path


def safe_output(text: str) -> Path:
    path = (ROOT / text).resolve()
    base = (ROOT / "ci" / "out").resolve()
    require(path.parent == base and path.name == Path(text).name, "output:ci_out_path")
    return path


def word_inv(word: Sequence[int]) -> list[int]:
    return [-int(letter) for letter in reversed(word)]


def word_reduce(word: Sequence[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        letter = int(raw)
        require(letter in (-2, -1, 1, 2), "word:letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    resource(len(out) <= MAX_LITERAL_LETTERS, "literal_letter_cap")
    return out


def word_mul(*words: Sequence[int]) -> list[int]:
    return word_reduce([letter for word in words for letter in word])


def exponent_sums(word: Sequence[int]) -> list[int]:
    return [sum(1 if x == generator else -1 if x == -generator else 0 for x in word)
            for generator in (1, 2)]


def add_sparse(left: dict[str, int], right: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(left)
    for key, raw in right.items():
        value = (out.get(key, 0) + int(scale) * int(raw)) % 3
        if value:
            out[key] = value
        else:
            out.pop(key, None)
    return out


def scale_sparse(row: dict[str, int], scale: int) -> dict[str, int]:
    return {key: int(value) * int(scale) % 3 for key, value in row.items()
            if int(value) * int(scale) % 3}


def linear_sum(coefficients: dict[str, int], rows: dict[str, dict[str, int]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for label, coefficient in coefficients.items():
        require(label in rows, "linear_sum:label")
        out = add_sparse(out, rows[label], coefficient)
    return out


def sparse_column(value: Any, labels: set[str], label: str) -> dict[str, int]:
    require(isinstance(value, dict) and set(value) <= labels, label + ":support")
    out: dict[str, int] = {}
    for key, raw in value.items():
        require(type(raw) is int and raw in (1, 2), label + ":coefficient")
        out[key] = raw
    return out


def matrix_compose(left: dict[str, dict[str, int]],
                   right: dict[str, dict[str, int]],
                   labels: Sequence[str]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for source in labels:
        column: dict[str, int] = {}
        for middle, a in right[source].items():
            for target, b in left[middle].items():
                value = (column.get(target, 0) + int(a) * int(b)) % 3
                if value:
                    column[target] = value
                else:
                    column.pop(target, None)
        out[source] = column
    return out


def validate_kernel(kernel: Any, label: str) -> tuple[list[str], dict[str, dict[str, dict[str, int]]]]:
    require(isinstance(kernel, dict) and kernel.get("complete") is True, label + ":complete")
    roster = kernel.get("K_roster")
    require(isinstance(roster, list) and 0 < len(roster) <= MAX_K_RANK, label + ":K_roster")
    labels: list[str] = []
    for item in roster:
        require(isinstance(item, dict), label + ":K_item")
        name, word = item.get("label"), item.get("word")
        require(isinstance(name, str) and name not in labels, label + ":K_order")
        require(isinstance(word, list) and all(type(x) is int and x in (-2, -1, 1, 2) for x in word),
                label + ":literal_word")
        resource(len(word) <= MAX_LITERAL_LETTERS, "K_literal_letter_cap")
        require(isinstance(item.get("ancestry"), dict) and item.get("strict_rank_rise") is True,
                label + ":word_ancestry")
        actual = item.get("rho1_actual_flattened")
        require(isinstance(actual, dict) and all(type(v) is int and v in (1, 2) for v in actual.values()),
                label + ":actual_fine_row")
        labels.append(name)
    label_set = set(labels)
    queue = kernel.get("queue")
    require(isinstance(queue, dict) and queue.get("accepted") == len(roster) and
            queue.get("cursor") == len(roster) and queue.get("next") == len(roster),
            label + ":queue_exhaustion")
    raw_matrices = kernel.get("action_matrices")
    require(isinstance(raw_matrices, dict) and set(raw_matrices) == {"1", "-1", "2", "-2"},
            label + ":four_actions")
    matrices: dict[str, dict[str, dict[str, int]]] = {}
    for letter in ("1", "-1", "2", "-2"):
        raw_matrix = raw_matrices[letter]
        require(isinstance(raw_matrix, dict) and set(raw_matrix) == label_set,
                label + ":matrix_columns")
        matrices[letter] = {source: sparse_column(raw_matrix[source], label_set,
                                                  label + ":matrix:" + letter)
                            for source in labels}
    identity = {source: {source: 1} for source in labels}
    require(matrix_compose(matrices["1"], matrices["-1"], labels) == identity and
            matrix_compose(matrices["-1"], matrices["1"], labels) == identity and
            matrix_compose(matrices["2"], matrices["-2"], labels) == identity and
            matrix_compose(matrices["-2"], matrices["2"], labels) == identity,
            label + ":inverse_replay")
    require(kernel.get("inverse_laws") == {"1-1": True, "-11": True,
                                             "2-2": True, "-22": True},
            label + ":inverse_owner")
    require(isinstance(kernel.get("actions"), list) and len(kernel["actions"]) == 4 * len(roster),
            label + ":complete_actions")
    return labels, matrices


def validate_a4(producer: dict[str, Any], checker: dict[str, Any]) -> tuple[
        list[str], dict[str, dict[str, dict[str, int]]]]:
    verify_self_digest(producer, "a4.producer")
    verify_self_digest(checker, "a4.checker")
    for value, label in ((producer, "producer"), (checker, "checker")):
        require(value.get("schema") == A4_SCHEMA and value.get("status") == "COMPLETE" and
                value.get("terminal") == A4_PASS and value.get("complete") is True,
                "a4:" + label + ":positive")
        require(value.get("A4_presentation_input") == 1 and
                value.get("A4_invariant_closure") == 1 and
                value.get("A4_word_bearing_K") == 1,
                "a4:" + label + ":milestones")
    require(checker.get("accepted") is True and checker.get("independent") is True,
            "a4:checker:independent_acceptance")
    p_labels, p_matrices = validate_kernel(producer.get("kernel"), "a4.producer.kernel")
    c_labels, c_matrices = validate_kernel(checker.get("kernel"), "a4.checker.kernel")
    require(p_labels == c_labels and p_matrices == c_matrices, "a4:independent_action_equality")
    for field in ("K_roster", "inverse_laws", "queue"):
        require(producer["kernel"].get(field) == checker["kernel"].get(field),
                "a4:independent:" + field)
    require(producer.get("authority") == checker.get("authority"), "a4:authority_equality")
    authority = producer.get("authority")
    require(isinstance(authority, dict) and
            authority.get("receipt_sha256") ==
            "82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5" and
            authority.get("task176", {}).get("receipt", {}).get("sha256") ==
            "715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41",
            "a4:typed_task198_task176_square")
    return p_labels, p_matrices


def restore_v12() -> dict[str, Any]:
    wrapper_pin = PINS["a4_wrapper_v12"]
    wrapper_path = ROOT / wrapper_pin[0]
    wrapper_raw = read_pin(wrapper_path, wrapper_pin[1], wrapper_pin[2], "a4.wrapper_v12")
    read_pin(ROOT / PINS["a4_checker_v14"][0], PINS["a4_checker_v14"][1],
             PINS["a4_checker_v14"][2], "a4.checker_v14")
    wrapper_ns: dict[str, Any] = {"__name__": "d382_v12_wrapper",
                                  "__file__": str(wrapper_path), "__package__": None}
    exec(compile(wrapper_raw, str(wrapper_path), "exec"), wrapper_ns, wrapper_ns)
    source = Path(wrapper_ns["SOURCE"])
    base_pin = PINS["a4_base_v6"]
    require(source.resolve() == (ROOT / base_pin[0]).resolve(), "a4.wrapper:source_path")
    raw = read_pin(source, base_pin[1], base_pin[2], "a4.base_v6")
    for old, new in wrapper_ns["PATCHES"]:
        require(raw.count(old) == 1, "a4.wrapper:patch_site")
        raw = raw.replace(old, new)
    owner: dict[str, Any] = {"__name__": "d382_frozen_v12_owner",
                             "__file__": str(source), "__package__": None}
    exec(compile(raw, str(source), "exec"), owner, owner)
    return owner


def instantiate_owner(owner: dict[str, Any]) -> tuple[Any, Any, Any]:
    require(tuple(owner["E4_SOURCE"]) == PINS["e4_arithmetic"] and
            tuple(owner["Q3_SOURCE"]) == PINS["q3_receipt"],
            "a4:frozen_arithmetic_pin_constants")
    args = SimpleNamespace(**{"task198_" + key: "ci/in/" + value
                              for key, value in owner["AUTH"].items()})
    meter = owner["Meter"](dict(owner["CAPS"]))
    authority = owner["AuthorityAdapter"](args, meter)
    runtime = owner["Runtime"](authority, meter)
    return authority, runtime, meter


def ast_literals(raw: bytes) -> tuple[list[list[int]], list[list[int]]]:
    try:
        tree = ast.parse(raw.decode("ascii"))
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise InputStop("task157ee:source_ast") from exc
    found: dict[str, Any] = {}
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            target = node.targets[0] if isinstance(node, ast.Assign) and len(node.targets) == 1 else \
                     node.target if isinstance(node, ast.AnnAssign) else None
            if isinstance(target, ast.Name) and target.id in {"SPLIT_WORDS", "P_RELATORS"}:
                found[target.id] = ast.literal_eval(node.value)
    require(set(found) == {"SPLIT_WORDS", "P_RELATORS"}, "task157ee:literal_fields")
    split_words, relators = found["SPLIT_WORDS"], found["P_RELATORS"]
    require(isinstance(split_words, list) and len(split_words) == 4 and
            isinstance(relators, list) and len(relators) == 5, "task157ee:literal_counts")
    for word in split_words + relators:
        require(isinstance(word, list) and word and
                all(type(x) is int and x in (-2, -1, 1, 2) for x in word),
                "task157ee:literal_word")
    return split_words, relators


def task157ee_owner() -> tuple[list[list[int]], list[list[int]], dict[str, Any]]:
    source_pin = PINS["task157ee_producer"]
    source_raw = read_pin(ROOT / source_pin[0], source_pin[1], source_pin[2],
                          "task157ee.producer")
    for name in ("task157ee_checker", "task157ee_driver"):
        pin = PINS[name]
        read_pin(ROOT / pin[0], pin[1], pin[2], "task157ee." + name)
    split_words, relators = ast_literals(source_raw)
    receipt_pin = PINS["task157ee_receipt"]
    receipt = parse_json(read_pin(ROOT / receipt_pin[0], receipt_pin[1], receipt_pin[2],
                                  "task157ee.receipt"), "task157ee.receipt")
    require(receipt.get("schema") == "d972-b345-joint-kernel-qstar-closure/v1" and
            receipt.get("status") == "B345_JOINT_KERNEL_QSTAR_CLOSED" and
            receipt.get("terminal_token") == "B345_JOINT_KERNEL_QSTAR_CLOSED",
            "task157ee:positive")
    q0 = receipt.get("q0_presentation", {})
    require(q0.get("P_order") == 504 and q0.get("Q0_order") == 1469664 and
            q0.get("split_word_lengths") == [len(word) for word in split_words] and
            q0.get("split_word_sha256") == digest(split_words) ==
            "e016a4762e8e89e6dcdb7f63d9c39426245af6e9fa5eb94f980106561e103622" and
            q0.get("P_relator_count") == 5,
            "task157ee:complete_split_presentation")
    return split_words, relators, q0


def unpack(owner: Any, width: int, count: int, label: str) -> bytes:
    require(isinstance(owner, dict) and owner.get("codec") == "zlib+base64" and
            owner.get("record_width_bytes") == width and owner.get("record_count") == count and
            owner.get("raw_bytes") == width * count <= MAX_GAMMA_RAW_BYTES,
            label + ":envelope")
    try:
        compressed = base64.b64decode(owner.get("data", ""), validate=True)
    except Exception as exc:
        raise InputStop(label + ":base64") from exc
    require(len(compressed) == owner.get("compressed_bytes") and
            sha(compressed) == owner.get("compressed_sha256"), label + ":compressed_pin")
    decoder = zlib.decompressobj()
    raw = decoder.decompress(compressed, width * count + 1)
    raw += decoder.flush()
    require(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail and
            len(raw) == width * count and sha(raw) == owner.get("raw_sha256"),
            label + ":lossless_decode")
    return raw


def value_from_blob(raw: bytes, index: int) -> tuple[bytes, bytes]:
    degree = 36 if index < 5 else 144
    width = 40 if index < 5 else 154
    require(len(raw) == width, "Gamma:value_width")
    permutation, pc = raw[:degree], raw[degree:]
    require(len(permutation) == degree and set(permutation) == set(range(degree)),
            "Gamma:permutation")
    return permutation, pc


def value_blob(value: Any) -> bytes:
    require(isinstance(value, tuple) and len(value) == 2 and
            isinstance(value[0], bytes) and isinstance(value[1], bytes), "roof:value")
    return value[0] + value[1]


class RoofGroup:
    def __init__(self, runtime: Any):
        self.runtime = runtime
        self.groups = [runtime.quotient(index) for index in range(10)]
        self.identity = tuple(group.identity for group in self.groups)

    def mul(self, left: Sequence[Any], right: Sequence[Any]) -> tuple[Any, ...]:
        require(len(left) == len(right) == 10, "roof:tuple_width")
        return tuple(group.mul(a, b) for group, a, b in zip(self.groups, left, right))

    def inverse(self, value: Sequence[Any]) -> tuple[Any, ...]:
        require(len(value) == 10, "roof:tuple_width")
        return tuple(group.inverse(a) for group, a in zip(self.groups, value))

    def conjugate(self, outer: Sequence[Any], inner: Sequence[Any]) -> tuple[Any, ...]:
        return self.mul(self.mul(outer, inner), self.inverse(outer))

    def key(self, value: Sequence[Any]) -> tuple[bytes, ...]:
        return tuple(value_blob(item) for item in value)

    def public(self, value: Sequence[Any]) -> list[str]:
        return [item.hex() for item in self.key(value)]

    def eval(self, word: Sequence[int], generators: Sequence[Sequence[Any]]) -> tuple[Any, ...]:
        result = self.identity
        inverses = [self.inverse(value) for value in generators]
        for raw in word:
            index = abs(int(raw)) - 1
            require(0 <= index < len(generators), "presentation:letter")
            result = self.mul(result, generators[index] if raw > 0 else inverses[index])
        return result


def permutation_inverse(value: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(value)
    for index, image in enumerate(value, 1):
        out[image - 1] = index
    return tuple(out)


def permutation_eval(word: Sequence[int], generators: Sequence[tuple[int, ...]]) -> tuple[int, ...]:
    result = tuple(range(1, len(generators[0]) + 1))
    inverses = [permutation_inverse(value) for value in generators]
    for letter in word:
        right = generators[abs(int(letter)) - 1] if letter > 0 else inverses[abs(int(letter)) - 1]
        result = tuple(result[right[index] - 1] for index in range(len(result)))
    return result


def replay_q0_projection(q3: dict[str, Any], split_words: list[list[int]],
                         relators: list[list[int]], final_words: list[list[int]]) -> dict[str, Any]:
    marked = q3.get("coarse_models", {}).get("Q0", {}).get("marked_permutations")
    require(isinstance(marked, list) and len(marked) == 2 and
            all(isinstance(row, list) and len(row) == 36 for row in marked),
            "v360:Q0_marked_projection")
    qgens = [tuple(int(value) for value in row) for row in marked]
    require(all(set(row) == set(range(1, 37)) for row in qgens), "v360:Q0_permutations")
    pgens = [tuple(row[:9]) for row in qgens]
    ggens = [tuple(value - 9 for value in row[9:]) for row in qgens]
    pid, gid = tuple(range(1, 10)), tuple(range(1, 28))
    expected = [(pgens[0], gid), (pgens[1], gid), (pid, ggens[0]), (pid, ggens[1])]
    observed = [(permutation_eval(word, pgens), permutation_eval(word, ggens))
                for word in split_words]
    require(observed == expected and
            all(permutation_eval(row, pgens) == pid for row in relators),
            "v360:pure_factor_projection_replay")
    final = [(permutation_eval(word, pgens), permutation_eval(word, ggens))
             for word in final_words]
    require(final == expected[:2], "v360:final_pure_S_projection")
    return {"Q0_order": 1469664, "P_order": 504, "G9_order": 2916,
            "all_four_split_factor_images_replayed": True,
            "final_generators_project_to_fixed_P_generators": True,
            "final_projection_sha256": digest(final)}


def gamma_owner(task176: dict[str, Any], runtime: Any, group: RoofGroup) -> dict[str, Any]:
    result = task176.get("result", {})
    gamma = result.get("Gamma", {})
    require(result.get("extension") == {"Gamma_order": 243, "Q0_order": 1469664,
                                         "exact_sequence": "1->Gamma->G->Q0->1"} and
            gamma.get("order") == 243, "task176:Gamma_extension")
    record_words = gamma.get("record_words")
    require(isinstance(record_words, list) and len(record_words) == 26, "Gamma:record_words")
    for word in record_words:
        require(isinstance(word, list) and word and
                all(type(x) is int and x in (-2, -1, 1, 2) for x in word),
                "Gamma:record_word")
    widths = [40] * 5 + [154] * 5
    row_width = sum(widths)
    raw_states = unpack(gamma.get("ten_coordinate_states"), row_width, 243,
                        "Gamma.ten_coordinate_states")
    raw_parents = unpack(gamma.get("section_parent_states_u16le"), 2, 243,
                         "Gamma.parent_states")
    raw_records = unpack(gamma.get("section_parent_record_u8"), 1, 243,
                         "Gamma.parent_records")
    states: list[tuple[Any, ...]] = []
    offset = 0
    for _ in range(243):
        coordinates = []
        for index, width in enumerate(widths):
            coordinates.append(value_from_blob(raw_states[offset:offset + width], index))
            offset += width
        states.append(tuple(coordinates))
    parents = [struct.unpack_from("<H", raw_parents, 2 * index)[0] for index in range(243)]
    records = list(raw_records)
    require(parents[0] == records[0] == 0 and group.key(states[0]) == group.key(group.identity),
            "Gamma:root")
    record_values = [tuple(state.a for state in runtime.states_direct(word))
                     for word in record_words]
    words: list[list[int]] = [[]]
    for index in range(1, 243):
        parent, record = parents[index], records[index]
        require(1 <= parent <= index and 1 <= record <= 26, "Gamma:parent_recurrence")
        parent_index, record_index = parent - 1, record - 1
        require(group.key(group.mul(states[parent_index], record_values[record_index])) ==
                group.key(states[index]), "Gamma:parent_value_replay")
        words.append(word_mul(words[parent_index], record_words[record_index]))
    require(len({group.key(value) for value in states}) == 243, "Gamma:state_uniqueness")
    for index, word in enumerate(words[1:], 1):
        if index in (1, 2, 3, 6, 9, 242):
            replay = tuple(state.a for state in runtime.states_direct(word))
            require(group.key(replay) == group.key(states[index]), "Gamma:literal_canary")
    return {"states": states, "words": words, "records": record_values,
            "record_words": record_words,
            "table_sha256": gamma["ten_coordinate_states"]["raw_sha256"],
            "parent_sha256": digest({"parents": parents, "records": records})}


def materialize_residual(runtime: Any, task176: dict[str, Any],
                         split_words: list[list[int]], relators: list[list[int]]) -> dict[str, Any]:
    group = RoofGroup(runtime)
    gamma = gamma_owner(task176, runtime, group)
    states, state_words = gamma["states"], gamma["words"]
    record_values = gamma["records"]
    p_values = [tuple(state.a for state in runtime.states_direct(word)) for word in split_words[:2]]
    solution_lists: list[list[int]] = []
    for p_value in p_values:
        targets = [group.key(group.conjugate(p_value, h)) for h in record_values]
        solutions = []
        for index, candidate in enumerate(states):
            if all(group.key(group.conjugate(candidate, h)) == target
                   for h, target in zip(record_values, targets)):
                solutions.append(index)
        require(len(solutions) == 27, "v360:inner_solution_coset")
        chosen = states[solutions[0]]
        require(all(group.key(group.conjugate(p_value, h)) ==
                    group.key(group.conjugate(chosen, h)) for h in states),
                "v360:full_243_inner_replay")
        solution_lists.append(solutions)
    centers = [index for index, value in enumerate(states)
               if all(group.key(group.mul(value, h)) == group.key(group.mul(h, value))
                      for h in record_values)]
    require(len(centers) == 27, "v360:center_order")
    for index in centers:
        require(all(group.key(group.mul(states[index], h)) ==
                    group.key(group.mul(h, states[index])) for h in states),
                "v360:center_full_replay")
    preliminary_values = []
    preliminary_words = []
    for p_value, p_word, solutions in zip(p_values, split_words[:2], solution_lists):
        gamma_index = solutions[0]
        preliminary_values.append(group.mul(group.inverse(states[gamma_index]), p_value))
        preliminary_words.append(word_mul(word_inv(state_words[gamma_index]), p_word))
    for value in preliminary_values:
        require(all(group.key(group.mul(value, h)) == group.key(group.mul(h, value))
                    for h in states), "v360:preliminary_centralizer")
    passing: list[tuple[int, int, tuple[Any, ...], tuple[Any, ...]]] = []
    for left in centers:
        s1 = group.mul(states[left], preliminary_values[0])
        for right in centers:
            s2 = group.mul(states[right], preliminary_values[1])
            if all(group.key(group.eval(relator, (s1, s2))) == group.key(group.identity)
                   for relator in relators):
                passing.append((left, right, s1, s2))
    require(len(passing) == 1, "v360:unique_729_PSL_pair")
    left, right, s1, s2 = passing[0]
    final_words = [word_mul(state_words[left], preliminary_words[0]),
                   word_mul(state_words[right], preliminary_words[1])]
    final_values = [s1, s2]
    for word, value in zip(final_words, final_values):
        replay = tuple(state.a for state in runtime.states_direct(word))
        require(group.key(replay) == group.key(value), "v360:final_literal_replay")
        require(all(group.key(group.mul(value, h)) == group.key(group.mul(h, value))
                    for h in states), "v360:final_centralizer")
    generators = [s1, s2, group.inverse(s1), group.inverse(s2)]
    seen = {group.key(group.identity): group.identity}
    queue = [group.identity]
    cursor = 0
    while cursor < len(queue):
        current = queue[cursor]
        cursor += 1
        for generator in generators:
            candidate = group.mul(current, generator)
            key = group.key(candidate)
            if key not in seen:
                seen[key] = candidate
                queue.append(candidate)
                require(len(seen) <= 504, "v360:subgroup_order_upper_bound")
    require(len(seen) == 504, "v360:subgroup_order_504")
    gamma_keys = {group.key(value) for value in states}
    require(set(seen).intersection(gamma_keys) == {group.key(group.identity)},
            "v360:trivial_Gamma_intersection")
    projection = replay_q0_projection(runtime.q3, split_words, relators, final_words)
    return {
        "group": group,
        "words": final_words,
        "values": final_values,
        "public": {
            "theorem": "v360 canonical residual action materialization",
            "Gamma_order": 243,
            "Gamma_record_count": 26,
            "Gamma_table_raw_sha256": gamma["table_sha256"],
            "Gamma_parent_recurrence_sha256": gamma["parent_sha256"],
            "inner_solution_counts": [len(value) for value in solution_lists],
            "inner_solution_state_ids_1_based": [[index + 1 for index in value]
                                                  for value in solution_lists],
            "center_order": len(centers),
            "center_state_ids_1_based": [index + 1 for index in centers],
            "central_pairs_exhausted": len(centers) ** 2,
            "complete_PSL_relator_count": len(relators),
            "complete_PSL_relators_sha256": digest(relators),
            "passing_central_pairs": 1,
            "selected_center_state_ids_1_based": [left + 1, right + 1],
            "subgroup_order": len(seen),
            "Gamma_intersection_order": 1,
            "Q0_projection_replay": projection,
            "generators": [{"id": "s" + str(index + 1), "word": word,
                              "word_sha256": digest(word), "value_hex": group.public(value)}
                             for index, (word, value) in enumerate(zip(final_words, final_values))],
        },
    }


def action_of_word(word: Sequence[int], matrices: dict[str, dict[str, dict[str, int]]],
                   labels: list[str]) -> dict[str, dict[str, int]]:
    result = {label: {label: 1} for label in labels}
    for letter in word:
        result = matrix_compose(result, matrices[str(int(letter))], labels)
    return result


def reduce_seed(raw: dict[str, int], seed_id: str, labels: list[str],
                rows: dict[int, dict[str, int]], formals: dict[int, dict[str, int]]) -> dict[str, Any]:
    work = dict(raw)
    formal = {seed_id: 1}
    trace = []
    for pivot in sorted(rows):
        coefficient = work.get(labels[pivot], 0)
        if coefficient:
            work = add_sparse(work, rows[pivot], -coefficient)
            formal = add_sparse(formal, formals[pivot], -coefficient)
            trace.append({"pivot": labels[pivot], "coefficient": coefficient})
    if not work:
        return {"rank_rise": False, "reduction_trace": trace, "relation": formal}
    pivot = next(index for index, label in enumerate(labels) if work.get(label, 0))
    scale = 1 if work[labels[pivot]] == 1 else 2
    normalized = scale_sparse(work, scale)
    normalized_formal = scale_sparse(formal, scale)
    rows[pivot], formals[pivot] = normalized, normalized_formal
    return {"rank_rise": True, "pivot_index": pivot, "pivot": labels[pivot],
            "normalization_scale": scale, "echelon_row": normalized,
            "change_of_basis": normalized_formal, "reduction_trace": trace}


def extract_c_rel(runtime: Any, a4: dict[str, Any], labels: list[str],
                  matrices: dict[str, dict[str, dict[str, int]]],
                  residual: dict[str, Any]) -> dict[str, Any]:
    roster = a4["kernel"]["K_roster"]
    k_words = {item["label"]: list(item["word"]) for item in roster}
    k_fine = {item["label"]: {str(key): int(value) for key, value in
                              item["rho1_actual_flattened"].items()} for item in roster}
    actions = [action_of_word(word, matrices, labels) for word in residual["words"]]
    rows: dict[int, dict[str, int]] = {}
    formals: dict[int, dict[str, int]] = {}
    blocks: list[dict[str, Any]] = []
    basis: list[dict[str, Any]] = []
    for generator_index, (s_word, action) in enumerate(zip(residual["words"], actions), 1):
        for basis_index, label in enumerate(labels, 1):
            seed_id = "s" + str(generator_index) + ":" + label
            conjugate_vector = action[label]
            seed = add_sparse(conjugate_vector, {label: 1}, -1)
            u_word = k_words[label]
            conjugate_word = word_mul(s_word, u_word, word_inv(s_word))
            commutator_word = word_mul(conjugate_word, word_inv(u_word))
            require(exponent_sums(commutator_word) == [0, 0], "C_rel:commutator_exponent_sums")
            conjugate_states = runtime.states_direct(conjugate_word)
            require(all(state.identity_roof() for state in conjugate_states),
                    "C_rel:conjugate_coarse_identity")
            conjugate_fine = runtime.row_from_states(conjugate_states)
            require(conjugate_fine == linear_sum(conjugate_vector, k_fine),
                    "C_rel:word_order_action_binding")
            commutator_states = runtime.states_direct(commutator_word)
            require(all(state.identity_roof() for state in commutator_states),
                    "C_rel:commutator_coarse_identity")
            commutator_fine = runtime.row_from_states(commutator_states)
            require(commutator_fine == linear_sum(seed, k_fine),
                    "C_rel:literal_commutator_fine_value")
            detail = reduce_seed(seed, seed_id, labels, rows, formals)
            block = {"seed_id": seed_id, "residual_generator_id": "s" + str(generator_index),
                     "K_basis_id": label, "K_basis_ordinal": basis_index,
                     "full_K_vector": seed, "conjugate_K_vector": conjugate_vector,
                     "literal_commutator_word_sha256": digest(commutator_word),
                     "conjugate_fine_value_sha256": digest(conjugate_fine),
                     "commutator_fine_value_sha256": digest(commutator_fine),
                     "coarse_identity": True, "integer_exponent_sums": [0, 0],
                     "rank_rise": detail["rank_rise"]}
            blocks.append(block)
            if detail["rank_rise"]:
                basis.append({**block, "literal_commutator_word": commutator_word,
                              "direct_fine_value": commutator_fine,
                              "literal_commutator_ancestry": [["s" + str(generator_index), label, 1]],
                              "formation_ancestry": {
                                  "theorem": "v37 relative formation surjectivity",
                                  "claim": "some Pi_S preimage has this finite value",
                                  "not_claimed": "identity with the displayed literal commutator"},
                              "pivot": detail["pivot"],
                              "pivot_index": detail["pivot_index"],
                              "normalization_scale": detail["normalization_scale"],
                              "echelon_row": detail["echelon_row"],
                              "change_of_basis": detail["change_of_basis"],
                              "reduction_trace": detail["reduction_trace"]})
    echelon = [{"pivot_index": pivot, "pivot": labels[pivot], "row": rows[pivot],
                "change_of_basis": formals[pivot]} for pivot in sorted(rows)]
    require(len(basis) == len(rows), "C_rel:rank_accounting")
    return {
        "formula": "C_rel=R_S(Delta1) intersect K=[R_S(Delta0),K]",
        "residual": "R_S(Delta0)=tilde-S",
        "ambient_K_dimension": len(labels),
        "ambient_K_labels": labels,
        "block_order": "s1 over ordered K, then s2 over ordered K",
        "block_count": len(blocks),
        "block_columns": blocks,
        "rank": len(rows),
        "basis": basis,
        "echelon": echelon,
        "final_span_coordinates": [item["row"] for item in echelon],
        "rank_proof_sha256": digest({"blocks": blocks, "echelon": echelon}),
        "commutator_convention": "[s,u]=s*u*s^-1*u^-1",
        "literal_and_formation_ancestry_distinguished": True,
        "extra_side_gate_intersection": False,
    }


def frozen_identities() -> dict[str, Any]:
    return {name: {"path": value[0], "bytes": value[1], "sha256": value[2]}
            for name, value in PINS.items()}


def seal(value: dict[str, Any]) -> bytes:
    body = dict(value)
    body["self_digest_sha256"] = digest(body)
    raw = canon(body)
    if len(raw) > MAX_OUTPUT_BYTES:
        raise ResourceStop("output_byte_cap")
    return raw


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".task382-", dir=str(path.parent))
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


def terminal_receipt(status: str, reason: str) -> bytes:
    body = {"schema": SCHEMA, "status": status, "terminal": status,
            "complete": False, "reason": reason, "checkpoint": None,
            "claim_boundary": {"C_rel_basis_computed": False,
                               "occurrence_image": False, "A_over_JA": False,
                               "L_over_JL": False, "compatible_lift": False,
                               "fake": False, "Ihara_witness": False}}
    body["self_digest_sha256"] = digest(body)
    return canon(body)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", required=True)
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
        output = safe_output(args.output)
        require(not output.exists(), "output:stale")
        a4_fields = (args.a4_receipt, args.a4_receipt_bytes, args.a4_receipt_sha256,
                     args.a4_verdict, args.a4_verdict_bytes, args.a4_verdict_sha256)
        has_a4 = all(value is not None for value in a4_fields)
        require(has_a4 or all(value is None for value in a4_fields), "a4:partial_pin_tuple")
        print("A4_LEGAL_SOURCE_PROGRESS phase=restore_frozen_arithmetic", flush=True)
        owner = restore_v12()
        authority, runtime, meter = instantiate_owner(owner)
        print("A4_LEGAL_SOURCE_PROGRESS phase=materialize_v360_243_plus_729", flush=True)
        split_words, relators, q0 = task157ee_owner()
        residual = materialize_residual(runtime, authority.task176, split_words, relators)
        if not has_a4:
            reason = "UNKNOWN_INPUT:A4_POSITIVE_AMBIENT_K_NOT_AVAILABLE"
            body = {
                "schema": SCHEMA, "status": UNKNOWN_INPUT, "terminal": UNKNOWN_INPUT,
                "complete": False, "reason": reason,
                "A4_ambient_owner": None,
                "frozen_owner_identities": frozen_identities(),
                "task198_task176_authority": authority.identity,
                "task157ee_factor_owner": {
                    "P_order": q0["P_order"], "Q0_order": q0["Q0_order"],
                    "split_word_sha256": digest(split_words),
                    "complete_PSL_relators_sha256": digest(relators),
                    "pure_S_split_word_indices_0_based": [0, 1]},
                "canonical_residual_action": residual["public"],
                "C_rel": None,
                "claim_boundary": {
                    "canonical_residual_action_materialized": True,
                    "C_rel_basis_computed": False, "full_K_used_as_C_rel": False,
                    "occurrence_image": False, "A_over_JA": False, "L_over_JL": False,
                    "compatible_lift": False, "fake": False, "Ihara_witness": False},
                "resource_caps": {
                    "A4_input_bytes_each": MAX_A4_BYTES, "output_bytes": MAX_OUTPUT_BYTES,
                    "Gamma_raw_bytes": MAX_GAMMA_RAW_BYTES, "K_rank": MAX_K_RANK,
                    "literal_letters_each": MAX_LITERAL_LETTERS,
                    "frozen_runtime": meter.public()},
                "checkpoint": None,
            }
            atomic_write(output, seal(body))
            terminal = UNKNOWN_INPUT
            print(PREFIX + " " + terminal, flush=True)
            return 0
        require(isinstance(args.a4_receipt_bytes, int) and
                isinstance(args.a4_verdict_bytes, int) and
                0 < args.a4_receipt_bytes <= MAX_A4_BYTES and
                0 < args.a4_verdict_bytes <= MAX_A4_BYTES, "a4:input_byte_cap")
        require(all(isinstance(value, str) and len(value) == 64 and value == value.lower() and
                    all(ch in "0123456789abcdef" for ch in value)
                    for value in (args.a4_receipt_sha256, args.a4_verdict_sha256)),
                "a4:sha_shape")
        print("A4_LEGAL_SOURCE_PROGRESS phase=authenticate_positive_A4", flush=True)
        a4_raw = read_pin(safe_input(args.a4_receipt, "a4.receipt"),
                          args.a4_receipt_bytes, args.a4_receipt_sha256, "a4.receipt")
        verdict_raw = read_pin(safe_input(args.a4_verdict, "a4.verdict"),
                               args.a4_verdict_bytes, args.a4_verdict_sha256, "a4.verdict")
        a4 = parse_json(a4_raw, "a4.receipt")
        verdict = parse_json(verdict_raw, "a4.verdict")
        labels, matrices = validate_a4(a4, verdict)
        require(a4.get("authority") == authority.identity, "a4:live_authority_replay")
        print("A4_LEGAL_SOURCE_PROGRESS phase=extract_C_rel", flush=True)
        c_rel = extract_c_rel(runtime, a4, labels, matrices, residual)
        body = {
            "schema": SCHEMA, "status": "COMPLETE", "terminal": PASS, "complete": True,
            "A4_ambient_owner": {
                "receipt": {"path": args.a4_receipt, "bytes": args.a4_receipt_bytes,
                            "sha256": args.a4_receipt_sha256},
                "verdict": {"path": args.a4_verdict, "bytes": args.a4_verdict_bytes,
                            "sha256": args.a4_verdict_sha256},
                "positive_authenticated": True,
            },
            "frozen_owner_identities": frozen_identities(),
            "task198_task176_authority": authority.identity,
            "task157ee_factor_owner": {
                "P_order": q0["P_order"], "Q0_order": q0["Q0_order"],
                "split_word_sha256": digest(split_words),
                "complete_PSL_relators_sha256": digest(relators),
                "pure_S_split_word_indices_0_based": [0, 1],
            },
            "canonical_residual_action": residual["public"],
            "C_rel": c_rel,
            "claim_boundary": {
                "C_rel_basis_computed": True, "full_K_used_as_C_rel": False,
                "occurrence_image": False, "A_over_JA": False, "L_over_JL": False,
                "compatible_lift": False, "fake": False, "Ihara_witness": False,
            },
            "resource_caps": {
                "A4_input_bytes_each": MAX_A4_BYTES, "output_bytes": MAX_OUTPUT_BYTES,
                "Gamma_raw_bytes": MAX_GAMMA_RAW_BYTES, "K_rank": MAX_K_RANK,
                "literal_letters_each": MAX_LITERAL_LETTERS,
                "frozen_runtime": meter.public(),
            },
            "checkpoint": None,
        }
        atomic_write(output, seal(body))
        terminal = PASS
    except InputStop as exc:
        reason = UNKNOWN_INPUT + ":" + str(exc).replace(" ", "_")
        terminal = UNKNOWN_INPUT
        if output is not None and not output.exists():
            atomic_write(output, terminal_receipt(UNKNOWN_INPUT, reason))
    except ResourceStop as exc:
        reason = UNKNOWN_RESOURCE + ":" + str(exc).replace(" ", "_")
        terminal = UNKNOWN_RESOURCE
        if output is not None and not output.exists():
            atomic_write(output, terminal_receipt(UNKNOWN_RESOURCE, reason))
    except Exception as exc:
        name = exc.__class__.__name__
        status = UNKNOWN_RESOURCE if name in {"ResourceStop", "HardStop"} else UNKNOWN_INPUT
        reason = status + ":FROZEN_OWNER_" + name + ":" + str(exc).replace(" ", "_")
        terminal = status
        if output is not None and not output.exists():
            atomic_write(output, terminal_receipt(status, reason))
    print(PREFIX + " " + terminal, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
