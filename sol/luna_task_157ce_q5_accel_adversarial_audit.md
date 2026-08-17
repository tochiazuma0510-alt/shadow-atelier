# Luna task 157ce: adversarial audit of q5 accelerator bundle

## Scope

Read task/reply 157by and independently audit these new files without editing them:

- `search/d972_b4_burau_accel_v1.py`
- `search/check_d972_b4_burau_accel_v1.py`
- `.github/workflows/d972-burau-accel-v1.yml`

Write only `sol/luna_reply_157ce_q5_accel_adversarial_audit.md`. Do not run GAP,
heavy enumeration, Git, or GHA.

## Required audit

Adversarially check exact-kernel completeness, discovery-witness closure,
candidate-only partial scan semantics, independent checker recomputation,
pentagon/A.18 convention, q3/q4 immutable artifact bindings, source/hash/schema
bindings, workflow status/marker gates, artifact upload on failure, YAML/bash
quoting, and that q5/a2,a4 are the only production matrix entries. Run only
light selftests/AST/YAML checks. Look specifically for fail-open mutations:
partial all-pass, missing last zero row, incomplete K, empty witnesses, status
disagreement, calibration substitution, and source hash drift.

Return `Q5_ACCEL_AUDIT_PASS` or `Q5_ACCEL_AUDIT_FAIL` with exact findings and
line references. A pass is permission for the parent to commit/dispatch, not an
A/B result.
