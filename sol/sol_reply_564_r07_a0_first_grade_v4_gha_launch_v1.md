# Sol Reply 564 — A0 first-grade v4 recovery launch

Author: Sol / 2026-09-03

Status: parent-owned GHA launch receipt.  This records execution state only;
it is not a MEMBER/NONMEMBER result and `verified=false`.

## 1. Reused completed production phases

The source is v3 production run `33677346616`, exact head
`22c6dddb43d107c05e65f53ad898823ae8ebe276`.  Its real prepare and all four
character closures are complete and retained for 90 days:

```text
prepare state artifact 9865061266
  state 1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865
  old ranks [505,503,503,503]
  defect origins 8232
  residual support 16254

block 0 artifact 9865238399  rank 1509  attempts 14268
block 1 artifact 9865242284  rank 1512  attempts 14280
block 2 artifact 9865193269  rank 1512  attempts 14280
block 3 artifact 9865239848  rank 1512  attempts 14280
```

Every block reports queue exhaustion.  The original v3 merge job
`100408719904` remains live; it was not cancelled.

## 2. Audited bounded optimization

Task562 produced the versioned v4 pair:

```text
producer 144552 bytes
  1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4
checker 69184 bytes
  ffd78b41fc9f7a1f59925eb8f07db7278b704c3580bb7e8fa3a586e85db9fe06
```

It removes only repeated packed suffix scans and the duplicate lower
reduction.  The row universe, traversal order, pivots, DAG, aggregation,
terminal predicate and replay remain unchanged.  It deliberately accepts the
sealed v3 state schema.  Independent Sol(max) Task563 returned
`FIRST_GRADE_MERGE_V4_PASS`; its reply is 10772 bytes with SHA-256
`753437f782bc02196bccdf44dd6e8e346945ca3d8d39444d17542649b9fe86a9`.

## 3. Recovery GHA launch

The parent committed and pushed exactly the versioned v4 programs, their
task/replies and the recovery workflow:

```text
commit 28ec1587222b16c6adcad2ee085bfda973243fd2
run    33687595111
job    100438646038  optimized joint physical fibre from sealed v3 phases
url    https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/33687595111
```

The exact-head, producer, checker and Task563 audit hash gates passed.  The
serial release fixtures passed.  Cross-run download of the 204 MB prepare
artifact and all four completed block artifacts passed, as did the five-state
fan-in checks.  At this receipt, step `Run optimized merge only` is live.  No
prepare or character closure was recomputed.  A successful merge is followed
automatically by the independent v4 terminal checker and a 90-day checked
artifact.

## 4. Claim boundary and v220 mapping

The v3 and v4 jobs compute the same finite grade-one question.  The first one
to reach a successful independent checker supplies the candidate terminal;
the other run remains useful as an independent execution comparison.  Until
then:

```text
FIRST RUNG: 0/6 grades decided
A0: 0/1 actual
A1: 4/4
A2: 2/3
A3: 3/3
A4: 1/3
ORDER-54,432 / FULL-Q0 / COMMON / COMPATIBLE LIFT / FAKE / IHARA: NOT DECLARED
verified=false
```

