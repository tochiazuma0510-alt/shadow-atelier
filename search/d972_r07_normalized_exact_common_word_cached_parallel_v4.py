#!/usr/bin/env python3
"""R07 cached-v3 production adapter with one persistent fork pool.

The v3 search, rank owner, caches, correction oracle, and checkpoint writer
remain authoritative.  This module replaces only the fixed-dual boundary
correlation call.  SELFTEST is a small, process-backed map/reduce fixture;
PRODUCTION wraps the authenticated cached-v3 source and keeps the pool alive
across boundary epochs.
"""
from __future__ import annotations

import argparse
import copy
import contextlib
import hashlib
import importlib.util
import io
import json
import multiprocessing
import os
import resource
import tempfile
import time
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-normalized-exact-common-word-cached-parallel/v4"
SELF_SCHEMA = SCHEMA + "/selftest"
PRODUCTION_SCHEMA = SCHEMA + "/production"
FIXTURE_SCHEMA = SCHEMA + "/fixture/v4"
SELFTEST_MARKER = "R07_NORMALIZED_EXACT_COMMON_WORD_CACHED_PARALLEL_V4_SELFTEST_PASS"
TERMINAL_PREFIX = "R07_NORMALIZED_EXACT_COMMON_WORD_CACHED_PARALLEL_V4_PRODUCER_TERMINAL"
PASS_TERMINAL = "PASS"
UNKNOWN_RESUME = "UNKNOWN_INPUT:authenticated_resume_absent"
UNKNOWN_ADAPTER = "UNKNOWN_INPUT:adapter_execution_failed"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE:parallel_adapter_resource_stop"
WORKER_COUNTS = (2, 3, 4)
CASE_NAMES = (
    "active_two_shards",
    "cancel_across_shards",
    "nontrivial_lex_winner",
    "no_active_key",
)
MUTATIONS = (
    "omitted_shard", "duplicated_shard", "overlapping_interval", "gap",
    "permuted_pair_order", "wrong_dual_digest", "wrong_descriptor_digest",
    "changed_coefficient", "changed_translation_key", "changed_contributor",
    "wrong_partial", "wrong_mod3_merge", "zero_kept_active", "wrong_lex_winner",
    "wrong_direct_scalar", "wrong_pair_count", "stale_epoch",
    "worker_failure_accepted", "incomplete_batch_checkpointed",
    "single_process_true", "worker_count_outside_range", "pid_replacement",
    "dishonest_rss",
)
FALSE_CLAIMS = {
    "common_word": False,
    "separator": False,
    "finite_common_word": False,
    "cofinal_lift": False,
    "fake": False,
    "ihara_witness": False,
}

V3_PINS = {
    "producer": ("search/d972_r07_normalized_exact_common_word_cached_v3.py",
                 193704,
                 "f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37"),
    "checker": ("crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py",
                154009,
                "dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10"),
    "driver": ("search/d972_r07_normalized_exact_common_word_cached_gha_driver_v3.g",
               11548,
               "2f7ff7b459e46d014268907ff5ba5f03c035836e8f8df79a2c5f4cdc3b75351d"),
    "fixture": ("search/certs/d972_r07_normalized_exact_common_word_cached_selftest_v3_20260827.json",
                276,
                "c49f434ad3daf1cc661ba45563dbb9557d436f91dca78c8ee0f47ed70332da12"),
}
V5_PINS = {
    "producer": ("search/d972_r07_normalized_exact_common_word_parallel_v5.py",
                 39234,
                 "19a2970fcf072c25c606d0305fd999c8481353e0be20879de4be2aa26f6fb90c"),
    "checker": ("crosscheck/check_d972_r07_normalized_exact_common_word_parallel_v5.py",
                32486,
                "530d67c854017a538fa2185b8bc5c48834a785f5bd6db38452db3551695cf1df"),
    "driver": ("search/d972_r07_normalized_exact_common_word_parallel_gha_driver_v5.g",
               7971,
               "0ac1b26d1844fdc16cc2701c536f50fd5415a7ef2479e030ebde96af79af4902"),
    "fixture": ("search/certs/d972_r07_normalized_exact_common_word_parallel_selftest_v5_20260828.json",
                1195,
                "4d481ba84e3c452c79f344e66a0eea5322ec8b64c15a81f1a290c22ce18e3fc9"),
}
PROOF_PINS = {
    "v254": ("sol/proof_r07_frozen_dual_boundary_mapreduce_v254.md", 6195,
             "e9fc7a69525200e8e1c0e8152652229227877ba923378ade8afa199c4f4ee1a0"),
    "v255": ("sol/proof_r07_boundary_adapter_state_and_local_provenance_v255.md", 8814,
             "06c93c46b48b681e0316d302058b72bc0b76fe9d12888cde3f7e45dc3a93ffa0"),
    "v256": ("sol/audit_r07_task192_cumulative_pairs_and_persistent_pool_v256.md", 4790,
             "f5a0c6e625e5113e4213b62762267fc9a5437cafd9f9751e603b055c549c1251"),
}
TASK298_PIN = (
    "search/d972_r07_normalized_exact_common_word_cached_resume_gha_driver_v2.g",
    19682,
    "169da7aa149d68907abb435f380b9ec2994c2bc285c6a17f13431614a388f5ad",
)
CHECKPOINT_ZIP = (
    "ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip",
    5001811,
    "f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566",
)
CHECKPOINT_MANIFEST = (
    "ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json",
    1328,
    "6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302",
)
CHECKPOINT_MEMBER = "d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json"
CHECKPOINT_RAW_BYTES = 86368039
CHECKPOINT_RAW_SHA = "c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab"
ORDER_VERSION = "v3-descriptor-outer-support-insertion-expanded-pairs-v1"
F3_ENCODING = "integer-residue-mod-3-delete-zero"
WINNER_ORDER_VERSION = "(block,translation_blob,relator_index)"
RSS_POLICY = "parent_peak_bytes + sum(child_peak_bytes); unknown RSS stops"

SHARD_BODY_FIELDS = {
    "worker_id", "pid", "start", "stop", "count", "interval_digest",
    "epoch_digest", "pair_roster_digest", "partial", "contributors",
    "worker_failed", "rss_known", "rss_peak_bytes",
}
SHARD_FIELDS = SHARD_BODY_FIELDS | {"result_digest"}
RUN_BODY_FIELDS = {
    "worker_count", "epoch_digest", "pair_roster_digest", "pair_count",
    "cover", "shards", "completed_shard_count", "accumulator",
    "contributors", "selected_key", "selected_scalar", "direct_scalar",
    "batch_complete", "checkpoint_state", "physical",
}
RUN_FIELDS = RUN_BODY_FIELDS | {"merge_digest"}
SEMANTIC_FIELDS = (
    "schema", "status", "terminal", "fixture_digest", "parallel_boundary",
    "single_process", "driver_worker_count", "worker_counts", "case_names",
    "cases", "epochs", "pool", "monitor", "resource", "checkpoint_state",
    "claims",
)


class SemanticError(RuntimeError):
    pass


class InputStop(RuntimeError):
    pass


class AdapterResourceStop(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise SemanticError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def key_blob(value):
    return canonical(value).decode("ascii")


def f3(value):
    return int(value) % 3


def rss_self_bytes():
    try:
        value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        return value if os.uname().sysname == "Darwin" else value * 1024
    except (AttributeError, OSError, ValueError):
        return None


def public_dual(dual):
    if isinstance(dual, dict):
        return [[key.hex(), int(value)] for key, value in dual.items()]
    return copy.deepcopy(dual)


def dual_digest(dual):
    return digest_obj(public_dual(dual))


def intervals(total, worker_count):
    require(worker_count in WORKER_COUNTS, "worker count outside 2..4")
    require(type(total) is int and total >= worker_count,
            "expanded pair roster too short")
    return [[worker * total // worker_count,
             (worker + 1) * total // worker_count]
            for worker in range(worker_count)]


def interval_digest(pairs, start, stop):
    return digest_obj({
        "start": start,
        "stop": stop,
        "pair_indices": [pair["pair_index"] for pair in pairs[start:stop]],
        "slice_digest": digest_obj(pairs[start:stop]),
    })


def add_f3(left, right):
    result = dict(left)
    for blob, value in right.items():
        require(type(value) is int and value in (1, 2), "partial F3 value")
        total = (result.get(blob, 0) + value) % 3
        if total:
            result[blob] = total
        else:
            result.pop(blob, None)
    return {blob: result[blob] for blob in sorted(result)}


def fixture_key(pair):
    t = (int(pair["g"]) - int(pair["h"])) % 17
    return [int(pair["block"]), f"t{t:02d}", int(pair["relator_index"])]


def pair_key(pair, runtime=None, v1=None):
    if pair.get("mode") == "fixture":
        return fixture_key(pair)
    block = int(pair["block"])
    quotient = v1.group_for_block(runtime, block)
    h = v1.unpack_element(runtime, bytes.fromhex(pair["h_hex"]), block)
    g = v1.unpack_element(runtime, bytes.fromhex(pair["g_hex"]), block)
    translation = quotient.mul(g, quotient.inverse(h))
    require(quotient.mul(translation, h) == g, "t*h=g")
    return [block, v1.element_blob(runtime, translation).hex(),
            int(pair["relator_index"])]


def pair_contribution(pair):
    return f3(int(pair["base_coefficient"]) *
              int(pair["lambda_coefficient"]))


def contributor_record(pair):
    return {
        "pair_index": int(pair["pair_index"]),
        "component": int(pair["component"]),
        "g_hex": (pair["g_hex"] if "g_hex" in pair
                   else f"{int(pair['g']):02x}"),
        "h_hex": (pair["h_hex"] if "h_hex" in pair
                  else f"{int(pair['h']):02x}"),
        "lambda_coefficient": int(pair["lambda_coefficient"]),
        "base_coefficient": f3(pair["base_coefficient"]),
    }


def serial_projection(pairs, runtime=None, v1=None):
    accumulator = {}
    contributors = {}
    for pair in pairs:
        key = key_blob(pair_key(pair, runtime, v1))
        coefficient = pair_contribution(pair)
        if coefficient:
            total = (accumulator.get(key, 0) + coefficient) % 3
            if total:
                accumulator[key] = total
            else:
                accumulator.pop(key, None)
        contributors.setdefault(key, []).append(contributor_record(pair))
    accumulator = {key: accumulator[key] for key in sorted(accumulator)}
    contributors = {key: contributors[key] for key in sorted(contributors)}
    active = [json.loads(blob) for blob, value in accumulator.items() if value]
    selected = min(active, key=lambda value: (value[0], value[1], value[2])) \
        if active else None
    selected_blob = key_blob(selected) if selected is not None else None
    scalar = accumulator.get(selected_blob, 0) if selected_blob else 0
    return {
        "accumulator": accumulator,
        "contributors": contributors,
        "selected_key": selected,
        "selected_scalar": scalar,
        "direct_scalar": scalar,
        "pair_count": len(pairs),
    }


def shard_compute(task):
    """Process entry point; only its own slice and immutable state are read."""
    state = _WORKER_STATE
    if not isinstance(state, dict):
        raise AdapterResourceStop("worker state missing")
    require(isinstance(task, dict), "worker task shape")
    for field in ("worker_id", "epoch_digest", "pair_roster_digest", "start",
                  "stop", "count", "pairs"):
        require(field in task, "worker task binding:" + field)
    start, stop = int(task["start"]), int(task["stop"])
    pairs = task["pairs"]
    require(type(task["count"]) is int and task["count"] == stop - start,
            "worker task count")
    require(len(pairs) == task["count"], "worker slice count")
    require(digest_obj(pairs) == task["slice_digest"], "worker slice digest")
    partial = {}
    contributors = {}
    retain_contributors = bool(state.get("retain_contributors", False))
    runtime = state.get("runtime")
    v1 = state.get("v1")
    for pair in pairs:
        key = key_blob(pair_key(pair, runtime, v1))
        coefficient = pair_contribution(pair)
        if coefficient:
            total = (partial.get(key, 0) + coefficient) % 3
            if total:
                partial[key] = total
            else:
                partial.pop(key, None)
        if retain_contributors:
            contributors.setdefault(key, []).append(contributor_record(pair))
    partial = {key: partial[key] for key in sorted(partial)}
    if retain_contributors:
        contributors = {key: contributors[key] for key in sorted(contributors)}
    rss = rss_self_bytes()
    body = {
        "worker_id": int(task["worker_id"]),
        "pid": os.getpid(),
        "start": start,
        "stop": stop,
        "count": int(task["count"]),
        "interval_digest": task["interval_digest"],
        "epoch_digest": task["epoch_digest"],
        "pair_roster_digest": task["pair_roster_digest"],
        "partial": partial,
        "contributors": contributors,
        "worker_failed": False,
        "rss_known": rss is not None,
        "rss_peak_bytes": int(rss or 0),
    }
    return {**body, "result_digest": digest_obj(body)}


_WORKER_STATE = None
_ACTIVE_RUNTIME_ADAPTERS = []
_PRODUCTION_WORKER_COUNT = 2
_V3_MODULE = None
_V3_ORIGINAL_BOUNDARY_CACHE = None


class MonitorShim:
    """Small monitor with the v1 bump/check interface for SELFTEST."""
    def __init__(self, limit=5_700_000_000):
        self.started = time.monotonic()
        self.limits = {"wall_seconds": 600.0, "boundary_pairs": 8_000_000,
                       "rss_bytes": int(limit)}
        self.counters = {"boundary_pairs": 0}
        self.phase = "selftest"

    def check(self, phase):
        self.phase = phase
        elapsed = time.monotonic() - self.started
        if elapsed > self.limits["wall_seconds"]:
            raise AdapterResourceStop("wall_seconds")

    def bump(self, name, amount=1, phase=None):
        self.counters[name] = self.counters.get(name, 0) + int(amount)
        self.phase = phase or self.phase
        if self.counters[name] > self.limits.get(name, 1 << 62):
            raise AdapterResourceStop(name)

    def public(self):
        return {"phase": self.phase,
                "elapsed_seconds": time.monotonic() - self.started,
                "rss_bytes": int(rss_self_bytes() or 0),
                "limits": dict(self.limits), "counters": dict(self.counters),
                "single_process": False}


class PersistentPool:
    """One fork pool whose PIDs and immutable state survive every epoch."""
    def __init__(self, worker_count, state, monitor):
        require(os.name == "posix", "Linux fork pool required")
        require(worker_count in WORKER_COUNTS, "pool worker count")
        global _WORKER_STATE
        self.worker_count = int(worker_count)
        self.monitor = monitor
        self.created_count = 0
        self.close_count = 0
        self.join_count = 0
        self.closed = False
        self.terminated = False
        self.epoch_records = []
        self.retain_contributors = bool(
            state.get("retain_contributors", state.get("mode") == "fixture"))
        self._state = dict(state)
        self._state["retain_contributors"] = self.retain_contributors
        _WORKER_STATE = self._state
        context = multiprocessing.get_context("fork")
        self.pool = context.Pool(self.worker_count)
        self.created_count = 1
        try:
            self.pid_roster = [int(worker.pid) for worker in self.pool._pool
                               if worker.pid is not None]
            require(len(self.pid_roster) == self.worker_count and
                    len(set(self.pid_roster)) == self.worker_count,
                    "pool PID roster")
        except Exception:
            self.closed = True
            self.terminated = True
            self.close_count += 1
            try:
                self.pool.terminate()
            finally:
                self.pool.join()
                self.join_count += 1
            raise

    def _current_pids(self):
        return [int(worker.pid) for worker in self.pool._pool
                if worker.pid is not None]

    def _resource_gate(self, phase):
        self.monitor.check(phase)
        parent = rss_self_bytes()
        if parent is None:
            raise AdapterResourceStop("parent RSS unknown")
        return int(parent)

    def run(self, pairs, epoch_digest, pair_roster_digest, worker_count,
            merge_callback):
        require(not self.closed, "pool already closed")
        require(worker_count in WORKER_COUNTS and worker_count <= self.worker_count,
                "requested worker count")
        total = len(pairs)
        cover = intervals(total, worker_count)
        parent_before = self._resource_gate("positive_boundary_correlation")
        if self._current_pids() != self.pid_roster:
            raise AdapterResourceStop("PID replacement before launch")
        tasks = []
        for worker_id, (start, stop) in enumerate(cover):
            slice_pairs = pairs[start:stop]
            tasks.append({
                "worker_id": worker_id,
                "epoch_digest": epoch_digest,
                "pair_roster_digest": pair_roster_digest,
                "start": start,
                "stop": stop,
                "count": stop - start,
                "interval_digest": interval_digest(pairs, start, stop),
                "slice_digest": digest_obj(slice_pairs),
                "pairs": slice_pairs,
            })
        launch = time.monotonic()
        try:
            shards = self.pool.map(shard_compute, tasks, chunksize=1)
        except Exception as error:
            raise AdapterResourceStop("worker failure:" + type(error).__name__)
        parent_after = self._resource_gate("positive_boundary_correlation")
        if self._current_pids() != self.pid_roster:
            raise AdapterResourceStop("PID replacement after return")
        require(isinstance(shards, list) and len(shards) == worker_count,
                "missing shard")
        for worker_id, (shard, (start, stop)) in enumerate(zip(shards, cover)):
            require(isinstance(shard, dict) and set(shard) == SHARD_FIELDS,
                    "shard shape")
            require(shard["worker_id"] == worker_id and
                    shard["pid"] in self.pid_roster and
                    shard["start"] == start and shard["stop"] == stop and
                    shard["count"] == stop - start and
                    shard["interval_digest"] == interval_digest(pairs, start, stop) and
                    shard["epoch_digest"] == epoch_digest and
                    shard["pair_roster_digest"] == pair_roster_digest and
                    shard["worker_failed"] is False and
                    shard["rss_known"] is True,
                    "shard binding")
            body = {field: copy.deepcopy(shard[field])
                    for field in SHARD_BODY_FIELDS}
            require(shard["result_digest"] == digest_obj(body),
                    "shard result digest")
        pids = [int(shard["pid"]) for shard in shards]
        require(len(set(pids)) == worker_count, "workers did not execute in parallel")
        child_peaks = [int(shard["rss_peak_bytes"]) for shard in shards]
        require(all(value > 0 for value in child_peaks), "child RSS unknown")
        aggregate = parent_after + sum(child_peaks)
        limit = int(self.monitor.limits.get("rss_bytes", 5_700_000_000))
        if aggregate > limit:
            raise AdapterResourceStop("aggregate RSS cap")
        merged = merge_shards(
            pairs, shards, worker_count, merge_callback,
            retain_shards=self.retain_contributors)
        self.monitor.bump("boundary_pairs", total, "positive_boundary_correlation")
        elapsed = time.monotonic() - launch
        physical = {
            "process_parallel": True,
            "single_process": False,
            "pool_worker_count": self.worker_count,
            "requested_worker_count": worker_count,
            "worker_pids": pids,
            "stable_pid_roster": list(self.pid_roster),
            "pid_replacements": 0,
            "parent_peak_rss_bytes": max(parent_before, parent_after),
            "child_peak_rss_bytes": child_peaks,
            "aggregate_peak_rss_bytes": aggregate,
            "rss_known": True,
            "aggregate_rss_policy": RSS_POLICY,
            "wall_before_launch_checked": True,
            "wall_after_return_checked": True,
            "elapsed_seconds": elapsed,
        }
        merged["physical"] = physical
        merged["merge_digest"] = digest_obj({
            field: copy.deepcopy(merged[field]) for field in RUN_BODY_FIELDS})
        self.epoch_records.append({
            "epoch_digest": epoch_digest,
            "pair_roster_digest": pair_roster_digest,
            "pair_count": total,
            "worker_count": worker_count,
            "cover": copy.deepcopy(cover),
            "shard_metadata": [
                {"worker_id": shard["worker_id"], "pid": shard["pid"],
                 "start": shard["start"], "stop": shard["stop"],
                 "count": shard["count"],
                 "epoch_digest": shard["epoch_digest"],
                 "pair_roster_digest": shard["pair_roster_digest"],
                 "interval_digest": shard["interval_digest"],
                 "result_digest": shard["result_digest"],
                 "partial_digest": digest_obj(shard["partial"]),
                 "contributors_digest": digest_obj(shard["contributors"]),
                 "rss_peak_bytes": shard["rss_peak_bytes"],
                 "worker_failed": shard["worker_failed"],
                 "rss_known": shard["rss_known"]}
                for shard in shards],
            "physical": copy.deepcopy(physical),
            "selected_key": copy.deepcopy(merged["selected_key"]),
            "selected_scalar": merged["selected_scalar"],
            "direct_scalar": merged["direct_scalar"],
            "batch_complete": True,
        })
        return merged

    def close(self):
        if self.closed:
            return
        self.closed = True
        self.close_count += 1
        try:
            self.pool.close()
        finally:
            self.pool.join()
            self.join_count += 1

    def terminate(self):
        if self.closed:
            return
        self.closed = True
        self.terminated = True
        self.close_count += 1
        try:
            self.pool.terminate()
        finally:
            self.pool.join()
            self.join_count += 1

    def public(self):
        return {
            "created_count": self.created_count,
            "close_count": self.close_count,
            "join_count": self.join_count,
            "worker_count": self.worker_count,
            "stable_pid_roster": list(self.pid_roster),
            "epoch_count": len(self.epoch_records),
            "epoch_digests": [record["epoch_digest"]
                              for record in self.epoch_records],
            "aggregate_rss_policy": RSS_POLICY,
            "terminated": self.terminated,
        }


def merge_shards(pairs, shards, worker_count, merge_callback,
                 retain_shards=True):
    cover = intervals(len(pairs), worker_count)
    observed = [[shard.get("start"), shard.get("stop")] for shard in shards]
    require(observed == cover, "ordered exact shard cover")
    accumulator = {}
    contributors = {}
    returned = 0
    for shard, (start, stop) in zip(shards, cover):
        require(shard["count"] == stop - start, "shard count")
        returned += shard["count"]
        accumulator = add_f3(accumulator, shard["partial"])
        for blob, records in shard["contributors"].items():
            contributors.setdefault(blob, []).extend(copy.deepcopy(records))
    require(returned == len(pairs), "complete pair cover")
    if contributors:
        contributors = {blob: contributors[blob]
                        for blob in sorted(contributors)}
    selected = (min((json.loads(blob) for blob, value in accumulator.items()
                     if value), key=lambda value: (value[0], value[1], value[2]))
                if accumulator else None)
    scalar = accumulator.get(key_blob(selected), 0) if selected is not None else 0
    direct = merge_callback(selected, scalar)
    require((selected is None and scalar == direct == 0) or
            (selected is not None and scalar == direct and scalar in (1, 2)),
            "direct scalar")
    body = {
        "worker_count": worker_count,
        "epoch_digest": shards[0]["epoch_digest"],
        "pair_roster_digest": shards[0]["pair_roster_digest"],
        "pair_count": returned,
        "cover": cover,
        "shards": (copy.deepcopy(shards) if retain_shards else []),
        "completed_shard_count": worker_count,
        "accumulator": accumulator,
        "contributors": contributors,
        "selected_key": selected,
        "selected_scalar": scalar,
        "direct_scalar": direct,
        "batch_complete": True,
        "checkpoint_state": None,
    }
    return {**body, "merge_digest": digest_obj(body)}


def expected_fixture():
    return {
        "schema": FIXTURE_SCHEMA,
        "case_names": list(CASE_NAMES),
        "epoch_runs": 3,
        "worker_counts": list(WORKER_COUNTS),
        "mutation_names": list(MUTATIONS),
        "parallel_boundary": True,
        "single_process": False,
        "expanded_pair_sharding": True,
        "case_expectations": {
            "active_two_shards": {
                "selected_key": [1, "t01", 1],
                "selected_scalar": 1,
                "w2_crosses_cut": True,
                "typed_support_concentrated_under_descriptor": True,
            },
            "cancel_across_shards": {
                "selected_key": [2, "t01", 2],
                "selected_scalar": 1,
                "cancelled_key": [1, "t01", 1],
            },
            "nontrivial_lex_winner": {
                "selected_key": [1, "t01", 2],
                "selected_scalar": 1,
                "competing_key": [1, "t02", 1],
            },
            "no_active_key": {"selected_key": None, "selected_scalar": 0},
        },
        "claims": copy.deepcopy(FALSE_CLAIMS),
    }


def load_fixture(path_value):
    path = Path(path_value)
    require(not path.is_absolute() and ".." not in path.parts and
            (path.as_posix().startswith("search/certs/") or
             path.as_posix().startswith("ci/in/")), "fixture path")
    value = json.loads((ROOT / path).read_text(encoding="ascii"))
    require(value == expected_fixture(), "fixture contract")
    return value


def fixture_descriptors(name):
    def descriptor(index, block, relator, component, h, base=1):
        return {"descriptor_index": index, "block": block,
                "relator_index": relator, "component": component, "h": h,
                "base_coefficient": base}

    if name == "active_two_shards":
        descriptors = [descriptor(0, 1, 1, 1, 2),
                       descriptor(1, 1, 2, 2, 4),
                       descriptor(2, 2, 1, 3, 6),
                       descriptor(3, 2, 2, 4, 8)]
        dual = [{"block": 1, "component": 1, "g": value,
                 "lambda_coefficient": 1}
                for value in (3, 5, 7, 9, 11, 20, 15, 0)]
    elif name == "cancel_across_shards":
        descriptors = [descriptor(0, 1, 1, 1, 2, 1),
                       descriptor(1, 2, 2, 3, 5, 1),
                       descriptor(2, 1, 1, 2, 3, 2),
                       descriptor(3, 2, 2, 4, 6, 0)]
        dual = [{"block": 1, "component": 1, "g": 3,
                 "lambda_coefficient": 1},
                {"block": 1, "component": 2, "g": 4,
                 "lambda_coefficient": 1},
                {"block": 2, "component": 3, "g": 6,
                 "lambda_coefficient": 1},
                {"block": 2, "component": 4, "g": 7,
                 "lambda_coefficient": 1}]
    elif name == "nontrivial_lex_winner":
        descriptors = [descriptor(0, 1, 2, 1, 2),
                       descriptor(1, 1, 1, 2, 2),
                       descriptor(2, 2, 1, 3, 4),
                       descriptor(3, 2, 2, 4, 5)]
        dual = [{"block": 1, "component": 1, "g": 3,
                 "lambda_coefficient": 1},
                {"block": 1, "component": 2, "g": 4,
                 "lambda_coefficient": 1},
                {"block": 2, "component": 3, "g": 5,
                 "lambda_coefficient": 0},
                {"block": 2, "component": 4, "g": 6,
                 "lambda_coefficient": 0}]
    elif name == "no_active_key":
        descriptors = [descriptor(0, 1, 1, 1, 2, 1),
                       descriptor(1, 1, 1, 2, 3, 2),
                       descriptor(2, 2, 1, 3, 4, 1),
                       descriptor(3, 2, 1, 4, 5, 2)]
        dual = [{"block": 1, "component": 1, "g": 3,
                 "lambda_coefficient": 1},
                {"block": 1, "component": 2, "g": 4,
                 "lambda_coefficient": 1},
                {"block": 2, "component": 3, "g": 5,
                 "lambda_coefficient": 1},
                {"block": 2, "component": 4, "g": 6,
                 "lambda_coefficient": 1}]
    else:
        raise SemanticError("unknown fixture case")
    return descriptors, dual


def fixture_pairs(descriptors, dual):
    support = {}
    for index, record in enumerate(dual):
        support.setdefault((record["block"], record["component"]), []).append(
            {"support_index": index, **record})
    pairs = []
    for descriptor in descriptors:
        for record in support.get((descriptor["block"], descriptor["component"]), []):
            index = len(pairs)
            pairs.append({
                "mode": "fixture", "pair_index": index,
                "descriptor_index": descriptor["descriptor_index"],
                "support_index": record["support_index"],
                "block": descriptor["block"],
                "relator_index": descriptor["relator_index"],
                "component": descriptor["component"],
                "h": descriptor["h"], "g": record["g"],
                "base_coefficient": descriptor["base_coefficient"],
                "lambda_coefficient": record["lambda_coefficient"],
            })
    require(pairs and len(pairs) >= 4, "fixture expanded pair roster")
    return pairs


def fixture_epoch_pairs(descriptors, dual):
    return fixture_pairs(descriptors, dual)


def fixture_merge_callback(_selected, scalar):
    return scalar


def make_fixture_run(controller, descriptors, dual, worker_count):
    pairs = fixture_pairs(descriptors, dual)
    epoch_identity = {
        "dual_digest": dual_digest(dual),
        "descriptor_digest": digest_obj(descriptors),
        "typed_support_digest": digest_obj(dual),
        "pair_roster_digest": digest_obj(pairs),
        "pair_count": len(pairs), "pair_order_version": ORDER_VERSION,
        "field": F3_ENCODING, "winner_order_version": WINNER_ORDER_VERSION,
    }
    result = controller.run(
        pairs, digest_obj(epoch_identity), digest_obj(pairs), worker_count,
        fixture_merge_callback)
    serial = serial_projection(pairs)
    require({field: result[field] for field in (
        "accumulator", "contributors", "selected_key", "selected_scalar",
        "direct_scalar", "pair_count")} == serial,
            "fixture parallel serial parity")
    result["epoch_identity"] = epoch_identity
    result["descriptors"] = copy.deepcopy(descriptors)
    result["dual"] = copy.deepcopy(dual)
    result["serial"] = serial
    result["local_winner_contributors"] = copy.deepcopy(
        result["contributors"].get(key_blob(result["selected_key"]), [])
        if result["selected_key"] is not None else [])
    result["pair_roster"] = copy.deepcopy(pairs)
    return result


def fixture_case_outcome(name, serial, descriptors):
    expected = expected_fixture()["case_expectations"][name]
    require(expected["selected_key"] == serial["selected_key"] and
            expected["selected_scalar"] == serial["selected_scalar"],
            "fixture expected serial outcome")
    if name == "active_two_shards":
        pairs = fixture_pairs(descriptors, fixture_descriptors(name)[1])
        cut = intervals(len(pairs), 2)[0][1]
        indices = [item["pair_index"] for item in serial["contributors"].get(
            key_blob(expected["selected_key"]), [])]
        require(any(index < cut for index in indices) and
                any(index >= cut for index in indices), "expanded w2 crossing")
    if name == "cancel_across_shards":
        cancelled = key_blob(expected["cancelled_key"])
        require(cancelled not in serial["accumulator"], "cancellation survived")
        pairs = fixture_pairs(descriptors, fixture_descriptors(name)[1])
        cut = intervals(len(pairs), 2)[0][1]
        indices = [item["pair_index"] for item in serial["contributors"].get(
            cancelled, [])]
        require(any(index < cut for index in indices) and
                any(index >= cut for index in indices),
                "cross-shard cancellation")
    if name == "nontrivial_lex_winner":
        require(key_blob(expected["competing_key"]) in serial["accumulator"] and
                expected["selected_key"][1] < expected["competing_key"][1] and
                expected["selected_key"][2] > expected["competing_key"][2],
                "nontrivial v3 lex order")
    return copy.deepcopy(expected)


def build_cases(controller):
    cases = []
    for name in CASE_NAMES:
        descriptors, dual = fixture_descriptors(name)
        pairs = fixture_pairs(descriptors, dual)
        serial = serial_projection(pairs)
        outcome = fixture_case_outcome(name, serial, descriptors)
        runs = {str(worker_count): make_fixture_run(
            controller, descriptors, dual, worker_count)
            for worker_count in WORKER_COUNTS}
        cases.append({"name": name, "descriptors": descriptors, "dual": dual,
                      "pair_roster": pairs, "serial": serial, "runs": runs,
                      "outcome": outcome})
    return cases


def epoch_dual(index):
    base = [{"block": 1, "component": 1, "g": value,
             "lambda_coefficient": coefficient}
            for value, coefficient in zip(
                (3, 5, 7, 9, 11, 13, 15, 0),
                ((1, 1, 1, 1, 1, 1, 1, 1) if index == 1 else
                 (2, 2, 2, 2, 2, 2, 2, 2) if index == 2 else
                 (1, 2, 1, 2, 1, 2, 1, 2)))]
    return base


def build_epochs(controller, worker_count):
    descriptors, _ = fixture_descriptors("active_two_shards")
    runs = []
    for index in (1, 2, 3):
        dual = epoch_dual(index)
        run = make_fixture_run(controller, descriptors, dual, worker_count)
        runs.append({"epoch_index": index, "dual": dual,
                     "serial": run["serial"], "parallel": run})
    digests = [digest_obj(run["parallel"]["epoch_identity"]) for run in runs]
    isolated = (len(set(digests)) == 3 and
                all(run["parallel"]["serial"] == run["serial"] for run in runs))
    require(isolated, "epoch state isolation")
    return {"runs": runs, "state_isolated": isolated,
            "epoch_digests": digests,
            "isolation_digest": digest_obj({"runs": runs,
                                             "state_isolated": isolated})}


def semantic_payload(receipt):
    return {field: copy.deepcopy(receipt[field]) for field in SEMANTIC_FIELDS
            if field in receipt}


def reseal(receipt):
    receipt.pop("input_digest", None)
    receipt["input_digest"] = digest_obj(semantic_payload(receipt))
    receipt.pop("self_digest_sha256", None)
    receipt["self_digest_sha256"] = digest_obj(receipt)


def check_seal(receipt):
    require(isinstance(receipt, dict), "receipt object")
    claimed = receipt.get("self_digest_sha256")
    body = dict(receipt)
    body.pop("self_digest_sha256", None)
    require(isinstance(claimed, str) and claimed == digest_obj(body),
            "receipt seal")


def expected_monitor(cases, epochs):
    case_pairs = sum(case["runs"]["2"]["pair_count"] for case in cases)
    case_runs = sum(len(case["runs"]) for case in cases)
    epoch_pairs = sum(run["parallel"]["pair_count"]
                      for run in epochs["runs"])
    return {
        "parallel_boundary": True, "single_process": False,
        "worker_counts_exercised": list(WORKER_COUNTS),
        "completed_batch_count": case_runs + len(epochs["runs"]),
        "completed_shard_count": 9 * len(cases) +
                                 sum(run["parallel"]["completed_shard_count"]
                                     for run in epochs["runs"]),
        "total_pair_count": case_pairs * 3 + epoch_pairs,
        "boundary_pairs": case_pairs * 3 + epoch_pairs,
        "worker_failures": 0, "aggregate_rss_policy": RSS_POLICY,
    }


def validate_shard(shard, pairs, epoch_digest, pair_roster_digest, start, stop):
    require(isinstance(shard, dict) and set(shard) == SHARD_FIELDS,
            "shard fields")
    expected = {
        "worker_id": shard["worker_id"], "pid": shard["pid"],
        "start": start, "stop": stop, "count": stop - start,
        "interval_digest": interval_digest(pairs, start, stop),
        "epoch_digest": epoch_digest, "pair_roster_digest": pair_roster_digest,
        "partial": {}, "contributors": {}, "worker_failed": False,
        "rss_known": True, "rss_peak_bytes": shard["rss_peak_bytes"],
    }
    for pair in pairs[start:stop]:
        blob = key_blob(pair_key(pair))
        coefficient = pair_contribution(pair)
        if coefficient:
            total = (expected["partial"].get(blob, 0) + coefficient) % 3
            if total:
                expected["partial"][blob] = total
            else:
                expected["partial"].pop(blob, None)
        expected["contributors"].setdefault(blob, []).append(
            contributor_record(pair))
    expected["partial"] = {key: expected["partial"][key]
                            for key in sorted(expected["partial"])}
    expected["contributors"] = {key: expected["contributors"][key]
                                 for key in sorted(expected["contributors"])}
    require(shard == {**expected, "result_digest": digest_obj(expected)},
            "direct shard replay")


def validate_fixture_run(run, descriptors, dual, worker_count):
    pairs = fixture_pairs(descriptors, dual)
    identity = {
        "dual_digest": dual_digest(dual),
        "descriptor_digest": digest_obj(descriptors),
        "typed_support_digest": digest_obj(dual),
        "pair_roster_digest": digest_obj(pairs), "pair_count": len(pairs),
        "pair_order_version": ORDER_VERSION, "field": F3_ENCODING,
        "winner_order_version": WINNER_ORDER_VERSION,
    }
    epoch = digest_obj(identity)
    require(set(run) == RUN_FIELDS | {"epoch_identity", "descriptors", "dual",
                                      "serial", "local_winner_contributors",
                                      "pair_roster"}, "run shape")
    require(run["worker_count"] == worker_count and
            run["epoch_digest"] == epoch and
            run["pair_roster_digest"] == digest_obj(pairs) and
            run["pair_count"] == len(pairs) and
            run["epoch_identity"] == identity and
            run["descriptors"] == descriptors and run["dual"] == dual and
            run["pair_roster"] == pairs and run["batch_complete"] is True and
            run["checkpoint_state"] is None, "run binding")
    cover = intervals(len(pairs), worker_count)
    require(run["cover"] == cover and len(run["shards"]) == worker_count,
            "run cover")
    for worker_id, (shard, (start, stop)) in enumerate(zip(run["shards"], cover)):
        require(shard["worker_id"] == worker_id, "worker id order")
        validate_shard(shard, pairs, epoch, digest_obj(pairs), start, stop)
    serial = serial_projection(pairs)
    require(run["serial"] == serial and
            {field: run[field] for field in (
                "accumulator", "contributors", "selected_key",
                "selected_scalar", "direct_scalar", "pair_count")} == serial,
            "run serial projection")
    require(run["local_winner_contributors"] == (
        run["contributors"].get(key_blob(run["selected_key"]), [])
        if run["selected_key"] is not None else []), "local winner")
    body = {field: copy.deepcopy(run[field]) for field in RUN_BODY_FIELDS}
    require(run["merge_digest"] == digest_obj(body), "merge digest")
    physical = run["physical"]
    require(physical["process_parallel"] is True and
            physical["single_process"] is False and
            physical["requested_worker_count"] == worker_count and
            len(physical["worker_pids"]) == worker_count and
            len(set(physical["worker_pids"])) == worker_count and
            physical["worker_pids"] == [shard["pid"] for shard in run["shards"]] and
            physical["rss_known"] is True and
            physical["parent_peak_rss_bytes"] > 0 and
            all(value > 0 for value in physical["child_peak_rss_bytes"]) and
            physical["aggregate_peak_rss_bytes"] ==
            physical["parent_peak_rss_bytes"] +
            sum(physical["child_peak_rss_bytes"]) and
            physical["aggregate_rss_policy"] == RSS_POLICY and
            physical["wall_before_launch_checked"] is True and
            physical["wall_after_return_checked"] is True,
            "physical process truth")


def validate_selftest_semantics(receipt, fixture, include_mutations=False):
    check_seal(receipt)
    require(set(receipt) == set(SEMANTIC_FIELDS) |
            {"input_digest", "mutation_controls", "self_digest_sha256"},
            "selftest envelope shape")
    require(receipt["schema"] == SELF_SCHEMA and receipt["status"] == "PASS" and
            receipt["terminal"] == PASS_TERMINAL and
            receipt["fixture_digest"] == digest_obj(fixture) and
            receipt["parallel_boundary"] is True and
            receipt["single_process"] is False and
            receipt["worker_counts"] == list(WORKER_COUNTS) and
            receipt["case_names"] == list(CASE_NAMES) and
            receipt["claims"] == FALSE_CLAIMS and
            receipt["checkpoint_state"] is None, "selftest boundary")
    require(receipt["input_digest"] == digest_obj(semantic_payload(receipt)),
            "semantic digest")
    cases = receipt["cases"]
    require([case.get("name") for case in cases] == list(CASE_NAMES),
            "case roster")
    for case in cases:
        descriptors, dual = fixture_descriptors(case["name"])
        require(case["descriptors"] == descriptors and case["dual"] == dual and
                case["pair_roster"] == fixture_pairs(descriptors, dual),
                "case fixture binding")
        serial = serial_projection(case["pair_roster"])
        require(case["serial"] == serial and
                case["outcome"] == fixture_case_outcome(
                    case["name"], serial, descriptors), "case serial")
        for worker_count in WORKER_COUNTS:
            validate_fixture_run(case["runs"][str(worker_count)], descriptors,
                                 dual, worker_count)
    epochs = receipt["epochs"]
    require(set(epochs) == {"runs", "state_isolated", "epoch_digests",
                             "isolation_digest"} and
            len(epochs["runs"]) == 3 and epochs["state_isolated"] is True and
            len(epochs["epoch_digests"]) == 3 and
            len(set(epochs["epoch_digests"])) == 3 and
            epochs["isolation_digest"] == digest_obj({
                "runs": epochs["runs"],
                "state_isolated": epochs["state_isolated"]}), "epoch envelope")
    for index, epoch in enumerate(epochs["runs"], 1):
        descriptors, _ = fixture_descriptors("active_two_shards")
        dual = epoch_dual(index)
        require(epoch["epoch_index"] == index and epoch["dual"] == dual and
                epoch["serial"] == serial_projection(fixture_pairs(descriptors, dual)),
                "epoch identity")
        validate_fixture_run(epoch["parallel"], descriptors, dual,
                             receipt["driver_worker_count"])
    require(receipt["monitor"] == expected_monitor(cases, epochs),
            "monitor counters")
    pool = receipt["pool"]
    require(pool["created_count"] == pool["close_count"] ==
            pool["join_count"] == 1 and pool["worker_count"] >= 2 and
            len(pool["stable_pid_roster"]) == pool["worker_count"] and
            len(set(pool["stable_pid_roster"])) == pool["worker_count"] and
            pool["aggregate_rss_policy"] == RSS_POLICY and
            pool["terminated"] is False, "persistent pool truth")
    resource_truth = receipt["resource"]
    require(resource_truth["rss_known"] is True and
            resource_truth["aggregate_rss_policy"] == RSS_POLICY and
            resource_truth["pool_created_once"] is True and
            resource_truth["pool_closed_once"] is True, "resource truth")
    if include_mutations:
        controls = receipt["mutation_controls"]
        require(controls["names"] == list(MUTATIONS) and
                controls["attempted"] == len(MUTATIONS) and
                controls["rejected"] == len(MUTATIONS) and
                len(controls["effects"]) == len(MUTATIONS),
                "mutation summary")


def refresh_shard(shard):
    body = {field: copy.deepcopy(shard[field]) for field in SHARD_BODY_FIELDS}
    shard["result_digest"] = digest_obj(body)


def refresh_run(run):
    body = {field: copy.deepcopy(run[field]) for field in RUN_BODY_FIELDS}
    run["merge_digest"] = digest_obj(body)


def apply_mutation(receipt, name):
    run = receipt["cases"][0]["runs"]["2"]
    if name == "omitted_shard":
        run["shards"].pop()
        run["cover"].pop()
    elif name == "duplicated_shard":
        run["shards"].append(copy.deepcopy(run["shards"][0]))
        run["cover"].append(copy.deepcopy(run["cover"][0]))
    elif name == "overlapping_interval":
        run["shards"][1]["start"] = run["shards"][0]["stop"] - 1
    elif name == "gap":
        run["shards"][1]["start"] = run["shards"][0]["stop"] + 1
    elif name == "permuted_pair_order":
        run["pair_roster"][0], run["pair_roster"][1] = (
            run["pair_roster"][1], run["pair_roster"][0])
    elif name == "wrong_dual_digest":
        run["shards"][0]["epoch_digest"] = "wrong:" + run["epoch_digest"]
    elif name == "wrong_descriptor_digest":
        run["pair_roster_digest"] = "wrong:" + run["pair_roster_digest"]
    elif name == "changed_coefficient":
        run["pair_roster"][0]["base_coefficient"] = 2
    elif name == "changed_translation_key":
        run["pair_roster"][0]["h"] += 1
    elif name == "changed_contributor":
        key = sorted(run["shards"][0]["contributors"])[0]
        run["shards"][0]["contributors"][key][0]["base_coefficient"] = 2
    elif name == "wrong_partial":
        run["shards"][0]["partial"][key_blob([1, "t00", 1])] = 1
    elif name == "wrong_mod3_merge":
        key = sorted(run["accumulator"])[0]
        run["accumulator"][key] = (run["accumulator"][key] % 2) + 1
    elif name == "zero_kept_active":
        run["accumulator"][key_blob([9, "t00", 9])] = 0
    elif name == "wrong_lex_winner":
        lex = receipt["cases"][2]["runs"]["2"]
        lex["selected_key"] = [1, "t02", 1]
        lex["selected_scalar"] = lex["accumulator"].get(key_blob(lex["selected_key"]), 0)
    elif name == "wrong_direct_scalar":
        run["direct_scalar"] = (run["direct_scalar"] + 1) % 3
    elif name == "wrong_pair_count":
        run["pair_count"] += 1
    elif name == "stale_epoch":
        receipt["epochs"]["runs"][1]["parallel"]["epoch_digest"] = \
            receipt["epochs"]["runs"][0]["parallel"]["epoch_digest"]
    elif name == "worker_failure_accepted":
        run["shards"][0]["worker_failed"] = True
    elif name == "incomplete_batch_checkpointed":
        run["batch_complete"] = False
        run["checkpoint_state"] = {"safe": True, "partial": True}
    elif name == "single_process_true":
        receipt["single_process"] = True
    elif name == "worker_count_outside_range":
        run["worker_count"] = 1
    elif name == "pid_replacement":
        run["physical"]["worker_pids"][0] += 1
    elif name == "dishonest_rss":
        run["physical"]["aggregate_peak_rss_bytes"] = 1
    else:
        raise SemanticError("unknown mutation")
    refresh_shard(run["shards"][0]) if run["shards"] else None
    refresh_run(run)


def mutation_effect_digest(receipt):
    return digest_obj(semantic_payload(receipt))


def run_mutations(baseline, fixture):
    baseline_digest = mutation_effect_digest(baseline)
    effects = []
    for name in MUTATIONS:
        mutant = copy.deepcopy(baseline)
        apply_mutation(mutant, name)
        reseal(mutant)
        mutant_digest = mutation_effect_digest(mutant)
        require(mutant_digest != baseline_digest, "mutation no-op:" + name)
        rejected = False
        reason = ""
        try:
            validate_selftest_semantics(mutant, fixture, include_mutations=False)
        except (SemanticError, KeyError, TypeError, ValueError) as error:
            rejected = True
            reason = type(error).__name__ + ":" + str(error)
        require(rejected, "mutation survived:" + name)
        effects.append({"name": name, "baseline_digest": baseline_digest,
                        "mutant_digest": mutant_digest, "rejected": True,
                        "reason_digest": digest_bytes(reason.encode("utf-8"))})
    return effects


def selftest(driver_worker_count, fixture_path):
    require(driver_worker_count in WORKER_COUNTS, "driver worker count")
    fixture = load_fixture(fixture_path)
    monitor = MonitorShim()
    pool = PersistentPool(max(4, driver_worker_count),
                           {"mode": "fixture", "runtime": None, "v1": None},
                           monitor)
    try:
        cases = build_cases(pool)
        epochs = build_epochs(pool, driver_worker_count)
        pool.close()
        pool_public = pool.public()
        monitor_public = expected_monitor(cases, epochs)
        resource_truth = {"rss_known": True, "aggregate_rss_policy": RSS_POLICY,
                          "pool_created_once": pool.created_count == 1,
                          "pool_closed_once": pool.close_count == 1 and
                          pool.join_count == 1,
                          "parent_peak_rss_bytes": int(rss_self_bytes() or 0)}
        receipt = {
            "schema": SELF_SCHEMA, "status": "PASS", "terminal": PASS_TERMINAL,
            "fixture_digest": digest_obj(fixture), "parallel_boundary": True,
            "single_process": False, "driver_worker_count": driver_worker_count,
            "worker_counts": list(WORKER_COUNTS), "case_names": list(CASE_NAMES),
            "cases": cases, "epochs": epochs, "pool": pool_public,
            "monitor": monitor_public, "resource": resource_truth,
            "checkpoint_state": None, "claims": copy.deepcopy(FALSE_CLAIMS),
            "mutation_controls": {"names": list(MUTATIONS), "attempted": 0,
                                   "rejected": 0, "effects": []},
        }
        reseal(receipt)
        validate_selftest_semantics(receipt, fixture)
        effects = run_mutations(receipt, fixture)
        receipt["mutation_controls"] = {
            "names": list(MUTATIONS), "attempted": len(effects),
            "rejected": sum(1 for effect in effects if effect["rejected"]),
            "effects": effects,
        }
        resource_truth["pool_closed_once"] = True
        receipt["resource"] = resource_truth
        reseal(receipt)
        validate_selftest_semantics(receipt, fixture, include_mutations=True)
        return receipt
    finally:
        pool.close()


def authenticate_pin(row):
    rel, size, expected = row
    path = ROOT / rel
    if not path.is_file():
        raise InputStop("missing:" + rel)
    raw = path.read_bytes()
    if len(raw) != size or digest_bytes(raw) != expected:
        raise InputStop("pin:" + rel)
    return raw


def authenticate_production_inputs(resume_value):
    if not resume_value:
        raise InputStop("resume:missing")
    for row in V3_PINS.values():
        authenticate_pin(row)
    for row in V5_PINS.values():
        authenticate_pin(row)
    for row in PROOF_PINS.values():
        authenticate_pin(row)
    authenticate_pin(TASK298_PIN)
    manifest_raw = authenticate_pin(CHECKPOINT_MANIFEST)
    zip_raw = authenticate_pin(CHECKPOINT_ZIP)
    manifest = json.loads(manifest_raw.decode("ascii"))
    require(manifest.get("zip", {}).get("member") == CHECKPOINT_MEMBER and
            manifest.get("raw_checkpoint", {}).get("bytes") == CHECKPOINT_RAW_BYTES and
            manifest.get("raw_checkpoint", {}).get("sha256") == CHECKPOINT_RAW_SHA,
            "checkpoint manifest identity")
    requested = Path(resume_value)
    require(not requested.is_absolute() and ".." not in requested.parts,
            "authenticated resume path")
    if requested.as_posix() in (CHECKPOINT_ZIP[0], CHECKPOINT_MANIFEST[0]):
        with zipfile.ZipFile(io.BytesIO(zip_raw), "r") as archive:
            members = [info for info in archive.infolist() if not info.is_dir()]
            require(len(members) == 1 and members[0].filename == CHECKPOINT_MEMBER,
                    "checkpoint one-member guard")
            raw_checkpoint = archive.read(members[0])
        require(len(raw_checkpoint) == CHECKPOINT_RAW_BYTES and
                digest_bytes(raw_checkpoint) == CHECKPOINT_RAW_SHA,
                "raw checkpoint authentication")
    elif (requested.as_posix().startswith("ci/out/") and
          len(requested.parts) == 3 and
          requested.name.endswith(".checkpoint.json")):
        sidecar = ROOT / requested
        if not sidecar.is_file():
            raise InputStop("resume:sidecar_missing")
        raw_checkpoint = sidecar.read_bytes()
        try:
            checkpoint = json.loads(raw_checkpoint.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise InputStop("resume:sidecar_json") from error
        require(isinstance(checkpoint, dict), "sidecar object")
        claimed = checkpoint.get("self_digest_sha256")
        body = dict(checkpoint)
        body.pop("self_digest_sha256", None)
        require(isinstance(claimed, str) and claimed == digest_obj(body),
                "sidecar seal")
    else:
        raise InputStop("resume:unsupported")
    return {"manifest": manifest, "zip_bytes": len(zip_raw),
            "zip_sha256": digest_bytes(zip_raw),
            "member": CHECKPOINT_MEMBER, "raw_bytes": CHECKPOINT_RAW_BYTES,
            "raw_sha256": CHECKPOINT_RAW_SHA,
            "resume": {"path": requested.as_posix(),
                       "bytes": len(raw_checkpoint),
                       "sha256": digest_bytes(raw_checkpoint)}}, raw_checkpoint


def load_authenticated_v3():
    path = ROOT / V3_PINS["producer"][0]
    spec = importlib.util.spec_from_file_location(
        "d972_cached_v3_authenticated_adapter_v4", path)
    if spec is None or spec.loader is None:
        raise InputStop("cached-v3 module loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RuntimeBoundaryDescriptorCache:
    """v3 descriptor cache with only correlation replaced by map/reduce."""
    def __init__(self, runtime, v1, original_translated):
        base = _V3_ORIGINAL_BOUNDARY_CACHE
        self._base = base(runtime, v1, original_translated)
        self.rt, self.v1 = runtime, v1
        self.original_translated = original_translated
        self.descriptors = self._base.descriptors
        self.rows = self._base.rows
        self.stats = self._base.stats
        self.input_digest = self._base.input_digest
        self.descriptor_public = self._base.public_descriptors()
        self.pool = None
        self.monitor = None
        self.epoch_records = []
        _ACTIVE_RUNTIME_ADAPTERS.append(self)

    def __getattr__(self, name):
        return getattr(self._base, name)

    def bind_input(self, digest):
        self.input_digest = digest
        self._base.bind_input(digest)

    def translated(self, block, index, translation_blob):
        return self._base.translated(block, index, translation_blob)

    def _support(self, dual):
        answer = {}
        ordered = []
        for key, coefficient in dual.items():
            if key[:1] != b"R":
                continue
            block, component, raw = self.v1.decode_row_key(key)
            record = {"g_hex": raw.hex(),
                      "lambda_coefficient": int(coefficient)}
            answer.setdefault((block, component), []).append(record)
            ordered.append({"type": [int(block), int(component)], **record})
        return answer, ordered

    def _pairs(self, dual):
        support, ordered = self._support(dual)
        pairs = []
        for descriptor_index, item in enumerate(self.descriptors):
            for support_index, record in enumerate(
                    support.get((item["block"], item["component"]), [])):
                pairs.append({
                    "mode": "runtime", "pair_index": len(pairs),
                    "descriptor_index": descriptor_index,
                    "support_index": support_index,
                    "block": int(item["block"]),
                    "relator_index": int(item["relator_index"]),
                    "component": int(item["component"]),
                    "h_hex": item["h_blob"].hex(),
                    "g_hex": record["g_hex"],
                    "base_coefficient": int(item["base_coefficient"]) % 3,
                    "lambda_coefficient": record["lambda_coefficient"],
                })
        return pairs, support, ordered

    def _callback(self, dual, selected, scalar):
        if selected is None:
            require(scalar == 0, "empty active scalar")
            return 0
        block, translation_hex, relator_index = selected
        translation_blob = bytes.fromhex(translation_hex)
        row = self.translated(block, relator_index, translation_blob)
        direct = self.v1.pair(dual, row)
        require(direct == scalar and direct != 0, "cached direct scalar")
        return direct

    def _local_provenance(self, dual, pairs, support, selected):
        if selected is None:
            return []
        block, translation_hex, relator_index = selected
        quotient = self.v1.group_for_block(self.rt, block)
        translation = self.v1.unpack_element(
            self.rt, bytes.fromhex(translation_hex), block)
        records = []
        for item in self.descriptors:
            if (item["block"], item["relator_index"]) != (block, relator_index):
                continue
            h = self.v1.unpack_element(self.rt, item["h_blob"], block)
            g = quotient.mul(translation, h)
            g_hex = self.v1.element_blob(self.rt, g).hex()
            for record in support.get((item["block"], item["component"]), []):
                if record["g_hex"] != g_hex:
                    continue
                t = quotient.mul(
                    self.v1.unpack_element(self.rt,
                                           bytes.fromhex(record["g_hex"]), block),
                    quotient.inverse(h))
                require(self.v1.element_blob(self.rt, t).hex() == translation_hex and
                        quotient.mul(t, h) ==
                        self.v1.unpack_element(self.rt,
                                               bytes.fromhex(record["g_hex"]), block),
                        "local t*h=g")
                records.append({
                    "component": int(item["component"]),
                    "g_hex": record["g_hex"], "h_hex": item["h_blob"].hex(),
                    "lambda_coefficient": int(record["lambda_coefficient"]),
                    "base_coefficient": int(item["base_coefficient"]) % 3,
                })
        return records

    def correlation(self, dual, monitor):
        self.monitor = monitor
        pairs, support, support_public = self._pairs(dual)
        require(pairs, "empty expanded boundary roster")
        descriptor_public = self.descriptor_public
        identity = {
            "dual_digest": dual_digest(dual),
            "descriptor_digest": digest_obj(descriptor_public),
            "typed_support_digest": digest_obj(support_public),
            "pair_roster_digest": digest_obj(pairs), "pair_count": len(pairs),
            "descriptor_count": len(self.descriptors),
            "pair_order_version": ORDER_VERSION, "field": F3_ENCODING,
            "winner_order_version": WINNER_ORDER_VERSION,
        }
        if self.pool is None:
            self.pool = PersistentPool(_PRODUCTION_WORKER_COUNT,
                                       {"mode": "runtime", "runtime": self.rt,
                                        "v1": self.v1}, monitor)
        digest = digest_obj(identity)
        try:
            merged = self.pool.run(
                pairs, digest, digest_obj(pairs), _PRODUCTION_WORKER_COUNT,
                lambda selected, scalar: self._callback(dual, selected, scalar))
        except AdapterResourceStop as error:
            limit = int(monitor.limits.get("rss_bytes", 5_700_000_000))
            raise self.v1.ResourceStop(
                "positive_boundary_correlation", "rss_bytes", limit + 1,
                limit) from error
        selected = merged["selected_key"]
        local = self._local_provenance(dual, pairs, support, selected)
        if self.pool.retain_contributors:
            merged_local = [dict(record) for record in merged["contributors"].get(
                key_blob(selected), [])] if selected is not None else []
            merged_local = [{key: value for key, value in record.items()
                             if key != "pair_index"} for record in merged_local]
            require(local == merged_local, "local winner provenance")
        parallel_meta = self.pool.epoch_records[-1]
        require(parallel_meta["epoch_digest"] == digest and
                parallel_meta["pair_roster_digest"] == digest_obj(pairs),
                "parallel epoch metadata")
        merged["local_winner_contributors"] = local
        merged["epoch_identity"] = identity
        self.epoch_records.append({
            "epoch_identity": identity,
            "epoch_digest": digest,
            "pair_count": len(pairs),
            "worker_count": _PRODUCTION_WORKER_COUNT,
            "descriptor_count": len(self.descriptors),
            "typed_support_count": len(support_public),
            "pair_roster_digest": digest_obj(pairs),
            "cover": copy.deepcopy(parallel_meta["cover"]),
            "shard_metadata": copy.deepcopy(parallel_meta["shard_metadata"]),
            "physical": copy.deepcopy(merged["physical"]),
            "batch_complete": True,
            "selected_key": copy.deepcopy(selected),
            "selected_scalar": merged["selected_scalar"],
            "direct_scalar": merged["direct_scalar"],
            "local_winner_digest": digest_obj({
                "selected_key": selected, "contributors": local}),
            "local_winner_contributors": copy.deepcopy(local),
        })
        if selected is None:
            require(not merged["accumulator"], "None with active coordinates")
            return None
        row = self.translated(selected[0], selected[2],
                              bytes.fromhex(selected[1]))
        return {"row": row, "provenance": {
            "family": "boundary", "block": selected[0],
            "base_relator_index": selected[2], "translation_hex": selected[1],
            "scalar": merged["selected_scalar"],
            "complete_support_occurrence_accumulation": True,
            "left_translation_gate": "t*h=g",
            "contributing_pairs": local,
        }}

    def close_pool(self):
        if self.pool is not None:
            self.pool.close()

    def pool_public(self):
        return None if self.pool is None else self.pool.public()


def production(resume_value, worker_count, args):
    global _V3_MODULE, _V3_ORIGINAL_BOUNDARY_CACHE, _PRODUCTION_WORKER_COUNT
    require(worker_count in WORKER_COUNTS, "production worker count")
    source, raw_checkpoint = authenticate_production_inputs(resume_value)
    _PRODUCTION_WORKER_COUNT = worker_count
    _V3_MODULE = load_authenticated_v3()
    original_cache = _V3_MODULE.BoundaryDescriptorCache
    _V3_ORIGINAL_BOUNDARY_CACHE = original_cache
    _V3_MODULE.BoundaryDescriptorCache = RuntimeBoundaryDescriptorCache
    target = ROOT / args.output
    with tempfile.TemporaryDirectory(prefix="d972-r07-v4-resume-") as temp:
        resume_path = Path(temp) / CHECKPOINT_MEMBER
        resume_path.write_bytes(raw_checkpoint)
        argv = ["--mode", "PRODUCTION", "--output", str(target),
                "--resume", str(resume_path), "--seconds", str(args.seconds),
                "--boundary-pairs", str(args.boundary_pairs),
                "--fibre-scans", str(args.fibre_scans),
                "--candidate-words", str(args.candidate_words),
                "--retained-columns", str(args.retained_columns),
                "--checkpoint-bytes", str(args.checkpoint_bytes),
                "--rss-bytes", str(args.rss_bytes),
                "--oracle-rounds", str(args.oracle_rounds)]
        captured = io.StringIO()
        try:
            with contextlib.redirect_stdout(captured):
                code = _V3_MODULE.main(argv)
            require(code == 0 and target.is_file(), "cached-v3 receipt missing")
            inner = json.loads(target.read_text(encoding="utf-8"))
        finally:
            runtime_pool_public = None
            runtime_epoch_records = []
            for adapter in list(_ACTIVE_RUNTIME_ADAPTERS):
                try:
                    adapter.close_pool()
                except Exception:
                    if adapter.pool is not None:
                        adapter.pool.terminate()
                if adapter.pool is not None:
                    runtime_pool_public = adapter.pool_public()
                runtime_epoch_records.extend(adapter.epoch_records)
            _ACTIVE_RUNTIME_ADAPTERS.clear()
            _V3_MODULE.BoundaryDescriptorCache = original_cache
    inner_digest = digest_obj(inner)
    sidecar_path = target.with_suffix(target.suffix + ".checkpoint.json")
    terminal = str(inner.get("terminal", UNKNOWN_ADAPTER))
    checkpoint = None
    if terminal.startswith("UNKNOWN_RESOURCE"):
        require(sidecar_path.is_file(), "resource stop missing safe checkpoint")
        raw = sidecar_path.read_bytes()
        checkpoint = {"path": sidecar_path.name, "bytes": len(raw),
                      "sha256": digest_bytes(raw), "sealed": True,
                      "adapter_safe": True, "epoch_restart_only": True}
    else:
        require(not sidecar_path.exists(), "COMMON retained checkpoint sidecar")
    pool_public = runtime_pool_public
    epoch_records = runtime_epoch_records
    if pool_public is None:
        pool_public = {"created_count": 0, "close_count": 0, "join_count": 0,
                       "worker_count": worker_count, "stable_pid_roster": [],
                       "epoch_count": 0, "epoch_digests": [],
                       "aggregate_rss_policy": RSS_POLICY, "terminated": False}
    outer = {
        "schema": PRODUCTION_SCHEMA, "status": inner.get("status", "UNKNOWN"),
        "terminal": terminal, "inner_terminal": terminal,
        "inner_receipt": inner, "inner_receipt_digest": inner_digest,
        "inner_single_process": inner.get("monitor", {}).get("single_process"),
        "inner_single_process_legacy_logical_only": True,
        "parallel_boundary": True, "single_process": False,
        "driver_worker_count": worker_count,
        "pool": pool_public,
        "epochs": epoch_records,
        "epoch_count": len(epoch_records),
        "epoch_digests": [digest_obj(record["epoch_identity"])
                          for record in epoch_records],
        "minimum_three_distinct_epochs": len({
            record["epoch_identity"]["dual_digest"] for record in epoch_records}) >= 3,
        "resource": {
            "aggregate_rss_policy": RSS_POLICY,
            "parent_peak_rss_bytes": max(
                [record["physical"]["parent_peak_rss_bytes"]
                 for record in epoch_records] or [0]),
            "rss_known": all(record["physical"]["rss_known"]
                              for record in epoch_records) if epoch_records else True,
            "wall_checks": all(record["physical"]["wall_before_launch_checked"] and
                                record["physical"]["wall_after_return_checked"]
                                for record in epoch_records) if epoch_records else True,
            "pool_created_once": pool_public["created_count"] == 1,
            "pool_closed_once": pool_public["close_count"] == 1 and
                                pool_public["join_count"] == 1,
        },
        "source_artifacts": source,
        "base_receipt_digest": inner_digest,
        "base_checkpoint_digest": (None if checkpoint is None else
                                    checkpoint["sha256"]),
        "checkpoint_state": checkpoint,
        "claims": copy.deepcopy(FALSE_CLAIMS),
    }
    reseal(outer)
    return outer


def sealed_stop(terminal, reason, worker_count):
    outer = {
        "schema": PRODUCTION_SCHEMA, "status": "UNKNOWN_INPUT",
        "terminal": terminal, "inner_terminal": terminal,
        "inner_receipt": None, "inner_receipt_digest": None,
        "inner_single_process": None,
        "inner_single_process_legacy_logical_only": True,
        "parallel_boundary": True, "single_process": False,
        "driver_worker_count": worker_count,
        "pool": {"created_count": 0, "close_count": 0, "join_count": 0,
                  "worker_count": worker_count, "stable_pid_roster": [],
                  "epoch_count": 0, "epoch_digests": [],
                  "aggregate_rss_policy": RSS_POLICY, "terminated": False},
        "epochs": [], "epoch_count": 0, "epoch_digests": [],
        "minimum_three_distinct_epochs": False,
        "resource": {"aggregate_rss_policy": RSS_POLICY, "rss_known": True,
                      "wall_checks": False, "pool_created_once": False,
                      "pool_closed_once": False},
        "source_artifacts": None, "base_receipt_digest": None,
        "base_checkpoint_digest": None,
        "checkpoint_state": None, "reason": reason,
        "claims": copy.deepcopy(FALSE_CLAIMS),
    }
    reseal(outer)
    return outer


def write_fresh(path_value, value):
    path = Path(path_value)
    require(not path.is_absolute() and path.as_posix().startswith("ci/out/") and
            ".." not in path.parts, "output path")
    target = ROOT / path
    require(not target.exists(), "stale output")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("xb") as stream:
        stream.write(canonical(value) + b"\n")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"),
                        default="PRODUCTION")
    parser.add_argument("--fixture", default=(
        "search/certs/"
        "d972_r07_normalized_exact_common_word_cached_parallel_selftest_v1_20260828.json"))
    parser.add_argument("--resume", default="")
    parser.add_argument("--boundary-workers", type=int, default=2)
    parser.add_argument("--seconds", type=int, default=10800)
    parser.add_argument("--boundary-pairs", type=int, default=8000000)
    parser.add_argument("--fibre-scans", type=int, default=80000000)
    parser.add_argument("--candidate-words", type=int, default=2000000)
    parser.add_argument("--retained-columns", type=int, default=250000)
    parser.add_argument("--checkpoint-bytes", type=int, default=4000000000)
    parser.add_argument("--rss-bytes", type=int, default=5700000000)
    parser.add_argument("--oracle-rounds", type=int, default=1)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    output_path = Path(args.output)
    checkpoint_path = output_path.with_suffix(
        output_path.suffix + ".checkpoint.json")
    if (output_path.is_absolute() or
            not output_path.as_posix().startswith("ci/out/") or
            ".." in output_path.parts or (ROOT / output_path).exists() or
            (ROOT / checkpoint_path).exists()):
        print(TERMINAL_PREFIX, UNKNOWN_RESUME, flush=True)
        return 2
    result = None
    code = 0
    try:
        require(args.boundary_workers in WORKER_COUNTS, "boundary worker range")
        if args.mode == "SELFTEST":
            result = selftest(args.boundary_workers, args.fixture)
        else:
            result = production(args.resume, args.boundary_workers, args)
    except (InputStop, SemanticError, AdapterResourceStop, OSError,
            UnicodeError, json.JSONDecodeError, zipfile.BadZipFile) as error:
        terminal = (UNKNOWN_RESUME if isinstance(error, InputStop) and
                    "resume" in str(error) else UNKNOWN_RESOURCE)
        result = sealed_stop(terminal, type(error).__name__ + ":" + str(error),
                             args.boundary_workers)
        code = 2 if args.mode == "SELFTEST" else 0
    except Exception as error:
        result = sealed_stop(UNKNOWN_ADAPTER,
                             type(error).__name__ + ":" + str(error),
                             args.boundary_workers)
        code = 0
    try:
        if args.mode == "PRODUCTION" and result.get("schema") == PRODUCTION_SCHEMA:
            target = ROOT / Path(args.output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(canonical(result) + b"\n")
        else:
            write_fresh(args.output, result)
    except (SemanticError, OSError):
        print(TERMINAL_PREFIX, UNKNOWN_RESUME, flush=True)
        return 2
    if args.mode == "SELFTEST" and code == 0 and result["terminal"] == PASS_TERMINAL:
        print(SELFTEST_MARKER, flush=True)
    print(TERMINAL_PREFIX, result["terminal"], flush=True)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
