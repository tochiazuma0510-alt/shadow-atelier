#!/usr/bin/env python3
"""Bounded target6 simultaneous-context image census (task 174).

The checked-in default is an immutable INPUT_STOP fixture.  The finite census
is opt-in and must be written to an explicit non-fixture output.  No result in
this file is a target6 solution or a correction-orbit computation.
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
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SELF_PATH = Path("search/d972_r07_target6_context_image_census_v1.py")
STATIC_FIXTURE = Path(
    "search/certs/d972_r07_target6_context_image_census_"
    "preflight_v1_20260827.json")
SCHEMA = "d972-r07-target6-context-image-census/v1"
PRODUCER_MARKER = "D174_TARGET6_CONTEXT_IMAGE_CENSUS_V1_PRODUCER_PASS"
SELFTEST_MARKER = "D174_TARGET6_CONTEXT_IMAGE_CENSUS_V1_SELFTEST_PASS"
TERMINAL_COMPLETE = "R07_TARGET6_CONTEXT_IMAGE_CENSUS_COMPLETE"
TERMINAL_RESOURCE = "R07_TARGET6_CONTEXT_IMAGE_CENSUS_UNKNOWN_RESOURCE"
TERMINAL_INPUT = "R07_TARGET6_CONTEXT_IMAGE_CENSUS_INPUT_STOP"
TERMINALS = {TERMINAL_COMPLETE, TERMINAL_RESOURCE, TERMINAL_INPUT}

STATE_CAP = 2_000_000
SOFT_DEADLINE_SECONDS = 9_000.0
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
SIGNED_TRANSITION_ORDER = (1, 2, -1, -2)
BOUNDARIES = {
    "full_D2_correlation_run": False,
    "full_correction_orbit_correlation_run": False,
    "target6_solved": False,
    "all_seven_solved": False,
    "cofinal_compatibility_proved": False,
    "fake": False,
    "Ihara_witness": False,
}


# task169 is deliberately absent.  The only imported mathematical modules are
# the frozen task163 core underlying task168 and the frozen 157ec E4 arithmetic
# authenticated by the task157ee receipt.  All parsed artifacts are pinned too.
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


class InputStop(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, reason: str, phase: str,
                 cursor: dict[str, Any]) -> None:
        super().__init__(reason)
        self.reason = reason
        self.phase = phase
        self.cursor = cursor


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def digest_raw(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(receipt: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(receipt)
    out.pop("self_digest_sha256", None)
    out["self_digest_sha256"] = digest_obj(out)
    return out


def verify_self_digest(receipt: dict[str, Any], label: str) -> None:
    require(type(receipt) is dict and
            type(receipt.get("self_digest_sha256")) is str,
            label + " self digest field")
    work = copy.deepcopy(receipt)
    claimed = work.pop("self_digest_sha256")
    require(claimed == digest_obj(work), label + " self digest")


def pin_inputs() -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for label, (rel, size, digest) in PINS.items():
        path = ROOT / rel
        if not path.is_file() or path.stat().st_size != size or \
                digest_file(path) != digest:
            raise InputStop("PIN_DRIFT:" + rel.as_posix())
        rows[label] = {"path": rel.as_posix(), "bytes": size,
                       "sha256": digest}
    return rows


def source_record() -> dict[str, Any]:
    path = ROOT / SELF_PATH
    require(path.is_file(), "producer source missing")
    return {"path": SELF_PATH.as_posix(), "bytes": path.stat().st_size,
            "sha256": digest_file(path)}


def load_module(label: str, rel: Path, expected: str) -> Any:
    require(label not in sys.modules, "fresh module label")
    path = ROOT / rel
    require(digest_file(path) == expected, "module pre-import pin")
    spec = importlib.util.spec_from_file_location(label, path)
    require(spec is not None and spec.loader is not None, "module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[label] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(label, None)
        raise
    require(digest_file(path) == expected, "module post-import pin")
    return module


def element_blob(value: Any) -> bytes:
    raw = bytes(value[0]) + bytes(value[1])
    require(len(raw) == E4_BLOB_WIDTH, "literal E4 blob width")
    return raw


def context_pair_blob(pair: Sequence[Any]) -> bytes:
    require(len(pair) == 2, "context pair arity")
    raw = element_blob(pair[0]) + element_blob(pair[1])
    require(len(raw) == CONTEXT_PAIR_WIDTH, "literal context pair width")
    return raw


def pack_bytes(raw: bytes, *, count: int, width: int,
               semantic: str) -> dict[str, Any]:
    require(count >= 0 and width > 0 and len(raw) == count * width,
            semantic + " packed shape")
    compressed = zlib.compress(raw, 9)
    return {
        "encoding": "zlib+base64/raw-fixed-width/v1",
        "semantic": semantic,
        "count": count,
        "record_width": width,
        "raw_bytes": len(raw),
        "raw_sha256": digest_raw(raw),
        "compressed_bytes": len(compressed),
        "compressed_sha256": digest_raw(compressed),
        "base64": base64.b64encode(compressed).decode("ascii"),
    }


def pack_u32(values: Iterable[int], semantic: str) -> dict[str, Any]:
    rows = [int(x) for x in values]
    require(all(0 <= x <= 0xffffffff for x in rows), semantic + " u32")
    raw = b"".join(struct.pack("<I", x) for x in rows)
    return pack_bytes(raw, count=len(rows), width=4, semantic=semantic)


def pack_u8(values: Iterable[int], semantic: str) -> dict[str, Any]:
    rows = [int(x) for x in values]
    require(all(0 <= x <= 255 for x in rows), semantic + " u8")
    return pack_bytes(bytes(rows), count=len(rows), width=1,
                      semantic=semantic)


def pack_bits(flags: Sequence[bool], semantic: str) -> dict[str, Any]:
    raw = bytearray((len(flags) + 7) // 8)
    for index, flag in enumerate(flags):
        if flag:
            raw[index // 8] |= 1 << (index % 8)
    compressed = zlib.compress(bytes(raw), 9)
    return {
        "encoding": "zlib+base64/lsb0-bitset/v1",
        "semantic": semantic,
        "bit_count": len(flags),
        "true_count": sum(bool(x) for x in flags),
        "raw_bytes": len(raw),
        "raw_sha256": digest_raw(bytes(raw)),
        "compressed_bytes": len(compressed),
        "compressed_sha256": digest_raw(compressed),
        "base64": base64.b64encode(compressed).decode("ascii"),
    }


def pending_frontier_payload(keys: Sequence[bytes], cursor: dict[str, Any],
                             generator_order: Sequence[int]) \
        -> dict[str, Any]:
    """Bind the exact ordered positive-BFS work remaining at ``cursor``."""
    order = [int(x) for x in generator_order]
    require(order == [1, 2], "registered frontier generator order")
    state_id = cursor.get("state_id")
    generator_index = cursor.get("generator_index")
    require(type(state_id) is int and type(generator_index) is int and
            0 <= state_id <= len(keys), "frontier cursor state")
    if state_id == len(keys):
        require(generator_index == 0, "closed frontier cursor")
    else:
        require(generator_index in (0, 1), "frontier generator cursor")
    header = canonical_bytes({"cursor": cursor,
                              "positive_generator_order": order})
    digest = hashlib.sha256()
    digest.update(b"D174-PENDING-POSITIVE-FRONTIER-V1\0")
    digest.update(struct.pack("<I", len(header)))
    digest.update(header)
    task_count = 0
    for pending_state_id in range(state_id, len(keys)):
        first = generator_index if pending_state_id == state_id else 0
        for pending_generator_index in range(first, 2):
            letter = order[pending_generator_index]
            key = keys[pending_state_id]
            require(len(key) == STATE_KEY_WIDTH, "frontier state key width")
            digest.update(struct.pack(
                "<IBB", pending_state_id, pending_generator_index, letter))
            digest.update(key)
            task_count += 1
    return {
        "definition": (
            "cursor header followed by ordered pending records "
            "<u32-state-id,u8-generator-index,u8-letter,462-byte-state-key>"),
        "digest_domain": "D174-PENDING-POSITIVE-FRONTIER-V1",
        "cursor": copy.deepcopy(cursor),
        "positive_generator_order": order,
        "record_width": 6 + STATE_KEY_WIDTH,
        "pending_task_count": task_count,
        "sha256": digest.hexdigest(),
    }


class Budget:
    def __init__(self, seconds: float) -> None:
        require(0 < seconds <= SOFT_DEADLINE_SECONDS,
                "registered soft deadline")
        self.seconds = float(seconds)
        self.started = time.monotonic()
        self.checks = 0

    def elapsed(self) -> float:
        return time.monotonic() - self.started

    def check(self, phase: str, cursor: dict[str, Any], *,
              force: bool = False) -> None:
        self.checks += 1
        if not force and self.checks % 1024:
            return
        if self.elapsed() >= self.seconds:
            raise ResourceStop("soft_deadline", phase, cursor)


class RealModel:
    def __init__(self, e4: Any, contexts: Sequence[Sequence[Any]]) -> None:
        require(len(contexts) == 3, "three target contexts")
        self.e4 = e4
        self.contexts = [tuple(row) for row in contexts]
        self.identity = (e4.identity, e4.identity, e4.identity)
        self.generators = {
            letter: tuple(e4.eval([letter], pair) for pair in self.contexts)
            for letter in (1, 2)
        }
        self.inverse_generators = {
            letter: tuple(e4.inverse(x) for x in self.generators[letter])
            for letter in (1, 2)
        }
        require(len(self.state_key(self.identity)) == STATE_KEY_WIDTH,
                "triple state width")

    def mul(self, left: Any, right: Any) -> Any:
        return tuple(self.e4.mul(left[i], right[i]) for i in range(3))

    def step(self, state: Any, signed_letter: int) -> Any:
        letter = abs(int(signed_letter))
        require(letter in (1, 2), "signed F2 letter")
        generator = (self.generators if signed_letter > 0 else
                     self.inverse_generators)[letter]
        return self.mul(state, generator)

    def eval(self, word: Sequence[int]) -> Any:
        out = self.identity
        for letter in word:
            out = self.step(out, int(letter))
        return out

    def state_key(self, state: Any) -> bytes:
        raw = b"".join(element_blob(x) for x in state)
        require(len(raw) == STATE_KEY_WIDTH, "literal triple key width")
        return raw

    def coordinate_key(self, value: Any, coordinate: int) -> bytes:
        del coordinate
        return element_blob(value)

    def coordinate_identity_key(self, coordinate: int) -> bytes:
        del coordinate
        return element_blob(self.e4.identity)

    def coordinate_step(self, value: Any, coordinate: int,
                        signed_letter: int) -> Any:
        generator = (self.generators if signed_letter > 0 else
                     self.inverse_generators)[abs(signed_letter)][coordinate]
        return self.e4.mul(value, generator)


class DeltaQuotient:
    """Independent explicit Delta3 quotient attached to the real model."""
    def __init__(self, core: Any, e4: Any, model: RealModel,
                 expected_words: Sequence[Sequence[int]]) -> None:
        self.pc = e4.pc
        xbar, ybar, zbar = (e4.eval(list(word))[1]
                             for word in (core.X0, core.Y0, core.Z0))
        require(zbar == self.pc.inverse(self.pc.mul(ybar, xbar)),
                "Delta3 z convention")
        self.generators = {1: (xbar, xbar, ybar),
                           2: (ybar, zbar, zbar)}
        self.inverse_generators = {
            letter: tuple(self.pc.inverse(x) for x in row)
            for letter, row in self.generators.items()
        }
        require(tuple(x[1] for x in model.generators[1]) == self.generators[1]
                and tuple(x[1] for x in model.generators[2]) == self.generators[2],
                "marked Omega-to-Delta3 generator agreement")
        identity = (self.pc.one(), self.pc.one(), self.pc.one())
        self.states = [identity]
        self.ids = {identity: 0}
        self.sections: list[list[int]] = [[]]
        self.tree: dict[int, tuple[int, int]] = {}
        for state_id, state in enumerate(self.states):
            for letter in (1, 2):
                following = self.mul(state, self.generators[letter])
                if following not in self.ids:
                    require(len(self.states) < 27, "Delta3 enumeration cap")
                    target = len(self.states)
                    self.ids[following] = target
                    self.states.append(following)
                    self.sections.append(self.sections[state_id] + [letter])
                    self.tree[target] = (state_id, letter)
        require(len(self.states) == 27, "Delta3 exact order")
        self.positive: dict[tuple[int, int], int] = {}
        self.schreier_words: list[list[int]] = []
        for state_id, state in enumerate(self.states):
            for letter in (1, 2):
                target = self.ids[self.mul(state, self.generators[letter])]
                self.positive[(state_id, letter)] = target
                if self.tree.get(target) != (state_id, letter):
                    word = reduce_word(self.sections[state_id] + [letter] +
                                       inverse_word(self.sections[target]))
                    self.schreier_words.append(word)
        require(self.schreier_words == [list(x) for x in expected_words] and
                len(self.schreier_words) == 28 and
                digest_obj(self.schreier_words) == TASK168_SCHREIER_WORDS_SHA,
                "frozen task168 Schreier roster")

    def mul(self, left: Any, right: Any) -> Any:
        return tuple(self.pc.mul(left[i], right[i]) for i in range(3))

    def step_id(self, state_id: int, signed_letter: int) -> int:
        if signed_letter > 0:
            return self.positive[(state_id, signed_letter)]
        following = self.mul(self.states[state_id],
                             self.inverse_generators[-signed_letter])
        return self.ids[following]

    def project(self, state: Any) -> int:
        row = tuple(x[1] for x in state)
        require(row in self.ids, "literal Delta3 quotient row")
        return self.ids[row]

    def state_key(self, state: Any) -> bytes:
        raw = b"".join(bytes(x) for x in state)
        require(len(raw) == DELTA_STATE_WIDTH, "Delta3 row width")
        return raw


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        letter = int(raw)
        require(letter in (-2, -1, 1, 2), "F2 letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(x) for x in reversed(word)]


def section_word(parents: Sequence[int], letters: Sequence[int],
                 state_id: int) -> list[int]:
    require(0 <= state_id < len(parents) == len(letters), "section id")
    reverse: list[int] = []
    seen = 0
    while state_id:
        require(0 <= parents[state_id] < state_id and
                letters[state_id] in (1, 2), "section parent edge")
        reverse.append(letters[state_id])
        state_id = parents[state_id]
        seen += 1
        require(seen <= len(parents), "section parent cycle")
    return list(reversed(reverse))


def enumerate_positive(model: Any, budget: Any, *, state_cap: int,
                       generator_order: Sequence[int]) -> dict[str, Any]:
    require(tuple(generator_order) in ((1, 2), (2, 1)),
            "positive generator order")
    identity = model.identity
    identity_key = model.state_key(identity)
    states = [identity]
    keys = [identity_key]
    ids = {identity_key: 0}
    parents = [0xffffffff]
    letters = [0]
    depths = [0]
    head = 0
    generator_index = 0
    while head < len(states):
        try:
            budget.check("positive_BFS", {
                "state_id": head, "generator_index": generator_index,
                "seen": len(states)})
        except ResourceStop as stop:
            return {
                "status": "UNKNOWN_RESOURCE", "reason": stop.reason,
                "phase": stop.phase, "cursor": stop.cursor,
                "states": states, "keys": keys, "ids": ids,
                "parents": parents, "letters": letters,
                "depths": depths, "head": head,
                "generator_order": list(generator_order),
                "transitions": None,
            }
        letter = int(generator_order[generator_index])
        following = model.step(states[head], letter)
        key = model.state_key(following)
        if key not in ids:
            if len(states) >= state_cap:
                return {
                    "status": "UNKNOWN_RESOURCE", "reason": "state_cap",
                    "phase": "positive_BFS",
                    "cursor": {"state_id": head,
                               "generator_index": generator_index,
                               "next_positive_letter": letter,
                               "attempted_novel_state_sha256": digest_raw(key)},
                    "states": states, "keys": keys, "ids": ids,
                    "parents": parents, "letters": letters,
                    "depths": depths, "head": head,
                    "generator_order": list(generator_order),
                    "transitions": None,
                }
            target = len(states)
            ids[key] = target
            states.append(following)
            keys.append(key)
            parents.append(head)
            letters.append(letter)
            depths.append(depths[head] + 1)
        generator_index += 1
        if generator_index == len(generator_order):
            generator_index = 0
            head += 1
    transitions: list[list[int]] = []
    for state_id, state in enumerate(states):
        try:
            budget.check("four_signed_transition_reconstruction",
                         {"state_id": state_id, "seen": len(states)})
        except ResourceStop as stop:
            return {
                "status": "UNKNOWN_RESOURCE", "reason": stop.reason,
                "phase": stop.phase,
                "cursor": {"state_id": len(states), "generator_index": 0},
                "resource_cursor": stop.cursor,
                "states": states, "keys": keys, "ids": ids,
                "parents": parents, "letters": letters,
                "depths": depths, "head": head,
                "generator_order": list(generator_order),
                "transitions": None,
            }
        row = []
        for letter in SIGNED_TRANSITION_ORDER:
            key = model.state_key(model.step(state, letter))
            require(key in ids, "full signed closure")
            row.append(ids[key])
        transitions.append(row)
    return {
        "status": "COMPLETE", "reason": "closed", "phase": "closed",
        "cursor": {"state_id": len(states), "generator_index": 0},
        "states": states, "keys": keys, "ids": ids,
        "parents": parents, "letters": letters, "depths": depths,
        "head": head, "generator_order": list(generator_order),
        "transitions": transitions,
    }


def enumeration_public(run: dict[str, Any]) -> dict[str, Any]:
    keys = run["keys"]
    parents = run["parents"]
    letters = run["letters"]
    depths = run["depths"]
    raw_states = b"".join(keys)
    parent_raw = b"".join(struct.pack("<I", int(x)) for x in parents)
    letter_raw = bytes(int(x) for x in letters)
    transitions = run.get("transitions")
    transition_pack = None
    if transitions is not None:
        flat = [target for row in transitions for target in row]
        transition_pack = pack_u32(flat, "four-signed-transition-targets")
    frontier = pending_frontier_payload(
        keys, run["cursor"], run["generator_order"])
    sorted_state_digest = digest_raw(b"".join(sorted(keys)))
    discovery_digest = digest_raw(raw_states)
    return {
        "status": run["status"],
        "positive_generator_order": run["generator_order"],
        "four_signed_transition_order": list(SIGNED_TRANSITION_ORDER),
        "state_key_definition":
            "literal 154-byte E4 coordinate blobs concatenated in fxy,fxz,fyz order",
        "state_key_width": STATE_KEY_WIDTH,
        "state_count": len(keys),
        "seen_state_count": len(keys),
        "frontier_count": len(keys) - int(run["head"]),
        "frontier_count_definition":
            "discovered states with state_id at or after cursor.state_id",
        "cursor": copy.deepcopy(run["cursor"]),
        "pending_positive_frontier": frontier,
        "identity_state_key_hex": keys[0].hex(),
        "discovery_states": pack_bytes(
            raw_states, count=len(keys), width=STATE_KEY_WIDTH,
            semantic="positive-BFS-discovery-order-literal-triple-states"),
        "discovery_order_sha256": discovery_digest,
        "discovery_prefix_state_count": len(keys),
        "discovery_prefix_sha256": discovery_digest,
        "canonical_sorted_state_set_sha256": sorted_state_digest,
        "seen_state_set_sha256": sorted_state_digest,
        "parents_u32": pack_u32(parents, "positive-BFS-parent-state-id"),
        "parent_letters_u8": pack_u8(
            letters, "actual-positive-generator-on-parent-edge"),
        "section_parent_sha256": digest_raw(parent_raw + letter_raw),
        "section_statistics": {
            "minimum_length": min(depths),
            "maximum_length": max(depths),
            "mean_length_numerator": sum(depths),
            "mean_length_denominator": len(depths),
        },
        "four_signed_transitions_u32": transition_pack,
        "all_four_signed_transitions_reconstructed": transitions is not None,
    }


def lex_kernel_section(run: dict[str, Any], flags: Sequence[bool]) \
        -> dict[str, Any] | None:
    rows = sorted((run["keys"][i], i) for i, flag in enumerate(flags)
                  if flag and i != 0)
    if not rows:
        return None
    key, state_id = rows[0]
    word = section_word(run["parents"], run["letters"], state_id)
    return {"state_key_hex": key.hex(), "state_id": state_id,
            "section_word": word, "section_word_sha256": digest_obj(word)}


def projection_payload(model: RealModel, run: dict[str, Any],
                       budget: Budget) -> dict[str, Any]:
    states = run["states"]
    keys = run["keys"]
    order = len(states)
    coordinate_rows = []
    for coordinate in range(3):
        image_values: dict[bytes, Any] = {}
        counts: Counter[bytes] = Counter()
        identity = model.coordinate_identity_key(coordinate)
        kernel = []
        for state_id, state in enumerate(states):
            budget.check("coordinate_projection", {
                "projection_id": coordinate + 1, "state_id": state_id})
            key = model.coordinate_key(state[coordinate], coordinate)
            image_values.setdefault(key, state[coordinate])
            counts[key] += 1
            kernel.append(key == identity)
        image_keys = sorted(image_values)
        kernel_order = sum(kernel)
        require(set(counts.values()) == {kernel_order} and
                order == len(image_keys) * kernel_order,
                "coordinate uniform fibre/Lagrange")
        for value in image_values.values():
            for letter in SIGNED_TRANSITION_ORDER:
                target = model.coordinate_key(
                    model.coordinate_step(value, coordinate, letter),
                    coordinate)
                require(target in image_values,
                        "coordinate literal signed-generator closure")
        kernel_keys = sorted(keys[i] for i, flag in enumerate(kernel) if flag)
        coordinate_rows.append({
            "projection_id": coordinate + 1,
            "coordinate_name": TARGET_ALIASES[coordinate],
            "image_order": len(image_keys),
            "kernel_order": kernel_order,
            "image_set": pack_bytes(
                b"".join(image_keys), count=len(image_keys),
                width=E4_BLOB_WIDTH,
                semantic=f"coordinate-{coordinate + 1}-literal-image-set"),
            "kernel_membership": pack_bits(
                kernel, f"coordinate-{coordinate + 1}-kernel-membership"),
            "canonical_image_digest_sha256": digest_raw(b"".join(image_keys)),
            "canonical_kernel_state_set_sha256":
                digest_raw(b"".join(kernel_keys)),
            "uniform_fibre_size": kernel_order,
            "uniform_fibre_histogram": {
                str(size): number
                for size, number in sorted(Counter(counts.values()).items())},
            "uniform_fibres_checked": True,
            "lagrange_identity_checked": True,
            "literal_four_signed_generator_closure_checked": True,
            "lex_first_nonidentity_kernel_section":
                lex_kernel_section(run, kernel),
        })

    pair_rows = []
    for left, right in ((0, 1), (0, 2), (1, 2)):
        pair_id = f"{left + 1},{right + 1}"
        image_values: dict[bytes, tuple[Any, Any]] = {}
        counts = Counter()
        identity = (model.coordinate_identity_key(left) +
                    model.coordinate_identity_key(right))
        kernel = []
        for state_id, state in enumerate(states):
            budget.check("pair_projection", {
                "pair_projection_id": pair_id, "state_id": state_id})
            key = (model.coordinate_key(state[left], left) +
                   model.coordinate_key(state[right], right))
            image_values.setdefault(key, (state[left], state[right]))
            counts[key] += 1
            kernel.append(key == identity)
        image_keys = sorted(image_values)
        kernel_order = sum(kernel)
        require(set(counts.values()) == {kernel_order} and
                order == len(image_keys) * kernel_order,
                "pair uniform fibre/Lagrange")
        for value in image_values.values():
            for letter in SIGNED_TRANSITION_ORDER:
                target = (
                    model.coordinate_key(model.coordinate_step(
                        value[0], left, letter), left) +
                    model.coordinate_key(model.coordinate_step(
                        value[1], right, letter), right))
                require(target in image_values,
                        "pair literal signed-generator closure")
        kernel_keys = sorted(keys[i] for i, flag in enumerate(kernel) if flag)
        pair_rows.append({
            "pair_projection_id": pair_id,
            "coordinate_ids": [left + 1, right + 1],
            "image_order": len(image_keys),
            "kernel_order": kernel_order,
            "image_set": pack_bytes(
                b"".join(image_keys), count=len(image_keys),
                width=2 * E4_BLOB_WIDTH,
                semantic=f"pair-{pair_id}-literal-image-set"),
            "kernel_membership": pack_bits(
                kernel, f"pair-{pair_id}-kernel-membership"),
            "canonical_image_digest_sha256": digest_raw(b"".join(image_keys)),
            "canonical_kernel_state_set_sha256":
                digest_raw(b"".join(kernel_keys)),
            "uniform_fibre_size": kernel_order,
            "uniform_fibre_histogram": {
                str(size): number
                for size, number in sorted(Counter(counts.values()).items())},
            "uniform_fibres_checked": True,
            "lagrange_identity_checked": True,
            "literal_four_signed_generator_closure_checked": True,
            "lex_first_nonidentity_kernel_section":
                lex_kernel_section(run, kernel),
        })

    coordinate_keys = [[element_blob(state[i]) for state in states]
                       for i in range(3)]
    equality_matrix = [[coordinate_keys[i] == coordinate_keys[j]
                        for j in range(3)] for i in range(3)]
    identity_blob = element_blob(model.e4.identity)
    common = [all(element_blob(state[i]) == identity_blob for i in range(3))
              for state in states]
    require(sum(common) == 1 and common[0],
            "common three-coordinate kernel identity")
    return {
        "coordinate_projections": coordinate_rows,
        "pair_projections": pair_rows,
        "coordinate_map_equality_matrix": equality_matrix,
        "equal_coordinate_map_pairs": [
            [i + 1, j + 1] for i in range(3) for j in range(i + 1, 3)
            if equality_matrix[i][j]],
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


def delta_payload(model: RealModel, delta: DeltaQuotient,
                  run: dict[str, Any], budget: Budget) -> dict[str, Any]:
    mapping: list[int] = []
    for state_id, state in enumerate(run["states"]):
        budget.check("Delta3_quotient", {"state_id": state_id})
        mapping.append(delta.project(state))
    counts = Counter(mapping)
    require(set(counts) == set(range(27)), "Delta3 literal surjectivity")
    fibre = len(run["states"]) // 27
    require(len(run["states"]) == 27 * fibre and
            set(counts.values()) == {fibre}, "Delta3 uniform fibres")
    transitions = run["transitions"]
    require(transitions is not None, "Delta3 complete transition table")
    for state_id, row in enumerate(transitions):
        for position, letter in enumerate(SIGNED_TRANSITION_ORDER):
            require(mapping[row[position]] ==
                    delta.step_id(mapping[state_id], letter),
                    "Delta3 transition homomorphism")
    delta_rows = [delta.state_key(state) for state in delta.states]
    kernel = [value == 0 for value in mapping]
    kernel_keys = sorted(run["keys"][i] for i, flag in enumerate(kernel)
                         if flag)
    return {
        "definition":
            "three exact E4 coordinates followed by literal Pi4[3] PC projection",
        "order_Delta3": 27,
        "marked_generator_agreement": True,
        "surjective_onto_all_27_literal_states": True,
        "not_inferred_from_divisibility": True,
        "canonical_state_rows": pack_bytes(
            b"".join(delta_rows), count=27, width=DELTA_STATE_WIDTH,
            semantic="Delta3-canonical-positive-BFS-state-rows"),
        "positive_BFS_transversal_words": delta.sections,
        "positive_BFS_transversal_words_sha256": digest_obj(delta.sections),
        "ordered_schreier_words": delta.schreier_words,
        "ordered_schreier_words_sha256": digest_obj(delta.schreier_words),
        "schreier_generator_count": 28,
        "state_to_Delta3_id_u8": pack_u8(
            mapping, "Delta_E-discovery-state-to-Delta3-id"),
        "quotient_row_digest_sha256": digest_raw(bytes(mapping)),
        "kernel_order": sum(kernel),
        "kernel_membership": pack_bits(kernel, "Delta3-kernel-membership"),
        "canonical_kernel_state_set_sha256":
            digest_raw(b"".join(kernel_keys)),
        "uniform_fibre_size": fibre,
        "uniform_fibre_histogram": {
            str(size): number
            for size, number in sorted(Counter(counts.values()).items())},
        "all_four_signed_transitions_respected": True,
    }


def select_task172_canaries(receipt: dict[str, Any]) -> list[dict[str, Any]]:
    transcript = receipt["fox_canaries"]["transcript"]
    selected = []
    for transcript_index, row in enumerate(transcript):
        word = row.get("r_word")
        if type(word) is list and word:
            require(all(int(x) in (-2, -1, 1, 2) for x in word),
                    "task172 relation canary word")
            selected.append({
                "transcript_index": transcript_index,
                "layer": row["layer"], "ordinal": row["ordinal"],
                "word_kind": "r_word", "word": [int(x) for x in word],
                "word_sha256": digest_obj(word),
            })
        if len(selected) == 20:
            break
    require(len(selected) == 20, "twenty task172 relation canaries")
    return selected


def build_context(pins: dict[str, Any]) -> dict[str, Any]:
    old = load_module(
        "_d174_producer_frozen_e4_arithmetic", PINS["e4_arithmetic"][0],
        PINS["e4_arithmetic"][2])
    core = load_module(
        "_d174_producer_frozen_task168_core", PINS["task168_core"][0],
        PINS["task168_core"][2])
    q3 = json.loads((ROOT / PINS["q3"][0]).read_text(encoding="utf-8"))
    require(q3.get("schema") == "d972-b345-q-chief/v1", "q3 schema")
    _, e4, _ = old.reconstruct_quotients(q3)
    contexts, aliases, context_public = old.cheap_context_registry(e4)
    require(len(contexts) == 31 and len(aliases) == 46 and
            context_public["context_rows_sha256"] == CONTEXT_ROWS_SHA and
            context_public["named_use_mapping_sha256"] == ALIAS_ROWS_SHA,
            "frozen context registry")

    joint_receipt = json.loads(
        (ROOT / PINS["task157ee_receipt"][0]).read_text(encoding="utf-8"))
    require(joint_receipt.get("schema") ==
            "d972-b345-joint-kernel-qstar-closure/v1" and
            joint_receipt.get("terminal_token") ==
            "B345_JOINT_KERNEL_QSTAR_CLOSED" and
            joint_receipt.get("context_registry") == context_public,
            "task157ee full receipt context binding")

    task172 = json.loads(
        (ROOT / PINS["task172_receipt"][0]).read_text(encoding="utf-8"))
    require(task172.get("schema") ==
            "d972-r07-full-e4-orbit-preflight/v7" and
            task172.get("terminal_token") ==
            "R07_FULL_E4_ORBIT_PREFLIGHT_READY" and
            task172["contexts"]["rows_sha256"] == CONTEXT_ROWS_SHA and
            task172["fox_canaries"]["status"] == "PASS" and
            task172["fox_canaries"]["pairs"] >= 101,
            "task172-v7 receipt")

    task168 = json.loads(
        (ROOT / PINS["task168_receipt"][0]).read_text(encoding="utf-8"))
    verify_self_digest(task168, "task168 receipt")
    require(task168.get("schema") ==
            "d972-r07-760-l3-target6-legal-coefficients/v1" and
            task168.get("preflight_state") ==
            "R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_PREFLIGHT_READY" and
            task168.get("producer_source") == pins["task168_producer"],
            "task168 frozen receipt")

    source_pairs = ((core.X0, core.Y0), (core.X0, core.Z0),
                    (core.Y0, core.Z0))
    literal_pairs = [(e4.eval(list(left)), e4.eval(list(right)))
                     for left, right in source_pairs]
    pair_blobs = [context_pair_blob(pair) for pair in literal_pairs]
    context_rows = context_public["contexts"]
    exact_ids = []
    for pair, raw in zip(literal_pairs, pair_blobs):
        matches = [row["context_id"] for row in context_rows
                   if row["left_hex"] == element_blob(pair[0]).hex() and
                   row["right_hex"] == element_blob(pair[1]).hex()]
        require(len(matches) == 1, "unique target context row")
        exact_ids.append(matches[0])
        require(len(raw) == CONTEXT_PAIR_WIDTH,
                "explicit context pair serialization")
    require(exact_ids == [1, 2, 3], "target context registry ids")
    alias_rows = {row["name"]: row["context_id"]
                  for row in context_public["named_uses"]}
    require([alias_rows[name] for name in TARGET_ALIASES] == [1, 2, 3],
            "target alias rows")
    target_contexts = [contexts[index - 1] for index in exact_ids]
    require(all(context_pair_blob(target_contexts[i]) == pair_blobs[i]
                for i in range(3)), "literal pair registry binding")
    bindings172 = task172["contexts"]["target6_bindings"]
    require(len(bindings172) == 3 and all(
        bindings172[i]["alias"] == TARGET_ALIASES[i] and
        bindings172[i]["registry_id"] == i + 1 and
        bindings172[i]["context_blob"] == pair_blobs[i].hex()
        for i in range(3)), "task172 target binding replay")

    expected_words, delta_public = core.delta_and_schreier(core, e4)
    require(delta_public["order_Delta"] == 27 and
            delta_public["schreier_generator_count"] == 28 and
            delta_public["schreier_words_sha256"] ==
            TASK168_SCHREIER_WORDS_SHA and
            digest_obj(expected_words) == TASK168_SCHREIER_WORDS_SHA,
            "task168 Delta3 public binding")
    model = RealModel(e4, target_contexts)
    delta = DeltaQuotient(core, e4, model, expected_words)

    marked_words = ([1], [2], [-1], [-2], [1, 2])
    marked_checks = []
    for word in marked_words:
        predecessor_value = tuple(e4.eval(word, pair)
                                  for pair in target_contexts)
        fresh_value = model.eval(word)
        require(predecessor_value == fresh_value,
                "marked predecessor/fresh evaluator agreement")
        marked_checks.append({"word": list(word),
                              "triple_key_hex": model.state_key(fresh_value).hex()})
    canaries = select_task172_canaries(task172)
    for row in canaries:
        predecessor_value = tuple(e4.eval(row["word"], pair)
                                  for pair in target_contexts)
        fresh_value = model.eval(row["word"])
        require(predecessor_value == fresh_value,
                "task172 canary predecessor/fresh evaluator agreement")
        row["triple_key_sha256"] = digest_raw(model.state_key(fresh_value))
        row.pop("word")
    return {
        "old": old, "core": core, "e4": e4, "model": model,
        "delta": delta, "task172": task172,
        "input_bindings": {
            "ordered_context_names": list(TARGET_ALIASES),
            "registry_context_ids": exact_ids,
            "context_pair_serialization":
                "left 154-byte E4 blob followed by right 154-byte E4 blob",
            "context_pair_blob_width": CONTEXT_PAIR_WIDTH,
            "context_pair_blobs_hex": [x.hex() for x in pair_blobs],
            "positive_generator_order": ["x", "y"],
            "marked_triple_generator_keys_hex": [
                model.state_key(model.generators[i]).hex() for i in (1, 2)],
            "marked_word_cross_checks": marked_checks,
            "task172_relation_canaries": canaries,
            "task172_relation_canary_count": len(canaries),
            "task168_Delta3_order": 27,
            "task168_ordered_schreier_words_sha256":
                TASK168_SCHREIER_WORDS_SHA,
            "exact_pair_alias_and_marked_value_binding": True,
        },
    }


def base_receipt(mode: str, pins: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "mode": mode,
        "grade": "CANDIDATE_PENDING_INDEPENDENT_CHECKER",
        "terminal": TERMINAL_INPUT,
        "status": "INPUT_STOP",
        "reason": "UNSET",
        "source": source_record(),
        "pins": pins,
        "registered_caps": {
            "state_cap": STATE_CAP,
            "soft_deadline_seconds": int(SOFT_DEADLINE_SECONDS),
            "producer_outer_timeout_seconds": PROCESS_OUTER_SECONDS,
            "checker_outer_timeout_seconds": PROCESS_OUTER_SECONDS,
            "workflow_upload_margin_seconds":
                WORKFLOW_UPLOAD_MARGIN_SECONDS,
            "total_outer_caps_plus_margin_seconds":
                2 * PROCESS_OUTER_SECONDS +
                WORKFLOW_UPLOAD_MARGIN_SECONDS,
            "raw_stream_count_formula": "6441*|Delta_E|",
            "overflow_safe_integer_arithmetic": True,
        },
        "input_bindings": None,
        "census": None,
        "resource": None,
        "selftest": {"executed": False,
                     "results_claimed_before_execution": False},
        "boundaries": copy.deepcopy(BOUNDARIES),
        "scope": {
            "simultaneous_context_image_census_only": True,
            "linked_Delta_E_not_replaced_by_E4_cubed": True,
            "complete_fibres_enable_but_do_not_execute_v118_correlation": True,
        },
        "GHA_dispatched": False,
        "unknowns": [],
    }


def static_receipt(pins: dict[str, Any]) -> dict[str, Any]:
    receipt = base_receipt("static_fixture", pins)
    receipt.update({
        "terminal": TERMINAL_INPUT,
        "status": "INPUT_STOP",
        "reason": "LOCAL_EXECUTION_NOT_AUTHORIZED_STATIC_FIXTURE",
        "input_bindings": {
            "ordered_context_names": list(TARGET_ALIASES),
            "registry_context_ids": [1, 2, 3],
            "positive_generator_order": ["x", "y"],
            "state_key_width": STATE_KEY_WIDTH,
            "context_pair_blob_width": CONTEXT_PAIR_WIDTH,
            "executed": False,
        },
        "unknowns": ["STATIC_FIXTURE_ONLY_NO_CENSUS"],
    })
    return seal(receipt)


def unknown_receipt(pins: dict[str, Any], context: dict[str, Any],
                    run: dict[str, Any], budget: Budget,
                    stop: ResourceStop | None = None) -> dict[str, Any]:
    receipt = base_receipt("census", pins)
    reason = run.get("reason", "soft_deadline")
    phase = run.get("phase", "positive_BFS")
    cursor = copy.deepcopy(run.get("resource_cursor", run.get("cursor", {})))
    if stop is not None:
        reason, phase, cursor = stop.reason, stop.phase, stop.cursor
    public_run = dict(run)
    public_run["status"] = "UNKNOWN_RESOURCE"
    public_run["reason"] = reason
    public_run["phase"] = phase
    public_run["transitions"] = None
    receipt.update({
        "terminal": TERMINAL_RESOURCE,
        "status": "UNKNOWN_RESOURCE",
        "reason": ("STATE_CAP_BEFORE_NOVEL_INSERT" if reason == "state_cap"
                   else "SOFT_DEADLINE_AT_REPLAYABLE_CURSOR"),
        "input_bindings": context["input_bindings"],
        "census": {
            "enumeration": enumeration_public(public_run),
            "order_Delta_E": None,
            "projections": None,
            "Delta3_quotient": None,
            "raw_direct_stream_column_count": None,
            "bounded_prefix_only": True,
        },
        "resource": {
            "reason": reason,
            "phase": phase,
            "cursor": cursor,
            "state_cap": STATE_CAP,
            "soft_deadline_seconds": int(SOFT_DEADLINE_SECONDS),
            "elapsed_seconds_at_receipt": budget.elapsed(),
            "prefix_replayable_without_order_inference": True,
        },
        "unknowns": ["FINITE_CENSUS_DID_NOT_REACH_A_CHECKED_COMPLETE_RECEIPT"],
    })
    return seal(receipt)


def complete_receipt(pins: dict[str, Any], context: dict[str, Any],
                     run: dict[str, Any], budget: Budget) -> dict[str, Any]:
    projections = projection_payload(context["model"], run, budget)
    quotient = delta_payload(context["model"], context["delta"], run, budget)
    order = len(run["states"])
    raw_count = 6441 * order
    require(raw_count // 6441 == order, "overflow-safe raw count")
    receipt = base_receipt("census", pins)
    receipt.update({
        "terminal": TERMINAL_COMPLETE,
        "status": "COMPLETE",
        "reason": "FINITE_POSITIVE_BFS_AND_ALL_CENSUS_GATES_CLOSED",
        "input_bindings": context["input_bindings"],
        "census": {
            "enumeration": enumeration_public(run),
            "order_Delta_E": order,
            "projections": projections,
            "Delta3_quotient": quotient,
            "raw_direct_stream_column_count": raw_count,
            "raw_direct_stream_formula": "6441*|Delta_E|",
            "raw_direct_stream_overflow_safe": True,
            "bounded_prefix_only": False,
        },
        "resource": {
            "reason": None, "phase": "complete",
            "state_cap": STATE_CAP,
            "soft_deadline_seconds": int(SOFT_DEADLINE_SECONDS),
            "elapsed_seconds_at_receipt": budget.elapsed(),
        },
        "unknowns": [],
    })
    return seal(receipt)


def atomic_immutable_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    require(not path.exists(), "refuse to overwrite output")
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
    require(path.read_bytes() == raw, "output readback")


def perm_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(right[left[i]] for i in range(3))


def perm_inv(value: tuple[int, ...]) -> tuple[int, ...]:
    out = [0, 0, 0]
    for i, image in enumerate(value):
        out[image] = i
    return tuple(out)


class ToyModel:
    """S3 x C2 embedded as a linked subgroup of S3 x C2 x C2."""
    def __init__(self) -> None:
        identity_perm = (0, 1, 2)
        self.identity = (identity_perm, 0, 0)
        x_s3 = (1, 0, 2)
        y_s3 = (1, 2, 0)
        self.generators = {1: (x_s3, 0, 1),
                           2: (y_s3, 1, 1)}
        self.inverse_generators = {
            letter: self.inverse(row) for letter, row in self.generators.items()}

    def mul(self, left: Any, right: Any) -> Any:
        return (perm_mul(left[0], right[0]), left[1] ^ right[1],
                left[2] ^ right[2])

    def inverse(self, value: Any) -> Any:
        return (perm_inv(value[0]), value[1], value[2])

    def step(self, state: Any, signed_letter: int) -> Any:
        table = self.generators if signed_letter > 0 else self.inverse_generators
        return self.mul(state, table[abs(signed_letter)])

    def eval(self, word: Sequence[int]) -> Any:
        out = self.identity
        for letter in word:
            out = self.step(out, int(letter))
        return out

    def state_key(self, state: Any) -> bytes:
        return bytes(state[0]) + bytes([state[1], state[2]])


class UnlimitedBudget:
    def check(self, phase: str, cursor: dict[str, Any], *,
              force: bool = False) -> None:
        del phase, cursor, force


def fixture_selftest() -> dict[str, Any]:
    model = ToyModel()
    run = enumerate_positive(model, UnlimitedBudget(), state_cap=32,
                             generator_order=(1, 2))
    require(run["status"] == "COMPLETE" and len(run["states"]) == 12,
            "toy linked image order")
    require(model.mul(model.generators[1], model.generators[2]) !=
            model.mul(model.generators[2], model.generators[1]),
            "toy image nonabelian")
    images = [set() for _ in range(3)]
    kernels = [0, 0, 0]
    pair_kernels = [0, 0, 0]
    for state in run["states"]:
        rows = [bytes(state[0]), bytes([state[1]]), bytes([state[2]])]
        for i in range(3):
            images[i].add(rows[i])
            identity = bytes((0, 1, 2)) if i == 0 else b"\0"
            kernels[i] += int(rows[i] == identity)
        pair_kernels[0] += int(rows[0] == bytes((0, 1, 2)) and rows[1] == b"\0")
        pair_kernels[1] += int(rows[0] == bytes((0, 1, 2)) and rows[2] == b"\0")
        pair_kernels[2] += int(rows[1] == b"\0" and rows[2] == b"\0")
    require([len(x) for x in images] == [6, 2, 2] and
            kernels == [2, 6, 6] and pair_kernels == [1, 1, 3] and
            len(run["states"]) < 6 * 2 * 2,
            "toy linked projection census")
    capped = enumerate_positive(model, UnlimitedBudget(), state_cap=4,
                                generator_order=(1, 2))
    require(capped["status"] == "UNKNOWN_RESOURCE" and
            capped["reason"] == "state_cap" and
            len(capped["states"]) == 4,
            "honest cap before novel insertion")
    bad_letters = list(run["letters"])
    target = next(i for i in range(1, len(bad_letters))
                  if bad_letters[i] == 1)
    bad_letters[target] = 2
    caught = False
    try:
        word = section_word(run["parents"], bad_letters, target)
        require(model.state_key(model.eval(word)) == run["keys"][target],
                "corrupted parent accepted")
    except RuntimeError:
        caught = True
    require(caught, "corrupted parent rejection")
    return {
        "group": "S3xC2 linked in S3xC2xC2",
        "nonabelian": True,
        "linked_image_order": 12,
        "direct_product_order": 24,
        "coordinate_image_orders": [6, 2, 2],
        "coordinate_kernel_orders": kernels,
        "pair_kernel_orders": pair_kernels,
        "nontrivial_pair_kernel_order": 3,
        "common_three_coordinate_kernel_order": 1,
        "cap_terminal": "UNKNOWN_RESOURCE",
        "corrupted_parent_rejected": True,
    }


def write_and_report(receipt: dict[str, Any], output: Path) -> None:
    verify_self_digest(receipt, "task174 receipt")
    raw = canonical_bytes(receipt) + b"\n"
    atomic_immutable_write(output, raw)
    print(receipt["terminal"])
    print(PRODUCER_MARKER + " terminal=" + receipt["terminal"] +
          " sha256=" + digest_raw(raw) + " bytes=" + str(len(raw)))


def parse_output(raw: str) -> Path:
    path = Path(raw)
    resolved = path if path.is_absolute() else ROOT / path
    return resolved.resolve()


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--run-census", action="store_true")
    mode.add_argument("--selftest", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.selftest:
        require(args.output is None, "selftest does not write repository files")
        result = fixture_selftest()
        print(SELFTEST_MARKER + " " + json.dumps(
            result, sort_keys=True, separators=(",", ":")))
        return 0
    require(type(args.output) is str and args.output,
            "explicit --output is required")
    output = parse_output(args.output)
    static_path = (ROOT / STATIC_FIXTURE).resolve()
    if args.run_census:
        require(output != static_path,
                "full census must not overwrite checked-in static fixture")
    else:
        require(output == static_path or ROOT not in output.parents,
                "static fixture output must be checked fixture or external")
    pins = pin_inputs()
    if not args.run_census:
        write_and_report(static_receipt(pins), output)
        return 0

    budget = Budget(SOFT_DEADLINE_SECONDS)
    context = build_context(pins)
    run: dict[str, Any]
    try:
        run = enumerate_positive(context["model"], budget,
                                 state_cap=STATE_CAP,
                                 generator_order=(1, 2))
    except ResourceStop as stop:
        run = {
            "status": "UNKNOWN_RESOURCE", "reason": "soft_deadline",
            "phase": stop.phase, "cursor": stop.cursor,
            "states": [context["model"].identity],
            "keys": [context["model"].state_key(context["model"].identity)],
            "ids": {context["model"].state_key(context["model"].identity): 0},
            "parents": [0xffffffff], "letters": [0], "depths": [0],
            "head": 0, "generator_order": [1, 2], "transitions": None,
        }
        write_and_report(unknown_receipt(
            pins, context, run, budget, stop), output)
        return 0
    if run["status"] == "UNKNOWN_RESOURCE":
        write_and_report(unknown_receipt(pins, context, run, budget), output)
        return 0
    try:
        receipt = complete_receipt(pins, context, run, budget)
    except ResourceStop as stop:
        receipt = unknown_receipt(pins, context, run, budget, stop)
    write_and_report(receipt, output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
