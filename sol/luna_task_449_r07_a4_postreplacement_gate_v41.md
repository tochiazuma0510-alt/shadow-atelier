# Luna task 449 — A4 v40 post-replacement gate v41

Role: Luna implementation owner.  This is a bounded driver-only repair after
GHA run 33505699434.  Do not change v22 producer, v28 checker, arithmetic,
checkpoint cadence, embedded base/delta/HEAD bytes, or production resources.
Do not run production, GHA, git, commit, or push.

## Exact diagnosis

Run 33505699434 received the correct preamble `D386Mode:="RESUME";;`, loaded
all packages, and stopped before the inner production driver with
`task446 post-replacement gate`.

In v40 `D446Pairs[7]`, the replacement inserts delta and HEAD seed calls
immediately before the unchanged checker checkpoint seed call.  Therefore the
old checker-seed substring is deliberately a suffix of the replacement string:
after the unique replacement its count is 1, not 0.  `D446ReplaceOnce` already
authenticated that the pre-replacement count was exactly 1.  The generic
post-loop test incorrectly requires zero old occurrences for this one
self-containing pair.

## Authorized outputs only

1. `search/d972_r07_word_independent_successor_kernel_gha_driver_v41.g`
2. `sol/luna_reply_449_r07_a4_postreplacement_gate_v41.md`

## Required repair

- Make v41 an exact SHA-pinned wrapper successor to v40; do not overwrite v40.
- Patch only the redundant post-replacement cardinality gate.  Pairs 1--6
  retain `old count = 0` and `new count = 1`.  Pair 7 must require
  `old count = 1` and `new count = 1`, because its new string contains its old
  checker-seed suffix exactly once.
- Preserve v40 execution and artifact paths.  Do not rewrite version strings,
  seed material, or the inner production driver beyond that gate.
- Fail closed on v40 byte/SHA drift, replacement cardinality drift, patched
  source byte/SHA drift, write/readback drift, or any unexpected count.
- Statically reconstruct through the repaired gate and report exact bytes/SHA,
  plus confirmation that the resulting v40 inner driver is still 76,586 bytes
  / `f407a306d25a0ace6bd347615195d94c2f4bc73625dbe9ac055fd02d5ea3961f`.
  Confirm seed order and row-26 HEAD are unchanged.

No new SELFTEST or full computation belongs in production.
