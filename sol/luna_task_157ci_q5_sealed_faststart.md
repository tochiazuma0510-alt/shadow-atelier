# Luna task 157ci: q5 accelerator sealed-calibration fast start

## Role and scope

You are Luna. Build a new workflow only; do not edit the audited producer or
checker from 157by. You may write only:

- `.github/workflows/d972-burau-accel-v2.yml`
- `sol/luna_reply_157ci_q5_sealed_faststart.md`

No local heavy enumeration, GAP, Git, or GHA.

## Objective

The audited v1 workflow redundantly reruns the q3 and q4 independent checkers
inside each q5 job, delaying the q5 producer by roughly 90 minutes. Replace
that repeated computation with fail-closed authentication of the already
independently checked calibration artifacts from run `32072654277`:

- q3 artifact id `9303461247`, name
  `d972-burau-q5-parallel-v1-calibration-q3-attempt1`, archive digest
  `sha256:24bf1fc9fcb7505a7fe83e7521bcc7c65a32b58947ce04edb471013e4720df24`,
  receipt SHA
  `0813a151cd47a56f29aab629ebfc35a0293a8ce84d98c24f3a3ac3e0601ad8e2`;
- q4 artifact id `9303700869`, name
  `d972-burau-q5-parallel-v1-calibration-q4-attempt1`, archive digest
  `sha256:38be12c17437dba07b3b1b33c82d558ba38478a059dbcbe6641fdfc0146ccf62`,
  receipt SHA
  `414c13fe680c2eeb6f3f75c7f6a7206a707c18a426da619543232e1a98855de2`.

## Required contract

1. Pin run ID, head SHA `303778b34e173acf6a35ad09297cf37f18dfce53`, artifact IDs,
   names, sizes, archive digests, nonexpired state, and attempt.
2. Download both artifacts by exact run/name. Validate receipt, seal, checker
   log, and checker-status files. Require receipt SHA, seal schema/complete,
   checker exit 0, marker exactly once, legacy producer/checker SHA, q/a,
   972 rows, and artifact/run IDs. The pinned archive digest must cover the
   whole evidence bundle.
3. The existing 157by producer still deep-validates both complete 972-row
   receipts, and its independent checker still receives the same receipts.
   Do not weaken any producer/checker/status/kernel/fiber gate.
4. Run q5/a2 and q5/a4 in `fail-fast:false`, with the candidate-only early
   stop/all-pass-complete contract unchanged. Upload all evidence on failure.
5. Do not execute the expensive legacy calibration checkers again. Explain
   why the immutable sealed evidence plus deep receipt validation is an exact
   reuse, not trust in an unchecked producer metric.

Run YAML/embedded-Python/source-hash/selftest static checks. Return
`Q5_SEALED_FASTSTART_READY` with the exact workflow SHA.
