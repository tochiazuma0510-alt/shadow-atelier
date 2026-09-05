#!/usr/bin/env python3
"""Task983: independent one-root eleven-slot and PB4-dropped grade consumer.

The input node grammar is authenticated separately from endpoint/Fox arithmetic.
The original fresh rho2 is an actual input, never a DERIVED replacement.
"""
from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import signal
import stat
import sys
import tempfile
import time
from typing import Any, Iterable

import numpy as np

REPOSITORY = Path(__file__).resolve().parents[1]
RETAINED_PINS = {
    "search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v9.py":
        (113012, "7b2beb39dbdc65494f85fa4451ed69d99a22685d11f1d4fef6e671322d24098d"),
    "search/check_d972_r07_grade2_forward_adjoint_maps_v4.py":
        (49643, "7ba94ee884db49bbe42d11a84228a6bdf7c88a3918407928af90c71b65fe4a29"),
}
DATA_PINS = {
    "ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json":
        (231570, "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "scratchpad/fuda1_a0_rmax_data.g":
        (4709, "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba"),
    "scratchpad/a0_paper_words_v1.json":
        (115928, "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893"),
    "scratchpad/a0_v2_words.json":
        (106133, "fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612"),
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


for _name, (_size, _digest) in RETAINED_PINS.items():
    _path = REPOSITORY / _name
    if _path.is_symlink() or _path.stat().st_size != _size or sha(_path.read_bytes()) != _digest:
        raise ValueError("same_word:retained_checker_pin:" + _name)
import check_d972_r07_a0_fresh_precision2_endpoint_signature_v9 as ENDPOINT
import check_d972_r07_grade2_forward_adjoint_maps_v4 as MAPS

SCHEMA = "d972.r07.continuation-same-word-eleven-slots.v1"
WORD_SCHEMA = "d972.r07.continuation-positive-word.v1"
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
OCCURRENCES = (
    (1, "H1_fxy", 1, 1, 0), (2, "H1_fxz", 1, -1, 1), (3, "H1_fyz", 1, 1, 2),
    (4, "H2_fux", 2, -1, 3), (5, "H2_fxy", 2, -1, 0), (6, "H2_fuy", 2, 1, 4),
    (7, "P_b1", 3, 1, 5), (8, "P_b2", 3, 1, 6), (9, "P_b3", 3, 1, 7),
    (10, "P_b5_inverse", 3, -1, 8), (11, "P_b4_inverse", 3, -1, 9),
)
PRINTED_NATIVE = {1: ((3, 1), (2, -1), (1, 1)),
                  2: ((6, 1), (5, -1), (4, -1)),
                  3: ((11, -1), (10, -1), (9, 1), (8, 1), (7, 1))}
STARTED = time.monotonic()
DEADLINE: float | None = None
MAX_RSS_BYTES = 7 * 1024**3
LAST_PHASE = "initialization"


class ResourceStop(Exception):
    pass


def require(condition: Any, label: str) -> None:
    if not condition:
        raise ValueError("same_word:" + label)


def boundary(phase: str, **fields: Any) -> None:
    global LAST_PHASE
    LAST_PHASE = phase
    if DEADLINE is not None and time.monotonic() >= DEADLINE:
        raise ResourceStop(phase)
    try:
        import resource
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024 > MAX_RSS_BYTES:
            raise ResourceStop("memory:" + phase)
    except ImportError:
        pass
    if fields:
        print(json.dumps({"phase": phase, **fields}, sort_keys=True), file=sys.stderr, flush=True)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def sealed(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    value = {"schema": SCHEMA + "." + kind, **copy.deepcopy(body)}
    require("sha256" not in value, "new_seal_has_no_existing_hash")
    return {**value, "sha256": sha(canonical(value))}


def integer(value: Any, label: str, lower: int | None = None, upper: int | None = None) -> int:
    require(type(value) is int and (lower is None or value >= lower) and
            (upper is None or value <= upper), label)
    return value


Element = tuple[bytes, bytes]
FoxRow = dict[tuple[int, Element], int]


@dataclass(frozen=True)
class FoxValue:
    endpoint: Element
    row: FoxRow


class TypedFox:
    """General LEFT Fox arithmetic; input dictionaries are never modified."""

    def __init__(self, quotient: Any, block: int):
        self.q = quotient
        self.block = integer(block, "typed_block", 1, 3)
        self.degree, self.pc_width, self.components = (36, 4, 3) if block < 3 else (144, 10, 6)
        require(quotient.degree == self.degree and quotient.pc.n == self.pc_width and
                len(quotient.generators) == self.components, "typed_marked_quotient_shape")

    def blob(self, value: Element) -> bytes:
        require(type(value) is tuple and len(value) == 2 and type(value[0]) is bytes and type(value[1]) is bytes,
                "typed_element_parts")
        permutation, pc = value
        require(len(permutation) == self.degree and set(permutation) == set(range(self.degree)) and
                len(pc) == self.pc_width and all(x < 3 for x in pc), "typed_element_width_permutation_pc")
        return permutation + pc

    def unblob(self, raw: bytes) -> Element:
        require(type(raw) is bytes and len(raw) == self.degree + self.pc_width, "typed_blob_exact_E3_E4_width")
        value = raw[:self.degree], raw[self.degree:]
        require(self.blob(value) == raw, "typed_blob_roundtrip")
        return value

    def identity(self) -> FoxValue:
        return FoxValue(self.q.identity, {})

    def literal_pb(self, word: Iterable[int]) -> FoxValue:
        letters = tuple(word)
        require(all(type(x) is int and 1 <= abs(x) <= self.components for x in letters), "literal_PB_letters")
        row, endpoint = ENDPOINT.cfox(letters, self.q)
        boundary("literal_PB_Fox")
        return FoxValue(endpoint, row)

    def translate_add(self, target: FoxRow, source: FoxRow, actor: Element, scalar: int) -> None:
        scalar %= 3
        if not scalar:
            return
        for index, ((component, value), coefficient) in enumerate(source.items()):
            key = component, self.q.mul(actor, value)
            total = (target.get(key, 0) + scalar * coefficient) % 3
            if total:
                target[key] = total
            else:
                target.pop(key, None)
            if index % 2048 == 0:
                boundary("general_LEFT_Fox_translation")

    def product(self, left: FoxValue, right: FoxValue) -> FoxValue:
        row = dict(left.row)
        self.translate_add(row, right.row, left.endpoint, 1)
        return FoxValue(self.q.mul(left.endpoint, right.endpoint), row)

    def inverse(self, value: FoxValue) -> FoxValue:
        inverse = self.q.inverse(value.endpoint)
        row: FoxRow = {}
        self.translate_add(row, value.row, inverse, -1)
        return FoxValue(inverse, row)

    def power(self, value: FoxValue, exponent: int) -> FoxValue:
        integer(exponent, "ordinary_integer_power")
        if exponent < 0:
            value, exponent = self.inverse(value), -exponent
        result = self.identity()
        while exponent:
            boundary("integer_power_binary")
            if exponent & 1:
                result = self.product(result, value)
            exponent >>= 1
            if exponent:
                value = self.product(value, value)
        return result

    def conjugate(self, actor: FoxValue, child: FoxValue) -> FoxValue:
        # This formula remains valid when the actual slot endpoint of child is nonunit.
        endpoint = self.q.mul(self.q.mul(actor.endpoint, child.endpoint), self.q.inverse(actor.endpoint))
        row = dict(actor.row)
        self.translate_add(row, child.row, actor.endpoint, 1)
        self.translate_add(row, actor.row, endpoint, -1)
        return FoxValue(endpoint, row)

    def row_records(self, row: FoxRow) -> list[list[Any]]:
        values = []
        for (component, element), coefficient in row.items():
            integer(component, "typed_Fox_component", 1, self.components)
            integer(coefficient, "canonical_nonzero_F3", 1, 2)
            values.append([component, self.blob(element).hex(), coefficient])
        return sorted(values, key=lambda item: (item[0], item[1]))

    def row_from_records(self, records: Any) -> FoxRow:
        require(type(records) is list, "typed_Fox_records")
        row = {}
        for record in records:
            require(type(record) is list and len(record) == 3 and type(record[1]) is str, "typed_Fox_record")
            component = integer(record[0], "typed_Fox_component", 1, self.components)
            coefficient = integer(record[2], "typed_Fox_coefficient", 1, 2)
            key = component, self.unblob(bytes.fromhex(record[1]))
            require(key not in row, "typed_Fox_duplicate_key")
            row[key] = coefficient
        require(records == self.row_records(row), "typed_Fox_canonical_order")
        return row


class CoarseReadout:
    """E3 coarse permutation -> v443 section-left/kernel-right Q2 coordinates."""

    def __init__(self, arithmetic: TypedFox, context: Any):
        require(arithmetic.block in (1, 2), "E3_readout_only")
        self.arithmetic, self.context = arithmetic, context
        self.cache: dict[bytes, Any] = {}

    def decode(self, element: Element) -> Any:
        raw = self.arithmetic.blob(element)
        permutation = raw[:36]
        if permutation in self.cache:
            return self.cache[permutation]
        p = tuple(permutation[:9])
        require(p in self.context.psl_index, "E3_PSL_matching")
        signs, translations = [], []
        for block in range(3):
            begin = 9 + 9 * block
            values = tuple(permutation[begin + i] - begin for i in range(9))
            translation = values[0]
            sign = (values[1] - translation) % 9
            require(sign in (1, 8) and values == tuple((sign * i + translation) % 9 for i in range(9)),
                    "E3_full_nine_point_signed_affine_block")
            signs.append(sign); translations.append(translation)
        require(signs[2] == signs[0] * signs[1] % 9, "E3_three_signs_same_parity")
        value = p, int(signs[1] == 8), int(signs[0] == 8), tuple(x % 3 for x in translations)
        if len(self.cache) >= 8192:
            self.cache.clear()
        self.cache[permutation] = value
        return value

    def normal(self, row: FoxRow) -> tuple[dict[tuple[int, Any], int], int]:
        result: dict[tuple[int, Any], int] = {}
        augmentation = 0
        a, c = self.context.aimages
        b = MAPS.ainverse(MAPS.amul(c, a))
        for index, ((component, element), coefficient) in enumerate(row.items()):
            integer(component, "PB3_normal_component", 1, 3)
            h = self.decode(element)
            if component == 1:
                augmentation = (augmentation + coefficient) % 3
                ha = MAPS.amul(h, a)
                terms = ((0, ha, -coefficient), (1, MAPS.amul(ha, b), -coefficient))
            else:
                terms = ((component - 2, h, coefficient),)
            for target_component, value, scalar in terms:
                key = target_component, value
                total = (result.get(key, 0) + scalar) % 3
                if total:
                    result[key] = total
                else:
                    result.pop(key, None)
            if index % 2048 == 0:
                boundary("typed_PB3_normal_readout")
        return result, augmentation


class IndependentFloor:
    def __init__(self):
        boundary("independent_marked_floor")
        self.data = {}
        for name, (size, digest) in DATA_PINS.items():
            item = REPOSITORY / name
            raw = item.read_bytes()
            require(not item.is_symlink() and len(raw) == size and sha(raw) == digest, "raw_context_pin:" + name)
            self.data[name] = raw
        q3 = json.loads(self.data["ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json"])
        class OnlyQ3:
            def json(self, key: str) -> Any:
                require(key == "q3", "independent_light_Q3_only")
                return q3
        self.runtime = ENDPOINT.build_checker_light(OnlyQ3())
        self.model = self.runtime["model"]
        self.words = json.loads(self.data["scratchpad/a0_paper_words_v1.json"])
        self.maps = MAPS.IndependentContext(self.words)
        self.filtered = ENDPOINT.Context(self.words)
        require(tuple(self.filtered.psels) == self.maps.psl and self.filtered.transport == self.maps.transports and
                self.filtered.shifts == self.maps.shifts, "independent_context_PSL_transport_prefix_join")
        self.arithmetic = {block: TypedFox(self.runtime["e3" if block < 3 else "e4"], block) for block in (1, 2, 3)}
        self.coarse = CoarseReadout(self.arithmetic[1], self.maps)
        require(tuple(ENDPOINT.OCCURRENCE_LAYOUT) == OCCURRENCES and len(self.model.specs) == 11,
                "actual_eleven_occurrence_layout")
        for spec, expected in zip(self.model.specs, OCCURRENCES, strict=True):
            ordinal, label, block, sign, coordinate = expected
            require((spec["label"], spec["block"], spec["sign"], spec["coordinate"]) ==
                    (label, block, sign, coordinate), "actual_occurrence_owner")
            if ordinal <= 6:
                require(self.coarse.decode(spec["occurrence_prefix"]) == self.maps.shifts[ordinal - 1],
                        "actual_E3_prefix_to_Task712_affine_prefix")
        a, c = self.maps.aimages
        b = MAPS.ainverse(MAPS.amul(c, a))
        require([self.coarse.decode(value) for value in self.runtime["e3"].generators] == [a, b, c],
                "actual_marked_PB3_to_Q2_commuting_square")

    def literal(self, ordinal: int, word: Iterable[int]) -> FoxValue:
        integer(ordinal, "occurrence_ordinal", 1, 11)
        spec = self.model.specs[ordinal - 1]
        letters = tuple(word)
        require(all(type(x) is int and x in (-2, -1, 1, 2) for x in letters), "literal_F2_letters")
        pb_word = self.model._substitute(letters, spec["left"], spec["right"], spec["lift"])
        return self.arithmetic[spec["block"]].literal_pb(pb_word)

    def source_arrays(self, ordinal: int, row: FoxRow) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
        integer(ordinal, "six_source_occurrence", 1, 6)
        normal, augmentation = self.coarse.normal(row)
        tag = ordinal - 1
        d0, d1, d2 = np.zeros((4, 2, 504), dtype=np.uint8), np.zeros((4, 2, 3, 504), dtype=np.uint8), np.zeros((4, 2, 6, 504), dtype=np.uint8)
        for (component, value), coefficient in normal.items():
            polynomial = ENDPOINT.e_poly(value[3])
            psl = self.maps.psl_index[value[0]]
            for character, label in enumerate(CHARACTERS):
                weight = coefficient * MAPS.character_sign(self.maps.transports[tag][label], (value[1], value[2]))
                d0[character, component, psl] = (int(d0[character, component, psl]) + weight * int(polynomial[0])) % 3
                d1[character, component, :, psl] = (d1[character, component, :, psl].astype(np.int16) + weight * polynomial[1:4]) % 3
                d2[character, component, :, psl] = (d2[character, component, :, psl].astype(np.int16) + weight * polynomial[4:]) % 3
        return d0, d1, d2, augmentation

    def direct_physical(self, block_rows: dict[int, FoxRow], normalized_pair: list[int]) -> tuple[np.ndarray, np.ndarray]:
        require(set(block_rows) == {1, 2} and len(normalized_pair) == 2 and
                all(type(x) is int and x in (0, 1, 2) for x in normalized_pair), "PB4_dropped_codomain_and_normalized_pair")
        out = np.zeros((4, 2, 2, 10, 504), dtype=np.uint8)
        auxiliary = np.zeros(4, dtype=np.uint8)
        for block in (1, 2):
            normal, augmentation = self.coarse.normal(block_rows[block])
            auxiliary[block - 1] = augmentation
            for index, ((component, value), coefficient) in enumerate(normal.items()):
                polynomial = ENDPOINT.e_poly(value[3])
                psl = self.maps.psl_index[value[0]]
                for character, label in enumerate(CHARACTERS):
                    weight = coefficient * MAPS.character_sign(label, (value[1], value[2]))
                    old = out[character, block - 1, component, :, psl].astype(np.int16)
                    out[character, block - 1, component, :, psl] = (old + weight * polynomial) % 3
                if index % 2048 == 0:
                    boundary("direct_filtered_physical_PB4_dropped")
        auxiliary[2:] = normalized_pair
        lower = np.concatenate((out[:, :, :, 0, :].reshape(-1), out[:, :, :, 1:4, :].reshape(-1), auxiliary))
        top = out[:, :, :, 4:, :].reshape(-1).copy()
        require(lower.size == 32260 and top.size == 48384, "current_filtered_physical_exact_widths")
        return lower, top


NAMESPACES = frozenset(("p1", "old-defect", "conn-lower", "conn-raw", "physical", "raw-e", "tree", "normalizer", "target"))


def hash_string(value: Any, label: str) -> str:
    require(type(value) is str and len(value) == 64 and all(x in "0123456789abcdef" for x in value), label)
    return value


def exact_json(raw: bytes, label: str) -> Any:
    value = json.loads(raw)
    require(canonical(value) == raw, "canonical_JSON:" + label)
    return value


def relative_file(root: Path, name: str) -> Path:
    require(type(name) is str and name and "\\" not in name and ":" not in name, "relative_file_name")
    parts = PurePosixPath(name)
    require(not parts.is_absolute() and parts.as_posix() == name and all(x not in ("", ".", "..") for x in parts.parts),
            "relative_file_canonical_path")
    require(root.is_dir() and not root.is_symlink(), "input_root_directory")
    target = root
    for component in parts.parts:
        target = target / component
        require(not target.is_symlink(), "input_path_no_symlink")
    require(target.is_file() and root.resolve() in target.resolve().parents, "input_regular_contained_file")
    return target


def node_children(value: dict[str, Any]) -> list[dict[str, Any]]:
    op, args = value["op"], value["args"]
    if op == "Act":
        return [args["conjugator"], args["word"]]
    if op == "OrderedProduct":
        return args["factors"]
    if op in ("Inverse", "IntegerPower", "Ref"):
        return [args["word"]]
    return []


class NodeCatalog:
    """Authenticate all JSONL bytes; retain offsets and liveness, not expanded words."""

    def __init__(self, item: Path, descriptor: dict[str, Any], root_id: int, root_hash: str,
                 dictionary_hash: str, relators: dict[str, list[int]], ancestor_entries: list[dict[str, Any]]):
        require(set(descriptor) == {"file", "bytes", "sha256", "nodes"} and descriptor["file"] == "ordered-word.jsonl",
                "nodes_file_descriptor")
        integer(descriptor["bytes"], "nodes_file_bytes", 1)
        integer(descriptor["nodes"], "nodes_file_count", 1)
        hash_string(descriptor["sha256"], "nodes_file_hash")
        self.item, self.descriptor = item, copy.deepcopy(descriptor)
        self.root_id = integer(root_id, "single_root_id", 0, descriptor["nodes"] - 1)
        self.root_hash = hash_string(root_hash, "single_root_node_hash")
        self.dictionary_hash, self.relators = dictionary_hash, relators
        self.ancestors = ancestor_entries
        self.offsets: list[tuple[int, int]] = []
        self.hashes: list[str] = []
        self.children: list[tuple[int, ...]] = []
        self.uses: list[int] = []
        self.symbols: dict[tuple[str, str, str], int] = {}
        require(item.is_file() and not item.is_symlink(), "nodes_input_file")
        full_hash, offset = hashlib.sha256(), 0
        with item.open("rb") as stream:
            while True:
                raw = stream.readline()
                if not raw:
                    break
                boundary("authenticate_ordered_nodes")
                number = len(self.hashes)
                if number % 1024 == 0:
                    boundary("authenticate_ordered_nodes", nodes=number)
                require(number < descriptor["nodes"], "nodes_after_declared_EOF")
                value = exact_json(raw, "node")
                self.validate_node(value, number)
                children = tuple(child["node"] for child in node_children(value))
                for child in children:
                    self.uses[child] += 1
                self.offsets.append((offset, len(raw)))
                self.hashes.append(value["node_sha256"])
                self.children.append(children)
                self.uses.append(0)
                full_hash.update(raw); offset += len(raw)
        require(offset == item.stat().st_size == descriptor["bytes"] and full_hash.hexdigest() == descriptor["sha256"] and
                len(self.hashes) == descriptor["nodes"] and self.hashes[self.root_id] == self.root_hash,
                "nodes_full_bytes_count_EOF_and_root")
        reachable, todo = set(), [self.root_id]
        while todo:
            node = todo.pop()
            if node not in reachable:
                reachable.add(node); todo.extend(self.children[node])
        require(len(reachable) == len(self.hashes), "all_literal_nodes_reachable_including_zero_power_edges")

    def validate_node(self, value: Any, number: int) -> None:
        require(type(value) is dict and set(value) == {"id", "type", "op", "args", "receipt_refs", "node_sha256"},
                "node_exact_six_fields")
        require(integer(value["id"], "continuous_node_id", 0) == number and value["type"] == "F2-word", "node_identity_and_type")
        require(type(value["receipt_refs"]) is list and all(type(x) is int and 0 <= x < len(self.ancestors)
                for x in value["receipt_refs"]), "node_receipt_refs_ordered_ids")
        args, op = value["args"], value["op"]
        fields = {"Identity": set(), "Letter": {"letter"},
            "Rel": {"dictionary_sha256", "relator_id", "letters", "letters_sha256"},
            "Act": {"conjugator", "word", "orientation"}, "OrderedProduct": {"factors"},
            "Inverse": {"word"}, "IntegerPower": {"word", "exponent"},
            "Ref": {"namespace", "key", "scope_sha256", "word"}}
        require(type(op) is str and op in fields and type(args) is dict and set(args) == fields[op], "node_op_exact_args")
        if op == "Letter":
            require(type(args["letter"]) is int and args["letter"] in (-2, -1, 1, 2), "literal_letter_integer")
        elif op == "Rel":
            name = args["relator_id"]
            require(type(name) is str and name in self.relators and args["dictionary_sha256"] == self.dictionary_hash,
                    "Rel_exact_bound_dictionary_and_ID")
            require(type(args["letters"]) is list and all(type(x) is int and x in (-2, -1, 1, 2) for x in args["letters"]) and
                    args["letters"] == self.relators[name] and args["letters_sha256"] == sha(canonical(args["letters"])),
                    "Rel_literal_letters_and_hash")
        elif op == "Act":
            require(args["orientation"] == "P*W*P^-1", "Act_literal_orientation")
        elif op == "OrderedProduct":
            require(type(args["factors"]) is list, "ordered_product_factor_array")
        elif op == "IntegerPower":
            integer(args["exponent"], "ordinary_power_exponent_not_F3")
        elif op == "Ref":
            require(type(args["namespace"]) is str and args["namespace"] in NAMESPACES and
                    type(args["key"]) is str and args["key"], "typed_Ref_symbol")
            scope = hash_string(args["scope_sha256"], "typed_Ref_scope_hash")
            symbol = args["namespace"], args["key"], scope
            require(symbol not in self.symbols, "typed_symbol_emitted_once")
            self.symbols[symbol] = number
            require((args["namespace"] == "normalizer" and scope == self.dictionary_hash) or any(entry["namespace"] == args["namespace"] and scope in
                (entry["parent_manifest_sha256"], entry["file_sha256"])
                for entry in (self.ancestors[x] for x in value["receipt_refs"])), "Ref_bound_to_actual_ancestor_scope")
        for child in node_children(value):
            require(type(child) is dict and set(child) == {"node", "sha256"}, "prior_child_exact_type")
            index = integer(child["node"], "prior_only_child_ID", 0, number - 1)
            require(child["sha256"] == self.hashes[index], "prior_child_same_node_hash")
        hash_string(value["node_sha256"], "node_seal_shape")
        require(value["node_sha256"] == sha(canonical({key: item for key, item in value.items() if key != "node_sha256"})),
                "node_canonical_seal")

    def read(self, stream: Any, number: int) -> dict[str, Any]:
        offset, length = self.offsets[number]
        stream.seek(offset)
        raw = stream.read(length)
        require(len(raw) == length, "positioned_node_EOF")
        value = exact_json(raw, "positioned-node")
        require(value["id"] == number and value["node_sha256"] == self.hashes[number] and
                sha(canonical({key: item for key, item in value.items() if key != "node_sha256"})) == self.hashes[number],
                "positioned_node_unchanged")
        return value

    def normalized_pair(self) -> dict[str, Any]:
        live: dict[int, tuple[int, int]] = {}
        remaining = self.uses.copy()
        with self.item.open("rb") as stream:
            for number in range(len(self.hashes)):
                value = self.read(stream, number); op, args = value["op"], value["args"]
                if op in ("Identity", "Letter", "Rel"):
                    letters = () if op == "Identity" else (args["letter"],) if op == "Letter" else args["letters"]
                    result = (sum(1 if x == 1 else -1 if x == -1 else 0 for x in letters) % 54,
                              sum(1 if x == 2 else -1 if x == -2 else 0 for x in letters) % 54)
                elif op == "OrderedProduct":
                    result = tuple(sum(live[child["node"]][i] for child in args["factors"]) % 54 for i in range(2))
                else:
                    child = live[args["word"]["node"]]
                    factor = -1 if op == "Inverse" else args["exponent"] if op == "IntegerPower" else 1
                    result = tuple(factor * item % 54 for item in child)
                live[number] = result
                for child in self.children[number]:
                    remaining[child] -= 1
                    if remaining[child] == 0 and child != self.root_id:
                        del live[child]
                boundary("same_root_integer_mod54")
        require(set(live) == {self.root_id} and not any(remaining), "integer_dependency_EOF_and_lifetime")
        residues = list(live[self.root_id])
        divisible = [value in (0, 18, 36) for value in residues]
        return {"same_root_id": self.root_id, "same_root_sha256": self.root_hash, "modulus": 54,
            "residue_type": "integer-residue-0-to-53", "exponent_residues": residues, "divisible18": divisible,
            "normalized_pair": [value // 18 for value in residues] if all(divisible) else None, "eof": True}

    def evaluate_slot(self, floor: IndependentFloor, ordinal: int) -> FoxValue:
        spec = floor.model.specs[integer(ordinal, "slot_ordinal", 1, 11) - 1]
        arithmetic = floor.arithmetic[spec["block"]]
        remaining = self.uses.copy()
        live: dict[int, FoxValue] = {}
        with self.item.open("rb") as stream:
            for number in range(len(self.hashes)):
                value = self.read(stream, number); op, args = value["op"], value["args"]
                if op == "Identity":
                    result = arithmetic.identity()
                elif op in ("Letter", "Rel"):
                    result = floor.literal(ordinal, (args["letter"],) if op == "Letter" else args["letters"])
                elif op == "Act":
                    result = arithmetic.conjugate(live[args["conjugator"]["node"]], live[args["word"]["node"]])
                elif op == "OrderedProduct":
                    result = arithmetic.identity()
                    for child in args["factors"]:
                        result = arithmetic.product(result, live[child["node"]])
                elif op == "Inverse":
                    result = arithmetic.inverse(live[args["word"]["node"]])
                elif op == "IntegerPower":
                    result = arithmetic.power(live[args["word"]["node"]], args["exponent"])
                else:
                    require(op == "Ref", "no_hidden_word_evaluator")
                    result = live[args["word"]["node"]]
                live[number] = result
                for child in self.children[number]:
                    remaining[child] -= 1
                    if remaining[child] == 0 and child != self.root_id:
                        del live[child]
                if number % 256 == 0:
                    boundary("one_slot_general_DAG", ordinal=ordinal, nodes=number + 1, live_nodes=len(live))
        require(set(live) == {self.root_id} and not any(remaining), "slot_dependency_EOF_and_lifetime")
        return live[self.root_id]


class OutputFiles:
    def __init__(self, root: Path):
        require(not root.exists(), "output_must_be_new")
        root.mkdir(parents=True)
        self.root, self.files = root.resolve(), {}

    def destination(self, name: str) -> Path:
        parts = PurePosixPath(name)
        require(parts.as_posix() == name and not parts.is_absolute() and
                all(x not in ("", ".", "..") for x in parts.parts) and name not in self.files,
                "new_output_name")
        target = self.root.joinpath(*parts.parts)
        require(not target.exists(), "output_no_overwrite")
        target.parent.mkdir(parents=True, exist_ok=True)
        return target

    def record(self, name: str, raw: bytes, **metadata: Any) -> dict[str, Any]:
        self.destination(name).write_bytes(raw)
        result = {"file": name, "bytes": len(raw), "sha256": sha(raw), **metadata}
        self.files[name] = result
        return copy.deepcopy(result)

    def json(self, name: str, value: Any) -> dict[str, Any]:
        return self.record(name, canonical(value))

    def trits(self, name: str, values: np.ndarray) -> dict[str, Any]:
        require(values.dtype == np.uint8 and not np.any(values > 2), "dense_trit_output")
        return self.record(name, values.tobytes(), dtype="u8-trit", shape=list(values.shape), eof=True)

    def fox(self, name: str, arithmetic: TypedFox, row: FoxRow) -> dict[str, Any]:
        target = self.destination(name)
        digest, size, count = hashlib.sha256(), 0, 0
        with target.open("xb") as stream:
            for (component, value), coefficient in sorted(row.items(), key=lambda item: (item[0][0], item[0][1])):
                require(type(component) is int and 1 <= component <= arithmetic.components and
                        type(coefficient) is int and coefficient in (1, 2), "Fox_output_term_type")
                raw = canonical([component, arithmetic.blob(value).hex(), coefficient])
                stream.write(raw); digest.update(raw); size += len(raw); count += 1
                if count % 2048 == 0:
                    boundary("write_complete_typed_Fox_row")
        result = {"file": name, "bytes": size, "sha256": digest.hexdigest(), "terms": count,
            "encoding": "component-typed-element-hex-F3-jsonl", "element_bytes": arithmetic.degree + arithmetic.pc_width,
            "components": arithmetic.components, "eof": True}
        self.files[name] = result
        return copy.deepcopy(result)


def row_difference(arithmetic: TypedFox, left: FoxRow, right: FoxRow) -> FoxRow:
    result = left.copy()
    arithmetic.translate_add(result, right, arithmetic.q.identity, -1)
    return result


def same_word_eleven(floor: IndependentFloor, catalog: NodeCatalog, output: OutputFiles,
                     normalized_pair: list[int] | None, word_manifest_sha256: str) -> dict[str, Any]:
    """One slot at a time, with independent printed-product and prefix paths."""
    d0 = np.zeros((4, 6, 2, 504), dtype=np.uint8)
    d1 = np.zeros((4, 6, 2, 3, 504), dtype=np.uint8)
    d2 = np.zeros((4, 6, 2, 6, 504), dtype=np.uint8)
    auxiliary = np.zeros(8, dtype=np.uint8)
    slots, blocks, direct_hexagons = {}, [], {}
    all_endpoints_one = True
    for block in (1, 2, 3):
        arithmetic = floor.arithmetic[block]
        old_printed, new_printed = arithmetic.identity(), arithmetic.identity()
        prefix_row: FoxRow = {}
        block_endpoints_one = True
        for ordinal, sign in PRINTED_NATIVE[block]:
            boundary("evaluate_one_actual_slot", ordinal=ordinal, block=block)
            spec = floor.model.specs[ordinal - 1]
            root = catalog.evaluate_slot(floor, ordinal)
            base = floor.literal(ordinal, floor.runtime["g760"])
            corrected = arithmetic.product(base, root)
            old_factor = base if sign == 1 else arithmetic.inverse(base)
            new_factor = corrected if sign == 1 else arithmetic.inverse(corrected)
            old_printed = arithmetic.product(old_printed, old_factor)
            new_printed = arithmetic.product(new_printed, new_factor)
            endpoint_one = root.endpoint == arithmetic.q.identity
            all_endpoints_one &= endpoint_one
            block_endpoints_one &= endpoint_one
            arithmetic.translate_add(prefix_row, root.row, spec["occurrence_prefix"], sign)
            row_receipt = output.fox(f"slots/{ordinal:02d}/unsigned-fox.jsonl", arithmetic, root.row)
            slot = sealed("slot", {"ordinal": ordinal, "label": spec["label"], "block": block,
                "coordinate": spec["coordinate"], "type": "E3" if block < 3 else "E4",
                "factor_sign": sign, "same_root_id": catalog.root_id, "same_root_sha256": catalog.root_hash,
                "word_manifest_sha256": word_manifest_sha256, "endpoint": arithmetic.blob(root.endpoint).hex(),
                "endpoint_one": endpoint_one, "fox_zero": not root.row, "unsigned_fox": row_receipt,
                "base_endpoint": arithmetic.blob(base.endpoint).hex(),
                "occurrence_prefix": arithmetic.blob(spec["occurrence_prefix"]).hex(), "eof": True})
            output.json(f"slots/{ordinal:02d}/receipt.json", slot)
            slots[ordinal] = slot
            if ordinal <= 6:
                d0[:, ordinal - 1], d1[:, ordinal - 1], d2[:, ordinal - 1], auxiliary[ordinal - 1] = floor.source_arrays(ordinal, root.row)
            del root, base, corrected, old_factor, new_factor
        require(old_printed.endpoint == arithmetic.q.identity, "actual_base_printed_endpoint")
        direct_row = row_difference(arithmetic, new_printed.row, old_printed.row)
        exact = direct_row == prefix_row
        if block_endpoints_one:
            require(new_printed.endpoint == arithmetic.q.identity and exact, "complete_direct_printed_equals_occurrence_sum")
        record = sealed("printed-block", {"block": block, "type": "E3" if block < 3 else "E4",
            "same_root_sha256": catalog.root_hash, "native_factor_order": [list(x) for x in PRINTED_NATIVE[block]],
            "old_endpoint": arithmetic.blob(old_printed.endpoint).hex(),
            "new_endpoint": arithmetic.blob(new_printed.endpoint).hex(),
            "all_slot_endpoints_one": block_endpoints_one,
            "direct_difference": output.fox(f"printed/{block}/direct-difference.jsonl", arithmetic, direct_row),
            "prefix_sum": output.fox(f"printed/{block}/prefix-sum.jsonl", arithmetic, prefix_row),
            "conditional_formula_applicable": block_endpoints_one, "direct_equals_prefix": exact,
            "PB4_in_current_physical_codomain": False, "unprojected_P_zero_required": False,
            "unprojected_P_zero_claimed": False, "eof": True})
        blocks.append(record); output.json(f"printed/{block}/receipt.json", record)
        if block < 3:
            direct_hexagons[block] = direct_row
        del old_printed, new_printed, prefix_row, direct_row
    require(set(slots) == set(range(1, 12)), "all_eleven_occurrences_preserved")
    require(slots[1]["endpoint"] == slots[5]["endpoint"] and
            slots[1]["unsigned_fox"]["sha256"] == slots[5]["unsigned_fox"]["sha256"] and
            slots[1]["block"] != slots[5]["block"] and slots[1]["factor_sign"] != slots[5]["factor_sign"],
            "duplicate_coordinate_zero_two_actual_occurrences")
    slot_manifest = sealed("eleven-slots", {"word_manifest_sha256": word_manifest_sha256,
        "same_root_id": catalog.root_id, "same_root_sha256": catalog.root_hash,
        "slots": [slots[x] for x in range(1, 12)], "printed_blocks": blocks,
        "all_endpoint_one": all_endpoints_one, "typed_E3_bytes": 40, "typed_E4_bytes": 154,
        "full_P_zero_claimed": False, "eof": True})
    output.json("eleven-slots.json", slot_manifest)
    require(all_endpoints_one, "actual_same_word_all_eleven_endpoint_gate")
    if normalized_pair is None:
        return {"slots": slot_manifest, "normalized_pair_applicable": False}
    auxiliary[6:] = normalized_pair
    source = (d0.reshape(4, -1), d1.reshape(4, -1), d2.reshape(4, -1), auxiliary)
    source_lower = np.concatenate((source[0].reshape(-1), source[1].reshape(-1), auxiliary))
    require(source_lower.size == 96776, "source_lower_is_not_physical_lower")
    physical0, physical1, filtered_top, physical_aux = ENDPOINT.aggregate(floor.filtered, source)
    filtered_lower = np.concatenate((physical0, physical1, physical_aux))
    direct_lower, direct_top = floor.direct_physical(direct_hexagons, normalized_pair)
    require(np.array_equal(filtered_lower, direct_lower) and np.array_equal(filtered_top, direct_top),
            "same_root_full_filtered_32260_and_48384_equality")
    receipts = {"source_lower": output.trits("grade/source-lower.u8", source_lower),
        "source_top": output.trits("grade/source-top.u8", source[2]),
        "physical_lower": output.trits("grade/physical-lower.u8", direct_lower),
        "physical_top": output.trits("grade/physical-top.u8", direct_top)}
    require(direct_lower.size == 32260 and direct_top.size == 48384, "direct_current_codomain_widths")
    return {"slots": slot_manifest, "normalized_pair_applicable": True, "source": source,
        "source_lower": source_lower, "source_lower_zero": not np.any(source_lower),
        "physical_lower": direct_lower, "physical_top": direct_top, "payloads": receipts,
        "full_filtered_coordinates_compared": 80644, "source_lower_zero_required": False}


RHO2_MANIFEST = (26047, "55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488")
RHO2_VERDICT = (418, "cdf0654738a10acf59844df3b9dda5ab8efdf2e387bba7d69b691a4ad46b2848")
RHO2_PACKED_SHA = "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e"
TASK712_MANIFEST = (24277, "48c5d1f455e775cbcb3d887248de72d6bbda9df25deb5bafb8f02c8d121bdd47")
TASK712_WORKFLOW = (1034, "3fc967d6851b03bcb5c6d9c662c05a5c32d80028b698c925b313fa9ae9cc68c8")
TASK712_CHECKED = (1133, "3d9dc1a40c37a91d00b114f166128a08281badd1a4cb0735008cbd1b3e7b3160")
CEGAR_CHECKER_SHA = "e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3"
CEGAR_PRODUCER_SHA = "67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c"
CONTINUATION_WORKFLOWS = frozenset((
    ".github/workflows/d972-r07-complete-oracle-cegar-checker-completion-v1.yml",
    ".github/workflows/d972-r07-complete-oracle-cegar-resume64-v1.yml",
    ".github/workflows/d972-r07-complete-oracle-cegar-resume-next-v1.yml"))
CONTINUATION_ENTRY_PINS = {
    "owner": (8612, "e356f7d614828b9c466c70e4e446ec561de73a758b4c6a2292fdd97be39ff77b"),
    "source": (2423, "c787d53c65c6392845e6f26c545e213b6b17d9b08dc07d694a1c4e33282f2651"),
    "start": (54707, "87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b"),
}


def file_receipt(item: Path, name: str | None = None) -> dict[str, Any]:
    require(item.is_file() and not item.is_symlink() and not item.is_junction() and
            stat.S_ISREG(item.lstat().st_mode), "regular_file_receipt")
    digest, size = hashlib.sha256(), 0
    with item.open("rb") as stream:
        while chunk := stream.read(8 << 20):
            digest.update(chunk); size += len(chunk)
            boundary("authenticate_complete_file")
    require(item.stat().st_size == size, "file_size_stable")
    return {"file": item.name if name is None else name, "bytes": size, "sha256": digest.hexdigest()}


def pinned_json(item: Path, pin: tuple[int, str], label: str) -> tuple[Any, bytes]:
    require(item.is_file() and not item.is_symlink(), "pinned_json_file:" + label)
    raw = item.read_bytes()
    require((len(raw), sha(raw)) == pin, "pinned_json_bytes:" + label)
    return exact_json(raw, label), raw


def seal_check(value: Any, schema: str, label: str) -> dict[str, Any]:
    require(type(value) is dict and value.get("schema") == schema and type(value.get("sha256")) is str and
            value["sha256"] == sha(canonical({key: part for key, part in value.items() if key != "sha256"})), label)
    return value


def descriptor_check(value: Any, label: str) -> dict[str, Any]:
    require(type(value) is dict and set(value) == {"file", "bytes", "sha256"} and type(value["file"]) is str, label)
    integer(value["bytes"], label + ":bytes", 0)
    hash_string(value["sha256"], label + ":sha256")
    return value


def packed_trits(raw: bytes, count: int, label: str) -> np.ndarray:
    require(type(count) is int and count >= 0 and len(raw) == (count + 3) // 4, label + ":packed_width")
    values = np.frombuffer(raw, dtype=np.uint8)
    require(not np.any(values > 80), label + ":base3_byte")
    expanded = np.empty((len(values), 4), dtype=np.uint8)
    for column, divisor in enumerate((1, 3, 9, 27)):
        expanded[:, column] = values // divisor % 3
    flat = expanded.reshape(-1)
    require(not np.any(flat[count:]), label + ":zero_unused_trits")
    return flat[:count].copy()


def original_rho2(root: Path) -> dict[str, Any]:
    manifest, manifest_raw = pinned_json(relative_file(root, "task640-payload/manifest.json"), RHO2_MANIFEST, "fresh_rho2_manifest")
    verdict, verdict_raw = pinned_json(relative_file(root, "task640-verdict.json"), RHO2_VERDICT, "fresh_rho2_verdict")
    require(manifest["schema"] == "d972.r07.a0.fresh-precision2-endpoint-signature.v9" and
            manifest["root"] == "Compose(C_<1,C_T)" and
            manifest["source_ancestry_sha256"] == "315f9d9be5c7301b7b54ca5f545a17ca1d491f2d1d24e40f426ce831388f2908" and
            manifest["dimensions"] == {"lower": 32260, "top": 48384, "packed_rho2": 12096}, "fresh_rho2_owner_dimensions")
    require(manifest["occurrence"]["count"] == 11 and manifest["occurrence"]["types"] == ["E3"] * 6 + ["E4"] * 5 and
            manifest["occurrence"]["coordinates"] == [record[4] for record in OCCURRENCES] and
            manifest["occurrence"]["signs"] == [record[3] for record in OCCURRENCES] and
            manifest["occurrence"]["all_seven_canary"] is True and manifest["occurrence"]["first_six_typed_restriction"] is True,
            "fresh_rho2_exact_occurrences")
    expected = {"lower_dense", "path_signatures", "rho2_dense", "rho2_packed", "roots", "signature_buckets", "target_dense"}
    require(type(manifest["files"]) is dict and set(manifest["files"]) == expected, "fresh_rho2_complete_seven_payloads")
    for descriptor in manifest["files"].values():
        descriptor_check(descriptor, "fresh_rho2_payload")
        item = relative_file(root, "task640-payload/" + descriptor["file"])
        require(file_receipt(item, descriptor["file"]) == descriptor, "fresh_rho2_actual_payload_bytes")
    def body(key: str) -> bytes:
        return relative_file(root, "task640-payload/" + manifest["files"][key]["file"]).read_bytes()
    packed, dense_raw, lower_raw, target_raw = body("rho2_packed"), body("rho2_dense"), body("lower_dense"), body("target_dense")
    dense = packed_trits(packed, 48384, "fresh_rho2")
    require(sha(packed) == RHO2_PACKED_SHA and dense.tobytes() == dense_raw and len(lower_raw) == 32260 and
            not any(lower_raw) and target_raw == lower_raw + dense_raw, "fresh_rho2_complete_dense_packed_target_join")
    roots = exact_json(body("roots"), "fresh_rho2_roots")
    require(roots["C_1"] == {"type": "Compose", "left": "C_<1", "right": "C_T"} and
            manifest["roots_sha256"] == manifest["files"]["roots"]["sha256"], "fresh_rho2_original_root_identity")
    require(verdict["marker"] == "R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CHECKER_PASS" and
            verdict["payload_manifest_sha256"] == sha(manifest_raw) and verdict["rho2_sha256"] == sha(packed) and
            verdict["lower_coordinates_checked"] == 32260 and verdict["top_coordinates_checked"] == 48384,
            "fresh_rho2_successful_checker_metadata")
    return {"manifest": manifest, "manifest_sha256": sha(manifest_raw), "verdict_sha256": sha(verdict_raw),
        "packed_sha256": sha(packed), "dense": dense, "original_body_directly_read": True,
        "old_signature_buckets_recomputed": False}


def task712_B_tables(root: Path, floor: IndependentFloor) -> dict[str, Any]:
    data, envelope = root / "r07-grade2-maps-v4", root
    require(data.is_dir() and not data.is_symlink() and not data.is_junction(), "task712_actual_data_directory")
    manifest, raw = pinned_json(relative_file(data, "manifest.json"), TASK712_MANIFEST, "task712_manifest")
    workflow, workflow_raw = pinned_json(relative_file(envelope, "r07-grade2-maps-v4-receipt.json"), TASK712_WORKFLOW, "task712_workflow")
    checked, checked_raw = pinned_json(relative_file(envelope, "r07-grade2-maps-v4-checker.json"), TASK712_CHECKED, "task712_checked")
    require(manifest["schema"] == MAPS.SCHEMA and manifest["prefix_shifts"] == floor.maps.prefix_record() and
            manifest["word_input"]["sha256"] == DATA_PINS["scratchpad/a0_paper_words_v1.json"][1] and
            manifest["marking_input"]["sha256"] == DATA_PINS["scratchpad/fuda1_a0_rmax_data.g"][1], "Task712_actual_context_owner")
    MAPS.validate_manifest_fixed_fields(manifest)
    require(checked["checker_sha256"] == RETAINED_PINS["search/check_d972_r07_grade2_forward_adjoint_maps_v4.py"][1] and
            checked["producer_manifest_sha256"] == sha(raw) and workflow["checker_result_sha256"] == sha(checked_raw) and
            workflow["manifest_sha256"] == sha(raw), "Task712_existing_independent_checker_lineage")
    tables, receipts = [], []
    by_name = {record["file"]: record for record in manifest["tables"]}
    require(len(by_name) == 40 and manifest["table_roster"] == MAPS.expected_roster()[2:], "Task712_full_roster_owner")
    for character in range(4):
        name = f"B_fwd_a{character}.jsonl"
        receipt = by_name[name]
        require(receipt["character"] == character and receipt["map_kind"] == "B" and receipt["map_direction"] == "forward",
                "Task712_forward_B_role")
        expected = sorted(MAPS.aggregation_records(floor.maps, character))
        tables.append(MAPS.parse_exact(relative_file(data, name), receipt, 36288, 48384, expected))
        receipts.append(copy.deepcopy(receipt))
        boundary("authenticate_four_actual_B_maps", character=character)
    return {"manifest_sha256": sha(raw), "workflow_sha256": sha(workflow_raw), "checker_sha256": sha(checked_raw),
        "tables": tables, "receipts": receipts, "prefix_sha256": manifest["prefix_shifts"]["sha256"]}


def compare_current_grade(evaluated: dict[str, Any], maps: dict[str, Any], rho2: dict[str, Any],
                          target: np.ndarray, output: OutputFiles) -> dict[str, Any]:
    require(target.shape == (48384,) and target.dtype == np.uint8 and not np.any(target > 2), "accepted_current_target_type")
    if evaluated["normalized_pair_applicable"] is False:
        record = sealed("current-grade", {"status": "NOT_APPLICABLE", "reason": "same_root_not_18_divisible",
            "grade2_member": "NOT_DECIDED", "source_lower_zero_required": False, "full_P_zero_claimed": False,
            "full_filtered_coordinates_compared": 0, "candidate": True, "cross_checked": False, "verified": False, "eof": True})
        output.json("current-grade.json", record)
        return record
    lower, top = evaluated["physical_lower"], evaluated["physical_top"]
    target_join = np.array_equal((top.astype(np.uint16) + target) % 3, rho2["dense"])
    positive_equal = np.array_equal(top, rho2["dense"])
    associated_receipt, associated_equal = None, None
    if evaluated["source_lower_zero"]:
        associated = np.zeros(48384, dtype=np.uint8)
        for character in range(4):
            contribution = MAPS.sparse_apply(maps["tables"][character], evaluated["source"][2][character], 36288, 48384)
            associated = ((associated.astype(np.uint16) + np.asarray(contribution, dtype=np.uint8)) % 3).astype(np.uint8)
            boundary("same_root_associated_four_B_sum", character=character)
        associated_equal = np.array_equal(associated, top)
        require(associated_equal, "source_lower_zero_associated_B_equals_direct_full_top")
        associated_receipt = output.trits("grade/associated-four-B.u8", associated)
    require(not np.any(lower), "same_word_current_physical_lower_full_32260_zero")
    require(target_join, "same_word_direct_top_plus_actual_remainder_equals_original_rho2_full_48384")
    target_zero = not np.any(target)
    if target_zero:
        require(positive_equal, "target_zero_direct_original_rho2_equality")
    record = sealed("current-grade", {"status": "PASS", "codomain": "PB4-dropped-two-hexagons-v478-2.7",
        "source_lower_width": 96776, "source_lower_zero": bool(evaluated["source_lower_zero"]),
        "source_lower_zero_required": False, "physical_lower_width": 32260, "physical_lower_zero": True,
        "physical_top_width": 48384, "full_filtered_coordinates_compared": 80644,
        "top_plus_current_target_equals_actual_original_rho2": True,
        "direct_top_equals_actual_original_rho2": bool(positive_equal), "current_target_zero": bool(target_zero),
        "original_rho2_manifest_sha256": rho2["manifest_sha256"], "original_rho2_packed_sha256": rho2["packed_sha256"],
        "original_rho2_directly_read": True, "current_target_dense_sha256": sha(target.tobytes()),
        "associated_four_B_applicable": bool(evaluated["source_lower_zero"]),
        "associated_four_B_equals_direct_top": None if associated_equal is None else bool(associated_equal),
        "associated_four_B": associated_receipt, "Task712_manifest_sha256": maps["manifest_sha256"],
        "positive_readout": "LOCAL_D_CONDITIONS_ONLY" if target_zero else "NOT_APPLICABLE_NONZERO_REMAINDER",
        "all_eleven_typed_receipts_retained": True, "PB4_Fox_zero_required": False, "full_P_zero_claimed": False,
        "side_localization_conditions_complete": False, "grade2_member": "NOT_DECIDED", "full_A0": False,
        "candidate": True, "cross_checked": False, "verified": False, "eof": True})
    output.json("current-grade.json", record)
    return record


PARENT_ROLES = ("state", "delta", "seed34", "packet", "refinement", "oracle", "e", "prepare",
                "block-0", "block-1", "block-2", "block-3", "p1", "task712", "continuation", "rho2")
PARENT_MANIFEST_FILES = {"state": "state/manifest.json", "delta": "output/manifest.json",
    "seed34": "output/manifest.json", "packet": "output/HEAD", "refinement": "output/HEAD",
    "oracle": "output/manifest.json", "e": "output/manifest.json", "p1": "manifest.json",
    "task712": "r07-grade2-maps-v4/manifest.json", "continuation": "output/HEAD", "rho2": "task640-payload/manifest.json"}
# Exact accepted artifact metadata, independent of producer implementation.
# tuple = run, head, artifact id, name, bytes, archive SHA, workflow basename.
FIXED_ARTIFACTS = {
    "state": (33891714539, "7b7b9de20faaa3b8f26e331bb738b374f6f5708c", 9944214057,
        "d972-r07-grade2-physical-state-separator-v2-candidate-33891714539-1", 107195261,
        "2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017", "d972-r07-grade2-physical-state-separator-v2.yml"),
    "delta": (33946247365, "7f6dfaddf4150449e62a9b3e85def472fcb41c01", 9963533999,
        "d972-r07-actual-seed30-materializer-v1-candidate-33946247365-1", 915410,
        "f9627416f0e920fa369f6bc6bb9bffa8c6b15674c0fb7ff37bbebaf77991ace6", "d972-r07-actual-seed30-materializer-v1.yml"),
    "seed34": (33956437467, "b9ae78b0950b186463849c3ec874f6474f359851", 9966542166,
        "d972-r07-actual-root-seed-materializer-v3-candidate-33956437467-1", 984053,
        "a4cb9f63a470636628d9ef02a5b5e55d90fe3b0a2c70f2012d32c9517d87defc", "d972-r07-actual-root-seed-materializer-v3.yml"),
    "packet": (33964709359, "fff114c41bd8748ad0e708919fe0820335c9cce8", 9969090590,
        "d972-r07-fixed-root-packet-loop-v2-candidate-33964709359-1", 1855391,
        "b15b07150d23a1a291fff387f23c8c13cf3ab5ada2b5f95f2a886b0bdf44a428", "d972-r07-fixed-root-packet-loop-v2.yml"),
    "refinement": (33971897879, "64475e1dfab1537a38d1b3131971bfed5fc3071c", 9971466432,
        "d972-r07-full-origin-checker-completion-v1-candidate-33971897879-1", 51943596,
        "0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8", "d972-r07-full-origin-checker-completion-v1.yml"),
    "oracle": (33977701313, "bbce98d8f95a845f36fe89c0f507b9360792666f", 9972829869,
        "d972-r07-section-cochain-checker-completion-v1-candidate-33977701313-1", 2299772,
        "1a5c8800af563493b95dd4166d20c2fe1b74449f5f7f15aa99278d9b1c1b878d", "d972-r07-section-cochain-checker-completion-v1.yml"),
    "e": (33981657987, "444c71c9e554ae8feb9c8ee54df57d3df19ed66f", 9973974150,
        "d972-r07-selected-cycle-materializer-v1-candidate-33981657987-1", 2816692,
        "884c039737cae9673c9e1d871c30713456c993b97f16a557e9c8c24078537f25", "d972-r07-selected-cycle-materializer-v1.yml"),
    "p1": (33851744070, "6673eb2ea15ca6022acc2ddc5a8a204a0380172f", 9931437113,
        "task809-canonical-p1-degree2-lift-v9-33851744070-1", 641518300,
        "6d6f2ec6eb7f1245b8e7d52645c710ecd519ae0cc442340237d1098c7fa63d5c", "d972-r07-canonical-p1-dag-degree2-lift-v9.yml"),
    "task712": (33814194630, "5ff2c5a30b604536df12acba8801828a5a7e5fe0", 9915928157,
        "d972-r07-grade2-maps-v4-33814194630-1", 22404961,
        "abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858", "d972-r07-grade2-maps-v4.yml"),
    "rho2": (33839962829, "17a8439c766d92719d7ae7d35846ea444da598fa", 9925190479,
        "task640-fresh-rho2-v17-33839962829-1", 6049643,
        "01722bfda081e577195aa6ca9c0bba3425a50dcfd829eca6ac23e33cb5d79ca4", "d972-r07-a0-fresh-precision2-endpoint-v17.yml"),
}
for _role, _id, _name, _size, _sha in (
    ("prepare", 9865061266, "prepare", 204360988, "da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4"),
    ("block-0", 9865238399, "state-block-0", 81729645, "2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838"),
    ("block-1", 9865242284, "state-block-1", 82259824, "849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb"),
    ("block-2", 9865193269, "state-block-2", 82200189, "d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d"),
    ("block-3", 9865239848, "state-block-3", 82266526, "87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92"),
):
    FIXED_ARTIFACTS[_role] = (33677346616, "22c6dddb43d107c05e65f53ad898823ae8ebe276", _id,
        f"task554-grade1-v3-{_name}-33677346616-1", _size, _sha, "d972-r07-a0-first-rung-grade1-v3.yml")


def typed_equal(left: Any, right: Any, label: str) -> None:
    require(canonical(left) == canonical(right), label)


def regular_tree(root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    require(root.is_dir() and not root.is_symlink() and not root.is_junction(), "input_regular_directory")
    files, directories = [], []
    for current, subdirectories, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(subdirectories):
            child = current_path / name
            require(not child.is_symlink() and not child.is_junction() and stat.S_ISDIR(child.lstat().st_mode), "input_no_reparse_directory")
            directories.append(child.relative_to(root).as_posix())
        for name in sorted(filenames):
            child = current_path / name
            files.append(file_receipt(child, child.relative_to(root).as_posix()))
        boundary("authenticate_complete_input_roster")
    return sorted(files, key=lambda item: item["file"]), sorted(directories)


def artifact_check(role: str, value: Any) -> None:
    require(type(value) is dict and set(value) == {"run", "attempt", "head", "id", "name", "bytes", "sha256",
            "workflow", "repository_id", "conclusion"}, "accepted_artifact_exact_tuple")
    for key in ("run", "attempt", "id", "bytes", "repository_id"):
        integer(value[key], "artifact_integer:" + key, 1)
    require(value["repository_id"] == 1312092366 and type(value["head"]) is str and len(value["head"]) == 40 and
            all(x in "0123456789abcdef" for x in value["head"]) and type(value["sha256"]) is str and
            value["sha256"].startswith("sha256:") and type(value["workflow"]) is str and
            value["workflow"].startswith(".github/workflows/") and type(value["name"]) is str and value["name"],
            "accepted_artifact_types")
    hash_string(value["sha256"][7:], "artifact_archive_hash")
    require(value["conclusion"] == ("failure" if role == "prepare" or role.startswith("block-") else "success"),
            "artifact_actual_accepted_conclusion")
    if role != "continuation":
        run, head, identifier, name, size, digest, workflow = FIXED_ARTIFACTS[role]
        typed_equal(value, {"run": run, "attempt": 1, "head": head, "id": identifier, "name": name, "bytes": size,
            "sha256": "sha256:" + digest, "workflow": ".github/workflows/" + workflow, "repository_id": 1312092366,
            "conclusion": "failure" if role == "prepare" or role.startswith("block-") else "success"}, "fixed_parent_artifact:" + role)
    else:
        require(value["workflow"] in CONTINUATION_WORKFLOWS, "registered_continuation_success_workflow")


def current_lambda_type(head: dict[str, Any], checked: dict[str, Any]) -> None:
    if head["kind"] == "Separator":
        require(type(checked["lambda_rho2"]) is dict and checked["lambda_rho2"]["mode"] == "derived" and
                checked["lambda_rho2"]["original_rho2_packed_sha256"] == RHO2_PACKED_SHA and
                type(head["lambda_sha256"]) is str, "selected_separator_derived_original_rho2_identity")
    else:
        require(head["kind"] == "LinearMembershipCandidate" and checked["lambda_rho2"] is None and
                head["lambda_sha256"] is None, "selected_linear_has_no_lambda_derivation")


class AcceptedInputs:
    """Root-provided observed acceptance, all immutable parent bytes, thin C PASS intake."""
    def __init__(self, args: argparse.Namespace):
        self.args = args
        raw = args.acceptance.read_bytes()
        self.acceptance = seal_check(exact_json(raw, "acceptance"), WORD_SCHEMA + ".acceptance", "observed_acceptance_seal")
        self.acceptance_sha = sha(raw)
        require(set(self.acceptance) == {"schema", "sha256", "status", "parents", "selected", "consumer_sources", "runtime",
                "candidate", "cross_checked", "verified"} and self.acceptance["status"] == "PASS" and
                self.acceptance["candidate"] is True and self.acceptance["cross_checked"] is False and
                self.acceptance["verified"] is False, "observed_acceptance_exact_fields")
        self.roots = {role: getattr(args, role.replace("-", "_") + "_root").resolve()
                      for role in PARENT_ROLES if not role.startswith("block-")}
        self.roots.update({f"block-{i}": root.resolve() for i, root in enumerate(args.block_root)})
        root_paths = [*self.roots.values(), args.word_root.resolve(), args.output.resolve()]
        require(len(root_paths) == len(set(root_paths)) and all(left not in right.parents and right not in left.parents
                for i, left in enumerate(root_paths) for right in root_paths[i + 1:]), "input_output_roots_nonoverlapping")
        require(type(self.acceptance["parents"]) is list and [item.get("role") for item in self.acceptance["parents"]] == list(PARENT_ROLES),
                "sixteen_parent_order")
        self.parents = {}
        for record in self.acceptance["parents"]:
            require(type(record) is dict and set(record) == {"role", "artifact", "manifest", "files", "directories"}, "parent_record_shape")
            role = record["role"]
            artifact_check(role, record["artifact"])
            descriptor_check(record["manifest"], "accepted_parent_manifest")
            require(type(record["files"]) is list and type(record["directories"]) is list, "accepted_parent_rosters")
            for descriptor in record["files"]:
                descriptor_check(descriptor, "accepted_parent_file")
            require(record["files"] == sorted(record["files"], key=lambda item: item["file"]) and
                    len({item["file"] for item in record["files"]}) == len(record["files"]) and
                    record["manifest"] in record["files"], "accepted_complete_parent_file_order")
            files, directories = regular_tree(self.roots[role])
            typed_equal(files, record["files"], "actual_all_parent_files:" + role)
            typed_equal(directories, record["directories"], "actual_all_parent_directories:" + role)
            self.parents[role] = {"record": copy.deepcopy(record), "files": {item["file"]: item for item in files}}
            if role == "prepare" or role.startswith("block-"):
                primary_head = self.json(role, role + ".HEAD")
                expected_name = role + "." + hash_string(primary_head["body_sha256"], "Task554_primary_body_hash") + ".json"
                require(record["manifest"]["sha256"] == primary_head["body_sha256"], "Task554_primary_manifest_is_HEAD_body")
            else:
                expected_name = PARENT_MANIFEST_FILES[role]
            require(record["manifest"]["file"] == expected_name, "accepted_role_exact_primary_manifest")
            boundary("accepted_parent_complete", role=role)
        self.check_runtime_sources()
        self.selected = self.read_selected()

    def read(self, role: str, name: str) -> bytes:
        require(role in self.parents and name in self.parents[role]["files"], "read_only_registered_parent_file")
        item = relative_file(self.roots[role], name)
        raw = item.read_bytes()
        record = self.parents[role]["files"][name]
        require(len(raw) == record["bytes"] and sha(raw) == record["sha256"], "registered_parent_file_still_pinned")
        return raw

    def json(self, role: str, name: str) -> Any:
        return exact_json(self.read(role, name), role + ":" + name)

    def check_runtime_sources(self) -> None:
        typed_equal(self.acceptance["runtime"], {"python": sys.version, "numpy": np.__version__}, "accepted_actual_runtime")
        sources = self.acceptance["consumer_sources"]
        require(type(sources) is dict and set(sources) == {"producer", "checker"}, "new_two_consumer_source_receipts")
        expected = {"producer": "search/d972_r07_continuation_positive_word_readout_v2.py",
                    "checker": "search/check_d972_r07_continuation_same_word_eleven_slots_v2.py"}
        for role, name in expected.items():
            descriptor_check(sources[role], "consumer_source_pin")
            require(sources[role]["file"] == name and file_receipt(relative_file(REPOSITORY, name), name) == sources[role],
                    "new_consumer_source_bytes:" + role)
        # Producer source is hashed only; no read of implementation or import.
        for name, pin in {**RETAINED_PINS, **DATA_PINS}.items():
            record = file_receipt(relative_file(REPOSITORY, name), name)
            require((record["bytes"], record["sha256"]) == pin, "retained_source_data_stable")

    def read_selected(self) -> dict[str, Any]:
        selected = self.acceptance["selected"]
        names = {"head": "output/HEAD", "result": "output/result.json", "checker": "checker-result.json",
                 "owner": "output/owner.json", "source": "output/source.json", "start": "output/start.json",
                 "fixed": "output/fixed/manifest.json"}
        require(type(selected) is dict and set(selected) == set(names) | {"completed_steps", "rank", "generation", "kind",
                "state_head", "target_remainder_sha256", "lambda_sha256", "terminal"}, "accepted_selected_snapshot_fields")
        values, hashes = {}, {}
        for key, name in names.items():
            descriptor_check(selected[key], "selected_entry")
            require(selected[key]["file"] == name and selected[key] == self.parents["continuation"]["files"][name],
                    "selected_entry_full_file_pin")
            raw = self.read("continuation", name)
            value = exact_json(raw, "selected_" + key)
            suffix = "fixed-manifest" if key == "fixed" else "checker-result" if key == "checker" else key
            values[key] = seal_check(value, "d972.r07.complete-oracle-cegar-continuation.v1." + suffix, "selected_inner_schema:" + key)
            hashes[key] = sha(raw)
            if key in CONTINUATION_ENTRY_PINS:
                require((len(raw), sha(raw)) == CONTINUATION_ENTRY_PINS[key], "same_immutable_continuation_entry:" + key)
        head, result, checked = values["head"], values["result"], values["checker"]
        require(values["source"]["producer_sha256"] == CEGAR_PRODUCER_SHA and
                values["source"]["python"] == sys.version and values["source"]["numpy"] == np.__version__,
                "same_frozen_CEGAR_producer_and_runtime")
        require(checked["status"] == "PASS" and checked["checker_sha256"] == CEGAR_CHECKER_SHA and
                checked["candidate"] is True and checked["cross_checked"] is False and checked["verified"] is False,
                "selected_successful_full_prefix_checker")
        for key in ("completed_steps", "rank", "generation", "kind", "state_head", "target_remainder_sha256", "lambda_sha256"):
            typed_equal(head[key], selected[key], "selected_HEAD_value:" + key)
            typed_equal(result[key], head[key], "selected_result_value:" + key)
            typed_equal(checked[key], head[key], "selected_checker_value:" + key)
        for key in ("completed_steps", "rank", "generation"):
            integer(head[key], "selected_snapshot_integer", 0)
        require(result["terminal"] == checked["terminal"] == selected["terminal"] and
                checked["prefix_steps_replayed"] == head["completed_steps"] == len(checked["steps"]) and
                checked["all_new_committed_arrays_and_json_compared"] is True and
                checked["current_checkpoint_fully_compared"] is True and checked["full_four_character_scope"] is True and
                checked["section_equalities_each"] == 8059 and checked["chords_each"] == 54433 and
                checked["auxiliary_tests_each"] == 2 and checked["external_e_attached"] == 1,
                "selected_full_prefix_scope_and_terminal")
        for key in ("owner", "source", "start", "fixed"):
            field = "fixed_manifest_sha256" if key == "fixed" else key + "_sha256"
            require(head[field] == result[field] == checked[field] == hashes[key], "selected_owner_source_start_fixed_join")
        require(result["head_sha256"] == checked["head_sha256"] == hashes["head"] and
                checked["result_sha256"] == hashes["result"] and
                values["start"]["lambda_rho2"]["original_rho2_packed_sha256"] == RHO2_PACKED_SHA,
                "selected_HEAD_result_and_original_rho2_identity")
        current_lambda_type(head, checked)
        count = head["completed_steps"]
        if count:
            step_name = f"output/steps/{count:06d}/manifest.json"
            step_raw = self.read("continuation", step_name)
            step = seal_check(exact_json(step_raw, "last_step"), "d972.r07.complete-oracle-cegar-continuation.v1.step-manifest", "last_step_seal")
            require(sha(step_raw) == head["last_step_manifest_sha256"] and step["step"] == count and
                    step["state_head"] == head["state_head"] and step["target_remainder_sha256"] == head["target_remainder_sha256"],
                    "only_HEAD_committed_last_step")
            target_raw = self.read("continuation", f"output/snapshots/{count - 1:06d}/e/physical/target-remainder.bin")
        else:
            require(head["last_step_manifest_sha256"] is None, "zero_new_prefix_last_step")
            target_raw = self.read("e", "output/target-remainder.bin")
        require(sha(target_raw) == head["target_remainder_sha256"], "actual_current_remainder_bytes")
        target = packed_trits(target_raw, 48384, "accepted_current_remainder")
        require(head["kind"] in ("Separator", "LinearMembershipCandidate") and
                (head["kind"] == "LinearMembershipCandidate") == (not np.any(target)), "selected_kind_and_actual_target_zero")
        return {"values": values, "hashes": hashes, "target": target, "target_raw_sha256": sha(target_raw)}

    def finish_unchanged(self) -> None:
        require(sha(self.args.acceptance.read_bytes()) == self.acceptance_sha, "acceptance_unchanged")
        self.check_runtime_sources()
        for role in PARENT_ROLES:
            files, directories = regular_tree(self.roots[role])
            typed_equal(files, self.parents[role]["record"]["files"], "all_parent_files_unchanged:" + role)
            typed_equal(directories, self.parents[role]["record"]["directories"], "all_parent_directories_unchanged:" + role)


def json_pointer(value: Any, pointer: str) -> Any:
    require(type(pointer) is str and (pointer == "" or pointer.startswith("/")), "RFC6901_pointer")
    current = value
    for escaped in pointer.split("/")[1:]:
        require(all(escaped[i + 1:i + 2] in ("0", "1") for i, char in enumerate(escaped) if char == "~"), "RFC6901_escape")
        token = escaped.replace("~1", "/").replace("~0", "~")
        if type(current) is list:
            require(token.isascii() and token.isdecimal() and str(int(token)) == token, "RFC6901_array_index")
            index = integer(int(token), "RFC6901_array_bounds", 0, len(current) - 1)
            current = current[index]
        else:
            require(type(current) is dict and token in current, "RFC6901_object_key")
            current = current[token]
    return current


class AncestorIndex:
    def __init__(self, inputs: AcceptedInputs, value: dict[str, Any],
                 basis_blobs: dict[tuple[str, str], dict[str, Any]] | None = None):
        seal_check(value, WORD_SCHEMA + ".ancestor-index", "ancestor_index_seal")
        require(type(value.get("entries")) is list, "ancestor_index_entries")
        self.inputs, self.entries = inputs, copy.deepcopy(value["entries"])
        self.pointed: dict[int, Any] = {}
        groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
        fields = {"id", "namespace", "parent_role", "parent_manifest_sha256", "file", "file_sha256",
                  "offset", "length", "record_sha256", "json_pointer"}
        for index, entry in enumerate(self.entries):
            require(type(entry) is dict and set(entry) == fields and type(entry["id"]) is int and entry["id"] == index and
                    entry["namespace"] in NAMESPACES and entry["parent_role"] in PARENT_ROLES, "ancestor_entry_exact_type")
            role = entry["parent_role"]
            require(entry["file"] in inputs.parents[role]["files"], "ancestor_file_in_accepted_roster")
            require(inputs.parents[role]["files"][entry["file"]]["sha256"] == entry["file_sha256"], "ancestor_actual_whole_file_sha")
            hash_string(entry["record_sha256"], "ancestor_pointed_hash")
            hash_string(entry["parent_manifest_sha256"], "ancestor_manifest_hash")
            require(entry["parent_manifest_sha256"] == inputs.parents[role]["record"]["manifest"]["sha256"],
                    "ancestor_manifest_is_same_role_accepted_primary_receipt")
            if entry["json_pointer"] is not None:
                require(type(entry["json_pointer"]) is str and entry["offset"] is None and entry["length"] is None,
                        "ancestor_pointer_no_ambiguous_position")
            else:
                integer(entry["offset"], "ancestor_byte_offset", 0)
                integer(entry["length"], "ancestor_byte_length", 0)
                require(entry["offset"] + entry["length"] <= inputs.parents[role]["files"][entry["file"]]["bytes"],
                        "ancestor_position_bounds")
            groups.setdefault((role, entry["file"]), []).append(entry)
        for (role, name), entries in groups.items():
            size = inputs.parents[role]["files"][name]["bytes"]
            if any(entry["json_pointer"] is not None for entry in entries):
                parsed = inputs.json(role, name)
                for entry in entries:
                    if entry["json_pointer"] is not None:
                        part = json_pointer(parsed, entry["json_pointer"])
                        require(sha(canonical(part)) == entry["record_sha256"], "actual_ancestor_JSON_pointer_hash")
                        self.pointed[entry["id"]] = part
                del parsed
            with relative_file(inputs.roots[role], name).open("rb") as stream:
                for entry in entries:
                    if entry["json_pointer"] is not None:
                        continue
                    if entry["offset"] == 0 and entry["length"] == size:
                        require(entry["record_sha256"] == entry["file_sha256"], "whole_file_ancestor_hash")
                        continue
                    offset, length = entry["offset"], entry["length"]
                    if name.endswith(".jsonl") and offset:
                        stream.seek(offset - 1)
                        require(stream.read(1) == b"\n", "ancestor_position_at_JSONL_record_start")
                    stream.seek(offset)
                    raw = stream.read(length)
                    require(len(raw) == length and sha(raw) == entry["record_sha256"], "ancestor_position_complete_record_hash")
                    if name.endswith(".jsonl"):
                        require(raw.endswith(b"\n") and b"\n" not in raw[:-1], "ancestor_position_one_complete_JSONL_record")
                        self.pointed[entry["id"]] = exact_json(raw, "positioned_ancestor")
                    else:
                        registered_basis = (basis_blobs or {}).get((role, name))
                        basis_row = (entry["namespace"] == "p1" and registered_basis is not None and
                            length == registered_basis["row_bytes"] and offset % length == 0 and
                            offset // length < registered_basis["rows"] and
                            size == registered_basis["rows"] * length and
                            entry["file_sha256"] == registered_basis["sha256"])
                        legal = (basis_row or (entry["namespace"] == "physical" and name.endswith(".bin") and length == 12096 and offset % 12096 == 0) or
                                 (entry["namespace"] == "p1" and name.endswith("degree2.cache.bin") and length == 36288 and offset % 36288 == 0) or
                                 (entry["namespace"] == "tree" and name.endswith(".u32") and length == 4 and offset % 4 == 0))
                        require(legal, "ancestor_typed_binary_record_shape")
            boundary("authenticate_ancestor_file_and_all_references", role=role, references=len(entries))

    def require_use(self, node: dict[str, Any], namespace: str, role: str, name: str,
                    *, pointer: str | None = None, offset: int | None = None, length: int | None = None) -> None:
        """A whole-file reference or an exact containing pointer covers this actual recipe."""
        for index in node["receipt_refs"]:
            entry = self.entries[index]
            if (entry["namespace"], entry["parent_role"], entry["file"]) != (namespace, role, name):
                continue
            if entry["json_pointer"] is None and entry["offset"] == 0 and entry["length"] == self.inputs.parents[role]["files"][name]["bytes"]:
                return
            if (pointer is not None and entry["json_pointer"] is not None and
                    (pointer == entry["json_pointer"] or pointer.startswith(entry["json_pointer"] + "/"))):
                return
            if offset is not None and entry["json_pointer"] is None and entry["offset"] == offset and entry["length"] == length:
                return
        raise ValueError("same_word:Ref_missing_actual_recipe_reference:" + namespace + ":" + role + ":" + name)


def literal_dictionary(floor: IndependentFloor) -> dict[str, list[int]]:
    words = floor.words
    seeds = words["relators"]
    raw = json.loads(floor.data["scratchpad/a0_v2_words.json"])
    qwords = raw["raw_q0_relators"]
    require(len(seeds) == 44 and sha(canonical(seeds)[:-1]) == "7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8" and
            len(qwords) == 19 and sha(canonical(qwords)[:-1]) == "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a",
            "actual_seed_and_normalizer_word_dictionaries")
    require(all(type(row) is list and all(type(t) is int and t in (-2, -1, 1, 2) for t in row) for row in seeds + qwords),
            "literal_dictionary_all_signed_letters")
    answer = {**{f"r:{i + 1}": list(row) for i, row in enumerate(seeds)},
              **{f"q:{i + 1}": list(row) for i, row in enumerate(qwords)},
              **{f"pure:{i}": list(ENDPOINT.PURE_WORDS[parity]) for i, parity in enumerate(CHARACTERS)}}
    def concatenate(factors: Iterable[tuple[int, int]]) -> list[int]:
        stack: list[int] = []
        for index, exponent in factors:
            word = qwords[index]
            for _ in range(abs(exponent)):
                for letter in (word if exponent >= 0 else [-t for t in reversed(word)]):
                    if stack and stack[-1] == -letter:
                        stack.pop()
                    else:
                        stack.append(letter)
        return stack
    for name, factors, size, digest in (
        ("r_x", ((0, 1), (5, -2), (6, 4), (8, 1)), 1058, "82fa1ff07d5269e5228fb411b97321b61869791c49133aaa65161f44d16b6f2c"),
        ("r_y", ((7, -1), (3, -1)), 466, "88657577db0338fd5c58f7edeec205c27ce5ff5ddba128b8af403167cb232ac0"),
    ):
        word = concatenate(factors)
        require(len(word) == size and sha(canonical(word)[:-1]) == digest, "normalizer_actual_reduced_literal:" + name)
        answer["normalizer:" + name] = word
    return answer


def signed(value: Any) -> int:
    integer(value, "saved_F3_coefficient", 0, 2)
    return (0, 1, -1)[value]


def decimal_key(value: str, label: str) -> int:
    require(type(value) is str and value.isascii() and value.isdecimal() and str(int(value)) == value, label)
    return int(value)


def ref_pattern(namespace: str, key: int | str, scope: str) -> tuple[Any, ...]:
    return "Ref", namespace, str(key), scope


def product_pattern(factors: Iterable[tuple[Any, ...]]) -> tuple[Any, ...]:
    return "OrderedProduct", tuple(factors)


def power_pattern(word: tuple[Any, ...], exponent: int) -> tuple[Any, ...]:
    return "IntegerPower", exponent, word


def projector_pattern(word: tuple[Any, ...], character: int) -> tuple[Any, ...]:
    integer(character, "whole_projector_character", 0, 3)
    return product_pattern(power_pattern(("Act", ("Rel", f"pure:{index}"), word),
        1 if sum(x * y for x, y in zip(CHARACTERS[character], parity)) % 2 == 0 else -1)
        for index, parity in enumerate(CHARACTERS))


def expect_pattern(catalog: NodeCatalog, stream: Any, number: int, pattern: tuple[Any, ...]) -> None:
    todo = [(number, pattern)]
    while todo:
        identifier, expected = todo.pop()
        node = catalog.read(stream, identifier)
        op, args = node["op"], node["args"]
        require(op == expected[0], "Ref_recipe_exact_ordered_operation")
        if op == "Identity":
            require(expected == ("Identity",), "recipe_identity")
        elif op == "Letter":
            require(args["letter"] == expected[1], "recipe_actual_letter")
        elif op == "Rel":
            require(args["relator_id"] == expected[1], "recipe_actual_dictionary_ID")
        elif op == "Ref":
            require((args["namespace"], args["key"], args["scope_sha256"]) == expected[1:] and
                    catalog.symbols[expected[1:]] == identifier, "recipe_prior_typed_symbol")
        elif op == "OrderedProduct":
            require(len(args["factors"]) == len(expected[1]), "recipe_all_factors_including_zero_and_duplicates")
            todo.extend((child["node"], wanted) for child, wanted in zip(args["factors"], expected[1], strict=True))
        elif op == "Act":
            todo.extend(((args["conjugator"]["node"], expected[1]), (args["word"]["node"], expected[2])))
        elif op == "IntegerPower":
            require(type(expected[1]) is int and args["exponent"] == expected[1], "recipe_actual_integer_exponent_once")
            todo.append((args["word"]["node"], expected[2]))
        elif op == "Inverse":
            todo.append((args["word"]["node"], expected[1]))
        else:
            raise ValueError("same_word:unsupported_recipe_operator")
        boundary("actual_recipe_to_prior_ordered_word")


P1_ORDER = (0, 505, 1008, 1511, 2014, 3523, 5035, 6547, 8059)


class SourceRecipes:
    """Literal metadata only: canonical P1 and retained lower recipes, no numeric replay."""
    def __init__(self, inputs: AcceptedInputs):
        self.inputs = inputs
        self.p1_scope = inputs.parents["p1"]["files"]["manifest.json"]["sha256"]
        self.p1, self.old, self.defects, self.body_names = [], [], [], {}
        self.basis_blobs: dict[tuple[str, str], dict[str, Any]] = {}
        self.basis_records: list[dict[str, Any]] = []
        self.basis_hashes: dict[int, tuple[str, str | None]] = {}
        manifest = inputs.json("p1", "manifest.json")
        require(manifest["rows"] == 8059 and manifest["global_order"] == list(P1_ORDER) and
                manifest["character_order"] == [list(x) for x in CHARACTERS] and
                manifest["actor_order"] == [1, -1, 2, -2], "canonical_P1_literal_owner_order")
        stream_record = manifest["instruction"]
        require(stream_record["path"] == "instructions.jsonl" and stream_record["eof"] is True and
                stream_record["sha256"] == inputs.parents["p1"]["files"]["instructions.jsonl"]["sha256"],
                "canonical_P1_stream_manifest")
        predecessor, offset, digest = "0" * 64, 0, hashlib.sha256()
        with relative_file(inputs.roots["p1"], "instructions.jsonl").open("rb") as stream:
            for node in range(8059):
                line = stream.readline()
                require(line, "canonical_P1_full_literal_EOF")
                value = exact_json(line, "canonical_P1_instruction")
                require(type(value["node"]) is int and value["node"] == node and value["predecessor"] == predecessor and
                        value["offset"] == node * 36288 and value["length"] == 36288,
                        "canonical_P1_node_and_row_position")
                predecessor = sha(bytes.fromhex(predecessor) + canonical({key: part for key, part in value.items() if key != "ancestry_sha256"}))
                require(value["ancestry_sha256"] == predecessor, "canonical_P1_literal_rolling_ancestry")
                self.p1.append({key: copy.deepcopy(value[key]) for key in ("node", "origin", "reductions", "scale", "p1_sha256",
                    "literal_input_sha256", "old_defect_literal_input_sha256", "ancestry_sha256", "row_receipt")})
                self.p1[-1].update({"instruction_offset": offset, "instruction_length": len(line), "instruction_sha256": sha(line)})
                digest.update(line); offset += len(line)
                if node % 256 == 0:
                    boundary("canonical_P1_literal_metadata", rows=node + 1)
            require(stream.read(1) == b"" and offset == stream_record["bytes"] and digest.hexdigest() == stream_record["sha256"] and
                    predecessor == stream_record["final_head"], "canonical_P1_complete_8059_literal_stream")
        prepare, prepare_name = self.read_body("prepare", -1)
        self.prepare_name, self.prepare_scope = prepare_name, inputs.parents["prepare"]["files"][prepare_name]["sha256"]
        for owner, block in enumerate(prepare["old_blocks"]):
            record = block["record"]
            require(len(record["dag_nodes"]) == P1_ORDER[owner + 1] - P1_ORDER[owner], "old_P1_literal_count")
            row_blob = self.bind_basis_blob("prepare", prepare_name, block["lower_basis_blob"], len(record["dag_nodes"]), 6056)
            companion_blob = self.bind_basis_blob("prepare", prepare_name, block["lifted_grade_blob"], len(record["dag_nodes"]), 72576)
            for local, actual in enumerate(record["dag_nodes"]):
                node = self.p1[P1_ORDER[owner] + local]
                typed_equal({key: node[key] for key in ("origin", "reductions", "scale")},
                            {key: actual[key] for key in ("origin", "reductions", "scale")}, "P1_old_actual_owner_recipe")
                lead = integer(actual["lead"], "old_actual_source_lead", 0, 6055)
                self.basis_records.append({"kind": "old", "owner": owner, "local": local, "node": node["node"],
                    "original_lead": lead, "embedded_lead": owner * 6048 + lead if lead < 6048 else 96768 + lead - 6048,
                    "row_blob": row_blob, "companion_blob": companion_blob})
            self.old.append({"seed_reductions": copy.deepcopy(record["seed_reductions"]),
                             "actor_transitions": copy.deepcopy(record["actor_transitions"])})
        for index, record in enumerate(prepare["defect_origins"]):
            require(type(record["id"]) is int and record["id"] == index, "prepare_defect_actual_ID")
            self.defects.append(copy.deepcopy(record))
        require(len(self.old) == 4 and len(self.defects) == 8232, "prepare_literal_complete_rosters")
        del prepare, block, record, actual
        for owner in range(4):
            block, name = self.read_body(f"block-{owner}", owner)
            require(len(block["dag_nodes"]) == P1_ORDER[owner + 5] - P1_ORDER[owner + 4], "new_P1_literal_count")
            row_blob = self.bind_basis_blob(f"block-{owner}", name, block["basis_blob"], len(block["dag_nodes"]), 18144)
            for local, actual in enumerate(block["dag_nodes"]):
                node = self.p1[P1_ORDER[owner + 4] + local]
                typed_equal({key: node[key] for key in ("origin", "reductions", "scale")},
                            {key: actual[key] for key in ("origin", "reductions", "scale")}, "P1_new_actual_owner_recipe")
                lead = integer(actual["lead"], "new_actual_source_lead", 0, 18143)
                require(block["pivot_leads"][local] == lead, "new_basis_saved_lead_join")
                self.basis_records.append({"kind": "new", "owner": owner, "local": local, "node": node["node"],
                    "original_lead": lead, "embedded_lead": 24192 + owner * 18144 + lead,
                    "row_blob": row_blob, "companion_blob": None})
            del block, actual
            boundary("literal_metadata_body_released", owner=owner)
        require(len(self.basis_records) == 8059 and [row["node"] for row in self.basis_records] == list(range(8059)),
                "all_canonical_source_basis_metadata")
        self.base_scope = inputs.parents["state"]["files"]["state/manifest.json"]["sha256"]
        self.lower, self.connections, self.base_pivots, self.base_records = [], {}, [], []
        raw = inputs.read("state", "state/instructions.jsonl")
        offset = 0
        for offer, line in enumerate(raw.splitlines(keepends=True)):
            value = exact_json(line, "base_physical_instruction")
            require(type(value["offer"]) is int and value["offer"] == offer, "base_physical_offer_order")
            source = value["source"]
            require(source["offer"] == offer and source["source"]["node"] == offer and 0 <= offer < len(self.p1),
                    "base_Conn_source_node")
            p1 = self.p1[offer]
            require(source["source"]["instruction_sha256"] == p1["instruction_sha256"] and
                    source["source"]["p1_sha256"] == p1["p1_sha256"] and
                    source["source"]["ancestry_sha256"] == p1["ancestry_sha256"], "Conn_actual_canonical_P1_join")
            record = {"value": value, "offset": offset, "length": len(line), "sha256": sha(line)}
            self.base_records.append(record)
            if source["kind"] == "pivot":
                require(source["rank"] == len(self.lower) + 1 and value["kind"] == "skipped", "retained_Conn_lower_insertion_order")
                self.lower.append(record)
            else:
                require(source["kind"] == "connection", "retained_Conn_raw_type")
                self.connections[offer] = record
            if value["kind"] == "physical_pivot":
                require(value["rank"] == len(self.base_pivots) + 1 and value["physical_offset"] == len(self.base_pivots) * 12096,
                        "base_physical_insertion_order")
                self.base_pivots.append(record)
            offset += len(line)
        require(len(self.base_records) == 8059 and len(self.base_pivots) == 1354 and offset == len(raw), "base_complete_literal_instruction_EOF")
        del raw

    def bind_basis_blob(self, role: str, body_file: str, value: dict[str, Any], rows: int, width: int) -> dict[str, Any]:
        require(type(value) is dict and value["rows"] == rows and value["width"] == width and
                value["bytes"] == rows * ((width + 3) // 4), "Task554_actual_basis_descriptor_shape")
        descriptor = {key: value[key] for key in ("file", "bytes", "sha256")}
        descriptor_check(descriptor, "Task554_basis_payload_descriptor")
        typed_equal(descriptor, self.inputs.parents[role]["files"][value["file"]], "Task554_basis_file_in_full_accepted_roster")
        key = role, value["file"]
        require(key not in self.basis_blobs, "Task554_basis_descriptor_unique")
        bound = {**descriptor, "role": role, "body_file": body_file,
            "body_sha256": self.inputs.parents[role]["files"][body_file]["sha256"],
            "rows": rows, "width": width, "row_bytes": (width + 3) // 4}
        self.basis_blobs[key] = bound
        return bound

    def event_basis_hashes(self, node: int) -> tuple[str, str | None]:
        integer(node, "event_basis_canonical_node", 0, 8058)
        if node not in self.basis_hashes:
            record = self.basis_records[node]
            hashes = []
            for key in ("row_blob", "companion_blob"):
                descriptor = record[key]
                if descriptor is None:
                    hashes.append(None)
                    continue
                item = relative_file(self.inputs.roots[descriptor["role"]], descriptor["file"])
                with item.open("rb") as stream:
                    stream.seek(record["local"] * descriptor["row_bytes"])
                    raw = stream.read(descriptor["row_bytes"])
                require(len(raw) == descriptor["row_bytes"], "E_event_original_basis_row_exact_bytes")
                hashes.append(sha(raw))
            self.basis_hashes[node] = (hashes[0], hashes[1])
        return self.basis_hashes[node]

    def read_body(self, role: str, owner: int) -> tuple[dict[str, Any], str]:
        stem = "prepare" if owner == -1 else f"block-{owner}"
        head = self.inputs.json(role, stem + ".HEAD")
        require(head["schema"] == "d972.r07.a0.first-rung-grade1.v3.state.head" and head["stem"] == stem,
                "literal_body_HEAD_type")
        name = stem + "." + hash_string(head["body_sha256"], "literal_body_HEAD_hash") + ".json"
        require(self.inputs.parents[role]["files"][name]["sha256"] == head["body_sha256"], "literal_body_HEAD_file_join")
        body = self.inputs.json(role, name)
        require(body["schema"] == "d972.r07.a0.first-rung-grade1.v3.state" and
                body["phase"] == ("prepare" if owner == -1 else "block") and body["parent_sha256"] == head["parent_sha256"],
                "literal_body_actual_schema")
        self.body_names[role] = name
        return body, name

    def p1_ref(self, node: int) -> tuple[Any, ...]:
        integer(node, "literal_P1_global_ID", 0, 8058)
        return ref_pattern("p1", node, self.p1_scope)

    def p1_pattern(self, node: int) -> tuple[Any, ...]:
        integer(node, "P1_recipe_ID", 0, 8058)
        segment = next(i for i in range(8) if P1_ORDER[i] <= node < P1_ORDER[i + 1])
        owner, local = segment % 4, node - P1_ORDER[segment]
        record, origin = self.p1[node], self.p1[node]["origin"]
        if origin["kind"] == "actor":
            parent = integer(origin["parent"], "P1_actor_local_parent", 0, local - 1)
            initial = ("Act", ("Letter", origin["letter"]), self.p1_ref(P1_ORDER[segment] + parent))
        elif segment < 4:
            require(origin["kind"] == "projected_seed", "old_P1_projected_origin")
            seed = integer(origin["seed"], "old_P1_seed_ID", 1, 44)
            initial = projector_pattern(("Rel", f"r:{seed}"), owner)
        else:
            require(origin["kind"] == "defect", "new_P1_whole_old_defect_origin")
            identifier = integer(origin["origin"], "new_P1_defect_ID", 0, len(self.defects) - 1)
            initial = projector_pattern(ref_pattern("old-defect", identifier, self.prepare_scope), owner)
        factors = [initial]
        for prior, coefficient in record["reductions"]:
            factors.append(power_pattern(self.p1_ref(P1_ORDER[segment] + integer(prior, "P1_owner_local_reduction", 0, local - 1)), -signed(coefficient)))
        require(record["scale"] in (1, 2), "P1_internal_nonzero_scale")
        return power_pattern(product_pattern(factors), signed(record["scale"]))

    def defect_pattern(self, identifier: int) -> tuple[Any, ...]:
        record = self.defects[integer(identifier, "old_defect_ID", 0, len(self.defects) - 1)]
        owner = integer(record["lower_character"], "old_defect_owner", 0, 3)
        if record["kind"] == "seed":
            seed = integer(record["seed"], "old_defect_seed", 1, 44)
            initial = projector_pattern(("Rel", f"r:{seed}"), owner)
            reductions = self.old[owner]["seed_reductions"][seed - 1]
        else:
            require(record["kind"] == "transition", "old_defect_transition_type")
            pivot = integer(record["pivot"], "old_defect_actor_parent", 0, P1_ORDER[owner + 1] - P1_ORDER[owner] - 1)
            letter = record["letter"]
            require(type(letter) is int and letter in (1, -1, 2, -2), "old_defect_actor_literal")
            initial = ("Act", ("Letter", letter), self.p1_ref(P1_ORDER[owner] + pivot))
            reductions = self.old[owner]["actor_transitions"][pivot][(1, -1, 2, -2).index(letter)]
        return product_pattern([initial, *(power_pattern(self.p1_ref(P1_ORDER[owner] + prior), -signed(coefficient))
                                          for prior, coefficient in reductions)])

    def conn_pattern(self, namespace: str, key: int) -> tuple[Any, ...]:
        record = self.lower[integer(key, "Conn_lower_ID", 0, len(self.lower) - 1)] if namespace == "conn-lower" else self.connections[key]
        source = record["value"]["source"]
        factors = [self.p1_ref(source["source"]["node"])]
        for prior, coefficient in source["reductions"]:
            integer(prior, "Conn_prior_lower_ID", 0, source["rank"] - (2 if namespace == "conn-lower" else 1))
            factors.append(power_pattern(ref_pattern("conn-lower", prior, self.base_scope), -signed(coefficient)))
        result = product_pattern(factors)
        return power_pattern(result, signed(source["sigma"])) if namespace == "conn-lower" else result


class PhysicalRecipes:
    def __init__(self, inputs: AcceptedInputs, source: SourceRecipes):
        self.inputs, self.source, self.rows = inputs, source, []
        self.raw_records: dict[str, dict[str, Any]] = {}
        base_result = inputs.json("state", "output/result.json")
        target_reduction = base_result["target_reduction"]
        require(target_reduction["rho2_sha256"] == RHO2_PACKED_SHA, "base_target_original_rho2_identity")
        coefficients = [0] * 1354
        used = set()
        for reduction in target_reduction["reductions"]:
            pivot = integer(reduction["pivot_id"], "base_target_pivot_ID", 0, 1353)
            require(pivot not in used, "base_target_coefficient_once")
            used.add(pivot); coefficients[pivot] = signed(reduction["scalar"])
        with relative_file(inputs.roots["state"], "state/physical.bin").open("rb") as stream:
            for pivot, source_record in enumerate(source.base_pivots):
                instruction = source_record["value"]
                raw = stream.read(12096)
                require(len(raw) == 12096, "base_physical_row_literal_receipt_EOF")
                self.rows.append({"pivot": pivot, "role": "state", "instruction_file": "state/instructions.jsonl",
                    "instruction": instruction, "scope": source.base_scope, "record_offset": source_record["offset"],
                    "record_length": source_record["length"], "row_sha256": sha(raw), "coefficient": coefficients[pivot],
                    "result_file": "output/result.json", "result_sha256": inputs.parents["state"]["files"]["output/result.json"]["sha256"],
                    "kind": "base"})
            require(stream.read(1) == b"", "base_physical_rows_exact_EOF")
        for role in ("delta", "seed34"):
            self.add_delta(role, "output", "legacy-seed")
        packet = inputs.json("packet", "output/HEAD")
        require(packet["completed_steps"] == 3, "accepted_fixed_packet_prefix_three")
        self.packet_relations = inputs.json("packet", "output/packet/relations.json")
        require(len(self.packet_relations["seeds"]) == 44 and
                [value["seed"] for value in self.packet_relations["seeds"]] == list(range(44)), "packet_all_zero_based_seed_relations")
        for step in range(1, 4):
            self.add_delta("packet", f"output/steps/{step:06d}", "packet")
        refinement = inputs.json("refinement", "output/HEAD")
        require(refinement["completed_steps"] == 26, "accepted_refinement_literal_prefix_26")
        for step in range(1, 27):
            self.add_delta("refinement", f"output/steps/{step:06d}", "refinement")
        self.add_delta("e", "output", "external-e")
        count = inputs.selected["values"]["head"]["completed_steps"]
        for step in range(1, count + 1):
            self.add_delta("continuation", f"output/snapshots/{step - 1:06d}/e/physical", "loop", step=step)
        require(len(self.rows) == inputs.selected["values"]["head"]["rank"] == 1386 + count,
                "target_word_all_physical_pivots_in_insertion_order")

    def add_delta(self, role: str, prefix: str, kind: str, *, step: int | None = None) -> None:
        instruction_file, result_file = prefix + "/instruction.json", prefix + "/result.json"
        instruction, result = self.inputs.json(role, instruction_file), self.inputs.json(role, result_file)
        scope = self.inputs.parents[role]["files"][instruction_file]["sha256"]
        row_raw = self.inputs.read(role, prefix + "/physical-normalized.bin")
        require(len(row_raw) == 12096 and type(instruction["rank"]) is int and instruction["rank"] == len(self.rows) + 1 and
                instruction["physical_offset"] == len(self.rows) * 12096, "new_physical_literal_global_insertion_ID")
        unsigned = {key: value for key, value in instruction.items() if key != "rolling_sha256"}
        require(instruction["rolling_sha256"] == sha(bytes.fromhex(instruction["predecessor"]) + canonical(unsigned)),
                "physical_literal_rolling_instruction_hash")
        coefficient = signed(result["target"]["scalar"])
        row = {"pivot": len(self.rows), "role": role, "instruction_file": instruction_file,
            "instruction": instruction, "scope": scope, "record_offset": None, "record_length": None,
            "row_sha256": sha(row_raw), "coefficient": coefficient, "result": result,
            "result_file": result_file, "result_sha256": self.inputs.parents[role]["files"][result_file]["sha256"],
            "kind": kind, "prefix": prefix, "step": step}
        if kind == "legacy-seed":
            row["materialization"] = result["ancestry"]
            row["materialization_file"] = result_file
            row["materialization_pointer"] = "/ancestry"
        elif kind == "packet":
            row["selection"] = result["selection"]
        elif kind == "refinement":
            row["materialization_file"] = prefix + "/materialization.json"
            row["materialization"] = self.inputs.json(role, row["materialization_file"])
            row["materialization_pointer"] = ""
        else:
            raw_prefix = "output" if kind == "external-e" else f"output/snapshots/{step - 1:06d}/e/raw"
            p1_prefix = "output" if kind == "external-e" else f"output/snapshots/{step - 1:06d}/e/p1"
            primal_prefix = "output" if kind == "external-e" else f"output/snapshots/{step - 1:06d}/e/primal"
            raw_file = raw_prefix + "/raw-word.json"
            raw = self.inputs.json(role, raw_file)
            raw_scope = self.inputs.parents[role]["files"][raw_file]["sha256"]
            key_prefix = "external-e" if kind == "external-e" else f"loop/{step - 1:06d}"
            require(raw["root"] == "raw-root" and type(raw["nodes"]) is list and
                    len({node["id"] for node in raw["nodes"]}) == len(raw["nodes"]), "accepted_raw_named_node_roster")
            correction_file, reductions_file = p1_prefix + "/source-correction.json", primal_prefix + "/p1-reductions.json"
            correction, reductions = self.inputs.json(role, correction_file), self.inputs.json(role, reductions_file)
            require(correction["raw_word_sha256"] == raw_scope and len(correction["p1_factors"]) == len(reductions["events"]),
                    "E_same_raw_word_and_P1_events")
            for index, (factor, event) in enumerate(zip(correction["p1_factors"], reductions["events"], strict=True)):
                node = integer(factor["node"], "E_factor_P1_ID", 0, 8058)
                require(factor["event"] == event["event"] == index and factor["node"] == event["node"] and
                        factor["coefficient"] == event["coefficient"] and factor["literal_exponent"] == -signed(event["coefficient"]) and
                        factor["p1_sha256"] == self.source.p1[node]["p1_sha256"], "E_ordered_P1_factor_join")
                basis = self.source.basis_records[node]
                typed_equal({key: event[key] for key in ("kind", "owner", "local", "node", "original_lead", "embedded_lead")},
                            {key: basis[key] for key in ("kind", "owner", "local", "node", "original_lead", "embedded_lead")},
                            "E_event_actual_Task554_basis_owner_lead")
                row_sha, companion_sha = self.source.event_basis_hashes(node)
                require(event["row_sha256"] == row_sha and event["row_offset"] == basis["local"] * basis["row_blob"]["row_bytes"] and
                        event["companion_sha256"] == companion_sha and event["companion_offset"] ==
                        (None if basis["companion_blob"] is None else basis["local"] * basis["companion_blob"]["row_bytes"]),
                        "E_event_actual_source_row_and_companion_bytes")
            raw_record = {"role": role, "file": raw_file, "scope": raw_scope, "raw": raw,
                "key_prefix": key_prefix, "correction": correction, "correction_file": correction_file,
                "reductions_file": reductions_file, "indices": {node["id"]: i for i, node in enumerate(raw["nodes"])}}
            self.raw_records[key_prefix] = raw_record
            row["raw_key_prefix"] = key_prefix
        if "physical_sha256" in instruction:
            require(instruction["physical_sha256"] == row["row_sha256"], "new_literal_normalized_row_hash")
        self.rows.append(row)
        boundary("accepted_physical_literal_record", pivots=len(self.rows))

    def ref(self, pivot: int) -> tuple[Any, ...]:
        row = self.rows[integer(pivot, "physical_prior_ID", 0, len(self.rows) - 1)]
        return ref_pattern("physical", pivot, row["scope"])

    def legacy_raw_pattern(self, row: dict[str, Any], relators: dict[str, list[int]]) -> tuple[Any, ...]:
        kind = row["kind"]
        if kind == "legacy-seed":
            materialization, raw_seed = row["materialization"], row["result"]["raw_seed"]
            seed, character = integer(raw_seed["seed"], "legacy_zero_based_seed", 0, 43), raw_seed["character"]
            require(raw_seed["compact_word"] == relators[f"r:{seed + 1}"] and materialization["seed"] == seed and
                    materialization["character"] == character, "legacy_seed_dictionary_and_character")
            initial, events = ("Rel", f"r:{seed + 1}"), materialization["raw_events"]
        elif kind == "packet":
            selection = row["selection"]
            seed, character = integer(selection["seed"], "packet_zero_based_seed", 0, 43), selection["character"]
            relation = self.packet_relations["seeds"][seed]
            require(row["result"]["literal"]["seed_relation_sha256"] == relation["sha256"], "packet_actual_seed_relation")
            initial, events = ("Rel", f"r:{seed + 1}"), relation["raw_events"]
        else:
            materialization = row["materialization"]
            selection, relation = materialization["selection"], materialization["relation"]
            character = selection["character"]
            if selection["origin_kind"] == "actor":
                initial = ("Act", ("Letter", selection["actor"]), self.source.p1_ref(selection["basis_i"]))
            else:
                require(selection["origin_kind"] == "seed", "refinement_literal_origin_type")
                initial = ("Rel", f"r:{integer(selection['seed'], 'refinement_zero_based_seed', 0, 43) + 1}")
            events = relation["raw_events"]
        factors = [initial]
        for index, event in enumerate(events):
            require(type(event["event_id"]) is int and event["event_id"] == index, "legacy_raw_event_order")
            factors.append(power_pattern(self.source.p1_ref(event["global_index"]), -signed(event["coefficient"])))
        return projector_pattern(product_pattern(factors), character)

    def pattern(self, pivot: int, relators: dict[str, list[int]]) -> tuple[Any, ...]:
        row = self.rows[pivot]
        instruction = row["instruction"]
        if row["kind"] == "base":
            initial = ref_pattern("conn-raw", instruction["offer"], self.source.base_scope)
            reductions = instruction["reductions"]
        elif row["kind"] in ("external-e", "loop"):
            raw = self.raw_records[row["raw_key_prefix"]]
            initial = product_pattern([ref_pattern("raw-e", raw["key_prefix"] + "/raw-root", raw["scope"]),
                *(power_pattern(self.source.p1_ref(factor["node"]), -signed(factor["coefficient"]))
                  for factor in raw["correction"]["p1_factors"])])
            reductions = [(item["pivot_id"], item["scalar"]) for item in instruction["physical_reductions"]]
        else:
            initial = self.legacy_raw_pattern(row, relators)
            reductions = [(item["pivot_id"], item["scalar"]) for item in
                          instruction["reductions" if row["kind"] == "legacy-seed" else "physical_reductions"]]
        factors = [initial]
        for prior, coefficient in reductions:
            integer(prior, "physical_reduction_prior_insertion_ID", 0, pivot - 1)
            factors.append(power_pattern(self.ref(prior), -signed(coefficient)))
        return power_pattern(product_pattern(factors), signed(instruction["sigma"]))

    def target_pattern(self) -> tuple[Any, ...]:
        return product_pattern(power_pattern(self.ref(row["pivot"]), row["coefficient"]) for row in self.rows)


class RefRecipes:
    def __init__(self, inputs: AcceptedInputs, ancestors: AncestorIndex, source: SourceRecipes,
                 physical: PhysicalRecipes, catalog: NodeCatalog, relators: dict[str, list[int]]):
        self.inputs, self.ancestors, self.source, self.physical = inputs, ancestors, source, physical
        self.catalog, self.relators = catalog, relators
        self.trees = {}
        for role, prefix in (("oracle", "output/geometry"), ("continuation", "output/fixed")):
            manifest_file = prefix + "/manifest.json"
            manifest = inputs.json(role, manifest_file)
            scope = inputs.parents[role]["files"][manifest_file]["sha256"]
            descriptors = {item["file"]: item for item in manifest["files"]}
            arrays = {}
            for name, shape in (("parent.u32", [54432]), ("parent-edge.u32", [54432]), ("next-pos.u32", [54432, 2])):
                descriptor = descriptors[name]
                raw = inputs.read(role, prefix + "/" + name)
                require(descriptor["dtype"] == "u32le" and descriptor["shape"] == shape and descriptor["bytes"] == len(raw) and
                        descriptor["sha256"] == sha(raw) and len(raw) == math.prod(shape) * 4, "tree_word_actual_typed_array")
                arrays[name] = np.frombuffer(raw, dtype="<u4").reshape(shape)
            parents, edges, nxt = arrays["parent.u32"], arrays["parent-edge.u32"], arrays["next-pos.u32"]
            require(int(parents[0]) == int(edges[0]) == 0xffffffff and not np.any(parents[1:] >= 54432) and
                    not np.any(edges[1:] >= 108864) and not np.any(nxt >= 54432), "tree_word_root_sentinel_and_full_array_bounds")
            require(np.array_equal(edges[1:] // 2, parents[1:]) and
                    np.array_equal(nxt[parents[1:].astype(np.int64), (edges[1:] % 2).astype(np.int64)], np.arange(1, 54432)),
                    "tree_word_parent_positive_edge_complete_join")
            self.trees[scope] = {"role": role, "prefix": prefix, "manifest_file": manifest_file, "arrays": arrays}
        for record in physical.raw_records.values():
            scope = record["raw"]["geometry_manifest_sha256"]
            expected_role = "oracle" if record["key_prefix"] == "external-e" else "continuation"
            require(scope in self.trees and self.trees[scope]["role"] == expected_role, "raw_word_actual_geometry_owner")

    def normalizers(self, raw_record: dict[str, Any]) -> None:
        value = raw_record["raw"]["normalizers"]
        size, digest = DATA_PINS["scratchpad/a0_v2_words.json"]
        typed_equal(value["dictionary"], {"file": "scratchpad/a0_v2_words.json", "bytes": size, "sha256": digest},
                    "raw_normalizer_actual_source_dictionary")
        require(value["raw_relators_sha256"] == "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a",
                "raw_normalizer_nineteen_roster")
        words = {item["name"]: item for item in value["words"]}
        for key in ("r_x", "r_y"):
            literal = self.relators["normalizer:" + key]
            require(words[key]["length"] == len(literal) and words[key]["word_sha256"] == sha(canonical(literal)[:-1]),
                    "same_normalizer_literal_at_actual_raw_use")

    def raw_pattern(self, key: str, scope: str) -> tuple[tuple[Any, ...], dict[str, Any], int]:
        if key.startswith("external-e/"):
            prefix, name = "external-e", key[len("external-e/"):]
        else:
            pieces = key.split("/", 2)
            require(len(pieces) == 3 and pieces[0] == "loop" and len(pieces[1]) == 6 and pieces[1].isascii() and pieces[1].isdecimal(),
                    "raw_e_key_snapshot_format")
            prefix, name = "/".join(pieces[:2]), pieces[2]
        require(prefix in self.physical.raw_records, "raw_e_only_accepted_committed_prefix")
        record = self.physical.raw_records[prefix]
        require(record["scope"] == scope and name in record["indices"], "raw_e_actual_scope_and_named_node")
        index = record["indices"][name]
        raw = record["raw"]["nodes"][index]
        op = raw["op"]
        def child(identifier: str) -> tuple[Any, ...]:
            require(identifier in record["indices"] and record["indices"][identifier] < index, "raw_e_actual_prior_named_dependency")
            return ref_pattern("raw-e", prefix + "/" + identifier, scope)
        if op == "Identity":
            require(set(raw) == {"id", "op"}, "raw_identity_fields")
            expected = ("Identity",)
        elif op == "Letter":
            require(set(raw) == {"id", "op", "letter"} and type(raw["letter"]) is int and raw["letter"] in (-2, -1, 1, 2), "raw_letter_fields")
            expected = ("Letter", raw["letter"])
        elif op == "Inverse":
            require(set(raw) == {"id", "op", "node"}, "raw_inverse_fields")
            expected = ("Inverse", child(raw["node"]))
        elif op == "IntegerPower":
            require(set(raw) == {"id", "op", "node", "exponent"}, "raw_power_fields")
            expected = power_pattern(child(raw["node"]), integer(raw["exponent"], "raw_ordinary_exponent"))
        elif op == "OrderedProduct":
            require(set(raw) == {"id", "op", "factors"} and type(raw["factors"]) is list, "raw_product_fields")
            expected = product_pattern(child(identifier) for identifier in raw["factors"])
        else:
            require(op == "Ref" and set(raw) == {"id", "op", "namespace", "key"}, "raw_reference_fields")
            if raw["namespace"] == "oracle-tree":
                vertex = integer(raw["key"], "raw_tree_vertex", 0, 54431)
                expected = ref_pattern("tree", vertex, record["raw"]["geometry_manifest_sha256"])
            else:
                require(raw["namespace"] == "normalizer-v459" and raw["key"] in ("r_x", "r_y"), "raw_normalizer_namespace")
                self.normalizers(record)
                expected = ref_pattern("normalizer", raw["key"], self.catalog.dictionary_hash)
        return expected, record, index

    def require_physical_sources(self, node: dict[str, Any], row: dict[str, Any]) -> None:
        role = row["role"]
        self.ancestors.require_use(node, "physical", role, row["instruction_file"],
            pointer=None if row["kind"] == "base" else "",
            offset=row["record_offset"], length=row["record_length"])
        binary = "state/physical.bin" if row["kind"] == "base" else row["prefix"] + "/physical-normalized.bin"
        offset = row["pivot"] * 12096 if row["kind"] == "base" else 0
        self.ancestors.require_use(node, "physical", role, binary, offset=offset, length=12096)
        if row["kind"] in ("legacy-seed", "refinement"):
            self.ancestors.require_use(node, "physical", role, row["materialization_file"], pointer=row["materialization_pointer"])
        elif row["kind"] == "packet":
            seed = row["selection"]["seed"]
            self.ancestors.require_use(node, "physical", "packet", "output/packet/relations.json", pointer=f"/seeds/{seed}")
        elif row["kind"] in ("external-e", "loop"):
            record = self.physical.raw_records[row["raw_key_prefix"]]
            self.ancestors.require_use(node, "physical", role, record["correction_file"], pointer="/p1_factors")
            self.ancestors.require_use(node, "physical", role, record["reductions_file"], pointer="/events")

    def check(self) -> dict[str, Any]:
        counts = {namespace: 0 for namespace in sorted(NAMESPACES)}
        with self.catalog.item.open("rb") as stream:
            for number in range(len(self.catalog.hashes)):
                node = self.catalog.read(stream, number)
                if node["op"] != "Ref":
                    continue
                args = node["args"]
                namespace, key, scope = args["namespace"], args["key"], args["scope_sha256"]
                if namespace == "p1":
                    identifier = decimal_key(key, "canonical_P1_Ref_key")
                    expected = self.source.p1_pattern(identifier)
                    require(scope == self.source.p1_scope, "canonical_P1_manifest_scope")
                    record = self.source.p1[identifier]
                    self.ancestors.require_use(node, namespace, "p1", "instructions.jsonl",
                        offset=record["instruction_offset"], length=record["instruction_length"])
                    segment = next(i for i in range(8) if P1_ORDER[i] <= identifier < P1_ORDER[i + 1])
                    owner, local = segment % 4, identifier - P1_ORDER[segment]
                    role = "prepare" if segment < 4 else f"block-{owner}"
                    pointer = f"/old_blocks/{owner}/record/dag_nodes/{local}" if segment < 4 else f"/dag_nodes/{local}"
                    self.ancestors.require_use(node, namespace, role, self.source.body_names[role], pointer=pointer)
                elif namespace == "old-defect":
                    identifier = decimal_key(key, "old_defect_Ref_key")
                    expected = self.source.defect_pattern(identifier)
                    require(scope == self.source.prepare_scope, "old_defect_prepare_body_scope")
                    self.ancestors.require_use(node, namespace, "prepare", self.source.prepare_name, pointer=f"/defect_origins/{identifier}")
                    record = self.source.defects[identifier]
                    owner = record["lower_character"]
                    suffix = (f"seed_reductions/{record['seed'] - 1}" if record["kind"] == "seed" else
                              f"actor_transitions/{record['pivot']}/{(1, -1, 2, -2).index(record['letter'])}")
                    self.ancestors.require_use(node, namespace, "prepare", self.source.prepare_name,
                        pointer=f"/old_blocks/{owner}/record/{suffix}")
                elif namespace in ("conn-lower", "conn-raw"):
                    identifier = decimal_key(key, "Conn_Ref_key")
                    expected = self.source.conn_pattern(namespace, identifier)
                    require(scope == self.source.base_scope, "Conn_base_state_manifest_scope")
                    record = self.source.lower[identifier] if namespace == "conn-lower" else self.source.connections[identifier]
                    self.ancestors.require_use(node, namespace, "state", "state/instructions.jsonl", offset=record["offset"], length=record["length"])
                elif namespace == "physical":
                    identifier = decimal_key(key, "physical_Ref_key")
                    integer(identifier, "physical_Ref_range", 0, len(self.physical.rows) - 1)
                    row = self.physical.rows[identifier]
                    require(scope == row["scope"], "physical_actual_instruction_scope")
                    expected = self.physical.pattern(identifier, self.relators)
                    self.require_physical_sources(node, row)
                elif namespace == "raw-e":
                    expected, record, index = self.raw_pattern(key, scope)
                    self.ancestors.require_use(node, namespace, record["role"], record["file"], pointer=f"/nodes/{index}")
                    raw = record["raw"]["nodes"][index]
                    if raw["op"] == "Ref" and raw["namespace"] == "normalizer-v459":
                        self.ancestors.require_use(node, namespace, record["role"], record["file"], pointer="/normalizers")
                elif namespace == "tree":
                    vertex = integer(decimal_key(key, "tree_Ref_key"), "tree_Ref_vertex", 0, 54431)
                    require(scope in self.trees, "tree_actual_geometry_or_fixed_scope")
                    tree = self.trees[scope]
                    if vertex == 0:
                        expected = ("Identity",)
                    else:
                        parent, edge = int(tree["arrays"]["parent.u32"][vertex]), int(tree["arrays"]["parent-edge.u32"][vertex])
                        expected = product_pattern([ref_pattern("tree", parent, scope), ("Letter", edge % 2 + 1)])
                    for filename in ("parent.u32", "parent-edge.u32"):
                        self.ancestors.require_use(node, namespace, tree["role"], tree["prefix"] + "/" + filename,
                            offset=vertex * 4, length=4)
                    if vertex:
                        self.ancestors.require_use(node, namespace, tree["role"], tree["prefix"] + "/next-pos.u32", offset=edge * 4, length=4)
                elif namespace == "normalizer":
                    require(key in ("r_x", "r_y") and scope == self.catalog.dictionary_hash, "normalizer_new_dictionary_scope")
                    expected = ("Rel", "normalizer:" + key)
                    matches = []
                    for raw in self.physical.raw_records.values():
                        try:
                            self.ancestors.require_use(node, namespace, raw["role"], raw["file"], pointer="/normalizers")
                        except ValueError:
                            continue
                        self.normalizers(raw); matches.append(raw["scope"])
                    require(matches, "normalizer_Ref_has_actual_sixteen_parent_use")
                else:
                    require(namespace == "target" and key == scope == self.inputs.selected["hashes"]["head"] and number == self.catalog.root_id,
                            "single_target_Ref_is_same_accepted_HEAD_root")
                    expected = self.physical.target_pattern()
                    self.ancestors.require_use(node, namespace, "continuation", "output/HEAD", pointer="")
                    for role, name in sorted({(row["role"], row["result_file"]) for row in self.physical.rows}):
                        self.ancestors.require_use(node, namespace, role, name,
                            pointer="/target_reduction" if role == "state" else "/target")
                expect_pattern(self.catalog, stream, args["word"]["node"], expected)
                counts[namespace] += 1
                boundary("Ref_actual_ordered_recipe_complete", namespace=namespace, count=counts[namespace])
            root = self.catalog.read(stream, self.catalog.root_id)
        require(root["op"] == "Ref" and root["args"]["namespace"] == "target" and counts["target"] == 1,
                "one_accepted_target_word_root")
        return sealed("recipe-bindings", {"same_root_id": self.catalog.root_id, "same_root_sha256": self.catalog.root_hash,
            "accepted_HEAD_sha256": self.inputs.selected["hashes"]["head"], "references": counts,
            "canonical_P1_recipes": 8059, "all_prior_child_recipes_compared": True,
            "saved_order_and_zero_coefficient_edges_retained": True, "fresh_rho2_packed_sha256": RHO2_PACKED_SHA,
            "old_numeric_insertions_replayed": 0, "old_numeric_scans_replayed": 0, "eof": True})


def rejected(action: Any, label: str) -> None:
    try:
        action()
    except (ValueError, RuntimeError):
        return
    raise ValueError("same_word:canary_accepted_mutation:" + label)


def fixture_catalog(root: Path, recipes: list[tuple[str, dict[str, Any]]], relators: dict[str, list[int]]) -> NodeCatalog:
    """Small protocol fixture, never an accepted current artifact."""
    nodes = []
    def prior(index: int) -> dict[str, Any]:
        return {"node": index, "sha256": nodes[index]["node_sha256"]}
    for index, (op, raw_args) in enumerate(recipes):
        args = copy.deepcopy(raw_args)
        if op in ("Inverse", "IntegerPower", "Ref"):
            args["word"] = prior(args["word"])
        elif op == "Act":
            args["word"], args["conjugator"] = prior(args["word"]), prior(args["conjugator"])
        elif op == "OrderedProduct":
            args["factors"] = [prior(child) for child in args["factors"]]
        elif op == "Rel":
            args.update({"dictionary_sha256": "d" * 64, "letters": relators[args["relator_id"]],
                         "letters_sha256": sha(canonical(relators[args["relator_id"]]))})
        node = {"id": index, "type": "F2-word", "op": op, "args": args, "receipt_refs": []}
        nodes.append({**node, "node_sha256": sha(canonical(node))})
    raw = b"".join(canonical(node) for node in nodes)
    root.mkdir()
    item = root / "ordered-word.jsonl"; item.write_bytes(raw)
    return NodeCatalog(item, {"file": item.name, "bytes": len(raw), "sha256": sha(raw), "nodes": len(nodes)},
                       len(nodes) - 1, nodes[-1]["node_sha256"], "d" * 64, relators, [])


def selftest() -> dict[str, Any]:
    """New D adapter boundaries only; no old successful suite or candidate replay."""
    tests = []
    floor = IndependentFloor()
    arithmetic = floor.arithmetic[1]
    x, y = floor.literal(1, [1]), floor.literal(1, [2])
    xy = arithmetic.product(x, y)
    require(xy == floor.literal(1, [1, 2]) and xy.endpoint != arithmetic.product(y, x).endpoint, "canary_noncommutative_product")
    require(arithmetic.inverse(xy) == arithmetic.product(arithmetic.inverse(y), arithmetic.inverse(x)) == floor.literal(1, [-2, -1]),
            "canary_inverse_reverses_product")
    acted = arithmetic.conjugate(x, y)
    require(acted == floor.literal(1, [1, 2, -1]), "canary_full_Act_flat_anchor")
    truncated: FoxRow = {}
    arithmetic.translate_add(truncated, y.row, x.endpoint, 1)
    require(acted.row != truncated, "canary_nonunit_child_requires_all_Act_terms")
    value, order = arithmetic.q.identity, None
    for count in range(1, 513):
        value = arithmetic.q.mul(value, x.endpoint)
        if value == arithmetic.q.identity:
            order = count; break
    require(order is not None, "canary_bounded_actual_marked_generator_order")
    closed = arithmetic.power(x, order)
    require(closed.endpoint == arithmetic.q.identity and closed.row and closed == floor.literal(1, [1] * order),
            "canary_endpoint_one_is_not_Fox_zero")
    rejected(lambda: arithmetic.unblob(floor.arithmetic[3].blob(floor.arithmetic[3].q.identity)), "E4_is_not_E3")
    require(floor.coarse.decode(arithmetic.q.mul(x.endpoint, y.endpoint)) == MAPS.amul(floor.coarse.decode(x.endpoint), floor.coarse.decode(y.endpoint)) and
            floor.coarse.decode(arithmetic.q.inverse(x.endpoint)) == MAPS.ainverse(floor.coarse.decode(x.endpoint)), "canary_full36_commuting_square")
    factors = {1: x, 2: xy, 3: y}
    native, reversed_native = arithmetic.identity(), arithmetic.identity()
    for ordinal, sign in PRINTED_NATIVE[1]:
        native = arithmetic.product(native, arithmetic.power(factors[ordinal], sign))
    for ordinal, sign in reversed(PRINTED_NATIVE[1]):
        reversed_native = arithmetic.product(reversed_native, arithmetic.power(factors[ordinal], sign))
    require(native == arithmetic.identity() and reversed_native != native, "canary_printed_native_reverse_order")
    tests.append({"name": "actual_nonunit_Act_inverse_typed_codec_endpoint_and_printed_order", "status": "PASS"})
    with tempfile.TemporaryDirectory(prefix="r07-same-word-D-") as temporary:
        root = Path(temporary)
        relators = literal_dictionary(floor)
        residues = fixture_catalog(root / "residue", [("Letter", {"letter": 1}), ("Letter", {"letter": 2}),
            ("IntegerPower", {"word": 0, "exponent": 18}), ("IntegerPower", {"word": 1, "exponent": 36}),
            ("OrderedProduct", {"factors": [2, 3]})], relators)
        pair = residues.normalized_pair()
        require(pair["exponent_residues"] == [18, 36] and pair["normalized_pair"] == [1, 2] and pair["divisible18"] == [True, True],
                "canary_same_root_mod54_then_18")
        rejected(lambda: typed_equal(pair, {**pair, "same_root_sha256": "0" * 64}, "different_normalized_root"), "different_normalized_root")
        raw = residues.item.read_bytes()
        residues.item.write_bytes(raw[:-1])
        rejected(lambda: NodeCatalog(residues.item, residues.descriptor, residues.root_id, residues.root_hash, "d" * 64, relators, []), "node_false_EOF")
        residues.item.write_bytes(raw)
        base_recipes = [("Rel", {"relator_id": "normalizer:r_x"}), ("Rel", {"relator_id": "normalizer:r_y"}),
            ("IntegerPower", {"word": 0, "exponent": 0}), ("IntegerPower", {"word": 1, "exponent": 0}),
            ("Ref", {"namespace": "normalizer", "key": "r_x", "scope_sha256": "d" * 64, "word": 0}),
            ("OrderedProduct", {"factors": [2, 3, 4]})]
        catalog = fixture_catalog(root / "recipe", base_recipes, relators)
        with catalog.item.open("rb") as stream:
            ref = catalog.read(stream, 4)
            expect_pattern(catalog, stream, ref["args"]["word"]["node"], ("Rel", "normalizer:" + ref["args"]["key"]))
        for field, value in (("word", 1), ("key", "r_y")):
            mutant = copy.deepcopy(base_recipes); mutant[4][1][field] = value
            altered = fixture_catalog(root / ("mutant-" + field), mutant, relators)
            with altered.item.open("rb") as stream:
                ref = altered.read(stream, 4)
                rejected(lambda: expect_pattern(altered, stream, ref["args"]["word"]["node"], ("Rel", "normalizer:" + ref["args"]["key"])),
                         "Ref_" + field + "_after_complete_reseal")
        tests.append({"name": "same_root_EOF_mod54_and_resealed_Ref_word_key_mutations", "status": "PASS"})

        fixture_root = root / "ancestor-fixture"; (fixture_root / "state").mkdir(parents=True)
        binary = bytes(12096) + bytes([1]) * 12096
        first, second = canonical({"offer": 0}), canonical({"offer": 1})
        (fixture_root / "state/physical.bin").write_bytes(binary)
        (fixture_root / "state/instructions.jsonl").write_bytes(first + second)
        files = {name: file_receipt(relative_file(fixture_root, name), name) for name in ("state/physical.bin", "state/instructions.jsonl")}
        fixture = type("RegisteredMetadataFixture", (), {})()
        fixture.roots = {"state": fixture_root}
        fixture.parents = {"state": {"files": files, "record": {"manifest": files["state/instructions.jsonl"]}}}
        entries = [{"id": 0, "namespace": "physical", "parent_role": "state",
            "parent_manifest_sha256": files["state/instructions.jsonl"]["sha256"], "file": "state/physical.bin",
            "file_sha256": sha(binary), "offset": 12096, "length": 12096, "record_sha256": sha(binary[12096:]), "json_pointer": None},
            {"id": 1, "namespace": "conn-raw", "parent_role": "state",
             "parent_manifest_sha256": files["state/instructions.jsonl"]["sha256"], "file": "state/instructions.jsonl",
             "file_sha256": sha(first + second), "offset": len(first), "length": len(second), "record_sha256": sha(second), "json_pointer": None}]
        def ancestor_document(records: list[dict[str, Any]]) -> dict[str, Any]:
            value = {"schema": WORD_SCHEMA + ".ancestor-index", "entries": records}
            return {**value, "sha256": sha(canonical(value))}
        AncestorIndex(fixture, ancestor_document(entries))
        for index in (0, 1):
            altered = copy.deepcopy(entries); altered[index]["length"] -= 1
            altered[index]["record_sha256"] = sha(binary[12096:-1] if index == 0 else second[:-1])
            rejected(lambda: AncestorIndex(fixture, ancestor_document(altered)), "binary_or_JSONL_truncated_record")
        current_lambda_type({"kind": "LinearMembershipCandidate", "lambda_sha256": None}, {"lambda_rho2": None})
        current_lambda_type({"kind": "Separator", "lambda_sha256": "1" * 64},
            {"lambda_rho2": {"mode": "derived", "original_rho2_packed_sha256": RHO2_PACKED_SHA}})
        rejected(lambda: current_lambda_type({"kind": "LinearMembershipCandidate", "lambda_sha256": None},
            {"lambda_rho2": {"mode": "derived"}}), "linear_lambda_must_be_null")
        rejected(lambda: current_lambda_type({"kind": "Separator", "lambda_sha256": "1" * 64}, {"lambda_rho2": None}), "separator_lambda_must_exist")
        identity = fixture_catalog(root / "identity", [("Identity", {})], relators)
        receipt = same_word_eleven(floor, identity, OutputFiles(root / "identity-eleven"), [0, 0], "e" * 64)
        require(len(receipt["slots"]["slots"]) == 11 and receipt["slots"]["slots"][0]["coordinate"] ==
                receipt["slots"]["slots"][4]["coordinate"] == 0 and receipt["full_filtered_coordinates_compared"] == 80644,
                "actual_eleven_adapter_duplicate_and_full_filtered_fixture")
        word_fixture = root / "thirteen-file-contract"; word_fixture.mkdir()
        owner_body = {"acceptance_sha256": "a" * 64, "accepted_owner_sha256": "b" * 64,
            "accepted_source_sha256": "c" * 64, "accepted_head_sha256": "d" * 64,
            "parent_roster_sha256": "e" * 64, "source_sha256": "f" * 64, "scope": WORD_SCOPE}
        for name in WORD_FILES:
            raw = identity.item.read_bytes() if name == "ordered-word.jsonl" else canonical(word_object(name[:-5],
                owner_body if name == "owner.json" else {"synthetic_contract_fixture": True}))
            (word_fixture / name).write_bytes(raw)
        owned = WordFiles(word_fixture)
        expect_word_document(owned, "owner.json", owner_body)
        owned.documents["owner.json"] = word_object("owner", {**owner_body, "accepted_owner_sha256": "0" * 64})
        rejected(lambda: expect_word_document(owned, "owner.json", owner_body), "resealed_wrong_accepted_owner")
        (word_fixture / ".unregistered").write_bytes(b"diagnostic is not a success payload\n")
        rejected(lambda: WordFiles(word_fixture), "word_root_unregistered_file")
        tests.append({"name": "actual_eleven_adapter_binary_JSONL_and_Linear_null_contracts", "status": "PASS",
                      "synthetic_contract_fixture": True, "actual_current_target_zero_claimed": False,
                      "owner_and_exact_thirteen_file_contract": True})
    return sealed("selftest", {"status": "PASS", "tests": tests, "old_success_suites": 0,
        "actual_parent_artifact_replayed": False, "candidate": True, "cross_checked": False, "verified": False})


WORD_FILES = frozenset(("source.json", "owner.json", "parent-roster.json", "fresh-rho2.json", "context.json",
    "literal-dictionary.json", "target-history.json", "ancestor-index.json", "ordered-word.jsonl",
    "word-manifest.json", "normalized-pair.json", "result.json", "manifest.json"))


class WordFiles:
    """All candidate bytes belong to one immutable, flat thirteen-file root."""
    def __init__(self, root: Path):
        self.root = root.resolve()
        files, directories = regular_tree(self.root)
        require(not directories and {item["file"] for item in files} == WORD_FILES and len(files) == len(WORD_FILES),
                "word_root_complete_exact_thirteen_files")
        self.roster = files
        self.files = {item["file"]: item for item in files}
        self.documents: dict[str, dict[str, Any]] = {}
        for name in sorted(WORD_FILES - {"ordered-word.jsonl"}):
            raw = relative_file(self.root, name).read_bytes()
            require(len(raw) == self.files[name]["bytes"] and sha(raw) == self.files[name]["sha256"], "word_file_stable_at_parse")
            value = exact_json(raw, "word:" + name)
            self.documents[name] = seal_check(value, WORD_SCHEMA + "." + name[:-5], "word_document_seal:" + name)

    def digest(self, name: str) -> str:
        require(name in self.files, "word_known_file_digest")
        return self.files[name]["sha256"]

    def finish_unchanged(self) -> None:
        files, directories = regular_tree(self.root)
        typed_equal(files, self.roster, "all_thirteen_word_files_unchanged")
        require(not directories, "word_no_directory_added")


def compare_normalized_pair(words: WordFiles, catalog: NodeCatalog) -> dict[str, Any]:
    actual = catalog.normalized_pair()
    expected = {"schema": WORD_SCHEMA + ".normalized-pair", "word_manifest_sha256": words.digest("word-manifest.json"), **actual}
    expected["sha256"] = sha(canonical(expected))
    typed_equal(words.documents["normalized-pair.json"], expected, "producer_C_receipt_equals_independent_same_root_mod54_18")
    return sealed("normalized-pair", {"status": "PASS", "word_manifest_sha256": words.digest("word-manifest.json"),
        "compared_producer_receipt_sha256": words.digest("normalized-pair.json"), **actual,
        "full_ordered_node_EOF": True, "candidate": True, "cross_checked": False, "verified": False})


def configure_resources(args: argparse.Namespace) -> None:
    global STARTED, DEADLINE, MAX_RSS_BYTES
    require(type(args.max_seconds) is float and math.isfinite(args.max_seconds) and args.max_seconds > 0,
            "explicit_positive_finite_deadline")
    integer(args.max_memory_mib, "explicit_positive_memory_bound", 1)
    STARTED = time.monotonic()
    DEADLINE = STARTED + args.max_seconds
    MAX_RSS_BYTES = args.max_memory_mib * 1024**2
    if hasattr(signal, "setitimer"):
        def resource_alarm(signum: int, frame: Any) -> None:
            boundary(LAST_PHASE)
        signal.signal(signal.SIGALRM, resource_alarm)
        # This also bounds retained typed codecs and full filtered maps while they run.
        signal.setitimer(signal.ITIMER_REAL, min(1.0, args.max_seconds), 1.0)


def clear_resource_alarm() -> None:
    if hasattr(signal, "setitimer"):
        signal.setitimer(signal.ITIMER_REAL, 0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    for role in PARENT_ROLES:
        if not role.startswith("block-"):
            parser.add_argument("--" + role + "-root", type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    parser.add_argument("--acceptance", type=Path)
    parser.add_argument("--word-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-seconds", type=float, required=True)
    parser.add_argument("--max-memory-mib", type=int, required=True)
    parser.add_argument("--producer-max-seconds", type=int)
    parser.add_argument("--producer-max-memory-mib", type=int)
    parser.add_argument("--selftest", action="store_true")
    return parser.parse_args()


def validate_actual_paths(args: argparse.Namespace) -> None:
    def no_reparse(item: Path) -> None:
        for component in (item, *item.parents):
            require(not component.is_symlink() and not component.is_junction(), "CLI_path_no_reparse_component")
    roots = [getattr(args, role.replace("-", "_") + "_root") for role in PARENT_ROLES if not role.startswith("block-")]
    require(all(type(item) is Path or isinstance(item, Path) for item in roots) and len(args.block_root) == 4 and
            isinstance(args.acceptance, Path) and isinstance(args.word_root, Path) and isinstance(args.output, Path),
            "actual_CLI_requires_sixteen_roots_acceptance_word_and_output")
    inputs = [*roots, *args.block_root, args.word_root]
    for item in inputs:
        no_reparse(item.absolute())
        require(item.is_dir(), "actual_CLI_input_directory")
    no_reparse(args.acceptance.absolute())
    require(args.acceptance.is_file(), "actual_CLI_acceptance_file")
    no_reparse(args.output.absolute())
    require(not args.output.exists(), "actual_CLI_output_new")
    resolved = [item.resolve() for item in inputs] + [args.output.resolve()]
    require(len(set(resolved)) == len(resolved) and all(left not in right.parents and right not in left.parents
            for index, left in enumerate(resolved) for right in resolved[index + 1:]), "all_CLI_roots_disjoint_before_any_write")
    require(args.output.resolve() not in args.acceptance.resolve().parents, "output_does_not_contain_acceptance")
    integer(args.producer_max_seconds, "actual_CLI_explicit_producer_deadline", 1)
    integer(args.producer_max_memory_mib, "actual_CLI_explicit_producer_memory_bound", 1)


def complete_output_report(output: OutputFiles, body: dict[str, Any], *, complete: bool) -> dict[str, Any]:
    """A partial directory can carry only a diagnostic receipt, never a complete PASS."""
    require(complete or body["status"] != "PASS", "no_partial_success_receipt")
    if complete:
        actual, directories = regular_tree(output.root)
        expected = [{key: value[key] for key in ("file", "bytes", "sha256")} for value in output.files.values()]
        typed_equal(actual, sorted(expected, key=lambda value: value["file"]), "complete_checker_output_exact_roster_before_final_seal")
        manifest = sealed("manifest", {"files": [copy.deepcopy(output.files[name]) for name in sorted(output.files)],
            "directories": directories, "eof": True, "all_compared": body["status"] == "PASS",
            "candidate": True, "cross_checked": False, "verified": False})
        manifest_receipt = output.json("manifest.json", manifest)
    else:
        manifest_receipt = None
    record = sealed("checker-result", {**body, "manifest": manifest_receipt,
        "complete_receipt": complete, "elapsed_seconds": round(time.monotonic() - STARTED, 6),
        "candidate": True, "cross_checked": False, "verified": False})
    output.json("checker-result.json", record)
    return record


WORD_SCOPE = {"source_lower_trits": 96776, "physical_lower_trits": 32260, "physical_top_trits": 48384,
    "p1_rows": 8059, "character_order": [0, 1, 2, 3], "unique_occurrences": 10,
    "occurrence_order": [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9], "current_grade": "v478-(2.7)-PB4-dropped",
    "word_group": "F2", "actor_convention": "P*W*P^-1", "normalized_modulus": 54,
    "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False}


def word_object(kind: str, body: dict[str, Any], *, assurance: bool = True) -> dict[str, Any]:
    value = {"schema": WORD_SCHEMA + "." + kind, **copy.deepcopy(body)}
    if assurance:
        value.update({"candidate": True, "cross_checked": False, "verified": False})
    require("sha256" not in value, "expected_word_object_has_no_existing_seal")
    return {**value, "sha256": sha(canonical(value))}


def expect_word_document(words: WordFiles, name: str, body: dict[str, Any], *, assurance: bool = True) -> None:
    typed_equal(words.documents[name], word_object(name[:-5], body, assurance=assurance), "entire_public_word_document:" + name)


def word_raw_sources() -> list[dict[str, Any]]:
    return [{"file": name, "bytes": DATA_PINS[name][0], "sha256": DATA_PINS[name][1]} for name in
            ("scratchpad/a0_paper_words_v1.json", "scratchpad/a0_v2_words.json", "scratchpad/fuda1_a0_rmax_data.g")]


def normalizer_word_records(relators: dict[str, list[int]]) -> list[dict[str, Any]]:
    records = []
    for name, root, exponent in (("r_x", "r_x", 1), ("r_y", "r_y", 1), ("c_x", "r_x", 9), ("c_y", "r_y", 9)):
        literal = relators["normalizer:" + root] * exponent
        records.append({"name": name, "length": len(literal), "word_sha256_without_LF": sha(canonical(literal)[:-1])})
    return records


def compare_word_intake(words: WordFiles, inputs: AcceptedInputs, source: SourceRecipes,
                        rho2: dict[str, Any], relators: dict[str, list[int]]) -> None:
    hashes = inputs.selected["hashes"]
    expect_word_document(words, "parent-roster.json", {"acceptance_sha256": inputs.acceptance_sha,
        "parents": inputs.acceptance["parents"], "all_files_and_directories_authenticated": True})
    expect_word_document(words, "source.json", {"acceptance_sha256": inputs.acceptance_sha,
        "consumer_sources": inputs.acceptance["consumer_sources"], "raw_sources": word_raw_sources(),
        "runtime": inputs.acceptance["runtime"], "accepted_continuation_source_sha256": hashes["source"],
        "arithmetic_imports": [], "old_numerical_replay": False})
    expect_word_document(words, "owner.json", {"acceptance_sha256": inputs.acceptance_sha,
        "accepted_owner_sha256": hashes["owner"], "accepted_source_sha256": hashes["source"],
        "accepted_head_sha256": hashes["head"], "parent_roster_sha256": words.digest("parent-roster.json"),
        "source_sha256": words.digest("source.json"), "scope": WORD_SCOPE})
    fresh_names = ("task640-payload/manifest.json", "task640-verdict.json", "task640-payload/rho2.bin",
        "task640-payload/rho2-dense.bin", "task640-payload/lower-dense.bin", "task640-payload/target-dense.bin",
        "task640-payload/authenticated-roots.json")
    expect_word_document(words, "fresh-rho2.json", {"artifact": inputs.parents["rho2"]["record"]["artifact"],
        "files": [inputs.parents["rho2"]["files"][name] for name in fresh_names],
        "manifest_sha256": rho2["manifest_sha256"], "packed_sha256": rho2["packed_sha256"],
        "manifest": rho2["manifest"], "verdict": inputs.json("rho2", "task640-verdict.json"),
        "direct_payload_parent": True, "derived_target_identity_used_as_direct_bytes": False})
    expect_word_document(words, "context.json", {"accepted_owner_sha256": hashes["owner"],
        "accepted_source_sha256": hashes["source"], "fresh_rho2_manifest_sha256": rho2["manifest_sha256"],
        "task712_manifest_sha256": TASK712_MANIFEST[1], "p1_manifest_sha256": source.p1_scope,
        "prepare_body_sha256": source.prepare_scope,
        "block_body_sha256": [inputs.parents[f"block-{owner}"]["files"][source.body_names[f"block-{owner}"]]["sha256"] for owner in range(4)],
        "canonical_index_sha256": inputs.parents["continuation"]["files"]["output/fixed/canonical-index.json"]["sha256"],
        "scope": WORD_SCOPE, "aggregation": "printed-v478-(2.7)-PB4-dropped", "same_word_all_occurrences_required": True})
    expect_word_document(words, "literal-dictionary.json", {"relators": relators, "raw_sources": word_raw_sources(),
        "paper_relators_pointer": "/relators", "normalizer_relators_pointer": "/raw_q0_relators",
        "normalizer_raw_roster_sha256_without_LF": "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a",
        "normalizer_words": normalizer_word_records(relators),
        "normalizer_recipe": {"r_x": "free(q1*q6^-2*q7^4*q9)", "r_y": "free(q8^-1*q4^-1)"},
        "pure_order": [list(parity) for parity in CHARACTERS], "central_representative": "sr(0,1,2)=(0,1,-1)",
        "relator_normal_closure_claim": False, "eof": True}, assurance=False)
    ancestors = words.documents["ancestor-index.json"]
    expect_word_document(words, "ancestor-index.json", {"parent_roster_sha256": words.digest("parent-roster.json"),
        "owner_sha256": words.digest("owner.json"), "source_sha256": words.digest("source.json"),
        "entries": ancestors["entries"], "eof": True}, assurance=False)
    boundary("whole_word_intake_receipts_compared")


def physical_raw_recipe(row: dict[str, Any]) -> dict[str, Any]:
    kind, role = row["kind"], row["role"]
    if kind == "base":
        return {"kind": "conn", "offer": row["instruction"]["offer"]}
    if kind == "legacy-seed":
        return {"kind": "legacy-seed", "parent_role": role, "file": row["materialization_file"], "pointer": "/ancestry"}
    if kind == "packet":
        selection = row["selection"]
        return {"kind": "packet-seed", "parent_role": "packet", "file": "output/packet/relations.json",
            "pointer": f"/seeds/{selection['seed']}", "seed": selection["seed"], "character": selection["character"]}
    if kind == "refinement":
        return {"kind": "refinement", "parent_role": "refinement", "file": row["materialization_file"], "pointer": ""}
    require(kind in ("external-e", "loop"), "target_history_E_recipe_kind")
    external = kind == "external-e"
    base = "output" if external else f"output/snapshots/{row['step'] - 1:06d}/e"
    key = "external-e" if external else f"loop/{row['step'] - 1:06d}"
    return {"kind": "e", "parent_role": role, "base": base, "key": key,
        "raw_file": base + ("/raw-word.json" if external else "/raw/raw-word.json"),
        "primal_file": base + ("/p1-reductions.json" if external else "/primal/p1-reductions.json"),
        "source_correction_file": base + ("/source-correction.json" if external else "/p1/source-correction.json"),
        "p1_roots_file": base + ("/p1-roots.json" if external else "/p1/p1-roots.json"),
        "physical_literal_file": base + ("/physical-literal.json" if external else "/physical/physical-literal.json"),
        "B_file": None if external else base + "/B/B.json",
        "geometry_role": "oracle" if external else "continuation", "geometry_base": "output/geometry" if external else "output/fixed",
        "witness_role": "oracle" if external else "continuation",
        "witness_file": "output/tree/witness.json" if external else f"output/snapshots/{row['step'] - 1:06d}/tree/witness.json"}


def target_parent_history(inputs: AcceptedInputs, source: SourceRecipes, physical: PhysicalRecipes) -> list[dict[str, Any]]:
    """Reconstruct the named subtractive identities from saved metadata, including Linear's final delta."""
    base = inputs.json("state", "output/result.json")
    target = base["target_reduction"]
    state_head, previous_remainder = target["state_head"], target["remainder_sha256"]
    require(state_head == source.base_records[-1]["value"]["rolling_sha256"], "base_target_complete_instruction_head")
    parents = [{"role": "base", "manifest_sha256": source.base_scope,
        "result_sha256": inputs.parents["state"]["files"]["output/result.json"]["sha256"],
        "state_head": state_head, "target_sha256": sha(canonical(target))}]
    for row in physical.rows[1354:]:
        kind, role = row["kind"], row["role"]
        instruction, target = row["instruction"], row["result"]["target"]
        require(instruction["predecessor"] == state_head, "target_history_contiguous_saved_state_head")
        parent_field = "old_remainder_sha256" if kind == "legacy-seed" else "parent_remainder_sha256"
        require(target[parent_field] == previous_remainder, "target_history_contiguous_actual_remainder")
        target_file = row["prefix"] + "/target-remainder.bin"
        require(target["remainder_sha256"] == inputs.parents[role]["files"][target_file]["sha256"], "target_history_actual_saved_residual_file")
        if kind == "legacy-seed":
            name = "seed30" if role == "delta" else "seed34"
            manifest_file = "output/manifest.json"
        elif kind in ("packet", "refinement"):
            name = kind + "-step-" + str(int(row["prefix"].rsplit("/", 1)[1]))
            manifest_file = row["prefix"] + "/manifest.json"
        elif kind == "external-e":
            name, manifest_file = "external-e", "output/manifest.json"
        else:
            require(kind == "loop", "target_history_registered_delta_kind")
            name, manifest_file = f"loop-e-{row['step']:06d}", f"output/steps/{row['step']:06d}/manifest.json"
            if row["step"] == 1:
                require(len(parents) == 33, "accepted_start_exact_33_target_parents")
                typed_equal(parents, inputs.selected["values"]["start"]["accepted_target_derivation_parents"], "accepted_start_named_parent_identities")
            snapshot_file = f"output/snapshots/{row['step'] - 1:06d}/start.json"
            snapshot = seal_check(inputs.json(role, snapshot_file), "d972.r07.complete-oracle-cegar-continuation.v1.snapshot", "target_history_snapshot_seal")
            typed_equal(snapshot["accepted_target_derivation_parents"], parents, "snapshot_frozen_pre_append_parent_identities")
            require(snapshot["state_head"] == state_head and snapshot["target_remainder_sha256"] == previous_remainder and
                    snapshot["rank"] == row["pivot"] and snapshot["generation"] == instruction["offer"], "target_history_actual_snapshot_before_delta")
            derivation = row["result"]["target_derivation"]
            typed_equal(derivation["accepted_target_derivation_parents"], parents, "E_delta_frozen_previous_named_parents")
            require(derivation["mode"] == "derived" and derivation["original_rho2_directly_read"] is False and
                    derivation["original_rho2_packed_sha256"] == RHO2_PACKED_SHA and
                    derivation["identity"] == "parent_remainder - new_remainder = target.scalar * new_normalized_row",
                    "E_actual_derived_identity_type")
            typed_equal(derivation["new_delta"], {"instruction_sha256": row["scope"], "state_head": instruction["rolling_sha256"],
                "normalized_sha256": row["row_sha256"], "target_sha256": sha(canonical(target))}, "E_actual_new_delta_identity")
            step = inputs.json(role, manifest_file)
            require(step["step"] == row["step"] and step["parent_state_head"] == state_head and
                    step["state_head"] == instruction["rolling_sha256"] and step["instruction_sha256"] == row["scope"] and
                    step["result_sha256"] == row["result_sha256"] and step["physical_normalized_sha256"] == row["row_sha256"] and
                    step["snapshot_sha256"] == inputs.parents[role]["files"][snapshot_file]["sha256"] and
                    step["target_remainder_sha256"] == target["remainder_sha256"], "named_delta_same_committed_step_manifest")
        entry = {"role": name, "manifest_sha256": inputs.parents[role]["files"][manifest_file]["sha256"],
            "result_sha256": row["result_sha256"], "state_head": instruction["rolling_sha256"], "target_sha256": sha(canonical(target))}
        if kind in ("external-e", "loop"):
            entry["instruction_sha256"] = row["scope"]
        parents.append(entry)
        state_head, previous_remainder = instruction["rolling_sha256"], target["remainder_sha256"]
    head = inputs.selected["values"]["head"]
    require(state_head == head["state_head"] and previous_remainder == head["target_remainder_sha256"] and
            len(parents) == 33 + head["completed_steps"], "entire_target_parent_history_to_actual_HEAD")
    if head["completed_steps"] == 0:
        typed_equal(parents, inputs.selected["values"]["start"]["accepted_target_derivation_parents"], "zero_new_steps_named_parent_identities")
    if head["kind"] == "Separator":
        for name in ("result", "checker"):
            typed_equal(inputs.selected["values"][name]["lambda_rho2"]["accepted_target_derivation_parents"], parents,
                        "current_separator_named_parent_closure:" + name)
    else:
        require(inputs.selected["values"]["result"]["lambda_rho2"] is None and
                inputs.selected["values"]["checker"]["lambda_rho2"] is None, "Linear_parent_history_never_reads_null_lambda")
    return parents


def compare_target_history(words: WordFiles, inputs: AcceptedInputs, source: SourceRecipes,
                           physical: PhysicalRecipes, ancestors: AncestorIndex) -> dict[str, Any]:
    history = words.documents["target-history.json"]
    require(type(history["pivots"]) is list and len(history["pivots"]) == len(physical.rows), "target_history_all_pivot_records")
    base_target_sha = sha(canonical(inputs.json("state", "output/result.json")["target_reduction"]))
    def exact_ref(identifier: int, namespace: str, role: str, name: str, pointer: str | None,
                  offset: int | None, length: int | None, record_sha: str) -> None:
        integer(identifier, "target_history_ancestor_ID", 0, len(ancestors.entries) - 1)
        typed_equal(ancestors.entries[identifier], {"id": identifier, "namespace": namespace, "parent_role": role,
            "parent_manifest_sha256": inputs.parents[role]["record"]["manifest"]["sha256"],
            "file": name, "file_sha256": inputs.parents[role]["files"][name]["sha256"],
            "offset": offset, "length": length, "record_sha256": record_sha, "json_pointer": pointer},
            "target_history_exact_ancestor_position_and_type")
    pivots = []
    for row, published in zip(physical.rows, history["pivots"], strict=True):
        instruction, role, base = row["instruction"], row["role"], row["kind"] == "base"
        require(type(published) is dict, "target_history_pivot_object")
        refs = {name: published[name] for name in ("physical_recipe_ref", "row_ref", "target_delta_ref")}
        exact_ref(refs["physical_recipe_ref"], "physical", role, row["instruction_file"], None if base else "",
            row["record_offset"], row["record_length"], source.base_records[instruction["offer"]]["sha256"] if base else row["scope"])
        exact_ref(refs["row_ref"], "physical", role, "state/physical.bin" if base else row["prefix"] + "/physical-normalized.bin",
                  None, row["pivot"] * 12096 if base else 0, 12096, row["row_sha256"])
        exact_ref(refs["target_delta_ref"], "target", role, row["result_file"], "/target_reduction" if base else "/target",
                  None, None, base_target_sha if base else sha(canonical(row["result"]["target"])))
        raw_recipe = physical_raw_recipe(row)
        if raw_recipe["kind"] == "e":
            for name in ("raw_file", "primal_file", "source_correction_file", "p1_roots_file", "physical_literal_file", "B_file"):
                require(raw_recipe[name] is None or raw_recipe[name] in inputs.parents[role]["files"], "E_raw_recipe_all_registered_parent_files")
            require(raw_recipe["geometry_base"] + "/manifest.json" in inputs.parents[raw_recipe["geometry_role"]]["files"] and
                    raw_recipe["witness_file"] in inputs.parents[raw_recipe["witness_role"]]["files"], "E_raw_recipe_actual_geometry_witness")
        expected = {"pivot_id": row["pivot"], "offer": instruction["offer"], "lead": instruction["lead"], "sigma": instruction["sigma"],
            "target_scalar": row["coefficient"] % 3, "literal_exponent": row["coefficient"], **refs,
            "scope_sha256": row["scope"], "raw_recipe": raw_recipe, "state_head": instruction["rolling_sha256"]}
        typed_equal(published, expected, "target_history_same_saved_pivot_and_literal_recipe")
        pivots.append(expected)
        if row["pivot"] % 128 == 0:
            boundary("target_history_pivot_refs", pivots=row["pivot"] + 1)
    lower_ids = {record["value"]["offer"]: index for index, record in enumerate(source.lower)}
    base_offers = []
    for record in source.base_records:
        value = record["value"]
        base_offers.append({"offer": value["offer"], "offset": record["offset"], "length": record["length"],
            "sha256": record["sha256"], "physical_kind": value["kind"], "conn_kind": value["source"]["kind"],
            "lower_pivot_id": lower_ids.get(value["offer"]), "p1_source": copy.deepcopy(value["source"]["source"])})
    head, hashes = inputs.selected["values"]["head"], inputs.selected["hashes"]
    count = head["completed_steps"]
    residual_role = "continuation" if count else "e"
    residual_name = f"output/snapshots/{count - 1:06d}/e/physical/target-remainder.bin" if count else "output/target-remainder.bin"
    zero = not bool(np.any(inputs.selected["target"]))
    expected = {"accepted_head_sha256": hashes["head"], "accepted_result_sha256": hashes["result"],
        "accepted_checker_sha256": hashes["checker"], **{name: head[name] for name in
            ("completed_steps", "rank", "generation", "state_head", "kind")}, "terminal": inputs.acceptance["selected"]["terminal"],
        "pivots": pivots, "base_offers": base_offers, "lower_pivot_offers": [record["value"]["offer"] for record in source.lower],
        "target_scalars": [row["coefficient"] % 3 for row in physical.rows],
        "residual": {"parent_role": residual_role, **inputs.parents[residual_role]["files"][residual_name], "trits": 48384, "zero": zero},
        "original_rho2_packed_sha256": RHO2_PACKED_SHA, "target_derivation_mode": "DERIVED_FROM_ACCEPTED_NUMERICAL_PARENTS",
        "accepted_target_derivation_parents": target_parent_history(inputs, source, physical),
        "identity": "rho2 = residual + insertion_order_sum(target_scalar * normalized_physical_row)",
        "positive_applicability": "LINEAR_ZERO_CANDIDATE" if zero else "NOT_APPLICABLE",
        "uncommitted_tail_appended": False, "old_numerical_replay": False, "eof": True}
    expect_word_document(words, "target-history.json", expected)
    return expected


def compare_word_root_manifest(words: WordFiles, inputs: AcceptedInputs, physical: PhysicalRecipes,
                               catalog: NodeCatalog, ancestors: AncestorIndex) -> None:
    streams = []
    for key, record in physical.raw_records.items():
        raw, role = record["raw"], record["role"]
        external = key == "external-e"
        geometry_role, geometry_file = ("oracle", "output/geometry/manifest.json") if external else ("continuation", "output/fixed/manifest.json")
        witness_role, witness_file = ("oracle", "output/tree/witness.json") if external else ("continuation", "output/snapshots/" + key.split("/")[1] + "/tree/witness.json")
        require(raw["geometry_manifest_sha256"] == inputs.parents[geometry_role]["files"][geometry_file]["sha256"] and
                raw["witness_sha256"] == inputs.parents[witness_role]["files"][witness_file]["sha256"], "raw_stream_actual_witness_geometry_hashes")
        stream = raw["word_stream"]
        require(type(stream) is dict and set(stream) == {"encoding", "letters", "bytes", "sha256", "full_eof"} and
                stream["encoding"] == "signed-byte:1=01,-1=ff,2=02,-2=fe" and stream["full_eof"] is True,
                "raw_stream_signed_byte_full_EOF_contract")
        require(integer(stream["letters"], "raw_stream_letters", 0) == integer(stream["bytes"], "raw_stream_bytes", 0), "raw_stream_one_byte_per_letter")
        hash_string(stream["sha256"], "raw_stream_separate_actual_word_hash")
        require(type(raw["eta"]) is list and len(raw["eta"]) == 2, "raw_two_auxiliary_coefficients")
        for scalar in raw["eta"]:
            integer(scalar, "raw_eta_F3", 0, 2)
        streams.append({"key": key, "parent_role": role, "raw_word_file": record["file"], "raw_word_sha256": record["scope"],
            "witness_sha256": raw["witness_sha256"], "geometry_manifest_sha256": raw["geometry_manifest_sha256"],
            "word_stream": stream, "eta": raw["eta"], "literal_root": "raw-root"})
    symbols = [{"namespace": symbol[0], "key": symbol[1], "scope_sha256": symbol[2], "node": node,
                "node_sha256": catalog.hashes[node]} for symbol, node in sorted(catalog.symbols.items(), key=lambda item: item[1])]
    expect_word_document(words, "word-manifest.json", {"grammar": "prior-only-ordered-F2-eight-ops-v1",
        "owner_sha256": words.digest("owner.json"), "source_sha256": words.digest("source.json"),
        "context_manifest_sha256": words.digest("context.json"), "fresh_rho2_manifest_sha256": RHO2_MANIFEST[1],
        "parent_roster_sha256": words.digest("parent-roster.json"), "accepted_head_sha256": inputs.selected["hashes"]["head"],
        "target_history_sha256": words.digest("target-history.json"), "ancestor_index_sha256": words.digest("ancestor-index.json"),
        "literal_dictionary_sha256": words.digest("literal-dictionary.json"), "nodes_file": catalog.descriptor,
        "root_id": catalog.root_id, "root_sha256": catalog.root_hash, "character_order": [0, 1, 2, 3],
        "actor_convention": "P*W*P^-1", "central_representative": "sr(0,1,2)=(0,1,-1)",
        "coefficient_rule": "saved-F3-to-signed-integer-once", "eof": True, "raw_streams": streams,
        "literal_dependency_closure": {"prior_only": True, "symbol_order": symbols, "all_used_edges_preserved": True},
        "input_receipts": len(ancestors.entries)})


def compare_producer_terminal(words: WordFiles, inputs: AcceptedInputs, catalog: NodeCatalog,
                              normalized: dict[str, Any], args: argparse.Namespace) -> None:
    hashes, head = inputs.selected["hashes"], inputs.selected["values"]["head"]
    expect_word_document(words, "manifest.json", {"owner_sha256": words.digest("owner.json"),
        "source_sha256": words.digest("source.json"), "accepted_head_sha256": hashes["head"],
        "word_manifest_sha256": words.digest("word-manifest.json"), "target_history_sha256": words.digest("target-history.json"),
        "normalized_pair_sha256": words.digest("normalized-pair.json"), "root_id": catalog.root_id, "root_sha256": catalog.root_hash,
        "file_roster": sorted(WORD_FILES), "files": [words.files[name] for name in sorted(WORD_FILES - {"manifest.json", "result.json"})],
        "all_inputs_unchanged": True})
    value = words.documents["result.json"]
    elapsed, limits = value["elapsed_seconds"], value["resource_limits"]
    require(type(elapsed) in (int, float) and math.isfinite(elapsed) and elapsed >= 0, "producer_authenticated_finite_elapsed_time")
    require(type(limits) is dict and set(limits) == {"max_seconds", "max_memory_mib"} and
            type(limits["max_seconds"]) is int and limits["max_seconds"] > 0 and
            limits["max_seconds"] == args.producer_max_seconds and type(limits["max_memory_mib"]) is int and
            limits["max_memory_mib"] == args.producer_max_memory_mib, "producer_resource_declaration_matches_registered_CLI")
    zero = not bool(np.any(inputs.selected["target"]))
    pair = normalized["normalized_pair"]
    expected = {"status": "PASS", "terminal": "POSITIVE_WORD_CANDIDATE" if zero else "NOT_APPLICABLE",
        "positive_applicability": "LINEAR_ZERO_CANDIDATE" if zero else "NOT_APPLICABLE",
        "positive_readout": "PENDING_SAME_WORD_D_AND_SIDE_CONDITIONS" if zero and pair == [0, 0] else "NOT_APPLICABLE",
        "manifest_sha256": words.digest("manifest.json"), "owner_sha256": words.digest("owner.json"), "source_sha256": words.digest("source.json"),
        "parent_roster_sha256": words.digest("parent-roster.json"), "context_manifest_sha256": words.digest("context.json"),
        "fresh_rho2_manifest_sha256": RHO2_MANIFEST[1], "word_manifest_sha256": words.digest("word-manifest.json"),
        "target_history_sha256": words.digest("target-history.json"), "ancestor_index_sha256": words.digest("ancestor-index.json"),
        "normalized_pair_sha256": words.digest("normalized-pair.json"), "accepted_head_sha256": hashes["head"],
        "accepted_checker_sha256": hashes["checker"], **{key: head[key] for key in ("completed_steps", "rank", "generation", "state_head")},
        "target_remainder_sha256": head["target_remainder_sha256"], "residual_zero": zero, "normalized_pair": pair,
        "normalized_zero": pair == [0, 0], "root_id": catalog.root_id, "root_sha256": catalog.root_hash, "nodes": len(catalog.hashes),
        "source_lower_zero": "NOT_ASSERTED_FOR_WHOLE_TARGET_WORD", "old_numerical_replays": 0, "same_word_B_C": True,
        "same_word_D": False, "eleven_slot_replay": False, "side_conditions": "PENDING", "grade2_member": "NOT_DECIDED",
        "grade2_nonmember": "NOT_DECIDED", "full_A0": False, "parent_inputs_unchanged": True, "eof": True,
        "resource_limits": limits, "elapsed_seconds": elapsed}
    expect_word_document(words, "result.json", expected)
    boundary("all_thirteen_producer_files_authenticated_and_compared")


def check_actual(args: argparse.Namespace, output: OutputFiles) -> dict[str, Any]:
    inputs = AcceptedInputs(args)
    words = WordFiles(args.word_root)
    floor = IndependentFloor()
    relators = literal_dictionary(floor)
    source = SourceRecipes(inputs)
    physical = PhysicalRecipes(inputs, source)
    rho2 = original_rho2(inputs.roots["rho2"])
    compare_word_intake(words, inputs, source, rho2, relators)
    ancestors = AncestorIndex(inputs, words.documents["ancestor-index.json"], source.basis_blobs)
    manifest = words.documents["word-manifest.json"]
    catalog = NodeCatalog(relative_file(words.root, "ordered-word.jsonl"), manifest["nodes_file"], manifest["root_id"],
                          manifest["root_sha256"], words.digest("literal-dictionary.json"), relators, ancestors.entries)
    recipes = RefRecipes(inputs, ancestors, source, physical, catalog, relators)
    recipe_receipt = output.json("recipe-bindings.json", recipes.check())
    history = compare_target_history(words, inputs, source, physical, ancestors)
    compare_word_root_manifest(words, inputs, physical, catalog, ancestors)
    normalized = compare_normalized_pair(words, catalog)
    normalized_receipt = output.json("normalized-pair.json", normalized)
    compare_producer_terminal(words, inputs, catalog, normalized, args)
    target_parent_count = len(history["accepted_target_derivation_parents"])
    residual_zero = history["residual"]["zero"]
    # All semantic joins and input JSON comparisons are complete; Fox evaluation needs
    # only the authenticated node offsets/hashes/liveness and the literal dictionary.
    catalog.ancestors = []
    catalog.symbols = {}
    words.documents.clear()
    del source, physical, ancestors, recipes, history, manifest
    boundary("completed_literal_metadata_released_before_eleven_slot_Fox")
    maps = task712_B_tables(inputs.roots["task712"], floor)
    evaluated = same_word_eleven(floor, catalog, output, normalized["normalized_pair"], words.digest("word-manifest.json"))
    grade = compare_current_grade(evaluated, maps, rho2, inputs.selected["target"], output)
    boundary("complete_same_word_typed_and_current_grade_comparison")
    inputs.finish_unchanged()
    words.finish_unchanged()
    source_receipt = output.json("checker-source.json", sealed("source", {
        "checker": inputs.acceptance["consumer_sources"]["checker"],
        "retained_checkers": [{"file": name, "bytes": size, "sha256": digest} for name, (size, digest) in RETAINED_PINS.items()],
        "raw_inputs": [{"file": name, "bytes": size, "sha256": digest} for name, (size, digest) in DATA_PINS.items()],
        "runtime": inputs.acceptance["runtime"], "producer_arithmetic_imported": False,
        "retained_TCB": ["LocalPc/LocalQ/local_quotients/cfox/LocalWords", "build_checker_light/IndependentAllSeven",
            "IndependentContext/Context/transport/prefix/aggregate", "Task712 four forward B table format"],
        "old_success_suites_replayed": 0, "old_numeric_prefixes_replayed": 0,
        "candidate": True, "cross_checked": False, "verified": False}))
    intake_receipt = output.json("input-comparison.json", sealed("inputs", {
        "acceptance_sha256": inputs.acceptance_sha, "accepted_HEAD_sha256": inputs.selected["hashes"]["head"],
        "parent_roster_sha256": words.digest("parent-roster.json"), "word_files": words.roster,
        "parents": [{"role": role, "artifact": inputs.parents[role]["record"]["artifact"],
            "manifest": inputs.parents[role]["record"]["manifest"], "files": len(inputs.parents[role]["files"]),
            "directories": len(inputs.parents[role]["record"]["directories"])} for role in PARENT_ROLES],
        "all_parent_files_and_directories_unchanged": True, "all_word_files_unchanged": True,
        "acceptance_and_source_data_unchanged": True, "eof": True,
        "candidate": True, "cross_checked": False, "verified": False}))
    head = inputs.selected["values"]["head"]
    status = "PASS" if grade["status"] == "PASS" else "NOT_APPLICABLE"
    return {"status": status, "terminal": "SAME_WORD_CURRENT_GRADE_COMPARED" if status == "PASS" else "NORMALIZED_PAIR_NOT_APPLICABLE",
        "checker_sha256": inputs.acceptance["consumer_sources"]["checker"]["sha256"], "checker_source": source_receipt,
        "inputs": intake_receipt, "recipe_bindings": recipe_receipt, "normalized_receipt": normalized_receipt,
        "word_manifest_sha256": words.digest("word-manifest.json"), "producer_result_sha256": words.digest("result.json"),
        "accepted_HEAD_sha256": inputs.selected["hashes"]["head"], "same_root_id": catalog.root_id, "same_root_sha256": catalog.root_hash,
        **{key: head[key] for key in ("completed_steps", "rank", "generation", "kind", "state_head", "target_remainder_sha256")},
        "all_thirteen_word_files_compared": True, "all_ordered_node_bytes_and_EOF_compared": True,
        "all_Ref_ordered_recipes_compared": True, "same_root_normalized_pair_compared": True,
        "target_history_named_parent_count": target_parent_count,
        "nodes": len(catalog.hashes), "typed_slots": 11, "typed_E3_bytes": 40, "typed_E4_bytes": 154,
        "all_eleven_endpoints_one": evaluated["slots"]["all_endpoint_one"],
        "all_three_printed_direct_prefix_equalities": all(record["direct_equals_prefix"] for record in evaluated["slots"]["printed_blocks"]),
        "source_lower_zero_required": False, "full_filtered_coordinates_compared": grade["full_filtered_coordinates_compared"],
        "current_grade": grade, "original_rho2_directly_read": True,
        "residual_zero": residual_zero, "normalized_pair": normalized["normalized_pair"],
        "positive_readout": "LOCAL_D_CONDITIONS_ONLY" if status == "PASS" and residual_zero and normalized["normalized_pair"] == [0, 0] else "NOT_APPLICABLE",
        "side_localization_conditions_complete": False, "full_P_zero_claimed": False, "grade2_member": "NOT_DECIDED",
        "grade2_nonmember": "NOT_DECIDED", "full_A0": False, "all_inputs_unchanged": True,
        "old_success_suites_replayed": 0, "old_numeric_prefixes_replayed": 0,
        "resource_limits": {"max_seconds": args.max_seconds, "max_memory_mib": args.max_memory_mib}, "eof": True}


def main() -> int:
    global DEADLINE
    args, output = None, None
    try:
        args = parse_args()
        configure_resources(args)
        if args.selftest:
            result = selftest()
            if args.output is not None:
                output = OutputFiles(args.output)
                output.json("selftest.json", result)
            code = 0
        else:
            validate_actual_paths(args)
            output = OutputFiles(args.output)
            body = check_actual(args, output)
            result = complete_output_report(output, body, complete=True)
            code = 0
    except (ResourceStop, MemoryError) as error:
        clear_resource_alarm()
        DEADLINE = None
        body = {"status": "UNKNOWN_RESOURCE", "terminal": "UNKNOWN_RESOURCE", "phase": LAST_PHASE,
            "error": type(error).__name__ + ":" + str(error), "all_required_comparisons_complete": False,
            "partial_output_is_not_a_success_candidate": True, "all_inputs_unchanged": False,
            "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False, "eof": False}
        result = complete_output_report(output, body, complete=False) if output is not None else sealed("checker-result", {
            **body, "complete_receipt": False, "manifest": None, "candidate": True, "cross_checked": False, "verified": False})
        code = 3
    except Exception as error:
        clear_resource_alarm()
        DEADLINE = None
        body = {"status": "FAIL", "terminal": "FAIL", "phase": LAST_PHASE,
            "error": type(error).__name__ + ":" + str(error), "all_required_comparisons_complete": False,
            "partial_output_is_not_a_success_candidate": True, "all_inputs_unchanged": False,
            "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False, "eof": False}
        result = complete_output_report(output, body, complete=False) if output is not None else sealed("checker-result", {
            **body, "complete_receipt": False, "manifest": None, "candidate": True, "cross_checked": False, "verified": False})
        code = 1
    finally:
        clear_resource_alarm()
    sys.stdout.buffer.write(canonical(result))
    sys.stdout.buffer.flush()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
