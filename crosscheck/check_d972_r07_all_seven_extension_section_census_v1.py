#!/usr/bin/env python3
"""Helper-nonshared checker for the R07 extension-section census.

No task176 producer code or helper is imported.  Frozen primary arithmetic is
loaded only after exact authentication; Gamma, deletion, Q0 discovery,
sections, A/L families, generators, and ten-coordinate replay are rebuilt
below.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import importlib.util
import json
import struct
import sys
import zlib
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-all-seven-extension-section-census/v1"
PASS = "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"
UNKNOWN_RESOURCE = "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_RESOURCE"
UNKNOWN_INPUT = "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_INPUT"
AUTHENTICATED_INPUT_PREFIX = "AUTHENTICATED_INPUT:"
CENSUS_REJECT_PREFIX = "CENSUS_REJECT:"
UNKNOWN_INPUT_PREFIXES = (AUTHENTICATED_INPUT_PREFIX, CENSUS_REJECT_PREFIX)
EXPECTED_Q0 = 1_469_664
EXPECTED_GAMMA = 243
EXPECTED_GAMMA_COARSE_ORDERS = (1, 1, 1, 1, 1, 81, 81, 81, 9, 9)
WIDTHS = [40] * 5 + [154] * 5
FAMILIES = [("ALL", tuple(range(10)))] + [(f"S{i}", (i,)) for i in range(10)]
PRODUCER_SHA256 = "5cf5617bebc932833dd34105bd85b2536e8c332137dce0f6ea176ebd82e09bd3"
PRODUCER_PATH = "search/d972_r07_all_seven_extension_section_census_v1.py"
FIXTURE = ROOT / "search/certs/d972_r07_all_seven_extension_section_census_preflight_v1_20260827.json"
FIXTURE_BYTES = 4350
FIXTURE_SHA256 = "b24827b10f8ceb0505802bf7065e2442d176b7b65ecb2066452941c2e7e0a471"
Q3_PATH = ROOT / "ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json"
JOINT_PATH = ROOT / "ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json"

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
V135_PIN = ("sol/proof_r07_q4_q0_noncontiguous_deletion_layout_v135.md", 4539,
            "75c511a765ad88ec1aa72c63a0d1965ac85724695d743cbf00350572a884cf67")


class Reject(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def canonical_packed_permutation(value: Any, degree: int, label: str) -> bytes:
    require(type(value) is bytes, f"{label} packed-bytes type")
    require(len(value) == degree and set(value) == set(range(degree)),
            f"{label} packed permutation")
    return value


def canonical_packed_extension_element(value: Any, degree: int, pc_width: int,
                                       label: str) -> tuple[bytes, bytes]:
    require(type(value) is tuple and len(value) == 2, f"{label} EKey tuple")
    permutation = canonical_packed_permutation(value[0], degree,
                                               f"{label} permutation")
    pc_value = value[1]
    require(type(pc_value) is bytes and len(pc_value) == pc_width,
            f"{label} packed PC component")
    return permutation, pc_value


def packed_permutation_selftest() -> int:
    identity = bytes(range(4))
    require(canonical_packed_permutation(identity, 4, "selftest identity") == identity,
            "packed permutation positive selftest")
    try:
        canonical_packed_permutation(tuple(range(4)), 4, "selftest tuple identity")
    except Reject:
        return 2
    raise Reject("tuple permutation representation accepted")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(canonical(value))


def public_pins() -> dict[str, dict[str, Any]]:
    return {name: {"path": row[0], "bytes": row[1], "sha256": row[2]}
            for name, row in PINS.items()}


def public_v135_pin() -> dict[str, Any]:
    relative, size, digest = V135_PIN
    return {"path": relative, "bytes": size, "sha256": digest}


def authenticate() -> None:
    for name, (relative, size, digest) in PINS.items():
        raw = (ROOT / relative).read_bytes()
        require((len(raw), sha_bytes(raw)) == (size, digest), f"pin {name}")
    relative, size, digest = V135_PIN
    raw = (ROOT / relative).read_bytes()
    require((len(raw), sha_bytes(raw)) == (size, digest), "pin v135")
    raw = (ROOT / PRODUCER_PATH).read_bytes()
    require(sha_bytes(raw) == PRODUCER_SHA256, "producer source pin")
    fixture_raw = FIXTURE.read_bytes()
    require((len(fixture_raw), sha_bytes(fixture_raw)) ==
            (FIXTURE_BYTES, FIXTURE_SHA256), "immutable fixture pin")


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "module spec")
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def unpack(obj: dict[str, Any], width: int | None = None,
           count: int | None = None) -> bytes:
    require(obj["codec"] == "zlib+base64", "codec")
    comp = base64.b64decode(obj["data"], validate=True)
    require(len(comp) == obj["compressed_bytes"] and
            sha_bytes(comp) == obj["compressed_sha256"], "compressed digest")
    raw = zlib.decompress(comp)
    require(len(raw) == obj["raw_bytes"] ==
            obj["record_width_bytes"] * obj["record_count"] and
            sha_bytes(raw) == obj["raw_sha256"], "raw digest")
    if width is not None:
        require(obj["record_width_bytes"] == width, "record width")
    if count is not None:
        require(obj["record_count"] == count, "record count")
    return raw


def reseal(receipt: dict[str, Any]) -> dict[str, Any]:
    receipt.pop("self_digest_sha256", None)
    receipt["self_digest_sha256"] = sha_obj(receipt)
    return receipt


def validate_envelope(receipt: dict[str, Any]) -> None:
    require(receipt.get("schema") == SCHEMA, "schema")
    body = dict(receipt); claimed = body.pop("self_digest_sha256", None)
    require(claimed == sha_obj(body), "self digest")
    require(receipt.get("pins") == public_pins(), "pins")
    require(receipt.get("coordinates") == COORDINATES, "coordinates")
    require(receipt["coordinates"][0]["context_id"] ==
            receipt["coordinates"][7]["context_id"] == 21 and
            receipt["coordinates"][0]["type"] != receipt["coordinates"][7]["type"],
            "typed 0/7 C21")
    require(receipt.get("boundaries") == {
        "all_seven_solution": False, "correction_word": False,
        "cofinal_lift": False, "fake": False, "Ihara_witness": False,
        "support_correlation_6441": False, "direct_Delta_enumeration": False,
    }, "boundaries")
    terminal = receipt.get("terminal")
    require(terminal in {PASS, UNKNOWN_RESOURCE, UNKNOWN_INPUT}, "terminal")
    if terminal == PASS:
        require(receipt.get("status") == "COMPLETE" and
                isinstance(receipt.get("result"), dict) and receipt.get("reason") is None,
                "complete envelope")
    elif terminal == UNKNOWN_RESOURCE:
        require(receipt.get("status") == "UNKNOWN_RESOURCE" and
                receipt.get("result") is None and isinstance(receipt.get("reason"), str),
                "resource envelope")
    else:
        reason = receipt.get("reason")
        require(receipt.get("status") == "UNKNOWN_INPUT" and
                receipt.get("result") is None and isinstance(reason, str) and
                any(reason.startswith(prefix) and len(reason) > len(prefix)
                    for prefix in UNKNOWN_INPUT_PREFIXES),
                "input envelope")


def independent_joint_blob(value: Any, label: str) -> bytes:
    if type(value) is not tuple or len(value) != 2:
        raise TypeError(f"{label} outer representation")
    permutation = value[0]
    pc_component = value[1]
    if type(permutation) is bytes:
        packed = permutation
    elif type(permutation) is tuple:
        if not all(type(entry) is int for entry in permutation):
            raise TypeError(f"{label} permutation entry representation")
        packed = bytes(permutation)
    else:
        raise TypeError(f"{label} permutation representation")
    if type(pc_component) is not bytes:
        raise TypeError(f"{label} PC representation")
    dimensions = (len(packed), len(pc_component))
    if dimensions not in {(36, 4), (144, 10)}:
        raise ValueError(f"{label} extension dimensions")
    if set(packed) != set(range(len(packed))):
        raise ValueError(f"{label} non-permutation")
    return packed + pc_component


def blob(old: Any, value: Any) -> bytes:
    del old
    return independent_joint_blob(value, "checker joint element")


def joint_blob_representation_selftest() -> int:
    class FailingLegacySerializer:
        @staticmethod
        def _element_blob(value: Any) -> bytes:
            del value
            raise AssertionError("checker consulted frozen serializer")

    pc = bytes(4)
    target = bytes(range(36)) + pc
    require(blob(FailingLegacySerializer(), (tuple(range(36)), pc)) == target,
            "checker tuple plus bytes boundary")
    require(blob(FailingLegacySerializer(), (bytes(range(36)), pc)) == target,
            "checker packed plus bytes boundary")
    checks = 2
    malformed = (
        [tuple(range(36)), pc],
        (list(range(36)), pc),
        (tuple(range(36)), tuple(pc)),
        (tuple(range(35)), pc),
        (tuple(range(36)), bytes(3)),
        (tuple([0, 0] + list(range(2, 36))), pc),
    )
    for candidate in malformed:
        try:
            independent_joint_blob(candidate, "checker selftest mutation")
        except (TypeError, ValueError):
            checks += 1
        else:
            raise Reject("checker accepted malformed joint serialization")
    return checks


def value(raw: bytes, index: int) -> Any:
    degree = 36 if index < 5 else 144
    return tuple(raw[:degree]), bytes(raw[degree:])


def bit_get(bits: bytes, index: int) -> bool:
    return bool(bits[index >> 3] & (1 << (index & 7)))


def make_translation(permutation: Sequence[int]) -> bytes:
    table = bytearray(range(256))
    for i, x in enumerate(permutation):
        table[i] = int(x)
    return bytes(table)


def coarse_delete(permutation: Any) -> bytes:
    source = canonical_packed_permutation(permutation, 144,
                                          "coarse deletion source")
    p_coordinates = source[27:36]
    g_coordinates = source[117:144]
    require(set(p_coordinates) == set(range(27, 36)),
            "coarse fourth P block")
    require(set(g_coordinates) == set(range(117, 144)),
            "coarse fourth G9 block")
    image = bytes([value - 27 for value in p_coordinates] +
                  [value - 108 for value in g_coordinates])
    return canonical_packed_permutation(image, 36,
                                        "coarse deletion image")


def independent_coarse_diagnostic(actual: Sequence[bytes],
                                  expected: Sequence[bytes]) -> dict[str, Any]:
    require(type(actual) is list and type(expected) is list and
            len(actual) == len(expected) == 6, "coarse diagnostic arity")
    target_names = ["X", "Z=(YX)^-1", "1", "Y", "1", "1"]
    braid_names = ["A12", "A13", "A14", "A23", "A24", "A34"]
    rows: list[dict[str, Any]] = []
    for position in range(6):
        observed = canonical_packed_permutation(actual[position], 36,
                                                "observed coarse row")
        target = canonical_packed_permutation(expected[position], 36,
                                              "target coarse row")
        differences = [i for i in range(36) if observed[i] != target[i]]
        equal = not differences
        rows.append({
            "marked_index_1_based": position + 1,
            "pb4_generator": braid_names[position],
            "target_label": target_names[position],
            "actual_hex": observed.hex(),
            "expected_hex": target.hex(),
            "actual_sha256": sha_bytes(observed),
            "expected_sha256": sha_bytes(target),
            "first_difference_index_0_based": None if equal else differences[0],
            "literal_equal": equal,
            "conjugation_required": False if equal else None,
        })
    return {
        "schema": "Q4-fourth-factor-to-Q0-marked-diagnostic/v1",
        "source_degree": 144,
        "target_degree": 36,
        "source_layout": "P^4_then_G9^4",
        "source_half_open_slices_0_based": [[27, 36], [117, 144]],
        "target_layout": "P_then_G9",
        "target_half_open_slices_0_based": [[0, 9], [9, 36]],
        "rebasing_subtractions": [27, 108],
        "strand_deleted_1_based": 4,
        "orientation": "literal_frozen_rows_no_strand_permutation",
        "rows": rows,
        "all_literal_equal": all(row["literal_equal"] for row in rows),
        "conjugation_used": False,
    }


def validate_coarse_diagnostic(claimed: Any, actual: list[bytes],
                               expected: list[bytes]) -> None:
    require(type(claimed) is dict, "coarse diagnostic object")
    reconstructed = independent_coarse_diagnostic(actual, expected)
    scalar_keys = (
        "schema", "source_degree", "target_degree", "source_layout",
        "source_half_open_slices_0_based", "target_layout",
        "target_half_open_slices_0_based", "rebasing_subtractions",
        "strand_deleted_1_based", "orientation", "all_literal_equal",
        "conjugation_used",
    )
    require(set(claimed) == set(scalar_keys) | {"rows"},
            "coarse diagnostic keys")
    for key in scalar_keys:
        require(claimed.get(key) == reconstructed[key],
                f"coarse diagnostic scalar {key}")
    require(type(claimed.get("rows")) is list and len(claimed["rows"]) == 6,
            "coarse diagnostic rows")
    row_keys = {
        "marked_index_1_based", "pb4_generator", "target_label", "actual_hex",
        "expected_hex", "actual_sha256", "expected_sha256",
        "first_difference_index_0_based", "literal_equal",
        "conjugation_required",
    }
    for index, (candidate, reference) in enumerate(zip(claimed["rows"],
                                                       reconstructed["rows"])):
        require(type(candidate) is dict and set(candidate) == row_keys,
                f"coarse diagnostic row keys {index + 1}")
        for key in row_keys:
            require(candidate.get(key) == reference[key],
                    f"coarse diagnostic row {index + 1} field {key}")


def independent_bucket_statistics(target: int, degree: int,
                                  table: dict[bytes, int | list[int]]) -> dict[str, Any]:
    require(target in range(10) and degree == (36 if target < 5 else 144) and table,
            "bucket statistic input")
    multiplicities: dict[int, int] = {}
    total = 0
    smallest: int | None = None
    largest = 0
    binding = hashlib.sha256()
    for key in table:  # insertion order is the independently rebuilt first-seen order
        require(type(key) is bytes and len(key) == degree, "bucket key representation")
        addresses = table[key]
        count = 1 if type(addresses) is int else len(addresses)
        require(count >= 1, "bucket multiplicity")
        multiplicities[count] = multiplicities.get(count, 0) + 1
        total += count
        smallest = count if smallest is None or count < smallest else smallest
        largest = count if count > largest else largest
        binding.update(len(key).to_bytes(2, "little"))
        binding.update(key)
        binding.update(count.to_bytes(4, "little"))
    histogram = [{"bucket_size": count,
                  "coarse_key_count": multiplicities[count]}
                 for count in sorted(multiplicities)]
    require(total == EXPECTED_Q0 and
            sum(x["bucket_size"] * x["coarse_key_count"] for x in histogram) == total,
            "bucket partition cardinality")
    return {
        "label": f"S{target}",
        "type": COORDINATES[target]["type"],
        "coarse_key_width_bytes": degree,
        "q0_state_count": EXPECTED_Q0,
        "distinct_coarse_keys": len(table),
        "bucket_size_min": smallest,
        "bucket_size_max": largest,
        "multiplicity_histogram": histogram,
        "multiplicity_histogram_sha256": sha_obj(histogram),
        "first_seen_key_multiplicity_sha256": binding.hexdigest(),
        "digest_encoding": "repeat(u16le_key_width,key_bytes,u32le_bucket_size)",
        "key_order": "first_seen_Q0_state_id",
        "bucket_equivalence": "literal_coarse_key_equality_not_C_i_left_coset",
    }


def deleter_representation_selftest() -> int:
    coarse_identity = coarse_delete(bytes(range(144)))
    require(coarse_identity == bytes(range(36)), "coarse deletion bytes selftest")
    pc_identity = bytes([0, 0])
    element = (coarse_identity, pc_identity)
    require(canonical_packed_extension_element(element, 36, 2,
                                               "selftest E3 element") == element,
            "E3 element positive selftest")
    checks = 2
    try:
        coarse_delete(tuple(range(144)))
    except Reject:
        checks += 1
    else:
        raise Reject("tuple coarse permutation accepted")
    mutations = [
        (tuple(range(36)), pc_identity),
        (coarse_identity, tuple(pc_identity)),
        [coarse_identity, pc_identity],
    ]
    for mutation in mutations:
        try:
            canonical_packed_extension_element(mutation, 36, 2,
                                               "selftest mutated E3 element")
        except Reject:
            checks += 1
        else:
            raise Reject("mutated E3 representation accepted")
    return checks


def deletion_convention_selftest() -> int:
    identity144 = bytes(range(144)); identity36 = bytes(range(36))
    require(coarse_delete(identity144) == identity36,
            "independent split-factor identity")
    checks = 1
    for pair in ((26, 27), (116, 117)):
        mutation = bytearray(identity144)
        mutation[pair[0]], mutation[pair[1]] = mutation[pair[1]], mutation[pair[0]]
        try:
            coarse_delete(bytes(mutation))
        except Reject:
            checks += 1
        else:
            raise Reject("cross-factor deletion mutation accepted")
    actual = [identity36] * 6; expected = [identity36] * 6
    baseline = independent_coarse_diagnostic(actual, expected)
    validate_coarse_diagnostic(copy.deepcopy(baseline), actual, expected)
    checks += 1
    for field, value in (("actual_hex", "00" * 36),
                         ("first_difference_index_0_based", 0)):
        mutation = copy.deepcopy(baseline)
        mutation["rows"][0][field] = value
        try:
            validate_coarse_diagnostic(mutation, actual, expected)
        except Reject:
            checks += 1
        else:
            raise Reject(f"coarse diagnostic mutation accepted: {field}")
    p4_source = bytearray(identity144)
    p4_source[27], p4_source[28] = p4_source[28], p4_source[27]
    correct_p4 = coarse_delete(bytes(p4_source))
    contiguous = canonical_packed_permutation(
        bytes(value - 108 for value in p4_source[108:144]), 36,
        "independent contiguous selector")
    wrong_p = canonical_packed_permutation(
        bytes(value - 18 for value in p4_source[18:27]) +
        bytes(value - 108 for value in p4_source[117:144]), 36,
        "independent wrong P selector")
    g4_source = bytearray(identity144)
    g4_source[117], g4_source[118] = g4_source[118], g4_source[117]
    correct_g4 = coarse_delete(bytes(g4_source))
    wrong_g = canonical_packed_permutation(
        bytes(value - 27 for value in g4_source[27:36]) +
        bytes(value - 81 for value in g4_source[90:117]), 36,
        "independent wrong G9 selector")
    for observed, target in ((contiguous, correct_p4), (wrong_p, correct_p4),
                             (wrong_g, correct_g4)):
        selector = independent_coarse_diagnostic(
            [observed] + [identity36] * 5, [target] + [identity36] * 5)
        try:
            require(selector["all_literal_equal"], "mutated deletion selector")
        except Reject:
            checks += 1
        else:
            raise Reject("mutated deletion selector accepted")
    bad_offset = (bytes(value - 27 for value in g4_source[27:36]) +
                  bytes(value - 117 for value in g4_source[117:144]))
    try:
        canonical_packed_permutation(bad_offset, 36,
                                     "independent wrong G9 output offset")
    except Reject:
        checks += 1
    else:
        raise Reject("wrong G9 output offset accepted")
    return checks


def reconstruct_deletion(e3: Any, e4: Any) -> tuple[Any, dict[str, Any]]:
    pc3, pc4 = e3.pc, e4.pc
    e3_pc_width = len(e3.identity[1])
    e4_pc_width = len(e4.identity[1])
    targets = [e3.generators[0][1], e3.generators[1][1], pc3.one(),
               e3.generators[2][1], pc3.one(), pc3.one()]
    states = [pc4.one()]; images = [pc3.one()]; ids = {bytes(pc4.one()): 0}
    for sid, state in enumerate(states):
        for source, target in zip((x[1] for x in e4.generators), targets):
            nxt = pc4.mul(state, source); image = pc3.mul(images[sid], target)
            key = bytes(nxt)
            if key not in ids:
                ids[key] = len(states); states.append(nxt); images.append(image)
            else:
                require(images[ids[key]] == image, "fine deletion consistency")
    require(len(states) == 59049, "fine deletion exhaustive")
    table = {bytes(x): bytes(y) for x, y in zip(states, images)}

    def delete(element: Any) -> Any:
        source = canonical_packed_extension_element(element, 144, e4_pc_width,
                                                    "E4 deletion source")
        require(source[1] in table, "fine deletion lookup")
        result = (coarse_delete(source[0]), table[source[1]])
        return canonical_packed_extension_element(result, 36, e3_pc_width,
                                                  "E3 deletion image")

    targets_e = [canonical_packed_extension_element(target, 36, e3_pc_width,
                                                    "marked E3 deletion target")
                 for target in [e3.generators[0], e3.generators[1], e3.identity,
                                e3.generators[2], e3.identity, e3.identity]]
    require([delete(x) for x in e4.generators] == targets_e, "marked deletion")
    actual_coarse = [coarse_delete(x[0]) for x in e4.generators]
    expected_coarse = [target[0] for target in targets_e]
    diagnostic = independent_coarse_diagnostic(actual_coarse, expected_coarse)
    require(diagnostic["all_literal_equal"], "literal marked coarse deletion")
    public = {
        "coarse_method": "literal_fourth_P_and_G9_block_restriction",
        "coarse_marked_images_sha256": sha_obj([list(x) for x in actual_coarse]),
        "coarse_marked_diagnostic": diagnostic,
        "fine": {
            "method": "full_Pi4_marked_Cayley_homomorphism_reconstruction",
            "source_order": len(states), "target_pc_width": len(pc3.one()),
            "marked_images": [list(x) for x in targets],
            "table_sha256": sha_bytes(b"".join(table[k] for k in sorted(table))),
        },
        "left_inverse_endpoint_marked_indices": [1, 2, 4],
        "v122_pinned_not_reproved": True,
    }
    return delete, public


def project(state: Any, delete: Any) -> tuple[Any, ...]:
    rows = state[1]
    return tuple([delete(rows[i - 1]) for i in (21, 22, 23, 24, 25)] +
                 [rows[i - 1] for i in (1, 27, 21, 26, 28)])


class GammaModel:
    def __init__(self, old: Any, e3: Any, e4: Any, contexts: Sequence[Any],
                 words: Sequence[Sequence[int]]) -> None:
        self.old, self.e3, self.e4 = old, e3, e4
        self.contexts = list(contexts); self.words = [list(x) for x in words]
        self.identity = (e3.identity, tuple(e4.identity for _ in contexts))
        self.generators = [self.eval(x) for x in words]
        self.states = [self.identity]; self.ids = {self.key(self.identity): 0}
        self.parent = [0]; self.parent_generator = [0]
        for sid, state in enumerate(self.states):
            for gid, generator in enumerate(self.generators):
                nxt = self.mul(state, generator); key = self.key(nxt)
                if key not in self.ids:
                    self.ids[key] = len(self.states); self.states.append(nxt)
                    self.parent.append(sid + 1); self.parent_generator.append(gid + 1)
        require(len(self.states) == EXPECTED_GAMMA, "Gamma order")

    def key(self, state: Any) -> tuple[bytes, ...]:
        return (blob(self.old, state[0]),) + tuple(blob(self.old, x) for x in state[1])

    def mul(self, left: Any, right: Any) -> Any:
        return (self.e3.mul(left[0], right[0]),
                tuple(self.e4.mul(a, b) for a, b in zip(left[1], right[1])))

    def eval(self, word: Sequence[int]) -> Any:
        return (self.e3.eval(self.old.embed_f2_pb3(word)),
                tuple(self.e4.eval(word, pair) for pair in self.contexts))

    def section_word(self, sid: int) -> list[int]:
        factors = []
        while sid:
            factors.append(self.parent_generator[sid] - 1); sid = self.parent[sid] - 1
        out: list[int] = []
        for gid in reversed(factors):
            out = self.old.reduce_word(out + self.words[gid])
        return out

    def closure(self, generators: Sequence[int]) -> set[int]:
        rows = list(dict.fromkeys(generators)); seen = {0}; queue = [0]
        for sid in queue:
            for gid in rows:
                nxt = self.ids[self.key(self.mul(self.states[sid], self.states[gid]))]
                if nxt not in seen:
                    seen.add(nxt); queue.append(nxt)
        return seen


def qmul(old: Any, left: bytes, right: bytes) -> bytes:
    return bytes(old.perm_mul(tuple(left), tuple(right)))


def qinv(old: Any, row: bytes) -> bytes:
    return bytes(old.perm_inv(tuple(row)))


def independent_gamma_coarse_statistics(old: Any,
                                        projected: Sequence[Sequence[Any]]) -> list[dict[str, Any]]:
    require(len(projected) == EXPECTED_GAMMA, "Gamma coarse source count")
    rows: list[dict[str, Any]] = []
    for index, expected_order in enumerate(EXPECTED_GAMMA_COARSE_ORDERS):
        degree = 36 if index < 5 else 144
        values: list[bytes] = []
        for state in projected:
            require(len(state) == 10, "Gamma projected row width")
            raw = blob(old, state[index])
            require(len(raw) == WIDTHS[index], "Gamma projected blob width")
            values.append(canonical_packed_permutation(raw[:degree], degree,
                                                       "independent Gamma coarse value"))
        image = set(values)
        require(len(image) == expected_order and bytes(range(degree)) in image,
                f"independent S{index} Gamma coarse order")
        require(all(qinv(old, item) in image for item in image) and
                all(qmul(old, a, b) in image for a in image for b in image),
                f"independent S{index} Gamma coarse subgroup")
        require(EXPECTED_GAMMA % expected_order == 0,
                f"independent S{index} Gamma coarse kernel")
        rows.append({
            "label": f"S{index}",
            "type": COORDINATES[index]["type"],
            "coarse_degree": degree,
            "source_state_count": EXPECTED_GAMMA,
            "image_order": len(image),
            "kernel_order": EXPECTED_GAMMA // len(image),
            "state_sequence_sha256": sha_bytes(b"".join(values)),
            "canonical_image_roster_sha256": sha_bytes(b"".join(sorted(image))),
            "group_checks": {"identity": True, "inverses": True, "closure": True},
            "all_243_literal_states_replayed": True,
        })
    return rows


def qclosure(old: Any, generators: Sequence[int], states: Sequence[bytes],
             ids: dict[bytes, int]) -> set[int]:
    tables = [make_translation(states[x]) for x in dict.fromkeys(generators)]
    seen = {0}; queue = [0]
    for sid in queue:
        for table in tables:
            target = ids[states[sid].translate(table)]
            if target not in seen:
                seen.add(target); queue.append(target)
    return seen


def qword(sid: int, parents: Sequence[int], letters: bytes) -> list[int]:
    out = []
    while sid:
        out.append(letters[sid]); sid = parents[sid]
    return list(reversed(out))


def family_key(row: Sequence[bytes], indices: Sequence[int]) -> tuple[bytes, ...]:
    return tuple(row[i] for i in indices)


def family_identity(old: Any, indices: Sequence[int], e3: Any, e4: Any) -> tuple[bytes, ...]:
    return tuple(blob(old, e3.identity if i < 5 else e4.identity) for i in indices)


def family_inverse(key: Sequence[bytes], indices: Sequence[int], e3: Any, e4: Any,
                   old: Any) -> tuple[bytes, ...]:
    return tuple(blob(old, (e3 if i < 5 else e4).inverse(value(raw, i)))
                 for raw, i in zip(key, indices))


def multiply_blob(old: Any, left: bytes, right: bytes, index: int,
                  e3: Any, e4: Any) -> bytes:
    group = e3 if index < 5 else e4
    return blob(old, group.mul(value(left, index), value(right, index)))


def inverse_blob(old: Any, raw: bytes, index: int, e3: Any, e4: Any) -> bytes:
    group = e3 if index < 5 else e4
    return blob(old, group.inverse(value(raw, index)))


def section_row(stores: Sequence[bytes | bytearray], sid: int) -> tuple[bytes, ...]:
    return tuple(bytes(store[sid * width:(sid + 1) * width])
                 for store, width in zip(stores, WIDTHS))


def eval_coords(old: Any, e3: Any, e4: Any, contexts: Sequence[Any], delete: Any,
                word: Sequence[int]) -> tuple[Any, ...]:
    return tuple([delete(e4.eval(word, contexts[i - 1])) for i in (21, 22, 23, 24, 25)] +
                 [e4.eval(word, contexts[i - 1]) for i in (1, 27, 21, 26, 28)])


def validate_family_order_record(public: dict[str, Any], name: str,
                                 indices: Sequence[int], a_order: int,
                                 l_order: int, q_order: int) -> int:
    require(public["label"] == name and
            public["coordinate_indices"] == list(indices), f"{name} family typing")
    require(a_order > 0 and l_order > 0 and q_order % l_order == 0,
            f"{name} family Lagrange")
    index = q_order // l_order; d_order = a_order * index
    require(public["A_order"] == a_order and public["L_order"] == l_order and
            public["Q0_index_L"] == index and public["D_order"] == d_order and
            public["formula"] == "|D_S|=|A_S|*[Q0:L_S]",
            f"{name} family order formula")
    return d_order


def verify_complete(receipt: dict[str, Any]) -> dict[str, Any]:
    result = receipt["result"]
    require(result["extension"] == {"Gamma_order": EXPECTED_GAMMA,
                                    "Q0_order": EXPECTED_Q0,
                                    "exact_sequence": "1->Gamma->G->Q0->1"},
            "extension metadata")
    old = load_module(ROOT / PINS["e4_arithmetic"][0], "d176_check_frozen_e4")
    q3 = json.loads(Q3_PATH.read_text(encoding="utf-8"))
    joint_receipt = json.loads(JOINT_PATH.read_text(encoding="utf-8"))
    e3, e4, _ = old.reconstruct_quotients(q3)
    contexts, aliases, context_public = old.cheap_context_registry(e4)
    require(len(contexts) == 31 and len(aliases) == 46, "registry reconstruction")
    require(result["registry"] == {
        "context_count": 31, "public_sha256": sha_obj(context_public),
        "selected_context_ids": [21, 22, 23, 24, 25, 1, 27, 21, 26, 28],
        "C21_typed_reuse_not_deduplicated": True}, "registry receipt")
    delete, deletion_public = reconstruct_deletion(e3, e4)
    claimed_deletion = result["deletion"]
    actual_coarse = [coarse_delete(generator[0]) for generator in e4.generators]
    expected_coarse = [target[0] for target in
                       [e3.generators[0], e3.generators[1], e3.identity,
                        e3.generators[2], e3.identity, e3.identity]]
    validate_coarse_diagnostic(claimed_deletion["coarse_marked_diagnostic"],
                               actual_coarse, expected_coarse)
    require(result["deletion"] == deletion_public, "deletion receipt reconstruction")
    words = [list(row["word"]) for row in q3["correction_fibre"]["records"] if row["word"]]
    gamma = GammaModel(old, e3, e4, contexts, words)
    projected = [project(x, delete) for x in gamma.states]
    gamma_coarse_images = independent_gamma_coarse_statistics(old, projected)
    projected_raw = b"".join(blob(old, x) for row in projected for x in row)
    gamma_public = result["Gamma"]
    require(gamma_public["record_words"] == words, "Gamma words")
    require(unpack(gamma_public["ten_coordinate_states"], sum(WIDTHS), EXPECTED_GAMMA) ==
            projected_raw, "Gamma ten-coordinate roster")
    gp = unpack(gamma_public["section_parent_states_u16le"], 2, EXPECTED_GAMMA)
    gg = unpack(gamma_public["section_parent_record_u8"], 1, EXPECTED_GAMMA)
    require([struct.unpack_from("<H", gp, 2 * i)[0] for i in range(EXPECTED_GAMMA)] ==
            gamma.parent and list(gg) == gamma.parent_generator, "Gamma section tables")

    coordinate_marks = []
    for item in COORDINATES:
        pair = contexts[item["context_id"] - 1]
        row = [e4.eval([x], pair) for x in (1, 2)]
        if item["type"] == "E3": row = [delete(x) for x in row]
        coordinate_marks.append(row)

    A_maps: dict[str, dict[tuple[bytes, ...], int]] = {}
    for name, indices in FAMILIES:
        first: dict[tuple[bytes, ...], int] = {}
        for sid, row in enumerate(projected):
            first.setdefault(tuple(blob(old, row[i]) for i in indices), sid)
        table = [{"coordinate_blobs_hex": [x.hex() for x in key],
                  "gamma_state_id": first[key] + 1} for key in sorted(first)]
        public = result["A_families"][name]
        require(public["order"] == len(first) and public["literal_elements"] == table and
                public["literal_table_sha256"] == sha_obj(table), f"{name} A table")
        # Independent exhaustive group laws and x/y normality.
        keys = set(first); ident = family_identity(old, indices, e3, e4)
        require(ident in keys, f"{name} A identity")
        for left in keys:
            require(family_inverse(left, indices, e3, e4, old) in keys,
                    f"{name} A inverse")
            for right in keys:
                product = tuple(blob(old, (e3 if i < 5 else e4).mul(value(a, i), value(b, i)))
                                for i, a, b in zip(indices, left, right))
                require(product in keys, f"{name} A closure")
            for letter in range(2):
                conjugate = []
                for i, raw in zip(indices, left):
                    group = e3 if i < 5 else e4; outer = coordinate_marks[i][letter]
                    conjugate.append(blob(old, group.mul(group.mul(group.inverse(outer),
                                                                   value(raw, i)), outer)))
                require(tuple(conjugate) in keys, f"{name} A normality")
        require(public["group_checks"] == {"identity": True, "closure": True,
                                           "inverses": True,
                                           "normal_under_section_x_y": True},
                f"{name} A check receipt")
        A_maps[name] = first

    qpub = result["Q0_section"]
    roster_raw = unpack(qpub["canonical_roster"], 36, EXPECTED_Q0)
    claimed_states = [roster_raw[36 * i:36 * (i + 1)] for i in range(EXPECTED_Q0)]
    parent_raw = unpack(qpub["parent_states_u32le"], 4, EXPECTED_Q0)
    claimed_parent_one = [struct.unpack_from("<I", parent_raw, 4 * i)[0]
                          for i in range(EXPECTED_Q0)]
    claimed_letters = unpack(qpub["parent_letters_u8"], 1, EXPECTED_Q0)
    require(qpub["roster_sha256"] == sha_bytes(roster_raw), "Q0 roster digest")
    require(qpub["ten_coordinate_marked_generator_blobs_hex"] ==
            [[blob(old, x).hex() for x in row] for row in coordinate_marks] and
            qpub["all_section_values_losslessly_reconstructible"] is True and
            qpub["section_value_decoder"] ==
            "replay parent_letters from root with the literal typed marked-generator blobs" and
            qpub["lossless_image_section_primitive"] ==
            "for every Q0 state q, parent/letter decodes s(q) and its ten literal values; pair with any A-table Gamma index",
            "lossless section decoder")
    q0_marked = [canonical_packed_permutation(old.perm_from_row(row, 36), 36,
                                              "Q0 marked generator")
                 for row in q3["coarse_models"]["Q0"]["marked_permutations"]]
    q0_relators = qpub["complete_presentation_relators"]
    q0_identity = canonical_packed_permutation(old.perm_one(36), 36, "Q0 identity")
    require(len(q0_relators) == 19 and
            all(canonical_packed_permutation(old.eval_perm_word(word, q0_marked), 36,
                                             "Q0 relator value") == q0_identity
                for word in q0_relators) and
            sha_obj(q0_relators) == qpub["complete_presentation_relators_sha256"] ==
            joint_receipt["q0_presentation"]["complete_relators_sha256"] and
            qpub["presentation_completeness"] ==
            "pinned v121 plus frozen task157ee factor presentations and split words",
            "complete Q0 presentation")
    qtables = [make_translation(x) for x in q0_marked]
    states = [bytes(range(36))]; ids = {states[0]: 0}; parents = [0]; letters = bytearray([0])
    stores = [bytearray(blob(old, e3.identity if i < 5 else e4.identity)) for i in range(10)]
    right_tables = [[make_translation(coordinate_marks[i][j][0]) for j in range(2)]
                    for i in range(10)]
    pc_cache: dict[tuple[int, int, bytes], bytes] = {}
    for sid, state in enumerate(states):
        require(sid < EXPECTED_Q0 and state == claimed_states[sid], "Q0 discovery row")
        expected_parent = 0 if sid == 0 else parents[sid] + 1
        require(claimed_parent_one[sid] == expected_parent and
                claimed_letters[sid] == letters[sid], "Q0 parent/letter")
        for letter in range(2):
            nxt = state.translate(qtables[letter])
            if nxt in ids: continue
            ids[nxt] = len(states); states.append(nxt); parents.append(sid); letters.append(letter + 1)
            for i, width in enumerate(WIDTHS):
                degree = 36 if i < 5 else 144
                raw = bytes(stores[i][sid * width:(sid + 1) * width])
                pc_left = raw[degree:]; cache_key = (i, letter, pc_left)
                pc_raw = pc_cache.get(cache_key)
                group = e3 if i < 5 else e4
                if pc_raw is None:
                    pc_raw = bytes(group.pc.mul(pc_left, coordinate_marks[i][letter][1]))
                    pc_cache[cache_key] = pc_raw
                stores[i].extend(raw[:degree].translate(right_tables[i][letter]) + pc_raw)
    require(len(states) == EXPECTED_Q0 and bytes(letters) == claimed_letters and
            b"".join(states) == roster_raw, "Q0 independent completion")

    memberships: dict[str, bytearray] = {
        name: bytearray((EXPECTED_Q0 + 7) // 8) for name, _ in FAMILIES}
    counts = {name: 0 for name, _ in FAMILIES}
    for sid in range(EXPECTED_Q0):
        row = section_row(stores, sid)
        for name, indices in FAMILIES:
            if family_key(row, indices) in A_maps[name]:
                memberships[name][sid >> 3] |= 1 << (sid & 7); counts[name] += 1

    independent_L_generators: dict[str, list[int]] = {}
    for name, indices in FAMILIES:
        public = result["families"][name]
        claimed_bits = unpack(public["membership_bitset"], 1, len(memberships[name]))
        require(claimed_bits == bytes(memberships[name]), f"{name} membership bitset")
        require(counts[name] == public["L_order"] and EXPECTED_Q0 % counts[name] == 0,
                f"{name} L order")
        selected: list[int] = []; subgroup = {0}
        for sid in range(EXPECTED_Q0):
            if bit_get(claimed_bits, sid) and sid not in subgroup:
                selected.append(sid); subgroup = qclosure(old, selected, states, ids)
                require(all(bit_get(claimed_bits, x) for x in subgroup), f"{name} L closure")
                if len(subgroup) == counts[name]: break
        require(len(subgroup) == counts[name] and
                all((sid in subgroup) == bit_get(claimed_bits, sid)
                    for sid in range(EXPECTED_Q0)), f"{name} L exact subgroup")
        for gid in selected:
            require(ids[qinv(old, states[gid])] in subgroup, f"{name} L inverse")
            normal_rows = []
            for outer in q0_marked:
                conjugate = qmul(old, qmul(old, qinv(old, bytes(outer)), states[gid]),
                                 bytes(outer))
                require(ids[conjugate] in subgroup, f"{name} L normality")
                normal_rows.append([gid + 1, ids[bytes(outer)], ids[conjugate] + 1])
        proof = public["L_group_checks"]
        require(proof["greedy_generator_state_ids"] == [x + 1 for x in selected] and
                proof["generated_order"] == counts[name] and
                all(proof[k] is True for k in ("identity", "closure_by_exact_generated_subgroup",
                                                "inverse_generators_in_subgroup", "normal_under_q0_x_y")),
                f"{name} L proof receipt")
        expected_normal = []
        for gid in selected:
            for outer in q0_marked:
                conjugate = qmul(old, qmul(old, qinv(old, bytes(outer)), states[gid]),
                                 bytes(outer))
                expected_normal.append([gid + 1, ids[bytes(outer)], ids[conjugate] + 1])
        require(proof["normality_witness_rows"] == expected_normal,
                f"{name} normality witness rows")
        validate_family_order_record(public, name, indices, len(A_maps[name]),
                                     counts[name], EXPECTED_Q0)
        independent_L_generators[name] = selected
    dall = result["families"]["ALL"]["D_order"]
    for i in range(10):
        di = result["families"][f"S{i}"]["D_order"]
        require(dall % di == 0 and result["projection_kernel_orders"][f"S{i}"] == dall // di,
                f"S{i} kernel quotient")

    section_public = result["section_independence"]
    require(section_public["method"] == "fixed nonidentity left Gamma twist" and
            section_public["sample_count"] == len(section_public["samples"]) > 0,
            "section-independence header")
    full_identity = family_identity(old, tuple(range(10)), e3, e4)
    for sample in section_public["samples"]:
        target = sample["target_q0_state_id"] - 1
        twist_id = sample["twist_gamma_state_id"] - 1
        require(0 <= target < EXPECTED_Q0 and 0 <= twist_id < EXPECTED_GAMMA,
                "section sample address")
        canonical_row = section_row(stores, target)
        twist_row = tuple(blob(old, x) for x in projected[twist_id])
        alt = [multiply_blob(old, twist_row[i], canonical_row[i], i, e3, e4)
               for i in range(10)]
        require(sample["alternate_ten_coordinate_blobs_hex"] == [x.hex() for x in alt],
                "alternate section literals")
        delta = tuple(multiply_blob(old, alt[i], inverse_blob(old, canonical_row[i], i, e3, e4),
                                    i, e3, e4) for i in range(10))
        require(delta == twist_row and delta in A_maps["ALL"] and delta != full_identity,
                "nontrivial Gamma section twist")
        comparisons = {name: ((family_key(alt, indices) in A_maps[name]) ==
                              (family_key(canonical_row, indices) in A_maps[name]))
                       for name, indices in FAMILIES}
        require(all(comparisons.values()) and
                sample["family_membership_equal"] == comparisons,
                "section membership independence")

    # Rebuild both kinds of literal source-word generators and replay every
    # row in all ten coordinates.
    for name, indices in FAMILIES:
        ident = family_identity(old, indices, e3, e4)
        kernel = {sid for sid, row in enumerate(projected)
                  if tuple(blob(old, row[i]) for i in indices) == ident}
        gselected: list[int] = []; subgroup = {0}
        for sid in sorted(kernel):
            if sid not in subgroup:
                gselected.append(sid); subgroup = gamma.closure(gselected)
        require(subgroup == kernel, f"{name} Gamma kernel")
        public = result["word_generators"][name]
        require(public["Gamma_S0_order"] == len(kernel) and
                len(public["Gamma_S0_generators"]) == len(gselected),
                f"{name} Gamma word roster")
        for row, sid in zip(public["Gamma_S0_generators"], gselected):
            expected_word = gamma.section_word(sid)
            replay = eval_coords(old, e3, e4, contexts, delete, row["source_word"])
            require(row["gamma_state_id"] == sid + 1 and row["source_word"] == expected_word and
                    row["ten_coordinate_blobs_hex"] == [blob(old, x).hex() for x in replay] and
                    tuple(blob(old, replay[i]) for i in indices) == ident,
                    f"{name} Gamma word replay")
        adjusted = public["adjusted_L_generators"]
        require(len(adjusted) == len(independent_L_generators[name]),
                f"{name} adjusted word count")
        for row, qid in zip(adjusted, independent_L_generators[name]):
            skey = family_key(section_row(stores, qid), indices)
            need = family_inverse(skey, indices, e3, e4, old)
            require(need in A_maps[name], f"{name} adjustment exists")
            gid = A_maps[name][need]
            expected_word = old.reduce_word(gamma.section_word(gid) + qword(qid, parents, letters))
            replay = eval_coords(old, e3, e4, contexts, delete, row["source_word"])
            require(row["q0_state_id"] == qid + 1 and
                    row["gamma_adjustment_state_id"] == gid + 1 and
                    row["source_word"] == expected_word and
                    row["ten_coordinate_blobs_hex"] == [blob(old, x).hex() for x in replay] and
                    tuple(blob(old, replay[i]) for i in indices) == ident,
                    f"{name} adjusted word replay")

    image_generators = [[projected[gamma.ids[gamma.key(g)]][i]
                         for g in gamma.generators] + list(coordinate_marks[i])
                        for i in range(10)]
    directed = []
    bucket_stats = []
    for target in range(10):
        degree = 36 if target < 5 else 144
        coarse_to_q: dict[bytes, int | list[int]] = {}
        for qid in range(EXPECTED_Q0):
            raw = bytes(stores[target][qid * WIDTHS[target]:(qid + 1) * WIDTHS[target]])
            coarse = raw[:degree]; prior = coarse_to_q.get(coarse)
            if prior is None:
                coarse_to_q[coarse] = qid
            elif isinstance(prior, int):
                coarse_to_q[coarse] = [prior, qid]
            else:
                prior.append(qid)
        bucket_stats.append(independent_bucket_statistics(target, degree, coarse_to_q))
        for source in range(10):
            if (source < 5) != (target < 5):
                directed.append({"left": f"S{source}", "right": f"S{target}",
                                 "relation": "NOT_COMPARABLE_DIFFERENT_TYPED_AMBIENT"})
                continue
            contained = True
            for element in image_generators[source]:
                raw = blob(old, element); candidate = coarse_to_q.get(raw[:degree])
                if candidate is None:
                    contained = False; break
                candidates = [candidate] if isinstance(candidate, int) else candidate
                found = False
                for qid in candidates:
                    section = bytes(stores[target][qid * WIDTHS[target]:(qid + 1) * WIDTHS[target]])
                    residual = multiply_blob(old, raw,
                                             inverse_blob(old, section, target, e3, e4),
                                             target, e3, e4)
                    if (residual,) in A_maps[f"S{target}"]:
                        found = True; break
                if not found:
                    contained = False; break
            directed.append({"left": f"S{source}", "right": f"S{target}",
                             "relation": "SUBGROUP" if contained else "NOT_SUBGROUP",
                             "generator_membership_test_count": len(image_generators[source])})
        del coarse_to_q
    typed = result["typed_singleton_images"]
    require(typed["directed_generator_containment"] == directed,
            "typed directed containment")
    claimed_stats = typed.get("raw_section_coarse_key_bucket_statistics")
    require(type(claimed_stats) is list and len(claimed_stats) == 10,
            "typed coarse bucket statistic roster")
    statistic_keys = set(bucket_stats[0])
    for target, (claimed, rebuilt) in enumerate(zip(claimed_stats, bucket_stats)):
        require(type(claimed) is dict and set(claimed) == statistic_keys,
                f"S{target} coarse bucket statistic keys")
        for key in statistic_keys:
            require(claimed.get(key) == rebuilt[key],
                    f"S{target} coarse bucket statistic {key}")
    claimed_gamma_coarse = typed.get("Gamma_coarse_images")
    require(type(claimed_gamma_coarse) is list and len(claimed_gamma_coarse) == 10,
            "Gamma coarse image statistic roster")
    gamma_statistic_keys = set(gamma_coarse_images[0])
    for coordinate, (claimed, rebuilt) in enumerate(zip(claimed_gamma_coarse,
                                                        gamma_coarse_images)):
        require(type(claimed) is dict and set(claimed) == gamma_statistic_keys,
                f"S{coordinate} Gamma coarse image statistic keys")
        for key in gamma_statistic_keys:
            require(claimed.get(key) == rebuilt[key],
                    f"S{coordinate} Gamma coarse image statistic {key}")
    lookup = {(x["left"], x["right"]): x["relation"] for x in directed}
    matrix = []
    for i in range(10):
        row = []
        for j in range(10):
            if (i < 5) != (j < 5): row.append("TYPED_NOT_COMPARABLE")
            else:
                row.append("EQUAL" if lookup[(f"S{i}", f"S{j}")] == "SUBGROUP" and
                           lookup[(f"S{j}", f"S{i}")] == "SUBGROUP" else "UNEQUAL")
        matrix.append(row)
    require(typed["equality_matrix"] == matrix and
            typed["coordinate_0_7_equal"] is False and
            len(typed["orders"]) == 10, "typed equality/order table")

    require(result["registry"]["C21_typed_reuse_not_deduplicated"] is True and
            result["performance"]["direct_Delta_states_enumerated"] == 0 and
            result["proof_pins"] == {"v108": "pinned_not_reproved",
                                     "v121": "pinned_not_reproved",
                                     "v122": "pinned_not_reproved", "v125": "implemented",
                                     "v135": public_v135_pin()},
            "scope/pin boundary")
    return {"Gamma_order": EXPECTED_GAMMA, "Q0_order": EXPECTED_Q0,
            "family_count": 11, "direct_word_replay": True,
            "full_D_order": dall}


TOY_KINDS = ("H", "A", "B", "Q", "TRIVIAL",
             "FULL", "AQ", "FULL", "BQ", "Q")
TOY_ID = (0, 0, 0, 0)
TOY_GENERATORS = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1))


def toy_mul(left: tuple[int, int, int, int],
            right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, c, q = left; x, y, z, r = right
    return ((a + x) % 3, (b + y) % 3, (c + z + a * y) % 3, (q + r) % 2)


def toy_inverse(row: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, c, q = row
    return ((-a) % 3, (-b) % 3, (-c + a * b) % 3, (-q) % 2)


def toy_project(kind: str, row: tuple[int, int, int, int]) -> tuple[int, ...]:
    a, b, c, q = row
    if kind == "FULL": return row
    if kind == "H": return (a, b, c)
    if kind == "AQ": return (a, q)
    if kind == "BQ": return (b, q)
    if kind == "A": return (a,)
    if kind == "B": return (b,)
    if kind == "Q": return (q,)
    require(kind == "TRIVIAL", "toy projection kind")
    return ()


def toy_target_mul(kind: str, left: tuple[int, ...],
                   right: tuple[int, ...]) -> tuple[int, ...]:
    if kind == "FULL": return toy_mul(tuple(left), tuple(right))
    if kind == "H":
        a, b, c = left; x, y, z = right
        return ((a + x) % 3, (b + y) % 3, (c + z + a * y) % 3)
    if kind in {"AQ", "BQ"}:
        return ((left[0] + right[0]) % 3, (left[1] + right[1]) % 2)
    if kind in {"A", "B"}: return ((left[0] + right[0]) % 3,)
    if kind == "Q": return ((left[0] + right[0]) % 2,)
    require(kind == "TRIVIAL", "toy target product kind")
    return ()


def toy_target_inverse(kind: str, row: tuple[int, ...]) -> tuple[int, ...]:
    if kind == "FULL": return toy_inverse(tuple(row))
    if kind == "H":
        a, b, c = row
        return ((-a) % 3, (-b) % 3, (-c + a * b) % 3)
    if kind in {"AQ", "BQ"}: return ((-row[0]) % 3, (-row[1]) % 2)
    if kind in {"A", "B"}: return ((-row[0]) % 3,)
    if kind == "Q": return ((-row[0]) % 2,)
    require(kind == "TRIVIAL", "toy target inverse kind")
    return ()


def toy_json(value: Any) -> Any:
    if isinstance(value, tuple): return [toy_json(x) for x in value]
    if isinstance(value, list): return [toy_json(x) for x in value]
    return value


def toy_eval_word(word: Sequence[int]) -> tuple[int, int, int, int]:
    out = TOY_ID
    for letter in word:
        require(1 <= abs(letter) <= 3, "toy source letter")
        generator = TOY_GENERATORS[abs(letter) - 1]
        out = toy_mul(out, generator if letter > 0 else toy_inverse(generator))
    return out


def toy_enumerate_gamma() -> tuple[list[tuple[int, int, int, int]], list[int], list[int],
                                   dict[tuple[int, int, int, int], int]]:
    generators = TOY_GENERATORS[:2]
    states = [TOY_ID]; parents = [0]; letters = [0]; ids = {TOY_ID: 0}
    for sid, state in enumerate(states):
        for letter, generator in enumerate(generators, 1):
            nxt = toy_mul(state, generator)
            if nxt not in ids:
                ids[nxt] = len(states); states.append(nxt)
                parents.append(sid + 1); letters.append(letter)
    require(len(states) == 27, "toy Gamma order")
    return states, parents, letters, ids


def toy_gamma_word(sid: int, parents: Sequence[int], letters: Sequence[int]) -> list[int]:
    out = []
    while sid:
        out.append(int(letters[sid])); sid = int(parents[sid]) - 1
    return list(reversed(out))


def toy_gamma_closure(generators: Sequence[int],
                      states: Sequence[tuple[int, int, int, int]],
                      ids: dict[tuple[int, int, int, int], int]) -> set[int]:
    rows = list(dict.fromkeys(int(x) for x in generators)); seen = {0}; queue = [0]
    for sid in queue:
        for gid in rows:
            target = ids[toy_mul(states[sid], states[gid])]
            if target not in seen:
                seen.add(target); queue.append(target)
    return seen


def toy_coordinate_row(element: tuple[int, int, int, int]) -> tuple[tuple[int, ...], ...]:
    return tuple(toy_project(kind, element) for kind in TOY_KINDS)


def toy_family_row(element: tuple[int, int, int, int],
                   indices: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    row = toy_coordinate_row(element)
    return tuple(row[i] for i in indices)


def toy_family_identity(indices: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    return toy_family_row(TOY_ID, indices)


def toy_family_inverse(row: Sequence[tuple[int, ...]],
                       indices: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    return tuple(toy_target_inverse(TOY_KINDS[i], x) for i, x in zip(indices, row))


def toy_family_mul(left: Sequence[tuple[int, ...]], right: Sequence[tuple[int, ...]],
                   indices: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    return tuple(toy_target_mul(TOY_KINDS[i], a, b)
                 for i, a, b in zip(indices, left, right))


def build_toy_payload() -> dict[str, Any]:
    gamma, gamma_parents, gamma_letters, gamma_ids = toy_enumerate_gamma()
    q_roster = [0, 1]; q_parents = [0, 1]; q_letters = [0, 1]
    q_words = [[], [3]]; sections = [toy_eval_word(word) for word in q_words]
    projected_gamma = [toy_coordinate_row(x) for x in gamma]
    section_rows = [toy_coordinate_row(x) for x in sections]
    a_maps: dict[str, dict[tuple[tuple[int, ...], ...], int]] = {}
    A_public: dict[str, Any] = {}; family_public: dict[str, Any] = {}
    word_public: dict[str, Any] = {}
    for name, indices in FAMILIES:
        first: dict[tuple[tuple[int, ...], ...], int] = {}
        for sid, row in enumerate(projected_gamma):
            first.setdefault(tuple(row[i] for i in indices), sid)
        a_maps[name] = first
        ordered = sorted(first)
        A_public[name] = {
            "order": len(first),
            "literal_elements": [{"coordinate_values": toy_json(key),
                                  "gamma_state_id": first[key] + 1}
                                 for key in ordered],
            "group_checks": {"identity": True, "closure": True, "inverses": True,
                             "normal_under_section_generator": True},
        }
        membership = [tuple(section_rows[q][i] for i in indices) in first for q in q_roster]
        l_order = sum(membership); index = 2 // l_order; d_order = len(first) * index
        selected_l = [1] if membership[1] else []
        normal_rows = [[qid + 1, 2, qid + 1] for qid in selected_l]
        family_public[name] = {
            "label": name, "coordinate_indices": list(indices), "A_order": len(first),
            "L_membership_bits": membership, "L_order": l_order,
            "Q0_index_L": index, "D_order": d_order,
            "formula": "|D_S|=|A_S|*[Q0:L_S]",
            "L_group_checks": {"identity": True, "closure": True, "inverses": True,
                               "normal_under_Q0_generator": True,
                               "greedy_generator_state_ids": [x + 1 for x in selected_l],
                               "normality_witness_rows": normal_rows},
        }
        identity = toy_family_identity(indices)
        gamma_kernel = {sid for sid, row in enumerate(projected_gamma)
                        if tuple(row[i] for i in indices) == identity}
        selected_gamma: list[int] = []; subgroup = {0}
        for sid in sorted(gamma_kernel):
            if sid not in subgroup:
                selected_gamma.append(sid)
                subgroup = toy_gamma_closure(selected_gamma, gamma, gamma_ids)
        gamma_words = []
        for sid in selected_gamma:
            word = toy_gamma_word(sid, gamma_parents, gamma_letters)
            gamma_words.append({"gamma_state_id": sid + 1, "source_word": word,
                                "ten_coordinate_values": toy_json(toy_coordinate_row(
                                    toy_eval_word(word)))})
        adjusted = []
        for qid in selected_l:
            section_key = tuple(section_rows[qid][i] for i in indices)
            need = toy_family_inverse(section_key, indices)
            gid = first[need]
            word = toy_gamma_word(gid, gamma_parents, gamma_letters) + q_words[qid]
            adjusted.append({"q0_state_id": qid + 1,
                             "gamma_adjustment_state_id": gid + 1,
                             "source_word": word,
                             "ten_coordinate_values": toy_json(toy_coordinate_row(
                                 toy_eval_word(word)))})
        word_public[name] = {"Gamma_S0_order": len(gamma_kernel),
                             "Gamma_S0_generators": gamma_words,
                             "adjusted_L_generators": adjusted,
                             "all_words_replayed_in_ten_coordinates": True}
    dall = family_public["ALL"]["D_order"]
    kernel_orders = {f"S{i}": dall // family_public[f"S{i}"]["D_order"]
                     for i in range(10)}
    source_images = [toy_project("FULL", x) for x in TOY_GENERATORS]
    target_images = [toy_project("H", x) for x in TOY_GENERATORS]
    return {
        "construction": "nonabelian_Heisenberg27_times_C2_extension_section_fixture",
        "coordinate_kinds": list(TOY_KINDS),
        "full_family_coordinates": list(range(10)),
        "deletion": {"source_coordinate": 7, "target_coordinate": 0,
                     "source_marked_images": toy_json(source_images),
                     "target_marked_images": toy_json(target_images),
                     "deleted_marked_images": toy_json([x[:3] for x in source_images]),
                     "marked_identity_holds": True},
        "Gamma": {"order": 27, "literal_elements": toy_json(gamma),
                  "section_parent_states": gamma_parents,
                  "section_parent_letters": gamma_letters,
                  "roster_sha256": sha_obj(toy_json(gamma)),
                  "nonabelian_witness": toy_json([
                      toy_mul(TOY_GENERATORS[0], TOY_GENERATORS[1]),
                      toy_mul(TOY_GENERATORS[1], TOY_GENERATORS[0])])},
        "Q0_section": {"order": 2, "roster": q_roster, "parent_states": q_parents,
                       "parent_letters": q_letters, "source_words": q_words,
                       "ten_coordinate_values": toy_json(section_rows),
                       "canonical_roster_digest": sha_obj(q_roster)},
        "A_families": A_public, "families": family_public,
        "projection_kernel_orders": kernel_orders, "word_generators": word_public,
        "typed_singleton_orders": [{"label": f"S{i}", "kind": TOY_KINDS[i],
                                    "D_order": family_public[f"S{i}"]["D_order"],
                                    "kernel_from_ALL_order": kernel_orders[f"S{i}"]}
                                   for i in range(10)],
    }


def toy_fixture() -> dict[str, Any]:
    receipt = {
        "schema": SCHEMA, "pins": public_pins(), "coordinates": copy.deepcopy(COORDINATES),
        "boundaries": {"all_seven_solution": False, "correction_word": False,
                       "cofinal_lift": False, "fake": False, "Ihara_witness": False,
                       "support_correlation_6441": False, "direct_Delta_enumeration": False},
        "claim": "selftest only", "GHA_dispatched": False,
        "status": "COMPLETE", "terminal": PASS, "reason": None,
        "result": {"selftest_toy": build_toy_payload()}, "selftest_mode": True,
    }
    return reseal(receipt)


def validate_toy_semantics(receipt: dict[str, Any]) -> None:
    toy = receipt["result"].get("selftest_toy")
    require(isinstance(toy, dict) and toy["construction"] ==
            "nonabelian_Heisenberg27_times_C2_extension_section_fixture",
            "toy construction")
    require(toy["coordinate_kinds"] == list(TOY_KINDS) and
            toy["full_family_coordinates"] == list(range(10)), "toy linked coordinates")
    gamma, gamma_parents, gamma_letters, gamma_ids = toy_enumerate_gamma()
    require(toy["Gamma"]["order"] == len(gamma) == 27 and
            toy["Gamma"]["literal_elements"] == toy_json(gamma) and
            toy["Gamma"]["section_parent_states"] == gamma_parents and
            toy["Gamma"]["section_parent_letters"] == gamma_letters and
            toy["Gamma"]["roster_sha256"] == sha_obj(toy_json(gamma)),
            "toy Gamma reconstruction")
    witness = [toy_mul(TOY_GENERATORS[0], TOY_GENERATORS[1]),
               toy_mul(TOY_GENERATORS[1], TOY_GENERATORS[0])]
    require(witness[0] != witness[1] and
            toy["Gamma"]["nonabelian_witness"] == toy_json(witness),
            "toy nonabelian witness")
    q_roster = [0, 1]; q_parents = [0, 1]; q_letters = [0, 1]
    q_words = [[], [3]]; sections = [toy_eval_word(x) for x in q_words]
    section_rows = [toy_coordinate_row(x) for x in sections]
    qpublic = toy["Q0_section"]
    require(qpublic["order"] == 2 and qpublic["roster"] == q_roster and
            qpublic["parent_states"] == q_parents and
            qpublic["parent_letters"] == q_letters and
            qpublic["source_words"] == q_words and
            qpublic["ten_coordinate_values"] == toy_json(section_rows) and
            qpublic["canonical_roster_digest"] == sha_obj(q_roster),
            "toy Q0 section reconstruction")
    deletion = toy["deletion"]
    source_images = [toy_project("FULL", x) for x in TOY_GENERATORS]
    target_images = [toy_project("H", x) for x in TOY_GENERATORS]
    deleted = [x[:3] for x in source_images]
    require(deletion["source_coordinate"] == 7 and deletion["target_coordinate"] == 0 and
            deletion["source_marked_images"] == toy_json(source_images) and
            deletion["target_marked_images"] == toy_json(target_images) and
            deletion["deleted_marked_images"] == toy_json(deleted) and
            deleted == target_images and deletion["marked_identity_holds"] is True,
            "toy deletion reconstruction")
    projected_gamma = [toy_coordinate_row(x) for x in gamma]
    a_maps: dict[str, dict[tuple[tuple[int, ...], ...], int]] = {}
    computed_d: dict[str, int] = {}
    for name, indices in FAMILIES:
        first: dict[tuple[tuple[int, ...], ...], int] = {}
        for sid, row in enumerate(projected_gamma):
            first.setdefault(tuple(row[i] for i in indices), sid)
        a_maps[name] = first; ordered = sorted(first)
        apublic = toy["A_families"][name]
        expected_literals = [{"coordinate_values": toy_json(key),
                              "gamma_state_id": first[key] + 1} for key in ordered]
        require(apublic["order"] == len(first) and
                apublic["literal_elements"] == expected_literals,
                f"toy {name} A literals")
        keys = set(first); identity = toy_family_identity(indices)
        identity_ok = identity in keys
        inverse_ok = all(toy_family_inverse(x, indices) in keys for x in keys)
        closure_ok = all(toy_family_mul(x, y, indices) in keys for x in keys for y in keys)
        outer = toy_family_row(TOY_GENERATORS[2], indices)
        outer_inverse = toy_family_inverse(outer, indices)
        normal_ok = all(toy_family_mul(toy_family_mul(outer_inverse, x, indices),
                                       outer, indices) in keys for x in keys)
        require(identity_ok and inverse_ok and closure_ok and normal_ok and
                apublic["group_checks"] == {"identity": True, "closure": True,
                                             "inverses": True,
                                             "normal_under_section_generator": True},
                f"toy {name} A group laws")
        membership = [tuple(section_rows[q][i] for i in indices) in first
                      for q in q_roster]
        lset = {q for q in q_roster if membership[q]}
        subgroup_ok = (0 in lset and
                       all(((a + b) % 2) in lset for a in lset for b in lset) and
                       all((-a) % 2 in lset for a in lset))
        normal_l_ok = all(((-outer + member + outer) % 2) in lset
                          for outer in q_roster for member in lset)
        require(subgroup_ok and normal_l_ok, f"toy {name} L subgroup/normality")
        selected_l = [1] if 1 in lset else []
        normal_rows = [[qid + 1, 2, qid + 1] for qid in selected_l]
        family = toy["families"][name]
        require(family["L_membership_bits"] == membership and
                family["L_group_checks"] == {
                    "identity": True, "closure": True, "inverses": True,
                    "normal_under_Q0_generator": True,
                    "greedy_generator_state_ids": [x + 1 for x in selected_l],
                    "normality_witness_rows": normal_rows},
                f"toy {name} L semantics")
        computed_d[name] = validate_family_order_record(
            family, name, indices, len(first), len(lset), 2)
        ident = toy_family_identity(indices)
        gamma_kernel = {sid for sid, row in enumerate(projected_gamma)
                        if tuple(row[i] for i in indices) == ident}
        selected_gamma: list[int] = []; subgroup = {0}
        for sid in sorted(gamma_kernel):
            if sid not in subgroup:
                selected_gamma.append(sid)
                subgroup = toy_gamma_closure(selected_gamma, gamma, gamma_ids)
                require(subgroup <= gamma_kernel, f"toy {name} Gamma closure")
        require(subgroup == gamma_kernel, f"toy {name} Gamma kernel")
        words = toy["word_generators"][name]
        require(words["Gamma_S0_order"] == len(gamma_kernel) and
                len(words["Gamma_S0_generators"]) == len(selected_gamma) and
                words["all_words_replayed_in_ten_coordinates"] is True,
                f"toy {name} word header")
        for row, sid in zip(words["Gamma_S0_generators"], selected_gamma):
            source_word = toy_gamma_word(sid, gamma_parents, gamma_letters)
            replay = toy_coordinate_row(toy_eval_word(source_word))
            require(row["gamma_state_id"] == sid + 1 and row["source_word"] == source_word and
                    row["ten_coordinate_values"] == toy_json(replay) and
                    tuple(replay[i] for i in indices) == ident,
                    f"toy {name} Gamma word replay")
        adjusted = words["adjusted_L_generators"]
        require(len(adjusted) == len(selected_l), f"toy {name} adjusted count")
        for row, qid in zip(adjusted, selected_l):
            section_key = tuple(section_rows[qid][i] for i in indices)
            need = toy_family_inverse(section_key, indices)
            require(need in first, f"toy {name} adjustment existence")
            gid = first[need]
            source_word = toy_gamma_word(gid, gamma_parents, gamma_letters) + q_words[qid]
            replay = toy_coordinate_row(toy_eval_word(source_word))
            require(row["q0_state_id"] == qid + 1 and
                    row["gamma_adjustment_state_id"] == gid + 1 and
                    row["source_word"] == source_word and
                    row["ten_coordinate_values"] == toy_json(replay) and
                    tuple(replay[i] for i in indices) == ident,
                    f"toy {name} adjusted word replay")
    dall = computed_d["ALL"]
    require(dall == 54, "toy linked full image order")
    expected_kernels = {}
    for i in range(10):
        require(dall % computed_d[f"S{i}"] == 0, f"toy S{i} quotient")
        expected_kernels[f"S{i}"] = dall // computed_d[f"S{i}"]
    require(toy["projection_kernel_orders"] == expected_kernels,
            "toy kernel-order quotients")
    orders = toy["typed_singleton_orders"]
    require(len(orders) == 10, "toy singleton order width")
    for i, row in enumerate(orders):
        require(row == {"label": f"S{i}", "kind": TOY_KINDS[i],
                        "D_order": computed_d[f"S{i}"],
                        "kernel_from_ALL_order": expected_kernels[f"S{i}"]},
                f"toy singleton order S{i}")


def validate_receipt_chain(receipt: dict[str, Any], allow_selftest: bool = False) -> dict[str, Any]:
    validate_envelope(receipt)
    if receipt["terminal"] != PASS:
        require(receipt.get("selftest_mode") is not True, "unknown selftest confusion")
        return {"terminal": receipt["terminal"], "grade": "UNKNOWN_ACCEPTED_NO_ORDER"}
    if receipt.get("selftest_mode") is True:
        require(allow_selftest, "selftest receipt outside selftest")
        validate_toy_semantics(receipt)
        return {"terminal": PASS, "grade": "SELFTEST_ONLY"}
    return {"terminal": PASS, "grade": "CROSS_CHECKED", **verify_complete(receipt)}


def reject_terminal_selftest() -> int:
    receipt = toy_fixture()
    receipt.pop("selftest_mode")
    receipt.update({"status": "UNKNOWN_INPUT", "terminal": UNKNOWN_INPUT,
                    "reason": f"{CENSUS_REJECT_PREFIX}SELFTEST_INVARIANT",
                    "result": None})
    reseal(receipt)
    audit = validate_receipt_chain(copy.deepcopy(receipt))
    require(audit.get("terminal") == UNKNOWN_INPUT and
            audit.get("grade") == "UNKNOWN_ACCEPTED_NO_ORDER" and
            len(audit) == 2, "typed Reject terminal acceptance")
    checks = 1
    for bad_reason in ("ValueError:SELFTEST_PROGRAMMING_ERROR", CENSUS_REJECT_PREFIX):
        mutation = copy.deepcopy(receipt)
        mutation["reason"] = bad_reason
        reseal(mutation)
        try:
            validate_receipt_chain(mutation)
        except Reject:
            checks += 1
        else:
            raise Reject(f"bad Reject reason accepted: {bad_reason}")
    return checks


def mutation_suite() -> tuple[int, int]:
    baseline = toy_fixture(); validate_receipt_chain(copy.deepcopy(baseline), True)
    mutations = []
    def add(label: str, fn: Any) -> None:
        row = copy.deepcopy(baseline); fn(row); reseal(row); mutations.append((label, row))
    add("coordinate_0_7_typed_dedup", lambda r: r["coordinates"][0].update({"type": "E4"}))
    add("deletion_generator_image", lambda r: r["result"]["selftest_toy"]
        ["deletion"]["source_marked_images"][0].__setitem__(0, 2))
    add("Gamma_element", lambda r: r["result"]["selftest_toy"]
        ["Gamma"]["literal_elements"][1].__setitem__(2, 2))
    add("Q0_parent_letter", lambda r: r["result"]["selftest_toy"]
        ["Q0_section"]["parent_letters"].__setitem__(1, 2))
    add("section_value", lambda r: r["result"]["selftest_toy"]
        ["Q0_section"]["ten_coordinate_values"][1][7].__setitem__(3, 0))
    add("A_literal", lambda r: r["result"]["selftest_toy"]
        ["A_families"]["S0"]["literal_elements"][1]["coordinate_values"][0]
        .__setitem__(0, 2))
    add("L_membership_bit", lambda r: r["result"]["selftest_toy"]
        ["families"]["S0"]["L_membership_bits"].__setitem__(1, False))
    add("L_normality_witness", lambda r: r["result"]["selftest_toy"]
        ["families"]["S0"]["L_group_checks"]["normality_witness_rows"][0]
        .__setitem__(2, 1))
    add("Gamma_adjustment", lambda r: r["result"]["selftest_toy"]
        ["word_generators"]["S0"]["adjusted_L_generators"][0]
        .update({"gamma_adjustment_state_id": 2}))
    add("emitted_source_word", lambda r: r["result"]["selftest_toy"]
        ["word_generators"]["S0"]["adjusted_L_generators"][0]
        ["source_word"].append(2))
    add("full_coordinate_dropped", lambda r: r["result"]["selftest_toy"]["full_family_coordinates"].pop())
    add("singleton_label_swap", lambda r: r["result"]["selftest_toy"]
        ["typed_singleton_orders"][0].update({"label": "S1"}))
    add("kernel_order_quotient", lambda r: r["result"]["selftest_toy"]
        ["projection_kernel_orders"].update({"S4": 8}))
    add("canonical_roster_digest", lambda r: r["result"]["selftest_toy"]
        ["Q0_section"].update({"canonical_roster_digest": "0" * 64}))
    add("terminal_alteration", lambda r: r.update({"terminal": UNKNOWN_RESOURCE}))
    rejected = 0
    for label, row in mutations:
        try:
            validate_receipt_chain(row, True)
        except (Reject, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            raise Reject(f"mutation accepted: {label}")
    return len(mutations), rejected


def write_verdict(path: Path, verdict: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    verdict = reseal(verdict)
    path.write_bytes(canonical(verdict) + b"\n")


def run(args: argparse.Namespace) -> int:
    authenticate()
    if args.selftest:
        fixture = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
        result = validate_receipt_chain(fixture)
        require(result["terminal"] == UNKNOWN_RESOURCE and
                fixture["reason"] == "LOCAL_EXECUTION_GUARD", "immutable fixture")
        perm_type_checks = packed_permutation_selftest()
        require(perm_type_checks == 2, "packed permutation selftest count")
        joint_blob_type_checks = joint_blob_representation_selftest()
        require(joint_blob_type_checks == 8,
                "joint blob representation selftest count")
        deleter_type_checks = deleter_representation_selftest()
        require(deleter_type_checks == 6, "deleter representation selftest count")
        deletion_convention_checks = deletion_convention_selftest()
        require(deletion_convention_checks == 10,
                "deletion convention selftest count")
        reject_checks = reject_terminal_selftest()
        require(reject_checks == 3, "Reject terminal selftest count")
        attempted, rejected = mutation_suite()
        require(attempted == rejected == 15, "mutation count")
        print("R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_CHECKER_SELFTEST_PASS "
              f"mutation_attempted={attempted} mutation_rejected={rejected} "
              f"reject_envelope_checks={reject_checks} "
              f"perm_type_checks={perm_type_checks} "
              f"joint_blob_type_checks={joint_blob_type_checks} "
              f"deleter_type_checks={deleter_type_checks} "
              f"deletion_convention_checks={deletion_convention_checks} "
              "linked_nonabelian_order=54", flush=True)
        return 0
    require(args.receipt and args.verdict, "production arguments")
    raw = Path(args.receipt).read_bytes(); receipt = json.loads(raw)
    audit = validate_receipt_chain(receipt)
    verdict = {
        "schema": "d972-r07-all-seven-extension-section-census-check/v1",
        "receipt_path": str(args.receipt), "receipt_bytes": len(raw),
        "receipt_sha256": sha_bytes(raw), "receipt_terminal": receipt["terminal"],
        "grade": audit.pop("grade"), "audit": audit,
        "producer_sha256": PRODUCER_SHA256,
        "claim_boundary": "no all-seven solution/correction/cofinal/fake/Ihara",
    }
    write_verdict(Path(args.verdict), verdict)
    print("R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_CHECKER_PASS "
          f"terminal={receipt['terminal']}", flush=True)
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(); mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--selftest", action="store_true")
    mode.add_argument("--receipt")
    p.add_argument("--fixture", default=str(FIXTURE)); p.add_argument("--verdict")
    return p


if __name__ == "__main__":
    try:
        raise SystemExit(run(parser().parse_args()))
    except (Reject, FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_CHECKER_STOP {exc}",
              file=sys.stderr, flush=True)
        raise SystemExit(1)
