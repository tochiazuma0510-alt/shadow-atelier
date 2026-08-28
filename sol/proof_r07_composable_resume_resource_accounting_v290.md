# R07 composable resume resource accounting v290

Author: Sol / 2026-08-29

Status: paper-grade checkpoint accounting theorem for the A4-v5 and A0-v10
resume paths.  V288 identifies the lossless mathematical state but leaves the
composition law for work counters implicit.  This note separates completed
semantic work, restore validation, current-invocation resources, and physical
peaks.  It prevents both cap erasure and the opposite error in which a fresh
GHA continuation immediately inherits an exhausted wall clock.  It does not
accept either implementation, execute a workflow, compute a lift, or prove a
fake/Ihara statement.  `verified=false`.

## 1. Four counter types

At a checkpoint frontier write

\[
 \mathfrak C=(S,V,H,P).
\tag{1.1}
\]

The four components have different composition laws.

1. \(S\) contains **completed semantic additive counters**: authority rows,
   row-piece products, sparse reductions, dual/correlation pairs, queue
   actions, DAG-node insertions, and every other transition count whose old
   work must not disappear on resume.
2. \(V\) contains **restore-validation additive counters**: bytes opened to
   authenticate the checkpoint, DAG recurrences checked, saved sparse
   insertion events replayed, queue relations checked, and canaries
   reconstructed.  These operations validate \(S\); they are not repetitions
   of its mathematical transitions.
3. \(H\) contains **current-invocation resources**: elapsed wall time, current
   process input traffic, and invocation-local timeout/deadline data.  A new
   authenticated GHA continuation receives a new driver budget, so its wall
   clock starts at zero.
4. \(P\) contains **physical peaks and gauges**: RSS peak, largest sidecar,
   current sidecar size, maximum sparse support, and similar quantities.
   A peak composes by maximum, while a current gauge is replaced by the new
   measured value.

Every key is registered with exactly one type.  An unregistered key is an
input error; treating all keys by one blanket `max` or one blanket sum is
invalid.

## 2. Resume transition

Let \((S_0,V_0,H_0,P_0)\) be the authenticated saved state.  During the new
invocation let

\[
 \Delta V,\qquad \Delta S,\qquad H_1,\qquad P_1
\tag{2.1}
\]

be, respectively, the restore checks, new semantic transitions, current host
resources, and newly observed physical gauges.  The continuation state is

\[
 \boxed{
 S_1=S_0+\Delta S,\qquad
 V_1=V_0+\Delta V.}
\tag{2.2}
\]

For every peak key \(p\),

\[
 P_1^{\rm history}(p)=\max(P_0^{\rm history}(p),P_1^{\rm run}(p)).
\tag{2.3}
\]

The current wall deadline is checked against \(H_1\), not against
\(H_0+H_1\).  For audit reporting one may additionally retain

\[
 H^{\rm history}=H_0^{\rm history}\mathbin{\|}H_1
\tag{2.4}
\]

as an ordered list, or report its sum, but that historical statistic is not
silently substituted for the driver's per-run timeout.

The checkpoint-open bytes belong to \(\Delta V\) and \(H_1\), not to
\(\Delta S\).  Likewise reconstructing the echelons from saved normalized
rows belongs to \(\Delta V\); evaluating old authority words would be a
forbidden semantic prefix replay, not validation.

## 3. Cap registry

Every cap declares its scope.

- A **global semantic cap** is tested against \(S_0+\Delta S\).  This prevents
  repeated resume from resetting a bound on candidate words, queue actions,
  DAG nodes, sparse operations, or ancestry expansion.
- A **per-invocation host cap** is tested against \(H_1\).  This includes the
  driver wall timeout and current-process input/RSS enforcement needed to
  make a continuation possible.
- A **physical object cap** is tested before allocation against the proposed
  current gauge, for example the next checkpoint byte size.  The total bytes
  serialized over all checkpoints is a separate additive audit key and must
  not be confused with current sidecar size.
- A **historical peak cap**, if explicitly required, is tested against
  (2.3).  Otherwise (2.3) is reported as provenance while the current
  invocation still obeys its own host cap.

The cap registry and its version are part of the authority identity.  A
resume may lower a cap only if the saved state already satisfies it; it may
not raise a load-bearing semantic cap under the same schema.  Driver-selected
wall time and RSS remain explicit invocation parameters and are recorded
separately from the immutable semantic envelope.

## 4. Authenticated checkpoint representation

A lossless checkpoint stores at least

\[
 (S_0,V_0,H_0^{\rm history},P_0^{\rm history},
   \text{cap registry},\text{next frontier},\text{semantic state}).
\tag{4.1}
\]

Its self seal, rebuild digest and next-state canary bind all these fields.
On restore, the validator first copies \(S_0,V_0,P_0\) into immutable saved
variables.  It measures \(\Delta V,H_1,P_1\) in distinct live structures.
Only after the complete restore validation passes may it install the
mathematical state and begin accumulating \(\Delta S\).

In particular:

- `completed_counters == counters` followed by a `max` merge is not (2.2);
- a `restore_validation_counters={}` field which is never charged is not
  evidence of validation work;
- assigning the current process elapsed time into the saved wall-time slot
  destroys history; and
- adding the saved exhausted wall time to a fresh driver deadline prevents
  the intended continuation.

The terminal receipt exports the four categories separately and gives both
the saved frontier and current-invocation identities.  Producer and checker
use distinct checkpoint-owner tags and code hashes.

## 5. Accounting soundness

### Theorem 5.1 (NO ERASURE AND NO DOUBLE SEMANTIC CHARGE)

Assume the lossless restore theorem v288, the typed registry of Section 3,
and a checkpoint which passes Section 4.  Then (2.2)--(2.4) have the following
properties.

1. Every completed mathematical transition is counted exactly once in
   \(S_1\).
2. Every restore check is visible in \(V_1\) and is not mislabeled as a
   repeated mathematical transition.
3. Repeated resumes cannot erase a global semantic cap.
4. A fresh invocation receives exactly its registered wall/RSS budget and
   therefore is not blocked merely because the preceding invocation reached
   its own deadline.

#### Proof

V288 gives a unique frontier at which the continuation begins, so the new
transition set is disjoint from the completed transition set.  Additivity in
(2.2) counts their disjoint union exactly once.  Restore operations occur
before the frontier is installed and are written only to \(\Delta V\), which
proves the second assertion.  A global semantic cap sees the monotone sum
\(S_0+\Delta S\), proving the third.  The current host cap sees \(H_1\) by
definition, while (2.4) retains rather than discards old provenance, proving
the fourth. \(\square\)

This theorem concerns honest accounting and resource terminals.  It does not
authenticate the algebraic checkpoint by itself; v288's DAG, echelon, queue,
row/bridge and authority checks remain mandatory.

## 6. Minimal implementation tests

The ordinary validator must reject a checkpoint which lowers one saved
semantic counter, relabels a semantic key as host-local, removes validation
charges, changes a peak to a current gauge, alters the cap registry, swaps
producer/checker owner tags, or changes the next frontier without changing
the counters and canary.

A resume SELFTEST needs at least:

1. uninterrupted and split runs reaching the same mathematical terminal and
   identical final \(S\);
2. a split run with nonzero \(V\), showing that \(S\) did not double;
3. a semantic-cap stop which remains stopped after resume;
4. a wall-time stop whose authenticated continuation receives a new wall
   budget; and
5. producer and independent-checker checkpoints rejected under the opposite
   owner/code identity.

All measured values remain `UNEXECUTED` until GHA performs these tests.

## 7. Fixed frontier

```text
COMPLETED SEMANTIC COUNTERS COMPOSE BY SUM:       PAPER PROOF
RESTORE VALIDATION IS SEPARATELY METERED:         PAPER PROOF
WALL DEADLINE IS CURRENT-INVOCATION LOCAL:        PAPER PROOF
RSS/SIDECAR PEAK AND CURRENT GAUGE ARE DISTINCT:  PAPER PROOF
BLANKET MAX MERGE / WALL OVERWRITE:               REJECTED
A4-v5 / A0-v10 IMPLEMENTATION OF THIS ABI:        IN PROGRESS
SELFTEST / PRODUCTION:                            UNEXECUTED
LIFT / FAKE / IHARA:                              NONE
```

`R07_COMPOSABLE_RESUME_RESOURCE_ACCOUNTING_V290_PAPER_GRADE`
