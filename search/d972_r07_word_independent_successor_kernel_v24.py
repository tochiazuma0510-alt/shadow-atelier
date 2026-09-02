#!/usr/bin/env python3
"""A4 v24: v23 physical shards wired into the real row/query production path."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER = ("search/d972_r07_word_independent_successor_kernel_v23.py", 14472,
         "d9c082570cfa5c52254e159cd91ad0e722e5ad0ee1ea2c52e8161c2729ee1d9a")
OWNER_GENERATED = (266117, "d406f1128dc66bc526fe5babf0f9fee0b086d7fce348f1435a7516d8090b9ef6")
RESULT_GENERATED = (285814, "9e3619f2e83dc7bea2e58d250bff3fafc24b8e09910c389b7a402a3b2d0d2d6a")

_LIVE_RETURN_OLD = b'''        return {"label": label, "row": stored, "ledger": ledger_value, "pivot": cdetail["pivot"],
                "scale": scale, "raw_identity": raw_identity}
'''
_LIVE_RETURN_NEW = b'''        return {"label": label, "row": stored, "ledger": ledger_value, "pivot": cdetail["pivot"],
                "scale": scale, "raw_identity": raw_identity,
                "boundary_detail": {"pivot": bdetail["pivot"], "scale": bdetail["scale"],
                                    "row": bdetail["row"], "label": label,
                                    "reduction": dict(bdetail["reduction"])},
                "combined_detail": {"pivot": cdetail["pivot"], "scale": cdetail["scale"],
                                    "row": cdetail["row"], "label": label,
                                    "reduction": dict(cdetail["reduction"]),
                                    "relation": dict(cdetail["relation"])},
                "formals": {"boundary_ledger": dict(ledger_value),
                            "combined_ledger": dict(combined_ledger),
                            "b_coefficients": dict(combined_coefficients),
                            "b_formals": [dict(combined_ledger), dict(combined_coefficients)]}}
'''
_DUAL_FIELDS_OLD = b'                        "entries": batch_entries, "dual": sorted(dual.items()), "target_dot": target_dot, "correlation": corr,\n'
_DUAL_FIELDS_NEW = b'                        "entries": batch_entries, "dual": sorted(dual.items()), "dual_digest": digest({"query_id": query_id,\n                        "dual": sorted(dual.items()), "target": target, "target_dot": target_dot, "correlation": corr}),\n                        "dual_event": dict(self.dual_chain[-1]), "target_dot": target_dot, "correlation": corr,\n'
_PREPARE_OLD = b'        query = oracle.query(assembled, {}, source_word, f"R:{ordinal}")\n'
_PREPARE_NEW = b'''        if ordinal >= 27 and physical_store.open_query is None:
            physical_store.prepare(source_word, assembled, bridge_trace, pending_row_digest, sample=pending_sample)
        else:
            require(ordinal < 27 or physical_store.open_query.get("query_id") == f"R:{ordinal}", "wire:resume_query_row")
        query = oracle.query(assembled, {}, source_word, f"R:{ordinal}")
'''
_PHYS_BRANCH_OLD = b'    if physical_store is not None and physical_store.shards and not physical_store.head.get("obsolete"):\n'
_PHYS_BRANCH_NEW = b'    if physical_store is not None and physical_store.root is not None and physical_store.shards and not physical_store.head.get("obsolete"):\n'
_PHYSICAL_RESTORE_OLD = b'    if physical_store.shards and resume_state is not None: physical_store.direct_restore(oracle.basis, oracle, meter)\n'
_PHYSICAL_RESTORE_NEW = b'''    if physical_store.shards:
        require(resume_state is not None and int(resume_state.get("next_row", 0)) == physical_store.next_row,
                "wire:physical_resume_binding")
        physical_store.direct_restore(oracle.basis, oracle, meter)
'''
_BATCH_BEFORE_OLD = b'            dual, target_dot, active = dual_from_projection(self.basis, target, meter, remainder)\n'
_BATCH_BEFORE_NEW = b'            batch_before = {"boundary_rank": len(self.basis.boundary.pivots), "combined_rank": self.basis.rank(),\n                            "records": len(self.records), "events": len(self.event_chain), "duals": len(self.dual_chain),\n                            "semantic": dict(self.meter.semantic_counters)}\n            dual, target_dot, active = dual_from_projection(self.basis, target, meter, remainder)\n'
_BATCH_LATE_OLD = b'                batch_before = {"boundary_rank": len(self.basis.boundary.pivots), "combined_rank": self.basis.rank(),\n                                "records": len(self.records), "events": len(self.event_chain), "duals": len(self.dual_chain),\n                                "semantic": dict(self.meter.semantic_counters)}\n'
_BATCH_LATE_NEW = b'                # batch state captured before dual/correlation\n'
_WIRE = b'''\
def _a4_wire_path(text: str) -> Path:
    raw = str(text).replace("\\\\", "/"); p = Path(raw)
    require(not p.is_absolute() and ".." not in p.parts and "." not in p.parts,
            "wire:physical_path")
    out = (ROOT / p).resolve(strict=False); area = (ROOT / "ci/out").resolve(strict=True)
    require(out != area and area in out.parents, "wire:physical_containment")
    cursor = ROOT
    for part in p.parts:
        cursor /= part
        if cursor.exists(): require(not stat.S_ISLNK(os.lstat(cursor).st_mode), "wire:physical_symlink")
    return out


def _a4_wire_row(value: Any) -> dict[str, int]:
    if hasattr(value, "to_dict"): value = value.to_dict()
    require(isinstance(value, dict), "wire:row_shape")
    return {str(k): int(v) % 3 for k, v in value.items() if int(v) % 3}


def _a4_wire_entry(store: Any, candidate: dict[str, Any], column: dict[str, int],
                   registration: dict[str, Any], basis: Any, query_event: dict[str, Any],
                   epoch_before: str, epoch_after: str, record: dict[str, Any]) -> dict[str, Any]:
    bd = registration["boundary_detail"]; cd = registration["combined_detail"]; fm = registration["formals"]
    b = {"pivot": bd["pivot"], "scale": bd["scale"], "row": _a4_wire_row(bd["row"]),
         "label": bd["label"], "reduction": dict(bd["reduction"])}
    c = {"pivot": cd["pivot"], "scale": cd["scale"], "row": _a4_wire_row(cd["row"]),
         "label": cd["label"], "reduction": dict(cd["reduction"])}
    raw = {"raw_key": registration["raw_identity"], "row": _a4_wire_row(column),
           "candidate": dict(candidate)}
    insertion = {"kind": "B", "label": b["label"], "column": dict(raw["row"]),
                 "raw_identity": raw["raw_key"], "boundary_row": dict(b["row"]),
                 "boundary_pivot": b["pivot"], "boundary_scale": b["scale"],
                 "boundary_reduction": dict(b["reduction"]), "combined_row": dict(c["row"]),
                 "combined_detail": {"pivot": c["pivot"], "scale": c["scale"],
                                     "row": dict(c["row"]), "reduction": dict(c["reduction"]),
                                     "relation": dict(cd.get("relation", {}))}}
    return {"kind": "B", "raw_identity": raw, "raw_digest": digest(raw["row"]),
            "boundary": {**b, "row_digest": digest(b["row"]), "label_digest": digest(b["label"])},
            "combined": {**c, "row_digest": digest(c["row"]), "label_digest": digest(c["label"])},
            "formals": {"boundary_reduction": dict(b["reduction"]), "combined_reduction": dict(c["reduction"]),
                        "boundary_ledger": dict(fm["boundary_ledger"]), "combined_ledger": dict(fm["combined_ledger"]),
                        "b_coefficients": dict(fm["b_coefficients"]),
                        "b_formals": [dict(fm["b_formals"][0]), dict(fm["b_formals"][1])]},
            "record": dict(record),
            "event": {"insertion": insertion, "query": dict(query_event)},
            "epoch_before": str(epoch_before), "epoch_after": str(epoch_after)}


def _a4_wire_close(store: Any, batch: dict[str, Any]) -> dict[str, Any]:
    require(store.open_query is not None, "wire:closed_without_query")
    candidates = list(batch["candidates"]); mask = [int(x) for x in batch["accepted_mask"]]; m = int(batch["m"])
    require(1 <= m <= 64 and len(candidates) == m and len(mask) == m and all(x in (0, 1) for x in mask),
            "wire:batch_prefix")
    entries = list(batch["entries"]); require(sum(mask) == len(entries), "wire:accepted_mask_entries")
    previous = store.shards[-1]["self_digest_sha256"] if store.shards else None
    pivots = getattr(store, "_a4_pivots", set())
    for entry in entries:
        _a4_validate_physical_entry(entry, pivots); pivots.add(entry["combined"]["pivot"])
    store._a4_pivots = pivots
    sequence = len(store.shards) + 1
    body = {"schema": "d972-r07-word-independent-successor-kernel/v430/shard", "sequence": sequence,
            "previous": previous, "query": dict(store.open_query), "candidate_count": m,
            "candidate_prefix": candidates, "candidate_prefix_digest": digest(candidates),
            "candidate_order_digest": digest([{"raw_identity": c["raw_identity"],
                                                "coefficient": c["coefficient"]} for c in candidates]),
            "accepted_mask": mask, "accepted_count": sum(mask), "dual": batch["dual"],
            "dual_digest": batch["dual_digest"], "dual_event": dict(batch["dual_event"]),
            "target_dot": batch["target_dot"], "correlation": batch["correlation"], "entries": entries,
            "batch_offsets": [0, len(entries)], "before": dict(batch["before"]), "after": dict(batch["after"]),
            "epoch_before": str(batch["epoch_before"]), "epoch_after": str(batch["epoch_after"]),
            "semantic_before": dict(batch["semantic_before"]), "semantic_after": dict(batch["semantic_after"]),
            "counter_digest": digest(batch["semantic_after"])}
    body["chain"] = sha((str(previous) + digest(body)).encode("ascii")); body["self_digest_sha256"] = digest(body)
    store.shards.append(body)
    store.head = {"schema": "d972-r07-word-independent-successor-kernel/v430/head", "sequence": sequence,
                  "next_row": store.next_row, "last_shard_sha256": body["self_digest_sha256"], "chain": body["chain"],
                  "open_query": dict(store.open_query),
                  "cumulative_examined": sum(int(s["candidate_count"]) for s in store.shards),
                  "cumulative_accepted": sum(int(s["accepted_count"]) for s in store.shards),
                  "rank": body["after"].get("combined_rank", 0), "boundary_rank": body["after"].get("boundary_rank", 0),
                  "epoch": body["epoch_after"], "counter_digest": body["counter_digest"], "obsolete": False}
    store.head["self_digest_sha256"] = digest(store.head)
    if store.root is not None:
        store.root.mkdir(parents=True, exist_ok=True)
        write_atomic(store.root / ("shard.%08d.json" % sequence), canon(body))
        write_atomic(store.head_path or store.root / "HEAD", canon(store.head))
    return body


def _a4_wire_restore_files(cls: Any, head_path: Path) -> Any:
    head = json.loads(head_path.read_bytes().decode("ascii")); unsigned = dict(head); claimed = unsigned.pop("self_digest_sha256", None)
    require(claimed == digest(unsigned) and head.get("schema", "").endswith("/head"), "wire:head_seal")
    out = cls(int(head.get("next_row", 27)), head_path.parent, head_path); previous = None; out._a4_pivots = set()
    for sequence in range(1, int(head.get("sequence", 0)) + 1):
        path = head_path.parent / ("shard.%08d.json" % sequence); shard = json.loads(path.read_bytes().decode("ascii"))
        body = dict(shard); seal_value = body.pop("self_digest_sha256", None)
        require(seal_value == digest(body) and shard.get("sequence") == sequence and shard.get("previous") == previous,
                "wire:restore_shard_chain")
        chain = sha((str(previous) + digest({k: v for k, v in body.items() if k != "chain"})).encode("ascii"))
        require(shard.get("chain") == chain, "wire:restore_chain")
        prior = out._a4_pivots
        for entry in shard.get("entries", []): _a4_validate_physical_entry(entry, prior); prior.add(entry["combined"]["pivot"])
        out.shards.append(shard); previous = seal_value
    require(head.get("last_shard_sha256") == previous and head.get("sequence") == len(out.shards) and
            head.get("chain") == (out.shards[-1].get("chain") if out.shards else "0" * 64) and
            head.get("obsolete") is not True and (not out.shards or head.get("open_query") is not None) and
            (not out.shards or head.get("counter_digest") == out.shards[-1].get("counter_digest")), "wire:restore_head")
    out.head = head; out.open_query = dict(head.get("open_query")) if head.get("open_query") else None
    return out


def _a4_wire_direct_restore(store: Any, basis: Any, oracle: Any, meter: Any) -> None:
    pool = _packed_pool_for(meter)
    for shard in store.shards:
        for entry in shard.get("entries", []):
            bd = entry["boundary"]; cd = entry["combined"]; label = str(cd["label"]); bp = str(bd["pivot"]); cp = str(cd["pivot"])
            require(bp not in basis.boundary.rows and cp not in basis.combined.rows, "wire:restore_duplicate_pivot")
            basis.boundary.rows[bp] = _PackedRow.from_dict(bd["row"], pool); basis.boundary.labels[bp] = str(bd["label"]); basis.boundary.pivots.append(bp)
            basis.combined.rows[cp] = _PackedRow.from_dict(cd["row"], pool); basis.combined.labels[cp] = label; basis.combined.pivots.append(cp)
            fm = entry["formals"]; basis.b_rows[label] = dict(cd["row"]); basis.b_ledgers[label] = dict(fm["combined_ledger"])
            basis.boundary_ledgers[label] = dict(fm["boundary_ledger"]); basis.combined_ledgers[label] = dict(fm["combined_ledger"])
            basis.b_coefficients[label] = dict(fm["b_coefficients"]); basis.b_formals[label] = (dict(fm["b_formals"][0]), dict(fm["b_formals"][1]))
            basis.active_registry.update(cd["row"]); basis.insertion_events.append(dict(entry["event"]["insertion"]))
            if isinstance(entry.get("record"), dict): oracle.records.append(dict(entry["record"]))
            if isinstance(entry["event"].get("query"), dict): oracle.event_chain.append(dict(entry["event"]["query"]))
    for shard in store.shards:
        if isinstance(shard.get("dual_event"), dict): oracle.dual_chain.append(dict(shard["dual_event"]))
        query = shard.get("query", {}); oracle.live_duals.append({"query_id": query.get("query_id"),
            "dual": dict(shard.get("dual", [])), "target": dict(query.get("target", {})),
            "target_dot": shard.get("target_dot"), "correlation": dict(shard.get("correlation", {}))})
    if store.shards:
        last = store.shards[-1]; oracle.meter.semantic_counters.update(dict(last.get("semantic_after", {})))
    if store.shards: oracle.epoch = str(store.shards[-1].get("epoch_after", oracle.epoch))
    oracle._a4_direct_restored = True; meter._a4_direct_restore_calls = int(getattr(meter, "_a4_direct_restore_calls", 0)) + 1


def _a4_wire_reference(store: Any, ordinary: dict[str, Any] | None) -> dict[str, Any]:
    def ident(path: Path) -> dict[str, Any]:
        raw = path.read_bytes(); return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}
    head_path = store.head_path or store.root / "HEAD"; paths = [store.root / ("shard.%08d.json" % int(s["sequence"])) for s in store.shards]
    return {"kind": "physical_shard_chain", "owner": "producer", "ordinary": ordinary, "physical_head": ident(head_path),
            "shards": [ident(path) for path in paths], "sequence": len(store.shards),
            "last_shard_sha256": store.shards[-1]["self_digest_sha256"], "chain": store.head["chain"], "next_row": store.next_row,
            "open_query": dict(store.open_query) if store.open_query else None,
            "cumulative_examined": store.head.get("cumulative_examined", 0), "cumulative_accepted": store.head.get("cumulative_accepted", 0),
            "obsolete": False}

_A4PhysicalShardStore.entry_from_live = _a4_wire_entry
_A4PhysicalShardStore.restore_files = classmethod(_a4_wire_restore_files)
_A4PhysicalShardStore.direct_restore = _a4_wire_direct_restore
_A4PhysicalShardStore.reference = _a4_wire_reference
_A4PhysicalShardStore._a4_prepare = _A4PhysicalShardStore.prepare
def _a4_wire_prepare_dispatch(self: Any, *args: Any, **kwargs: Any) -> Any:
    self._a4_prepare_calls = int(getattr(self, "_a4_prepare_calls", 0)) + 1
    return self._a4_prepare(*args, **kwargs)
_A4PhysicalShardStore.prepare = _a4_wire_prepare_dispatch
_A4PhysicalShardStore._v430_close_batch = _A4PhysicalShardStore.close_batch
_A4PhysicalShardStore._v430_commit = _A4PhysicalShardStore.commit
def _a4_wire_close_dispatch(self: Any, examined: Any) -> Any:
    self._a4_close_calls = int(getattr(self, "_a4_close_calls", 0)) + 1
    return _a4_wire_close(self, examined) if isinstance(examined, dict) else self._v430_close_batch(examined)
def _a4_wire_commit_dispatch(self: Any, terminal: dict[str, Any]) -> Any:
    self._a4_commit_calls = int(getattr(self, "_a4_commit_calls", 0)) + 1
    result = self._v430_commit(terminal)
    if self.root is not None and self.head_path is not None:
        self.head["next_row"] = self.next_row; self.head["open_query"] = None; self.head["obsolete"] = True
        self.head["self_digest_sha256"] = digest({k: v for k, v in self.head.items() if k != "self_digest_sha256"}); write_atomic(self.head_path, canon(self.head))
    return result
_A4PhysicalShardStore.close_batch = _a4_wire_close_dispatch
_A4PhysicalShardStore.commit = _a4_wire_commit_dispatch

'''

_PATCHES = (
    (_LIVE_RETURN_OLD, _LIVE_RETURN_NEW, 1),
    (b'def __init__(self, next_row: int = 27, root: Path | None = None):\n', b'def __init__(self, next_row: int = 27, root: Path | None = None,\n                 head_path: Path | None = None):\n', 1),
    (b'        self.root = root\n', b'        self.root = root; self.head_path = head_path or (root / "HEAD" if root is not None else None)\n', 1),
    (b'            write_atomic(self.root / "HEAD", canon(self.head))\n', b'            write_atomic(self.head_path or self.root / "HEAD", canon(self.head))\n', 1),
    (b'def build_kernel(authority: AuthorityAdapter, runtime: Runtime, dag_forward: ForwardDAG,\n', _WIRE + b'def build_kernel(authority: AuthorityAdapter, runtime: Runtime, dag_forward: ForwardDAG,\n', 1),
    (b'def __init__(self, runtime: Runtime, ledger: BoundaryLedger, meter: Meter):\n', b'def __init__(self, runtime: Runtime, ledger: BoundaryLedger, meter: Meter, shard_store: Any | None = None):\n', 1),
    (b'        self.runtime, self.ledger, self.meter = runtime, ledger, meter; self.basis = LiveBasis(meter, ledger)\n', b'        self.runtime, self.ledger, self.meter = runtime, ledger, meter; self.basis = LiveBasis(meter, ledger)\n        self.shard_store = shard_store; self._a4_batch_entries: list[dict[str, Any]] = []\n', 1),
    (b'''                require(0 < examined_limit <= CANONICAL_BATCH_CAP and\n                        examined_limit == min(64, len(private_candidates)),\n                        "batch:exact_examined_limit")\n                accepted = 0; examined = 0; accepted_nonzero_reductions = 0\n''', b'''                require(0 < examined_limit <= CANONICAL_BATCH_CAP and\n                        examined_limit == min(64, len(private_candidates)),\n                        "batch:exact_examined_limit")\n                batch_before = {"boundary_rank": len(self.basis.boundary.pivots), "combined_rank": self.basis.rank(),\n                                "records": len(self.records), "events": len(self.event_chain), "duals": len(self.dual_chain),\n                                "semantic": dict(self.meter.semantic_counters)}\n                batch_candidates: list[dict[str, Any]] = []; batch_mask: list[int] = []; batch_entries: list[dict[str, Any]] = []\n                accepted = 0; examined = 0; accepted_nonzero_reductions = 0\n''', 1),
    (b'''                    raw_id = raw_key(context, relation, translation); column = seed.translate(translation)\n                    current_remainder, _current_correction = self.basis.combined.reduce(column)\n''', b'''                    raw_id = raw_key(context, relation, translation); column = seed.translate(translation)\n                    candidate_identity = {"raw_identity": raw_id, "selected": [context, relation, text], "coefficient": int(coefficient), "row": dict(column)}\n                    batch_candidates.append(candidate_identity)\n                    current_remainder, _current_correction = self.basis.combined.reduce(column)\n''', 1),
    (b'                    if not current_remainder: continue\n', b'                    if not current_remainder: batch_mask.append(0); continue\n', 1),
    (b'                    rank_before = self.basis.rank()\n', b'                    epoch_before = self.epoch; rank_before = self.basis.rank()\n', 1),
    (b'                    self._record(record); accepted += 1\n', b'''                    self._record(record); accepted += 1; batch_mask.append(1)\n                    if self.shard_store is not None and self.shard_store.open_query is not None:\n                        batch_entries.append(self.shard_store.entry_from_live(candidate_identity, column, reg, self.basis,\n                                                                            self.event_chain[-1], epoch_before, self.epoch,\n                                                                            record))\n''', 1),
    (b'''                progress_once(meter, "CORRELATION", int(getattr(meter, "_a4_current_row", 0)),\n                              self.basis.rank(), len(self.basis.boundary.pivots),\n                              len(self.basis.k_items), accepted)\n                continue\n''', b'''                progress_once(meter, "CORRELATION", int(getattr(meter, "_a4_current_row", 0)),\n                              self.basis.rank(), len(self.basis.boundary.pivots),\n                              len(self.basis.k_items), accepted)\n                if self.shard_store is not None and self.shard_store.open_query is not None:\n                    batch_after = {"boundary_rank": len(self.basis.boundary.pivots), "combined_rank": self.basis.rank(),\n                                   "records": len(self.records), "events": len(self.event_chain), "duals": len(self.dual_chain)}\n                    self.shard_store.close_batch({"m": examined_limit, "candidates": batch_candidates, "accepted_mask": batch_mask,\n                        "entries": batch_entries, "dual": sorted(dual.items()), "target_dot": target_dot, "correlation": corr,\n                        "before": batch_before, "after": batch_after, "epoch_before": batch_entries[0]["epoch_before"] if batch_entries else self.epoch,\n                        "epoch_after": self.epoch, "semantic_before": dict(batch_before["semantic"]), "semantic_after": dict(self.meter.semantic_counters)})\n                continue\n''', 1),
    (_DUAL_FIELDS_OLD, _DUAL_FIELDS_NEW, 1),
    (_PREPARE_OLD, _PREPARE_NEW, 1),
    (_BATCH_BEFORE_OLD, _BATCH_BEFORE_NEW, 1),
    (_BATCH_LATE_OLD, _BATCH_LATE_NEW, 1),
    (b'''def build_kernel(authority: AuthorityAdapter, runtime: Runtime, dag_forward: ForwardDAG,\n                 primitive: list[tuple[int, ...]], inventory: dict[str, Any], meter: Meter,\n                 checkpoint_path: Path | None = None,\n                 resume_state: dict[str, Any] | None = None) -> dict[str, Any]:\n''', b'''def build_kernel(authority: AuthorityAdapter, runtime: Runtime, dag_forward: ForwardDAG,\n                 primitive: list[tuple[int, ...]], inventory: dict[str, Any], meter: Meter,\n                 checkpoint_path: Path | None = None,\n                 resume_state: dict[str, Any] | None = None,\n                 physical_root: Path | None = None, physical_head: Path | None = None) -> dict[str, Any]:\n''', 1),
    (b'    ledger = BoundaryLedger(runtime, meter); oracle = Oracle(runtime, ledger, meter)\n', b'''    ledger = BoundaryLedger(runtime, meter)\n    physical_store = _A4PhysicalShardStore(next_row=27, root=physical_root, head_path=physical_head)\n    if physical_head is not None and physical_head.exists(): physical_store = _A4PhysicalShardStore.restore_files(physical_head)\n    meter._a4_physical_store = physical_store; oracle = Oracle(runtime, ledger, meter, physical_store)\n''', 1),
    (b'''    oracle.row_digests = row_digests; oracle.row_chunks = chunks\n    oracle.samples = samples; oracle.sample_rows = sample_rows\n    resume_row = 1 if resume_state is None else int(resume_state.get("next_row", 0))\n''', b'''    oracle.row_digests = row_digests; oracle.row_chunks = chunks\n    oracle.samples = samples; oracle.sample_rows = sample_rows\n    if physical_store.shards and resume_state is not None: physical_store.direct_restore(oracle.basis, oracle, meter)\n    resume_row = 1 if resume_state is None else int(resume_state.get("next_row", 0))\n''', 1),
    (_PHYSICAL_RESTORE_OLD, _PHYSICAL_RESTORE_NEW, 1),
    # The physical reference branch is root-gated in the injected wire body.
    (b'        oracle.bridge_chain.append(bridge_trace["bridge_trace_digest"])\n', b'        pending_bridge_digest = bridge_trace["bridge_trace_digest"]\n', 1),
    (b'        row_digests.append(digest(row_value))\n', b'        pending_row_digest = digest(row_value)\n', 1),
    (b'''        if ordinal in {1024, 2048, 3072, 4096, 5120, 6144, 6441}:\n            chunks.append({"start": chunk_start, "end": ordinal,\n                           "sha256": digest(row_digests[chunk_start - 1:ordinal])})\n            chunk_start = ordinal + 1\n''', b'        pending_chunk = ordinal in {1024, 2048, 3072, 4096, 5120, 6144, 6441}\n', 1),
    (b'''        if ordinal - 1 in sample_indices:\n            direct = runtime.states_direct(source_word); require(runtime.row_from_states(direct) == assembled,\n                                                               "row:fixed_direct_canary")\n            samples.append({"ordinal": ordinal, "word": list(source_word), "row_digest": digest(assembled)})\n            sample_rows[ordinal] = {"word": tuple(source_word), "row": assembled}\n''', b'''        pending_sample = None\n        if ordinal - 1 in sample_indices:\n            direct = runtime.states_direct(source_word); require(runtime.row_from_states(direct) == assembled,\n                                                               "row:fixed_direct_canary")\n            pending_sample = {"ordinal": ordinal, "word": list(source_word), "row_digest": digest(assembled), "row": assembled}\n''', 1),
    (b'        meter._a4_completed_row = ordinal\n', b'''        if ordinal >= 27 and physical_store.open_query is not None: physical_store.commit(query)\n        oracle.bridge_chain.append(pending_bridge_digest); row_digests.append(pending_row_digest)\n        if pending_chunk:\n            chunks.append({"start": chunk_start, "end": ordinal, "sha256": digest(row_digests[chunk_start - 1:ordinal])}); chunk_start = ordinal + 1\n        if pending_sample is not None:\n            samples.append({key: pending_sample[key] for key in ("ordinal", "word", "row_digest")}); sample_rows[ordinal] = {"word": tuple(pending_sample["word"]), "row": pending_sample["row"]}\n        meter._a4_completed_row = ordinal\n''', 1),
    (b'''             "boundary": {"seed_count": len(ledger.seeds), "rank": len(oracle.basis.b_rows),\n''', b'''             "physical_shard_chain": {"sequence": len(physical_store.shards), "head": dict(physical_store.head),\n                                       "open_query": dict(physical_store.open_query) if physical_store.open_query else None,\n                                       "call_counts": {"prepare": int(getattr(physical_store, "_a4_prepare_calls", 0)),\n                                                        "close_batch": int(getattr(physical_store, "_a4_close_calls", 0)),\n                                                        "direct_restore": int(getattr(meter, "_a4_direct_restore_calls", 0)),\n                                                        "commit": int(getattr(physical_store, "_a4_commit_calls", 0))},\n                                       "direct_restore_calls": int(getattr(meter, "_a4_direct_restore_calls", 0))},\n             "boundary": {"seed_count": len(ledger.seeds), "rank": len(oracle.basis.b_rows),\n''', 1),
    (b'''def actual_result(authority: AuthorityAdapter, meter: Meter, checkpoint: Path | None = None,\n                  resume_state: dict[str, Any] | None = None) -> dict[str, Any]:\n''', b'''def actual_result(authority: AuthorityAdapter, meter: Meter, checkpoint: Path | None = None,\n                  resume_state: dict[str, Any] | None = None, physical_root: Path | None = None,\n                  physical_head: Path | None = None) -> dict[str, Any]:\n''', 1),
    (b'''    forward = ForwardDAG(runtime, meter); kernel = build_kernel(authority, runtime, forward, primitive,\n                                                                  inventory, meter, checkpoint, resume_state)\n''', b'''    forward = ForwardDAG(runtime, meter); kernel = build_kernel(authority, runtime, forward, primitive,\n                                                                  inventory, meter, checkpoint, resume_state, physical_root, physical_head)\n''', 1),
    (b'''    p.add_argument("--input", default="ci/in/d972_r07_seven_context_roof_presentation_v1.json")\n''', b'''    p.add_argument("--input", default="ci/in/d972_r07_seven_context_roof_presentation_v1.json")\n    p.add_argument("--physical-root")\n    p.add_argument("--physical-head")\n''', 1),
    (b'''    output: Path | None = None\n    authority_identity: str | None = None\n''', b'''    output: Path | None = None\n    physical_root: Path | None = None; physical_head: Path | None = None\n    authority_identity: str | None = None\n''', 1),
    (b'''            if args.resume:\n                resume_text = str(args.resume).replace("\\\\", "/")\n                resume_path = Path(resume_text)\n                resume_arg = exact_path(resume_text, "ci/out", resume_path.name, "CHECKPOINT_RESUME")\n''', b'''            if args.resume:\n                resume_text = str(args.resume).replace("\\\\", "/")\n                resume_path = Path(resume_text)\n                resume_arg = exact_path(resume_text, "ci/out", resume_path.name, "CHECKPOINT_RESUME")\n            if args.physical_root:\n                physical_root = _a4_wire_path(args.physical_root); physical_head = physical_root / "HEAD"\n            if args.physical_head:\n                physical_head = _a4_wire_path(args.physical_head); require(physical_head.name == "HEAD", "wire:physical_head_name")\n                if physical_root is None: physical_root = physical_head.parent\n''', 1),
    (b'            normal = actual_result(authority, meter, checkpoint_arg)\n', b'            normal = actual_result(authority, meter, checkpoint_arg, None, physical_root, physical_head)\n', 1),
    (b'        result = actual_result(authority, meter, checkpoint_arg, resume_state)\n', b'        result = actual_result(authority, meter, checkpoint_arg, resume_state, physical_root, physical_head)\n', 1),
    (b'''    if path is not None and path.name.endswith(".head.checkpoint.json"):\n        try:\n            return _delta_checkpoint_reference(path, meter)\n        except Exception:\n            pass\n''', b'''    physical_store = getattr(meter, "_a4_physical_store", None)\n    if physical_store is not None and physical_store.root is not None and physical_store.shards and not physical_store.head.get("obsolete"):\n        ordinary = None\n        if path is not None and path.name.endswith(".head.checkpoint.json"):\n            try: ordinary = _delta_checkpoint_reference(path, meter)\n            except Exception: ordinary = None\n        return physical_store.reference(ordinary)\n    if path is not None and path.name.endswith(".head.checkpoint.json"):\n        try:\n            return _delta_checkpoint_reference(path, meter)\n        except Exception:\n            pass\n''', 1),
)

def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def _v23_generated() -> bytes:
    path = ROOT / OWNER[0]; raw = path.read_bytes()
    if len(raw) != OWNER[1] or _sha(raw) != OWNER[2]: raise RuntimeError("v24 producer owner pin drift")
    ns: dict[str, Any] = {"__name__": "_v24_v23_owner", "__file__": str(path),
                          "__package__": None, "__cached__": None}
    exec(compile(raw, str(path), "exec"), ns, ns)
    source = ns.get("restore_frozen", lambda: None)()
    if not isinstance(source, bytes) or len(source) != OWNER_GENERATED[0] or _sha(source) != OWNER_GENERATED[1]:
        raise RuntimeError("v24 producer generated owner pin drift")
    return source

def _generate() -> tuple[bytes, list[dict[str, Any]]]:
    raw = _v23_generated(); report = []
    for index, (old, new, expected) in enumerate(_PATCHES, 1):
        before = raw.count(old); new_before = raw.count(new)
        if before != expected or new_before != 0: raise RuntimeError(f"v24 producer patch {index} cardinality")
        raw = raw.replace(old, new)
        # Insertion patches deliberately retain the anchor inside their replacement;
        # this includes the commit handoff, whose retained line is not at byte 0.
        keep_old = old in new
        if ((not keep_old and raw.count(old) != 0) or
                (keep_old and raw.count(old) != expected) or
                raw.count(new) != expected):
            raise RuntimeError(f"v24 producer patch {index} postcondition old={raw.count(old)} new={raw.count(new)} keep={keep_old}")
        report.append({"index": index, "old_before": before, "new_before": new_before,
                       "old_after": raw.count(old), "new_after": raw.count(new),
                       "old": old.decode("ascii", "replace")[:120]})
    return raw, report

_SOURCE, _REPORT = _generate()
if "--source-patch-info" in sys.argv[1:]:
    print(json.dumps({"owner": {"path": OWNER[0], "bytes": OWNER[1], "sha256": OWNER[2]},
                      "owner_generated": {"bytes": OWNER_GENERATED[0], "sha256": OWNER_GENERATED[1]},
                      "generated": {"bytes": len(_SOURCE), "sha256": _sha(_SOURCE)}, "patches": _REPORT},
                     sort_keys=True, separators=(",", ":")))
    raise SystemExit(0)
if RESULT_GENERATED[0] and (len(_SOURCE) != RESULT_GENERATED[0] or _sha(_SOURCE) != RESULT_GENERATED[1]):
    raise RuntimeError("v24 producer generated pin drift")
exec(compile(_SOURCE, str(ROOT / OWNER[0]), "exec"), globals(), globals())
