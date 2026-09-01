# R07 deadline-flush short batch (v427)

Author: Sol / 2026-09-02

Status: paper theorem refining v422/v424 after the measured Task453 resource
run.  It shows that literal-certified rank rises already accumulated in an
open batch may be closed and sealed before a soft deadline, instead of being
discarded merely because the nominal batch cap was not reached.  It asserts
no existing hidden rise, COMMON word, negative result, fake, or Ihara
witness.  `verified=false`.

## 1. Failure mode exposed by the completed run

Task453 run `33516227668` completed successfully as a workflow and its
independent checker accepted the emitted resource receipt, but the durable
state stayed

```text
rank=51, accepted_count=8, batch_count=0, round=9
reason=UNKNOWN_RESOURCE:tau_free_candidate:time_limit
```

The producer spent about one hour 49 minutes after selective setup inside
the candidate scan.  Its batch cap was 64.  Since a batch was durable only
after reaching its cap, every literal-certified row accumulated before the
deadline, if any, was absent from the checkpoint.  This is an honest resource
result, but it is the wrong durability boundary.

The same issue can recur with cap 16 at a later, more dependent rank.  Merely
making the cap smaller trades less loss for more dual recomputations; it does
not eliminate deadline loss.

## 2. Two deadlines and one atomic boundary

For one invocation choose

\[
 t_{\rm search}<t_{\rm hard}<t_{\rm external}.
\tag{2.1}
\]

The interval `t_hard - t_search` is a measured reserve for one dual update,
receipt construction, canonical serialization, `fsync`, and atomic replace.
The external supervisor leaves a further kill margin.  RSS has an analogous
soft threshold below its hard supervisor threshold.

Candidate enumeration checks the **soft** boundary.  On reaching it, control
returns to the batch owner with the current list `rows`, rather than escaping
directly to the outer resource handler.  Each element of `rows` has already
passed all v424 retained-row gates and exactly one actual `add`; no untested
proposal is present.

The owner then performs exactly one of the following atomic transitions.

1. If `rows` is empty, return the previous `last_closed`.
2. If `1 <= len(rows) <= 16`, compute the ordinary post-batch dual/remainder,
   append a closed receipt of that actual length, append the segment counts,
   seal it canonically, `fsync`, atomically replace the checkpoint, and only
   then set `last_closed` to the new state.
3. If the close itself fails or crosses the hard boundary, leave the previous
   checkpoint untouched and return/reference only that previous closed state.

The resource result records whether the soft flush committed or fell back.
It never serializes the transient in-memory echelon as a closed state.

## 3. Mathematical soundness of an early close

### Theorem 3.1 (ANY NONEMPTY CERTIFIED PREFIX IS A VALID BATCH)

Let `dual` be the fixed anchor at the start of a Task451/v424 batch.  Suppose
the producer successively accepts rows

\[
 r_1,\ldots,r_k,\qquad 1\leq k\leq16,
\tag{3.1}
\]

where every row has nonzero anchor pairing, passes all literal and side
gates, and raises the actual physical echelon at its insertion.  Then closing
the batch after `r_k` yields a valid physical state and a valid next dual.
No premise requires `k=16`.

#### Proof

The physical state after (3.1) is obtained by the same chronological `add`
operations used in an ordinary full batch.  Each insertion was certified
independent in the state in which it occurred.  The update operation depends
only on the resulting echelon and fixed target, so applying it after `k`
rows returns exactly the dual/remainder of that valid span.  The value 16 is
only an operational upper bound controlling durability and amortization; it
does not occur in the linear-algebra invariant.  \(\square\)

An early update may change which candidate is selected after resume compared
with a hypothetical 16-row continuation.  This is harmless: the lane is
positive discovery, not a prescribed exhaustive order.  Every later retained
row is again replayed against its actual anchor, and no miss is promoted.

### Corollary 3.2 (RESOURCE FLUSH DOES NOT WEAKEN THE FINAL CERTIFICATE)

If a final independent checker replays every variable-length closed batch
from canonical `C99`, including its anchors, literal rows, pivots, and post
duals, a COMMON terminal has the same force as under fixed-size batches.
Intermediate soft-flush resource receipts remain candidates until that
replay.

## 4. Required owner/checker contract

The narrow successor to the audited actual rank-99 owner must satisfy:

- `batch_cap=16` means `1 <= closed_row_count <= 16`, not exactly 16;
- the per-invocation cap remains at most 64 new rises and counts every
  deadline-flushed rise;
- `SOFT_FLUSH` is caught inside the batch owner; unrelated exceptions are not
  converted to resource results;
- the old `last_closed` is written before heavy work and remains the fallback;
- a committed short batch has the same anchor/post/row/pivot/literal gates as
  a cap-sized batch;
- segment start/end counts and seals include the actual short length;
- the independent checker accepts lengths 1--16 but rejects zero, 17, count
  drift, an unsealed open batch, or a resource receipt pointing past the last
  atomic checkpoint; and
- bounded fixtures interrupt after 1 and 15 accepted rows, compare the
  resumed state with uninterrupted execution at the same early-close point,
  and force a close failure to prove fallback to the preceding seal.

The driver should combine this with v426's discovery-chain policy: a
resource segment may feed the next candidate segment without paying a full
semantic checker each time, while a COMMON result must receive the complete
independent prefix replay.

## 5. v220 consequence

```text
Task453 completed workflow:                 cross-checked RESOURCE at rank 51
Task453 new durable rises:                  0
fixed-size open-batch loss:                 measured execution defect
deadline-flush theorem:                     paper closed here
rank-99 owner implementation:               pending Task472 audit/successor
A0 actual COMMON:                           still 0/1
```

This repair is materially different from a larger checkpoint framework: it
changes one exception boundary and permits the already defined receipt to
close at its actual positive length.  No full boundary reconstruction,
negative exhaustion, or persistent 176-MB selector cache is part of the
immediate change.

`R07_DEADLINE_FLUSH_SHORT_BATCH_V427_PAPER_GRADE`
