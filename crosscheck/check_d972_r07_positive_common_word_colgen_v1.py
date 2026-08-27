#!/usr/bin/env python3
"""Helper-nonshared positive checker for task179.

No producer code is imported.  The checker uses the independent task175
quotient/Fox implementation, rebuilds every retained column and rank
transition, and validates only positive finite witnesses.  UNKNOWN receipts
are integrity checkpoints and never become negative certificates.
"""

from __future__ import annotations

import argparse
from array import array
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import sys
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-positive-common-word-colgen/v1"
CHECKPOINT_SCHEMA = "d972-r07-positive-common-word-colgen-checkpoint/v1"
COMMON = "R07_POSITIVE_COMMON_WORD_COLGEN_COMMON_WORD"
FIXTURE = ROOT / "search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json"
FIXTURE_BYTES = 407
FIXTURE_SHA256 = "46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78"


PINS: dict[str, tuple[str, int, str]] = {
    "producer": ("search/d972_r07_positive_common_word_colgen_v1.py", 123870,
                 "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"),
    "task179": ("sol/luna_task_179_r07_positive_common_word_colgen_v1.md", 13105,
                "f97870ec0243b2c399928bcef4f89134f1cd41f15869cc88e3ba7d9dc6956a73"),
    "proof142": ("sol/proof_r07_actual_singleton_coarse_inverse_selector_v142.md", 4942,
                 "5f0fffe64b729a8e44643ce86e9d588ef96cbe199ef8ca03741c712c2b162ee8"),
    "proof143": ("sol/proof_r07_actual_weighted_support_hitting_selector_v143.md", 5253,
                 "aae57d5481d7e649d449b58d06ade2d9cbf90fa48d50a8ae43650da5243cf259"),
    "proof139": ("sol/proof_r07_witness_first_fibre_dovetail_selector_v139.md", 8310,
                 "62e2160348db38eca1570b2ca6eb8934b885569f4e8cfb276a91b98c9b983920"),
    "proof140": ("sol/proof_r07_positive_only_common_word_colgen_v140.md", 10073,
                 "6d388a74c75d55d215b0035496c451aa9de5bbc7a8248c277e76021092b8562b"),
    "proof138": ("sol/proof_r07_cubic_moment_resource_cap_erratum_v138.md", 6371,
                 "9dc94b6de5120e54f3b5a5324fb58a24646ad5917b3bd85c36162af29aa86456"),
    "proof110": ("sol/proof_r07_full_e4_seven_evaluation_orbit_selector_v110.md", 12136,
                 "dd0b75d6dc85229405a3a95e3631a709aa40a0ad21f2c17b96106dae2c7989dc"),
    "proof108": ("sol/proof_pb4_eleven_relator_presentation_equality_v108.md", 6742,
                 "4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f"),
    "proof121": ("sol/proof_pb3_two_relator_presentation_equality_v121.md", 5762,
                 "efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5"),
    "proof122": ("sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md", 7939,
                 "daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348"),
    "proof125": ("sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md", 8545,
                 "b82c81e0a053658fdb48cbb4d3054a094a57a81b2fd5d0153bcd0735ef4852b3"),
    "proof135": ("sol/proof_r07_q4_q0_noncontiguous_deletion_layout_v135.md", 4539,
                 "75c511a765ad88ec1aa72c63a0d1965ac85724695d743cbf00350572a884cf67"),
    "task175_producer": ("search/d972_r07_all_seven_raw_bridge_preflight_v1.py", 60306,
                         "1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa"),
    "task175_checker": ("crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py", 88503,
                        "0b45c3daa1db6cad63d434170c65d0dbfa928efc51543b881dc0aa2e3a0f1fce"),
    "task175_driver": ("search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g", 22052,
                       "919e7a9efe7385444c480203dc51525873e770236777dd61e2f6fc1ef22de494"),
    "task176_producer": ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109,
                         "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"),
    "task176_checker": ("crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py", 84980,
                        "4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"),
    "task176_driver": ("search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g", 15929,
                       "1c6dc7f10d9b27092c2441a274ff74726d8899599ac10c2b8cc47cb59da02995"),
    "q3_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570,
                   "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "joint_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036,
                      "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    "seedspan_arithmetic": ("search/d972_b345_seedspan_triple4_v1.py", 535219,
                            "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
    "old_arithmetic": ("search/d972_b345_triple_cube_raw_lambda_census_v1.py", 126942,
                       "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"),
    "joint_source": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945,
                     "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    "v172_source": ("search/d972_r07_full_e4_joint_orbit_preflight_v7.py", 21918,
                    "92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"),
    "g760_source": ("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py", 33409,
                    "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f"),
    "pb4_source": ("search/d972_b345_target6_dual_colgen_v2.py", 444497,
                   "b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7"),
    "full_d2_v1": ("search/d972_b345_full_d2_dual_correlation_v1.py", 78832,
                   "6903b745be2c005c573d7a368beb826d5f411f0f4a353eeedf3a8cccbc9fde52"),
    "full_d2_v2": ("search/d972_b345_full_d2_dual_correlation_v2.py", 42449,
                   "6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f"),
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(canonical(value))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def pinned_source_identity(rel: str) -> tuple[Path, int, str]:
    identities = {(size, digest) for candidate, size, digest in PINS.values()
                  if candidate == rel}
    require(len(identities) == 1, "module not uniquely pinned:" + rel)
    size, digest = next(iter(identities)); path = ROOT / rel
    require(path.is_file(), "module missing:" + rel)
    raw = path.read_bytes()
    require(len(raw) == size and sha_bytes(raw) == digest,
            "module pin:" + rel)
    return path.resolve(), size, digest


def authenticated_bound_module(name: str, rel: str) -> Any:
    expected_path, _, _ = pinned_source_identity(rel)
    module = sys.modules.get(name)
    require(module is not None, "authenticated module slot empty:" + name)
    source = getattr(module, "__file__", None)
    require(isinstance(source, str) and Path(source).resolve() == expected_path,
            "authenticated module name collision:" + name)
    return module


def authenticate() -> dict[str, Any]:
    out = {}
    for name, (rel, size, digest) in PINS.items():
        raw = (ROOT / rel).read_bytes()
        require(len(raw) == size and sha_bytes(raw) == digest, "pin:" + rel)
        out[name] = {"path": rel, "bytes": size, "sha256": digest}
    raw = FIXTURE.read_bytes()
    require(len(raw) == FIXTURE_BYTES and sha_bytes(raw) == FIXTURE_SHA256,
            "fixture pin")
    out["fixture"] = {"path": str(FIXTURE.relative_to(ROOT)).replace("\\", "/"),
                      "bytes": FIXTURE_BYTES, "sha256": FIXTURE_SHA256}
    return out


def load_module(rel: str, name: str) -> Any:
    path, _, _ = pinned_source_identity(rel)
    if name in sys.modules:
        return authenticated_bound_module(name, rel)
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "module loader")
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        if sys.modules.get(name) is module:
            del sys.modules[name]
        raise
    return module


def module_import_control_public() -> dict[str, Any]:
    double_rel, double_size, double_sha = PINS["g760_source"]
    cross_rel, cross_size, cross_sha = PINS["old_arithmetic"]
    seed_rel, seed_size, seed_sha = PINS["seedspan_arithmetic"]
    return {
        "same_name_same_path_reused": True,
        "same_name_cross_path_rejected": True,
        "double_source": {"path": double_rel, "bytes": double_size,
                          "sha256": double_sha},
        "cross_source": {"path": cross_rel, "bytes": cross_size,
                         "sha256": cross_sha},
        "production_predecessor_slot": "_d972_157ed_old_producer",
        "production_source": {"path": seed_rel, "bytes": seed_size,
                              "sha256": seed_sha},
        "second_authenticated_input_call": False,
    }


def module_import_selftest() -> dict[str, Any]:
    """Independent bounded real-loader double/cross-import control."""
    name = "_d179_checker_bounded_double_cross_import"
    require(name not in sys.modules, "checker import-control slot prebound")
    first: Any = None
    try:
        first = load_module(PINS["g760_source"][0], name)
        require(load_module(PINS["g760_source"][0], name) is first,
                "checker same-path double import did not reuse")
        rejected = False
        try:
            load_module(PINS["old_arithmetic"][0], name)
        except RuntimeError as exc:
            require(str(exc) == "authenticated module name collision:" + name,
                    "checker cross-import rejection type")
            rejected = True
        require(rejected, "checker same-name cross import accepted")
    finally:
        if first is not None and sys.modules.get(name) is first:
            del sys.modules[name]
    return module_import_control_public()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    answer = dict(value); answer.pop("self_digest", None)
    answer["self_digest"] = sha_obj(answer)
    return answer


def validate_seal(value: dict[str, Any]) -> None:
    body = dict(value); claimed = body.pop("self_digest", None)
    require(type(claimed) is str and claimed == sha_obj(body), "self digest")


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        letter = int(raw); require(letter != 0, "zero letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(x) for x in reversed(word)]


def exponent_pair(word: Sequence[int]) -> tuple[int, int]:
    return (sum(1 if x == 1 else -1 if x == -1 else 0 for x in word) % 3,
            sum(1 if x == 2 else -1 if x == -2 else 0 for x in word) % 3)


def row_key(block: int, component: int, blob: bytes) -> bytes:
    require(block in (1, 2, 3) and 1 <= component <= 6, "typed key")
    return b"R" + bytes((block, component)) + len(blob).to_bytes(2, "big") + blob


def exponent_key(index: int) -> bytes:
    return b"E" + bytes((index,))


def decode_row_key(key: bytes) -> tuple[int, int, bytes]:
    require(len(key) >= 5 and key[:1] == b"R", "row key")
    width = int.from_bytes(key[3:5], "big")
    require(len(key) == 5 + width, "row width")
    return key[1], key[2], key[5:]


Sparse = dict[bytes, int]


def add_scaled(target: Sparse, source: Sparse, scalar: int) -> None:
    for key, coefficient in source.items():
        value = (target.get(key, 0) + scalar * coefficient) % 3
        if value:
            target[key] = value
        else:
            target.pop(key, None)


def public_sparse(row: Sparse) -> list[list[Any]]:
    return [[key.hex(), row[key] % 3] for key in sorted(row) if row[key] % 3]


def parse_sparse(rows: Sequence[Sequence[Any]]) -> Sparse:
    answer: Sparse = {}
    for raw, coefficient0 in rows:
        key = bytes.fromhex(str(raw)); coefficient = int(coefficient0)
        require(key not in answer and coefficient in (1, 2), "canonical sparse entry")
        answer[key] = coefficient
    require(public_sparse(answer) == [list(x) for x in rows], "sparse order")
    return answer


def pair(functional: Sparse, row: Sparse) -> int:
    return sum(value * row.get(key, 0) for key, value in functional.items()) % 3


class RowSpace:
    """Independent Gaussian implementation (not imported from producer)."""
    def __init__(self) -> None:
        self.pivots: list[bytes] = []; self.rows: dict[bytes, Sparse] = {}
        self.origins: dict[bytes, dict[int, int]] = {}

    @staticmethod
    def combine(left: dict[int, int], right: dict[int, int], scalar: int) -> None:
        for key, coefficient in right.items():
            value = (left.get(key, 0) + scalar * coefficient) % 3
            if value:
                left[key] = value
            else:
                left.pop(key, None)

    def reduce(self, source: Sparse) -> tuple[Sparse, dict[int, int]]:
        row = dict(source); solution: dict[int, int] = {}
        for pivot in self.pivots:
            coefficient = row.get(pivot, 0)
            if coefficient:
                add_scaled(row, self.rows[pivot], -coefficient)
                self.combine(solution, self.origins[pivot], coefficient)
        return row, solution

    def add(self, source: Sparse, column_id: int) -> tuple[bytes, dict[int, int]]:
        row = dict(source); origin = {column_id: 1}
        for pivot in self.pivots:
            coefficient = row.get(pivot, 0)
            if coefficient:
                add_scaled(row, self.rows[pivot], -coefficient)
                self.combine(origin, self.origins[pivot], -coefficient)
        require(row, "dependent retained column")
        pivot = min(row); inv = 1 if row[pivot] == 1 else 2
        row = {key: value * inv % 3 for key, value in row.items() if value * inv % 3}
        origin = {key: value * inv % 3 for key, value in origin.items() if value * inv % 3}
        require(pivot not in self.rows, "pivot collision")
        self.pivots.append(pivot); self.rows[pivot] = row; self.origins[pivot] = origin
        return pivot, origin

    def dual(self, target: Sparse) -> Sparse:
        remainder, _ = self.reduce(target); require(remainder, "dual after membership")
        functional: Sparse = {min(remainder): 1}
        for pivot in reversed(self.pivots):
            value = -sum(coefficient * functional.get(key, 0)
                         for key, coefficient in self.rows[pivot].items()
                         if key != pivot) % 3
            if value:
                functional[pivot] = value
        require(all(pair(functional, self.rows[pivot]) == 0 for pivot in self.pivots) and
                pair(functional, target) != 0, "independent exact dual")
        return functional


def parse_element(raw: bytes, block: int) -> Any:
    degree = 36 if block in (1, 2) else 144
    width = 4 if block in (1, 2) else 10
    require(len(raw) == degree + width, "element blob width")
    return (bytes(raw[:degree]), bytes(raw[degree:]))


def tagged_checker_row(checker: Any, row: dict[Any, int], block: int) -> Sparse:
    answer: Sparse = {}
    for component, raw, coefficient in checker.serial_row(row):
        key = row_key(block, int(component), bytes.fromhex(raw))
        answer[key] = int(coefficient)
    return answer


def independent_runtime() -> dict[str, Any]:
    checker = load_module(PINS["task175_checker"][0], "d179_independent_175")
    obj = checker.reconstruct({})
    require(len(obj["roster"]) == 6441 and len(obj["pb3_rows"]) == 2 and
            len(obj["pb4_rows"]) == 11, "independent task175 universe")
    return {"checker": checker, "obj": obj, "e3": obj["e3"], "e4": obj["e4"]}


def independent_target(runtime: dict[str, Any]) -> Sparse:
    answer: Sparse = {}
    for label, block in (("H1", 1), ("H2", 2), ("P", 3)):
        row = runtime["obj"]["raw_base_targets"][label]
        require(sha_obj(row["row"]) == row["sha256"], "independent target digest")
        source = {row_key(block, int(component), bytes.fromhex(raw)): int(coefficient)
                  for component, raw, coefficient in row["row"]}
        add_scaled(answer, source, -1)
    return answer


def boundary_row(runtime: dict[str, Any], block: int, index: int,
                 translation_hex: str) -> Sparse:
    quotient = runtime["e3"] if block in (1, 2) else runtime["e4"]
    sources = runtime["obj"]["pb3_rows"] if block in (1, 2) else runtime["obj"]["pb4_rows"]
    require(1 <= index <= len(sources), "independent boundary index")
    translation = parse_element(bytes.fromhex(translation_hex), block)
    translated = {(component, quotient.mul(translation, value)): coefficient
                  for (component, value), coefficient in sources[index - 1].items()}
    return tagged_checker_row(runtime["checker"], translated, block)


def direct_correction(runtime: dict[str, Any], delta: Sequence[int],
                      relator: Sequence[int]) -> tuple[Sparse, dict[str, Any]]:
    c = runtime["checker"]; obj = runtime["obj"]
    conjugate = c.reduce_word(tuple(delta) + tuple(relator) + c.inverse(delta))
    require(obj["joint"].eval(conjugate) == obj["joint"].identity,
            "independent joint-kernel conjugate")
    corrected = c.reduce_word(tuple(obj["g760"]) + conjugate)
    base_hex = c.hexagon_words(obj["g760"]); new_hex = c.hexagon_words(corrected)
    rows = []
    for block, quotient, base, new in (
            (1, runtime["e3"], c.embed_pb3(base_hex[0]), c.embed_pb3(new_hex[0])),
            (2, runtime["e3"], c.embed_pb3(base_hex[1]), c.embed_pb3(new_hex[1])),
            (3, runtime["e4"], c.pentagon_word(obj["g760"]), c.pentagon_word(corrected))):
        difference, base_value, new_value = c.raw_difference(quotient, base, new)
        require(base_value == quotient.identity and new_value == quotient.identity,
                "independent all-seven quotient replay")
        rows.append((block, tagged_checker_row(c, difference, block)))
    answer: Sparse = {}
    for _, row in rows:
        add_scaled(answer, row, 1)
    e1, e2 = exponent_pair(relator)
    if e1:
        answer[exponent_key(1)] = e1
    if e2:
        answer[exponent_key(2)] = e2
    return answer, {"conjugate_word": list(conjugate),
                    "corrected_word": list(corrected),
                    "all_seven_direct": True}


def independent_coordinates(runtime: dict[str, Any], word: Sequence[int]) -> list[str]:
    c = runtime["checker"]; e3, e4 = runtime["e3"], runtime["e4"]
    x, y = (1,), (2,); z = c.inverse(c.paper_product(x, y))
    u = c.inverse(c.paper_product(y, x))
    pairs = [(x, y), (x, z), (y, z), (u, x), (u, y)]
    values = [e3.eval(c.embed_pb3(c.f2_substitute(word, left, right)))
              for left, right in pairs]
    contexts = c.pentagon_context_words()
    for natural in (1, 3, 0, 2, 4):
        left, right = contexts[natural]
        values.append(e4.eval(c.f2_substitute(word, left, right)))
    return [c.element_blob(value).hex() for value in values]


def validate_selector_provenance(runtime: dict[str, Any], provenance: dict[str, Any],
                                 replay: dict[str, Any]) -> None:
    """Replay the chosen Q0 section without importing the producer index."""
    coordinate = int(provenance["coordinate"])
    require(0 <= coordinate < 10, "selector coordinate")
    require(1 <= int(provenance["q0_state_id"]) <= 1_469_664 and
            1 <= int(provenance["gamma_state_id"]) <= 243 and
            provenance.get("selection") == "least_qid_then_gid_coarse_inverse",
            "selector public ids/order")
    section_hex = provenance.get("section_blob_hex")
    require(type(section_hex) is list and len(section_hex) == 10,
            "selector complete section provenance")
    section_blobs = [bytes.fromhex(str(raw)) for raw in section_hex]
    require(all(len(raw) == (40 if i < 5 else 154)
                for i, raw in enumerate(section_blobs)),
            "selector section widths")
    q0_word = [int(x) for x in provenance["q0_source_word"]]
    gamma_word = [int(x) for x in provenance["gamma_source_word"]]
    source_word = reduce_word(gamma_word + q0_word)
    require(source_word == provenance["delta_word"], "selector source word")
    require(independent_coordinates(runtime, q0_word) == [x.hex() for x in section_blobs],
            "selector direct Q0 section replay")
    gamma_blobs = independent_coordinates(runtime, gamma_word)
    require(gamma_blobs[coordinate] == provenance["gamma_coordinate_blob_hex"],
            "selector Gamma coordinate replay")
    expected = independent_coordinates(runtime, source_word)
    require(expected == provenance["delta_coordinate_blobs_hex"],
            "selector ten-coordinate replay")
    block = 1 if coordinate < 5 else 3
    quotient = runtime["e3"] if coordinate < 5 else runtime["e4"]
    target = parse_element(bytes.fromhex(str(provenance["target_hex"])), block)
    gamma_value = parse_element(bytes.fromhex(gamma_blobs[coordinate]), block)
    section_value = parse_element(section_blobs[coordinate], block)
    require(quotient.mul(gamma_value, section_value) == target,
            "selector full packed target")


class IndependentCoarseInverse:
    """Checker-local collision test; no producer index helper is imported."""
    def __init__(self, store: bytearray, width: int, degree: int,
                 hash_fn: Any, table_length: int = 8):
        self.store = store; self.width = width; self.degree = degree
        self.hash_fn = hash_fn; self.table_length = table_length
        self.slots = array("I", [0]) * table_length
        require(self.slots.itemsize == 4, "checker uint32 itemsize")

    def coarse(self, qid: int) -> bytes:
        start = qid * self.width
        return bytes(self.store[start:start + self.degree])

    def build(self) -> None:
        for qid in range(len(self.store) // self.width):
            slot = self.hash_fn(self.coarse(qid)) & (self.table_length - 1)
            while self.slots[slot]:
                prior = int(self.slots[slot]) - 1
                if self.coarse(prior) == self.coarse(qid):
                    raise RuntimeError("duplicate exact coarse key")
                slot = (slot + 1) & (self.table_length - 1)
            self.slots[slot] = qid + 1

    def lookup(self, key: bytes) -> int | None:
        slot = self.hash_fn(key) & (self.table_length - 1)
        for _ in range(self.table_length):
            prior = int(self.slots[slot])
            if not prior:
                return None
            if self.coarse(prior - 1) == key:
                return prior - 1
            slot = (slot + 1) & (self.table_length - 1)
        return None


def independent_coarse_inverse_selftest() -> dict[str, Any]:
    width, degree = 3, 2
    store = bytearray(b"\x10\x01\xaa\x13\x02\xaa")
    inverse = IndependentCoarseInverse(store, width, degree, lambda _key: 0)
    inverse.build()
    require(inverse.lookup(b"\x13\x02") == 1 and
            inverse.lookup(b"\x10\x01") == 0,
            "checker coarse collision resolution")
    duplicate_rejected = False
    try:
        duplicate = IndependentCoarseInverse(
            bytearray(b"\x10\x01\xaa\x10\x01\xab"), width, degree,
            lambda _key: 0)
        duplicate.build()
    except RuntimeError as exc:
        duplicate_rejected = str(exc) == "duplicate exact coarse key"
    require(duplicate_rejected, "checker duplicate coarse rejection")
    hit = inverse.lookup(b"\x13\x02")
    mismatch_rejected = (hit is not None and
                         bytes(store[hit * width:(hit + 1) * width]) !=
                         b"\x13\x02\xab")
    require(mismatch_rejected, "checker full packed mismatch")
    target = b"\x11\x00\xaa"; candidates = []
    for a, gid in ((b"\x02\x02\x00", 4), (b"\x01\x01\x00", 8)):
        section_target = bytes(x ^ y for x, y in zip(a, target))
        qid = inverse.lookup(section_target[:degree])
        if qid is None:
            continue
        section_full = bytes(store[qid * width:(qid + 1) * width])
        if section_full != section_target or bytes(x ^ y for x, y in zip(a, section_full)) != target:
            continue
        candidates.append((qid, gid))
    selected = min(candidates, key=lambda pair: pair)
    require(selected == (0, 8), "checker least pair")
    return {"table_length": 8, "uint32_itemsize": inverse.slots.itemsize,
            "exact_key_collision_resolution": True,
            "duplicate_coarse_key_rejected": duplicate_rejected,
            "least_qid_gid_selection": list(selected),
            "full_packed_mismatch_rejected": mismatch_rejected,
            "hash": "injectable_constant_zero_only_selftest",
            "tables_not_production": True}


def independent_formula(runtime: dict[str, Any], relator: Sequence[int],
                        dual: Sparse) -> dict[str, Any]:
    c = runtime["checker"]; e3, e4 = runtime["e3"], runtime["e4"]
    g = runtime["obj"]["g760"]
    x, y = (1,), (2,); z = c.inverse(c.paper_product(x, y))
    u = c.inverse(c.paper_product(y, x))
    pcontexts = c.pentagon_context_words()
    specs: list[dict[str, Any]] = []
    for block, coordinate, quotient, left, right, sign, lift, label in (
            (1, 0, e3, x, y, 1, True, "H1_fxy"),
            (1, 1, e3, x, z, -1, True, "H1_fxz"),
            (1, 2, e3, y, z, 1, True, "H1_fyz"),
            (2, 3, e3, u, x, -1, True, "H2_fux"),
            (2, 0, e3, x, y, -1, True, "H2_fxy"),
            (2, 4, e3, u, y, 1, True, "H2_fuy")):
        specs.append({"block": block, "coordinate": coordinate, "quotient": quotient,
                      "left": left, "right": right, "sign": sign,
                      "lift": lift, "label": label})
    for natural, coordinate, label in ((1, 5, "P_b1"), (3, 6, "P_b2"),
                                       (0, 7, "P_b3"), (2, 8, "P_b5_inverse"),
                                       (4, 9, "P_b4_inverse")):
        left, right = pcontexts[natural]
        specs.append({"block": 3, "coordinate": coordinate, "quotient": e4,
                      "left": left, "right": right,
                      "sign": -1 if natural in (2, 4) else 1,
                      "lift": False, "label": label})
    for spec in specs:
        factor = c.f2_substitute(g, spec["left"], spec["right"])
        if spec["lift"]:
            factor = c.embed_pb3(factor)
        if spec["sign"] < 0:
            factor = c.inverse(factor)
        spec["base_factor"] = factor
    for block in (1, 2, 3):
        quotient = e3 if block in (1, 2) else e4
        indices = [i for i, spec in enumerate(specs) if spec["block"] == block]
        prefix = quotient.identity
        for index in reversed(indices):
            specs[index]["prefix"] = prefix
            prefix = quotient.mul(prefix, quotient.eval(specs[index]["base_factor"]))
        require(prefix == quotient.identity, "independent base prefix")
    # Rebuild the factor-internal Fox transport independently: positive
    # g_i*c_i slots contribute prefix*g_i*D(c_i), whereas inverse slots
    # contribute prefix*D(c_i^-1).
    for spec in specs:
        spec["occurrence_prefix"] = spec["prefix"]
        if spec["sign"] > 0:
            spec["occurrence_prefix"] = spec["quotient"].mul(
                spec["prefix"], spec["quotient"].eval(spec["base_factor"]))
    merged: dict[tuple[int, bytes], int] = {}; occurrences = []
    for ordinal, spec in enumerate(specs, 1):
        quotient = spec["quotient"]
        relation = c.f2_substitute(relator, spec["left"], spec["right"])
        if spec["lift"]:
            relation = c.embed_pb3(relation)
        if spec["sign"] < 0:
            relation = c.inverse(relation)
        gradient, value = c.fox(quotient, relation)
        require(value == quotient.identity, "independent occurrence identity")
        prefix_inverse = quotient.inverse(spec["occurrence_prefix"]); count = 0
        for (component, base_value), base_coefficient in gradient.items():
            base_inverse = quotient.inverse(base_value)
            for key, lambda_coefficient in dual.items():
                if key[:1] != b"R":
                    continue
                block, dual_component, target_raw = decode_row_key(key)
                if block != spec["block"] or dual_component != component:
                    continue
                target = parse_element(target_raw, block)
                required_value = quotient.mul(quotient.mul(prefix_inverse, target),
                                              base_inverse)
                raw = c.element_blob(required_value)
                merged_key = (spec["coordinate"], raw)
                contribution = base_coefficient * lambda_coefficient % 3
                merged[merged_key] = (merged.get(merged_key, 0) + contribution) % 3
                if not merged[merged_key]:
                    del merged[merged_key]
                count += 1
        occurrences.append({"ordinal": ordinal, "label": spec["label"],
                            "coordinate": spec["coordinate"],
                            "factor_sign": spec["sign"],
                            "raw_dual_pair_terms": count})
    exponents = exponent_pair(relator)
    constant = (dual.get(exponent_key(1), 0) * exponents[0] +
                dual.get(exponent_key(2), 0) * exponents[1]) % 3
    ordered = sorted(merged.items(), key=lambda item: (item[0][0], item[0][1]))
    return {"K": constant,
            "terms": [[coordinate, raw.hex(), coefficient]
                      for (coordinate, raw), coefficient in ordered],
            "same_target_merged_mod3": True, "zero_sums_deleted": True,
            "eleven_occurrences": occurrences}


def independent_weighted_support(formula: dict[str, Any]) -> dict[str, Any]:
    orders = (9, 9, 9, 9, 9, 1, 1, 1, 3, 3)
    targets = sorted(formula["terms"], key=lambda row: (int(row[0]), str(row[1])))
    distinct = [{"coordinate": int(coordinate), "target_hex": str(raw),
                 "kernel_order": orders[int(coordinate)]}
                for coordinate, raw, _coefficient in targets]
    return {"K": int(formula["K"]),
            "W": sum(row["kernel_order"] for row in distinct),
            "delta_order": 357_128_352,
                "kernel_orders": list(orders), "distinct_targets": distinct}


def validate_weighted_checkpoint_state(runtime: dict[str, Any],
                                       progress: dict[str, Any],
                                       dual: Sparse | None) -> None:
    """Shared validator for row states and the advanced completed-row cursor."""
    correction = progress["correction"]
    roster = runtime["obj"]["roster"]
    cursor = correction["canonical_row_cursor"]
    require(type(cursor) is int and 0 <= cursor <= len(roster),
            "weighted canonical cursor bounds")
    rows = correction["weighted_rows"]
    require(type(rows) is dict, "weighted checkpoint rows map")
    orders = [9, 9, 9, 9, 9, 1, 1, 1, 3, 3]
    for key, state in rows.items():
        require(type(key) is str and key.isdecimal() and str(int(key)) == key,
                "weighted checkpoint row key")
        index = int(key)
        require(1 <= index <= len(roster) and type(state) is dict,
                "weighted checkpoint row index")
        require(type(state.get("formula_sha256")) is str and
                type(state.get("K")) is int and state["K"] in (0, 1, 2) and
                type(state.get("W")) is int and state["W"] >= 0 and
                state.get("delta_order") == 357_128_352 and
                state.get("kernel_orders") == orders and
                type(state.get("support_fibre_cursor")) is int and
                type(state.get("kernel_cursor")) is int and
                type(state.get("global_prefix")) is int and
                type(state.get("complete")) is bool,
                "weighted row checkpoint state")
        require(state["support_fibre_cursor"] >= 0 and
                state["kernel_cursor"] >= 0 and
                state["global_prefix"] >= 0 and
                state["kernel_cursor"] <= max(orders) and
                state["global_prefix"] <= 357_128_352,
                "weighted row cursor bounds")
        if dual is not None:
            formula = independent_formula(runtime, roster[index - 1]["word"], dual)
            support = independent_weighted_support(formula)
            require(state["formula_sha256"] == sha_obj(formula) and
                    state["K"] == support["K"] and state["W"] == support["W"],
                    "weighted row formula identity")
            target_bound = max(len(support["distinct_targets"]) - 1, 0)
            require(state["support_fibre_cursor"] <= target_bound,
                    "weighted support cursor bound")
            if support["K"] == 0:
                require(state["global_prefix"] == 0,
                        "K=0 global cursor must be zero")
                targets = support["distinct_targets"]
                if not targets:
                    require(state["support_fibre_cursor"] == 0 and
                            state["kernel_cursor"] == 0,
                            "empty K=0 support cursor state")
                else:
                    current_order = targets[state["support_fibre_cursor"]][
                        "kernel_order"]
                    require(state["kernel_cursor"] <= current_order,
                            "K=0 coordinate kernel cursor bound")
                    if state["complete"]:
                        require(state["support_fibre_cursor"] == target_bound and
                                state["kernel_cursor"] in (0, current_order),
                                "completed K=0 cursor state")
            else:
                global_bound = (support["W"] + 1
                                if support["W"] < 357_128_352
                                else 357_128_352)
                require(state["support_fibre_cursor"] == 0 and
                        state["kernel_cursor"] == 0 and
                        state["global_prefix"] <= global_bound,
                        "K!=0 weighted cursor state")
            if state["complete"]:
                require(support["K"] == 0 and
                        state["support_fibre_cursor"] >= target_bound,
                        "completed weighted row state")
        if index <= cursor:
            require(state["complete"] is True,
                    "completed cursor crossed incomplete row")
        else:
            require(index == cursor + 1 and state["complete"] is False,
                    "future weighted row state")
    for index in range(1, cursor + 1):
        require(str(index) in rows and rows[str(index)].get("complete") is True,
                "missing completed weighted row")


def replay_columns(runtime: dict[str, Any], target: Sparse,
                   columns: Sequence[dict[str, Any]]) -> tuple[RowSpace, list[Sparse]]:
    basis = RowSpace(); rebuilt: list[Sparse] = []
    for column_id, record in enumerate(columns, 1):
        require(record.get("column_id") == column_id and
                record.get("rank_before") == column_id - 1 and
                record.get("rank_after") == column_id, "column order/rank")
        provenance = record.get("provenance", {})
        if record.get("family") == "boundary":
            require(provenance.get("family") == "boundary", "boundary family")
            row = boundary_row(runtime, int(provenance["block"]),
                               int(provenance["base_relator_index"]),
                               provenance["translation_hex"])
            # Recheck the left-action orientation on every literal occurrence.
            quotient = runtime["e3"] if int(provenance["block"]) in (1, 2) else runtime["e4"]
            translation = parse_element(bytes.fromhex(provenance["translation_hex"]),
                                        int(provenance["block"]))
            sources = runtime["obj"]["pb3_rows"] if int(provenance["block"]) in (1, 2) else runtime["obj"]["pb4_rows"]
            source_row = sources[int(provenance["base_relator_index"]) - 1]
            for contributor in provenance.get("contributing_pairs", []):
                h = parse_element(bytes.fromhex(contributor["h_hex"]),
                                  int(provenance["block"]))
                g = parse_element(bytes.fromhex(contributor["g_hex"]),
                                  int(provenance["block"]))
                require(any(component == int(contributor["component"]) and value == h
                            for (component, value) in source_row),
                        "boundary contributor occurrence")
                require(quotient.mul(translation, h) == g, "boundary t*h=g")
        elif record.get("family") == "correction":
            require(provenance.get("family") == "correction", "correction family")
            roster_index = int(provenance["roster_index"])
            roster = runtime["obj"]["roster"][roster_index - 1]
            require(provenance["relator_word"] == roster["word"] and
                    provenance["layer"] == roster["layer"] and
                    int(provenance["ordinal"]) == int(roster["ordinal"]),
                    "literal roster provenance")
            row, replay = direct_correction(runtime, provenance["delta_word"],
                                            provenance["relator_word"])
            require(replay["conjugate_word"] == provenance["conjugate_word"] and
                    independent_coordinates(runtime, provenance["delta_word"]) ==
                    provenance["delta_coordinate_blobs_hex"],
                    "literal delta/conjugate/context replay")
            selector = provenance.get("section_provenance")
            if isinstance(selector, dict) and "section_blob_hex" in selector:
                selector = dict(selector)
                selector["delta_word"] = provenance["delta_word"]
                selector["delta_coordinate_blobs_hex"] = provenance[
                    "delta_coordinate_blobs_hex"]
                validate_selector_provenance(runtime, selector, replay)
        else:
            raise RuntimeError("unknown column family")
        require(public_sparse(row) == record["sparse_row"] and
                record["sparse_row_sha256"] == sha_obj(record["sparse_row"]),
                "retained sparse row")
        active_dual = record.get("active_dual")
        if active_dual is not None:
            dual = parse_sparse(active_dual)
            require(record["active_dual_sha256"] == sha_obj(active_dual) and
                    dual == basis.dual(target) and record["dual_pairing"] == pair(dual, row) != 0,
                    "ACTIVE dual/rank gate")
            if record["family"] == "correction":
                expected_formula = independent_formula(runtime,
                    record["provenance"]["relator_word"], dual)
                require(expected_formula == record["provenance"]["weighted_formula"],
                        "independent full weighted formula")
                weighted = independent_weighted_support(expected_formula)
                require(record["provenance"].get("support_hitting") == weighted,
                        "independent weighted support bound")
                schedule = record["provenance"].get("schedule")
                selector_meta = record["provenance"].get("section_provenance", {})
                if weighted["K"] == 0:
                    require(schedule == "weighted_support_fibre_complete",
                            "K=0 support-fibre schedule")
                    require(any(int(row["coordinate"]) == int(selector_meta["coordinate"]) and
                                row["target_hex"] == selector_meta["target_hex"]
                                for row in weighted["distinct_targets"]) and
                            0 <= int(selector_meta["kernel_cursor"]) <
                                weighted["kernel_orders"][int(selector_meta["coordinate"])],
                            "K=0 complete kernel candidate")
                elif weighted["W"] < weighted["delta_order"]:
                    require(schedule == "weighted_global_prefix_W_plus_1" and
                            int(record["provenance"]["section_provenance"][
                                "global_cursor"]) <= weighted["W"],
                            "K!=0 W+1 global schedule")
                else:
                    require(schedule == "weighted_global_fair_fallback",
                            "typed global fallback schedule")
                coords = [bytes.fromhex(x) for x in
                          record["provenance"]["delta_coordinate_blobs_hex"]]
                scalar = expected_formula["K"]
                for coordinate, raw_hex, coefficient in expected_formula["terms"]:
                    if coords[int(coordinate)] == bytes.fromhex(raw_hex):
                        scalar += int(coefficient)
                require(scalar % 3 == record["dual_pairing"],
                        "full merged eleven-term scalar")
            else:
                block = int(provenance["block"])
                quotient = runtime["e3"] if block in (1, 2) else runtime["e4"]
                translation = parse_element(bytes.fromhex(provenance["translation_hex"]), block)
                sources = (runtime["obj"]["pb3_rows"] if block in (1, 2)
                           else runtime["obj"]["pb4_rows"])
                source_row = sources[int(provenance["base_relator_index"]) - 1]
                expected_contributors = []
                for (component, h), base_coefficient in source_row.items():
                    h_inverse = quotient.inverse(h)
                    for dual_key, lambda_coefficient in dual.items():
                        if dual_key[:1] != b"R":
                            continue
                        dual_block, dual_component, g_raw = decode_row_key(dual_key)
                        if dual_block != block or dual_component != component:
                            continue
                        g = parse_element(g_raw, block)
                        candidate_translation = quotient.mul(g, h_inverse)
                        require(quotient.mul(candidate_translation, h) == g,
                                "independent t=g*h^-1 gate")
                        if candidate_translation == translation:
                            expected_contributors.append({
                                "component": int(component), "g_hex": g_raw.hex(),
                                "h_hex": runtime["checker"].element_blob(h).hex(),
                                "lambda_coefficient": int(lambda_coefficient),
                                "base_coefficient": int(base_coefficient) % 3})
                order = lambda row: (row["component"], row["g_hex"], row["h_hex"],
                                     row["lambda_coefficient"], row["base_coefficient"])
                claimed = provenance.get("contributing_pairs", [])
                require(sorted(expected_contributors, key=order) == sorted(claimed, key=order) and
                        sum(row["lambda_coefficient"] * row["base_coefficient"]
                            for row in expected_contributors) % 3 ==
                            provenance.get("scalar") == record["dual_pairing"],
                        "complete typed boundary correlation")
        pivot, ancestry = basis.add(row, column_id)
        require(record["pivot_hex"] == pivot.hex() and
                record["pivot_ancestry"] == [[key, value]
                                             for key, value in sorted(ancestry.items())],
                "pivot/ancestry replay")
        rebuilt.append(row)
    return basis, rebuilt


def validate_checkpoint(runtime: dict[str, Any], target: Sparse,
                        checkpoint: dict[str, Any], expected_pins: dict[str, Any],
                        receipt_input: str | None = None) -> tuple[RowSpace, list[Sparse]]:
    validate_seal(checkpoint)
    require(checkpoint.get("schema") == CHECKPOINT_SCHEMA and
            checkpoint.get("pins_sha256") == sha_obj(expected_pins) and
            checkpoint.get("input_sha256") == sha_obj(checkpoint.get("input_components")) and
            parse_sparse(checkpoint.get("target", [])) == target and
            checkpoint.get("target_sha256") == sha_obj(checkpoint["target"]),
            "checkpoint input/target")
    require(checkpoint.get("input_components", {}).get(
                "authenticated_module_import") == module_import_control_public(),
            "checkpoint authenticated module reuse")
    index_meta = checkpoint.get("coarse_inverse_index", {})
    require(index_meta.get("state_count") == 1_469_664 and
            index_meta.get("table_length") == (1 << 22) and
            index_meta.get("uint32_itemsize") == 4 and
            index_meta.get("payload_bytes_total") == 167_772_160 and
            index_meta.get("injectivity") ==
                "hard_stop_on_duplicate_exact_coarse_key",
            "checkpoint coarse inverse metadata")
    require(checkpoint.get("weighted_support_hitting") == {
        "delta_order": 357_128_352,
        "kernel_orders": [9, 9, 9, 9, 9, 1, 1, 1, 3, 3],
        "schedule": "K0_complete_fibres_or_Knonzero_W_plus_1_global"},
        "checkpoint weighted selector metadata")
    if receipt_input is not None:
        require(checkpoint.get("input_sha256") == receipt_input,
                "checkpoint/receipt input binding")
    basis, rows = replay_columns(runtime, target, checkpoint.get("columns", []))
    remainder, solution = basis.reduce(target)
    require(public_sparse(remainder) == checkpoint.get("reduced_target") and
            checkpoint.get("rank") == len(basis.pivots) and
            checkpoint.get("pivot_order") == [key.hex() for key in basis.pivots] and
            checkpoint.get("pivot_rows_sha256") == sha_obj(
                [public_sparse(basis.rows[key]) for key in basis.pivots]) and
            checkpoint.get("target_solution_if_zero") ==
                [[key, value] for key, value in sorted(solution.items())],
            "checkpoint rowspace replay")
    current = checkpoint.get("current_dual")
    dual: Sparse | None = None
    if current is not None:
        dual = parse_sparse(current)
        require(current == public_sparse(basis.dual(target)) and
                checkpoint.get("current_dual_sha256") == sha_obj(current),
                "checkpoint current dual")
    elif remainder:
        dual = basis.dual(target)
    progress = checkpoint.get("progress", {})
    require(set(progress) == {"boundary", "correction"} and
            progress["boundary"].get("complete") in (True, False) and
            type(progress["correction"].get("canonical_row_cursor")) is int and
            type(progress["correction"].get("kernel_prefix")) is int and
            type(progress["correction"].get("global_cursors")) is dict and
            type(progress["correction"].get("live_fibres")) is list and
            type(progress["correction"].get("weighted_rows")) is dict and
            progress["correction"].get("live_fibre_count") ==
                len(progress["correction"].get("live_fibres")),
            "checkpoint oracle cursors")
    if remainder:
        require(dual is not None and
                progress["correction"].get("dual_sha256") ==
                sha_obj(public_sparse(dual)),
                "checkpoint correction dual digest")
    validate_weighted_checkpoint_state(runtime, progress, dual)
    monitor = checkpoint.get("monitor", {}); limits = monitor.get("limits", {})
    counters = monitor.get("counters", {})
    require(all(name in limits for name in ("wall_seconds", "boundary_pairs",
        "fibre_scans", "candidate_words", "retained_columns",
        "checkpoint_bytes", "rss_bytes", "oracle_rounds", "global_roster")) and
        all(int(value) >= 0 for value in counters.values()) and
        checkpoint.get("negative_claim") is False and checkpoint.get("separator") is False,
        "checkpoint resource/claim boundary")
    return basis, rows


def validate_common(runtime: dict[str, Any], receipt: dict[str, Any],
                    expected_pins: dict[str, Any]) -> dict[str, Any]:
    require(receipt.get("status") == "COMMON_WORD" and receipt.get("terminal") == COMMON and
            receipt.get("pins") == expected_pins and receipt.get("negative_claim") is False and
            receipt.get("separator") is False, "COMMON envelope")
    target = independent_target(runtime)
    require(parse_sparse(receipt.get("target", [])) == target and
            receipt.get("input_sha256") == sha_obj(receipt.get("input_components")) and
            receipt.get("target_source") ==
            "negative task175 raw_base_targets H1/H2/P; never stacked_target",
            "exact target/canary separation")
    require(receipt.get("input_components", {}).get(
                "authenticated_module_import") == module_import_control_public(),
            "COMMON authenticated module reuse")
    index_meta = receipt.get("input_components", {}).get("coarse_inverse_index", {})
    require(index_meta.get("state_count") == 1_469_664 and
            index_meta.get("coordinate_count") == 10 and
            index_meta.get("table_length") == (1 << 22) and
            index_meta.get("payload_bytes_total") == 167_772_160 and
            index_meta.get("uint32_itemsize") == 4 and
            index_meta.get("tables_not_serialized") is True,
            "COMMON coarse inverse metadata")
    require(receipt["input_components"].get("delta_order") == 357_128_352 and
            receipt["input_components"].get("kernel_orders") ==
                [9, 9, 9, 9, 9, 1, 1, 1, 3, 3],
            "COMMON finite kernel order metadata")
    require(receipt.get("weighted_support_hitting") == {
        "delta_order": 357_128_352,
        "kernel_orders": [9, 9, 9, 9, 9, 1, 1, 1, 3, 3],
        "schedule": "K0_complete_fibres_or_Knonzero_W_plus_1_global"},
        "COMMON weighted selector metadata")
    basis, rows = replay_columns(runtime, target, receipt.get("columns", []))
    remainder, solution = basis.reduce(target)
    require(not remainder and receipt.get("solution_coefficients") ==
            [[key, value] for key, value in sorted(solution.items())],
            "COMMON sparse membership")
    combined: Sparse = {}; correction_sum: Sparse = {}; boundary_sum: Sparse = {}
    correction_word: list[int] = []; selected_expected = []; boundary_expected = []
    for column_id in sorted(solution):
        coefficient = solution[column_id]; record = receipt["columns"][column_id - 1]
        add_scaled(combined, rows[column_id - 1], coefficient)
        if record["family"] == "boundary":
            add_scaled(boundary_sum, rows[column_id - 1], coefficient)
            boundary_expected.append({"column_id": column_id, "coefficient": coefficient,
                                      "provenance": record["provenance"]})
        else:
            add_scaled(correction_sum, rows[column_id - 1], coefficient)
            conjugate = record["provenance"]["conjugate_word"]
            factor = list(conjugate) if coefficient == 1 else inverse_word(conjugate)
            require(runtime["obj"]["joint"].eval(factor) ==
                    runtime["obj"]["joint"].identity, "selected joint kernel factor")
            inverse_replay = False
            if coefficient == 2:
                inverse_row, inverse_public = direct_correction(
                    runtime, record["provenance"]["delta_word"],
                    inverse_word(record["provenance"]["relator_word"]))
                expected_negative = {key: -value % 3 for key, value in
                                     rows[column_id - 1].items()}
                require(inverse_row == expected_negative and
                        inverse_public["conjugate_word"] == factor,
                        "independent coefficient-two inverse column")
                inverse_replay = True
            correction_word = reduce_word(correction_word + factor)
            selected_expected.append({"column_id": column_id, "coefficient": coefficient,
                "factor_word": factor, "inverse_for_coefficient_2": coefficient == 2,
                "inverse_column_replay": inverse_replay,
                "provenance": record["provenance"]})
    require(combined == target and receipt.get("boundary_chains") == boundary_expected and
            receipt.get("selected_corrections") == selected_expected,
            "selected column provenance")
    require(receipt.get("correction_word") == correction_word and
            exponent_pair(correction_word) == (0, 0) and
            receipt.get("exponent_sums_mod3") == [0, 0] and
            receipt.get("coefficient_2_uses_inverse") is True and
            receipt.get("boundary_words_not_inserted") is True,
            "literal correction product")
    direct, replay = direct_correction(runtime, [], correction_word)
    require(direct == correction_sum and
            receipt.get("corrected_word") == replay["corrected_word"] ==
            reduce_word(list(runtime["obj"]["g760"]) + correction_word),
            "right corrected word/direct additivity")
    base = {key: -value % 3 for key, value in target.items()}
    residual = dict(base); add_scaled(residual, correction_sum, 1)
    add_scaled(residual, boundary_sum, 1)
    require(not residual, "two PB3 plus eleven PB4 boundary chains")
    checkpoint = receipt.get("checkpoint", {})
    checkpoint_basis, _ = validate_checkpoint(runtime, target, checkpoint,
                                               expected_pins, receipt.get("input_sha256"))
    require(checkpoint.get("columns") == receipt.get("columns") and
            len(checkpoint_basis.pivots) == receipt.get("rank") == len(basis.pivots),
            "COMMON checkpoint binding")
    boundaries = receipt.get("boundaries", {})
    require(boundaries == {"cofinal_lift": False, "fake": False,
                           "ihara_witness": False, "v129_input_only": True},
            "finite claim boundary")
    return {"terminal": COMMON, "rank": len(basis.pivots),
            "selected_corrections": len(selected_expected),
            "boundary_columns": len(boundary_expected),
            "helper_nonshared": True}


def validate_unknown(runtime: dict[str, Any] | None, receipt: dict[str, Any],
                     expected_pins: dict[str, Any], receipt_path: Path) -> dict[str, Any]:
    terminal = str(receipt.get("terminal", ""))
    require(receipt.get("status") == "UNKNOWN" and
            (terminal.startswith("UNKNOWN_RESOURCE:") or terminal.startswith("UNKNOWN_INPUT:")) and
            receipt.get("positive_claim") is False and receipt.get("negative_claim") is False and
            receipt.get("separator") is False and receipt.get("correction_word") is None and
            receipt.get("common_word") is None and receipt.get("pins") == expected_pins,
            "typed UNKNOWN envelope")
    require("TypeError" not in terminal and "ValueError" not in terminal and
            "Traceback" not in terminal, "programming exception relabelled UNKNOWN")
    monitor = receipt.get("monitor")
    require(type(monitor) is dict and monitor.get("single_process") is True,
            "UNKNOWN monitor")
    limits = monitor.get("limits")
    require(type(limits) is dict, "UNKNOWN monitor limits")
    if terminal.startswith("UNKNOWN_RESOURCE:"):
        match = re.fullmatch(
            r"UNKNOWN_RESOURCE:phase=([^:]+):cap=([^:]+):value="
            r"([-+]?(?:\d+(?:\.\d*)?|\.\d+)):limit="
            r"([-+]?(?:\d+(?:\.\d*)?|\.\d+))", terminal)
        require(match is not None, "UNKNOWN_RESOURCE receipt fields")
        phase, cap, value_text, limit_text = match.groups()
        require(phase and cap in limits, "UNKNOWN_RESOURCE registered cap")
        value = float(value_text); limit = float(limit_text)
        registered = limits[cap]
        require(math.isfinite(value) and math.isfinite(limit) and
                limit == float(registered) and value > limit,
                "UNKNOWN_RESOURCE cap/value binding")
    checkpoint_ref = receipt.get("checkpoint")
    replay_rank = 0
    if checkpoint_ref is not None:
        require(runtime is not None, "UNKNOWN checkpoint requires arithmetic replay")
        path = receipt_path.parent / checkpoint_ref["path"]
        raw = path.read_bytes()
        require(len(raw) == checkpoint_ref["bytes"] and
                sha_bytes(raw) == checkpoint_ref["sha256"], "UNKNOWN checkpoint sidecar")
        checkpoint = json.loads(raw.decode("ascii"))
        target = independent_target(runtime)
        basis, _ = validate_checkpoint(runtime, target, checkpoint, expected_pins)
        replay_rank = len(basis.pivots)
    require(receipt.get("boundaries") == {"finite_common_word": False,
        "cofinal_lift": False, "fake": False, "ihara_witness": False},
        "UNKNOWN claim boundary")
    return {"terminal": terminal, "checkpoint_rank": replay_rank,
            "positive_claim": False, "negative_claim": False}


# Independent S3 SELFTEST arithmetic.
def p_mul(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[i]] for i in range(len(a)))


def p_inv(a: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(a)
    for i, value in enumerate(a):
        out[value] = i
    return tuple(out)


def p_eval(word: Sequence[int], generators: Sequence[tuple[int, ...]]) -> tuple[int, ...]:
    value = tuple(range(3))
    for letter in word:
        generator = generators[abs(int(letter)) - 1]
        value = p_mul(value, generator if letter > 0 else p_inv(generator))
    return value


def independent_toy_fox(word: Sequence[int], generators: Sequence[tuple[int, ...]],
                        block: int) -> Sparse:
    value = tuple(range(3)); answer: Sparse = {}
    for letter0 in word:
        letter = int(letter0); generator = generators[abs(letter) - 1]
        if letter > 0:
            key_value = value; coefficient = 1; value = p_mul(value, generator)
        else:
            value = p_mul(value, p_inv(generator)); key_value = value; coefficient = 2
        key = row_key(block, abs(letter), bytes(key_value))
        answer[key] = (answer.get(key, 0) + coefficient) % 3
        if not answer[key]:
            del answer[key]
    return answer


def independent_toy_column(fixture: dict[str, Any], delta: Sequence[int],
                           relator: Sequence[int]) -> tuple[Sparse, list[dict[str, Any]]]:
    generators = [tuple(x) for x in fixture["generators"]]
    require(p_eval(relator, generators) == tuple(range(3)), "toy relator")
    conjugate = reduce_word(list(delta) + list(relator) + inverse_word(delta))
    base = independent_toy_fox(conjugate, generators, 1)
    prefixes = [tuple(range(3)), generators[0], p_mul(generators[0], generators[1])]
    answer: Sparse = {}; public = []
    for ordinal, prefix in enumerate(prefixes, 1):
        row: Sparse = {}
        for key, coefficient in base.items():
            block, component, raw = decode_row_key(key)
            row[row_key(block, component, bytes(p_mul(prefix, tuple(raw))))] = coefficient
        add_scaled(answer, row, 1)
        public.append({"ordinal": ordinal, "prefix": list(prefix),
                       "row": public_sparse(row)})
    e1, e2 = exponent_pair(relator)
    if e1:
        answer[exponent_key(1)] = e1
    if e2:
        answer[exponent_key(2)] = e2
    return answer, public


def validate_selftest(fixture: dict[str, Any], cert: dict[str, Any]) -> None:
    validate_seal(cert)
    require(cert.get("schema") == "d972-r07-positive-common-word-colgen-selftest-output/v1" and
            cert.get("terminal") == COMMON and cert.get("separator") is False and
            cert.get("negative_claim") is False and cert.get("fixture_sha256") == FIXTURE_SHA256,
            "SELFTEST envelope")
    require(cert.get("module_import_control") == module_import_control_public(),
            "SELFTEST producer double/cross import control")
    require(cert.get("coarse_inverse") == independent_coarse_inverse_selftest(),
            "SELFTEST independent coarse inverse")
    weighted = cert.get("weighted_support", {})
    require(weighted.get("K0_last_point") == {
        "kernel_order": 3, "hit_index": 2, "tested": [0, 0, 1]} and
        weighted.get("K0_exhaustion") == {
            "kernel_order": 3, "tested": [0, 0, 0], "row_skipped": True},
        "SELFTEST independent K0 fibres")
    global_case = weighted.get("Knonzero_W_plus_1", {})
    require(global_case.get("K") in (1, 2) and global_case.get("W") == 2 and
            global_case.get("global_points") == [0, 1, 2] and
            global_case.get("hit_index") == 2 and
            len(set(global_case["global_points"])) == 3,
            "SELFTEST independent W+1")
    gate = weighted.get("kernel_order_gate", {})
    require(gate.get("registered") == [9, 9, 9, 9, 9, 1, 1, 1, 3, 3] and
            gate.get("overstated_rejected") is True and
            gate.get("understated_rejected") is True,
            "SELFTEST independent kernel gate")
    merged = weighted.get("merged_target_W", {})
    require(merged.get("full") == 18 and merged.get("omitted") == 9 and
            merged.get("omitted_target_rejected") is True,
            "SELFTEST independent merged W")
    distinct = weighted.get("global_distinctness", {})
    require(distinct.get("repeated") == [0, 1, 1] and
            distinct.get("repeated_rejected") is True,
            "SELFTEST independent global distinctness")
    cursor = weighted.get("completed_cursor", {})
    require(cursor.get("tested") == 3 and cursor.get("cursor") == 3 and
            cursor.get("advanced_past_untested_rejected") is True,
            "SELFTEST independent cursor")
    impossible = weighted.get("W_plus_1_impossible", {})
    require(impossible.get("typed_unknown") is False and
            impossible.get("hard_invariant_failure") is True,
            "SELFTEST independent W+1 invariant failure")
    require(cert.get("target_source") == "toy_raw_base_targets_not_canary",
            "SELFTEST target/canary separation")
    generators = [tuple(x) for x in fixture["generators"]]
    require(p_mul(generators[0], generators[1]) != p_mul(generators[1], generators[0]),
            "SELFTEST noncommutative")
    support = cert["support"]
    delta = reduce_word(support["kernel_prefix_word"] + support["section_word"])
    require(delta == support["delta_word"], "SELFTEST linked section/kernel")
    conjugate = reduce_word(delta + support["relator_word"] + inverse_word(delta))
    require(conjugate == support["conjugate_word"], "SELFTEST conjugation")
    support_row, occurrences = independent_toy_column(fixture, delta,
                                                      support["relator_word"])
    require(occurrences == support["occurrences"] and len(occurrences) == 3 and
            support["same_target_merged_before_scalar"] is True and
            support["full_scalar_not_single_occurrence"] is True and
            support["selected_coefficient"] == 2 and
            support["selected_factor_word"] == inverse_word(conjugate),
            "SELFTEST full occurrence/coefficient2")
    global_row, global_occurrences = independent_toy_column(
        fixture, cert["global"]["word"], cert["global"]["relator_word"])
    require(cert["global"]["K_nonzero"] is True and
            cert["global"]["occurrences"] == global_occurrences and
            exponent_pair(cert["global"]["relator_word"]) != (0, 0),
            "SELFTEST K global")
    boundary = cert["boundary"]
    base = independent_toy_fox(boundary["relation_word"], generators,
                               int(boundary["block"]))
    translation = tuple(boundary["translation"]); boundary_row: Sparse = {}
    for key, coefficient in base.items():
        block, component, raw = decode_row_key(key)
        boundary_row[row_key(block, component, bytes(p_mul(translation, tuple(raw))))] = coefficient
    require(public_sparse(boundary_row) == boundary["row"] and
            boundary["not_inserted_in_correction_word"] is True,
            "SELFTEST boundary ACTIVE")
    target = parse_sparse(cert["target"])
    row_by_family = {"boundary": boundary_row,
                     "support_fibre_kernel_prefix": support_row,
                     "K_nonzero_global": global_row}
    require(len(cert.get("columns", [])) == 3, "SELFTEST retained column count")
    basis = RowSpace()
    for index, record in enumerate(cert["columns"], 1):
        require(record.get("family") in row_by_family, "SELFTEST column family")
        row = row_by_family[record["family"]]
        dual = basis.dual(target)
        require(record["column_id"] == index and record["row"] == public_sparse(row) and
                record["dual"] == public_sparse(dual) and
                record["full_scalar"] == pair(dual, row) != 0,
                "SELFTEST dual/full scalar")
        pivot, ancestry = basis.add(row, index)
        require(record["pivot_hex"] == pivot.hex() and record["rank_after"] == index and
                record["ancestry"] == [[k, v] for k, v in sorted(ancestry.items())],
                "SELFTEST rank")
    remainder, solution = basis.reduce(target)
    require(not remainder and cert["solution_coefficients"] ==
            [[key, value] for key, value in sorted(solution.items())], "SELFTEST membership")
    product = cert["ordered_product"]
    require(product["indices"] == fixture["ordered_product_indices"] and
            product["words"] == fixture["ordered_product_words"], "SELFTEST factor roster")
    product_word = reduce_word(letter for index in product["indices"]
                               for letter in product["words"][index])
    require(product["product_word"] == product_word and
            p_eval(product_word, generators) == tuple(range(3)),
            "SELFTEST ordered product")
    checkpoint = cert["checkpoint"]; validate_seal(checkpoint)
    require(checkpoint["target"] == cert["target"] and checkpoint["columns"] == cert["columns"] and
            checkpoint["pending_prefix"] == {"support_fibre": 2, "kernel_power": 2,
                                             "global_cursor": 1} and
            checkpoint["separator"] is False, "SELFTEST checkpoint")


def independent_selftest_mutations(fixture: dict[str, Any], cert: dict[str, Any]) -> int:
    actions = [
        lambda x: x["support"]["delta_word"].append(2),
        lambda x: x["support"].__setitem__("conjugate_word",
            reduce_word(inverse_word(x["support"]["delta_word"]) +
                        x["support"]["relator_word"] + x["support"]["delta_word"])),
        lambda x: x["support"]["occurrences"].pop(),
        lambda x: x["support"].__setitem__("same_target_merged_before_scalar", False),
        lambda x: x["support"].__setitem__("full_scalar_not_single_occurrence", False),
        lambda x: x["columns"].append(copy.deepcopy(x["columns"][0])),
        lambda x: x["columns"][1].__setitem__("rank_after", 9),
        lambda x: x.__setitem__("target_source", "stacked_target"),
        lambda x: x["support"].__setitem__("selected_factor_word",
                                           x["support"]["conjugate_word"]),
        lambda x: x["boundary"].__setitem__("not_inserted_in_correction_word", False),
        lambda x: x["boundary"].__setitem__("block", 1),
        lambda x: x["ordered_product"]["indices"].reverse(),
        lambda x: x["checkpoint"]["pending_prefix"].__setitem__("global_cursor", 8),
        lambda x: x.__setitem__("separator", True),
        lambda x: x.__setitem__("terminal", "UNKNOWN_RESOURCE:TypeError"),
    ]
    rejected = 0
    for ordinal, action in enumerate(actions, 1):
        candidate = copy.deepcopy(cert); action(candidate)
        if ordinal == 13:
            candidate["checkpoint"] = seal(candidate["checkpoint"])
        candidate = seal(candidate)
        try:
            validate_selftest(fixture, candidate)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError(f"checker mutation accepted:{ordinal}")
    require(rejected == 15, "checker fifteen mutations")
    return rejected


def independent_weighted_mutations(fixture: dict[str, Any], cert: dict[str, Any]) -> int:
    actions = [
        lambda x: x["weighted_support"]["K0_last_point"].__setitem__("kernel_order", 4),
        lambda x: x["weighted_support"]["K0_exhaustion"].__setitem__("row_skipped", False),
        lambda x: x["weighted_support"]["Knonzero_W_plus_1"].__setitem__("hit_index", 1),
        lambda x: x["weighted_support"]["kernel_order_gate"]["registered"].__setitem__(0, 8),
        lambda x: x["weighted_support"]["merged_target_W"].__setitem__("omitted_target_rejected", False),
        lambda x: x["weighted_support"]["global_distinctness"].__setitem__("repeated_rejected", False),
        lambda x: x["weighted_support"]["completed_cursor"].__setitem__("cursor", 4),
        lambda x: x["weighted_support"]["W_plus_1_impossible"].__setitem__(
            "typed_unknown", True),
    ]
    rejected = 0
    for ordinal, action in enumerate(actions, 1):
        candidate = copy.deepcopy(cert); action(candidate); candidate = seal(candidate)
        try:
            validate_selftest(fixture, candidate)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError(f"checker weighted mutation accepted:{ordinal}")
    require(rejected == 8, "checker eight weighted mutations")
    return rejected


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"), required=True)
    value.add_argument("--receipt", type=Path, required=True)
    value.add_argument("--verdict", type=Path, required=True)
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value) + b"\n")


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    receipt_path = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    verdict_path = args.verdict if args.verdict.is_absolute() else ROOT / args.verdict
    checker_pins = authenticate()
    expected_pins = {name: value for name, value in checker_pins.items()
                     if name != "producer"}
    receipt = json.loads(receipt_path.read_text(encoding="ascii")); validate_seal(receipt)
    if args.mode == "SELFTEST":
        fixture = json.loads(FIXTURE.read_text(encoding="ascii"))
        require(module_import_selftest() == receipt.get("module_import_control"),
                "independent double/cross import control")
        validate_selftest(fixture, receipt)
        rejected = independent_selftest_mutations(fixture, receipt)
        weighted_rejected = independent_weighted_mutations(fixture, receipt)
        require(receipt.get("mutation_results", {}).get("attempted") == 15 and
                receipt["mutation_results"].get("rejected") == 15 and
                receipt.get("weighted_mutation_results", {}).get("attempted") == 8 and
                receipt["weighted_mutation_results"].get("rejected") == 8,
                "producer mutation transcript")
        verdict = seal({"schema": "d972-r07-positive-common-word-colgen-verdict/v1",
            "mode": "SELFTEST", "terminal": COMMON, "status": "PASS",
            "mutation_attempted": 15, "mutation_rejected": rejected,
            "weighted_mutation_attempted": 8,
            "weighted_mutation_rejected": weighted_rejected,
            "module_import_double_cross": True,
            "helper_nonshared": True})
        marker = ("R07_POSITIVE_COMMON_WORD_COLGEN_V1_CHECKER_SELFTEST_PASS "
                  "mutation_attempted=15 mutation_rejected=15 "
                  "coarse_inverse_checks=4 weighted_mutation_attempted=8 "
                  "weighted_mutation_rejected=8")
    else:
        if receipt.get("terminal") == COMMON:
            runtime = independent_runtime()
            result = validate_common(runtime, receipt, expected_pins)
        else:
            runtime = (independent_runtime() if receipt.get("checkpoint") is not None
                       else None)
            result = validate_unknown(runtime, receipt, expected_pins, receipt_path)
        verdict = seal({"schema": "d972-r07-positive-common-word-colgen-verdict/v1",
                        "mode": "PRODUCTION", "status": "PASS", **result})
        marker = "R07_POSITIVE_COMMON_WORD_COLGEN_V1_CHECKER_PRODUCTION_PASS terminal=" + str(result["terminal"])
    write_json(verdict_path, verdict)
    print(marker, flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("R07_POSITIVE_COMMON_WORD_COLGEN_V1_CHECKER_STOP " +
              type(exc).__name__ + ":" + str(exc), file=sys.stderr, flush=True)
        raise
