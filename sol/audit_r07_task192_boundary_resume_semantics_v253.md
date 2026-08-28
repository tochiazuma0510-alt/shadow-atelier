# R07 task192 boundary-resume semantics audit v253

Author: Sol / 2026-08-28

Status: exact static control-flow audit of the authenticated task192 v3
producer and task298 v2 transport.  It changes no mathematical result and
does not declare A0, a lift, a fake, or an Ihara witness.

## 1. Result

Task298 genuinely transports and replays the 2,896 retained columns, rebuilds
the echelon basis from rank zero, recomputes the current dual, and starts a
fresh wall clock with the original authenticated limits.  It does **not**
resume the interrupted boundary correlation at pair 3,145,089.

The transported boundary state is exactly

```text
complete             false
pair_attempts         3,145,088
restart_pair_cursor   0
```

while the cumulative monitor counter is 3,145,728.  Thus run 33163964747 is
an exact rank/column/dual resume with a **boundary-epoch restart**, not a
pair-cursor continuation.

## 2. Code trace

The task298 driver authenticates the values above at
`search/d972_r07_normalized_exact_common_word_cached_resume_gha_driver_v2.g`
lines 152 and 175.  It intentionally preserves `restart_pair_cursor=0`.

The v3 rank-zero firewall recomputes the dual.  If the stored safe progress
and dual match, it preserves the stored boundary object
(`search/d972_r07_normalized_exact_common_word_cached_v3.py`, lines
1501--1559).  This preservation does not implement a cursor.

At the actual boundary call, `BoundaryDescriptorCache.correlation` (lines
1023--1066) creates fresh empty `accumulated` and `contributors` dictionaries
and iterates every descriptor/support pair from the beginning.  It neither
accepts the progress object nor reads `pair_attempts` or
`restart_pair_cursor`.  The v1 owner then marks the boundary complete only
after this whole call returns
(`search/d972_r07_positive_common_word_colgen_v1.py`, lines 1694--1706).

Consequently, an interrupted call has no semantically reusable partial sum.
On resume, the old monitor counters are cumulative but the wall clock is new;
the pair loop itself starts at global pair zero.

## 3. Consequences

1. This is not a soundness defect.  A completed rerun computes the same full
   F3 correlation and exact lexicographic active column.
2. It is a performance defect for repeated wall stops.  With the same machine
   and 10,800-second cap, the rerun may reach approximately the same prefix
   and stop again without advancing the boundary cursor.
3. The cumulative 8,000,000 pair cap can also be consumed by repeated work.
4. Therefore the current run may still succeed through runtime variance, but
   it must not be reported as continuing at pair 3,145,089.

## 4. Required production repair

A production parallel adapter must bind one frozen dual digest and one exact
global pair order, and then do one of the following:

- finish the whole correlation by exact parallel map/reduce within one wall
  budget; or
- checkpoint only completed deterministic batches, retaining the next global
  pair cursor plus the authenticated partial F3 accumulator and contributor
  records.

For a cursor-bearing implementation, restart must reconstruct the prefix
directly from the immutable descriptors and dual (or independently replay its
sealed partial state), process a disjoint suffix, and finally reproduce the
serial v3 accumulator, winner, translated row, and direct scalar exactly.
Adaptive rank changes and dual changes remain outside the workers and reset
the boundary epoch.

The task303 parallel-kernel SELFTEST is therefore useful but insufficient by
itself: an authenticated v3 production adapter and resumable epoch state are
still required before it accelerates A0.

```text
TASK298 COLUMN/RANK/DUAL TRANSPORT:       EXACT STATIC PATH
TASK298 MID-BOUNDARY PAIR RESUME:         NO
RUN 33163964747:                          RUNNING, BOUNDARY RESTART
MATHEMATICAL A0 TERMINAL:                 NONE
TASK303 PARALLEL KERNEL:                  IMPLEMENTATION IN PROGRESS
PRODUCTION CURSOR/PARTIAL ADAPTER:        REQUIRED
WITNESS / FAKE / IHARA:                   UNCHANGED
```

`R07_TASK192_BOUNDARY_RESUME_SEMANTICS_V253_STATIC_AUDIT`
