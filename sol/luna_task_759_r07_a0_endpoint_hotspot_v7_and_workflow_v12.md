# Luna Task 759 — A0 endpoint v7 finite release repair + workflow v12

You are Luna, implementation/compute support.  Read this FULL mail, sections 1
through 7.  Create only:

- `search/d972_r07_a0_fresh_precision2_endpoint_signature_v7.py`
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v12.yml`
- `sol/luna_reply_759_r07_a0_endpoint_hotspot_v7_and_workflow_v12.md`

Use v6 as producer source and workflow v11 as workflow source.  Do not edit
those files.  Do not run real parents, GHA, git, or large calculations.

## 1. Exact purpose

Implement only the four finite blockers in Sol(max) Task756.  Preserve the v495
monoid cache: production generic endpoint evaluations remain exactly four actor
atoms plus one per reached seed, with zero empty-word and zero full-prefix
generic evaluations.  Do not change the candidate universe, term reduction,
direct columns, bucket arithmetic, precision-two aggregation, lower-zero gate,
rho2, or claim flags.

## 2. Preserve checker-v4 wire contract

The v7 producer must deliberately emit the existing v4 payload wire format:

- schema `d972.r07.a0.fresh-precision2-endpoint-signature.v4`;
- marker `R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V4_CANDIDATE`;
- the `occurrence` object must have exactly the eight keys required by checker
  v4, including `all_seven_canary: true`, and no profiling-only extra keys.

Keep the optimization counters in selftest output and the Luna reply/log only.
Do not create or modify a checker.

## 3. Typed recurrence and noncommuting fixture

In every `extend_signature` slot require both parent and atom tags to equal
`E3` for slots 0..5 and `E4` for slots 6..10 before unpack/multiply.  Emit that
expected tag.  Add bounded rejection tests for a missing/None atom, a mislabeled
parent slot, and a mislabeled atom slot.

Use genuinely noncommuting S3 and S4 permutation images in the recurrence
fixture.  Require live `parent * atom` to match direct evaluation and an
explicit reversed `atom * parent` mutant to differ, including signed atoms.
Do not rely on the former repeated-cycle/abelian fixture.

## 4. Bounded progress, no log flood

For each large phase (`direct_column`, `precision2_aggregation`) print exactly
one explicit start and one explicit complete boundary line.  After each item,
retain `guard(started)` and call the existing `meter.check` with a phase string
containing `done/total`; do not call the unconditionally printing
`endpoint_checkpoint` per item.  Atom and reached-seed logs may remain because
they are bounded.  This must reduce the possible explicit flushed large-loop
lines from 410,488 to four, while still exposing 60-second meter progress.

## 5. Workflow v12

Clone v11 minimally and version it to v12.  Pin the exact v7 producer size/SHA
and unchanged checker-v4 size/SHA.  Compile/selftest both, invoke v7 in the real
producer step, invoke checker-v4 unchanged, keep exact immutable parent IDs and
auth gates, preserve useful stdout/stderr/time logs and artifact upload on
failure.  Use fire token `[fire-fresh-precision2-endpoint-v12]`.  Do not
dispatch.  Avoid unrelated YAML condensation or refactoring.

## 6. Bounded tests

Run py_compile without leaving repository pycache, both producer-v7 and
checker-v4 selftests, YAML parse, and source/AST probes proving:

- production coordinates count form `4+R`, `R<=44`;
- no all-prefix direct `signature` comparison;
- exact v4 output schema/marker/occurrence keys;
- large-loop explicit boundary lines exactly four and per-item meter throttling;
- v12 pins/invokes v7 and checker-v4.

## 7. Reply boundary

Report exact bytes/LF/SHA, v6->v7 and v11->v12 diffs, bounded results, and:

```text
SAFE_FOR_INDEPENDENT_AUDIT=yes
REAL_PARENT_REPLAY=NOT_RUN
FRESH_RHO2=NOT_PRODUCED
A0/FAKE/IHARA=NOT_DECLARED
verified=false
```
