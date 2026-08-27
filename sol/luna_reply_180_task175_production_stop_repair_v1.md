# Luna reply 180 - task175 production stop repair v1

Date: 2026-08-27
Role: Luna bounded implementation/static audit

## 1. Disposition

Disposition is **LATEST PRODUCTION IMPLEMENTATION STOP DIAGNOSED / STATIC
SYMBOL REPAIR COMPLETE / RE-SELFTEST AND PRODUCTION NOT RUN**.
Run `33042556905` remains a hard producer implementation/resource stop.  It
is neither a task175 `READY` receipt nor a mathematical `UNKNOWN`.

The authenticated evidence from that run proves only this control flow:

1. the producer process ended nonzero;
2. the serial shell consequently did not start the checker; and
3. GAP `Exec` continued after the nonzero child shell and then obscured the
   originating failure by trying to read the nonexistent checker log.

The old redirection left no public producer stderr, exit code, receipt, or
artifact from which the final Python exception or signal can be recovered.
Therefore the exact root cause cannot honestly be promoted to `OOM`, timeout,
or a particular Python exception from old-run evidence alone.

Static source inspection does establish a major deterministic resource
amplifier.  The producer's 20 semantic mutations each deep-copied the full
state and, before reaching the cheap field that had been changed, replayed all
6,441 joint words, all PB4 D1 checks, and all 110 Fox pairs.  The checker did
the analogous full reconstruction for each mutation: quotient and retraction,
6,441-row roster, D2, and 110 canaries.  This repeated work is now removed
without removing the one canonical full semantic replay in either component.

The approximately 2,457-second stop does not match a task175 source timer.
There is no producer deadline.  The fine deletion gate is a cardinality cap
at 59,049 states and raises a typed `Unknown`; it is not a wall-clock stop.
The driver's outer timeout is 9,000 seconds, and the registered GHA production
field is 180 minutes.  Thus a diagnostic rerun is still required to distinguish
an implementation traceback from an OS/runner resource exit.  The repaired
driver makes that distinction public.

That diagnostic rerun is now run `33047989700`, head
`95e8868197fa9a591caf56274839947a07b5acb2`.  It reached the flushed
`roster_replayed` boundary and then stopped hard in
`all_seven_fox_sample` at producer line 611.  The exact cause was the bare,
undefined name `add_scaled`; Python exposed a `NameError`, the producer exposed
it as `TASK175_IMPLEMENTATION_STOP`, and the driver emitted exactly
`T175_STAGE_FAILURE stage=PRODUCER exit=1`.  The checker was not started and
no driver PASS or positive receipt was emitted.  Thus the observability and
hard-stop repairs worked exactly as intended.  This run is implementation
failure evidence only, not a mathematical negative result.

No Python, Node, GAP, git, GHA, workflow dispatch, or production command was
run during this commission.

## 2. Final file identities

```text
bytes  SHA-256                                                           path
60306  1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa  search/d972_r07_all_seven_raw_bridge_preflight_v1.py
85848  c55ec99a9a920cd5d0ef92db7d5f2ad841dda7b0f1dcc59a5dc45e469ed6f7cc  crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py
21580  dbe147f98774fde50dee86de7306f9e18243ac1becef0ec7516765bcb2e08765  search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g
 6870  0d9a9588cd4f58531923dc208819f32d552006eea8e323a198382901d132c69f  search/certs/d972_r07_all_seven_raw_bridge_preflight_v1_20260827.json (unchanged)
```

The driver pins the exact producer and checker identities above.  The
checked-in fixture is unchanged.  The reply itself must be hashed by the
parent after its last byte is written; it cannot contain a non-self-referential
hash of itself.

## 3. Complete production-path audit

The reachable producer path was inspected from `run_preflight()` through the
last output write:

1. authenticate the 16 frozen inputs;
2. load the pinned v172/predecessor arithmetic and q3 receipt;
3. reconstruct E3/E4 and the exact context registry;
4. reconstruct the 59,049-state fine deletion and noncontiguous coarse map;
5. load the 26 words and construct `g760`;
6. construct the 243-state joint group and the 6,441-row roster;
7. evaluate every retained roster word and select the deterministic canary;
8. replay both hexagons, the five ordered pentagon factors, direct and prefix
   raw changes, base targets, PB3/PB4 D2, and 110 Fox pairs;
9. execute the producer mutation contract;
10. assemble the lossless receipt and serialize it; and
11. print the old exact producer marker and terminal.

The audit found no internal timer corresponding to 2,457 seconds.  The
59,049-state BFS cap is checked by state count and becomes a registered typed
stop.  The 6,441-row and 110-pair passes have no time-triggered exception.
Generic `TypeError`, `ValueError`, `KeyError`, `MemoryError`, and other
programming/resource exceptions still escape receipt construction as hard
nonzero implementation STOPs.

### Run 33047989700 symbol repair and free-name audit

The failed call was copied in the shape of v172's module-local wrapper,
`add_scaled(old,d,src,scale)`, but task175 neither imports nor defines that
wrapper.  The actual authenticated arithmetic object is the pinned seedspan
module `old`.  It exports the exact API
`add_scaled(target,source,scalar)`, whose operation is the required sparse
mod-3 update.  The independent checker separately implements the same
three-argument operation.

The one-line meaning-preserving repair is therefore:

```text
old.add_scaled(predicted_add,
               old.translate_vector(gb, va, quotient), 1)
```

It still computes `ga + translate(gb,va)` for the actual product Fox
additivity check.  No word, quotient value, coefficient, transcript field,
mutation, terminal, or mathematical acceptance gate changed.

Every callable name reachable inside `all_seven_fox_sample` was then
inventoried.  The eight calls through `old` are exactly:

```text
inv_word, pp_words, reduce_word, f2_substitute, embed_f2_pb3,
fox_gradient_without_sections, translate_vector, add_scaled
```

Each has one definition in the exact pinned predecessor source.  The only
producer-global custom calls are `paper_product`, `element_blob`,
`digest_obj`, and the `Unknown` stop class, each defined before the function.
The remaining calls are its three nested helpers or Python builtins.  Static
search now finds no bare `add_scaled` call in task175 and no other unresolved
custom callable in this function.  This is a static name/API audit, not a
claim that Python was executed locally.

The checker needs no code change: it already defines and uses its own local
three-argument `add_scaled`, and its helper-independent contract deliberately
does not import or execute the producer.  Its bytes/SHA therefore remain
unchanged.  The pin cascade is exact at the actual boundary: the driver now
pins the new producer identity and the unchanged checker identity, and static
comparison of both driver pins with the files is exact PASS.

### Representation boundary

Task175 must not be confused with task176's mixed representation.  The pinned
seedspan arithmetic used here declares `Perm = bytes`, `Pc = bytes`, and
`EKey = tuple[Perm,Pc]`; `MatchedQuotient` constructs both components as
packed bytes.  Its legacy `_element_blob(value)` therefore receives
`bytes + bytes`, not `tuple + bytes`, on this production path.  A task176-style
serializer mismatch is not statically proved as the cause of run
`33042556905`.

For one canonical boundary nevertheless, every task175 producer serialization
site now uses its local `element_blob(value) = bytes(value[0]) +
bytes(value[1])`.  Static search found zero remaining reachable
`old._element_blob` call sites.  This changes no permutation, PC coordinate,
word, group operation, or digest for the actual `(bytes,bytes)` values; it
only prevents representation-sensitive concatenation from being reintroduced
through a predecessor helper.  The independent checker retains its own packed
bytes implementation and imports no producer helper.

### Memory/copy audit

Three avoidable whole-object copies were found and repaired:

- input authentication formerly materialized the 45,246,709-byte v172
  certificate as one `read_bytes()` object; producer and checker now hash all
  pins in 1 MiB chunks;
- the checker formerly parsed a receipt through a full `read_text()` copy;
  it now uses `json.load()` on the stream; and
- producer receipt output formerly built an entire formatted Unicode string,
  concatenated a newline copy, and then encoded it; it now uses `json.dump()`
  directly to the output stream.

These are meaning-preserving storage changes.  A serialization or I/O error
remains hard nonzero and cannot write a typed positive/UNKNOWN terminal.

## 4. Producer mutation repair

The canonical producer algebra is still replayed fully once.  In particular,
the unmutated state still checks:

- the correction in the full joint group;
- every one of the 6,441 roster words in that group;
- D1 of every PB4 column;
- a fresh 110-pair Fox transcript, both same-context witnesses, and the actual
  product-additivity witness; and
- the literal ordered pentagon product.

The 20 mutation candidates now use a shallow top-level state plus deep copies
only for fields physically mutated.  No `deepcopy(base_state)` remains.  The
validator first applies the exact typed dependency gate changed by the
candidate: envelope, correction side, roster digest, PB4 digest, Fox
transcript, contexts/source pairs, derived words, insertion/deletion, raw/base
target separation, or pentagon factors.  Every registered mutation is rejected
there before entering the canonical heavy replay.  This is not a generic
`except Exception`: only the existing explicit `Unknown` and
`MutationReject` classes count as expected mutation rejection.

The large baseline objects (`roster`, PB4 columns, Fox transcript, contexts,
source pairs, raw rows, and pentagon rows) are retained by reference.  A
candidate copies its writable dependency cone before mutation, so it cannot
alter the baseline.  The full canonical replay follows the cheap gates only
for the unique unmutated state.

Flush-labelled progress lines were added at the following completed
boundaries:

```text
pins_authenticated
quotient_bridge_replayed
roster_constructed
roster_replayed
fox_replayed
canonical_mutation_baseline_replayed
semantic_mutations_rejected
receipt_assembled
receipt_serialization_started
```

They are diagnostics only.  They do not replace or duplicate
`D175_PRODUCER_DONE`, and they do not create a receipt on failure.

## 5. Independent checker mutation repair

The checker remains helper-independent: it has no producer loader and locally
implements word algebra, permutations, PC collection, E3/E4, the deletion,
contexts, the joint group, roster, Fox/D1/D2, sparse serialization, and every
receipt comparison.

`validate_ready()` now performs exactly one canonical full reconstruction.
That one reconstruction still rebuilds and evaluates all 6,441 roster rows,
both D2 tables, and all 110 canaries, and `compare_ready()` still validates
the full lossless receipt.  The mutation suite no longer calls
`reconstruct(cert, mutation=...)` 19 times.

Instead, each mutation enters a checker-local algebraic dependency cone:

- correction side: recompute the opposite free product;
- base/corrected sign: recompute the actual H1 raw difference;
- H2 `u/z`, derived `u`, inverse prefix, and derived `z`: recompute the
  affected literal prefix formula in E3;
- three pentagon mutations: multiply the changed five actual E4 factor
  values in the printed order;
- coface swap: rebuild the exact context registry from independently changed
  coface maps;
- rank/blob swaps: rebuild the mutated q3 quotient presentation;
- name-only dedup: check the actual registry cardinality dependency;
- dropped block tag: rebuild the tagged H1/H2/P sparse row;
- insertion/deletion swaps: evaluate the changed formal `d_E i_E` images in
  E3;
- roster letter: alter the deterministic actual word and evaluate it in the
  reconstructed joint group;
- additivity term: run a bounded three-Fox actual product calculation and
  mutate its group-ring term before comparison;
- base-target confusion: rebuild the direct raw rows and compare them with
  the independently reconstructed base targets; and
- terminal marker: enter the normal exact READY envelope validator.

These probes use actual quotient/group/Fox operations.  They do not accept or
reject by whole-certificate or whole-canonical-dictionary equality.  Only the
checker `Stop` class counts as a caught semantic rejection; a Python
programming exception remains a hard checker nonzero.

The checker verdict now reports
`CANONICAL_FULL_RECONSTRUCTION_ONCE_PLUS_INDEPENDENT_DEPENDENCY_CONES` as its
mutation gate.

## 6. Driver observability and fail-closure

The producer and checker remain one serial pair under
`timeout 9000s bash -o pipefail`.  Each command now runs as
`2>&1 | tee <stage-log>`.  The shell immediately copies both entries of
`PIPESTATUS`, selects the original Python status unless only `tee` failed,
and writes it to a separate ASCII exit receipt.

On a nonzero stage the shell emits and appends exactly:

```text
T175_STAGE_FAILURE stage=PRODUCER exit=<code>
```

or

```text
T175_STAGE_FAILURE stage=CHECKER exit=<code>
```

and exits with the retained code.  A producer failure exits before the checker
command.  A checker failure exits before driver PASS.  Because `tee` mirrors
stderr into the GHA step log, the originating traceback or last flushed
progress line is public even if later GAP checks fail.

GAP now audits the producer exit receipt before reading any checker path.  It
audits the checker exit only after producer success.  If the outer timeout or
an abrupt shell death prevents an exit receipt, GAP prints the exact fallback
`exit=MISSING_OR_TIMEOUT`; a missing post-zero stage file has the separate
`exit=MISSING_STAGE_SENTINEL` diagnostic.  Thus the old misleading
`missing ... checker_v1.log` path is no longer reachable after producer
failure.

Pre-existing rejection covers all original outputs plus both exit receipts
and every probe file.  Positive marker, allowed-terminal, JSON coverage,
receipt/checker terminal agreement, and immutable fixture gates are unchanged.
The driver pins the repaired producer/checker and is ASCII-only.

### Bounded SELFTEST failure injection

The successful fixture producer/checker path still has to reach the old exact
`D175_PRODUCER_DONE` and `D175_STATIC_CHECK_PASS` markers and the existing
noncommutative quotient/Fox/D1 fixture.

After that successful path, two shell-only bounded probes run:

1. an injected producer exits 17.  Its isolated log must be exactly the
   injected line plus one `stage=PRODUCER exit=17` line.  The checker-started
   flag, positive receipt, positive verdict, and driver PASS must all be
   absent;
2. an injected checker exits 23.  Its isolated log must be exactly the
   injected line plus one `stage=CHECKER exit=23` line.  Its positive receipt,
   verdict, and driver PASS must all be absent.

Only after both fail-closure probes pass does SELFTEST write
`D175_DRIVER_PASS`.  The injected stage-failure lines in a successful SELFTEST
GHA log are intentional evidence from these two isolated probes.

The one-line Fox symbol repair changes no SELFTEST marker, terminal, failure
probe, or driver contract.  SELFTEST does not execute the production-only
110-pair path, but a fresh SELFTEST is still required because the driver now
pins a new producer identity.  Expected marker text is unchanged.

## 7. Static checks performed

Only read/hash/ASCII/static text checks were used.  They found:

```text
producer deepcopy(base_state) occurrences:                  0
producer old._element_blob occurrences:                     0
producer canonical full mutation-baseline calls:            1
producer streamed json.dump(receipt, stream) calls:          1
producer bare add_scaled calls:                              0
all_seven_fox_sample pinned old APIs found:                  8/8
checker reconstruct calls inside mutation dependency suite: 0
checker canonical reconstruct(cert) calls in validate_ready: 1
driver PIPESTATUS captures:                                  6

## 8. Parent GHA re-SELFTEST receipt

Parent committed the symbol repair and ran GHA SELFTEST as run
`33051307076` at head
`c05936086bb67751279807e32b01128def0a7364`. The workflow completed
successfully and emitted the exact final marker:

```text
D175_DRIVER_PASS
mode=SELFTEST
terminal=FIXTURE_PASS
```

Both injected fail-closure probes were also observed exactly:

```text
T175_STAGE_FAILURE stage=PRODUCER exit=17
T175_STAGE_FAILURE stage=CHECKER exit=23
```

Downloaded `gap-run-out` identities include:

- selftest receipt: `8696 / 46a644588c6fdaadb079a954db9766e2e1d797ebca2ccd13020ca91174a5c336`;
- producer log: `58 / 2c591f0a6757f6f7880f02a751990730442307c9bf2f06c2f8eadd7693f69ea3`;
- checker log: `200 / 00a314da72c44b6abadb619a1fc6bb1be1817d02e1db488670cfdb5092d89df0`;
- driver PASS sidecar: `53 / 668cd02a70318001f9c0079940b759820585ecccd92f8af17aae80b7f5301e54`;
- run log: `402 / 83cb4e09ebdd5a6fe1cce0805b88ceddd1cfe8b795b8c6bb1cfe787bcc1cbadb`.

This promotes the repaired bundle to `SELFTEST PASS`; production READY is
still pending a fresh full run. No local Python, Node, or GAP was used.
driver outer timeout 9000s declarations:                     2
driver non-ASCII bytes:                                      0
driver NUL bytes:                                            0
driver CR bytes:                                             0
driver static double-quoted string scan:                     closed
driver raw parenthesis/bracket counts:                       balanced
fixture bytes/SHA:                                           unchanged
```

The driver contains six `PIPESTATUS` captures because production and SELFTEST
each have producer/checker stages and SELFTEST has two isolated failure
probes.  This does not add a second real producer or checker to production.

Because local Python and GAP execution were explicitly forbidden, Python
parse/runtime and GAP parse/runtime remain **not executed**, not reported as
PASS.  Parent must perform the source review, commit/push, bounded SELFTEST,
and only then production dispatch.

## 8. Exact rerun preambles

SELFTEST:

```gap
D972_R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_MODE:=List([83,69,76,70,84,69,83,84],CharInt);;
Read("search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g");
```

PRODUCTION, only after SELFTEST succeeds at these exact source identities:

```gap
D972_R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_MODE:=List([80,82,79,68,85,67,84,73,79,78],CharInt);;
Read("search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g");
```

Use `out_dir=ci/out`, `with_pquot_packages=false`, and `timeout_min=180`.
No production result is claimed by this static repair.

`TASK175_PRODUCTION_STOP_REPAIR_V1_STATIC_COMPLETE`
