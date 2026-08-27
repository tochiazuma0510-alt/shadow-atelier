# Luna reply 176: R07 all-seven extension-section census v1

Date: 2026-08-27

## 1. Disposition

Disposition is **SELFTEST COMPLETE / PRODUCTION RUNNING**.  GHA SELFTEST run
`33038004295` at head
`abac045ac8ee38e853c8970c9c2c628ebb64b9fa` completed successfully.  In its
`run.log`, each of the three contractual lines occurs exactly once:

```text
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_PRODUCER_SELFTEST_PASS
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_CHECKER_SELFTEST_PASS mutation_attempted=15 mutation_rejected=15 reject_envelope_checks=3 linked_nonabelian_order=54
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_GHA_DRIVER_PASS mode=SELFTEST terminal=SELFTEST
```

The driver line is one physical line with no GAP continuation or newline
fold.  This supersedes the former UNKNOWN status of both coordinated repairs:
the external child-shell `printf` sentinel and the typed Reject-envelope
selftest have now passed their bounded GHA contract.  The downloaded artifact
is at
`%TEMP%\task176_selftest_33038004295_debf6d67540a4ba5b7e24a2c1080c728`.

PRODUCTION run `33038109917` was dispatched from the same head with a
360-minute workflow timeout and is queued at the time of this report.  It has
not yet returned any mathematical terminal, receipt, order, or runtime.  No
local Python, Node, GAP, git, GHA dispatch, or production command was run while
making this report update.

There is no currently identified `UNKNOWN_INPUT` obstruction.  The frozen
task157ee shelf contains enough data to reconstruct both required objects:

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
45282  65feb6a88b95deb990f6bd435775d2af447b838b72cd4bb31b0a56e260cc3524  search/d972_r07_all_seven_extension_section_census_v1.py
63086  f140fadcedba523fcd718cdb6951c75919d59db1988bfc3d64ca199c87464d06  crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py
15296  6a3ad93d4806af470d4e0a51b7a8cf07bfb188020446378a24390ab2612b2122  search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g
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
The exact checker marker therefore adds `reject_envelope_checks=3` while the
original destructive mutation count remains 15/15.

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
`reject_envelope_checks=3`.

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

Run `33038004295` confirms this final design: producer PASS, the expanded
checker PASS, and the exact unwrapped driver PASS each occur once.  In
particular, `reject_envelope_checks=3` confirms acceptance of the well-typed
Reject receipt and rejection of both malformed reason mutations through the
independent checker path.  The bounded SELFTEST gate is therefore complete.

Production uses a 9,000-second soft producer deadline and 9,600-second outer
timeouts for producer and checker separately.  This leaves 2,400 seconds of
upload/workflow margin inside a six-hour GHA job.  Expected runtime is roughly
45--150 minutes per COMPLETE producer/checker pass; the registered caps, not
that estimate, are authoritative.  An exceeded producer budget is a typed
`UNKNOWN_RESOURCE`, never an order.  A missing required serialization is a
typed `UNKNOWN_INPUT`.

Active production workflow record:

```text
run_id:       33038109917
head_sha:     abac045ac8ee38e853c8970c9c2c628ebb64b9fa
script:       search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g
out_dir:      ci/out
timeout_min:  360
with_pquot_packages: false
state:        queued at report time
```

The exact SELFTEST sentinel gate was satisfied before this PRODUCTION dispatch.
No production terminal may be inferred from the queued state.

## 6. Audit, completed SELFTEST, and remaining production gates

Repair-specific source evidence is fixed at these lines:

- producer lines 29--31 register the two nonempty typed input prefixes, lines
  190--224 validate the envelope, lines 884--914 implement the narrow
  production exception conversion, and lines 930--936 retain the outer hard
  STOP for `Reject` outside that block and programming exception classes;
- checker lines 30--37 independently register the prefixes and pin the new
  producer, lines 169--200 validate the envelope componentwise, lines
  1113--1135 exercise the typed Reject terminal and two reason mutations, and
  lines 1138--1182 retain the fifteen production-shaped semantic mutations;
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
checks, and the exact one-line external driver sentinel.  The former SELFTEST
UNKNOWN is superseded: **SELFTEST COMPLETE**.

Production run `33038109917` is **PRODUCTION RUNNING** (queued at this report's
snapshot).  Its exact Q0 completion, terminal, orders, receipt/verdict hashes,
runtime, RSS, and artifact size remain UNKNOWN until that run terminates.

No all-seven solution, correction word, cofinal lift, fake, or Ihara witness
is claimed.

R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_SELFTEST_COMPLETE_PRODUCTION_RUNNING
