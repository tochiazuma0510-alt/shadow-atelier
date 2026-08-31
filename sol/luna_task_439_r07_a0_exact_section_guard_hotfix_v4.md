# Luna task 439 - exact-section guard hotfix v4

Run `33407759683` crossed both prior ABI failures, compiled all 44 formulae,
completed the exact Q0 roster of 1,469,664 states and the S0--S2 membership
indices, then stopped on the first singleton reconstruction with exact reason
`selective singleton replay`.

The defect is now localized by comparison with the pinned Task179
`FibreOracle.canonical` lines 945--974.  Task436 v1 looks up a Q0 state only
by the 36-byte coarse permutation and immediately replays it.  The reference
implementation first compares the stored full 40-byte section element with
`section_target` and skips the coarse collision when they differ.  Restore
that exact guard.  This is not a new search, closure, or mathematical change.

## 1. Allowed outputs

Create only:

1. `search/d972_r07_a0_actual_b72_first_active_v4.py`
2. `crosscheck/check_d972_r07_a0_actual_b72_first_active_v4.py`
3. `search/d972_r07_a0_actual_b72_first_active_gha_driver_v4.g`
4. `sol/luna_reply_439_r07_a0_exact_section_guard_hotfix_v4.md`

Do not overwrite v1--v3 or modify any other file.  No local production, Q0,
commit, push, dispatch, download, workflow edit, or framework repair.

## 2. Producer

Use the exact Task436 v1 producer as the algorithmic source and make only the
following versioned changes:

- retain the already accepted p176 dict-plus-attribute adapter and
  `base["load_json"] = t413["load_json"]` bootstrap adapter from v3, installed
  before the unchanged production run;
- in selective `SF.canonical`, after the coarse `qid` lookup, recover the
  literal 40-byte stored section at that coordinate and require equality with
  `st` by `continue` on inequality, exactly as Task179 lines 960--965 do;
- only after that equality may the q0/gamma word and ten-coordinate replay be
  constructed;
- use v4 schema, marker, output/checkpoint/log paths.

Do not broaden the fibre, add a second lookup table, rebuild all ten stores,
resume occurrence closure, or weaken any assertion/status gate.  Preserve
positive-first order and EMPTY rejection.

Add a bootstrap-free toy fixture which gives two records with the same coarse
prefix and different 40-byte full values, and demonstrates that the wrong
full value is skipped while the exact value is accepted.  This fixture must
not enumerate Q0.

## 3. Independent checker and driver

The checker must independently retain both bootstrap adapters and all v1
ACTIVE/resource/status gates, use only v4 schema/marker, and not import the
producer.  Extend its self-test with an independent coarse-equal/full-unequal
rejection toy, followed by the unchanged ten mutation rejections.

The driver must pin exact v4 producer/checker bytes and SHA-256, require the
external v4 preamble, use fresh v4 result/checkpoint/log paths, retain the
2,400-second and 4.8-GB producer caps, and require both PASS markers.

Run only syntax compilation, producer toy fixture, checker self-test, static
driver pin/command reconstruction, and `git diff --check`.  Report exact
bytes/SHA-256.  Stop after these bounded gates.
