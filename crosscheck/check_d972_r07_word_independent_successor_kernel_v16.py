#!/usr/bin/env python3
"""Independent A4 v16 checker: v15 with canonical current-basis batching.

This restores the independent v15 arithmetic and recomputes its own complete
correlation accumulator, roster reductions, raw columns and insertions.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v15.py")
OWNER_BYTES = 10487
OWNER_SHA256 = "7779d545a679580130a0a191705f96e32834e67eaed37eb934e79aa7875a932d"

PATCHES = (
    (
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v13.py"',
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v14.py"',
    ),
    (
        b'''def correlate(boundary: Boundary, dual: dict[str, int], meter: Meter) -> dict[str, Any]:
    accum: dict[tuple[int, int, str], int] = {}; pairs = 0
    expected_pairs = sum(len(boundary.by_component.get(split_key(key)[:2], ()))
                         for key in dual)
    meter._a4_correlation_rounds = int(getattr(meter, "_a4_correlation_rounds", 0)) + 1
    meter.reserve("correlation_pairs", expected_pairs, "checker.full_D_correlation")
    for key, coefficient in dual.items():
        context, component, text = split_key(key); g = decode_token(text)
        for seed, h, seed_coefficient in boundary.by_component.get((context, component), []):
            inverse_h = boundary.inverses[context, h]; translation = seed.q.mul(g, inverse_h)
            require(seed.q.mul(translation, h) == g, "checker:translation_product")
            target = (context, seed.relation, token(translation)); accum[target] = (accum.get(target, 0) + int(coefficient) * int(seed_coefficient)) % 3
            pairs += 1
    require(pairs == expected_pairs, "checker:correlation_pair_count")
    meter.bump("correlation_pairs", pairs, "checker.full_D_correlation")
    nonzero = sorted(((key, value) for key, value in accum.items() if value), key=lambda item: item[0])
    return {"pair_count": pairs, "accumulator_digest": digest(sorted((list(key), value) for key, value in accum.items())),
            "selected": ([nonzero[0][0][0], nonzero[0][0][1], nonzero[0][0][2], nonzero[0][1]] if nonzero else None),
            "complete": True}
''',
        b'''CANONICAL_BATCH_CAP = 64


def correlate_private(boundary: Boundary, dual: dict[str, int], meter: Meter) -> tuple[dict[str, Any], list[tuple[tuple[int, int, str], int]]]:
    accum: dict[tuple[int, int, str], int] = {}; pairs = 0
    expected_pairs = sum(len(boundary.by_component.get(split_key(key)[:2], ()))
                         for key in dual)
    meter._a4_correlation_rounds = int(getattr(meter, "_a4_correlation_rounds", 0)) + 1
    meter.reserve("correlation_pairs", expected_pairs, "checker.full_D_correlation")
    for key, coefficient in dual.items():
        context, component, text = split_key(key); g = decode_token(text)
        for seed, h, seed_coefficient in boundary.by_component.get((context, component), []):
            inverse_h = boundary.inverses[context, h]; translation = seed.q.mul(g, inverse_h)
            require(seed.q.mul(translation, h) == g, "checker:translation_product")
            target = (context, seed.relation, token(translation)); accum[target] = (accum.get(target, 0) + int(coefficient) * int(seed_coefficient)) % 3
            pairs += 1
    require(pairs == expected_pairs, "checker:correlation_pair_count")
    meter.bump("correlation_pairs", pairs, "checker.full_D_correlation")
    nonzero = sorted(((key, value) for key, value in accum.items() if value), key=lambda item: item[0])
    public = {"pair_count": pairs,
              "accumulator_digest": digest(sorted((list(key), value) for key, value in accum.items())),
              "selected": ([nonzero[0][0][0], nonzero[0][0][1], nonzero[0][0][2], nonzero[0][1]]
                           if nonzero else None), "complete": True}
    require(CANONICAL_BATCH_CAP == 64, "checker:batch_exact_cap")
    require(set(public) == {"pair_count", "accumulator_digest", "selected", "complete"} and
            "candidates" not in public, "checker:batch_public_correlation_schema")
    require((public["selected"] is not None) == bool(nonzero), "checker:batch_roster_branch")
    return public, nonzero


def correlate(boundary: Boundary, dual: dict[str, int], meter: Meter) -> dict[str, Any]:
    public, _private_candidates = correlate_private(boundary, dual, meter)
    return public
''',
    ),
    (
        b'''            dual, target_dot = dual_pullback(self.basis, target, self.meter, remainder); correlation = correlate(self.boundary, dual, self.meter)
            if not self.live_duals:
                # Keep one bounded actual dual sample.  The complete history
                # is represented by dual_event_chain/epoch digest entries.
                self.live_duals.append({"query_id": query_id, "dual": dict(dual),
                                        "target": dict(target), "target_dot": target_dot,
                                        "correlation": correlation})
            dual_digest = digest({"query_id": query_id, "dual": sorted(dual.items()),
                                  "target": target, "target_dot": target_dot,
                                  "correlation": correlation})
            self.dual_chain.append({"index": len(self.dual_chain) + 1,
                                    "query_id": query_id, "digest": dual_digest})
            if correlation["selected"] is not None:
                context, relation, text, coefficient = correlation["selected"]; seed = self.boundary.by_key[context, relation]
                translated = decode_token(text); column = seed.translate(translated); raw_identity = raw_key(context, relation, translated)
                self.meter.reserve("active_keys", len(column), "checker.boundary_rank_rise")
                added = self.basis.add_boundary(column, raw_identity)
                self.meter.bump("active_keys", len(column), "checker.boundary_rank_rise")
                result = {"schema": "BOUNDARY_RANK_RISE", "query_id": query_id, "rank_before": self.basis.rank() - 1,
                          "rank_after": self.basis.rank(), "selected": [context, relation, text, coefficient],
                          "column_digest": digest(column), "ledger_digest": digest(added["ledger"]),
                          "dual_digest": digest(sorted(dual.items())), "pair_count": correlation["pair_count"],
                          "accumulator_digest": correlation["accumulator_digest"]}; self.record(result)
                progress_once(self.meter, "CORRELATION", int(getattr(self.meter, "_a4_current_row", 0)),
                              self.basis.rank(), len(self.basis.bspace.pivots),
                              len(self.basis.k_items), 1)
                continue
''',
        b'''            dual, target_dot = dual_pullback(self.basis, target, self.meter, remainder)
            correlation, private_candidates = correlate_private(self.boundary, dual, self.meter)
            require(set(correlation) == {"pair_count", "accumulator_digest", "selected", "complete"} and
                    "candidates" not in correlation, "checker:batch_public_digest_excludes_roster")
            if not self.live_duals:
                # Keep one bounded actual dual sample.  The complete history
                # is represented by dual_event_chain/epoch digest entries.
                self.live_duals.append({"query_id": query_id, "dual": dict(dual),
                                        "target": dict(target), "target_dot": target_dot,
                                        "correlation": correlation})
            dual_digest = digest({"query_id": query_id, "dual": sorted(dual.items()),
                                  "target": target, "target_dot": target_dot,
                                  "correlation": correlation})
            dual_events_before = len(self.dual_chain)
            self.dual_chain.append({"index": len(self.dual_chain) + 1,
                                    "query_id": query_id, "digest": dual_digest})
            require(correlation.get("complete") is True and
                    len(self.dual_chain) == dual_events_before + 1,
                    "checker:batch_one_dual_event_per_correlation")
            if correlation["selected"] is not None:
                first_key, first_coefficient = private_candidates[0]
                require(correlation["selected"] == [first_key[0], first_key[1], first_key[2], first_coefficient],
                        "checker:batch_first_canonical_candidate")
                accepted = 0; accepted_nonzero_reductions = 0
                insertion_events_before = len(self.event_chain)
                fixed_dual_digest = digest(sorted(dual.items()))
                for (context, relation, text), coefficient in private_candidates:
                    if accepted == CANONICAL_BATCH_CAP: break
                    seed = self.boundary.by_key[context, relation]
                    translated = decode_token(text); column = seed.translate(translated)
                    raw_identity = raw_key(context, relation, translated)
                    current_remainder, _current_correction = self.basis.combined.reduce(column)
                    if not current_remainder: continue
                    accepted_nonzero_reductions += 1
                    rank_before = self.basis.rank()
                    self.meter.reserve("active_keys", len(column), "checker.boundary_rank_rise")
                    added = self.basis.add_boundary(column, raw_identity)
                    self.meter.bump("active_keys", len(column), "checker.boundary_rank_rise")
                    require(self.basis.rank() == rank_before + 1,
                            "checker:batch_current_combined_nonzero_rank_rise")
                    result = {"schema": "BOUNDARY_RANK_RISE", "query_id": query_id,
                              "rank_before": rank_before, "rank_after": self.basis.rank(),
                              "selected": [context, relation, text, coefficient],
                              "column_digest": digest(column), "ledger_digest": digest(added["ledger"]),
                              "dual_digest": fixed_dual_digest, "pair_count": correlation["pair_count"],
                              "accumulator_digest": correlation["accumulator_digest"]}
                    self.record(result); accepted += 1
                require(0 < accepted <= CANONICAL_BATCH_CAP and
                        accepted_nonzero_reductions == accepted,
                        "checker:batch_positive_current_combined_acceptance")
                require(len(self.event_chain) == insertion_events_before + accepted and
                        all(event.get("schema") == "BOUNDARY_RANK_RISE" and
                            event.get("query_id") == query_id
                            for event in self.event_chain[insertion_events_before:]),
                        "checker:batch_one_event_per_insertion")
                progress_once(self.meter, "CORRELATION", int(getattr(self.meter, "_a4_current_row", 0)),
                              self.basis.rank(), len(self.basis.bspace.pivots),
                              len(self.basis.k_items), accepted)
                continue
            require(not private_candidates, "checker:batch_zero_branch_has_roster")
''',
    ),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v16 checker: frozen v15 owner drift")
    owner_ns: dict[str, Any] = {
        "__name__": "_r07_a4_v15_owner",
        "__file__": str(OWNER.resolve()),
        "__package__": None,
        "__cached__": None,
    }
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v16 checker: audited site is not unique")
        raw = raw.replace(old, new)
    return raw


def main() -> None:
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(OWNER), "exec"), ns, ns)


if __name__ == "__main__":
    main()
