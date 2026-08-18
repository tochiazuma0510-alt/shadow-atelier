# Luna reply 157dm — relative-Frattini-3 normalized inverse repair

Date: 2026-08-18

## Verdict

The dispatch blocker is repaired without changing the mathematical
predicate, candidate universe/order, Fox certificates, caps, or positive
terminal meaning.  Production no longer constructs a raw
`S^(order-1)` inverse word.

## Finite normalized inverse

The producer now reconstructs directly from the pinned q3 receipt:

- the authenticated normalized order-nine roof orbit;
- its unique canonical exponent-7 row;
- all 27 records of the authenticated fine correction fibre.

For each of the 27 exponent-7-plus-correction words it builds the six
`source_words_m0` images and tests both compositions against the fixed
exponent-2 six-image tuple in `E4`.  The receipt binds the exponent-7 row,
tested indices `1..27`, the full passing-index set, deterministic selected
index/word, selected six inverse words, and maximum inverse-word length.
If more than one passes, the first registered index is selected and the full
passing set remains recorded.  No componentwise Q4/Pi4 inverse words are
combined.

The selected finite inverse tuple is cached under the exact ordered tuple of
six E4 source images.  Every search candidate independently evaluates its
own six-image tuple.  A match replays ST and TS in E4 and then independently
builds that candidate's S-relations, T-relations, ST/TS words, Fox gradients,
and sparse ledgers.  Acceptance and certificates are never cached.  A tuple
mismatch has no raw-power fallback: it is recorded as candidate-local
`missing_bounded_inverse_representative`, and an otherwise empty run becomes
`B345_RELFRAT3_UNKNOWN_RESOURCE`.  Cache hits, misses, tuple-match/mismatch
counts, and maximum inverse length are bound in the search receipt.

The independent checker reconstructs the same exponent-7 × 27 finite test
from the pinned q3 data, compares the entire normalized-inverse receipt,
reconstructs the selected candidate's inverse and all literal target words,
and replays both compositions.  It does not trust the producer's cache
booleans as positive evidence.

## Terminal hardening and logging

`B345_RELFRAT3_MISSING_MATCHED_CHAIN` and
`B345_RELFRAT3_PROJECTED_OBSTRUCTION` were removed from the producer,
checker, and driver terminal sets.  Neither branch is implemented in this
v1, so even a supplied projection boolean cannot make either token valid.
Mutations to both unsupported tokens are rejected fail-closed; the checker
contains a canary for each.

Per the updated task, the optional live tee was not added.  Producer and
checker logging remain redirected exactly as before; this is operational
only and changes no predicate.

## Audit

The one authorized lightweight combined selftest passed:

```text
D972_B345_RELFRAT3_PRODUCER_SELFTEST_PASS relevant_formula_sha256=5b66299d255964ff8afa9e9d75e9a5d61d767fd76539fd3c6ae94acd65039127 normalized_inverse_cache_hit_canaries=1
D972_B345_RELFRAT3_CHECKER_SELFTEST_PASS mutations=4 fox_orientation_canaries=2
```

The producer canary uses two distinct free representatives inducing the
same exact toy E4 endomorphism and confirms two hits of the same finite
inverse tuple.  After this sole permitted execution, the final unsupported-
projection audit removed `PROJECTED_OBSTRUCTION` and added a fifth mutation
canary.  That last fail-closed edit and the resulting SHA chain were checked
statically; the selftest was not run a second time.  No GAP, GHA, Git, or
production computation was run.

## Final files and SHA-256

```text
search/d972_b345_relfrat3_v1.py
  77505 bytes
  4b73fbfe19bb33a9decdec5fda437f58f61a3ecb1989090bd08151f60ce6609e

search/check_d972_b345_relfrat3_v1.py
  52315 bytes
  3d86240237229b250943c4795c24c32ac75af9229534c73d16bd838f6d6d0101

search/d972_b345_relfrat3_gha_driver_v1.g
  6811 bytes
  fce9b3ba8c9b686fb6af2bd5a6da1b29f7486616948a6907982af14cd5d8738b
```

B345_RELFRAT3_NORMALIZED_INVERSE_GO
