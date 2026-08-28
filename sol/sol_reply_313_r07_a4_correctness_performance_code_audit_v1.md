# Sol(max) reply 313 — R07 A4 correctness/performance static code audit

## Verdict

**REJECT.  Do not execute actual A4 with this bundle.**

This is a source-only ruling.  Performance is load-bearing in the verdict,
not a note: the current producer and checker contain prohibited full-space
reconstruction, rebuild an existing echelon from zero on every membership
round, flatten unmetered ancestry, and do not make most advertised caps live.
There are also deterministic correctness stops before those costs can produce
a positive certificate:

1. the actual task198 roster uses per-layer ordinals, while both A4 paths
   require one global ordinal sequence;
2. the producer's successful return calls `envelope("COMPLETE", ISO, ...)`
   without passing `terminal=ISO`, so the emitted terminal is `COMPLETE`, a
   value rejected by both checker and driver;
3. no independently accepted task198 authority bundle is pinned, and the
   structural manifest/attestation checks do not bind an actual checker run;
4. boundary/K coefficients, literal ancestry, negative duals, action matrices,
   and the projected basis anchor are not independently replayed to the
   commissioned standard.

No Python, Node, GAP, GHA, workflow, network, or git command was run.  Neither
producer nor checker was executed.  Read-only source inspection and byte/SHA
reads only were used.  Consequently this audit is not A4 progress.

```text
EXECUTION:                         UNEXECUTED
A4 ACTUAL PRESENTATION INPUT:      0/1
A4 ACTUAL INVARIANT CLOSURE:       0/1
A4 ACTUAL WORD-BEARING K:          0/1
A4 ACTUAL:                         0/3
LIFT / FAKE / IHARA CONCLUSION:    NONE
```

## 1. Static identities and governing pins

The four audited paths have the following read-only identities.  The three
driver pins at driver line 14 match the current producer, checker, and fixture;
the GAP driver is ASCII-only.

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v1.py` | 89,162 | `fe5dcf38b774b15c1a2907e70f8e6f90beca90b887aef1e0ea661f486817b862` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v1.py` | 55,388 | `157c61927884eeb3d7a01d1f6e8df6755e52dc708353fdb38eb7ad57239333d2` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v1.g` | 4,242 | `d29f99ba3e50640990ad9249af57eb9dc07b45391980c050f2622fa8ea5e52d2` |
| `search/certs/d972_r07_word_independent_successor_kernel_selftest_v1_20260828.json` | 720 | `302c31244a43a86dd46d4a54e41756f067044f251db78b749c7bf70025fc85e7` |

All eleven entries in producer `PROOF_PINS` (producer lines 71--83), including
v188, v189, v190, v231, v247 and the task232/244/244b/252 contracts, match
their current exact bytes and SHA-256.  All three `TASK198_PINS` entries
(lines 84--88) also match, including the refreshed 157,253-byte task198
checker from task284.  Pin integrity itself is therefore a PASS.

The mathematical architecture in the five requested proof pins is coherent:
v188/v231 replace a roof or successor roster by the rank-bounded relator-defect
closure; v189 fixes ten typed coordinates versus seven relation blocks; v190
fixes the complete 6,441-row presentation; and v247 requires an actual A4
basis lift of the projected `z0`, not the literal commutator cube.  The code
failures below are implementation/certificate failures, not a rejection of
those paper theorems.

## 2. Task198 authentication — FAIL

### F1. Actual row ordinals are rejected deterministically

Producer lines 862--868 and checker lines 225--229 require

```text
row["ordinal"] == enumerate(rows, 1)
```

over the entire 6,441-row concatenation.  The pinned task198 producer instead
constructs ordinals within each layer: Gamma Cayley rows at task198 producer
lines 1140--1142, action rows at lines 1163--1165, and Q0 lifts at lines
1171--1176.  Thus the first action row has global position 6,319 but ordinal
1; the first Q0 lift has global position 6,423 but ordinal 1.  A genuine
task198 receipt necessarily hits `TASK198_LITERAL_PRESENTATION_ROW` before
any successor work, and its independent A4 authentication fails the same way.

Bounded repair: validate the exact ordered `(layer, layer-local ordinal)`
roster—Gamma `1..6318`, action `1..104`, Q0 lift `1..19`—together with the
seven chunk seals.  Do not replace the receipt's typed ordinal by a new global
meaning.

### F2. The external authority is syntactic, not exact

Producer lines 907--920 and checker lines 257--268 correctly require a
canonical seven-key manifest and bind member bytes/SHA to the receipt.  But
`artifact_id` and `run` need only be nonempty strings; `head` and
`zip_sha256` need only look hexadecimal.  No exact accepted task198 run,
artifact, ZIP digest, head, checker run, or sidecar digest is anchored.  The
two text attestations at producer lines 926--929 and checker lines 273--277
are exact strings, but they carry no run/head/member digest and are not bound
to the manifest.  Anyone able to stage four mutually consistent files can
mint those lines.

This matters now.  V258 authenticates only the task198 **producer capture**:
run `33155653989`, member bytes `31017244`, member SHA
`d4bccb2f6443acde5ebe07c3648fc9a505315fd4b2eb00e6cdbad372fa9c5f4b`.
V258 lines 63--76 explicitly say the independent checker was still pending
and the capture must not yet be staged as accepted A4 input.  No later
accepted task198 authority was included in this commission.  Therefore the
task198 prerequisite remains 0/1 regardless of the A4 source defects.

Bounded repair: after an actual independent task198 acceptance, issue one
canonical acceptance manifest binding exact producer and checker run/head,
artifact/ZIP/member identities, receipt self-digest, both exact terminal-log
digests, and current task198 source identities.  Pin that manifest's bytes/SHA
in the A4 driver and independently in both A4 implementations.  V258 alone
must remain nonpositive.

### F3. Receipt semantics are only partially authenticated

The following checks are present and sound as far as they go: schema/status/
terminal and self-seal (producer lines 846--855; checker 210--224), 6,441 rows,
layer counts, row digest and seven chunks (producer 856--890; checker
217--243), fixed task176 provenance (producer 921--925; checker 269--272), and
bridge branch/kernel one.

They do not satisfy the exact task232/task237 input ABI:

- raw receipt bytes are not required to equal canonical serialization;
- `normal_closure_exact=True` is trusted without checking the v190
  `normal_generation_proof`, its 243/6318/104/19/order-bound fields, or its
  task172 roster binding;
- bridge validation checks only branch and kernel order (producer 891--894;
  checker 244--247), not image order, ten-to-eleven insertion, seven blocks,
  eleven occurrences, four marked inverse replays, typed-ledger digest, or the
  6,441 bridge replay digest;
- evaluator validation checks only schema and the six entry-point names
  (producer 895--900), not callable argument schemas, multiplication/action
  semantics, exact widths `40^5,154^5`, typed-coordinate digest,
  `relator_rows_sha256`, or canaries.  The checker is weaker still;
- local task198 source pins are checked only by the producer.  The checker
  does not independently authenticate the task198 implementation/dependency
  cone.

Exact accepted bytes could make many semantic rechecks redundant, but the
current code has neither an exact accepted-byte pin nor the full semantic
fallback.  It cannot use the two weaknesses together as an authentication
argument.

### F4. The path guard admits traversal aliases

Producer lines 828--831 and analogous checker guards accept any textual path
starting `ci/in/`, including `ci/in/../../...`; output/checkpoint guards use
the same pattern.  This is not the exact guarded-path contract.  Resolve the
path, require containment under the resolved `ROOT/ci/in` or `ROOT/ci/out`,
reject `..`/aliases, and for the four task198 inputs require the exact
registered basenames.

## 3. Successor mathematics and certificate replay

### What is correctly represented

- The fixed types, IDs, and tags at producer lines 31--44 and checker lines
  22--25 are the required five E3 plus five E4 roster, preserving E3-C21 and
  E4-C21.
- `task232_contexts` (producer 1011--1032) uses the literal substitutions and
  frozen right-to-left `PP`; the checker reconstructs them separately at
  lines 320--328.
- The producer's lazy support-times-occurrence boundary oracle (1062--1149)
  queries all ten tagged direct-sum coordinates without enumerating all
  boundary translates.  The checker implements a reverse traversal rather
  than calling task179's deciding `boundary_oracle` (checker 438--488).  This
  is the right generator-only boundary architecture.
- The producer does enqueue each quotient-rank raise, applies four marked
  actions, drains the queue, and subsequently queries all 6,441 initial rows
  and all four translates (producer 1238--1367).  The checker independently
  drains a differently ordered generator queue (526--559).
- The built-in H2(9) multiplication/inverse at producer 182--214 and checker
  52--80 matches v252.  Least-nonzero selection and inverse-scalar word
  construction in producer 1419--1467 and checker 363--417 have the correct
  intended form.

These partial PASS items do not rescue the certificate because the following
load-bearing gates fail.

### F5. Boundary ancestry is not a serialized proof

When a boundary row is inserted, producer lines 1123--1130 discard the
echelon insertion ancestry and retain only `inserted: True`, the raw row, and
provenance.  Later `boundary_value_from_coefficients` (1215--1225) interprets
`B:<pivot>` against normalized internal boundary rows, not against serialized
raw boundary-record indices.  The pivot-to-raw-row coefficient maps in
`self.boundary.ancestry` are never exported.  Basis rows then expose a bare
`boundary_value` and coefficients over those private pivots (1270--1286,
1322--1340).  A consumer cannot replay every boundary coefficient/sign from
the receipt without recreating the producer's private min-pivot state.

The checker does not do that replay: lines 606--622 check only field presence,
and lines 713--719 compare boundary rank/record counts and nonempty provenance.
It never proves a producer `boundary_value` is the stated combination of the
translated rows.  This fails task244 Sections 3 and 5.

Bounded repair: label every raw translated boundary record by a stable record
index, retain the independently implemented pivot ancestry all the way to
those raw indices, expand each K-row boundary certificate to that label set,
and have the checker reconstruct each translated row and replay the exact F3
sum.

### F6. Checker coefficient receipts are mathematically false

`IndependentEchelon.insert` reduces and pivot-normalizes an input row but
stores only one label (checker 128--136).  It does not store the inherited
row-operation coefficients or the pivot scale.  `reduce_with_coeff` later
attributes a normalized stored pivot directly to that original label
(138--149).  Hence its `B:*`/`K:*` maps are generally not coefficients of the
rows supplied by the caller.

This corrupts checker membership/action matrices and the K coordinates used
in the anchor.  It also makes the literal equality tests at checker lines
669--670 and 688--689 doubly invalid: task232 explicitly permits the checker
to discover a different basis, so checker-basis coordinates need not equal
producer-basis coordinates even after coefficient ancestry is repaired.

Bounded repair: implement an independent coefficient-carrying echelon whose
insert scales inherited ancestry, replay every returned sum, and compare
elements/spans through an explicit producer-to-checker change-of-basis map
modulo independently rebuilt boundaries—not by equality of coordinate
dictionaries belonging to different bases.

### F7. Literal conjugator ancestry reverses after depth one

For a translated basis row, producer lines 1304--1310 prepend the new outer
letter to both the conjugator list and literal word.  After two actions this
correctly stores the literal word

```text
b a r a^-1 b^-1.
```

But `ancestry_value_actual` iterates the stored list from left to right
(1489--1493).  The list `[b,a]` therefore applies `b` first and then `a`,
producing `a.(b.v)` rather than the required `b.(a.v)`.  No commutation of the
two roof actions is available.  The toy has the same ordering pattern and
does not force a depth-two rank raise, so it is not a gate for this defect.

Furthermore `evaluate_k_z` only asks whether the directly evaluated basis
source word belongs to final `B+K` (1434--1445).  It never requires that word's
translation equal the indexed stored basis row modulo a **boundary-only**
combination.  Thus the H2 projection vector is not proved to be the projection
of the ordered basis whose row certificate is exported.

Bounded repair: give conjugator lists one explicit composition convention and
replay them against `conjugated_word`; for every basis index require
`direct_defect(source_word) - stored_row` to have a boundary-only receipt.
Then and only then compute the v247 projection and least-index anchor.

### F8. The independent checker does not replay the producer load-bearing data

The checker rebuilds a candidate subspace, which is necessary, but it mostly
checks producer ledgers by shape or Boolean:

- it does not compare each producer initial source word/ten chains/defect to
  its own reconstruction, nor replay each producer membership coefficient
  (checker 593--603);
- it does not verify producer negative dual annihilation, full boundary
  zero-correlation, normalization, or target pairing (606--618);
- it does not replay literal producer ancestry or boundary sums (619--622);
- it constructs checker action matrices but never compares their entries with
  producer matrices; producer matrices need only be truthy and the producer's
  four summary Booleans fixed (692--700);
- it compares boundary transcript lengths, not active row/provenance/scalar
  equality (713--719);
- `IndependentEchelon.dual` itself lacks the producer's final all-row
  annihilation gate, and no loop replays every producer dual.

Therefore omitted/wrong rows can survive behind matching rank, span, count,
or asserted summary fields.  This is below task232 Section 8 and task244
Sections 5--6.

### F9. The advertised group replays are tautological vector operations

Producer lines 1389--1394 check `v+2v=0` and
`(a+b)+2a=b` on F3 dictionaries.  The second is an algebraic tautology and
the first follows from the representation; neither directly evaluates the
retained source words' cubes or commutators in the ten affine successors.
The checker trusts the resulting producer Booleans at 696--700.  A structural
proof that every directly evaluated word lies in the authenticated
elementary-abelian kernel could replace a quadratic word-pair replay, but the
current tautologies are not that proof.

### F10. SELFTEST/mutations do not own the production gates

The fixture's types, context IDs, completeness, queue, alternate-basis, and
`production_forbidden` fields (fixture lines 7--19) are mostly ignored; the
producer reads only minimum rank and context count (producer 808--811), and
the checker again reads only those two values (checker 913--916).  The toy is
a separate `run_toy` algorithm rather than the production functions required
by task237 Section 9.

Many of the 57 names are aliases or shallow digest/Boolean edits: for example
`task198_bytes`/`task198_artifact`, multiple completeness aliases, and several
affine mutations collapse to the same owner (producer 739--800; checker
863--912).  None mutates the real task198 authentication, complete boundary
oracle, production queue, depth-two ancestry, runtime resource stop, or exact
positive terminal.  A syntactic 57/57 result would not establish production
reachability or semantic rejection.

## 4. Deterministic terminal and driver failures

### F11. The positive producer terminal is unreachable

Producer line 1542 calls

```python
return envelope("COMPLETE", ISO, result, started, meter)
```

while `envelope` sets `terminal` to `terminal or status` at lines 1568--1575.
Because no terminal argument is supplied, a completed kernel emits terminal
`COMPLETE`, not `R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_PASS`.  Checker line
924 and driver lines 29--30 allow only the ISO token (or the two UNKNOWN
tokens), so a genuine computation cannot be accepted.

Bounded repair: pass `terminal=ISO`, and independently require the exact
positive status/reason/result schema and all forbidden flags in the checker.
Do not merely add `COMPLETE` to the allowlist.

### F12. Nonpositive receipts are underchecked

For `UNKNOWN_INPUT` or `UNKNOWN_RESOURCE`, checker lines 919--939 verify only
schema, terminal vocabulary, and self-digest.  They do not require status to
match terminal, A4 milestone zeros, all downstream flags false, a typed
resource/input reason, or a resource-cap witness.  A resealed nonpositive
receipt carrying false progress or a fake/Ihara flag would pass.

### F13. Exact-one marker gates are not exact-one

In SELFTEST, driver line 25 uses `grep -Fxc ... >/dev/null`, which accepts any
positive count.  In PRODUCTION, lines 29--30 take `tail -n 1` and never require
the count to be one.  Duplicate producer/checker terminals therefore pass the
marker gate.  Lines 31--32 correctly require nonempty exact terminal equality,
but equality of the last occurrences is not exact-one acceptance.

The fixed receipt/OK/log/shell stale-output precheck at driver line 18 and the
producer's final-output existence checks at lines 1616--1632 are otherwise
sound.  Optional checkpoint output is not stale-protected and can be
overwritten at producer lines 1547--1557.

## 5. Production hot paths and asymptotic audit — FAIL

Use the following symbols:

```text
n = 6,441 presentation rows
c = 10 typed successor contexts
t = terminal K rank
t0 = rank raises among the initial n rows, 0 <= t0 <= t
b = retained translated-boundary rank
s = a representative sparse-row support cost
L = total signed-letter length of the 6,441 words
A = fully expanded ancestry letter/term volume
q = 1,469,664 Q0 states
```

### 5.1 Producer path

| phase | static roster/bound | current cost and ruling |
|---|---:|---|
| Task198 input | v258 candidate is 31,017,244 bytes | One JSON parse at producer 846--850, followed by linear self/row/chunk hashing.  There is no second JSON parse in this process; that part is acceptable.  Input bytes are not metered. |
| Imported runtime | exactly `q` states and `2q=2,939,328` positive Q0 edges | `p179.build_runtime` is called at producer 1509--1519.  Its lines 454--580 reconstruct the task175 6,441 roster, then call task176 `enumerate_q0_sections` and scan all Q0 memberships.  The section stores alone have width `5*40+5*154=970` bytes per state, at least **1,425,574,080 raw bytes**, before state dictionaries/lists.  A4 uses only local E3/E4 successor arithmetic and boundary generators.  This full Q0 group-space construction and duplicate 6,441-roster reconstruction are unnecessary and prohibited. |
| Initial successor defects | `n*c = 64,410` Fox/substitution evaluations, total word work `O(cL)` | This is mathematically necessary once in the producer.  The independent checker must repeat it. |
| Membership calls | exactly `2n + 9t + t0 + 1`, hence between `12,883+9t` and `12,883+10t`, plus one repeated round per new boundary row | Every round constructs a new `Echelon` and reinserts every retained B and K row (producer 1105--1113).  Building `m=b_current+t_current` rows is worst-case `O(m^2 s)` before reducing/dualizing the candidate.  The aggregate hot path is therefore as bad as `O((12,883+10t+b)(b+t)^2 s)`.  This is the commission's expressly forbidden “recompute rank from scratch where the existing echelon can be updated.” |
| Marked action | at least `8t` actions for closure plus terminal replay, then ancestry actions | Each `actual_action` recomputes ten marked actor Fox evaluations and scans the whole row once for each of ten coordinates (1152--1172).  Cache the 40 actor values once and bucket a row by coordinate. |
| Matrix/group tail | four sparse matrix compositions; pair loop over `t^2` rows | `compose` can reach `O(t^3)` when dense (1369--1386).  The `t^2` commutation loop (1391--1394) is both expensive and tautological.  Neither loop performs a live wall/RSS check. |
| Ancestry | no static bound in code | `combine_term_ancestry` copies flattened prior term lists (1204--1212); translate insertion copies them again (1303--1317); `word_from_ancestry` materializes the entire literal word.  This can grow combinatorially with rank/depth.  The declared ancestry node/word caps are never charged. |
| Anchor | `t+1` ten-context word evaluations plus `t+1` membership calls | Required in principle, but the words may already have unbounded `A`, and membership again rebuilds the whole echelon. |
| Receipt/seal | `n` full initial records, another `n` replay records, `4t` translate records, basis/ancestry, boundary transcript | The authenticated task198 return stores `Delta0` (which contains presentation) and the same `presentation` again at producer 930--937, so JSON serialization expands the 6,441 rows twice.  `envelope` canonicalizes the entire output for its digest and `main` canonicalizes it again for writing.  No serialized-byte cap or streaming digest is used. |

The correct bounded membership design is one live coefficient-carrying total
echelon.  Insert a newly certified boundary or K row once, retain its stable
raw-family ancestry, and reduce future candidates against that state.  A
separate boundary-only view may be kept for provenance, but neither view
should be reconstructed per query.

### 5.2 Independent checker path

The independent parse/reconstruction of the task198 input and the `n*c`
successor defects is **necessary checker replay**, not accidental duplicate
work.  Running checker after producer is also a genuine data dependency: it
must inspect the producer receipt.  The driver has no sleeps or locks, and the
producer/checker processes are not needless subprocesses.

The following extra work is accidental:

| phase | static bound | current cost and ruling |
|---|---:|---|
| Checker runtime | same `q`, `2q`, and >=1,425,574,080 raw section bytes | Checker line 531 again calls producer-side `p179.build_runtime`; the full Q0/state/membership and predecessor 6,441-roster work is not needed for an independent local successor/boundary replay. |
| Checker membership | for a positive equal-rank run, approximately `n+7t+1`, plus `b` active-boundary repeats | Checker lines 491--509 rebuild `IndependentEchelon` from every B and K row on every round.  It has the same `O((n+7t+b)(b+t)^2 s)` worst-case defect. |
| Checker action/matrices | `4t` action rows and four matrix products | Each checker action recomputes ten generator roof values and rescans the row ten times (420--435); dense matrix composition can be cubic. |
| Producer receipt load | proportional to the unbounded producer output | Necessary once, but made needlessly large by duplicated task198 rows and flattened producer ancestry. |

A lightweight producer runtime and a separately coded lightweight checker
runtime should reconstruct only the pinned PB3/PB4 quotient arithmetic,
boundary-source rows, blob codec primitives, and ten marked generator values.
Neither needs task179's Q0 section census, `scan_memberships`, `prove_L`,
global roster, or task175 roster equality in this A4 invocation.

### 5.3 Resource caps are not live

Producer lines 45--52 advertise caps which are mostly disconnected from the
executed monitor:

| advertised cap | static result |
|---|---|
| `wall_seconds`, `rss_bytes` | Partially checked by `Task179Monitor` only on selected bumps.  Authentication, quadratic/cubic tail work, ancestry flattening, sealing, and output writing have no checks.  `merge_snapshot` records only the successor monitor's elapsed segment, so final wall time can exclude authentication. |
| `input_bytes` | Never bumped; the 31 MB task198 input and checkpoint are uncharged. |
| `relator_evaluations` | Never bumped.  The code uses a different `candidate_words` counter. |
| `affine_oracle_rounds` / `membership_queries` | The successor monitor enforces its own `oracle_rounds`; the advertised keys are never charged. |
| `boundary_columns` | Never bumped; only the separate `retained_columns` limit is live. |
| `accepted_rank` | `monitor.bump("accepted_rank")` is called, but `Task179Monitor.limits` has no such key, so the 100,000 cap is unreachable. |
| `queue_actions` | Never bumped. |
| `ancestry_words`, `ancestry_nodes` | Never bumped despite unbounded flattening/materialization. |
| `dual_correlations` | Never bumped; `boundary_pairs` is only a partial surrogate. |
| `checker_work` | Checker increments it, but `CheckerMonitor.bump` never compares any limit. |
| `checkpoint_bytes` | No size preflight/check when writing. |
| `serialized_bytes` | Never bumped before the two whole-object serializations. |

Checker lines 294--317 are especially decisive: `check` only assigns a phase,
and `bump` only increments.  The nominal four-hour/8 GB checker limits are
never enforced.  An OS/GHA timeout would be an untyped process loss, not
`UNKNOWN_RESOURCE`.

The advertised resume path is also not a usable checkpoint.  Producer
1470--1481 authenticates a seal, but production recomputes task198 auth,
runtime, all rows, boundary state, and the complete queue before it inspects
three resume fields at 1527--1531.  It neither restores accepted rows/oracle
state nor checks input equality, cap monotonicity, cursors, or transcript.
Resource stops write only an empty rank-zero restart (1550--1554).  Either
implement a genuinely safe incremental checkpoint and charge its replay, or
remove the progress/resume claim and explicitly expose rank-zero restart only.

Because large work occurs outside any live cap, and because the checker cap is
wholly inert, completion within the configured 14,400 seconds/8 GB for the
preregistered input cannot be certified.  This is independently sufficient
for REJECT.

## 6. Required bounded repair before another static audit

1. **Freeze task198 authority first.**  Obtain an actual independent task198
   acceptance and pin one exact producer+checker acceptance manifest.  Repair
   per-layer ordinals, canonical bytes, full v190/bridge/evaluator semantics,
   and resolved exact paths.
2. **Fix the terminal ABI.**  Emit the exact ISO positive terminal, require
   exact status/reason/zero-or-one milestone rules, validate all false
   downstream flags for every terminal, and make all driver marker counts
   exactly one.
3. **Create a lightweight A4 runtime.**  Remove the 1,469,664-state Q0 census,
   Q0 membership scans, global roster facilities, and redundant task175
   6,441-row reconstruction from both processes.  Cache the forty marked actor
   values.
4. **Make the quotient echelon incremental.**  Maintain one live B+K echelon
   per implementation, store full scaled ancestry to raw B/K labels, and
   never rebuild it per query.  The checker must use its own pivot/ancestry
   implementation and an explicit basis-change proof.
5. **Repair word and boundary ancestry.**  Fix conjugator composition order,
   serialize raw-boundary coefficients, and directly bind every source word to
   its indexed basis row modulo boundary only.  Replay every producer positive
   coefficient and negative dual in the checker.
6. **Rebuild the v247 gate on that basis binding.**  Independently compare full
   basis H2 values and direct ten-context values; compare elements through
   change-of-basis rather than equating coordinates from different bases.
7. **Bound all materialization.**  Use a persistent ancestry DAG/stream,
   compact nonduplicated task198 identity references, incremental output
   hashing/writing, and live counters for every declared cap.  Check wall/RSS
   inside every long loop and before/after serialization; a cap stop must seal
   a replayable state or an honestly named rank-zero restart.
8. **Replace the toy gate.**  Exercise the production authentication,
   membership, queue, ancestry, resource, terminal, and checker owner
   validators on a bounded fixture.  Every named mutation must change its own
   reconstructed object and reach its exact owner gate.

Only after these repairs pass a new correctness **and performance** static
audit should actual A4 be dispatched.  A static PASS at that later point
would still leave A4 actual at 0/3 until producer and independent checker have
accepted the real object.

```text
TASK313 A4 CORRECTNESS AUDIT:                  REJECT
TASK313 A4 PERFORMANCE AUDIT:                  REJECT
TASK198 ACCEPTED PRODUCER+CHECKER AUTHORITY:   NOT PRESENT IN v258
COMPLETE 6,441-ROW A4 INPUT GATE:              UNREACHABLE AS CODED
POSITIVE A4 TERMINAL:                          UNREACHABLE AS CODED
INCREMENTAL ECHELON / LIVE RESOURCE CAPS:      NOT IMPLEMENTED
A4 ACTUAL:                                     0/3
LIFT / FAKE / IHARA:                           NO CONCLUSION
```

`TASK313_R07_A4_CORRECTNESS_PERFORMANCE_STATIC_AUDIT_REJECT_UNEXECUTED`
