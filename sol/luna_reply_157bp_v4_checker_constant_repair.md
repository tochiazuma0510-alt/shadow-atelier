# Luna reply 157bp — v4 checker constant repair

## Verdict

The pre-computation blocker is repaired and the q5-fast workflow is bound to
the repaired checker.  The bundle is ready for rerun.  No local GAP, Git,
push, or GHA execution was performed.

## Root cause and repair

Run `32069959135` stopped before mathematical work because the appended v4
checker path referenced `P_ORDER` and `PPRIME_ORDER` at former lines 914 and
915, while the standalone checker had never declared them.  The exact frozen
compact-roof constants are now declared at checker lines 26–27:

```text
P_ORDER      = 1469664
PPRIME_ORDER = 367416
```

The receipt gate already compares both independently reconstructed SymPy
orders against these constants.  The checker selftest now performs the same
roof and derived-roof order computation and asserts both literal constants at
lines 991–999.  Thus omission, literal drift, or compact-roof construction
drift fails before receipt acceptance.

The q5-fast workflow's `CHECKER_SHA256` was updated at line 27.  The producer
hash remains unchanged and matches its existing pinned value.  The workflow
already runs the repaired checker for both pinned calibrations and for both
q5 jobs; those invocations remain at lines 188–190 and 280.  The q5 matrix
continues to run `a=2` and `a=4` independently.  No structural workflow
rewrite was needed for this strictly constant/hash repair, avoiding a change
to the existing fail-closed artifact and identity gates.

## Next-blocker audit

The checker was statically scanned for unresolved global names after the
repair; no possible undefined global remained.  `V4_SCHEMA`, `V4_FINAL`,
`V4_PRODUCER`, source-role constants, algorithm constant, calibration constants,
and the newly restored roof constants are all defined before the v4 checker
entry point.  The q5-fast workflow's source hash gate, pinned q3/q4 metadata,
receipt schema, row-count, and repaired-checker invocations are consistent.

## Tests

Commands executed (with bytecode writing disabled for runtime checks):

```text
python -B -m py_compile search/d972_b4_burau_fiber_v4.py search/check_d972_b4_burau_fiber_v4.py
python -B search/d972_b4_burau_fiber_v4.py --self-test
python -B search/check_d972_b4_burau_fiber_v4.py --self-test
```

Observed producer markers:

```text
D972_B4_BURAU_V4_SOURCE_WORD_ROOF_ONLY_NEGATIVE_PASS row=2 exponent=(-4,-8) nonzero=956
D972_B4_BURAU_FIBER_V4_NEGATIVE_FIXTURES_PASS
D972_B4_BURAU_FIBER_V4_SELFTEST_PASS
```

Observed checker markers:

```text
D972_B4_BURAU_FIBER_V4_SOURCE_WORD_ROOF_ONLY_NEGATIVE_PASS row=2 exponent=(-4,-8) nonzero=956
D972_B4_BURAU_FIBER_V4_CHECKER_SELFTEST_PASS
D972_B4_BURAU_FIBER_V4_CHECKER_FINAL_MARKER status=PASS
```

The pinned q3/q4 receipts from the task-context temp artifact path were
checked lightweightly (JSON/scalar/hash/972-row gates; no full heavy receipt
recheck):

```text
V4_PINNED_RECEIPT_LIGHTWEIGHT_PASS 3 d972_b4_burau_fiber_v4_q3.json
V4_PINNED_RECEIPT_LIGHTWEIGHT_PASS 4 d972_b4_burau_fiber_v4_q4.json
```

Both retain `|H|=105815808`, `|H'|=2939328`, `|K|=8`, the expected q/a, and
the unchanged producer source hash.  Static workflow checks observed:

```text
Q5_FAST_CHECKER_INVOCATION_STATIC_PASS
```

## SHA-256

```text
search/check_d972_b4_burau_fiber_v4.py    E0B4CB923C1BD73B9AFDC7F47DE739F91C8AA3C0D7764C239E1DF76D74FBCE14
.github/workflows/d972-burau-tuple-q5-fast-v1.yml 33BF99A237A3193DE220C49B1A5559FF9358C4897A400782D273BC76BDFB23FC
```

V4_CHECKER_CONSTANT_REPAIR_READY
