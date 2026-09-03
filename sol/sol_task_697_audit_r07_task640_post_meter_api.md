# Sol(max) Task697 — bounded post-Meter API compatibility audit

## Purpose

GHA v8 is currently spending about twelve minutes on the accepted Task625
replay.  Without changing or delaying that run, inspect the already released
fresh-rho2 producer for any **deterministic immediate interface mismatch after
the repaired v12f `Meter` construction**.  This is a code/API audit only, not
a new mathematical or security audit.

## Frozen inputs

- `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`, release
  SHA-256 `684c629eef8100175b676a4e4762db18f67e5a99672b4107facc7dad412acfc2`.
- `search/d972_r07_history_free_positive_fast_resume_v12f.py`, producer pin
  embedded in the first file.
- `search/d972_r07_a0_first_rung_grade2_prebuild_v1.py`, pin embedded in the
  first file.
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v8.yml`, SHA-256
  `ebc77080a5b51626ea170362bb3b6de441c7530694ce6387fae5a79e0705c5e6`.

## Exact questions

1. Resolve the actual types returned by `load_all_seven()` and check every
   subsequent attribute/method call and expected return shape on
   `ProducerAllSeven`, its runtime, `Context`, and the prebuild arithmetic.
2. Check names and call signatures from `signature`, `extend_signature`,
   endpoint/base gates, `coordinates`, `direct_column`, source-word tags,
   `act_precision2`, `aggregate_precision2`, and direct target construction.
3. Report any call that must fail deterministically before real arithmetic can
   proceed, with the single minimal repair.  Do not speculate about data-
   dependent mathematical outcomes or resource time.
4. If no deterministic mismatch is found, say `PASS_POST_METER_API`.

Do not edit code, run the heavy producer/checker, commission further audit,
or touch git/GHA.  Write only
`sol/sol_reply_697_audit_r07_task640_post_meter_api.md`, including exact input
and reply hashes.  `verified=false`.
