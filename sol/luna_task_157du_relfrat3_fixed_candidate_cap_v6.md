# Luna task 157du — fixed-candidate cap-calibrated v6

## Role and objective

You are Luna.  Implement a versioned **resource-cap-only** successor to the
frozen fixed-candidate v5.  The cross-checked v5 production run reached the
registered sparse-entry cap with low RSS before the fixed blocker pivot
appeared.  Raise exactly the two caps required to reach the already registered
32,768-translation bound.  Preserve every mathematical predicate, word,
candidate, translation, pivot, retry, certificate, terminal, and claim meaning.

Frozen v5 sources:

```text
search/d972_b345_relfrat3_fixed_candidate_v5.py
  e4675906601714ee16219d747cf95ffef54b19e354228dd6e7d3cd99d59127ea
search/check_d972_b345_relfrat3_fixed_candidate_v5.py
  0cb7e0173fe022f304010c64ef89b7200464f4ad8c1e1bc7c3ad4001ffe12246
search/d972_b345_relfrat3_fixed_candidate_gha_driver_v5.g
  3bcb19326bfff1e313870a64cca95840b0e581aa1f7c713ee18300faf149261d
```

Cross-checked production evidence:

```text
commit 6b8a93a6d77187dacdb69c17226bcf3354ba62bb
canary run 32211875374: PASS
canary artifact 9351149748 / 1570 bytes
canary archive sha256 bf7d4dd184454490d2277f6e9eb3989facb73eba7ddda9547a5f2a55c50d83bb

full run 32212335985: workflow/driver/independent checker PASS
artifact 9351317721 / gap-run-out / 48716 bytes
archive sha256 be02babfe2c7219ef9ea16946b077a319e7942aee8aa4b055e3f9e4816afc8ff
receipt sha256 c9231ebb8fe65c47107556c6e06873fa68b74e148e1ab248cfada08a699975d4
terminal B345_RELFRAT3_FIXED_CANDIDATE_UNKNOWN_RESOURCE
reason total_sparse_group_ring_keys
producer runtime 193.037337425 s
peak RSS 296407040 bytes
```

Exact stop prefix:

```text
translations       10809
columns             118894
pivots              118893
live sparse entries 999999
element pool        330011
section SLP nodes   32768
DAG nodes/edges     218739 / 157480
blocker pivot       absent
candidate attempts/rollbacks/commits 1 / 1 / 0
```

The fixed candidate's blocker was reconstructed at checkpoint 1 as target 6,
`hexagon_1_coface_0`, component 4, and remained absent at every geometric
checkpoint through 8,192.  This is not nonmembership or an obstruction.

## Authorized files

Create only:

```text
search/d972_b345_relfrat3_fixed_candidate_v6.py
search/check_d972_b345_relfrat3_fixed_candidate_v6.py
search/d972_b345_relfrat3_fixed_candidate_gha_driver_v6.g
sol/luna_reply_157du_relfrat3_fixed_candidate_cap_v6.md
```

Do not edit v1--v5, q3 sources, workflows, receipts, or any other file.
Temporary diagnostics belong outside the repository.

## A. Exact cap delta

Version v5 and change exactly these mathematical-runtime constants in both
producer and independent checker:

```text
CAPS["total_sparse_group_ring_keys"]: 1_000_000 -> 4_194_304
CAPS["element_pool"]:                 1_000_000 -> 2_000_000
```

Keep every other cap byte-for-byte equal to v5, including:

```text
translations per relator 32768
sparse pivot rows 1000000
DAG nodes/edges 2000000/4000000
section SLP nodes 65536
single word/section 100000
RSS 4831838208 bytes
producer soft wall 18000 s
workflow wall 330 min
```

Changing `element_pool` also changes the integer stride used only as an
injective pair key in the bounded product cache.  Explicitly selftest that the
new stride is injective over valid IDs and that cache hits/evictions do not
alter multiplication.  Pivot order remains `(component, canonical E4 bytes)`,
never numeric insertion ID or pair-cache key.

Do not increase a third cap preemptively.  Any later registered cap remains an
honest `B345_RELFRAT3_FIXED_CANDIDATE_UNKNOWN_RESOURCE` with the exact prefix.

## B. Semantics and active route must be unchanged

Retain the v5 registered universe exactly:

```text
kind=fixed_positive_candidate
correction_indices=[1]
correction_word=[]
full_4096_universe_claimed=false
earliest_global_candidate_claimed=false
negative_completeness_claimed=false
m=0, lambda=1, frozen row37/exponent2 outside roof
```

The active run must remain a fresh same-job reconstruction.  The v5 artifact
does not serialize the persistent basis/DAG and must not be used as a resume
checkpoint.  Recompute the checkpoint-1 blocker from q3/source data; do not
read or pin its canonical bytes from the v5 receipt.  Ordinal/name/component
remain post-reconstruction drift canaries only.

Preserve without semantic edits:

- fixed-candidate direct preflight and all 50 literal targets;
- normalized inverse fibre and the 100,000 flat-word cap;
- left-Fox convention and quotient identities;
- translation BFS `+1..+6,-1..-6` and checkpoints 1..32768;
- canonical byte pivot order, sparse elimination, blocker monotonicity;
- retry only after the exact pivot introduction;
- pool/DAG transaction, rollback, and LRU clearing;
- packed reachable-DAG PASS certificate and independent streaming replay;
- all three v5 terminal meanings and fixed/non-global claim boundary.

No dictionary/4,096-candidate DP, omitted-candidate scan, PB5, ANUPQ, resume,
or checkpoint serialization may be introduced.

## C. Cap-calibration receipt and checker

Version schema/output/progress/driver names to v6.  Pin the three v5 source
hashes above.  Add a compact exact `cap_calibration` record containing:

```text
source_run=32212335985
source_receipt_sha256=c9231ebb8fe65c47107556c6e06873fa68b74e148e1ab248cfada08a699975d4
source_stop_reason=total_sparse_group_ring_keys
source_translations=10809
source_live_sparse_entries=999999
source_element_pool=330011
source_peak_RSS=296407040
old/new sparse cap=1000000/4194304
old/new pool cap=1000000/2000000
semantics_changed=false
resume_used=false
```

The checker must require exact top-level/schema/key sets, reconstruct all v5
mathematics independently, validate the cap delta and record, and reject any
change to other caps, registered universe, terminal claims, search order, or
certificate semantics.  It must not import producer code or trust producer
digests as equality.

On a new UNKNOWN, preserve the exact bounded prefix and cap synchronization.
On INCOMPLETE, require all 32,768 translations.  On PASS, perform the full v5
regeneration and packed-DAG replay.  Nonpositive receipts must retain exactly:

```text
claim_classification=unknown_not_obstruction
claim_scope=fixed_candidate_only
no_mathematical_obstruction_claimed=true
```

## D. Performance accounting

The measured late growth projects approximately:

```text
at 32768 translations:
  live sparse entries ~3.03 million
  pivots              ~360 thousand
  element pool        ~0.98 million
  DAG nodes/edges     ~0.66m / 0.48m
  section nodes       32768 (already saturated by BFS registration)
```

Therefore the two new caps provide headroom while the 4.5-GiB RSS guard stays
load-bearing.  Record the new peak/cap ratios and phase timings.  Keep live
progress at every geometric checkpoint and at most every 30 seconds.

Source-only expectation is producer 4--7 minutes and full job/checker 7--12
minutes if no PASS serialization occurs; conservatively allow 45 minutes for
a deep PASS replay.  These are estimates, not proof claims.

## E. Driver and dispatch

Version the v5 driver and retain exact q3 separate-child teardown,
`with_pquot_packages=true`, source SHA gates, stale purge, `python3 -u`,
`pipefail|tee`, exit sentinels, unique terminal/checker markers, and artifact
SHA.  Pin v1--v5.  Do not edit the workflow.

Proposed full dispatch:

```yaml
script: search/d972_b345_relfrat3_fixed_candidate_gha_driver_v6.g
preamble: 'D972_B345_RELFRAT3_FIXED_CANDIDATE_V6_RUN:=true;; D972_B345_RELFRAT3_FIXED_CANDIDATE_V6_OUTPUT:="ci/out/d972_b345_relfrat3_fixed_candidate_v6.json";;'
out_dir: ci/out
timeout_min: '330'
with_pquot_packages: true
```

Parent will use the byte-preserving JSON dispatch route.

## F. Test and freeze discipline

Run at most one lightweight combined differential selftest after the complete
implementation.  It must prove:

1. the only semantic-runtime changes from v5 are the two cap values;
2. all other cap values and the fixed registered universe are identical;
3. the new pool pair-key stride is injective and cache-neutral;
4. an exact toy prefix stopped by the old sparse cap continues under the new
   cap without changing pivots/values/order;
5. v5 blocker skip/retry, rollback, PASS, INCOMPLETE, UNKNOWN, claim-mutation,
   and packed-DAG fixtures still pass/reject identically;
6. cap-calibration field mutations are rejected.

Do not run the full producer locally.  Do not run production GAP, Git, GHA,
or edit workflows.  If the sole test exposes only a fixture error, report it
and request one corrective rerun.

## Reply contract

In `sol/luna_reply_157du_relfrat3_fixed_candidate_cap_v6.md`, report exact
source hashes/bytes, the two-value cap diff, selftest result, static v5/v6
semantic-diff audit, driver pins, estimates, and proposed GHA inputs.  State
explicitly that this is a cap calibration only, that no resume was used, and
that no nonpositive/global conclusion is strengthened.

End with exactly:

```text
B345_RELFRAT3_FIXED_CANDIDATE_CAP_V6_READY_FOR_GHA
```
