# Luna task 157ds — transactional relative-Frattini v4

## Role and objective

You are Luna.  Implement a **versioned, semantics-preserving v4** successor
to the frozen packed v3 search.  The v3 production run solved the former
hosted-runner/OOM problem and returned a cross-checked artifact, but stopped
on an artificial cumulative candidate-gradient cap before doing a deep sparse
search.  Preserve the frozen v2/v3 mathematical universe, checkpoint-major
order, literal predicate, and terminal meanings.  Change only candidate
lifetime and exact cheap-gate evaluation.

Frozen v3 references:

```text
search/d972_b345_relfrat3_v3.py
  df60849f9fa4bb6a09e0d23d799e31473960544728db6eb5507a6fd54749343b
search/check_d972_b345_relfrat3_v3.py
  11345a8db5ff6d08fa8395301c270532d0d96714cc8d77d98643dac04a6856cf
search/d972_b345_relfrat3_gha_driver_v3.g
  fe7a76191a484194696931c5acb59ec6ee0115af75d543613281c28e4d6a4d7a
```

Production evidence to bind in the reply:

```text
commit 84bea6176b29adab5e24e8595be71f7466e0cc3d
GHA selftest 32202347904: PASS
transport-only failure 32202487446: quotes stripped from CLI preamble; no search
full run 32202638830: workflow success, driver/checker PASS
artifact id/name/size 9348803701 / gap-run-out / 227111
receipt sha256 a8dd8c9d5938b9257f7585d31a904eb98505f88902bc767ec19486c55c697095
terminal B345_RELFRAT3_UNKNOWN_RESOURCE
reason compact_candidate_sparse_entries
runtime 2253.417311103 s
peak sampled RSS 288403456 bytes
checkpoint translations=8, columns=pivots=88, basis live entries=774
candidate cache size=3, candidate sparse entries=688932
element pool size=431843, packed payload=66503822 bytes
```

The receipt and independent checker agree.  This is not a mathematical
obstruction: `claim_classification=unknown_not_obstruction`.

## Authorized files

Create only:

```text
search/d972_b345_relfrat3_v4.py
search/check_d972_b345_relfrat3_v4.py
search/d972_b345_relfrat3_gha_driver_v4.g
sol/luna_reply_157ds_relfrat3_transactional_v4.md
```

Do not edit v1/v2/v3, q3 sources, workflows, existing receipts, or any other
file.  Temporary diagnostics must be outside the repository.

## Registered semantics that must not change

1. The 4,096 correction words and their exact first-seen BFS order.
2. The translation BFS order `+1..+6,-1..-6`.
3. Geometric checkpoints `1,2,4,...,32768`.
4. Checkpoint-major selection: at a checkpoint candidates are considered in
   registered correction-index order.  The first candidate certified at the
   earliest checkpoint wins exactly as in v2/v3.
5. All cheap/full quotient gates, normalized inverse fibre, target order,
   left-Fox convention, F3 row-space predicate, and literal acceptance gates.
6. PASS, SEARCH_INCOMPLETE, and UNKNOWN_RESOURCE meanings.  No bounded miss,
   skip, or cap is an obstruction/nonexistence claim.
7. The packed positive proof/independent streaming checker contract from v3.
8. Cache/transaction policy affects runtime only, never a group value, pivot,
   candidate result, selected pair, or terminal meaning.

Do not merely raise the one-million candidate-entry cap, retain a packed
global candidate cache, or spill global pool IDs to disk.  Those leave the
candidate-only element-pool growth intact and are outside this task.

## A. Exact fixed-context cheap-gate DP

The v3 full run spent 2,182.984 seconds before its first sparse checkpoint.
The 4,096 long words caused about 364 million PC cache hits.  Replace only this
repeated evaluation with an exact finite-image recurrence.

Extend the correction dictionary with lossless first-seen provenance:

```text
word[1] = identity
word[i] = reduce(word[parent[i]] + signed_seed[edge[i]])
```

Keep the existing reduced word array and dedup/order unchanged.  Independently
gate every parent index, edge, reduced reconstruction, exponent-zero property,
and E3-kernel property.

Enumerate the complete fixed list of two-generator E4 contexts used by
`cheap_candidate_bad`: the five correction/coface pairs, all candidate pairs
used by both hexagons, the five A.18 pentagon pairs, and the six pairs needed
to construct the source endomorphism.  Deduplicate contexts only by exact E4
pair value, with a lossless mapping back to each named use.

For each signed seed and fixed context, evaluate its E4 image once.  Propagate
the correction image in dictionary order by

```text
rho(c_i) = rho(c_parent) * rho(signed_seed)
rho(FIXED_WORD * c_i) = rho(FIXED_WORD) * rho(c_i).
```

Free reduction does not change the finite-group value.  Reconstruct the exact
same named cheap failures from these values.  Source PB4 relations remain
literal short-relator evaluation on the six source images.  This DP must not
replace the selected/full direct word replay: every candidate that reaches the
full lane is materialized from its registered word, and its direct quotient
gate result must equal the DP result before any Fox membership test.

The independent checker must reconstruct the parent/edge table, context
registry, seed images, propagated values, failure bitsets/counts/digests, and
the direct-vs-DP equality for every full-lane candidate.  It must not import
the producer or trust a producer signature.

Record at minimum:

- context count and exact named-use mapping digest;
- dictionary parent/edge/reconstruction digest;
- cheap candidates evaluated, survivor count, ordered survivor indices and
  digest, completion flag, and per-gate failure counts;
- direct replay count and all direct-vs-DP comparisons;
- PC cache hit/miss delta and runtime for the cheap phase.

Flush the completed survivor count/indices digest before sparse search.  If a
resource stop occurs earlier, record the exact evaluated prefix and current
candidate rather than losing it.

## B. Candidate-local transaction

Delete the cross-checkpoint `candidate_cache` of all gradients.  At each
geometric checkpoint, preserve the exact v3 candidate scheduling and process
one candidate at a time:

1. take an element-pool checkpoint and a provenance-DAG checkpoint before any
   candidate-specific inverse/source tuple or gradient is interned;
2. materialize/complete the candidate and hard-check direct cheap/full gates;
3. generate targets in the frozen order, **one target at a time**;
4. generate that target's packed Fox gradient and immediately call the same
   basis solve;
5. if it solves, retain only its proof-root node for the current transaction
   and continue to the next target;
6. on the first nonsolved target, record the exact missing pivot and roll the
   entire candidate transaction back;
7. only a candidate whose every target solves is selected.  Regenerate it and
   compare an exact canonical target/gradient/value binding before exporting
   the unchanged packed positive certificate.

The missing-pivot blocker is:

```text
(target ordinal, component, canonical E4 bytes)
```

The basis only gains pivot rows and never mutates an existing row.  Therefore,
after a failed fully reduced target, that candidate cannot become solvable
until a basis row with the exact missing pivot exists.  At later checkpoints:

- if the blocker element is absent from the persistent pool, or its packed
  `(component,id)` is not a basis pivot, skip recomputation exactly;
- once that exact pivot row appears, regenerate the candidate from its word
  and retry from target one.

The checker must verify this monotonic blocker theorem from the receipt's
checkpoint trace and exact pivot introductions.  A blocker is only a runtime
skip certificate; it never turns a candidate into a mathematical rejection at
the registered final cap.

## C. Exact pool/DAG rollback

Add an explicit candidate transaction to the v3 exact element pool.

- Snapshot the pool length before `complete_candidate` or any other
  candidate-only operation that can call `pool.intern`, not merely before the
  first Fox gradient.
- A failed candidate must roll the proof DAG back to its checkpoint.
- Delete every `ids` entry and canonical byte row in the pool suffix.
- Before any numeric ID is reused, clear the element product and inverse LRUs;
  no cache entry may refer to a deleted ID.
- Candidate gradient generation must not bind lazy BFS sections or mutate the
  sparse basis.  Assert both conditions around each rollback.
- Persistent basis rows, DAG leaves, translation BFS/SLP bindings, generators,
  inverse tuple certificate, and registry IDs must all predate and survive the
  candidate rollback unchanged.
- PC collector caches contain canonical coordinates rather than pool IDs and
  may remain bounded; document and gate this distinction.
- On PASS, commit only what the selected proof needs, then retain the existing
  selected-candidate regeneration and positive certificate checks.

Record transaction starts/commits/rollbacks, pool length/peak/suffix removed,
LRU clears, candidate target count, target gradients generated, early failures,
missing-pivot skips/retries, and per-candidate/peak transient sparse entries.
Use the existing pool/cap/RSS/wall guards.  A failure to rollback or a local
cap is UNKNOWN_RESOURCE.

## D. Receipt and terminal repair

The v3 global resource receipt correctly preserved bounded accounting but did
not include the already-computed cheap survivor ledger or current candidate.
Every v4 terminal, including an exception during candidate construction, must
contain a bounded search prefix with:

```text
cheap evaluated/completed/count/digest
current checkpoint, correction index, target ordinal/name
blocker table count/digest
transaction count/rollback count
basis/pool/DAG/section/cache accounting
precise cap and whether it was monitor or registered structural cap
```

Synchronize `resource_guards.hit_reason` with a non-monitor structural cap (or
provide a separately exact structural-cap field); do not emit `hit=true` with
an unexplained null reason.  The checker must reject an UNKNOWN branch that
claims obstruction or omits the exact evaluated prefix.

## E. Driver and GHA contract

Version the v3 driver.  Keep:

- q3 in one separate GAP child which exits before Python;
- exact q3 artifact/checker marker gates;
- `python3 -u`, `bash -o pipefail`, `tee`, sentinels, unique markers;
- stale artifact deletion;
- mandatory `with_pquot_packages=true` / `GAP_P2_PACKAGE_ROOT`;
- producer soft 300 minutes, workflow 330 minutes.

Pin v1/v2/v3 and all q3 inputs.  Do not edit the workflow.  In the reply,
state that parent dispatch must use `gh workflow run --json` (or an equivalent
byte-preserving API) for the quoted output-path preamble; run 32202487446 is a
transport-only negative example.

## F. Tests and freeze discipline

Run at most one lightweight combined differential selftest after the first
complete implementation.  It must cover:

1. dictionary parent/edge reconstruction and exact DP versus direct word
   evaluation for every item in a bounded deterministic toy dictionary;
2. all named cheap contexts and failure-bit equality;
3. streamed target solve versus v3 all-target solve on a toy basis;
4. missing-pivot skip before introduction and mandatory retry after exact pivot
   introduction;
5. pool suffix rollback, ID reuse only after both element LRUs clear, and
   unchanged persistent basis/DAG/SLP state;
6. PASS regeneration/canonical gradient binding;
7. all three terminals and a structural-cap UNKNOWN with exact prefix.

Do not run the full producer locally.  Do not run production GAP, Git, GHA, or
edit workflows.  If the single test exposes only a fixture error, report it
and request one corrective rerun.

## Reply contract

Write `sol/luna_reply_157ds_relfrat3_transactional_v4.md` with final hashes,
byte counts, exact v3-to-v4 invariant table, transaction/DP design, caps,
selftest result, source-only runtime estimate, and exact proposed GHA inputs.
Explicitly record the three v3 GHA runs and commit above.  Do not claim a v4
PASS before a new cross-checked production artifact, and do not claim global
B4-B.

Final token:

```text
B345_RELFRAT3_TRANSACTIONAL_V4_READY_FOR_GHA
```
