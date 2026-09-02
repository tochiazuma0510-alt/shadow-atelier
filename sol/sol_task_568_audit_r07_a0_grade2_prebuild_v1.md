# Sol Task 568: independent audit of the first-rung grade-two prebuild (v1)

Author: Sol / 2026-09-03

## 1. Role and objective

You are Sol(max), the independent mathematical and implementation auditor.  Audit
the Task565 candidate as the target-independent continuation of the actual A0
first rung.  The objects under audit are:

- `search/d972_r07_a0_first_rung_grade2_prebuild_v1.py`;
- `search/check_d972_r07_a0_first_rung_grade2_prebuild_v1.py`;
- `sol/luna_reply_565_r07_a0_first_rung_grade2_prebuild_v1.md`.

Read Task565, v450, mandatory repair v451, and the full Task566 audit reply.
This is the requested independent audit of the implementation, not a renewed
audit of row 36 or of the 648 non-arithmetic labels.  Do not broaden the task.

## 2. Allowed output and execution boundary

Write only
`sol/sol_reply_568_audit_r07_a0_grade2_prebuild_v1.md`.  Do not repair either
program, modify v220, create certificates, commit, push, dispatch GHA, or run a
real grade-two phase.  Temporary fixtures and bytecode caches must be outside
the repository.  Run bounded serial checks only; do not launch parallel Python.

Independently record the three input sizes and SHA-256 values before the audit.

## 3. Mathematical completeness audit

Trace the implementation against the actual formulas and state schema, rather
than accepting comments or field names.  Decide each of the following:

1. `P_chi` (the full filtered word sum) is never conflated with the pure-grade
   idempotent `e_lambda`, including in reconstruction and checking.
2. The global order and offsets are exactly v451: all lifted-old rows by
   character and pivot, followed by all new `H^[1]` rows by character and
   pivot.  Check the formulas for `R_chi`, `O_chi`, `N_chi`, `D_chi`, origin
   indices and signs in all four characters.
3. All 44 original seed relations and every one of the four actor transitions
   of every old and new `B1` row are reconstructed from authenticated data.
   Check compact/DAG ancestry and direct precision-one replay; sampling alone
   is insufficient where a complete loop is required.
4. The precision-two affine arithmetic is exact, especially negative columns
   (`u -> 2u+u^2`), multiplication, extension data, and crossed cochains.  No
   additive-cochain shortcut is permitted.
5. The full lower-grade gate is implemented: translated PB3 rows, both PB4
   blocks, filtration, physical aggregation, cocycle and integral-exponent
   checks.  All six degree-two monomials remain coupled through source closure
   and the physical fibre.
6. The defect roster is exactly `44 + 4*rank(B1)`, each character closure is
   complete, and the module construction is genuinely target-independent.
   Prepare plus all four exhausted blocks suffice; neither a merge state nor
   target coefficients may leak into prebuild.
7. The inactive MEMBER join requires an independently checked grade-one MEMBER
   state, rebuilds literal `c1`, independently recomputes the complete
   degree-at-most-two replay, asserts every one of the 32,260 lower/auxiliary
   coordinates is zero, and recomputes all 48,384 `rho2` coordinates and their
   support/digests.  It must not trust `next_degree2_residual` or silently
   perform grade-two membership.
8. Every parent link, canonical JSON object, blob shape/size/hash, queue
   exhaustion record, origin roster, character/actor order and phase ancestry
   is authenticated fail-closed.  Check v3/v4 schema compatibility.

For every PASS, cite concrete functions/line numbers or an executed bounded
test.  For a failure, give the smallest exact counterexample and whether it is
load-bearing.

## 4. Independent-checker audit

Confirm by import tracing and code comparison that the checker does not import
the producer or share its mathematical helper implementation.  Determine
whether it independently checks the complete roster, closures, old physical
connections, all old/new transitions, lower gate and future residual join,
rather than merely comparing producer-computed summaries.

Run the prescribed serial `py_compile`, producer fixture and checker fixture.
Add focused bounded mutations if needed for an otherwise untested load-bearing
gate.  Confirm that every Task565 fixture is actually reachable and that its
mutation changes the intended semantic datum, rather than only a checksum.

## 5. Performance and memory audit

The researcher explicitly forbids wasting another run on avoidable overhead.
Inspect the real-phase paths for:

- accidental dense expansion of sparse/packed rows;
- retaining four character owners at once;
- duplicate physical or ancestry rows;
- per-pivot conversion/copying, repeated full-blob hashing or repeated full
  scans inside rank loops;
- unbounded Python-object metadata at the declared ceilings;
- recomputation of completed grade-one prepare/blocks or dependence on merge;
- missing deterministic progress, checkpoint/resume, atomic sealing or
  `UNKNOWN_RESOURCE` handling.

Distinguish (a) a correctness blocker, (b) a likely production memory/time
blocker, and (c) optional optimization.  Do not demand cosmetic refactoring or
an unrelated generalized framework.  If the present file-backed design cannot
fit a standard GHA runner at its stated ceiling, say so quantitatively and
propose only the minimal repair.

## 6. Verdict and claim boundary

Return exactly one headline:

```text
GRADE2_PREBUILD_V1_AUDIT_PASS
GRADE2_PREBUILD_V1_AUDIT_PASS_AFTER_REPAIR
GRADE2_PREBUILD_V1_AUDIT_FAIL
```

`PASS_AFTER_REPAIR` must list finite, exact edits that can be applied without
redesign.  Do not call the candidate cross-checked merely because fixtures
pass.  Even on PASS:

```text
GRADE ONE: terminal still external
GRADE TWO MODULE: audited executable candidate, not a real result
GRADE TWO MEMBER/NONMEMBER: not run
A0 / COMMON / COFINAL LIFT / FAKE / IHARA: not declared
verified=false
```

