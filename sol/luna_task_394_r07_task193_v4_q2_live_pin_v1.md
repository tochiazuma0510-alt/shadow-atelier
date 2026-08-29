# Luna task 394: task193-v4 actual-q2 live-pin successor

Role: **Luna implementation/compute reinforcement**.  This is a pin-only
versioned successor of the existing actual A0 class-two q2 owner.

## 1. Frozen inputs

```text
search/d972_r07_actual_a0_class_two_q2_v1.py
  50355 bytes c61d8f2cd96e6dd5c36089ddb83f6519c5e42b0dac66b42e9cec46ca9adfe9a6
crosscheck/check_d972_r07_actual_a0_class_two_q2_v1.py
  51554 bytes 0b2d944d1655c359ab7252a732fe99f3c92add8e7ea9d45d44825707698deaa0
search/d972_r07_actual_a0_class_two_q2_gha_driver_v1.g
  8218 bytes eb80e5ae0b2ae5d9cbb99e7eda38d40da31f7037779f31feca8fec11bc886d9c

search/d972_r07_second_frattini_affine_prefix_compiler_v4.py
  2851 bytes a6e1d54c1c656ab496ed54e6bcac5fa8c027edc5686fa913c86cc1c0fe349d1a
crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v4.py
  2986 bytes 04f7c7df3395e841a21fe75fec71bd5fef1f35a4fbc4c0e642b5db7fa31e390d
search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v4.g
  5798 bytes 7447b2da4c83ba0f9818a3ea355636310368b22c8585e6b95632100894dfafb4
```

Fail closed on drift.

## 2. Exact successor

Create only:

```text
search/d972_r07_actual_a0_class_two_q2_v2.py
crosscheck/check_d972_r07_actual_a0_class_two_q2_v2.py
search/d972_r07_actual_a0_class_two_q2_gha_driver_v2.g
sol/luna_reply_394_r07_task193_v4_q2_live_pin_v1.md
```

Restore/wrap the exact v1 producer/checker semantics.  Change only:

1. task193 schema/terminal/checker schema and exact physical pins v3 -> v4;
2. q2 owner schema/checker schema/checkpoint schema/terminal family v1 -> v2;
3. task193 provenance labels v3 -> v4; and
4. driver source pins plus fresh v2 receipt/verdict/checkpoint/log/sentinel
   paths.

Preserve the actual class-two arithmetic, occurrence order, resource and
resume policy, COMPLETE/UNKNOWN semantics, all independent replay, and the
claim boundary.  Add no retry, fallback, SELFTEST branch, eager roster or
new calculation.

## 3. Bounded static acceptance

Check physical/generated SHA-256 and bytes, exact wrapper cardinalities,
Python AST compile/load without main, full pin closure, absence of stale
task193-v3 and q2-v1 identifiers in generated owners, ASCII GAP parse-only,
fresh path closure and unchanged executable AST modulo the enumerated literal
changes.

No production, GHA, SELFTEST, heavy local calculation, mutation campaign,
git or network.  Report exact physical/generated hashes and residual risk.

`TASK394_R07_TASK193_V4_Q2_LIVE_PIN_COMMISSIONED`
