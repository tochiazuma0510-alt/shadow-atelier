# Luna Task 565: target-independent first-rung grade-two prebuild (v1)

Author: Sol / 2026-09-03

## 1. Role and objective

You are Luna, implementation support.  Implement the target-independent half
of the exact grade-two step while the grade-one physical terminal is still
running.  The mathematical source is
`sol/proof_r07_grade1_to_grade2_split_presentation_handoff_v450.md`, together
with v441, v444, v446--v449 and the audited grade-one v3/v4 state schema.

This task must not decide grade-two membership, trust a not-yet-checked
grade-one terminal, alter the running workflows, or launch a real local/GHA
computation.  It prepares a versioned executable and bounded fixtures only.

## 2. Allowed output files

Write only:

1. `search/d972_r07_a0_first_rung_grade2_prebuild_v1.py`;
2. `search/check_d972_r07_a0_first_rung_grade2_prebuild_v1.py`;
3. `sol/luna_reply_565_r07_a0_first_rung_grade2_prebuild_v1.md`.

Do not modify v3/v4, their certificates, any workflow, provenance file, or
v220.  Temporary files must be outside the repository.  Do not commit, push,
dispatch, download production artifacts, or run heavy/local parallel Python.

## 3. Exact input contract

The producer consumes one authenticated grade-one split state directory:

- prepare HEAD/body and every referenced lower/lift/packet blob;
- block-0 through block-3 HEAD/body and every referenced basis blob; and
- the exact frozen input manifest used by v3/v4.

It must accept both the v3 and v4 executions because their
`STATE_SCHEMA` is deliberately identical.  It must not require a merge state
or grade-one target coefficients for the target-independent phase.

Authenticate canonical JSON, HEAD/body digests, parent links, all blob
sizes/hashes/shapes, character order, actor order, queue-exhaustion receipts,
origin roster and packet bindings before using a row.  Fail closed on a
missing or mismatched item.

## 4. Required mathematics in the producer

Use the deterministic global order of v450:

```text
all lifted old rows by character,pivot;
then all H^[1] rows by character,pivot.
```

Reconstruct the complete `B1` presentation from split records, rather than
using the merge certificate's summary object:

1. assemble the full precision-one rows with compact literal/DAG ancestry;
2. derive reductions of the 44 original seeds in `B1`;
3. derive all four actor transitions of every `B1` row, inserting the stored
   seed/transition-defect reductions for lifted-old rows and using the stored
   block transitions for new rows;
4. directly replay all assembled identities at precision one;
5. lift `B1`, every seed relation and every actor transition to precision
   two using the exact v442/v443 affine formulas;
6. form the complete v444 defect roster `44 + 4*rank(B1)` (a larger redundant
   projected-seed roster is forbidden unless separately justified and
   declared);
7. project each complete defect by the four legal v447 character projectors,
   retaining all six degree-two monomials coupled;
8. expose phase/checkpoint interfaces for four independent source closures,
   each of width 36,288; and
9. expose a merge interface that combines every lifted `B1` row with the
   four exhausted defect bases in one lower-first fibre with lower width
   32,260 and new-grade physical width 48,384.

Do not split individual monomials and do not close after physical
aggregation.  Persist full origin reductions, actor transitions, compact
ancestry and exact state ancestry required to form `T2` after a future
MEMBER join.

The only terminal allowed by this task is
`FIRST_RUNG_GRADE2_MODULE_READY`.  It means the target-independent fibre is
complete; it does not mean MEMBER.  Incomplete closure or a resource cap is
`UNKNOWN_RESOURCE`, never NONMEMBER.

## 5. Future MEMBER join boundary

Provide a separate, inactive-by-default join entry point which requires an
independently checked `FIRST_RUNG_GRADE1_MEMBER` state and certificate.  It
must independently rebuild the literal accumulated word `c1`, compute

```text
rho2 = direct_degree2_target - direct_degree2_replay(c1),
```

and recompute width 48,384, packed length 12,096, support, packed SHA-256 and
sparse digest.  Merely reading `next_degree2_residual` is forbidden.  The
join must bind the exact prepare/four-block/module-state/certificate hashes
as parents before a future membership reduction.  For this task, stop after
the residual comparison fixture; do not emit a production MEMBER or
NONMEMBER certificate.

## 6. Independent checker and fixtures

The checker must not import the producer.  Give it independent small affine,
polynomial, actor, projector and row-replay routines.  Bounded fixtures must
reach at least:

1. split `B1` assembly with a nonzero old transition defect;
2. recovery of one original seed from four projected seed records;
3. all four actor transitions for both an old and a new `B1` row;
4. a negative signed kernel column using `u -> 2u+u^2` at degree two;
5. all six monomials remaining coupled in one character row;
6. a dependent lifted-old physical row producing a nonzero grade-two
   connection;
7. rejection of a mutated origin reduction, transition, blob, parent hash,
   monomial split and incomplete queue;
8. independent recomputation and mutation rejection of a small MEMBER-join
   residual; and
9. deterministic resume/idempotence of every implemented phase.

Run only serial `py_compile`, producer fixture and checker fixture.  Record
commands, runtimes, file sizes and SHA-256 values in the reply.  State
explicitly that no real certificate and no membership result were produced.

## 7. Claim boundary

The reply must use exactly one of:

```text
GRADE2_PREBUILD_V1_IMPLEMENTED_AUDIT_REQUIRED
GRADE2_PREBUILD_V1_BLOCKED
```

Even on success:

```text
GRADE ONE: terminal still external
GRADE TWO MODULE: executable candidate only
GRADE TWO MEMBER/NONMEMBER: not run
ORDER-54,432 / FULL-Q0 / A0 / COMMON / COFINAL LIFT: not declared
FAKE / IHARA: not declared
verified=false
```
