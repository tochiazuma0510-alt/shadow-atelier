# Luna task 392: A0 v23 pre-heavy worker fork

Role: **Luna implementation/compute reinforcement**.  This is a narrowly
scoped mechanical successor of A0 v22.  Do not change the mathematical
search, candidate order, checkpoint ABI, resume semantics or terminal
meaning.

## 1. Frozen input owner

Use exactly these physical v22 owners:

```text
search/d972_r07_history_free_positive_fast_resume_v22.py
  3280 bytes
  1cc875afb05b7c3db189d7a77fd6d9d4e2604610a0af6a383895011ecbdd0d01
crosscheck/check_d972_r07_history_free_positive_fast_resume_v22.py
  2066 bytes
  4c79b841b5ce003e4d2eefaf1320e878aab400c20ef1a23e4f2900ea61e5cf13
search/d972_r07_history_free_positive_fast_resume_gha_driver_v22.g
  8266 bytes
  8b8f2e9a1dc0b6a30e61ab8866c8d2393328a7038c22323873350d91d5b6531d
```

Fail closed if any pin differs.  Inspect the generated v22 owner; do not
edit an unpinned historical source in place.

## 2. The only semantic repair

The generated producer currently performs the replacement two-worker fork
after `build_heavy`.  Move creation/start of that replacement worker pair to
the interval after the light checkpoint is sealed and before `build_heavy`.
Only the parent then executes `build_heavy`.

The worker arithmetic used by the disjoint pair must remain on the light
runtime it already consumes.  Preserve exactly:

1. the same two disjoint worker slices and their order;
2. all candidate ordinals, predicates, budgets and accepted-set semantics;
3. old-owner abort/join, replacement-owner lifecycle and final cleanup;
4. the v22 live/prepool checkpoint bodies, source identity, resume cursor,
   atomic write and byte caps;
5. the 10800-second internal and 11100-second external bounds; and
6. every heavy structure and lookup result used by the parent search.

Do **not** implement the separate scalar-gating, row-sharing, streaming JSON,
cache or checker optimizations in this task.  They are intentionally outside
the minimal memory repair.

## 3. Exact versioned outputs

Create only:

```text
search/d972_r07_history_free_positive_fast_resume_v23.py
crosscheck/check_d972_r07_history_free_positive_fast_resume_v23.py
search/d972_r07_history_free_positive_fast_resume_gha_driver_v23.g
sol/luna_reply_392_r07_a0_preheavy_fork_v23.md
```

Advance all owner schema/terminal/path/pin labels cleanly to v23.  The v23
checker must independently pin the final v23 producer.  The v23 driver must
pin both files, retain the optional exact resume triple, and preserve the
same fail-closed typed terminal grammar.  It must not silently accept v22
receipts as v23 receipts.

## 4. Bounded static acceptance

Perform only bounded static checks:

1. physical bytes/SHA-256 for all frozen inputs and all final outputs;
2. wrapper definition-load and generated-source compilation;
3. a generated v22/v23 AST or textual audit proving the worker start moved
   before `build_heavy` and no other search statement changed except required
   version/pin text;
4. prove the parent alone calls `build_heavy`, the replacement workers are
   live before it, and worker code references no heavy-only object;
5. GAP `ReadAsFunction` parse-only for the driver; and
6. ASCII-only executables plus `git diff --check` on the four outputs.

No production run, heavy local run, SELFTEST, mutation campaign, GHA,
workflow dispatch, git operation or network access.  Report all exact hashes,
the moved statement interval and any honest residual risk.

`TASK392_R07_A0_V23_PREHEAVY_FORK_COMMISSIONED`
