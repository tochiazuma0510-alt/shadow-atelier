# Sol(max) reply 361 — task359 pre-A0 A3 code/performance audit v1

## 0. Verdict and audit boundary

**Static verdict: REJECT.**  **Execution/GHA: UNEXECUTED.**

The frozen five task359 outputs have the commissioned byte counts and SHA-256
values, and the underlying g760/v302/task226/task227 mathematics has no further
shape mismatch identified below.  Nevertheless there are multiple independent,
deterministic blockers before any actual closure can be accepted:

1. the exact P0 bytes fail both programs' canonical-input predicate;
2. P0's declared self seal does not match its canonical seal-stripped body;
3. the driver carries a 63-character P0 SHA and therefore stops on its own pin;
4. the projected ABI is resealed incorrectly and is not the v303-only object;
5. task198's required semantic authority links and exact evaluator ABI are not
   decoded;
6. the independent 486/729 verifier is unmetered, serialization is not reserved,
   and cap stops do not reliably publish typed UNKNOWN; and
7. the driver can call an UNKNOWN/UNKNOWN match `DRIVER_PASS`.

Any one of items 1--3 is already fatal at the frozen identities.  Therefore no
MEMBER or NONMEMBER terminal, no A3 numerator, and no downstream conclusion is
authorized by this audit.

I did not run Python, Node, GAP, GHA, a workflow, or any candidate program.  I
used read-only PowerShell inspection/hashing and an initial read-only commit,
branch, and status check; there was no git mutation or network access.  The
inspected identity was branch `sol/r07-explicit-lift-20260825`, commit
`0e625fea63f5ece8757d95cae7b89e5b3e3a678f`.  The already-dirty unrelated
worktree was left untouched.

## 1. Frozen identities and seal graph

The commissioned files physically match the supplied identities:

| owner | bytes | SHA-256 |
|---|---:|---|
| P0 | 6,691 | `f8092796af77da3ea137908b1cca48db6563c412d937147bc341be29cc49489f` |
| producer | 45,897 | `de69138d64a0324b45cd8327cb1425df88dcf54525c32d6127f0dbac251e94d6` |
| checker | 46,751 | `ba087b0e37fa15a7ff8dbb1a1d65509e0a3721b4d1b4a0f07789c40c3411ad7d` |
| driver | 7,032 | `69ac613a075b3677b16b038ae9be8dd0954acfbfd9038b6929f94f5ada322f8a` |
| Luna reply | 6,643 | `f9d56734b22f1512789efcf27b1265c080d3648038ba80e4ce580314d00cad48` |

All physical task198 receipt/manifest/attestation/verdict/source-owner pins,
both g760 ancestry pins, both task226 engines, both task227 engines plus its
driver, and v302/v303 also match the byte/SHA roster in P0.  Structurally the
intended graph is acyclic: old authorities point to P0; each new Python owner
pins P0; the driver pins P0 and the two new Python owners.  P0 does not pin a
new program or the new driver.

That structural graph is not executable because its root is malformed:

### F1 — P0 is not the canonical byte string required by either program

P0 byte 6,691 is `0x0a`.  It also has non-sorted object keys; for example,
inside `authority`, `task198_acceptance` occurs after the task227 entries even
though Python `sort_keys=True` places it before `task226_*`.  Producer lines
234--241 and checker lines 197--204 define canonical bytes with
`json.dumps(..., sort_keys=True, separators=(",", ":"), ensure_ascii=True)`
and no trailing newline, then require literal raw-byte equality.  Hence the
exact pinned P0 deterministically raises `P0 noncanonical bytes` before task198
authentication, dynamic import, base construction, or closure.

This is not an inferred runtime possibility.  It follows directly from the
last physical byte and key order versus the literal predicate.

### F2 — P0's declared self seal is stale

P0 declares
`406b333ee2acfd67e09a5cd43ba75abb03d7c4d4a80df14efc5ae70ed038fa18`.
An ordinal-key, ASCII, compact canonical reconstruction of the parsed object
after deleting `self_digest_sha256` gives
`3430a9ca7e2946299728d3b42e9cdd86d573a93e98b6b3c1ef74c5d63d03d77c`.
The reconstruction procedure was calibrated on the accepted task198 manifest,
where it reproduces the known seal
`0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684`
exactly.  Thus merely removing P0's newline/reordering it would reach a second
failure at producer lines 213--219/241 and checker lines 176--182/204.

### F3 — the driver's P0 pin has only 63 hex characters

Driver line 26 contains

```text
f8092796af77da3ea137908b1cca48db6563c412d937147bc341be29cc49489
```

and omits the final `f` of the physical 64-character SHA.  Lines 55--61 compare
this string with `HexSHA256(raw)`, so the driver always raises `pin drift` on
P0 before stale-output checks or Python launch.  This is independent of F1/F2.

The task359 reply's P0 self-seal and fail-closed-driver claims are therefore
false at the exact frozen bytes.

## 2. task198 authority and one-read semantics

Producer lines 277--288 and checker lines 241--251 collect every P0 path pin
and hash the corresponding physical owner.  Each side reads the 31,017,244-byte
receipt once into `raw_by_path`, calls `json.loads` once, extracts the exact
eleven-row ledger, and clears the authority byte map after authentication.  The
literal ledger and ten-to-eleven checks themselves are correct.

The required semantic authentication is incomplete, however.  Producer lines
295--382 and checker lines 281--348 do not require the following manifest links:

- `accepted_receipt_basename`;
- all fields of both `producer.member` and `checker.member`, including basename,
  bytes, and SHA;
- the manifest's producer/checker attestation metadata, including basename,
  bytes, and SHA; or
- the manifest's checker-verdict metadata, including basename, bytes, SHA,
  schema, terminal, and acceptance flags.

The adjacent physical attestation/verdict files are hashed and their contents
are checked, but that does not establish the omitted manifest-to-owner/member
edges required by task359 Section 4.

More importantly, the receipt evaluator contract is not decoded.  Each side
only tests that `section_cocycle` is a key of `evaluator.entry_points`
(producer lines 371--372; checker lines 339--340).  It does not require the
frozen evaluator schema, module, registry callable, runtime constructor, ten
coordinate widths, coordinate/relator digests, the six exact callable names and
argument lists, encoding, or multiplication/action/cocycle semantics.  This is
precisely the case excluded by the instruction that a raw SHA match does not
excuse failure to decode the exact evaluator ABI.

The implementation also transiently retains the 31-MB raw receipt, its parsed
DOM, and a second approximately 31-MB `canonical(receipt)` allocation during
raw equality.  In the checker, the new output receipt is read before the
task198 byte map is cleared.  Parsing is once per process, but the avoidable
second canonical byte copy and peak overlap violate the requested memory
discipline.

## 3. g760, task226, v302, and the three canaries

No independent defect was found by static inspection in these local formulas:

- Producer lines 563--572 and checker lines 525--534 independently encode
  `red(W2 (W3^-1 W2)^8)` and then `red(g616 y^36 x^-108)`, require lengths
  616/760, the frozen word digests, and exponent sums `[0,0]`.
- The actual task226 calls have current API shape.  The producer calls
  `specialize(g760, [], rows)` and reads its returned package/ABI; the checker
  calls `reconstruct(g760, [], rows)`, whose current independent API returns the
  ABI directly.
- The empty-correction checks require `f=g760`, `a=[]`, zero `B_a`, and equal
  base/corrected occurrence words and quotient values.  The separate retained
  full-package diagnostics are labelled `BASE_REFERENCE_ONLY`.
- Producer lines 601--623 and checker lines 537--558 locally rebuild
  `1-R_B(g760)` via their own Fox/endpoint implementations and compare it with
  task226's `bar_epsilon_1`.
- Producer lines 626--670 and checker lines 561--596 use authenticated ledger
  signs and independently evaluated substitutions.  Their residue rows are
  exactly H1 `[[6],[6],[6]]`, H2 `[[3],[3],[3]]`, and P
  `[[0,0,0,6],[0,6,6,0],[6,0,0,0],[0,0,3,3],[3,3,0,0]]`, with all three
  products/sums zero.  This agrees with v302's signed `-3/+3` tables modulo 9.
- Producer lines 761--776 and checker lines 669--683 form
  `[x,y]^3`, evaluate exponents 0, 1, 2 through the side-local task226 engine,
  require the same three target blocks, and attach the requested
  `PROJECTED_AREA_REPRESENTATIVE_ONLY` label.

These are code-shape findings only.  No digest, target, or canary value was
obtained by candidate execution.

## 4. v303 projection typing and seal failure

### F4 — the projected v216 ABI seal is computed over the old seal

Task226 returns a `full_abi` which already contains `self_digest_sha256`.
Both task359 `make_projection` implementations deep-copy it, update the
projection annotations, and then execute

```python
projected["self_digest_sha256"] = digest_obj(projected)
```

at producer lines 712--728 and checker lines 626--640.  The digest input thus
contains task226's **old** seal.  The assigned value is not the digest of the
new object with `self_digest_sha256` removed, which is the repository's seal
contract and the predicate at producer lines 819--824/checker lines 710--713.

Neither side validates the baseline projected seal.  The `ABI_seal_target`
mutation merely replaces the already-invalid seal with zeros and observes that
the mutant also fails.  It does not prove baseline acceptance.  Because both
wrappers repeat the same resealing algorithm, their equality is correlated and
does not repair the defect.

### F5 — the explicit interface is insufficient and is not what feeds closure

The separate `projected_a3_interface` at producer lines 673--710/checker lines
599--625 contains each `p_o/xi_o/w_o/u0_o` row, but omits all eleven marked
`q_o(x)` and `q_o(y)` maps.  Those maps determine the occurrence-dependent
actor action and are necessary to compute the invariant closure.  A generic
string saying `p_o conjugation followed by z0 action` does not bind them.

Conversely, the task227-shaped object named `projected` is a deep copy of the
entire task226 ABI.  It retains `literals`, `rword_f`, `B_a`, exact PB-chain
fields, and the other full-package data even while its separate interface says
`full_package_fields_excluded`.  Producer line 957 passes this full annotated
copy, not the explicit interface, to `t227.closure`.

Therefore the load-bearing v303 projection is neither sufficient to determine
the closure nor the sole closure input.  Labels do not establish the required
type separation.

## 5. task227 APIs, rosters, coefficients, and independence

The current producer call signatures are otherwise compatible:

- `t227.closure(projected, meter, structural=None)` matches task227 producer
  line 193;
- `t227.encode_gate(run)` matches line 222; and
- checker `t227.verify_gate(gate, projected, internal, "production")` matches
  the four-argument independent API at checker-engine line 185.

The producer engine's closure retains its occurrence basis and ancestry,
block basis/echelon/remainder, canonical 486 ideal rows, all 729 translates,
`c_i`, `lambda`, `kappa`, all four replay rows, quotient remainder, and either
the dual or MEMBER replay.  The independent task227 verifier reconstructs the
orbit, exact 486 and 729 rosters, compares occurrence and block spans both
ways, reconstructs echelon/coefficients, and checks MEMBER replay or all dual
pairings.  The wrapper preserves these objects in `gate`.  No missing current
API attribute or return-shape mismatch was found by inspection.

Producer Meter compatibility is narrowly sufficient for the frozen producer
engine: production `closure` calls only `budget.bump(...)` and reads no method
other than that in this route; the wrapper supplies `.bump`, `.used`, and all
keys called by the engine.  This does **not** make the resource claims sound,
as Section 7 explains.  The independent frozen verifier accepts no meter at
all.

Producer and checker import different pinned task226/task227 engines under
private names and share no new helper.  Their new authority, word, projection,
central, and mutation glue is nevertheless nearly line-for-line duplicated;
F1, F4, and F5 occur identically on both sides.  Thus helper non-sharing is
present, but the new wrapper layer has demonstrated correlated implementation
failure.

## 6. Glue mutation semantics

The twelve P0 roster names, one attempted mutation per name, changed-owner
digests, narrow `NarrowReject` catch, and uncaught wrapper
`MutationAccepted` pattern are present on both sides.  The sign, prefix, g760,
mode/task192, central H1/H2/P, area target, ABI seal, and conclusion owners are
all extant objects.

They are not an acceptance-quality mutation envelope:

- no baseline `cheap_validate` call is made before mutations;
- the load-bearing ABI baseline fails its own seal predicate (F4);
- the authority and central mutations mostly exercise equality of a copied
  fixture against another copy, not the actual authentication/replay call
  graph; and
- each record fills `expected_gate` from the caught observed exception rather
  than comparing against a separately preregistered reason owner.

The checker also does not require the producer result's complete
`false_conclusion_flags` object.  It checks six top-level flags and the
separate task192 mode, but never checks `actual_a3_numerator` in that result
object.  The cheap forbidden-flag fixture cannot substitute for an acceptance
path predicate.

## 7. Resource accounting and performance

### F6 — the independent closure verification is outside the meter

Checker-engine `verify_gate` lines 185--214 take no meter and internally:

- rebuild the orbit;
- construct the 486 ideal rows and 729 translates;
- rebuild the block echelon;
- replay coefficients/dual pairings; and
- perform twelve span-comparison calls.

The wrapper merely calls `meter.check` immediately before and after it
(checker lines 899--902).  There is no in-call wall interruption, RSS
enforcement, operation counter, closure-run counter, or roster counter.  If
the external `timeout` kills the verifier, it cannot emit a typed verdict.

The producer meter is also only partial.  `closure_runs` and
`closure_actions` are bumped by one wrapper call; `closure_actions` does not
count closure actions.  `occurrence_support` is never bumped.
`actor_operations` and `orbit_actions` are both bumped for the same low-level
q-multiplications, including structural arithmetic.  The checker leaves the
closure/run/rank/roster counters at zero.  Task226 base/area calls and dynamic
imports are counted only after completion.  Thus several cap names do not mean
what the reply claims.

RSS is sampled only by the final `snapshot`; no `setrlimit`, signal deadline,
or periodic check enforces the 6-GiB cap during a large allocation.  A snapshot
RSS stop recursively calls another snapshot while constructing UNKNOWN and can
escape without an output.

### F7 — reserve-before-allocation and serialization accounting are absent

Every authority/output file is read before its byte counter is bumped.  The
base and area ABI objects are built before their counts are bumped.  The full
receipt/verdict is canonicalized before `serialized_bytes` is bumped
(producer lines 922--931; checker lines 787--795).  Moreover the resource
snapshot is embedded and sealed before that bump (producer lines 912--918;
checker lines 798--821), so successful telemetry records zero rather than the
actual serialized output bytes.

The producer canonicalizes the whole receipt once to compute its self seal and
again to write it.  The checker does the same for its verdict.  The frozen
independent verifier's `compare_sparse_spans` already checks both directions
inside one call, yet line 198 invokes each pair again in reversed order.  It
rebuilds the same sparse bases and block-image lists repeatedly.  These are
avoidable hidden passes, not measured work.

If `serialized_bytes` exceeds its cap, the first bump leaves the meter above
cap; UNKNOWN publication calls the same writer and raises again.  `MemoryError`
is classified as `UNKNOWN_INPUT`, not resource exhaustion, and then attempts
another full canonicalization.  The stated “only typed UNKNOWN on a cap”
contract is therefore false.

The Luna reply gives the 21,600-second and 6-GiB caps, but no actual one-case
runtime estimate as requested.  The driver advertises a 43,200-second serial
worst case.  That bound is incompatible with the six-hour workflow ceiling
already observed in v220 delta38; each external timeout also equals, rather
than safely exceeds, the internal wall cap.  The accepted five-case task227
SELFTEST took 493 seconds, so a realistic one-case estimate should have been
derived and a workflow-safe internal/external margin preregistered instead of
using a twelve-hour serial envelope.

## 8. Fresh publication, shell quoting, and terminals

Initial driver stale-path checks and Python `xb` final-path opens are present.
They are not failure-atomic.  Both programs write directly to the final path,
not to an exclusively created temporary owner followed by a no-overwrite
publication.  If a write leaves a partial final file, or if the normal path
discovers a stale file, the UNKNOWN handler re-enters the same stale-output
rejection and escapes.  Disk-write `OSError` is not caught.  Thus neither
UNKNOWN path can safely publish after partial output.

The specifically requested shell quote at driver line 87 is correct by static
inspection.  It emits the shell word

```text
'"receipt_sha256":"'${rsha}'"'
```

whose adjacent quoted/unquoted parts expand to the fixed JSON substring
`"receipt_sha256":"<physical sha>"`.  Together with checker raw-byte hashing,
this would bind the post-check physical receipt against substitution.  Fixed
paths contain no shell metacharacters, and producer/checker execution is
serial.

Other terminal logic is not acceptable:

- F3 prevents the shell from being generated at all.
- Lines 76--91 admit MEMBER, NONMEMBER, `UNKNOWN_INPUT`, and
  `UNKNOWN_RESOURCE`, require only producer/checker equality, and lines 93--98
  then create the production sentinel and print `D359_DRIVER_PASS` for all four.
  This contradicts the preregistered non-accepting UNKNOWN semantics.
- Process exit zero is therefore not supplemented by an accepted-terminal
  predicate.  The terminal count and equality checks are necessary but not
  sufficient.

## 9. Effect on v220

This audit does not alter v220.  Delta39's accepted task227 SELFTEST envelope
remains accepted; F1--F7 are defects in the new task359 P0/wrappers/driver and
do not retract that frozen five-case implementation result.  Conversely,
task359 is statically rejected and unexecuted, so none of delta38/delta39's
three actual A3 milestones moves: actual task226 package **0**, actual
orbit/486/729 equality **0**, and actual MEMBER coefficient or NONMEMBER dual
**0**.  A3 therefore remains **0/3**.  No later A5--A9, B, C, W, or F
numerator moves, and no compatible/cofinal lift, fake certificate, or Ihara
witness follows.  The delta38 six-hour cancellation remains the relevant
warning against the present driver's twelve-hour serial envelope; it is not
negative mathematical evidence.

No edit to v220 is authorized or made by this reply.

## 10. Required repair boundary

A successor cannot preserve any of the present four new machine-owner hashes.
At minimum it must:

1. regenerate P0 as exact compact sorted ASCII with no newline, recompute its
   seal, bytes, and SHA, then refresh both Python pins and the full 64-character
   driver pin;
2. decode and cross-bind the complete task198 manifest member/attestation/
   verdict graph and exact evaluator ABI while retaining one parse;
3. define one sufficient v303 interface including all marked action maps,
   derive a pruned task227 ABI from only that projection, remove the old seal
   before resealing, and validate the unmutated baseline;
4. make the independent verifier interruptibly wall/RSS bounded despite its
   meter-free API, give counters honest meanings, reserve before every material
   allocation, and include serialization in sealed telemetry;
5. publish receipt/verdict failure-atomically and make UNKNOWN recovery safe
   after a partial attempt; and
6. make the driver distinguish accepted MEMBER/NONMEMBER from non-accepting
   UNKNOWN, with an external timeout margin and workflow-feasible bound.

Only a fresh static audit after those repairs may authorize GHA.  Only an
accepted producer plus independent-checker GHA artifact may change an actual
A3 numerator.

```text
STATIC TASK359 IMPLEMENTATION:         REJECT
FROZEN P0 / DRIVER ENTRY:              BLOCKED BY DETERMINISTIC PIN/CANONICAL FAILURES
V302 CENTRAL FORMULAS:                 NO ADDITIONAL STATIC DEFECT FOUND
PRE-A0 COMPUTATIONAL BASE FORMULAS:    NO ADDITIONAL STATIC DEFECT FOUND
V303 PROJECTION / ABI SEAL:            REJECT
ONE ACTUAL 486/729 CLOSURE ROUTE:      NOT REACHED / NOT ACCEPTABLE
INDEPENDENT MEMBER/DUAL CHECKER:       UNMETERED / NOT ACCEPTABLE
CHEAP GLUE MUTATIONS:                  REJECT (INVALID BASELINE)
SERIAL GHA DRIVER / P0:                REJECT
EXECUTION / GHA:                       UNEXECUTED
ACTUAL A3 NUMERATOR:                   remains 0/3; no numerator authorized
A0 COMMON / POINTED / EXACT PB:        OPEN
COFINAL LIFT / FAKE / IHARA:           NONE
```

`TASK361_R07_TASK359_PRE_A0_A3_CODE_PERFORMANCE_AUDIT_V1_REJECT`
