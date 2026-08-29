# Luna task 391 — A0 v22 -> adapter v5 -> task193 v4 live-pin successor

## Role and objective

You are Luna.  This is a bounded mechanical exact-pin migration.  The active
A0 production owner is v22, but the only current adapter v4 accepts A0 v20,
and task193 v3 accepts only that adapter.  Build the minimal versioned
successors so a future accepted A0-v22 artifact has a nonempty path into the
unchanged task193 affine-prefix mathematics.

Do not redesign arithmetic, search order, receipt meaning, UNKNOWN
semantics, or resource policy.  Do not run production, GHA, SELFTEST, git,
network, mutation campaigns, or heavy calculation.

## Frozen live A0 owners

Pin exactly this one family; do not add an OR gate for older A0 versions:

```text
search/d972_r07_history_free_positive_fast_resume_v22.py
  bytes 3280
  sha256 1cc875afb05b7c3db189d7a77fd6d9d4e2604610a0af6a383895011ecbdd0d01
crosscheck/check_d972_r07_history_free_positive_fast_resume_v22.py
  bytes 2066
  sha256 4c79b841b5ce003e4d2eefaf1320e878aab400c20ef1a23e4f2900ea61e5cf13
search/d972_r07_history_free_positive_fast_resume_gha_driver_v22.g
  bytes 8266
  sha256 8b8f2e9a1dc0b6a30e61ab8866c8d2393328a7038c22323873350d91d5b6531d
```

## Required output files

Create only these versioned files plus the reply:

```text
search/d972_r07_history_free_task193_compat_adapter_v5.py
crosscheck/check_d972_r07_history_free_task193_compat_adapter_v5.py
search/d972_r07_history_free_task193_compat_adapter_gha_driver_v5.g
search/d972_r07_second_frattini_affine_prefix_compiler_v4.py
crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v4.py
search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v4.g
sol/luna_reply_391_r07_a0_v22_task193_live_pin_v1.md
```

Do not modify any existing file.

## Adapter v5 contract

1. Restore or wrap the exact accepted adapter-v4 producer/checker semantics
   by byte/sha pin and unique patch sites.
2. Replace only the physical A0 producer/checker pins with the v22 family
   above; advance adapter schema, checker schema, terminal family, module
   labels and fresh v5 output paths consistently.
3. The v5 driver must exact-pin all three A0-v22 physical owners and the new
   adapter-v5 producer/checker.  It remains production-only, accepts only
   allowlisted `ci/in/` receipt/verdict paths, rejects stale outputs, and
   preserves the current accepted-versus-typed-UNKNOWN terminal boundary.
4. A v22 receipt is accepted only when the independent v22 verdict already
   accepts the same positive A0 result.  Workflow success or an
   `UNKNOWN_RESOURCE` receipt must not become adapter acceptance.

## Task193 v4 contract

1. Restore or wrap the exact task193-v3 producer/checker mathematics by
   byte/sha pin and unique patch sites.
2. Replace only the adapter schema/terminal/checker-schema and physical
   producer/checker pins with the new adapter-v5 owners.  Advance task193
   schema, checker schema, terminal family and checkpoint schema to v4.
3. The v4 driver exact-pins adapter-v5 producer/checker/driver and task193-v4
   producer/checker, uses fresh v4 receipt/verdict/checkpoint/log/sentinel
   paths, and preserves the all-or-none resume and typed
   `UNKNOWN_INPUT`/`UNKNOWN_RESOURCE` contracts.
4. Do not add retries, broad fallback versions, eager rosters, SELFTEST-only
   work, or any computation not already present in task193 v3.

## Bounded static acceptance

In memory only, check exact owner restoration, patch cardinalities,
resulting source SHA pins, Python AST parse/compile without entering main,
ASCII for GAP wrappers, stale-version/path absence in the generated owners,
and full pin closure.  Explicitly report whether any new slow path was added
(the required answer should be no).

Record physical bytes/SHA-256 and, for wrapper-generated Python, resulting
generated-source bytes/SHA-256 in the reply.  State clearly that no
production/SELFTEST/GHA result is claimed.

End the reply with:

```text
TASK391_A0_V22_TASK193_LIVE_PIN_COMMISSIONED
```
