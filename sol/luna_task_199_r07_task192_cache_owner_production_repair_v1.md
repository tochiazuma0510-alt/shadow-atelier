# Luna task 199 - task192 production cache-owner repair v1

Commissioner: Sol / 2026-08-28

Reply to the existing task192 report:
`sol/luna_reply_192_r07_normalized_exact_cached_colgen_v3.md`.

Role: bounded mechanical repair and adversarial static audit only.  Do not
run Python, GAP, Node, git, GHA, or network locally.  Parent Sol owns every
execution and repository operation.  Edit only the same five task192 files:

```text
search/d972_r07_normalized_exact_common_word_cached_v3.py
crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py
search/d972_r07_normalized_exact_common_word_cached_gha_driver_v3.g
search/certs/d972_r07_normalized_exact_common_word_cached_selftest_v3_20260827.json
sol/luna_reply_192_r07_normalized_exact_cached_colgen_v3.md
```

Do not alter task179/task186, workflow files, proofs, or any other file.

## 1. Authenticated failure

GHA PRODUCTION run `33106084328`, head
`f38bd00d689a4fdb1f83d9ef89da16896a3d5631`, ran for about 2h02m and failed
before a receipt or checker artifact.  The exact traceback is:

```text
PositiveSearch.run -> initial_basis -> add_column
search/d972_r07_normalized_exact_common_word_cached_v3.py:2122 in add
self.cache.clear()
AttributeError: 'PositiveSearch' object has no attribute 'cache'
```

There are no uploaded artifacts.  This is an implementation STOP, not
`UNKNOWN_RESOURCE`, nonmembership, or evidence against an explicit word.

## 2. Required ownership repair

The monkey-patched object at that line is `PositiveSearch`.  Its rank-
dependent caches are owned below `self.fibres`:

1. `self.fibres._v3_values` is the bounded candidate-value cache and owns its
   basis epoch; and
2. `self.fibres.cache` is the predecessor canonical-selector dictionary used
   by the patched `FibreOracle.canonical`.

On every retained-rank change, atomically:

```text
self.fibres._v3_values.invalidate_basis()
self.fibres.cache.clear()
```

or perform the exactly equivalent operation through one explicit helper.
Never access or create `PositiveSearch.cache`.  Do not clear the Fox template
or boundary-descriptor caches: their keys/data are dual-independent.  Require
the two intended owners to exist before the first initial-boundary rank
increase and fail hard on an ownership/programming error.

Audit every rank-increase path, including the 15 calls made by
`initial_basis`, resumed-column replay, and later ACTIVE additions.  There
must be one invalidation per actual increase, no invalidation for a dependent
or failed insertion, and no stale canonical-selector value after an epoch
change.

## 3. Load-bearing SELFTEST repair

The previous SELFTEST did not execute the production monkey-patched `add`
path; its `production_path_selftest` invoked the unpatched authenticated v1
method.  Add a bounded test which reaches the exact v3 rank-change hook on a
production-shaped `PositiveSearch`/`FibreOracle` object and proves:

1. the first initial-basis-like insertion raises rank without
   `AttributeError`;
2. candidate basis epoch increases exactly once;
3. the bounded candidate cache and `self.fibres.cache` are both cleared;
4. the Fox and boundary caches are retained;
5. a non-rank-changing control does not invalidate;
6. a second rank increase repeats the same ownership transition; and
7. the historical owner mutation `PositiveSearch.cache` is rejected.

Route this through the actual helper used by production, not a duplicated
side model.  The independent checker must reconstruct and bind this
production-path trace and its mutation.  Update exact schemas/keysets only if
necessary; no cache evidence may weaken the mathematical v2 replay gates.

Also search the complete producer/checker for any other attribute whose
declared owner differs from the object on which it is accessed.  Record the
audit in the reply even if none are found.

## 4. Failure closure and delivery

Programming exceptions must remain hard nonzero STOPs and must never be
translated to `UNKNOWN_RESOURCE`.  Preserve the full v2 schedule,
normalization, literal replay, chunk/resume, exactification, and checker
semantics.  No cap widening is authorized merely because the failed run spent
two hours before reaching the bug.

Refresh all exact pins and the driver.  The driver remains ASCII-only, has no
self-SHA pin, rejects stale outputs, and requires exact-one producer/checker
markers.  Update the reply with this run's authenticated classification, the
repair, SELFTEST coverage, final identities, and conservative rerun estimate.

End with:

```text
RUN 33106084328:                         IMPLEMENTATION STOP / NO RECEIPT
POSITIVESEARCH CACHE OWNER:              REPAIRED STATICALLY
PRODUCTION RANK-CHANGE HOOK SELFTEST:     NOT EXECUTED BY LUNA
CACHED NORMALIZED FIRST-EDGE WORD:        NOT OBTAINED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:   NOT DECLARED
```

`TASK199_TASK192_CACHE_OWNER_PRODUCTION_REPAIR_COMMISSIONED`
