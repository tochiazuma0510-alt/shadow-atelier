# Luna reply 157ds — transactional relative-Frattini v4

Date: 2026-08-19

## Verdict

The versioned v4 producer, independent checker, and same-job GHA driver are
implemented and statically frozen.  The v4 lane preserves the registered v2/v3
mathematical universe and search order while replacing both measured v3
bottlenecks:

1. fixed-context cheap gates are evaluated by an exact parent/edge recurrence;
2. full candidate gradients live only inside an exact pool/DAG transaction and
   are streamed target-by-target.

The one authorized combined lightweight selftest passed.  No production GAP,
full producer, Git, GHA, or workflow dispatch was run.  No v1/v2/v3, q3,
workflow, or existing receipt file was changed.

This is an implementation-ready result only.  There is no v4 production
artifact yet, hence no v4 PASS, obstruction, or global B4-B claim.

## Frozen v3 evidence and reason for v4

The reply binds the frozen v3 bundle and its parent execution record:

```text
commit                         84bea6176b29adab5e24e8595be71f7466e0cc3d
GHA selftest                   32202347904 — PASS
transport-only failure        32202487446 — quoted preamble stripped; no search
full cross-checked run         32202638830 — workflow/driver/checker PASS
artifact                      9348803701 / gap-run-out / 227111 bytes
receipt SHA-256                a8dd8c9d5938b9257f7585d31a904eb98505f88902bc767ec19486c55c697095
terminal                       B345_RELFRAT3_UNKNOWN_RESOURCE
reason                         compact_candidate_sparse_entries
claim classification           unknown_not_obstruction
producer runtime               2253.417311103 s
peak sampled RSS               288403456 bytes
translations                   8
basis columns/pivots/live       88 / 88 / 774
candidate cache/entries         3 / 688932
element pool/payload            431843 / 66503822 bytes
```

The v3 checker agreed with that receipt.  The stop is not mathematical.  The
cheap preparation alone consumed 2182.984 seconds and about 364 million PC
cache hits; afterward three persistent candidate gradients accumulated
688,932 sparse entries and the next candidate would cross the registered
cumulative cap.  These two independently measured costs are exactly the two
representation-only targets repaired in v4.

## First cross-checked v4 production run

The parent broker committed and ran this frozen v4 bundle as
`e7a69c5517b7f83f155622e66578b899324bc4ed`.  Canary run
[32208843272](https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/32208843272)
passed with the producer, checker, and driver markers each occurring exactly
once.  Its artifact `gap-run-out` has id `9350090673`, reported size 2,184
bytes, and archive SHA-256
`09a5f420b5aca529d728fe110ca0ea782bb3ee1480de314fe980af40b5fcdbbe`.

Full GHA run
[32209072242](https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/32209072242)
completed the workflow successfully; the independent checker passed.  Artifact
`gap-run-out` has id `9350213499`, reported size 242,201 bytes, and archive
SHA-256 `dbf774a26d0f881d23102efec460d97da1016bc5b7b9eaaf4557741ad63aacff`.
The receipt is 14,523,463 bytes with SHA-256
`b35f69ec7584c98f7dba92d7e50e33ea4639e2526824b0815631e201871128e5`.

The cross-checked terminal is `B345_RELFRAT3_UNKNOWN_RESOURCE`, precise reason
`single_word_or_section_length`, with producer runtime 176.6198 seconds and
peak sampled RSS 175,161,344 bytes.  The fixed-context DP completed all 4,096
candidates and all 4,096 survived.  Candidate 1 reached target 6 at checkpoint
1, recorded an exact missing-pivot blocker, and was correctly skipped at
checkpoints 2, 4, and 8.  At checkpoint 8, candidate 2 passed its direct cheap
replay and hit the word/section representation cap before target 1
(`target_ordinal=null` in the bounded prefix).  At the stop the basis had 88
pivots and 774 live entries, the element pool had 306 elements, and the exact
transaction ledger had two starts and two rollbacks.

Thus the v4 DP, blocker, transaction, rollback, bounded-UNKNOWN receipt, and
independent-checker contracts all worked in production.  This terminal is a
representation-bound UNKNOWN, not an obstruction or global B4-A/B result.

Frozen v3 source pins retained by both the receipt contract and driver are:

```text
producer  df60849f9fa4bb6a09e0d23d799e31473960544728db6eb5507a6fd54749343b
checker   11345a8db5ff6d08fa8395301c270532d0d96714cc8d77d98643dac04a6856cf
driver    fe7a76191a484194696931c5acb59ec6ee0115af75d543613281c28e4d6a4d7a
```

## Exact v3-to-v4 invariant table

| Registered item | v4 status |
|---|---|
| 4,096 correction words | unchanged, including exact first-seen BFS order |
| Correction translation generators | unchanged order `+1..+6,-1..-6` |
| Sparse checkpoints | unchanged geometric order `1,2,4,...,32768` |
| Candidate scheduling | unchanged checkpoint-major, then correction-index order |
| Empty-correction priority and complete normalized inverse fibre | unchanged |
| Cheap and full finite-quotient gates | unchanged values and failure meanings |
| Source PB4 relators | unchanged literal evaluation on six source images |
| Target order and left-Fox convention | unchanged |
| Sparse F3 row space and canonical pivot order | unchanged |
| Literal charming/hexagon/pentagon/onto acceptance | unchanged |
| Selected pair | earliest fully certified pair under the same registered order |
| `LITERAL_PAIR_PASS` | unchanged positive meaning |
| `SEARCH_INCOMPLETE` | bounded miss only; never obstruction |
| `UNKNOWN_RESOURCE` | exact resource stop only; never obstruction |
| Packed positive certificate/checker | v3 contract retained |

The new DP, transaction, cache, and blocker policy can change runtime and
memory only.  They cannot change a group value, pivot, row space, candidate,
selection order, or terminal meaning.

## Exact fixed-context DP

The correction dictionary now records, losslessly, the parent index and signed
seed edge of every first-seen reduced word.  The producer independently gates
the reconstruction

```text
word[i] = reduce(word[parent[i]] + signed_seed[edge[i]])
```

as well as exponent-zero and E3-kernel conditions.  It registers every named
two-generator E4 context used by the five correction cofaces, both hexagons,
the five ordered A.18 pentagon uses, and the six source-endomorphism images.
The current exact registry has 46 named uses and deduplicates only by complete
E4 pair value.  Its mapping and order are digest-bound.

Each signed seed is evaluated once in each exact context.  Correction images
are propagated in dictionary order, and the old cheap gate bitsets are rebuilt
from those finite values.  The receipt includes dictionary provenance,
context registry, per-gate counts/bitsets, evaluated prefix, ordered survivor
indices/digest, completion flag, PC-cache delta, and cheap-phase runtime.

This recurrence does not replace a full check.  Every candidate entering the
sparse lane is materialized from its registered word and directly replayed in
all required quotient contexts; the direct result must equal the DP result
before any Fox solve.  The checker independently reconstructs the dictionary,
contexts, seed values, recurrence, bitsets, survivor ledger, and every direct
comparison without importing producer code.

If a resource guard fires during cheap evaluation, the receipt carries an
incremental evaluated-prefix digest, survivor-prefix digest/count, and current
candidate.  No incomplete cheap ledger is silently presented as complete.

## Candidate-local transaction and exact blockers

The active v4 path has no persistent candidate-gradient cache:

```text
persistent_candidate_gradient_entries = 0
```

At each checkpoint, one scheduled candidate is processed at a time.  The
element-pool and proof-DAG snapshots are taken before `complete_candidate` and
before any candidate-specific inverse/source tuple can intern an element.
Targets are generated and solved one at a time in frozen order.  Solved targets
retain only their proof roots inside the current transaction.

On the first nonsolved target the producer records the exact blocker

```text
(target ordinal, component, canonical E4 bytes)
```

and rolls the complete candidate suffix back.  At later checkpoints the
candidate is skipped only while that exact element/pivot is absent; the exact
pivot introduction forces a retry.  The checker binds the ordered
`(checkpoint,candidate_index)` direct-comparison pairs to the transaction
events, checks canonical blocker byte width, validates skip booleans, and
proves that every retry follows the matching pivot introduction.  A blocker is
only a monotone runtime certificate; it never becomes a rejection at the final
cap.

## Pool/DAG rollback and bounded receipt

A failed transaction deletes every candidate-only pool byte row and reverse-ID
entry and rolls the proof DAG to its snapshot.  Before any numeric pool ID can
be reused, both pool-ID product/inverse LRUs are cleared.  Persistent basis
rows, DAG leaves, translation SLP, generator/inverse IDs, registry anchors, and
source-tuple anchors are checked byte-for-byte across rollback.  PC collector
caches may survive because they contain canonical PC coordinates, not pool
IDs.  Candidate gradient construction is also checked not to bind lazy
sections or mutate the sparse basis.

On PASS, only the selected transaction is committed.  The candidate is then
regenerated and its canonical target/gradient/value binding is compared before
the unchanged packed certificate is exported.

Every terminal receipt carries a bounded search prefix containing the cheap
evaluated/completed ledger and digests, current checkpoint/candidate/target,
blocker count/digest, transaction/rollback counts, basis/pool/DAG/SLP/cache
accounting, and exact monitor or structural-cap reason.  A structural
`ResourceStop` is synchronized with `resource_guards.hit_reason`.  The checker
rejects an UNKNOWN receipt with a missing prefix, null reason, or obstruction
claim.

## Caps and accounting

| Item | Cap |
|---|---:|
| correction dictionary | 4,096 |
| translations per relator | 32,768 |
| live sparse group-ring keys | 1,000,000 |
| sparse pivot rows | 1,000,000 |
| provenance DAG nodes / edges | 2,000,000 / 4,000,000 |
| single word or section length | 100,000 |
| element pool | 1,000,000 |
| element product / inverse LRU | 262,144 / 65,536 |
| PC pair-product / inverse LRU | 65,536 / 16,384 |
| lazy section SLP nodes | 65,536 |
| persistent candidate gradient entries | **0** |
| blocker table | 4,096 |
| transaction trace records | 100,000 |
| exact cheap contexts | 64 |
| producer soft wall / RSS | 18,000 s / 4,831,838,208 bytes |
| progress interval | at most 30 s |

The receipt additionally records transaction starts/commits/rollbacks,
candidate target counts, generated gradients, early failures, blocker
skips/retries, transient sparse peaks, pool suffix deletions, and LRU clears.
Any failure of rollback or any registered local/global cap yields
`B345_RELFRAT3_UNKNOWN_RESOURCE`.

## Single combined differential selftest

The sole authorized combined lightweight selftest was run once:

```powershell
python -u -B search/d972_b345_relfrat3_v4.py --self-test
python -u -B search/check_d972_b345_relfrat3_v4.py --self-test
```

It completed in about 0.6 seconds and emitted both PASS markers.  The producer
marker bound formula SHA-256
`5b66299d255964ff8afa9e9d75e9a5d61d767fd76539fd3c6ae94acd65039127`
and reported:

```text
cheap_DP_direct=4
named_contexts=46
streamed_vs_v3=1
missing_pivot_retry=1
transaction_rollback_ID_reuse=1
PASS_regeneration=1
packed_DAG_rollback=1
RSS_UNKNOWN=1
terminals=3
structural_UNKNOWN=1
```

The checker reported `mutations=19`, `cheap_DP_direct=4`,
`named_contexts=46`, `prefix_UNKNOWN=1`, `blocker_skip_retry=1`, and
`streaming_parent_release=1`.  The deterministic cheap-DP fixture evaluated
four items with one survivor and survivor digest
`080a9ed428559ef602668b4c00f114f1a11c3f6b02a435f0bdc154578e4d7f22`.

The test covers parent/edge reconstruction, DP/direct equality, all named
contexts and failure bits, streamed versus all-target solving, blocker skip
and mandatory retry, complete pool/DAG rollback and safe ID reuse, selected
regeneration, all three terminal types, and a structural-cap UNKNOWN with an
exact prefix.  No second selftest was run.  Afterward only static pin,
placeholder, scope, whitespace/conflict, and diff checks were used.

## Driver and exact proposed GHA inputs

The driver deletes stale q3/v4 artifacts, logs, SHA files, child scripts, and
sentinels.  It runs the pinned q3 producer/checker once in a separate GAP child
and requires that child to exit before Python starts.  It then requires the
exact q3 artifact SHA and unique q3 checker marker.  Producer and checker use
`python3 -u` under `bash -o pipefail` with `tee`; each success sentinel is
written only after the pipe exits zero.  Exactly one producer terminal and one
independent checker PASS marker are mandatory.

`with_pquot_packages=true` is required.  The q3 child loads `smallgrp`,
`autpgrp`, `anupq`, and `json` through `GAP_P2_PACKAGE_ROOT`; a false/missing
input intentionally fails closed before the producer.

Proposed `gap-run.yml` dispatch inputs, not dispatched here:

```yaml
script: search/d972_b345_relfrat3_gha_driver_v4.g
preamble: 'D972_B345_RELFRAT3_V4_RUN:=true;; D972_B345_RELFRAT3_V4_OUTPUT:="ci/out/d972_b345_relfrat3_v4.json";;'
out_dir: ci/out
timeout_min: '330'
with_pquot_packages: true
```

The parent broker must use `gh workflow run --json` or an equivalent
byte-preserving API for this quoted preamble.  Run 32202487446 proves that the
CLI field form can strip the embedded GAP string quotes and fail before any
mathematics runs.

## Source-only runtime estimate

This is not a production benchmark.  The same-job q3 regeneration/check is
expected to remain on the order of 13 seconds.  The 364-million-hit v3 cheap
phase is replaced by at most 4,096 dictionary steps across at most 64 exact
contexts plus one-time signed-seed evaluations, so the cheap stage should be
seconds to a few minutes rather than about 36 minutes.  Candidate gradient
memory is now transient and rolled back, so it no longer grows cumulatively
across checkpoints.

The sparse basis itself can still grow to the unchanged one-million-entry,
pool, DAG, RSS, or 300-minute guard.  Consequently the full wall time remains
unknown and may use the complete 300-minute producer budget.  Such a stop is
an independently checkable `UNKNOWN_RESOURCE`, not evidence for nonexistence.
There is no reusable v3 search checkpoint; v4 restarts from the regenerated
frozen q3 receipt.

## Final files

| File | Bytes | SHA-256 |
|---|---:|---|
| `search/d972_b345_relfrat3_v4.py` | 197,022 | `ff2e021647fdaf84697c91f741f2d039575036bc1f389d9dc59dee512e6ca7e1` |
| `search/check_d972_b345_relfrat3_v4.py` | 145,016 | `54308d8628cd434bbc6a4522fe86296d72d01b42de8db2bc72ea9a6961157c2b` |
| `search/d972_b345_relfrat3_gha_driver_v4.g` | 11,134 | `b717b6a214913d26207ba4683bbe0403123d5139b5aa45cd7bba62be2b885d56` |
| `sol/luna_reply_157ds_relfrat3_transactional_v4.md` | reported after close | reported after close |

The reply cannot contain its own ordinary SHA-256 without changing the bytes;
its exact final byte count and SHA-256 are returned in the completion message.

`B345_RELFRAT3_TRANSACTIONAL_V4_READY_FOR_GHA`
