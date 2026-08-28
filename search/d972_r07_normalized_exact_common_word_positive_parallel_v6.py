#!/usr/bin/env python3
"""Task325 positive-only persistent process adapter for cached-v3.

The authenticated cached-v3 search remains the sole mathematical owner.  This
module registers one replacement for BoundaryDescriptorCache.correlation and
otherwise delegates the production schedule and COMMON construction unchanged.
"""
from __future__ import annotations

import argparse
import bisect
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import multiprocessing
import multiprocessing.connection
import os
import pickle
import struct
import sys
import tempfile
import time
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-normalized-exact-common-word-positive-parallel/v6"
SELFTEST_SCHEMA = SCHEMA + "/selftest"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint-state"
FIXTURE_SCHEMA = SCHEMA + "/fixture/v6"
COMMON = "R07_NORMALIZED_EXACT_COMMON_WORD_POSITIVE_PARALLEL_V6_COMMON_WORD"
SELFTEST_PASS = "R07_NORMALIZED_EXACT_COMMON_WORD_POSITIVE_PARALLEL_V6_SELFTEST_PASS"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
PRODUCER_PREFIX = "R07_NORMALIZED_EXACT_COMMON_WORD_POSITIVE_PARALLEL_V6_PRODUCER_TERMINAL"
V3_COMMON = "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD"
V3_SCHEMA = "d972-r07-normalized-exact-cached-colgen/v3"
PAIR_ORDER = "descriptor_order_then_typed_support_insertion_order/v3"
WINNER_ORDER = "(block,translation_blob,relator_index)/v3"
F3_ENCODING = "canonical_nonzero_1_or_2"
HOOK_NAME = "boundary_descriptor_cache_correlation_positive_parallel_v6"
FIXTURE = (
    "search/certs/"
    "d972_r07_normalized_exact_common_word_positive_parallel_selftest_v6_20260828.json"
)
CHECKPOINT_ZIP = (
    "ci/in/"
    "d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip"
)
CHECKPOINT_MANIFEST = (
    "ci/in/"
    "d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json"
)
CHECKPOINT_MEMBER = (
    "d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json"
)
RAW_CHECKPOINT_BYTES = 86_368_039
RAW_CHECKPOINT_SHA256 = (
    "c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab"
)
WORKER_COUNTS = (2, 4)
PROGRESS_GRANULARITY = 4096
STARTUP_SECONDS = 20.0
SHUTDOWN_SECONDS = 2.0
MAX_SUPPORT_BYTES = 1_048_576
MAX_FRAME_BYTES = 33_554_432
MAX_EPOCH_SERIALIZATION_BYTES = 268_435_456


# Every task325 input is an authenticated, immutable dependency.  The current
# producer is intentionally absent: recursive self-pinning is impossible.
SOURCE_PINS = {
    "commission_v6": (
        "sol/luna_task_325_r07_task192_positive_only_persistent_parallel_v6.md",
        10172,
        "b22813ff9aa5250af25412db34f98b6e40996115a874e895b497e3a8753e4bf8",
    ),
    "positive_only_v140": (
        "sol/proof_r07_positive_only_common_word_colgen_v140.md",
        10073,
        "6d388a74c75d55d215b0035496c451aa9de5bbc7a8248c277e76021092b8562b",
    ),
    "history_free_v265": (
        "sol/proof_r07_history_free_positive_common_word_verifier_v265.md",
        10122,
        "fd30ccb2458691ec7844d304f220a4be7d704259318c452f928f8088552ecb0a",
    ),
    "resume_semantics_v253": (
        "sol/audit_r07_task192_boundary_resume_semantics_v253.md",
        4110,
        "a1d9f6d3d8cb31d8b261dd5cb1977865abfeba24bfc6aae7436d2a893e3ef19a",
    ),
    "mapreduce_v254": (
        "sol/proof_r07_frozen_dual_boundary_mapreduce_v254.md",
        6195,
        "e9fc7a69525200e8e1c0e8152652229227877ba923378ade8afa199c4f4ee1a0",
    ),
    "adapter_state_v255": (
        "sol/proof_r07_boundary_adapter_state_and_local_provenance_v255.md",
        8814,
        "06c93c46b48b681e0316d302058b72bc0b76fe9d12888cde3f7e45dc3a93ffa0",
    ),
    "counters_v256": (
        "sol/audit_r07_task192_cumulative_pairs_and_persistent_pool_v256.md",
        4790,
        "f5a0c6e625e5113e4213b62762267fc9a5437cafd9f9751e603b055c549c1251",
    ),
    "task319_audit": (
        "sol/sol_reply_319_r07_task311_persistent_parallel_code_performance_audit.md",
        20604,
        "9b9908eadf0f8c8204f9397d2af0511ba98959a979a00058c7b28cae9c74f981",
    ),
    "task321_commission": (
        "sol/luna_task_321_r07_task192_persistent_parallel_adapter_v5_rewrite.md",
        9128,
        "681b7a1a4b8edcd6f788f8d01aca930d60f3e61330293e70a4db47df205d2cc9",
    ),
    "task321_reply": (
        "sol/luna_reply_321_r07_task192_persistent_parallel_adapter_v5.md",
        12122,
        "bd8104b462f35979af2fd2ee820ad08a1c1c165cac6e2558a8e4eba6e7946c8b",
    ),
    "task303_producer": (
        "search/d972_r07_normalized_exact_common_word_parallel_v5.py",
        39234,
        "19a2970fcf072c25c606d0305fd999c8481353e0be20879de4be2aa26f6fb90c",
    ),
    "task303_checker": (
        "crosscheck/check_d972_r07_normalized_exact_common_word_parallel_v5.py",
        32486,
        "530d67c854017a538fa2185b8bc5c48834a785f5bd6db38452db3551695cf1df",
    ),
    "task303_driver": (
        "search/d972_r07_normalized_exact_common_word_parallel_gha_driver_v5.g",
        7971,
        "0ac1b26d1844fdc16cc2701c536f50fd5415a7ef2479e030ebde96af79af4902",
    ),
    "task303_fixture": (
        "search/certs/d972_r07_normalized_exact_common_word_parallel_selftest_v5_20260828.json",
        1195,
        "4d481ba84e3c452c79f344e66a0eea5322ec8b64c15a81f1a290c22ce18e3fc9",
    ),
    "cached_v3_producer": (
        "search/d972_r07_normalized_exact_common_word_cached_v3.py",
        193704,
        "f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37",
    ),
    "cached_v3_checker": (
        "crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py",
        154009,
        "dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10",
    ),
    "cached_v3_driver": (
        "search/d972_r07_normalized_exact_common_word_cached_gha_driver_v3.g",
        11548,
        "2f7ff7b459e46d014268907ff5ba5f03c035836e8f8df79a2c5f4cdc3b75351d",
    ),
    "cached_v3_fixture": (
        "search/certs/d972_r07_normalized_exact_common_word_cached_selftest_v3_20260827.json",
        276,
        "c49f434ad3daf1cc661ba45563dbb9557d436f91dca78c8ee0f47ed70332da12",
    ),
    "task298_driver": (
        "search/d972_r07_normalized_exact_common_word_cached_resume_gha_driver_v2.g",
        19682,
        "169da7aa149d68907abb435f380b9ec2994c2bc285c6a17f13431614a388f5ad",
    ),
    "task298_reply": (
        "sol/luna_reply_298_r07_task192_checkpoint_resume_transport_v2.md",
        9200,
        "732c9b1d279e9201d4cce3b432b5a4805a60d346d6104865246ce0a3030af22f",
    ),
    "checkpoint_zip": (
        CHECKPOINT_ZIP,
        5_001_811,
        "f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566",
    ),
    "checkpoint_manifest": (
        CHECKPOINT_MANIFEST,
        1328,
        "6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302",
    ),
    "selftest_fixture_v6": (
        FIXTURE,
        4102,
        "a6ade562478f86fcd986f119f4d349949c7a866332999acb1d9605a039fcb8ad",
    ),
}

FALSE_CLAIMS = {
    "common_word": False,
    "separator": False,
    "negative": False,
    "finite_common_word": False,
    "cofinal_lift": False,
    "fake": False,
    "ihara_witness": False,
}
POSITIVE_CLAIMS = {
    **FALSE_CLAIMS,
    "common_word": True,
    "finite_common_word": True,
}


class InputStop(RuntimeError):
    pass


class ProtocolError(RuntimeError):
    pass


class ParallelResource(RuntimeError):
    def __init__(self, phase, cap, value, limit, reason):
        super().__init__(reason)
        self.phase = str(phase)
        self.cap = str(cap)
        self.value = value
        self.limit = limit
        self.reason = str(reason)


class SelftestReject(RuntimeError):
    def __init__(self, stage, reason):
        super().__init__(stage + ":" + reason)
        self.stage = stage
        self.reason = reason


def require(condition, message):
    if not condition:
        raise ProtocolError(message)


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def digest_obj(value):
    return digest_bytes(canonical(value))


def public_pins():
    return {
        label: {"path": path, "bytes": size, "sha256": sha}
        for label, (path, size, sha) in SOURCE_PINS.items()
    }


def source_pins_digest():
    return digest_obj(public_pins())


def authenticate_sources():
    for label, (relative, expected_bytes, expected_sha) in SOURCE_PINS.items():
        path = ROOT / relative
        if not path.is_file():
            raise InputStop("source_missing:" + label)
        raw = path.read_bytes()
        if len(raw) != expected_bytes or digest_bytes(raw) != expected_sha:
            raise InputStop("source_pin:" + label)
    return public_pins()


def _seal_outer(value):
    answer = copy.deepcopy(value)
    answer.pop("self_digest_sha256", None)
    answer["self_digest_sha256"] = digest_obj(answer)
    return answer


def _seal_v3(value):
    answer = copy.deepcopy(value)
    answer.pop("self_digest", None)
    answer["self_digest"] = digest_obj(answer)
    return answer


def _fresh_relative(path_value, suffix=None):
    path = Path(path_value)
    if path.is_absolute() or ".." in path.parts:
        raise InputStop("output_path")
    normalized = path.as_posix()
    if not normalized.startswith("ci/out/"):
        raise InputStop("output_boundary")
    if suffix is not None and not normalized.endswith(suffix):
        raise InputStop("output_suffix")
    target = ROOT / path
    if target.exists():
        raise InputStop("stale_output")
    return target


def _write_exclusive(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)


def _jsonable(value):
    if isinstance(value, bytes):
        return {"bytes_hex": value.hex()}
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    return value


def _key_public(key):
    return [int(key[0]), int(key[1]), bytes(key[2]).hex()]


def _key_private(value):
    require(isinstance(value, list) and len(value) == 3, "key shape")
    return (int(value[0]), int(value[1]), bytes.fromhex(str(value[2])))


def _winner_key(key):
    return (int(key[0]), bytes(key[2]), int(key[1]))


def _sparse_public(accumulator):
    return [
        [_key_public(key), int(accumulator[key])]
        for key in sorted(accumulator, key=_winner_key)
        if int(accumulator[key]) % 3
    ]


def _sparse_private(value):
    answer = {}
    require(isinstance(value, list), "sparse accumulator shape")
    for item in value:
        require(isinstance(item, list) and len(item) == 2, "sparse item")
        key = _key_private(item[0])
        coefficient = int(item[1])
        require(coefficient in (1, 2) and key not in answer, "sparse canonical")
        answer[key] = coefficient
    require(_sparse_public(answer) == value, "sparse order")
    return answer


def _f3_add(target, source):
    for key, value in source.items():
        coefficient = (target.get(key, 0) + int(value)) % 3
        if coefficient:
            target[key] = coefficient
        else:
            target.pop(key, None)


def _descriptor_public(descriptor):
    return {
        "block": int(descriptor[0]),
        "relator_index": int(descriptor[1]),
        "component": int(descriptor[2]),
        "h_hex": bytes(descriptor[3]).hex(),
        "base_coefficient": int(descriptor[6]) % 3,
    }


def _roster_public(roster):
    return [_descriptor_public(item) for item in roster["descriptors"]]


def _roster_digest(roster):
    return digest_obj(_roster_public(roster))


def _roster_mul(roster, block, left, right):
    if roster["kind"] == "c17":
        return (int(left) + int(right)) % 17
    return roster["groups"][int(block)].mul(left, right)


def _roster_blob(roster, block, element):
    if roster["kind"] == "c17":
        value = int(element)
        require(0 <= value < 17, "C17 element range")
        return bytes((value,))
    return roster["v1"].element_blob(roster["runtime"], element)


def _roster_unpack(roster, block, raw):
    if roster["kind"] == "c17":
        require(type(raw) is bytes and len(raw) == 1 and raw[0] < 17,
                "C17 canonical byte")
        return raw[0]
    return roster["v1"].unpack_element(roster["runtime"], raw, int(block))


def _encode_support(support):
    records = list(support)
    out = bytearray(struct.pack(">I", len(records)))
    public = []
    seen = set()
    for position, item in enumerate(records):
        require(isinstance(item, (tuple, list)) and len(item) == 4,
                "support record")
        block, component, raw, coefficient = item
        block = int(block)
        component = int(component)
        coefficient = int(coefficient)
        raw = bytes(raw)
        require(0 < block < 65536 and 0 <= component < 65536,
                "support type range")
        require(coefficient in (1, 2) and len(raw) < 2 ** 32,
                "support coefficient/blob")
        identity = (block, component, raw)
        require(identity not in seen, "duplicate typed support element")
        seen.add(identity)
        out.extend(struct.pack(">HHBI", block, component, coefficient, len(raw)))
        out.extend(raw)
        public.append([block, component, raw.hex(), coefficient])
    return bytes(out), public


def _decode_support(roster, raw):
    require(type(raw) is bytes and len(raw) >= 4, "support buffer")
    count = struct.unpack_from(">I", raw, 0)[0]
    offset = 4
    records = []
    typed = {}
    lookup = {}
    seen = set()
    for position in range(count):
        require(offset + 9 <= len(raw), "support header truncation")
        block, component, coefficient, size = struct.unpack_from(
            ">HHBI", raw, offset
        )
        offset += 9
        require(offset + size <= len(raw), "support blob truncation")
        blob = raw[offset:offset + size]
        offset += size
        require(coefficient in (1, 2), "support F3")
        identity = (block, component, blob)
        require(identity not in seen, "support duplicate")
        seen.add(identity)
        element = _roster_unpack(roster, block, blob)
        record = (block, component, blob, coefficient, element, position)
        records.append(record)
        typed.setdefault((block, component), []).append(record)
        lookup.setdefault((block, component), {})[blob] = record
    require(offset == len(raw), "support trailing bytes")
    return records, typed, lookup


def _prefix_offsets(roster, typed):
    offsets = [0]
    for descriptor in roster["descriptors"]:
        offsets.append(
            offsets[-1] + len(typed.get((descriptor[0], descriptor[2]), ()))
        )
    return offsets


def _intervals(total, worker_count):
    require(type(total) is int and total >= 0, "pair total")
    require(type(worker_count) is int and worker_count > 0, "worker count")
    active = min(total, worker_count)
    if not active:
        return []
    return [
        [worker * total // active, (worker + 1) * total // active]
        for worker in range(active)
    ]


def _current_rss(pid=None):
    target = os.getpid() if pid is None else int(pid)
    path = Path("/proc") / str(target) / "status"
    try:
        for line in path.read_text(encoding="ascii").splitlines():
            if line.startswith("VmRSS:"):
                fields = line.split()
                return int(fields[1]) * 1024
    except (OSError, UnicodeError, ValueError, IndexError):
        return 0
    return 0


def _send_frame(connection, value):
    raw = pickle.dumps(value, protocol=5)
    require(len(raw) <= MAX_FRAME_BYTES, "bounded worker frame")
    connection.send_bytes(raw)
    return len(raw)


def _recv_frame(connection):
    raw = connection.recv_bytes()
    return pickle.loads(raw), len(raw)


def _worker_result_digest(value):
    body = {key: copy.deepcopy(item) for key, item in value.items()
            if key != "result_digest"}
    return digest_obj(_jsonable(body))


def _worker_interval(roster, typed, offsets, start, stop, cancel,
                     progress, fault, attempted_update):
    if fault == "death":
        os._exit(73)
    if fault == "timeout":
        cancel.wait(60.0)
        return {}, None, None, 0, False
    effective_stop = stop
    if fault == "partial" and stop > start:
        effective_stop = start + max(1, (stop - start) // 2)
    accumulator = {}
    first_by_key = {}
    attempted = 0
    descriptors = roster["descriptors"]
    descriptor_index = max(0, bisect.bisect_right(offsets, start) - 1)
    while descriptor_index < len(descriptors) and offsets[descriptor_index] < effective_stop:
        descriptor = descriptors[descriptor_index]
        block, relator, component, h_blob, h, h_inverse, base = descriptor
        support = typed.get((block, component), ())
        pair_start = offsets[descriptor_index]
        left = max(start, pair_start)
        right = min(effective_stop, offsets[descriptor_index + 1])
        for pair_index in range(left, right):
            if cancel.is_set():
                return accumulator, None, None, attempted, False
            support_item = support[pair_index - pair_start]
            g_blob, coefficient, g = support_item[2], support_item[3], support_item[4]
            translation = _roster_mul(roster, block, g, h_inverse)
            require(_roster_mul(roster, block, translation, h) == g,
                    "worker left translation gate")
            translation_blob = _roster_blob(roster, block, translation)
            key = (block, relator, translation_blob)
            contribution = (int(base) * int(coefficient)) % 3
            combined = (accumulator.get(key, 0) + contribution) % 3
            if combined:
                accumulator[key] = combined
            else:
                accumulator.pop(key, None)
            first_by_key.setdefault(key, {
                "pair_index": pair_index,
                "component": component,
                "g_hex": g_blob.hex(),
                "h_hex": h_blob.hex(),
                "lambda_coefficient": coefficient,
                "base_coefficient": base,
            })
            attempted += 1
            attempted_update(attempted)
            if attempted % PROGRESS_GRANULARITY == 0:
                progress(attempted)
        descriptor_index += 1
    winner = min(accumulator, key=_winner_key) if accumulator else None
    provenance = None if winner is None else first_by_key[winner]
    complete = effective_stop == stop and not cancel.is_set()
    return accumulator, winner, provenance, attempted, complete


def _worker_main(worker_id, connection, roster, cancel, attempted_shared):
    try:
        ready = {
            "kind": "ready",
            "worker_id": worker_id,
            "pid": os.getpid(),
            "descriptor_digest": _roster_digest(roster),
            "rss_bytes": _current_rss(),
        }
        _send_frame(connection, ready)
        while True:
            request, _ = _recv_frame(connection)
            if request.get("kind") == "shutdown":
                _send_frame(connection, {
                    "kind": "bye", "worker_id": worker_id,
                    "pid": os.getpid(), "rss_bytes": _current_rss(),
                })
                return
            require(request.get("kind") == "epoch", "worker request kind")
            support_raw = request["support"]
            require(digest_bytes(support_raw) == request["support_digest"],
                    "worker support digest")
            _, typed, _ = _decode_support(roster, support_raw)
            offsets = _prefix_offsets(roster, typed)
            require(digest_obj(offsets) == request["prefix_digest"] and
                    offsets[-1] == request["total_pairs"],
                    "worker prefix identity")
            require(request["descriptor_digest"] == _roster_digest(roster),
                    "worker descriptor identity")
            start, stop = request["interval"]
            sent_progress = 0

            def progress(attempted):
                nonlocal sent_progress
                frame = {
                    "kind": "progress", "worker_id": worker_id,
                    "epoch_id": request["epoch_id"],
                    "dual_digest": request["dual_digest"],
                    "interval": [start, stop], "attempted": attempted,
                    "rss_bytes": _current_rss(),
                }
                sent_progress += _send_frame(connection, frame)

            accumulator, local_winner, local_provenance, attempted, complete = \
                _worker_interval(
                    roster, typed, offsets, start, stop, cancel, progress,
                    request.get("fault"),
                    lambda value: attempted_shared.__setitem__(worker_id, value),
                )
            body = {
                "kind": "result", "worker_id": worker_id,
                "epoch_id": request["epoch_id"],
                "dual_digest": request["dual_digest"],
                "descriptor_digest": request["descriptor_digest"],
                "support_digest": request["support_digest"],
                "prefix_digest": request["prefix_digest"],
                "interval": [start, stop],
                "attempted": attempted,
                "complete": complete,
                "accumulator": _sparse_public(accumulator),
                "local_winner": None if local_winner is None else
                    _key_public(local_winner),
                "local_provenance": local_provenance,
                "rss_bytes": _current_rss(),
                "progress_serialization_bytes": sent_progress,
            }
            body["result_digest"] = _worker_result_digest(body)
            _send_frame(connection, body)
    except (EOFError, BrokenPipeError, OSError):
        return
    except BaseException as error:
        try:
            _send_frame(connection, {
                "kind": "error", "worker_id": worker_id,
                "error_type": type(error).__name__, "error": str(error),
                "rss_bytes": _current_rss(),
            })
        except BaseException:
            pass
        return
    finally:
        try:
            connection.close()
        except OSError:
            pass


def _empty_counters():
    return {
        "historical_attempted_pairs": 0,
        "historical_committed_pairs": 0,
        "historical_discarded_pairs": 0,
        "historical_retried_pairs": 0,
        "attempted_pairs": 0,
        "committed_pairs": 0,
        "discarded_pairs": 0,
        "retried_pairs": 0,
        "historical_attempted_epochs": 0,
        "historical_committed_epochs": 0,
        "historical_discarded_epochs": 0,
        "historical_retried_epochs": 0,
        "attempted_epochs": 0,
        "committed_epochs": 0,
        "discarded_epochs": 0,
        "retried_epochs": 0,
        "retry_pending_pairs": 0,
    }


def _validate_counter_equations(counters):
    required = set(_empty_counters())
    require(isinstance(counters, dict) and set(counters) == required,
            "adapter counter fields")
    require(all(type(counters[key]) is int and counters[key] >= 0
                for key in required), "adapter nonnegative counters")
    require(counters["attempted_pairs"] ==
            counters["committed_pairs"] + counters["discarded_pairs"],
            "adapter pair counter conservation")
    require(counters["attempted_epochs"] ==
            counters["committed_epochs"] + counters["discarded_epochs"],
            "adapter epoch counter conservation")
    for stem in ("attempted", "committed", "discarded", "retried"):
        require(counters[stem + "_pairs"] >=
                counters["historical_" + stem + "_pairs"],
                "historical pair counter reset")
        require(counters[stem + "_epochs"] >=
                counters["historical_" + stem + "_epochs"],
                "historical epoch counter reset")
    require(counters["retried_pairs"] <= counters["attempted_pairs"] and
            counters["retried_epochs"] <= counters["attempted_epochs"],
            "retry counter bounds")


def _seed_counters(checkpoint):
    adapter = checkpoint.get("positive_parallel_v6")
    if isinstance(adapter, dict):
        require(adapter.get("schema") == CHECKPOINT_SCHEMA,
                "resume adapter checkpoint schema")
        require(adapter.get("source_pins_sha256") == source_pins_digest(),
                "resume adapter source pins")
        counters = copy.deepcopy(adapter.get("counters"))
        _validate_counter_equations(counters)
        return counters, copy.deepcopy(adapter.get("epoch_chain_sha256")), \
            copy.deepcopy(adapter.get("last_epoch"))
    monitor = checkpoint.get("monitor", {}).get("counters", {})
    progress = checkpoint.get("progress", {}).get("boundary", {})
    attempted_pairs = int(monitor.get("boundary_pairs", 0))
    committed_pairs = int(progress.get("pair_attempts", attempted_pairs))
    require(0 <= committed_pairs <= attempted_pairs,
            "checkpoint boundary counter order")
    discarded_pairs = attempted_pairs - committed_pairs
    columns = checkpoint.get("columns", [])
    require(isinstance(columns, list), "checkpoint columns")
    committed_epochs = sum(
        1 for record in columns
        if isinstance(record, dict) and record.get("active_dual") is not None
    )
    discarded_epochs = 1 if discarded_pairs else 0
    counters = _empty_counters()
    counters.update({
        "historical_attempted_pairs": attempted_pairs,
        "historical_committed_pairs": committed_pairs,
        "historical_discarded_pairs": discarded_pairs,
        "attempted_pairs": attempted_pairs,
        "committed_pairs": committed_pairs,
        "discarded_pairs": discarded_pairs,
        "historical_attempted_epochs": committed_epochs + discarded_epochs,
        "historical_committed_epochs": committed_epochs,
        "historical_discarded_epochs": discarded_epochs,
        "attempted_epochs": committed_epochs + discarded_epochs,
        "committed_epochs": committed_epochs,
        "discarded_epochs": discarded_epochs,
        "retry_pending_pairs": discarded_pairs,
    })
    _validate_counter_equations(counters)
    chain = digest_obj({
        "source": "authenticated_cached_v3_checkpoint",
        "checkpoint_self_digest": checkpoint.get("self_digest"),
        "counters": counters,
        "historical_replay_claim": False,
    })
    return counters, chain, None


class ProductionMeter:
    def __init__(self, monitor, v1):
        self.monitor = monitor
        self.v1 = v1

    def deadline_ns(self):
        limit = float(self.monitor.limits["wall_seconds"])
        return int((float(self.monitor.started) + limit) * 1_000_000_000)

    def charge_pairs(self, count):
        try:
            self.monitor.bump(
                "boundary_pairs", int(count), "positive_boundary_parallel_v6"
            )
        except self.v1.ResourceStop as error:
            raise ParallelResource(
                error.phase, error.cap, error.value, error.limit,
                "owner_monitor_pair_cap",
            ) from error

    def check(self, aggregate_rss):
        elapsed = time.monotonic() - float(self.monitor.started)
        wall_limit = float(self.monitor.limits["wall_seconds"])
        if elapsed > wall_limit:
            raise ParallelResource(
                "positive_boundary_parallel_v6", "wall_seconds", elapsed,
                wall_limit, "live_deadline",
            )
        rss_limit = int(self.monitor.limits["rss_bytes"])
        if aggregate_rss and aggregate_rss > rss_limit:
            raise ParallelResource(
                "positive_boundary_parallel_v6", "rss_bytes",
                aggregate_rss, rss_limit, "aggregate_parent_children_rss",
            )


class SelftestMeter:
    def __init__(self, seconds=5.0, rss_bytes=1 << 60):
        self.started = time.monotonic()
        self.seconds = float(seconds)
        self.rss_bytes = int(rss_bytes)
        self.charged_pairs = 0

    def deadline_ns(self):
        return int((self.started + self.seconds) * 1_000_000_000)

    def charge_pairs(self, count):
        self.charged_pairs += int(count)

    def check(self, aggregate_rss):
        elapsed = time.monotonic() - self.started
        if elapsed > self.seconds:
            raise ParallelResource(
                "selftest_parallel", "wall_seconds", elapsed, self.seconds,
                "live_deadline",
            )
        if aggregate_rss > self.rss_bytes:
            raise ParallelResource(
                "selftest_parallel", "rss_bytes", aggregate_rss,
                self.rss_bytes, "aggregate_parent_children_rss",
            )


class PersistentProcessRoster:
    """One immutable fork roster reused by serial fixed-dual epochs."""

    def __init__(self, roster, worker_count, counters=None,
                 epoch_chain_sha256=None, last_epoch=None):
        if sys.platform != "linux":
            raise InputStop("persistent_pool_requires_linux")
        if worker_count not in WORKER_COUNTS:
            raise InputStop("boundary_workers_must_be_2_or_4")
        context = multiprocessing.get_context("fork")
        if context.get_start_method() != "fork":
            raise InputStop("persistent_pool_requires_fork")
        self.roster = roster
        self.worker_count = int(worker_count)
        self.descriptor_digest = _roster_digest(roster)
        self.cancel = context.Event()
        self.attempted_shared = context.Array(
            "Q", self.worker_count, lock=False
        )
        self.connections = []
        self.processes = []
        self.cleanup_transitions = ["started"]
        self.cleanup_complete = False
        self.started_pids = []
        self.live_pids_after_join = None
        self.worker_exitcodes = []
        self._child_rss = {}
        self.serialization = {
            "sent_bytes": 0,
            "received_bytes": 0,
            "max_frame_bytes": 0,
            "max_epoch_inflight_bytes": 0,
            "support_bytes_last_epoch": 0,
            "support_cap_bytes": MAX_SUPPORT_BYTES,
            "frame_cap_bytes": MAX_FRAME_BYTES,
            "epoch_cap_bytes": MAX_EPOCH_SERIALIZATION_BYTES,
        }
        self.resource = {
            "parent_rss_peak_bytes": 0,
            "children_rss_peak_bytes": 0,
            "aggregate_rss_peak_bytes": 0,
            "rss_samples": 0,
            "worker_restarts": 0,
            "checkpoint_bytes": 0,
        }
        self.counters = copy.deepcopy(counters or _empty_counters())
        _validate_counter_equations(self.counters)
        self.epoch_chain_sha256 = (
            str(epoch_chain_sha256) if epoch_chain_sha256 else
            digest_obj({"schema": CHECKPOINT_SCHEMA, "genesis": True})
        )
        self.last_epoch = copy.deepcopy(last_epoch)
        self.epoch_records_retained = 0 if last_epoch is None else 1
        self._epoch_serial = int(self.counters["attempted_epochs"])
        try:
            for worker_id in range(self.worker_count):
                parent, child = context.Pipe(duplex=True)
                process = context.Process(
                    target=_worker_main,
                    args=(worker_id, child, roster, self.cancel,
                          self.attempted_shared),
                    name="r07-v6-boundary-%d" % worker_id,
                    daemon=True,
                )
                process.start()
                child.close()
                self.connections.append(parent)
                self.processes.append(process)
                self.started_pids.append(int(process.pid))
            self._await_ready()
        except BaseException:
            self._fail_cleanup()
            raise

    def _account_frame(self, size, sent):
        field = "sent_bytes" if sent else "received_bytes"
        self.serialization[field] += int(size)
        self.serialization["max_frame_bytes"] = max(
            self.serialization["max_frame_bytes"], int(size)
        )

    def _send(self, worker_id, value):
        size = _send_frame(self.connections[worker_id], value)
        self._account_frame(size, True)
        return size

    def _recv(self, worker_id):
        value, size = _recv_frame(self.connections[worker_id])
        self._account_frame(size, False)
        return value, size

    def _sample_rss(self, child_values=None):
        parent = _current_rss()
        if child_values is not None:
            self._child_rss.update(
                {int(key): int(value) for key, value in child_values.items()}
            )
        for worker_id, process in enumerate(self.processes):
            if process.is_alive() and not self._child_rss.get(worker_id):
                self._child_rss[worker_id] = _current_rss(process.pid)
            if not process.is_alive():
                self._child_rss[worker_id] = 0
        children = sum(self._child_rss.values())
        aggregate = parent + children
        self.resource["parent_rss_peak_bytes"] = max(
            self.resource["parent_rss_peak_bytes"], parent
        )
        self.resource["children_rss_peak_bytes"] = max(
            self.resource["children_rss_peak_bytes"], children
        )
        self.resource["aggregate_rss_peak_bytes"] = max(
            self.resource["aggregate_rss_peak_bytes"], aggregate
        )
        self.resource["rss_samples"] += 1
        return aggregate

    def _await_ready(self):
        pending = set(range(self.worker_count))
        deadline = time.monotonic() + STARTUP_SECONDS
        child_rss = {}
        while pending:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                self._fail_cleanup()
                raise InputStop("persistent_pool_startup_timeout")
            ready_connections = multiprocessing.connection.wait(
                [self.connections[index] for index in pending], timeout=remaining
            )
            if not ready_connections:
                self._fail_cleanup()
                raise InputStop("persistent_pool_startup_timeout")
            for connection in ready_connections:
                worker_id = self.connections.index(connection)
                try:
                    frame, _ = self._recv(worker_id)
                except (EOFError, OSError) as error:
                    self._fail_cleanup()
                    raise InputStop("persistent_pool_startup_death") from error
                require(frame.get("kind") == "ready" and
                        frame.get("worker_id") == worker_id and
                        frame.get("descriptor_digest") == self.descriptor_digest,
                        "persistent worker ready identity")
                child_rss[worker_id] = int(frame.get("rss_bytes", 0))
                pending.remove(worker_id)
        self._child_rss.update(child_rss)
        self._sample_rss(child_rss)

    def _record_epoch(self, record):
        compact = copy.deepcopy(record)
        compact["previous_epoch_chain_sha256"] = self.epoch_chain_sha256
        self.epoch_chain_sha256 = digest_obj(compact)
        compact["epoch_chain_sha256"] = self.epoch_chain_sha256
        self.last_epoch = compact
        self.epoch_records_retained = 1

    def _counter_attempt(self, attempted_pairs, committed, total_pairs,
                         retry_planned):
        attempted_pairs = int(attempted_pairs)
        self.counters["attempted_pairs"] += attempted_pairs
        self.counters["attempted_epochs"] += 1
        retried = min(attempted_pairs, int(retry_planned))
        if retried:
            self.counters["retried_pairs"] += retried
            self.counters["retried_epochs"] += 1
        if committed:
            require(attempted_pairs == int(total_pairs), "commit pair count")
            self.counters["committed_pairs"] += attempted_pairs
            self.counters["committed_epochs"] += 1
            self.counters["retry_pending_pairs"] = 0
        else:
            self.counters["discarded_pairs"] += attempted_pairs
            self.counters["discarded_epochs"] += 1
            self.counters["retry_pending_pairs"] = max(
                int(total_pairs), self.counters["retry_pending_pairs"]
            )
        _validate_counter_equations(self.counters)

    def _fail_cleanup(self):
        self.cancel.set()
        self.close(force=True)

    def close(self, force=False):
        if self.cleanup_complete:
            return
        if not self.cleanup_transitions or self.cleanup_transitions[-1] != "closing":
            self.cleanup_transitions.append("closing")
        if not force:
            for worker_id, process in enumerate(self.processes):
                if process.is_alive():
                    try:
                        self._send(worker_id, {"kind": "shutdown"})
                    except (BrokenPipeError, EOFError, OSError):
                        force = True
            deadline = time.monotonic() + SHUTDOWN_SECONDS
            pending = {index for index, process in enumerate(self.processes)
                       if process.is_alive()}
            while pending and not force:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    force = True
                    break
                available = multiprocessing.connection.wait(
                    [self.connections[index] for index in pending],
                    timeout=remaining,
                )
                if not available:
                    force = True
                    break
                for connection in available:
                    worker_id = self.connections.index(connection)
                    try:
                        frame, _ = self._recv(worker_id)
                        if frame.get("kind") != "bye":
                            force = True
                        pending.discard(worker_id)
                    except (EOFError, OSError):
                        pending.discard(worker_id)
        for process in self.processes:
            process.join(timeout=SHUTDOWN_SECONDS)
        if force or any(process.is_alive() for process in self.processes):
            self.cleanup_transitions.append("terminating")
            for process in self.processes:
                if process.is_alive():
                    process.terminate()
            for process in self.processes:
                process.join(timeout=SHUTDOWN_SECONDS)
        self.cleanup_transitions.append("joined")
        self.live_pids_after_join = [
            int(process.pid) for process in self.processes if process.is_alive()
        ]
        self.worker_exitcodes = [process.exitcode for process in self.processes]
        for connection in self.connections:
            try:
                connection.close()
            except OSError:
                pass
        self.cleanup_complete = not self.live_pids_after_join
        if not self.cleanup_complete:
            raise ProtocolError("worker survived terminate/join")

    def public_state(self):
        _validate_counter_equations(self.counters)
        return {
            "schema": CHECKPOINT_SCHEMA,
            "hook": HOOK_NAME,
            "owner": "cached-v3 BoundaryDescriptorCache.correlation",
            "source_pins_sha256": source_pins_digest(),
            "descriptor_digest": self.descriptor_digest,
            "descriptor_count": len(self.roster["descriptors"]),
            "worker_count": self.worker_count,
            "persistent_processes": True,
            "serial_dual_epochs": True,
            "atomic_full_epoch": True,
            "pair_order": PAIR_ORDER,
            "winner_order": WINNER_ORDER,
            "f3_encoding": F3_ENCODING,
            "historical_replay_claim": False,
            "counters": copy.deepcopy(self.counters),
            "serialization": copy.deepcopy(self.serialization),
            "resource": copy.deepcopy(self.resource),
            "epoch_chain_sha256": self.epoch_chain_sha256,
            "epoch_records_retained": self.epoch_records_retained,
            "last_epoch": copy.deepcopy(self.last_epoch),
            "cleanup": {
                "transitions": list(self.cleanup_transitions),
                "started_pids": list(self.started_pids),
                "live_pids_after_join": copy.deepcopy(self.live_pids_after_join),
                "worker_exitcodes": list(self.worker_exitcodes),
                "complete": self.cleanup_complete,
            },
        }

    def run_epoch(self, support, dual_digest, meter, fault=None,
                  epoch_context=None):
        if self.cleanup_complete:
            raise ProtocolError("epoch after pool cleanup")
        support_raw, support_public = _encode_support(support)
        decoded, typed, lookup = _decode_support(self.roster, support_raw)
        require(len(decoded) == len(support_public), "support decode count")
        offsets = _prefix_offsets(self.roster, typed)
        total_pairs = offsets[-1]
        intervals = _intervals(total_pairs, self.worker_count)
        support_digest = digest_bytes(support_raw)
        prefix_digest = digest_obj(offsets)
        self._epoch_serial += 1
        identity_body = {
            "serial_epoch": self._epoch_serial,
            "owner_epoch_context": copy.deepcopy(epoch_context or {}),
            "dual_digest": str(dual_digest),
            "descriptor_digest": self.descriptor_digest,
            "support_public_digest": digest_obj(support_public),
            "support_buffer_digest": support_digest,
            "typed_support_digests": {
                "%d:%d" % key: digest_obj([
                    [item[2].hex(), item[3], item[5]] for item in values
                ]) for key, values in sorted(typed.items())
            },
            "prefix_offsets": offsets,
            "prefix_digest": prefix_digest,
            "expanded_pair_count": total_pairs,
            "pair_order": PAIR_ORDER,
            "winner_order": WINNER_ORDER,
            "f3_encoding": F3_ENCODING,
        }
        epoch_id = digest_obj(identity_body)
        retry_planned = min(
            total_pairs, int(self.counters["retry_pending_pairs"])
        )
        if len(support_raw) > MAX_SUPPORT_BYTES:
            self._counter_attempt(0, False, total_pairs, retry_planned)
            self._record_epoch({
                **identity_body, "epoch_id": epoch_id,
                "status": "discarded", "reason": "support_serialization_cap",
                "intervals": intervals, "attempted_pairs": 0,
                "committed_pairs": 0,
            })
            self._fail_cleanup()
            raise ParallelResource(
                "positive_boundary_parallel_v6", "serialization_bytes",
                len(support_raw), MAX_SUPPORT_BYTES,
                "support_serialization_cap",
            )
        deadline_ns = meter.deadline_ns()
        if not intervals:
            try:
                meter.charge_pairs(0)
                meter.check(self._sample_rss())
            except ParallelResource as error:
                self._counter_attempt(0, False, 0, retry_planned)
                record = {
                    **identity_body, "epoch_id": epoch_id,
                    "status": "discarded", "reason": error.reason,
                    "intervals": [], "attempted_pairs": 0,
                    "committed_pairs": 0,
                }
                self._record_epoch(record)
                self._fail_cleanup()
                raise
            self._counter_attempt(0, True, 0, retry_planned)
            record = {
                **identity_body, "epoch_id": epoch_id,
                "status": "committed", "reason": None,
                "intervals": [], "attempted_pairs": 0,
                "committed_pairs": 0,
                "accumulator_digest": digest_obj([]),
                "selected_key": None,
            }
            self._record_epoch(record)
            return {
                "identity": identity_body, "epoch_id": epoch_id,
                "support": support_public, "support_raw": support_raw,
                "typed": typed, "lookup": lookup, "offsets": offsets,
                "intervals": [], "shards": [], "accumulator": {},
                "selected_key": None, "selected_scalar": 0,
                "pair_count": 0, "batch_complete": True,
            }
        self.cancel.clear()
        pending = set(range(len(intervals)))
        for worker_id in range(self.worker_count):
            self.attempted_shared[worker_id] = 0
        child_attempts = {worker_id: 0 for worker_id in pending}
        child_rss = {worker_id: 0 for worker_id in pending}
        shards = {}
        epoch_sent = 0
        epoch_received = 0
        charged_pairs = 0
        for worker_id, interval in enumerate(intervals):
            request = {
                "kind": "epoch", "worker_id": worker_id,
                "epoch_id": epoch_id, "dual_digest": str(dual_digest),
                "descriptor_digest": self.descriptor_digest,
                "support": support_raw, "support_digest": support_digest,
                "prefix_digest": prefix_digest, "total_pairs": total_pairs,
                "interval": interval, "deadline_ns": deadline_ns,
                "fault": fault if worker_id == 0 else None,
            }
            try:
                epoch_sent += self._send(worker_id, request)
            except (BrokenPipeError, EOFError, OSError) as error:
                self.cancel.set()
                self.close(force=True)
                exact_attempted = sum(
                    int(self.attempted_shared[index])
                    for index in range(self.worker_count)
                )
                charge_error = None
                try:
                    meter.charge_pairs(exact_attempted)
                except ParallelResource as resource_error:
                    charge_error = resource_error
                self._counter_attempt(
                    exact_attempted, False, total_pairs, retry_planned
                )
                self._record_epoch({
                    **identity_body, "epoch_id": epoch_id,
                    "status": "discarded",
                    "reason": (charge_error.reason if charge_error else
                               "worker_send_failure"),
                    "intervals": intervals,
                    "attempted_pairs": exact_attempted,
                    "committed_pairs": 0,
                })
                if charge_error is not None:
                    raise charge_error
                raise ParallelResource(
                    "positive_boundary_parallel_v6", "worker_channel", 1, 0,
                    "worker_send_failure",
                ) from error
        self.serialization["support_bytes_last_epoch"] = len(support_raw)
        self.serialization["max_epoch_inflight_bytes"] = max(
            self.serialization["max_epoch_inflight_bytes"], epoch_sent
        )
        require(epoch_sent <= MAX_EPOCH_SERIALIZATION_BYTES,
                "epoch request serialization cap")
        failure = None
        while pending and failure is None:
            remaining_ns = deadline_ns - time.monotonic_ns()
            if remaining_ns <= 0:
                failure = ParallelResource(
                    "positive_boundary_parallel_v6", "wall_seconds",
                    time.monotonic(), deadline_ns / 1_000_000_000,
                    "live_deadline",
                )
                break
            dead = [worker_id for worker_id in pending
                    if not self.processes[worker_id].is_alive()]
            if dead:
                failure = ParallelResource(
                    "positive_boundary_parallel_v6", "worker_death",
                    dead[0], -1, "worker_death",
                )
                break
            available = multiprocessing.connection.wait(
                [self.connections[index] for index in pending],
                timeout=remaining_ns / 1_000_000_000,
            )
            if not available:
                failure = ParallelResource(
                    "positive_boundary_parallel_v6", "wall_seconds",
                    time.monotonic(), deadline_ns / 1_000_000_000,
                    "live_deadline",
                )
                break
            for connection in available:
                worker_id = self.connections.index(connection)
                try:
                    frame, frame_bytes = self._recv(worker_id)
                    epoch_received += frame_bytes
                except (EOFError, OSError):
                    failure = ParallelResource(
                        "positive_boundary_parallel_v6", "worker_death",
                        worker_id, -1, "worker_death",
                    )
                    break
                if frame.get("kind") == "progress":
                    if frame.get("worker_id") != worker_id or \
                            frame.get("epoch_id") != epoch_id or \
                            frame.get("dual_digest") != str(dual_digest) or \
                            frame.get("interval") != intervals[worker_id]:
                        failure = ParallelResource(
                            "positive_boundary_parallel_v6", "worker_protocol",
                            worker_id, -1, "cross_epoch_progress",
                        )
                        break
                    attempted = int(frame.get("attempted", -1))
                    prior_attempted = child_attempts[worker_id]
                    if not (prior_attempted <= attempted <=
                            intervals[worker_id][1] - intervals[worker_id][0]):
                        failure = ParallelResource(
                            "positive_boundary_parallel_v6", "worker_protocol",
                            attempted, intervals[worker_id][1] - intervals[worker_id][0],
                            "progress_counter",
                        )
                        break
                    child_attempts[worker_id] = attempted
                    child_rss[worker_id] = int(frame.get("rss_bytes", 0))
                    delta = attempted - prior_attempted
                elif frame.get("kind") == "result":
                    prior_attempted = child_attempts[worker_id]
                    child_attempts[worker_id] = max(
                        child_attempts[worker_id], int(frame.get("attempted", 0))
                    )
                    child_rss[worker_id] = int(frame.get("rss_bytes", 0))
                    shards[worker_id] = frame
                    pending.remove(worker_id)
                    delta = child_attempts[worker_id] - prior_attempted
                else:
                    failure = ParallelResource(
                        "positive_boundary_parallel_v6", "worker_protocol",
                        worker_id, -1, "worker_error_frame",
                    )
                    break
                try:
                    charged_pairs += delta
                    meter.charge_pairs(delta)
                    meter.check(self._sample_rss(child_rss))
                except ParallelResource as error:
                    failure = error
                    break
        if failure is not None:
            self.serialization["max_epoch_inflight_bytes"] = max(
                self.serialization["max_epoch_inflight_bytes"],
                epoch_sent + epoch_received,
            )
            require(epoch_sent + epoch_received <=
                    MAX_EPOCH_SERIALIZATION_BYTES,
                    "failed epoch serialization cap")
            self.cancel.set()
            self.close(force=True)
            attempted_on_failure = sum(
                int(self.attempted_shared[index])
                for index in range(len(intervals))
            )
            charge_error = None
            try:
                remaining_charge = attempted_on_failure - charged_pairs
                require(remaining_charge >= 0, "live pair charge overflow")
                meter.charge_pairs(remaining_charge)
            except ParallelResource as error:
                charge_error = error
            self._counter_attempt(
                attempted_on_failure, False, total_pairs, retry_planned
            )
            self._record_epoch({
                **identity_body, "epoch_id": epoch_id,
                "status": "discarded",
                "reason": (charge_error or failure).reason,
                "intervals": intervals,
                "attempted_pairs": attempted_on_failure,
                "committed_pairs": 0,
                "returned_shards": len(shards),
            })
            raise charge_error or failure
        self.serialization["max_epoch_inflight_bytes"] = max(
            self.serialization["max_epoch_inflight_bytes"],
            epoch_sent + epoch_received,
        )
        require(epoch_sent + epoch_received <= MAX_EPOCH_SERIALIZATION_BYTES,
                "returned epoch serialization cap")
        try:
            ordered = [shards[index] for index in range(len(intervals))]
            accumulator = {}
            observed_cover = []
            for worker_id, (shard, interval) in enumerate(zip(ordered, intervals)):
                require(shard.get("result_digest") == _worker_result_digest(shard),
                        "worker result digest")
                require(shard.get("worker_id") == worker_id and
                        shard.get("epoch_id") == epoch_id and
                        shard.get("dual_digest") == str(dual_digest),
                        "worker result epoch identity")
                require(shard.get("descriptor_digest") == self.descriptor_digest and
                        shard.get("support_digest") == support_digest and
                        shard.get("prefix_digest") == prefix_digest,
                        "worker result roster identity")
                observed_cover.append(shard.get("interval"))
                require(shard.get("interval") == interval,
                        "worker result interval")
                require(shard.get("complete") is True and
                        shard.get("attempted") == interval[1] - interval[0],
                        "partial worker return")
                require(int(self.attempted_shared[worker_id]) ==
                        shard.get("attempted"),
                        "shared exact attempted counter")
                partial = _sparse_private(shard.get("accumulator"))
                expected_local = min(partial, key=_winner_key) if partial else None
                require(shard.get("local_winner") ==
                        (None if expected_local is None else
                         _key_public(expected_local)),
                        "worker local winner")
                require((expected_local is None) ==
                        (shard.get("local_provenance") is None),
                        "worker local provenance")
                _f3_add(accumulator, partial)
            require(observed_cover == intervals and intervals[0][0] == 0 and
                    intervals[-1][1] == total_pairs and
                    all(intervals[index][1] == intervals[index + 1][0]
                        for index in range(len(intervals) - 1)),
                    "ordered exact interval cover")
            selected = min(accumulator, key=_winner_key) if accumulator else None
            scalar = 0 if selected is None else accumulator[selected]
            meter.check(self._sample_rss(child_rss))
        except ParallelResource as error:
            self._counter_attempt(total_pairs, False, total_pairs, retry_planned)
            self._record_epoch({
                **identity_body, "epoch_id": epoch_id,
                "status": "discarded", "reason": error.reason,
                "intervals": intervals, "attempted_pairs": total_pairs,
                "committed_pairs": 0, "returned_shards": len(shards),
            })
            self._fail_cleanup()
            raise
        except ProtocolError as error:
            actual_returned = sum(
                int(self.attempted_shared[index])
                for index in range(len(intervals))
            )
            charge_error = None
            try:
                remaining_charge = actual_returned - charged_pairs
                require(remaining_charge >= 0, "protocol pair charge overflow")
                meter.charge_pairs(remaining_charge)
            except ParallelResource as resource_error:
                charge_error = resource_error
            self._counter_attempt(
                actual_returned, False, total_pairs, retry_planned
            )
            self._record_epoch({
                **identity_body, "epoch_id": epoch_id,
                "status": "discarded",
                "reason": (charge_error.reason if charge_error else
                           "merge_protocol"),
                "intervals": intervals, "attempted_pairs": actual_returned,
                "committed_pairs": 0, "returned_shards": len(shards),
            })
            self._fail_cleanup()
            if charge_error is not None:
                raise charge_error
            raise ParallelResource(
                "positive_boundary_parallel_v6", "worker_protocol", 1, 0,
                "merge_protocol:" + str(error),
            ) from error
        self._counter_attempt(total_pairs, True, total_pairs, retry_planned)
        self._record_epoch({
            **identity_body, "epoch_id": epoch_id,
            "status": "committed", "reason": None,
            "intervals": intervals, "attempted_pairs": total_pairs,
            "committed_pairs": total_pairs,
            "accumulator_digest": digest_obj(_sparse_public(accumulator)),
            "selected_key": None if selected is None else _key_public(selected),
            "selected_scalar": scalar,
            "returned_shards": len(shards),
        })
        return {
            "identity": identity_body, "epoch_id": epoch_id,
            "support": support_public, "support_raw": support_raw,
            "typed": typed, "lookup": lookup, "offsets": offsets,
            "intervals": intervals, "shards": ordered,
            "accumulator": accumulator, "selected_key": selected,
            "selected_scalar": scalar, "pair_count": total_pairs,
            "batch_complete": True,
        }


def _production_support(dual, runtime, v1):
    support = []
    for key, coefficient in dual.items():
        if key[:1] != b"R":
            continue
        block, component, raw = v1.decode_row_key(key)
        coefficient = int(coefficient) % 3
        if coefficient:
            support.append((int(block), int(component), bytes(raw), coefficient))
    return support


def _local_winner_provenance(roster, outcome, selected):
    if selected is None:
        return []
    block, relator, translation_blob = selected
    translation = _roster_unpack(roster, block, translation_blob)
    lookup = outcome["lookup"]
    answer = []
    for descriptor in roster["relator_index"].get((block, relator), ()):
        d_block, d_relator, component, h_blob, h, _, base = descriptor
        require(d_block == block and d_relator == relator,
                "relator descriptor index")
        g = _roster_mul(roster, block, translation, h)
        g_blob = _roster_blob(roster, block, g)
        record = lookup.get((block, component), {}).get(g_blob)
        if record is None:
            continue
        answer.append({
            "component": component,
            "g_hex": g_blob.hex(),
            "h_hex": h_blob.hex(),
            "lambda_coefficient": int(record[3]),
            "base_coefficient": int(base),
        })
    return answer


def _synthetic_translated_row(roster, selected):
    if selected is None:
        return {}
    block, relator, translation_blob = selected
    translation = _roster_unpack(roster, block, translation_blob)
    row = {}
    for descriptor in roster["relator_index"].get((block, relator), ()):
        d_block, d_relator, component, _, h, _, base = descriptor
        require(d_block == block and d_relator == relator,
                "synthetic relator descriptor index")
        g = _roster_mul(roster, block, translation, h)
        key = (block, component, _roster_blob(roster, block, g))
        coefficient = (row.get(key, 0) + int(base)) % 3
        if coefficient:
            row[key] = coefficient
        else:
            row.pop(key, None)
    return row


def _synthetic_direct_scalar(row, support_public):
    dual = {
        (int(block), int(component), bytes.fromhex(raw_hex)): int(coefficient)
        for block, component, raw_hex, coefficient in support_public
    }
    return sum(dual.get(key, 0) * coefficient
               for key, coefficient in row.items()) % 3


class CorrelationHookRegistry:
    def __init__(self):
        self._hooks = {}

    def register(self, name, factory):
        if name in self._hooks or not callable(factory):
            raise InputStop("correlation_hook_registration")
        self._hooks[name] = factory

    def resolve(self, name):
        if set(self._hooks) != {HOOK_NAME} or name != HOOK_NAME:
            raise InputStop("correlation_hook_owner")
        return self._hooks[name]


class AdapterRegistry:
    def __init__(self, seed, worker_count):
        self.seed = seed
        self.worker_count = worker_count
        self.instances = []

    def add(self, instance):
        if self.instances:
            raise ProtocolError("more than one persistent correlation pool")
        self.instances.append(instance)

    def close_all(self, force=False):
        for instance in self.instances:
            instance.close(force=force)

    def public_state(self):
        if self.instances:
            return self.instances[0].public_state()
        counters, chain, last_epoch = self.seed
        parent_rss = _current_rss()
        return {
            "schema": CHECKPOINT_SCHEMA,
            "hook": HOOK_NAME,
            "owner": "cached-v3 BoundaryDescriptorCache.correlation",
            "source_pins_sha256": source_pins_digest(),
            "descriptor_digest": None,
            "descriptor_count": 0,
            "worker_count": self.worker_count,
            "persistent_processes": True,
            "serial_dual_epochs": True,
            "atomic_full_epoch": True,
            "pair_order": PAIR_ORDER,
            "winner_order": WINNER_ORDER,
            "f3_encoding": F3_ENCODING,
            "historical_replay_claim": False,
            "counters": copy.deepcopy(counters),
            "serialization": {
                "sent_bytes": 0, "received_bytes": 0,
                "max_frame_bytes": 0, "max_epoch_inflight_bytes": 0,
                "support_bytes_last_epoch": 0,
                "support_cap_bytes": MAX_SUPPORT_BYTES,
                "frame_cap_bytes": MAX_FRAME_BYTES,
                "epoch_cap_bytes": MAX_EPOCH_SERIALIZATION_BYTES,
            },
            "resource": {
                "parent_rss_peak_bytes": parent_rss,
                "children_rss_peak_bytes": 0,
                "aggregate_rss_peak_bytes": parent_rss,
                "rss_samples": 1,
                "worker_restarts": 0,
                "checkpoint_bytes": 0,
            },
            "epoch_chain_sha256": chain,
            "epoch_records_retained": 0 if last_epoch is None else 1,
            "last_epoch": copy.deepcopy(last_epoch),
            "cleanup": {
                "transitions": ["not_started"], "started_pids": [],
                "live_pids_after_join": [], "worker_exitcodes": [],
                "complete": True,
            },
        }


def _production_roster(cache):
    descriptors = []
    groups = {}
    for item in cache.descriptors:
        block = int(item["block"])
        groups.setdefault(block, cache.v1.group_for_block(cache.rt, block))
        h_blob = bytes(item["h_blob"])
        h = cache.v1.unpack_element(cache.rt, h_blob, block)
        descriptors.append((
            block, int(item["relator_index"]), int(item["component"]),
            h_blob, h, item["h_inverse"], int(item["base_coefficient"]) % 3,
        ))
    relator_index = {}
    for descriptor in descriptors:
        relator_index.setdefault((descriptor[0], descriptor[1]), []).append(
            descriptor
        )
    return {
        "kind": "production", "runtime": cache.rt, "v1": cache.v1,
        "groups": groups, "descriptors": tuple(descriptors),
        "relator_index": {
            key: tuple(value) for key, value in relator_index.items()
        },
    }


def _install_production_hook(v3, registry):
    original = v3.BoundaryDescriptorCache
    hook_registry = CorrelationHookRegistry()

    def factory():
        class PositiveParallelBoundaryDescriptorCache(original):
            def __init__(self, runtime, v1, original_translated):
                super().__init__(runtime, v1, original_translated)
                roster = _production_roster(self)
                counters, chain, last_epoch = registry.seed
                self._positive_parallel_v6 = PersistentProcessRoster(
                    roster, registry.worker_count, counters, chain, last_epoch
                )
                registry.add(self._positive_parallel_v6)

            def correlation(self, dual, monitor):
                support = _production_support(dual, self.rt, self.v1)
                dual_public = self.v1.public_sparse(dual)
                dual_digest = self.v1.sha_obj(dual_public)
                meter = ProductionMeter(monitor, self.v1)
                try:
                    outcome = self._positive_parallel_v6.run_epoch(
                        support, dual_digest, meter,
                        epoch_context={
                            "input_sha256": self.input_digest,
                            "normalized_semantics_digest":
                                v3.NORMALIZED_SEMANTICS_DIGEST,
                            "owner_retained_columns": int(
                                monitor.counters.get("retained_columns", 0)
                            ),
                            "owner_boundary_pairs_before": int(
                                monitor.counters.get("boundary_pairs", 0)
                            ),
                        },
                    )
                except ParallelResource as error:
                    raise self.v1.ResourceStop(
                        error.phase, error.cap, error.value, error.limit
                    ) from error
                selected = outcome["selected_key"]
                if selected is None:
                    return None
                block, index, translation_blob = selected
                contributors = _local_winner_provenance(
                    self._positive_parallel_v6.roster, outcome, selected
                )
                contribution_sum = sum(
                    int(item["base_coefficient"]) *
                    int(item["lambda_coefficient"])
                    for item in contributors
                ) % 3
                require(contribution_sum == outcome["selected_scalar"] and
                        contribution_sum in (1, 2),
                        "local winner provenance scalar")
                row = self.translated(block, index, translation_blob)
                scalar = self.v1.pair(dual, row)
                require(scalar == outcome["selected_scalar"] and scalar,
                        "parallel cached complete boundary scalar")
                return {"row": row, "provenance": {
                    "family": "boundary", "block": block,
                    "base_relator_index": index,
                    "translation_hex": translation_blob.hex(),
                    "scalar": scalar,
                    "complete_support_occurrence_accumulation": True,
                    "left_translation_gate": "t*h=g",
                    "contributing_pairs": contributors,
                }}

        PositiveParallelBoundaryDescriptorCache.__name__ = (
            "PositiveParallelBoundaryDescriptorCacheV6"
        )
        return PositiveParallelBoundaryDescriptorCache

    hook_registry.register(HOOK_NAME, factory)
    replacement = hook_registry.resolve(HOOK_NAME)()
    v3.BoundaryDescriptorCache = replacement
    return {
        "registered_hook": HOOK_NAME,
        "owner_class": "BoundaryDescriptorCache",
        "replaced_method": "correlation",
        "base_class_preserved": original.__name__,
        "rank_dual_correction_candidate_common_owner": "cached-v3",
    }


def _load_v3():
    relative, expected_bytes, expected_sha = SOURCE_PINS["cached_v3_producer"]
    path = ROOT / relative
    raw = path.read_bytes()
    if len(raw) != expected_bytes or digest_bytes(raw) != expected_sha:
        raise InputStop("cached_v3_producer_pin")
    name = "_d972_task325_cached_v3_owner"
    if name in sys.modules:
        raise InputStop("cached_v3_module_slot_prebound")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise InputStop("cached_v3_module_loader")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        if sys.modules.get(name) is module:
            del sys.modules[name]
        raise
    return module


def _read_resume(resume_value, manifest_value, temporary):
    path = Path(resume_value)
    if path.is_absolute() or ".." in path.parts:
        raise InputStop("resume_path")
    resolved = ROOT / path
    if path.as_posix() == CHECKPOINT_ZIP:
        manifest_path = Path(manifest_value)
        if manifest_path.as_posix() != CHECKPOINT_MANIFEST or \
                manifest_path.is_absolute() or ".." in manifest_path.parts:
            raise InputStop("checkpoint_manifest_path")
        zip_raw = resolved.read_bytes()
        manifest_raw = (ROOT / manifest_path).read_bytes()
        if len(zip_raw) != SOURCE_PINS["checkpoint_zip"][1] or \
                digest_bytes(zip_raw) != SOURCE_PINS["checkpoint_zip"][2]:
            raise InputStop("checkpoint_zip_pin")
        if len(manifest_raw) != SOURCE_PINS["checkpoint_manifest"][1] or \
                digest_bytes(manifest_raw) != SOURCE_PINS["checkpoint_manifest"][2]:
            raise InputStop("checkpoint_manifest_pin")
        manifest = json.loads(manifest_raw.decode("ascii"))
        if manifest.get("zip", {}).get("member") != CHECKPOINT_MEMBER or \
                manifest.get("raw_checkpoint") != {
                    "bytes": RAW_CHECKPOINT_BYTES,
                    "sha256": RAW_CHECKPOINT_SHA256,
                }:
            raise InputStop("checkpoint_manifest_contract")
        with zipfile.ZipFile(io.BytesIO(zip_raw), "r") as archive:
            names = archive.namelist()
            if names != [CHECKPOINT_MEMBER]:
                raise InputStop("checkpoint_zip_member_roster")
            raw = archive.read(CHECKPOINT_MEMBER)
        if len(raw) != RAW_CHECKPOINT_BYTES or \
                digest_bytes(raw) != RAW_CHECKPOINT_SHA256:
            raise InputStop("checkpoint_raw_pin")
        checkpoint = json.loads(raw.decode("utf-8"))
        target = Path(temporary) / "resume-v6-source.json"
        target.write_bytes(raw)
        return checkpoint, target, {
            "transport": "sealed_zip_manifest",
            "zip": public_pins()["checkpoint_zip"],
            "manifest": public_pins()["checkpoint_manifest"],
            "member": CHECKPOINT_MEMBER,
            "raw_checkpoint": {
                "bytes": RAW_CHECKPOINT_BYTES,
                "sha256": RAW_CHECKPOINT_SHA256,
            },
        }
    normalized = path.as_posix()
    if not (normalized.startswith("ci/in/") or normalized.startswith("ci/out/")):
        raise InputStop("resume_boundary")
    raw = resolved.read_bytes()
    checkpoint = json.loads(raw.decode("utf-8"))
    body = dict(checkpoint)
    claimed = body.pop("self_digest", None)
    if not isinstance(claimed, str) or claimed != digest_obj(body):
        raise InputStop("resume_checkpoint_seal")
    adapter = checkpoint.get("positive_parallel_v6")
    if not isinstance(adapter, dict) or \
            adapter.get("schema") != CHECKPOINT_SCHEMA or \
            adapter.get("source_pins_sha256") != source_pins_digest():
        raise InputStop("resume_adapter_binding")
    target = Path(temporary) / "resume-v6-source.json"
    target.write_bytes(raw)
    return checkpoint, target, {
        "transport": "same_adapter_checkpoint",
        "path": normalized, "bytes": len(raw), "sha256": digest_bytes(raw),
        "self_digest": claimed,
    }


def _checkpoint_ref(path, raw, value):
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "basename": path.name,
        "bytes": len(raw),
        "sha256": digest_bytes(raw),
        "self_digest": value.get("self_digest"),
        "schema": value.get("schema"),
        "source_pins_sha256": source_pins_digest(),
    }


def _bind_checkpoint_bytes(checkpoint, adapter_state, byte_limit):
    value = copy.deepcopy(checkpoint)
    value["positive_parallel_v6"] = copy.deepcopy(adapter_state)
    value["positive_parallel_v6"]["next_clean_epoch"] = {
        "atomic_cursor": 0,
        "prefix_accumulator": [],
        "partial_epoch_committed": False,
        "retry_pending_pairs": value["positive_parallel_v6"]["counters"][
            "retry_pending_pairs"
        ],
    }
    value["positive_parallel_v6"]["historical_replay_claim"] = False
    guess = 0
    raw = b""
    for _ in range(12):
        value.setdefault("monitor", {}).setdefault("counters", {})[
            "checkpoint_bytes"
        ] = guess
        value["positive_parallel_v6"]["resource"]["checkpoint_bytes"] = guess
        value = _seal_v3(value)
        raw = canonical(value) + b"\n"
        measured = len(raw)
        if measured == guess:
            break
        guess = measured
    else:
        raise ProtocolError("checkpoint byte fixed point")
    if len(raw) > int(byte_limit):
        raise ParallelResource(
            "checkpoint_serialization", "checkpoint_bytes", len(raw),
            int(byte_limit), "adapter_checkpoint_bytes",
        )
    return value, raw


def _inner_reference(path, raw, value):
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "basename": path.name,
        "bytes": len(raw),
        "sha256": digest_bytes(raw),
        "self_digest": value.get("self_digest"),
        "terminal": value.get("terminal"),
        "schema": value.get("schema"),
        "source_pins": {
            label: public_pins()[label]
            for label in (
                "cached_v3_producer", "cached_v3_checker",
                "cached_v3_driver", "cached_v3_fixture",
            )
        },
    }


def _typed_boundary_ancestry(inner):
    columns = inner.get("columns", [])
    answer = []
    for basis_index, witness in enumerate(inner.get("nu_kernel_ancestry", []), 1):
        boundary_terms = []
        for column_id, coefficient in witness.get("boundary_coefficients", []):
            record = columns[int(column_id) - 1]
            provenance = record.get("provenance", {})
            require(record.get("family") == "boundary" and
                    provenance.get("family") == "boundary",
                    "typed boundary ancestry family")
            boundary_terms.append({
                "column_id": int(column_id),
                "coefficient": int(coefficient),
                "block": int(provenance["block"]),
                "base_relator_index": int(provenance["base_relator_index"]),
                "translation_hex": str(provenance["translation_hex"]),
                "scalar": int(provenance["scalar"]),
                "left_translation_gate": provenance.get(
                    "left_translation_gate"
                ),
                "complete_support_occurrence_accumulation": provenance.get(
                    "complete_support_occurrence_accumulation"
                ),
                "contributing_pairs": copy.deepcopy(
                    provenance.get("contributing_pairs", [])
                ),
            })
        answer.append({
            "basis_index": basis_index,
            "nu": copy.deepcopy(witness.get("nu")),
            "coefficients": copy.deepcopy(witness.get("coefficients", [])),
            "boundary_coefficients": copy.deepcopy(
                witness.get("boundary_coefficients", [])
            ),
            "correction_coefficients": copy.deepcopy(
                witness.get("correction_coefficients", [])
            ),
            "boundary_terms": boundary_terms,
            "B_zero_sha256": witness.get("B_zero_sha256"),
            "correction_boundary_zero_sha256": witness.get(
                "correction_boundary_zero_sha256"
            ),
        })
    return answer


def compact_positive_view(inner):
    require(inner.get("terminal") == V3_COMMON and
            inner.get("status") == "COMMON_WORD",
            "compact view requires cached-v3 COMMON")
    exactification = inner.get("exactification", {})
    literal = exactification.get("literal", {})
    r_words = exactification.get("r_words", {})
    require(set(r_words) == {"3", "9", "12"} and
            set(literal) == {"c_star", "v0", "u0", "h", "c_exact"},
            "compact exactification fields")
    return {
        "c_star": copy.deepcopy(inner.get("correction_word", [])),
        "solution_coefficients": copy.deepcopy(
            inner.get("solution_coefficients", [])
        ),
        "exact_words": copy.deepcopy(literal),
        "registered_relators": {
            "3": copy.deepcopy(r_words["3"]),
            "9": copy.deepcopy(r_words["9"]),
            "12": copy.deepcopy(r_words["12"]),
        },
        "exponents": copy.deepcopy(exactification.get("exponents", {})),
        "A": exactification.get("A"),
        "B": exactification.get("B"),
        "joint_kernel_replay": copy.deepcopy(
            exactification.get("joint_kernel_replay", {})
        ),
        "direct_all_seven_replay": copy.deepcopy(
            inner.get("exact_direct_replay", {})
        ),
        "typed_boundary_ancestry": _typed_boundary_ancestry(inner),
        "boundary_words_not_inserted": inner.get(
            "boundary_words_not_inserted"
        ),
    }


def _outer_base(status, terminal, pins, adapter_state, resume_transport):
    return {
        "schema": SCHEMA,
        "status": status,
        "terminal": terminal,
        "positive_only": True,
        "retrospective_epoch_replay_claim": None,
        "owner_hook": {
            "registered_hook": HOOK_NAME,
            "owner_class": "BoundaryDescriptorCache",
            "replaced_method": "correlation",
            "unchanged_owner_functions": [
                "rank", "dual", "correction", "candidate",
                "COMMON", "ordinary_checkpoint",
            ],
        },
        "source_pins": copy.deepcopy(pins),
        "source_pins_sha256": source_pins_digest(),
        "resume_transport": copy.deepcopy(resume_transport),
        "adapter_state": copy.deepcopy(adapter_state),
    }


def _terminal_reason(inner_terminal, inner):
    if inner_terminal.startswith(UNKNOWN_RESOURCE + ":"):
        return "cached_v3:" + inner_terminal[len(UNKNOWN_RESOURCE) + 1:]
    if inner_terminal.startswith(UNKNOWN_INPUT + ":"):
        return "cached_v3:" + inner_terminal[len(UNKNOWN_INPUT) + 1:]
    reason = inner.get("reason")
    return "cached_v3:" + str(reason or "untyped_stop")


def production(args, pins, output_target):
    inner_target = output_target.with_suffix(output_target.suffix + ".inner_v3.json")
    checkpoint_target = output_target.with_suffix(
        output_target.suffix + ".checkpoint.json"
    )
    for path in (inner_target, checkpoint_target):
        if path.exists():
            raise InputStop("stale_output_sidecar:" + path.name)
    with tempfile.TemporaryDirectory(prefix="d972-r07-v6-") as temporary:
        checkpoint, resume_path, resume_transport = _read_resume(
            args.resume, args.resume_manifest, temporary
        )
        seed = _seed_counters(checkpoint)
        v3 = _load_v3()
        registry = AdapterRegistry(seed, args.boundary_workers)
        hook = _install_production_hook(v3, registry)
        raw_inner_path = Path(temporary) / "inner-v3.json"
        argv = [
            "--mode", "PRODUCTION", "--output", str(raw_inner_path),
            "--resume", str(resume_path),
            "--seconds", str(args.seconds),
            "--boundary-pairs", str(args.boundary_pairs),
            "--fibre-scans", str(args.fibre_scans),
            "--candidate-words", str(args.candidate_words),
            "--retained-columns", str(args.retained_columns),
            "--checkpoint-bytes", str(args.checkpoint_bytes),
            "--rss-bytes", str(args.rss_bytes),
            "--oracle-rounds", str(args.oracle_rounds),
        ]
        captured = io.StringIO()
        try:
            with contextlib.redirect_stdout(captured):
                rc = v3.main(argv)
        finally:
            registry.close_all(force=False)
        if rc != 0 or not raw_inner_path.is_file():
            raise ProtocolError("cached-v3 owner stopped without receipt")
        inner_raw = raw_inner_path.read_bytes()
        inner = json.loads(inner_raw.decode("utf-8"))
        inner_terminal = str(inner.get("terminal", ""))
        adapter_state = registry.public_state()
        adapter_state["owner_hook_installation"] = hook
        if inner_terminal == V3_COMMON:
            if raw_inner_path.with_suffix(
                    raw_inner_path.suffix + ".checkpoint.json").exists():
                raise ProtocolError("COMMON retained temporary checkpoint")
            _write_exclusive(inner_target, inner_raw)
            reference = _inner_reference(inner_target, inner_raw, inner)
            receipt = _outer_base(
                "COMMON_WORD", COMMON, pins, adapter_state, resume_transport
            )
            receipt.update({
                "inner_cached_v3": reference,
                "compact_positive_view": compact_positive_view(inner),
                "claims": copy.deepcopy(POSITIVE_CLAIMS),
                "checkpoint": None,
            })
            return _seal_outer(receipt)
        is_resource = inner_terminal.startswith(UNKNOWN_RESOURCE + ":")
        is_input = inner_terminal.startswith(UNKNOWN_INPUT + ":")
        if not (is_resource or is_input):
            raise ProtocolError("cached-v3 unexpected terminal")
        reason = _terminal_reason(inner_terminal, inner)
        if is_resource:
            temporary_checkpoint = raw_inner_path.with_suffix(
                raw_inner_path.suffix + ".checkpoint.json"
            )
            if not temporary_checkpoint.is_file():
                raise ProtocolError("resource stop missing last-safe checkpoint")
            checkpoint_value = json.loads(
                temporary_checkpoint.read_text(encoding="utf-8")
            )
            checkpoint_value, checkpoint_raw = _bind_checkpoint_bytes(
                checkpoint_value, adapter_state, args.checkpoint_bytes
            )
            _write_exclusive(checkpoint_target, checkpoint_raw)
            adapter_state = copy.deepcopy(
                checkpoint_value["positive_parallel_v6"]
            )
            receipt = _outer_base(
                "UNKNOWN_RESOURCE", UNKNOWN_RESOURCE + ":" + reason,
                pins, adapter_state, resume_transport,
            )
            receipt.update({
                "reason": reason,
                "inner_terminal": inner_terminal,
                "resource_monitor_snapshot": copy.deepcopy(
                    inner.get("resource_monitor_snapshot", inner.get("monitor"))
                ),
                "checkpoint": _checkpoint_ref(
                    checkpoint_target, checkpoint_raw, checkpoint_value
                ),
                "inner_cached_v3": None,
                "compact_positive_view": None,
                "claims": copy.deepcopy(FALSE_CLAIMS),
            })
            return _seal_outer(receipt)
        temporary_checkpoint = raw_inner_path.with_suffix(
            raw_inner_path.suffix + ".checkpoint.json"
        )
        if temporary_checkpoint.exists():
            temporary_checkpoint.unlink()
        receipt = _outer_base(
            "UNKNOWN_INPUT", UNKNOWN_INPUT + ":" + reason,
            pins, adapter_state, resume_transport,
        )
        receipt.update({
            "reason": reason,
            "inner_terminal": inner_terminal,
            "checkpoint": None,
            "inner_cached_v3": None,
            "compact_positive_view": None,
            "claims": copy.deepcopy(FALSE_CLAIMS),
        })
        return _seal_outer(receipt)


def _load_fixture(path_value):
    path = Path(path_value)
    if path.is_absolute() or ".." in path.parts or not (
            path.as_posix().startswith("search/certs/") or
            path.as_posix().startswith("ci/in/")):
        raise InputStop("fixture_path")
    raw = (ROOT / path).read_bytes()
    if path.as_posix() == FIXTURE and (
            len(raw) != SOURCE_PINS["selftest_fixture_v6"][1] or
            digest_bytes(raw) != SOURCE_PINS["selftest_fixture_v6"][2]):
        raise InputStop("fixture_pin")
    fixture = json.loads(raw.decode("ascii"))
    require(fixture.get("schema") == FIXTURE_SCHEMA, "fixture schema")
    require(fixture.get("worker_counts") == list(WORKER_COUNTS),
            "fixture worker counts")
    return fixture, raw


def _c17_roster(descriptor_public):
    descriptors = []
    previous = None
    for item in descriptor_public:
        require(set(item) == {
            "block", "relator_index", "component", "h_hex",
            "base_coefficient",
        }, "C17 descriptor fields")
        raw = bytes.fromhex(item["h_hex"])
        require(len(raw) == 1 and raw[0] < 17, "C17 descriptor codec")
        key = (
            int(item["block"]), int(item["relator_index"]),
            int(item["component"]), raw, int(item["base_coefficient"]),
        )
        require(previous is None or previous <= key, "descriptor canonical order")
        previous = key
        h = raw[0]
        descriptors.append((
            key[0], key[1], key[2], raw, h, (-h) % 17, key[4] % 3,
        ))
    relator_index = {}
    for descriptor in descriptors:
        relator_index.setdefault((descriptor[0], descriptor[1]), []).append(
            descriptor
        )
    return {
        "kind": "c17", "descriptors": tuple(descriptors),
        "relator_index": {
            key: tuple(value) for key, value in relator_index.items()
        },
    }


def _fixture_support(value):
    support = []
    for item in value:
        require(isinstance(item, list) and len(item) == 4,
                "fixture support item")
        raw = bytes.fromhex(str(item[2]))
        require(len(raw) == 1 and raw[0] < 17, "fixture C17 support codec")
        support.append((int(item[0]), int(item[1]), raw, int(item[3])))
    _encode_support(support)
    return support


def _serial_c17(descriptors, support_public):
    typed = {}
    for position, item in enumerate(support_public):
        block, component, raw_hex, coefficient = item
        typed.setdefault((int(block), int(component)), []).append(
            (bytes.fromhex(raw_hex)[0], raw_hex, int(coefficient), position)
        )
    accumulator = {}
    contributors = {}
    pair_index = 0
    for descriptor in descriptors:
        block = int(descriptor["block"])
        relator = int(descriptor["relator_index"])
        component = int(descriptor["component"])
        h = bytes.fromhex(descriptor["h_hex"])[0]
        base = int(descriptor["base_coefficient"])
        for g, g_hex, coefficient, position in typed.get((block, component), []):
            translation = (g - h) % 17
            if (translation + h) % 17 != g:
                raise ProtocolError("serial C17 t*h=g")
            key = (block, relator, bytes((translation,)))
            combined = (accumulator.get(key, 0) + base * coefficient) % 3
            if combined:
                accumulator[key] = combined
            else:
                accumulator.pop(key, None)
            contributors.setdefault(key, []).append({
                "pair_index": pair_index,
                "support_position": position,
                "component": component,
                "g_hex": g_hex,
                "h_hex": "%02x" % h,
                "lambda_coefficient": coefficient,
                "base_coefficient": base,
            })
            pair_index += 1
    selected = min(accumulator, key=_winner_key) if accumulator else None
    selected_scalar = 0 if selected is None else accumulator[selected]
    row = {}
    if selected is not None:
        block, relator, translation_blob = selected
        translation = translation_blob[0]
        for descriptor in descriptors:
            if int(descriptor["block"]) != block or \
                    int(descriptor["relator_index"]) != relator:
                continue
            h = bytes.fromhex(descriptor["h_hex"])[0]
            row_key = (
                block, int(descriptor["component"]),
                bytes(((translation + h) % 17,)),
            )
            value = (row.get(row_key, 0) +
                     int(descriptor["base_coefficient"])) % 3
            if value:
                row[row_key] = value
            else:
                row.pop(row_key, None)
    dual = {
        (int(item[0]), int(item[1]), bytes.fromhex(item[2])): int(item[3])
        for item in support_public
    }
    direct = sum(dual.get(key, 0) * value for key, value in row.items()) % 3
    require(direct == selected_scalar, "serial C17 direct scalar")
    return {
        "pair_count": pair_index,
        "accumulator": _sparse_public(accumulator),
        "selected_key": None if selected is None else _key_public(selected),
        "selected_scalar": selected_scalar,
        "direct_scalar": direct,
        "row": [
            [[key[0], key[1], key[2].hex()], row[key]]
            for key in sorted(row, key=lambda item: (item[0], item[2], item[1]))
        ],
        "winner_contributors": [] if selected is None else
            contributors.get(selected, []),
    }


def _outcome_public(roster, outcome):
    selected = outcome["selected_key"]
    contributors = _local_winner_provenance(roster, outcome, selected)
    row = _synthetic_translated_row(roster, selected)
    direct = _synthetic_direct_scalar(row, outcome["support"])
    require(direct == outcome["selected_scalar"],
            "parallel C17 direct scalar")
    return {
        "identity": copy.deepcopy(outcome["identity"]),
        "epoch_id": outcome["epoch_id"],
        "dual_digest": outcome["identity"]["dual_digest"],
        "descriptor_digest": outcome["identity"]["descriptor_digest"],
        "support": copy.deepcopy(outcome["support"]),
        "support_buffer_hex": outcome["support_raw"].hex(),
        "offsets": list(outcome["offsets"]),
        "intervals": copy.deepcopy(outcome["intervals"]),
        "shards": copy.deepcopy(outcome["shards"]),
        "accumulator": _sparse_public(outcome["accumulator"]),
        "selected_key": None if selected is None else _key_public(selected),
        "selected_scalar": outcome["selected_scalar"],
        "winner_provenance": contributors,
        "translated_row": [
            [[key[0], key[1], key[2].hex()], row[key]]
            for key in sorted(row, key=lambda item: (item[0], item[2], item[1]))
        ],
        "direct_scalar": direct,
        "pair_count": outcome["pair_count"],
        "batch_complete": outcome["batch_complete"],
    }


def _projection(run):
    return {
        key: copy.deepcopy(run[key]) for key in (
            "accumulator", "selected_key", "selected_scalar",
            "winner_provenance", "translated_row", "direct_scalar",
            "pair_count", "batch_complete",
        )
    }


def _synthetic_positive_envelope():
    inner = _seal_v3({
        "schema": "synthetic-cached-v3-common/v1",
        "status": "COMMON_WORD",
        "terminal": "SYNTHETIC_CACHED_V3_COMMON",
        "correction_word": [1, -2, 3],
        "exact_words": {
            "c_star": [1, -2, 3], "v0": [4], "u0": [-4],
            "h": [5, -6], "c_exact": [1, -2, 3, 5, -6],
        },
        "registered_relators": {"3": [3], "9": [9], "12": [12]},
        "exponents": {"c_star": [54, -54], "c_exact": [0, 0]},
        "direct_all_seven_replay": {
            "joint_kernel": True, "hexagons": True,
            "pentagon_printed_order": True,
        },
        "typed_boundary_ancestry": [{
            "block": 1, "relator_index": 2, "component": 1,
            "translation_hex": "01", "coefficient": 2,
        }],
    })
    inner_raw = canonical(inner) + b"\n"
    compact = {
        "c_star": copy.deepcopy(inner["correction_word"]),
        "exact_words": copy.deepcopy(inner["exact_words"]),
        "registered_relators": copy.deepcopy(inner["registered_relators"]),
        "exponents": copy.deepcopy(inner["exponents"]),
        "direct_all_seven_replay": copy.deepcopy(
            inner["direct_all_seven_replay"]
        ),
        "typed_boundary_ancestry": copy.deepcopy(
            inner["typed_boundary_ancestry"]
        ),
    }
    return _seal_outer({
        "schema": "synthetic-positive-envelope/v6",
        "status": "COMMON_WORD", "terminal": "SYNTHETIC_V6_COMMON",
        "output_fresh": True,
        "inner_raw_hex": inner_raw.hex(),
        "inner_ref": {
            "bytes": len(inner_raw), "sha256": digest_bytes(inner_raw),
            "self_digest": inner["self_digest"],
            "terminal": inner["terminal"],
        },
        "checker_line": (
            "SYNTHETIC_CACHED_V3_CHECKER_PASS "
            "terminal=SYNTHETIC_CACHED_V3_COMMON"
        ),
        "checker_invocations": 1,
        "compact_view": compact,
        "claims": copy.deepcopy(POSITIVE_CLAIMS),
        "checkpoint": None,
    })


def _synthetic_resource_envelope():
    counters = _empty_counters()
    counters.update({
        "historical_attempted_pairs": 10,
        "historical_committed_pairs": 8,
        "historical_discarded_pairs": 2,
        "attempted_pairs": 14,
        "committed_pairs": 8,
        "discarded_pairs": 6,
        "historical_attempted_epochs": 3,
        "historical_committed_epochs": 2,
        "historical_discarded_epochs": 1,
        "attempted_epochs": 4,
        "committed_epochs": 2,
        "discarded_epochs": 2,
        "retry_pending_pairs": 4,
        "retried_pairs": 2,
        "retried_epochs": 1,
    })
    _validate_counter_equations(counters)
    adapter = {
        "schema": CHECKPOINT_SCHEMA,
        "source_pins_sha256": source_pins_digest(),
        "counters": counters,
        "cleanup": {
            "transitions": ["started", "closing", "terminating", "joined"],
            "started_pids": [41001, 41002],
            "live_pids_after_join": [],
            "worker_exitcodes": [-15, 0],
            "complete": True,
        },
        "next_clean_epoch": {
            "atomic_cursor": 0, "prefix_accumulator": [],
            "partial_epoch_committed": False, "retry_pending_pairs": 4,
        },
        "historical_replay_claim": False,
    }
    checkpoint = _seal_v3({
        "schema": "synthetic-v6-last-safe-checkpoint/v1",
        "positive_parallel_v6": copy.deepcopy(adapter),
        "source_pins_sha256": source_pins_digest(),
    })
    raw = canonical(checkpoint) + b"\n"
    return _seal_outer({
        "schema": "synthetic-resource-envelope/v6",
        "status": "UNKNOWN_RESOURCE",
        "terminal": "UNKNOWN_RESOURCE:synthetic_live_timeout",
        "reason": "synthetic_live_timeout",
        "output_fresh": True,
        "adapter_state": copy.deepcopy(adapter),
        "checkpoint_raw_hex": raw.hex(),
        "checkpoint_ref": {
            "bytes": len(raw), "sha256": digest_bytes(raw),
            "self_digest": checkpoint["self_digest"],
        },
        "inner_cached_v3": None,
        "compact_positive_view": None,
        "checker_invocations": 0,
        "claims": copy.deepcopy(FALSE_CLAIMS),
    })


def _reject(stage, reason):
    raise SelftestReject(stage, reason)


def _check_outer_seal(value, stage):
    if not isinstance(value, dict):
        _reject(stage, "shape")
    body = dict(value)
    claimed = body.pop("self_digest_sha256", None)
    if not isinstance(claimed, str) or claimed != digest_obj(body):
        _reject(stage, "seal")


def _independent_pairs(descriptors, support):
    typed = {}
    for position, item in enumerate(support):
        block, component, g_hex, coefficient = item
        typed.setdefault((int(block), int(component)), []).append(
            (bytes.fromhex(g_hex)[0], str(g_hex), int(coefficient), position)
        )
    pairs = []
    offsets = [0]
    for descriptor in descriptors:
        block = int(descriptor["block"])
        relator = int(descriptor["relator_index"])
        component = int(descriptor["component"])
        h = bytes.fromhex(descriptor["h_hex"])[0]
        base = int(descriptor["base_coefficient"])
        for g, g_hex, coefficient, support_position in typed.get(
                (block, component), []):
            translation = (g - h) % 17
            pairs.append({
                "key": (block, relator, bytes((translation,))),
                "contribution": base * coefficient % 3,
                "provenance": {
                    "component": component, "g_hex": g_hex,
                    "h_hex": "%02x" % h,
                    "lambda_coefficient": coefficient,
                    "base_coefficient": base,
                    "support_position": support_position,
                },
            })
        offsets.append(len(pairs))
    return pairs, offsets


def _independent_slice(pairs, start, stop):
    accumulator = {}
    first = {}
    for pair_index in range(start, stop):
        pair = pairs[pair_index]
        key = pair["key"]
        value = (accumulator.get(key, 0) + pair["contribution"]) % 3
        if value:
            accumulator[key] = value
        else:
            accumulator.pop(key, None)
        first.setdefault(key, {
            "pair_index": pair_index,
            "component": pair["provenance"]["component"],
            "g_hex": pair["provenance"]["g_hex"],
            "h_hex": pair["provenance"]["h_hex"],
            "lambda_coefficient": pair["provenance"]["lambda_coefficient"],
            "base_coefficient": pair["provenance"]["base_coefficient"],
        })
    winner = min(accumulator, key=_winner_key) if accumulator else None
    return accumulator, winner, None if winner is None else first[winner]


def _expected_winner_provenance(descriptors, support, selected):
    if selected is None:
        return []
    block, relator, translation_hex = selected
    translation = bytes.fromhex(translation_hex)[0]
    lookup = {}
    for item in support:
        lookup[(int(item[0]), int(item[1]), str(item[2]))] = int(item[3])
    answer = []
    for descriptor in descriptors:
        if int(descriptor["block"]) != int(block) or \
                int(descriptor["relator_index"]) != int(relator):
            continue
        h = bytes.fromhex(descriptor["h_hex"])[0]
        g_hex = "%02x" % ((translation + h) % 17)
        coefficient = lookup.get((
            int(block), int(descriptor["component"]), g_hex
        ))
        if coefficient is not None:
            answer.append({
                "component": int(descriptor["component"]),
                "g_hex": g_hex,
                "h_hex": str(descriptor["h_hex"]),
                "lambda_coefficient": coefficient,
                "base_coefficient": int(descriptor["base_coefficient"]),
            })
    return answer


def _validate_kernel_run(run, descriptors):
    support = run.get("support")
    if not isinstance(support, list):
        _reject("kernel.dual", "dual_digest")
    try:
        support_records = _fixture_support(support)
        support_raw, support_public = _encode_support(support_records)
    except (ProtocolError, TypeError, ValueError):
        _reject("kernel.dual", "noncanonical_c17_codec")
    expected_dual = digest_obj(support)
    if run.get("dual_digest") != expected_dual or \
            run.get("identity", {}).get("dual_digest") != expected_dual:
        _reject("kernel.dual", "dual_digest")
    roster = _c17_roster(descriptors)
    if run.get("descriptor_digest") != _roster_digest(roster) or \
            run.get("identity", {}).get("descriptor_digest") != _roster_digest(roster):
        _reject("kernel.epoch", "cross_epoch_result")
    if support_public != support or run.get("support_buffer_hex") != support_raw.hex():
        _reject("kernel.dual", "dual_digest")
    pairs, offsets = _independent_pairs(descriptors, support)
    if run.get("offsets") != offsets or \
            run.get("identity", {}).get("prefix_offsets") != offsets:
        _reject("kernel.cover", "missing_interval")
    identity = run.get("identity")
    if not isinstance(identity, dict) or \
            identity.get("owner_epoch_context") != {"universe": "C17"} or \
            digest_obj(identity) != run.get("epoch_id"):
        _reject("kernel.epoch", "cross_epoch_result")
    total = len(pairs)
    intervals = run.get("intervals")
    shards = run.get("shards")
    if not isinstance(intervals, list) or not isinstance(shards, list) or \
            len(intervals) != len(shards):
        _reject("kernel.cover", "missing_interval")
    if total == 0:
        if intervals != []:
            _reject("kernel.cover", "overlapping_interval")
    else:
        if not intervals or intervals[0][0] != 0 or intervals[-1][1] != total:
            _reject("kernel.cover", "missing_interval")
        for left, right in zip(intervals, intervals[1:]):
            if int(right[0]) < int(left[1]):
                _reject("kernel.cover", "overlapping_interval")
            if int(right[0]) > int(left[1]):
                _reject("kernel.cover", "missing_interval")
    merged = {}
    for worker_id, (interval, shard) in enumerate(zip(intervals, shards)):
        if shard.get("dual_digest") != expected_dual:
            _reject("kernel.dual", "dual_digest")
        if shard.get("epoch_id") != run.get("epoch_id"):
            _reject("kernel.epoch", "cross_epoch_result")
        if shard.get("complete") is not True or \
                shard.get("attempted") != int(interval[1]) - int(interval[0]):
            _reject("kernel.completion", "partial_return")
        if shard.get("interval") != interval:
            if shard.get("interval", [0, 0])[0] < interval[0]:
                _reject("kernel.cover", "overlapping_interval")
            _reject("kernel.cover", "missing_interval")
        expected_partial, expected_winner, expected_provenance = \
            _independent_slice(pairs, int(interval[0]), int(interval[1]))
        try:
            partial = _sparse_private(shard.get("accumulator"))
        except (ProtocolError, TypeError, ValueError):
            _reject("kernel.merge", "accumulator")
        if partial != expected_partial:
            _reject("kernel.merge", "accumulator")
        expected_public_winner = (
            None if expected_winner is None else _key_public(expected_winner)
        )
        if shard.get("local_winner") != expected_public_winner or \
                shard.get("local_provenance") != expected_provenance:
            _reject("kernel.winner", "winner_provenance")
        if shard.get("result_digest") != _worker_result_digest(shard):
            _reject("kernel.merge", "accumulator")
        _f3_add(merged, partial)
    if run.get("accumulator") != _sparse_public(merged):
        _reject("kernel.merge", "accumulator")
    selected = min(merged, key=_winner_key) if merged else None
    selected_public = None if selected is None else _key_public(selected)
    scalar = 0 if selected is None else merged[selected]
    if run.get("selected_key") != selected_public or \
            run.get("selected_scalar") != scalar or \
            run.get("winner_provenance") != _expected_winner_provenance(
                descriptors, support, selected_public):
        _reject("kernel.winner", "winner_provenance")
    serial = _serial_c17(descriptors, support)
    if run.get("translated_row") != serial["row"] or \
            run.get("direct_scalar") != scalar or \
            run.get("direct_scalar") != serial["direct_scalar"]:
        _reject("kernel.scalar", "direct_scalar")
    if run.get("pair_count") != total:
        _reject("kernel.cover", "missing_interval")
    if run.get("batch_complete") is not True:
        _reject("kernel.completion", "partial_return")


def _validate_cleanup(cleanup):
    if not isinstance(cleanup, dict) or cleanup.get("complete") is not True or \
            cleanup.get("live_pids_after_join") != []:
        _reject("cleanup", "child_alive")
    transitions = cleanup.get("transitions")
    if transitions not in (
            ["started", "closing", "joined"],
            ["started", "closing", "terminating", "joined"],
            ["not_started"],
    ):
        _reject("cleanup", "child_alive")


def _validate_claim_flags(claims, positive):
    expected = POSITIVE_CLAIMS if positive else FALSE_CLAIMS
    if not isinstance(claims, dict):
        _reject("claims", "shape")
    for field in ("separator", "cofinal_lift", "fake", "ihara_witness"):
        if claims.get(field) is not expected[field]:
            _reject("claims", field)
    if claims != expected:
        _reject("claims", "claim_vector")


def _synthetic_compact(inner):
    return {
        "c_star": copy.deepcopy(inner["correction_word"]),
        "exact_words": copy.deepcopy(inner["exact_words"]),
        "registered_relators": copy.deepcopy(inner["registered_relators"]),
        "exponents": copy.deepcopy(inner["exponents"]),
        "direct_all_seven_replay": copy.deepcopy(
            inner["direct_all_seven_replay"]
        ),
        "typed_boundary_ancestry": copy.deepcopy(
            inner["typed_boundary_ancestry"]
        ),
    }


def _validate_synthetic_positive(value):
    _check_outer_seal(value, "positive.inner")
    if value.get("status") != "COMMON_WORD" or \
            value.get("terminal") != "SYNTHETIC_V6_COMMON" or \
            value.get("checkpoint") is not None:
        _reject("envelope", "terminal")
    raw = bytes.fromhex(str(value.get("inner_raw_hex", "")))
    reference = value.get("inner_ref", {})
    if reference.get("bytes") != len(raw) or \
            reference.get("sha256") != digest_bytes(raw):
        _reject("positive.inner", "inner_digest")
    try:
        inner = json.loads(raw.decode("ascii"))
    except (UnicodeError, json.JSONDecodeError):
        _reject("positive.inner", "inner_digest")
    inner_body = dict(inner)
    claimed = inner_body.pop("self_digest", None)
    if claimed != digest_obj(inner_body) or \
            reference.get("self_digest") != claimed or \
            reference.get("terminal") != inner.get("terminal"):
        _reject("positive.inner", "inner_digest")
    expected_line = (
        "SYNTHETIC_CACHED_V3_CHECKER_PASS "
        "terminal=SYNTHETIC_CACHED_V3_COMMON"
    )
    if value.get("checker_invocations") != 1 or \
            value.get("checker_line") != expected_line:
        _reject("positive.checker", "checker_terminal")
    if value.get("compact_view") != _synthetic_compact(inner):
        _reject("positive.compact", "compact_view")
    _validate_claim_flags(value.get("claims"), True)
    if value.get("output_fresh") is not True:
        _reject("transport", "stale_output")


def _validate_synthetic_resource(value):
    _check_outer_seal(value, "resource.checkpoint")
    if value.get("status") != "UNKNOWN_RESOURCE" or \
            value.get("terminal") != "UNKNOWN_RESOURCE:synthetic_live_timeout":
        _reject("envelope", "terminal")
    adapter = value.get("adapter_state", {})
    _validate_cleanup(adapter.get("cleanup"))
    counters = adapter.get("counters")
    try:
        _validate_counter_equations(counters)
    except ProtocolError:
        _reject("counters", "historical_reset")
    if any(counters[stem] < counters["historical_" + stem]
           for stem in (
               "attempted_pairs", "committed_pairs", "discarded_pairs",
               "retried_pairs", "attempted_epochs", "committed_epochs",
               "discarded_epochs", "retried_epochs",
           )):
        _reject("counters", "historical_reset")
    raw = bytes.fromhex(str(value.get("checkpoint_raw_hex", "")))
    reference = value.get("checkpoint_ref", {})
    if reference.get("bytes") != len(raw) or \
            reference.get("sha256") != digest_bytes(raw):
        _reject("resource.checkpoint", "checkpoint_binding")
    try:
        checkpoint = json.loads(raw.decode("ascii"))
    except (UnicodeError, json.JSONDecodeError):
        _reject("resource.checkpoint", "checkpoint_binding")
    body = dict(checkpoint)
    claimed = body.pop("self_digest", None)
    if claimed != digest_obj(body) or reference.get("self_digest") != claimed or \
            checkpoint.get("positive_parallel_v6") != adapter:
        _reject("resource.checkpoint", "checkpoint_binding")
    claims = value.get("claims", {})
    if claims.get("common_word") is not False or \
            claims.get("finite_common_word") is not False:
        _reject("resource.claims", "positive_claim")
    _validate_claim_flags(claims, False)
    if value.get("inner_cached_v3") is not None or \
            value.get("compact_positive_view") is not None or \
            value.get("checker_invocations") != 0:
        _reject("resource.claims", "positive_claim")
    if value.get("output_fresh") is not True:
        _reject("transport", "stale_output")


def _validate_selftest_document(document):
    if not isinstance(document, dict) or document.get("schema") != \
            SELFTEST_SCHEMA + "/document":
        _reject("document", "schema")
    for case in document.get("cases", []):
        _validate_kernel_run(case["run"], case["descriptors"])
        expected = _serial_c17(case["descriptors"], case["run"]["support"])
        if _projection(case["run"]) != {
                "accumulator": expected["accumulator"],
                "selected_key": expected["selected_key"],
                "selected_scalar": expected["selected_scalar"],
                "winner_provenance": _expected_winner_provenance(
                    case["descriptors"], case["run"]["support"],
                    expected["selected_key"],
                ),
                "translated_row": expected["row"],
                "direct_scalar": expected["direct_scalar"],
                "pair_count": expected["pair_count"],
                "batch_complete": True,
        }:
            _reject("kernel.merge", "accumulator")
    persistent = document.get("persistent_epochs", {})
    if set(persistent) != {"2", "4"}:
        _reject("kernel.cover", "missing_interval")
    for worker_count in WORKER_COUNTS:
        runs = persistent[str(worker_count)]["runs"]
        if len(runs) != 3 or len({run["dual_digest"] for run in runs}) != 3:
            _reject("kernel.epoch", "cross_epoch_result")
        for run in runs:
            _validate_kernel_run(run, document["full_descriptors"])
        _validate_cleanup(persistent[str(worker_count)]["cleanup"])
    for left, right in zip(
            persistent["2"]["runs"], persistent["4"]["runs"]):
        if _projection(left) != _projection(right):
            _reject("kernel.merge", "accumulator")
    for fault in document.get("fault_controls", []):
        if fault.get("rejected") is not True:
            _reject("kernel.completion", "partial_return")
        _validate_cleanup(fault.get("cleanup"))
    _validate_synthetic_positive(document.get("positive_envelope"))
    _validate_synthetic_resource(document.get("resource_envelope"))


def _refresh_worker_result(shard):
    shard["result_digest"] = _worker_result_digest(shard)


def _apply_mutation(document, name):
    run = document["persistent_epochs"]["2"]["runs"][2]
    positive = document["positive_envelope"]
    resource = document["resource_envelope"]
    if name == "wrong_dual_digest":
        run["shards"][0]["dual_digest"] = "0" * 64
        _refresh_worker_result(run["shards"][0])
    elif name == "noncanonical_c17_alias":
        run["support"][0][2] = "14"
    elif name == "missing_interval":
        run["intervals"].pop()
        run["shards"].pop()
    elif name == "overlapping_interval":
        run["intervals"][1][0] = run["intervals"][0][1] - 1
        run["shards"][1]["interval"] = copy.deepcopy(run["intervals"][1])
        _refresh_worker_result(run["shards"][1])
    elif name == "changed_accumulator":
        run["accumulator"][0][1] = 1 if run["accumulator"][0][1] == 2 else 2
    elif name == "changed_winner_provenance":
        run["winner_provenance"][0]["g_hex"] = "00"
    elif name == "changed_direct_scalar":
        run["direct_scalar"] = 1 if run["direct_scalar"] != 1 else 2
    elif name == "cross_epoch_result":
        run["shards"][0]["epoch_id"] = \
            document["persistent_epochs"]["2"]["runs"][1]["epoch_id"]
        _refresh_worker_result(run["shards"][0])
    elif name == "partial_return_accepted":
        run["shards"][0]["complete"] = False
        run["shards"][0]["attempted"] -= 1
        _refresh_worker_result(run["shards"][0])
    elif name == "child_left_alive":
        resource["adapter_state"]["cleanup"]["live_pids_after_join"] = [41001]
        resource["adapter_state"]["cleanup"]["complete"] = False
        resource = _seal_outer(resource)
        document["resource_envelope"] = resource
    elif name == "counter_reset":
        resource["adapter_state"]["counters"]["attempted_pairs"] = 0
        resource = _seal_outer(resource)
        document["resource_envelope"] = resource
    elif name == "unbound_checkpoint":
        resource["checkpoint_ref"]["sha256"] = "0" * 64
        document["resource_envelope"] = _seal_outer(resource)
    elif name == "changed_inner_receipt_digest":
        positive["inner_ref"]["sha256"] = "0" * 64
        document["positive_envelope"] = _seal_outer(positive)
    elif name == "fake_v3_checker_terminal":
        positive["checker_line"] = "synthetic prefix " + positive["checker_line"]
        document["positive_envelope"] = _seal_outer(positive)
    elif name == "compact_view_mismatch":
        positive["compact_view"]["c_star"].append(99)
        document["positive_envelope"] = _seal_outer(positive)
    elif name == "positive_claim_on_resource_exit":
        resource["claims"]["common_word"] = True
        document["resource_envelope"] = _seal_outer(resource)
    elif name in ("separator_flip", "cofinal_flip", "fake_flip", "ihara_flip"):
        field = {
            "separator_flip": "separator", "cofinal_flip": "cofinal_lift",
            "fake_flip": "fake", "ihara_flip": "ihara_witness",
        }[name]
        positive["claims"][field] = True
        document["positive_envelope"] = _seal_outer(positive)
    elif name == "terminal_reseal":
        positive["terminal"] = "SYNTHETIC_V6_COMMON_RESEALED"
        document["positive_envelope"] = _seal_outer(positive)
    elif name == "stale_output":
        positive["output_fresh"] = False
        document["positive_envelope"] = _seal_outer(positive)
    else:
        raise ProtocolError("unknown mutation:" + name)


def _run_mutations(document, fixture):
    baseline_digest = digest_obj(document)
    effects = []
    for specification in fixture["mutations"]:
        mutant = copy.deepcopy(document)
        _apply_mutation(mutant, specification["name"])
        mutant_digest = digest_obj(mutant)
        require(mutant_digest != baseline_digest,
                "mutation no-op:" + specification["name"])
        try:
            _validate_selftest_document(mutant)
        except SelftestReject as error:
            require(error.stage == specification["stage"] and
                    error.reason == specification["reason"],
                    "mutation narrow rejection:" + specification["name"] +
                    ":" + error.stage + ":" + error.reason)
            effects.append({
                "name": specification["name"],
                "stage": error.stage, "reason": error.reason,
                "baseline_digest": baseline_digest,
                "mutant_digest": mutant_digest, "rejected": True,
            })
        else:
            raise ProtocolError("mutation survived:" + specification["name"])
    return effects


def _run_one_c17_pool(descriptors, worker_count, jobs):
    roster = _c17_roster(descriptors)
    pool = PersistentProcessRoster(roster, worker_count)
    runs = []
    try:
        for support_value in jobs:
            support = _fixture_support(support_value)
            _, support_public = _encode_support(support)
            dual_digest = digest_obj(support_public)
            outcome = pool.run_epoch(
                support, dual_digest, SelftestMeter(seconds=5.0),
                epoch_context={"universe": "C17"},
            )
            runs.append(_outcome_public(roster, outcome))
    finally:
        pool.close(force=False)
    return runs, pool.public_state()


def _run_fault_control(descriptors, support_value, name):
    roster = _c17_roster(descriptors)
    pool = PersistentProcessRoster(roster, 2)
    fault = {
        "live_timeout": "timeout",
        "worker_death": "death",
        "partial_return": "partial",
    }[name]
    rejected = False
    error_record = None
    try:
        support = _fixture_support(support_value)
        _, support_public = _encode_support(support)
        seconds = 0.125 if name == "live_timeout" else 5.0
        pool.run_epoch(
            support, digest_obj(support_public),
            SelftestMeter(seconds=seconds), fault=fault,
            epoch_context={"universe": "C17", "fault": name},
        )
    except ParallelResource as error:
        rejected = True
        error_record = {
            "phase": error.phase, "cap": error.cap,
            "reason": error.reason,
        }
    finally:
        pool.close(force=True)
    require(rejected, "fault survived:" + name)
    state = pool.public_state()
    return {
        "name": name, "rejected": True,
        "error": error_record,
        "cleanup": state["cleanup"],
        "counters": state["counters"],
    }


def selftest(args, pins):
    fixture, fixture_raw = _load_fixture(args.fixture)
    codec = fixture.get("codec", {})
    require(codec == {
        "name": "C17-canonical-one-byte",
        "identity_hex": "00", "elements": 17,
        "multiplication": "(a+b) mod 17",
        "inverse": "(-a) mod 17",
        "translation_gate": "t*h=g",
    }, "fixture C17 codec")
    full_descriptors = fixture["descriptors"]
    cases_by_prefix = {0: [], 1: [], len(full_descriptors): []}
    for case in fixture["cases"]:
        prefix = int(case["descriptor_prefix"])
        require(prefix in cases_by_prefix, "fixture descriptor prefix")
        cases_by_prefix[prefix].append(case)
    case_records = []
    for prefix in (0, 1):
        descriptors = full_descriptors[:prefix]
        jobs = [case["support"] for case in cases_by_prefix[prefix]]
        runs, state = _run_one_c17_pool(descriptors, 2, jobs)
        for case, run in zip(cases_by_prefix[prefix], runs):
            serial = _serial_c17(descriptors, run["support"])
            case_records.append({
                "name": case["name"], "descriptors": descriptors,
                "run": run, "serial_digest": digest_obj(serial),
                "pool_cleanup": copy.deepcopy(state["cleanup"]),
            })
    full_case_jobs = [case["support"]
                      for case in cases_by_prefix[len(full_descriptors)]]
    roster2 = _c17_roster(full_descriptors)
    pool2 = PersistentProcessRoster(roster2, 2)
    full_runs = []
    epoch2_runs = []
    try:
        for support_value in full_case_jobs:
            support = _fixture_support(support_value)
            _, public = _encode_support(support)
            full_runs.append(_outcome_public(
                roster2, pool2.run_epoch(
                    support, digest_obj(public), SelftestMeter(seconds=5.0),
                    epoch_context={"universe": "C17"},
                )
            ))
        for epoch in fixture["persistent_epochs"]:
            support = _fixture_support(epoch["support"])
            _, public = _encode_support(support)
            epoch2_runs.append(_outcome_public(
                roster2, pool2.run_epoch(
                    support, digest_obj(public), SelftestMeter(seconds=5.0),
                    epoch_context={"universe": "C17"},
                )
            ))
    finally:
        pool2.close(force=False)
    state2 = pool2.public_state()
    for case, run in zip(
            cases_by_prefix[len(full_descriptors)], full_runs):
        serial = _serial_c17(full_descriptors, run["support"])
        case_records.append({
            "name": case["name"], "descriptors": full_descriptors,
            "run": run, "serial_digest": digest_obj(serial),
            "pool_cleanup": copy.deepcopy(state2["cleanup"]),
        })
    roster4 = _c17_roster(full_descriptors)
    pool4 = PersistentProcessRoster(roster4, 4)
    epoch4_runs = []
    try:
        for epoch in fixture["persistent_epochs"]:
            support = _fixture_support(epoch["support"])
            _, public = _encode_support(support)
            epoch4_runs.append(_outcome_public(
                roster4, pool4.run_epoch(
                    support, digest_obj(public), SelftestMeter(seconds=5.0),
                    epoch_context={"universe": "C17"},
                )
            ))
    finally:
        pool4.close(force=False)
    state4 = pool4.public_state()
    persistent = {
        "2": {
            "runs": epoch2_runs, "cleanup": state2["cleanup"],
            "started_pids": state2["cleanup"]["started_pids"],
            "one_roster_reused": True,
        },
        "4": {
            "runs": epoch4_runs, "cleanup": state4["cleanup"],
            "started_pids": state4["cleanup"]["started_pids"],
            "one_roster_reused": True,
        },
    }
    fault_support = [
        [1, 2, "03", 1], [1, 3, "05", 1], [1, 1, "03", 1],
        [2, 5, "09", 1], [2, 4, "07", 1],
    ]
    fault_controls = [
        _run_fault_control(full_descriptors, fault_support, name)
        for name in fixture["faults"]
    ]
    document = {
        "schema": SELFTEST_SCHEMA + "/document",
        "codec": copy.deepcopy(codec),
        "full_descriptors": copy.deepcopy(full_descriptors),
        "cases": case_records,
        "persistent_epochs": persistent,
        "fault_controls": fault_controls,
        "positive_envelope": _synthetic_positive_envelope(),
        "resource_envelope": _synthetic_resource_envelope(),
    }
    _validate_selftest_document(document)
    effects = _run_mutations(document, fixture)
    require(len(effects) == len(fixture["mutations"]),
            "mutation count")
    receipt = {
        "schema": SELFTEST_SCHEMA,
        "status": "SELFTEST_PASS",
        "terminal": SELFTEST_PASS,
        "fixture": {
            "path": Path(args.fixture).as_posix(),
            "bytes": len(fixture_raw), "sha256": digest_bytes(fixture_raw),
            "digest": digest_obj(fixture),
        },
        "source_pins": copy.deepcopy(pins),
        "source_pins_sha256": source_pins_digest(),
        "document": document,
        "mutation_controls": {
            "names": [item["name"] for item in fixture["mutations"]],
            "attempted": len(effects), "rejected": len(effects),
            "effects": effects,
        },
        "production_executed": False,
        "actual_common_checker_invocations": 0,
        "retrospective_epoch_replay_claim": None,
        "claims": copy.deepcopy(FALSE_CLAIMS),
    }
    return _seal_outer(receipt)


def _input_unknown(args, pins, reason):
    counters = _empty_counters()
    adapter_state = AdapterRegistry(
        (counters, digest_obj({"genesis": True}), None),
        args.boundary_workers if args.boundary_workers in WORKER_COUNTS else 2,
    ).public_state()
    receipt = _outer_base(
        "UNKNOWN_INPUT", UNKNOWN_INPUT + ":" + reason,
        pins or {}, adapter_state, None,
    )
    receipt.update({
        "reason": reason, "inner_terminal": None,
        "checkpoint": None, "inner_cached_v3": None,
        "compact_positive_view": None,
        "claims": copy.deepcopy(FALSE_CLAIMS),
    })
    return _seal_outer(receipt)


def parser():
    value = argparse.ArgumentParser()
    value.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"),
                       default="PRODUCTION")
    value.add_argument("--fixture", default=FIXTURE)
    value.add_argument("--resume", default=CHECKPOINT_ZIP)
    value.add_argument("--resume-manifest", default=CHECKPOINT_MANIFEST)
    value.add_argument("--boundary-workers", type=int, default=2)
    value.add_argument("--seconds", type=float, default=19_800.0)
    value.add_argument("--boundary-pairs", type=int, default=8_000_000)
    value.add_argument("--fibre-scans", type=int, default=80_000_000)
    value.add_argument("--candidate-words", type=int, default=2_000_000)
    value.add_argument("--retained-columns", type=int, default=250_000)
    value.add_argument("--checkpoint-bytes", type=int, default=4_000_000_000)
    value.add_argument("--rss-bytes", type=int, default=5_700_000_000)
    value.add_argument("--oracle-rounds", type=int, default=1)
    value.add_argument("--output", required=True)
    return value


def main(argv=None):
    args = parser().parse_args(argv)
    output_target = _fresh_relative(args.output, ".json")
    pins = None
    try:
        pins = authenticate_sources()
        if args.boundary_workers not in WORKER_COUNTS:
            raise InputStop("boundary_workers_must_be_2_or_4")
        if args.mode == "SELFTEST":
            receipt = selftest(args, pins)
        else:
            receipt = production(args, pins, output_target)
    except (InputStop, OSError, UnicodeError, json.JSONDecodeError,
            zipfile.BadZipFile) as error:
        receipt = _input_unknown(
            args, pins, type(error).__name__ + ":" + str(error)
        )
    _write_exclusive(output_target, canonical(receipt) + b"\n")
    if args.mode == "SELFTEST" and receipt.get("terminal") == SELFTEST_PASS:
        print(SELFTEST_PASS, flush=True)
    print(PRODUCER_PREFIX + " " + str(receipt["terminal"]), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
