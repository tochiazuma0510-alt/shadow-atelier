# R07 task192 cumulative-pair semantics and persistent-pool consequence v256

Author: Sol / 2026-08-28

Status: exact audit correcting the performance interpretation of v253.  The
boundary restart classification in v253 remains correct; the scale of the
discarded current-epoch prefix is corrected below.  No A0, lift, fake, or
Ihara conclusion is declared.

## 1. Exact counters

The authenticated run-33149728601 checkpoint has

```text
rank / retained_columns                    2,896
monitor.boundary_pairs                 3,145,728
progress.boundary.pair_attempts         3,145,088
progress.boundary.complete                  false
progress.boundary.restart_pair_cursor           0
current_dual nonzero entries                 1,188
current_dual typed support              (B,c)=(1,1) only
cached boundary descriptor count               104
```

The raw checkpoint is 86,368,039 bytes with SHA-256
`c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab`.
The source manifest is
`ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json`.

Therefore the exact number attempted **inside the interrupted current dual
epoch** is

\[
  3{,}145{,}728-3{,}145{,}088=640.                                  \tag{1.1}
\]

It is not 3,145,728.

## 2. Why `pair_attempts` is cumulative

When the dual changes, the v1 owner writes

```python
"pair_attempts": self.monitor.counters["boundary_pairs"]
```

before calling the boundary oracle
(`search/d972_r07_positive_common_word_colgen_v1.py`, lines 1691--1704).
The monitor counter is global and cumulative.  Only after the full oracle
returns does line 1706 overwrite `pair_attempts` with the then-current
cumulative total.  A wall stop inside the oracle leaves the epoch-start value
in `progress.boundary.pair_attempts`.

Thus v253 correctly proved that the restarted oracle has no reusable cursor
or accumulator, but its Section 3 must not be read as saying that the whole
3.145-million cumulative history belongs to the interrupted epoch.  The
discarded algebraic prefix is exactly (1.1); checkpoint/rank-zero rebuild work
is a separate restart cost.

Two independent magnitude checks agree:

- the 3,145,728 cumulative pairs were accumulated while retaining 2,896
  columns, averaging about 1,086.23 monitor pairs per retained column; and
- one epoch can use at most 104 times 1,188 descriptor/support pairs, so the
  cumulative value cannot be the current epoch's pair count.

## 3. Consequence for run 33163964747

The run is still accurately called `RUNNING-BOUNDARY-RESTART`: its current
epoch restarts at pair zero.  But it repeats 640 current-epoch pair attempts,
not the preceding 3,145,088 cumulative attempts.  If rank-zero replay reaches
the oracle before the fresh wall stop, it can finish that epoch and continue
the serial ladder.  A later dual change starts a genuinely new epoch and its
pairs are not duplicates of the old dual's pairs.

The cumulative 8,000,000 cap remains load-bearing, but the immediate duplicate
charge from this checkpoint is 640.  It is therefore premature to diagnose
the running resume as certain repeated-prefix stagnation.

## 4. Correct production acceleration target

The observed workload is thousands of short, serially dependent frozen-dual
epochs, not one three-million-pair epoch.  A production adapter must therefore:

1. keep one persistent process pool across rank/dual epochs rather than pay a
   new process-spawn cost for every boundary call;
2. expand the exact descriptor-times-typed-support **global pair roster** and
   partition pair indices, not merely the 104 outer descriptor indices;
3. broadcast/bind the new dual support and epoch identity after each serial
   rank change, while keeping descriptor/group data resident where safe;
4. return one exact merged answer to the serial rank owner before the next
   epoch; and
5. use the v254/v255 cursor state only if an individual epoch itself cannot
   finish within the wall budget.

Task303's process kernel remains a valid algebraic SELFTEST candidate.  Its
production adapter must not naively instantiate a fresh `Pool` at each of the
approximately 2,896 observed rank transitions, and its fixture descriptors
must be replaced by the actual expanded pair roster.

```text
V253 BOUNDARY-RESTART CLASSIFICATION:        RETAINED
CURRENT-EPOCH DISCARDED PAIRS:               640
3,145,728 INTERPRETATION:                    CUMULATIVE ACROSS RANK EPOCHS
PERSISTENT WORKER POOL REQUIRED:             PRODUCTION PERFORMANCE CONTRACT
TASK303 SELFTEST / PRODUCTION ADAPTER:        PENDING GHA / NOT IMPLEMENTED
A0 COMMON + INDEPENDENT ACCEPTANCE:           0/1
WITNESS / FAKE / IHARA:                       UNCHANGED
```

`R07_TASK192_CUMULATIVE_PAIRS_PERSISTENT_POOL_V256_STATIC_AUDIT`

