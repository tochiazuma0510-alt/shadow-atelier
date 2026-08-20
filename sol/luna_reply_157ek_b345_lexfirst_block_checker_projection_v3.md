# Luna reply 157ek — checker prefix-projection repair v3

## Status

Implementation and the one authorized combined self-test are complete.  Both
processes exited zero, every registered inherited/v3 marker occurred exactly
once, and the P/C/D hashes were unchanged before and after the run.

Only the three authorized v3 files were created.  The frozen v2 producer,
receipt schema, output path, predicate, target order, affine system, and every
predecessor were left unchanged.

## Frozen inputs and pin chain

The implementation contract was read in full and authenticated as:

```text
sol/luna_task_157ek_b345_lexfirst_block_checker_projection_v3.md
af5bfe5182e66010fb8893a68ad9f02dda87389171ea425c4122c3fad8addb7c / 13686
```

The active chain is exactly:

```text
P(v2) search/d972_b345_lexfirst_block_target6_v2.py
  ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a / 148824
    -> C(v3) search/check_d972_b345_lexfirst_block_target6_v3.py
       bc0c1c4dfe2e4bc6ea8fd6c18e3af245d20e0959408649dd61d23f969cba9845 / 14032
         -> D(v3) search/d972_b345_lexfirst_block_target6_gha_driver_v3.g
            2637e08c67e48bd0fca41e3b79a68be68344488734123d4043725d5c82971908 / 13805
```

The v3 driver additionally pins frozen v2 checker/driver/task/reply and every
v1, 157eh, 157ec, and q3 predecessor named by v2, with both SHA-256 and byte
count.  The v3 checker authenticates the frozen v2 checker and invokes its
unchanged `authenticate()` gate, retaining all q3/157ec/157ed/157eh/v1 pins.

Unchanged public contract:

```text
receipt schema: d972-b345-lexfirst-block-target6/v2
receipt output: ci/out/d972_b345_lexfirst_block_target6_v2.json
receipt task:   sol/luna_task_157ej_b345_lexfirst_block_target6_v2.md
producer mark: D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_PASS
```

There is deliberately no v3 producer and no v3 mathematical receipt schema.

## Sole repair

The v3 checker is a thin authenticated wrapper around the byte-frozen v2
checker.  It installs one production helper at the exact global
`_project_prefix` resolved by frozen `check_receipt`.  The projection now has
exactly these three keys:

```text
directed_base_support
directed_surgery
prefix
```

The nested `prefix` remains the same nine-field narrowing used by v2:
`counts`, `accounting`, `basis_gate`, `prefix_pool_checkpoint`,
`dependent_events`, `dependent_event_count`, `dependent_event_sha256`,
`fresh_not_imported`, and `source_sha256`.

The helper requires exact key sets and exact values against the authenticated
receipt.  Missing inputs, the incident two-key shape, extra keys, empty/stale/
mutated support, and nested-prefix drift are hard failures.  The resulting
three-key object is passed positionally and unchanged to the existing
`ed.replay_prefix(old, projected, e4, normalized, base_key)`.  That inherited
independent replay remains load-bearing for base support, all translations and
columns, blocker history, dependent events, basis gates, counts, and digests.

No producer code, predicate, pool schedule, column, target, affine row,
terminal meaning, resource boundary, or proof serialization changed.

## Regression fixture contract

The v3 checker self-test first runs the complete frozen v2 checker self-test,
including CONSISTENT/INCONSISTENT, RESOURCE, INPUT, 24 EI mutations, lifecycle,
phase, and selected-proof fixtures.  It then tests the production-installed
projector and publishes these counters:

```text
prefix_projection_three_keys=1
directed_base_support_consumed=1
prefix_projection_omissions_rejected=3
prefix_projection_extra_rejected=1
prefix_projection_support_mutations_rejected=3
prefix_projection_nested_mutations_rejected=2
production_wrapper_entry=1
source_shape_recurrence=1
```

The source-shape recurrence gate binds the patched global to the former
failing locus and confirms the unchanged five positional replay arguments.
A fake replay recorder consumes all three fields.  The full inherited replay
continues to run only in production because it requires the authenticated q3
and fresh large prefix; no digest-only replacement was added.

The bounded combined self-test was executed exactly once with the equivalent
of:

```powershell
$log = Join-Path $env:TEMP 'd972_157ek_combined_selftest.log'
python -u -B search/d972_b345_lexfirst_block_target6_v2.py --self-test *> $log
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -u -B search/check_d972_b345_lexfirst_block_target6_v3.py --self-test *>> $log
exit $LASTEXITCODE
```

Result:

```text
producer exit: 0
checker exit:  0
log: C:\Users\81905\AppData\Local\Temp\d972_157ek_combined_selftest_1787246816115.log
log SHA-256: 8b7a430b138e44a88e12c3923480c6494c3a0f41b4144d6fcb327532f4c351ec
log bytes: 4002
traceback count: 0
```

Exact-once log gates:

```text
D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_SELFTEST_PASS: 1
D972_B345_LEXBLOCK_TARGET6_V2_CHECKER_SELFTEST_PASS: 1
D972_B345_LEXBLOCK_TARGET6_V3_CHECKER_SELFTEST_PASS: 1
D972_B345_FULL_D2_DUAL_CORRELATION_V2_PRODUCER_SELFTEST_PASS: 1
D972_B345_FULL_D2_DUAL_CORRELATION_V2_CHECKER_SELFTEST_PASS: 1
prefix_projection_three_keys=1: 1
directed_base_support_consumed=1: 1
prefix_projection_omissions_rejected=3: 1
prefix_projection_extra_rejected=1: 1
prefix_projection_support_mutations_rejected=3: 1
prefix_projection_nested_mutations_rejected=2: 1
production_wrapper_entry=1: 1
source_shape_recurrence=1: 1
value_root_union=1: 1
source_omission_rejected=1: 1
```

Pre/post hashes were identical:

```text
P(v2) ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a
C(v3) bc0c1c4dfe2e4bc6ea8fd6c18e3af245d20e0959408649dd61d23f969cba9845
D(v3) 2637e08c67e48bd0fca41e3b79a68be68344488734123d4043725d5c82971908
```

No additional execution followed this combined self-test.

## Static audit

```text
checker Python AST parse: PASS
driver ASCII-only: PASS
driver lexical quote/bracket balance: PASS
v3 checker pin in driver: exact once
157ek task pin in driver: exact once
active full path P(v2) -> C(v3): exact once each
v2 receipt output preserved: PASS
unfinished-token count in authorized implementation files: 0
self-test execution: PASS, exactly once
GAP/full/GHA/Git: NOT RUN
```

Scoped status at freeze is expected to contain only these new files plus the
pre-existing Sol task:

```text
?? search/check_d972_b345_lexfirst_block_target6_v3.py
?? search/d972_b345_lexfirst_block_target6_gha_driver_v3.g
?? sol/luna_reply_157ek_b345_lexfirst_block_checker_projection_v3.md
?? sol/luna_task_157ek_b345_lexfirst_block_checker_projection_v3.md
```

The wider shared worktree was already dirty; no unrelated file was modified.

## Run 32394380070 correction record

Run `32394380070`, head
`ff555abffb36cf66a795fdbec932cad647fde5d4`, ended FAILURE.  q3 producer and
checker passed.  The unchanged v2 producer emitted exactly one candidate
marker with terminal `B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT`, after which
the checker raised `KeyError: 'directed_base_support'` at the two-key
projection.  V2 checker and driver PASS markers were absent, artifact upload
was skipped, and the run has zero artifacts.

Repository-external log evidence:

```text
C:\Users\81905\AppData\Local\Temp\gha_run_32394380070_1787245811608.log
b35d8357c9e2ad7788b8493e668eab4be1468bafc38b624837d784e824465c8c / 194263
```

Producer phase timings were provenance-only: fresh prefix 101.887956s,
raw-lambda 13.644790s, correlation 0.967257s, section witness 0.008886s,
block insertion 1.603776s, target reduction 334.109854s; all reported producer
phases sum to 708.054822s.  No receipt SHA, B1 rank, affine rank/nullity, or
dual can be recovered from the absent artifact.

Therefore the producer terminal is a candidate only, not cross-checked
evidence.  It proves neither B1/full-D2 inconsistency nor nonexistence, failed
lift, B4-A, or B4-B.  The failed runner-local receipt is not imported; a fresh
same-job rerun is mandatory.

## Runtime and claim boundary

This repair adds only one dictionary field and bounded projection validation.
It does not duplicate prefix replay or affine work.  Source-only expectation
remains 18–30 minutes for a normal rerun, pessimistically 35–60 minutes, under
the unchanged 300-minute soft and 330-minute job bounds and existing RSS caps.

If a fresh cross-checked result is INCONSISTENT, it is limited to the
registered 108-seed family modulo B1; the next lane is a new B1 dual followed
by complete full-D2 correlation.  CONSISTENT would settle target 6 modulo B1
only; targets 7–33 and a typed lift would remain open.  UNKNOWN_RESOURCE and
UNKNOWN_INPUT carry no mathematical conclusion.

READY_FOR_GHA
