# Luna task 393: task193-v4 -> A5/A7 live-pin successor

Role: **Luna implementation/compute reinforcement**.  Perform the complete
bounded pin migration below.  Preserve the accepted A5/A6/A7 mathematics and
the representative-complete streaming dovetail.

## 1. Frozen input owners

```text
search/d972_r07_zero_base_a5_a6_compiler_v3.py
  59239 bytes c287011d5e573452094e62c76020ab4b1076bc427103174b1771a22a1bb4fbd8
crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v3.py
  45942 bytes e86806444efa146954213da4bbb13726a8b5dc79b16c0a4b97aaa5c7b05b1cb0
search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v3.g
  4255 bytes 5cac3f9ff13ef2697e14275376beb17b2272da824d0f50458e3794208a09c392
search/d972_r07_direct_relator_a5_a7_fusion_v5.py
  57482 bytes ce9c6b0d7ba587f877634b60e0162f8ad3f60091b182b3031775b512f719f2ff
crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v5.py
  29559 bytes e651ad1909e3a50152e9ff7574b6a3f7dddf841402fff04ef809c81e940ccfba
search/d972_r07_direct_relator_a5_a7_fusion_gha_driver_v5.g
  6675 bytes 5f1aefba79c4fde1c5a0688a62a83effe3bb590e16c016c95a6797514d6f2dea
```

The new live task193 owners are exactly:

```text
search/d972_r07_second_frattini_affine_prefix_compiler_v4.py
  2851 bytes a6e1d54c1c656ab496ed54e6bcac5fa8c027edc5686fa913c86cc1c0fe349d1a
crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v4.py
  2986 bytes 04f7c7df3395e841a21fe75fec71bd5fef1f35a4fbc4c0e642b5db7fa31e390d
search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v4.g
  5798 bytes 7447b2da4c83ba0f9818a3ea355636310368b22c8585e6b95632100894dfafb4
```

Fail closed on every pin mismatch.

## 2. Zero-base loader successor

Create a v4 successor of the zero-base A5/A6 producer/checker/driver which:

1. changes only the task193 schema, accepted terminal, checker schema and
   exact three physical pins from task193 v3 to v4;
2. advances its own schema/checker terminal/checkpoint/owner labels and all
   output paths cleanly to v4;
3. preserves `load_task193`, A5 arithmetic, candidate order, resource caps,
   MEMBER/NONMEMBER/UNKNOWN boundaries and checker independence; and
4. adds no eager roster, retry, fallback or slow path.

## 3. Direct-relator fusion successor and fail-fast order

Create a v6 successor of task377-v5 which pins the new zero-base-v4 owner
and checker, its driver, and task193-v4 producer/checker/driver.  Preserve
the v5 mathematics, canonical literal owner, task292 binding, checkpoint,
sidecar, representative-complete streaming Schreier/translation dovetail and
all claim boundaries.

Make one performance-neutral ordering repair in producer and checker:

- authenticate/load task193 immediately after loading the pinned zero-base
  module and before constructing the task198 `AuthorityAdapter`/`Authority`,
  `Runtime`/`CheckerArithmetic`, or `BoundaryLedger`/`Boundary`;
- only after task193 is positive may the 6,441-row task198 authority and
  boundary owners be built;
- producer receipt parsing may remain after those owners where the replay
  needs them, but an invalid task193 input must fail before their construction.

Advance all task193 owner keys from v3 to v4, all task377 schema/terminal and
fresh receipt/verdict/checkpoint/sidecar/log/sentinel paths to v6.  Do not
change the ordering or membership semantics inside the dovetail.

## 4. Exact output files

Create only:

```text
search/d972_r07_zero_base_a5_a6_compiler_v4.py
crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v4.py
search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v4.g
search/d972_r07_direct_relator_a5_a7_fusion_v6.py
crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v6.py
search/d972_r07_direct_relator_a5_a7_fusion_gha_driver_v6.g
sol/luna_reply_393_r07_task193_v4_a5_a7_live_pin_v1.md
```

Do not modify an existing file.

## 5. Bounded static acceptance

Check physical and generated pins, wrapper patch cardinalities, Python AST
compile/load without `main`, full owner-pin closure, stale v3/v5 generated
owner absence, ASCII GAP parse-only, fresh path closure, and a source/AST
audit that the only task377 executable change besides version text is the
task193 fail-fast move.  Explicitly confirm no full
Schreier-by-translation roster is pre-materialized.

No production, GHA, SELFTEST, heavy local calculation, mutation campaign,
git or network.  Report exact physical/generated hashes and residual risk.

`TASK393_R07_TASK193_V4_A5_A7_LIVE_PIN_COMMISSIONED`

