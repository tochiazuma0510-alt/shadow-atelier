#!/usr/bin/env python3
"""Independent checker for the task-174 linked context-image census.

This checker never imports the task-174 producer or any of its helpers.  Its
COMPLETE enumeration uses positive order y,x; the published producer order
x,y is replayed separately only after literal state-set equality is known.
"""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import importlib.util
import json
import os
import struct
import sys
import tempfile
import time
import zlib
from collections import Counter, deque
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
PRODUCER_PATH = Path("search/d972_r07_target6_context_image_census_v1.py")
STATIC_FIXTURE = Path(
    "search/certs/d972_r07_target6_context_image_census_"
    "preflight_v1_20260827.json")
SCHEMA = "d972-r07-target6-context-image-census/v1"
VERDICT_SCHEMA = "d972-r07-target6-context-image-census-verdict/v1"
CHECKER_MARKER = "D174_TARGET6_CONTEXT_IMAGE_CENSUS_V1_CHECKER_PASS"
SELFTEST_MARKER = "D174_TARGET6_CONTEXT_IMAGE_CENSUS_V1_CHECKER_SELFTEST_PASS"
TERMINAL_COMPLETE = "R07_TARGET6_CONTEXT_IMAGE_CENSUS_COMPLETE"
TERMINAL_RESOURCE = "R07_TARGET6_CONTEXT_IMAGE_CENSUS_UNKNOWN_RESOURCE"
TERMINAL_INPUT = "R07_TARGET6_CONTEXT_IMAGE_CENSUS_INPUT_STOP"
TERMINALS = {TERMINAL_COMPLETE, TERMINAL_RESOURCE, TERMINAL_INPUT}
STATE_CAP = 2_000_000
SOFT_DEADLINE_SECONDS = 9_000
PROCESS_OUTER_SECONDS = 10_200
WORKFLOW_UPLOAD_MARGIN_SECONDS = 1_200
STATE_KEY_WIDTH = 462
E4_BLOB_WIDTH = 154
CONTEXT_PAIR_WIDTH = 308
DELTA_STATE_WIDTH = 30
TASK168_SCHREIER_WORDS_SHA = (
    "c7053b4b2c085ff8016ad1da1e0459dc77f0fc777323693b93f1157de0fbde1e")
CONTEXT_ROWS_SHA = (
    "bf07578f91f5ed66e6ddddd4ef83dafa45817a29df066940bbc13bd53cdd00f6")
ALIAS_ROWS_SHA = (
    "15cdac950ede8ce4596e5014ae1b6d0caa28523898cb42f3387f435a11b919a8")
TARGET_ALIASES = (
    "hexagon_1_fxy_0", "hexagon_1_fxz_0", "hexagon_1_fyz_0")
SIGNED_ORDER = (1, 2, -1, -2)
PRODUCER_BYTES = 57948
PRODUCER_SHA256 = "c7307c0ed21a4cee0798256fefc3f6b0044b1618d76bc76369ccf7e78c4bbaea"
STATIC_FIXTURE_BYTES = 5971
STATIC_FIXTURE_SHA256 = (
    "f96115087a4ddeb26552d7be9caadfda62bfcacc2972b1258d0859df567e4c7d")
BOUNDARIES = {
    "full_D2_correlation_run": False,
    "full_correction_orbit_correlation_run": False,
    "target6_solved": False,
    "all_seven_solved": False,
    "cofinal_compatibility_proved": False,
    "fake": False,
    "Ihara_witness": False,
}


PINS: dict[str, tuple[Path, int, str]] = {
    "task174": (Path("sol/luna_task_174_r07_target6_context_image_census_v1.md"),
        6765, "b0ed2024d0dddb99e6a9407eca4ca732dc8f5791052d6a01b09c0b7126375ec4"),
    "task174b": (Path("sol/luna_task_174b_r07_target6_context_image_census_repair.md"),
        6294, "0a17d240740e403706ffe234778dbd0eb1bb9ab78a0e588e4173943ebf8bb7d7"),
    "proof109": (Path("sol/proof_r07_full_e4_joint_orbit_selector_v109.md"),
        11228, "3224f0be545ac1ffe1d3c674087b30f55c0eb97fda0bd7702eb5f85b768255f0"),
    "proof118": (Path("sol/proof_r07_context_fibre_dual_correlation_v118.md"),
        8776, "6ef2cbf4ebf5ff3466b5eaf21ef4da572684517eb2f6d18c23fd12c8ad3ada3b"),
    "proof120": (Path("sol/proof_r07_extension_section_context_census_v120.md"),
        7367, "118cecd8b972c3fbeb7713597196f5b9760366778ff4d47df7eda4fb3e20f436"),
    "audit119": (Path("sol/audit_r07_full_e4_orbit_preflight_v7_v119.md"),
        4943, "48191c65aac368dd15a1da74c133a1afd5eb9b25eda997ed16ddfa3d01200234"),
    "task172_producer": (Path("search/d972_r07_full_e4_joint_orbit_preflight_v7.py"),
        21918, "92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"),
    "task172_checker": (Path("crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py"),
        12423, "e3917ec05b95b8996e3a5cec1cc2bfde51c3ed8c6972175fd9be9e1178205c23"),
    "task172_receipt": (Path("search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json"),
        45246709, "86c6f3a72a3f852a1be7c5323bf72c7ad987377fd5483b6e32528fe263e290ff"),
    "task172_reply": (Path("sol/luna_reply_172_r07_full_e4_orbit_preflight_repair_v7.md"),
        4200, "62ab78ecf0f832452d2a8e4e929cbc142188f0ba08c9751cc06e9eec026204e2"),
    "task168_task": (Path("sol/luna_task_168_r07_jennings_legal_coefficients_v1.md"),
        7262, "4d85fd8f9ec69a618828c06498aa22922cf5372e21d10ed65280ca2468f5b7f1"),
    "task168_reply": (Path("sol/luna_reply_168_r07_jennings_legal_coefficients_v1.md"),
        10692, "d22bed5ee8331fd5eb1d84256813699d0985df5a5bdf9a31152fdc448f847940"),
    "task168_producer": (Path("search/d972_r07_760_l3_target6_legal_coefficients_v1.py"),
        57792, "7db4e174dec13e2f69f4011b09abcc52320699261b164b5eedb18a53fa64b962"),
    "task168_checker": (Path("crosscheck/check_d972_r07_760_l3_target6_legal_coefficients_v1.py"),
        49633, "a54383185601e8251b7cbac87b6c57f89d3a8df8519cb93014b08a3893825e25"),
    "task168_driver": (Path("search/d972_r07_760_l3_target6_legal_coefficients_gha_driver_v1.g"),
        19176, "bad7911b0958983aacd541bb682b0f14a2903de02cecfc01043b593b17ab1e16"),
    "task168_receipt": (Path("search/certs/d972_r07_760_l3_target6_legal_coefficients_preflight_v1_20260827.json"),
        6833, "f390f53e6fc840f41009eb31beab519e36b4989b49ac70f9c8f4df7b32776138"),
    "task168_core": (Path("search/d972_r07_760_l3_target6_v1.py"),
        53284, "7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde"),
    "task157ee_task": (Path("sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md"),
        11226, "64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4"),
    "task157ee_reply": (Path("sol/luna_reply_157ee_b345_joint_kernel_qstar_closure.md"),
        4118, "53f20c2cb1395b8ff59ee961e1d5a14d55156a488eb6fa49edefed5dd7619eee"),
    "task157ee_producer": (Path("search/d972_b345_joint_kernel_qstar_closure_v1.py"),
        67945, "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    "task157ee_checker": (Path("search/check_d972_b345_joint_kernel_qstar_closure_v2.py"),
        5942, "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88"),
    "task157ee_driver": (Path("search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g"),
        3912, "8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7"),
    "task157ee_receipt": (Path("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json"),
        2166036, "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    "q3": (Path("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json"),
        231570, "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "e4_arithmetic": (Path("search/d972_b345_seedspan_triple4_v1.py"),
        535219, "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
}


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_raw(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def verify_self_digest(receipt: dict[str, Any], label: str) -> None:
    require(type(receipt) is dict and
            type(receipt.get("self_digest_sha256")) is str,
            label + " self digest field")
    work = copy.deepcopy(receipt)
    claimed = work.pop("self_digest_sha256")
    require(claimed == digest_obj(work), label + " self digest")


def pin_inputs() -> dict[str, Any]:
    rows = {}
    for label, (rel, size, digest) in PINS.items():
        path = ROOT / rel
        require(path.is_file() and path.stat().st_size == size and
                digest_file(path) == digest, "checker pin " + label)
        rows[label] = {"path": rel.as_posix(), "bytes": size,
                       "sha256": digest}
    producer = ROOT / PRODUCER_PATH
    require(producer.is_file() and producer.stat().st_size == PRODUCER_BYTES and
            digest_file(producer) == PRODUCER_SHA256, "producer source pin")
    return rows


def load_module(label: str, rel: Path, digest: str) -> Any:
    require(label not in sys.modules, "fresh independent module label")
    path = ROOT / rel
    require(digest_file(path) == digest, "checker module pre-pin")
    spec = importlib.util.spec_from_file_location(label, path)
    require(spec is not None and spec.loader is not None,
            "checker module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[label] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(label, None)
        raise
    require(digest_file(path) == digest, "checker module post-pin")
    return module


def element_blob(value: Any) -> bytes:
    raw = bytes(value[0]) + bytes(value[1])
    require(len(raw) == E4_BLOB_WIDTH, "checker E4 blob width")
    return raw


def pair_blob(pair: Sequence[Any]) -> bytes:
    require(len(pair) == 2, "checker context pair arity")
    raw = element_blob(pair[0]) + element_blob(pair[1])
    require(len(raw) == CONTEXT_PAIR_WIDTH, "checker pair blob width")
    return raw


def pack_fixed(raw: bytes, count: int, width: int,
               semantic: str) -> dict[str, Any]:
    require(count >= 0 and width > 0 and len(raw) == count * width,
            "checker pack shape")
    compressed = zlib.compress(raw, 9)
    return {
        "encoding": "zlib+base64/raw-fixed-width/v1",
        "semantic": semantic, "count": count, "record_width": width,
        "raw_bytes": len(raw), "raw_sha256": digest_raw(raw),
        "compressed_bytes": len(compressed),
        "compressed_sha256": digest_raw(compressed),
        "base64": base64.b64encode(compressed).decode("ascii"),
    }


def pack_u32(values: Iterable[int], semantic: str) -> dict[str, Any]:
    rows = [int(x) for x in values]
    require(all(0 <= x <= 0xffffffff for x in rows), "checker u32")
    return pack_fixed(b"".join(struct.pack("<I", x) for x in rows),
                      len(rows), 4, semantic)


def pack_u8(values: Iterable[int], semantic: str) -> dict[str, Any]:
    rows = [int(x) for x in values]
    require(all(0 <= x <= 255 for x in rows), "checker u8")
    return pack_fixed(bytes(rows), len(rows), 1, semantic)


def pack_bits(flags: Sequence[bool], semantic: str) -> dict[str, Any]:
    raw = bytearray((len(flags) + 7) // 8)
    for index, flag in enumerate(flags):
        if flag:
            raw[index // 8] |= 1 << (index % 8)
    compressed = zlib.compress(bytes(raw), 9)
    return {
        "encoding": "zlib+base64/lsb0-bitset/v1",
        "semantic": semantic, "bit_count": len(flags),
        "true_count": sum(bool(x) for x in flags),
        "raw_bytes": len(raw), "raw_sha256": digest_raw(bytes(raw)),
        "compressed_bytes": len(compressed),
        "compressed_sha256": digest_raw(compressed),
        "base64": base64.b64encode(compressed).decode("ascii"),
    }


def unpack_fixed(row: dict[str, Any], *, count: int, width: int,
                 semantic: str) -> bytes:
    require(set(row) == {"encoding", "semantic", "count", "record_width",
                         "raw_bytes", "raw_sha256", "compressed_bytes",
                         "compressed_sha256", "base64"},
            semantic + " packed keys")
    require(row["encoding"] == "zlib+base64/raw-fixed-width/v1" and
            row["semantic"] == semantic and row["count"] == count and
            row["record_width"] == width and
            row["raw_bytes"] == count * width,
            semantic + " packed metadata")
    compressed = base64.b64decode(row["base64"], validate=True)
    require(len(compressed) == row["compressed_bytes"] and
            digest_raw(compressed) == row["compressed_sha256"],
            semantic + " compressed binding")
    raw = zlib.decompress(compressed)
    require(len(raw) == row["raw_bytes"] and
            digest_raw(raw) == row["raw_sha256"],
            semantic + " raw binding")
    return raw


def unpack_bits(row: dict[str, Any], *, count: int,
                semantic: str) -> list[bool]:
    require(set(row) == {"encoding", "semantic", "bit_count", "true_count",
                         "raw_bytes", "raw_sha256", "compressed_bytes",
                         "compressed_sha256", "base64"},
            semantic + " bitset keys")
    require(row["encoding"] == "zlib+base64/lsb0-bitset/v1" and
            row["semantic"] == semantic and row["bit_count"] == count and
            row["raw_bytes"] == (count + 7) // 8,
            semantic + " bitset metadata")
    compressed = base64.b64decode(row["base64"], validate=True)
    require(len(compressed) == row["compressed_bytes"] and
            digest_raw(compressed) == row["compressed_sha256"],
            semantic + " bitset compressed")
    raw = zlib.decompress(compressed)
    require(len(raw) == row["raw_bytes"] and
            digest_raw(raw) == row["raw_sha256"],
            semantic + " bitset raw")
    flags = [bool(raw[i // 8] & (1 << (i % 8))) for i in range(count)]
    if count % 8:
        require(raw[-1] >> (count % 8) == 0, semantic + " unused bits")
    require(sum(flags) == row["true_count"], semantic + " true count")
    return flags


def rebuild_pending_frontier(keys: Sequence[bytes], cursor: dict[str, Any],
                             generator_order: Sequence[int]) \
        -> dict[str, Any]:
    """Independent implementation of the registered pending-work digest."""
    order = [int(x) for x in generator_order]
    require(order == [1, 2], "checker frontier generator order")
    state_cursor = cursor.get("state_id")
    letter_cursor = cursor.get("generator_index")
    require(type(state_cursor) is int and type(letter_cursor) is int and
            0 <= state_cursor <= len(keys), "checker frontier cursor")
    if state_cursor == len(keys):
        require(letter_cursor == 0, "checker closed frontier")
    else:
        require(letter_cursor in (0, 1), "checker frontier letter cursor")
    header = canonical_bytes({"cursor": cursor,
                              "positive_generator_order": order})
    accumulator = hashlib.sha256()
    accumulator.update(b"D174-PENDING-POSITIVE-FRONTIER-V1\0")
    accumulator.update(struct.pack("<I", len(header)))
    accumulator.update(header)
    number = 0
    for sid in range(state_cursor, len(keys)):
        begin = letter_cursor if sid == state_cursor else 0
        for gi in range(begin, 2):
            require(len(keys[sid]) == STATE_KEY_WIDTH,
                    "checker frontier state width")
            accumulator.update(struct.pack("<IBB", sid, gi, order[gi]))
            accumulator.update(keys[sid])
            number += 1
    return {
        "definition": (
            "cursor header followed by ordered pending records "
            "<u32-state-id,u8-generator-index,u8-letter,462-byte-state-key>"),
        "digest_domain": "D174-PENDING-POSITIVE-FRONTIER-V1",
        "cursor": copy.deepcopy(cursor),
        "positive_generator_order": order,
        "record_width": 6 + STATE_KEY_WIDTH,
        "pending_task_count": number,
        "sha256": accumulator.hexdigest(),
    }


def registered_caps(state_cap: int = STATE_CAP,
                    soft_seconds: int = SOFT_DEADLINE_SECONDS) \
        -> dict[str, Any]:
    return {
        "state_cap": state_cap,
        "soft_deadline_seconds": soft_seconds,
        "producer_outer_timeout_seconds": PROCESS_OUTER_SECONDS,
        "checker_outer_timeout_seconds": PROCESS_OUTER_SECONDS,
        "workflow_upload_margin_seconds": WORKFLOW_UPLOAD_MARGIN_SECONDS,
        "total_outer_caps_plus_margin_seconds": 21600,
        "raw_stream_count_formula": "6441*|Delta_E|",
        "overflow_safe_integer_arithmetic": True,
    }


def reduce_word(word: Iterable[int]) -> list[int]:
    answer: list[int] = []
    for raw in word:
        letter = int(raw)
        require(letter in (-2, -1, 1, 2), "checker F2 letter")
        if answer and answer[-1] == -letter:
            answer.pop()
        else:
            answer.append(letter)
    return answer


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(x) for x in reversed(word)]


class CheckModel:
    def __init__(self, e4: Any, contexts: Sequence[Sequence[Any]]) -> None:
        self.e4 = e4
        self.contexts = [tuple(x) for x in contexts]
        require(len(self.contexts) == 3, "checker context count")
        self.identity = tuple(e4.identity for _ in range(3))
        self.generators = {
            letter: tuple(e4.eval([letter], pair) for pair in self.contexts)
            for letter in (1, 2)}
        self.inverses = {letter: tuple(e4.inverse(x) for x in row)
                         for letter, row in self.generators.items()}

    def mul(self, left: Any, right: Any) -> Any:
        return tuple(self.e4.mul(left[i], right[i]) for i in range(3))

    def step(self, state: Any, signed_letter: int) -> Any:
        table = self.generators if signed_letter > 0 else self.inverses
        return self.mul(state, table[abs(signed_letter)])

    def eval(self, word: Sequence[int]) -> Any:
        value = self.identity
        for letter in word:
            value = self.step(value, int(letter))
        return value

    def key(self, state: Any) -> bytes:
        raw = b"".join(element_blob(x) for x in state)
        require(len(raw) == STATE_KEY_WIDTH, "checker state key width")
        return raw

    def coordinate_step(self, value: Any, coordinate: int,
                        signed_letter: int) -> Any:
        table = self.generators if signed_letter > 0 else self.inverses
        return self.e4.mul(value, table[abs(signed_letter)][coordinate])


class CheckDelta:
    def __init__(self, core: Any, e4: Any, model: CheckModel,
                 expected_words: Sequence[Sequence[int]]) -> None:
        self.pc = e4.pc
        x, y, z = (e4.eval(list(word))[1]
                   for word in (core.X0, core.Y0, core.Z0))
        require(z == self.pc.inverse(self.pc.mul(y, x)),
                "checker Delta z")
        self.generators = {1: (x, x, y), 2: (y, z, z)}
        self.inverses = {letter: tuple(self.pc.inverse(v) for v in row)
                         for letter, row in self.generators.items()}
        require(tuple(v[1] for v in model.generators[1]) == self.generators[1]
                and tuple(v[1] for v in model.generators[2]) == self.generators[2],
                "checker Delta marked map")
        identity = tuple(self.pc.one() for _ in range(3))
        self.states = [identity]
        self.ids = {identity: 0}
        self.sections = [[]]
        tree = {}
        queue = deque([0])
        while queue:
            state_id = queue.popleft()
            for letter in (1, 2):
                following = self.mul(self.states[state_id],
                                     self.generators[letter])
                if following not in self.ids:
                    require(len(self.states) < 27, "checker Delta cap")
                    target = len(self.states)
                    self.ids[following] = target
                    self.states.append(following)
                    self.sections.append(self.sections[state_id] + [letter])
                    tree[target] = (state_id, letter)
                    queue.append(target)
        require(len(self.states) == 27, "checker Delta order")
        self.positive = {}
        self.schreier_words = []
        for state_id, state in enumerate(self.states):
            for letter in (1, 2):
                target = self.ids[self.mul(state, self.generators[letter])]
                self.positive[(state_id, letter)] = target
                if tree.get(target) != (state_id, letter):
                    self.schreier_words.append(reduce_word(
                        self.sections[state_id] + [letter] +
                        inverse_word(self.sections[target])))
        require(self.schreier_words == [list(x) for x in expected_words] and
                digest_obj(self.schreier_words) == TASK168_SCHREIER_WORDS_SHA,
                "checker task168 Schreier roster")

    def mul(self, left: Any, right: Any) -> Any:
        return tuple(self.pc.mul(left[i], right[i]) for i in range(3))

    def step(self, state_id: int, letter: int) -> int:
        if letter > 0:
            return self.positive[(state_id, letter)]
        row = self.mul(self.states[state_id], self.inverses[-letter])
        return self.ids[row]

    def project(self, state: Any) -> int:
        row = tuple(value[1] for value in state)
        require(row in self.ids, "checker Delta projection row")
        return self.ids[row]

    def key(self, state: Any) -> bytes:
        raw = b"".join(bytes(x) for x in state)
        require(len(raw) == DELTA_STATE_WIDTH, "checker Delta key width")
        return raw


def select_canaries(task172: dict[str, Any]) -> list[dict[str, Any]]:
    answer = []
    for index, row in enumerate(task172["fox_canaries"]["transcript"]):
        word = row.get("r_word")
        if type(word) is list and word:
            answer.append({"transcript_index": index,
                           "layer": row["layer"],
                           "ordinal": row["ordinal"],
                           "word_kind": "r_word",
                           "word": [int(x) for x in word],
                           "word_sha256": digest_obj(word)})
        if len(answer) == 20:
            break
    require(len(answer) == 20, "checker canary count")
    return answer


def build_context(pins: dict[str, Any]) -> dict[str, Any]:
    old = load_module("_d174_checker_frozen_e4_arithmetic",
                      PINS["e4_arithmetic"][0],
                      PINS["e4_arithmetic"][2])
    core = load_module("_d174_checker_frozen_task168_core",
                       PINS["task168_core"][0], PINS["task168_core"][2])
    q3 = json.loads((ROOT / PINS["q3"][0]).read_text(encoding="utf-8"))
    require(q3.get("schema") == "d972-b345-q-chief/v1", "checker q3")
    _, e4, _ = old.reconstruct_quotients(q3)
    contexts, aliases, public = old.cheap_context_registry(e4)
    require(len(contexts) == 31 and len(aliases) == 46 and
            public["context_rows_sha256"] == CONTEXT_ROWS_SHA and
            public["named_use_mapping_sha256"] == ALIAS_ROWS_SHA,
            "checker context registry")
    joint = json.loads((ROOT / PINS["task157ee_receipt"][0]).read_text(
        encoding="utf-8"))
    require(joint.get("terminal_token") ==
            "B345_JOINT_KERNEL_QSTAR_CLOSED" and
            joint.get("context_registry") == public,
            "checker 157ee context receipt")
    task172 = json.loads((ROOT / PINS["task172_receipt"][0]).read_text(
        encoding="utf-8"))
    require(task172.get("schema") ==
            "d972-r07-full-e4-orbit-preflight/v7" and
            task172.get("terminal_token") ==
            "R07_FULL_E4_ORBIT_PREFLIGHT_READY" and
            task172["fox_canaries"]["status"] == "PASS",
            "checker task172 receipt")
    task168 = json.loads((ROOT / PINS["task168_receipt"][0]).read_text(
        encoding="utf-8"))
    verify_self_digest(task168, "checker task168")
    require(task168.get("producer_source") == pins["task168_producer"],
            "checker task168 source binding")

    source_pairs = ((core.X0, core.Y0), (core.X0, core.Z0),
                    (core.Y0, core.Z0))
    literal_pairs = [(e4.eval(list(a)), e4.eval(list(b)))
                     for a, b in source_pairs]
    raw_pairs = [pair_blob(row) for row in literal_pairs]
    rows = public["contexts"]
    ids = []
    for pair in literal_pairs:
        hits = [row["context_id"] for row in rows
                if row["left_hex"] == element_blob(pair[0]).hex() and
                row["right_hex"] == element_blob(pair[1]).hex()]
        require(len(hits) == 1, "checker unique target context")
        ids.append(hits[0])
    require(ids == [1, 2, 3], "checker context ids")
    alias_map = {row["name"]: row["context_id"] for row in public["named_uses"]}
    require([alias_map[x] for x in TARGET_ALIASES] == ids,
            "checker context aliases")
    target_contexts = [contexts[i - 1] for i in ids]
    require([pair_blob(x) for x in target_contexts] == raw_pairs,
            "checker literal context pairs")
    bindings = task172["contexts"]["target6_bindings"]
    require(all(bindings[i]["alias"] == TARGET_ALIASES[i] and
                bindings[i]["registry_id"] == i + 1 and
                bindings[i]["context_blob"] == raw_pairs[i].hex()
                for i in range(3)), "checker task172 pair binding")
    words, delta_public = core.delta_and_schreier(core, e4)
    require(delta_public["order_Delta"] == 27 and
            delta_public["schreier_words_sha256"] ==
            TASK168_SCHREIER_WORDS_SHA,
            "checker task168 Delta public")
    model = CheckModel(e4, target_contexts)
    delta = CheckDelta(core, e4, model, words)
    marked = []
    for word in ([1], [2], [-1], [-2], [1, 2]):
        left = tuple(e4.eval(word, pair) for pair in target_contexts)
        right = model.eval(word)
        require(left == right, "checker marked evaluator agreement")
        marked.append({"word": list(word),
                       "triple_key_hex": model.key(right).hex()})
    canaries = select_canaries(task172)
    public_canaries = []
    for row in canaries:
        left = tuple(e4.eval(row["word"], pair) for pair in target_contexts)
        right = model.eval(row["word"])
        require(left == right, "checker task172 canary agreement")
        public_row = {key: value for key, value in row.items() if key != "word"}
        public_row["triple_key_sha256"] = digest_raw(model.key(right))
        public_canaries.append(public_row)
    expected_binding = {
        "ordered_context_names": list(TARGET_ALIASES),
        "registry_context_ids": ids,
        "context_pair_serialization":
            "left 154-byte E4 blob followed by right 154-byte E4 blob",
        "context_pair_blob_width": CONTEXT_PAIR_WIDTH,
        "context_pair_blobs_hex": [x.hex() for x in raw_pairs],
        "positive_generator_order": ["x", "y"],
        "marked_triple_generator_keys_hex": [
            model.key(model.generators[i]).hex() for i in (1, 2)],
        "marked_word_cross_checks": marked,
        "task172_relation_canaries": public_canaries,
        "task172_relation_canary_count": 20,
        "task168_Delta3_order": 27,
        "task168_ordered_schreier_words_sha256":
            TASK168_SCHREIER_WORDS_SHA,
        "exact_pair_alias_and_marked_value_binding": True,
    }
    return {"model": model, "delta": delta,
            "expected_binding": expected_binding}


def validate_envelope(receipt: dict[str, Any], pins: dict[str, Any], *,
                      expected_caps: dict[str, Any] | None = None) -> None:
    require(set(receipt) == {
        "schema", "mode", "grade", "terminal", "status", "reason",
        "source", "pins", "registered_caps", "input_bindings", "census",
        "resource", "selftest", "boundaries", "scope", "GHA_dispatched",
        "unknowns", "self_digest_sha256"}, "receipt top-level keys")
    verify_self_digest(receipt, "task174 receipt")
    require(receipt["schema"] == SCHEMA and receipt["terminal"] in TERMINALS and
            receipt["grade"] == "CANDIDATE_PENDING_INDEPENDENT_CHECKER" and
            receipt["source"] == {"path": PRODUCER_PATH.as_posix(),
                                  "bytes": PRODUCER_BYTES,
                                  "sha256": PRODUCER_SHA256} and
            receipt["pins"] == pins and receipt["boundaries"] == BOUNDARIES and
            receipt["GHA_dispatched"] is False,
            "receipt fixed envelope")
    expected_status = {TERMINAL_COMPLETE: "COMPLETE",
                       TERMINAL_RESOURCE: "UNKNOWN_RESOURCE",
                       TERMINAL_INPUT: "INPUT_STOP"}[receipt["terminal"]]
    require(receipt["status"] == expected_status, "terminal/status typing")
    if expected_caps is None:
        expected_caps = registered_caps()
    require(receipt["registered_caps"] == expected_caps,
            "registered cap envelope")
    require(receipt["scope"] == {
        "simultaneous_context_image_census_only": True,
        "linked_Delta_E_not_replaced_by_E4_cubed": True,
        "complete_fibres_enable_but_do_not_execute_v118_correlation": True},
        "scope boundary")


class CheckBudget:
    def __init__(self) -> None:
        self.started = time.monotonic()
        self.checks = 0

    def check(self, label: str) -> None:
        self.checks += 1
        if self.checks % 1024 == 0:
            require(time.monotonic() - self.started < SOFT_DEADLINE_SECONDS,
                    "checker soft deadline at " + label)


def independent_enumeration(model: CheckModel, budget: CheckBudget, *,
                            state_cap: int = STATE_CAP) \
        -> tuple[list[Any], list[bytes], dict[bytes, int]]:
    states = [model.identity]
    keys = [model.key(model.identity)]
    ids = {keys[0]: 0}
    queue = deque([0])
    while queue:
        state_id = queue.popleft()
        for letter in (2, 1):
            budget.check("independent_yx_BFS")
            following = model.step(states[state_id], letter)
            key = model.key(following)
            if key not in ids:
                require(len(states) < state_cap,
                        "checker independent state cap")
                ids[key] = len(states)
                states.append(following)
                keys.append(key)
                queue.append(ids[key])
    return states, keys, ids


def decode_enumeration(public: dict[str, Any], *,
                       state_cap: int = STATE_CAP) \
        -> tuple[list[bytes], list[int], list[int], list[int] | None]:
    count = public["state_count"]
    require(type(count) is int and 0 < count <= state_cap,
            "published state count cap")
    raw = unpack_fixed(public["discovery_states"], count=count,
                       width=STATE_KEY_WIDTH,
                       semantic="positive-BFS-discovery-order-literal-triple-states")
    keys = [raw[i * STATE_KEY_WIDTH:(i + 1) * STATE_KEY_WIDTH]
            for i in range(count)]
    parent_raw = unpack_fixed(public["parents_u32"], count=count, width=4,
                              semantic="positive-BFS-parent-state-id")
    parents = [struct.unpack_from("<I", parent_raw, 4 * i)[0]
               for i in range(count)]
    letter_raw = unpack_fixed(
        public["parent_letters_u8"], count=count, width=1,
        semantic="actual-positive-generator-on-parent-edge")
    letters = list(letter_raw)
    transitions = None
    if public["four_signed_transitions_u32"] is not None:
        traw = unpack_fixed(
            public["four_signed_transitions_u32"], count=4 * count, width=4,
            semantic="four-signed-transition-targets")
        transitions = [struct.unpack_from("<I", traw, 4 * i)[0]
                       for i in range(4 * count)]
    expected_frontier = rebuild_pending_frontier(
        keys, public["cursor"], public["positive_generator_order"])
    require(len(set(keys)) == count and parents[0] == 0xffffffff and
            letters[0] == 0 and public["state_key_width"] == STATE_KEY_WIDTH and
            public["positive_generator_order"] == [1, 2] and
            public["four_signed_transition_order"] == list(SIGNED_ORDER) and
            public["identity_state_key_hex"] == keys[0].hex() and
            public["discovery_order_sha256"] == digest_raw(raw) and
            public["canonical_sorted_state_set_sha256"] ==
            digest_raw(b"".join(sorted(keys))) and
            public["section_parent_sha256"] ==
            digest_raw(parent_raw + letter_raw) and
            public["seen_state_count"] == count and
            public["discovery_prefix_state_count"] == count and
            public["discovery_prefix_sha256"] == digest_raw(raw) and
            public["seen_state_set_sha256"] ==
            digest_raw(b"".join(sorted(keys))) and
            public["frontier_count_definition"] ==
            "discovered states with state_id at or after cursor.state_id" and
            public["frontier_count"] == count - public["cursor"]["state_id"] and
            public["pending_positive_frontier"] == expected_frontier,
            "published enumeration exact fields")
    return keys, parents, letters, transitions


def replay_published_complete(model: CheckModel, published_keys: list[bytes],
                              parents: list[int], letters: list[int]) \
        -> list[Any]:
    require(published_keys[0] == model.key(model.identity),
            "producer identity key")
    states = [model.identity]
    ids = {published_keys[0]: 0}
    head = 0
    while head < len(states):
        for letter in (1, 2):
            following = model.step(states[head], letter)
            key = model.key(following)
            if key not in ids:
                target = len(states)
                require(target < len(published_keys) and
                        published_keys[target] == key and
                        parents[target] == head and letters[target] == letter,
                        "producer positive BFS parent/order replay")
                ids[key] = target
                states.append(following)
        head += 1
    require(len(states) == len(published_keys),
            "producer discovery roster complete")
    return states


def replay_published_prefix(model: CheckModel, public: dict[str, Any],
                            keys: list[bytes], parents: list[int],
                            letters: list[int], resource: dict[str, Any], *,
                            state_cap: int = STATE_CAP,
                            soft_seconds: int = SOFT_DEADLINE_SECONDS) \
        -> list[Any]:
    states = [model.identity]
    ids = {keys[0]: 0}
    head = 0
    generator_index = 0
    target_cursor = public["cursor"]
    while True:
        if (head == target_cursor["state_id"] and
                generator_index == target_cursor["generator_index"]):
            break
        require(head < len(states), "prefix cursor beyond frontier")
        letter = (1, 2)[generator_index]
        following = model.step(states[head], letter)
        key = model.key(following)
        if key not in ids:
            target = len(states)
            require(target < len(keys) and keys[target] == key and
                    parents[target] == head and letters[target] == letter,
                    "exact bounded prefix discovery replay")
            ids[key] = target
            states.append(following)
        generator_index += 1
        if generator_index == 2:
            generator_index = 0
            head += 1
    require(len(states) == len(keys), "prefix state count at cursor")
    if resource["reason"] == "state_cap":
        require(len(states) == state_cap and head < len(states),
                "state cap cursor")
        letter = (1, 2)[generator_index]
        attempted = model.key(model.step(states[head], letter))
        require(attempted not in ids and
                target_cursor["next_positive_letter"] == letter and
                target_cursor["attempted_novel_state_sha256"] ==
                digest_raw(attempted), "state cap before novel insertion")
    else:
        require(resource["reason"] == "soft_deadline" and
                resource["elapsed_seconds_at_receipt"] >=
                soft_seconds,
                "deadline resource envelope")
    return states


def section_word(parents: Sequence[int], letters: Sequence[int],
                 state_id: int) -> list[int]:
    reverse = []
    guard = 0
    while state_id:
        require(0 <= parents[state_id] < state_id and
                letters[state_id] in (1, 2), "checker parent section")
        reverse.append(letters[state_id])
        state_id = parents[state_id]
        guard += 1
        require(guard <= len(parents), "checker parent cycle")
    return list(reversed(reverse))


def sample_indices(count: int) -> list[int]:
    if count <= 1000:
        return list(range(count))
    return sorted({i * (count - 1) // 999 for i in range(1000)})


def expected_lex_section(keys: Sequence[bytes], parents: Sequence[int],
                         letters: Sequence[int], flags: Sequence[bool]) \
        -> dict[str, Any] | None:
    rows = sorted((keys[i], i) for i, flag in enumerate(flags)
                  if flag and i != 0)
    if not rows:
        return None
    key, state_id = rows[0]
    word = section_word(parents, letters, state_id)
    return {"state_key_hex": key.hex(), "state_id": state_id,
            "section_word": word, "section_word_sha256": digest_obj(word)}


def expected_projection(model: CheckModel, states: Sequence[Any],
                        keys: Sequence[bytes], parents: Sequence[int],
                        letters: Sequence[int], budget: CheckBudget) \
        -> dict[str, Any]:
    order = len(states)
    coordinate_rows = []
    identity_blob = element_blob(model.e4.identity)
    for coordinate in range(3):
        values = {}
        counts = Counter()
        flags = []
        for state in states:
            budget.check("checker coordinate projection")
            key = element_blob(state[coordinate])
            values.setdefault(key, state[coordinate])
            counts[key] += 1
            flags.append(key == identity_blob)
        image = sorted(values)
        kernel_order = sum(flags)
        require(set(counts.values()) == {kernel_order} and
                order == len(image) * kernel_order,
                "checker coordinate Lagrange")
        for value in values.values():
            for signed in SIGNED_ORDER:
                target = element_blob(model.coordinate_step(
                    value, coordinate, signed))
                require(target in values, "checker coordinate closure")
        kernel_keys = sorted(keys[i] for i, flag in enumerate(flags) if flag)
        coordinate_rows.append({
            "projection_id": coordinate + 1,
            "coordinate_name": TARGET_ALIASES[coordinate],
            "image_order": len(image), "kernel_order": kernel_order,
            "image_set": pack_fixed(
                b"".join(image), len(image), E4_BLOB_WIDTH,
                f"coordinate-{coordinate + 1}-literal-image-set"),
            "kernel_membership": pack_bits(
                flags, f"coordinate-{coordinate + 1}-kernel-membership"),
            "canonical_image_digest_sha256": digest_raw(b"".join(image)),
            "canonical_kernel_state_set_sha256":
                digest_raw(b"".join(kernel_keys)),
            "uniform_fibre_size": kernel_order,
            "uniform_fibre_histogram": {
                str(size): number
                for size, number in sorted(Counter(counts.values()).items())},
            "uniform_fibres_checked": True,
            "lagrange_identity_checked": True,
            "literal_four_signed_generator_closure_checked": True,
            "lex_first_nonidentity_kernel_section": expected_lex_section(
                keys, parents, letters, flags),
        })
    pair_rows = []
    for left, right in ((0, 1), (0, 2), (1, 2)):
        pair_id = f"{left + 1},{right + 1}"
        values = {}
        counts = Counter()
        flags = []
        identity = identity_blob + identity_blob
        for state in states:
            budget.check("checker pair projection")
            key = element_blob(state[left]) + element_blob(state[right])
            values.setdefault(key, (state[left], state[right]))
            counts[key] += 1
            flags.append(key == identity)
        image = sorted(values)
        kernel_order = sum(flags)
        require(set(counts.values()) == {kernel_order} and
                order == len(image) * kernel_order,
                "checker pair Lagrange")
        for value in values.values():
            for signed in SIGNED_ORDER:
                target = (element_blob(model.coordinate_step(
                    value[0], left, signed)) +
                    element_blob(model.coordinate_step(
                        value[1], right, signed)))
                require(target in values, "checker pair closure")
        kernel_keys = sorted(keys[i] for i, flag in enumerate(flags) if flag)
        pair_rows.append({
            "pair_projection_id": pair_id,
            "coordinate_ids": [left + 1, right + 1],
            "image_order": len(image), "kernel_order": kernel_order,
            "image_set": pack_fixed(
                b"".join(image), len(image), 2 * E4_BLOB_WIDTH,
                f"pair-{pair_id}-literal-image-set"),
            "kernel_membership": pack_bits(
                flags, f"pair-{pair_id}-kernel-membership"),
            "canonical_image_digest_sha256": digest_raw(b"".join(image)),
            "canonical_kernel_state_set_sha256":
                digest_raw(b"".join(kernel_keys)),
            "uniform_fibre_size": kernel_order,
            "uniform_fibre_histogram": {
                str(size): number
                for size, number in sorted(Counter(counts.values()).items())},
            "uniform_fibres_checked": True,
            "lagrange_identity_checked": True,
            "literal_four_signed_generator_closure_checked": True,
            "lex_first_nonidentity_kernel_section": expected_lex_section(
                keys, parents, letters, flags),
        })
    coordinate_keys = [[element_blob(state[i]) for state in states]
                       for i in range(3)]
    equality = [[coordinate_keys[i] == coordinate_keys[j]
                 for j in range(3)] for i in range(3)]
    common = [all(element_blob(state[i]) == identity_blob for i in range(3))
              for state in states]
    require(sum(common) == 1 and common[0], "checker common kernel identity")
    return {
        "coordinate_projections": coordinate_rows,
        "pair_projections": pair_rows,
        "coordinate_map_equality_matrix": equality,
        "equal_coordinate_map_pairs": [
            [i + 1, j + 1] for i in range(3) for j in range(i + 1, 3)
            if equality[i][j]],
        "common_three_coordinate_kernel": {
            "order": 1,
            "membership": pack_bits(
                common, "common-three-coordinate-kernel-membership"),
            "canonical_state_set_sha256": digest_raw(keys[0]),
            "is_identity_only": True,
            "proof": (
                "A state in the intersection has all three literal E4 "
                "coordinates equal to identity; the 462-byte triple key is "
                "therefore the identity key, so injective literal state "
                "keys force the state itself to be identity."),
        },
        "full_group_literal_four_signed_generator_closure": True,
        "all_projection_lagrange_identities": True,
    }


def expected_delta(delta: CheckDelta, states: Sequence[Any],
                   keys: Sequence[bytes], transitions: Sequence[int],
                   budget: CheckBudget) -> dict[str, Any]:
    mapping = []
    for state in states:
        budget.check("checker Delta quotient")
        mapping.append(delta.project(state))
    counts = Counter(mapping)
    require(set(counts) == set(range(27)), "checker Delta surjectivity")
    fibre = len(states) // 27
    require(len(states) == 27 * fibre and set(counts.values()) == {fibre},
            "checker Delta fibres")
    for state_id in range(len(states)):
        for pos, letter in enumerate(SIGNED_ORDER):
            require(mapping[transitions[4 * state_id + pos]] ==
                    delta.step(mapping[state_id], letter),
                    "checker Delta transition")
    rows = [delta.key(state) for state in delta.states]
    flags = [value == 0 for value in mapping]
    kernel_keys = sorted(keys[i] for i, flag in enumerate(flags) if flag)
    return {
        "definition":
            "three exact E4 coordinates followed by literal Pi4[3] PC projection",
        "order_Delta3": 27,
        "marked_generator_agreement": True,
        "surjective_onto_all_27_literal_states": True,
        "not_inferred_from_divisibility": True,
        "canonical_state_rows": pack_fixed(
            b"".join(rows), 27, DELTA_STATE_WIDTH,
            "Delta3-canonical-positive-BFS-state-rows"),
        "positive_BFS_transversal_words": delta.sections,
        "positive_BFS_transversal_words_sha256": digest_obj(delta.sections),
        "ordered_schreier_words": delta.schreier_words,
        "ordered_schreier_words_sha256": digest_obj(delta.schreier_words),
        "schreier_generator_count": 28,
        "state_to_Delta3_id_u8": pack_u8(
            mapping, "Delta_E-discovery-state-to-Delta3-id"),
        "quotient_row_digest_sha256": digest_raw(bytes(mapping)),
        "kernel_order": sum(flags),
        "kernel_membership": pack_bits(flags, "Delta3-kernel-membership"),
        "canonical_kernel_state_set_sha256":
            digest_raw(b"".join(kernel_keys)),
        "uniform_fibre_size": fibre,
        "uniform_fibre_histogram": {
            str(size): number
            for size, number in sorted(Counter(counts.values()).items())},
        "all_four_signed_transitions_respected": True,
    }


def validate_complete(receipt: dict[str, Any], context: dict[str, Any]) \
        -> dict[str, Any]:
    state_cap = int(context.get("state_cap", STATE_CAP))
    require(receipt["mode"] == "census" and
            receipt["reason"] ==
            "FINITE_POSITIVE_BFS_AND_ALL_CENSUS_GATES_CLOSED" and
            receipt["unknowns"] == [] and receipt["resource"]["reason"] is None,
            "complete envelope")
    require(receipt["input_bindings"] == context["expected_binding"],
            "complete input bindings")
    census = receipt["census"]
    public = census["enumeration"]
    require(public["status"] == "COMPLETE" and
            public["all_four_signed_transitions_reconstructed"] is True and
            public["frontier_count"] == 0 and
            public["cursor"] == {"state_id": public["state_count"],
                                  "generator_index": 0},
            "complete enumeration envelope")
    keys, parents, letters, published_transitions = decode_enumeration(
        public, state_cap=state_cap)
    require(published_transitions is not None, "complete transitions present")
    budget = CheckBudget()
    independent_states, independent_keys, independent_ids = \
        independent_enumeration(
            context["model"], budget, state_cap=state_cap)
    del independent_states, independent_ids
    require(sorted(independent_keys) == sorted(keys),
            "literal sorted state-set equality under y,x enumeration")
    producer_states = replay_published_complete(
        context["model"], keys, parents, letters)
    key_to_id = {key: i for i, key in enumerate(keys)}
    expected_transitions = []
    for state_id, state in enumerate(producer_states):
        budget.check("checker signed transition table")
        row = []
        for letter in SIGNED_ORDER:
            target = context["model"].key(context["model"].step(state, letter))
            require(target in key_to_id, "checker full signed closure")
            row.append(key_to_id[target])
        require(row[2] < len(keys) and row[3] < len(keys),
                "checker inverse targets")
        expected_transitions.extend(row)
    require(published_transitions == expected_transitions and
            public["four_signed_transitions_u32"] == pack_u32(
                expected_transitions, "four-signed-transition-targets"),
            "exact four-letter transition table")
    depths = [0] * len(keys)
    for state_id in range(1, len(keys)):
        require(parents[state_id] < state_id and letters[state_id] in (1, 2),
                "parent table order")
        depths[state_id] = depths[parents[state_id]] + 1
    require(public["section_statistics"] == {
        "minimum_length": min(depths), "maximum_length": max(depths),
        "mean_length_numerator": sum(depths),
        "mean_length_denominator": len(depths)},
        "section statistics")
    samples = sample_indices(len(keys))
    for state_id in samples:
        word = section_word(parents, letters, state_id)
        require(context["model"].key(context["model"].eval(word)) ==
                keys[state_id], "sampled section replay")
    require(len(samples) >= min(1000, len(keys)), "section sample quota")
    projection = expected_projection(
        context["model"], producer_states, keys, parents, letters, budget)
    require(census["projections"] == projection,
            "independent projection/kernel/fibre census")
    quotient = expected_delta(context["delta"], producer_states, keys,
                              expected_transitions, budget)
    require(census["Delta3_quotient"] == quotient,
            "independent Delta3 quotient census")
    order = len(keys)
    require(census["order_Delta_E"] == order and
            census["raw_direct_stream_column_count"] == 6441 * order and
            census["raw_direct_stream_formula"] == "6441*|Delta_E|" and
            census["raw_direct_stream_overflow_safe"] is True and
            census["bounded_prefix_only"] is False,
            "complete order/raw count fields")
    return {"grade": "CROSS_CHECKED", "cross_checked_census": True,
            "bounded_prefix_cross_checked": False,
            "state_count": order, "section_replays": len(samples),
            "independent_positive_generator_order": ["y", "x"]}


def validate_resource(receipt: dict[str, Any], context: dict[str, Any]) \
        -> dict[str, Any]:
    state_cap = int(context.get("state_cap", STATE_CAP))
    soft_seconds = int(context.get(
        "soft_deadline_seconds", SOFT_DEADLINE_SECONDS))
    require(receipt["mode"] == "census" and
            receipt["reason"] in {"STATE_CAP_BEFORE_NOVEL_INSERT",
                                  "SOFT_DEADLINE_AT_REPLAYABLE_CURSOR"} and
            receipt["input_bindings"] == context["expected_binding"] and
            len(receipt["unknowns"]) == 1,
            "resource envelope")
    census = receipt["census"]
    require(census["order_Delta_E"] is None and
            census["projections"] is None and
            census["Delta3_quotient"] is None and
            census["raw_direct_stream_column_count"] is None and
            census["bounded_prefix_only"] is True,
            "resource makes no order/projection claim")
    public = census["enumeration"]
    require(public["status"] == "UNKNOWN_RESOURCE" and
            public["four_signed_transitions_u32"] is None and
            public["all_four_signed_transitions_reconstructed"] is False,
            "resource enumeration fields")
    keys, parents, letters, transitions = decode_enumeration(
        public, state_cap=state_cap)
    require(transitions is None, "resource transition absence")
    resource = receipt["resource"]
    require(resource["reason"] in {"state_cap", "soft_deadline"} and
            resource["state_cap"] == state_cap and
            resource["soft_deadline_seconds"] == soft_seconds and
            resource["prefix_replayable_without_order_inference"] is True,
            "resource registered contract")
    phase = resource["phase"]
    require(phase in {"positive_BFS", "four_signed_transition_reconstruction",
                      "coordinate_projection", "pair_projection",
                      "Delta3_quotient"}, "registered resource phase")
    if phase == "positive_BFS":
        require(resource["cursor"] == public["cursor"],
                "resource enumeration cursor binding")
    else:
        require(resource["reason"] == "soft_deadline" and
                public["cursor"] == {"state_id": public["state_count"],
                                      "generator_index": 0} and
                public["frontier_count"] == 0,
                "postclosure deadline/public prefix")
        cursor = resource["cursor"]
        if phase == "four_signed_transition_reconstruction":
            require(set(cursor) == {"state_id", "seen"} and
                    0 <= cursor["state_id"] <= public["state_count"] and
                    cursor["seen"] == public["state_count"],
                    "signed-transition resource cursor")
        elif phase == "coordinate_projection":
            require(set(cursor) == {"projection_id", "state_id"} and
                    cursor["projection_id"] in (1, 2, 3) and
                    0 <= cursor["state_id"] <= public["state_count"],
                    "coordinate resource cursor")
        elif phase == "pair_projection":
            require(set(cursor) == {"pair_projection_id", "state_id"} and
                    cursor["pair_projection_id"] in {"1,2", "1,3", "2,3"} and
                    0 <= cursor["state_id"] <= public["state_count"],
                    "pair resource cursor")
        else:
            require(set(cursor) == {"state_id"} and
                    0 <= cursor["state_id"] <= public["state_count"],
                    "Delta3 resource cursor")
    states = replay_published_prefix(
        context["model"], public, keys, parents, letters, resource,
        state_cap=state_cap, soft_seconds=soft_seconds)
    require(len(states) == len(keys) and
            public["frontier_count"] == len(keys) -
            public["cursor"]["state_id"],
            "resource exact frontier")
    return {"grade": "CROSS_CHECKED_BOUNDED_PREFIX_UNKNOWN",
            "cross_checked_census": False,
            "bounded_prefix_cross_checked": True,
            "state_count": len(keys), "section_replays": 0,
            "independent_positive_generator_order": None}


def validate_input(receipt: dict[str, Any], raw: bytes,
                   receipt_path: Path) -> dict[str, Any]:
    fixture = (ROOT / STATIC_FIXTURE).resolve()
    require(fixture.is_file() and fixture.stat().st_size ==
            STATIC_FIXTURE_BYTES and digest_file(fixture) ==
            STATIC_FIXTURE_SHA256 and raw == fixture.read_bytes() and
            receipt_path.read_bytes() == raw,
            "INPUT_STOP is the immutable static fixture only")
    require(receipt["mode"] == "static_fixture" and
            receipt["reason"] ==
            "LOCAL_EXECUTION_NOT_AUTHORIZED_STATIC_FIXTURE" and
            receipt["census"] is None and receipt["resource"] is None and
            receipt["unknowns"] == ["STATIC_FIXTURE_ONLY_NO_CENSUS"] and
            receipt["input_bindings"] == {
                "ordered_context_names": list(TARGET_ALIASES),
                "registry_context_ids": [1, 2, 3],
                "positive_generator_order": ["x", "y"],
                "state_key_width": STATE_KEY_WIDTH,
                "context_pair_blob_width": CONTEXT_PAIR_WIDTH,
                "executed": False},
            "static fixture fields")
    return {"grade": "INPUT_ONLY_NOT_A_CENSUS",
            "cross_checked_census": False,
            "bounded_prefix_cross_checked": False,
            "state_count": None, "section_replays": 0,
            "independent_positive_generator_order": None}


def validate_receipt_chain(receipt: dict[str, Any], raw: bytes,
                           receipt_path: Path, pins: dict[str, Any], *,
                           context: dict[str, Any] | None = None,
                           expected_caps: dict[str, Any] | None = None) \
        -> dict[str, Any]:
    """The single production validation path used by runtime and selftest."""
    validate_envelope(receipt, pins, expected_caps=expected_caps)
    if receipt["terminal"] == TERMINAL_INPUT:
        require(context is None, "INPUT_STOP has no reconstructed context")
        return validate_input(receipt, raw, receipt_path)
    require(context is not None, "census terminal requires typed context")
    if receipt["terminal"] == TERMINAL_COMPLETE:
        return validate_complete(receipt, context)
    return validate_resource(receipt, context)


def h27_mul(left: tuple[int, int, int],
            right: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = left
    d, e, f = right
    return ((a + d) % 3, (b + e) % 3, (c + f + a * e) % 3)


def h27_inverse(value: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = value
    return ((-a) % 3, (-b) % 3, (-c + a * b) % 3)


class ToyProductionE4:
    """A 154-byte literal carrier for H_27 x C_2 fixture coordinates."""
    def __init__(self) -> None:
        self.identity = self.encode((0, 0, 0), 0)

    @staticmethod
    def encode(hvalue: tuple[int, int, int], flag: int) \
            -> tuple[bytes, bytes]:
        a, b, c = hvalue
        require(all(x in (0, 1, 2) for x in (a, b, c)) and flag in (0, 1),
                "toy E4 coordinate range")
        return (bytes((a, b, c, flag)) + bytes(140), bytes(10))

    @staticmethod
    def decode(value: Any) -> tuple[tuple[int, int, int], int]:
        require(type(value) is tuple and len(value) == 2 and
                type(value[0]) is bytes and len(value[0]) == 144 and
                type(value[1]) is bytes and len(value[1]) == 10 and
                value[0][4:] == bytes(140) and value[1] == bytes(10),
                "toy E4 literal representation")
        a, b, c, flag = value[0][:4]
        require(all(x in (0, 1, 2) for x in (a, b, c)) and flag in (0, 1),
                "toy E4 decoded coordinate range")
        return (a, b, c), flag

    def mul(self, left: Any, right: Any) -> Any:
        lh, lf = self.decode(left)
        rh, rf = self.decode(right)
        return self.encode(h27_mul(lh, rh), lf ^ rf)

    def inverse(self, value: Any) -> Any:
        hvalue, flag = self.decode(value)
        return self.encode(h27_inverse(hvalue), flag)


class ToyProductionModel:
    """H_27 x C_2 linked inside three literal 154-byte coordinates."""
    def __init__(self) -> None:
        self.e4 = ToyProductionE4()
        one = (0, 0, 0)
        a = (1, 0, 0)
        b = (0, 1, 0)
        self.identity = tuple(self.e4.identity for _ in range(3))
        self.generators = {
            1: (self.e4.encode(a, 1), self.e4.encode(a, 0),
                self.e4.encode(one, 1)),
            2: (self.e4.encode(b, 0), self.e4.encode(b, 0),
                self.e4.encode(one, 0)),
        }
        self.inverses = {
            letter: tuple(self.e4.inverse(x) for x in row)
            for letter, row in self.generators.items()}

    def mul(self, left: Any, right: Any) -> Any:
        return tuple(self.e4.mul(left[i], right[i]) for i in range(3))

    def step(self, state: Any, signed_letter: int) -> Any:
        table = self.generators if signed_letter > 0 else self.inverses
        return self.mul(state, table[abs(signed_letter)])

    def eval(self, word: Sequence[int]) -> Any:
        value = self.identity
        for letter in word:
            value = self.step(value, int(letter))
        return value

    def key(self, state: Any) -> bytes:
        raw = b"".join(element_blob(value) for value in state)
        require(len(raw) == STATE_KEY_WIDTH, "toy triple key width")
        return raw

    def coordinate_step(self, value: Any, coordinate: int,
                        signed_letter: int) -> Any:
        table = self.generators if signed_letter > 0 else self.inverses
        return self.e4.mul(value, table[abs(signed_letter)][coordinate])


class ToyProductionDelta:
    """The exact H_27 quotient of the bounded production-shaped fixture."""
    def __init__(self, model: ToyProductionModel) -> None:
        self.model = model
        self.generators = {1: (1, 0, 0), 2: (0, 1, 0)}
        self.inverses = {letter: h27_inverse(value)
                         for letter, value in self.generators.items()}
        self.states = [(0, 0, 0)]
        self.ids = {self.states[0]: 0}
        self.sections = [[]]
        tree: dict[int, tuple[int, int]] = {}
        head = 0
        while head < len(self.states):
            for letter in (1, 2):
                following = h27_mul(self.states[head], self.generators[letter])
                if following not in self.ids:
                    target = len(self.states)
                    self.ids[following] = target
                    self.states.append(following)
                    self.sections.append(self.sections[head] + [letter])
                    tree[target] = (head, letter)
            head += 1
        require(len(self.states) == 27, "toy Delta order")
        self.positive: dict[tuple[int, int], int] = {}
        self.schreier_words: list[list[int]] = []
        for state_id, state in enumerate(self.states):
            for letter in (1, 2):
                target = self.ids[h27_mul(state, self.generators[letter])]
                self.positive[(state_id, letter)] = target
                if tree.get(target) != (state_id, letter):
                    self.schreier_words.append(reduce_word(
                        self.sections[state_id] + [letter] +
                        inverse_word(self.sections[target])))
        require(len(self.schreier_words) == 28, "toy Schreier count")

    def step(self, state_id: int, letter: int) -> int:
        if letter > 0:
            return self.positive[(state_id, letter)]
        return self.ids[h27_mul(self.states[state_id],
                                self.inverses[-letter])]

    def project(self, state: Any) -> int:
        hvalue, flag = self.model.e4.decode(state[1])
        require(flag == 0 and hvalue in self.ids, "toy Delta projection")
        return self.ids[hvalue]

    @staticmethod
    def key(state: tuple[int, int, int]) -> bytes:
        return bytes(state) + bytes(27)


def fixture_pending_frontier(keys: Sequence[bytes], cursor: dict[str, Any]) \
        -> dict[str, Any]:
    """Fixture writer implementation; production validator uses another one."""
    header = canonical_bytes({"cursor": cursor,
                              "positive_generator_order": [1, 2]})
    accumulator = hashlib.sha256()
    accumulator.update(b"D174-PENDING-POSITIVE-FRONTIER-V1\0")
    accumulator.update(struct.pack("<I", len(header)))
    accumulator.update(header)
    task_count = 0
    first_state = int(cursor["state_id"])
    first_generator = int(cursor["generator_index"])
    for state_id, key in enumerate(keys[first_state:], first_state):
        for generator_index, letter in enumerate((1, 2)):
            if state_id == first_state and generator_index < first_generator:
                continue
            accumulator.update(struct.pack(
                "<IBB", state_id, generator_index, letter))
            accumulator.update(key)
            task_count += 1
    return {
        "definition": (
            "cursor header followed by ordered pending records "
            "<u32-state-id,u8-generator-index,u8-letter,462-byte-state-key>"),
        "digest_domain": "D174-PENDING-POSITIVE-FRONTIER-V1",
        "cursor": copy.deepcopy(cursor),
        "positive_generator_order": [1, 2],
        "record_width": 468,
        "pending_task_count": task_count,
        "sha256": accumulator.hexdigest(),
    }


def fixture_enumeration(model: ToyProductionModel, state_cap: int) \
        -> dict[str, Any]:
    states = [model.identity]
    keys = [model.key(model.identity)]
    ids = {keys[0]: 0}
    parents = [0xffffffff]
    letters = [0]
    depths = [0]
    head = 0
    generator_index = 0
    cursor: dict[str, Any] | None = None
    while head < len(states):
        letter = (1, 2)[generator_index]
        following = model.step(states[head], letter)
        key = model.key(following)
        if key not in ids:
            if len(states) >= state_cap:
                cursor = {
                    "state_id": head, "generator_index": generator_index,
                    "next_positive_letter": letter,
                    "attempted_novel_state_sha256": digest_raw(key),
                }
                break
            ids[key] = len(states)
            states.append(following)
            keys.append(key)
            parents.append(head)
            letters.append(letter)
            depths.append(depths[head] + 1)
        generator_index += 1
        if generator_index == 2:
            generator_index = 0
            head += 1
    transitions = None
    status = "UNKNOWN_RESOURCE"
    if cursor is None:
        require(head == len(states), "toy positive closure")
        cursor = {"state_id": len(states), "generator_index": 0}
        transitions = []
        for state in states:
            transitions.extend(ids[model.key(model.step(state, letter))]
                               for letter in SIGNED_ORDER)
        status = "COMPLETE"
    return {
        "status": status, "states": states, "keys": keys, "ids": ids,
        "parents": parents, "letters": letters, "depths": depths,
        "head": head, "cursor": cursor, "transitions": transitions,
    }


def fixture_enumeration_public(run: dict[str, Any]) -> dict[str, Any]:
    keys = run["keys"]
    parents = run["parents"]
    letters = run["letters"]
    raw = b"".join(keys)
    parent_raw = b"".join(struct.pack("<I", value) for value in parents)
    letter_raw = bytes(letters)
    transition_pack = (None if run["transitions"] is None else
                       pack_u32(run["transitions"],
                                "four-signed-transition-targets"))
    cursor = copy.deepcopy(run["cursor"])
    sorted_digest = digest_raw(b"".join(sorted(keys)))
    discovery_digest = digest_raw(raw)
    return {
        "status": run["status"],
        "positive_generator_order": [1, 2],
        "four_signed_transition_order": list(SIGNED_ORDER),
        "state_key_definition": (
            "literal 154-byte E4 coordinate blobs concatenated in "
            "fxy,fxz,fyz order"),
        "state_key_width": STATE_KEY_WIDTH,
        "state_count": len(keys),
        "seen_state_count": len(keys),
        "frontier_count": len(keys) - int(run["head"]),
        "frontier_count_definition": (
            "discovered states with state_id at or after cursor.state_id"),
        "cursor": cursor,
        "pending_positive_frontier": fixture_pending_frontier(keys, cursor),
        "identity_state_key_hex": keys[0].hex(),
        "discovery_states": pack_fixed(
            raw, len(keys), STATE_KEY_WIDTH,
            "positive-BFS-discovery-order-literal-triple-states"),
        "discovery_order_sha256": discovery_digest,
        "discovery_prefix_state_count": len(keys),
        "discovery_prefix_sha256": discovery_digest,
        "canonical_sorted_state_set_sha256": sorted_digest,
        "seen_state_set_sha256": sorted_digest,
        "parents_u32": pack_u32(parents, "positive-BFS-parent-state-id"),
        "parent_letters_u8": pack_u8(
            letters, "actual-positive-generator-on-parent-edge"),
        "section_parent_sha256": digest_raw(parent_raw + letter_raw),
        "section_statistics": {
            "minimum_length": min(run["depths"]),
            "maximum_length": max(run["depths"]),
            "mean_length_numerator": sum(run["depths"]),
            "mean_length_denominator": len(run["depths"]),
        },
        "four_signed_transitions_u32": transition_pack,
        "all_four_signed_transitions_reconstructed":
            run["transitions"] is not None,
    }


def fixture_binding(model: ToyProductionModel) -> dict[str, Any]:
    marked = []
    for word in ([1], [2], [-1], [-2], [1, 2]):
        marked.append({"word": list(word),
                       "triple_key_hex": model.key(model.eval(word)).hex()})
    canaries = [{
        "transcript_index": index, "layer": index % 3,
        "ordinal": index + 1, "word_kind": "r_word",
        "word_sha256": digest_obj([1, 2] * (index + 1)),
        "triple_key_sha256": digest_raw(
            model.key(model.eval([1, 2] * (index + 1)))),
    } for index in range(20)]
    return {
        "ordered_context_names": list(TARGET_ALIASES),
        "registry_context_ids": [1, 2, 3],
        "context_pair_serialization": (
            "left 154-byte E4 blob followed by right 154-byte E4 blob"),
        "context_pair_blob_width": CONTEXT_PAIR_WIDTH,
        "context_pair_blobs_hex": [bytes(CONTEXT_PAIR_WIDTH).hex()] * 3,
        "positive_generator_order": ["x", "y"],
        "marked_triple_generator_keys_hex": [
            model.key(model.generators[i]).hex() for i in (1, 2)],
        "marked_word_cross_checks": marked,
        "task172_relation_canaries": canaries,
        "task172_relation_canary_count": 20,
        "task168_Delta3_order": 27,
        "task168_ordered_schreier_words_sha256":
            TASK168_SCHREIER_WORDS_SHA,
        "exact_pair_alias_and_marked_value_binding": True,
    }


def seal_fixture_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    answer = copy.deepcopy(receipt)
    answer.pop("self_digest_sha256", None)
    answer["self_digest_sha256"] = digest_obj(answer)
    return answer


def fixture_receipt_base(pins: dict[str, Any], caps: dict[str, Any],
                         binding: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": SCHEMA, "mode": "census",
        "grade": "CANDIDATE_PENDING_INDEPENDENT_CHECKER",
        "terminal": TERMINAL_INPUT, "status": "INPUT_STOP",
        "reason": "UNSET",
        "source": {"path": PRODUCER_PATH.as_posix(),
                   "bytes": PRODUCER_BYTES, "sha256": PRODUCER_SHA256},
        "pins": pins, "registered_caps": copy.deepcopy(caps),
        "input_bindings": copy.deepcopy(binding), "census": None,
        "resource": None,
        "selftest": {"executed": True,
                     "results_claimed_before_execution": False},
        "boundaries": copy.deepcopy(BOUNDARIES),
        "scope": {
            "simultaneous_context_image_census_only": True,
            "linked_Delta_E_not_replaced_by_E4_cubed": True,
            "complete_fibres_enable_but_do_not_execute_v118_correlation": True,
        },
        "GHA_dispatched": False, "unknowns": [],
    }


def fixture_complete_receipt(model: ToyProductionModel,
                             delta: ToyProductionDelta,
                             pins: dict[str, Any], state_cap: int) \
        -> tuple[dict[str, Any], dict[str, Any]]:
    run = fixture_enumeration(model, state_cap)
    require(run["status"] == "COMPLETE" and len(run["states"]) == 54,
            "toy complete linked order")
    context = {"model": model, "delta": delta,
               "expected_binding": fixture_binding(model),
               "state_cap": state_cap,
               "soft_deadline_seconds": SOFT_DEADLINE_SECONDS}
    budget = CheckBudget()
    projections = expected_projection(
        model, run["states"], run["keys"], run["parents"],
        run["letters"], budget)
    quotient = expected_delta(delta, run["states"], run["keys"],
                              run["transitions"], budget)
    receipt = fixture_receipt_base(
        pins, registered_caps(state_cap), context["expected_binding"])
    receipt.update({
        "terminal": TERMINAL_COMPLETE, "status": "COMPLETE",
        "reason": "FINITE_POSITIVE_BFS_AND_ALL_CENSUS_GATES_CLOSED",
        "census": {
            "enumeration": fixture_enumeration_public(run),
            "order_Delta_E": len(run["states"]),
            "projections": projections, "Delta3_quotient": quotient,
            "raw_direct_stream_column_count": 6441 * len(run["states"]),
            "raw_direct_stream_formula": "6441*|Delta_E|",
            "raw_direct_stream_overflow_safe": True,
            "bounded_prefix_only": False,
        },
        "resource": {
            "reason": None, "phase": "complete", "state_cap": state_cap,
            "soft_deadline_seconds": SOFT_DEADLINE_SECONDS,
            "elapsed_seconds_at_receipt": 0.0,
        },
        "unknowns": [],
    })
    return seal_fixture_receipt(receipt), context


def fixture_resource_receipt(model: ToyProductionModel,
                             delta: ToyProductionDelta,
                             pins: dict[str, Any], state_cap: int) \
        -> tuple[dict[str, Any], dict[str, Any]]:
    run = fixture_enumeration(model, state_cap)
    require(run["status"] == "UNKNOWN_RESOURCE" and
            len(run["states"]) == state_cap,
            "toy honest cap before novel insert")
    binding = fixture_binding(model)
    context = {"model": model, "delta": delta,
               "expected_binding": binding, "state_cap": state_cap,
               "soft_deadline_seconds": SOFT_DEADLINE_SECONDS}
    receipt = fixture_receipt_base(
        pins, registered_caps(state_cap), binding)
    receipt.update({
        "terminal": TERMINAL_RESOURCE, "status": "UNKNOWN_RESOURCE",
        "reason": "STATE_CAP_BEFORE_NOVEL_INSERT",
        "census": {
            "enumeration": fixture_enumeration_public(run),
            "order_Delta_E": None, "projections": None,
            "Delta3_quotient": None,
            "raw_direct_stream_column_count": None,
            "bounded_prefix_only": True,
        },
        "resource": {
            "reason": "state_cap", "phase": "positive_BFS",
            "cursor": copy.deepcopy(run["cursor"]),
            "state_cap": state_cap,
            "soft_deadline_seconds": SOFT_DEADLINE_SECONDS,
            "elapsed_seconds_at_receipt": 0.0,
            "prefix_replayable_without_order_inference": True,
        },
        "unknowns": [
            "FINITE_CENSUS_DID_NOT_REACH_A_CHECKED_COMPLETE_RECEIPT"],
    })
    return seal_fixture_receipt(receipt), context


def expect_reject(action: Any, label: str) -> None:
    try:
        action()
    except (RuntimeError, ValueError, KeyError, TypeError, zlib.error):
        return
    raise RuntimeError("mutation accepted: " + label)


def repack_mutation(row: dict[str, Any], offset: int,
                    replacement: int) -> dict[str, Any]:
    raw = unpack_fixed(row, count=row["count"], width=row["record_width"],
                       semantic=row["semantic"])
    changed = bytearray(raw)
    changed[offset] = replacement
    return pack_fixed(bytes(changed), row["count"], row["record_width"],
                      row["semantic"])


def fixture_and_mutations() -> dict[str, Any]:
    pins = {"bounded_production_fixture": {
        "path": "checker-internal/H27xC2", "bytes": 0,
        "sha256": digest_raw(b"D174-H27xC2-production-shaped-fixture-v1")}}
    model = ToyProductionModel()
    delta = ToyProductionDelta(model)
    baseline, context = fixture_complete_receipt(model, delta, pins, 64)
    resource, resource_context = fixture_resource_receipt(
        model, delta, pins, 8)
    baseline_raw = canonical_bytes(baseline) + b"\n"
    resource_raw = canonical_bytes(resource) + b"\n"
    complete_result = validate_receipt_chain(
        baseline, baseline_raw, ROOT / "checker-internal-complete.json", pins,
        context=context, expected_caps=registered_caps(64))
    resource_result = validate_receipt_chain(
        resource, resource_raw, ROOT / "checker-internal-resource.json", pins,
        context=resource_context, expected_caps=registered_caps(8))

    fixture_path = (ROOT / STATIC_FIXTURE).resolve()
    input_raw = fixture_path.read_bytes()
    input_receipt = json.loads(input_raw.decode("ascii"))
    input_result = validate_receipt_chain(
        input_receipt, input_raw, fixture_path, input_receipt["pins"])

    projections = baseline["census"]["projections"]
    require(complete_result["grade"] == "CROSS_CHECKED" and
            resource_result["grade"] ==
            "CROSS_CHECKED_BOUNDED_PREFIX_UNKNOWN" and
            input_result["grade"] == "INPUT_ONLY_NOT_A_CENSUS" and
            baseline["census"]["order_Delta_E"] == 54 and
            [row["image_order"]
             for row in projections["coordinate_projections"]] == [54, 27, 2]
            and [row["kernel_order"]
                 for row in projections["coordinate_projections"]] ==
            [1, 2, 27] and
            [row["image_order"]
             for row in projections["pair_projections"]] == [54, 54, 54] and
            [row["kernel_order"]
             for row in projections["pair_projections"]] == [1, 1, 1],
            "production-shaped fixture baseline profiles")
    require(resource["census"]["enumeration"]
            ["pending_positive_frontier"]["pending_task_count"] > 0,
            "UNKNOWN_RESOURCE fixture has a nonempty pending frontier")
    require(model.mul(model.generators[1], model.generators[2]) !=
            model.mul(model.generators[2], model.generators[1]),
            "fixture genuinely nonabelian")
    labels: list[str] = []

    def mutate(label: str, action: Any) -> None:
        candidate = copy.deepcopy(baseline)
        action(candidate)
        candidate = seal_fixture_receipt(candidate)
        raw = canonical_bytes(candidate) + b"\n"
        expect_reject(lambda: validate_receipt_chain(
            candidate, raw, ROOT / "checker-internal-mutation.json", pins,
            context=context, expected_caps=registered_caps(64)), label)
        labels.append(label)

    def mutate_unknown(label: str, action: Any) -> None:
        candidate = copy.deepcopy(resource)
        action(candidate)
        candidate = seal_fixture_receipt(candidate)
        raw = canonical_bytes(candidate) + b"\n"
        expect_reject(lambda: validate_receipt_chain(
            candidate, raw, ROOT / "checker-internal-resource-mutation.json",
            pins, context=resource_context,
            expected_caps=registered_caps(8)), label)
        labels.append(label)

    enumeration = lambda row: row["census"]["enumeration"]
    projection = lambda row: row["census"]["projections"]
    quotient = lambda row: row["census"]["Delta3_quotient"]

    def mutate_state(row: dict[str, Any]) -> None:
        public = enumeration(row)
        public["discovery_states"] = repack_mutation(
            public["discovery_states"], 0, 255)

    def mutate_transition(row: dict[str, Any]) -> None:
        public = enumeration(row)
        public["four_signed_transitions_u32"] = repack_mutation(
            public["four_signed_transitions_u32"], 0, 255)

    def mutate_parent_letter(row: dict[str, Any]) -> None:
        public = enumeration(row)
        packed = public["parent_letters_u8"]
        raw = unpack_fixed(packed, count=packed["count"], width=1,
                           semantic=packed["semantic"])
        replacement = 2 if raw[1] != 2 else 1
        public["parent_letters_u8"] = repack_mutation(
            packed, 1, replacement)

    def mutate_kernel(row: dict[str, Any]) -> None:
        target = projection(row)["coordinate_projections"][0]
        packed = target["kernel_membership"]
        flags = unpack_bits(
            packed, count=enumeration(row)["state_count"],
            semantic="coordinate-1-kernel-membership")
        flags[0] = not flags[0]
        target["kernel_membership"] = pack_bits(
            flags, "coordinate-1-kernel-membership")

    def mutate_delta_row(row: dict[str, Any]) -> None:
        target = quotient(row)["state_to_Delta3_id_u8"]
        target_raw = unpack_fixed(
            target, count=target["count"], width=1,
            semantic="Delta_E-discovery-state-to-Delta3-id")
        replacement = 1 if target_raw[0] != 1 else 2
        quotient(row)["state_to_Delta3_id_u8"] = repack_mutation(
            target, 0, replacement)

    mutate("generator_order_binding", lambda row: enumeration(row).__setitem__(
        "positive_generator_order", [2, 1]))
    mutate("one_triple_coordinate", lambda row:
           row["input_bindings"]["marked_triple_generator_keys_hex"].__setitem__(
               0, "00" + row["input_bindings"]
               ["marked_triple_generator_keys_hex"][0][2:]))
    mutate("one_state_blob_byte", mutate_state)
    mutate("one_transition_target", mutate_transition)
    mutate("one_parent_letter", mutate_parent_letter)
    for index in range(3):
        mutate(f"coordinate_projection_id_{index + 1}",
               lambda row, i=index:
               projection(row)["coordinate_projections"][i].__setitem__(
                   "projection_id", 9))
    for index in range(3):
        mutate(f"pair_projection_id_{index + 1}",
               lambda row, i=index:
               projection(row)["pair_projections"][i].__setitem__(
                   "pair_projection_id", "9,9"))
    mutate("one_kernel_membership", mutate_kernel)
    mutate("one_Delta3_quotient_row", mutate_delta_row)
    mutate("one_count", lambda row: enumeration(row).__setitem__(
        "state_count", 55))
    mutate_unknown("one_pending_frontier_digest", lambda row:
                   enumeration(row)["pending_positive_frontier"].__setitem__(
                       "sha256", "0" * 64))
    for terminal in ("R07_TARGET6_SOLVED", "R07_ALL_SEVEN_SOLVED",
                     "R07_FAKE_FOUND", "R07_IHARA_WITNESS_FOUND",
                     "R07_FULL_D2_CORRELATION_COMPLETE"):
        mutate("forbidden_terminal_" + terminal,
               lambda row, token=terminal: row.__setitem__("terminal", token))
    require(len(labels) == 20, "registered production-path mutation count")
    return {
        "fixture_group": "H27xC2 linked in (H27xC2)xH27xC2",
        "production_validator_chain": [
            "validate_envelope", "decode_enumeration",
            "replay_published_complete_or_prefix",
            "validate_complete_or_validate_resource_or_validate_input"],
        "production_shaped_complete_passed": True,
        "production_shaped_unknown_resource_passed": True,
        "immutable_input_stop_fixture_passed": True,
        "pending_frontier_independently_rebuilt": True,
        "nonabelian": True, "linked_image_order": 54,
        "direct_product_coordinate_image_order": 2916,
        "coordinate_image_orders": [54, 27, 2],
        "coordinate_kernel_orders": [1, 2, 27],
        "pair_image_orders": [54, 54, 54],
        "pair_kernel_orders": [1, 1, 1],
        "common_kernel_order": 1,
        "honest_cap_unknown": True,
        "corrupted_parent_rejected": "one_parent_letter" in labels,
        "mutation_count": len(labels), "mutations": labels,
    }


def atomic_immutable_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    require(not path.exists(), "refuse to overwrite checker verdict")
    handle, name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp",
                                    dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    require(path.read_bytes() == raw, "verdict readback")


def seal_verdict(row: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(row)
    result["self_digest_sha256"] = digest_obj(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt")
    parser.add_argument("--verdict")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        require(args.receipt is None and args.verdict is None,
                "selftest file isolation")
        result = fixture_and_mutations()
        print(SELFTEST_MARKER + " " + json.dumps(
            result, sort_keys=True, separators=(",", ":")))
        return 0
    require(type(args.receipt) is str and args.receipt,
            "explicit --receipt required")
    receipt_path = Path(args.receipt)
    if not receipt_path.is_absolute():
        receipt_path = ROOT / receipt_path
    receipt_path = receipt_path.resolve()
    raw = receipt_path.read_bytes()
    receipt = json.loads(raw.decode("ascii"))
    pins = pin_inputs()
    context = None if receipt["terminal"] == TERMINAL_INPUT else \
        build_context(pins)
    result = validate_receipt_chain(
        receipt, raw, receipt_path, pins, context=context)
    verdict = seal_verdict({
        "schema": VERDICT_SCHEMA,
        "receipt": {"path": (receipt_path.relative_to(ROOT).as_posix()
                              if ROOT in receipt_path.parents else
                              receipt_path.as_posix()),
                    "bytes": len(raw), "sha256": digest_raw(raw)},
        "terminal": receipt["terminal"],
        **result,
        "producer_imported": False,
        "producer_helpers_shared": False,
        "claims": copy.deepcopy(BOUNDARIES),
    })
    if args.verdict is not None:
        verdict_path = Path(args.verdict)
        if not verdict_path.is_absolute():
            verdict_path = ROOT / verdict_path
        verdict_raw = canonical_bytes(verdict) + b"\n"
        atomic_immutable_write(verdict_path.resolve(), verdict_raw)
    print(CHECKER_MARKER + " status=" + receipt["status"] +
          " grade=" + result["grade"] +
          " receipt_sha256=" + digest_raw(raw))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
