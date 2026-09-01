# Luna task 494 — rank-99 compiled-formula prefix replay repair v5

Role: Luna implementation only.  This is an urgent, surgical successor to the
independently audited v4 owner.  Do not change the search order, finite
universe, batching, checkpoint semantics, resource limits, or mathematics.
Do not modify existing files and do not run production/GHA/git.

## 1. Exact observed failure

GHA run `33551170421`, job `100000701817`, immutable head
`15f8dce96c5bdbeac8a3c3fa3662606bcfe315b0`, reached all selective-runtime
construction phases and then returned a 376-byte canonical UNKNOWN result
with exact reason `'constant'`.  Artifact `9817670360` has API zip digest
`8b1501cdaee7a305f9df161c12f80534236d28e32241c0e6922bcb0e847b1edb`.
Its 356146-byte checkpoint has SHA-256
`fc43d0bedd482ef029660fa86cf625a64ca1a26c9e2c4baf48f3229ff2ffac7a`
and remains the normalized C99 BOOTSTRAP state rank/count/batches/round
`99/56/3/12`, seal
`b9761eefb702179ea547d57af3fe5489bff1e5d2a8102bb057f654bcaf0f74ff`.
No new row or mathematics ran.

The exact defect is already localized:

- `formula_bundle` converts the Task179 occurrence formula into the compiled
  selector shape
  `{seed_index, K, merged, required_coordinates}`;
- producer `selector_literal` line 681 and independent checker
  `selector_literal` line 562 pass that compiled object to
  `model.formula_scalar`, whose ABI is the original occurrence shape with a
  `constant` member;
- therefore replaying the first frozen correction raises
  `KeyError('constant')` before READY;
- the correct compiled scalar is
  `(K + sum(v for (coordinate,target),v in merged.items()
             if blobs[coordinate] == target)) mod 3`, exactly the existing
  pinned rank-ladder-v2 `formula_scalar(model,f,blobs)` ABI.

The raw identity check inside `formula_bundle` is different and must remain
`model.formula_scalar(raw_formula, ids)`: that call correctly uses the original
Task179 shape.  Do not globally replace raw formula evaluation.

## 2. Frozen v4 pins

- producer 98576 bytes / SHA-256
  `5b8f3ae76abb64768decb14be50fbd6d75b5e84aeaad2b1a63fcb544933cf36f`;
- checker 66212 bytes / SHA-256
  `cd0acf346d4f133dfaa8e047db6593511a5423c6a166060a37fc313504e928e7`;
- driver 9424 bytes / SHA-256
  `948f6254298eef51d524e834441c530ecb1a5a3a5cbefbdfe3dac9e7922d0ff8`;
- binding
  `d5777bc12023298808fa7f0637de47e072af0bf8137c7922ce4c0cd17c7327be`.

Task492's D1--D6 and base/BOOTSTRAP GO ruling remains the premise.  V5 must
change only the compiled-formula replay ABI plus version/schema/marker/pins.

## 3. Required versioned outputs

Create only:

1. `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py`
2. `crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py`
3. `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v5.g`
4. `sol/luna_reply_494_r07_rank99_compiled_formula_replay_repair_v5.md`

No cache or fixture file in the repository.

## 4. Surgical implementation contract

Define a small compiled-formula scalar helper independently in producer and
checker.  It must require:

- integer `K` modulo 3;
- mapping-shaped `merged` with `(int, bytes)` keys and coefficients modulo 3;
- coordinate bounds against the supplied blob tuple;
- exact byte equality at the selected target;
- result in `{0,1,2}`.

Use that helper in every path that evaluates a compiled formula: frozen-prefix
`selector_literal` and live retained-correction evaluation.  Keep the raw
Task179 `model.formula_scalar(raw_formula, ids)` identity checks unchanged.
Producer and checker must not import one another.

Preserve the v4 production-used retained-candidate helper, D1--D6 fixes,
normalized BOOTSTRAP predecessor, zero-progress carry-forward, exclusive
RESOURCE/COMMON markers, one producer/conditional-one-checker driver, and all
limits verbatim.  The driver must pin the final v5 producer/checker hashes and
use distinct v5 paths/markers.  It must not accept v4 output as v5 output.

## 5. Required bounded regression gates

In addition to the complete v4 fixture/self-test/pin battery, add a regression
that would fail with the observed bug:

1. construct a raw Task179-shaped formula containing `constant` and a compiled
   selector formula containing `K` but no `constant`;
2. prove the raw identity lane still uses the raw evaluator;
3. prove both producer and checker compiled helpers return the same expected
   scalar on at least constant-only, one-hit, non-hit, cancellation, and
   coordinate-bound cases;
4. explicitly call the frozen-prefix selector/replay ABI with a compiled
   formula and show it does not request `constant`;
5. reject a compiled object that substitutes `constant` for `K` or malformed
   `merged` data.

Run AST/compile, producer FIXTURE, checker self-test and pin-check, exact driver
pin checks, generated-shell syntax, and bounded GAP parse.  Do not rebuild the
full selective runtime locally merely to reproduce four minutes of GHA work.

The reply must give exact v4-to-v5 semantic diff locations, final bytes/hashes,
all commands, and confirm no production result.  End exactly with one of:

`TASK494_R07_RANK99_COMPILED_FORMULA_REPLAY_REPAIR_V5_PASS`

or

`TASK494_R07_RANK99_COMPILED_FORMULA_REPLAY_REPAIR_V5_STOP`

