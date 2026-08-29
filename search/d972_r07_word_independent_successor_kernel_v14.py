#!/usr/bin/env python3
"""A4 v14 owner: v13 with one exact canonical current-basis batch.

The public correlation and checkpoint ABIs are unchanged.  The private
generated-source interface exposes the already-computed canonical nonzero
roster only for the duration of the current query.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


OWNER = Path(__file__).with_name("d972_r07_word_independent_successor_kernel_v13.py")
OWNER_BYTES = 9731
OWNER_SHA256 = "c8e93ba9b72971428f2a8dba96049e183bfe1d794ac6008cb6495e6d5661f514"

PATCHES = (
    (
        b'''def correlate(ledger: BoundaryLedger, dual: dict[str, int], meter: Meter) -> dict[str, Any]:
    accum: dict[tuple[int, int, str], int] = {}; pairs = 0
    expected_pairs = sum(len(ledger.by_component.get(split_row_key(key)[:2], ()))
                         for key in dual)
    meter._a4_correlation_rounds = int(getattr(meter, "_a4_correlation_rounds", 0)) + 1
    meter.reserve("correlation_pairs", expected_pairs, "full_D_correlation")
    for dual_key, lambda_value in dual.items():
        context, component, text = split_row_key(dual_key); g = decode_token(text)
        for seed, h, seed_coefficient in ledger.by_component.get((context, component), []):
            inverse_h = ledger.inverse_cache[context, h]; t = seed.q.mul(g, inverse_h)
            require(seed.q.mul(t, h) == g, "dual:translation_product")
            key = (context, seed.relation, token(t)); KEYS[key[2]] = t
            accum[key] = (accum.get(key, 0) + int(lambda_value) * int(seed_coefficient)) % 3
            pairs += 1
    require(pairs == expected_pairs, "dual:correlation_pair_count")
    meter.bump("correlation_pairs", pairs, "full_D_correlation")
    ordered = sorted(((key, value) for key, value in accum.items() if value),
                     key=lambda item: item[0])
    return {"pair_count": pairs, "accumulator_digest": digest(sorted((list(k), v) for k, v in accum.items())),
            "selected": ([ordered[0][0][0], ordered[0][0][1], ordered[0][0][2], ordered[0][1]]
                         if ordered else None), "complete": True}
''',
        b'''CANONICAL_BATCH_CAP = 64


def correlate_private(ledger: BoundaryLedger, dual: dict[str, int], meter: Meter) -> tuple[dict[str, Any], list[tuple[tuple[int, int, str], int]]]:
    accum: dict[tuple[int, int, str], int] = {}; pairs = 0
    expected_pairs = sum(len(ledger.by_component.get(split_row_key(key)[:2], ()))
                         for key in dual)
    meter._a4_correlation_rounds = int(getattr(meter, "_a4_correlation_rounds", 0)) + 1
    meter.reserve("correlation_pairs", expected_pairs, "full_D_correlation")
    for dual_key, lambda_value in dual.items():
        context, component, text = split_row_key(dual_key); g = decode_token(text)
        for seed, h, seed_coefficient in ledger.by_component.get((context, component), []):
            inverse_h = ledger.inverse_cache[context, h]; t = seed.q.mul(g, inverse_h)
            require(seed.q.mul(t, h) == g, "dual:translation_product")
            key = (context, seed.relation, token(t)); KEYS[key[2]] = t
            accum[key] = (accum.get(key, 0) + int(lambda_value) * int(seed_coefficient)) % 3
            pairs += 1
    require(pairs == expected_pairs, "dual:correlation_pair_count")
    meter.bump("correlation_pairs", pairs, "full_D_correlation")
    ordered = sorted(((key, value) for key, value in accum.items() if value),
                     key=lambda item: item[0])
    public = {"pair_count": pairs,
              "accumulator_digest": digest(sorted((list(k), v) for k, v in accum.items())),
              "selected": ([ordered[0][0][0], ordered[0][0][1], ordered[0][0][2], ordered[0][1]]
                           if ordered else None), "complete": True}
    require(CANONICAL_BATCH_CAP == 64, "batch:exact_cap")
    require(set(public) == {"pair_count", "accumulator_digest", "selected", "complete"} and
            "candidates" not in public, "batch:public_correlation_schema")
    require((public["selected"] is not None) == bool(ordered), "batch:roster_branch")
    return public, ordered


def correlate(ledger: BoundaryLedger, dual: dict[str, int], meter: Meter) -> dict[str, Any]:
    public, _private_candidates = correlate_private(ledger, dual, meter)
    return public
''',
    ),
    (
        b'''            dual, target_dot, active = dual_from_projection(self.basis, target, meter, remainder)
            corr = correlate(self.ledger, dual, meter)
            if not self.live_duals:
                self.live_duals.append({"query_id": query_id, "dual": dict(dual),
                                       "target": dict(target), "target_dot": target_dot,
                                       "correlation": corr})
            dual_digest = digest({"query_id": query_id, "dual": sorted(dual.items()),
                                  "target": target, "target_dot": target_dot,
                                  "correlation": corr})
            self.dual_chain.append({"index": len(self.dual_chain) + 1,
                                    "query_id": query_id, "digest": dual_digest})
            if corr["selected"] is not None:
                context, relation, text, coefficient = corr["selected"]; translation = decode_token(text)
                seed = self.ledger.seed_by_context_relation.get((context, relation))
                require(seed is not None, "boundary:selected_seed")
                raw_id = raw_key(context, relation, translation); column = seed.translate(translation)
                self.meter.reserve("active_keys", len(column), "boundary_rank_rise")
                reg = self.basis.add_boundary(column, raw_id)
                self.meter.bump("active_keys", len(column), "boundary_rank_rise")
                record = {"schema": "BOUNDARY_RANK_RISE", "query_id": query_id,
                          "rank_before": self.basis.rank() - 1, "rank_after": self.basis.rank(),
                          "selected": [context, relation, text, coefficient],
                          "column_digest": digest(column), "ledger_digest": digest(reg["ledger"]),
                          "dual_digest": digest(sorted(dual.items())),
                          "pair_count": corr["pair_count"], "accumulator_digest": corr["accumulator_digest"]}
                self._record(record)
                progress_once(meter, "CORRELATION", int(getattr(meter, "_a4_current_row", 0)),
                              self.basis.rank(), len(self.basis.boundary.pivots),
                              len(self.basis.k_items), 1)
                continue
''',
        b'''            dual, target_dot, active = dual_from_projection(self.basis, target, meter, remainder)
            corr, private_candidates = correlate_private(self.ledger, dual, meter)
            require(set(corr) == {"pair_count", "accumulator_digest", "selected", "complete"} and
                    "candidates" not in corr, "batch:public_digest_excludes_roster")
            if not self.live_duals:
                self.live_duals.append({"query_id": query_id, "dual": dict(dual),
                                       "target": dict(target), "target_dot": target_dot,
                                       "correlation": corr})
            dual_digest = digest({"query_id": query_id, "dual": sorted(dual.items()),
                                  "target": target, "target_dot": target_dot,
                                  "correlation": corr})
            dual_events_before = len(self.dual_chain)
            self.dual_chain.append({"index": len(self.dual_chain) + 1,
                                    "query_id": query_id, "digest": dual_digest})
            require(corr.get("complete") is True and len(self.dual_chain) == dual_events_before + 1,
                    "batch:one_dual_event_per_correlation")
            if corr["selected"] is not None:
                first_key, first_coefficient = private_candidates[0]
                require(corr["selected"] == [first_key[0], first_key[1], first_key[2], first_coefficient],
                        "batch:first_canonical_candidate")
                accepted = 0; accepted_nonzero_reductions = 0
                insertion_events_before = len(self.event_chain)
                fixed_dual_digest = digest(sorted(dual.items()))
                for (context, relation, text), coefficient in private_candidates:
                    if accepted == CANONICAL_BATCH_CAP: break
                    translation = decode_token(text)
                    seed = self.ledger.seed_by_context_relation.get((context, relation))
                    require(seed is not None, "boundary:selected_seed")
                    raw_id = raw_key(context, relation, translation); column = seed.translate(translation)
                    current_remainder, _current_correction = self.basis.combined.reduce(column)
                    if not current_remainder: continue
                    accepted_nonzero_reductions += 1
                    rank_before = self.basis.rank()
                    self.meter.reserve("active_keys", len(column), "boundary_rank_rise")
                    reg = self.basis.add_boundary(column, raw_id)
                    self.meter.bump("active_keys", len(column), "boundary_rank_rise")
                    require(self.basis.rank() == rank_before + 1,
                            "batch:current_combined_nonzero_rank_rise")
                    record = {"schema": "BOUNDARY_RANK_RISE", "query_id": query_id,
                              "rank_before": rank_before, "rank_after": self.basis.rank(),
                              "selected": [context, relation, text, coefficient],
                              "column_digest": digest(column), "ledger_digest": digest(reg["ledger"]),
                              "dual_digest": fixed_dual_digest,
                              "pair_count": corr["pair_count"], "accumulator_digest": corr["accumulator_digest"]}
                    self._record(record); accepted += 1
                require(0 < accepted <= CANONICAL_BATCH_CAP and
                        accepted_nonzero_reductions == accepted,
                        "batch:positive_current_combined_acceptance")
                require(len(self.event_chain) == insertion_events_before + accepted and
                        all(event.get("schema") == "BOUNDARY_RANK_RISE" and
                            event.get("query_id") == query_id
                            for event in self.event_chain[insertion_events_before:]),
                        "batch:one_event_per_insertion")
                progress_once(meter, "CORRELATION", int(getattr(meter, "_a4_current_row", 0)),
                              self.basis.rank(), len(self.basis.boundary.pivots),
                              len(self.basis.k_items), accepted)
                continue
            require(not private_candidates, "batch:zero_branch_has_roster")
''',
    ),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v14 producer: frozen v13 owner drift")
    owner_ns: dict[str, Any] = {
        "__name__": "_r07_a4_v13_owner",
        "__file__": str(OWNER.resolve()),
        "__package__": None,
        "__cached__": None,
    }
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v14 producer: audited site is not unique")
        raw = raw.replace(old, new)
    return raw


def main() -> None:
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(OWNER), "exec"), ns, ns)


if __name__ == "__main__":
    main()
