# Luna reply 176: R07 all-seven extension-section census v1

Date: 2026-08-27

## 1. Disposition

Disposition is **PRODUCTION TYPED UNKNOWN_INPUT / FIRST GATE REPAIRED /
RE-SELFTEST PENDING**.  GHA PRODUCTION run `33038109917` at head
`abac045ac8ee38e853c8970c9c2c628ebb64b9fa` terminated normally with typed
`UNKNOWN_INPUT`.  Its three exact terminal lines agree:

```text
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_PRODUCER_TERMINAL R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_INPUT
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_CHECKER_PASS terminal=R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_INPUT
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_GHA_DRIVER_PASS mode=PRODUCTION terminal=R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_INPUT
```

The receipt has SHA-256
`c969abc8a4f38545c40c06491f8a5889ff7b8d4e8825374a4a79a437c4ed3eb7`
and exact reason `CENSUS_REJECT:complete Q0 presentation replay`; the verdict
SHA-256 is
`b78364618b5f9c743bd28160f91678329c7a651bfbb003d19d75cac380eb051a`.
Producer/checker times were 26/0 seconds.  The artifact is at
`%TEMP%\task176_prod_33038109917_a407c4d787784db48a86617fb26b9f20`.
No order or COMPLETE result was emitted.

The first failed gate is diagnosed exactly.  Frozen task176 arithmetic defines
`Perm = bytes`; `old.perm_from_row` converts the 1-based receipt row to 0-based
packed `bytes`, while both `old.perm_one(36)` and `old.eval_perm_word` return
that same type.  The failed gate instead compared the evaluated bytes with
`tuple(range(36))`, so equality was false solely because `bytes != tuple`.
The task157ee helper `p_eval` is a separate 1-based tuple model and is not used
for this gate.  The repair substitutes the canonical `old.perm_one(36)` and
adds an explicit packed-permutation validator to the producer and independent
checker real paths.  Their SELFTESTs accept canonical bytes and reject the
equal-entry tuple through that same validator (`perm_type_checks=2`).

The prior SELFTEST run `33038004295` remains the successful audit of the
preceding bundle, but the new type guard and marker require one bounded
re-SELFTEST before another PRODUCTION dispatch.  No local Python, Node, GAP,
git, GHA dispatch, or production command was run while diagnosing and making
this repair.  The frozen task157ee shelf otherwise contains enough data to
reconstruct both required objects:

- the 1,469,664-state Q0 discovery roster and a deterministic positive
  `x,y` first-seen section, encoded losslessly by one shared parent/letter
  table; and
- all Gamma adjustments, encoded by the reconstructed 243 Gamma states and
  a canonical literal `A_S` element to first Gamma-state-index table for each
  of the eleven families.

The checked-in receipt remains the mandated immutable
`UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD` fixture.  No order is present in it.
Its `GHA_dispatched=false` field describes that immutable fixture, not the
subsequent external SELFTEST and PRODUCTION runs recorded above.

## 2. Final runtime files

```text
bytes  SHA-256                                                           path
46433  6a6c7c46f958d419da53c0fd207208a51db4a0ac7ea0ea50f3078feb6667c5f8  search/d972_r07_all_seven_extension_section_census_v1.py
64237  bd143dedc86e5d012ab51762a2522ed6894b9ab4d7dfbe91695de1dca22c4779  crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py
15372  b3b53ff3ff33a167e2018c8318ab35759334d4d9f3276b0f7a3383eb5e01cfc2  search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g
 4350  b24827b10f8ceb0505802bf7065e2442d176b7b65ecb2066452941c2e7e0a471  search/certs/d972_r07_all_seven_extension_section_census_preflight_v1_20260827.json
```

The fixture has canonical internal self-digest
`880f490c379fd50ebfa553d6d07e0a14263775c26f29a05efab938fe51afe055`.
This is the digest of the body under the actual Python
`json.dumps(sort_keys=True,separators=(",",":"))` canonicalization; the former
invalid value was rejected and removed.  Producer and checker both bind the
fixture's exact 4,350 bytes and external SHA-256, and the driver binds those
values plus the corrected internal digest.

## 3. Producer implementation

The producer authenticates fourteen frozen inputs by exact bytes and SHA-256:
task176; the task157ee producer/checker/driver/task/reply, q3 receipt, and
joint receipt; the frozen E3/E4 arithmetic; proofs v108, v121, v122, and v125;
and the task174 terminal receipt note.  It imports neither task169 nor task175
and does not import or resume task174's direct linked-image BFS.

The production path performs the following fail-closed reconstruction:

1. Reconstruct E3 and E4 from the pinned q3 receipt and replay the 31-row
   registry.
2. Reconstruct the fourth-strand deletion.  The coarse map is the literal
   fourth 36-point block restriction.  The fine map is rebuilt on all 59,049
   Pi4 pc states from the six marked images, with path-consistency and marked
   left-inverse gates.
3. Reconstruct the 243-state task157ee Gamma Cayley graph from the 26 literal
   correction words.  Project it in the exact ordered v125 coordinates
   `[d_E C21,...,d_E C25,C1,C27,C21,C26,C28]`.  Coordinate 0 and coordinate 7
   remain separately typed E3/E4 rows.
4. Rebuild and replay the literal 19-relator complete Q0 presentation, then
   enumerate Q0 exactly once in deterministic positive `x,y` BFS order.
   For each new Q0 state, all ten section values are extended in the same
   discovery step.  No Delta state is enumerated.
5. Construct literal `A_ALL,A_S0,...,A_S9` tables, checking identity, every
   product, every inverse, and normality under the two section generators.
6. Scan the shared Q0 section once for all eleven exact L bitsets.  For every
   L, a greedy literal Q0 generating set is closed exactly; equality with the
   bitset proves closure and inverses, and conjugation of the generators by
   Q0's marked `x,y` proves normality.
7. Apply `|D_S|=|A_S|[Q0:L_S]` with exact divisibility gates, then compute all
   ten `|D_ALL|/|D_Si|` kernel quotients.
8. Emit literal source-word generators for every `Gamma_S^0` and every
   adjusted L lift.  Each emitted word is directly replayed in all ten linked
   coordinates.  A fixed nonidentity literal Gamma twist checks section
   independence on sixteen registered Q0 states.
9. Retain the Q0 roster, parent/letter table, ten literal marked-generator
   images, all A tables and Gamma indices, all eleven L bitsets, word-bearing
   H data, and the singleton image-section decoder.  The decoder represents
   every target seen in the run by its Q0 state and any required A/Gamma
   adjustment; it does not serialize Delta.
10. Compute typed singleton order and equality-pattern tables.  The literal
    subgroup-containment test supports nonfaithful coarse singleton maps by
    retaining all Q0 candidates over a coarse value; it does not assume a
    unique coarse preimage.

The raw persistent section payload is exactly
`1,469,664 * 970 = 1,425,574,080` bytes.  Together with the 52,907,904-byte
Q0 roster, 7,348,320-byte parent/letter data, and eleven L bitsets, the
unboxed fixed-width payload is about 1.386 GiB.  Python dictionaries, pc
caches, subgroup closures, compression, and the temporary equality index
raise the conservative producer/checker peak estimate to 4.5--5.8 GiB.

### First production gate repair: packed Q0 identity

Run `33038109917` stopped before Q0 enumeration at the 19-relator replay.
The relator words and their digest were not contradicted.  The comparison used
two unequal Python container types for the same entries: the frozen evaluator
returned 0-based packed `bytes`, while the literal identity was a tuple.  The
repair now:

1. requires both marked Q0 generators returned by `old.perm_from_row` to be
   canonical packed permutations;
2. obtains the identity from `old.perm_one(36)`;
3. requires every `old.eval_perm_word` result to have the same packed type and
   degree before comparing it with that identity; and
4. mirrors these checks independently in the checker.

`canonical_packed_permutation` uses exact `type(value) is bytes`, degree, and
bijectivity gates.  The producer and checker each call this real-path helper in
a two-case SELFTEST: canonical bytes must pass and `tuple(range(4))` must raise
`Reject`.  This is a representation correction only; no relator, generator,
group law, order, digest, or mathematical acceptance criterion changed.

### Production exception boundary

The receipt-producing `try` now has four deliberately disjoint outcomes:

- normal completion emits `COMPLETE`;
- `ResourceStop` emits `UNKNOWN_RESOURCE`;
- authenticated input absence/parse failures (`InputStop`,
  `FileNotFoundError`, and the specifically named `json.JSONDecodeError`)
  emit `UNKNOWN_INPUT` with nonempty `AUTHENTICATED_INPUT:` reason; and
- the producer's explicit semantic assertion class `Reject` emits
  `UNKNOWN_INPUT` with nonempty `CENSUS_REJECT:` reason.

No catch-all was added.  In particular, generic `TypeError`, `ValueError`,
and `KeyError` leave `run()` and are caught only by the outer command-line
guard, which prints `PRODUCER_STOP` and exits nonzero without manufacturing a
receipt.  Receipt serialization and post-write envelope validation also stay
outside the conversion block, so an implementation or serialization failure
there cannot be mislabeled as input.  `json.JSONDecodeError` remains the one
explicit `ValueError` subclass treated as authenticated-input syntax failure.

## 4. Independent checker and destructive controls

The checker imports neither the producer nor producer helpers.  It loads only
the exact pinned primary E3/E4 arithmetic and independently implements:

- the Gamma group and section graph;
- the exhaustive Pi4-to-Pi3 deletion homomorphism;
- the ten maps and marked images;
- the Q0 BFS, parent/letter section replay, and complete relator replay;
- every A table/group-law gate and every L bitset/subgroup/normality gate;
- every order quotient, Gamma adjustment, source word, and ten-coordinate
  direct replay;
- section twists, image-section decoding, and typed containment/equality
  tables.

The checker selftest uses the same `validate_receipt_chain` dispatcher as a
production receipt.  Its bounded linked fixture is the nonabelian split
extension `1 -> Heisenberg(27) -> Heisenberg(27) x C2 -> C2 -> 1`, with a
literal noncommuting-product witness and full linked image order 54.  The
fixture builder emits production-shaped deletion, Gamma, Q0-section, eleven
`A_S`/`L_S` families, adjusted words, full/singleton orders, quotient, and
roster fields.  The semantic validator does not call the builder or compare
the payload to a frozen whole dictionary.  It independently reconstructs the
Gamma and Q0 sections from their group laws, then checks deletion, every A
literal and exhaustive A closure/inverse/normality, every L bit and
closure/inverse/normality, the shared family-order formula, every Gamma
adjustment and emitted-word replay in all ten coordinates, and the full and
singleton orders/quotients/rosters.

Exactly fifteen resealed semantic mutations are registered.  The baseline and
all mutations enter through `validate_receipt_chain(..., allow_selftest=True)`;
there is no direct mutation-only equality oracle:

```text
typed coordinate 0/7 deduplication; deletion image; Gamma element;
Q0 parent letter; section value; A literal; L membership bit;
L normality witness; Gamma adjustment; emitted source word;
full-family coordinate drop; singleton-label swap; kernel quotient;
canonical roster digest; COMPLETE/UNKNOWN terminal alteration.
```

The receipt self-digest is resealed after each mutation, so digest mismatch is
not the mutation oracle.  Fourteen data mutations are rejected by envelope or
the component-by-component semantic reconstruction; the terminal mutation is
rejected by the same dispatcher's typed terminal/envelope gate.

The checker independently accepts an `UNKNOWN_INPUT` reason only when it has
one of the two registered prefixes and at least one character after the
prefix.  Its selftest now constructs and reseals one componentwise typed
`CENSUS_REJECT:SELFTEST_INVARIANT` receipt, requires the returned terminal and
no-order grade separately, then reseals two reason mutations: a generic
`ValueError:...` label and an empty `CENSUS_REJECT:` prefix.  Both must be
rejected through `validate_receipt_chain`; no whole-dictionary oracle is used.
The current exact checker marker carries both `reject_envelope_checks=3` and
`perm_type_checks=2`, while the original destructive mutation count remains
15/15.  The producer marker independently carries `perm_type_checks=2`.

## 5. Driver and exact terminals

The ASCII-only driver accepts exactly one of these externally bound modes:

```gap
D972_R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_MODE:="SELFTEST";;
D972_R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_MODE:="PRODUCTION";;
```

Unbound or any other string is an error.  It authenticates the producer,
checker, fixture, and fourteen predecessors before creating output.  It
rejects every pre-existing driver-owned artifact, runs one producer and then
one checker strictly serially under Bash `set -euo pipefail`, gates exact-one
markers and terminal agreement, writes artifact hashes and timings, and emits
only a final success sentinel of this exact form (SELFTEST shown):

```text
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_GHA_DRIVER_PASS mode=SELFTEST terminal=SELFTEST
```

For `UNKNOWN_INPUT`, the driver additionally requires exactly one registered
reason prefix (`AUTHENTICATED_INPUT:` or `CENSUS_REJECT:`), rejects either
empty prefixed reason, and requires producer/checker/verdict terminal
agreement.  Its SELFTEST exact-line gate now includes
`reject_envelope_checks=3` and both producer/checker
`perm_type_checks=2` markers.

### GHA formatting failures and repairs

The failure was a lossless-output bug, not a producer, checker, or mathematical
failure.  The pre-repair driver wrote the child Bash script through pathname
`PrintTo`/`AppendTo`, leaving GAP print formatting enabled.  GAP wrapped a long
single-quoted grep expression by inserting its `backslash + newline`
formatting continuation.  Bash preserves that pair inside single quotes, so
grep received a pattern line ending in a backslash and reported
`grep: Trailing backslash`.  The command substitution therefore yielded no
integer; generated shell line 13 reported `test: : integer expression
expected`, `set -e` exited, and the checker and final sentinel were never
reached.

The repaired driver opens one `OutputTextFile`, disables formatting with
`SetPrintFormattingStatus(...,false)`, and sends every child-script fragment
through that stream before closing it.  The two selftest marker gates now use
literal exact-line `grep -Fxc` rather than anchored regular expressions.  A
post-close readback rejects any literal `backslash + newline` continuation
before `Exec`.  Mathematical inputs, the semantic validator, serial order,
timeouts, terminal set, and success sentinel are unchanged.

That repair was confirmed by GHA SELFTEST run `33036920357`: producer,
checker, all fifteen destructive mutations, child-shell sentinel, and workflow
all passed.  The remaining defect was the independent GAP user-console
formatter.  It wrapped the final `Print` as `termin` followed by GAP's visible
continuation and then `al=SELFTEST`.  The workflow did not fail, but the output
was not the contractually required exact one-line sentinel.  The narrow second
repair disables formatting on `OutputTextUser()` immediately before the final
`Print`; it did not touch the now-passing child shell or any semantic code.

GHA SELFTEST run `33037201796` at head `499e4c0a` proved that the second
repair was ineffective: producer and checker again passed exactly, including
all fifteen mutation rejections, but GAP still wrapped the same final line.
The third repair therefore removes GAP from sentinel rendering.  The existing
generated Bash script now has an `--emit-driver-pass` branch.  Only after all
GAP-side producer/checker/log/receipt/verdict audits have succeeded, GAP maps
the closed terminal set to one of four inert codes and invokes that branch.
The branch requires exactly two arguments, accepts only those four codes,
independently composes the mode/terminal line and compares it with a frozen
full expected literal, rejects embedded CR or LF, then emits it with Bash's
builtin `printf '%s\n'`.  Unknown arguments exit before output.  No computed
or receipt-controlled text is interpolated into a shell command.

This output is inherited directly from the external child rather than routed
through GAP's console printer.  The pre-existing post-generation readback
still rejects any literal `backslash + newline` anywhere in the complete
child script before its first execution, so it covers the new emitter branch
as well.  The final emitter is invoked only after the semantic audits, so an
earlier failure cannot print a false PASS.

Run `33038004295` confirmed the pre-identity-fix design: producer PASS, the
expanded Reject-envelope checker PASS, and the exact unwrapped driver PASS
each occurred once.  In
particular, `reject_envelope_checks=3` confirms acceptance of the well-typed
Reject receipt and rejection of both malformed reason mutations through the
independent checker path.  The newly added packed-permutation checks remain
pending one re-SELFTEST.

Production uses a 9,000-second soft producer deadline and 9,600-second outer
timeouts for producer and checker separately.  This leaves 2,400 seconds of
upload/workflow margin inside a six-hour GHA job.  Expected runtime is roughly
45--150 minutes per COMPLETE producer/checker pass; the registered caps, not
that estimate, are authoritative.  An exceeded producer budget is a typed
`UNKNOWN_RESOURCE`, never an order.  A missing required serialization is a
typed `UNKNOWN_INPUT`.

Completed production workflow record:

```text
run_id:       33038109917
head_sha:     abac045ac8ee38e853c8970c9c2c628ebb64b9fa
script:       search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g
out_dir:      ci/out
timeout_min:  360
with_pquot_packages: false
state:        completed typed UNKNOWN_INPUT
reason:       CENSUS_REJECT:complete Q0 presentation replay
```

Required bounded re-SELFTEST preamble for the repaired bundle:

```gap
D972_R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_MODE:=List([83,69,76,70,84,69,83,84],CharInt);;
```

Use the same driver, `out_dir=ci/out`, `timeout_min=60`, and
`with_pquot_packages=false`.  Do not redispatch PRODUCTION until the new
producer/checker markers and the exact one-line driver sentinel all pass.

## 6. Audit, typed production stop, and pending re-SELFTEST

Repair-specific source evidence is fixed at these lines:

- producer lines 113--128 define and selftest the packed-permutation contract,
  lines 628--638 apply it to the real Q0 relator replay, lines 906--918 expose
  the new bounded SELFTEST marker, lines 919--938 preserve the narrow typed
  production conversion, and lines 954--960 retain programming hard STOPs;
- checker lines 30--37 pin the new producer, lines 109--124 independently
  define/selftest the packed-permutation contract, lines 505--518 apply it to
  the real receipt validator, lines 1134--1156 retain the typed Reject-envelope
  tests, and lines 1212--1230 expose all current SELFTEST markers;
- driver lines 26--31 pin the final producer/checker/fixture bytes and hashes,
  lines 112--149 enforce terminal envelopes including the nonempty typed
  `UNKNOWN_INPUT` reason, lines 158--207 perform lossless unformatted shell
  emission, lines 162--176 define the closed exact-sentinel branch, and lines
  208--211 reject a formatting continuation before execution; driver lines
  246--257 map the audited terminal to a closed code and invoke the external
  emitter; and
- fixture lines 41, 44, and 46 bind its typed reason, canonical self-digest,
  and exact terminal.

Only PowerShell read/hash/schema scans were used during this repair.  They
found:

- the downloaded run `33038109917` receipt matches the recorded
  `c969abc8...` SHA-256, typed reason, 26/0-second timing, and all three
  agreeing external terminals;
- all fourteen producer and checker predecessor pins match current exact
  bytes/SHA-256;
- all seventeen driver pins (three runtime files plus fourteen predecessors)
  match;
- checker-to-producer source pin and driver runtime pins agree;
- fixture bytes/external SHA and corrected canonical self-digest agree in the
  producer, checker, driver, and immutable receipt;
- producer, checker, driver, and fixture contain zero non-ASCII bytes and no
  unresolved substitution marker;
- the revised driver contains zero literal `backslash + newline` pairs;
- the repaired relator gates contain no tuple identity and use only the
  canonical packed identity returned by frozen `old.perm_one(36)`;
- the producer's receipt-producing `try` catches `Reject` but not generic
  `TypeError`, `ValueError`, or `KeyError`; those remain in the hard-STOP outer
  guard, while only the explicitly named JSON parser exception is typed input;
- neither task169 nor task175 is imported or named; and
- the GAP driver does not assign or interpret an `Exec` return value.

Run `33036568540` records the first child-shell formatting failure.  Run
`33036920357` establishes producer selftest PASS, checker syntax/import PASS,
all fifteen mutation rejections, and the repaired child shell.  Run
`33037201796` repeats those semantic passes and proves that
`OutputTextUser()` does not suppress the GHA console wrap.  Finally, run
`33038004295` on head `abac045ac8ee38e853c8970c9c2c628ebb64b9fa`
establishes the expanded checker's 15/15 mutations, all three Reject-envelope
checks, and the exact one-line external driver sentinel for that preceding
bundle.  Production run `33038109917` then returns the typed first-gate
`UNKNOWN_INPUT` documented above; producer/checker/driver terminal agreement
and receipt/verdict hashes are complete.  Its failure is not an order or a
nonexistence result.

The canonical packed-identity repair and `perm_type_checks=2` markers are
currently **RE-SELFTEST PENDING**.  Q0 completion, orders, runtime beyond the
first repaired gate, and a COMPLETE receipt remain UNKNOWN until a repaired
bundle passes SELFTEST and is dispatched again.

No all-seven solution, correction word, cofinal lift, fake, or Ihara witness
is claimed.

R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_FIRST_GATE_REPAIRED_RESELFTEST_PENDING
