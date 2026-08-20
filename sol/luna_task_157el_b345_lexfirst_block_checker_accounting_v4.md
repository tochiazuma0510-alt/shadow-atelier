# Luna task 157el — lex-first target-6 completed-anchor accounting repair v4

## 0. Role, scope, and authorized files

Implement the smallest versioned checker-only successor to failed full run
`32397796696`.  Luna may create or edit only these three implementation/report
files:

1. `search/check_d972_b345_lexfirst_block_target6_v4.py`
2. `search/d972_b345_lexfirst_block_target6_gha_driver_v4.g`
3. `sol/luna_reply_157el_b345_lexfirst_block_checker_accounting_v4.md`

This Sol-authored task file is the implementation contract.  Do not edit the
frozen v2 producer, any v1/v2/v3 checker or driver, any predecessor, q3 bundle,
workflow, claim ledger, dialogue book, or other repository file.  Temporary
self-test output belongs outside the repository.  Do not run a full production
job, GAP, GHA, Git commit, or push; the parent session owns those actions.

Reuse the frozen v2 producer exactly.  There is no v3 or v4 producer.  Keep the
v2 receipt schema, receipt output, receipt `task_sha256`, mathematical
predicate, candidate, ordered 11-column block, target-6 affine system, terminal
tokens, and claim boundary unchanged.  The only semantic repair is the
independent checker's completed-anchor argument wiring: its six-field
checker-native replay accounting must not be passed as though it were the
producer's eleven-field public accounting receipt.

## A. Exact frozen inputs

Authenticate path, SHA-256, and byte count before self-test or checking:

```text
search/d972_b345_lexfirst_block_target6_v2.py
  ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a / 148824
search/check_d972_b345_lexfirst_block_target6_v2.py
  fb28b8b4c7b42f5d83dd1f5c762136812d36731c427a003aae8a8fb0c36a66ba / 130007
search/check_d972_b345_lexfirst_block_target6_v3.py
  bc0c1c4dfe2e4bc6ea8fd6c18e3af245d20e0959408649dd61d23f969cba9845 / 14032
search/d972_b345_lexfirst_block_target6_gha_driver_v3.g
  2637e08c67e48bd0fca41e3b79a68be68344488734123d4043725d5c82971908 / 13805
sol/luna_task_157ek_b345_lexfirst_block_checker_projection_v3.md
  af5bfe5182e66010fb8893a68ad9f02dda87389171ea425c4122c3fad8addb7c / 13686
sol/luna_reply_157ek_b345_lexfirst_block_checker_projection_v3.md
  accf8cf58f511ebca7b30a1409be02a742a454762220df6c1ea9d9c69eb327b0 / 8603
search/d972_b345_lexfirst_block_target6_gha_driver_v2.g
  48f5717b9be1d6f6087cdf2864d20d41df2475f5d0d87b43c2bd1deefab01394 / 13597
sol/luna_task_157ej_b345_lexfirst_block_target6_v2.md
  1d6f14ef9f799a43fc344daa38606281dbcf0b2fe47d86db0b44df382762f290 / 14667
sol/luna_reply_157ej_b345_lexfirst_block_target6_v2.md
  f00a3f56e140663002e85a488f78b37ade796126928d475f30bb57e951020428 / 8676
```

The v4 checker must retain every q3/157ec/157ed/157eh/v1 pin authenticated by
the frozen chain.  Do not silently repin a predecessor.  The final v4 checker
must authenticate this 157el task by its final SHA and byte count.  The v4
driver must pin the unchanged v2 producer, final v4 checker, this task, frozen
v3 checker/driver/task/reply, and all upstream inputs already pinned by v3.

Keep exactly:

```text
receipt schema  d972-b345-lexfirst-block-target6/v2
receipt output  ci/out/d972_b345_lexfirst_block_target6_v2.json
receipt TASK    sol/luna_task_157ej_b345_lexfirst_block_target6_v2.md
producer marker D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_PASS
```

Only checker/driver version metadata, v4 markers, authentication, and the
repair below may differ.  In particular, the unchanged producer's receipt must
still carry the frozen 157ej task SHA, not this 157el task SHA.

## B. Run 32397796696: exact incident and claim boundary

Full run `32397796696`, exact head
`f7dc097f2b9f317898f3e5035329235156561008`, failed after 19m49s.  A
repository-external downloaded log has SHA-256
`3e2da0f3b54cab45d70102818592bb0de77dee3abc582ce36d9927ceb688bc15`
and 196222 bytes.  It is provenance evidence only and must not be an input.

The q3 producer/checker and the unchanged v2 producer completed.  The latter
printed exactly:

```text
D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_PASS
terminal=B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT
```

Its stable phase timings included authenticated 169.117504s, source preflight
86.342308s, fresh prefix 104.089495s, raw-lambda oracle 14.257491s,
correlation 1.104663s, section witness 0.008473s, block insertion 1.748643s,
and target reduction 333.197588s.  Times and RSS are volatile provenance and
must not enter any stable digest.

The v3 checker passed the repaired three-key prefix projection, independently
replayed all 32768 prefix translations, entered completed block replay, and
then failed exactly at the inherited v2 check:

```text
check_d972_b345_lexfirst_block_target6_v3.py:187 -> v2.check_receipt
check_d972_b345_lexfirst_block_target6_v2.py:1781 -> _validate_completed_core
check_d972_b345_lexfirst_block_target6_v2.py:1569 -> validate_anchor
check_d972_b345_lexfirst_block_target6_v2.py:1761 -> _validate_anchor_public
check_d972_b345_lexfirst_block_target6_v2.py:1545
  _validate_completed_block_anchor(block, anchor)
check_d972_b345_lexfirst_block_target6_v2.py:453
  RuntimeError: checker complete block accounting relation
```

The driver then rejected the missing math sentinel.  There was no checker PASS,
no driver PASS, no artifact, and no cross-checked terminal.  The producer's
INCONSISTENT value remains a candidate only.  It is not evidence of B1
inconsistency, full-D2 inconsistency, nonexistence, a failed lift, B4-A, or
B4-B.  The failed job cannot be resumed and its runner-local receipt must not
be imported.  A fresh same-job producer/v4-checker rerun is required.

## C. Exact defect: two accounting types were conflated

The frozen checker deliberately has two different accounting records.

### C.1 Checker-native replay ledger: six fields

Frozen v2 `_replay_block` lines 1084--1087 and 1121--1126 construct:

```text
columns
pivots
dependent
live_sparse_entries
pool_size
pool_order_sha256
```

These are checker-private replay values.  The checker does not reconstruct the
producer's private provenance DAG or section-expression registry, nor should
it copy their private IDs.  Frozen lines 1186--1197 already compare the
load-bearing semantic projection of the independently replayed block with the
producer block.  That comparison checks the ordered 11 columns, raw rows,
q-star scalars, rank gain, relator-9 pivot theorem, shadow rank, and the four
mathematical basis counts.  Pool allocation/order is intentionally private and
not public equality.

### C.2 Producer public receipt ledger: eleven fields

Frozen `_validate_completed_block_anchor` lines 446--475 requires the public
producer receipt's exact eleven accounting keys:

```text
columns, pivots, dependent, live_sparse_entries,
pool_size, pool_order_sha256,
DAG_nodes, DAG_edges,
section_bindings, section_expression_nodes, section_expression_edges
```

It checks the public `pre_accounting -> post_accounting` relations, including
the one new section binding and eleven inserted columns, and binds that public
ledger to `post_block_anchor`.

### C.3 The sole bad wire

Frozen lines 1755--1763 receive the six-field replayed block from
`_replay_block`, then pass that object to `_validate_anchor_public`.  The latter
calls the eleven-field public validator.  Therefore the exact key-set test at
line 453 must fail even though the semantic equality at line 1196 has passed.
This is a deterministic checker false negative, not a producer mathematical
failure or a reason to weaken either ledger.

## D. Required repair

### D.1 Completed-anchor callback

At the completed normal-path callback, validate the two types separately:

1. keep `_replay_block(..., data["translation_block"])` and its frozen semantic
   equality at lines 1186--1197 load-bearing and unchanged;
2. call the existing full public anchor validator with the authenticated
   producer receipt objects

   ```python
   data["translation_block"], data["post_block_anchor"]
   ```

   not with the six-field checker replay object;
3. pass the independently replayed basis live-entry count as the separate
   `live_basis_entries` argument, so the frozen anchor still must equal the
   actual checker replay state;
4. explicitly bind the replay object's post `live_sparse_entries` to that
   same checker basis count before public-anchor validation.

The intended logical shape is:

```python
def validate_completed_anchor(replayed):
    # Six-field checker-native object remains independently replayed and typed.
    require(exact_checker_accounting_shape(replayed),
            "157el checker semantic accounting type")
    require(replayed["post_accounting"]["live_sparse_entries"] ==
            basis.live_entries,
            "157el replayed basis live-entry binding")
    _validate_anchor_public(
        data["translation_block"],
        data["post_block_anchor"],
        frozen=True,
        live_basis_entries=basis.live_entries)
```

Equivalent factoring through one production-shared helper is preferred.  The
exact helper name is not prescribed.  If the v4 file remains a thin wrapper,
it may install a narrowly scoped wrapper around the frozen completed-core
callback, but it must authenticate the original source shape and must not use
key-count sniffing inside `_validate_anchor_public`, catch the exception, fill
missing public fields, or relax exact key sets.  A mechanical v4 checker copy
is also allowed if the diff is demonstrably limited to the v3 projection
repair, this callback wiring, authentication, and markers.

### D.2 Both validators remain strict

Do not change or bypass:

- `_validate_completed_block_anchor` and its exact eleven-key public ledger;
- `_validate_anchor_public` and its full block/anchor relations;
- `_replay_block`'s raw-column reconstruction, ordered absorption, relator-9
  independence, and semantic comparison at frozen lines 1186--1197;
- the separate frozen post-anchor equality to independently replayed
  `basis.live_entries`;
- the v3 exact three-key prefix projection repair.

Never synthesize the five producer-only DAG/section fields from checker counts.
Never compare producer and checker private pool IDs or allocation order.  Never
replace the independent replay with receipt equality or a digest-only gate.

### D.3 No other predicate or schema change

Retain unchanged all q3/E3/E4/source/context gates, correlation and section
witness replay, B0 basis, ordered B1 block, target-6 109 rows, 108-variable
affine system, complete contradiction absorption or selected proof, absolute
deadline, monitor/cap registries, checked-write rules, RESOURCE/INPUT paths,
and all four v2 terminal meanings.  Do not special-case the expected
INCONSISTENT candidate.

## E. Required regression fixtures

Fixtures must exercise the same production helper/callback used by the actual
`check_receipt` path.  A toy-only validator is insufficient.  At minimum:

1. construct a six-key checker-native replay block and an independent
   eleven-key producer public block plus anchor; the repaired production
   callback accepts the correctly paired objects;
2. reproduce the incident by passing the six-key block into the full public
   validator and require rejection at a named
   `semantic_ledger_as_public_rejected` canary;
3. pass the eleven-key public block into the checker-semantic ledger gate and
   require rejection at a named `public_ledger_as_semantic_rejected` canary;
4. omit each of the five public-only fields (`DAG_nodes`, `DAG_edges`,
   `section_bindings`, `section_expression_nodes`,
   `section_expression_edges`) and require fail-closed rejection;
5. mutate the public section-binding increment, column increment, rank gain,
   dependent increment, anchor binding, and anchor semantic digest, one at a
   time, and require rejection by the unchanged public validator;
6. mutate the independently replayed live-entry count and require rejection by
   the separate live-basis gate even when the public block and anchor remain
   mutually consistent;
7. omit or add a checker-native accounting key and require rejection;
8. source-shape recurrence proves the frozen bad callback occurs exactly once
   and that the installed production path calls the repaired helper exactly
   once with `data["translation_block"]`, `data["post_block_anchor"]`, and the
   independently replayed live-entry count;
9. all inherited v2 and v3 completed CONSISTENT/INCONSISTENT, RESOURCE, INPUT,
   24 receipt mutations, three-key projection, lifecycle, phase-key, and proof
   fixtures remain live and pass.

Publish exact counters, for example:

```text
semantic_public_accounting_split=1
semantic_ledger_as_public_rejected=1
public_ledger_as_semantic_rejected=1
public_only_omissions_rejected=5
replayed_live_entries_bound=1
completed_anchor_production_wrapper=1
inherited_v3_projection=1
```

Use new exact markers such as:

```text
D972_B345_LEXBLOCK_TARGET6_V4_CHECKER_SELFTEST_PASS
D972_B345_LEXBLOCK_TARGET6_V4_CHECKER_PASS
```

The unchanged producer continues to emit v2 markers.  The fixture must also
contain a mutation showing that merely deleting the eleven-key validator would
be rejected by the self-test contract.

## F. v4 driver and fresh rerun contract

Create an ASCII-only v4 driver.  It must:

1. pin the unchanged v2 producer, final v4 checker, this task, frozen v3
   checker/driver/task/reply, frozen v2 task/reply, and every upstream pin;
2. regenerate q3 and independently check q3 in the same job exactly as v3;
3. remove the stale v2 receipt and all v4 logs/sentinels before starting;
4. run the unchanged v2 producer from scratch, then v4 checker against the
   same v2 output, under one shared absolute 18000-second deadline with
   pipefail/tee;
5. require exactly one registered v2 producer terminal, exactly one v4 checker
   PASS marker, and exactly one v4 driver PASS sentinel;
6. fail closed on traceback, missing/duplicate marker, stale output, pin drift,
   checker nonzero exit, missing receipt, unsupported terminal, or deadline;
7. upload the v2 receipt and bounded logs only after producer and checker both
   pass.

Self-test mode runs unchanged v2 producer self-test plus the actual v4 checker
self-test and exact-counts all inherited and new markers.  Production mode
must not use either failed run's runner-local output or any imported prefix
checkpoint.  Driver/output optional-variable behavior stays identical to v3,
apart from v4 names and pins.

## G. Terminal and claim boundary

Accept only the four frozen v2 tokens:

```text
B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT
B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT
B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE
B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_INPUT
```

Their meanings do not change.  Only a fresh producer/v4-checker PASS makes a
terminal cross-checked.  A cross-checked INCONSISTENT result concerns the exact
108-variable target-6 affine system after the one fixed lex-first 11-relator
block over the frozen 32768-translation prefix.  It is not a full-D2
obstruction, global nonexistence theorem, B4-A, or B4-B.  RESOURCE and INPUT
remain UNKNOWN.  The repair itself proves no mathematics.

## H. Performance and report

This is checker wiring only.  Normal runtime should remain in the observed
v2/v3 band: roughly 17--25 minutes total on the hosted runner, with target
reduction and independent prefix replay dominant.  Treat a material new
runtime or memory regression as a STOP and diagnose it; do not cache or skip
independent replay to recover time.

The reply must report:

- final SHA-256 and byte count for v4 checker, v4 driver, this task, and reply;
- every frozen pin and exact diff scope;
- combined self-test command, exit status, exact marker counts, and the new
  ledger-split counters;
- source-shape recurrence evidence for the production callback;
- confirmation that v2 schema/output/receipt task hash and producer are
  unchanged;
- confirmation that no full production run, GAP, GHA, Git action, or
  unauthorized file edit occurred;
- `git status --short` inventory distinguishing pre-existing changes from the
  three authorized outputs.

## I. Recurrence-prevention table

| Boundary | Required type | Forbidden recurrence |
|---|---|---|
| `_replay_block` result | six-key checker-native accounting | treating it as producer provenance receipt |
| semantic equality | independently replayed ordered block and four basis counts | private pool/DAG/section ID equality |
| public block validator | original eleven-key `data["translation_block"]` | filling missing keys from checker state |
| anchor validator | original `data["post_block_anchor"]` plus separate replayed live count | trusting producer anchor without replay binding |
| prefix input | v3 exact three-key projection | reverting to the old two-key projection |
| fixture | actual production callback/helper | toy helper that bypasses the failing path |
| terminal | fresh same-job producer + v4 checker PASS | promoting either failed producer candidate |

