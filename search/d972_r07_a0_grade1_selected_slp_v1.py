#!/usr/bin/env python3
"""Bounded constructive extraction of the selected grade-one ancestry."""
from __future__ import annotations

import argparse
import bisect
import gc
import hashlib
import importlib.util
import json
import os
import struct
import sys
import time
from pathlib import Path

import numpy as np

try:
    import resource
except ImportError:
    resource = None


ROOT = Path(__file__).resolve().parents[1]
V3_PATH = ROOT / "search/d972_r07_a0_first_rung_grade1_v3.py"
V3_SHA = "bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff"
BODY_SHA = "62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d"
BASIS_SHA = "b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d"
MARKER = "R07_GRADE1_SELECTED_SLP_V1_CANDIDATE"
NODE = struct.Struct("<IBQIQI")
EDGE = struct.Struct("<HB")
LEAF_MAGIC = b"R07LEAF1"
LEAF_VERSION = 1
LEAF_SCHEMA = "d972.r07.a0.literal-leaves.v1"
LEAF_HEADER = struct.Struct("<8sBBBB32sQ")
LEAF_RECORD = struct.Struct("<IIBI")
EMERGENCY_BYTES = 64 * 1024

if hashlib.sha256(V3_PATH.read_bytes()).hexdigest() != V3_SHA:
    raise RuntimeError("v3_hash_preimport")
spec = importlib.util.spec_from_file_location("frozen_v3", V3_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("v3_loader")
v3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v3)

_STARTED = time.monotonic()
_LAST_PHASE = "startup"
_LAST_RSS = 0
_LAST_PEAK = 0
_LAST_CURSORS: dict[str, int | str] = {}
_EMERGENCY: bytearray | None = bytearray(EMERGENCY_BYTES)


def sha(data) -> str:
    return hashlib.sha256(data).hexdigest()


def canon(value) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


def fail(reason: str) -> None:
    raise RuntimeError(reason)


def current_rss() -> int:
    if sys.platform.startswith("linux"):
        try:
            fields = Path("/proc/self/statm").read_text(encoding="ascii").split()
            return int(fields[1]) * int(os.sysconf("SC_PAGE_SIZE"))
        except (OSError, ValueError, IndexError):
            return 0
    return 0


def peak_rss() -> int:
    if resource is None:
        return 0
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value * 1024 if sys.platform.startswith("linux") else value


def phase(name: str, **cursors: int | str) -> None:
    global _LAST_PHASE, _LAST_RSS, _LAST_PEAK, _LAST_CURSORS
    _LAST_PHASE = name
    _LAST_RSS = current_rss()
    _LAST_PEAK = peak_rss()
    _LAST_CURSORS = dict(cursors)
    record = {
        "phase": name,
        "elapsed_seconds": round(time.monotonic() - _STARTED, 6),
        "rss_bytes": _LAST_RSS,
        "peak_rss_bytes": _LAST_PEAK,
    }
    record.update(cursors)
    os.write(2, canon(record))


def emergency_unknown_resource() -> None:
    global _EMERGENCY
    _EMERGENCY = None
    try:
        cursor_text = ",".join(
            "%s=%s" % (key, _LAST_CURSORS[key]) for key in sorted(_LAST_CURSORS)
        )
        message = (
            "UNKNOWN_RESOURCE MemoryError phase=%s rss=%d peak=%d cursors=%s\n"
            % (_LAST_PHASE, _LAST_RSS, _LAST_PEAK, cursor_text)
        ).encode("ascii", "replace")[:1024]
        os.write(2, message)
    except BaseException:
        try:
            os.write(2, b"UNKNOWN_RESOURCE MemoryError\n")
        except BaseException:
            pass


def guard(started: float) -> None:
    if time.monotonic() - started > float(os.environ.get("TASK601_SECONDS", "2400")):
        fail("UNKNOWN_RESOURCE:time")
    if peak_rss() > int(os.environ.get("TASK601_MAX_RSS", str(7 * 1024**3))):
        fail("UNKNOWN_RESOURCE:rss")


def auth_candidate(directory: Path):
    head_raw = (directory / "decision-v2.HEAD").read_bytes()
    head = json.loads(head_raw)
    if (
        sha(head_raw)
        != "07de7a817e8c5ae2e7346402a290c32631d05b0cc621d03702faa6cb43a948c0"
        or head.get("body_sha256") != BODY_SHA
    ):
        fail("candidate_head")
    body_raw = (directory / f"decision-v2.{BODY_SHA}.json").read_bytes()
    if sha(body_raw) != BODY_SHA:
        fail("candidate_body")
    body = json.loads(body_raw)
    if (
        body.get("terminal") != "GRADE1_DECISION_MEMBER"
        or body.get("prepare_sha256") is None
        or body.get("grade_rank") != 5044
        or body.get("lower_rank") != 1661
        or len(body.get("member_coefficients", [])) != 3317
    ):
        fail("candidate_semantics")
    if body.get("basis_receipt", {}).get("sha256") != BASIS_SHA:
        fail("candidate_basis")
    basis = (directory / body["basis_receipt"]["file"]).read_bytes()
    remainder = (directory / body["remainder_receipt"]["file"]).read_bytes()
    if sha(basis) != BASIS_SHA or sha(remainder) != body["remainder_receipt"]["sha256"]:
        fail("candidate_blob")
    return body, basis, remainder


class NodeView:
    def __init__(self, data):
        self.data = memoryview(data).cast("B")
        if len(self.data) % NODE.size:
            fail("node_record_size")

    def __len__(self):
        return len(self.data) // NODE.size

    def __getitem__(self, index: int):
        if not 0 <= index < len(self):
            raise IndexError(index)
        return NODE.unpack_from(self.data, index * NODE.size)


class EdgeView:
    def __init__(self, data):
        self.data = memoryview(data).cast("B")
        if len(self.data) % EDGE.size:
            fail("edge_record_size")

    def __len__(self):
        return len(self.data) // EDGE.size

    def __getitem__(self, index: int):
        if not 0 <= index < len(self):
            raise IndexError(index)
        return EDGE.unpack_from(self.data, index * EDGE.size)


def append_edges(stream: bytearray, reductions) -> tuple[int, int]:
    start = len(stream) // EDGE.size
    count = 0
    for pivot, coefficient in reductions:
        pivot = int(pivot)
        coefficient = int(coefficient)
        if not 0 <= pivot <= 0xFFFF or coefficient not in (1, 2):
            fail("edge_value")
        stream.extend(EDGE.pack(pivot, coefficient))
        count += 1
    return start, count


def append_row(stream: bytearray, row, expected: int) -> None:
    view = memoryview(row).cast("B")
    if len(view) != expected:
        fail("packed_row")
    if len(view) and int(np.frombuffer(view, dtype=np.uint8).max()) > 80:
        fail("packed_row")
    stream.extend(view)


def pack_nodes(records) -> bytearray:
    result = bytearray(len(records) * NODE.size)
    for index, record in enumerate(records):
        NODE.pack_into(result, index * NODE.size, *record)
    return result


def bitset(flags) -> bytearray:
    result = bytearray((len(flags) + 7) // 8)
    for index in np.flatnonzero(flags):
        result[int(index) // 8] |= 1 << (int(index) % 8)
    return result


def write_all(stream, data, digest=None) -> None:
    view = memoryview(data).cast("B")
    if digest is not None:
        digest.update(view)
    offset = 0
    while offset < len(view):
        written = stream.write(view[offset:])
        if not written:
            fail("short_payload_write")
        offset += written


def write_receipt(output: Path, name: str, data) -> dict:
    digest = hashlib.sha256()
    path = output / name
    with path.open("wb") as stream:
        write_all(stream, data, digest)
    return {"file": name, "bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def valid_leaf_key(seed: int, path: tuple[int, ...], coefficient: int) -> None:
    if not 0 < seed <= 0xFFFFFFFF or coefficient not in (1, 2):
        fail("leaf_scalar")
    if len(path) > 0xFFFFFFFF:
        fail("leaf_path_length")
    for index, letter in enumerate(path):
        if letter not in (-2, -1, 1, 2):
            fail("leaf_letter")
        if index and path[index - 1] == -letter:
            fail("leaf_not_reduced")


def leaf_chunks(leaf_map: dict, ancestry_sha256: str):
    keys = sorted(leaf_map)
    yield LEAF_HEADER.pack(
        LEAF_MAGIC,
        LEAF_VERSION,
        1,
        0,
        0,
        bytes.fromhex(ancestry_sha256),
        len(keys),
    )
    previous = None
    for seed, path in keys:
        path = tuple(int(letter) for letter in path)
        coefficient = int(leaf_map[(seed, path)])
        valid_leaf_key(int(seed), path, coefficient)
        key = (int(seed), path)
        if previous is not None and key <= previous:
            fail("leaf_order")
        previous = key
        yield LEAF_RECORD.pack(9 + len(path), int(seed), coefficient, len(path))
        if path:
            yield struct.pack("<%db" % len(path), *path)


def write_leaf_receipt(
    output: Path, name: str, leaf_map: dict, ancestry_sha256: str
) -> dict:
    digest = hashlib.sha256()
    path = output / name
    with path.open("wb") as stream:
        for chunk in leaf_chunks(leaf_map, ancestry_sha256):
            write_all(stream, chunk, digest)
    return {"file": name, "bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def parse_leaf_fixture(data: bytes, ancestry_sha256: str) -> dict:
    view = memoryview(data)
    if len(view) < LEAF_HEADER.size:
        fail("leaf_header")
    magic, version, quotient, common, states, binding, count = LEAF_HEADER.unpack_from(view)
    if (
        magic != LEAF_MAGIC
        or version != LEAF_VERSION
        or (quotient, common, states) != (1, 0, 0)
        or binding != bytes.fromhex(ancestry_sha256)
    ):
        fail("leaf_header")
    cursor = LEAF_HEADER.size
    result = {}
    previous = None
    for _ in range(count):
        if cursor + LEAF_RECORD.size > len(view):
            fail("leaf_record_short")
        payload, seed, coefficient, length = LEAF_RECORD.unpack_from(view, cursor)
        cursor += LEAF_RECORD.size
        if payload != 9 + length or cursor + length > len(view):
            fail("leaf_record_length")
        path = tuple(struct.unpack_from("<%db" % length, view, cursor)) if length else ()
        cursor += length
        valid_leaf_key(seed, path, coefficient)
        key = (seed, path)
        if previous is not None and key <= previous:
            fail("leaf_order")
        previous = key
        result[key] = coefficient
    if cursor != len(view):
        fail("leaf_trailing")
    return result


def make_old_ref(prepare: dict, logical: int, character: int, pivot: int) -> dict:
    item = prepare["old_blocks"][character]
    record = item.get("record", {})
    node = record["dag_nodes"][pivot]
    origin = node["origin"]
    seed = int(origin["seed"]) if origin["kind"] == "projected_seed" else None
    return {
        "logical": logical,
        "kind": "old",
        "character": character,
        "pivot": pivot,
        "old_dag_node": node,
        "defect_origin_range": item.get("defect_origin_range"),
        "seed_index": seed,
        "seed_reduction": (
            record["seed_reductions"][seed - 1] if seed is not None else None
        ),
        "ancestry_key": f"old:{character}:{pivot}",
    }


def execute(args) -> int:
    global _STARTED
    if args.selftest:
        tiny = v3.PackedEchelon(8)
        coefficient_two = tiny.insert(
            np.asarray([0, 2, 0, 0, 0, 0, 0, 0], dtype=np.uint8)
        )
        nonmonotone = v3.PackedEchelon(8)
        nonmonotone.insert(np.asarray([0, 1, 0, 0, 0, 0, 0, 0], dtype=np.uint8))
        nonmonotone.insert(np.asarray([1, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8))
        flags = [False, True, False]
        edges = bytearray()
        append_edges(edges, [(0, 1)])
        edge_view = EdgeView(edges)
        for index in range(2, -1, -1):
            if flags[index] and index == 1:
                flags[edge_view[0][0]] = True
        ancestry_digest = "11" * 32
        leaf_map = {(1, ()): 1, (2, (-2, 1)): 2}
        encoded = b"".join(leaf_chunks(leaf_map, ancestry_digest))
        if parse_leaf_fixture(encoded, ancestry_digest) != leaf_map:
            fail("fixture_leaf_roundtrip")
        header = encoded[: LEAF_HEADER.size]
        first_size = LEAF_RECORD.size
        _, _, _, first_length = LEAF_RECORD.unpack_from(encoded, LEAF_HEADER.size)
        first_size += first_length
        swapped = header + encoded[LEAF_HEADER.size + first_size :] + encoded[LEAF_HEADER.size : LEAF_HEADER.size + first_size]
        try:
            parse_leaf_fixture(swapped, ancestry_digest)
        except RuntimeError:
            pass
        else:
            fail("fixture_leaf_order")
        mutated = bytearray(encoded)
        mutated[LEAF_HEADER.size + 8] = 0
        try:
            parse_leaf_fixture(bytes(mutated), ancestry_digest)
        except RuntimeError:
            pass
        else:
            fail("fixture_leaf_mutation")
        derived = {
            "schema": "d972.r07.a0.selected-literal-derived.v2",
            "leaf_receipt": {"file": "literal-leaves.bin", "schema": LEAF_SCHEMA},
        }
        if "states" in derived:
            fail("fixture_states_present")
        if (
            not coefficient_two.get("accepted")
            or coefficient_two.get("scale") != 2
            or nonmonotone.leads != [1, 0]
            or flags != [True, True, False]
        ):
            fail("fixture_failure")
        print(
            json.dumps(
                {
                    "coefficient_2": "PASS",
                    "compact_leaf_mutations": 2,
                    "compact_leaf_roundtrip": "PASS",
                    "derived_states_absent": "PASS",
                    "fixture": "PASS",
                    "nonmonotone_lead": "PASS",
                    "reverse_closure": "PASS",
                },
                sort_keys=True,
            )
        )
        return 0

    if not args.state or not args.candidate or not args.out:
        fail("usage: --state STATE --candidate CANDIDATE --out OUT")
    _STARTED = time.monotonic()
    started = _STARTED
    if sha(V3_PATH.read_bytes()) != V3_SHA:
        fail("v3_hash")

    decision, basis_blob, remainder_blob = auth_candidate(args.candidate)
    candidate_remainder = np.frombuffer(remainder_blob, dtype=np.uint8)
    if candidate_remainder.shape != (v3.PHYSICAL_GRADE_WIDTH // 4,):
        fail("candidate_remainder_shape")
    prepare, prepare_digest = v3.read_sealed_state(args.state, "prepare")
    _, input_receipt = v3.load_pinned_inputs()
    v3.validate_prepare_state(
        args.state,
        prepare,
        input_receipt,
        fixture=False,
        authenticate_residual=True,
        authenticate_old=True,
        authenticate_packets=range(4),
    )
    if prepare_digest != decision["prepare_sha256"]:
        fail("parent_binding")
    if decision["residual_receipt"] != prepare["residual_blob"]:
        fail("residual_binding")

    context = v3.context_for_state(prepare)
    lower = v3.PackedEchelon(v3.PHYSICAL_LOWER_WIDTH)
    grade = v3.PackedEchelon(v3.PHYSICAL_GRADE_WIDTH)
    lower_companions_dense = []
    lower_nodes = []
    grade_nodes = []
    lower_edges = bytearray()
    grade_edges = bytearray()
    lower_origins = bytearray()
    lower_stored = bytearray()
    lower_companions = bytearray()
    grade_origins = bytearray()
    old_lower_zero = bytearray()
    source_descriptors = []
    logical = 0
    lower_offers = 0
    grade_offers = 0
    lower_width_bytes = v3.PHYSICAL_LOWER_WIDTH // 4
    grade_width_bytes = v3.PHYSICAL_GRADE_WIDTH // 4

    def accept_lower(remainder, reductions, origin: int) -> int:
        nonzero = np.flatnonzero(remainder)
        if not len(nonzero):
            fail("lower_accept_zero")
        byte_index = int(nonzero[0])
        lead = 4 * byte_index + int(v3._PACKED_FIRST[int(remainder[byte_index])])
        coefficient = lower.coefficient(remainder, lead)
        scale = 1 if coefficient == 1 else 2
        normalized = remainder.copy() if scale == 1 else v3._PACKED_SCALE2[remainder]
        pivot = len(lower.rows)
        lower.rows.append(normalized.copy())
        lower.leads.append(lead)
        position = bisect.bisect_left(lower._ordered_keys, (lead, pivot))
        lower._ordered_keys.insert(position, (lead, pivot))
        lower.ordered_pivots.insert(position, pivot)
        lower.lead_to_pivot[lead] = pivot
        edge_start, edge_count = append_edges(lower_edges, reductions)
        lower_nodes.append((origin, scale, edge_start, edge_count, 0, 0))
        return scale

    for item in prepare["old_blocks"]:
        character = int(item["character_index"])
        rank = int(item["rank"])
        low_raw = v3.read_blob(args.state, item["lower_basis_blob"])
        lift_raw = v3.read_blob(args.state, item["lifted_grade_blob"])
        low = np.frombuffer(low_raw, dtype=np.uint8).reshape(
            rank, v3.LOWER_ECHELON_WIDTH // 4
        )
        lift = np.frombuffer(lift_raw, dtype=np.uint8).reshape(
            rank, v3.SOURCE_TOTAL_WIDTH // 4
        )
        for pivot in range(rank):
            occurrence = logical
            lower_row = v3.unpack_trits(low[pivot], v3.LOWER_ECHELON_WIDTH)
            occurrence_lower = np.zeros(
                (4, v3.SOURCE_BASE_WIDTH), dtype=np.uint8
            )
            occurrence_lower[character] = lower_row[: v3.SOURCE_BASE_WIDTH]
            occurrence_grade = v3.unpack_trits(
                lift[pivot], v3.SOURCE_TOTAL_WIDTH
            ).reshape(4, v3.SOURCE_BLOCK_WIDTH)
            physical_lower, physical_grade = v3.aggregate_pair(
                context,
                occurrence_lower,
                occurrence_grade,
                lower_row[v3.SOURCE_BASE_WIDTH :],
            )
            lower_offers += 1
            remainder, reductions = lower.reduce_packed(v3.pack_trits(physical_lower))
            companion = physical_grade.copy()
            for earlier, coefficient in reductions:
                v3._add_mod3(
                    companion,
                    lower_companions_dense[int(earlier)],
                    -int(coefficient),
                )
            if np.any(remainder):
                scale = accept_lower(remainder, reductions, occurrence)
                append_row(lower_origins, v3.pack_trits(physical_lower), lower_width_bytes)
                if scale == 2:
                    companion[:] = (
                        2 * companion.astype(np.uint16) % 3
                    ).astype(np.uint8)
                lower_companions_dense.append(companion)
                append_row(lower_companions, v3.pack_trits(companion), grade_width_bytes)
                append_row(lower_stored, lower.rows[-1], lower_width_bytes)
            else:
                append_row(old_lower_zero, remainder, lower_width_bytes)
                inserted = grade.insert(companion)
                grade_offers += 1
                if inserted["accepted"]:
                    append_row(grade_origins, v3.pack_trits(companion), grade_width_bytes)
                    lower_start, lower_count = append_edges(lower_edges, reductions)
                    edge_start, edge_count = append_edges(
                        grade_edges, inserted["reductions"]
                    )
                    grade_nodes.append(
                        (
                            occurrence,
                            int(inserted["scale"]),
                            edge_start,
                            edge_count,
                            lower_start,
                            lower_count,
                        )
                    )
            source_descriptors.append((occurrence, 0, character, pivot))
            logical += 1
        del low, lift, low_raw, lift_raw
        guard(started)

    if logical != 2014:
        fail("old_cursor")
    del lower_companions_dense
    gc.collect()
    phase(
        "prepare-old-complete",
        logical=logical,
        lower_rank=len(lower.rows),
        grade_rank=len(grade.rows),
    )

    block_digests = []
    for block_index in range(4):
        body, digest = v3.read_sealed_state(
            args.state, f"block-{block_index}", prepare_digest
        )
        v3.validate_block_state(
            args.state,
            body,
            prepare,
            prepare_digest,
            block_index,
            authenticate_basis=True,
        )
        if digest != decision["block_sha256"][block_index]:
            fail("parent_binding")
        block_digests.append(digest)
        owner = v3.load_block_owner(args.state, body)
        for pivot in range(len(owner.rows)):
            occurrence = logical
            origin_grade = v3.aggregate_pure_grade(
                context, block_index, owner.dense_row(pivot)
            )
            inserted = grade.insert(origin_grade)
            grade_offers += 1
            if inserted["accepted"]:
                append_row(grade_origins, v3.pack_trits(origin_grade), grade_width_bytes)
                edge_start, edge_count = append_edges(
                    grade_edges, inserted["reductions"]
                )
                grade_nodes.append(
                    (
                        occurrence,
                        int(inserted["scale"]),
                        edge_start,
                        edge_count,
                        0,
                        0,
                    )
                )
            source_descriptors.append((occurrence, 1, block_index, pivot))
            logical += 1
        del owner, body
        gc.collect()
        guard(started)
        phase(
            "block-routed-released",
            block=block_index,
            logical=logical,
            grade_rank=len(grade.rows),
            grade_edges=len(grade_edges) // EDGE.size,
        )

    if block_digests != decision["block_sha256"]:
        fail("parent_binding")
    if (
        logical,
        len(lower.rows),
        grade_offers,
        len(grade.rows),
    ) != (8059, 1661, 6398, 5044):
        fail("route_mismatch")
    if len(basis_blob) != len(grade.rows) * grade_width_bytes:
        fail("candidate_basis_size")
    basis_digest = hashlib.sha256()
    basis_view = memoryview(basis_blob)
    for pivot, row in enumerate(grade.rows):
        expected = np.frombuffer(
            basis_view,
            dtype=np.uint8,
            count=grade_width_bytes,
            offset=pivot * grade_width_bytes,
        )
        if not np.array_equal(row, expected):
            fail("route_mismatch")
        basis_digest.update(memoryview(row))
    if basis_digest.hexdigest() != BASIS_SHA:
        fail("route_basis_hash")
    guard(started)

    residual_raw = v3.read_blob(args.state, prepare["residual_blob"])
    residual = np.frombuffer(residual_raw, dtype=np.uint8)
    remainder, coefficients = grade.reduce_packed(residual)
    if (
        np.any(remainder)
        or coefficients != decision["member_coefficients"]
        or not np.array_equal(remainder, candidate_remainder)
    ):
        fail("member_mismatch")

    grade_selected = np.zeros(len(grade_nodes), dtype=bool)
    lower_selected = np.zeros(len(lower_nodes), dtype=bool)
    grade_edge_view = EdgeView(grade_edges)
    lower_edge_view = EdgeView(lower_edges)
    for pivot, coefficient in coefficients:
        pivot = int(pivot)
        if not 0 <= pivot < len(grade_nodes) or int(coefficient) not in (1, 2):
            fail("member_coefficient")
        grade_selected[pivot] = True
    for pivot in range(len(grade_nodes) - 1, -1, -1):
        if not grade_selected[pivot]:
            continue
        _, _, edge_start, edge_count, lower_start, lower_count = grade_nodes[pivot]
        for index in range(edge_start, edge_start + edge_count):
            earlier, _ = grade_edge_view[index]
            if earlier >= pivot:
                fail("grade_closure_order")
            grade_selected[earlier] = True
        for index in range(lower_start, lower_start + lower_count):
            earlier, _ = lower_edge_view[index]
            if earlier >= len(lower_selected):
                fail("lower_closure_index")
            lower_selected[earlier] = True
    for pivot in range(len(lower_nodes) - 1, -1, -1):
        if not lower_selected[pivot]:
            continue
        _, _, edge_start, edge_count, _, _ = lower_nodes[pivot]
        for index in range(edge_start, edge_start + edge_count):
            earlier, _ = lower_edge_view[index]
            if earlier >= pivot:
                fail("lower_closure_order")
            lower_selected[earlier] = True

    selected_origins = {
        int(grade_nodes[index][0])
        for index in np.flatnonzero(grade_selected)
    }
    selected_origins.update(
        int(lower_nodes[index][0])
        for index in np.flatnonzero(lower_selected)
    )
    selected_descriptors = [
        descriptor
        for descriptor in source_descriptors
        if int(descriptor[0]) in selected_origins
    ]
    grade_nodes_raw = pack_nodes(grade_nodes)
    lower_nodes_raw = pack_nodes(lower_nodes)
    grade_node_view = NodeView(grade_nodes_raw)
    lower_node_view = NodeView(lower_nodes_raw)
    grade_count = len(grade_node_view)
    lower_count = len(lower_node_view)
    phase(
        "route-member-physical-closure-complete",
        logical=logical,
        coefficients=len(coefficients),
        grade_selected=int(np.count_nonzero(grade_selected)),
        lower_selected=int(np.count_nonzero(lower_selected)),
    )

    output = args.out
    output.mkdir(parents=True, exist_ok=True)
    files = {}
    files["grade_nodes"] = write_receipt(output, "grade-nodes.bin", grade_nodes_raw)
    files["grade_edges"] = write_receipt(output, "grade-edges.bin", grade_edges)
    files["lower_nodes"] = write_receipt(output, "lower-nodes.bin", lower_nodes_raw)
    files["lower_edges"] = write_receipt(output, "lower-edges.bin", lower_edges)
    files["lower_origins"] = write_receipt(output, "lower-origins.bin", lower_origins)
    files["lower_stored"] = write_receipt(output, "lower-stored.bin", lower_stored)
    files["lower_companions"] = write_receipt(
        output, "lower-companions.bin", lower_companions
    )
    files["grade_origins"] = write_receipt(output, "grade-origins.bin", grade_origins)
    files["old_lower_zero"] = write_receipt(
        output, "old-lower-zero.bin", old_lower_zero
    )
    grade_bits = bitset(grade_selected)
    lower_bits = bitset(lower_selected)
    files["selected_grade"] = write_receipt(output, "selected-grade.bits", grade_bits)
    files["selected_lower"] = write_receipt(output, "selected-lower.bits", lower_bits)

    del (
        lower_origins,
        lower_stored,
        lower_companions,
        grade_origins,
        old_lower_zero,
        grade_bits,
        lower_bits,
        grade_nodes,
        lower_nodes,
        source_descriptors,
        lower,
        grade,
        context,
        basis_blob,
        basis_view,
        remainder_blob,
        candidate_remainder,
        residual_raw,
        residual,
        remainder,
    )
    gc.collect()
    phase(
        "packed-physical-temporaries-released",
        grade_nodes=grade_count,
        lower_nodes=lower_count,
        grade_edges=len(grade_edge_view),
        lower_edges=len(lower_edge_view),
    )

    source_nodes: dict[str, dict] = {}
    defect_nodes: dict[str, dict] = {}
    expressions: dict[str, dict] = {}
    selected_ref_map: dict[int, dict] = {}

    def add_old_closure(character: int, roots) -> None:
        record = prepare["old_blocks"][character]["record"]
        todo = [int(value) for value in roots]
        while todo:
            pivot = todo.pop()
            key = f"old:{character}:{pivot}"
            if key in source_nodes:
                continue
            node = record["dag_nodes"][pivot]
            origin = node["origin"]
            children = []
            if origin["kind"] == "actor":
                parent = int(origin["parent"])
                children.append(f"old:{character}:{parent}")
                todo.append(parent)
            for earlier, _ in node["reductions"]:
                earlier = int(earlier)
                children.append(f"old:{character}:{earlier}")
                todo.append(earlier)
            source_nodes[key] = {
                "key": key,
                "kind": "old",
                "character": character,
                "pivot": pivot,
                "node": node,
                "children": children,
                "expression_key": None,
                "syntax": {
                    "origin": origin,
                    "reductions": [
                        {"pivot": int(q), "coefficient": int(c)}
                        for q, c in node["reductions"]
                    ],
                    "scale": int(node["scale"]),
                },
            }

    def add_defect(source_block: int, origin_index: int) -> str:
        key = f"defect:{origin_index}"
        if key in defect_nodes:
            return key
        origin = prepare["defect_origins"][origin_index]
        character = int(origin["lower_character"])
        record = prepare["old_blocks"][character]["record"]
        if origin["kind"] == "seed":
            seed = int(origin["seed"])
            expression = record["seed_reductions"][seed - 1]
            expression_key = f"seed:{character}:{seed}"
            expressions[expression_key] = {
                "key": expression_key,
                "kind": "seed_reduction",
                "character": character,
                "seed": seed,
                "expression": expression,
            }
            old_roots = [int(q) for q, _ in expression]
        elif origin["kind"] == "transition":
            pivot = int(origin["pivot"])
            letter = int(origin["letter"])
            expression = record["actor_transitions"][pivot][v3.ACTORS.index(letter)]
            expression_key = f"actor:{character}:{pivot}:{letter}"
            expressions[expression_key] = {
                "key": expression_key,
                "kind": "actor_transition_expression",
                "character": character,
                "pivot": pivot,
                "letter": letter,
                "expression": expression,
            }
            old_roots = [pivot] + [int(q) for q, _ in expression]
        else:
            fail("ancestry_defect_origin")
        children = []
        if origin["kind"] == "transition":
            children.append(f"old:{character}:{int(origin['pivot'])}")
        children.extend(f"old:{character}:{int(q)}" for q, _ in expression)
        defect_nodes[key] = {
            "key": key,
            "kind": "defect",
            "source_block": source_block,
            "origin": origin,
            "children": children,
            "expression_key": expression_key,
        }
        add_old_closure(character, old_roots)
        return key

    selected_blocks = {index: [] for index in range(4)}
    for logical_index, kind, character, pivot in selected_descriptors:
        if kind == 0:
            selected_ref_map[int(logical_index)] = make_old_ref(
                prepare, int(logical_index), int(character), int(pivot)
            )
            add_old_closure(int(character), [int(pivot)])
        else:
            selected_blocks[int(character)].append((int(logical_index), int(pivot)))

    for block_index in range(4):
        roots = selected_blocks[block_index]
        if not roots:
            continue
        body, digest = v3.read_sealed_state(
            args.state, f"block-{block_index}", prepare_digest
        )
        if digest != block_digests[block_index]:
            fail("source_block_parent")
        v3.validate_block_state(
            args.state,
            body,
            prepare,
            prepare_digest,
            block_index,
            authenticate_basis=False,
        )
        for logical_index, pivot in roots:
            node = body["dag_nodes"][pivot]
            selected_ref_map[logical_index] = {
                "logical": logical_index,
                "kind": "block",
                "block": block_index,
                "pivot": pivot,
                "block_dag_node": node,
                "ancestry_key": f"block:{block_index}:{pivot}",
            }
        todo = [pivot for _, pivot in roots]
        while todo:
            pivot = todo.pop()
            key = f"block:{block_index}:{pivot}"
            if key in source_nodes:
                continue
            node = body["dag_nodes"][pivot]
            origin = node["origin"]
            children = []
            if origin["kind"] == "actor":
                parent = int(origin["parent"])
                children.append(f"block:{block_index}:{parent}")
                todo.append(parent)
            elif origin["kind"] == "defect":
                children.append(add_defect(block_index, int(origin["origin"])))
            else:
                fail("ancestry_block_origin")
            for earlier, _ in node["reductions"]:
                earlier = int(earlier)
                children.append(f"block:{block_index}:{earlier}")
                todo.append(earlier)
            source_nodes[key] = {
                "key": key,
                "kind": "block",
                "character": block_index,
                "pivot": pivot,
                "node": node,
                "children": children,
                "syntax": {
                    "origin": origin,
                    "reductions": [
                        {"pivot": int(q), "coefficient": int(c)}
                        for q, c in node["reductions"]
                    ],
                    "scale": int(node["scale"]),
                },
            }
        del body
        gc.collect()
        phase(
            "selected-source-block-copied-released",
            block=block_index,
            selected_roots=len(roots),
            source_nodes=len(source_nodes),
        )

    selected_refs = [selected_ref_map[key] for key in sorted(selected_ref_map)]
    if {int(ref["logical"]) for ref in selected_refs} != selected_origins:
        fail("selected_ref_closure")
    del selected_ref_map, selected_descriptors, selected_blocks, selected_origins

    words_path = ROOT / "scratchpad/a0_paper_words_v1.json"
    words_raw = words_path.read_bytes()
    words = json.loads(words_raw.decode("utf-8"))
    literal_dictionary = {
        "schema": "d972.r07.a0.literal-dictionary.v1",
        "source_file": "scratchpad/a0_paper_words_v1.json",
        "source_sha256": sha(words_raw),
        "relators_sha256": words.get("relators_sha256"),
        "relators": words["relators"],
        "pure_q1_words": {str(key): list(value) for key, value in v3.PURE_Q1_WORDS.items()},
        "literal_actor_words": {
            "x": [1],
            "x_inverse": [-1],
            "y": [2],
            "y_inverse": [-2],
        },
    }
    root_emissions = [
        {
            "kind": "grade",
            "ids": [int(pivot)],
            "prefix": [],
            "coefficient": int(coefficient),
        }
        for pivot, coefficient in coefficients
    ]
    structural = {
        "schema": "d972.r07.a0.selected-slp-structure.v2",
        "syntax_contract": ["origin", "ordered_signed_reductions", "scale_power"],
        "member_roots": [
            {"pivot": int(pivot), "coefficient": int(coefficient)}
            for pivot, coefficient in coefficients
        ],
        "grade_selected": [int(index) for index in np.flatnonzero(grade_selected)],
        "lower_selected": [int(index) for index in np.flatnonzero(lower_selected)],
        "source_nodes": [source_nodes[key] for key in sorted(source_nodes)],
        "defect_nodes": [defect_nodes[key] for key in sorted(defect_nodes)],
        "expressions": [expressions[key] for key in sorted(expressions)],
        "literal_dictionary": literal_dictionary,
    }
    leaf_metadata = {
        "file": "literal-leaves.bin",
        "schema": LEAF_SCHEMA,
        "quotient_specific_evaluation": True,
        "common_source_witness": False,
        "states_exported": False,
    }
    ancestry = {
        "schema": "d972.r07.a0.selected-ancestry.v3",
        "selected_refs": selected_refs,
        "roots": root_emissions,
        "structure": structural,
        "derived": {
            "schema": "d972.r07.a0.selected-literal-derived.v2",
            "leaf_receipt": leaf_metadata,
        },
    }
    refs_raw = canon(selected_refs)
    ancestry_raw = canon(ancestry)
    files["source_refs"] = write_receipt(output, "source-refs.json", refs_raw)
    files["source_ancestry"] = write_receipt(
        output, "source-ancestry.json", ancestry_raw
    )
    ancestry_digest = files["source_ancestry"]["sha256"]
    del ancestry, structural, refs_raw, ancestry_raw, words, words_raw
    gc.collect()

    refs_by_logical = {int(ref["logical"]): ref for ref in selected_refs}
    pending: dict[tuple, int] = {}
    leaf_map: dict[tuple[int, tuple[int, ...]], int] = {}
    processed = 0
    maximum_path = 0

    def prepend(prefix, suffix):
        return tuple(v3.floor.wm(tuple(prefix), tuple(suffix)))

    def push(kind: str, ids: tuple[int, ...], prefix, coefficient: int) -> None:
        nonlocal maximum_path
        coefficient %= 3
        if not coefficient:
            return
        prefix = tuple(int(value) for value in prefix)
        maximum_path = max(maximum_path, len(prefix))
        key = (kind,) + tuple(int(value) for value in ids) + (prefix,)
        value = (pending.get(key, 0) + coefficient) % 3
        if value:
            pending[key] = value
        else:
            pending.pop(key, None)

    def leaf(seed: int, word, coefficient: int) -> None:
        nonlocal maximum_path
        coefficient %= 3
        if not coefficient:
            return
        word = tuple(int(value) for value in word)
        maximum_path = max(maximum_path, len(word))
        key = (int(seed), word)
        value = (leaf_map.get(key, 0) + coefficient) % 3
        if value:
            leaf_map[key] = value
        else:
            leaf_map.pop(key, None)

    for pivot, coefficient in coefficients:
        push("grade", (int(pivot),), (), int(coefficient))

    while pending:
        state, coefficient = pending.popitem()
        kind = state[0]
        ids = tuple(int(value) for value in state[1:-1])
        prefix = tuple(state[-1])
        processed += 1
        if kind == "grade":
            pivot = ids[0]
            logical_index, scale, edge_start, edge_count, lower_start, lower_count = grade_node_view[pivot]
            ref = refs_by_logical[int(logical_index)]
            if ref["kind"] == "old":
                push(
                    "old",
                    (int(ref["character"]), int(ref["pivot"])),
                    prefix,
                    coefficient * int(scale),
                )
                for index in range(lower_start, lower_start + lower_count):
                    earlier, value = lower_edge_view[index]
                    push(
                        "lower",
                        (int(earlier),),
                        prefix,
                        -coefficient * int(scale) * int(value),
                    )
            elif ref["kind"] == "block":
                push(
                    "block",
                    (int(ref["block"]), int(ref["pivot"])),
                    prefix,
                    coefficient * int(scale),
                )
            else:
                fail("ancestry_grade_origin")
            for index in range(edge_start, edge_start + edge_count):
                earlier, value = grade_edge_view[index]
                push(
                    "grade",
                    (int(earlier),),
                    prefix,
                    -coefficient * int(scale) * int(value),
                )
        elif kind == "lower":
            pivot = ids[0]
            logical_index, scale, edge_start, edge_count, _, _ = lower_node_view[pivot]
            ref = refs_by_logical[int(logical_index)]
            push(
                "old",
                (int(ref["character"]), int(ref["pivot"])),
                prefix,
                coefficient * int(scale),
            )
            for index in range(edge_start, edge_start + edge_count):
                earlier, value = lower_edge_view[index]
                push(
                    "lower",
                    (int(earlier),),
                    prefix,
                    -coefficient * int(scale) * int(value),
                )
        elif kind == "block":
            character, pivot = ids
            node = source_nodes[f"block:{character}:{pivot}"]["node"]
            scale = int(node["scale"])
            origin = node["origin"]
            if origin["kind"] == "defect":
                label = v3.CHARACTER_LABELS[character]
                for parity, word in v3.PURE_Q1_WORDS.items():
                    push(
                        "defect",
                        (int(origin["origin"]),),
                        prepend(prefix, word),
                        coefficient * scale * v3.cv(label, parity[0], parity[1]),
                    )
            elif origin["kind"] == "actor":
                push(
                    "block",
                    (character, int(origin["parent"])),
                    prepend(prefix, (int(origin["letter"]),)),
                    coefficient * scale,
                )
            else:
                fail("ancestry_block_origin")
            for earlier, value in node["reductions"]:
                push(
                    "block",
                    (character, int(earlier)),
                    prefix,
                    -coefficient * scale * int(value),
                )
        elif kind == "defect":
            item = defect_nodes[f"defect:{ids[0]}"]
            origin = item["origin"]
            character = int(origin["lower_character"])
            expression = expressions[item["expression_key"]]["expression"]
            if origin["kind"] == "seed":
                seed = int(origin["seed"])
                label = v3.CHARACTER_LABELS[character]
                for parity, word in v3.PURE_Q1_WORDS.items():
                    leaf(
                        seed,
                        prepend(prefix, word),
                        coefficient * v3.cv(label, parity[0], parity[1]),
                    )
            elif origin["kind"] == "transition":
                push(
                    "old",
                    (character, int(origin["pivot"])),
                    prepend(prefix, (int(origin["letter"]),)),
                    coefficient,
                )
            else:
                fail("ancestry_defect_origin")
            for earlier, value in expression:
                push(
                    "old",
                    (character, int(earlier)),
                    prefix,
                    -coefficient * int(value),
                )
        elif kind == "old":
            character, pivot = ids
            node = source_nodes[f"old:{character}:{pivot}"]["node"]
            scale = int(node["scale"])
            origin = node["origin"]
            if origin["kind"] == "projected_seed":
                seed = int(origin["seed"])
                label = v3.CHARACTER_LABELS[character]
                for parity, word in v3.PURE_Q1_WORDS.items():
                    leaf(
                        seed,
                        prepend(prefix, word),
                        coefficient
                        * scale
                        * v3.cv(label, parity[0], parity[1]),
                    )
            elif origin["kind"] == "actor":
                push(
                    "old",
                    (character, int(origin["parent"])),
                    prepend(prefix, (int(origin["letter"]),)),
                    coefficient * scale,
                )
            else:
                fail("ancestry_old_origin")
            for earlier, value in node["reductions"]:
                push(
                    "old",
                    (character, int(earlier)),
                    prefix,
                    -coefficient * scale * int(value),
                )
        else:
            fail("ancestry_kind")
        if processed % 65536 == 0:
            guard(started)
            phase(
                "adjoint-progress",
                processed=processed,
                pending=len(pending),
                leaves=len(leaf_map),
                maximum_path_length=maximum_path,
            )

    files["literal_leaves"] = write_leaf_receipt(
        output, leaf_metadata["file"], leaf_map, ancestry_digest
    )
    leaf_count = len(leaf_map)
    del leaf_map, pending
    gc.collect()
    phase(
        "canonical-graph-leaf-sealed",
        processed=processed,
        leaves=leaf_count,
        source_nodes=len(source_nodes),
        defect_nodes=len(defect_nodes),
        maximum_path_length=maximum_path,
    )

    roots = {
        "C_T": {
            "type": "OrderedProduct",
            "children": [
                {
                    "type": "GradeNodeRef",
                    "pivot": int(pivot),
                    "coefficient": int(coefficient),
                }
                for pivot, coefficient in coefficients
            ],
        },
        "C_<1": {
            "type": "RegisteredPriorProduct",
            "terms": prepare.get("canonical_solution", {}).get("terms", []),
        },
        "C_1": {"type": "Compose", "left": "C_<1", "right": "C_T"},
        "direct_occurrence_replay": False,
        "next_degree2_residual": None,
        "cross_checked": False,
        "verified": False,
        "A0": False,
        "COMMON": False,
        "FAKE": False,
        "IHARA": False,
    }
    files["roots"] = write_receipt(output, "roots.json", canon(roots))
    durable = sum(int(receipt["bytes"]) for receipt in files.values())
    if durable > 7 * 1024**3:
        fail("UNKNOWN_RESOURCE:durable_cap")
    manifest = {
        "schema": "d972.r07.a0.grade1-selected-slp.v1",
        "marker": MARKER,
        "decision_sha256": BODY_SHA,
        "prepare_sha256": prepare_digest,
        "block_sha256": block_digests,
        "cursor": logical,
        "lower_offer_count": lower_offers,
        "lower_rank": lower_count,
        "grade_offer_count": grade_offers,
        "grade_rank": grade_count,
        "coefficient_count": len(coefficients),
        "files": files,
        "roots": "roots.json",
        "direct_occurrence_replay": False,
        "next_degree2_residual": None,
        "cross_checked": False,
        "verified": False,
        "A0": False,
        "COMMON": False,
        "FAKE": False,
        "IHARA": False,
        "elapsed_seconds": time.monotonic() - started,
    }
    (output / "manifest.json").write_bytes(canon(manifest))
    phase(
        "payload-sealed",
        cursor=logical,
        lower_rank=lower_count,
        grade_rank=grade_count,
        coefficients=len(coefficients),
        payload_bytes=durable,
    )
    print(
        json.dumps(
            {
                "marker": MARKER,
                "cursor": logical,
                "lower_rank": lower_count,
                "grade_rank": grade_count,
                "coefficient_count": len(coefficients),
            },
            sort_keys=True,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    try:
        return execute(args)
    except MemoryError:
        emergency_unknown_resource()
        return 2
    except Exception as exc:
        print(json.dumps({"status": "NOT_READY", "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
