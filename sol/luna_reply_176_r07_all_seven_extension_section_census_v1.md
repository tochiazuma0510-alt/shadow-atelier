# Luna reply 176: R07 all-seven extension-section census v1

Date: 2026-08-27

## 1. Disposition

Disposition is **SECOND PRODUCTION TYPED UNKNOWN / NONCONTIGUOUS DELETION
LAYOUT REPAIRED / v135 PROVENANCE PINNED / RE-SELFTEST PENDING**.  GHA
PRODUCTION run `33039406462` at
head prefix `8c75f840` terminated normally with typed `UNKNOWN_INPUT`.  Its
three exact terminal lines agree:

```text
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_PRODUCER_TERMINAL R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_INPUT
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_CHECKER_PASS terminal=R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_INPUT
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_GHA_DRIVER_PASS mode=PRODUCTION terminal=R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_INPUT
```

The receipt has SHA-256
`3e519e36fd8e2096eea784b38cf1ee25b678a0a8a55e0c76b22316c5d9ebce79`
and exact reason `CENSUS_REJECT:coarse marked fourth-strand deletion`; the
verdict SHA-256 is
`6be410d2c82e1e449001c211d5588c4e730ee37a43c92fb60248a75c8cc4eb7a`.
Producer/checker times were 25/0 seconds.  The downloaded artifact is at
`%TEMP%\task176_prod_33039406462\gap-run-out`.  No order or COMPLETE result
was emitted.

The stop is now diagnosed exactly.  Frozen Q4 does not consist of four
contiguous 36-point Q0 blocks.  Its point layout is
`P1,P2,P3,P4` on `[0,36)` in four 9-point blocks, followed by
`G9_1,G9_2,G9_3,G9_4` on `[36,144)` in four 27-point blocks.  V122 Section 2
and the predecessor checker therefore require the fourth-strand projection

```text
Q0[0:9]  = Q4[27:36]  - 27
Q0[9:36] = Q4[117:144] - 108
```

The failed implementation instead used `Q4[108:144]-108`, mixing the last
nine points of `G9_3` with all of `G9_4` and omitting `P4`.  This is the
implementation erratum isolated in paper note v135; it does not change v122's
abstract deletion theorem.  Static replay of the authenticated q3 rows shows
that the corrected noncontiguous projection sends the six PB4 marked rows
literally, with no inversion, strand permutation, or conjugation, to
`(X,Z,1,Y,1,1)`, `Z=(YX)^-1`.

The producer and independently written checker now each implement that exact
two-slice projection, require invariance of both source blocks, and retain a
typed, lossless six-row diagnostic: actual and expected 36-byte hex, both
SHA-256 values, zero-based first differing index, literal-equality flag, and
whether conjugation is required.  The current rows all have null first
difference and `conjugation_required=false`; acceptance still derives the
expected rows from the proved E3 marked images rather than copying actual into
expected.  `deletion_convention_checks=10` rejects cross-factor invariance,
contiguous-suffix, wrong-P-block, wrong-G9-block, output-offset, orientation,
and independently resealed diagnostic-field mutations.

The earlier representation repairs remain in force.  `coarse_delete` requires
a canonical 144-byte permutation and returns canonical 36-byte packed bytes;
full E4 inputs, E3 outputs, and E3 targets pass a
`tuple[bytes,bytes]` validator with exact PC width.  `deleter_type_checks=6`
covers the two positive paths and four semantic type mutations.  Generic
programming exceptions remain hard STOPs and are not converted to typed input.

SELFTEST run `33038764764` at head `56fbbc7b` succeeded at `04:14:40Z`, but it
contains only the earlier Q0-relator canonical-bytes repair.  It is recorded as
a **superseded intermediate SELFTEST**, not authorization for PRODUCTION.  The
  current noncontiguous deleter and new marker require another bounded SELFTEST.  No
local Python, Node, GAP, git, GHA dispatch, or production command was run while
making this repair.  The frozen task157ee shelf otherwise contains enough data
to reconstruct both required objects:

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
60643  304929fdd83e313864b8126457bcec4f59c8e597f2e2fdf8428793ada0c6ea99  search/d972_r07_all_seven_extension_section_census_v1.py
80637  b31af78d66b9d15926c2bc0223e7ae38c4c20dc018d8d4e3d915ddd4506cf538  crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py
15717  d8104835c1b156fcbf8ee3678aa86125e59be580b5bd4fe68e0a041cdd4c26cd  search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g
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

The producer authenticates fourteen fixture-public frozen inputs by exact bytes
and SHA-256: task176; the task157ee producer/checker/driver/task/reply, q3
receipt, and joint receipt; the frozen E3/E4 arithmetic; proofs v108, v121,
v122, and v125; and the task174 terminal receipt note.  It separately
authenticates the governing v135 note at exact path
`sol/proof_r07_q4_q0_noncontiguous_deletion_layout_v135.md`, 4,539 bytes, and
SHA-256
`75c511a765ad88ec1aa72c63a0d1965ac85724695d743cbf00350572a884cf67`.
The COMPLETE receipt retains that full path/bytes/SHA triple under
`proof_pins.v135`, and the independently written checker requires exact field
equality after authenticating v135 itself.  V135 remains separate from the
immutable fixture's original public pin ledger, so no fixture bytes or semantics
changed.  The producer imports neither task169 nor task175 and does not import
or resume task174's direct linked-image BFS.

The production path performs the following fail-closed reconstruction:

1. Reconstruct E3 and E4 from the pinned q3 receipt and replay the 31-row
   registry.
2. Reconstruct the fourth-strand deletion.  The coarse map is the literal
   noncontiguous fourth `P` and fourth `G9` block restriction
   `[27,36)+[117,144) -> [0,9)+[9,36)`.  The fine map is rebuilt on all 59,049
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
    unique coarse preimage.  While each existing `coarse_to_q` table is live,
    retain its exact raw-key distinct count, min/max multiplicity, complete
    multiplicity histogram and two streaming digests without serializing the
    full map.
11. Replay the coarse part of all 243 Gamma states in every coordinate.  The
    acceptance vector for `|C_i|=|coarse(Phi_i(Gamma))|` is
    `(1,1,1,1,1,81,81,81,9,9)`; each row retains the image and kernel orders,
    state-sequence and canonical-roster digests, and independent
    identity/inverse/closure checks.

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

### Complete `make_deleter` representation boundary

The function-local inventory before repair was:

```text
boundary                         old representation                 canonical representation
q0_marked[0], q0_marked[1]       bytes                              bytes
e3.generators[*][0]              bytes                              bytes
coarse_delete(...)               tuple[int,...]                     bytes
coarse identity slots            tuple(range(36))                   old.perm_one(36): bytes
fine[pc_key]                     bytes                              bytes
producer delete PC result        tuple(fine[pc_key])                bytes
E3/E4 full element               tuple[bytes,bytes]                 tuple[bytes,bytes]
```

Thus the old coarse list comparison necessarily mixed types in slots 1, 2,
and 4, and the producer's later full-element comparison also mixed the PC
component.  After repair, `coarse_delete` rejects non-bytes input and returns
bytes, all six expected/actual coarse entries are bytes, and every full source,
image, and target is checked as an outer tuple with packed bytes components.
The checker's independently written `reconstruct_deletion` enforces the same
boundary.  All `tuple(range(36))` occurrences remaining near these functions
are deliberate negative SELFTEST mutations; production deletion paths contain
zero tuple/bytes representation mixtures.

### Noncontiguous factor layout and six marked rows

The independently traced frozen layout is:

```text
factor     source half-open interval       target half-open interval   rebase
P4         [27,36)                         [0,9)                        -27
G9_4       [117,144)                       [9,36)                       -108
```

The old contiguous selector and corrected literal factor selector have these
static 36-byte SHA-256 diagnostics on the six authenticated q3 marked rows:

```text
PB4 row  target       old [108,144) SHA-256                                      old first diff  corrected/expected SHA-256                               corrected first diff
A12      X            e99e7d70065da9dc2d444d51f023146d761c4db9f7c18535794f4f480b20ecdd  0               647c45371928ff0fde51bac8e728a4d66015ab465ae7141c076c81cbfed17e3e  null
A13      Z=(YX)^-1    e09e2526271724f6b64d9d02ab574c6b8b1e4c5d40b9ffa5bcd6f05ed09197d5  0               dd117176a000c267ad2e262cfbcfa092706ac441fa73022819df2f26bbb8648f  null
A14      1            e5ed95ec4ad8905efb32ad84d748bf6926cab3ac3e3e854c892ffede4caba0bf  0               5d7e2d9b1dcbc85e7c890036a2cf2f9fe7b66554f2df08cec6aa9c0a25c99c21  null
A23      Y            8447ec1e2801bae1657abe33e80416b6260d30dfbf9a22276fd13d738172ad61  0               46bbd2639dc02af5be2b98702b940fd86d80770855de5780e214e7bfda83b8a9  null
A24      1            052dd5e1f266f6a54fee7412577bde3cab0b2790a8123a47756d3350860e2c37  0               5d7e2d9b1dcbc85e7c890036a2cf2f9fe7b66554f2df08cec6aa9c0a25c99c21  null
A34      1            5d7e2d9b1dcbc85e7c890036a2cf2f9fe7b66554f2df08cec6aa9c0a25c99c21  null            5d7e2d9b1dcbc85e7c890036a2cf2f9fe7b66554f2df08cec6aa9c0a25c99c21  null
```

Thus five old rows fail immediately at byte 0 and only the final identity row
matches accidentally.  The corrected rows are byte-for-byte equal to their
proved targets, so no conjugacy search is needed or used.  The receipt keeps
both full 72-hex-character rows, not only these displayed digests; the checker
reconstructs every scalar and every row field componentwise before its existing
whole deletion-receipt equality gate.

### Gamma coarse images and bucket boundary

The previous statement that Gamma was coarse-trivial in every selected
coordinate was false.  The repaired producer now replays all 243 literal Gamma
states and gates the candidate coarse-image orders

```text
(|C_0|,...,|C_9|) = (1,1,1,1,1,81,81,81,9,9).
```

The checker independently rebuilds the same 243-state group and verifies the
ten orders, kernel divisibility, identity, all inverses, all products, the
state-major coarse-image digest, and the sorted image-roster digest.  These
numbers remain pending GHA replay; they are an acceptance contract, not a
completed production result in this reply.

The newly retained `raw_section_coarse_key_bucket_statistics` are explicitly
typed as literal coarse-key equality, not `C_i`-coset equivalence.  They include
per coordinate the distinct raw coarse-key count, bucket min/max, full
multiplicity histogram and histogram digest, plus a streaming digest over
`(key width,key bytes,bucket size)` in first-seen Q0 order.  This adds one
streaming pass over each already-live dictionary and no full-map artifact.

For a uniform partial-target membership oracle the correct thick bucket is the
left coset `C_i*b_i(q)`, with necessary test
`c_i(t_i)*b_i(q)^-1 in C_i`.  Computing all ten nontrivial-coset histograms
would add a new coset-canonicalization pass beyond the current repair, so it is
deferred rather than hidden inside the production-gate fix.  A future oracle
must also intersect full residuals using one common Gamma state; choosing a
different Gamma state independently in each coordinate is forbidden.

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
The current exact checker marker carries `reject_envelope_checks=3`,
`perm_type_checks=2`, `joint_blob_type_checks=8`, `deleter_type_checks=6`, and
`deletion_convention_checks=10`, while the original destructive mutation count
remains 15/15.  The producer marker independently carries all four bounded
check counts.  On COMPLETE input the checker also reconstructs each six-row
deletion diagnostic field, all ten raw bucket-statistic fields, and all ten
Gamma coarse-image records rather than trusting producer summaries.

## 5. Driver and exact terminals

The ASCII-only driver accepts exactly one of these externally bound modes:

```gap
D972_R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_MODE:="SELFTEST";;
D972_R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_MODE:="PRODUCTION";;
```

Unbound or any other string is an error.  It authenticates the producer,
checker, fixture, and fifteen predecessors, including v135, before creating
output.  It
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
`perm_type_checks=2`, `joint_blob_type_checks=8`, `deleter_type_checks=6`, and
`deletion_convention_checks=10` markers.

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
independent checker path.  Run `33038764764` later confirmed the packed-Q0
identity checks, but predates `deleter_type_checks=6` and is therefore only an
intermediate success.  Run `33039406462` subsequently passed those
representation gates and exposed the distinct noncontiguous-layout defect.
The current factor-layout formula and `deletion_convention_checks=10` remain
pending one re-SELFTEST.

Production uses a 9,000-second soft producer deadline and 9,600-second outer
timeouts for producer and checker separately.  This leaves 2,400 seconds of
upload/workflow margin inside a six-hour GHA job.  Expected runtime is roughly
45--150 minutes per COMPLETE producer/checker pass; the registered caps, not
that estimate, are authoritative.  An exceeded producer budget is a typed
`UNKNOWN_RESOURCE`, never an order.  A missing required serialization is a
typed `UNKNOWN_INPUT`.

First completed production workflow record:

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

Previous completed production workflow record:

```text
run_id:       33039406462
head_prefix:  8c75f840
script:       search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g
out_dir:      ci/out
timeout_min:  360
with_pquot_packages: false
state:        completed typed UNKNOWN_INPUT
reason:       CENSUS_REJECT:coarse marked fourth-strand deletion
receipt_sha:  3e519e36fd8e2096eea784b38cf1ee25b678a0a8a55e0c76b22316c5d9ebce79
verdict_sha:  6be410d2c82e1e449001c211d5588c4e730ee37a43c92fb60248a75c8cc4eb7a
timing:       producer 25 seconds / checker 0 seconds
```

Latest completed production workflow record:

```text
run_id:       33041705078
head_prefix:  a84a3947
script:       search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g
out_dir:      ci/out
timeout_min:  360
with_pquot_packages: false
state:        completed hard STOP after 33 seconds
stderr:       R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_PRODUCER_STOP can only concatenate tuple (not "bytes") to tuple
receipt:      none
artifact:     none
checker:      not run
driver_pass:  absent
```

Required bounded re-SELFTEST preamble for the repaired bundle:

```gap
D972_R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_MODE:=List([83,69,76,70,84,69,83,84],CharInt);;
```

Use the same driver, `out_dir=ci/out`, `timeout_min=60`, and
`with_pquot_packages=false`.  Do not redispatch PRODUCTION until the new
producer/checker markers and the exact one-line driver sentinel all pass:

```text
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_PRODUCER_SELFTEST_PASS perm_type_checks=2 joint_blob_type_checks=8 deleter_type_checks=6 deletion_convention_checks=10
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_CHECKER_SELFTEST_PASS mutation_attempted=15 mutation_rejected=15 reject_envelope_checks=3 perm_type_checks=2 joint_blob_type_checks=8 deleter_type_checks=6 deletion_convention_checks=10 linked_nonabelian_order=54
R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_GHA_DRIVER_PASS mode=SELFTEST terminal=SELFTEST
```

## 6. Audit, typed production stop, and pending re-SELFTEST

Repair-specific source evidence is fixed at these lines:

- producer lines 95--96 and 180--190 define/authenticate the exact v135 pin;
  lines 116--142 define packed permutation/EKey contracts; lines 342--509
  implement, diagnose, and mutation-test the noncontiguous deletion; lines
  510--555 stream raw coarse-key bucket statistics; lines 782--822 replay all
  ten Gamma coarse images; line 929 retains the repaired Q0 relator replay;
  lines 1176--1178 retain v135 in COMPLETE `proof_pins`; and lines 1205--1268
  preserve bounded SELFTEST, narrow typed receipt conversion, and programming
  hard STOPs;
- checker line 38 pins the new producer; lines 99--100 and 159--175 independently
  define/authenticate the exact v135 pin; lines 112--139 independently define
  packed permutation/EKey contracts; lines 263--546 independently implement,
  validate field-by-field, and mutation-test deletion; lines 354--397 and
  608--649 rebuild raw bucket and Gamma coarse-image statistics; lines
  714--1063 perform the COMPLETE semantic replay, including exact v135 receipt
  equality at lines 1056--1060; and lines 1540 onward expose bounded SELFTEST
  and production verdict paths;
- driver lines 26--31 pin the final producer/checker/fixture bytes and hashes,
  line 50 pins v135, lines 113--150 enforce terminal envelopes including the
  nonempty typed `UNKNOWN_INPUT` reason, lines 159--208 perform lossless
  unformatted shell emission, lines 163--177 define the closed exact-sentinel
  branch, and lines 209--211 reject a formatting continuation before execution;
  driver lines 247--258 map the audited terminal to a closed code and invoke the
  external emitter; and
- fixture lines 41, 44, and 46 bind its typed reason, canonical self-digest,
  and exact terminal.

Only PowerShell read/hash/schema scans were used during this repair.  They
found:

- the downloaded run `33039406462` receipt and verdict match the full
  `3e519e36...` / `6be410d2...` SHA-256 values above, exact typed reason,
  25/0-second timing, and all three agreeing external terminals;
- the earlier run `33038109917` artifact still matches its recorded
  `c969abc8...` receipt, Q0-relator reason, 26/0-second timing, and agreeing
  terminals;
- all fifteen governing producer/checker source pins (fourteen fixture-public
  predecessors plus the separately authenticated v135 note) match current exact
  bytes/SHA-256;
- all eighteen driver pins (three runtime files plus fifteen predecessors)
  match;
- checker-to-producer source pin and driver runtime pins agree;
- fixture bytes/external SHA and corrected canonical self-digest agree in the
  producer, checker, driver, and immutable receipt;
- producer, checker, driver, and fixture contain zero non-ASCII bytes and no
  unresolved substitution marker;
- the revised driver contains zero literal `backslash + newline` pairs;
- the repaired relator gates contain no tuple identity and use only the
  canonical packed identity returned by frozen `old.perm_one(36)`;
- the producer/checker deletion production paths contain zero
  `tuple(range(36))`, tuple permutation outputs, or tuple PC outputs; all such
  remaining nearby tuple literals occur only in negative SELFTEST mutations;
- the only remaining `[108:144]` deletion selector is an explicit rejected
  contiguous-suffix SELFTEST; production uses exactly `[27:36]` and
  `[117:144]` with rebases 27 and 108;
- static replay of all six authenticated q3 marked rows gives literal
  corrected equality, five old-selector first differences at byte 0, one
  accidental identity equality, and no required conjugation;
- raw-key bucket statistics are explicitly distinguished from the deferred
  `C_i` thick-coset statistics, and the Gamma coarse-order vector is bound as a
  pending all-243-state replay rather than reported as a completed result;
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
nonexistence result.  Intermediate SELFTEST run `33038764764` at head
`56fbbc7b` subsequently passes the Q0-relator identity repair at `04:14:40Z`,
but predates the complete deleter boundary repair and is superseded for
production promotion.  Production run `33039406462` passes those earlier
representation gates and returns the separately typed coarse-layout stop with
matching producer/checker/driver terminals and the exact hashes above.

Production run `33041705078` at head prefix `a84a3947` then crossed the
authenticated driver gates but stopped after 33 seconds with the exact
tuple-plus-bytes `TypeError` recorded above.  Because this is a programming
exception, no receipt was written, the checker did not run, no artifact was
uploaded, and no driver PASS appeared.  It is neither typed UNKNOWN evidence
nor a mathematical result.

The later SELFTEST attempt `33041044008` was canceled when the independent
audit found that v135 governed the repaired selector but was cited only in this
reply, not authenticated by the runtime bundle.  It supplies no terminal or
promotion evidence.  The narrow repair now exact-pins v135 in producer,
checker, driver, and COMPLETE receipt semantics, but no replacement SELFTEST
has yet run against the final identities in Section 2.

The noncontiguous factor projection, six-row diagnostic,
`deletion_convention_checks=10`, raw bucket summaries, and all-243 Gamma
coarse-image replay, together with the new `joint_blob_type_checks=8`, are
currently **RE-SELFTEST PENDING**.  Q0 completion,
orders, runtime beyond the deletion gate, and a COMPLETE receipt remain UNKNOWN
until the current bundle passes SELFTEST and is dispatched again.

No all-seven solution, correction word, cofinal lift, fake, or Ihara witness
is claimed.

## 7. Run 33041705078 tuple/bytes hard-STOP repair

The failing expression is uniquely identified in the authenticated frozen
arithmetic source at
`search/d972_b345_seedspan_triple4_v1.py:2797`:

```python
return value[0] + value[1]
```

The pre-repair task176 `blob(old, value)` delegated directly to that expression.
For a live product value `(tuple permutation, bytes PC)`, Python evaluates
`tuple + bytes` before task176's outer `bytes(...)` can canonicalize anything,
which yields exactly the run's error text.  The pinned task157ee `JointGroup`
also delegates its key serializer to the same frozen helper, so repairing only
the local call would have left a second route to the identical stop.

The producer now owns one narrow serializer boundary.  It accepts exactly a
two-component tuple whose permutation is either canonical packed bytes or the
documented zero-based integer tuple returned by product arithmetic, requires a
packed-bytes PC component, fixes the only live dimensions to `(36,4)` and
`(144,10)`, checks permutation bijectivity, and returns
`bytes(permutation) + pc_bytes`.  Every local blob path, including reconstructed
section products, uses it.  A tiny `PackedJointGroup` subclass overrides only
the imported class's serializer, so its construction, transition table,
group law, section words, v135 deletion, Gamma replay, and bucket mathematics
remain unchanged while the frozen broken concatenation is no longer called.

The checker implements the same accepted mathematical representations through
separate code and never calls the producer helper.  Each SELFTEST exercises the
formerly failing exact `(tuple(range(36)), bytes(4))` case with a deliberately
poisoned legacy helper, the original packed-bytes case, and six independent
malformations: outer list, permutation list, tuple PC, wrong degree, wrong PC
width, and non-bijection.  The exact producer/checker/driver gates therefore
bind `joint_blob_type_checks=8`.

This compatibility adapter does not convert programming failures to a typed
receipt.  Its malformed representation gates raise only `TypeError` or
`ValueError`; the production receipt-producing `try` still does not catch
either class.  They reach the existing outer STOP and exit nonzero without a
receipt, exactly as run `33041705078` did.  Only the pre-existing semantic
`Reject`, resource stop, and named authenticated-input exceptions retain their
typed envelopes.

Static final runtime identities before this reply's own final hash are:

```text
search/d972_r07_all_seven_extension_section_census_v1.py
  bytes 63872
  sha256 5cf5617bebc932833dd34105bd85b2536e8c332137dce0f6ea176ebd82e09bd3
crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py
  bytes 82983
  sha256 892b9b2e086acf2dc9cb69e01b8c5ebb579050ae1622dd2ed4b66c83887a69a8
search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g
  bytes 15817
  sha256 9d854d02b1c8c1fdcdda5855f16a85b1d8f51998c6a9a4a660c0313138a9839f
```

No local Python, GAP, Node, GHA, or git command was run.  Production was not
redispatched.  The required next action is the bounded SELFTEST preamble in
Section 5, followed by PRODUCTION only after both new exact markers and the
one-line external driver sentinel pass.

R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_TUPLE_BYTES_SERIALIZER_REPAIRED_RESELFTEST_PENDING
