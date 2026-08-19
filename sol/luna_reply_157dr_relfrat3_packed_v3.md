# Luna reply 157dr — packed relative-Frattini v3

Date: 2026-08-19

## Verdict

The versioned v3 producer, independent checker, and same-job driver are
implemented.  They preserve the frozen v2 mathematical universe, candidate
order, literal gates, sparse row space, and terminal meanings while replacing
the memory-heavy representations that caused both v2 hosted runners to die at
about 121 minutes without an artifact.

No v1/v2/q3 source, workflow, or existing receipt was changed.  No production
GAP, full producer, Git, GHA, or dispatch was run.

## Frozen inputs

All pins were recomputed from the working-tree bytes before freeze:

```text
q3 producer  b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755
q3 checker   ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73
q3 driver    c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831

v1 producer  4b73fbfe19bb33a9decdec5fda437f58f61a3ecb1989090bd08151f60ce6609e
v1 checker   3d86240237229b250943c4795c24c32ac75af9229534c73d16bd838f6d6d0101
v1 driver    fce9b3ba8c9b686fb6af2bd5a6da1b29f7486616948a6907982af14cd5d8738b

v2 producer  fad364043926dbdc03e56accf089f454d625e0b315c98a7647bc891677313cc8
v2 checker   3c8967bea6946b42cef08cd097eab4e9071aae203ee27ac38038c4d5adb83f07
v2 driver    006e33e97c6f9ac1982887206c904dbcf423c95790ec2fe0c45d9a1b3a2e38aa

q3 artifact  3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72
formula      b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef
```

The driver regenerates that q3 artifact and independently checks it in the
same job; it does not rely on a stale workspace copy.

## Exact v2-to-v3 semantic invariants

The following remain unchanged:

1. the 4,096-word correction dictionary and its registered order;
2. empty-correction-first candidate priority, cheap/full gates, and the
   normalized exponent-seven complete 27-fibre inverse;
3. translation BFS order `+1..+6,-1..-6` and geometric checkpoints
   `1,2,4,...`;
4. the left Fox convention, the eleven PB4 relator columns, the F3 row-space
   membership predicate, and all charming/hexagon/pentagon/onto literal gates;
5. the canonical pivot order `(component,EKey)`.  Stable element IDs are not
   used as an order surrogate;
6. the first positive candidate and the meaning of
   `B345_RELFRAT3_LITERAL_PAIR_PASS`;
7. a bounded miss is only `B345_RELFRAT3_SEARCH_INCOMPLETE`, while a local or
   global resource skip is `B345_RELFRAT3_UNKNOWN_RESOURCE`; neither is an
   obstruction or nonexistence claim;
8. cache capacity and eviction can affect runtime only, never a quotient
   value, row space, search order, candidate, or terminal.

The v3 receipt binds the frozen v2 trio as its semantic reference and the v1
trio as the underlying predicate/search-order reference.

## Packed implementation

### Exact quotient-element pool

Every persistent E4 value is interned by the exact immutable concatenation of
its 144-point zero-based permutation bytes and its PC-coordinate bytes.
Equality is byte equality, never digest equality.  Stable zero-based IDs are
used in hot sparse keys, BFS state, DAG leaves, inverse-cache keys, and compact
candidate gradients.  Pivot comparison expands an ID to its canonical bytes,
so its order is exactly the v2 tuple order.  A positive boundary maps every
internal ID to a one-based external registry row, and the checker independently
re-evaluates each registry section to its actual permutation/PC element and
rejects duplicate actual elements.

### Bounded arithmetic caches and lazy sections

The v2 arbitrary-full-token `PcCollector.cache` is absent from the active v3
path.  Each PC collector has only bounded exact pair-product and inverse LRUs;
the element pool likewise has bounded product and inverse LRUs.  Evictions are
semantics-neutral and fully counted.

The translation BFS stores a parent SLP node and one signed generator letter.
It preserves first-seen shortlex order and free cancellation.  Full section
words are materialized only for reachable PASS leaves, then evaluated back to
the exact pooled element before serialization.

Candidate cache entries contain only the correction index, target names and
kinds, packed gradients, and quotient-value IDs.  They contain no section map
or retained candidate word.  On PASS, the selected candidate is regenerated,
all packed gradients/values are compared exactly, and only then are its
certificate sections built.  A candidate removed after a local resource stop
also decrements the recorded live sparse-entry count.

### Packed provenance certificate

The in-memory proof DAG uses parallel typed arrays for node kind, relator,
translation ID, edge offset/length, parent ID, and F3 coefficient.  Failed
columns and failed candidate solves roll back transactionally.  A positive
receipt serializes only the union reachable from its roots as versioned
little-endian typed arrays in canonical base64.  Every array binds its type,
typecode, item size, logical length, byte length, cap, and SHA-256.  No
per-node JSON dict/list expansion is performed.

Reachability construction, array conversion, and base64 construction each
reserve/check RSS headroom.  If the compact certificate cannot be formed
under the guard, the result is honest `UNKNOWN_RESOURCE` rather than an
uncertified PASS.

The checker has an independent decoder and arithmetic implementation.  It
checks canonical base64 and every per-array SHA, rejects malformed IDs,
forward references and unreachable inserted nodes, reconstructs actual leaf
translations from independently checked registry sections, and replays every
translated Fox column and F3 linear node.  Its topological evaluator maintains
future-use counts and deletes a parent vector immediately after its last use;
it therefore does not recreate v2's all-node `dict[id,vector]` memory tail.
Only root vectors survive for comparison with independently reconstructed
literal residuals.

## Caps and accounting

The exact frozen/search and v3 resource caps are:

| item | cap |
|---|---:|
| small representation dimension | 64 |
| correction dictionary | 4,096 |
| translations per relator | 32,768 |
| live sparse group-ring keys | 1,000,000 |
| sparse pivot rows | 1,000,000 |
| provenance DAG nodes / edges | 2,000,000 / 4,000,000 |
| single word or section length | 100,000 |
| affine residual dimension / explicit candidates | 12 / 531,441 |
| element pool | 1,000,000 |
| element product / inverse LRU | 262,144 / 65,536 |
| PC pair-product / inverse LRU, per collector | 65,536 / 16,384 |
| lazy section SLP nodes | 65,536 |
| compact candidate entries / sparse entries | 4,096 / 1,000,000 |
| producer wall / RSS soft guard | 18,000 s / 4,831,838,208 bytes (4.5 GiB) |
| progress interval | at most 30 s |

The receipt records pool capacity/size/peak/packed width/payload bytes,
hit/miss counts, equality and canonical-order contracts, and an ordered
payload binding digest.  Every LRU records capacity, live size, peak, hits,
misses, and evictions.  It also records lazy SLP live/peak/bound counts; basis
columns, dependent columns, pivots, live entries, maximum supports, and
elimination count; live/peak DAG nodes/edges and packed payload bytes;
candidate-cache size/live sparse entries; inverse-cache tuple hit/miss counts;
and monitor check count, last phase, current/peak RSS, and exact stop reason.

Progress is flushed at powers of two and at least every 30 seconds with the
required translations/columns/pivots/sparse/pool/DAG/candidate/PC-cache and RSS
fields.  On a global guard, the producer snapshots bounded accounting, clears
the basis, DAG, candidate cache, SLP, element pool and arithmetic caches, runs
GC, and only then writes an `UNKNOWN_RESOURCE` receipt.  There is deliberately
no checkpoint/resume in v3.

## Process isolation and proposed GHA input

The driver removes all stale q3/v3 artifacts, logs, scripts, hashes, and
sentinels.  It writes and verifies a fixed q3 child script, launches q3 in a
separate GAP process, and requires GAP 4.16.0 plus `smallgrp`, `autpgrp`,
`anupq`, and `json`.  The child exits before Python starts.  The outer process
then requires the exact q3 artifact SHA, the q3 checker sentinel, and exactly
one `B345_Q3_CHECKER_PASS` marker.  Producer/checker run unbuffered through
`bash -o pipefail` plus `tee`; a success sentinel is written only after the
pipe exits zero.  Terminal and checker PASS markers are also required exactly
once.

Proposed `gap-run.yml` dispatch inputs (not dispatched here):

```yaml
script: search/d972_b345_relfrat3_gha_driver_v3.g
preamble: 'D972_B345_RELFRAT3_V3_RUN:=true;; D972_B345_RELFRAT3_V3_OUTPUT:="ci/out/d972_b345_relfrat3_v3.json";;'
out_dir: ci/out
timeout_min: '330'
with_pquot_packages: true
```

`with_pquot_packages=true` is mandatory: the separate q3 child consumes
`GAP_P2_PACKAGE_ROOT` and loads the four packages above.  With the input false,
`${GAP_P2_PACKAGE_ROOT:?}` intentionally stops the child before any producer
run.  This is fail-closed, not a supported reduced mode.

## Single differential selftest

The one authorized combined lightweight selftest was run once:

```text
python -B search/d972_b345_relfrat3_v3.py --self-test
python -B search/check_d972_b345_relfrat3_v3.py --self-test
```

It passed with these exact markers:

```text
D972_B345_RELFRAT3_V3_PRODUCER_SELFTEST_PASS relevant_formula_sha256=5b66299d255964ff8afa9e9d75e9a5d61d767fd76539fd3c6ae94acd65039127 interning=1 pc_cache_differential=1 bfs_differential=1 packed_basis_checkpoints=1 packed_DAG_rollback=1 RSS_UNKNOWN=1 terminal_mutations=3
D972_B345_RELFRAT3_V3_CHECKER_SELFTEST_PASS mutations=16 fox_orientation_canaries=2 packed_DAG_canaries=10 streaming_parent_release=1
```

The sealed-positive fixture traverses the production packed encoder/decoder,
independent leaf resolver, streaming node replay, and root comparison.  The
mutations cover packed-array type/length/SHA/base64 drift, bad references and
reachability, section/element collisions, cache/accounting drift, RSS UNKNOWN,
and all terminal branches.  T-52's future known-positive control is recorded
for a future negative lane; this positive-semidecision v3 makes no negative
claim and is not blocked by it.

After that sole selftest, only static checks were run: both Python ASTs parse;
all nine frozen source pins match; driver source pins match the final producer
and checker bytes; the driver is ASCII and its shell quoting, stale deletion,
package-root gate, `pipefail`, `tee`, sentinels, and marker counts are present;
and all three code files have no trailing whitespace, conflict marker, or
missing final newline.

A final hostile audit found one checker-only attribute-connection typo in the
pool-width accounting gate: checker `Quotient` exposes its PC collector as
`collector`, not producer-side `pc`.  The expression is now
`e4.degree + e4.collector.n`.  This changes no receipt, predicate, search, or
producer byte.  The already-consumed single-selftest allowance was not reused;
the repaired checker was instead AST-parsed, every remaining `.pc` occurrence
was statically audited, and the new checker SHA was repinned in the driver.

## Parent GHA execution record

The parent Sol broker committed and pushed this frozen bundle as
`84bea6176b29adab5e24e8595be71f7466e0cc3d` on
`sol/b345-q3-chief-v1`.

1. GHA selftest run
   [32202347904](https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/32202347904)
   completed successfully.  The producer selftest marker, checker selftest
   marker, and `B345_RELFRAT3_PACKED_V3_GHA_DRIVER_PASS mode=selftest` each
   occurred exactly once.  Optional p-quotient packages were enabled and the
   pinned ANUPQ/JSON package build/load path passed.
2. Run
   [32202487446](https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/32202487446)
   failed before reading the fixed output path because the CLI field form
   stripped the GAP string quotes from the preamble.  Its logged value was
   `D972_B345_RELFRAT3_V3_OUTPUT:=ci/out/d972_b345_relfrat3_v3.json`, and GAP
   stopped at undefined variable `ci`.  It did not enter q3 or the search and
   is transport evidence only.  Subsequent full dispatches must use the JSON
   input path (or another byte-preserving API) for quoted GAP strings.
3. Full run
   [32202638830](https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/32202638830)
   completed the workflow successfully in 38m54s.  Artifact
   `gap-run-out` has id `9348803701` and archived size 227,111 bytes.  The
   producer receipt and independent checker agree on SHA-256
   `a8dd8c9d5938b9257f7585d31a904eb98505f88902bc767ec19486c55c697095`.
   The q3 checker marker, relative-Frattini checker marker, and full driver
   marker each occurred exactly once.

The cross-checked terminal is
`B345_RELFRAT3_UNKNOWN_RESOURCE`, with
`claim_classification=unknown_not_obstruction` and precise reason
`compact_candidate_sparse_entries`.  This is not a mathematical obstruction.
At the stop, the producer had used 2,253.417311103 seconds and sampled peak RSS
of only 288,403,456 bytes.  The basis had 8 translations, 88 columns/pivots,
and 774 live sparse entries; the packed DAG had 184 nodes/150 edges.  Three
retained candidate gradients already contained 688,932 sparse entries, and
the fourth candidate would exceed the registered cumulative one-million
candidate-entry cap.  The exact element pool was 431,843 elements (66,503,822
packed payload bytes), well below both the pool and RSS caps.

The live log also isolates the dominant pre-search cost: 2,182.984 seconds
elapsed before the first sparse checkpoint, with about 364 million PC-cache
hits from reevaluating all 4,096 long correction words.  Thus v3 achieved its
primary operational goal--it replaced the former unrecorded runner/OOM loss
with a fast, atomic, independently checked UNKNOWN receipt--and exposed two
separate semantics-neutral v4 targets: fixed-context parent/seed propagation
for the cheap gates, and candidate-local streamed gradient transactions rather
than cumulative cross-checkpoint gradient retention.

## Source-only performance estimate and residual risk

This is an estimate, not a production benchmark.  The q3 regeneration and
cross-check should remain on the order of tens of seconds.  Based on the two
v2 deaths near 121 minutes and the removed full-word cache, copied section
maps, object-heavy DAG, and all-node checker vectors, a v3 full producer is
budgeted at roughly 45–180 minutes and about 1.5–4.5 GiB RSS; a positive
checker is budgeted at roughly 5–60 minutes depending on reachable-DAG size.
The hard operational expectation is only that v3 returns an artifact before
the 4.5 GiB/300-minute soft guards, not that it must finish positively.

Sparse Gaussian fill-in can still exhaust the registered sparse, DAG, pool,
RSS, or wall caps.  Such an outcome is intentionally a cross-checkable
`UNKNOWN_RESOURCE`.  The two v2 runs left no reusable artifact/checkpoint, so
v3 starts from the frozen q3 receipt and cannot resume v2.

## Final files

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_b345_relfrat3_v3.py` | 158,867 | `df60849f9fa4bb6a09e0d23d799e31473960544728db6eb5507a6fd54749343b` |
| `search/check_d972_b345_relfrat3_v3.py` | 94,677 | `11345a8db5ff6d08fa8395301c270532d0d96714cc8d77d98643dac04a6856cf` |
| `search/d972_b345_relfrat3_gha_driver_v3.g` | 9,792 | `fe7a76191a484194696931c5acb59ec6ee0115af75d543613281c28e4d6a4d7a` |
| `sol/luna_reply_157dr_relfrat3_packed_v3.md` | REPLY_BYTES=016123 | final file SHA-256 is returned after close in the completion message |

The reply cannot contain its own ordinary file SHA-256 without changing the
bytes being hashed; its exact final byte count is fixed above and its exact
file hash is returned alongside this frozen reply.

This v3 changes representation and resource behavior only.  It remains a
direct PB3/PB4 relative-Frattini positive semidecision, does not prove any
bounded miss is an obstruction, does not supply deeper/cofinal iteration, and
does not by itself establish global B4-B.

`B345_RELFRAT3_PACKED_V3_READY_FOR_GHA`
