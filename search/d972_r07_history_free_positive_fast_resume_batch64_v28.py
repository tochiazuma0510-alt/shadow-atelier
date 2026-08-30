#!/usr/bin/env python3
"""A0 v28: globally merged boundary batch-64 over frozen streaming v26."""
from __future__ import annotations

import hashlib
from pathlib import Path

_V26 = Path(__file__).resolve().with_name(
    "d972_r07_history_free_positive_fast_resume_v26.py")
_V26_BYTES = 5950
_V26_SHA256 = "4ae9de2eaf0ae337d48309f107fe7aef94afe3783ee2bde63b7c839364e1098e"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("batch64 v28 " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("batch64 v28 " + label + " result cardinality")
    return result


def _replace_region(source: bytes, start: bytes, stop: bytes,
                    replacement: bytes, label: str) -> bytes:
    if source.count(start) != 1 or source.count(stop) != 1:
        raise SystemExit("batch64 v28 " + label + " boundary cardinality")
    left = source.index(start); right = source.index(stop, left)
    if right <= left:
        raise SystemExit("batch64 v28 " + label + " boundary order")
    result = source[:left] + replacement + source[right:]
    if result.count(replacement) != 1:
        raise SystemExit("batch64 v28 " + label + " replacement cardinality")
    return result


_raw = _V26.read_bytes()
if len(_raw) != _V26_BYTES or hashlib.sha256(_raw).hexdigest() != _V26_SHA256:
    raise SystemExit("batch64 v28 frozen v26 owner drift")
_scope = {"__file__": str(_V26), "__name__": "_r07_v26_for_batch64_v28"}
exec(compile(_raw, str(_V26), "exec"), _scope, _scope)
_patched = _scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("batch64 v28 generated v26 owner missing")

_HELPERS = b'''BATCH_CAP = 64


def _batch_global_merge(worker_results, batch_cap):
    require(type(batch_cap) is int and batch_cap >= 1, "batch cap")
    accumulated = {}
    worker_ids = set()
    accumulator_entries = 0
    for result in worker_results:
        worker_id = int(result["worker_id"])
        require(worker_id not in worker_ids, "batch worker uniqueness")
        worker_ids.add(worker_id)
        rows = result["accumulator"]
        require(type(rows) is list, "batch worker accumulator")
        prior = None
        for block0, raw_hex, relator0, coefficient0 in rows:
            key = (int(block0), bytes.fromhex(str(raw_hex)), int(relator0))
            coefficient = int(coefficient0)
            require(coefficient in (1, 2) and (prior is None or prior < key),
                    "batch canonical worker accumulator")
            prior = key
            value = (accumulated.get(key, 0) + coefficient) % 3
            if value: accumulated[key] = value
            else: accumulated.pop(key, None)
            accumulator_entries += 1
    selected_keys = sorted(accumulated)[:batch_cap]
    selected_public = [[block, raw.hex(), relator, accumulated[(block, raw, relator)]]
                       for block, raw, relator in selected_keys]
    return {"active": accumulated,
            "global_active_index_count": len(accumulated),
            "selected_keys": selected_keys,
            "selected_batch": selected_public,
            "selected_batch_sha256": sha_obj(selected_public),
            "accumulator_entries": accumulator_entries}


'''
_patched = _swap(_patched, b'class PersistentBoundaryOwner:',
                 _HELPERS + b'class PersistentBoundaryOwner:',
                 "global merge helper")
_patched = _swap(
    _patched,
    b'            "winner_reconstructions": 0, "process_restarts": 0,\n'
    b'            "metric": "sampled RSS sum; not exact physical peak"}',
    b'            "winner_reconstructions": 0, "process_restarts": 0,\n'
    b'            "batch_cap": BATCH_CAP, "global_active_index_count": 0,\n'
    b'            "selected_batch_sha256": sha_obj([]),\n'
    b'            "materialized_count": 0, "retained_independent_count": 0,\n'
    b'            "dependent_count": 0, "dual_rebuild_count": 0,\n'
    b'            "parent_pair_visits": 0, "last_parent_pair_visits": 0,\n'
    b'            "metric": "sampled RSS sum; not exact physical peak"}',
    "batch accounting")

_RUN_TAIL = b'''        for result in results:
            rows = result["accumulator"]
            self.accounting["accumulator_entries"] += len(rows)
            self.accounting["max_accumulator_entries"] = max(
                self.accounting["max_accumulator_entries"], len(rows))
        merged = _batch_global_merge(results, BATCH_CAP)
        require(merged["accumulator_entries"] == sum(
                len(result["accumulator"]) for result in results),
                "global batch accumulator accounting")
        selected_keys = merged["selected_keys"]
        selected = selected_keys[0] if selected_keys else None
        accumulated = merged["active"]
        self.meter.commit("boundary_pairs", total)
        self.accounting["epochs_committed"] += 1
        self.accounting["literal_pairs_committed"] += total
        self.accounting["support_bytes"] += len(canonical(support["entries"]))
        self.accounting["global_active_index_count"] = merged[
            "global_active_index_count"]
        self.accounting["selected_batch_sha256"] = merged[
            "selected_batch_sha256"]
        outcome = {"epoch": self.epoch, "dual_sha256": dual_digest,
            "support_entry_count": support["entry_count"],
            "support_sha256": support["sha256"],
            "support_types": support["types"],
            "matching_descriptor_ids": descriptor_ids,
            "matching_descriptor_count": len(descriptor_ids),
            "expanded_pair_count": total, "intervals": intervals,
            "slice_digests": [frame["slice_sha256"] for frame in frames],
            "slice_coverage": {"global_ordinal": [0, total],
                                "disjoint": True, "overlap": False},
            "batch_cap": BATCH_CAP,
            "global_active_index_count": merged["global_active_index_count"],
            "selected_batch": merged["selected_batch"],
            "selected_batch_sha256": merged["selected_batch_sha256"],
            "selected": None if selected is None else
                [selected[0], selected[1].hex(), selected[2]],
            "selected_scalar": None if selected is None else accumulated[selected],
            "zero_complete": selected is None,
            "result_digests": [row["result_sha256"] for row in results],
            "worker_results": results}
        if self.epoch == 1 and len(dual) == 1188:
            require(support["entry_count"] == 1188 and
                    support["types"] == [[1, 1]] and
                    len(descriptor_ids) == 4 and total == 4752,
                    "exact pinned first boundary epoch")
            outcome["pinned_first_epoch"] = True
        return outcome


'''
_patched = _replace_region(
    _patched,
    b'        accumulated: dict[tuple[int, bytes, int], int] = {}\n',
    b'    def materialize(self, dual: dict[bytes, int], outcome: dict[str, Any])',
    _RUN_TAIL,
    "globally merged batch run tail")

_MATERIALIZE = b'''    def materialize_batch(self, dual, outcome):
        require(outcome["epoch"] == self._materialize_epoch and
                self._materialize_support_private is not None and
                outcome.get("batch_cap") == BATCH_CAP and
                type(outcome.get("selected_batch")) is list and
                1 <= len(outcome["selected_batch"]) <= BATCH_CAP and
                outcome.get("selected_batch_sha256") ==
                    sha_obj(outcome["selected_batch"]) and
                outcome.get("global_active_index_count", -1) >=
                    len(outcome["selected_batch"]),
                "parent batch support/epoch binding")
        live = self.runtime["live"]
        selected_positions = {}
        for position, selected in enumerate(outcome["selected_batch"]):
            require(type(selected) is list and len(selected) == 4,
                    "parent selected batch row")
            block, translation_hex, relator, claimed_scalar = selected
            key = (int(block), bytes.fromhex(str(translation_hex)), int(relator))
            require(key not in selected_positions and int(claimed_scalar) in (1, 2),
                    "parent selected batch uniqueness/scalar")
            selected_positions[key] = position
        support = self._materialize_support_private
        contributors = [[] for _selected in outcome["selected_batch"]]
        visits = 0
        for descriptor_id in outcome["matching_descriptor_ids"]:
            descriptor = self.descriptors[descriptor_id]
            quotient = live.group_for_block(self.runtime, descriptor["block"])
            for g_blob, lambda_coefficient, g in support.get(
                    (descriptor["block"], descriptor["component"]), ()):
                if (visits & 4095) == 0:
                    self.meter.check("positive_boundary_batch_parent_scan",
                                     self.pids())
                visits += 1
                translation = quotient.mul(g, descriptor["h_inverse"])
                require(quotient.mul(translation, descriptor["h"]) == g,
                        "parent batch t*h=g")
                key = (descriptor["block"],
                       live.element_blob(self.runtime, translation),
                       descriptor["relator"])
                position = selected_positions.get(key)
                if position is not None:
                    contributors[position].append({"component": descriptor["component"],
                        "g_hex": g_blob.hex(), "h_hex": descriptor["h_blob"].hex(),
                        "lambda_coefficient": lambda_coefficient,
                        "base_coefficient": descriptor["base_coefficient"]})
        require(visits == outcome["expanded_pair_count"],
                "parent batch single complete pair scan")
        payloads = []
        for position, selected in enumerate(outcome["selected_batch"]):
            block, translation_hex, relator, claimed_scalar = selected
            translation_blob = bytes.fromhex(translation_hex)
            row = live.translated_boundary(self.runtime, int(block), int(relator),
                                           translation_blob)
            scalar = live.pair(dual, row)
            require(scalar == claimed_scalar and scalar in (1, 2),
                    "parent batch translated-row scalar")
            claimed_contributors = contributors[position]
            require(claimed_contributors and
                    sum(item["lambda_coefficient"] * item["base_coefficient"]
                        for item in claimed_contributors) % 3 == scalar,
                    "parent batch full contributors")
            selection = {"schema": SCHEMA + "/global-batch-selection/v28",
                "batch_cap": BATCH_CAP, "epoch": outcome["epoch"],
                "dual_sha256": outcome["dual_sha256"],
                "global_active_index_count": outcome["global_active_index_count"],
                "selected_count": len(outcome["selected_batch"]),
                "selected_batch_sha256": outcome["selected_batch_sha256"],
                "expanded_pair_count": outcome["expanded_pair_count"],
                "parent_pair_visits": visits,
                "selected_position": position,
                "selected_index": [block, translation_hex, relator],
                "selected_scalar": scalar}
            payloads.append({"row": row, "provenance": {"family": "boundary",
                "block": block, "base_relator_index": relator,
                "translation_hex": translation_hex, "scalar": scalar,
                "complete_support_occurrence_accumulation": True,
                "left_translation_gate": "t*h=g",
                "contributing_pairs": claimed_contributors,
                "batch_selection": selection}})
        self.accounting["winner_reconstructions"] += len(payloads)
        self.accounting["materialized_count"] += len(payloads)
        self.accounting["parent_pair_visits"] += visits
        self.accounting["last_parent_pair_visits"] = visits
        return payloads

    def finish_materialize_batch(self):
        self._materialize_support_private = None

'''
_patched = _swap(_patched,
                 b'    def abort(self, reason: str) -> None:',
                 _MATERIALIZE + b'    def abort(self, reason: str) -> None:',
                 "parent batch materializer")

_SEARCH_BATCH = b'''    def add_boundary_batch_payload(self, payload, dual, position):
        row, provenance = payload["row"], payload["provenance"]
        live = self.runtime["live"]
        require(live.pair(dual, row) == provenance["scalar"] in (1, 2),
                "batch frozen-dual scalar")
        remainder = dict(row)
        for pivot in self.reducer.order:
            value = remainder.get(pivot, 0)
            if value: live.add_scaled(remainder, self.reducer.rows[pivot], -value)
        if not remainder:
            require(position > 0, "batch first row must raise rank")
            self.boundary.accounting["dependent_count"] += 1
            return False
        self.meter.reserve("retained_columns", 1, "batch_rank_increase")
        symbol = f"n:{len(self.new_records) + 1:04d}"
        before_order = len(self.reducer.order)
        before_nodes = len(self.reducer.ancestry.nodes)
        before_formal = self.reducer.formal_entries
        before_support = self.reducer.dag_support_allocations
        before_dag_meter = self.meter.counters["dag_node_allocations"]
        try:
            pivot, pivot_node_id = self.reducer.add_actual(row, symbol)
        except BaseException:
            for added_pivot in self.reducer.order[before_order:]:
                self.reducer.rows.pop(added_pivot, None)
                self.reducer.expr_ids.pop(added_pivot, None)
            del self.reducer.order[before_order:]
            appended = self.reducer.ancestry.nodes[before_nodes:]
            for node in appended:
                if self.reducer.ancestry.intern.get(node, -1) >= before_nodes:
                    self.reducer.ancestry.intern.pop(node, None)
            del self.reducer.ancestry.nodes[before_nodes:]
            self.reducer.formal_entries = before_formal
            self.reducer.dag_support_allocations = before_support
            self.meter.counters["dag_node_allocations"] = before_dag_meter
            raise
        self.meter.commit("retained_columns", 1)
        before = before_order
        public_row = live.public_sparse(row)
        record = {"symbol": symbol, "family": "boundary",
            "provenance": provenance, "sparse_row": public_row,
            "sparse_row_sha256": live.sha_obj(public_row),
            "pivot_hex": pivot.hex(), "pivot_node_id": pivot_node_id,
            "rank_before": before, "rank_after": before + 1,
            "active_dual": live.public_sparse(dual),
            "active_dual_sha256": live.sha_obj(live.public_sparse(dual)),
            "dual_pairing": live.pair(dual, row), "actual_direct_replay": True}
        self.new_records.append(record)
        self.boundary.accounting["retained_independent_count"] += 1
        self.boundary.accounting["formal_ancestry_entries"] = self.reducer.formal_entries
        self.correction_progress = {"dual_sha256": None,
                                    "canonical_row_cursor": 0,
                                    "weighted_rows": {}}
        self.last_safe_phase = "batch_actual_rank_increase"
        return True

    def add_boundary_batch(self, dual, outcome):
        selected = outcome.get("selected_batch")
        require(type(selected) is list and selected and len(selected) <= BATCH_CAP,
                "nonempty bounded selected batch")
        retained = 0
        try:
            payloads = self.boundary.materialize_batch(dual, outcome)
            require(len(payloads) == len(selected), "complete batch payloads")
            for position, payload in enumerate(payloads):
                self.meter.check("positive_boundary_batch_materialize",
                                 self.boundary.pids())
                if self.add_boundary_batch_payload(payload, dual, position):
                    retained += 1
        except ResourceStop:
            if retained:
                self.boundary.accounting["dual_rebuild_count"] += 1
            raise
        finally:
            self.boundary.finish_materialize_batch()
        require(retained >= 1, "nonempty batch rank growth")
        self.boundary.accounting["dual_rebuild_count"] += 1
        return retained

'''
_patched = _swap(_patched,
                 b'    def _formal_public(self) -> dict[str, Any]:',
                 _SEARCH_BATCH + b'    def _formal_public(self) -> dict[str, Any]:',
                 "sequential batch reducer")
_patched = _swap(
    _patched,
    b'            outcome = self.boundary.run_epoch(dual)\n'
    b'            active = self.boundary.materialize(dual, outcome)\n'
    b'            if active is not None:\n'
    b'                self.add_actual(active, dual)\n'
    b'                continue\n',
    b'            outcome = self.boundary.run_epoch(dual)\n'
    b'            if outcome.get("selected_batch"):\n'
    b'                self.add_boundary_batch(dual, outcome)\n'
    b'                continue\n'
    b'            self.boundary.finish_materialize_batch()\n',
    "production batch loop")
_patched = _swap(
    _patched,
    b'    current = dict(search.boundary.accounting); restored = dict(prior_boundary["accounting"])\n',
    b'    current = dict(search.boundary.accounting)\n'
    b'    restored = dict(current)\n'
    b'    restored.update(prior_boundary["accounting"])\n'
    b'    for name, default in (("batch_cap", BATCH_CAP),\n'
    b'            ("global_active_index_count", 0),\n'
    b'            ("selected_batch_sha256", sha_obj([])),\n'
    b'            ("materialized_count", 0),\n'
    b'            ("retained_independent_count", 0),\n'
    b'            ("dependent_count", 0), ("dual_rebuild_count", 0),\n'
    b'            ("parent_pair_visits", 0),\n'
    b'            ("last_parent_pair_visits", 0)):\n'
    b'        restored.setdefault(name, default)\n'
    b'    require(restored["batch_cap"] == BATCH_CAP,\n'
    b'            "batch accounting resume cap")\n',
    "v24 accounting migration")

if (_patched.count(b'def _stream_pre_records') != 1 or
        _patched.count(b'def _stream_post_parse') != 1 or
        _patched.count(b'_stream_resume(search, resume_path, 1663424241,') != 1 or
        b'restore_checkpoint(search, resume_path)' in _patched or
        _patched.count(b'BATCH_CAP = 64') != 1 or
        _patched.count(b'def _batch_global_merge') != 1 or
        _patched.count(b'def materialize_batch') != 1 or
        b'def materialize_selected' in _patched):
    raise SystemExit("batch64 v28 generated owner gate")

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
