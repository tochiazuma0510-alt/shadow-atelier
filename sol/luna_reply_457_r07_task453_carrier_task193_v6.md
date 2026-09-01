# Luna reply 457: Task453 carrier-v2 -> task193 compiler v6

Status: **IMPLEMENTED / BOUNDED PYTHON GATES PASS / PRODUCTION NOT RUN**

## Physical outputs

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_second_frattini_affine_prefix_compiler_v6.py` | 5013 | `0b987286bdd8e4dd6bba539b00beecfdfd811a6d410de29c53edb7e7d9150687` |
| `crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v6.py` | 4760 | `d41ed98fa134bbc4b5a7129f734812c67ae8f3ac5aeeb3953d451bf5be97c112` |
| `search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v6.g` | 2271 | `e88c81396b8b3cac415df3d776cf95fae3ac2f22460b0f2a451b27c6f66e25a2` |

No optional repository fixture was created.

## Exact generated owners

The v6 Python files are fail-closed source successors of the frozen Task454
owners.  They verify the v5 physical byte/SHA pin, every replacement
cardinality and postcondition, and the final generated-source byte/SHA pin
before compiling the generated body.

| generated body | bytes | SHA-256 |
|---|---:|---|
| producer | 12216 | `b5002f26ec9503f4f65127f269e6068d5ab4e5bf0b65d1bb79f2ba06400e27c9` |
| helper-nonshared checker | 7809 | `6f7bcbef4bc98d1cee1669c221affed45c614ab8d8cc4a5e8f064ebf251eca48` |

Producer generation used exactly 14 registered replacements.  Schema,
task193 terminal, three carrier physical pins, module name, checkpoint label,
rank-zero rejection label, corrected-word provenance, and descriptive label
each had cardinality `old 1 -> 0 / new 0 -> 1`; carrier schema and carrier
terminal each had `4 -> 0 / 0 -> 4`; embedded Task451 driver and source head
each had `2 -> 0 / 0 -> 2`.

Checker generation used exactly 13 registered replacements.  Its task193
terminal, carrier schema, carrier terminal, and checker-verdict suffix each
had `2 -> 0 / 0 -> 2`; every other registered replacement had
`1 -> 0 / 0 -> 1`.  No new replacement literal existed in either owner before
patching, and no registered old literal survived.

## Migrated provenance firewall

Both generated bodies require exactly:

- carrier-v2 producer `3530 / abe7d2ad15a48d641a41f51fb69c1d989224e96d024b688859a6ab141b176bf3`;
- carrier-v2 checker `3584 / 8a27b06155bf94a99a38a8fd891bb811e2c0958db5ac7f39312403337a8c878b`;
- carrier-v2 driver `2502 / 6c0b9cc285796f4c91987e2eacfb4907e7c27867379132fdf1f8194aa9505c67`;
- carrier schema/terminals `...carrier/v2`, `...CARRIER_V2_ACCEPTED`,
  `...carrier/v2/checker`, and `...CARRIER_V2_CHECKER_PASS`;
- embedded Task453 outer driver
  `2387 / 8f8c803cff86fbb4bb774570cb596e9e5a8262c05321e955e2cf0de545df60dc`;
- dispatched source head `7498d381de7180c8ca562fba5cf3bc15323d522c`.

The Task451 producer/checker and frozen-rank-51 pins remain byte-identical.
The three physical Task451 result/checkpoint/log identities and positive
numeric `run_id`/`artifact_id` ABI remain unchanged.  No GHA run/job value was
reinterpreted as an artifact.

## Preserved mathematical boundary

No task193 affine/Fox core line was edited.  The generated producer still
loads the exact v4 owner and invokes its rank-zero `actual_compile`; the
checker still performs its independent v4 replay and final v1 reseal.  The
following remain literal: u32be historical sparse digest, full replay,
literal words and right product, exponent/joint gates, hexagon and printed
pentagon flags, inner-key compatibility conversion, ordinary/pointed rows,
equality oracle, presentation boundary, and conventional verdict claims.

Task193 labels advance only to v6, including checkpoint schema and checker
verdict schema `.../v6/checker-verdict/v6`.  `UNKNOWN_RESOURCE` remains
non-resumable and every non-PASS A2/lift/fake/Ihara claim remains false.  No
resume adapter, retry, worker pool, new oracle, Task451 state copy, A2, or A5
computation was added.

## Bounded gates

Passed:

```text
python -m py_compile <producer-v6> <checker-v6>
python -B <producer-v6> --fixture --output %TEMP%/task457_fixture_v6.json
python -B <checker-v6> --self-test
python -B <producer-v6> --source-patch-info
python -B <checker-v6> --source-patch-info
TASK457_FULL_PIN_CLOSURE_PASS stale_carrier_v1=0
```

Terminals:

```text
R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V6_PRODUCER_TERMINAL FIXTURE
R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V6_CHECKER_SELFTEST_PASS mutations=15 inner_key_transform=true final_reseal=true verdict_abi=true actual_task451_positive=false
```

The producer fixture reports `actual_task451_positive=false`, asserts no
task193 value, and rejected all 16 inherited concrete mutations.  Full pin
closure read all six frozen dependencies through each generated module.
Generated-source scanning found zero stale carrier-v1 schema, terminal,
physical carrier pin, old Task451 driver, old source head, or Task452
provenance label.  All three physical outputs are ASCII-only and
newline-terminated.

The bounded GAP guard load was attempted, but local GAP failed before reading
the driver with `couldn't create signal pipe, Win32 error 5`.  Consequently
the runtime `task193 v6 external preamble` observation is unavailable in this
environment.  The external guard is statically the first executable clause;
no filesystem, pin, Python, or production action ran in that attempt.

No task193/Task451/carrier production, GHA, heavy calculation, workflow edit,
git, network, or credential action was performed.  There is no implementation
blocker.

`TASK457_R07_TASK453_CARRIER_TASK193_V6_PASS`
