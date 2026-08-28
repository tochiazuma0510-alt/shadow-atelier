# R07 task307/v7 GHA fixture failure audit v257

Author: Sol / 2026-08-28

Status: exact post-run failure classification.  This note records an
implementation-fixture defect, not an A5/A6 mathematical terminal.  No lift,
fake certificate, or Ihara conclusion is declared.  `verified=false`.

## 1. Authenticated failed run

The task307/v7 synthetic SELFTEST was dispatched through the unchanged
generic `gap-run.yml` workflow:

```text
run id = 33167156710
head   = 66e63e7f3cf398ae826599715e35eb5f515a442a
status = completed / failure
failed step = Run GAP script
```

The driver preserved the quoted preamble
`D307Mode:="SELFTEST";;` and reached the pinned producer.  The producer
stopped in `compile_case` before any case terminal with

```text
RuntimeError: action owner
```

Thus this is neither a GAP setup failure nor a MEMBER/NONMEMBER result.

## 2. Exact defect

In the first fixture case `nonzero-member`, the literal matrices
`A_theta/A_theta_binding` and `A_Z/A_Z_binding` agree.  The matrices
`A_E/A_E_binding` do not.  Exactly two binding rows are malformed:

```text
row 6: A_E has 11 entries; A_E_binding has 10 entries
row 7: A_E has 11 entries; A_E_binding has 10 entries
```

Every other fixture case has all three literal owner bindings equal.  The
producer's fail-closed owner gate therefore behaved correctly.  The earlier
task309 static PASS did not compare these two literal rows and is superseded
for execution authorization by this observed failure.

## 3. Repair and audit boundary

A versioned v8 repair must not weaken the owner gate.  It must repair the two
binding rows to the exact 11-column `A_E` rows, update all versioned identities
and pins, and add an explicit all-case fixture preflight.  Before execution,
an independent Sol(max) audit must directly compare every bound literal and
dimension, not merely infer the advertised ranks.

The same audit must include an efficiency pass: reject redundant full-case
recomputation, accidental exponential enumeration beyond the intended tiny
kernel canaries, repeated fixture parsing, or any other unnecessary serial
work.  This synthetic kernel is small, but the rule is retained for every
future production-code audit.

## 4. Accounting

```text
TASK307/V7 GHA SELFTEST:        FAILED BEFORE CASE TERMINAL
DEFECT TYPE:                    MALFORMED FIXTURE BINDING
A5 ACTUAL / A6 ACTUAL:         0/3 / 0/3
IMPLEMENTATION SELFTEST:        NOT ACCEPTED
LIFT / FAKE / IHARA:            NONE
```

`R07_TASK307_V7_GHA_FIXTURE_FAILURE_EXACTLY_CLASSIFIED`
