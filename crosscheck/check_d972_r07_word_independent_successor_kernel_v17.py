#!/usr/bin/env python3
"""Independent A4 v17 checker: v16 with an examined-candidate cap.

The independent checker keeps the complete correlation and canonical private
roster, but decodes/translates/current-reduces only its first at most 64
candidates.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v16.py")
OWNER_BYTES = 12407
OWNER_SHA256 = "1470f12585d8ed16bb1dea0480787ba99d80592d3a034215cbbde20748f6090e"
OWNER_GENERATED_BYTES = 265792
OWNER_GENERATED_SHA256 = "60973559b2f139dad471059b99746902a17b5ad5e52fba81288564303b8b05ec"
RESULT_GENERATED_BYTES = 266860
RESULT_GENERATED_SHA256 = "78409970ed60b7e5d97335592275716adb298ed85e65b49829c66bacc98f1d92"

PATCHES = (
    (
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v14.py"',
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v15.py"',
    ),
    (
        b'''                accepted = 0; accepted_nonzero_reductions = 0
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
''',
        b'''                examined_limit = min(CANONICAL_BATCH_CAP, len(private_candidates))
                require(0 < examined_limit <= CANONICAL_BATCH_CAP and
                        examined_limit == min(64, len(private_candidates)),
                        "checker:batch_exact_examined_limit")
                accepted = 0; examined = 0; accepted_nonzero_reductions = 0
                first_canonical_accepted = False
                insertion_events_before = len(self.event_chain)
                fixed_dual_digest = digest(sorted(dual.items()))
                for candidate_index in range(examined_limit):
                    (context, relation, text), coefficient = private_candidates[candidate_index]
                    examined += 1
                    require(examined == candidate_index + 1 and examined <= CANONICAL_BATCH_CAP,
                            "checker:batch_examined_counter_bound")
                    seed = self.boundary.by_key[context, relation]
                    translated = decode_token(text); column = seed.translate(translated)
                    raw_identity = raw_key(context, relation, translated)
                    current_remainder, _current_correction = self.basis.combined.reduce(column)
                    if candidate_index == 0:
                        require(bool(current_remainder),
                                "checker:batch_first_canonical_current_independence")
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
                    if candidate_index == 0: first_canonical_accepted = True
                require(examined == examined_limit == min(64, len(private_candidates)),
                        "checker:batch_examined_equals_canonical_prefix")
                require(first_canonical_accepted and
                        0 < accepted <= examined <= CANONICAL_BATCH_CAP and
                        accepted_nonzero_reductions == accepted,
                        "checker:batch_positive_bounded_current_combined_acceptance")
''',
    ),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v17 checker: frozen v16 owner drift")
    owner_ns: dict[str, Any] = {
        "__name__": "_r07_a4_v16_owner",
        "__file__": str(OWNER.resolve()),
        "__package__": None,
        "__cached__": None,
    }
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if (len(raw) != OWNER_GENERATED_BYTES or
            hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256):
        raise SystemExit("v17 checker: frozen v16 generated source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v17 checker: audited site is not unique")
        raw = raw.replace(old, new)
    if (len(raw) != RESULT_GENERATED_BYTES or
            hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256):
        raise SystemExit("v17 checker: resulting generated source drift")
    return raw


def main() -> None:
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(OWNER), "exec"), ns, ns)


if __name__ == "__main__":
    main()
