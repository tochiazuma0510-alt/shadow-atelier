# Sol(max) Task 573: adversarial audit of packed GF(3) stream worker v2

Author: Sol / 2026-09-03

## 1. Role and exact scope

Act as an independent mathematical/software auditor.  Audit the complete
Task572 instruction, its reply, and exactly these candidate files:

1. `search/d972_packed_gf3_stream_worker_v2.c`;
2. `search/d972_packed_gf3_stream_worker_v2.py`;
3. `search/check_d972_packed_gf3_stream_worker_v2.py`;
4. `sol/luna_reply_572_r07_packed_gf3_stream_worker_v2.md`.

Write only `sol/sol_reply_573_audit_r07_packed_gf3_stream_worker_v2.md`.
Do not edit code, Task565, v220, workflows or provenance.  Do not dispatch
GHA or run parallel Python.  This is a bounded audit of the primitive, not a
request for extra features or production proof.

## 2. Load-bearing questions

Determine whether the C service, not merely the Python emulator, implements
the exact v452/v4 transducer and can accept the registered grade-two source
and physical envelopes.  Check all of:

1. packed GF(3) first-lead reduction, coefficient two, normalization,
   insertion-order pivots, nonmonotone leads and exact expression semantics;
2. dynamic offer/response: an accepted result can generate later actor
   offers, with the opaque offer ID bound unambiguously;
3. binary transcript and offsets are exactly `record starts + one EOF`, for
   zero, one, two and many offers, and chronological pivots are checked;
4. an interrupted compiled process really resumes after multiple offers,
   including companion mode, without replaying committed offers;
5. committed-prefix authentication rejects corruption even when an
   uncommitted suffix exists, while truncating only that suffix;
6. Linux and Windows path handling, 64-bit sizes, checked allocation/arithmetic,
   defined C11 memory behavior, file error propagation and atomic manifest
   publication;
7. rank/offer/byte caps fail as `UNKNOWN_RESOURCE` without blocking dependent
   offers merely because rank reached its maximum;
8. bounded memory: accepted basis + lead map + one work row/current reductions,
   with no historical-offer or all-reduction retention;
9. bounded runtime: look specifically for repeated whole-file hashing/fsync,
   quadratic checkpoint work, unnecessary full copies, blocked undrained
   pipes, or other processing which makes 177432 offers infeasible;
10. wrapper has no production timeout/fallback and cannot deadlock on stderr;
11. the independent checker is genuinely dense/helper-independent and its
    fixtures exercise the compiled paths they claim.  Emulator-only success
    must remain labelled as such.

The parent static read found possible attack surfaces which must be decided,
not assumed: separator choice in `path_join`, two offsets appended per offer,
whole-file checkpointing after each offer, authentication when `got>want`,
companion-basis reconstruction on resume, stale byte-cap lengths, rank-cap
handling, and a piped but unread stderr stream.  Confirm or refute each from
the exact source and seek any additional load-bearing defect.

## 3. Required report

Record exact input byte counts/SHA-256, commands, bounded observations and a
minimal repair list.  Distinguish algebraic correctness, protocol correctness,
real resume, resource feasibility and fixture coverage.  Do not demand style
changes, unrelated refactors, exhaustive production computation, or a new
mathematical universe.

End with exactly one verdict:

```text
PACKED_GF3_STREAM_WORKER_V2_AUDIT_PASS
PACKED_GF3_STREAM_WORKER_V2_AUDIT_PASS_AFTER_REPAIR
PACKED_GF3_STREAM_WORKER_V2_AUDIT_FAIL
```

State explicitly that no Task565 integration, GHA production, grade
membership, A0, COMMON, cofinal lift, fake or Ihara conclusion is made.
