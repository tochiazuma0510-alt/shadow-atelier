# Sol(max) task 495 — audit rank-99 compiled-formula replay repair v5

Role: independent mathematical/implementation audit only.  Do not edit the
three implementation files, run production/GHA, or broaden the search.
Write only
`sol/sol_reply_495_audit_r07_rank99_compiled_formula_replay_repair_v5.md`.

## 1. Exact candidate pins

- producer
  `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py`,
  104031 bytes, SHA-256
  `25c308ec11b9f36cc9779dfec46058a4956068969d664ee582a26f9cb0db7c09`;
- checker
  `crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py`,
  71589 bytes, SHA-256
  `970ffe3a78687f3a27a222e089ae3d5e928bbfa048b9aef9f51fcf4c0b5d578d`;
- driver
  `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v5.g`,
  9425 bytes, SHA-256
  `bed9105b36fef5e59120d954029ec507b16f393ab2859a7599867a19156b1b5d`;
- claimed binding
  `0e0123e99309a768910e150d5bf4725295a0dc35eab7e15eac66538a3a37d56b`.

Read the full Task494 commission and Luna reply.  The v4 trio and Task492 GO
ruling are the immutable comparison premise.

## 2. Audit question

Decide only whether v5 is safe for immediate GHA dispatch from the same C99
rank99/56 prefix after v4 run `33551170421` failed with `KeyError('constant')`.

Independently establish:

1. the observed exception is explained by the v4 compiled/raw ABI mismatch;
2. the raw Task179 identity lane still evaluates the original
   `{constant,merged,...}` object with `model.formula_scalar`;
3. every compiled selector lane evaluates `{K,merged,...}` using the new
   formula `K + sum(hit coefficients) mod 3`, independently in producer and
   checker, and no compiled object reaches the raw evaluator;
4. this compiled formula is extensionally the pinned rank-ladder-v2 ABI and
   is correctly applied both to frozen-prefix replay and live retained
   candidates;
5. v4-to-v5 differences outside version/schema/marker/default paths, the
   helper calls, and bounded regressions do not alter search order, finite
   universe, action-first policy, batching, state/segment/checkpoint behavior,
   resource caps, or COMMON/RESOURCE ownership;
6. driver pins the exact final files, invokes one producer and at most one
   COMMON-only checker, and cannot accept v4 markers/files as v5;
7. Task492 D1--D6 and normalized BOOTSTRAP/zero-progress fixes remain present.

Pay special attention to formula shape, byte-target comparison, coefficient
normalization, coordinate bounds, and whether any raw/compiled call remains
ambiguous.  A cosmetic or optional improvement is not a STOP.  STOP only for
an executable soundness/dispatch defect and give an exact reproducer.

## 3. Bounded checks

Reproduce independently, without full selective-runtime construction:

- exact file hashes and binding;
- AST/call-target diff audit;
- producer fixture;
- checker self-test and pin-check;
- exact driver pin/marker/path/resource-limit audit;
- generated shell `bash -n` and bounded GAP `ReadAsFunction` if available.

No production result is expected.  State mathematical status `UNCHANGED`.
End the reply with exactly one of:

`GO_FOR_GHA_DISPATCH`

or

`STOP_WITH_EXACT_DEFECTS`

