#!/usr/bin/env python3
"""Task966: one selected legal cycle, independently materialized.

The actual source uses ordinary F3[C3^3] coefficients and a complete cyclic
difference basis. Accepted oracle arrays are authenticated inputs, not an
invitation to run the previous complete oracle or historical scans again.
"""
from __future__ import annotations

import argparse
import copy
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import re
import signal
import sys
import tempfile
import time
from typing import Any, Callable, Iterator

import numpy as np

ORACLE_CHECKER_SHA = "2db166400dd819805f36b613993d4622e8365f04339ca7aef0371a28de71c967"
ORACLE_PRODUCER_SHA = "4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb"
_oracle_file = Path(__file__).resolve().with_name("check_d972_r07_section_cochain_oracle_v1.py")
if _oracle_file.is_symlink() or hashlib.sha256(_oracle_file.read_bytes()).hexdigest() != ORACLE_CHECKER_SHA:
    raise ValueError("selected_cycle_checker:oracle_checker_source_pin")
import check_d972_r07_section_cochain_oracle_v1 as ORACLE

REFINE, FIXED, LEGACY, BASE, ARITH = ORACLE.REFINE, ORACLE.FIXED, ORACLE.LEGACY, ORACLE.BASE, ORACLE.ARITH
canonical, sha, same, path, fixed = ORACLE.canonical, ORACLE.sha, ORACLE.same, ORACLE.path, ORACLE.fixed
pack, unpack, dot = ORACLE.pack, ORACLE.unpack, ORACLE.dot
SCHEMA = "d972.r07.selected-cycle-materializer.v1"
CHARACTERS, KERNEL = ORACLE.CHARACTERS, ORACLE.KERNEL
VERTICES, EDGES, SOURCE_LOWER, SOURCE_TOP, PHYSICAL, ROW_BYTES = 54432, 108864, 96776, 36288, 48384, 12096
OLD_OFFSETS, NEW_OFFSETS = ORACLE.OLD_OFFSETS, ORACLE.NEW_OFFSETS
ORACLE_ARTIFACT = {"run": 33977701313, "attempt": 1, "head": "bbce98d8f95a845f36fe89c0f507b9360792666f",
    "id": 9972829869, "name": "d972-r07-section-cochain-checker-completion-v1-candidate-33977701313-1",
    "bytes": 2299772, "sha256": "sha256:1a5c8800af563493b95dd4166d20c2fe1b74449f5f7f15aa99278d9b1c1b878d"}
ORACLE_FILES = {
    "source-receipt.json": (2673, "cd9a45a389cafd0cfb3813181c1365b0a66cdd682cc737a1a68f27b438d92934"),
    "checker-result.json": (15387, "92739f2db1007ec9ee040716c9dcb26859c10e5a5917a377514bb8e4eb4cd41a"),
    "completion-run-receipt.json": (2089, "3c2eb678db147c7538adf7520f19d91610b255488464704d32a224f9cda4102b"),
    "repair-source-receipt.json": (3204, "2b2efda3b1922e30246621a8b8cf87a277587767ca77662a03b7a35ef821bd37"),
    "preserved-input.json": (10504, "332f6b62aca1042868e65117d4cc9de952ef8d4817d5169ae8a1ee1a9298e625"),
    "output/manifest.json": (1430, "7df077372a51d12cbf95be5f26c94a5e29ef0f6b118f1ed7efb452ba01942639"),
    "output/start.json": (48377, "7ff970e54dec57512593f5445fed387075d6602bff31f41b7db9f34bab045a2a"),
    "output/owner.json": (8419, "6c71fbc405105bd0722924a308594ba41aea6745725ae85d046ff7409998b322"),
    "output/source.json": (1246, "af1e178d19e4ee427439d102de74a559ed6202ca0a2839212a60748ccfe482ac"),
    "output/result.json": (13727, "c7f65255443a8901fa1b6fbab69e81bbc811014e1eb527e7f671e2f6343ba312")}
ORACLE_REPAIRED_CHECKER_SHA = "a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d"
ORACLE_SNAPSHOT = {"rank": 1385, "generation": 8090,
    "state_head": "8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61",
    "lambda_sha256": "1e720af4a30bac955ab4565366f0242b5c2d43125eb280e241df20976331cdf1",
    "target_remainder_sha256": "111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad"}
PRODUCER_SHA = "4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3"
NORMALIZER_DATA = {"file": "scratchpad/a0_v2_words.json", "bytes": 106133,
    "sha256": "fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612"}
NORMALIZER_ROSTER_SHA = "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a"
NORMALIZER_ATOMS = {
    "r_x": (1058, "82fa1ff07d5269e5228fb411b97321b61869791c49133aaa65161f44d16b6f2c"),
    "r_y": (466, "88657577db0338fd5c58f7edeec205c27ce5ff5ddba128b8af403167cb232ac0"),
    "c_x": (9522, "2935d479d5896360e71b66aa95bcb964cdb04d9716f27c06f492034b5ac98abb"),
    "c_y": (4194, "c1f3ebec1ef6c448b854b216f8473e674a67a3b5d3a3059888af016293a1a6dd")}
STARTED = time.monotonic()
DEADLINE: float | None = None
LAST_PHASE = "initialization"
COMPLETED_STAGES: list[str] = []


class ResourceStop(Exception):
    pass


def require(condition: Any, label: str) -> None:
    if not condition:
        raise ValueError("selected_cycle_checker:" + label)


def boundary(phase: str, **fields: Any) -> None:
    global LAST_PHASE
    LAST_PHASE = phase
    if DEADLINE is not None and time.monotonic() >= DEADLINE:
        raise ResourceStop(phase)
    print(json.dumps({"phase": phase, **fields}, sort_keys=True), file=sys.stderr, flush=True)


def document(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    return ORACLE.seal({"schema": SCHEMA + "." + kind, **body})


def signed(value: int) -> int:
    require(type(value) is int and value in (0, 1, 2), "coefficient_trit")
    return -1 if value == 2 else value


def inverse_word(word: Any) -> list[int]:
    return [-int(letter) for letter in reversed(word)]


def reduced_word(letters: Any) -> list[int]:
    stack: list[int] = []
    for item in letters:
        letter = int(item)
        require(letter in (1, -1, 2, -2), "literal_signed_letter")
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return stack


def word_power(word: list[int], exponent: int) -> list[int]:
    require(type(exponent) is int, "integer_word_power")
    return (word if exponent >= 0 else inverse_word(word)) * abs(exponent)


def compact_word_bytes(word: Any) -> bytes:
    return json.dumps(word, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def normalizer_words() -> dict[str, Any]:
    repository = Path(__file__).resolve().parents[1]
    raw = fixed(repository, NORMALIZER_DATA["file"], (NORMALIZER_DATA["bytes"], NORMALIZER_DATA["sha256"]))
    data = json.loads(raw)
    roster = data["raw_q0_relators"]
    require(isinstance(roster, list) and len(roster) == 19 and sha(compact_word_bytes(roster)) == NORMALIZER_ROSTER_SHA,
            "normalizer_nineteen_word_roster")
    words = [reduced_word(row) for row in roster]
    rx = reduced_word(words[0] + word_power(words[5], -2) + word_power(words[6], 4) + words[8])
    ry = reduced_word(inverse_word(words[7]) + inverse_word(words[3]))
    atoms = {"r_x": rx, "r_y": ry, "c_x": reduced_word(word_power(rx, 9)), "c_y": reduced_word(word_power(ry, 9))}
    for name, word in atoms.items():
        length, digest = NORMALIZER_ATOMS[name]
        require(len(word) == length and sha(compact_word_bytes(word)) == digest, "actual_normalizer_atom:" + name)
    return {"atoms": atoms, "data": NORMALIZER_DATA, "roster_sha256": NORMALIZER_ROSTER_SHA}


def perm_product(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(right[point] for point in left)


def perm_inverse(value: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0] * len(value)
    for point, image in enumerate(value):
        answer[image] = point
    return tuple(answer)


def perm_power(value: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    answer = tuple(range(len(value)))
    if exponent < 0:
        value, exponent = perm_inverse(value), -exponent
    while exponent:
        if exponent & 1:
            answer = perm_product(answer, value)
        value, exponent = perm_product(value, value), exponent // 2
    return answer


class SelectedGeometry:
    """Actual multiplication plus authenticated oracle arrays, without A--D replay."""
    def __init__(self, context: Any, arrays: dict[str, np.ndarray]):
        self.context = context
        self.elements, self.positions = context.psels, context.psidx
        self.kernel = np.asarray(KERNEL, dtype=np.int64)
        self.signs = np.array([[1 if not e[1] else -1, 1 if not e[0] else -1,
                              1 if e[0] == e[1] else -1] for e in CHARACTERS], dtype=np.int64)
        self.psl_product = np.empty((504, 504), dtype=np.int32)
        for i, left in enumerate(self.elements):
            for j, right in enumerate(self.elements):
                self.psl_product[i, j] = self.positions[perm_product(left, right)]
            if i % 126 == 125:
                boundary("selected_psl_index", rows=i + 1)
        self.successor = arrays["next-pos.u32"].astype(np.int32)
        self.inverse_successor = arrays["prev-pos.u32"].astype(np.int32)
        self.tag_maps = arrays["phi.u32"].astype(np.int32)
        self.tree_parent = arrays["parent.u32"].astype(np.int64)
        self.tree_edge = arrays["parent-edge.u32"].astype(np.int64)
        self.tree_order = arrays["bfs-order.u32"].astype(np.int32)
        self.carry = arrays["carry.u8"]
        self.chords = arrays["chord-edges.u32"].astype(np.int32)
        self.generators = [self.affine_id(image) for image in context.images]
        self.depth = np.full(VERTICES, -1, dtype=np.int64)
        self.depth[0] = 0
        require(self.tree_order[0] == 0 and set(self.tree_order.tolist()) == set(range(VERTICES)), "accepted_tree_vertex_roster")
        require(self.tree_parent[0] == self.tree_edge[0] == 4294967295, "accepted_tree_root_sentinel")
        for raw_child in self.tree_order[1:]:
            child = int(raw_child)
            parent, edge = int(self.tree_parent[child]), int(self.tree_edge[child])
            require(0 <= parent < VERTICES and self.depth[parent] >= 0 and edge // 2 == parent and
                    int(self.successor[parent, edge % 2]) == child, "accepted_tree_parent_edge_join")
            self.depth[child] = self.depth[parent] + 1
        require(int(self.depth.max()) <= VERTICES - 1, "finite_tree_depth_bound")
        q0_file = Path(__file__).resolve().parents[1] / "scratchpad/fuda1_a0_rmax_data.g"
        raw = q0_file.read_bytes()
        pin = FIXED.DATA_PINS["scratchpad/fuda1_a0_rmax_data.g"]
        require(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"], "q0_marking_input_pin")
        match = re.search(r"FUDA1_Q0PERMS\s*:=\s*\[\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\]\s*;;", raw.decode("utf-8"), re.S)
        require(match is not None, "actual_q0_marking_text")
        self.q0_generators = [tuple(int(point) - 1 for point in json.loads(match.group(slot + 1))) for slot in range(2)]
        for slot, image in enumerate(self.q0_generators):
            require(len(image) == 36 and sorted(image) == list(range(36)), "actual_q0_36_point_permutation")
            generator = self.generators[slot]
            e, k = generator // (27 * 504), self.kernel[(generator // 504) % 27]
            reconstructed = list(self.elements[generator % 504])
            for axis in range(3):
                begin = 9 + 9 * axis
                translation = image[begin] - begin
                require(translation % 3 == int(k[axis]), "q0_q2_kernel_reduction")
                reconstructed.extend(begin + (int(self.signs[e, axis]) * u + translation) % 9 for u in range(9))
            require(tuple(reconstructed) == image, "actual_q0_full36_reconstruction")

    def affine_id(self, image: Any) -> int:
        k = [int(value) % 3 for value in image[3]]
        return (((2 * int(image[1]) + int(image[2])) * 27 + 9 * k[0] + 3 * k[1] + k[2]) * 504 + self.positions[image[0]])

    def multiply(self, left: Any, right: Any) -> Any:
        l, r = np.asarray(left, dtype=np.int64), np.asarray(right, dtype=np.int64)
        le, re = l // (27 * 504), r // (27 * 504)
        kernel = (self.signs[re] * self.kernel[(l // 504) % 27] + self.kernel[(r // 504) % 27]) % 3
        result = ((np.bitwise_xor(le, re) * 27 + 9 * kernel[..., 0] + 3 * kernel[..., 1] + kernel[..., 2]) * 504 +
                  self.psl_product[l % 504, r % 504])
        return int(result) if result.ndim == 0 else result.astype(np.int32)

    def inverse(self, value: int) -> int:
        p, e, k = value % 504, value // (27 * 504), self.kernel[(value // 504) % 27]
        inverse_p = self.positions[perm_inverse(self.elements[p])]
        inverse_k = -self.signs[e] * k % 3
        answer = int((e * 27 + 9 * inverse_k[0] + 3 * inverse_k[1] + inverse_k[2]) * 504 + inverse_p)
        require(self.multiply(value, answer) == self.multiply(answer, value) == 0, "q2_inverse")
        return answer

    def power(self, value: int, exponent: int) -> int:
        answer = 0
        if exponent < 0:
            value, exponent = self.inverse(value), -exponent
        while exponent:
            if exponent & 1:
                answer = self.multiply(answer, value)
            value, exponent = self.multiply(value, value), exponent // 2
        return answer

    def tree_word(self, vertex: int) -> list[int]:
        require(type(vertex) is int and 0 <= vertex < VERTICES, "tree_reference_vertex")
        answer = []
        while vertex:
            edge = int(self.tree_edge[vertex])
            answer.append(edge % 2 + 1)
            vertex = int(self.tree_parent[vertex])
            require(len(answer) <= VERTICES - 1, "tree_reference_cycle")
        return list(reversed(answer))


def letter_statistics(letters: Any, geometry: SelectedGeometry) -> dict[str, Any]:
    a, b, omega, length, q2 = 0, 0, 0, 0, 0
    q0 = tuple(range(36))
    for signed_letter in letters:
        letter = int(signed_letter)
        require(letter in (1, -1, 2, -2), "statistic_letter")
        slot, sign = abs(letter) - 1, 1 if letter > 0 else -1
        if slot == 0:
            omega, a = (omega + sign * b) % 3, a + sign
        else:
            b += sign
        generator = geometry.q0_generators[slot]
        q0 = perm_product(q0, generator if sign > 0 else perm_inverse(generator))
        q2 = int(geometry.successor[q2, slot] if sign > 0 else geometry.inverse_successor[q2, slot])
        length += 1
    return {"exponent": [a, b], "omega": omega, "length": length, "q0": list(q0), "q2": q2}


def combine_statistics(left: dict[str, Any], right: dict[str, Any], geometry: SelectedGeometry) -> dict[str, Any]:
    a, b = left["exponent"]
    c, d = right["exponent"]
    return {"exponent": [a + c, b + d], "omega": (left["omega"] + right["omega"] + b * c) % 3,
        "length": left["length"] + right["length"],
        "q0": list(perm_product(tuple(left["q0"]), tuple(right["q0"]))),
        "q2": geometry.multiply(left["q2"], right["q2"])}


def power_statistics(value: dict[str, Any], exponent: int, geometry: SelectedGeometry) -> dict[str, Any]:
    require(type(exponent) is int, "slp_integer_power_type")
    a, b = value["exponent"]
    return {"exponent": [exponent * a, exponent * b],
        "omega": (exponent * value["omega"] + exponent * (exponent - 1) // 2 * b * a) % 3,
        "length": abs(exponent) * value["length"],
        "q0": list(perm_power(tuple(value["q0"]), exponent)), "q2": geometry.power(value["q2"], exponent)}


class RawSLP:
    """Typed ordered word and bottom-up scalar endpoints; full chains are not cached per node."""
    def __init__(self, geometry: SelectedGeometry, atoms: dict[str, Any]):
        self.geometry, self.atoms = geometry, atoms
        self.nodes: list[dict[str, Any]] = []
        self.by_id: dict[str, dict[str, Any]] = {}
        self.values: dict[str, dict[str, Any]] = {}
        self.identity = {"exponent": [0, 0], "omega": 0, "length": 0, "q0": list(range(36)), "q2": 0}

    def add(self, name: str, operation: str, **fields: Any) -> str:
        require(name not in self.by_id, "unique_slp_node_id")
        node = {"id": name, "op": operation, **fields}
        if operation == "Identity":
            value = dict(self.identity)
        elif operation == "Letter":
            value = letter_statistics([fields["letter"]], self.geometry)
        elif operation == "Ref":
            value = letter_statistics(self.reference_word(node), self.geometry)
        elif operation == "OrderedProduct":
            value = dict(self.identity)
            for factor in fields["factors"]:
                require(factor in self.values, "slp_prior_product_reference")
                value = combine_statistics(value, self.values[factor], self.geometry)
        elif operation in ("Inverse", "IntegerPower"):
            require(fields["node"] in self.values, "slp_prior_unary_reference")
            value = power_statistics(self.values[fields["node"]], -1 if operation == "Inverse" else fields["exponent"], self.geometry)
        else:
            raise ValueError("selected_cycle_checker:unknown_slp_grammar")
        self.nodes.append(node); self.by_id[name] = node; self.values[name] = value
        return name

    def reference_word(self, node: dict[str, Any]) -> list[int]:
        if node["namespace"] == "oracle-tree":
            return self.geometry.tree_word(node["key"])
        require(node["namespace"] == "normalizer-v459" and node["key"] in ("r_x", "r_y"), "slp_reference_namespace")
        return self.atoms[node["key"]]

    def letters(self, name: str, inverse: bool = False) -> Iterator[int]:
        node = self.by_id[name]
        op = node["op"]
        if op == "Identity":
            return
        if op == "Letter":
            yield -node["letter"] if inverse else node["letter"]
        elif op == "Ref":
            word = self.reference_word(node)
            yield from inverse_word(word) if inverse else word
        elif op == "OrderedProduct":
            factors = list(reversed(node["factors"])) if inverse else node["factors"]
            for factor in factors:
                yield from self.letters(factor, inverse)
        elif op == "Inverse":
            yield from self.letters(node["node"], not inverse)
        elif op == "IntegerPower":
            exponent = node["exponent"]
            for _ in range(abs(exponent)):
                yield from self.letters(node["node"], inverse != (exponent < 0))

    def chain(self, name: str) -> tuple[np.ndarray, int]:
        """One accumulator per active product; inverse/power use actual LEFT Fox action."""
        node, geometry = self.by_id[name], self.geometry

        def product_pair(left: tuple[np.ndarray, int], right: tuple[np.ndarray, int]) -> tuple[np.ndarray, int]:
            chain, endpoint = left
            other, other_endpoint = right
            moved = np.zeros((VERTICES, 2), dtype=np.uint8)
            moved[geometry.multiply(endpoint, np.arange(VERTICES, dtype=np.int32))] = other.reshape(VERTICES, 2)
            return ((chain.astype(np.uint16) + moved.reshape(-1)) % 3).astype(np.uint8), geometry.multiply(endpoint, other_endpoint)

        def invert(pair: tuple[np.ndarray, int]) -> tuple[np.ndarray, int]:
            chain, endpoint = pair
            endpoint = geometry.inverse(endpoint)
            moved = np.zeros((VERTICES, 2), dtype=np.uint8)
            moved[geometry.multiply(endpoint, np.arange(VERTICES, dtype=np.int32))] = (-chain.reshape(VERTICES, 2).astype(np.int16)) % 3
            return moved.reshape(-1), endpoint

        if node["op"] in ("Identity", "Letter", "Ref"):
            chain, endpoint = flat_fox_chain(self.letters(name), geometry)
        elif node["op"] == "OrderedProduct":
            chain, endpoint = np.zeros(EDGES, dtype=np.uint8), 0
            for factor in node["factors"]:
                chain, endpoint = product_pair((chain, endpoint), self.chain(factor))
        else:
            exponent = -1 if node["op"] == "Inverse" else node["exponent"]
            power = self.chain(node["node"])
            if exponent < 0:
                power, exponent = invert(power), -exponent
            chain, endpoint = np.zeros(EDGES, dtype=np.uint8), 0
            while exponent:
                if exponent & 1:
                    chain, endpoint = product_pair((chain, endpoint), power)
                exponent //= 2
                if exponent:
                    power = product_pair(power, power)
        require(endpoint == self.values[name]["q2"], "slp_chain_endpoint:" + name)
        return chain, endpoint


def flat_fox_chain(letters: Any, geometry: SelectedGeometry) -> tuple[np.ndarray, int]:
    chain = np.zeros((VERTICES, 2), dtype=np.int64)
    vertex = 0
    for count, signed_letter in enumerate(letters, 1):
        letter = int(signed_letter)
        require(letter in (1, -1, 2, -2), "raw_fox_signed_letter")
        slot = abs(letter) - 1
        if letter > 0:
            chain[vertex, slot] += 1
            vertex = int(geometry.successor[vertex, slot])
        else:
            vertex = int(geometry.inverse_successor[vertex, slot])
            chain[vertex, slot] -= 1
        if count % 65536 == 0:
            boundary("selected_raw_fox_letters", letters=count)
    return (chain.reshape(-1) % 3).astype(np.uint8), vertex


def selected_raw_slp(geometry: SelectedGeometry, witness: dict[str, Any], normalizers: dict[str, Any]) -> RawSLP:
    require(witness["kind"] in ("chord", "auxiliary") and witness["scalar"] in (1, 2), "nonzero_oracle_witness_type")
    slp = RawSLP(geometry, normalizers["atoms"])
    slp.add("identity", "Identity"); slp.add("x", "Letter", letter=1); slp.add("y", "Letter", letter=2)
    factors = []
    for i, cycle in enumerate(witness["cycles"]):
        edge, coefficient = cycle["edge"], cycle["coefficient"]
        require(type(edge) is int and edge in geometry.chords, "selected_chord_membership")
        tail, slot = divmod(edge, 2)
        slp.add("tail-" + str(i), "Ref", namespace="oracle-tree", key=tail)
        slp.add("head-" + str(i), "Ref", namespace="oracle-tree", key=int(geometry.successor[tail, slot]))
        slp.add("head-inverse-" + str(i), "Inverse", node="head-" + str(i))
        slp.add("cycle-" + str(i), "OrderedProduct", factors=["tail-" + str(i), "x" if slot == 0 else "y", "head-inverse-" + str(i)])
        factors.append(slp.add("cycle-power-" + str(i), "IntegerPower", node="cycle-" + str(i), exponent=signed(coefficient)))
    slp.add("w", "OrderedProduct", factors=factors)
    slp.add("r-x", "Ref", namespace="normalizer-v459", key="r_x")
    slp.add("r-y", "Ref", namespace="normalizer-v459", key="r_y")
    slp.add("r-x-cube", "IntegerPower", node="r-x", exponent=3)
    slp.add("r-y-cube", "IntegerPower", node="r-y", exponent=3)
    slp.add("r-x-inverse", "Inverse", node="r-x")
    slp.add("r-y-inverse", "Inverse", node="r-y")
    slp.add("commutator", "OrderedProduct", factors=["r-x-inverse", "r-y-inverse", "r-x", "r-y"])
    for name, exponent in (("r-x", [2, 0]), ("r-y", [0, 2])):
        require(slp.values[name]["q0"] == list(range(36)) and slp.values[name]["q2"] == 0 and
                slp.values[name]["exponent"] == exponent, "literal_normalizer_N0:" + name)
    require(slp.values["commutator"]["omega"] == 2, "actual_commutator_omega_sign")
    if witness["kind"] == "chord":
        a, b = slp.values["w"]["exponent"]
        require(len(witness["cycles"]) == 6 and a % 6 == b % 6 == 0 and
                slp.values["w"]["q0"] == list(range(36)) and slp.values["w"]["q2"] == 0, "legal_six_cycle_word")
        slp.add("repair-x", "IntegerPower", node="r-x-cube", exponent=-a // 6)
        slp.add("repair-y", "IntegerPower", node="r-y-cube", exponent=-b // 6)
        slp.add("repair-central", "IntegerPower", node="commutator", exponent=signed(slp.values["w"]["omega"]))
        slp.add("raw-root", "OrderedProduct", factors=["w", "repair-x", "repair-y", "repair-central"])
    else:
        require(not witness["cycles"] and witness["coordinate"] in (0, 1), "auxiliary_cycle_roster")
        slp.add("raw-root", "IntegerPower", node="r-x" if witness["coordinate"] == 0 else "r-y", exponent=9)
    expected = [18 * int(value) for value in witness["eta"]]
    root = slp.values["raw-root"]
    require(root["exponent"] == expected and root["omega"] == 0 and root["q0"] == list(range(36)) and root["q2"] == 0,
            "actual_legal_raw_root_endpoint_exponents")
    return slp


def ordinary_source(geometry: SelectedGeometry, tagged_chains: list[np.ndarray], eta: list[int]) -> tuple[np.ndarray, ...]:
    """Actual forward scatter through ordinary group coefficients, then difference-basis extraction."""
    _, moments = ORACLE.cyclic_difference_moments()
    moments = moments.astype(np.int64)
    source = REFINE.zero_source()
    d0, d1, d2, aux = source
    all_vertices = np.arange(VERTICES, dtype=np.int32)
    for tag, chain in enumerate(tagged_chains):
        chain = chain.reshape(VERTICES, 2)
        ordinary = np.zeros((2, VERTICES), dtype=np.int64)
        # This is the linear PB3 stencil; prefixes need not be closed words.
        np.add.at(ordinary[0], geometry.successor[:, 0], -chain[:, 0].astype(np.int64))
        np.add.at(ordinary[1], geometry.inverse_successor[:, 1], -chain[:, 0].astype(np.int64))
        np.add.at(ordinary[1], all_vertices, chain[:, 1].astype(np.int64))
        ordinary %= 3
        aux[tag] = int(chain[:, 0].sum(dtype=np.uint64) % 3)
        for component in range(2):
            coefficients = ordinary[component].reshape(4, 27, 504)
            for character, label in enumerate(CHARACTERS):
                monomial = np.zeros((10, 504), dtype=np.int64)
                transported = geometry.context.transport[tag][label]
                for parity, e in enumerate(CHARACTERS):
                    weight = 1 if sum(left * right for left, right in zip(transported, e)) % 2 == 0 else -1
                    monomial += weight * (moments.T @ coefficients[parity])
                monomial %= 3
                d0.reshape(4, 6, 2, 504)[character, tag, component] = monomial[0]
                d1.reshape(4, 6, 2, 3, 504)[character, tag, component] = monomial[1:4]
                d2.reshape(4, 6, 2, 6, 504)[character, tag, component] = monomial[4:]
        boundary("ordinary27_actual_source", tag=tag)
    require(len(eta) == 2 and all(type(value) is int and value in (0, 1, 2) for value in eta), "same_legal_root_eta")
    aux[6:] = eta
    return source


def tag_chain_from_raw(geometry: SelectedGeometry, chain: np.ndarray) -> list[np.ndarray]:
    require(chain.shape == (EDGES,), "raw_chain_full_width")
    answer = []
    shaped = chain.reshape(VERTICES, 2)
    for tag, pair in enumerate(ARITH.SEED_OO):
        current = np.zeros((VERTICES, 2), dtype=np.int64)
        for slot in range(2):
            vertices = np.flatnonzero(shaped[:, slot]).astype(np.int32)
            coefficients = shaped[vertices, slot].astype(np.int64)
            terms, endpoint = ORACLE.linear_fox_terms(geometry, pair[slot])
            for component, prefix, value in terms:
                destinations = geometry.multiply(geometry.tag_maps[tag, vertices], prefix)
                np.add.at(current[:, component], destinations, int(value) * coefficients)
        answer.append((current.reshape(-1) % 3).astype(np.uint8))
        boundary("selected_same_raw_chain_tag", tag=tag)
    return answer


def direct_slp_tag_chains(slp: RawSLP) -> tuple[list[np.ndarray], dict[str, Any]]:
    """Separate whole-word substituted Fox route, with actual signed-stream EOF/hash."""
    answer, stream_hash, emitted = [], hashlib.sha256(), 0
    for letter in slp.letters("raw-root"):
        stream_hash.update(bytes([letter & 255])); emitted += 1
        if emitted % 65536 == 0:
            boundary("raw_signed_word_stream", letters=emitted)
    require(emitted == slp.values["raw-root"]["length"], "raw_word_stream_exact_eof")
    for tag, pair in enumerate(ARITH.SEED_OO):
        def substituted() -> Iterator[int]:
            for letter in slp.letters("raw-root"):
                word = pair[abs(letter) - 1]
                yield from inverse_word(word) if letter < 0 else word
        chain, endpoint = flat_fox_chain(substituted(), slp.geometry)
        require(endpoint == 0, "same_raw_slp_tagged_endpoint")
        answer.append(chain)
        boundary("same_raw_slp_direct_tag", tag=tag)
    return answer, {"encoding": "signed-byte:1=01,-1=ff,2=02,-2=fe", "letters": emitted, "bytes": emitted,
                    "sha256": stream_hash.hexdigest(), "full_eof": True}


def full_lower(source: tuple[np.ndarray, ...]) -> np.ndarray:
    return np.concatenate((source[0].reshape(-1), source[1].reshape(-1), source[3]))


def residue_pair(value: Any) -> list[int]:
    require(isinstance(value, list) and len(value) == 2 and
            all(type(x) is int and 0 <= x < 54 for x in value), "residue54_pair_type")
    return value


def exponent_expression(origin: list[int], reductions: Any, prior: list[list[int]], scale: int = 1) -> list[int]:
    """Ordered signed-word homomorphism to (Z/54)^2; independent of source aux."""
    answer = list(origin)
    for local, coefficient in reductions:
        require(type(local) is int and 0 <= local < len(prior), "literal_owner_local_prior")
        for axis in range(2):
            answer[axis] += -signed(coefficient) * prior[local][axis]
    require(type(scale) is int and scale in (1, 2), "literal_internal_scale")
    return residue_pair([(signed(scale) * item) % 54 for item in answer])


def projected_exponents(pair: list[int], owner: int) -> list[int]:
    # Four conjugates with signed character coefficients; 4 must remain 4 here.
    multiplier = sum(1 if sum(x * y for x, y in zip(CHARACTERS[owner], parity)) % 2 == 0 else -1
                     for parity in CHARACTERS)
    return [(multiplier * value) % 54 for value in pair]


def node_metadata(node: dict[str, Any]) -> dict[str, Any]:
    return {"origin": node["origin"], "reductions_sha256": sha(canonical(node["reductions"])), "scale": node["scale"]}


def source_basis_metadata(state: dict[str, Any], words: dict[str, Any]) -> dict[str, Any]:
    """Keep one large saved body at a time; retain only small row and literal metadata."""
    seed_pairs = [[sum((1 if letter > 0 else -1) for letter in word if abs(letter) == axis) % 54
                   for axis in (1, 2)] for word in words["relators"]]
    require(len(seed_pairs) == 44, "literal_seed_roster")
    records, pairs, node_joins, descriptors = [], [], [], []
    checked = BASE.state_descriptor(state["task554"]["prepare"], -1)
    old_pairs = []
    for owner, old in enumerate(checked["body"]["old_blocks"]):
        local_pairs = []
        for local, node in enumerate(old["record"]["dag_nodes"]):
            origin = node["origin"]
            if origin["kind"] == "projected_seed":
                require(type(origin["seed"]) is int and 1 <= origin["seed"] <= 44, "one_based_projected_seed")
                initial = projected_exponents(seed_pairs[origin["seed"] - 1], owner)
            else:
                require(origin["kind"] == "actor" and origin["letter"] in (1, -1, 2, -2) and
                        type(origin["parent"]) is int and 0 <= origin["parent"] < local, "old_literal_actor")
                initial = local_pairs[origin["parent"]]
            local_pairs.append(exponent_expression(initial, node["reductions"], local_pairs, node["scale"]))
            lead = int(node["lead"])
            embedded = owner * 6048 + lead if lead < 6048 else 96768 + lead - 6048
            records.append({"kind": "old", "owner": owner, "local": local, "node": OLD_OFFSETS[owner] + local,
                            "original_lead": lead, "embedded_lead": embedded})
            node_joins.append(node_metadata(node))
        pairs.extend(local_pairs); old_pairs.append(local_pairs)
        descriptors.extend((checked["root"], old[key]) for key in ("lower_basis_blob", "lifted_grade_blob"))
    defects = []
    for number, origin in enumerate(checked["body"]["defect_origins"]):
        owner = origin["lower_character"]
        record = checked["body"]["old_blocks"][owner]["record"]
        require(origin["id"] == number, "whole_old_defect_id")
        if origin["kind"] == "seed":
            initial = projected_exponents(seed_pairs[origin["seed"] - 1], owner)
            reductions = record["seed_reductions"][origin["seed"] - 1]
        else:
            require(origin["kind"] == "transition" and origin["letter"] in BASE.ACTORS, "whole_old_defect_type")
            initial = old_pairs[owner][origin["pivot"]]
            reductions = record["actor_transitions"][origin["pivot"]][BASE.ACTORS.index(origin["letter"])]
        defects.append(exponent_expression(initial, reductions, old_pairs[owner]))
    del checked, old, record, node, reductions
    require(len(pairs) == 2014 and len(defects) == BASE.TASK554_ORIGINS, "old_literal_complete_eof")
    boundary("literal_old_body_released", rows=len(pairs))
    for owner in range(4):
        checked = BASE.state_descriptor(state["task554"]["blocks"][owner], owner)
        local_pairs = []
        for local, node in enumerate(checked["body"]["dag_nodes"]):
            origin = node["origin"]
            if origin["kind"] == "defect":
                require(type(origin["origin"]) is int and 0 <= origin["origin"] < len(defects), "new_whole_defect_reference")
                initial = projected_exponents(defects[origin["origin"]], owner)
            else:
                require(origin["kind"] == "actor" and origin["letter"] in BASE.ACTORS and
                        type(origin["parent"]) is int and 0 <= origin["parent"] < local, "new_literal_actor")
                initial = local_pairs[origin["parent"]]
            local_pairs.append(exponent_expression(initial, node["reductions"], local_pairs, node["scale"]))
            lead = int(node["lead"])
            require(checked["body"]["pivot_leads"][local] == lead, "new_original_lead_identity")
            records.append({"kind": "new", "owner": owner, "local": local, "node": NEW_OFFSETS[owner] + local,
                            "original_lead": lead, "embedded_lead": 24192 + owner * 18144 + lead})
            node_joins.append(node_metadata(node))
        pairs.extend(local_pairs)
        descriptors.append((checked["root"], checked["body"]["basis_blob"]))
        del checked, node
        boundary("literal_new_body_released", owner=owner, rows=len(pairs))
    require(len(records) == len(pairs) == len(node_joins) == 8059 and
            [r["node"] for r in records] == list(range(8059)) and
            len({r["embedded_lead"] for r in records}) == 8059, "complete_canonical_original_leads")
    return {"records": records, "pairs": pairs, "node_joins": node_joins, "descriptors": descriptors}


def authenticated_blob(root: Path, descriptor: dict[str, Any]) -> None:
    item = path(root, descriptor["file"])
    require(item.stat().st_size == descriptor["bytes"] == descriptor["rows"] * ((descriptor["width"] + 3) // 4), "basis_blob_size")
    digest = hashlib.sha256()
    with item.open("rb") as stream:
        while True:
            chunk = stream.read(1 << 20)
            if not chunk:
                break
            digest.update(chunk)
    require(digest.hexdigest() == descriptor["sha256"], "basis_blob_complete_hash")


def primal_rows(raw_source: tuple[np.ndarray, ...], records: list[dict[str, Any]],
                read_row: Callable[[dict[str, Any]], tuple[bytes, bytes | None]]) -> dict[str, Any]:
    """Ascending full source leads; raw row scale has already been normalized."""
    lower = full_lower(raw_source).copy()
    alpha = np.zeros(len(records), dtype=np.uint8)
    old = sorted((r for r in records if r["kind"] == "old"), key=lambda r: r["embedded_lead"])
    new = sorted((r for r in records if r["kind"] == "new"), key=lambda r: (r["owner"], r["original_lead"]))
    events = []
    for r in old + new:
        coefficient = int(lower[r["embedded_lead"]])
        if not coefficient:
            continue
        packed_row, packed_companion = read_row(r)
        owner, lead = r["owner"], r["original_lead"]
        if r["kind"] == "old":
            row = unpack(packed_row, 6056)
            require(row[lead] == 1 and not np.any(row[:lead]) and (owner == 0 or not np.any(row[6048:])), "primal_old_original_lead")
            LEGACY.subtract(lower[owner * 6048:(owner + 1) * 6048], row[:6048], coefficient)
            LEGACY.subtract(lower[96768:], row[6048:], coefficient)
            require(packed_companion is not None, "old_complete_four_d1_companion")
            LEGACY.subtract(lower[24192:96768], unpack(packed_companion, 72576), coefficient)
        else:
            row = unpack(packed_row, 18144)
            require(row[lead] == 1 and not np.any(row[:lead]) and packed_companion is None, "primal_new_original_lead")
            begin = 24192 + owner * 18144
            LEGACY.subtract(lower[begin:begin + 18144], row, coefficient)
        require(lower[r["embedded_lead"]] == 0, "primal_eliminated_original_lead")
        alpha[r["node"]] = coefficient
        events.append({"event": len(events), **r, "coefficient": coefficient, "literal_exponent": -signed(coefficient),
            "row_offset": r["local"] * len(packed_row), "row_sha256": sha(packed_row),
            "companion_offset": r["local"] * len(packed_companion) if packed_companion is not None else None,
            "companion_sha256": sha(packed_companion) if packed_companion is not None else None})
        if len(events) % 128 == 0:
            boundary("primal_source_reduction", events=len(events))
    require(lower.shape == (SOURCE_LOWER,) and not np.any(lower), "primal_all_96776_zero")
    return {"alpha": alpha, "events": events, "lower": lower}


def actual_primal(args: argparse.Namespace, source: tuple[np.ndarray, ...], basis: dict[str, Any]) -> dict[str, Any]:
    for root, descriptor in basis["descriptors"]:
        authenticated_blob(root, descriptor)
        boundary("source_basis_blob_authenticated", file=descriptor["file"])
    with ExitStack() as stack:
        streams = [stack.enter_context(path(root, descriptor["file"]).open("rb")) for root, descriptor in basis["descriptors"]]
        def row(r: dict[str, Any]) -> tuple[bytes, bytes | None]:
            if r["kind"] == "old":
                return (LEGACY.blob_row(streams[2 * r["owner"]], r["local"], 6056),
                        LEGACY.blob_row(streams[2 * r["owner"] + 1], r["local"], 72576))
            return LEGACY.blob_row(streams[8 + r["owner"]], r["local"], 18144), None
        answer = primal_rows(source, basis["records"], row)
    return answer


def authenticate_literal_instructions(args: argparse.Namespace, state: dict[str, Any], basis: dict[str, Any]) -> dict[str, Any]:
    index = state["accepted_refinement"]["index"]
    p1 = BASE.validate_p1({**state["launch"]["p1_parent"], "root": str(args.p1_root.resolve())})
    digest, offset, predecessor = hashlib.sha256(), 0, "0" * 64
    with path(args.p1_root, "instructions.jsonl").open("rb", buffering=1 << 20) as stream:
        for node, reference in enumerate(index["references"]):
            length = reference["instruction_length"]
            require(reference["node"] == node and reference["instruction_offset"] == offset and
                    type(length) is int and 0 < length < (1 << 24), "positioned_canonical_instruction")
            raw = stream.read(length)
            item = json.loads(raw)
            require(len(raw) == length and raw == canonical(item) and sha(raw) == reference["instruction_sha256"], "actual_canonical_instruction_bytes")
            digest.update(raw); offset += length
            require(item["node"] == node and item["predecessor"] == predecessor == reference["predecessor"] and
                    item["offset"] == node * 36288 and item["length"] == 36288 and
                    item["row_receipt"] == {"offset": node * 36288, "length": 36288, "sha256": reference["row_sha256"]} and
                    item["p1_sha256"] == reference["p1_sha256"] and item["literal_input_sha256"] == reference["literal_input_sha256"],
                    "canonical_instruction_typed_joins")
            same(node_metadata(item), basis["node_joins"][node], "actual_p1_literal_matches_saved_DAG")
            require(sha(canonical(item["origin"])) == reference["origin_sha256"] and
                    sha(canonical(item["reductions"])) == reference["reductions_sha256"] and item["scale"] == reference["scale"],
                    "canonical_instruction_origin_reductions_scale")
            predecessor = sha(bytes.fromhex(predecessor) + canonical({k: v for k, v in item.items() if k != "ancestry_sha256"}))
            require(item["ancestry_sha256"] == predecessor == reference["ancestry_sha256"], "canonical_instruction_rolling_hash")
            if (node + 1) % 1024 == 0:
                boundary("canonical_literal_exponent_join", rows=node + 1)
        require(stream.read(1) == b"" and offset == BASE.P1_INSTRUCTION_BYTES and
                digest.hexdigest() == BASE.P1_INSTRUCTION_SHA256 and predecessor == p1["manifest"]["ancestry_sha256"],
                "canonical_literal_all_8059_exact_eof")
    return index


def p1_corrected_source(args: argparse.Namespace, source: tuple[np.ndarray, ...], basis: dict[str, Any],
                        primal: dict[str, Any], index: dict[str, Any]) -> tuple[tuple[np.ndarray, ...], dict[str, Any]]:
    corrected = tuple(part.copy() for part in source)
    # This reconstruction starts from the raw tuple, independently of primal's lower remainder.
    roots, digest, total = [], hashlib.sha256(), 0
    with ExitStack() as stack:
        streams = [stack.enter_context(path(root, descriptor["file"]).open("rb")) for root, descriptor in basis["descriptors"]]
        cache = stack.enter_context(path(args.p1_root, "degree2.cache.bin").open("rb", buffering=1 << 20))
        for node, reference in enumerate(index["references"]):
            raw = cache.read(36288)
            require(len(raw) == 36288 and sha(raw) == reference["row_sha256"], "all_canonical_p1_cache_rows")
            digest.update(raw); total += len(raw)
            coefficient = int(primal["alpha"][node])
            if coefficient:
                # source_lift's positioned cache read ends at this same next-row position.
                lift, components = REFINE.source_lift(args, streams, cache, reference)
                for target, part in zip(corrected, lift):
                    LEGACY.subtract(target, part, coefficient)
                roots.append({**reference, "lift_components": components})
            if (node + 1) % 1024 == 0:
                boundary("p1_source_reconstruction", rows=node + 1, selected=len(roots))
        require(cache.read(1) == b"" and total == BASE.P1_CACHE_BYTES and digest.hexdigest() == BASE.P1_CACHE_SHA256,
                "p1_complete_cache_eof")
    require(np.array_equal(full_lower(corrected), primal["lower"]) and not np.any(full_lower(corrected)),
            "independent_primal_and_full_P1_source_lower_equality")
    return corrected, document("p1-roots", {"p1_manifest_sha256": BASE.P1_MANIFEST_SHA256,
        "instruction_sha256": BASE.P1_INSTRUCTION_SHA256, "cache_sha256": BASE.P1_CACHE_SHA256,
        "canonical_index_sha256": sha(canonical(index)), "roots": roots, "all_references_authenticated": True})


def raw_materialization(geometry: SelectedGeometry, normalizers: dict[str, Any], oracle: dict[str, Any]) -> dict[str, Any]:
    witness = oracle["witness"]
    require(witness["kind"] in ("chord", "auxiliary") and type(witness["scalar"]) is int and witness["scalar"] in (1, 2),
            "accepted_selected_nonzero_witness")
    slp = selected_raw_slp(geometry, witness, normalizers)
    chain, endpoint = slp.chain("raw-root")
    require(endpoint == 0, "raw_SLP_closed_Q2")
    wanted_chain = np.zeros(EDGES, dtype=np.int16)
    if witness["kind"] == "chord":
        require(len(witness["cycles"]) == 6 and witness["cycles"][0] == {"edge": witness["failed_chord"], "coefficient": 1} and
                [r["edge"] for r in witness["cycles"][1:]] == witness["basis_chords"] and
                [r["coefficient"] for r in witness["cycles"][1:]] == [(-int(x)) % 3 for x in witness["basis_coefficients"]],
                "six_ordered_failed_then_basis_cycles")
        for record in witness["cycles"]:
            edge, coefficient = record["edge"], record["coefficient"]
            require(type(edge) is int and edge in set(geometry.chords.tolist()), "selected_actual_chord_id")
            q, slot = divmod(edge, 2)
            word = geometry.tree_word(q) + [slot + 1] + inverse_word(geometry.tree_word(int(geometry.successor[q, slot])))
            cycle, cycle_endpoint = flat_fox_chain(word, geometry)
            require(cycle_endpoint == 0, "raw_fundamental_cycle_endpoint")
            wanted_chain += signed(coefficient) * cycle.astype(np.int16)
    for name in ("r_x", "r_y"):
        _, normalizer_endpoint = flat_fox_chain(normalizers["atoms"][name], geometry)
        require(normalizer_endpoint == 0, "normalizer_atom_Q2_endpoint")
    for name in ("r-x-cube", "r-y-cube", "commutator"):
        normalizer_chain, normalizer_endpoint = slp.chain(name)
        require(normalizer_endpoint == 0 and not np.any(normalizer_chain), "repair_factor_actual_Q2_Fox_zero")
    require(np.array_equal(chain, (wanted_chain % 3).astype(np.uint8)), "raw_repair_preserves_same_chain")
    tau = (chain.astype(np.uint64) @ geometry.carry.astype(np.uint64) % 3).astype(np.uint8)
    require(not np.any(tau) and witness["tau"] == [0] * 5, "selected_six_cycle_tau_zero")
    scalar = (dot(chain, oracle["arrays"]["cochain"]["f.u8"]) +
              dot(np.asarray(witness["eta"], dtype=np.uint8), oracle["arrays"]["cochain"]["b-aux.u8"])) % 3
    require(scalar == witness["scalar"], "same_raw_chain_witness_scalar")
    tagged = tag_chain_from_raw(geometry, chain)
    direct, word_stream = direct_slp_tag_chains(slp)
    require(all(np.array_equal(a, b) for a, b in zip(tagged, direct)), "all_six_actual_direct_SLP_Fox_chains")
    source = ordinary_source(geometry, tagged, witness["eta"])
    word_info = slp.values["w"]
    bound = word_info["length"] + 3 * abs(word_info["exponent"][0] // 6) * 1058 + 3 * abs(word_info["exponent"][1] // 6) * 466
    bound += 2 * abs(signed(word_info["omega"])) * (1058 + 466)
    if witness["kind"] == "auxiliary":
        bound = NORMALIZER_ATOMS["c_x" if witness["coordinate"] == 0 else "c_y"][0]
    require(word_info["length"] <= 6 * (2 * int(geometry.depth.max()) + 1) and slp.values["raw-root"]["length"] <= bound,
            "selected_raw_word_finite_length_bound")
    raw_word = document("raw-word", {"grammar": "ordered-slp-v1", "nodes": slp.nodes, "root": "raw-root",
        "cycles": witness["cycles"], "eta": witness["eta"],
        "node_values": [{"id": node["id"], **slp.values[node["id"]]} for node in slp.nodes],
        "normalizers": {"dictionary": normalizers["data"], "raw_relators_sha256": normalizers["roster_sha256"],
            "words": [{"name": name, "length": value[0], "word_sha256": value[1]} for name, value in NORMALIZER_ATOMS.items()]},
        "geometry_manifest_sha256": oracle["stage_hashes"]["geometry"], "witness_sha256": oracle["witness_sha256"],
        "word_bound": {"tree_height": int(geometry.depth.max()), "unrepaired": word_info["length"],
            "normalized": bound, "actual_slp_length": slp.values["raw-root"]["length"]}, "word_stream": word_stream,
        "legality": {"method": "v547-three-factor" if witness["kind"] == "chord" else "v459-ninth-power",
            "q0_identity": True, "q2_identity": True, "tau": [0] * 5, "epsilon_divisible18": True,
            "normalized_pair": witness["eta"], "omega": 0, "epsilon_exact_zero": not any(slp.values["raw-root"]["exponent"]),
            "omega_zero": True, "delta_endpoint_mode": "v547-retained-Gamma0-readout" if witness["kind"] == "chord" else "v459-retained-expGamma9",
            "actual_delta_enumerated": False, "normalizer_Q2_Fox_zero": True, "raw_chain_matches_witness": True}})
    roots, kappa = oracle["arrays"]["section"]["q.bin"], oracle["arrays"]["section"]["kappa.bin"]
    homogeneous = sum(dot(roots[a], source[2][a]) for a in range(4)) % 3
    section = dot(kappa, full_lower(source))
    require((homogeneous - section) % 3 == scalar, "ordinary27_actual_raw_source_scalar_anchor")
    raw_source = document("raw-source", {"method": "raw-Q2-Fox-and-six-tag-direct-SLP", "components": REFINE.source_components(source),
        "raw_word_sha256": sha(canonical(raw_word)), "chain_sha256": sha(pack(chain)), "eta": witness["eta"],
        "tag_chain_receipts": [{"tag": tag, "raw_fox_sha256": sha(pack(value)), "direct_fox_same": True, "q2_endpoint": 0}
                               for tag, value in enumerate(tagged)],
        "source_lower_sha256": sha(pack(full_lower(source))), "source_full_top_sha256": sha(pack(source[2])),
        "homogeneous_scalar": homogeneous, "section_scalar": section, "witness_scalar": scalar,
        "direct_raw_word_replay": True, "full_tag_eof": True, "eleven_slot_replay": False})
    return {"slp": slp, "chain": chain, "source": source, "raw_word": raw_word, "raw_source": raw_source,
            "homogeneous_scalar": homogeneous, "section_scalar": section, "selected_scalar": scalar}


ORACLE_ROSTER = {
    "geometry": {"next-pos.u32": ("u32le", [54432, 2]), "prev-pos.u32": ("u32le", [54432, 2]),
        "phi.u32": ("u32le", [6, 54432]), "parent.u32": ("u32le", [54432]), "parent-edge.u32": ("u32le", [54432]),
        "bfs-order.u32": ("u32le", [54432]), "carry.u8": ("u8", [108864, 5]), "chord-edges.u32": ("u32le", [54433]),
        "geometry.json": ("json", None), "tag-fox.json": ("json", None)},
    "section": {"q.bin": ("packed3", [4, 36288]), "p1-values.u8": ("u8", [4, 8059]), "chi.u8": ("u8", [8059]),
        "equation-values.u8": ("u8", [8059]), "equation-residuals.u8": ("u8", [8059]), "beta.u8": ("u8", [2014]),
        "kappa.bin": ("packed3", [96776]), "lead-original.u32": ("u32le", [8059]), "lead-embedded.u32": ("u32le", [8059]),
        "new-solve-order.u32": ("u32le", [6045]), "old-solve-order.u32": ("u32le", [2014]), "section.json": ("json", None)},
    "cochain": {"score.u8": ("u8", [6, 2, 54432]), "f.u8": ("u8", [108864]), "b-aux.u8": ("u8", [2]), "cochain.json": ("json", None)},
    "tree": {"potential-f.u8": ("u8", [54432]), "potential-tau.u8": ("u8", [54432, 5]),
        "chord-values.u8": ("u8", [54433]), "chord-tau.u8": ("u8", [54433, 5]), "chord-residuals.u8": ("u8", [54433]),
        "selected-chords.u32": ("u32le", [5]), "fit.u8": ("u8", [5]), "witness.json": ("json", None), "tree.json": ("json", None)}}


def canonical_json(raw: bytes, *, schema: str | None = None) -> dict[str, Any]:
    value = json.loads(raw)
    require(isinstance(value, dict) and canonical(value) == raw, "canonical_JSON_exact_bytes")
    if schema is not None:
        require(value.get("schema") == schema and type(value.get("sha256")) is str and
                value["sha256"] == sha(canonical({k: v for k, v in value.items() if k != "sha256"})), "generic_JSON_seal")
    return value


def read_pinned_oracle_entries(args: argparse.Namespace) -> dict[str, Any]:
    require(ORACLE_ARTIFACT and len(ORACLE_FILES) == 10 and args.oracle_root.is_dir(), "observed_oracle_parent_required")
    answer = {name: canonical_json(fixed(args.oracle_root, name, pin)) for name, pin in ORACLE_FILES.items()}
    for name in ("manifest", "owner", "start", "source", "result"):
        canonical_json(canonical(answer["output/" + name + ".json"]), schema=ORACLE.SCHEMA + "." + name)
    canonical_json(canonical(answer["checker-result.json"]), schema=ORACLE.SCHEMA + ".checker-result")
    old, checked, completion, repair, preserved = [answer[name] for name in
        ("source-receipt.json", "checker-result.json", "completion-run-receipt.json", "repair-source-receipt.json", "preserved-input.json")]
    launch = {key: ORACLE_ARTIFACT[key] for key in ("run", "attempt", "head")}
    workflow = {"file": ".github/workflows/d972-r07-section-cochain-checker-completion-v1.yml", "bytes": 44679,
                "sha256": "b439c24229523daec90570f527a72a5bdc5c32f475fd3a1ad0361922a0cb60e8"}
    origin = {"run": 33975617653, "attempt": 1, "head": "c57a722224320f9a573cfe84dea6979df5cb5320",
        "workflow": ".github/workflows/d972-r07-section-cochain-oracle-v1.yml", "artifact": 9972256636,
        "name": "d972-r07-section-cochain-oracle-v1-diagnostics-33975617653-1", "archive_bytes": 2271586,
        "archive_sha256": "sha256:c66e7477740c8c5e0c0e9e00e613836bf5baacf00f10acf63fad5b23d6cc113a"}
    require(completion["completion"] == {**launch, "workflow": workflow} and repair["launch"] == launch and repair["workflow"] == workflow and
            completion["origin"] == preserved["origin"] == origin, "oracle_two_distinct_run_origins")
    for key, name in (("new_checker_result_sha256", "checker-result.json"), ("source_receipt_sha256", "source-receipt.json"),
                      ("repair_source_receipt_sha256", "repair-source-receipt.json"), ("preserved_input_sha256", "preserved-input.json"),
                      ("producer_result_sha256", "output/result.json")):
        require(completion[key] == ORACLE_FILES[name][1], "oracle_completion_entry_chain:" + key)
    require(completion["status"] == "PASS" and completion["producer_invocations"] == 0 and completion["checker_invocations"] == 1 and
            completion["old_success_suites"] == completion["old_parent_canaries_executed"] == 0 and
            all(completion[key] is True for key in ("complete_A_to_D_replay", "all_stage_and_top_arrays_compared", "producer_output_unchanged")) and
            completion["output_files"] == preserved["output_file_count"] == 44 and completion["output_directories"] == 4 and
            completion["output_bytes"] == preserved["output_bytes"] == 5361492, "oracle_completion_full_output_and_execution")
    require(completion["producer_sha256"] == ORACLE_PRODUCER_SHA and completion["original_checker_sha256"] == ORACLE_CHECKER_SHA and
            completion["repaired_checker_sha256"] == checked["checker_sha256"] == ORACLE_REPAIRED_CHECKER_SHA and
            repair["files"][:14] == old["files"] and len(repair["files"]) == 15 and
            repair["files"][-1]["file"] == "search/check_d972_r07_section_cochain_oracle_v2.py" and
            repair["files"][-1]["sha256"] == ORACLE_REPAIRED_CHECKER_SHA and old["data"] == repair["data"] == FIXED.DATA_PINS,
            "original_producer_and_repaired_checker_source_lineages")
    for receipt in (checked, completion, repair):
        require(receipt["python"] == answer["output/source.json"]["python"] and
                receipt["numpy"] == answer["output/source.json"]["numpy"], "oracle_preserved_runtime")
    return answer


def oracle_semantics(oracle: dict[str, Any], current: dict[str, Any] | None = None) -> None:
    top, checked = oracle["entries"], oracle["entries"]["checker-result.json"]
    start, owner, source, result, manifest = [top["output/" + name + ".json"] for name in ("start", "owner", "source", "result", "manifest")]
    require(manifest["file_roster"] == ["cochain", "geometry", "manifest.json", "owner.json", "result.json", "section", "source.json", "start.json", "tree"] and
            [r["file"] for r in manifest["files"]] == ["owner.json", "result.json", "source.json", "start.json"], "oracle-roster")
    for key, value in ORACLE_SNAPSHOT.items():
        require(start[key] == result[key] == value, "oracle-snapshot")
    for key in ("rank", "generation", "state_head"):
        require(checked[key] == start[key], "oracle-snapshot")
    require(checked["status"] == result["status"] == "PASS" and
            checked["terminal"] == result["terminal"] == oracle["json"]["tree"]["tree.json"]["terminal"] and
            result["terminal"] in ("VIOLATION_CANDIDATE", "COMPLETE_ZERO_CANDIDATE") and start["kind"] == "Separator", "oracle_terminal_type")
    require(checked["all_stage_arrays_compared"] is True and checked["section_equalities"] == 8059 and checked["chords_checked"] == 54433 and
            checked["auxiliary_tests"] == 2 and checked["new_physical_appends"] == result["physical_appends"] == 0 and
            result["all8059_section_equalities"] is True and result["all54433_chords_checked"] is True and
            oracle["json"]["geometry"]["geometry.json"]["full_edge_eof"] is True and
            oracle["json"]["section"]["section.json"]["equation_eof"] is True and
            oracle["json"]["cochain"]["cochain.json"]["edge_eof"] is True and
            oracle["json"]["tree"]["tree.json"]["full_chord_eof"] is True, "oracle-eof")
    require(source["producer_sha256"] == ORACLE_PRODUCER_SHA and source["data"] == FIXED.DATA_PINS and
            result["source_sha256"] == manifest["source_sha256"] == ORACLE_FILES["output/source.json"][1] and
            checked["result_sha256"] == manifest["result_sha256"] == ORACLE_FILES["output/result.json"][1] and
            checked["manifest_sha256"] == ORACLE_FILES["output/manifest.json"][1], "oracle_current_source_receipts")
    require(result["owner_sha256"] == checked["owner_sha256"] == manifest["owner_sha256"] == ORACLE_FILES["output/owner.json"][1] and
            result["snapshot_sha256"] == checked["snapshot_sha256"] == manifest["snapshot_sha256"] == ORACLE_FILES["output/start.json"][1] and
            result["stage_manifests"] == checked["stage_manifests"] == manifest["stage_manifests"] == oracle["stage_hashes"], "oracle_current_root_receipts")
    require(result["witness_sha256"] == oracle["witness_sha256"] == sha(canonical(oracle["witness"])), "oracle-witness-scalar")
    witness = oracle["witness"]
    if result["terminal"] == "VIOLATION_CANDIDATE":
        require(type(witness["scalar"]) is int and witness["scalar"] in (1, 2) and witness["tau"] == [0] * 5 and
                witness["kind"] in ("chord", "auxiliary") and witness["materialization"] == "MATERIALIZATION_PENDING", "oracle-witness-scalar")
    else:
        require(witness["kind"] == "none" and witness["scalar"] == 0, "oracle_zero_witness")
    if current is not None:
        for key in ("rank", "generation", "state_head", "lambda_sha256", "target_remainder_sha256"):
            require(start[key] == current[key], "oracle-current-root")
        for key in ("accepted_refinement_layout", "accepted_target_derivation_parents", "lambda_rho2", "direct_pairing"):
            same(start[key], current[key], "oracle-current-root")


def read_oracle(args: argparse.Namespace) -> dict[str, Any]:
    entries = read_pinned_oracle_entries(args)
    root, manifest = args.oracle_root / "output", entries["output/manifest.json"]
    require(root.is_dir() and not root.is_symlink() and sorted(p.name for p in root.iterdir()) == manifest["file_roster"], "oracle_output_top_roster")
    for receipt in manifest["files"]:
        require(receipt == {"file": receipt["file"], "bytes": ORACLE_FILES["output/" + receipt["file"]][0],
                            "sha256": ORACLE_FILES["output/" + receipt["file"]][1]}, "oracle_top_file_receipts")
    stage_hashes, arrays, metadata, observed = {}, {}, {}, {}
    for name, specification in ORACLE_ROSTER.items():
        stage_root = root / name
        require(stage_root.is_dir() and not stage_root.is_symlink() and
                {p.name for p in stage_root.iterdir()} == set(specification) | {"manifest.json"}, "oracle_stage_roster")
        item = path(stage_root, "manifest.json")
        require(item.stat().st_size < (1 << 20), "oracle_stage_manifest_size")
        raw = item.read_bytes(); stage_hashes[name] = sha(raw)
        require(stage_hashes[name] == manifest["stage_manifests"][name], "oracle_stage_root_hash")
        stage = canonical_json(raw, schema=ORACLE.SCHEMA + ".stage-manifest")
        dependencies = () if name in ("geometry", "section") else (("geometry", "section") if name == "cochain" else ("geometry", "cochain"))
        require(stage["stage"] == name and stage["owner_sha256"] == manifest["owner_sha256"] and
                stage["snapshot_sha256"] == manifest["snapshot_sha256"] and
                stage["inputs"] == {key: stage_hashes[key] for key in dependencies} and
                [r["file"] for r in stage["files"]] == sorted(specification), "oracle_stage_typed_joins")
        arrays[name], metadata[name] = {}, {}
        for receipt in stage["files"]:
            file, size = receipt["file"], receipt["bytes"]
            dtype, shape = specification[file]
            require(receipt["dtype"] == dtype and receipt["shape"] == shape and type(size) is int and 0 < size < (1 << 24), "oracle_array_typed_roster")
            data = fixed(stage_root, file, (size, receipt["sha256"]))
            observed[name + "/" + file] = (size, sha(data))
            if dtype == "json":
                metadata[name][file] = canonical_json(data, schema=None if file == "tag-fox.json" else ORACLE.SCHEMA + "." + file[:-5])
            else:
                count = 1
                for dimension in shape:
                    count *= dimension
                require(len(data) == ((count + 3) // 4 if dtype == "packed3" else count * (4 if dtype == "u32le" else 1)), "oracle_array_exact_EOF")
                array = unpack(data, count) if dtype == "packed3" else np.frombuffer(data, dtype="<u4" if dtype == "u32le" else np.uint8)
                if dtype == "u8":
                    require(not np.any(array > 2), "oracle_array_trit_type")
                arrays[name][file] = array.reshape(shape)
        boundary("accepted_oracle_stage_hash_EOF", stage=name)
    oracle = {"entries": entries, "stage_hashes": stage_hashes, "arrays": arrays, "json": metadata,
        "witness": metadata["tree"]["witness.json"], "witness_sha256": observed["tree/witness.json"][1]}
    oracle_semantics(oracle)
    return oracle


def oracle_layout(oracle: dict[str, Any]) -> dict[str, Any]:
    start, result = oracle["entries"]["output/start.json"], oracle["entries"]["output/result.json"]
    return document("oracle-parent-layout", {"artifact": ORACLE_ARTIFACT,
        "entry_files": [{"file": name, "bytes": pin[0], "sha256": pin[1]} for name, pin in sorted(ORACLE_FILES.items())],
        **{name + "_sha256": ORACLE_FILES["output/" + name + ".json"][1] for name in ("manifest", "start", "owner", "source", "result")},
        "witness_sha256": oracle["witness_sha256"], "terminal": result["terminal"],
        **{key: start[key] for key in ("state_head", "rank", "generation", "lambda_sha256", "target_remainder_sha256")},
        "old_arithmetic_replayed": False})


SCOPE = {"snapshot_count": 1, "physical_appends": 1, "characters": [0, 1, 2, 3], "source_tags": 6,
    "p1_rows": 8059, "source_lower_trits": 96776, "physical_trits": 48384, "max_cycles": 6,
    "full_raw_word_source_replay": True, "full_normalized_word_replay": False, "eleven_slot_replay": False}
FORMULA = "v547-literal-repair;v548-primal-section;four-B;one-physical-row"


def new_start_owner(state: dict[str, Any], tables: list[Any], oracle: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    current, old_owner = ORACLE.start_and_owner(state, tables)
    oracle_semantics(oracle, current)
    same(old_owner, oracle["entries"]["output/owner.json"], "oracle_actual_inherited_owner")
    inherited = ("p1_parent", "task554_parent", "task712_parent", "task712_manifest_sha256", "word_dictionary_sha256", "relator_dictionary_sha256")
    owner = document("owner", {"formula_id": FORMULA, "scope": SCOPE,
        "oracle_owner_sha256": ORACLE_FILES["output/owner.json"][1], "refinement_head_sha256": ORACLE.REFINEMENT_FILES["output/HEAD"][1],
        **{key: old_owner[key] for key in inherited}})
    start = document("start", {**{key: current[key] for key in ("kind", "rank", "generation", "state_head", "lambda_sha256",
        "target_remainder_sha256", "accepted_refinement_layout", "accepted_target_derivation_parents", "lambda_rho2", "direct_pairing")},
        "accepted_oracle_layout": oracle_layout(oracle)})
    return start, owner


def producer_source() -> dict[str, Any]:
    retained = ORACLE.producer_source_receipt()
    modules = {**retained["modules"], "d972_r07_section_cochain_oracle_v1.py": ORACLE_PRODUCER_SHA}
    require(retained["producer_sha256"] == ORACLE_PRODUCER_SHA, "immutable_oracle_producer_source")
    producer = Path(__file__).resolve().with_name("d972_r07_selected_cycle_materializer_v1.py")
    require(producer.is_file() and not producer.is_symlink() and sha(producer.read_bytes()) == PRODUCER_SHA, "current_producer_source_pin")
    data = {**FIXED.DATA_PINS, NORMALIZER_DATA["file"]: {key: NORMALIZER_DATA[key] for key in ("bytes", "sha256")}}
    for name, pin in data.items():
        fixed(Path(__file__).resolve().parents[1], name, (pin["bytes"], pin["sha256"]))
    return document("source", {"producer_sha256": PRODUCER_SHA, "modules": modules, "data": data, "python": sys.version, "numpy": np.__version__})


def one_physical_row(raw: np.ndarray, old_target: np.ndarray, old_lambda: np.ndarray, pivots: list[dict[str, Any]],
                     row_reader: Callable[[int], bytes], offer: int, selected: int) -> dict[str, Any]:
    require(dot(old_lambda, raw) == selected and selected in (1, 2), "physical_selected_nonzero_scalar")
    remainder, reductions = LEGACY.reduce_dense(raw, pivots, row_reader, verbose=True)
    require(dot(old_lambda, remainder) == selected, "old_lambda_remainder_scalar")
    normalized, lead, sigma = LEGACY.normalize(remainder)
    target, scalar = LEGACY.next_target(old_target, normalized, lead, [p["lead"] for p in pivots])
    separator, functional = None, None
    if np.any(target):
        step = LEGACY.next_separator(target, pivots, normalized, lead, row_reader, offer)
        functional = step["lambda"]
        pairings = [dot(functional, unpack(row_reader(i), len(raw))) for i in range(len(pivots))]
        pairings.append(dot(functional, normalized))
        parent_dot, target_dot = dot(functional, old_target), dot(functional, target)
        require(not any(pairings) and parent_dot == target_dot == 1, "fresh_lambda_all_current_rows_both_targets")
        separator = {"free_coordinate": step["free_coordinate"], "free_value": step["free_value"], "lambda_sha256": sha(pack(functional)),
            "direct_pairing": {"rows": len(pairings), "row_pairings_sha256": sha(bytes(pairings)), "lambda_pivots": 0,
                               "lambda_parent_remainder": parent_dot, "lambda_new_remainder": target_dot}}
    return {"raw": raw, "remainder": remainder, "normalized": normalized, "lead": lead, "sigma": sigma,
        "reductions": reductions, "target": target, "target_scalar": scalar, "separator": separator, "lambda": functional,
        "kind": "Separator" if separator is not None else "LinearMembershipCandidate",
        "terminal": "PIVOT_CANDIDATE" if separator is not None else "LINEAR_MEMBERSHIP_CANDIDATE"}


def source_correction_record(raw: dict[str, Any], corrected: tuple[np.ndarray, ...], primal: dict[str, Any],
                             basis: dict[str, Any], roots: dict[str, Any], index: dict[str, Any]) -> dict[str, Any]:
    exponent = raw["slp"].values["raw-root"]["exponent"].copy()
    for event in primal["events"]:
        pair = residue_pair(basis["pairs"][event["node"]])
        for axis in range(2):
            exponent[axis] += event["literal_exponent"] * pair[axis]
    residue = residue_pair([value % 54 for value in exponent])
    require(all(value in (0, 18, 36) for value in residue), "corrected_literal_epsilon_divisible18")
    eta = [value // 18 for value in residue]
    require(eta == corrected[3][6:].tolist(), "same_corrected_literal_normalized_pair")
    return document("source-correction", {"operation": "ordered-product", "raw_word_sha256": sha(canonical(raw["raw_word"])),
        "p1_factor_order": "event-ascending", "p1_factors": [{key: event[key] for key in ("event", "node", "coefficient", "literal_exponent")} |
            {"p1_sha256": index["references"][event["node"]]["p1_sha256"]} for event in primal["events"]],
        "p1_roots_sha256": sha(canonical(roots)), "coefficients_sha256": sha(primal["alpha"].tobytes()),
        "exponent_residue_mod54": residue, "normalized_pair": eta, "components": REFINE.source_components(corrected),
        "source_lower_zero": {"trits": SOURCE_LOWER, "packed_sha256": sha(pack(primal["lower"]))},
        "source_lower_equality": True, "top_characters": [0, 1, 2, 3], "whole_word_direct_replay": False,
        "canonical_p1_source_replay": True, "eleven_slot_replay": False})


def new_delta_records(start: dict[str, Any], owner: dict[str, Any], source: dict[str, Any], oracle: dict[str, Any],
                      raw: dict[str, Any], correction: dict[str, Any], roots: dict[str, Any], reductions: dict[str, Any],
                      physical: dict[str, Any], corrected_scalar: int) -> dict[str, Any]:
    scalar = raw["selected_scalar"]
    literal = document("physical-literal", {"operation": "scaled-ordered-product", "source_correction_sha256": sha(canonical(correction)),
        "accepted_physical_head": start["state_head"], "physical_factors": [{**r, "literal_exponent": -signed(r["scalar"])} for r in physical["reductions"]],
        "sigma": physical["sigma"], "literal_outer_exponent": signed(physical["sigma"]), "source_lower_zero": "NOT_ASSERTED",
        "physical_lower_zero": True, "physical_normalized_sha256": sha(pack(physical["normalized"])),
        "whole_word_direct_replay": False, "eleven_slot_replay": False, "target_word_direct_replay": False})
    instruction = {"schema": SCHEMA + ".instruction", "predecessor": start["state_head"], "offer": start["generation"],
        "rank": start["rank"] + 1, "generation": start["generation"] + 1, "physical_offset": start["rank"] * ROW_BYTES,
        "origin": {"kind": "v548-cycle" if oracle["witness"]["kind"] == "chord" else "v548-aux",
            "oracle_manifest_sha256": ORACLE_FILES["output/manifest.json"][1], "witness_sha256": oracle["witness_sha256"],
            "raw_word_sha256": sha(canonical(raw["raw_word"]))}, "source_correction_sha256": sha(canonical(correction)),
        "physical_literal_sha256": sha(canonical(literal)), "p1_roots_sha256": sha(canonical(roots)),
        "p1_reductions_sha256": sha(canonical(reductions)), "physical_reductions": physical["reductions"],
        "lead": physical["lead"], "sigma": physical["sigma"], "physical_sha256": sha(pack(physical["normalized"])),
        "selected_scalar": scalar, "target_scalar": physical["target_scalar"], "target_remainder_sha256": sha(pack(physical["target"]))}
    instruction["rolling_sha256"] = sha(bytes.fromhex(start["state_head"]) + canonical(instruction))
    target = {"parent_remainder_sha256": start["target_remainder_sha256"], "remainder_sha256": sha(pack(physical["target"])), "scalar": physical["target_scalar"]}
    derivation = {"mode": "derived", "original_rho2_directly_read": False,
        "original_rho2_packed_sha256": start["lambda_rho2"]["original_rho2_packed_sha256"],
        "accepted_target_derivation_parents": start["accepted_target_derivation_parents"],
        "new_delta": {"instruction_sha256": sha(canonical(instruction)), "state_head": instruction["rolling_sha256"],
            "normalized_sha256": sha(pack(physical["normalized"])), "target_sha256": sha(canonical(target))},
        "identity": "parent_remainder - new_remainder = target.scalar * new_normalized_row"}
    separator = physical["separator"]
    if separator is not None:
        separator = {**separator, "lambda_rho2": {"mode": "derived", "value": 1, "original_rho2_directly_read": False,
            "target_derivation": derivation, "new_target_steps_executed": 1}}
    result = document("result", {"status": "PASS", "terminal": physical["terminal"], "kind": physical["kind"],
        "owner_sha256": sha(canonical(owner)), "start_sha256": sha(canonical(start)), "source_sha256": sha(canonical(source)),
        "parent_state_head": start["state_head"], "state_head": instruction["rolling_sha256"],
        "rank_before": start["rank"], "rank_after": start["rank"] + 1, "generation_before": start["generation"], "generation_after": start["generation"] + 1,
        "selected_scalar": scalar, "homogeneous_scalar": raw["homogeneous_scalar"], "section_scalar": raw["section_scalar"],
        "corrected_scalar": corrected_scalar, "physical_scalar": scalar, "remainder_scalar": scalar,
        "pivot": {"lead": physical["lead"], "scale": physical["sigma"], "normalized_sha256": sha(pack(physical["normalized"])), "reductions": physical["reductions"]},
        "target": target, "separator": separator, "target_derivation": derivation,
        "raw_word_sha256": sha(canonical(raw["raw_word"])), "source_correction_sha256": sha(canonical(correction)),
        "physical_literal_sha256": sha(canonical(literal)), "p1_roots_sha256": sha(canonical(roots)), "instruction_sha256": sha(canonical(instruction)),
        "physical_appends": 1, "positive_readout": "TASK958_PENDING" if separator is None else "NOT_APPLICABLE",
        "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False,
        "candidate": True, "cross_checked": False, "verified": False})
    return {"physical-literal.json": literal, "instruction.json": instruction, "result.json": result}


def grouped_forward(entries: np.ndarray, source: np.ndarray, width: int = PHYSICAL) -> np.ndarray:
    """Group integer contributions by output coordinate before reducing in F3."""
    require(entries.ndim == 2 and entries.shape[1] == 3 and
            np.all((entries[:, 0] >= 0) & (entries[:, 0] < source.size)) and
            np.all((entries[:, 1] >= 0) & (entries[:, 1] < width)), "forward_B_typed_entries")
    out = np.zeros(width, dtype=np.uint8)
    if len(entries):
        order = np.argsort(entries[:, 1], kind="stable")
        positions = entries[order, 1]
        starts = np.concatenate((np.array([0], dtype=np.int64), np.flatnonzero(positions[1:] != positions[:-1]) + 1))
        summands = entries[order, 2].astype(np.int64) * source[entries[order, 0]].astype(np.int64)
        out[positions[starts]] = np.add.reduceat(summands, starts) % 3
    return out


def check_telemetry(root: Path, payloads: dict[str, Any], stages: dict[str, list[str]], alpha_support: int, letters: int) -> dict[str, Any]:
    item = path(root, "telemetry.json")
    require(item.stat().st_size < (1 << 20), "telemetry_size")
    actual = canonical_json(item.read_bytes(), schema=SCHEMA + ".telemetry")
    require(isinstance(actual["stages"], list) and len(actual["stages"]) == 6, "telemetry_six_complete_stages")
    expected = []
    for record, (stage, names) in zip(actual["stages"], stages.items()):
        elapsed = record["elapsed_seconds"]
        require(type(elapsed) in (int, float) and np.isfinite(elapsed) and elapsed >= 0, "telemetry_finite_nonnegative_time")
        expected.append({"stage": stage, "elapsed_seconds": elapsed, "bytes": sum(len(payloads[name][0]) for name in names),
            "eof": True, "alpha_support": alpha_support if stage in ("primal", "p1") else None, "letters": letters if stage == "raw" else None})
    wanted = document("telemetry", {"stages": expected, "old_scans_numerically_replayed": 0,
        "old_inserts_numerically_replayed": 0, "physical_appends": 1})
    same(actual, wanted, "all_non_time_telemetry_fields")
    return wanted


def finalize_candidate(root: Path, payloads: dict[str, Any], start: dict[str, Any], owner: dict[str, Any], source: dict[str, Any],
                       physical: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    instruction = json.loads(payloads["instruction.json"][0])
    state_head = instruction["rolling_sha256"]
    manifest = document("manifest", {"owner_sha256": sha(canonical(owner)), "start_sha256": sha(canonical(start)),
        "source_sha256": sha(canonical(source)), "result_sha256": sha(payloads["result.json"][0]),
        "instruction_sha256": sha(payloads["instruction.json"][0]), "parent_state_head": start["state_head"], "state_head": state_head,
        "files": [{"file": name, "bytes": len(data), "sha256": sha(data), "dtype": dtype, "shape": shape}
                  for name, (data, dtype, shape) in sorted(payloads.items())],
        "stage_eof": ["raw", "source", "primal", "p1", "B", "physical"], "candidate": True, "cross_checked": False, "verified": False})
    head = document("head", {"owner_sha256": sha(canonical(owner)), "source_sha256": sha(canonical(source)), "start_sha256": sha(canonical(start)),
        "manifest_sha256": sha(canonical(manifest)), "instruction_sha256": sha(payloads["instruction.json"][0]),
        "parent_state_head": start["state_head"], "state_head": state_head, "rank": start["rank"] + 1,
        "generation": start["generation"] + 1, "kind": physical["kind"], "completed_steps": 1,
        "physical_sha256": sha(pack(physical["normalized"])), "target_remainder_sha256": sha(pack(physical["target"])),
        "lambda_sha256": None if physical["lambda"] is None else sha(pack(physical["lambda"]))})
    expected = {**{name: value[0] for name, value in payloads.items()}, "manifest.json": canonical(manifest), "HEAD": canonical(head)}
    require(root.is_dir() and not root.is_symlink() and {p.name for p in root.iterdir()} == set(expected), "complete_new_candidate_roster")
    errors = []
    for name, raw in expected.items():
        with path(root, name).open("rb") as stream:
            if stream.read(len(raw) + 1) != raw:
                errors.append(name)
    require(not errors, "full_payload_bytes_and_EOF:" + ",".join(errors))
    return manifest, head


def check_actual(args: argparse.Namespace) -> dict[str, Any]:
    source = producer_source()
    oracle = read_oracle(args)
    if oracle["entries"]["output/result.json"]["terminal"] == "COMPLETE_ZERO_CANDIDATE":
        result = document("not-applicable", {"status": "NOT_APPLICABLE", "terminal": "NOT_APPLICABLE",
            "oracle_terminal": "COMPLETE_ZERO_CANDIDATE", "accepted_oracle_layout": oracle_layout(oracle),
            "physical_appends": 0, "candidate": False, "cross_checked": False, "verified": False})
        require({p.name for p in args.candidate_root.iterdir()} == {"not-applicable.json"} and
                path(args.candidate_root, "not-applicable.json").read_bytes() == canonical(result), "zero_oracle_typed_not_applicable")
        return result
    metadata = ORACLE.accepted_refinement_metadata(args)
    boundary("current_physical_parent_begin")
    state = ORACLE.current_snapshot(args, metadata)
    tables = REFINE.load_tables(args)
    start, owner = new_start_owner(state, tables, oracle)
    current_roots = np.stack([FIXED.pullback(table["entries"], state["start_lambda"]) for table in tables])
    require(np.array_equal(current_roots, oracle["arrays"]["section"]["q.bin"]), "actual_all_four_current_B_roots")
    context, words = BASE.checker_source_context()
    geometry = SelectedGeometry(context, oracle["arrays"]["geometry"])
    raw = raw_materialization(geometry, normalizer_words(), oracle)
    COMPLETED_STAGES.extend(("raw", "source"))
    boundary("raw_and_source_actual_EOF", letters=raw["slp"].values["raw-root"]["length"])
    basis = source_basis_metadata(state, words)
    index = authenticate_literal_instructions(args, state, basis)
    require([r["original_lead"] for r in basis["records"]] == oracle["arrays"]["section"]["lead-original.u32"].tolist() and
            [r["embedded_lead"] for r in basis["records"]] == oracle["arrays"]["section"]["lead-embedded.u32"].tolist(), "oracle_section_same_original_basis_ids")
    primal = actual_primal(args, raw["source"], basis)
    COMPLETED_STAGES.append("primal")
    corrected, roots = p1_corrected_source(args, raw["source"], basis, primal, index)
    correction = source_correction_record(raw, corrected, primal, basis, roots, index)
    COMPLETED_STAGES.append("p1")
    by_character = np.stack([grouped_forward(tables[a]["entries"], corrected[2][a]) for a in range(4)])
    physical_raw = (by_character.sum(axis=0, dtype=np.uint16) % 3).astype(np.uint8)
    corrected_scalar = sum(dot(current_roots[a], corrected[2][a]) for a in range(4)) % 3
    require(corrected_scalar == raw["selected_scalar"] == dot(state["start_lambda"], physical_raw) and
            corrected_scalar == (raw["homogeneous_scalar"] - raw["section_scalar"]) % 3, "same_witness_full_four_B_sum")
    COMPLETED_STAGES.append("B")
    boundary("physical_single_row_begin", alpha_support=int(np.count_nonzero(primal["alpha"])))
    with path(args.state_root, "state/physical.bin").open("rb", buffering=1 << 20) as stream:
        def row_reader(number: int) -> bytes:
            return LEGACY.blob_row(stream, number, PHYSICAL) if number < 1354 else state["saved_rows"][number - 1354]
        physical = one_physical_row(physical_raw, state["start_target"], state["start_lambda"], state["pivots"], row_reader,
                                    start["generation"], raw["selected_scalar"])
    reduction_record = document("p1-reductions", {"order": "old-global-ascending-embedded-original-lead;new-owner-major-ascending-original-lead",
        "rows": 8059, "events": primal["events"], "coefficients_sha256": sha(primal["alpha"].tobytes()),
        "lower_zero": {"trits": SOURCE_LOWER, "packed_sha256": sha(pack(primal["lower"]))}, "eof": True})
    exponent_record = document("p1-exponent-residues", {"rows": 8059, "order": "canonical-row-id", "modulus": 54,
        "pairs": basis["pairs"], "p1_manifest_sha256": BASE.P1_MANIFEST_SHA256, "instruction_sha256": BASE.P1_INSTRUCTION_SHA256,
        "method": "ordered-signed-DAG-exponent-mod54", "eof": True})
    records = new_delta_records(start, owner, source, oracle, raw, correction, roots, reduction_record, physical, corrected_scalar)
    COMPLETED_STAGES.append("physical")
    json_payload, array_payload = ORACLE.json_payload, ORACLE.typed_array
    payloads = {"owner.json": json_payload(owner), "start.json": json_payload(start), "source.json": json_payload(source),
        "raw-word.json": json_payload(raw["raw_word"]), "raw-chain.bin": array_payload(raw["chain"], "packed3", (EDGES,)),
        "raw-source.json": json_payload(raw["raw_source"]), "p1-coefficients.u8": array_payload(primal["alpha"], "u8", (8059,)),
        "p1-reductions.json": json_payload(reduction_record), "p1-exponent-residues.json": json_payload(exponent_record),
        "p1-roots.json": json_payload(roots), "source-lower-remainder.bin": array_payload(primal["lower"], "packed3", (SOURCE_LOWER,)),
        "source-top-corrected.bin": array_payload(corrected[2], "packed3", (4, SOURCE_TOP)), "source-correction.json": json_payload(correction),
        "physical-by-character.bin": array_payload(by_character, "packed3", (4, PHYSICAL)),
        "physical-raw.bin": array_payload(physical["raw"], "packed3", (PHYSICAL,)),
        "physical-remainder.bin": array_payload(physical["remainder"], "packed3", (PHYSICAL,)),
        "physical-normalized.bin": array_payload(physical["normalized"], "packed3", (PHYSICAL,)),
        "target-remainder.bin": array_payload(physical["target"], "packed3", (PHYSICAL,)),
        **{name: json_payload(value) for name, value in records.items()}}
    for role, part in zip(("d0", "d1", "d2", "aux"), raw["source"]):
        payloads["raw-source-" + role + ".bin"] = array_payload(part, "packed3", part.shape)
    if physical["lambda"] is not None:
        payloads["lambda.bin"] = array_payload(physical["lambda"], "packed3", (PHYSICAL,))
    stages = {"raw": ["raw-word.json", "raw-chain.bin"],
        "source": ["raw-source-" + name + ".bin" for name in ("d0", "d1", "d2", "aux")] + ["raw-source.json"],
        "primal": ["p1-coefficients.u8", "p1-reductions.json", "p1-exponent-residues.json"],
        "p1": ["p1-roots.json", "source-lower-remainder.bin", "source-top-corrected.bin", "source-correction.json"],
        "B": ["physical-by-character.bin", "physical-raw.bin"],
        "physical": ["physical-remainder.bin", "physical-normalized.bin", "physical-literal.json", "instruction.json", "target-remainder.bin"] +
            (["lambda.bin"] if physical["lambda"] is not None else []) + ["result.json"]}
    telemetry = check_telemetry(args.candidate_root, payloads, stages, int(np.count_nonzero(primal["alpha"])), raw["slp"].values["raw-root"]["length"])
    payloads["telemetry.json"] = json_payload(telemetry)
    manifest, head = finalize_candidate(args.candidate_root, payloads, start, owner, source, physical)
    boundary("all_selected_cycle_payloads_compared", terminal=physical["terminal"], files=len(payloads) + 2)
    return document("checker-result", {"status": "PASS", "terminal": physical["terminal"], "kind": physical["kind"],
        "owner_sha256": sha(canonical(owner)), "start_sha256": sha(canonical(start)), "manifest_sha256": sha(canonical(manifest)),
        "head_sha256": sha(canonical(head)), "result_sha256": sha(payloads["result.json"][0]), "instruction_sha256": sha(payloads["instruction.json"][0]),
        "state_head": head["state_head"], "rank": head["rank"], "generation": head["generation"], "physical_appends": 1,
        "all_arrays_and_json_compared": True, "ordinary27_actual_raw_source": True, "direct_raw_word_replay": True, "source_lower_trits": SOURCE_LOWER,
        "source_lower_zero": True, "p1_rows": 8059, "p1_literal_exponents_modulus": 54, "all_four_B_summed": True,
        "selected_scalar": raw["selected_scalar"], "target_scalar": physical["target_scalar"], "separator": records["result.json"]["separator"],
        "target_derivation": records["result.json"]["target_derivation"], "accepted_oracle_layout": oracle_layout(oracle),
        "old_scans_numerically_replayed": 0, "old_inserts_numerically_replayed": 0, "old_oracle_arithmetic_replayed": False,
        "full_normalized_word_replay": False, "eleven_slot_replay": False, "positive_readout": records["result.json"]["positive_readout"],
        "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False,
        "checker_sha256": sha(Path(__file__).read_bytes()), "retained_oracle_checker_sha256": ORACLE_CHECKER_SHA,
        "accepted_completion_checker_sha256": ORACLE_REPAIRED_CHECKER_SHA, "python": sys.version, "numpy": np.__version__,
        "elapsed_seconds": time.monotonic() - STARTED, "completed_stages": COMPLETED_STAGES.copy(), "producer_telemetry": telemetry,
        "candidate": True, "cross_checked": False, "verified": False})


def rejected(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (ValueError, KeyError, TypeError, IndexError):
        return
    raise ValueError("selected_cycle_checker:mutation_accepted:" + label)


def parent_layout_selftest(args: argparse.Namespace) -> dict[str, Any]:
    inherited = ORACLE.parent_layout_selftest(args)
    oracle = read_oracle(args)
    same(oracle["entries"]["output/start.json"]["accepted_refinement_layout"], inherited["accepted_refinement_layout"], "actual_oracle_refinement_layout")
    current = dict(oracle["entries"]["output/start.json"])
    metadata = ORACLE.accepted_refinement_metadata(args)
    layout = ORACLE.refinement_layout(metadata)
    current.update({key: layout[key] for key in ("rank", "generation", "state_head", "lambda_sha256", "target_remainder_sha256")})
    current["accepted_refinement_layout"] = layout
    oracle_semantics(oracle, current)
    names = list(inherited["rejected_cases"])
    for label in ("oracle-roster", "oracle-witness-scalar", "oracle-snapshot", "oracle-eof", "oracle-current-root"):
        mutant = {**oracle, "entries": copy.deepcopy(oracle["entries"]), "json": copy.deepcopy(oracle["json"]), "witness": dict(oracle["witness"])}
        root = dict(current)
        if label == "oracle-roster":
            mutant["entries"]["output/manifest.json"]["file_roster"].remove("tree")
        elif label == "oracle-witness-scalar":
            mutant["witness"]["scalar"] = 0
        elif label == "oracle-snapshot":
            mutant["entries"]["output/result.json"]["generation"] += 1
        elif label == "oracle-eof":
            mutant["json"]["section"]["section.json"]["equation_eof"] = False
        else:
            root["state_head"] = "0" * 64
        rejected(lambda: oracle_semantics(mutant, root), label)
        names.append(label)
    require(len(names) == len(set(names)) == 20, "actual_parent_twenty_distinct_refusals")
    return document("parent-layout-selftest", {"status": "PASS", "metadata_only": True,
        **{key: inherited[key] for key in ("parent_layout", "accepted_packet_layout", "accepted_refinement_layout")},
        "accepted_oracle_layout": oracle_layout(oracle), "rejected_cases": names, "cross_checked": False, "verified": False})


def selftest() -> dict[str, Any]:
    """Three new production-interface gates, without the old complete oracle suite."""
    ORACLE.check_source_data()
    context, words = BASE.checker_source_context()
    # Retained geometry only supplies a parent-free actual-input fixture. No old
    # section, cochain, complete tree test, or old selftest is called here.
    fixture = ORACLE.Geometry(context)
    parent, parent_edge = fixture.tree_parent.astype(np.int64), fixture.tree_edge.astype(np.int64)
    parent[0] = parent_edge[0] = 4294967295
    arrays = {"next-pos.u32": fixture.successor, "prev-pos.u32": fixture.inverse_successor, "phi.u32": fixture.tag_maps,
        "parent.u32": parent.astype("<u4"), "parent-edge.u32": parent_edge.astype("<u4"), "bfs-order.u32": fixture.tree_order,
        "carry.u8": fixture.carry, "chord-edges.u32": fixture.chords}
    geometry = SelectedGeometry(context, arrays)
    del fixture
    x, y = geometry.generators
    require(geometry.multiply(x, y) != geometry.multiply(y, x), "canary_actual_noncommuting_endpoints")
    normalizers = normalizer_words()
    slp = RawSLP(geometry, normalizers["atoms"])
    slp.add("x", "Letter", letter=1); slp.add("y", "Letter", letter=2)
    slp.add("yx", "OrderedProduct", factors=["y", "x"])
    slp.add("negative-path", "IntegerPower", node="yx", exponent=-2)
    short_chain, short_endpoint = slp.chain("negative-path")
    flat_short, flat_short_endpoint = flat_fox_chain([-1, -2, -1, -2], geometry)
    require(short_endpoint == flat_short_endpoint and np.array_equal(short_chain, flat_short) and
            slp.values["negative-path"] == letter_statistics([-1, -2, -1, -2], geometry) and slp.values["yx"]["omega"] == 1,
            "canary_noncommuting_negative_ordered_product_Fox_and_omega")
    slp.add("rx", "Ref", namespace="normalizer-v459", key="r_x")
    slp.add("ry", "Ref", namespace="normalizer-v459", key="r_y")
    slp.add("rx3", "IntegerPower", node="rx", exponent=3)
    slp.add("ry3", "IntegerPower", node="ry", exponent=3)
    slp.add("rxi", "Inverse", node="rx"); slp.add("ryi", "Inverse", node="ry")
    slp.add("comm", "OrderedProduct", factors=["rxi", "ryi", "rx", "ry"])
    atom_chain, atom_endpoint = slp.chain("rx")
    require(atom_endpoint == 0 and np.any(atom_chain) and int(atom_chain.reshape(VERTICES, 2)[:, 0].sum(dtype=np.uint64) % 3) == 2,
            "canary_atom_Fox_augmentation_is_nonzero")
    for name in ("rx3", "ry3", "comm"):
        repair_chain, repair_endpoint = slp.chain(name)
        require(repair_endpoint == 0 and not np.any(repair_chain), "canary_actual_three_repair_Fox_chains_zero")
    seed = normalizers["atoms"]["r_x"] * 9
    slp.add("raw-root", "IntegerPower", node="rx", exponent=-9)
    require(slp.values["raw-root"] == letter_statistics(inverse_word(seed), geometry), "canary_negative_power_all_statistics")
    chain, endpoint = slp.chain("raw-root")
    flat, flat_endpoint = flat_fox_chain(inverse_word(seed), geometry)
    require(endpoint == flat_endpoint == 0 and np.array_equal(chain, flat), "canary_actual_SLP_Fox_inverse_chain")
    tags = tag_chain_from_raw(geometry, chain)
    direct, stream = direct_slp_tag_chains(slp)
    require(all(np.array_equal(a, b) for a, b in zip(tags, direct)), "canary_actual_six_tag_SLP_connection")
    epsilon = slp.values["raw-root"]["exponent"]
    require(all(value % 18 == 0 for value in epsilon), "canary_legal_raw_integer_exponents")
    eta = [(value // 18) % 3 for value in epsilon]
    actual = ordinary_source(geometry, tags, eta)
    anchor = ARITH._checker_seed_evaluate_seed(context, tuple(inverse_word(seed)))
    require(all(np.array_equal(a, b) for a, b in zip(actual, anchor)), "canary_actual_raw_source_retained_forward_anchor")
    probes, expected = [], REFINE.zero_source()
    moment = np.array([1, 2, 1, 1, 1, 2, 2, 0, 1, 0], dtype=np.uint8)
    for tag in range(6):
        parity = tag % 4
        vertex = ((parity * 27 + 22) * 504 + tag)
        probe = np.zeros(EDGES, dtype=np.uint8); probe[2 * vertex + 1] = 1; probes.append(probe)
        for character, label in enumerate(CHARACTERS):
            weight = 1 if sum(a * b for a, b in zip(context.transport[tag][label], CHARACTERS[parity])) % 2 == 0 else 2
            coefficients = moment * weight % 3
            expected[0].reshape(4, 6, 2, 504)[character, tag, 1, tag] = coefficients[0]
            expected[1].reshape(4, 6, 2, 3, 504)[character, tag, 1, :, tag] = coefficients[1:4]
            expected[2].reshape(4, 6, 2, 6, 504)[character, tag, 1, :, tag] = coefficients[4:]
    expected[3][6:] = [1, 2]
    mixed = ordinary_source(geometry, probes, [1, 2])
    require(all(np.array_equal(a, b) for a, b in zip(mixed, expected)) and
            all(np.any(part[a]) for part in mixed[:3] for a in range(4)), "canary_all_six_tags_four_characters_mixed_degrees_eta")
    augmentation = [probe.copy() for probe in probes]
    for probe in augmentation:
        probe[0] = 1
    require(ordinary_source(geometry, augmentation, [1, 2])[3].tolist() == [1] * 6 + [1, 2], "canary_shared_eight_auxiliary_slots")
    tests = [{"name": "actual-negative-SLP-six-tag-ordinary27-and-mixed-four-character-source", "status": "PASS",
              "raw_letters": stream["letters"], "retained_forward_anchor_only_in_canary": True}]

    records = [{"kind": "old", "owner": 0, "local": 0, "node": 0, "original_lead": 6048, "embedded_lead": 96768},
               {"kind": "old", "owner": 0, "local": 1, "node": 1, "original_lead": 2, "embedded_lead": 2}]
    rows: dict[int, tuple[bytes, bytes | None]] = {}
    row0, row1 = np.zeros(6056, dtype=np.uint8), np.zeros(6056, dtype=np.uint8)
    row0[6048] = 1; row1[2] = 1; row1[6048] = 2
    companion0, companion1 = np.zeros((4, 18144), dtype=np.uint8), np.zeros((4, 18144), dtype=np.uint8)
    companion0[:, 9] = [1, 2, 1, 2]; companion1[:, 10] = 1
    rows[0], rows[1] = (pack(row0), pack(companion0)), (pack(row1), pack(companion1))
    input_source = REFINE.zero_source()
    input_source[0][0, 2] = 1; input_source[3][0] = 1
    input_source[1][:] = (2 * companion0 + companion1) % 3
    coefficients = [2, 1, 1, 2, 1, 2, 1]
    for node, (owner, local, lead) in enumerate(((0, 0, 7), (0, 1, 3), (1, 0, 3), (2, 0, 3), (3, 0, 3)), 2):
        row = np.zeros(18144, dtype=np.uint8); row[lead] = 1
        if node == 3:
            row[7] = 2
        rows[node] = (pack(row), None)
        input_source[1][owner] = (input_source[1][owner] + coefficients[node] * row) % 3
        records.append({"kind": "new", "owner": owner, "local": local, "node": node, "original_lead": lead,
                        "embedded_lead": 24192 + owner * 18144 + lead})
    primal = primal_rows(input_source, records, lambda r: rows[r["node"]])
    require(primal["alpha"].tolist() == coefficients and [r["node"] for r in primal["events"]] == [1, 0, 3, 2, 4, 5, 6],
            "canary_original_leads_differ_from_insertion_ids")
    require(projected_exponents([2, 3], 0) == [8, 12] and projected_exponents([2, 3], 1) == [0, 0] and
            exponent_expression([18, 0], [[0, 2]], [[0, 18]], 2) == [36, 36], "canary_signed_DAG_mod54_scale_once")
    for bad in ([True, 0], [54, 0], [-1, 0], [1.0, 0]):
        rejected(lambda: residue_pair(bad), "residue54-is-not-trit-or-boolean")
    tests.append({"name": "full-original-lead-primal-four-d1-shared-aux-and-residue54", "status": "PASS", "source_lower_trits": SOURCE_LOWER})

    old_row = np.array([1, 0, 0, 0, 2, 0, 0, 0], dtype=np.uint8)
    pivots = [{"offer": 11, "lead": 0, "physical_offset": 0}]
    row_reader = lambda _: pack(old_row)
    raw = np.array([0, 1, 1, 0, 0, 0, 0, 0], dtype=np.uint8)
    old_lambda = np.array([0, 0, 1, 0, 0, 0, 0, 0], dtype=np.uint8)
    unchanged = one_physical_row(raw, old_lambda.copy(), old_lambda, pivots, row_reader, 23, 1)
    linear = one_physical_row(raw, raw.copy(), old_lambda, pivots, row_reader, 23, 1)
    require(unchanged["target_scalar"] == 0 and unchanged["separator"] is not None and np.array_equal(unchanged["target"], old_lambda) and
            linear["terminal"] == "LINEAR_MEMBERSHIP_CANDIDATE" and linear["separator"] is None, "canary_target_scalar_zero_and_linear_candidate")
    toy_start = document("start", {"rank": 1, "generation": 23, "state_head": "1" * 64,
        "target_remainder_sha256": sha(pack(old_lambda)), "lambda_rho2": {"original_rho2_packed_sha256": "2" * 64},
        "accepted_target_derivation_parents": [{"role": "canary-accepted-parent"}]})
    toy_owner, toy_source = document("owner", {}), document("source", {})
    toy_raw = {"selected_scalar": 1, "homogeneous_scalar": 2, "section_scalar": 1, "raw_word": document("raw-word", {})}
    delta = new_delta_records(toy_start, toy_owner, toy_source, {"witness": {"kind": "chord"}, "witness_sha256": "3" * 64},
        toy_raw, document("source-correction", {}), document("p1-roots", {}), document("p1-reductions", {}), unchanged, 1)
    require(set(delta["result.json"]["target"]) == {"parent_remainder_sha256", "remainder_sha256", "scalar"} and
            delta["instruction.json"]["generation"] == 24 and delta["instruction.json"]["offer"] == 23, "canary_dynamic_generation_plain_target")
    payloads = {name: ORACLE.json_payload(value) for name, value in delta.items()}
    payloads["target-remainder.bin"] = ORACLE.typed_array(unchanged["target"], "packed3", (8,))
    with tempfile.TemporaryDirectory(prefix="r07-selected-cycle-checker-") as temporary:
        root = Path(temporary)
        for name, (data, _, _) in payloads.items():
            (root / name).write_bytes(data)
        instruction = delta["instruction.json"]
        # Obtain the exact production manifest/HEAD without bypassing its byte checker.
        files = [{"file": name, "bytes": len(data), "sha256": sha(data), "dtype": dtype, "shape": shape}
                 for name, (data, dtype, shape) in sorted(payloads.items())]
        manifest = document("manifest", {"owner_sha256": sha(canonical(toy_owner)), "start_sha256": sha(canonical(toy_start)),
            "source_sha256": sha(canonical(toy_source)), "result_sha256": sha(payloads["result.json"][0]),
            "instruction_sha256": sha(canonical(instruction)), "parent_state_head": toy_start["state_head"], "state_head": instruction["rolling_sha256"],
            "files": files, "stage_eof": ["raw", "source", "primal", "p1", "B", "physical"], "candidate": True, "cross_checked": False, "verified": False})
        head = document("head", {"owner_sha256": sha(canonical(toy_owner)), "source_sha256": sha(canonical(toy_source)),
            "start_sha256": sha(canonical(toy_start)), "manifest_sha256": sha(canonical(manifest)), "instruction_sha256": sha(canonical(instruction)),
            "parent_state_head": toy_start["state_head"], "state_head": instruction["rolling_sha256"], "rank": 2, "generation": 24,
            "kind": unchanged["kind"], "completed_steps": 1, "physical_sha256": sha(pack(unchanged["normalized"])),
            "target_remainder_sha256": sha(pack(unchanged["target"])), "lambda_sha256": sha(pack(unchanged["lambda"]))})
        (root / "manifest.json").write_bytes(canonical(manifest)); (root / "HEAD").write_bytes(canonical(head))
        finalize_candidate(root, payloads, toy_start, toy_owner, toy_source, unchanged)
        mutated = copy.deepcopy(delta["result.json"]); mutated["target"]["sha256"] = "0" * 64
        (root / "result.json").write_bytes(canonical(mutated))
        rejected(lambda: finalize_candidate(root, payloads, toy_start, toy_owner, toy_source, unchanged), "plain-target-rejects-generic-seal")
        (root / "result.json").write_bytes(payloads["result.json"][0])
        (root / "target-remainder.bin").write_bytes(payloads["target-remainder.bin"][0] + b"\0")
        rejected(lambda: finalize_candidate(root, payloads, toy_start, toy_owner, toy_source, unchanged), "actual-array-trailing-EOF")
    tests.append({"name": "one-row-dynamic-target-zero-plain-target-and-full-EOF", "status": "PASS", "old_numerical_suites": 0})
    return document("selftest", {"status": "PASS", "tests": tests, "cross_checked": False, "verified": False})


def main() -> int:
    global DEADLINE, STARTED
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("state", "delta", "seed34", "packet", "refinement", "prepare", "p1", "task712", "oracle"):
        parser.add_argument("--" + name + "-root", type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    parser.add_argument("--candidate-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-seconds", type=float, default=1800)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--selftest", action="store_true")
    modes.add_argument("--parent-layout-selftest", action="store_true")
    args = parser.parse_args()
    STARTED = time.monotonic()
    require(np.isfinite(args.max_seconds) and args.max_seconds > 0, "positive_finite_resource_limit")
    DEADLINE = STARTED + args.max_seconds
    def interrupted(signum: int, frame: Any) -> None:
        raise ResourceStop("signal-" + str(signum) + ":" + LAST_PHASE)
    signal.signal(signal.SIGINT, interrupted); signal.signal(signal.SIGTERM, interrupted)
    # Existing loaders/physical primitives report progress through this boundary.
    def retained_progress(phase: str, **fields: Any) -> None:
        boundary("retained:" + phase, **fields)
    for module in (ORACLE, REFINE, FIXED, LEGACY, LEGACY.ROOTS, BASE):
        for name in ("boundary", "progress"):
            if hasattr(module, name):
                setattr(module, name, retained_progress)
    exit_code = 0
    try:
        if args.selftest:
            result = selftest()
        else:
            require(all(getattr(args, name + "_root") is not None for name in ("state", "delta", "seed34", "packet", "refinement", "oracle")),
                    "actual_six_saved_parent_roots")
            if args.parent_layout_selftest:
                result = parent_layout_selftest(args)
            else:
                require(args.candidate_root is not None and args.output is not None and len(args.block_root) == 4 and
                        all(getattr(args, name + "_root") is not None for name in ("prepare", "p1", "task712")), "actual_complete_roots_and_report")
                result = check_actual(args)
    except (ResourceStop, ORACLE.ResourceStop, REFINE.ResourceStop):
        result = document("checker-result", {"status": "UNKNOWN_RESOURCE", "terminal": "UNKNOWN_RESOURCE", "phase": LAST_PHASE,
            "completed_stages": COMPLETED_STAGES.copy(), "candidate": False, "cross_checked": False, "verified": False})
        exit_code = 3
    except Exception as error:
        result = document("checker-result", {"status": "FAIL", "reason": type(error).__name__ + ":" + str(error),
            "phase": LAST_PHASE, "completed_stages": COMPLETED_STAGES.copy(), "candidate": False, "cross_checked": False, "verified": False})
        exit_code = 1
    raw = canonical(result)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(raw)
    sys.stdout.buffer.write(raw)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
