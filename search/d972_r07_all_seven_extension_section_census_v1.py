#!/usr/bin/env python3
"""Exact extension-section census for the frozen R07 all-seven family.

This program implements proof v125.  It deliberately enumerates Q0 once and
never enumerates the linked image Delta.  COMPLETE output is still only a
finite candidate receipt until the helper-nonshared checker accepts it.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import struct
import sys
import time
import zlib
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-all-seven-extension-section-census/v1"
PASS = "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"
UNKNOWN_RESOURCE = "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_RESOURCE"
UNKNOWN_INPUT = "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_INPUT"
FIXTURE = ROOT / "search/certs/d972_r07_all_seven_extension_section_census_preflight_v1_20260827.json"
FIXTURE_BYTES = 4350
FIXTURE_SHA256 = "b24827b10f8ceb0505802bf7065e2442d176b7b65ecb2066452941c2e7e0a471"
DEFAULT_Q3 = ROOT / "ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json"
DEFAULT_JOINT = ROOT / "ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json"
EXPECTED_Q0 = 1_469_664
EXPECTED_GAMMA = 243
COORDINATE_WIDTHS = [40] * 5 + [154] * 5
FAMILIES = [("ALL", tuple(range(10)))] + [(f"S{i}", (i,)) for i in range(10)]
COORDINATES = [
    {"index": 0, "type": "E3", "construction": "d_E(C21)", "context_id": 21,
     "source": "(x,y)", "role": "hexagon_fxy"},
    {"index": 1, "type": "E3", "construction": "d_E(C22)", "context_id": 22,
     "source": "(x,z)", "role": "hexagon_fxz"},
    {"index": 2, "type": "E3", "construction": "d_E(C23)", "context_id": 23,
     "source": "(y,z)", "role": "hexagon_fyz"},
    {"index": 3, "type": "E3", "construction": "d_E(C24)", "context_id": 24,
     "source": "(u,x)", "role": "hexagon_fux"},
    {"index": 4, "type": "E3", "construction": "d_E(C25)", "context_id": 25,
     "source": "(u,y)", "role": "hexagon_fuy"},
    {"index": 5, "type": "E4", "construction": "C1", "context_id": 1,
     "source": "b1/phi234", "role": "pentagon_b1"},
    {"index": 6, "type": "E4", "construction": "C27", "context_id": 27,
     "source": "b2/phi1_23_4", "role": "pentagon_b2"},
    {"index": 7, "type": "E4", "construction": "C21", "context_id": 21,
     "source": "b3/phi123", "role": "pentagon_b3"},
    {"index": 8, "type": "E4", "construction": "C26", "context_id": 26,
     "source": "b5/phi12_3_4", "role": "pentagon_b5_inverse_slot"},
    {"index": 9, "type": "E4", "construction": "C28", "context_id": 28,
     "source": "b4/phi1_2_34", "role": "pentagon_b4_inverse_slot"},
]

PINS = {
    "task176": ("sol/luna_task_176_r07_all_seven_extension_section_census_v1.md", 7054,
                "a1778c17c33e42880a6dd0c2480303a13702cb38950cf836a4ca9d8cca6fa332"),
    "e4_arithmetic": ("search/d972_b345_seedspan_triple4_v1.py", 535219,
                      "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
    "task157ee_producer": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945,
                           "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    "task157ee_checker": ("search/check_d972_b345_joint_kernel_qstar_closure_v2.py", 5942,
                          "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88"),
    "task157ee_driver": ("search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g", 3912,
                         "8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7"),
    "task157ee_task": ("sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md", 11226,
                       "64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4"),
    "task157ee_reply": ("sol/luna_reply_157ee_b345_joint_kernel_qstar_closure.md", 4118,
                        "53f20c2cb1395b8ff59ee961e1d5a14d55156a488eb6fa49edefed5dd7619eee"),
    "task157ee_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036,
                          "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    "q3": ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570,
           "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "proof108": ("sol/proof_pb4_eleven_relator_presentation_equality_v108.md", 6742,
                 "4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f"),
    "proof121": ("sol/proof_pb3_two_relator_presentation_equality_v121.md", 5762,
                 "efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5"),
    "proof122": ("sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md", 7939,
                 "daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348"),
    "proof125": ("sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md", 8545,
                 "b82c81e0a053658fdb48cbb4d3054a094a57a81b2fd5d0153bcd0735ef4852b3"),
    "task174_terminal_note": ("sol/luna_reply_174_r07_target6_context_image_census_v1.md", 13224,
                              "516d15d4ad73e9e2d8e564789e856224c35a30a235e46e87ad857cb20470b49f"),
}


class Reject(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    pass


class InputStop(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(canonical(value))


def file_identity(path: Path) -> tuple[int, str]:
    raw = path.read_bytes()
    return len(raw), sha_bytes(raw)


def public_pins() -> dict[str, dict[str, Any]]:
    return {name: {"path": row[0], "bytes": row[1], "sha256": row[2]}
            for name, row in PINS.items()}


def authenticate_pins(q3_path: Path, joint_path: Path) -> None:
    for name, (relative, size, digest) in PINS.items():
        path = ROOT / relative
        if name == "q3":
            path = q3_path.resolve()
        elif name == "task157ee_receipt":
            path = joint_path.resolve()
        if not path.is_file():
            raise InputStop(f"MISSING_PINNED_INPUT:{name}:{path}")
        require(file_identity(path) == (size, digest), f"pin mismatch {name}")


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"module spec {name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def pack(raw: bytes, record_width: int, record_count: int,
         meaning: str) -> dict[str, Any]:
    require(record_width >= 0 and record_count >= 0, "packed dimensions")
    require(len(raw) == record_width * record_count, "packed byte count")
    compressed = zlib.compress(raw, 9)
    return {
        "codec": "zlib+base64", "record_width_bytes": record_width,
        "record_count": record_count, "raw_bytes": len(raw),
        "raw_sha256": sha_bytes(raw), "compressed_bytes": len(compressed),
        "compressed_sha256": sha_bytes(compressed),
        "data": base64.b64encode(compressed).decode("ascii"), "meaning": meaning,
    }


def unpack(obj: dict[str, Any]) -> bytes:
    require(obj["codec"] == "zlib+base64", "packed codec")
    compressed = base64.b64decode(obj["data"], validate=True)
    require(len(compressed) == obj["compressed_bytes"] and
            sha_bytes(compressed) == obj["compressed_sha256"], "compressed binding")
    raw = zlib.decompress(compressed)
    require(len(raw) == obj["raw_bytes"] ==
            obj["record_width_bytes"] * obj["record_count"] and
            sha_bytes(raw) == obj["raw_sha256"], "raw binding")
    return raw


def seal(receipt: dict[str, Any]) -> dict[str, Any]:
    receipt = dict(receipt)
    receipt.pop("self_digest_sha256", None)
    receipt["self_digest_sha256"] = sha_obj(receipt)
    return receipt


def validate_envelope(receipt: dict[str, Any]) -> None:
    require(receipt.get("schema") == SCHEMA, "schema")
    claimed = receipt.get("self_digest_sha256")
    body = dict(receipt); body.pop("self_digest_sha256", None)
    require(isinstance(claimed, str) and claimed == sha_obj(body), "self digest")
    require(receipt.get("pins") == public_pins(), "pin ledger")
    require(receipt.get("coordinates") == COORDINATES, "typed coordinate ledger")
    require(receipt["coordinates"][0]["context_id"] ==
            receipt["coordinates"][7]["context_id"] == 21 and
            receipt["coordinates"][0]["type"] == "E3" and
            receipt["coordinates"][7]["type"] == "E4", "typed C21 reuse")
    terminal = receipt.get("terminal")
    require(terminal in {PASS, UNKNOWN_RESOURCE, UNKNOWN_INPUT}, "terminal")
    if terminal == PASS:
        require(receipt.get("status") == "COMPLETE" and
                isinstance(receipt.get("result"), dict) and
                receipt.get("reason") is None, "complete envelope")
    elif terminal == UNKNOWN_RESOURCE:
        require(receipt.get("status") == "UNKNOWN_RESOURCE" and
                receipt.get("result") is None and
                isinstance(receipt.get("reason"), str), "resource envelope")
    else:
        require(receipt.get("status") == "UNKNOWN_INPUT" and
                receipt.get("result") is None and
                isinstance(receipt.get("reason"), str), "input envelope")
    boundaries = receipt.get("boundaries", {})
    require(boundaries == {
        "all_seven_solution": False, "correction_word": False,
        "cofinal_lift": False, "fake": False, "Ihara_witness": False,
        "support_correlation_6441": False, "direct_Delta_enumeration": False,
    }, "claim boundary")


class Budget:
    def __init__(self, seconds: float) -> None:
        self.started = time.monotonic(); self.seconds = seconds

    def check(self, phase: str) -> None:
        if time.monotonic() - self.started > self.seconds:
            raise ResourceStop(f"DEADLINE:{phase}")

    def elapsed(self) -> float:
        return time.monotonic() - self.started


def blob(old: Any, value: Any) -> bytes:
    return bytes(old._element_blob(value))


def split_blob(raw: bytes, degree: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return tuple(raw[:degree]), tuple(raw[degree:])


def bit_get(bits: bytes | bytearray, index: int) -> bool:
    return bool(bits[index >> 3] & (1 << (index & 7)))


def bit_set(bits: bytearray, index: int) -> None:
    bits[index >> 3] |= 1 << (index & 7)


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-x for x in reversed(word)]


def q0_section_word(state: int, parents: Sequence[int], letters: bytes) -> list[int]:
    out: list[int] = []
    while state:
        out.append(int(letters[state]))
        state = int(parents[state])
    out.reverse()
    return out


def build_fine_deletion(e3: Any, e4: Any, budget: Budget) -> tuple[dict[bytes, bytes], dict[str, Any]]:
    pc3, pc4 = e3.pc, e4.pc
    source = [g[1] for g in e4.generators]
    target = [e3.generators[0][1], e3.generators[1][1], pc3.one(),
              e3.generators[2][1], pc3.one(), pc3.one()]
    states = [pc4.one()]; images = [pc3.one()]
    ids = {bytes(states[0]): 0}
    for sid, state in enumerate(states):
        if (sid & 1023) == 0:
            budget.check("fine_deletion")
        for sg, tg in zip(source, target):
            nxt = pc4.mul(state, sg); image = pc3.mul(images[sid], tg)
            key = bytes(nxt)
            prior = ids.get(key)
            if prior is None:
                ids[key] = len(states); states.append(nxt); images.append(image)
            else:
                require(images[prior] == image, "fine deletion path consistency")
    require(len(states) == 59049, "Pi4 full state count")
    table = {bytes(state): bytes(image) for state, image in zip(states, images)}
    for sg, tg in zip(source, target):
        require(table[bytes(sg)] == bytes(tg), "fine marked deletion")
    return table, {
        "method": "full_Pi4_marked_Cayley_homomorphism_reconstruction",
        "source_order": len(states), "target_pc_width": len(pc3.one()),
        "marked_images": [list(x) for x in target],
        "table_sha256": sha_bytes(b"".join(table[k] for k in sorted(table))),
    }


def coarse_delete(permutation: Sequence[int]) -> tuple[int, ...]:
    require(len(permutation) == 144, "Q4 degree")
    row = tuple(int(x) for x in permutation[108:144])
    require(all(108 <= x < 144 for x in row), "fourth block invariance")
    return tuple(x - 108 for x in row)


def make_deleter(old: Any, e3: Any, e4: Any, fine: dict[bytes, bytes],
                 q0_marked: Sequence[tuple[int, ...]]) -> tuple[Any, dict[str, Any]]:
    expected = [q0_marked[0], e3.generators[1][0], tuple(range(36)),
                q0_marked[1], tuple(range(36)), tuple(range(36))]
    actual = [coarse_delete(g[0]) for g in e4.generators]
    require(actual == expected, "coarse marked fourth-strand deletion")

    def delete(value: Any) -> Any:
        pc_key = bytes(value[1])
        require(pc_key in fine, "fine deletion domain")
        return coarse_delete(value[0]), tuple(fine[pc_key])

    for source, target in zip(e4.generators,
                              [e3.generators[0], e3.generators[1], e3.identity,
                               e3.generators[2], e3.identity, e3.identity]):
        require(delete(source) == target, "matched marked deletion")
    return delete, {
        "coarse_method": "literal_fourth_36_block_restriction",
        "coarse_marked_images_sha256": sha_obj([list(x) for x in actual]),
        "fine": None,
        "left_inverse_endpoint_marked_indices": [1, 2, 4],
        "v122_pinned_not_reproved": True,
    }


def projection(state: Any, delete: Any) -> tuple[Any, ...]:
    e4rows = state[1]
    return tuple([delete(e4rows[i - 1]) for i in (21, 22, 23, 24, 25)] +
                 [e4rows[i - 1] for i in (1, 27, 21, 26, 28)])


def tuple_key(old: Any, values: Sequence[Any]) -> tuple[bytes, ...]:
    return tuple(blob(old, x) for x in values)


def family_key(row: Sequence[bytes], indices: Sequence[int]) -> tuple[bytes, ...]:
    return tuple(row[i] for i in indices)


def family_mul(values: Sequence[Any], other: Sequence[Any], indices: Sequence[int],
               e3: Any, e4: Any) -> tuple[Any, ...]:
    return tuple((e3 if i < 5 else e4).mul(a, b)
                 for i, a, b in zip(indices, values, other))


def family_inverse(values: Sequence[Any], indices: Sequence[int],
                   e3: Any, e4: Any) -> tuple[Any, ...]:
    return tuple((e3 if i < 5 else e4).inverse(a) for i, a in zip(indices, values))


def family_identity(indices: Sequence[int], e3: Any, e4: Any) -> tuple[Any, ...]:
    return tuple(e3.identity if i < 5 else e4.identity for i in indices)


def validate_A(old: Any, name: str, indices: Sequence[int], rows: Sequence[tuple[Any, ...]],
               qmarks: Sequence[Sequence[Any]], e3: Any, e4: Any) -> dict[str, Any]:
    keys = {tuple_key(old, row) for row in rows}
    identity = family_identity(indices, e3, e4)
    require(tuple_key(old, identity) in keys, f"{name} A identity")
    inverse_ok = all(tuple_key(old, family_inverse(row, indices, e3, e4)) in keys
                     for row in rows)
    require(inverse_ok, f"{name} A inverses")
    for left in rows:
        for right in rows:
            require(tuple_key(old, family_mul(left, right, indices, e3, e4)) in keys,
                    f"{name} A closure")
    for row in rows:
        for letter in range(2):
            outer = tuple(qmarks[i][letter] for i in indices)
            inv_outer = family_inverse(outer, indices, e3, e4)
            conj = family_mul(family_mul(inv_outer, row, indices, e3, e4),
                              outer, indices, e3, e4)
            require(tuple_key(old, conj) in keys, f"{name} A normality")
    return {"identity": True, "closure": True, "inverses": True,
            "normal_under_section_x_y": True}


def make_translation(permutation: Sequence[int]) -> bytes:
    table = bytearray(range(256))
    for i, value in enumerate(permutation):
        table[i] = int(value)
    return bytes(table)


def enumerate_q0_sections(old: Any, q0_marked: Sequence[tuple[int, ...]],
                          coordinate_marks: Sequence[Sequence[Any]],
                          e3: Any, e4: Any, budget: Budget) -> tuple[
                              list[bytes], dict[bytes, int], list[int], bytes,
                              list[bytearray], list[tuple[int, int, int]]]:
    identity = bytes(range(36))
    generators = [bytes(x) for x in q0_marked]
    qtables = [make_translation(x) for x in generators]
    states = [identity]; ids = {identity: 0}; parents = [0]; letters = bytearray([0])
    coordinate_values = [bytearray(blob(old, e3.identity if i < 5 else e4.identity))
                         for i in range(10)]
    right_tables: list[list[bytes]] = []
    for i in range(10):
        right_tables.append([make_translation(coordinate_marks[i][j][0]) for j in range(2)])
    pc_cache: dict[tuple[int, int, bytes], bytes] = {}
    duplicate_edges: list[tuple[int, int, int]] = []

    for sid, state in enumerate(states):
        if (sid & 4095) == 0:
            budget.check("Q0_discovery")
        for letter in range(2):
            nxt = state.translate(qtables[letter])
            prior = ids.get(nxt)
            new_blobs: list[bytes] = []
            for i, width in enumerate(COORDINATE_WIDTHS):
                degree = 36 if i < 5 else 144
                left = bytes(coordinate_values[i][sid * width:(sid + 1) * width])
                left_perm, left_pc = split_blob(left, degree)
                right = coordinate_marks[i][letter]
                perm_raw = bytes(left_perm).translate(right_tables[i][letter])
                cache_key = (i, letter, bytes(left_pc))
                pc_raw = pc_cache.get(cache_key)
                if pc_raw is None:
                    pc = e3.pc if i < 5 else e4.pc
                    pc_raw = bytes(pc.mul(left_pc, right[1]))
                    pc_cache[cache_key] = pc_raw
                new_blobs.append(perm_raw + pc_raw)
            if prior is None:
                prior = len(states); ids[nxt] = prior; states.append(nxt)
                parents.append(sid); letters.append(letter + 1)
                for store, value in zip(coordinate_values, new_blobs):
                    store.extend(value)
            elif len(duplicate_edges) < 256 and prior != sid:
                duplicate_edges.append((sid, letter + 1, prior))
    require(len(states) == EXPECTED_Q0 and len(ids) == EXPECTED_Q0,
            "Q0 exact discovery order")
    require(all(len(store) == EXPECTED_Q0 * width
                for store, width in zip(coordinate_values, COORDINATE_WIDTHS)),
            "section store dimensions")
    return states, ids, parents, bytes(letters), coordinate_values, duplicate_edges


def section_row(stores: Sequence[bytearray], state: int) -> tuple[bytes, ...]:
    return tuple(bytes(store[state * width:(state + 1) * width])
                 for store, width in zip(stores, COORDINATE_WIDTHS))


def value_from_blob(raw: bytes, index: int) -> Any:
    degree = 36 if index < 5 else 144
    return split_blob(raw, degree)


def multiply_blob(left: bytes, right: bytes, index: int, e3: Any, e4: Any) -> bytes:
    group = e3 if index < 5 else e4
    return blob_raw(group.mul(value_from_blob(left, index), value_from_blob(right, index)))


def inverse_blob(raw: bytes, index: int, e3: Any, e4: Any) -> bytes:
    group = e3 if index < 5 else e4
    return blob_raw(group.inverse(value_from_blob(raw, index)))


def blob_raw(value: Any) -> bytes:
    return bytes(value[0]) + bytes(value[1])


def family_inverse_key(key: Sequence[bytes], indices: Sequence[int],
                       e3: Any, e4: Any) -> tuple[bytes, ...]:
    return tuple(inverse_blob(raw, i, e3, e4) for raw, i in zip(key, indices))


def scan_memberships(stores: Sequence[bytearray], A_maps: dict[str, dict[tuple[bytes, ...], int]],
                     budget: Budget) -> tuple[dict[str, bytearray], dict[str, int]]:
    size = (EXPECTED_Q0 + 7) // 8
    bits = {name: bytearray(size) for name, _ in FAMILIES}
    counts = {name: 0 for name, _ in FAMILIES}
    for state in range(EXPECTED_Q0):
        if (state & 4095) == 0:
            budget.check("A_L_membership_scan")
        row = section_row(stores, state)
        for name, indices in FAMILIES:
            if family_key(row, indices) in A_maps[name]:
                bit_set(bits[name], state); counts[name] += 1
    for name in counts:
        require(counts[name] > 0 and EXPECTED_Q0 % counts[name] == 0,
                f"{name} L Lagrange")
    return bits, counts


def closure_q0(old: Any, generators: Sequence[int], qstates: Sequence[bytes],
               qids: dict[bytes, int], budget: Budget) -> set[int]:
    rows = list(dict.fromkeys(int(x) for x in generators))
    tables = [make_translation(qstates[x]) for x in rows]
    seen = {0}; queue = [0]
    for cursor, sid in enumerate(queue):
        if (cursor & 4095) == 0:
            budget.check("L_subgroup_closure")
        state = qstates[sid]
        for table in tables:
            target = qids[state.translate(table)]
            if target not in seen:
                seen.add(target); queue.append(target)
    return seen


def qmul(old: Any, left: bytes, right: bytes) -> bytes:
    return bytes(old.perm_mul(tuple(left), tuple(right)))


def qinv(old: Any, value: bytes) -> bytes:
    return bytes(old.perm_inv(tuple(value)))


def prove_L(old: Any, name: str, membership: bytes | bytearray, count: int,
            qstates: Sequence[bytes], qids: dict[bytes, int],
            q0_marked: Sequence[tuple[int, ...]], budget: Budget) -> tuple[list[int], dict[str, Any]]:
    require(bit_get(membership, 0), f"{name} L identity")
    selected: list[int] = []; subgroup = {0}
    for sid in range(EXPECTED_Q0):
        if bit_get(membership, sid) and sid not in subgroup:
            selected.append(sid)
            subgroup = closure_q0(old, selected, qstates, qids, budget)
            require(all(bit_get(membership, x) for x in subgroup), f"{name} closure subset")
            if len(subgroup) == count:
                break
    require(len(subgroup) == count and all((sid in subgroup) == bit_get(membership, sid)
                                           for sid in range(EXPECTED_Q0)),
            f"{name} generated subgroup equals bitset")
    inverse_ok = all(qids[qinv(old, qstates[x])] in subgroup for x in selected)
    require(inverse_ok, f"{name} inverses")
    normal_rows = []
    marked_bytes = [bytes(x) for x in q0_marked]
    require(all(x in qids for x in marked_bytes), "Q0 marked states in roster")
    letter_ids = [qids[x] for x in marked_bytes]
    normal_ok = True
    for generator in selected:
        for outer_id in letter_ids:
            outer = qstates[outer_id]
            conjugate = qmul(old, qmul(old, qinv(old, outer), qstates[generator]), outer)
            cid = qids[conjugate]
            normal_rows.append([generator + 1, outer_id, cid + 1])
            normal_ok &= cid in subgroup
    require(normal_ok, f"{name} normality")
    return selected, {
        "identity": True, "closure_by_exact_generated_subgroup": True,
        "inverse_generators_in_subgroup": True, "normal_under_q0_x_y": True,
        "generated_order": len(subgroup), "greedy_generator_state_ids": [x + 1 for x in selected],
        "normality_witness_rows": normal_rows,
        "proof_method": "greedy_generator_closure_equals_exact_membership_bitset",
    }


def eval_word_coordinates(old: Any, e3: Any, e4: Any, contexts: Sequence[Any],
                          delete: Any, word: Sequence[int]) -> tuple[Any, ...]:
    return tuple([delete(e4.eval(word, contexts[i - 1])) for i in (21, 22, 23, 24, 25)] +
                 [e4.eval(word, contexts[i - 1]) for i in (1, 27, 21, 26, 28)])


def gamma_kernel_generators(group: Any, projected: Sequence[tuple[Any, ...]],
                            indices: Sequence[int], e3: Any, e4: Any,
                            old: Any) -> tuple[list[int], set[int]]:
    identity_key = tuple_key(old, family_identity(indices, e3, e4))
    kernel = {sid for sid, row in enumerate(projected)
              if tuple_key(old, tuple(row[i] for i in indices)) == identity_key}
    selected: list[int] = []; subgroup = {0}
    for sid in sorted(kernel):
        if sid not in subgroup:
            selected.append(sid); subgroup = group.closure_ids(selected)
            require(subgroup <= kernel, "Gamma kernel closure")
    require(subgroup == kernel, "Gamma kernel generation")
    return selected, kernel


def family_public_A(old: Any, name: str, indices: Sequence[int],
                    projected: Sequence[tuple[Any, ...]], e3: Any, e4: Any,
                    qmarks: Sequence[Sequence[Any]]) -> tuple[dict[tuple[bytes, ...], int], dict[str, Any]]:
    first: dict[tuple[bytes, ...], int] = {}
    literal: dict[tuple[bytes, ...], tuple[Any, ...]] = {}
    for sid, row in enumerate(projected):
        value = tuple(row[i] for i in indices); key = tuple_key(old, value)
        first.setdefault(key, sid); literal.setdefault(key, value)
    ordered = sorted(first)
    closure = validate_A(old, name, indices, [literal[x] for x in ordered],
                         qmarks, e3, e4)
    table = [{"coordinate_blobs_hex": [x.hex() for x in key],
              "gamma_state_id": first[key] + 1} for key in ordered]
    return first, {"order": len(first), "literal_elements": table,
                   "literal_table_sha256": sha_obj(table), "group_checks": closure}


def build_result(q3_path: Path, joint_path: Path, seconds: float) -> dict[str, Any]:
    budget = Budget(seconds)
    authenticate_pins(q3_path, joint_path)
    q3 = json.loads(q3_path.read_text(encoding="utf-8"))
    joint_receipt = json.loads(joint_path.read_text(encoding="utf-8"))
    require(joint_receipt["terminal_token"] == "B345_JOINT_KERNEL_QSTAR_CLOSED" and
            joint_receipt["gamma"]["order"] == EXPECTED_GAMMA,
            "task157ee COMPLETE Gamma receipt")
    old = load_module(ROOT / PINS["e4_arithmetic"][0], "d176_frozen_e4")
    jointmod = load_module(ROOT / PINS["task157ee_producer"][0], "d176_frozen_157ee")
    e3, e4, _ = old.reconstruct_quotients(q3)
    contexts, aliases, context_public = old.cheap_context_registry(e4)
    require(len(contexts) == 31 and len(context_public["named_uses"]) == 46,
            "31-row registry")
    words = [list(row["word"]) for row in q3["correction_fibre"]["records"] if row["word"]]
    require(len(words) == 26 and sha_obj(words) == joint_receipt["record_manifest"]["words_sha256"],
            "26 correction words")
    gamma = jointmod.JointGroup(old, e3, e4, contexts, words)
    require(len(gamma.states) == EXPECTED_GAMMA and
            gamma.public()["state_rows_sha256"] == joint_receipt["gamma"]["state_rows_sha256"],
            "Gamma reconstruction")
    fine, fine_public = build_fine_deletion(e3, e4, budget)
    q0_marked = [old.perm_from_row(row, 36)
                 for row in q3["coarse_models"]["Q0"]["marked_permutations"]]
    q0_relators = jointmod.complete_relators(old)
    require(len(q0_relators) == 19 and
            all(old.eval_perm_word(word, q0_marked) == tuple(range(36))
                for word in q0_relators) and
            sha_obj(q0_relators) == joint_receipt["q0_presentation"]["complete_relators_sha256"],
            "complete Q0 presentation replay")
    delete, deletion_public = make_deleter(old, e3, e4, fine, q0_marked)
    deletion_public["fine"] = fine_public
    projected = [projection(state, delete) for state in gamma.states]
    require(all([len(blob(old, x)) for x in row] == COORDINATE_WIDTHS for row in projected),
            "ten projected widths")
    require(all(projected[sid][0] == gamma.states[sid][0] for sid in range(EXPECTED_GAMMA)),
            "C21 deletion equals registered E3 source")
    coordinate_marks = []
    for item in COORDINATES:
        pair = contexts[item["context_id"] - 1]
        values = [e4.eval([letter], pair) for letter in (1, 2)]
        if item["type"] == "E3":
            values = [delete(x) for x in values]
        coordinate_marks.append(values)
    require(coordinate_marks[0] == [e3.generators[0], e3.generators[2]],
            "source E3 x/y replay")

    A_maps: dict[str, dict[tuple[bytes, ...], int]] = {}
    A_public: dict[str, Any] = {}
    for name, indices in FAMILIES:
        A_maps[name], A_public[name] = family_public_A(
            old, name, indices, projected, e3, e4, coordinate_marks)
    qstates, qids, parents, letters, stores, duplicate_edges = enumerate_q0_sections(
        old, q0_marked, coordinate_marks, e3, e4, budget)
    del duplicate_edges
    memberships, L_counts = scan_memberships(stores, A_maps, budget)

    family_rows: dict[str, Any] = {}
    L_generators: dict[str, list[int]] = {}
    for name, indices in FAMILIES:
        selected, proof = prove_L(old, name, memberships[name], L_counts[name],
                                  qstates, qids, q0_marked, budget)
        L_generators[name] = selected
        index = EXPECTED_Q0 // L_counts[name]
        d_order = A_public[name]["order"] * index
        require(d_order % A_public[name]["order"] == 0, f"{name} order formula")
        family_rows[name] = {
            "label": name, "coordinate_indices": list(indices),
            "A_order": A_public[name]["order"], "L_order": L_counts[name],
            "Q0_index_L": index, "D_order": d_order,
            "formula": "|D_S|=|A_S|*[Q0:L_S]",
            "membership_bitset": pack(bytes(memberships[name]), 1, len(memberships[name]),
                                      f"little-bit order Q0 state IDs for L_{name}"),
            "L_group_checks": proof,
        }
    dall = family_rows["ALL"]["D_order"]
    kernel_orders = {}
    for i in range(10):
        di = family_rows[f"S{i}"]["D_order"]
        require(dall % di == 0, f"projection kernel divisibility S{i}")
        kernel_orders[f"S{i}"] = dall // di

    gamma_parent = bytearray(); gamma_record = bytearray()
    for parent, generator in zip(gamma.parent, gamma.parent_generator):
        gamma_parent.extend(struct.pack("<H", 0 if parent is None else parent + 1))
        gamma_record.append(0 if generator is None else generator + 1)
    projected_raw = b"".join(blob(old, x) for row in projected for x in row)
    q_parent_raw = b"".join(struct.pack("<I", x + 1 if i else 0)
                            for i, x in enumerate(parents))

    emitted: dict[str, Any] = {}
    for name, indices in FAMILIES:
        gamma_selected, gamma_kernel = gamma_kernel_generators(
            gamma, projected, indices, e3, e4, old)
        gamma_words = []
        for sid in gamma_selected:
            word = gamma.section_word(sid)
            replay = eval_word_coordinates(old, e3, e4, contexts, delete, word)
            require(tuple_key(old, tuple(replay[i] for i in indices)) ==
                    tuple_key(old, family_identity(indices, e3, e4)),
                    f"{name} Gamma kernel word")
            gamma_words.append({"gamma_state_id": sid + 1, "source_word": word,
                                "ten_coordinate_blobs_hex": [blob(old, x).hex() for x in replay]})
        adjusted_words = []
        for qid in L_generators[name]:
            row = section_row(stores, qid); section_key = family_key(row, indices)
            need = family_inverse_key(section_key, indices, e3, e4)
            require(need in A_maps[name], f"{name} Gamma adjustment exists")
            gid = A_maps[name][need]
            word = old.reduce_word(gamma.section_word(gid) +
                                   q0_section_word(qid, parents, letters))
            replay = eval_word_coordinates(old, e3, e4, contexts, delete, word)
            require(tuple_key(old, tuple(replay[i] for i in indices)) ==
                    tuple_key(old, family_identity(indices, e3, e4)),
                    f"{name} adjusted L word")
            adjusted_words.append({"q0_state_id": qid + 1,
                                   "gamma_adjustment_state_id": gid + 1,
                                   "source_word": word,
                                   "ten_coordinate_blobs_hex": [blob(old, x).hex() for x in replay]})
        emitted[name] = {
            "Gamma_S0_order": len(gamma_kernel),
            "Gamma_S0_generators": gamma_words,
            "adjusted_L_generators": adjusted_words,
            "H_S_generating_words": "union of the two literal lists above",
            "all_words_directly_replayed_in_all_ten_coordinates": True,
        }

    # A second deterministic section obtained by one fixed, literal,
    # nonidentity Gamma twist.  This avoids any assumption that a non-tree
    # edge has nontrivial image in the selected ten-coordinate quotient.
    samples = []
    full_identity_key = tuple(blob(old, e3.identity if i < 5 else e4.identity)
                              for i in range(10))
    twist_id = next((sid for sid, row in enumerate(projected)
                     if tuple_key(old, row) != full_identity_key), None)
    require(twist_id is not None, "nontrivial registered Gamma twist")
    twist_row = tuple(blob(old, x) for x in projected[twist_id])
    for target in range(16):
        canonical_row = section_row(stores, target)
        alt = [multiply_blob(twist_row[i], canonical_row[i], i, e3, e4)
               for i in range(10)]
        delta = tuple(multiply_blob(alt[i], inverse_blob(canonical_row[i], i, e3, e4),
                                    i, e3, e4) for i in range(10))
        require(delta == twist_row and delta in A_maps["ALL"], "literal Gamma twist")
        comparisons = {}
        for name, indices in FAMILIES:
            comparisons[name] = ((family_key(alt, indices) in A_maps[name]) ==
                                 (family_key(canonical_row, indices) in A_maps[name]))
            require(comparisons[name], f"{name} section independence")
        samples.append({"target_q0_state_id": target + 1,
                        "twist_gamma_state_id": twist_id + 1,
                        "family_membership_equal": comparisons,
                        "alternate_ten_coordinate_blobs_hex": [x.hex() for x in alt]})

    # Literal equality pattern for singleton images.  Membership of a source
    # generator in a target image is reduced to its coarse section plus A.
    image_generators = []
    for i in range(10):
        image_generators.append([projected[gamma.ids[gamma.key(g)]][i]
                                 for g in gamma.generators] + list(coordinate_marks[i]))
    equality = []
    for target in range(10):
        ambient = "E3" if target < 5 else "E4"
        degree = 36 if target < 5 else 144
        coarse_to_q: dict[bytes, int | list[int]] = {}
        for qid in range(EXPECTED_Q0):
            if (qid & 4095) == 0:
                budget.check("typed_singleton_equality")
            raw = bytes(stores[target][qid * COORDINATE_WIDTHS[target]:
                                       (qid + 1) * COORDINATE_WIDTHS[target]])
            coarse = raw[:degree]; prior = coarse_to_q.get(coarse)
            if prior is None:
                coarse_to_q[coarse] = qid
            elif isinstance(prior, int):
                coarse_to_q[coarse] = [prior, qid]
            else:
                prior.append(qid)
        for source in range(10):
            if (source < 5) != (target < 5):
                equality.append({"left": f"S{source}", "right": f"S{target}",
                                 "relation": "NOT_COMPARABLE_DIFFERENT_TYPED_AMBIENT"})
                continue
            contained = True
            for value in image_generators[source]:
                raw = blob(old, value); candidate = coarse_to_q.get(raw[:degree])
                if candidate is None:
                    contained = False; break
                candidates = [candidate] if isinstance(candidate, int) else candidate
                found = False
                for qid in candidates:
                    section = bytes(stores[target][qid * COORDINATE_WIDTHS[target]:
                                                  (qid + 1) * COORDINATE_WIDTHS[target]])
                    residual = multiply_blob(raw, inverse_blob(section, target, e3, e4),
                                             target, e3, e4)
                    if (residual,) in A_maps[f"S{target}"]:
                        found = True; break
                if not found:
                    contained = False; break
            equality.append({"left": f"S{source}", "right": f"S{target}",
                             "relation": "SUBGROUP" if contained else "NOT_SUBGROUP",
                             "generator_membership_test_count": len(image_generators[source])})
        del coarse_to_q
    equality_matrix = []
    lookup = {(row["left"], row["right"]): row["relation"] for row in equality}
    for i in range(10):
        row = []
        for j in range(10):
            if (i < 5) != (j < 5):
                row.append("TYPED_NOT_COMPARABLE")
            else:
                row.append("EQUAL" if lookup[(f"S{i}", f"S{j}")] == "SUBGROUP" and
                           lookup[(f"S{j}", f"S{i}")] == "SUBGROUP" else "UNEQUAL")
        equality_matrix.append(row)

    result = {
        "theorem": "v125 finite extension-section reduction",
        "extension": {"Gamma_order": EXPECTED_GAMMA, "Q0_order": EXPECTED_Q0,
                      "exact_sequence": "1->Gamma->G->Q0->1"},
        "deletion": deletion_public,
        "registry": {"context_count": len(contexts), "public_sha256": sha_obj(context_public),
                     "selected_context_ids": [21, 22, 23, 24, 25, 1, 27, 21, 26, 28],
                     "C21_typed_reuse_not_deduplicated": True},
        "Gamma": {
            "order": EXPECTED_GAMMA,
            "record_words": words,
            "section_parent_states_u16le": pack(bytes(gamma_parent), 2, EXPECTED_GAMMA,
                                                 "0 root; otherwise one-based parent state"),
            "section_parent_record_u8": pack(bytes(gamma_record), 1, EXPECTED_GAMMA,
                                              "0 root; otherwise one-based correction record"),
            "ten_coordinate_states": pack(projected_raw, sum(COORDINATE_WIDTHS), EXPECTED_GAMMA,
                                           "state-major ten typed coordinate blobs"),
        },
        "A_families": A_public,
        "Q0_section": {
            "order": EXPECTED_Q0, "discovery": "positive x,y first-seen BFS",
            "complete_presentation_relators": q0_relators,
            "complete_presentation_relators_sha256": sha_obj(q0_relators),
            "presentation_completeness":
                "pinned v121 plus frozen task157ee factor presentations and split words",
            "canonical_roster": pack(b"".join(qstates), 36, EXPECTED_Q0,
                                     "zero-based Q0 permutations in discovery order"),
            "parent_states_u32le": pack(q_parent_raw, 4, EXPECTED_Q0,
                                        "0 root; otherwise one-based parent state"),
            "parent_letters_u8": pack(letters, 1, EXPECTED_Q0, "0 root, 1=x, 2=y"),
            "roster_sha256": sha_bytes(b"".join(qstates)),
            "ten_coordinate_marked_generator_blobs_hex": [
                [blob(old, value).hex() for value in row] for row in coordinate_marks],
            "section_value_decoder":
                "replay parent_letters from root with the literal typed marked-generator blobs",
            "all_section_values_losslessly_reconstructible": True,
            "lossless_image_section_primitive":
                "for every Q0 state q, parent/letter decodes s(q) and its ten literal values; pair with any A-table Gamma index",
        },
        "families": family_rows,
        "projection_kernel_orders": kernel_orders,
        "word_generators": emitted,
        "section_independence": {"method": "fixed nonidentity left Gamma twist",
                                 "sample_count": len(samples), "samples": samples},
        "typed_singleton_images": {
            "orders": [{"label": f"S{i}", "type": COORDINATES[i]["type"],
                        "D_order": family_rows[f"S{i}"]["D_order"],
                        "kernel_from_ALL_order": kernel_orders[f"S{i}"]}
                       for i in range(10)],
            "directed_generator_containment": equality,
            "equality_matrix": equality_matrix,
            "coordinate_0_7_equal": False,
            "coordinate_0_7_reason": "different typed ambient E3 versus E4",
        },
        "proof_pins": {"v108": "pinned_not_reproved", "v121": "pinned_not_reproved",
                       "v122": "pinned_not_reproved", "v125": "implemented"},
        "performance": {"elapsed_seconds": budget.elapsed(),
                        "direct_Delta_states_enumerated": 0,
                        "Q0_states_enumerated_once": EXPECTED_Q0,
                        "Pi4_deletion_states": 59049},
    }
    return result


def base_receipt() -> dict[str, Any]:
    return {
        "schema": SCHEMA, "pins": public_pins(), "coordinates": COORDINATES,
        "boundaries": {"all_seven_solution": False, "correction_word": False,
                       "cofinal_lift": False, "fake": False, "Ihara_witness": False,
                       "support_correlation_6441": False, "direct_Delta_enumeration": False},
        "claim": "exact Delta_all/ten projection orders and word-bearing projection-kernel data only",
        "GHA_dispatched": False,
    }


def write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical(seal(receipt)) + b"\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(raw); temporary.replace(path)


def run(args: argparse.Namespace) -> int:
    if args.selftest:
        fixture_path = Path(args.fixture)
        require(file_identity(fixture_path) == (FIXTURE_BYTES, FIXTURE_SHA256),
                "immutable fixture identity")
        receipt = json.loads(fixture_path.read_text(encoding="utf-8"))
        validate_envelope(receipt)
        require(receipt["terminal"] == UNKNOWN_RESOURCE and
                receipt["reason"] == "LOCAL_EXECUTION_GUARD", "immutable fixture semantics")
        print("R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_PRODUCER_SELFTEST_PASS", flush=True)
        return 0
    require(args.run_census and args.output, "production arguments")
    receipt = base_receipt()
    try:
        result = build_result(Path(args.q3), Path(args.joint), args.soft_seconds)
        receipt.update({"status": "COMPLETE", "terminal": PASS,
                        "reason": None, "result": result})
    except ResourceStop as exc:
        receipt.update({"status": "UNKNOWN_RESOURCE", "terminal": UNKNOWN_RESOURCE,
                        "reason": str(exc), "result": None})
    except (InputStop, FileNotFoundError, json.JSONDecodeError) as exc:
        receipt.update({"status": "UNKNOWN_INPUT", "terminal": UNKNOWN_INPUT,
                        "reason": f"AUTHENTICATED_INPUT:{exc}", "result": None})
    write_receipt(Path(args.output), receipt)
    validate_envelope(json.loads(Path(args.output).read_text(encoding="utf-8")))
    print(f"R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_PRODUCER_TERMINAL {receipt['terminal']}",
          flush=True)
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    mode = result.add_mutually_exclusive_group(required=True)
    mode.add_argument("--selftest", action="store_true")
    mode.add_argument("--run-census", action="store_true")
    result.add_argument("--fixture", default=str(FIXTURE))
    result.add_argument("--q3", default=str(DEFAULT_Q3))
    result.add_argument("--joint", default=str(DEFAULT_JOINT))
    result.add_argument("--output")
    result.add_argument("--soft-seconds", type=float, default=9_000.0)
    return result


if __name__ == "__main__":
    try:
        raise SystemExit(run(parser().parse_args()))
    except (Reject, ValueError, KeyError, TypeError) as exc:
        print(f"R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_PRODUCER_STOP {exc}",
              file=sys.stderr, flush=True)
        raise SystemExit(1)
