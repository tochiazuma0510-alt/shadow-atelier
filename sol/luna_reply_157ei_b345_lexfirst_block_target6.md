# Luna reply 157ei — lex-first complete block and target 6

## Status and scope

The four-file v1 implementation is READY after the final authorized combined
selftest passed.  The first two attempts stopped in the producer and the third
stopped in the checker; all three fixture-only causes and their repairs remain
recorded below.  The fourth attempt ran the unchanged final P/C/D freeze and
passed producer plus independent checker with every required marker exactly
once.

The mathematical lane is exactly:

1. fresh reconstruction of the authenticated 157eh prefix `B0`;
2. fresh complete old-qstar correlation and the canonical first ACTIVE
   translation;
3. persistent insertion of that translation's eleven relator columns in
   order, giving `B1`;
4. a fresh target-6 affine solve for the fixed ordered 108-seed universe.

It does not add all 568 old ACTIVE rows, inspect targets 7--33, exhaust full
`D2`, construct a typed lift, or assert B4-A/B.

## Frozen paths

| role | path | SHA-256 | bytes |
|---|---|---:|---:|
| producer | `search/d972_b345_lexfirst_block_target6_v1.py` | `f901cffd73069e78c9cc256e1a6c18c7e7ce6adef6d4de0c4fe68970571476bb` | 143075 |
| checker | `search/check_d972_b345_lexfirst_block_target6_v1.py` | `d0601533131008002d09a6320ab643df865a2a86245ed23f399e4c469bd93c57` | 128399 |
| driver | `search/d972_b345_lexfirst_block_target6_gha_driver_v1.g` | `e0cb01bf119ae7834fa85da7910c6dd82048c8ae756e48f834fad055a7bc4c0a` | 10516 |
| task | `sol/luna_task_157ei_b345_lexfirst_block_target6.md` | `cfe0c50046a750e4169c473872c5770ce76c105267353e82c9ed19de01c043f4` | 24179 |

The checker independently authenticates the final current producer path,
SHA, and byte length.  The driver authenticates the final producer, checker,
and task SHAs before either mode runs.  This is intentionally a one-way pin
chain: the producer receipt authenticates the frozen upstream inputs; it does
not claim a cyclic self/checker/driver hash.

## Load-bearing implementation gates

- The complete old correlation is replayed before selecting its first row.
  The exact 154-byte `t`, its contributing pair, `t=g*h^-1`, left action,
  section word, and stable correlation digest are bound.
- The section oracle is distinct from pool containment.  The translation must
  be absent from the section table, is registered exactly once, and the public
  block requires `section_newly_registered=true`.
- All eleven raw columns are recomputed termwise, checked for quotient identity
  and `D1*D2=0`, and inserted in relator order.  Direct old-qstar values are
  `0` for relators 1--8 and `1` for relator 9.
- The actual pivot count is sampled immediately before and after relator 9;
  the latter must equal the former plus one.  It is not inferred.
- The public block ledger has closed nested keysets, canonical 154-byte row
  encodings, raw/reducer digests, pre/post accounting, rank gain, and an
  ID-free post-block anchor.
- Target 6 rebuilds the base gradient directly.  `formula([])=0` is used only
  as the empty-delta canary, and `b=-z` is explicit.  Every one of the 108
  seed deltas is direct-vs-typed replayed and freshly reduced modulo `B1`.
- The transposed solver derives its coordinate count dynamically from the
  union of base and delta coordinates.  The number `109` means remainder
  probes, not affine coordinate rows.  Absorption continues after the first
  contradiction.
- A consistent branch passes through the shared selected-literal replay and
  reachable proof builder.  An inconsistent branch publishes a normalized
  dual only after the full system; support is bounded by the noncontact
  theorem `support <= 109 < 128`.

## Independent checker and production-path fixture

The checker rebuilds q3/E3/E4, the 108 words and source gates, `B0`, qstar,
the complete correlation and section, the ordered eleven-column block, the
post-block anchor, all 109 target remainders, and the final affine result.  It
does not import producer pool/DAG/section IDs.  Public equality is canonical
component plus exact 154-byte blob equality.

The bounded fixture is wired through shared production block absorption,
target reduction, selected replay, normal finalization, exact envelopes, and
the checker's shared completed-receipt core.  Both consistent and inconsistent
fixtures are noncommutative.  Twenty-four EI-specific mutations per side cover
the complete-block omit/relator9-only/duplicate/reorder/index/blob/digest
cases, qstar scalars, section registration, pre-block anchor, base and RHS
orientation, old-`B0` import, noncommutative order, continued contradiction
absorption, target row/delta digests, selected coefficients/support/proof, and
stale RESOURCE/INPUT fields.  The pinned 157eh production-path selftests are
also invoked for complete correlation orientation and packed section/DAG
coverage.

The original combined command was run once.  Its producer-side log is:

```text
C:\Users\81905\AppData\Local\Temp\d972_157ei_combined_selftest_1787241340073.log
```

That attempt had exit status 1.  It recorded exactly one inherited 157eg
producer marker and exactly one inherited 157eh-v2 producer marker.  The 157ei
producer marker count was zero; the checker was not launched and all checker
marker counts were zero.  P/C/D hashes were unchanged by the attempt.

The targeted diagnostic (not a second official combined run) located the stop
at producer `validate_receipt_schema(resource_row, fixture=True)`: the RESOURCE
fixture copied a completed receipt, supplied an explicit empty
`current.block_prefix`, and `_partial` hashed the empty prefix because a
completed block was also present.  The validator correctly required `None` for
an explicit empty current prefix.  This is fixture-only; a real mid-block
RESOURCE receipt has not yet committed the completed block.

The repair makes `_partial` presence-sensitive:

- explicit empty `block_prefix` gives `None`;
- explicit nonempty `block_prefix` gives that prefix's SHA;
- an absent key alone permits fallback to the completed block columns.

All three cases use the shared production `_partial` helper and are now bounded
canaries (`partial_presence=3`).  The mathematical and normal paths are
unchanged.

The authorized corrective combined attempt is recorded at:

```text
C:\Users\81905\AppData\Local\Temp\d972_157ei_corrective_combined_selftest_1787242015568.combined.log
```

It also exited 1 in the producer; the checker was not started.  Pre/post P/C/D
hashes were identical.  The inherited 157eg and 157eh-v2 producer markers each
occurred exactly once, while the 157ei producer and every checker marker had
count zero.  Its complete traceback ended at the EI mutation labelled
`target delta-row digest`: the producer schema-only mutation helper accepted a
changed public digest because the fixture does not serialize the underlying
delta rows from which that digest can be derived.

A targeted collect diagnostic, not an official combined rerun, traversed the
remaining EI fixture: this was the unique accepted mutation; the other 29
expect-failure checks rejected.  The repair adds a bounded completed-fixture
validator.  After the production receipt schema, it exact-compares normal
terminal `target6` and `affine_system` records with the values freshly produced
by the already shared `_fixture_affine` target core.  All 24 receipt mutations
now pass through this wrapper.  No digest is hardcoded; baseline entry count is
bound as `completed_fixture_validator=2`.  Production `run`, mathematics, and
normal receipt behavior are unchanged.

The next authorized corrective attempt is recorded at:

```text
C:\Users\81905\AppData\Local\Temp\d972_157ei_next_corrective_combined_selftest_1787242363116.combined.log
```

The producer exited 0 with its EI marker exactly once.  The checker was then
started and exited 1 before its EI marker.  All inherited 157eg and 157eh-v2
producer/checker markers occurred exactly once, and P/C/D hashes were unchanged.
The checker traceback stopped when `eg.load_ed_checker()` required a fresh
`_d972_157eg_pinned_157ed_checker`; the inherited checker selftest had already
loaded it.  Its `ed.load_old()` would analogously have collided with the already
loaded `_d972_157ed_independent_old_checker`.

The repair is checker-selftest-only.  It reuses those two exact existing module
objects after independently binding each `sys.modules` key, resolved file path,
SHA, byte length, schema, required API, and the 157ed old-checker pin chain.  The
old checker API is exactly `CheckerAffineSystem` plus
`checker_target_row_transposed`.  Nine bounded lifecycle mutations reject wrong
paths, wrong SHAs, missing APIs, bare substitutes at both layers, and a stale
old-checker pin.  Production `check_receipt` retains its original fresh
`load_ed_checker()` then `load_old()` path unchanged.

The final authorized combined attempt is recorded at:

```text
C:\Users\81905\AppData\Local\Temp\d972_157ei_lifecycle_corrective_combined_selftest_1787242875725.combined.log
```

Producer and checker both exited 0.  The EI producer/checker markers and all
four inherited 157eg/157eh-v2 producer/checker markers each occurred exactly
once.  Producer stderr and checker stderr were empty.  The final marker payloads
bound `ei_mutations=24`, `completed_fixture_validator=2`,
`partial_presence=3`, `completed_core=2`, and `lifecycle_mutations=9`.
P/C/D pre/post hashes were byte-for-byte unchanged:

```text
P f901cffd73069e78c9cc256e1a6c18c7e7ce6adef6d4de0c4fe68970571476bb
C d0601533131008002d09a6320ab643df865a2a86245ed23f399e4c469bd93c57
D e0cb01bf119ae7834fa85da7910c6dd82048c8ae756e48f834fad055a7bc4c0a
```

The driver additionally requires each inherited 157eh producer/checker
selftest marker exactly once.

## Resource, driver, and transport boundary

The exact outer/inner monitor registry uses one clock/RSS epoch.  Prefix,
block, target, and proof adapters are identity-gated and detached.  RESOURCE
records use closed phase-specific committed/attempted ledgers, including raw
and shadow block prefixes, target seed prefixes, and a completed-system
projection at the dual-support boundary.  Receipt serialization uses checked
canonical write/readback and a committed-block RESOURCE fallback; the checker
has an independent serialization-resource fixture.  The phase-timing ledger
also has an exact terminal/stage-aware completed-phase keyset; arbitrary or
future phase labels cannot be injected as diagnostics.

The thin GAP driver:

- removes stale q3/output/log/sentinel files;
- regenerates q3 in the same job with the pinned package path and independently
  checks it;
- uses `bash -o pipefail`, live `tee`, and a shared absolute 18000-second
  producer/checker budget;
- accepts exactly one of the four registered terminal strings and exactly one
  independent checker PASS marker;
- treats the optional output variable as an exact fixed-path assertion.

Expected runtime remains approximately 20--32 minutes for the likely
INCONSISTENT branch, 27--55 minutes for a CONSISTENT proof branch, with the
task's pessimistic 45--90 minute non-resource band and sub-2-GiB expectation.

## Recurrent-failure guard

| guard | result | binding |
|---|---|---|
| dynamic coordinate count is not 109 | PASS | derived from exact coordinate union; 109 retained only as probe count |
| section registration is not pool containment | PASS | absent-section gate followed by exactly-one registration |
| old qstar is not reused after the block | PASS | qstar gates only the new block; target system is rebuilt modulo `B1` |
| RESOURCE committed/attempted states are separate | PASS | exact substage relations and prefix digests |
| normal finalizer is shared with fixtures | PASS | `_finalize_normal_terminal` entry counter |
| fixture markers come from real entry counters | PASS | block/target/selected/completed/finalizer counters are hard-gated |
| checker shares no producer IDs or fixture shortcut | PASS | independent canonical replay through `_validate_completed_core` |
| base gradient is not `formula([])` | PASS | direct base binding plus separate empty-delta canary and mutation |

Future CV-9 freeze list: retain the authenticated 157ec, 157ee, and 157eg
artifacts plus every lex-first iterative block receipt and its ordered eleven
column ledger.

## Static audit

- previous pre-repair `python -B -m py_compile` on producer and checker: PASS;
  the authorized final combined run then exercised both final files.
- all fixture-only patches and the final P -> C -> driver pin chain were
  inspected statically before that run.
- task and predecessor pin constants: present; current checker pins producer;
  driver pins producer/checker/task.
- placeholder scan: zero after final pinning.
- first combined selftest attempt: **FAIL (exit 1)** at the diagnosed
  fixture-only RESOURCE prefix mismatch; checker not started.
- corrective combined selftest attempt: **FAIL (exit 1)** at the unique
  accepted target-delta-digest mutation; checker not started.
- next corrective combined selftest attempt: producer **PASS**, checker
  **FAIL (exit 1)** at the inherited-module fresh-load collision.
- final corrective combined selftest: **PASS**, producer/checker exit 0,
  required markers each exactly once, P/C/D pre-post hashes unchanged.

READY_FOR_GHA
