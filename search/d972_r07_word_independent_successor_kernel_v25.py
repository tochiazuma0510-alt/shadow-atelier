#!/usr/bin/env python3
"""A4 v25: ordered physical resume and query-level live-dual repair."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
import types
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
V24 = ("search/d972_r07_word_independent_successor_kernel_v24.py", 34535,
       "8dc698e43fa7971dff4af3a5a19a7ac309ab5d43a19bb1f5189c0c222df01dfe")
V24_GENERATED = (285814, "9e3619f2e83dc7bea2e58d250bff3fafc24b8e09910c389b7a402a3b2d0d2d6a")
RESULT_GENERATED = (286439, "e4fb7ead7e1dcfc5806574481f1e83e008991e516de20e2eb3a67753fec03098")


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _need(value: object, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def _load_v24() -> bytes:
    path = ROOT / V24[0]; raw = path.read_bytes()
    _need(len(raw) == V24[1] and _sha(raw) == V24[2], "v25:v24_pin")
    ns: dict[str, Any] = {"__name__": "task512_v24_owner", "__file__": str(path),
                           "__package__": None, "__cached__": None}
    saved_argv = sys.argv[:]
    try:
        sys.argv = [str(path)]
        exec(compile(raw, str(path), "exec"), ns, ns)
    finally:
        sys.argv = saved_argv
    generated = ns.get("_SOURCE")
    _need(isinstance(generated, bytes) and len(generated) == V24_GENERATED[0] and
          _sha(generated) == V24_GENERATED[1], "v25:v24_generated_pin")
    return generated


_SOURCE = _load_v24()

# R1: physical state is installed only after ordinary checkpoint authentication
# and completed-counter installation.  The early cursor check remains.
_EARLY_RESTORE = b'''    if physical_store.shards:
        require(resume_state is not None and int(resume_state.get("next_row", 0)) == physical_store.next_row,
                "wire:physical_resume_binding")
        physical_store.direct_restore(oracle.basis, oracle, meter)
'''
_EARLY_RESTORE_NEW = b'''    if physical_store.shards:
        require(resume_state is not None and int(resume_state.get("next_row", 0)) == physical_store.next_row,
                "wire:physical_resume_binding")
'''
_need(_SOURCE.count(_EARLY_RESTORE) == 1, "v25:early_restore_cardinality")
_SOURCE = _SOURCE.replace(_EARLY_RESTORE, _EARLY_RESTORE_NEW, 1)

_INSTALL = b'''        meter.install_completed(meter.pending_completed_counters, dict(meter.restore_validation_counters),
                                meter.pending_saved_peak)
        meter._a4_completed_row = resume_row - 1
'''
_INSTALL_NEW = b'''        meter.install_completed(meter.pending_completed_counters, dict(meter.restore_validation_counters),
                                meter.pending_saved_peak)
        if physical_store.shards:
            physical_store.direct_restore(oracle.basis, oracle, meter)
        meter._a4_completed_row = resume_row - 1
'''
_need(_SOURCE.count(_INSTALL) == 1, "v25:install_restore_cardinality")
_SOURCE = _SOURCE.replace(_INSTALL, _INSTALL_NEW, 1)

# R2: one ordinary checkpoint live-dual entry is retained; shard dual events
# are restored once, but no physical batch creates another live-dual entry.
_LIVE_DUALS = b'''    for shard in store.shards:
        if isinstance(shard.get("dual_event"), dict): oracle.dual_chain.append(dict(shard["dual_event"]))
        query = shard.get("query", {}); oracle.live_duals.append({"query_id": query.get("query_id"),
            "dual": dict(shard.get("dual", [])), "target": dict(query.get("target", {})),
            "target_dot": shard.get("target_dot"), "correlation": dict(shard.get("correlation", {}))})
'''
_LIVE_DUALS_NEW = b'''    for shard in store.shards:
        if isinstance(shard.get("dual_event"), dict): oracle.dual_chain.append(dict(shard["dual_event"]))
'''
_need(_SOURCE.count(_LIVE_DUALS) == 1, "v25:live_dual_restore_cardinality")
_SOURCE = _SOURCE.replace(_LIVE_DUALS, _LIVE_DUALS_NEW, 1)

_RESTORE_FILES = b'''    out = cls(int(head.get("next_row", 27)), head_path.parent, head_path); previous = None; out._a4_pivots = set()
    for sequence in range(1, int(head.get("sequence", 0)) + 1):
'''
_RESTORE_FILES_NEW = b'''    out = cls(int(head.get("next_row", 27)), head_path.parent, head_path); previous = None; prior_semantic = None; out._a4_pivots = set()
    for sequence in range(1, int(head.get("sequence", 0)) + 1):
'''
_need(_SOURCE.count(_RESTORE_FILES) == 1, "v25:restore_file_anchor")
_SOURCE = _SOURCE.replace(_RESTORE_FILES, _RESTORE_FILES_NEW, 1)
_SEMANTIC_ANCHOR = b'''        require(seal_value == digest(body) and shard.get("sequence") == sequence and shard.get("previous") == previous,
                "wire:restore_shard_chain")
        chain = sha((str(previous) + digest({k: v for k, v in body.items() if k != "chain"})).encode("ascii"))
'''
_SEMANTIC_NEW = b'''        require(seal_value == digest(body) and shard.get("sequence") == sequence and shard.get("previous") == previous,
                "wire:restore_shard_chain")
        if prior_semantic is not None:
            require(shard.get("semantic_before") == prior_semantic, "wire:semantic_counter_order")
        prior_semantic = dict(shard.get("semantic_after", {}))
        chain = sha((str(previous) + digest({k: v for k, v in body.items() if k != "chain"})).encode("ascii"))
'''
_need(_SOURCE.count(_SEMANTIC_ANCHOR) == 1, "v25:semantic_order_anchor")
_SOURCE = _SOURCE.replace(_SEMANTIC_ANCHOR, _SEMANTIC_NEW, 1)

_LIVE_DUAL_RESUME = b'        oracle.live_duals = list(resume_state.get("live_duals", []))\n'
_LIVE_DUAL_RESUME_NEW = b'''        oracle.live_duals = list(resume_state.get("live_duals", []))
        require(len(oracle.live_duals) <= 1, "checkpoint:duplicate_live_dual")
'''
_need(_SOURCE.count(_LIVE_DUAL_RESUME) == 1, "v25:resume_live_dual_anchor")
_SOURCE = _SOURCE.replace(_LIVE_DUAL_RESUME, _LIVE_DUAL_RESUME_NEW, 1)
_DIRECT_POOL = b'''def _a4_wire_direct_restore(store: Any, basis: Any, oracle: Any, meter: Any) -> None:
    pool = _packed_pool_for(meter)
'''
_DIRECT_POOL_NEW = b'''def _a4_wire_direct_restore(store: Any, basis: Any, oracle: Any, meter: Any) -> None:
    require(len(oracle.live_duals) == 1, "wire:live_dual_history")
    pool = _packed_pool_for(meter)
'''
_need(_SOURCE.count(_DIRECT_POOL) == 1, "v25:direct_restore_anchor")
_SOURCE = _SOURCE.replace(_DIRECT_POOL, _DIRECT_POOL_NEW, 1)

# Task512a: commit changes in memory first.  The ordinary completed-row delta
# is durable before the physical HEAD can be atomically marked obsolete.
_COMMIT = b'''def _a4_wire_commit_dispatch(self: Any, terminal: dict[str, Any]) -> Any:
    self._a4_commit_calls = int(getattr(self, "_a4_commit_calls", 0)) + 1
    result = self._v430_commit(terminal)
    if self.root is not None and self.head_path is not None:
        self.head["next_row"] = self.next_row; self.head["open_query"] = None; self.head["obsolete"] = True
        self.head["self_digest_sha256"] = digest({k: v for k, v in self.head.items() if k != "self_digest_sha256"}); write_atomic(self.head_path, canon(self.head))
    return result
'''
_COMMIT_NEW = b'''def _a4_wire_commit_dispatch(self: Any, terminal: dict[str, Any]) -> Any:
    self._a4_commit_calls = int(getattr(self, "_a4_commit_calls", 0)) + 1
    return self._v430_commit(terminal)

def _a4_wire_publish_obsolete(self: Any) -> None:
    require(self.root is not None and self.head_path is not None and self.terminal is not None and
            self.open_query is None and self.head.get("obsolete") is True,
            "wire:obsolete_publish_state")
    self.head["next_row"] = self.next_row; self.head["open_query"] = None; self.head["obsolete"] = True
    self.head["self_digest_sha256"] = digest({k: v for k, v in self.head.items() if k != "self_digest_sha256"})
    write_atomic(self.head_path, canon(self.head))
'''
_need(_SOURCE.count(_COMMIT) == 1, "v25:commit_order_anchor")
_SOURCE = _SOURCE.replace(_COMMIT, _COMMIT_NEW, 1)
_ASSIGN_COMMIT = b'_A4PhysicalShardStore.commit = _a4_wire_commit_dispatch\n'
_ASSIGN_COMMIT_NEW = b'_A4PhysicalShardStore.commit = _a4_wire_commit_dispatch\n_A4PhysicalShardStore.publish_obsolete = _a4_wire_publish_obsolete\n'
_need(_SOURCE.count(_ASSIGN_COMMIT) == 1, "v25:obsolete_method_anchor")
_SOURCE = _SOURCE.replace(_ASSIGN_COMMIT, _ASSIGN_COMMIT_NEW, 1)
_CHECKPOINT = b'''        if checkpoint_path is not None and checkpoint_writes_enabled:
            write_checkpoint(checkpoint_path, authority, meter, ordinal + 1, oracle, words, queue, 0,
                             queue_phase_snapshot(queue, 0, actions, matrix, inverse_checks,
                                                  action_event_chain))
'''
_CHECKPOINT_NEW = b'''        if checkpoint_path is not None and checkpoint_writes_enabled:
            write_checkpoint(checkpoint_path, authority, meter, ordinal + 1, oracle, words, queue, 0,
                             queue_phase_snapshot(queue, 0, actions, matrix, inverse_checks,
                                                  action_event_chain))
        if ordinal >= 27 and physical_store.terminal is not None and physical_store.open_query is None:
            require(checkpoint_path is not None and checkpoint_writes_enabled, "wire:ordinary_before_obsolete")
            physical_store.publish_obsolete()
'''
_need(_SOURCE.count(_CHECKPOINT) == 1, "v25:checkpoint_order_anchor")
_SOURCE = _SOURCE.replace(_CHECKPOINT, _CHECKPOINT_NEW, 1)

if RESULT_GENERATED[0] and (len(_SOURCE) != RESULT_GENERATED[0] or _sha(_SOURCE) != RESULT_GENERATED[1]):
    raise RuntimeError("v25:generated_pin_drift")


def _tiny_entry(ns: dict[str, Any], index: int) -> dict[str, Any]:
    row = {"k:%d" % index: 1}; pivot = next(iter(row)); label = "B:%d" % index
    detail = {"pivot": pivot, "scale": 1, "row": row, "label": label,
              "reduction": {}, "row_digest": ns["digest"](row),
              "label_digest": ns["digest"](label)}
    raw = {"raw_key": "raw:%d" % index, "row": {"r:%d" % index: 1},
           "candidate": {"index": index}}
    ins = {"kind": "B", "label": label, "column": dict(raw["row"]),
           "raw_identity": raw["raw_key"], "boundary_row": dict(row),
           "boundary_pivot": pivot, "boundary_scale": 1,
           "boundary_reduction": {}, "combined_row": dict(row),
           "combined_detail": {"pivot": pivot, "scale": 1, "row": dict(row),
                               "reduction": {}, "relation": {}}
    }
    return {"kind": "B", "raw_identity": raw, "raw_digest": ns["digest"](raw["row"]),
            "boundary": dict(detail), "combined": dict(detail),
            "formals": {"boundary_reduction": {}, "combined_reduction": {},
                        "boundary_ledger": {}, "combined_ledger": {},
                        "b_coefficients": {}, "b_formals": [{}, {}]},
            "record": {"query_id": "R:27:B:%d" % index, "schema": "BOUNDARY_RANK_RISE"},
            "event": {"insertion": ins, "query": {"query_id": "R:27:B:%d" % index}},
            "epoch_before": "e%d" % index, "epoch_after": "e%d" % (index + 1)}


def _live_four_batch_fixture() -> dict[str, Any]:
    """Run generated build_kernel through CLI-shaped interruption/resume."""
    # The generated function is compiled unchanged except for a fixture-only
    # return after its real consume_row loop, so no production path is shortened.
    marker = b'''    for ordinal, row in enumerate(authority.rows[resume_row - 1:], resume_row):
        consume_row(ordinal, row)
    require(len(initial_terminals) == ROWS and len(row_digests) == ROWS and len(chunks) == 7,
'''
    replacement = b'''    for ordinal, row in enumerate(authority.rows[resume_row - 1:], resume_row):
        consume_row(ordinal, row)
    if _TASK512_FIXTURE_SHORT:
        return {"fixture_short": True, "physical_store": physical_store, "oracle": oracle}
    require(len(initial_terminals) == ROWS and len(row_digests) == ROWS and len(chunks) == 7,
'''
    _need(_SOURCE.count(marker) == 1, "v25:fixture_build_kernel_anchor")
    fixture_source = _SOURCE.replace(marker, replacement, 1)
    ns: dict[str, Any] = {"__name__": "task512_generated_fixture", "__file__": str(ROOT / V24[0])}
    exec(compile(fixture_source, str(ROOT / V24[0]), "exec"), ns, ns)
    stats: dict[str, Any] = {"phase": "interrupt", "direct_restore": 0,
                             "direct_restore_by_phase": {}, "restore_replay": 0,
                             "close": 0, "publish": 0, "publish_by_phase": {}}
    class FakeState:
        def identity_roof(self) -> bool: return True
    class FakeRuntime:
        actors: dict[tuple[int, int], Any] = {}
        def identity(self, index: int) -> FakeState: return FakeState()
        def row_from_states(self, states: Any) -> dict[str, int]: return {}
    class FakeForward:
        def __init__(self) -> None: self.nodes = list(range(15971))
        def add(self, word: Any) -> None: return None
    class FakeLedger:
        def __init__(self, runtime: Any, meter: Any) -> None:
            self.seeds = []; self.seed_by_context_relation = {}
    class FakeWordDAG:
        def __init__(self, runtime: Any, ledger: Any, meter: Any) -> None: self.nodes = []
    class FakeBasis:
        def __init__(self) -> None:
            E = types.SimpleNamespace(rows={}, labels={}, pivots=[])
            self.boundary = E; self.combined = E
            self.b_rows = {}; self.b_ledgers = {}; self.boundary_ledgers = {}; self.combined_ledgers = {}
            self.b_coefficients = {}; self.b_formals = {}; self.active_registry = types.SimpleNamespace(update=lambda x: None)
            self.insertion_events = []; self.k_items = []
        def rank(self) -> int: return 0
    class FakeOracle:
        def __init__(self, runtime: Any, ledger: Any, meter: Any, shard_store: Any = None) -> None:
            self.runtime, self.ledger, self.meter, self.shard_store = runtime, ledger, meter, shard_store
            self.basis = FakeBasis(); self.records = []; self.live_duals = [{"query_id": "R:27", "dual": {}}]
            self.event_chain = []; self.dual_chain = []; self.bridge_chain = []; self.epoch = "e0"
        def query(self, target: Any, discrepancy: Any, word: Any, query_id: str) -> dict[str, Any]:
            if self.shard_store.open_query is not None:
                if stats["phase"] == "interrupt":
                    for index in range(1, 4):
                        before = {} if index == 1 else {"q": index - 1}; after = {"q": index}
                        self.shard_store.close_batch({"m": 1, "candidates": [{"raw_identity": "c:%d" % index, "coefficient": 1}],
                            "accepted_mask": [1], "entries": [_tiny_entry(ns, index)], "dual": [], "dual_digest": "d" * 64,
                            "dual_event": {"index": index, "query_id": query_id, "digest": "d" * 64},
                            "target_dot": {}, "correlation": {}, "before": {"boundary_rank": 0, "combined_rank": 0, "records": 0, "events": 0, "duals": index - 1, "semantic": before},
                            "after": {"boundary_rank": 0, "combined_rank": 0, "records": 0, "events": 0, "duals": index},
                            "epoch_before": "e%d" % (index - 1), "epoch_after": "e%d" % index,
                            "semantic_before": before, "semantic_after": after})
                    stats["close"] += 3
                    raise ns["ResourceStop"]("FIXTURE", "interrupt", 1, 2, "QUERY")
                index = 4; before = dict(self.shard_store.shards[-1]["semantic_after"]); stats["fourth_before"] = dict(before); after = {"q": 4}
                self.shard_store.close_batch({"m": 1, "candidates": [{"raw_identity": "c:4", "coefficient": 1}],
                    "accepted_mask": [1], "entries": [_tiny_entry(ns, index)], "dual": [], "dual_digest": "d" * 64,
                    "dual_event": {"index": index, "query_id": query_id, "digest": "d" * 64},
                    "target_dot": {}, "correlation": {}, "before": {"boundary_rank": 0, "combined_rank": 0, "records": 0, "events": 0, "duals": 3, "semantic": before},
                    "after": {"boundary_rank": 0, "combined_rank": 0, "records": 0, "events": 0, "duals": 4},
                    "epoch_before": "e3", "epoch_after": "e4", "semantic_before": before, "semantic_after": after})
                stats["close"] += 1
                return {"schema": "MEMBER", "query_id": query_id, "rank": 0}
            return {"schema": "MEMBER", "query_id": query_id, "rank": 0}
    class FakeAuthority:
        def __init__(self, args: Any, meter: Any) -> None:
            self.identity = "task512-fixture-authority"; self.rows = [{"layer": "normal"} for _ in range(27)]; self.receipt = {}
    ns.update({"BoundaryLedger": FakeLedger, "Oracle": FakeOracle, "WordDAG": FakeWordDAG,
               "replay_ancestry": lambda row: ([], [], []),
               "bridge_trace_from_states": lambda *args: {"bridge_trace_digest": "b" * 64},
               "progress_once": lambda *args, **kwargs: None, "AuthorityAdapter": FakeAuthority,
               "ForwardDAG": FakeForward, "restore_word_dag": lambda *args: None,
               "restore_basis": lambda *args: None, "validate_queue_prefix": lambda *args: None,
               "queue_phase_snapshot": lambda *args: {}, "checkpoint_payload": lambda *args: {"rebuild_digest": "x"},
               "write_atomic": lambda path, raw: (path.parent.mkdir(parents=True, exist_ok=True), path.write_bytes(raw))[1],
               "write_checkpoint": lambda path, *args: (_ for _ in ()).throw(OSError("fixture:ordinary_write_failed")) if stats.get("phase") == "fail_ordinary" else path.write_bytes(b"ordinary-checkpoint"),
               "_TASK512_FIXTURE_SHORT": True})
    _publish = ns["_A4PhysicalShardStore"].publish_obsolete
    def measured_publish(store: Any) -> None:
        stats["publish"] += 1
        phase = stats["phase"]
        stats["publish_by_phase"][phase] = stats["publish_by_phase"].get(phase, 0) + 1
        return _publish(store)
    ns["_A4PhysicalShardStore"].publish_obsolete = measured_publish
    resume_state = {"next_row": 27, "word_ledger_dag": [], "boundary_echelon": {}, "echelon_rebuild": {},
                    "insertion_events": [], "B_roster": {}, "B_ledgers": {}, "boundary_ledgers": {},
                    "combined_ledgers": {}, "B_coefficients": {}, "B_formals": {}, "K_roster": [],
                    "oracle_records": [], "live_duals": [{"query_id": "R:27", "dual": {}}],
                    "query_event_chain": [], "dual_event_chain": [], "epoch_digest": "e0",
                    "bridge_digests": ["b" * 64] * 26, "row_digests": ["r" * 64] * 26,
                    "row_chunks": [], "initial_terminal_records": [], "samples": [], "sample_rows": {},
                    "queue_phase": {}, "queue": [], "queue_head": 0, "_delta_transport": True, "_delta_meta": {}}
    with tempfile.TemporaryDirectory(prefix="task512_") as td:
        root = Path(td) / "physical"; head = root / "HEAD"; ordinary = Path(td) / "ordinary.head.checkpoint.json"
        def fake_actual(authority: Any, meter: Any, checkpoint: Any = None, resume_state_arg: Any = None,
                        physical_root: Any = None, physical_head: Any = None) -> dict[str, Any]:
            meter.pending_completed_counters = dict(meter.semantic_counters); meter.pending_saved_validation = {}; meter.pending_saved_peak = dict(meter.peak_counters)
            try:
                result = ns["build_kernel"](authority, FakeRuntime(), FakeForward(), [], {}, meter, ordinary, resume_state,
                                             root, head)
                calls = int(getattr(meter, "_a4_direct_restore_calls", 0))
                stats["direct_restore"] += calls
                phase = stats["phase"]
                stats["direct_restore_by_phase"][phase] = (
                    stats["direct_restore_by_phase"].get(phase, 0) + calls)
                stats["resume_oracle"] = result["oracle"]
                stats["resume_meter"] = meter
                return result
            except Exception as exc:
                stats["error"] = type(exc).__name__ + ":" + str(exc)
                raise
        ns["actual_result"] = fake_actual; ns["exact_path"] = lambda *args: Path("C:/Temp/task512_fixture_resume.json")
        ns["restore_delta_chain"] = lambda *args: resume_state
        ns["_TASK512_FIXTURE_SHORT"] = True
        rc1 = ns["main"]([]); _need(rc1 == 0, "fixture:interrupt_route")
        _need(head.exists(), "fixture:three_shard_head:" + str(stats.get("error", "none")))
        live_root = Path(td) / "live_copy"; shutil.copytree(root, live_root)
        fail_root = Path(td) / "failure_copy"; shutil.copytree(live_root, fail_root)
        stats["phase"] = "fail_ordinary"; failure_head = fail_root / "HEAD"
        original_root, original_head = root, head; root, head = fail_root, failure_head
        rc_fail = ns["main"]([]); _need(rc_fail == 2, "fixture:ordinary_failure_route")
        failed_disk_head = json.loads(failure_head.read_text()); _need(failed_disk_head.get("obsolete") is False, "fixture:failure_disk_head_live")
        _need(stats.get("close") == 4 and stats["publish_by_phase"].get("fail_ordinary", 0) == 0,
              "fixture:failure_fourth_close")
        root, head = original_root, original_head
        stats["phase"] = "resume"; rc2 = ns["main"](["--resume", "fixture.json"]); _need(rc2 == 0, "fixture:resume_route:" + str(stats.get("error", "none")))
        _need(stats["close"] == 5, "fixture:four_closes")
        _need(stats["direct_restore_by_phase"].get("resume", 0) == 1,
              "fixture:direct_restore_counter")
        shards = [json.loads((root / ("shard.%08d.json" % i)).read_text()) for i in range(1, 4)]
        shard4 = json.loads((root / "shard.00000004.json").read_text())
        _need(shards[-1]["semantic_after"] == {"q": 3}, "fixture:third_after")
        # The fourth before value is generated from the restored third shard.
        _need(shard4.get("semantic_before") == shards[-1].get("semantic_after") and
              stats.get("fourth_before") == shard4.get("semantic_before"), "fixture:fourth_before_equals_third_after")
        _need(stats.get("close") == 5, "fixture:generated_oracle_callsite")
        _need(stats["publish_by_phase"].get("resume", 0) == 1,
              "fixture:normal_publish_count")
        restored_oracle = stats["resume_oracle"]
        uninterrupted_live_duals = [{"query_id": "R:27", "dual": {}}]
        _need(restored_oracle.live_duals == uninterrupted_live_duals, "fixture:live_dual_equality")
        _need(len(restored_oracle.dual_chain) == 3 and restored_oracle.epoch == "e3", "fixture:dual_epoch_equality")
        _need(len(restored_oracle.records) == 3 and len(restored_oracle.event_chain) == 3 and
              len(restored_oracle.basis.boundary.rows) == 3 and len(restored_oracle.basis.combined.rows) == 3 and
              len(restored_oracle.basis.b_formals) == 3, "fixture:restored_maps_events")
        broken_root = Path(td) / "counter_mutation"; shutil.copytree(live_root, broken_root)
        broken_path = broken_root / "shard.00000002.json"; broken = json.loads(broken_path.read_text())
        broken["semantic_before"] = {"q": 99}; broken_body = dict(broken); broken_body.pop("self_digest_sha256", None)
        broken["self_digest_sha256"] = ns["digest"](broken_body); broken_path.write_text(json.dumps(broken, sort_keys=True, separators=(",", ":")))
        try: ns["_A4PhysicalShardStore"].restore_files(broken_root / "HEAD")
        except Exception as exc: _need("semantic_counter_order" in str(exc), "fixture:counter_order_mutation_reason")
        else: raise RuntimeError("fixture:counter_order_mutation_accepted")
        dup = dict(resume_state); dup["live_duals"] = [{"query_id": "R:27", "dual": {}}, {"query_id": "R:27", "dual": {}}]
        meter = ns["Meter"](); meter.pending_completed_counters = dict(meter.semantic_counters); meter.pending_saved_validation = {}; meter.pending_saved_peak = dict(meter.peak_counters)
        try: ns["build_kernel"](FakeAuthority(None, meter), FakeRuntime(), FakeForward(), [], {}, meter, ordinary, dup, live_root, live_root / "HEAD")
        except Exception as exc: _need("duplicate_live_dual" in str(exc), "fixture:duplicate_live_dual_reason")
        else: raise RuntimeError("fixture:duplicate_live_dual_accepted")
        handoff = ns["_A4PhysicalShardStore"].restore_files(live_root / "HEAD"); handoff.terminal = {"query_id": "R:27"}; handoff.open_query = None; handoff.head["obsolete"] = True
        before = json.loads((live_root / "HEAD").read_text()); original_writer = ns["write_atomic"]
        ns["write_atomic"] = lambda path, raw: (_ for _ in ()).throw(OSError("fixture:ordinary_write_failed"))
        try: _publish(handoff)
        except OSError: pass
        finally: ns["write_atomic"] = original_writer
        disk_after_failure = json.loads((live_root / "HEAD").read_text())
        _need(disk_after_failure.get("obsolete") is False, "fixture:failure_keeps_live_head")
        _need(ordinary.exists(), "fixture:ordinary_checkpoint_written")
        _publish(handoff); disk_after_success = json.loads((live_root / "HEAD").read_text())
        _need(disk_after_success.get("obsolete") is True and
              stats["publish_by_phase"].get("resume", 0) == 1,
              "fixture:postordinary_obsolete:" + repr(disk_after_success) + ":" +
              repr(stats.get("publish")) + ":" + repr(stats.get("publish_by_phase")))
        ns["_delta_checkpoint_reference"] = lambda path, meter: {"kind": "delta_chain", "next_row": 28}
        _need(ns["checkpoint_reference"](ordinary, stats["resume_meter"]).get("kind") == "delta_chain", "fixture:ordinary_ref_kind")
        return {"generated_build_kernel": True, "cli_resume": True, "closed_shards": 3,
                "fourth_close": True, "semantic_order": True, "live_duals_preserved": True,
                "direct_restore_once": True, "restore_replay_calls": 0,
                "counter_order_mutation_rejected": True, "duplicate_live_dual_rejected": True,
                "completion_handoff_failure_safe": True, "completion_handoff_after_write": True}


def fixture() -> dict[str, Any]:
    return {"status": "PASS", "generated": {"bytes": len(_SOURCE), "sha256": _sha(_SOURCE)},
            "repair": {"ordered_restore_after_install": True, "query_live_dual_once": True,
                       "commit_before_ordinary_then_obsolete": True},
            "live_four_batch": _live_four_batch_fixture()}


if "--source-patch-info" in sys.argv[1:]:
    print(json.dumps({"owner": {"path": V24[0], "bytes": V24[1], "sha256": V24[2]},
                      "owner_generated": {"bytes": V24_GENERATED[0], "sha256": V24_GENERATED[1]},
                      "generated": {"bytes": len(_SOURCE), "sha256": _sha(_SOURCE)}},
                     sort_keys=True, separators=(",", ":")))
    raise SystemExit(0)
if "--fixture" in sys.argv[1:]:
    print(json.dumps(fixture(), sort_keys=True, separators=(",", ":"))); raise SystemExit(0)
exec(compile(_SOURCE, str(ROOT / V24[0]), "exec"), globals(), globals())
