# Luna reply 157em — bounded target-6 full-D2 column generation

## Status

`COMBINED_SELFTEST_PASS / FINAL_FREEZE_READY / FIVE_PRIOR_COMBINED_FAILURES_RETAINED / PRODUCER_DIAGNOSTIC_RETAINED`

Five authorized combined lightweight attempts have been made.  The first four
failed in the producer; the fifth completed the producer and then exposed a
checker-only toy API omission.  The third attempt's PowerShell harness stopped
on the first native stderr record and did not preserve the full traceback.
Sol therefore authorized one bounded producer-only diagnostic, which captured
a fixture no-op.  The fourth attempt reached the production checked-write
validator and exposed that the bounded normal fixture was intentionally not a
sealed production receipt.  Checked-write now uses the already validated exact
UNKNOWN_INPUT fixture while retaining the real production writer and validator
unchanged.  The fifth attempt proved the corrected producer self-test reaches
its final marker, then stopped at the independent checker's reverse-lift toy.
The three checker-fixture corrections described below subsequently passed one
separately authorized combined self-test.  All earlier failure and diagnostic
history remains losslessly recorded.  No GAP computation, full
producer/checker run, GHA dispatch, or Git operation has been run in this task.

The task was read in full and authenticated:

```text
sol/luna_task_157em_b345_target6_dual_colgen.md
60df04261bfd9f30928ed51b26bd501518c05eae43b0bb8ca08507e3b6c4ca99 / 43511
```

Current code freeze:

```text
P search/d972_b345_target6_dual_colgen_v1.py
  8a3dd09811ec790b90f5f3d16890e9ef534a9fc0399597a0daa892605c58c8fc / 410757
C search/check_d972_b345_target6_dual_colgen_v1.py
  08cee7be18128b1dcc1376012854a828695c19a97bd1495e4cb0d7f7ddea035e / 228980
D search/d972_b345_target6_dual_colgen_gha_driver_v1.g
  e67d6397fca2b7181710fe8baf5893f8273399dc43b6c4ec27caebe4f1a903dc / 14634
```

Under the amended pin-cycle contract, the driver authenticates P, C, the task,
and every immediate runtime predecessor but deliberately does not pin this
mutable reply.  This report's own final digest is reported out of band after
freeze; no self-digest or P/C/D/R digest cycle is embedded here.

## Implemented lane

The producer reconstructs fresh B0, then the cross-checked lexicographic first
complete block B1.  It solves target 6 over the registered 108 variables.  For
each inconsistent generation it freshly reverse-lifts the public dual through
the actual current sparse reducer, performs a complete semantic 76-occurrence
by 11-relator correlation, chooses canonical ACTIVE translations, stages every
selected complete 11-column block before mutation, commits at most 1024 blocks
per batch, updates all 109 remainders by incremental normal form, and solves
again.  Bounds are eight batches and 4096 added translation blocks.

Only these mathematical terminals are exposed:

- `B345_E4_D2_COLGEN_TARGET6_CONSISTENT` after actual coefficient replay and a
  positive packed proof;
- `B345_E4_D2_COLGEN_TARGET6_FULL_D2_OBSTRUCTION` only after a complete
  zero-correlation pass for the current full D2 prefix;
- exact `UNKNOWN_RESOURCE` and `UNKNOWN_INPUT` terminals with no provisional
  mathematical claim.

Targets 7–33, a typed lift, full H3, B4-A/B, and global nonexistence remain
outside the claim.

## Exact implementation boundaries

- Public recovery keys are semantic `(component, canonical 154-byte E4 blob)`
  keys.  Exactly one canonical parent is retained; pool IDs and candidate roots
  are private and never serialized.
- Correlation streams the nonzero lifted support against 76 frozen base
  occurrences.  It never enumerates E4, interns into the live pool, or builds a
  full sparse candidate vector in its hot loop.
- Pass 1 completes scalar accumulation and cancellation before ACTIVE
  selection.  One selected-only Pass 2 then chooses the raw-byte lexicographic
  contributor.  A contributor term is not confused with the accumulated
  scalar.
- Every selected block is staged as all 11 raw, typed, and scalar rows before
  persistent mutation.  Translation transactions roll back pool, basis, DAG,
  section, recovery, complete-block mask, and ledger state on an unfinished
  relator.
- The fixed B1 predecessor deliberately bypasses subclass dispatch.  Its 76
  occurrence recovery edges are instrumented manually exactly once.
- Incremental rows are first fully reduced by the pre-batch basis, normalized,
  required to have unique semantic pivots, sorted by pivot, and only then
  applied to all 109 target remainders.  The checker freshly reduces all 109
  rows against its current full basis.
- Receipt validation uses exact terminal/stage key sets, generation-chain
  bindings, phase-aware performance fields, RESOURCE attempted-versus-committed
  prefixes, and a checked-write/readback finalizer.

## Resource and import closure

The local and imported resource registries are separate.  The imported table
has exactly 24 reachable keys, SHA-256:

```text
3acd005b511d12943fb1450a1f0ba920cf26d91cc6ceef71db0fe0e0bd61dd8f
```

`directed_columns`, `candidate_element_pool_suffix`,
`transaction_trace_records`, `blocker_table`, and
`missing_bounded_inverse_representative` are excluded as unreachable.  Each
reachable imported key has a closed `(outer phase, inner phase, current-shape,
comparator)` table.  Producer and checker contain independent literal copies
of all 24 values and reject value drift even when the forged digest is updated.

Production module order is exactly `157el -> 157eh -> 157eg -> 157ed` once.
The q3 object and old producer come only from authenticated
`157ed.authenticated_input`; receipt validators perform no dynamic import.
Pre-authentication INPUT may carry `{}` or the literal imported-cap table; all
other terminals require the literal table.

Immediate frozen inputs include:

```text
157el P  ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a / 148824
157el C  f15a2beeaf1925c1ea4894ef5fae02de6973c36047a91915b7efd12f6d424533 / 21594
157el D  fa288727c77dcbdd8061b066d4863babeaf160dbac8ca4f87ba602a6c7a58836 / 14899
157el task 755861e724fbd66f88b59b9ad9808703f26e2c8016394cb49c0c9cb09ce1f88a / 16945
157el reply af8b33dccc44881fae7533d633922899774738b7dd1c310afbfaeda967417cb6 / 16035
157eh P  6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f / 42449
157eh C  881719f18b302afcb5ee25fd22e36ef7d6b50ee38a3562f208a2adb2a6e74060 / 21933
157eh D  5b76b267a36526f4f2d9e325b4b92e36c7b241f6f9d75abec7e08c3c9ff74cde / 13253
157eh task 5d8da27e3997b261c004bb2fb4a40e9416bed39536816ab2fca9f3a9935c095e / 15015
157eh reply 0b595d82e7fa84ce4ee59256e03ca813b55f36a5c0f90d012ad141554fc23bfa / 10817
157ec P  fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29 / 535219
157ec C  ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981 / 574347
q3 P     b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755 / 76867
q3 C     ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73 / 89082
q3 D     c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831 / 5488
```

The q3 checker path is the actual frozen
`search/check_d972_b345_q3_chief_v1.py`; the obsolete task typo ending in
`q3_finite_v1.py` is not used.

## Cross-checked predecessor evidence

Run `32401947156`, head
`2808c3fb61962d7180a192947fed375c754a25ce`, receipt
`746ca938a962f4d918c07ee270d4e03c3e4f75e40689f3a0507c8daff9d57053`
/ 1,314,365 bytes, is evidence only.  Its pool, basis, affine system, and proof
objects are never imported.  Fresh construction must reproduce the B0/B1
anchors before column generation.

## Independent checker

The checker imports no new producer helper.  It independently authenticates
q3 and all predecessors, rebuilds B0 and fixed B1 with its own pool schedule,
reconstructs recovery semantics, freshly reduces the initial 109 rows, and for
each generation independently:

1. reverse-lifts the dual through the current reducer;
2. recomputes the complete two-pass correlation;
3. decodes and replays every selected section and all 11 columns;
4. decodes the fixed 225-byte ledger records;
5. derives pre-batch quotient rows and checks all 109 fresh current-basis
   remainders;
6. re-solves target 6 and validates the positive proof or full-D2 separator.

For every selected `(t,j)` the checker also rebuilds the exact eleven base Fox
columns, computes the direct semantic left translation and a separate
`old.translate(base_j,t,e4)` typed translation, requires equality, quotient
identity, and translated `D1=0`, and derives the two column hashes through
separate serialization paths.  Its production-core fixture rejects both a
wrong typed translation and a nonzero translated D1.

The checker production loader is fresh.  Its self-test first runs the inherited
157el-v4 chain, then reuses both already-bound 157ed/old checker modules only
through the frozen v2 exact path/SHA/bytes/schema/API gate.  Two calls return
the identical cached tuple; wrong-bound objects are rejected and restored.

Private IDs may differ.  Exact public blob projections, packed bytes, semantic
digests, ranks, terminal, and checked receipt bytes must agree.

## Recurrent-failure guard

| Previous failure mode | Gate in this lane | Static result |
|---|---|---|
| old support-one qstar reused | general reverse-pivot lift; old-qstar boundary says unused after B1 | PASS |
| support label lacked a source section | initial word/offset and canonical translated recovery parents | PASS |
| inherited inverse typo or unbounded materialization | owned INVERSE materializer, reserve, pinned `old.inv_word` | PASS |
| target root omitted six source roots | exact target-first closure and omission canary inherited from 157ej | PASS |
| pool IDs compared across schedules | semantic 154-byte blobs only | PASS |
| wrong `h*g^-1` direction | exact `g*h^-1`, `t*h=g`, orientation mutations | PASS |
| ACTIVE relator alone added | complete ordered 11-relator blocks only | PASS |
| unbounded ACTIVE expansion | 1024/batch, 4096 total, eight batches | PASS |
| contributor chosen before cancellation | full Pass 1 then one selected-only Pass 2 | PASS |
| later inputs changed by early mutation | whole selected batch precompute before commit | PASS |
| JSON block ledger grew without bound | 225-byte records and bounded base64 decoder | PASS |
| one block per expensive target solve | canonical batch then one solve | PASS |
| stale remainder reused | quotient-row incremental NF plus checker all-109 fresh replay | PASS |
| 6-field/11-field accounting conflated | separate semantic and public projections | PASS |
| checker prefix projection lost a key | exact three-key replay projection | PASS |
| monitor phase/identity leaked | exact pair registry and attach/detach gates | PASS |
| dynamic import collision | exact fresh/reuse path/SHA/bytes/schema/API gates | PASS |
| RESOURCE promoted partial math | exact phase prefix, rollback, claim none | PASS |
| RESOURCE reason differed from cap key | reason/key/limit/comparator/source exact | PASS |
| fixture pretended to build full B0 | sealed bounded provider; production main cannot select it | PASS |
| volatile values entered semantic SHA | elapsed/RSS/object IDs excluded | PASS |
| checker copied producer result | independent reconstruction and replay | PASS |
| target coordinate count confused with 109 probes | dynamic semantic coordinate union; probes remain 109 | PASS |
| section registration confused with pool containment | section registry and pool membership gated separately | PASS |
| completed/attempted RESOURCE state conflated | committed batch anchor plus explicit current/rollback ledger | PASS |
| fixture marker was hand-written | markers derive from shared-core counters | PASS |
| base `formula([])` substituted for base gradient | base gradient and delta formulas remain distinct | PASS |
| local comparator reused for imported stop | source-local comparator tables | PASS |
| adaptive mask survived rollback | mask prior value restored/deleted in translation transaction | PASS |
| checker equated typed SHA with raw SHA without replay | independent 11-base rebuild, translation, quotient and D1 gates | PASS |
| inherited checker module reloaded after self-test | exact two-layer reuse plus identical cache and wrong-binding canaries | PASS |
| fixture confused semantic blob with typed Element | local exact decode/roundtrip helper and typed-slot mutation | PASS |

## First authorized combined self-test: exact FAIL history

The initial frozen bundle was:

```text
P cc111c3e051cfb61e167b03c017ccd58182fc279133216e5faa43f3619214d1b / 408870
C 380d12bff3175cf2df6d62ed8091d02e010dd28522ed15fc55817c73689276ba / 228007
D 32b4e965efd725e8aafe86af66449d73192e0b7c4f4d769eece5d771211a1183 / 14442
```

After Sol's static GO, the combined command began at
`2026-08-21T09:59:23.1052444+09:00` and ended at
`2026-08-21T09:59:23.6831328+09:00`.  Producer exit was 1; the conditional
checker launch was not reached.  The exact TEMP log is:

```text
C:\Users\81905\AppData\Local\Temp\d972-157em-combined-selftest-static-go-1.log
6818 bytes
```

Pre/post hashes of P, C, and D were identical to the three initial frozen
values above.  Exact marker counts were:

```text
new 157em producer SELFTEST PASS     0
new 157em checker SELFTEST PASS      0
inherited 157el-v2 producer PASS     1
inherited 157el-v4 checker PASS      0
inherited 157eh-v2 producer PASS     1
inherited 157eh-v2 checker PASS      0
inherited 157eg-v1 producer PASS     1
typed_stage_core=1                   0
typed_stage_mutations=2              0
Traceback (most recent call last):   2
```

The two traceback-string occurrences are the PowerShell native-command wrapper
and the Python traceback for the same failure.  The exact Python path was
`self_test:6811 -> commit_batch:2258 -> recovery_expression_root:1468 ->
_expression_flat:1418 -> SectionExpressionDAG.flat:1735`, ending with:

```text
_d972_157em_selftest_old_producer.Reject:
registered flat section direct quotient replay
```

The sealed fixture registered the generator blob as the direct recovery value
for source word `[1]`, positive signed offset 1.  Fox prefixes are taken before
a positive letter, so that offset materialized the empty word and identity
blob.  The corrective fixture uses source `[1,1]`, offset 2, whose recovered
prefix is `[1]`; therefore public `word_length=1`, `sha_obj([1])`, private
`g_word=[1]`, and the materialization canary stay unchanged.  A separate
RecoveryMap now sends offset 1 through the same production
`recovery_expression_root` and requires rejection.  No production code,
mathematics, order, predicate, cap, or terminal changed.

## First corrective combined self-test: exact FAIL history

The first corrective bundle was:

```text
P 61619b8f147687e3efcb555f13441e142a38b3b6f8c335ec2d9c74c8373d41bf / 409619
C 9d9a800e6e3b0f43819c82de01bac8feda4cff729276b10a001c7acc0a2e1271 / 228007
D 59adaaa2e9e76956a9f11493f9b555fd08a3ac4b433b3b6792ed89f2bab560a7 / 14507
```

After Sol's fixed-diff GO, it began at
`2026-08-21T10:09:09.1846328+09:00` and ended at
`2026-08-21T10:09:09.7503644+09:00`.  Producer exit was 1; the checker was not
started.  The lossless merged stdout/stderr TEMP log is:

```text
C:\Users\81905\AppData\Local\Temp\d972-157em-combined-selftest-corrective-go-1.log
1ea56ba6f7b91142a36c47e45079644ed9add605b6981e12f3c8401a0e2d1f38 / 2920
```

Pre/post P/C/D hashes were identical.  Exact marker counts were:

```text
inherited 157eg-v1 producer PASS     1
inherited 157eh-v2 producer PASS     1
inherited 157el-v2 producer PASS     1
new 157em producer PASS              0
all inherited/new checker PASS       0
positive_prefix_offset=1             0
typed_stage_core=1                   0
typed_stage_mutations=2              0
Traceback (most recent call last):   1
```

The exact Python path was `self_test:6823 -> commit_batch:2295 ->
ToyBasis.add_column:6720 -> ToyPool.intern:6469 -> ToyPool.pack:6461 ->
element_blob:237`, ending with `RuntimeError: 157em canonical E4 blob width`.
`stage_batch` correctly exposes raw semantic keys as `(component,154-byte
blob)`, while the sealed ToyBasis adapter incorrectly passed that blob to
`ToyPool.intern`, whose API accepts an Element `(permutation,pc)` pair.  The
second fixture-only correction decodes through `ToyPool.unpack`, gates exact
bytes type/width and pack roundtrip, then interns the Element.  A typed Element
in the blob slot is rejected through that same local helper.  Production
`SparseBoundaryBasis.add_column`, ToyPool, stage_batch, mathematics, order,
predicate, cap, and terminal are unchanged.

## Third authorized combined attempt: harness FAIL history

The third combined attempt used this fixed bundle:

```text
P 242d798189247af9a8d5c894c21ddd03ef53e759fc65a90f43972dd627546eb7 / 410472
C 70b6d7fa8a10bb117e9e8f361c0d8bcdbb498c012d526ed8f000018578269912 / 228007
D 04cf6e70e1bd0cdef0299a1f40a151197834e046511c84a6a3722f5c17ece473 / 14570
R 930dd11afd91613b0b14c2551addc27712e26f34672b89750577c55e8e6aad72 / 18129
```

The producer was invoked once.  The PowerShell wrapper had
`$ErrorActionPreference='Stop'` while using native `2>&1 | Tee-Object`.
Windows PowerShell converted the producer's first stderr traceback record into
a terminating `NativeCommandError`; execution therefore left the harness
before it captured Python's `$LASTEXITCODE` or entered the conditional checker
branch.  The checker was not started.  The wrapper/tool exit was 1.  The only
stderr retained by the tool boundary was the header
`python.exe : Traceback (most recent call last):`; the rest was lost, so this
attempt is explicitly **not** represented as a lossless traceback.

The partial TEMP log is:

```text
C:\Users\81905\AppData\Local\Temp\d972-157em-combined-selftest-attempt3-go-1.log
740a3ffcc3aed5904a3e750c99d5d4e9f98e6c41f6dfdcb979e4a67b6eeef8ef / 1622
created 2026-08-21T10:21:09.8252765+09:00
written 2026-08-21T10:21:09.8878007+09:00
```

It contains exactly one producer marker from each of inherited 157eg-v1,
157eh-v2, and 157el-v2; it contains zero new 157em producer markers, zero
checker markers, zero `fixture_blob_decoder=1`, zero
`positive_prefix_offset=1`, zero `typed_stage_core=1`, zero
`typed_stage_mutations=2`, and zero traceback headers.  Pre/post P/C/D/R
hashes and byte counts were identical to the bundle above.  There was no
rerun, edit, or reply update after this failed combined attempt.

## Authorized producer-only diagnostic: exact FAIL history

Sol authorized one producer-only diagnostic against that same fixed P.  C,
full computation, GAP, GHA, and Git were forbidden and were not run.  The
scope was exactly:

```text
cmd.exe /d /c python -u -B search\d972_b345_target6_dual_colgen_v1.py --self-test > "%TEMP%\d972-157em-attempt3-producer-diagnostic.log" 2>&1
```

It began at `2026-08-21T10:28:16.1308948+09:00` and ended at
`2026-08-21T10:28:16.8249121+09:00`; producer exit was 1.  The checker was not
started.  Direct `cmd.exe` redirection retained the complete merged stream:

```text
C:\Users\81905\AppData\Local\Temp\d972-157em-attempt3-producer-diagnostic.log
a509e1f967c791a3b71c3ac76a516d485c06efabd604f931bd61a058d3d6387b / 1755
created 2026-08-21T10:28:16.1620907+09:00
written 2026-08-21T10:28:16.7936689+09:00
```

The complete log was:

```text
D972_B345_FULL_D2_DUAL_CORRELATION_PRODUCER_SELFTEST_PASS production_correlation=1 terminal_schema=1 active=1 separator=1 cancellation=1 orientations=3 public_shape=1 resource=1 section=1 cap_sources=2 serialization_finalizer=1 provenance=1 performance=1
D972_B345_FULL_D2_DUAL_CORRELATION_V2_PRODUCER_SELFTEST_PASS registry_pairs=18 shared_clock=1 reserve=1 outer_resources=2 actual_dag_1024=1 packed_reducers=2 proof_serializers=2 detach=1 v1_fixture=1
D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_SELFTEST_PASS block_core=1 relator9_independent=1 target_reducer=2 consistent_proof=1 inconsistent_dual=1 schemas=4 selected_core=1 normal_finalizer=2 ei_mutations=24 completed_fixture_validator=2 partial_presence=3 monitor_callbacks=1 checked_write=1 value_root_union=1 source_omission_rejected=1 inherited_eh=1
Traceback (most recent call last):
  File "C:\Users\81905\Desktop\shadow-atelier\search\d972_b345_target6_dual_colgen_v1.py", line 7757, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "C:\Users\81905\Desktop\shadow-atelier\search\d972_b345_target6_dual_colgen_v1.py", line 7747, in main
    self_test(); return 0
    ~~~~~~~~~^^
  File "C:\Users\81905\Desktop\shadow-atelier\search\d972_b345_target6_dual_colgen_v1.py", line 7583, in self_test
    expect_failure(lambda bad=bad: validate_receipt(
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        bad, allow_unsealed=True), "resource " + field)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\81905\Desktop\shadow-atelier\search\d972_b345_target6_dual_colgen_v1.py", line 6087, in expect_failure
    raise RuntimeError("157em mutation accepted: " + label)
RuntimeError: 157em mutation accepted: resource comparator
```

Exact counts were inherited producer markers 1/1/1, new 157em producer 0,
all checker markers 0, `fixture_blob_decoder=1` 0,
`positive_prefix_offset=1` 0, both typed-stage markers 0, and traceback 1.
Pre/post P/C/D/R hashes were unchanged.

The RESOURCE fixture itself is a local `producer_soft_rss_bytes` stop whose
closed comparator is `ge`.  Its mutation table also assigned `ge`, so the
purported mutation was a literal no-op and the production validator correctly
accepted the unchanged receipt.  Sol authorized only changing that fixture
mutation to `gt`, which is genuinely wrong for the RSS stop and must be
rejected.  Production code, receipt schema, resource semantics, mathematics,
order, caps, predicate, and terminals are unchanged.

## Fourth authorized combined self-test: exact FAIL history

After the comparator-fixture correction, Sol authorized one robust combined
self-test against this bundle:

```text
P 09706ffac72af65f1d46a199da78279b6f3eb5a470777fa3503a82032f42d04b / 410472
C 9e2ba226fcb714af66bd48a20b513e86634751ea791349ce298bd879d394f5ba / 228007
D 9e15444eba8b728485de51b1c9fdd8942a9d0ab1ecdfe7cd7f3da7c0ba102edc / 14570
R 4f767902416f70755c8ad5f722fb7f3f49ce8e70fa610063575bcf3da0c954ac / 23679
```

The `cmd.exe` harness began at `2026-08-21T10:42:57.3135659+09:00`.
The producer ran from `10:42:57.3193705` through `10:42:58.0437000` and
exited 1.  The checker was conditionally guarded and was not started.  The
complete merged log is:

```text
C:\Users\81905\AppData\Local\Temp\d972-157em-combined-selftest-post-comparator-go-1.log
88383bb636ac32b1661ebd0126e0c9a131ff066b421b88c9a97e0457321d5967 / 2460
created 2026-08-21T10:42:57.3557985+09:00
written 2026-08-21T10:42:58.0124592+09:00
```

Its complete output was:

```text
D972_B345_FULL_D2_DUAL_CORRELATION_PRODUCER_SELFTEST_PASS production_correlation=1 terminal_schema=1 active=1 separator=1 cancellation=1 orientations=3 public_shape=1 resource=1 section=1 cap_sources=2 serialization_finalizer=1 provenance=1 performance=1
D972_B345_FULL_D2_DUAL_CORRELATION_V2_PRODUCER_SELFTEST_PASS registry_pairs=18 shared_clock=1 reserve=1 outer_resources=2 actual_dag_1024=1 packed_reducers=2 proof_serializers=2 detach=1 v1_fixture=1
D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_SELFTEST_PASS block_core=1 relator9_independent=1 target_reducer=2 consistent_proof=1 inconsistent_dual=1 schemas=4 selected_core=1 normal_finalizer=2 ei_mutations=24 completed_fixture_validator=2 partial_presence=3 monitor_callbacks=1 checked_write=1 value_root_union=1 source_omission_rejected=1 inherited_eh=1
Traceback (most recent call last):
  File "C:\Users\81905\Desktop\shadow-atelier\search\d972_b345_target6_dual_colgen_v1.py", line 7757, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "C:\Users\81905\Desktop\shadow-atelier\search\d972_b345_target6_dual_colgen_v1.py", line 7747, in main
    self_test(); return 0
    ~~~~~~~~~^^
  File "C:\Users\81905\Desktop\shadow-atelier\search\d972_b345_target6_dual_colgen_v1.py", line 7682, in self_test
    written, raw = write_checked(target, copy.deepcopy(normal))
                   ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\81905\Desktop\shadow-atelier\search\d972_b345_target6_dual_colgen_v1.py", line 6072, in write_checked
    validate_receipt(receipt)
    ~~~~~~~~~~~~~~~~^^^^^^^^^
  File "C:\Users\81905\Desktop\shadow-atelier\search\d972_b345_target6_dual_colgen_v1.py", line 5488, in validate_receipt
    require(all(receipt[key] for key in ("base_q3_replay",
    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        "normalized_inverse_fibre", "seed_manifest", "source_preflight",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
        "initial_target", "generation_ledger", "packed_block_ledger")),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        "157em completed receipt stage payload")
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\81905\Desktop\shadow-atelier\search\d972_b345_target6_dual_colgen_v1.py", line 215, in require
    raise RuntimeError(message)
RuntimeError: 157em completed receipt stage payload
```

Exact counts were inherited producer markers 1/1/1, new 157em producer 0,
all checker markers 0, `fixture_blob_decoder=1` 0,
`positive_prefix_offset=1` 0, both typed-stage markers 0, both requested
resource marker substrings 0, and traceback 1.  Pre/post P/C/D/R hashes were
identical to the bundle above.  No rerun or reply edit followed that attempt.

The bounded CONSISTENT fixture deliberately left these fourteen production
stage payloads empty: `base_q3_replay`, `normalized_inverse_fibre`,
`seed_manifest`, `source_preflight`, `directed_base_support`,
`directed_surgery`, `prefix_B0`, `base_columns`, `fixed_B1_block`,
`fixed_B1_anchor`, `old_qstar_boundary`, `raw_parent_manifest`,
`recovery_map`, and `initial_target`.  Its earlier
`validate_receipt(..., allow_unsealed=True)` call correctly validates only the
present bounded payloads.  Production `write_checked` correctly calls strict
`validate_receipt(receipt)`, whose completed-stage gate rejects that normal
fixture before the frozen prefix, generation cross-binding, performance-phase,
and production-provider gates.  The validator is correct and remains
unchanged.

The checked-write fixture now selects the already constructed exact
`B345_E4_D2_COLGEN_TARGET6_UNKNOWN_INPUT` receipt, hard-gates that token before
the call and on the returned receipt, and preserves the existing fixed-point
`receipt_bytes`, exact file readback, SHA, and fixed q3-pin assertions.  That
terminal legitimately has no mathematical stage payload, so it passes the
same strict production validator without pretending to construct the 362k-row
prefix.  Production `write_checked`, `validate_receipt`, and
`allow_unsealed` semantics are byte-for-byte unchanged.

## Fifth authorized combined self-test: exact FAIL history

After the UNKNOWN_INPUT checked-write fixture correction, Sol authorized one
robust combined self-test against this bundle:

```text
P 8a3dd09811ec790b90f5f3d16890e9ef534a9fc0399597a0daa892605c58c8fc / 410757
C 27e319b3be1f7be75a197a5e6ca21bfb8a83e21b9765c6d0bb90006e856544e8 / 228007
D 22a606d0594c0c2b44e28c1864ef600a2e945275b688d8c4e7e353df67c13c9f / 14570
R 8efefa12b3a132a0f8e26d9c0345359ffb613e348df358d909f04af8a9253af1 / 29076
```

The combined harness began at `2026-08-21T10:52:23.6127696+09:00`.
The producer ended at `10:52:24.2382712` with exit 0.  Only after that success
did the checker start; it ended at `10:52:25.1158171` with exit 1.  The lossless
merged log is:

```text
C:\Users\81905\AppData\Local\Temp\d972-157em-combined-selftest-input-write-go-1.log
316014be3e1e5d3010be3e59672836e48dfffeb4ad3a685e2c0774875a79e1de / 4293
created 2026-08-21T10:52:23.6283982+09:00
written 2026-08-21T10:52:25.1001957+09:00
```

The new producer marker occurred exactly once.  Its inherited EG, EH-v2, and
EI-v2 producer markers each occurred once.  On the checker side the inherited
EG, EH-v2, EI-v2, EI-v3, and EI-v4 markers each occurred once, while the new
157em checker marker did not occur.  `fixture_blob_decoder=1`,
`positive_prefix_offset=1`, `resource_registry=1`, and
`resource_current_scopes=1` each occurred once.  The checker had not yet
reached `typed_stage_core=1` or `typed_stage_mutations=2`.  There was exactly
one traceback:

```text
Traceback (most recent call last):
  File "C:\Users\81905\Desktop\shadow-atelier\search\check_d972_b345_target6_dual_colgen_v1.py", line 4282, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "C:\Users\81905\Desktop\shadow-atelier\search\check_d972_b345_target6_dual_colgen_v1.py", line 4273, in main
    self_test(); return 0
    ~~~~~~~~~^^
  File "C:\Users\81905\Desktop\shadow-atelier\search\check_d972_b345_target6_dual_colgen_v1.py", line 4153, in self_test
    lifted, _ = reverse_lift(ToyOld(), ToyPool(), ToyBasis(), ToySystem(),
                ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                             remainders, [], [])
                             ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\81905\Desktop\shadow-atelier\search\check_d972_b345_target6_dual_colgen_v1.py", line 1621, in reverse_lift
    require(not system.consistent and isinstance(dual, dict) and
                ^^^^^^^^^^^^^^^^^
AttributeError: 'ToySystem' object has no attribute 'consistent'
```

Pre/post P/C/D/R hashes were identical to the attempted bundle.  No edit,
rerun, or reply update followed the failure until Sol completed a read-only
trace and authorized the bounded fixture correction.

The trace found that `reverse_lift` needs only `system.consistent` and
`system.dual_public()`.  The toy now supplies exact `consistent=False` without
changing the production API.  It also pre-closes the next two deterministic
fixture failures found by the same trace: the new semantic pivot is the exact
zero blob and is hard-ordered before the `0x01` and `0x02` blobs, and only the
single 109-row toy incremental call receives a 30-second local clock.  That
call saves the exact `(CHECKER_STARTED, CHECKER_DEADLINE, CHECKER_CHECKS)`
triple, resets the counter, captures exactly 109 checks, and restores the exact
prior triple in `finally`.  No production `tick`, deadline adapter, reducer,
mathematics, schema, or terminal changed.  The final checker marker derives
`fixture_scope_repairs=3` from these three passed shared-path gates, and the
driver requires that marker exactly once.

## Sixth authorized combined self-test: PASS

Sol authorized exactly one combined run against the fixed bundle.  Pre-run
pins were:

```text
P 8a3dd09811ec790b90f5f3d16890e9ef534a9fc0399597a0daa892605c58c8fc / 410757
C 08cee7be18128b1dcc1376012854a828695c19a97bd1495e4cb0d7f7ddea035e / 228980
D e67d6397fca2b7181710fe8baf5893f8273399dc43b6c4ec27caebe4f1a903dc / 14634
R 3a651dfe6e646068cbf87b62033ed9169cd2137a6138944cf4ac34015930f992 / 32896
```

The robust harness invoked the producer once and invoked the checker once only
after producer exit 0.  Both stdout and stderr were redirected by `cmd.exe`
into one repository-external log.  The producer and checker both exited 0:

```text
overall start  2026-08-21T11:07:23.0539373+09:00
producer start 2026-08-21T11:07:23.0695578+09:00
producer end   2026-08-21T11:07:23.6889536+09:00  exit 0
checker start  2026-08-21T11:07:23.6889536+09:00
checker end    2026-08-21T11:07:24.6022892+09:00  exit 0
overall end    2026-08-21T11:07:24.6022892+09:00

C:\Users\81905\AppData\Local\Temp\d972-157em-combined-selftest-checker-fixture-go-1.log
6272f9f246bef2b8002427e60e5751e932248fa0ba9811291cfbf5ebcf70aac8 / 3578
created 2026-08-21T11:07:23.1008006+09:00
written 2026-08-21T11:07:24.5710481+09:00
```

The harness wall interval was about 1.548 seconds (producer about 0.619 seconds,
checker about 0.913 seconds).  The harness did not sample process RSS, so no
self-test RSS number is claimed.  Required occurrence counts were:

```text
new 157em producer marker                    1
new 157em checker marker                     1
inherited EG producer/checker                1 / 1
inherited EH-v2 producer/checker             1 / 1
inherited EI-v2 producer/checker             1 / 1
inherited EI-v3 checker                      1
inherited EI-v4 checker                      1
fixture_scope_repairs=3                      1
fixture_blob_decoder=1                       1
positive_prefix_offset=1                     1
typed_stage_core=1                           1
typed_stage_mutations=2                      1
resource_registry=1                          1
resource_current_scopes=1                    1
independent_reverse_lift=1                   1
independent_correlation=1                    1
incremental_all109=1                         1
Traceback (most recent call last):           0
```

The bare `packed_225=1` substring occurs twice, once in each new marker; the
driver's producer-specific composite
`packed_225=1 terminals=4 checked_write=1` occurs exactly once, while the new
checker marker itself is exact once.  The complete merged output was:

```text
D972_B345_FULL_D2_DUAL_CORRELATION_PRODUCER_SELFTEST_PASS production_correlation=1 terminal_schema=1 active=1 separator=1 cancellation=1 orientations=3 public_shape=1 resource=1 section=1 cap_sources=2 serialization_finalizer=1 provenance=1 performance=1
D972_B345_FULL_D2_DUAL_CORRELATION_V2_PRODUCER_SELFTEST_PASS registry_pairs=18 shared_clock=1 reserve=1 outer_resources=2 actual_dag_1024=1 packed_reducers=2 proof_serializers=2 detach=1 v1_fixture=1
D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_SELFTEST_PASS block_core=1 relator9_independent=1 target_reducer=2 consistent_proof=1 inconsistent_dual=1 schemas=4 selected_core=1 normal_finalizer=2 ei_mutations=24 completed_fixture_validator=2 partial_presence=3 monitor_callbacks=1 checked_write=1 value_root_union=1 source_omission_rejected=1 inherited_eh=1
D972_B345_TARGET6_DUAL_COLGEN_V1_PRODUCER_SELFTEST_PASS prefix_provider=1 reverse_lift=1 correlation=2 section_inverse=1 resource_registry=1 monitor_pair_registry=1 upstream_throw_site_exact=1 authenticated_frontend=4 exact_157eg_prefix_projection=1 recovery_4096_monitor_pairs=1 recovery=1 stage_batch=1 commit_batch=1 incremental109=1 incremental_order=1 nested_validators=3 stable_prefix_payloads=1 contributor_aggregate_split=1 generation_cross_bind=1 packed_generation_bindings=1 resource_current_scopes=1 selected_payload_serializers=1 incremental_foreign_progress=1 single_recovery_edge_path=1 transaction_rollback=1 complete_block_registry=1 fixed_B1_manual_recovery=1 positive_prefix_offset=1 fixture_blob_decoder=1 receipt_validator=1 packed_225=1 terminals=4 checked_write=1 mutations=107 inherited_157el=1
D972_B345_FULL_D2_DUAL_CORRELATION_CHECKER_SELFTEST_PASS production_correlation=1 terminal_schema=1 active=1 separator=1 cancellation=1 orientations=3 public_shape=1 resource_schema=1 section_decoder=1 inverse_mutation=1 state_snapshot=1 cap_sources=2 deadline_bridge=1 provenance=1 performance=1
D972_B345_FULL_D2_DUAL_CORRELATION_V2_CHECKER_SELFTEST_PASS registry_pairs=18 cross_rejections=1 shared_clock=1 check_reserve=1 duplicate_inner_two_outers=1 outer_inner_mutations=3 stale_detach=1 v1_production_core=1
D972_B345_LEXBLOCK_TARGET6_V2_CHECKER_SELFTEST_PASS block_core=3 relator9_independent=1 target_reducer=4 consistent_proof=1 inconsistent_dual=1 schemas=4 selected_core=2 completed_core=2 ei_mutations=24 lifecycle_mutations=9 independent_pool_schedule=1 monitor_callbacks=1 serialization_resource=1 inherited_eh=1
D972_B345_LEXBLOCK_TARGET6_V3_CHECKER_SELFTEST_PASS prefix_projection_three_keys=1 directed_base_support_consumed=1 prefix_projection_omissions_rejected=3 prefix_projection_extra_rejected=1 prefix_projection_support_mutations_rejected=3 prefix_projection_nested_mutations_rejected=2 production_wrapper_entry=1 source_shape_recurrence=1 inherited_v2_checker=1
D972_B345_LEXBLOCK_TARGET6_V4_CHECKER_SELFTEST_PASS semantic_public_accounting_split=1 semantic_ledger_as_public_rejected=1 public_ledger_as_semantic_rejected=1 public_only_omissions_rejected=5 public_relation_mutations_rejected=6 semantic_shape_mutations_rejected=2 replayed_live_entries_bound=1 completed_anchor_production_wrapper=1 eleven_key_validator_retained=1 completed_anchor_source_recurrence=1 inherited_v3_projection=1
D972_B345_TARGET6_DUAL_COLGEN_V1_CHECKER_SELFTEST_PASS independent_reverse_lift=1 independent_correlation=1 incremental_all109=1 packed_225=1 terminals=4 stable_schema=1 resource_schema=1 lifecycle_reuse=1 fixed_B1_dispatch=1 typed_stage_core=1 typed_stage_mutations=2 fixture_scope_repairs=3 mutations=17 inherited_157el_v4=1
```

Post-run P/C/D hashes and byte counts were exactly identical to the pre-run
bundle.  The pre-update reply hash was also unchanged by the self-test; only
this authorized evidence/READY update changes R.  No additional Python
execution followed the PASS.

## Static audit and final self-test

Completed static checks:

```text
python -m py_compile search/d972_b345_target6_dual_colgen_v1.py
python -m py_compile search/check_d972_b345_target6_dual_colgen_v1.py
```

Both passed.  Static import/API audit found no active predecessor attribute
mismatch; the sole optional `_source_prefix_rows` access is guarded by
`hasattr`.  Producer/checker schema, task SHA, caps, algorithm, top-level keys,
monitor table, throw-site table, 24 imported-cap values, and cap digest agree.
The driver pin table was checked against every listed local file; it contains
no current-reply path, accepts exactly one mode, fixes the optional output,
deletes stale q3/current/predecessor output, uses quoted Python paths, and
passes one decreasing 18,000-second budget from producer to checker.  Full-mode
gates bind the produced receipt SHA/bytes to the producer marker and require
exactly one terminal, producer PASS, checker PASS, visible phase output, and
the final driver PASS marker.

The separately authorized final combined self-test executed these two commands
in sequence, with the second conditional on the first exit 0:

```text
python -u -B search/d972_b345_target6_dual_colgen_v1.py --self-test
python -u -B search/check_d972_b345_target6_dual_colgen_v1.py --self-test
```

The five earlier combined failures, including the explicitly incomplete third
harness capture, and the complete producer-only diagnostic remain retained
above without promoting the diagnostic into a combined self-test.  The final
combined command exited zero, both new markers and all required inherited
markers occurred exactly once, traceback count was zero, and P/C/D hashes were
unchanged.

## Runtime expectation and residual risk

Expected production bands remain 30–70 minutes for one or two batches,
90–180 minutes for several batches, and a hard 300-minute shared producer plus
checker allowance.  The principal residual risk before self-test/full dispatch
is the large fresh B0 reconstruction and Python sparse-reducer memory pressure;
no claim or universe is weakened if a declared resource bound is reached.

No result in this reply is called cross-checked until a full producer and
independent checker both pass.  Nothing here is called verified; that word is
reserved for Lean.

READY_FOR_GHA
