#!/usr/bin/env python3
"""A4 v15 owner: v14 with an exact canonical examined-candidate cap.

The complete correlation and private canonical roster are unchanged.  Only
the first min(64, roster length) candidates may be decoded, translated and
reduced against the current combined basis.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


OWNER = Path(__file__).with_name("d972_r07_word_independent_successor_kernel_v14.py")
OWNER_BYTES = 11918
OWNER_SHA256 = "0c7595d50765062a6d2270d5b40c44b753f0ea4a96311795994a3c2502fe0c2c"
OWNER_GENERATED_BYTES = 225853
OWNER_GENERATED_SHA256 = "952e559d363ae6c5261a057438ad3bfdfb1d85cc9f4417d714b85ed66fa9239c"
RESULT_GENERATED_BYTES = 226857
RESULT_GENERATED_SHA256 = "fe3c23ffb4c5c952f99eceba73cb8594885dbadd9d2c4bd50d8b28c173e46940"

PATCHES = (
    (
        b'''                accepted = 0; accepted_nonzero_reductions = 0
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
''',
        b'''                examined_limit = min(CANONICAL_BATCH_CAP, len(private_candidates))
                require(0 < examined_limit <= CANONICAL_BATCH_CAP and
                        examined_limit == min(64, len(private_candidates)),
                        "batch:exact_examined_limit")
                accepted = 0; examined = 0; accepted_nonzero_reductions = 0
                first_canonical_accepted = False
                insertion_events_before = len(self.event_chain)
                fixed_dual_digest = digest(sorted(dual.items()))
                for candidate_index in range(examined_limit):
                    (context, relation, text), coefficient = private_candidates[candidate_index]
                    examined += 1
                    require(examined == candidate_index + 1 and examined <= CANONICAL_BATCH_CAP,
                            "batch:examined_counter_bound")
                    translation = decode_token(text)
                    seed = self.ledger.seed_by_context_relation.get((context, relation))
                    require(seed is not None, "boundary:selected_seed")
                    raw_id = raw_key(context, relation, translation); column = seed.translate(translation)
                    current_remainder, _current_correction = self.basis.combined.reduce(column)
                    if candidate_index == 0:
                        require(bool(current_remainder), "batch:first_canonical_current_independence")
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
                    if candidate_index == 0: first_canonical_accepted = True
                require(examined == examined_limit == min(64, len(private_candidates)),
                        "batch:examined_equals_canonical_prefix")
                require(first_canonical_accepted and
                        0 < accepted <= examined <= CANONICAL_BATCH_CAP and
                        accepted_nonzero_reductions == accepted,
                        "batch:positive_bounded_current_combined_acceptance")
''',
    ),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v15 producer: frozen v14 owner drift")
    owner_ns: dict[str, Any] = {
        "__name__": "_r07_a4_v14_owner",
        "__file__": str(OWNER.resolve()),
        "__package__": None,
        "__cached__": None,
    }
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if (len(raw) != OWNER_GENERATED_BYTES or
            hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256):
        raise SystemExit("v15 producer: frozen v14 generated source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v15 producer: audited site is not unique")
        raw = raw.replace(old, new)
    if (len(raw) != RESULT_GENERATED_BYTES or
            hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256):
        raise SystemExit("v15 producer: resulting generated source drift")
    return raw


def main() -> None:
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(OWNER), "exec"), ns, ns)


if __name__ == "__main__":
    main()
