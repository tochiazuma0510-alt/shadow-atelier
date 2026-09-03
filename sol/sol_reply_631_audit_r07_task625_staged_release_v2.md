# Sol(max) Task631 reply: independent static audit of Task625 staged release v2

## Verdict

`PASS_AFTER_REPAIR`.

The staged mathematics, the retained Task622 route, and the independent
checker are sound on this snapshot.  I found no sign, word-order,
topological-order, physical-replay, 8,059-offer, or claim-boundary
counterexample.  Four finite resource/performance defects remain, however.
They are directly on the production path and must be repaired before launch.
They do not require a new framework or any mathematical change.

**Launch is prohibited for the audited hashes.**  Apply only R1--R4 below and
submit the resulting exact quartet to the same static re-audit.  This verdict
does not authorize production or GHA.

This is a static/code verdict, not a computed selected payload or a
cross-check.  `verified=false`.

## Exact input binding

All requested inputs were read completely.  Their current byte streams are:

| input | bytes | SHA-256 |
|---|---:|---|
| Task631 | 3,034 | `ee36ac8617f6a3ee109646e0e55041b950a19a7868c81ad18ac926231216fc73` |
| v2 producer | 71,954 | `c3b7d53accb8b0814049cae4e1cadebc905941031b156dd12763ac2072219cf0` |
| v2 checker | 101,254 | `33dd8cf7fdc94c971e58a09211e5acbf749980dfc49109f3bf51db4495d46002` |
| v2 workflow | 6,077 | `35682ef40110d15199ddc5e17300b25e17d44bd414d59d2346bca86fbf95f653` |
| Task625 Luna reply | 7,968 | `b3872695fb287841c5d4078471fdadc076c6a3c6eac45e0656c626e3f79b7b17` |
| repaired theorem v475 | 8,253 | `757ffab5aa011643efa3df4b133dc03d423895d57a003ed6830a47528388148e` |
| Task628 reply | 9,721 | `09c2d5defc272ddd18e0e300879e6860ba7ffd8e876ecc81adc26b7d20ab126a` |
| Task629 reply | 4,103 | `581a6242bb2f584d04c298594a361695bc91271ab0a9791677273c941c3dea90` |
| Task625 kickoff | 6,177 | `d3918ac3b4b522c485d9749b9657b131c1609694378e08455f80e44a8614d858` |
| Task622 reply | 8,106 | `4eaf1f92f4ef1fdd0a7f3289175d7c8b97c5ac85714b0b368d4aa66a20f151e0` |
| accepted v1 producer | 47,935 | `cfd581f8a71176f9252555a94028a8482ede862ee3430098270109e52fa0d3ff` |
| accepted v1 checker | 71,637 | `09ee815345e9ad2cfd80799a5bf7daf4446cda0eb3d8bc79bd7b3d9c61fa86c8` |
| accepted v1 workflow | 5,497 | `7f1b59790d2092fd93035742510ce7232834b4f7ea0a470507a408100d2e39cd` |
| pinned v3 producer | 138,202 | `bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff` |

The four primary v2 hashes and all frozen v1/v475 parent hashes match the
Task631/Task625 declarations exactly.

## Correctness audit

### C1. Task622 invariants survive: PASS

The candidate/source authentication, packed `NodeView`/`EdgeView`/`RowView`
formats, online cursors, selected-source replay, compact-leaf codec, and the
later standalone independent transcript router retain the Task622-accepted
logic.  In particular:

- the lower-first transcript still consumes exactly 8,059 logical objects,
  including every all-zero old-lower offer;
- the preliminary selected replay uses only `declared_lower`, while the later
  authoritative reroute checks all 1,661 lower and all 5,044 grade pivots;
- the fixed offer counts 2,014/6,398, ranks 1,661/5,044, 3,317 MEMBER
  coefficients, zero remainder, basis equation, physical origin/link data,
  and terminal cursor exhaustion remain gated;
- the checker reuses the authenticated packed basis view rather than copying
  or rebuilding it for each row; and
- the roots filename is explicitly tied to `files["roots"]["file"]`, and its
  semantic contents and receipt digest cannot silently refer to different
  files.

No full 8,059-object local route was run in this audit.

### C2. Actual staged DAG and schedule: PASS

The executable order is exactly

```text
G decreasing; L decreasing; B_0,...,B_3 each decreasing;
all D in canonical origin order; O_0,...,O_3 each decreasing; leaves.
```

The concrete edge constructors reproduce the v1 recurrence:

- `G` emits its scaled old/block origin, scaled negative lower links, and
  scaled negative earlier-grade reductions;
- `L` emits its scaled old origin and scaled negative earlier-lower
  reductions;
- `B` emits the four signed pure-Q1 defect terms or its actor parent, plus
  scaled negative reductions;
- `D` emits its seed leaves or transition actor word, plus the negative old
  expression; and
- `O` emits projected-seed leaves or its actor parent, plus scaled negative
  reductions.

Every destination is required to have a strictly greater schedule position.
Reduction and actor edges additionally authenticate `target_pivot <
source_pivot`.  Thus every predecessor has finished before a node is popped,
and no released accumulator can receive a late contribution.  Root insertion
does not increment `state_edge_traversals`.

### C3. Coefficients and exact words: PASS

All coefficients are accumulated modulo three with zero deletion, including
coefficient `2=-1`.  Edge scalars and all minus signs agree with v1.  Actor
words are multiplied as `red(Pq)`, left to right.  Equality is exact freely
reduced signed-tuple equality: neither a quotient endpoint, endpoint
signature, seed, hash alone, nor transient path ID merges words.  Producer
IDs are injectively backed by exact tuples, and the literal receipt emits the
tuple, not the ID.  The checker instead keeps exact tuples directly and
byte-compares its independently encoded complete leaf stream.

### C4. Independence and statistics: PASS

The checker does not import the producer, its scheduler, or its word
interner.  It reconstructs the graph and schedule through separate local
code, checks the selected graph and compact leaves, releases those large
objects, and then performs the independent physical reroute.

`expanded_states` is incremented once per nonzero `(node,path)` in the popped
node map.  `state_edge_traversals` is incremented once per outgoing edge for
each such state, with roots excluded, exactly as repaired in v475.  The
checker compares all deterministic counters.  Stage and total wall/RSS/peak
RSS/durable observations are schema- and cap-checked but deliberately omitted
from the equality projection, so serial-process observations are not compared
as deterministic data.

### C5. Sealing, workflow, and claims: PASS subject to R4

The producer writes only into a process-specific staging directory and uses
`os.replace` only after all receipts and the manifest exist.  All caught cap
and memory terminals remove staging and return `UNKNOWN_RESOURCE`; neither a
partial payload nor a mathematical negative result is published.

The workflow pins the producer, checker, Task625 reply, v3, and v475 hashes,
the exact Task554/Task595 parents and candidate commit.  Actions are immutable
SHA-pinned.  The inert trigger is
`[fire-grade1-selected-slp-staged-v2]`; producer and checker are serial; the
payload/verdict artifact is success-only after the checker marker; logs are
always requested.  `ulimit -v 8388608`, the 7-GiB RSS cap, 45-minute command
timeouts, and 60-minute job boundary are coherent with the Task625 envelope.
The 60-minute job bound is intentionally stricter than the sum of both
per-process maxima; exceeding it yields no promoted artifact, not a negative
answer.

## Load-bearing finite repairs

### R1. Reuse one checked edge batch per reached node

Both schedulers first perform the required harmless streaming validation of
all static edges.  But during expansion the producer calls `edges_for(node)`
and `checked_edge` inside the loop over every path in that node; the checker
does the same with `edge_iterator`/`audit_edge`.  Consequently a node with
`N_v` exact paths regenerates and revalidates its complete edge list `N_v`
times in addition to the global scan.  Edge propagation itself must occur
`N_v` times, but Python descriptor construction and invariant validation do
not.

Minimal repair: retain the global streaming prevalidation.  For each reached
node only, locally materialize and check its outgoing descriptors once before
the path loop, reuse that local batch for every path, and release it
immediately after the node.  Apply this independently in producer and
checker.  Do **not** retain a global Python tuple cache of the roughly
multi-million-edge graph; added live memory must be only `O(max node degree)`.
The traversal counters must continue to count `N_v * degree(v)`.

### R2. Remove the producer's full final leaf-map duplicate

The producer keeps `leaves[(seed,path_id)]` and, while that full dictionary
and both interning containers are still live, constructs a second full
`leaf_map[(seed,paths[path_id])]` by comprehension.  Up to the configured
two-million-state boundary this is a needless large retained duplicate.

Minimal repair: when a literal is reached, key the terminal accumulator
directly by `(seed, paths[path_id])`, reusing the already interned tuple
object.  Return/serialize that dictionary directly and remove the terminal
comprehension.  Node accumulators may and should continue to use compact path
IDs.  Leaf counts, cancellation, tuple authority, sorting, and bytes must be
unchanged.

### R3. Remove the canonical-product double tuple formation

On every nonempty suffix, the producer currently tupleizes the list returned
by the pinned `v3.floor.wm` and then `exact_word` tupleizes it again.  The
checker similarly creates a canonical tuple in its local `word_mul` and then
copies that tuple in `normalize_word`.  This is repeated on the hot
state-edge path; the old real run observed paths up to length 21, so it is not
merely setup work.

Minimal repair: form each reduced product tuple once.  On the producer side,
pass the reducer's list to the existing validating interner for the sole tuple
formation.  On the checker side, use a narrowly scoped insertion path only
for the tuple returned by its own local `word_mul`, reuse that tuple, and
retain the length cap and exact-path set accounting.  Raw roots and edge
suffixes must still receive full alphabet/free-reduction validation.  Do not
weaken exact-word equality or share this helper between executables.

### R4. Count `manifest.json` in the producer durable cap

The producer presently computes `durable` from `files` and checks it before
constructing/writing `manifest.json`.  The checker correctly computes
`len(manifest_raw) + sum(receipt bytes)`.  Hence the concrete boundary
`sum(receipt bytes) = cap`, with any nonempty manifest, passes the producer
check and publishes a payload over its declared cap; the checker then rejects
it as `manifest_receipts`.  This contradicts the advertised producer durable
boundary even though atomic sealing prevents a partial artifact.

Minimal repair: serialize the manifest once, set final durable bytes to the
receipt sum plus that serialized length, apply `resource_fail("durable_cap")`
before `os.replace`, write those same serialized bytes, and report the final
total in the payload-sealed telemetry.  No manifest self-reference or schema
expansion is needed.

## Performance verdict

Subject to R1--R3, the performance design is acceptable and has no
load-bearing asymptotic regression.  I found no dense boundary closure, no
full root-to-leaf path replay, no expansion of a released state, no repeated
8,059-row reconstruction inside the selected evaluator, no new large NumPy
copy, and no selftest/diagnostic work on the production branch.  The complete
static edge prevalidation is a necessary linear pass and should remain.
Packed row/edge streams and their zero-copy views, selected-only preliminary
replay, block lifetime separation, and later one-time full independent reroute
remain intact.

## Bounded fixtures and adversarial probes

No production data was evaluated.  The permitted serial commands returned
exit zero:

```text
python -B search/d972_r07_a0_grade1_selected_slp_v2.py --selftest
  fixture=PASS; staged fixtures=9; expanded=13; traversals=13;
  maximum_live=3; resource caps rejected=5

python -B search/check_d972_r07_a0_grade1_selected_slp_v2.py --selftest
  all retained cursor/leaf/claim fixtures PASS;
  staged fixtures=9; expanded=13; traversals=13;
  maximum_live=3; resource caps rejected=5;
  statistics_projection=PASS
```

An additional in-memory one-node/two-exact-path probe used the actual
production scheduler functions.  Each node had one literal edge.  Both
schedulers returned two leaves, `expanded_states=2`, and
`state_edge_traversals=2`, but each invoked its edge provider three times:
one global validation plus once for each path.  This is the finite witness for
R1; after repair it must be two calls (global validation plus one node-local
batch) while the traversal counter remains two.

The shipped fixtures establish the algebraic cases (diamond cancellation,
late third contribution, actor-boundary cancellation, coefficient two,
distinct exact words, invalid arrows/cycle, and resource terminals), but they
do not discharge R1--R4 because their toy sizes do not exercise the retained
copy/edge-regeneration or final-manifest boundary.

## Claim boundary

The false-claim gates remain false in both manifest and roots:

```text
direct_occurrence_replay = false
next_degree2_residual    = null
cross_checked            = false
verified                 = false
A0 / COMMON / FAKE / IHARA = false
```

This audit produced no selected-SLP payload, fresh rho2, next-grade decision,
cross-check numerator, A0 result, common/cofinal lift, fake witness, Ihara
counterexample, or Lean verification.  Run `33723160379` remains
`UNKNOWN_RESOURCE:time`; nothing here reclassifies it.

```text
STAGED MATHEMATICS / ROUTING:       PASS
INDEPENDENT CHECKER:                PASS
DETERMINISTIC COUNTERS:             PASS
PERFORMANCE / DURABLE BOUNDARY:     PASS_AFTER_REPAIR (R1--R4)
PRODUCTION OR GHA LAUNCH:           PROHIBITED ON AUDITED HASHES
verified:                           false
OVERALL:                            PASS_AFTER_REPAIR
```

`R07_TASK625_STAGED_RELEASE_V2_STATIC_PASS_AFTER_REPAIR`
