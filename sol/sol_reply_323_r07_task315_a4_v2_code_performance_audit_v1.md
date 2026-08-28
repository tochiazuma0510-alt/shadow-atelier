# Sol(max) reply 323 — task315 A4/v2 code/performance audit

## Verdict

**REJECT / UNEXECUTED.  Do not dispatch either SELFTEST or production with
this bundle.**

The first load-bearing implementation blocker is not a performance
uncertainty: after the intended manifest gate, the producer unconditionally
raises `LOCAL_AUTHENTICATED_EVALUATOR_NOT_STAGED` at producer line 2063, and
the checker unconditionally raises `checker positive runtime deferred to
independent audit` at checker line 1552.  The code following the producer
raise does not call `build_kernel` or `evaluate_k_z`; it merely constructs a
shaped positive dictionary.  Thus a manifest-pin refresh alone cannot make
actual A4 reachable.

There are earlier deterministic failures too.  With the newly staged actual
receipt and only `ACCEPTED_MANIFEST_SHA256` refreshed, producer line 1493
first rejects `Gamma_Cayley_state_count`: the receipt spells the authenticated
field `Gamma_cayley_state_count`.  The code also expects
`Q0_defect_normal_closure_order=1469664`, whereas the accepted receipt has the
correct Gamma normal-closure order `243`.  SELFTEST itself reaches an
undefined `ToyRuntime.boundary_records` at producer line 963 on the first
boundary-bearing query.  None of these conclusions required execution.

Only read-only PowerShell byte/hash/text inspection was used.  Python, Node,
GAP, GHA, workflows, network, and git were not run.  Producer, checker,
SELFTEST, and production all remain unexecuted.

## 1. Exact v2 identities and driver

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v2.py` | 108,706 | `02455b61f400076133cdee7b692a3e96a64b5400f6d97ad69a0ffa660f7baa4d` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v2.py` | 82,533 | `44b2a632a8292854d499287527faf3f7e8b8eafee0348bb90a31d6324ec47ffd` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v2.g` | 5,013 | `fc612ff036593400b3f3748c2327ce7bde4b1146cd1228f11473943835abb2de` |
| `search/certs/d972_r07_word_independent_successor_kernel_selftest_v2_20260828.json` | 1,070 | `0a7d94678bb0fa933469938a2953cde396a30a77a1aa43ae6544ba3cf57788aa` |

These identities agree with the Luna reply and the three driver pins.  The
driver is ASCII-only.  In either mutually exclusive mode it emits exactly
one producer command and exactly one checker command.  It rejects all five
stale output/log/script paths, requires a nonempty producer receipt, consumes
the exact-one full-line producer and checker counts, compares the two
terminals, and checks the one-line final `.ok` sentinel.

The driver gate is nevertheless incomplete:

1. there is no checker verdict path at all—only a checker log—so no nonempty,
   sealed independent verdict is produced or checked;
2. the newly staged acceptance manifest is not pinned by the driver; and
3. an exact-one log line is not a replacement for the commissioned sealed
   checker verdict.

The post-gate `.ok` check is sound as far as it goes.  The missing verdict is
independently sufficient to fail the Section 2 driver contract.

## 2. Exact execution boundary

The current producer route does fail closed before reading authority bytes:

```text
ACCEPTED_MANIFEST_SHA256 = None                 producer 124
raise StaticBlocked(STATIC_BLOCKED)             producer 1594--1595
STATIC_BLOCKED envelope                         producer 2044--2047
```

That envelope has `status == terminal ==
STATIC_BLOCKED:TASK198_AUTHORITY_NOT_STAGED`, all three A4 milestones zero,
all downstream flags including lift/fake/Ihara false, and meter state
`RANK_ZERO_RESTART`.  The checker accepts only that sealed nonpositive shape
and returns the same terminal.  This establishes only the current static
stop, not A4.

The ordered post-pin stops on the actual staged object are:

1. wrong normal-generation field names/value at producer 1483--1504;
2. a nonmatching bridge occurrence ledger at producer 1511--1520 (the real
   ledger contains load-bearing `block_index` and `block_slot`, omitted from
   `expected_bridge_ledger`);
3. the unconditional producer evaluator stop at 2063;
4. no producer positive computation after that stop—the following result is
   shaped, not computed;
5. the checker's analogous normal-proof and occurrence-ledger mismatches at
   1423--1478; and
6. the unconditional checker positive-replay stop at 1552.

Accordingly, neither the already staged manifest nor a later constant refresh
is sufficient.  An authenticated local successor evaluator, the actual
6,441-defect closure, the anchor, and an actual independent positive replay
are all absent from the production branch.

## 3. Authority and path semantics in v2

### What was repaired

The producer enforces the exact three contiguous layer blocks and local
ordinals `1..6318`, `1..104`, and `1..19`.  It computes the whole-row digest
and seven chunks, checks canonical receipt bytes and a receipt self-seal, and
uses exact registered lexical basenames for all four authority inputs.
Both implementations reject absolute paths, `.`/`..`, and resolved escape
outside `ci/in`; output paths receive the analogous `ci/out` containment
check.  No checkpoint/resume implementation is advertised.

### Remaining failures

- The producer's only exact acceptance anchor is the `None` constant.  The
  checker has no accepted-manifest SHA pin at all; it accepts a structurally
  self-consistent manifest with nonempty run/artifact fields.
- The manifest schema binds terminal-line hashes but has no checker-verdict
  member/digest and no `accepted=true` or `independent=true` field.
- The producer's normal-generation constants do not match the actual accepted
  task198 schema, as detailed above.  The checker repeats the same wrong
  capitalization and order value.
- The producer's expected occurrence objects omit the real `block_index` and
  `block_slot`; the checker does the same.  Thus the exact accepted ledger is
  rejected rather than replayed.
- `_validate_evaluator` preserves whatever `callable` string the input
  supplied when forming its comparison at producer 1560--1563.  It checks
  canaries only for dictionary type, not their exact values or the group-law
  replays.  The checker checks only widths, row digest, and counts of entries
  and canaries at 1485--1490.
- Resolving a registered top-level symlink to an in-tree nested object with
  the same basename is not rejected: the code checks containment and final
  basename, not equality with the resolved registered top-level path.  The
  outside-tree escape case is correctly rejected, but the full exact anti-
  alias contract is not met.
- The SELFTEST authority mutations alter a separate shallow dictionary; they
  never invoke the production canonical-byte, resolved-path, roster, normal-
  proof, bridge, or evaluator validators.

Therefore `authority/path semantics` is **FAIL** even apart from the
intentional current static block.

## 4. Lightweight runtime and exact mathematics

### Full-space exclusion

There is no import or callable path to `p179.build_runtime`, task176
`enumerate_q0_sections`, `scan_memberships`, `prove_L`, the 1,469,664-state
Q0 universe, its 2,939,328 edges, a raw section store, or a second task175
roster.  `FULL Q0 / GLOBAL ROSTER RECONSTRUCTION: ABSENT` is a correct static
statement.

It is, however, vacuous as an implementation claim.  `PackedPBCodec` accepts
an ad-hoc lookup table that the accepted evaluator ABI does not supply, and
otherwise permits only the synthetic coordinate-wise law.  The only wired
runtimes are `ToyRuntime` and `IndependentRuntime`, both synthetic.  No actual
PB3/PB4 codec, ten actual substitutions, forty actual cached actors, boundary
source, or task198-row evaluator is connected to production.  The checker
never reconstructs the actual 6,441 defects; its positive branch stops before
any such work.

### Echelon and coefficient failures

The source contains one persistent total echelon and one boundary echelon per
toy implementation, so the v1 rebuild-per-query architecture was partly
removed.  The coefficient certificate is still not correct in general.

1. `add_boundary` first reduces a raw boundary and then calls `insert`, which
   reduces it a second time.  The returned ancestry represents the
   pivot-normalized remainder, but lines 801--802 require it to replay the
   unnormalized raw row.  Any nontrivial prior reduction or pivot scale two
   makes this false.  Checker lines 488--499 repeat the same defect.
2. Producer nonmember lines 850--860 export `+scale*old_coefficients` as the
   ancestry without the new label.  Since
   `normalized = scale*(candidate-old_coefficients*raw_rows)`, the sign must
   be negative.  The build path later recomputes a different, correct sign,
   leaving the exported membership map itself false.
3. `K:i` raw labels denote the unreduced candidate, while `basis[i].row`
   denotes its pivot-normalized remainder.  Action columns are computed in
   raw-candidate coordinates but are composed as though their indices were
   the normalized stored basis.  After a rank raise with a prior-K component,
   the advertised identity/inverse matrix equations are in different bases.
4. Producer alternate-basis records are not independently replayed.  The
   checker checks their `replay` Booleans, then constructs different maps.
5. Checker line 1270 calls `change_map(independent["basis"], ...)`, passing
   complete basis-record dictionaries rather than their sparse `row` values.
   `mod3_row` then attempts integer conversion of strings/dictionaries.  This
   is a deterministic SELFTEST failure even if earlier failures are repaired.
6. The checker replays only positive producer membership maps.  It does not
   independently replay normalization, all-row annihilation, and target
   pairing for every initial and translated NONMEMBER receipt.  Its one
   special negative target `{"9:9:ff":1}` is outside the authenticated blob
   widths and proves nonmembership only in an artificially enlarged key
   universe.

Thus the claimed stable raw `B:`/`K:` proof, independent change of basis, and
two-way span certificate are **FAIL**.

### Word ancestry and v247 failures

The outer-first/reversed convention and the displayed depth-two canary are
explicit, but the load-bearing ancestry is not constructed.

- Initial line 1107 passes string labels such as `K:0` where `AncestryDAG.linear`
  requires integer DAG node indices.  The first accepted row whose reduction
  has an old K coefficient therefore fails integer conversion.
- A translated rank raise stores only the conjugate of the parent's source
  word and only the action of the parent's vector node.  It omits the
  normalization scale and all old-K correction words required by
  `scale*(moved-old)`.  Consequently the direct word need not equal the new
  basis row modulo boundary only.
- Initial rows likewise retain the unscaled original source word even when
  the accepted basis row is a scaled/corrected remainder.  The boundary-only
  receipt can succeed only in special triangular cases.
- DAG evaluation recursively expands shared children without memoization;
  persistent storage does not prevent repeated expanded work.
- The direct cube/commutator replay in the wired runtimes is only an H2(9)
  quotient test, not equality in the actual first successor.  The actual
  group product/identity ABI is not wired.
- The v247 functions have the right formal least-index/inverse-scalar shape,
  but they run on the incorrectly bound source words and are never reached in
  production.  The checker has no actual positive anchor replay.

Persistent-DAG shape, conjugator convention, and H2 formula are partial
repairs; the commissioned word-bearing A4 mathematics is not implemented.

## 5. All twenty mutation owners

Every mutation is caught through a broad tuple
`(RuntimeError, KeyError, IndexError, StopIteration)` without requiring the
expected gate or message.  The following is the actual owner trace.

| # | mutation | actual rejection path | ruling |
|---:|---|---|---|
| 1 | `per_layer_ordinal` | shallow `authority.ordinal_roster` exact-dictionary comparison | wrong owner; never calls the 6,441-row roster gate |
| 2 | `authority_binding` | shallow basename comparison | wrong owner; no run/head/artifact/member manifest replay |
| 3 | `canonical_input_bytes` | flips a Boolean named `canonical_bytes` | wrong owner; no byte canonicalization |
| 4 | `resolved_path_traversal` | changes a stored string rejected by dictionary equality | wrong owner; no `safe_path`/resolution call |
| 5 | `normal_generation_proof` | flips `normal_generation_exact` | wrong owner; no proof-field replay |
| 6 | `bridge_typed_occurrence_ledger` | mutates the ledger without resealing its digest | wrong-seal/summary rejection, not the actual bridge owner |
| 7 | `evaluator_abi_canary` | changes a synthetic digest string | wrong owner; no callable/canary evaluation |
| 8 | `raw_boundary_coefficient` | first-row literal equality catches it | no raw coefficient-map replay owner |
| 9 | `live_echelon_inherited_scale` | hard-coded first-basis dictionary catches it | no echelon row-operation owner |
| 10 | `producer_checker_basis_change` | flips a `replay` Boolean | producer map is not reconstructed |
| 11 | `conjugator_order` | changes the canary's convention string | no mutated literal conjugation replay |
| 12 | `source_word_basis_boundary_difference` | flips a boundary `replay` Boolean | no direct word/boundary sum mutation |
| 13 | `negative_dual` | sets the recorded pairing to zero | no dual recomputation from mutated rows |
| 14 | `action_matrix` | empties a matrix and fails shape | no independently changed action owner |
| 15 | `projected_h2_exponent` | alters a summary vector; producer catches consistency, checker later recomputes only the toy | not an actual v247 owner |
| 16 | `k_z_inverse_scalar_powered_word` | assigns an invalid scalar | shallow shape rejection |
| 17 | `live_resource_cap` | edits a prebuilt synthetic stop witness | never drives the live meter past a cap |
| 18 | `positive_status_terminal` | changes a SELFTEST `PASS/SELFTEST_COMPLETE` envelope | wrong owner; not the production positive ABI |
| 19 | `nonpositive_false_progress` | sets a flag on the positive SELFTEST certificate | wrong owner; not `validate_nonpositive` |
| 20 | `duplicate_markers` | changes JSON `marker_count` | wrong owner; no duplicate producer/checker/final log line |

This is not 20-owner mutation reachability.  Broad-catch, wrong-owner, and
wrong-seal rejection are explicit blockers under task323 Section 5.

The positive fixture also cannot reach these controls: on its first query,
`ToyRuntime.boundary_source` accesses the nonexistent
`self.boundary_records`.  Additionally, producer `make_toy_runtime` zips six
words against `rows.values()` from a dictionary whose freely reduced empty-
word key is duplicated, collapsing/realigning the roster; the independent
checker retains the six-row list.  Their direct initial-defect replay would
therefore disagree even after the missing attribute is repaired.

## 6. Performance and live-resource audit

Let `n=6441`, `t` be terminal kernel rank, `t0` the initial rank raises,
`b` the number of inserted boundary rows, and `s` a sparse reduction cost.
If the generic toy-shaped kernel were reachable, the code makes exactly

```text
oracle.query calls  = 2*n + 9*t + 2
oracle loop rounds  = 2*n + 9*t + 2 + b
boundary-only reductions for basis/anchor binding = 2*t + 1
```

before counting alternate/bidirectional basis-change reductions.  Therefore
the advertised `2*n+9*t+t0+2+b` is only a loose upper bound with a spurious
`t0`, not the exact count claimed in the reply.  Each total reduction scans
up to `b+t` pivots, but NONMEMBER dual construction reduces a second time,
and every boundary insertion is pre-reduced and then reduced again in both
views.  The displayed query bound also omits alternate insertion, two basis-
change directions, boundary-only receipts, and anchor work.  There is no
rebuild of all retained rows per one of the 6,441 queries, which is a genuine
v1 improvement, but avoidable duplicate reductions remain.

Four dense matrix compositions do give the stated worst-case `O(4*t^3)`
tail if reached, and the old quadratic pairwise F3 tautology loop is absent.
Zero global-roster construction follows from the source, but only because the
actual runtime is absent.  Forty actor-cache creations follow for each toy
process; they do not establish forty authenticated actual actor values.

Further load-bearing performance/resource failures are:

- `make_envelope` canonicalizes the full body for sealing, then
  `sealed_bytes` canonicalizes the same full body again for writing.  This is
  precisely the prohibited double full-output serialization.
- The resource snapshot is inserted into the body before either serialization
  bump, so the sealed receipt underreports the work used to seal and write
  itself.
- Authority files and producer receipts are read into memory before the input
  cap is charged.  Oversize input can exhaust memory before a typed resource
  stop.
- Canonical receipt equality, receipt self-seal, whole-row digest, and seven
  chunk digests repeatedly serialize/hash roughly the same 31 MB object;
  several of those serializations are not charged to `serialized_bytes`.
- The producer serializes defects again in `initial_replay` and action rows
  again in `translate_replay`, despite already retaining the corresponding
  initial/translated records.
- Sparse support has no general live cap before a large row is allocated.
- Recursive DAG evaluation has no memo table, so shared ancestry can be
  reevaluated in proportion to expanded ancestry rather than DAG size.
- Checker ancestry-node ingestion is not charged, and the positive actual
  checker work is absent rather than bounded.
- `last_replayable_state` is overwritten with transient query/rank labels even
  though no checkpoint can restore them; a resource envelope simultaneously
  advertises `rank_zero_restart=true`.  The recorded last state is therefore
  not necessarily replayable.

There are no sleeps, retries, polls, locks, or an unnecessary extra checker
subprocess.  One producer followed by one independent checker is the required
dependency.  These positive observations do not offset the unimplemented
actual route, duplicate serialization, false resource transcript, and
avoidable reductions.  `PERFORMANCE: FAIL`.

## 7. Newly staged task198 authority bundle — separate verdict

### Exact identities

| staged member | bytes | SHA-256 |
|---|---:|---|
| receipt | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| acceptance manifest | 1,966 | `44ad985b20c7238e5aea661355b28b7c6b1100cd1e3947f7f23d8f658bf67903` |
| producer attestation | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| checker attestation | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |

Both JSON files are compact ASCII with zero CR/LF.  Read-only byte surgery on
the canonical top-level objects independently reproduced:

```text
receipt self digest  = c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f
manifest self digest = 2c7f543cba2f0f0ee2b8f2b23269129eb0e67500361e4712e5e52bcf01566d0e
row digest           = e00880c01bc96ba8f0549311f4955662668d74001ecf5c06097646dad4268950
```

The row byte stream contains exactly 6,441 contiguous entries with the exact
local ordinal blocks `Gamma_Cayley 1..6318`, `action 1..104`, and `Q0_lift
1..19`; seven sealed chunk intervals are present.  The manifest exactly binds
both sides to run `33155710862`, head
`bed1d5e6b41477b8799f2a33a24e46f7800f9510`, artifact `9686477718`, archive
digest `8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854`,
and the receipt basename/bytes/SHA/self-digest.  Its three source identities
match the current local producer, checker, and task198 driver exactly:

```text
producer 137169 / 6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c
checker  157253 / 001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1
driver    20541 / 6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068
```

The two attestation bytes are exactly the positive producer terminal and
independent checker PASS line, including one final LF each, and their hashes
match the manifest.  Removing only top-level `resource` and self-digest from
this receipt and the preserved producer-only capture yields identical
30,582,643-byte objects with common SHA-256
`595dbe85a9338ef77c694a31f62e456c5f49f6bd84263b8273bf21fb38238d19`.
Thus every non-resource mathematical/structural field agrees exactly with
the earlier capture.

### Bundle blocker

**AUTHORITY_BUNDLE: REJECT.**  Neither staged JSON contains an `accepted`
field or an `independent` field.  The four-file bundle omits the direct run's
150-byte canonical checker verdict

```json
{"accepted":true,"independent":true,"receipt_terminal":"ROOF_BRIDGE_ISOMORPHISM","schema":"d972-r07-seven-context-roof-presentation/v1/crosscheck/v2"}
```

whose preserved artifact identity is SHA-256
`ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de`.
The acceptance manifest binds only the checker terminal-line attestation; it
does not bind that verdict's basename, bytes, SHA, or its two Booleans.  Hence
the commissioned four-file A4 authority bundle does not itself prove
`accepted=true, independent=true`.

This narrow bundle rejection does not reverse the separately recorded v264
cross-check of the underlying GHA run.  It says that the four staged A4 input
members do not carry/bind all evidence required by task323 Section 7.  It also
does not alter the independent A4/v2 rejection above.

## 8. F1--F13 and final accounting

| item | verdict | reason |
|---|---|---|
| F1 layer-local ordinals | **FAIL** | producer roster is correct; checker permits interleaved layers and the mutation uses a three-item shadow roster |
| F2 exact authority | **FAIL** | producer pin is `None`; checker has no manifest SHA pin; checker verdict/accepted/independent are unbound |
| F3 complete receipt semantics | **FAIL** | actual normal-proof schema/value mismatch; bridge ledger mismatch; evaluator/canaries underchecked |
| F4 resolved exact paths | **FAIL** | traversal/outside escape repaired, but same-basename in-tree symlink alias is not rejected |
| F5 raw boundary ancestry | **FAIL** | normalized ancestry is replayed as raw; nonmember exported sign is wrong |
| F6 independent echelon/basis change | **FAIL** | raw-K/normalized-basis mismatch and deterministic `change_map` wrong-type call |
| F7 conjugator/source binding | **FAIL** | convention exists; scaled/prior-K source-word ancestry is omitted |
| F8 complete checker replay | **FAIL** | actual positive replay is deferred; all negative receipts and producer maps are not replayed |
| F9 direct group replay | **FAIL** | vector tautology removed, but wired test is only synthetic H2 and actual group ABI is absent |
| F10 production-shaped mutations | **FAIL** | all 20 are shallow/wrong-owner or broad-catch; SELFTEST fails before controls |
| F11 positive terminal | **FAIL (syntax repaired only)** | exact ISO token is explicit, but the branch is unreachable and its shaped result bypasses every A4 computation |
| F12 nonpositive/resource envelope | **FAIL** | current static envelope is sound, but resource last-state/restart semantics and allocation-before-cap are not |
| F13 exact-one driver | **FAIL** | log counts/equality repaired; sealed independent checker verdict is absent |

```text
TASK323 A4/V2 STATIC AUDIT:                    REJECT / UNEXECUTED
TASK313 F1--F13 REPAIR COVERAGE:              NOT COMPLETE
AUTHORITY/PATH SEMANTICS:                     FAIL
AUTHORITY_BUNDLE (FOUR STAGED FILES):         REJECT
ACTUAL POSITIVE-BRANCH REACHABILITY:          FAIL / UNCONDITIONAL STOPS
INDEPENDENT POSITIVE REPLAY:                  NOT IMPLEMENTED
MUTATION OWNER REACHABILITY:                  FAIL 0/20 TO REQUIRED STANDARD
FULL Q0 / GLOBAL ROSTER RECONSTRUCTION:       FORBIDDEN / ABSENT
MEMBERSHIP ECHELON:                           LIVE SHAPE / CERTIFICATE INCORRECT
PERFORMANCE:                                  FAIL
SELFTEST:                                     UNEXECUTED
PRODUCTION:                                   UNEXECUTED
ACTUAL A4:                                    0/3
LIFT / FAKE / IHARA:                          NONE
```

`TASK323_R07_TASK315_A4_V2_CODE_PERFORMANCE_AUDIT_REJECT_UNEXECUTED`
