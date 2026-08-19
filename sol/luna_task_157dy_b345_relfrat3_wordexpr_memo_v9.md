# Luna task 157dy — B345 relative-Frattini WordExpr v9 memo/fusion accelerator

## 0. Role and immutability boundary

You are Luna. Implement a **versioned, semantics-preserving performance successor**
to the frozen v8 WordExpr/Fox lane.  The currently running v8 GHA job must not be
cancelled, modified, or used as an input checkpoint.

Frozen v8 sources:

- `search/d972_b345_relfrat3_wordexpr_v8.py`
  SHA256 `ea2c2901e316bfaa1c42d3f9966de5ec76323139728dfef46d2032608997e8db`
- `search/check_d972_b345_relfrat3_wordexpr_v8.py`
  SHA256 `9d3368504953862e688f474871e72cdc1ae4153e4737b8b6260ba260804db413`
- `search/d972_b345_relfrat3_wordexpr_gha_driver_v8.g`
  SHA256 `63e9a8dcc87c446fb130665dfe94c29cbe0836f1b87682f9b5ac4a7eb7c25018`

Transport calibration:

- apt-free canary `32246634125`, commit
  `8e206842f3892bf1eacc37035f74ef6da5ca3dd2`, PASS.
- full v8 `32247008986` is active when this task is issued.  Do not infer its
  outcome and do not touch it.

The only mathematical search allowed is the exact frozen v8 universe and order:
4096 registered candidates, index order 1 through 4096, operational first-PASS.
The 33 acceptance targets and 17 diagnostic-only targets remain exactly v8.

## 1. Authorized files

Create only these four new files:

1. `search/d972_b345_relfrat3_wordexpr_memo_v9.py`
2. `search/check_d972_b345_relfrat3_wordexpr_memo_v9.py`
3. `search/d972_b345_relfrat3_wordexpr_memo_gha_driver_v9.g`
4. `sol/luna_reply_157dy_b345_relfrat3_wordexpr_memo_v9.md`

Do not edit v1--v8, the workflow, frozen artifacts, prior replies, claims, or
the current GHA run.  No Git/GHA action; the parent is the sole broker.

## 2. Exact objective

Remove repeated evaluation of identical typed WordExpr subtrees without
changing any group value, Fox gradient, sparse membership answer, proof DAG,
candidate order, stopping rule, or terminal claim.

The static audit identified the load-bearing duplication:

- v8 `WordExprEvaluator.evaluate_gradients` rebuilds reachable ancestors and
  gradients from zero on each root call;
- candidate 1 runs the mandatory 50-root flat bridge separately;
- 23 S/ST/TS roots repeatedly traverse the same six source subtrees;
- acceptance membership re-evaluates target roots already computed by the
  bridge; and
- a PASS regenerates 33 roots once more for proof provenance.

v9 must compute an identical node/candidate binding once and reuse it where
sound.

## 3. Mandatory accelerator A — candidate-local typed gradient memo

Implement an exact candidate-local memo for WordExpr value/Fox-gradient
evaluation.

1. The key must bind the complete typed expression node identity, rank/arity,
   candidate binding, quotient/presentation identity, and leaf bindings.  A
   coincidentally equal E4 value is **not** a valid key: equal group values can
   have different Fox derivatives.
2. PRODUCT, INVERSE, SUBSTITUTE, negative-prefix orientation, and ordinary
   left-Fox conventions remain byte-for-byte/definitionally the v8 rules.
3. Pin the six source roots as candidate-local anchors.  Fixed literal leaves
   and fixed inverse/T-side data may be shared across candidates only when the
   complete typed binding is independent of the candidate; prove and gate that
   independence rather than assuming it.
4. Failed-candidate candidate-dependent entries are discarded at the existing
   transaction boundary.  Never retain pool IDs, proof-node IDs, or candidate
   suffix state across rollback.
5. Use a deterministic bounded LRU/entry policy.  Eviction changes performance
   only: an evicted entry is recomputed exactly.  Cache exhaustion must not
   become a mathematical terminal or candidate rejection.
6. Account for working plus cached sparse entries and RSS.  Keep the frozen
   global RSS/resource fail-closed guards.  Register cache entry/gradient
   limits explicitly; target an additional cache budget no larger than 512 MiB.
7. Receipt performance data must include hit/miss/eviction counts, peak cached
   sparse entries, pinned-source count, and per-phase elapsed times.  These are
   diagnostics, not acceptance predicates.

## 4. Mandatory accelerator B — bridge/membership fusion

For candidate 1, preserve and evaluate all frozen 50 bridge canaries in their
original order.  No canary may be dropped or relabelled.

1. Reuse their exact already-computed value/gradient records when the
   corresponding acceptance target enters sparse membership.
2. If target 6 gives the first missing pivot, record it exactly, continue the
   remaining bridge canaries as v8 requires, and do not evaluate target 6 a
   second time merely to rediscover the same vector.
3. Candidate 1 flat-vs-WordExpr differential equality remains a production-path
   gate for all 33 acceptance and 17 diagnostic roots.
4. On a prospective PASS, run the provenance-enabled solve with the same
   gradient bindings and demand equality with the membership-only result.
   Produce the same lossless mathematical proof payload as v8.  Cache records
   are never accepted as proof by themselves.
5. The independent checker reconstructs all selected values/gradients and the
   proof as before.  It may retain the slower recomputation route; it must not
   import producer code or trust producer cache statistics.

## 5. Mandatory progress visibility

The driver already uses unbuffered Python and `pipefail | tee`.  Add flushed,
bounded progress records at least every 10 seconds and at phase/candidate/target
boundaries.  Include:

- phase, candidate index, target ordinal/name/component;
- WordExpr node count and source-anchor progress;
- cache hits/misses/evictions and live/pinned sparse entries;
- pivot/blocker status, pool suffix, RSS, and elapsed seconds.

Progress output is operational only.  It must not enter canonical receipt
digests or acceptance decisions.  Never print secrets or unbounded vectors.

## 6. Explicit non-features

- Do not reorder candidates and do not add W-FORM-first.  T-53 preregistration
  and D29-FRZ require the neutral frozen order.
- Do not claim a negative result, full mathematical universe, obstruction, or
  cofinal/global B4-B result.
- Do not add candidate sharding in v9.  A future sound shard merge would require
  contiguous ranges and complete non-PASS coverage below a selected index; a
  first-returned PASS is invalid.
- Do not grow the Gaussian basis with candidate targets.  The frozen basis is
  immutable and shared read-only across sequential candidates.
- Do not add disk checkpoint/resume, imported state, or v8 receipt state.
- Do not apply UU to the left-Fox complex.  Do not add FC-22 here.
- T-54 integer linking/mod-3^k prefilter is diagnostic-only in this registered
  universe: all 4096 candidates already have exact F2 exponent sums `[0,0]`, so
  it cannot reduce the scan.  Recompute this as a canary if useful, but do not
  advertise a speedup from it.
- FC-21/SR-1 requires a separate exact YES receipt and is out of v9 scope.

## 7. Schema, terminals, and differential guarantees

Use a new v9 schema, paths, markers, and source pins.  Preserve the v8 terminal
semantics and exact four-way terminal set.  Nonpositive terminals remain
`unknown_not_obstruction`; cache eviction is not a resource reason.

Add frozen semantic-difference gates:

1. dictionary candidate order/digest equals v8;
2. source-tuple preflight equals v8;
3. all candidate-1 33/17 value and Fox gradients agree between the v8-style
   cold evaluator and memo/fusion evaluator;
4. at least one nontrivial shared-source toy and one inverse/substitution toy
   exercise cache hit, miss, eviction, rollback/ID reuse, and recomputation;
5. a forged cache key, cross-candidate reuse, equal-value/different-expression
   alias, wrong negative-prefix orientation, dropped bridge canary, diagnostic
   promotion, acceptance demotion, and changed candidate order are rejected;
6. selected PASS proof is independently regenerated and all roots replay.

The checker must use helper-independent implementations for receipt decoding,
WordExpr/Fox replay, sparse membership/proof replay, and terminal validation.

## 8. Driver and tests

The thin GAP driver must preserve the v8/q3 chain of fixed SHA pins, run q3 in a
separate child as v8 does, delete exact stale paths before execution, use
`python3 -u` under `bash -o pipefail ... | tee`, create exit-zero sentinels only
after success, and require exactly one registered terminal marker.

One combined lightweight producer/checker selftest is authorized after the
static audit.  If it fails only in a fixture before production logic, document
the exact failure and request one corrective run; do not loop tests.  No full
local search, GAP production calculation, Git, GHA, or workflow edit.

## 9. Required reply

Report:

- all four SHA256/byte counts and exact ready marker;
- exact v8-to-v9 semantic diff and proof that candidate/target order is fixed;
- cold-vs-memo differential selftest result;
- cache caps/accounting, progress cadence, and source-only runtime/RSS estimate;
- all known limitations and result-dependent use:
  PASS = v8/v9 existence only, nonpositive = no obstruction;
- confirmation that the active v8 run and all v1--v8 files were untouched.

End the reply with exactly:

`B345_RELFRAT3_WORDEXPR_MEMO_V9_READY_FOR_GHA`
