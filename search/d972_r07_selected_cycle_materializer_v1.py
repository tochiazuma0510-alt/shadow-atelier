#!/usr/bin/env python3
"""Task965: one accepted v548 witness, one ordered legal source, one row.

No accepted scan or old insertion arithmetic is replayed. All new outputs
are candidates. Exact oracle acceptance pins are required before any run.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import signal
import sys
import tempfile
import time
from typing import Any, Iterable

import numpy as np

SCHEMA = "d972.r07.selected-cycle-materializer.v1"
SEARCH = Path(__file__).resolve().parent
PROJECT = SEARCH.parent
ORACLE_MODULE = "d972_r07_section_cochain_oracle_v1.py"
ORACLE_MODULE_SHA = "4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb"
# Successful checker-only completion; original v1 producer bytes are retained.
ORACLE_ARTIFACT: dict[str, Any] = {
    "run": 33977701313, "attempt": 1,
    "head": "bbce98d8f95a845f36fe89c0f507b9360792666f", "id": 9972829869,
    "name": "d972-r07-section-cochain-checker-completion-v1-candidate-33977701313-1",
    "bytes": 2299772,
    "sha256": "sha256:1a5c8800af563493b95dd4166d20c2fe1b74449f5f7f15aa99278d9b1c1b878d",
}
ORACLE_FILES: dict[str, tuple[int, str]] = {
    "output/manifest.json": (1430, "7df077372a51d12cbf95be5f26c94a5e29ef0f6b118f1ed7efb452ba01942639"),
    "output/start.json": (48377, "7ff970e54dec57512593f5445fed387075d6602bff31f41b7db9f34bab045a2a"),
    "output/owner.json": (8419, "6c71fbc405105bd0722924a308594ba41aea6745725ae85d046ff7409998b322"),
    "output/source.json": (1246, "af1e178d19e4ee427439d102de74a559ed6202ca0a2839212a60748ccfe482ac"),
    "output/result.json": (13727, "c7f65255443a8901fa1b6fbab69e81bbc811014e1eb527e7f671e2f6343ba312"),
    "checker-result.json": (15387, "92739f2db1007ec9ee040716c9dcb26859c10e5a5917a377514bb8e4eb4cd41a"),
    "source-receipt.json": (2673, "cd9a45a389cafd0cfb3813181c1365b0a66cdd682cc737a1a68f27b438d92934"),
    "completion-run-receipt.json": (2089, "3c2eb678db147c7538adf7520f19d91610b255488464704d32a224f9cda4102b"),
    "repair-source-receipt.json": (3204, "2b2efda3b1922e30246621a8b8cf87a277587767ca77662a03b7a35ef821bd37"),
    "preserved-input.json": (10504, "332f6b62aca1042868e65117d4cc9de952ef8d4817d5169ae8a1ee1a9298e625"),
}
ORACLE_SNAPSHOT: dict[str, Any] = {
    "terminal": "VIOLATION_CANDIDATE", "rank": 1385, "generation": 8090,
    "state_head": "8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61",
    "lambda_sha256": "1e720af4a30bac955ab4565366f0242b5c2d43125eb280e241df20976331cdf1",
    "target_remainder_sha256": "111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad",
    "witness_sha256": "1c282b82cbf430b3ef492a325c26ac3c7d2bf9146f15aa76c94744f8477620fd",
}
NORMALIZER_DATA = {"file": "scratchpad/a0_v2_words.json", "bytes": 106133,
    "sha256": "fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612"}
NORMALIZER_ROSTER_SHA = "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a"
NORMALIZER_WORDS = {
    "r_x": (1058, "82fa1ff07d5269e5228fb411b97321b61869791c49133aaa65161f44d16b6f2c"),
    "r_y": (466, "88657577db0338fd5c58f7edeec205c27ce5ff5ddba128b8af403167cb232ac0"),
    "c_x": (9522, "2935d479d5896360e71b66aa95bcb964cdb04d9716f27c06f492034b5ac98abb"),
    "c_y": (4194, "c1f3ebec1ef6c448b854b216f8473e674a67a3b5d3a3059888af016293a1a6dd"),
}
N, EDGES, LOWER, TOP, PHYSICAL, P1_ROWS = 54432, 108864, 96776, 36288, 48384, 8059
OLD_OFFSETS, NEW_OFFSETS = (0, 505, 1008, 1511), (2014, 3523, 5035, 6547)
OLD_RANKS, NEW_RANKS = (505, 503, 503, 503), (1509, 1512, 1512, 1512)
CHARS, ACTORS = ((0, 0), (0, 1), (1, 0), (1, 1)), (1, -1, 2, -2)
ASSURANCE = {"candidate": True, "cross_checked": False, "verified": False}
FORMULA = "v547-literal-repair;v548-primal-section;four-B;one-physical-row"
SCOPE = {"snapshot_count": 1, "physical_appends": 1, "characters": [0, 1, 2, 3],
    "source_tags": 6, "p1_rows": P1_ROWS, "source_lower_trits": LOWER,
    "physical_trits": PHYSICAL, "max_cycles": 6, "full_raw_word_source_replay": True,
    "full_normalized_word_replay": False, "eleven_slot_replay": False}
STARTED = time.monotonic()
DEADLINE: float | None = None
STOP_REQUESTED = False
COMPLETED_STAGES: list[str] = []
LOADED_ORACLE: Any = None
OUTPUT_CREATED = False


class ResourceStop(RuntimeError):
    pass


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    require("schema" not in body and "sha256" not in body, "reserved_seal_fields")
    unsigned = {"schema": SCHEMA + "." + kind, **body}
    return {**unsigned, "sha256": sha(canonical(unsigned))}


def sealed_ok(value: Any, kind: str | None = None) -> bool:
    return isinstance(value, dict) and (kind is None or value.get("schema") == SCHEMA + "." + kind) and \
        value.get("sha256") == sha(canonical({k: v for k, v in value.items() if k != "sha256"}))


def signrep(value: int) -> int:
    require(type(value) is int and value in (0, 1, 2), "trit_signed_representative")
    return (0, 1, -1)[value]


def check_deadline(phase: str) -> None:
    if STOP_REQUESTED or (DEADLINE is not None and time.monotonic() >= DEADLINE):
        raise ResourceStop(phase)


def progress(phase: str, **fields: Any) -> None:
    print(json.dumps({"phase": phase, "elapsed_seconds": round(time.monotonic() - STARTED, 3), **fields},
                     sort_keys=True), file=sys.stderr, flush=True)
    check_deadline(phase)


def own_dependencies() -> Any:
    global LOADED_ORACLE
    path = SEARCH / ORACLE_MODULE
    require(path.is_file() and not path.is_symlink() and sha(path.read_bytes()) == ORACLE_MODULE_SHA,
            "oracle_producer_source_pin")
    spec = importlib.util.spec_from_file_location("selected_cycle_own_oracle", path)
    require(spec is not None and spec.loader is not None, "own_oracle_import_spec")
    oracle = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = oracle
    spec.loader.exec_module(oracle)
    oracle.check_deadline = check_deadline
    LOADED_ORACLE = oracle
    refinement, p2, m, base, descriptors = oracle.own_dependencies()
    m.progress = progress
    return oracle, refinement, p2, m, base, descriptors


def lower_row(parts: Any) -> np.ndarray:
    return np.concatenate((parts[0].reshape(-1), parts[1].reshape(-1), parts[3]))


def free_reduce(word: Iterable[int]) -> tuple[int, ...]:
    result: list[int] = []
    for letter in word:
        require(type(letter) is int and letter in ACTORS, "signed_letter")
        if result and result[-1] == -letter:
            result.pop()
        else:
            result.append(letter)
    return tuple(result)


def inverse_word(word: Iterable[int]) -> tuple[int, ...]:
    return tuple(-letter for letter in reversed(tuple(word)))


def exponent_omega(word: Iterable[int]) -> tuple[int, int, int]:
    a, b, omega = 0, 0, 0
    for letter in word:
        if abs(letter) == 1:
            value = 1 if letter == 1 else -1
            omega = (omega + value * b) % 3
            a += value
        else:
            require(letter in (2, -2), "exponent_letter")
            b += 1 if letter == 2 else -1
    return a, b, omega


def scalar_product(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, omega = left
    c, d, psi = right
    return a + c, b + d, (omega + psi + b * c) % 3


def scalar_power(value: tuple[int, int, int], exponent: int) -> tuple[int, int, int]:
    a, b, omega = value
    require(type(exponent) is int, "ordinary_integer_power")
    return exponent * a, exponent * b, (exponent * omega + exponent * (exponent - 1) // 2 * b * a) % 3


def group_power(value: Any, exponent: int, identity: Any, multiply: Any, invert: Any) -> Any:
    if exponent < 0:
        value, exponent = invert(value), -exponent
    result = identity
    while exponent:
        if exponent & 1:
            result = multiply(result, value)
        exponent >>= 1
        if exponent:
            value = multiply(value, value)
    return result


def q2_value(context: Any, index: int) -> Any:
    require(type(index) is int and 0 <= index < N, "q2_vertex")
    p = index % 504
    kid, parity = (index // 504) % 27, index // (504 * 27)
    return context.psels[p], parity // 2, parity % 2, (kid // 9, (kid // 3) % 3, kid % 3)


def marked_q0(oracle: Any, arith: Any, context: Any) -> Any:
    oracle.validate_marking(arith, context)
    raw = oracle.safe_file(PROJECT, "scratchpad/fuda1_a0_rmax_data.g").read_bytes().decode("ascii")
    match = re.search(r"FUDA1_Q0PERMS\s*:=\s*(\[\s*\[.*?\]\s*,\s*\[.*?\]\s*\])\s*;;", raw, re.S)
    require(match is not None, "q0_literal_marking")
    return tuple(tuple(int(x) - 1 for x in row) for row in json.loads(match.group(1)))


def normalizer_dictionary(oracle: Any) -> Any:
    raw = oracle.read_fixed(PROJECT, NORMALIZER_DATA["file"],
                            (NORMALIZER_DATA["bytes"], NORMALIZER_DATA["sha256"]))
    value = json.loads(raw.decode("ascii"))
    relators = value["raw_q0_relators"]
    require(len(relators) == 19 and sha(canonical(relators)[:-1]) == NORMALIZER_ROSTER_SHA,
            "normalizer_nineteen_word_roster")
    q = [tuple(int(x) for x in word) for word in relators]
    rx = free_reduce(q[0] + inverse_word(q[5]) * 2 + q[6] * 4 + q[8])
    ry = free_reduce(inverse_word(q[7]) + inverse_word(q[3]))
    words = {"r_x": rx, "r_y": ry, "c_x": free_reduce(rx * 9), "c_y": free_reduce(ry * 9)}
    receipts = []
    for name, word in words.items():
        count, digest = NORMALIZER_WORDS[name]
        require(len(word) == count and sha(canonical(list(word))[:-1]) == digest,
                "normalizer_literal_pin:" + name)
        receipts.append({"name": name, "length": count, "word_sha256": digest})
    require(exponent_omega(rx)[:2] == (2, 0) and exponent_omega(ry)[:2] == (0, 2),
            "normalizer_integer_exponents")
    return words, {"dictionary": NORMALIZER_DATA, "raw_relators_sha256": NORMALIZER_ROSTER_SHA,
                   "words": receipts}


class RawSLP:
    def __init__(self, oracle: Any, arith: Any, context: Any, geometry: Any, normalizers: Any):
        self.oracle, self.arith, self.context, self.geometry = oracle, arith, context, geometry
        self.normalizers, self.q0 = normalizers, marked_q0(oracle, arith, context)
        self.nodes: list[dict[str, Any]] = []
        self.records: dict[str, Any] = {}
        self.values: dict[str, Any] = {}
        self.refs: dict[str, tuple[int, ...]] = {}
        self.q0_identity = tuple(range(36))

    def tree_word(self, vertex: int) -> tuple[int, ...]:
        letters: list[int] = []
        while vertex:
            require(len(letters) < N, "tree_reference_acyclic")
            edge, parent = int(self.geometry["parent_edge"][vertex]), int(self.geometry["parent"][vertex])
            require(edge // 2 == parent and int(self.geometry["next"][parent, edge % 2]) == vertex,
                    "tree_reference_edge")
            letters.append(edge % 2 + 1)
            vertex = parent
        return tuple(reversed(letters))

    def literal_value(self, word: tuple[int, ...]) -> Any:
        q0 = self.q0_identity
        inverses = tuple(self.arith._seed_perm_inv(x) for x in self.q0)
        for letter in word:
            image = self.q0[abs(letter) - 1] if letter > 0 else inverses[abs(letter) - 1]
            q0 = self.arith._seed_perm_mul(q0, image)
        return {"scalar": exponent_omega(word), "length": len(word), "q0": q0,
                "q2": self.arith._seed_affine_eval(word, self.context.images)}

    def add(self, node_id: str, operation: str, **fields: Any) -> str:
        require(node_id not in self.records, "slp_unique_node")
        record = {"id": node_id, "op": operation, **fields}
        identity = {"scalar": (0, 0, 0), "length": 0, "q0": self.q0_identity,
                    "q2": self.arith.SEED_AFFINE_IDENTITY}
        if operation == "Identity":
            value = identity
        elif operation == "Letter":
            value = self.literal_value((fields["letter"],))
        elif operation == "Ref":
            if fields["namespace"] == "oracle-tree":
                word = self.tree_word(fields["key"])
            else:
                require(fields["namespace"] == "normalizer-v459" and fields["key"] in ("r_x", "r_y"),
                        "raw_ref_namespace")
                word = self.normalizers[fields["key"]]
            self.refs[node_id] = word
            value = self.literal_value(word)
        elif operation == "OrderedProduct":
            value = identity
            for factor in fields["factors"]:
                right = self.values[factor]
                value = {"scalar": scalar_product(value["scalar"], right["scalar"]),
                    "length": value["length"] + right["length"],
                    "q0": self.arith._seed_perm_mul(value["q0"], right["q0"]),
                    "q2": self.arith._seed_affine_mul(value["q2"], right["q2"])}
        else:
            require(operation in ("Inverse", "IntegerPower"), "raw_slp_operation")
            power = -1 if operation == "Inverse" else fields["exponent"]
            child = self.values[fields["node"]]
            value = {"scalar": scalar_power(child["scalar"], power), "length": abs(power) * child["length"],
                "q0": group_power(child["q0"], power, self.q0_identity,
                    self.arith._seed_perm_mul, self.arith._seed_perm_inv),
                "q2": group_power(child["q2"], power, self.arith.SEED_AFFINE_IDENTITY,
                    self.arith._seed_affine_mul, self.arith._seed_affine_inv)}
        self.nodes.append(record)
        self.records[node_id], self.values[node_id] = record, value
        return node_id

    def letters(self, node_id: str, inverse: bool = False) -> Iterable[int]:
        record = self.records[node_id]
        op = record["op"]
        if op == "Identity":
            return
        if op == "Letter":
            yield -record["letter"] if inverse else record["letter"]
        elif op == "Ref":
            word = self.refs[node_id]
            yield from inverse_word(word) if inverse else word
        elif op == "OrderedProduct":
            factors = reversed(record["factors"]) if inverse else record["factors"]
            for factor in factors:
                yield from self.letters(factor, inverse)
        elif op == "Inverse":
            yield from self.letters(record["node"], not inverse)
        else:
            require(op == "IntegerPower", "raw_emit_operation")
            exponent = -record["exponent"] if inverse else record["exponent"]
            for _ in range(abs(exponent)):
                yield from self.letters(record["node"], exponent < 0)

    def node_receipts(self) -> Any:
        return [{"id": record["id"], "exponent": list(self.values[record["id"]]["scalar"][:2]),
            "omega": self.values[record["id"]]["scalar"][2], "length": self.values[record["id"]]["length"],
            "q0": list(self.values[record["id"]]["q0"]),
            "q2": self.oracle.qid(self.context, self.values[record["id"]]["q2"])} for record in self.nodes]


def word_fox(slp: RawSLP, node_id: str, *, substitution: Any = None) -> tuple[Any, Any, Any]:
    digest, count, a, b, omega = hashlib.sha256(), 0, 0, 0, 0

    def stream() -> Iterable[int]:
        nonlocal count, a, b, omega
        for letter in slp.letters(node_id):
            emitted = (letter,) if substitution is None else \
                (tuple(substitution[letter - 1]) if letter > 0 else inverse_word(substitution[-letter - 1]))
            for item in emitted:
                digest.update(bytes((item & 255,)))
                count += 1
                if abs(item) == 1:
                    coefficient = 1 if item == 1 else -1
                    omega = (omega + coefficient * b) % 3
                    a += coefficient
                else:
                    b += 1 if item == 2 else -1
                if count % 4096 == 0:
                    check_deadline("raw-slp-fox-stream")
                yield item
    gradient, endpoint = slp.arith._seed_affine_fox(stream(), slp.context.images)
    chain = np.zeros((N, 2), dtype=np.uint8)
    for (component, vertex), coefficient in gradient.items():
        chain[slp.oracle.qid(slp.context, vertex), component] = coefficient
    if substitution is None:
        expected = slp.values[node_id]
        require(count == expected["length"] and (a, b, omega) == expected["scalar"] and
                endpoint == expected["q2"], "same_raw_slp_stream_metadata")
    check_deadline("raw-slp-fox-eof")
    return chain.reshape(-1), endpoint, {"encoding": "signed-byte:1=01,-1=ff,2=02,-2=fe",
        "bytes": count, "letters": count, "sha256": digest.hexdigest(), "full_eof": True}


def witness_chain(geometry: Any, witness: Any) -> np.ndarray:
    chain = np.zeros(EDGES, dtype=np.int32)
    for item in witness["cycles"]:
        edge, coefficient = item["edge"], signrep(item["coefficient"])
        require(type(edge) is int and edge in geometry["chord_set"], "witness_actual_chord")
        tail, slot = divmod(edge, 2)
        head = int(geometry["next"][tail, slot])
        chain[edge] += coefficient
        for vertex, weight in ((tail, coefficient), (head, -coefficient)):
            visited = 0
            while vertex:
                parent_edge = int(geometry["parent_edge"][vertex])
                chain[parent_edge] += weight
                vertex = int(geometry["parent"][vertex])
                visited += 1
                require(visited < N, "witness_tree_acyclic")
    return (chain % 3).astype(np.uint8)


def selected_raw_word(oracle: Any, arith: Any, context: Any, accepted: Any) -> Any:
    geometry, witness = accepted["geometry"], accepted["witness"]
    words, normalizers = normalizer_dictionary(oracle)
    slp = RawSLP(oracle, arith, context, geometry, words)
    slp.add("identity", "Identity")
    slp.add("x", "Letter", letter=1)
    slp.add("y", "Letter", letter=2)
    factors = []
    for index, item in enumerate(witness["cycles"]):
        edge, coefficient = item["edge"], signrep(item["coefficient"])
        tail, slot = divmod(edge, 2)
        head = int(geometry["next"][tail, slot])
        suffix = str(index)
        slp.add("tail-" + suffix, "Ref", namespace="oracle-tree", key=tail)
        slp.add("head-" + suffix, "Ref", namespace="oracle-tree", key=head)
        slp.add("head-inverse-" + suffix, "Inverse", node="head-" + suffix)
        slp.add("cycle-" + suffix, "OrderedProduct",
                factors=["tail-" + suffix, ("x", "y")[slot], "head-inverse-" + suffix])
        factors.append(slp.add("cycle-power-" + suffix, "IntegerPower",
                                node="cycle-" + suffix, exponent=coefficient))
    slp.add("w", "OrderedProduct", factors=factors)
    slp.add("r-x", "Ref", namespace="normalizer-v459", key="r_x")
    slp.add("r-y", "Ref", namespace="normalizer-v459", key="r_y")
    slp.add("r-x-cube", "IntegerPower", node="r-x", exponent=3)
    slp.add("r-y-cube", "IntegerPower", node="r-y", exponent=3)
    slp.add("r-x-inverse", "Inverse", node="r-x")
    slp.add("r-y-inverse", "Inverse", node="r-y")
    slp.add("commutator", "OrderedProduct", factors=["r-x-inverse", "r-y-inverse", "r-x", "r-y"])
    require(slp.values["r-x"]["q0"] == slp.values["r-y"]["q0"] == slp.q0_identity,
            "actual_normalizer_q0_identity")
    a, b, omega = slp.values["w"]["scalar"]
    if witness["kind"] == "chord":
        require(len(witness["cycles"]) == 6 and slp.values["w"]["q0"] == slp.q0_identity and
                a % 6 == b % 6 == 0, "legal_chord_integer_six_divisibility")
        slp.add("repair-x", "IntegerPower", node="r-x-cube", exponent=-a // 6)
        slp.add("repair-y", "IntegerPower", node="r-y-cube", exponent=-b // 6)
        slp.add("repair-central", "IntegerPower", node="commutator", exponent=signrep(omega))
        slp.add("raw-root", "OrderedProduct", factors=["w", "repair-x", "repair-y", "repair-central"])
        method = "v547-three-factor"
    else:
        require(witness["kind"] == "auxiliary" and witness["coordinate"] in (0, 1) and
                witness["cycles"] == [], "selected_auxiliary_type")
        slp.add("raw-root", "IntegerPower", node=("r-x", "r-y")[witness["coordinate"]], exponent=9)
        method = "v459-ninth-power"
    for node in ("r-x-cube", "r-y-cube", "commutator"):
        check, endpoint, _ = word_fox(slp, node)
        require(not np.any(check) and endpoint == arith.SEED_AFFINE_IDENTITY,
                "literal_normalizer_q2_fox_zero")
    chain, endpoint, stream = word_fox(slp, "raw-root")
    expected_chain = witness_chain(geometry, witness)
    require(np.array_equal(chain, expected_chain), "raw_root_same_witness_chain")
    root = slp.values["raw-root"]
    a0, b0, omega0 = root["scalar"]
    require(root["q0"] == slp.q0_identity and endpoint == arith.SEED_AFFINE_IDENTITY and
            a0 % 18 == b0 % 18 == 0 and omega0 == 0, "raw_root_legal_endpoint_exponent")
    eta = [a0 // 18 % 3, b0 // 18 % 3]
    require(eta == witness["eta"] and (method != "v547-three-factor" or (a0, b0) == (0, 0)),
            "raw_root_same_normalized_eta")
    tau = (chain.astype(np.uint64) @ geometry["carry"].astype(np.uint64) % 3).astype(np.uint8)
    boundary = np.zeros(N, dtype=np.int32)
    for slot in range(2):
        weights = chain.reshape(N, 2)[:, slot].astype(np.int32)
        boundary -= weights
        np.add.at(boundary, geometry["next"][:, slot], weights)
    require(not np.any(boundary % 3) and not np.any(tau) and witness["tau"] == tau.tolist(),
            "raw_chain_boundary_and_five_carry")
    value = (oracle.dot(chain, accepted["f"]) + oracle.dot(np.asarray(eta), accepted["b_aux"])) % 3
    require(value == witness["scalar"] and value in (1, 2), "raw_witness_scalar")
    depths = np.zeros(N, dtype=np.uint32)
    for vertex0 in geometry["order"][1:]:
        vertex = int(vertex0)
        depths[vertex] = depths[int(geometry["parent"][vertex])] + 1
    height = int(np.max(depths))
    require(height < N, "tree_height_bound")
    l0 = slp.values["w"]["length"]
    bound = (l0 + 3 * abs(a // 6) * len(words["r_x"]) + 3 * abs(b // 6) * len(words["r_y"]) +
             2 * abs(signrep(omega)) * (len(words["r_x"]) + len(words["r_y"]))) \
        if method == "v547-three-factor" else len(words[("c_x", "c_y")[witness["coordinate"]]])
    require(l0 <= 6 * (2 * height + 1) and root["length"] <= bound,
            "selected_raw_word_integer_length_bound")
    record = seal("raw-word", {"grammar": "ordered-slp-v1", "nodes": slp.nodes, "root": "raw-root",
        "cycles": witness["cycles"], "eta": eta, "node_values": slp.node_receipts(),
        "normalizers": normalizers, "geometry_manifest_sha256": accepted["stages"]["geometry"],
        "witness_sha256": accepted["layout"]["witness_sha256"],
        "word_bound": {"tree_height": height, "unrepaired": l0, "normalized": bound,
                       "actual_slp_length": root["length"]}, "word_stream": stream,
        "legality": {"method": method, "q0_identity": True, "q2_identity": True, "tau": tau.tolist(),
            "epsilon_divisible18": True, "normalized_pair": eta, "omega": omega0,
            "epsilon_exact_zero": (a0, b0) == (0, 0), "omega_zero": True,
            "delta_endpoint_mode": "v547-retained-Gamma0-readout" if method == "v547-three-factor" else
                "v459-retained-expGamma9", "actual_delta_enumerated": False,
            "normalizer_Q2_Fox_zero": True, "raw_chain_matches_witness": True}})
    progress("raw-selected-word", letters=stream["letters"], chain_support=int(np.count_nonzero(chain)))
    return {"slp": slp, "record": record, "chain": chain, "eta": eta}


def source_from_chain(oracle: Any, refinement: Any, m: Any, arith: Any, context: Any,
                      accepted: Any, raw: Any) -> Any:
    geometry = accepted["geometry"]
    parts = refinement.empty_lift(m)
    base_chain = raw["chain"].reshape(N, 2)
    maps = oracle.RightMaps(arith, context)
    polynomial = np.asarray([arith._seed_e_poly((kid // 9, (kid // 3) % 3, kid % 3))
                             for kid in range(27)], dtype=np.int32)
    receipts = []
    for tag, words in enumerate(arith.SEED_OO):
        gradient = np.zeros((N, 2), dtype=np.int32)
        for slot in range(2):
            selected = np.flatnonzero(base_chain[:, slot])
            for component, prefix, coefficient in geometry["tags"][tag]["fox"][slot]:
                destinations = maps.at(q2_value(context, prefix))[geometry["phi"][tag, selected]]
                np.add.at(gradient[:, component], destinations,
                          int(coefficient) * base_chain[selected, slot].astype(np.int32))
        gradient = (gradient % 3).astype(np.uint8)
        direct, endpoint, _ = word_fox(raw["slp"], "raw-root", substitution=words)
        require(endpoint == arith.SEED_AFFINE_IDENTITY and np.array_equal(direct, gradient.reshape(-1)),
                "same_raw_slp_all_tag_fox:" + str(tag))
        normal = np.zeros((N, 2), dtype=np.int32)
        np.add.at(normal[:, 0], geometry["next"][:, 0], -gradient[:, 0].astype(np.int32))
        np.add.at(normal[:, 1], geometry["prev"][:, 1], -gradient[:, 0].astype(np.int32))
        normal[:, 1] += gradient[:, 1].astype(np.int32)
        normal %= 3
        parts[3][tag] = int(np.sum(gradient[:, 0], dtype=np.uint64) % 3)
        for component in range(2):
            positions = np.flatnonzero(normal[:, component])
            psl, kid, parity = positions % 504, (positions // 504) % 27, positions // (504 * 27)
            for character, label in enumerate(CHARS):
                cv = np.asarray([arith._seed_cv(context.transport[tag][label], value) for value in CHARS], dtype=np.int32)
                weight = normal[positions, component] * cv[parity]
                group = tag * 2 + component
                values = np.zeros(504, dtype=np.int64)
                np.add.at(values, psl, weight)
                parts[0][character, group * 504:(group + 1) * 504] = values % 3
                for mono in range(3):
                    begin = (group * 3 + mono) * 504
                    # Accumulate in signed integer scratch, not uint8 wraparound.
                    values = np.zeros(504, dtype=np.int64)
                    np.add.at(values, psl, weight * polynomial[kid, 1 + mono])
                    parts[1][character, begin:begin + 504] = values % 3
                for mono in range(6):
                    begin = (group * 6 + mono) * 504
                    values = np.zeros(504, dtype=np.int64)
                    np.add.at(values, psl, weight * polynomial[kid, 4 + mono])
                    parts[2][character, begin:begin + 504] = values % 3
        receipts.append({"tag": tag, "raw_fox_sha256": sha(oracle.pack(gradient.reshape(-1))),
                         "direct_fox_same": True, "q2_endpoint": 0})
        progress("raw-six-tag-source", tags=tag + 1, total=6)
    parts[3][6:] = raw["eta"]
    homogeneous = sum(oracle.dot(accepted["q"][a], parts[2][a]) for a in range(4)) % 3
    section = oracle.dot(accepted["kappa"], lower_row(parts))
    require((homogeneous - section) % 3 == accepted["witness"]["scalar"], "same_raw_source_oracle_scalar")
    record = seal("raw-source", {"method": "raw-Q2-Fox-and-six-tag-direct-SLP",
        "components": refinement.component_receipts(m, parts), "raw_word_sha256": sha(canonical(raw["record"])),
        "chain_sha256": sha(oracle.pack(raw["chain"])), "eta": raw["eta"], "tag_chain_receipts": receipts,
        "source_lower_sha256": sha(oracle.pack(lower_row(parts))), "source_full_top_sha256": sha(oracle.pack(parts[2])),
        "homogeneous_scalar": homogeneous, "section_scalar": section,
        "witness_scalar": accepted["witness"]["scalar"], "direct_raw_word_replay": True,
        "full_tag_eof": True, "eleven_slot_replay": False})
    return {"parts": parts, "record": record, "homogeneous": homogeneous, "section": section}


def signed_pair_product(raw: tuple[int, int], reductions: Any, base: int,
                        pairs: list[Any], scale: int) -> tuple[int, int]:
    a, b = raw
    for local, coefficient in reductions:
        prior = pairs[base + local]
        require(prior is not None, "integer_prior_p1_reference")
        power = -signrep(coefficient)
        a, b = a + power * prior[0], b + power * prior[1]
    power = signrep(scale)
    require(power != 0, "integer_normalized_scale")
    return power * a % 54, power * b % 54


def p1_metadata_join(node: Any, global_id: int, index: Any) -> None:
    reference = index["references"][global_id]
    require(sha(canonical(node["origin"])) == reference["origin_sha256"] and
            sha(canonical(node["reductions"])) == reference["reductions_sha256"] and
            node["scale"] == reference["scale"], "integer_dag_same_canonical_instruction")


def basis_segments(oracle: Any, base: Any, task554: Any, p1: Any, index: Any,
                   words: Any) -> Any:
    pairs: list[Any] = [None] * P1_ROWS
    segments, defect_pairs = [], []
    seed_pairs = [exponent_omega(tuple(word))[:2] for word in words["relators"]]

    def projected(value: tuple[int, int], character: int) -> tuple[int, int]:
        coefficient = sum(signrep(base.ARITH._seed_cv(CHARS[character], label)) for label in CHARS)
        return coefficient * value[0] % 54, coefficient * value[1] % 54

    prepare = base._state_descriptor(task554["prepare"], -1, need_blobs=True)
    for owner, old in enumerate(prepare["body"]["old_blocks"]):
        nodes = old["record"]["dag_nodes"]
        require(len(nodes) == OLD_RANKS[owner], "integer_old_rows")
        for local, node in enumerate(nodes):
            global_id = OLD_OFFSETS[owner] + local
            p1_metadata_join(node, global_id, index)
            origin = node["origin"]
            if origin["kind"] == "projected_seed":
                raw_pair = projected(seed_pairs[origin["seed"] - 1], owner)
            else:
                require(origin["kind"] == "actor" and 0 <= origin["parent"] < local and
                        origin["letter"] in ACTORS, "integer_old_actor")
                raw_pair = pairs[OLD_OFFSETS[owner] + origin["parent"]]
            pairs[global_id] = signed_pair_product(raw_pair, node["reductions"],
                                                    OLD_OFFSETS[owner], pairs, node["scale"])
        segments.append({"kind": "old", "owner": owner, "start": OLD_OFFSETS[owner],
            "rows": OLD_RANKS[owner], "root": prepare["root"], "body_sha256": prepare["body_sha256"],
            "leads": [node["lead"] for node in nodes],
            "lower_descriptor": copy.deepcopy(old["lower_basis_blob"]),
            "grade_descriptor": copy.deepcopy(old["lifted_grade_blob"])})
    for origin in prepare["body"]["defect_origins"]:
        owner = origin["lower_character"]
        record = prepare["body"]["old_blocks"][owner]["record"]
        if origin["kind"] == "seed":
            raw_pair = projected(seed_pairs[origin["seed"] - 1], owner)
            reductions = record["seed_reductions"][origin["seed"] - 1]
        else:
            require(origin["kind"] == "transition", "integer_old_defect_origin")
            raw_pair = pairs[OLD_OFFSETS[owner] + origin["pivot"]]
            reductions = record["actor_transitions"][origin["pivot"]][ACTORS.index(origin["letter"])]
        defect_pairs.append(signed_pair_product(raw_pair, reductions, OLD_OFFSETS[owner], pairs, 1))
    del nodes, old, record, prepare
    progress("primal-parent-body", bodies=1)
    for owner in range(4):
        block = base._state_descriptor(task554["blocks"][owner], owner, need_blobs=True)
        nodes = block["body"]["dag_nodes"]
        require(len(nodes) == NEW_RANKS[owner] and
                [node["lead"] for node in nodes] == block["body"]["pivot_leads"], "integer_new_rows")
        for local, node in enumerate(nodes):
            global_id = NEW_OFFSETS[owner] + local
            p1_metadata_join(node, global_id, index)
            origin = node["origin"]
            if origin["kind"] == "defect":
                raw_pair = projected(defect_pairs[origin["origin"]], owner)
            else:
                require(origin["kind"] == "actor" and 0 <= origin["parent"] < local and
                        origin["letter"] in ACTORS, "integer_new_actor")
                raw_pair = pairs[NEW_OFFSETS[owner] + origin["parent"]]
            pairs[global_id] = signed_pair_product(raw_pair, node["reductions"], NEW_OFFSETS[owner], pairs, node["scale"])
        segments.append({"kind": "new", "owner": owner, "start": NEW_OFFSETS[owner],
            "rows": NEW_RANKS[owner], "root": block["root"], "body_sha256": block["body_sha256"],
            "leads": list(block["body"]["pivot_leads"]),
            "basis_descriptor": copy.deepcopy(block["body"]["basis_blob"])})
        del nodes, block
        progress("primal-parent-body", bodies=owner + 2)
    require(all(pair is not None and len(pair) == 2 and
                all(type(value) is int and 0 <= value < 54 for value in pair) for pair in pairs),
            "all_canonical_residue54_pairs")
    exponents = seal("p1-exponent-residues", {"rows": P1_ROWS, "order": "canonical-row-id", "modulus": 54,
        "pairs": [list(pair) for pair in pairs], "p1_manifest_sha256": p1["manifest_sha256"],
        "instruction_sha256": p1["instruction"]["sha256"], "method": "ordered-signed-DAG-exponent-mod54", "eof": True})
    return segments, pairs, exponents


def primal_section(oracle: Any, m: Any, segments: Any, parts: Any) -> Any:
    work = tuple(part.copy() for part in parts)
    alpha = np.zeros(P1_ROWS, dtype=np.uint8)
    events = []
    readers = {}
    try:
        for segment in segments:
            descriptors = (("lower", segment["lower_descriptor"]), ("grade", segment["grade_descriptor"])) \
                if segment["kind"] == "old" else (("basis", segment["basis_descriptor"]),)
            for role, descriptor in descriptors:
                readers[(segment["kind"], segment["owner"], role)] = oracle.PackedRows(segment["root"], descriptor)
        old_order = []
        for segment in segments[:4]:
            owner = segment["owner"]
            for local, lead in enumerate(segment["leads"]):
                embedded = owner * 6048 + lead if lead < 6048 else 96768 + lead - 6048
                old_order.append((embedded, owner, local, lead))
        require(len({item[0] for item in old_order}) == 2014, "primal_unique_old_embedded_leads")
        for done, (embedded, owner, local, lead) in enumerate(sorted(old_order), 1):
            lower = readers[("old", owner, "lower")].row(local)
            grade = readers[("old", owner, "grade")].row(local)
            require(lower[lead] == 1 and not np.any(lower[:lead]), "primal_old_normalized_original_lead")
            coefficient = consume_source_row(m, work, "old", owner, lead, lower, grade)
            if coefficient:
                node = OLD_OFFSETS[owner] + local
                alpha[node] = coefficient
                events.append({"event": len(events), "kind": "old", "owner": owner, "local": local,
                    "node": node, "original_lead": lead, "embedded_lead": embedded, "coefficient": coefficient,
                    "literal_exponent": -signrep(coefficient), "row_offset": local * 1514,
                    "row_sha256": sha(oracle.pack(lower)), "companion_offset": local * 18144,
                    "companion_sha256": sha(oracle.pack(grade))})
            if done % 256 == 0 or done == 2014:
                progress("primal-old", rows=done, total=2014)
        require(not np.any(work[0]) and not np.any(work[3]), "primal_all_old_d0_and_shared_aux_zero")
        for owner, segment in enumerate(segments[4:]):
            leads = segment["leads"]
            require(len(set(leads)) == NEW_RANKS[owner], "primal_unique_new_leads")
            for local in sorted(range(len(leads)), key=lambda i: leads[i]):
                lead = leads[local]
                row = readers[("new", owner, "basis")].row(local)
                require(row[lead] == 1 and not np.any(row[:lead]), "primal_new_normalized_original_lead")
                coefficient = consume_source_row(m, work, "new", owner, lead, row)
                if coefficient:
                    node = NEW_OFFSETS[owner] + local
                    alpha[node] = coefficient
                    events.append({"event": len(events), "kind": "new", "owner": owner, "local": local,
                        "node": node, "original_lead": lead, "embedded_lead": 24192 + owner * 18144 + lead,
                        "coefficient": coefficient, "literal_exponent": -signrep(coefficient),
                        "row_offset": local * 4536, "row_sha256": sha(oracle.pack(row)),
                        "companion_offset": None, "companion_sha256": None})
            require(not np.any(work[1][owner]), "primal_new_owner_zero")
            progress("primal-new", owner=owner, rows=len(leads))
    finally:
        for reader in readers.values():
            reader.close()
    lower = lower_row(work)
    require(lower.size == LOWER and not np.any(lower), "primal_full_96776_zero")
    record = seal("p1-reductions", {
        "order": "old-global-ascending-embedded-original-lead;new-owner-major-ascending-original-lead",
        "rows": P1_ROWS, "events": events, "coefficients_sha256": sha(alpha.tobytes()),
        "lower_zero": {"trits": LOWER, "packed_sha256": sha(oracle.pack(lower))}, "eof": True})
    return {"alpha": alpha, "events": events, "lower": lower, "record": record}


def consume_source_row(m: Any, work: Any, kind: str, owner: int, lead: int,
                       row: np.ndarray, companion: np.ndarray | None = None) -> int:
    if kind == "old":
        coefficient = int(work[0][owner, lead] if lead < 6048 else work[3][lead - 6048])
        require(companion is not None and companion.size == 72576, "old_full_four_companion")
        if coefficient:
            m.add_scaled(work[0][owner], row[:6048], 3 - coefficient)
            m.add_scaled(work[3], row[6048:], 3 - coefficient)
            m.add_scaled(work[1], companion.reshape(4, 18144), 3 - coefficient)
    else:
        require(kind == "new" and companion is None, "new_d1_only_row")
        coefficient = int(work[1][owner, lead])
        if coefficient:
            m.add_scaled(work[1][owner], row, 3 - coefficient)
    return coefficient


def validate_plain_target(value: Any, parent: str, child: str, scalar: int) -> None:
    require(isinstance(value, dict) and set(value) == {"parent_remainder_sha256", "remainder_sha256", "scalar"} and
            value["parent_remainder_sha256"] == parent and value["remainder_sha256"] == child and
            type(value["scalar"]) is int and value["scalar"] == scalar and scalar in (0, 1, 2), "plain_target_delta")


def corrected_source(oracle: Any, refinement: Any, m: Any, p1: Any, index: Any, segments: Any,
                     pairs: Any, raw: Any, source: Any, primal: Any) -> Any:
    parts = tuple(part.copy() for part in source["parts"])
    selected = {int(i) for i in np.flatnonzero(primal["alpha"])}
    components = refinement.subtract_lifts(m, p1, index, segments, primal["alpha"], selected, parts)
    require(np.array_equal(lower_row(parts), primal["lower"]), "primal_source_reconstruction_full_lower")
    instruction = oracle.safe_file(p1["root"], p1["instruction"]["path"])
    require(oracle.file_pin(instruction) == {"bytes": p1["instruction"]["bytes"],
                                            "sha256": p1["instruction"]["sha256"]}, "p1_instruction_full_pin")
    component_map = {item["node"]: item["components"] for item in components}
    roots = []
    with instruction.open("rb", buffering=1 << 20) as stream:
        for node in sorted(selected):
            reference = index["references"][node]
            stream.seek(reference["instruction_offset"])
            line = stream.read(reference["instruction_length"])
            require(sha(line) == reference["instruction_sha256"], "selected_p1_positioned_instruction")
            record = json.loads(line.decode("ascii"))
            require(canonical(record) == line and record["node"] == node and
                    record["p1_sha256"] == reference["p1_sha256"] and
                    record["ancestry_sha256"] == reference["ancestry_sha256"] and
                    record["row_receipt"]["sha256"] == reference["row_sha256"], "selected_p1_typed_reference")
            p1_metadata_join(record, node, index)
            roots.append({**reference, "lift_components": component_map[node]})
    root_record = seal("p1-roots", {"p1_manifest_sha256": p1["manifest_sha256"],
        "instruction_sha256": p1["instruction"]["sha256"], "cache_sha256": p1["cache"]["sha256"],
        "canonical_index_sha256": sha(canonical(index)), "roots": roots, "all_references_authenticated": True})
    a, b = raw["slp"].values["raw-root"]["scalar"][:2]
    factors = []
    for event in primal["events"]:
        node, power = event["node"], event["literal_exponent"]
        a, b = (a + power * pairs[node][0]) % 54, (b + power * pairs[node][1]) % 54
        factors.append({"event": event["event"], "node": node, "coefficient": event["coefficient"],
                        "literal_exponent": power, "p1_sha256": index["references"][node]["p1_sha256"]})
    a, b = a % 54, b % 54
    require(a in (0, 18, 36) and b in (0, 18, 36), "corrected_word_integral_normalized_pair")
    normalized_pair = [a // 18 % 3, b // 18 % 3]
    require(normalized_pair == [0, 0] and normalized_pair == parts[3][6:].tolist(),
            "corrected_word_same_source_eta")
    record = seal("source-correction", {"operation": "ordered-product",
        "raw_word_sha256": sha(canonical(raw["record"])), "p1_factor_order": "event-ascending",
        "p1_factors": factors, "p1_roots_sha256": sha(canonical(root_record)),
        "coefficients_sha256": sha(primal["alpha"].tobytes()), "exponent_residue_mod54": [a, b],
        "normalized_pair": normalized_pair, "components": refinement.component_receipts(m, parts),
        "source_lower_zero": {"trits": LOWER, "packed_sha256": sha(oracle.pack(lower_row(parts)))},
        "source_lower_equality": True, "top_characters": [0, 1, 2, 3], "whole_word_direct_replay": False,
        "canonical_p1_source_replay": True, "eleven_slot_replay": False})
    progress("p1-source-correction", alpha_support=len(selected), references=len(roots))
    return {"parts": parts, "roots": root_record, "record": record}


def four_B(oracle: Any, m: Any, tables: Any, state: Any, accepted: Any, corrected: Any) -> Any:
    parts = corrected["parts"]
    require(not np.any(lower_row(parts)), "four_B_source_lower_zero_gate")
    by_character = np.asarray([m.apply_sparse(table["forward"]["B"], TOP, PHYSICAL, parts[2][a])
                               for a, table in enumerate(tables)], dtype=np.uint8)
    raw = (np.sum(by_character, axis=0, dtype=np.uint32) % 3).astype(np.uint8)
    corrected_scalar = sum(oracle.dot(accepted["q"][a], parts[2][a]) for a in range(4)) % 3
    scalar = oracle.dot(state["lambda"], raw)
    require(scalar == corrected_scalar == accepted["witness"]["scalar"] and scalar in (1, 2),
            "all_four_B_same_witness_scalar")
    progress("four-B", physical_support=int(np.count_nonzero(raw)), scalar=scalar)
    return {"by_character": by_character, "raw": oracle.pack(raw),
            "corrected_scalar": corrected_scalar, "physical_scalar": scalar}


def fresh_separator(oracle: Any, m: Any, state: Any, normalized: bytes, lead: int,
                    target: bytes, target_derivation: Any) -> Any:
    free = m.first_nonzero(target, PHYSICAL)
    require(free is not None and free[0] not in set(state["leads"]) | {lead}, "one_row_free_coordinate")
    functional = np.zeros(PHYSICAL, dtype=np.uint8)
    functional[free[0]] = free[1]
    all_rows, records = [*state["rows"], normalized], [*state["records"], {"lead": lead, "offer": state["generation"]}]
    for done, (record, raw) in enumerate(zip(reversed(records), reversed(all_rows)), 1):
        row, coordinate = oracle.unpack(raw, PHYSICAL), record["lead"]
        require(row[coordinate] == 1 and functional[coordinate] == 0, "one_row_reverse_normalized_pivot")
        functional[coordinate] = (-oracle.dot(row, functional)) % 3
        require(oracle.dot(row, functional) == 0, "one_row_reverse_equation")
        if done % 256 == 0 or done == len(all_rows):
            progress("one-row-fresh-separator", rows=done, total=len(all_rows))
    direct = m.check_final_separator(functional, all_rows, state["target_raw"], target)
    raw_lambda = oracle.pack(functional)
    return {"free_coordinate": free[0], "free_value": free[1], "lambda_sha256": sha(raw_lambda),
        "direct_pairing": direct, "lambda_rho2": {"mode": "derived", "value": 1,
            "original_rho2_directly_read": False, "target_derivation": target_derivation,
            "new_target_steps_executed": 1}}, raw_lambda


def one_physical_row(oracle: Any, m: Any, state: Any, start: Any, owner: Any, source_pin: Any,
                     accepted: Any, raw: Any, source: Any, primal: Any, corrected: Any, physical: Any) -> Any:
    remainder, reductions = m.physical_reduce(physical["raw"], state["records"], state["rows"])
    remainder_scalar = oracle.dot(state["lambda"], oracle.unpack(remainder, PHYSICAL))
    require(remainder_scalar == physical["physical_scalar"] and remainder_scalar in (1, 2),
            "one_row_residual_old_lambda_nonzero")
    normalized, lead, sigma = m.normalize_pivot(remainder, state["leads"])
    target, target_scalar = m.update_target(state["target_raw"], normalized, lead, state["leads"])
    target_body = {"parent_remainder_sha256": sha(state["target_raw"]),
                   "remainder_sha256": sha(target), "scalar": target_scalar}
    validate_plain_target(target_body, sha(state["target_raw"]), sha(target), target_scalar)
    literal = seal("physical-literal", {"operation": "scaled-ordered-product",
        "source_correction_sha256": sha(canonical(corrected["record"])), "accepted_physical_head": state["head"],
        "physical_factors": [{**item, "literal_exponent": -signrep(item["scalar"])} for item in reductions],
        "sigma": sigma, "literal_outer_exponent": signrep(sigma), "source_lower_zero": "NOT_ASSERTED",
        "physical_lower_zero": True, "physical_normalized_sha256": sha(normalized),
        "whole_word_direct_replay": False, "eleven_slot_replay": False, "target_word_direct_replay": False})
    instruction = {"schema": SCHEMA + ".instruction", "predecessor": state["head"],
        "offer": state["generation"], "rank": state["rank"] + 1, "generation": state["generation"] + 1,
        "physical_offset": state["rank"] * 12096,
        "origin": {"kind": "v548-cycle" if accepted["witness"]["kind"] == "chord" else "v548-aux",
            "oracle_manifest_sha256": accepted["layout"]["manifest_sha256"],
            "witness_sha256": accepted["layout"]["witness_sha256"], "raw_word_sha256": sha(canonical(raw["record"]))},
        "source_correction_sha256": sha(canonical(corrected["record"])),
        "physical_literal_sha256": sha(canonical(literal)), "p1_roots_sha256": sha(canonical(corrected["roots"])),
        "p1_reductions_sha256": sha(canonical(primal["record"])), "physical_reductions": reductions,
        "lead": lead, "sigma": sigma, "physical_sha256": sha(normalized),
        "selected_scalar": accepted["witness"]["scalar"], "target_scalar": target_scalar,
        "target_remainder_sha256": sha(target)}
    instruction["rolling_sha256"] = sha(bytes.fromhex(state["head"]) + canonical(instruction))
    target_derivation = {"mode": "derived", "original_rho2_directly_read": False,
        "original_rho2_packed_sha256": start["lambda_rho2"]["original_rho2_packed_sha256"],
        "accepted_target_derivation_parents": start["accepted_target_derivation_parents"],
        "new_delta": {"instruction_sha256": sha(canonical(instruction)),
            "state_head": instruction["rolling_sha256"], "normalized_sha256": sha(normalized),
            "target_sha256": sha(canonical(target_body))},
        "identity": "parent_remainder - new_remainder = target.scalar * new_normalized_row"}
    if m.first_nonzero(target, PHYSICAL) is None:
        terminal, kind, separator, raw_lambda = "LINEAR_MEMBERSHIP_CANDIDATE", "LinearMembershipCandidate", None, None
    else:
        terminal, kind = "PIVOT_CANDIDATE", "Separator"
        separator, raw_lambda = fresh_separator(oracle, m, state, normalized, lead, target, target_derivation)
    result = seal("result", {"status": "PASS", "terminal": terminal, "kind": kind,
        "owner_sha256": sha(canonical(owner)), "start_sha256": sha(canonical(start)),
        "source_sha256": sha(canonical(source_pin)), "parent_state_head": state["head"],
        "state_head": instruction["rolling_sha256"], "rank_before": state["rank"], "rank_after": state["rank"] + 1,
        "generation_before": state["generation"], "generation_after": state["generation"] + 1,
        "selected_scalar": accepted["witness"]["scalar"], "homogeneous_scalar": source["homogeneous"],
        "section_scalar": source["section"], "corrected_scalar": physical["corrected_scalar"],
        "physical_scalar": physical["physical_scalar"], "remainder_scalar": remainder_scalar,
        "pivot": {"lead": lead, "scale": sigma, "normalized_sha256": sha(normalized), "reductions": reductions},
        "target": target_body, "separator": separator, "target_derivation": target_derivation,
        "raw_word_sha256": sha(canonical(raw["record"])), "source_correction_sha256": sha(canonical(corrected["record"])),
        "physical_literal_sha256": sha(canonical(literal)), "p1_roots_sha256": sha(canonical(corrected["roots"])),
        "instruction_sha256": sha(canonical(instruction)), "physical_appends": 1,
        "positive_readout": "TASK958_PENDING" if raw_lambda is None else "NOT_APPLICABLE",
        "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False, **ASSURANCE})
    return {"remainder": remainder, "normalized": normalized, "literal": literal, "instruction": instruction,
            "target": target, "lambda": raw_lambda, "result": result}


ORACLE_ROSTERS = {
    "geometry": {
        "next-pos.u32": ("u32le", [N, 2]), "prev-pos.u32": ("u32le", [N, 2]),
        "phi.u32": ("u32le", [6, N]), "parent.u32": ("u32le", [N]),
        "parent-edge.u32": ("u32le", [N]), "bfs-order.u32": ("u32le", [N]),
        "carry.u8": ("u8", [EDGES, 5]), "chord-edges.u32": ("u32le", [54433]),
        "geometry.json": ("json", None), "tag-fox.json": ("json", None)},
    "section": {
        "q.bin": ("packed3", [4, TOP]), "p1-values.u8": ("u8", [4, P1_ROWS]),
        "chi.u8": ("u8", [P1_ROWS]), "equation-values.u8": ("u8", [P1_ROWS]),
        "equation-residuals.u8": ("u8", [P1_ROWS]), "beta.u8": ("u8", [2014]),
        "kappa.bin": ("packed3", [LOWER]), "lead-original.u32": ("u32le", [P1_ROWS]),
        "lead-embedded.u32": ("u32le", [P1_ROWS]), "new-solve-order.u32": ("u32le", [6045]),
        "old-solve-order.u32": ("u32le", [2014]), "section.json": ("json", None)},
    "cochain": {"score.u8": ("u8", [6, 2, N]), "f.u8": ("u8", [EDGES]),
                "b-aux.u8": ("u8", [2]), "cochain.json": ("json", None)},
    "tree": {"potential-f.u8": ("u8", [N]), "potential-tau.u8": ("u8", [N, 5]),
        "chord-values.u8": ("u8", [54433]), "chord-tau.u8": ("u8", [54433, 5]),
        "chord-residuals.u8": ("u8", [54433]), "selected-chords.u32": ("u32le", [5]),
        "fit.u8": ("u8", [5]), "witness.json": ("json", None), "tree.json": ("json", None)},
}


def validate_oracle_public_metadata(objects: Any, arrays: Any, snapshot: Any) -> None:
    manifest, start, result = (objects["output/" + name] for name in ("manifest.json", "start.json", "result.json"))
    require(set(manifest["file_roster"]) == {"cochain", "geometry", "manifest.json", "owner.json", "result.json",
                                            "section", "source.json", "start.json", "tree"}, "oracle_public_roster")
    require({key: result[key] for key in snapshot} == snapshot, "oracle_public_snapshot")
    require(start["lambda_sha256"] == result["lambda_sha256"] == snapshot["lambda_sha256"], "oracle_public_current_root")
    require(all(value is True for value in (
        arrays["geometry"]["geometry.json"]["full_vertex_eof"], arrays["geometry"]["geometry.json"]["full_edge_eof"],
        arrays["section"]["section.json"]["equation_eof"], arrays["cochain"]["cochain.json"]["score_eof"],
        arrays["cochain"]["cochain.json"]["edge_eof"], arrays["tree"]["tree.json"]["full_chord_eof"])), "oracle_public_eof")
    witness = arrays["tree"]["witness.json"]
    require(type(witness["scalar"]) is int and
            ((result["terminal"] == "VIOLATION_CANDIDATE" and witness["scalar"] in (1, 2) and
              witness["kind"] in ("chord", "auxiliary")) or
             (result["terminal"] == "COMPLETE_ZERO_CANDIDATE" and witness["scalar"] == 0 and witness["kind"] == "none")),
            "oracle_public_witness_scalar")


def validate_oracle_completion(objects: Any) -> None:
    completion = objects["completion-run-receipt.json"]
    preserved = objects["preserved-input.json"]
    original = objects["source-receipt.json"]
    repair = objects["repair-source-receipt.json"]
    checked, source = objects["checker-result.json"], objects["output/source.json"]
    prefix = "d972.r07.section-cochain-checker-completion.v1."
    require(completion["schema"] == prefix + "completion-run-receipt" and
            preserved["schema"] == prefix + "preserved-input" and
            repair["schema"] == prefix + "repair-source-receipt" and
            original["schema"] == "d972.r07.section-cochain-oracle.v1.source-receipt",
            "oracle_completion_receipt_types")
    launch = {key: ORACLE_ARTIFACT[key] for key in ("run", "attempt", "head")}
    require({key: completion["completion"][key] for key in launch} == repair["launch"] == launch and
            completion["completion"]["workflow"] == repair["workflow"] and
            completion["origin"] == preserved["origin"], "oracle_completion_distinct_launches")
    references = {"new_checker_result_sha256": "checker-result.json",
        "producer_result_sha256": "output/result.json", "source_receipt_sha256": "source-receipt.json",
        "repair_source_receipt_sha256": "repair-source-receipt.json", "preserved_input_sha256": "preserved-input.json"}
    require(all(completion[field] == ORACLE_FILES[name][1] for field, name in references.items()),
            "oracle_completion_receipt_hash_chain")
    require(completion["status"] == "PASS" and completion["producer_invocations"] == 0 and
            completion["checker_invocations"] == 1 and completion["old_success_suites"] == 0 and
            completion["old_parent_canaries_executed"] == 0 and
            all(completion[key] is True for key in ("producer_output_unchanged", "complete_A_to_D_replay",
                                                   "all_stage_and_top_arrays_compared")) and
            completion["output_files"] == preserved["output_file_count"] == 44 and
            completion["output_bytes"] == preserved["output_bytes"] == 5361492 and
            completion["output_directories"] == len(preserved["output_directories"]) == 4,
            "oracle_successful_checker_only_completion")
    original_files = {item["file"]: item for item in original["files"]}
    require(len(original_files) == len(original["files"]) and
            repair["files"][:-1] == original["files"] and
            repair["files"][-1]["file"] == "search/check_d972_r07_section_cochain_oracle_v2.py" and
            repair["files"][-1]["sha256"] == checked["checker_sha256"] == completion["repaired_checker_sha256"] and
            original_files["search/check_d972_r07_section_cochain_oracle_v1.py"]["sha256"] ==
                completion["original_checker_sha256"] and
            original_files["search/" + ORACLE_MODULE]["sha256"] == completion["producer_sha256"] ==
                source["producer_sha256"] == ORACLE_MODULE_SHA and
            original["data"] == repair["data"] == source["data"] == checked["source_data_pins"],
            "oracle_original_producer_and_repaired_checker_sources")
    pins = {item["file"]: (item["bytes"], item["sha256"]) for item in preserved["entry_pins"]}
    require(all(pins[name] == ORACLE_FILES[name] for name in
                ("output/manifest.json", "output/start.json", "output/owner.json", "output/source.json",
                 "output/result.json", "source-receipt.json")) and
            pins["output/tree/witness.json"][1] == ORACLE_SNAPSHOT["witness_sha256"],
            "oracle_preserved_source_and_output_entry_pins")


def read_oracle(oracle: Any, root: Path) -> Any:
    require(ORACLE_ARTIFACT and ORACLE_FILES and ORACLE_SNAPSHOT, "actual_oracle_acceptance_pins_pending")
    objects = {name: oracle.json_bytes(oracle.read_fixed(root, name, pin)) for name, pin in ORACLE_FILES.items()}
    manifest, start, owner, source, result, checked = (objects[name] for name in
        ("output/manifest.json", "output/start.json", "output/owner.json", "output/source.json",
         "output/result.json", "checker-result.json"))
    for value, kind in ((manifest, "manifest"), (start, "start"), (owner, "owner"),
                        (source, "source"), (result, "result"), (checked, "checker-result")):
        require(oracle.sealed_ok(value, kind), "accepted_oracle_seal:" + kind)
    validate_oracle_completion(objects)
    require(checked["schema"] == oracle.SCHEMA + ".checker-result" and
            checked["status"] == result["status"] == "PASS" and
            result["terminal"] in ("COMPLETE_ZERO_CANDIDATE", "VIOLATION_CANDIDATE") and
            all(value.get("cross_checked") is False and value.get("verified") is False for value in (result, checked)),
            "accepted_oracle_success_type")
    snapshot = {key: result[key] for key in ("terminal", "rank", "generation", "state_head",
                                            "lambda_sha256", "target_remainder_sha256", "witness_sha256")}
    require(snapshot == ORACLE_SNAPSHOT, "accepted_oracle_snapshot_pin")
    for key in ("rank", "generation", "state_head"):
        require(start[key] == result[key] == checked[key], "accepted_oracle_snapshot_join:" + key)
    require(start["lambda_sha256"] == result["lambda_sha256"] and
            start["target_remainder_sha256"] == result["target_remainder_sha256"] and
            manifest["owner_sha256"] == result["owner_sha256"] == checked["owner_sha256"] == sha(canonical(owner)) and
            manifest["snapshot_sha256"] == result["snapshot_sha256"] == checked["snapshot_sha256"] == sha(canonical(start)) and
            manifest["source_sha256"] == result["source_sha256"] == sha(canonical(source)) and
            manifest["result_sha256"] == checked["result_sha256"] == sha(canonical(result)) and
            checked["manifest_sha256"] == sha(canonical(manifest)) and
            checked["terminal"] == result["terminal"] and checked["materialization"] == result["materialization"] and
            checked["stage_manifests"] == result["stage_manifests"] == manifest["stage_manifests"] and
            checked["lambda_rho2"] == start["lambda_rho2"] == result["lambda_rho2"] and
            checked["direct_pairing"] == start["direct_pairing"] == result["direct_pairing"],
            "accepted_oracle_owner_start_source_result")
    require(checked["all_stage_arrays_compared"] is True and checked["section_equalities"] == P1_ROWS and
            checked["chords_checked"] == 54433 and checked["auxiliary_tests"] == 2 and
            checked["new_physical_appends"] == checked["old_scans_numerically_replayed"] == 0 and
            source["producer_sha256"] == ORACLE_MODULE_SHA, "accepted_oracle_complete_checker")
    output = root / "output"
    require({path.name for path in output.iterdir()} == set(manifest["file_roster"]) ==
            {"cochain", "geometry", "manifest.json", "owner.json", "result.json", "section", "source.json", "start.json", "tree"},
            "accepted_oracle_top_roster")
    expected_top = [{"file": name, "bytes": len(canonical(objects["output/" + name])),
                     "sha256": sha(canonical(objects["output/" + name]))}
                    for name in ("owner.json", "result.json", "source.json", "start.json")]
    require(manifest["files"] == expected_top, "accepted_oracle_top_file_pins")
    arrays, stage_hashes = {}, result["stage_manifests"]
    for stage, roster in ORACLE_ROSTERS.items():
        directory = output / stage
        stage_manifest = oracle.read_json(output, stage + "/manifest.json")
        require(oracle.sealed_ok(stage_manifest, "stage-manifest") and
                sha(canonical(stage_manifest)) == stage_hashes[stage] and stage_manifest["stage"] == stage and
                stage_manifest["owner_sha256"] == sha(canonical(owner)) and
                stage_manifest["snapshot_sha256"] == sha(canonical(start)), "accepted_oracle_stage_binding")
        expected_inputs = {} if stage in ("geometry", "section") else \
            {name: stage_hashes[name] for name in (("geometry", "section") if stage == "cochain" else ("geometry", "cochain"))}
        files = stage_manifest["files"]
        require(stage_manifest["inputs"] == expected_inputs and
                [item["file"] for item in files] == sorted(roster) and
                {path.name for path in directory.iterdir()} == set(roster) | {"manifest.json"},
                "accepted_oracle_stage_roster")
        arrays[stage] = {}
        for item in files:
            dtype, shape = roster[item["file"]]
            require(set(item) == {"file", "bytes", "sha256", "dtype", "shape"} and
                    (item["dtype"], item["shape"]) == (dtype, shape), "accepted_oracle_array_type")
            raw_bytes = oracle.read_fixed(directory, item["file"], (item["bytes"], item["sha256"]))
            if dtype == "json":
                value = oracle.json_bytes(raw_bytes)
            else:
                count = math.prod(shape)
                if dtype == "packed3":
                    value = oracle.unpack(raw_bytes, count)
                elif dtype == "u8":
                    require(len(raw_bytes) == count, "accepted_oracle_u8_bytes")
                    value = np.frombuffer(raw_bytes, dtype=np.uint8)
                    require(not np.any(value > 2), "accepted_oracle_trit_values")
                else:
                    require(dtype == "u32le" and len(raw_bytes) == count * 4, "accepted_oracle_u32_bytes")
                    value = np.frombuffer(raw_bytes, dtype="<u4")
                value = value.reshape(tuple(shape))
            arrays[stage][item["file"]] = value
        check_deadline("accepted-oracle-stage:" + stage)
    geometry, section, cochain, tree = (arrays[name] for name in ("geometry", "section", "cochain", "tree"))
    for value, kind in ((geometry["geometry.json"], "geometry"), (section["section.json"], "section"),
                        (cochain["cochain.json"], "cochain"), (tree["tree.json"], "tree"), (tree["witness.json"], "witness")):
        require(oracle.sealed_ok(value, kind), "accepted_oracle_payload_seal")
    require(geometry["geometry.json"]["full_vertex_eof"] is True and
            geometry["geometry.json"]["full_edge_eof"] is True and
            section["section.json"]["equation_eof"] is True and
            cochain["cochain.json"]["score_eof"] is True and cochain["cochain.json"]["edge_eof"] is True and
            tree["tree.json"]["full_chord_eof"] is True and
            not np.any(section["equation-residuals.u8"]) and
            np.array_equal(section["equation-values.u8"], section["chi.u8"]), "accepted_oracle_all_eof")
    witness = tree["witness.json"]
    require(sha(canonical(witness)) == snapshot["witness_sha256"] and
            tree["tree.json"]["terminal"] == result["terminal"] and
            witness["materialization"] == result["materialization"], "accepted_oracle_witness_binding")
    if result["terminal"] == "COMPLETE_ZERO_CANDIDATE":
        require(witness["kind"] == "none" and witness["scalar"] == 0 and witness["cycles"] == [] and
                not np.any(cochain["b-aux.u8"]) and not np.any(tree["chord-residuals.u8"]),
                "accepted_oracle_complete_zero")
    else:
        require(witness["kind"] in ("chord", "auxiliary") and type(witness["scalar"]) is int and
                witness["scalar"] in (1, 2) and witness["materialization"] == "MATERIALIZATION_PENDING",
                "accepted_oracle_nonzero_witness")
    validate_oracle_public_metadata(objects, arrays, ORACLE_SNAPSHOT)
    layout = seal("oracle-parent-layout", {"artifact": ORACLE_ARTIFACT,
        "entry_files": [{"file": name, "bytes": pin[0], "sha256": pin[1]} for name, pin in sorted(ORACLE_FILES.items())],
        "manifest_sha256": sha(canonical(manifest)), "start_sha256": sha(canonical(start)),
        "owner_sha256": sha(canonical(owner)), "source_sha256": sha(canonical(source)),
        "result_sha256": sha(canonical(result)), **snapshot, "old_arithmetic_replayed": False})
    return {"objects": objects, "layout": layout, "stages": stage_hashes, "arrays": arrays,
        "witness": witness, "q": section["q.bin"], "kappa": section["kappa.bin"],
        "f": cochain["f.u8"], "b_aux": cochain["b-aux.u8"],
        "geometry": {"next": geometry["next-pos.u32"], "prev": geometry["prev-pos.u32"],
            "parent": geometry["parent.u32"], "parent_edge": geometry["parent-edge.u32"],
            "order": geometry["bfs-order.u32"], "phi": geometry["phi.u32"], "carry": geometry["carry.u8"],
            "chords": geometry["chord-edges.u32"], "chord_set": set(int(x) for x in geometry["chord-edges.u32"]),
            "tags": geometry["tag-fox.json"]["tags"]}}


class PayloadWriter:
    def __init__(self, oracle: Any, output: Path):
        self.oracle, self.output = oracle, output
        self.entries: dict[str, Any] = {}
        self.telemetry: list[Any] = []

    def write(self, name: str, value: Any, dtype: str = "json", shape: Any = None) -> None:
        require(name not in self.entries, "unique_output_payload")
        if dtype == "json":
            raw, shape = canonical(value), None
        elif dtype == "packed3" and isinstance(value, bytes):
            raw = value
            require(shape is not None and len(raw) * 4 == math.prod(shape), "packed_output_shape")
            self.oracle.unpack(raw, math.prod(shape))
        else:
            raw, returned_dtype, returned_shape = self.oracle.array_payload(value, dtype)
            require(dtype == returned_dtype and (shape is None or shape == returned_shape), "array_output_shape")
            shape = returned_shape
        self.oracle.write_atomic(self.output, name, raw)
        self.entries[name] = {"file": name, "bytes": len(raw), "sha256": sha(raw), "dtype": dtype, "shape": shape}

    def stage(self, stage: str, begun: float, files: Any, *, alpha_support: int | None = None,
              letters: int | None = None) -> None:
        require(stage == ("raw", "source", "primal", "p1", "B", "physical")[len(self.telemetry)], "stage_order")
        self.telemetry.append({"stage": stage, "elapsed_seconds": round(time.monotonic() - begun, 6),
            "bytes": sum(self.entries[name]["bytes"] for name in files), "eof": True,
            "alpha_support": alpha_support, "letters": letters})
        COMPLETED_STAGES.append(stage)
        progress("completed-stage", stage=stage, files=len(files))


def retained_source(oracle: Any, refinement: Any, p2: Any) -> Any:
    modules = {ORACLE_MODULE: ORACLE_MODULE_SHA,
        oracle.REFINEMENT_MODULE: oracle.REFINEMENT_MODULE_SHA,
        refinement.FIXED_MODULE: refinement.FIXED_MODULE_SHA, **p2.MODULE_PINS}
    data = {**p2.DATA_PINS, NORMALIZER_DATA["file"]: {k: NORMALIZER_DATA[k] for k in ("bytes", "sha256")}}
    return seal("source", {"producer_sha256": sha(Path(__file__).read_bytes()), "modules": modules,
        "data": data, "python": sys.version, "numpy": np.__version__})


def run_actual(args: Any) -> Any:
    global OUTPUT_CREATED
    oracle, refinement, p2, m, base, descriptors = own_dependencies()
    output = args.output_root.resolve()
    roots = [getattr(args, name) for name in ("state_root", "delta_root", "seed34_root", "packet_root",
             "refinement_root", "prepare_root", "p1_root", "task712_root", "oracle_root")] + args.block_root
    require(not output.exists() and not args.output_root.is_symlink(), "fresh_cycle_output")
    for path in roots:
        root = path.resolve()
        require(path.is_dir() and not path.is_symlink() and root != output and
                root not in output.parents and output not in root.parents, "cycle_disjoint_roots")
    accepted = read_oracle(oracle, args.oracle_root)
    if accepted["layout"]["terminal"] == "COMPLETE_ZERO_CANDIDATE":
        result = seal("not-applicable", {"status": "NOT_APPLICABLE", "terminal": "NOT_APPLICABLE",
            "oracle_terminal": "COMPLETE_ZERO_CANDIDATE", "accepted_oracle_layout": accepted["layout"],
            "physical_appends": 0, "candidate": False, "cross_checked": False, "verified": False})
        output.mkdir(parents=True)
        OUTPUT_CREATED = True
        oracle.write_atomic(output, "not-applicable.json", canonical(result))
        return result
    state, old_start, old_owner, p1, task554, tables = oracle.accepted_snapshot(refinement, p2, m, base, descriptors, args)
    require(old_start == accepted["objects"]["output/start.json"] and
            old_owner == accepted["objects"]["output/owner.json"], "oracle_same_actual_current_snapshot")
    index = oracle.read_json(args.refinement_root, "output/canonical-index.json")
    source_pin = retained_source(oracle, refinement, p2)
    expected_modules = {key: value for key, value in source_pin["modules"].items() if key != ORACLE_MODULE}
    require(accepted["objects"]["output/source.json"]["modules"] == expected_modules and
            accepted["objects"]["output/source.json"]["data"] == p2.DATA_PINS, "oracle_same_retained_sources")
    owner = seal("owner", {"formula_id": FORMULA, "scope": SCOPE,
        "oracle_owner_sha256": accepted["layout"]["owner_sha256"],
        "refinement_head_sha256": oracle.REFINEMENT_FILES["output/HEAD"][1],
        **{key: old_owner[key] for key in ("p1_parent", "task554_parent", "task712_parent",
             "task712_manifest_sha256", "word_dictionary_sha256", "relator_dictionary_sha256")}})
    start = seal("start", {"kind": "Separator", "rank": state["rank"], "generation": state["generation"],
        "state_head": state["head"], "lambda_sha256": sha(state["lambda_raw"]),
        "target_remainder_sha256": sha(state["target_raw"]), "accepted_oracle_layout": accepted["layout"],
        **{key: old_start[key] for key in ("accepted_refinement_layout", "accepted_target_derivation_parents",
                                         "lambda_rho2", "direct_pairing")}})
    check_deadline("before-cycle-output")
    output.mkdir(parents=True)
    OUTPUT_CREATED = True
    writer = PayloadWriter(oracle, output)
    for name, value in (("owner.json", owner), ("start.json", start), ("source.json", source_pin)):
        writer.write(name, value)
    context, words = base.source_context()
    begun = time.monotonic()
    raw = selected_raw_word(oracle, base.ARITH, context, accepted)
    writer.write("raw-word.json", raw["record"])
    writer.write("raw-chain.bin", raw["chain"], "packed3")
    writer.stage("raw", begun, ["raw-word.json", "raw-chain.bin"], letters=raw["record"]["word_stream"]["letters"])
    begun = time.monotonic()
    source = source_from_chain(oracle, refinement, m, base.ARITH, context, accepted, raw)
    names = []
    for name, part in zip(("d0", "d1", "d2", "aux"), source["parts"]):
        name = "raw-source-" + name + ".bin"
        writer.write(name, part, "packed3")
        names.append(name)
    writer.write("raw-source.json", source["record"])
    writer.stage("source", begun, [*names, "raw-source.json"])
    begun = time.monotonic()
    segments, pairs, exponents = basis_segments(oracle, base, task554, p1, index, words)
    primal = primal_section(oracle, m, segments, source["parts"])
    support = int(np.count_nonzero(primal["alpha"]))
    writer.write("p1-coefficients.u8", primal["alpha"], "u8")
    writer.write("p1-reductions.json", primal["record"])
    writer.write("p1-exponent-residues.json", exponents)
    writer.stage("primal", begun, ["p1-coefficients.u8", "p1-reductions.json", "p1-exponent-residues.json"], alpha_support=support)
    begun = time.monotonic()
    corrected = corrected_source(oracle, refinement, m, p1, index, segments, pairs, raw, source, primal)
    writer.write("p1-roots.json", corrected["roots"])
    writer.write("source-lower-remainder.bin", lower_row(corrected["parts"]), "packed3")
    writer.write("source-top-corrected.bin", corrected["parts"][2], "packed3")
    writer.write("source-correction.json", corrected["record"])
    writer.stage("p1", begun, ["p1-roots.json", "source-lower-remainder.bin", "source-top-corrected.bin",
                               "source-correction.json"], alpha_support=support)
    begun = time.monotonic()
    physical = four_B(oracle, m, tables, state, accepted, corrected)
    writer.write("physical-by-character.bin", physical["by_character"], "packed3")
    writer.write("physical-raw.bin", physical["raw"], "packed3", [PHYSICAL])
    writer.stage("B", begun, ["physical-by-character.bin", "physical-raw.bin"])
    begun = time.monotonic()
    row = one_physical_row(oracle, m, state, start, owner, source_pin, accepted, raw, source, primal, corrected, physical)
    names = []
    for name, key in (("physical-remainder.bin", "remainder"), ("physical-normalized.bin", "normalized"),
                      ("target-remainder.bin", "target"), ("lambda.bin", "lambda")):
        if row[key] is not None:
            writer.write(name, row[key], "packed3", [PHYSICAL])
            names.append(name)
    for name, key in (("physical-literal.json", "literal"), ("instruction.json", "instruction"), ("result.json", "result")):
        writer.write(name, row[key])
        names.append(name)
    writer.stage("physical", begun, names)
    writer.write("telemetry.json", seal("telemetry", {"stages": writer.telemetry,
        "old_scans_numerically_replayed": 0, "old_inserts_numerically_replayed": 0, "physical_appends": 1}))
    result = row["result"]
    manifest = seal("manifest", {"owner_sha256": sha(canonical(owner)), "start_sha256": sha(canonical(start)),
        "source_sha256": sha(canonical(source_pin)), "result_sha256": sha(canonical(result)),
        "instruction_sha256": sha(canonical(row["instruction"])), "parent_state_head": state["head"],
        "state_head": result["state_head"], "files": [writer.entries[key] for key in sorted(writer.entries)],
        "stage_eof": ["raw", "source", "primal", "p1", "B", "physical"], **ASSURANCE})
    check_deadline("before-one-row-commit")
    oracle.write_atomic(output, "manifest.json", canonical(manifest))
    head = seal("head", {"owner_sha256": sha(canonical(owner)), "source_sha256": sha(canonical(source_pin)),
        "start_sha256": sha(canonical(start)), "manifest_sha256": sha(canonical(manifest)),
        "instruction_sha256": sha(canonical(row["instruction"])), "parent_state_head": state["head"],
        "state_head": result["state_head"], "rank": result["rank_after"], "generation": result["generation_after"],
        "kind": result["kind"], "completed_steps": 1, "physical_sha256": sha(row["normalized"]),
        "target_remainder_sha256": sha(row["target"]), "lambda_sha256": sha(row["lambda"]) if row["lambda"] is not None else None})
    oracle.write_atomic(output, "HEAD", canonical(head))
    return result


def expect_reject(action: Any, name: str) -> None:
    try:
        action()
    except ResourceStop:
        raise
    except Exception:
        return
    raise RuntimeError("mutation_accepted:" + name)


def parent_layout_selftest(args: Any) -> Any:
    oracle, _refinement, _p2, _m, _base, _descriptors = own_dependencies()
    old = oracle.parent_layout_selftest(args)
    accepted = read_oracle(oracle, args.oracle_root)
    cases = ("oracle-roster", "oracle-witness-scalar", "oracle-snapshot", "oracle-eof", "oracle-current-root")
    for name in cases:
        objects, arrays = copy.deepcopy(accepted["objects"]), copy.deepcopy(accepted["arrays"])
        if name == "oracle-roster":
            objects["output/manifest.json"]["file_roster"].remove("geometry")
        elif name == "oracle-witness-scalar":
            witness = arrays["tree"]["witness.json"]
            witness["scalar"] = 0 if witness["scalar"] else 1
        elif name == "oracle-snapshot":
            objects["output/result.json"]["rank"] += 1
        elif name == "oracle-eof":
            arrays["geometry"]["geometry.json"]["full_edge_eof"] = False
        else:
            objects["output/start.json"]["lambda_sha256"] = "0" * 64
        expect_reject(lambda: validate_oracle_public_metadata(objects, arrays, ORACLE_SNAPSHOT), name)
    return seal("parent-layout-selftest", {"status": "PASS", "metadata_only": True,
        **{key: old[key] for key in ("parent_layout", "accepted_packet_layout", "accepted_refinement_layout")},
        "accepted_oracle_layout": accepted["layout"], "rejected_cases": [*old["rejected_cases"], *cases],
        "cross_checked": False, "verified": False})


def selftest() -> Any:
    oracle, refinement, _p2, m, base, _descriptors = own_dependencies()
    context, words = base.source_context()
    arith = base.ARITH
    left, right = (1, 2, -1, 2), (-2, 1, 1, -2)
    require(scalar_product(exponent_omega(left), exponent_omega(right)) == exponent_omega(left + right),
            "canary_omega_product")
    for power in (-3, -1, 0, 1, 2, 4):
        word = left * power if power >= 0 else inverse_word(left) * -power
        require(scalar_power(exponent_omega(left), power) == exponent_omega(word), "canary_omega_integer_power")
    require(exponent_omega((-1, -2, 1, 2))[2] == 2, "canary_commutator_sign")
    require(signed_pair_product((0, 0), [[0, 2]], 0, [(18, 36)], 2) == (36, 18), "canary_signed_P1_mod54")
    expect_reject(lambda: oracle.array_payload(np.asarray([18, 36], dtype=np.uint8), "u8"), "residue54_not_trits")

    geometry_data = oracle.geometry_inputs(arith, context)
    ga = geometry_data["arrays"]
    geometry = {"next": ga["next-pos.u32"][0], "prev": ga["prev-pos.u32"][0],
        "parent": ga["parent.u32"][0], "parent_edge": ga["parent-edge.u32"][0],
        "order": ga["bfs-order.u32"][0], "phi": ga["phi.u32"][0], "carry": ga["carry.u8"][0],
        "chords": ga["chord-edges.u32"][0], "chord_set": set(int(x) for x in ga["chord-edges.u32"][0]),
        "tags": ga["tag-fox.json"][0]["tags"]}
    normalizers, _ = normalizer_dictionary(oracle)
    slp = RawSLP(oracle, arith, context, geometry, normalizers)
    for letter in ACTORS:
        slp.add("letter" + str(letter), "Letter", letter=letter)
    seed = tuple(words["relators"][2])
    slp.add("seed", "OrderedProduct", factors=["letter" + str(letter) for letter in seed])
    slp.add("raw-root", "IntegerPower", node="seed", exponent=-1)
    chain, endpoint, stream = word_fox(slp, "raw-root")
    require(endpoint == arith.SEED_AFFINE_IDENTITY and stream["letters"] == len(seed), "canary_negative_raw_word")
    a, b = slp.values["raw-root"]["scalar"][:2]
    require(a % 18 == b % 18 == 0, "canary_raw_integer_eta")
    raw = {"slp": slp, "chain": chain, "eta": [a // 18 % 3, b // 18 % 3], "record": {"fixture": "negative-seed2"}}
    accepted = {"geometry": geometry, "q": np.zeros((4, TOP), dtype=np.uint8),
        "kappa": np.zeros(LOWER, dtype=np.uint8), "witness": {"scalar": 0}}
    rebuilt = source_from_chain(oracle, refinement, m, arith, context, accepted, raw)
    direct = arith._seed_evaluate_seed(context, inverse_word(seed))
    require(all(np.array_equal(x, y) for x, y in zip(rebuilt["parts"], direct)) and np.any(direct[2]),
            "canary_same_raw_word_all_filtered_degrees_characters")
    edge = int(geometry["chords"][0])
    positive = witness_chain(geometry, {"cycles": [{"edge": edge, "coefficient": 1}]})
    negative = witness_chain(geometry, {"cycles": [{"edge": edge, "coefficient": 2}]})
    require(np.array_equal(negative, (-positive.astype(np.int16)) % 3), "canary_negative_chord_chain")
    require(arith._seed_affine_mul(context.images[0], context.images[1]) !=
            arith._seed_affine_mul(context.images[1], context.images[0]), "canary_actual_noncommuting_endpoints")

    # Nonmonotone original leads: reverse insertion leaves an earlier source
    # coordinate behind. Full old d1 companions and shared aux are consumed.
    rows, companions = [], []
    leads = (2, 0, 1)
    for i, lead in enumerate(leads):
        row = np.zeros(6056, dtype=np.uint8)
        row[lead] = 1
        if lead < 2:
            row[lead + 1] = 1
        companion = np.zeros((4, 18144), dtype=np.uint8)
        for owner in range(4):
            companion[owner, i] = 1 + owner % 2
        rows.append(row)
        companions.append(companion.reshape(-1))
    work = refinement.empty_lift(m)
    for row, companion in zip(rows, companions):
        m.add_scaled(work[0][0], row[:6048], 1)
        m.add_scaled(work[1], companion.reshape(4, 18144), 1)
    wrong = tuple(x.copy() for x in work)
    for local in reversed(range(3)):
        consume_source_row(m, wrong, "old", 0, leads[local], rows[local], companions[local])
    require(np.any(wrong[0]), "canary_reverse_insertion_wrong_source_order")
    for local in sorted(range(3), key=lambda i: leads[i]):
        consume_source_row(m, work, "old", 0, leads[local], rows[local], companions[local])
    require(not np.any(work[0]) and not np.any(work[1]), "canary_primal_old_four_companions")
    aux_row = np.zeros(6056, dtype=np.uint8)
    aux_row[6054] = 1
    work[3][6] = 2
    consume_source_row(m, work, "old", 0, 6054, aux_row, np.zeros(72576, dtype=np.uint8))
    for owner in range(4):
        row = np.zeros(18144, dtype=np.uint8)
        row[7] = 1
        work[1][owner, 7] = 2
        require(consume_source_row(m, work, "new", owner, 7, row) == 2, "canary_new_original_row_no_double_scale")
    require(not np.any(lower_row(work)), "canary_primal_full_shared_lower_zero")

    e0, e1, e2 = (np.zeros(PHYSICAL, dtype=np.uint8) for _ in range(3))
    e0[0], e1[1], e2[2] = 1, 1, 1
    state = {"rank": 1, "generation": 4, "head": "1" * 64, "rows": [oracle.pack(e0)], "leads": [0],
        "records": [{"offer": 0, "lead": 0, "physical_offset": 0}], "target_raw": oracle.pack(e2), "lambda": e1 + e2}
    start = {"lambda_rho2": {"original_rho2_packed_sha256": "2" * 64}, "accepted_target_derivation_parents": []}
    fixture_accepted = {"witness": {"kind": "chord", "scalar": 1},
                        "layout": {"manifest_sha256": "3" * 64, "witness_sha256": "4" * 64}}
    source, primal, corrected = {"homogeneous": 1, "section": 0}, {"record": {}}, {"record": {}, "roots": {}}
    physical = {"raw": oracle.pack(e1), "corrected_scalar": 1, "physical_scalar": 1}
    first = one_physical_row(oracle, m, state, start, {}, {}, fixture_accepted, {"record": {}}, source, primal, corrected, physical)
    require(first["result"]["target"]["scalar"] == 0 and first["target"] == state["target_raw"] and
            first["result"]["generation_after"] == 5 and first["result"]["terminal"] == "PIVOT_CANDIDATE",
            "canary_plain_zero_scalar_dynamic_generation")
    bad_target = seal("target", first["result"]["target"])
    expect_reject(lambda: validate_plain_target(bad_target, sha(state["target_raw"]), sha(first["target"]), 0),
                  "plain_target_generic_seal")
    state["target_raw"], state["lambda"] = oracle.pack(e1), e1.copy()
    member = one_physical_row(oracle, m, state, start, {}, {}, fixture_accepted, {"record": {}}, source, primal, corrected, physical)
    require(member["lambda"] is None and member["result"]["terminal"] == "LINEAR_MEMBERSHIP_CANDIDATE" and
            member["result"]["positive_readout"] == "TASK958_PENDING", "canary_linear_zero_is_not_MEMBER")
    with tempfile.TemporaryDirectory(prefix="r07-selected-cycle-canary-") as folder:
        writer = PayloadWriter(oracle, Path(folder))
        writer.write("target-remainder.bin", first["target"], "packed3", [PHYSICAL])
        writer.write("instruction.json", first["instruction"])
        require(sha((Path(folder) / "instruction.json").read_bytes()) == writer.entries["instruction.json"]["sha256"],
                "canary_actual_payload_serializer")
        instruction = first["instruction"]
        require(instruction["rolling_sha256"] == sha(bytes.fromhex(instruction["predecessor"]) +
                canonical({key: value for key, value in instruction.items() if key != "rolling_sha256"})),
                "canary_actual_one_row_instruction_chain")
    return seal("selftest", {"status": "PASS", "groups": ["raw-slp-omega-negative-source",
        "primal-original-leads-shared-aux-mod54", "one-row-plain-target-and-serializer"],
        "whole_old_suites_run": 0, "old_prefix_numerically_replayed": 0, "cross_checked": False, "verified": False})


def request_stop(_signal: int, _frame: Any) -> None:
    global STOP_REQUESTED
    STOP_REQUESTED = True


def main() -> int:
    global DEADLINE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--parent-layout-selftest", action="store_true")
    parser.add_argument("--max-seconds", type=float, default=1800.0)
    names = ("state-root", "delta-root", "seed34-root", "packet-root", "refinement-root", "oracle-root",
             "prepare-root", "p1-root", "task712-root")
    for name in names:
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    parser.add_argument("--output", dest="output_root", type=Path)
    args = parser.parse_args()
    try:
        require(0 < args.max_seconds < float("inf"), "finite_positive_resource_bound")
        DEADLINE = STARTED + args.max_seconds
        for signum in (signal.SIGINT, signal.SIGTERM):
            signal.signal(signum, request_stop)
        if args.selftest:
            require(not args.parent_layout_selftest and args.output_root is None and not args.block_root and
                    all(getattr(args, name.replace("-", "_")) is None for name in names), "selftest_no_parents")
            result = selftest()
        elif args.parent_layout_selftest:
            require(args.output_root is None and not args.block_root and
                    all(getattr(args, name.replace("-", "_")) is not None for name in names[:6]) and
                    all(getattr(args, name.replace("-", "_")) is None for name in names[6:]), "metadata_six_parents")
            result = parent_layout_selftest(args)
        else:
            require(args.output_root is not None and len(args.block_root) == 4 and
                    all(getattr(args, name.replace("-", "_")) is not None for name in names), "actual_thirteen_parents")
            result = run_actual(args)
        print(canonical(result).decode("ascii"), end="", flush=True)
        return 0
    except ResourceStop as exc:
        diagnostic = seal("resource-stop", {"status": "UNKNOWN_RESOURCE", "terminal": "UNKNOWN_RESOURCE",
            "phase": str(exc), "completed_stages": list(COMPLETED_STAGES),
            "candidate": False, "cross_checked": False, "verified": False})
        if OUTPUT_CREATED and LOADED_ORACLE is not None and args.output_root is not None and \
                args.output_root.is_dir() and not args.output_root.is_symlink():
            LOADED_ORACLE.write_atomic(args.output_root.resolve(), "resource-stop.json", canonical(diagnostic), replace=True)
        print(canonical(diagnostic).decode("ascii"), end="", flush=True)
        return 3
    except Exception as exc:
        print(canonical({"status": "REJECTED", "reason": str(exc), "error_type": type(exc).__name__,
                         "cross_checked": False, "verified": False}).decode("ascii"), end="", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
