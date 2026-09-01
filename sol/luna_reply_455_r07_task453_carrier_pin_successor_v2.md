# Luna reply 455: Task453 batch-64 provenance carrier pin successor v2

Status: **IMPLEMENTED / BOUNDED PYTHON GATES PASS / PRODUCTION NOT RUN**

## Outputs and physical pins

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_task451_task193_carrier_v2.py` | 3530 | `abe7d2ad15a48d641a41f51fb69c1d989224e96d024b688859a6ab141b176bf3` |
| `crosscheck/check_d972_r07_task451_task193_carrier_v2.py` | 3584 | `8a27b06155bf94a99a38a8fd891bb811e2c0958db5ac7f39312403337a8c878b` |
| `search/d972_r07_task451_task193_carrier_gha_driver_v2.g` | 2502 | `6c0b9cc285796f4c91987e2eacfb4907e7c27867379132fdf1f8194aa9505c67` |

The Python successors exact-pin and patch the accepted Task452-v1 owners:

| generated source | bytes | SHA-256 |
|---|---:|---|
| producer mathematical body | 8619 | `eea64d185ad20a1b9d8bf202ad0a04a13d0bb3fc10c202363ad4cfe46fe88c43` |
| helper-nonshared checker body | 8582 | `86c0e347b32f371cf5fc3f489a491ce92f2c25fb5b5aed7148d230230d994592` |

Both wrappers fail closed on v1 owner byte/SHA drift, replacement-cardinality
drift, replacement postcondition drift, or generated-source byte/SHA drift.

## Exact successor boundary

The only non-label provenance replacements are:

- upstream driver owner: v1 `2569 / 6910d38a...` -> Task453 outer v2
  `2387 / 8f8c803cff86fbb4bb774570cb596e9e5a8262c05321e955e2cf0de545df60dc`;
- required source head: `3316809e483223ec571ca7d6976dc1317c892441` ->
  `7498d381de7180c8ca562fba5cf3bc15323d522c`.

Thus carrier-v2 cannot accept the old head as a Task453 artifact.  The
dispatch identifiers `run 33516227668 / job 99883831511` are recorded only as
ledger context, exactly as commissioned.  No unprovided artifact ID or new job
field was invented or reinterpreted; the accepted v1 positive numeric
`run_id`/`artifact_id` ABI remains unchanged.

Each producer patch has exact cardinality `old 1 -> 0`, `new 0 -> 1` for the
schema, terminal marker, upstream driver tuple, source head, and six module
labels (10 replacements total).  Each checker patch has the same cardinality
for nine entries; its terminal-marker replacement is exactly `old 2 -> 0`,
`new 0 -> 2`, because it also advances the literal ACCEPTED terminal (10
replacements total).  All new strings were absent before replacement.

The driver advances the external guard, `D455*` module variables, output
paths, producer/checker terminals, and final marker to the v2 dialect.  It
exact-pins the two physical v2 wrappers above.

## Preserved behavior

The generated bodies retain the accepted Task452 mathematics and acceptance
boundary byte-for-byte outside the enumerated provenance/version/module-label
strings: exact `C451.check(result)` and physical result/checkpoint/log binding;
checker-equal `terminal_replay.literal_word`; literal 760-letter `g760`; right
multiplication; exponent zero; ten-coordinate joint kernel; target/correction
owners; eleven-occurrence/all-seven replay; full replay; task193 u32be sparse
digest; hexagon and printed-pentagon flags; selected action ancestry; and both
canonical seals.  Claims remain carrier-only, with A2/lift/fake/Ihara false.
RESOURCE/UNKNOWN and every non-PASS input remain nonpositive.

## Bounded results

The following bounded gates passed (also independently reproduced by the
parent session):

```text
python -m py_compile <producer-v2> <checker-v2>
python -B <producer-v2> --mode FIXTURE --output %TEMP%/task455_carrier_fixture_v2.json
python -B <checker-v2> --self-test
python -B <producer-v2> --source-patch-info
python -B <checker-v2> --source-patch-info
```

Terminals:

```text
R07_TASK451_TASK193_CARRIER_V2 status=FIXTURE
R07_TASK451_TASK193_CARRIER_V2_CHECKER_SELFTEST_PASS
```

The fixture explicitly reports `actual_task451_positive=false`.  The checker
rejected all 18 registered mutations: terminal, result, checkpoint, checker
marker, head, run, artifact, correction literal, `g760`, corrected word/order,
occurrence, exponent, joint kernel, ancestry, sparse-row digest, full replay,
hexagons, and pentagon ordering.  The three physical outputs are ASCII-only
and newline-terminated.

One environment-only gate remains unconfirmed: the bounded GAP driver load
could not start because local GAP failed before reading the script with
`couldn't create signal pipe, Win32 error 5`; therefore the runtime observation
of `task455 external preamble required` was not obtained.  The guard is the
first executable driver clause, so no pin, filesystem, Python, or production
operation ran during that failed attempt.

No Task451/Task452 production, GAP production, GHA, git, network, credential,
Q0/batch/dual/echelon/fibre copy, or other repository output was performed.
There is no implementation blocker.

`TASK455_R07_TASK453_CARRIER_PIN_SUCCESSOR_V2_PASS`
