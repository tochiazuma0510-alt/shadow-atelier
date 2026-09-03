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
V475_PATH = ROOT / "sol/proof_r07_selected_slp_staged_adjoint_repair_v475.md"
V475_SHA = "757ffab5aa011643efa3df4b133dc03d423895d57a003ed6830a47528388148e"
V475_BYTES = 8253
BODY_SHA = "62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d"
BASIS_SHA = "b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d"
MARKER = "R07_GRADE1_SELECTED_SLP_V2_CANDIDATE"
NODE = struct.Struct("<IBQIQI")
EDGE = struct.Struct("<HB")
LEAF_MAGIC = b"R07LEAF1"
LEAF_VERSION = 1
LEAF_SCHEMA = "d972.r07.a0.literal-leaves.v1"
LEAF_HEADER = struct.Struct("<8sBBBB32sQ")
LEAF_RECORD = struct.Struct("<IIBI")
EMERGENCY_BYTES = 64 * 1024
DEFAULT_ACCUMULATED_CAP = 2_000_000
DEFAULT_PATH_CAP = 2_000_000
DEFAULT_PATH_LENGTH_CAP = 4096

if hashlib.sha256(V3_PATH.read_bytes()).hexdigest() != V3_SHA:
    raise RuntimeError("v3_hash_preimport")
if (
    V475_PATH.stat().st_size != V475_BYTES
    or hashlib.sha256(V475_PATH.read_bytes()).hexdigest() != V475_SHA
):
    raise RuntimeError("v475_hash_preimport")
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


class UnknownResource(RuntimeError):
    pass


def resource_fail(reason: str) -> None:
    raise UnknownResource("UNKNOWN_RESOURCE:" + reason)


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


def phase(name: str, **cursors: int | str) -> dict:
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
    return record


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
        resource_fail("time")
    if peak_rss() > int(os.environ.get("TASK601_MAX_RSS", str(7 * 1024**3))):
        resource_fail("rss")


def staging_path(final_output: Path) -> Path:
    return final_output.parent / ("." + final_output.name + f".task625-{os.getpid()}")


def discard_staging(final_output: Path | None) -> None:
    if final_output is None:
        return
    staging = staging_path(final_output)
    if not staging.is_dir():
        return
    try:
        for child in staging.iterdir():
            if child.is_file():
                child.unlink()
            else:
                return
        staging.rmdir()
    except OSError:
        pass


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


def staged_caps() -> dict[str, int | float]:
    return {
        "accumulated_states": int(
            os.environ.get("TASK625_ACCUMULATED_CAP", str(DEFAULT_ACCUMULATED_CAP))
        ),
        "interned_paths": int(
            os.environ.get("TASK625_PATH_CAP", str(DEFAULT_PATH_CAP))
        ),
        "path_length": int(
            os.environ.get("TASK625_PATH_LENGTH_CAP", str(DEFAULT_PATH_LENGTH_CAP))
        ),
        "durable_bytes": int(
            os.environ.get("TASK625_DURABLE_CAP", str(7 * 1024**3))
        ),
        "seconds": float(os.environ.get("TASK601_SECONDS", "2400")),
        "rss_bytes": int(
            os.environ.get("TASK601_MAX_RSS", str(7 * 1024**3))
        ),
    }


def inclusive_durable_total(receipt_bytes: int, manifest_raw: bytes, cap: int) -> int:
    if (
        type(receipt_bytes) is not int
        or receipt_bytes < 0
        or type(manifest_raw) is not bytes
        or type(cap) is not int
        or cap < 1
    ):
        fail("durable_accounting")
    total = receipt_bytes + len(manifest_raw)
    if total > cap:
        resource_fail("durable_cap")
    return total


def staged_adjoint(
    stages,
    roots,
    edges_for,
    multiply,
    caps: dict,
    *,
    started_at: float | None = None,
    now=time.monotonic,
    reporter=None,
    durable_bytes: int = 0,
):
    """Accumulate exact paths once at each node in a checked topological order."""
    required_caps = {
        "accumulated_states",
        "interned_paths",
        "path_length",
        "durable_bytes",
        "seconds",
        "rss_bytes",
    }
    if (
        set(caps) != required_caps
        or any(caps[key] < 1 for key in required_caps - {"seconds"})
        or not isinstance(caps["seconds"], (int, float))
        or float(caps["seconds"]) <= 0
    ):
        fail("staged_caps")
    if started_at is None:
        started_at = now()
    if type(durable_bytes) is not int or durable_bytes < 0:
        fail("staged_durable_bytes")
    if durable_bytes > int(caps["durable_bytes"]):
        resource_fail("staged_durable_cap")

    ordered = []
    stage_ranges = []
    for stage_name, nodes in stages:
        nodes = tuple(nodes)
        begin = len(ordered)
        ordered.extend(nodes)
        stage_ranges.append((str(stage_name), begin, len(ordered)))
    if len(ordered) != len(set(ordered)):
        fail("staged_duplicate_node")
    positions = {node: index for index, node in enumerate(ordered)}

    def check_clock_rss() -> None:
        if now() - started_at > float(caps["seconds"]):
            resource_fail("staged_time_cap")
        if peak_rss() > int(caps["rss_bytes"]):
            resource_fail("staged_rss_cap")

    def exact_word(value) -> tuple[int, ...]:
        if type(value) is tuple and all(type(letter) is int for letter in value):
            word = value
        else:
            word = tuple(int(letter) for letter in value)
        if len(word) > int(caps["path_length"]):
            resource_fail("staged_path_length_cap")
        for index, letter in enumerate(word):
            if letter not in (-2, -1, 1, 2):
                fail("staged_path_letter")
            if index and word[index - 1] == -letter:
                fail("staged_path_not_reduced")
        return word

    def checked_edge(source, edge, source_index: int):
        if not isinstance(edge, tuple) or len(edge) != 7:
            fail("staged_edge_shape")
        target, seed, scalar, suffix, relation, source_pivot, target_pivot = edge
        scalar = int(scalar) % 3
        if scalar not in (1, 2):
            fail("staged_edge_scalar")
        suffix = exact_word(suffix)
        if relation == "reduction":
            if not (
                isinstance(source_pivot, int)
                and isinstance(target_pivot, int)
                and target_pivot < source_pivot
            ):
                fail("staged_reduction_not_earlier")
        elif relation == "actor":
            if not (
                isinstance(source_pivot, int)
                and isinstance(target_pivot, int)
                and target_pivot < source_pivot
            ):
                fail("staged_actor_parent_not_earlier")
        elif relation not in ("link", "literal"):
            fail("staged_edge_relation")
        if target is None:
            if relation != "literal" or not isinstance(seed, int) or seed <= 0:
                fail("staged_leaf_edge")
        else:
            if seed is not None or target not in positions:
                fail("staged_missing_node")
            if positions[target] <= source_index:
                fail("staged_processed_destination")
        return target, seed, scalar, suffix

    # Validate every authenticated edge before any coefficient expansion.
    for source_index, source in enumerate(ordered):
        for edge in edges_for(source):
            checked_edge(source, edge, source_index)
        if source_index % 1024 == 0:
            check_clock_rss()

    paths = [()]
    path_ids = {(): 0}
    accumulators = {}
    leaves = {}
    live_node_entries = 0
    state_insertions = 0
    incoming_contributions = 0
    state_edge_traversals = 0
    cancellations = 0
    expanded_states = 0
    maximum_live_entries = 0
    maximum_path_length = 0
    current_index = -1
    stage_peak_live = 0

    def touch_live() -> None:
        nonlocal maximum_live_entries, stage_peak_live
        live = live_node_entries + len(leaves)
        maximum_live_entries = max(maximum_live_entries, live)
        stage_peak_live = max(stage_peak_live, live)
        if live > int(caps["accumulated_states"]):
            resource_fail("staged_state_cap")

    def intern(value) -> int:
        nonlocal maximum_path_length
        word = exact_word(value)
        maximum_path_length = max(maximum_path_length, len(word))
        known = path_ids.get(word)
        if known is not None:
            return known
        if len(paths) >= int(caps["interned_paths"]):
            resource_fail("staged_path_cap")
        identifier = len(paths)
        paths.append(word)
        path_ids[word] = identifier
        return identifier

    def add_node(target, path_id: int, coefficient: int) -> None:
        nonlocal live_node_entries, state_insertions, incoming_contributions
        nonlocal cancellations
        coefficient %= 3
        if not coefficient:
            return
        target_index = positions.get(target)
        if target_index is None:
            fail("staged_missing_node")
        if target_index <= current_index:
            fail("staged_processed_destination")
        incoming_contributions += 1
        bucket = accumulators.get(target)
        if bucket is None:
            bucket = {}
            accumulators[target] = bucket
        value = (bucket.get(path_id, 0) + coefficient) % 3
        if value:
            if path_id not in bucket:
                live_node_entries += 1
                state_insertions += 1
                if state_insertions > int(caps["accumulated_states"]):
                    resource_fail("staged_state_cap")
            bucket[path_id] = value
        elif path_id in bucket:
            del bucket[path_id]
            live_node_entries -= 1
            cancellations += 1
            if not bucket:
                del accumulators[target]
        touch_live()

    def add_leaf(seed: int, path_id: int, coefficient: int) -> None:
        nonlocal state_insertions, incoming_contributions, cancellations
        coefficient %= 3
        if not coefficient:
            return
        incoming_contributions += 1
        key = (int(seed), paths[path_id])
        value = (leaves.get(key, 0) + coefficient) % 3
        if value:
            if key not in leaves:
                state_insertions += 1
                if state_insertions > int(caps["accumulated_states"]):
                    resource_fail("staged_state_cap")
            leaves[key] = value
        elif key in leaves:
            del leaves[key]
            cancellations += 1
        touch_live()

    for target, path, coefficient in roots:
        add_node(target, intern(path), int(coefficient))

    stage_statistics = []
    processed_nodes = 0
    nonzero_nodes = 0
    first_stage = True
    for stage_name, begin, end in stage_ranges:
        before_insertions = 0 if first_stage else state_insertions
        before_contributions = 0 if first_stage else incoming_contributions
        before_cancellations = 0 if first_stage else cancellations
        before_expanded = expanded_states
        before_traversals = state_edge_traversals
        first_stage = False
        stage_peak_live = live_node_entries + len(leaves)
        stage_nonzero_nodes = 0
        for current_index in range(begin, end):
            node = ordered[current_index]
            bucket = accumulators.pop(node, None)
            processed_nodes += 1
            if not bucket:
                continue
            stage_nonzero_nodes += 1
            nonzero_nodes += 1
            live_node_entries -= len(bucket)
            touch_live()
            outgoing_edges = tuple(
                checked_edge(node, edge, current_index) for edge in edges_for(node)
            )
            for path_id, coefficient in bucket.items():
                expanded_states += 1
                for target, seed, scalar, suffix in outgoing_edges:
                    state_edge_traversals += 1
                    next_path = (
                        intern(multiply(paths[path_id], suffix))
                        if suffix
                        else path_id
                    )
                    outgoing = coefficient * scalar
                    if target is None:
                        add_leaf(seed, next_path, outgoing)
                    else:
                        add_node(target, next_path, outgoing)
                if expanded_states % 65536 == 0:
                    check_clock_rss()
            del outgoing_edges
            del bucket
        check_clock_rss()
        observed = {
            "elapsed_seconds": round(now() - started_at, 6),
            "rss_bytes": current_rss(),
            "peak_rss_bytes": peak_rss(),
            "durable_bytes": durable_bytes,
        }
        stage_record = {
            "stage": stage_name,
            "processed_nodes": end - begin,
            "nonzero_nodes": stage_nonzero_nodes,
            "accumulated_states": state_insertions - before_insertions,
            "incoming_contributions": incoming_contributions
            - before_contributions,
            "cancelled_states": cancellations - before_cancellations,
            "expanded_states": expanded_states - before_expanded,
            "state_edge_traversals": state_edge_traversals - before_traversals,
            "interned_paths": len(paths),
            "maximum_live_entries": stage_peak_live,
            "maximum_path_length": maximum_path_length,
            "leaf_count": len(leaves),
            "observation": observed,
        }
        stage_statistics.append(stage_record)
        if reporter is not None:
            reporter(stage_record)

    if accumulators:
        fail("staged_unprocessed_accumulator")
    leaf_stage = {
        "stage": "leaves",
        "processed_nodes": 0,
        "nonzero_nodes": 0,
        "accumulated_states": 0,
        "incoming_contributions": 0,
        "cancelled_states": 0,
        "expanded_states": 0,
        "state_edge_traversals": 0,
        "interned_paths": len(paths),
        "maximum_live_entries": len(leaves),
        "maximum_path_length": maximum_path_length,
        "leaf_count": len(leaves),
        "observation": {
            "elapsed_seconds": round(now() - started_at, 6),
            "rss_bytes": current_rss(),
            "peak_rss_bytes": peak_rss(),
            "durable_bytes": durable_bytes,
        },
    }
    stage_statistics.append(leaf_stage)
    if reporter is not None:
        reporter(leaf_stage)
    check_clock_rss()
    final_observation = {
        "elapsed_seconds": round(now() - started_at, 6),
        "rss_bytes": current_rss(),
        "peak_rss_bytes": peak_rss(),
        "durable_bytes": durable_bytes,
    }
    statistics = {
        "schema": "d972.r07.a0.staged-adjoint-statistics.v2",
        "schedule": [name for name, _, _ in stage_ranges] + ["leaves"],
        "caps": dict(caps),
        "stages": stage_statistics,
        "totals": {
            "processed_nodes": processed_nodes,
            "nonzero_nodes": nonzero_nodes,
            "accumulated_states": state_insertions,
            "incoming_contributions": incoming_contributions,
            "cancelled_states": cancellations,
            "expanded_states": expanded_states,
            "state_edge_traversals": state_edge_traversals,
            "interned_paths": len(paths),
            "maximum_live_entries": maximum_live_entries,
            "maximum_path_length": maximum_path_length,
            "leaf_count": len(leaves),
            "observation": final_observation,
        },
    }
    return leaves, statistics


def staged_scheduler_selftest() -> dict:
    def multiply(left, right):
        output = list(left)
        for letter in right:
            if output and output[-1] == -letter:
                output.pop()
            else:
                output.append(letter)
        return tuple(output)

    base_caps = {
        "accumulated_states": 100,
        "interned_paths": 100,
        "path_length": 20,
        "durable_bytes": 1_000_000,
        "seconds": 60.0,
        "rss_bytes": 2**63 - 1,
    }
    reducer_product = v3.floor.wm((1,), (-1, 2))
    if type(reducer_product) is not list or reducer_product != [2]:
        fail("fixture_v3_reducer_list")

    def run(
        stages,
        roots,
        graph,
        caps=None,
        *,
        clock=None,
        started_at=None,
        durable_bytes=0,
        provider_calls=None,
        multiplier=None,
    ):
        def provider(node):
            if provider_calls is not None:
                provider_calls[node] = provider_calls.get(node, 0) + 1
            return iter(graph.get(node, ()))

        return staged_adjoint(
            stages,
            roots,
            provider,
            multiply if multiplier is None else multiplier,
            dict(base_caps if caps is None else caps),
            started_at=started_at,
            now=time.monotonic if clock is None else clock,
            durable_bytes=durable_bytes,
        )

    leaf = lambda seed=1, coefficient=1, word=(): (
        None,
        seed,
        coefficient,
        tuple(word),
        "literal",
        None,
        None,
    )
    link = lambda target, coefficient=1, word=(): (
        target,
        None,
        coefficient,
        tuple(word),
        "link",
        None,
        None,
    )
    actor_link = lambda target, source_pivot, target_pivot, word: (
        target,
        None,
        1,
        tuple(word),
        "actor",
        source_pivot,
        target_pivot,
    )

    diamond_graph = {
        "a": (link("m", 1),),
        "b": (link("m", 2),),
        "m": (leaf(),),
    }
    cancelled, cancelled_stats = run(
        (("roots", ("a", "b")), ("merge", ("m",))),
        (("a", (), 1), ("b", (), 1)),
        diamond_graph,
    )
    if cancelled or cancelled_stats["totals"]["cancelled_states"] != 1:
        fail("fixture_staged_diamond_cancel")

    third_graph = dict(diamond_graph)
    third_graph["c"] = (link("m", 1),)
    third, third_stats = run(
        (("roots", ("a", "b", "c")), ("merge", ("m",))),
        (("a", (), 1), ("b", (), 1), ("c", (), 1)),
        third_graph,
    )
    if third != {(1, ()): 1}:
        fail("fixture_staged_diamond_third")

    captured_products = []

    def capture_product(left, right):
        product = multiply(left, right)
        captured_products.append(product)
        return product

    actor, actor_stats = run(
        (("actor", ("a",)), ("terminal", ("m",))),
        (("a", (1,), 1),),
        {"a": (actor_link("m", 1, 0, (-1, 2)),), "m": (leaf(),)},
        multiplier=capture_product,
    )
    if (
        actor != {(1, (2,)): 1}
        or len(captured_products) != 1
        or next(iter(actor))[1] is not captured_products[0]
    ):
        fail("fixture_staged_actor_cancellation")

    raw_path = [1, 2]
    raw_leaf, _ = run(
        (("raw", ("a",)),),
        (("a", raw_path, 1),),
        {"a": (leaf(),)},
    )
    raw_leaf_path = next(iter(raw_leaf))[1]
    if type(raw_leaf_path) is not tuple or raw_leaf_path != (1, 2):
        fail("fixture_staged_raw_path_canonicalization")
    for bad_path, expected in (
        ((1, -1), "staged_path_not_reduced"),
        ((3,), "staged_path_letter"),
    ):
        try:
            run((("raw", ("a",)),), (("a", bad_path, 1),), {})
        except RuntimeError as exc:
            if str(exc) != expected:
                raise
        else:
            fail("fixture_staged_raw_path_gate")

    coefficient_two, coefficient_stats = run(
        (("coefficient", ("a",)),),
        (("a", (), 2),),
        {"a": (leaf(),)},
    )
    if coefficient_two != {(1, ()): 2}:
        fail("fixture_staged_coefficient_two")

    provider_calls = {}
    distinct, distinct_stats = run(
        (("roots", ("a", "b")), ("merge", ("m",))),
        (("a", (), 1), ("b", (), 1)),
        {
            "a": (link("m", word=(1,)),),
            "b": (link("m", word=(2,)),),
            "m": (leaf(),),
        },
        provider_calls=provider_calls,
    )
    toy_endpoint = lambda word: len(word) & 1
    if (
        toy_endpoint((1,)) != toy_endpoint((2,))
        or distinct != {(1, (1,)): 1, (1, (2,)): 1}
        or distinct_stats["totals"]["state_edge_traversals"] != 4
        or provider_calls.get("m") != 2
    ):
        fail("fixture_staged_exact_words")

    bad_cases = (
        (
            "staged_reduction_not_earlier",
            (("bad", ("a", "b")),),
            {"a": (("b", None, 1, (), "reduction", 0, 0),)},
        ),
        (
            "staged_actor_parent_not_earlier",
            (("bad", ("a", "b")),),
            {"a": (("b", None, 1, (1,), "actor", 0, 0),)},
        ),
        (
            "staged_processed_destination",
            (("cycle", ("a", "b")),),
            {"a": (link("b"),), "b": (link("a"),)},
        ),
    )
    for expected, stages, graph in bad_cases:
        try:
            run(stages, (("a", (), 1),), graph)
        except RuntimeError as exc:
            if str(exc) != expected:
                raise
        else:
            fail("fixture_staged_bad_edge_not_rejected")

    resource_cases = []
    state_caps = dict(base_caps, accumulated_states=1)
    resource_cases.append(
        ((("roots", ("a", "b")),), (("a", (), 1), ("b", (), 1)), {}, state_caps)
    )
    path_caps = dict(base_caps, interned_paths=1)
    resource_cases.append(
        ((("path", ("a",)),), (("a", (1,), 1),), {}, path_caps)
    )
    length_caps = dict(base_caps, path_length=1)
    resource_cases.append(
        ((("path", ("a",)),), (("a", (1, 2), 1),), {}, length_caps)
    )
    time_caps = dict(base_caps, seconds=0.5)
    resource_cases.append(((("time", ("a",)),), (("a", (), 1),), {}, time_caps))
    resource_cases[-1] = resource_cases[-1] + (lambda: 1.0, 0.0)
    durable_caps = dict(base_caps, durable_bytes=1)
    resource_cases.append(
        ((("durable", ("a",)),), (("a", (), 1),), {}, durable_caps, None, None, 2)
    )
    for case in resource_cases:
        stages, roots, graph, caps, *clock_values = case
        try:
            run(
                stages,
                roots,
                graph,
                caps,
                clock=clock_values[0] if clock_values else None,
                started_at=clock_values[1] if clock_values else None,
                durable_bytes=clock_values[2] if len(clock_values) > 2 else 0,
            )
        except UnknownResource as exc:
            if not str(exc).startswith("UNKNOWN_RESOURCE:"):
                raise
        else:
            fail("fixture_staged_resource_cap_not_rejected")

    if inclusive_durable_total(9, b"x", 10) != 10:
        fail("fixture_manifest_inclusive_total")
    try:
        inclusive_durable_total(10, b"x", 10)
    except UnknownResource as exc:
        if str(exc) != "UNKNOWN_RESOURCE:durable_cap":
            raise
    else:
        fail("fixture_manifest_byte_cap")

    source = Path(__file__).read_text(encoding="utf-8")
    scheduler_source = source[
        source.index("\ndef staged_adjoint(") : source.index(
            "\ndef staged_scheduler_selftest()"
        )
    ]
    if "leaf_map = {" in scheduler_source or "for (seed, path_id)" in scheduler_source:
        fail("fixture_terminal_leaf_clone")

    positive_stats = (
        cancelled_stats,
        third_stats,
        actor_stats,
        coefficient_stats,
        distinct_stats,
    )
    return {
        "fixtures": 9,
        "positive_expanded_states": sum(
            item["totals"]["expanded_states"] for item in positive_stats
        ),
        "positive_maximum_live_entries": max(
            item["totals"]["maximum_live_entries"] for item in positive_stats
        ),
        "positive_state_edge_traversals": sum(
            item["totals"]["state_edge_traversals"] for item in positive_stats
        ),
        "resource_caps_rejected": len(resource_cases),
        "two_path_provider_calls": provider_calls["m"],
        "canonical_tuple_reuse": "PASS",
        "raw_word_gates": "PASS",
        "terminal_leaf_clone_absent": "PASS",
        "manifest_inclusive_cap": "PASS",
        "v3_reducer_list_to_interner": "PASS",
    }


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
        scheduler_fixture = staged_scheduler_selftest()
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
                    "staged_scheduler": scheduler_fixture,
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
    if V475_PATH.stat().st_size != V475_BYTES or sha(V475_PATH.read_bytes()) != V475_SHA:
        fail("v475_hash")

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

    final_output = args.out
    if final_output.exists():
        fail("output_must_not_exist")
    output = staging_path(final_output)
    if output.exists():
        fail("staging_exists")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir()
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
    block_pivots = {character: [] for character in range(4)}
    old_pivots = {character: [] for character in range(4)}
    for item in source_nodes.values():
        if item["kind"] == "block":
            block_pivots[int(item["character"])].append(int(item["pivot"]))
        elif item["kind"] == "old":
            old_pivots[int(item["character"])].append(int(item["pivot"]))
        else:
            fail("staged_source_kind")
    defect_origins = sorted(
        int(key.split(":", 1)[1]) for key in defect_nodes
    )
    stages = [
        (
            "physical-grade",
            tuple(
                ("grade", int(pivot))
                for pivot in reversed(np.flatnonzero(grade_selected).tolist())
            ),
        ),
        (
            "physical-lower",
            tuple(
                ("lower", int(pivot))
                for pivot in reversed(np.flatnonzero(lower_selected).tolist())
            ),
        ),
    ]
    stages.extend(
        (
            f"block-{character}",
            tuple(
                ("block", character, pivot)
                for pivot in sorted(block_pivots[character], reverse=True)
            ),
        )
        for character in range(4)
    )
    stages.append(
        ("defect", tuple(("defect", origin) for origin in defect_origins))
    )
    stages.extend(
        (
            f"old-{character}",
            tuple(
                ("old", character, pivot)
                for pivot in sorted(old_pivots[character], reverse=True)
            ),
        )
        for character in range(4)
    )

    def node_edge(
        target,
        coefficient: int,
        word=(),
        relation="link",
        source_pivot=None,
        target_pivot=None,
    ):
        return (
            target,
            None,
            int(coefficient),
            tuple(int(letter) for letter in word),
            relation,
            source_pivot,
            target_pivot,
        )

    def literal_edge(seed: int, coefficient: int, word=()):
        return (
            None,
            int(seed),
            int(coefficient),
            tuple(int(letter) for letter in word),
            "literal",
            None,
            None,
        )

    def staged_edges(identifier):
        kind = identifier[0]
        if kind == "grade":
            pivot = int(identifier[1])
            logical_index, scale, edge_start, edge_count, lower_start, lower_count = grade_node_view[pivot]
            ref = refs_by_logical.get(int(logical_index))
            if ref is None:
                fail("staged_missing_physical_origin")
            if ref["kind"] == "old":
                yield node_edge(
                    ("old", int(ref["character"]), int(ref["pivot"])),
                    int(scale),
                )
                for index in range(lower_start, lower_start + lower_count):
                    earlier, value = lower_edge_view[index]
                    yield node_edge(
                        ("lower", int(earlier)), -int(scale) * int(value)
                    )
            elif ref["kind"] == "block":
                yield node_edge(
                    ("block", int(ref["block"]), int(ref["pivot"])),
                    int(scale),
                )
            else:
                fail("staged_grade_origin")
            for index in range(edge_start, edge_start + edge_count):
                earlier, value = grade_edge_view[index]
                yield node_edge(
                    ("grade", int(earlier)),
                    -int(scale) * int(value),
                    relation="reduction",
                    source_pivot=pivot,
                    target_pivot=int(earlier),
                )
        elif kind == "lower":
            pivot = int(identifier[1])
            logical_index, scale, edge_start, edge_count, _, _ = lower_node_view[pivot]
            ref = refs_by_logical.get(int(logical_index))
            if ref is None or ref.get("kind") != "old":
                fail("staged_lower_origin")
            yield node_edge(
                ("old", int(ref["character"]), int(ref["pivot"])), int(scale)
            )
            for index in range(edge_start, edge_start + edge_count):
                earlier, value = lower_edge_view[index]
                yield node_edge(
                    ("lower", int(earlier)),
                    -int(scale) * int(value),
                    relation="reduction",
                    source_pivot=pivot,
                    target_pivot=int(earlier),
                )
        elif kind == "block":
            character, pivot = int(identifier[1]), int(identifier[2])
            item = source_nodes.get(f"block:{character}:{pivot}")
            if item is None:
                fail("staged_missing_block")
            node = item["node"]
            scale = int(node["scale"])
            origin = node["origin"]
            if origin["kind"] == "defect":
                label = v3.CHARACTER_LABELS[character]
                for parity, word in v3.PURE_Q1_WORDS.items():
                    yield node_edge(
                        ("defect", int(origin["origin"])),
                        scale * v3.cv(label, parity[0], parity[1]),
                        word,
                    )
            elif origin["kind"] == "actor":
                parent = int(origin["parent"])
                yield node_edge(
                    ("block", character, parent),
                    scale,
                    (int(origin["letter"]),),
                    relation="actor",
                    source_pivot=pivot,
                    target_pivot=parent,
                )
            else:
                fail("staged_block_origin")
            for earlier, value in node["reductions"]:
                yield node_edge(
                    ("block", character, int(earlier)),
                    -scale * int(value),
                    relation="reduction",
                    source_pivot=pivot,
                    target_pivot=int(earlier),
                )
        elif kind == "defect":
            origin_index = int(identifier[1])
            item = defect_nodes.get(f"defect:{origin_index}")
            if item is None:
                fail("staged_missing_defect")
            origin = item["origin"]
            character = int(origin["lower_character"])
            expression_item = expressions.get(item["expression_key"])
            if expression_item is None:
                fail("staged_missing_expression")
            expression = expression_item["expression"]
            if origin["kind"] == "seed":
                label = v3.CHARACTER_LABELS[character]
                for parity, word in v3.PURE_Q1_WORDS.items():
                    yield literal_edge(
                        int(origin["seed"]),
                        v3.cv(label, parity[0], parity[1]),
                        word,
                    )
            elif origin["kind"] == "transition":
                yield node_edge(
                    ("old", character, int(origin["pivot"])),
                    1,
                    (int(origin["letter"]),),
                )
            else:
                fail("staged_defect_origin")
            for earlier, value in expression:
                yield node_edge(
                    ("old", character, int(earlier)), -int(value)
                )
        elif kind == "old":
            character, pivot = int(identifier[1]), int(identifier[2])
            item = source_nodes.get(f"old:{character}:{pivot}")
            if item is None:
                fail("staged_missing_old")
            node = item["node"]
            scale = int(node["scale"])
            origin = node["origin"]
            if origin["kind"] == "projected_seed":
                label = v3.CHARACTER_LABELS[character]
                for parity, word in v3.PURE_Q1_WORDS.items():
                    yield literal_edge(
                        int(origin["seed"]),
                        scale * v3.cv(label, parity[0], parity[1]),
                        word,
                    )
            elif origin["kind"] == "actor":
                parent = int(origin["parent"])
                yield node_edge(
                    ("old", character, parent),
                    scale,
                    (int(origin["letter"]),),
                    relation="actor",
                    source_pivot=pivot,
                    target_pivot=parent,
                )
            else:
                fail("staged_old_origin")
            for earlier, value in node["reductions"]:
                yield node_edge(
                    ("old", character, int(earlier)),
                    -scale * int(value),
                    relation="reduction",
                    source_pivot=pivot,
                    target_pivot=int(earlier),
                )
        else:
            fail("staged_node_kind")

    def staged_report(record: dict) -> None:
        phase(
            "staged-adjoint-stage-complete",
            stage=record["stage"],
            processed_nodes=record["processed_nodes"],
            accumulated_states=record["accumulated_states"],
            expanded_states=record["expanded_states"],
            state_edge_traversals=record["state_edge_traversals"],
            interned_paths=record["interned_paths"],
            maximum_live_entries=record["maximum_live_entries"],
            maximum_path_length=record["maximum_path_length"],
            leaves=record["leaf_count"],
            durable_bytes=record["observation"]["durable_bytes"],
        )

    scheduler_limits = staged_caps()
    leaf_map, scheduler_statistics = staged_adjoint(
        stages,
        tuple(
            (("grade", int(pivot)), (), int(coefficient))
            for pivot, coefficient in coefficients
        ),
        staged_edges,
        lambda left, right: v3.floor.wm(left, right),
        scheduler_limits,
        started_at=started,
        reporter=staged_report,
        durable_bytes=sum(int(receipt["bytes"]) for receipt in files.values()),
    )

    files["literal_leaves"] = write_leaf_receipt(
        output, leaf_metadata["file"], leaf_map, ancestry_digest
    )
    leaf_count = len(leaf_map)
    scheduler_totals = scheduler_statistics["totals"]
    del leaf_map
    gc.collect()
    phase(
        "canonical-graph-leaf-sealed",
        expanded_states=scheduler_totals["expanded_states"],
        interned_paths=scheduler_totals["interned_paths"],
        maximum_live_entries=scheduler_totals["maximum_live_entries"],
        leaves=leaf_count,
        source_nodes=len(source_nodes),
        defect_nodes=len(defect_nodes),
        maximum_path_length=scheduler_totals["maximum_path_length"],
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
    receipt_durable = sum(int(receipt["bytes"]) for receipt in files.values())
    manifest = {
        "schema": "d972.r07.a0.grade1-selected-slp.v2",
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
        "staged_theorem": {
            "file": "sol/proof_r07_selected_slp_staged_adjoint_repair_v475.md",
            "bytes": V475_BYTES,
            "sha256": V475_SHA,
        },
        "staged_adjoint": scheduler_statistics,
        "resource_caps": {
            "virtual_memory_bytes": 8 * 1024**3,
            "rss_bytes": int(scheduler_limits["rss_bytes"]),
            "durable_bytes": int(scheduler_limits["durable_bytes"]),
            "wall_seconds": float(scheduler_limits["seconds"]),
            "accumulated_states": int(scheduler_limits["accumulated_states"]),
            "interned_paths": int(scheduler_limits["interned_paths"]),
            "path_length": int(scheduler_limits["path_length"]),
        },
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
    manifest_raw = canon(manifest)
    durable = inclusive_durable_total(
        receipt_durable, manifest_raw, int(scheduler_limits["durable_bytes"])
    )
    (output / "manifest.json").write_bytes(manifest_raw)
    os.replace(output, final_output)
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
                "payload_bytes": durable,
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
    except UnknownResource as exc:
        discard_staging(args.out)
        try:
            os.write(2, (str(exc) + "\n").encode("ascii", "replace")[:1024])
        except BaseException:
            pass
        return 2
    except MemoryError:
        emergency_unknown_resource()
        discard_staging(args.out)
        return 2
    except Exception as exc:
        discard_staging(args.out)
        print(json.dumps({"status": "NOT_READY", "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
