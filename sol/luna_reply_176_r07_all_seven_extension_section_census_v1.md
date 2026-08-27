# Luna reply 176: R07 all-seven extension-section census v1

Date: 2026-08-27

## 1. Disposition

The five-file bundle requested by task176 has received a narrow driver repair.
Static disposition is **GO for a rerun of the bounded GHA SELFTEST**, followed
by PRODUCTION only if that rerun returns the exact driver sentinel.  GHA run
`33036568540` reached the unchanged producer's exact selftest PASS, but the
pre-repair generated shell then failed before the checker started.  It is not
a complete SELFTEST PASS.  During this repair no local Python, Node, GAP, git,
or GHA command was run.

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
subsequent external SELFTEST attempt recorded above.

## 2. Final runtime files

```text
bytes  SHA-256                                                           path
44757  9fb3839eaf856f6e4d8cc77a2ee358417c6c624564925179d9a62c9e141e2743  search/d972_r07_all_seven_extension_section_census_v1.py
61609  b3b5c305d9e181ef39a192127b815a24b6cb9b86a4a5dccbdb49f793a470d21c  crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py
12839  1ec5e879e95a88c0be8efc74cbd58149bc643274c3ca4245f5ba09664ec39743  search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g
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
only this final success sentinel:

```text
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_GHA_DRIVER_PASS
```

### GHA run 33036568540 failure and repair

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

Production uses a 9,000-second soft producer deadline and 9,600-second outer
timeouts for producer and checker separately.  This leaves 2,400 seconds of
upload/workflow margin inside a six-hour GHA job.  Expected runtime is roughly
45--150 minutes per COMPLETE producer/checker pass; the registered caps, not
that estimate, are authoritative.  An exceeded producer budget is a typed
`UNKNOWN_RESOURCE`, never an order.  A missing required serialization is a
typed `UNKNOWN_INPUT`.

Recommended generic workflow inputs, not dispatched here:

```text
script:       search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g
out_dir:      ci/out
timeout_min:  360
with_pquot_packages: false
```

Run SELFTEST first with the first preamble above.  Dispatch PRODUCTION with the
second preamble only after the exact selftest sentinel appears.

## 6. Static audit and remaining UNKNOWN gates

Repair-specific source evidence is fixed at these lines:

- producer lines 30--31 and 881--886 bind and semantically check the corrected
  immutable fixture;
- checker lines 34 and 37--38 bind producer and fixture identities, lines
  379--391 supply the order-formula gate shared with production, lines
  711--937 define/build the bounded nonabelian extension, and lines 953--1092
  independently reconstruct every advertised component;
- checker lines 1095--1104 dispatch the selftest through the authenticated
  receipt chain, while lines 1107--1151 build, reseal, and submit all fifteen
  mutations to that same entry point;
- driver lines 26--31 pin the final producer/checker/fixture bytes and hashes,
  lines 101--109 bind the corrected internal fixture digest, lines 152--186
  perform lossless unformatted shell emission, and lines 187--190 reject a
  formatting continuation before execution; and
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
- neither task169 nor task175 is imported or named; and
- the GAP driver does not assign or interpret an `Exec` return value.

Run `33036568540` establishes the unchanged producer's selftest PASS and the
pre-repair driver's ability to parse and enter its generated shell.  Because
repair execution was forbidden, the repaired GAP driver parse, checker
syntax/import, fifteen mutation rejections, exact Q0 completion, COMPLETE
orders, runtime, RSS, and artifact size remain **UNKNOWN pending the rerun**.
Static inspection found no remaining deterministic source/pin/schema/contract
STOP, but the repaired bundle must still pass the bounded GHA SELFTEST before
PRODUCTION.

No all-seven solution, correction word, cofinal lift, fake, or Ihara witness
is claimed.

R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_STATIC_GO_REPAIR_UNEXECUTED
