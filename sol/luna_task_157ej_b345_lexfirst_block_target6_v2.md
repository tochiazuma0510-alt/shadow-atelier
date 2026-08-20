# Luna task 157ej - versioned value-root coverage repair for the lex-first block lane

## 0. Role and authorized files

Create a minimal **versioned successor** to frozen task 157ei.  The already-run
v1 bundle is immutable.  Luna may create or edit only these four new files:

1. `search/d972_b345_lexfirst_block_target6_v2.py`
2. `search/check_d972_b345_lexfirst_block_target6_v2.py`
3. `search/d972_b345_lexfirst_block_target6_gha_driver_v2.g`
4. `sol/luna_reply_157ej_b345_lexfirst_block_target6_v2.md`

Do not modify any v1 file, frozen q3/157ec/157eg/157eh file, workflow, claims
ledger, dialogue book, or other worktree file.  Temporary selftest material
belongs outside the repository.  Luna may run the bounded combined selftest,
but not a production scan, GAP, GHA, or Git.  The parent session owns commit,
push, dispatch, and artifact handling.

Start by copying the final frozen v1 producer/checker/driver into the three v2
paths.  Preserve every v1 mathematical predicate, candidate/seed order,
column order, terminal meaning, resource cap, monitor boundary, receipt field,
and independent replay.  The sole mathematical-path repair is the exact
WordExpr value-root coverage in Section 3.  Version the schema/output,
selftest/pass markers, logs, sentinels, and driver paths so no v1 output can be
mistaken for v2.  Use schema
`d972-b345-lexfirst-block-target6/v2` and output
`ci/out/d972_b345_lexfirst_block_target6_v2.json`.  Use these exact v2 markers:

```text
D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_SELFTEST_PASS
D972_B345_LEXBLOCK_TARGET6_V2_CHECKER_SELFTEST_PASS
D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_PASS
D972_B345_LEXBLOCK_TARGET6_V2_CHECKER_PASS
```

The four mathematical terminal strings remain exactly the frozen v1 strings:

```text
B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT
B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT
B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE
B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_INPUT
```

Do not version or alias these terminal strings.  Schema, paths, pins, markers,
and sentinels distinguish v2 transport; the token names denote the unchanged
mathematical branches.

## 1. Frozen inputs

Hard-authenticate the complete final 157ei bundle:

```text
search/d972_b345_lexfirst_block_target6_v1.py
  f901cffd73069e78c9cc256e1a6c18c7e7ce6adef6d4de0c4fe68970571476bb / 143075
search/check_d972_b345_lexfirst_block_target6_v1.py
  d0601533131008002d09a6320ab643df865a2a86245ed23f399e4c469bd93c57 / 128399
search/d972_b345_lexfirst_block_target6_gha_driver_v1.g
  e0cb01bf119ae7834fa85da7910c6dd82048c8ae756e48f834fad055a7bc4c0a / 10516
sol/luna_reply_157ei_b345_lexfirst_block_target6.md
  de6c22867a7a66cb28fdbbffae2f92632e8dfc382a5f7088a097d7518cef2ad2 / 13277
sol/luna_task_157ei_b345_lexfirst_block_target6.md
  cfe0c50046a750e4169c473872c5770ce76c105267353e82c9ed19de01c043f4 / 24179
```

Retain every upstream pin from v1, including the same-job q3 artifact and the
frozen 157ec and 157eh bundles.  The v2 checker authenticates the final v2
producer path/SHA/bytes.  The v2 driver authenticates final v2 producer,
checker, task, and all inherited inputs.  No digest may be filled from a live
file at runtime.

## 2. Exact failure evidence and claim boundary

GHA run `32391706973`, attempt 1, exact head
`8045966623b17c264567798032ca35b73c7e3ea6`, authenticated checkout/GAP and
optional p-quotient package setup.  The math step then failed after the
complete lex-first block was inserted, on this call chain:

```text
_target6_system_core
  -> old._affine_candidate_values
  -> WordExprEvaluator.pin_source_roots
  -> WordExprEvaluator._gradient_node
  -> hard require: "WordExpr flat value/gradient"
```

The run conclusion was failure, artifact upload was skipped, artifact count
was zero, and no receipt, receipt SHA, checker PASS, counts receipt, or
mathematical terminal exists.  This run is regression evidence only.  It is
not CONSISTENT, INCONSISTENT, RESOURCE, INPUT, an obstruction, or any other
mathematical result.  The v2 reply and receipt provenance must say this
exactly; never invent a receipt SHA for the failed run.

The local cause is exact.  The v1 producer called the frozen 157ec helper with

```python
pin_sources=True, value_roots=[target6_root]
```

`evaluate_values([target6_root])` computes values only on that root's reachable
closure and leaves every unreachable DAG node at its typed identity
placeholder.  `pin_source_roots(six_source_roots)` subsequently requests Fox
gradients for six additional roots.  A reachable FLAT_WORD under such a source
root can therefore compute a nonidentity direct value while comparing against
an unevaluated identity placeholder.  The hard failure is correct; the caller
failed to establish the evaluator precondition.

## 3. Sole production repair: exact target plus six-source value roots

### 3.1 Load-bearing invariant

For a `WordExprEvaluator`, before requesting gradients at a set `G`, exact
quotient values must have been evaluated on the complete DAG closure
`Reach(G)`.  In this call the eventual gradient roots are exactly

```text
G = {target6_root} union set(base_compiled["source_roots"]),
```

where the ordered source-root list has exactly six entries.  Preserve the
frozen source-root order.  Do not replace it by a set iteration, sorting,
pool/DAG allocation order, or receipt-derived order.

Factor construction and validation of the ordered coverage roots into one
small production-shared helper.  Its normal result is exactly

```python
[target6_root, *list(base_compiled["source_roots"])]
```

and its semantic set must equal the target root union all six source roots.
It must hard-reject a missing source root, missing target root, extra root,
reordering, malformed/non-node root, or any proposed list other than this
exact target-first/source-order sequence.  Duplicates, if the frozen DAG ever
contains one, are retained in this ordered public-to-helper contract; the
frozen evaluator itself takes the reachable set and evaluates nodes in DAG
ordinal order.  Do not silently deduplicate or reorder at the caller.

Use the helper at the failing base call:

```python
base_value_roots = exact_pinned_value_roots(
    target6_root, base_compiled["source_roots"])
base_eval = old._affine_candidate_values(
    base_compiled, e4, 0, static,
    pin_sources=True,
    value_roots=base_value_roots)
```

The exact helper name may differ, but the call graph and gates may not.  Keep
`pin_sources=True`: changing it to false would bypass the intended six-source
pin/value-gradient canary.  Do not evaluate only the target, only the six
sources, or a receipt-selected subset.  Evaluating the entire DAG would be
mathematically safe but is outside this minimal repair; use the exact union.

After this union evaluation, `pin_source_roots` remains in the frozen source
order, seals the same memo pin stage, and the target gradient is evaluated as
before.  Root enumeration order cannot alter values because evaluation is in
DAG ordinal order.  This is a cache/value-availability repair only: it must not
change the literal word, quotient, Fox formula, target, candidate order,
108-seed order, B1 basis, affine equations, first terminal, receipt claim, or
resource semantics.

Do not modify the frozen 157ec helper.  Do not catch or downgrade
`WordExpr flat value/gradient`; any failure after correct coverage remains a
hard internal failure.

### 3.2 Producer regression gates

The production call must use the shared helper, not duplicate list syntax in
an untested branch.  Add bounded selftest canaries that traverse this exact
helper and require:

- target first and all six frozen-order source entries are present;
- omitting each source entry is rejected (at least the exact omission that
  reproduces the old target-only list must be explicitly named);
- target omission, source reordering, and one extra root are rejected;
- the accepted sequence is passed unchanged as `value_roots` while
  `pin_sources=True` to the production wrapper.

A small fake-call recorder may be injected into the helper boundary to prove
the exact keyword arguments without constructing q3.  If a bounded typed toy
DAG/quotient is already available, also prove disjoint target/source roots:
target-only values followed by unrelated-source gradient is rejected, while
union values followed by the same gradient succeeds.  Do not introduce a new
large reconstruction merely for that optional toy.  The real production
`pin_source_roots` hard equality remains the final runtime gate.

Selftest markers must publish exact entry counts such as
`value_root_union=1` and `source_omission_rejected=1`; syntax-only coverage is
not enough.

## 4. Checker and receipt invariants

The independent v2 checker retains the v1 mathematical replay.  It already
computes the base gradient by direct Fox replay and, for each typed target,
evaluates values and gradients on the same target-root closure.  It does not
pin unrelated producer source roots and therefore needs no mathematical
predicate change for this incident.

The checker must:

1. authenticate the final v2 producer SHA/bytes and v2 task;
2. retain independent reconstruction of q3, B0, the complete 11-column block,
   B1, all 109 target remainders, and the 108-variable system;
3. retain the corrected two-layer selftest-only module reuse from frozen v1;
4. never import the producer coverage helper or trust producer DAG IDs;
5. reject schema/path/pin drift and require exactly one v2 checker marker.

The coverage-root list and DAG node IDs are private evaluator scheduling data,
not mathematics.  Do not add transient node IDs, cache contents, or pin order
to the receipt.  No receipt mathematical field or terminal claim is weakened
or widened.  Apart from v2 schema/path/marker provenance, the receipt remains
the v1 exact stage-aware schema.

## 5. Preserve all frozen v1 repairs

The successor must retain and rerun every final v1 bounded fixture.  In
particular, preserve:

- exact stage-aware `phase_seconds` sets;
- presence-sensitive `_partial`: explicit empty block prefix maps to `None`,
  explicit nonempty maps to its digest, and absent key alone may fall back to
  the completed block;
- producer normal-fixture target/affine exact replay, including rejection of
  the former accepted `delta_rows_sha256` mutation;
- checker selftest reuse of both exact module keys
  `_d972_157eg_pinned_157ed_checker` and
  `_d972_157ed_independent_old_checker`, with path/SHA/bytes/schema/API/pin
  gates and restoration-safe wrong-module canaries;
- production checker fresh-load path, one absolute deadline, monitor adapter
  identity/detach gates, resource partials, checked-write fallback, and exact
  terminal keysets.

The v2 repair must not reopen any of these paths.

## 6. Selftest, driver, and rerun boundary

Run one bounded combined v2 selftest outside the repository.  Require exactly
one producer selftest marker and one checker selftest marker, all inherited v1
markers exactly once where expected, the old fixture/mutation counts, and the
new coverage/omission markers.  A traceback hidden by a shell pipeline is a
failure.  Capture the complete combined log outside the repository and report
its path and SHA.

The v2 GAP driver must:

- pin the final v2 producer, checker, and task hashes;
- retain same-job q3 generation and independent q3 checking;
- use v2-only output/log/sentinel names and remove them before starting;
- use pipefail/tee and one shared absolute deadline;
- require exactly one producer terminal and exactly one independent checker
  PASS marker before artifact upload;
- fail on missing/duplicate markers, syntax/traceback, hash drift, stale v1 or
  v2 output, checker failure, or absent artifact.

Luna must not run the full job.  After parent commit/push/dispatch, a full v2
rerun is the first source of mathematics.  It must pass the prior failure
locus, produce a canonical receipt, run the independent checker, and upload
the artifact before any receipt SHA/count/result is reported.  The failed v1
run cannot be resumed and supplies no checkpoint.

Expected runtime remains the v1 band: normally about 20--32 minutes for an
INCONSISTENT branch, potentially 27--55 minutes for CONSISTENT selected proof,
with the inherited pessimistic 45--90 minute non-resource band and unchanged
300-minute soft/330-minute job limits.  Adding six value roots to one small
base DAG evaluation is negligible relative to fresh prefix and checker replay.

## 7. Recurrence-prevention table

The reply must include this table with concrete source lines and PASS/FAIL:

| Hazard | Required prevention |
|---|---|
| target-only value table followed by six-source gradients | exact target-first plus six-source coverage helper |
| omitting one source while retaining `pin_sources=True` | production-shared omission-reject canary |
| disabling source pins to hide the failure | `pin_sources=True` hard gate |
| unordered set/dedup root construction | exact frozen source sequence equality |
| evaluating roots but requesting a different gradient set | helper call recorder and runtime flat value/gradient gate |
| treating node IDs/cache order as receipt mathematics | no root IDs or cache state in receipt |
| overwriting the already-run v1 bundle | v2-only authorized paths and pins |
| stale checker after producer repair | v2 checker authenticates final v2 producer; driver pins both |
| classifying run 32391706973 as mathematics | explicit failure/no-artifact/no-receipt statement |
| schema-only fixture missing semantic drift | retain producer target/affine exact fixture replay |
| empty mid-block prefix falling back to completed block | retain presence-sensitive `_partial` and 3 canaries |
| inherited checker `sys.modules` collision | retain exact two-layer fixture reuse; production fresh path unchanged |
| timing/resource fields accepting arbitrary keys | retain exact terminal/stage phase sets and resource registries |
| shell pipeline hiding a traceback | pipefail, full log, exit sentinel, exact markers |

## 8. Reply and freeze

The new reply must list:

- all four authorized paths with final SHA-256 and byte length;
- inherited authenticated pins and the final P -> C -> driver pin chain;
- exact diff from v1, including schema/path/marker-only versioning and the one
  production value-root repair;
- bounded selftest command, external log path/SHA, exact PASS markers/counts;
- explicit statement that run 32391706973 had no mathematical result;
- terminal meanings and unchanged claim boundary;
- source-only runtime/RSS band;
- `git status --short` evidence showing only the four authorized new files.

End the reply with exactly:

```text
READY_FOR_GHA
```
